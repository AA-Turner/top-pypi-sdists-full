from uiutil import BaseFrame, standalone, Switch


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.switch = Switch(text="Choose")


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
