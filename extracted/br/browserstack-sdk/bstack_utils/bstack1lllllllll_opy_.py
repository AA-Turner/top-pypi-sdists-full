# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1lll11l1l1l_opy_:
    def __init__(self):
        self._1ll11l1l1lll_opy_ = deque()
        self._1ll11l1ll1l1_opy_ = {}
        self._1ll11l1lll11_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll11ll11111_opy_(self, test_name, bstack1ll11l1ll111_opy_):
        with self._lock:
            bstack1ll11l1ll1ll_opy_ = self._1ll11l1ll1l1_opy_.get(test_name, {})
            return bstack1ll11l1ll1ll_opy_.get(bstack1ll11l1ll111_opy_, 0)
    def bstack1ll11ll1111l_opy_(self, test_name, bstack1ll11l1ll111_opy_):
        with self._lock:
            bstack1ll11l1lll1l_opy_ = self.bstack1ll11ll11111_opy_(test_name, bstack1ll11l1ll111_opy_)
            self.bstack1ll11l1ll11l_opy_(test_name, bstack1ll11l1ll111_opy_)
            return bstack1ll11l1lll1l_opy_
    def bstack1ll11l1ll11l_opy_(self, test_name, bstack1ll11l1ll111_opy_):
        with self._lock:
            if test_name not in self._1ll11l1ll1l1_opy_:
                self._1ll11l1ll1l1_opy_[test_name] = {}
            bstack1ll11l1ll1ll_opy_ = self._1ll11l1ll1l1_opy_[test_name]
            bstack1ll11l1lll1l_opy_ = bstack1ll11l1ll1ll_opy_.get(bstack1ll11l1ll111_opy_, 0)
            bstack1ll11l1ll1ll_opy_[bstack1ll11l1ll111_opy_] = bstack1ll11l1lll1l_opy_ + 1
    def bstack1l11l11111_opy_(self, bstack1ll11l1lllll_opy_, bstack1ll11l1llll1_opy_):
        bstack1ll11ll111l1_opy_ = self.bstack1ll11ll1111l_opy_(bstack1ll11l1lllll_opy_, bstack1ll11l1llll1_opy_)
        event_name = bstack1lllllll11l1_opy_[bstack1ll11l1llll1_opy_]
        bstack11l1l1l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ⦣").format(bstack1ll11l1lllll_opy_, event_name, bstack1ll11ll111l1_opy_)
        with self._lock:
            self._1ll11l1l1lll_opy_.append(bstack11l1l1l1ll1_opy_)
    def bstack11l111lll1_opy_(self):
        with self._lock:
            return len(self._1ll11l1l1lll_opy_) == 0
    def bstack11ll1l1l11_opy_(self):
        with self._lock:
            if self._1ll11l1l1lll_opy_:
                bstack1ll11l1l1ll1_opy_ = self._1ll11l1l1lll_opy_.popleft()
                return bstack1ll11l1l1ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll11l1lll11_opy_
    def bstack111ll111l1_opy_(self):
        with self._lock:
            self._1ll11l1lll11_opy_ = True
    def bstack1llll1l11ll_opy_(self):
        with self._lock:
            self._1ll11l1lll11_opy_ = False