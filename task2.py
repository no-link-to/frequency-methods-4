import matplotlib.pyplot as plt
import numpy as np

class LinearFilters:
    __a = None
    __b = None
    __c = None
    __d = None
    __t1 = -6
    __t2 = 6
    __T = 0.9
    __T1 = 0.03
    __T2 = 5
    __T3 = 0.1

    __g = None
    __t_list = None
    __func_u = None
    __transformed_func_u = None
    __transformed = None
    __complex_transformed = None
    __first_filter = None
    __special_filter = None
    __signal_first_filter = None
    __signal_special_filter = None
    __type = 1

    def __init__(self, filter_type, a, b, c, d):
        self.__type = filter_type
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d

    def __calculate_t(self):
        self.__t_list = np.linspace(-18, 18, 1000)

    def __calculate_g(self):
        self.__g = [self.__a if self.__t1 <= self.__t_list[i] <= self.__t2 else 0
                    for i in range(len(self.__t_list))]

    def __calculate_func_u(self):
        self.__func_u = (self.__g + self.__b * (np.random.rand(len(self.__t_list)) - 0.5) +
                         self.__c * np.sin(self.__d * self.__t_list))

    def __calculate_transformed(self):
        self.__transformed = np.fft.fftfreq(len(self.__t_list), self.__t_list[1] - self.__t_list[0])
        self.__complex_transformed = 1j * self.__transformed

    def __calculate_first_filter(self):
        self.__first_filter = 1 / (self.__T * self.__complex_transformed + 1)

    def __calculate_special_filter(self): \
        self.__special_filter = ((self.__T1 ** 2 * self.__complex_transformed ** 2 +
                                  2 * self.__T1 * self.__complex_transformed + 1) /
                                 (self.__T2 * self.__T3 * self.__complex_transformed ** 2 +
                                  (self.__T2 + self.__T3) * self.__complex_transformed + 1))\

    def __calculate_filtered_signal(self):
        self.__signal_first_filter = np.fft.ifft(self.__first_filter * np.fft.fft(self.__func_u))
        self.__signal_special_filter = np.fft.ifft(self.__special_filter * np.fft.fft(self.__func_u))

    def __calculate_filtered_u(self):
        self.__transformed_func_u = np.fft.fftshift(np.fft.fft(self.__func_u))
        self.__transformed_func_u_filtered = np.fft.fftshift((self.__first_filter if self.__type == 1
                                                             else self.__special_filter) * np.fft.fft(self.__func_u))

    def __calculate_achx(self):
        self.__achx_first = 1 / np.sqrt(1 + self.__T ** 2 * self.__transformed ** 2)
        self.__achx_special = np.abs(self.__special_filter)

    def __draw_special_filtered(self):
        plt.figure(figsize=(8, 4))
        func = self.__signal_first_filter if self.__type == 1 else self.__signal_special_filter
        plt.plot(self.__t_list, self.__func_u,
                 label='Исходный', color='yellow')
        plt.plot(self.__t_list, func.real,
                 label='Фильтрованный', color='darkblue')
        plt.legend()
        plt.show()

    def __draw_filtered(self):
        plt.figure(figsize=(8, 4))
        plt.plot(self.__t_list, abs(self.__transformed_func_u),
                 label='Исходный', color='yellow')
        plt.plot(self.__t_list, abs(self.__transformed_func_u_filtered),
                 label='Фильтрованный', color='darkblue')
        plt.legend()
        plt.show()

    def __draw_achx(self):
        plt.figure(figsize=(8, 4))
        func = self.__achx_first if self.__type == 1 else self.__achx_special
        plt.plot(self.__transformed[self.__transformed > 0],
                 func[self.__transformed > 0],
                 color='darkblue')
        plt.show()

    def run(self):
        # Calculate
        self.__calculate_t()
        self.__calculate_g()
        self.__calculate_func_u()
        self.__calculate_transformed()
        self.__calculate_first_filter()
        self.__calculate_special_filter()
        self.__calculate_filtered_signal()
        self.__calculate_filtered_u()
        self.__calculate_achx()

        # Draw
        self.__draw_special_filtered()
        self.__draw_filtered()
        self.__draw_achx()


if __name__ == "__main__":
    ex = LinearFilters(1, 15, 0.9, 0, 9)
    ex.run()
