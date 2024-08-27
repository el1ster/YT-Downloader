import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
import yt_dlp
from concurrent.futures import ThreadPoolExecutor


class VideoDownloader(QThread):
    update_status = pyqtSignal(str)

    def __init__(self, urls, output_path):
        super().__init__()
        self.urls = urls
        self.output_path = output_path

    def download_video(self, url):
        try:
            ydl_opts = {
                'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',
                'format': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080][ext=mp4]',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.update_status.emit(f"Відео успішно завантажене: {url}")
        except Exception as e:
            self.update_status.emit(f"Сталася помилка при завантаженні {url}: {e}")

    def run(self):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download_video, url) for url in self.urls]
            for future in futures:
                future.result()


class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Downloader')
        self.setGeometry(200, 200, 500, 300)

        layout = QVBoxLayout()

        # Стилізація шрифтів
        font = QFont('Arial', 10)
        self.setFont(font)

        # Поле ввода URL
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Введіть URL відео (через кому, якщо декілька)')
        layout.addWidget(self.url_input)

        # Метка для пути сохранения
        self.save_path_label = QLabel('Шлях до папки для збереження:', self)
        layout.addWidget(self.save_path_label)

        # Кнопка для выбора пути сохранения
        self.save_path_btn = QPushButton('Вибрати папку', self)
        self.save_path_btn.clicked.connect(self.select_save_path)
        layout.addWidget(self.save_path_btn)

        # Кнопка для начала загрузки
        self.download_btn = QPushButton('Завантажити', self)
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        # Метка для статуса
        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Загрузка стилей из файла
        with open('styles.css', 'r') as f:
            self.setStyleSheet(f.read())

    def select_save_path(self):
        save_path = QFileDialog.getExistingDirectory(self, 'Виберіть папку для збереження')
        if save_path:
            self.save_path_label.setText(f'Шлях до папки для збереження: {save_path}')
        else:
            self.save_path_label.setText('Шлях до папки для збереження: (поточна папка)')

    def start_download(self):
        urls = self.url_input.text().split(',')
        save_path = self.save_path_label.text().split(': ')[1] or '.'

        self.status_label.setText('Завантаження...')
        self.download_thread = VideoDownloader(urls, save_path)
        self.download_thread.update_status.connect(self.update_status)
        self.download_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = DownloaderApp()
    downloader.show()
    sys.exit(app.exec_())
