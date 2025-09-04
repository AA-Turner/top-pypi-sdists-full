# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l11111_opy_, bstack11111l1l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l11111_opy_ = bstack1111l11111_opy_
        self.bstack11111l1l1l_opy_ = bstack11111l1l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111lll111_opy_(bstack111111l111_opy_):
        bstack111111l1l1_opy_ = []
        if bstack111111l111_opy_:
            tokens = str(os.path.basename(bstack111111l111_opy_)).split(bstack1111l1l_opy_ (u"ࠣࡡࠥ႓"))
            camelcase_name = bstack1111l1l_opy_ (u"ࠤࠣࠦ႔").join(t.title() for t in tokens)
            suite_name, bstack111111l11l_opy_ = os.path.splitext(camelcase_name)
            bstack111111l1l1_opy_.append(suite_name)
        return bstack111111l1l1_opy_
    @staticmethod
    def bstack111111l1ll_opy_(typename):
        if bstack1111l1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ႕") in typename:
            return bstack1111l1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ႖")
        return bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ႗")