# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import base64
import json
import os
import re
import threading
from types import SimpleNamespace
from bstack_utils.logger_utils import get_logger
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111l1l1111_opy_ import bstack1ll11l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll11l1l1l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.bstack1lll11111_opy_ import bstack1lll11111_opy_, Events, bstack1lll1111_opy_
from browserstack_sdk import sdk_pb2 as structs
logger = get_logger(__name__)
try:
    from robot import version as bstack1ll1llll1ll_opy_
    _1ll1llll111_opy_ = bstack1ll1llll1ll_opy_.VERSION
except:
    _1ll1llll111_opy_ = bstack1ll111_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᇿ")
cli_context = bstack1lll11l1l1l_opy_(
    test_framework_name=bstack1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨሀ"),
    test_framework_version=_1ll1llll111_opy_,
    platform_index=-1,
)
class PlaywrightPatcher:
    ROBOT_LISTENER_API_VERSION = 2
    _CLOSE_KEYWORDS = {
        bstack1ll111_opy_ (u"ࠪࡧࡱࡵࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴࠪሁ"), bstack1ll111_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠣࡧࡴࡴࡴࡦࡺࡷࠫሂ"), bstack1ll111_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠤࡵࡧࡧࡦࠩሃ"),
        bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࠮ࡤ࡮ࡲࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠧሄ"), bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲ࠯ࡥ࡯ࡳࡸ࡫ࠠࡤࡱࡱࡸࡪࡾࡴࠨህ"), bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ࠰ࡦࡰࡴࡹࡥࠡࡲࡤ࡫ࡪ࠭ሆ"),
    }
    _BROWSER_OPEN_KEYWORDS = {
        bstack1ll111_opy_ (u"ࠩࡱࡩࡼࠦࡢࡳࡱࡺࡷࡪࡸࠧሇ"), bstack1ll111_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠤࡹࡵࠠࡣࡴࡲࡻࡸ࡫ࡲࠨለ"),
        bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࠳ࡴࡥࡸࠢࡥࡶࡴࡽࡳࡦࡴࠪሉ"), bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠴ࡣࡰࡰࡱࡩࡨࡺࠠࡵࡱࠣࡦࡷࡵࡷࡴࡧࡵࠫሊ"),
    }
    def __init__(self):
        self._1lll1111111_opy_ = None
        self._1ll1lll1ll1_opy_ = False
        self._1lll111l11l_opy_ = False
        self._1ll1lllll11_opy_ = None
        self._1lll11l11ll_opy_ = None
        self._1lll1111lll_opy_ = False
        if cli.bstack111ll1l1_opy_():
            try:
                if cli.bstack1lll11111ll_opy_:
                    cli_context.platform_index = cli.bstack1lll11111ll_opy_.platform_index
                else:
                    cli_context.platform_index = int(os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ላ"), bstack1ll111_opy_ (u"ࠧ࠱ࠩሌ")))
            except Exception as e:
                pass
    def _1lll11l1lll_opy_(self):
        if self._1lll1111111_opy_ is None:
            try:
                from robot.libraries.BuiltIn import BuiltIn
                self._1lll1111111_opy_ = BuiltIn().get_library_instance(bstack1ll111_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࠩል"))
            except Exception as e:
                logger.warning(bstack1ll111_opy_ (u"ࠤࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡼࡧࢀࠦሎ").format(e=e))
        return self._1lll1111111_opy_
    def _1ll1llll1l1_opy_(self):
        try:
            bstack1ll1ll1llll_opy_ = self._1lll11l1lll_opy_()
            if bstack1ll1ll1llll_opy_ and hasattr(bstack1ll1ll1llll_opy_, bstack1ll111_opy_ (u"ࠪࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡵࡷࡥࡹ࡫ࠧሏ")):
                bstack1lll11l1111_opy_ = bstack1ll1ll1llll_opy_._playwright_state
                if hasattr(bstack1lll11l1111_opy_, bstack1ll111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡦࡺࡡ࡭ࡱࡪࠫሐ")):
                    bstack1lll11l11l1_opy_ = bstack1lll11l1111_opy_._get_browser_catalog()
                else:
                    from robot.libraries.BuiltIn import BuiltIn
                    bstack1lll11l11l1_opy_ = BuiltIn().run_keyword(bstack1ll111_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࠴ࡇࡦࡶࠣࡆࡷࡵࡷࡴࡧࡵࠤࡈࡧࡴࡢ࡮ࡲ࡫ࠬሑ"))
                for bstack1lll111ll11_opy_ in bstack1lll11l11l1_opy_:
                    contexts = bstack1lll111ll11_opy_.get(bstack1ll111_opy_ (u"࠭ࡣࡰࡰࡷࡩࡽࡺࡳࠨሒ"), [])
                    for ctx in contexts:
                        pages = ctx.get(bstack1ll111_opy_ (u"ࠧࡱࡣࡪࡩࡸ࠭ሓ"), [])
                        if pages:
                            return True
            return False
        except Exception as e:
            logger.warning(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠾ࠥࢁࡥࡾࠤሔ").format(e=e))
            return False
    def _1ll1llll11l_opy_(self, action, arguments):
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            bstack1lll111111l_opy_ = {
                bstack1ll111_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩሕ"): action,
                bstack1ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ሖ"): arguments
            }
            executor_cmd = bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠧሗ") + json.dumps(bstack1lll111111l_opy_)
            arg_string = bstack1ll111_opy_ (u"ࠧࡧࡲࡨ࠿ࡾࡩࡽ࡫ࡣࡶࡶࡲࡶࡤࡩ࡭ࡥࡿࠥመ").format(executor_cmd=executor_cmd)
            result = builtin.run_keyword(
                bstack1ll111_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸ࠮ࡆࡸࡤࡰࡺࡧࡴࡦࠢࡍࡥࡻࡧࡓࡤࡴ࡬ࡴࡹ࠭ሙ"),
                None,
                bstack1ll111_opy_ (u"ࠧࡠࠢࡀࡂࠥࢁࡽࠨሚ"),
                arg_string
            )
            logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡻࡩࡨࡻࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡡࡤࡶ࡬ࡳࡳࢃࠬࠡࡴࡨࡷࡺࡲࡴ࠻ࠢࡾࡶࡪࡹࡵ࡭ࡶࢀࠦማ").format(action=action, result=result))
            return result
        except Exception as e:
            logger.warning(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࡨࢁࠧሜ").format(e=e))
    def _call_driver_init(self):
        bstack1ll111_opy_ (u"ࠥࠦࠧࡓࡡ࡬ࡧࠣࡸ࡭࡫ࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲࠠࡵࡱࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡺࡨࡪࡵࠣࡶࡴࡨ࡯ࡵ࠯ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡺࡨࡦࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡳࡳࡵࡻ࡬ࡢࡶࡨࡷࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡌࡲࡩ࡫ࡸࡾࡡࡵࡩ࡫ࡥࡻࡳࡧࡩࢁࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡮ࡴࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼࠫࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡳࡵࡱࡵࡩ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥ࡯ࡳࠡࡴࡨࡵࡺ࡯ࡲࡦࡦࠣࡪࡴࡸࠠࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠤࡪࡼࡥ࡯ࡶࡶ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡰࡳࡱࡧࡹࡨࡺࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡩࡱࡲ࡯ࡸࠦࠨࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠬࠡ࡮ࡲࡧࡦࡲࠠࡵࡷࡱࡲࡪࡲࠬࠡࡃࡌ࠭࠱ࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦም")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1lllllll_opy_
            from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
            if not cli.bstack1ll1lll11ll_opy_ or not cli.cli_bin_session_id:
                logger.debug(bstack1ll111_opy_ (u"ࠦࡤࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࡦࡰ࡮ࠦ࡮ࡰࡶࠣࡶࡪࡧࡤࡺ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧሞ"))
                return None
            instance = next(iter(bstack1ll1lllllll_opy_.bstack1ll1llllll1_opy_.values()), None)
            if not instance:
                logger.debug(bstack1ll111_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡲࡴࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠨሟ"))
                return None
            hub_url = os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡏࡃࡑࡗࡣࡕ࡝࡟ࡄࡆࡓࡣ࡚ࡘࡌࠨሠ"), bstack1ll111_opy_ (u"ࠧࠨሡ"))
            req = structs.DriverInitRequest()
            req.bin_session_id = cli.cli_bin_session_id
            req.platform_index = cli_context.platform_index if cli_context.platform_index >= 0 else 0
            req.ref = instance.ref()
            req.user_input_params = json.dumps({bstack1ll111_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧሢ"): True}).encode(bstack1ll111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣሣ"))
            if hub_url:
                req.hub_url = hub_url
            req.client_worker_id = bstack1ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤሤ").format(threading.get_ident(), os.getpid())
            logger.debug(bstack1ll111_opy_ (u"ࠦࡤࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡧࡩࡁࢀࡸࡥࡧࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶࡩࡾࠤሥ").format(
                ref=instance.ref(), pi=req.platform_index))
            response = cli.bstack1ll1lll11ll_opy_.DriverInit(req)
            if response and response.success:
                logger.debug(bstack1ll111_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠥሦ"))
                if response.capabilities:
                    try:
                        bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧሧ")))
                        if bstack1lll1111ll1_opy_:
                            bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll1l1l_opy_, bstack1lll1111ll1_opy_)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.debug(bstack1ll111_opy_ (u"ࠢࡠࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡀࠠࡼࡧࢀࠦረ").format(e=e))
                return response
            else:
                logger.debug(bstack1ll111_opy_ (u"ࠣࡡࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡶࡪࡺࡵࡳࡰࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸࡃࡆࡢ࡮ࡶࡩࠧሩ"))
                return None
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠤࡢࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࡨࢁࠧሪ").format(e=e))
            return None
    def _populate_browser_instance_data(self):
        bstack1ll111_opy_ (u"ࠥࠦࠧࡖ࡯ࡱࡷ࡯ࡥࡹ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬ࠡࡣࡱࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡲࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠠࡧࡱࡵࠤࡷࡵࡢࡰࡶ࠰ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠮ࠣࠤࠥራ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1lllllll_opy_
            from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
            if not self._1ll1llll1l1_opy_():
                logger.debug(bstack1ll111_opy_ (u"ࠦࡤࡶ࡯ࡱࡷ࡯ࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡢࡨࡦࡺࡡ࠻ࠢࡱࡳࠥࡧࡣࡵ࡫ࡹࡩࠥࡶࡡࡨࡧ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨሬ"))
                return
            if not self._1lll1111lll_opy_:
                response = self._call_driver_init()
                self._1lll1111lll_opy_ = True
                if response and response.success:
                    logger.debug(bstack1ll111_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠤር"))
            result = self._1ll1llll11l_opy_(bstack1ll111_opy_ (u"࠭ࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠪሮ"), {})
            logger.debug(bstack1ll111_opy_ (u"ࠢࡠࡲࡲࡴࡺࡲࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡤࡢࡶࡤ࠾ࠥ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠢࡵࡩࡸࡻ࡬ࡵ࠿ࡾࡶࢂࠨሯ").format(r=result))
            if not result:
                logger.debug(bstack1ll111_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦ࡮ࡰࠢࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠦሰ"))
                return
            bstack1lll111l111_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack1lll111l111_opy_.get(bstack1ll111_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬሱ"), bstack1ll111_opy_ (u"ࠪࠫሲ"))
            hub_url = os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡔࡈࡏࡕࡡࡓ࡛ࡤࡉࡄࡑࡡࡘࡖࡑ࠭ሳ"), bstack1ll111_opy_ (u"ࠬ࠭ሴ"))
            logger.debug(bstack1ll111_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࡽࡶ࡭ࡩࢃࠬࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࡾࡹࡷࡲࡽࠣስ").format(sid=session_id, url=hub_url[:80] if hub_url else bstack1ll111_opy_ (u"ࠧࠨሶ")))
            current_test_id = getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪሷ"), None)
            for instance in bstack1ll1lllllll_opy_.bstack1ll1llllll1_opy_.values():
                if not bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll111l_opy_, None):
                    bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll111l_opy_, session_id)
                    bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1lll111l1ll_opy_, hub_url)
                    if current_test_id:
                        bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪሸ"), current_test_id)
                    logger.debug(bstack1ll111_opy_ (u"ࠥࡔࡴࡶࡵ࡭ࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠼ࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࡼࡵ࡬ࡨࢂ࠲ࠠࡩࡷࡥࡣࡺࡸ࡬ࠡࡵࡨࡸ࠱ࠦࡴࡦࡵࡷࡣ࡮ࡪ࠽ࡼࡶ࡬ࡨࢂࠨሹ").format(
                        sid=session_id, tid=current_test_id))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱࡳࡹࡱࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡪࡡࡵࡣ࠽ࠤࢀ࡫ࡽࠣሺ").format(e=e))
    def _clear_session_data(self):
        bstack1ll111_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬ࡲࡰ࡯ࠣࡥࡱࡲࠠࡣࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࠤࡹࡵࠠࡦࡰࡶࡹࡷ࡫ࠠࡵࡧࡶࡸࠥ࡯ࡳࡰ࡮ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨሻ")
        try:
            from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1lllllll_opy_
            from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
            bstack1lll11l1ll1_opy_ = 0
            for instance in bstack1ll1lllllll_opy_.bstack1ll1llllll1_opy_.values():
                bstack1lll11111l1_opy_ = False
                if bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll111l_opy_, None):
                    bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1ll1lll111l_opy_, bstack1ll111_opy_ (u"࠭ࠧሼ"))
                    bstack1lll11111l1_opy_ = True
                if bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1lll111l1ll_opy_, None):
                    bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1lll111l1l1_opy_.bstack1lll111l1ll_opy_, bstack1ll111_opy_ (u"ࠧࠨሽ"))
                    bstack1lll11111l1_opy_ = True
                if bstack1lll111l1l1_opy_.bstack1lll111lll1_opy_(instance, bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡩࡥࠩሾ"), None):
                    bstack1lll111l1l1_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡪࡦࠪሿ"), None)
                    bstack1lll11111l1_opy_ = True
                if bstack1lll11111l1_opy_:
                    bstack1lll11l1ll1_opy_ += 1
            logger.debug(bstack1ll111_opy_ (u"ࠥࡣࡨࡲࡥࡢࡴࡢࡷࡪࡹࡳࡪࡱࡱࡣࡩࡧࡴࡢ࠼ࠣࡇࡱ࡫ࡡࡳࡧࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡽࡱࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠣቀ").format(
                n=bstack1lll11l1ll1_opy_))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤ࡮ࡨࡥࡷࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡣࡷࡥ࠿ࠦࡻࡦࡿࠥቁ").format(e=e))
    def _1lll111llll_opy_(self, status, reason=bstack1ll111_opy_ (u"ࠧࠨቂ")):
        bstack1ll111_opy_ (u"ࠨࠢࠣࡏࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦቃ")
        bstack1ll1lll11l1_opy_ = bstack1ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢቄ") if status == bstack1ll111_opy_ (u"ࠣࡒࡄࡗࡘࠨቅ") else bstack1ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤቆ")
        if bstack1ll1lll11l1_opy_ == bstack1ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥቇ"):
            return self._1ll1llll11l_opy_(bstack1ll111_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢቈ"), {
                bstack1ll111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ቉"): bstack1ll1lll11l1_opy_,
                bstack1ll111_opy_ (u"ࠨࡲࡦࡣࡶࡳࡳࠨቊ"): reason
            })
        else:
            return self._1ll1llll11l_opy_(bstack1ll111_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥቋ"), {
                bstack1ll111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣቌ"): bstack1ll1lll11l1_opy_
            })
    def _1ll1lll1l11_opy_(self, name):
        bstack1ll111_opy_ (u"ࠤࠥࠦࡘ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤࠥࠦቍ")
        return self._1ll1llll11l_opy_(bstack1ll111_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ቎"), {
            bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ቏"): name
        })
    def _1ll1lllll1l_opy_(self):
        bstack1ll111_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡣࡧࡩࡳࡷ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡥ࡯ࡳࡸ࡫ࠠࡰࡴࠣࡸࡪࡧࡲࡥࡱࡺࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡶࡤࡸࡺࡹࠠࡪࡵࠣ࡭ࡳ࡬ࡥࡳࡴࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡣࡱࡧࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦ࠼ࠣ࡭࡫ࠦࡡ࡯ࡻࠣࡊࡆࡏࡌ࠮࡮ࡨࡺࡪࡲࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡢࡵࠣࡧࡦࡶࡴࡶࡴࡨࡨࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡷࡩࡸࡺࠬࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣ࡭ࡸࠦࡦࡢ࡫࡯࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧቐ")
        if self._1lll111l11l_opy_:
            return
        try:
            global_config = Config.get_instance()
            if self._1ll1lllll11_opy_ and not global_config.should_skip_session_name():
                self._1ll1lll1l11_opy_(self._1ll1lllll11_opy_)
            status = bstack1ll111_opy_ (u"࠭ࡆࡂࡋࡏࠫቑ") if self._1lll11l11ll_opy_ else bstack1ll111_opy_ (u"ࠧࡑࡃࡖࡗࠬቒ")
            message = self._1lll11l11ll_opy_ or bstack1ll111_opy_ (u"ࠨࠩቓ")
            if not global_config.should_skip_session_status():
                logger.debug(bstack1ll111_opy_ (u"ࠤࡐࡥࡷࡱࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡨࡲ࡯ࡴࡧ࠽ࠤࡸࡺࡡࡵࡷࡶࡁࢀࡹࡴࡢࡶࡸࡷࢂ࠲ࠠ࡮ࡧࡶࡷࡦ࡭ࡥ࠾ࡽࡰࡩࡸࡹࡡࡨࡧࢀࠦቔ").format(status=status, message=message))
                self._1lll111llll_opy_(status, message)
            self._1lll111l11l_opy_ = True
            logger.debug(bstack1ll111_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡰࡥࡷࡱࡥࡥࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤቕ"))
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡧࢀࠦቖ").format(e=e))
    def _extract_screenshot_base64(self, bstack1lll111ll1l_opy_):
        bstack1ll111_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡌ࡙ࡓࡌࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡲࡦࡴࡺࠧࡴࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡱࡵࡧࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠠࡢࡵࠣࡌ࡙ࡓࡌࠡࡹ࡬ࡸ࡭ࠦࡥࡪࡶ࡫ࡩࡷࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡨࡥࡥࡦࡨࡨ࠿ࠦ࠼ࡪ࡯ࡪࠤࡸࡸࡣ࠾ࠤࡧࡥࡹࡧ࠺ࡪ࡯ࡤ࡫ࡪ࠵ࡰ࡯ࡩ࠾ࡦࡦࡹࡥ࠷࠶࠯ࡿࡩࡧࡴࡢࡿࠥࠤ࠳࠴࠮࠿ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌࡩ࡭ࡧࠣࡰ࡮ࡴ࡫࠻ࠢ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧࡶࡡࡵࡪ࠲ࡸࡴ࠵ࡦࡪ࡮ࡨ࠲ࡵࡴࡧࠣࠢ࠱࠲࠳ࡄࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ቗")
        match = re.search(bstack1ll111_opy_ (u"ࡸࠧࡴࡴࡦࡁࠧࡪࡡࡵࡣ࠽࡭ࡲࡧࡧࡦ࠱ࡳࡲ࡬ࡁࡢࡢࡵࡨ࠺࠹࠲ࠨ࡜ࡠࠥࡡ࠰࠯ࠢࠨቘ"), bstack1lll111ll1l_opy_)
        if match:
            return match.group(1)
        match = re.search(bstack1ll111_opy_ (u"ࡲࠨ࠾࡬ࡱ࡬ࡡ࡞࠿࡟࠮ࡷࡷࡩ࠽ࠣࠪ࡞ࡢࠧࡣࠫ࡝࠰ࠫࡃ࠿ࡶ࡮ࡨࡾ࡭ࡴ࡬ࢂࡪࡱࡧࡪ࠭࠮ࠨࠧ቙"), bstack1lll111ll1l_opy_)
        if match:
            file_path = match.group(1)
            try:
                from pathlib import Path
                path = Path(file_path)
                if not path.is_absolute():
                    bstack1ll1lll1111_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠨࡔࡒࡆࡔ࡚࡟ࡐࡗࡗࡔ࡚࡚࡟ࡅࡋࡕࠫቚ"), os.getcwd())
                    path = Path(bstack1ll1lll1111_opy_) / path
                if path.is_file():
                    with open(path, bstack1ll111_opy_ (u"ࠩࡵࡦࠬቛ")) as f:
                        return base64.b64encode(f.read()).decode(bstack1ll111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩቜ"))
            except Exception as e:
                logger.debug(bstack1ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡳࡧࡤࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡩ࡭ࡱ࡫ࠠࡼࡲࡤࡸ࡭ࢃ࠺ࠡࡽࡨࢁࠧቝ").format(path=file_path, e=e))
        return None
    def start_test(self, name, attrs):
        if cli.is_running():
            self._1ll1lll1ll1_opy_ = False
            self._1lll111l11l_opy_ = False
            self._1ll1lllll11_opy_ = name
            self._1lll11l11ll_opy_ = None
            self._1lll1111lll_opy_ = False
            threading.current_thread().current_test_uuid = attrs.get(bstack1ll111_opy_ (u"ࠬ࡯ࡤࠨ቞"), None)
            threading.current_thread().current_test_id = attrs.get(bstack1ll111_opy_ (u"࠭ࡩࡥࠩ቟"), None)
            self._clear_session_data()
            bstack1lllll1111l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, bstack1lllll1111l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, bstack1lllll1111l_opy_)
            return
        logger.debug(bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡴࡦࡵࡷࠤࡈࡇࡌࡍࡇࡇࠤ࠲ࠦࡴࡦࡵࡷ࠾ࠥࢁ࡮ࡢ࡯ࡨࢁࠧበ").format(name=name))
        self._1ll1lll1ll1_opy_ = False
        self._1lll111l11l_opy_ = False
        self._1ll1lllll11_opy_ = name
        self._1lll11l11ll_opy_ = None
    def end_test(self, name, attrs):
        if cli.is_running():
            self._populate_browser_instance_data()
            bstack1lllll1111l_opy_ = SimpleNamespace(name=name, **attrs)
            bstack1ll1lll1lll_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨቡ")),
                message=attrs.get(bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪቢ"), bstack1ll111_opy_ (u"ࠪࠫባ")),
                starttime=attrs.get(bstack1ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠧቤ"), bstack1ll111_opy_ (u"ࠬ࠭ብ")),
                endtime=attrs.get(bstack1ll111_opy_ (u"࠭ࡥ࡯ࡦࡷ࡭ࡲ࡫ࠧቦ"), bstack1ll111_opy_ (u"ࠧࠨቧ")),
                elapsedtime=attrs.get(bstack1ll111_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ቨ"), 0)
            )
            cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, bstack1lllll1111l_opy_)
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, bstack1lllll1111l_opy_, bstack1ll1lll1lll_opy_)
        status = attrs.get(bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩቩ"), bstack1ll111_opy_ (u"࡙ࠪࡓࡑࡎࡐ࡙ࡑࠫቪ"))
        message = attrs.get(bstack1ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬቫ"), bstack1ll111_opy_ (u"ࠬ࠭ቬ"))
        logger.debug(bstack1ll111_opy_ (u"ࠨࡥ࡯ࡦࡢࡸࡪࡹࡴࠡࡅࡄࡐࡑࡋࡄࠡ࠯ࠣࡸࡪࡹࡴ࠻ࠢࡾࡲࡦࡳࡥࡾ࠮ࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࡹࡴࡢࡶࡸࡷࢂࠨቭ").format(name=name, status=status))
        self._1ll1lll1ll1_opy_ = True
        if not self._1lll111l11l_opy_ and self._1ll1llll1l1_opy_():
            try:
                global_config = Config.get_instance()
                if not global_config.should_skip_session_name():
                    self._1ll1lll1l11_opy_(name)
                if not global_config.should_skip_session_status():
                    logger.debug(bstack1ll111_opy_ (u"ࠢࡎࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡲࠥ࡫࡮ࡥࡡࡷࡩࡸࡺ࠺ࠡࡵࡷࡥࡹࡻࡳ࠾ࡽࡶࡸࡦࡺࡵࡴࡿࠥቮ").format(status=status))
                    self._1lll111llll_opy_(status, message)
                self._1lll111l11l_opy_ = True
                logger.debug(bstack1ll111_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቯ"))
            except Exception as e:
                logger.error(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࠠࡦࡰࡧࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡪࢃࠢተ").format(e=e))
        elif self._1lll111l11l_opy_:
            logger.debug(bstack1ll111_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤࡦࡲࡲࡦࡣࡧࡽࠥࡳࡡࡳ࡭ࡨࡨࠧቱ"))
        else:
            logger.debug(bstack1ll111_opy_ (u"ࠦࡓࡵࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡱࡣࡪࡩࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠢቲ"))
    def start_suite(self, name, attrs):
        bstack1ll111_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡽࡨࡦࡰࠣࡥࠥࡹࡵࡪࡶࡨࠤࡸࡺࡡࡳࡶࡶࠦࠧࠨታ")
        if cli.is_running():
            threading.current_thread().current_suite_id = attrs.get(bstack1ll111_opy_ (u"࠭ࡩࡥࠩቴ"), None)
            bstack1lll11l111l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, bstack1lll11l111l_opy_)
            return
        logger.debug(bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢት").format(name=name))
    def end_suite(self, name, attrs):
        bstack1ll111_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡹ࡫ࡩࡳࠦࡡࠡࡵࡸ࡭ࡹ࡫ࠠࡦࡰࡧࡷࠧࠨࠢቶ")
        if cli.is_running():
            bstack1lll11l111l_opy_ = SimpleNamespace(name=name, **attrs)
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_ALL, TestHookState.POST, bstack1lll11l111l_opy_)
            return
        logger.debug(bstack1ll111_opy_ (u"ࠤࡨࡲࡩࡥࡳࡶ࡫ࡷࡩࠥࡉࡁࡍࡎࡈࡈࠥ࠳ࠠࡴࡷ࡬ࡸࡪࡀࠠࡼࡰࡤࡱࡪࢃࠢቷ").format(name=name))
    def start_keyword(self, name, attrs):
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧቸ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ቹ"), None)
            if attrs.get(bstack1ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪቺ"), bstack1ll111_opy_ (u"࠭ࠧቻ")).lower() in [bstack1ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ቼ"), bstack1ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪች")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧቾ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                bstack1ll1ll1ll1l_opy_ = SimpleNamespace(name=attrs.get(bstack1ll111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪቿ"), name), id=current_test_id, **attrs)
                cli.test_framework.track_event(cli_context, state, TestHookState.PRE, bstack1ll1ll1ll1l_opy_)
            else:
                if current_test_id:
                    bstack1ll1ll1ll1l_opy_ = SimpleNamespace(name=attrs.get(bstack1ll111_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫኀ"), name), id=current_test_id, **attrs)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, bstack1ll1ll1ll1l_opy_, test_id=current_test_id)
        if self._1lll111l11l_opy_ or self._1ll1lll1ll1_opy_:
            return
        bstack1lll1111l1l_opy_ = False
        bstack1lll11l1l11_opy_ = attrs.get(bstack1ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪኁ"), bstack1ll111_opy_ (u"࠭ࠧኂ")).lower()
        if name.lower() in self._CLOSE_KEYWORDS:
            bstack1lll1111l1l_opy_ = True
            logger.debug(bstack1ll111_opy_ (u"ࠢࡄ࡮ࡲࡷࡪࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࡿࡳࡧ࡭ࡦࡿ࠯ࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡢࡦࡨࡲࡶࡪࠦࡩࡵࠢࡨࡼࡪࡩࡵࡵࡧࡶࠦኃ").format(name=name))
        elif bstack1lll11l1l11_opy_ == bstack1ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪኄ"):
            bstack1lll1111l1l_opy_ = True
            logger.debug(bstack1ll111_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬࠲ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡷࡩࡦࡸࡤࡰࡹࡱࠤࡪࡾࡥࡤࡷࡷࡩࡸࠨኅ"))
        if bstack1lll1111l1l_opy_ and self._1ll1llll1l1_opy_():
            self._populate_browser_instance_data()
            self._1ll1lllll1l_opy_()
    def end_keyword(self, name, attrs):
        bstack1ll111_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡥ࡫ࡺࡥࡳࠢࡤࠤࡰ࡫ࡹࡸࡱࡵࡨࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡳ࠯ࠤࠥࠦኆ")
        if cli.is_running():
            current_test_uuid = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨኇ"), None)
            current_test_id = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧኈ"), None)
            bstack1ll1ll1ll1l_opy_ = SimpleNamespace(name=attrs.get(bstack1ll111_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭኉"), name), id=current_test_id, **attrs)
            bstack1ll1lll1lll_opy_ = SimpleNamespace(
                status=attrs.get(bstack1ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧኊ")),
                message=attrs.get(bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩኋ"), bstack1ll111_opy_ (u"ࠩࠪኌ")),
                starttime=attrs.get(bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡶ࡬ࡱࡪ࠭ኍ"), bstack1ll111_opy_ (u"ࠫࠬ኎")),
                endtime=attrs.get(bstack1ll111_opy_ (u"ࠬ࡫࡮ࡥࡶ࡬ࡱࡪ࠭኏"), bstack1ll111_opy_ (u"࠭ࠧነ")),
                elapsedtime=attrs.get(bstack1ll111_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬኑ"), 0)
            )
            if attrs.get(bstack1ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ኒ"), bstack1ll111_opy_ (u"ࠩࠪና")).lower() in [bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩኔ"), bstack1ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ን")]:
                hook_type = self._get_hook_type_for_method(attrs.get(bstack1ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪኖ")), current_test_uuid)
                state = TestFrameworkState[hook_type]
                cli.test_framework.track_event(cli_context, state, TestHookState.POST, bstack1ll1ll1ll1l_opy_, bstack1ll1lll1lll_opy_)
            else:
                if current_test_id:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, bstack1ll1ll1ll1l_opy_, bstack1ll1lll1lll_opy_, test_id=current_test_id)
            if (name.lower() in self._BROWSER_OPEN_KEYWORDS
                    and attrs.get(bstack1ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ኗ"), bstack1ll111_opy_ (u"ࠧࠨኘ")).upper() == bstack1ll111_opy_ (u"ࠨࡒࡄࡗࡘ࠭ኙ")):
                logger.debug(bstack1ll111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࠣࡳࡵ࡫࡮ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨ࠿ࠦࡻ࡯ࡣࡰࡩࢂ࠲ࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡪࡡࡵࡣࠥኚ").format(name=name))
                self._populate_browser_instance_data()
    def log_message(self, message):
        bstack1ll111_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡪࡴࡸࠠࡦࡸࡨࡶࡾࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡢࡲࡷࡹࡷ࡫ࡳࠡࡈࡄࡍࡑࠦ࡬ࡦࡸࡨࡰࠥࡳࡥࡴࡵࡤ࡫ࡪࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡢࡵࠣࡩࡷࡸ࡯ࡳࠢࡵࡩࡦࡹ࡯࡯࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡯࡮ࡤࡧࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡺࡴࡳࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤ࡮ࡴࡣ࡭ࡷࡧࡩࠥࡺࡨࡦࠢࡨࡶࡷࡵࡲࠡ࡯ࡨࡷࡸࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢኛ")
        if cli.is_running():
            try:
                if message.get(bstack1ll111_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩኜ"), bstack1ll111_opy_ (u"ࠬࡴ࡯ࠨኝ")) == bstack1ll111_opy_ (u"࠭ࡹࡦࡵࠪኞ"):
                    screenshot_base64 = self._extract_screenshot_base64(message.get(bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨኟ"), bstack1ll111_opy_ (u"ࠨࠩአ")))
                    if screenshot_base64 and cli.is_screenshots_allowed():
                        msg_obj = SimpleNamespace(
                            message=screenshot_base64,
                            kind=bstack1ll111_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ኡ"),
                            level=bstack1ll111_opy_ (u"ࠪࡍࡓࡌࡏࠨኢ"),
                            timestamp=message.get(bstack1ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧኣ"), None)
                        )
                        current_test_id = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧኤ"), None)
                        cli.test_framework.track_event(
                            cli_context, TestFrameworkState.LOG, TestHookState.POST,
                            msg_obj, test_id=current_test_id
                        )
                else:
                    msg_obj = SimpleNamespace(
                        message=message.get(bstack1ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧእ"), bstack1ll111_opy_ (u"ࠧࠨኦ")),
                        level=message.get(bstack1ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧኧ"), bstack1ll111_opy_ (u"ࠩࡌࡒࡋࡕࠧከ")),
                        timestamp=message.get(bstack1ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ኩ"), None)
                    )
                    current_test_id = threading.current_thread().__dict__.get(bstack1ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ኪ"), None)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, msg_obj, test_id=current_test_id)
            except:
                pass
        level = message.get(bstack1ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫካ"), bstack1ll111_opy_ (u"࠭ࠧኬ"))
        if level == bstack1ll111_opy_ (u"ࠧࡇࡃࡌࡐࠬክ"):
            self._1lll11l11ll_opy_ = message.get(bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩኮ"), bstack1ll111_opy_ (u"ࠩࠪኯ"))
            logger.debug(bstack1ll111_opy_ (u"ࠥࡇࡦࡶࡴࡶࡴࡨࡨࠥ࡫ࡲࡳࡱࡵࠤࡲ࡫ࡳࡴࡣࡪࡩ࠿ࠦࡻࡦࡴࡵࡳࡷࢃࠢኰ").format(error=self._1lll11l11ll_opy_))
    def _get_hook_type_for_method(self, hook_type, current_test_uuid):
        bstack1ll111_opy_ (u"ࠦࠧࠨࡄࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡬ࡪࠥࡹࡥࡵࡷࡳ࠳ࡹ࡫ࡡࡳࡦࡲࡻࡳࠦࡩࡴࠢࡶࡹ࡮ࡺࡥ࠮࡮ࡨࡺࡪࡲࠠࡰࡴࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲ࠮ࠣࠤࠥ኱")
        if hook_type.lower() == bstack1ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫኲ"):
            return bstack1ll111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪኳ") if current_test_uuid is None else bstack1ll111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬኴ")
        elif hook_type.lower() == bstack1ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪኵ"):
            return bstack1ll111_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ኶") if current_test_uuid is None else bstack1ll111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ኷")