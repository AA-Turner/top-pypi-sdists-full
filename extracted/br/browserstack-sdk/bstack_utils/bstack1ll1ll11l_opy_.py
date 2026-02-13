# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack111lll111_opy_:
    def __init__(self):
        self._1lll1lll1111_opy_ = deque()
        self._1lll1lll11l1_opy_ = {}
        self._1lll1ll1llll_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll1lll11ll_opy_(self, test_name, bstack1lll1ll1ll1l_opy_):
        with self._lock:
            bstack1lll1llll111_opy_ = self._1lll1lll11l1_opy_.get(test_name, {})
            return bstack1lll1llll111_opy_.get(bstack1lll1ll1ll1l_opy_, 0)
    def bstack1lll1ll1ll11_opy_(self, test_name, bstack1lll1ll1ll1l_opy_):
        with self._lock:
            bstack1lll1lll111l_opy_ = self.bstack1lll1lll11ll_opy_(test_name, bstack1lll1ll1ll1l_opy_)
            self.bstack1lll1ll1lll1_opy_(test_name, bstack1lll1ll1ll1l_opy_)
            return bstack1lll1lll111l_opy_
    def bstack1lll1ll1lll1_opy_(self, test_name, bstack1lll1ll1ll1l_opy_):
        with self._lock:
            if test_name not in self._1lll1lll11l1_opy_:
                self._1lll1lll11l1_opy_[test_name] = {}
            bstack1lll1llll111_opy_ = self._1lll1lll11l1_opy_[test_name]
            bstack1lll1lll111l_opy_ = bstack1lll1llll111_opy_.get(bstack1lll1ll1ll1l_opy_, 0)
            bstack1lll1llll111_opy_[bstack1lll1ll1ll1l_opy_] = bstack1lll1lll111l_opy_ + 1
    def bstack11l1l1ll1l_opy_(self, bstack1lll1lll1lll_opy_, bstack1lll1lll1l1l_opy_):
        bstack1lll1lll1l11_opy_ = self.bstack1lll1ll1ll11_opy_(bstack1lll1lll1lll_opy_, bstack1lll1lll1l1l_opy_)
        event_name = bstack111ll1l111l_opy_[bstack1lll1lll1l1l_opy_]
        bstack1l1111lll11_opy_ = bstack11l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨ↟").format(bstack1lll1lll1lll_opy_, event_name, bstack1lll1lll1l11_opy_)
        with self._lock:
            self._1lll1lll1111_opy_.append(bstack1l1111lll11_opy_)
    def bstack1111l1l1_opy_(self):
        with self._lock:
            return len(self._1lll1lll1111_opy_) == 0
    def bstack1111l11l_opy_(self):
        with self._lock:
            if self._1lll1lll1111_opy_:
                bstack1lll1lll1ll1_opy_ = self._1lll1lll1111_opy_.popleft()
                return bstack1lll1lll1ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll1ll1llll_opy_
    def bstack11l11l1l1l_opy_(self):
        with self._lock:
            self._1lll1ll1llll_opy_ = True
    def bstack11111ll1_opy_(self):
        with self._lock:
            self._1lll1ll1llll_opy_ = False