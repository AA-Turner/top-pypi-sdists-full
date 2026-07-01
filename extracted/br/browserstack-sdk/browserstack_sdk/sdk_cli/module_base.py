# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import logging
import abc
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
class BaseModule(abc.ABC):
    bin_session_id: str
    async_dispatcher: AsyncDispatcher
    def __init__(self):
        self.cli_service = None
        self.config = None
        self.bin_session_id = None
        self.async_dispatcher = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1l11l1ll111_opy_(self):
        return (self.cli_service != None and self.bin_session_id != None and self.async_dispatcher != None)
    def configure(self, cli_service, config, bin_session_id: str, async_dispatcher: AsyncDispatcher):
        self.cli_service = cli_service
        self.config = config
        self.bin_session_id = bin_session_id
        self.async_dispatcher = async_dispatcher
        if self.bin_session_id:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡱࡴࡪࡵ࡭ࡧࠣࡿࡸ࡫࡬ࡧ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣ࠳ࡥ࡟࡯ࡣࡰࡩࡤࡥࡽ࠻ࠢࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦᦊ") + str(self.bin_session_id) + bstack1l1llll_opy_ (u"ࠣࠤᦋ"))
    def ensure_bin_session(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1llll_opy_ (u"ࠤࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡎࡰࡰࡨࠦᦌ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False