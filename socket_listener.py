# Source https://github.com/miladinovic/OTbioelettronica_LSL
import socket
import keyboard
import logging
from pylsl import StreamInfo, StreamOutlet
from helpers.socket_helper import convert_data_to_ints, recvall, stop_stream, send_default_configuration
from helpers.socket_variables import ch_labels, INFO_TEXT

TCPPort = 54320
Hostname = '192.168.76.1'
nCh = 82
sRate = 2000
chunkSize = 1

log = logging.getLogger("data-log")


def client_emg():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    ip = socket.gethostbyname(Hostname)
    address = (ip, TCPPort)
    client.connect(address)
    return client


def main():
    print(INFO_TEXT)

    # Create TCP I/O socket
    client = client_emg()

    # Send configuration
    send_default_configuration(client)

    print("Start LSL")
    # Create LSL stream info
    stream_info_bioelettronica = StreamInfo('Bioelettronica_EMG', 'EEG', nCh, 2000, 'float32', 'bioet_muovi_ZRS_EMG')

    # append meta-data
    stream_info_bioelettronica.desc().append_child_value("manufacturer", "Bioelettronica")
    channels = stream_info_bioelettronica.desc().append_child("channels")

    for c in ch_labels:
        ch = channels.append_child("channel")
        ch.append_child_value("label", c)
        ch.append_child_value("type", "EMG")

    # create LSL outlet
    bioelettronica_outlet = StreamOutlet(stream_info_bioelettronica, sRate * chunkSize)

    try:
        print("Start streaming...")
        print("Press q to quit")
        print("Number of channels: ", nCh)
        print("Sampling rate: ", sRate)
        print("Streaming chunk size (sec): ", chunkSize)
        print("Total buffer size (words i.e. 2bytes): ", nCh * sRate * chunkSize)

        animation = " | / - \\"
        idx = 0
        print(" ", animation[idx % len(animation)], end="\n")
        while True:
            if keyboard.is_pressed("q"):
                print("q pressed, ending loop")
                break
            data = recvall(client, nCh * sRate * chunkSize * 2)
            data = convert_data_to_ints(data, True)
            if bioelettronica_outlet.have_consumers():
                bioelettronica_outlet.push_chunk(data)
            log.info(data)
            print(data)

            print(" ", animation[idx % len(animation)], end="\r")
            print(data[0], end="\r")
            idx += 1
        stop_stream(client)
        client.close()
    except Exception as e:
        print(e)
        print("Server didn't respond with any data! Try restarting syncstation and probes! Check out the LEDs!")
        print("- 1 & 2 green led on syncstation must be ON")
        print(
            "- no red blinking on probes 1 and 2 should be present, if present single blink means DATA_LOSS, "
            "triple blinking LOW_BATTERY")
    finally:
        print("Stopping stream...")
        stop_stream(client)
        print("Closing socket...")
        client.close()
        print("Channels labels: ")
        print('["', '", "'.join(str(item) for item in ch_labels), '"]')


if __name__ == '__main__':
    main()
