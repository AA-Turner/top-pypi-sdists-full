from uiutil import BaseFrame, standalone, Label


class MyFrame(BaseFrame):
    def __init__(self, **kwargs):
        super(MyFrame, self).__init__(**kwargs)
        Label(text="Hello", font=("Arial Bold", 50))


standalone(frame=MyFrame, title="Welcome to UI Util app")

