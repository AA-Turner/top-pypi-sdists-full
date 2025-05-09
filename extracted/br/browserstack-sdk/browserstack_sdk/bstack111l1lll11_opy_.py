# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111lll111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111l1l11l1_opy_(bstack1111l1lll1_opy_):
        bstack1111l1ll1l_opy_ = []
        if bstack1111l1lll1_opy_:
            tokens = str(os.path.basename(bstack1111l1lll1_opy_)).split(bstack11lll_opy_ (u"ࠧࡥࠢဒ"))
            camelcase_name = bstack11lll_opy_ (u"ࠨࠠࠣဓ").join(t.title() for t in tokens)
            suite_name, bstack1111ll1111_opy_ = os.path.splitext(camelcase_name)
            bstack1111l1ll1l_opy_.append(suite_name)
        return bstack1111l1ll1l_opy_
    @staticmethod
    def bstack1111l1llll_opy_(typename):
        if bstack11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥန") in typename:
            return bstack11lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤပ")
        return bstack11lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥဖ")