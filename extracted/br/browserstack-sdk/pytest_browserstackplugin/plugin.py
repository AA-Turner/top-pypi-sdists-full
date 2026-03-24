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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1ll11111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1ll11l1ll1_opy_, update, bstack1l11l11ll1_opy_,
                                       bstack11l1l11lll_opy_, bstack1l1l1111_opy_, bstack1111ll1ll1_opy_, bstack111llll11_opy_,
                                       bstack1l1l1111ll_opy_, bstack1l1l1ll1ll_opy_, bstack1lll1l11l1_opy_,
                                       bstack1111l11ll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11ll11l1l1_opy_)
from browserstack_sdk.bstack11llllll1l_opy_ import bstack1llll1111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1lllll1ll1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1111lll111_opy_, bstack111l1lll_opy_, bstack111ll1l1_opy_, \
    bstack1lll1l1111_opy_
from bstack_utils.helper import bstack111l1lll11_opy_, bstack11111ll1l11_opy_, bstack1llll1ll111_opy_, bstack11llllll_opy_, bstack1l11l1111l_opy_, current_time, \
    bstack1111l11ll1l_opy_, \
    bstack11111l1l1l1_opy_, bstack1l11ll1l1l_opy_, bstack1ll111lll_opy_, bstack11111ll1ll1_opy_, bstack1l11ll1lll_opy_, Notset, \
    bstack11l11l1111_opy_, time_diff, bstack111111ll1l1_opy_, Result, bstack11111lll11l_opy_, bstack11111ll11ll_opy_, error_handler, \
    bstack11l1111l11_opy_, bstack1l111llll1_opy_, bstack11llll111l_opy_, bstack11111l1l111_opy_
from bstack_utils.bstack1lllllll111l_opy_ import bstack1llllll1l111_opy_
from bstack_utils.messages import bstack11lll11lll_opy_, bstack11111lll11_opy_, bstack111ll1ll_opy_, bstack11111llll_opy_, bstack111l1ll1l1_opy_, \
    bstack1lll1111l_opy_, bstack111l1l11l_opy_, CONFIG_FILE_CONTENT, bstack1111l1ll_opy_, bstack1111l111l1_opy_, \
    bstack1l1ll1ll1l_opy_, bstack1111l1ll1l_opy_, bstack1ll111111l_opy_
from bstack_utils.proxy import bstack111ll1ll11_opy_, bstack1l1ll11l_opy_
from bstack_utils.bstack1l11ll111l_opy_ import bstack1lll111l11ll_opy_, bstack1lll111l111l_opy_, bstack1lll1111l111_opy_, bstack1lll1111ll11_opy_, \
    bstack1lll111l1l11_opy_, bstack1lll1111l11l_opy_, bstack1lll1111lll1_opy_, bstack1lll11l1_opy_, bstack1lll1111l1l1_opy_
from bstack_utils.bstack11ll1l1l11_opy_ import bstack1lll11111_opy_
from bstack_utils.session_utils import browserstack_executor_helper, bstack11l11ll11_opy_, update_caps_for_local, \
    bstack1111lll1l1_opy_, bstack11ll11ll11_opy_
from bstack_utils.test_data import TestData
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1lll11llll_opy_ import bstack1l11ll1ll1_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack11ll111lll_opy_ import bstack1llll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l111111ll_opy_ import bstack1l111111ll_opy_, Events, bstack11lll111_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1lll1l11_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l111111ll_opy_ import bstack1l111111ll_opy_, Events, bstack11lll111_opy_
bstack111llll111_opy_ = None
bstack1l1lll1111_opy_ = None
bstack11l1ll1l1_opy_ = None
bstack11l1l1lll1_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1ll1lllll_opy_ = None
bstack1l1l11l11_opy_ = None
bstack11111l1111_opy_ = None
bstack11l1l11111_opy_ = None
bstack111l111l11_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack111l111111_opy_ = None
bstack111ll11lll_opy_ = None
FRAMEWORK_NAME = bstack1ll1lll_opy_ (u"࠭ࠧ⛚")
CONFIG = {}
bstack1ll1ll1l1_opy_ = False
bstack1lllll111_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨ⛛")
bstack11llllll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࠩ⛜")
PARALLELISE_VANILLA_PYTHON = False
bstack1lllllllll_opy_ = []
bstack1l1ll1l111_opy_ = bstack1111lll111_opy_
bstack1ll1l111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⛝")
bstack1l1llllll1_opy_ = {}
SESSION_NAME = None
bstack1llll1ll_opy_ = False
logger = logger_utils.get_logger(__name__, bstack1l1ll1l111_opy_)
store = {
    bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⛞"): []
}
bstack1ll1l11l1l11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1llll111lll_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1lll1l11_opy_(
    test_framework_name=bstack111l111lll_opy_[bstack1ll1lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨ⛟")] if bstack1l11ll1lll_opy_() else bstack111l111lll_opy_[bstack1ll1lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬ⛠")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack1l1ll11ll_opy_):
    try:
        page.evaluate(bstack1ll1lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⛡"),
                      bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ⛢") + json.dumps(
                          bstack1l1ll11ll_opy_) + bstack1ll1lll_opy_ (u"ࠣࡿࢀࠦ⛣"))
    except Exception as e:
        print(bstack1ll1lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ⛤"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1ll1lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ⛥"), bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ⛦") + json.dumps(
            message) + bstack1ll1lll_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ⛧") + json.dumps(level) + bstack1ll1lll_opy_ (u"࠭ࡽࡾࠩ⛨"))
    except Exception as e:
        print(bstack1ll1lll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ⛩"), e)
def pytest_configure(config):
    global bstack1lllll111_opy_
    global CONFIG
    global_config = Config.get_instance()
    config.args = bstack11lll1l11_opy_.bstack1ll1l1l11111_opy_(config.args)
    global_config.bstack11lll1llll_opy_(bstack11llll111l_opy_(config.getoption(bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⛪"))))
    try:
        logger_utils.bstack1lllll1ll11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l111111ll_opy_.invoke(Events.CONNECT, bstack11lll111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⛫"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬ⛬")))
        config = json.loads(os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ⛭"), bstack1ll1lll_opy_ (u"ࠧࢁࡽࠣ⛮")))
        cli.bstack1l1l1llll11_opy_(bstack1ll111lll_opy_(bstack1lllll111_opy_, CONFIG), cli_context.platform_index, bstack1l11l11ll1_opy_)
    if cli.bstack1llll11ll_opy_(bstack1llll1ll1l_opy_):
        cli.bstack1lll1l1ll_opy_()
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⛯") + str(cli_context.platform_index) + bstack1ll1lll_opy_ (u"ࠢࠣ⛰"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1ll1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨ⛱"), None)
    if cli.is_running() and when == bstack1ll1lll_opy_ (u"ࠤࡦࡥࡱࡲࠢ⛲"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1ll1lll_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⛳"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⛴")))
        if not passed:
            config = json.loads(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦ⛵"), bstack1ll1lll_opy_ (u"ࠨࡻࡾࠤ⛶")))
            if bstack1l11ll1ll1_opy_.bstack1llll1lll1_opy_(config):
                bstack1lll1l11lll1_opy_ = bstack1l11ll1ll1_opy_.bstack1ll111l1_opy_(config)
                if item.execution_count > bstack1lll1l11lll1_opy_:
                    print(bstack1ll1lll_opy_ (u"ࠧࡕࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡷ࠿ࠦࠧ⛷"), report.nodeid, os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⛸")))
                    bstack1l11ll1ll1_opy_.bstack1llll1ll11l1_opy_(report.nodeid)
            else:
                print(bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠩ⛹"), report.nodeid, os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⛺")))
                bstack1l11ll1ll1_opy_.bstack1llll1ll11l1_opy_(report.nodeid)
        else:
            print(bstack1ll1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡳࡥࡸࡹࡥࡥ࠼ࠣࠫ⛻"), report.nodeid, os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⛼")))
    if cli.is_running():
        if when == bstack1ll1lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ⛽"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack1ll1lll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ⛾"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1ll1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ⛿"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ✀"))
    plugins = item.config.getoption(bstack1ll1lll_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦ✁"))
    report = outcome.get_result()
    os.environ[bstack1ll1lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ✂")] = report.nodeid
    bstack1ll1l1111l1l_opy_(item, call, report)
    if bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥ✃") not in plugins or bstack1l11ll1lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1lll_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢ✄"), None)
    page = getattr(item, bstack1ll1lll_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨ✅"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1l11l111l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1l1111l11_opy_(item, report, summary, skipSessionName)
def bstack1ll1l11l111l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ✆") and report.skipped:
        bstack1lll1111l1l1_opy_(report)
    if report.when in [bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ✇"), bstack1ll1lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ✈")]:
        return
    if not bstack1l11l1111l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1ll1lll_opy_ (u"ࠫࡹࡸࡵࡦࠩ✉")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ✊") + json.dumps(
                    report.nodeid) + bstack1ll1lll_opy_ (u"࠭ࡽࡾࠩ✋"))
        os.environ[bstack1ll1lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ✌")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣ✍").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1lll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ✎")))
    bstack1111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦ✏")
    bstack1lll1111l1l1_opy_(report)
    if not passed:
        try:
            bstack1111l1lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ✐").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1111l1lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1lll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ✑")))
        bstack1111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠨࠢ✒")
        if not passed:
            try:
                bstack1111l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1lll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ✓").format(e)
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
                    bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ✔")
                    + json.dumps(bstack1ll1lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥ✕"))
                    + bstack1ll1lll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨ✖")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ✗")
                    + json.dumps(str(bstack1111l1lll_opy_))
                    + bstack1ll1lll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ✘")
                )
        except Exception as e:
            summary.append(bstack1ll1lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦ✙").format(e))
def bstack1ll1l111l1l1_opy_(test_name, error_message):
    try:
        bstack1ll1l1111lll_opy_ = []
        bstack111111lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ✚"), bstack1ll1lll_opy_ (u"ࠨ࠲ࠪ✛"))
        bstack111l11l1ll_opy_ = {bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ✜"): test_name, bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ✝"): error_message, bstack1ll1lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ✞"): bstack111111lll1_opy_}
        bstack1ll1l11l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1lll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ✟"))
        if os.path.exists(bstack1ll1l11l11ll_opy_):
            with open(bstack1ll1l11l11ll_opy_) as f:
                bstack1ll1l1111lll_opy_ = json.load(f)
        bstack1ll1l1111lll_opy_.append(bstack111l11l1ll_opy_)
        with open(bstack1ll1l11l11ll_opy_, bstack1ll1lll_opy_ (u"࠭ࡷࠨ✠")) as f:
            json.dump(bstack1ll1l1111lll_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬ✡") + str(e))
def bstack1ll1l1111l11_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ✢"), bstack1ll1lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ✣")]:
        return
    if (str(skipSessionName).lower() != bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ✤")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ✥")))
    bstack1111l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨ✦")
    bstack1lll1111l1l1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1111l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ✧").format(e)
                )
        try:
            if passed:
                bstack11ll11ll11_opy_(getattr(item, bstack1ll1lll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭✨"), None), bstack1ll1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ✩"))
            else:
                error_message = bstack1ll1lll_opy_ (u"ࠩࠪ✪")
                if bstack1111l1lll_opy_:
                    playwright_annotate(item._page, str(bstack1111l1lll_opy_), bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ✫"))
                    bstack11ll11ll11_opy_(getattr(item, bstack1ll1lll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ✬"), None), bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ✭"), str(bstack1111l1lll_opy_))
                    error_message = str(bstack1111l1lll_opy_)
                else:
                    bstack11ll11ll11_opy_(getattr(item, bstack1ll1lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ✮"), None), bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ✯"))
                bstack1ll1l111l1l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧ✰").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1ll1lll_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨ✱"), default=bstack1ll1lll_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ✲"), help=bstack1ll1lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ✳"))
    parser.addoption(bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ✴"), default=bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ✵"), help=bstack1ll1lll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ✶"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1lll_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥ✷"), action=bstack1ll1lll_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣ✸"), default=bstack1ll1lll_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥ✹"),
                         help=bstack1ll1lll_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥ✺"))
def bstack1lllllllll1_opy_(log):
    if not (log[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭✻")] and log[bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ✼")].strip()):
        return
    active = bstack1llllll1l1l_opy_()
    log = {
        bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭✽"): log[bstack1ll1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ✾")],
        bstack1ll1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ✿"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠪ࡞ࠬ❀"),
        bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ❁"): log[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭❂")],
    }
    if active:
        if active[bstack1ll1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ❃")] == bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ❄"):
            log[bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ❅")] = active[bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ❆")]
        elif active[bstack1ll1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ❇")] == bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ❈"):
            log[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ❉")] = active[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭❊")]
    TestHubHandler.bstack11lllll111_opy_([log])
def bstack1llllll1l1l_opy_():
    if len(store[bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ❋")]) > 0 and store[bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ❌")][-1]:
        return {
            bstack1ll1lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ❍"): bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ❎"),
            bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ❏"): store[bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ❐")][-1]
        }
    if store.get(bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ❑"), None):
        return {
            bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ❒"): bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭❓"),
            bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ❔"): store[bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ❕")]
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
        item._1ll1l11lll11_opy_ = True
        bstack111ll1l111_opy_ = a11y.is_enabled_testcase(bstack11111l1l1l1_opy_(item.own_markers))
        if not cli.bstack1llll11ll_opy_(bstack1llll1ll1l_opy_):
            item._a11y_test_case = bstack111ll1l111_opy_
            if bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ❖"), None):
                driver = getattr(item, bstack1ll1lll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭❗"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack111ll1l111_opy_)
        if not TestHubHandler.on() or bstack1ll1l111ll11_opy_ != bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭❘"):
            return
        global current_test_uuid #, bstack1lllll1llll_opy_
        bstack1llll11111l_opy_ = {
            bstack1ll1lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ❙"): uuid4().__str__(),
            bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ❚"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠩ࡝ࠫ❛")
        }
        current_test_uuid = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ❜")]
        store[bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ❝")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ❞")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1llll111lll_opy_[item.nodeid] = {**_1llll111lll_opy_[item.nodeid], **bstack1llll11111l_opy_}
        bstack1ll1l11lllll_opy_(item, _1llll111lll_opy_[item.nodeid], bstack1ll1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ❟"))
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩ❠"), str(err))
def pytest_runtest_setup(item):
    store[bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ❡")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ❢"))
    if bstack1l11ll1ll1_opy_.bstack1llll1ll1111_opy_():
            bstack1ll1l111lll1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡥࡸࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ❣")
            logger.error(bstack1ll1l111lll1_opy_)
            bstack1llll11111l_opy_ = {
                bstack1ll1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ❤"): uuid4().__str__(),
                bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ❥"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"࡚࠭ࠨ❦"),
                bstack1ll1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ❧"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠨ࡜ࠪ❨"),
                bstack1ll1lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ❩"): bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ❪"),
                bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ❫"): bstack1ll1l111lll1_opy_,
                bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ❬"): [],
                bstack1ll1lll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ❭"): []
            }
            bstack1ll1l11lllll_opy_(item, bstack1llll11111l_opy_, bstack1ll1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ❮"))
            pytest.skip(bstack1ll1l111lll1_opy_)
            return # skip all existing operations
    global bstack1ll1l11l1l11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11111ll1ll1_opy_():
        atexit.register(bstack111ll1l11l_opy_)
        if not bstack1ll1l11l1l11_opy_:
            try:
                bstack1ll1l11ll1ll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11111l1l111_opy_():
                    bstack1ll1l11ll1ll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1l11ll1ll_opy_:
                    signal.signal(s, bstack1lll1lll1l1_opy_)
                bstack1ll1l11l1l11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤ❯") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll111l11ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ❰")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1llll11111l_opy_ = {
            bstack1ll1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ❱"): uuid,
            bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ❲"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠬࡠࠧ❳"),
            bstack1ll1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ❴"): bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ❵"),
            bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ❶"): bstack1ll1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ❷"),
            bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭❸"): bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ❹")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ❺")] = item
        store[bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ❻")] = [uuid]
        if not _1llll111lll_opy_.get(item.nodeid, None):
            _1llll111lll_opy_[item.nodeid] = {bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭❼"): [], bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ❽"): []}
        _1llll111lll_opy_[item.nodeid][bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ❾")].append(bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ❿")])
        _1llll111lll_opy_[item.nodeid + bstack1ll1lll_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ➀")] = bstack1llll11111l_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1l11ll111_opy_(item, bstack1llll11111l_opy_, bstack1ll1lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭➁"))
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ➂"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ➃"))
        return # skip all existing operations
    try:
        global bstack1l1llllll1_opy_
        bstack111111lll1_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack111111lll1_opy_ = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ➄")))
        if bstack1l11lll1ll_opy_.bstack1l1l11ll11_opy_() == bstack1ll1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ➅"):
            if bstack1l11lll1ll_opy_.bstack1lll11ll1l_opy_() == bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ➆"):
                bstack1ll1l111l11l_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ➇"), None)
                bstack11ll1lllll_opy_ = bstack1ll1l111l11l_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣ➈")
                driver = getattr(item, bstack1ll1lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ➉"), None)
                bstack11llll11l_opy_ = getattr(item, bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ➊"), None)
                bstack1l111l1111_opy_ = getattr(item, bstack1ll1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭➋"), None)
                PercySDK.screenshot(driver, bstack11ll1lllll_opy_, bstack11llll11l_opy_=bstack11llll11l_opy_, bstack1l111l1111_opy_=bstack1l111l1111_opy_, bstack1l111l11l1_opy_=bstack111111lll1_opy_)
        if not cli.bstack1llll11ll_opy_(bstack1llll1ll1l_opy_):
            if getattr(item, bstack1ll1lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ➌"), False):
                bstack1llll1111_opy_.bstack11l111ll1_opy_(getattr(item, bstack1ll1lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ➍"), None), bstack1l1llllll1_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1llll11111l_opy_ = {
            bstack1ll1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ➎"): uuid4().__str__(),
            bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ➏"): bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"࡚࠭ࠨ➐"),
            bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ➑"): bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭➒"),
            bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ➓"): bstack1ll1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ➔"),
            bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ➕"): bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ➖")
        }
        _1llll111lll_opy_[item.nodeid + bstack1ll1lll_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ➗")] = bstack1llll11111l_opy_
        bstack1ll1l11ll111_opy_(item, bstack1llll11111l_opy_, bstack1ll1lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ➘"))
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ➙"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lll1111ll11_opy_(fixturedef.argname):
        store[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ➚")] = request.node
    elif bstack1lll111l1l11_opy_(fixturedef.argname):
        store[bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ➛")] = request.node
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
            bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ➜"): fixturedef.argname,
            bstack1ll1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ➝"): bstack1111l11ll1l_opy_(outcome),
            bstack1ll1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ➞"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ➟")]
        if not _1llll111lll_opy_.get(current_test_item.nodeid, None):
            _1llll111lll_opy_[current_test_item.nodeid] = {bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ➠"): []}
        _1llll111lll_opy_[current_test_item.nodeid][bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ➡")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭➢"), str(err))
if bstack1l11ll1lll_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1llll111lll_opy_[request.node.nodeid][bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ➣")].bstack1l11ll1111_opy_(id(step))
        except Exception as err:
            print(bstack1ll1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ➤"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1llll111lll_opy_[request.node.nodeid][bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ➥")].bstack1lllll1ll11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ➦"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            test_data: TestData = _1llll111lll_opy_[request.node.nodeid][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ➧")]
            test_data.bstack1lllll1ll11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭➨"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1l111ll11_opy_
        try:
            if not TestHubHandler.on() or bstack1ll1l111ll11_opy_ != bstack1ll1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ➩"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ➪"), None)
            if not _1llll111lll_opy_.get(request.node.nodeid, None):
                _1llll111lll_opy_[request.node.nodeid] = {}
            test_data = TestData.bstack1ll1lll11ll1_opy_(
                scenario, feature, request.node,
                name=bstack1lll1111l11l_opy_(request.node, scenario),
                started_at=current_time(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ➫"),
                tags=bstack1lll1111lll1_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llllllll11_opy_(driver) if driver and driver.session_id else {}
            )
            _1llll111lll_opy_[request.node.nodeid][bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ➬")] = test_data
            bstack1ll1l11l1l1l_opy_(test_data.uuid)
            TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ➭"), test_data)
        except Exception as err:
            print(bstack1ll1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ➮"), str(err))
def bstack1ll1l11lll1l_opy_(bstack1lllll1l1ll_opy_):
    if bstack1lllll1l1ll_opy_ in store[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭➯")]:
        store[bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ➰")].remove(bstack1lllll1l1ll_opy_)
def bstack1ll1l11l1l1l_opy_(test_uuid):
    store[bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ➱")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll1ll11l111_opy_
def bstack1ll1l1111l1l_opy_(item, call, report):
    logger.debug(bstack1ll1lll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ➲"))
    global bstack1ll1l111ll11_opy_
    bstack1l1l1lllll_opy_ = current_time()
    if hasattr(report, bstack1ll1lll_opy_ (u"࠭ࡳࡵࡱࡳࠫ➳")):
        bstack1l1l1lllll_opy_ = bstack11111lll11l_opy_(report.stop)
    elif hasattr(report, bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭➴")):
        bstack1l1l1lllll_opy_ = bstack11111lll11l_opy_(report.start)
    try:
        if getattr(report, bstack1ll1lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭➵"), bstack1ll1lll_opy_ (u"ࠩࠪ➶")) == bstack1ll1lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ➷"):
            logger.debug(bstack1ll1lll_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭➸").format(getattr(report, bstack1ll1lll_opy_ (u"ࠬࡽࡨࡦࡰࠪ➹"), bstack1ll1lll_opy_ (u"࠭ࠧ➺")).__str__(), bstack1ll1l111ll11_opy_))
            if bstack1ll1l111ll11_opy_ == bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ➻"):
                _1llll111lll_opy_[item.nodeid][bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭➼")] = bstack1l1l1lllll_opy_
                bstack1ll1l11lllll_opy_(item, _1llll111lll_opy_[item.nodeid], bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ➽"), report, call)
                store[bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ➾")] = None
            elif bstack1ll1l111ll11_opy_ == bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ➿"):
                test_data = _1llll111lll_opy_[item.nodeid][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⟀")]
                test_data.set(hooks=_1llll111lll_opy_[item.nodeid].get(bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⟁"), []))
                exception, bstack1llllllll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llllllll1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭⟂"), bstack1ll1lll_opy_ (u"ࠨࠩ⟃"))]
                test_data.stop(time=bstack1l1l1lllll_opy_, result=Result(result=getattr(report, bstack1ll1lll_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⟄"), bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⟅")), exception=exception, bstack1llllllll1l_opy_=bstack1llllllll1l_opy_))
                TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⟆"), _1llll111lll_opy_[item.nodeid][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⟇")])
        elif getattr(report, bstack1ll1lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⟈"), bstack1ll1lll_opy_ (u"ࠧࠨ⟉")) in [bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⟊"), bstack1ll1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⟋")]:
            logger.debug(bstack1ll1lll_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⟌").format(getattr(report, bstack1ll1lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⟍"), bstack1ll1lll_opy_ (u"ࠬ࠭⟎")).__str__(), bstack1ll1l111ll11_opy_))
            bstack1llllll111l_opy_ = item.nodeid + bstack1ll1lll_opy_ (u"࠭࠭ࠨ⟏") + getattr(report, bstack1ll1lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⟐"), bstack1ll1lll_opy_ (u"ࠨࠩ⟑"))
            if getattr(report, bstack1ll1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⟒"), False):
                hook_type = bstack1ll1lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⟓") if getattr(report, bstack1ll1lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⟔"), bstack1ll1lll_opy_ (u"ࠬ࠭⟕")) == bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⟖") else bstack1ll1lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⟗")
                _1llll111lll_opy_[bstack1llllll111l_opy_] = {
                    bstack1ll1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⟘"): uuid4().__str__(),
                    bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⟙"): bstack1l1l1lllll_opy_,
                    bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⟚"): hook_type
                }
            _1llll111lll_opy_[bstack1llllll111l_opy_][bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⟛")] = bstack1l1l1lllll_opy_
            bstack1ll1l11lll1l_opy_(_1llll111lll_opy_[bstack1llllll111l_opy_][bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⟜")])
            bstack1ll1l11ll111_opy_(item, _1llll111lll_opy_[bstack1llllll111l_opy_], bstack1ll1lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⟝"), report, call)
            if getattr(report, bstack1ll1lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⟞"), bstack1ll1lll_opy_ (u"ࠨࠩ⟟")) == bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⟠"):
                if getattr(report, bstack1ll1lll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⟡"), bstack1ll1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⟢")) == bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⟣"):
                    bstack1llll11111l_opy_ = {
                        bstack1ll1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⟤"): uuid4().__str__(),
                        bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⟥"): current_time(),
                        bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⟦"): current_time()
                    }
                    _1llll111lll_opy_[item.nodeid] = {**_1llll111lll_opy_[item.nodeid], **bstack1llll11111l_opy_}
                    bstack1ll1l11lllll_opy_(item, _1llll111lll_opy_[item.nodeid], bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⟧"))
                    bstack1ll1l11lllll_opy_(item, _1llll111lll_opy_[item.nodeid], bstack1ll1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⟨"), report, call)
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ⟩"), str(err))
def bstack1ll1l11llll1_opy_(test, bstack1llll11111l_opy_, result=None, call=None, bstack111111ll11_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    test_data = {
        bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⟪"): bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⟫")],
        bstack1ll1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⟬"): bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭⟭"),
        bstack1ll1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⟮"): test.name,
        bstack1ll1lll_opy_ (u"ࠪࡦࡴࡪࡹࠨ⟯"): {
            bstack1ll1lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⟰"): bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⟱"),
            bstack1ll1lll_opy_ (u"࠭ࡣࡰࡦࡨࠫ⟲"): inspect.getsource(test.obj)
        },
        bstack1ll1lll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⟳"): test.name,
        bstack1ll1lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⟴"): test.name,
        bstack1ll1lll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⟵"): bstack11lll1l11_opy_.bstack1llll1l1111_opy_(test),
        bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⟶"): file_path,
        bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⟷"): file_path,
        bstack1ll1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⟸"): bstack1ll1lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⟹"),
        bstack1ll1lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⟺"): file_path,
        bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⟻"): bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⟼")],
        bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⟽"): bstack1ll1lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⟾"),
        bstack1ll1lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⟿"): {
            bstack1ll1lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ⠀"): test.nodeid
        },
        bstack1ll1lll_opy_ (u"ࠧࡵࡣࡪࡷࠬ⠁"): bstack11111l1l1l1_opy_(test.own_markers)
    }
    if bstack111111ll11_opy_ in [bstack1ll1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⠂"), bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⠃")]:
        test_data[bstack1ll1lll_opy_ (u"ࠪࡱࡪࡺࡡࠨ⠄")] = {
            bstack1ll1lll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⠅"): bstack1llll11111l_opy_.get(bstack1ll1lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⠆"), [])
        }
    if bstack111111ll11_opy_ == bstack1ll1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⠇"):
        test_data[bstack1ll1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⠈")] = bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⠉")
        test_data[bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⠊")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⠋")]
        test_data[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⠌")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⠍")]
    if result:
        test_data[bstack1ll1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⠎")] = result.outcome
        test_data[bstack1ll1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⠏")] = result.duration * 1000
        test_data[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⠐")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⠑")]
        if result.failed:
            test_data[bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⠒")] = TestHubHandler.bstack1ll1llll1ll_opy_(call.excinfo.typename)
            test_data[bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⠓")] = TestHubHandler.bstack1ll1l1lll1ll_opy_(call.excinfo, result)
        test_data[bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⠔")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⠕")]
    if outcome:
        test_data[bstack1ll1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⠖")] = bstack1111l11ll1l_opy_(outcome)
        test_data[bstack1ll1lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⠗")] = 0
        test_data[bstack1ll1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⠘")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⠙")]
        if test_data[bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⠚")] == bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⠛"):
            test_data[bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⠜")] = bstack1ll1lll_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⠝")  # bstack1ll1l11111ll_opy_
            test_data[bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⠞")] = [{bstack1ll1lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⠟"): [bstack1ll1lll_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⠠")]}]
        test_data[bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⠡")] = bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⠢")]
    return test_data
def bstack1ll1l11ll1l1_opy_(test, bstack1lllll11l1l_opy_, bstack111111ll11_opy_, result, call, outcome, bstack1ll1l1111ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⠣")]
    hook_name = bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⠤")]
    hook_data = {
        bstack1ll1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⠥"): bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⠦")],
        bstack1ll1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⠧"): bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⠨"),
        bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⠩"): bstack1ll1lll_opy_ (u"࠭ࡻࡾࠩ⠪").format(bstack1lll111l111l_opy_(hook_name)),
        bstack1ll1lll_opy_ (u"ࠧࡣࡱࡧࡽࠬ⠫"): {
            bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⠬"): bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⠭"),
            bstack1ll1lll_opy_ (u"ࠪࡧࡴࡪࡥࠨ⠮"): None
        },
        bstack1ll1lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⠯"): test.name,
        bstack1ll1lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⠰"): bstack11lll1l11_opy_.bstack1llll1l1111_opy_(test, hook_name),
        bstack1ll1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⠱"): file_path,
        bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⠲"): file_path,
        bstack1ll1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⠳"): bstack1ll1lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⠴"),
        bstack1ll1lll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⠵"): file_path,
        bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⠶"): bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⠷")],
        bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⠸"): bstack1ll1lll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ⠹") if bstack1ll1l111ll11_opy_ == bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⠺") else bstack1ll1lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⠻"),
        bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⠼"): hook_type
    }
    bstack1l11ll11ll1_opy_ = bstack1lllll111ll_opy_(_1llll111lll_opy_.get(test.nodeid, None))
    if bstack1l11ll11ll1_opy_:
        hook_data[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⠽")] = bstack1l11ll11ll1_opy_
    if result:
        hook_data[bstack1ll1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⠾")] = result.outcome
        hook_data[bstack1ll1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⠿")] = result.duration * 1000
        hook_data[bstack1ll1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⡀")] = bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⡁")]
        if result.failed:
            hook_data[bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⡂")] = TestHubHandler.bstack1ll1llll1ll_opy_(call.excinfo.typename)
            hook_data[bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⡃")] = TestHubHandler.bstack1ll1l1lll1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⡄")] = bstack1111l11ll1l_opy_(outcome)
        hook_data[bstack1ll1lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⡅")] = 100
        hook_data[bstack1ll1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⡆")] = bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⡇")]
        if hook_data[bstack1ll1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⡈")] == bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⡉"):
            hook_data[bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⡊")] = bstack1ll1lll_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ⡋")  # bstack1ll1l11111ll_opy_
            hook_data[bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⡌")] = [{bstack1ll1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⡍"): [bstack1ll1lll_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ⡎")]}]
    if bstack1ll1l1111ll1_opy_:
        hook_data[bstack1ll1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⡏")] = bstack1ll1l1111ll1_opy_.result
        hook_data[bstack1ll1lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⡐")] = time_diff(bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⡑")], bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⡒")])
        hook_data[bstack1ll1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⡓")] = bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⡔")]
        if hook_data[bstack1ll1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⡕")] == bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⡖"):
            hook_data[bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⡗")] = TestHubHandler.bstack1ll1llll1ll_opy_(bstack1ll1l1111ll1_opy_.exception_type)
            hook_data[bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⡘")] = [{bstack1ll1lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⡙"): bstack111111ll1l1_opy_(bstack1ll1l1111ll1_opy_.exception)}]
    return hook_data
def bstack1ll1l11lllll_opy_(test, bstack1llll11111l_opy_, bstack111111ll11_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1ll1lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⡚").format(bstack111111ll11_opy_))
    test_data = bstack1ll1l11llll1_opy_(test, bstack1llll11111l_opy_, result, call, bstack111111ll11_opy_, outcome)
    driver = getattr(test, bstack1ll1lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⡛"), None)
    if bstack111111ll11_opy_ == bstack1ll1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⡜") and driver:
        test_data[bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ⡝")] = TestHubHandler.bstack1llllllll11_opy_(driver)
    if bstack111111ll11_opy_ == bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⡞"):
        bstack111111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⡟")
    bstack1lllll11ll1_opy_ = {
        bstack1ll1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⡠"): bstack111111ll11_opy_,
        bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⡡"): test_data
    }
    TestHubHandler.bstack11l1ll111l_opy_(bstack1lllll11ll1_opy_)
    if bstack111111ll11_opy_ == bstack1ll1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⡢"):
        threading.current_thread().bstackTestMeta = {bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⡣"): bstack1ll1lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⡤")}
    elif bstack111111ll11_opy_ == bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⡥"):
        threading.current_thread().bstackTestMeta = {bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⡦"): getattr(result, bstack1ll1lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⡧"), bstack1ll1lll_opy_ (u"ࠬ࠭⡨"))}
def bstack1ll1l11ll111_opy_(test, bstack1llll11111l_opy_, bstack111111ll11_opy_, result=None, call=None, outcome=None, bstack1ll1l1111ll1_opy_=None):
    logger.debug(bstack1ll1lll_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⡩").format(bstack111111ll11_opy_))
    hook_data = bstack1ll1l11ll1l1_opy_(test, bstack1llll11111l_opy_, bstack111111ll11_opy_, result, call, outcome, bstack1ll1l1111ll1_opy_)
    bstack1lllll11ll1_opy_ = {
        bstack1ll1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⡪"): bstack111111ll11_opy_,
        bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ⡫"): hook_data
    }
    TestHubHandler.bstack11l1ll111l_opy_(bstack1lllll11ll1_opy_)
def bstack1lllll111ll_opy_(bstack1llll11111l_opy_):
    if not bstack1llll11111l_opy_:
        return None
    if bstack1llll11111l_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⡬"), None):
        return getattr(bstack1llll11111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⡭")], bstack1ll1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⡮"), None)
    return bstack1llll11111l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⡯"), None)
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
        places = [bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⡰"), bstack1ll1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⡱"), bstack1ll1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⡲")]
        logs = []
        for bstack1ll1l111l1ll_opy_ in places:
            records = caplog.get_records(bstack1ll1l111l1ll_opy_)
            bstack1ll1l11ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⡳") if bstack1ll1l111l1ll_opy_ == bstack1ll1lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⡴") else bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⡵")
            bstack1ll1l111l111_opy_ = request.node.nodeid + (bstack1ll1lll_opy_ (u"ࠬ࠭⡶") if bstack1ll1l111l1ll_opy_ == bstack1ll1lll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⡷") else bstack1ll1lll_opy_ (u"ࠧ࠮ࠩ⡸") + bstack1ll1l111l1ll_opy_)
            test_uuid = bstack1lllll111ll_opy_(_1llll111lll_opy_.get(bstack1ll1l111l111_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11111ll11ll_opy_(record.message):
                    continue
                logs.append({
                    bstack1ll1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⡹"): bstack11111ll1l11_opy_(record.created).isoformat() + bstack1ll1lll_opy_ (u"ࠩ࡝ࠫ⡺"),
                    bstack1ll1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⡻"): record.levelname,
                    bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⡼"): record.message,
                    bstack1ll1l11ll11l_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack11lllll111_opy_(logs)
    except Exception as err:
        print(bstack1ll1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ⡽"), str(err))
def bstack1l11l11l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1llll1ll_opy_
    bstack1llllll1l1_opy_ = bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ⡾"), None) and bstack111l1lll11_opy_(
            threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⡿"), None)
    bstack1l1l1lll11_opy_ = getattr(driver, bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⢀"), None) != None and getattr(driver, bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⢁"), None) == True
    if sequence == bstack1ll1lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⢂") and driver != None:
      if not bstack1llll1ll_opy_ and bstack1l11l1111l_opy_() and bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⢃") in CONFIG and CONFIG[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⢄")] == True and accessibility_scripts.bstack1111lll1_opy_(driver_command) and (bstack1l1l1lll11_opy_ or bstack1llllll1l1_opy_) and not bstack11ll11l1l1_opy_(args):
        try:
          bstack1llll1ll_opy_ = True
          logger.debug(bstack1ll1lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ⢅").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ⢆").format(str(err)))
        bstack1llll1ll_opy_ = False
    if sequence == bstack1ll1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⢇"):
        if driver_command == bstack1ll1lll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭⢈"):
            TestHubHandler.bstack11lll1l11l_opy_({
                bstack1ll1lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ⢉"): response[bstack1ll1lll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ⢊")],
                bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⢋"): store[bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⢌")]
            })
def bstack111ll1l11l_opy_():
    global bstack1lllllllll_opy_
    logger_utils.bstack1llll111_opy_()
    logging.shutdown()
    TestHubHandler.bstack1llll1l1l11_opy_()
    for driver in bstack1lllllllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1lll1l1_opy_(*args):
    global bstack1lllllllll_opy_
    TestHubHandler.bstack1llll1l1l11_opy_()
    for driver in bstack1lllllllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1l1ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l1l111lll_opy_(self, *args, **kwargs):
    bstack11lllll1l1_opy_ = bstack111llll111_opy_(self, *args, **kwargs)
    bstack1111l1ll1_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⢍"), None)
    if bstack1111l1ll1_opy_ and bstack1111l1ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⢎"), bstack1ll1lll_opy_ (u"ࠩࠪ⢏")) == bstack1ll1lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⢐"):
        TestHubHandler.send_cbt_info(self)
    return bstack11lllll1l1_opy_
@measure(event_name=EVENTS.bstack111lll1l11_opy_, stage=STAGE.bstack11l11l1l1_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1111l1l1l_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.get_instance()
    if global_config.get_property(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⢑")):
        return
    global_config.bstack11lll11l11_opy_(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⢒"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack1111l1ll1l_opy_.format(FRAMEWORK_NAME.split(bstack1ll1lll_opy_ (u"࠭࠭ࠨ⢓"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l11l1111l_opy_():
            Service.start = bstack1111ll1ll1_opy_
            Service.stop = bstack111llll11_opy_
            webdriver.Remote.get = bstack1ll11llll1_opy_
            webdriver.Remote.__init__ = bstack1l11ll11_opy_
            if not isinstance(os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ⢔")), str):
                return
            WebDriver.quit = bstack1ll111l1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1l1l111lll_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭⢕")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⢖")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack1l1l1ll1ll_opy_(bstack1ll1lll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ⢗"), bstack1l1ll1ll1l_opy_)
    if bstack1l1ll1lll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⢘")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⢙"))):
                RemoteConnection._get_proxy_url = bstack111llllll1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack111llllll1_opy_
        except Exception as e:
            logger.error(bstack1lll1111l_opy_.format(str(e)))
    if bstack1ll1lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⢚") in str(framework_name).lower():
        if not bstack1l11l1111l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l1l11lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1111_opy_
            Config.getoption = bstack11ll11l11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11ll1ll11_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll1ll111_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1ll111l1l_opy_(self):
    global FRAMEWORK_NAME
    global bstack1llll1ll1_opy_
    global bstack1l1lll1111_opy_
    try:
        if bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⢛") in FRAMEWORK_NAME and self.session_id != None and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ⢜"), bstack1ll1lll_opy_ (u"ࠩࠪ⢝")) != bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⢞"):
            bstack1l1llll11l_opy_ = bstack1ll1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⢟") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⢠")
            bstack1l111llll1_opy_(logger, True)
            if os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⢡"), None):
                self.execute_script(
                    bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ⢢") + json.dumps(
                        os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⢣"))) + bstack1ll1lll_opy_ (u"ࠩࢀࢁࠬ⢤"))
            if self != None:
                bstack1111lll1l1_opy_(self, bstack1l1llll11l_opy_, bstack1ll1lll_opy_ (u"ࠪ࠰ࠥ࠭⢥").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll11ll_opy_(bstack1llll1ll1l_opy_):
            item = store.get(bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⢦"), None)
            if item is not None and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⢧"), None):
                bstack1llll1111_opy_.bstack11l111ll1_opy_(self, bstack1l1llllll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1lll_opy_ (u"࠭ࠧ⢨")
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ⢩") + str(e))
    bstack1l1lll1111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l1111l_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1l11ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1ll1_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack111llll111_opy_
    global bstack1lllllllll_opy_
    global bstack1lllll111_opy_
    global bstack11llllll1_opy_
    global bstack1l1llllll1_opy_
    CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⢪")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack1ll111lll_opy_(bstack1lllll111_opy_, CONFIG)
    logger.debug(bstack11111llll_opy_.format(command_executor))
    proxy = bstack1111l11ll1_opy_(CONFIG, proxy)
    bstack111111lll1_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack111111lll1_opy_ = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⢫")))
    except:
        bstack111111lll1_opy_ = 0
    bstack1111lll1ll_opy_ = get_caps(CONFIG, bstack111111lll1_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1111lll1ll_opy_)))
    bstack1l1llllll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⢬"))[bstack111111lll1_opy_]
    if bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⢭") in CONFIG and CONFIG[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⢮")]:
        update_caps_for_local(bstack1111lll1ll_opy_, bstack11llllll1_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack111111lll1_opy_) and a11y.is_platform_supported(bstack1111lll1ll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll11ll_opy_(bstack1llll1ll1l_opy_):
            a11y.set_capabilities(bstack1111lll1ll_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll1lll1ll_opy_ = bstack1ll11l1ll1_opy_(desired_capabilities)
        bstack1ll1lll1ll_opy_[bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⢯")] = bstack11l11l1111_opy_(CONFIG)
        bstack1l1llll11_opy_ = get_caps(bstack1ll1lll1ll_opy_)
        if bstack1l1llll11_opy_:
            bstack1111lll1ll_opy_ = update(bstack1l1llll11_opy_, bstack1111lll1ll_opy_)
        desired_capabilities = None
    if options:
        bstack1l1l1111ll_opy_(options, bstack1111lll1ll_opy_)
    if not options:
        options = bstack1l11l11ll1_opy_(bstack1111lll1ll_opy_)
    if proxy and bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⢰")):
        options.proxy(proxy)
    if options and bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⢱")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l11ll1l1l_opy_() < version.parse(bstack1ll1lll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⢲")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1111lll1ll_opy_)
    logger.info(bstack111ll1ll_opy_)
    bstack1ll11111_opy_.end(EVENTS.bstack111lll1l11_opy_.value, EVENTS.bstack111lll1l11_opy_.value + bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⢳"),
                               EVENTS.bstack111lll1l11_opy_.value + bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⢴"), True, None)
    try:
        if bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ⢵")):
            bstack111llll111_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⢶")):
            bstack111llll111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ⢷")):
            bstack111llll111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack111llll111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1ll1llll1l_opy_:
        logger.error(bstack1ll111111l_opy_.format(bstack1ll1lll_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧ⢸"), str(bstack1ll1llll1l_opy_)))
        raise bstack1ll1llll1l_opy_
    try:
        bstack111l111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠩࠪ⢹")
        if bstack1l11ll1l1l_opy_() >= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ⢺")):
            bstack111l111l1l_opy_ = self.caps.get(bstack1ll1lll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⢻"))
        else:
            bstack111l111l1l_opy_ = self.capabilities.get(bstack1ll1lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⢼"))
        if bstack111l111l1l_opy_:
            bstack11l1111l11_opy_(bstack111l111l1l_opy_)
            if bstack1l11ll1l1l_opy_() <= version.parse(bstack1ll1lll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭⢽")):
                self.command_executor._url = bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⢾") + bstack1lllll111_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ⢿")
            else:
                self.command_executor._url = bstack1ll1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ⣀") + bstack111l111l1l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ⣁")
            logger.debug(bstack11111lll11_opy_.format(bstack111l111l1l_opy_))
        else:
            logger.debug(bstack11lll11lll_opy_.format(bstack1ll1lll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ⣂")))
    except Exception as e:
        logger.debug(bstack11lll11lll_opy_.format(e))
    bstack1llll1ll1_opy_ = self.session_id
    if bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⣃") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⣄"), None)
        if item:
            bstack1ll1l11l1111_opy_ = getattr(item, bstack1ll1lll_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ⣅"), False)
            if not getattr(item, bstack1ll1lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⣆"), None) and bstack1ll1l11l1111_opy_:
                setattr(store[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⣇")], bstack1ll1lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⣈"), self)
        bstack1111l1ll1_opy_ = getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ⣉"), None)
        if bstack1111l1ll1_opy_ and bstack1111l1ll1_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⣊"), bstack1ll1lll_opy_ (u"࠭ࠧ⣋")) == bstack1ll1lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⣌"):
            TestHubHandler.send_cbt_info(self)
    bstack1lllllllll_opy_.append(self)
    if bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⣍") in CONFIG and bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⣎") in CONFIG[bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⣏")][bstack111111lll1_opy_]:
        SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⣐")][bstack111111lll1_opy_][bstack1ll1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⣑")]
    logger.debug(bstack1111l111l1_opy_.format(bstack1llll1ll1_opy_))
@measure(event_name=EVENTS.bstack111ll1l11_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack1ll1l11l1l_opy_=SESSION_NAME)
def bstack1ll11llll1_opy_(self, url):
    global bstack11l1l11111_opy_
    global CONFIG
    try:
        bstack11l11ll11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1111l1ll_opy_.format(str(err)))
    try:
        bstack11l1l11111_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack111ll1l1_opy_):
                bstack11l11ll11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1111l1ll_opy_.format(str(err)))
        raise e
def bstack11ll111l1l_opy_(item, when):
    global bstack111l111111_opy_
    try:
        bstack111l111111_opy_(item, when)
    except Exception as e:
        pass
def bstack11ll1ll11_opy_(item, call, rep):
    global bstack111ll11lll_opy_
    global bstack1lllllllll_opy_
    name = bstack1ll1lll_opy_ (u"࠭ࠧ⣒")
    try:
        if rep.when == bstack1ll1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⣓"):
            bstack1llll1ll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1ll1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⣔"))
            try:
                if (str(skipSessionName).lower() != bstack1ll1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⣕")):
                    name = str(rep.nodeid)
                    executor_string = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⣖"), name, bstack1ll1lll_opy_ (u"ࠫࠬ⣗"), bstack1ll1lll_opy_ (u"ࠬ࠭⣘"), bstack1ll1lll_opy_ (u"࠭ࠧ⣙"), bstack1ll1lll_opy_ (u"ࠧࠨ⣚"))
                    os.environ[bstack1ll1lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⣛")] = name
                    for driver in bstack1lllllllll_opy_:
                        if bstack1llll1ll1_opy_ == driver.session_id:
                            driver.execute_script(executor_string)
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⣜").format(str(e)))
            try:
                bstack1lll11l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⣝"):
                    status = bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⣞") if rep.outcome.lower() == bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⣟") else bstack1ll1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⣠")
                    reason = bstack1ll1lll_opy_ (u"ࠧࠨ⣡")
                    if status == bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⣢"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1lll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ⣣") if status == bstack1ll1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⣤") else bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⣥")
                    data = name + bstack1ll1lll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ⣦") if status == bstack1ll1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⣧") else name + bstack1ll1lll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ⣨") + reason
                    bstack1l1ll1llll_opy_ = browserstack_executor_helper(bstack1ll1lll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⣩"), bstack1ll1lll_opy_ (u"ࠩࠪ⣪"), bstack1ll1lll_opy_ (u"ࠪࠫ⣫"), bstack1ll1lll_opy_ (u"ࠫࠬ⣬"), level, data)
                    for driver in bstack1lllllllll_opy_:
                        if bstack1llll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll1llll_opy_)
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⣭").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ⣮").format(str(e)))
    bstack111ll11lll_opy_(item, call, rep)
notset = Notset()
def bstack11ll11l11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll1ll1l_opy_
    if str(name).lower() == bstack1ll1lll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ⣯"):
        return bstack1ll1lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ⣰")
    else:
        return bstack1ll1ll1l_opy_(self, name, default, skip)
def bstack111llllll1_opy_(self):
    global CONFIG
    global bstack1l1l11l11_opy_
    try:
        proxy = bstack111ll1ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1lll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⣱")):
                proxies = bstack1l1ll11l_opy_(proxy, bstack1ll111lll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll11ll11_opy_ = proxies.popitem()
                    if bstack1ll1lll_opy_ (u"ࠥ࠾࠴࠵ࠢ⣲") in bstack1lll11ll11_opy_:
                        return bstack1lll11ll11_opy_
                    else:
                        return bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⣳") + bstack1lll11ll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ⣴").format(str(e)))
    return bstack1l1l11l11_opy_(self)
def bstack1l1ll1lll_opy_():
    return (bstack1ll1lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⣵") in CONFIG or bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⣶") in CONFIG) and bstack11llllll_opy_() and bstack1l11ll1l1l_opy_() >= version.parse(
        bstack111l1lll_opy_)
def bstack1ll1111l1_opy_(self,
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
    CONFIG[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⣷")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack111111lll1_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack111111lll1_opy_ = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⣸")))
    except:
        bstack111111lll1_opy_ = 0
    CONFIG[bstack1ll1lll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ⣹")] = True
    bstack1111lll1ll_opy_ = get_caps(CONFIG, bstack111111lll1_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1111lll1ll_opy_)))
    if CONFIG.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⣺")):
        update_caps_for_local(bstack1111lll1ll_opy_, bstack11llllll1_opy_)
    if bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⣻") in CONFIG and bstack1ll1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⣼") in CONFIG[bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⣽")][bstack111111lll1_opy_]:
        SESSION_NAME = CONFIG[bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⣾")][bstack111111lll1_opy_][bstack1ll1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⣿")]
    import urllib
    import json
    if bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⤀") in CONFIG and str(CONFIG[bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⤁")]).lower() != bstack1ll1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⤂"):
        bstack1ll1ll1l11_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1ll1ll1l11_opy_ + urllib.parse.quote(json.dumps(bstack1111lll1ll_opy_))
    else:
        cdpUrl = bstack1ll1lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ⤃") + urllib.parse.quote(json.dumps(bstack1111lll1ll_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l1lll1l1_opy_
        if not bstack1l11l1111l_opy_():
            global bstack11lll1ll1l_opy_
            if not bstack11lll1ll1l_opy_:
                from bstack_utils.helper import bstack11l1lll1ll_opy_, bstack1111l1ll111_opy_
                bstack11lll1ll1l_opy_ = bstack11l1lll1ll_opy_()
                bstack1111l1ll111_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l1l1lll1l1_opy_
            return
        BrowserType.launch = bstack1ll1111l1_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll1l11l1ll1_opy_():
    global CONFIG
    global bstack1ll1ll1l1_opy_
    global bstack1lllll111_opy_
    global bstack11llllll1_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack1l1ll1l111_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭⤄")))
    bstack1ll1ll1l1_opy_ = eval(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ⤅")))
    bstack1lllll111_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ⤆"))
    bstack1lll1l11l1_opy_(CONFIG, bstack1ll1ll1l1_opy_)
    bstack1l1ll1l111_opy_ = logger_utils.configure_logger(CONFIG, bstack1l1ll1l111_opy_)
    if cli.bstack111llllll_opy_():
        bstack1l111111ll_opy_.invoke(Events.CONNECT, bstack11lll111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⤇"), bstack1ll1lll_opy_ (u"ࠫ࠵࠭⤈")))
        cli.bstack1l1lll1ll1_opy_(cli_context.platform_index)
        cli.bstack1l1l1llll11_opy_(bstack1ll111lll_opy_(bstack1lllll111_opy_, CONFIG), cli_context.platform_index, bstack1l11l11ll1_opy_)
        cli.bstack1lll1l1ll_opy_()
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⤉") + str(cli_context.platform_index) + bstack1ll1lll_opy_ (u"ࠨࠢ⤊"))
        return # skip all existing operations
    global bstack111llll111_opy_
    global bstack1l1lll1111_opy_
    global bstack11l1ll1l1_opy_
    global bstack11l1l1lll1_opy_
    global bstack1l1ll111l1_opy_
    global bstack1ll1lllll_opy_
    global bstack11111l1111_opy_
    global bstack11l1l11111_opy_
    global bstack1l1l11l11_opy_
    global bstack1ll1ll1l_opy_
    global bstack111l111111_opy_
    global bstack111ll11lll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111llll111_opy_ = webdriver.Remote.__init__
        bstack1l1lll1111_opy_ = WebDriver.quit
        bstack11111l1111_opy_ = WebDriver.close
        bstack11l1l11111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⤋") in CONFIG or bstack1ll1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⤌") in CONFIG) and bstack11llllll_opy_():
        if bstack1l11ll1l1l_opy_() < version.parse(bstack111l1lll_opy_):
            logger.error(bstack111l1l11l_opy_.format(bstack1l11ll1l1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⤍")) and callable(getattr(RemoteConnection, bstack1ll1lll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⤎"))):
                    bstack1l1l11l11_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1l11l11_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1lll1111l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll1ll1l_opy_ = Config.getoption
        from _pytest import runner
        bstack111l111111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1ll1lll_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦ⤏"), bstack111l1ll1l1_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack111ll11lll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭⤐"))
    bstack11llllll1_opy_ = CONFIG.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ⤑"), {}).get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⤒"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack1111l1l1l_opy_(bstack1lll1l1111_opy_)
if (bstack11111ll1ll1_opy_()):
    bstack1ll1l11l1ll1_opy_()
@error_handler(class_method=False)
def bstack1ll1l11l11l1_opy_(hook_name, event, bstack11l1l1l11l1_opy_=None):
    if hook_name not in [bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⤓"), bstack1ll1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⤔"), bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⤕"), bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⤖"), bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⤗"), bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⤘"), bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⤙"), bstack1ll1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ⤚")]:
        return
    node = store[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⤛")]
    if hook_name in [bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⤜"), bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⤝")]:
        node = store[bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ⤞")]
    elif hook_name in [bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⤟"), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⤠")]:
        node = store[bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭⤡")]
    hook_type = bstack1lll1111l111_opy_(hook_name)
    if event == bstack1ll1lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⤢"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lllll11l1l_opy_ = {
            bstack1ll1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⤣"): uuid,
            bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⤤"): current_time(),
            bstack1ll1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⤥"): bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⤦"),
            bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⤧"): hook_type,
            bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⤨"): hook_name
        }
        store[bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⤩")].append(uuid)
        bstack1ll1l111llll_opy_ = node.nodeid
        if hook_type == bstack1ll1lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⤪"):
            if not _1llll111lll_opy_.get(bstack1ll1l111llll_opy_, None):
                _1llll111lll_opy_[bstack1ll1l111llll_opy_] = {bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⤫"): []}
            _1llll111lll_opy_[bstack1ll1l111llll_opy_][bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⤬")].append(bstack1lllll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⤭")])
        _1llll111lll_opy_[bstack1ll1l111llll_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠮ࠩ⤮") + hook_name] = bstack1lllll11l1l_opy_
        bstack1ll1l11ll111_opy_(node, bstack1lllll11l1l_opy_, bstack1ll1lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⤯"))
    elif event == bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⤰"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l1l1l11l1_opy_)
            return
        bstack1llllll111l_opy_ = node.nodeid + bstack1ll1lll_opy_ (u"ࠪ࠱ࠬ⤱") + hook_name
        _1llll111lll_opy_[bstack1llllll111l_opy_][bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⤲")] = current_time()
        bstack1ll1l11lll1l_opy_(_1llll111lll_opy_[bstack1llllll111l_opy_][bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⤳")])
        bstack1ll1l11ll111_opy_(node, _1llll111lll_opy_[bstack1llllll111l_opy_], bstack1ll1lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⤴"), bstack1ll1l1111ll1_opy_=bstack11l1l1l11l1_opy_)
def bstack1ll1l111ll1l_opy_():
    global bstack1ll1l111ll11_opy_
    if bstack1l11ll1lll_opy_():
        bstack1ll1l111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⤵")
    else:
        bstack1ll1l111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⤶")
@TestHubHandler.bstack1ll1ll11l111_opy_
def bstack1ll1l11l1lll_opy_():
    bstack1ll1l111ll1l_opy_()
    if cli.is_running():
        try:
            bstack1llllll1l111_opy_(bstack1ll1l11l11l1_opy_)
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⤷").format(e))
        return
    if bstack11llllll_opy_():
        global_config = Config.get_instance()
        bstack1ll1lll_opy_ (u"ࠪࠫࠬࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡃࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡩࡨࡸࡸࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠮ࡹࡵࡥࡵࡶࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡳࡷࡱࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡯࡮ࠡࡣࠣࡨ࡮࡬ࡦࡦࡴࡨࡲࡹࠦࡰࡳࡱࡦࡩࡸࡹࠠࡪࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡹࡸࠦࡷࡦࠢࡱࡩࡪࡪࠠࡵࡱࠣࡹࡸ࡫ࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡒࡤࡸࡨ࡮ࠨࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠬࠤ࡫ࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠫࠬ࠭⤸")
        if global_config.get_property(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⤹")):
            if CONFIG.get(bstack1ll1lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⤺")) is not None and int(CONFIG[bstack1ll1lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⤻")]) > 1:
                bstack1lll11111_opy_(bstack1l11l11l_opy_)
            return
        bstack1lll11111_opy_(bstack1l11l11l_opy_)
    try:
        bstack1llllll1l111_opy_(bstack1ll1l11l11l1_opy_)
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⤼").format(e))
bstack1ll1l11l1lll_opy_()