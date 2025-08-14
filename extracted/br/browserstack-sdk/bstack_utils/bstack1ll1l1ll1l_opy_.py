# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1ll1ll1lll_opy_:
    def __init__(self):
        self._11111l11ll1_opy_ = deque()
        self._11111l111l1_opy_ = {}
        self._11111l111ll_opy_ = False
        self._lock = threading.RLock()
    def bstack11111l1l1l1_opy_(self, test_name, bstack11111l1ll1l_opy_):
        with self._lock:
            bstack11111l1l1ll_opy_ = self._11111l111l1_opy_.get(test_name, {})
            return bstack11111l1l1ll_opy_.get(bstack11111l1ll1l_opy_, 0)
    def bstack11111l1ll11_opy_(self, test_name, bstack11111l1ll1l_opy_):
        with self._lock:
            bstack11111l1l111_opy_ = self.bstack11111l1l1l1_opy_(test_name, bstack11111l1ll1l_opy_)
            self.bstack11111l1l11l_opy_(test_name, bstack11111l1ll1l_opy_)
            return bstack11111l1l111_opy_
    def bstack11111l1l11l_opy_(self, test_name, bstack11111l1ll1l_opy_):
        with self._lock:
            if test_name not in self._11111l111l1_opy_:
                self._11111l111l1_opy_[test_name] = {}
            bstack11111l1l1ll_opy_ = self._11111l111l1_opy_[test_name]
            bstack11111l1l111_opy_ = bstack11111l1l1ll_opy_.get(bstack11111l1ll1l_opy_, 0)
            bstack11111l1l1ll_opy_[bstack11111l1ll1l_opy_] = bstack11111l1l111_opy_ + 1
    def bstack1llll1111_opy_(self, bstack11111l1111l_opy_, bstack11111l11l11_opy_):
        bstack11111l11lll_opy_ = self.bstack11111l1ll11_opy_(bstack11111l1111l_opy_, bstack11111l11l11_opy_)
        event_name = bstack11l1ll1ll1l_opy_[bstack11111l11l11_opy_]
        bstack1l1l1l11lll_opy_ = bstack1l1l1ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨἰ").format(bstack11111l1111l_opy_, event_name, bstack11111l11lll_opy_)
        with self._lock:
            self._11111l11ll1_opy_.append(bstack1l1l1l11lll_opy_)
    def bstack1l1111l1ll_opy_(self):
        with self._lock:
            return len(self._11111l11ll1_opy_) == 0
    def bstack11l1ll1ll_opy_(self):
        with self._lock:
            if self._11111l11ll1_opy_:
                bstack11111l11l1l_opy_ = self._11111l11ll1_opy_.popleft()
                return bstack11111l11l1l_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._11111l111ll_opy_
    def bstack1ll11lll1_opy_(self):
        with self._lock:
            self._11111l111ll_opy_ = True
    def bstack11lllllll1_opy_(self):
        with self._lock:
            self._11111l111ll_opy_ = False