# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll11l11_opy_
class bstack1l11ll1l111_opy_(abc.ABC):
    bin_session_id: str
    bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_
    def __init__(self):
        self.bstack1ll11ll11l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1l1lll11ll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l1l1l111ll_opy_(self):
        return (self.bstack1ll11ll11l_opy_ != None and self.bin_session_id != None and self.bstack1l1lll11ll1_opy_ != None)
    def configure(self, bstack1ll11ll11l_opy_, config, bin_session_id: str, bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_):
        self.bstack1ll11ll11l_opy_ = bstack1ll11ll11l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1l1lll11ll1_opy_ = bstack1l1lll11ll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1ll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᚦ") + str(self.bin_session_id) + bstack1ll_opy_ (u"ࠥࠦᚧ"))
    def bstack1l111l1ll11_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1ll_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨᚨ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False