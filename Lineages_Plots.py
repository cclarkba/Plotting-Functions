import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

data_file_folder = '../CharlesLab'

for file in os.listdir(data_file_folder):
    if file.endswith('.xlsx'):
        print('Lodaing file {0}...'.format(file))
        data = pd.read_excel(os.path.join(data_file_folder, file))
        temp = data.columns
        date_x = np.array(data['Date Collected'])
        for i in range(1,6):
            freq_y = np.array(data['BA.{0}'.format(i)])
            freq_y[freq_y == 0] = np.nan
            mask = np.isfinite(freq_y)
            data.columns = temp
            fig, ax = plt.subplots()
            ax.scatter(date_x[mask], freq_y[mask], marker=".", edgecolors='black')
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=(6, 12, 18, 24)))
            for label in ax.get_xticklabels(which="major"):
                label.set(rotation=45, horizontalalignment="right")
            ax.grid(axis="y", color="gray", alpha=0.5)

            plt.subplots_adjust(bottom=0.25)
            plt.title('Omicron (BA.{0})'.format(i))
            plt.xlabel("Sampling Date")
            plt.ylabel("Frequency (%)")

            plt.tight_layout()

            plt.show(block=True)