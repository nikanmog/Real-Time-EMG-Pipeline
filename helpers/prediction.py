from collections import deque

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

resampling_buffer = list()
signal_memory = deque()
model = load_model("model")


def get_buffer(signal_data: list):
    # TODO Clean input
    signal_memory.append(signal_data)
    if len(signal_memory) < 32:
        return None
    if len(signal_memory) > 32:
        signal_memory.popleft()
    return_buffer = np.array(signal_memory)
    return_buffer = np.reshape(return_buffer, [1, 32, 128])
    return return_buffer


def int_to_volt(data: list):
    return [convert_to_emg(x) for x in data]


def convert_to_emg(signal):
    if signal == 0:
        conv = 0.0
    else:
        # if input < (2 ** 15) - 1, the number is positive
        if signal < 32767:
            conv1 = signal
        else:
            conv1 = signal - 65536
        conv = float(float(conv1) / 108134.4 *100000)  # 108134.4 = (2 ** 15) * 3.3
    return conv


def clean_input(data: list):
    sensor_1 = data[0:64]
    sensor_2 = data[70:134]
    sensor_1.extend(sensor_2)
    return sensor_1


def get_prediction(data: list):

    data = clean_input(data)
    print(data)
    data = int_to_volt(data)

    resampling_buffer.append(data)
    if len(resampling_buffer) >= 8:
        buffer_average = pd.DataFrame(resampling_buffer)
        buffer_average = buffer_average[buffer_average.columns].mean()
        sig_memory = get_buffer(buffer_average)
        if sig_memory is not None:
            return model.predict(sig_memory, verbose=False)
        resampling_buffer.clear()
    return [0.0] * 5
