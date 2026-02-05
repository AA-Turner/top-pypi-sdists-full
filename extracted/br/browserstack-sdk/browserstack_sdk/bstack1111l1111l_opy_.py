# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1lllll1ll1l_opy_, bstack1lllll111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll1ll1l_opy_ = bstack1lllll1ll1l_opy_
        self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11111l11l1_opy_(bstack1llll1111ll_opy_):
        bstack1llll1111l1_opy_ = []
        if bstack1llll1111ll_opy_:
            tokens = str(os.path.basename(bstack1llll1111ll_opy_)).split(bstack11l1ll1_opy_ (u"ࠥࡣࠧᄶ"))
            camelcase_name = bstack11l1ll1_opy_ (u"ࠦࠥࠨᄷ").join(t.title() for t in tokens)
            suite_name, bstack1llll111l11_opy_ = os.path.splitext(camelcase_name)
            bstack1llll1111l1_opy_.append(suite_name)
        return bstack1llll1111l1_opy_
    @staticmethod
    def bstack1llll11111l_opy_(typename):
        if bstack11l1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᄸ") in typename:
            return bstack11l1ll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᄹ")
        return bstack11l1ll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᄺ")