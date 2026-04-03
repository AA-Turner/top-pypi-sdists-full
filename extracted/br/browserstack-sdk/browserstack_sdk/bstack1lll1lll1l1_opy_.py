# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lllll111l1_opy_, bstack1lllll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
        self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1ll11l1_opy_(bstack1ll111ll11l_opy_):
        bstack1ll111l1ll1_opy_ = []
        if bstack1ll111ll11l_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll111ll11l_opy_)).split(bstack1ll1l11_opy_ (u"ࠣࡡࠥ᎜"))
                camelcase_name = bstack1ll1l11_opy_ (u"ࠤࠣࠦ᎝").join(t.title() for t in tokens)
                suite_name, bstack1ll111l1l1l_opy_ = os.path.splitext(camelcase_name)
                bstack1ll111l1ll1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll111ll11l_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll111ll11l_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll111ll111_opy_ = os.path.splitext(part)[0]
                        bstack1ll111l1ll1_opy_.append(bstack1ll111ll111_opy_)
                    else:
                        bstack1ll111l1ll1_opy_.append(part)
        return bstack1ll111l1ll1_opy_
    @staticmethod
    def bstack1ll111l1lll_opy_(typename):
        if bstack1ll1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ᎞") in typename:
            return bstack1ll1l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ᎟")
        return bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᎠ")