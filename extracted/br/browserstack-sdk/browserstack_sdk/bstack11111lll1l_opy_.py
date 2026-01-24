# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1llll1l1lll_opy_, bstack1lllll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1l1lll_opy_ = bstack1llll1l1lll_opy_
        self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11111l1111_opy_(bstack1llll1111ll_opy_):
        bstack1llll111l11_opy_ = []
        if bstack1llll1111ll_opy_:
            tokens = str(os.path.basename(bstack1llll1111ll_opy_)).split(bstack1l1111_opy_ (u"ࠧࡥࠢᄱ"))
            camelcase_name = bstack1l1111_opy_ (u"ࠨࠠࠣᄲ").join(t.title() for t in tokens)
            suite_name, bstack1llll111l1l_opy_ = os.path.splitext(camelcase_name)
            bstack1llll111l11_opy_.append(suite_name)
        return bstack1llll111l11_opy_
    @staticmethod
    def bstack1llll1111l1_opy_(typename):
        if bstack1l1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᄳ") in typename:
            return bstack1l1111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᄴ")
        return bstack1l1111_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᄵ")