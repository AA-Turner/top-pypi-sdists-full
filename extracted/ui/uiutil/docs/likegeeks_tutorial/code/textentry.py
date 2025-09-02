from uiutil import BaseFrame, standalone, Label, Button, TextEntry
from uiutil.tk_names import HORIZONTAL


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(layout=HORIZONTAL,
                                      **kwargs)

        self.label = Label(value="Hello")

        self.text = TextEntry()

        Button(text="Click Me")


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
