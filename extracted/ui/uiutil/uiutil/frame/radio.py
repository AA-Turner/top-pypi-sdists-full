# encoding: utf-8

from tkinter import NORMAL, DISABLED, EW
from collections import OrderedDict

from .label import BaseLabelFrame


class BaseRadioFrame(BaseLabelFrame):

    BUTTON = u'button'
    TEXT = u'text'

    def __init__(self,
                 title,
                 options,
                 *args,
                 **kwargs):

        """

        :param title:
        :param options: A list of option names or, if the option objects
                        and labels are different, a dictionary:

                             {<option object>: "option label",
                              ...
                              <option object>: "option label"}
        :param width:
        :param args:
        :param kwargs:
        """

        logging.warning(u'BaseRadioFrame is deprecated. Use the RadioBox widget instead')

        super(BaseRadioFrame, self).__init__(*args, **kwargs)

        self._set_title(title=title)

        self.selected = self.string_var(value=options[0])  # Sets default option to the first in the unsorted list

        if not isinstance(options, dict):
            options = {opt: opt for opt in options}

        self.options = OrderedDict(sorted({opt: {self.TEXT: options[opt]} for opt in options}.items(),
                                          key=lambda t: t[0]))

        for opt_object, opt in iter(self.options.items()):
            opt[self.BUTTON] = self.radiobutton(text=opt[self.TEXT],
                                                variable=self.selected,
                                                value=opt[self.TEXT],
                                                state=NORMAL,
                                                command=(lambda opt=opt_object: self.state_change(opt)),
                                                row=self.row.next(),
                                                column=self.column.start(),
                                                sticky=EW)

    def enable_all(self):
        for opt in self.options.values():
            opt[self.BUTTON].config(state=NORMAL)

    def disable_all(self):
        for opt in self.options.values():
            opt[self.BUTTON].config(state=DISABLED)

    def state_change(self,
                     opt):
        u"""
        Override this method to take action when a
        new option is selected.
        """
        pass
