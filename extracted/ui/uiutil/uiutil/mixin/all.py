# encoding: utf-8

from .var import VarMixIn
from .poll import PollMixIn
from .style import StyleMixIn
from .widget import WidgetMixIn
from .layout import FrameLayoutMixIn
from classutils.observer import ObservableObserverMixIn
from classutils.thread_pool import ThreadPoolMixIn


class AllMixIn(FrameLayoutMixIn,
               StyleMixIn,
               WidgetMixIn,
               VarMixIn,
               PollMixIn,
               ObservableObserverMixIn,
               ThreadPoolMixIn):

    def __init__(self,
                 *args,
                 **kwargs):
        super(AllMixIn, self).__init__(*args, **kwargs)
