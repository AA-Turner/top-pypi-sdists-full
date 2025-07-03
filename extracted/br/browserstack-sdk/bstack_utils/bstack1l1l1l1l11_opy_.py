# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1ll1111l11_opy_:
    def __init__(self):
        self._11111lllll1_opy_ = deque()
        self._11111llll1l_opy_ = {}
        self._1111l111l11_opy_ = False
        self._lock = threading.RLock()
    def bstack1111l11111l_opy_(self, test_name, bstack1111l111lll_opy_):
        with self._lock:
            bstack11111llllll_opy_ = self._11111llll1l_opy_.get(test_name, {})
            return bstack11111llllll_opy_.get(bstack1111l111lll_opy_, 0)
    def bstack1111l11l111_opy_(self, test_name, bstack1111l111lll_opy_):
        with self._lock:
            bstack1111l111l1l_opy_ = self.bstack1111l11111l_opy_(test_name, bstack1111l111lll_opy_)
            self.bstack1111l1111l1_opy_(test_name, bstack1111l111lll_opy_)
            return bstack1111l111l1l_opy_
    def bstack1111l1111l1_opy_(self, test_name, bstack1111l111lll_opy_):
        with self._lock:
            if test_name not in self._11111llll1l_opy_:
                self._11111llll1l_opy_[test_name] = {}
            bstack11111llllll_opy_ = self._11111llll1l_opy_[test_name]
            bstack1111l111l1l_opy_ = bstack11111llllll_opy_.get(bstack1111l111lll_opy_, 0)
            bstack11111llllll_opy_[bstack1111l111lll_opy_] = bstack1111l111l1l_opy_ + 1
    def bstack1lllllllll_opy_(self, bstack1111l11l11l_opy_, bstack1111l111ll1_opy_):
        bstack1111l1111ll_opy_ = self.bstack1111l11l111_opy_(bstack1111l11l11l_opy_, bstack1111l111ll1_opy_)
        event_name = bstack11l1ll11ll1_opy_[bstack1111l111ll1_opy_]
        bstack1l1l1l111l1_opy_ = bstack1l1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣẟ").format(bstack1111l11l11l_opy_, event_name, bstack1111l1111ll_opy_)
        with self._lock:
            self._11111lllll1_opy_.append(bstack1l1l1l111l1_opy_)
    def bstack1ll1l1l111_opy_(self):
        with self._lock:
            return len(self._11111lllll1_opy_) == 0
    def bstack1l1ll1111l_opy_(self):
        with self._lock:
            if self._11111lllll1_opy_:
                bstack1111l111111_opy_ = self._11111lllll1_opy_.popleft()
                return bstack1111l111111_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1111l111l11_opy_
    def bstack1lll11111_opy_(self):
        with self._lock:
            self._1111l111l11_opy_ = True
    def bstack11l1l111_opy_(self):
        with self._lock:
            self._1111l111l11_opy_ = False