# encoding: utf-8

from .scroll import BaseScrollFrame
from ._dynamic_base import DynamicBaseFrame


class DynamicScrollFrame(DynamicBaseFrame,
                         BaseScrollFrame):

    def __init__(self,
                 key,
                 *args,
                 **kwargs):

        self.key = key

        BaseScrollFrame.__init__(self, *args, **kwargs)
        super(DynamicScrollFrame, self).__init__(*args, **kwargs)
