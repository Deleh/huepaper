# huepaper - a colorful wallpaper generator

![Logo](./images/logo.png)

**huepaper** creates wallpapers based on color hues. Bring a little
color in your life by randomness, because every huepaper is truly
unique.

You can find [examples](#examples) below.

## Installation

Until now there is no install method, just ways to call the script.

### NixOS

Call `nix-shell` in the project directory. This will drop you into a
python environment with all necessary requirements.

### LegacyOS

Install the python requirements with `pip install -r requirements.txt`.

## Usage

    usage: huepaper.py [-h] [-W WIDTH] [-H HEIGHT] [-c COLOR] [-p] [-o OUTPUT]
    [-l [LINES]] [-lb [LINES_BRIGHT]] [-ld [LINES_DARK]]
    [-P PIXELATE] [-e EMBLEM] [-hue HUE] [-smin SMIN]
    [-smax SMAX] [-lmin LMIN] [-lmax LMAX]
    
    Create wallpapers based on color hues.
    
    optional arguments:
      -h, --help            show this help message and exit
      -W WIDTH, --width WIDTH
                            width of wallpaper (defaul: 1920)
      -H HEIGHT, --height HEIGHT
                            height of wallpaper (default: 1080)
      -c COLOR, --color COLOR
                            color, the wallpaper is generated from (uses a random
                            color if not given)
      -p, --preview         preview wallpaper
      -o OUTPUT, --output OUTPUT
                            file where to save the wallpaper to (default: None)
      -l [LINES], --lines [LINES]
                            include one to three random lines in base color with
                            given opacity in range [0, 1] (default: 0.1)
      -lb [LINES_BRIGHT], --lines_bright [LINES_BRIGHT]
                            include one to three bright random lines with given
                            opacity in range [0, 1] (default: 0.1)
      -ld [LINES_DARK], --lines_dark [LINES_DARK]
                            include one to three dark random lines with given
                            opacity in range [0, 1] (default: 0.1)
      -P PIXELATE, --pixelate PIXELATE
                            pixelate image (e.g. 42x42)
      -e EMBLEM, --emblem EMBLEM
                            emblem to add in the center of the wallpaper
      -hue HUE              maximum hue to differ from given color in range [0, 1]
                            (default: 0.1)
      -smin SMIN            minimum satisfaction for colors in range [0, 1]
                            (default: 0.2)
      -smax SMAX            maximum satisfaction for colors in range [0, 1]
                            (default: 1.0)
      -lmin LMIN            minimum luminance for colors in range [0, 1] (default:
                            0.2)
      -lmax LMAX            maximum luminance for colors in range [0, 1] (default:
                            0.9)

All image operations are called in order of the help file. E.g. pixelate
(`-P`) is called after adding lines (`-l`).

If you set the color via `-c` it is not guaranteed, that it is included
in the huepaper. Colors, similar to the given one are chosen. You can
specify how far the colors differ in the hue range with the `-hue`
parameter. Valid color expressions are e.g. `#F5F5DC`, `#0f0`, `red`.
Make sure, that colors beginning with a `#` are encapsulated in quotes
(`"`). All supported color names can be seen
[here](https://www.w3schools.com/colors/colors_names.asp).

If you use the `-e` argument to specify an emblem, make sure it has the
right size. It is not scaled or stretched, just placed in the center of
the image. If you want an offset, e.g. put it in the left bottom corner,
provide an emblem file with the size of the huepaper, transparent
background and your emblem in the bottom left corner.

## Examples

Please note, that every huepaper call generates a new random image. You
will never get the same huepaper twice. You may like some and dislike
others. Fiddle around with the options to find a result, you are happy
with.

![Huepaper 1](./images/huepaper_1.png)

`huepaper.py -p`

-----

![Huepaper 2](./images/huepaper_2.png)

`huepaper.py -p -c lightgreen`

-----

![Huepaper 3](./images/huepaper_3.png)

`huepaper.py -p -c "#ff7f50" -lb 0.05`

-----

![Huepaper 4](./images/huepaper_4.png)

`huepaper.py -p -hue 1.0 -lmin 0.3 -lmax 0.6 -smin 0.8 -smax 1.0`

-----

![Huepaper 5](./images/huepaper_5.png)

`huepaper.py -p -hue 0.3 -lmin 0.5 -lmax 0.5 -l 0.5 -P 64x36`

-----

![Huepaper 6](./images/huepaper_6.png)

`huepaper.py -p -l -lb -ld -e nixos.png`

## Acknowledgements

Thanks to all the people who created the nice software, this project in
based on.
