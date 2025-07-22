# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111l1ll1_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1l111l_opy_(bstack111111ll1l_opy_):
        bstack111111lll1_opy_ = []
        if bstack111111ll1l_opy_:
            tokens = str(os.path.basename(bstack111111ll1l_opy_)).split(bstack111l111_opy_ (u"ࠥࡣࠧႇ"))
            camelcase_name = bstack111l111_opy_ (u"ࠦࠥࠨႈ").join(t.title() for t in tokens)
            suite_name, bstack11111l1111_opy_ = os.path.splitext(camelcase_name)
            bstack111111lll1_opy_.append(suite_name)
        return bstack111111lll1_opy_
    @staticmethod
    def bstack111111llll_opy_(typename):
        if bstack111l111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣႉ") in typename:
            return bstack111l111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢႊ")
        return bstack111l111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣႋ")