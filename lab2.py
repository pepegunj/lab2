import os

import requests
from imageparser import YandexImage

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
            if image_counter > 15:
                print("Reached the maximum image limit (15). Stopping the function.")
                break
        except requests.RequestException as e:
            print(f"Error downloading image from URL {item.url}. Error: {e}")


parseImages("rose")
parseImages("tulip")