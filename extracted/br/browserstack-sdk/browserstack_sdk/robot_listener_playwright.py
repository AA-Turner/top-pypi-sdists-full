# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11ll111lll_opy_ import bstack1llll1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1lll1l11_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import bstack111lll11l_opy_, bstack111l11ll_opy_, bstack1lll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1l111111ll_opy_ import bstack1l111111ll_opy_, Events, bstack11lll111_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1ll1l1lllll_opy_
    _1ll1lll1l1l_opy_ = bstack1ll1l1lllll_opy_.VERSION
except:
    _1ll1lll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨበ")
cli_context = bstack1ll1lll1l11_opy_(
    test_framework_name=bstack1ll1lll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧቡ"),
    test_framework_version=_1ll1lll1l1l_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1ll1lll_opy_ (u"ࠩࡦࡰࡴࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠩቢ"), bstack1ll1lll_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡦࡳࡳࡺࡥࡹࡶࠪባ"), bstack1ll1lll_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡴࡦ࡭ࡥࠨቤ"),
        bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷ࠭ብ"), bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡣࡰࡰࡷࡩࡽࡺࠧቦ"), bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡱࡣࡪࡩࠬቧ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1ll1lll_opy_ (u"ࠨࡰࡨࡻࠥࡨࡲࡰࡹࡶࡩࡷ࠭ቨ"), bstack1ll1lll_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠣࡸࡴࠦࡢࡳࡱࡺࡷࡪࡸࠧቩ"),
        bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࠡࡤࡵࡳࡼࡹࡥࡳࠩቪ"), bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡯࡯ࡰࡨࡧࡹࠦࡴࡰࠢࡥࡶࡴࡽࡳࡦࡴࠪቫ"),
    }
    def __init__(self):
        self._1ll1l1l1l11_opy_ = None
        self._1ll1l1ll1ll_opy_ = False
        self._1ll1ll1l11l_opy_ = False
        self._current_test_name = None
        self._1ll1l1lll1l_opy_ = None
        self._1ll1l11ll1l_opy_ = False
        if cli.bstack111llllll_opy_():
            try:
                if cli.bstack1ll11ll1_opy_:
                    cli_context.platform_index = cli.bstack1ll11ll1_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬቬ"), bstack1ll1lll_opy_ (u"࠭࠰ࠨቭ")))
            except Exception as e:
                pass
        PlaywrightPatcher._1ll1l1l11l1_opy_()
    @staticmethod
    def _1ll1l1l11l1_opy_():
        try:
            import functools
            from Browser.keywords.bstack1111111l11_opy_ import bstack1ll1ll11111_opy_
            from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1ll1ll11ll1_opy_
            _1ll1lll11l1_opy_ = bstack1ll1ll11111_opy_.close_browser
            _1ll1ll1lll1_opy_ = bstack1ll1ll11111_opy_.bstack1ll1lll1lll_opy_
            @functools.wraps(_1ll1lll11l1_opy_)
            def _1ll1lll1111_opy_(self, browser=bstack1ll1lll_opy_ (u"ࠢࡄࡗࡕࡖࡊࡔࡔࠣቮ")):
                if not bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.is_set():
                    logger.debug(bstack1ll1lll_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡤ࠵࠶ࡿࠠࡴࡥࡤࡲࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵ࠯ࠤࡼࡧࡩࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡶࡲࠤ࠶࠻ࡳࠣቯ"))
                    bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.wait(timeout=15)
                return _1ll1lll11l1_opy_(self, browser)
            @functools.wraps(_1ll1ll1lll1_opy_)
            def _1ll1ll11l11_opy_(self, page=bstack1ll1lll_opy_ (u"ࠤࡆ࡙ࡗࡘࡅࡏࡖࠥተ")):
                if not bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.is_set():
                    logger.debug(bstack1ll1lll_opy_ (u"ࠥࡧࡱࡵࡳࡦࡡࡳࡥ࡬࡫࠺ࠡࡣ࠴࠵ࡾࠦࡳࡤࡣࡱࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴ࠮ࠣࡻࡦ࡯ࡴࡪࡰࡪࠤࡺࡶࠠࡵࡱࠣ࠵࠺ࡹࠢቱ"))
                    bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.wait(timeout=15)
                return _1ll1ll1lll1_opy_(self, page)
            bstack1ll1ll11111_opy_.close_browser = _1ll1lll1111_opy_
            bstack1ll1ll11111_opy_.bstack1ll1lll1lll_opy_ = _1ll1ll11l11_opy_
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡤࡶࡡࡵࡥ࡫ࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡥ࡯ࡳࡸ࡫࡟࡮ࡧࡷ࡬ࡴࡪࡳ࠻ࠢࡳࡥࡹࡩࡨࡦࡦࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡓࡵࡣࡷࡩࠥࡩ࡬ࡰࡵࡨࠤࡲ࡫ࡴࡩࡱࡧࡷࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡨࡣࡷࡩࠧቲ"))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡥࡰࡢࡶࡦ࡬ࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡦࡰࡴࡹࡥࡠ࡯ࡨࡸ࡭ࡵࡤࡴ࠼ࠣࡷࡰ࡯ࡰࡱࡧࡧࠤ࠭ࡈࡲࡰࡹࡶࡩࡷࠦ࡬ࡪࡤࡵࡥࡷࡿࠠ࡯ࡱࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡰࡴࠣࡥ࠶࠷ࡹࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠬ࠾ࠥࢁࡥࡾࠤታ").format(e=e))
    def _1ll1l1ll11l_opy_(self):
        if self._1ll1l1l1l11_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1ll1l1l1l11_opy_ = BuiltIn().get_library_instance(bstack1ll1lll_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࠧቴ"))
            except Exception as e:
                logger.warning(bstack1ll1lll_opy_ (u"ࠢࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠾ࠥࢁࡥࡾࠤት").format(e=e))
        return self._1ll1l1l1l11_opy_
    def _1ll1l1ll1l1_opy_(self):
        try:
            bstack11111111ll_opy_ = self._1ll1l1ll11l_opy_()
            if bstack11111111ll_opy_ and hasattr(bstack11111111ll_opy_, bstack1ll1lll_opy_ (u"ࠨࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡥࡳࡵࡣࡷࡩࠬቶ")):
                bstack1111111l11_opy_ = bstack11111111ll_opy_._playwright_state
                if hasattr(bstack1111111l11_opy_, bstack1ll1lll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥࡤࡸࡦࡲ࡯ࡨࠩቷ")):
                    bstack11111111l1_opy_ = bstack1111111l11_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack11111111l1_opy_ = BuiltIn().run_keyword(bstack1ll1lll_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡌ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࠢࡆࡥࡹࡧ࡬ࡰࡩࠪቸ"))
                for bstack1ll1ll11lll_opy_ in bstack11111111l1_opy_:
                    contexts = bstack1ll1ll11lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸࡸ࠭ቹ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1ll1lll_opy_ (u"ࠬࡶࡡࡨࡧࡶࠫቺ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1ll1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠼ࠣࡿࡪࢃࠢቻ").format(e=e))
            return False
    def _1ll1ll1llll_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1ll1l1l1lll_opy_ = {
                bstack1ll1lll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧቼ"): action,
                bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫች"): arguments
            }
            executor_cmd = bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠬቾ") + json.dumps(bstack1ll1l1l1lll_opy_)
            arg_string = bstack1ll1lll_opy_ (u"ࠥࡥࡷ࡭࠽ࡼࡧࡻࡩࡨࡻࡴࡰࡴࡢࡧࡲࡪࡽࠣቿ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1ll1lll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡋࡶࡢ࡮ࡸࡥࡹ࡫ࠠࡋࡣࡹࡥࡘࡩࡲࡪࡲࡷࠫኀ"),
                None,
                bstack1ll1lll_opy_ (u"ࠬࡥࠠ࠾ࡀࠣࡿࢂ࠭ኁ"),
                arg_string
            )
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡧࡦࡹࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡦࡩࡴࡪࡱࡱࢁ࠱ࠦࡲࡦࡵࡸࡰࡹࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤኂ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡦࡿࠥኃ").format(e=e))
    def _populate_browser_instance_data(self):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࡔࡴࡶࡵ࡭ࡣࡷࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࠦࡡ࡯ࡦࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡰࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࠥ࡬࡯ࡳࠢࡵࡳࡧࡵࡴ࠮ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࠨࠢࠣኄ")
        try:
            from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
            if not self._1ll1l1ll1l1_opy_():
                logger.debug(bstack1ll1lll_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠ࡯ࡱࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦኅ"))
                return
            result = self._1ll1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠪ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠧኆ"), {})
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠦࡲࡦࡵࡸࡰࡹࡃࡻࡳࡿࠥኇ").format(r=result))
            if not result:
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡲࡴࠦࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠣኈ"))
                return
            bstack1ll1l11lll1_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1ll1l11lll1_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ኉"), bstack1ll1lll_opy_ (u"ࠧࠨኊ"))
            hub_url = os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡑࡅࡓ࡙ࡥࡐࡘࡡࡆࡈࡕࡥࡕࡓࡎࠪኋ"), bstack1ll1lll_opy_ (u"ࠩࠪኌ"))
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧ࠺ࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࢁࡳࡪࡦࢀ࠰ࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࡻࡶࡴ࡯ࢁࠧኍ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1ll1lll_opy_ (u"ࠫࠬ኎")))
            current_test_id = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ኏"), None)
            for instance in bstack111lll11l_opy_.bstack111llll1l_opy_.values():
                if not bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(instance, bstack11ll1l1l_opy_.bstack1ll1l1l111l_opy_, None):
                    bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1ll1l1l111l_opy_, session_id)
                    bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1l111ll111_opy_, hub_url)
                    if current_test_id:
                        bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧነ"), current_test_id)
                    logger.debug(bstack1ll1lll_opy_ (u"ࠢࡑࡱࡳࡹࡱࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࢀࡹࡩࡥࡿ࠯ࠤ࡭ࡻࡢࡠࡷࡵࡰࠥࡹࡥࡵ࠮ࠣࡸࡪࡹࡴࡠ࡫ࡧࡁࢀࡺࡩࡥࡿࠥኑ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵࡰࡶ࡮ࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡧࡥࡹࡧ࠺ࠡࡽࡨࢁࠧኒ").format(e=e))
    def _clear_session_data(self):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࡈࡲࡥࡢࡴࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩࡧࡴࡢࠢࡩࡶࡴࡳࠠࡢ࡮࡯ࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠡࡶࡲࠤࡪࡴࡳࡶࡴࡨࠤࡹ࡫ࡳࡵࠢ࡬ࡷࡴࡲࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥና")
        try:
            from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
            bstack1ll1l1l1111_opy_ = 0
            for instance in bstack111lll11l_opy_.bstack111llll1l_opy_.values():
                bstack1ll1l1ll111_opy_ = False
                if bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(instance, bstack11ll1l1l_opy_.bstack1ll1l1l111l_opy_, None):
                    bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1ll1l1l111l_opy_, bstack1ll1lll_opy_ (u"ࠪࠫኔ"))
                    bstack1ll1l1ll111_opy_ = True
                if bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(instance, bstack11ll1l1l_opy_.bstack1l111ll111_opy_, None):
                    bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack1l111ll111_opy_, bstack1ll1lll_opy_ (u"ࠫࠬን"))
                    bstack1ll1l1ll111_opy_ = True
                if bstack11ll1l1l_opy_.bstack1ll1lll11ll_opy_(instance, bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭ኖ"), None):
                    bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧኗ"), None)
                    bstack1ll1l1ll111_opy_ = True
                if bstack111lll11l_opy_.bstack1ll1l1l1ll1_opy_(instance, bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠬኘ")):
                    bstack111lll11l_opy_.bstack1l1l11lll_opy_(instance, bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹ࠭ኙ"), None)
                    bstack1ll1l1ll111_opy_ = True
                if bstack1ll1l1ll111_opy_:
                    bstack1ll1l1l1111_opy_ += 1
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡢࡧࡱ࡫ࡡࡳࡡࡶࡩࡸࡹࡩࡰࡰࡢࡨࡦࡺࡡ࠻ࠢࡆࡰࡪࡧࡲࡦࡦࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩࡧࡴࡢࠢࡩࡶࡴࡳࠠࡼࡰࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠢኚ").format(
                n=bstack1ll1l1l1111_opy_))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣ࡭ࡧࡤࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡢࡶࡤ࠾ࠥࢁࡥࡾࠤኛ").format(e=e))
    def _1ll1ll1l1l1_opy_(self, status, reason=bstack1ll1lll_opy_ (u"ࠦࠧኜ")):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦ࡯࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣࠤࠥኝ")
        bstack1ll1lll111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨኞ") if status == bstack1ll1lll_opy_ (u"ࠢࡑࡃࡖࡗࠧኟ") else bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣአ")
        if bstack1ll1lll111l_opy_ == bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤኡ"):
            return self._1ll1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨኢ"), {
                bstack1ll1lll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦኣ"): bstack1ll1lll111l_opy_,
                bstack1ll1lll_opy_ (u"ࠧࡸࡥࡢࡵࡲࡲࠧኤ"): reason
            })
        else:
            return self._1ll1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤእ"), {
                bstack1ll1lll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢኦ"): bstack1ll1lll111l_opy_
            })
    def _1ll1l1llll1_opy_(self, name):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࡗࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦ࡯࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣࠤࠥኧ")
        return self._1ll1ll1llll_opy_(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥከ"), {
            bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣኩ"): name
        })
    def _1ll1ll111ll_opy_(self):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡍࡢࡴ࡮ࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡢࡦࡨࡲࡶࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡤ࡮ࡲࡷࡪࠦ࡯ࡳࠢࡷࡩࡦࡸࡤࡰࡹࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡵࡣࡷࡹࡸࠦࡩࡴࠢ࡬ࡲ࡫࡫ࡲࡳࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡢࡰࡦࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥ࠻ࠢ࡬ࡪࠥࡧ࡮ࡺࠢࡉࡅࡎࡒ࠭࡭ࡧࡹࡩࡱࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡽࡡࡴࠢࡦࡥࡵࡺࡵࡳࡧࡧࠤࡩࡻࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡶࡨࡷࡹ࠲ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢ࡬ࡷࠥ࡬ࡡࡪ࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦኪ")
        if self._1ll1ll1l11l_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._current_test_name and not global_config.should_skip_session_name():
                self._1ll1l1llll1_opy_(self._current_test_name)
            status = bstack1ll1lll_opy_ (u"ࠬࡌࡁࡊࡎࠪካ") if self._1ll1l1lll1l_opy_ else bstack1ll1lll_opy_ (u"࠭ࡐࡂࡕࡖࠫኬ")
            message = self._1ll1l1lll1l_opy_ or bstack1ll1lll_opy_ (u"ࠧࠨክ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡏࡤࡶࡰ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡧࡱࡵࡳࡦ࠼ࠣࡷࡹࡧࡴࡶࡵࡀࡿࡸࡺࡡࡵࡷࡶࢁ࠱ࠦ࡭ࡦࡵࡶࡥ࡬࡫࠽ࡼ࡯ࡨࡷࡸࡧࡧࡦࡿࠥኮ").format(status=status, message=message))
                self._1ll1ll1l1l1_opy_(status, message)
            self._1ll1ll1l11l_opy_ = True
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣኯ"))
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡦࡿࠥኰ").format(e=e))
    def _extract_screenshot_base64(self, bstack1ll1l1lll11_opy_):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡅࡹࡶࡵࡥࡨࡺࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡩࡧࡴࡢࠢࡩࡶࡴࡳࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡋࡘࡒࡒࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡱࡥࡳࡹ࠭ࡳࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠣࡰࡴ࡭ࡳࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸࠦࡡࡴࠢࡋࡘࡒࡒࠠࡸ࡫ࡷ࡬ࠥ࡫ࡩࡵࡪࡨࡶ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡈࡱࡧ࡫ࡤࡥࡧࡧ࠾ࠥࡂࡩ࡮ࡩࠣࡷࡷࡩ࠽ࠣࡦࡤࡸࡦࡀࡩ࡮ࡣࡪࡩ࠴ࡶ࡮ࡨ࠽ࡥࡥࡸ࡫࠶࠵࠮ࡾࡨࡦࡺࡡࡾࠤࠣ࠲࠳࠴࠾ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋ࡯࡬ࡦࠢ࡯࡭ࡳࡱ࠺ࠡ࠾࡬ࡱ࡬ࠦࡳࡳࡥࡀࠦࡵࡧࡴࡩ࠱ࡷࡳ࠴࡬ࡩ࡭ࡧ࠱ࡴࡳ࡭ࠢࠡ࠰࠱࠲ࡃࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ኱")
        match = re.search(bstack1ll1lll_opy_ (u"ࡷ࠭ࡳࡳࡥࡀࠦࡩࡧࡴࡢ࠼࡬ࡱࡦ࡭ࡥ࠰ࡲࡱ࡫ࡀࡨࡡࡴࡧ࠹࠸࠱࠮࡛࡟ࠤࡠ࠯࠮ࠨࠧኲ"), bstack1ll1l1lll11_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1ll1lll_opy_ (u"ࡸࠧ࠽࡫ࡰ࡫ࡠࡤ࠾࡞࠭ࡶࡶࡨࡃࠢࠩ࡝ࡡࠦࡢ࠱࡜࠯ࠪࡂ࠾ࡵࡴࡧࡽ࡬ࡳ࡫ࢁࡰࡰࡦࡩࠬ࠭ࠧ࠭ኳ"), bstack1ll1l1lll11_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1ll1ll1l111_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡓࡑࡅࡓ࡙ࡥࡏࡖࡖࡓ࡙࡙ࡥࡄࡊࡔࠪኴ"), os.getcwd())
                    path = Path(bstack1ll1ll1l111_opy_) / path
                if path.is_file():
                    with open(path, bstack1ll1lll_opy_ (u"ࠨࡴࡥࠫኵ")) as f:
                        return base64.b64encode(f.read()).decode(bstack1ll1lll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ኶"))
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡲࡦࡣࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡨ࡬ࡰࡪࠦࡻࡱࡣࡷ࡬ࢂࡀࠠࡼࡧࢀࠦ኷").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll1l1ll1ll_opy_ = False
            self._1ll1ll1l11l_opy_ = False
            self._current_test_name = name
            self._1ll1l1lll1l_opy_ = None
            self._1ll1l11ll1l_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧኸ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡯ࡤࠨኹ"), None)
            self._clear_session_data()
            bstack1llll1l111l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1llll1l111l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1llll1l111l_opy_)
            return
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡺࡥࡴࡶ࠽ࠤࢀࡴࡡ࡮ࡧࢀࠦኺ").format(name=name))
        self._1ll1l1ll1ll_opy_ = False
        self._1ll1ll1l11l_opy_ = False
        self._current_test_name = name
        self._1ll1l1lll1l_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1llll1l111l_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1ll1lll1ll1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧኻ")),
                message=attrs.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩኼ"), bstack1ll1lll_opy_ (u"ࠩࠪኽ")),
                starttime=attrs.get(bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡶ࡬ࡱࡪ࠭ኾ"), bstack1ll1lll_opy_ (u"ࠫࠬ኿")),
                endtime=attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡥࡶ࡬ࡱࡪ࠭ዀ"), bstack1ll1lll_opy_ (u"࠭ࠧ዁")),
                elapsedtime=attrs.get(bstack1ll1lll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬዂ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1llll1l111l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1llll1l111l_opy_, bstack1ll1lll1ll1_opy_)
        status = attrs.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨዃ"), bstack1ll1lll_opy_ (u"ࠩࡘࡒࡐࡔࡏࡘࡐࠪዄ"))
        message = attrs.get(bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫዅ"), bstack1ll1lll_opy_ (u"ࠫࠬ዆"))
        logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡫࡮ࡥࡡࡷࡩࡸࡺࠠࡄࡃࡏࡐࡊࡊࠠ࠮ࠢࡷࡩࡸࡺ࠺ࠡࡽࡱࡥࡲ࡫ࡽ࠭ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࡸࡺࡡࡵࡷࡶࢁࠧ዇").format(name=name, status=status))
        self._1ll1l1ll1ll_opy_ = True
        if not self._1ll1ll1l11l_opy_ and self._1ll1l1ll1l1_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1ll1l1llll1_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡍࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡱࠤࡪࡴࡤࡠࡶࡨࡷࡹࡀࠠࡴࡶࡤࡸࡺࡹ࠽ࡼࡵࡷࡥࡹࡻࡳࡾࠤወ").format(status=status))
                    self._1ll1ll1l1l1_opy_(status, message)
                self._1ll1ll1l11l_opy_ = True
                logger.debug(bstack1ll1lll_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨዉ"))
            except Exception as e:
                logger.error(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡳࠦࡥ࡯ࡦࡢࡸࡪࡹࡴ࠻ࠢࡾࡩࢂࠨዊ").format(e=e))
        elif self._1ll1ll1l11l_opy_:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡥࡱࡸࡥࡢࡦࡼࠤࡲࡧࡲ࡬ࡧࡧࠦዋ"))
        else:
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠨዌ"))
    def start_suite(self, name, attrs):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡼ࡮ࡥ࡯ࠢࡤࠤࡸࡻࡩࡵࡧࠣࡷࡹࡧࡲࡵࡵࠥࠦࠧው")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1ll1lll_opy_ (u"ࠬ࡯ࡤࠨዎ"), None)
            bstack1ll1ll1ll1l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1ll1ll1ll1l_opy_)
            return
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡵࡪࡶࡨࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡳࡶ࡫ࡷࡩ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨዏ").format(name=name))
    def end_suite(self, name, attrs):
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡥࡽࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡸࡪࡨࡲࠥࡧࠠࡴࡷ࡬ࡸࡪࠦࡥ࡯ࡦࡶࠦࠧࠨዐ")
        if cli.is_running():
            bstack1ll1ll1ll1l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1ll1ll1ll1l_opy_)
            return
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡧࡱࡨࡤࡹࡵࡪࡶࡨࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡳࡶ࡫ࡷࡩ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨዑ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ዒ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬዓ"), None)
            if attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩዔ"), bstack1ll1lll_opy_ (u"ࠬ࠭ዕ")).lower() in [bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬዖ"), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ዗")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ዘ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1ll1ll11l1l_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1lll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩዙ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1ll1ll11l1l_opy_)
            else:
                if current_test_id:
                    bstack1ll1ll11l1l_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1lll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪዚ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1ll1ll11l1l_opy_, test_id=current_test_id)
            try:
                if cli.accessibility and cli.bstack1ll11ll1_opy_:
                    _1ll1ll1ll11_opy_ = next(iter(bstack111lll11l_opy_.bstack111llll1l_opy_.values()), None)
                    if _1ll1ll1ll11_opy_ and attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩዛ"), bstack1ll1lll_opy_ (u"ࠬ࠭ዜ")).lower() not in [bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬዝ"), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩዞ")]:
                        cli.accessibility.bstack1ll1ll1111l_opy_(
                            cli.bstack1ll11ll1_opy_,
                            None,
                            (_1ll1ll1ll11_opy_, bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺ࡟࡬ࡧࡼࡻࡴࡸࡤࠨዟ")),
                            (bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.PRE),
                            None,
                            [name, attrs],
                        )
            except Exception as _e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠ࡭ࡨࡽࡼࡵࡲࡥ࠼ࠣࡥ࠶࠷ࡹࠡࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤዠ").format(e=_e))
        if name.lower() in self._CLOSE_KEYWORDS:
            try:
                if cli.accessibility:
                    cli.accessibility.bstack1ll1l1l1l1l_opy_()
            except Exception as _e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦ࠽ࠤࡦ࠷࠱ࡺࠢࡶࡸࡴࡶ࡟ࡤࡣࡳࡸࡺࡸࡥࡠࡤࡨࡪࡴࡸࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧዡ").format(e=_e))
        if self._1ll1ll1l11l_opy_ or self._1ll1l1ll1ll_opy_:
            return
        bstack1ll1l1l11ll_opy_ = False
        bstack1ll1l11llll_opy_ = attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩዢ"), bstack1ll1lll_opy_ (u"ࠬ࠭ዣ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1ll1l1l11ll_opy_ = True
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡃ࡭ࡱࡶࡩࠥࡱࡥࡺࡹࡲࡶࡩࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࡾࡲࡦࡳࡥࡾ࠮ࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡯ࡴࠡࡧࡻࡩࡨࡻࡴࡦࡵࠥዤ").format(name=name))
        elif bstack1ll1l11llll_opy_ == bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩዥ"):
            bstack1ll1l1l11ll_opy_ = True
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫࠱ࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡶࡨࡥࡷࡪ࡯ࡸࡰࠣࡩࡽ࡫ࡣࡶࡶࡨࡷࠧዦ"))
        if bstack1ll1l1l11ll_opy_ and self._1ll1l1ll1l1_opy_():
            self._populate_browser_instance_data()
            self._1ll1ll111ll_opy_()
    def end_keyword(self, name, attrs):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡤࡪࡹ࡫ࡲࠡࡣࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡹ࠮ࠣࠤࠥዧ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧየ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ዩ"), None)
            bstack1ll1ll11l1l_opy_ = SimpleNamespace(name=attrs.get(bstack1ll1lll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬዪ"), name), id=current_test_id, **attrs)
            bstack1ll1lll1ll1_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ያ")),
                message=attrs.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨዬ"), bstack1ll1lll_opy_ (u"ࠨࠩይ")),
                starttime=attrs.get(bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡵ࡫ࡰࡩࠬዮ"), bstack1ll1lll_opy_ (u"ࠪࠫዯ")),
                endtime=attrs.get(bstack1ll1lll_opy_ (u"ࠫࡪࡴࡤࡵ࡫ࡰࡩࠬደ"), bstack1ll1lll_opy_ (u"ࠬ࠭ዱ")),
                elapsedtime=attrs.get(bstack1ll1lll_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫዲ"), 0)
            )
            if attrs.get(bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬዳ"), bstack1ll1lll_opy_ (u"ࠨࠩዴ")).lower() in [bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨድ"), bstack1ll1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬዶ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩዷ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1ll1ll11l1l_opy_, bstack1ll1lll1ll1_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1ll1ll11l1l_opy_, bstack1ll1lll1ll1_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬዸ"), bstack1ll1lll_opy_ (u"࠭ࠧዹ")).upper() == bstack1ll1lll_opy_ (u"ࠧࡑࡃࡖࡗࠬዺ")):
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࠢࡲࡴࡪࡴࠠ࡬ࡧࡼࡻࡴࡸࡤࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁ࠱ࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩࡧࡴࡢࠤዻ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡩࡳࡷࠦࡥࡷࡧࡵࡽࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡡࡱࡶࡸࡶࡪࡹࠠࡇࡃࡌࡐࠥࡲࡥࡷࡧ࡯ࠤࡲ࡫ࡳࡴࡣࡪࡩࡸࠦࡴࡰࠢࡸࡷࡪࠦࡡࡴࠢࡨࡶࡷࡵࡲࠡࡴࡨࡥࡸࡵ࡮࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡷ࡮ࡴࡣࡦࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡥࡹࡺࡲࡴࠢࡧࡳࡪࡹ࡮ࠨࡶࠣ࡭ࡳࡩ࡬ࡶࡦࡨࠤࡹ࡮ࡥࠡࡧࡵࡶࡴࡸࠠ࡮ࡧࡶࡷࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨዼ")
        if cli.is_running():
            try:
                if message.get(bstack1ll1lll_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨዽ"), bstack1ll1lll_opy_ (u"ࠫࡳࡵࠧዾ")) == bstack1ll1lll_opy_ (u"ࠬࡿࡥࡴࠩዿ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧጀ"), bstack1ll1lll_opy_ (u"ࠧࠨጁ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1ll1lll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬጂ"),
                            level=bstack1ll1lll_opy_ (u"ࠩࡌࡒࡋࡕࠧጃ"),
                            timestamp=message.get(bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ጄ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ጅ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ጆ"), bstack1ll1lll_opy_ (u"࠭ࠧጇ")),
                        level=message.get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ገ"), bstack1ll1lll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ጉ")),
                        timestamp=message.get(bstack1ll1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬጊ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬጋ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1ll1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪጌ"), bstack1ll1lll_opy_ (u"ࠬ࠭ግ"))
        if level == bstack1ll1lll_opy_ (u"࠭ࡆࡂࡋࡏࠫጎ"):
            self._1ll1l1lll1l_opy_ = message.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨጏ"), bstack1ll1lll_opy_ (u"ࠨࠩጐ"))
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡆࡥࡵࡺࡵࡳࡧࡧࠤࡪࡸࡲࡰࡴࠣࡱࡪࡹࡳࡢࡩࡨ࠾ࠥࢁࡥࡳࡴࡲࡶࢂࠨ጑").format(error=self._1ll1l1lll1l_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࡊࡥࡵࡧࡵࡱ࡮ࡴࡥࠡ࡫ࡩࠤࡸ࡫ࡴࡶࡲ࠲ࡸࡪࡧࡲࡥࡱࡺࡲࠥ࡯ࡳࠡࡵࡸ࡭ࡹ࡫࠭࡭ࡧࡹࡩࡱࠦ࡯ࡳࠢࡷࡩࡸࡺ࠭࡭ࡧࡹࡩࡱ࠴ࠢࠣࠤጒ")
        if hook_type.lower() == bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪጓ"):
            return bstack1ll1lll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩጔ") if current_test_uuid is None else bstack1ll1lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫጕ")
        elif hook_type.lower() == bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ጖"):
            return bstack1ll1lll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ጗") if current_test_uuid is None else bstack1ll1lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ጘ")