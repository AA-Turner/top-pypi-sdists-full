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
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.module_event_dispatcher import EventDispatcherModule
from browserstack_sdk.sdk_cli.test_framework import TestFrameworkContext, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_, AutomationFrameworkState, HookState
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack111ll11ll_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack111ll1l1l_opy_
    _11l111l11_opy_ = bstack111ll1l1l_opy_.VERSION
except:
    _11l111l11_opy_ = bstack1l1llll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨಛ")
cli_context = TestFrameworkContext(
    test_framework_name=bstack1l1llll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧಜ"),
    test_framework_version=_11l111l11_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1l1llll_opy_ (u"ࠩࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠩಝ"), bstack1l1llll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡦࡳࡳࡺࡥࡹࡶࠪಞ"), bstack1l1llll_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡴࡦ࡭ࡥࠨಟ"),
        bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷ࠭ಠ"), bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡣࡰࡰࡷࡩࡽࡺࠧಡ"), bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡱࡣࡪࡩࠬಢ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1l1llll_opy_ (u"ࠨࡰࡨࡻࠥࡨࡲࡰࡹࡶࡩࡷ࠭ಣ"), bstack1l1llll_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠣࡸࡴࠦࡢࡳࡱࡺࡷࡪࡸࠧತ"),
        bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࠡࡤࡵࡳࡼࡹࡥࡳࠩಥ"), bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡯࡯ࡰࡨࡧࡹࠦࡴࡰࠢࡥࡶࡴࡽࡳࡦࡴࠪದ"),
    }
    def __init__(self):
        self._111lll11l_opy_ = None
        self._111llll11_opy_ = False
        self._111ll11l1_opy_ = False
        self._current_test_name = None
        self._111l11ll1_opy_ = None
        self._111l11l11_opy_ = False
        if cli.bstack111l1ll11_opy_():
            try:
                if cli.automation_framework:
                    cli_context.platform_index = cli.automation_framework.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಧ"), bstack1l1llll_opy_ (u"࠭࠰ࠨನ")))
            except Exception as e:
                pass
        PlaywrightPatcher._111lll1ll_opy_()
    @staticmethod
    def _111lll1ll_opy_():
        try:
            import functools
            from Browser.keywords.bstack1lllll1l_opy_ import bstack111l1lll1_opy_
            from browserstack_sdk.sdk_cli.bstack111l1l11l_opy_ import bstack111ll111l_opy_
            _11l1111ll_opy_ = bstack111l1lll1_opy_.close_browser
            _111l1l1ll_opy_ = bstack111l1lll1_opy_.bstack111l11lll_opy_
            @functools.wraps(_11l1111ll_opy_)
            def _111l1l111_opy_(self, browser=bstack1l1llll_opy_ (u"ࠢࡄࡗࡕࡖࡊࡔࡔࠣ಩")):
                if not bstack111ll111l_opy_._111lll111_opy_.is_set():
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡤ࠵࠶ࡿࠠࡴࡥࡤࡲࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵ࠯ࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡶࡲࠤ࠶࠻ࡳࠣಪ"))
                    bstack111ll111l_opy_._111lll111_opy_.wait(timeout=15)
                return _11l1111ll_opy_(self, browser)
            @functools.wraps(_111l1l1ll_opy_)
            def _11l111111_opy_(self, page=bstack1l1llll_opy_ (u"ࠤࡆ࡙ࡗࡘࡅࡏࡖࠥಫ")):
                if not bstack111ll111l_opy_._111lll111_opy_.is_set():
                    logger.debug(bstack1l1llll_opy_ (u"ࠥࡧࡱࡵࡳࡦࡡࡳࡥ࡬࡫࠺ࠡࡣ࠴࠵ࡾࠦࡳࡤࡣࡱࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴ࠮ࠣࡻࡦ࡯ࡴࡪࡰࡪࠤࡺࡶࠠࡵࡱࠣ࠵࠺ࡹࠢಬ"))
                    bstack111ll111l_opy_._111lll111_opy_.wait(timeout=15)
                return _111l1l1ll_opy_(self, page)
            bstack111l1lll1_opy_.close_browser = _111l1l111_opy_
            bstack111l1lll1_opy_.bstack111l11lll_opy_ = _11l111111_opy_
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡤࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡥ࡯ࡳࡸ࡫࡟࡮ࡧࡷ࡬ࡴࡪࡳ࠻ࠢࡳࡥࡹࡩࡨࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡓࡵࡣࡷࡩࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧࡷࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡨࡣࡷࡩࠧಭ"))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡰࡢࡶࡦ࡬ࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡦࡰࡴࡹࡥࡠ࡯ࡨࡸ࡭ࡵࡤࡴ࠼ࠣࡷࡰ࡯ࡰࡱࡧࡧࠤ࠭ࡈࡲࡰࡹࡶࡩࡷࠦ࡬ࡪࡤࡵࡥࡷࡿࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡰࡴࠣࡥ࠶࠷ࡹࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠬ࠾ࠥࢁࡥࡾࠤಮ").format(e=e))
    def _111l1ll1l_opy_(self):
        if self._111lll11l_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._111lll11l_opy_ = BuiltIn().get_library_instance(bstack1l1llll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࠧಯ"))
            except Exception as e:
                logger.warning(bstack1l1llll_opy_ (u"ࠢࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠾ࠥࢁࡥࡾࠤರ").format(e=e))
        return self._111lll11l_opy_
    def _111l1l1l_opy_(self):
        try:
            bstack1llllll1_opy_ = self._111l1ll1l_opy_()
            if bstack1llllll1_opy_ and hasattr(bstack1llllll1_opy_, bstack1l1llll_opy_ (u"ࠨࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡥࡳࡵࡣࡷࡩࠬಱ")):
                bstack1lllll1l_opy_ = bstack1llllll1_opy_._playwright_state
                if hasattr(bstack1lllll1l_opy_, bstack1l1llll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥࡤࡸࡦࡲ࡯ࡨࠩಲ")):
                    bstack1lllll11_opy_ = bstack1lllll1l_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lllll11_opy_ = BuiltIn().run_keyword(bstack1l1llll_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡌ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࠢࡆࡥࡹࡧ࡬ࡰࡩࠪಳ"))
                for bstack111ll1ll1_opy_ in bstack1lllll11_opy_:
                    contexts = bstack111ll1ll1_opy_.get(bstack1l1llll_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸࡸ࠭಴"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1l1llll_opy_ (u"ࠬࡶࡡࡨࡧࡶࠫವ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1l1llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠼ࠣࡿࡪࢃࠢಶ").format(e=e))
            return False
    def _1l11llll_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1l11l111_opy_ = {
                bstack1l1llll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧಷ"): action,
                bstack1l1llll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಸ"): arguments
            }
            executor_cmd = bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠬಹ") + json.dumps(bstack1l11l111_opy_)
            arg_string = bstack1l1llll_opy_ (u"ࠥࡥࡷ࡭࠽ࡼࡧࡻࡩࡨࡻࡴࡰࡴࡢࡧࡲࡪࡽࠣ಺").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1l1llll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡋࡶࡢ࡮ࡸࡥࡹ࡫ࠠࡋࡣࡹࡥࡘࡩࡲࡪࡲࡷࠫ಻"),
                None,
                bstack1l1llll_opy_ (u"ࠬࡥࠠ࠾ࡀࠣࡿࢂ಼࠭"),
                arg_string
            )
            logger.debug(bstack1l1llll_opy_ (u"ࠨࡅࡹࡧࡦࡹࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡦࡩࡴࡪࡱࡱࢁ࠱ࠦࡲࡦࡵࡸࡰࡹࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤಽ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1l1llll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡦࡿࠥಾ").format(e=e))
    def _populate_browser_instance_data(self):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡔࡴࡶࡵ࡭ࡣࡷࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࠦࡡ࡯ࡦࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡰࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࠥ࡬࡯ࡳࠢࡵࡳࡧࡵࡴ࠮ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࠨࠢࠣಿ")
        try:
            from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
            if not self._111l1l1l_opy_():
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠ࡯ࡱࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦೀ"))
                return
            result = self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠪ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠧು"), {})
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠦࡲࡦࡵࡸࡰࡹࡃࡻࡳࡿࠥೂ").format(r=result))
            if not result:
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡲࡴࠦࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠣೃ"))
                return
            bstack111ll1ll_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack111ll1ll_opy_.get(bstack1l1llll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩೄ"), bstack1l1llll_opy_ (u"ࠧࠨ೅"))
            hub_url = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡑࡅࡓ࡙ࡥࡐࡘࡡࡆࡈࡕࡥࡕࡓࡎࠪೆ"), bstack1l1llll_opy_ (u"ࠩࠪೇ"))
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧ࠺ࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࢁࡳࡪࡦࢀ࠰ࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࡻࡶࡴ࡯ࢁࠧೈ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1l1llll_opy_ (u"ࠫࠬ೉")))
            current_test_id = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧೊ"), None)
            for instance in list(bstack1l111l1l_opy_.instances.values()):
                if not bstack111ll111_opy_.get_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, None):
                    bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, session_id)
                    bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, hub_url)
                    if current_test_id:
                        bstack111ll111_opy_.set_state(instance, bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧೋ"), current_test_id)
                    logger.debug(bstack1l1llll_opy_ (u"ࠢࡑࡱࡳࡹࡱࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࢀࡹࡩࡥࡿ࠯ࠤ࡭ࡻࡢࡠࡷࡵࡰࠥࡹࡥࡵ࠮ࠣࡸࡪࡹࡴࡠ࡫ࡧࡁࢀࡺࡩࡥࡿࠥೌ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.warning(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵࡰࡶ࡮ࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡧࡥࡹࡧ࠺ࠡࡽࡨࢁ್ࠧ").format(e=e))
    def _clear_session_data(self):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡈࡲࡥࡢࡴࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩࡧࡴࡢࠢࡩࡶࡴࡳࠠࡢ࡮࡯ࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠡࡶࡲࠤࡪࡴࡳࡶࡴࡨࠤࡹ࡫ࡳࡵࠢ࡬ࡷࡴࡲࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡷࡧࡷࠡࡔࡲࡦࡴࡺࠫࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࠭ࡩࡵࡴࡶࡲࡱࠥࡱࡥࡺࡹࡲࡶࡩࠦ࡬ࡪࡤࡵࡥࡷ࡯ࡥࡴࠢࡦࡥࡱࡲࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠯ࡣࡱࡨࡷࡵࡩࡥ࠰ࡦࡳࡳࡴࡥࡤࡶࠫ࠭ࠥࡧࡴࠡࡵࡸ࡭ࡹ࡫࠭ࡴࡧࡷࡹࡵࠦࡴࡪ࡯ࡨ࠭࠱ࠦࡴࡩࡧࠣࡗࡆࡓࡅࠡࡤࡵࡳࡼࡹࡥࡳࠌࠣࠤࠥࠦࠠࠡࠢࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠࡴࡪࡤࡶࡪࡪࠠࡢࡥࡵࡳࡸࡹࠠࡢ࡮࡯ࠤࡹ࡫ࡳࡵࡵ࠱ࠤ࡙࡮ࡥࡳࡧࠪࡷࠥࡴ࡯ࠡࡴࡨ࠱ࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡸ࡭ࠦࡢࡦࡥࡤࡹࡸ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡡ࡫ࡥࡸࡥࡡࡤࡶ࡬ࡺࡪࡥࡰࡢࡩࡨࠬ࠮ࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡳࠡࡶ࡫ࡩࠥࡈࡲࡰࡹࡶࡩࡷࠦ࡬ࡪࡤࡵࡥࡷࡿࠠࡤࡣࡷࡥࡱࡵࡧ࠯ࠢࡆࡰࡪࡧࡲࡪࡰࡪࠤ࡭࡫ࡲࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻࡴࡻ࡬ࡥࠢࡺ࡭ࡵ࡫ࠠࡵࡪࡨࠤࡩࡧࡴࡢࠢࡤࡲࡩࠦ࡮ࡦࡸࡨࡶࠥࡸࡥࡴࡶࡲࡶࡪࠦࡩࡵ࠰ࠣࡗࡴࠦࡷࡦࠢࡱࡳ࠲ࡵࡰࠡࡶ࡫ࡩࠥࡩ࡬ࡦࡣࡵࠤ࡮ࡴࠠࡵࡪࡤࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣࡢࡵࡨࠤ⠙ࠦ࡭ࡰࡦࡸࡰࡪࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠱ࡳࡳࡥࡣࡰࡰࡱࡩࡨࡺ࠮ࡸࡴࡤࡴࡵ࡫ࡤࠡ࠭ࠣࡳࡳࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࡢࡨ࡮ࡹࡰࡢࡶࡦ࡬࠳ࡽࡲࡢࡲࡳࡩࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࡱࡱࡳࡹࡱࡧࡴࡦࠢ࡫ࡹࡧࡥࡵࡳ࡮࠯ࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠯ࠤࡦࡴࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡣࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡩࡲࡦࡣࡷࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡪ࡯ࡨ࠰ࠥࡧ࡮ࡥࠢࡷ࡬ࡪࡿࠠࡳࡧࡰࡥ࡮ࡴࠠࡷࡣ࡯࡭ࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡦࡰࡷ࡭ࡷ࡫ࠠࡴࡷ࡬ࡸࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ೎")
        try:
            from bstack_utils.helper import is_robot_with_playwright as _111l11l1l_opy_
            from bstack_utils.helper import is_robot_playwright_installed as _111ll1111_opy_
            if _111l11l1l_opy_() and not _111ll1111_opy_():
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡨࡲࡥࡢࡴࡢࡷࡪࡹࡳࡪࡱࡱࡣࡩࡧࡴࡢ࠼ࠣࡶࡦࡽࠠࡓࡱࡥࡳࡹ࠱ࡐࡘࠢ⠗ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡣ࡭ࡧࡤࡶࠥ࠮ࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡷࡺ࡯ࡴࡦ࠯ࡶࡧࡴࡶࡥࡥࠫࠥ೏"))
                return
        except (ImportError, AttributeError) as e:
            logger.warning(bstack1l1llll_opy_ (u"ࠦࡤࡩ࡬ࡦࡣࡵࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡪࡡࡵࡣ࠽ࠤ࡮ࡹ࡟ࡳࡱࡥࡳࡹࡥࡷࡪࡶ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠠ⠕ࠢࡶࡹ࡮ࡺࡥ࠮ࡵࡦࡳࡵ࡫ࡤࠡࡵࡷࡥࡹ࡫ࠠ࡮ࡣࡼࠤࡧ࡫ࠠࡸ࡫ࡳࡩࡩࠦࡩ࡯ࡥࡲࡶࡷ࡫ࡣࡵ࡮ࡼ࠾ࠥࢁࡽࠣ೐").format(e))
        try:
            from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
            bstack111l111ll_opy_ = 0
            for instance in list(bstack1l111l1l_opy_.instances.values()):
                bstack111ll1lll_opy_ = False
                if bstack111ll111_opy_.get_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, None):
                    bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, bstack1l1llll_opy_ (u"ࠬ࠭೑"))
                    bstack111ll1lll_opy_ = True
                if bstack111ll111_opy_.get_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, None):
                    bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, bstack1l1llll_opy_ (u"࠭ࠧ೒"))
                    bstack111ll1lll_opy_ = True
                if bstack111ll111_opy_.get_state(instance, bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨ೓"), None):
                    bstack111ll111_opy_.set_state(instance, bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡩࡥࠩ೔"), None)
                    bstack111ll1lll_opy_ = True
                if bstack1l111l1l_opy_.has_state(instance, bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡲ࡮ࡺࠧೕ")):
                    bstack1l111l1l_opy_.set_state(instance, bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠨೖ"), None)
                    bstack111ll1lll_opy_ = True
                if bstack111ll1lll_opy_:
                    bstack111l111ll_opy_ += 1
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡤࡩ࡬ࡦࡣࡵࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡪࡡࡵࡣ࠽ࠤࡈࡲࡥࡢࡴࡨࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮ࠢࡾࡲࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠤ೗").format(
                n=bstack111l111ll_opy_))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡯ࡩࡦࡸࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡤࡸࡦࡀࠠࡼࡧࢀࠦ೘").format(e=e))
    def _1l11l1l1_opy_(self, status, reason=bstack1l1llll_opy_ (u"ࠨࠢ೙")):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡐࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥࠦࠧ೚")
        bstack1l111ll1_opy_ = bstack1l1llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ೛") if status == bstack1l1llll_opy_ (u"ࠤࡓࡅࡘ࡙ࠢ೜") else bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥೝ")
        if bstack1l111ll1_opy_ == bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦೞ"):
            return self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ೟"), {
                bstack1l1llll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨೠ"): bstack1l111ll1_opy_,
                bstack1l1llll_opy_ (u"ࠢࡳࡧࡤࡷࡴࡴࠢೡ"): reason
            })
        else:
            return self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦೢ"), {
                bstack1l1llll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤೣ"): bstack1l111ll1_opy_
            })
    def _111llllll_opy_(self, name):
        bstack1l1llll_opy_ (u"࡙ࠥࠦࠧࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥࠦࠧ೤")
        return self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ೥"), {
            bstack1l1llll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ೦"): name
        })
    def _11l111l1l_opy_(self):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡤࡨࡪࡴࡸࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡦࡰࡴࡹࡥࠡࡱࡵࠤࡹ࡫ࡡࡳࡦࡲࡻࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡷࡥࡹࡻࡳࠡ࡫ࡶࠤ࡮ࡴࡦࡦࡴࡵࡩࡩࠦࡦࡳࡱࡰࠤࡤࡲࡡࡴࡶࡢࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧ࠽ࠤ࡮࡬ࠠࡢࡰࡼࠤࡋࡇࡉࡍ࠯࡯ࡩࡻ࡫࡬ࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡣࡶࠤࡨࡧࡰࡵࡷࡵࡩࡩࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡸࡪࡹࡴ࠭ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡮ࡹࠠࡧࡣ࡬ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ೧")
        if self._111ll11l1_opy_:
            return
        try:
            global_config = Config.bstack1lll1l11_opy_()
            if self._current_test_name and not global_config.bstack11lll1l1_opy_():
                self._111llllll_opy_(self._current_test_name)
            status = bstack1l1llll_opy_ (u"ࠧࡇࡃࡌࡐࠬ೨") if self._111l11ll1_opy_ else bstack1l1llll_opy_ (u"ࠨࡒࡄࡗࡘ࠭೩")
            message = self._111l11ll1_opy_ or bstack1l1llll_opy_ (u"ࠩࠪ೪")
            if not global_config.bstack11l11l1l_opy_():
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡑࡦࡸ࡫ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡨࡥࡧࡱࡵࡩࠥࡩ࡬ࡰࡵࡨ࠾ࠥࡹࡴࡢࡶࡸࡷࡂࢁࡳࡵࡣࡷࡹࡸࢃࠬࠡ࡯ࡨࡷࡸࡧࡧࡦ࠿ࡾࡱࡪࡹࡳࡢࡩࡨࢁࠧ೫").format(status=status, message=message))
                self._1l11l1l1_opy_(status, message)
            self._111ll11l1_opy_ = True
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡱࡦࡸ࡫ࡦࡦࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥ೬"))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࡨࢁࠧ೭").format(e=e))
    def _extract_screenshot_base64(self, bstack11l11111l_opy_):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡍ࡚ࡍࡍࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡳࡧࡵࡴࠨࡵࠣࡆࡷࡵࡷࡴࡧࡵࠤࡱ࡯ࡢࡳࡣࡵࡽࠥࡲ࡯ࡨࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠡࡣࡶࠤࡍ࡚ࡍࡍࠢࡺ࡭ࡹ࡮ࠠࡦ࡫ࡷ࡬ࡪࡸ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡊࡳࡢࡦࡦࡧࡩࡩࡀࠠ࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࡨࡦࡺࡡ࠻࡫ࡰࡥ࡬࡫࠯ࡱࡰࡪ࠿ࡧࡧࡳࡦ࠸࠷࠰ࢀࡪࡡࡵࡣࢀࠦࠥ࠴࠮࠯ࡀࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡪ࡮ࡨࠤࡱ࡯࡮࡬࠼ࠣࡀ࡮ࡳࡧࠡࡵࡵࡧࡂࠨࡰࡢࡶ࡫࠳ࡹࡵ࠯ࡧ࡫࡯ࡩ࠳ࡶ࡮ࡨࠤࠣ࠲࠳࠴࠾ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ೮")
        match = re.search(bstack1l1llll_opy_ (u"ࡲࠨࡵࡵࡧࡂࠨࡤࡢࡶࡤ࠾࡮ࡳࡡࡨࡧ࠲ࡴࡳ࡭࠻ࡣࡣࡶࡩ࠻࠺ࠬࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩ೯"), bstack11l11111l_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1l1llll_opy_ (u"ࡳࠩ࠿࡭ࡲ࡭࡛࡟ࡀࡠ࠯ࡸࡸࡣ࠾ࠤࠫ࡟ࡣࠨ࡝ࠬ࡞࠱ࠬࡄࡀࡰ࡯ࡩࡿ࡮ࡵ࡭ࡼ࡫ࡲࡨ࡫࠮࠯ࠢࠨ೰"), bstack11l11111l_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack111lll1l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡕࡓࡇࡕࡔࡠࡑࡘࡘࡕ࡛ࡔࡠࡆࡌࡖࠬೱ"), os.getcwd())
                    path = Path(bstack111lll1l1_opy_) / path
                if path.is_file():
                    with open(path, bstack1l1llll_opy_ (u"ࠪࡶࡧ࠭ೲ")) as f:
                        return base64.b64encode(f.read()).decode(bstack1l1llll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪೳ"))
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡴࡨࡥࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡪ࡮ࡲࡥࠡࡽࡳࡥࡹ࡮ࡽ࠻ࠢࡾࡩࢂࠨ೴").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._111llll11_opy_ = False
            self._111ll11l1_opy_ = False
            self._current_test_name = name
            self._111l11ll1_opy_ = None
            self._111l11l11_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1l1llll_opy_ (u"࠭ࡩࡥࠩ೵"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1l1llll_opy_ (u"ࠧࡪࡦࠪ೶"), None)
            self._clear_session_data()
            bstack1lllll11l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lllll11l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lllll11l_opy_)
            return
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡵࡧࡶࡸࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡵࡧࡶࡸ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨ೷").format(name=name))
        self._111llll11_opy_ = False
        self._111ll11l1_opy_ = False
        self._current_test_name = name
        self._111l11ll1_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lllll11l_opy_ = SimpleNamespace(name=name, **attrs)
            bstack111l1l1l1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ೸")),
                message=attrs.get(bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ೹"), bstack1l1llll_opy_ (u"ࠫࠬ೺")),
                starttime=attrs.get(bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡸ࡮ࡳࡥࠨ೻"), bstack1l1llll_opy_ (u"࠭ࠧ೼")),
                endtime=attrs.get(bstack1l1llll_opy_ (u"ࠧࡦࡰࡧࡸ࡮ࡳࡥࠨ೽"), bstack1l1llll_opy_ (u"ࠨࠩ೾")),
                elapsedtime=attrs.get(bstack1l1llll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧ೿"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lllll11l_opy_, bstack111l1l1l1_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lllll11l_opy_)
        status = attrs.get(bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪഀ"), bstack1l1llll_opy_ (u"࡚ࠫࡔࡋࡏࡑ࡚ࡒࠬഁ"))
        message = attrs.get(bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ം"), bstack1l1llll_opy_ (u"࠭ࠧഃ"))
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡦࡰࡧࡣࡹ࡫ࡳࡵࠢࡆࡅࡑࡒࡅࡅࠢ࠰ࠤࡹ࡫ࡳࡵ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡳࡵࡣࡷࡹࡸࢃࠢഄ").format(name=name, status=status))
        self._111llll11_opy_ = True
        if not self._111ll11l1_opy_ and self._111l1l1l_opy_():
            try:
                global_config = Config.bstack1lll1l11_opy_()
                if not global_config.bstack11lll1l1_opy_():
                    self._111llllll_opy_(name)
                if not global_config.bstack11l11l1l_opy_():
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡏࡤࡶࡰ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡳࠦࡥ࡯ࡦࡢࡸࡪࡹࡴ࠻ࠢࡶࡸࡦࡺࡵࡴ࠿ࡾࡷࡹࡧࡴࡶࡵࢀࠦഅ").format(status=status))
                    self._1l11l1l1_opy_(status, message)
                self._111ll11l1_opy_ = True
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣആ"))
            except Exception as e:
                logger.error(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯࡮ࠡࡧࡱࡨࡤࡺࡥࡴࡶ࠽ࠤࢀ࡫ࡽࠣഇ").format(e=e))
        elif self._111ll11l1_opy_:
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡧ࡬ࡳࡧࡤࡨࡾࠦ࡭ࡢࡴ࡮ࡩࡩࠨഈ"))
        else:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠣഉ"))
    def start_suite(self, name, attrs):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡷࡩࡧࡱࠤࡦࠦࡳࡶ࡫ࡷࡩࠥࡹࡴࡢࡴࡷࡷࠧࠨࠢഊ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1l1llll_opy_ (u"ࠧࡪࡦࠪഋ"), None)
            bstack111l111l1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack111l111l1_opy_)
            return
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡷ࡬ࡸࡪࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡵࡸ࡭ࡹ࡫࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣഌ").format(name=name))
    def end_suite(self, name, attrs):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡺ࡬ࡪࡴࠠࡢࠢࡶࡹ࡮ࡺࡥࠡࡧࡱࡨࡸࠨࠢࠣ഍")
        if cli.is_running():
            bstack111l111l1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack111l111l1_opy_)
            return
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡩࡳࡪ࡟ࡴࡷ࡬ࡸࡪࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡵࡸ࡭ࡹ࡫࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣഎ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨഏ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧഐ"), None)
            if attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫ഑"), bstack1l1llll_opy_ (u"ࠧࠨഒ")).lower() in [bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧഓ"), bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫഔ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1l1llll_opy_ (u"ࠪࡸࡾࡶࡥࠨക")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack111l1llll_opy_ = SimpleNamespace(name=attrs.get(bstack1l1llll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫഖ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack111l1llll_opy_)
            else:
                if current_test_id:
                    bstack111l1llll_opy_ = SimpleNamespace(name=attrs.get(bstack1l1llll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬഗ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack111l1llll_opy_, test_id=current_test_id)
            try:
                if cli.accessibility and cli.automation_framework:
                    _instance = next(iter(bstack1l111l1l_opy_.instances.values()), None)
                    if _instance and attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫഘ"), bstack1l1llll_opy_ (u"ࠧࠨങ")).lower() not in [bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧച"), bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫഛ")]:
                        cli.accessibility.bstack111lllll1_opy_(
                            cli.automation_framework,
                            None,
                            (_instance, bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࠪജ")),
                            (AutomationFrameworkState.EXECUTE, HookState.PRE),
                            None,
                            [name, attrs],
                        )
            except Exception as _e:
                logger.debug(bstack1l1llll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢ࡯ࡪࡿࡷࡰࡴࡧ࠾ࠥࡧ࠱࠲ࡻࠣࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦഝ").format(e=_e))
        if name.lower() in self._CLOSE_KEYWORDS:
            try:
                if cli.accessibility:
                    cli.accessibility.stop_capture_before_browser_close()
            except Exception as _e:
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡰ࡫ࡹࡸࡱࡵࡨ࠿ࠦࡡ࠲࠳ࡼࠤࡸࡺ࡯ࡱࡡࡦࡥࡵࡺࡵࡳࡧࡢࡦࡪ࡬࡯ࡳࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢഞ").format(e=_e))
        if self._111ll11l1_opy_ or self._111llll11_opy_:
            return
        bstack111llll1l_opy_ = False
        bstack11l1111l1_opy_ = attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫട"), bstack1l1llll_opy_ (u"ࠧࠨഠ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack111llll1l_opy_ = True
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡅ࡯ࡳࡸ࡫ࠠ࡬ࡧࡼࡻࡴࡸࡤࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࢀࡴࡡ࡮ࡧࢀ࠰ࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡪࡶࠣࡩࡽ࡫ࡣࡶࡶࡨࡷࠧഡ").format(name=name))
        elif bstack11l1111l1_opy_ == bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫഢ"):
            bstack111llll1l_opy_ = True
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠬࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡸࡪࡧࡲࡥࡱࡺࡲࠥ࡫ࡸࡦࡥࡸࡸࡪࡹࠢണ"))
        if bstack111llll1l_opy_ and self._111l1l1l_opy_():
            self._populate_browser_instance_data()
            self._11l111l1l_opy_()
    def end_keyword(self, name, attrs):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡦ࡬ࡴࡦࡴࠣࡥࠥࡱࡥࡺࡹࡲࡶࡩࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡴ࠰ࠥࠦࠧത")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩഥ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨദ"), None)
            bstack111l1llll_opy_ = SimpleNamespace(name=attrs.get(bstack1l1llll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧധ"), name), id=current_test_id, **attrs)
            bstack111l1l1l1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨന")),
                message=attrs.get(bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪഩ"), bstack1l1llll_opy_ (u"ࠪࠫപ")),
                starttime=attrs.get(bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠧഫ"), bstack1l1llll_opy_ (u"ࠬ࠭ബ")),
                endtime=attrs.get(bstack1l1llll_opy_ (u"࠭ࡥ࡯ࡦࡷ࡭ࡲ࡫ࠧഭ"), bstack1l1llll_opy_ (u"ࠧࠨമ")),
                elapsedtime=attrs.get(bstack1l1llll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭യ"), 0)
            )
            if attrs.get(bstack1l1llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧര"), bstack1l1llll_opy_ (u"ࠪࠫറ")).lower() in [bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪല"), bstack1l1llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧള")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫഴ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack111l1llll_opy_, bstack111l1l1l1_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack111l1llll_opy_, bstack111l1l1l1_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧവ"), bstack1l1llll_opy_ (u"ࠨࠩശ")).upper() == bstack1l1llll_opy_ (u"ࠩࡓࡅࡘ࡙ࠧഷ")):
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࠤࡴࡶࡥ࡯ࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࡀࠠࡼࡰࡤࡱࡪࢃࠬࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡢࡶࡤࠦസ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡷࡿࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡳࡸࡺࡸࡥࡴࠢࡉࡅࡎࡒࠠ࡭ࡧࡹࡩࡱࠦ࡭ࡦࡵࡶࡥ࡬࡫ࡳࠡࡶࡲࠤࡺࡹࡥࠡࡣࡶࠤࡪࡸࡲࡰࡴࠣࡶࡪࡧࡳࡰࡰ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡩ࡯ࡥࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡧࡴࡵࡴࡶࠤࡩࡵࡥࡴࡰࠪࡸࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡴࡩࡧࠣࡩࡷࡸ࡯ࡳࠢࡰࡩࡸࡹࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣഹ")
        if cli.is_running():
            try:
                if message.get(bstack1l1llll_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪഺ"), bstack1l1llll_opy_ (u"࠭࡮ࡰ഻ࠩ")) == bstack1l1llll_opy_ (u"ࠧࡺࡧࡶ഼ࠫ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩഽ"), bstack1l1llll_opy_ (u"ࠩࠪാ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1l1llll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧി"),
                            level=bstack1l1llll_opy_ (u"ࠫࡎࡔࡆࡐࠩീ"),
                            timestamp=message.get(bstack1l1llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨു"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨൂ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨൃ"), bstack1l1llll_opy_ (u"ࠨࠩൄ")),
                        level=message.get(bstack1l1llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ൅"), bstack1l1llll_opy_ (u"ࠪࡍࡓࡌࡏࠨെ")),
                        timestamp=message.get(bstack1l1llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧേ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧൈ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡰࡴ࡭࠭ࡦࡸࡨࡲࡹࠦࡴࡳࡣࡦ࡯࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁ࠿ࠦࡻࡾࠤ൉").format(type(e).__name__, e), exc_info=True)
        level = message.get(bstack1l1llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ൊ"), bstack1l1llll_opy_ (u"ࠨࠩോ"))
        if level == bstack1l1llll_opy_ (u"ࠩࡉࡅࡎࡒࠧൌ"):
            self._111l11ll1_opy_ = message.get(bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ്ࠫ"), bstack1l1llll_opy_ (u"ࠫࠬൎ"))
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡉࡡࡱࡶࡸࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦ࡭ࡦࡵࡶࡥ࡬࡫࠺ࠡࡽࡨࡶࡷࡵࡲࡾࠤ൏").format(error=self._111l11ll1_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡆࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡮࡬ࠠࡴࡧࡷࡹࡵ࠵ࡴࡦࡣࡵࡨࡴࡽ࡮ࠡ࡫ࡶࠤࡸࡻࡩࡵࡧ࠰ࡰࡪࡼࡥ࡭ࠢࡲࡶࠥࡺࡥࡴࡶ࠰ࡰࡪࡼࡥ࡭࠰ࠥࠦࠧ൐")
        if hook_type.lower() == bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭൑"):
            return bstack1l1llll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ൒") if current_test_uuid is None else bstack1l1llll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ൓")
        elif hook_type.lower() == bstack1l1llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬൔ"):
            return bstack1l1llll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧൕ") if current_test_uuid is None else bstack1l1llll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩൖ")