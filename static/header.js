  function sendToBeatBuddy() {
  // Retrieve the values from localStorage
  var genre = document.getElementById("selectedGenreHeader").textContent;
  var song = document.getElementById("selectedSongHeader").textContent;

  var form = document.createElement("form");
  form.setAttribute("method", "POST");
  form.setAttribute("action", "/send_to_bb");

  var genreInput = document.createElement("input");
  genreInput.setAttribute("type", "hidden");
  genreInput.setAttribute("name", "genre");
  genreInput.setAttribute("value", genre);

  var songInput = document.createElement("input");
  songInput.setAttribute("type", "hidden");
  songInput.setAttribute("name", "song");
  songInput.setAttribute("value", song);

  form.appendChild(genreInput);
  form.appendChild(songInput);

  document.body.appendChild(form);

  // Display the success message
  var successMessage = document.getElementById("successMessage");
  successMessage.style.display = "block";
  // Store the values in localStorage
	localStorage.setItem("currentGenre", genreInput.value);
	localStorage.setItem("currentSong", songInput.value);

  // Move value from "setlist" to "past"
  var setlist = JSON.parse(localStorage.getItem("setlist"));
  var past = JSON.parse(localStorage.getItem("past")) || [];
  
  // Find the index of the selected value in the "setlist" array
  var index = setlist.findIndex(function(item) {
    return item.genre.trim() === genre.trim() && item.song.trim() === song.trim();
  });
  
  if (index !== -1) {
    // Remove the selected value from "setlist"
    var removedValue = setlist.splice(index, 1)[0];
    // Add the removed value to "past"
    past.push(removedValue);
    
    // Update the modified arrays in localStorage
    localStorage.setItem("setlist", JSON.stringify(setlist));
    localStorage.setItem("past", JSON.stringify(past));
  }

  // Submit the form
  form.submit();
}

    function delay(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }

    function updateSetlist() {
        // Get the selected genre and song
        var selectedGenre = document.getElementById("selectedGenreHeader").textContent;
        var selectedSong = document.getElementById("selectedSongHeader").textContent;
        console.log("Selected genre:", selectedGenre);
        console.log("Selected song:", selectedSong);

        // Create an object for the new song
        var songObject = {
            genre: selectedGenre,
            song: selectedSong
        };

        // Retrieve the existing setlist from local storage or create an empty array
        var setlist = JSON.parse(localStorage.getItem("setlist")) || [];

        // Add the new song to the setlist
        setlist.push(songObject);

        // Store the updated setlist in local storage
        localStorage.setItem("setlist", JSON.stringify(setlist));

        var setListAdded = document.getElementById("setListAdded");
        setListAdded.style.display = "block";
        delay(1000);
        console.log("waited one second");
        window.location.href = "/";
            // Update the setlist display

        //document.addEventListener("DOMContentLoaded", function() {
        //  displaySetlist();
        //    });
    }