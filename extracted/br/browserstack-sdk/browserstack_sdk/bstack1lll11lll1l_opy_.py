# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1llll1ll1l1_opy_, bstack1llll1lll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1ll1l1_opy_ = bstack1llll1ll1l1_opy_
        self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1l1l1l1_opy_(bstack1ll111l1111_opy_):
        bstack1ll1111llll_opy_ = []
        if bstack1ll111l1111_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll111l1111_opy_)).split(bstack111ll_opy_ (u"ࠥࡣࠧᏁ"))
                camelcase_name = bstack111ll_opy_ (u"ࠦࠥࠨᏂ").join(t.title() for t in tokens)
                suite_name, bstack1ll111l11ll_opy_ = os.path.splitext(camelcase_name)
                bstack1ll1111llll_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll111l1111_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll111l1111_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll111l11l1_opy_ = os.path.splitext(part)[0]
                        bstack1ll1111llll_opy_.append(bstack1ll111l11l1_opy_)
                    else:
                        bstack1ll1111llll_opy_.append(part)
        return bstack1ll1111llll_opy_
    @staticmethod
    def bstack1ll111l111l_opy_(typename):
        if bstack111ll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᏃ") in typename:
            return bstack111ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᏄ")
        return bstack111ll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᏅ")