# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l11ll1ll_opy_:
    def __init__(self):
        self._11111l111ll_opy_ = deque()
        self._11111l11lll_opy_ = {}
        self._11111l1llll_opy_ = False
        self._lock = threading.RLock()
    def bstack11111l11l11_opy_(self, test_name, bstack11111l1l1ll_opy_):
        with self._lock:
            bstack11111l1ll1l_opy_ = self._11111l11lll_opy_.get(test_name, {})
            return bstack11111l1ll1l_opy_.get(bstack11111l1l1ll_opy_, 0)
    def bstack11111l1ll11_opy_(self, test_name, bstack11111l1l1ll_opy_):
        with self._lock:
            bstack11111l11ll1_opy_ = self.bstack11111l11l11_opy_(test_name, bstack11111l1l1ll_opy_)
            self.bstack11111l1l1l1_opy_(test_name, bstack11111l1l1ll_opy_)
            return bstack11111l11ll1_opy_
    def bstack11111l1l1l1_opy_(self, test_name, bstack11111l1l1ll_opy_):
        with self._lock:
            if test_name not in self._11111l11lll_opy_:
                self._11111l11lll_opy_[test_name] = {}
            bstack11111l1ll1l_opy_ = self._11111l11lll_opy_[test_name]
            bstack11111l11ll1_opy_ = bstack11111l1ll1l_opy_.get(bstack11111l1l1ll_opy_, 0)
            bstack11111l1ll1l_opy_[bstack11111l1l1ll_opy_] = bstack11111l11ll1_opy_ + 1
    def bstack11llll11l1_opy_(self, bstack11111l1l11l_opy_, bstack11111l11l1l_opy_):
        bstack11111l1l111_opy_ = self.bstack11111l1ll11_opy_(bstack11111l1l11l_opy_, bstack11111l11l1l_opy_)
        event_name = bstack11l1l1lllll_opy_[bstack11111l11l1l_opy_]
        bstack1l1l1l11ll1_opy_ = bstack11l1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢἣ").format(bstack11111l1l11l_opy_, event_name, bstack11111l1l111_opy_)
        with self._lock:
            self._11111l111ll_opy_.append(bstack1l1l1l11ll1_opy_)
    def bstack1l11ll1111_opy_(self):
        with self._lock:
            return len(self._11111l111ll_opy_) == 0
    def bstack11l11l11ll_opy_(self):
        with self._lock:
            if self._11111l111ll_opy_:
                bstack11111l1lll1_opy_ = self._11111l111ll_opy_.popleft()
                return bstack11111l1lll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._11111l1llll_opy_
    def bstack1l1l1ll1l_opy_(self):
        with self._lock:
            self._11111l1llll_opy_ = True
    def bstack111llll1l_opy_(self):
        with self._lock:
            self._11111l1llll_opy_ = False