"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
import sys

from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="192.168.1.187",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=10024,
      help="The port the OSC server is listening on")
  parser.add_argument("--tempo", type=int, default=120,
      help="Tempo should be a value from 40 to 300")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port, args.tempo)

  tempo = args.tempo

  delayVal = round(60000 / tempo )
  print(str(delayVal) + " sent to mr18")

  for x in range(1):
    client.send_message("/fx/3/par/01", delayVal )
    time.sleep(1)