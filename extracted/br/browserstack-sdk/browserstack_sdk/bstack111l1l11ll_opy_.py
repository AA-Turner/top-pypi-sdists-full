# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1lll1_opy_, bstack1111l111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_
        self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111lllll1_opy_(bstack111111llll_opy_):
        bstack111111ll11_opy_ = []
        if bstack111111llll_opy_:
            tokens = str(os.path.basename(bstack111111llll_opy_)).split(bstack1l1_opy_ (u"ࠣࡡࠥႅ"))
            camelcase_name = bstack1l1_opy_ (u"ࠤࠣࠦႆ").join(t.title() for t in tokens)
            suite_name, bstack111111lll1_opy_ = os.path.splitext(camelcase_name)
            bstack111111ll11_opy_.append(suite_name)
        return bstack111111ll11_opy_
    @staticmethod
    def bstack111111ll1l_opy_(typename):
        if bstack1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨႇ") in typename:
            return bstack1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧႈ")
        return bstack1l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨႉ")