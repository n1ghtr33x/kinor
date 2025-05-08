import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QStackedWidget, QStackedLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class DiscordStyleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Discord-Style UI")
        self.setGeometry(100, 100, 800, 600)

        # Устанавливаем иконку (замените на свой путь)
        self.setWindowIcon(QIcon("path_to_icon.png"))

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        main_layout = QHBoxLayout()

        # Боковая панель
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: #2f3136;")
        sidebar_layout = QVBoxLayout()

        # Добавляем кнопки на боковую панель
        sidebar_layout.addWidget(QPushButton("Главная"))
        sidebar_layout.addWidget(QPushButton("Сообщения"))
        sidebar_layout.addWidget(QPushButton("Настройки"))
        sidebar_layout.addStretch()  # Снизу пустое пространство для выравнивания

        self.sidebar.setLayout(sidebar_layout)

        self.stacked_widget = QStackedWidget()



        # Контентное окно
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.addWidget(QLabel("Добро пожаловать в Discord-Style интерфейс"))
        content_widget.setLayout(content_layout)



        content_widget2 = QWidget()
        content_layout2 = QVBoxLayout()
        content_layout2.addWidget(QLabel("вторая страница"))
        content_widget2.setLayout(content_layout2)

        #self.stacked_widget.addWidget(content_widget2)

        # Собираем все в основной макет
        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(content_widget, 3)


        self.central_widget.setLayout(main_layout)

        self.stacked_widget.addWidget(content_widget)

        # Стилизация через QSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #36393f;
            }
            QPushButton {
                background-color: #2f3136;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7289da;
            }
            QLabel {
                color: white;
                font-size: 18px;
            }
        """)

class ChatScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("💬 Экран чата"))
        self.setLayout(layout)

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙️ Настройки"))
        self.setLayout(layout)

class Speak(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Kinor')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()

        self.sidebar = QWidget()
        self.sidebar.setStyleSheet('background-color: #2f3136;')
        sidebar_layout = QVBoxLayout()

        btn_main = QPushButton('Main')
        btn_messages = QPushButton('Messages')

        sidebar_layout.addWidget(btn_main)
        sidebar_layout.addWidget(btn_messages)
        sidebar_layout.addStretch()
        self.sidebar.setLayout(sidebar_layout)

        self.stack = QStackedWidget()
        self.chat_screen = ChatScreen()
        self.settings_screen = SettingsScreen()
        self.stack.addWidget(self.chat_screen)      # index 1
        self.stack.addWidget(self.settings_screen)

        #QLabel("hello to Kinor")

        btn_main.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_messages.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(self.stack, 3)
        self.central_widget.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #36393f;
                color: white;
                font-size: 16px;
            }
            QPushButton {
                background-color: #2f3136;
                border: none;
                padding: 12px;
                border-radius: 6px;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #7289da;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = DiscordStyleWindow()
    window = Speak()
    window.show()
    sys.exit(app.exec_())
