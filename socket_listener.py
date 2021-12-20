# Source https://github.com/miladinovic/OTbioelettronica_LSL
import time
from pylsl import StreamInfo, StreamOutlet
import socket
import struct

TCPPort = 54320
Hostname = '192.168.76.1'
nCh = 82
sRate = 2000
chunkSize = 1

INFO_TEXT = """
1) the white LED is related to wireless data transfer. \n
2) the red LED highlights errors or problems. \n
*------------*-----------------------------------*----------------------*-------------------------*---------------* \n
| n. flashes | 1                                 | 2                    | 3                       | 4             | \n
*------------*-----------------------------------*----------------------*-------------------------*---------------* \n
| white      | WiFi active                       | Connected to network | Connected to TCP socket | Data transfer | \n
*------------*-----------------------------------*----------------------*-------------------------*---------------* \n
| red        | Loss of data during WiFi transfer | -                    | Low battery level       | -             | \n
*------------*-----------------------------------*----------------------*-------------------------*---------------*"
"""


def client_emg():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    ip = socket.gethostbyname(Hostname)
    address = (ip, TCPPort)
    client.connect(address)
    return client


def convert_data_to_ints(data, big_endian=True):
    int_count = len(data) // 2  # bytes long
    fmt = ">" if big_endian else "<"
    fmt += "h" * int_count
    return struct.unpack(fmt, data[:int_count * 2])


def send_default_configuration(client):  # TODO Update
    packet = bytearray()  # double([5;9;25;134]);
    packet.append(5)
    packet.append(9)
    packet.append(25)
    packet.append(134)  # CRC8
    client.send(packet)
    time.sleep(0.3)
    print(packet)


def send_test_configuration(client):
    packet = bytearray()  # double([5;15;31;241]);
    packet.append(5)
    packet.append(15)
    packet.append(31)
    packet.append(241)  # CRC8
    client.send(packet)
    time.sleep(0.3)


def stop_stream(client):
    packet = bytearray()  # double([0;63]);
    packet.append(0)
    packet.append(63)  # CRC8
    client.send(packet)
    time.sleep(0.3)


def recvall(client, n):
    data = bytearray()
    while len(data) < n:
        packet = client.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


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
    ch_labels = ['MuoviI-1', 'MuoviI-2', 'MuoviI-3', 'MuoviI-4', 'MuoviI-5', 'MuoviI-6', 'MuoviI-7', 'MuoviI-8',
                 'MuoviI-9', 'MuoviI-10', 'MuoviI-11', 'MuoviI-12', 'MuoviI-13', 'MuoviI-14', 'MuoviI-15', 'MuoviI-16',
                 'MuoviI-17', 'MuoviI-18', 'MuoviI-19', 'MuoviI-20', 'MuoviI-21', 'MuoviI-22', 'MuoviI-23', 'MuoviI-24',
                 'MuoviI-25', 'MuoviI-26', 'MuoviI-27', 'MuoviI-28', 'MuoviI-29', 'MuoviI-30', 'MuoviI-31', 'MuoviI-32',
                 'MuoviI-W', 'MuoviI-X', 'MuoviI-Y', 'MuoviI-Z', 'MuoviI-sync', 'MuoviI-counter', 'MuoviII-1',
                 'MuoviII-2', 'MuoviII-3', 'MuoviII-4', 'MuoviII-5', 'MuoviII-6', 'MuoviII-7', 'MuoviII-8', 'MuoviII-9',
                 'MuoviII-10', 'MuoviII-11', 'MuoviII-12', 'MuoviII-13', 'MuoviII-14', 'MuoviII-15', 'MuoviII-16',
                 'MuoviII-17', 'MuoviII-18', 'MuoviII-19', 'MuoviII-20', 'MuoviII-21', 'MuoviII-22', 'MuoviII-23',
                 'MuoviII-24', 'MuoviII-25', 'MuoviII-26', 'MuoviII-27', 'MuoviII-28', 'MuoviII-29', 'MuoviII-30',
                 'MuoviII-31', 'MuoviII-32', 'MuoviII-W', 'MuoviII-X', 'MuoviII-Y', 'MuoviII-Z', 'MuoviII-sync',
                 'MuoviII-counter', 'Station-aux-1', 'Station-aux-2', 'Station-aux-3', 'Station-aux-4', 'Station-sync',
                 'Station-counter']

    for c in ch_labels:
        ch = channels.append_child("channel")
        ch.append_child_value("label", c)
        ch.append_child_value("type", "EMG")

    # create LSL outlet
    bioelettronica_outlet = StreamOutlet(stream_info_bioelettronica, sRate * chunkSize)

    try:
        print("Start streaming...")
        print("Number of channels: ", nCh)
        print("Sampling rate: ", sRate)
        print("Streaming chunk size (sec): ", chunkSize)
        print("Total buffer size (words i.e. 2bytes): ", nCh * sRate * chunkSize)

        animation = " | / - \\"
        idx = 0
        print(" ", animation[idx % len(animation)], end="\n")
        while True:
            print(idx + " Loop Iteration")
            data = recvall(client, nCh * sRate * chunkSize * 2)
            data = convert_data_to_ints(data, True)
            if bioelettronica_outlet.have_consumers():
                bioelettronica_outlet.push_chunk(data)
            print(" ", animation[idx % len(animation)], end="\r")
            print(data[0], end="\r")
            idx += 1
    except Exception as e:
        print("!!! Exception: ", e,
              ", server didn't respond with any data! Try restarting syncstation and probes! Check out the LEDs!")
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
        print("Press Enter to continue ...")
        input()


if __name__ == '__main__':
    main()
