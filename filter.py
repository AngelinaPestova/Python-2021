import argparse

import numpy as np
from PIL import Image


def get_block_sum(start_y, start_x, arr, block_size):
    block_sum = 0
    for row in range(start_y, start_y + block_size):
        for col in range(start_x, start_x + block_size):
            red = int(arr[row][col][0])
            green = int(arr[row][col][1])
            blue = int(arr[row][col][2])
            block_sum += (red + green + blue) / 3
    block_sum = int(block_sum // block_size ** 2)
    return block_sum


def make_block_gradation(start_y, start_x, arr, block_sum, block_size, gradations_amount):
    for row in range(start_y, start_y + block_size):
        for col in range(start_x, start_x + block_size):
            arr[row][col][0] = int(block_sum // gradations_amount) * gradations_amount
            arr[row][col][1] = int(block_sum // gradations_amount) * gradations_amount
            arr[row][col][2] = int(block_sum // gradations_amount) * gradations_amount


def transform_image(img, block_size, gradation_amount):
    arr = np.array(img)
    height = len(arr)
    width = len(arr[1])
    for y in range(0, height - 1, block_size):
        for x in range(0, width - 1, block_size):
            block_sum = get_block_sum(y, x, arr, block_size)
            make_block_gradation(y, x, arr, block_sum, block_size, gradation_amount)
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
    res.save("result_image.jpg")


main()
