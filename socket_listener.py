# Source https://github.com/miladinovic/OTbioelettronica_LSL
import helpers.socket_helper as sh
import helpers.socket_variables as sv
import pandas as pd

TCP_PORT = 54320
HOSTNAME = '192.168.76.1'
CHANNEL_NUMBER = 82  # Old: 82
SAMPLE_RATE = 1
CHUNK_SIZE = 1

if __name__ == '__main__':
    dataframe = pd.DataFrame()

    print(sv.INFO_TEXT)
    client = sh.emg_client(tcp_port=TCP_PORT, hostname=HOSTNAME)  # Create TCP I/O socket
    sh.send_signal(client, sv.START_SIGNAL)  # Send configuration

    try:
        print(sv.STREAM_START_TEXT)
        print(CHANNEL_NUMBER, SAMPLE_RATE, CHUNK_SIZE, CHANNEL_NUMBER * SAMPLE_RATE * CHUNK_SIZE)

        while True:
            data = sh.receive_signal(client, CHANNEL_NUMBER * SAMPLE_RATE * CHUNK_SIZE * 2)
            data = sh.convert_data_to_ints(data, True)
            dataframe.append(data)
    except Exception as e:
        print(e, sv.ERROR_TEXT)
        dataframe.to_feather("/example")
        sh.send_signal(client, sv.STOP_SIGNAL)
        client.close()
        print(dataframe.head(10))
        dataframe.to_feather("/example")
    finally:
        print(sv.STREAM_CLOSE_TEXT)
        print(dataframe.head(10))
        sh.send_signal(client, sv.STOP_SIGNAL)
        client.close()
        print(dataframe.head(10))
        dataframe.to_feather("/example")
