#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageOps
from colour import Color
import random


def get_base_color(
    color_string=None, sat_min=0.2, sat_max=1.0, lum_min=0.2, lum_max=0.9
):
    """Get base color for a huepaper by color string."""
    # If no color string is given, create a random color
    if not color_string:
        hue = random.uniform(0, 1)
        sat = random.uniform(sat_min, sat_max)
        lum = random.uniform(lum_min, lum_max)
        base_color = Color(hue=hue, saturation=sat, luminance=lum)

    # Else try to parse string
    else:
        try:
            base_color = Color(color_string)
        except:
            try:
                base_color = Color("#{}".format(color_string))
            except:
                raise Exception("Invalid color expression: {}".format(color_string))

    return base_color


def create_colors(
    base_color=None, hue_max=0.1, sat_min=0.2, sat_max=1.0, lum_min=0.3, lum_max=0.9
):
    """Create four corner colors for a huepaper by an optional base color."""
    if not base_color:
        base_color = get_base_color(None, sat_min, sat_max, lum_min, lum_max)

    colors = []

    max_sat_diff = 0.1
    max_lum_diff = 0.1

    # Create four random colors similar to the given base_color
    for i in range(0, 4):

        tmp_hue = base_color.hue + random.uniform(-hue_max / 2.0, hue_max / 2.0)
        if tmp_hue > 1.0:
            tmp_hue -= 1

        tmp_sat = base_color.saturation + random.uniform(-max_sat_diff, max_sat_diff)
        tmp_sat = min(sat_max, max(sat_min, tmp_sat))

        tmp_lum = base_color.luminance + random.uniform(-max_lum_diff, max_lum_diff)
        tmp_lum = min(lum_max, max(lum_min, tmp_lum))

        color = Color(hue=tmp_hue, saturation=tmp_sat, luminance=tmp_lum)
        colors.append(color.rgb)

    return tuple(colors)


def create_base_image(c1, c2, c3, c4, width=1920, height=1080):
    """Create a base huepaper by four corner colors.

    c1 - top left
    c2 - top right
    c3 - bottom right
    c4 - bottom left
    """
    # Lambda for adding four colors
    add = lambda c1, c2, c3, c4: (
        c1[0] + c2[0] + c3[0] + c4[0],
        c1[1] + c2[1] + c3[1] + c4[1],
        c1[2] + c2[2] + c3[2] + c4[2],
    )

    # Lambda for multiplying a color with a factor
    mul = lambda c, x: (c[0] * x, c[1] * x, c[2] * x)

    # Lambda for scaling a color from [0 , 1] to [0, 255]
    cor = lambda c: (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))

    # Lambda for calculating a color at x and y in range [0, 1]
    #  Color limits are set at creation
    col = lambda x, y, c1=c1, c2=c2, c3=c3, c4=c4: cor(
        add(
            mul(c1, (1.0 - x) * (1.0 - y)),
            mul(c2, x * (1.0 - y)),
            mul(c3, x * y),
            mul(c4, (1.0 - x) * y),
        )
    )

    # Create image
    image = Image.new("RGBA", (width, height))
    pixels = image.load()

    for x in range(0, width):
        for y in range(0, height):
            pixels[x, y] = col(x / (width - 1), y / (height - 1))

    return image


def add_lines(image, color):
    """Add one to three random lines to an image with given color."""
    width, height = image.size

    line_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(line_image)

    # Set color
    color = tuple(map(lambda x: int(x * 255), color))

    # Generate lines
    number_of_lines = random.randint(1, 3)
    scale = width / 100.0
    base_width = random.randint(int(2 * scale), int(5 * scale))
    rand_width = lambda base_width=base_width: base_width + random.randint(
        -base_width // 2, base_width // 2
    )
    space = rand_width() // 2
    offset = random.randint(0, space)
    for i in range(0, number_of_lines):
        line_width = rand_width()
        x = offset + space + (line_width // 2)
        draw.line((x, 0, x, height), fill=color, width=line_width)
        offset += space + line_width

    # Mirror line image eventually
    orientation = random.randrange(2)
    if orientation == 1:
        line_image = ImageOps.mirror(line_image)

    # Add line image to input image
    image.alpha_composite(line_image, (0, 0))

    return image


def add_pixelation(image, x=16, y=9):
    """Pixelate an image."""
    width, height = image.size

    image = image.resize((x, y))
    image = image.resize((width, height), Image.BOX)

    return image


def add_emblem(image, filepath):
    """Add an amblem to an image by filepath."""
    width, height = image.size

    # Load image
    try:
        emblem_image = Image.open(filepath)
    except Exception as e:
        raise Exception("Failed to load emblem: {}".format(e))

    # Exit if emblem is too big
    if emblem_image.size[0] > width or emblem_image.size[1] > height:
        raise Exception("Emblem can't be bigger than the huepaper")

    # Insert emblem in the center
    offset = (
        (image.size[0] - emblem_image.size[0]) // 2,
        (image.size[1] - emblem_image.size[1]) // 2,
    )
    image.alpha_composite(emblem_image, offset)

    return image
