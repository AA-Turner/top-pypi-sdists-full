# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11111l111_opy_:
    def __init__(self):
        self._1llll1111l11_opy_ = deque()
        self._1llll11111ll_opy_ = {}
        self._1llll111l111_opy_ = False
        self._lock = threading.RLock()
    def bstack1llll11111l1_opy_(self, test_name, bstack1llll1111111_opy_):
        with self._lock:
            bstack1llll1111ll1_opy_ = self._1llll11111ll_opy_.get(test_name, {})
            return bstack1llll1111ll1_opy_.get(bstack1llll1111111_opy_, 0)
    def bstack1llll111111l_opy_(self, test_name, bstack1llll1111111_opy_):
        with self._lock:
            bstack1lll1llllll1_opy_ = self.bstack1llll11111l1_opy_(test_name, bstack1llll1111111_opy_)
            self.bstack1lll1lllll1l_opy_(test_name, bstack1llll1111111_opy_)
            return bstack1lll1llllll1_opy_
    def bstack1lll1lllll1l_opy_(self, test_name, bstack1llll1111111_opy_):
        with self._lock:
            if test_name not in self._1llll11111ll_opy_:
                self._1llll11111ll_opy_[test_name] = {}
            bstack1llll1111ll1_opy_ = self._1llll11111ll_opy_[test_name]
            bstack1lll1llllll1_opy_ = bstack1llll1111ll1_opy_.get(bstack1llll1111111_opy_, 0)
            bstack1llll1111ll1_opy_[bstack1llll1111111_opy_] = bstack1lll1llllll1_opy_ + 1
    def bstack111l1ll1l1_opy_(self, bstack1llll1111l1l_opy_, bstack1lll1lllll11_opy_):
        bstack1lll1lllllll_opy_ = self.bstack1llll111111l_opy_(bstack1llll1111l1l_opy_, bstack1lll1lllll11_opy_)
        event_name = bstack111ll1ll1l1_opy_[bstack1lll1lllll11_opy_]
        bstack1l111ll11ll_opy_ = bstack11ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ↧").format(bstack1llll1111l1l_opy_, event_name, bstack1lll1lllllll_opy_)
        with self._lock:
            self._1llll1111l11_opy_.append(bstack1l111ll11ll_opy_)
    def bstack1l11111l1l_opy_(self):
        with self._lock:
            return len(self._1llll1111l11_opy_) == 0
    def bstack1l1ll11ll1_opy_(self):
        with self._lock:
            if self._1llll1111l11_opy_:
                bstack1llll1111lll_opy_ = self._1llll1111l11_opy_.popleft()
                return bstack1llll1111lll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1llll111l111_opy_
    def bstack1l11l1l1l1_opy_(self):
        with self._lock:
            self._1llll111l111_opy_ = True
    def bstack1ll11lllll_opy_(self):
        with self._lock:
            self._1llll111l111_opy_ = False