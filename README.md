# huepaper

**huepaper** creates wallpapers based on color hues.

## Instalation

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

## Acknowledgements

Thanks to all the people who created the nice software, this project in
based on.
