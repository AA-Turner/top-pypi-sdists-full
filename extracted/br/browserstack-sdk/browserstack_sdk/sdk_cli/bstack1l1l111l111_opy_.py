# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1lll1111l_opy_
class bstack1l11l1l11ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_
    def __init__(self):
        self.bstack111111ll1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1ll1llll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1l1l1lll1_opy_(self):
        return (self.bstack111111ll1l_opy_ != None and self.bin_session_id != None and self.bstack1l1ll1llll1_opy_ != None)
    def configure(self, bstack111111ll1l_opy_, config, bin_session_id: str, bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_):
        self.bstack111111ll1l_opy_ = bstack111111ll1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1ll1llll1_opy_ = bstack1l1ll1llll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack111ll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᛐ") + str(self.bin_session_id) + bstack111ll_opy_ (u"ࠥࠦᛑ"))
    def bstack11llllll111_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack111ll_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᛒ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False