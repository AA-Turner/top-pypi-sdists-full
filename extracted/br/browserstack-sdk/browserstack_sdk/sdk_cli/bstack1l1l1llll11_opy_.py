# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1ll1ll11l11_opy_
class bstack1ll1111l1ll_opy_(abc.ABC):
    bin_session_id: str
    bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_
    def __init__(self):
        self.bstack1ll1ll1lll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1ll1ll11lll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1lllll111_opy_(self):
        return (self.bstack1ll1ll1lll1_opy_ != None and self.bin_session_id != None and self.bstack1ll1ll11lll_opy_ != None)
    def configure(self, bstack1ll1ll1lll1_opy_, config, bin_session_id: str, bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_):
        self.bstack1ll1ll1lll1_opy_ = bstack1ll1ll1lll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1ll1ll11lll_opy_ = bstack1ll1ll11lll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1111l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᔞ") + str(self.bin_session_id) + bstack1111l_opy_ (u"ࠥࠦᔟ"))
    def bstack1l1l111l1ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1111l_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᔠ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False