from uiutil import BaseFrame, standalone, RadioBox, Label, Position


class MyFrame(BaseFrame):
    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.radiobox = RadioBox(title="Pick One",
                                 options={"First":  {"some key": "some value"},
                                          "Second": 2,
                                          "Third":  "3rd"},
                                 command=self.set_label)

        self.label = Label(row=Position.NEXT,
                           value="")
        self.set_label()

    def set_label(self):
        self.label.value = ("Selected: {selected}\n"
                            "Value: {value}\n"
                            "Type: {typename}"
                            .format(selected=self.radiobox.selected,
                                    value=self.radiobox.value,
                                    typename=self.radiobox.value.__class__))


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
