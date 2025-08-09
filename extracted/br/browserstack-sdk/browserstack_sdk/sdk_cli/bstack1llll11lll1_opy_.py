# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack111111l11l_opy_
class bstack1llll11l11l_opy_(abc.ABC):
    bin_session_id: str
    bstack111111ll11_opy_: bstack111111l11l_opy_
    def __init__(self):
        self.bstack1ll1llllll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111ll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll1l1ll1_opy_(self):
        return (self.bstack1ll1llllll1_opy_ != None and self.bin_session_id != None and self.bstack111111ll11_opy_ != None)
    def configure(self, bstack1ll1llllll1_opy_, config, bin_session_id: str, bstack111111ll11_opy_: bstack111111l11l_opy_):
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11l1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣቁ") + str(self.bin_session_id) + bstack11l1_opy_ (u"ࠧࠨቂ"))
    def bstack1ll11llllll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11l1_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣቃ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False