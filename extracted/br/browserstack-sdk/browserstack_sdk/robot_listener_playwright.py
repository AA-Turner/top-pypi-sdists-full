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
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111ll1l11_opy_ import bstack1l111l11_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1lllll1l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import bstack11l1l1l1_opy_, bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_
from browserstack_sdk.sdk_cli.bstack11ll1l11_opy_ import bstack11ll1l11_opy_, Events, bstack1ll11l1l11_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1l1llll1ll1_opy_
    _1ll1111lll1_opy_ = bstack1l1llll1ll1_opy_.VERSION
except:
    _1ll1111lll1_opy_ = bstack111ll_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᏆ")
cli_context = bstack1ll1lllll1l_opy_(
    test_framework_name=bstack111ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᏇ"),
    test_framework_version=_1ll1111lll1_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack111ll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴࠪᏈ"), bstack111ll_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡧࡴࡴࡴࡦࡺࡷࠫᏉ"), bstack111ll_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡵࡧࡧࡦࠩᏊ"),
        bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠧᏋ"), bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡱࡸࡪࡾࡴࠨᏌ"), bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡲࡤ࡫ࡪ࠭Ꮝ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack111ll_opy_ (u"ࠩࡱࡩࡼࠦࡢࡳࡱࡺࡷࡪࡸࠧᏎ"), bstack111ll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠤࡹࡵࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᏏ"),
        bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࠢࡥࡶࡴࡽࡳࡦࡴࠪᏐ"), bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣࡰࡰࡱࡩࡨࡺࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࠫᏑ"),
    }
    def __init__(self):
        self._1ll11111l11_opy_ = None
        self._1ll11111lll_opy_ = False
        self._1l1lll1l111_opy_ = False
        self._current_test_name = None
        self._1ll111111l1_opy_ = None
        self._1l1lllll111_opy_ = False
        if cli.bstack11lll11ll1_opy_():
            try:
                if cli.bstack11l111l1l_opy_:
                    cli_context.platform_index = cli.bstack11l111l1l_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮢ"), bstack111ll_opy_ (u"ࠧ࠱ࠩᏓ")))
            except Exception as e:
                pass
        PlaywrightPatcher._1l1lll11ll1_opy_()
    @staticmethod
    def _1l1lll11ll1_opy_():
        try:
            import functools
            from Browser.keywords.bstack1llll1lllll_opy_ import bstack1l1llll1l1l_opy_
            from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll111111ll_opy_
            _1l1lll1llll_opy_ = bstack1l1llll1l1l_opy_.close_browser
            _1l1lll1ll1l_opy_ = bstack1l1llll1l1l_opy_.bstack1l1lll1ll11_opy_
            @functools.wraps(_1l1lll1llll_opy_)
            def _1ll1111ll1l_opy_(self, browser=bstack111ll_opy_ (u"ࠣࡅࡘࡖࡗࡋࡎࡕࠤᏔ")):
                if not bstack1ll111111ll_opy_._1l1lllll1ll_opy_.is_set():
                    logger.debug(bstack111ll_opy_ (u"ࠤࡦࡰࡴࡹࡥࡠࡤࡵࡳࡼࡹࡥࡳ࠼ࠣࡥ࠶࠷ࡹࠡࡵࡦࡥࡳࠦࡩ࡯ࠢࡳࡶࡴ࡭ࡲࡦࡵࡶ࠰ࠥࡽࡡࡪࡶ࡬ࡲ࡬ࠦࡵࡱࠢࡷࡳࠥ࠷࠵ࡴࠤᏕ"))
                    bstack1ll111111ll_opy_._1l1lllll1ll_opy_.wait(timeout=15)
                return _1l1lll1llll_opy_(self, browser)
            @functools.wraps(_1l1lll1ll1l_opy_)
            def _1ll11111l1l_opy_(self, page=bstack111ll_opy_ (u"ࠥࡇ࡚ࡘࡒࡆࡐࡗࠦᏖ")):
                if not bstack1ll111111ll_opy_._1l1lllll1ll_opy_.is_set():
                    logger.debug(bstack111ll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡤ࠵࠶ࡿࠠࡴࡥࡤࡲࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵ࠯ࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡶࡲࠤ࠶࠻ࡳࠣᏗ"))
                    bstack1ll111111ll_opy_._1l1lllll1ll_opy_.wait(timeout=15)
                return _1l1lll1ll1l_opy_(self, page)
            bstack1l1llll1l1l_opy_.close_browser = _1ll1111ll1l_opy_
            bstack1l1llll1l1l_opy_.bstack1l1lll1ll11_opy_ = _1ll11111l1l_opy_
            logger.debug(bstack111ll_opy_ (u"ࠧࡥࡰࡢࡶࡦ࡬ࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡦࡰࡴࡹࡥࡠ࡯ࡨࡸ࡭ࡵࡤࡴ࠼ࠣࡴࡦࡺࡣࡩࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡔࡶࡤࡸࡪࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨࡸࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡩࡤࡸࡪࠨᏘ"))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠨ࡟ࡱࡣࡷࡧ࡭ࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡢࡧࡱࡵࡳࡦࡡࡰࡩࡹ࡮࡯ࡥࡵ࠽ࠤࡸࡱࡩࡱࡲࡨࡨࠥ࠮ࡂࡳࡱࡺࡷࡪࡸࠠ࡭࡫ࡥࡶࡦࡸࡹࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡱࡵࠤࡦ࠷࠱ࡺࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠭࠿ࠦࡻࡦࡿࠥᏙ").format(e=e))
    def _1l1llll1l11_opy_(self):
        if self._1ll11111l11_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1ll11111l11_opy_ = BuiltIn().get_library_instance(bstack111ll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࠨᏚ"))
            except Exception as e:
                logger.warning(bstack111ll_opy_ (u"ࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤ࡬࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠿ࠦࡻࡦࡿࠥᏛ").format(e=e))
        return self._1ll11111l11_opy_
    def _1ll11111ll1_opy_(self):
        try:
            bstack1lllll111l1_opy_ = self._1l1llll1l11_opy_()
            if bstack1lllll111l1_opy_ and hasattr(bstack1lllll111l1_opy_, bstack111ll_opy_ (u"ࠩࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࡟ࡴࡶࡤࡸࡪ࠭Ꮬ")):
                bstack1llll1lllll_opy_ = bstack1lllll111l1_opy_._playwright_state
                if hasattr(bstack1llll1lllll_opy_, bstack111ll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡥࡹࡧ࡬ࡰࡩࠪᏝ")):
                    bstack1lllll11111_opy_ = bstack1llll1lllll_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lllll11111_opy_ = BuiltIn().run_keyword(bstack111ll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡍࡥࡵࠢࡅࡶࡴࡽࡳࡦࡴࠣࡇࡦࡺࡡ࡭ࡱࡪࠫᏞ"))
                for bstack1l1lll1lll1_opy_ in bstack1lllll11111_opy_:
                    contexts = bstack1l1lll1lll1_opy_.get(bstack111ll_opy_ (u"ࠬࡩ࡯࡯ࡶࡨࡼࡹࡹࠧᏟ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack111ll_opy_ (u"࠭ࡰࡢࡩࡨࡷࠬᏠ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack111ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧ࠽ࠤࢀ࡫ࡽࠣᏡ").format(e=e))
            return False
    def _1l1llll111l_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1ll1111111l_opy_ = {
                bstack111ll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᏢ"): action,
                bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᏣ"): arguments
            }
            executor_cmd = bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥ࠭Ꮴ") + json.dumps(bstack1ll1111111l_opy_)
            arg_string = bstack111ll_opy_ (u"ࠦࡦࡸࡧ࠾ࡽࡨࡼࡪࡩࡵࡵࡱࡵࡣࡨࡳࡤࡾࠤᏥ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack111ll_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠴ࡅࡷࡣ࡯ࡹࡦࡺࡥࠡࡌࡤࡺࡦ࡙ࡣࡳ࡫ࡳࡸࠬᏦ"),
                None,
                bstack111ll_opy_ (u"࠭࡟ࠡ࠿ࡁࠤࢀࢃࠧᏧ"),
                arg_string
            )
            logger.debug(bstack111ll_opy_ (u"ࠢࡆࡺࡨࡧࡺࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡧࡣࡵ࡫ࡲࡲࢂ࠲ࠠࡳࡧࡶࡹࡱࡺ࠺ࠡࡽࡵࡩࡸࡻ࡬ࡵࡿࠥᏨ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡪࡾࡥࡤࡷࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡧࢀࠦᏩ").format(e=e))
    def _populate_browser_instance_data(self):
        bstack111ll_opy_ (u"ࠤࠥࠦࡕࡵࡰࡶ࡮ࡤࡸࡪࠦࡨࡶࡤࡢࡹࡷࡲࠠࡢࡰࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡱࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࠦࡦࡰࡴࠣࡶࡴࡨ࡯ࡵ࠯ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࠢࠣࠤᏪ")
        try:
            from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
            if not self._1ll11111ll1_opy_():
                logger.debug(bstack111ll_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧ࠺ࠡࡰࡲࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᏫ"))
                return
            result = self._1l1llll111l_opy_(bstack111ll_opy_ (u"ࠫ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠨᏬ"), {})
            logger.debug(bstack111ll_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠠࡳࡧࡶࡹࡱࡺ࠽ࡼࡴࢀࠦᏭ").format(r=result))
            if not result:
                logger.debug(bstack111ll_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡳࡵࠠࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤᏮ"))
                return
            bstack1l1lll11l11_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1l1lll11l11_opy_.get(bstack111ll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᏯ"), bstack111ll_opy_ (u"ࠨࠩᏰ"))
            hub_url = os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡒࡆࡔ࡚࡟ࡑ࡙ࡢࡇࡉࡖ࡟ࡖࡔࡏࠫᏱ"), bstack111ll_opy_ (u"ࠪࠫᏲ"))
            logger.debug(bstack111ll_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࡻࡴ࡫ࡧࢁ࠱ࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࡼࡷࡵࡰࢂࠨᏳ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack111ll_opy_ (u"ࠬ࠭Ᏼ")))
            current_test_id = getattr(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨᏵ"), None)
            for instance in bstack11l1l1l1_opy_.bstack111l11l1l1_opy_.values():
                if not bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1111ll11_opy_, None):
                    bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1111ll11_opy_, session_id)
                    bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_, hub_url)
                    if current_test_id:
                        bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨ᏶"), current_test_id)
                    logger.debug(bstack111ll_opy_ (u"ࠣࡒࡲࡴࡺࡲࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠺ࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࢁࡳࡪࡦࢀ࠰ࠥ࡮ࡵࡣࡡࡸࡶࡱࠦࡳࡦࡶ࠯ࠤࡹ࡫ࡳࡵࡡ࡬ࡨࡂࢁࡴࡪࡦࢀࠦ᏷").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡨࡦࡺࡡ࠻ࠢࡾࡩࢂࠨᏸ").format(e=e))
    def _clear_session_data(self):
        bstack111ll_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡣ࡯ࡰࠥࡨࡲࡰࡹࡶࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠢࡷࡳࠥ࡫࡮ࡴࡷࡵࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࡵ࡬ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᏹ")
        try:
            from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
            bstack1l1lllllll1_opy_ = 0
            for instance in bstack11l1l1l1_opy_.bstack111l11l1l1_opy_.values():
                bstack1l1lll1l1ll_opy_ = False
                if bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1111ll11_opy_, None):
                    bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1111ll11_opy_, bstack111ll_opy_ (u"ࠫࠬᏺ"))
                    bstack1l1lll1l1ll_opy_ = True
                if bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_, None):
                    bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll1llll1_opy_, bstack111ll_opy_ (u"ࠬ࠭ᏻ"))
                    bstack1l1lll1l1ll_opy_ = True
                if bstack11ll1l1ll_opy_.bstack1l1llll1111_opy_(instance, bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧᏼ"), None):
                    bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨᏽ"), None)
                    bstack1l1lll1l1ll_opy_ = True
                if bstack11l1l1l1_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹ࠭᏾")):
                    bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡲ࡮ࡺࠧ᏿"), None)
                    bstack1l1lll1l1ll_opy_ = True
                if bstack1l1lll1l1ll_opy_:
                    bstack1l1lllllll1_opy_ += 1
            logger.debug(bstack111ll_opy_ (u"ࠥࡣࡨࡲࡥࡢࡴࡢࡷࡪࡹࡳࡪࡱࡱࡣࡩࡧࡴࡢ࠼ࠣࡇࡱ࡫ࡡࡳࡧࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡽࡱࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠣ᐀").format(
                n=bstack1l1lllllll1_opy_))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡦࡿࠥᐁ").format(e=e))
    def _1l1llll11ll_opy_(self, status, reason=bstack111ll_opy_ (u"ࠧࠨᐂ")):
        bstack111ll_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦᐃ")
        bstack1l1lll1l11l_opy_ = bstack111ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᐄ") if status == bstack111ll_opy_ (u"ࠣࡒࡄࡗࡘࠨᐅ") else bstack111ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᐆ")
        if bstack1l1lll1l11l_opy_ == bstack111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᐇ"):
            return self._1l1llll111l_opy_(bstack111ll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᐈ"), {
                bstack111ll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᐉ"): bstack1l1lll1l11l_opy_,
                bstack111ll_opy_ (u"ࠨࡲࡦࡣࡶࡳࡳࠨᐊ"): reason
            })
        else:
            return self._1l1llll111l_opy_(bstack111ll_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᐋ"), {
                bstack111ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᐌ"): bstack1l1lll1l11l_opy_
            })
    def _1ll1111l11l_opy_(self, name):
        bstack111ll_opy_ (u"ࠤࠥࠦࡘ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦᐍ")
        return self._1l1llll111l_opy_(bstack111ll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᐎ"), {
            bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐏ"): name
        })
    def _1l1llll1lll_opy_(self):
        bstack111ll_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡣࡧࡩࡳࡷ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡥ࡯ࡳࡸ࡫ࠠࡰࡴࠣࡸࡪࡧࡲࡥࡱࡺࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡶࡤࡸࡺࡹࠠࡪࡵࠣ࡭ࡳ࡬ࡥࡳࡴࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡣࡱࡧࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦ࠼ࠣ࡭࡫ࠦࡡ࡯ࡻࠣࡊࡆࡏࡌ࠮࡮ࡨࡺࡪࡲࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡢࡵࠣࡧࡦࡶࡴࡶࡴࡨࡨࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡷࡩࡸࡺࠬࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࠦࡦࡢ࡫࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᐐ")
        if self._1l1lll1l111_opy_:
            return
        try:
            global_config = Config.bstack1l1l11ll1_opy_()
            if self._current_test_name and not global_config.bstack1ll1lll11ll_opy_():
                self._1ll1111l11l_opy_(self._current_test_name)
            status = bstack111ll_opy_ (u"࠭ࡆࡂࡋࡏࠫᐑ") if self._1ll111111l1_opy_ else bstack111ll_opy_ (u"ࠧࡑࡃࡖࡗࠬᐒ")
            message = self._1ll111111l1_opy_ or bstack111ll_opy_ (u"ࠨࠩᐓ")
            if not global_config.bstack1ll1ll1lll1_opy_():
                logger.debug(bstack111ll_opy_ (u"ࠤࡐࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡨࡲ࡯ࡴࡧ࠽ࠤࡸࡺࡡࡵࡷࡶࡁࢀࡹࡴࡢࡶࡸࡷࢂ࠲ࠠ࡮ࡧࡶࡷࡦ࡭ࡥ࠾ࡽࡰࡩࡸࡹࡡࡨࡧࢀࠦᐔ").format(status=status, message=message))
                self._1l1llll11ll_opy_(status, message)
            self._1l1lll1l111_opy_ = True
            logger.debug(bstack111ll_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡰࡥࡷࡱࡥࡥࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᐕ"))
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡧࢀࠦᐖ").format(e=e))
    def _extract_screenshot_base64(self, bstack1l1lll11l1l_opy_):
        bstack111ll_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡌ࡙ࡓࡌࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡲࡦࡴࡺࠧࡴࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡱࡵࡧࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠠࡢࡵࠣࡌ࡙ࡓࡌࠡࡹ࡬ࡸ࡭ࠦࡥࡪࡶ࡫ࡩࡷࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡨࡥࡥࡦࡨࡨ࠿ࠦ࠼ࡪ࡯ࡪࠤࡸࡸࡣ࠾ࠤࡧࡥࡹࡧ࠺ࡪ࡯ࡤ࡫ࡪ࠵ࡰ࡯ࡩ࠾ࡦࡦࡹࡥ࠷࠶࠯ࡿࡩࡧࡴࡢࡿࠥࠤ࠳࠴࠮࠿ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌࡩ࡭ࡧࠣࡰ࡮ࡴ࡫࠻ࠢ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧࡶࡡࡵࡪ࠲ࡸࡴ࠵ࡦࡪ࡮ࡨ࠲ࡵࡴࡧࠣࠢ࠱࠲࠳ࡄࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᐗ")
        match = re.search(bstack111ll_opy_ (u"ࡸࠧࡴࡴࡦࡁࠧࡪࡡࡵࡣ࠽࡭ࡲࡧࡧࡦ࠱ࡳࡲ࡬ࡁࡢࡢࡵࡨ࠺࠹࠲ࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨᐘ"), bstack1l1lll11l1l_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack111ll_opy_ (u"ࡲࠨ࠾࡬ࡱ࡬ࡡ࡞࠿࡟࠮ࡷࡷࡩ࠽ࠣࠪ࡞ࡢࠧࡣࠫ࡝࠰ࠫࡃ࠿ࡶ࡮ࡨࡾ࡭ࡴ࡬ࢂࡪࡱࡧࡪ࠭࠮ࠨࠧᐙ"), bstack1l1lll11l1l_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1l1llllll11_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠨࡔࡒࡆࡔ࡚࡟ࡐࡗࡗࡔ࡚࡚࡟ࡅࡋࡕࠫᐚ"), os.getcwd())
                    path = Path(bstack1l1llllll11_opy_) / path
                if path.is_file():
                    with open(path, bstack111ll_opy_ (u"ࠩࡵࡦࠬᐛ")) as f:
                        return base64.b64encode(f.read()).decode(bstack111ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᐜ"))
            except Exception as e:
                logger.debug(bstack111ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡩ࡭ࡱ࡫ࠠࡼࡲࡤࡸ࡭ࢃ࠺ࠡࡽࡨࢁࠧᐝ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll11111lll_opy_ = False
            self._1l1lll1l111_opy_ = False
            self._current_test_name = name
            self._1ll111111l1_opy_ = None
            self._1l1lllll111_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack111ll_opy_ (u"ࠬ࡯ࡤࠨᐞ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack111ll_opy_ (u"࠭ࡩࡥࠩᐟ"), None)
            self._clear_session_data()
            bstack1lll1ll11ll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lll1ll11ll_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lll1ll11ll_opy_)
            return
        logger.debug(bstack111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡴࡦࡵࡷࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡴࡦࡵࡷ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧᐠ").format(name=name))
        self._1ll11111lll_opy_ = False
        self._1l1lll1l111_opy_ = False
        self._current_test_name = name
        self._1ll111111l1_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lll1ll11ll_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1l1lll11lll_opy_ = SimpleNamespace(
                status=attrs.get(bstack111ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᐡ")),
                message=attrs.get(bstack111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᐢ"), bstack111ll_opy_ (u"ࠪࠫᐣ")),
                starttime=attrs.get(bstack111ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠧᐤ"), bstack111ll_opy_ (u"ࠬ࠭ᐥ")),
                endtime=attrs.get(bstack111ll_opy_ (u"࠭ࡥ࡯ࡦࡷ࡭ࡲ࡫ࠧᐦ"), bstack111ll_opy_ (u"ࠧࠨᐧ")),
                elapsedtime=attrs.get(bstack111ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᐨ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lll1ll11ll_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lll1ll11ll_opy_, bstack1l1lll11lll_opy_)
        status = attrs.get(bstack111ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᐩ"), bstack111ll_opy_ (u"࡙ࠪࡓࡑࡎࡐ࡙ࡑࠫᐪ"))
        message = attrs.get(bstack111ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐫ"), bstack111ll_opy_ (u"ࠬ࠭ᐬ"))
        logger.debug(bstack111ll_opy_ (u"ࠨࡥ࡯ࡦࡢࡸࡪࡹࡴࠡࡅࡄࡐࡑࡋࡄࠡ࠯ࠣࡸࡪࡹࡴ࠻ࠢࡾࡲࡦࡳࡥࡾ࠮ࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࡹࡴࡢࡶࡸࡷࢂࠨᐭ").format(name=name, status=status))
        self._1ll11111lll_opy_ = True
        if not self._1l1lll1l111_opy_ and self._1ll11111ll1_opy_():
            try:
                global_config = Config.bstack1l1l11ll1_opy_()
                if not global_config.bstack1ll1lll11ll_opy_():
                    self._1ll1111l11l_opy_(name)
                if not global_config.bstack1ll1ll1lll1_opy_():
                    logger.debug(bstack111ll_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡵࡷࡥࡹࡻࡳ࠾ࡽࡶࡸࡦࡺࡵࡴࡿࠥᐮ").format(status=status))
                    self._1l1llll11ll_opy_(status, message)
                self._1l1lll1l111_opy_ = True
                logger.debug(bstack111ll_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᐯ"))
            except Exception as e:
                logger.error(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡪࢃࠢᐰ").format(e=e))
        elif self._1l1lll1l111_opy_:
            logger.debug(bstack111ll_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤࡦࡲࡲࡦࡣࡧࡽࠥࡳࡡࡳ࡭ࡨࡨࠧᐱ"))
        else:
            logger.debug(bstack111ll_opy_ (u"ࠦࡓࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠢᐲ"))
    def start_suite(self, name, attrs):
        bstack111ll_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡽࡨࡦࡰࠣࡥࠥࡹࡵࡪࡶࡨࠤࡸࡺࡡࡳࡶࡶࠦࠧࠨᐳ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack111ll_opy_ (u"࠭ࡩࡥࠩᐴ"), None)
            bstack1ll1111l1l1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1ll1111l1l1_opy_)
            return
        logger.debug(bstack111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢᐵ").format(name=name))
    def end_suite(self, name, attrs):
        bstack111ll_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡹ࡫ࡩࡳࠦࡡࠡࡵࡸ࡭ࡹ࡫ࠠࡦࡰࡧࡷࠧࠨࠢᐶ")
        if cli.is_running():
            bstack1ll1111l1l1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1ll1111l1l1_opy_)
            return
        logger.debug(bstack111ll_opy_ (u"ࠤࡨࡲࡩࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢᐷ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᐸ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᐹ"), None)
            if attrs.get(bstack111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᐺ"), bstack111ll_opy_ (u"࠭ࠧᐻ")).lower() in [bstack111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᐼ"), bstack111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᐽ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack111ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᐾ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1l1lll1l1l1_opy_ = SimpleNamespace(name=attrs.get(bstack111ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪᐿ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1l1lll1l1l1_opy_)
            else:
                if current_test_id:
                    bstack1l1lll1l1l1_opy_ = SimpleNamespace(name=attrs.get(bstack111ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᑀ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1l1lll1l1l1_opy_, test_id=current_test_id)
            try:
                if cli.accessibility and cli.bstack11l111l1l_opy_:
                    _1l1llllllll_opy_ = next(iter(bstack11l1l1l1_opy_.bstack111l11l1l1_opy_.values()), None)
                    if _1l1llllllll_opy_ and attrs.get(bstack111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᑁ"), bstack111ll_opy_ (u"࠭ࠧᑂ")).lower() not in [bstack111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᑃ"), bstack111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑄ")]:
                        cli.accessibility.bstack1l1llllll1l_opy_(
                            cli.bstack11l111l1l_opy_,
                            None,
                            (_1l1llllllll_opy_, bstack111ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࠩᑅ")),
                            (bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE),
                            None,
                            [name, attrs],
                        )
            except Exception as _e:
                logger.debug(bstack111ll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦ࠽ࠤࡦ࠷࠱ࡺࠢࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥᑆ").format(e=_e))
        if name.lower() in self._CLOSE_KEYWORDS:
            try:
                if cli.accessibility:
                    cli.accessibility.bstack1l1lllll11l_opy_()
            except Exception as _e:
                logger.debug(bstack111ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢ࡯ࡪࡿࡷࡰࡴࡧ࠾ࠥࡧ࠱࠲ࡻࠣࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࡡࡥࡩ࡫ࡵࡲࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨᑇ").format(e=_e))
        if self._1l1lll1l111_opy_ or self._1ll11111lll_opy_:
            return
        bstack1ll11111111_opy_ = False
        bstack1ll1111l1ll_opy_ = attrs.get(bstack111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᑈ"), bstack111ll_opy_ (u"࠭ࠧᑉ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1ll11111111_opy_ = True
            logger.debug(bstack111ll_opy_ (u"ࠢࡄ࡮ࡲࡷࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡩࡵࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦᑊ").format(name=name))
        elif bstack1ll1111l1ll_opy_ == bstack111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑋ"):
            bstack1ll11111111_opy_ = True
            logger.debug(bstack111ll_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬࠲ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡷࡩࡦࡸࡤࡰࡹࡱࠤࡪࡾࡥࡤࡷࡷࡩࡸࠨᑌ"))
        if bstack1ll11111111_opy_ and self._1ll11111ll1_opy_():
            self._populate_browser_instance_data()
            self._1l1llll1lll_opy_()
    def end_keyword(self, name, attrs):
        bstack111ll_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡥ࡫ࡺࡥࡳࠢࡤࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡳ࠯ࠤࠥࠦᑍ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᑎ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧᑏ"), None)
            bstack1l1lll1l1l1_opy_ = SimpleNamespace(name=attrs.get(bstack111ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᑐ"), name), id=current_test_id, **attrs)
            bstack1l1lll11lll_opy_ = SimpleNamespace(
                status=attrs.get(bstack111ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᑑ")),
                message=attrs.get(bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑒ"), bstack111ll_opy_ (u"ࠩࠪᑓ")),
                starttime=attrs.get(bstack111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡶ࡬ࡱࡪ࠭ᑔ"), bstack111ll_opy_ (u"ࠫࠬᑕ")),
                endtime=attrs.get(bstack111ll_opy_ (u"ࠬ࡫࡮ࡥࡶ࡬ࡱࡪ࠭ᑖ"), bstack111ll_opy_ (u"࠭ࠧᑗ")),
                elapsedtime=attrs.get(bstack111ll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬᑘ"), 0)
            )
            if attrs.get(bstack111ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᑙ"), bstack111ll_opy_ (u"ࠩࠪᑚ")).lower() in [bstack111ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᑛ"), bstack111ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᑜ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᑝ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1l1lll1l1l1_opy_, bstack1l1lll11lll_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1l1lll1l1l1_opy_, bstack1l1lll11lll_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᑞ"), bstack111ll_opy_ (u"ࠧࠨᑟ")).upper() == bstack111ll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᑠ")):
                logger.debug(bstack111ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࠣࡳࡵ࡫࡮ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨ࠿ࠦࡻ࡯ࡣࡰࡩࢂ࠲ࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠥᑡ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack111ll_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡶࡾࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡲࡷࡹࡷ࡫ࡳࠡࡈࡄࡍࡑࠦ࡬ࡦࡸࡨࡰࠥࡳࡥࡴࡵࡤ࡫ࡪࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡢࡵࠣࡩࡷࡸ࡯ࡳࠢࡵࡩࡦࡹ࡯࡯࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡯࡮ࡤࡧࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡺࡴࡳࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡺࡨࡦࠢࡨࡶࡷࡵࡲࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᑢ")
        if cli.is_running():
            try:
                if message.get(bstack111ll_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩᑣ"), bstack111ll_opy_ (u"ࠬࡴ࡯ࠨᑤ")) == bstack111ll_opy_ (u"࠭ࡹࡦࡵࠪᑥ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᑦ"), bstack111ll_opy_ (u"ࠨࠩᑧ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack111ll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᑨ"),
                            level=bstack111ll_opy_ (u"ࠪࡍࡓࡌࡏࠨᑩ"),
                            timestamp=message.get(bstack111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᑪ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧᑫ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᑬ"), bstack111ll_opy_ (u"ࠧࠨᑭ")),
                        level=message.get(bstack111ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᑮ"), bstack111ll_opy_ (u"ࠩࡌࡒࡋࡕࠧᑯ")),
                        timestamp=message.get(bstack111ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᑰ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᑱ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack111ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᑲ"), bstack111ll_opy_ (u"࠭ࠧᑳ"))
        if level == bstack111ll_opy_ (u"ࠧࡇࡃࡌࡐࠬᑴ"):
            self._1ll111111l1_opy_ = message.get(bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑵ"), bstack111ll_opy_ (u"ࠩࠪᑶ"))
            logger.debug(bstack111ll_opy_ (u"ࠥࡇࡦࡶࡴࡶࡴࡨࡨࠥ࡫ࡲࡳࡱࡵࠤࡲ࡫ࡳࡴࡣࡪࡩ࠿ࠦࡻࡦࡴࡵࡳࡷࢃࠢᑷ").format(error=self._1ll111111l1_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack111ll_opy_ (u"ࠦࠧࠨࡄࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡬ࡪࠥࡹࡥࡵࡷࡳ࠳ࡹ࡫ࡡࡳࡦࡲࡻࡳࠦࡩࡴࠢࡶࡹ࡮ࡺࡥ࠮࡮ࡨࡺࡪࡲࠠࡰࡴࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲ࠮ࠣࠤࠥᑸ")
        if hook_type.lower() == bstack111ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᑹ"):
            return bstack111ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᑺ") if current_test_uuid is None else bstack111ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᑻ")
        elif hook_type.lower() == bstack111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑼ"):
            return bstack111ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᑽ") if current_test_uuid is None else bstack111ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑾ")