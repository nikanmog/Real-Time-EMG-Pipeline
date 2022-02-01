import socket
import time

from crc import CrcCalculator, Crc8


def emg_client(tcp_port: int, hostname: str) -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    ip = socket.gethostbyname(hostname)
    address = (ip, tcp_port)
    client.connect(address)
    return client


def send_signal(client: socket.socket, signal: list[int]) -> None:
    packet = bytearray(signal)
    crc_calculator = CrcCalculator(Crc8.MAXIM_DOW)
    packet.append(crc_calculator.calculate_checksum(packet))  # Add CRC-8
    client.send(packet)
    time.sleep(0.3)


def receive_signal(client: socket.socket, n: int) -> list[int]:
    packet = client.recv(n)
    int_data = [int.from_bytes(packet[i:i + 2], byteorder='big') for i in range(0, len(packet), 2)]
    return int_data
