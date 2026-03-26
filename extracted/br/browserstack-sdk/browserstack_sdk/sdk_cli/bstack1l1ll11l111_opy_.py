# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll1l1111ll_opy_ import bstack1ll11lllll1_opy_
class bstack1ll111l11ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_
    def __init__(self):
        self.bstack1l1llll1lll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll1l1111ll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll111l1l11_opy_(self):
        return (self.bstack1l1llll1lll_opy_ != None and self.bin_session_id != None and self.bstack1ll1l1111ll_opy_ != None)
    def configure(self, bstack1l1llll1lll_opy_, config, bin_session_id: str, bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_):
        self.bstack1l1llll1lll_opy_ = bstack1l1llll1lll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll1l1111ll_opy_ = bstack1ll1l1111ll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡯ࡲࡨࡺࡲࡥࠡࡽࡶࡩࡱ࡬࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡ࠱ࡣࡤࡴࡡ࡮ࡧࡢࡣࢂࡀࠠࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᕧ") + str(self.bin_session_id) + bstack1ll1lll_opy_ (u"ࠨࠢᕨ"))
    def bstack1l11l1l111l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠢࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡓࡵ࡮ࡦࠤᕩ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False