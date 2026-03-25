# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11l1ll1l1l_opy_:
    def __init__(self):
        self._1lll11ll111l_opy_ = deque()
        self._1lll11ll1l11_opy_ = {}
        self._1lll11l1lll1_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll11l1l1ll_opy_(self, test_name, bstack1lll11ll1l1l_opy_):
        with self._lock:
            bstack1lll11ll11ll_opy_ = self._1lll11ll1l11_opy_.get(test_name, {})
            return bstack1lll11ll11ll_opy_.get(bstack1lll11ll1l1l_opy_, 0)
    def bstack1lll11l1llll_opy_(self, test_name, bstack1lll11ll1l1l_opy_):
        with self._lock:
            bstack1lll11l1ll11_opy_ = self.bstack1lll11l1l1ll_opy_(test_name, bstack1lll11ll1l1l_opy_)
            self.bstack1lll11l1ll1l_opy_(test_name, bstack1lll11ll1l1l_opy_)
            return bstack1lll11l1ll11_opy_
    def bstack1lll11l1ll1l_opy_(self, test_name, bstack1lll11ll1l1l_opy_):
        with self._lock:
            if test_name not in self._1lll11ll1l11_opy_:
                self._1lll11ll1l11_opy_[test_name] = {}
            bstack1lll11ll11ll_opy_ = self._1lll11ll1l11_opy_[test_name]
            bstack1lll11l1ll11_opy_ = bstack1lll11ll11ll_opy_.get(bstack1lll11ll1l1l_opy_, 0)
            bstack1lll11ll11ll_opy_[bstack1lll11ll1l1l_opy_] = bstack1lll11l1ll11_opy_ + 1
    def bstack1l1lllll_opy_(self, bstack1lll11ll1111_opy_, bstack1lll11l1l1l1_opy_):
        bstack1lll11ll11l1_opy_ = self.bstack1lll11l1llll_opy_(bstack1lll11ll1111_opy_, bstack1lll11l1l1l1_opy_)
        event_name = bstack111l1l11111_opy_[bstack1lll11l1l1l1_opy_]
        bstack11llll1ll11_opy_ = bstack1l1_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤ⏧").format(bstack1lll11ll1111_opy_, event_name, bstack1lll11ll11l1_opy_)
        with self._lock:
            self._1lll11ll111l_opy_.append(bstack11llll1ll11_opy_)
    def bstack1l1l1l1l1l_opy_(self):
        with self._lock:
            return len(self._1lll11ll111l_opy_) == 0
    def bstack11ll1lll11_opy_(self):
        with self._lock:
            if self._1lll11ll111l_opy_:
                bstack1lll11ll1ll1_opy_ = self._1lll11ll111l_opy_.popleft()
                return bstack1lll11ll1ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll11l1lll1_opy_
    def bstack111l11l1l_opy_(self):
        with self._lock:
            self._1lll11l1lll1_opy_ = True
    def bstack1lllll1ll_opy_(self):
        with self._lock:
            self._1lll11l1lll1_opy_ = False