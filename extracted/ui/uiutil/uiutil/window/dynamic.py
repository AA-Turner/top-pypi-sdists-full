# encoding: utf-8

from .root import RootWindow
from .child import ChildWindow
from ..frame.dynamic import DynamicFrame
from configurationutil import Configuration


class _DynamicWindow(object):

    def __init__(self,
                 layout_key,
                 window_title=u'Config Window',
                 item_dict=None,
                 *args,
                 **kwargs):

        self.cfg = Configuration()

        self.key = layout_key
        self.window_title = window_title
        self.item_dict = item_dict

        super(_DynamicWindow, self).__init__(*args, **kwargs)

    def _draw_widgets(self):
        self.title(self.window_title)
        self.dynamic_frame = self.add_frame(frame=DynamicFrame,
                                            parent=self._main_frame,
                                            layout_key=self.key,
                                            item_dict=self.item_dict)


class DynamicRootWindow(_DynamicWindow, RootWindow):

    def __init__(self, *args, **kwargs):
        super(DynamicRootWindow, self).__init__(*args, **kwargs)


class DynamicChildWindow(_DynamicWindow, ChildWindow):

    def __init__(self, *args, **kwargs):
        super(DynamicChildWindow, self).__init__(*args, **kwargs)
