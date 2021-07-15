#!/usr/bin/env python

from huepaper import (
    get_base_color,
    create_colors,
    create_base_image,
    add_lines,
    add_pixelation,
    add_emblem,
    save_image,
)
import argparse


def print_greeter():
    greeter = """
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
"""
    print(greeter)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create wallpapers based on color hues."
    )
    parser.add_argument(
        "-s",
        "--size",
        default="1920x1080",
        help="size of huepaper in the form WIDTHxHEIGHT (default: 1920x1080)",
    )
    parser.add_argument(
        "-c",
        "--color",
        help="base color from which the huepaper is generated (default: random color)",
    )
    parser.add_argument(
        "-np", "--no-preview", action="store_true", help="don't preview the huepaper"
    )
    parser.add_argument(
        "-o", "--output", help="filepath where the huepaper will be saved"
    )
    parser.add_argument(
        "-l",
        "--lines",
        nargs="?",
        const=0.3,
        type=float,
        help="include one to three random lines in base color with given opacity in range [0, 1] (default: 0.3)",
    )
    parser.add_argument(
        "-lb",
        "--lines_bright",
        nargs="?",
        const=0.1,
        type=float,
        help="include one to three bright random lines with given opacity in range [0, 1] (default: 0.1)",
    )
    parser.add_argument(
        "-ld",
        "--lines_dark",
        nargs="?",
        const=0.1,
        type=float,
        help="include one to three dark random lines with given opacity in range [0, 1] (default: 0.1)",
    )
    parser.add_argument(
        "-P",
        "--pixelate",
        nargs="?",
        const="16x9",
        help="pixelate image with WIDTHxHEIGHT (default: 16x9)",
    )
    parser.add_argument(
        "-e", "--emblem", help="emblem to add in the center of the huepaper"
    )
    parser.add_argument(
        "-hue",
        default=0.1,
        type=float,
        help="maximum hue to differ from given color in range [0, 1] (default: 0.1)",
    )
    parser.add_argument(
        "-smin",
        default=0.2,
        type=float,
        help="minimum satisfaction for colors in range [0, 1] (default: 0.2)",
    )
    parser.add_argument(
        "-smax",
        default=1.0,
        type=float,
        help="maximum satisfaction for colors in range [0, 1] (default: 1.0)",
    )
    parser.add_argument(
        "-lmin",
        default=0.2,
        type=float,
        help="minimum luminance for colors in range [0, 1] (default: 0.2)",
    )
    parser.add_argument(
        "-lmax",
        default=0.9,
        type=float,
        help="maximum luminance for colors in range [0, 1] (default: 0.9)",
    )

    # Get args
    args = parser.parse_args()
    size = args.size
    color = args.color
    no_preview = args.no_preview
    output = args.output
    lines = args.lines
    lines_bright = args.lines_bright
    lines_dark = args.lines_dark
    emblem = args.emblem
    pixelate = args.pixelate
    hue_max = args.hue
    sat_min = args.smin
    sat_max = args.smax
    lum_min = args.lmin
    lum_max = args.lmax

    # Get size
    try:
        values = size.split("x")
        width = int(values[0])
        height = int(values[1])
    except:
        parser.error("The size must be given in form: 1920x1080")

    # Check preconditions
    if no_preview and not output:
        parser.error("You must either omit -np (--no-preview) or set -o (--output)")
    if pixelate:
        try:
            values = pixelate.split("x")
            px = int(values[0])
            py = int(values[1])
        except:
            parser.error("Pixelation value must be set in form: 42x42")

    print_greeter()
    base_color = get_base_color(color, sat_min, sat_max, lum_min, lum_max)
    c1, c2, c3, c4 = create_colors(
        base_color, hue_max, sat_min, sat_max, lum_min, lum_max
    )
    image = create_base_image(c1, c2, c3, c4, width, height)

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

    image.mode = "RGB"

    if not no_preview:
        image.show()
        if not output:
            save = input("Do you want to save the image? [y/N] ")
            if save == "y" or save == "Y":
                path = input("Enter the path where the wallpaper shall be saved: ")
                save_image(image, path)

    if output:
        save_image(image, output)
