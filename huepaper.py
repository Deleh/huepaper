#!/usr/bin/env python

import argparse
import os.path
import random
import sys
from colour import Color
from PIL import Image, ImageDraw, ImageOps


def print_logo():
    logo = '''
 .lk.
  cO.
  cO.;:lc.  ,c.  .cc   .,',c;  .,c.;coc.   ;,.,c.  ':l.:lo:    '',:c.  '::.lo. 
  cO'   kd  .O;   dO  ,x...,Ox  cO;   lO: ;x   xk   OO.  .kO. x;...x0'  0x. .  
  cO.   xx  .O;   dO  ko......  :O.    Ox  .,..xO   kk    ;0;;0......   0d     
  cO.   xx  .O;   xO  dO.    .. :O.   .O; dk   xO   kk    :O.'0o     ,  0d     
 .dk,  .kk.  okc;,ox'  ckxllc.  :Oc'.,l'  oOl;'dO:. kO;..:l.  ,xOolc;  ,Ox.    
                                :O.                 kk                         
                                lO,                 OO                         
 OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO00O0000000000000000; 
''';
    print(logo)

# Get base color
def get_base_color(color_string = None):

    # If no color string is given, create a random color
    if not color_string:
        hue = random.uniform(0, 1)
        sat = random.uniform(sat_min, sat_max)
        lum = random.uniform(lum_min, lum_max)
        base_color = Color(hue = hue, saturation = sat, luminance = lum)
        print('Selected random base color: {}'.format(base_color.hex))

    # Else try to parse string
    else:
        try:
            base_color = Color(color_string)
        except:
            print('Not a valid color expression: {}'.format(color_string))
            sys.exit(1)

    return base_color


# Create colors from a base color
def create_colors(base_color):

    colors = []
    
    max_sat_diff = 0.1
    max_lum_diff = 0.1

    # Create four random colors similar to the given base_color
    for i in range(0, 4):

        tmp_hue = base_color.hue + random.uniform(-max_hue / 2.0, max_hue / 2.0)
        if tmp_hue > 1.0:
            tmp_hue -= 1

        tmp_sat = base_color.saturation + random.uniform(-max_sat_diff, max_sat_diff)
        tmp_sat = min(sat_max, max(sat_min, tmp_sat))
        
        tmp_lum = base_color.luminance + random.uniform(-max_lum_diff, max_lum_diff)
        tmp_lum = min(lum_max, max(lum_min, tmp_lum))

        color = Color(hue = tmp_hue, saturation = tmp_sat, luminance = tmp_lum)
        colors.append(color.rgb)

    return tuple(colors)


# Create base image from four colors, width and height
# c1 - top left
# c2 - top right
# c3 - bottom right
# c4 - bottom left
def create_base_image(c1, c2, c3, c4):

    # Lambda for adding four colors
    add = lambda c1, c2, c3, c4 : (c1[0] + c2[0] + c3[0] + c4[0], c1[1] + c2[1] + c3[1] + c4[1], c1[2] + c2[2] + c3[2] + c4[2])

    # Lambda for multiplying a color with a factor
    mul = lambda c, x : (c[0] * x, c[1] * x, c[2] * x)

    # Lambda for scaling a color from [0 , 1] to [0, 255]
    cor = lambda c : (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))

    # Lambda for calculating a color at x and y in range [0, 1]
    #  Color limits are set at creation
    col = lambda x, y, c1 = c1, c2 = c2, c3 = c3, c4 = c4 : cor(add(mul(c1, (1.0 - x) * (1.0 - y)), mul(c2, x * (1.0 - y)), mul(c3, x * y), mul(c4, (1.0 - x) * y)))

    # Create image
    image = Image.new('RGBA', (width, height))
    pixels = image.load()
    
    for x in range(0, width):
        for y in range(0, height):
            pixels[x, y] = col(x / (width - 1), y / (height - 1))

    return image


# Add lines to an image
def add_lines(image, color):

    line_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(line_image)

    # Set color
    color = tuple(map(lambda x : int(x * 255), color))

    # Generate lines
    number_of_lines = random.randint(1, 3)
    scale = width / 100.0
    base_width = random.randint(int(2 * scale), int(5 * scale))
    rand_width = lambda base_width = base_width : base_width + random.randint(-base_width // 2, base_width // 2)
    space = rand_width() // 2
    offset = random.randint(0, space)
    for i in range(0, number_of_lines):
        line_width = rand_width()
        x = offset + space + (line_width // 2)
        draw.line((x, 0, x, height), fill = color, width = line_width)
        offset += space + line_width

    # Mirror line image eventually
    orientation = random.randrange(2)
    if orientation == 1:
        line_image = ImageOps.mirror(line_image)

    # Add line image to input image
    image.alpha_composite(line_image, (0, 0))
    
    return image


# Add pixelation to image
def add_pixelation(image, x, y):

    image = image.resize((x, y))
    image = image.resize((width, height), Image.BOX)

    return image


# Add emblem to an image from a filepath
def add_emblem(image, filepath):

    # Load image
    try:
        emblem_image = Image.open(filepath)
    except Exception as e:
        print('Failed to load emblem: {}'.format(e))
        sys.exit(1)

    # Exit if emblem is too big
    if emblem_image.size[0] > width or emblem_image.size[1] > height:
        print('Emblem can\'t be bigger than the wallpaper')
        sys.exit(1)

    # Insert emblem in the center
    offset = ((image.size[0] - emblem_image.size[0]) // 2, (image.size[1] - emblem_image.size[1]) // 2)
    image.alpha_composite(emblem_image, offset)

    return image


# Save image to filepath
def save_image(filepath, image):

    save = True

    # Check whether file exists
    if os.path.isfile(filepath):
        overwrite = input('The file {} already exists. Do you want to overwrite it? [y/N] '.format(filepath))
        if overwrite != 'y' and overwrite != 'Y':
            save = False

    if save:

        stop = False
        while not stop:
            try:
                image.save(filepath)
                stop = True
            except Exception as e:
                print('Failed to save wallpaper: {}'.format(e))
                again = input('Do you want to try again? [Y/n] ')
                if again == 'n' or again == 'N':
                    stop = True
                else:
                    filepath = input('Please enter new path where the wallpaper shall be saved: ')


'''
Main
'''

def main():

    global width, height, max_hue, sat_min, sat_max, lum_min, lum_max

    # Initialize parser
    parser = argparse.ArgumentParser(description = 'Create wallpapers based on color hues.')
    parser.add_argument('-W', '--width', default = 1920, type = int, help = 'width of huepaper (default: 1920)')
    parser.add_argument('-H', '--height', default = 1080, type = int, help = 'height of huepaper (default: 1080)')
    parser.add_argument('-c', '--color', help = 'color, the huepaper is generated from (uses a random color if not given)')
    parser.add_argument('-p', '--preview', action = 'store_true', help = 'preview huepaper')
    parser.add_argument('-o', '--output', help = 'file where to save the huepaper to (default: None)')
    parser.add_argument('-l', '--lines', nargs = '?', const = 0.1, type = float, help = 'include one to three random lines in base color with given opacity in range [0, 1] (default: 0.1)')
    parser.add_argument('-lb', '--lines_bright', nargs = '?', const = 0.1, type = float, help = 'include one to three bright random lines with given opacity in range [0, 1] (default: 0.1)')
    parser.add_argument('-ld', '--lines_dark', nargs = '?', const = 0.1, type = float, help = 'include one to three dark random lines with given opacity in range [0, 1] (default: 0.1)')
    parser.add_argument('-P', '--pixelate', help = "pixelate image (e.g. 42x42)")
    parser.add_argument('-e', '--emblem', help = 'emblem to add in the center of the huepaper')
    parser.add_argument('-hue', default = 0.1, type = float, help = 'maximum hue to differ from given color in range [0, 1] (default: 0.1)')
    parser.add_argument('-smin', default = 0.2, type = float, help = 'minimum satisfaction for colors in range [0, 1] (default: 0.2)')
    parser.add_argument('-smax', default = 1.0, type = float, help = 'maximum satisfaction for colors in range [0, 1] (default: 1.0)')
    parser.add_argument('-lmin', default = 0.2, type = float, help = 'minimum luminance for colors in range [0, 1] (default: 0.2)')
    parser.add_argument('-lmax', default = 0.9, type = float, help = 'maximum luminance for colors in range [0, 1] (default: 0.9)')

    # Get args
    args = parser.parse_args()
    width = args.width
    height = args.height
    color = args.color
    preview = args.preview
    output = args.output
    lines = args.lines
    lines_bright = args.lines_bright
    lines_dark = args.lines_dark
    emblem = args.emblem
    pixelate = args.pixelate
    max_hue = args.hue
    sat_min = args.smin
    sat_max = args.smax
    lum_min = args.lmin
    lum_max = args.lmax

    # Check preconditions
    if not preview and not output:
        parser.error('You must either set -p (--preview) or -o (--output)')
    if pixelate:
        try:
            values = pixelate.split('x')
            px = int(values[0])
            py = int(values[1])
        except:
            parser.error('Pixelation value must be set in form: 42x42')

    # Main routine
    print_logo()
    base_color = get_base_color(color)
    c1, c2, c3, c4 = create_colors(base_color)
    image = create_base_image(c1, c2, c3, c4)

    if lines:
        image = add_lines(image, base_color.rgb + (lines,))
    if lines_bright:
        image = add_lines(image, (1.0, 1.0, 1.0, lines_bright))
    if lines_dark:
        image = add_lines(image, (0.0, 0.0, 0.0, lines_dark))

    if pixelate:
        image = add_pixelation(image, px, py)
        
    if emblem:
        image = add_emblem(image, emblem)

    if preview:
        image.show()
        if not output:
            save = input('Do you want to save the image? [y/N] ')
            if save == 'y' or save == 'Y':
                path = input('Enter the path where the wallpaper shall be saved: ')
                save_image(path, image)

    if output:
        save_image(output, image)
       

if __name__ == '__main__':
    main()
