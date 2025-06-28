# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack111111llll_opy_
class bstack1llll1111ll_opy_(abc.ABC):
    bin_session_id: str
    bstack111111ll11_opy_: bstack111111llll_opy_
    def __init__(self):
        self.bstack1lll1l111l1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111111ll11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll11ll11l_opy_(self):
        return (self.bstack1lll1l111l1_opy_ != None and self.bin_session_id != None and self.bstack111111ll11_opy_ != None)
    def configure(self, bstack1lll1l111l1_opy_, config, bin_session_id: str, bstack111111ll11_opy_: bstack111111llll_opy_):
        self.bstack1lll1l111l1_opy_ = bstack1lll1l111l1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨࠥࡳ࡯ࡥࡷ࡯ࡩࠥࢁࡳࡦ࡮ࡩ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥ࠮ࡠࡡࡱࡥࡲ࡫࡟ࡠࡿ࠽ࠤࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨሇ") + str(self.bin_session_id) + bstack1l1ll1_opy_ (u"ࠥࠦለ"))
    def bstack1ll111ll1ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1ll1_opy_ (u"ࠦࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡩࡡ࡯ࡰࡲࡸࠥࡨࡥࠡࡐࡲࡲࡪࠨሉ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False