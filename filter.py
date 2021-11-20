import argparse
import doctest

import numpy as np
from PIL import Image


def get_block_mean(arr, block_size):
    """
    Возвращает среднее значение сумм цветов пикселей для заданного участка

    Параметры:
    :param arr: Массив участка
    :param block_size: Размер блока
    :return: Среднее значение цвета пикселей для заданного участка

    >>> get_block_mean([[[1, 1, 3]]], 1)
    1
    >>> get_block_mean([[[1, 2, 3]]], 1)
    2
    >>> get_block_mean([[[0, 0, 0]]], 1)
    0
    >>> get_block_mean([[[5, 4, 3]] * 3] * 3, 3)
    4
    """
    return int(np.sum(arr) / 3 // (block_size ** 2))


def make_block_gradation(
    start_y, start_x, arr,
    block_mean, block_size, gradations_amount
):
    """
    Возвращает массив с измененным цветом пикселей у заданного участка

    :param start_y: y-координата левого нижнего пикселя участка
    :param start_x: x-координата левого нижнего пикселя участка
    :param arr: Исходный массив
    :param block_mean: Среднее значение цвета пикселей для заданного участка
    :param block_size: Размер блока
    :param gradations_amount: Количество градаций серого
    :return: Массив с измененным цветом у заданного участка
    """
    color = int(block_mean // gradations_amount) * gradations_amount
    for row in range(start_y, start_y + block_size):
        for col in range(start_x, start_x + block_size):
            arr[row][col] = [color, color, color]
    return arr


def transform_image(img, block_size, gradation_amount):
    """
    Возвращает изображение с наложенным фильтром

    :param img: Исходное изображение
    :param block_size: Размер блока
    :param gradation_amount: Количество градаций серого
    :return: Изображение с наложенным фильтром
    """
    arr = np.array(img)
    height = len(arr)
    width = len(arr[1])
    for y in range(0, height - 1, block_size):
        for x in range(0, width - 1, block_size):
            block_mean = get_block_mean(
                arr[y:y + block_size, x:x + block_size],
                block_size
            )
            arr = make_block_gradation(
                y, x, arr, block_mean,
                block_size, gradation_amount
            )
    return Image.fromarray(arr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_image", type=str, default="img2.jpg")
    parser.add_argument("-block_size", type=int, default=10)
    parser.add_argument("-gradation_amount", type=int, default=50)
    args = parser.parse_args()

    img = Image.open(args.input_image)
    block_size = args.block_size
    gradation_amount = args.gradation_amount

    res = transform_image(img, block_size, gradation_amount)
    res.save("res_filter.jpg")


print(doctest.testmod())
main()
