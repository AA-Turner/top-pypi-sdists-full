# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1lll11l11l_opy_:
    def __init__(self):
        self._11111l11l11_opy_ = deque()
        self._111111lllll_opy_ = {}
        self._11111l1l111_opy_ = False
        self._lock = threading.RLock()
    def bstack11111l11ll1_opy_(self, test_name, bstack11111l1111l_opy_):
        with self._lock:
            bstack11111l111ll_opy_ = self._111111lllll_opy_.get(test_name, {})
            return bstack11111l111ll_opy_.get(bstack11111l1111l_opy_, 0)
    def bstack11111l1l11l_opy_(self, test_name, bstack11111l1111l_opy_):
        with self._lock:
            bstack11111l111l1_opy_ = self.bstack11111l11ll1_opy_(test_name, bstack11111l1111l_opy_)
            self.bstack11111l11l1l_opy_(test_name, bstack11111l1111l_opy_)
            return bstack11111l111l1_opy_
    def bstack11111l11l1l_opy_(self, test_name, bstack11111l1111l_opy_):
        with self._lock:
            if test_name not in self._111111lllll_opy_:
                self._111111lllll_opy_[test_name] = {}
            bstack11111l111ll_opy_ = self._111111lllll_opy_[test_name]
            bstack11111l111l1_opy_ = bstack11111l111ll_opy_.get(bstack11111l1111l_opy_, 0)
            bstack11111l111ll_opy_[bstack11111l1111l_opy_] = bstack11111l111l1_opy_ + 1
    def bstack1l1llll1l_opy_(self, bstack11111l1l1ll_opy_, bstack11111l11111_opy_):
        bstack11111l1l1l1_opy_ = self.bstack11111l1l11l_opy_(bstack11111l1l1ll_opy_, bstack11111l11111_opy_)
        event_name = bstack11l1lll1ll1_opy_[bstack11111l11111_opy_]
        bstack1l1l1l111ll_opy_ = bstack1l11l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨἢ").format(bstack11111l1l1ll_opy_, event_name, bstack11111l1l1l1_opy_)
        with self._lock:
            self._11111l11l11_opy_.append(bstack1l1l1l111ll_opy_)
    def bstack111l1l111_opy_(self):
        with self._lock:
            return len(self._11111l11l11_opy_) == 0
    def bstack1llllll11l_opy_(self):
        with self._lock:
            if self._11111l11l11_opy_:
                bstack11111l11lll_opy_ = self._11111l11l11_opy_.popleft()
                return bstack11111l11lll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._11111l1l111_opy_
    def bstack11lll1111l_opy_(self):
        with self._lock:
            self._11111l1l111_opy_ = True
    def bstack111lll11_opy_(self):
        with self._lock:
            self._11111l1l111_opy_ = False