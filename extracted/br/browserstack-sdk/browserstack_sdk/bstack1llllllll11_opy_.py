# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lll1lllll1_opy_, bstack1lll1l11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll1lllll1_opy_ = bstack1lll1lllll1_opy_
        self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111111l1l1_opy_(bstack1lll11lll11_opy_):
        bstack1lll11ll11l_opy_ = []
        if bstack1lll11lll11_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1lll11lll11_opy_)).split(bstack1ll111_opy_ (u"ࠥࡣࠧᇺ"))
                camelcase_name = bstack1ll111_opy_ (u"ࠦࠥࠨᇻ").join(t.title() for t in tokens)
                suite_name, bstack1lll11ll111_opy_ = os.path.splitext(camelcase_name)
                bstack1lll11ll11l_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1lll11lll11_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1lll11lll11_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1lll11ll1ll_opy_ = os.path.splitext(part)[0]
                        bstack1lll11ll11l_opy_.append(bstack1lll11ll1ll_opy_)
                    else:
                        bstack1lll11ll11l_opy_.append(part)
        return bstack1lll11ll11l_opy_
    @staticmethod
    def bstack1lll11ll1l1_opy_(typename):
        if bstack1ll111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᇼ") in typename:
            return bstack1ll111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᇽ")
        return bstack1ll111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᇾ")