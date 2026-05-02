import board
import digitalio

class pin_number:pass
class digitalio__digital_in_out:pass

class LED:
    def __init__(self,
                 led_pin: pin_number = None,
                 quick_start: bool = False) -> None:
        self.quick_start = quick_start

        if quick_start:
            self.left_led = self.createLED(board.GP28)
            self.right_led = self.createLED(board.GP4)
        elif led_pin != None:
            self.led_pin = led_pin
            self.led = self.createLED(led_pin)

    # Creates an LED object and returns it
    def createLED(self,
                  led_pin: pin_number) -> digitalio__digital_in_out:
        led = digitalio.DigitalInOut(led_pin)
        led.direction = digitalio.Direction.OUTPUT

        return led

    # Turns on the LED
    def on(self) -> None:
        if self.quick_start:
            self.left_led.value = True
            self.right_led.value = True
        else:
            self.led.value = True

    # Turns off the LED
    def off(self) -> None:
        if self.quick_start:
            self.left_led.value = False
            self.right_led.value = False
        else:
            self.led.value = False

    # Toggles the LED
    def toggle(self) -> None:
        if self.quick_start:
            self.left_led.value = not self.left_led.value
            self.right_led.value = not self.right_led.value
        else:
            self.led.value = not self.led.value
