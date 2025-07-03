# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack111111l1l1_opy_
class bstack1lll11l1111_opy_(abc.ABC):
    bin_session_id: str
    bstack1111111ll1_opy_: bstack111111l1l1_opy_
    def __init__(self):
        self.bstack1llll11l1l1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111111ll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll1ll11111_opy_(self):
        return (self.bstack1llll11l1l1_opy_ != None and self.bin_session_id != None and self.bstack1111111ll1_opy_ != None)
    def configure(self, bstack1llll11l1l1_opy_, config, bin_session_id: str, bstack1111111ll1_opy_: bstack111111l1l1_opy_):
        self.bstack1llll11l1l1_opy_ = bstack1llll11l1l1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧሾ") + str(self.bin_session_id) + bstack1l1_opy_ (u"ࠤࠥሿ"))
    def bstack1ll1l111ll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧቀ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False