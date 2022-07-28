from datetime import datetime

import pandas as pd

from helpers.environment_variables import CHANNELS

COLUMN_NAMES = [str(x) for x in range(CHANNELS - 6)]
COLUMN_NAMES.extend(["IMU_W", "IMU_X", "IMU_Y", "IMU_Z", "Buffer_Usage", "Counter"])

signal_storage = list()


def add_recording(data: list[int]):
    """
    Use this method to add new data to the memory signal store
    :param data: EMG Data to be persisted
    """
    signal_storage.append(data)


def persist_recordings():
    """
    Use this method to save the memory signal store as a compressed parquet file to the disk
    """
    dataframe = pd.DataFrame(data=signal_storage, columns=COLUMN_NAMES)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    print(dataframe.head(10))
    dataframe.to_parquet("data/" + timestamp + ".parquet")
