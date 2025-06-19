# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack11111lll11_opy_ import bstack11111ll11l_opy_
class bstack1lll1l11ll1_opy_(abc.ABC):
    bin_session_id: str
    bstack11111lll11_opy_: bstack11111ll11l_opy_
    def __init__(self):
        self.bstack1lll1ll1l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack11111lll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1l11lll_opy_(self):
        return (self.bstack1lll1ll1l11_opy_ != None and self.bin_session_id != None and self.bstack11111lll11_opy_ != None)
    def configure(self, bstack1lll1ll1l11_opy_, config, bin_session_id: str, bstack11111lll11_opy_: bstack11111ll11l_opy_):
        self.bstack1lll1ll1l11_opy_ = bstack1lll1ll1l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack11111lll11_opy_ = bstack11111lll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᇘ") + str(self.bin_session_id) + bstack111lll_opy_ (u"ࠧࠨᇙ"))
    def bstack1ll11ll1l11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack111lll_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣᇚ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False