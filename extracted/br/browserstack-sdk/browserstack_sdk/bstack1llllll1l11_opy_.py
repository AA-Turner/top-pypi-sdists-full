# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lll1l1111l_opy_, bstack1lll1l1llll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll1l1111l_opy_ = bstack1lll1l1111l_opy_
        self.bstack1lll1l1llll_opy_ = bstack1lll1l1llll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lllll11ll1_opy_(bstack1lll11l1l11_opy_):
        bstack1lll11l1ll1_opy_ = []
        if bstack1lll11l1l11_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1lll11l1l11_opy_)).split(bstack1111l_opy_ (u"ࠣࡡࠥሰ"))
                camelcase_name = bstack1111l_opy_ (u"ࠤࠣࠦሱ").join(t.title() for t in tokens)
                suite_name, bstack1lll11l1lll_opy_ = os.path.splitext(camelcase_name)
                bstack1lll11l1ll1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1lll11l1l11_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1lll11l1l11_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1lll11ll111_opy_ = os.path.splitext(part)[0]
                        bstack1lll11l1ll1_opy_.append(bstack1lll11ll111_opy_)
                    else:
                        bstack1lll11l1ll1_opy_.append(part)
        return bstack1lll11l1ll1_opy_
    @staticmethod
    def bstack1lll11l1l1l_opy_(typename):
        if bstack1111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨሲ") in typename:
            return bstack1111l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧሳ")
        return bstack1111l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨሴ")