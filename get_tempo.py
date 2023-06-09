import mido
import time

inport_name = 'AudioBox iTwo MIDI In'
mido.set_backend('mido.backends.pygame')


def look():
    print("entering get_tempo")
    # wipe out tempo
    current_tempo = None
    clock_ticks = 0
    # Setup tempo timer
    start_time = time.time()

    try:
        # Open the MIDI input
        with mido.open_input(inport_name) as port:
            for message in port:
                if message.type == 'clock':

                    clock_ticks += 1
                    # Calculate tempo every quarter note (24 MIDI clock ticks)
                    if clock_ticks % 24 == 0:
                        elapsed_time = time.time() - start_time
                        tempo = 60.0 / elapsed_time
                        rounded_tempo = int(tempo)

                        # Read tempo only if it has changed
                        if rounded_tempo != current_tempo:
                            current_tempo = rounded_tempo
                            print(f"Tempo: {current_tempo} BPM")
                            # Exit the loop after reading the tempo
                            break
            # Print the current tempo before exiting the `with` statement
            print("hey we got a current tempo of", current_tempo)
    finally:
        # Do not close the MIDI port here    
        pass

    return current_tempo
