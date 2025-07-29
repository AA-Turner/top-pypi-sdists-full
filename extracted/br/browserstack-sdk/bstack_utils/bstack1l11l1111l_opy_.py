# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11llll1lll_opy_:
    def __init__(self):
        self._1111l111l11_opy_ = deque()
        self._11111llll11_opy_ = {}
        self._1111l1111ll_opy_ = False
        self._lock = threading.RLock()
    def bstack11111llllll_opy_(self, test_name, bstack1111l111111_opy_):
        with self._lock:
            bstack1111l1111l1_opy_ = self._11111llll11_opy_.get(test_name, {})
            return bstack1111l1111l1_opy_.get(bstack1111l111111_opy_, 0)
    def bstack11111llll1l_opy_(self, test_name, bstack1111l111111_opy_):
        with self._lock:
            bstack11111lll1l1_opy_ = self.bstack11111llllll_opy_(test_name, bstack1111l111111_opy_)
            self.bstack1111l11111l_opy_(test_name, bstack1111l111111_opy_)
            return bstack11111lll1l1_opy_
    def bstack1111l11111l_opy_(self, test_name, bstack1111l111111_opy_):
        with self._lock:
            if test_name not in self._11111llll11_opy_:
                self._11111llll11_opy_[test_name] = {}
            bstack1111l1111l1_opy_ = self._11111llll11_opy_[test_name]
            bstack11111lll1l1_opy_ = bstack1111l1111l1_opy_.get(bstack1111l111111_opy_, 0)
            bstack1111l1111l1_opy_[bstack1111l111111_opy_] = bstack11111lll1l1_opy_ + 1
    def bstack1llll11l1_opy_(self, bstack1111l111ll1_opy_, bstack11111lll1ll_opy_):
        bstack1111l111l1l_opy_ = self.bstack11111llll1l_opy_(bstack1111l111ll1_opy_, bstack11111lll1ll_opy_)
        event_name = bstack11l1lll1ll1_opy_[bstack11111lll1ll_opy_]
        bstack1l1l1l11l11_opy_ = bstackl_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣẦ").format(bstack1111l111ll1_opy_, event_name, bstack1111l111l1l_opy_)
        with self._lock:
            self._1111l111l11_opy_.append(bstack1l1l1l11l11_opy_)
    def bstack11lll1ll1l_opy_(self):
        with self._lock:
            return len(self._1111l111l11_opy_) == 0
    def bstack11lllll1_opy_(self):
        with self._lock:
            if self._1111l111l11_opy_:
                bstack11111lllll1_opy_ = self._1111l111l11_opy_.popleft()
                return bstack11111lllll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1111l1111ll_opy_
    def bstack11l11ll1l_opy_(self):
        with self._lock:
            self._1111l1111ll_opy_ = True
    def bstack11ll1llll1_opy_(self):
        with self._lock:
            self._1111l1111ll_opy_ = False