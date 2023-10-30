# image_utils.py

from PIL import Image

def resize_image(input_image_path, output_image_path, size):
    """
    Изменяет размер изображения и сохраняет его.

    :param input_image_path: Путь к исходному изображению.
    :type input_image_path: str
    :param output_image_path: Путь, куда будет сохранено измененное изображение.
    :type output_image_path: str
    :param size: Новый размер изображения в формате (ширина, высота).
    :type size: tuple
    :return: None
    """
    with Image.open(input_image_path) as img:
        img = img.resize(size)
        img.save(output_image_path)

def convert_to_grayscale(input_image_path, output_image_path):
    """
    Конвертирует изображение в черно-белый формат и сохраняет его.

    :param input_image_path: Путь к исходному изображению.
    :type input_image_path: str
    :param output_image_path: Путь, куда будет сохранено измененное изображение.
    :type output_image_path: str
    :return: None
    """
    with Image.open(input_image_path) as img:
        img = img.convert('L')
        img.save(output_image_path)
