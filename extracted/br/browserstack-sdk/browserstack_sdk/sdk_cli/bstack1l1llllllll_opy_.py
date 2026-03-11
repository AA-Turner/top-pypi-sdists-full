# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll1ll1l111_opy_ import bstack1ll1ll1l11l_opy_
class bstack1ll11111l11_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_
    def __init__(self):
        self.bstack1ll1lll11ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll1ll1l111_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll11l1lll1_opy_(self):
        return (self.bstack1ll1lll11ll_opy_ != None and self.bin_session_id != None and self.bstack1ll1ll1l111_opy_ != None)
    def configure(self, bstack1ll1lll11ll_opy_, config, bin_session_id: str, bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_):
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll1ll1l111_opy_ = bstack1ll1ll1l111_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᓣ") + str(self.bin_session_id) + bstack1ll111_opy_ (u"ࠢࠣᓤ"))
    def bstack1l11ll1llll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll111_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᓥ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False