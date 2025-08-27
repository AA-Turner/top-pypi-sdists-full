# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111lll1l_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111lll1l_opy_ = bstack11111lll1l_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l111l1l_opy_(bstack111111lll1_opy_):
        bstack11111l1111_opy_ = []
        if bstack111111lll1_opy_:
            tokens = str(os.path.basename(bstack111111lll1_opy_)).split(bstack1111lll_opy_ (u"ࠥࡣࠧႎ"))
            camelcase_name = bstack1111lll_opy_ (u"ࠦࠥࠨႏ").join(t.title() for t in tokens)
            suite_name, bstack111111llll_opy_ = os.path.splitext(camelcase_name)
            bstack11111l1111_opy_.append(suite_name)
        return bstack11111l1111_opy_
    @staticmethod
    def bstack111111ll1l_opy_(typename):
        if bstack1111lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ႐") in typename:
            return bstack1111lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ႑")
        return bstack1111lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ႒")