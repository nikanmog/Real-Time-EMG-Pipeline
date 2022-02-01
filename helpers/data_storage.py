from datetime import datetime

import pandas as pd

recording_buffer = list()


def add_recording(data: tuple):
    recording_buffer.append(data)


def persist_recordings():
    dataframe = pd.DataFrame(data=recording_buffer, columns=[str(x) for x in range(82)])
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    print(dataframe.head(10))
    dataframe.to_feather("data/" + timestamp)
