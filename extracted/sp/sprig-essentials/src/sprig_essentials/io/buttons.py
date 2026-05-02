import board
import displayio, digitalio

# To show return tooltips for functions
class Any:pass
class pin_number:pass
class digitalio__digital_in_out:pass

# Reset all pins to allow new connections
displayio.release_displays()

class Button:
    def __init__(self,
                 button_pin: pin_number = None,
                 quick_start: bool = False) -> None:
        # Store inputs for future use if needed
        self.quick_start = quick_start

        if quick_start:
            self.w, self.a, self.s, self.d, self.i, self.j, self.k, self.l = self.quickStartButtons()

            # Intial button states
            # button order:                  w      a      s      d      i      j      k      l
            self.quick_btns_prev_states = [False, False, False, False, False, False, False, False]
            self.quick_btns_cur_states = [False, False, False, False, False, False, False, False]
        elif button_pin != None:
            self.button_pin = button_pin
            self.button = self.createButton(button_pin)

            # Intial button states
            self.prev_state = False
            self.cur_state = False

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.quick_start:
            return self.w, self.a, self.s, self.d, self.i, self.j, self.k, self.l
        else:
            return self.button

    # Create a button
    def createButton(self,
                     btn_pin: pin_number) -> digitalio__digital_in_out:
        button = digitalio.DigitalInOut(btn_pin)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP

        return button

    # Automates buttons creation, assuming you're using a Sprig
    def quickStartButtons(self) -> "tuple[digitalio__digital_in_out]":
        w = digitalio.DigitalInOut(board.GP5)
        w.direction = digitalio.Direction.INPUT
        w.pull = digitalio.Pull.UP

        a = digitalio.DigitalInOut(board.GP6)
        a.direction = digitalio.Direction.INPUT
        a.pull = digitalio.Pull.UP

        s = digitalio.DigitalInOut(board.GP7)
        s.direction = digitalio.Direction.INPUT
        s.pull = digitalio.Pull.UP

        d = digitalio.DigitalInOut(board.GP8)
        d.direction = digitalio.Direction.INPUT
        d.pull = digitalio.Pull.UP

        i = digitalio.DigitalInOut(board.GP12)
        i.direction = digitalio.Direction.INPUT
        i.pull = digitalio.Pull.UP

        j = digitalio.DigitalInOut(board.GP13)
        j.direction = digitalio.Direction.INPUT
        j.pull = digitalio.Pull.UP

        k = digitalio.DigitalInOut(board.GP14)
        k.direction = digitalio.Direction.INPUT
        k.pull = digitalio.Pull.UP

        l = digitalio.DigitalInOut(board.GP15)
        l.direction = digitalio.Direction.INPUT
        l.pull = digitalio.Pull.UP

        return w, a, s, d, i, j, k, l

    # Gets the current state of the button
    # True is pressed, False is released
    def getPressed(self) -> bool | "list[bool]":
        self.updateButton()

        if not self.quick_start:
            return not self.button.value
        else:
            # Return a list of all the buttons that are pressed currently
            return [self.getPressed(self.w), self.getPressed(self.a), self.getPressed(self.s), self.getPressed(self.d),
                    self.getPressed(self.i), self.getPressed(self.j), self.getPressed(self.k), self.getPressed(self.l)]

    # Returns "pressed" if state changes from False to True,
    #         "released" if state changes from True to False,
    #         "no change" if nothing changed
    def getButtonStateChange(self) -> bool | "list[bool]":
        self.updateButton()

        if not self.quick_start:
            if self.prev_state != self.cur_state:
                if self.cur_state:
                    return "pressed"
                else:
                    return "released"
            else:
                return "no change"
        else:
            # Return a list of all the buttons that are pressed currently
            output = []

            for p, c in zip(self.quick_btns_prev_states, self.quick_btns_cur_states):
                if p != c:
                    if c:
                        output.append("pressed")
                    else:
                        output.append("released")
                else:
                    output.append("no change")

            return output

    # Update the current and previous state of the button
    def updateButton(self) -> None:
        if self.quick_start:
            self.quick_btns_prev_states = self.quick_btns_cur_states.copy()
            self.quick_btns_cur_states = self.getPressed()
        else:
            self.prev_state = self.cur_state
            self.prev_state = self.getPressed()

    def resetButtonStates(self) -> None:
        if self.quick_start:
            self.quick_btns_cur_states = [False, False, False, False, False, False, False, False]
            self.quick_btns_prev_states = [False, False, False, False, False, False, False, False]
        else:
            self.cur_state = False
            self.prev_state = False
