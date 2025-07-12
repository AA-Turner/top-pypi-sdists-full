# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1llll1l1l1l_opy_ import bstack1ll1llllll1_opy_
class bstack1lll1lllll1_opy_(abc.ABC):
    bin_session_id: str
    bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_
    def __init__(self):
        self.bstack1lll1llll1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1llll1l1l1l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll1lllllll_opy_(self):
        return (self.bstack1lll1llll1l_opy_ != None and self.bin_session_id != None and self.bstack1llll1l1l1l_opy_ != None)
    def configure(self, bstack1lll1llll1l_opy_, config, bin_session_id: str, bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_):
        self.bstack1lll1llll1l_opy_ = bstack1lll1llll1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡱࡴࡪࡵ࡭ࡧࠣࡿࡸ࡫࡬ࡧ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣ࠳ࡥ࡟࡯ࡣࡰࡩࡤࡥࡽ࠻ࠢࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦᅁ") + str(self.bin_session_id) + bstack11l1111_opy_ (u"ࠣࠤᅂ"))
    def bstack1lll1lll1l1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11l1111_opy_ (u"ࠤࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡎࡰࡰࡨࠦᅃ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False