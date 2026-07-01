# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1ll1llll_opy_, bstack1ll1l11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll1llll_opy_ = bstack1ll1llll_opy_
        self.bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1llll1ll1_opy_(bstack11l111lll_opy_):
        bstack11l111ll1_opy_ = []
        if bstack11l111lll_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack11l111lll_opy_)).split(bstack1l1llll_opy_ (u"ࠤࡢࠦಖ"))
                camelcase_name = bstack1l1llll_opy_ (u"ࠥࠤࠧಗ").join(t.title() for t in tokens)
                suite_name, bstack11l11l11l_opy_ = os.path.splitext(camelcase_name)
                bstack11l111ll1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack11l111lll_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack11l111lll_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack11l11l111_opy_ = os.path.splitext(part)[0]
                        bstack11l111ll1_opy_.append(bstack11l11l111_opy_)
                    else:
                        bstack11l111ll1_opy_.append(part)
        return bstack11l111ll1_opy_
    @staticmethod
    def failure_type(typename):
        if bstack1l1llll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢಘ") in typename:
            return bstack1l1llll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨಙ")
        return bstack1l1llll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢಚ")