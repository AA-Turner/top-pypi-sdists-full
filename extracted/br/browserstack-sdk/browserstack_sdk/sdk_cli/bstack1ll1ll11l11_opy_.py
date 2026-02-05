# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll1llll1l_opy_
class bstack1ll1l11l1ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_
    def __init__(self):
        self.bstack1ll1llll1ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lll1llll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll11l1l11l_opy_(self):
        return (self.bstack1ll1llll1ll_opy_ != None and self.bin_session_id != None and self.bstack1lll1llll11_opy_ != None)
    def configure(self, bstack1ll1llll1ll_opy_, config, bin_session_id: str, bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_):
        self.bstack1ll1llll1ll_opy_ = bstack1ll1llll1ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣፄ") + str(self.bin_session_id) + bstack11l1ll1_opy_ (u"ࠧࠨፅ"))
    def bstack1l1lll1ll1l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11l1ll1_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣፆ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False