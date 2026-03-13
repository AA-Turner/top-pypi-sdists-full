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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack111l1l1ll1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1ll1lll1l1_opy_, update, bstack1l11l1111l_opy_,
                                       bstack1111ll11l_opy_, bstack1l1l1l11_opy_, bstack1l11l111_opy_, bstack11lll1l11l_opy_,
                                       bstack1111l11ll_opy_, bstack11ll1ll11l_opy_, bstack1l111l111l_opy_,
                                       bstack11l11l1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1l11l11l_opy_)
from browserstack_sdk.bstack1ll11l1ll_opy_ import bstack11l11llll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack11111l1l11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11l1111lll_opy_, bstack11l11ll1_opy_, bstack11lll1l1l1_opy_, \
    bstack111ll1l11l_opy_
from bstack_utils.helper import bstack1l11l11l11_opy_, bstack11111ll1l1l_opy_, bstack1lllll1111l_opy_, bstack1l11ll1111_opy_, bstack111l1ll11l_opy_, current_time, \
    bstack1111lll1l11_opy_, \
    bstack1111l1l1ll1_opy_, bstack1l1ll1ll1l_opy_, bstack1ll11l111l_opy_, bstack11111l11l11_opy_, bstack111ll11ll1_opy_, Notset, \
    bstack11l1111l_opy_, time_diff, bstack1111l1l111l_opy_, Result, bstack11111l1ll1l_opy_, bstack1111l1lllll_opy_, error_handler, \
    bstack11ll11111l_opy_, bstack1111l1ll1_opy_, bstack1ll111llll_opy_, bstack11111l11111_opy_
from bstack_utils.bstack1111111l1ll_opy_ import bstack11111111l11_opy_
from bstack_utils.messages import bstack1l11lll111_opy_, bstack1l1lll11l_opy_, bstack111l11l11_opy_, bstack11l1l1l1l1_opy_, bstack111ll11l11_opy_, \
    bstack111l1lllll_opy_, bstack1ll1lllll1_opy_, CONFIG_FILE_CONTENT, bstack1l1111l111_opy_, bstack1l11l1ll11_opy_, \
    bstack111111ll_opy_, bstack1ll11lll1l_opy_, bstack111llll11l_opy_
from bstack_utils.proxy import bstack11ll1lllll_opy_, bstack1llll1l1ll_opy_
from bstack_utils.bstack1lll1l11l1_opy_ import bstack1lll11l1ll1l_opy_, bstack1lll11l1l1l1_opy_, bstack1lll11l11l1l_opy_, bstack1lll11l1l11l_opy_, \
    bstack1lll11l11ll1_opy_, bstack1lll11l11l11_opy_, bstack1lll11l1llll_opy_, bstack111lll111_opy_, bstack1lll11ll1111_opy_
from bstack_utils.bstack1111l11lll_opy_ import bstack1l111l1lll_opy_
from bstack_utils.session_utils import browserstack_executor_helper, bstack1l11ll111l_opy_, update_caps_for_local, \
    bstack1ll1111l1l_opy_, bstack1l111l11ll_opy_
from bstack_utils.test_data import TestData
from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack11llllll1_opy_ import bstack11ll11l11l_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack1llll1l11_opy_ import bstack11l1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1111ll11_opy_ import bstack1111ll11_opy_, Events, bstack1lllll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1lll11l1_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111ll11_opy_ import bstack1111ll11_opy_, Events, bstack1lllll111l_opy_
bstack1ll1l1ll_opy_ = None
bstack11l1ll11l_opy_ = None
bstack1lllllll1_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1111111l_opy_ = None
bstack1l1l111l1l_opy_ = None
bstack11l11l11l1_opy_ = None
bstack11l11lll1_opy_ = None
bstack111l11l1l_opy_ = None
bstack1l11l1l1_opy_ = None
bstack1ll1l1111_opy_ = None
bstack11ll11ll1l_opy_ = None
FRAMEWORK_NAME = bstack1111l_opy_ (u"ࠩࠪ⚉")
CONFIG = {}
bstack1l1111111l_opy_ = False
bstack11l11lll11_opy_ = bstack1111l_opy_ (u"ࠪࠫ⚊")
bstack1l1l111ll_opy_ = bstack1111l_opy_ (u"ࠫࠬ⚋")
PARALLELISE_VANILLA_PYTHON = False
bstack1l1lll1ll_opy_ = []
bstack111l11lll1_opy_ = bstack11l1111lll_opy_
bstack1ll1l1l11l1l_opy_ = bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⚌")
bstack111l1l111_opy_ = {}
SESSION_NAME = None
bstack1l1ll1ll_opy_ = False
logger = logger_utils.get_logger(__name__, bstack111l11lll1_opy_)
store = {
    bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⚍"): []
}
bstack1ll1l1ll11l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111111111_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1lll11l1_opy_(
    test_framework_name=bstack11lll11ll1_opy_[bstack1111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ⚎")] if bstack111ll11ll1_opy_() else bstack11lll11ll1_opy_[bstack1111l_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨ⚏")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack1ll11lll_opy_):
    try:
        page.evaluate(bstack1111l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ⚐"),
                      bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧ⚑") + json.dumps(
                          bstack1ll11lll_opy_) + bstack1111l_opy_ (u"ࠦࢂࢃࠢ⚒"))
    except Exception as e:
        print(bstack1111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ⚓"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1111l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⚔"), bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ⚕") + json.dumps(
            message) + bstack1111l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫ⚖") + json.dumps(level) + bstack1111l_opy_ (u"ࠩࢀࢁࠬ⚗"))
    except Exception as e:
        print(bstack1111l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨ⚘"), e)
def pytest_configure(config):
    global bstack11l11lll11_opy_
    global CONFIG
    global_config = Config.get_instance()
    config.args = bstack11l11ll1l1_opy_.bstack1ll1l1llll1l_opy_(config.args)
    global_config.bstack111lllll11_opy_(bstack1ll111llll_opy_(config.getoption(bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ⚙"))))
    try:
        logger_utils.bstack1llllll11l11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1111ll11_opy_.invoke(Events.CONNECT, bstack1lllll111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⚚"), bstack1111l_opy_ (u"࠭࠰ࠨ⚛")))
        config = json.loads(os.environ.get(bstack1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ⚜"), bstack1111l_opy_ (u"ࠣࡽࢀࠦ⚝")))
        cli.bstack1ll11111ll1_opy_(bstack1ll11l111l_opy_(bstack11l11lll11_opy_, CONFIG), cli_context.platform_index, bstack1l11l1111l_opy_)
    if cli.bstack1lllll1ll_opy_(bstack11l1l111ll_opy_):
        cli.bstack1ll1llll1l_opy_()
        logger.debug(bstack1111l_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣ⚞") + str(cli_context.platform_index) + bstack1111l_opy_ (u"ࠥࠦ⚟"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤ⚠"), None)
    if cli.is_running() and when == bstack1111l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ⚡"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1111l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⚢"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⚣")))
        if not passed:
            config = json.loads(os.environ.get(bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢ⚤"), bstack1111l_opy_ (u"ࠤࡾࢁࠧ⚥")))
            if bstack11ll11l11l_opy_.bstack11lllll111_opy_(config):
                bstack1lll1l1lll1l_opy_ = bstack11ll11l11l_opy_.bstack1l11l11l1l_opy_(config)
                if item.execution_count > bstack1lll1l1lll1l_opy_:
                    print(bstack1111l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡳࡧࡷࡶ࡮࡫ࡳ࠻ࠢࠪ⚦"), report.nodeid, os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⚧")))
                    bstack11ll11l11l_opy_.bstack1lllll1111ll_opy_(report.nodeid)
            else:
                print(bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠬ⚨"), report.nodeid, os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⚩")))
                bstack11ll11l11l_opy_.bstack1lllll1111ll_opy_(report.nodeid)
        else:
            print(bstack1111l_opy_ (u"ࠧࡕࡧࡶࡸࠥࡶࡡࡴࡵࡨࡨ࠿ࠦࠧ⚪"), report.nodeid, os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⚫")))
    if cli.is_running():
        if when == bstack1111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ⚬"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack1111l_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⚭"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⚮"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⚯"))
    plugins = item.config.getoption(bstack1111l_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢ⚰"))
    report = outcome.get_result()
    os.environ[bstack1111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⚱")] = report.nodeid
    bstack1ll1l1ll11ll_opy_(item, call, report)
    if bstack1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨ⚲") not in plugins or bstack111ll11ll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111l_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥ⚳"), None)
    page = getattr(item, bstack1111l_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤ⚴"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1l1l111ll_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1l1ll1l1l_opy_(item, report, summary, skipSessionName)
def bstack1ll1l1l111ll_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⚵") and report.skipped:
        bstack1lll11ll1111_opy_(report)
    if report.when in [bstack1111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⚶"), bstack1111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ⚷")]:
        return
    if not bstack111l1ll11l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ⚸")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⚹") + json.dumps(
                    report.nodeid) + bstack1111l_opy_ (u"ࠩࢀࢁࠬ⚺"))
        os.environ[bstack1111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⚻")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦ⚼").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⚽")))
    bstack1111l1lll_opy_ = bstack1111l_opy_ (u"ࠨࠢ⚾")
    bstack1lll11ll1111_opy_(report)
    if not passed:
        try:
            bstack1111l1lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ⚿").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1111l1lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1111l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⛀")))
        bstack1111l1lll_opy_ = bstack1111l_opy_ (u"ࠤࠥ⛁")
        if not passed:
            try:
                bstack1111l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⛂").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1111l1lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⛃")
                    + json.dumps(bstack1111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨ⛄"))
                    + bstack1111l_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ⛅")
                )
            else:
                item._driver.execute_script(
                    bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ⛆")
                    + json.dumps(str(bstack1111l1lll_opy_))
                    + bstack1111l_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ⛇")
                )
        except Exception as e:
            summary.append(bstack1111l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢ⛈").format(e))
def bstack1ll1l1l1111l_opy_(test_name, error_message):
    try:
        bstack1ll1l1l1l111_opy_ = []
        bstack111l11l1ll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⛉"), bstack1111l_opy_ (u"ࠫ࠵࠭⛊"))
        bstack1111lllll1_opy_ = {bstack1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⛋"): test_name, bstack1111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⛌"): error_message, bstack1111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⛍"): bstack111l11l1ll_opy_}
        bstack1ll1l1l111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⛎"))
        if os.path.exists(bstack1ll1l1l111l1_opy_):
            with open(bstack1ll1l1l111l1_opy_) as f:
                bstack1ll1l1l1l111_opy_ = json.load(f)
        bstack1ll1l1l1l111_opy_.append(bstack1111lllll1_opy_)
        with open(bstack1ll1l1l111l1_opy_, bstack1111l_opy_ (u"ࠩࡺࠫ⛏")) as f:
            json.dump(bstack1ll1l1l1l111_opy_, f)
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨ⛐") + str(e))
def bstack1ll1l1ll1l1l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⛑"), bstack1111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⛒")]:
        return
    if (str(skipSessionName).lower() != bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ⛓")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⛔")))
    bstack1111l1lll_opy_ = bstack1111l_opy_ (u"ࠣࠤ⛕")
    bstack1lll11ll1111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1111l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⛖").format(e)
                )
        try:
            if passed:
                bstack1l111l11ll_opy_(getattr(item, bstack1111l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⛗"), None), bstack1111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ⛘"))
            else:
                error_message = bstack1111l_opy_ (u"ࠬ࠭⛙")
                if bstack1111l1lll_opy_:
                    playwright_annotate(item._page, str(bstack1111l1lll_opy_), bstack1111l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ⛚"))
                    bstack1l111l11ll_opy_(getattr(item, bstack1111l_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭⛛"), None), bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ⛜"), str(bstack1111l1lll_opy_))
                    error_message = str(bstack1111l1lll_opy_)
                else:
                    bstack1l111l11ll_opy_(getattr(item, bstack1111l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⛝"), None), bstack1111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ⛞"))
                bstack1ll1l1l1111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣ⛟").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1111l_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ⛠"), default=bstack1111l_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ⛡"), help=bstack1111l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ⛢"))
    parser.addoption(bstack1111l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ⛣"), default=bstack1111l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⛤"), help=bstack1111l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⛥"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111l_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨ⛦"), action=bstack1111l_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦ⛧"), default=bstack1111l_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨ⛨"),
                         help=bstack1111l_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨ⛩"))
def bstack111111l1l1_opy_(log):
    if not (log[bstack1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⛪")] and log[bstack1111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⛫")].strip()):
        return
    active = bstack1111111lll_opy_()
    log = {
        bstack1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⛬"): log[bstack1111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⛭")],
        bstack1111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⛮"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"࡚࠭ࠨ⛯"),
        bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⛰"): log[bstack1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⛱")],
    }
    if active:
        if active[bstack1111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⛲")] == bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⛳"):
            log[bstack1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⛴")] = active[bstack1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⛵")]
        elif active[bstack1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⛶")] == bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࠬ⛷"):
            log[bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⛸")] = active[bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⛹")]
    TestHubHandler.bstack1l1l1111l_opy_([log])
def bstack1111111lll_opy_():
    if len(store[bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⛺")]) > 0 and store[bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⛻")][-1]:
        return {
            bstack1111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⛼"): bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⛽"),
            bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⛾"): store[bstack1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⛿")][-1]
        }
    if store.get(bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭✀"), None):
        return {
            bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ✁"): bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ✂"),
            bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ✃"): store[bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ✄")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, item)
        return
    try:
        global CONFIG
        item._1ll1l1ll1ll1_opy_ = True
        bstack1lllll1l1_opy_ = a11y.is_enabled_testcase(bstack1111l1l1ll1_opy_(item.own_markers))
        if not cli.bstack1lllll1ll_opy_(bstack11l1l111ll_opy_):
            item._a11y_test_case = bstack1lllll1l1_opy_
            if bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭✅"), None):
                driver = getattr(item, bstack1111l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ✆"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack1lllll1l1_opy_)
        if not TestHubHandler.on() or bstack1ll1l1l11l1l_opy_ != bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ✇"):
            return
        global current_test_uuid #, bstack11111ll1l1_opy_
        bstack1lllll1l11l_opy_ = {
            bstack1111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ✈"): uuid4().__str__(),
            bstack1111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ✉"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠬࡠࠧ✊")
        }
        current_test_uuid = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ✋")]
        store[bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ✌")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭✍")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111111111_opy_[item.nodeid] = {**_1111111111_opy_[item.nodeid], **bstack1lllll1l11l_opy_}
        bstack1ll1l11lllll_opy_(item, _1111111111_opy_[item.nodeid], bstack1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ✎"))
    except Exception as err:
        print(bstack1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬ✏"), str(err))
def pytest_runtest_setup(item):
    store[bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ✐")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ✑"))
    if bstack11ll11l11l_opy_.bstack1llll1llll1l_opy_():
            bstack1ll1l1ll1l11_opy_ = bstack1111l_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡡࡴࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥ✒")
            logger.error(bstack1ll1l1ll1l11_opy_)
            bstack1lllll1l11l_opy_ = {
                bstack1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ✓"): uuid4().__str__(),
                bstack1111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ✔"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠩ࡝ࠫ✕"),
                bstack1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ✖"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠫ࡟࠭✗"),
                bstack1111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ✘"): bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ✙"),
                bstack1111l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ✚"): bstack1ll1l1ll1l11_opy_,
                bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ✛"): [],
                bstack1111l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ✜"): []
            }
            bstack1ll1l11lllll_opy_(item, bstack1lllll1l11l_opy_, bstack1111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ✝"))
            pytest.skip(bstack1ll1l1ll1l11_opy_)
            return # skip all existing operations
    global bstack1ll1l1ll11l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11111l11l11_opy_():
        atexit.register(bstack11l11l1l1_opy_)
        if not bstack1ll1l1ll11l1_opy_:
            try:
                bstack1ll1l1ll111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11111l11111_opy_():
                    bstack1ll1l1ll111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1l1ll111l_opy_:
                    signal.signal(s, bstack1llll1l1l11_opy_)
                bstack1ll1l1ll11l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧ✞") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11l1ll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ✟")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lllll1l11l_opy_ = {
            bstack1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ✠"): uuid,
            bstack1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ✡"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠨ࡜ࠪ✢"),
            bstack1111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ✣"): bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ✤"),
            bstack1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ✥"): bstack1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ✦"),
            bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ✧"): bstack1111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭✨")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ✩")] = item
        store[bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭✪")] = [uuid]
        if not _1111111111_opy_.get(item.nodeid, None):
            _1111111111_opy_[item.nodeid] = {bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ✫"): [], bstack1111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭✬"): []}
        _1111111111_opy_[item.nodeid][bstack1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ✭")].append(bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ✮")])
        _1111111111_opy_[item.nodeid + bstack1111l_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧ✯")] = bstack1lllll1l11l_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1l1l11ll1_opy_(item, bstack1lllll1l11l_opy_, bstack1111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ✰"))
    except Exception as err:
        print(bstack1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ✱"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ✲"))
        return # skip all existing operations
    try:
        global bstack111l1l111_opy_
        bstack111l11l1ll_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack111l11l1ll_opy_ = int(os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ✳")))
        if bstack1llll111ll_opy_.bstack1l11111l1l_opy_() == bstack1111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ✴"):
            if bstack1llll111ll_opy_.bstack11l11l11_opy_() == bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ✵"):
                bstack1ll1l1l1lll1_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ✶"), None)
                bstack1111ll1l_opy_ = bstack1ll1l1l1lll1_opy_ + bstack1111l_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ✷")
                driver = getattr(item, bstack1111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ✸"), None)
                bstack111llll1_opy_ = getattr(item, bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ✹"), None)
                bstack1l111lll1l_opy_ = getattr(item, bstack1111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ✺"), None)
                PercySDK.screenshot(driver, bstack1111ll1l_opy_, bstack111llll1_opy_=bstack111llll1_opy_, bstack1l111lll1l_opy_=bstack1l111lll1l_opy_, bstack11lllllll_opy_=bstack111l11l1ll_opy_)
        if not cli.bstack1lllll1ll_opy_(bstack11l1l111ll_opy_):
            if getattr(item, bstack1111l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬ✻"), False):
                bstack11l11llll1_opy_.bstack11l11l111_opy_(getattr(item, bstack1111l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ✼"), None), bstack111l1l111_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lllll1l11l_opy_ = {
            bstack1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ✽"): uuid4().__str__(),
            bstack1111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ✾"): bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠩ࡝ࠫ✿"),
            bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ❀"): bstack1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ❁"),
            bstack1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ❂"): bstack1111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ❃"),
            bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ❄"): bstack1111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ❅")
        }
        _1111111111_opy_[item.nodeid + bstack1111l_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬ❆")] = bstack1lllll1l11l_opy_
        bstack1ll1l1l11ll1_opy_(item, bstack1lllll1l11l_opy_, bstack1111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ❇"))
    except Exception as err:
        print(bstack1111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪ❈"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lll11l1l11l_opy_(fixturedef.argname):
        store[bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ❉")] = request.node
    elif bstack1lll11l11ll1_opy_(fixturedef.argname):
        store[bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ❊")] = request.node
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
            bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ❋"): fixturedef.argname,
            bstack1111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ❌"): bstack1111lll1l11_opy_(outcome),
            bstack1111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ❍"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ❎")]
        if not _1111111111_opy_.get(current_test_item.nodeid, None):
            _1111111111_opy_[current_test_item.nodeid] = {bstack1111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭❏"): []}
        _1111111111_opy_[current_test_item.nodeid][bstack1111l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ❐")].append(fixture)
    except Exception as err:
        logger.debug(bstack1111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ❑"), str(err))
if bstack111ll11ll1_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1111111111_opy_[request.node.nodeid][bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ❒")].bstack1ll1l111l_opy_(id(step))
        except Exception as err:
            print(bstack1111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭❓"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1111111111_opy_[request.node.nodeid][bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ❔")].bstack11111ll11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ❕"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            test_data: TestData = _1111111111_opy_[request.node.nodeid][bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ❖")]
            test_data.bstack11111ll11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ❗"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1l1l11l1l_opy_
        try:
            if not TestHubHandler.on() or bstack1ll1l1l11l1l_opy_ != bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ❘"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭❙"), None)
            if not _1111111111_opy_.get(request.node.nodeid, None):
                _1111111111_opy_[request.node.nodeid] = {}
            test_data = TestData.bstack1lll11111l1l_opy_(
                scenario, feature, request.node,
                name=bstack1lll11l11l11_opy_(request.node, scenario),
                started_at=current_time(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ❚"),
                tags=bstack1lll11l1llll_opy_(feature, scenario),
                integrations=TestHubHandler.bstack11111ll1ll_opy_(driver) if driver and driver.session_id else {}
            )
            _1111111111_opy_[request.node.nodeid][bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ❛")] = test_data
            bstack1ll1l1lll1ll_opy_(test_data.uuid)
            TestHubHandler.send_run_event(bstack1111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ❜"), test_data)
        except Exception as err:
            print(bstack1111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭❝"), str(err))
def bstack1ll1l1l11lll_opy_(bstack11111l111l_opy_):
    if bstack11111l111l_opy_ in store[bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ❞")]:
        store[bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ❟")].remove(bstack11111l111l_opy_)
def bstack1ll1l1lll1ll_opy_(test_uuid):
    store[bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ❠")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll1ll1l1111_opy_
def bstack1ll1l1ll11ll_opy_(item, call, report):
    logger.debug(bstack1111l_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡳࡶࠪ❡"))
    global bstack1ll1l1l11l1l_opy_
    bstack11lll1l1ll_opy_ = current_time()
    if hasattr(report, bstack1111l_opy_ (u"ࠩࡶࡸࡴࡶࠧ❢")):
        bstack11lll1l1ll_opy_ = bstack11111l1ll1l_opy_(report.stop)
    elif hasattr(report, bstack1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ❣")):
        bstack11lll1l1ll_opy_ = bstack11111l1ll1l_opy_(report.start)
    try:
        if getattr(report, bstack1111l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ❤"), bstack1111l_opy_ (u"ࠬ࠭❥")) == bstack1111l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ❦"):
            logger.debug(bstack1111l_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ❧").format(getattr(report, bstack1111l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭❨"), bstack1111l_opy_ (u"ࠩࠪ❩")).__str__(), bstack1ll1l1l11l1l_opy_))
            if bstack1ll1l1l11l1l_opy_ == bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ❪"):
                _1111111111_opy_[item.nodeid][bstack1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ❫")] = bstack11lll1l1ll_opy_
                bstack1ll1l11lllll_opy_(item, _1111111111_opy_[item.nodeid], bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ❬"), report, call)
                store[bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ❭")] = None
            elif bstack1ll1l1l11l1l_opy_ == bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ❮"):
                test_data = _1111111111_opy_[item.nodeid][bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ❯")]
                test_data.set(hooks=_1111111111_opy_[item.nodeid].get(bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ❰"), []))
                exception, bstack11111l1111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11111l1111_opy_ = [call.excinfo.exconly(), getattr(report, bstack1111l_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩ❱"), bstack1111l_opy_ (u"ࠫࠬ❲"))]
                test_data.stop(time=bstack11lll1l1ll_opy_, result=Result(result=getattr(report, bstack1111l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭❳"), bstack1111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭❴")), exception=exception, bstack11111l1111_opy_=bstack11111l1111_opy_))
                TestHubHandler.send_run_event(bstack1111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ❵"), _1111111111_opy_[item.nodeid][bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ❶")])
        elif getattr(report, bstack1111l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ❷"), bstack1111l_opy_ (u"ࠪࠫ❸")) in [bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ❹"), bstack1111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ❺")]:
            logger.debug(bstack1111l_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ❻").format(getattr(report, bstack1111l_opy_ (u"ࠧࡸࡪࡨࡲࠬ❼"), bstack1111l_opy_ (u"ࠨࠩ❽")).__str__(), bstack1ll1l1l11l1l_opy_))
            bstack111111l111_opy_ = item.nodeid + bstack1111l_opy_ (u"ࠩ࠰ࠫ❾") + getattr(report, bstack1111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ❿"), bstack1111l_opy_ (u"ࠫࠬ➀"))
            if getattr(report, bstack1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭➁"), False):
                hook_type = bstack1111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ➂") if getattr(report, bstack1111l_opy_ (u"ࠧࡸࡪࡨࡲࠬ➃"), bstack1111l_opy_ (u"ࠨࠩ➄")) == bstack1111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ➅") else bstack1111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ➆")
                _1111111111_opy_[bstack111111l111_opy_] = {
                    bstack1111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ➇"): uuid4().__str__(),
                    bstack1111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ➈"): bstack11lll1l1ll_opy_,
                    bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ➉"): hook_type
                }
            _1111111111_opy_[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ➊")] = bstack11lll1l1ll_opy_
            bstack1ll1l1l11lll_opy_(_1111111111_opy_[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭➋")])
            bstack1ll1l1l11ll1_opy_(item, _1111111111_opy_[bstack111111l111_opy_], bstack1111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ➌"), report, call)
            if getattr(report, bstack1111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ➍"), bstack1111l_opy_ (u"ࠫࠬ➎")) == bstack1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ➏"):
                if getattr(report, bstack1111l_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ➐"), bstack1111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ➑")) == bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ➒"):
                    bstack1lllll1l11l_opy_ = {
                        bstack1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ➓"): uuid4().__str__(),
                        bstack1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ➔"): current_time(),
                        bstack1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ➕"): current_time()
                    }
                    _1111111111_opy_[item.nodeid] = {**_1111111111_opy_[item.nodeid], **bstack1lllll1l11l_opy_}
                    bstack1ll1l11lllll_opy_(item, _1111111111_opy_[item.nodeid], bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭➖"))
                    bstack1ll1l11lllll_opy_(item, _1111111111_opy_[item.nodeid], bstack1111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ➗"), report, call)
    except Exception as err:
        print(bstack1111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬ➘"), str(err))
def bstack1ll1l1lll111_opy_(test, bstack1lllll1l11l_opy_, result=None, call=None, bstack111lll11l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    test_data = {
        bstack1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭➙"): bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ➚")],
        bstack1111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ➛"): bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ➜"),
        bstack1111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ➝"): test.name,
        bstack1111l_opy_ (u"࠭ࡢࡰࡦࡼࠫ➞"): {
            bstack1111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ➟"): bstack1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ➠"),
            bstack1111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ➡"): inspect.getsource(test.obj)
        },
        bstack1111l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ➢"): test.name,
        bstack1111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ➣"): test.name,
        bstack1111l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ➤"): bstack11l11ll1l1_opy_.bstack1lllll11ll1_opy_(test),
        bstack1111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ➥"): file_path,
        bstack1111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ➦"): file_path,
        bstack1111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ➧"): bstack1111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ➨"),
        bstack1111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ➩"): file_path,
        bstack1111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ➪"): bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ➫")],
        bstack1111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ➬"): bstack1111l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ➭"),
        bstack1111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ➮"): {
            bstack1111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭➯"): test.nodeid
        },
        bstack1111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ➰"): bstack1111l1l1ll1_opy_(test.own_markers)
    }
    if bstack111lll11l_opy_ in [bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ➱"), bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ➲")]:
        test_data[bstack1111l_opy_ (u"࠭࡭ࡦࡶࡤࠫ➳")] = {
            bstack1111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ➴"): bstack1lllll1l11l_opy_.get(bstack1111l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ➵"), [])
        }
    if bstack111lll11l_opy_ == bstack1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ➶"):
        test_data[bstack1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ➷")] = bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ➸")
        test_data[bstack1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ➹")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ➺")]
        test_data[bstack1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ➻")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭➼")]
    if result:
        test_data[bstack1111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ➽")] = result.outcome
        test_data[bstack1111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ➾")] = result.duration * 1000
        test_data[bstack1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ➿")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⟀")]
        if result.failed:
            test_data[bstack1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⟁")] = TestHubHandler.bstack1lll11l1l1l_opy_(call.excinfo.typename)
            test_data[bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⟂")] = TestHubHandler.bstack1ll1lll111l1_opy_(call.excinfo, result)
        test_data[bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⟃")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⟄")]
    if outcome:
        test_data[bstack1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⟅")] = bstack1111lll1l11_opy_(outcome)
        test_data[bstack1111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⟆")] = 0
        test_data[bstack1111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⟇")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⟈")]
        if test_data[bstack1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⟉")] == bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⟊"):
            test_data[bstack1111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⟋")] = bstack1111l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ⟌")  # bstack1ll1l1l11111_opy_
            test_data[bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⟍")] = [{bstack1111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⟎"): [bstack1111l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ⟏")]}]
        test_data[bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⟐")] = bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⟑")]
    return test_data
def bstack1ll1l1lll1l1_opy_(test, bstack1llll1ll1ll_opy_, bstack111lll11l_opy_, result, call, outcome, bstack1ll1l1l1l1ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⟒")]
    hook_name = bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⟓")]
    hook_data = {
        bstack1111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⟔"): bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⟕")],
        bstack1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⟖"): bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⟗"),
        bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⟘"): bstack1111l_opy_ (u"ࠩࡾࢁࠬ⟙").format(bstack1lll11l1l1l1_opy_(hook_name)),
        bstack1111l_opy_ (u"ࠪࡦࡴࡪࡹࠨ⟚"): {
            bstack1111l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⟛"): bstack1111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⟜"),
            bstack1111l_opy_ (u"࠭ࡣࡰࡦࡨࠫ⟝"): None
        },
        bstack1111l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⟞"): test.name,
        bstack1111l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⟟"): bstack11l11ll1l1_opy_.bstack1lllll11ll1_opy_(test, hook_name),
        bstack1111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⟠"): file_path,
        bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⟡"): file_path,
        bstack1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⟢"): bstack1111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⟣"),
        bstack1111l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⟤"): file_path,
        bstack1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⟥"): bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⟦")],
        bstack1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⟧"): bstack1111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ⟨") if bstack1ll1l1l11l1l_opy_ == bstack1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ⟩") else bstack1111l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⟪"),
        bstack1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⟫"): hook_type
    }
    bstack1l1l11l1l1l_opy_ = bstack1lllll11l1l_opy_(_1111111111_opy_.get(test.nodeid, None))
    if bstack1l1l11l1l1l_opy_:
        hook_data[bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⟬")] = bstack1l1l11l1l1l_opy_
    if result:
        hook_data[bstack1111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⟭")] = result.outcome
        hook_data[bstack1111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⟮")] = result.duration * 1000
        hook_data[bstack1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⟯")] = bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⟰")]
        if result.failed:
            hook_data[bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⟱")] = TestHubHandler.bstack1lll11l1l1l_opy_(call.excinfo.typename)
            hook_data[bstack1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⟲")] = TestHubHandler.bstack1ll1lll111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⟳")] = bstack1111lll1l11_opy_(outcome)
        hook_data[bstack1111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⟴")] = 100
        hook_data[bstack1111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⟵")] = bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⟶")]
        if hook_data[bstack1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⟷")] == bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⟸"):
            hook_data[bstack1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⟹")] = bstack1111l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⟺")  # bstack1ll1l1l11111_opy_
            hook_data[bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⟻")] = [{bstack1111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⟼"): [bstack1111l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⟽")]}]
    if bstack1ll1l1l1l1ll_opy_:
        hook_data[bstack1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⟾")] = bstack1ll1l1l1l1ll_opy_.result
        hook_data[bstack1111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⟿")] = time_diff(bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⠀")], bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⠁")])
        hook_data[bstack1111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⠂")] = bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⠃")]
        if hook_data[bstack1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⠄")] == bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⠅"):
            hook_data[bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⠆")] = TestHubHandler.bstack1lll11l1l1l_opy_(bstack1ll1l1l1l1ll_opy_.exception_type)
            hook_data[bstack1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⠇")] = [{bstack1111l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⠈"): bstack1111l1l111l_opy_(bstack1ll1l1l1l1ll_opy_.exception)}]
    return hook_data
def bstack1ll1l11lllll_opy_(test, bstack1lllll1l11l_opy_, bstack111lll11l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1111l_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ⠉").format(bstack111lll11l_opy_))
    test_data = bstack1ll1l1lll111_opy_(test, bstack1lllll1l11l_opy_, result, call, bstack111lll11l_opy_, outcome)
    driver = getattr(test, bstack1111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⠊"), None)
    if bstack111lll11l_opy_ == bstack1111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⠋") and driver:
        test_data[bstack1111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⠌")] = TestHubHandler.bstack11111ll1ll_opy_(driver)
    if bstack111lll11l_opy_ == bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⠍"):
        bstack111lll11l_opy_ = bstack1111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⠎")
    bstack1llll1lll1l_opy_ = {
        bstack1111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⠏"): bstack111lll11l_opy_,
        bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⠐"): test_data
    }
    TestHubHandler.bstack111lllllll_opy_(bstack1llll1lll1l_opy_)
    if bstack111lll11l_opy_ == bstack1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⠑"):
        threading.current_thread().bstackTestMeta = {bstack1111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⠒"): bstack1111l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⠓")}
    elif bstack111lll11l_opy_ == bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⠔"):
        threading.current_thread().bstackTestMeta = {bstack1111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⠕"): getattr(result, bstack1111l_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⠖"), bstack1111l_opy_ (u"ࠨࠩ⠗"))}
def bstack1ll1l1l11ll1_opy_(test, bstack1lllll1l11l_opy_, bstack111lll11l_opy_, result=None, call=None, outcome=None, bstack1ll1l1l1l1ll_opy_=None):
    logger.debug(bstack1111l_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⠘").format(bstack111lll11l_opy_))
    hook_data = bstack1ll1l1lll1l1_opy_(test, bstack1lllll1l11l_opy_, bstack111lll11l_opy_, result, call, outcome, bstack1ll1l1l1l1ll_opy_)
    bstack1llll1lll1l_opy_ = {
        bstack1111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⠙"): bstack111lll11l_opy_,
        bstack1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭⠚"): hook_data
    }
    TestHubHandler.bstack111lllllll_opy_(bstack1llll1lll1l_opy_)
def bstack1lllll11l1l_opy_(bstack1lllll1l11l_opy_):
    if not bstack1lllll1l11l_opy_:
        return None
    if bstack1lllll1l11l_opy_.get(bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⠛"), None):
        return getattr(bstack1lllll1l11l_opy_[bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⠜")], bstack1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⠝"), None)
    return bstack1lllll1l11l_opy_.get(bstack1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⠞"), None)
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
        places = [bstack1111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⠟"), bstack1111l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⠠"), bstack1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⠡")]
        logs = []
        for bstack1ll1l1ll1111_opy_ in places:
            records = caplog.get_records(bstack1ll1l1ll1111_opy_)
            bstack1ll1l1l1ll1l_opy_ = bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⠢") if bstack1ll1l1ll1111_opy_ == bstack1111l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⠣") else bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⠤")
            bstack1ll1l1lll11l_opy_ = request.node.nodeid + (bstack1111l_opy_ (u"ࠨࠩ⠥") if bstack1ll1l1ll1111_opy_ == bstack1111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⠦") else bstack1111l_opy_ (u"ࠪ࠱ࠬ⠧") + bstack1ll1l1ll1111_opy_)
            test_uuid = bstack1lllll11l1l_opy_(_1111111111_opy_.get(bstack1ll1l1lll11l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1111l1lllll_opy_(record.message):
                    continue
                logs.append({
                    bstack1111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⠨"): bstack11111ll1l1l_opy_(record.created).isoformat() + bstack1111l_opy_ (u"ࠬࡠࠧ⠩"),
                    bstack1111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⠪"): record.levelname,
                    bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⠫"): record.message,
                    bstack1ll1l1l1ll1l_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1l1l1111l_opy_(logs)
    except Exception as err:
        print(bstack1111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ⠬"), str(err))
def bstack1l11l1llll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1ll1ll_opy_
    bstack1llllll11l_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭⠭"), None) and bstack1l11l11l11_opy_(
            threading.current_thread(), bstack1111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⠮"), None)
    bstack1l1ll111ll_opy_ = getattr(driver, bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⠯"), None) != None and getattr(driver, bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⠰"), None) == True
    if sequence == bstack1111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⠱") and driver != None:
      if not bstack1l1ll1ll_opy_ and bstack111l1ll11l_opy_() and bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⠲") in CONFIG and CONFIG[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⠳")] == True and accessibility_scripts.bstack11ll1l1l11_opy_(driver_command) and (bstack1l1ll111ll_opy_ or bstack1llllll11l_opy_) and not bstack1l1l11l11l_opy_(args):
        try:
          bstack1l1ll1ll_opy_ = True
          logger.debug(bstack1111l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ⠴").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨ⠵").format(str(err)))
        bstack1l1ll1ll_opy_ = False
    if sequence == bstack1111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⠶"):
        if driver_command == bstack1111l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ⠷"):
            TestHubHandler.bstack11l1lll1l1_opy_({
                bstack1111l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ⠸"): response[bstack1111l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭⠹")],
                bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⠺"): store[bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⠻")]
            })
def bstack11l11l1l1_opy_():
    global bstack1l1lll1ll_opy_
    logger_utils.bstack11l1l1l1_opy_()
    logging.shutdown()
    TestHubHandler.bstack11111111ll_opy_()
    for driver in bstack1l1lll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l1l11_opy_(*args):
    global bstack1l1lll1ll_opy_
    TestHubHandler.bstack11111111ll_opy_()
    for driver in bstack1l1lll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l11111_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1lll111lll_opy_(self, *args, **kwargs):
    bstack111ll11ll_opy_ = bstack1ll1l1ll_opy_(self, *args, **kwargs)
    bstack1111l111l_opy_ = getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⠼"), None)
    if bstack1111l111l_opy_ and bstack1111l111l_opy_.get(bstack1111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⠽"), bstack1111l_opy_ (u"ࠬ࠭⠾")) == bstack1111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⠿"):
        TestHubHandler.send_cbt_info(self)
    return bstack111ll11ll_opy_
@measure(event_name=EVENTS.bstack111l11111l_opy_, stage=STAGE.bstack1lll1l11ll_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack111lllll1_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.get_instance()
    if global_config.get_property(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⡀")):
        return
    global_config.bstack1ll1111l11_opy_(bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⡁"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack1ll11lll1l_opy_.format(FRAMEWORK_NAME.split(bstack1111l_opy_ (u"ࠩ࠰ࠫ⡂"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111l1ll11l_opy_():
            Service.start = bstack1l11l111_opy_
            Service.stop = bstack11lll1l11l_opy_
            webdriver.Remote.get = bstack11ll1ll1_opy_
            webdriver.Remote.__init__ = bstack1l11l111ll_opy_
            if not isinstance(os.getenv(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ⡃")), str):
                return
            WebDriver.quit = bstack11l1l1ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1lll111lll_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1111l_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⡄")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1111l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ⡅")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack11ll1ll11l_opy_(bstack1111l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ⡆"), bstack111111ll_opy_)
    if bstack1l1ll1l11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1111l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⡇")) and callable(getattr(RemoteConnection, bstack1111l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⡈"))):
                RemoteConnection._get_proxy_url = bstack1111l11ll1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1111l11ll1_opy_
        except Exception as e:
            logger.error(bstack111l1lllll_opy_.format(str(e)))
    if bstack1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⡉") in str(framework_name).lower():
        if not bstack111l1ll11l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1111ll11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l11_opy_
            Config.getoption = bstack1l1111ll1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l1ll1111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11111ll1l_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack11l1l1ll_opy_(self):
    global FRAMEWORK_NAME
    global bstack1lll11111_opy_
    global bstack11l1ll11l_opy_
    try:
        if bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⡊") in FRAMEWORK_NAME and self.session_id != None and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ⡋"), bstack1111l_opy_ (u"ࠬ࠭⡌")) != bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⡍"):
            bstack11l1l1llll_opy_ = bstack1111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⡎") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⡏")
            bstack1111l1ll1_opy_(logger, True)
            if os.environ.get(bstack1111l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⡐"), None):
                self.execute_script(
                    bstack1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ⡑") + json.dumps(
                        os.environ.get(bstack1111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⡒"))) + bstack1111l_opy_ (u"ࠬࢃࡽࠨ⡓"))
            if self != None:
                bstack1ll1111l1l_opy_(self, bstack11l1l1llll_opy_, bstack1111l_opy_ (u"࠭ࠬࠡࠩ⡔").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lllll1ll_opy_(bstack11l1l111ll_opy_):
            item = store.get(bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⡕"), None)
            if item is not None and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⡖"), None):
                bstack11l11llll1_opy_.bstack11l11l111_opy_(self, bstack111l1l111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1111l_opy_ (u"ࠩࠪ⡗")
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ⡘") + str(e))
    bstack11l1ll11l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1lll111_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack1l11l111ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll11111_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1ll1l1ll_opy_
    global bstack1l1lll1ll_opy_
    global bstack11l11lll11_opy_
    global bstack1l1l111ll_opy_
    global bstack111l1l111_opy_
    CONFIG[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⡙")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack1ll11l111l_opy_(bstack11l11lll11_opy_, CONFIG)
    logger.debug(bstack11l1l1l1l1_opy_.format(command_executor))
    proxy = bstack11l11l1ll_opy_(CONFIG, proxy)
    bstack111l11l1ll_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack111l11l1ll_opy_ = int(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⡚")))
    except:
        bstack111l11l1ll_opy_ = 0
    bstack1ll11lll11_opy_ = get_caps(CONFIG, bstack111l11l1ll_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11lll11_opy_)))
    bstack111l1l111_opy_ = CONFIG.get(bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⡛"))[bstack111l11l1ll_opy_]
    if bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⡜") in CONFIG and CONFIG[bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⡝")]:
        update_caps_for_local(bstack1ll11lll11_opy_, bstack1l1l111ll_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack111l11l1ll_opy_) and a11y.is_platform_supported(bstack1ll11lll11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lllll1ll_opy_(bstack11l1l111ll_opy_):
            a11y.set_capabilities(bstack1ll11lll11_opy_, CONFIG)
    if desired_capabilities:
        bstack1llll111l1_opy_ = bstack1ll1lll1l1_opy_(desired_capabilities)
        bstack1llll111l1_opy_[bstack1111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⡞")] = bstack11l1111l_opy_(CONFIG)
        bstack1llll1ll_opy_ = get_caps(bstack1llll111l1_opy_)
        if bstack1llll1ll_opy_:
            bstack1ll11lll11_opy_ = update(bstack1llll1ll_opy_, bstack1ll11lll11_opy_)
        desired_capabilities = None
    if options:
        bstack1111l11ll_opy_(options, bstack1ll11lll11_opy_)
    if not options:
        options = bstack1l11l1111l_opy_(bstack1ll11lll11_opy_)
    if proxy and bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⡟")):
        options.proxy(proxy)
    if options and bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⡠")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1ll1ll1l_opy_() < version.parse(bstack1111l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⡡")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll11lll11_opy_)
    logger.info(bstack111l11l11_opy_)
    bstack111l1l1ll1_opy_.end(EVENTS.bstack111l11111l_opy_.value, EVENTS.bstack111l11111l_opy_.value + bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⡢"),
                               EVENTS.bstack111l11111l_opy_.value + bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⡣"), True, None)
    try:
        if bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⡤")):
            bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⡥")):
            bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ⡦")):
            bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1ll1l1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1111l1l1l_opy_:
        logger.error(bstack111llll11l_opy_.format(bstack1111l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠪ⡧"), str(bstack1111l1l1l_opy_)))
        raise bstack1111l1l1l_opy_
    try:
        bstack11111l1ll_opy_ = bstack1111l_opy_ (u"ࠬ࠭⡨")
        if bstack1l1ll1ll1l_opy_() >= version.parse(bstack1111l_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ⡩")):
            bstack11111l1ll_opy_ = self.caps.get(bstack1111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⡪"))
        else:
            bstack11111l1ll_opy_ = self.capabilities.get(bstack1111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ⡫"))
        if bstack11111l1ll_opy_:
            bstack11ll11111l_opy_(bstack11111l1ll_opy_)
            if bstack1l1ll1ll1l_opy_() <= version.parse(bstack1111l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ⡬")):
                self.command_executor._url = bstack1111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⡭") + bstack11l11lll11_opy_ + bstack1111l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ⡮")
            else:
                self.command_executor._url = bstack1111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ⡯") + bstack11111l1ll_opy_ + bstack1111l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ⡰")
            logger.debug(bstack1l1lll11l_opy_.format(bstack11111l1ll_opy_))
        else:
            logger.debug(bstack1l11lll111_opy_.format(bstack1111l_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ⡱")))
    except Exception as e:
        logger.debug(bstack1l11lll111_opy_.format(e))
    bstack1lll11111_opy_ = self.session_id
    if bstack1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⡲") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⡳"), None)
        if item:
            bstack1ll1l1l1l11l_opy_ = getattr(item, bstack1111l_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⡴"), False)
            if not getattr(item, bstack1111l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⡵"), None) and bstack1ll1l1l1l11l_opy_:
                setattr(store[bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⡶")], bstack1111l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⡷"), self)
        bstack1111l111l_opy_ = getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⡸"), None)
        if bstack1111l111l_opy_ and bstack1111l111l_opy_.get(bstack1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⡹"), bstack1111l_opy_ (u"ࠩࠪ⡺")) == bstack1111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⡻"):
            TestHubHandler.send_cbt_info(self)
    bstack1l1lll1ll_opy_.append(self)
    if bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⡼") in CONFIG and bstack1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⡽") in CONFIG[bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⡾")][bstack111l11l1ll_opy_]:
        SESSION_NAME = CONFIG[bstack1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⡿")][bstack111l11l1ll_opy_][bstack1111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⢀")]
    logger.debug(bstack1l11l1ll11_opy_.format(bstack1lll11111_opy_))
@measure(event_name=EVENTS.bstack1111ll1ll1_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=SESSION_NAME)
def bstack11ll1ll1_opy_(self, url):
    global bstack11l11lll1_opy_
    global CONFIG
    try:
        bstack1l11ll111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1111l111_opy_.format(str(err)))
    try:
        bstack11l11lll1_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack11lll1l1l1_opy_):
                bstack1l11ll111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1111l111_opy_.format(str(err)))
        raise e
def bstack1l1lll1l11_opy_(item, when):
    global bstack1ll1l1111_opy_
    try:
        bstack1ll1l1111_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1ll1111_opy_(item, call, rep):
    global bstack11ll11ll1l_opy_
    global bstack1l1lll1ll_opy_
    name = bstack1111l_opy_ (u"ࠩࠪ⢁")
    try:
        if rep.when == bstack1111l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⢂"):
            bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1111l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⢃"))
            try:
                if (str(skipSessionName).lower() != bstack1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪ⢄")):
                    name = str(rep.nodeid)
                    executor_string = browserstack_executor_helper(bstack1111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⢅"), name, bstack1111l_opy_ (u"ࠧࠨ⢆"), bstack1111l_opy_ (u"ࠨࠩ⢇"), bstack1111l_opy_ (u"ࠩࠪ⢈"), bstack1111l_opy_ (u"ࠪࠫ⢉"))
                    os.environ[bstack1111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⢊")] = name
                    for driver in bstack1l1lll1ll_opy_:
                        if bstack1lll11111_opy_ == driver.session_id:
                            driver.execute_script(executor_string)
            except Exception as e:
                logger.debug(bstack1111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⢋").format(str(e)))
            try:
                bstack111lll111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⢌"):
                    status = bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⢍") if rep.outcome.lower() == bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⢎") else bstack1111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⢏")
                    reason = bstack1111l_opy_ (u"ࠪࠫ⢐")
                    if status == bstack1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⢑"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1111l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ⢒") if status == bstack1111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⢓") else bstack1111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⢔")
                    data = name + bstack1111l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ⢕") if status == bstack1111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⢖") else name + bstack1111l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭⢗") + reason
                    bstack111lll111l_opy_ = browserstack_executor_helper(bstack1111l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭⢘"), bstack1111l_opy_ (u"ࠬ࠭⢙"), bstack1111l_opy_ (u"࠭ࠧ⢚"), bstack1111l_opy_ (u"ࠧࠨ⢛"), level, data)
                    for driver in bstack1l1lll1ll_opy_:
                        if bstack1lll11111_opy_ == driver.session_id:
                            driver.execute_script(bstack111lll111l_opy_)
            except Exception as e:
                logger.debug(bstack1111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⢜").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭⢝").format(str(e)))
    bstack11ll11ll1l_opy_(item, call, rep)
notset = Notset()
def bstack1l1111ll1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11l1l1_opy_
    if str(name).lower() == bstack1111l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ⢞"):
        return bstack1111l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ⢟")
    else:
        return bstack1l11l1l1_opy_(self, name, default, skip)
def bstack1111l11ll1_opy_(self):
    global CONFIG
    global bstack1l1l111l1l_opy_
    try:
        proxy = bstack11ll1lllll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ⢠")):
                proxies = bstack1llll1l1ll_opy_(proxy, bstack1ll11l111l_opy_())
                if len(proxies) > 0:
                    protocol, bstack11llll1l1_opy_ = proxies.popitem()
                    if bstack1111l_opy_ (u"ࠨ࠺࠰࠱ࠥ⢡") in bstack11llll1l1_opy_:
                        return bstack11llll1l1_opy_
                    else:
                        return bstack1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⢢") + bstack11llll1l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ⢣").format(str(e)))
    return bstack1l1l111l1l_opy_(self)
def bstack1l1ll1l11l_opy_():
    return (bstack1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⢤") in CONFIG or bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⢥") in CONFIG) and bstack1l11ll1111_opy_() and bstack1l1ll1ll1l_opy_() >= version.parse(
        bstack11l11ll1_opy_)
def bstack11ll111l1_opy_(self,
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
    CONFIG[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⢦")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack111l11l1ll_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack111l11l1ll_opy_ = int(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⢧")))
    except:
        bstack111l11l1ll_opy_ = 0
    CONFIG[bstack1111l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ⢨")] = True
    bstack1ll11lll11_opy_ = get_caps(CONFIG, bstack111l11l1ll_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll11lll11_opy_)))
    if CONFIG.get(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⢩")):
        update_caps_for_local(bstack1ll11lll11_opy_, bstack1l1l111ll_opy_)
    if bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⢪") in CONFIG and bstack1111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⢫") in CONFIG[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⢬")][bstack111l11l1ll_opy_]:
        SESSION_NAME = CONFIG[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⢭")][bstack111l11l1ll_opy_][bstack1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⢮")]
    import urllib
    import json
    if bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⢯") in CONFIG and str(CONFIG[bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⢰")]).lower() != bstack1111l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⢱"):
        bstack1l11111ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1l11111ll_opy_ + urllib.parse.quote(json.dumps(bstack1ll11lll11_opy_))
    else:
        cdpUrl = bstack1111l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ⢲") + urllib.parse.quote(json.dumps(bstack1ll11lll11_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1111llll_opy_
        if not bstack111l1ll11l_opy_():
            global bstack1l1l1l1l1l_opy_
            if not bstack1l1l1l1l1l_opy_:
                from bstack_utils.helper import bstack1l11ll1ll_opy_, bstack111111l1ll1_opy_
                bstack1l1l1l1l1l_opy_ = bstack1l11ll1ll_opy_()
                bstack111111l1ll1_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1ll1111llll_opy_
            return
        BrowserType.launch = bstack11ll111l1_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll1l1l11l11_opy_():
    global CONFIG
    global bstack1l1111111l_opy_
    global bstack11l11lll11_opy_
    global bstack1l1l111ll_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack111l11lll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ⢳")))
    bstack1l1111111l_opy_ = eval(os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⢴")))
    bstack11l11lll11_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ⢵"))
    bstack1l111l111l_opy_(CONFIG, bstack1l1111111l_opy_)
    bstack111l11lll1_opy_ = logger_utils.configure_logger(CONFIG, bstack111l11lll1_opy_)
    if cli.bstack11l1l111_opy_():
        bstack1111ll11_opy_.invoke(Events.CONNECT, bstack1lllll111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⢶"), bstack1111l_opy_ (u"ࠧ࠱ࠩ⢷")))
        cli.bstack1lll11llll_opy_(cli_context.platform_index)
        cli.bstack1ll11111ll1_opy_(bstack1ll11l111l_opy_(bstack11l11lll11_opy_, CONFIG), cli_context.platform_index, bstack1l11l1111l_opy_)
        cli.bstack1ll1llll1l_opy_()
        logger.debug(bstack1111l_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⢸") + str(cli_context.platform_index) + bstack1111l_opy_ (u"ࠤࠥ⢹"))
        return # skip all existing operations
    global bstack1ll1l1ll_opy_
    global bstack11l1ll11l_opy_
    global bstack1lllllll1_opy_
    global bstack1l1ll1111_opy_
    global bstack1ll1l11ll1_opy_
    global bstack1111111l_opy_
    global bstack11l11l11l1_opy_
    global bstack11l11lll1_opy_
    global bstack1l1l111l1l_opy_
    global bstack1l11l1l1_opy_
    global bstack1ll1l1111_opy_
    global bstack11ll11ll1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1ll1l1ll_opy_ = webdriver.Remote.__init__
        bstack11l1ll11l_opy_ = WebDriver.quit
        bstack11l11l11l1_opy_ = WebDriver.close
        bstack11l11lll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⢺") in CONFIG or bstack1111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⢻") in CONFIG) and bstack1l11ll1111_opy_():
        if bstack1l1ll1ll1l_opy_() < version.parse(bstack11l11ll1_opy_):
            logger.error(bstack1ll1lllll1_opy_.format(bstack1l1ll1ll1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1111l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⢼")) and callable(getattr(RemoteConnection, bstack1111l_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⢽"))):
                    bstack1l1l111l1l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1l111l1l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack111l1lllll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l11l1l1_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll1l1111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1111l_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢ⢾"), bstack111ll11l11_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack11ll11ll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ⢿"))
    bstack1l1l111ll_opy_ = CONFIG.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭⣀"), {}).get(bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⣁"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack111lllll1_opy_(bstack111ll1l11l_opy_)
if (bstack11111l11l11_opy_()):
    bstack1ll1l1l11l11_opy_()
@error_handler(class_method=False)
def bstack1ll1l1l1llll_opy_(hook_name, event, bstack11l1l1ll11l_opy_=None):
    if hook_name not in [bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⣂"), bstack1111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⣃"), bstack1111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⣄"), bstack1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⣅"), bstack1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⣆"), bstack1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⣇"), bstack1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ⣈"), bstack1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⣉")]:
        return
    node = store[bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⣊")]
    if hook_name in [bstack1111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⣋"), bstack1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⣌")]:
        node = store[bstack1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ⣍")]
    elif hook_name in [bstack1111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⣎"), bstack1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⣏")]:
        node = store[bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⣐")]
    hook_type = bstack1lll11l11l1l_opy_(hook_name)
    if event == bstack1111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⣑"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1llll1ll1ll_opy_ = {
            bstack1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⣒"): uuid,
            bstack1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⣓"): current_time(),
            bstack1111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⣔"): bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⣕"),
            bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⣖"): hook_type,
            bstack1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⣗"): hook_name
        }
        store[bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⣘")].append(uuid)
        bstack1ll1l1ll1lll_opy_ = node.nodeid
        if hook_type == bstack1111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⣙"):
            if not _1111111111_opy_.get(bstack1ll1l1ll1lll_opy_, None):
                _1111111111_opy_[bstack1ll1l1ll1lll_opy_] = {bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⣚"): []}
            _1111111111_opy_[bstack1ll1l1ll1lll_opy_][bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⣛")].append(bstack1llll1ll1ll_opy_[bstack1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⣜")])
        _1111111111_opy_[bstack1ll1l1ll1lll_opy_ + bstack1111l_opy_ (u"ࠪ࠱ࠬ⣝") + hook_name] = bstack1llll1ll1ll_opy_
        bstack1ll1l1l11ll1_opy_(node, bstack1llll1ll1ll_opy_, bstack1111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⣞"))
    elif event == bstack1111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ⣟"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l1l1ll11l_opy_)
            return
        bstack111111l111_opy_ = node.nodeid + bstack1111l_opy_ (u"࠭࠭ࠨ⣠") + hook_name
        _1111111111_opy_[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⣡")] = current_time()
        bstack1ll1l1l11lll_opy_(_1111111111_opy_[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⣢")])
        bstack1ll1l1l11ll1_opy_(node, _1111111111_opy_[bstack111111l111_opy_], bstack1111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⣣"), bstack1ll1l1l1l1ll_opy_=bstack11l1l1ll11l_opy_)
def bstack1ll1l1l1ll11_opy_():
    global bstack1ll1l1l11l1l_opy_
    if bstack111ll11ll1_opy_():
        bstack1ll1l1l11l1l_opy_ = bstack1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⣤")
    else:
        bstack1ll1l1l11l1l_opy_ = bstack1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⣥")
@TestHubHandler.bstack1ll1ll1l1111_opy_
def bstack1ll1l1l1l1l1_opy_():
    bstack1ll1l1l1ll11_opy_()
    if cli.is_running():
        try:
            bstack11111111l11_opy_(bstack1ll1l1l1llll_opy_)
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ⣦").format(e))
        return
    if bstack1l11ll1111_opy_():
        global_config = Config.get_instance()
        bstack1111l_opy_ (u"࠭ࠧࠨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡ࠿ࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤ࡬࡫ࡴࡴࠢࡸࡷࡪࡪࠠࡧࡱࡵࠤࡦ࠷࠱ࡺࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠱ࡼࡸࡡࡱࡲ࡬ࡲ࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡷࠤ࡮ࡹࠠࡱࡣࡷࡧ࡭࡫ࡤࠡ࡫ࡱࠤࡦࠦࡤࡪࡨࡩࡩࡷ࡫࡮ࡵࠢࡳࡶࡴࡩࡥࡴࡵࠣ࡭ࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡵࡴࠢࡺࡩࠥࡴࡥࡦࡦࠣࡸࡴࠦࡵࡴࡧࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡕࡧࡴࡤࡪࠫࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡮ࡡ࡯ࡦ࡯ࡩࡷ࠯ࠠࡧࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠧࠨࠩ⣧")
        if global_config.get_property(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⣨")):
            if CONFIG.get(bstack1111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⣩")) is not None and int(CONFIG[bstack1111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⣪")]) > 1:
                bstack1l111l1lll_opy_(bstack1l11l1llll_opy_)
            return
        bstack1l111l1lll_opy_(bstack1l11l1llll_opy_)
    try:
        bstack11111111l11_opy_(bstack1ll1l1l1llll_opy_)
    except Exception as e:
        logger.debug(bstack1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⣫").format(e))
bstack1ll1l1l1l1l1_opy_()