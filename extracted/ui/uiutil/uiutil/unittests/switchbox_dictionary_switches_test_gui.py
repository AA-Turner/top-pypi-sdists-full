from uiutil import BaseFrame, standalone, Label, Position
from uiutil import NewSwitchBox as SwitchBox
from uiutil.tk_names import CENTER


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.switchbox = SwitchBox(title="Three",
                                   switches={"First": {"some key": "some value"},
                                             "Second": 2,
                                             "Third": "3rd"},
                                   switch_states={"First": False},
                                   max_rows=2,
                                   command=self.clicked)

        self.label = Label(row=Position.NEXT,
                           value="Click a switch\n\n\n",
                           justify=CENTER)

    def clicked(self,
                switch):
        value = self.switchbox.value(switch)
        self.label.value = ("Clicked: {selected}\n"
                            "State: {state}\n"
                            "Value: {value}\n"
                            "Type: {typename}"
                            .format(selected=switch,
                                    value=value,
                                    state=self.switchbox.switch_state(switch),
                                    typename=value.__class__))


standalone(frame=MyFrame,
           title="Welcome to UI Util app",
           width=250,
           height=200)
