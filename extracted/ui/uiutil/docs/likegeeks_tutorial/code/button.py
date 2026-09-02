from uiutil import BaseFrame, standalone, Label, Button, Position


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)
        Label(text="Hello")

        Button(text="Click Me",
               column=Position.NEXT)


standalone(frame=MyFrame,
           title="Welcome to UI Util app")

