import csv
from flask import Flask, render_template, request, jsonify, redirect, url_for
import logging
import mido
import os
import subprocess
import time
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from mido import Message
from params import *

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Global variables to store the current tempo
current_tempo = 120
nrpn_msb = 0
nrpn_lsb = 0
tempo_msb = 0
tempo_lsb = 0

mido.set_backend('mido.backends.rtmidi')  # or 'mido.backends.portmidi'
output = mido.open_output()

toggle = 0  # Define toggle as a global variable outside the function

# app name
@app.errorhandler(404)
def not_found(e):
    genre_data = read_genre_data(f"{homedir_songs}/config.csv")
    genre_names = genre_data  # Use the genre_data dictionary directly
    genre_songs = {}  # Create an empty dictionary to store genre songs

    return render_template(
        "index.html",
        genre_data=genre_data,
        genre_names=genre_names,
        genre_songs=genre_songs,
    )


def read_genre_data(file_path):
    genre_data = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            code = row[0].strip()
            name = row[1].strip()
            if code != "FOLDER":
                genre_data[code] = name
    return genre_data


def read_song_names(file_path):
    song_names = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                song_names.append(row[1].strip())
    return song_names

## Routes

outz = mido.get_output_names()
inz = mido.get_input_names()

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        selected_input = request.form.get('input')
        selected_output = request.form.get('output')
        homedir_songs = request.form.get('homedir_songs')
        write_params(selected_input, selected_output, homedir_songs)
        return 'Params file created successfully!'
    
    return render_template('index.html', inputs=inz, outputs=outz)

def write_params(selected_input, selected_output, homedir_songs):
    params_code = f"import mido\nport_name = '{selected_input}'\noutport = '{selected_output}'\nhomedir_songs = r'{homedir_songs}'"
    with open('params.py', 'w') as file:
        file.write(params_code)




@app.route("/get_songs", methods=["POST"])
def get_songs():
    genre_folder = request.json.get("genreCode")
    genre_songs = []

    genre_config_path = f"{homedir_songs}/{genre_folder}/config.csv"
    with open(genre_config_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            genre_songs.append(row[1])

    return jsonify(genre_songs)


@app.route("/")
def index():
    global current_tempo
    genre_data = read_genre_data(f"{homedir_songs}/config.csv")
    genre_names = genre_data  # Use the genre_data dictionary directly
    genre_songs = {}  # Create an empty dictionary to store genre songs

    return render_template(
        "index.html",
        genre_data=genre_data,
        genre_names=genre_names,
        genre_songs=genre_songs,
        current_tempo=current_tempo,
    )


@app.route("/select_song", methods=["POST"])
def select_song():
    genre_name = request.form["genre"]
    genre_data = read_genre_data(f"{homedir_songs}/config.csv")
    genre_code = None
    for code, name in genre_data.items():
        if name.strip() == genre_name:
            genre_code = code
            break
    if genre_code is None:
        return "Genre code not found."
    genre_config_path = f"{homedir_songs}/{genre_code}/config.csv"
    song_names = read_song_names(genre_config_path)
    return render_template("select_song.html", genre=genre_name, song_names=song_names)


# @app.route("/results", methods=["POST"])
# def display_results():
# genre = request.form["genre"]
# song = request.form["song"]
# genre_data = read_genre_data(f"{homedir_songs}/config.csv")
# return render_template(
# "results.html", genre=genre, song=song, genre_data=genre_data
# )


@app.route("/send_to_bb", methods=["POST"])
def send_to_bb():
    global current_tempo, port_name
    # print("entering send_to_bb")
    genre = request.form["genre"]
    song = request.form["song"]

    genre_number = genre.split(".")[0].strip()
    song_number = song.split(".")[0].strip()
    genre_number = str(int(genre_number) - 1)
    song_number = str(int(song_number) - 1)

    try:
        output = subprocess.check_output(
            ["python", "set_bb.py", "0", genre_number, song_number],
            stderr=subprocess.STDOUT,
        )

        # Variables for tempo calculation
        clock_ticks = 0
        start_time = time.time()
        # current_tempo = None

        # Open the MIDI input
        with mido.open_input(port_name) as port:
            for message in port:
                if message.type == "clock":
                    clock_ticks += 1

                    # Calculate tempo every quarter note (24 MIDI clock ticks)
                    if clock_ticks % 24 == 0:
                        elapsed_time = time.time() - start_time
                        tempo = 60.0 / elapsed_time
                        rounded_tempo = int(tempo) + 1

                        # Read tempo only if it has changed
                        if rounded_tempo != current_tempo:
                            current_tempo = rounded_tempo
                            # print(f"Tempo: {current_tempo} BPM")
                            # Exit the loop after reading the tempo
                            break
                        # Reset timing variables
                        start_time = time.time()
            # return str(current_tempo)
        magic()
        return redirect(url_for("index"))
    except subprocess.CalledProcessError as e:
        # print("Error executing set_bb.py:", e.output)
        return "Error sending data to Beat Buddy."


def magic():
    global current_tempo
    genre_data = read_genre_data(f"{homedir_songs}/config.csv")
    genre_names = genre_data  # Use the genre_data dictionary directly
    genre_songs = {}  # Create an empty dictionary to store genre songs
    return render_template(
        "index.html",
        genre_data=genre_data,
        genre_names=genre_names,
        genre_songs=genre_songs,
        current_tempo=current_tempo,
    )


# @app.route("/tempo_control")
# def tempo_control():
# # print("tempo_control route")
# return render_template("tempo_control.html", current_tempo=current_tempo)


@app.route("/set_tempo", methods=["POST"])
def set_tempo():
    # print("set_tempo route")
    global current_tempo, nrpn_msb, nrpn_lsb, tempo_msb, tempo_lsb, outport

    new_tempo = int(request.form["new_tempo"])
    # print("new tempo", new_tempo)

    output = mido.open_output(outport)
    output.close()

    # Calculate the MSB and LSB values for the new tempo
    nrpn_msb = new_tempo // 128
    nrpn_lsb = new_tempo % 128
    tempo_msb = nrpn_msb
    tempo_lsb = nrpn_lsb

    # Set the NRPN MSB and LSB
    with mido.open_output(outport) as port_out:

        # Set the tempo using Tempo MSB and LSB
        port_out.send(mido.Message("control_change", control=106, value=tempo_msb))
        # logging.info(f'Sent tempo MSB: {tempo_msb}')
        port_out.send(mido.Message("control_change", control=107, value=tempo_lsb))
      # logging.info(f"Sent tempo LSB: {tempo_lsb}")

    # Update the current tempo
    current_tempo = new_tempo
    output = subprocess.check_output(
        ["python", "fx_send.py", "--tempo", str(new_tempo)],
        stderr=subprocess.STDOUT,
    )
    # print(output)

    return str(current_tempo)  # Return the updated tempo


@app.route("/adjust_tempo", methods=["POST"])
def adjust_tempo():
    global current_tempo, nrpn_msb, nrpn_lsb, tempo_msb, tempo_lsb, outport
    print("adjust_tempo route. Current tempo is ", current_tempo)
    adjustment = int(request.form["adjustment"])

    output = mido.open_output(outport)
    # debounce
    time.sleep(0.250)
    output.close()

    try:
        # Apply the adjustment to the current tempo
        new_tempo = current_tempo + adjustment
        print("new tempo", new_tempo)
        # Ensure the new tempo is within the valid range
        new_tempo = max(40, min(new_tempo, 300))

        # Calculate the MSB and LSB values for the new tempo
        nrpn_msb = new_tempo // 128
        nrpn_lsb = new_tempo % 128
        tempo_msb = nrpn_msb
        tempo_lsb = nrpn_lsb

        # Set the NRPN MSB and LSB
        with mido.open_output(outport) as port_out:
            # Set the tempo using Tempo MSB and LSB
            port_out.send(mido.Message("control_change", control=106, value=tempo_msb))
            logging.info(f"Sent tempo MSB: {tempo_msb}")
            port_out.send(mido.Message("control_change", control=107, value=tempo_lsb))
            logging.info(f"Sent tempo LSB: {tempo_lsb}")

        # Update the current tempo
        current_tempo = new_tempo
        output = subprocess.check_output(
            ["python", "fx_send.py", "--tempo", str(new_tempo)],
            stderr=subprocess.STDOUT,
        )
        # print(output)
        time.sleep(0.500)
        return str(current_tempo)  # Return the updated tempo

    except Exception as e:
        logging.error(f"Error occurred while adjusting tempo: {str(e)}")
        return f"Error occurred: {str(e)}"


def search_songs(query):
    results = []

    with open(os.path.join(homedir_songs, "config.csv"), "r") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            genre_code = row[0]
            genre_name = row[1]
            genre_folder_path = os.path.join(homedir_songs, genre_code)

            if os.path.exists(genre_folder_path):
                config_file_path = os.path.join(genre_folder_path, "config.csv")
                with open(config_file_path, "r") as config_file:
                    reader2 = list(csv.reader(config_file))
                    for row2 in reader2:
                        if len(row2) > 1:  # Skip empty rows
                            song_code = row2[0]
                            song_name = row2[1]
                            song_file = os.path.join(
                                genre_folder_path, song_code + ".wav"
                            )

                            if query.lower() in song_name.lower():
                                results.append(
                                    {
                                        "genre_code": genre_code,
                                        "genre_name": genre_name,
                                        "song_file": song_file,
                                        "song_name": song_name,
                                    }
                                )

    return results


@app.route("/search", methods=["GET", "POST"])
def search():
    # print("we're in serach")
    if request.method == "POST":
        query = request.form["query"]
        search_results = search_songs(query)
        # print("search results :" + str(search_results))
        if search_results:
            return render_template(
                "search_results.html", query=query, results=search_results
            )
        else:
            return redirect("/bbmatch/query=" + query)

    return render_template("search.html")


@app.route("/search/query=<query>", methods=["GET", "POST"])
def bbsearch(query):
    search_results = search_songs(query)
    # print("search query results :" + str(search_results))
    return render_template("search_results.html", query=query, results=search_results)


@app.route("/bbmatch/query=<query>", methods=["GET", "POST"])
def bbmatch_results(query):
    if request.method == "GET":
        # print("bbmatch query: " + query)
        search_value = query
        if search_value is None or search_value.strip() == "":
            # print("escaped at if")
            return render_template("search.html")

        encoded_search_value = quote(search_value)
        # print("encoded: " + encoded_search_value)

        url = f"https://songmatcher.singularsound.com/?q={encoded_search_value}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        results_table = soup.find("table")
        table_rows = results_table.find_all("tr")[1:]  # Exclude the header row
        results = []

        for row in table_rows:
            columns = row.find_all("td")
            song_name = columns[0].text.strip()
            genre_name = columns[1].text.strip()
            beat = columns[2].text.strip()
            bpm = columns[3].text.strip()
            genre = columns[5].text.strip()

            result = {
                "song_name": song_name,
                "genre_name": genre_name,
                "beat": beat,
                "bpm": bpm + "bpm",
                "genre": genre,
            }
            results.append(result)
        # print("moving to search results 2")
        return render_template("search_results2.html", query=query, results=results)

    return redirect("/search/query=" + query)


@app.route("/submit", methods=["POST"])
def submit():
    global current_tempo, outport, port_name
    # print("submit route")

    output = mido.open_output(outport)
    output.close()
    time.sleep(0.500)
    try:
        genre_number = request.form.get("genre_number")
        song_number = request.form.get("song_number")
        bpm = request.form.get("bpm")
        # print("bpm in send to bb: " + bpm)

        if not genre_number or not song_number:
            raise ValueError("Genre number or song number is missing.")

        genre_number = request.form.get("genre_number")
        song_number = request.form.get("song_number")
        genre_number = str(int(genre_number) - 1)
        song_number = str(int(song_number) - 1)
        # print(f"genre_number: {genre_number}, song_number: {song_number}")

        output = subprocess.check_output(
            ["python", "set_bb.py", "0", genre_number, song_number],
            stderr=subprocess.STDOUT,
        )
        if bpm is not None:
            # Variables for tempo calculation
            clock_ticks = 0
            start_time = time.time()

            current_tempo = None if bpm == "null" else bpm
            # print("current tempo is", current_tempo)
            # Open the MIDI input
            if current_tempo is not None:
                # print("tempo has a value of", current_tempo)
                time.sleep(0.500)
                with mido.open_output(outport) as port_out:
                    # Calculate the MSB and LSB values for the new tempo
                    nrpn_msb = int(current_tempo) // 128
                    nrpn_lsb = int(current_tempo) % 128
                    tempo_msb = nrpn_msb
                    tempo_lsb = nrpn_lsb
                    # print("msb", tempo_msb, "lsb", tempo_lsb)
                    port_out.send(
                        mido.Message("control_change", control=106, value=tempo_msb)
                    )
                    port_out.send(
                        mido.Message("control_change", control=107, value=tempo_lsb)
                    )

            # Open the MIDI input
            else:
                with mido.open_input(port_name) as port:
                    for message in port:
                        if message.type == "clock":
                            clock_ticks += 1

                            # Calculate tempo every quarter note (24 MIDI clock ticks)
                            if clock_ticks % 24 == 0:
                                elapsed_time = time.time() - start_time
                                tempo = 60.0 / elapsed_time
                                rounded_tempo = int(tempo)

                                # Read tempo only if it has changed
                                if rounded_tempo != current_tempo:
                                    current_tempo = rounded_tempo
                                    # print(f"Tempo: {current_tempo} BPM")
                                    # Exit the loop after reading the tempo
                                    break
                                # Reset timing variables
                                start_time = time.time()
                    # return str(current_tempo)
                magic()
        return redirect(url_for("index"))
    except Exception as e:
        # print("Error:", str(e))
        return "Error submitting the song."


toggle = 0


@app.route("/send_midi", methods=["POST"])
def send_midi():
    global toggle, outport  # Declare toggle as a global variable to modify it
    command = request.form["command"]
    output = mido.open_output(outport)

    channel = 0  # Assuming you want to send the message on channel 1
    cc_value = 1

    if command == "stop":
        cc_number = 115
    elif command == "start":
        cc_number = 114
    elif command == "pause":
        cc_number = 111
        cc_value = 2
    elif command == "fill":
        cc_number = 112
    elif command == "half":
        cc_number = 82
        if toggle == 0:
            toggle = 1
            cc_value = 1
        elif toggle == 1:
            cc_value = 0
            toggle = 0
    elif command == "double":
        cc_number = 83
        if toggle == 0:
            toggle = 2
            cc_value = 1
        elif toggle == 2:
            cc_value = 0
            toggle = 0
    elif command == "previous":
        cc_number = 113
        cc_value = 126
        message = Message(
            "control_change", control=cc_number, value=cc_value, channel=channel
        )
        output.send(message)
        time.sleep(0.500)
        cc_value = 0
    elif command == "next":
        cc_number = 113
        cc_value = 127
        message = Message(
            "control_change", control=cc_number, value=cc_value, channel=channel
        )
        output.send(message)
        time.sleep(0.500)
        cc_value = 0

    message = Message(
        "control_change", control=cc_number, value=cc_value, channel=channel
    )
    # print(message)
    output.send(message)

    return "MIDI command sent successfully."
    # output.close()


# # Close the MIDI output port when the app is shut down
# @app.teardown_appcontext
# def close_midi_port(exception=None):
# output.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
