# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1lll1l111_opy_:
    def __init__(self):
        self._11111l1llll_opy_ = deque()
        self._11111l11lll_opy_ = {}
        self._11111l11l11_opy_ = False
        self._lock = threading.RLock()
    def bstack11111l1lll1_opy_(self, test_name, bstack11111l1ll11_opy_):
        with self._lock:
            bstack11111l11ll1_opy_ = self._11111l11lll_opy_.get(test_name, {})
            return bstack11111l11ll1_opy_.get(bstack11111l1ll11_opy_, 0)
    def bstack11111l11l1l_opy_(self, test_name, bstack11111l1ll11_opy_):
        with self._lock:
            bstack11111l111ll_opy_ = self.bstack11111l1lll1_opy_(test_name, bstack11111l1ll11_opy_)
            self.bstack11111l1l11l_opy_(test_name, bstack11111l1ll11_opy_)
            return bstack11111l111ll_opy_
    def bstack11111l1l11l_opy_(self, test_name, bstack11111l1ll11_opy_):
        with self._lock:
            if test_name not in self._11111l11lll_opy_:
                self._11111l11lll_opy_[test_name] = {}
            bstack11111l11ll1_opy_ = self._11111l11lll_opy_[test_name]
            bstack11111l111ll_opy_ = bstack11111l11ll1_opy_.get(bstack11111l1ll11_opy_, 0)
            bstack11111l11ll1_opy_[bstack11111l1ll11_opy_] = bstack11111l111ll_opy_ + 1
    def bstack1llllll111_opy_(self, bstack11111l1ll1l_opy_, bstack11111l1l111_opy_):
        bstack11111l1l1l1_opy_ = self.bstack11111l11l1l_opy_(bstack11111l1ll1l_opy_, bstack11111l1l111_opy_)
        event_name = bstack11l1ll1lll1_opy_[bstack11111l1l111_opy_]
        bstack1l1l1l1l11l_opy_ = bstack1ll1ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨἢ").format(bstack11111l1ll1l_opy_, event_name, bstack11111l1l1l1_opy_)
        with self._lock:
            self._11111l1llll_opy_.append(bstack1l1l1l1l11l_opy_)
    def bstack1l11l1l1l1_opy_(self):
        with self._lock:
            return len(self._11111l1llll_opy_) == 0
    def bstack1lll1l1l11_opy_(self):
        with self._lock:
            if self._11111l1llll_opy_:
                bstack11111l1l1ll_opy_ = self._11111l1llll_opy_.popleft()
                return bstack11111l1l1ll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._11111l11l11_opy_
    def bstack1l1lllllll_opy_(self):
        with self._lock:
            self._11111l11l11_opy_ = True
    def bstack1lllll1lll_opy_(self):
        with self._lock:
            self._11111l11l11_opy_ = False