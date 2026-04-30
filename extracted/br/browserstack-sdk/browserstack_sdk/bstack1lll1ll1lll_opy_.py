# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lllll1111l_opy_, bstack1llll1lll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll1111l_opy_ = bstack1lllll1111l_opy_
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1l11ll1_opy_(bstack1ll111l11ll_opy_):
        bstack1ll111l1ll1_opy_ = []
        if bstack1ll111l11ll_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll111l11ll_opy_)).split(bstack1l1111l_opy_ (u"ࠥࡣࠧᎳ"))
                camelcase_name = bstack1l1111l_opy_ (u"ࠦࠥࠨᎴ").join(t.title() for t in tokens)
                suite_name, bstack1ll111l1l11_opy_ = os.path.splitext(camelcase_name)
                bstack1ll111l1ll1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll111l11ll_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll111l11ll_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll111l11l1_opy_ = os.path.splitext(part)[0]
                        bstack1ll111l1ll1_opy_.append(bstack1ll111l11l1_opy_)
                    else:
                        bstack1ll111l1ll1_opy_.append(part)
        return bstack1ll111l1ll1_opy_
    @staticmethod
    def bstack1ll111l1l1l_opy_(typename):
        if bstack1l1111l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᎵ") in typename:
            return bstack1l1111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᎶ")
        return bstack1l1111l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᎷ")