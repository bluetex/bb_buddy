import mido
import sys
import time
from params import *
# Open a MIDI output port
output = mido.open_output(outport)

# Check if the desired CC-0, CC-32, and program change values are provided as command line arguments
if len(sys.argv) < 4:
    print("Usage: python set_bb.py <CC-0 value> <CC-32 value> <program change value>")
    sys.exit(1)

# Extract the desired CC-0, CC-32, and program change values from command line arguments
desired_cc0_value = max(0, min(127, int(sys.argv[1])))
desired_cc32_value = max(0, min(127, int(sys.argv[2])))
desired_program_change_value = max(0, min(127, int(sys.argv[3])))

# Send a CC-0 message to change the bank LSB
cc0_message = mido.Message('control_change', control=0, value=desired_cc0_value)
output.send(cc0_message)
time.sleep(0.1)  # Add a small delay

# Send a CC-32 message to change the bank MSB
cc32_message = mido.Message('control_change', control=32, value=desired_cc32_value)
output.send(cc32_message)
time.sleep(0.1)  # Add a small delay

# Send a Program Change message to change the program
program_change_message = mido.Message('program_change', program=desired_program_change_value)
output.send(program_change_message)

# Close the MIDI output port
output.close()
