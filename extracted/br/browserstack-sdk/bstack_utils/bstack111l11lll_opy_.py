# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1l1l1111_opy_:
    def __init__(self):
        self._111ll11l11l_opy_ = deque()
        self._111l1llllll_opy_ = {}
        self._111ll11111l_opy_ = False
    def bstack111ll111lll_opy_(self, test_name, bstack111ll11l1l1_opy_):
        bstack111ll111l1l_opy_ = self._111l1llllll_opy_.get(test_name, {})
        return bstack111ll111l1l_opy_.get(bstack111ll11l1l1_opy_, 0)
    def bstack111ll111l11_opy_(self, test_name, bstack111ll11l1l1_opy_):
        bstack111ll1111ll_opy_ = self.bstack111ll111lll_opy_(test_name, bstack111ll11l1l1_opy_)
        self.bstack111ll111ll1_opy_(test_name, bstack111ll11l1l1_opy_)
        return bstack111ll1111ll_opy_
    def bstack111ll111ll1_opy_(self, test_name, bstack111ll11l1l1_opy_):
        if test_name not in self._111l1llllll_opy_:
            self._111l1llllll_opy_[test_name] = {}
        bstack111ll111l1l_opy_ = self._111l1llllll_opy_[test_name]
        bstack111ll1111ll_opy_ = bstack111ll111l1l_opy_.get(bstack111ll11l1l1_opy_, 0)
        bstack111ll111l1l_opy_[bstack111ll11l1l1_opy_] = bstack111ll1111ll_opy_ + 1
    def bstack11llll1l_opy_(self, bstack111ll11l1ll_opy_, bstack111ll11l111_opy_):
        bstack111ll111111_opy_ = self.bstack111ll111l11_opy_(bstack111ll11l1ll_opy_, bstack111ll11l111_opy_)
        event_name = bstack11ll1ll1l11_opy_[bstack111ll11l111_opy_]
        bstack1l1ll1l11l1_opy_ = bstack1l11lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣᴂ").format(bstack111ll11l1ll_opy_, event_name, bstack111ll111111_opy_)
        self._111ll11l11l_opy_.append(bstack1l1ll1l11l1_opy_)
    def bstack11111ll11_opy_(self):
        return len(self._111ll11l11l_opy_) == 0
    def bstack11l11l11ll_opy_(self):
        bstack111ll1111l1_opy_ = self._111ll11l11l_opy_.popleft()
        return bstack111ll1111l1_opy_
    def capturing(self):
        return self._111ll11111l_opy_
    def bstack1l11lll1ll_opy_(self):
        self._111ll11111l_opy_ = True
    def bstack1ll11lll1l_opy_(self):
        self._111ll11111l_opy_ = False