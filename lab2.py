import os
import random
import requests
from imageparser import YandexImage
import csv
import shutil

def parseImages(query):
    parser = YandexImage()
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    dir_path = os.path.join('dataset', query)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    image_counter = 0

    for item in parser.search(query, parser.size.large):
        print(item.title)
        print(item.url)
        print(item.preview.url)
        print("(", item.size, ")", sep='')
        filename = os.path.join(dir_path, f"{image_counter:04}.jpg")
        try:
            response = requests.get(item.url, stream=True)
            response.raise_for_status()
            
            # Запись изображения в файл
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            image_counter += 1
            if image_counter > 10:
                print("Reached the maximum image limit (10). Stopping the function.")
                break
        except requests.RequestException as e:
            print(f"Error downloading image from URL {item.url}. Error: {e}")

def create_annotation_file(class_folder, output_file):
    dataset_folder = 'dataset'
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Absolute Path', 'Relative Path', 'Class Label'])
        class_path = os.path.join(dataset_folder, class_folder)
        for root, dirs, files in os.walk(class_path):
            for file in files:
                if file.endswith('.jpg'):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, dataset_folder)
                    label = class_folder
                    writer.writerow([abs_path, rel_path, label])

def copy_dataset_with_rename(class_folder, output_folder):
    input_folder = 'dataset'
    for root, dirs, files in os.walk(os.path.join(input_folder, class_folder)):
        for file in files:
            if file.endswith('.jpg'):
                new_name = f"{class_folder}_{file}"
                old_path = os.path.join(root, file)
                new_path = os.path.join(output_folder, new_name)
                shutil.copy(old_path, new_path)

def create_copy_with_unique_random_names():
    input_folder = 'dataset'
    output_folder = 'newdataset'  
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    used_names = set()
    
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.jpg'):
                random_name = None
                while random_name is None or random_name in used_names:
                    random_name = str(random.randint(0, 10000)) + '.jpg'
                used_names.add(random_name)
                old_path = os.path.join(root, file)
                new_path = os.path.join(output_folder, random_name)
                shutil.copy(old_path, new_path)




parseImages("rose")
parseImages("tulip")