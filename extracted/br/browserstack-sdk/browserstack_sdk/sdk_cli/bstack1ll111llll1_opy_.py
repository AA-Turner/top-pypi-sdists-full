# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
class bstack1l1llll1l11_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_
    def __init__(self):
        self.bstack1l1ll1l1ll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll1l11l1l1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1l1ll111l_opy_(self):
        return (self.bstack1l1ll1l1ll1_opy_ != None and self.bin_session_id != None and self.bstack1ll1l11l1l1_opy_ != None)
    def configure(self, bstack1l1ll1l1ll1_opy_, config, bin_session_id: str, bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_):
        self.bstack1l1ll1l1ll1_opy_ = bstack1l1ll1l1ll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᕏ") + str(self.bin_session_id) + bstack1ll1lll_opy_ (u"ࠥࠦᕐ"))
    def bstack1l11l1ll111_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᕑ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False