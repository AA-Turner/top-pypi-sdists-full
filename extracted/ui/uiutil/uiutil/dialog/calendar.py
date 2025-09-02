# encoding: utf-8

from .. import ChildWindow, BaseFrame, Button, Position
from ..tk_names import NSEW, EW
from ..ttk_override.ttk_calendar import Calendar

# Source: https://github.com/moshekaplan/tkinter_components/tree/master/CalendarDialog


class CalendarDialog(ChildWindow):
    """Dialog box that displays a calendar and returns the selected date"""

    def __init__(self,
                 *args,
                 **kwargs):

        self.result = None

        super(CalendarDialog, self).__init__(*args,
                                             **kwargs)

    def _draw_widgets(self):
        self.calendar = Calendar(self._main_frame)
        self.calendar.grid(sticky=NSEW)

        box = BaseFrame(parent=self._main_frame,
                        row=Position.NEXT,
                        column=Position.START,
                        sticky=NSEW)

        Button(frame=box,
               text=u'OK',
               command=self.ok,
               column=Position.START,
               sticky=EW)

        Button(frame=box,
               text=u'Cancel',
               command=self.cancel,
               column=Position.NEXT,
               sticky=EW)

        box.nice_grid()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def ok(self,
           _=None):
        self.result = self.calendar.selection
        self.exit()

    def cancel(self,
               _=None):
        self.exit()
