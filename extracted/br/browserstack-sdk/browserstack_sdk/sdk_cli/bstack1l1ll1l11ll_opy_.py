# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
class bstack1l1lllllll1_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_
    def __init__(self):
        self.bstack1l1lll11l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll1l11l1l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1llll1l11_opy_(self):
        return (self.bstack1l1lll11l11_opy_ != None and self.bin_session_id != None and self.bstack1ll1l11l1l1_opy_ != None)
    def configure(self, bstack1l1lll11l11_opy_, config, bin_session_id: str, bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_):
        self.bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᕓ") + str(self.bin_session_id) + bstack11lll1_opy_ (u"ࠢࠣᕔ"))
    def bstack1l1l1111l1l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11lll1_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥᕕ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False