import board
import displayio, digitalio, busio
from adafruit_st7735r import ST7735R

# To show return tooltips for functions
class Any:pass
class pin_number:pass
class digitalio__digital_in_out:pass
class busio__spi:pass
class displayio__display_bus:pass
class st7735r:pass
class displayio__group:pass
class displayio__bitmap:pass
class displayio__palette:pass
class displayio__sprite:pass

# Reset all pins to allow new connections
displayio.release_displays()

class Display:
    def __init__(self,
                 backlight_pin: pin_number = board.GP17,
                 clock_pin: pin_number = board.GP18,
                 MOSI_pin: pin_number = board.GP19,
                 MISO_pin: pin_number = board.GP16,
                 cs_pin: pin_number = board.GP20,
                 dc_pin: pin_number = board.GP22,
                 reset_pin: pin_number = board.GP26,
                 screen_width: int = 160,
                 screen_height: int = 128,
                 rotation: int = 270,
                 bgr: bool = True,
                 auto_refresh: bool = True) -> None:
        # Store inputs for future use if needed
        self.backlight_pin = backlight_pin
        self.clock_pin = clock_pin
        self.MOSI_pin = MOSI_pin
        self.MISO_pin = MISO_pin
        self.cs_pin = cs_pin
        self.dc_pin = dc_pin
        self.reset_pin = reset_pin
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rotation = rotation
        self.bgr = bgr
        self.auto_refresh = auto_refresh

        # Create display device
        self.backlight = self.startBacklight(backlight_pin)
        self.spi = self.createSPI(clock_pin, MOSI_pin, MISO_pin)
        self.display_bus = self.createDisplayBus(self.spi, cs_pin, dc_pin, reset_pin)
        self.display = self.initDisplay(screen_width, screen_height, rotation, bgr, auto_refresh)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.display

    # Turn on backlight as it doesn't turn on automatically
    def startBacklight(self,
                       backlight_pin: pin_number) -> digitalio__digital_in_out:
        backlight = digitalio.DigitalInOut(backlight_pin)
        backlight.direction = digitalio.Direction.OUTPUT
        backlight.value = True
        return backlight

    def createSPI(self,
                  clock: pin_number,
                  mosi: pin_number,
                  miso: pin_number) -> busio__spi:
        spi = busio.SPI(clock=clock, MOSI=mosi, MISO=miso)

        return spi

    def createDisplayBus(self,
                         spi: busio__spi,
                         cs_pin: pin_number,
                         dc_pin: pin_number,
                         reset_pin: pin_number) -> displayio__display_bus:
        display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

        return display_bus

    def initDisplay(self,
                    width: int,
                    height: int,
                    rotation: int,
                    bgr: bool,
                    auto_refresh: bool) -> st7735r:
        display = ST7735R(self.display_bus, width=width, height=height, rotation=rotation, bgr=bgr)
        display.auto_refresh = auto_refresh

        return display

    def showDisplayGroup(self,
                         group: displayio__group) -> None:
        self.display.show(group)

    def showSprite(self,
                   group: displayio__group,
                   sprite: displayio__sprite) -> None:
        group.append(sprite)


# Releases displays to create new ones if needed
def releaseDisplays():
    # Reset all pins to allow new connections
    displayio.release_displays()

def createDisplayGroup(x: int = 0,
                       y: int = 0,
                       scale: int = 1) -> displayio__group:
    group = displayio.Group(x=x, y=y, scale=scale)

    return group

def createBitmap(width: int,
                 height: int,
                 value_count: int = 1) -> displayio__bitmap:
    bitmap = displayio.Bitmap(width, height, value_count)

    return bitmap

# Need to use convertRGBToHex function before passing a colour into here
def createColourPalette(colours: int) -> displayio__palette:
    colour_palette = displayio.Palette(len(colours))

    for i in range(len(colours)):
        colour_palette[i] = colours[i]

    return colour_palette

def createSprite(bitmap: displayio__bitmap,
                 pixel_shader: displayio__palette,
                 x: int = 0,
                 y: int = 0) -> displayio__sprite:
    sprite = displayio.TileGrid(bitmap, pixel_shader=pixel_shader, x=x, y=y)

    return sprite
