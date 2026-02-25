# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1llll1lll11_opy_, bstack1llll1111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
        self.bstack1llll1111l1_opy_ = bstack1llll1111l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111111lll1_opy_(bstack1lll1ll1l1l_opy_):
        bstack1lll1ll1lll_opy_ = []
        if bstack1lll1ll1l1l_opy_:
            tokens = str(os.path.basename(bstack1lll1ll1l1l_opy_)).split(bstack11l1l11_opy_ (u"ࠨ࡟ࠣᆍ"))
            camelcase_name = bstack11l1l11_opy_ (u"ࠢࠡࠤᆎ").join(t.title() for t in tokens)
            suite_name, bstack1lll1ll1ll1_opy_ = os.path.splitext(camelcase_name)
            bstack1lll1ll1lll_opy_.append(suite_name)
        return bstack1lll1ll1lll_opy_
    @staticmethod
    def bstack1lll1ll1l11_opy_(typename):
        if bstack11l1l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᆏ") in typename:
            return bstack11l1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᆐ")
        return bstack11l1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᆑ")