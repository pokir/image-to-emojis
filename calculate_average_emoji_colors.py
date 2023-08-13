import cairosvg
from io import BytesIO
import os
import PIL
from PIL import Image
import sys


buffer = ''

# iterate over every emoji image in the `emojis` directory and find the average
# color of it
for subdir, dirs, files in os.walk('emojis'):
    for file in files:
        emoji_image_path = os.path.join(subdir, file)
        emoji_name = os.path.splitext(file)[0]

        # convert svg to png
        out = BytesIO()
        cairosvg.svg2png(url=emoji_image_path, write_to=out)

        average_red = 0
        average_green = 0
        average_blue = 0

        with Image.open(out) as im:
            pixels = im.load()
            dim_x, dim_y = im.size

        for y in range(dim_y):
            for x in range(dim_x):
                red, green, blue = pixels[x, y][:-1]

                # add to the running sum
                average_red += red
                average_green += green
                average_blue += blue

        num_pixels = im.size[1] * im.size[0]

        # divide the sum by the number of pixels to give an average color
        average_red /= num_pixels
        average_green /= num_pixels
        average_blue /= num_pixels

        buffer += f'{emoji_name} {average_red},{average_green},{average_blue}\n'

# remove the final newline
buffer = buffer[:-1]

with open('emojis_average_colors.txt', 'w') as f:
    f.write(buffer)
