# encoding: utf-8

from uiutil.frame import BaseFrame
from uiutil import Label, Separator
from uiutil.tk_names import EW


class HeadingsFrame(BaseFrame):

    def __init__(self,
                 headings,
                 font="-weight bold",
                 *args,
                 **kwargs):

        self.headings = []

        kwargs['columnspan'] = len(headings)

        super(HeadingsFrame, self).__init__(*args, **kwargs)

        for index, heading in enumerate(headings):
            # Set up a fake label behind the real label.
            # This is so we can set the width of the fake
            # label in order to match column widths of
            # data rows.
            self.headings.append(Label(text="",
                                       column=index))
            # This is the visible label, which will be
            # centred over the column
            Label(text=heading,
                  font=font,
                  column=index)
        Separator(padx=0)

    def set_width(self,
                  index,
                  width):
        self.headings[index].config(width=width)

    def set_widths(self,
                   widths):
        for index, width in enumerate(widths):
            self.set_width(index=index,
                           width=width)

