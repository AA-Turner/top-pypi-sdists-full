# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1111llll1l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack11ll11l11l_opy_, update, bstack1lll1111_opy_,
                                       bstack1l111l11l_opy_, bstack1l1111ll_opy_, bstack11l1l111_opy_, bstack1ll1ll1l1l_opy_,
                                       bstack1111l111l1_opy_, bstack111l11lll1_opy_, bstack1l111ll1_opy_,
                                       bstack1lllll1l1l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11l111l11_opy_)
from browserstack_sdk.bstack11l1111lll_opy_ import bstack1l111l1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1llll11l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll11l1111_opy_, bstack111lll1l1_opy_, bstack111llll1ll_opy_, \
    bstack111lll1l1l_opy_
from bstack_utils.helper import bstack11l11l1ll_opy_, bstack1llll11ll111_opy_, bstack1lll1l11ll1_opy_, bstack11l111l111_opy_, bstack1l1lllllll_opy_, bstack111ll1ll1l_opy_, \
    bstack1lllllll111l_opy_, \
    bstack1llll1l1l11l_opy_, bstack11lll1ll_opy_, bstack1lll1lll11_opy_, bstack1llllll111l1_opy_, bstack1ll1111ll1_opy_, Notset, \
    bstack111l11l1_opy_, bstack1ll1l1ll111_opy_, bstack1lllll1lll11_opy_, Result, bstack1lllll11lll1_opy_, bstack1llllll1l1ll_opy_, error_handler, \
    bstack1ll1l11ll_opy_, bstack1lllllll11l_opy_, bstack1l111l11l1_opy_, bstack1llll11l111l_opy_
from bstack_utils.bstack1lll1llll111_opy_ import bstack1lll1lll1ll1_opy_
from bstack_utils.messages import bstack1ll11l1l1l_opy_, bstack1l1llllll1_opy_, bstack11l1l11l_opy_, bstack1ll1llll1l_opy_, bstack1llllll1ll1_opy_, \
    bstack1l11l111_opy_, bstack1ll1ll1l1_opy_, CONFIG_FILE_CONTENT, bstack1ll11ll1_opy_, bstack1l1111l1_opy_, \
    bstack11111l1l_opy_, bstack11111l1l1_opy_, bstack1l11l1ll11_opy_
from bstack_utils.proxy import bstack111111lll_opy_, bstack11lll111l1_opy_
from bstack_utils.bstack1lll11ll1l_opy_ import bstack1ll1l1l11l11_opy_, bstack1ll1l11lll1l_opy_, bstack1ll1l11ll111_opy_, bstack1ll1l11lllll_opy_, \
    bstack1ll1l11ll1l1_opy_, bstack1ll1l1l1111l_opy_, bstack1ll1l11ll11l_opy_, bstack1l1l1l1l11_opy_, bstack1ll1l11lll11_opy_
from bstack_utils.bstack1lll111111_opy_ import bstack1l1ll111l1_opy_
from bstack_utils.bstack11l11llll_opy_ import bstack1l11ll111l_opy_, bstack1lll1l111l_opy_, update_caps_for_local, \
    bstack11l11lll1l_opy_, bstack1l1ll1l111_opy_
from bstack_utils.bstack1llll11llll_opy_ import bstack1llll1l111l_opy_
from bstack_utils.bstack111ll111ll_opy_ import bstack11l1l1l1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack111l1llll_opy_ import bstack11l1ll1ll_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack1ll11111l1_opy_ import bstack1llll11l1l_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l_opy_ import bstack111111l1l_opy_, Events, bstack1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll11l111l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111111l1l_opy_ import bstack111111l1l_opy_, Events, bstack1ll1ll1l_opy_
bstack1l1l11l111_opy_ = None
bstack1lll1ll11_opy_ = None
bstack1111111l1l_opy_ = None
bstack11ll1l1lll_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack111lll1111_opy_ = None
bstack11ll11ll1_opy_ = None
bstack11l11l11l_opy_ = None
bstack1111ll111l_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack111llll1l1_opy_ = None
bstack11l11111ll_opy_ = None
bstack1lllll1ll1_opy_ = None
FRAMEWORK_NAME = bstack1ll1l11_opy_ (u"ࠨࠩ⣢")
CONFIG = {}
bstack1l1ll1l11l_opy_ = False
bstack1111ll111_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪ⣣")
bstack111l111l1_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫ⣤")
PARALLELISE_VANILLA_PYTHON = False
bstack1111llllll_opy_ = []
bstack1llll1l1ll_opy_ = bstack1ll11l1111_opy_
bstack1ll111l11lll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⣥")
bstack1ll11l1l1_opy_ = {}
SESSION_NAME = None
bstack1111l11111_opy_ = False
logger = logger_utils.get_logger(__name__, bstack1llll1l1ll_opy_)
store = {
    bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⣦"): []
}
bstack1ll1111lll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lll1l11l11_opy_ = {}
current_test_uuid = None
cli_context = bstack1lll11l111l_opy_(
    test_framework_name=bstack11l1ll1lll_opy_[bstack1ll1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ⣧")] if bstack1ll1111ll1_opy_() else bstack11l1ll1lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧ⣨")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack1111ll1l1_opy_):
    try:
        page.evaluate(bstack1ll1l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⣩"),
                      bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭⣪") + json.dumps(
                          bstack1111ll1l1_opy_) + bstack1ll1l11_opy_ (u"ࠥࢁࢂࠨ⣫"))
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ⣬"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1ll1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⣭"), bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ⣮") + json.dumps(
            message) + bstack1ll1l11_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ⣯") + json.dumps(level) + bstack1ll1l11_opy_ (u"ࠨࡿࢀࠫ⣰"))
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ⣱"), e)
def pytest_configure(config):
    global bstack1111ll111_opy_
    global CONFIG
    global_config = Config.bstack1lllllll1_opy_()
    config.args = bstack11l1l1l1_opy_.bstack1ll111ll1l11_opy_(config.args)
    global_config.bstack111l1ll111_opy_(bstack1l111l11l1_opy_(config.getoption(bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⣲"))))
    try:
        logger_utils.bstack1lll1l1ll1ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111111l1l_opy_.invoke(Events.CONNECT, bstack1ll1ll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⣳"), bstack1ll1l11_opy_ (u"ࠬ࠶ࠧ⣴")))
        config = json.loads(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ⣵"), bstack1ll1l11_opy_ (u"ࠢࡼࡿࠥ⣶")))
        cli.bstack1l11l1ll1l1_opy_(bstack1lll1lll11_opy_(bstack1111ll111_opy_, CONFIG), cli_context.platform_index, bstack1lll1111_opy_)
    if cli.bstack11lll111ll_opy_(bstack1llll11l1l_opy_):
        cli.bstack1111l111l_opy_()
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⣷") + str(cli_context.platform_index) + bstack1ll1l11_opy_ (u"ࠤࠥ⣸"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1ll1l11_opy_ (u"ࠥࡻ࡭࡫࡮ࠣ⣹"), None)
    if cli.is_running() and when == bstack1ll1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⣺"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1ll1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ⣻"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⣼")))
        if not passed:
            config = json.loads(os.environ.get(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ⣽"), bstack1ll1l11_opy_ (u"ࠣࡽࢀࠦ⣾")))
            if bstack11l1ll1ll_opy_.bstack111llll11l_opy_(config):
                bstack1ll1llll1111_opy_ = bstack11l1ll1ll_opy_.bstack1l1lll11_opy_(config)
                if item.execution_count > bstack1ll1llll1111_opy_:
                    print(bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡲࡦࡶࡵ࡭ࡪࡹ࠺ࠡࠩ⣿"), report.nodeid, os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⤀")))
                    bstack11l1ll1ll_opy_.bstack1lll1111ll1l_opy_(report.nodeid)
            else:
                print(bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠫ⤁"), report.nodeid, os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⤂")))
                bstack11l1ll1ll_opy_.bstack1lll1111ll1l_opy_(report.nodeid)
        else:
            print(bstack1ll1l11_opy_ (u"࠭ࡔࡦࡵࡷࠤࡵࡧࡳࡴࡧࡧ࠾ࠥ࠭⤃"), report.nodeid, os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⤄")))
    if cli.is_running():
        if when == bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⤅"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack1ll1l11_opy_ (u"ࠤࡦࡥࡱࡲࠢ⤆"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1ll1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ⤇"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⤈"))
    plugins = item.config.getoption(bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨ⤉"))
    report = outcome.get_result()
    os.environ[bstack1ll1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⤊")] = report.nodeid
    bstack1ll111l11ll1_opy_(item, call, report)
    if bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧ⤋") not in plugins or bstack1ll1111ll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1l11_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤ⤌"), None)
    page = getattr(item, bstack1ll1l11_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣ⤍"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll111l1111l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1111ll1l1_opy_(item, report, summary, skipSessionName)
def bstack1ll111l1111l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⤎") and report.skipped:
        bstack1ll1l11lll11_opy_(report)
    if report.when in [bstack1ll1l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⤏"), bstack1ll1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⤐")]:
        return
    if not bstack1l1lllllll_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1ll1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ⤑")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ⤒") + json.dumps(
                    report.nodeid) + bstack1ll1l11_opy_ (u"ࠨࡿࢀࠫ⤓"))
        os.environ[bstack1ll1l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⤔")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥ⤕").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⤖")))
    bstack11ll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨ⤗")
    bstack1ll1l11lll11_opy_(report)
    if not passed:
        try:
            bstack11ll11ll11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⤘").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll11ll11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⤙")))
        bstack11ll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠣࠤ⤚")
        if not passed:
            try:
                bstack11ll11ll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⤛").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll11ll11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ⤜")
                    + json.dumps(bstack1ll1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧ⤝"))
                    + bstack1ll1l11_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ⤞")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⤟")
                    + json.dumps(str(bstack11ll11ll11_opy_))
                    + bstack1ll1l11_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ⤠")
                )
        except Exception as e:
            summary.append(bstack1ll1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨ⤡").format(e))
def bstack1ll1111l1lll_opy_(test_name, error_message):
    try:
        bstack1ll111l11111_opy_ = []
        bstack11ll1l111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⤢"), bstack1ll1l11_opy_ (u"ࠪ࠴ࠬ⤣"))
        bstack1l11111lll_opy_ = {bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⤤"): test_name, bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⤥"): error_message, bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⤦"): bstack11ll1l111_opy_}
        bstack1ll1111ll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ⤧"))
        if os.path.exists(bstack1ll1111ll1ll_opy_):
            with open(bstack1ll1111ll1ll_opy_) as f:
                bstack1ll111l11111_opy_ = json.load(f)
        bstack1ll111l11111_opy_.append(bstack1l11111lll_opy_)
        with open(bstack1ll1111ll1ll_opy_, bstack1ll1l11_opy_ (u"ࠨࡹࠪ⤨")) as f:
            json.dump(bstack1ll111l11111_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ⤩") + str(e))
def bstack1ll1111ll1l1_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⤪"), bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⤫")]:
        return
    if (str(skipSessionName).lower() != bstack1ll1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪ⤬")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⤭")))
    bstack11ll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠢࠣ⤮")
    bstack1ll1l11lll11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11ll11ll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⤯").format(e)
                )
        try:
            if passed:
                bstack1l1ll1l111_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⤰"), None), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ⤱"))
            else:
                error_message = bstack1ll1l11_opy_ (u"ࠫࠬ⤲")
                if bstack11ll11ll11_opy_:
                    playwright_annotate(item._page, str(bstack11ll11ll11_opy_), bstack1ll1l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ⤳"))
                    bstack1l1ll1l111_opy_(getattr(item, bstack1ll1l11_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⤴"), None), bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ⤵"), str(bstack11ll11ll11_opy_))
                    error_message = str(bstack11ll11ll11_opy_)
                else:
                    bstack1l1ll1l111_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⤶"), None), bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⤷"))
                bstack1ll1111l1lll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ⤸").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1ll1l11_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ⤹"), default=bstack1ll1l11_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⤺"), help=bstack1ll1l11_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⤻"))
    parser.addoption(bstack1ll1l11_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ⤼"), default=bstack1ll1l11_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ⤽"), help=bstack1ll1l11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ⤾"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1l11_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ⤿"), action=bstack1ll1l11_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ⥀"), default=bstack1ll1l11_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ⥁"),
                         help=bstack1ll1l11_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ⥂"))
def bstack1llll1l1l1l_opy_(log):
    if not (log[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⥃")] and log[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⥄")].strip()):
        return
    active = bstack1llll1111ll_opy_()
    log = {
        bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⥅"): log[bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⥆")],
        bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⥇"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠬࡠࠧ⥈"),
        bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⥉"): log[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⥊")],
    }
    if active:
        if active[bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⥋")] == bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⥌"):
            log[bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⥍")] = active[bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⥎")]
        elif active[bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⥏")] == bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࠫ⥐"):
            log[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⥑")] = active[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⥒")]
    TestHubHandler.bstack1l11ll11l_opy_([log])
def bstack1llll1111ll_opy_():
    if len(store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⥓")]) > 0 and store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⥔")][-1]:
        return {
            bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⥕"): bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⥖"),
            bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⥗"): store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⥘")][-1]
        }
    if store.get(bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⥙"), None):
        return {
            bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⥚"): bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨ⥛"),
            bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⥜"): store[bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⥝")]
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
        item._1ll111l111l1_opy_ = True
        bstack11ll111lll_opy_ = a11y.is_enabled_testcase(bstack1llll1l1l11l_opy_(item.own_markers))
        if not cli.bstack11lll111ll_opy_(bstack1llll11l1l_opy_):
            item._a11y_test_case = bstack11ll111lll_opy_
            if bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⥞"), None):
                driver = getattr(item, bstack1ll1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⥟"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack11ll111lll_opy_)
        if not TestHubHandler.on() or bstack1ll111l11lll_opy_ != bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⥠"):
            return
        global current_test_uuid #, bstack1llll1l1111_opy_
        bstack1lll1l1l111_opy_ = {
            bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⥡"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⥢"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠫ࡟࠭⥣")
        }
        current_test_uuid = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⥤")]
        store[bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⥥")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⥦")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lll1l11l11_opy_[item.nodeid] = {**_1lll1l11l11_opy_[item.nodeid], **bstack1lll1l1l111_opy_}
        bstack1ll111l1l111_opy_(item, _1lll1l11l11_opy_[item.nodeid], bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⥧"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫ⥨"), str(err))
def pytest_runtest_setup(item):
    store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⥩")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⥪"))
    if bstack11l1ll1ll_opy_.bstack1lll111l1l1l_opy_():
            bstack1ll111l1ll11_opy_ = bstack1ll1l11_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡧࡳࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ⥫")
            logger.error(bstack1ll111l1ll11_opy_)
            bstack1lll1l1l111_opy_ = {
                bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⥬"): uuid4().__str__(),
                bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⥭"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠨ࡜ࠪ⥮"),
                bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⥯"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠪ࡞ࠬ⥰"),
                bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⥱"): bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⥲"),
                bstack1ll1l11_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭⥳"): bstack1ll111l1ll11_opy_,
                bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⥴"): [],
                bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⥵"): []
            }
            bstack1ll111l1l111_opy_(item, bstack1lll1l1l111_opy_, bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⥶"))
            pytest.skip(bstack1ll111l1ll11_opy_)
            return # skip all existing operations
    global bstack1ll1111lll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1llllll111l1_opy_():
        atexit.register(bstack11111l11l1_opy_)
        if not bstack1ll1111lll11_opy_:
            try:
                bstack1ll1111l1l11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1llll11l111l_opy_():
                    bstack1ll1111l1l11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1111l1l11_opy_:
                    signal.signal(s, bstack1ll1l11l11l_opy_)
                bstack1ll1111lll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦ⥷") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1l1l11l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⥸")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lll1l1l111_opy_ = {
            bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⥹"): uuid,
            bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⥺"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"࡛ࠧࠩ⥻"),
            bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⥼"): bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⥽"),
            bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⥾"): bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⥿"),
            bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⦀"): bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⦁")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⦂")] = item
        store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⦃")] = [uuid]
        if not _1lll1l11l11_opy_.get(item.nodeid, None):
            _1lll1l11l11_opy_[item.nodeid] = {bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⦄"): [], bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⦅"): []}
        _1lll1l11l11_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⦆")].append(bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⦇")])
        _1lll1l11l11_opy_[item.nodeid + bstack1ll1l11_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭⦈")] = bstack1lll1l1l111_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll111l11l1l_opy_(item, bstack1lll1l1l111_opy_, bstack1ll1l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⦉"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ⦊"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⦋"))
        return # skip all existing operations
    try:
        global bstack1ll11l1l1_opy_
        bstack11ll1l111_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11ll1l111_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⦌")))
        if bstack11ll111l1l_opy_.bstack1111ll1l1l_opy_() == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ⦍"):
            if bstack11ll111l1l_opy_.bstack11l1l11l1l_opy_() == bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⦎"):
                bstack1ll1111lllll_opy_ = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⦏"), None)
                bstack1l1l1ll11_opy_ = bstack1ll1111lllll_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥ⦐")
                driver = getattr(item, bstack1ll1l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⦑"), None)
                bstack111lll1lll_opy_ = getattr(item, bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⦒"), None)
                bstack111lll1ll_opy_ = getattr(item, bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⦓"), None)
                PercySDK.screenshot(driver, bstack1l1l1ll11_opy_, bstack111lll1lll_opy_=bstack111lll1lll_opy_, bstack111lll1ll_opy_=bstack111lll1ll_opy_, bstack11lllll1l1_opy_=bstack11ll1l111_opy_)
        if not cli.bstack11lll111ll_opy_(bstack1llll11l1l_opy_):
            if getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ⦔"), False):
                bstack1l111l1ll_opy_.bstack1ll1l111l_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⦕"), None), bstack1ll11l1l1_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lll1l1l111_opy_ = {
            bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⦖"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⦗"): bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠨ࡜ࠪ⦘"),
            bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⦙"): bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⦚"),
            bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⦛"): bstack1ll1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⦜"),
            bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⦝"): bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⦞")
        }
        _1lll1l11l11_opy_[item.nodeid + bstack1ll1l11_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ⦟")] = bstack1lll1l1l111_opy_
        bstack1ll111l11l1l_opy_(item, bstack1lll1l1l111_opy_, bstack1ll1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⦠"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩ⦡"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1ll1l11lllll_opy_(fixturedef.argname):
        store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ⦢")] = request.node
    elif bstack1ll1l11ll1l1_opy_(fixturedef.argname):
        store[bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ⦣")] = request.node
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
            bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⦤"): fixturedef.argname,
            bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⦥"): bstack1lllllll111l_opy_(outcome),
            bstack1ll1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⦦"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⦧")]
        if not _1lll1l11l11_opy_.get(current_test_item.nodeid, None):
            _1lll1l11l11_opy_[current_test_item.nodeid] = {bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⦨"): []}
        _1lll1l11l11_opy_[current_test_item.nodeid][bstack1ll1l11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⦩")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ⦪"), str(err))
if bstack1ll1111ll1_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1lll1l11l11_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⦫")].bstack1ll1l111_opy_(id(step))
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ⦬"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1lll1l11l11_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⦭")].bstack1llll1ll111_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭⦮"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            bstack1llll11llll_opy_: bstack1llll1l111l_opy_ = _1lll1l11l11_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⦯")]
            bstack1llll11llll_opy_.bstack1llll1ll111_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ⦰"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111l11lll_opy_
        try:
            if not TestHubHandler.on() or bstack1ll111l11lll_opy_ != bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⦱"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ⦲"), None)
            if not _1lll1l11l11_opy_.get(request.node.nodeid, None):
                _1lll1l11l11_opy_[request.node.nodeid] = {}
            bstack1llll11llll_opy_ = bstack1llll1l111l_opy_.bstack1ll11llll1l1_opy_(
                scenario, feature, request.node,
                name=bstack1ll1l1l1111l_opy_(request.node, scenario),
                started_at=bstack111ll1ll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ⦳"),
                tags=bstack1ll1l11ll11l_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llll11lll1_opy_(driver) if driver and driver.session_id else {}
            )
            _1lll1l11l11_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⦴")] = bstack1llll11llll_opy_
            bstack1ll111l1l1l1_opy_(bstack1llll11llll_opy_.uuid)
            TestHubHandler.bstack1llll11l111_opy_(bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⦵"), bstack1llll11llll_opy_)
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ⦶"), str(err))
def bstack1ll111l1l11l_opy_(bstack1llll11ll1l_opy_):
    if bstack1llll11ll1l_opy_ in store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⦷")]:
        store[bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⦸")].remove(bstack1llll11ll1l_opy_)
def bstack1ll111l1l1l1_opy_(test_uuid):
    store[bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⦹")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll11l11llll_opy_
def bstack1ll111l11ll1_opy_(item, call, report):
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩ⦺"))
    global bstack1ll111l11lll_opy_
    bstack1111l1l11l_opy_ = bstack111ll1ll1l_opy_()
    if hasattr(report, bstack1ll1l11_opy_ (u"ࠨࡵࡷࡳࡵ࠭⦻")):
        bstack1111l1l11l_opy_ = bstack1lllll11lll1_opy_(report.stop)
    elif hasattr(report, bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ⦼")):
        bstack1111l1l11l_opy_ = bstack1lllll11lll1_opy_(report.start)
    try:
        if getattr(report, bstack1ll1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⦽"), bstack1ll1l11_opy_ (u"ࠫࠬ⦾")) == bstack1ll1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⦿"):
            logger.debug(bstack1ll1l11_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ⧀").format(getattr(report, bstack1ll1l11_opy_ (u"ࠧࡸࡪࡨࡲࠬ⧁"), bstack1ll1l11_opy_ (u"ࠨࠩ⧂")).__str__(), bstack1ll111l11lll_opy_))
            if bstack1ll111l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⧃"):
                _1lll1l11l11_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⧄")] = bstack1111l1l11l_opy_
                bstack1ll111l1l111_opy_(item, _1lll1l11l11_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⧅"), report, call)
                store[bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⧆")] = None
            elif bstack1ll111l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ⧇"):
                bstack1llll11llll_opy_ = _1lll1l11l11_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⧈")]
                bstack1llll11llll_opy_.set(hooks=_1lll1l11l11_opy_[item.nodeid].get(bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⧉"), []))
                exception, bstack1llll1l11l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llll1l11l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ⧊"), bstack1ll1l11_opy_ (u"ࠪࠫ⧋"))]
                bstack1llll11llll_opy_.stop(time=bstack1111l1l11l_opy_, result=Result(result=getattr(report, bstack1ll1l11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⧌"), bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⧍")), exception=exception, bstack1llll1l11l1_opy_=bstack1llll1l11l1_opy_))
                TestHubHandler.bstack1llll11l111_opy_(bstack1ll1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⧎"), _1lll1l11l11_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⧏")])
        elif getattr(report, bstack1ll1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⧐"), bstack1ll1l11_opy_ (u"ࠩࠪ⧑")) in [bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⧒"), bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⧓")]:
            logger.debug(bstack1ll1l11_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⧔").format(getattr(report, bstack1ll1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫ⧕"), bstack1ll1l11_opy_ (u"ࠧࠨ⧖")).__str__(), bstack1ll111l11lll_opy_))
            bstack1llll1ll11l_opy_ = item.nodeid + bstack1ll1l11_opy_ (u"ࠨ࠯ࠪ⧗") + getattr(report, bstack1ll1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⧘"), bstack1ll1l11_opy_ (u"ࠪࠫ⧙"))
            if getattr(report, bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⧚"), False):
                hook_type = bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⧛") if getattr(report, bstack1ll1l11_opy_ (u"࠭ࡷࡩࡧࡱࠫ⧜"), bstack1ll1l11_opy_ (u"ࠧࠨ⧝")) == bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⧞") else bstack1ll1l11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⧟")
                _1lll1l11l11_opy_[bstack1llll1ll11l_opy_] = {
                    bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⧠"): uuid4().__str__(),
                    bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⧡"): bstack1111l1l11l_opy_,
                    bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⧢"): hook_type
                }
            _1lll1l11l11_opy_[bstack1llll1ll11l_opy_][bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⧣")] = bstack1111l1l11l_opy_
            bstack1ll111l1l11l_opy_(_1lll1l11l11_opy_[bstack1llll1ll11l_opy_][bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⧤")])
            bstack1ll111l11l1l_opy_(item, _1lll1l11l11_opy_[bstack1llll1ll11l_opy_], bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⧥"), report, call)
            if getattr(report, bstack1ll1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⧦"), bstack1ll1l11_opy_ (u"ࠪࠫ⧧")) == bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⧨"):
                if getattr(report, bstack1ll1l11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⧩"), bstack1ll1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⧪")) == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⧫"):
                    bstack1lll1l1l111_opy_ = {
                        bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⧬"): uuid4().__str__(),
                        bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⧭"): bstack111ll1ll1l_opy_(),
                        bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⧮"): bstack111ll1ll1l_opy_()
                    }
                    _1lll1l11l11_opy_[item.nodeid] = {**_1lll1l11l11_opy_[item.nodeid], **bstack1lll1l1l111_opy_}
                    bstack1ll111l1l111_opy_(item, _1lll1l11l11_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⧯"))
                    bstack1ll111l1l111_opy_(item, _1lll1l11l11_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⧰"), report, call)
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ⧱"), str(err))
def bstack1ll111l1l1ll_opy_(test, bstack1lll1l1l111_opy_, result=None, call=None, bstack11l1l1lll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1llll11llll_opy_ = {
        bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⧲"): bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⧳")],
        bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⧴"): bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨ⧵"),
        bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⧶"): test.name,
        bstack1ll1l11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⧷"): {
            bstack1ll1l11_opy_ (u"࠭࡬ࡢࡰࡪࠫ⧸"): bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⧹"),
            bstack1ll1l11_opy_ (u"ࠨࡥࡲࡨࡪ࠭⧺"): inspect.getsource(test.obj)
        },
        bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⧻"): test.name,
        bstack1ll1l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⧼"): test.name,
        bstack1ll1l11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⧽"): bstack11l1l1l1_opy_.bstack1lll1ll11l1_opy_(test),
        bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⧾"): file_path,
        bstack1ll1l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⧿"): file_path,
        bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⨀"): bstack1ll1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⨁"),
        bstack1ll1l11_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⨂"): file_path,
        bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⨃"): bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⨄")],
        bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⨅"): bstack1ll1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⨆"),
        bstack1ll1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⨇"): {
            bstack1ll1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⨈"): test.nodeid
        },
        bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⨉"): bstack1llll1l1l11l_opy_(test.own_markers)
    }
    if bstack11l1l1lll1_opy_ in [bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⨊"), bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⨋")]:
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡵࡣࠪ⨌")] = {
            bstack1ll1l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⨍"): bstack1lll1l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⨎"), [])
        }
    if bstack11l1l1lll1_opy_ == bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⨏"):
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⨐")] = bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⨑")
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⨒")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⨓")]
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⨔")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⨕")]
    if result:
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⨖")] = result.outcome
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⨗")] = result.duration * 1000
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⨘")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⨙")]
        if result.failed:
            bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⨚")] = TestHubHandler.bstack1ll111l1lll_opy_(call.excinfo.typename)
            bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⨛")] = TestHubHandler.bstack1ll11l111ll1_opy_(call.excinfo, result)
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⨜")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⨝")]
    if outcome:
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⨞")] = bstack1lllllll111l_opy_(outcome)
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⨟")] = 0
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⨠")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⨡")]
        if bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⨢")] == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⨣"):
            bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⨤")] = bstack1ll1l11_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⨥")  # bstack1ll1111lll1l_opy_
            bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⨦")] = [{bstack1ll1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⨧"): [bstack1ll1l11_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⨨")]}]
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⨩")] = bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⨪")]
    return bstack1llll11llll_opy_
def bstack1ll111l11l11_opy_(test, bstack1lll1ll1ll1_opy_, bstack11l1l1lll1_opy_, result, call, outcome, bstack1ll111l1ll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⨫")]
    hook_name = bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⨬")]
    hook_data = {
        bstack1ll1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⨭"): bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⨮")],
        bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⨯"): bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⨰"),
        bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⨱"): bstack1ll1l11_opy_ (u"ࠨࡽࢀࠫ⨲").format(bstack1ll1l11lll1l_opy_(hook_name)),
        bstack1ll1l11_opy_ (u"ࠩࡥࡳࡩࡿࠧ⨳"): {
            bstack1ll1l11_opy_ (u"ࠪࡰࡦࡴࡧࠨ⨴"): bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⨵"),
            bstack1ll1l11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⨶"): None
        },
        bstack1ll1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⨷"): test.name,
        bstack1ll1l11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⨸"): bstack11l1l1l1_opy_.bstack1lll1ll11l1_opy_(test, hook_name),
        bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⨹"): file_path,
        bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⨺"): file_path,
        bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⨻"): bstack1ll1l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⨼"),
        bstack1ll1l11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⨽"): file_path,
        bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⨾"): bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⨿")],
        bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⩀"): bstack1ll1l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ⩁") if bstack1ll111l11lll_opy_ == bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⩂") else bstack1ll1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⩃"),
        bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⩄"): hook_type
    }
    bstack1l111ll11ll_opy_ = bstack1lll11ll111_opy_(_1lll1l11l11_opy_.get(test.nodeid, None))
    if bstack1l111ll11ll_opy_:
        hook_data[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⩅")] = bstack1l111ll11ll_opy_
    if result:
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩆")] = result.outcome
        hook_data[bstack1ll1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⩇")] = result.duration * 1000
        hook_data[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⩈")] = bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩉")]
        if result.failed:
            hook_data[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⩊")] = TestHubHandler.bstack1ll111l1lll_opy_(call.excinfo.typename)
            hook_data[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⩋")] = TestHubHandler.bstack1ll11l111ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⩌")] = bstack1lllllll111l_opy_(outcome)
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⩍")] = 100
        hook_data[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⩎")] = bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⩏")]
        if hook_data[bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⩐")] == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⩑"):
            hook_data[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⩒")] = bstack1ll1l11_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⩓")  # bstack1ll1111lll1l_opy_
            hook_data[bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⩔")] = [{bstack1ll1l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⩕"): [bstack1ll1l11_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⩖")]}]
    if bstack1ll111l1ll1l_opy_:
        hook_data[bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⩗")] = bstack1ll111l1ll1l_opy_.result
        hook_data[bstack1ll1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⩘")] = bstack1ll1l1ll111_opy_(bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⩙")], bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⩚")])
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⩛")] = bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⩜")]
        if hook_data[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⩝")] == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⩞"):
            hook_data[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⩟")] = TestHubHandler.bstack1ll111l1lll_opy_(bstack1ll111l1ll1l_opy_.exception_type)
            hook_data[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⩠")] = [{bstack1ll1l11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⩡"): bstack1lllll1lll11_opy_(bstack1ll111l1ll1l_opy_.exception)}]
    return hook_data
def bstack1ll111l1l111_opy_(test, bstack1lll1l1l111_opy_, bstack11l1l1lll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ⩢").format(bstack11l1l1lll1_opy_))
    bstack1llll11llll_opy_ = bstack1ll111l1l1ll_opy_(test, bstack1lll1l1l111_opy_, result, call, bstack11l1l1lll1_opy_, outcome)
    driver = getattr(test, bstack1ll1l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⩣"), None)
    if bstack11l1l1lll1_opy_ == bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⩤") and driver:
        bstack1llll11llll_opy_[bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ⩥")] = TestHubHandler.bstack1llll11lll1_opy_(driver)
    if bstack11l1l1lll1_opy_ == bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⩦"):
        bstack11l1l1lll1_opy_ = bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⩧")
    bstack1lll1llll1l_opy_ = {
        bstack1ll1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⩨"): bstack11l1l1lll1_opy_,
        bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⩩"): bstack1llll11llll_opy_
    }
    TestHubHandler.bstack1ll11ll11_opy_(bstack1lll1llll1l_opy_)
    if bstack11l1l1lll1_opy_ == bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⩪"):
        threading.current_thread().bstackTestMeta = {bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⩫"): bstack1ll1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⩬")}
    elif bstack11l1l1lll1_opy_ == bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⩭"):
        threading.current_thread().bstackTestMeta = {bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⩮"): getattr(result, bstack1ll1l11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⩯"), bstack1ll1l11_opy_ (u"ࠧࠨ⩰"))}
def bstack1ll111l11l1l_opy_(test, bstack1lll1l1l111_opy_, bstack11l1l1lll1_opy_, result=None, call=None, outcome=None, bstack1ll111l1ll1l_opy_=None):
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⩱").format(bstack11l1l1lll1_opy_))
    hook_data = bstack1ll111l11l11_opy_(test, bstack1lll1l1l111_opy_, bstack11l1l1lll1_opy_, result, call, outcome, bstack1ll111l1ll1l_opy_)
    bstack1lll1llll1l_opy_ = {
        bstack1ll1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⩲"): bstack11l1l1lll1_opy_,
        bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ⩳"): hook_data
    }
    TestHubHandler.bstack1ll11ll11_opy_(bstack1lll1llll1l_opy_)
def bstack1lll11ll111_opy_(bstack1lll1l1l111_opy_):
    if not bstack1lll1l1l111_opy_:
        return None
    if bstack1lll1l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⩴"), None):
        return getattr(bstack1lll1l1l111_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⩵")], bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⩶"), None)
    return bstack1lll1l1l111_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⩷"), None)
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
        places = [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⩸"), bstack1ll1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧ⩹"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⩺")]
        logs = []
        for bstack1ll1111l11ll_opy_ in places:
            records = caplog.get_records(bstack1ll1111l11ll_opy_)
            bstack1ll1111ll111_opy_ = bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⩻") if bstack1ll1111l11ll_opy_ == bstack1ll1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⩼") else bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⩽")
            bstack1ll1111l1l1l_opy_ = request.node.nodeid + (bstack1ll1l11_opy_ (u"ࠧࠨ⩾") if bstack1ll1111l11ll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭⩿") else bstack1ll1l11_opy_ (u"ࠩ࠰ࠫ⪀") + bstack1ll1111l11ll_opy_)
            test_uuid = bstack1lll11ll111_opy_(_1lll1l11l11_opy_.get(bstack1ll1111l1l1l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1llllll1l1ll_opy_(record.message):
                    continue
                logs.append({
                    bstack1ll1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⪁"): bstack1llll11ll111_opy_(record.created).isoformat() + bstack1ll1l11_opy_ (u"ࠫ࡟࠭⪂"),
                    bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⪃"): record.levelname,
                    bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⪄"): record.message,
                    bstack1ll1111ll111_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1l11ll11l_opy_(logs)
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ⪅"), str(err))
def bstack11lll11l11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1111l11111_opy_
    bstack1l1l11l1l1_opy_ = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ⪆"), None) and bstack11l11l1ll_opy_(
            threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⪇"), None)
    bstack11111ll1l_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⪈"), None) != None and getattr(driver, bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⪉"), None) == True
    if sequence == bstack1ll1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⪊") and driver != None:
      if not bstack1111l11111_opy_ and bstack1l1lllllll_opy_() and bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⪋") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⪌")] == True and accessibility_scripts.bstack11l111lll_opy_(driver_command) and (bstack11111ll1l_opy_ or bstack1l1l11l1l1_opy_) and not bstack11l111l11_opy_(args):
        try:
          bstack1111l11111_opy_ = True
          logger.debug(bstack1ll1l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ⪍").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ⪎").format(str(err)))
        bstack1111l11111_opy_ = False
    if sequence == bstack1ll1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⪏"):
        if driver_command == bstack1ll1l11_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ⪐"):
            TestHubHandler.bstack11l11l1l1l_opy_({
                bstack1ll1l11_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⪑"): response[bstack1ll1l11_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ⪒")],
                bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⪓"): store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⪔")]
            })
def bstack11111l11l1_opy_():
    global bstack1111llllll_opy_
    logger_utils.bstack1111111ll1_opy_()
    logging.shutdown()
    TestHubHandler.bstack1lll1ll11ll_opy_()
    for driver in bstack1111llllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l11l11l_opy_(*args):
    global bstack1111llllll_opy_
    TestHubHandler.bstack1lll1ll11ll_opy_()
    for driver in bstack1111llllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll111lll_opy_, stage=STAGE.bstack1ll11l11_opy_, bstack1lll1l1ll1_opy_=SESSION_NAME)
def bstack1l11llll11_opy_(self, *args, **kwargs):
    bstack1llll1ll1_opy_ = bstack1l1l11l111_opy_(self, *args, **kwargs)
    bstack1ll111111_opy_ = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⪕"), None)
    if bstack1ll111111_opy_ and bstack1ll111111_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⪖"), bstack1ll1l11_opy_ (u"ࠫࠬ⪗")) == bstack1ll1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⪘"):
        TestHubHandler.send_cbt_info(self)
    return bstack1llll1ll1_opy_
@measure(event_name=EVENTS.bstack1lllllll1l1_opy_, stage=STAGE.bstack1l11l11l1_opy_, bstack1lll1l1ll1_opy_=SESSION_NAME)
def bstack111l11ll_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.bstack1lllllll1_opy_()
    if global_config.get_property(bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⪙")):
        return
    global_config.bstack1111ll1l11_opy_(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⪚"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack11111l1l1_opy_.format(FRAMEWORK_NAME.split(bstack1ll1l11_opy_ (u"ࠨ࠯ࠪ⪛"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lllllll_opy_():
            Service.start = bstack11l1l111_opy_
            Service.stop = bstack1ll1ll1l1l_opy_
            webdriver.Remote.get = bstack1l1llll1ll_opy_
            webdriver.Remote.__init__ = bstack1ll1ll1lll_opy_
            if not isinstance(os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ⪜")), str):
                return
            WebDriver.quit = bstack1l1l11l11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1l11llll11_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⪝")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⪞")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack111l11lll1_opy_(bstack1ll1l11_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ⪟"), bstack11111l1l_opy_)
    if bstack11l11l11l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1ll1l11_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⪠")) and callable(getattr(RemoteConnection, bstack1ll1l11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⪡"))):
                RemoteConnection._get_proxy_url = bstack11l11lll11_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11l11lll11_opy_
        except Exception as e:
            logger.error(bstack1l11l111_opy_.format(str(e)))
    if bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⪢") in str(framework_name).lower():
        if not bstack1l1lllllll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l111l11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1111ll_opy_
            Config.getoption = bstack11l11l1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1llllll1111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111111llll_opy_, stage=STAGE.bstack1ll11l11_opy_, bstack1lll1l1ll1_opy_=SESSION_NAME)
def bstack1l1l11l11l_opy_(self):
    global FRAMEWORK_NAME
    global bstack11ll1l1111_opy_
    global bstack1lll1ll11_opy_
    try:
        if bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⪣") in FRAMEWORK_NAME and self.session_id != None and bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ⪤"), bstack1ll1l11_opy_ (u"ࠫࠬ⪥")) != bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⪦"):
            bstack11111111l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⪧") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⪨")
            bstack1lllllll11l_opy_(logger, True)
            if os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⪩"), None):
                self.execute_script(
                    bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ⪪") + json.dumps(
                        os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⪫"))) + bstack1ll1l11_opy_ (u"ࠫࢂࢃࠧ⪬"))
            if self != None:
                bstack11l11lll1l_opy_(self, bstack11111111l_opy_, bstack1ll1l11_opy_ (u"ࠬ࠲ࠠࠨ⪭").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack11lll111ll_opy_(bstack1llll11l1l_opy_):
            item = store.get(bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⪮"), None)
            if item is not None and bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⪯"), None):
                bstack1l111l1ll_opy_.bstack1ll1l111l_opy_(self, bstack1ll11l1l1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"ࠨࠩ⪰")
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ⪱") + str(e))
    bstack1lll1ll11_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1ll11l_opy_, stage=STAGE.bstack1ll11l11_opy_, bstack1lll1l1ll1_opy_=SESSION_NAME)
def bstack1ll1ll1lll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll1l1111_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1l1l11l111_opy_
    global bstack1111llllll_opy_
    global bstack1111ll111_opy_
    global bstack111l111l1_opy_
    global bstack1ll11l1l1_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⪲")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack1lll1lll11_opy_(bstack1111ll111_opy_, CONFIG)
    logger.debug(bstack1ll1llll1l_opy_.format(command_executor))
    proxy = bstack1lllll1l1l1_opy_(CONFIG, proxy)
    bstack11ll1l111_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11ll1l111_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⪳")))
    except:
        bstack11ll1l111_opy_ = 0
    bstack11l111ll_opy_ = get_caps(CONFIG, bstack11ll1l111_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l111ll_opy_)))
    bstack1ll11l1l1_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⪴"))[bstack11ll1l111_opy_]
    if bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⪵") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⪶")]:
        update_caps_for_local(bstack11l111ll_opy_, bstack111l111l1_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack11ll1l111_opy_) and a11y.is_platform_supported(bstack11l111ll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack11lll111ll_opy_(bstack1llll11l1l_opy_):
            a11y.set_capabilities(bstack11l111ll_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll1111ll_opy_ = bstack11ll11l11l_opy_(desired_capabilities)
        bstack1lll1111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⪷")] = bstack111l11l1_opy_(CONFIG)
        bstack1111l111ll_opy_ = get_caps(bstack1lll1111ll_opy_)
        if bstack1111l111ll_opy_:
            bstack11l111ll_opy_ = update(bstack1111l111ll_opy_, bstack11l111ll_opy_)
        desired_capabilities = None
    if options:
        bstack1111l111l1_opy_(options, bstack11l111ll_opy_)
    if not options:
        options = bstack1lll1111_opy_(bstack11l111ll_opy_)
    if proxy and bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⪸")):
        options.proxy(proxy)
    if options and bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⪹")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11lll1ll_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⪺")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l111ll_opy_)
    logger.info(bstack11l1l11l_opy_)
    bstack1111llll1l_opy_.end(EVENTS.bstack1lllllll1l1_opy_.value, EVENTS.bstack1lllllll1l1_opy_.value + bstack1ll1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⪻"),
                               EVENTS.bstack1lllllll1l1_opy_.value + bstack1ll1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⪼"), True, None)
    try:
        if bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⪽")):
            bstack1l1l11l111_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⪾")):
            bstack1l1l11l111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ⪿")):
            bstack1l1l11l111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l1l11l111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11lll1lll1_opy_:
        logger.error(bstack1l11l1ll11_opy_.format(bstack1ll1l11_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩ⫀"), str(bstack11lll1lll1_opy_)))
        raise bstack11lll1lll1_opy_
    try:
        bstack11l1l1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬ⫁")
        if bstack11lll1ll_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭⫂")):
            bstack11l1l1ll1_opy_ = self.caps.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⫃"))
        else:
            bstack11l1l1ll1_opy_ = self.capabilities.get(bstack1ll1l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⫄"))
        if bstack11l1l1ll1_opy_:
            bstack1ll1l11ll_opy_(bstack11l1l1ll1_opy_)
            if bstack11lll1ll_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ⫅")):
                self.command_executor._url = bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⫆") + bstack1111ll111_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ⫇")
            else:
                self.command_executor._url = bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ⫈") + bstack11l1l1ll1_opy_ + bstack1ll1l11_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ⫉")
            logger.debug(bstack1l1llllll1_opy_.format(bstack11l1l1ll1_opy_))
        else:
            logger.debug(bstack1ll11l1l1l_opy_.format(bstack1ll1l11_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ⫊")))
    except Exception as e:
        logger.debug(bstack1ll11l1l1l_opy_.format(e))
    bstack11ll1l1111_opy_ = self.session_id
    if bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⫋") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⫌"), None)
        if item:
            bstack1ll111l1lll1_opy_ = getattr(item, bstack1ll1l11_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ⫍"), False)
            if not getattr(item, bstack1ll1l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⫎"), None) and bstack1ll111l1lll1_opy_:
                setattr(store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⫏")], bstack1ll1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⫐"), self)
        bstack1ll111111_opy_ = getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⫑"), None)
        if bstack1ll111111_opy_ and bstack1ll111111_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⫒"), bstack1ll1l11_opy_ (u"ࠨࠩ⫓")) == bstack1ll1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⫔"):
            TestHubHandler.send_cbt_info(self)
    bstack1111llllll_opy_.append(self)
    if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⫕") in CONFIG and bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⫖") in CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⫗")][bstack11ll1l111_opy_]:
        SESSION_NAME = CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⫘")][bstack11ll1l111_opy_][bstack1ll1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⫙")]
    logger.debug(bstack1l1111l1_opy_.format(bstack11ll1l1111_opy_))
@measure(event_name=EVENTS.bstack111l11l11_opy_, stage=STAGE.bstack1ll11l11_opy_, bstack1lll1l1ll1_opy_=SESSION_NAME)
def bstack1l1llll1ll_opy_(self, url):
    global bstack1111ll111l_opy_
    global CONFIG
    try:
        bstack1lll1l111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll11ll1_opy_.format(str(err)))
    try:
        bstack1111ll111l_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack111llll1ll_opy_):
                bstack1lll1l111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll11ll1_opy_.format(str(err)))
        raise e
def bstack1111l1l11_opy_(item, when):
    global bstack11l11111ll_opy_
    try:
        bstack11l11111ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1llllll1111_opy_(item, call, rep):
    global bstack1lllll1ll1_opy_
    global bstack1111llllll_opy_
    name = bstack1ll1l11_opy_ (u"ࠨࠩ⫚")
    try:
        if rep.when == bstack1ll1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧ⫛"):
            bstack11ll1l1111_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⫝̸"))
            try:
                if (str(skipSessionName).lower() != bstack1ll1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩ⫝")):
                    name = str(rep.nodeid)
                    bstack11111lll1_opy_ = bstack1l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⫞"), name, bstack1ll1l11_opy_ (u"࠭ࠧ⫟"), bstack1ll1l11_opy_ (u"ࠧࠨ⫠"), bstack1ll1l11_opy_ (u"ࠨࠩ⫡"), bstack1ll1l11_opy_ (u"ࠩࠪ⫢"))
                    os.environ[bstack1ll1l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⫣")] = name
                    for driver in bstack1111llllll_opy_:
                        if bstack11ll1l1111_opy_ == driver.session_id:
                            driver.execute_script(bstack11111lll1_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⫤").format(str(e)))
            try:
                bstack1l1l1l1l11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⫥"):
                    status = bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⫦") if rep.outcome.lower() == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⫧") else bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⫨")
                    reason = bstack1ll1l11_opy_ (u"ࠩࠪ⫩")
                    if status == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⫪"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ⫫") if status == bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⫬") else bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⫭")
                    data = name + bstack1ll1l11_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ⫮") if status == bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⫯") else name + bstack1ll1l11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ⫰") + reason
                    bstack11l111llll_opy_ = bstack1l11ll111l_opy_(bstack1ll1l11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⫱"), bstack1ll1l11_opy_ (u"ࠫࠬ⫲"), bstack1ll1l11_opy_ (u"ࠬ࠭⫳"), bstack1ll1l11_opy_ (u"࠭ࠧ⫴"), level, data)
                    for driver in bstack1111llllll_opy_:
                        if bstack11ll1l1111_opy_ == driver.session_id:
                            driver.execute_script(bstack11l111llll_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⫵").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ⫶").format(str(e)))
    bstack1lllll1ll1_opy_(item, call, rep)
notset = Notset()
def bstack11l11l1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack111llll1l1_opy_
    if str(name).lower() == bstack1ll1l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ⫷"):
        return bstack1ll1l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ⫸")
    else:
        return bstack111llll1l1_opy_(self, name, default, skip)
def bstack11l11lll11_opy_(self):
    global CONFIG
    global bstack11ll11ll1_opy_
    try:
        proxy = bstack111111lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ⫹")):
                proxies = bstack11lll111l1_opy_(proxy, bstack1lll1lll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1ll1lll1_opy_ = proxies.popitem()
                    if bstack1ll1l11_opy_ (u"ࠧࡀ࠯࠰ࠤ⫺") in bstack1l1ll1lll1_opy_:
                        return bstack1l1ll1lll1_opy_
                    else:
                        return bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⫻") + bstack1l1ll1lll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ⫼").format(str(e)))
    return bstack11ll11ll1_opy_(self)
def bstack11l11l11l1_opy_():
    return (bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⫽") in CONFIG or bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⫾") in CONFIG) and bstack11l111l111_opy_() and bstack11lll1ll_opy_() >= version.parse(
        bstack111lll1l1_opy_)
def bstack1ll11lll11_opy_(self,
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
    CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⫿")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack11ll1l111_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11ll1l111_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⬀")))
    except:
        bstack11ll1l111_opy_ = 0
    CONFIG[bstack1ll1l11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ⬁")] = True
    bstack11l111ll_opy_ = get_caps(CONFIG, bstack11ll1l111_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack11l111ll_opy_)))
    if CONFIG.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⬂")):
        update_caps_for_local(bstack11l111ll_opy_, bstack111l111l1_opy_)
    if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⬃") in CONFIG and bstack1ll1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⬄") in CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⬅")][bstack11ll1l111_opy_]:
        SESSION_NAME = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⬆")][bstack11ll1l111_opy_][bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⬇")]
    import urllib
    import json
    if bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⬈") in CONFIG and str(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⬉")]).lower() != bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭⬊"):
        bstack1llll1l11l_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1llll1l11l_opy_ + urllib.parse.quote(json.dumps(bstack11l111ll_opy_))
    else:
        cdpUrl = bstack1ll1l11_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ⬋") + urllib.parse.quote(json.dumps(bstack11l111ll_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l1l11111_opy_
        if not bstack1l1lllllll_opy_():
            global bstack1l1l11l1_opy_
            if not bstack1l1l11l1_opy_:
                from bstack_utils.helper import bstack1111l1ll1l_opy_, bstack1llll11ll11l_opy_
                bstack1l1l11l1_opy_ = bstack1111l1ll1l_opy_()
                bstack1llll11ll11l_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l1l1l11111_opy_
            return
        BrowserType.launch = bstack1ll11lll11_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll1111ll11l_opy_():
    global CONFIG
    global bstack1l1ll1l11l_opy_
    global bstack1111ll111_opy_
    global bstack111l111l1_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack1llll1l1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ⬌")))
    bstack1l1ll1l11l_opy_ = eval(os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⬍")))
    bstack1111ll111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ⬎"))
    bstack1l111ll1_opy_(CONFIG, bstack1l1ll1l11l_opy_)
    bstack1llll1l1ll_opy_ = logger_utils.configure_logger(CONFIG, bstack1llll1l1ll_opy_)
    if cli.bstack11lll111l_opy_():
        bstack111111l1l_opy_.invoke(Events.CONNECT, bstack1ll1ll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⬏"), bstack1ll1l11_opy_ (u"࠭࠰ࠨ⬐")))
        cli.bstack1lllll11ll_opy_(cli_context.platform_index)
        cli.bstack1l11l1ll1l1_opy_(bstack1lll1lll11_opy_(bstack1111ll111_opy_, CONFIG), cli_context.platform_index, bstack1lll1111_opy_)
        cli.bstack1111l111l_opy_()
        logger.debug(bstack1ll1l11_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⬑") + str(cli_context.platform_index) + bstack1ll1l11_opy_ (u"ࠣࠤ⬒"))
        return # skip all existing operations
    global bstack1l1l11l111_opy_
    global bstack1lll1ll11_opy_
    global bstack1111111l1l_opy_
    global bstack11ll1l1lll_opy_
    global bstack1ll1l11ll1_opy_
    global bstack111lll1111_opy_
    global bstack11l11l11l_opy_
    global bstack1111ll111l_opy_
    global bstack11ll11ll1_opy_
    global bstack111llll1l1_opy_
    global bstack11l11111ll_opy_
    global bstack1lllll1ll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l11l111_opy_ = webdriver.Remote.__init__
        bstack1lll1ll11_opy_ = WebDriver.quit
        bstack11l11l11l_opy_ = WebDriver.close
        bstack1111ll111l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⬓") in CONFIG or bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⬔") in CONFIG) and bstack11l111l111_opy_():
        if bstack11lll1ll_opy_() < version.parse(bstack111lll1l1_opy_):
            logger.error(bstack1ll1ll1l1_opy_.format(bstack11lll1ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1ll1l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⬕")) and callable(getattr(RemoteConnection, bstack1ll1l11_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⬖"))):
                    bstack11ll11ll1_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack11ll11ll1_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l11l111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack111llll1l1_opy_ = Config.getoption
        from _pytest import runner
        bstack11l11111ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1ll1l11_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨ⬗"), bstack1llllll1ll1_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1lllll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ⬘"))
    bstack111l111l1_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ⬙"), {}).get(bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⬚"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack111l11ll_opy_(bstack111lll1l1l_opy_)
if (bstack1llllll111l1_opy_()):
    bstack1ll1111ll11l_opy_()
@error_handler(class_method=False)
def bstack1ll111l1llll_opy_(hook_name, event, bstack11l111l11l1_opy_=None):
    if hook_name not in [bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⬛"), bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⬜"), bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⬝"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⬞"), bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⬟"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⬠"), bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⬡"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ⬢")]:
        return
    node = store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⬣")]
    if hook_name in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⬤"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⬥")]:
        node = store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭⬦")]
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⬧"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⬨")]:
        node = store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⬩")]
    hook_type = bstack1ll1l11ll111_opy_(hook_name)
    if event == bstack1ll1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⬪"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lll1ll1ll1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⬫"): uuid,
            bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⬬"): bstack111ll1ll1l_opy_(),
            bstack1ll1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ⬭"): bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭⬮"),
            bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⬯"): hook_type,
            bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⬰"): hook_name
        }
        store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⬱")].append(uuid)
        bstack1ll1111l1ll1_opy_ = node.nodeid
        if hook_type == bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⬲"):
            if not _1lll1l11l11_opy_.get(bstack1ll1111l1ll1_opy_, None):
                _1lll1l11l11_opy_[bstack1ll1111l1ll1_opy_] = {bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⬳"): []}
            _1lll1l11l11_opy_[bstack1ll1111l1ll1_opy_][bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⬴")].append(bstack1lll1ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⬵")])
        _1lll1l11l11_opy_[bstack1ll1111l1ll1_opy_ + bstack1ll1l11_opy_ (u"ࠩ࠰ࠫ⬶") + hook_name] = bstack1lll1ll1ll1_opy_
        bstack1ll111l11l1l_opy_(node, bstack1lll1ll1ll1_opy_, bstack1ll1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⬷"))
    elif event == bstack1ll1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⬸"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l111l11l1_opy_)
            return
        bstack1llll1ll11l_opy_ = node.nodeid + bstack1ll1l11_opy_ (u"ࠬ࠳ࠧ⬹") + hook_name
        _1lll1l11l11_opy_[bstack1llll1ll11l_opy_][bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⬺")] = bstack111ll1ll1l_opy_()
        bstack1ll111l1l11l_opy_(_1lll1l11l11_opy_[bstack1llll1ll11l_opy_][bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⬻")])
        bstack1ll111l11l1l_opy_(node, _1lll1l11l11_opy_[bstack1llll1ll11l_opy_], bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⬼"), bstack1ll111l1ll1l_opy_=bstack11l111l11l1_opy_)
def bstack1ll111l111ll_opy_():
    global bstack1ll111l11lll_opy_
    if bstack1ll1111ll1_opy_():
        bstack1ll111l11lll_opy_ = bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⬽")
    else:
        bstack1ll111l11lll_opy_ = bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⬾")
@TestHubHandler.bstack1ll11l11llll_opy_
def bstack1ll1111llll1_opy_():
    bstack1ll111l111ll_opy_()
    if cli.is_running():
        try:
            bstack1lll1lll1ll1_opy_(bstack1ll111l1llll_opy_)
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⬿").format(e))
        return
    if bstack11l111l111_opy_():
        global_config = Config.bstack1lllllll1_opy_()
        bstack1ll1l11_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ⭀")
        if global_config.get_property(bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⭁")):
            if CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⭂")) is not None and int(CONFIG[bstack1ll1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⭃")]) > 1:
                bstack1l1ll111l1_opy_(bstack11lll11l11_opy_)
            return
        bstack1l1ll111l1_opy_(bstack11lll11l11_opy_)
    try:
        bstack1lll1lll1ll1_opy_(bstack1ll111l1llll_opy_)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⭄").format(e))
bstack1ll1111llll1_opy_()