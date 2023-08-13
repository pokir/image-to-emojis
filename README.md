# image-to-emoji

This program turns images into emojis (all emojis).

## How to use it (MacOS/Linux)

Instructions for Windows are not included but it is possible (follow the same steps but with Windows commands).

### Install the required packages

```py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the code

For example, to convert `YOUR_IMAGE.png` to emoji with `50` emojis per line, run:

```py
source venv/bin/activate
python3 image_to_emoji.py YOUR_IMAGE.png 50
```

This will write the output to `output.txt`.

You then just have to send every block of emojis separated by `---` as a separate message in discord (because discord has a 199 emoji per message limit).

## Developer notes

The average colors for each emoji were calculated using:

```py
python3 calculate_average_emoji_colors.py
```

The `emojis` directory must exist and every emoji must be in svg format.
The name of the emoji in discord must be the name of the file.
