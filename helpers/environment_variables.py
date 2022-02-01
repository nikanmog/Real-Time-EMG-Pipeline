TCP_PORT = 54320
HOSTNAME = '192.168.76.1'
CHANNELS = 76
SAMPLE_RATE = 1
CHUNK_SIZE = 1

# Read more in the docs "SyncStation - communication protocol.pdf"
START_BYTE = int('00001011', 2)  # Defines which channels are active, more info in docs
MUOVI_PLUS_5_CONTROL_BYTE = int('01001001', 2)
MUOVI_PLUS_6_CONTROL_BYTE = int('01011001', 2)
START_SIGNAL = [START_BYTE, 0, 0, 0, 0, MUOVI_PLUS_5_CONTROL_BYTE]
STOP_SIGNAL = [0]

INFO_TEXT = """
1) the white LED is related to wireless data transfer.
2) the red LED highlights errors or problems.
*------------*-----------------------------------*----------------------*-------------------------*---------------*
| n. flashes | 1                                 | 2                    | 3                       | 4             |
*------------*-----------------------------------*----------------------*-------------------------*---------------*
| white      | WiFi active                       | Connected to network | Connected to TCP socket | Data transfer |
*------------*-----------------------------------*----------------------*-------------------------*---------------*
| red        | Loss of data during WiFi transfer | -                    | Low battery level       | -             |
*------------*-----------------------------------*----------------------*-------------------------*---------------*"
"""

ERROR_TEXT = """
Server didn't respond with any data! Try restarting sync station and probes! Check out the LEDs!
- 1 & 2 green led on sync station must be ON
- no red blinking on probes 1 and 2 should be present, present single blink means DATA_LOSS, triple blinking LOW_BATTERY
"""
STREAM_START_TEXT = """
Start streaming...
Number of channels, Sampling rate, Streaming chunk size (sec), Total buffer size (words i.e. 2bytes):
"""
STREAM_CLOSE_TEXT = """
Stopping stream...
Closing socket...
"""
