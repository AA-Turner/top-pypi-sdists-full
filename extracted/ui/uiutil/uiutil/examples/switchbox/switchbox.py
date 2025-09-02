from uiutil import BaseFrame, standalone, SwitchBox, Position
from collections import OrderedDict


class MyFrame(BaseFrame):

    SWITCHES = OrderedDict([("First",   1),
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

        self.sb1 = SwitchBox(title="Unrestricted (expands downwards)",
                             switches=self.SWITCHES,
                             sort=False)

        self.sb2 = SwitchBox(title="2 col (expands downwards)",
                             switches=self.SWITCHES,
                             sort=False,
                             max_columns=2,
                             column=Position.NEXT)

        self.sb3 = SwitchBox(title="2 row (expands to the right)",
                             switches=self.SWITCHES,
                             sort=False,
                             max_rows=2,
                             row=Position.NEXT,
                             column=Position.START)

        self.sb4 = SwitchBox(title="2x2 sorted (expands downwards)",
                             switches=self.SWITCHES,
                             sort=True,
                             max_rows=2,
                             max_columns=2,
                             column=Position.NEXT)

standalone(frame=MyFrame)
