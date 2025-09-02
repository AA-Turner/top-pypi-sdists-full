from uiutil import BaseFrame, standalone, TextScroll
from uiutil.tk_names import INSERT


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.text = TextScroll(width=40,
                               height=10)
        self.text.insert(INSERT, "This is a TextScroll widget...........................")


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
