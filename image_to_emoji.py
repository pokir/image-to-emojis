import os
import PIL
from PIL import Image
import sys


# dark to light (maps to 255 to 0)
skin_tones = reversed(range(1, 6))
emojis = [f':thumbsup_tone{skin_tone}:' for skin_tone in skin_tones]

emoji_average_colors = {}

with open('emoji_average_colors.txt') as f:
    lines = f.read().split('\n')[:-1]

    for line in lines:
        emoji_name, emoji_average_color_string = line.split()
        emoji_average_color = tuple(map(float, emoji_average_color_string.split(',')))
        emoji_average_colors[emoji_name] = emoji_average_color

try:
    image_path = sys.argv[1]
except IndexError:
    image_path = input('Image path: ')

try:
    width = int(sys.argv[2])
except IndexError:
    width = int(input('How many emojis should be on one line? '))
    print()

try:
    with Image.open(image_path) as im:
        resized = im.resize((width, int(im.size[1] * width / im.size[0])))

except (FileNotFoundError, PIL.UnidentifiedImageError):
    print(f'No image found at "{image_path}".')

pixels = resized.load()

# because of discord emoji limits (199 emojis max per message), the buffer must
# be broken up
lines_per_message = 199 // width 

buffer = ''
line_count = 0

for y in range(resized.size[1]):
    for x in range(resized.size[0]):
        # select the emoji based on the one that best matches the pixel color
        pixel = pixels[x, y]

        least_color_error = None
        least_color_error_emoji = None

        for emoji, emoji_average_color in emoji_average_colors.items():
            color_error = sum([abs(pixel[i] - emoji_average_color[i])
                               for i in range(3)])

            if least_color_error == None or color_error < least_color_error:
                least_color_error = color_error
                least_color_error_emoji = emoji

        buffer += least_color_error_emoji

    buffer += '\n'
    line_count += 1

    if line_count % lines_per_message == 0:
        # add a separator so the user knows where to cut the message
        buffer += '\n' + '-' * 20 + '\n\n'

print(buffer)

with open('output.txt', 'w') as f:
    f.write(buffer)
