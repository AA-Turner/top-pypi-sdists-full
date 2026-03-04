# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1ll1l1l11_opy_:
    def __init__(self):
        self._1lll1ll1l1l1_opy_ = deque()
        self._1lll1ll11lll_opy_ = {}
        self._1lll1ll111ll_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll1ll11ll1_opy_(self, test_name, bstack1lll1ll1l11l_opy_):
        with self._lock:
            bstack1lll1ll11l1l_opy_ = self._1lll1ll11lll_opy_.get(test_name, {})
            return bstack1lll1ll11l1l_opy_.get(bstack1lll1ll1l11l_opy_, 0)
    def bstack1lll1l1lllll_opy_(self, test_name, bstack1lll1ll1l11l_opy_):
        with self._lock:
            bstack1lll1ll1l111_opy_ = self.bstack1lll1ll11ll1_opy_(test_name, bstack1lll1ll1l11l_opy_)
            self.bstack1lll1ll111l1_opy_(test_name, bstack1lll1ll1l11l_opy_)
            return bstack1lll1ll1l111_opy_
    def bstack1lll1ll111l1_opy_(self, test_name, bstack1lll1ll1l11l_opy_):
        with self._lock:
            if test_name not in self._1lll1ll11lll_opy_:
                self._1lll1ll11lll_opy_[test_name] = {}
            bstack1lll1ll11l1l_opy_ = self._1lll1ll11lll_opy_[test_name]
            bstack1lll1ll1l111_opy_ = bstack1lll1ll11l1l_opy_.get(bstack1lll1ll1l11l_opy_, 0)
            bstack1lll1ll11l1l_opy_[bstack1lll1ll1l11l_opy_] = bstack1lll1ll1l111_opy_ + 1
    def bstack1lllll111l_opy_(self, bstack1lll1ll1111l_opy_, bstack1lll1l1llll1_opy_):
        bstack1lll1ll11l11_opy_ = self.bstack1lll1l1lllll_opy_(bstack1lll1ll1111l_opy_, bstack1lll1l1llll1_opy_)
        event_name = bstack111ll1l11ll_opy_[bstack1lll1l1llll1_opy_]
        bstack1l1111l1l11_opy_ = bstack1lll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦ⋑").format(bstack1lll1ll1111l_opy_, event_name, bstack1lll1ll11l11_opy_)
        with self._lock:
            self._1lll1ll1l1l1_opy_.append(bstack1l1111l1l11_opy_)
    def bstack111ll1l11l_opy_(self):
        with self._lock:
            return len(self._1lll1ll1l1l1_opy_) == 0
    def bstack1l1l1l1l1_opy_(self):
        with self._lock:
            if self._1lll1ll1l1l1_opy_:
                bstack1lll1ll11111_opy_ = self._1lll1ll1l1l1_opy_.popleft()
                return bstack1lll1ll11111_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll1ll111ll_opy_
    def bstack11lll111l1_opy_(self):
        with self._lock:
            self._1lll1ll111ll_opy_ = True
    def bstack11l1lllll1_opy_(self):
        with self._lock:
            self._1lll1ll111ll_opy_ = False