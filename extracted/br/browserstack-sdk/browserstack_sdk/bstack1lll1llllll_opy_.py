# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
from bstack_utils.helper import is_robot_playwright_installed
class RobotHandler():
    def __init__(self, args, logger, bstack1lllllll11l_opy_, bstack1llllll1l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllllll11l_opy_ = bstack1lllllll11l_opy_
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1lll1ll11l1_opy_(bstack1ll1lll1111_opy_):
        bstack1ll1lll1l11_opy_ = []
        if bstack1ll1lll1111_opy_:
            if not is_robot_playwright_installed():
                tokens = str(os.path.basename(bstack1ll1lll1111_opy_)).split(bstack1ll1lll_opy_ (u"ࠧࡥࠢታ"))
                camelcase_name = bstack1ll1lll_opy_ (u"ࠨࠠࠣቴ").join(t.title() for t in tokens)
                suite_name, bstack1ll1lll111l_opy_ = os.path.splitext(camelcase_name)
                bstack1ll1lll1l11_opy_.append(suite_name)
            else:
                try:
                    rel_path = os.path.relpath(bstack1ll1lll1111_opy_, start=os.getcwd())
                except ValueError:
                    rel_path = os.path.basename(bstack1ll1lll1111_opy_)
                path_parts = rel_path.split(os.sep)
                for i, part in enumerate(path_parts):
                    if i == len(path_parts) - 1:
                        bstack1ll1lll11l1_opy_ = os.path.splitext(part)[0]
                        bstack1ll1lll1l11_opy_.append(bstack1ll1lll11l1_opy_)
                    else:
                        bstack1ll1lll1l11_opy_.append(part)
        return bstack1ll1lll1l11_opy_
    @staticmethod
    def bstack1ll1lll11ll_opy_(typename):
        if bstack1ll1lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥት") in typename:
            return bstack1ll1lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤቶ")
        return bstack1ll1lll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥቷ")