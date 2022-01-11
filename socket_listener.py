# Source https://github.com/miladinovic/OTbioelettronica_LSL
import keyboard
import logging
from helpers.socket_helper import convert_data_to_ints, recvall, stop_stream, send_default_configuration, emg_client
from helpers.socket_variables import INFO_TEXT, ERROR_TEXT, STREAM_CLOSE_TEXT, STREAM_START_TEXT

TCP_PORT = 54320
HOSTNAME = '192.168.76.1'
CHANNEL_NUMBER = 82
SAMPLE_RATE = 2000
CHUNK_SIZE = 1

log = logging.getLogger("data-log")


if __name__ == '__main__':
    print(INFO_TEXT)
    client = emg_client(tcp_port=TCP_PORT, hostname=HOSTNAME)  # Create TCP I/O socket
    send_default_configuration(client)  # Send configuration

    try:
        print(STREAM_START_TEXT)
        print(CHANNEL_NUMBER, SAMPLE_RATE, CHUNK_SIZE, CHANNEL_NUMBER * SAMPLE_RATE * CHUNK_SIZE)

        while True:
            if keyboard.is_pressed("q"):
                print("q pressed, ending loop")
                break
            data = recvall(client, CHANNEL_NUMBER * SAMPLE_RATE * CHUNK_SIZE * 2)
            data = convert_data_to_ints(data, True)
            log.info(data)
            print(data)

            print(data[0], end="\r")
        stop_stream(client)
        client.close()
    except Exception as e:
        print(e, ERROR_TEXT)
    finally:
        print(STREAM_CLOSE_TEXT)
        stop_stream(client)
        client.close()
