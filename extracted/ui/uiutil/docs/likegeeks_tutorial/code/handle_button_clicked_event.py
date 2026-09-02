from uiutil import BaseFrame, standalone, Label, Button
from uiutil.tk_names import HORIZONTAL


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(layout=HORIZONTAL,
                                      **kwargs)

        self.label = Label(value="Hello")

        Button(text="Click Me",
               command=self.clicked)

    def clicked(self):
        self.label.value = "Button was clicked!"


standalone(frame=MyFrame,
           title="Welcome to UI Util app",
           width=350)
