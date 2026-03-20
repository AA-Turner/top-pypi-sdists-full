# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lll11l111l_opy_, bstack1lll111l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll11l111l_opy_ = bstack1lll11l111l_opy_
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lllll11l11_opy_(bstack1ll1llll11l_opy_):
        bstack1ll1llll111_opy_ = []
        if bstack1ll1llll11l_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll1llll11l_opy_)).split(bstack11lll1_opy_ (u"ࠤࡢࠦቛ"))
                camelcase_name = bstack11lll1_opy_ (u"ࠥࠤࠧቜ").join(t.title() for t in tokens)
                suite_name, bstack1ll1llll1ll_opy_ = os.path.splitext(camelcase_name)
                bstack1ll1llll111_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll1llll11l_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll1llll11l_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll1llll1l1_opy_ = os.path.splitext(part)[0]
                        bstack1ll1llll111_opy_.append(bstack1ll1llll1l1_opy_)
                    else:
                        bstack1ll1llll111_opy_.append(part)
        return bstack1ll1llll111_opy_
    @staticmethod
    def bstack1ll1lllll11_opy_(typename):
        if bstack11lll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢቝ") in typename:
            return bstack11lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ቞")
        return bstack11lll1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ቟")