# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1l1ll_opy_, bstack1111ll1111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
        self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111lllll1_opy_(bstack1111l11111_opy_):
        bstack1111l111l1_opy_ = []
        if bstack1111l11111_opy_:
            tokens = str(os.path.basename(bstack1111l11111_opy_)).split(bstack111lll_opy_ (u"ࠥࡣࠧ၁"))
            camelcase_name = bstack111lll_opy_ (u"ࠦࠥࠨ၂").join(t.title() for t in tokens)
            suite_name, bstack1111l1111l_opy_ = os.path.splitext(camelcase_name)
            bstack1111l111l1_opy_.append(suite_name)
        return bstack1111l111l1_opy_
    @staticmethod
    def bstack11111lllll_opy_(typename):
        if bstack111lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ၃") in typename:
            return bstack111lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ၄")
        return bstack111lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ၅")