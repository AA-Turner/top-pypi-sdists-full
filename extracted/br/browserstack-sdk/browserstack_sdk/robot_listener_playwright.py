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
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll11111l1_opy_ import bstack1llll11l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll11l111l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack1l1l1ll1ll_opy_ import bstack1111lll1ll_opy_, bstack1l1111l1l1_opy_, bstack1ll111111l_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l_opy_ import bstack111111l1l_opy_, Events, bstack1ll1ll1l_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1l1lll1l1ll_opy_
    _1l1lllllll1_opy_ = bstack1l1lll1l1ll_opy_.VERSION
except:
    _1l1lllllll1_opy_ = bstack1ll1l11_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᎡ")
cli_context = bstack1lll11l111l_opy_(
    test_framework_name=bstack1ll1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭Ꭲ"),
    test_framework_version=_1l1lllllll1_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1ll1l11_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᎣ"), bstack1ll1l11_opy_ (u"ࠩࡦࡰࡴࡹࡥࠡࡥࡲࡲࡹ࡫ࡸࡵࠩᎤ"), bstack1ll1l11_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡳࡥ࡬࡫ࠧᎥ"),
        bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠬᎦ"), bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩࠥࡩ࡯࡯ࡶࡨࡼࡹ࠭Ꭷ"), bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡰࡢࡩࡨࠫᎨ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1ll1l11_opy_ (u"ࠧ࡯ࡧࡺࠤࡧࡸ࡯ࡸࡵࡨࡶࠬᎩ"), bstack1ll1l11_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠢࡷࡳࠥࡨࡲࡰࡹࡶࡩࡷ࠭Ꭺ"),
        bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᎫ"), bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࠩᎬ"),
    }
    def __init__(self):
        self._1l1lll1llll_opy_ = None
        self._1ll1111llll_opy_ = False
        self._1l1llll1l11_opy_ = False
        self._current_test_name = None
        self._1ll111l1l11_opy_ = None
        self._1ll111111l1_opy_ = False
        if cli.bstack11lll111l_opy_():
            try:
                if cli.bstack1l1l1ll1ll_opy_:
                    cli_context.platform_index = cli.bstack1l1l1ll1ll_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᎭ"), bstack1ll1l11_opy_ (u"ࠬ࠶ࠧᎮ")))
            except Exception as e:
                pass
        PlaywrightPatcher._1l1llll1ll1_opy_()
    @staticmethod
    def _1l1llll1ll1_opy_():
        try:
            import functools
            from Browser.keywords.bstack1lllll1l11l_opy_ import bstack1l1llllll1l_opy_
            from browserstack_sdk.sdk_cli.bstack1ll1111ll1l_opy_ import bstack1l1lll1ll1l_opy_
            _1ll111111ll_opy_ = bstack1l1llllll1l_opy_.close_browser
            _1ll1111ll11_opy_ = bstack1l1llllll1l_opy_.bstack1ll111l1111_opy_
            @functools.wraps(_1ll111111ll_opy_)
            def _1l1llll1l1l_opy_(self, browser=bstack1ll1l11_opy_ (u"ࠨࡃࡖࡔࡕࡉࡓ࡚ࠢᎯ")):
                if not bstack1l1lll1ll1l_opy_._1l1llll11ll_opy_.is_set():
                    logger.debug(bstack1ll1l11_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࡥࡢࡳࡱࡺࡷࡪࡸ࠺ࠡࡣ࠴࠵ࡾࠦࡳࡤࡣࡱࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴ࠮ࠣࡻࡦ࡯ࡴࡪࡰࡪࠤࡺࡶࠠࡵࡱࠣ࠵࠺ࡹࠢᎰ"))
                    bstack1l1lll1ll1l_opy_._1l1llll11ll_opy_.wait(timeout=15)
                return _1ll111111ll_opy_(self, browser)
            @functools.wraps(_1ll1111ll11_opy_)
            def _1ll1111111l_opy_(self, page=bstack1ll1l11_opy_ (u"ࠣࡅࡘࡖࡗࡋࡎࡕࠤᎱ")):
                if not bstack1l1lll1ll1l_opy_._1l1llll11ll_opy_.is_set():
                    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡦࡰࡴࡹࡥࡠࡲࡤ࡫ࡪࡀࠠࡢ࠳࠴ࡽࠥࡹࡣࡢࡰࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳ࠭ࠢࡺࡥ࡮ࡺࡩ࡯ࡩࠣࡹࡵࠦࡴࡰࠢ࠴࠹ࡸࠨᎲ"))
                    bstack1l1lll1ll1l_opy_._1l1llll11ll_opy_.wait(timeout=15)
                return _1ll1111ll11_opy_(self, page)
            bstack1l1llllll1l_opy_.close_browser = _1l1llll1l1l_opy_
            bstack1l1llllll1l_opy_.bstack1ll111l1111_opy_ = _1ll1111111l_opy_
            logger.debug(bstack1ll1l11_opy_ (u"ࠥࡣࡵࡧࡴࡤࡪࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࡟ࡤ࡮ࡲࡷࡪࡥ࡭ࡦࡶ࡫ࡳࡩࡹ࠺ࠡࡲࡤࡸࡨ࡮ࡥࡥࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡙ࡴࡢࡶࡨࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦࡶࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡧࡢࡶࡨࠦᎳ"))
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠦࡤࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡥ࡯ࡳࡸ࡫࡟࡮ࡧࡷ࡬ࡴࡪࡳ࠻ࠢࡶ࡯࡮ࡶࡰࡦࡦࠣࠬࡇࡸ࡯ࡸࡵࡨࡶࠥࡲࡩࡣࡴࡤࡶࡾࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦ࡯ࡳࠢࡤ࠵࠶ࡿࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠫ࠽ࠤࢀ࡫ࡽࠣᎴ").format(e=e))
    def _1ll1111lll1_opy_(self):
        if self._1l1lll1llll_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1l1lll1llll_opy_ = BuiltIn().get_library_instance(bstack1ll1l11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠭Ꮅ"))
            except Exception as e:
                logger.warning(bstack1ll1l11_opy_ (u"ࠨࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡪࡩࡹࠦࡂࡳࡱࡺࡷࡪࡸࠠ࡭࡫ࡥࡶࡦࡸࡹࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀ࡫ࡽࠣᎶ").format(e=e))
        return self._1l1lll1llll_opy_
    def _1l1llllllll_opy_(self):
        try:
            bstack1lllll1l111_opy_ = self._1ll1111lll1_opy_()
            if bstack1lllll1l111_opy_ and hasattr(bstack1lllll1l111_opy_, bstack1ll1l11_opy_ (u"ࠧࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡤࡹࡴࡢࡶࡨࠫᎷ")):
                bstack1lllll1l11l_opy_ = bstack1lllll1l111_opy_._playwright_state
                if hasattr(bstack1lllll1l11l_opy_, bstack1ll1l11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤࡣࡷࡥࡱࡵࡧࠨᎸ")):
                    bstack1lllll11lll_opy_ = bstack1lllll1l11l_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lllll11lll_opy_ = BuiltIn().run_keyword(bstack1ll1l11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴ࠱ࡋࡪࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࠡࡅࡤࡸࡦࡲ࡯ࡨࠩᎹ"))
                for bstack1l1lllll111_opy_ in bstack1lllll11lll_opy_:
                    contexts = bstack1l1lllll111_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡧࡴࡴࡴࡦࡺࡷࡷࠬᎺ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1ll1l11_opy_ (u"ࠫࡵࡧࡧࡦࡵࠪᎻ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥ࠻ࠢࡾࡩࢂࠨᎼ").format(e=e))
            return False
    def _1ll1111l1l1_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1ll111l11l1_opy_ = {
                bstack1ll1l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭Ꮍ"): action,
                bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᎾ"): arguments
            }
            executor_cmd = bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠫᎿ") + json.dumps(bstack1ll111l11l1_opy_)
            arg_string = bstack1ll1l11_opy_ (u"ࠤࡤࡶ࡬ࡃࡻࡦࡺࡨࡧࡺࡺ࡯ࡳࡡࡦࡱࡩࢃࠢᏀ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1ll1l11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡊࡼࡡ࡭ࡷࡤࡸࡪࠦࡊࡢࡸࡤࡗࡨࡸࡩࡱࡶࠪᏁ"),
                None,
                bstack1ll1l11_opy_ (u"ࠫࡤࠦ࠽࠿ࠢࡾࢁࠬᏂ"),
                arg_string
            )
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡦࡥࡸࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡥࡨࡺࡩࡰࡰࢀ࠰ࠥࡸࡥࡴࡷ࡯ࡸ࠿ࠦࡻࡳࡧࡶࡹࡱࡺࡽࠣᏃ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡨࡼࡪࡩࡵࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡥࡾࠤᏄ").format(e=e))
    def _populate_browser_instance_data(self):
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࡓࡳࡵࡻ࡬ࡢࡶࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࠥࡧ࡮ࡥࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦ࡯࡯ࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࠤ࡫ࡵࡲࠡࡴࡲࡦࡴࡺ࠭ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࠧࠨࠢᏅ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll1l1l11_opy_ import bstack1l1l11ll1l_opy_
            if not self._1l1llllllll_opy_():
                logger.debug(bstack1ll1l11_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦ࡮ࡰࠢࡤࡧࡹ࡯ࡶࡦࠢࡳࡥ࡬࡫ࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠥᏆ"))
                return
            result = self._1ll1111l1l1_opy_(bstack1ll1l11_opy_ (u"ࠩࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸ࠭Ꮗ"), {})
            logger.debug(bstack1ll1l11_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧ࠺ࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠥࡸࡥࡴࡷ࡯ࡸࡂࢁࡲࡾࠤᏈ").format(r=result))
            if not result:
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡱࡳࠥࡸࡥࡴࡷ࡯ࡸࠥ࡬ࡲࡰ࡯ࠣ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢᏉ"))
                return
            bstack1l1llll111l_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1l1llll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᏊ"), bstack1ll1l11_opy_ (u"࠭ࠧᏋ"))
            hub_url = os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡐࡄࡒࡘࡤࡖࡗࡠࡅࡇࡔࡤ࡛ࡒࡍࠩᏌ"), bstack1ll1l11_opy_ (u"ࠨࠩᏍ"))
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࢀࡹࡩࡥࡿ࠯ࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࢁࡵࡳ࡮ࢀࠦᏎ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1ll1l11_opy_ (u"ࠪࠫᏏ")))
            current_test_id = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭Ꮠ"), None)
            for instance in bstack1111lll1ll_opy_.bstack11l111111_opy_.values():
                if not bstack1l1l11ll1l_opy_.bstack1l1lll1ll11_opy_(instance, bstack1l1l11ll1l_opy_.bstack1ll111l111l_opy_, None):
                    bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1l1l11ll1l_opy_.bstack1ll111l111l_opy_, session_id)
                    bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1111llll_opy_, hub_url)
                    if current_test_id:
                        bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭Ꮡ"), current_test_id)
                    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡐࡰࡲࡸࡰࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠿ࠦࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࡿࡸ࡯ࡤࡾ࠮ࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࠤࡸ࡫ࡴ࠭ࠢࡷࡩࡸࡺ࡟ࡪࡦࡀࡿࡹ࡯ࡤࡾࠤᏒ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡴࡶࡵ࡭ࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡦࡤࡸࡦࡀࠠࡼࡧࢀࠦᏓ").format(e=e))
    def _clear_session_data(self):
        bstack1ll1l11_opy_ (u"ࠣࠤࠥࡇࡱ࡫ࡡࡳࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡡ࡭࡮ࠣࡦࡷࡵࡷࡴࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠠࡵࡱࠣࡩࡳࡹࡵࡳࡧࠣࡸࡪࡹࡴࠡ࡫ࡶࡳࡱࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᏔ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll1l1l11_opy_ import bstack1l1l11ll1l_opy_
            bstack1ll1111l11l_opy_ = 0
            for instance in bstack1111lll1ll_opy_.bstack11l111111_opy_.values():
                bstack1ll11111l1l_opy_ = False
                if bstack1l1l11ll1l_opy_.bstack1l1lll1ll11_opy_(instance, bstack1l1l11ll1l_opy_.bstack1ll111l111l_opy_, None):
                    bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1l1l11ll1l_opy_.bstack1ll111l111l_opy_, bstack1ll1l11_opy_ (u"ࠩࠪᏕ"))
                    bstack1ll11111l1l_opy_ = True
                if bstack1l1l11ll1l_opy_.bstack1l1lll1ll11_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1111llll_opy_, None):
                    bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1111llll_opy_, bstack1ll1l11_opy_ (u"ࠪࠫᏖ"))
                    bstack1ll11111l1l_opy_ = True
                if bstack1l1l11ll1l_opy_.bstack1l1lll1ll11_opy_(instance, bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡬ࡨࠬᏗ"), None):
                    bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭Ꮨ"), None)
                    bstack1ll11111l1l_opy_ = True
                if bstack1111lll1ll_opy_.bstack1l1llll1111_opy_(instance, bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠫᏙ")):
                    bstack1111lll1ll_opy_.bstack1ll11l1ll_opy_(instance, bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠬᏚ"), None)
                    bstack1ll11111l1l_opy_ = True
                if bstack1ll11111l1l_opy_:
                    bstack1ll1111l11l_opy_ += 1
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡡࡦࡰࡪࡧࡲࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡧࡥࡹࡧ࠺ࠡࡅ࡯ࡩࡦࡸࡥࡥࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡻ࡯ࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࠨᏛ").format(
                n=bstack1ll1111l11l_opy_))
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡬ࡦࡣࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣ࠽ࠤࢀ࡫ࡽࠣᏜ").format(e=e))
    def _1ll1111l1ll_opy_(self, status, reason=bstack1ll1l11_opy_ (u"ࠥࠦᏝ")):
        bstack1ll1l11_opy_ (u"ࠦࠧࠨࡍࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢࠣࠤᏞ")
        bstack1ll1111l111_opy_ = bstack1ll1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᏟ") if status == bstack1ll1l11_opy_ (u"ࠨࡐࡂࡕࡖࠦᏠ") else bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᏡ")
        if bstack1ll1111l111_opy_ == bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᏢ"):
            return self._1ll1111l1l1_opy_(bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᏣ"), {
                bstack1ll1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᏤ"): bstack1ll1111l111_opy_,
                bstack1ll1l11_opy_ (u"ࠦࡷ࡫ࡡࡴࡱࡱࠦᏥ"): reason
            })
        else:
            return self._1ll1111l1l1_opy_(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᏦ"), {
                bstack1ll1l11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᏧ"): bstack1ll1111l111_opy_
            })
    def _1ll111l11ll_opy_(self, name):
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࡖࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢࠣࠤᏨ")
        return self._1ll1111l1l1_opy_(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᏩ"), {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏪ"): name
        })
    def _1ll11111lll_opy_(self):
        bstack1ll1l11_opy_ (u"ࠥࠦࠧࡓࡡࡳ࡭ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡨࡥࡧࡱࡵࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡣ࡭ࡱࡶࡩࠥࡵࡲࠡࡶࡨࡥࡷࡪ࡯ࡸࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡴࡢࡶࡸࡷࠥ࡯ࡳࠡ࡫ࡱࡪࡪࡸࡲࡦࡦࠣࡪࡷࡵ࡭ࠡࡡ࡯ࡥࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫࠺ࠡ࡫ࡩࠤࡦࡴࡹࠡࡈࡄࡍࡑ࠳࡬ࡦࡸࡨࡰࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼࡧࡳࠡࡥࡤࡴࡹࡻࡲࡦࡦࠣࡨࡺࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡵࡧࡶࡸ࠱ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡ࡫ࡶࠤ࡫ࡧࡩ࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᏫ")
        if self._1l1llll1l11_opy_:
            return
        try:
            global_config = Config.bstack1lllllll1_opy_()
            if self._current_test_name and not global_config.bstack1lll111ll11_opy_():
                self._1ll111l11ll_opy_(self._current_test_name)
            status = bstack1ll1l11_opy_ (u"ࠫࡋࡇࡉࡍࠩᏬ") if self._1ll111l1l11_opy_ else bstack1ll1l11_opy_ (u"ࠬࡖࡁࡔࡕࠪᏭ")
            message = self._1ll111l1l11_opy_ or bstack1ll1l11_opy_ (u"࠭ࠧᏮ")
            if not global_config.bstack1ll1lll1111_opy_():
                logger.debug(bstack1ll1l11_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡦࡰࡴࡹࡥ࠻ࠢࡶࡸࡦࡺࡵࡴ࠿ࡾࡷࡹࡧࡴࡶࡵࢀ࠰ࠥࡳࡥࡴࡵࡤ࡫ࡪࡃࡻ࡮ࡧࡶࡷࡦ࡭ࡥࡾࠤᏯ").format(status=status, message=message))
                self._1ll1111l1ll_opy_(status, message)
            self._1l1llll1l11_opy_ = True
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏰ"))
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡥࡾࠤᏱ").format(e=e))
    def _extract_screenshot_base64(self, bstack1ll11111ll1_opy_):
        bstack1ll1l11_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡊࡗࡑࡑࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡰࡤࡲࡸࠬࡹࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࡯ࡳ࡬ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠥࡧࡳࠡࡊࡗࡑࡑࠦࡷࡪࡶ࡫ࠤࡪ࡯ࡴࡩࡧࡵ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡦࡪࡪࡤࡦࡦ࠽ࠤࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࡥࡣࡷࡥ࠿࡯࡭ࡢࡩࡨ࠳ࡵࡴࡧ࠼ࡤࡤࡷࡪ࠼࠴࠭ࡽࡧࡥࡹࡧࡽࠣࠢ࠱࠲࠳ࡄࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊ࡮ࡲࡥࠡ࡮࡬ࡲࡰࡀࠠ࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࡴࡦࡺࡨ࠰ࡶࡲ࠳࡫࡯࡬ࡦ࠰ࡳࡲ࡬ࠨࠠ࠯࠰࠱ࡂࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᏲ")
        match = re.search(bstack1ll1l11_opy_ (u"ࡶࠬࡹࡲࡤ࠿ࠥࡨࡦࡺࡡ࠻࡫ࡰࡥ࡬࡫࠯ࡱࡰࡪ࠿ࡧࡧࡳࡦ࠸࠷࠰࠭ࡡ࡞ࠣ࡟࠮࠭ࠧ࠭Ᏻ"), bstack1ll11111ll1_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1ll1l11_opy_ (u"ࡷ࠭࠼ࡪ࡯ࡪ࡟ࡣࡄ࡝ࠬࡵࡵࡧࡂࠨࠨ࡜ࡠࠥࡡ࠰ࡢ࠮ࠩࡁ࠽ࡴࡳ࡭ࡼ࡫ࡲࡪࢀ࡯ࡶࡥࡨࠫࠬࠦࠬᏴ"), bstack1ll11111ll1_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1l1llll1lll_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡒࡐࡄࡒࡘࡤࡕࡕࡕࡒࡘࡘࡤࡊࡉࡓࠩᏵ"), os.getcwd())
                    path = Path(bstack1l1llll1lll_opy_) / path
                if path.is_file():
                    with open(path, bstack1ll1l11_opy_ (u"ࠧࡳࡤࠪ᏶")) as f:
                        return base64.b64encode(f.read()).decode(bstack1ll1l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᏷"))
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡸࡥࡢࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡧ࡫࡯ࡩࠥࢁࡰࡢࡶ࡫ࢁ࠿ࠦࡻࡦࡿࠥᏸ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll1111llll_opy_ = False
            self._1l1llll1l11_opy_ = False
            self._current_test_name = name
            self._1ll111l1l11_opy_ = None
            self._1ll111111l1_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ᏹ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1ll1l11_opy_ (u"ࠫ࡮ࡪࠧᏺ"), None)
            self._clear_session_data()
            bstack1lll1lll1ll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lll1lll1ll_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lll1lll1ll_opy_)
            return
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡹ࡫ࡳࡵࠢࡆࡅࡑࡒࡅࡅࠢ࠰ࠤࡹ࡫ࡳࡵ࠼ࠣࡿࡳࡧ࡭ࡦࡿࠥᏻ").format(name=name))
        self._1ll1111llll_opy_ = False
        self._1l1llll1l11_opy_ = False
        self._current_test_name = name
        self._1ll111l1l11_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lll1lll1ll_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1l1lllll1l1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᏼ")),
                message=attrs.get(bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᏽ"), bstack1ll1l11_opy_ (u"ࠨࠩ᏾")),
                starttime=attrs.get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡵ࡫ࡰࡩࠬ᏿"), bstack1ll1l11_opy_ (u"ࠪࠫ᐀")),
                endtime=attrs.get(bstack1ll1l11_opy_ (u"ࠫࡪࡴࡤࡵ࡫ࡰࡩࠬᐁ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᐂ")),
                elapsedtime=attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫᐃ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lll1lll1ll_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lll1lll1ll_opy_, bstack1l1lllll1l1_opy_)
        status = attrs.get(bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᐄ"), bstack1ll1l11_opy_ (u"ࠨࡗࡑࡏࡓࡕࡗࡏࠩᐅ"))
        message = attrs.get(bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᐆ"), bstack1ll1l11_opy_ (u"ࠪࠫᐇ"))
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡪࡴࡤࡠࡶࡨࡷࡹࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡶࡨࡷࡹࡀࠠࡼࡰࡤࡱࡪࢃࠬࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࡷࡹࡧࡴࡶࡵࢀࠦᐈ").format(name=name, status=status))
        self._1ll1111llll_opy_ = True
        if not self._1l1llll1l11_opy_ and self._1l1llllllll_opy_():
            try:
                global_config = Config.bstack1lllllll1_opy_()
                if not global_config.bstack1lll111ll11_opy_():
                    self._1ll111l11ll_opy_(name)
                if not global_config.bstack1ll1lll1111_opy_():
                    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡓࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡰࠣࡩࡳࡪ࡟ࡵࡧࡶࡸ࠿ࠦࡳࡵࡣࡷࡹࡸࡃࡻࡴࡶࡤࡸࡺࡹࡽࠣᐉ").format(status=status))
                    self._1ll1111l1ll_opy_(status, message)
                self._1l1llll1l11_opy_ = True
                logger.debug(bstack1ll1l11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡳࡡࡳ࡭ࡨࡨࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᐊ"))
            except Exception as e:
                logger.error(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡽࡨࢁࠧᐋ").format(e=e))
        elif self._1l1llll1l11_opy_:
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡱࡦࡸ࡫ࡦࡦࠥᐌ"))
        else:
            logger.debug(bstack1ll1l11_opy_ (u"ࠤࡑࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡷࡪࡹࡳࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠧᐍ"))
    def start_suite(self, name, attrs):
        bstack1ll1l11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡻ࡭࡫࡮ࠡࡣࠣࡷࡺ࡯ࡴࡦࠢࡶࡸࡦࡸࡴࡴࠤࠥࠦᐎ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1ll1l11_opy_ (u"ࠫ࡮ࡪࠧᐏ"), None)
            bstack1l1llll11l1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1l1llll11l1_opy_)
            return
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸࡻࡩࡵࡧࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡹࡵࡪࡶࡨ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧᐐ").format(name=name))
    def end_suite(self, name, attrs):
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡷࡩࡧࡱࠤࡦࠦࡳࡶ࡫ࡷࡩࠥ࡫࡮ࡥࡵࠥࠦࠧᐑ")
        if cli.is_running():
            bstack1l1llll11l1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1l1llll11l1_opy_)
            return
        logger.debug(bstack1ll1l11_opy_ (u"ࠢࡦࡰࡧࡣࡸࡻࡩࡵࡧࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡹࡵࡪࡶࡨ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧᐒ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᐓ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫᐔ"), None)
            if attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᐕ"), bstack1ll1l11_opy_ (u"ࠫࠬᐖ")).lower() in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᐗ"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᐘ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᐙ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1l1lll1l1l1_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨᐚ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1l1lll1l1l1_opy_)
            else:
                if current_test_id:
                    bstack1l1lll1l1l1_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩᐛ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1l1lll1l1l1_opy_, test_id=current_test_id)
            try:
                if cli.accessibility and cli.bstack1l1l1ll1ll_opy_:
                    _1ll11111111_opy_ = next(iter(bstack1111lll1ll_opy_.bstack11l111111_opy_.values()), None)
                    if _1ll11111111_opy_ and attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᐜ"), bstack1ll1l11_opy_ (u"ࠫࠬᐝ")).lower() not in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᐞ"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᐟ")]:
                        cli.accessibility.bstack1l1lllll11l_opy_(
                            cli.bstack1l1l1ll1ll_opy_,
                            None,
                            (_1ll11111111_opy_, bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹࡥ࡫ࡦࡻࡺࡳࡷࡪࠧᐠ")),
                            (bstack1l1111l1l1_opy_.bstack1l1llllll11_opy_, bstack1ll111111l_opy_.PRE),
                            None,
                            [name, attrs],
                        )
            except Exception as _e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟࡬ࡧࡼࡻࡴࡸࡤ࠻ࠢࡤ࠵࠶ࡿࠠࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣᐡ").format(e=_e))
        if name.lower() in self._CLOSE_KEYWORDS:
            try:
                if cli.accessibility:
                    cli.accessibility.bstack1ll11111l11_opy_()
            except Exception as _e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠ࡭ࡨࡽࡼࡵࡲࡥ࠼ࠣࡥ࠶࠷ࡹࠡࡵࡷࡳࡵࡥࡣࡢࡲࡷࡹࡷ࡫࡟ࡣࡧࡩࡳࡷ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦᐢ").format(e=_e))
        if self._1l1llll1l11_opy_ or self._1ll1111llll_opy_:
            return
        bstack1l1lllll1ll_opy_ = False
        bstack1l1lll1lll1_opy_ = attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᐣ"), bstack1ll1l11_opy_ (u"ࠫࠬᐤ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1l1lllll1ll_opy_ = True
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡉ࡬ࡰࡵࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࡽࡱࡥࡲ࡫ࡽ࠭ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡮ࡺࠠࡦࡺࡨࡧࡺࡺࡥࡴࠤᐥ").format(name=name))
        elif bstack1l1lll1lll1_opy_ == bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᐦ"):
            bstack1l1lllll1ll_opy_ = True
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪ࠰ࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡵࡧࡤࡶࡩࡵࡷ࡯ࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦᐧ"))
        if bstack1l1lllll1ll_opy_ and self._1l1llllllll_opy_():
            self._populate_browser_instance_data()
            self._1ll11111lll_opy_()
    def end_keyword(self, name, attrs):
        bstack1ll1l11_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡣࡩࡸࡪࡸࠠࡢࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡸ࠴ࠢࠣࠤᐨ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᐩ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬᐪ"), None)
            bstack1l1lll1l1l1_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫᐫ"), name), id=current_test_id, **attrs)
            bstack1l1lllll1l1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᐬ")),
                message=attrs.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᐭ"), bstack1ll1l11_opy_ (u"ࠧࠨᐮ")),
                starttime=attrs.get(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡴࡪ࡯ࡨࠫᐯ"), bstack1ll1l11_opy_ (u"ࠩࠪᐰ")),
                endtime=attrs.get(bstack1ll1l11_opy_ (u"ࠪࡩࡳࡪࡴࡪ࡯ࡨࠫᐱ"), bstack1ll1l11_opy_ (u"ࠫࠬᐲ")),
                elapsedtime=attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪᐳ"), 0)
            )
            if attrs.get(bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᐴ"), bstack1ll1l11_opy_ (u"ࠧࠨᐵ")).lower() in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᐶ"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᐷ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᐸ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1l1lll1l1l1_opy_, bstack1l1lllll1l1_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1l1lll1l1l1_opy_, bstack1l1lllll1l1_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᐹ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᐺ")).upper() == bstack1ll1l11_opy_ (u"࠭ࡐࡂࡕࡖࠫᐻ")):
                logger.debug(bstack1ll1l11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࠡࡱࡳࡩࡳࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦ࠽ࠤࢀࡴࡡ࡮ࡧࢀ࠰ࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡦࡺࡡࠣᐼ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1ll1l11_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡴࡼࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡧࡰࡵࡷࡵࡩࡸࠦࡆࡂࡋࡏࠤࡱ࡫ࡶࡦ࡮ࠣࡱࡪࡹࡳࡢࡩࡨࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡧࡳࠡࡧࡵࡶࡴࡸࠠࡳࡧࡤࡷࡴࡴࠬࠋࠢࠣࠤࠥࠦࠠࠡࠢࡶ࡭ࡳࡩࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡤࡸࡹࡸࡳࠡࡦࡲࡩࡸࡴࠧࡵࠢ࡬ࡲࡨࡲࡵࡥࡧࠣࡸ࡭࡫ࠠࡦࡴࡵࡳࡷࠦ࡭ࡦࡵࡶࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᐽ")
        if cli.is_running():
            try:
                if message.get(bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡲࡲࠧᐾ"), bstack1ll1l11_opy_ (u"ࠪࡲࡴ࠭ᐿ")) == bstack1ll1l11_opy_ (u"ࠫࡾ࡫ࡳࠨᑀ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑁ"), bstack1ll1l11_opy_ (u"࠭ࠧᑂ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1ll1l11_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᑃ"),
                            level=bstack1ll1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᑄ"),
                            timestamp=message.get(bstack1ll1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᑅ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬᑆ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑇ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᑈ")),
                        level=message.get(bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᑉ"), bstack1ll1l11_opy_ (u"ࠧࡊࡐࡉࡓࠬᑊ")),
                        timestamp=message.get(bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᑋ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫᑌ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᑍ"), bstack1ll1l11_opy_ (u"ࠫࠬᑎ"))
        if level == bstack1ll1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪᑏ"):
            self._1ll111l1l11_opy_ = message.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᑐ"), bstack1ll1l11_opy_ (u"ࠧࠨᑑ"))
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡅࡤࡴࡹࡻࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡰࡩࡸࡹࡡࡨࡧ࠽ࠤࢀ࡫ࡲࡳࡱࡵࢁࠧᑒ").format(error=self._1ll111l1l11_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1ll1l11_opy_ (u"ࠤࠥࠦࡉ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡪࡨࠣࡷࡪࡺࡵࡱ࠱ࡷࡩࡦࡸࡤࡰࡹࡱࠤ࡮ࡹࠠࡴࡷ࡬ࡸࡪ࠳࡬ࡦࡸࡨࡰࠥࡵࡲࠡࡶࡨࡷࡹ࠳࡬ࡦࡸࡨࡰ࠳ࠨࠢࠣᑓ")
        if hook_type.lower() == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᑔ"):
            return bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᑕ") if current_test_uuid is None else bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᑖ")
        elif hook_type.lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᑗ"):
            return bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᑘ") if current_test_uuid is None else bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᑙ")