# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l11111l_opy_:
    def __init__(self):
        self._1lll11l11l11_opy_ = deque()
        self._1lll11l1l1l1_opy_ = {}
        self._1lll11l1ll11_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll11l11lll_opy_(self, test_name, bstack1lll11l11l1l_opy_):
        with self._lock:
            bstack1lll11l1l111_opy_ = self._1lll11l1l1l1_opy_.get(test_name, {})
            return bstack1lll11l1l111_opy_.get(bstack1lll11l11l1l_opy_, 0)
    def bstack1lll11l11111_opy_(self, test_name, bstack1lll11l11l1l_opy_):
        with self._lock:
            bstack1lll11l11ll1_opy_ = self.bstack1lll11l11lll_opy_(test_name, bstack1lll11l11l1l_opy_)
            self.bstack1lll11l111l1_opy_(test_name, bstack1lll11l11l1l_opy_)
            return bstack1lll11l11ll1_opy_
    def bstack1lll11l111l1_opy_(self, test_name, bstack1lll11l11l1l_opy_):
        with self._lock:
            if test_name not in self._1lll11l1l1l1_opy_:
                self._1lll11l1l1l1_opy_[test_name] = {}
            bstack1lll11l1l111_opy_ = self._1lll11l1l1l1_opy_[test_name]
            bstack1lll11l11ll1_opy_ = bstack1lll11l1l111_opy_.get(bstack1lll11l11l1l_opy_, 0)
            bstack1lll11l1l111_opy_[bstack1lll11l11l1l_opy_] = bstack1lll11l11ll1_opy_ + 1
    def bstack1llll11ll_opy_(self, bstack1lll11l1111l_opy_, bstack1lll11l111ll_opy_):
        bstack1lll11l1l11l_opy_ = self.bstack1lll11l11111_opy_(bstack1lll11l1111l_opy_, bstack1lll11l111ll_opy_)
        event_name = bstack111l11l1111_opy_[bstack1lll11l111ll_opy_]
        bstack11llll1111l_opy_ = bstack1ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧ␔").format(bstack1lll11l1111l_opy_, event_name, bstack1lll11l1l11l_opy_)
        with self._lock:
            self._1lll11l11l11_opy_.append(bstack11llll1111l_opy_)
    def bstack1llll1ll11_opy_(self):
        with self._lock:
            return len(self._1lll11l11l11_opy_) == 0
    def bstack11lllll11l_opy_(self):
        with self._lock:
            if self._1lll11l11l11_opy_:
                bstack1lll11l1l1ll_opy_ = self._1lll11l11l11_opy_.popleft()
                return bstack1lll11l1l1ll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll11l1ll11_opy_
    def bstack1l11ll11ll_opy_(self):
        with self._lock:
            self._1lll11l1ll11_opy_ = True
    def bstack11l1l1llll_opy_(self):
        with self._lock:
            self._1lll11l1ll11_opy_ = False