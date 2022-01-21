# Source https://github.com/miladinovic/OTbioelettronica_LSL
import logging
import helpers.socket_helper as sh
import helpers.socket_variables as sv

TCP_PORT = 54320
HOSTNAME = '192.168.76.1'
CHANNEL_NUMBER = 82  # Old: 82
SAMPLE_RATE = 1
CHUNK_SIZE = 1

log = logging.getLogger("data-log")


if __name__ == '__main__':
    print(sv.INFO_TEXT)
    client = sh.emg_client(tcp_port=TCP_PORT, hostname=HOSTNAME)  # Create TCP I/O socket
    sh.send_default_configuration(client)  # Send configuration

    try:
        print(sv.STREAM_START_TEXT)
        print(CHANNEL_NUMBER, SAMPLE_RATE, CHUNK_SIZE, CHANNEL_NUMBER * SAMPLE_RATE * CHUNK_SIZE)

        while True:
            data = sh.recvall(client, CHANNEL_NUMBER * SAMPLE_RATE * CHUNK_SIZE * 2)
            data = sh.convert_data_to_ints(data, True)
            log.info(data)
            print(data)
        sh.stop_stream(client)
        client.close()
    except Exception as e:
        print(e, sv.ERROR_TEXT)
    finally:
        print(sv.STREAM_CLOSE_TEXT)
        sh.stop_stream(client)
        client.close()
