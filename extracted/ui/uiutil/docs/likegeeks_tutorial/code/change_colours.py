from uiutil import BaseFrame, standalone, Label, Button, Position


class MyFrame(BaseFrame):

    ORANGE_RED_BUTTON = "OrangeRedButton.TButton"

    STYLES = {ORANGE_RED_BUTTON: dict(foreground="red",
                                      background="orange")}

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        Label(text="Hello")

        Button(text="Click Me",
               column=Position.NEXT,
               style=self.ORANGE_RED_BUTTON)


standalone(frame=MyFrame,
           title="Welcome to UI Util app")

