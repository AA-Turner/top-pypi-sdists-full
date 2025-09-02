from uiutil import BaseFrame, standalone, RadioButton
from uiutil.tk_names import HORIZONTAL


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(layout=HORIZONTAL,
                                      **kwargs)

        RadioButton(text="First")

        RadioButton(text="Second")

        RadioButton(text="Third")


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
