# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11l1lll1l1_opy_:
    def __init__(self):
        self._1111l11l11l_opy_ = deque()
        self._1111l1111l1_opy_ = {}
        self._11111llll1l_opy_ = False
        self._lock = threading.RLock()
    def bstack1111l111l1l_opy_(self, test_name, bstack1111l11111l_opy_):
        with self._lock:
            bstack1111l111111_opy_ = self._1111l1111l1_opy_.get(test_name, {})
            return bstack1111l111111_opy_.get(bstack1111l11111l_opy_, 0)
    def bstack1111l111lll_opy_(self, test_name, bstack1111l11111l_opy_):
        with self._lock:
            bstack1111l111ll1_opy_ = self.bstack1111l111l1l_opy_(test_name, bstack1111l11111l_opy_)
            self.bstack1111l11l111_opy_(test_name, bstack1111l11111l_opy_)
            return bstack1111l111ll1_opy_
    def bstack1111l11l111_opy_(self, test_name, bstack1111l11111l_opy_):
        with self._lock:
            if test_name not in self._1111l1111l1_opy_:
                self._1111l1111l1_opy_[test_name] = {}
            bstack1111l111111_opy_ = self._1111l1111l1_opy_[test_name]
            bstack1111l111ll1_opy_ = bstack1111l111111_opy_.get(bstack1111l11111l_opy_, 0)
            bstack1111l111111_opy_[bstack1111l11111l_opy_] = bstack1111l111ll1_opy_ + 1
    def bstack1l1ll1l111_opy_(self, bstack1111l111l11_opy_, bstack11111lllll1_opy_):
        bstack1111l1111ll_opy_ = self.bstack1111l111lll_opy_(bstack1111l111l11_opy_, bstack11111lllll1_opy_)
        event_name = bstack111llll1111_opy_[bstack11111lllll1_opy_]
        bstack1lll11ll1ll_opy_ = bstack11l1111_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥạ").format(bstack1111l111l11_opy_, event_name, bstack1111l1111ll_opy_)
        with self._lock:
            self._1111l11l11l_opy_.append(bstack1lll11ll1ll_opy_)
    def bstack11111l1ll_opy_(self):
        with self._lock:
            return len(self._1111l11l11l_opy_) == 0
    def bstack1llll111l_opy_(self):
        with self._lock:
            if self._1111l11l11l_opy_:
                bstack11111llllll_opy_ = self._1111l11l11l_opy_.popleft()
                return bstack11111llllll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._11111llll1l_opy_
    def bstack1lll1ll11_opy_(self):
        with self._lock:
            self._11111llll1l_opy_ = True
    def bstack1l1l11111_opy_(self):
        with self._lock:
            self._11111llll1l_opy_ = False