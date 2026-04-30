# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll111l1_opy_
class bstack1l1l1111111_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_
    def __init__(self):
        self.bstack11l1ll1lll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1lll11l1l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l11l1l11ll_opy_(self):
        return (self.bstack11l1ll1lll_opy_ != None and self.bin_session_id != None and self.bstack1l1lll11l1l_opy_ != None)
    def configure(self, bstack11l1ll1lll_opy_, config, bin_session_id: str, bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_):
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1lll11l1l_opy_ = bstack1l1lll11l1l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᛁ") + str(self.bin_session_id) + bstack1l1111l_opy_ (u"ࠤࠥᛂ"))
    def bstack1l1111l1ll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1111l_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧᛃ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False