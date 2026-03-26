# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack11l111l1ll_opy_:
    def __init__(self):
        self._1lll11l11l11_opy_ = deque()
        self._1lll11l1l11l_opy_ = {}
        self._1lll11l1l1l1_opy_ = False
        self._lock = threading.RLock()
    def bstack1lll11l11lll_opy_(self, test_name, bstack1lll11l111ll_opy_):
        with self._lock:
            bstack1lll11l1ll1l_opy_ = self._1lll11l1l11l_opy_.get(test_name, {})
            return bstack1lll11l1ll1l_opy_.get(bstack1lll11l111ll_opy_, 0)
    def bstack1lll11l1lll1_opy_(self, test_name, bstack1lll11l111ll_opy_):
        with self._lock:
            bstack1lll11l111l1_opy_ = self.bstack1lll11l11lll_opy_(test_name, bstack1lll11l111ll_opy_)
            self.bstack1lll11l11l1l_opy_(test_name, bstack1lll11l111ll_opy_)
            return bstack1lll11l111l1_opy_
    def bstack1lll11l11l1l_opy_(self, test_name, bstack1lll11l111ll_opy_):
        with self._lock:
            if test_name not in self._1lll11l1l11l_opy_:
                self._1lll11l1l11l_opy_[test_name] = {}
            bstack1lll11l1ll1l_opy_ = self._1lll11l1l11l_opy_[test_name]
            bstack1lll11l111l1_opy_ = bstack1lll11l1ll1l_opy_.get(bstack1lll11l111ll_opy_, 0)
            bstack1lll11l1ll1l_opy_[bstack1lll11l111ll_opy_] = bstack1lll11l111l1_opy_ + 1
    def bstack1lll1lll_opy_(self, bstack1lll11l1ll11_opy_, bstack1lll11l1l111_opy_):
        bstack1lll11l1l1ll_opy_ = self.bstack1lll11l1lll1_opy_(bstack1lll11l1ll11_opy_, bstack1lll11l1l111_opy_)
        event_name = bstack111l11l1l1l_opy_[bstack1lll11l1l111_opy_]
        bstack11llll1l111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤ␃").format(bstack1lll11l1ll11_opy_, event_name, bstack1lll11l1l1ll_opy_)
        with self._lock:
            self._1lll11l11l11_opy_.append(bstack11llll1l111_opy_)
    def bstack1111lll11_opy_(self):
        with self._lock:
            return len(self._1lll11l11l11_opy_) == 0
    def bstack11l1ll1l1_opy_(self):
        with self._lock:
            if self._1lll11l11l11_opy_:
                bstack1lll11l11ll1_opy_ = self._1lll11l11l11_opy_.popleft()
                return bstack1lll11l11ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1lll11l1l1l1_opy_
    def bstack11lll111l_opy_(self):
        with self._lock:
            self._1lll11l1l1l1_opy_ = True
    def bstack1llll11l11_opy_(self):
        with self._lock:
            self._1lll11l1l1l1_opy_ = False