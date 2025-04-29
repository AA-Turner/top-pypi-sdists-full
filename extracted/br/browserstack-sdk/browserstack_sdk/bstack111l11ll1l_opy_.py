# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111ll1l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
        self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l11ll11_opy_(bstack1111l1lll1_opy_):
        bstack1111ll111l_opy_ = []
        if bstack1111l1lll1_opy_:
            tokens = str(os.path.basename(bstack1111l1lll1_opy_)).split(bstack1llllll_opy_ (u"ࠧࡥࠢဒ"))
            camelcase_name = bstack1llllll_opy_ (u"ࠨࠠࠣဓ").join(t.title() for t in tokens)
            suite_name, bstack1111ll1111_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll111l_opy_.append(suite_name)
        return bstack1111ll111l_opy_
    @staticmethod
    def bstack1111l1llll_opy_(typename):
        if bstack1llllll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥန") in typename:
            return bstack1llllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤပ")
        return bstack1llllll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥဖ")