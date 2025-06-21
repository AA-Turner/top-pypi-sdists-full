# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll11ll_opy_, bstack11111lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
        self.bstack11111lllll_opy_ = bstack11111lllll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111llllll_opy_(bstack11111l111l_opy_):
        bstack11111l11l1_opy_ = []
        if bstack11111l111l_opy_:
            tokens = str(os.path.basename(bstack11111l111l_opy_)).split(bstack1l1l1l1_opy_ (u"ࠤࡢࠦ၎"))
            camelcase_name = bstack1l1l1l1_opy_ (u"ࠥࠤࠧ၏").join(t.title() for t in tokens)
            suite_name, bstack11111l1111_opy_ = os.path.splitext(camelcase_name)
            bstack11111l11l1_opy_.append(suite_name)
        return bstack11111l11l1_opy_
    @staticmethod
    def bstack11111l11ll_opy_(typename):
        if bstack1l1l1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢၐ") in typename:
            return bstack1l1l1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨၑ")
        return bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢၒ")