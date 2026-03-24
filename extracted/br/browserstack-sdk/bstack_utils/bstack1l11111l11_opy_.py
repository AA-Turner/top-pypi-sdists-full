# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l1111lll1_opy_:
    def __init__(self):
        self._1lll11ll11ll_opy_ = deque()
        self._1lll11l1llll_opy_ = {}
        self._1lll11ll1l11_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll11l1l1ll_opy_(self, test_name, bstack1lll11ll11l1_opy_):
        with self._lock:
            bstack1lll11ll1ll1_opy_ = self._1lll11l1llll_opy_.get(test_name, {})
            return bstack1lll11ll1ll1_opy_.get(bstack1lll11ll11l1_opy_, 0)
    def bstack1lll11ll1111_opy_(self, test_name, bstack1lll11ll11l1_opy_):
        with self._lock:
            bstack1lll11l1ll11_opy_ = self.bstack1lll11l1l1ll_opy_(test_name, bstack1lll11ll11l1_opy_)
            self.bstack1lll11ll1lll_opy_(test_name, bstack1lll11ll11l1_opy_)
            return bstack1lll11l1ll11_opy_
    def bstack1lll11ll1lll_opy_(self, test_name, bstack1lll11ll11l1_opy_):
        with self._lock:
            if test_name not in self._1lll11l1llll_opy_:
                self._1lll11l1llll_opy_[test_name] = {}
            bstack1lll11ll1ll1_opy_ = self._1lll11l1llll_opy_[test_name]
            bstack1lll11l1ll11_opy_ = bstack1lll11ll1ll1_opy_.get(bstack1lll11ll11l1_opy_, 0)
            bstack1lll11ll1ll1_opy_[bstack1lll11ll11l1_opy_] = bstack1lll11l1ll11_opy_ + 1
    def bstack1lll1lll1_opy_(self, bstack1lll11l1lll1_opy_, bstack1lll11l1ll1l_opy_):
        bstack1lll11ll111l_opy_ = self.bstack1lll11ll1111_opy_(bstack1lll11l1lll1_opy_, bstack1lll11l1ll1l_opy_)
        event_name = bstack111l11l1l1l_opy_[bstack1lll11l1ll1l_opy_]
        bstack11llll11lll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦ⏢").format(bstack1lll11l1lll1_opy_, event_name, bstack1lll11ll111l_opy_)
        with self._lock:
            self._1lll11ll11ll_opy_.append(bstack11llll11lll_opy_)
    def bstack11ll1l1ll1_opy_(self):
        with self._lock:
            return len(self._1lll11ll11ll_opy_) == 0
    def bstack11l111ll1l_opy_(self):
        with self._lock:
            if self._1lll11ll11ll_opy_:
                bstack1lll11ll1l1l_opy_ = self._1lll11ll11ll_opy_.popleft()
                return bstack1lll11ll1l1l_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll11ll1l11_opy_
    def bstack1l1ll1ll1_opy_(self):
        with self._lock:
            self._1lll11ll1l11_opy_ = True
    def bstack11l1l111l1_opy_(self):
        with self._lock:
            self._1lll11ll1l11_opy_ = False