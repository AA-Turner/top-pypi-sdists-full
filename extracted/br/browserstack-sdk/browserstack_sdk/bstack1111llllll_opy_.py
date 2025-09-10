# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111l11ll_opy_, bstack1111l111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l11ll_opy_ = bstack11111l11ll_opy_
        self.bstack1111l111l1_opy_ = bstack1111l111l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11111l_opy_(bstack1111111lll_opy_):
        bstack111111l1l1_opy_ = []
        if bstack1111111lll_opy_:
            tokens = str(os.path.basename(bstack1111111lll_opy_)).split(bstack1ll11ll_opy_ (u"ࠢࡠࠤ႒"))
            camelcase_name = bstack1ll11ll_opy_ (u"ࠣࠢࠥ႓").join(t.title() for t in tokens)
            suite_name, bstack111111l111_opy_ = os.path.splitext(camelcase_name)
            bstack111111l1l1_opy_.append(suite_name)
        return bstack111111l1l1_opy_
    @staticmethod
    def bstack111111l11l_opy_(typename):
        if bstack1ll11ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ႔") in typename:
            return bstack1ll11ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ႕")
        return bstack1ll11ll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ႖")