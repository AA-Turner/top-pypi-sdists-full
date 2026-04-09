# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self.bstack1lllll111ll_opy_ = bstack1lllll111ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1l1llll_opy_(bstack1ll111l1lll_opy_):
        bstack1ll111ll111_opy_ = []
        if bstack1ll111l1lll_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll111l1lll_opy_)).split(bstack11ll11_opy_ (u"ࠣࡡࠥ᎜"))
                camelcase_name = bstack11ll11_opy_ (u"ࠤࠣࠦ᎝").join(t.title() for t in tokens)
                suite_name, bstack1ll111l1l1l_opy_ = os.path.splitext(camelcase_name)
                bstack1ll111ll111_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll111l1lll_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll111l1lll_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll111l1ll1_opy_ = os.path.splitext(part)[0]
                        bstack1ll111ll111_opy_.append(bstack1ll111l1ll1_opy_)
                    else:
                        bstack1ll111ll111_opy_.append(part)
        return bstack1ll111ll111_opy_
    @staticmethod
    def bstack1ll111ll11l_opy_(typename):
        if bstack11ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ᎞") in typename:
            return bstack11ll11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ᎟")
        return bstack11ll11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᎠ")