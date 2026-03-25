# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l1l1ll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1111111ll_opy_, update, bstack1ll111lll1_opy_,
                                       bstack1ll11llll_opy_, bstack1l11ll111_opy_, bstack11111lll1l_opy_, bstack1111l1111l_opy_,
                                       bstack1l111111l1_opy_, bstack11111lll1_opy_, bstack11111lll_opy_,
                                       bstack11llll111l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack111l1ll1ll_opy_)
from browserstack_sdk.bstack11l111ll11_opy_ import bstack111l1lll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1lllllllll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1l1l1ll1_opy_, bstack11l1l1ll11_opy_, bstack11lll1l111_opy_, \
    bstack1111ll1l_opy_
from bstack_utils.helper import bstack1l1lll111l_opy_, bstack1lllllll1lll_opy_, bstack1lllll11ll1_opy_, bstack11l111ll_opy_, bstack1ll11111l1_opy_, current_time, \
    bstack1111111ll1l_opy_, \
    bstack1111l1l111l_opy_, bstack1lllllll1l_opy_, bstack11lll11l1_opy_, bstack11111ll1ll1_opy_, bstack1111111ll1_opy_, Notset, \
    bstack1lll1ll1ll_opy_, time_diff, bstack111111l1l1l_opy_, Result, bstack1llllllll111_opy_, bstack1111111lll1_opy_, error_handler, \
    bstack111lll1ll_opy_, bstack11lll1ll11_opy_, bstack1l11llll_opy_, bstack1111111ll11_opy_
from bstack_utils.bstack1lllllll1111_opy_ import bstack1lllllll11l1_opy_
from bstack_utils.messages import bstack1l1lll11l_opy_, bstack111ll11l_opy_, bstack111ll11lll_opy_, bstack1l1ll1l1ll_opy_, bstack11llllll1l_opy_, \
    bstack11l1llllll_opy_, bstack1l11111111_opy_, CONFIG_FILE_CONTENT, bstack1llll1ll1_opy_, bstack1ll11l11l1_opy_, \
    bstack11ll1l11_opy_, bstack1l1111l1ll_opy_, bstack1llll11111_opy_
from bstack_utils.proxy import bstack1l1l11111l_opy_, bstack1ll1111111_opy_
from bstack_utils.bstack111l1l11l_opy_ import bstack1lll111l11l1_opy_, bstack1lll111l111l_opy_, bstack1lll1111l11l_opy_, bstack1lll1111lll1_opy_, \
    bstack1lll11111ll1_opy_, bstack1lll1111llll_opy_, bstack1lll111l1111_opy_, bstack1ll1lll1ll_opy_, bstack1lll111l11ll_opy_
from bstack_utils.bstack11l1lll1l1_opy_ import bstack1lll1llll1_opy_
from bstack_utils.session_utils import browserstack_executor_helper, bstack1ll111l1_opy_, update_caps_for_local, \
    bstack11l11l1l11_opy_, bstack1ll111ll11_opy_
from bstack_utils.test_data import TestData
from bstack_utils.bstack1llll11lll_opy_ import bstack1111l1lll1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1l11llll1l_opy_ import bstack1ll1lll1l_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack1l111ll11_opy_ import bstack1ll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l_opy_ import bstack1ll111111l_opy_, Events, bstack1lllllll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1ll11ll1_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll111111l_opy_ import bstack1ll111111l_opy_, Events, bstack1lllllll1_opy_
bstack1l1l1l1lll_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1llll1ll11_opy_ = None
bstack111l111ll1_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack1l11l1lll_opy_ = None
bstack1111l11lll_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack1lll11lll1_opy_ = None
bstack1llllllll_opy_ = None
bstack11lllll111_opy_ = None
bstack1llllll1l_opy_ = None
FRAMEWORK_NAME = bstack1l1_opy_ (u"ࠫࠬ⛟")
CONFIG = {}
bstack11ll111111_opy_ = False
bstack11l1ll1ll_opy_ = bstack1l1_opy_ (u"ࠬ࠭⛠")
bstack1l11l111_opy_ = bstack1l1_opy_ (u"࠭ࠧ⛡")
PARALLELISE_VANILLA_PYTHON = False
bstack1ll1l1ll1_opy_ = []
bstack111l1l11ll_opy_ = bstack1l1l1l1ll1_opy_
bstack1ll1l11l11ll_opy_ = bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⛢")
bstack1l111111_opy_ = {}
SESSION_NAME = None
bstack11llll1111_opy_ = False
logger = logger_utils.get_logger(__name__, bstack111l1l11ll_opy_)
store = {
    bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⛣"): []
}
bstack1ll1l111ll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lllll111ll_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1ll11ll1_opy_(
    test_framework_name=bstack111l11l1l1_opy_[bstack1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭⛤")] if bstack1111111ll1_opy_() else bstack111l11l1l1_opy_[bstack1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪ⛥")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack111ll1111l_opy_):
    try:
        page.evaluate(bstack1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ⛦"),
                      bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩ⛧") + json.dumps(
                          bstack111ll1111l_opy_) + bstack1l1_opy_ (u"ࠨࡽࡾࠤ⛨"))
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ⛩"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⛪"), bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ⛫") + json.dumps(
            message) + bstack1l1_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭⛬") + json.dumps(level) + bstack1l1_opy_ (u"ࠫࢂࢃࠧ⛭"))
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ⛮"), e)
def pytest_configure(config):
    global bstack11l1ll1ll_opy_
    global CONFIG
    global_config = Config.get_instance()
    config.args = bstack1111l1lll1_opy_.bstack1ll1l11lllll_opy_(config.args)
    global_config.bstack1l1lll1l1_opy_(bstack1l11llll_opy_(config.getoption(bstack1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ⛯"))))
    try:
        logger_utils.bstack1lllll1lllll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll111111l_opy_.invoke(Events.CONNECT, bstack1lllllll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⛰"), bstack1l1_opy_ (u"ࠨ࠲ࠪ⛱")))
        config = json.loads(os.environ.get(bstack1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣ⛲"), bstack1l1_opy_ (u"ࠥࡿࢂࠨ⛳")))
        cli.bstack1ll111111l1_opy_(bstack11lll11l1_opy_(bstack11l1ll1ll_opy_, CONFIG), cli_context.platform_index, bstack1ll111lll1_opy_)
    if cli.bstack11ll1l1l11_opy_(bstack1ll11lllll_opy_):
        cli.bstack1111llll11_opy_()
        logger.debug(bstack1l1_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ⛴") + str(cli_context.platform_index) + bstack1l1_opy_ (u"ࠧࠨ⛵"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦ⛶"), None)
    if cli.is_running() and when == bstack1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ⛷"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1l1_opy_ (u"ࠣࡥࡤࡰࡱࠨ⛸"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ⛹")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤ⛺"), bstack1l1_opy_ (u"ࠦࢀࢃࠢ⛻")))
            if bstack1ll1lll1l_opy_.bstack1l1llllll1_opy_(config):
                bstack1lll1l11l11l_opy_ = bstack1ll1lll1l_opy_.bstack1llll11l1_opy_(config)
                if item.execution_count > bstack1lll1l11l11l_opy_:
                    print(bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡵࡩࡹࡸࡩࡦࡵ࠽ࠤࠬ⛼"), report.nodeid, os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⛽")))
                    bstack1ll1lll1l_opy_.bstack1llll1l11l11_opy_(report.nodeid)
            else:
                print(bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠧ⛾"), report.nodeid, os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⛿")))
                bstack1ll1lll1l_opy_.bstack1llll1l11l11_opy_(report.nodeid)
        else:
            print(bstack1l1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡱࡣࡶࡷࡪࡪ࠺ࠡࠩ✀"), report.nodeid, os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ✁")))
    if cli.is_running():
        if when == bstack1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ✂"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack1l1_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ✃"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ✄"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ✅"))
    plugins = item.config.getoption(bstack1l1_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤ✆"))
    report = outcome.get_result()
    os.environ[bstack1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ✇")] = report.nodeid
    bstack1ll1l11ll1l1_opy_(item, call, report)
    if bstack1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣ✈") not in plugins or bstack1111111ll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧ✉"), None)
    page = getattr(item, bstack1l1_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦ✊"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1l11l1ll1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1l11111ll_opy_(item, report, summary, skipSessionName)
def bstack1ll1l11l1ll1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ✋") and report.skipped:
        bstack1lll111l11ll_opy_(report)
    if report.when in [bstack1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ✌"), bstack1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ✍")]:
        return
    if not bstack1ll11111l1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ✎")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ✏") + json.dumps(
                    report.nodeid) + bstack1l1_opy_ (u"ࠫࢂࢃࠧ✐"))
        os.environ[bstack1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ✑")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨ✒").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ✓")))
    bstack11l1111l11_opy_ = bstack1l1_opy_ (u"ࠣࠤ✔")
    bstack1lll111l11ll_opy_(report)
    if not passed:
        try:
            bstack11l1111l11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ✕").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1111l11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ✖")))
        bstack11l1111l11_opy_ = bstack1l1_opy_ (u"ࠦࠧ✗")
        if not passed:
            try:
                bstack11l1111l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ✘").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1111l11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ✙")
                    + json.dumps(bstack1l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣ✚"))
                    + bstack1l1_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ✛")
                )
            else:
                item._driver.execute_script(
                    bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ✜")
                    + json.dumps(str(bstack11l1111l11_opy_))
                    + bstack1l1_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨ✝")
                )
        except Exception as e:
            summary.append(bstack1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤ✞").format(e))
def bstack1ll1l11l1l11_opy_(test_name, error_message):
    try:
        bstack1ll1l11l1111_opy_ = []
        bstack1ll11l11ll_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ✟"), bstack1l1_opy_ (u"࠭࠰ࠨ✠"))
        bstack1111l1l1l_opy_ = {bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ✡"): test_name, bstack1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ✢"): error_message, bstack1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ✣"): bstack1ll11l11ll_opy_}
        bstack1ll1l11l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ✤"))
        if os.path.exists(bstack1ll1l11l1lll_opy_):
            with open(bstack1ll1l11l1lll_opy_) as f:
                bstack1ll1l11l1111_opy_ = json.load(f)
        bstack1ll1l11l1111_opy_.append(bstack1111l1l1l_opy_)
        with open(bstack1ll1l11l1lll_opy_, bstack1l1_opy_ (u"ࠫࡼ࠭✥")) as f:
            json.dump(bstack1ll1l11l1111_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪ✦") + str(e))
def bstack1ll1l11111ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ✧"), bstack1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ✨")]:
        return
    if (str(skipSessionName).lower() != bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭✩")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ✪")))
    bstack11l1111l11_opy_ = bstack1l1_opy_ (u"ࠥࠦ✫")
    bstack1lll111l11ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l1111l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ✬").format(e)
                )
        try:
            if passed:
                bstack1ll111ll11_opy_(getattr(item, bstack1l1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ✭"), None), bstack1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ✮"))
            else:
                error_message = bstack1l1_opy_ (u"ࠧࠨ✯")
                if bstack11l1111l11_opy_:
                    playwright_annotate(item._page, str(bstack11l1111l11_opy_), bstack1l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ✰"))
                    bstack1ll111ll11_opy_(getattr(item, bstack1l1_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ✱"), None), bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ✲"), str(bstack11l1111l11_opy_))
                    error_message = str(bstack11l1111l11_opy_)
                else:
                    bstack1ll111ll11_opy_(getattr(item, bstack1l1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ✳"), None), bstack1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ✴"))
                bstack1ll1l11l1l11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥ✵").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ✶"), default=bstack1l1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ✷"), help=bstack1l1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ✸"))
    parser.addoption(bstack1l1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ✹"), default=bstack1l1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ✺"), help=bstack1l1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ✻"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣ✼"), action=bstack1l1_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨ✽"), default=bstack1l1_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣ✾"),
                         help=bstack1l1_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣ✿"))
def bstack1llllll11l1_opy_(log):
    if not (log[bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ❀")] and log[bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ❁")].strip()):
        return
    active = bstack1lllll1lll1_opy_()
    log = {
        bstack1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ❂"): log[bstack1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ❃")],
        bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ❄"): bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠨ࡜ࠪ❅"),
        bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ❆"): log[bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ❇")],
    }
    if active:
        if active[bstack1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ❈")] == bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ❉"):
            log[bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭❊")] = active[bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ❋")]
        elif active[bstack1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭❌")] == bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧ❍"):
            log[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ❎")] = active[bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ❏")]
    TestHubHandler.bstack1llllll1l1_opy_([log])
def bstack1lllll1lll1_opy_():
    if len(store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ❐")]) > 0 and store[bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ❑")][-1]:
        return {
            bstack1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ❒"): bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭❓"),
            bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ❔"): store[bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ❕")][-1]
        }
    if store.get(bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ❖"), None):
        return {
            bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ❗"): bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࠫ❘"),
            bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ❙"): store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ❚")]
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
        item._1ll1l11l111l_opy_ = True
        bstack1l1ll11lll_opy_ = a11y.is_enabled_testcase(bstack1111l1l111l_opy_(item.own_markers))
        if not cli.bstack11ll1l1l11_opy_(bstack1ll11lllll_opy_):
            item._a11y_test_case = bstack1l1ll11lll_opy_
            if bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ❛"), None):
                driver = getattr(item, bstack1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ❜"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack1l1ll11lll_opy_)
        if not TestHubHandler.on() or bstack1ll1l11l11ll_opy_ != bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ❝"):
            return
        global current_test_uuid #, bstack1llllll11ll_opy_
        bstack1llll1l1lll_opy_ = {
            bstack1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ❞"): uuid4().__str__(),
            bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ❟"): bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"࡛ࠧࠩ❠")
        }
        current_test_uuid = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭❡")]
        store[bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭❢")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ❣")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lllll111ll_opy_[item.nodeid] = {**_1lllll111ll_opy_[item.nodeid], **bstack1llll1l1lll_opy_}
        bstack1ll1l11l1l1l_opy_(item, _1lllll111ll_opy_[item.nodeid], bstack1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ❤"))
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧ❥"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ❦")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭❧"))
    if bstack1ll1lll1l_opy_.bstack1llll111ll11_opy_():
            bstack1ll1l11llll1_opy_ = bstack1l1_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡣࡶࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠧ❨")
            logger.error(bstack1ll1l11llll1_opy_)
            bstack1llll1l1lll_opy_ = {
                bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ❩"): uuid4().__str__(),
                bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ❪"): bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠫ࡟࠭❫"),
                bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ❬"): bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"࡚࠭ࠨ❭"),
                bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ❮"): bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ❯"),
                bstack1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ❰"): bstack1ll1l11llll1_opy_,
                bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ❱"): [],
                bstack1l1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭❲"): []
            }
            bstack1ll1l11l1l1l_opy_(item, bstack1llll1l1lll_opy_, bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭❳"))
            pytest.skip(bstack1ll1l11llll1_opy_)
            return # skip all existing operations
    global bstack1ll1l111ll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11111ll1ll1_opy_():
        atexit.register(bstack11l1l1l1l_opy_)
        if not bstack1ll1l111ll11_opy_:
            try:
                bstack1ll1l111l111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1111111ll11_opy_():
                    bstack1ll1l111l111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1l111l111_opy_:
                    signal.signal(s, bstack1lll1lll111_opy_)
                bstack1ll1l111ll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢ❴") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll111l11l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ❵")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1llll1l1lll_opy_ = {
            bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭❶"): uuid,
            bstack1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭❷"): bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠪ࡞ࠬ❸"),
            bstack1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ❹"): bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ❺"),
            bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ❻"): bstack1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ❼"),
            bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ❽"): bstack1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ❾")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ❿")] = item
        store[bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ➀")] = [uuid]
        if not _1lllll111ll_opy_.get(item.nodeid, None):
            _1lllll111ll_opy_[item.nodeid] = {bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ➁"): [], bstack1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ➂"): []}
        _1lllll111ll_opy_[item.nodeid][bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭➃")].append(bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭➄")])
        _1lllll111ll_opy_[item.nodeid + bstack1l1_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩ➅")] = bstack1llll1l1lll_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1l1111ll1_opy_(item, bstack1llll1l1lll_opy_, bstack1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ➆"))
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ➇"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ➈"))
        return # skip all existing operations
    try:
        global bstack1l111111_opy_
        bstack1ll11l11ll_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll11l11ll_opy_ = int(os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭➉")))
        if bstack1l11111l11_opy_.bstack1lll1111_opy_() == bstack1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ➊"):
            if bstack1l11111l11_opy_.bstack1l1l11l1l_opy_() == bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ➋"):
                bstack1ll1l11lll11_opy_ = bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ➌"), None)
                bstack1ll1111l1_opy_ = bstack1ll1l11lll11_opy_ + bstack1l1_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ➍")
                driver = getattr(item, bstack1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ➎"), None)
                bstack1ll111l1ll_opy_ = getattr(item, bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ➏"), None)
                bstack1111l111ll_opy_ = getattr(item, bstack1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ➐"), None)
                PercySDK.screenshot(driver, bstack1ll1111l1_opy_, bstack1ll111l1ll_opy_=bstack1ll111l1ll_opy_, bstack1111l111ll_opy_=bstack1111l111ll_opy_, bstack1ll11l111_opy_=bstack1ll11l11ll_opy_)
        if not cli.bstack11ll1l1l11_opy_(bstack1ll11lllll_opy_):
            if getattr(item, bstack1l1_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ➑"), False):
                bstack111l1lll1l_opy_.bstack1l1ll1111l_opy_(getattr(item, bstack1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ➒"), None), bstack1l111111_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1llll1l1lll_opy_ = {
            bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ➓"): uuid4().__str__(),
            bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ➔"): bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠫ࡟࠭➕"),
            bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ➖"): bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ➗"),
            bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ➘"): bstack1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ➙"),
            bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ➚"): bstack1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ➛")
        }
        _1lllll111ll_opy_[item.nodeid + bstack1l1_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧ➜")] = bstack1llll1l1lll_opy_
        bstack1ll1l1111ll1_opy_(item, bstack1llll1l1lll_opy_, bstack1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭➝"))
    except Exception as err:
        print(bstack1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬ➞"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lll1111lll1_opy_(fixturedef.argname):
        store[bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭➟")] = request.node
    elif bstack1lll11111ll1_opy_(fixturedef.argname):
        store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭➠")] = request.node
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
            bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ➡"): fixturedef.argname,
            bstack1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ➢"): bstack1111111ll1l_opy_(outcome),
            bstack1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭➣"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ➤")]
        if not _1lllll111ll_opy_.get(current_test_item.nodeid, None):
            _1lllll111ll_opy_[current_test_item.nodeid] = {bstack1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ➥"): []}
        _1lllll111ll_opy_[current_test_item.nodeid][bstack1l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ➦")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ➧"), str(err))
if bstack1111111ll1_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1lllll111ll_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ➨")].bstack1lll1ll1_opy_(id(step))
        except Exception as err:
            print(bstack1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ➩"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1lllll111ll_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ➪")].bstack1lllll1llll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ➫"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            test_data: TestData = _1lllll111ll_opy_[request.node.nodeid][bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ➬")]
            test_data.bstack1lllll1llll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ➭"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1l11l11ll_opy_
        try:
            if not TestHubHandler.on() or bstack1ll1l11l11ll_opy_ != bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ➮"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ➯"), None)
            if not _1lllll111ll_opy_.get(request.node.nodeid, None):
                _1lllll111ll_opy_[request.node.nodeid] = {}
            test_data = TestData.bstack1ll1lll11lll_opy_(
                scenario, feature, request.node,
                name=bstack1lll1111llll_opy_(request.node, scenario),
                started_at=current_time(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ➰"),
                tags=bstack1lll111l1111_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llllllllll_opy_(driver) if driver and driver.session_id else {}
            )
            _1lllll111ll_opy_[request.node.nodeid][bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ➱")] = test_data
            bstack1ll1l1111l1l_opy_(test_data.uuid)
            TestHubHandler.send_run_event(bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭➲"), test_data)
        except Exception as err:
            print(bstack1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ➳"), str(err))
def bstack1ll1l11ll1ll_opy_(bstack1llllllll11_opy_):
    if bstack1llllllll11_opy_ in store[bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ➴")]:
        store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ➵")].remove(bstack1llllllll11_opy_)
def bstack1ll1l1111l1l_opy_(test_uuid):
    store[bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭➶")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll1ll11111l_opy_
def bstack1ll1l11ll1l1_opy_(item, call, report):
    logger.debug(bstack1l1_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡵࡸࠬ➷"))
    global bstack1ll1l11l11ll_opy_
    bstack111l111l1l_opy_ = current_time()
    if hasattr(report, bstack1l1_opy_ (u"ࠫࡸࡺ࡯ࡱࠩ➸")):
        bstack111l111l1l_opy_ = bstack1llllllll111_opy_(report.stop)
    elif hasattr(report, bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫ➹")):
        bstack111l111l1l_opy_ = bstack1llllllll111_opy_(report.start)
    try:
        if getattr(report, bstack1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ➺"), bstack1l1_opy_ (u"ࠧࠨ➻")) == bstack1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭➼"):
            logger.debug(bstack1l1_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ➽").format(getattr(report, bstack1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ➾"), bstack1l1_opy_ (u"ࠫࠬ➿")).__str__(), bstack1ll1l11l11ll_opy_))
            if bstack1ll1l11l11ll_opy_ == bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⟀"):
                _1lllll111ll_opy_[item.nodeid][bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⟁")] = bstack111l111l1l_opy_
                bstack1ll1l11l1l1l_opy_(item, _1lllll111ll_opy_[item.nodeid], bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⟂"), report, call)
                store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⟃")] = None
            elif bstack1ll1l11l11ll_opy_ == bstack1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ⟄"):
                test_data = _1lllll111ll_opy_[item.nodeid][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⟅")]
                test_data.set(hooks=_1lllll111ll_opy_[item.nodeid].get(bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⟆"), []))
                exception, bstack1llllll1l11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llllll1l11_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫ⟇"), bstack1l1_opy_ (u"࠭ࠧ⟈"))]
                test_data.stop(time=bstack111l111l1l_opy_, result=Result(result=getattr(report, bstack1l1_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⟉"), bstack1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⟊")), exception=exception, bstack1llllll1l11_opy_=bstack1llllll1l11_opy_))
                TestHubHandler.send_run_event(bstack1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⟋"), _1lllll111ll_opy_[item.nodeid][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⟌")])
        elif getattr(report, bstack1l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⟍"), bstack1l1_opy_ (u"ࠬ࠭⟎")) in [bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⟏"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⟐")]:
            logger.debug(bstack1l1_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ⟑").format(getattr(report, bstack1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⟒"), bstack1l1_opy_ (u"ࠪࠫ⟓")).__str__(), bstack1ll1l11l11ll_opy_))
            bstack1llllll1l1l_opy_ = item.nodeid + bstack1l1_opy_ (u"ࠫ࠲࠭⟔") + getattr(report, bstack1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ⟕"), bstack1l1_opy_ (u"࠭ࠧ⟖"))
            if getattr(report, bstack1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⟗"), False):
                hook_type = bstack1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⟘") if getattr(report, bstack1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⟙"), bstack1l1_opy_ (u"ࠪࠫ⟚")) == bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⟛") else bstack1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⟜")
                _1lllll111ll_opy_[bstack1llllll1l1l_opy_] = {
                    bstack1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⟝"): uuid4().__str__(),
                    bstack1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⟞"): bstack111l111l1l_opy_,
                    bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⟟"): hook_type
                }
            _1lllll111ll_opy_[bstack1llllll1l1l_opy_][bstack1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⟠")] = bstack111l111l1l_opy_
            bstack1ll1l11ll1ll_opy_(_1lllll111ll_opy_[bstack1llllll1l1l_opy_][bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⟡")])
            bstack1ll1l1111ll1_opy_(item, _1lllll111ll_opy_[bstack1llllll1l1l_opy_], bstack1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⟢"), report, call)
            if getattr(report, bstack1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ⟣"), bstack1l1_opy_ (u"࠭ࠧ⟤")) == bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⟥"):
                if getattr(report, bstack1l1_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⟦"), bstack1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⟧")) == bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⟨"):
                    bstack1llll1l1lll_opy_ = {
                        bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⟩"): uuid4().__str__(),
                        bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⟪"): current_time(),
                        bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⟫"): current_time()
                    }
                    _1lllll111ll_opy_[item.nodeid] = {**_1lllll111ll_opy_[item.nodeid], **bstack1llll1l1lll_opy_}
                    bstack1ll1l11l1l1l_opy_(item, _1lllll111ll_opy_[item.nodeid], bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⟬"))
                    bstack1ll1l11l1l1l_opy_(item, _1lllll111ll_opy_[item.nodeid], bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⟭"), report, call)
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧ⟮"), str(err))
def bstack1ll1l111lll1_opy_(test, bstack1llll1l1lll_opy_, result=None, call=None, bstack1l1111111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    test_data = {
        bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⟯"): bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⟰")],
        bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ⟱"): bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࠫ⟲"),
        bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⟳"): test.name,
        bstack1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭⟴"): {
            bstack1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⟵"): bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⟶"),
            bstack1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩ⟷"): inspect.getsource(test.obj)
        },
        bstack1l1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⟸"): test.name,
        bstack1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⟹"): test.name,
        bstack1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⟺"): bstack1111l1lll1_opy_.bstack1lll1llllll_opy_(test),
        bstack1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⟻"): file_path,
        bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⟼"): file_path,
        bstack1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⟽"): bstack1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⟾"),
        bstack1l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⟿"): file_path,
        bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⠀"): bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⠁")],
        bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⠂"): bstack1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⠃"),
        bstack1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭⠄"): {
            bstack1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ⠅"): test.nodeid
        },
        bstack1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪ⠆"): bstack1111l1l111l_opy_(test.own_markers)
    }
    if bstack1l1111111l_opy_ in [bstack1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⠇"), bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⠈")]:
        test_data[bstack1l1_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭⠉")] = {
            bstack1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⠊"): bstack1llll1l1lll_opy_.get(bstack1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⠋"), [])
        }
    if bstack1l1111111l_opy_ == bstack1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⠌"):
        test_data[bstack1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⠍")] = bstack1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⠎")
        test_data[bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⠏")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⠐")]
        test_data[bstack1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⠑")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⠒")]
    if result:
        test_data[bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⠓")] = result.outcome
        test_data[bstack1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⠔")] = result.duration * 1000
        test_data[bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⠕")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⠖")]
        if result.failed:
            test_data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⠗")] = TestHubHandler.bstack1ll1llll1ll_opy_(call.excinfo.typename)
            test_data[bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⠘")] = TestHubHandler.bstack1ll1l1lllll1_opy_(call.excinfo, result)
        test_data[bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⠙")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⠚")]
    if outcome:
        test_data[bstack1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⠛")] = bstack1111111ll1l_opy_(outcome)
        test_data[bstack1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⠜")] = 0
        test_data[bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⠝")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⠞")]
        if test_data[bstack1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⠟")] == bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⠠"):
            test_data[bstack1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⠡")] = bstack1l1_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭⠢")  # bstack1ll1l11l11l1_opy_
            test_data[bstack1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⠣")] = [{bstack1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⠤"): [bstack1l1_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⠥")]}]
        test_data[bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⠦")] = bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⠧")]
    return test_data
def bstack1ll1l11111l1_opy_(test, bstack1llll11l11l_opy_, bstack1l1111111l_opy_, result, call, outcome, bstack1ll1l11ll111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⠨")]
    hook_name = bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⠩")]
    hook_data = {
        bstack1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⠪"): bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⠫")],
        bstack1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭⠬"): bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⠭"),
        bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ⠮"): bstack1l1_opy_ (u"ࠫࢀࢃࠧ⠯").format(bstack1lll111l111l_opy_(hook_name)),
        bstack1l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⠰"): {
            bstack1l1_opy_ (u"࠭࡬ࡢࡰࡪࠫ⠱"): bstack1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⠲"),
            bstack1l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭⠳"): None
        },
        bstack1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ⠴"): test.name,
        bstack1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⠵"): bstack1111l1lll1_opy_.bstack1lll1llllll_opy_(test, hook_name),
        bstack1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⠶"): file_path,
        bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⠷"): file_path,
        bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⠸"): bstack1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⠹"),
        bstack1l1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⠺"): file_path,
        bstack1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⠻"): bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⠼")],
        bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⠽"): bstack1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ⠾") if bstack1ll1l11l11ll_opy_ == bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⠿") else bstack1l1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⡀"),
        bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⡁"): hook_type
    }
    bstack1l11ll11ll1_opy_ = bstack1llll11l111_opy_(_1lllll111ll_opy_.get(test.nodeid, None))
    if bstack1l11ll11ll1_opy_:
        hook_data[bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ⡂")] = bstack1l11ll11ll1_opy_
    if result:
        hook_data[bstack1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⡃")] = result.outcome
        hook_data[bstack1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⡄")] = result.duration * 1000
        hook_data[bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⡅")] = bstack1llll11l11l_opy_[bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⡆")]
        if result.failed:
            hook_data[bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⡇")] = TestHubHandler.bstack1ll1llll1ll_opy_(call.excinfo.typename)
            hook_data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⡈")] = TestHubHandler.bstack1ll1l1lllll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⡉")] = bstack1111111ll1l_opy_(outcome)
        hook_data[bstack1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⡊")] = 100
        hook_data[bstack1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⡋")] = bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⡌")]
        if hook_data[bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⡍")] == bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⡎"):
            hook_data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⡏")] = bstack1l1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⡐")  # bstack1ll1l11l11l1_opy_
            hook_data[bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⡑")] = [{bstack1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⡒"): [bstack1l1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⡓")]}]
    if bstack1ll1l11ll111_opy_:
        hook_data[bstack1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⡔")] = bstack1ll1l11ll111_opy_.result
        hook_data[bstack1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⡕")] = time_diff(bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⡖")], bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⡗")])
        hook_data[bstack1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⡘")] = bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⡙")]
        if hook_data[bstack1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⡚")] == bstack1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⡛"):
            hook_data[bstack1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⡜")] = TestHubHandler.bstack1ll1llll1ll_opy_(bstack1ll1l11ll111_opy_.exception_type)
            hook_data[bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⡝")] = [{bstack1l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⡞"): bstack111111l1l1l_opy_(bstack1ll1l11ll111_opy_.exception)}]
    return hook_data
def bstack1ll1l11l1l1l_opy_(test, bstack1llll1l1lll_opy_, bstack1l1111111l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1_opy_ (u"ࠪࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ⡟").format(bstack1l1111111l_opy_))
    test_data = bstack1ll1l111lll1_opy_(test, bstack1llll1l1lll_opy_, result, call, bstack1l1111111l_opy_, outcome)
    driver = getattr(test, bstack1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⡠"), None)
    if bstack1l1111111l_opy_ == bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⡡") and driver:
        test_data[bstack1l1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ⡢")] = TestHubHandler.bstack1llllllllll_opy_(driver)
    if bstack1l1111111l_opy_ == bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⡣"):
        bstack1l1111111l_opy_ = bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⡤")
    bstack1lllll1l1l1_opy_ = {
        bstack1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⡥"): bstack1l1111111l_opy_,
        bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⡦"): test_data
    }
    TestHubHandler.bstack11ll1l11ll_opy_(bstack1lllll1l1l1_opy_)
    if bstack1l1111111l_opy_ == bstack1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⡧"):
        threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⡨"): bstack1l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⡩")}
    elif bstack1l1111111l_opy_ == bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⡪"):
        threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⡫"): getattr(result, bstack1l1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⡬"), bstack1l1_opy_ (u"ࠪࠫ⡭"))}
def bstack1ll1l1111ll1_opy_(test, bstack1llll1l1lll_opy_, bstack1l1111111l_opy_, result=None, call=None, outcome=None, bstack1ll1l11ll111_opy_=None):
    logger.debug(bstack1l1_opy_ (u"ࠫࡸ࡫࡮ࡥࡡ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡨࡰࡱ࡮ࠤࡩࡧࡴࡢ࠮ࠣࡩࡻ࡫࡮ࡵࡖࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ⡮").format(bstack1l1111111l_opy_))
    hook_data = bstack1ll1l11111l1_opy_(test, bstack1llll1l1lll_opy_, bstack1l1111111l_opy_, result, call, outcome, bstack1ll1l11ll111_opy_)
    bstack1lllll1l1l1_opy_ = {
        bstack1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⡯"): bstack1l1111111l_opy_,
        bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ⡰"): hook_data
    }
    TestHubHandler.bstack11ll1l11ll_opy_(bstack1lllll1l1l1_opy_)
def bstack1llll11l111_opy_(bstack1llll1l1lll_opy_):
    if not bstack1llll1l1lll_opy_:
        return None
    if bstack1llll1l1lll_opy_.get(bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⡱"), None):
        return getattr(bstack1llll1l1lll_opy_[bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⡲")], bstack1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⡳"), None)
    return bstack1llll1l1lll_opy_.get(bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⡴"), None)
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
        places = [bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⡵"), bstack1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⡶"), bstack1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⡷")]
        logs = []
        for bstack1ll1l111l1l1_opy_ in places:
            records = caplog.get_records(bstack1ll1l111l1l1_opy_)
            bstack1ll1l11ll11l_opy_ = bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⡸") if bstack1ll1l111l1l1_opy_ == bstack1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭⡹") else bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⡺")
            bstack1ll1l11lll1l_opy_ = request.node.nodeid + (bstack1l1_opy_ (u"ࠪࠫ⡻") if bstack1ll1l111l1l1_opy_ == bstack1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⡼") else bstack1l1_opy_ (u"ࠬ࠳ࠧ⡽") + bstack1ll1l111l1l1_opy_)
            test_uuid = bstack1llll11l111_opy_(_1lllll111ll_opy_.get(bstack1ll1l11lll1l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1111111lll1_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⡾"): bstack1lllllll1lll_opy_(record.created).isoformat() + bstack1l1_opy_ (u"࡛ࠧࠩ⡿"),
                    bstack1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⢀"): record.levelname,
                    bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⢁"): record.message,
                    bstack1ll1l11ll11l_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1llllll1l1_opy_(logs)
    except Exception as err:
        print(bstack1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ⢂"), str(err))
def bstack11l1111ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11llll1111_opy_
    bstack1ll1llll1_opy_ = bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ⢃"), None) and bstack1l1lll111l_opy_(
            threading.current_thread(), bstack1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⢄"), None)
    bstack1ll1lll1_opy_ = getattr(driver, bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭⢅"), None) != None and getattr(driver, bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⢆"), None) == True
    if sequence == bstack1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⢇") and driver != None:
      if not bstack11llll1111_opy_ and bstack1ll11111l1_opy_() and bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⢈") in CONFIG and CONFIG[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⢉")] == True and accessibility_scripts.bstack1lll1l1ll1_opy_(driver_command) and (bstack1ll1lll1_opy_ or bstack1ll1llll1_opy_) and not bstack111l1ll1ll_opy_(args):
        try:
          bstack11llll1111_opy_ = True
          logger.debug(bstack1l1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭⢊").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ⢋").format(str(err)))
        bstack11llll1111_opy_ = False
    if sequence == bstack1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ⢌"):
        if driver_command == bstack1l1_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ⢍"):
            TestHubHandler.bstack1l1llll11_opy_({
                bstack1l1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ⢎"): response[bstack1l1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ⢏")],
                bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⢐"): store[bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⢑")]
            })
def bstack11l1l1l1l_opy_():
    global bstack1ll1l1ll1_opy_
    logger_utils.bstack1ll111l11l_opy_()
    logging.shutdown()
    TestHubHandler.bstack1llll1l11l1_opy_()
    for driver in bstack1ll1l1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1lll111_opy_(*args):
    global bstack1ll1l1ll1_opy_
    TestHubHandler.bstack1llll1l11l1_opy_()
    for driver in bstack1ll1l1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1l1llll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack11l111l11l_opy_=SESSION_NAME)
def bstack11ll1ll11_opy_(self, *args, **kwargs):
    bstack11111l111_opy_ = bstack1l1l1l1lll_opy_(self, *args, **kwargs)
    bstack1l11111l1l_opy_ = getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⢒"), None)
    if bstack1l11111l1l_opy_ and bstack1l11111l1l_opy_.get(bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⢓"), bstack1l1_opy_ (u"ࠧࠨ⢔")) == bstack1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⢕"):
        TestHubHandler.send_cbt_info(self)
    return bstack11111l111_opy_
@measure(event_name=EVENTS.bstack1lll1ll1l_opy_, stage=STAGE.bstack11ll1ll1_opy_, bstack11l111l11l_opy_=SESSION_NAME)
def bstack1llll1l11l_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.get_instance()
    if global_config.get_property(bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭⢖")):
        return
    global_config.bstack11l11111ll_opy_(bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⢗"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack1l1111l1ll_opy_.format(FRAMEWORK_NAME.split(bstack1l1_opy_ (u"ࠫ࠲࠭⢘"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll11111l1_opy_():
            Service.start = bstack11111lll1l_opy_
            Service.stop = bstack1111l1111l_opy_
            webdriver.Remote.get = bstack11lll1llll_opy_
            webdriver.Remote.__init__ = bstack11111l11ll_opy_
            if not isinstance(os.getenv(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭⢙")), str):
                return
            WebDriver.quit = bstack1l111l11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack11ll1ll11_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ⢚")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1l1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ⢛")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack11111lll1_opy_(bstack1l1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ⢜"), bstack11ll1l11_opy_)
    if bstack1ll1llll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⢝")) and callable(getattr(RemoteConnection, bstack1l1_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⢞"))):
                RemoteConnection._get_proxy_url = bstack1l1lllllll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1lllllll_opy_
        except Exception as e:
            logger.error(bstack11l1llllll_opy_.format(str(e)))
    if bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⢟") in str(framework_name).lower():
        if not bstack1ll11111l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11llll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11ll111_opy_
            Config.getoption = bstack11ll111l1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11ll1111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111ll11ll_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack11l111l11l_opy_=SESSION_NAME)
def bstack1l111l11l_opy_(self):
    global FRAMEWORK_NAME
    global bstack111l1ll11l_opy_
    global bstack1l1ll11l1_opy_
    try:
        if bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⢠") in FRAMEWORK_NAME and self.session_id != None and bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ⢡"), bstack1l1_opy_ (u"ࠧࠨ⢢")) != bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⢣"):
            bstack1ll11l1ll1_opy_ = bstack1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⢤") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⢥")
            bstack11lll1ll11_opy_(logger, True)
            if os.environ.get(bstack1l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⢦"), None):
                self.execute_script(
                    bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ⢧") + json.dumps(
                        os.environ.get(bstack1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⢨"))) + bstack1l1_opy_ (u"ࠧࡾࡿࠪ⢩"))
            if self != None:
                bstack11l11l1l11_opy_(self, bstack1ll11l1ll1_opy_, bstack1l1_opy_ (u"ࠨ࠮ࠣࠫ⢪").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack11ll1l1l11_opy_(bstack1ll11lllll_opy_):
            item = store.get(bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⢫"), None)
            if item is not None and bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⢬"), None):
                bstack111l1lll1l_opy_.bstack1l1ll1111l_opy_(self, bstack1l111111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1_opy_ (u"ࠫࠬ⢭")
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ⢮") + str(e))
    bstack1l1ll11l1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1lll1l1l11_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack11l111l11l_opy_=SESSION_NAME)
def bstack11111l11ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack111l1ll11l_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1l1l1l1lll_opy_
    global bstack1ll1l1ll1_opy_
    global bstack11l1ll1ll_opy_
    global bstack1l11l111_opy_
    global bstack1l111111_opy_
    CONFIG[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⢯")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack11lll11l1_opy_(bstack11l1ll1ll_opy_, CONFIG)
    logger.debug(bstack1l1ll1l1ll_opy_.format(command_executor))
    proxy = bstack11llll111l_opy_(CONFIG, proxy)
    bstack1ll11l11ll_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll11l11ll_opy_ = int(os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⢰")))
    except:
        bstack1ll11l11ll_opy_ = 0
    bstack1l1ll11l11_opy_ = get_caps(CONFIG, bstack1ll11l11ll_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1l1ll11l11_opy_)))
    bstack1l111111_opy_ = CONFIG.get(bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⢱"))[bstack1ll11l11ll_opy_]
    if bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⢲") in CONFIG and CONFIG[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⢳")]:
        update_caps_for_local(bstack1l1ll11l11_opy_, bstack1l11l111_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack1ll11l11ll_opy_) and a11y.is_platform_supported(bstack1l1ll11l11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack11ll1l1l11_opy_(bstack1ll11lllll_opy_):
            a11y.set_capabilities(bstack1l1ll11l11_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll1l1111_opy_ = bstack1111111ll_opy_(desired_capabilities)
        bstack11ll1l1111_opy_[bstack1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ⢴")] = bstack1lll1ll1ll_opy_(CONFIG)
        bstack11ll1111ll_opy_ = get_caps(bstack11ll1l1111_opy_)
        if bstack11ll1111ll_opy_:
            bstack1l1ll11l11_opy_ = update(bstack11ll1111ll_opy_, bstack1l1ll11l11_opy_)
        desired_capabilities = None
    if options:
        bstack1l111111l1_opy_(options, bstack1l1ll11l11_opy_)
    if not options:
        options = bstack1ll111lll1_opy_(bstack1l1ll11l11_opy_)
    if proxy and bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ⢵")):
        options.proxy(proxy)
    if options and bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⢶")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lllllll1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⢷")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1ll11l11_opy_)
    logger.info(bstack111ll11lll_opy_)
    bstack11l1l1ll_opy_.end(EVENTS.bstack1lll1ll1l_opy_.value, EVENTS.bstack1lll1ll1l_opy_.value + bstack1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⢸"),
                               EVENTS.bstack1lll1ll1l_opy_.value + bstack1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⢹"), True, None)
    try:
        if bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⢺")):
            bstack1l1l1l1lll_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⢻")):
            bstack1l1l1l1lll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ⢼")):
            bstack1l1l1l1lll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l1l1l1lll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11ll1111l1_opy_:
        logger.error(bstack1llll11111_opy_.format(bstack1l1_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠬ⢽"), str(bstack11ll1111l1_opy_)))
        raise bstack11ll1111l1_opy_
    try:
        bstack11llll1ll_opy_ = bstack1l1_opy_ (u"ࠧࠨ⢾")
        if bstack1lllllll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ⢿")):
            bstack11llll1ll_opy_ = self.caps.get(bstack1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ⣀"))
        else:
            bstack11llll1ll_opy_ = self.capabilities.get(bstack1l1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⣁"))
        if bstack11llll1ll_opy_:
            bstack111lll1ll_opy_(bstack11llll1ll_opy_)
            if bstack1lllllll1l_opy_() <= version.parse(bstack1l1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ⣂")):
                self.command_executor._url = bstack1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⣃") + bstack11l1ll1ll_opy_ + bstack1l1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ⣄")
            else:
                self.command_executor._url = bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ⣅") + bstack11llll1ll_opy_ + bstack1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ⣆")
            logger.debug(bstack111ll11l_opy_.format(bstack11llll1ll_opy_))
        else:
            logger.debug(bstack1l1lll11l_opy_.format(bstack1l1_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ⣇")))
    except Exception as e:
        logger.debug(bstack1l1lll11l_opy_.format(e))
    bstack111l1ll11l_opy_ = self.session_id
    if bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⣈") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⣉"), None)
        if item:
            bstack1ll1l1111l11_opy_ = getattr(item, bstack1l1_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪ⣊"), False)
            if not getattr(item, bstack1l1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⣋"), None) and bstack1ll1l1111l11_opy_:
                setattr(store[bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⣌")], bstack1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⣍"), self)
        bstack1l11111l1l_opy_ = getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⣎"), None)
        if bstack1l11111l1l_opy_ and bstack1l11111l1l_opy_.get(bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⣏"), bstack1l1_opy_ (u"ࠫࠬ⣐")) == bstack1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⣑"):
            TestHubHandler.send_cbt_info(self)
    bstack1ll1l1ll1_opy_.append(self)
    if bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⣒") in CONFIG and bstack1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⣓") in CONFIG[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⣔")][bstack1ll11l11ll_opy_]:
        SESSION_NAME = CONFIG[bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⣕")][bstack1ll11l11ll_opy_][bstack1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⣖")]
    logger.debug(bstack1ll11l11l1_opy_.format(bstack111l1ll11l_opy_))
@measure(event_name=EVENTS.bstack1lllll11_opy_, stage=STAGE.bstack1ll1llll_opy_, bstack11l111l11l_opy_=SESSION_NAME)
def bstack11lll1llll_opy_(self, url):
    global bstack1l11l1ll1_opy_
    global CONFIG
    try:
        bstack1ll111l1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1llll1ll1_opy_.format(str(err)))
    try:
        bstack1l11l1ll1_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack11lll1l111_opy_):
                bstack1ll111l1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1llll1ll1_opy_.format(str(err)))
        raise e
def bstack1ll11l1lll_opy_(item, when):
    global bstack11lllll111_opy_
    try:
        bstack11lllll111_opy_(item, when)
    except Exception as e:
        pass
def bstack11ll1111_opy_(item, call, rep):
    global bstack1llllll1l_opy_
    global bstack1ll1l1ll1_opy_
    name = bstack1l1_opy_ (u"ࠫࠬ⣗")
    try:
        if rep.when == bstack1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⣘"):
            bstack111l1ll11l_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⣙"))
            try:
                if (str(skipSessionName).lower() != bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ⣚")):
                    name = str(rep.nodeid)
                    executor_string = browserstack_executor_helper(bstack1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⣛"), name, bstack1l1_opy_ (u"ࠩࠪ⣜"), bstack1l1_opy_ (u"ࠪࠫ⣝"), bstack1l1_opy_ (u"ࠫࠬ⣞"), bstack1l1_opy_ (u"ࠬ࠭⣟"))
                    os.environ[bstack1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⣠")] = name
                    for driver in bstack1ll1l1ll1_opy_:
                        if bstack111l1ll11l_opy_ == driver.session_id:
                            driver.execute_script(executor_string)
            except Exception as e:
                logger.debug(bstack1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ⣡").format(str(e)))
            try:
                bstack1ll1lll1ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⣢"):
                    status = bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⣣") if rep.outcome.lower() == bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⣤") else bstack1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⣥")
                    reason = bstack1l1_opy_ (u"ࠬ࠭⣦")
                    if status == bstack1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⣧"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1_opy_ (u"ࠧࡪࡰࡩࡳࠬ⣨") if status == bstack1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⣩") else bstack1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⣪")
                    data = name + bstack1l1_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ⣫") if status == bstack1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⣬") else name + bstack1l1_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ⣭") + reason
                    bstack11l11l1ll_opy_ = browserstack_executor_helper(bstack1l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ⣮"), bstack1l1_opy_ (u"ࠧࠨ⣯"), bstack1l1_opy_ (u"ࠨࠩ⣰"), bstack1l1_opy_ (u"ࠩࠪ⣱"), level, data)
                    for driver in bstack1ll1l1ll1_opy_:
                        if bstack111l1ll11l_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11l1ll_opy_)
            except Exception as e:
                logger.debug(bstack1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ⣲").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ⣳").format(str(e)))
    bstack1llllll1l_opy_(item, call, rep)
notset = Notset()
def bstack11ll111l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llllllll_opy_
    if str(name).lower() == bstack1l1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ⣴"):
        return bstack1l1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ⣵")
    else:
        return bstack1llllllll_opy_(self, name, default, skip)
def bstack1l1lllllll_opy_(self):
    global CONFIG
    global bstack1l11l1lll_opy_
    try:
        proxy = bstack1l1l11111l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ⣶")):
                proxies = bstack1ll1111111_opy_(proxy, bstack11lll11l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1l1l111l_opy_ = proxies.popitem()
                    if bstack1l1_opy_ (u"ࠣ࠼࠲࠳ࠧ⣷") in bstack1l1l1l111l_opy_:
                        return bstack1l1l1l111l_opy_
                    else:
                        return bstack1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⣸") + bstack1l1l1l111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ⣹").format(str(e)))
    return bstack1l11l1lll_opy_(self)
def bstack1ll1llll1l_opy_():
    return (bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⣺") in CONFIG or bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⣻") in CONFIG) and bstack11l111ll_opy_() and bstack1lllllll1l_opy_() >= version.parse(
        bstack11l1l1ll11_opy_)
def bstack11ll11ll_opy_(self,
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
    CONFIG[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⣼")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1ll11l11ll_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1ll11l11ll_opy_ = int(os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⣽")))
    except:
        bstack1ll11l11ll_opy_ = 0
    CONFIG[bstack1l1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ⣾")] = True
    bstack1l1ll11l11_opy_ = get_caps(CONFIG, bstack1ll11l11ll_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1l1ll11l11_opy_)))
    if CONFIG.get(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⣿")):
        update_caps_for_local(bstack1l1ll11l11_opy_, bstack1l11l111_opy_)
    if bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⤀") in CONFIG and bstack1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⤁") in CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⤂")][bstack1ll11l11ll_opy_]:
        SESSION_NAME = CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⤃")][bstack1ll11l11ll_opy_][bstack1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⤄")]
    import urllib
    import json
    if bstack1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⤅") in CONFIG and str(CONFIG[bstack1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⤆")]).lower() != bstack1l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ⤇"):
        bstack11111l11l_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack11111l11l_opy_ + urllib.parse.quote(json.dumps(bstack1l1ll11l11_opy_))
    else:
        cdpUrl = bstack1l1_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭⤈") + urllib.parse.quote(json.dumps(bstack1l1ll11l11_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1lllll1ll_opy_
        if not bstack1ll11111l1_opy_():
            global bstack11l111l1_opy_
            if not bstack11l111l1_opy_:
                from bstack_utils.helper import bstack111l11l111_opy_, bstack111111l11l1_opy_
                bstack11l111l1_opy_ = bstack111l11l111_opy_()
                bstack111111l11l1_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l1lllll1ll_opy_
            return
        BrowserType.launch = bstack11ll11ll_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll1l111ll1l_opy_():
    global CONFIG
    global bstack11ll111111_opy_
    global bstack11l1ll1ll_opy_
    global bstack1l11l111_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack111l1l11ll_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ⤉")))
    bstack11ll111111_opy_ = eval(os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ⤊")))
    bstack11l1ll1ll_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ⤋"))
    bstack11111lll_opy_(CONFIG, bstack11ll111111_opy_)
    bstack111l1l11ll_opy_ = logger_utils.configure_logger(CONFIG, bstack111l1l11ll_opy_)
    if cli.bstack1111llll1_opy_():
        bstack1ll111111l_opy_.invoke(Events.CONNECT, bstack1lllllll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⤌"), bstack1l1_opy_ (u"ࠩ࠳ࠫ⤍")))
        cli.bstack1l1ll111ll_opy_(cli_context.platform_index)
        cli.bstack1ll111111l1_opy_(bstack11lll11l1_opy_(bstack11l1ll1ll_opy_, CONFIG), cli_context.platform_index, bstack1ll111lll1_opy_)
        cli.bstack1111llll11_opy_()
        logger.debug(bstack1l1_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ⤎") + str(cli_context.platform_index) + bstack1l1_opy_ (u"ࠦࠧ⤏"))
        return # skip all existing operations
    global bstack1l1l1l1lll_opy_
    global bstack1l1ll11l1_opy_
    global bstack1l111lll1l_opy_
    global bstack1llll1ll11_opy_
    global bstack111l111ll1_opy_
    global bstack1l1ll11ll_opy_
    global bstack1111l11lll_opy_
    global bstack1l11l1ll1_opy_
    global bstack1l11l1lll_opy_
    global bstack1llllllll_opy_
    global bstack11lllll111_opy_
    global bstack1llllll1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l1l1lll_opy_ = webdriver.Remote.__init__
        bstack1l1ll11l1_opy_ = WebDriver.quit
        bstack1111l11lll_opy_ = WebDriver.close
        bstack1l11l1ll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⤐") in CONFIG or bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⤑") in CONFIG) and bstack11l111ll_opy_():
        if bstack1lllllll1l_opy_() < version.parse(bstack11l1l1ll11_opy_):
            logger.error(bstack1l11111111_opy_.format(bstack1lllllll1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⤒")) and callable(getattr(RemoteConnection, bstack1l1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⤓"))):
                    bstack1l11l1lll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l11l1lll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11l1llllll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llllllll_opy_ = Config.getoption
        from _pytest import runner
        bstack11lllll111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1l1_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤ⤔"), bstack11llllll1l_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1llllll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ⤕"))
    bstack1l11l111_opy_ = CONFIG.get(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ⤖"), {}).get(bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⤗"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack1llll1l11l_opy_(bstack1111ll1l_opy_)
if (bstack11111ll1ll1_opy_()):
    bstack1ll1l111ll1l_opy_()
@error_handler(class_method=False)
def bstack1ll1l111llll_opy_(hook_name, event, bstack11l11llll1l_opy_=None):
    if hook_name not in [bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⤘"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⤙"), bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⤚"), bstack1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⤛"), bstack1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⤜"), bstack1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⤝"), bstack1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ⤞"), bstack1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⤟")]:
        return
    node = store[bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⤠")]
    if hook_name in [bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⤡"), bstack1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⤢")]:
        node = store[bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⤣")]
    elif hook_name in [bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⤤"), bstack1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⤥")]:
        node = store[bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ⤦")]
    hook_type = bstack1lll1111l11l_opy_(hook_name)
    if event == bstack1l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ⤧"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1llll11l11l_opy_ = {
            bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⤨"): uuid,
            bstack1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⤩"): current_time(),
            bstack1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ⤪"): bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⤫"),
            bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⤬"): hook_type,
            bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⤭"): hook_name
        }
        store[bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⤮")].append(uuid)
        bstack1ll1l111l1ll_opy_ = node.nodeid
        if hook_type == bstack1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⤯"):
            if not _1lllll111ll_opy_.get(bstack1ll1l111l1ll_opy_, None):
                _1lllll111ll_opy_[bstack1ll1l111l1ll_opy_] = {bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⤰"): []}
            _1lllll111ll_opy_[bstack1ll1l111l1ll_opy_][bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⤱")].append(bstack1llll11l11l_opy_[bstack1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⤲")])
        _1lllll111ll_opy_[bstack1ll1l111l1ll_opy_ + bstack1l1_opy_ (u"ࠬ࠳ࠧ⤳") + hook_name] = bstack1llll11l11l_opy_
        bstack1ll1l1111ll1_opy_(node, bstack1llll11l11l_opy_, bstack1l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⤴"))
    elif event == bstack1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⤵"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l11llll1l_opy_)
            return
        bstack1llllll1l1l_opy_ = node.nodeid + bstack1l1_opy_ (u"ࠨ࠯ࠪ⤶") + hook_name
        _1lllll111ll_opy_[bstack1llllll1l1l_opy_][bstack1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⤷")] = current_time()
        bstack1ll1l11ll1ll_opy_(_1lllll111ll_opy_[bstack1llllll1l1l_opy_][bstack1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⤸")])
        bstack1ll1l1111ll1_opy_(node, _1lllll111ll_opy_[bstack1llllll1l1l_opy_], bstack1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⤹"), bstack1ll1l11ll111_opy_=bstack11l11llll1l_opy_)
def bstack1ll1l1111lll_opy_():
    global bstack1ll1l11l11ll_opy_
    if bstack1111111ll1_opy_():
        bstack1ll1l11l11ll_opy_ = bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⤺")
    else:
        bstack1ll1l11l11ll_opy_ = bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⤻")
@TestHubHandler.bstack1ll1ll11111l_opy_
def bstack1ll1l111l11l_opy_():
    bstack1ll1l1111lll_opy_()
    if cli.is_running():
        try:
            bstack1lllllll11l1_opy_(bstack1ll1l111llll_opy_)
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⤼").format(e))
        return
    if bstack11l111ll_opy_():
        global_config = Config.get_instance()
        bstack1l1_opy_ (u"ࠨࠩࠪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡁࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡧࡦࡶࡶࠤࡺࡹࡥࡥࠢࡩࡳࡷࠦࡡ࠲࠳ࡼࠤࡨࡵ࡭࡮ࡣࡱࡨࡸ࠳ࡷࡳࡣࡳࡴ࡮ࡴࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡹࠦࡩࡴࠢࡳࡥࡹࡩࡨࡦࡦࠣ࡭ࡳࠦࡡࠡࡦ࡬ࡪ࡫࡫ࡲࡦࡰࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࠥ࡯ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡷࡶࠤࡼ࡫ࠠ࡯ࡧࡨࡨࠥࡺ࡯ࠡࡷࡶࡩ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࡐࡢࡶࡦ࡬࠭ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡩࡣࡱࡨࡱ࡫ࡲࠪࠢࡩࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠩࠪࠫ⤽")
        if global_config.get_property(bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭⤾")):
            if CONFIG.get(bstack1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⤿")) is not None and int(CONFIG[bstack1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ⥀")]) > 1:
                bstack1lll1llll1_opy_(bstack11l1111ll1_opy_)
            return
        bstack1lll1llll1_opy_(bstack11l1111ll1_opy_)
    try:
        bstack1lllllll11l1_opy_(bstack1ll1l111llll_opy_)
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ⥁").format(e))
bstack1ll1l111l11l_opy_()