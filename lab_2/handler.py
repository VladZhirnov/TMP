from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
import random
import os
import csv
import shutil

def create_dataset(main_window: QWidget) -> None:

    select_folder = main_window.select_folder
    folderpath = QtWidgets.QFileDialog.getExistingDirectory(main_window, "Выберите папку")
    print(f"Вы выбрали: {folderpath}")
    main_window.next_folder = folderpath
    
    new_folder_path = main_window.next_folder

    print("Создание файла аннотации исходного датасета")
    annotation_file = "annotation.csv"

    print(select_folder)
    print(new_folder_path)

    annotation_file = "annotation.csv"

    print(new_folder_path + "/" + annotation_file)

    with open(new_folder_path + "/" + annotation_file, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)

        for folder in os.listdir(select_folder):
            if folder != "tiger" and folder != "leopard":
                print("Не правильная папка")
                return None

            path_folder = os.path.join(select_folder, folder)

            for img in os.listdir(path_folder):
                img_path = os.path.join(path_folder, img)

                # Абсолютный путь
                absolute_path = os.path.abspath(img_path)

                # Относительный путь
                relative_path = os.path.relpath(img_path, select_folder)

                csv_writer.writerow([absolute_path, relative_path, folder])

    print("Файл создался")

def on_clicked_button(main_windows: QWidget) -> str:
    folderpath = QtWidgets.QFileDialog.getExistingDirectory(main_windows, "Выберите папку")
    print(f"Вы выбрали: {folderpath}")
    main_windows.select_folder = folderpath
    
def on_clicked_button_for_dataset(main_window: QWidget) -> None:
    print(main_window.select_folder)
    folderpath = QtWidgets.QFileDialog.getExistingDirectory(main_window, "Выберите папку")
    print(f"Вы выбрали: {folderpath}")
    main_window.next_folder = folderpath
    print(main_window.next_folder)

    create_dataset(main_window.select_folder, main_window.next_folder)




def copy_dataset_with_random(main_window: QWidget) -> None:
    source_dataset = main_window.select_folder
    folderpath = QtWidgets.QFileDialog.getExistingDirectory(main_window, "Выберите папку")
    print(f"Вы выбрали: {folderpath}")
    main_window.next_folder = folderpath
    
    target_dataset = main_window.next_folder

    os.makedirs(target_dataset, exist_ok=True)
    annotation_file = os.path.join(target_dataset, 'annotation.csv')

    with open(annotation_file, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        for folder in os.listdir(source_dataset):
            path_folder = os.path.join(source_dataset, folder)

            print(len(os.listdir(path_folder)))
            for img in os.listdir(path_folder):
                img_path = os.path.join(path_folder, img)

                new_img_name = f"{random.randint(1, 10000)}.jpg"

                # полный путь к новому файлу
                target_img_path = os.path.join(target_dataset, new_img_name)

                # копируем картинку в новую папку
                shutil.copy(img_path, target_img_path)

                # абсолютный путь
                absolute_path = os.path.abspath(target_img_path)

                # относительный патч
                relative_path = os.path.relpath(target_img_path, target_dataset)

                csv_writer.writerow([absolute_path, relative_path, folder])
    
    print("Датасет скопировался")


class Iterator:

    def __init__(self, class_label, dataset_path) -> None:
        self.class_label = class_label
        self.dataset_path = dataset_path
        self.class_path = os.path.join(self.dataset_path, class_label)
        self.instances = self.get_instances()


    def get_instances(self) -> list:
        if not os.path.exists(self.class_path):
            print(f"Папка {self.class_label} не найдена.")
            return None

        instances = os.listdir(self.class_path)
        random.shuffle(instances)
        return instances
    
    def __iter__(self):
        return self

    def __next__(self) -> str:
        if not self.instances:
            raise StopIteration("Экземпляры закончились.")
        return os.path.join(self.class_path, self.instances.pop(0))


def next_tiger(main_window: QWidget) -> None:
    class_label = "tiger"
    manager = Iterator(class_label, main_window.select_folder)

    image_path = manager.__next__()
    if image_path:
       main_window.current_image = QPixmap(image_path)
       main_window.label.setPixmap(main_window.current_image.scaled(400, 400))

def next_leopard(main_window: QWidget) -> None:
    class_label = "leopard"
    manager = Iterator(class_label, main_window.select_folder)

    image_path = manager.__next__()
    if image_path:
       main_window.current_image = QPixmap(image_path)
       main_window.label.setPixmap(main_window.current_image.scaled(400, 400))