# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l11l11_opy_, bstack11111ll111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l11l11_opy_ = bstack1111l11l11_opy_
        self.bstack11111ll111_opy_ = bstack11111ll111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1ll1ll_opy_(bstack111111llll_opy_):
        bstack11111l1111_opy_ = []
        if bstack111111llll_opy_:
            tokens = str(os.path.basename(bstack111111llll_opy_)).split(bstack1ll1ll_opy_ (u"ࠦࡤࠨႈ"))
            camelcase_name = bstack1ll1ll_opy_ (u"ࠧࠦࠢႉ").join(t.title() for t in tokens)
            suite_name, bstack11111l11l1_opy_ = os.path.splitext(camelcase_name)
            bstack11111l1111_opy_.append(suite_name)
        return bstack11111l1111_opy_
    @staticmethod
    def bstack11111l111l_opy_(typename):
        if bstack1ll1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤႊ") in typename:
            return bstack1ll1ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣႋ")
        return bstack1ll1ll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤႌ")