import string
import random
from PIL import Image, ImageDraw, ImageFont


def generate_code(length=6):
    characters = string.digits + string.ascii_uppercase
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def generate_captcha_image(code):
    image_width = 200
    image_height = 80
    background_color = (255, 255, 255)

    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    font_size = 40
    font = ImageFont.truetype('./Arial.ttf', font_size)

    x_offset = random.randint(10, 30)
    y_offset = random.randint(10, 30)

    draw.text((x_offset, y_offset), code, font=font, fill=(0, 0, 0))

    noise_level = 0.05
    num_noise_pixels = int(image_width * image_height * noise_level)
    for _ in range(num_noise_pixels):
        x = random.randint(0, image_width - 1)
        y = random.randint(0, image_height - 1)
        draw.point((x, y), fill=(0, 0, 0))

    image.save("./app/static/captcha.png")
    return True
