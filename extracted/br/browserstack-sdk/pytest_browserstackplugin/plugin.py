# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack111lll111l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11l11ll11l_opy_, bstack111111111_opy_, update, bstack11ll1l11ll_opy_,
                                       bstack11llll11ll_opy_, bstack1l11111ll1_opy_, bstack1ll111l1_opy_, bstack11lll1ll1_opy_,
                                       bstack1ll11111ll_opy_, bstack1ll1llll1l_opy_, bstack11llll1l_opy_,
                                       bstack1l111lll1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11l11111l_opy_)
from browserstack_sdk.bstack1ll1lll11_opy_ import bstack11111111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1111l1lll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1llllll1l_opy_, bstack1lll11ll1l_opy_, bstack11l11lll11_opy_, \
    bstack1ll1l111l1_opy_
from bstack_utils.helper import bstack11llll11l1_opy_, bstack111l1l111ll_opy_, bstack1llllll1lll_opy_, bstack1ll111l1l_opy_, bstack1l111lll111_opy_, current_time, \
    bstack111l11lll1l_opy_, \
    bstack111l1l11111_opy_, bstack1l1ll1111l_opy_, bstack1l11111111_opy_, bstack1111l1l1111_opy_, bstack1llll1ll1_opy_, Notset, \
    bstack11ll1l1l1l_opy_, time_diff, bstack111l11l1l1l_opy_, Result, bstack111l11l1111_opy_, bstack111l11l1ll1_opy_, error_handler, \
    bstack11l1ll1l1_opy_, bstack1llll1l11_opy_, bstack1lll1l111_opy_, bstack111l11l1l11_opy_
from bstack_utils.bstack1111l111111_opy_ import bstack11111llll11_opy_
from bstack_utils.messages import bstack1111111l_opy_, bstack1l111ll11_opy_, bstack1l11lll1ll_opy_, bstack111l111111_opy_, bstack11l11ll1ll_opy_, \
    bstack1l1ll1l1l1_opy_, bstack11lllll1_opy_, bstack1l1l111111_opy_, bstack1lllll111l_opy_, bstack11l1l1l1_opy_, \
    bstack1111l1ll1_opy_, bstack11111l1l_opy_, bstack1llll1lll_opy_
from bstack_utils.proxy import bstack11lll1ll11_opy_, bstack11ll11lll_opy_
from bstack_utils.bstack1ll1111ll_opy_ import bstack1lll1ll11ll1_opy_, bstack1lll1ll1111l_opy_, bstack1lll1ll11111_opy_, bstack1lll1ll111l1_opy_, \
    bstack1lll1l1llll1_opy_, bstack1lll1l1lll11_opy_, bstack1lll1l1ll1ll_opy_, bstack1ll1l1l1l_opy_, bstack1lll1ll11l11_opy_
from bstack_utils.bstack111l1lll1_opy_ import bstack1l111111l_opy_
from bstack_utils.session_utils import browserstack_executor_helper, bstack11llll1ll1_opy_, bstack1l1l11111l_opy_, \
    bstack11lll1l11l_opy_, bstack1l111l11l1_opy_
from bstack_utils.test_data import TestData
from bstack_utils.bstack1111lll11l_opy_ import bstack1l111111_opy_
import bstack_utils.accessibility as bstack1l111ll111_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.bstack111llllll1_opy_ import bstack111llllll1_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1l1l11l11l_opy_
from browserstack_sdk.__init__ import bstack11l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack11l1l1l11_opy_, bstack1lllllll1_opy_, bstack1l1111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11ll111l11l_opy_, bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack11l1l1l11_opy_, bstack1lllllll1_opy_, bstack1l1111l1l_opy_
bstack11l1ll11l1_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1lll111lll_opy_ = None
bstack1lll111111_opy_ = None
bstack11l111lll1_opy_ = None
bstack1l1l111ll1_opy_ = None
bstack111l1ll11l_opy_ = None
bstack11l11l1l_opy_ = None
bstack1lll111ll_opy_ = None
bstack11ll11ll11_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack11l11llll1_opy_ = None
bstack1lll1lll1l_opy_ = None
bstack11ll1ll111_opy_ = bstack11l1l11_opy_ (u"ࠪࠫ⒙")
CONFIG = {}
bstack1l11ll1ll1_opy_ = False
bstack1l1l11ll11_opy_ = bstack11l1l11_opy_ (u"ࠫࠬ⒚")
bstack1l1l1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭⒛")
bstack1l11ll11ll_opy_ = False
bstack1ll1111ll1_opy_ = []
bstack1l11l11l1_opy_ = bstack1llllll1l_opy_
bstack1ll1ll1llll1_opy_ = bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⒜")
bstack1ll11ll11l_opy_ = {}
bstack1ll1ll11l1_opy_ = None
bstack11l11ll111_opy_ = False
logger = logger_utils.get_logger(__name__, bstack1l11l11l1_opy_)
store = {
    bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⒝"): []
}
bstack1ll1ll1ll1l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111l11l11_opy_ = {}
current_test_uuid = None
cli_context = bstack11ll111l11l_opy_(
    test_framework_name=bstack1l1l1l1l_opy_[bstack11l1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ⒞")] if bstack1llll1ll1_opy_() else bstack1l1l1l1l_opy_[bstack11l1l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩ⒟")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11lll1ll1l_opy_(page, bstack1llll1l11l_opy_):
    try:
        page.evaluate(bstack11l1l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ⒠"),
                      bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨ⒡") + json.dumps(
                          bstack1llll1l11l_opy_) + bstack11l1l11_opy_ (u"ࠧࢃࡽࠣ⒢"))
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦ⒣"), e)
def bstack1lll1l1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ⒤"), bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭⒥") + json.dumps(
            message) + bstack11l1l11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ⒦") + json.dumps(level) + bstack11l1l11_opy_ (u"ࠪࢁࢂ࠭⒧"))
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ⒨"), e)
def pytest_configure(config):
    global bstack1l1l11ll11_opy_
    global CONFIG
    global_config = Config.get_instance()
    config.args = bstack1l111111_opy_.bstack1ll1llll11l1_opy_(config.args)
    global_config.bstack1lllll11l1_opy_(bstack1lll1l111_opy_(config.getoption(bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ⒩"))))
    try:
        logger_utils.bstack11111l1l1l1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.CONNECT, bstack1l1111l1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⒪"), bstack11l1l11_opy_ (u"ࠧ࠱ࠩ⒫")))
        config = json.loads(os.environ.get(bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢ⒬"), bstack11l1l11_opy_ (u"ࠤࡾࢁࠧ⒭")))
        cli.bstack1l1llll1111_opy_(bstack1l11111111_opy_(bstack1l1l11ll11_opy_, CONFIG), cli_context.platform_index, bstack11ll1l11ll_opy_)
    if cli.bstack1l1lll1l1ll_opy_(bstack1ll1l1l1lll_opy_):
        cli.bstack1ll11llllll_opy_()
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ⒮") + str(cli_context.platform_index) + bstack11l1l11_opy_ (u"ࠦࠧ⒯"))
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.BEFORE_ALL, bstack1ll11lll1ll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11l1l11_opy_ (u"ࠧࡽࡨࡦࡰࠥ⒰"), None)
    if cli.is_running() and when == bstack11l1l11_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⒱"):
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.LOG_REPORT, bstack1ll11lll1ll_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11l1l11_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ⒲"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⒳")))
        if not passed:
            config = json.loads(os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣ⒴"), bstack11l1l11_opy_ (u"ࠥࡿࢂࠨ⒵")))
            if bstack1l1l11l11l_opy_.bstack111lll1l11_opy_(config):
                bstack1llll1l1lll1_opy_ = bstack1l1l11l11l_opy_.bstack111lll1ll1_opy_(config)
                if item.execution_count > bstack1llll1l1lll1_opy_:
                    print(bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡴࡨࡸࡷ࡯ࡥࡴ࠼ࠣࠫⒶ"), report.nodeid, os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪⒷ")))
                    bstack1l1l11l11l_opy_.bstack1llllll1111l_opy_(report.nodeid)
            else:
                print(bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥ࠭Ⓒ"), report.nodeid, os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⒹ")))
                bstack1l1l11l11l_opy_.bstack1llllll1111l_opy_(report.nodeid)
        else:
            print(bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࠦࡰࡢࡵࡶࡩࡩࡀࠠࠨⒺ"), report.nodeid, os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧⒻ")))
    if cli.is_running():
        if when == bstack11l1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤⒼ"):
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.BEFORE_EACH, bstack1ll11lll1ll_opy_.POST, item, call, outcome)
        elif when == bstack11l1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤⒽ"):
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.LOG_REPORT, bstack1ll11lll1ll_opy_.POST, item, call, outcome)
        elif when == bstack11l1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢⒾ"):
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.AFTER_EACH, bstack1ll11lll1ll_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack11l1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨⒿ"))
    plugins = item.config.getoption(bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣⓀ"))
    report = outcome.get_result()
    os.environ[bstack11l1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫⓁ")] = report.nodeid
    bstack1ll1ll1l11ll_opy_(item, call, report)
    if bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢⓂ") not in plugins or bstack1llll1ll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1l11_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦⓃ"), None)
    page = getattr(item, bstack11l1l11_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥⓄ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1ll1l1l1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1ll1l1l11_opy_(item, report, summary, skipSessionName)
def bstack1ll1ll1l1l1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫⓅ") and report.skipped:
        bstack1lll1ll11l11_opy_(report)
    if report.when in [bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧⓆ"), bstack11l1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤⓇ")]:
        return
    if not bstack1l111lll111_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ⓢ")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧⓉ") + json.dumps(
                    report.nodeid) + bstack11l1l11_opy_ (u"ࠪࢁࢂ࠭Ⓤ"))
        os.environ[bstack11l1l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧⓋ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧⓌ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣⓍ")))
    bstack1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠢࠣⓎ")
    bstack1lll1ll11l11_opy_(report)
    if not passed:
        try:
            bstack1lll1111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣⓏ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1111l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦⓐ")))
        bstack1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠥࠦⓑ")
        if not passed:
            try:
                bstack1lll1111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦⓒ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1111l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩⓓ")
                    + json.dumps(bstack11l1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢⓔ"))
                    + bstack11l1l11_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥⓕ")
                )
            else:
                item._driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ⓖ")
                    + json.dumps(str(bstack1lll1111l_opy_))
                    + bstack11l1l11_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧⓗ")
                )
        except Exception as e:
            summary.append(bstack11l1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣⓘ").format(e))
def bstack1ll1lll1l1ll_opy_(test_name, error_message):
    try:
        bstack1ll1lll1l1l1_opy_ = []
        bstack1ll11ll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫⓙ"), bstack11l1l11_opy_ (u"ࠬ࠶ࠧⓚ"))
        bstack1l1l1l1l1l_opy_ = {bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⓛ"): test_name, bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ⓜ"): error_message, bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧⓝ"): bstack1ll11ll1l1_opy_}
        bstack1ll1lll111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧⓞ"))
        if os.path.exists(bstack1ll1lll111ll_opy_):
            with open(bstack1ll1lll111ll_opy_) as f:
                bstack1ll1lll1l1l1_opy_ = json.load(f)
        bstack1ll1lll1l1l1_opy_.append(bstack1l1l1l1l1l_opy_)
        with open(bstack1ll1lll111ll_opy_, bstack11l1l11_opy_ (u"ࠪࡻࠬⓟ")) as f:
            json.dump(bstack1ll1lll1l1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩⓠ") + str(e))
def bstack1ll1ll1l1l11_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦⓡ"), bstack11l1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣⓢ")]:
        return
    if (str(skipSessionName).lower() != bstack11l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬⓣ")):
        bstack11lll1ll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥⓤ")))
    bstack1lll1111l_opy_ = bstack11l1l11_opy_ (u"ࠤࠥⓥ")
    bstack1lll1ll11l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll1111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥⓦ").format(e)
                )
        try:
            if passed:
                bstack1l111l11l1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪⓧ"), None), bstack11l1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧⓨ"))
            else:
                error_message = bstack11l1l11_opy_ (u"࠭ࠧⓩ")
                if bstack1lll1111l_opy_:
                    bstack1lll1l1l1l_opy_(item._page, str(bstack1lll1111l_opy_), bstack11l1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ⓪"))
                    bstack1l111l11l1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⓫"), None), bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⓬"), str(bstack1lll1111l_opy_))
                    error_message = str(bstack1lll1111l_opy_)
                else:
                    bstack1l111l11l1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⓭"), None), bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⓮"))
                bstack1ll1lll1l1ll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤ⓯").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11l1l11_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ⓰"), default=bstack11l1l11_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ⓱"), help=bstack11l1l11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ⓲"))
    parser.addoption(bstack11l1l11_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ⓳"), default=bstack11l1l11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ⓴"), help=bstack11l1l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ⓵"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1l11_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢ⓶"), action=bstack11l1l11_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧ⓷"), default=bstack11l1l11_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢ⓸"),
                         help=bstack11l1l11_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢ⓹"))
def bstack1111l1l11l_opy_(log):
    if not (log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⓺")] and log[bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⓻")].strip()):
        return
    active = bstack1111l1l1l1_opy_()
    log = {
        bstack11l1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⓼"): log[bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⓽")],
        bstack11l1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⓾"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"࡛ࠧࠩ⓿"),
        bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ─"): log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ━")],
    }
    if active:
        if active[bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ│")] == bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ┃"):
            log[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┄")] = active[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┅")]
        elif active[bstack11l1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ┆")] == bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭┇"):
            log[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ┈")] = active[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ┉")]
    TestHubHandler.bstack1l111ll1_opy_([log])
def bstack1111l1l1l1_opy_():
    if len(store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ┊")]) > 0 and store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ┋")][-1]:
        return {
            bstack11l1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ┌"): bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ┍"),
            bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ┎"): store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭┏")][-1]
        }
    if store.get(bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ┐"), None):
        return {
            bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ┑"): bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࠪ┒"),
            bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┓"): store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ└")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.INIT_TEST, bstack1ll11lll1ll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.INIT_TEST, bstack1ll11lll1ll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1ll1lll11l1l_opy_ = True
        bstack1l1lll11ll_opy_ = bstack1l111ll111_opy_.bstack11ll1lll1l_opy_(bstack111l1l11111_opy_(item.own_markers))
        if not cli.bstack1l1lll1l1ll_opy_(bstack1ll1l1l1lll_opy_):
            item._a11y_test_case = bstack1l1lll11ll_opy_
            if bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ┕"), None):
                driver = getattr(item, bstack11l1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ┖"), None)
                item._a11y_started = bstack1l111ll111_opy_.bstack111ll1ll11_opy_(driver, bstack1l1lll11ll_opy_)
        if not TestHubHandler.on() or bstack1ll1ll1llll1_opy_ != bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ┗"):
            return
        global current_test_uuid #, bstack1111ll1lll_opy_
        bstack1lllllll1l1_opy_ = {
            bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ┘"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ┙"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"࡚࠭ࠨ┚")
        }
        current_test_uuid = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┛")]
        store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ├")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ┝")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111l11l11_opy_[item.nodeid] = {**_1111l11l11_opy_[item.nodeid], **bstack1lllllll1l1_opy_}
        bstack1ll1ll1lll11_opy_(item, _1111l11l11_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ┞"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭┟"), str(err))
def pytest_runtest_setup(item):
    store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ┠")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.BEFORE_EACH, bstack1ll11lll1ll_opy_.PRE, item, bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ┡"))
    if bstack1l1l11l11l_opy_.bstack11111111111_opy_():
            bstack1ll1ll1ll11l_opy_ = bstack11l1l11_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡢࡵࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦ┢")
            logger.error(bstack1ll1ll1ll11l_opy_)
            bstack1lllllll1l1_opy_ = {
                bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭┣"): uuid4().__str__(),
                bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭┤"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠪ࡞ࠬ┥"),
                bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ┦"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠬࡠࠧ┧"),
                bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭┨"): bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ┩"),
                bstack11l1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ┪"): bstack1ll1ll1ll11l_opy_,
                bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ┫"): [],
                bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ┬"): []
            }
            bstack1ll1ll1lll11_opy_(item, bstack1lllllll1l1_opy_, bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ┭"))
            pytest.skip(bstack1ll1ll1ll11l_opy_)
            return # skip all existing operations
    global bstack1ll1ll1ll1l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111l1l1111_opy_():
        atexit.register(bstack1llll1l1_opy_)
        if not bstack1ll1ll1ll1l1_opy_:
            try:
                bstack1ll1lll11lll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l11l1l11_opy_():
                    bstack1ll1lll11lll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1lll11lll_opy_:
                    signal.signal(s, bstack1lllll1llll_opy_)
                bstack1ll1ll1ll1l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ┮") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll1ll11ll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭┯")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lllllll1l1_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┰"): uuid,
            bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ┱"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠩ࡝ࠫ┲"),
            bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ┳"): bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ┴"),
            bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ┵"): bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ┶"),
            bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ┷"): bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ┸")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭┹")] = item
        store[bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ┺")] = [uuid]
        if not _1111l11l11_opy_.get(item.nodeid, None):
            _1111l11l11_opy_[item.nodeid] = {bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ┻"): [], bstack11l1l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ┼"): []}
        _1111l11l11_opy_[item.nodeid][bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ┽")].append(bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┾")])
        _1111l11l11_opy_[item.nodeid + bstack11l1l11_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ┿")] = bstack1lllllll1l1_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1ll1l11l1_opy_(item, bstack1lllllll1l1_opy_, bstack11l1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ╀"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭╁"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.AFTER_EACH, bstack1ll11lll1ll_opy_.PRE, item, bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭╂"))
        return # skip all existing operations
    try:
        global bstack1ll11ll11l_opy_
        bstack1ll11ll1l1_opy_ = 0
        if bstack1l11ll11ll_opy_ is True:
            bstack1ll11ll1l1_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ╃")))
        if bstack11l1llll1_opy_.bstack1l1111ll11_opy_() == bstack11l1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦ╄"):
            if bstack11l1llll1_opy_.bstack11l1ll111l_opy_() == bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ╅"):
                bstack1ll1lll11111_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ╆"), None)
                bstack1l1111l11l_opy_ = bstack1ll1lll11111_opy_ + bstack11l1l11_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧ╇")
                driver = getattr(item, bstack11l1l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ╈"), None)
                bstack1ll1l1ll1l_opy_ = getattr(item, bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ╉"), None)
                bstack111l1l1ll1_opy_ = getattr(item, bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ╊"), None)
                PercySDK.screenshot(driver, bstack1l1111l11l_opy_, bstack1ll1l1ll1l_opy_=bstack1ll1l1ll1l_opy_, bstack111l1l1ll1_opy_=bstack111l1l1ll1_opy_, bstack111l1111l1_opy_=bstack1ll11ll1l1_opy_)
        if not cli.bstack1l1lll1l1ll_opy_(bstack1ll1l1l1lll_opy_):
            if getattr(item, bstack11l1l11_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭╋"), False):
                bstack11111111_opy_.bstack1ll1l1l1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ╌"), None), bstack1ll11ll11l_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lllllll1l1_opy_ = {
            bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭╍"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭╎"): bstack1llllll1lll_opy_().isoformat() + bstack11l1l11_opy_ (u"ࠪ࡞ࠬ╏"),
            bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ═"): bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ║"),
            bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ╒"): bstack11l1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ╓"),
            bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ╔"): bstack11l1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ╕")
        }
        _1111l11l11_opy_[item.nodeid + bstack11l1l11_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭╖")] = bstack1lllllll1l1_opy_
        bstack1ll1ll1l11l1_opy_(item, bstack1lllllll1l1_opy_, bstack11l1l11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ╗"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫ╘"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lll1ll111l1_opy_(fixturedef.argname):
        store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ╙")] = request.node
    elif bstack1lll1l1llll1_opy_(fixturedef.argname):
        store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ╚")] = request.node
    if not TestHubHandler.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.SETUP_FIXTURE, bstack1ll11lll1ll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.SETUP_FIXTURE, bstack1ll11lll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.SETUP_FIXTURE, bstack1ll11lll1ll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.SETUP_FIXTURE, bstack1ll11lll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭╛"): fixturedef.argname,
            bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ╜"): bstack111l11lll1l_opy_(outcome),
            bstack11l1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ╝"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ╞")]
        if not _1111l11l11_opy_.get(current_test_item.nodeid, None):
            _1111l11l11_opy_[current_test_item.nodeid] = {bstack11l1l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ╟"): []}
        _1111l11l11_opy_[current_test_item.nodeid][bstack11l1l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ╠")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ╡"), str(err))
if bstack1llll1ll1_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.STEP, bstack1ll11lll1ll_opy_.PRE, request, step)
            return
        try:
            _1111l11l11_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ╢")].bstack1lll11111l_opy_(id(step))
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ╣"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.STEP, bstack1ll11lll1ll_opy_.POST, request, step, exception)
            return
        try:
            _1111l11l11_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭╤")].bstack1111l1llll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ╥"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.STEP, bstack1ll11lll1ll_opy_.POST, request, step)
            return
        try:
            test_data: TestData = _1111l11l11_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ╦")]
            test_data.bstack1111l1llll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ╧"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1ll1llll1_opy_
        try:
            if not TestHubHandler.on() or bstack1ll1ll1llll1_opy_ != bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ╨"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ╩"), None)
            if not _1111l11l11_opy_.get(request.node.nodeid, None):
                _1111l11l11_opy_[request.node.nodeid] = {}
            test_data = TestData.bstack1lll11ll1l11_opy_(
                scenario, feature, request.node,
                name=bstack1lll1l1lll11_opy_(request.node, scenario),
                started_at=current_time(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ╪"),
                tags=bstack1lll1l1ll1ll_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1111ll1ll1_opy_(driver) if driver and driver.session_id else {}
            )
            _1111l11l11_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭╫")] = test_data
            bstack1ll1lll111l1_opy_(test_data.uuid)
            TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ╬"), test_data)
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ╭"), str(err))
def bstack1ll1ll1l111l_opy_(bstack1111l1l111_opy_):
    if bstack1111l1l111_opy_ in store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ╮")]:
        store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ╯")].remove(bstack1111l1l111_opy_)
def bstack1ll1lll111l1_opy_(test_uuid):
    store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ╰")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1lll111l1ll1_opy_
def bstack1ll1ll1l11ll_opy_(item, call, report):
    logger.debug(bstack11l1l11_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡴࡷࠫ╱"))
    global bstack1ll1ll1llll1_opy_
    bstack111l11l1l_opy_ = current_time()
    if hasattr(report, bstack11l1l11_opy_ (u"ࠪࡷࡹࡵࡰࠨ╲")):
        bstack111l11l1l_opy_ = bstack111l11l1111_opy_(report.stop)
    elif hasattr(report, bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ╳")):
        bstack111l11l1l_opy_ = bstack111l11l1111_opy_(report.start)
    try:
        if getattr(report, bstack11l1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪ╴"), bstack11l1l11_opy_ (u"࠭ࠧ╵")) == bstack11l1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ╶"):
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ╷").format(getattr(report, bstack11l1l11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ╸"), bstack11l1l11_opy_ (u"ࠪࠫ╹")).__str__(), bstack1ll1ll1llll1_opy_))
            if bstack1ll1ll1llll1_opy_ == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ╺"):
                _1111l11l11_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ╻")] = bstack111l11l1l_opy_
                bstack1ll1ll1lll11_opy_(item, _1111l11l11_opy_[item.nodeid], bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ╼"), report, call)
                store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ╽")] = None
            elif bstack1ll1ll1llll1_opy_ == bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ╾"):
                test_data = _1111l11l11_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ╿")]
                test_data.set(hooks=_1111l11l11_opy_[item.nodeid].get(bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ▀"), []))
                exception, bstack1111l11ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1111l11ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l1l11_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪ▁"), bstack11l1l11_opy_ (u"ࠬ࠭▂"))]
                test_data.stop(time=bstack111l11l1l_opy_, result=Result(result=getattr(report, bstack11l1l11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ▃"), bstack11l1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ▄")), exception=exception, bstack1111l11ll1_opy_=bstack1111l11ll1_opy_))
                TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ▅"), _1111l11l11_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ▆")])
        elif getattr(report, bstack11l1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ▇"), bstack11l1l11_opy_ (u"ࠫࠬ█")) in [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ▉"), bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ▊")]:
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ▋").format(getattr(report, bstack11l1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭▌"), bstack11l1l11_opy_ (u"ࠩࠪ▍")).__str__(), bstack1ll1ll1llll1_opy_))
            bstack1111l1ll11_opy_ = item.nodeid + bstack11l1l11_opy_ (u"ࠪ࠱ࠬ▎") + getattr(report, bstack11l1l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ▏"), bstack11l1l11_opy_ (u"ࠬ࠭▐"))
            if getattr(report, bstack11l1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ░"), False):
                hook_type = bstack11l1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ▒") if getattr(report, bstack11l1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭▓"), bstack11l1l11_opy_ (u"ࠩࠪ▔")) == bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ▕") else bstack11l1l11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ▖")
                _1111l11l11_opy_[bstack1111l1ll11_opy_] = {
                    bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ▗"): uuid4().__str__(),
                    bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ▘"): bstack111l11l1l_opy_,
                    bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ▙"): hook_type
                }
            _1111l11l11_opy_[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭▚")] = bstack111l11l1l_opy_
            bstack1ll1ll1l111l_opy_(_1111l11l11_opy_[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ▛")])
            bstack1ll1ll1l11l1_opy_(item, _1111l11l11_opy_[bstack1111l1ll11_opy_], bstack11l1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ▜"), report, call)
            if getattr(report, bstack11l1l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ▝"), bstack11l1l11_opy_ (u"ࠬ࠭▞")) == bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ▟"):
                if getattr(report, bstack11l1l11_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ■"), bstack11l1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ□")) == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ▢"):
                    bstack1lllllll1l1_opy_ = {
                        bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ▣"): uuid4().__str__(),
                        bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ▤"): current_time(),
                        bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ▥"): current_time()
                    }
                    _1111l11l11_opy_[item.nodeid] = {**_1111l11l11_opy_[item.nodeid], **bstack1lllllll1l1_opy_}
                    bstack1ll1ll1lll11_opy_(item, _1111l11l11_opy_[item.nodeid], bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ▦"))
                    bstack1ll1ll1lll11_opy_(item, _1111l11l11_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ▧"), report, call)
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭▨"), str(err))
def bstack1ll1lll11l11_opy_(test, bstack1lllllll1l1_opy_, result=None, call=None, bstack1l11l11l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    test_data = {
        bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ▩"): bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ▪")],
        bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ▫"): bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࠪ▬"),
        bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ▭"): test.name,
        bstack11l1l11_opy_ (u"ࠧࡣࡱࡧࡽࠬ▮"): {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭▯"): bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ▰"),
            bstack11l1l11_opy_ (u"ࠪࡧࡴࡪࡥࠨ▱"): inspect.getsource(test.obj)
        },
        bstack11l1l11_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ▲"): test.name,
        bstack11l1l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ△"): test.name,
        bstack11l1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭▴"): bstack1l111111_opy_.bstack111111lll1_opy_(test),
        bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ▵"): file_path,
        bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ▶"): file_path,
        bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ▷"): bstack11l1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ▸"),
        bstack11l1l11_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ▹"): file_path,
        bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ►"): bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ▻")],
        bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ▼"): bstack11l1l11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ▽"),
        bstack11l1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ▾"): {
            bstack11l1l11_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧ▿"): test.nodeid
        },
        bstack11l1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩ◀"): bstack111l1l11111_opy_(test.own_markers)
    }
    if bstack1l11l11l_opy_ in [bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭◁"), bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ◂")]:
        test_data[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ◃")] = {
            bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ◄"): bstack1lllllll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ◅"), [])
        }
    if bstack1l11l11l_opy_ == bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ◆"):
        test_data[bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ◇")] = bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭◈")
        test_data[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ◉")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭◊")]
        test_data[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭○")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ◌")]
    if result:
        test_data[bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ◍")] = result.outcome
        test_data[bstack11l1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ◎")] = result.duration * 1000
        test_data[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ●")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ◐")]
        if result.failed:
            test_data[bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭◑")] = TestHubHandler.bstack1lll1ll1l11_opy_(call.excinfo.typename)
            test_data[bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ◒")] = TestHubHandler.bstack1lll111111ll_opy_(call.excinfo, result)
        test_data[bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ◓")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ◔")]
    if outcome:
        test_data[bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ◕")] = bstack111l11lll1l_opy_(outcome)
        test_data[bstack11l1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭◖")] = 0
        test_data[bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ◗")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ◘")]
        if test_data[bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ◙")] == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ◚"):
            test_data[bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ◛")] = bstack11l1l11_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ◜")  # bstack1ll1ll1lllll_opy_
            test_data[bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭◝")] = [{bstack11l1l11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ◞"): [bstack11l1l11_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ◟")]}]
        test_data[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ◠")] = bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ◡")]
    return test_data
def bstack1ll1ll1ll1ll_opy_(test, bstack11111l1lll_opy_, bstack1l11l11l_opy_, result, call, outcome, bstack1ll1ll1l1lll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭◢")]
    hook_name = bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ◣")]
    hook_data = {
        bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ◤"): bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ◥")],
        bstack11l1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ◦"): bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭◧"),
        bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ◨"): bstack11l1l11_opy_ (u"ࠪࡿࢂ࠭◩").format(bstack1lll1ll1111l_opy_(hook_name)),
        bstack11l1l11_opy_ (u"ࠫࡧࡵࡤࡺࠩ◪"): {
            bstack11l1l11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ◫"): bstack11l1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭◬"),
            bstack11l1l11_opy_ (u"ࠧࡤࡱࡧࡩࠬ◭"): None
        },
        bstack11l1l11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ◮"): test.name,
        bstack11l1l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ◯"): bstack1l111111_opy_.bstack111111lll1_opy_(test, hook_name),
        bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭◰"): file_path,
        bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭◱"): file_path,
        bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ◲"): bstack11l1l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ◳"),
        bstack11l1l11_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ◴"): file_path,
        bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ◵"): bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭◶")],
        bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭◷"): bstack11l1l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭◸") if bstack1ll1ll1llll1_opy_ == bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ◹") else bstack11l1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭◺"),
        bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ◻"): hook_type
    }
    bstack1l1l1lll1ll_opy_ = bstack11111lll11_opy_(_1111l11l11_opy_.get(test.nodeid, None))
    if bstack1l1l1lll1ll_opy_:
        hook_data[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭◼")] = bstack1l1l1lll1ll_opy_
    if result:
        hook_data[bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ◽")] = result.outcome
        hook_data[bstack11l1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ◾")] = result.duration * 1000
        hook_data[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ◿")] = bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ☀")]
        if result.failed:
            hook_data[bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ☁")] = TestHubHandler.bstack1lll1ll1l11_opy_(call.excinfo.typename)
            hook_data[bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ☂")] = TestHubHandler.bstack1lll111111ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ☃")] = bstack111l11lll1l_opy_(outcome)
        hook_data[bstack11l1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ☄")] = 100
        hook_data[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ★")] = bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ☆")]
        if hook_data[bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ☇")] == bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭☈"):
            hook_data[bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭☉")] = bstack11l1l11_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ☊")  # bstack1ll1ll1lllll_opy_
            hook_data[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ☋")] = [{bstack11l1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭☌"): [bstack11l1l11_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ☍")]}]
    if bstack1ll1ll1l1lll_opy_:
        hook_data[bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ☎")] = bstack1ll1ll1l1lll_opy_.result
        hook_data[bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ☏")] = time_diff(bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ☐")], bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭☑")])
        hook_data[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ☒")] = bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ☓")]
        if hook_data[bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ☔")] == bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ☕"):
            hook_data[bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ☖")] = TestHubHandler.bstack1lll1ll1l11_opy_(bstack1ll1ll1l1lll_opy_.exception_type)
            hook_data[bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ☗")] = [{bstack11l1l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ☘"): bstack111l11l1l1l_opy_(bstack1ll1ll1l1lll_opy_.exception)}]
    return hook_data
def bstack1ll1ll1lll11_opy_(test, bstack1lllllll1l1_opy_, bstack1l11l11l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11l1l11_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭☙").format(bstack1l11l11l_opy_))
    test_data = bstack1ll1lll11l11_opy_(test, bstack1lllllll1l1_opy_, result, call, bstack1l11l11l_opy_, outcome)
    driver = getattr(test, bstack11l1l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ☚"), None)
    if bstack1l11l11l_opy_ == bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ☛") and driver:
        test_data[bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ☜")] = TestHubHandler.bstack1111ll1ll1_opy_(driver)
    if bstack1l11l11l_opy_ == bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ☝"):
        bstack1l11l11l_opy_ = bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ☞")
    bstack111111l1l1_opy_ = {
        bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ☟"): bstack1l11l11l_opy_,
        bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ☠"): test_data
    }
    TestHubHandler.bstack1l1ll11lll_opy_(bstack111111l1l1_opy_)
    if bstack1l11l11l_opy_ == bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ☡"):
        threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ☢"): bstack11l1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭☣")}
    elif bstack1l11l11l_opy_ == bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ☤"):
        threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ☥"): getattr(result, bstack11l1l11_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ☦"), bstack11l1l11_opy_ (u"ࠩࠪ☧"))}
def bstack1ll1ll1l11l1_opy_(test, bstack1lllllll1l1_opy_, bstack1l11l11l_opy_, result=None, call=None, outcome=None, bstack1ll1ll1l1lll_opy_=None):
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡷࡪࡴࡤࡠࡪࡲࡳࡰࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥ࡮࡯ࡰ࡭ࠣࡨࡦࡺࡡ࠭ࠢࡨࡺࡪࡴࡴࡕࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ☨").format(bstack1l11l11l_opy_))
    hook_data = bstack1ll1ll1ll1ll_opy_(test, bstack1lllllll1l1_opy_, bstack1l11l11l_opy_, result, call, outcome, bstack1ll1ll1l1lll_opy_)
    bstack111111l1l1_opy_ = {
        bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ☩"): bstack1l11l11l_opy_,
        bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ☪"): hook_data
    }
    TestHubHandler.bstack1l1ll11lll_opy_(bstack111111l1l1_opy_)
def bstack11111lll11_opy_(bstack1lllllll1l1_opy_):
    if not bstack1lllllll1l1_opy_:
        return None
    if bstack1lllllll1l1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ☫"), None):
        return getattr(bstack1lllllll1l1_opy_[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ☬")], bstack11l1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭☭"), None)
    return bstack1lllllll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ☮"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.LOG, bstack1ll11lll1ll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_.LOG, bstack1ll11lll1ll_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not TestHubHandler.on():
            return
        places = [bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ☯"), bstack11l1l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ☰"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ☱")]
        logs = []
        for bstack1ll1lll1l11l_opy_ in places:
            records = caplog.get_records(bstack1ll1lll1l11l_opy_)
            bstack1ll1lll1l111_opy_ = bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☲") if bstack1ll1lll1l11l_opy_ == bstack11l1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ☳") else bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ☴")
            bstack1ll1ll1ll111_opy_ = request.node.nodeid + (bstack11l1l11_opy_ (u"ࠩࠪ☵") if bstack1ll1lll1l11l_opy_ == bstack11l1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ☶") else bstack11l1l11_opy_ (u"ࠫ࠲࠭☷") + bstack1ll1lll1l11l_opy_)
            test_uuid = bstack11111lll11_opy_(_1111l11l11_opy_.get(bstack1ll1ll1ll111_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l11l1ll1_opy_(record.message):
                    continue
                logs.append({
                    bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ☸"): bstack111l1l111ll_opy_(record.created).isoformat() + bstack11l1l11_opy_ (u"࡚࠭ࠨ☹"),
                    bstack11l1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭☺"): record.levelname,
                    bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ☻"): record.message,
                    bstack1ll1lll1l111_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1l111ll1_opy_(logs)
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭☼"), str(err))
def bstack111l1l1l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l11ll111_opy_
    bstack111l11111l_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ☽"), None) and bstack11llll11l1_opy_(
            threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ☾"), None)
    bstack11l1l1l11l_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ☿"), None) != None and getattr(driver, bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭♀"), None) == True
    if sequence == bstack11l1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ♁") and driver != None:
      if not bstack11l11ll111_opy_ and bstack1l111lll111_opy_() and bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ♂") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ♃")] == True and bstack111llllll1_opy_.bstack1l111l1l1l_opy_(driver_command) and (bstack11l1l1l11l_opy_ or bstack111l11111l_opy_) and not bstack11l11111l_opy_(args):
        try:
          bstack11l11ll111_opy_ = True
          logger.debug(bstack11l1l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ♄").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l1l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ♅").format(str(err)))
        bstack11l11ll111_opy_ = False
    if sequence == bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ♆"):
        if driver_command == bstack11l1l11_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ♇"):
            TestHubHandler.bstack11l1lllll_opy_({
                bstack11l1l11_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭♈"): response[bstack11l1l11_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ♉")],
                bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ♊"): store[bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ♋")]
            })
def bstack1llll1l1_opy_():
    global bstack1ll1111ll1_opy_
    logger_utils.bstack1l1ll11l1_opy_()
    logging.shutdown()
    TestHubHandler.bstack1llllllll1l_opy_()
    for driver in bstack1ll1111ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllll1llll_opy_(*args):
    global bstack1ll1111ll1_opy_
    TestHubHandler.bstack1llllllll1l_opy_()
    for driver in bstack1ll1111ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11lllllll1_opy_(self, *args, **kwargs):
    bstack1l11ll111l_opy_ = bstack11l1ll11l1_opy_(self, *args, **kwargs)
    bstack1l1llllll1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ♌"), None)
    if bstack1l1llllll1_opy_ and bstack1l1llllll1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ♍"), bstack11l1l11_opy_ (u"࠭ࠧ♎")) == bstack11l1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ♏"):
        TestHubHandler.bstack1lllll1ll1_opy_(self)
    return bstack1l11ll111l_opy_
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack11111l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11ll11l111_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.get_instance()
    if global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ♐")):
        return
    global_config.bstack1l111111ll_opy_(bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭♑"), True)
    global bstack11ll1ll111_opy_
    global bstack1lll1ll1ll_opy_
    bstack11ll1ll111_opy_ = framework_name
    logger.info(bstack11111l1l_opy_.format(bstack11ll1ll111_opy_.split(bstack11l1l11_opy_ (u"ࠪ࠱ࠬ♒"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l111lll111_opy_():
            Service.start = bstack1ll111l1_opy_
            Service.stop = bstack11lll1ll1_opy_
            webdriver.Remote.get = bstack1l11ll111_opy_
            webdriver.Remote.__init__ = bstack11l11l1lll_opy_
            if not isinstance(os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ♓")), str):
                return
            WebDriver.quit = bstack11l11111l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack11lllllll1_opy_
        bstack1lll1ll1ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11l1l11_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ♔")):
        bstack1lll1ll1ll_opy_ = eval(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ♕")))
    if not bstack1lll1ll1ll_opy_:
        bstack1ll1llll1l_opy_(bstack11l1l11_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ♖"), bstack1111l1ll1_opy_)
    if bstack111111l11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ♗")) and callable(getattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ♘"))):
                RemoteConnection._get_proxy_url = bstack1l1111l111_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1111l111_opy_
        except Exception as e:
            logger.error(bstack1l1ll1l1l1_opy_.format(str(e)))
    if bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ♙") in str(framework_name).lower():
        if not bstack1l111lll111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11llll11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11111ll1_opy_
            Config.getoption = bstack1l1l111l1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111ll1ll1l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1llllll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11l11111l1_opy_(self):
    global bstack11ll1ll111_opy_
    global bstack1ll1l1111l_opy_
    global bstack1l1ll111l1_opy_
    try:
        if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ♚") in bstack11ll1ll111_opy_ and self.session_id != None and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ♛"), bstack11l1l11_opy_ (u"࠭ࠧ♜")) != bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ♝"):
            bstack11l1ll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ♞") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ♟")
            bstack1llll1l11_opy_(logger, True)
            if os.environ.get(bstack11l1l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭♠"), None):
                self.execute_script(
                    bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ♡") + json.dumps(
                        os.environ.get(bstack11l1l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ♢"))) + bstack11l1l11_opy_ (u"࠭ࡽࡾࠩ♣"))
            if self != None:
                bstack11lll1l11l_opy_(self, bstack11l1ll11_opy_, bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠪ♤").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l1lll1l1ll_opy_(bstack1ll1l1l1lll_opy_):
            item = store.get(bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ♥"), None)
            if item is not None and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ♦"), None):
                bstack11111111_opy_.bstack1ll1l1l1_opy_(self, bstack1ll11ll11l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l1l11_opy_ (u"ࠪࠫ♧")
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ♨") + str(e))
    bstack1l1ll111l1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11llllllll_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack11l11l1lll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1l1111l_opy_
    global bstack1ll1ll11l1_opy_
    global bstack1l11ll11ll_opy_
    global bstack11ll1ll111_opy_
    global bstack11l1ll11l1_opy_
    global bstack1ll1111ll1_opy_
    global bstack1l1l11ll11_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1ll11ll11l_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ♩")] = str(bstack11ll1ll111_opy_) + str(__version__)
    command_executor = bstack1l11111111_opy_(bstack1l1l11ll11_opy_, CONFIG)
    logger.debug(bstack111l111111_opy_.format(command_executor))
    proxy = bstack1l111lll1l_opy_(CONFIG, proxy)
    bstack1ll11ll1l1_opy_ = 0
    try:
        if bstack1l11ll11ll_opy_ is True:
            bstack1ll11ll1l1_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭♪")))
    except:
        bstack1ll11ll1l1_opy_ = 0
    bstack11ll11llll_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1ll11ll1l1_opy_)
    logger.debug(bstack1l1l111111_opy_.format(str(bstack11ll11llll_opy_)))
    bstack1ll11ll11l_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ♫"))[bstack1ll11ll1l1_opy_]
    if bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ♬") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭♭")]:
        bstack1l1l11111l_opy_(bstack11ll11llll_opy_, bstack1l1l1l1ll1_opy_)
    if bstack1l111ll111_opy_.bstack111ll1111l_opy_(CONFIG, bstack1ll11ll1l1_opy_) and bstack1l111ll111_opy_.bstack11l1llllll_opy_(bstack11ll11llll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l1lll1l1ll_opy_(bstack1ll1l1l1lll_opy_):
            bstack1l111ll111_opy_.set_capabilities(bstack11ll11llll_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll1ll1ll_opy_ = bstack111111111_opy_(desired_capabilities)
        bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ♮")] = bstack11ll1l1l1l_opy_(CONFIG)
        bstack111ll111l_opy_ = bstack11l11ll11l_opy_(bstack11ll1ll1ll_opy_)
        if bstack111ll111l_opy_:
            bstack11ll11llll_opy_ = update(bstack111ll111l_opy_, bstack11ll11llll_opy_)
        desired_capabilities = None
    if options:
        bstack1ll11111ll_opy_(options, bstack11ll11llll_opy_)
    if not options:
        options = bstack11ll1l11ll_opy_(bstack11ll11llll_opy_)
    if proxy and bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ♯")):
        options.proxy(proxy)
    if options and bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ♰")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1ll1111l_opy_() < version.parse(bstack11l1l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ♱")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11ll11llll_opy_)
    logger.info(bstack1l11lll1ll_opy_)
    bstack111lll111l_opy_.end(EVENTS.bstack1ll111l1l1_opy_.value, EVENTS.bstack1ll111l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ♲"),
                               EVENTS.bstack1ll111l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ♳"), True, None)
    try:
        if bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ♴")):
            bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ♵")):
            bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ♶")):
            bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack11l1ll11l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1lll11ll_opy_:
        logger.error(bstack1llll1lll_opy_.format(bstack11l1l11_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠫ♷"), str(bstack1lll11ll_opy_)))
        raise bstack1lll11ll_opy_
    try:
        bstack11lll11l1_opy_ = bstack11l1l11_opy_ (u"࠭ࠧ♸")
        if bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨ♹")):
            bstack11lll11l1_opy_ = self.caps.get(bstack11l1l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ♺"))
        else:
            bstack11lll11l1_opy_ = self.capabilities.get(bstack11l1l11_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ♻"))
        if bstack11lll11l1_opy_:
            bstack11l1ll1l1_opy_(bstack11lll11l1_opy_)
            if bstack1l1ll1111l_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ♼")):
                self.command_executor._url = bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ♽") + bstack1l1l11ll11_opy_ + bstack11l1l11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ♾")
            else:
                self.command_executor._url = bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ♿") + bstack11lll11l1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ⚀")
            logger.debug(bstack1l111ll11_opy_.format(bstack11lll11l1_opy_))
        else:
            logger.debug(bstack1111111l_opy_.format(bstack11l1l11_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤ⚁")))
    except Exception as e:
        logger.debug(bstack1111111l_opy_.format(e))
    bstack1ll1l1111l_opy_ = self.session_id
    if bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⚂") in bstack11ll1ll111_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⚃"), None)
        if item:
            bstack1ll1lll1ll1l_opy_ = getattr(item, bstack11l1l11_opy_ (u"ࠫࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࡠࡵࡷࡥࡷࡺࡥࡥࠩ⚄"), False)
            if not getattr(item, bstack11l1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⚅"), None) and bstack1ll1lll1ll1l_opy_:
                setattr(store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⚆")], bstack11l1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⚇"), self)
        bstack1l1llllll1_opy_ = getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⚈"), None)
        if bstack1l1llllll1_opy_ and bstack1l1llllll1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⚉"), bstack11l1l11_opy_ (u"ࠪࠫ⚊")) == bstack11l1l11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⚋"):
            TestHubHandler.bstack1lllll1ll1_opy_(self)
    bstack1ll1111ll1_opy_.append(self)
    if bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⚌") in CONFIG and bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⚍") in CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⚎")][bstack1ll11ll1l1_opy_]:
        bstack1ll1ll11l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⚏")][bstack1ll11ll1l1_opy_][bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⚐")]
    logger.debug(bstack11l1l1l1_opy_.format(bstack1ll1l1111l_opy_))
@measure(event_name=EVENTS.bstack1l1ll1ll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=bstack1ll1ll11l1_opy_)
def bstack1l11ll111_opy_(self, url):
    global bstack1lll111ll_opy_
    global CONFIG
    try:
        bstack11llll1ll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lllll111l_opy_.format(str(err)))
    try:
        bstack1lll111ll_opy_(self, url)
    except Exception as e:
        try:
            bstack111llllll_opy_ = str(e)
            if any(err_msg in bstack111llllll_opy_ for err_msg in bstack11l11lll11_opy_):
                bstack11llll1ll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lllll111l_opy_.format(str(err)))
        raise e
def bstack111llll1l1_opy_(item, when):
    global bstack11l11llll1_opy_
    try:
        bstack11l11llll1_opy_(item, when)
    except Exception as e:
        pass
def bstack111ll1ll1l_opy_(item, call, rep):
    global bstack1lll1lll1l_opy_
    global bstack1ll1111ll1_opy_
    name = bstack11l1l11_opy_ (u"ࠪࠫ⚑")
    try:
        if rep.when == bstack11l1l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⚒"):
            bstack1ll1l1111l_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⚓"))
            try:
                if (str(skipSessionName).lower() != bstack11l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ⚔")):
                    name = str(rep.nodeid)
                    executor_string = browserstack_executor_helper(bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⚕"), name, bstack11l1l11_opy_ (u"ࠨࠩ⚖"), bstack11l1l11_opy_ (u"ࠩࠪ⚗"), bstack11l1l11_opy_ (u"ࠪࠫ⚘"), bstack11l1l11_opy_ (u"ࠫࠬ⚙"))
                    os.environ[bstack11l1l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⚚")] = name
                    for driver in bstack1ll1111ll1_opy_:
                        if bstack1ll1l1111l_opy_ == driver.session_id:
                            driver.execute_script(executor_string)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭⚛").format(str(e)))
            try:
                bstack1ll1l1l1l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⚜"):
                    status = bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⚝") if rep.outcome.lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⚞") else bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⚟")
                    reason = bstack11l1l11_opy_ (u"ࠫࠬ⚠")
                    if status == bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⚡"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ⚢") if status == bstack11l1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⚣") else bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⚤")
                    data = name + bstack11l1l11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ⚥") if status == bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⚦") else name + bstack11l1l11_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧ⚧") + reason
                    bstack11l11lllll_opy_ = browserstack_executor_helper(bstack11l1l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ⚨"), bstack11l1l11_opy_ (u"࠭ࠧ⚩"), bstack11l1l11_opy_ (u"ࠧࠨ⚪"), bstack11l1l11_opy_ (u"ࠨࠩ⚫"), level, data)
                    for driver in bstack1ll1111ll1_opy_:
                        if bstack1ll1l1111l_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11lllll_opy_)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭⚬").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧ⚭").format(str(e)))
    bstack1lll1lll1l_opy_(item, call, rep)
notset = Notset()
def bstack1l1l111l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11l1ll1_opy_
    if str(name).lower() == bstack11l1l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫ⚮"):
        return bstack11l1l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ⚯")
    else:
        return bstack1l11l1ll1_opy_(self, name, default, skip)
def bstack1l1111l111_opy_(self):
    global CONFIG
    global bstack111l1ll11l_opy_
    try:
        proxy = bstack11lll1ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1l11_opy_ (u"࠭࠮ࡱࡣࡦࠫ⚰")):
                proxies = bstack11ll11lll_opy_(proxy, bstack1l11111111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1llll11ll_opy_ = proxies.popitem()
                    if bstack11l1l11_opy_ (u"ࠢ࠻࠱࠲ࠦ⚱") in bstack1llll11ll_opy_:
                        return bstack1llll11ll_opy_
                    else:
                        return bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⚲") + bstack1llll11ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨ⚳").format(str(e)))
    return bstack111l1ll11l_opy_(self)
def bstack111111l11_opy_():
    return (bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⚴") in CONFIG or bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⚵") in CONFIG) and bstack1ll111l1l_opy_() and bstack1l1ll1111l_opy_() >= version.parse(
        bstack1lll11ll1l_opy_)
def bstack11111ll1_opy_(self,
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
    global bstack1ll1ll11l1_opy_
    global bstack1l11ll11ll_opy_
    global bstack11ll1ll111_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⚶")] = str(bstack11ll1ll111_opy_) + str(__version__)
    bstack1ll11ll1l1_opy_ = 0
    try:
        if bstack1l11ll11ll_opy_ is True:
            bstack1ll11ll1l1_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⚷")))
    except:
        bstack1ll11ll1l1_opy_ = 0
    CONFIG[bstack11l1l11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ⚸")] = True
    bstack11ll11llll_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1ll11ll1l1_opy_)
    logger.debug(bstack1l1l111111_opy_.format(str(bstack11ll11llll_opy_)))
    if CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⚹")):
        bstack1l1l11111l_opy_(bstack11ll11llll_opy_, bstack1l1l1l1ll1_opy_)
    if bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⚺") in CONFIG and bstack11l1l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⚻") in CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⚼")][bstack1ll11ll1l1_opy_]:
        bstack1ll1ll11l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⚽")][bstack1ll11ll1l1_opy_][bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⚾")]
    import urllib
    import json
    if bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⚿") in CONFIG and str(CONFIG[bstack11l1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⛀")]).lower() != bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ⛁"):
        bstack111l1l1ll_opy_ = bstack11l11l11l_opy_()
        cdpUrl = bstack111l1l1ll_opy_ + urllib.parse.quote(json.dumps(bstack11ll11llll_opy_))
    else:
        cdpUrl = bstack11l1l11_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬ⛂") + urllib.parse.quote(json.dumps(bstack11ll11llll_opy_))
    browser = self.connect(cdpUrl)
    return browser
def bstack11llllll1l_opy_():
    global bstack1lll1ll1ll_opy_
    global bstack11ll1ll111_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1l111l_opy_
        if not bstack1l111lll111_opy_():
            global bstack1l1l1l1lll_opy_
            if not bstack1l1l1l1lll_opy_:
                from bstack_utils.helper import bstack11llllll1_opy_, bstack111ll1lll1_opy_
                bstack1l1l1l1lll_opy_ = bstack11llllll1_opy_()
                bstack111ll1lll1_opy_(bstack11ll1ll111_opy_)
            BrowserType.connect = bstack1ll1l111l_opy_
            return
        BrowserType.launch = bstack11111ll1_opy_
        bstack1lll1ll1ll_opy_ = True
    except Exception as e:
        pass
def bstack1ll1lll1111l_opy_():
    global CONFIG
    global bstack1l11ll1ll1_opy_
    global bstack1l1l11ll11_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1l11ll11ll_opy_
    global bstack1l11l11l1_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ⛃")))
    bstack1l11ll1ll1_opy_ = eval(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭⛄")))
    bstack1l1l11ll11_opy_ = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭⛅"))
    bstack11llll1l_opy_(CONFIG, bstack1l11ll1ll1_opy_)
    bstack1l11l11l1_opy_ = logger_utils.configure_logger(CONFIG, bstack1l11l11l1_opy_)
    if cli.bstack1lll11l1l_opy_():
        bstack11l1l1l11_opy_.invoke(bstack1lllllll1_opy_.CONNECT, bstack1l1111l1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⛆"), bstack11l1l11_opy_ (u"ࠨ࠲ࠪ⛇")))
        cli.bstack1ll11lll111_opy_(cli_context.platform_index)
        cli.bstack1l1llll1111_opy_(bstack1l11111111_opy_(bstack1l1l11ll11_opy_, CONFIG), cli_context.platform_index, bstack11ll1l11ll_opy_)
        cli.bstack1ll11llllll_opy_()
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣ⛈") + str(cli_context.platform_index) + bstack11l1l11_opy_ (u"ࠥࠦ⛉"))
        return # skip all existing operations
    global bstack11l1ll11l1_opy_
    global bstack1l1ll111l1_opy_
    global bstack1lll111lll_opy_
    global bstack1lll111111_opy_
    global bstack11l111lll1_opy_
    global bstack1l1l111ll1_opy_
    global bstack11l11l1l_opy_
    global bstack1lll111ll_opy_
    global bstack111l1ll11l_opy_
    global bstack1l11l1ll1_opy_
    global bstack11l11llll1_opy_
    global bstack1lll1lll1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l1ll11l1_opy_ = webdriver.Remote.__init__
        bstack1l1ll111l1_opy_ = WebDriver.quit
        bstack11l11l1l_opy_ = WebDriver.close
        bstack1lll111ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⛊") in CONFIG or bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⛋") in CONFIG) and bstack1ll111l1l_opy_():
        if bstack1l1ll1111l_opy_() < version.parse(bstack1lll11ll1l_opy_):
            logger.error(bstack11lllll1_opy_.format(bstack1l1ll1111l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11l1l11_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⛌")) and callable(getattr(RemoteConnection, bstack11l1l11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⛍"))):
                    bstack111l1ll11l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack111l1ll11l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1ll1l1l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l11l1ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack11l11llll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack11l1l11_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣ⛎"), bstack11l11ll1ll_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1lll1lll1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ⛏"))
    bstack1l1l1l1ll1_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ⛐"), {}).get(bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⛑"))
    bstack1l11ll11ll_opy_ = True
    bstack11ll11l111_opy_(bstack1ll1l111l1_opy_)
if (bstack1111l1l1111_opy_()):
    bstack1ll1lll1111l_opy_()
@error_handler(class_method=False)
def bstack1ll1ll1l1ll1_opy_(hook_name, event, bstack11ll1l1l11l_opy_=None):
    if hook_name not in [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⛒"), bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⛓"), bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⛔"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⛕"), bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⛖"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⛗"), bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ⛘"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⛙")]:
        return
    node = store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⛚")]
    if hook_name in [bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⛛"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⛜")]:
        node = store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ⛝")]
    elif hook_name in [bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⛞"), bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⛟")]:
        node = store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ⛠")]
    hook_type = bstack1lll1ll11111_opy_(hook_name)
    if event == bstack11l1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⛡"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_[hook_type], bstack1ll11lll1ll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack11111l1lll_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⛢"): uuid,
            bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⛣"): current_time(),
            bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⛤"): bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⛥"),
            bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⛦"): hook_type,
            bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⛧"): hook_name
        }
        store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⛨")].append(uuid)
        bstack1ll1lll11ll1_opy_ = node.nodeid
        if hook_type == bstack11l1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⛩"):
            if not _1111l11l11_opy_.get(bstack1ll1lll11ll1_opy_, None):
                _1111l11l11_opy_[bstack1ll1lll11ll1_opy_] = {bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⛪"): []}
            _1111l11l11_opy_[bstack1ll1lll11ll1_opy_][bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⛫")].append(bstack11111l1lll_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⛬")])
        _1111l11l11_opy_[bstack1ll1lll11ll1_opy_ + bstack11l1l11_opy_ (u"ࠫ࠲࠭⛭") + hook_name] = bstack11111l1lll_opy_
        bstack1ll1ll1l11l1_opy_(node, bstack11111l1lll_opy_, bstack11l1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⛮"))
    elif event == bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ⛯"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1llllll1l_opy_[hook_type], bstack1ll11lll1ll_opy_.POST, node, None, bstack11ll1l1l11l_opy_)
            return
        bstack1111l1ll11_opy_ = node.nodeid + bstack11l1l11_opy_ (u"ࠧ࠮ࠩ⛰") + hook_name
        _1111l11l11_opy_[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⛱")] = current_time()
        bstack1ll1ll1l111l_opy_(_1111l11l11_opy_[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⛲")])
        bstack1ll1ll1l11l1_opy_(node, _1111l11l11_opy_[bstack1111l1ll11_opy_], bstack11l1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⛳"), bstack1ll1ll1l1lll_opy_=bstack11ll1l1l11l_opy_)
def bstack1ll1lll1ll11_opy_():
    global bstack1ll1ll1llll1_opy_
    if bstack1llll1ll1_opy_():
        bstack1ll1ll1llll1_opy_ = bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ⛴")
    else:
        bstack1ll1ll1llll1_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⛵")
@TestHubHandler.bstack1lll111l1ll1_opy_
def bstack1ll1ll1lll1l_opy_():
    bstack1ll1lll1ll11_opy_()
    if cli.is_running():
        try:
            bstack11111llll11_opy_(bstack1ll1ll1l1ll1_opy_)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⛶").format(e))
        return
    if bstack1ll111l1l_opy_():
        global_config = Config.get_instance()
        bstack11l1l11_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡀࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡭ࡥࡵࡵࠣࡹࡸ࡫ࡤࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠲ࡽࡲࡢࡲࡳ࡭ࡳ࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡸࠥ࡯ࡳࠡࡲࡤࡸࡨ࡮ࡥࡥࠢ࡬ࡲࠥࡧࠠࡥ࡫ࡩࡪࡪࡸࡥ࡯ࡶࠣࡴࡷࡵࡣࡦࡵࡶࠤ࡮ࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡶࡵࠣࡻࡪࠦ࡮ࡦࡧࡧࠤࡹࡵࠠࡶࡵࡨࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡖࡡࡵࡥ࡫ࠬࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡨࡢࡰࡧࡰࡪࡸࠩࠡࡨࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࠩࠪ⛷")
        if global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⛸")):
            if CONFIG.get(bstack11l1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⛹")) is not None and int(CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⛺")]) > 1:
                bstack1l111111l_opy_(bstack111l1l1l1_opy_)
            return
        bstack1l111111l_opy_(bstack111l1l1l1_opy_)
    try:
        bstack11111llll11_opy_(bstack1ll1ll1l1ll1_opy_)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⛻").format(e))
bstack1ll1ll1lll1l_opy_()