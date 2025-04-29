# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
class bstack1ll1llll1l1_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_
    def __init__(self):
        self.bstack1lllll1llll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1ll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll1l11ll_opy_(self):
        return (self.bstack1lllll1llll_opy_ != None and self.bin_session_id != None and self.bstack1111l1ll11_opy_ != None)
    def configure(self, bstack1lllll1llll_opy_, config, bin_session_id: str, bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_):
        self.bstack1lllll1llll_opy_ = bstack1lllll1llll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1llllll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᆢ") + str(self.bin_session_id) + bstack1llllll_opy_ (u"ࠢࠣᆣ"))
    def bstack1ll1ll11lll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1llllll_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᆤ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False