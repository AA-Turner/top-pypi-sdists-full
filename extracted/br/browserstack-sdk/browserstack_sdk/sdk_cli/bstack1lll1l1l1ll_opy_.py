# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1l1l1_opy_ import bstack1111l1ll11_opy_
class bstack1ll1llll1ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_
    def __init__(self):
        self.bstack1lll1ll1l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1l1l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll1lllllll_opy_(self):
        return (self.bstack1lll1ll1l11_opy_ != None and self.bin_session_id != None and self.bstack1111l1l1l1_opy_ != None)
    def configure(self, bstack1lll1ll1l11_opy_, config, bin_session_id: str, bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_):
        self.bstack1lll1ll1l11_opy_ = bstack1lll1ll1l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᆢ") + str(self.bin_session_id) + bstack1l1lll_opy_ (u"ࠢࠣᆣ"))
    def bstack1ll1ll1l1l1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1lll_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᆤ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False