# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1lll1_opy_, bstack11111ll1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_
        self.bstack11111ll1l1_opy_ = bstack11111ll1l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111lllll1_opy_(bstack111111ll1l_opy_):
        bstack111111lll1_opy_ = []
        if bstack111111ll1l_opy_:
            tokens = str(os.path.basename(bstack111111ll1l_opy_)).split(bstack11l1111_opy_ (u"ࠥࡣࠧႇ"))
            camelcase_name = bstack11l1111_opy_ (u"ࠦࠥࠨႈ").join(t.title() for t in tokens)
            suite_name, bstack111111ll11_opy_ = os.path.splitext(camelcase_name)
            bstack111111lll1_opy_.append(suite_name)
        return bstack111111lll1_opy_
    @staticmethod
    def bstack111111llll_opy_(typename):
        if bstack11l1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣႉ") in typename:
            return bstack11l1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢႊ")
        return bstack11l1111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣႋ")