# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
class bstack1ll1l1llll1_opy_(abc.ABC):
    bin_session_id: str
    bstack1111111ll1_opy_: bstack11111111ll_opy_
    def __init__(self):
        self.bstack1lll111111l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111111ll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1111lll_opy_(self):
        return (self.bstack1lll111111l_opy_ != None and self.bin_session_id != None and self.bstack1111111ll1_opy_ != None)
    def configure(self, bstack1lll111111l_opy_, config, bin_session_id: str, bstack1111111ll1_opy_: bstack11111111ll_opy_):
        self.bstack1lll111111l_opy_ = bstack1lll111111l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥቊ") + str(self.bin_session_id) + bstack1l11ll1_opy_ (u"ࠢࠣቋ"))
    def bstack1ll11l111l1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l11ll1_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥቌ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False