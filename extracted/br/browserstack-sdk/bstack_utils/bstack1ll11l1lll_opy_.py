# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11l111ll1_opy_:
    def __init__(self):
        self._111111lllll_opy_ = deque()
        self._11111l11111_opy_ = {}
        self._11111l1111l_opy_ = False
        self._lock = threading.RLock()
    def bstack111111ll1ll_opy_(self, test_name, bstack11111l111l1_opy_):
        with self._lock:
            bstack111111ll1l1_opy_ = self._11111l11111_opy_.get(test_name, {})
            return bstack111111ll1l1_opy_.get(bstack11111l111l1_opy_, 0)
    def bstack111111lll11_opy_(self, test_name, bstack11111l111l1_opy_):
        with self._lock:
            bstack111111lll1l_opy_ = self.bstack111111ll1ll_opy_(test_name, bstack11111l111l1_opy_)
            self.bstack111111ll111_opy_(test_name, bstack11111l111l1_opy_)
            return bstack111111lll1l_opy_
    def bstack111111ll111_opy_(self, test_name, bstack11111l111l1_opy_):
        with self._lock:
            if test_name not in self._11111l11111_opy_:
                self._11111l11111_opy_[test_name] = {}
            bstack111111ll1l1_opy_ = self._11111l11111_opy_[test_name]
            bstack111111lll1l_opy_ = bstack111111ll1l1_opy_.get(bstack11111l111l1_opy_, 0)
            bstack111111ll1l1_opy_[bstack11111l111l1_opy_] = bstack111111lll1l_opy_ + 1
    def bstack11l11lllll_opy_(self, bstack11111l111ll_opy_, bstack111111ll11l_opy_):
        bstack11111l11l11_opy_ = self.bstack111111lll11_opy_(bstack11111l111ll_opy_, bstack111111ll11l_opy_)
        event_name = bstack11l1ll1l1ll_opy_[bstack111111ll11l_opy_]
        bstack1l1l1l11ll1_opy_ = bstack1111lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣἝ").format(bstack11111l111ll_opy_, event_name, bstack11111l11l11_opy_)
        with self._lock:
            self._111111lllll_opy_.append(bstack1l1l1l11ll1_opy_)
    def bstack111ll111_opy_(self):
        with self._lock:
            return len(self._111111lllll_opy_) == 0
    def bstack111llll1_opy_(self):
        with self._lock:
            if self._111111lllll_opy_:
                bstack111111llll1_opy_ = self._111111lllll_opy_.popleft()
                return bstack111111llll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._11111l1111l_opy_
    def bstack1l111111l_opy_(self):
        with self._lock:
            self._11111l1111l_opy_ = True
    def bstack11lll11lll_opy_(self):
        with self._lock:
            self._11111l1111l_opy_ = False