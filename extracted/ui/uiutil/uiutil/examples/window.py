# encoding: utf-8

from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.constants import NSEW, EW, NORMAL

from uiutil.window.root import RootWindow
from uiutil.frame.frame import BaseFrame
from uiutil.frame.scroll import BaseScrollFrame
from uiutil.frame.label import BaseLabelFrame
from uiutil.helper.layout import nice_grid
from uiutil.widget.entry import IntEntry


class ExampleWindow(RootWindow):

    def __init__(self, *args, **kwargs):
        super(ExampleWindow, self).__init__(*args, **kwargs)

    def _draw_widgets(self):

        self.base = BaseFrame(self._main_frame,
                              column=0,
                              row=0)
        self.base.grid(sticky=EW)

        showinfo(u"Test",
                 u"Some information...",
                 icon=u'warning',
                 parent=self.base)

        self.button = ttk.Button(self.base,
                                 state=NORMAL,
                                 text=u'Button 1',
                                 width=15, )

        self.button.grid(row=self.base.row.start(),
                         column=self.base.column.start())

        self.button2 = ttk.Button(self.base,
                                  state=NORMAL,
                                  text=u'Button 2',
                                  width=15)
        self.button2.grid(row=self.base.row.current,
                          column=self.base.column.next())

        nice_grid(self.base)

        self.base1 = BaseLabelFrame(self._main_frame,
                                    column=0,
                                    row=1)
        self.base1.grid(sticky=EW)

        self.button = ttk.Button(self.base1,
                                 state=NORMAL,
                                 text=u'Button 3',
                                 width=15)

        self.button.grid(row=self.base1.row.start(),
                         column=self.base1.column.start())

        self.button2 = ttk.Button(self.base1,
                                  state=NORMAL,
                                  text=u'Button 4',
                                  width=15)

        self.button2.grid(row=self.base1.row.current,
                          column=self.base1.column.next())

        nice_grid(self.base1)

        self.base2 = BaseFrame(self._main_frame,
                               column=0,
                               row=2)

        self.base2.grid(sticky=NSEW)

        self.base2canvas = BaseScrollFrame(self.base2)
        self.base2canvas.grid(sticky=NSEW)

        for row in range(100):
            ttk.Label(self.base2canvas,
                      text=u"%s" % row,
                      width=3,
                      borderwidth=u"1",
                      relief=u"solid",
                      style = u"Blue.TLabel").grid(row=row, column=0)
            t = u"this is the second column for row %s... Text, " \
                u"More text and even more text!" % row
            ttk.Label(self.base2canvas,
                      text=t,
                      style = u"Blue.TLabel").grid(row=row, column=1)

        IntEntry(frame=self.base2,
                 row=self.base.row.next(),
                 min=-128,
                 max=127)

        IntEntry(frame=self.base2,
                 row=self.base.row.next(),
                 min=0,
                 max=999)

        nice_grid(self._main_frame)


if __name__ == u'__main__':
    ExampleWindow(width=400, height=350)
    # print query_dialog_with_options(title=u'Query',
    #                                 prompt=u'Question?',
    #                                 values=[u'V1', u'V2'])
