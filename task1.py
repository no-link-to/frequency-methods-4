import matplotlib.pyplot as plt
import numpy as np


class Spectral:
    __a = 0.001
    __dt = 0.1

    __func = None
    __func_u = None
    __t_list = None

    __func_u_transformed = None
    __transformed = None
    __func_u_transformed_der = None
    __spectral_der = None


    def __init__(self):
        pass

    def __calculate_t(self):
        self.__t_list = np.linspace(-100, 100, 2000)

    def __calculate_func(self):
        self.__func = [np.sin(self.__t_list[i]) for i in range(len(self.__t_list))]

    def __calculate_u_func(self):
        self.__func_u = self.__func + self.__a * (np.random.rand(len(self.__t_list)) - 0.5)

    def __calculate_spectral_der(self):
        self.__func_u_transformed = np.fft.fft(self.__func_u)
        self.__transformed = np.fft.fftfreq(len(self.__t_list), self.__dt)
        self.__func_u_transformed_der = 2 * np.pi * 1j * self.__transformed * self.__func_u_transformed
        self.__spectral_der = np.fft.ifft(self.__func_u_transformed_der)

    def __calculate_num_der(self):
        self.__num_der = [(self.__func_u[i] - self.__func_u[i - 1]) / (self.__t_list[i] - self.__t_list[i - 1])
                          for i in range(1, len(self.__t_list))]
        self.__num_der.append(self.__num_der[len(self.__num_der) - 1])

    def __draw_re(self):
        plt.figure(figsize=(8, 4))
        plt.plot(
            self.__transformed[self.__transformed > 0],
            self.__func_u_transformed_der.real[self.__transformed > 0],
            label='Вещественная',
            color='darkblue'
        )
        plt.plot(
            self.__transformed[self.__transformed < 0],
            self.__func_u_transformed_der.real[self.__transformed < 0],
            color='darkblue'
        )
        plt.xlim([-1.5, 1.5])
        plt.legend()
        plt.show()

    def __draw_im(self):
        plt.figure(figsize=(8, 4))
        plt.plot(
            self.__transformed[self.__transformed < 0],
            self.__func_u_transformed.imag[self.__transformed < 0],
            label='Мнимая',
            color='darkblue'
        )
        plt.plot(
            self.__transformed[self.__transformed > 0],
            self.__func_u_transformed.imag[self.__transformed > 0],
            color='darkblue'
        )
        plt.xlim([-1, 1])
        plt.legend()
        plt.show()

    def __draw_num_true(self):
        plt.figure(figsize=(8, 4))
        plt.plot(self.__t_list, self.__num_der,
                 label='Численная', color='darkblue')
        plt.plot(self.__t_list, np.cos(self.__t_list),
                 label='Истинная', linestyle='dotted', color='yellow')
        plt.legend()
        plt.xlim([-90, 90])
        plt.ylim([-1.5, 1.5])
        plt.show()

    def __draw_spectral_true(self):
        plt.figure(figsize=(8, 4))
        plt.plot(self.__t_list, self.__spectral_der.real,
                 label='Спектральная', color='darkblue')
        plt.plot(self.__t_list, np.cos(self.__t_list),
                 label='Истинная', linestyle='dotted', color='yellow')
        plt.legend()
        plt.xlim([-90, 90])
        plt.ylim([-1.5, 1.5])
        plt.show()

    def run(self):
        # Calculate
        self.__calculate_t()
        self.__calculate_func()
        self.__calculate_u_func()
        self.__calculate_num_der()
        self.__calculate_spectral_der()

        # Draw
        self.__draw_im()
        self.__draw_re()
        self.__draw_spectral_true()
        self.__draw_num_true()


if __name__ == "__main__":
    ex = Spectral()
    ex.run()
