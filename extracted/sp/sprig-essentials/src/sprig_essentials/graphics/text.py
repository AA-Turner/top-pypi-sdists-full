import board
import terminalio
from adafruit_display_text import label

class terminalio__font:pass
class label__label:pass

class Text:
    def __init__(self) -> None:
        pass

def createTextSprite(text: str,
                     colour: tuple,
                     x: int = 0,
                     y: int = 0,
                     font: terminalio__font = terminalio.FONT) -> label__label:
    text_area = label.Label(font, text=text, color=colour, x=x, y=y)

    return text_area
