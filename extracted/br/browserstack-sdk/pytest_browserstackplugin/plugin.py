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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import performance_tester
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1ll1l11ll1l_opy_, update, bstack1llll11ll11_opy_,
                                       bstack1l1lll11l11_opy_, bstack111l11lll1_opy_, bstack1ll11llll11_opy_, bstack1ll11l1l1l_opy_,
                                       bstack1lllll111l_opy_, bstack1ll1l1lll1_opy_, bstack1l1lll1111l_opy_,
                                       bstack1l1l11l1ll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11l1l1ll_opy_)
from browserstack_sdk.bstack11ll11l1l_opy_ import bstack11llll11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack111ll1l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack111l11l111_opy_, bstack1l1l1ll1l11_opy_, bstack1111ll111l_opy_, \
    bstack1l111lll1l_opy_
from bstack_utils.helper import bstack11llll11_opy_, bstack1lll1lll1l11_opy_, bstack1llllllll_opy_, bstack1l1111l1ll_opy_, is_bstack_automation, bstack1l1111ll_opy_, \
    bstack1lll11ll11l1_opy_, \
    bstack1llll1ll11l1_opy_, bstack1l1ll11111_opy_, bstack1l1l111ll11_opy_, bstack1llll1l11lll_opy_, bstack1llll1l11l1_opy_, Notset, \
    bstack11l1ll1111_opy_, bstack1ll1l11ll_opy_, bstack1lll1l1l1l11_opy_, Result, bstack1lll1ll111l1_opy_, bstack1llll1111l11_opy_, error_handler, \
    bstack1lll11l111_opy_, bstack11l1ll11ll_opy_, bstack11lll11l1l_opy_, bstack1lll1l1lll1l_opy_
from bstack_utils.bstack1lll111l1lll_opy_ import bstack1lll111ll1l1_opy_
from bstack_utils.messages import bstack1lllllll11l_opy_, bstack1lllll11l11_opy_, bstack1llll1llll1_opy_, bstack11llll1lll_opy_, bstack11llllll1_opy_, \
    bstack1ll1l1l1l1_opy_, bstack1ll1ll1l1l_opy_, CONFIG_FILE_CONTENT, bstack11l1l1ll1l_opy_, bstack1l1ll1ll1l_opy_, \
    bstack1ll11111l1l_opy_, bstack11l1llll11_opy_, bstack111ll1111l_opy_
from bstack_utils.proxy import bstack1l111ll111_opy_, bstack1ll1ll1111l_opy_
from bstack_utils.bstack111111l11l_opy_ import bstack1ll111ll1l1l_opy_, bstack1ll111ll1lll_opy_, bstack1ll111lll1l1_opy_, bstack1ll111ll11l1_opy_, \
    bstack1ll111llll11_opy_, bstack1ll111lllll1_opy_, bstack1ll111ll11ll_opy_, bstack1lll11l11l_opy_, bstack1ll111lll111_opy_
from bstack_utils.bstack1ll1l1lll1l_opy_ import bstack1llllllllll_opy_
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1lll111ll_opy_, bstack1l1l1llll1l_opy_, update_caps_for_local, \
    bstack1l1lll1ll1l_opy_, bstack1lll1111l1l_opy_
from bstack_utils.test_data import bstack1l1l1111_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111l_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.module_event_dispatcher import EventDispatcherModule
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack111ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFrameworkContext, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack111ll11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack111111ll1l_opy_ import FileUploader
from browserstack_sdk.sdk_cli.utils.custom_tag_manager import CustomTagManager
bstack1l1l1l111l1_opy_ = None
bstack1lllll11111_opy_ = None
bstack1111l1l1l1_opy_ = None
bstack11l1l1l1l1_opy_ = None
bstack111lll1l11_opy_ = None
bstack1llllll111l_opy_ = None
bstack11l1l11l1l_opy_ = None
bstack11l11ll1ll_opy_ = None
bstack11l1111111_opy_ = None
bstack111l111l11_opy_ = None
bstack1l111l1ll1_opy_ = None
bstack111l1lll11_opy_ = None
bstack1llllll1lll_opy_ = None
FRAMEWORK_NAME = bstack1l1llll_opy_ (u"ࠨࠩⶤ")
CONFIG = {}
bstack11ll111lll_opy_ = False
bstack1lll1ll1l11_opy_ = bstack1l1llll_opy_ (u"ࠩࠪⶥ")
bstack1ll1ll111ll_opy_ = bstack1l1llll_opy_ (u"ࠪࠫⶦ")
PARALLELISE_VANILLA_PYTHON = False
bstack1111ll11l_opy_ = []
bstack1l1111l111_opy_ = bstack111l11l111_opy_
bstack1l1ll111l1l1_opy_ = bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⶧")
bstack1ll1ll11111_opy_ = {}
SESSION_NAME = None
bstack11lll1llll_opy_ = False
logger = logger_utils.get_logger(__name__, bstack1l1111l111_opy_)
store = {
    bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩⶨ"): []
}
bstack1l1l1llll111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1llll11ll_opy_ = {}
current_test_uuid = None
cli_context = TestFrameworkContext(
    test_framework_name=bstack1ll11lll1ll_opy_[bstack1l1llll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪⶩ")] if bstack1llll1l11l1_opy_() else bstack1ll11lll1ll_opy_[bstack1l1llll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧⶪ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack1l1ll11l1ll_opy_):
    try:
        page.evaluate(bstack1l1llll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤⶫ"),
                      bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ⶬ") + json.dumps(
                          bstack1l1ll11l1ll_opy_) + bstack1l1llll_opy_ (u"ࠥࢁࢂࠨⶭ"))
    except Exception as e:
        print(bstack1l1llll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤⶮ"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1l1llll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⶯"), bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫⶰ") + json.dumps(
            message) + bstack1l1llll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪⶱ") + json.dumps(level) + bstack1l1llll_opy_ (u"ࠨࡿࢀࠫⶲ"))
    except Exception as e:
        print(bstack1l1llll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧⶳ"), e)
def _1l1l1lll1l11_opy_():
    bstack1l1llll_opy_ (u"ࠥࠦࠧ࡝ࡡ࡭࡭ࠣࡇ࡜ࡊࠠࡶࡲࡺࡥࡷࡪࠠ࡭ࡱࡲ࡯࡮ࡴࡧࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬࠯ࠤࠥࠦⶴ")
    bstack1l1l1llll1ll_opy_ = os.getcwd()
    while True:
        for name in (bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧⶵ"), bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠩⶶ")):
            candidate = os.path.join(bstack1l1l1llll1ll_opy_, name)
            if os.path.exists(candidate):
                return candidate
        parent = os.path.dirname(bstack1l1l1llll1ll_opy_)
        if parent == bstack1l1l1llll1ll_opy_:
            break
        bstack1l1l1llll1ll_opy_ = parent
    return None
def _1l1ll11l11ll_opy_():
    bstack1l1llll_opy_ (u"ࠨࠢࠣࡆࡨࡸࡪࡩࡴࠡ࡫ࡩࠤࡵࡿࡴࡦࡵࡷࠤࡼࡧࡳࠡ࡮ࡤࡹࡳࡩࡨࡦࡦࠣࡦࡾࠦࡡ࡯ࠢࡌࡈࡊࠦࡲࡶࡰࡱࡩࡷ࠴ࠊࠡࠢࠣࠤ࡚ࡹࡥࡴࠢࡶࡸࡦࡨ࡬ࡦ࠮ࠣࡰࡴࡴࡧ࠮࡮࡬ࡺࡪࡪࠠࡦࡰࡹࠤࡻࡧࡲࡴࠢࡶࡩࡹࠦࡡࡶࡶࡲࡱࡦࡺࡩࡤࡣ࡯ࡰࡾࠦࡢࡺࠢࡌࡈࡊࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࡑ࡛ࡆࡌࡆࡘࡍࡠࡊࡒࡗ࡙ࡋࡄࠡࠢࠣࠤ⠙ࠦࡊࡦࡶࡅࡶࡦ࡯࡮ࡴࠢࡓࡽࡈ࡮ࡡࡳ࡯ࠣࠬࢃ࠸࠰࠲࠵࠮࠭ࠏࠦࠠࠡࠢࠣࠤ࡙ࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠠࠡ⠖ࠣࡎࡪࡺࡂࡳࡣ࡬ࡲࡸࠦࡉࡅࡇࡶࠤࡻ࡯ࡡࠡࡖࡨࡥࡲࡉࡩࡵࡻࠣࡴࡷࡵࡴࡰࡥࡲࡰࠥ࠮࠱࠱࠭ࠣࡽࡪࡧࡲࡴࠫࠍࠤࠥࠦࠠࠣࠤࠥ⶷")
    return os.environ.get(bstack1l1llll_opy_ (u"ࠧࡑ࡛ࡆࡌࡆࡘࡍࡠࡊࡒࡗ࡙ࡋࡄࠨⶸ")) == bstack1l1llll_opy_ (u"ࠨ࠳ࠪⶹ") or \
           bool(os.environ.get(bstack1l1llll_opy_ (u"ࠩࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠬⶺ")))
def pytest_configure(config):
    global bstack1lll1ll1l11_opy_
    global CONFIG
    global bstack11ll111lll_opy_
    if not os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠧⶻ")) and _1l1ll11l11ll_opy_():
        _1l1ll11l1ll1_opy_ = _1l1l1lll1l11_opy_()
        if _1l1ll11l1ll1_opy_:
            try:
                from browserstack_sdk import bstack1lll1l11lll_opy_
                if bstack1lll1l11lll_opy_(_1l1ll11l1ll1_opy_):
                    CONFIG = json.loads(os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪⶼ"), bstack1l1llll_opy_ (u"ࠬࢁࡽࠨⶽ")))
                    bstack1lll1ll1l11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ⶾ"), bstack1l1llll_opy_ (u"ࠧࠨ⶿"))
                    bstack11ll111lll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩⷀ"), bstack1l1llll_opy_ (u"ࠩࡉࡥࡱࡹࡥࠨⷁ")).lower() == bstack1l1llll_opy_ (u"ࠪࡸࡷࡻࡥࠨⷂ")
            except Exception as e:
                logger.error(bstack1l1llll_opy_ (u"ࠦࡕࡲࡵࡨ࡫ࡱࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦⷃ").format(e))
    global_config = Config.bstack1lll1l11_opy_()
    config.args = bstack1ll111ll_opy_.bstack1l1ll1ll1lll_opy_(config.args)
    global_config.bstack1ll111llll1_opy_(bstack11lll11l1l_opy_(config.getoption(bstack1l1llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩⷄ"))))
    try:
        logger_utils.bstack1ll1llll1l11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack111ll11ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ⷅ"), bstack1l1llll_opy_ (u"ࠧ࠱ࠩⷆ")))
        config = json.loads(os.environ.get(bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢ⷇"), bstack1l1llll_opy_ (u"ࠤࡾࢁࠧⷈ")))
        cli.bstack11lllllll11_opy_(bstack1l1l111ll11_opy_(bstack1lll1ll1l11_opy_, CONFIG), cli_context.platform_index, bstack1llll11ll11_opy_)
    if cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
        cli.bstack1ll11l111_opy_()
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤⷉ") + str(cli_context.platform_index) + bstack1l1llll_opy_ (u"ࠦࠧⷊ"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
def pytest_unconfigure(config):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࡓࡷࡱࠤࡘࡊࡋࠡࡥ࡯ࡩࡦࡴࡵࡱࠢࡺ࡬࡮ࡲࡥࠡࡲࡼࡸࡪࡹࡴࠡࠪࡤࡲࡩࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠩࠡ࡫ࡶࠤࡸࡺࡩ࡭࡮ࠣࡥࡱ࡯ࡶࡦ࠰ࠍࠤࠥࠦࠠࡊࡰࠣࡴࡱࡻࡧࡪࡰࠣࡱࡴࡪࡥ࠭ࠢࡥࡷࡹࡧࡣ࡬ࡡࡨࡼ࡮ࡺ࡟ࡩࡣࡱࡨࡱ࡫ࡲࠡࡨ࡬ࡶࡪࡹࠠࡢࡶࠣࡥࡹ࡫ࡸࡪࡶࠣࡦࡺࡺࠠࡣࡻࠣࡸ࡭࡫࡮ࠋࠢࠣࠤࠥࡶࡹࡵࡧࡶࡸࠥ࡮ࡡࡴࠢࡷࡳࡷࡴࠠࡥࡱࡺࡲࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠯ࠢࡕࡹࡳࡴࡩ࡯ࡩࠣ࡭ࡹࠦࡨࡦࡴࡨࠤࡪࡴࡳࡶࡴࡨࡷࠏࠦࠠࠡࠢࡷ࡬ࡪࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭ࠣࡥࡳࡪࠠࡔࡆࡎࠤࡷࡻ࡮ࠡࡧࡱࡨࡪࡪࠠ࡮ࡧࡶࡷࡦ࡭ࡥࡴࠢࡵࡩࡦࡩࡨࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡵࡲࡰࡪ࠴ࠢࠣࠤⷋ")
    if os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡄࡆࡡࡓࡐ࡚ࡍࡉࡏࡡࡐࡓࡉࡋࠧⷌ")) and cli.is_running():
        from browserstack_sdk import bstack1111l1111l_opy_
        bstack1111l1111l_opy_()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1llll_opy_ (u"ࠢࡸࡪࡨࡲࠧⷍ"), None)
    if cli.is_running() and when == bstack1l1llll_opy_ (u"ࠣࡥࡤࡰࡱࠨⷎ"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1l1llll_opy_ (u"ࠤࡦࡥࡱࡲࠢ⷏"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1llll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧⷐ")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥⷑ"), bstack1l1llll_opy_ (u"ࠧࢁࡽࠣⷒ")))
            if bstack11ll1111l_opy_.bstack11lll1l1l_opy_(config):
                bstack1ll11ll11l11_opy_ = bstack11ll1111l_opy_.bstack1l1111111_opy_(config)
                if item.execution_count > bstack1ll11ll11l11_opy_:
                    print(bstack1l1llll_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡶࡪࡺࡲࡪࡧࡶ࠾ࠥ࠭ⷓ"), report.nodeid, os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⷔ")))
                    bstack11ll1111l_opy_.bstack1ll1ll11ll1l_opy_(report.nodeid)
            else:
                print(bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠨⷕ"), report.nodeid, os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧⷖ")))
                bstack11ll1111l_opy_.bstack1ll1ll11ll1l_opy_(report.nodeid)
        else:
            print(bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡲࡤࡷࡸ࡫ࡤ࠻ࠢࠪ⷗"), report.nodeid, os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⷘ")))
    if cli.is_running():
        if when == bstack1l1llll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦⷙ"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
            try:
                report = outcome.get_result()
                bstack1l1ll11l1l11_opy_ = getattr(report, bstack1l1llll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢⷚ"), False)
                bstack1ll1l111ll11_opy_ = getattr(report, bstack1l1llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢⷛ"), False)
                if bstack1l1ll11l1l11_opy_ or bstack1ll1l111ll11_opy_:
                    cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, item)
                    cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
            except Exception as err:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡪࡳࡩࡵࠢࡶࡽࡳࡺࡨࡦࡶ࡬ࡧ࡚ࠥࡅࡔࡖࠣࡩࡻ࡫࡮ࡵࡵࠣࡪࡴࡸࠠ࡯ࡱࡱ࠱ࡵࡧࡳࡴࡧࡧࠤࡸ࡫ࡴࡶࡲ࠽ࠤࠪࡹࠢⷜ"), err)
        elif when == bstack1l1llll_opy_ (u"ࠤࡦࡥࡱࡲࠢⷝ"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1l1llll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧⷞ"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l1llll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⷟"))
    plugins = item.config.getoption(bstack1l1llll_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨⷠ"))
    report = outcome.get_result()
    os.environ[bstack1l1llll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩⷡ")] = report.nodeid
    bstack1l1l1lllll1l_opy_(item, call, report)
    if bstack1l1llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧⷢ") not in plugins or bstack1llll1l11l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1llll_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤⷣ"), None)
    page = getattr(item, bstack1l1llll_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣⷤ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1l1ll1111l1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1l1ll11111ll_opy_(item, report, summary, skipSessionName)
def bstack1l1ll1111l1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩⷥ") and report.skipped:
        bstack1ll111lll111_opy_(report)
    if report.when in [bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥⷦ"), bstack1l1llll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢⷧ")]:
        return
    if not is_bstack_automation():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1llll_opy_ (u"࠭ࡴࡳࡷࡨࠫⷨ")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬⷩ") + json.dumps(
                    report.nodeid) + bstack1l1llll_opy_ (u"ࠨࡿࢀࠫⷪ"))
        os.environ[bstack1l1llll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬⷫ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥⷬ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1llll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨⷭ")))
    bstack1ll1lll111l_opy_ = bstack1l1llll_opy_ (u"ࠧࠨⷮ")
    bstack1ll111lll111_opy_(report)
    if not passed:
        try:
            bstack1ll1lll111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1llll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨⷯ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1lll111l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1llll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤⷰ")))
        bstack1ll1lll111l_opy_ = bstack1l1llll_opy_ (u"ࠣࠤⷱ")
        if not passed:
            try:
                bstack1ll1lll111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1llll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤⷲ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1lll111l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧⷳ")
                    + json.dumps(bstack1l1llll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧⷴ"))
                    + bstack1l1llll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣⷵ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫⷶ")
                    + json.dumps(str(bstack1ll1lll111l_opy_))
                    + bstack1l1llll_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥⷷ")
                )
        except Exception as e:
            summary.append(bstack1l1llll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨⷸ").format(e))
def bstack1l1ll111l111_opy_(test_name, error_message):
    try:
        bstack1l1l1llll1l1_opy_ = []
        bstack1ll1l111l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩⷹ"), bstack1l1llll_opy_ (u"ࠪ࠴ࠬⷺ"))
        bstack1111lllll1_opy_ = {bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩⷻ"): test_name, bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫⷼ"): error_message, bstack1l1llll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬⷽ"): bstack1ll1l111l1_opy_}
        bstack1l1ll1111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬⷾ"))
        if os.path.exists(bstack1l1ll1111l11_opy_):
            with open(bstack1l1ll1111l11_opy_) as f:
                bstack1l1l1llll1l1_opy_ = json.load(f)
        bstack1l1l1llll1l1_opy_.append(bstack1111lllll1_opy_)
        with open(bstack1l1ll1111l11_opy_, bstack1l1llll_opy_ (u"ࠨࡹࠪⷿ")) as f:
            json.dump(bstack1l1l1llll1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ⸀") + str(e))
def bstack1l1ll11111ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1llll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⸁"), bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⸂")]:
        return
    if (str(skipSessionName).lower() != bstack1l1llll_opy_ (u"ࠬࡺࡲࡶࡧࠪ⸃")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1llll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⸄")))
    bstack1ll1lll111l_opy_ = bstack1l1llll_opy_ (u"ࠢࠣ⸅")
    bstack1ll111lll111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1lll111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1llll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⸆").format(e)
                )
        try:
            if passed:
                bstack1lll1111l1l_opy_(getattr(item, bstack1l1llll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⸇"), None), bstack1l1llll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ⸈"))
            else:
                error_message = bstack1l1llll_opy_ (u"ࠫࠬ⸉")
                if bstack1ll1lll111l_opy_:
                    playwright_annotate(item._page, str(bstack1ll1lll111l_opy_), bstack1l1llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ⸊"))
                    bstack1lll1111l1l_opy_(getattr(item, bstack1l1llll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⸋"), None), bstack1l1llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ⸌"), str(bstack1ll1lll111l_opy_))
                    error_message = str(bstack1ll1lll111l_opy_)
                else:
                    bstack1lll1111l1l_opy_(getattr(item, bstack1l1llll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⸍"), None), bstack1l1llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⸎"))
                bstack1l1ll111l111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1llll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ⸏").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1llll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ⸐"), default=bstack1l1llll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⸑"), help=bstack1l1llll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⸒"))
    parser.addoption(bstack1l1llll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ⸓"), default=bstack1l1llll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ⸔"), help=bstack1l1llll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ⸕"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1llll_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ⸖"), action=bstack1l1llll_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ⸗"), default=bstack1l1llll_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ⸘"),
                         help=bstack1l1llll_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ⸙"))
def log_handler(log):
    if not (log[bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⸚")] and log[bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⸛")].strip()):
        return
    active = bstack11llll1l_opy_()
    log = {
        bstack1l1llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⸜"): log[bstack1l1llll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⸝")],
        bstack1l1llll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⸞"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠬࡠࠧ⸟"),
        bstack1l1llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⸠"): log[bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⸡")],
    }
    if active:
        if active[bstack1l1llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⸢")] == bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⸣"):
            log[bstack1l1llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⸤")] = active[bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⸥")]
        elif active[bstack1l1llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⸦")] == bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࠫ⸧"):
            log[bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⸨")] = active[bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⸩")]
    TestHubHandler.bstack1ll11111_opy_([log])
def bstack11llll1l_opy_():
    if len(store[bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⸪")]) > 0 and store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⸫")][-1]:
        return {
            bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⸬"): bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⸭"),
            bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⸮"): store[bstack1l1llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫⸯ")][-1]
        }
    if store.get(bstack1l1llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⸰"), None):
        return {
            bstack1l1llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⸱"): bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࠨ⸲"),
            bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⸳"): store[bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⸴")]
        }
    return None
def pytest_collection_modifyitems(config, items):
    if not cli.is_running():
        return
    bstack1l1ll11l1lll_opy_ = set()
    for item in items:
        cls = getattr(item, bstack1l1llll_opy_ (u"ࠨࡣ࡭ࡵࠥ⸵"), None)
        if cls is None or cls in bstack1l1ll11l1lll_opy_:
            continue
        bstack1l1ll11l1lll_opy_.add(cls)
        try:
            if not hasattr(cls, bstack1l1llll_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ⸶")):
                cls.upload_attachment = staticmethod(FileUploader.upload_attachment)
            if not hasattr(cls, bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࡤࡩࡵࡴࡶࡲࡱࡤࡺࡡࡨࠤ⸷")):
                cls.set_custom_tag = staticmethod(CustomTagManager.set_custom_tag)
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏ࠿ࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡳࡥࡹࡩࡨࠡࡥ࡯ࡥࡸࡹࠠࠦࡵ࠽ࠤࠪࡹࠢ⸸"), getattr(cls, bstack1l1llll_opy_ (u"ࠥࡣࡤࡴࡡ࡮ࡧࡢࡣࠧ⸹"), cls), e)
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        try:
            bstack1l1ll111l1ll_opy_ = item.nodeid + bstack1l1llll_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ⸺")
            if bstack1l1ll111l1ll_opy_ in _1llll11ll_opy_ and bstack1l1llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⸻") in _1llll11ll_opy_[bstack1l1ll111l1ll_opy_]:
                bstack1l1ll11ll111_opy_(_1llll11ll_opy_[bstack1l1ll111l1ll_opy_][bstack1l1llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⸼")])
        except Exception:
            pass
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, item)
        _instance = None
        _1l1llll11_opy_ = None
        try:
            from browserstack_sdk.sdk_cli.test_framework import TestFramework as _1l1ll1111ll1_opy_
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            _instance = _1l1ll1111ll1_opy_.get_tracked_instance(item.nodeid)
            _1l1llll11_opy_ = _1l1ll1111ll1_opy_.get_state(_instance, _1l1ll1111ll1_opy_.KEY_TEST_UUID) if _instance else None
            if _1l1llll11_opy_:
                threading.current_thread().current_test_uuid = _1l1llll11_opy_
            PlaywrightDriverWrapperDirect._send_cbt_info_on_session()
        except Exception as bstack1l1l1lll11ll_opy_:
            logger.warning(bstack1l1llll_opy_ (u"ࠢࡄࡄࡗࠤ࡫ࡲࡵࡴࡪࠣࡷࡰ࡯ࡰࡱࡧࡧࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡃࡻࡾࠢࠫࡻࡷࡧࡰࡱࡧࡵࡁࢀࢃࠬࠡࡷࡸ࡭ࡩࡃࡻࡾࠫ࠽ࠤࢀࢃࠢ⸽").format(
                item.nodeid, _instance is not None, _1l1llll11_opy_, bstack1l1l1lll11ll_opy_))
        return
    try:
        global CONFIG
        item._1l1l1lllll11_opy_ = True
        bstack1ll111l111_opy_ = a11y.is_enabled_testcase(bstack1llll1ll11l1_opy_(item.own_markers))
        if not cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
            item._a11y_test_case = bstack1ll111l111_opy_
            if bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⸾"), None):
                driver = getattr(item, bstack1l1llll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⸿"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack1ll111l111_opy_)
        if not TestHubHandler.on() or bstack1l1ll111l1l1_opy_ != bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⹀"):
            return
        global current_test_uuid #, bstack11l1l111_opy_
        bstack111111l1_opy_ = {
            bstack1l1llll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⹁"): uuid4().__str__(),
            bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⹂"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"࡚࠭ࠨ⹃")
        }
        current_test_uuid = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⹄")]
        store[bstack1l1llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⹅")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⹆")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1llll11ll_opy_[item.nodeid] = {**_1llll11ll_opy_[item.nodeid], **bstack111111l1_opy_}
        bstack1l1ll111l11l_opy_(item, _1llll11ll_opy_[item.nodeid], bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⹇"))
    except Exception as err:
        print(bstack1l1llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭⹈"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⹉")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⹊"))
    if bstack11ll1111l_opy_.bstack1ll1ll1ll11l_opy_():
            bstack1l1ll111ll11_opy_ = bstack1l1llll_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡢࡵࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦ⹋")
            logger.error(bstack1l1ll111ll11_opy_)
            bstack111111l1_opy_ = {
                bstack1l1llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⹌"): uuid4().__str__(),
                bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⹍"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠪ࡞ࠬ⹎"),
                bstack1l1llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⹏"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠬࡠࠧ⹐"),
                bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⹑"): bstack1l1llll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⹒"),
                bstack1l1llll_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ⹓"): bstack1l1ll111ll11_opy_,
                bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⹔"): [],
                bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⹕"): []
            }
            bstack1l1ll111l11l_opy_(item, bstack111111l1_opy_, bstack1l1llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⹖"))
            pytest.skip(bstack1l1ll111ll11_opy_)
            return # skip all existing operations
    global bstack1l1l1llll111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1llll1l11lll_opy_():
        atexit.register(bstack1111l1111l_opy_)
        if not bstack1l1l1llll111_opy_:
            try:
                bstack1l1ll11l111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1lll1l1lll1l_opy_():
                    bstack1l1ll11l111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1l1ll11l111l_opy_:
                    signal.signal(s, bstack1l11lll11_opy_)
                bstack1l1l1llll111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ⹗") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll111ll1l1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⹘")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack111111l1_opy_ = {
            bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⹙"): uuid,
            bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⹚"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠩ࡝ࠫ⹛"),
            bstack1l1llll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⹜"): bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⹝"),
            bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⹞"): bstack1l1llll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⹟"),
            bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⹠"): bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⹡")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⹢")] = item
        store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⹣")] = [uuid]
        if not _1llll11ll_opy_.get(item.nodeid, None):
            _1llll11ll_opy_[item.nodeid] = {bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⹤"): [], bstack1l1llll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⹥"): []}
        _1llll11ll_opy_[item.nodeid][bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⹦")].append(bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⹧")])
        _1llll11ll_opy_[item.nodeid + bstack1l1llll_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ⹨")] = bstack111111l1_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1l1l1lll1l1l_opy_(item, bstack111111l1_opy_, bstack1l1llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⹩"))
    except Exception as err:
        print(bstack1l1llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭⹪"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⹫"))
        try:
            from browserstack_sdk import _execute_deferred_playwright_close
            _execute_deferred_playwright_close(bstack111l11llll_opy_=True)
        except Exception as _1l1ll1111lll_opy_:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡊࡥࡧࡧࡵࡶࡪࡪࠠࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡨࡲ࡯ࡴࡧࠣࡪࡱࡻࡳࡩࠢࡩࡥ࡮ࡲࡥࡥࠢ࡬ࡲࠥࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠦ⹬").format(_1l1ll1111lll_opy_))
        return # skip all existing operations
    try:
        global bstack1ll1ll11111_opy_
        bstack1ll1l111l1_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll1l111l1_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⹭")))
        if bstack11ll1l1111_opy_.bstack1lll11llll1_opy_() == bstack1l1llll_opy_ (u"ࠢࡵࡴࡸࡩࠧ⹮"):
            if bstack11ll1l1111_opy_.bstack1l1ll1l1lll_opy_() == bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ⹯"):
                bstack1l1ll111ll1l_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⹰"), None)
                bstack11lll11lll_opy_ = bstack1l1ll111ll1l_opy_ + bstack1l1llll_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ⹱")
                driver = getattr(item, bstack1l1llll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⹲"), None)
                bstack1lll1llll1l_opy_ = getattr(item, bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⹳"), None)
                bstack11l1l11ll1_opy_ = getattr(item, bstack1l1llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⹴"), None)
                PercySDK.screenshot(driver, bstack11lll11lll_opy_, bstack1lll1llll1l_opy_=bstack1lll1llll1l_opy_, bstack11l1l11ll1_opy_=bstack11l1l11ll1_opy_, bstack1llllll11l_opy_=bstack1ll1l111l1_opy_)
        if not cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
            if getattr(item, bstack1l1llll_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ⹵"), False):
                bstack11llll11l_opy_.bstack11l1ll111_opy_(getattr(item, bstack1l1llll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⹶"), None), bstack1ll1ll11111_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack111111l1_opy_ = {
            bstack1l1llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⹷"): uuid4().__str__(),
            bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⹸"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠫ࡟࠭⹹"),
            bstack1l1llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⹺"): bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⹻"),
            bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⹼"): bstack1l1llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⹽"),
            bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⹾"): bstack1l1llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⹿")
        }
        _1llll11ll_opy_[item.nodeid + bstack1l1llll_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧ⺀")] = bstack111111l1_opy_
        threading.current_thread().current_hook_uuid = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⺁")]
        store[bstack1l1llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⺂")].append(bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⺃")])
        bstack1l1l1lll1l1l_opy_(item, bstack111111l1_opy_, bstack1l1llll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⺄"))
    except Exception as err:
        print(bstack1l1llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨ⺅"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1ll111ll11l1_opy_(fixturedef.argname):
        store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⺆")] = request.node
    elif bstack1ll111llll11_opy_(fixturedef.argname):
        store[bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⺇")] = request.node
    if not TestHubHandler.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⺈"): fixturedef.argname,
            bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⺉"): bstack1lll11ll11l1_opy_(outcome),
            bstack1l1llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⺊"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⺋")]
        if not _1llll11ll_opy_.get(current_test_item.nodeid, None):
            _1llll11ll_opy_[current_test_item.nodeid] = {bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⺌"): []}
        _1llll11ll_opy_[current_test_item.nodeid][bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⺍")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1llll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ⺎"), str(err))
if bstack1llll1l11l1_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1llll11ll_opy_[request.node.nodeid][bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⺏")].start_step(id(step))
        except Exception as err:
            print(bstack1l1llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ⺐"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1llll11ll_opy_[request.node.nodeid][bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⺑")].bstack1l111111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⺒"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            test_data: bstack1l1l1111_opy_ = _1llll11ll_opy_[request.node.nodeid][bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⺓")]
            test_data.bstack1l111111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ⺔"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1l1ll111l1l1_opy_
        try:
            if not TestHubHandler.on() or bstack1l1ll111l1l1_opy_ != bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ⺕"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ⺖"), None)
            if not _1llll11ll_opy_.get(request.node.nodeid, None):
                _1llll11ll_opy_[request.node.nodeid] = {}
            test_data = bstack1l1l1111_opy_.bstack1l1llllll11l_opy_(
                scenario, feature, request.node,
                name=bstack1ll111lllll1_opy_(request.node, scenario),
                started_at=bstack1l1111ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1llll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ⺗"),
                tags=bstack1ll111ll11ll_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1l11111l_opy_(driver) if driver and driver.session_id else {}
            )
            _1llll11ll_opy_[request.node.nodeid][bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⺘")] = test_data
            bstack1l1l1lll1ll1_opy_(test_data.uuid)
            TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⺙"), test_data)
        except Exception as err:
            print(bstack1l1llll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ⺚"), str(err))
def bstack1l1ll11ll111_opy_(bstack11l11111_opy_):
    if bstack11l11111_opy_ in store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⺛")]:
        store[bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⺜")].remove(bstack11l11111_opy_)
def bstack1l1l1lll1ll1_opy_(test_uuid):
    store[bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⺝")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1l1lll1l1ll1_opy_
def bstack1l1l1lllll1l_opy_(item, call, report):
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ⺞"))
    global bstack1l1ll111l1l1_opy_
    bstack1ll1l1111ll_opy_ = bstack1l1111ll_opy_()
    if hasattr(report, bstack1l1llll_opy_ (u"ࠧࡴࡶࡲࡴࠬ⺟")):
        bstack1ll1l1111ll_opy_ = bstack1lll1ll111l1_opy_(report.stop)
    elif hasattr(report, bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ⺠")):
        bstack1ll1l1111ll_opy_ = bstack1lll1ll111l1_opy_(report.start)
    try:
        if getattr(report, bstack1l1llll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⺡"), bstack1l1llll_opy_ (u"ࠪࠫ⺢")) == bstack1l1llll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⺣"):
            logger.debug(bstack1l1llll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⺤").format(getattr(report, bstack1l1llll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⺥"), bstack1l1llll_opy_ (u"ࠧࠨ⺦")).__str__(), bstack1l1ll111l1l1_opy_))
            if bstack1l1ll111l1l1_opy_ == bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⺧"):
                _1llll11ll_opy_[item.nodeid][bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⺨")] = bstack1ll1l1111ll_opy_
                bstack1l1ll111l11l_opy_(item, _1llll11ll_opy_[item.nodeid], bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⺩"), report, call)
                store[bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⺪")] = None
            elif bstack1l1ll111l1l1_opy_ == bstack1l1llll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ⺫"):
                test_data = _1llll11ll_opy_[item.nodeid][bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⺬")]
                test_data.set(hooks=_1llll11ll_opy_[item.nodeid].get(bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⺭"), []))
                exception, bstack1l1l1ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l1ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧ⺮"), bstack1l1llll_opy_ (u"ࠩࠪ⺯"))]
                test_data.stop(time=bstack1ll1l1111ll_opy_, result=Result(result=getattr(report, bstack1l1llll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⺰"), bstack1l1llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⺱")), exception=exception, bstack1l1l1ll1_opy_=bstack1l1l1ll1_opy_))
                TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⺲"), _1llll11ll_opy_[item.nodeid][bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⺳")])
        elif getattr(report, bstack1l1llll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⺴"), bstack1l1llll_opy_ (u"ࠨࠩ⺵")) in [bstack1l1llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⺶"), bstack1l1llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⺷")]:
            logger.debug(bstack1l1llll_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭⺸").format(getattr(report, bstack1l1llll_opy_ (u"ࠬࡽࡨࡦࡰࠪ⺹"), bstack1l1llll_opy_ (u"࠭ࠧ⺺")).__str__(), bstack1l1ll111l1l1_opy_))
            bstack1ll111l1_opy_ = item.nodeid + bstack1l1llll_opy_ (u"ࠧ࠮ࠩ⺻") + getattr(report, bstack1l1llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⺼"), bstack1l1llll_opy_ (u"ࠩࠪ⺽"))
            if getattr(report, bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⺾"), False):
                hook_type = bstack1l1llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⺿") if getattr(report, bstack1l1llll_opy_ (u"ࠬࡽࡨࡦࡰࠪ⻀"), bstack1l1llll_opy_ (u"࠭ࠧ⻁")) == bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⻂") else bstack1l1llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⻃")
                _1llll11ll_opy_[bstack1ll111l1_opy_] = {
                    bstack1l1llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⻄"): uuid4().__str__(),
                    bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⻅"): bstack1ll1l1111ll_opy_,
                    bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⻆"): hook_type
                }
            _1llll11ll_opy_[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⻇")] = bstack1ll1l1111ll_opy_
            bstack1l1ll11ll111_opy_(_1llll11ll_opy_[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⻈")])
            bstack1l1l1lll1l1l_opy_(item, _1llll11ll_opy_[bstack1ll111l1_opy_], bstack1l1llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⻉"), report, call)
            if getattr(report, bstack1l1llll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⻊"), bstack1l1llll_opy_ (u"ࠩࠪ⻋")) == bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⻌"):
                if getattr(report, bstack1l1llll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⻍"), bstack1l1llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⻎")) == bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⻏"):
                    bstack111111l1_opy_ = {
                        bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⻐"): uuid4().__str__(),
                        bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⻑"): bstack1l1111ll_opy_(),
                        bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⻒"): bstack1l1111ll_opy_()
                    }
                    _1llll11ll_opy_[item.nodeid] = {**_1llll11ll_opy_[item.nodeid], **bstack111111l1_opy_}
                    bstack1l1ll111l11l_opy_(item, _1llll11ll_opy_[item.nodeid], bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⻓"))
                    bstack1l1ll111l11l_opy_(item, _1llll11ll_opy_[item.nodeid], bstack1l1llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⻔"), report, call)
    except Exception as err:
        print(bstack1l1llll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ⻕"), str(err))
def bstack1l1ll1111111_opy_(test, bstack111111l1_opy_, result=None, call=None, bstack1l1lll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    test_data = {
        bstack1l1llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⻖"): bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⻗")],
        bstack1l1llll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⻘"): bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࠧ⻙"),
        bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⻚"): test.name,
        bstack1l1llll_opy_ (u"ࠫࡧࡵࡤࡺࠩ⻛"): {
            bstack1l1llll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⻜"): bstack1l1llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⻝"),
            bstack1l1llll_opy_ (u"ࠧࡤࡱࡧࡩࠬ⻞"): inspect.getsource(test.obj)
        },
        bstack1l1llll_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⻟"): test.name,
        bstack1l1llll_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ⻠"): test.name,
        bstack1l1llll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⻡"): bstack1ll111ll_opy_.bstack1llll1ll1_opy_(test),
        bstack1l1llll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⻢"): file_path,
        bstack1l1llll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⻣"): file_path,
        bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⻤"): bstack1l1llll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⻥"),
        bstack1l1llll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⻦"): file_path,
        bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⻧"): bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⻨")],
        bstack1l1llll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⻩"): bstack1l1llll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⻪"),
        bstack1l1llll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ⻫"): {
            bstack1l1llll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ⻬"): test.nodeid
        },
        bstack1l1llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⻭"): bstack1llll1ll11l1_opy_(test.own_markers)
    }
    if bstack1l1lll111_opy_ in [bstack1l1llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⻮"), bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⻯")]:
        test_data[bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ⻰")] = {
            bstack1l1llll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⻱"): bstack111111l1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⻲"), [])
        }
    if bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⻳"):
        test_data[bstack1l1llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⻴")] = bstack1l1llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⻵")
        test_data[bstack1l1llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⻶")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⻷")]
        test_data[bstack1l1llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⻸")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⻹")]
    if result:
        test_data[bstack1l1llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⻺")] = result.outcome
        test_data[bstack1l1llll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⻻")] = result.duration * 1000
        test_data[bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⻼")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⻽")]
        if result.failed:
            test_data[bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⻾")] = TestHubHandler.failure_type(call.excinfo.typename)
            test_data[bstack1l1llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⻿")] = TestHubHandler.bstack1l1lll11llll_opy_(call.excinfo, result)
        test_data[bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⼀")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⼁")]
    if outcome:
        test_data[bstack1l1llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⼂")] = bstack1lll11ll11l1_opy_(outcome)
        test_data[bstack1l1llll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⼃")] = 0
        test_data[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⼄")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⼅")]
        if test_data[bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⼆")] == bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⼇"):
            test_data[bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⼈")] = bstack1l1llll_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⼉")  # bstack1l1ll11111l1_opy_
            test_data[bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⼊")] = [{bstack1l1llll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⼋"): [bstack1l1llll_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⼌")]}]
        test_data[bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⼍")] = bstack111111l1_opy_[bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⼎")]
    return test_data
def bstack1l1ll11l11l1_opy_(test, bstack1lllll1l1_opy_, bstack1l1lll111_opy_, result, call, outcome, bstack1l1ll111lll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⼏")]
    hook_name = bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⼐")]
    hook_data = {
        bstack1l1llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⼑"): bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⼒")],
        bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⼓"): bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⼔"),
        bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⼕"): bstack1l1llll_opy_ (u"ࠧࡼࡿࠪ⼖").format(bstack1ll111ll1lll_opy_(hook_name)),
        bstack1l1llll_opy_ (u"ࠨࡤࡲࡨࡾ࠭⼗"): {
            bstack1l1llll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⼘"): bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⼙"),
            bstack1l1llll_opy_ (u"ࠫࡨࡵࡤࡦࠩ⼚"): None
        },
        bstack1l1llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⼛"): test.name,
        bstack1l1llll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⼜"): bstack1ll111ll_opy_.bstack1llll1ll1_opy_(test, hook_name),
        bstack1l1llll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⼝"): file_path,
        bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⼞"): file_path,
        bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⼟"): bstack1l1llll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⼠"),
        bstack1l1llll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⼡"): file_path,
        bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⼢"): bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⼣")],
        bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⼤"): bstack1l1llll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⼥") if bstack1l1ll111l1l1_opy_ == bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⼦") else bstack1l1llll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⼧"),
        bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⼨"): hook_type
    }
    bstack11ll11ll1l1_opy_ = bstack1lllll1ll_opy_(_1llll11ll_opy_.get(test.nodeid, None))
    if bstack11ll11ll1l1_opy_:
        hook_data[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⼩")] = bstack11ll11ll1l1_opy_
    if result:
        hook_data[bstack1l1llll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⼪")] = result.outcome
        hook_data[bstack1l1llll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⼫")] = result.duration * 1000
        hook_data[bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⼬")] = bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⼭")]
        if result.failed:
            hook_data[bstack1l1llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⼮")] = TestHubHandler.failure_type(call.excinfo.typename)
            hook_data[bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⼯")] = TestHubHandler.bstack1l1lll11llll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⼰")] = bstack1lll11ll11l1_opy_(outcome)
        hook_data[bstack1l1llll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⼱")] = 100
        hook_data[bstack1l1llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⼲")] = bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⼳")]
        if hook_data[bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⼴")] == bstack1l1llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⼵"):
            hook_data[bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⼶")] = bstack1l1llll_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭⼷")  # bstack1l1ll11111l1_opy_
            hook_data[bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⼸")] = [{bstack1l1llll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⼹"): [bstack1l1llll_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⼺")]}]
    if bstack1l1ll111lll1_opy_:
        hook_data[bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⼻")] = bstack1l1ll111lll1_opy_.result
        hook_data[bstack1l1llll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⼼")] = bstack1ll1l11ll_opy_(bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⼽")], bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⼾")])
        hook_data[bstack1l1llll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⼿")] = bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⽀")]
        if hook_data[bstack1l1llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⽁")] == bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⽂"):
            hook_data[bstack1l1llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⽃")] = TestHubHandler.failure_type(bstack1l1ll111lll1_opy_.exception_type)
            hook_data[bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⽄")] = [{bstack1l1llll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⽅"): bstack1lll1l1l1l11_opy_(bstack1l1ll111lll1_opy_.exception)}]
    return hook_data
def bstack1l1ll111l11l_opy_(test, bstack111111l1_opy_, bstack1l1lll111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1llll_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ⽆").format(bstack1l1lll111_opy_))
    test_data = bstack1l1ll1111111_opy_(test, bstack111111l1_opy_, result, call, bstack1l1lll111_opy_, outcome)
    driver = getattr(test, bstack1l1llll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⽇"), None)
    if bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⽈") and driver:
        test_data[bstack1l1llll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⽉")] = TestHubHandler.bstack1l11111l_opy_(driver)
    if bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⽊"):
        bstack1l1lll111_opy_ = bstack1l1llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⽋")
    bstack111l1111_opy_ = {
        bstack1l1llll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⽌"): bstack1l1lll111_opy_,
        bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⽍"): test_data
    }
    TestHubHandler.bstack1lll11ll1_opy_(bstack111l1111_opy_)
    if bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⽎"):
        threading.current_thread().bstackTestMeta = {bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⽏"): bstack1l1llll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⽐")}
    elif bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⽑"):
        threading.current_thread().bstackTestMeta = {bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⽒"): getattr(result, bstack1l1llll_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⽓"), bstack1l1llll_opy_ (u"࠭ࠧ⽔"))}
def bstack1l1l1lll1l1l_opy_(test, bstack111111l1_opy_, bstack1l1lll111_opy_, result=None, call=None, outcome=None, bstack1l1ll111lll1_opy_=None):
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ⽕").format(bstack1l1lll111_opy_))
    hook_data = bstack1l1ll11l11l1_opy_(test, bstack111111l1_opy_, bstack1l1lll111_opy_, result, call, outcome, bstack1l1ll111lll1_opy_)
    bstack111l1111_opy_ = {
        bstack1l1llll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⽖"): bstack1l1lll111_opy_,
        bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ⽗"): hook_data
    }
    TestHubHandler.bstack1lll11ll1_opy_(bstack111l1111_opy_)
def bstack1lllll1ll_opy_(bstack111111l1_opy_):
    if not bstack111111l1_opy_:
        return None
    if bstack111111l1_opy_.get(bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⽘"), None):
        return getattr(bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⽙")], bstack1l1llll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⽚"), None)
    return bstack111111l1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⽛"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, request, caplog)
        return # skip all existing operations
    try:
        if not TestHubHandler.on():
            return
        places = [bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⽜"), bstack1l1llll_opy_ (u"ࠨࡥࡤࡰࡱ࠭⽝"), bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⽞")]
        logs = []
        for bstack1l1l1llll11l_opy_ in places:
            records = caplog.get_records(bstack1l1l1llll11l_opy_)
            bstack1l1l1llllll1_opy_ = bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⽟") if bstack1l1l1llll11l_opy_ == bstack1l1llll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⽠") else bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⽡")
            bstack1l1l1lll1lll_opy_ = request.node.nodeid + (bstack1l1llll_opy_ (u"࠭ࠧ⽢") if bstack1l1l1llll11l_opy_ == bstack1l1llll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⽣") else bstack1l1llll_opy_ (u"ࠨ࠯ࠪ⽤") + bstack1l1l1llll11l_opy_)
            test_uuid = bstack1lllll1ll_opy_(_1llll11ll_opy_.get(bstack1l1l1lll1lll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1llll1111l11_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⽥"): bstack1lll1lll1l11_opy_(record.created).isoformat() + bstack1l1llll_opy_ (u"ࠪ࡞ࠬ⽦"),
                    bstack1l1llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⽧"): record.levelname,
                    bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⽨"): record.message,
                    bstack1l1l1llllll1_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1ll11111_opy_(logs)
    except Exception as err:
        print(bstack1l1llll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ⽩"), str(err))
def bstack1111l11ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11lll1llll_opy_
    bstack111ll1l1ll_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ⽪"), None) and bstack11llll11_opy_(
            threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⽫"), None)
    bstack1111llll1_opy_ = getattr(driver, bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⽬"), None) != None and getattr(driver, bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⽭"), None) == True
    if sequence == bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⽮") and driver != None:
      if not bstack11lll1llll_opy_ and is_bstack_automation() and bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⽯") in CONFIG and CONFIG[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⽰")] == True and accessibility_scripts.bstack1ll111ll1l1_opy_(driver_command) and (bstack1111llll1_opy_ or bstack111ll1l1ll_opy_) and not bstack1l11l1l1ll_opy_(args):
        try:
          bstack11lll1llll_opy_ = True
          logger.debug(bstack1l1llll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ⽱").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1llll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭⽲").format(str(err)))
        bstack11lll1llll_opy_ = False
    if sequence == bstack1l1llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⽳"):
        if driver_command == bstack1l1llll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ⽴"):
            TestHubHandler.bstack1ll11ll1ll_opy_({
                bstack1l1llll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⽵"): response[bstack1l1llll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⽶")],
                bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⽷"): store[bstack1l1llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⽸")]
            })
def bstack1111l1111l_opy_():
    global bstack1111ll11l_opy_
    logger_utils.bstack1llll1l111_opy_()
    logging.shutdown()
    TestHubHandler.bstack1111111l_opy_()
    for driver in bstack1111ll11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11lll11_opy_(*args):
    global bstack1111ll11l_opy_
    TestHubHandler.bstack1111111l_opy_()
    for driver in bstack1111ll11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1llll1ll_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1lll11llll_opy_(self, *args, **kwargs):
    bstack111111l1ll_opy_ = bstack1l1l1l111l1_opy_(self, *args, **kwargs)
    bstack111l1ll1l1_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⽹"), None)
    if bstack111l1ll1l1_opy_ and bstack111l1ll1l1_opy_.get(bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⽺"), bstack1l1llll_opy_ (u"ࠪࠫ⽻")) == bstack1l1llll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⽼"):
        TestHubHandler.send_cbt_info(self)
    return bstack111111l1ll_opy_
@measure(event_name=EVENTS.bstack1111l1l1l_opy_, stage=STAGE.bstack1l11ll1l1l_opy_, bstack11lllll111_opy_=SESSION_NAME)
def bstack1ll11111l11_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.bstack1lll1l11_opy_()
    if global_config.get_property(bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⽽")):
        return
    global_config.bstack1ll11l111l_opy_(bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⽾"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack11l1llll11_opy_.format(FRAMEWORK_NAME.split(bstack1l1llll_opy_ (u"ࠧ࠮ࠩ⽿"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if is_bstack_automation():
            Service.start = bstack1ll11llll11_opy_
            Service.stop = bstack1ll11l1l1l_opy_
            webdriver.Remote.get = bstack1ll1ll11l1l_opy_
            webdriver.Remote.__init__ = bstack1111ll11ll_opy_
            if not isinstance(os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ⾀")), str):
                return
            WebDriver.quit = bstack11lll1l111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1lll11llll_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1llll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⾁")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1l1llll_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⾂")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack1ll1l1lll1_opy_(bstack1l1llll_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ⾃"), bstack1ll11111l1l_opy_)
    if bstack1111lll11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⾄")) and callable(getattr(RemoteConnection, bstack1l1llll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⾅"))):
                RemoteConnection._get_proxy_url = bstack1ll1ll1lll1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1ll1ll1lll1_opy_
        except Exception as e:
            logger.error(bstack1ll1l1l1l1_opy_.format(str(e)))
    if bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⾆") in str(framework_name).lower():
        if not is_bstack_automation():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1lll11l11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l11lll1_opy_
            Config.getoption = bstack11111l1ll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll11ll11l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llllll1ll1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack11lll1l111_opy_(self):
    global FRAMEWORK_NAME
    global bstack11llll1l11_opy_
    global bstack1lllll11111_opy_
    try:
        if bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⾇") in FRAMEWORK_NAME and self.session_id != None and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭⾈"), bstack1l1llll_opy_ (u"ࠪࠫ⾉")) != bstack1l1llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⾊"):
            bstack111llll1l1_opy_ = bstack1l1llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⾋") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⾌")
            bstack11l1ll11ll_opy_(logger, True)
            if os.environ.get(bstack1l1llll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⾍"), None):
                self.execute_script(
                    bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⾎") + json.dumps(
                        os.environ.get(bstack1l1llll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⾏"))) + bstack1l1llll_opy_ (u"ࠪࢁࢂ࠭⾐"))
            if self != None:
                bstack1l1lll1ll1l_opy_(self, bstack111llll1l1_opy_, bstack1l1llll_opy_ (u"ࠫ࠱ࠦࠧ⾑").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
            item = store.get(bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⾒"), None)
            if item is not None and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⾓"), None):
                bstack11llll11l_opy_.bstack11l1ll111_opy_(self, bstack1ll1ll11111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1llll_opy_ (u"ࠧࠨ⾔")
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ⾕") + str(e))
    bstack1lllll11111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1ll1lllll1l_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1111ll11ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
    global CONFIG
    global bstack11llll1l11_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1l1l1l111l1_opy_
    global bstack1111ll11l_opy_
    global bstack1lll1ll1l11_opy_
    global bstack1ll1ll111ll_opy_
    global bstack1ll1ll11111_opy_
    CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⾖")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack1l1l111ll11_opy_(bstack1lll1ll1l11_opy_, CONFIG)
    logger.debug(bstack11llll1lll_opy_.format(command_executor))
    proxy = bstack1l1l11l1ll1_opy_(CONFIG, proxy)
    bstack1ll1l111l1_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll1l111l1_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⾗")))
    except:
        bstack1ll1l111l1_opy_ = 0
    bstack11111lll1l_opy_ = get_caps(CONFIG, bstack1ll1l111l1_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11111lll1l_opy_)))
    bstack1ll1ll11111_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⾘"))[bstack1ll1l111l1_opy_]
    if bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⾙") in CONFIG and CONFIG[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⾚")]:
        update_caps_for_local(bstack11111lll1l_opy_, bstack1ll1ll111ll_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack1ll1l111l1_opy_) and a11y.is_platform_supported(bstack11111lll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l1ll1l1111_opy_(EventDispatcherModule):
            a11y.set_capabilities(bstack11111lll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll111lll1_opy_ = bstack1ll1l11ll1l_opy_(desired_capabilities)
        bstack1lll111lll1_opy_[bstack1l1llll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⾛")] = bstack11l1ll1111_opy_(CONFIG)
        bstack1l1lllll11_opy_ = get_caps(bstack1lll111lll1_opy_)
        if bstack1l1lllll11_opy_:
            bstack11111lll1l_opy_ = update(bstack1l1lllll11_opy_, bstack11111lll1l_opy_)
        desired_capabilities = None
    if options:
        bstack1lllll111l_opy_(options, bstack11111lll1l_opy_)
    if not options:
        options = bstack1llll11ll11_opy_(bstack11111lll1l_opy_)
    if proxy and bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⾜")):
        options.proxy(proxy)
    if options and bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⾝")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1ll11111_opy_() < version.parse(bstack1l1llll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⾞")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11111lll1l_opy_)
    logger.info(bstack1llll1llll1_opy_)
    performance_tester.end(EVENTS.bstack1111l1l1l_opy_.value, EVENTS.bstack1111l1l1l_opy_.value + bstack1l1llll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⾟"),
                               EVENTS.bstack1111l1l1l_opy_.value + bstack1l1llll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⾠"), True, None)
    try:
        if bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⾡")):
            bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⾢")):
            bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ⾣")):
            bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l1l1l111l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack111lll11l1_opy_:
        logger.error(bstack111ll1111l_opy_.format(bstack1l1llll_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨ⾤"), str(bstack111lll11l1_opy_)))
        raise bstack111lll11l1_opy_
    try:
        bstack1l1l1llllll_opy_ = bstack1l1llll_opy_ (u"ࠪࠫ⾥")
        if bstack1l1ll11111_opy_() >= version.parse(bstack1l1llll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ⾦")):
            bstack1l1l1llllll_opy_ = self.caps.get(bstack1l1llll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⾧"))
        else:
            bstack1l1l1llllll_opy_ = self.capabilities.get(bstack1l1llll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⾨"))
        if bstack1l1l1llllll_opy_:
            bstack1lll11l111_opy_(bstack1l1l1llllll_opy_)
            if bstack1l1ll11111_opy_() <= version.parse(bstack1l1llll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ⾩")):
                self.command_executor._url = bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⾪") + bstack1lll1ll1l11_opy_ + bstack1l1llll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ⾫")
            else:
                self.command_executor._url = bstack1l1llll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ⾬") + bstack1l1l1llllll_opy_ + bstack1l1llll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ⾭")
            logger.debug(bstack1lllll11l11_opy_.format(bstack1l1l1llllll_opy_))
        else:
            logger.debug(bstack1lllllll11l_opy_.format(bstack1l1llll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ⾮")))
    except Exception as e:
        logger.debug(bstack1lllllll11l_opy_.format(e))
    bstack11llll1l11_opy_ = self.session_id
    if bstack1l1llll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⾯") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⾰"), None)
        if item:
            bstack1l1l1lllllll_opy_ = getattr(item, bstack1l1llll_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭⾱"), False)
            if not getattr(item, bstack1l1llll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⾲"), None) and bstack1l1l1lllllll_opy_:
                setattr(store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⾳")], bstack1l1llll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⾴"), self)
        bstack111l1ll1l1_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⾵"), None)
        if bstack111l1ll1l1_opy_ and bstack111l1ll1l1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⾶"), bstack1l1llll_opy_ (u"ࠧࠨ⾷")) == bstack1l1llll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⾸"):
            TestHubHandler.send_cbt_info(self)
    bstack1111ll11l_opy_.append(self)
    if bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⾹") in CONFIG and bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⾺") in CONFIG[bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⾻")][bstack1ll1l111l1_opy_]:
        SESSION_NAME = CONFIG[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⾼")][bstack1ll1l111l1_opy_][bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⾽")]
    logger.debug(bstack1l1ll1ll1l_opy_.format(bstack11llll1l11_opy_))
@measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=SESSION_NAME)
def bstack1ll1ll11l1l_opy_(self, url):
    global bstack11l1111111_opy_
    global CONFIG
    try:
        bstack1l1l1llll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1l1ll1l_opy_.format(str(err)))
    try:
        bstack11l1111111_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack1111ll111l_opy_):
                bstack1l1l1llll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1l1ll1l_opy_.format(str(err)))
        raise e
def bstack1l11llll1l_opy_(item, when):
    global bstack111l1lll11_opy_
    try:
        bstack111l1lll11_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll11ll11l_opy_(item, call, rep):
    global bstack1llllll1lll_opy_
    global bstack1111ll11l_opy_
    name = bstack1l1llll_opy_ (u"ࠧࠨ⾾")
    try:
        if rep.when == bstack1l1llll_opy_ (u"ࠨࡥࡤࡰࡱ࠭⾿"):
            bstack11llll1l11_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1llll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⿀"))
            try:
                if (str(skipSessionName).lower() != bstack1l1llll_opy_ (u"ࠪࡸࡷࡻࡥࠨ⿁")):
                    name = str(rep.nodeid)
                    bstack1l1lll11l_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⿂"), name, bstack1l1llll_opy_ (u"ࠬ࠭⿃"), bstack1l1llll_opy_ (u"࠭ࠧ⿄"), bstack1l1llll_opy_ (u"ࠧࠨ⿅"), bstack1l1llll_opy_ (u"ࠨࠩ⿆"))
                    os.environ[bstack1l1llll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⿇")] = name
                    for driver in bstack1111ll11l_opy_:
                        if bstack11llll1l11_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1lll11l_opy_)
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⿈").format(str(e)))
            try:
                bstack1lll11l11l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1llll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⿉"):
                    status = bstack1l1llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⿊") if rep.outcome.lower() == bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⿋") else bstack1l1llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⿌")
                    reason = bstack1l1llll_opy_ (u"ࠨࠩ⿍")
                    if status == bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⿎"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1llll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ⿏") if status == bstack1l1llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⿐") else bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⿑")
                    data = name + bstack1l1llll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ⿒") if status == bstack1l1llll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⿓") else name + bstack1l1llll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫ⿔") + reason
                    bstack1lll11l1lll_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ⿕"), bstack1l1llll_opy_ (u"ࠪࠫ⿖"), bstack1l1llll_opy_ (u"ࠫࠬ⿗"), bstack1l1llll_opy_ (u"ࠬ࠭⿘"), level, data)
                    for driver in bstack1111ll11l_opy_:
                        if bstack11llll1l11_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11l1lll_opy_)
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⿙").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ⿚").format(str(e)))
    bstack1llllll1lll_opy_(item, call, rep)
notset = Notset()
def bstack11111l1ll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l111l1ll1_opy_
    if str(name).lower() == bstack1l1llll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ⿛"):
        return bstack1l1llll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ⿜")
    else:
        return bstack1l111l1ll1_opy_(self, name, default, skip)
def bstack1ll1ll1lll1_opy_(self):
    global CONFIG
    global bstack11l1l11l1l_opy_
    try:
        proxy = bstack1l111ll111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1llll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ⿝")):
                proxies = bstack1ll1ll1111l_opy_(proxy, bstack1l1l111ll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1lllll1_opy_ = proxies.popitem()
                    if bstack1l1llll_opy_ (u"ࠦ࠿࠵࠯ࠣ⿞") in bstack1ll1lllll1_opy_:
                        return bstack1ll1lllll1_opy_
                    else:
                        return bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⿟") + bstack1ll1lllll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ⿠").format(str(e)))
    return bstack11l1l11l1l_opy_(self)
def bstack1111lll11l_opy_():
    return (bstack1l1llll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⿡") in CONFIG or bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⿢") in CONFIG) and bstack1l1111l1ll_opy_() and bstack1l1ll11111_opy_() >= version.parse(
        bstack1l1l1ll1l11_opy_)
def bstack11111llll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    CONFIG[bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⿣")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1ll1l111l1_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll1l111l1_opy_ = int(os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⿤")))
    except:
        bstack1ll1l111l1_opy_ = 0
    CONFIG[bstack1l1llll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ⿥")] = True
    bstack11111lll1l_opy_ = get_caps(CONFIG, bstack1ll1l111l1_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11111lll1l_opy_)))
    if CONFIG.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⿦")):
        update_caps_for_local(bstack11111lll1l_opy_, bstack1ll1ll111ll_opy_)
    if bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⿧") in CONFIG and bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⿨") in CONFIG[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⿩")][bstack1ll1l111l1_opy_]:
        SESSION_NAME = CONFIG[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⿪")][bstack1ll1l111l1_opy_][bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⿫")]
    import urllib
    import json
    if bstack1l1llll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⿬") in CONFIG and str(CONFIG[bstack1l1llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⿭")]).lower() != bstack1l1llll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⿮"):
        bstack1l1lllll1ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1l1lllll1ll_opy_ + urllib.parse.quote(json.dumps(bstack11111lll1l_opy_))
    else:
        cdpUrl = bstack1l1llll_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ⿯") + urllib.parse.quote(json.dumps(bstack11111lll1l_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11l1l11l1_opy_
        if not is_bstack_automation():
            global bstack11l1111lll_opy_
            if not bstack11l1111lll_opy_:
                from bstack_utils.helper import bstack1l1l11l1l1l_opy_, bstack1llll11l1lll_opy_
                bstack11l1111lll_opy_ = bstack1l1l11l1l1l_opy_()
                bstack1llll11l1lll_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l11l1l11l1_opy_
            return
        BrowserType.launch = bstack11111llll_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1l1ll111llll_opy_():
    global CONFIG
    global bstack11ll111lll_opy_
    global bstack1lll1ll1l11_opy_
    global bstack1ll1ll111ll_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack1l1111l111_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ⿰")))
    bstack11ll111lll_opy_ = eval(os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ⿱")))
    bstack1lll1ll1l11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ⿲"))
    bstack1l1lll1111l_opy_(CONFIG, bstack11ll111lll_opy_)
    bstack1l1111l111_opy_ = logger_utils.configure_logger(CONFIG, bstack1l1111l111_opy_)
    if cli.bstack111l1ll11_opy_():
        bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack111ll11ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⿳"), bstack1l1llll_opy_ (u"ࠬ࠶ࠧ⿴")))
        cli.bstack1ll1111l11l_opy_(cli_context.platform_index)
        cli.bstack11lllllll11_opy_(bstack1l1l111ll11_opy_(bstack1lll1ll1l11_opy_, CONFIG), cli_context.platform_index, bstack1llll11ll11_opy_)
        cli.bstack1ll11l111_opy_()
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⿵") + str(cli_context.platform_index) + bstack1l1llll_opy_ (u"ࠢࠣ⿶"))
        return # skip all existing operations
    global bstack1l1l1l111l1_opy_
    global bstack1lllll11111_opy_
    global bstack1111l1l1l1_opy_
    global bstack11l1l1l1l1_opy_
    global bstack111lll1l11_opy_
    global bstack1llllll111l_opy_
    global bstack11l11ll1ll_opy_
    global bstack11l1111111_opy_
    global bstack11l1l11l1l_opy_
    global bstack1l111l1ll1_opy_
    global bstack111l1lll11_opy_
    global bstack1llllll1lll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l1l111l1_opy_ = webdriver.Remote.__init__
        bstack1lllll11111_opy_ = WebDriver.quit
        bstack11l11ll1ll_opy_ = WebDriver.close
        bstack11l1111111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1llll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⿷") in CONFIG or bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⿸") in CONFIG) and bstack1l1111l1ll_opy_():
        if bstack1l1ll11111_opy_() < version.parse(bstack1l1l1ll1l11_opy_):
            logger.error(bstack1ll1ll1l1l_opy_.format(bstack1l1ll11111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⿹")) and callable(getattr(RemoteConnection, bstack1l1llll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⿺"))):
                    bstack11l1l11l1l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack11l1l11l1l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1ll1l1l1l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l111l1ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack111l1lll11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1l1llll_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧ⿻"), bstack11llllll1_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1llllll1lll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ⿼"))
    bstack1ll1ll111ll_opy_ = CONFIG.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⿽"), {}).get(bstack1l1llll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⿾"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack1ll11111l11_opy_(bstack1l111lll1l_opy_)
if (bstack1llll1l11lll_opy_()):
    bstack1l1ll111llll_opy_()
@error_handler(class_method=False)
def bstack1l1ll11l1l1l_opy_(hook_name, event, hook_result=None):
    if hook_name not in [bstack1l1llll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⿿"), bstack1l1llll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ　"), bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ、"), bstack1l1llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ。"), bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ〃"), bstack1l1llll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ〄"), bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ々"), bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ〆")]:
        return
    node = store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ〇")]
    if hook_name in [bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ〈"), bstack1l1llll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ〉")]:
        node = store[bstack1l1llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ《")]
    elif hook_name in [bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ》"), bstack1l1llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ「")]:
        node = store[bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ」")]
    hook_type = bstack1ll111lll1l1_opy_(hook_name)
    if event == bstack1l1llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ『"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lllll1l1_opy_ = {
            bstack1l1llll_opy_ (u"ࠫࡺࡻࡩࡥࠩ』"): uuid,
            bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ【"): bstack1l1111ll_opy_(),
            bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫ】"): bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ〒"),
            bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ〓"): hook_type,
            bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ〔"): hook_name
        }
        store[bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ〕")].append(uuid)
        bstack1l1ll111111l_opy_ = node.nodeid
        if hook_type == bstack1l1llll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ〖"):
            if not _1llll11ll_opy_.get(bstack1l1ll111111l_opy_, None):
                _1llll11ll_opy_[bstack1l1ll111111l_opy_] = {bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ〗"): []}
            _1llll11ll_opy_[bstack1l1ll111111l_opy_][bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ〘")].append(bstack1lllll1l1_opy_[bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ〙")])
        _1llll11ll_opy_[bstack1l1ll111111l_opy_ + bstack1l1llll_opy_ (u"ࠨ࠯ࠪ〚") + hook_name] = bstack1lllll1l1_opy_
        bstack1l1l1lll1l1l_opy_(node, bstack1lllll1l1_opy_, bstack1l1llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ〛"))
    elif event == bstack1l1llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ〜"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, hook_result)
            return
        bstack1ll111l1_opy_ = node.nodeid + bstack1l1llll_opy_ (u"ࠫ࠲࠭〝") + hook_name
        _1llll11ll_opy_[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ〞")] = bstack1l1111ll_opy_()
        bstack1l1ll11ll111_opy_(_1llll11ll_opy_[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ〟")])
        bstack1l1l1lll1l1l_opy_(node, _1llll11ll_opy_[bstack1ll111l1_opy_], bstack1l1llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ〠"), bstack1l1ll111lll1_opy_=hook_result)
def bstack1l1ll11ll11l_opy_():
    global bstack1l1ll111l1l1_opy_
    if bstack1llll1l11l1_opy_():
        bstack1l1ll111l1l1_opy_ = bstack1l1llll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ〡")
    else:
        bstack1l1ll111l1l1_opy_ = bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ〢")
@TestHubHandler.bstack1l1lll1l1ll1_opy_
def bstack1l1ll11l1111_opy_():
    bstack1l1ll11ll11l_opy_()
    if cli.is_running():
        try:
            bstack1lll111ll1l1_opy_(bstack1l1ll11l1l1l_opy_)
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ〣").format(e))
        return
    if bstack1l1111l1ll_opy_():
        global_config = Config.bstack1lll1l11_opy_()
        bstack1l1llll_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ〤")
        if global_config.get_property(bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ〥")):
            if CONFIG.get(bstack1l1llll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭〦")) is not None and int(CONFIG[bstack1l1llll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ〧")]) > 1:
                bstack1llllllllll_opy_(bstack1111l11ll1_opy_)
            return
        bstack1llllllllll_opy_(bstack1111l11ll1_opy_)
    try:
        bstack1lll111ll1l1_opy_(bstack1l1ll11l1l1l_opy_)
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ〨").format(e))
bstack1l1ll11l1111_opy_()