# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1llll1l11_opy_ import bstack11l1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1lll11l1_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack1111ll11_opy_ import bstack1111ll11_opy_, Events, bstack1lllll111l_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1lll1111lll_opy_
    _1lll11111ll_opy_ = bstack1lll1111lll_opy_.VERSION
except:
    _1lll11111ll_opy_ = bstack1111l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧስ")
cli_context = bstack1ll1lll11l1_opy_(
    test_framework_name=bstack1111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ሶ"),
    test_framework_version=_1lll11111ll_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1111l_opy_ (u"ࠨࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠨሷ"), bstack1111l_opy_ (u"ࠩࡦࡰࡴࡹࡥࠡࡥࡲࡲࡹ࡫ࡸࡵࠩሸ"), bstack1111l_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡳࡥ࡬࡫ࠧሹ"),
        bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡩ࡬ࡰࡵࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠬሺ"), bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣ࡭ࡱࡶࡩࠥࡩ࡯࡯ࡶࡨࡼࡹ࠭ሻ"), bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡰࡢࡩࡨࠫሼ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1111l_opy_ (u"ࠧ࡯ࡧࡺࠤࡧࡸ࡯ࡸࡵࡨࡶࠬሽ"), bstack1111l_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠢࡷࡳࠥࡨࡲࡰࡹࡶࡩࡷ࠭ሾ"),
        bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࠱ࡲࡪࡽࠠࡣࡴࡲࡻࡸ࡫ࡲࠨሿ"), bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࠲ࡨࡵ࡮࡯ࡧࡦࡸࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࠩቀ"),
    }
    def __init__(self):
        self._1ll1ll1ll1l_opy_ = None
        self._1ll1lll11ll_opy_ = False
        self._1lll1111111_opy_ = False
        self._1lll11l1111_opy_ = None
        self._1lll11l11ll_opy_ = None
        self._1ll1ll1ll11_opy_ = False
        if cli.bstack11l1l111_opy_():
            try:
                if cli.bstack1ll1ll1l11l_opy_:
                    cli_context.platform_index = cli.bstack1ll1ll1l11l_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫቁ"), bstack1111l_opy_ (u"ࠬ࠶ࠧቂ")))
            except Exception as e:
                pass
    def _1lll111l11l_opy_(self):
        if self._1ll1ll1ll1l_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1ll1ll1ll1l_opy_ = BuiltIn().get_library_instance(bstack1111l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࠧቃ"))
            except Exception as e:
                logger.warning(bstack1111l_opy_ (u"ࠢࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣ࡫ࡪࡺࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠾ࠥࢁࡥࡾࠤቄ").format(e=e))
        return self._1ll1ll1ll1l_opy_
    def _1lll111ll11_opy_(self):
        try:
            bstack1lll1111l1l_opy_ = self._1lll111l11l_opy_()
            if bstack1lll1111l1l_opy_ and hasattr(bstack1lll1111l1l_opy_, bstack1111l_opy_ (u"ࠨࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡥࡳࡵࡣࡷࡩࠬቅ")):
                bstack1lll11111l1_opy_ = bstack1lll1111l1l_opy_._playwright_state
                if hasattr(bstack1lll11111l1_opy_, bstack1111l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥࡤࡸࡦࡲ࡯ࡨࠩቆ")):
                    bstack1lll111ll1l_opy_ = bstack1lll11111l1_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lll111ll1l_opy_ = BuiltIn().run_keyword(bstack1111l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡌ࡫ࡴࠡࡄࡵࡳࡼࡹࡥࡳࠢࡆࡥࡹࡧ࡬ࡰࡩࠪቇ"))
                for bstack1ll1lll1l1l_opy_ in bstack1lll111ll1l_opy_:
                    contexts = bstack1ll1lll1l1l_opy_.get(bstack1111l_opy_ (u"ࠫࡨࡵ࡮ࡵࡧࡻࡸࡸ࠭ቈ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1111l_opy_ (u"ࠬࡶࡡࡨࡧࡶࠫ቉"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠼ࠣࡿࡪࢃࠢቊ").format(e=e))
            return False
    def _1lll11l11l1_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1ll1ll1llll_opy_ = {
                bstack1111l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧቋ"): action,
                bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫቌ"): arguments
            }
            executor_cmd = bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠬቍ") + json.dumps(bstack1ll1ll1llll_opy_)
            arg_string = bstack1111l_opy_ (u"ࠥࡥࡷ࡭࠽ࡼࡧࡻࡩࡨࡻࡴࡰࡴࡢࡧࡲࡪࡽࠣ቎").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1111l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶ࠳ࡋࡶࡢ࡮ࡸࡥࡹ࡫ࠠࡋࡣࡹࡥࡘࡩࡲࡪࡲࡷࠫ቏"),
                None,
                bstack1111l_opy_ (u"ࠬࡥࠠ࠾ࡀࠣࡿࢂ࠭ቐ"),
                arg_string
            )
            logger.debug(bstack1111l_opy_ (u"ࠨࡅࡹࡧࡦࡹࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡦࡩࡴࡪࡱࡱࢁ࠱ࠦࡲࡦࡵࡸࡰࡹࡀࠠࡼࡴࡨࡷࡺࡲࡴࡾࠤቑ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡦࡿࠥቒ").format(e=e))
    def _call_driver_init(self):
        bstack1111l_opy_ (u"ࠣࠤࠥࡑࡦࡱࡥࠡࡶ࡫ࡩࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠢࡪࡖࡕࡉࠠࡤࡣ࡯ࡰࠥࡺ࡯ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡸ࡭࡯ࡳࠡࡴࡲࡦࡴࡺ࠭ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡸ࡭࡫ࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡱࡱࡳࡹࡱࡧࡴࡦࡵࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡊࡰࡧࡩࡽࢃ࡟ࡳࡧࡩࡣࢀࡸࡥࡧࡿࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢ࡬ࡲࠥࡺࡨࡦࠢࡥ࡭ࡳࡧࡲࡺࠩࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡢࡶࡤࠤࡸࡺ࡯ࡳࡧ࠯ࠤࡼ࡮ࡩࡤࡪࠣ࡭ࡸࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡨࡲࡶࠥࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠢࡨࡺࡪࡴࡴࡴ࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡵࡸ࡯ࡥࡷࡦࡸࠥࡳ࡯ࡥࡷ࡯ࡩࠥ࡮࡯ࡰ࡭ࡶࠤ࠭ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࠱ࠦ࡬ࡰࡥࡤࡰࠥࡺࡵ࡯ࡰࡨࡰ࠱ࠦࡁࡊࠫ࠯ࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤቓ")
        try:
            from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1llll111_opy_
            from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
            if not cli.bstack1ll1ll1lll1_opy_ or not cli.cli_bin_session_id:
                logger.debug(bstack1111l_opy_ (u"ࠤࡢࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࡤ࡮࡬ࠤࡳࡵࡴࠡࡴࡨࡥࡩࡿࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠥቔ"))
                return None
            instance = next(iter(bstack1ll1llll111_opy_.bstack1ll1lll111l_opy_.values()), None)
            if not instance:
                logger.debug(bstack1111l_opy_ (u"ࠥࡣࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡶࡰࡧࠦቕ"))
                return None
            hub_url = os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡔࡈࡏࡕࡡࡓ࡛ࡤࡉࡄࡑࡡࡘࡖࡑ࠭ቖ"), bstack1111l_opy_ (u"ࠬ࠭቗"))
            req = structs.DriverInitRequest()
            req.bin_session_id = cli.cli_bin_session_id
            req.platform_index = cli_context.platform_index if cli_context.platform_index >= 0 else 0
            req.ref = instance.ref()
            req.user_input_params = json.dumps({bstack1111l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬቘ"): True}).encode(bstack1111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ቙"))
            if hub_url:
                req.hub_url = hub_url
            req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢቚ").format(threading.get_ident(), os.getpid())
            logger.debug(bstack1111l_opy_ (u"ࠤࡢࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡸࡥࡧ࠿ࡾࡶࡪ࡬ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴ࡮ࢃࠢቛ").format(
                ref=instance.ref(), pi=req.platform_index))
            response = cli.bstack1ll1ll1lll1_opy_.DriverInit(req)
            if response and response.success:
                logger.debug(bstack1111l_opy_ (u"ࠥࡣࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠣቜ"))
                if response.capabilities:
                    try:
                        bstack1lll111l1l1_opy_ = json.loads(response.capabilities.decode(bstack1111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥቝ")))
                        if bstack1lll111l1l1_opy_:
                            bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1lll1lll_opy_, bstack1lll111l1l1_opy_)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.debug(bstack1111l_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࢁࡥࡾࠤ቞").format(e=e))
                return response
            else:
                logger.debug(bstack1111l_opy_ (u"ࠨ࡟ࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡁࡋࡧ࡬ࡴࡧࠥ቟"))
                return None
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠢࡠࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡦࡿࠥበ").format(e=e))
            return None
    def _populate_browser_instance_data(self):
        bstack1111l_opy_ (u"ࠣࠤࠥࡔࡴࡶࡵ࡭ࡣࡷࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࠦࡡ࡯ࡦࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡰࠣࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࠥ࡬࡯ࡳࠢࡵࡳࡧࡵࡴ࠮ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࠨࠢࠣቡ")
        try:
            from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1llll111_opy_
            from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
            if not self._1lll111ll11_opy_():
                logger.debug(bstack1111l_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠ࡯ࡱࠣࡥࡨࡺࡩࡷࡧࠣࡴࡦ࡭ࡥ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦቢ"))
                return
            if not self._1ll1ll1ll11_opy_:
                response = self._call_driver_init()
                self._1ll1ll1ll11_opy_ = True
                if response and response.success:
                    logger.debug(bstack1111l_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧ࠺ࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠢባ"))
            result = self._1lll11l11l1_opy_(bstack1111l_opy_ (u"ࠫ࡬࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡧࡷࡥ࡮ࡲࡳࠨቤ"), {})
            logger.debug(bstack1111l_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠠࡳࡧࡶࡹࡱࡺ࠽ࡼࡴࢀࠦብ").format(r=result))
            if not result:
                logger.debug(bstack1111l_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡳࡵࠠࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤቦ"))
                return
            bstack1lll111l1ll_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1lll111l1ll_opy_.get(bstack1111l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪቧ"), bstack1111l_opy_ (u"ࠨࠩቨ"))
            hub_url = os.environ.get(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡒࡆࡔ࡚࡟ࡑ࡙ࡢࡇࡉࡖ࡟ࡖࡔࡏࠫቩ"), bstack1111l_opy_ (u"ࠪࠫቪ"))
            logger.debug(bstack1111l_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࡻࡴ࡫ࡧࢁ࠱ࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࡼࡷࡵࡰࢂࠨቫ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1111l_opy_ (u"ࠬ࠭ቬ")))
            current_test_id = getattr(threading.current_thread(), bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨቭ"), None)
            for instance in bstack1ll1llll111_opy_.bstack1ll1lll111l_opy_.values():
                if not bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1llll1l1_opy_, None):
                    bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1llll1l1_opy_, session_id)
                    bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1lll1111ll1_opy_, hub_url)
                    if current_test_id:
                        bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨቮ"), current_test_id)
                    logger.debug(bstack1111l_opy_ (u"ࠣࡒࡲࡴࡺࡲࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠺ࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࢁࡳࡪࡦࢀ࠰ࠥ࡮ࡵࡣࡡࡸࡶࡱࠦࡳࡦࡶ࠯ࠤࡹ࡫ࡳࡵࡡ࡬ࡨࡂࢁࡴࡪࡦࢀࠦቯ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡨࡦࡺࡡ࠻ࠢࡾࡩࢂࠨተ").format(e=e))
    def _clear_session_data(self):
        bstack1111l_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡣ࡯ࡰࠥࡨࡲࡰࡹࡶࡩࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠢࡷࡳࠥ࡫࡮ࡴࡷࡵࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࡵ࡬ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦቱ")
        try:
            from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1llll111_opy_
            from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
            bstack1ll1ll1l1ll_opy_ = 0
            for instance in bstack1ll1llll111_opy_.bstack1ll1lll111l_opy_.values():
                bstack1lll111llll_opy_ = False
                if bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1llll1l1_opy_, None):
                    bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1ll1llll1l1_opy_, bstack1111l_opy_ (u"ࠫࠬቲ"))
                    bstack1lll111llll_opy_ = True
                if bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll1llllll1_opy_.bstack1lll1111ll1_opy_, None):
                    bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll1llllll1_opy_.bstack1lll1111ll1_opy_, bstack1111l_opy_ (u"ࠬ࠭ታ"))
                    bstack1lll111llll_opy_ = True
                if bstack1ll1llllll1_opy_.bstack1ll1lll1l11_opy_(instance, bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡮ࡪࠧቴ"), None):
                    bstack1ll1llllll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡯ࡤࠨት"), None)
                    bstack1lll111llll_opy_ = True
                if bstack1lll111llll_opy_:
                    bstack1ll1ll1l1ll_opy_ += 1
            logger.debug(bstack1111l_opy_ (u"ࠣࡡࡦࡰࡪࡧࡲࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡧࡥࡹࡧ࠺ࠡࡅ࡯ࡩࡦࡸࡥࡥࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡻ࡯ࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࠨቶ").format(
                n=bstack1ll1ll1l1ll_opy_))
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡬ࡦࡣࡵࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣ࠽ࠤࢀ࡫ࡽࠣቷ").format(e=e))
    def _1ll1ll1l1l1_opy_(self, status, reason=bstack1111l_opy_ (u"ࠥࠦቸ")):
        bstack1111l_opy_ (u"ࠦࠧࠨࡍࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢࠣࠤቹ")
        bstack1lll11l111l_opy_ = bstack1111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧቺ") if status == bstack1111l_opy_ (u"ࠨࡐࡂࡕࡖࠦቻ") else bstack1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢቼ")
        if bstack1lll11l111l_opy_ == bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣች"):
            return self._1lll11l11l1_opy_(bstack1111l_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧቾ"), {
                bstack1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥቿ"): bstack1lll11l111l_opy_,
                bstack1111l_opy_ (u"ࠦࡷ࡫ࡡࡴࡱࡱࠦኀ"): reason
            })
        else:
            return self._1lll11l11l1_opy_(bstack1111l_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣኁ"), {
                bstack1111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨኂ"): bstack1lll11l111l_opy_
            })
    def _1ll1llll11l_opy_(self, name):
        bstack1111l_opy_ (u"ࠢࠣࠤࡖࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢࠣࠤኃ")
        return self._1lll11l11l1_opy_(bstack1111l_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤኄ"), {
            bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢኅ"): name
        })
    def _1lll111lll1_opy_(self):
        bstack1111l_opy_ (u"ࠥࠦࠧࡓࡡࡳ࡭ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡣࡱࡨࠥࡹࡴࡢࡶࡸࡷࠥࡨࡥࡧࡱࡵࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡣ࡭ࡱࡶࡩࠥࡵࡲࠡࡶࡨࡥࡷࡪ࡯ࡸࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡴࡢࡶࡸࡷࠥ࡯ࡳࠡ࡫ࡱࡪࡪࡸࡲࡦࡦࠣࡪࡷࡵ࡭ࠡࡡ࡯ࡥࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫࠺ࠡ࡫ࡩࠤࡦࡴࡹࠡࡈࡄࡍࡑ࠳࡬ࡦࡸࡨࡰࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼࡧࡳࠡࡥࡤࡴࡹࡻࡲࡦࡦࠣࡨࡺࡸࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡵࡧࡶࡸ࠱ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡ࡫ࡶࠤ࡫ࡧࡩ࡭࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥኆ")
        if self._1lll1111111_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._1lll11l1111_opy_ and not global_config.should_skip_session_name():
                self._1ll1llll11l_opy_(self._1lll11l1111_opy_)
            status = bstack1111l_opy_ (u"ࠫࡋࡇࡉࡍࠩኇ") if self._1lll11l11ll_opy_ else bstack1111l_opy_ (u"ࠬࡖࡁࡔࡕࠪኈ")
            message = self._1lll11l11ll_opy_ or bstack1111l_opy_ (u"࠭ࠧ኉")
            if not global_config.should_skip_session_status():
                logger.debug(bstack1111l_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡦࡰࡴࡹࡥ࠻ࠢࡶࡸࡦࡺࡵࡴ࠿ࡾࡷࡹࡧࡴࡶࡵࢀ࠰ࠥࡳࡥࡴࡵࡤ࡫ࡪࡃࡻ࡮ࡧࡶࡷࡦ࡭ࡥࡾࠤኊ").format(status=status, message=message))
                self._1ll1ll1l1l1_opy_(status, message)
            self._1lll1111111_opy_ = True
            logger.debug(bstack1111l_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢኋ"))
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡥࡾࠤኌ").format(e=e))
    def _extract_screenshot_base64(self, bstack1lll1111l11_opy_):
        bstack1111l_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡊࡗࡑࡑࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡰࡤࡲࡸࠬࡹࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࡯ࡳ࡬ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠥࡧࡳࠡࡊࡗࡑࡑࠦࡷࡪࡶ࡫ࠤࡪ࡯ࡴࡩࡧࡵ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡇࡰࡦࡪࡪࡤࡦࡦ࠽ࠤࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࡥࡣࡷࡥ࠿࡯࡭ࡢࡩࡨ࠳ࡵࡴࡧ࠼ࡤࡤࡷࡪ࠼࠴࠭ࡽࡧࡥࡹࡧࡽࠣࠢ࠱࠲࠳ࡄࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊ࡮ࡲࡥࠡ࡮࡬ࡲࡰࡀࠠ࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࡴࡦࡺࡨ࠰ࡶࡲ࠳࡫࡯࡬ࡦ࠰ࡳࡲ࡬ࠨࠠ࠯࠰࠱ࡂࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤኍ")
        match = re.search(bstack1111l_opy_ (u"ࡶࠬࡹࡲࡤ࠿ࠥࡨࡦࡺࡡ࠻࡫ࡰࡥ࡬࡫࠯ࡱࡰࡪ࠿ࡧࡧࡳࡦ࠸࠷࠰࠭ࡡ࡞ࠣ࡟࠮࠭ࠧ࠭኎"), bstack1lll1111l11_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1111l_opy_ (u"ࡷ࠭࠼ࡪ࡯ࡪ࡟ࡣࡄ࡝ࠬࡵࡵࡧࡂࠨࠨ࡜ࡠࠥࡡ࠰ࡢ࠮ࠩࡁ࠽ࡴࡳ࡭ࡼ࡫ࡲࡪࢀ࡯ࡶࡥࡨࠫࠬࠦࠬ኏"), bstack1lll1111l11_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1lll111l111_opy_ = os.environ.get(bstack1111l_opy_ (u"࠭ࡒࡐࡄࡒࡘࡤࡕࡕࡕࡒࡘࡘࡤࡊࡉࡓࠩነ"), os.getcwd())
                    path = Path(bstack1lll111l111_opy_) / path
                if path.is_file():
                    with open(path, bstack1111l_opy_ (u"ࠧࡳࡤࠪኑ")) as f:
                        return base64.b64encode(f.read()).decode(bstack1111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧኒ"))
            except Exception as e:
                logger.debug(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡸࡥࡢࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡧ࡫࡯ࡩࠥࢁࡰࡢࡶ࡫ࢁ࠿ࠦࡻࡦࡿࠥና").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll1lll11ll_opy_ = False
            self._1lll1111111_opy_ = False
            self._1lll11l1111_opy_ = name
            self._1lll11l11ll_opy_ = None
            self._1ll1ll1ll11_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1111l_opy_ (u"ࠪ࡭ࡩ࠭ኔ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1111l_opy_ (u"ࠫ࡮ࡪࠧን"), None)
            self._clear_session_data()
            bstack1lllllllll1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lllllllll1_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lllllllll1_opy_)
            return
        logger.debug(bstack1111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡹ࡫ࡳࡵࠢࡆࡅࡑࡒࡅࡅࠢ࠰ࠤࡹ࡫ࡳࡵ࠼ࠣࡿࡳࡧ࡭ࡦࡿࠥኖ").format(name=name))
        self._1ll1lll11ll_opy_ = False
        self._1lll1111111_opy_ = False
        self._1lll11l1111_opy_ = name
        self._1lll11l11ll_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lllllllll1_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1lll111111l_opy_ = SimpleNamespace(
                status=attrs.get(bstack1111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ኗ")),
                message=attrs.get(bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨኘ"), bstack1111l_opy_ (u"ࠨࠩኙ")),
                starttime=attrs.get(bstack1111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡵ࡫ࡰࡩࠬኚ"), bstack1111l_opy_ (u"ࠪࠫኛ")),
                endtime=attrs.get(bstack1111l_opy_ (u"ࠫࡪࡴࡤࡵ࡫ࡰࡩࠬኜ"), bstack1111l_opy_ (u"ࠬ࠭ኝ")),
                elapsedtime=attrs.get(bstack1111l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫኞ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lllllllll1_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lllllllll1_opy_, bstack1lll111111l_opy_)
        status = attrs.get(bstack1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧኟ"), bstack1111l_opy_ (u"ࠨࡗࡑࡏࡓࡕࡗࡏࠩአ"))
        message = attrs.get(bstack1111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪኡ"), bstack1111l_opy_ (u"ࠪࠫኢ"))
        logger.debug(bstack1111l_opy_ (u"ࠦࡪࡴࡤࡠࡶࡨࡷࡹࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡶࡨࡷࡹࡀࠠࡼࡰࡤࡱࡪࢃࠬࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࡷࡹࡧࡴࡶࡵࢀࠦኣ").format(name=name, status=status))
        self._1ll1lll11ll_opy_ = True
        if not self._1lll1111111_opy_ and self._1lll111ll11_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1ll1llll11l_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack1111l_opy_ (u"ࠧࡓࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡰࠣࡩࡳࡪ࡟ࡵࡧࡶࡸ࠿ࠦࡳࡵࡣࡷࡹࡸࡃࡻࡴࡶࡤࡸࡺࡹࡽࠣኤ").format(status=status))
                    self._1ll1ll1l1l1_opy_(status, message)
                self._1lll1111111_opy_ = True
                logger.debug(bstack1111l_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡳࡡࡳ࡭ࡨࡨࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧእ"))
            except Exception as e:
                logger.error(bstack1111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡽࡨࢁࠧኦ").format(e=e))
        elif self._1lll1111111_opy_:
            logger.debug(bstack1111l_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡱࡦࡸ࡫ࡦࡦࠥኧ"))
        else:
            logger.debug(bstack1111l_opy_ (u"ࠤࡑࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡦࡰࡴࠣࡷࡪࡹࡳࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠧከ"))
    def start_suite(self, name, attrs):
        bstack1111l_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡻ࡭࡫࡮ࠡࡣࠣࡷࡺ࡯ࡴࡦࠢࡶࡸࡦࡸࡴࡴࠤࠥࠦኩ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1111l_opy_ (u"ࠫ࡮ࡪࠧኪ"), None)
            bstack1ll1llll1ll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1ll1llll1ll_opy_)
            return
        logger.debug(bstack1111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸࡻࡩࡵࡧࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡹࡵࡪࡶࡨ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧካ").format(name=name))
    def end_suite(self, name, attrs):
        bstack1111l_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡷࡩࡧࡱࠤࡦࠦࡳࡶ࡫ࡷࡩࠥ࡫࡮ࡥࡵࠥࠦࠧኬ")
        if cli.is_running():
            bstack1ll1llll1ll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1ll1llll1ll_opy_)
            return
        logger.debug(bstack1111l_opy_ (u"ࠢࡦࡰࡧࡣࡸࡻࡩࡵࡧࠣࡇࡆࡒࡌࡆࡆࠣ࠱ࠥࡹࡵࡪࡶࡨ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧክ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬኮ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫኯ"), None)
            if attrs.get(bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨኰ"), bstack1111l_opy_ (u"ࠫࠬ኱")).lower() in [bstack1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫኲ"), bstack1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨኳ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬኴ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1ll1lll1111_opy_ = SimpleNamespace(name=attrs.get(bstack1111l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨኵ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1ll1lll1111_opy_)
            else:
                if current_test_id:
                    bstack1ll1lll1111_opy_ = SimpleNamespace(name=attrs.get(bstack1111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ኶"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1ll1lll1111_opy_, test_id=current_test_id)
        if self._1lll1111111_opy_ or self._1ll1lll11ll_opy_:
            return
        bstack1ll1lllllll_opy_ = False
        bstack1ll1lll1ll1_opy_ = attrs.get(bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ኷"), bstack1111l_opy_ (u"ࠫࠬኸ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1ll1lllllll_opy_ = True
            logger.debug(bstack1111l_opy_ (u"ࠧࡉ࡬ࡰࡵࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࡽࡱࡥࡲ࡫ࡽ࠭ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡮ࡺࠠࡦࡺࡨࡧࡺࡺࡥࡴࠤኹ").format(name=name))
        elif bstack1ll1lll1ll1_opy_ == bstack1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨኺ"):
            bstack1ll1lllllll_opy_ = True
            logger.debug(bstack1111l_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪ࠰ࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡵࡧࡤࡶࡩࡵࡷ࡯ࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦኻ"))
        if bstack1ll1lllllll_opy_ and self._1lll111ll11_opy_():
            self._populate_browser_instance_data()
            self._1lll111lll1_opy_()
    def end_keyword(self, name, attrs):
        bstack1111l_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡣࡩࡸࡪࡸࠠࡢࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡸ࠴ࠢࠣࠤኼ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ኽ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬኾ"), None)
            bstack1ll1lll1111_opy_ = SimpleNamespace(name=attrs.get(bstack1111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ኿"), name), id=current_test_id, **attrs)
            bstack1lll111111l_opy_ = SimpleNamespace(
                status=attrs.get(bstack1111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬዀ")),
                message=attrs.get(bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ዁"), bstack1111l_opy_ (u"ࠧࠨዂ")),
                starttime=attrs.get(bstack1111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡴࡪ࡯ࡨࠫዃ"), bstack1111l_opy_ (u"ࠩࠪዄ")),
                endtime=attrs.get(bstack1111l_opy_ (u"ࠪࡩࡳࡪࡴࡪ࡯ࡨࠫዅ"), bstack1111l_opy_ (u"ࠫࠬ዆")),
                elapsedtime=attrs.get(bstack1111l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪ዇"), 0)
            )
            if attrs.get(bstack1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫወ"), bstack1111l_opy_ (u"ࠧࠨዉ")).lower() in [bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧዊ"), bstack1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫዋ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨዌ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1ll1lll1111_opy_, bstack1lll111111l_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1ll1lll1111_opy_, bstack1lll111111l_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫው"), bstack1111l_opy_ (u"ࠬ࠭ዎ")).upper() == bstack1111l_opy_ (u"࠭ࡐࡂࡕࡖࠫዏ")):
                logger.debug(bstack1111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࠡࡱࡳࡩࡳࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦ࠽ࠤࢀࡴࡡ࡮ࡧࢀ࠰ࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡦࡺࡡࠣዐ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1111l_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡴࡼࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡧࡰࡵࡷࡵࡩࡸࠦࡆࡂࡋࡏࠤࡱ࡫ࡶࡦ࡮ࠣࡱࡪࡹࡳࡢࡩࡨࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡧࡳࠡࡧࡵࡶࡴࡸࠠࡳࡧࡤࡷࡴࡴࠬࠋࠢࠣࠤࠥࠦࠠࠡࠢࡶ࡭ࡳࡩࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡤࡸࡹࡸࡳࠡࡦࡲࡩࡸࡴࠧࡵࠢ࡬ࡲࡨࡲࡵࡥࡧࠣࡸ࡭࡫ࠠࡦࡴࡵࡳࡷࠦ࡭ࡦࡵࡶࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧዑ")
        if cli.is_running():
            try:
                if message.get(bstack1111l_opy_ (u"ࠩ࡫ࡸࡲࡲࠧዒ"), bstack1111l_opy_ (u"ࠪࡲࡴ࠭ዓ")) == bstack1111l_opy_ (u"ࠫࡾ࡫ࡳࠨዔ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ዕ"), bstack1111l_opy_ (u"࠭ࠧዖ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1111l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ዗"),
                            level=bstack1111l_opy_ (u"ࠨࡋࡑࡊࡔ࠭ዘ"),
                            timestamp=message.get(bstack1111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬዙ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬዚ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬዛ"), bstack1111l_opy_ (u"ࠬ࠭ዜ")),
                        level=message.get(bstack1111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬዝ"), bstack1111l_opy_ (u"ࠧࡊࡐࡉࡓࠬዞ")),
                        timestamp=message.get(bstack1111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫዟ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫዠ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩዡ"), bstack1111l_opy_ (u"ࠫࠬዢ"))
        if level == bstack1111l_opy_ (u"ࠬࡌࡁࡊࡎࠪዣ"):
            self._1lll11l11ll_opy_ = message.get(bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧዤ"), bstack1111l_opy_ (u"ࠧࠨዥ"))
            logger.debug(bstack1111l_opy_ (u"ࠣࡅࡤࡴࡹࡻࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡰࡩࡸࡹࡡࡨࡧ࠽ࠤࢀ࡫ࡲࡳࡱࡵࢁࠧዦ").format(error=self._1lll11l11ll_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1111l_opy_ (u"ࠤࠥࠦࡉ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡪࡨࠣࡷࡪࡺࡵࡱ࠱ࡷࡩࡦࡸࡤࡰࡹࡱࠤ࡮ࡹࠠࡴࡷ࡬ࡸࡪ࠳࡬ࡦࡸࡨࡰࠥࡵࡲࠡࡶࡨࡷࡹ࠳࡬ࡦࡸࡨࡰ࠳ࠨࠢࠣዧ")
        if hook_type.lower() == bstack1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩየ"):
            return bstack1111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨዩ") if current_test_uuid is None else bstack1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪዪ")
        elif hook_type.lower() == bstack1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨያ"):
            return bstack1111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪዬ") if current_test_uuid is None else bstack1111l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬይ")