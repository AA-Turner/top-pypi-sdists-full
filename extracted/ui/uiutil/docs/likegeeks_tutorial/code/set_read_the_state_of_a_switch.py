from uiutil import BaseFrame, standalone, Switch, Label, Position


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.switch = Switch(text="Choose",
                             trace=self.set_label)

        self.label = Label(row=Position.NEXT,
                           value="?")
        self.set_label()

    def set_label(self):
        self.label.value = ("Switch is on"
                            if self.switch.switched_on
                            else "Switch is off")


standalone(frame=MyFrame,
           title="Welcome to UI Util app")