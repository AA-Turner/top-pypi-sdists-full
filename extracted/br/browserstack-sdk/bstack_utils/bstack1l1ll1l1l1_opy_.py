# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack111llll1l_opy_:
    def __init__(self):
        self._1ll1ll11111l_opy_ = deque()
        self._1ll1l1llll11_opy_ = {}
        self._1ll1l1lll1l1_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1l1llll1l_opy_(self, test_name, bstack1ll1l1lllll1_opy_):
        with self._lock:
            bstack1ll1l1lll1ll_opy_ = self._1ll1l1llll11_opy_.get(test_name, {})
            return bstack1ll1l1lll1ll_opy_.get(bstack1ll1l1lllll1_opy_, 0)
    def bstack1ll1ll1111ll_opy_(self, test_name, bstack1ll1l1lllll1_opy_):
        with self._lock:
            bstack1ll1ll111l11_opy_ = self.bstack1ll1l1llll1l_opy_(test_name, bstack1ll1l1lllll1_opy_)
            self.bstack1ll1ll1111l1_opy_(test_name, bstack1ll1l1lllll1_opy_)
            return bstack1ll1ll111l11_opy_
    def bstack1ll1ll1111l1_opy_(self, test_name, bstack1ll1l1lllll1_opy_):
        with self._lock:
            if test_name not in self._1ll1l1llll11_opy_:
                self._1ll1l1llll11_opy_[test_name] = {}
            bstack1ll1l1lll1ll_opy_ = self._1ll1l1llll11_opy_[test_name]
            bstack1ll1ll111l11_opy_ = bstack1ll1l1lll1ll_opy_.get(bstack1ll1l1lllll1_opy_, 0)
            bstack1ll1l1lll1ll_opy_[bstack1ll1l1lllll1_opy_] = bstack1ll1ll111l11_opy_ + 1
    def bstack11ll1lllll_opy_(self, bstack1ll1l1lll11l_opy_, bstack1ll1l1lll111_opy_):
        bstack1ll1l1llllll_opy_ = self.bstack1ll1ll1111ll_opy_(bstack1ll1l1lll11l_opy_, bstack1ll1l1lll111_opy_)
        event_name = bstack11111l1111l_opy_[bstack1ll1l1lll111_opy_]
        bstack11ll1111l1l_opy_ = bstack11ll11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ◫").format(bstack1ll1l1lll11l_opy_, event_name, bstack1ll1l1llllll_opy_)
        with self._lock:
            self._1ll1ll11111l_opy_.append(bstack11ll1111l1l_opy_)
    def bstack1l1l111lll_opy_(self):
        with self._lock:
            return len(self._1ll1ll11111l_opy_) == 0
    def bstack1l11llll1_opy_(self):
        with self._lock:
            if self._1ll1ll11111l_opy_:
                bstack1ll1ll111111_opy_ = self._1ll1ll11111l_opy_.popleft()
                return bstack1ll1ll111111_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1l1lll1l1_opy_
    def bstack1l111111l1_opy_(self):
        with self._lock:
            self._1ll1l1lll1l1_opy_ = True
    def bstack11ll1ll111_opy_(self):
        with self._lock:
            self._1ll1l1lll1l1_opy_ = False