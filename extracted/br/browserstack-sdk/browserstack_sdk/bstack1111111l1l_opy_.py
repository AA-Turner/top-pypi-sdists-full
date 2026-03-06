# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1llll1ll111_opy_, bstack1llll111ll1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1ll111_opy_ = bstack1llll1ll111_opy_
        self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11111l1l11_opy_(bstack1lll1l1llll_opy_):
        bstack1lll1l1lll1_opy_ = []
        if bstack1lll1l1llll_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1lll1l1llll_opy_)).split(bstack1111_opy_ (u"ࠦࡤࠨᆒ"))
                camelcase_name = bstack1111_opy_ (u"ࠧࠦࠢᆓ").join(t.title() for t in tokens)
                suite_name, bstack1lll1l1ll11_opy_ = os.path.splitext(camelcase_name)
                bstack1lll1l1lll1_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1lll1l1llll_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1lll1l1llll_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1lll1l1ll1l_opy_ = os.path.splitext(part)[0]
                        bstack1lll1l1lll1_opy_.append(bstack1lll1l1ll1l_opy_)
                    else:
                        bstack1lll1l1lll1_opy_.append(part)
        return bstack1lll1l1lll1_opy_
    @staticmethod
    def bstack1lll1ll1111_opy_(typename):
        if bstack1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᆔ") in typename:
            return bstack1111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᆕ")
        return bstack1111_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᆖ")