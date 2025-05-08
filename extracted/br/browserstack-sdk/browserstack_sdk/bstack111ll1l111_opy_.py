# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111llll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
        self.bstack1111llll1l_opy_ = bstack1111llll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111lll111l_opy_(bstack1111ll111l_opy_):
        bstack1111l1lll1_opy_ = []
        if bstack1111ll111l_opy_:
            tokens = str(os.path.basename(bstack1111ll111l_opy_)).split(bstack1l1lll_opy_ (u"ࠧࡥࠢဒ"))
            camelcase_name = bstack1l1lll_opy_ (u"ࠨࠠࠣဓ").join(t.title() for t in tokens)
            suite_name, bstack1111l1llll_opy_ = os.path.splitext(camelcase_name)
            bstack1111l1lll1_opy_.append(suite_name)
        return bstack1111l1lll1_opy_
    @staticmethod
    def bstack1111ll1111_opy_(typename):
        if bstack1l1lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥန") in typename:
            return bstack1l1lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤပ")
        return bstack1l1lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥဖ")