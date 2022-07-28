import socket
import time

from crc import CrcCalculator, Crc8

import helpers.environment_variables as env


def get_emg_client(tcp_port: int, hostname: str) -> socket.socket:
    """
    Use this method to initialize the connection with the EMG device and create the TCP I/O socket
    :param tcp_port: Port number of EMG Client
    :param hostname: Hostname of EMG Client
    :return: Socket which represents the EMG Client
    """
    print(env.INFO_TEXT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    ip = socket.gethostbyname(hostname)
    address = (ip, tcp_port)
    client.connect(address)
    return client


def send_signal(client: socket.socket, signal: list[int]) -> None:
    """
    Use this method to send signals to the EMG device
    :param client: Initialized EMG client
    :param signal: Byte signal that will be transmitted to the EMG device
    """
    print(env.STREAM_TEXT)
    print(env.CHANNELS, env.SAMPLE_RATE, env.CHUNK_SIZE, env.CHANNELS * env.SAMPLE_RATE * env.CHUNK_SIZE)
    packet = bytearray(signal)
    crc_calculator = CrcCalculator(Crc8.MAXIM_DOW)
    packet.append(crc_calculator.calculate_checksum(packet))  # Add CRC-8
    client.send(packet)
    time.sleep(0.3)


def receive_signal(client: socket.socket, n: int) -> list[int]:
    """
    Use this method to get signals from the EMG device
    :param client: Initialized EMG client
    :param n: Length of the expected signal
    :return: Signal converted to an integer array
    """
    packet = client.recv(n)
    int_data = [int.from_bytes(packet[i:i + 2], byteorder='big') for i in range(0, len(packet), 2)]
    return int_data
