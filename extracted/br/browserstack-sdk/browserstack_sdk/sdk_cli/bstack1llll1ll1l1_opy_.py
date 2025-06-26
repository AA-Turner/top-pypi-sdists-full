# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111ll11_opy_
class bstack1lll1ll1l1l_opy_(abc.ABC):
    bin_session_id: str
    bstack111111lll1_opy_: bstack111111ll11_opy_
    def __init__(self):
        self.bstack1lll1l1ll1l_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111lll1_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1ll1ll1_opy_(self):
        return (self.bstack1lll1l1ll1l_opy_ != None and self.bin_session_id != None and self.bstack111111lll1_opy_ != None)
    def configure(self, bstack1lll1l1ll1l_opy_, config, bin_session_id: str, bstack111111lll1_opy_: bstack111111ll11_opy_):
        self.bstack1lll1l1ll1l_opy_ = bstack1lll1l1ll1l_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111lll1_opy_ = bstack111111lll1_opy_
        if self.bin_session_id:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨሇ") + str(self.bin_session_id) + bstack11ll1l1_opy_ (u"ࠥࠦለ"))
    def bstack1ll11llllll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack11ll1l1_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨሉ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False