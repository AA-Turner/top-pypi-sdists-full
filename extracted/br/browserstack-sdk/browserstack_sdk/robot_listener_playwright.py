# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1111lll_opy_ import bstack1111l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll1l11l1l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack1l11lll1_opy_ import bstack1l11lll1_opy_, bstack1111ll11_opy_, bstack1l1l111l11_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1lll11l11l1_opy_
    _1lll111ll1l_opy_ = bstack1lll11l11l1_opy_.VERSION
except:
    _1lll111ll1l_opy_ = bstack1lll1l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᆖ")
cli_context = bstack1lll1l11l1l_opy_(
    test_framework_name=bstack1lll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨᆗ"),
    test_framework_version=_1lll111ll1l_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1lll1l_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴࠪᆘ"), bstack1lll1l_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡧࡴࡴࡴࡦࡺࡷࠫᆙ"), bstack1lll1l_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡵࡧࡧࡦࠩᆚ"),
        bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠧᆛ"), bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡱࡸࡪࡾࡴࠨᆜ"), bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡲࡤ࡫ࡪ࠭ᆝ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1lll1l_opy_ (u"ࠩࡱࡩࡼࠦࡢࡳࡱࡺࡷࡪࡸࠧᆞ"), bstack1lll1l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠤࡹࡵࠠࡣࡴࡲࡻࡸ࡫ࡲࠨᆟ"),
        bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࠢࡥࡶࡴࡽࡳࡦࡴࠪᆠ"), bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣࡰࡰࡱࡩࡨࡺࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࠫᆡ"),
    }
    def __init__(self):
        self._1lll1l111ll_opy_ = None
        self._1lll1l1l111_opy_ = False
        self._1lll11l1lll_opy_ = False
        self._1lll11lll1l_opy_ = None
        self._1lll11l1l1l_opy_ = None
        self._1lll11l111l_opy_ = False
        if cli.bstack1111111ll_opy_():
            try:
                if cli.bstack1lll1l1ll1l_opy_:
                    cli_context.platform_index = cli.bstack1lll1l1ll1l_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᆢ"), bstack1lll1l_opy_ (u"ࠧ࠱ࠩᆣ")))
            except Exception as e:
                pass
    def _1lll11l1111_opy_(self):
        if self._1lll1l111ll_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1lll1l111ll_opy_ = BuiltIn().get_library_instance(bstack1lll1l_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࠩᆤ"))
            except Exception as e:
                logger.warning(bstack1lll1l_opy_ (u"ࠤࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡼࡧࢀࠦᆥ").format(e=e))
        return self._1lll1l111ll_opy_
    def _1lll1111l1l_opy_(self):
        try:
            bstack1lll1l1l11l_opy_ = self._1lll11l1111_opy_()
            if bstack1lll1l1l11l_opy_ and hasattr(bstack1lll1l1l11l_opy_, bstack1lll1l_opy_ (u"ࠪࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡵࡷࡥࡹ࡫ࠧᆦ")):
                bstack1lll11l11ll_opy_ = bstack1lll1l1l11l_opy_._playwright_state
                if hasattr(bstack1lll11l11ll_opy_, bstack1lll1l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡦࡺࡡ࡭ࡱࡪࠫᆧ")):
                    bstack1lll11111ll_opy_ = bstack1lll11l11ll_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lll11111ll_opy_ = BuiltIn().run_keyword(bstack1lll1l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠴ࡇࡦࡶࠣࡆࡷࡵࡷࡴࡧࡵࠤࡈࡧࡴࡢ࡮ࡲ࡫ࠬᆨ"))
                for bstack1lll11l1l11_opy_ in bstack1lll11111ll_opy_:
                    contexts = bstack1lll11l1l11_opy_.get(bstack1lll1l_opy_ (u"࠭ࡣࡰࡰࡷࡩࡽࡺࡳࠨᆩ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1lll1l_opy_ (u"ࠧࡱࡣࡪࡩࡸ࠭ᆪ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1lll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠾ࠥࢁࡥࡾࠤᆫ").format(e=e))
            return False
    def _1lll111ll11_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1lll1l1l1l1_opy_ = {
                bstack1lll1l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩᆬ"): action,
                bstack1lll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᆭ"): arguments
            }
            executor_cmd = bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠧᆮ") + json.dumps(bstack1lll1l1l1l1_opy_)
            arg_string = bstack1lll1l_opy_ (u"ࠧࡧࡲࡨ࠿ࡾࡩࡽ࡫ࡣࡶࡶࡲࡶࡤࡩ࡭ࡥࡿࠥᆯ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1lll1l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸ࠮ࡆࡸࡤࡰࡺࡧࡴࡦࠢࡍࡥࡻࡧࡓࡤࡴ࡬ࡴࡹ࠭ᆰ"),
                None,
                bstack1lll1l_opy_ (u"ࠧࡠࠢࡀࡂࠥࢁࡽࠨᆱ"),
                arg_string
            )
            logger.debug(bstack1lll1l_opy_ (u"ࠣࡇࡻࡩࡨࡻࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡡࡤࡶ࡬ࡳࡳࢃࠬࠡࡴࡨࡷࡺࡲࡴ࠻ࠢࡾࡶࡪࡹࡵ࡭ࡶࢀࠦᆲ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࡨࢁࠧᆳ").format(e=e))
    def _call_driver_init(self):
        bstack1lll1l_opy_ (u"ࠥࠦࠧࡓࡡ࡬ࡧࠣࡸ࡭࡫ࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲࠠࡵࡱࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡺࡨࡪࡵࠣࡶࡴࡨ࡯ࡵ࠯ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡳࡳࡵࡻ࡬ࡢࡶࡨࡷࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡌࡲࡩ࡫ࡸࡾࡡࡵࡩ࡫ࡥࡻࡳࡧࡩࢁࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡮ࡴࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼࠫࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡳࡵࡱࡵࡩ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥ࡯ࡳࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡪࡴࡸࠠࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠤࡪࡼࡥ࡯ࡶࡶ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡰࡳࡱࡧࡹࡨࡺࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡩࡱࡲ࡯ࡸࠦࠨࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠬࠡ࡮ࡲࡧࡦࡲࠠࡵࡷࡱࡲࡪࡲࠬࠡࡃࡌ࠭࠱ࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᆴ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import bstack1lll1111l11_opy_
            from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
            if not cli.bstack1lll111lll1_opy_ or not cli.cli_bin_session_id:
                logger.debug(bstack1lll1l_opy_ (u"ࠦࡤࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࡦࡰ࡮ࠦ࡮ࡰࡶࠣࡶࡪࡧࡤࡺ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᆵ"))
                return None
            instance = next(iter(bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.values()), None)
            if not instance:
                logger.debug(bstack1lll1l_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠨᆶ"))
                return None
            hub_url = os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡏࡃࡑࡗࡣࡕ࡝࡟ࡄࡆࡓࡣ࡚ࡘࡌࠨᆷ"), bstack1lll1l_opy_ (u"ࠧࠨᆸ"))
            req = structs.DriverInitRequest()
            req.bin_session_id = cli.cli_bin_session_id
            req.platform_index = cli_context.platform_index if cli_context.platform_index >= 0 else 0
            req.ref = instance.ref()
            req.user_input_params = json.dumps({bstack1lll1l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᆹ"): True}).encode(bstack1lll1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᆺ"))
            if hub_url:
                req.hub_url = hub_url
            req.client_worker_id = bstack1lll1l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᆻ").format(threading.get_ident(), os.getpid())
            logger.debug(bstack1lll1l_opy_ (u"ࠦࡤࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡧࡩࡁࢀࡸࡥࡧࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶࡩࡾࠤᆼ").format(
                ref=instance.ref(), pi=req.platform_index))
            response = cli.bstack1lll111lll1_opy_.DriverInit(req)
            if response and response.success:
                logger.debug(bstack1lll1l_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠥᆽ"))
                if response.capabilities:
                    try:
                        bstack1lll11l1ll1_opy_ = json.loads(response.capabilities.decode(bstack1lll1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᆾ")))
                        if bstack1lll11l1ll1_opy_:
                            bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll11ll1l1_opy_, bstack1lll11l1ll1_opy_)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.debug(bstack1lll1l_opy_ (u"ࠢࡠࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࡼࡧࢀࠦᆿ").format(e=e))
                return response
            else:
                logger.debug(bstack1lll1l_opy_ (u"ࠣࡡࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡶࡪࡺࡵࡳࡰࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸࡃࡆࡢ࡮ࡶࡩࠧᇀ"))
                return None
        except Exception as e:
            logger.debug(bstack1lll1l_opy_ (u"ࠤࡢࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࡨࢁࠧᇁ").format(e=e))
            return None
    def _populate_browser_instance_data(self):
        bstack1lll1l_opy_ (u"ࠥࠦࠧࡖ࡯ࡱࡷ࡯ࡥࡹ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬ࠡࡣࡱࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡲࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠠࡧࡱࡵࠤࡷࡵࡢࡰࡶ࠰ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࠣࠤࠥᇂ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import bstack1lll1111l11_opy_
            from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
            if not self._1lll1111l1l_opy_():
                logger.debug(bstack1lll1l_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨᇃ"))
                return
            if not self._1lll11l111l_opy_:
                response = self._call_driver_init()
                self._1lll11l111l_opy_ = True
                if response and response.success:
                    logger.debug(bstack1lll1l_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠤᇄ"))
            result = self._1lll111ll11_opy_(bstack1lll1l_opy_ (u"࠭ࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠪᇅ"), {})
            logger.debug(bstack1lll1l_opy_ (u"ࠢࡠࡲࡲࡴࡺࡲࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡤࡢࡶࡤ࠾ࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡸࡻ࡬ࡵ࠿ࡾࡶࢂࠨᇆ").format(r=result))
            if not result:
                logger.debug(bstack1lll1l_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦ࡮ࡰࠢࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦᇇ"))
                return
            bstack1lll11ll111_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1lll11ll111_opy_.get(bstack1lll1l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᇈ"), bstack1lll1l_opy_ (u"ࠪࠫᇉ"))
            hub_url = os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡔࡈࡏࡕࡡࡓ࡛ࡤࡉࡄࡑࡡࡘࡖࡑ࠭ᇊ"), bstack1lll1l_opy_ (u"ࠬ࠭ᇋ"))
            logger.debug(bstack1lll1l_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࡽࡶ࡭ࡩࢃࠬࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࡾࡹࡷࡲࡽࠣᇌ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1lll1l_opy_ (u"ࠧࠨᇍ")))
            current_test_id = getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪᇎ"), None)
            for instance in bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.values():
                if not bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1111ll1_opy_, None):
                    bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1111ll1_opy_, session_id)
                    bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1l11ll1_opy_, hub_url)
                    if current_test_id:
                        bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪᇏ"), current_test_id)
                    logger.debug(bstack1lll1l_opy_ (u"ࠥࡔࡴࡶࡵ࡭ࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠼ࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࡼࡵ࡬ࡨࢂ࠲ࠠࡩࡷࡥࡣࡺࡸ࡬ࠡࡵࡨࡸ࠱ࠦࡴࡦࡵࡷࡣ࡮ࡪ࠽ࡼࡶ࡬ࡨࢂࠨᇐ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱࡳࡹࡱࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡪࡡࡵࡣ࠽ࠤࢀ࡫ࡽࠣᇑ").format(e=e))
    def _clear_session_data(self):
        bstack1lll1l_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬ࡲࡰ࡯ࠣࡥࡱࡲࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࠤࡹࡵࠠࡦࡰࡶࡹࡷ࡫ࠠࡵࡧࡶࡸࠥ࡯ࡳࡰ࡮ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᇒ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import bstack1lll1111l11_opy_
            from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
            bstack1lll111l111_opy_ = 0
            for instance in bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.values():
                bstack1lll1111lll_opy_ = False
                if bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1111ll1_opy_, None):
                    bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1111ll1_opy_, bstack1lll1l_opy_ (u"࠭ࠧᇓ"))
                    bstack1lll1111lll_opy_ = True
                if bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1l11ll1_opy_, None):
                    bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll111l1ll_opy_.bstack1lll1l11ll1_opy_, bstack1lll1l_opy_ (u"ࠧࠨᇔ"))
                    bstack1lll1111lll_opy_ = True
                if bstack1lll111l1ll_opy_.bstack1lll111l1l1_opy_(instance, bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡩࡥࠩᇕ"), None):
                    bstack1lll111l1ll_opy_.bstack1lll1l11lll_opy_(instance, bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪᇖ"), None)
                    bstack1lll1111lll_opy_ = True
                if bstack1lll1111lll_opy_:
                    bstack1lll111l111_opy_ += 1
            logger.debug(bstack1lll1l_opy_ (u"ࠥࡣࡨࡲࡥࡢࡴࡢࡷࡪࡹࡳࡪࡱࡱࡣࡩࡧࡴࡢ࠼ࠣࡇࡱ࡫ࡡࡳࡧࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡽࡱࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠣᇗ").format(
                n=bstack1lll111l111_opy_))
        except Exception as e:
            logger.debug(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡦࡿࠥᇘ").format(e=e))
    def _1lll1l11111_opy_(self, status, reason=bstack1lll1l_opy_ (u"ࠧࠨᇙ")):
        bstack1lll1l_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦᇚ")
        bstack1lll11lllll_opy_ = bstack1lll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᇛ") if status == bstack1lll1l_opy_ (u"ࠣࡒࡄࡗࡘࠨᇜ") else bstack1lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᇝ")
        if bstack1lll11lllll_opy_ == bstack1lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᇞ"):
            return self._1lll111ll11_opy_(bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᇟ"), {
                bstack1lll1l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᇠ"): bstack1lll11lllll_opy_,
                bstack1lll1l_opy_ (u"ࠨࡲࡦࡣࡶࡳࡳࠨᇡ"): reason
            })
        else:
            return self._1lll111ll11_opy_(bstack1lll1l_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᇢ"), {
                bstack1lll1l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᇣ"): bstack1lll11lllll_opy_
            })
    def _1lll1l111l1_opy_(self, name):
        bstack1lll1l_opy_ (u"ࠤࠥࠦࡘ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦᇤ")
        return self._1lll111ll11_opy_(bstack1lll1l_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᇥ"), {
            bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇦ"): name
        })
    def _1lll11llll1_opy_(self):
        bstack1lll1l_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡣࡧࡩࡳࡷ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡥ࡯ࡳࡸ࡫ࠠࡰࡴࠣࡸࡪࡧࡲࡥࡱࡺࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡶࡤࡸࡺࡹࠠࡪࡵࠣ࡭ࡳ࡬ࡥࡳࡴࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡣࡱࡧࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦ࠼ࠣ࡭࡫ࠦࡡ࡯ࡻࠣࡊࡆࡏࡌ࠮࡮ࡨࡺࡪࡲࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡢࡵࠣࡧࡦࡶࡴࡶࡴࡨࡨࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡷࡩࡸࡺࠬࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࠦࡦࡢ࡫࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᇧ")
        if self._1lll11l1lll_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._1lll11lll1l_opy_ and not global_config.should_skip_session_name():
                self._1lll1l111l1_opy_(self._1lll11lll1l_opy_)
            status = bstack1lll1l_opy_ (u"࠭ࡆࡂࡋࡏࠫᇨ") if self._1lll11l1l1l_opy_ else bstack1lll1l_opy_ (u"ࠧࡑࡃࡖࡗࠬᇩ")
            message = self._1lll11l1l1l_opy_ or bstack1lll1l_opy_ (u"ࠨࠩᇪ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack1lll1l_opy_ (u"ࠤࡐࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡨࡲ࡯ࡴࡧ࠽ࠤࡸࡺࡡࡵࡷࡶࡁࢀࡹࡴࡢࡶࡸࡷࢂ࠲ࠠ࡮ࡧࡶࡷࡦ࡭ࡥ࠾ࡽࡰࡩࡸࡹࡡࡨࡧࢀࠦᇫ").format(status=status, message=message))
                self._1lll1l11111_opy_(status, message)
            self._1lll11l1lll_opy_ = True
            logger.debug(bstack1lll1l_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡰࡥࡷࡱࡥࡥࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᇬ"))
        except Exception as e:
            logger.error(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡧࢀࠦᇭ").format(e=e))
    def _extract_screenshot_base64(self, bstack1lll11lll11_opy_):
        bstack1lll1l_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡌ࡙ࡓࡌࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡲࡦࡴࡺࠧࡴࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡱࡵࡧࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠠࡢࡵࠣࡌ࡙ࡓࡌࠡࡹ࡬ࡸ࡭ࠦࡥࡪࡶ࡫ࡩࡷࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡨࡥࡥࡦࡨࡨ࠿ࠦ࠼ࡪ࡯ࡪࠤࡸࡸࡣ࠾ࠤࡧࡥࡹࡧ࠺ࡪ࡯ࡤ࡫ࡪ࠵ࡰ࡯ࡩ࠾ࡦࡦࡹࡥ࠷࠶࠯ࡿࡩࡧࡴࡢࡿࠥࠤ࠳࠴࠮࠿ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌࡩ࡭ࡧࠣࡰ࡮ࡴ࡫࠻ࠢ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧࡶࡡࡵࡪ࠲ࡸࡴ࠵ࡦࡪ࡮ࡨ࠲ࡵࡴࡧࠣࠢ࠱࠲࠳ࡄࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᇮ")
        match = re.search(bstack1lll1l_opy_ (u"ࡸࠧࡴࡴࡦࡁࠧࡪࡡࡵࡣ࠽࡭ࡲࡧࡧࡦ࠱ࡳࡲ࡬ࡁࡢࡢࡵࡨ࠺࠹࠲ࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨᇯ"), bstack1lll11lll11_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1lll1l_opy_ (u"ࡲࠨ࠾࡬ࡱ࡬ࡡ࡞࠿࡟࠮ࡷࡷࡩ࠽ࠣࠪ࡞ࡢࠧࡣࠫ࡝࠰ࠫࡃ࠿ࡶ࡮ࡨࡾ࡭ࡴ࡬ࢂࡪࡱࡧࡪ࠭࠮ࠨࠧᇰ"), bstack1lll11lll11_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1lll1l11l11_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠨࡔࡒࡆࡔ࡚࡟ࡐࡗࡗࡔ࡚࡚࡟ࡅࡋࡕࠫᇱ"), os.getcwd())
                    path = Path(bstack1lll1l11l11_opy_) / path
                if path.is_file():
                    with open(path, bstack1lll1l_opy_ (u"ࠩࡵࡦࠬᇲ")) as f:
                        return base64.b64encode(f.read()).decode(bstack1lll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᇳ"))
            except Exception as e:
                logger.debug(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡩ࡭ࡱ࡫ࠠࡼࡲࡤࡸ࡭ࢃ࠺ࠡࡽࡨࢁࠧᇴ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1lll1l1l111_opy_ = False
            self._1lll11l1lll_opy_ = False
            self._1lll11lll1l_opy_ = name
            self._1lll11l1l1l_opy_ = None
            self._1lll11l111l_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨᇵ"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1lll1l_opy_ (u"࠭ࡩࡥࠩᇶ"), None)
            self._clear_session_data()
            bstack111111llll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack111111llll_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack111111llll_opy_)
            return
        logger.debug(bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡴࡦࡵࡷࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡴࡦࡵࡷ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧᇷ").format(name=name))
        self._1lll1l1l111_opy_ = False
        self._1lll11l1lll_opy_ = False
        self._1lll11lll1l_opy_ = name
        self._1lll11l1l1l_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack111111llll_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1lll11ll11l_opy_ = SimpleNamespace(
                status=attrs.get(bstack1lll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᇸ")),
                message=attrs.get(bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᇹ"), bstack1lll1l_opy_ (u"ࠪࠫᇺ")),
                starttime=attrs.get(bstack1lll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠧᇻ"), bstack1lll1l_opy_ (u"ࠬ࠭ᇼ")),
                endtime=attrs.get(bstack1lll1l_opy_ (u"࠭ࡥ࡯ࡦࡷ࡭ࡲ࡫ࠧᇽ"), bstack1lll1l_opy_ (u"ࠧࠨᇾ")),
                elapsedtime=attrs.get(bstack1lll1l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ᇿ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack111111llll_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack111111llll_opy_, bstack1lll11ll11l_opy_)
        status = attrs.get(bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩሀ"), bstack1lll1l_opy_ (u"࡙ࠪࡓࡑࡎࡐ࡙ࡑࠫሁ"))
        message = attrs.get(bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬሂ"), bstack1lll1l_opy_ (u"ࠬ࠭ሃ"))
        logger.debug(bstack1lll1l_opy_ (u"ࠨࡥ࡯ࡦࡢࡸࡪࡹࡴࠡࡅࡄࡐࡑࡋࡄࠡ࠯ࠣࡸࡪࡹࡴ࠻ࠢࡾࡲࡦࡳࡥࡾ࠮ࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࡹࡴࡢࡶࡸࡷࢂࠨሄ").format(name=name, status=status))
        self._1lll1l1l111_opy_ = True
        if not self._1lll11l1lll_opy_ and self._1lll1111l1l_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1lll1l111l1_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack1lll1l_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡵࡷࡥࡹࡻࡳ࠾ࡽࡶࡸࡦࡺࡵࡴࡿࠥህ").format(status=status))
                    self._1lll1l11111_opy_(status, message)
                self._1lll11l1lll_opy_ = True
                logger.debug(bstack1lll1l_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢሆ"))
            except Exception as e:
                logger.error(bstack1lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡪࢃࠢሇ").format(e=e))
        elif self._1lll11l1lll_opy_:
            logger.debug(bstack1lll1l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤࡦࡲࡲࡦࡣࡧࡽࠥࡳࡡࡳ࡭ࡨࡨࠧለ"))
        else:
            logger.debug(bstack1lll1l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠢሉ"))
    def start_suite(self, name, attrs):
        bstack1lll1l_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡽࡨࡦࡰࠣࡥࠥࡹࡵࡪࡶࡨࠤࡸࡺࡡࡳࡶࡶࠦࠧࠨሊ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1lll1l_opy_ (u"࠭ࡩࡥࠩላ"), None)
            bstack1lll1l1l1ll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1lll1l1l1ll_opy_)
            return
        logger.debug(bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢሌ").format(name=name))
    def end_suite(self, name, attrs):
        bstack1lll1l_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡹ࡫ࡩࡳࠦࡡࠡࡵࡸ࡭ࡹ࡫ࠠࡦࡰࡧࡷࠧࠨࠢል")
        if cli.is_running():
            bstack1lll1l1l1ll_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1lll1l1l1ll_opy_)
            return
        logger.debug(bstack1lll1l_opy_ (u"ࠤࡨࡲࡩࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢሎ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧሏ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ሐ"), None)
            if attrs.get(bstack1lll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪሑ"), bstack1lll1l_opy_ (u"࠭ࠧሒ")).lower() in [bstack1lll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ሓ"), bstack1lll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪሔ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧሕ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1lll11ll1ll_opy_ = SimpleNamespace(name=attrs.get(bstack1lll1l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪሖ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1lll11ll1ll_opy_)
            else:
                if current_test_id:
                    bstack1lll11ll1ll_opy_ = SimpleNamespace(name=attrs.get(bstack1lll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫሗ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1lll11ll1ll_opy_, test_id=current_test_id)
        if self._1lll11l1lll_opy_ or self._1lll1l1l111_opy_:
            return
        bstack1lll1l1ll11_opy_ = False
        bstack1lll111llll_opy_ = attrs.get(bstack1lll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪመ"), bstack1lll1l_opy_ (u"࠭ࠧሙ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1lll1l1ll11_opy_ = True
            logger.debug(bstack1lll1l_opy_ (u"ࠢࡄ࡮ࡲࡷࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡩࡵࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦሚ").format(name=name))
        elif bstack1lll111llll_opy_ == bstack1lll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪማ"):
            bstack1lll1l1ll11_opy_ = True
            logger.debug(bstack1lll1l_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬࠲ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡷࡩࡦࡸࡤࡰࡹࡱࠤࡪࡾࡥࡤࡷࡷࡩࡸࠨሜ"))
        if bstack1lll1l1ll11_opy_ and self._1lll1111l1l_opy_():
            self._populate_browser_instance_data()
            self._1lll11llll1_opy_()
    def end_keyword(self, name, attrs):
        bstack1lll1l_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡥ࡫ࡺࡥࡳࠢࡤࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡳ࠯ࠤࠥࠦም")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨሞ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧሟ"), None)
            bstack1lll11ll1ll_opy_ = SimpleNamespace(name=attrs.get(bstack1lll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ሠ"), name), id=current_test_id, **attrs)
            bstack1lll11ll11l_opy_ = SimpleNamespace(
                status=attrs.get(bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧሡ")),
                message=attrs.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩሢ"), bstack1lll1l_opy_ (u"ࠩࠪሣ")),
                starttime=attrs.get(bstack1lll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡶ࡬ࡱࡪ࠭ሤ"), bstack1lll1l_opy_ (u"ࠫࠬሥ")),
                endtime=attrs.get(bstack1lll1l_opy_ (u"ࠬ࡫࡮ࡥࡶ࡬ࡱࡪ࠭ሦ"), bstack1lll1l_opy_ (u"࠭ࠧሧ")),
                elapsedtime=attrs.get(bstack1lll1l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬረ"), 0)
            )
            if attrs.get(bstack1lll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ሩ"), bstack1lll1l_opy_ (u"ࠩࠪሪ")).lower() in [bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩራ"), bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ሬ")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1lll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪር")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1lll11ll1ll_opy_, bstack1lll11ll11l_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1lll11ll1ll_opy_, bstack1lll11ll11l_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ሮ"), bstack1lll1l_opy_ (u"ࠧࠨሯ")).upper() == bstack1lll1l_opy_ (u"ࠨࡒࡄࡗࡘ࠭ሰ")):
                logger.debug(bstack1lll1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࠣࡳࡵ࡫࡮ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨ࠿ࠦࡻ࡯ࡣࡰࡩࢂ࠲ࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠥሱ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1lll1l_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡶࡾࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡲࡷࡹࡷ࡫ࡳࠡࡈࡄࡍࡑࠦ࡬ࡦࡸࡨࡰࠥࡳࡥࡴࡵࡤ࡫ࡪࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡢࡵࠣࡩࡷࡸ࡯ࡳࠢࡵࡩࡦࡹ࡯࡯࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡯࡮ࡤࡧࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡺࡴࡳࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡺࡨࡦࠢࡨࡶࡷࡵࡲࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢሲ")
        if cli.is_running():
            try:
                if message.get(bstack1lll1l_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩሳ"), bstack1lll1l_opy_ (u"ࠬࡴ࡯ࠨሴ")) == bstack1lll1l_opy_ (u"࠭ࡹࡦࡵࠪስ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨሶ"), bstack1lll1l_opy_ (u"ࠨࠩሷ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1lll1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ሸ"),
                            level=bstack1lll1l_opy_ (u"ࠪࡍࡓࡌࡏࠨሹ"),
                            timestamp=message.get(bstack1lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧሺ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧሻ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1lll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧሼ"), bstack1lll1l_opy_ (u"ࠧࠨሽ")),
                        level=message.get(bstack1lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧሾ"), bstack1lll1l_opy_ (u"ࠩࡌࡒࡋࡕࠧሿ")),
                        timestamp=message.get(bstack1lll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ቀ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1lll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ቁ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫቂ"), bstack1lll1l_opy_ (u"࠭ࠧቃ"))
        if level == bstack1lll1l_opy_ (u"ࠧࡇࡃࡌࡐࠬቄ"):
            self._1lll11l1l1l_opy_ = message.get(bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩቅ"), bstack1lll1l_opy_ (u"ࠩࠪቆ"))
            logger.debug(bstack1lll1l_opy_ (u"ࠥࡇࡦࡶࡴࡶࡴࡨࡨࠥ࡫ࡲࡳࡱࡵࠤࡲ࡫ࡳࡴࡣࡪࡩ࠿ࠦࡻࡦࡴࡵࡳࡷࢃࠢቇ").format(error=self._1lll11l1l1l_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1lll1l_opy_ (u"ࠦࠧࠨࡄࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡬ࡪࠥࡹࡥࡵࡷࡳ࠳ࡹ࡫ࡡࡳࡦࡲࡻࡳࠦࡩࡴࠢࡶࡹ࡮ࡺࡥ࠮࡮ࡨࡺࡪࡲࠠࡰࡴࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲ࠮ࠣࠤࠥቈ")
        if hook_type.lower() == bstack1lll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ቉"):
            return bstack1lll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪቊ") if current_test_uuid is None else bstack1lll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬቋ")
        elif hook_type.lower() == bstack1lll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪቌ"):
            return bstack1lll1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬቍ") if current_test_uuid is None else bstack1lll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ቎")