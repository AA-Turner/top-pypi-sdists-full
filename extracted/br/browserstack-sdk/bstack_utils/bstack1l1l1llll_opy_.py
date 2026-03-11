# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1ll1llll11_opy_:
    def __init__(self):
        self._1llll1ll11ll_opy_ = deque()
        self._1llll1ll1ll1_opy_ = {}
        self._1llll1ll1lll_opy_ = False
        self._lock = threading.RLock()
    def bstack1llll1llll11_opy_(self, test_name, bstack1llll1lll111_opy_):
        with self._lock:
            bstack1llll1lll11l_opy_ = self._1llll1ll1ll1_opy_.get(test_name, {})
            return bstack1llll1lll11l_opy_.get(bstack1llll1lll111_opy_, 0)
    def bstack1llll1ll1l11_opy_(self, test_name, bstack1llll1lll111_opy_):
        with self._lock:
            bstack1llll1ll1l1l_opy_ = self.bstack1llll1llll11_opy_(test_name, bstack1llll1lll111_opy_)
            self.bstack1llll1lll1ll_opy_(test_name, bstack1llll1lll111_opy_)
            return bstack1llll1ll1l1l_opy_
    def bstack1llll1lll1ll_opy_(self, test_name, bstack1llll1lll111_opy_):
        with self._lock:
            if test_name not in self._1llll1ll1ll1_opy_:
                self._1llll1ll1ll1_opy_[test_name] = {}
            bstack1llll1lll11l_opy_ = self._1llll1ll1ll1_opy_[test_name]
            bstack1llll1ll1l1l_opy_ = bstack1llll1lll11l_opy_.get(bstack1llll1lll111_opy_, 0)
            bstack1llll1lll11l_opy_[bstack1llll1lll111_opy_] = bstack1llll1ll1l1l_opy_ + 1
    def bstack1ll1l1lll_opy_(self, bstack1llll1lll1l1_opy_, bstack1llll1ll11l1_opy_):
        bstack1llll1l1llll_opy_ = self.bstack1llll1ll1l11_opy_(bstack1llll1lll1l1_opy_, bstack1llll1ll11l1_opy_)
        event_name = bstack1llll1ll111l_opy_[bstack1llll1ll11l1_opy_]
        bstack1l1111111ll_opy_ = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦḁ").format(bstack1llll1lll1l1_opy_, event_name, bstack1llll1l1llll_opy_)
        with self._lock:
            self._1llll1ll11ll_opy_.append(bstack1l1111111ll_opy_)
    def bstack11lll111_opy_(self):
        with self._lock:
            return len(self._1llll1ll11ll_opy_) == 0
    def bstack11ll1111l_opy_(self):
        with self._lock:
            if self._1llll1ll11ll_opy_:
                bstack1llll1ll1111_opy_ = self._1llll1ll11ll_opy_.popleft()
                return bstack1llll1ll1111_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1llll1ll1lll_opy_
    def bstack1111l111l1_opy_(self):
        with self._lock:
            self._1llll1ll1lll_opy_ = True
    def bstack1lll1l1l1l_opy_(self):
        with self._lock:
            self._1llll1ll1lll_opy_ = False