# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll11l11_opy_
class bstack1l11llll11l_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_
    def __init__(self):
        self.bstack1l1l1l1l1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1lll11l1l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l11ll1l11l_opy_(self):
        return (self.bstack1l1l1l1l1l_opy_ != None and self.bin_session_id != None and self.bstack1l1lll11l1l_opy_ != None)
    def configure(self, bstack1l1l1l1l1l_opy_, config, bin_session_id: str, bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_):
        self.bstack1l1l1l1l1l_opy_ = bstack1l1l1l1l1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1lll11l1l_opy_ = bstack1l1lll11l1l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᚿ") + str(self.bin_session_id) + bstack111ll11_opy_ (u"ࠢࠣᛀ"))
    def bstack1l1111lllll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack111ll11_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᛁ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False