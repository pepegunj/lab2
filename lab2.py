import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Функция для создания папок и загрузки изображений
def download_images(query, class_name, num_images):
    # Создаем папку dataset, если она не существует
    if not os.path.exists('dataset'):
        os.mkdir('dataset')
    
    # Создаем папку для класса, если она не существует
    class_folder = os.path.join('dataset', class_name)
    if not os.path.exists(class_folder):
        os.mkdir(class_folder)
    
    # Ссылка на страницу с результатами поиска
    search_url = f'https://yandex.ru/images/search?text={query}'
    
    # Отправляем запрос на страницу поиска
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Счетчик загруженных изображений
    downloaded_images = 0
    
    # Парсим миниатюры изображений
    for thumbnail in soup.find_all('img', class_='serp-item__thumb'):
        img_url = thumbnail.get('src')
        
        # Собираем абсолютную ссылку
        img_url = urljoin(search_url, img_url)
        
        # Определяем расширение файла
        img_ext = '.jpg'  # Устанавливаем расширение .jpg
        
        # Сохраняем изображение
        img_filename = f'{downloaded_images:04d}{img_ext}'
        img_path = os.path.join(class_folder, img_filename)
        
        # Загружаем изображение
        img_data = requests.get(img_url).content
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
        
        downloaded_images += 1
        
        # Если достигнуто заданное количество изображений, выходим из цикла
        if downloaded_images >= num_images:
            break
    
    print(f'Downloaded {downloaded_images} images for class {class_name}')

# Загрузка изображений для класса "rose"
download_images('rose', 'rose', 1000)

# Загрузка изображений для класса "tulip"
download_images('tulip', 'tulip', 1000)
