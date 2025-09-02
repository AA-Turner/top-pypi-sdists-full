# encoding: utf-8

from collections import OrderedDict
from uiutil import BaseFrame, standalone, Combobox, Position, Label


class MyFrame(BaseFrame):

    FIRST = [1]
    SECOND = [2]
    THIRD = 3,
    FOURTH = "4th"
    FIFTH = [1, 2, 3, 4, 5]
    SIXTH = [666666]
    SEVENTH = "G"

    VALUES = OrderedDict([("First",   FIRST),
                          ("Second",  SECOND),
                          ("Third",   THIRD),
                          ("Fourth",  FOURTH),
                          ("Fifth",   FIFTH),
                          ("Sixth",   SIXTH),])

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
                            value="Sixth",
                            sort=Combobox.sorted_except_first_value,
                            row=Position.NEXT,
                            trace=self.selection,
                            )

        self.label = Label(row=Position.NEXT,
                           value="?")
        self.selection()

    def selection(self):
        try:
            cb1 = self.cb1.value
            cb2 = self.cb2.value
            cb3 = self.cb3.value
        except AttributeError:
            return  # Widgets not initialised
        self.label.value = ('combobox 1: {cb1}\n'
                            'combobox 2: {cb2}\n'
                            'combobox 3: {cb3}\n'
                            .format(cb1=cb1,
                                    cb2=cb2,
                                    cb3=cb3))
        if self.cb3.value == self.FIFTH:
            self.cb3.value = ("Seventh", self.SEVENTH)


standalone(frame=MyFrame)
