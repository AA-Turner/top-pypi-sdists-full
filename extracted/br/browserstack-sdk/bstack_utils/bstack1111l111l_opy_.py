# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1l11lll1l1_opy_:
    def __init__(self):
        self._1111l11l1ll_opy_ = deque()
        self._1111l11l1l1_opy_ = {}
        self._1111l11ll1l_opy_ = False
    def bstack1111l11llll_opy_(self, test_name, bstack1111l11l11l_opy_):
        bstack1111l1l111l_opy_ = self._1111l11l1l1_opy_.get(test_name, {})
        return bstack1111l1l111l_opy_.get(bstack1111l11l11l_opy_, 0)
    def bstack1111l1l1111_opy_(self, test_name, bstack1111l11l11l_opy_):
        bstack1111l1l11ll_opy_ = self.bstack1111l11llll_opy_(test_name, bstack1111l11l11l_opy_)
        self.bstack1111l11l111_opy_(test_name, bstack1111l11l11l_opy_)
        return bstack1111l1l11ll_opy_
    def bstack1111l11l111_opy_(self, test_name, bstack1111l11l11l_opy_):
        if test_name not in self._1111l11l1l1_opy_:
            self._1111l11l1l1_opy_[test_name] = {}
        bstack1111l1l111l_opy_ = self._1111l11l1l1_opy_[test_name]
        bstack1111l1l11ll_opy_ = bstack1111l1l111l_opy_.get(bstack1111l11l11l_opy_, 0)
        bstack1111l1l111l_opy_[bstack1111l11l11l_opy_] = bstack1111l1l11ll_opy_ + 1
    def bstack1l1111l111_opy_(self, bstack1111l1l1l11_opy_, bstack1111l1l11l1_opy_):
        bstack1111l11ll11_opy_ = self.bstack1111l1l1111_opy_(bstack1111l1l1l11_opy_, bstack1111l1l11l1_opy_)
        event_name = bstack11ll111lll1_opy_[bstack1111l1l11l1_opy_]
        bstack1l1l1lll1l1_opy_ = bstack11ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤḾ").format(bstack1111l1l1l11_opy_, event_name, bstack1111l11ll11_opy_)
        self._1111l11l1ll_opy_.append(bstack1l1l1lll1l1_opy_)
    def bstack11l11l1ll1_opy_(self):
        return len(self._1111l11l1ll_opy_) == 0
    def bstack1l1111ll_opy_(self):
        bstack1111l11lll1_opy_ = self._1111l11l1ll_opy_.popleft()
        return bstack1111l11lll1_opy_
    def capturing(self):
        return self._1111l11ll1l_opy_
    def bstack1ll11lll1l_opy_(self):
        self._1111l11ll1l_opy_ = True
    def bstack11l11111_opy_(self):
        self._1111l11ll1l_opy_ = False