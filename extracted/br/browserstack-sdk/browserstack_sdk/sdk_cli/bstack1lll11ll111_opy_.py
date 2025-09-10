# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
class bstack1ll1l1l11l1_opy_(abc.ABC):
    bin_session_id: str
    bstack1111111ll1_opy_: bstack11111111ll_opy_
    def __init__(self):
        self.bstack1ll1llllll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111111ll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll11ll1l_opy_(self):
        return (self.bstack1ll1llllll1_opy_ != None and self.bin_session_id != None and self.bstack1111111ll1_opy_ != None)
    def configure(self, bstack1ll1llllll1_opy_, config, bin_session_id: str, bstack1111111ll1_opy_: bstack11111111ll_opy_):
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡱࡴࡪࡵ࡭ࡧࠣࡿࡸ࡫࡬ࡧ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣ࠳ࡥ࡟࡯ࡣࡰࡩࡤࡥࡽ࠻ࠢࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦቋ") + str(self.bin_session_id) + bstack1ll11ll_opy_ (u"ࠣࠤቌ"))
    def bstack1ll11l11lll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll11ll_opy_ (u"ࠤࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡎࡰࡰࡨࠦቍ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False