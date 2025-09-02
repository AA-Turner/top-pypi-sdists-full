from uiutil import BaseFrame, standalone, RadioBox, Position
from collections import OrderedDict


class MyFrame(BaseFrame):

    OPTIONS = OrderedDict([("First",   1),
                           ("Second",  2),
                           ("Third",   3),
                           ("Fourth",  4),
                           ("Fifth",   5),
                           ("Sixth",   6),
                           ("Seventh", 7),
                           ])

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.rb1 = RadioBox(title="Unrestricted (expands downwards)",
                            options=self.OPTIONS,
                            sort=False)

        self.rb2 = RadioBox(title="2 col (expands downwards)",
                            options=self.OPTIONS,
                            sort=False,
                            max_columns=2,
                            column=Position.NEXT)

        self.rb3 = RadioBox(title="2 row (expands to the right)",
                            options=self.OPTIONS,
                            sort=False,
                            max_rows=2,
                            row=Position.NEXT,
                            column=Position.START)

        self.rb4 = RadioBox(title="2x2 sorted (expands downwards)",
                            options=self.OPTIONS,
                            sort=True,
                            max_rows=2,
                            max_columns=2,
                            column=Position.NEXT)

standalone(frame=MyFrame)
