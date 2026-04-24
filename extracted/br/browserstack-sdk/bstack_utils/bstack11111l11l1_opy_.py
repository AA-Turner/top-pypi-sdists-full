# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack111lllll11_opy_:
    def __init__(self):
        self._1ll1l1l1ll11_opy_ = deque()
        self._1ll1l1l1lll1_opy_ = {}
        self._1ll1l1l1ll1l_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1l1ll1111_opy_(self, test_name, bstack1ll1l1l1l1ll_opy_):
        with self._lock:
            bstack1ll1l1ll111l_opy_ = self._1ll1l1l1lll1_opy_.get(test_name, {})
            return bstack1ll1l1ll111l_opy_.get(bstack1ll1l1l1l1ll_opy_, 0)
    def bstack1ll1l1l1l1l1_opy_(self, test_name, bstack1ll1l1l1l1ll_opy_):
        with self._lock:
            bstack1ll1l1l1l111_opy_ = self.bstack1ll1l1ll1111_opy_(test_name, bstack1ll1l1l1l1ll_opy_)
            self.bstack1ll1l1ll11l1_opy_(test_name, bstack1ll1l1l1l1ll_opy_)
            return bstack1ll1l1l1l111_opy_
    def bstack1ll1l1ll11l1_opy_(self, test_name, bstack1ll1l1l1l1ll_opy_):
        with self._lock:
            if test_name not in self._1ll1l1l1lll1_opy_:
                self._1ll1l1l1lll1_opy_[test_name] = {}
            bstack1ll1l1ll111l_opy_ = self._1ll1l1l1lll1_opy_[test_name]
            bstack1ll1l1l1l111_opy_ = bstack1ll1l1ll111l_opy_.get(bstack1ll1l1l1l1ll_opy_, 0)
            bstack1ll1l1ll111l_opy_[bstack1ll1l1l1l1ll_opy_] = bstack1ll1l1l1l111_opy_ + 1
    def bstack1111l1l1l1_opy_(self, bstack1ll1l1l1l11l_opy_, bstack1ll1l1l11lll_opy_):
        bstack1ll1l1l1llll_opy_ = self.bstack1ll1l1l1l1l1_opy_(bstack1ll1l1l1l11l_opy_, bstack1ll1l1l11lll_opy_)
        event_name = bstack11111l1llll_opy_[bstack1ll1l1l11lll_opy_]
        bstack11ll111l11l_opy_ = bstack111ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧ☡").format(bstack1ll1l1l1l11l_opy_, event_name, bstack1ll1l1l1llll_opy_)
        with self._lock:
            self._1ll1l1l1ll11_opy_.append(bstack11ll111l11l_opy_)
    def bstack111l111l1l_opy_(self):
        with self._lock:
            return len(self._1ll1l1l1ll11_opy_) == 0
    def bstack1111l1l1ll_opy_(self):
        with self._lock:
            if self._1ll1l1l1ll11_opy_:
                bstack1ll1l1l11ll1_opy_ = self._1ll1l1l1ll11_opy_.popleft()
                return bstack1ll1l1l11ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1l1l1ll1l_opy_
    def bstack1ll1llllll_opy_(self):
        with self._lock:
            self._1ll1l1l1ll1l_opy_ = True
    def bstack11l1lll11l_opy_(self):
        with self._lock:
            self._1ll1l1l1ll1l_opy_ = False