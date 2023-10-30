import datetime
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

def create_annotation_file(dataset_folder='dataset', output_folder='output_folder'):
    # Генерируем имя файла аннотации с текущим временем в миллисекундах
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    output_file = os.path.join(output_folder, f'annotation_{timestamp}.csv')

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Absolute Path', 'Relative Path', 'Class Label'])

        for class_folder in os.listdir(dataset_folder):
            class_path = os.path.join(dataset_folder, class_folder)
            if os.path.isdir(class_path):
                for root, dirs, files in os.walk(class_path):
                    for file in files:
                        if file.endswith('.jpg'):
                            abs_path = os.path.abspath(os.path.join(root, file))
                            rel_path = os.path.relpath(abs_path, dataset_folder)
                            label = class_folder
                            writer.writerow([abs_path, rel_path, label])



def copy_dataset_with_rename(output_folder):
    input_folder = 'dataset'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    class_folders = os.listdir(input_folder)

    for class_folder in class_folders:
        if os.path.isdir(os.path.join(input_folder, class_folder)):
            files = os.listdir(os.path.join(input_folder, class_folder))
            for file in files:
                if file.endswith('.jpg'):
                    new_name = f"{class_folder}_{file}"
                    old_path = os.path.join(input_folder, class_folder, file)
                    new_path = os.path.join(output_folder, new_name)
                    shutil.copy(old_path, new_path)

def create_copy_with_unique_random_names(output_folder):
    input_folder = 'dataset'
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


#used_instances = set()
#instances_by_class = {}

def collect_instances_by_class(instances_by_class:dict,dataset_folder='dataset'):
    for class_folder in os.listdir(dataset_folder):
        if os.path.isdir(os.path.join(dataset_folder, class_folder)):
            instances = [f for f in os.listdir(os.path.join(dataset_folder, class_folder)) if f.endswith('.jpg')]
            if instances:
                instances_by_class[class_folder] = instances
def get_next_instance(used_instances:set , instances_by_class:dict, class_folder, dataset_folder='dataset'):
    if class_folder not in instances_by_class:
        print('None')
        return None

    instances = instances_by_class[class_folder]
    if not instances:
        print('None')
        return None

    unused_instances = list(set(instances) - used_instances)
    if not unused_instances:
        print('None')
        return None

    random_instance = random.choice(unused_instances)
    used_instances.add(random_instance)
    instance_path = os.path.join(dataset_folder, class_folder, random_instance)
    print(instance_path)
    return instance_path


# parseImages("rose")
# parseImages("tulip")
# create_annotation_file('rose','annotation.csv')
# copy_dataset_with_rename('newset1')
# create_copy_with_unique_random_names('newset2')
# get_next_instance('tulip')


