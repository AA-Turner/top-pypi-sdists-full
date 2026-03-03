# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lll11lll11_opy_
class bstack1ll1l1l11l1_opy_(abc.ABC):
    bin_session_id: str
    bstack1lll11llll1_opy_: bstack1lll11lll11_opy_
    def __init__(self):
        self.bstack1l1llllll1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lll11llll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1lll11lll_opy_(self):
        return (self.bstack1l1llllll1l_opy_ != None and self.bin_session_id != None and self.bstack1lll11llll1_opy_ != None)
    def configure(self, bstack1l1llllll1l_opy_, config, bin_session_id: str, bstack1lll11llll1_opy_: bstack1lll11lll11_opy_):
        self.bstack1l1llllll1l_opy_ = bstack1l1llllll1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lll11llll1_opy_ = bstack1lll11llll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᏬ") + str(self.bin_session_id) + bstack11ll111_opy_ (u"ࠧࠨᏭ"))
    def bstack1l1l11llll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11ll111_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣᏮ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False