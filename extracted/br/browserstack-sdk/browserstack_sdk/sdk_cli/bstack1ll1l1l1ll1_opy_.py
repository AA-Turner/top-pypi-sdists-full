# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack1111111lll_opy_
class bstack1ll1l1ll1ll_opy_(abc.ABC):
    bin_session_id: str
    bstack111111l1l1_opy_: bstack1111111lll_opy_
    def __init__(self):
        self.bstack1lll1l1l1ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111l1l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll1l1ll1l1_opy_(self):
        return (self.bstack1lll1l1l1ll_opy_ != None and self.bin_session_id != None and self.bstack111111l1l1_opy_ != None)
    def configure(self, bstack1lll1l1l1ll_opy_, config, bin_session_id: str, bstack111111l1l1_opy_: bstack1111111lll_opy_):
        self.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111l1l1_opy_ = bstack111111l1l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstackl_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣቁ") + str(self.bin_session_id) + bstackl_opy_ (u"ࠧࠨቂ"))
    def bstack1ll111llll1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstackl_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣቃ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False