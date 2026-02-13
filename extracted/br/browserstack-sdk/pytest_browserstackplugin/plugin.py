# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11ll11ll1l_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll111l1_opy_, bstack11llll11ll_opy_, update, bstack1111ll1ll1_opy_,
                                       bstack1l111llll1_opy_, bstack1l1l1ll1l1_opy_, bstack1l1l1ll1l_opy_, bstack1ll1l1ll_opy_,
                                       bstack1ll1lllll_opy_, bstack1l11l1ll1l_opy_, bstack11111llll_opy_,
                                       bstack1l11l1lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11ll1111l1_opy_)
from browserstack_sdk.bstack1ll1l111ll_opy_ import bstack1ll11l1l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack11111llll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11ll111l_opy_, bstack11ll111ll1_opy_, bstack11ll11l1l1_opy_, \
    bstack1lllllll1l_opy_
from bstack_utils.helper import bstack11ll11l11_opy_, bstack1111l1111l1_opy_, bstack111111l11l_opy_, bstack1l1l1l1lll_opy_, bstack1l111lllll1_opy_, bstack11l1lll11_opy_, \
    bstack111l1111l11_opy_, \
    bstack1111ll1lll1_opy_, bstack111l1lll1_opy_, bstack1l1llll1ll_opy_, bstack1111l1ll1l1_opy_, bstack11lll1111l_opy_, Notset, \
    bstack1l1l1llll_opy_, bstack111l11l1ll1_opy_, bstack1111lll111l_opy_, Result, bstack111l111l1l1_opy_, bstack11111lll11l_opy_, error_handler, \
    bstack111llll1_opy_, bstack11111l111_opy_, bstack1ll1l11lll_opy_, bstack1111llll111_opy_
from bstack_utils.bstack11111ll11l1_opy_ import bstack11111ll1l1l_opy_
from bstack_utils.messages import bstack1lll111111_opy_, bstack11l1l1l1_opy_, bstack111l1l1l1_opy_, bstack1111ll11l_opy_, bstack11lllll11_opy_, \
    bstack11l1111l1_opy_, bstack1111lllll_opy_, bstack1l11ll1ll_opy_, bstack1l1ll11l_opy_, bstack1ll11111ll_opy_, \
    bstack11111lll_opy_, bstack11ll111lll_opy_, bstack1l1lll1lll_opy_
from bstack_utils.proxy import bstack111l11l11_opy_, bstack11l11l1ll1_opy_
from bstack_utils.bstack1ll1ll111_opy_ import bstack1lll1l11ll1l_opy_, bstack1lll1l11l1l1_opy_, bstack1lll1l1l1l1l_opy_, bstack1lll1l1l11ll_opy_, \
    bstack1lll1l11ll11_opy_, bstack1lll1l1l111l_opy_, bstack1lll1l11l11l_opy_, bstack11ll1llll_opy_, bstack1lll1l11l1ll_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack111l111l1_opy_
from bstack_utils.bstack1ll111l1l1_opy_ import bstack1lll1l1l1l_opy_, bstack1ll111ll1_opy_, bstack1l1111l111_opy_, \
    bstack1ll1l1l1_opy_, bstack1l11lll11l_opy_
from bstack_utils.bstack11111lll1l_opy_ import bstack1111ll1111_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack11l1ll111l_opy_
import bstack_utils.accessibility as bstack1lllll111l_opy_
from bstack_utils.bstack1111l11lll_opy_ import bstack1ll111l1_opy_
from bstack_utils.bstack1l1lll111l_opy_ import bstack1l1lll111l_opy_
from bstack_utils.bstack1l11ll1l_opy_ import bstack1l11l1l1ll_opy_
from browserstack_sdk.__init__ import bstack1l1ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11111_opy_ import bstack1l11l11111_opy_, bstack11ll111111_opy_, bstack111l1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11ll1l1llll_opy_, bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l11l11111_opy_ import bstack1l11l11111_opy_, bstack11ll111111_opy_, bstack111l1ll1l_opy_
bstack11l111111_opy_ = None
bstack11l111l1ll_opy_ = None
bstack11ll1l1111_opy_ = None
bstack111llll11l_opy_ = None
bstack111l1l111_opy_ = None
bstack1l1l1ll1ll_opy_ = None
bstack111lllllll_opy_ = None
bstack1l1111l1ll_opy_ = None
bstack11ll11ll_opy_ = None
bstack1ll1111l1l_opy_ = None
bstack1l111l1ll1_opy_ = None
bstack1ll111111l_opy_ = None
bstack11l1ll11l1_opy_ = None
bstack11l1111ll1_opy_ = bstack11l11_opy_ (u"࠭ࠧ⒎")
CONFIG = {}
bstack11lll1l11_opy_ = False
bstack1ll1l1l1ll_opy_ = bstack11l11_opy_ (u"ࠧࠨ⒏")
bstack1l1lll1l11_opy_ = bstack11l11_opy_ (u"ࠨࠩ⒐")
bstack11lllll1l_opy_ = False
bstack111l1llll1_opy_ = []
bstack1l1ll1llll_opy_ = bstack11ll111l_opy_
bstack1ll1ll111l11_opy_ = bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⒑")
bstack11l11lll1l_opy_ = {}
bstack11l1111lll_opy_ = None
bstack1l1l1ll111_opy_ = False
logger = logger_utils.get_logger(__name__, bstack1l1ll1llll_opy_)
store = {
    bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⒒"): []
}
bstack1ll1ll11lll1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lllllll11l_opy_ = {}
current_test_uuid = None
cli_context = bstack11ll1l1llll_opy_(
    test_framework_name=bstack1l1ll11l1_opy_[bstack11l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨ⒓")] if bstack11lll1111l_opy_() else bstack1l1ll11l1_opy_[bstack11l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬ⒔")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1111llll_opy_(page, bstack11l1llll1_opy_):
    try:
        page.evaluate(bstack11l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ⒕"),
                      bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ⒖") + json.dumps(
                          bstack11l1llll1_opy_) + bstack11l11_opy_ (u"ࠣࡿࢀࠦ⒗"))
    except Exception as e:
        print(bstack11l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ⒘"), e)
def bstack11l1l11ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ⒙"), bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ⒚") + json.dumps(
            message) + bstack11l11_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ⒛") + json.dumps(level) + bstack11l11_opy_ (u"࠭ࡽࡾࠩ⒜"))
    except Exception as e:
        print(bstack11l11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ⒝"), e)
def pytest_configure(config):
    global bstack1ll1l1l1ll_opy_
    global CONFIG
    bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
    config.args = bstack11l1ll111l_opy_.bstack1ll1ll1lll1l_opy_(config.args)
    bstack11l1l1111_opy_.bstack1ll1l11ll1_opy_(bstack1ll1l11lll_opy_(config.getoption(bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⒞"))))
    try:
        logger_utils.bstack111111ll111_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.CONNECT, bstack111l1ll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⒟"), bstack11l11_opy_ (u"ࠪ࠴ࠬ⒠")))
        config = json.loads(os.environ.get(bstack11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ⒡"), bstack11l11_opy_ (u"ࠧࢁࡽࠣ⒢")))
        cli.bstack1ll1l111l1l_opy_(bstack1l1llll1ll_opy_(bstack1ll1l1l1ll_opy_, CONFIG), cli_context.platform_index, bstack1111ll1ll1_opy_)
    if cli.bstack1l1ll1ll11l_opy_(bstack1ll11ll1lll_opy_):
        cli.bstack1ll11l11lll_opy_()
        logger.debug(bstack11l11_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⒣") + str(cli_context.platform_index) + bstack11l11_opy_ (u"ࠢࠣ⒤"))
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.BEFORE_ALL, bstack1l1lllll1ll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11l11_opy_ (u"ࠣࡹ࡫ࡩࡳࠨ⒥"), None)
    if cli.is_running() and when == bstack11l11_opy_ (u"ࠤࡦࡥࡱࡲࠢ⒦"):
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.LOG_REPORT, bstack1l1lllll1ll_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11l11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⒧"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⒨")))
        if not passed:
            config = json.loads(os.environ.get(bstack11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦ⒩"), bstack11l11_opy_ (u"ࠨࡻࡾࠤ⒪")))
            if bstack1l11l1l1ll_opy_.bstack11l11lll11_opy_(config):
                bstack1llll1ll11ll_opy_ = bstack1l11l1l1ll_opy_.bstack11l1l1lll1_opy_(config)
                if item.execution_count > bstack1llll1ll11ll_opy_:
                    print(bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡷ࠿ࠦࠧ⒫"), report.nodeid, os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⒬")))
                    bstack1l11l1l1ll_opy_.bstack1lllll111l11_opy_(report.nodeid)
            else:
                print(bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠩ⒭"), report.nodeid, os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⒮")))
                bstack1l11l1l1ll_opy_.bstack1lllll111l11_opy_(report.nodeid)
        else:
            print(bstack11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡳࡥࡸࡹࡥࡥ࠼ࠣࠫ⒯"), report.nodeid, os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⒰")))
    if cli.is_running():
        if when == bstack11l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ⒱"):
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.BEFORE_EACH, bstack1l1lllll1ll_opy_.POST, item, call, outcome)
        elif when == bstack11l11_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ⒲"):
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.LOG_REPORT, bstack1l1lllll1ll_opy_.POST, item, call, outcome)
        elif when == bstack11l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ⒳"):
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.AFTER_EACH, bstack1l1lllll1ll_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⒴"))
    plugins = item.config.getoption(bstack11l11_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦ⒵"))
    report = outcome.get_result()
    os.environ[bstack11l11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧⒶ")] = report.nodeid
    bstack1ll1ll11l11l_opy_(item, call, report)
    if bstack11l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥⒷ") not in plugins or bstack11lll1111l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l11_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢⒸ"), None)
    page = getattr(item, bstack11l11_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨⒹ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1ll111ll1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1ll1ll11l_opy_(item, report, summary, skipSessionName)
def bstack1ll1ll111ll1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧⒺ") and report.skipped:
        bstack1lll1l11l1ll_opy_(report)
    if report.when in [bstack11l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣⒻ"), bstack11l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧⒼ")]:
        return
    if not bstack1l111lllll1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11l11_opy_ (u"ࠫࡹࡸࡵࡦࠩⒽ")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪⒾ") + json.dumps(
                    report.nodeid) + bstack11l11_opy_ (u"࠭ࡽࡾࠩⒿ"))
        os.environ[bstack11l11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪⓀ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣⓁ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦⓂ")))
    bstack11ll111l1_opy_ = bstack11l11_opy_ (u"ࠥࠦⓃ")
    bstack1lll1l11l1ll_opy_(report)
    if not passed:
        try:
            bstack11ll111l1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦⓄ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll111l1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢⓅ")))
        bstack11ll111l1_opy_ = bstack11l11_opy_ (u"ࠨࠢⓆ")
        if not passed:
            try:
                bstack11ll111l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢⓇ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll111l1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬⓈ")
                    + json.dumps(bstack11l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥⓉ"))
                    + bstack11l11_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨⓊ")
                )
            else:
                item._driver.execute_script(
                    bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩⓋ")
                    + json.dumps(str(bstack11ll111l1_opy_))
                    + bstack11l11_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣⓌ")
                )
        except Exception as e:
            summary.append(bstack11l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦⓍ").format(e))
def bstack1ll1ll1ll1l1_opy_(test_name, error_message):
    try:
        bstack1ll1ll1l1ll1_opy_ = []
        bstack11lllll1l1_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧⓎ"), bstack11l11_opy_ (u"ࠨ࠲ࠪⓏ"))
        bstack11lll11l_opy_ = {bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧⓐ"): test_name, bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩⓑ"): error_message, bstack11l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪⓒ"): bstack11lllll1l1_opy_}
        bstack1ll1ll11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪⓓ"))
        if os.path.exists(bstack1ll1ll11l1l1_opy_):
            with open(bstack1ll1ll11l1l1_opy_) as f:
                bstack1ll1ll1l1ll1_opy_ = json.load(f)
        bstack1ll1ll1l1ll1_opy_.append(bstack11lll11l_opy_)
        with open(bstack1ll1ll11l1l1_opy_, bstack11l11_opy_ (u"࠭ࡷࠨⓔ")) as f:
            json.dump(bstack1ll1ll1l1ll1_opy_, f)
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬⓕ") + str(e))
def bstack1ll1ll1ll11l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11l11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢⓖ"), bstack11l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦⓗ")]:
        return
    if (str(skipSessionName).lower() != bstack11l11_opy_ (u"ࠪࡸࡷࡻࡥࠨⓘ")):
        bstack1111llll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l11_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨⓙ")))
    bstack11ll111l1_opy_ = bstack11l11_opy_ (u"ࠧࠨⓚ")
    bstack1lll1l11l1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11ll111l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨⓛ").format(e)
                )
        try:
            if passed:
                bstack1l11lll11l_opy_(getattr(item, bstack11l11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ⓜ"), None), bstack11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣⓝ"))
            else:
                error_message = bstack11l11_opy_ (u"ࠩࠪⓞ")
                if bstack11ll111l1_opy_:
                    bstack11l1l11ll_opy_(item._page, str(bstack11ll111l1_opy_), bstack11l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤⓟ"))
                    bstack1l11lll11l_opy_(getattr(item, bstack11l11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪⓠ"), None), bstack11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧⓡ"), str(bstack11ll111l1_opy_))
                    error_message = str(bstack11ll111l1_opy_)
                else:
                    bstack1l11lll11l_opy_(getattr(item, bstack11l11_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬⓢ"), None), bstack11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢⓣ"))
                bstack1ll1ll1ll1l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧⓤ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11l11_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨⓥ"), default=bstack11l11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤⓦ"), help=bstack11l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥⓧ"))
    parser.addoption(bstack11l11_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦⓨ"), default=bstack11l11_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧⓩ"), help=bstack11l11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ⓪"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l11_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥ⓫"), action=bstack11l11_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣ⓬"), default=bstack11l11_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥ⓭"),
                         help=bstack11l11_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥ⓮"))
def bstack1111ll111l_opy_(log):
    if not (log[bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⓯")] and log[bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⓰")].strip()):
        return
    active = bstack11111ll1ll_opy_()
    log = {
        bstack11l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⓱"): log[bstack11l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⓲")],
        bstack11l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⓳"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"ࠪ࡞ࠬ⓴"),
        bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⓵"): log[bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⓶")],
    }
    if active:
        if active[bstack11l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⓷")] == bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⓸"):
            log[bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⓹")] = active[bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⓺")]
        elif active[bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ⓻")] == bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⓼"):
            log[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⓽")] = active[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⓾")]
    bstack1ll111l1_opy_.bstack1l1l1l11l_opy_([log])
def bstack11111ll1ll_opy_():
    if len(store[bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⓿")]) > 0 and store[bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ─")][-1]:
        return {
            bstack11l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ━"): bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ│"),
            bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ┃"): store[bstack11l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ┄")][-1]
        }
    if store.get(bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ┅"), None):
        return {
            bstack11l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ┆"): bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭┇"),
            bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ┈"): store[bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ┉")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.INIT_TEST, bstack1l1lllll1ll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.INIT_TEST, bstack1l1lllll1ll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1ll1ll1l1l1l_opy_ = True
        bstack1l11l111l_opy_ = bstack1lllll111l_opy_.bstack11l11l1lll_opy_(bstack1111ll1lll1_opy_(item.own_markers))
        if not cli.bstack1l1ll1ll11l_opy_(bstack1ll11ll1lll_opy_):
            item._a11y_test_case = bstack1l11l111l_opy_
            if bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ┊"), None):
                driver = getattr(item, bstack11l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭┋"), None)
                item._a11y_started = bstack1lllll111l_opy_.bstack11l1l11ll1_opy_(driver, bstack1l11l111l_opy_)
        if not bstack1ll111l1_opy_.on() or bstack1ll1ll111l11_opy_ != bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭┌"):
            return
        global current_test_uuid #, bstack1111l1l1l1_opy_
        bstack11111l1111_opy_ = {
            bstack11l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┍"): uuid4().__str__(),
            bstack11l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ┎"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"ࠩ࡝ࠫ┏")
        }
        current_test_uuid = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ┐")]
        store[bstack11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ┑")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ┒")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lllllll11l_opy_[item.nodeid] = {**_1lllllll11l_opy_[item.nodeid], **bstack11111l1111_opy_}
        bstack1ll1ll1l11l1_opy_(item, _1lllllll11l_opy_[item.nodeid], bstack11l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ┓"))
    except Exception as err:
        print(bstack11l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩ└"), str(err))
def pytest_runtest_setup(item):
    store[bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ┕")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.BEFORE_EACH, bstack1l1lllll1ll_opy_.PRE, item, bstack11l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ┖"))
    if bstack1l11l1l1ll_opy_.bstack1llll1llll1l_opy_():
            bstack1ll1ll1ll1ll_opy_ = bstack11l11_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡥࡸࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ┗")
            logger.error(bstack1ll1ll1ll1ll_opy_)
            bstack11111l1111_opy_ = {
                bstack11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ┘"): uuid4().__str__(),
                bstack11l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ┙"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"࡚࠭ࠨ┚"),
                bstack11l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ┛"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"ࠨ࡜ࠪ├"),
                bstack11l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ┝"): bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ┞"),
                bstack11l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ┟"): bstack1ll1ll1ll1ll_opy_,
                bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ┠"): [],
                bstack11l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ┡"): []
            }
            bstack1ll1ll1l11l1_opy_(item, bstack11111l1111_opy_, bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ┢"))
            pytest.skip(bstack1ll1ll1ll1ll_opy_)
            return # skip all existing operations
    global bstack1ll1ll11lll1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111l1ll1l1_opy_():
        atexit.register(bstack11ll1l1l11_opy_)
        if not bstack1ll1ll11lll1_opy_:
            try:
                bstack1ll1ll111l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1111llll111_opy_():
                    bstack1ll1ll111l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll1ll111l1l_opy_:
                    signal.signal(s, bstack1lllll111ll_opy_)
                bstack1ll1ll11lll1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤ┣") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll1l11ll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ┤")
    try:
        if not bstack1ll111l1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack11111l1111_opy_ = {
            bstack11l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ┥"): uuid,
            bstack11l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ┦"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"ࠬࡠࠧ┧"),
            bstack11l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ┨"): bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ┩"),
            bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ┪"): bstack11l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ┫"),
            bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭┬"): bstack11l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ┭")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ┮")] = item
        store[bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ┯")] = [uuid]
        if not _1lllllll11l_opy_.get(item.nodeid, None):
            _1lllllll11l_opy_[item.nodeid] = {bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭┰"): [], bstack11l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ┱"): []}
        _1lllllll11l_opy_[item.nodeid][bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ┲")].append(bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ┳")])
        _1lllllll11l_opy_[item.nodeid + bstack11l11_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ┴")] = bstack11111l1111_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1ll1lll11_opy_(item, bstack11111l1111_opy_, bstack11l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭┵"))
    except Exception as err:
        print(bstack11l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ┶"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.AFTER_EACH, bstack1l1lllll1ll_opy_.PRE, item, bstack11l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ┷"))
        return # skip all existing operations
    try:
        global bstack11l11lll1l_opy_
        bstack11lllll1l1_opy_ = 0
        if bstack11lllll1l_opy_ is True:
            bstack11lllll1l1_opy_ = int(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ┸")))
        if bstack11l11ll11_opy_.bstack1l1l1l1111_opy_() == bstack11l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ┹"):
            if bstack11l11ll11_opy_.bstack1lllll11l1_opy_() == bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ┺"):
                bstack1ll1ll11l1ll_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ┻"), None)
                bstack1l1l1l1ll_opy_ = bstack1ll1ll11l1ll_opy_ + bstack11l11_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣ┼")
                driver = getattr(item, bstack11l11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ┽"), None)
                bstack11lll1l1ll_opy_ = getattr(item, bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ┾"), None)
                bstack11l1ll11_opy_ = getattr(item, bstack11l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭┿"), None)
                PercySDK.screenshot(driver, bstack1l1l1l1ll_opy_, bstack11lll1l1ll_opy_=bstack11lll1l1ll_opy_, bstack11l1ll11_opy_=bstack11l1ll11_opy_, bstack1l11111l1l_opy_=bstack11lllll1l1_opy_)
        if not cli.bstack1l1ll1ll11l_opy_(bstack1ll11ll1lll_opy_):
            if getattr(item, bstack11l11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ╀"), False):
                bstack1ll11l1l11_opy_.bstack1l1l111l_opy_(getattr(item, bstack11l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ╁"), None), bstack11l11lll1l_opy_, logger, item)
        if not bstack1ll111l1_opy_.on():
            return
        bstack11111l1111_opy_ = {
            bstack11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ╂"): uuid4().__str__(),
            bstack11l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ╃"): bstack111111l11l_opy_().isoformat() + bstack11l11_opy_ (u"࡚࠭ࠨ╄"),
            bstack11l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ╅"): bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭╆"),
            bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ╇"): bstack11l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ╈"),
            bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ╉"): bstack11l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ╊")
        }
        _1lllllll11l_opy_[item.nodeid + bstack11l11_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ╋")] = bstack11111l1111_opy_
        bstack1ll1ll1lll11_opy_(item, bstack11111l1111_opy_, bstack11l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ╌"))
    except Exception as err:
        print(bstack11l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ╍"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lll1l1l11ll_opy_(fixturedef.argname):
        store[bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ╎")] = request.node
    elif bstack1lll1l11ll11_opy_(fixturedef.argname):
        store[bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ╏")] = request.node
    if not bstack1ll111l1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.SETUP_FIXTURE, bstack1l1lllll1ll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.SETUP_FIXTURE, bstack1l1lllll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.SETUP_FIXTURE, bstack1l1lllll1ll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.SETUP_FIXTURE, bstack1l1lllll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack11l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ═"): fixturedef.argname,
            bstack11l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ║"): bstack111l1111l11_opy_(outcome),
            bstack11l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ╒"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ╓")]
        if not _1lllllll11l_opy_.get(current_test_item.nodeid, None):
            _1lllllll11l_opy_[current_test_item.nodeid] = {bstack11l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ╔"): []}
        _1lllllll11l_opy_[current_test_item.nodeid][bstack11l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ╕")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭╖"), str(err))
if bstack11lll1111l_opy_() and bstack1ll111l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.STEP, bstack1l1lllll1ll_opy_.PRE, request, step)
            return
        try:
            _1lllllll11l_opy_[request.node.nodeid][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ╗")].bstack11lll11lll_opy_(id(step))
        except Exception as err:
            print(bstack11l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ╘"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.STEP, bstack1l1lllll1ll_opy_.POST, request, step, exception)
            return
        try:
            _1lllllll11l_opy_[request.node.nodeid][bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ╙")].bstack11111ll11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ╚"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.STEP, bstack1l1lllll1ll_opy_.POST, request, step)
            return
        try:
            bstack11111lll1l_opy_: bstack1111ll1111_opy_ = _1lllllll11l_opy_[request.node.nodeid][bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ╛")]
            bstack11111lll1l_opy_.bstack11111ll11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭╜"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1ll111l11_opy_
        try:
            if not bstack1ll111l1_opy_.on() or bstack1ll1ll111l11_opy_ != bstack11l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ╝"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ╞"), None)
            if not _1lllllll11l_opy_.get(request.node.nodeid, None):
                _1lllllll11l_opy_[request.node.nodeid] = {}
            bstack11111lll1l_opy_ = bstack1111ll1111_opy_.bstack1lll111lll1l_opy_(
                scenario, feature, request.node,
                name=bstack1lll1l1l111l_opy_(request.node, scenario),
                started_at=bstack11l1lll11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ╟"),
                tags=bstack1lll1l11l11l_opy_(feature, scenario),
                bstack1111l111l1_opy_=bstack1ll111l1_opy_.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {}
            )
            _1lllllll11l_opy_[request.node.nodeid][bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ╠")] = bstack11111lll1l_opy_
            bstack1ll1ll111111_opy_(bstack11111lll1l_opy_.uuid)
            bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ╡"), bstack11111lll1l_opy_)
        except Exception as err:
            print(bstack11l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ╢"), str(err))
def bstack1ll1ll11111l_opy_(bstack1111l1111l_opy_):
    if bstack1111l1111l_opy_ in store[bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭╣")]:
        store[bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ╤")].remove(bstack1111l1111l_opy_)
def bstack1ll1ll111111_opy_(test_uuid):
    store[bstack11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ╥")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1ll111l1_opy_.bstack1ll1llll1lll_opy_
def bstack1ll1ll11l11l_opy_(item, call, report):
    logger.debug(bstack11l11_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ╦"))
    global bstack1ll1ll111l11_opy_
    bstack11l11lllll_opy_ = bstack11l1lll11_opy_()
    if hasattr(report, bstack11l11_opy_ (u"࠭ࡳࡵࡱࡳࠫ╧")):
        bstack11l11lllll_opy_ = bstack111l111l1l1_opy_(report.stop)
    elif hasattr(report, bstack11l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭╨")):
        bstack11l11lllll_opy_ = bstack111l111l1l1_opy_(report.start)
    try:
        if getattr(report, bstack11l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭╩"), bstack11l11_opy_ (u"ࠩࠪ╪")) == bstack11l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ╫"):
            logger.debug(bstack11l11_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭╬").format(getattr(report, bstack11l11_opy_ (u"ࠬࡽࡨࡦࡰࠪ╭"), bstack11l11_opy_ (u"࠭ࠧ╮")).__str__(), bstack1ll1ll111l11_opy_))
            if bstack1ll1ll111l11_opy_ == bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ╯"):
                _1lllllll11l_opy_[item.nodeid][bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭╰")] = bstack11l11lllll_opy_
                bstack1ll1ll1l11l1_opy_(item, _1lllllll11l_opy_[item.nodeid], bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ╱"), report, call)
                store[bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ╲")] = None
            elif bstack1ll1ll111l11_opy_ == bstack11l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ╳"):
                bstack11111lll1l_opy_ = _1lllllll11l_opy_[item.nodeid][bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ╴")]
                bstack11111lll1l_opy_.set(hooks=_1lllllll11l_opy_[item.nodeid].get(bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ╵"), []))
                exception, bstack1111ll11l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1111ll11l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l11_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭╶"), bstack11l11_opy_ (u"ࠨࠩ╷"))]
                bstack11111lll1l_opy_.stop(time=bstack11l11lllll_opy_, result=Result(result=getattr(report, bstack11l11_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ╸"), bstack11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ╹")), exception=exception, bstack1111ll11l1_opy_=bstack1111ll11l1_opy_))
                bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭╺"), _1lllllll11l_opy_[item.nodeid][bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ╻")])
        elif getattr(report, bstack11l11_opy_ (u"࠭ࡷࡩࡧࡱࠫ╼"), bstack11l11_opy_ (u"ࠧࠨ╽")) in [bstack11l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ╾"), bstack11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ╿")]:
            logger.debug(bstack11l11_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ▀").format(getattr(report, bstack11l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ▁"), bstack11l11_opy_ (u"ࠬ࠭▂")).__str__(), bstack1ll1ll111l11_opy_))
            bstack1111ll11ll_opy_ = item.nodeid + bstack11l11_opy_ (u"࠭࠭ࠨ▃") + getattr(report, bstack11l11_opy_ (u"ࠧࡸࡪࡨࡲࠬ▄"), bstack11l11_opy_ (u"ࠨࠩ▅"))
            if getattr(report, bstack11l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ▆"), False):
                hook_type = bstack11l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ▇") if getattr(report, bstack11l11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ█"), bstack11l11_opy_ (u"ࠬ࠭▉")) == bstack11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ▊") else bstack11l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ▋")
                _1lllllll11l_opy_[bstack1111ll11ll_opy_] = {
                    bstack11l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭▌"): uuid4().__str__(),
                    bstack11l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭▍"): bstack11l11lllll_opy_,
                    bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭▎"): hook_type
                }
            _1lllllll11l_opy_[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ▏")] = bstack11l11lllll_opy_
            bstack1ll1ll11111l_opy_(_1lllllll11l_opy_[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ▐")])
            bstack1ll1ll1lll11_opy_(item, _1lllllll11l_opy_[bstack1111ll11ll_opy_], bstack11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ░"), report, call)
            if getattr(report, bstack11l11_opy_ (u"ࠧࡸࡪࡨࡲࠬ▒"), bstack11l11_opy_ (u"ࠨࠩ▓")) == bstack11l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ▔"):
                if getattr(report, bstack11l11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ▕"), bstack11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ▖")) == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ▗"):
                    bstack11111l1111_opy_ = {
                        bstack11l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ▘"): uuid4().__str__(),
                        bstack11l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ▙"): bstack11l1lll11_opy_(),
                        bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭▚"): bstack11l1lll11_opy_()
                    }
                    _1lllllll11l_opy_[item.nodeid] = {**_1lllllll11l_opy_[item.nodeid], **bstack11111l1111_opy_}
                    bstack1ll1ll1l11l1_opy_(item, _1lllllll11l_opy_[item.nodeid], bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ▛"))
                    bstack1ll1ll1l11l1_opy_(item, _1lllllll11l_opy_[item.nodeid], bstack11l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ▜"), report, call)
    except Exception as err:
        print(bstack11l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ▝"), str(err))
def bstack1ll1ll11llll_opy_(test, bstack11111l1111_opy_, result=None, call=None, bstack1l1ll11111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11111lll1l_opy_ = {
        bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ▞"): bstack11111l1111_opy_[bstack11l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ▟")],
        bstack11l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ■"): bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭□"),
        bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ▢"): test.name,
        bstack11l11_opy_ (u"ࠪࡦࡴࡪࡹࠨ▣"): {
            bstack11l11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ▤"): bstack11l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ▥"),
            bstack11l11_opy_ (u"࠭ࡣࡰࡦࡨࠫ▦"): inspect.getsource(test.obj)
        },
        bstack11l11_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ▧"): test.name,
        bstack11l11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ▨"): test.name,
        bstack11l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ▩"): bstack11l1ll111l_opy_.bstack11111l11ll_opy_(test),
        bstack11l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭▪"): file_path,
        bstack11l11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭▫"): file_path,
        bstack11l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ▬"): bstack11l11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ▭"),
        bstack11l11_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ▮"): file_path,
        bstack11l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ▯"): bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭▰")],
        bstack11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭▱"): bstack11l11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ▲"),
        bstack11l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ△"): {
            bstack11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ▴"): test.nodeid
        },
        bstack11l11_opy_ (u"ࠧࡵࡣࡪࡷࠬ▵"): bstack1111ll1lll1_opy_(test.own_markers)
    }
    if bstack1l1ll11111_opy_ in [bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ▶"), bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ▷")]:
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠪࡱࡪࡺࡡࠨ▸")] = {
            bstack11l11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭▹"): bstack11111l1111_opy_.get(bstack11l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ►"), [])
        }
    if bstack1l1ll11111_opy_ == bstack11l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ▻"):
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ▼")] = bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ▽")
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ▾")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ▿")]
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ◀")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ◁")]
    if result:
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭◂")] = result.outcome
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ◃")] = result.duration * 1000
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭◄")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ◅")]
        if result.failed:
            bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ◆")] = bstack1ll111l1_opy_.bstack1lll1l11lll_opy_(call.excinfo.typename)
            bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ◇")] = bstack1ll111l1_opy_.bstack1lll1111l111_opy_(call.excinfo, result)
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ◈")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ◉")]
    if outcome:
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ◊")] = bstack111l1111l11_opy_(outcome)
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ○")] = 0
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ◌")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ◍")]
        if bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ◎")] == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ●"):
            bstack11111lll1l_opy_[bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ◐")] = bstack11l11_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ◑")  # bstack1ll1ll1l1l11_opy_
            bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ◒")] = [{bstack11l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ◓"): [bstack11l11_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ◔")]}]
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ◕")] = bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ◖")]
    return bstack11111lll1l_opy_
def bstack1ll1ll11ll11_opy_(test, bstack11111l1ll1_opy_, bstack1l1ll11111_opy_, result, call, outcome, bstack1ll1ll1ll111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11111l1ll1_opy_[bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ◗")]
    hook_name = bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ◘")]
    hook_data = {
        bstack11l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭◙"): bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ◚")],
        bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ◛"): bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ◜"),
        bstack11l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ◝"): bstack11l11_opy_ (u"࠭ࡻࡾࠩ◞").format(bstack1lll1l11l1l1_opy_(hook_name)),
        bstack11l11_opy_ (u"ࠧࡣࡱࡧࡽࠬ◟"): {
            bstack11l11_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭◠"): bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ◡"),
            bstack11l11_opy_ (u"ࠪࡧࡴࡪࡥࠨ◢"): None
        },
        bstack11l11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ◣"): test.name,
        bstack11l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ◤"): bstack11l1ll111l_opy_.bstack11111l11ll_opy_(test, hook_name),
        bstack11l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ◥"): file_path,
        bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ◦"): file_path,
        bstack11l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ◧"): bstack11l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ◨"),
        bstack11l11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ◩"): file_path,
        bstack11l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ◪"): bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ◫")],
        bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ◬"): bstack11l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ◭") if bstack1ll1ll111l11_opy_ == bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ◮") else bstack11l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ◯"),
        bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭◰"): hook_type
    }
    bstack1l1ll1111ll_opy_ = bstack1111111l11_opy_(_1lllllll11l_opy_.get(test.nodeid, None))
    if bstack1l1ll1111ll_opy_:
        hook_data[bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ◱")] = bstack1l1ll1111ll_opy_
    if result:
        hook_data[bstack11l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ◲")] = result.outcome
        hook_data[bstack11l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ◳")] = result.duration * 1000
        hook_data[bstack11l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ◴")] = bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭◵")]
        if result.failed:
            hook_data[bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ◶")] = bstack1ll111l1_opy_.bstack1lll1l11lll_opy_(call.excinfo.typename)
            hook_data[bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ◷")] = bstack1ll111l1_opy_.bstack1lll1111l111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ◸")] = bstack111l1111l11_opy_(outcome)
        hook_data[bstack11l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭◹")] = 100
        hook_data[bstack11l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ◺")] = bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ◻")]
        if hook_data[bstack11l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ◼")] == bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ◽"):
            hook_data[bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ◾")] = bstack11l11_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ◿")  # bstack1ll1ll1l1l11_opy_
            hook_data[bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭☀")] = [{bstack11l11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ☁"): [bstack11l11_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ☂")]}]
    if bstack1ll1ll1ll111_opy_:
        hook_data[bstack11l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ☃")] = bstack1ll1ll1ll111_opy_.result
        hook_data[bstack11l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ☄")] = bstack111l11l1ll1_opy_(bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ★")], bstack11111l1ll1_opy_[bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ☆")])
        hook_data[bstack11l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ☇")] = bstack11111l1ll1_opy_[bstack11l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ☈")]
        if hook_data[bstack11l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ☉")] == bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ☊"):
            hook_data[bstack11l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ☋")] = bstack1ll111l1_opy_.bstack1lll1l11lll_opy_(bstack1ll1ll1ll111_opy_.exception_type)
            hook_data[bstack11l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ☌")] = [{bstack11l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ☍"): bstack1111lll111l_opy_(bstack1ll1ll1ll111_opy_.exception)}]
    return hook_data
def bstack1ll1ll1l11l1_opy_(test, bstack11111l1111_opy_, bstack1l1ll11111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11l11_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ☎").format(bstack1l1ll11111_opy_))
    bstack11111lll1l_opy_ = bstack1ll1ll11llll_opy_(test, bstack11111l1111_opy_, result, call, bstack1l1ll11111_opy_, outcome)
    driver = getattr(test, bstack11l11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ☏"), None)
    if bstack1l1ll11111_opy_ == bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ☐") and driver:
        bstack11111lll1l_opy_[bstack11l11_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ☑")] = bstack1ll111l1_opy_.bstack1111l11l1l_opy_(driver)
    if bstack1l1ll11111_opy_ == bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ☒"):
        bstack1l1ll11111_opy_ = bstack11l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ☓")
    bstack11111l1lll_opy_ = {
        bstack11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ☔"): bstack1l1ll11111_opy_,
        bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ☕"): bstack11111lll1l_opy_
    }
    bstack1ll111l1_opy_.bstack11l11lll_opy_(bstack11111l1lll_opy_)
    if bstack1l1ll11111_opy_ == bstack11l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ☖"):
        threading.current_thread().bstackTestMeta = {bstack11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ☗"): bstack11l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ☘")}
    elif bstack1l1ll11111_opy_ == bstack11l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ☙"):
        threading.current_thread().bstackTestMeta = {bstack11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ☚"): getattr(result, bstack11l11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ☛"), bstack11l11_opy_ (u"ࠬ࠭☜"))}
def bstack1ll1ll1lll11_opy_(test, bstack11111l1111_opy_, bstack1l1ll11111_opy_, result=None, call=None, outcome=None, bstack1ll1ll1ll111_opy_=None):
    logger.debug(bstack11l11_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭☝").format(bstack1l1ll11111_opy_))
    hook_data = bstack1ll1ll11ll11_opy_(test, bstack11111l1111_opy_, bstack1l1ll11111_opy_, result, call, outcome, bstack1ll1ll1ll111_opy_)
    bstack11111l1lll_opy_ = {
        bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ☞"): bstack1l1ll11111_opy_,
        bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ☟"): hook_data
    }
    bstack1ll111l1_opy_.bstack11l11lll_opy_(bstack11111l1lll_opy_)
def bstack1111111l11_opy_(bstack11111l1111_opy_):
    if not bstack11111l1111_opy_:
        return None
    if bstack11111l1111_opy_.get(bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ☠"), None):
        return getattr(bstack11111l1111_opy_[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭☡")], bstack11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ☢"), None)
    return bstack11111l1111_opy_.get(bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ☣"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.LOG, bstack1l1lllll1ll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_.LOG, bstack1l1lllll1ll_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack1ll111l1_opy_.on():
            return
        places = [bstack11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ☤"), bstack11l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ☥"), bstack11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ☦")]
        logs = []
        for bstack1ll1ll1l11ll_opy_ in places:
            records = caplog.get_records(bstack1ll1ll1l11ll_opy_)
            bstack1ll1ll1l1lll_opy_ = bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ☧") if bstack1ll1ll1l11ll_opy_ == bstack11l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ☨") else bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☩")
            bstack1ll1ll1111l1_opy_ = request.node.nodeid + (bstack11l11_opy_ (u"ࠬ࠭☪") if bstack1ll1ll1l11ll_opy_ == bstack11l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ☫") else bstack11l11_opy_ (u"ࠧ࠮ࠩ☬") + bstack1ll1ll1l11ll_opy_)
            test_uuid = bstack1111111l11_opy_(_1lllllll11l_opy_.get(bstack1ll1ll1111l1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11111lll11l_opy_(record.message):
                    continue
                logs.append({
                    bstack11l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ☭"): bstack1111l1111l1_opy_(record.created).isoformat() + bstack11l11_opy_ (u"ࠩ࡝ࠫ☮"),
                    bstack11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ☯"): record.levelname,
                    bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ☰"): record.message,
                    bstack1ll1ll1l1lll_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1ll111l1_opy_.bstack1l1l1l11l_opy_(logs)
    except Exception as err:
        print(bstack11l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ☱"), str(err))
def bstack111lll1l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l1ll111_opy_
    bstack1l111lll1l_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ☲"), None) and bstack11ll11l11_opy_(
            threading.current_thread(), bstack11l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭☳"), None)
    bstack11llll11l_opy_ = getattr(driver, bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ☴"), None) != None and getattr(driver, bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ☵"), None) == True
    if sequence == bstack11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ☶") and driver != None:
      if not bstack1l1l1ll111_opy_ and bstack1l111lllll1_opy_() and bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ☷") in CONFIG and CONFIG[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ☸")] == True and bstack1l1lll111l_opy_.bstack1lll1l1ll_opy_(driver_command) and (bstack11llll11l_opy_ or bstack1l111lll1l_opy_) and not bstack11ll1111l1_opy_(args):
        try:
          bstack1l1l1ll111_opy_ = True
          logger.debug(bstack11l11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ☹").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ☺").format(str(err)))
        bstack1l1l1ll111_opy_ = False
    if sequence == bstack11l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ☻"):
        if driver_command == bstack11l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭☼"):
            bstack1ll111l1_opy_.bstack1l111111l_opy_({
                bstack11l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ☽"): response[bstack11l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ☾")],
                bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☿"): store[bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ♀")]
            })
def bstack11ll1l1l11_opy_():
    global bstack111l1llll1_opy_
    logger_utils.bstack111l1ll111_opy_()
    logging.shutdown()
    bstack1ll111l1_opy_.bstack11111l1l1l_opy_()
    for driver in bstack111l1llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllll111ll_opy_(*args):
    global bstack111l1llll1_opy_
    bstack1ll111l1_opy_.bstack11111l1l1l_opy_()
    for driver in bstack111l1llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1ll11_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll1llll1_opy_(self, *args, **kwargs):
    bstack1ll1ll1ll_opy_ = bstack11l111111_opy_(self, *args, **kwargs)
    bstack111l1l1l_opy_ = getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ♁"), None)
    if bstack111l1l1l_opy_ and bstack111l1l1l_opy_.get(bstack11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ♂"), bstack11l11_opy_ (u"ࠩࠪ♃")) == bstack11l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ♄"):
        bstack1ll111l1_opy_.bstack1ll1111l11_opy_(self)
    return bstack1ll1ll1ll_opy_
@measure(event_name=EVENTS.bstack11lllll1ll_opy_, stage=STAGE.bstack111l1ll11l_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1l1l1lll11_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
    if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ♅")):
        return
    bstack11l1l1111_opy_.bstack1ll111ll11_opy_(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ♆"), True)
    global bstack11l1111ll1_opy_
    global bstack1l1lllll_opy_
    bstack11l1111ll1_opy_ = framework_name
    logger.info(bstack11ll111lll_opy_.format(bstack11l1111ll1_opy_.split(bstack11l11_opy_ (u"࠭࠭ࠨ♇"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l111lllll1_opy_():
            Service.start = bstack1l1l1ll1l_opy_
            Service.stop = bstack1ll1l1ll_opy_
            webdriver.Remote.get = bstack1ll1l1l111_opy_
            webdriver.Remote.__init__ = bstack1ll111111_opy_
            if not isinstance(os.getenv(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ♈")), str):
                return
            WebDriver.quit = bstack1ll11ll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1ll111l1_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1llll1_opy_
        bstack1l1lllll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11l11_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭♉")):
        bstack1l1lllll_opy_ = eval(os.environ.get(bstack11l11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ♊")))
    if not bstack1l1lllll_opy_:
        bstack1l11l1ll1l_opy_(bstack11l11_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ♋"), bstack11111lll_opy_)
    if bstack1lll1ll11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11l11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ♌")) and callable(getattr(RemoteConnection, bstack11l11_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭♍"))):
                RemoteConnection._get_proxy_url = bstack1l11ll1l1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l11ll1l1_opy_
        except Exception as e:
            logger.error(bstack11l1111l1_opy_.format(str(e)))
    if bstack11l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭♎") in str(framework_name).lower():
        if not bstack1l111lllll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l111llll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1ll1l1_opy_
            Config.getoption = bstack11l1ll1l1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l111ll1ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll11l1l1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll11ll11l_opy_(self):
    global bstack11l1111ll1_opy_
    global bstack1111ll1l1_opy_
    global bstack11l111l1ll_opy_
    try:
        if bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ♏") in bstack11l1111ll1_opy_ and self.session_id != None and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ♐"), bstack11l11_opy_ (u"ࠩࠪ♑")) != bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ♒"):
            bstack111l111lll_opy_ = bstack11l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ♓") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ♔")
            bstack11111l111_opy_(logger, True)
            if os.environ.get(bstack11l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ♕"), None):
                self.execute_script(
                    bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ♖") + json.dumps(
                        os.environ.get(bstack11l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ♗"))) + bstack11l11_opy_ (u"ࠩࢀࢁࠬ♘"))
            if self != None:
                bstack1ll1l1l1_opy_(self, bstack111l111lll_opy_, bstack11l11_opy_ (u"ࠪ࠰ࠥ࠭♙").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l1ll1ll11l_opy_(bstack1ll11ll1lll_opy_):
            item = store.get(bstack11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ♚"), None)
            if item is not None and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ♛"), None):
                bstack1ll11l1l11_opy_.bstack1l1l111l_opy_(self, bstack11l11lll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l11_opy_ (u"࠭ࠧ♜")
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ♝") + str(e))
    bstack11l111l1ll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l11ll1_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll111111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1111ll1l1_opy_
    global bstack11l1111lll_opy_
    global bstack11lllll1l_opy_
    global bstack11l1111ll1_opy_
    global bstack11l111111_opy_
    global bstack111l1llll1_opy_
    global bstack1ll1l1l1ll_opy_
    global bstack1l1lll1l11_opy_
    global bstack11l11lll1l_opy_
    CONFIG[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ♞")] = str(bstack11l1111ll1_opy_) + str(__version__)
    command_executor = bstack1l1llll1ll_opy_(bstack1ll1l1l1ll_opy_, CONFIG)
    logger.debug(bstack1111ll11l_opy_.format(command_executor))
    proxy = bstack1l11l1lll_opy_(CONFIG, proxy)
    bstack11lllll1l1_opy_ = 0
    try:
        if bstack11lllll1l_opy_ is True:
            bstack11lllll1l1_opy_ = int(os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ♟")))
    except:
        bstack11lllll1l1_opy_ = 0
    bstack11ll1ll1_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11lllll1l1_opy_)
    logger.debug(bstack1l11ll1ll_opy_.format(str(bstack11ll1ll1_opy_)))
    bstack11l11lll1l_opy_ = CONFIG.get(bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭♠"))[bstack11lllll1l1_opy_]
    if bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ♡") in CONFIG and CONFIG[bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ♢")]:
        bstack1l1111l111_opy_(bstack11ll1ll1_opy_, bstack1l1lll1l11_opy_)
    if bstack1lllll111l_opy_.bstack1llll1lll1_opy_(CONFIG, bstack11lllll1l1_opy_) and bstack1lllll111l_opy_.bstack11l111l1l_opy_(bstack11ll1ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l1ll1ll11l_opy_(bstack1ll11ll1lll_opy_):
            bstack1lllll111l_opy_.set_capabilities(bstack11ll1ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1lllll1ll_opy_ = bstack11llll11ll_opy_(desired_capabilities)
        bstack1lllll1ll_opy_[bstack11l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭♣")] = bstack1l1l1llll_opy_(CONFIG)
        bstack1l11l1111l_opy_ = bstack1lll111l1_opy_(bstack1lllll1ll_opy_)
        if bstack1l11l1111l_opy_:
            bstack11ll1ll1_opy_ = update(bstack1l11l1111l_opy_, bstack11ll1ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1lllll_opy_(options, bstack11ll1ll1_opy_)
    if not options:
        options = bstack1111ll1ll1_opy_(bstack11ll1ll1_opy_)
    if proxy and bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ♤")):
        options.proxy(proxy)
    if options and bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ♥")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l1lll1_opy_() < version.parse(bstack11l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ♦")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11ll1ll1_opy_)
    logger.info(bstack111l1l1l1_opy_)
    bstack11ll11ll1l_opy_.end(EVENTS.bstack11lllll1ll_opy_.value, EVENTS.bstack11lllll1ll_opy_.value + bstack11l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ♧"),
                               EVENTS.bstack11lllll1ll_opy_.value + bstack11l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ♨"), True, None)
    try:
        if bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ♩")):
            bstack11l111111_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ♪")):
            bstack11l111111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ♫")):
            bstack11l111111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack11l111111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11llll111l_opy_:
        logger.error(bstack1l1lll1lll_opy_.format(bstack11l11_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧ♬"), str(bstack11llll111l_opy_)))
        raise bstack11llll111l_opy_
    try:
        bstack1111lll1_opy_ = bstack11l11_opy_ (u"ࠩࠪ♭")
        if bstack111l1lll1_opy_() >= version.parse(bstack11l11_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ♮")):
            bstack1111lll1_opy_ = self.caps.get(bstack11l11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ♯"))
        else:
            bstack1111lll1_opy_ = self.capabilities.get(bstack11l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ♰"))
        if bstack1111lll1_opy_:
            bstack111llll1_opy_(bstack1111lll1_opy_)
            if bstack111l1lll1_opy_() <= version.parse(bstack11l11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭♱")):
                self.command_executor._url = bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ♲") + bstack1ll1l1l1ll_opy_ + bstack11l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ♳")
            else:
                self.command_executor._url = bstack11l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ♴") + bstack1111lll1_opy_ + bstack11l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ♵")
            logger.debug(bstack11l1l1l1_opy_.format(bstack1111lll1_opy_))
        else:
            logger.debug(bstack1lll111111_opy_.format(bstack11l11_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ♶")))
    except Exception as e:
        logger.debug(bstack1lll111111_opy_.format(e))
    bstack1111ll1l1_opy_ = self.session_id
    if bstack11l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ♷") in bstack11l1111ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ♸"), None)
        if item:
            bstack1ll1ll1l111l_opy_ = getattr(item, bstack11l11_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ♹"), False)
            if not getattr(item, bstack11l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ♺"), None) and bstack1ll1ll1l111l_opy_:
                setattr(store[bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭♻")], bstack11l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ♼"), self)
        bstack111l1l1l_opy_ = getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ♽"), None)
        if bstack111l1l1l_opy_ and bstack111l1l1l_opy_.get(bstack11l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ♾"), bstack11l11_opy_ (u"࠭ࠧ♿")) == bstack11l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⚀"):
            bstack1ll111l1_opy_.bstack1ll1111l11_opy_(self)
    bstack111l1llll1_opy_.append(self)
    if bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⚁") in CONFIG and bstack11l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⚂") in CONFIG[bstack11l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⚃")][bstack11lllll1l1_opy_]:
        bstack11l1111lll_opy_ = CONFIG[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⚄")][bstack11lllll1l1_opy_][bstack11l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⚅")]
    logger.debug(bstack1ll11111ll_opy_.format(bstack1111ll1l1_opy_))
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=bstack11l1111lll_opy_)
def bstack1ll1l1l111_opy_(self, url):
    global bstack11ll11ll_opy_
    global CONFIG
    try:
        bstack1ll111ll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1ll11l_opy_.format(str(err)))
    try:
        bstack11ll11ll_opy_(self, url)
    except Exception as e:
        try:
            bstack111lll11l1_opy_ = str(e)
            if any(err_msg in bstack111lll11l1_opy_ for err_msg in bstack11ll11l1l1_opy_):
                bstack1ll111ll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1ll11l_opy_.format(str(err)))
        raise e
def bstack1l1lllll1l_opy_(item, when):
    global bstack1ll111111l_opy_
    try:
        bstack1ll111111l_opy_(item, when)
    except Exception as e:
        pass
def bstack1l111ll1ll_opy_(item, call, rep):
    global bstack11l1ll11l1_opy_
    global bstack111l1llll1_opy_
    name = bstack11l11_opy_ (u"࠭ࠧ⚆")
    try:
        if rep.when == bstack11l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⚇"):
            bstack1111ll1l1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⚈"))
            try:
                if (str(skipSessionName).lower() != bstack11l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⚉")):
                    name = str(rep.nodeid)
                    bstack11111lll1_opy_ = bstack1lll1l1l1l_opy_(bstack11l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⚊"), name, bstack11l11_opy_ (u"ࠫࠬ⚋"), bstack11l11_opy_ (u"ࠬ࠭⚌"), bstack11l11_opy_ (u"࠭ࠧ⚍"), bstack11l11_opy_ (u"ࠧࠨ⚎"))
                    os.environ[bstack11l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⚏")] = name
                    for driver in bstack111l1llll1_opy_:
                        if bstack1111ll1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack11111lll1_opy_)
            except Exception as e:
                logger.debug(bstack11l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⚐").format(str(e)))
            try:
                bstack11ll1llll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⚑"):
                    status = bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⚒") if rep.outcome.lower() == bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⚓") else bstack11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⚔")
                    reason = bstack11l11_opy_ (u"ࠧࠨ⚕")
                    if status == bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⚖"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ⚗") if status == bstack11l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⚘") else bstack11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⚙")
                    data = name + bstack11l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ⚚") if status == bstack11l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⚛") else name + bstack11l11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ⚜") + reason
                    bstack1lll111lll_opy_ = bstack1lll1l1l1l_opy_(bstack11l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⚝"), bstack11l11_opy_ (u"ࠩࠪ⚞"), bstack11l11_opy_ (u"ࠪࠫ⚟"), bstack11l11_opy_ (u"ࠫࠬ⚠"), level, data)
                    for driver in bstack111l1llll1_opy_:
                        if bstack1111ll1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll111lll_opy_)
            except Exception as e:
                logger.debug(bstack11l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⚡").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ⚢").format(str(e)))
    bstack11l1ll11l1_opy_(item, call, rep)
notset = Notset()
def bstack11l1ll1l1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l111l1ll1_opy_
    if str(name).lower() == bstack11l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ⚣"):
        return bstack11l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ⚤")
    else:
        return bstack1l111l1ll1_opy_(self, name, default, skip)
def bstack1l11ll1l1_opy_(self):
    global CONFIG
    global bstack111lllllll_opy_
    try:
        proxy = bstack111l11l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⚥")):
                proxies = bstack11l11l1ll1_opy_(proxy, bstack1l1llll1ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1111ll11_opy_ = proxies.popitem()
                    if bstack11l11_opy_ (u"ࠥ࠾࠴࠵ࠢ⚦") in bstack1111ll11_opy_:
                        return bstack1111ll11_opy_
                    else:
                        return bstack11l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⚧") + bstack1111ll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ⚨").format(str(e)))
    return bstack111lllllll_opy_(self)
def bstack1lll1ll11_opy_():
    return (bstack11l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⚩") in CONFIG or bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⚪") in CONFIG) and bstack1l1l1l1lll_opy_() and bstack111l1lll1_opy_() >= version.parse(
        bstack11ll111ll1_opy_)
def bstack11ll11ll1_opy_(self,
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
    global bstack11l1111lll_opy_
    global bstack11lllll1l_opy_
    global bstack11l1111ll1_opy_
    CONFIG[bstack11l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⚫")] = str(bstack11l1111ll1_opy_) + str(__version__)
    bstack11lllll1l1_opy_ = 0
    try:
        if bstack11lllll1l_opy_ is True:
            bstack11lllll1l1_opy_ = int(os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⚬")))
    except:
        bstack11lllll1l1_opy_ = 0
    CONFIG[bstack11l11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ⚭")] = True
    bstack11ll1ll1_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11lllll1l1_opy_)
    logger.debug(bstack1l11ll1ll_opy_.format(str(bstack11ll1ll1_opy_)))
    if CONFIG.get(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⚮")):
        bstack1l1111l111_opy_(bstack11ll1ll1_opy_, bstack1l1lll1l11_opy_)
    if bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⚯") in CONFIG and bstack11l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⚰") in CONFIG[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⚱")][bstack11lllll1l1_opy_]:
        bstack11l1111lll_opy_ = CONFIG[bstack11l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⚲")][bstack11lllll1l1_opy_][bstack11l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⚳")]
    import urllib
    import json
    if bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⚴") in CONFIG and str(CONFIG[bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⚵")]).lower() != bstack11l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⚶"):
        bstack1lll1l1l11_opy_ = bstack1l1ll1ll11_opy_()
        cdpUrl = bstack1lll1l1l11_opy_ + urllib.parse.quote(json.dumps(bstack11ll1ll1_opy_))
    else:
        cdpUrl = bstack11l11_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ⚷") + urllib.parse.quote(json.dumps(bstack11ll1ll1_opy_))
    browser = self.connect(cdpUrl)
    return browser
def bstack11l111llll_opy_():
    global bstack1l1lllll_opy_
    global bstack11l1111ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111lll_opy_
        if not bstack1l111lllll1_opy_():
            global bstack11llllll11_opy_
            if not bstack11llllll11_opy_:
                from bstack_utils.helper import bstack1ll1llll11_opy_, bstack1l1lll1l_opy_
                bstack11llllll11_opy_ = bstack1ll1llll11_opy_()
                bstack1l1lll1l_opy_(bstack11l1111ll1_opy_)
            BrowserType.connect = bstack1l111lll_opy_
            return
        BrowserType.launch = bstack11ll11ll1_opy_
        bstack1l1lllll_opy_ = True
    except Exception as e:
        pass
def bstack1ll1ll1l1111_opy_():
    global CONFIG
    global bstack11lll1l11_opy_
    global bstack1ll1l1l1ll_opy_
    global bstack1l1lll1l11_opy_
    global bstack11lllll1l_opy_
    global bstack1l1ll1llll_opy_
    CONFIG = json.loads(os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭⚸")))
    bstack11lll1l11_opy_ = eval(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ⚹")))
    bstack1ll1l1l1ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ⚺"))
    bstack11111llll_opy_(CONFIG, bstack11lll1l11_opy_)
    bstack1l1ll1llll_opy_ = logger_utils.configure_logger(CONFIG, bstack1l1ll1llll_opy_)
    if cli.bstack11111l1l_opy_():
        bstack1l11l11111_opy_.invoke(bstack11ll111111_opy_.CONNECT, bstack111l1ll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⚻"), bstack11l11_opy_ (u"ࠫ࠵࠭⚼")))
        cli.bstack1ll1111l11l_opy_(cli_context.platform_index)
        cli.bstack1ll1l111l1l_opy_(bstack1l1llll1ll_opy_(bstack1ll1l1l1ll_opy_, CONFIG), cli_context.platform_index, bstack1111ll1ll1_opy_)
        cli.bstack1ll11l11lll_opy_()
        logger.debug(bstack11l11_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⚽") + str(cli_context.platform_index) + bstack11l11_opy_ (u"ࠨࠢ⚾"))
        return # skip all existing operations
    global bstack11l111111_opy_
    global bstack11l111l1ll_opy_
    global bstack11ll1l1111_opy_
    global bstack111llll11l_opy_
    global bstack111l1l111_opy_
    global bstack1l1l1ll1ll_opy_
    global bstack1l1111l1ll_opy_
    global bstack11ll11ll_opy_
    global bstack111lllllll_opy_
    global bstack1l111l1ll1_opy_
    global bstack1ll111111l_opy_
    global bstack11l1ll11l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l111111_opy_ = webdriver.Remote.__init__
        bstack11l111l1ll_opy_ = WebDriver.quit
        bstack1l1111l1ll_opy_ = WebDriver.close
        bstack11ll11ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⚿") in CONFIG or bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⛀") in CONFIG) and bstack1l1l1l1lll_opy_():
        if bstack111l1lll1_opy_() < version.parse(bstack11ll111ll1_opy_):
            logger.error(bstack1111lllll_opy_.format(bstack111l1lll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11l11_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⛁")) and callable(getattr(RemoteConnection, bstack11l11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⛂"))):
                    bstack111lllllll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack111lllllll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11l1111l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l111l1ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll111111l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack11l11_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦ⛃"), bstack11lllll11_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack11l1ll11l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭⛄"))
    bstack1l1lll1l11_opy_ = CONFIG.get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ⛅"), {}).get(bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⛆"))
    bstack11lllll1l_opy_ = True
    bstack1l1l1lll11_opy_(bstack1lllllll1l_opy_)
if (bstack1111l1ll1l1_opy_()):
    bstack1ll1ll1l1111_opy_()
@error_handler(class_method=False)
def bstack1ll1ll11ll1l_opy_(hook_name, event, bstack11l1lll111l_opy_=None):
    if hook_name not in [bstack11l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⛇"), bstack11l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⛈"), bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⛉"), bstack11l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⛊"), bstack11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⛋"), bstack11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⛌"), bstack11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⛍"), bstack11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ⛎")]:
        return
    node = store[bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⛏")]
    if hook_name in [bstack11l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⛐"), bstack11l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⛑")]:
        node = store[bstack11l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ⛒")]
    elif hook_name in [bstack11l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⛓"), bstack11l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⛔")]:
        node = store[bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭⛕")]
    hook_type = bstack1lll1l1l1l1l_opy_(hook_name)
    if event == bstack11l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⛖"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_[hook_type], bstack1l1lllll1ll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack11111l1ll1_opy_ = {
            bstack11l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⛗"): uuid,
            bstack11l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⛘"): bstack11l1lll11_opy_(),
            bstack11l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ⛙"): bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⛚"),
            bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⛛"): hook_type,
            bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⛜"): hook_name
        }
        store[bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⛝")].append(uuid)
        bstack1ll1ll1111ll_opy_ = node.nodeid
        if hook_type == bstack11l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⛞"):
            if not _1lllllll11l_opy_.get(bstack1ll1ll1111ll_opy_, None):
                _1lllllll11l_opy_[bstack1ll1ll1111ll_opy_] = {bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⛟"): []}
            _1lllllll11l_opy_[bstack1ll1ll1111ll_opy_][bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⛠")].append(bstack11111l1ll1_opy_[bstack11l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⛡")])
        _1lllllll11l_opy_[bstack1ll1ll1111ll_opy_ + bstack11l11_opy_ (u"ࠧ࠮ࠩ⛢") + hook_name] = bstack11111l1ll1_opy_
        bstack1ll1ll1lll11_opy_(node, bstack11111l1ll1_opy_, bstack11l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⛣"))
    elif event == bstack11l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⛤"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1l1lllllll1_opy_[hook_type], bstack1l1lllll1ll_opy_.POST, node, None, bstack11l1lll111l_opy_)
            return
        bstack1111ll11ll_opy_ = node.nodeid + bstack11l11_opy_ (u"ࠪ࠱ࠬ⛥") + hook_name
        _1lllllll11l_opy_[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⛦")] = bstack11l1lll11_opy_()
        bstack1ll1ll11111l_opy_(_1lllllll11l_opy_[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⛧")])
        bstack1ll1ll1lll11_opy_(node, _1lllllll11l_opy_[bstack1111ll11ll_opy_], bstack11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⛨"), bstack1ll1ll1ll111_opy_=bstack11l1lll111l_opy_)
def bstack1ll1ll111lll_opy_():
    global bstack1ll1ll111l11_opy_
    if bstack11lll1111l_opy_():
        bstack1ll1ll111l11_opy_ = bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⛩")
    else:
        bstack1ll1ll111l11_opy_ = bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⛪")
@bstack1ll111l1_opy_.bstack1ll1llll1lll_opy_
def bstack1ll1ll11l111_opy_():
    bstack1ll1ll111lll_opy_()
    if cli.is_running():
        try:
            bstack11111ll1l1l_opy_(bstack1ll1ll11ll1l_opy_)
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⛫").format(e))
        return
    if bstack1l1l1l1lll_opy_():
        bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
        bstack11l11_opy_ (u"ࠪࠫࠬࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡃࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡩࡨࡸࡸࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠮ࡹࡵࡥࡵࡶࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡳࡷࡱࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡯࡮ࠡࡣࠣࡨ࡮࡬ࡦࡦࡴࡨࡲࡹࠦࡰࡳࡱࡦࡩࡸࡹࠠࡪࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡹࡸࠦࡷࡦࠢࡱࡩࡪࡪࠠࡵࡱࠣࡹࡸ࡫ࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡒࡤࡸࡨ࡮ࠨࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠬࠤ࡫ࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠫࠬ࠭⛬")
        if bstack11l1l1111_opy_.get_property(bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⛭")):
            if CONFIG.get(bstack11l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⛮")) is not None and int(CONFIG[bstack11l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⛯")]) > 1:
                bstack111l111l1_opy_(bstack111lll1l1_opy_)
            return
        bstack111l111l1_opy_(bstack111lll1l1_opy_)
    try:
        bstack11111ll1l1l_opy_(bstack1ll1ll11ll1l_opy_)
    except Exception as e:
        logger.debug(bstack11l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⛰").format(e))
bstack1ll1ll11l111_opy_()