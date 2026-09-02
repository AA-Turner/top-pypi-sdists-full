from uiutil import BaseFrame, standalone, Label, Position, IntRadioButton


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.radio = IntRadioButton(text="First",
                                    value=1,
                                    command=self.set_label)

        IntRadioButton(text="Second",
                       value=2,
                       column=Position.NEXT)

        IntRadioButton(text="Third",
                       value=3,
                       column=Position.NEXT)

        self.label = Label(row=Position.NEXT,
                           column=Position.START,
                           columnspan=3,
                           value="?")
        self.radio.value = 2
        self.set_label()

    def set_label(self):
        self.label.value = "{value} selected".format(value=self.radio.value)


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
