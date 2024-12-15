import os
import logging

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QApplication, QFileDialog
from PyQt6.QtGui import QPixmap

from annotation import create_annotation
from copy1 import copy_dataset  
from copy_dataset import copy_dataset_with_random_numbers
from Instance_Iterator import InstanceIterator


logging.basicConfig(level = logging.DEBUG, 
                    format = "%(asctime)s - %(levelname)s - %(message)s",
                    handlers = [
                        logging.FileHandler("logging.log"),
                        logging.StreamHandler()
                    ])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        logging.info("Инициализация главного окна приложения")

        self.selected_folder_path = None
        self.current_image = None 
        self.resize(300, 100)
        self.folder_path_label = QtWidgets.QLabel('Выберите папку с исходным датасетом:')
        self.folder_path_button = QtWidgets.QPushButton('Выбрать папку', self)
        self.create_annotation_button = QtWidgets.QPushButton('Создать аннотацию', self)
        self.copy_dataset_button = QtWidgets.QPushButton('Создать датасет c файлами типа class_0000.jpg', self)
        self.copy_dataset_with_random_numbers_button = QtWidgets.QPushButton('Создать датасет со случ. названиями файлов', self)

        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 100, 100)
        layout.addWidget(self.label)
        layout.addWidget(self.button1())
        layout.addWidget(self.button2())
        layout.addWidget(self.folder_path_label)
        layout.addWidget(self.folder_path_button)
        layout.addWidget(self.create_annotation_button)
        layout.addWidget(self.copy_dataset_button)
        layout.addWidget(self.copy_dataset_with_random_numbers_button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.folder_path_button.clicked.connect(self.get_folder_path)
        self.create_annotation_button.clicked.connect(self.create_annotation)
        self.copy_dataset_button.clicked.connect(self.copy_dataset)
        self.copy_dataset_with_random_numbers_button.clicked.connect(self.copy_dataset_with_random_numbers)

    def get_folder_path(self) -> None:
        """Getting the folder path"""
        logging.info("Получение папки с исходным датасетом")
        self.selected_folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с исходным датасетом')
        if self.selected_folder_path:
            logging.info(f"Выбрана папка: {self.selected_folder_path}")
            logging.debug(f"Абсолютный путь к папке: {os.path.abspath(self.selected_folder_path)}")
        else:
            logging.warning("Папка не выбрана")

    def create_annotation(self) -> None:
        """Creating an annotation for a folder"""
        if not self.selected_folder_path:
            logging.error("Ошибка: папка с исходным датасетом не выбрана")
            return QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Выберите папку с исходным датасетом.')
        relative_path = os.path.relpath(self.selected_folder_path)
        create_annotation(relative_path)
        logging.info(f"Аннотация создана для папки: {relative_path}")

    def copy_dataset(self) -> None:
        """Creating a copy of the dataset folder to another folder"""
        if not self.selected_folder_path:
            logging.error("Ошибка: папка с исходным датасетом не выбрана")
            return QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Выберите папку с исходным датасетом.')
        new_directory = QFileDialog.getExistingDirectory(self, 'Выберите папку для нового датасета')
        if new_directory:
            relative_path1 = os.path.relpath(self.selected_folder_path)
            relative_path2 = os.path.relpath(new_directory)
            copy_dataset(relative_path1, relative_path2)
            logging.info(f"Датасет скопирован в новую папку: {relative_path2}")
        else:
            logging.warning("Папка для нового датасета не выбрана")
    
    def copy_dataset_with_random_numbers(self)-> None:
        """Creating a copy of the dataset folder with a random number of files"""
        if not self.selected_folder_path:
            logging.error("Ошибка: папка с исходным датасетом не выбрана")
            return QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Выберите папку с исходным датасетом.')
        relative_path = os.path.relpath(self.selected_folder_path)
        copy_dataset_with_random_numbers(relative_path)
        logging.info(f"Датасет скопирован с случайными номерами файлов в папку: copy_{relative_path}")

    def next_tiger(self) -> None:
        """Iterator for tiger"""
        if not self.selected_folder_path:
            logging.error("Ошибка: папка с исходным датасетом не выбрана")
            return None
        self.class_label = "tiger"
        logging.info("Показ следующего изображения класса 'tiger'")
        instances = InstanceIterator(self.class_label, self.selected_folder_path)
        image_path = instances.__next__()
        logging.debug(f"Загружено изображение: {image_path}")
        self.current_image = QPixmap(image_path)
        self.label.setPixmap(self.current_image.scaled(400, 400))

    def next_leopard(self) -> None:
        """Iterator for leopard"""
        if not self.selected_folder_path:
            logging.error("Ошибка: папка с исходным датасетом не выбрана")
            return None
        self.class_label = "leopard"
        logging.info("Показ следующего изображения класса 'leopard'")
        instances = InstanceIterator(self.class_label, self.selected_folder_path)
        image_path = instances.__next__()
        logging.debug(f"Загружено изображение: {image_path}")
        self.current_image = QPixmap(image_path)
        self.label.setPixmap(self.current_image.scaled(400, 400))

    def button1(self) -> QPushButton:
        """create button1"""
        button = QPushButton("Следующая картинка tiger")
        button.clicked.connect(self.next_tiger)
        return button

    def button2(self) -> QPushButton:
        """create button2"""
        button = QPushButton("Следующая картинка leopard")
        button.clicked.connect(self.next_leopard)
        return button
    

if __name__ == "__main__":
    logging.info("Приложение запущено")
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    logging.info("Приложение завершено")