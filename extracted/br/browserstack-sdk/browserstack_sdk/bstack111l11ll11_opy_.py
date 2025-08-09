# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111ll1l1_opy_, bstack1111ll1111_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111ll1l1_opy_ = bstack11111ll1l1_opy_
        self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l111l1l_opy_(bstack11111l1111_opy_):
        bstack111111llll_opy_ = []
        if bstack11111l1111_opy_:
            tokens = str(os.path.basename(bstack11111l1111_opy_)).split(bstack11l1_opy_ (u"ࠦࡤࠨႈ"))
            camelcase_name = bstack11l1_opy_ (u"ࠧࠦࠢႉ").join(t.title() for t in tokens)
            suite_name, bstack11111l11l1_opy_ = os.path.splitext(camelcase_name)
            bstack111111llll_opy_.append(suite_name)
        return bstack111111llll_opy_
    @staticmethod
    def bstack11111l111l_opy_(typename):
        if bstack11l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤႊ") in typename:
            return bstack11l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣႋ")
        return bstack11l1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤႌ")