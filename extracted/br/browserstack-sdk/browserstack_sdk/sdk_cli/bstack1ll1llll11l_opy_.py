# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111lll_opy_
class bstack1lll1lll111_opy_(abc.ABC):
    bin_session_id: str
    bstack1111111ll1_opy_: bstack1111111lll_opy_
    def __init__(self):
        self.bstack1ll1ll11l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111111ll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1ll1ll1_opy_(self):
        return (self.bstack1ll1ll11l11_opy_ != None and self.bin_session_id != None and self.bstack1111111ll1_opy_ != None)
    def configure(self, bstack1ll1ll11l11_opy_, config, bin_session_id: str, bstack1111111ll1_opy_: bstack1111111lll_opy_):
        self.bstack1ll1ll11l11_opy_ = bstack1ll1ll11l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤࡲࡵࡤࡶ࡮ࡨࠤࢀࡹࡥ࡭ࡨ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤ࠴࡟ࡠࡰࡤࡱࡪࡥ࡟ࡾ࠼ࠣࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧቌ") + str(self.bin_session_id) + bstack1111l1l_opy_ (u"ࠤࠥቍ"))
    def bstack1ll1l1111ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1111l1l_opy_ (u"ࠥࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠤࡨࡧ࡮࡯ࡱࡷࠤࡧ࡫ࠠࡏࡱࡱࡩࠧ቎"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False