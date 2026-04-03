# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1lll11l11_opy_ import bstack1l1lll11ll1_opy_
class bstack1l11lll1l1l_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_
    def __init__(self):
        self.bstack1llll11l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1lll11l11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l11lllll11_opy_(self):
        return (self.bstack1llll11l11_opy_ != None and self.bin_session_id != None and self.bstack1l1lll11l11_opy_ != None)
    def configure(self, bstack1llll11l11_opy_, config, bin_session_id: str, bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_):
        self.bstack1llll11l11_opy_ = bstack1llll11l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᚦ") + str(self.bin_session_id) + bstack1ll1l11_opy_ (u"ࠥࠦᚧ"))
    def bstack1l11111111l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll1l11_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᚨ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False