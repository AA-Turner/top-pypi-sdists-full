# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1l111_opy_ import bstack11111lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll1l1l1ll_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack11l1lllll1_opy_ import bstack11l1lllll1_opy_, bstack1llll11l1_opy_, bstack11ll111l1_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1lll11l1lll_opy_
    _1lll1111l1l_opy_ = bstack1lll11l1lll_opy_.VERSION
except:
    _1lll1111l1l_opy_ = bstack1111_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪᆗ")
cli_context = bstack1lll1l1l1ll_opy_(
    test_framework_name=bstack1111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩᆘ"),
    test_framework_version=_1lll1111l1l_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1111_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵࠫᆙ"), bstack1111_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡨࡵ࡮ࡵࡧࡻࡸࠬᆚ"), bstack1111_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠥࡶࡡࡨࡧࠪᆛ"),
        bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᆜ"), bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡥࡲࡲࡹ࡫ࡸࡵࠩᆝ"), bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࠱ࡧࡱࡵࡳࡦࠢࡳࡥ࡬࡫ࠧᆞ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1111_opy_ (u"ࠪࡲࡪࡽࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᆟ"), bstack1111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠥࡺ࡯ࠡࡤࡵࡳࡼࡹࡥࡳࠩᆠ"),
        bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴࡮ࡦࡹࠣࡦࡷࡵࡷࡴࡧࡵࠫᆡ"), bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤࡱࡱࡲࡪࡩࡴࠡࡶࡲࠤࡧࡸ࡯ࡸࡵࡨࡶࠬᆢ"),
    }
    def __init__(self):
        self._1lll11111ll_opy_ = None
        self._1lll1l1l111_opy_ = False
        self._1lll1l11l11_opy_ = False
        self._1lll11ll11l_opy_ = None
        self._1lll11ll111_opy_ = None
        self._1lll11ll1ll_opy_ = False
        if cli.bstack1lll1l1lll_opy_():
            try:
                if cli.bstack1lll11lllll_opy_:
                    cli_context.platform_index = cli.bstack1lll11lllll_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᆣ"), bstack1111_opy_ (u"ࠨ࠲ࠪᆤ")))
            except Exception as e:
                pass
    def _1lll1l1l11l_opy_(self):
        if self._1lll11111ll_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1lll11111ll_opy_ = BuiltIn().get_library_instance(bstack1111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࠪᆥ"))
            except Exception as e:
                logger.warning(bstack1111_opy_ (u"ࠥࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡧࡦࡶࠣࡆࡷࡵࡷࡴࡧࡵࠤࡱ࡯ࡢࡳࡣࡵࡽࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠺ࠡࡽࡨࢁࠧᆦ").format(e=e))
        return self._1lll11111ll_opy_
    def _1lll111llll_opy_(self):
        try:
            bstack1lll11l1l1l_opy_ = self._1lll1l1l11l_opy_()
            if bstack1lll11l1l1l_opy_ and hasattr(bstack1lll11l1l1l_opy_, bstack1111_opy_ (u"ࠫࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡡࡶࡸࡦࡺࡥࠨᆧ")):
                bstack1lll1l1111l_opy_ = bstack1lll11l1l1l_opy_._playwright_state
                if hasattr(bstack1lll1l1111l_opy_, bstack1111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡧࡴࡢ࡮ࡲ࡫ࠬᆨ")):
                    bstack1lll11111l1_opy_ = bstack1lll1l1111l_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lll11111l1_opy_ = BuiltIn().run_keyword(bstack1111_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸ࠮ࡈࡧࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡉࡡࡵࡣ࡯ࡳ࡬࠭ᆩ"))
                for bstack1lll11ll1l1_opy_ in bstack1lll11111l1_opy_:
                    contexts = bstack1lll11ll1l1_opy_.get(bstack1111_opy_ (u"ࠧࡤࡱࡱࡸࡪࡾࡴࡴࠩᆪ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1111_opy_ (u"ࠨࡲࡤ࡫ࡪࡹࠧᆫ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩ࠿ࠦࡻࡦࡿࠥᆬ").format(e=e))
            return False
    def _1lll111l1ll_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1lll1l11lll_opy_ = {
                bstack1111_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᆭ"): action,
                bstack1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᆮ"): arguments
            }
            executor_cmd = bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠨᆯ") + json.dumps(bstack1lll1l11lll_opy_)
            arg_string = bstack1111_opy_ (u"ࠨࡡࡳࡩࡀࡿࡪࡾࡥࡤࡷࡷࡳࡷࡥࡣ࡮ࡦࢀࠦᆰ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1111_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡇࡹࡥࡱࡻࡡࡵࡧࠣࡎࡦࡼࡡࡔࡥࡵ࡭ࡵࡺࠧᆱ"),
                None,
                bstack1111_opy_ (u"ࠨࡡࠣࡁࡃࠦࡻࡾࠩᆲ"),
                arg_string
            )
            logger.debug(bstack1111_opy_ (u"ࠤࡈࡼࡪࡩࡵࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡢࡥࡷ࡭ࡴࡴࡽ࠭ࠢࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡿࡷ࡫ࡳࡶ࡮ࡷࢁࠧᆳ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡩࢂࠨᆴ").format(e=e))
    def _call_driver_init(self):
        bstack1111_opy_ (u"ࠦࠧࠨࡍࡢ࡭ࡨࠤࡹ࡮ࡥࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬ࠡࡶࡲࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡴࡩ࡫ࡶࠤࡷࡵࡢࡰࡶ࠰ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡴࡩࡧࠣࡦ࡮ࡴࡡࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡴࡴࡶࡵ࡭ࡣࡷࡩࡸࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡽࡳࡰࡦࡺࡦࡰࡴࡰࡍࡳࡪࡥࡹࡿࡢࡶࡪ࡬࡟ࡼࡴࡨࡪࢂࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠬࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡧࡥࡹࡧࠠࡴࡶࡲࡶࡪ࠲ࠠࡸࡪ࡬ࡧ࡭ࠦࡩࡴࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡱࡴࡲࡨࡺࡩࡴࠡ࡯ࡲࡨࡺࡲࡥࠡࡪࡲࡳࡰࡹࠠࠩࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠭ࠢ࡯ࡳࡨࡧ࡬ࠡࡶࡸࡲࡳ࡫࡬࠭ࠢࡄࡍ࠮࠲ࠠࡢࡰࡧࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᆵ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1lll11l1ll1_opy_
            from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
            if not cli.bstack1lll111l111_opy_ or not cli.cli_bin_session_id:
                logger.debug(bstack1111_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨᆶ"))
                return None
            instance = next(iter(bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.values()), None)
            if not instance:
                logger.debug(bstack1111_opy_ (u"ࠨ࡟ࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠢᆷ"))
                return None
            hub_url = os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡐࡄࡒࡘࡤࡖࡗࡠࡅࡇࡔࡤ࡛ࡒࡍࠩᆸ"), bstack1111_opy_ (u"ࠨࠩᆹ"))
            req = structs.DriverInitRequest()
            req.bin_session_id = cli.cli_bin_session_id
            req.platform_index = cli_context.platform_index if cli_context.platform_index >= 0 else 0
            req.ref = instance.ref()
            req.user_input_params = json.dumps({bstack1111_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᆺ"): True}).encode(bstack1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᆻ"))
            if hub_url:
                req.hub_url = hub_url
            req.client_worker_id = bstack1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᆼ").format(threading.get_ident(), os.getpid())
            logger.debug(bstack1111_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡷࡪࡴࡤࡪࡰࡪࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡪࡂࢁࡲࡦࡨࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰࡪࡿࠥᆽ").format(
                ref=instance.ref(), pi=req.platform_index))
            response = cli.bstack1lll111l111_opy_.DriverInit(req)
            if response and response.success:
                logger.debug(bstack1111_opy_ (u"ࠨ࡟ࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠦᆾ"))
                if response.capabilities:
                    try:
                        bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᆿ")))
                        if bstack1lll1111ll1_opy_:
                            bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1111l11_opy_, bstack1lll1111ll1_opy_)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.debug(bstack1111_opy_ (u"ࠣࡡࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࡽࡨࢁࠧᇀ").format(e=e))
                return response
            else:
                logger.debug(bstack1111_opy_ (u"ࠤࡢࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡷ࡫ࡴࡶࡴࡱࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࡇࡣ࡯ࡷࡪࠨᇁ"))
                return None
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠥࡣࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࡩࢂࠨᇂ").format(e=e))
            return None
    def _populate_browser_instance_data(self):
        bstack1111_opy_ (u"ࠦࠧࠨࡐࡰࡲࡸࡰࡦࡺࡥࠡࡪࡸࡦࡤࡻࡲ࡭ࠢࡤࡲࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡳࡳࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠡࡨࡲࡶࠥࡸ࡯ࡣࡱࡷ࠱ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠯ࠤࠥࠦᇃ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1lll11l1ll1_opy_
            from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
            if not self._1lll111llll_opy_():
                logger.debug(bstack1111_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡲࡴࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠢᇄ"))
                return
            if not self._1lll11ll1ll_opy_:
                response = self._call_driver_init()
                self._1lll11ll1ll_opy_ = True
                if response and response.success:
                    logger.debug(bstack1111_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠥᇅ"))
            result = self._1lll111l1ll_opy_(bstack1111_opy_ (u"ࠧࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠫᇆ"), {})
            logger.debug(bstack1111_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠣࡶࡪࡹࡵ࡭ࡶࡀࡿࡷࢃࠢᇇ").format(r=result))
            if not result:
                logger.debug(bstack1111_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠ࡯ࡱࠣࡶࡪࡹࡵ࡭ࡶࠣࡪࡷࡵ࡭ࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠧᇈ"))
                return
            bstack1lll11llll1_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1lll11llll1_opy_.get(bstack1111_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᇉ"), bstack1111_opy_ (u"ࠫࠬᇊ"))
            hub_url = os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡕࡂࡐࡖࡢࡔ࡜ࡥࡃࡅࡒࡢ࡙ࡗࡒࠧᇋ"), bstack1111_opy_ (u"࠭ࠧᇌ"))
            logger.debug(bstack1111_opy_ (u"ࠢࡠࡲࡲࡴࡺࡲࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡤࡢࡶࡤ࠾ࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࡾࡷ࡮ࡪࡽ࠭ࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࡿࡺࡸ࡬ࡾࠤᇍ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1111_opy_ (u"ࠨࠩᇎ")))
            current_test_id = getattr(threading.current_thread(), bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫᇏ"), None)
            for instance in bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.values():
                if not bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1l1l1l1_opy_, None):
                    bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1l1l1l1_opy_, session_id)
                    bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll11lll1l_opy_, hub_url)
                    if current_test_id:
                        bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠ࡫ࡧࠫᇐ"), current_test_id)
                    logger.debug(bstack1111_opy_ (u"ࠦࡕࡵࡰࡶ࡮ࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࡽࡶ࡭ࡩࢃࠬࠡࡪࡸࡦࡤࡻࡲ࡭ࠢࡶࡩࡹ࠲ࠠࡵࡧࡶࡸࡤ࡯ࡤ࠾ࡽࡷ࡭ࡩࢃࠢᇑ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡴࡺࡲࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡤࡢࡶࡤ࠾ࠥࢁࡥࡾࠤᇒ").format(e=e))
    def _clear_session_data(self):
        bstack1111_opy_ (u"ࠨࠢࠣࡅ࡯ࡩࡦࡸࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡳࡱࡰࠤࡦࡲ࡬ࠡࡤࡵࡳࡼࡹࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࠥࡺ࡯ࠡࡧࡱࡷࡺࡸࡥࠡࡶࡨࡷࡹࠦࡩࡴࡱ࡯ࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᇓ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1lll11l1ll1_opy_
            from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
            bstack1lll11l11l1_opy_ = 0
            for instance in bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.values():
                bstack1lll1l111l1_opy_ = False
                if bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1l1l1l1_opy_, None):
                    bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll1l1l1l1_opy_, bstack1111_opy_ (u"ࠧࠨᇔ"))
                    bstack1lll1l111l1_opy_ = True
                if bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll11lll1l_opy_, None):
                    bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1lll11lll1l_opy_, bstack1111_opy_ (u"ࠨࠩᇕ"))
                    bstack1lll1l111l1_opy_ = True
                if bstack1lll11l11ll_opy_.bstack1lll1l11111_opy_(instance, bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪᇖ"), None):
                    bstack1lll11l11ll_opy_.bstack1lll1l11l1l_opy_(instance, bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠ࡫ࡧࠫᇗ"), None)
                    bstack1lll1l111l1_opy_ = True
                if bstack1lll1l111l1_opy_:
                    bstack1lll11l11l1_opy_ += 1
            logger.debug(bstack1111_opy_ (u"ࠦࡤࡩ࡬ࡦࡣࡵࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡪࡡࡵࡣ࠽ࠤࡈࡲࡥࡢࡴࡨࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮ࠢࡾࡲࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠤᇘ").format(
                n=bstack1lll11l11l1_opy_))
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡯ࡩࡦࡸࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡤࡸࡦࡀࠠࡼࡧࢀࠦᇙ").format(e=e))
    def _1lll1l111ll_opy_(self, status, reason=bstack1111_opy_ (u"ࠨࠢᇚ")):
        bstack1111_opy_ (u"ࠢࠣࠤࡐࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥࠦࠧᇛ")
        bstack1lll1l11ll1_opy_ = bstack1111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᇜ") if status == bstack1111_opy_ (u"ࠤࡓࡅࡘ࡙ࠢᇝ") else bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᇞ")
        if bstack1lll1l11ll1_opy_ == bstack1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᇟ"):
            return self._1lll111l1ll_opy_(bstack1111_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᇠ"), {
                bstack1111_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᇡ"): bstack1lll1l11ll1_opy_,
                bstack1111_opy_ (u"ࠢࡳࡧࡤࡷࡴࡴࠢᇢ"): reason
            })
        else:
            return self._1lll111l1ll_opy_(bstack1111_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᇣ"), {
                bstack1111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᇤ"): bstack1lll1l11ll1_opy_
            })
    def _1lll11l111l_opy_(self, name):
        bstack1111_opy_ (u"࡙ࠥࠦࠧࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥࠦࠧᇥ")
        return self._1lll111l1ll_opy_(bstack1111_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᇦ"), {
            bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇧ"): name
        })
    def _1lll11l1l11_opy_(self):
        bstack1111_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡤࡨࡪࡴࡸࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡦࡰࡴࡹࡥࠡࡱࡵࠤࡹ࡫ࡡࡳࡦࡲࡻࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡷࡥࡹࡻࡳࠡ࡫ࡶࠤ࡮ࡴࡦࡦࡴࡵࡩࡩࠦࡦࡳࡱࡰࠤࡤࡲࡡࡴࡶࡢࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧ࠽ࠤ࡮࡬ࠠࡢࡰࡼࠤࡋࡇࡉࡍ࠯࡯ࡩࡻ࡫࡬ࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡣࡶࠤࡨࡧࡰࡵࡷࡵࡩࡩࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡸࡪࡹࡴ࠭ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡮ࡹࠠࡧࡣ࡬ࡰ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᇨ")
        if self._1lll1l11l11_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._1lll11ll11l_opy_ and not global_config.should_skip_session_name():
                self._1lll11l111l_opy_(self._1lll11ll11l_opy_)
            status = bstack1111_opy_ (u"ࠧࡇࡃࡌࡐࠬᇩ") if self._1lll11ll111_opy_ else bstack1111_opy_ (u"ࠨࡒࡄࡗࡘ࠭ᇪ")
            message = self._1lll11ll111_opy_ or bstack1111_opy_ (u"ࠩࠪᇫ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack1111_opy_ (u"ࠥࡑࡦࡸ࡫ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡨࡥࡧࡱࡵࡩࠥࡩ࡬ࡰࡵࡨ࠾ࠥࡹࡴࡢࡶࡸࡷࡂࢁࡳࡵࡣࡷࡹࡸࢃࠬࠡ࡯ࡨࡷࡸࡧࡧࡦ࠿ࡾࡱࡪࡹࡳࡢࡩࡨࢁࠧᇬ").format(status=status, message=message))
                self._1lll1l111ll_opy_(status, message)
            self._1lll1l11l11_opy_ = True
            logger.debug(bstack1111_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡱࡦࡸ࡫ࡦࡦࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠥᇭ"))
        except Exception as e:
            logger.error(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࡨࢁࠧᇮ").format(e=e))
    def _extract_screenshot_base64(self, bstack1lll11l1111_opy_):
        bstack1111_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡍ࡚ࡍࡍࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡳࡧࡵࡴࠨࡵࠣࡆࡷࡵࡷࡴࡧࡵࠤࡱ࡯ࡢࡳࡣࡵࡽࠥࡲ࡯ࡨࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠡࡣࡶࠤࡍ࡚ࡍࡍࠢࡺ࡭ࡹ࡮ࠠࡦ࡫ࡷ࡬ࡪࡸ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡊࡳࡢࡦࡦࡧࡩࡩࡀࠠ࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࡨࡦࡺࡡ࠻࡫ࡰࡥ࡬࡫࠯ࡱࡰࡪ࠿ࡧࡧࡳࡦ࠸࠷࠰ࢀࡪࡡࡵࡣࢀࠦࠥ࠴࠮࠯ࡀࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡪ࡮ࡨࠤࡱ࡯࡮࡬࠼ࠣࡀ࡮ࡳࡧࠡࡵࡵࡧࡂࠨࡰࡢࡶ࡫࠳ࡹࡵ࠯ࡧ࡫࡯ࡩ࠳ࡶ࡮ࡨࠤࠣ࠲࠳࠴࠾ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᇯ")
        match = re.search(bstack1111_opy_ (u"ࡲࠨࡵࡵࡧࡂࠨࡤࡢࡶࡤ࠾࡮ࡳࡡࡨࡧ࠲ࡴࡳ࡭࠻ࡣࡣࡶࡩ࠻࠺ࠬࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩᇰ"), bstack1lll11l1111_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1111_opy_ (u"ࡳࠩ࠿࡭ࡲ࡭࡛࡟ࡀࡠ࠯ࡸࡸࡣ࠾ࠤࠫ࡟ࡣࠨ࡝ࠬ࡞࠱ࠬࡄࡀࡰ࡯ࡩࡿ࡮ࡵ࡭ࡼ࡫ࡲࡨ࡫࠮࠯ࠢࠨᇱ"), bstack1lll11l1111_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1lll111ll11_opy_ = os.environ.get(bstack1111_opy_ (u"ࠩࡕࡓࡇࡕࡔࡠࡑࡘࡘࡕ࡛ࡔࡠࡆࡌࡖࠬᇲ"), os.getcwd())
                    path = Path(bstack1lll111ll11_opy_) / path
                if path.is_file():
                    with open(path, bstack1111_opy_ (u"ࠪࡶࡧ࠭ᇳ")) as f:
                        return base64.b64encode(f.read()).decode(bstack1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᇴ"))
            except Exception as e:
                logger.debug(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡴࡨࡥࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡪ࡮ࡲࡥࠡࡽࡳࡥࡹ࡮ࡽ࠻ࠢࡾࡩࢂࠨᇵ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1lll1l1l111_opy_ = False
            self._1lll1l11l11_opy_ = False
            self._1lll11ll11l_opy_ = name
            self._1lll11ll111_opy_ = None
            self._1lll11ll1ll_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1111_opy_ (u"࠭ࡩࡥࠩᇶ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1111_opy_ (u"ࠧࡪࡦࠪᇷ"), None)
            self._clear_session_data()
            bstack1lllllllll1_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lllllllll1_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lllllllll1_opy_)
            return
        logger.debug(bstack1111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡵࡧࡶࡸࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡵࡧࡶࡸ࠿ࠦࡻ࡯ࡣࡰࡩࢂࠨᇸ").format(name=name))
        self._1lll1l1l111_opy_ = False
        self._1lll1l11l11_opy_ = False
        self._1lll11ll11l_opy_ = name
        self._1lll11ll111_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lllllllll1_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1lll11lll11_opy_ = SimpleNamespace(
                status=attrs.get(bstack1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᇹ")),
                message=attrs.get(bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇺ"), bstack1111_opy_ (u"ࠫࠬᇻ")),
                starttime=attrs.get(bstack1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡸ࡮ࡳࡥࠨᇼ"), bstack1111_opy_ (u"࠭ࠧᇽ")),
                endtime=attrs.get(bstack1111_opy_ (u"ࠧࡦࡰࡧࡸ࡮ࡳࡥࠨᇾ"), bstack1111_opy_ (u"ࠨࠩᇿ")),
                elapsedtime=attrs.get(bstack1111_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧሀ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lllllllll1_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lllllllll1_opy_, bstack1lll11lll11_opy_)
        status = attrs.get(bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪሁ"), bstack1111_opy_ (u"࡚ࠫࡔࡋࡏࡑ࡚ࡒࠬሂ"))
        message = attrs.get(bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ሃ"), bstack1111_opy_ (u"࠭ࠧሄ"))
        logger.debug(bstack1111_opy_ (u"ࠢࡦࡰࡧࡣࡹ࡫ࡳࡵࠢࡆࡅࡑࡒࡅࡅࠢ࠰ࠤࡹ࡫ࡳࡵ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡳࡵࡣࡷࡹࡸࢃࠢህ").format(name=name, status=status))
        self._1lll1l1l111_opy_ = True
        if not self._1lll1l11l11_opy_ and self._1lll111llll_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1lll11l111l_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack1111_opy_ (u"ࠣࡏࡤࡶࡰ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡳࠦࡥ࡯ࡦࡢࡸࡪࡹࡴ࠻ࠢࡶࡸࡦࡺࡵࡴ࠿ࡾࡷࡹࡧࡴࡶࡵࢀࠦሆ").format(status=status))
                    self._1lll1l111ll_opy_(status, message)
                self._1lll1l11l11_opy_ = True
                logger.debug(bstack1111_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣሇ"))
            except Exception as e:
                logger.error(bstack1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯࡮ࠡࡧࡱࡨࡤࡺࡥࡴࡶ࠽ࠤࢀ࡫ࡽࠣለ").format(e=e))
        elif self._1lll1l11l11_opy_:
            logger.debug(bstack1111_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡧ࡬ࡳࡧࡤࡨࡾࠦ࡭ࡢࡴ࡮ࡩࡩࠨሉ"))
        else:
            logger.debug(bstack1111_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡸ࡮ࡼࡥࠡࡲࡤ࡫ࡪࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠣሊ"))
    def start_suite(self, name, attrs):
        bstack1111_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡷࡩࡧࡱࠤࡦࠦࡳࡶ࡫ࡷࡩࠥࡹࡴࡢࡴࡷࡷࠧࠨࠢላ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1111_opy_ (u"ࠧࡪࡦࠪሌ"), None)
            bstack1lll111ll1l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1lll111ll1l_opy_)
            return
        logger.debug(bstack1111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡷ࡬ࡸࡪࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡵࡸ࡭ࡹ࡫࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣል").format(name=name))
    def end_suite(self, name, attrs):
        bstack1111_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡺ࡬ࡪࡴࠠࡢࠢࡶࡹ࡮ࡺࡥࠡࡧࡱࡨࡸࠨࠢࠣሎ")
        if cli.is_running():
            bstack1lll111ll1l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1lll111ll1l_opy_)
            return
        logger.debug(bstack1111_opy_ (u"ࠥࡩࡳࡪ࡟ࡴࡷ࡬ࡸࡪࠦࡃࡂࡎࡏࡉࡉࠦ࠭ࠡࡵࡸ࡭ࡹ࡫࠺ࠡࡽࡱࡥࡲ࡫ࡽࠣሏ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨሐ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧሑ"), None)
            if attrs.get(bstack1111_opy_ (u"࠭ࡴࡺࡲࡨࠫሒ"), bstack1111_opy_ (u"ࠧࠨሓ")).lower() in [bstack1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧሔ"), bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫሕ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨሖ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1lll111111l_opy_ = SimpleNamespace(name=attrs.get(bstack1111_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫሗ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1lll111111l_opy_)
            else:
                if current_test_id:
                    bstack1lll111111l_opy_ = SimpleNamespace(name=attrs.get(bstack1111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬመ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1lll111111l_opy_, test_id=current_test_id)
        if self._1lll1l11l11_opy_ or self._1lll1l1l111_opy_:
            return
        bstack1lll111l11l_opy_ = False
        bstack1lll111lll1_opy_ = attrs.get(bstack1111_opy_ (u"࠭ࡴࡺࡲࡨࠫሙ"), bstack1111_opy_ (u"ࠧࠨሚ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1lll111l11l_opy_ = True
            logger.debug(bstack1111_opy_ (u"ࠣࡅ࡯ࡳࡸ࡫ࠠ࡬ࡧࡼࡻࡴࡸࡤࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࢀࡴࡡ࡮ࡧࢀ࠰ࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡪࡶࠣࡩࡽ࡫ࡣࡶࡶࡨࡷࠧማ").format(name=name))
        elif bstack1lll111lll1_opy_ == bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫሜ"):
            bstack1lll111l11l_opy_ = True
            logger.debug(bstack1111_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠬࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡸࡪࡧࡲࡥࡱࡺࡲࠥ࡫ࡸࡦࡥࡸࡸࡪࡹࠢም"))
        if bstack1lll111l11l_opy_ and self._1lll111llll_opy_():
            self._populate_browser_instance_data()
            self._1lll11l1l11_opy_()
    def end_keyword(self, name, attrs):
        bstack1111_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡦ࡬ࡴࡦࡴࠣࡥࠥࡱࡥࡺࡹࡲࡶࡩࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡴ࠰ࠥࠦࠧሞ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩሟ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨሠ"), None)
            bstack1lll111111l_opy_ = SimpleNamespace(name=attrs.get(bstack1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧሡ"), name), id=current_test_id, **attrs)
            bstack1lll11lll11_opy_ = SimpleNamespace(
                status=attrs.get(bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨሢ")),
                message=attrs.get(bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪሣ"), bstack1111_opy_ (u"ࠪࠫሤ")),
                starttime=attrs.get(bstack1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠧሥ"), bstack1111_opy_ (u"ࠬ࠭ሦ")),
                endtime=attrs.get(bstack1111_opy_ (u"࠭ࡥ࡯ࡦࡷ࡭ࡲ࡫ࠧሧ"), bstack1111_opy_ (u"ࠧࠨረ")),
                elapsedtime=attrs.get(bstack1111_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ሩ"), 0)
            )
            if attrs.get(bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧሪ"), bstack1111_opy_ (u"ࠪࠫራ")).lower() in [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪሬ"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧር")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1111_opy_ (u"࠭ࡴࡺࡲࡨࠫሮ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1lll111111l_opy_, bstack1lll11lll11_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1lll111111l_opy_, bstack1lll11lll11_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧሯ"), bstack1111_opy_ (u"ࠨࠩሰ")).upper() == bstack1111_opy_ (u"ࠩࡓࡅࡘ࡙ࠧሱ")):
                logger.debug(bstack1111_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࠤࡴࡶࡥ࡯ࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࡀࠠࡼࡰࡤࡱࡪࢃࠬࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡤࡢࡶࡤࠦሲ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1111_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡷࡿࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡳࡸࡺࡸࡥࡴࠢࡉࡅࡎࡒࠠ࡭ࡧࡹࡩࡱࠦ࡭ࡦࡵࡶࡥ࡬࡫ࡳࠡࡶࡲࠤࡺࡹࡥࠡࡣࡶࠤࡪࡸࡲࡰࡴࠣࡶࡪࡧࡳࡰࡰ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡹࡩ࡯ࡥࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡧࡴࡵࡴࡶࠤࡩࡵࡥࡴࡰࠪࡸࠥ࡯࡮ࡤ࡮ࡸࡨࡪࠦࡴࡩࡧࠣࡩࡷࡸ࡯ࡳࠢࡰࡩࡸࡹࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣሳ")
        if cli.is_running():
            try:
                if message.get(bstack1111_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪሴ"), bstack1111_opy_ (u"࠭࡮ࡰࠩስ")) == bstack1111_opy_ (u"ࠧࡺࡧࡶࠫሶ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩሷ"), bstack1111_opy_ (u"ࠩࠪሸ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1111_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧሹ"),
                            level=bstack1111_opy_ (u"ࠫࡎࡔࡆࡐࠩሺ"),
                            timestamp=message.get(bstack1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨሻ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨሼ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨሽ"), bstack1111_opy_ (u"ࠨࠩሾ")),
                        level=message.get(bstack1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨሿ"), bstack1111_opy_ (u"ࠪࡍࡓࡌࡏࠨቀ")),
                        timestamp=message.get(bstack1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧቁ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧቂ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬቃ"), bstack1111_opy_ (u"ࠧࠨቄ"))
        if level == bstack1111_opy_ (u"ࠨࡈࡄࡍࡑ࠭ቅ"):
            self._1lll11ll111_opy_ = message.get(bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪቆ"), bstack1111_opy_ (u"ࠪࠫቇ"))
            logger.debug(bstack1111_opy_ (u"ࠦࡈࡧࡰࡵࡷࡵࡩࡩࠦࡥࡳࡴࡲࡶࠥࡳࡥࡴࡵࡤ࡫ࡪࡀࠠࡼࡧࡵࡶࡴࡸࡽࠣቈ").format(error=self._1lll11ll111_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1111_opy_ (u"ࠧࠨࠢࡅࡧࡷࡩࡷࡳࡩ࡯ࡧࠣ࡭࡫ࠦࡳࡦࡶࡸࡴ࠴ࡺࡥࡢࡴࡧࡳࡼࡴࠠࡪࡵࠣࡷࡺ࡯ࡴࡦ࠯࡯ࡩࡻ࡫࡬ࠡࡱࡵࠤࡹ࡫ࡳࡵ࠯࡯ࡩࡻ࡫࡬࠯ࠤࠥࠦ቉")
        if hook_type.lower() == bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬቊ"):
            return bstack1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫቋ") if current_test_uuid is None else bstack1111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ቌ")
        elif hook_type.lower() == bstack1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫቍ"):
            return bstack1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭቎") if current_test_uuid is None else bstack1111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ቏")