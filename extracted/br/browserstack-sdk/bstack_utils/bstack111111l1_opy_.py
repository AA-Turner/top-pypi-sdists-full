# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11llllll11_opy_:
    def __init__(self):
        self._1llll1111111_opy_ = deque()
        self._1llll111l11l_opy_ = {}
        self._1lll1lllll1l_opy_ = False
        self._lock = threading.RLock()
    def bstack1llll1111l11_opy_(self, test_name, bstack1lll1llllll1_opy_):
        with self._lock:
            bstack1llll11111l1_opy_ = self._1llll111l11l_opy_.get(test_name, {})
            return bstack1llll11111l1_opy_.get(bstack1lll1llllll1_opy_, 0)
    def bstack1llll111111l_opy_(self, test_name, bstack1lll1llllll1_opy_):
        with self._lock:
            bstack1llll111l111_opy_ = self.bstack1llll1111l11_opy_(test_name, bstack1lll1llllll1_opy_)
            self.bstack1llll11111ll_opy_(test_name, bstack1lll1llllll1_opy_)
            return bstack1llll111l111_opy_
    def bstack1llll11111ll_opy_(self, test_name, bstack1lll1llllll1_opy_):
        with self._lock:
            if test_name not in self._1llll111l11l_opy_:
                self._1llll111l11l_opy_[test_name] = {}
            bstack1llll11111l1_opy_ = self._1llll111l11l_opy_[test_name]
            bstack1llll111l111_opy_ = bstack1llll11111l1_opy_.get(bstack1lll1llllll1_opy_, 0)
            bstack1llll11111l1_opy_[bstack1lll1llllll1_opy_] = bstack1llll111l111_opy_ + 1
    def bstack1l111lll11_opy_(self, bstack1llll1111ll1_opy_, bstack1llll1111l1l_opy_):
        bstack1llll1111lll_opy_ = self.bstack1llll111111l_opy_(bstack1llll1111ll1_opy_, bstack1llll1111l1l_opy_)
        event_name = bstack111lll11lll_opy_[bstack1llll1111l1l_opy_]
        bstack1l111ll1l11_opy_ = bstack11l1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥ↪").format(bstack1llll1111ll1_opy_, event_name, bstack1llll1111lll_opy_)
        with self._lock:
            self._1llll1111111_opy_.append(bstack1l111ll1l11_opy_)
    def bstack11ll1ll1l1_opy_(self):
        with self._lock:
            return len(self._1llll1111111_opy_) == 0
    def bstack1l1l1lll1l_opy_(self):
        with self._lock:
            if self._1llll1111111_opy_:
                bstack1lll1lllllll_opy_ = self._1llll1111111_opy_.popleft()
                return bstack1lll1lllllll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll1lllll1l_opy_
    def bstack111ll111l1_opy_(self):
        with self._lock:
            self._1lll1lllll1l_opy_ = True
    def bstack1111l1111_opy_(self):
        with self._lock:
            self._1lll1lllll1l_opy_ = False