# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111l1l1_opy_
class bstack1llll11l1ll_opy_(abc.ABC):
    bin_session_id: str
    bstack111111lll1_opy_: bstack111111l1l1_opy_
    def __init__(self):
        self.bstack1ll1ll111l1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111lll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll11l1l1l_opy_(self):
        return (self.bstack1ll1ll111l1_opy_ != None and self.bin_session_id != None and self.bstack111111lll1_opy_ != None)
    def configure(self, bstack1ll1ll111l1_opy_, config, bin_session_id: str, bstack111111lll1_opy_: bstack111111l1l1_opy_):
        self.bstack1ll1ll111l1_opy_ = bstack1ll1ll111l1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111lll1_opy_ = bstack111111lll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡯ࡲࡨࡺࡲࡥࠡࡽࡶࡩࡱ࡬࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡ࠱ࡣࡤࡴࡡ࡮ࡧࡢࡣࢂࡀࠠࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᇧ") + str(self.bin_session_id) + bstack1l1l1l1_opy_ (u"ࠨࠢᇨ"))
    def bstack1ll11l1l1ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1l1l1_opy_ (u"ࠢࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡓࡵ࡮ࡦࠤᇩ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False