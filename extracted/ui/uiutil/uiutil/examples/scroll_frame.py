# encoding: utf-8

from tkinter import ttk
from tkinter.constants import NORMAL

from uiutil.frame.scroll import BaseScrollFrame
from uiutil.frame.frame import BaseFrame
from uiutil.window.root import RootWindow


class ExampleScrollWindow(RootWindow):

    def __init__(self, *args, **kwargs):
        super(ExampleScrollWindow, self).__init__(*args, **kwargs)

    def _draw_widgets(self):

        self.base = BaseScrollFrame(self._main_frame,
                                    column=0,
                                    row=0)
        self.base.grid(sticky=u'nsew')

        # Add data to usable frame
        for i in range(40):
            ttk.Label(self.base, text=i).grid(row=i, column=0)
            ttk.Label(self.base, text="my text" + str(i)).grid(row=i, column=1)
            ttk.Label(self.base, text="...................................."
                                      ".....................................").grid(row=i, column=2)

        self.base1 = BaseScrollFrame(self._main_frame,
                                     column=1,
                                     row=0)
        self.base1.grid(sticky=u'nsew')

        # Add data to usable frame
        for i in range(15):
            ttk.Label(self.base1, text=i).grid(row=i, column=0)
            ttk.Label(self.base1, text="my text" + str(i)).grid(row=i, column=1)
            ttk.Label(self.base1, text="...................................."
                                       ".....................................").grid(row=i, column=2)

        self.base2 = BaseFrame(self._main_frame,
                               column=0,
                               row=1)
        self.base2.grid(sticky=u'sew')

        self.button = ttk.Button(self.base2,
                                 state=NORMAL,
                                 text=u'Button 1',
                                 width=15, )
        self.button.grid(row=self.base2.row.next(),
                         column=self.base2.column.start())

        self.button2 = ttk.Button(self.base2,
                                  state=NORMAL,
                                  text=u'Button 2',
                                  width=15, )
        self.button2.grid(row=self.base2.row.current,
                          column=self.base2.column.next())

        self._main_frame.nice_grid(rows=False)
        self._main_frame.rowconfigure(0, weight=1)
        self.nice_grid()


if __name__ == u'__main__':
    ExampleScrollWindow()
