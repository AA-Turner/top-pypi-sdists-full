# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1l1l1_opy_ import bstack1111l1ll11_opy_
class bstack1llll111111_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_
    def __init__(self):
        self.bstack1lll1ll11ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1l1l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll1l1l1l_opy_(self):
        return (self.bstack1lll1ll11ll_opy_ != None and self.bin_session_id != None and self.bstack1111l1l1l1_opy_ != None)
    def configure(self, bstack1lll1ll11ll_opy_, config, bin_session_id: str, bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_):
        self.bstack1lll1ll11ll_opy_ = bstack1lll1ll11ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᆢ") + str(self.bin_session_id) + bstack1l11lll_opy_ (u"ࠢࠣᆣ"))
    def bstack1ll1ll1l11l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l11lll_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᆤ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False