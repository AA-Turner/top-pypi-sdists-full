# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1111ll1l11_opy_:
    def __init__(self):
        self._1ll1l1lll1ll_opy_ = deque()
        self._1ll1l1ll1ll1_opy_ = {}
        self._1ll1l1ll1l1l_opy_ = False
        self._lock = threading.RLock()
    def bstack1ll1l1llll1l_opy_(self, test_name, bstack1ll1l1ll1l11_opy_):
        with self._lock:
            bstack1ll1l1lll11l_opy_ = self._1ll1l1ll1ll1_opy_.get(test_name, {})
            return bstack1ll1l1lll11l_opy_.get(bstack1ll1l1ll1l11_opy_, 0)
    def bstack1ll1l1lll1l1_opy_(self, test_name, bstack1ll1l1ll1l11_opy_):
        with self._lock:
            bstack1ll1l1ll111l_opy_ = self.bstack1ll1l1llll1l_opy_(test_name, bstack1ll1l1ll1l11_opy_)
            self.bstack1ll1l1lll111_opy_(test_name, bstack1ll1l1ll1l11_opy_)
            return bstack1ll1l1ll111l_opy_
    def bstack1ll1l1lll111_opy_(self, test_name, bstack1ll1l1ll1l11_opy_):
        with self._lock:
            if test_name not in self._1ll1l1ll1ll1_opy_:
                self._1ll1l1ll1ll1_opy_[test_name] = {}
            bstack1ll1l1lll11l_opy_ = self._1ll1l1ll1ll1_opy_[test_name]
            bstack1ll1l1ll111l_opy_ = bstack1ll1l1lll11l_opy_.get(bstack1ll1l1ll1l11_opy_, 0)
            bstack1ll1l1lll11l_opy_[bstack1ll1l1ll1l11_opy_] = bstack1ll1l1ll111l_opy_ + 1
    def bstack1lllll1lll1_opy_(self, bstack1ll1l1ll11ll_opy_, bstack1ll1l1ll11l1_opy_):
        bstack1ll1l1ll1lll_opy_ = self.bstack1ll1l1lll1l1_opy_(bstack1ll1l1ll11ll_opy_, bstack1ll1l1ll11l1_opy_)
        event_name = bstack1111111lll1_opy_[bstack1ll1l1ll11l1_opy_]
        bstack11ll111l111_opy_ = bstack1l111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢ☇").format(bstack1ll1l1ll11ll_opy_, event_name, bstack1ll1l1ll1lll_opy_)
        with self._lock:
            self._1ll1l1lll1ll_opy_.append(bstack11ll111l111_opy_)
    def bstack11111l1l_opy_(self):
        with self._lock:
            return len(self._1ll1l1lll1ll_opy_) == 0
    def bstack111ll1l11l_opy_(self):
        with self._lock:
            if self._1ll1l1lll1ll_opy_:
                bstack1ll1l1llll11_opy_ = self._1ll1l1lll1ll_opy_.popleft()
                return bstack1ll1l1llll11_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1ll1l1ll1l1l_opy_
    def bstack1ll1l1ll_opy_(self):
        with self._lock:
            self._1ll1l1ll1l1l_opy_ = True
    def bstack1l1ll11ll_opy_(self):
        with self._lock:
            self._1ll1l1ll1l1l_opy_ = False