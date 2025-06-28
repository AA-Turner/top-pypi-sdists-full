# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack11ll1lll_opy_:
    def __init__(self):
        self._1111l111l11_opy_ = deque()
        self._1111l1111ll_opy_ = {}
        self._1111l11l111_opy_ = False
    def bstack1111l11l11l_opy_(self, test_name, bstack1111l111lll_opy_):
        bstack1111l11lll1_opy_ = self._1111l1111ll_opy_.get(test_name, {})
        return bstack1111l11lll1_opy_.get(bstack1111l111lll_opy_, 0)
    def bstack1111l11ll1l_opy_(self, test_name, bstack1111l111lll_opy_):
        bstack1111l11ll11_opy_ = self.bstack1111l11l11l_opy_(test_name, bstack1111l111lll_opy_)
        self.bstack1111l11l1l1_opy_(test_name, bstack1111l111lll_opy_)
        return bstack1111l11ll11_opy_
    def bstack1111l11l1l1_opy_(self, test_name, bstack1111l111lll_opy_):
        if test_name not in self._1111l1111ll_opy_:
            self._1111l1111ll_opy_[test_name] = {}
        bstack1111l11lll1_opy_ = self._1111l1111ll_opy_[test_name]
        bstack1111l11ll11_opy_ = bstack1111l11lll1_opy_.get(bstack1111l111lll_opy_, 0)
        bstack1111l11lll1_opy_[bstack1111l111lll_opy_] = bstack1111l11ll11_opy_ + 1
    def bstack1llllllll_opy_(self, bstack1111l111l1l_opy_, bstack1111l11l1ll_opy_):
        bstack1111l1111l1_opy_ = self.bstack1111l11ll1l_opy_(bstack1111l111l1l_opy_, bstack1111l11l1ll_opy_)
        event_name = bstack11l1ll11l1l_opy_[bstack1111l11l1ll_opy_]
        bstack1l1l1l1llll_opy_ = bstack1l1ll1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀ࠱ࢀࢃࠢṟ").format(bstack1111l111l1l_opy_, event_name, bstack1111l1111l1_opy_)
        self._1111l111l11_opy_.append(bstack1l1l1l1llll_opy_)
    def bstack1l1lllll1_opy_(self):
        return len(self._1111l111l11_opy_) == 0
    def bstack1lll111l_opy_(self):
        bstack1111l111ll1_opy_ = self._1111l111l11_opy_.popleft()
        return bstack1111l111ll1_opy_
    def capturing(self):
        return self._1111l11l111_opy_
    def bstack1l1l11llll_opy_(self):
        self._1111l11l111_opy_ = True
    def bstack1111l11l_opy_(self):
        self._1111l11l111_opy_ = False