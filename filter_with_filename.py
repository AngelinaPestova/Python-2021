import numpy as np
from PIL import Image


def get_block_mean(arr, block_size):
    return int(np.sum(arr) / 3 // (block_size ** 2))


def make_block_gradation(
    start_y, start_x, arr,
    block_mean, block_size, gradations_amount
):
    color = int(block_mean // gradations_amount) * gradations_amount
    for row in range(start_y, start_y + block_size):
        for col in range(start_x, start_x + block_size):
            arr[row][col] = [color, color, color]
    return arr


def transform_image(img, block_size, gradation_amount):
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
    img = Image.open("img2.jpg")
    res = transform_image(img, 10, 50)
    res.save("res_filter_with_filename.jpg")


main()
