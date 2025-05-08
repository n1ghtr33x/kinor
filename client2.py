import socket
import threading
import pyaudio
import numpy as np
import noisereduce as nr
from config import config

CHUNK = 2048  # Размер чанка
SAMPLE_RATE = 44100  # Частота дискретизации
p = pyaudio.PyAudio()

# Инициализация аудиопотока
stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, output=True, frames_per_buffer=CHUNK)

# Создаем сокет для подключения к серверу
s = socket.socket()
s.connect((config.HOST, config.PORT))

def apply_noise_reduction(audio_data):
    # Применение шумоподавления с помощью noisereduce
    reduced_noise = nr.reduce_noise(y=audio_data, sr=SAMPLE_RATE)
    return reduced_noise

def record_and_send_audio():
    while True:
        try:
            # Чтение данных с микрофона
            data = stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Применяем шумоподавление
            processed_audio_data = apply_noise_reduction(audio_data)

            # Отправляем обработанные данные на сервер
            s.send(processed_audio_data.tobytes())

        except Exception as e:
            print(f"Ошибка при обработке или отправке аудио: {e}")

def recv_audio():
    while True:
        try:
            data = s.recv(CHUNK)
            if not data:
                break
            stream.write(data)
        except Exception as e:
            print(f"Ошибка при получении аудио: {e}")
            break

# Запуск потоков
send_thread = threading.Thread(target=record_and_send_audio)
recv_thread = threading.Thread(target=recv_audio)

send_thread.daemon = True
recv_thread.daemon = True

send_thread.start()
recv_thread.start()

# Ожидание завершения потоков
send_thread.join()
recv_thread.join()

# Закрытие потоков и сокета
stream.stop_stream()
stream.close()
s.close()
p.terminate()
