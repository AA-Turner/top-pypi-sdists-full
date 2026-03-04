# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1llll1l1l1l_opy_, bstack1llll1ll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
        self.bstack1llll1ll11l_opy_ = bstack1llll1ll11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111111l1ll_opy_(bstack1lll1l1llll_opy_):
        bstack1lll1ll1111_opy_ = []
        if bstack1lll1l1llll_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1lll1l1llll_opy_)).split(bstack1lll1l_opy_ (u"ࠥࡣࠧᆑ"))
                camelcase_name = bstack1lll1l_opy_ (u"ࠦࠥࠨᆒ").join(t.title() for t in tokens)
                suite_name, bstack1lll1ll11l1_opy_ = os.path.splitext(camelcase_name)
                bstack1lll1ll1111_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1lll1l1llll_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1lll1l1llll_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1lll1l1lll1_opy_ = os.path.splitext(part)[0]
                        bstack1lll1ll1111_opy_.append(bstack1lll1l1lll1_opy_)
                    else:
                        bstack1lll1ll1111_opy_.append(part)
        return bstack1lll1ll1111_opy_
    @staticmethod
    def bstack1lll1ll111l_opy_(typename):
        if bstack1lll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᆓ") in typename:
            return bstack1lll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᆔ")
        return bstack1lll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᆕ")