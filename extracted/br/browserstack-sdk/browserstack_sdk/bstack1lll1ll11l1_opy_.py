# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1l1ll11_opy_(bstack1ll1ll1lll1_opy_):
        bstack1ll1lll11l1_opy_ = []
        if bstack1ll1ll1lll1_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll1ll1lll1_opy_)).split(bstack1ll11_opy_ (u"ࠣࡡࠥኄ"))
                camelcase_name = bstack1ll11_opy_ (u"ࠤࠣࠦኅ").join(t.title() for t in tokens)
                suite_name, bstack1ll1lll1111_opy_ = os.path.splitext(camelcase_name)
                bstack1ll1lll11l1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll1ll1lll1_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll1ll1lll1_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll1ll1llll_opy_ = os.path.splitext(part)[0]
                        bstack1ll1lll11l1_opy_.append(bstack1ll1ll1llll_opy_)
                    else:
                        bstack1ll1lll11l1_opy_.append(part)
        return bstack1ll1lll11l1_opy_
    @staticmethod
    def bstack1ll1lll111l_opy_(typename):
        if bstack1ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨኆ") in typename:
            return bstack1ll11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧኇ")
        return bstack1ll11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨኈ")