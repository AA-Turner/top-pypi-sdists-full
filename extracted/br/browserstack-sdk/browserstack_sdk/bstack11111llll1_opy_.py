# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1llll111l1l_opy_, bstack1llll11ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111111ll1l_opy_(bstack1lll1ll1ll1_opy_):
        bstack1lll1ll1l1l_opy_ = []
        if bstack1lll1ll1ll1_opy_:
            tokens = str(os.path.basename(bstack1lll1ll1ll1_opy_)).split(bstack11ll111_opy_ (u"ࠤࡢࠦᆉ"))
            camelcase_name = bstack11ll111_opy_ (u"ࠥࠤࠧᆊ").join(t.title() for t in tokens)
            suite_name, bstack1lll1ll1l11_opy_ = os.path.splitext(camelcase_name)
            bstack1lll1ll1l1l_opy_.append(suite_name)
        return bstack1lll1ll1l1l_opy_
    @staticmethod
    def bstack1lll1ll11ll_opy_(typename):
        if bstack11ll111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᆋ") in typename:
            return bstack11ll111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᆌ")
        return bstack11ll111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᆍ")