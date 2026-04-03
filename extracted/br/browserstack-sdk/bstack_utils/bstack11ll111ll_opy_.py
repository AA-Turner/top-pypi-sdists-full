# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11ll1l11ll_opy_:
    def __init__(self):
        self._1ll1l1lll1ll_opy_ = deque()
        self._1ll1ll111111_opy_ = {}
        self._1ll1ll1111l1_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1ll11111l_opy_(self, test_name, bstack1ll1l1llll11_opy_):
        with self._lock:
            bstack1ll1ll111ll1_opy_ = self._1ll1ll111111_opy_.get(test_name, {})
            return bstack1ll1ll111ll1_opy_.get(bstack1ll1l1llll11_opy_, 0)
    def bstack1ll1l1llll1l_opy_(self, test_name, bstack1ll1l1llll11_opy_):
        with self._lock:
            bstack1ll1ll111lll_opy_ = self.bstack1ll1ll11111l_opy_(test_name, bstack1ll1l1llll11_opy_)
            self.bstack1ll1l1llllll_opy_(test_name, bstack1ll1l1llll11_opy_)
            return bstack1ll1ll111lll_opy_
    def bstack1ll1l1llllll_opy_(self, test_name, bstack1ll1l1llll11_opy_):
        with self._lock:
            if test_name not in self._1ll1ll111111_opy_:
                self._1ll1ll111111_opy_[test_name] = {}
            bstack1ll1ll111ll1_opy_ = self._1ll1ll111111_opy_[test_name]
            bstack1ll1ll111lll_opy_ = bstack1ll1ll111ll1_opy_.get(bstack1ll1l1llll11_opy_, 0)
            bstack1ll1ll111ll1_opy_[bstack1ll1l1llll11_opy_] = bstack1ll1ll111lll_opy_ + 1
    def bstack111lll111_opy_(self, bstack1ll1ll111l1l_opy_, bstack1ll1ll111l11_opy_):
        bstack1ll1ll1111ll_opy_ = self.bstack1ll1l1llll1l_opy_(bstack1ll1ll111l1l_opy_, bstack1ll1ll111l11_opy_)
        event_name = bstack11111l1lll1_opy_[bstack1ll1ll111l11_opy_]
        bstack11ll1111lll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥ◧").format(bstack1ll1ll111l1l_opy_, event_name, bstack1ll1ll1111ll_opy_)
        with self._lock:
            self._1ll1l1lll1ll_opy_.append(bstack11ll1111lll_opy_)
    def bstack111llll11_opy_(self):
        with self._lock:
            return len(self._1ll1l1lll1ll_opy_) == 0
    def bstack111111l1l1_opy_(self):
        with self._lock:
            if self._1ll1l1lll1ll_opy_:
                bstack1ll1l1lllll1_opy_ = self._1ll1l1lll1ll_opy_.popleft()
                return bstack1ll1l1lllll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1ll1111l1_opy_
    def bstack1lllll1lll_opy_(self):
        with self._lock:
            self._1ll1ll1111l1_opy_ = True
    def bstack11111111_opy_(self):
        with self._lock:
            self._1ll1ll1111l1_opy_ = False