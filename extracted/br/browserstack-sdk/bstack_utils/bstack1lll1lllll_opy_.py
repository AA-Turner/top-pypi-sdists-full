# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack111ll1111_opy_:
    def __init__(self):
        self._111111l1l11_opy_ = deque()
        self._111111l1lll_opy_ = {}
        self._111111l1l1l_opy_ = False
        self._lock = threading.RLock()
    def bstack111111ll11l_opy_(self, test_name, bstack111111l1ll1_opy_):
        with self._lock:
            bstack111111llll1_opy_ = self._111111l1lll_opy_.get(test_name, {})
            return bstack111111llll1_opy_.get(bstack111111l1ll1_opy_, 0)
    def bstack111111l11ll_opy_(self, test_name, bstack111111l1ll1_opy_):
        with self._lock:
            bstack111111ll1l1_opy_ = self.bstack111111ll11l_opy_(test_name, bstack111111l1ll1_opy_)
            self.bstack111111ll1ll_opy_(test_name, bstack111111l1ll1_opy_)
            return bstack111111ll1l1_opy_
    def bstack111111ll1ll_opy_(self, test_name, bstack111111l1ll1_opy_):
        with self._lock:
            if test_name not in self._111111l1lll_opy_:
                self._111111l1lll_opy_[test_name] = {}
            bstack111111llll1_opy_ = self._111111l1lll_opy_[test_name]
            bstack111111ll1l1_opy_ = bstack111111llll1_opy_.get(bstack111111l1ll1_opy_, 0)
            bstack111111llll1_opy_[bstack111111l1ll1_opy_] = bstack111111ll1l1_opy_ + 1
    def bstack11111111_opy_(self, bstack111111ll111_opy_, bstack111111l11l1_opy_):
        bstack111111lll11_opy_ = self.bstack111111l11ll_opy_(bstack111111ll111_opy_, bstack111111l11l1_opy_)
        event_name = bstack11l1lll111l_opy_[bstack111111l11l1_opy_]
        bstack1l1l1l11l1l_opy_ = bstack1l11ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦἠ").format(bstack111111ll111_opy_, event_name, bstack111111lll11_opy_)
        with self._lock:
            self._111111l1l11_opy_.append(bstack1l1l1l11l1l_opy_)
    def bstack11lll1l1l1_opy_(self):
        with self._lock:
            return len(self._111111l1l11_opy_) == 0
    def bstack1ll111l1ll_opy_(self):
        with self._lock:
            if self._111111l1l11_opy_:
                bstack111111lll1l_opy_ = self._111111l1l11_opy_.popleft()
                return bstack111111lll1l_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._111111l1l1l_opy_
    def bstack1ll1llll11_opy_(self):
        with self._lock:
            self._111111l1l1l_opy_ = True
    def bstack1llll1l1_opy_(self):
        with self._lock:
            self._111111l1l1l_opy_ = False