# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1ll11l11l_opy_:
    def __init__(self):
        self._11111llllll_opy_ = deque()
        self._1111l11111l_opy_ = {}
        self._1111l111l1l_opy_ = False
        self._lock = threading.RLock()
    def bstack11111lll1ll_opy_(self, test_name, bstack1111l111111_opy_):
        with self._lock:
            bstack11111lllll1_opy_ = self._1111l11111l_opy_.get(test_name, {})
            return bstack11111lllll1_opy_.get(bstack1111l111111_opy_, 0)
    def bstack1111l111lll_opy_(self, test_name, bstack1111l111111_opy_):
        with self._lock:
            bstack11111llll1l_opy_ = self.bstack11111lll1ll_opy_(test_name, bstack1111l111111_opy_)
            self.bstack1111l1111l1_opy_(test_name, bstack1111l111111_opy_)
            return bstack11111llll1l_opy_
    def bstack1111l1111l1_opy_(self, test_name, bstack1111l111111_opy_):
        with self._lock:
            if test_name not in self._1111l11111l_opy_:
                self._1111l11111l_opy_[test_name] = {}
            bstack11111lllll1_opy_ = self._1111l11111l_opy_[test_name]
            bstack11111llll1l_opy_ = bstack11111lllll1_opy_.get(bstack1111l111111_opy_, 0)
            bstack11111lllll1_opy_[bstack1111l111111_opy_] = bstack11111llll1l_opy_ + 1
    def bstack1lll1111l_opy_(self, bstack11111llll11_opy_, bstack1111l111l11_opy_):
        bstack1111l1111ll_opy_ = self.bstack1111l111lll_opy_(bstack11111llll11_opy_, bstack1111l111l11_opy_)
        event_name = bstack11ll1111111_opy_[bstack1111l111l11_opy_]
        bstack1l1l1l11l11_opy_ = bstack111l111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢấ").format(bstack11111llll11_opy_, event_name, bstack1111l1111ll_opy_)
        with self._lock:
            self._11111llllll_opy_.append(bstack1l1l1l11l11_opy_)
    def bstack1l111llll_opy_(self):
        with self._lock:
            return len(self._11111llllll_opy_) == 0
    def bstack1l1l1111l_opy_(self):
        with self._lock:
            if self._11111llllll_opy_:
                bstack1111l111ll1_opy_ = self._11111llllll_opy_.popleft()
                return bstack1111l111ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1111l111l1l_opy_
    def bstack1111l1ll_opy_(self):
        with self._lock:
            self._1111l111l1l_opy_ = True
    def bstack1ll1ll111_opy_(self):
        with self._lock:
            self._1111l111l1l_opy_ = False