# encoding: utf-8

from ..mixin import FrameMixIn
from ..tk_names import ttk


class BaseFrame(ttk.Frame,
                FrameMixIn):

    FRAME = ttk.Frame

    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):

        self._common_init(parent=parent,
                          *args,
                          **kwargs)
