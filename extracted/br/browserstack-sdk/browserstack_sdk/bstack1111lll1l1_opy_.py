# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111l1l1l1_opy_, bstack1111l1ll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111lllll1_opy_(bstack11111l111l_opy_):
        bstack11111l11ll_opy_ = []
        if bstack11111l111l_opy_:
            tokens = str(os.path.basename(bstack11111l111l_opy_)).split(bstack11ll1l1_opy_ (u"ࠤࡢࠦ၎"))
            camelcase_name = bstack11ll1l1_opy_ (u"ࠥࠤࠧ၏").join(t.title() for t in tokens)
            suite_name, bstack11111l11l1_opy_ = os.path.splitext(camelcase_name)
            bstack11111l11ll_opy_.append(suite_name)
        return bstack11111l11ll_opy_
    @staticmethod
    def bstack11111l1111_opy_(typename):
        if bstack11ll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢၐ") in typename:
            return bstack11ll1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨၑ")
        return bstack11ll1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢၒ")