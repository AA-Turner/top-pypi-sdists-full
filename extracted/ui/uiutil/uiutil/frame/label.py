# encoding: utf-8

from ..mixin import FrameMixIn
from ..tk_names import ttk


class BaseLabelFrame(ttk.Labelframe,
                     FrameMixIn):

    FRAME = ttk.Labelframe
    TITLE = None

    def __init__(self,
                 parent=None,
                 title=None,
                 *args,
                 **kwargs):

        self._common_init(parent=parent,
                          *args,
                          **kwargs)
        if title:
            self._set_title(title=title)

        elif self.TITLE:
            self._set_title(title=self.TITLE)
