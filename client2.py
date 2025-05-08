import sys
import socket
import threading
import pyaudio
from config import config

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import qdarkstyle

CHUNK = config.CHUNK
SAMPLE_RATE = 44100
p = pyaudio.PyAudio()

class Communicator(QObject):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

class VoiceChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.s = None
        self.stream = None
        self.is_connected = False
        self.comm = Communicator()
        self.comm.log_signal.connect(self.log)
        self.comm.status_signal.connect(self.update_status)

    def init_ui(self):
        self.setWindowTitle("🎧 Voice Chat Client")
        self.setGeometry(600, 200, 500, 400)
        self.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border-radius: 8px;
                background-color: #444;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #222;
                color: #9fdfbf;
                font-family: Consolas;
                font-size: 12px;
                border-radius: 6px;
            }
        """)

        layout = QVBoxLayout()

        self.status_label = QLabel("🔴 Отключено")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")

        self.toggle_button = QPushButton("Подключиться / Отключиться")
        self.toggle_button.clicked.connect(self.toggle_connection)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.toggle_button)
        top_bar.addWidget(self.status_label, alignment=Qt.AlignRight)

        layout.addLayout(top_bar)
        layout.addWidget(self.log_box)
        self.setLayout(layout)

    def log(self, message):
        self.log_box.append(f"[LOG] {message}")

    def update_status(self, status_text):
        if "🟢" in status_text:
            self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_label.setText(status_text)

    def toggle_connection(self):
        if not self.is_connected:
            self.start_connection()
        else:
            self.stop_connection()

    def start_connection(self):
        try:
            self.s = socket.socket()
            self.s.connect((config.HOST, config.PORT))
            self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, output=True, frames_per_buffer=CHUNK)
            self.is_connected = True

            self.send_thread = threading.Thread(target=self.send_audio)
            self.recv_thread = threading.Thread(target=self.recv_audio)
            self.send_thread.start()
            self.recv_thread.start()

            self.comm.status_signal.emit("🟢 Подключено")
            self.comm.log_signal.emit("Соединение установлено.")
        except Exception as e:
            self.comm.log_signal.emit(f"Ошибка подключения: {e}")

    def stop_connection(self):
        self.is_connected = False
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.s:
                self.s.close()
            self.comm.status_signal.emit("🔴 Отключено")
            self.comm.log_signal.emit("Отключено от сервера.")
        except Exception as e:
            self.comm.log_signal.emit(f"Ошибка при отключении: {e}")

    def send_audio(self):
        while self.is_connected:
            try:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                self.s.send(data)
            except Exception as e:
                self.comm.log_signal.emit(f"Ошибка отправки: {e}")
                break

    def recv_audio(self):
        while self.is_connected:
            try:
                data = self.s.recv(CHUNK)
                if not data:
                    break
                self.stream.write(data)
            except Exception as e:
                self.comm.log_signal.emit(f"Ошибка получения: {e}")
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = VoiceChatClient()
    window.show()
    sys.exit(app.exec_())
