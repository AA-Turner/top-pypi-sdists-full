# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111ll1ll_opy_, bstack11111ll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
        self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11111l_opy_(bstack111111llll_opy_):
        bstack111111lll1_opy_ = []
        if bstack111111llll_opy_:
            tokens = str(os.path.basename(bstack111111llll_opy_)).split(bstack1l1l1ll_opy_ (u"ࠥࡣࠧႎ"))
            camelcase_name = bstack1l1l1ll_opy_ (u"ࠦࠥࠨႏ").join(t.title() for t in tokens)
            suite_name, bstack11111l1111_opy_ = os.path.splitext(camelcase_name)
            bstack111111lll1_opy_.append(suite_name)
        return bstack111111lll1_opy_
    @staticmethod
    def bstack111111ll1l_opy_(typename):
        if bstack1l1l1ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ႐") in typename:
            return bstack1l1l1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ႑")
        return bstack1l1l1ll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ႒")