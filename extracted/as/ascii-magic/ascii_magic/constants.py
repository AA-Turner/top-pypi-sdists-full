import PIL
from PIL import Image

import warnings
from enum import Enum


class Front(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39
    LIGHTBLACK = 90
    LIGHTRED = 91
    LIGHTGREEN = 92
    LIGHTYELLOW = 93
    LIGHTBLUE = 94
    LIGHTMAGENTA = 95
    LIGHTCYAN = 96
    LIGHTWHITE = 97


class Back(Enum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49
    LIGHTBLACK = 100
    LIGHTRED = 101
    LIGHTGREEN = 102
    LIGHTYELLOW = 103
    LIGHTBLUE = 104
    LIGHTMAGENTA = 105
    LIGHTCYAN = 106
    LIGHTWHITE = 107


class Modes(Enum):
    ASCII = 'ASCII'
    TERMINAL = 'TERMINAL'
    OBJECT = 'OBJECT'

    HTML = 'HTML'
    HTML_MONOCHROME = 'HTML_MONOCHROME'
    HTML_TERMINAL = 'HTML_TERMINAL'
    HTML_FULL_COLOR = 'HTML_FULL_COLOR'


PALETTE = [
    ((0, 0, 0), Front.LIGHTBLACK, '#222'),
    ((0, 0, 1), Front.BLUE, '#00F'),
    ((0, 1, 0), Front.GREEN, '#0F0'),
    ((1, 0, 0), Front.RED, '#F00'),
    ((1, 1, 1), Front.WHITE, '#FFF'),
    ((1, 0, 1), Front.MAGENTA, '#F0F'),
    ((0, 1, 1), Front.CYAN, '#0FF'),
    ((1, 1, 0), Front.YELLOW, '#FF0'),
]

CHARS_BY_DENSITY = ' .`-_\':,;^=+/"|)\\<>)iv%xclrs{*}I?!][1taeo7zjLunT#JCwfy325Fp6mqSghVd4EgXPGZbYkOA&8U$@KHDBWNMR0QQ'

DEFAULT_STYLES = 'display: inline-block; border-width: 4px 6px; border-color: black; color: white; border-style: solid; background-color:black; font-size: 8px;'

DEFAULT_GEMINI_MODEL = 'gemini-2.5-flash-image'

# Image.Resampling.LANCZOS was added in Pillow 10 replacing Image.LANCZOS
RESAMPLING_METHOD = (
    getattr(getattr(Image, 'Resampling'), 'LANCZOS') or
    getattr(Image, 'LANCZOS') or
    1
)

# PIL.__version__ was added in Pillow 5.2
# PIL.PILLOW_VERSION was removed in Pillow 9
# PIL.VERSION was removed in Pillow 6
PILLOW_VERSION = (
    getattr(PIL, '__version__') or
    getattr(PIL, 'PILLOW_VERSION') or
    getattr(PIL, 'VERSION') or
    '0'
)
if PILLOW_VERSION == '0':
    warnings.warn('Could not determine Pillow version')
