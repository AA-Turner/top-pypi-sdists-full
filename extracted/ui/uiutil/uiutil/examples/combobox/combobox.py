from uiutil import BaseFrame, standalone, Combobox, Position, Label


class MyFrame(BaseFrame):

    VALUES = ["First",
              "Second",
              "Third",
              "Fourth",
              "Fifth",
              "Sixth",
              "Seventh"]

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.cb1 = Combobox(values=self.VALUES,
                            sort=False,
                            trace=self.selection)

        self.cb2 = Combobox(values=self.VALUES,
                            sort=True,
                            row=Position.NEXT,
                            trace=self.selection)

        self.cb3 = Combobox(values=self.VALUES,
                            value=self.VALUES[1],
                            sort=Combobox.sorted_except_first_value,
                            row=Position.NEXT,
                            trace=self.selection)

        self.label = Label(row=Position.NEXT,
                           value="?")
        self.selection()

    def selection(self):
        try:
            comboboxes = (self.cb1, self.cb2, self.cb3)
        except AttributeError:
            return  # Widgets not initialised
        self.label.value = (u'\n'.join(['combobox {n}: {v}; [{i}]'
                                        .format(n=n+1,
                                                v=cb.value,
                                                i=cb.current())
                                        for n, cb in enumerate(comboboxes)]))

standalone(frame=MyFrame)
