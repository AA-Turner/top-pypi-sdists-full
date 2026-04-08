# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
class bstack1l111111l1l_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_
    def __init__(self):
        self.bstack11l11lll11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1l1ll11l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l11l1lll1l_opy_(self):
        return (self.bstack11l11lll11_opy_ != None and self.bin_session_id != None and self.bstack1l1l1ll11l1_opy_ != None)
    def configure(self, bstack11l11lll11_opy_, config, bin_session_id: str, bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_):
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1l1ll11l1_opy_ = bstack1l1l1ll11l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack111l_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦ࡭ࡰࡦࡸࡰࡪࠦࡻࡴࡧ࡯ࡪ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟࠯ࡡࡢࡲࡦࡳࡥࡠࡡࢀ࠾ࠥࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢ᜺") + str(self.bin_session_id) + bstack111l_opy_ (u"ࠦࠧ᜻"))
    def bstack11lllll1111_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack111l_opy_ (u"ࠧࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡣࡢࡰࡱࡳࡹࠦࡢࡦࠢࡑࡳࡳ࡫ࠢ᜼"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False