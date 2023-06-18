

    // Retrieve the values from localStorage
    var value1 = localStorage.getItem("currentGenre");
    var value2 = localStorage.getItem("currentSong");
    //localStorage.removeItem("bpm");

    // Display the values on the page
    document.getElementById("displayValue1").textContent = value1;
    document.getElementById("displayValue2").textContent = value2;

    $(document).ready(function() {
        // Send MIDI command on button click
        $('#start-button').click(function() {
            sendMidiCommand('start');
        });

        $('#stop-button').click(function() {
            sendMidiCommand('stop');
        });

        $('#pause-button').click(function() {
            sendMidiCommand('pause');
        });

        $('#fill-button').click(function() {
            sendMidiCommand('fill');
        });

        // Send MIDI command on button click
        $('#half-button').click(function() {
            sendMidiCommand('half');
        });

        $('#double-button').click(function() {
            sendMidiCommand('double');
        });

        $('#previous-button').click(function() {
            sendMidiCommand('previous');
        });

        $('#next-button').click(function() {
            sendMidiCommand('next');
        });


        // Function to send MIDI command via AJAX
        function sendMidiCommand(command) {
            $.ajax({
                url: '/send_midi',
                method: 'POST',
                data: {
                    command: command
                },
                success: function(response) {
                    console.log(response);
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            });
        }
    });

 
function displaySetlist() {
    document.addEventListener("DOMContentLoaded", function() {
        // Retrieve the setlist from local storage
        var setlist = JSON.parse(localStorage.getItem("setlist")) || [];

        // Get the setlist container element
        var setlistContainer = document.getElementById("setlist");

        // Clear the previous setlist items
        //setlistContainer.innerHTML = "";

        // Iterate over the setlist and create list items for each song
        setlist.forEach(function(song) {
            var listItem = document.createElement("li");
            listItem.textContent = song.genre + " - " + song.song;
            setlistContainer.appendChild(listItem);
        });

        // Update the setlist display in the accordion panel
        createSetlistAccordions(setlist);
    });
  }

function createSetlistAccordions(setlist) {
  // Get the setlist panel
  var setlistPanel = document.getElementById("setListPanel");

  // Clear the previous setlist
  setlistPanel.innerHTML = "";

  // Create a list for the current setlist
  var setlistList = document.createElement("ul");
  setlistList.classList.add("setlist-list");

  // Populate the list with current setlist items
  setlist.forEach(function (song) {
    var listItem = document.createElement("li");
    listItem.textContent = song.genre + " - " + song.song;
    setlistList.appendChild(listItem);
  });

  // Append the current setlist to the setlist panel
  setlistPanel.appendChild(setlistList);

}



    function toggleGenre(genreButton) {
        console.log("func toggleGenre");
        // Get the currently active genre button
        var activeButton = document.querySelector(".accordion.active");

        // Remove the active class from the currently active genre button
        if (activeButton) {
            activeButton.classList.remove("active");
            activeButton.nextElementSibling.style.display = "none";
        }

        // Toggle the active class for the clicked genre button
        genreButton.classList.toggle("active");

        // Toggle the display of the corresponding panel
        var panel = genreButton.nextElementSibling;
        if (genreButton.classList.contains("active")) {
            panel.style.display = "block";

            // Create accordion buttons for the selected songs
            var genreCode = genreButton.dataset.genreCode;
            createSongAccordions(panel, genreCode);
        } else {
            panel.style.display = "none";
        }

        // Update the selected genre and song in the header
        var selectedGenre = genreButton.textContent;
        var selectedSong = genreButton.nextElementSibling.querySelector(".active");
        var selectedSongText = selectedSong ? selectedSong.textContent : "";
        updateHeader(selectedGenre, selectedSongText);
    }



    function createSongAccordions(panel, genreCode) {
        console.log("func createSongAccordions");
        var selectedSongAccordion = document.getElementById("selectedSongAccordion");
        selectedSongAccordion.innerHTML = ""; // Clear previous accordions

        var genreConfigPath = `{{ homedir_path }}/${genreCode}/config.csv`;

        fetch('/get_songs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    genreCode: genreCode
                }),
            })
            .then((response) => response.json())
            .then((data) => {
                data.forEach((song, index) => {
                    var button = document.createElement("button");
                    button.className = "accordion song-accordion";
                    button.textContent = song;

                    button.addEventListener("click", function() {
                        selectSong(this.textContent);

                        // Update the header with the selected genre and song
                        var selectedGenre = document.getElementById("selectedGenreHeader").textContent;
                        updateHeader(selectedGenre, this.textContent);
                    });

                    var songPanel = document.createElement("div");
                    songPanel.className = "panel";
                    songPanel.appendChild(document.createTextNode(song));

                    selectedSongAccordion.appendChild(button);
                    selectedSongAccordion.appendChild(songPanel);

                    // Select the first song by default
                    if (index + 1 === 1) {
                        button.classList.add("active");
                        selectSong(song);
                    }
                });

                selectedSongAccordion.style.display = "block";

                // Add event listeners to the song accordions
                var songAccordions = selectedSongAccordion.getElementsByClassName("song-accordion");
                for (var j = 0; j < songAccordions.length; j++) {
                    songAccordions[j].addEventListener("click", function() {
                        var isActive = this.classList.toggle("active");
                        // closeOtherSongAccordions(this);

                        if (isActive) {
                            // Retrieve the selected genre and song
                            var selectedGenre = document.getElementById("selectedGenreHeader").textContent;
                            var selectedSong = this.textContent;
                            console.log("func createSongAccordions.is active");
                            // Update the header with the selected genre and song
                            updateHeader(selectedGenre, selectedSong);
                        }
                    });
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }

    function selectSong(song) {
        var activeSongButton = document.querySelector(".selected-song-accordion .song-accordion.active");
        if (activeSongButton) {
            activeSongButton.classList.remove("active");
        }

        var selectedSongButton = document.querySelector(`.selected-song-accordion .song-accordion[data-song="${song}"]`);
        if (selectedSongButton) {
            selectedSongButton.classList.add("active");
        }

        document.getElementById("selectedSongHeader").textContent = song;
    }


    function updateHeader(genre, song) {
        document.getElementById("selectedGenreHeader").textContent = genre;
        document.getElementById("selectedSongHeader").textContent = song;
    }
    document.getElementById("setlistForm").addEventListener("submit", function(e) {
        e.preventDefault();
        console.log("running update");
        var genre = document.getElementById("selectedGenreHeader").textContent;
        var song = document.getElementById("selectedSongHeader").textContent;

        var genreInput = document.getElementById("genreInput");
        genreInput.value = genre;

        var songInput = document.getElementById("songInput");
        songInput.value = song;

        updateSetlist();
        displaySetlist();
    });
    document.getElementById("bbForm").addEventListener("submit", function(e) {
        e.preventDefault();

        var genre = document.getElementById("selectedGenreHeader").textContent;
        var song = document.getElementById("selectedSongHeader").textContent;

        var genreInput = document.getElementById("genreInput");
        genreInput.value = genre;

        var songInput = document.getElementById("songInput");
        songInput.value = song;

        sendToBeatBuddy();
    });
    $(document).ready(function() {
        var inputActive = false; // Flag to track if the input field is active

        // Trigger setTempo() function on Enter/Return key press
        $(document).on("keydown", function(e) {
            if ((e.keyCode === 13) && ($("#new_tempo").is(":focus"))) {
                setTempo();
                e.preventDefault(); // Prevent the default behavior of Enter/Return key
            }
        });

        var keydownCount = 0;
        var isProcessingKeydown = false;
        var idleDelay = 250; // Adjust this value as needed

        // Trigger adjustTempo(-1) function on Down Arrow key press
        $(document).on("keydown", function(e) {
            if (e.keyCode === 40) {
                if (!inputActive && !isProcessingKeydown) {
                    adjustTempo(-1);
                    e.preventDefault(); // Prevent the default behavior of Down Arrow key
                    isProcessingKeydown = true;
                    keydownCount++;
                    setTimeout(commitKeydownValue, idleDelay);
                }
            }
        });

        // Trigger adjustTempo(1) function on Up Arrow key press
        $(document).on("keydown", function(e) {
            if (e.keyCode === 38) {
                if (!inputActive && !isProcessingKeydown) {
                    adjustTempo(1);
                    e.preventDefault(); // Prevent the default behavior of Up Arrow key
                    isProcessingKeydown = true;
                    keydownCount++;
                    setTimeout(commitKeydownValue, idleDelay);
                }
            }
        });

        function commitKeydownValue() {
            // Do something with the keydownCount value
            console.log("Keydown count:", keydownCount);
            keydownCount = 0; // Reset the count
            isProcessingKeydown = false; // Reset the flag
        }

        // Set inputActive flag to true when the input field is focused
        $("#new_tempo").on("focus", function() {
            inputActive = true;
        });

        // Set inputActive flag to false when the input field loses focus
        $("#new_tempo").on("blur", function() {
            inputActive = false;
        });

        // Set focus back to the input field when a numeric key is pressed
/*         $(document).on("keypress", function(e) {
            if (isNumericKey(e.keyCode)) {
                $("#new_tempo").focus();
            } else {
                $("#search").focus();
            }
        }); */

        // Helper function to check if a key code corresponds to a numeric key
        function isNumericKey(keyCode) {
            return (keyCode >= 48 && keyCode <= 57) || (keyCode >= 96 && keyCode <= 105);
        }
    });

    function setTempo() {
        var newTempo = document.getElementById("new_tempo").value;

        // Send an AJAX POST request to the /set_tempo route
        $.post("/set_tempo", {
            new_tempo: newTempo
        }, function(data) {
            document.getElementById("current_tempo").innerText = data;
            document.getElementById("new_tempo").value = "";
            document.getElementById("new_tempo").blur(); // Remove focus from the input field
        });
    }

    function adjustTempo(adjustment) {
        // Send an AJAX POST request to the /adjust_tempo route
        $.post("/adjust_tempo", {
            adjustment: adjustment
        }, function(data) {
            document.getElementById("current_tempo").innerText = data;
            // document.getElementById("new_tempo").blur(); // Remove focus from the input field
        });
    }
    
	document.addEventListener('DOMContentLoaded', function() {
	  // Check the value of 'setlist' in localStorage
	  const setlistValue = localStorage.getItem('setlist');

	  // Get a reference to the button element
	  const toggleButton = document.getElementById('toggleButton');

	  // Parse the 'setlist' value as an array and check its length
	  const setlistArray = JSON.parse(setlistValue);
	  if (setlistArray && setlistArray.length > 0) {
		// 'setlist' is not empty, show the button
		toggleButton.style.display = 'block';
	  } else {
		// 'setlist' is empty, hide the button
		toggleButton.style.display = 'none';
	  }
	});	
    toggleButton.addEventListener('click', function() {
        var setListPanel = document.getElementById('setListPanel');
        var songListPanel = document.getElementById("genre-songs-container-id");
		var fileInput = document.getElementById("fileInput");
        if (setListPanel.style.display === 'none') {
            setListPanel.style.display = 'block';
            songListPanel.style.display = 'none';
        } else {
            setListPanel.style.display = 'none';
            songListPanel.style.display = 'block';
        }

    });

    // Retrieve set list from localStorage
    var setList = localStorage.getItem('setlist');
    if (setList) {
        setList = JSON.parse(setList);

        // Create accordion buttons for each item in the set list
        var setListPanel = document.getElementById('setListPanel');
        var activeAccordion = null;

        for (var i = 0; i < setList.length; i++) {
            var item = setList[i];
            if (!item) continue;

            var genre = item.genre.trim();

            var song = item.song.trim();

            var accordion = document.createElement('button');
            accordion.classList.add('accordion');
            accordion.textContent = genre + ' - ' + song;
            setListPanel.appendChild(accordion);

            var panel = document.createElement('div');
            panel.classList.add('panel');
            panel.textContent = 'Genre: ' + genre + ', Song: ' + song;
            setListPanel.appendChild(panel);

            // Add hidden input fields to store the values and their numeric counterparts
            var genreInput = document.createElement('input');
            genreInput.type = 'hidden';
            genreInput.name = 'genreNumber';
            genreInput.id = genre;
            genreInput.value = getNumericValue(genre);
            panel.appendChild(genreInput);

            var songInput = document.createElement('input');
            songInput.type = 'hidden';
            songInput.name = 'songNumber';
            songInput.id = song;
            songInput.value = getNumericValue(song);
            panel.appendChild(songInput);

            var removeButton = document.createElement('button');
            removeButton.classList.add('remove-button');
            removeButton.textContent = 'Remove';
            accordion.appendChild(removeButton);

            accordion.addEventListener('click', function() {
                if (activeAccordion === this) {
                    this.classList.remove('active');
                    var removeButton = this.querySelector('.remove-button');
                    removeButton.style.display = 'none';
                    activeAccordion = null;
                } else {
                    if (activeAccordion !== null) {
                        activeAccordion.classList.remove('active');
                        var activeRemoveButton = activeAccordion.querySelector('.remove-button');
                        activeRemoveButton.style.display = 'none';
                    }
                    this.classList.add('active');
                    var removeButton = this.querySelector('.remove-button');
                    removeButton.style.display = 'block';
                    activeAccordion = this;

                    // Log the genreNumber and songNumber values
                    var genreNumber = this.nextElementSibling.querySelector('input[name="genreNumber"]').value;
                    var songNumber = this.nextElementSibling.querySelector('input[name="songNumber"]').value;
                    var songName = this.nextElementSibling.querySelector('input[name="songNumber"]').id;
                    var genreName = this.nextElementSibling.querySelector('input[name="genreNumber"]').id;
                    console.log('Selected Values:');
                    console.log('genreNumber:', genreNumber);
                    console.log('genre:', genreName);
                    console.log('songNumber:', songNumber);
                    console.log('song:', songName);
                    
                    updateHeader(genreName, songName);
                }
            });

            removeButton.addEventListener('click', createRemoveButtonClickHandler(accordion, panel, genreInput, songInput));
        }
    }

    // Function to create remove button click event handler
    function createRemoveButtonClickHandler(accordion, panel, genreInput, songInput) {
        return function(event) {
            event.stopPropagation();
            var genreSong = accordion.textContent.trim();
            var genreValue = genreInput.value;
            var songValue = songInput.value;
            console.log('Selected Values:');
            console.log('Genre:', genreValue);
            console.log('Song:', songValue);
            var index = Array.from(accordion.parentNode.children).indexOf(accordion) / 2;
            setList.splice(index, 1);
            localStorage.setItem('setlist', JSON.stringify(setList));
            accordion.remove();
            panel.remove();
            genreInput.remove(); // Remove the genre input field
            songInput.remove(); // Remove the song input field
        };
    }

    // Function to extract the numeric value from the string
    function getNumericValue(str) {
        var numericValue = str.match(/^\d+/);
        return numericValue ? parseInt(numericValue[0]) : 0;
    }

      function searchByBeat(button, event) {
          console.log("searchByBeat");
          event.preventDefault(); // Prevent the default button behavior
          var beat = button.getAttribute("data-beat");
          var bpm = button.getAttribute("data-bpm");
          bpm = bpm.substring(0, bpm.length-3);
          console.log(bpm);
          var mybeat = beat.substring(beat.lastIndexOf(":") + 1).trim();
          var searchUrl = "/search/query=" + encodeURIComponent(mybeat);
          localStorage.setItem("bpm", bpm);

          window.location.href = searchUrl;
      }
	  
// Function to update the search value in localStorage
function updateSearchValue(value) {
  localStorage.setItem('searchValue', value);
  localStorage.removeItem('bpm');
}

// Function to save the search value to localStorage before form submission
function saveSearch() {
  var searchInput = document.getElementById('search');
  updateSearchValue(searchInput.value);
}

