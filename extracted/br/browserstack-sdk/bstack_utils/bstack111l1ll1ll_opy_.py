# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11l11l11_opy_:
    def __init__(self):
        self._1llll1l1l1l1_opy_ = deque()
        self._1llll1l1111l_opy_ = {}
        self._1llll1l11111_opy_ = False
        self._lock = threading.RLock()
    def bstack1llll1l11l1l_opy_(self, test_name, bstack1llll1l1ll11_opy_):
        with self._lock:
            bstack1llll1l1l111_opy_ = self._1llll1l1111l_opy_.get(test_name, {})
            return bstack1llll1l1l111_opy_.get(bstack1llll1l1ll11_opy_, 0)
    def bstack1llll1l1l1ll_opy_(self, test_name, bstack1llll1l1ll11_opy_):
        with self._lock:
            bstack1llll1l11ll1_opy_ = self.bstack1llll1l11l1l_opy_(test_name, bstack1llll1l1ll11_opy_)
            self.bstack1llll1l111ll_opy_(test_name, bstack1llll1l1ll11_opy_)
            return bstack1llll1l11ll1_opy_
    def bstack1llll1l111ll_opy_(self, test_name, bstack1llll1l1ll11_opy_):
        with self._lock:
            if test_name not in self._1llll1l1111l_opy_:
                self._1llll1l1111l_opy_[test_name] = {}
            bstack1llll1l1l111_opy_ = self._1llll1l1111l_opy_[test_name]
            bstack1llll1l11ll1_opy_ = bstack1llll1l1l111_opy_.get(bstack1llll1l1ll11_opy_, 0)
            bstack1llll1l1l111_opy_[bstack1llll1l1ll11_opy_] = bstack1llll1l11ll1_opy_ + 1
    def bstack11l11lll1_opy_(self, bstack1llll1l111l1_opy_, bstack1llll1l1l11l_opy_):
        bstack1llll1l11lll_opy_ = self.bstack1llll1l1l1ll_opy_(bstack1llll1l111l1_opy_, bstack1llll1l1l11l_opy_)
        event_name = bstack11l11111ll1_opy_[bstack1llll1l1l11l_opy_]
        bstack1l11l1l11ll_opy_ = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁ⃓ࠧ").format(bstack1llll1l111l1_opy_, event_name, bstack1llll1l11lll_opy_)
        with self._lock:
            self._1llll1l1l1l1_opy_.append(bstack1l11l1l11ll_opy_)
    def bstack11l1l1l11_opy_(self):
        with self._lock:
            return len(self._1llll1l1l1l1_opy_) == 0
    def bstack1l11llll11_opy_(self):
        with self._lock:
            if self._1llll1l1l1l1_opy_:
                bstack1llll1l11l11_opy_ = self._1llll1l1l1l1_opy_.popleft()
                return bstack1llll1l11l11_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1llll1l11111_opy_
    def bstack11l111l1_opy_(self):
        with self._lock:
            self._1llll1l11111_opy_ = True
    def bstack1l1l1l11l_opy_(self):
        with self._lock:
            self._1llll1l11111_opy_ = False