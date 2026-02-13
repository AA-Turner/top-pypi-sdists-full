# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1llll111111_opy_, bstack1llll11ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll111111_opy_ = bstack1llll111111_opy_
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11111l11ll_opy_(bstack1lll1l1l111_opy_):
        bstack1lll1l11ll1_opy_ = []
        if bstack1lll1l1l111_opy_:
            tokens = str(os.path.basename(bstack1lll1l1l111_opy_)).split(bstack11l11_opy_ (u"ࠦࡤࠨᆄ"))
            camelcase_name = bstack11l11_opy_ (u"ࠧࠦࠢᆅ").join(t.title() for t in tokens)
            suite_name, bstack1lll1l1l11l_opy_ = os.path.splitext(camelcase_name)
            bstack1lll1l11ll1_opy_.append(suite_name)
        return bstack1lll1l11ll1_opy_
    @staticmethod
    def bstack1lll1l11lll_opy_(typename):
        if bstack11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᆆ") in typename:
            return bstack11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᆇ")
        return bstack11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᆈ")