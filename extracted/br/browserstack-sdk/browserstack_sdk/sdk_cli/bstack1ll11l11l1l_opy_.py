# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll1111111_opy_
class bstack1ll111l1l1l_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_
    def __init__(self):
        self.bstack1lll111l111_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll1lllll1l_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1ll111111ll_opy_(self):
        return (self.bstack1lll111l111_opy_ != None and self.bin_session_id != None and self.bstack1ll1lllll1l_opy_ != None)
    def configure(self, bstack1lll111l111_opy_, config, bin_session_id: str, bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_):
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡱࡴࡪࡵ࡭ࡧࠣࡿࡸ࡫࡬ࡧ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣ࠳ࡥ࡟࡯ࡣࡰࡩࡤࡥࡽ࠻ࠢࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦᑻ") + str(self.bin_session_id) + bstack1111_opy_ (u"ࠣࠤᑼ"))
    def bstack1l1l111ll1l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1111_opy_ (u"ࠤࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡎࡰࡰࡨࠦᑽ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False