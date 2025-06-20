# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack111111ll1l_opy_
class bstack1ll1ll1llll_opy_(abc.ABC):
    bin_session_id: str
    bstack111111l1ll_opy_: bstack111111ll1l_opy_
    def __init__(self):
        self.bstack1llll1l1l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111l1ll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1ll1l1l_opy_(self):
        return (self.bstack1llll1l1l11_opy_ != None and self.bin_session_id != None and self.bstack111111l1ll_opy_ != None)
    def configure(self, bstack1llll1l1l11_opy_, config, bin_session_id: str, bstack111111l1ll_opy_: bstack111111ll1l_opy_):
        self.bstack1llll1l1l11_opy_ = bstack1llll1l1l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111l1ll_opy_ = bstack111111l1ll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᇦ") + str(self.bin_session_id) + bstack11ll11_opy_ (u"ࠧࠨᇧ"))
    def bstack1ll1l1l1111_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11ll11_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣᇨ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False