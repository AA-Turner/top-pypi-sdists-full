# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import threading
from collections import deque
from bstack_utils.constants import *
class bstack1l1l111l_opy_:
    def __init__(self):
        self._1111111ll1l_opy_ = deque()
        self._111111l1111_opy_ = {}
        self._1111111l111_opy_ = False
        self._lock = threading.RLock()
    def bstack111111l11ll_opy_(self, test_name, bstack111111l111l_opy_):
        with self._lock:
            bstack1111111l11l_opy_ = self._111111l1111_opy_.get(test_name, {})
            return bstack1111111l11l_opy_.get(bstack111111l111l_opy_, 0)
    def bstack1111111lll1_opy_(self, test_name, bstack111111l111l_opy_):
        with self._lock:
            bstack1111111ll11_opy_ = self.bstack111111l11ll_opy_(test_name, bstack111111l111l_opy_)
            self.bstack1111111llll_opy_(test_name, bstack111111l111l_opy_)
            return bstack1111111ll11_opy_
    def bstack1111111llll_opy_(self, test_name, bstack111111l111l_opy_):
        with self._lock:
            if test_name not in self._111111l1111_opy_:
                self._111111l1111_opy_[test_name] = {}
            bstack1111111l11l_opy_ = self._111111l1111_opy_[test_name]
            bstack1111111ll11_opy_ = bstack1111111l11l_opy_.get(bstack111111l111l_opy_, 0)
            bstack1111111l11l_opy_[bstack111111l111l_opy_] = bstack1111111ll11_opy_ + 1
    def bstack1111111ll_opy_(self, bstack11111111lll_opy_, bstack1111111l1ll_opy_):
        bstack1111111l1l1_opy_ = self.bstack1111111lll1_opy_(bstack11111111lll_opy_, bstack1111111l1ll_opy_)
        event_name = bstack11l1l1lll11_opy_[bstack1111111l1ll_opy_]
        bstack1l1l11llll1_opy_ = bstack1ll11ll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥἦ").format(bstack11111111lll_opy_, event_name, bstack1111111l1l1_opy_)
        with self._lock:
            self._1111111ll1l_opy_.append(bstack1l1l11llll1_opy_)
    def bstack111llll111_opy_(self):
        with self._lock:
            return len(self._1111111ll1l_opy_) == 0
    def bstack1ll1111111_opy_(self):
        with self._lock:
            if self._1111111ll1l_opy_:
                bstack111111l11l1_opy_ = self._1111111ll1l_opy_.popleft()
                return bstack111111l11l1_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1111111l111_opy_
    def bstack1l11l11l_opy_(self):
        with self._lock:
            self._1111111l111_opy_ = True
    def bstack1ll11l1l1_opy_(self):
        with self._lock:
            self._1111111l111_opy_ = False