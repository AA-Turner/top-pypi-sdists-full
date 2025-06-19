# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1llll11l_opy_:
    def __init__(self):
        self._111l1111l11_opy_ = deque()
        self._1111lllllll_opy_ = {}
        self._1111llll1l1_opy_ = False
    def bstack1111lllll1l_opy_(self, test_name, bstack1111llll111_opy_):
        bstack111l11111ll_opy_ = self._1111lllllll_opy_.get(test_name, {})
        return bstack111l11111ll_opy_.get(bstack1111llll111_opy_, 0)
    def bstack1111llll11l_opy_(self, test_name, bstack1111llll111_opy_):
        bstack111l111111l_opy_ = self.bstack1111lllll1l_opy_(test_name, bstack1111llll111_opy_)
        self.bstack1111llll1ll_opy_(test_name, bstack1111llll111_opy_)
        return bstack111l111111l_opy_
    def bstack1111llll1ll_opy_(self, test_name, bstack1111llll111_opy_):
        if test_name not in self._1111lllllll_opy_:
            self._1111lllllll_opy_[test_name] = {}
        bstack111l11111ll_opy_ = self._1111lllllll_opy_[test_name]
        bstack111l111111l_opy_ = bstack111l11111ll_opy_.get(bstack1111llll111_opy_, 0)
        bstack111l11111ll_opy_[bstack1111llll111_opy_] = bstack111l111111l_opy_ + 1
    def bstack1l1lllll1_opy_(self, bstack111l1111111_opy_, bstack1111llllll1_opy_):
        bstack1111lllll11_opy_ = self.bstack1111llll11l_opy_(bstack111l1111111_opy_, bstack1111llllll1_opy_)
        event_name = bstack11l1llll1l1_opy_[bstack1111llllll1_opy_]
        bstack1l1ll11l11l_opy_ = bstack111lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣḓ").format(bstack111l1111111_opy_, event_name, bstack1111lllll11_opy_)
        self._111l1111l11_opy_.append(bstack1l1ll11l11l_opy_)
    def bstack1l11l1ll11_opy_(self):
        return len(self._111l1111l11_opy_) == 0
    def bstack11ll111lll_opy_(self):
        bstack111l11111l1_opy_ = self._111l1111l11_opy_.popleft()
        return bstack111l11111l1_opy_
    def capturing(self):
        return self._1111llll1l1_opy_
    def bstack1l1l1111l_opy_(self):
        self._1111llll1l1_opy_ = True
    def bstack11lll1l1_opy_(self):
        self._1111llll1l1_opy_ = False