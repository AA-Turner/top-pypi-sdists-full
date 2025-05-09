# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1ll11_opy_
class bstack1lll1l1lll1_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1l1ll_opy_: bstack1111l1ll11_opy_
    def __init__(self):
        self.bstack1llllll1l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1l1ll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lllll1111l_opy_(self):
        return (self.bstack1llllll1l11_opy_ != None and self.bin_session_id != None and self.bstack1111l1l1ll_opy_ != None)
    def configure(self, bstack1llllll1l11_opy_, config, bin_session_id: str, bstack1111l1l1ll_opy_: bstack1111l1ll11_opy_):
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᆢ") + str(self.bin_session_id) + bstack11lll_opy_ (u"ࠢࠣᆣ"))
    def bstack1ll11llll11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11lll_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᆤ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False