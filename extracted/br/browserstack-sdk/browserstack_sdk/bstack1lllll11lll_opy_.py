# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lll11ll1l1_opy_, bstack1lll1111l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll11ll1l1_opy_ = bstack1lll11ll1l1_opy_
        self.bstack1lll1111l11_opy_ = bstack1lll1111l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1llllll_opy_(bstack1ll1lllll11_opy_):
        bstack1ll1llll11l_opy_ = []
        if bstack1ll1lllll11_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll1lllll11_opy_)).split(bstack1l1_opy_ (u"ࠤࡢࠦቛ"))
                camelcase_name = bstack1l1_opy_ (u"ࠥࠤࠧቜ").join(t.title() for t in tokens)
                suite_name, bstack1ll1llll1l1_opy_ = os.path.splitext(camelcase_name)
                bstack1ll1llll11l_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll1lllll11_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll1lllll11_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll1llll111_opy_ = os.path.splitext(part)[0]
                        bstack1ll1llll11l_opy_.append(bstack1ll1llll111_opy_)
                    else:
                        bstack1ll1llll11l_opy_.append(part)
        return bstack1ll1llll11l_opy_
    @staticmethod
    def bstack1ll1llll1ll_opy_(typename):
        if bstack1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢቝ") in typename:
            return bstack1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ቞")
        return bstack1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ቟")