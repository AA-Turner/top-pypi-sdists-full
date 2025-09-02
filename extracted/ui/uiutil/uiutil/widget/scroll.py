# -*- coding: utf-8 -*-

import logging_helper

from uiutil.helper.introspection import calling_base_frame
from uiutil.tk_names import (NONE,
                             RIGHT,
                             Y,
                             HORIZONTAL,
                             BOTTOM,
                             X,
                             LEFT,
                             BOTH,
                             NORMAL,
                             DISABLED,
                             END,
                             Text,
                             Scrollbar,
                             NS,
                             EW,
                             NSEW)
from .base_widget import BaseWidget
from ..frame.frame import BaseFrame
from ..helper.arguments import pop_kwarg, raise_on_positional_args, get_grid_kwargs, get_widget_kwargs

logging = logging_helper.setup_logging()


class TextScroll(BaseWidget):

    """
    TextScroll made of a frame, with optional scroll bars contanining a Text
    object. The Text object methods are available directly, as well as BaseWidget's.
    The other objects (hbar, vbar, containing_frame) can also be accessed,
    e.g. text_scroll_instance.hbar
    """

    WIDGET = Text
    VAR_TYPE = None
    VAR_PARAM = None

    def __init__(self,
                 # frame=None,
                 # vbar=True,
                 # hbar=True,
                 *args,
                 **kwargs):

        raise_on_positional_args(self, args)
        frame = pop_kwarg(kwargs, u'frame')
        vbar = pop_kwarg(kwargs, u'vbar', True)
        hbar = pop_kwarg(kwargs, u'hbar', True)

        frame = calling_base_frame(frame)

        grid_kwargs = get_grid_kwargs(frame=frame,
                                      **kwargs)

        widget_kwargs = get_widget_kwargs(**kwargs)

        # Setup a containing frame
        self.containing_frame = BaseFrame(frame)
        kwarg_upd = {u'wrap': NONE}

        if vbar:
            self.vbar = Scrollbar(self.containing_frame)
            self.vbar.grid(row=1,
                           column=2,
                           sticky=NS,
                           rowspan=2)
            kwarg_upd[u'yscrollcommand'] = self.vbar.set

        if hbar:
            self.hbar = Scrollbar(self.containing_frame, orient=HORIZONTAL)
            self.hbar.grid(row=2,
                           column=1,
                           sticky=EW)
            kwarg_upd[u'xscrollcommand'] = self.hbar.set

        widget_kwargs.update(kwarg_upd)

        super(TextScroll, self).__init__(frame=self.containing_frame,
                                         **widget_kwargs)

        self.widget.grid(row=1,
                         column=1,
                         sticky=NSEW)

        self.containing_frame.columnconfigure(1, weight=1)
        self.containing_frame.rowconfigure(1, weight=1)

        if vbar:
            self.vbar[u'command'] = self.widget.yview

        if hbar:
            self.hbar[u'command'] = self.widget.xview

        self.containing_frame.grid(**grid_kwargs)

    def __str__(self):
        return str(self.containing_frame)

    def append_text(self,
                    text,
                    tags=None):

        if tags is None:
            tags = tuple()

        self.configure(state=NORMAL)

        try:
            self.insert(END, text, tags)

        except Exception as e:
            logging.error(u'Error inserting: [{msg}]'.format(msg=text))
            logging.error(e)

        self.configure(state=DISABLED)

        # Autoscroll to the bottom (shifted for the blank line)
        self.yview(float(self.index("end-1c linestart")) - 1)

    def append(self,
               text,
               tags=None):
        # This is necessary because we can't modify the Text from other threads
        # and we don't want this to be blocking!
        self.containing_frame.after(0, self.append_text, text, tags)

    def clear(self,
              start=1.0,
              end=END):
        self.configure(state=NORMAL)
        self.delete(start, end)
        self.configure(state=DISABLED)
