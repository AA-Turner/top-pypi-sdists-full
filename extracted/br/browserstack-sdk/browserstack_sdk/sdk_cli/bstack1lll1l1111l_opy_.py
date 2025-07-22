# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import bstack111111l1l1_opy_
class bstack1llll1l1l11_opy_(abc.ABC):
    bin_session_id: str
    bstack1111111lll_opy_: bstack111111l1l1_opy_
    def __init__(self):
        self.bstack1lll1l11l1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111111lll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll1ll111l1_opy_(self):
        return (self.bstack1lll1l11l1l_opy_ != None and self.bin_session_id != None and self.bstack1111111lll_opy_ != None)
    def configure(self, bstack1lll1l11l1l_opy_, config, bin_session_id: str, bstack1111111lll_opy_: bstack111111l1l1_opy_):
        self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111111lll_opy_ = bstack1111111lll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢቀ") + str(self.bin_session_id) + bstack111l111_opy_ (u"ࠦࠧቁ"))
    def bstack1ll111l1l11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack111l111_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢቂ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False