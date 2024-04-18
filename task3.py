import csv
import matplotlib.pyplot as plt
import numpy as np

class Business:
    __T = 365
    __parsed = []
    __t_list = []
    __filename = 'AMZN_210404_240404.csv'

    __transformed = None
    __complex_transformed = None
    __filtered = None

    def __init__(self):
        pass

    def __read_file(self):
        with open(self.__filename) as reader:
            file_reader = list(csv.reader(reader, delimiter=","))
            for row in file_reader[1:]:
                self.__parsed.append(float(row[5]))
                self.__t_list.append(row[2])

    def __calculate_filtered(self):
        self.__transformed = np.fft.fftfreq(len(self.__t_list), 1)
        self.__complex_transformed = 1j * self.__transformed
        self.__filtered = np.fft.ifft(1 / (self.__T * self.__complex_transformed + 1) * np.fft.fft(self.__parsed))

    def __draw(self):
        plt.figure(figsize=(8, 4))
        plt.plot(self.__t_list, self.__parsed,
                 label='Исходный')
        plt.plot(self.__t_list[2:], self.__filtered[2:].real,
                 label='Фильтрованный', color='darkblue')
        plt.xticks(range(0, len(self.__t_list), 40), self.__t_list[::40], rotation=60)
        plt.legend()
        plt.show()

    def run(self):
        self.__read_file()
        self.__calculate_filtered()
        self.__draw()


if __name__ == "__main__":
    ex = Business()
    ex.run()
