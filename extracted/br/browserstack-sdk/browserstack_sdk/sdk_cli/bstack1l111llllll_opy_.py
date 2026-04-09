# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll1l11l_opy_
class bstack1l11ll11111_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_
    def __init__(self):
        self.bstack1l1l111l1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1lll11ll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1l1llll11_opy_(self):
        return (self.bstack1l1l111l1_opy_ != None and self.bin_session_id != None and self.bstack1l1lll11ll1_opy_ != None)
    def configure(self, bstack1l1l111l1_opy_, config, bin_session_id: str, bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_):
        self.bstack1l1l111l1_opy_ = bstack1l1l111l1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1lll11ll1_opy_ = bstack1l1lll11ll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᚦ") + str(self.bin_session_id) + bstack11ll11_opy_ (u"ࠥࠦᚧ"))
    def bstack1l11111l1l1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11ll11_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᚨ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False