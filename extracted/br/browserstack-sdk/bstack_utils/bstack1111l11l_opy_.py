# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l1111l1l_opy_:
    def __init__(self):
        self._1lll1l11l111_opy_ = deque()
        self._1lll1l11lll1_opy_ = {}
        self._1lll1l11llll_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll1l1l1111_opy_(self, test_name, bstack1lll1l11l1l1_opy_):
        with self._lock:
            bstack1lll1l111lll_opy_ = self._1lll1l11lll1_opy_.get(test_name, {})
            return bstack1lll1l111lll_opy_.get(bstack1lll1l11l1l1_opy_, 0)
    def bstack1lll1l1l11l1_opy_(self, test_name, bstack1lll1l11l1l1_opy_):
        with self._lock:
            bstack1lll1l11l11l_opy_ = self.bstack1lll1l1l1111_opy_(test_name, bstack1lll1l11l1l1_opy_)
            self.bstack1lll1l1l111l_opy_(test_name, bstack1lll1l11l1l1_opy_)
            return bstack1lll1l11l11l_opy_
    def bstack1lll1l1l111l_opy_(self, test_name, bstack1lll1l11l1l1_opy_):
        with self._lock:
            if test_name not in self._1lll1l11lll1_opy_:
                self._1lll1l11lll1_opy_[test_name] = {}
            bstack1lll1l111lll_opy_ = self._1lll1l11lll1_opy_[test_name]
            bstack1lll1l11l11l_opy_ = bstack1lll1l111lll_opy_.get(bstack1lll1l11l1l1_opy_, 0)
            bstack1lll1l111lll_opy_[bstack1lll1l11l1l1_opy_] = bstack1lll1l11l11l_opy_ + 1
    def bstack111111ll1_opy_(self, bstack1lll1l1l11ll_opy_, bstack1lll1l11ll1l_opy_):
        bstack1lll1l11ll11_opy_ = self.bstack1lll1l1l11l1_opy_(bstack1lll1l1l11ll_opy_, bstack1lll1l11ll1l_opy_)
        event_name = bstack111l1llll1l_opy_[bstack1lll1l11ll1l_opy_]
        bstack1l111111lll_opy_ = bstack1111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ⎑").format(bstack1lll1l1l11ll_opy_, event_name, bstack1lll1l11ll11_opy_)
        with self._lock:
            self._1lll1l11l111_opy_.append(bstack1l111111lll_opy_)
    def bstack1l11ll1ll1_opy_(self):
        with self._lock:
            return len(self._1lll1l11l111_opy_) == 0
    def bstack111l11ll1l_opy_(self):
        with self._lock:
            if self._1lll1l11l111_opy_:
                bstack1lll1l11l1ll_opy_ = self._1lll1l11l111_opy_.popleft()
                return bstack1lll1l11l1ll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll1l11llll_opy_
    def bstack1l1111l1l1_opy_(self):
        with self._lock:
            self._1lll1l11llll_opy_ = True
    def bstack11lll1llll_opy_(self):
        with self._lock:
            self._1lll1l11llll_opy_ = False