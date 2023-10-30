import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # Для отображения изображений

from lab2 import create_annotation_file, get_next_instance, collect_instances_by_class

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dataset Tool")
        
        # Переменные для хранения пути к папке датасета и текущего класса
        self.dataset_folder = ""
        self.current_class = ""
        self.used_instances = set()
        self.instances_by_class = {}

        # Элементы интерфейса
        self.dataset_label = tk.Label(root, text="Путь к папке с датасетом:")
        self.dataset_label.pack()
        
        self.dataset_path_entry = tk.Entry(root)
        self.dataset_path_entry.pack()
        
        self.browse_button = tk.Button(root, text="Обзор", command=self.browse_dataset_folder)
        self.browse_button.pack()
        
        self.annotation_button = tk.Button(root, text="Создать аннотацию", command=self.create_annotation)
        self.annotation_button.pack()
        
        self.display_label = tk.Label(root, text="")
        self.display_label.pack()

        self.class_buttons = [] 

    def browse_dataset_folder(self):
        self.dataset_folder = filedialog.askdirectory()
        self.dataset_path_entry.delete(0, tk.END)
        self.dataset_path_entry.insert(0, self.dataset_folder)
        self.create_class_buttons()
        collect_instances_by_class(self.instances_by_class ,self.dataset_folder)


    def create_class_buttons(self):
        if os.path.isdir(self.dataset_folder):
            for button in self.class_buttons:
                button.destroy()
            self.class_buttons = []

            for class_folder in os.listdir(self.dataset_folder):
                class_path = os.path.join(self.dataset_folder, class_folder)
                if os.path.isdir(class_path):
                    button_text = f"Следующий экземпляр {class_folder}"
                    button = tk.Button(self.root, text=button_text, command=lambda cf=class_folder: self.get_next_instance(cf))
                    button.pack()
                    self.class_buttons.append(button)

    def create_annotation(self):
        output_folder = filedialog.askdirectory()
        create_annotation_file(self.dataset_folder, output_folder)
        self.display_label.config(text=f"Аннотация создана: {output_folder}")

    def get_next_instance(self,class_folder):
        if self.current_class != class_folder:
            self.used_instances = set()
        if class_folder:
            self.current_class = class_folder
            instance_path = get_next_instance(self.used_instances, self.instances_by_class,class_folder, self.dataset_folder)
            if instance_path:
                self.display_instance(instance_path)

    def display_instance(self, instance_path):
        image = Image.open(instance_path)
        image = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.display_label.config(image=photo)
        self.display_label.photo = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
