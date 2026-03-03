# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11111111l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11l1111l1l_opy_, bstack1l1l11ll1_opy_, update, bstack1ll1ll1ll1_opy_,
                                       bstack111lll11_opy_, bstack11llllll1_opy_, bstack1l1l1l11l1_opy_, bstack1llllllll_opy_,
                                       bstack11l1l11l1l_opy_, bstack11l11ll11l_opy_, bstack11lll1llll_opy_,
                                       bstack1llll1111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1l1ll1ll_opy_)
from browserstack_sdk.bstack1ll111lll1_opy_ import bstack1l1l111l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1111ll1l11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack111ll1l11_opy_, bstack11lll1l1l_opy_, bstack111l1lll1l_opy_, \
    bstack1ll1l1ll11_opy_
from bstack_utils.helper import bstack1lll11l111_opy_, bstack111l1111l11_opy_, bstack1111111l11_opy_, bstack1lllll11l_opy_, bstack1l11l1111ll_opy_, current_time, \
    bstack1111l11ll1l_opy_, \
    bstack1111l1ll1l1_opy_, bstack1ll1lll11_opy_, bstack1l111lll11_opy_, bstack111l111l111_opy_, bstack111l1lll_opy_, Notset, \
    bstack1ll1lll1l1_opy_, time_diff, bstack111l11lll1l_opy_, Result, bstack1111l1ll11l_opy_, bstack111l11ll111_opy_, error_handler, \
    bstack1l111111_opy_, bstack11ll1l11ll_opy_, bstack11l1lll1_opy_, bstack111l1111l1l_opy_
from bstack_utils.bstack1111l1111ll_opy_ import bstack1111l1111l1_opy_
from bstack_utils.messages import bstack1l111lll1l_opy_, bstack111l111lll_opy_, bstack11llll11ll_opy_, bstack11ll1l1l1_opy_, bstack11l1ll1ll1_opy_, \
    bstack1lll111111_opy_, bstack1ll111llll_opy_, bstack1ll1l11l1l_opy_, bstack1111ll1l_opy_, bstack11ll1l111l_opy_, \
    bstack1111ll11_opy_, bstack111l111l_opy_, bstack1lllllll1l_opy_
from bstack_utils.proxy import bstack1111lllll1_opy_, bstack111l11ll11_opy_
from bstack_utils.bstack1l1l11lll_opy_ import bstack1lll1l1lll11_opy_, bstack1lll1l1ll11l_opy_, bstack1lll1l1ll111_opy_, bstack1lll1l1lllll_opy_, \
    bstack1lll1l1ll1l1_opy_, bstack1lll1ll111ll_opy_, bstack1lll1ll111l1_opy_, bstack1l1ll1ll1l_opy_, bstack1lll1l1ll1ll_opy_
from bstack_utils.bstack1llll1ll1_opy_ import bstack1l111l1l1l_opy_
from bstack_utils.session_utils import browserstack_executor_helper, bstack111l11l111_opy_, bstack1l1111l1l_opy_, \
    bstack1l11l1ll11_opy_, bstack111l1l1lll_opy_
from bstack_utils.test_data import TestData
from bstack_utils.bstack1111ll1l1l_opy_ import bstack11lll1ll1_opy_
import bstack_utils.accessibility as bstack11l11l11ll_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.bstack11ll11llll_opy_ import bstack11ll11llll_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1111lll11_opy_
from browserstack_sdk.__init__ import bstack11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1lll_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack111l1llll1_opy_ import bstack111l1llll1_opy_, bstack1l11lll1ll_opy_, bstack11ll1l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11l1llllll1_opy_, bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111l1llll1_opy_ import bstack111l1llll1_opy_, bstack1l11lll1ll_opy_, bstack11ll1l11l1_opy_
bstack11lll1ll_opy_ = None
bstack1llll1llll_opy_ = None
bstack11lll1l11l_opy_ = None
bstack11l11ll1_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack1l1111ll1l_opy_ = None
bstack1l11l1l11_opy_ = None
bstack11ll11lll_opy_ = None
bstack11lll1ll1l_opy_ = None
bstack11ll1l1111_opy_ = None
bstack111ll1llll_opy_ = None
bstack1l111ll1l_opy_ = None
bstack1lll11llll_opy_ = None
bstack111l11111l_opy_ = bstack11ll111_opy_ (u"ࠧࠨ⒖")
CONFIG = {}
bstack1llll11l1_opy_ = False
bstack11lll111ll_opy_ = bstack11ll111_opy_ (u"ࠨࠩ⒗")
bstack11111ll1l_opy_ = bstack11ll111_opy_ (u"ࠩࠪ⒘")
bstack11lll11ll_opy_ = False
bstack1llllllll1_opy_ = []
bstack1l11l1l1_opy_ = bstack111ll1l11_opy_
bstack1ll1ll1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⒙")
bstack1ll11111l1_opy_ = {}
bstack1lll11lll_opy_ = None
bstack1111l11l1_opy_ = False
logger = logger_utils.get_logger(__name__, bstack1l11l1l1_opy_)
store = {
    bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⒚"): []
}
bstack1ll1lll111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11111l11ll_opy_ = {}
current_test_uuid = None
cli_context = bstack11l1llllll1_opy_(
    test_framework_name=bstack1lll1l1lll_opy_[bstack11ll111_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩ⒛")] if bstack111l1lll_opy_() else bstack1lll1l1lll_opy_[bstack11ll111_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭⒜")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l11l111l_opy_(page, bstack1ll1ll1lll_opy_):
    try:
        page.evaluate(bstack11ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ⒝"),
                      bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ⒞") + json.dumps(
                          bstack1ll1ll1lll_opy_) + bstack11ll111_opy_ (u"ࠤࢀࢁࠧ⒟"))
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ⒠"), e)
def bstack11l1ll1ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll111_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ⒡"), bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ⒢") + json.dumps(
            message) + bstack11ll111_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ⒣") + json.dumps(level) + bstack11ll111_opy_ (u"ࠧࡾࡿࠪ⒤"))
    except Exception as e:
        print(bstack11ll111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⒥"), e)
def pytest_configure(config):
    global bstack11lll111ll_opy_
    global CONFIG
    global_config = Config.get_instance()
    config.args = bstack11lll1ll1_opy_.bstack1ll1lll1lll1_opy_(config.args)
    global_config.bstack1ll1llll_opy_(bstack11l1lll1_opy_(config.getoption(bstack11ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⒦"))))
    try:
        logger_utils.bstack11111l1l1l1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.CONNECT, bstack11ll1l11l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⒧"), bstack11ll111_opy_ (u"ࠫ࠵࠭⒨")))
        config = json.loads(os.environ.get(bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦ⒩"), bstack11ll111_opy_ (u"ࠨࡻࡾࠤ⒪")))
        cli.bstack1ll111lllll_opy_(bstack1l111lll11_opy_(bstack11lll111ll_opy_, CONFIG), cli_context.platform_index, bstack1ll1ll1ll1_opy_)
    if cli.bstack1ll11llllll_opy_(bstack1l1llll1l11_opy_):
        cli.bstack1ll1l11l111_opy_()
        logger.debug(bstack11ll111_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⒫") + str(cli_context.platform_index) + bstack11ll111_opy_ (u"ࠣࠤ⒬"))
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.BEFORE_ALL, bstack1l1llll1l1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11ll111_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ⒭"), None)
    if cli.is_running() and when == bstack11ll111_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⒮"):
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.LOG_REPORT, bstack1l1llll1l1l_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11ll111_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⒯"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⒰")))
        if not passed:
            config = json.loads(os.environ.get(bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ⒱"), bstack11ll111_opy_ (u"ࠢࡼࡿࠥ⒲")))
            if bstack1111lll11_opy_.bstack111ll11111_opy_(config):
                bstack1llll1l1l1l1_opy_ = bstack1111lll11_opy_.bstack11llllll_opy_(config)
                if item.execution_count > bstack1llll1l1l1l1_opy_:
                    print(bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡸࡥࡵࡴ࡬ࡩࡸࡀࠠࠨ⒳"), report.nodeid, os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⒴")))
                    bstack1111lll11_opy_.bstack1llllll1ll11_opy_(report.nodeid)
            else:
                print(bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠪ⒵"), report.nodeid, os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⒶ")))
                bstack1111lll11_opy_.bstack1llllll1ll11_opy_(report.nodeid)
        else:
            print(bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࠣࡴࡦࡹࡳࡦࡦ࠽ࠤࠬⒷ"), report.nodeid, os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫⒸ")))
    if cli.is_running():
        if when == bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨⒹ"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.BEFORE_EACH, bstack1l1llll1l1l_opy_.POST, item, call, outcome)
        elif when == bstack11ll111_opy_ (u"ࠣࡥࡤࡰࡱࠨⒺ"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.LOG_REPORT, bstack1l1llll1l1l_opy_.POST, item, call, outcome)
        elif when == bstack11ll111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦⒻ"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.AFTER_EACH, bstack1l1llll1l1l_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack11ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬⒼ"))
    plugins = item.config.getoption(bstack11ll111_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧⒽ"))
    report = outcome.get_result()
    os.environ[bstack11ll111_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨⒾ")] = report.nodeid
    bstack1ll1ll1ll1l1_opy_(item, call, report)
    if bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦⒿ") not in plugins or bstack111l1lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll111_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣⓀ"), None)
    page = getattr(item, bstack11ll111_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢⓁ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1ll1l1111_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1lll11111_opy_(item, report, summary, skipSessionName)
def bstack1ll1ll1l1111_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨⓂ") and report.skipped:
        bstack1lll1l1ll1ll_opy_(report)
    if report.when in [bstack11ll111_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤⓃ"), bstack11ll111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨⓄ")]:
        return
    if not bstack1l11l1111ll_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪⓅ")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫⓆ") + json.dumps(
                    report.nodeid) + bstack11ll111_opy_ (u"ࠧࡾࡿࠪⓇ"))
        os.environ[bstack11ll111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫⓈ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll111_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤⓉ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧⓊ")))
    bstack11l1lll111_opy_ = bstack11ll111_opy_ (u"ࠦࠧⓋ")
    bstack1lll1l1ll1ll_opy_(report)
    if not passed:
        try:
            bstack11l1lll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll111_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧⓌ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1lll111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣⓍ")))
        bstack11l1lll111_opy_ = bstack11ll111_opy_ (u"ࠢࠣⓎ")
        if not passed:
            try:
                bstack11l1lll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣⓏ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l1lll111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ⓐ")
                    + json.dumps(bstack11ll111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦⓑ"))
                    + bstack11ll111_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢⓒ")
                )
            else:
                item._driver.execute_script(
                    bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪⓓ")
                    + json.dumps(str(bstack11l1lll111_opy_))
                    + bstack11ll111_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤⓔ")
                )
        except Exception as e:
            summary.append(bstack11ll111_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧⓕ").format(e))
def bstack1ll1lll1111l_opy_(test_name, error_message):
    try:
        bstack1ll1lll111l1_opy_ = []
        bstack1l111l111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨⓖ"), bstack11ll111_opy_ (u"ࠩ࠳ࠫⓗ"))
        bstack111l11llll_opy_ = {bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨⓘ"): test_name, bstack11ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪⓙ"): error_message, bstack11ll111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫⓚ"): bstack1l111l111_opy_}
        bstack1ll1ll1l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫⓛ"))
        if os.path.exists(bstack1ll1ll1l1lll_opy_):
            with open(bstack1ll1ll1l1lll_opy_) as f:
                bstack1ll1lll111l1_opy_ = json.load(f)
        bstack1ll1lll111l1_opy_.append(bstack111l11llll_opy_)
        with open(bstack1ll1ll1l1lll_opy_, bstack11ll111_opy_ (u"ࠧࡸࠩⓜ")) as f:
            json.dump(bstack1ll1lll111l1_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ⓝ") + str(e))
def bstack1ll1lll11111_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣⓞ"), bstack11ll111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧⓟ")]:
        return
    if (str(skipSessionName).lower() != bstack11ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩⓠ")):
        bstack11l11l111l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll111_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢⓡ")))
    bstack11l1lll111_opy_ = bstack11ll111_opy_ (u"ࠨࠢⓢ")
    bstack1lll1l1ll1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l1lll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll111_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢⓣ").format(e)
                )
        try:
            if passed:
                bstack111l1l1lll_opy_(getattr(item, bstack11ll111_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧⓤ"), None), bstack11ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤⓥ"))
            else:
                error_message = bstack11ll111_opy_ (u"ࠪࠫⓦ")
                if bstack11l1lll111_opy_:
                    bstack11l1ll1ll_opy_(item._page, str(bstack11l1lll111_opy_), bstack11ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥⓧ"))
                    bstack111l1l1lll_opy_(getattr(item, bstack11ll111_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫⓨ"), None), bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨⓩ"), str(bstack11l1lll111_opy_))
                    error_message = str(bstack11l1lll111_opy_)
                else:
                    bstack111l1l1lll_opy_(getattr(item, bstack11ll111_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭⓪"), None), bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ⓫"))
                bstack1ll1lll1111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll111_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨ⓬").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11ll111_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ⓭"), default=bstack11ll111_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ⓮"), help=bstack11ll111_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ⓯"))
    parser.addoption(bstack11ll111_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ⓰"), default=bstack11ll111_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ⓱"), help=bstack11ll111_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ⓲"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll111_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ⓳"), action=bstack11ll111_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ⓴"), default=bstack11ll111_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ⓵"),
                         help=bstack11ll111_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦ⓶"))
def bstack1111ll111l_opy_(log):
    if not (log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⓷")] and log[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⓸")].strip()):
        return
    active = bstack1111l1lll1_opy_()
    log = {
        bstack11ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⓹"): log[bstack11ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⓺")],
        bstack11ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⓻"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"ࠫ࡟࠭⓼"),
        bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⓽"): log[bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⓾")],
    }
    if active:
        if active[bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬ⓿")] == bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰ࠭─"):
            log[bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ━")] = active[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ│")]
        elif active[bstack11ll111_opy_ (u"ࠫࡹࡿࡰࡦࠩ┃")] == bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࠪ┄"):
            log[bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┅")] = active[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ┆")]
    TestHubHandler.bstack1ll11l1ll_opy_([log])
def bstack1111l1lll1_opy_():
    if len(store[bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ┇")]) > 0 and store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭┈")][-1]:
        return {
            bstack11ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨ┉"): bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ┊"),
            bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┋"): store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ┌")][-1]
        }
    if store.get(bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ┍"), None):
        return {
            bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭┎"): bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࠧ┏"),
            bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ┐"): store[bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ┑")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.INIT_TEST, bstack1l1llll1l1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.INIT_TEST, bstack1l1llll1l1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1ll1lll11l11_opy_ = True
        bstack11l1llll1_opy_ = bstack11l11l11ll_opy_.bstack1l11ll1111_opy_(bstack1111l1ll1l1_opy_(item.own_markers))
        if not cli.bstack1ll11llllll_opy_(bstack1l1llll1l11_opy_):
            item._a11y_test_case = bstack11l1llll1_opy_
            if bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ┒"), None):
                driver = getattr(item, bstack11ll111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ┓"), None)
                item._a11y_started = bstack11l11l11ll_opy_.bstack11lll111l1_opy_(driver, bstack11l1llll1_opy_)
        if not TestHubHandler.on() or bstack1ll1ll1l1l1l_opy_ != bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ└"):
            return
        global current_test_uuid #, bstack1111l1l11l_opy_
        bstack111111l1ll_opy_ = {
            bstack11ll111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭┕"): uuid4().__str__(),
            bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭┖"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"ࠪ࡞ࠬ┗")
        }
        current_test_uuid = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ┘")]
        store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ┙")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ┚")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11111l11ll_opy_[item.nodeid] = {**_11111l11ll_opy_[item.nodeid], **bstack111111l1ll_opy_}
        bstack1ll1lll1ll11_opy_(item, _11111l11ll_opy_[item.nodeid], bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ┛"))
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ├"), str(err))
def pytest_runtest_setup(item):
    store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭┝")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.BEFORE_EACH, bstack1l1llll1l1l_opy_.PRE, item, bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ┞"))
    if bstack1111lll11_opy_.bstack1llllll11l11_opy_():
            bstack1ll1ll1l1ll1_opy_ = bstack11ll111_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡦࡹࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ┟")
            logger.error(bstack1ll1ll1l1ll1_opy_)
            bstack111111l1ll_opy_ = {
                bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ┠"): uuid4().__str__(),
                bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ┡"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"࡛ࠧࠩ┢"),
                bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭┣"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"ࠩ࡝ࠫ┤"),
                bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ┥"): bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ┦"),
                bstack11ll111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ┧"): bstack1ll1ll1l1ll1_opy_,
                bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ┨"): [],
                bstack11ll111_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ┩"): []
            }
            bstack1ll1lll1ll11_opy_(item, bstack111111l1ll_opy_, bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ┪"))
            pytest.skip(bstack1ll1ll1l1ll1_opy_)
            return # skip all existing operations
    global bstack1ll1lll111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l111l111_opy_():
        atexit.register(bstack1l11l11lll_opy_)
        if not bstack1ll1lll111ll_opy_:
            try:
                bstack1ll1lll11l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l1111l1l_opy_():
                    bstack1ll1lll11l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1lll11l1l_opy_:
                    signal.signal(s, bstack1lllll1ll11_opy_)
                bstack1ll1lll111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ┫") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll1l1lll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ┬")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack111111l1ll_opy_ = {
            bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ┭"): uuid,
            bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ┮"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"࡚࠭ࠨ┯"),
            bstack11ll111_opy_ (u"ࠧࡵࡻࡳࡩࠬ┰"): bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰ࠭┱"),
            bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ┲"): bstack11ll111_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ┳"),
            bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ┴"): bstack11ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ┵")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ┶")] = item
        store[bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ┷")] = [uuid]
        if not _11111l11ll_opy_.get(item.nodeid, None):
            _11111l11ll_opy_[item.nodeid] = {bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ┸"): [], bstack11ll111_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ┹"): []}
        _11111l11ll_opy_[item.nodeid][bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ┺")].append(bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ┻")])
        _11111l11ll_opy_[item.nodeid + bstack11ll111_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ┼")] = bstack111111l1ll_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1ll1ll11l_opy_(item, bstack111111l1ll_opy_, bstack11ll111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ┽"))
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ┾"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.AFTER_EACH, bstack1l1llll1l1l_opy_.PRE, item, bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ┿"))
        return # skip all existing operations
    try:
        global bstack1ll11111l1_opy_
        bstack1l111l111_opy_ = 0
        if bstack11lll11ll_opy_ is True:
            bstack1l111l111_opy_ = int(os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ╀")))
        if bstack1ll1111l_opy_.bstack1lll11ll1l_opy_() == bstack11ll111_opy_ (u"ࠥࡸࡷࡻࡥࠣ╁"):
            if bstack1ll1111l_opy_.bstack11lllllll_opy_() == bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ╂"):
                bstack1ll1lll1l111_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ╃"), None)
                bstack1ll1l111l1_opy_ = bstack1ll1lll1l111_opy_ + bstack11ll111_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤ╄")
                driver = getattr(item, bstack11ll111_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ╅"), None)
                bstack11l1ll11l_opy_ = getattr(item, bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭╆"), None)
                bstack1ll11ll1l_opy_ = getattr(item, bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ╇"), None)
                PercySDK.screenshot(driver, bstack1ll1l111l1_opy_, bstack11l1ll11l_opy_=bstack11l1ll11l_opy_, bstack1ll11ll1l_opy_=bstack1ll11ll1l_opy_, bstack11l111l1l_opy_=bstack1l111l111_opy_)
        if not cli.bstack1ll11llllll_opy_(bstack1l1llll1l11_opy_):
            if getattr(item, bstack11ll111_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ╈"), False):
                bstack1l1l111l11_opy_.bstack1ll11llll_opy_(getattr(item, bstack11ll111_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ╉"), None), bstack1ll11111l1_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack111111l1ll_opy_ = {
            bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ╊"): uuid4().__str__(),
            bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ╋"): bstack1111111l11_opy_().isoformat() + bstack11ll111_opy_ (u"࡛ࠧࠩ╌"),
            bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭╍"): bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ╎"),
            bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭╏"): bstack11ll111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ═"),
            bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ║"): bstack11ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ╒")
        }
        _11111l11ll_opy_[item.nodeid + bstack11ll111_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ╓")] = bstack111111l1ll_opy_
        bstack1ll1ll1ll11l_opy_(item, bstack111111l1ll_opy_, bstack11ll111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ╔"))
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨ╕"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lll1l1lllll_opy_(fixturedef.argname):
        store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ╖")] = request.node
    elif bstack1lll1l1ll1l1_opy_(fixturedef.argname):
        store[bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ╗")] = request.node
    if not TestHubHandler.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.SETUP_FIXTURE, bstack1l1llll1l1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.SETUP_FIXTURE, bstack1l1llll1l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.SETUP_FIXTURE, bstack1l1llll1l1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.SETUP_FIXTURE, bstack1l1llll1l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack11ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ╘"): fixturedef.argname,
            bstack11ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭╙"): bstack1111l11ll1l_opy_(outcome),
            bstack11ll111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ╚"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ╛")]
        if not _11111l11ll_opy_.get(current_test_item.nodeid, None):
            _11111l11ll_opy_[current_test_item.nodeid] = {bstack11ll111_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ╜"): []}
        _11111l11ll_opy_[current_test_item.nodeid][bstack11ll111_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ╝")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ╞"), str(err))
if bstack111l1lll_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.STEP, bstack1l1llll1l1l_opy_.PRE, request, step)
            return
        try:
            _11111l11ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ╟")].bstack11l11111l_opy_(id(step))
        except Exception as err:
            print(bstack11ll111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ╠"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.STEP, bstack1l1llll1l1l_opy_.POST, request, step, exception)
            return
        try:
            _11111l11ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ╡")].bstack1111l11lll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ╢"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.STEP, bstack1l1llll1l1l_opy_.POST, request, step)
            return
        try:
            test_data: TestData = _11111l11ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ╣")]
            test_data.bstack1111l11lll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ╤"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1ll1l1l1l_opy_
        try:
            if not TestHubHandler.on() or bstack1ll1ll1l1l1l_opy_ != bstack11ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ╥"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ╦"), None)
            if not _11111l11ll_opy_.get(request.node.nodeid, None):
                _11111l11ll_opy_[request.node.nodeid] = {}
            test_data = TestData.bstack1lll11ll11l1_opy_(
                scenario, feature, request.node,
                name=bstack1lll1ll111ll_opy_(request.node, scenario),
                started_at=current_time(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ╧"),
                tags=bstack1lll1ll111l1_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {}
            )
            _11111l11ll_opy_[request.node.nodeid][bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ╨")] = test_data
            bstack1ll1lll11lll_opy_(test_data.uuid)
            TestHubHandler.send_run_event(bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ╩"), test_data)
        except Exception as err:
            print(bstack11ll111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ╪"), str(err))
def bstack1ll1ll1l111l_opy_(bstack1111l11ll1_opy_):
    if bstack1111l11ll1_opy_ in store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ╫")]:
        store[bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ╬")].remove(bstack1111l11ll1_opy_)
def bstack1ll1lll11lll_opy_(test_uuid):
    store[bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ╭")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1lll11111l1l_opy_
def bstack1ll1ll1ll1l1_opy_(item, call, report):
    logger.debug(bstack11ll111_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ╮"))
    global bstack1ll1ll1l1l1l_opy_
    bstack11lll111_opy_ = current_time()
    if hasattr(report, bstack11ll111_opy_ (u"ࠧࡴࡶࡲࡴࠬ╯")):
        bstack11lll111_opy_ = bstack1111l1ll11l_opy_(report.stop)
    elif hasattr(report, bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ╰")):
        bstack11lll111_opy_ = bstack1111l1ll11l_opy_(report.start)
    try:
        if getattr(report, bstack11ll111_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ╱"), bstack11ll111_opy_ (u"ࠪࠫ╲")) == bstack11ll111_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ╳"):
            logger.debug(bstack11ll111_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ╴").format(getattr(report, bstack11ll111_opy_ (u"࠭ࡷࡩࡧࡱࠫ╵"), bstack11ll111_opy_ (u"ࠧࠨ╶")).__str__(), bstack1ll1ll1l1l1l_opy_))
            if bstack1ll1ll1l1l1l_opy_ == bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ╷"):
                _11111l11ll_opy_[item.nodeid][bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ╸")] = bstack11lll111_opy_
                bstack1ll1lll1ll11_opy_(item, _11111l11ll_opy_[item.nodeid], bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ╹"), report, call)
                store[bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ╺")] = None
            elif bstack1ll1ll1l1l1l_opy_ == bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ╻"):
                test_data = _11111l11ll_opy_[item.nodeid][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ╼")]
                test_data.set(hooks=_11111l11ll_opy_[item.nodeid].get(bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭╽"), []))
                exception, bstack1111ll1lll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1111ll1lll_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll111_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧ╾"), bstack11ll111_opy_ (u"ࠩࠪ╿"))]
                test_data.stop(time=bstack11lll111_opy_, result=Result(result=getattr(report, bstack11ll111_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ▀"), bstack11ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ▁")), exception=exception, bstack1111ll1lll_opy_=bstack1111ll1lll_opy_))
                TestHubHandler.send_run_event(bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ▂"), _11111l11ll_opy_[item.nodeid][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ▃")])
        elif getattr(report, bstack11ll111_opy_ (u"ࠧࡸࡪࡨࡲࠬ▄"), bstack11ll111_opy_ (u"ࠨࠩ▅")) in [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ▆"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ▇")]:
            logger.debug(bstack11ll111_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭█").format(getattr(report, bstack11ll111_opy_ (u"ࠬࡽࡨࡦࡰࠪ▉"), bstack11ll111_opy_ (u"࠭ࠧ▊")).__str__(), bstack1ll1ll1l1l1l_opy_))
            bstack1111l1l111_opy_ = item.nodeid + bstack11ll111_opy_ (u"ࠧ࠮ࠩ▋") + getattr(report, bstack11ll111_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭▌"), bstack11ll111_opy_ (u"ࠩࠪ▍"))
            if getattr(report, bstack11ll111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ▎"), False):
                hook_type = bstack11ll111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ▏") if getattr(report, bstack11ll111_opy_ (u"ࠬࡽࡨࡦࡰࠪ▐"), bstack11ll111_opy_ (u"࠭ࠧ░")) == bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭▒") else bstack11ll111_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ▓")
                _11111l11ll_opy_[bstack1111l1l111_opy_] = {
                    bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ▔"): uuid4().__str__(),
                    bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ▕"): bstack11lll111_opy_,
                    bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ▖"): hook_type
                }
            _11111l11ll_opy_[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ▗")] = bstack11lll111_opy_
            bstack1ll1ll1l111l_opy_(_11111l11ll_opy_[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ▘")])
            bstack1ll1ll1ll11l_opy_(item, _11111l11ll_opy_[bstack1111l1l111_opy_], bstack11ll111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ▙"), report, call)
            if getattr(report, bstack11ll111_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭▚"), bstack11ll111_opy_ (u"ࠩࠪ▛")) == bstack11ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ▜"):
                if getattr(report, bstack11ll111_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ▝"), bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ▞")) == bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭▟"):
                    bstack111111l1ll_opy_ = {
                        bstack11ll111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ■"): uuid4().__str__(),
                        bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ□"): current_time(),
                        bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ▢"): current_time()
                    }
                    _11111l11ll_opy_[item.nodeid] = {**_11111l11ll_opy_[item.nodeid], **bstack111111l1ll_opy_}
                    bstack1ll1lll1ll11_opy_(item, _11111l11ll_opy_[item.nodeid], bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ▣"))
                    bstack1ll1lll1ll11_opy_(item, _11111l11ll_opy_[item.nodeid], bstack11ll111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭▤"), report, call)
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ▥"), str(err))
def bstack1ll1ll1l11ll_opy_(test, bstack111111l1ll_opy_, result=None, call=None, bstack11l1l1llll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    test_data = {
        bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ▦"): bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ▧")],
        bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭▨"): bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࠧ▩"),
        bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ▪"): test.name,
        bstack11ll111_opy_ (u"ࠫࡧࡵࡤࡺࠩ▫"): {
            bstack11ll111_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ▬"): bstack11ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭▭"),
            bstack11ll111_opy_ (u"ࠧࡤࡱࡧࡩࠬ▮"): inspect.getsource(test.obj)
        },
        bstack11ll111_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ▯"): test.name,
        bstack11ll111_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ▰"): test.name,
        bstack11ll111_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ▱"): bstack11lll1ll1_opy_.bstack111111ll1l_opy_(test),
        bstack11ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ▲"): file_path,
        bstack11ll111_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ△"): file_path,
        bstack11ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭▴"): bstack11ll111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ▵"),
        bstack11ll111_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭▶"): file_path,
        bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭▷"): bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ▸")],
        bstack11ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ▹"): bstack11ll111_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ►"),
        bstack11ll111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ▻"): {
            bstack11ll111_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ▼"): test.nodeid
        },
        bstack11ll111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭▽"): bstack1111l1ll1l1_opy_(test.own_markers)
    }
    if bstack11l1l1llll_opy_ in [bstack11ll111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ▾"), bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ▿")]:
        test_data[bstack11ll111_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ◀")] = {
            bstack11ll111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ◁"): bstack111111l1ll_opy_.get(bstack11ll111_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ◂"), [])
        }
    if bstack11l1l1llll_opy_ == bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ◃"):
        test_data[bstack11ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ◄")] = bstack11ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ◅")
        test_data[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ◆")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ◇")]
        test_data[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ◈")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ◉")]
    if result:
        test_data[bstack11ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ◊")] = result.outcome
        test_data[bstack11ll111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ○")] = result.duration * 1000
        test_data[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ◌")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ◍")]
        if result.failed:
            test_data[bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ◎")] = TestHubHandler.bstack1lll1ll11ll_opy_(call.excinfo.typename)
            test_data[bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭●")] = TestHubHandler.bstack1lll11111lll_opy_(call.excinfo, result)
        test_data[bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ◐")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭◑")]
    if outcome:
        test_data[bstack11ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ◒")] = bstack1111l11ll1l_opy_(outcome)
        test_data[bstack11ll111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ◓")] = 0
        test_data[bstack11ll111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ◔")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ◕")]
        if test_data[bstack11ll111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ◖")] == bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭◗"):
            test_data[bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭◘")] = bstack11ll111_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ◙")  # bstack1ll1ll1lllll_opy_
            test_data[bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ◚")] = [{bstack11ll111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭◛"): [bstack11ll111_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ◜")]}]
        test_data[bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ◝")] = bstack111111l1ll_opy_[bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ◞")]
    return test_data
def bstack1ll1lll1l1ll_opy_(test, bstack11111ll1l1_opy_, bstack11l1l1llll_opy_, result, call, outcome, bstack1ll1ll1lll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ◟")]
    hook_name = bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ◠")]
    hook_data = {
        bstack11ll111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ◡"): bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ◢")],
        bstack11ll111_opy_ (u"ࠫࡹࡿࡰࡦࠩ◣"): bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ◤"),
        bstack11ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ◥"): bstack11ll111_opy_ (u"ࠧࡼࡿࠪ◦").format(bstack1lll1l1ll11l_opy_(hook_name)),
        bstack11ll111_opy_ (u"ࠨࡤࡲࡨࡾ࠭◧"): {
            bstack11ll111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ◨"): bstack11ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ◩"),
            bstack11ll111_opy_ (u"ࠫࡨࡵࡤࡦࠩ◪"): None
        },
        bstack11ll111_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ◫"): test.name,
        bstack11ll111_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭◬"): bstack11lll1ll1_opy_.bstack111111ll1l_opy_(test, hook_name),
        bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ◭"): file_path,
        bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ◮"): file_path,
        bstack11ll111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ◯"): bstack11ll111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ◰"),
        bstack11ll111_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ◱"): file_path,
        bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ◲"): bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ◳")],
        bstack11ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ◴"): bstack11ll111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ◵") if bstack1ll1ll1l1l1l_opy_ == bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭◶") else bstack11ll111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ◷"),
        bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ◸"): hook_type
    }
    bstack1l1l1l111ll_opy_ = bstack1111l11111_opy_(_11111l11ll_opy_.get(test.nodeid, None))
    if bstack1l1l1l111ll_opy_:
        hook_data[bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ◹")] = bstack1l1l1l111ll_opy_
    if result:
        hook_data[bstack11ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭◺")] = result.outcome
        hook_data[bstack11ll111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ◻")] = result.duration * 1000
        hook_data[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭◼")] = bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ◽")]
        if result.failed:
            hook_data[bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ◾")] = TestHubHandler.bstack1lll1ll11ll_opy_(call.excinfo.typename)
            hook_data[bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ◿")] = TestHubHandler.bstack1lll11111lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ☀")] = bstack1111l11ll1l_opy_(outcome)
        hook_data[bstack11ll111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ☁")] = 100
        hook_data[bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ☂")] = bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭☃")]
        if hook_data[bstack11ll111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ☄")] == bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ★"):
            hook_data[bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ☆")] = bstack11ll111_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭☇")  # bstack1ll1ll1lllll_opy_
            hook_data[bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ☈")] = [{bstack11ll111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ☉"): [bstack11ll111_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ☊")]}]
    if bstack1ll1ll1lll1l_opy_:
        hook_data[bstack11ll111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ☋")] = bstack1ll1ll1lll1l_opy_.result
        hook_data[bstack11ll111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ☌")] = time_diff(bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ☍")], bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ☎")])
        hook_data[bstack11ll111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ☏")] = bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ☐")]
        if hook_data[bstack11ll111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ☑")] == bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ☒"):
            hook_data[bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ☓")] = TestHubHandler.bstack1lll1ll11ll_opy_(bstack1ll1ll1lll1l_opy_.exception_type)
            hook_data[bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ☔")] = [{bstack11ll111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ☕"): bstack111l11lll1l_opy_(bstack1ll1ll1lll1l_opy_.exception)}]
    return hook_data
def bstack1ll1lll1ll11_opy_(test, bstack111111l1ll_opy_, bstack11l1l1llll_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11ll111_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ☖").format(bstack11l1l1llll_opy_))
    test_data = bstack1ll1ll1l11ll_opy_(test, bstack111111l1ll_opy_, result, call, bstack11l1l1llll_opy_, outcome)
    driver = getattr(test, bstack11ll111_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ☗"), None)
    if bstack11l1l1llll_opy_ == bstack11ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ☘") and driver:
        test_data[bstack11ll111_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ☙")] = TestHubHandler.bstack1111l11l1l_opy_(driver)
    if bstack11l1l1llll_opy_ == bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ☚"):
        bstack11l1l1llll_opy_ = bstack11ll111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭☛")
    bstack11111111ll_opy_ = {
        bstack11ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ☜"): bstack11l1l1llll_opy_,
        bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ☝"): test_data
    }
    TestHubHandler.bstack11ll11111_opy_(bstack11111111ll_opy_)
    if bstack11l1l1llll_opy_ == bstack11ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ☞"):
        threading.current_thread().bstackTestMeta = {bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ☟"): bstack11ll111_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ☠")}
    elif bstack11l1l1llll_opy_ == bstack11ll111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ☡"):
        threading.current_thread().bstackTestMeta = {bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ☢"): getattr(result, bstack11ll111_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭☣"), bstack11ll111_opy_ (u"࠭ࠧ☤"))}
def bstack1ll1ll1ll11l_opy_(test, bstack111111l1ll_opy_, bstack11l1l1llll_opy_, result=None, call=None, outcome=None, bstack1ll1ll1lll1l_opy_=None):
    logger.debug(bstack11ll111_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ☥").format(bstack11l1l1llll_opy_))
    hook_data = bstack1ll1lll1l1ll_opy_(test, bstack111111l1ll_opy_, bstack11l1l1llll_opy_, result, call, outcome, bstack1ll1ll1lll1l_opy_)
    bstack11111111ll_opy_ = {
        bstack11ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ☦"): bstack11l1l1llll_opy_,
        bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ☧"): hook_data
    }
    TestHubHandler.bstack11ll11111_opy_(bstack11111111ll_opy_)
def bstack1111l11111_opy_(bstack111111l1ll_opy_):
    if not bstack111111l1ll_opy_:
        return None
    if bstack111111l1ll_opy_.get(bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭☨"), None):
        return getattr(bstack111111l1ll_opy_[bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ☩")], bstack11ll111_opy_ (u"ࠬࡻࡵࡪࡦࠪ☪"), None)
    return bstack111111l1ll_opy_.get(bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ☫"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.LOG, bstack1l1llll1l1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_.LOG, bstack1l1llll1l1l_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not TestHubHandler.on():
            return
        places = [bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭☬"), bstack11ll111_opy_ (u"ࠨࡥࡤࡰࡱ࠭☭"), bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ☮")]
        logs = []
        for bstack1ll1ll1lll11_opy_ in places:
            records = caplog.get_records(bstack1ll1ll1lll11_opy_)
            bstack1ll1ll1llll1_opy_ = bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ☯") if bstack1ll1ll1lll11_opy_ == bstack11ll111_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ☰") else bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☱")
            bstack1ll1ll1ll1ll_opy_ = request.node.nodeid + (bstack11ll111_opy_ (u"࠭ࠧ☲") if bstack1ll1ll1lll11_opy_ == bstack11ll111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ☳") else bstack11ll111_opy_ (u"ࠨ࠯ࠪ☴") + bstack1ll1ll1lll11_opy_)
            test_uuid = bstack1111l11111_opy_(_11111l11ll_opy_.get(bstack1ll1ll1ll1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l11ll111_opy_(record.message):
                    continue
                logs.append({
                    bstack11ll111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ☵"): bstack111l1111l11_opy_(record.created).isoformat() + bstack11ll111_opy_ (u"ࠪ࡞ࠬ☶"),
                    bstack11ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ☷"): record.levelname,
                    bstack11ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭☸"): record.message,
                    bstack1ll1ll1llll1_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1ll11l1ll_opy_(logs)
    except Exception as err:
        print(bstack11ll111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ☹"), str(err))
def bstack111l1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1111l11l1_opy_
    bstack1l1111l1ll_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ☺"), None) and bstack1lll11l111_opy_(
            threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ☻"), None)
    bstack11ll11l1l1_opy_ = getattr(driver, bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ☼"), None) != None and getattr(driver, bstack11ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ☽"), None) == True
    if sequence == bstack11ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ☾") and driver != None:
      if not bstack1111l11l1_opy_ and bstack1l11l1111ll_opy_() and bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ☿") in CONFIG and CONFIG[bstack11ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭♀")] == True and bstack11ll11llll_opy_.bstack111l1111l1_opy_(driver_command) and (bstack11ll11l1l1_opy_ or bstack1l1111l1ll_opy_) and not bstack1l1l1ll1ll_opy_(args):
        try:
          bstack1111l11l1_opy_ = True
          logger.debug(bstack11ll111_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ♁").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭♂").format(str(err)))
        bstack1111l11l1_opy_ = False
    if sequence == bstack11ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ♃"):
        if driver_command == bstack11ll111_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ♄"):
            TestHubHandler.bstack1lll11ll1_opy_({
                bstack11ll111_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ♅"): response[bstack11ll111_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ♆")],
                bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭♇"): store[bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ♈")]
            })
def bstack1l11l11lll_opy_():
    global bstack1llllllll1_opy_
    logger_utils.bstack11l1l111l_opy_()
    logging.shutdown()
    TestHubHandler.bstack1111l111ll_opy_()
    for driver in bstack1llllllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllll1ll11_opy_(*args):
    global bstack1llllllll1_opy_
    TestHubHandler.bstack1111l111ll_opy_()
    for driver in bstack1llllllll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll11l11_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1ll1lll111_opy_(self, *args, **kwargs):
    bstack1l111lll1_opy_ = bstack11lll1ll_opy_(self, *args, **kwargs)
    bstack1llll11l_opy_ = getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ♉"), None)
    if bstack1llll11l_opy_ and bstack1llll11l_opy_.get(bstack11ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ♊"), bstack11ll111_opy_ (u"ࠪࠫ♋")) == bstack11ll111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ♌"):
        TestHubHandler.bstack1l1ll1l11_opy_(self)
    return bstack1l111lll1_opy_
@measure(event_name=EVENTS.bstack1l1lll1l_opy_, stage=STAGE.bstack11ll1ll11l_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1l1ll111l1_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.get_instance()
    if global_config.get_property(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ♍")):
        return
    global_config.bstack111lll11ll_opy_(bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ♎"), True)
    global bstack111l11111l_opy_
    global bstack1l111l11l1_opy_
    bstack111l11111l_opy_ = framework_name
    logger.info(bstack111l111l_opy_.format(bstack111l11111l_opy_.split(bstack11ll111_opy_ (u"ࠧ࠮ࠩ♏"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l11l1111ll_opy_():
            Service.start = bstack1l1l1l11l1_opy_
            Service.stop = bstack1llllllll_opy_
            webdriver.Remote.get = bstack1lll11l1_opy_
            webdriver.Remote.__init__ = bstack1ll111ll11_opy_
            if not isinstance(os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ♐")), str):
                return
            WebDriver.quit = bstack11llll1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1ll1lll111_opy_
        bstack1l111l11l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11ll111_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ♑")):
        bstack1l111l11l1_opy_ = eval(os.environ.get(bstack11ll111_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ♒")))
    if not bstack1l111l11l1_opy_:
        bstack11l11ll11l_opy_(bstack11ll111_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ♓"), bstack1111ll11_opy_)
    if bstack1ll11ll1l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11ll111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭♔")) and callable(getattr(RemoteConnection, bstack11ll111_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ♕"))):
                RemoteConnection._get_proxy_url = bstack11lll1l1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11lll1l1_opy_
        except Exception as e:
            logger.error(bstack1lll111111_opy_.format(str(e)))
    if bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ♖") in str(framework_name).lower():
        if not bstack1l11l1111ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111lll11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11llllll1_opy_
            Config.getoption = bstack11l11l1l11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111lllll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack11llll1l_opy_(self):
    global bstack111l11111l_opy_
    global bstack1lll1l1l_opy_
    global bstack1llll1llll_opy_
    try:
        if bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ♗") in bstack111l11111l_opy_ and self.session_id != None and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭♘"), bstack11ll111_opy_ (u"ࠪࠫ♙")) != bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ♚"):
            bstack1lll1ll11_opy_ = bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ♛") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭♜")
            bstack11ll1l11ll_opy_(logger, True)
            if os.environ.get(bstack11ll111_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ♝"), None):
                self.execute_script(
                    bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭♞") + json.dumps(
                        os.environ.get(bstack11ll111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ♟"))) + bstack11ll111_opy_ (u"ࠪࢁࢂ࠭♠"))
            if self != None:
                bstack1l11l1ll11_opy_(self, bstack1lll1ll11_opy_, bstack11ll111_opy_ (u"ࠫ࠱ࠦࠧ♡").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll11llllll_opy_(bstack1l1llll1l11_opy_):
            item = store.get(bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ♢"), None)
            if item is not None and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ♣"), None):
                bstack1l1l111l11_opy_.bstack1ll11llll_opy_(self, bstack1ll11111l1_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll111_opy_ (u"ࠧࠨ♤")
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ♥") + str(e))
    bstack1llll1llll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11ll111lll_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1ll111ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll1l1l_opy_
    global bstack1lll11lll_opy_
    global bstack11lll11ll_opy_
    global bstack111l11111l_opy_
    global bstack11lll1ll_opy_
    global bstack1llllllll1_opy_
    global bstack11lll111ll_opy_
    global bstack11111ll1l_opy_
    global bstack1ll11111l1_opy_
    CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ♦")] = str(bstack111l11111l_opy_) + str(__version__)
    command_executor = bstack1l111lll11_opy_(bstack11lll111ll_opy_, CONFIG)
    logger.debug(bstack11ll1l1l1_opy_.format(command_executor))
    proxy = bstack1llll1111_opy_(CONFIG, proxy)
    bstack1l111l111_opy_ = 0
    try:
        if bstack11lll11ll_opy_ is True:
            bstack1l111l111_opy_ = int(os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ♧")))
    except:
        bstack1l111l111_opy_ = 0
    bstack1l11l11111_opy_ = bstack11l1111l1l_opy_(CONFIG, bstack1l111l111_opy_)
    logger.debug(bstack1ll1l11l1l_opy_.format(str(bstack1l11l11111_opy_)))
    bstack1ll11111l1_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ♨"))[bstack1l111l111_opy_]
    if bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ♩") in CONFIG and CONFIG[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ♪")]:
        bstack1l1111l1l_opy_(bstack1l11l11111_opy_, bstack11111ll1l_opy_)
    if bstack11l11l11ll_opy_.bstack11l1111ll_opy_(CONFIG, bstack1l111l111_opy_) and bstack11l11l11ll_opy_.bstack1l1lllll1l_opy_(bstack1l11l11111_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll11llllll_opy_(bstack1l1llll1l11_opy_):
            bstack11l11l11ll_opy_.set_capabilities(bstack1l11l11111_opy_, CONFIG)
    if desired_capabilities:
        bstack111lll1lll_opy_ = bstack1l1l11ll1_opy_(desired_capabilities)
        bstack111lll1lll_opy_[bstack11ll111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ♫")] = bstack1ll1lll1l1_opy_(CONFIG)
        bstack1lllllll11_opy_ = bstack11l1111l1l_opy_(bstack111lll1lll_opy_)
        if bstack1lllllll11_opy_:
            bstack1l11l11111_opy_ = update(bstack1lllllll11_opy_, bstack1l11l11111_opy_)
        desired_capabilities = None
    if options:
        bstack11l1l11l1l_opy_(options, bstack1l11l11111_opy_)
    if not options:
        options = bstack1ll1ll1ll1_opy_(bstack1l11l11111_opy_)
    if proxy and bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ♬")):
        options.proxy(proxy)
    if options and bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ♭")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1lll11_opy_() < version.parse(bstack11ll111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ♮")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11l11111_opy_)
    logger.info(bstack11llll11ll_opy_)
    bstack11111111l_opy_.end(EVENTS.bstack1l1lll1l_opy_.value, EVENTS.bstack1l1lll1l_opy_.value + bstack11ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ♯"),
                               EVENTS.bstack1l1lll1l_opy_.value + bstack11ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ♰"), True, None)
    try:
        if bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭♱")):
            bstack11lll1ll_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭♲")):
            bstack11lll1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ♳")):
            bstack11lll1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack11lll1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11ll111111_opy_:
        logger.error(bstack1lllllll1l_opy_.format(bstack11ll111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨ♴"), str(bstack11ll111111_opy_)))
        raise bstack11ll111111_opy_
    try:
        bstack1ll1111l11_opy_ = bstack11ll111_opy_ (u"ࠪࠫ♵")
        if bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ♶")):
            bstack1ll1111l11_opy_ = self.caps.get(bstack11ll111_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ♷"))
        else:
            bstack1ll1111l11_opy_ = self.capabilities.get(bstack11ll111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ♸"))
        if bstack1ll1111l11_opy_:
            bstack1l111111_opy_(bstack1ll1111l11_opy_)
            if bstack1ll1lll11_opy_() <= version.parse(bstack11ll111_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ♹")):
                self.command_executor._url = bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ♺") + bstack11lll111ll_opy_ + bstack11ll111_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ♻")
            else:
                self.command_executor._url = bstack11ll111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ♼") + bstack1ll1111l11_opy_ + bstack11ll111_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ♽")
            logger.debug(bstack111l111lll_opy_.format(bstack1ll1111l11_opy_))
        else:
            logger.debug(bstack1l111lll1l_opy_.format(bstack11ll111_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ♾")))
    except Exception as e:
        logger.debug(bstack1l111lll1l_opy_.format(e))
    bstack1lll1l1l_opy_ = self.session_id
    if bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭♿") in bstack111l11111l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⚀"), None)
        if item:
            bstack1ll1ll1l1l11_opy_ = getattr(item, bstack11ll111_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭⚁"), False)
            if not getattr(item, bstack11ll111_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⚂"), None) and bstack1ll1ll1l1l11_opy_:
                setattr(store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⚃")], bstack11ll111_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⚄"), self)
        bstack1llll11l_opy_ = getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⚅"), None)
        if bstack1llll11l_opy_ and bstack1llll11l_opy_.get(bstack11ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⚆"), bstack11ll111_opy_ (u"ࠧࠨ⚇")) == bstack11ll111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⚈"):
            TestHubHandler.bstack1l1ll1l11_opy_(self)
    bstack1llllllll1_opy_.append(self)
    if bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⚉") in CONFIG and bstack11ll111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⚊") in CONFIG[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⚋")][bstack1l111l111_opy_]:
        bstack1lll11lll_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⚌")][bstack1l111l111_opy_][bstack11ll111_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⚍")]
    logger.debug(bstack11ll1l111l_opy_.format(bstack1lll1l1l_opy_))
@measure(event_name=EVENTS.bstack1l1l1l1l1l_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=bstack1lll11lll_opy_)
def bstack1lll11l1_opy_(self, url):
    global bstack11lll1ll1l_opy_
    global CONFIG
    try:
        bstack111l11l111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1111ll1l_opy_.format(str(err)))
    try:
        bstack11lll1ll1l_opy_(self, url)
    except Exception as e:
        try:
            bstack111lllll1l_opy_ = str(e)
            if any(err_msg in bstack111lllll1l_opy_ for err_msg in bstack111l1lll1l_opy_):
                bstack111l11l111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1111ll1l_opy_.format(str(err)))
        raise e
def bstack111ll111l_opy_(item, when):
    global bstack1l111ll1l_opy_
    try:
        bstack1l111ll1l_opy_(item, when)
    except Exception as e:
        pass
def bstack111lllll1_opy_(item, call, rep):
    global bstack1lll11llll_opy_
    global bstack1llllllll1_opy_
    name = bstack11ll111_opy_ (u"ࠧࠨ⚎")
    try:
        if rep.when == bstack11ll111_opy_ (u"ࠨࡥࡤࡰࡱ࠭⚏"):
            bstack1lll1l1l_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⚐"))
            try:
                if (str(skipSessionName).lower() != bstack11ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨ⚑")):
                    name = str(rep.nodeid)
                    executor_string = browserstack_executor_helper(bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⚒"), name, bstack11ll111_opy_ (u"ࠬ࠭⚓"), bstack11ll111_opy_ (u"࠭ࠧ⚔"), bstack11ll111_opy_ (u"ࠧࠨ⚕"), bstack11ll111_opy_ (u"ࠨࠩ⚖"))
                    os.environ[bstack11ll111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⚗")] = name
                    for driver in bstack1llllllll1_opy_:
                        if bstack1lll1l1l_opy_ == driver.session_id:
                            driver.execute_script(executor_string)
            except Exception as e:
                logger.debug(bstack11ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⚘").format(str(e)))
            try:
                bstack1l1ll1ll1l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll111_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⚙"):
                    status = bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⚚") if rep.outcome.lower() == bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⚛") else bstack11ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⚜")
                    reason = bstack11ll111_opy_ (u"ࠨࠩ⚝")
                    if status == bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⚞"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll111_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ⚟") if status == bstack11ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⚠") else bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⚡")
                    data = name + bstack11ll111_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ⚢") if status == bstack11ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⚣") else name + bstack11ll111_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫ⚤") + reason
                    bstack1l1ll1111_opy_ = browserstack_executor_helper(bstack11ll111_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ⚥"), bstack11ll111_opy_ (u"ࠪࠫ⚦"), bstack11ll111_opy_ (u"ࠫࠬ⚧"), bstack11ll111_opy_ (u"ࠬ࠭⚨"), level, data)
                    for driver in bstack1llllllll1_opy_:
                        if bstack1lll1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll1111_opy_)
            except Exception as e:
                logger.debug(bstack11ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⚩").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ⚪").format(str(e)))
    bstack1lll11llll_opy_(item, call, rep)
notset = Notset()
def bstack11l11l1l11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack111ll1llll_opy_
    if str(name).lower() == bstack11ll111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ⚫"):
        return bstack11ll111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ⚬")
    else:
        return bstack111ll1llll_opy_(self, name, default, skip)
def bstack11lll1l1_opy_(self):
    global CONFIG
    global bstack1l11l1l11_opy_
    try:
        proxy = bstack1111lllll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll111_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ⚭")):
                proxies = bstack111l11ll11_opy_(proxy, bstack1l111lll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack111lllll11_opy_ = proxies.popitem()
                    if bstack11ll111_opy_ (u"ࠦ࠿࠵࠯ࠣ⚮") in bstack111lllll11_opy_:
                        return bstack111lllll11_opy_
                    else:
                        return bstack11ll111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⚯") + bstack111lllll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ⚰").format(str(e)))
    return bstack1l11l1l11_opy_(self)
def bstack1ll11ll1l1_opy_():
    return (bstack11ll111_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⚱") in CONFIG or bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⚲") in CONFIG) and bstack1lllll11l_opy_() and bstack1ll1lll11_opy_() >= version.parse(
        bstack11lll1l1l_opy_)
def bstack1lll1l11l_opy_(self,
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
    global bstack1lll11lll_opy_
    global bstack11lll11ll_opy_
    global bstack111l11111l_opy_
    CONFIG[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⚳")] = str(bstack111l11111l_opy_) + str(__version__)
    bstack1l111l111_opy_ = 0
    try:
        if bstack11lll11ll_opy_ is True:
            bstack1l111l111_opy_ = int(os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⚴")))
    except:
        bstack1l111l111_opy_ = 0
    CONFIG[bstack11ll111_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ⚵")] = True
    bstack1l11l11111_opy_ = bstack11l1111l1l_opy_(CONFIG, bstack1l111l111_opy_)
    logger.debug(bstack1ll1l11l1l_opy_.format(str(bstack1l11l11111_opy_)))
    if CONFIG.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⚶")):
        bstack1l1111l1l_opy_(bstack1l11l11111_opy_, bstack11111ll1l_opy_)
    if bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⚷") in CONFIG and bstack11ll111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⚸") in CONFIG[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⚹")][bstack1l111l111_opy_]:
        bstack1lll11lll_opy_ = CONFIG[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⚺")][bstack1l111l111_opy_][bstack11ll111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⚻")]
    import urllib
    import json
    if bstack11ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⚼") in CONFIG and str(CONFIG[bstack11ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⚽")]).lower() != bstack11ll111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⚾"):
        bstack1l1111ll_opy_ = bstack11llll11_opy_()
        cdpUrl = bstack1l1111ll_opy_ + urllib.parse.quote(json.dumps(bstack1l11l11111_opy_))
    else:
        cdpUrl = bstack11ll111_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ⚿") + urllib.parse.quote(json.dumps(bstack1l11l11111_opy_))
    browser = self.connect(cdpUrl)
    return browser
def bstack11l1l111l1_opy_():
    global bstack1l111l11l1_opy_
    global bstack111l11111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1ll1lll1_opy_
        if not bstack1l11l1111ll_opy_():
            global bstack1ll1l11lll_opy_
            if not bstack1ll1l11lll_opy_:
                from bstack_utils.helper import bstack1l1l111l_opy_, bstack11l11l11_opy_
                bstack1ll1l11lll_opy_ = bstack1l1l111l_opy_()
                bstack11l11l11_opy_(bstack111l11111l_opy_)
            BrowserType.connect = bstack1l1ll1lll1_opy_
            return
        BrowserType.launch = bstack1lll1l11l_opy_
        bstack1l111l11l1_opy_ = True
    except Exception as e:
        pass
def bstack1ll1ll1ll111_opy_():
    global CONFIG
    global bstack1llll11l1_opy_
    global bstack11lll111ll_opy_
    global bstack11111ll1l_opy_
    global bstack11lll11ll_opy_
    global bstack1l11l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ⛀")))
    bstack1llll11l1_opy_ = eval(os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ⛁")))
    bstack11lll111ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ⛂"))
    bstack11lll1llll_opy_(CONFIG, bstack1llll11l1_opy_)
    bstack1l11l1l1_opy_ = logger_utils.configure_logger(CONFIG, bstack1l11l1l1_opy_)
    if cli.bstack1l11l1111_opy_():
        bstack111l1llll1_opy_.invoke(bstack1l11lll1ll_opy_.CONNECT, bstack11ll1l11l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⛃"), bstack11ll111_opy_ (u"ࠬ࠶ࠧ⛄")))
        cli.bstack1ll1l11l1ll_opy_(cli_context.platform_index)
        cli.bstack1ll111lllll_opy_(bstack1l111lll11_opy_(bstack11lll111ll_opy_, CONFIG), cli_context.platform_index, bstack1ll1ll1ll1_opy_)
        cli.bstack1ll1l11l111_opy_()
        logger.debug(bstack11ll111_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⛅") + str(cli_context.platform_index) + bstack11ll111_opy_ (u"ࠢࠣ⛆"))
        return # skip all existing operations
    global bstack11lll1ll_opy_
    global bstack1llll1llll_opy_
    global bstack11lll1l11l_opy_
    global bstack11l11ll1_opy_
    global bstack1ll1l1l1ll_opy_
    global bstack1l1111ll1l_opy_
    global bstack11ll11lll_opy_
    global bstack11lll1ll1l_opy_
    global bstack1l11l1l11_opy_
    global bstack111ll1llll_opy_
    global bstack1l111ll1l_opy_
    global bstack1lll11llll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11lll1ll_opy_ = webdriver.Remote.__init__
        bstack1llll1llll_opy_ = WebDriver.quit
        bstack11ll11lll_opy_ = WebDriver.close
        bstack11lll1ll1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11ll111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⛇") in CONFIG or bstack11ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⛈") in CONFIG) and bstack1lllll11l_opy_():
        if bstack1ll1lll11_opy_() < version.parse(bstack11lll1l1l_opy_):
            logger.error(bstack1ll111llll_opy_.format(bstack1ll1lll11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11ll111_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⛉")) and callable(getattr(RemoteConnection, bstack11ll111_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⛊"))):
                    bstack1l11l1l11_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l11l1l11_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1lll111111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack111ll1llll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l111ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack11ll111_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧ⛋"), bstack11l1ll1ll1_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1lll11llll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ⛌"))
    bstack11111ll1l_opy_ = CONFIG.get(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⛍"), {}).get(bstack11ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⛎"))
    bstack11lll11ll_opy_ = True
    bstack1l1ll111l1_opy_(bstack1ll1l1ll11_opy_)
if (bstack111l111l111_opy_()):
    bstack1ll1ll1ll111_opy_()
@error_handler(class_method=False)
def bstack1ll1lll11ll1_opy_(hook_name, event, bstack11l1llll11l_opy_=None):
    if hook_name not in [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⛏"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⛐"), bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⛑"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⛒"), bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⛓"), bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⛔"), bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⛕"), bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ⛖")]:
        return
    node = store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⛗")]
    if hook_name in [bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⛘"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⛙")]:
        node = store[bstack11ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ⛚")]
    elif hook_name in [bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⛛"), bstack11ll111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⛜")]:
        node = store[bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⛝")]
    hook_type = bstack1lll1l1ll111_opy_(hook_name)
    if event == bstack11ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⛞"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_[hook_type], bstack1l1llll1l1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack11111ll1l1_opy_ = {
            bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩ⛟"): uuid,
            bstack11ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⛠"): current_time(),
            bstack11ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫ⛡"): bstack11ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⛢"),
            bstack11ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⛣"): hook_type,
            bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⛤"): hook_name
        }
        store[bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⛥")].append(uuid)
        bstack1ll1ll1l11l1_opy_ = node.nodeid
        if hook_type == bstack11ll111_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⛦"):
            if not _11111l11ll_opy_.get(bstack1ll1ll1l11l1_opy_, None):
                _11111l11ll_opy_[bstack1ll1ll1l11l1_opy_] = {bstack11ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⛧"): []}
            _11111l11ll_opy_[bstack1ll1ll1l11l1_opy_][bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⛨")].append(bstack11111ll1l1_opy_[bstack11ll111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⛩")])
        _11111l11ll_opy_[bstack1ll1ll1l11l1_opy_ + bstack11ll111_opy_ (u"ࠨ࠯ࠪ⛪") + hook_name] = bstack11111ll1l1_opy_
        bstack1ll1ll1ll11l_opy_(node, bstack11111ll1l1_opy_, bstack11ll111_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⛫"))
    elif event == bstack11ll111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⛬"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l1l_opy_[hook_type], bstack1l1llll1l1l_opy_.POST, node, None, bstack11l1llll11l_opy_)
            return
        bstack1111l1l111_opy_ = node.nodeid + bstack11ll111_opy_ (u"ࠫ࠲࠭⛭") + hook_name
        _11111l11ll_opy_[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⛮")] = current_time()
        bstack1ll1ll1l111l_opy_(_11111l11ll_opy_[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⛯")])
        bstack1ll1ll1ll11l_opy_(node, _11111l11ll_opy_[bstack1111l1l111_opy_], bstack11ll111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⛰"), bstack1ll1ll1lll1l_opy_=bstack11l1llll11l_opy_)
def bstack1ll1lll1l1l1_opy_():
    global bstack1ll1ll1l1l1l_opy_
    if bstack111l1lll_opy_():
        bstack1ll1ll1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⛱")
    else:
        bstack1ll1ll1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⛲")
@TestHubHandler.bstack1lll11111l1l_opy_
def bstack1ll1lll1l11l_opy_():
    bstack1ll1lll1l1l1_opy_()
    if cli.is_running():
        try:
            bstack1111l1111l1_opy_(bstack1ll1lll11ll1_opy_)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⛳").format(e))
        return
    if bstack1lllll11l_opy_():
        global_config = Config.get_instance()
        bstack11ll111_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ⛴")
        if global_config.get_property(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⛵")):
            if CONFIG.get(bstack11ll111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⛶")) is not None and int(CONFIG[bstack11ll111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⛷")]) > 1:
                bstack1l111l1l1l_opy_(bstack111l1l1l_opy_)
            return
        bstack1l111l1l1l_opy_(bstack111l1l1l_opy_)
    try:
        bstack1111l1111l1_opy_(bstack1ll1lll11ll1_opy_)
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⛸").format(e))
bstack1ll1lll1l11l_opy_()