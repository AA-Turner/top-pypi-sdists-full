from uiutil import BaseFrame, standalone, Label


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)
        Label(text="Hello")


standalone(frame=MyFrame,
           title="Welcome to UI Util app",
           width=350,
           height=200)

