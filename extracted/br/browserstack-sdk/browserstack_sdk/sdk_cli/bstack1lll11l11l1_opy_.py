# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111l111_opy_ import bstack1111111lll_opy_
class bstack1llll11l111_opy_(abc.ABC):
    bin_session_id: str
    bstack111111l111_opy_: bstack1111111lll_opy_
    def __init__(self):
        self.bstack1lll1llll11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111l111_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll11l1l1_opy_(self):
        return (self.bstack1lll1llll11_opy_ != None and self.bin_session_id != None and self.bstack111111l111_opy_ != None)
    def configure(self, bstack1lll1llll11_opy_, config, bin_session_id: str, bstack111111l111_opy_: bstack1111111lll_opy_):
        self.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111l111_opy_ = bstack111111l111_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢቇ") + str(self.bin_session_id) + bstack1111lll_opy_ (u"ࠦࠧቈ"))
    def bstack1ll1l111lll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1111lll_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢ቉"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False