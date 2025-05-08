import numpy as np
import pyrnnoise
import matplotlib.pyplot as plt

# Инициализация шумоподавления
try:
    denoiser = pyrnnoise.RNNoise(16000)  # Используем частоту 16000
    print("Шумоподавление успешно инициализировано.")
except Exception as e:
    print(f"Ошибка при инициализации RNNoise: {e}")
    exit(1)

# Генерация простого синусоидального сигнала
sample_rate = 44100
freq = 1000  # Частота синусоиды (Гц)
duration = 1  # Длительность (сек)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * freq * t)

# Преобразуем сигнал в нужный формат
signal = signal.astype(np.float32)  # RNNoise ожидает float32

# Попробуем обработать сигнал
processed_signal = denoiser.process_frame(signal)

# Печатаем результат
if processed_signal is None:
    print("Шумоподавление вернуло None для синусоиды.")
else:
    print("Шумоподавление успешно обработало синусоиду.")
    # Визуализируем исходный и обработанный сигнал
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title("Исходный сигнал")
    plt.plot(t[:1000], signal[:1000])  # Рисуем первые 1000 сэмплов

    plt.subplot(2, 1, 2)
    plt.title("Обработанный сигнал")
    plt.plot(t[:1000], processed_signal[:1000])  # Рисуем первые 1000 сэмплов

    plt.tight_layout()
    plt.show()
