import socket
import struct
import time

from crc import CrcCalculator, Crc8


def emg_client(tcp_port: int, hostname: str) -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    ip = socket.gethostbyname(hostname)
    address = (ip, tcp_port)
    client.connect(address)
    return client


def send_signal(client: socket.socket, signal: list) -> None:
    packet = bytearray(signal)
    crc_calculator = CrcCalculator(Crc8.MAXIM_DOW)
    packet.append(crc_calculator.calculate_checksum(packet))  # Add CRC-8
    client.send(packet)
    time.sleep(0.3)


def receive_signal(client: socket.socket, n: int) -> bytearray:
    data = bytearray()
    while len(data) < n:
        packet = client.recv(n - len(data))
        if not packet:
            return bytearray()
        data.extend(packet)
    return data


def convert_data_to_ints(data: bytearray, big_endian=True) -> tuple:
    int_count = len(data) // 2  # bytes long
    fmt = ">" if big_endian else "<"
    fmt += "h" * int_count
    return struct.unpack(fmt, data[:int_count * 2])
