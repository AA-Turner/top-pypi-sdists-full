# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1lll1111ll_opy_:
    def __init__(self):
        self._111ll1111ll_opy_ = deque()
        self._111ll11111l_opy_ = {}
        self._111ll111111_opy_ = False
    def bstack111ll111l1l_opy_(self, test_name, bstack111ll11l11l_opy_):
        bstack111ll11l111_opy_ = self._111ll11111l_opy_.get(test_name, {})
        return bstack111ll11l111_opy_.get(bstack111ll11l11l_opy_, 0)
    def bstack111ll111lll_opy_(self, test_name, bstack111ll11l11l_opy_):
        bstack111ll1111l1_opy_ = self.bstack111ll111l1l_opy_(test_name, bstack111ll11l11l_opy_)
        self.bstack111l1llll1l_opy_(test_name, bstack111ll11l11l_opy_)
        return bstack111ll1111l1_opy_
    def bstack111l1llll1l_opy_(self, test_name, bstack111ll11l11l_opy_):
        if test_name not in self._111ll11111l_opy_:
            self._111ll11111l_opy_[test_name] = {}
        bstack111ll11l111_opy_ = self._111ll11111l_opy_[test_name]
        bstack111ll1111l1_opy_ = bstack111ll11l111_opy_.get(bstack111ll11l11l_opy_, 0)
        bstack111ll11l111_opy_[bstack111ll11l11l_opy_] = bstack111ll1111l1_opy_ + 1
    def bstack1l1l111111_opy_(self, bstack111ll111l11_opy_, bstack111ll111ll1_opy_):
        bstack111l1lllll1_opy_ = self.bstack111ll111lll_opy_(bstack111ll111l11_opy_, bstack111ll111ll1_opy_)
        event_name = bstack11ll11lll1l_opy_[bstack111ll111ll1_opy_]
        bstack1l1ll1l11l1_opy_ = bstack11lll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾ࠯ࡾࢁࠧᴍ").format(bstack111ll111l11_opy_, event_name, bstack111l1lllll1_opy_)
        self._111ll1111ll_opy_.append(bstack1l1ll1l11l1_opy_)
    def bstack11l11l1l1_opy_(self):
        return len(self._111ll1111ll_opy_) == 0
    def bstack1l11l1ll_opy_(self):
        bstack111l1llllll_opy_ = self._111ll1111ll_opy_.popleft()
        return bstack111l1llllll_opy_
    def capturing(self):
        return self._111ll111111_opy_
    def bstack1ll1llll1l_opy_(self):
        self._111ll111111_opy_ = True
    def bstack11l11lll_opy_(self):
        self._111ll111111_opy_ = False