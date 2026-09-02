from uiutil import BaseFrame, standalone, SwitchBox


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.switch = SwitchBox(title="Three",
                                switches=("First",
                                          "Second",
                                          "Third",
                                          ),
                                switch_states={"First": False},
                                max_rows=1)


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
