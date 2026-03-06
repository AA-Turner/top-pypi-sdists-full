# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack111l111ll1_opy_:
    def __init__(self):
        self._1lll1ll111l1_opy_ = deque()
        self._1lll1l1lll11_opy_ = {}
        self._1lll1ll11l1l_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll1l1llll1_opy_(self, test_name, bstack1lll1l1lllll_opy_):
        with self._lock:
            bstack1lll1ll11111_opy_ = self._1lll1l1lll11_opy_.get(test_name, {})
            return bstack1lll1ll11111_opy_.get(bstack1lll1l1lllll_opy_, 0)
    def bstack1lll1ll1111l_opy_(self, test_name, bstack1lll1l1lllll_opy_):
        with self._lock:
            bstack1lll1ll1l111_opy_ = self.bstack1lll1l1llll1_opy_(test_name, bstack1lll1l1lllll_opy_)
            self.bstack1lll1ll111ll_opy_(test_name, bstack1lll1l1lllll_opy_)
            return bstack1lll1ll1l111_opy_
    def bstack1lll1ll111ll_opy_(self, test_name, bstack1lll1l1lllll_opy_):
        with self._lock:
            if test_name not in self._1lll1l1lll11_opy_:
                self._1lll1l1lll11_opy_[test_name] = {}
            bstack1lll1ll11111_opy_ = self._1lll1l1lll11_opy_[test_name]
            bstack1lll1ll1l111_opy_ = bstack1lll1ll11111_opy_.get(bstack1lll1l1lllll_opy_, 0)
            bstack1lll1ll11111_opy_[bstack1lll1l1lllll_opy_] = bstack1lll1ll1l111_opy_ + 1
    def bstack111l11ll_opy_(self, bstack1lll1ll11lll_opy_, bstack1lll1l1lll1l_opy_):
        bstack1lll1ll11l11_opy_ = self.bstack1lll1ll1111l_opy_(bstack1lll1ll11lll_opy_, bstack1lll1l1lll1l_opy_)
        event_name = bstack111ll1l1111_opy_[bstack1lll1l1lll1l_opy_]
        bstack1l1111ll111_opy_ = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧ⋒").format(bstack1lll1ll11lll_opy_, event_name, bstack1lll1ll11l11_opy_)
        with self._lock:
            self._1lll1ll111l1_opy_.append(bstack1l1111ll111_opy_)
    def bstack1lll1l11l1_opy_(self):
        with self._lock:
            return len(self._1lll1ll111l1_opy_) == 0
    def bstack111llll11_opy_(self):
        with self._lock:
            if self._1lll1ll111l1_opy_:
                bstack1lll1ll11ll1_opy_ = self._1lll1ll111l1_opy_.popleft()
                return bstack1lll1ll11ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll1ll11l1l_opy_
    def bstack1ll1l111l_opy_(self):
        with self._lock:
            self._1lll1ll11l1l_opy_ = True
    def bstack1lll1ll1l_opy_(self):
        with self._lock:
            self._1lll1ll11l1l_opy_ = False