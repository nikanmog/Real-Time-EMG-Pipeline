import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication

pw = pg.plot()


def plot_force(prediction):
    """
    Use this method to update the realtime prediction plot
    :param prediction: Array with values to be plotted
    """
    if len(prediction) > 0:
        prediction = np.reshape(prediction, [5])
        pw.plot(prediction, clear=True)
        QApplication.processEvents()
        # print(prediction)
