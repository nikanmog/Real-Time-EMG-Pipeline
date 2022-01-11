import struct
import time


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
