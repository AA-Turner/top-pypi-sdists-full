
import time
from uiutil import BaseFrame, Button, Label, standalone, Position, Separator
from uiutil.tk_names import HORIZONTAL, NSEW, EW


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
        Separator()

    def set_width(self,
                  index,
                  width):
        self.headings[index].config(width=width)

    def set_widths(self,
                   widths):
        for index, width in enumerate(widths):
            self.set_width(index=index,
                           width=width)


class AdhocFrame(BaseFrame):
    AUTO_POSITION = HORIZONTAL
    STYLES = {BLUE_TEXT_RADIO_BUTTON: BLUE_TEXT,
              BLUE_TEXT_BUTTON: BLUE_TEXT,
              BLUE_TEXT_LABEL: BLUE_TEXT,
              }
    HEADINGS = ['Scenario',
                'Description']


    def __init__(self,
                 *args,
                 **kwargs):
        super(AdhocFrame, self).__init__(*args, **kwargs)

        self.width = 50

        self.headings = HeadingsFrame(headings=self.HEADINGS,
                                      sticky=EW,
                                      padx=0)

        self.b_widen = Button(text=u'Widen',
                              command=self.widen,
                              row=Position.NEXT,
                              )

        self.b_narrow = Button(text=u'Narrow',
                               command=self.narrow,
                               )
        self.set_widths()

    def set_widths(self):
        self.b_widen.config(width=self.width)
        self.b_narrow.config(width=self.width*2)
        self.headings.set_widths([self.width, self.width*2])

    def widen(self):
        if self.width < 100:
            self.width += 10
            self.set_widths()

    def narrow(self):
        if self.width > 10:
            self.width -= 10
            self.set_widths()


standalone(AdhocFrame,
           sticky=NSEW)
