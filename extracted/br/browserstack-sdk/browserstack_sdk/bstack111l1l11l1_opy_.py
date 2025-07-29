# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1111l_opy_, bstack1111ll1111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1111l_opy_ = bstack1111l1111l_opy_
        self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11llll_opy_(bstack111111llll_opy_):
        bstack111111ll1l_opy_ = []
        if bstack111111llll_opy_:
            tokens = str(os.path.basename(bstack111111llll_opy_)).split(bstackl_opy_ (u"ࠦࡤࠨႈ"))
            camelcase_name = bstackl_opy_ (u"ࠧࠦࠢႉ").join(t.title() for t in tokens)
            suite_name, bstack111111lll1_opy_ = os.path.splitext(camelcase_name)
            bstack111111ll1l_opy_.append(suite_name)
        return bstack111111ll1l_opy_
    @staticmethod
    def bstack111111ll11_opy_(typename):
        if bstackl_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤႊ") in typename:
            return bstackl_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣႋ")
        return bstackl_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤႌ")