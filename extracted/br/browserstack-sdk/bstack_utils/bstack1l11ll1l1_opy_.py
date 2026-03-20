# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11111ll111_opy_:
    def __init__(self):
        self._1lll11ll11l1_opy_ = deque()
        self._1lll11ll1ll1_opy_ = {}
        self._1lll11ll111l_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll11ll1l11_opy_(self, test_name, bstack1lll11ll1l1l_opy_):
        with self._lock:
            bstack1lll11lll111_opy_ = self._1lll11ll1ll1_opy_.get(test_name, {})
            return bstack1lll11lll111_opy_.get(bstack1lll11ll1l1l_opy_, 0)
    def bstack1lll11ll1111_opy_(self, test_name, bstack1lll11ll1l1l_opy_):
        with self._lock:
            bstack1lll11ll11ll_opy_ = self.bstack1lll11ll1l11_opy_(test_name, bstack1lll11ll1l1l_opy_)
            self.bstack1lll11l1lll1_opy_(test_name, bstack1lll11ll1l1l_opy_)
            return bstack1lll11ll11ll_opy_
    def bstack1lll11l1lll1_opy_(self, test_name, bstack1lll11ll1l1l_opy_):
        with self._lock:
            if test_name not in self._1lll11ll1ll1_opy_:
                self._1lll11ll1ll1_opy_[test_name] = {}
            bstack1lll11lll111_opy_ = self._1lll11ll1ll1_opy_[test_name]
            bstack1lll11ll11ll_opy_ = bstack1lll11lll111_opy_.get(bstack1lll11ll1l1l_opy_, 0)
            bstack1lll11lll111_opy_[bstack1lll11ll1l1l_opy_] = bstack1lll11ll11ll_opy_ + 1
    def bstack11111llll_opy_(self, bstack1lll11ll1lll_opy_, bstack1lll11lll11l_opy_):
        bstack1lll11lll1l1_opy_ = self.bstack1lll11ll1111_opy_(bstack1lll11ll1lll_opy_, bstack1lll11lll11l_opy_)
        event_name = bstack111l11l1111_opy_[bstack1lll11lll11l_opy_]
        bstack11lllll11ll_opy_ = bstack11lll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧ⏜").format(bstack1lll11ll1lll_opy_, event_name, bstack1lll11lll1l1_opy_)
        with self._lock:
            self._1lll11ll11l1_opy_.append(bstack11lllll11ll_opy_)
    def bstack1ll1ll111_opy_(self):
        with self._lock:
            return len(self._1lll11ll11l1_opy_) == 0
    def bstack11lll11l_opy_(self):
        with self._lock:
            if self._1lll11ll11l1_opy_:
                bstack1lll11l1llll_opy_ = self._1lll11ll11l1_opy_.popleft()
                return bstack1lll11l1llll_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll11ll111l_opy_
    def bstack1l1l11l11l_opy_(self):
        with self._lock:
            self._1lll11ll111l_opy_ = True
    def bstack1l11111l_opy_(self):
        with self._lock:
            self._1lll11ll111l_opy_ = False