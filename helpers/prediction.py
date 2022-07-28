from collections import deque

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

resampling_buffer = list()
signal_memory = deque()
model = load_model("model")


def get_buffer(signal_data):
    # TODO Clean input
    signal_memory.append(signal_data)
    if len(signal_memory) < 32:
        return None
    if len(signal_memory) > 32:
        signal_memory.popleft()
    return_buffer = np.array(signal_memory)
    return_buffer = np.reshape(return_buffer, [1, 32, 128])
    return return_buffer


def get_prediction(data):
    resampling_buffer.append(data)
    if len(resampling_buffer) >= 8:
        buffer_average = pd.DataFrame(resampling_buffer)
        buffer_average = buffer_average[buffer_average.columns].mean()
        sig_memory = get_buffer(buffer_average)
        if sig_memory is not None:
            return model.predict(sig_memory, verbose=False)
        resampling_buffer.clear()
    return [0.0] * 5
