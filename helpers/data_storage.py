from datetime import datetime

import pandas as pd

from helpers.environment_variables import CHANNELS

recording_buffer = list()
COLUMN_NAMES = [str(x) for x in range(CHANNELS - 6)]
COLUMN_NAMES.extend(["IMU_W", "IMU_X", "IMU_Y", "IMU_Z", "Buffer_Usage", "Counter"])


def add_recording(data: list[int]):
    recording_buffer.append(data)


def persist_recordings():
    dataframe = pd.DataFrame(data=recording_buffer, columns=COLUMN_NAMES)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    print(dataframe.head(10))
    dataframe.to_parquet("data/" + timestamp + ".parquet")
