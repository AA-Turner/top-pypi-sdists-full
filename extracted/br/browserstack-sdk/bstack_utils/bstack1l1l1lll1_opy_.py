# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack111111l1_opy_:
    def __init__(self):
        self._1111l1l1111_opy_ = deque()
        self._1111l11l111_opy_ = {}
        self._1111l11l1l1_opy_ = False
    def bstack1111l11ll11_opy_(self, test_name, bstack1111l1l11ll_opy_):
        bstack1111l11lll1_opy_ = self._1111l11l111_opy_.get(test_name, {})
        return bstack1111l11lll1_opy_.get(bstack1111l1l11ll_opy_, 0)
    def bstack1111l1l11l1_opy_(self, test_name, bstack1111l1l11ll_opy_):
        bstack1111l11llll_opy_ = self.bstack1111l11ll11_opy_(test_name, bstack1111l1l11ll_opy_)
        self.bstack1111l1l1l11_opy_(test_name, bstack1111l1l11ll_opy_)
        return bstack1111l11llll_opy_
    def bstack1111l1l1l11_opy_(self, test_name, bstack1111l1l11ll_opy_):
        if test_name not in self._1111l11l111_opy_:
            self._1111l11l111_opy_[test_name] = {}
        bstack1111l11lll1_opy_ = self._1111l11l111_opy_[test_name]
        bstack1111l11llll_opy_ = bstack1111l11lll1_opy_.get(bstack1111l1l11ll_opy_, 0)
        bstack1111l11lll1_opy_[bstack1111l1l11ll_opy_] = bstack1111l11llll_opy_ + 1
    def bstack1l11l11l1_opy_(self, bstack1111l1l111l_opy_, bstack1111l11ll1l_opy_):
        bstack1111l11l11l_opy_ = self.bstack1111l1l11l1_opy_(bstack1111l1l111l_opy_, bstack1111l11ll1l_opy_)
        event_name = bstack11l1ll1llll_opy_[bstack1111l11ll1l_opy_]
        bstack1l1l1lll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥḿ").format(bstack1111l1l111l_opy_, event_name, bstack1111l11l11l_opy_)
        self._1111l1l1111_opy_.append(bstack1l1l1lll11l_opy_)
    def bstack11l111ll_opy_(self):
        return len(self._1111l1l1111_opy_) == 0
    def bstack11ll1l1lll_opy_(self):
        bstack1111l11l1ll_opy_ = self._1111l1l1111_opy_.popleft()
        return bstack1111l11l1ll_opy_
    def capturing(self):
        return self._1111l11l1l1_opy_
    def bstack1l1l1l1l11_opy_(self):
        self._1111l11l1l1_opy_ = True
    def bstack11111l1ll_opy_(self):
        self._1111l11l1l1_opy_ = False