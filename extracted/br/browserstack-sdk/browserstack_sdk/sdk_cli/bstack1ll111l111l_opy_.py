# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1lll1lllll1_opy_
class bstack1ll1ll111l1_opy_(abc.ABC):
    bin_session_id: str
    bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_
    def __init__(self):
        self.bstack1ll1111l1ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lll1llll1l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll11l1lll1_opy_(self):
        return (self.bstack1ll1111l1ll_opy_ != None and self.bin_session_id != None and self.bstack1lll1llll1l_opy_ != None)
    def configure(self, bstack1ll1111l1ll_opy_, config, bin_session_id: str, bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_):
        self.bstack1ll1111l1ll_opy_ = bstack1ll1111l1ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lll1llll1l_opy_ = bstack1lll1llll1l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡯ࡲࡨࡺࡲࡥࠡࡽࡶࡩࡱ࡬࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡ࠱ࡣࡤࡴࡡ࡮ࡧࡢࡣࢂࡀࠠࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤጾ") + str(self.bin_session_id) + bstack1l1111_opy_ (u"ࠨࠢጿ"))
    def bstack1l1lllllll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1111_opy_ (u"ࠢࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡓࡵ࡮ࡦࠤፀ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False