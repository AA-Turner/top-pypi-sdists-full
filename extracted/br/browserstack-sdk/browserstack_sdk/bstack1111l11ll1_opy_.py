# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1lllll1lll1_opy_, bstack1lllll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll1lll1_opy_ = bstack1lllll1lll1_opy_
        self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111111lll_opy_(bstack1llll111l1l_opy_):
        bstack1llll111l11_opy_ = []
        if bstack1llll111l1l_opy_:
            tokens = str(os.path.basename(bstack1llll111l1l_opy_)).split(bstack11lllll_opy_ (u"ࠥࡣࠧᄶ"))
            camelcase_name = bstack11lllll_opy_ (u"ࠦࠥࠨᄷ").join(t.title() for t in tokens)
            suite_name, bstack1llll1111l1_opy_ = os.path.splitext(camelcase_name)
            bstack1llll111l11_opy_.append(suite_name)
        return bstack1llll111l11_opy_
    @staticmethod
    def bstack1llll1111ll_opy_(typename):
        if bstack11lllll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᄸ") in typename:
            return bstack11lllll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᄹ")
        return bstack11lllll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᄺ")