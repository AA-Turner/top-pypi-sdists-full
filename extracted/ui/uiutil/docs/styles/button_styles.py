# encoding: utf-8

import logging_helper
from tkinter.constants import NORMAL, E, FLAT, SUNKEN

from uiutil import Button, BaseFrame, standalone

logging = logging_helper.setup_logging()


RED_BUTTON = u'red.TButton'
AMBER_BUTTON = u'amber.TButton'
GREEN_BUTTON = u'green.TButton'
NORMAL_BUTTON = u'TButton'


def next_style(style):
    if style is RED_BUTTON:
        return AMBER_BUTTON
    elif style is AMBER_BUTTON:
        return GREEN_BUTTON
    elif style is GREEN_BUTTON:
        return RED_BUTTON
    raise ValueError(u'Unknown style:{style}'.format(style=style))


class TheFrame(BaseFrame):

    BUTTON_WIDTH = 20
    BUTTON_ONE = u'Button One'
    BUTTON_TWO = u'Button Two'

    STYLES = {RED_BUTTON: dict(foreground='red'),

              AMBER_BUTTON: dict(relief=SUNKEN,
                                 foreground='orange',
                                 background='yellow'),

              GREEN_BUTTON: dict(relief=FLAT,
                                 foreground='green')}

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self,
                           *args,
                           **kwargs)

        self.widgets = {}

        self.widgets[self.BUTTON_ONE] = Button(state=NORMAL,
                                               value=self.BUTTON_ONE,
                                               width=self.BUTTON_WIDTH,
                                               command=lambda: self.cycle_style(self.BUTTON_ONE),
                                               column=self.column.next(),
                                               style=GREEN_BUTTON,
                                               sticky=E)

        self.widgets[self.BUTTON_TWO] = Button(state=NORMAL,
                                               value=self.BUTTON_TWO,
                                               width=self.BUTTON_WIDTH,
                                               command=lambda: self.cycle_style(self.BUTTON_TWO),
                                               row=self.row.next(),
                                               style=RED_BUTTON,
                                               sticky=E)
        self.widget_style = {self.BUTTON_ONE: GREEN_BUTTON,
                             self.BUTTON_TWO: RED_BUTTON}

    def cycle_style(self,
                    event=None):
        self.widget_style[event] = next_style(self.widget_style[event])
        self.widgets[event].configure(style=self.widget_style[event])


if __name__ == u'__main__':
    standalone(TheFrame)
