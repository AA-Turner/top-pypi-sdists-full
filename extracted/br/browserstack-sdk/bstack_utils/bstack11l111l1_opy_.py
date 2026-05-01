# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1111l1lll_opy_:
    def __init__(self):
        self._1ll1l1l1111l_opy_ = deque()
        self._1ll1l1l11l1l_opy_ = {}
        self._1ll1l1l111l1_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1l1l1ll11_opy_(self, test_name, bstack1ll1l1l1l111_opy_):
        with self._lock:
            bstack1ll1l1l11ll1_opy_ = self._1ll1l1l11l1l_opy_.get(test_name, {})
            return bstack1ll1l1l11ll1_opy_.get(bstack1ll1l1l1l111_opy_, 0)
    def bstack1ll1l1l1l1ll_opy_(self, test_name, bstack1ll1l1l1l111_opy_):
        with self._lock:
            bstack1ll1l1l1ll1l_opy_ = self.bstack1ll1l1l1ll11_opy_(test_name, bstack1ll1l1l1l111_opy_)
            self.bstack1ll1l1l11lll_opy_(test_name, bstack1ll1l1l1l111_opy_)
            return bstack1ll1l1l1ll1l_opy_
    def bstack1ll1l1l11lll_opy_(self, test_name, bstack1ll1l1l1l111_opy_):
        with self._lock:
            if test_name not in self._1ll1l1l11l1l_opy_:
                self._1ll1l1l11l1l_opy_[test_name] = {}
            bstack1ll1l1l11ll1_opy_ = self._1ll1l1l11l1l_opy_[test_name]
            bstack1ll1l1l1ll1l_opy_ = bstack1ll1l1l11ll1_opy_.get(bstack1ll1l1l1l111_opy_, 0)
            bstack1ll1l1l11ll1_opy_[bstack1ll1l1l1l111_opy_] = bstack1ll1l1l1ll1l_opy_ + 1
    def bstack1l111lllll_opy_(self, bstack1ll1l1l111ll_opy_, bstack1ll1l1l1l11l_opy_):
        bstack1ll1l1l1l1l1_opy_ = self.bstack1ll1l1l1l1ll_opy_(bstack1ll1l1l111ll_opy_, bstack1ll1l1l1l11l_opy_)
        event_name = bstack11111111l1l_opy_[bstack1ll1l1l1l11l_opy_]
        bstack11l1llll1ll_opy_ = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦ♭").format(bstack1ll1l1l111ll_opy_, event_name, bstack1ll1l1l1l1l1_opy_)
        with self._lock:
            self._1ll1l1l1111l_opy_.append(bstack11l1llll1ll_opy_)
    def bstack11l1l11l11_opy_(self):
        with self._lock:
            return len(self._1ll1l1l1111l_opy_) == 0
    def bstack11l111l11_opy_(self):
        with self._lock:
            if self._1ll1l1l1111l_opy_:
                bstack1ll1l1l11l11_opy_ = self._1ll1l1l1111l_opy_.popleft()
                return bstack1ll1l1l11l11_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1l1l111l1_opy_
    def bstack1l1l11llll_opy_(self):
        with self._lock:
            self._1ll1l1l111l1_opy_ = True
    def bstack1l1l11ll_opy_(self):
        with self._lock:
            self._1ll1l1l111l1_opy_ = False