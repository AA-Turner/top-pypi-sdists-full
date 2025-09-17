# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111l11ll_opy_, bstack11111l111l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
        self.bstack11111l111l_opy_ = bstack11111l111l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111llllll_opy_(bstack111111l11l_opy_):
        bstack1111111lll_opy_ = []
        if bstack111111l11l_opy_:
            tokens = str(os.path.basename(bstack111111l11l_opy_)).split(bstack1l11ll1_opy_ (u"ࠨ࡟ࠣ႑"))
            camelcase_name = bstack1l11ll1_opy_ (u"ࠢࠡࠤ႒").join(t.title() for t in tokens)
            suite_name, bstack111111l111_opy_ = os.path.splitext(camelcase_name)
            bstack1111111lll_opy_.append(suite_name)
        return bstack1111111lll_opy_
    @staticmethod
    def bstack111111l1l1_opy_(typename):
        if bstack1l11ll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ႓") in typename:
            return bstack1l11ll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ႔")
        return bstack1l11ll1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ႕")