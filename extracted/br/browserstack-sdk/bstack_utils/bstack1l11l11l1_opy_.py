# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack11l111lll_opy_:
    def __init__(self):
        self._111ll111ll1_opy_ = deque()
        self._111ll111111_opy_ = {}
        self._111ll111lll_opy_ = False
    def bstack111ll1111l1_opy_(self, test_name, bstack111ll11l1l1_opy_):
        bstack111l1llllll_opy_ = self._111ll111111_opy_.get(test_name, {})
        return bstack111l1llllll_opy_.get(bstack111ll11l1l1_opy_, 0)
    def bstack111ll11l11l_opy_(self, test_name, bstack111ll11l1l1_opy_):
        bstack111ll111l1l_opy_ = self.bstack111ll1111l1_opy_(test_name, bstack111ll11l1l1_opy_)
        self.bstack111ll11111l_opy_(test_name, bstack111ll11l1l1_opy_)
        return bstack111ll111l1l_opy_
    def bstack111ll11111l_opy_(self, test_name, bstack111ll11l1l1_opy_):
        if test_name not in self._111ll111111_opy_:
            self._111ll111111_opy_[test_name] = {}
        bstack111l1llllll_opy_ = self._111ll111111_opy_[test_name]
        bstack111ll111l1l_opy_ = bstack111l1llllll_opy_.get(bstack111ll11l1l1_opy_, 0)
        bstack111l1llllll_opy_[bstack111ll11l1l1_opy_] = bstack111ll111l1l_opy_ + 1
    def bstack11l1lll1l1_opy_(self, bstack111ll111l11_opy_, bstack111ll1111ll_opy_):
        bstack111ll11l1ll_opy_ = self.bstack111ll11l11l_opy_(bstack111ll111l11_opy_, bstack111ll1111ll_opy_)
        event_name = bstack11ll1l1llll_opy_[bstack111ll1111ll_opy_]
        bstack1l1ll1l11l1_opy_ = bstack1llllll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿࠥᴄ").format(bstack111ll111l11_opy_, event_name, bstack111ll11l1ll_opy_)
        self._111ll111ll1_opy_.append(bstack1l1ll1l11l1_opy_)
    def bstack1l1l1l1l1_opy_(self):
        return len(self._111ll111ll1_opy_) == 0
    def bstack1ll1111l1_opy_(self):
        bstack111ll11l111_opy_ = self._111ll111ll1_opy_.popleft()
        return bstack111ll11l111_opy_
    def capturing(self):
        return self._111ll111lll_opy_
    def bstack11lll1l1_opy_(self):
        self._111ll111lll_opy_ = True
    def bstack11l1l111_opy_(self):
        self._111ll111lll_opy_ = False