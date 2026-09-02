# encoding: utf-8

import sys
from uiutil.tk_names import Toplevel
from ._base import BaseWindow


class ChildWindow(BaseWindow,
                  Toplevel):

    def __init__(self,
                 *args,
                 **kwargs):
        if sys.version_info.major == 2:
            Toplevel.__init__(self)
        super(ChildWindow, self).__init__(*args, **kwargs)
        self.make_active_window()
