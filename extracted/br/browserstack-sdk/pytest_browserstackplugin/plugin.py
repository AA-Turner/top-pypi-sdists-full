# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l11l1l11_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1lll1ll1l_opy_, update, bstack1llllll1111_opy_,
                                       bstack11l11lll_opy_, bstack111111ll1l_opy_, bstack11lllll11_opy_, bstack111l1lllll_opy_,
                                       bstack111lll11l1_opy_, bstack11l111l1l_opy_, bstack1l11l11l1_opy_,
                                       bstack11lll11ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack111lllllll_opy_)
from browserstack_sdk.bstack1ll11l11ll_opy_ import bstack11l1l11ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1llll111l1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11111l1l11_opy_, bstack1l11l1l111_opy_, bstack1lll1111l1_opy_, \
    bstack11lllllll1_opy_
from bstack_utils.helper import bstack11ll1l11l_opy_, bstack1llll1lllll1_opy_, bstack1lll1ll1l11_opy_, bstack1l11ll1111_opy_, bstack1l1ll1ll1l_opy_, bstack1l1l111l1l_opy_, \
    bstack1lllll1l1l1l_opy_, \
    bstack1llll11l1111_opy_, bstack1lll1l11l1_opy_, bstack111ll11l11_opy_, bstack1llll1lll111_opy_, bstack1lll1l111_opy_, Notset, \
    bstack1l111l111l_opy_, bstack1ll1l1llll1_opy_, bstack1llllll11l1l_opy_, Result, bstack1lllllll1l1l_opy_, bstack1lllll1llll1_opy_, error_handler, \
    bstack11ll111l_opy_, bstack1111ll1l11_opy_, bstack1lll1lll1_opy_, bstack1llll1lll11l_opy_
from bstack_utils.bstack1lll1lllll11_opy_ import bstack1lll1lll1lll_opy_
from bstack_utils.messages import bstack1llll11111_opy_, bstack11l11ll1l1_opy_, bstack11l111l11_opy_, bstack11lll1l1ll_opy_, bstack1l11l1ll11_opy_, \
    bstack111ll11ll_opy_, bstack1l11llll1l_opy_, CONFIG_FILE_CONTENT, bstack111l1l111_opy_, bstack11111ll1l1_opy_, \
    bstack1l1ll11l_opy_, bstack1llll1l1_opy_, bstack1ll11lll11_opy_
from bstack_utils.proxy import bstack1ll111lll1_opy_, bstack1ll11ll11_opy_
from bstack_utils.bstack11l1111lll_opy_ import bstack1ll1l11l1l1l_opy_, bstack1ll1l11ll11l_opy_, bstack1ll1l11l1lll_opy_, bstack1ll1l11l1ll1_opy_, \
    bstack1ll1l11ll111_opy_, bstack1ll1l11lll1l_opy_, bstack1ll1l11lllll_opy_, bstack1l1l11ll11_opy_, bstack1ll1l11ll1ll_opy_
from bstack_utils.bstack111ll11l1l_opy_ import bstack1111l1111_opy_
from bstack_utils.bstack11ll11ll11_opy_ import bstack1l1l1l11l_opy_, bstack111l1llll_opy_, update_caps_for_local, \
    bstack111ll1l1_opy_, bstack11l1l11lll_opy_
from bstack_utils.bstack1llll11llll_opy_ import bstack1llll1l1l1l_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1lllll1l11_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1l1lll1l11_opy_ import bstack1ll11l11l1_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack11llll1ll_opy_ import bstack1ll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack1l1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1ll1ll1l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack1l1ll1lll_opy_
bstack1l1ll111l_opy_ = None
bstack1l11111ll_opy_ = None
bstack11l1lll11l_opy_ = None
bstack11ll11l11_opy_ = None
bstack11llll1l1_opy_ = None
bstack11ll1l1l11_opy_ = None
bstack1l1111l11_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack1ll1111111_opy_ = None
bstack11111l1lll_opy_ = None
bstack1l1l11l1l_opy_ = None
bstack1lllllll1ll_opy_ = None
bstack11lll1111_opy_ = None
FRAMEWORK_NAME = bstack11ll11_opy_ (u"ࠬ࠭⣦")
CONFIG = {}
bstack1lll11111_opy_ = False
bstack11l1ll11l1_opy_ = bstack11ll11_opy_ (u"࠭ࠧ⣧")
bstack111lllll1_opy_ = bstack11ll11_opy_ (u"ࠧࠨ⣨")
PARALLELISE_VANILLA_PYTHON = False
bstack1ll11llll_opy_ = []
bstack111lllll1l_opy_ = bstack11111l1l11_opy_
bstack1ll111l1111l_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⣩")
bstack111l1111_opy_ = {}
SESSION_NAME = None
bstack111l1ll111_opy_ = False
logger = logger_utils.get_logger(__name__, bstack111lllll1l_opy_)
store = {
    bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⣪"): []
}
bstack1ll1111l11ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lll11l1l11_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1ll1ll1l_opy_(
    test_framework_name=bstack11llll11_opy_[bstack11ll11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ⣫")] if bstack1lll1l111_opy_() else bstack11llll11_opy_[bstack11ll11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫ⣬")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack11ll1ll1l_opy_):
    try:
        page.evaluate(bstack11ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⣭"),
                      bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ⣮") + json.dumps(
                          bstack11ll1ll1l_opy_) + bstack11ll11_opy_ (u"ࠢࡾࡿࠥ⣯"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ⣰"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack11ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ⣱"), bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ⣲") + json.dumps(
            message) + bstack11ll11_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ⣳") + json.dumps(level) + bstack11ll11_opy_ (u"ࠬࢃࡽࠨ⣴"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ⣵"), e)
def pytest_configure(config):
    global bstack11l1ll11l1_opy_
    global CONFIG
    global_config = Config.bstack111llll11_opy_()
    config.args = bstack1lllll1l11_opy_.bstack1ll111l1ll1l_opy_(config.args)
    global_config.bstack1l1l1ll11l_opy_(bstack1lll1lll1_opy_(config.getoption(bstack11ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⣶"))))
    try:
        logger_utils.bstack1lll1ll1llll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack1l1ll1lll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⣷"), bstack11ll11_opy_ (u"ࠩ࠳ࠫ⣸")))
        config = json.loads(os.environ.get(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤ⣹"), bstack11ll11_opy_ (u"ࠦࢀࢃࠢ⣺")))
        cli.bstack1l11l11l1l1_opy_(bstack111ll11l11_opy_(bstack11l1ll11l1_opy_, CONFIG), cli_context.platform_index, bstack1llllll1111_opy_)
    if cli.bstack111l1l1ll1_opy_(bstack1ll1llll11_opy_):
        cli.bstack11lllll1l1_opy_()
        logger.debug(bstack11ll11_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⣻") + str(cli_context.platform_index) + bstack11ll11_opy_ (u"ࠨࠢ⣼"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11ll11_opy_ (u"ࠢࡸࡪࡨࡲࠧ⣽"), None)
    if cli.is_running() and when == bstack11ll11_opy_ (u"ࠣࡥࡤࡰࡱࠨ⣾"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack11ll11_opy_ (u"ࠤࡦࡥࡱࡲࠢ⣿"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⤀")))
        if not passed:
            config = json.loads(os.environ.get(bstack11ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ⤁"), bstack11ll11_opy_ (u"ࠧࢁࡽࠣ⤂")))
            if bstack1ll11l11l1_opy_.bstack1111l1lll1_opy_(config):
                bstack1ll1ll11llll_opy_ = bstack1ll11l11l1_opy_.bstack1llll1l11l_opy_(config)
                if item.execution_count > bstack1ll1ll11llll_opy_:
                    print(bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡶࡪࡺࡲࡪࡧࡶ࠾ࠥ࠭⤃"), report.nodeid, os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⤄")))
                    bstack1ll11l11l1_opy_.bstack1lll11lll111_opy_(report.nodeid)
            else:
                print(bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠨ⤅"), report.nodeid, os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⤆")))
                bstack1ll11l11l1_opy_.bstack1lll11lll111_opy_(report.nodeid)
        else:
            print(bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡲࡤࡷࡸ࡫ࡤ࠻ࠢࠪ⤇"), report.nodeid, os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⤈")))
    if cli.is_running():
        if when == bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⤉"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack11ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⤊"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack11ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ⤋"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⤌"))
    plugins = item.config.getoption(bstack11ll11_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥ⤍"))
    report = outcome.get_result()
    os.environ[bstack11ll11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⤎")] = report.nodeid
    bstack1ll1111ll111_opy_(item, call, report)
    if bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤ⤏") not in plugins or bstack1lll1l111_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll11_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨ⤐"), None)
    page = getattr(item, bstack11ll11_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧ⤑"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1111lll1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll111l1l1ll_opy_(item, report, summary, skipSessionName)
def bstack1ll1111lll1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⤒") and report.skipped:
        bstack1ll1l11ll1ll_opy_(report)
    if report.when in [bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⤓"), bstack11ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ⤔")]:
        return
    if not bstack1l1ll1ll1l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ⤕")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ⤖") + json.dumps(
                    report.nodeid) + bstack11ll11_opy_ (u"ࠬࢃࡽࠨ⤗"))
        os.environ[bstack11ll11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⤘")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢ⤙").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⤚")))
    bstack1l1l11l11_opy_ = bstack11ll11_opy_ (u"ࠤࠥ⤛")
    bstack1ll1l11ll1ll_opy_(report)
    if not passed:
        try:
            bstack1l1l11l11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⤜").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l11l11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⤝")))
        bstack1l1l11l11_opy_ = bstack11ll11_opy_ (u"ࠧࠨ⤞")
        if not passed:
            try:
                bstack1l1l11l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⤟").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l11l11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⤠")
                    + json.dumps(bstack11ll11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤ⤡"))
                    + bstack11ll11_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ⤢")
                )
            else:
                item._driver.execute_script(
                    bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⤣")
                    + json.dumps(str(bstack1l1l11l11_opy_))
                    + bstack11ll11_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢ⤤")
                )
        except Exception as e:
            summary.append(bstack11ll11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥ⤥").format(e))
def bstack1ll1111llll1_opy_(test_name, error_message):
    try:
        bstack1ll111l1l1l1_opy_ = []
        bstack1l11l11ll_opy_ = os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⤦"), bstack11ll11_opy_ (u"ࠧ࠱ࠩ⤧"))
        bstack1ll1l11111_opy_ = {bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⤨"): test_name, bstack11ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⤩"): error_message, bstack11ll11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⤪"): bstack1l11l11ll_opy_}
        bstack1ll111l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⤫"))
        if os.path.exists(bstack1ll111l1l11l_opy_):
            with open(bstack1ll111l1l11l_opy_) as f:
                bstack1ll111l1l1l1_opy_ = json.load(f)
        bstack1ll111l1l1l1_opy_.append(bstack1ll1l11111_opy_)
        with open(bstack1ll111l1l11l_opy_, bstack11ll11_opy_ (u"ࠬࡽࠧ⤬")) as f:
            json.dump(bstack1ll111l1l1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫ⤭") + str(e))
def bstack1ll111l1l1ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⤮"), bstack11ll11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ⤯")]:
        return
    if (str(skipSessionName).lower() != bstack11ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⤰")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⤱")))
    bstack1l1l11l11_opy_ = bstack11ll11_opy_ (u"ࠦࠧ⤲")
    bstack1ll1l11ll1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l11l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ⤳").format(e)
                )
        try:
            if passed:
                bstack11l1l11lll_opy_(getattr(item, bstack11ll11_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⤴"), None), bstack11ll11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ⤵"))
            else:
                error_message = bstack11ll11_opy_ (u"ࠨࠩ⤶")
                if bstack1l1l11l11_opy_:
                    playwright_annotate(item._page, str(bstack1l1l11l11_opy_), bstack11ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ⤷"))
                    bstack11l1l11lll_opy_(getattr(item, bstack11ll11_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⤸"), None), bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⤹"), str(bstack1l1l11l11_opy_))
                    error_message = str(bstack1l1l11l11_opy_)
                else:
                    bstack11l1l11lll_opy_(getattr(item, bstack11ll11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ⤺"), None), bstack11ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ⤻"))
                bstack1ll1111llll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦ⤼").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11ll11_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ⤽"), default=bstack11ll11_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⤾"), help=bstack11ll11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⤿"))
    parser.addoption(bstack11ll11_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ⥀"), default=bstack11ll11_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⥁"), help=bstack11ll11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⥂"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll11_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤ⥃"), action=bstack11ll11_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ⥄"), default=bstack11ll11_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ⥅"),
                         help=bstack11ll11_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ⥆"))
def bstack1llll111lll_opy_(log):
    if not (log[bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⥇")] and log[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⥈")].strip()):
        return
    active = bstack1llll1ll1l1_opy_()
    log = {
        bstack11ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⥉"): log[bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⥊")],
        bstack11ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⥋"): bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠩ࡝ࠫ⥌"),
        bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⥍"): log[bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⥎")],
    }
    if active:
        if active[bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⥏")] == bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⥐"):
            log[bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⥑")] = active[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⥒")]
        elif active[bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⥓")] == bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࠨ⥔"):
            log[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⥕")] = active[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⥖")]
    TestHubHandler.bstack111ll1lll1_opy_([log])
def bstack1llll1ll1l1_opy_():
    if len(store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⥗")]) > 0 and store[bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⥘")][-1]:
        return {
            bstack11ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⥙"): bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⥚"),
            bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⥛"): store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⥜")][-1]
        }
    if store.get(bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⥝"), None):
        return {
            bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⥞"): bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࠬ⥟"),
            bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⥠"): store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⥡")]
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
        item._1ll111l11111_opy_ = True
        bstack111111111l_opy_ = a11y.is_enabled_testcase(bstack1llll11l1111_opy_(item.own_markers))
        if not cli.bstack111l1l1ll1_opy_(bstack1ll1llll11_opy_):
            item._a11y_test_case = bstack111111111l_opy_
            if bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⥢"), None):
                driver = getattr(item, bstack11ll11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⥣"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack111111111l_opy_)
        if not TestHubHandler.on() or bstack1ll111l1111l_opy_ != bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⥤"):
            return
        global current_test_uuid #, bstack1llll1ll111_opy_
        bstack1lll11lllll_opy_ = {
            bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⥥"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⥦"): bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠨ࡜ࠪ⥧")
        }
        current_test_uuid = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⥨")]
        store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⥩")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⥪")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lll11l1l11_opy_[item.nodeid] = {**_1lll11l1l11_opy_[item.nodeid], **bstack1lll11lllll_opy_}
        bstack1ll111l11lll_opy_(item, _1lll11l1l11_opy_[item.nodeid], bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⥫"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨ⥬"), str(err))
def pytest_runtest_setup(item):
    store[bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⥭")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⥮"))
    if bstack1ll11l11l1_opy_.bstack1lll1111ll1l_opy_():
            bstack1ll1111l1l11_opy_ = bstack11ll11_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡤࡷࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨ⥯")
            logger.error(bstack1ll1111l1l11_opy_)
            bstack1lll11lllll_opy_ = {
                bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⥰"): uuid4().__str__(),
                bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⥱"): bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧ⥲"),
                bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⥳"): bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"࡛ࠧࠩ⥴"),
                bstack11ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⥵"): bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⥶"),
                bstack11ll11_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ⥷"): bstack1ll1111l1l11_opy_,
                bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⥸"): [],
                bstack11ll11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⥹"): []
            }
            bstack1ll111l11lll_opy_(item, bstack1lll11lllll_opy_, bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⥺"))
            pytest.skip(bstack1ll1111l1l11_opy_)
            return # skip all existing operations
    global bstack1ll1111l11ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1llll1lll111_opy_():
        atexit.register(bstack111l1l1l1l_opy_)
        if not bstack1ll1111l11ll_opy_:
            try:
                bstack1ll1111lll11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1llll1lll11l_opy_():
                    bstack1ll1111lll11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1111lll11_opy_:
                    signal.signal(s, bstack1ll1l11llll_opy_)
                bstack1ll1111l11ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣ⥻") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1l11l1l1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⥼")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lll11lllll_opy_ = {
            bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⥽"): uuid,
            bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⥾"): bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠫ࡟࠭⥿"),
            bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⦀"): bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⦁"),
            bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⦂"): bstack11ll11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⦃"),
            bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⦄"): bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⦅")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⦆")] = item
        store[bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⦇")] = [uuid]
        if not _1lll11l1l11_opy_.get(item.nodeid, None):
            _1lll11l1l11_opy_[item.nodeid] = {bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⦈"): [], bstack11ll11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⦉"): []}
        _1lll11l1l11_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⦊")].append(bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⦋")])
        _1lll11l1l11_opy_[item.nodeid + bstack11ll11_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪ⦌")] = bstack1lll11lllll_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll111l1ll11_opy_(item, bstack1lll11lllll_opy_, bstack11ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⦍"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ⦎"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack11ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⦏"))
        return # skip all existing operations
    try:
        global bstack111l1111_opy_
        bstack1l11l11ll_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l11l11ll_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⦐")))
        if bstack111111l111_opy_.bstack11llllll_opy_() == bstack11ll11_opy_ (u"ࠣࡶࡵࡹࡪࠨ⦑"):
            if bstack111111l111_opy_.bstack11l11l1l1_opy_() == bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ⦒"):
                bstack1ll1111l1lll_opy_ = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⦓"), None)
                bstack1llll111l1_opy_ = bstack1ll1111l1lll_opy_ + bstack11ll11_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⦔")
                driver = getattr(item, bstack11ll11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⦕"), None)
                bstack111llll111_opy_ = getattr(item, bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⦖"), None)
                bstack1llll11ll1_opy_ = getattr(item, bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⦗"), None)
                PercySDK.screenshot(driver, bstack1llll111l1_opy_, bstack111llll111_opy_=bstack111llll111_opy_, bstack1llll11ll1_opy_=bstack1llll11ll1_opy_, bstack11ll1l1lll_opy_=bstack1l11l11ll_opy_)
        if not cli.bstack111l1l1ll1_opy_(bstack1ll1llll11_opy_):
            if getattr(item, bstack11ll11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⦘"), False):
                bstack11l1l11ll1_opy_.bstack1l1111l111_opy_(getattr(item, bstack11ll11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⦙"), None), bstack111l1111_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lll11lllll_opy_ = {
            bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⦚"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⦛"): bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧ⦜"),
            bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⦝"): bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⦞"),
            bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⦟"): bstack11ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⦠"),
            bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⦡"): bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⦢")
        }
        _1lll11l1l11_opy_[item.nodeid + bstack11ll11_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⦣")] = bstack1lll11lllll_opy_
        bstack1ll111l1ll11_opy_(item, bstack1lll11lllll_opy_, bstack11ll11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⦤"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭⦥"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1ll1l11l1ll1_opy_(fixturedef.argname):
        store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ⦦")] = request.node
    elif bstack1ll1l11ll111_opy_(fixturedef.argname):
        store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⦧")] = request.node
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
            bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⦨"): fixturedef.argname,
            bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⦩"): bstack1lllll1l1l1l_opy_(outcome),
            bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⦪"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⦫")]
        if not _1lll11l1l11_opy_.get(current_test_item.nodeid, None):
            _1lll11l1l11_opy_[current_test_item.nodeid] = {bstack11ll11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⦬"): []}
        _1lll11l1l11_opy_[current_test_item.nodeid][bstack11ll11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⦭")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ⦮"), str(err))
if bstack1lll1l111_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1lll11l1l11_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⦯")].bstack11lll1l1_opy_(id(step))
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩ⦰"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1lll11l1l11_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⦱")].bstack1llll1ll11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ⦲"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            bstack1llll11llll_opy_: bstack1llll1l1l1l_opy_ = _1lll11l1l11_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⦳")]
            bstack1llll11llll_opy_.bstack1llll1ll11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⦴"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111l1111l_opy_
        try:
            if not TestHubHandler.on() or bstack1ll111l1111l_opy_ != bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⦵"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ⦶"), None)
            if not _1lll11l1l11_opy_.get(request.node.nodeid, None):
                _1lll11l1l11_opy_[request.node.nodeid] = {}
            bstack1llll11llll_opy_ = bstack1llll1l1l1l_opy_.bstack1ll11ll1l1l1_opy_(
                scenario, feature, request.node,
                name=bstack1ll1l11lll1l_opy_(request.node, scenario),
                started_at=bstack1l1l111l1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭⦷"),
                tags=bstack1ll1l11lllll_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llll11ll11_opy_(driver) if driver and driver.session_id else {}
            )
            _1lll11l1l11_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⦸")] = bstack1llll11llll_opy_
            bstack1ll111l111l1_opy_(bstack1llll11llll_opy_.uuid)
            TestHubHandler.bstack1llll1l1111_opy_(bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⦹"), bstack1llll11llll_opy_)
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ⦺"), str(err))
def bstack1ll1111ll11l_opy_(bstack1llll1111ll_opy_):
    if bstack1llll1111ll_opy_ in store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⦻")]:
        store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⦼")].remove(bstack1llll1111ll_opy_)
def bstack1ll111l111l1_opy_(test_uuid):
    store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⦽")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll11l111lll_opy_
def bstack1ll1111ll111_opy_(item, call, report):
    logger.debug(bstack11ll11_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡶࡹ࠭⦾"))
    global bstack1ll111l1111l_opy_
    bstack1ll1lll1l1_opy_ = bstack1l1l111l1l_opy_()
    if hasattr(report, bstack11ll11_opy_ (u"ࠬࡹࡴࡰࡲࠪ⦿")):
        bstack1ll1lll1l1_opy_ = bstack1lllllll1l1l_opy_(report.stop)
    elif hasattr(report, bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ⧀")):
        bstack1ll1lll1l1_opy_ = bstack1lllllll1l1l_opy_(report.start)
    try:
        if getattr(report, bstack11ll11_opy_ (u"ࠧࡸࡪࡨࡲࠬ⧁"), bstack11ll11_opy_ (u"ࠨࠩ⧂")) == bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࠧ⧃"):
            logger.debug(bstack11ll11_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⧄").format(getattr(report, bstack11ll11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⧅"), bstack11ll11_opy_ (u"ࠬ࠭⧆")).__str__(), bstack1ll111l1111l_opy_))
            if bstack1ll111l1111l_opy_ == bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⧇"):
                _1lll11l1l11_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⧈")] = bstack1ll1lll1l1_opy_
                bstack1ll111l11lll_opy_(item, _1lll11l1l11_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⧉"), report, call)
                store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⧊")] = None
            elif bstack1ll111l1111l_opy_ == bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ⧋"):
                bstack1llll11llll_opy_ = _1lll11l1l11_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⧌")]
                bstack1llll11llll_opy_.set(hooks=_1lll11l1l11_opy_[item.nodeid].get(bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⧍"), []))
                exception, bstack1llll11ll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llll11ll1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll11_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬ⧎"), bstack11ll11_opy_ (u"ࠧࠨ⧏"))]
                bstack1llll11llll_opy_.stop(time=bstack1ll1lll1l1_opy_, result=Result(result=getattr(report, bstack11ll11_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⧐"), bstack11ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⧑")), exception=exception, bstack1llll11ll1l_opy_=bstack1llll11ll1l_opy_))
                TestHubHandler.bstack1llll1l1111_opy_(bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⧒"), _1lll11l1l11_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⧓")])
        elif getattr(report, bstack11ll11_opy_ (u"ࠬࡽࡨࡦࡰࠪ⧔"), bstack11ll11_opy_ (u"࠭ࠧ⧕")) in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⧖"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⧗")]:
            logger.debug(bstack11ll11_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ⧘").format(getattr(report, bstack11ll11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⧙"), bstack11ll11_opy_ (u"ࠫࠬ⧚")).__str__(), bstack1ll111l1111l_opy_))
            bstack1llll1l1ll1_opy_ = item.nodeid + bstack11ll11_opy_ (u"ࠬ࠳ࠧ⧛") + getattr(report, bstack11ll11_opy_ (u"࠭ࡷࡩࡧࡱࠫ⧜"), bstack11ll11_opy_ (u"ࠧࠨ⧝"))
            if getattr(report, bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⧞"), False):
                hook_type = bstack11ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⧟") if getattr(report, bstack11ll11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⧠"), bstack11ll11_opy_ (u"ࠫࠬ⧡")) == bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⧢") else bstack11ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⧣")
                _1lll11l1l11_opy_[bstack1llll1l1ll1_opy_] = {
                    bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⧤"): uuid4().__str__(),
                    bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⧥"): bstack1ll1lll1l1_opy_,
                    bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⧦"): hook_type
                }
            _1lll11l1l11_opy_[bstack1llll1l1ll1_opy_][bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⧧")] = bstack1ll1lll1l1_opy_
            bstack1ll1111ll11l_opy_(_1lll11l1l11_opy_[bstack1llll1l1ll1_opy_][bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⧨")])
            bstack1ll111l1ll11_opy_(item, _1lll11l1l11_opy_[bstack1llll1l1ll1_opy_], bstack11ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⧩"), report, call)
            if getattr(report, bstack11ll11_opy_ (u"࠭ࡷࡩࡧࡱࠫ⧪"), bstack11ll11_opy_ (u"ࠧࠨ⧫")) == bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⧬"):
                if getattr(report, bstack11ll11_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⧭"), bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⧮")) == bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⧯"):
                    bstack1lll11lllll_opy_ = {
                        bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⧰"): uuid4().__str__(),
                        bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⧱"): bstack1l1l111l1l_opy_(),
                        bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⧲"): bstack1l1l111l1l_opy_()
                    }
                    _1lll11l1l11_opy_[item.nodeid] = {**_1lll11l1l11_opy_[item.nodeid], **bstack1lll11lllll_opy_}
                    bstack1ll111l11lll_opy_(item, _1lll11l1l11_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⧳"))
                    bstack1ll111l11lll_opy_(item, _1lll11l1l11_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⧴"), report, call)
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨ⧵"), str(err))
def bstack1ll1111l1111_opy_(test, bstack1lll11lllll_opy_, result=None, call=None, bstack1l11l1l1ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1llll11llll_opy_ = {
        bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⧶"): bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⧷")],
        bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⧸"): bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࠬ⧹"),
        bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⧺"): test.name,
        bstack11ll11_opy_ (u"ࠩࡥࡳࡩࡿࠧ⧻"): {
            bstack11ll11_opy_ (u"ࠪࡰࡦࡴࡧࠨ⧼"): bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⧽"),
            bstack11ll11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⧾"): inspect.getsource(test.obj)
        },
        bstack11ll11_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⧿"): test.name,
        bstack11ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⨀"): test.name,
        bstack11ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⨁"): bstack1lllll1l11_opy_.bstack1lll1l1llll_opy_(test),
        bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⨂"): file_path,
        bstack11ll11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⨃"): file_path,
        bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⨄"): bstack11ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⨅"),
        bstack11ll11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⨆"): file_path,
        bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⨇"): bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⨈")],
        bstack11ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⨉"): bstack11ll11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⨊"),
        bstack11ll11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ⨋"): {
            bstack11ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ⨌"): test.nodeid
        },
        bstack11ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫ⨍"): bstack1llll11l1111_opy_(test.own_markers)
    }
    if bstack1l11l1l1ll_opy_ in [bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⨎"), bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⨏")]:
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠩࡰࡩࡹࡧࠧ⨐")] = {
            bstack11ll11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⨑"): bstack1lll11lllll_opy_.get(bstack11ll11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⨒"), [])
        }
    if bstack1l11l1l1ll_opy_ == bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⨓"):
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⨔")] = bstack11ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⨕")
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⨖")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⨗")]
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⨘")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⨙")]
    if result:
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⨚")] = result.outcome
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⨛")] = result.duration * 1000
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⨜")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⨝")]
        if result.failed:
            bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⨞")] = TestHubHandler.bstack1ll111ll11l_opy_(call.excinfo.typename)
            bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⨟")] = TestHubHandler.bstack1ll11l1111l1_opy_(call.excinfo, result)
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⨠")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⨡")]
    if outcome:
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⨢")] = bstack1lllll1l1l1l_opy_(outcome)
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⨣")] = 0
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⨤")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⨥")]
        if bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⨦")] == bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⨧"):
            bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⨨")] = bstack11ll11_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⨩")  # bstack1ll1111l111l_opy_
            bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⨪")] = [{bstack11ll11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⨫"): [bstack11ll11_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⨬")]}]
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⨭")] = bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⨮")]
    return bstack1llll11llll_opy_
def bstack1ll111l11l11_opy_(test, bstack1lll11ll1l1_opy_, bstack1l11l1l1ll_opy_, result, call, outcome, bstack1ll1111l1l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⨯")]
    hook_name = bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⨰")]
    hook_data = {
        bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⨱"): bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⨲")],
        bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⨳"): bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⨴"),
        bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⨵"): bstack11ll11_opy_ (u"ࠬࢁࡽࠨ⨶").format(bstack1ll1l11ll11l_opy_(hook_name)),
        bstack11ll11_opy_ (u"࠭ࡢࡰࡦࡼࠫ⨷"): {
            bstack11ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⨸"): bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⨹"),
            bstack11ll11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⨺"): None
        },
        bstack11ll11_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⨻"): test.name,
        bstack11ll11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⨼"): bstack1lllll1l11_opy_.bstack1lll1l1llll_opy_(test, hook_name),
        bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⨽"): file_path,
        bstack11ll11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⨾"): file_path,
        bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⨿"): bstack11ll11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⩀"),
        bstack11ll11_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⩁"): file_path,
        bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⩂"): bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⩃")],
        bstack11ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⩄"): bstack11ll11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ⩅") if bstack1ll111l1111l_opy_ == bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⩆") else bstack11ll11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⩇"),
        bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⩈"): hook_type
    }
    bstack1l111l11ll1_opy_ = bstack1lll1l1l11l_opy_(_1lll11l1l11_opy_.get(test.nodeid, None))
    if bstack1l111l11ll1_opy_:
        hook_data[bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ⩉")] = bstack1l111l11ll1_opy_
    if result:
        hook_data[bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⩊")] = result.outcome
        hook_data[bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⩋")] = result.duration * 1000
        hook_data[bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⩌")] = bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⩍")]
        if result.failed:
            hook_data[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⩎")] = TestHubHandler.bstack1ll111ll11l_opy_(call.excinfo.typename)
            hook_data[bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⩏")] = TestHubHandler.bstack1ll11l1111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⩐")] = bstack1lllll1l1l1l_opy_(outcome)
        hook_data[bstack11ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⩑")] = 100
        hook_data[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⩒")] = bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⩓")]
        if hook_data[bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩔")] == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⩕"):
            hook_data[bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⩖")] = bstack11ll11_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ⩗")  # bstack1ll1111l111l_opy_
            hook_data[bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⩘")] = [{bstack11ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⩙"): [bstack11ll11_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ⩚")]}]
    if bstack1ll1111l1l1l_opy_:
        hook_data[bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩛")] = bstack1ll1111l1l1l_opy_.result
        hook_data[bstack11ll11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⩜")] = bstack1ll1l1llll1_opy_(bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⩝")], bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩞")])
        hook_data[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⩟")] = bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⩠")]
        if hook_data[bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⩡")] == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⩢"):
            hook_data[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⩣")] = TestHubHandler.bstack1ll111ll11l_opy_(bstack1ll1111l1l1l_opy_.exception_type)
            hook_data[bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⩤")] = [{bstack11ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⩥"): bstack1llllll11l1l_opy_(bstack1ll1111l1l1l_opy_.exception)}]
    return hook_data
def bstack1ll111l11lll_opy_(test, bstack1lll11lllll_opy_, bstack1l11l1l1ll_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11ll11_opy_ (u"ࠫࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⩦").format(bstack1l11l1l1ll_opy_))
    bstack1llll11llll_opy_ = bstack1ll1111l1111_opy_(test, bstack1lll11lllll_opy_, result, call, bstack1l11l1l1ll_opy_, outcome)
    driver = getattr(test, bstack11ll11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⩧"), None)
    if bstack1l11l1l1ll_opy_ == bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⩨") and driver:
        bstack1llll11llll_opy_[bstack11ll11_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭⩩")] = TestHubHandler.bstack1llll11ll11_opy_(driver)
    if bstack1l11l1l1ll_opy_ == bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⩪"):
        bstack1l11l1l1ll_opy_ = bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⩫")
    bstack1lll1ll1lll_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⩬"): bstack1l11l1l1ll_opy_,
        bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⩭"): bstack1llll11llll_opy_
    }
    TestHubHandler.bstack1l1l1l1ll_opy_(bstack1lll1ll1lll_opy_)
    if bstack1l11l1l1ll_opy_ == bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⩮"):
        threading.current_thread().bstackTestMeta = {bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⩯"): bstack11ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⩰")}
    elif bstack1l11l1l1ll_opy_ == bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⩱"):
        threading.current_thread().bstackTestMeta = {bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⩲"): getattr(result, bstack11ll11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⩳"), bstack11ll11_opy_ (u"ࠫࠬ⩴"))}
def bstack1ll111l1ll11_opy_(test, bstack1lll11lllll_opy_, bstack1l11l1l1ll_opy_, result=None, call=None, outcome=None, bstack1ll1111l1l1l_opy_=None):
    logger.debug(bstack11ll11_opy_ (u"ࠬࡹࡥ࡯ࡦࡢ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡩࡱࡲ࡯ࠥࡪࡡࡵࡣ࠯ࠤࡪࡼࡥ࡯ࡶࡗࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ⩵").format(bstack1l11l1l1ll_opy_))
    hook_data = bstack1ll111l11l11_opy_(test, bstack1lll11lllll_opy_, bstack1l11l1l1ll_opy_, result, call, outcome, bstack1ll1111l1l1l_opy_)
    bstack1lll1ll1lll_opy_ = {
        bstack11ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⩶"): bstack1l11l1l1ll_opy_,
        bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ⩷"): hook_data
    }
    TestHubHandler.bstack1l1l1l1ll_opy_(bstack1lll1ll1lll_opy_)
def bstack1lll1l1l11l_opy_(bstack1lll11lllll_opy_):
    if not bstack1lll11lllll_opy_:
        return None
    if bstack1lll11lllll_opy_.get(bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⩸"), None):
        return getattr(bstack1lll11lllll_opy_[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⩹")], bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⩺"), None)
    return bstack1lll11lllll_opy_.get(bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⩻"), None)
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
        places = [bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⩼"), bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⩽"), bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⩾")]
        logs = []
        for bstack1ll1111ll1ll_opy_ in places:
            records = caplog.get_records(bstack1ll1111ll1ll_opy_)
            bstack1ll1111lllll_opy_ = bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⩿") if bstack1ll1111ll1ll_opy_ == bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࠧ⪀") else bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⪁")
            bstack1ll111l1l111_opy_ = request.node.nodeid + (bstack11ll11_opy_ (u"ࠫࠬ⪂") if bstack1ll1111ll1ll_opy_ == bstack11ll11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⪃") else bstack11ll11_opy_ (u"࠭࠭ࠨ⪄") + bstack1ll1111ll1ll_opy_)
            test_uuid = bstack1lll1l1l11l_opy_(_1lll11l1l11_opy_.get(bstack1ll111l1l111_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1lllll1llll1_opy_(record.message):
                    continue
                logs.append({
                    bstack11ll11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⪅"): bstack1llll1lllll1_opy_(record.created).isoformat() + bstack11ll11_opy_ (u"ࠨ࡜ࠪ⪆"),
                    bstack11ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⪇"): record.levelname,
                    bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⪈"): record.message,
                    bstack1ll1111lllll_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack111ll1lll1_opy_(logs)
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ⪉"), str(err))
def bstack1ll11l1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack111l1ll111_opy_
    bstack1l11l111ll_opy_ = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ⪊"), None) and bstack11ll1l11l_opy_(
            threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⪋"), None)
    bstack11ll11l1l_opy_ = getattr(driver, bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⪌"), None) != None and getattr(driver, bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⪍"), None) == True
    if sequence == bstack11ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⪎") and driver != None:
      if not bstack111l1ll111_opy_ and bstack1l1ll1ll1l_opy_() and bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⪏") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⪐")] == True and accessibility_scripts.bstack1l1l1lll_opy_(driver_command) and (bstack11ll11l1l_opy_ or bstack1l11l111ll_opy_) and not bstack111lllllll_opy_(args):
        try:
          bstack111l1ll111_opy_ = True
          logger.debug(bstack11ll11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ⪑").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ⪒").format(str(err)))
        bstack111l1ll111_opy_ = False
    if sequence == bstack11ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⪓"):
        if driver_command == bstack11ll11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ⪔"):
            TestHubHandler.bstack11l111ll1_opy_({
                bstack11ll11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ⪕"): response[bstack11ll11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ⪖")],
                bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⪗"): store[bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⪘")]
            })
def bstack111l1l1l1l_opy_():
    global bstack1ll11llll_opy_
    logger_utils.bstack1l1lll111_opy_()
    logging.shutdown()
    TestHubHandler.bstack1lll11l1l1l_opy_()
    for driver in bstack1ll11llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l11llll_opy_(*args):
    global bstack1ll11llll_opy_
    TestHubHandler.bstack1lll11l1l1l_opy_()
    for driver in bstack1ll11llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111l111_opy_, stage=STAGE.bstack1111l1111l_opy_, bstack1l111l1111_opy_=SESSION_NAME)
def bstack1111ll11l1_opy_(self, *args, **kwargs):
    bstack111111l1ll_opy_ = bstack1l1ll111l_opy_(self, *args, **kwargs)
    bstack111ll1ll11_opy_ = getattr(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⪙"), None)
    if bstack111ll1ll11_opy_ and bstack111ll1ll11_opy_.get(bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⪚"), bstack11ll11_opy_ (u"ࠨࠩ⪛")) == bstack11ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⪜"):
        TestHubHandler.send_cbt_info(self)
    return bstack111111l1ll_opy_
@measure(event_name=EVENTS.bstack11lll1l1l1_opy_, stage=STAGE.bstack1ll1ll1ll1_opy_, bstack1l111l1111_opy_=SESSION_NAME)
def bstack1111l1ll11_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.bstack111llll11_opy_()
    if global_config.get_property(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⪝")):
        return
    global_config.bstack1111lll11_opy_(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⪞"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack1llll1l1_opy_.format(FRAMEWORK_NAME.split(bstack11ll11_opy_ (u"ࠬ࠳ࠧ⪟"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll1ll1l_opy_():
            Service.start = bstack11lllll11_opy_
            Service.stop = bstack111l1lllll_opy_
            webdriver.Remote.get = bstack1lllll111l_opy_
            webdriver.Remote.__init__ = bstack1llll1l1ll_opy_
            if not isinstance(os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ⪠")), str):
                return
            WebDriver.quit = bstack11ll1l1ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1111ll11l1_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack11ll11_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ⪡")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack11ll11_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭⪢")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack11l111l1l_opy_(bstack11ll11_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ⪣"), bstack1l1ll11l_opy_)
    if bstack1l11l1ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⪤")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⪥"))):
                RemoteConnection._get_proxy_url = bstack1ll11ll111_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1ll11ll111_opy_
        except Exception as e:
            logger.error(bstack111ll11ll_opy_.format(str(e)))
    if bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⪦") in str(framework_name).lower():
        if not bstack1l1ll1ll1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l11lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111111ll1l_opy_
            Config.getoption = bstack11ll11l111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l11ll11l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1lll1l1_opy_, stage=STAGE.bstack1111l1111l_opy_, bstack1l111l1111_opy_=SESSION_NAME)
def bstack11ll1l1ll_opy_(self):
    global FRAMEWORK_NAME
    global bstack1l1l1llll_opy_
    global bstack1l11111ll_opy_
    try:
        if bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⪧") in FRAMEWORK_NAME and self.session_id != None and bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ⪨"), bstack11ll11_opy_ (u"ࠨࠩ⪩")) != bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⪪"):
            bstack111l1l11ll_opy_ = bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⪫") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⪬")
            bstack1111ll1l11_opy_(logger, True)
            if os.environ.get(bstack11ll11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⪭"), None):
                self.execute_script(
                    bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ⪮") + json.dumps(
                        os.environ.get(bstack11ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⪯"))) + bstack11ll11_opy_ (u"ࠨࡿࢀࠫ⪰"))
            if self != None:
                bstack111ll1l1_opy_(self, bstack111l1l11ll_opy_, bstack11ll11_opy_ (u"ࠩ࠯ࠤࠬ⪱").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack111l1l1ll1_opy_(bstack1ll1llll11_opy_):
            item = store.get(bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⪲"), None)
            if item is not None and bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⪳"), None):
                bstack11l1l11ll1_opy_.bstack1l1111l111_opy_(self, bstack111l1111_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll11_opy_ (u"ࠬ࠭⪴")
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢ⪵") + str(e))
    bstack1l11111ll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1111ll11_opy_, stage=STAGE.bstack1111l1111l_opy_, bstack1l111l1111_opy_=SESSION_NAME)
def bstack1llll1l1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1l1llll_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1l1ll111l_opy_
    global bstack1ll11llll_opy_
    global bstack11l1ll11l1_opy_
    global bstack111lllll1_opy_
    global bstack111l1111_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⪶")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack111ll11l11_opy_(bstack11l1ll11l1_opy_, CONFIG)
    logger.debug(bstack11lll1l1ll_opy_.format(command_executor))
    proxy = bstack11lll11ll_opy_(CONFIG, proxy)
    bstack1l11l11ll_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l11l11ll_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⪷")))
    except:
        bstack1l11l11ll_opy_ = 0
    bstack111l1ll11_opy_ = get_caps(CONFIG, bstack1l11l11ll_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack111l1ll11_opy_)))
    bstack111l1111_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⪸"))[bstack1l11l11ll_opy_]
    if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⪹") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⪺")]:
        update_caps_for_local(bstack111l1ll11_opy_, bstack111lllll1_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack1l11l11ll_opy_) and a11y.is_platform_supported(bstack111l1ll11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack111l1l1ll1_opy_(bstack1ll1llll11_opy_):
            a11y.set_capabilities(bstack111l1ll11_opy_, CONFIG)
    if desired_capabilities:
        bstack11l1ll1lll_opy_ = bstack1lll1ll1l_opy_(desired_capabilities)
        bstack11l1ll1lll_opy_[bstack11ll11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ⪻")] = bstack1l111l111l_opy_(CONFIG)
        bstack1lll1lll11_opy_ = get_caps(bstack11l1ll1lll_opy_)
        if bstack1lll1lll11_opy_:
            bstack111l1ll11_opy_ = update(bstack1lll1lll11_opy_, bstack111l1ll11_opy_)
        desired_capabilities = None
    if options:
        bstack111lll11l1_opy_(options, bstack111l1ll11_opy_)
    if not options:
        options = bstack1llllll1111_opy_(bstack111l1ll11_opy_)
    if proxy and bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⪼")):
        options.proxy(proxy)
    if options and bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⪽")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1l11l1_opy_() < version.parse(bstack11ll11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⪾")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack111l1ll11_opy_)
    logger.info(bstack11l111l11_opy_)
    bstack1l11l1l11_opy_.end(EVENTS.bstack11lll1l1l1_opy_.value, EVENTS.bstack11lll1l1l1_opy_.value + bstack11ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⪿"),
                               EVENTS.bstack11lll1l1l1_opy_.value + bstack11ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⫀"), True, None)
    try:
        if bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⫁")):
            bstack1l1ll111l_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⫂")):
            bstack1l1ll111l_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭⫃")):
            bstack1l1ll111l_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l1ll111l_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1ll1l1ll1_opy_:
        logger.error(bstack1ll11lll11_opy_.format(bstack11ll11_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰ࠭⫄"), str(bstack1ll1l1ll1_opy_)))
        raise bstack1ll1l1ll1_opy_
    try:
        bstack1ll11l1lll_opy_ = bstack11ll11_opy_ (u"ࠨࠩ⫅")
        if bstack1lll1l11l1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ⫆")):
            bstack1ll11l1lll_opy_ = self.caps.get(bstack11ll11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⫇"))
        else:
            bstack1ll11l1lll_opy_ = self.capabilities.get(bstack11ll11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⫈"))
        if bstack1ll11l1lll_opy_:
            bstack11ll111l_opy_(bstack1ll11l1lll_opy_)
            if bstack1lll1l11l1_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ⫉")):
                self.command_executor._url = bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⫊") + bstack11l1ll11l1_opy_ + bstack11ll11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ⫋")
            else:
                self.command_executor._url = bstack11ll11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ⫌") + bstack1ll11l1lll_opy_ + bstack11ll11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ⫍")
            logger.debug(bstack11l11ll1l1_opy_.format(bstack1ll11l1lll_opy_))
        else:
            logger.debug(bstack1llll11111_opy_.format(bstack11ll11_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦ⫎")))
    except Exception as e:
        logger.debug(bstack1llll11111_opy_.format(e))
    bstack1l1l1llll_opy_ = self.session_id
    if bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⫏") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⫐"), None)
        if item:
            bstack1ll111l11l1l_opy_ = getattr(item, bstack11ll11_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫ⫑"), False)
            if not getattr(item, bstack11ll11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⫒"), None) and bstack1ll111l11l1l_opy_:
                setattr(store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⫓")], bstack11ll11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⫔"), self)
        bstack111ll1ll11_opy_ = getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⫕"), None)
        if bstack111ll1ll11_opy_ and bstack111ll1ll11_opy_.get(bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⫖"), bstack11ll11_opy_ (u"ࠬ࠭⫗")) == bstack11ll11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⫘"):
            TestHubHandler.send_cbt_info(self)
    bstack1ll11llll_opy_.append(self)
    if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⫙") in CONFIG and bstack11ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⫚") in CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⫛")][bstack1l11l11ll_opy_]:
        SESSION_NAME = CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⫝̸")][bstack1l11l11ll_opy_][bstack11ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⫝")]
    logger.debug(bstack11111ll1l1_opy_.format(bstack1l1l1llll_opy_))
@measure(event_name=EVENTS.bstack1lll11ll1l_opy_, stage=STAGE.bstack1111l1111l_opy_, bstack1l111l1111_opy_=SESSION_NAME)
def bstack1lllll111l_opy_(self, url):
    global bstack1ll1111111_opy_
    global CONFIG
    try:
        bstack111l1llll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111l1l111_opy_.format(str(err)))
    try:
        bstack1ll1111111_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack1lll1111l1_opy_):
                bstack111l1llll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111l1l111_opy_.format(str(err)))
        raise e
def bstack11lll11l1l_opy_(item, when):
    global bstack1lllllll1ll_opy_
    try:
        bstack1lllllll1ll_opy_(item, when)
    except Exception as e:
        pass
def bstack11l11ll11l_opy_(item, call, rep):
    global bstack11lll1111_opy_
    global bstack1ll11llll_opy_
    name = bstack11ll11_opy_ (u"ࠬ࠭⫞")
    try:
        if rep.when == bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⫟"):
            bstack1l1l1llll_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⫠"))
            try:
                if (str(skipSessionName).lower() != bstack11ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭⫡")):
                    name = str(rep.nodeid)
                    bstack1111l11lll_opy_ = bstack1l1l1l11l_opy_(bstack11ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⫢"), name, bstack11ll11_opy_ (u"ࠪࠫ⫣"), bstack11ll11_opy_ (u"ࠫࠬ⫤"), bstack11ll11_opy_ (u"ࠬ࠭⫥"), bstack11ll11_opy_ (u"࠭ࠧ⫦"))
                    os.environ[bstack11ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⫧")] = name
                    for driver in bstack1ll11llll_opy_:
                        if bstack1l1l1llll_opy_ == driver.session_id:
                            driver.execute_script(bstack1111l11lll_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ⫨").format(str(e)))
            try:
                bstack1l1l11ll11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⫩"):
                    status = bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⫪") if rep.outcome.lower() == bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⫫") else bstack11ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⫬")
                    reason = bstack11ll11_opy_ (u"࠭ࠧ⫭")
                    if status == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⫮"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭⫯") if status == bstack11ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⫰") else bstack11ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⫱")
                    data = name + bstack11ll11_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭⫲") if status == bstack11ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⫳") else name + bstack11ll11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ⫴") + reason
                    bstack1llllll1l1_opy_ = bstack1l1l1l11l_opy_(bstack11ll11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ⫵"), bstack11ll11_opy_ (u"ࠨࠩ⫶"), bstack11ll11_opy_ (u"ࠩࠪ⫷"), bstack11ll11_opy_ (u"ࠪࠫ⫸"), level, data)
                    for driver in bstack1ll11llll_opy_:
                        if bstack1l1l1llll_opy_ == driver.session_id:
                            driver.execute_script(bstack1llllll1l1_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ⫹").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ⫺").format(str(e)))
    bstack11lll1111_opy_(item, call, rep)
notset = Notset()
def bstack11ll11l111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1l11l1l_opy_
    if str(name).lower() == bstack11ll11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭⫻"):
        return bstack11ll11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ⫼")
    else:
        return bstack1l1l11l1l_opy_(self, name, default, skip)
def bstack1ll11ll111_opy_(self):
    global CONFIG
    global bstack1l1111l11_opy_
    try:
        proxy = bstack1ll111lll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭⫽")):
                proxies = bstack1ll11ll11_opy_(proxy, bstack111ll11l11_opy_())
                if len(proxies) > 0:
                    protocol, bstack11l1ll11_opy_ = proxies.popitem()
                    if bstack11ll11_opy_ (u"ࠤ࠽࠳࠴ࠨ⫾") in bstack11l1ll11_opy_:
                        return bstack11l1ll11_opy_
                    else:
                        return bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⫿") + bstack11l1ll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣ⬀").format(str(e)))
    return bstack1l1111l11_opy_(self)
def bstack1l11l1ll_opy_():
    return (bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ⬁") in CONFIG or bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⬂") in CONFIG) and bstack1l11ll1111_opy_() and bstack1lll1l11l1_opy_() >= version.parse(
        bstack1l11l1l111_opy_)
def bstack1l11ll111_opy_(self,
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
    CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⬃")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1l11l11ll_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l11l11ll_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⬄")))
    except:
        bstack1l11l11ll_opy_ = 0
    CONFIG[bstack11ll11_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ⬅")] = True
    bstack111l1ll11_opy_ = get_caps(CONFIG, bstack1l11l11ll_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack111l1ll11_opy_)))
    if CONFIG.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⬆")):
        update_caps_for_local(bstack111l1ll11_opy_, bstack111lllll1_opy_)
    if bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⬇") in CONFIG and bstack11ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⬈") in CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⬉")][bstack1l11l11ll_opy_]:
        SESSION_NAME = CONFIG[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⬊")][bstack1l11l11ll_opy_][bstack11ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⬋")]
    import urllib
    import json
    if bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⬌") in CONFIG and str(CONFIG[bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⬍")]).lower() != bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ⬎"):
        bstack1111ll1ll1_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1111ll1ll1_opy_ + urllib.parse.quote(json.dumps(bstack111l1ll11_opy_))
    else:
        cdpUrl = bstack11ll11_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ⬏") + urllib.parse.quote(json.dumps(bstack111l1ll11_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11l11lll1_opy_
        if not bstack1l1ll1ll1l_opy_():
            global bstack1ll11111l_opy_
            if not bstack1ll11111l_opy_:
                from bstack_utils.helper import bstack1lll1lllll_opy_, bstack1lllll1l1111_opy_
                bstack1ll11111l_opy_ = bstack1lll1lllll_opy_()
                bstack1lllll1l1111_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l11l11lll1_opy_
            return
        BrowserType.launch = bstack1l11ll111_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll1111l1ll1_opy_():
    global CONFIG
    global bstack1lll11111_opy_
    global bstack11l1ll11l1_opy_
    global bstack111lllll1_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack111lllll1l_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ⬐")))
    bstack1lll11111_opy_ = eval(os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ⬑")))
    bstack11l1ll11l1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ⬒"))
    bstack1l11l11l1_opy_(CONFIG, bstack1lll11111_opy_)
    bstack111lllll1l_opy_ = logger_utils.configure_logger(CONFIG, bstack111lllll1l_opy_)
    if cli.bstack11lllll1l_opy_():
        bstack111ll1l11_opy_.invoke(Events.CONNECT, bstack1l1ll1lll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⬓"), bstack11ll11_opy_ (u"ࠪ࠴ࠬ⬔")))
        cli.bstack1lll1lll1l_opy_(cli_context.platform_index)
        cli.bstack1l11l11l1l1_opy_(bstack111ll11l11_opy_(bstack11l1ll11l1_opy_, CONFIG), cli_context.platform_index, bstack1llllll1111_opy_)
        cli.bstack11lllll1l1_opy_()
        logger.debug(bstack11ll11_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ⬕") + str(cli_context.platform_index) + bstack11ll11_opy_ (u"ࠧࠨ⬖"))
        return # skip all existing operations
    global bstack1l1ll111l_opy_
    global bstack1l11111ll_opy_
    global bstack11l1lll11l_opy_
    global bstack11ll11l11_opy_
    global bstack11llll1l1_opy_
    global bstack11ll1l1l11_opy_
    global bstack1l1ll1l11_opy_
    global bstack1ll1111111_opy_
    global bstack1l1111l11_opy_
    global bstack1l1l11l1l_opy_
    global bstack1lllllll1ll_opy_
    global bstack11lll1111_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1ll111l_opy_ = webdriver.Remote.__init__
        bstack1l11111ll_opy_ = WebDriver.quit
        bstack1l1ll1l11_opy_ = WebDriver.close
        bstack1ll1111111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⬗") in CONFIG or bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⬘") in CONFIG) and bstack1l11ll1111_opy_():
        if bstack1lll1l11l1_opy_() < version.parse(bstack1l11l1l111_opy_):
            logger.error(bstack1l11llll1l_opy_.format(bstack1lll1l11l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⬙")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⬚"))):
                    bstack1l1111l11_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1111l11_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack111ll11ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1l11l1l_opy_ = Config.getoption
        from _pytest import runner
        bstack1lllllll1ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack11ll11_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥ⬛"), bstack1l11l1ll11_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack11lll1111_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ⬜"))
    bstack111lllll1_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⬝"), {}).get(bstack11ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⬞"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack1111l1ll11_opy_(bstack11lllllll1_opy_)
if (bstack1llll1lll111_opy_()):
    bstack1ll1111l1ll1_opy_()
@error_handler(class_method=False)
def bstack1ll111l11ll1_opy_(hook_name, event, bstack111ll1ll1l1_opy_=None):
    if hook_name not in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⬟"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⬠"), bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⬡"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⬢"), bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⬣"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⬤"), bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⬥"), bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⬦")]:
        return
    node = store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⬧")]
    if hook_name in [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⬨"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⬩")]:
        node = store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ⬪")]
    elif hook_name in [bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⬫"), bstack11ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⬬")]:
        node = store[bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ⬭")]
    hook_type = bstack1ll1l11l1lll_opy_(hook_name)
    if event == bstack11ll11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⬮"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lll11ll1l1_opy_ = {
            bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⬯"): uuid,
            bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⬰"): bstack1l1l111l1l_opy_(),
            bstack11ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⬱"): bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⬲"),
            bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⬳"): hook_type,
            bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⬴"): hook_name
        }
        store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⬵")].append(uuid)
        bstack1ll1111ll1l1_opy_ = node.nodeid
        if hook_type == bstack11ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⬶"):
            if not _1lll11l1l11_opy_.get(bstack1ll1111ll1l1_opy_, None):
                _1lll11l1l11_opy_[bstack1ll1111ll1l1_opy_] = {bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⬷"): []}
            _1lll11l1l11_opy_[bstack1ll1111ll1l1_opy_][bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⬸")].append(bstack1lll11ll1l1_opy_[bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⬹")])
        _1lll11l1l11_opy_[bstack1ll1111ll1l1_opy_ + bstack11ll11_opy_ (u"࠭࠭ࠨ⬺") + hook_name] = bstack1lll11ll1l1_opy_
        bstack1ll111l1ll11_opy_(node, bstack1lll11ll1l1_opy_, bstack11ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⬻"))
    elif event == bstack11ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⬼"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack111ll1ll1l1_opy_)
            return
        bstack1llll1l1ll1_opy_ = node.nodeid + bstack11ll11_opy_ (u"ࠩ࠰ࠫ⬽") + hook_name
        _1lll11l1l11_opy_[bstack1llll1l1ll1_opy_][bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⬾")] = bstack1l1l111l1l_opy_()
        bstack1ll1111ll11l_opy_(_1lll11l1l11_opy_[bstack1llll1l1ll1_opy_][bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⬿")])
        bstack1ll111l1ll11_opy_(node, _1lll11l1l11_opy_[bstack1llll1l1ll1_opy_], bstack11ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⭀"), bstack1ll1111l1l1l_opy_=bstack111ll1ll1l1_opy_)
def bstack1ll111l111ll_opy_():
    global bstack1ll111l1111l_opy_
    if bstack1lll1l111_opy_():
        bstack1ll111l1111l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⭁")
    else:
        bstack1ll111l1111l_opy_ = bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⭂")
@TestHubHandler.bstack1ll11l111lll_opy_
def bstack1ll1111l11l1_opy_():
    bstack1ll111l111ll_opy_()
    if cli.is_running():
        try:
            bstack1lll1lll1lll_opy_(bstack1ll111l11ll1_opy_)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⭃").format(e))
        return
    if bstack1l11ll1111_opy_():
        global_config = Config.bstack111llll11_opy_()
        bstack11ll11_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ⭄")
        if global_config.get_property(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⭅")):
            if CONFIG.get(bstack11ll11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ⭆")) is not None and int(CONFIG[bstack11ll11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⭇")]) > 1:
                bstack1111l1111_opy_(bstack1ll11l1l1l_opy_)
            return
        bstack1111l1111_opy_(bstack1ll11l1l1l_opy_)
    try:
        bstack1lll1lll1lll_opy_(bstack1ll111l11ll1_opy_)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⭈").format(e))
bstack1ll1111l11l1_opy_()