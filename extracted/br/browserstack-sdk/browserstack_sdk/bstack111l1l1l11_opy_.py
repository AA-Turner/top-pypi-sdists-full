# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11111llll1_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1l1111_opy_(bstack11111l11ll_opy_):
        bstack11111l1l11_opy_ = []
        if bstack11111l11ll_opy_:
            tokens = str(os.path.basename(bstack11111l11ll_opy_)).split(bstack1l1ll1_opy_ (u"ࠤࡢࠦ၎"))
            camelcase_name = bstack1l1ll1_opy_ (u"ࠥࠤࠧ၏").join(t.title() for t in tokens)
            suite_name, bstack11111l111l_opy_ = os.path.splitext(camelcase_name)
            bstack11111l1l11_opy_.append(suite_name)
        return bstack11111l1l11_opy_
    @staticmethod
    def bstack11111l11l1_opy_(typename):
        if bstack1l1ll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢၐ") in typename:
            return bstack1l1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨၑ")
        return bstack1l1ll1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢၒ")