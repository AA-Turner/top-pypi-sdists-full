# encoding: utf-8

import sys
from uiutil.tk_names import Tk

from ._base import BaseWindow
from ..mixin.menubar import MenuBarMixIn


class RootWindow(BaseWindow,
                 MenuBarMixIn,
                 Tk):

    def __init__(self,
                 menu=True,
                 *args,
                 **kwargs):

        if sys.version_info.major == 2:
            Tk.__init__(self)
        super(RootWindow, self).__init__(*args, **kwargs)
        if menu:
            self.enable_menubar()
        self.make_active_application()

        self.mainloop()


class Standalone(RootWindow):

    def __init__(self,
                 frame,
                 title=None,
                 **kwargs):
        self.frame = frame
        self._title = title
        menu = kwargs.pop('menu', True)
        self.frame_kwargs = kwargs
        super(Standalone, self).__init__(menu=menu,
                                         **kwargs)

    def _draw_widgets(self):
        self.title(self._title
                   if self._title is not None
                   else u"Standalone {frame}".format(frame=self.frame.__name__))
        self.frame = self.frame(**self.frame_kwargs)


def standalone(frame,
               title=None,
               **kwargs):
    Standalone(frame=frame,
               title=title,
               **kwargs)
