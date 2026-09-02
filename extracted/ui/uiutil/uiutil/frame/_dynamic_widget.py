# encoding: utf-8

from .frame import BaseFrame
from ._dynamic_base import DynamicBaseFrame


class DynamicWidgetFrame(DynamicBaseFrame,
                         BaseFrame):

    def __init__(self,
                 key,
                 *args,
                 **kwargs):

        self.key = key

        BaseFrame.__init__(self, *args, **kwargs)
        super(DynamicWidgetFrame, self).__init__(*args, **kwargs)
