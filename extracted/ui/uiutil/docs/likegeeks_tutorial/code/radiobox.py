from uiutil import BaseFrame, standalone, RadioBox, Label, Position


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.radiobox = RadioBox(title="Pick One",
                                 options=("First", "Second", "Third"),
                                 command=self.set_label,
                                 max_rows=1)

        self.label = Label(row=Position.NEXT,
                           value="")
        self.set_label()

    def set_label(self):
        self.label.value = ("Selected : {selected}"
                            .format(selected=self.radiobox.selected))


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
