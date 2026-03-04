# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1ll1lllll1l_opy_
class bstack1ll11l1ll11_opy_(abc.ABC):
    bin_session_id: str
    bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_
    def __init__(self):
        self.bstack1lll111lll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lll111111l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll111lllll_opy_(self):
        return (self.bstack1lll111lll1_opy_ != None and self.bin_session_id != None and self.bstack1lll111111l_opy_ != None)
    def configure(self, bstack1lll111lll1_opy_, config, bin_session_id: str, bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_):
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lll111111l_opy_ = bstack1lll111111l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᑺ") + str(self.bin_session_id) + bstack1lll1l_opy_ (u"ࠢࠣᑻ"))
    def bstack1l1l1111ll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1lll1l_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᑼ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False