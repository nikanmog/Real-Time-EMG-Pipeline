from datetime import datetime

import pandas as pd

dataframe = pd.DataFrame()


def add_recording(data: tuple):
    dataframe.append(data)


def persist_recordings():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    print(dataframe.head(10))
    dataframe.to_feather("/data/" + timestamp)
