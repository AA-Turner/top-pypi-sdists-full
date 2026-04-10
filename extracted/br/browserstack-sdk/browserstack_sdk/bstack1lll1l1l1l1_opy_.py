# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lllll11111_opy_, bstack1lllll111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
        self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll11ll111_opy_(bstack1ll111l1l1l_opy_):
        bstack1ll111l1ll1_opy_ = []
        if bstack1ll111l1l1l_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll111l1l1l_opy_)).split(bstack1ll_opy_ (u"ࠣࡡࠥ᎜"))
                camelcase_name = bstack1ll_opy_ (u"ࠤࠣࠦ᎝").join(t.title() for t in tokens)
                suite_name, bstack1ll111ll11l_opy_ = os.path.splitext(camelcase_name)
                bstack1ll111l1ll1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll111l1l1l_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll111l1l1l_opy_)
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
        if bstack1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ᎞") in typename:
            return bstack1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ᎟")
        return bstack1ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᎠ")