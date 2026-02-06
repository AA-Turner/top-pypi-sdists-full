# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1lll11l1lll_opy_
class bstack1lll1l1l1l1_opy_(abc.ABC):
    bin_session_id: str
    bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_
    def __init__(self):
        self.bstack1ll1l1l1ll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lll11ll111_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll11l11111_opy_(self):
        return (self.bstack1ll1l1l1ll1_opy_ != None and self.bin_session_id != None and self.bstack1lll11ll111_opy_ != None)
    def configure(self, bstack1ll1l1l1ll1_opy_, config, bin_session_id: str, bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_):
        self.bstack1ll1l1l1ll1_opy_ = bstack1ll1l1l1ll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lll11ll111_opy_ = bstack1lll11ll111_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥ።") + str(self.bin_session_id) + bstack11lllll_opy_ (u"ࠢࠣ፣"))
    def bstack1l1ll1l11ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11lllll_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥ፤"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False