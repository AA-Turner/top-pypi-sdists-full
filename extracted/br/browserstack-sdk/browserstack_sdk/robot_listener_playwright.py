# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll1llll_opy_ import bstack111111l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll111l1l1_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import bstack11ll11l1l1_opy_, bstack11l111l1l_opy_, bstack1111111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l111_opy_ import bstack1ll1l1l111_opy_, Events, bstack1ll1l1l1ll_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1l1lllllll1_opy_
    _1l1lll1l11l_opy_ = bstack1l1lllllll1_opy_.VERSION
except:
    _1l1lll1l11l_opy_ = bstack111ll11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᎸ")
cli_context = bstack1lll111l1l1_opy_(
    test_framework_name=bstack111ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᎹ"),
    test_framework_version=_1l1lll1l11l_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack111ll11_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴࠪᎺ"), bstack111ll11_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡧࡴࡴࡴࡦࡺࡷࠫᎻ"), bstack111ll11_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡵࡧࡧࡦࠩᎼ"),
        bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠧᎽ"), bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡱࡸࡪࡾࡴࠨᎾ"), bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡲࡤ࡫ࡪ࠭Ꮏ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack111ll11_opy_ (u"ࠩࡱࡩࡼࠦࡢࡳࡱࡺࡷࡪࡸࠧᏀ"), bstack111ll11_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠤࡹࡵࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᏁ"),
        bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࠢࡥࡶࡴࡽࡳࡦࡴࠪᏂ"), bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣࡰࡰࡱࡩࡨࡺࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࠫᏃ"),
    }
    def __init__(self):
        self._1ll11111111_opy_ = None
        self._1ll111111l1_opy_ = False
        self._1l1llll111l_opy_ = False
        self._current_test_name = None
        self._1l1llllll11_opy_ = None
        self._1ll111111ll_opy_ = False
        if cli.bstack11l1l1l11_opy_():
            try:
                if cli.bstack1ll111l111_opy_:
                    cli_context.platform_index = cli.bstack1ll111l111_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮔ"), bstack111ll11_opy_ (u"ࠧ࠱ࠩᏅ")))
            except Exception as e:
                pass
        PlaywrightPatcher._1ll111l111l_opy_()
    @staticmethod
    def _1ll111l111l_opy_():
        try:
            import functools
            from Browser.keywords.bstack1lllll11l11_opy_ import bstack1l1llll11l1_opy_
            from browserstack_sdk.sdk_cli.bstack1l1llll1l1l_opy_ import bstack1l1llll1111_opy_
            _1ll111l11l1_opy_ = bstack1l1llll11l1_opy_.close_browser
            _1l1lll1l111_opy_ = bstack1l1llll11l1_opy_.bstack1l1llll1ll1_opy_
            @functools.wraps(_1ll111l11l1_opy_)
            def _1l1lll1llll_opy_(self, browser=bstack111ll11_opy_ (u"ࠣࡅࡘࡖࡗࡋࡎࡕࠤᏆ")):
                if not bstack1l1llll1111_opy_._1l1llllll1l_opy_.is_set():
                    logger.debug(bstack111ll11_opy_ (u"ࠤࡦࡰࡴࡹࡥࡠࡤࡵࡳࡼࡹࡥࡳ࠼ࠣࡥ࠶࠷ࡹࠡࡵࡦࡥࡳࠦࡩ࡯ࠢࡳࡶࡴ࡭ࡲࡦࡵࡶ࠰ࠥࡽࡡࡪࡶ࡬ࡲ࡬ࠦࡵࡱࠢࡷࡳࠥ࠷࠵ࡴࠤᏇ"))
                    bstack1l1llll1111_opy_._1l1llllll1l_opy_.wait(timeout=15)
                return _1ll111l11l1_opy_(self, browser)
            @functools.wraps(_1l1lll1l111_opy_)
            def _1ll1111l1l1_opy_(self, page=bstack111ll11_opy_ (u"ࠥࡇ࡚ࡘࡒࡆࡐࡗࠦᏈ")):
                if not bstack1l1llll1111_opy_._1l1llllll1l_opy_.is_set():
                    logger.debug(bstack111ll11_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࡢࡴࡦ࡭ࡥ࠻ࠢࡤ࠵࠶ࡿࠠࡴࡥࡤࡲࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵ࠯ࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡶࡲࠤ࠶࠻ࡳࠣᏉ"))
                    bstack1l1llll1111_opy_._1l1llllll1l_opy_.wait(timeout=15)
                return _1l1lll1l111_opy_(self, page)
            bstack1l1llll11l1_opy_.close_browser = _1l1lll1llll_opy_
            bstack1l1llll11l1_opy_.bstack1l1llll1ll1_opy_ = _1ll1111l1l1_opy_
            logger.debug(bstack111ll11_opy_ (u"ࠧࡥࡰࡢࡶࡦ࡬ࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡦࡰࡴࡹࡥࡠ࡯ࡨࡸ࡭ࡵࡤࡴ࠼ࠣࡴࡦࡺࡣࡩࡧࡧࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡔࡶࡤࡸࡪࠦࡣ࡭ࡱࡶࡩࠥࡳࡥࡵࡪࡲࡨࡸࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡩࡤࡸࡪࠨᏊ"))
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠨ࡟ࡱࡣࡷࡧ࡭ࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡢࡧࡱࡵࡳࡦࡡࡰࡩࡹ࡮࡯ࡥࡵ࠽ࠤࡸࡱࡩࡱࡲࡨࡨࠥ࠮ࡂࡳࡱࡺࡷࡪࡸࠠ࡭࡫ࡥࡶࡦࡸࡹࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡱࡵࠤࡦ࠷࠱ࡺࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧ࠭࠿ࠦࡻࡦࡿࠥᏋ").format(e=e))
    def _1ll1111ll1l_opy_(self):
        if self._1ll11111111_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1ll11111111_opy_ = BuiltIn().get_library_instance(bstack111ll11_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࠨᏌ"))
            except Exception as e:
                logger.warning(bstack111ll11_opy_ (u"ࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤ࡬࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠿ࠦࡻࡦࡿࠥᏍ").format(e=e))
        return self._1ll11111111_opy_
    def _1l1lll1ll1l_opy_(self):
        try:
            bstack1lllll11l1l_opy_ = self._1ll1111ll1l_opy_()
            if bstack1lllll11l1l_opy_ and hasattr(bstack1lllll11l1l_opy_, bstack111ll11_opy_ (u"ࠩࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࡟ࡴࡶࡤࡸࡪ࠭Ꮞ")):
                bstack1lllll11l11_opy_ = bstack1lllll11l1l_opy_._playwright_state
                if hasattr(bstack1lllll11l11_opy_, bstack111ll11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡥࡹࡧ࡬ࡰࡩࠪᏏ")):
                    bstack1lllll111ll_opy_ = bstack1lllll11l11_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lllll111ll_opy_ = BuiltIn().run_keyword(bstack111ll11_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡍࡥࡵࠢࡅࡶࡴࡽࡳࡦࡴࠣࡇࡦࡺࡡ࡭ࡱࡪࠫᏐ"))
                for bstack1ll11111l1l_opy_ in bstack1lllll111ll_opy_:
                    contexts = bstack1ll11111l1l_opy_.get(bstack111ll11_opy_ (u"ࠬࡩ࡯࡯ࡶࡨࡼࡹࡹࠧᏑ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack111ll11_opy_ (u"࠭ࡰࡢࡩࡨࡷࠬᏒ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack111ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧ࠽ࠤࢀ࡫ࡽࠣᏓ").format(e=e))
            return False
    def _1l1lllll11l_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1l1lll1lll1_opy_ = {
                bstack111ll11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᏔ"): action,
                bstack111ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᏕ"): arguments
            }
            executor_cmd = bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥ࠭Ꮦ") + json.dumps(bstack1l1lll1lll1_opy_)
            arg_string = bstack111ll11_opy_ (u"ࠦࡦࡸࡧ࠾ࡽࡨࡼࡪࡩࡵࡵࡱࡵࡣࡨࡳࡤࡾࠤᏗ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack111ll11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠴ࡅࡷࡣ࡯ࡹࡦࡺࡥࠡࡌࡤࡺࡦ࡙ࡣࡳ࡫ࡳࡸࠬᏘ"),
                None,
                bstack111ll11_opy_ (u"࠭࡟ࠡ࠿ࡁࠤࢀࢃࠧᏙ"),
                arg_string
            )
            logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡨࡧࡺࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡧࡣࡵ࡫ࡲࡲࢂ࠲ࠠࡳࡧࡶࡹࡱࡺ࠺ࠡࡽࡵࡩࡸࡻ࡬ࡵࡿࠥᏚ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack111ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡪࡾࡥࡤࡷࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡧࢀࠦᏛ").format(e=e))
    def _populate_browser_instance_data(self):
        bstack111ll11_opy_ (u"ࠤࠥࠦࡕࡵࡰࡶ࡮ࡤࡸࡪࠦࡨࡶࡤࡢࡹࡷࡲࠠࡢࡰࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡱࠤࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࠦࡦࡰࡴࠣࡶࡴࡨ࡯ࡵ࠯ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࠢࠣࠤᏜ")
        try:
            from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
            if not self._1l1lll1ll1l_opy_():
                logger.debug(bstack111ll11_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧ࠺ࠡࡰࡲࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᏝ"))
                return
            result = self._1l1lllll11l_opy_(bstack111ll11_opy_ (u"ࠫ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠨᏞ"), {})
            logger.debug(bstack111ll11_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠠࡳࡧࡶࡹࡱࡺ࠽ࡼࡴࢀࠦᏟ").format(r=result))
            if not result:
                logger.debug(bstack111ll11_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡳࡵࠠࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤᏠ"))
                return
            bstack1l1llll1lll_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1l1llll1lll_opy_.get(bstack111ll11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᏡ"), bstack111ll11_opy_ (u"ࠨࠩᏢ"))
            hub_url = os.environ.get(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡒࡆࡔ࡚࡟ࡑ࡙ࡢࡇࡉࡖ࡟ࡖࡔࡏࠫᏣ"), bstack111ll11_opy_ (u"ࠪࠫᏤ"))
            logger.debug(bstack111ll11_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࡻࡴ࡫ࡧࢁ࠱ࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࡼࡷࡵࡰࢂࠨᏥ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack111ll11_opy_ (u"ࠬ࠭Ꮶ")))
            current_test_id = getattr(threading.current_thread(), bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨᏧ"), None)
            for instance in bstack11ll11l1l1_opy_.bstack1111l11ll_opy_.values():
                if not bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll11111_opy_.bstack1ll11111lll_opy_, None):
                    bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack1ll11111lll_opy_, session_id)
                    bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack111llll1ll_opy_, hub_url)
                    if current_test_id:
                        bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨᏨ"), current_test_id)
                    logger.debug(bstack111ll11_opy_ (u"ࠣࡒࡲࡴࡺࡲࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠺ࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࢁࡳࡪࡦࢀ࠰ࠥ࡮ࡵࡣࡡࡸࡶࡱࠦࡳࡦࡶ࠯ࠤࡹ࡫ࡳࡵࡡ࡬ࡨࡂࢁࡴࡪࡦࢀࠦᏩ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡨࡦࡺࡡ࠻ࠢࡾࡩࢂࠨᏪ").format(e=e))
    def _clear_session_data(self):
        bstack111ll11_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡣ࡯ࡰࠥࡨࡲࡰࡹࡶࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠢࡷࡳࠥ࡫࡮ࡴࡷࡵࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࡵ࡬ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᏫ")
        try:
            from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
            bstack1l1lll1l1l1_opy_ = 0
            for instance in bstack11ll11l1l1_opy_.bstack1111l11ll_opy_.values():
                bstack1ll1111l111_opy_ = False
                if bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll11111_opy_.bstack1ll11111lll_opy_, None):
                    bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack1ll11111lll_opy_, bstack111ll11_opy_ (u"ࠫࠬᏬ"))
                    bstack1ll1111l111_opy_ = True
                if bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll11111_opy_.bstack111llll1ll_opy_, None):
                    bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack111llll1ll_opy_, bstack111ll11_opy_ (u"ࠬ࠭Ꮽ"))
                    bstack1ll1111l111_opy_ = True
                if bstack111ll11111_opy_.bstack1l1lllll1l1_opy_(instance, bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧᏮ"), None):
                    bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨᏯ"), None)
                    bstack1ll1111l111_opy_ = True
                if bstack11ll11l1l1_opy_.bstack1l1llll1l11_opy_(instance, bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹ࠭Ᏸ")):
                    bstack11ll11l1l1_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡲ࡮ࡺࠧᏱ"), None)
                    bstack1ll1111l111_opy_ = True
                if bstack1ll1111l111_opy_:
                    bstack1l1lll1l1l1_opy_ += 1
            logger.debug(bstack111ll11_opy_ (u"ࠥࡣࡨࡲࡥࡢࡴࡢࡷࡪࡹࡳࡪࡱࡱࡣࡩࡧࡴࡢ࠼ࠣࡇࡱ࡫ࡡࡳࡧࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡽࡱࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠣᏲ").format(
                n=bstack1l1lll1l1l1_opy_))
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡦࡿࠥᏳ").format(e=e))
    def _1ll1111l1ll_opy_(self, status, reason=bstack111ll11_opy_ (u"ࠧࠨᏴ")):
        bstack111ll11_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦᏵ")
        bstack1l1lll1ll11_opy_ = bstack111ll11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ᏶") if status == bstack111ll11_opy_ (u"ࠣࡒࡄࡗࡘࠨ᏷") else bstack111ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᏸ")
        if bstack1l1lll1ll11_opy_ == bstack111ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᏹ"):
            return self._1l1lllll11l_opy_(bstack111ll11_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᏺ"), {
                bstack111ll11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᏻ"): bstack1l1lll1ll11_opy_,
                bstack111ll11_opy_ (u"ࠨࡲࡦࡣࡶࡳࡳࠨᏼ"): reason
            })
        else:
            return self._1l1lllll11l_opy_(bstack111ll11_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᏽ"), {
                bstack111ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᏾"): bstack1l1lll1ll11_opy_
            })
    def _1ll1111ll11_opy_(self, name):
        bstack111ll11_opy_ (u"ࠤࠥࠦࡘ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦ᏿")
        return self._1l1lllll11l_opy_(bstack111ll11_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ᐀"), {
            bstack111ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐁ"): name
        })
    def _1l1lll1l1ll_opy_(self):
        bstack111ll11_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡣࡧࡩࡳࡷ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡥ࡯ࡳࡸ࡫ࠠࡰࡴࠣࡸࡪࡧࡲࡥࡱࡺࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡶࡤࡸࡺࡹࠠࡪࡵࠣ࡭ࡳ࡬ࡥࡳࡴࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡣࡱࡧࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦ࠼ࠣ࡭࡫ࠦࡡ࡯ࡻࠣࡊࡆࡏࡌ࠮࡮ࡨࡺࡪࡲࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡢࡵࠣࡧࡦࡶࡴࡶࡴࡨࡨࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡷࡩࡸࡺࠬࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࠦࡦࡢ࡫࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᐂ")
        if self._1l1llll111l_opy_:
            return
        try:
            global_config = Config.bstack1lllll1lll1_opy_()
            if self._current_test_name and not global_config.bstack1lll111llll_opy_():
                self._1ll1111ll11_opy_(self._current_test_name)
            status = bstack111ll11_opy_ (u"࠭ࡆࡂࡋࡏࠫᐃ") if self._1l1llllll11_opy_ else bstack111ll11_opy_ (u"ࠧࡑࡃࡖࡗࠬᐄ")
            message = self._1l1llllll11_opy_ or bstack111ll11_opy_ (u"ࠨࠩᐅ")
            if not global_config.bstack1ll1l1ll1l1_opy_():
                logger.debug(bstack111ll11_opy_ (u"ࠤࡐࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡨࡲ࡯ࡴࡧ࠽ࠤࡸࡺࡡࡵࡷࡶࡁࢀࡹࡴࡢࡶࡸࡷࢂ࠲ࠠ࡮ࡧࡶࡷࡦ࡭ࡥ࠾ࡽࡰࡩࡸࡹࡡࡨࡧࢀࠦᐆ").format(status=status, message=message))
                self._1ll1111l1ll_opy_(status, message)
            self._1l1llll111l_opy_ = True
            logger.debug(bstack111ll11_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡰࡥࡷࡱࡥࡥࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᐇ"))
        except Exception as e:
            logger.error(bstack111ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡧࢀࠦᐈ").format(e=e))
    def _extract_screenshot_base64(self, bstack1l1llllllll_opy_):
        bstack111ll11_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡌ࡙ࡓࡌࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡲࡦࡴࡺࠧࡴࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡱࡵࡧࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠠࡢࡵࠣࡌ࡙ࡓࡌࠡࡹ࡬ࡸ࡭ࠦࡥࡪࡶ࡫ࡩࡷࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡨࡥࡥࡦࡨࡨ࠿ࠦ࠼ࡪ࡯ࡪࠤࡸࡸࡣ࠾ࠤࡧࡥࡹࡧ࠺ࡪ࡯ࡤ࡫ࡪ࠵ࡰ࡯ࡩ࠾ࡦࡦࡹࡥ࠷࠶࠯ࡿࡩࡧࡴࡢࡿࠥࠤ࠳࠴࠮࠿ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌࡩ࡭ࡧࠣࡰ࡮ࡴ࡫࠻ࠢ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧࡶࡡࡵࡪ࠲ࡸࡴ࠵ࡦࡪ࡮ࡨ࠲ࡵࡴࡧࠣࠢ࠱࠲࠳ࡄࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᐉ")
        match = re.search(bstack111ll11_opy_ (u"ࡸࠧࡴࡴࡦࡁࠧࡪࡡࡵࡣ࠽࡭ࡲࡧࡧࡦ࠱ࡳࡲ࡬ࡁࡢࡢࡵࡨ࠺࠹࠲ࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨᐊ"), bstack1l1llllllll_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack111ll11_opy_ (u"ࡲࠨ࠾࡬ࡱ࡬ࡡ࡞࠿࡟࠮ࡷࡷࡩ࠽ࠣࠪ࡞ࡢࠧࡣࠫ࡝࠰ࠫࡃ࠿ࡶ࡮ࡨࡾ࡭ࡴ࡬ࢂࡪࡱࡧࡪ࠭࠮ࠨࠧᐋ"), bstack1l1llllllll_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1l1llll11ll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠨࡔࡒࡆࡔ࡚࡟ࡐࡗࡗࡔ࡚࡚࡟ࡅࡋࡕࠫᐌ"), os.getcwd())
                    path = Path(bstack1l1llll11ll_opy_) / path
                if path.is_file():
                    with open(path, bstack111ll11_opy_ (u"ࠩࡵࡦࠬᐍ")) as f:
                        return base64.b64encode(f.read()).decode(bstack111ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᐎ"))
            except Exception as e:
                logger.debug(bstack111ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡩ࡭ࡱ࡫ࠠࡼࡲࡤࡸ࡭ࢃ࠺ࠡࡽࡨࢁࠧᐏ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll111111l1_opy_ = False
            self._1l1llll111l_opy_ = False
            self._current_test_name = name
            self._1l1llllll11_opy_ = None
            self._1ll111111ll_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack111ll11_opy_ (u"ࠬ࡯ࡤࠨᐐ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack111ll11_opy_ (u"࠭ࡩࡥࠩᐑ"), None)
            self._clear_session_data()
            bstack1lll1l1ll11_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lll1l1ll11_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lll1l1ll11_opy_)
            return
        logger.debug(bstack111ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡴࡦࡵࡷࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡴࡦࡵࡷ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧᐒ").format(name=name))
        self._1ll111111l1_opy_ = False
        self._1l1llll111l_opy_ = False
        self._current_test_name = name
        self._1l1llllll11_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lll1l1ll11_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1ll111l1111_opy_ = SimpleNamespace(
                status=attrs.get(bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᐓ")),
                message=attrs.get(bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᐔ"), bstack111ll11_opy_ (u"ࠪࠫᐕ")),
                starttime=attrs.get(bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠧᐖ"), bstack111ll11_opy_ (u"ࠬ࠭ᐗ")),
                endtime=attrs.get(bstack111ll11_opy_ (u"࠭ࡥ࡯ࡦࡷ࡭ࡲ࡫ࠧᐘ"), bstack111ll11_opy_ (u"ࠧࠨᐙ")),
                elapsedtime=attrs.get(bstack111ll11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᐚ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lll1l1ll11_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lll1l1ll11_opy_, bstack1ll111l1111_opy_)
        status = attrs.get(bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᐛ"), bstack111ll11_opy_ (u"࡙ࠪࡓࡑࡎࡐ࡙ࡑࠫᐜ"))
        message = attrs.get(bstack111ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐝ"), bstack111ll11_opy_ (u"ࠬ࠭ᐞ"))
        logger.debug(bstack111ll11_opy_ (u"ࠨࡥ࡯ࡦࡢࡸࡪࡹࡴࠡࡅࡄࡐࡑࡋࡄࠡ࠯ࠣࡸࡪࡹࡴ࠻ࠢࡾࡲࡦࡳࡥࡾ࠮ࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࡹࡴࡢࡶࡸࡷࢂࠨᐟ").format(name=name, status=status))
        self._1ll111111l1_opy_ = True
        if not self._1l1llll111l_opy_ and self._1l1lll1ll1l_opy_():
            try:
                global_config = Config.bstack1lllll1lll1_opy_()
                if not global_config.bstack1lll111llll_opy_():
                    self._1ll1111ll11_opy_(name)
                if not global_config.bstack1ll1l1ll1l1_opy_():
                    logger.debug(bstack111ll11_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡵࡷࡥࡹࡻࡳ࠾ࡽࡶࡸࡦࡺࡵࡴࡿࠥᐠ").format(status=status))
                    self._1ll1111l1ll_opy_(status, message)
                self._1l1llll111l_opy_ = True
                logger.debug(bstack111ll11_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᐡ"))
            except Exception as e:
                logger.error(bstack111ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡪࢃࠢᐢ").format(e=e))
        elif self._1l1llll111l_opy_:
            logger.debug(bstack111ll11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤࡦࡲࡲࡦࡣࡧࡽࠥࡳࡡࡳ࡭ࡨࡨࠧᐣ"))
        else:
            logger.debug(bstack111ll11_opy_ (u"ࠦࡓࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠢᐤ"))
    def start_suite(self, name, attrs):
        bstack111ll11_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡽࡨࡦࡰࠣࡥࠥࡹࡵࡪࡶࡨࠤࡸࡺࡡࡳࡶࡶࠦࠧࠨᐥ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack111ll11_opy_ (u"࠭ࡩࡥࠩᐦ"), None)
            bstack1ll1111l11l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1ll1111l11l_opy_)
            return
        logger.debug(bstack111ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢᐧ").format(name=name))
    def end_suite(self, name, attrs):
        bstack111ll11_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡹ࡫ࡩࡳࠦࡡࠡࡵࡸ࡭ࡹ࡫ࠠࡦࡰࡧࡷࠧࠨࠢᐨ")
        if cli.is_running():
            bstack1ll1111l11l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1ll1111l11l_opy_)
            return
        logger.debug(bstack111ll11_opy_ (u"ࠤࡨࡲࡩࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢᐩ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᐪ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᐫ"), None)
            if attrs.get(bstack111ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪᐬ"), bstack111ll11_opy_ (u"࠭ࠧᐭ")).lower() in [bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᐮ"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᐯ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack111ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᐰ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1ll11111ll1_opy_ = SimpleNamespace(name=attrs.get(bstack111ll11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪᐱ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1ll11111ll1_opy_)
            else:
                if current_test_id:
                    bstack1ll11111ll1_opy_ = SimpleNamespace(name=attrs.get(bstack111ll11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᐲ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1ll11111ll1_opy_, test_id=current_test_id)
            try:
                if cli.accessibility and cli.bstack1ll111l111_opy_:
                    _1l1lllll111_opy_ = next(iter(bstack11ll11l1l1_opy_.bstack1111l11ll_opy_.values()), None)
                    if _1l1lllll111_opy_ and attrs.get(bstack111ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪᐳ"), bstack111ll11_opy_ (u"࠭ࠧᐴ")).lower() not in [bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᐵ"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᐶ")]:
                        cli.accessibility.bstack1ll1111111l_opy_(
                            cli.bstack1ll111l111_opy_,
                            None,
                            (_1l1lllll111_opy_, bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࠩᐷ")),
                            (bstack11l111l1l_opy_.bstack1ll1111lll1_opy_, bstack1111111ll_opy_.PRE),
                            None,
                            [name, attrs],
                        )
            except Exception as _e:
                logger.debug(bstack111ll11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦ࠽ࠤࡦ࠷࠱ࡺࠢࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥᐸ").format(e=_e))
        if name.lower() in self._CLOSE_KEYWORDS:
            try:
                if cli.accessibility:
                    cli.accessibility.bstack1ll11111l11_opy_()
            except Exception as _e:
                logger.debug(bstack111ll11_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢ࡯ࡪࡿࡷࡰࡴࡧ࠾ࠥࡧ࠱࠲ࡻࠣࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࡡࡥࡩ࡫ࡵࡲࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨᐹ").format(e=_e))
        if self._1l1llll111l_opy_ or self._1ll111111l1_opy_:
            return
        bstack1l1lllll1ll_opy_ = False
        bstack1ll1111llll_opy_ = attrs.get(bstack111ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪᐺ"), bstack111ll11_opy_ (u"࠭ࠧᐻ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1l1lllll1ll_opy_ = True
            logger.debug(bstack111ll11_opy_ (u"ࠢࡄ࡮ࡲࡷࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡩࡵࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦᐼ").format(name=name))
        elif bstack1ll1111llll_opy_ == bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᐽ"):
            bstack1l1lllll1ll_opy_ = True
            logger.debug(bstack111ll11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬࠲ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡷࡩࡦࡸࡤࡰࡹࡱࠤࡪࡾࡥࡤࡷࡷࡩࡸࠨᐾ"))
        if bstack1l1lllll1ll_opy_ and self._1l1lll1ll1l_opy_():
            self._populate_browser_instance_data()
            self._1l1lll1l1ll_opy_()
    def end_keyword(self, name, attrs):
        bstack111ll11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡥ࡫ࡺࡥࡳࠢࡤࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡳ࠯ࠤࠥࠦᐿ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᑀ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧᑁ"), None)
            bstack1ll11111ll1_opy_ = SimpleNamespace(name=attrs.get(bstack111ll11_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ᑂ"), name), id=current_test_id, **attrs)
            bstack1ll111l1111_opy_ = SimpleNamespace(
                status=attrs.get(bstack111ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᑃ")),
                message=attrs.get(bstack111ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑄ"), bstack111ll11_opy_ (u"ࠩࠪᑅ")),
                starttime=attrs.get(bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡶ࡬ࡱࡪ࠭ᑆ"), bstack111ll11_opy_ (u"ࠫࠬᑇ")),
                endtime=attrs.get(bstack111ll11_opy_ (u"ࠬ࡫࡮ࡥࡶ࡬ࡱࡪ࠭ᑈ"), bstack111ll11_opy_ (u"࠭ࠧᑉ")),
                elapsedtime=attrs.get(bstack111ll11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬᑊ"), 0)
            )
            if attrs.get(bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᑋ"), bstack111ll11_opy_ (u"ࠩࠪᑌ")).lower() in [bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᑍ"), bstack111ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᑎ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack111ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪᑏ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1ll11111ll1_opy_, bstack1ll111l1111_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1ll11111ll1_opy_, bstack1ll111l1111_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᑐ"), bstack111ll11_opy_ (u"ࠧࠨᑑ")).upper() == bstack111ll11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᑒ")):
                logger.debug(bstack111ll11_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࠣࡳࡵ࡫࡮ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨ࠿ࠦࡻ࡯ࡣࡰࡩࢂ࠲ࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠥᑓ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack111ll11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡶࡾࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡲࡷࡹࡷ࡫ࡳࠡࡈࡄࡍࡑࠦ࡬ࡦࡸࡨࡰࠥࡳࡥࡴࡵࡤ࡫ࡪࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡢࡵࠣࡩࡷࡸ࡯ࡳࠢࡵࡩࡦࡹ࡯࡯࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡯࡮ࡤࡧࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡺࡴࡳࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡺࡨࡦࠢࡨࡶࡷࡵࡲࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᑔ")
        if cli.is_running():
            try:
                if message.get(bstack111ll11_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩᑕ"), bstack111ll11_opy_ (u"ࠬࡴ࡯ࠨᑖ")) == bstack111ll11_opy_ (u"࠭ࡹࡦࡵࠪᑗ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᑘ"), bstack111ll11_opy_ (u"ࠨࠩᑙ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack111ll11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᑚ"),
                            level=bstack111ll11_opy_ (u"ࠪࡍࡓࡌࡏࠨᑛ"),
                            timestamp=message.get(bstack111ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᑜ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧᑝ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᑞ"), bstack111ll11_opy_ (u"ࠧࠨᑟ")),
                        level=message.get(bstack111ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᑠ"), bstack111ll11_opy_ (u"ࠩࡌࡒࡋࡕࠧᑡ")),
                        timestamp=message.get(bstack111ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᑢ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ᑣ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack111ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᑤ"), bstack111ll11_opy_ (u"࠭ࠧᑥ"))
        if level == bstack111ll11_opy_ (u"ࠧࡇࡃࡌࡐࠬᑦ"):
            self._1l1llllll11_opy_ = message.get(bstack111ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᑧ"), bstack111ll11_opy_ (u"ࠩࠪᑨ"))
            logger.debug(bstack111ll11_opy_ (u"ࠥࡇࡦࡶࡴࡶࡴࡨࡨࠥ࡫ࡲࡳࡱࡵࠤࡲ࡫ࡳࡴࡣࡪࡩ࠿ࠦࡻࡦࡴࡵࡳࡷࢃࠢᑩ").format(error=self._1l1llllll11_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack111ll11_opy_ (u"ࠦࠧࠨࡄࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡬ࡪࠥࡹࡥࡵࡷࡳ࠳ࡹ࡫ࡡࡳࡦࡲࡻࡳࠦࡩࡴࠢࡶࡹ࡮ࡺࡥ࠮࡮ࡨࡺࡪࡲࠠࡰࡴࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲ࠮ࠣࠤࠥᑪ")
        if hook_type.lower() == bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᑫ"):
            return bstack111ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪᑬ") if current_test_uuid is None else bstack111ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᑭ")
        elif hook_type.lower() == bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑮ"):
            return bstack111ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᑯ") if current_test_uuid is None else bstack111ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑰ")