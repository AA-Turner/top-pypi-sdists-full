# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack11ll11ll1_opy_:
    def __init__(self):
        self._111l1llllll_opy_ = deque()
        self._111ll11l111_opy_ = {}
        self._111ll111l11_opy_ = False
    def bstack111ll111111_opy_(self, test_name, bstack111ll1111l1_opy_):
        bstack111ll1111ll_opy_ = self._111ll11l111_opy_.get(test_name, {})
        return bstack111ll1111ll_opy_.get(bstack111ll1111l1_opy_, 0)
    def bstack111ll11l11l_opy_(self, test_name, bstack111ll1111l1_opy_):
        bstack111ll11111l_opy_ = self.bstack111ll111111_opy_(test_name, bstack111ll1111l1_opy_)
        self.bstack111ll111ll1_opy_(test_name, bstack111ll1111l1_opy_)
        return bstack111ll11111l_opy_
    def bstack111ll111ll1_opy_(self, test_name, bstack111ll1111l1_opy_):
        if test_name not in self._111ll11l111_opy_:
            self._111ll11l111_opy_[test_name] = {}
        bstack111ll1111ll_opy_ = self._111ll11l111_opy_[test_name]
        bstack111ll11111l_opy_ = bstack111ll1111ll_opy_.get(bstack111ll1111l1_opy_, 0)
        bstack111ll1111ll_opy_[bstack111ll1111l1_opy_] = bstack111ll11111l_opy_ + 1
    def bstack1ll111l11_opy_(self, bstack111ll11l1l1_opy_, bstack111ll111lll_opy_):
        bstack111ll111l1l_opy_ = self.bstack111ll11l11l_opy_(bstack111ll11l1l1_opy_, bstack111ll111lll_opy_)
        event_name = bstack11ll1l1ll11_opy_[bstack111ll111lll_opy_]
        bstack1l1ll1l1111_opy_ = bstack1l1lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣᴉ").format(bstack111ll11l1l1_opy_, event_name, bstack111ll111l1l_opy_)
        self._111l1llllll_opy_.append(bstack1l1ll1l1111_opy_)
    def bstack1llllll111_opy_(self):
        return len(self._111l1llllll_opy_) == 0
    def bstack1l1l1111ll_opy_(self):
        bstack111ll11l1ll_opy_ = self._111l1llllll_opy_.popleft()
        return bstack111ll11l1ll_opy_
    def capturing(self):
        return self._111ll111l11_opy_
    def bstack1ll1111111_opy_(self):
        self._111ll111l11_opy_ = True
    def bstack111l111ll_opy_(self):
        self._111ll111l11_opy_ = False