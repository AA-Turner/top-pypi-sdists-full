# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11l1ll11ll_opy_:
    def __init__(self):
        self._111111lll1l_opy_ = deque()
        self._111111llll1_opy_ = {}
        self._111111ll1l1_opy_ = False
        self._lock = threading.RLock()
    def bstack111111ll11l_opy_(self, test_name, bstack111111l1l11_opy_):
        with self._lock:
            bstack111111l1l1l_opy_ = self._111111llll1_opy_.get(test_name, {})
            return bstack111111l1l1l_opy_.get(bstack111111l1l11_opy_, 0)
    def bstack111111l11ll_opy_(self, test_name, bstack111111l1l11_opy_):
        with self._lock:
            bstack111111l1lll_opy_ = self.bstack111111ll11l_opy_(test_name, bstack111111l1l11_opy_)
            self.bstack111111ll111_opy_(test_name, bstack111111l1l11_opy_)
            return bstack111111l1lll_opy_
    def bstack111111ll111_opy_(self, test_name, bstack111111l1l11_opy_):
        with self._lock:
            if test_name not in self._111111llll1_opy_:
                self._111111llll1_opy_[test_name] = {}
            bstack111111l1l1l_opy_ = self._111111llll1_opy_[test_name]
            bstack111111l1lll_opy_ = bstack111111l1l1l_opy_.get(bstack111111l1l11_opy_, 0)
            bstack111111l1l1l_opy_[bstack111111l1l11_opy_] = bstack111111l1lll_opy_ + 1
    def bstack111111l1_opy_(self, bstack111111lllll_opy_, bstack111111ll1ll_opy_):
        bstack111111lll11_opy_ = self.bstack111111l11ll_opy_(bstack111111lllll_opy_, bstack111111ll1ll_opy_)
        event_name = bstack11l1ll111ll_opy_[bstack111111ll1ll_opy_]
        bstack1l1l1l111ll_opy_ = bstack1111l1l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨἢ").format(bstack111111lllll_opy_, event_name, bstack111111lll11_opy_)
        with self._lock:
            self._111111lll1l_opy_.append(bstack1l1l1l111ll_opy_)
    def bstack1l1lll1l_opy_(self):
        with self._lock:
            return len(self._111111lll1l_opy_) == 0
    def bstack11lll11ll_opy_(self):
        with self._lock:
            if self._111111lll1l_opy_:
                bstack111111l1ll1_opy_ = self._111111lll1l_opy_.popleft()
                return bstack111111l1ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._111111ll1l1_opy_
    def bstack1lll11l1l1_opy_(self):
        with self._lock:
            self._111111ll1l1_opy_ = True
    def bstack1ll1ll1l1l_opy_(self):
        with self._lock:
            self._111111ll1l1_opy_ = False