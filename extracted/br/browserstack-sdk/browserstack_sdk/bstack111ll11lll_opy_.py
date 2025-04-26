# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll1lll_opy_, bstack1111lll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111ll1ll11_opy_(bstack1111ll111l_opy_):
        bstack1111l1lll1_opy_ = []
        if bstack1111ll111l_opy_:
            tokens = str(os.path.basename(bstack1111ll111l_opy_)).split(bstack1l11lll_opy_ (u"ࠧࡥࠢဒ"))
            camelcase_name = bstack1l11lll_opy_ (u"ࠨࠠࠣဓ").join(t.title() for t in tokens)
            suite_name, bstack1111ll1111_opy_ = os.path.splitext(camelcase_name)
            bstack1111l1lll1_opy_.append(suite_name)
        return bstack1111l1lll1_opy_
    @staticmethod
    def bstack1111l1llll_opy_(typename):
        if bstack1l11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥန") in typename:
            return bstack1l11lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤပ")
        return bstack1l11lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥဖ")