# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l111l1lll_opy_ import bstack1lll11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1l11lll1_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack11ll11l1_opy_, bstack11lll111_opy_, bstack1l11l11l1_opy_
from browserstack_sdk.sdk_cli.bstack11llllll11_opy_ import bstack11llllll11_opy_, Events, bstack1l1llll1_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1ll1ll1l11l_opy_
    _1ll1l1l111l_opy_ = bstack1ll1ll1l11l_opy_.VERSION
except:
    _1ll1l1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫቸ")
cli_context = bstack1ll1l11lll1_opy_(
    test_framework_name=bstack1ll1lll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪቹ"),
    test_framework_version=_1ll1l1l111l_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1ll1lll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠬቺ"), bstack1ll1lll_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠥࡩ࡯࡯ࡶࡨࡼࡹ࠭ቻ"), bstack1ll1lll_opy_ (u"ࠧࡤ࡮ࡲࡷࡪࠦࡰࡢࡩࡨࠫቼ"),
        bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠩች"), bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࠱ࡧࡱࡵࡳࡦࠢࡦࡳࡳࡺࡥࡹࡶࠪቾ"), bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡲ࡯ࡴࡧࠣࡴࡦ࡭ࡥࠨቿ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1ll1lll_opy_ (u"ࠫࡳ࡫ࡷࠡࡤࡵࡳࡼࡹࡥࡳࠩኀ"), bstack1ll1lll_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࠦࡴࡰࠢࡥࡶࡴࡽࡳࡦࡴࠪኁ"),
        bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮࡯ࡧࡺࠤࡧࡸ࡯ࡸࡵࡨࡶࠬኂ"), bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥࡲࡲࡳ࡫ࡣࡵࠢࡷࡳࠥࡨࡲࡰࡹࡶࡩࡷ࠭ኃ"),
    }
    def __init__(self):
        self._1ll1ll1l111_opy_ = None
        self._1ll1l111l11_opy_ = False
        self._1ll1l1ll1l1_opy_ = False
        self._current_test_name = None
        self._1ll1l11l1l1_opy_ = None
        self._1ll1ll1lll1_opy_ = False
        if cli.bstack1l11lll1l_opy_():
            try:
                if cli.bstack111l11ll11_opy_:
                    cli_context.platform_index = cli.bstack111l11ll11_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨኄ"), bstack1ll1lll_opy_ (u"ࠩ࠳ࠫኅ")))
            except Exception as e:
                pass
        PlaywrightPatcher._1ll1l1l11ll_opy_()
    @staticmethod
    def _1ll1l1l11ll_opy_():
        try:
            import functools
            from Browser.keywords.bstack1llllllll11_opy_ import bstack1ll1ll1l1ll_opy_
            from browserstack_sdk.sdk_cli.bstack1ll1l1l1l1l_opy_ import bstack1ll1ll1l1l1_opy_
            _1ll1l1l1lll_opy_ = bstack1ll1ll1l1ll_opy_.close_browser
            _1ll1ll11lll_opy_ = bstack1ll1ll1l1ll_opy_.bstack1ll1l1l1111_opy_
            @functools.wraps(_1ll1l1l1lll_opy_)
            def _1ll1ll11l11_opy_(self, browser=bstack1ll1lll_opy_ (u"ࠥࡇ࡚ࡘࡒࡆࡐࡗࠦኆ")):
                if not bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.is_set():
                    logger.debug(bstack1ll1lll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡢࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࡧ࠱࠲ࡻࠣࡷࡨࡧ࡮ࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸ࠲ࠠࡸࡣ࡬ࡸ࡮ࡴࡧࠡࡷࡳࠤࡹࡵࠠ࠲࠷ࡶࠦኇ"))
                    bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.wait(timeout=15)
                return _1ll1l1l1lll_opy_(self, browser)
            @functools.wraps(_1ll1ll11lll_opy_)
            def _1ll1l1ll11l_opy_(self, page=bstack1ll1lll_opy_ (u"ࠧࡉࡕࡓࡔࡈࡒ࡙ࠨኈ")):
                if not bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.is_set():
                    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡤࡶࡡࡨࡧ࠽ࠤࡦ࠷࠱ࡺࠢࡶࡧࡦࡴࠠࡪࡰࠣࡴࡷࡵࡧࡳࡧࡶࡷ࠱ࠦࡷࡢ࡫ࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡸࡴࠦ࠱࠶ࡵࠥ኉"))
                    bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.wait(timeout=15)
                return _1ll1ll11lll_opy_(self, page)
            bstack1ll1ll1l1ll_opy_.close_browser = _1ll1ll11l11_opy_
            bstack1ll1ll1l1ll_opy_.bstack1ll1l1l1111_opy_ = _1ll1l1ll11l_opy_
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡠࡲࡤࡸࡨ࡮࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡣࡨࡲ࡯ࡴࡧࡢࡱࡪࡺࡨࡰࡦࡶ࠾ࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡖࡸࡦࡺࡥࠡࡥ࡯ࡳࡸ࡫ࠠ࡮ࡧࡷ࡬ࡴࡪࡳࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣ࡫ࡦࡺࡥࠣኊ"))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡡࡳࡥࡹࡩࡨࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤࡩ࡬ࡰࡵࡨࡣࡲ࡫ࡴࡩࡱࡧࡷ࠿ࠦࡳ࡬࡫ࡳࡴࡪࡪࠠࠩࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡳࡷࠦࡡ࠲࠳ࡼࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠯࠺ࠡࡽࡨࢁࠧኋ").format(e=e))
    def _1ll1ll11111_opy_(self):
        if self._1ll1ll1l111_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1ll1ll1l111_opy_ = BuiltIn().get_library_instance(bstack1ll1lll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࠪኌ"))
            except Exception as e:
                logger.warning(bstack1ll1lll_opy_ (u"ࠥࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡧࡦࡶࠣࡆࡷࡵࡷࡴࡧࡵࠤࡱ࡯ࡢࡳࡣࡵࡽࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠺ࠡࡽࡨࢁࠧኍ").format(e=e))
        return self._1ll1ll1l111_opy_
    def _1ll1l1ll1ll_opy_(self):
        try:
            bstack1lllllllll1_opy_ = self._1ll1ll11111_opy_()
            if bstack1lllllllll1_opy_ and hasattr(bstack1lllllllll1_opy_, bstack1ll1lll_opy_ (u"ࠫࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡶࡸࡦࡺࡥࠨ኎")):
                bstack1llllllll11_opy_ = bstack1lllllllll1_opy_._playwright_state
                if hasattr(bstack1llllllll11_opy_, bstack1ll1lll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡧࡴࡢ࡮ࡲ࡫ࠬ኏")):
                    bstack1llllllll1l_opy_ = bstack1llllllll11_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1llllllll1l_opy_ = BuiltIn().run_keyword(bstack1ll1lll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸ࠮ࡈࡧࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡉࡡࡵࡣ࡯ࡳ࡬࠭ነ"))
                for bstack1ll1ll1111l_opy_ in bstack1llllllll1l_opy_:
                    contexts = bstack1ll1ll1111l_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡤࡱࡱࡸࡪࡾࡴࡴࠩኑ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1ll1lll_opy_ (u"ࠨࡲࡤ࡫ࡪࡹࠧኒ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩ࠿ࠦࡻࡦࡿࠥና").format(e=e))
            return False
    def _1ll1l111l1l_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1ll1ll1ll1l_opy_ = {
                bstack1ll1lll_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪኔ"): action,
                bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧን"): arguments
            }
            executor_cmd = bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠨኖ") + json.dumps(bstack1ll1ll1ll1l_opy_)
            arg_string = bstack1ll1lll_opy_ (u"ࠨࡡࡳࡩࡀࡿࡪࡾࡥࡤࡷࡷࡳࡷࡥࡣ࡮ࡦࢀࠦኗ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1ll1lll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡇࡹࡥࡱࡻࡡࡵࡧࠣࡎࡦࡼࡡࡔࡥࡵ࡭ࡵࡺࠧኘ"),
                None,
                bstack1ll1lll_opy_ (u"ࠨࡡࠣࡁࡃࠦࡻࡾࠩኙ"),
                arg_string
            )
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡪࡩࡵࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡢࡥࡷ࡭ࡴࡴࡽ࠭ࠢࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡿࡷ࡫ࡳࡶ࡮ࡷࢁࠧኚ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡩࢂࠨኛ").format(e=e))
    def _populate_browser_instance_data(self):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡐࡰࡲࡸࡰࡦࡺࡥࠡࡪࡸࡦࡤࡻࡲ࡭ࠢࡤࡲࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡳࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠡࡨࡲࡶࠥࡸ࡯ࡣࡱࡷ࠱ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠯ࠤࠥࠦኜ")
        try:
            from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
            if not self._1ll1l1ll1ll_opy_():
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡲࡴࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠢኝ"))
                return
            result = self._1ll1l111l1l_opy_(bstack1ll1lll_opy_ (u"࠭ࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠪኞ"), {})
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡠࡲࡲࡴࡺࡲࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡤࡢࡶࡤ࠾ࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡸࡻ࡬ࡵ࠿ࡾࡶࢂࠨኟ").format(r=result))
            if not result:
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦ࡮ࡰࠢࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦአ"))
                return
            bstack1ll1ll1llll_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1ll1ll1llll_opy_.get(bstack1ll1lll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬኡ"), bstack1ll1lll_opy_ (u"ࠪࠫኢ"))
            hub_url = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡔࡈࡏࡕࡡࡓ࡛ࡤࡉࡄࡑࡡࡘࡖࡑ࠭ኣ"), bstack1ll1lll_opy_ (u"ࠬ࠭ኤ"))
            logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࡽࡶ࡭ࡩࢃࠬࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࡾࡹࡷࡲࡽࠣእ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1ll1lll_opy_ (u"ࠧࠨኦ")))
            current_test_id = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪኧ"), None)
            for instance in bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.values():
                if not bstack111l111ll_opy_.bstack1ll1l11llll_opy_(instance, bstack111l111ll_opy_.bstack1ll1ll111ll_opy_, None):
                    bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1ll1ll111ll_opy_, session_id)
                    bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1lll111l_opy_, hub_url)
                    if current_test_id:
                        bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪከ"), current_test_id)
                    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡔࡴࡶࡵ࡭ࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠼ࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࡼࡵ࡬ࡨࢂ࠲ࠠࡩࡷࡥࡣࡺࡸ࡬ࠡࡵࡨࡸ࠱ࠦࡴࡦࡵࡷࡣ࡮ࡪ࠽ࡼࡶ࡬ࡨࢂࠨኩ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱࡳࡹࡱࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡪࡡࡵࡣ࠽ࠤࢀ࡫ࡽࠣኪ").format(e=e))
    def _clear_session_data(self):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬ࡲࡰ࡯ࠣࡥࡱࡲࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࠤࡹࡵࠠࡦࡰࡶࡹࡷ࡫ࠠࡵࡧࡶࡸࠥ࡯ࡳࡰ࡮ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨካ")
        try:
            from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
            bstack1ll1l11l1ll_opy_ = 0
            for instance in bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.values():
                bstack1ll1l11l111_opy_ = False
                if bstack111l111ll_opy_.bstack1ll1l11llll_opy_(instance, bstack111l111ll_opy_.bstack1ll1ll111ll_opy_, None):
                    bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1ll1ll111ll_opy_, bstack1ll1lll_opy_ (u"࠭ࠧኬ"))
                    bstack1ll1l11l111_opy_ = True
                if bstack111l111ll_opy_.bstack1ll1l11llll_opy_(instance, bstack111l111ll_opy_.bstack1lll111l_opy_, None):
                    bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack1lll111l_opy_, bstack1ll1lll_opy_ (u"ࠧࠨክ"))
                    bstack1ll1l11l111_opy_ = True
                if bstack111l111ll_opy_.bstack1ll1l11llll_opy_(instance, bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡩࡥࠩኮ"), None):
                    bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪኯ"), None)
                    bstack1ll1l11l111_opy_ = True
                if bstack11ll11l1_opy_.bstack1ll1l1lll1l_opy_(instance, bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠨኰ")):
                    bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠩ኱"), None)
                    bstack1ll1l11l111_opy_ = True
                if bstack1ll1l11l111_opy_:
                    bstack1ll1l11l1ll_opy_ += 1
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡥࡣ࡭ࡧࡤࡶࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡤࡢࡶࡤ࠾ࠥࡉ࡬ࡦࡣࡵࡩࡩࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬ࡲࡰ࡯ࠣࡿࡳࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࠥኲ").format(
                n=bstack1ll1l11l1ll_opy_))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡰࡪࡧࡲࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡧࡥࡹࡧ࠺ࠡࡽࡨࢁࠧኳ").format(e=e))
    def _1ll1l111lll_opy_(self, status, reason=bstack1ll1lll_opy_ (u"ࠢࠣኴ")):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࡑࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡲࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦࠧࠨኵ")
        bstack1ll1l1l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ኶") if status == bstack1ll1lll_opy_ (u"ࠥࡔࡆ࡙ࡓࠣ኷") else bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦኸ")
        if bstack1ll1l1l1l11_opy_ == bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧኹ"):
            return self._1ll1l111l1l_opy_(bstack1ll1lll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤኺ"), {
                bstack1ll1lll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢኻ"): bstack1ll1l1l1l11_opy_,
                bstack1ll1lll_opy_ (u"ࠣࡴࡨࡥࡸࡵ࡮ࠣኼ"): reason
            })
        else:
            return self._1ll1l111l1l_opy_(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧኽ"), {
                bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥኾ"): bstack1ll1l1l1l11_opy_
            })
    def _1ll1l1ll111_opy_(self, name):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡓࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡲࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦࠧࠨ኿")
        return self._1ll1l111l1l_opy_(bstack1ll1lll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨዀ"), {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ዁"): name
        })
    def _1ll1l11ll1l_opy_(self):
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࡐࡥࡷࡱࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡶࡸࡦࡺࡵࡴࠢࡥࡩ࡫ࡵࡲࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡧࡱࡵࡳࡦࠢࡲࡶࠥࡺࡥࡢࡴࡧࡳࡼࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡸࡦࡺࡵࡴࠢ࡬ࡷࠥ࡯࡮ࡧࡧࡵࡶࡪࡪࠠࡧࡴࡲࡱࠥࡥ࡬ࡢࡵࡷࡣࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨ࠾ࠥ࡯ࡦࠡࡣࡱࡽࠥࡌࡁࡊࡎ࠰ࡰࡪࡼࡥ࡭ࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹࡤࡷࠥࡩࡡࡱࡶࡸࡶࡪࡪࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵ࠮ࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡯ࡳࠡࡨࡤ࡭ࡱ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢዂ")
        if self._1ll1l1ll1l1_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._current_test_name and not global_config.should_skip_session_name():
                self._1ll1l1ll111_opy_(self._current_test_name)
            status = bstack1ll1lll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ዃ") if self._1ll1l11l1l1_opy_ else bstack1ll1lll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧዄ")
            message = self._1ll1l11l1l1_opy_ or bstack1ll1lll_opy_ (u"ࠪࠫዅ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡒࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡣ࡭ࡱࡶࡩ࠿ࠦࡳࡵࡣࡷࡹࡸࡃࡻࡴࡶࡤࡸࡺࡹࡽ࠭ࠢࡰࡩࡸࡹࡡࡨࡧࡀࡿࡲ࡫ࡳࡴࡣࡪࡩࢂࠨ዆").format(status=status, message=message))
                self._1ll1l111lll_opy_(status, message)
            self._1ll1l1ll1l1_opy_ = True
            logger.debug(bstack1ll1lll_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡲࡧࡲ࡬ࡧࡧࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ዇"))
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࡩࢂࠨወ").format(e=e))
    def _extract_screenshot_base64(self, bstack1ll1ll11l1l_opy_):
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡥࡣࡷࡥࠥ࡬ࡲࡰ࡯ࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡎࡔࡎࡎࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡴࡨ࡯ࡵࠩࡶࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡲࡩࡣࡴࡤࡶࡾࠦ࡬ࡰࡩࡶࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠢࡤࡷࠥࡎࡔࡎࡎࠣࡻ࡮ࡺࡨࠡࡧ࡬ࡸ࡭࡫ࡲ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡋ࡭ࡣࡧࡧࡨࡪࡪ࠺ࠡ࠾࡬ࡱ࡬ࠦࡳࡳࡥࡀࠦࡩࡧࡴࡢ࠼࡬ࡱࡦ࡭ࡥ࠰ࡲࡱ࡫ࡀࡨࡡࡴࡧ࠹࠸࠱ࢁࡤࡢࡶࡤࢁࠧࠦ࠮࠯࠰ࡁࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇ࡫࡯ࡩࠥࡲࡩ࡯࡭࠽ࠤࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࡱࡣࡷ࡬࠴ࡺ࡯࠰ࡨ࡬ࡰࡪ࠴ࡰ࡯ࡩࠥࠤ࠳࠴࠮࠿ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨዉ")
        match = re.search(bstack1ll1lll_opy_ (u"ࡳࠩࡶࡶࡨࡃࠢࡥࡣࡷࡥ࠿࡯࡭ࡢࡩࡨ࠳ࡵࡴࡧ࠼ࡤࡤࡷࡪ࠼࠴࠭ࠪ࡞ࡢࠧࡣࠫࠪࠤࠪዊ"), bstack1ll1ll11l1l_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1ll1lll_opy_ (u"ࡴࠪࡀ࡮ࡳࡧ࡜ࡠࡁࡡ࠰ࡹࡲࡤ࠿ࠥࠬࡠࡤࠢ࡞࠭࡟࠲࠭ࡅ࠺ࡱࡰࡪࢀ࡯ࡶࡧࡽ࡬ࡳࡩ࡬࠯ࠩࠣࠩዋ"), bstack1ll1ll11l1l_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1ll1l1lll11_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡖࡔࡈࡏࡕࡡࡒ࡙࡙ࡖࡕࡕࡡࡇࡍࡗ࠭ዌ"), os.getcwd())
                    path = Path(bstack1ll1l1lll11_opy_) / path
                if path.is_file():
                    with open(path, bstack1ll1lll_opy_ (u"ࠫࡷࡨࠧው")) as f:
                        return base64.b64encode(f.read()).decode(bstack1ll1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫዎ"))
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡵࡩࡦࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡫࡯࡬ࡦࠢࡾࡴࡦࡺࡨࡾ࠼ࠣࡿࡪࢃࠢዏ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll1l111l11_opy_ = False
            self._1ll1l1ll1l1_opy_ = False
            self._current_test_name = name
            self._1ll1l11l1l1_opy_ = None
            self._1ll1ll1lll1_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1ll1lll_opy_ (u"ࠧࡪࡦࠪዐ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࠫዑ"), None)
            self._clear_session_data()
            bstack1llll111l1l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1llll111l1l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1llll111l1l_opy_)
            return
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡶࡨࡷࡹࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡶࡨࡷࡹࡀࠠࡼࡰࡤࡱࡪࢃࠢዒ").format(name=name))
        self._1ll1l111l11_opy_ = False
        self._1ll1l1ll1l1_opy_ = False
        self._current_test_name = name
        self._1ll1l11l1l1_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1llll111l1l_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1ll1l1llll1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪዓ")),
                message=attrs.get(bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬዔ"), bstack1ll1lll_opy_ (u"ࠬ࠭ዕ")),
                starttime=attrs.get(bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡹ࡯࡭ࡦࠩዖ"), bstack1ll1lll_opy_ (u"ࠧࠨ዗")),
                endtime=attrs.get(bstack1ll1lll_opy_ (u"ࠨࡧࡱࡨࡹ࡯࡭ࡦࠩዘ"), bstack1ll1lll_opy_ (u"ࠩࠪዙ")),
                elapsedtime=attrs.get(bstack1ll1lll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨዚ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1llll111l1l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1llll111l1l_opy_, bstack1ll1l1llll1_opy_)
        status = attrs.get(bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫዛ"), bstack1ll1lll_opy_ (u"࡛ࠬࡎࡌࡐࡒ࡛ࡓ࠭ዜ"))
        message = attrs.get(bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧዝ"), bstack1ll1lll_opy_ (u"ࠧࠨዞ"))
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡧࡱࡨࡤࡺࡥࡴࡶࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡺࡥࡴࡶ࠽ࠤࢀࡴࡡ࡮ࡧࢀ࠰ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡴࡶࡤࡸࡺࡹࡽࠣዟ").format(name=name, status=status))
        self._1ll1l111l11_opy_ = True
        if not self._1ll1l1ll1l1_opy_ and self._1ll1l1ll1ll_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1ll1l1ll111_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡐࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡷࡹࡧࡴࡶࡵࡀࡿࡸࡺࡡࡵࡷࡶࢁࠧዠ").format(status=status))
                    self._1ll1l111lll_opy_(status, message)
                self._1ll1l1ll1l1_opy_ = True
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡰࡥࡷࡱࡥࡥࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤዡ"))
            except Exception as e:
                logger.error(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩ࡯ࠢࡨࡲࡩࡥࡴࡦࡵࡷ࠾ࠥࢁࡥࡾࠤዢ").format(e=e))
        elif self._1ll1l1ll1l1_opy_:
            logger.debug(bstack1ll1lll_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡡ࡭ࡴࡨࡥࡩࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠢዣ"))
        else:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡎࡰࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫ࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠤዤ"))
    def start_suite(self, name, attrs):
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡥࡽࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡸࡪࡨࡲࠥࡧࠠࡴࡷ࡬ࡸࡪࠦࡳࡵࡣࡵࡸࡸࠨࠢࠣዥ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࠫዦ"), None)
            bstack1ll1l1l1ll1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1ll1l1l1ll1_opy_)
            return
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡸ࡭ࡹ࡫ࠠࡄࡃࡏࡐࡊࡊࠠ࠮ࠢࡶࡹ࡮ࡺࡥ࠻ࠢࡾࡲࡦࡳࡥࡾࠤዧ").format(name=name))
    def end_suite(self, name, attrs):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡻ࡭࡫࡮ࠡࡣࠣࡷࡺ࡯ࡴࡦࠢࡨࡲࡩࡹࠢࠣࠤየ")
        if cli.is_running():
            bstack1ll1l1l1ll1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1ll1l1l1ll1_opy_)
            return
        logger.debug(bstack1ll1lll_opy_ (u"ࠦࡪࡴࡤࡠࡵࡸ࡭ࡹ࡫ࠠࡄࡃࡏࡐࡊࡊࠠ࠮ࠢࡶࡹ࡮ࡺࡥ࠻ࠢࡾࡲࡦࡳࡥࡾࠤዩ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩዪ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨያ"), None)
            if attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬዬ"), bstack1ll1lll_opy_ (u"ࠨࠩይ")).lower() in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨዮ"), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬዯ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩደ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1ll1ll1ll11_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1lll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬዱ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1ll1ll1ll11_opy_)
            else:
                if current_test_id:
                    bstack1ll1ll1ll11_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1lll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ዲ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1ll1ll1ll11_opy_, test_id=current_test_id)
            try:
                if cli.accessibility and cli.bstack111l11ll11_opy_:
                    _1ll1l111ll1_opy_ = next(iter(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.values()), None)
                    if _1ll1l111ll1_opy_ and attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬዳ"), bstack1ll1lll_opy_ (u"ࠨࠩዴ")).lower() not in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨድ"), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬዶ")]:
                        cli.accessibility.bstack1ll1l1l11l1_opy_(
                            cli.bstack111l11ll11_opy_,
                            None,
                            (_1ll1l111ll1_opy_, bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࠫዷ")),
                            (bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE),
                            None,
                            [name, attrs],
                        )
            except Exception as _e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡰ࡫ࡹࡸࡱࡵࡨ࠿ࠦࡡ࠲࠳ࡼࠤࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧዸ").format(e=_e))
        if name.lower() in self._CLOSE_KEYWORDS:
            try:
                if cli.accessibility:
                    cli.accessibility.bstack1ll1ll11ll1_opy_()
            except Exception as _e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡱࡥࡺࡹࡲࡶࡩࡀࠠࡢ࠳࠴ࡽࠥࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࡣࡧ࡫ࡦࡰࡴࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣዹ").format(e=_e))
        if self._1ll1l1ll1l1_opy_ or self._1ll1l111l11_opy_:
            return
        bstack1ll1l11l11l_opy_ = False
        bstack1ll1l11ll11_opy_ = attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬዺ"), bstack1ll1lll_opy_ (u"ࠨࠩዻ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1ll1l11l11l_opy_ = True
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡆࡰࡴࡹࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁ࠱ࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡤࡨࡪࡴࡸࡥࠡ࡫ࡷࠤࡪࡾࡥࡤࡷࡷࡩࡸࠨዼ").format(name=name))
        elif bstack1ll1l11ll11_opy_ == bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬዽ"):
            bstack1ll1l11l11l_opy_ = True
            logger.debug(bstack1ll1lll_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧ࠭ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡹ࡫ࡡࡳࡦࡲࡻࡳࠦࡥࡹࡧࡦࡹࡹ࡫ࡳࠣዾ"))
        if bstack1ll1l11l11l_opy_ and self._1ll1l1ll1ll_opy_():
            self._populate_browser_instance_data()
            self._1ll1l11ll1l_opy_()
    def end_keyword(self, name, attrs):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡧࡦࡵࡧࡵࠤࡦࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡵ࠱ࠦࠧࠨዿ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪጀ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩጁ"), None)
            bstack1ll1ll1ll11_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨጂ"), name), id=current_test_id, **attrs)
            bstack1ll1l1llll1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩጃ")),
                message=attrs.get(bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫጄ"), bstack1ll1lll_opy_ (u"ࠫࠬጅ")),
                starttime=attrs.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡸ࡮ࡳࡥࠨጆ"), bstack1ll1lll_opy_ (u"࠭ࠧጇ")),
                endtime=attrs.get(bstack1ll1lll_opy_ (u"ࠧࡦࡰࡧࡸ࡮ࡳࡥࠨገ"), bstack1ll1lll_opy_ (u"ࠨࠩጉ")),
                elapsedtime=attrs.get(bstack1ll1lll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧጊ"), 0)
            )
            if attrs.get(bstack1ll1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨጋ"), bstack1ll1lll_opy_ (u"ࠫࠬጌ")).lower() in [bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫግ"), bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨጎ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬጏ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1ll1ll1ll11_opy_, bstack1ll1l1llll1_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1ll1ll1ll11_opy_, bstack1ll1l1llll1_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨጐ"), bstack1ll1lll_opy_ (u"ࠩࠪ጑")).upper() == bstack1ll1lll_opy_ (u"ࠪࡔࡆ࡙ࡓࠨጒ")):
                logger.debug(bstack1ll1lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࠥࡵࡰࡦࡰࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠺ࠡࡽࡱࡥࡲ࡫ࡽ࠭ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥࠧጓ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡬࡯ࡳࠢࡨࡺࡪࡸࡹࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡤࡴࡹࡻࡲࡦࡵࠣࡊࡆࡏࡌࠡ࡮ࡨࡺࡪࡲࠠ࡮ࡧࡶࡷࡦ࡭ࡥࡴࠢࡷࡳࠥࡻࡳࡦࠢࡤࡷࠥ࡫ࡲࡳࡱࡵࠤࡷ࡫ࡡࡴࡱࡱ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡳࡪࡰࡦࡩࠥࡱࡥࡺࡹࡲࡶࡩࠦࡡࡵࡶࡵࡷࠥࡪ࡯ࡦࡵࡱࠫࡹࠦࡩ࡯ࡥ࡯ࡹࡩ࡫ࠠࡵࡪࡨࠤࡪࡸࡲࡰࡴࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤጔ")
        if cli.is_running():
            try:
                if message.get(bstack1ll1lll_opy_ (u"࠭ࡨࡵ࡯࡯ࠫጕ"), bstack1ll1lll_opy_ (u"ࠧ࡯ࡱࠪ጖")) == bstack1ll1lll_opy_ (u"ࠨࡻࡨࡷࠬ጗"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪጘ"), bstack1ll1lll_opy_ (u"ࠪࠫጙ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1ll1lll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨጚ"),
                            level=bstack1ll1lll_opy_ (u"ࠬࡏࡎࡇࡑࠪጛ"),
                            timestamp=message.get(bstack1ll1lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩጜ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩጝ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩጞ"), bstack1ll1lll_opy_ (u"ࠩࠪጟ")),
                        level=message.get(bstack1ll1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩጠ"), bstack1ll1lll_opy_ (u"ࠫࡎࡔࡆࡐࠩጡ")),
                        timestamp=message.get(bstack1ll1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨጢ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨጣ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ጤ"), bstack1ll1lll_opy_ (u"ࠨࠩጥ"))
        if level == bstack1ll1lll_opy_ (u"ࠩࡉࡅࡎࡒࠧጦ"):
            self._1ll1l11l1l1_opy_ = message.get(bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫጧ"), bstack1ll1lll_opy_ (u"ࠫࠬጨ"))
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡉࡡࡱࡶࡸࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦ࡭ࡦࡵࡶࡥ࡬࡫࠺ࠡࡽࡨࡶࡷࡵࡲࡾࠤጩ").format(error=self._1ll1l11l1l1_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࡆࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡮࡬ࠠࡴࡧࡷࡹࡵ࠵ࡴࡦࡣࡵࡨࡴࡽ࡮ࠡ࡫ࡶࠤࡸࡻࡩࡵࡧ࠰ࡰࡪࡼࡥ࡭ࠢࡲࡶࠥࡺࡥࡴࡶ࠰ࡰࡪࡼࡥ࡭࠰ࠥࠦࠧጪ")
        if hook_type.lower() == bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ጫ"):
            return bstack1ll1lll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬጬ") if current_test_uuid is None else bstack1ll1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧጭ")
        elif hook_type.lower() == bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬጮ"):
            return bstack1ll1lll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧጯ") if current_test_uuid is None else bstack1ll1lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩጰ")