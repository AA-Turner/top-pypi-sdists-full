# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111llll1_opy_, bstack11111ll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
        self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11l1l1_opy_(bstack111111lll1_opy_):
        bstack111111l1ll_opy_ = []
        if bstack111111lll1_opy_:
            tokens = str(os.path.basename(bstack111111lll1_opy_)).split(bstack1l11l11_opy_ (u"ࠦࡤࠨႈ"))
            camelcase_name = bstack1l11l11_opy_ (u"ࠧࠦࠢႉ").join(t.title() for t in tokens)
            suite_name, bstack111111ll11_opy_ = os.path.splitext(camelcase_name)
            bstack111111l1ll_opy_.append(suite_name)
        return bstack111111l1ll_opy_
    @staticmethod
    def bstack111111ll1l_opy_(typename):
        if bstack1l11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤႊ") in typename:
            return bstack1l11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣႋ")
        return bstack1l11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤႌ")