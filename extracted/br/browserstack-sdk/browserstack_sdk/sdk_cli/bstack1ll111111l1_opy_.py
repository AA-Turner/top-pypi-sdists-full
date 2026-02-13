# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lll11l111l_opy_
class bstack1l1ll1lll11_opy_(abc.ABC):
    bin_session_id: str
    bstack1lll111lll1_opy_: bstack1lll11l111l_opy_
    def __init__(self):
        self.bstack1ll1l1l1lll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lll111lll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll11111ll1_opy_(self):
        return (self.bstack1ll1l1l1lll_opy_ != None and self.bin_session_id != None and self.bstack1lll111lll1_opy_ != None)
    def configure(self, bstack1ll1l1l1lll_opy_, config, bin_session_id: str, bstack1lll111lll1_opy_: bstack1lll11l111l_opy_):
        self.bstack1ll1l1l1lll_opy_ = bstack1ll1l1l1lll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡼࡵࡨࡰ࡫࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠ࠰ࡢࡣࡳࡧ࡭ࡦࡡࡢࢁ࠿ࠦࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᏥ") + str(self.bin_session_id) + bstack11l11_opy_ (u"ࠧࠨᏦ"))
    def bstack1l1l11l1111_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11l11_opy_ (u"ࠨࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡤࡣࡱࡲࡴࡺࠠࡣࡧࠣࡒࡴࡴࡥࠣᏧ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False