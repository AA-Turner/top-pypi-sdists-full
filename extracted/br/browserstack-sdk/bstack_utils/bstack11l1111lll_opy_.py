# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1lll1ll1l1_opy_:
    def __init__(self):
        self._1ll1l1l1l1l1_opy_ = deque()
        self._1ll1l1l1l1ll_opy_ = {}
        self._1ll1l1l1lll1_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1l1l11l1l_opy_(self, test_name, bstack1ll1l1l1l11l_opy_):
        with self._lock:
            bstack1ll1l1l1ll1l_opy_ = self._1ll1l1l1l1ll_opy_.get(test_name, {})
            return bstack1ll1l1l1ll1l_opy_.get(bstack1ll1l1l1l11l_opy_, 0)
    def bstack1ll1l1l11l11_opy_(self, test_name, bstack1ll1l1l1l11l_opy_):
        with self._lock:
            bstack1ll1l1l11ll1_opy_ = self.bstack1ll1l1l11l1l_opy_(test_name, bstack1ll1l1l1l11l_opy_)
            self.bstack1ll1l1l1l111_opy_(test_name, bstack1ll1l1l1l11l_opy_)
            return bstack1ll1l1l11ll1_opy_
    def bstack1ll1l1l1l111_opy_(self, test_name, bstack1ll1l1l1l11l_opy_):
        with self._lock:
            if test_name not in self._1ll1l1l1l1ll_opy_:
                self._1ll1l1l1l1ll_opy_[test_name] = {}
            bstack1ll1l1l1ll1l_opy_ = self._1ll1l1l1l1ll_opy_[test_name]
            bstack1ll1l1l11ll1_opy_ = bstack1ll1l1l1ll1l_opy_.get(bstack1ll1l1l1l11l_opy_, 0)
            bstack1ll1l1l1ll1l_opy_[bstack1ll1l1l1l11l_opy_] = bstack1ll1l1l11ll1_opy_ + 1
    def bstack1l1lllll_opy_(self, bstack1ll1l1ll1111_opy_, bstack1ll1l1l1llll_opy_):
        bstack1ll1l1l11lll_opy_ = self.bstack1ll1l1l11l11_opy_(bstack1ll1l1ll1111_opy_, bstack1ll1l1l1llll_opy_)
        event_name = bstack111111ll1l1_opy_[bstack1ll1l1l1llll_opy_]
        bstack11ll1111l11_opy_ = bstack1l1111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ☣").format(bstack1ll1l1ll1111_opy_, event_name, bstack1ll1l1l11lll_opy_)
        with self._lock:
            self._1ll1l1l1l1l1_opy_.append(bstack11ll1111l11_opy_)
    def bstack11111111_opy_(self):
        with self._lock:
            return len(self._1ll1l1l1l1l1_opy_) == 0
    def bstack1llllll1lll_opy_(self):
        with self._lock:
            if self._1ll1l1l1l1l1_opy_:
                bstack1ll1l1l1ll11_opy_ = self._1ll1l1l1l1l1_opy_.popleft()
                return bstack1ll1l1l1ll11_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1l1l1lll1_opy_
    def bstack111lll1l11_opy_(self):
        with self._lock:
            self._1ll1l1l1lll1_opy_ = True
    def bstack11l1ll11l1_opy_(self):
        with self._lock:
            self._1ll1l1l1lll1_opy_ = False