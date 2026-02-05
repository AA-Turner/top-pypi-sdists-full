# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l1l11l1_opy_:
    def __init__(self):
        self._1llll1l1l1l1_opy_ = deque()
        self._1llll1l11lll_opy_ = {}
        self._1llll1l1l111_opy_ = False
        self._lock = threading.RLock()
    def bstack1llll1l1lll1_opy_(self, test_name, bstack1llll1l1ll11_opy_):
        with self._lock:
            bstack1llll1ll1111_opy_ = self._1llll1l11lll_opy_.get(test_name, {})
            return bstack1llll1ll1111_opy_.get(bstack1llll1l1ll11_opy_, 0)
    def bstack1llll1l1ll1l_opy_(self, test_name, bstack1llll1l1ll11_opy_):
        with self._lock:
            bstack1llll1ll111l_opy_ = self.bstack1llll1l1lll1_opy_(test_name, bstack1llll1l1ll11_opy_)
            self.bstack1llll1ll11l1_opy_(test_name, bstack1llll1l1ll11_opy_)
            return bstack1llll1ll111l_opy_
    def bstack1llll1ll11l1_opy_(self, test_name, bstack1llll1l1ll11_opy_):
        with self._lock:
            if test_name not in self._1llll1l11lll_opy_:
                self._1llll1l11lll_opy_[test_name] = {}
            bstack1llll1ll1111_opy_ = self._1llll1l11lll_opy_[test_name]
            bstack1llll1ll111l_opy_ = bstack1llll1ll1111_opy_.get(bstack1llll1l1ll11_opy_, 0)
            bstack1llll1ll1111_opy_[bstack1llll1l1ll11_opy_] = bstack1llll1ll111l_opy_ + 1
    def bstack11l111ll1l_opy_(self, bstack1llll1l1l11l_opy_, bstack1llll1l1llll_opy_):
        bstack1llll1l1l1ll_opy_ = self.bstack1llll1l1ll1l_opy_(bstack1llll1l1l11l_opy_, bstack1llll1l1llll_opy_)
        event_name = bstack11l111ll1ll_opy_[bstack1llll1l1llll_opy_]
        bstack1l11l11llll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣ₳").format(bstack1llll1l1l11l_opy_, event_name, bstack1llll1l1l1ll_opy_)
        with self._lock:
            self._1llll1l1l1l1_opy_.append(bstack1l11l11llll_opy_)
    def bstack1llll111l1_opy_(self):
        with self._lock:
            return len(self._1llll1l1l1l1_opy_) == 0
    def bstack111l1l11ll_opy_(self):
        with self._lock:
            if self._1llll1l1l1l1_opy_:
                bstack1llll1l11ll1_opy_ = self._1llll1l1l1l1_opy_.popleft()
                return bstack1llll1l11ll1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1llll1l1l111_opy_
    def bstack1111111l_opy_(self):
        with self._lock:
            self._1llll1l1l111_opy_ = True
    def bstack1l1llllll1_opy_(self):
        with self._lock:
            self._1llll1l1l111_opy_ = False