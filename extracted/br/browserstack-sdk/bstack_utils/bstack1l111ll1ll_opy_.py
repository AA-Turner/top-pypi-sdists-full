# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l1l111l11_opy_:
    def __init__(self):
        self._1ll1l1lll1l1_opy_ = deque()
        self._1ll1l1llll11_opy_ = {}
        self._1ll1ll1111ll_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1ll111l11_opy_(self, test_name, bstack1ll1l1lll1ll_opy_):
        with self._lock:
            bstack1ll1ll111111_opy_ = self._1ll1l1llll11_opy_.get(test_name, {})
            return bstack1ll1ll111111_opy_.get(bstack1ll1l1lll1ll_opy_, 0)
    def bstack1ll1l1llllll_opy_(self, test_name, bstack1ll1l1lll1ll_opy_):
        with self._lock:
            bstack1ll1l1llll1l_opy_ = self.bstack1ll1ll111l11_opy_(test_name, bstack1ll1l1lll1ll_opy_)
            self.bstack1ll1ll11111l_opy_(test_name, bstack1ll1l1lll1ll_opy_)
            return bstack1ll1l1llll1l_opy_
    def bstack1ll1ll11111l_opy_(self, test_name, bstack1ll1l1lll1ll_opy_):
        with self._lock:
            if test_name not in self._1ll1l1llll11_opy_:
                self._1ll1l1llll11_opy_[test_name] = {}
            bstack1ll1ll111111_opy_ = self._1ll1l1llll11_opy_[test_name]
            bstack1ll1l1llll1l_opy_ = bstack1ll1ll111111_opy_.get(bstack1ll1l1lll1ll_opy_, 0)
            bstack1ll1ll111111_opy_[bstack1ll1l1lll1ll_opy_] = bstack1ll1l1llll1l_opy_ + 1
    def bstack11ll1l1ll1_opy_(self, bstack1ll1ll1111l1_opy_, bstack1ll1ll111l1l_opy_):
        bstack1ll1l1lll11l_opy_ = self.bstack1ll1l1llllll_opy_(bstack1ll1ll1111l1_opy_, bstack1ll1ll111l1l_opy_)
        event_name = bstack11111ll11ll_opy_[bstack1ll1ll111l1l_opy_]
        bstack11l1l1lll11_opy_ = bstack111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨ◪").format(bstack1ll1ll1111l1_opy_, event_name, bstack1ll1l1lll11l_opy_)
        with self._lock:
            self._1ll1l1lll1l1_opy_.append(bstack11l1l1lll11_opy_)
    def bstack11llll1ll_opy_(self):
        with self._lock:
            return len(self._1ll1l1lll1l1_opy_) == 0
    def bstack1llll1l1_opy_(self):
        with self._lock:
            if self._1ll1l1lll1l1_opy_:
                bstack1ll1l1lllll1_opy_ = self._1ll1l1lll1l1_opy_.popleft()
                return bstack1ll1l1lllll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1ll1111ll_opy_
    def bstack1l111llll1_opy_(self):
        with self._lock:
            self._1ll1ll1111ll_opy_ = True
    def bstack1llll1l1l_opy_(self):
        with self._lock:
            self._1ll1ll1111ll_opy_ = False