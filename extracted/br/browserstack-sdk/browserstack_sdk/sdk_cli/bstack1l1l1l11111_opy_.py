# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll11llll11_opy_ import bstack1ll11llllll_opy_
class bstack1ll111l11ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll11llll11_opy_: bstack1ll11llllll_opy_
    def __init__(self):
        self.bstack1l1ll1ll111_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll11llll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1l1l11lll_opy_(self):
        return (self.bstack1l1ll1ll111_opy_ != None and self.bin_session_id != None and self.bstack1ll11llll11_opy_ != None)
    def configure(self, bstack1l1ll1ll111_opy_, config, bin_session_id: str, bstack1ll11llll11_opy_: bstack1ll11llllll_opy_):
        self.bstack1l1ll1ll111_opy_ = bstack1l1ll1ll111_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll11llll11_opy_ = bstack1ll11llll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᕸ") + str(self.bin_session_id) + bstack1ll11_opy_ (u"ࠤࠥᕹ"))
    def bstack1l1l1111l11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll11_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧᕺ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False