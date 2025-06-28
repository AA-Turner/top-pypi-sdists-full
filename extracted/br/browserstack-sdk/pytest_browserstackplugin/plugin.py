# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l11l1llll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11lll1l1ll_opy_, bstack1l1l1l1l1l_opy_, update, bstack1ll1l1111l_opy_,
                                       bstack1ll11llll1_opy_, bstack1ll11l11l1_opy_, bstack1l1ll11l_opy_, bstack1lll1l11_opy_,
                                       bstack1lllll11ll_opy_, bstack1l1l1llll1_opy_, bstack11ll111l1l_opy_,
                                       bstack1lll1l11l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11l111l1ll_opy_)
from browserstack_sdk.bstack1l11l1l1ll_opy_ import bstack1llll111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11lll1ll_opy_
from bstack_utils.capture import bstack111lll1111_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11lll111_opy_, bstack1ll1ll1111_opy_, bstack1l1lllll1l_opy_, \
    bstack11llll11ll_opy_
from bstack_utils.helper import bstack11l1ll11ll_opy_, bstack11l11l1l1l1_opy_, bstack1111lll11l_opy_, bstack11l1l1l1l_opy_, bstack1l1lll11111_opy_, bstack1llllll1l_opy_, \
    bstack11l1l11111l_opy_, \
    bstack11l1l11l111_opy_, bstack1111l1l1l_opy_, bstack1llll1llll_opy_, bstack11l111lllll_opy_, bstack1ll11l111l_opy_, Notset, \
    bstack1l1l111l11_opy_, bstack11l11ll1l11_opy_, bstack11l11ll1lll_opy_, Result, bstack11l111ll11l_opy_, bstack11l1111l1ll_opy_, bstack111l1111ll_opy_, \
    bstack1l11l1ll1_opy_, bstack11lll11l1_opy_, bstack11lll1lll1_opy_, bstack111lll1llll_opy_
from bstack_utils.bstack111lll111ll_opy_ import bstack111ll1lll1l_opy_
from bstack_utils.messages import bstack1llll1ll_opy_, bstack1l1l111111_opy_, bstack1l1llll1ll_opy_, bstack1l1111111_opy_, bstack1l111l11ll_opy_, \
    bstack11lll1l11_opy_, bstack1l1l1111l_opy_, bstack111ll1111_opy_, bstack11l1ll1l_opy_, bstack1l1l11ll_opy_, \
    bstack1l1l1111l1_opy_, bstack11l111l1l_opy_
from bstack_utils.proxy import bstack11l1lll11_opy_, bstack11l1l11ll1_opy_
from bstack_utils.bstack111l1l1l_opy_ import bstack11111l1ll11_opy_, bstack11111l111ll_opy_, bstack11111l11l1l_opy_, bstack11111ll1111_opy_, \
    bstack11111l1l11l_opy_, bstack11111l11ll1_opy_, bstack11111l1ll1l_opy_, bstack1l111l1lll_opy_, bstack11111l1l1ll_opy_
from bstack_utils.bstack1ll11ll1_opy_ import bstack11l1l1111_opy_
from bstack_utils.bstack1llll1111l_opy_ import bstack111111ll1_opy_, bstack11ll1lllll_opy_, bstack11lll11l1l_opy_, \
    bstack1l1ll1lll1_opy_, bstack1ll1111l11_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack111lll11l1_opy_
from bstack_utils.bstack111ll1lll1_opy_ import bstack111l1ll1l_opy_
import bstack_utils.accessibility as bstack1l11ll1lll_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack1l1lll1l_opy_
from bstack_utils.bstack1ll1l1l1l_opy_ import bstack1ll1l1l1l_opy_
from bstack_utils.bstack111l11ll_opy_ import bstack11l1ll1l1_opy_
from browserstack_sdk.__init__ import bstack1l1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import bstack1llll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l_opy_ import bstack1l1l111l_opy_, bstack1l11111l1l_opy_, bstack1l1l1lll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111lll1ll_opy_, bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1l111l_opy_ import bstack1l1l111l_opy_, bstack1l11111l1l_opy_, bstack1l1l1lll1l_opy_
bstack11llllll11_opy_ = None
bstack111l11l1l_opy_ = None
bstack1lll11111_opy_ = None
bstack11l111l1l1_opy_ = None
bstack11l1111l11_opy_ = None
bstack11l1l11ll_opy_ = None
bstack1lll1llll_opy_ = None
bstack11ll11lll1_opy_ = None
bstack1lll1ll11_opy_ = None
bstack11lllll1_opy_ = None
bstack1lll1lll1l_opy_ = None
bstack1l11l1lll_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1l11lll1l_opy_ = bstack1l1ll1_opy_ (u"ࠧࠨℲ")
CONFIG = {}
bstack1l1lllllll_opy_ = False
bstack1l1ll1l11l_opy_ = bstack1l1ll1_opy_ (u"ࠨࠩℳ")
bstack1111ll11l_opy_ = bstack1l1ll1_opy_ (u"ࠩࠪℴ")
bstack11111ll1l_opy_ = False
bstack1ll1l11lll_opy_ = []
bstack111111l11_opy_ = bstack11lll111_opy_
bstack1llll1l1l11l_opy_ = bstack1l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪℵ")
bstack1ll111l11_opy_ = {}
bstack11111ll1_opy_ = None
bstack1ll1ll1l11_opy_ = False
logger = bstack11lll1ll_opy_.get_logger(__name__, bstack111111l11_opy_)
store = {
    bstack1l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨℶ"): []
}
bstack1llll1ll1l1l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l111l1l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111lll1ll_opy_(
    test_framework_name=bstack1l111ll11_opy_[bstack1l1ll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩℷ")] if bstack1ll11l111l_opy_() else bstack1l111ll11_opy_[bstack1l1ll1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭ℸ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l11l1lll_opy_(page, bstack11l11ll1_opy_):
    try:
        page.evaluate(bstack1l1ll1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣℹ"),
                      bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ℺") + json.dumps(
                          bstack11l11ll1_opy_) + bstack1l1ll1_opy_ (u"ࠤࢀࢁࠧ℻"))
    except Exception as e:
        print(bstack1l1ll1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣℼ"), e)
def bstack1ll11lllll_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1ll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧℽ"), bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪℾ") + json.dumps(
            message) + bstack1l1ll1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩℿ") + json.dumps(level) + bstack1l1ll1_opy_ (u"ࠧࡾࡿࠪ⅀"))
    except Exception as e:
        print(bstack1l1ll1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⅁"), e)
def pytest_configure(config):
    global bstack1l1ll1l11l_opy_
    global CONFIG
    bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
    config.args = bstack111l1ll1l_opy_.bstack1llll1llllll_opy_(config.args)
    bstack11lll111ll_opy_.bstack1lll111l1l_opy_(bstack11lll1lll1_opy_(config.getoption(bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⅂"))))
    try:
        bstack11lll1ll_opy_.bstack111ll11l1ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.CONNECT, bstack1l1l1lll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⅃"), bstack1l1ll1_opy_ (u"ࠫ࠵࠭⅄")))
        config = json.loads(os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦⅅ"), bstack1l1ll1_opy_ (u"ࠨࡻࡾࠤⅆ")))
        cli.bstack1ll1lll1l1l_opy_(bstack1llll1llll_opy_(bstack1l1ll1l11l_opy_, CONFIG), cli_context.platform_index, bstack1ll1l1111l_opy_)
    if cli.bstack1llll11ll11_opy_(bstack1llll1ll1ll_opy_):
        cli.bstack1ll1lll11l1_opy_()
        logger.debug(bstack1l1ll1_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨⅇ") + str(cli_context.platform_index) + bstack1l1ll1_opy_ (u"ࠣࠤⅈ"))
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.BEFORE_ALL, bstack1ll1lllll1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1ll1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢⅉ"), None)
    if cli.is_running() and when == bstack1l1ll1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⅊"):
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.LOG_REPORT, bstack1ll1lllll1l_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1l1ll1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⅋"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⅌")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ⅍"), bstack1l1ll1_opy_ (u"ࠢࡼࡿࠥⅎ")))
            if bstack11l1ll1l1_opy_.bstack1ll1ll1ll1_opy_(config):
                bstack111l11111ll_opy_ = bstack11l1ll1l1_opy_.bstack1l1111l111_opy_(config)
                if item.execution_count > bstack111l11111ll_opy_:
                    print(bstack1l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡸࡥࡵࡴ࡬ࡩࡸࡀࠠࠨ⅏"), report.nodeid, os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⅐")))
                    bstack11l1ll1l1_opy_.bstack111l1l111ll_opy_(report.nodeid)
            else:
                print(bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠪ⅑"), report.nodeid, os.environ.get(bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⅒")))
                bstack11l1ll1l1_opy_.bstack111l1l111ll_opy_(report.nodeid)
        else:
            print(bstack1l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡴࡦࡹࡳࡦࡦ࠽ࠤࠬ⅓"), report.nodeid, os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⅔")))
    if cli.is_running():
        if when == bstack1l1ll1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⅕"):
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.BEFORE_EACH, bstack1ll1lllll1l_opy_.POST, item, call, outcome)
        elif when == bstack1l1ll1_opy_ (u"ࠣࡥࡤࡰࡱࠨ⅖"):
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.LOG_REPORT, bstack1ll1lllll1l_opy_.POST, item, call, outcome)
        elif when == bstack1l1ll1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ⅗"):
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.AFTER_EACH, bstack1ll1lllll1l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    skipSessionName = item.config.getoption(bstack1l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⅘"))
    plugins = item.config.getoption(bstack1l1ll1_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧ⅙"))
    report = outcome.get_result()
    os.environ[bstack1l1ll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⅚")] = report.nodeid
    bstack1llll11lllll_opy_(item, call, report)
    if bstack1l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦ⅛") not in plugins or bstack1ll11l111l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1ll1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣ⅜"), None)
    page = getattr(item, bstack1l1ll1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢ⅝"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll1lll1l1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll1l11l11_opy_(item, report, summary, skipSessionName)
def bstack1llll1lll1l1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⅞") and report.skipped:
        bstack11111l1l1ll_opy_(report)
    if report.when in [bstack1l1ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⅟"), bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨⅠ")]:
        return
    if not bstack1l1lll11111_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪⅡ")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫⅢ") + json.dumps(
                    report.nodeid) + bstack1l1ll1_opy_ (u"ࠧࡾࡿࠪⅣ"))
        os.environ[bstack1l1ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫⅤ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤⅥ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧⅦ")))
    bstack11l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠦࠧⅧ")
    bstack11111l1l1ll_opy_(report)
    if not passed:
        try:
            bstack11l111l11l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1ll1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧⅨ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111l11l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1ll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣⅩ")))
        bstack11l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠢࠣⅪ")
        if not passed:
            try:
                bstack11l111l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣⅫ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111l11l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭Ⅼ")
                    + json.dumps(bstack1l1ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦⅭ"))
                    + bstack1l1ll1_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢⅮ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪⅯ")
                    + json.dumps(str(bstack11l111l11l_opy_))
                    + bstack1l1ll1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤⅰ")
                )
        except Exception as e:
            summary.append(bstack1l1ll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧⅱ").format(e))
def bstack1llll11lll1l_opy_(test_name, error_message):
    try:
        bstack1llll1l111ll_opy_ = []
        bstack1l11llll1_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨⅲ"), bstack1l1ll1_opy_ (u"ࠩ࠳ࠫⅳ"))
        bstack111l1l1ll_opy_ = {bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨⅴ"): test_name, bstack1l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪⅵ"): error_message, bstack1l1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫⅶ"): bstack1l11llll1_opy_}
        bstack1llll1lll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1ll1_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫⅷ"))
        if os.path.exists(bstack1llll1lll11l_opy_):
            with open(bstack1llll1lll11l_opy_) as f:
                bstack1llll1l111ll_opy_ = json.load(f)
        bstack1llll1l111ll_opy_.append(bstack111l1l1ll_opy_)
        with open(bstack1llll1lll11l_opy_, bstack1l1ll1_opy_ (u"ࠧࡸࠩⅸ")) as f:
            json.dump(bstack1llll1l111ll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ⅹ") + str(e))
def bstack1llll1l11l11_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣⅺ"), bstack1l1ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧⅻ")]:
        return
    if (str(skipSessionName).lower() != bstack1l1ll1_opy_ (u"ࠫࡹࡸࡵࡦࠩⅼ")):
        bstack11l11l1lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1ll1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢⅽ")))
    bstack11l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠨࠢⅾ")
    bstack11111l1l1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l111l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1ll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢⅿ").format(e)
                )
        try:
            if passed:
                bstack1ll1111l11_opy_(getattr(item, bstack1l1ll1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧↀ"), None), bstack1l1ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤↁ"))
            else:
                error_message = bstack1l1ll1_opy_ (u"ࠪࠫↂ")
                if bstack11l111l11l_opy_:
                    bstack1ll11lllll_opy_(item._page, str(bstack11l111l11l_opy_), bstack1l1ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥↃ"))
                    bstack1ll1111l11_opy_(getattr(item, bstack1l1ll1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫↄ"), None), bstack1l1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨↅ"), str(bstack11l111l11l_opy_))
                    error_message = str(bstack11l111l11l_opy_)
                else:
                    bstack1ll1111l11_opy_(getattr(item, bstack1l1ll1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ↆ"), None), bstack1l1ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣↇ"))
                bstack1llll11lll1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨↈ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1ll1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ↉"), default=bstack1l1ll1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ↊"), help=bstack1l1ll1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ↋"))
    parser.addoption(bstack1l1ll1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ↌"), default=bstack1l1ll1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ↍"), help=bstack1l1ll1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ↎"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1ll1_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ↏"), action=bstack1l1ll1_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ←"), default=bstack1l1ll1_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ↑"),
                         help=bstack1l1ll1_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦ→"))
def bstack111llll1ll_opy_(log):
    if not (log[bstack1l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ↓")] and log[bstack1l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ↔")].strip()):
        return
    active = bstack111ll1llll_opy_()
    log = {
        bstack1l1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ↕"): log[bstack1l1ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ↖")],
        bstack1l1ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭↗"): bstack1111lll11l_opy_().isoformat() + bstack1l1ll1_opy_ (u"ࠫ࡟࠭↘"),
        bstack1l1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭↙"): log[bstack1l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ↚")],
    }
    if active:
        if active[bstack1l1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ↛")] == bstack1l1ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭↜"):
            log[bstack1l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ↝")] = active[bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ↞")]
        elif active[bstack1l1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ↟")] == bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࠪ↠"):
            log[bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭↡")] = active[bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ↢")]
    bstack1l1lll1l_opy_.bstack11llll1l1_opy_([log])
def bstack111ll1llll_opy_():
    if len(store[bstack1l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ↣")]) > 0 and store[bstack1l1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭↤")][-1]:
        return {
            bstack1l1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨ↥"): bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ↦"),
            bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ↧"): store[bstack1l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ↨")][-1]
        }
    if store.get(bstack1l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ↩"), None):
        return {
            bstack1l1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭↪"): bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࠧ↫"),
            bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ↬"): store[bstack1l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ↭")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.INIT_TEST, bstack1ll1lllll1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.INIT_TEST, bstack1ll1lllll1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llll1l1l1l1_opy_ = True
        bstack1l1111l11l_opy_ = bstack1l11ll1lll_opy_.bstack11l11l11_opy_(bstack11l1l11l111_opy_(item.own_markers))
        if not cli.bstack1llll11ll11_opy_(bstack1llll1ll1ll_opy_):
            item._a11y_test_case = bstack1l1111l11l_opy_
            if bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ↮"), None):
                driver = getattr(item, bstack1l1ll1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ↯"), None)
                item._a11y_started = bstack1l11ll1lll_opy_.bstack1llll1l11_opy_(driver, bstack1l1111l11l_opy_)
        if not bstack1l1lll1l_opy_.on() or bstack1llll1l1l11l_opy_ != bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ↰"):
            return
        global current_test_uuid #, bstack111llllll1_opy_
        bstack111l111111_opy_ = {
            bstack1l1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↱"): uuid4().__str__(),
            bstack1l1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭↲"): bstack1111lll11l_opy_().isoformat() + bstack1l1ll1_opy_ (u"ࠪ࡞ࠬ↳")
        }
        current_test_uuid = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ↴")]
        store[bstack1l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ↵")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↶")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l111l1l_opy_[item.nodeid] = {**_111l111l1l_opy_[item.nodeid], **bstack111l111111_opy_}
        bstack1llll1l1ll1l_opy_(item, _111l111l1l_opy_[item.nodeid], bstack1l1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ↷"))
    except Exception as err:
        print(bstack1l1ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ↸"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭↹")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.BEFORE_EACH, bstack1ll1lllll1l_opy_.PRE, item, bstack1l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ↺"))
    if bstack11l1ll1l1_opy_.bstack111l1l11l11_opy_():
            bstack1llll1ll11l1_opy_ = bstack1l1ll1_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡦࡹࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ↻")
            logger.error(bstack1llll1ll11l1_opy_)
            bstack111l111111_opy_ = {
                bstack1l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ↼"): uuid4().__str__(),
                bstack1l1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ↽"): bstack1111lll11l_opy_().isoformat() + bstack1l1ll1_opy_ (u"࡛ࠧࠩ↾"),
                bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭↿"): bstack1111lll11l_opy_().isoformat() + bstack1l1ll1_opy_ (u"ࠩ࡝ࠫ⇀"),
                bstack1l1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⇁"): bstack1l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⇂"),
                bstack1l1ll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⇃"): bstack1llll1ll11l1_opy_,
                bstack1l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⇄"): [],
                bstack1l1ll1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⇅"): []
            }
            bstack1llll1l1ll1l_opy_(item, bstack111l111111_opy_, bstack1l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⇆"))
            pytest.skip(bstack1llll1ll11l1_opy_)
            return # skip all existing bstack1llll1l11l1l_opy_
    global bstack1llll1ll1l1l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l111lllll_opy_():
        atexit.register(bstack11ll1l1ll_opy_)
        if not bstack1llll1ll1l1l_opy_:
            try:
                bstack1llll1l1l1ll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111lll1llll_opy_():
                    bstack1llll1l1l1ll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1l1l1ll_opy_:
                    signal.signal(s, bstack1llll1ll1ll1_opy_)
                bstack1llll1ll1l1l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ⇇") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l1ll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⇈")
    try:
        if not bstack1l1lll1l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l111111_opy_ = {
            bstack1l1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇉"): uuid,
            bstack1l1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⇊"): bstack1111lll11l_opy_().isoformat() + bstack1l1ll1_opy_ (u"࡚࠭ࠨ⇋"),
            bstack1l1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⇌"): bstack1l1ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭⇍"),
            bstack1l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⇎"): bstack1l1ll1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⇏"),
            bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⇐"): bstack1l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⇑")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⇒")] = item
        store[bstack1l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇓")] = [uuid]
        if not _111l111l1l_opy_.get(item.nodeid, None):
            _111l111l1l_opy_[item.nodeid] = {bstack1l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⇔"): [], bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⇕"): []}
        _111l111l1l_opy_[item.nodeid][bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⇖")].append(bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇗")])
        _111l111l1l_opy_[item.nodeid + bstack1l1ll1_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ⇘")] = bstack111l111111_opy_
        bstack1llll1ll111l_opy_(item, bstack111l111111_opy_, bstack1l1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⇙"))
    except Exception as err:
        print(bstack1l1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ⇚"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.AFTER_EACH, bstack1ll1lllll1l_opy_.PRE, item, bstack1l1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⇛"))
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        global bstack1ll111l11_opy_
        bstack1l11llll1_opy_ = 0
        if bstack11111ll1l_opy_ is True:
            bstack1l11llll1_opy_ = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⇜")))
        if bstack11llll1111_opy_.bstack1ll1111lll_opy_() == bstack1l1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ⇝"):
            if bstack11llll1111_opy_.bstack11llll1l11_opy_() == bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ⇞"):
                bstack1llll1l1lll1_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⇟"), None)
                bstack1l1llllll_opy_ = bstack1llll1l1lll1_opy_ + bstack1l1ll1_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤ⇠")
                driver = getattr(item, bstack1l1ll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⇡"), None)
                bstack1l111l111_opy_ = getattr(item, bstack1l1ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭⇢"), None)
                bstack1lll11l1ll_opy_ = getattr(item, bstack1l1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⇣"), None)
                PercySDK.screenshot(driver, bstack1l1llllll_opy_, bstack1l111l111_opy_=bstack1l111l111_opy_, bstack1lll11l1ll_opy_=bstack1lll11l1ll_opy_, bstack1l1l1l1l11_opy_=bstack1l11llll1_opy_)
        if not cli.bstack1llll11ll11_opy_(bstack1llll1ll1ll_opy_):
            if getattr(item, bstack1l1ll1_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ⇤"), False):
                bstack1llll111_opy_.bstack1llll1lll_opy_(getattr(item, bstack1l1ll1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⇥"), None), bstack1ll111l11_opy_, logger, item)
        if not bstack1l1lll1l_opy_.on():
            return
        bstack111l111111_opy_ = {
            bstack1l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⇦"): uuid4().__str__(),
            bstack1l1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⇧"): bstack1111lll11l_opy_().isoformat() + bstack1l1ll1_opy_ (u"࡛ࠧࠩ⇨"),
            bstack1l1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭⇩"): bstack1l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⇪"),
            bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⇫"): bstack1l1ll1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ⇬"),
            bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⇭"): bstack1l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⇮")
        }
        _111l111l1l_opy_[item.nodeid + bstack1l1ll1_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⇯")] = bstack111l111111_opy_
        bstack1llll1ll111l_opy_(item, bstack111l111111_opy_, bstack1l1ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⇰"))
    except Exception as err:
        print(bstack1l1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨ⇱"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111ll1111_opy_(fixturedef.argname):
        store[bstack1l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⇲")] = request.node
    elif bstack11111l1l11l_opy_(fixturedef.argname):
        store[bstack1l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⇳")] = request.node
    if not bstack1l1lll1l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.SETUP_FIXTURE, bstack1ll1lllll1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.SETUP_FIXTURE, bstack1ll1lllll1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.SETUP_FIXTURE, bstack1ll1lllll1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.SETUP_FIXTURE, bstack1ll1lllll1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        fixture = {
            bstack1l1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⇴"): fixturedef.argname,
            bstack1l1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⇵"): bstack11l1l11111l_opy_(outcome),
            bstack1l1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⇶"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⇷")]
        if not _111l111l1l_opy_.get(current_test_item.nodeid, None):
            _111l111l1l_opy_[current_test_item.nodeid] = {bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⇸"): []}
        _111l111l1l_opy_[current_test_item.nodeid][bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⇹")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ⇺"), str(err))
if bstack1ll11l111l_opy_() and bstack1l1lll1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.STEP, bstack1ll1lllll1l_opy_.PRE, request, step)
            return
        try:
            _111l111l1l_opy_[request.node.nodeid][bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⇻")].bstack111ll11ll_opy_(id(step))
        except Exception as err:
            print(bstack1l1ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ⇼"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.STEP, bstack1ll1lllll1l_opy_.POST, request, step, exception)
            return
        try:
            _111l111l1l_opy_[request.node.nodeid][bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⇽")].bstack111ll1l11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⇾"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.STEP, bstack1ll1lllll1l_opy_.POST, request, step)
            return
        try:
            bstack111llll1l1_opy_: bstack111lll11l1_opy_ = _111l111l1l_opy_[request.node.nodeid][bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⇿")]
            bstack111llll1l1_opy_.bstack111ll1l11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ∀"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1l1l11l_opy_
        try:
            if not bstack1l1lll1l_opy_.on() or bstack1llll1l1l11l_opy_ != bstack1l1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ∁"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ∂"), None)
            if not _111l111l1l_opy_.get(request.node.nodeid, None):
                _111l111l1l_opy_[request.node.nodeid] = {}
            bstack111llll1l1_opy_ = bstack111lll11l1_opy_.bstack1lllllllll1l_opy_(
                scenario, feature, request.node,
                name=bstack11111l11ll1_opy_(request.node, scenario),
                started_at=bstack1llllll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1ll1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ∃"),
                tags=bstack11111l1ll1l_opy_(feature, scenario),
                bstack111ll1l1ll_opy_=bstack1l1lll1l_opy_.bstack111ll11ll1_opy_(driver) if driver and driver.session_id else {}
            )
            _111l111l1l_opy_[request.node.nodeid][bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ∄")] = bstack111llll1l1_opy_
            bstack1llll1ll11ll_opy_(bstack111llll1l1_opy_.uuid)
            bstack1l1lll1l_opy_.bstack111llll111_opy_(bstack1l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ∅"), bstack111llll1l1_opy_)
        except Exception as err:
            print(bstack1l1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ∆"), str(err))
def bstack1llll1lll111_opy_(bstack111lllll11_opy_):
    if bstack111lllll11_opy_ in store[bstack1l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ∇")]:
        store[bstack1l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ∈")].remove(bstack111lllll11_opy_)
def bstack1llll1ll11ll_opy_(test_uuid):
    store[bstack1l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ∉")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1lll1l_opy_.bstack1lllll1lllll_opy_
def bstack1llll11lllll_opy_(item, call, report):
    logger.debug(bstack1l1ll1_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ∊"))
    global bstack1llll1l1l11l_opy_
    bstack1ll1llll11_opy_ = bstack1llllll1l_opy_()
    if hasattr(report, bstack1l1ll1_opy_ (u"ࠧࡴࡶࡲࡴࠬ∋")):
        bstack1ll1llll11_opy_ = bstack11l111ll11l_opy_(report.stop)
    elif hasattr(report, bstack1l1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ∌")):
        bstack1ll1llll11_opy_ = bstack11l111ll11l_opy_(report.start)
    try:
        if getattr(report, bstack1l1ll1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ∍"), bstack1l1ll1_opy_ (u"ࠪࠫ∎")) == bstack1l1ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ∏"):
            logger.debug(bstack1l1ll1_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ∐").format(getattr(report, bstack1l1ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫ∑"), bstack1l1ll1_opy_ (u"ࠧࠨ−")).__str__(), bstack1llll1l1l11l_opy_))
            if bstack1llll1l1l11l_opy_ == bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ∓"):
                _111l111l1l_opy_[item.nodeid][bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∔")] = bstack1ll1llll11_opy_
                bstack1llll1l1ll1l_opy_(item, _111l111l1l_opy_[item.nodeid], bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ∕"), report, call)
                store[bstack1l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ∖")] = None
            elif bstack1llll1l1l11l_opy_ == bstack1l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ∗"):
                bstack111llll1l1_opy_ = _111l111l1l_opy_[item.nodeid][bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ∘")]
                bstack111llll1l1_opy_.set(hooks=_111l111l1l_opy_[item.nodeid].get(bstack1l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭∙"), []))
                exception, bstack111lll1ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll1ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1ll1_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧ√"), bstack1l1ll1_opy_ (u"ࠩࠪ∛"))]
                bstack111llll1l1_opy_.stop(time=bstack1ll1llll11_opy_, result=Result(result=getattr(report, bstack1l1ll1_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ∜"), bstack1l1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ∝")), exception=exception, bstack111lll1ll1_opy_=bstack111lll1ll1_opy_))
                bstack1l1lll1l_opy_.bstack111llll111_opy_(bstack1l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ∞"), _111l111l1l_opy_[item.nodeid][bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ∟")])
        elif getattr(report, bstack1l1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬ∠"), bstack1l1ll1_opy_ (u"ࠨࠩ∡")) in [bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ∢"), bstack1l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ∣")]:
            logger.debug(bstack1l1ll1_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭∤").format(getattr(report, bstack1l1ll1_opy_ (u"ࠬࡽࡨࡦࡰࠪ∥"), bstack1l1ll1_opy_ (u"࠭ࠧ∦")).__str__(), bstack1llll1l1l11l_opy_))
            bstack111lll111l_opy_ = item.nodeid + bstack1l1ll1_opy_ (u"ࠧ࠮ࠩ∧") + getattr(report, bstack1l1ll1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭∨"), bstack1l1ll1_opy_ (u"ࠩࠪ∩"))
            if getattr(report, bstack1l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ∪"), False):
                hook_type = bstack1l1ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ∫") if getattr(report, bstack1l1ll1_opy_ (u"ࠬࡽࡨࡦࡰࠪ∬"), bstack1l1ll1_opy_ (u"࠭ࠧ∭")) == bstack1l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭∮") else bstack1l1ll1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ∯")
                _111l111l1l_opy_[bstack111lll111l_opy_] = {
                    bstack1l1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ∰"): uuid4().__str__(),
                    bstack1l1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ∱"): bstack1ll1llll11_opy_,
                    bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ∲"): hook_type
                }
            _111l111l1l_opy_[bstack111lll111l_opy_][bstack1l1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ∳")] = bstack1ll1llll11_opy_
            bstack1llll1lll111_opy_(_111l111l1l_opy_[bstack111lll111l_opy_][bstack1l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ∴")])
            bstack1llll1ll111l_opy_(item, _111l111l1l_opy_[bstack111lll111l_opy_], bstack1l1ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ∵"), report, call)
            if getattr(report, bstack1l1ll1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭∶"), bstack1l1ll1_opy_ (u"ࠩࠪ∷")) == bstack1l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ∸"):
                if getattr(report, bstack1l1ll1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ∹"), bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ∺")) == bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭∻"):
                    bstack111l111111_opy_ = {
                        bstack1l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ∼"): uuid4().__str__(),
                        bstack1l1ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ∽"): bstack1llllll1l_opy_(),
                        bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∾"): bstack1llllll1l_opy_()
                    }
                    _111l111l1l_opy_[item.nodeid] = {**_111l111l1l_opy_[item.nodeid], **bstack111l111111_opy_}
                    bstack1llll1l1ll1l_opy_(item, _111l111l1l_opy_[item.nodeid], bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ∿"))
                    bstack1llll1l1ll1l_opy_(item, _111l111l1l_opy_[item.nodeid], bstack1l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭≀"), report, call)
    except Exception as err:
        print(bstack1l1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ≁"), str(err))
def bstack1llll1l11ll1_opy_(test, bstack111l111111_opy_, result=None, call=None, bstack1111l1ll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111llll1l1_opy_ = {
        bstack1l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ≂"): bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ≃")],
        bstack1l1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭≄"): bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࠧ≅"),
        bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ≆"): test.name,
        bstack1l1ll1_opy_ (u"ࠫࡧࡵࡤࡺࠩ≇"): {
            bstack1l1ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ≈"): bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭≉"),
            bstack1l1ll1_opy_ (u"ࠧࡤࡱࡧࡩࠬ≊"): inspect.getsource(test.obj)
        },
        bstack1l1ll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ≋"): test.name,
        bstack1l1ll1_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ≌"): test.name,
        bstack1l1ll1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ≍"): bstack111l1ll1l_opy_.bstack111l1l1111_opy_(test),
        bstack1l1ll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ≎"): file_path,
        bstack1l1ll1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ≏"): file_path,
        bstack1l1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭≐"): bstack1l1ll1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ≑"),
        bstack1l1ll1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭≒"): file_path,
        bstack1l1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭≓"): bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ≔")],
        bstack1l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ≕"): bstack1l1ll1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ≖"),
        bstack1l1ll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ≗"): {
            bstack1l1ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ≘"): test.nodeid
        },
        bstack1l1ll1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭≙"): bstack11l1l11l111_opy_(test.own_markers)
    }
    if bstack1111l1ll1_opy_ in [bstack1l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ≚"), bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ≛")]:
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ≜")] = {
            bstack1l1ll1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ≝"): bstack111l111111_opy_.get(bstack1l1ll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ≞"), [])
        }
    if bstack1111l1ll1_opy_ == bstack1l1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ≟"):
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≠")] = bstack1l1ll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ≡")
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ≢")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ≣")]
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≤")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≥")]
    if result:
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ≦")] = result.outcome
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ≧")] = result.duration * 1000
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ≨")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≩")]
        if result.failed:
            bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ≪")] = bstack1l1lll1l_opy_.bstack11111l11l1_opy_(call.excinfo.typename)
            bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭≫")] = bstack1l1lll1l_opy_.bstack1llllll111l1_opy_(call.excinfo, result)
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≬")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭≭")]
    if outcome:
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≮")] = bstack11l1l11111l_opy_(outcome)
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ≯")] = 0
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≰")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≱")]
        if bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ≲")] == bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭≳"):
            bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭≴")] = bstack1l1ll1_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ≵")  # bstack1llll1l1ll11_opy_
            bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ≶")] = [{bstack1l1ll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭≷"): [bstack1l1ll1_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ≸")]}]
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ≹")] = bstack111l111111_opy_[bstack1l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≺")]
    return bstack111llll1l1_opy_
def bstack1llll1ll1lll_opy_(test, bstack111l1l111l_opy_, bstack1111l1ll1_opy_, result, call, outcome, bstack1llll1ll1l11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ≻")]
    hook_name = bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ≼")]
    hook_data = {
        bstack1l1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ≽"): bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ≾")],
        bstack1l1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ≿"): bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⊀"),
        bstack1l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⊁"): bstack1l1ll1_opy_ (u"ࠧࡼࡿࠪ⊂").format(bstack11111l111ll_opy_(hook_name)),
        bstack1l1ll1_opy_ (u"ࠨࡤࡲࡨࡾ࠭⊃"): {
            bstack1l1ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⊄"): bstack1l1ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⊅"),
            bstack1l1ll1_opy_ (u"ࠫࡨࡵࡤࡦࠩ⊆"): None
        },
        bstack1l1ll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⊇"): test.name,
        bstack1l1ll1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⊈"): bstack111l1ll1l_opy_.bstack111l1l1111_opy_(test, hook_name),
        bstack1l1ll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⊉"): file_path,
        bstack1l1ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⊊"): file_path,
        bstack1l1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊋"): bstack1l1ll1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⊌"),
        bstack1l1ll1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⊍"): file_path,
        bstack1l1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊎"): bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊏")],
        bstack1l1ll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⊐"): bstack1l1ll1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⊑") if bstack1llll1l1l11l_opy_ == bstack1l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⊒") else bstack1l1ll1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⊓"),
        bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⊔"): hook_type
    }
    bstack1ll1l1l1111_opy_ = bstack111l11ll1l_opy_(_111l111l1l_opy_.get(test.nodeid, None))
    if bstack1ll1l1l1111_opy_:
        hook_data[bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⊕")] = bstack1ll1l1l1111_opy_
    if result:
        hook_data[bstack1l1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⊖")] = result.outcome
        hook_data[bstack1l1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⊗")] = result.duration * 1000
        hook_data[bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊘")] = bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⊙")]
        if result.failed:
            hook_data[bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⊚")] = bstack1l1lll1l_opy_.bstack11111l11l1_opy_(call.excinfo.typename)
            hook_data[bstack1l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⊛")] = bstack1l1lll1l_opy_.bstack1llllll111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⊜")] = bstack11l1l11111l_opy_(outcome)
        hook_data[bstack1l1ll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⊝")] = 100
        hook_data[bstack1l1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊞")] = bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊟")]
        if hook_data[bstack1l1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊠")] == bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⊡"):
            hook_data[bstack1l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⊢")] = bstack1l1ll1_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭⊣")  # bstack1llll1l1ll11_opy_
            hook_data[bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⊤")] = [{bstack1l1ll1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⊥"): [bstack1l1ll1_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⊦")]}]
    if bstack1llll1ll1l11_opy_:
        hook_data[bstack1l1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊧")] = bstack1llll1ll1l11_opy_.result
        hook_data[bstack1l1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⊨")] = bstack11l11ll1l11_opy_(bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⊩")], bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⊪")])
        hook_data[bstack1l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⊫")] = bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊬")]
        if hook_data[bstack1l1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⊭")] == bstack1l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⊮"):
            hook_data[bstack1l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⊯")] = bstack1l1lll1l_opy_.bstack11111l11l1_opy_(bstack1llll1ll1l11_opy_.exception_type)
            hook_data[bstack1l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⊰")] = [{bstack1l1ll1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⊱"): bstack11l11ll1lll_opy_(bstack1llll1ll1l11_opy_.exception)}]
    return hook_data
def bstack1llll1l1ll1l_opy_(test, bstack111l111111_opy_, bstack1111l1ll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1ll1_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ⊲").format(bstack1111l1ll1_opy_))
    bstack111llll1l1_opy_ = bstack1llll1l11ll1_opy_(test, bstack111l111111_opy_, result, call, bstack1111l1ll1_opy_, outcome)
    driver = getattr(test, bstack1l1ll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⊳"), None)
    if bstack1111l1ll1_opy_ == bstack1l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⊴") and driver:
        bstack111llll1l1_opy_[bstack1l1ll1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⊵")] = bstack1l1lll1l_opy_.bstack111ll11ll1_opy_(driver)
    if bstack1111l1ll1_opy_ == bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⊶"):
        bstack1111l1ll1_opy_ = bstack1l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⊷")
    bstack1111ll1lll_opy_ = {
        bstack1l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⊸"): bstack1111l1ll1_opy_,
        bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⊹"): bstack111llll1l1_opy_
    }
    bstack1l1lll1l_opy_.bstack11l1111l_opy_(bstack1111ll1lll_opy_)
    if bstack1111l1ll1_opy_ == bstack1l1ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⊺"):
        threading.current_thread().bstackTestMeta = {bstack1l1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⊻"): bstack1l1ll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⊼")}
    elif bstack1111l1ll1_opy_ == bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⊽"):
        threading.current_thread().bstackTestMeta = {bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⊾"): getattr(result, bstack1l1ll1_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⊿"), bstack1l1ll1_opy_ (u"࠭ࠧ⋀"))}
def bstack1llll1ll111l_opy_(test, bstack111l111111_opy_, bstack1111l1ll1_opy_, result=None, call=None, outcome=None, bstack1llll1ll1l11_opy_=None):
    logger.debug(bstack1l1ll1_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ⋁").format(bstack1111l1ll1_opy_))
    hook_data = bstack1llll1ll1lll_opy_(test, bstack111l111111_opy_, bstack1111l1ll1_opy_, result, call, outcome, bstack1llll1ll1l11_opy_)
    bstack1111ll1lll_opy_ = {
        bstack1l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⋂"): bstack1111l1ll1_opy_,
        bstack1l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ⋃"): hook_data
    }
    bstack1l1lll1l_opy_.bstack11l1111l_opy_(bstack1111ll1lll_opy_)
def bstack111l11ll1l_opy_(bstack111l111111_opy_):
    if not bstack111l111111_opy_:
        return None
    if bstack111l111111_opy_.get(bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⋄"), None):
        return getattr(bstack111l111111_opy_[bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⋅")], bstack1l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⋆"), None)
    return bstack111l111111_opy_.get(bstack1l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⋇"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.LOG, bstack1ll1lllll1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_.LOG, bstack1ll1lllll1l_opy_.POST, request, caplog)
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        if not bstack1l1lll1l_opy_.on():
            return
        places = [bstack1l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⋈"), bstack1l1ll1_opy_ (u"ࠨࡥࡤࡰࡱ࠭⋉"), bstack1l1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⋊")]
        logs = []
        for bstack1llll1l11lll_opy_ in places:
            records = caplog.get_records(bstack1llll1l11lll_opy_)
            bstack1llll11llll1_opy_ = bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⋋") if bstack1llll1l11lll_opy_ == bstack1l1ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⋌") else bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⋍")
            bstack1llll1l1l111_opy_ = request.node.nodeid + (bstack1l1ll1_opy_ (u"࠭ࠧ⋎") if bstack1llll1l11lll_opy_ == bstack1l1ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⋏") else bstack1l1ll1_opy_ (u"ࠨ࠯ࠪ⋐") + bstack1llll1l11lll_opy_)
            test_uuid = bstack111l11ll1l_opy_(_111l111l1l_opy_.get(bstack1llll1l1l111_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1111l1ll_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⋑"): bstack11l11l1l1l1_opy_(record.created).isoformat() + bstack1l1ll1_opy_ (u"ࠪ࡞ࠬ⋒"),
                    bstack1l1ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⋓"): record.levelname,
                    bstack1l1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⋔"): record.message,
                    bstack1llll11llll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1lll1l_opy_.bstack11llll1l1_opy_(logs)
    except Exception as err:
        print(bstack1l1ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ⋕"), str(err))
def bstack11l11l11l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1ll1l11_opy_
    bstack111l1111l_opy_ = bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ⋖"), None) and bstack11l1ll11ll_opy_(
            threading.current_thread(), bstack1l1ll1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⋗"), None)
    bstack1ll1llll_opy_ = getattr(driver, bstack1l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⋘"), None) != None and getattr(driver, bstack1l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⋙"), None) == True
    if sequence == bstack1l1ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⋚") and driver != None:
      if not bstack1ll1ll1l11_opy_ and bstack1l1lll11111_opy_() and bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⋛") in CONFIG and CONFIG[bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⋜")] == True and bstack1ll1l1l1l_opy_.bstack11l11lll_opy_(driver_command) and (bstack1ll1llll_opy_ or bstack111l1111l_opy_) and not bstack11l111l1ll_opy_(args):
        try:
          bstack1ll1ll1l11_opy_ = True
          logger.debug(bstack1l1ll1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ⋝").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1ll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭⋞").format(str(err)))
        bstack1ll1ll1l11_opy_ = False
    if sequence == bstack1l1ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⋟"):
        if driver_command == bstack1l1ll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ⋠"):
            bstack1l1lll1l_opy_.bstack1l1l1111ll_opy_({
                bstack1l1ll1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⋡"): response[bstack1l1ll1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⋢")],
                bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⋣"): store[bstack1l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⋤")]
            })
def bstack11ll1l1ll_opy_():
    global bstack1ll1l11lll_opy_
    bstack11lll1ll_opy_.bstack1111l1l1_opy_()
    logging.shutdown()
    bstack1l1lll1l_opy_.bstack111ll11l1l_opy_()
    for driver in bstack1ll1l11lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1ll1ll1_opy_(*args):
    global bstack1ll1l11lll_opy_
    bstack1l1lll1l_opy_.bstack111ll11l1l_opy_()
    for driver in bstack1ll1l11lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11lllll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1l11l1l111_opy_(self, *args, **kwargs):
    bstack1lll11lll_opy_ = bstack11llllll11_opy_(self, *args, **kwargs)
    bstack1l11l111l1_opy_ = getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⋥"), None)
    if bstack1l11l111l1_opy_ and bstack1l11l111l1_opy_.get(bstack1l1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⋦"), bstack1l1ll1_opy_ (u"ࠪࠫ⋧")) == bstack1l1ll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⋨"):
        bstack1l1lll1l_opy_.bstack11l11l1l_opy_(self)
    return bstack1lll11lll_opy_
@measure(event_name=EVENTS.bstack1l1l11ll11_opy_, stage=STAGE.bstack111lll111_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack111ll1l1l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
    if bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⋩")):
        return
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⋪"), True)
    global bstack1l11lll1l_opy_
    global bstack11l1l1ll11_opy_
    bstack1l11lll1l_opy_ = framework_name
    logger.info(bstack11l111l1l_opy_.format(bstack1l11lll1l_opy_.split(bstack1l1ll1_opy_ (u"ࠧ࠮ࠩ⋫"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lll11111_opy_():
            Service.start = bstack1l1ll11l_opy_
            Service.stop = bstack1lll1l11_opy_
            webdriver.Remote.get = bstack1lllll1ll_opy_
            webdriver.Remote.__init__ = bstack11llll1ll_opy_
            if not isinstance(os.getenv(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ⋬")), str):
                return
            WebDriver.quit = bstack11lll1ll11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1lll1l_opy_.on():
            webdriver.Remote.__init__ = bstack1l11l1l111_opy_
        bstack11l1l1ll11_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⋭")):
        bstack11l1l1ll11_opy_ = eval(os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⋮")))
    if not bstack11l1l1ll11_opy_:
        bstack1l1l1llll1_opy_(bstack1l1ll1_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ⋯"), bstack1l1l1111l1_opy_)
    if bstack11ll11111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⋰")) and callable(getattr(RemoteConnection, bstack1l1ll1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⋱"))):
                RemoteConnection._get_proxy_url = bstack1l111ll11l_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l111ll11l_opy_
        except Exception as e:
            logger.error(bstack11lll1l11_opy_.format(str(e)))
    if bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⋲") in str(framework_name).lower():
        if not bstack1l1lll11111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11llll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll11l11l1_opy_
            Config.getoption = bstack11l1l1l1l1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l1l1lll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l11l1l11_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11lll1ll11_opy_(self):
    global bstack1l11lll1l_opy_
    global bstack1l11l11ll_opy_
    global bstack111l11l1l_opy_
    try:
        if bstack1l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⋳") in bstack1l11lll1l_opy_ and self.session_id != None and bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭⋴"), bstack1l1ll1_opy_ (u"ࠪࠫ⋵")) != bstack1l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⋶"):
            bstack11l11ll111_opy_ = bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⋷") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⋸")
            bstack11lll11l1_opy_(logger, True)
            if os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⋹"), None):
                self.execute_script(
                    bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⋺") + json.dumps(
                        os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⋻"))) + bstack1l1ll1_opy_ (u"ࠪࢁࢂ࠭⋼"))
            if self != None:
                bstack1l1ll1lll1_opy_(self, bstack11l11ll111_opy_, bstack1l1ll1_opy_ (u"ࠫ࠱ࠦࠧ⋽").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll11ll11_opy_(bstack1llll1ll1ll_opy_):
            item = store.get(bstack1l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⋾"), None)
            if item is not None and bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⋿"), None):
                bstack1llll111_opy_.bstack1llll1lll_opy_(self, bstack1ll111l11_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1ll1_opy_ (u"ࠧࠨ⌀")
    except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ⌁") + str(e))
    bstack111l11l1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11l11l1111_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack11llll1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11l11ll_opy_
    global bstack11111ll1_opy_
    global bstack11111ll1l_opy_
    global bstack1l11lll1l_opy_
    global bstack11llllll11_opy_
    global bstack1ll1l11lll_opy_
    global bstack1l1ll1l11l_opy_
    global bstack1111ll11l_opy_
    global bstack1ll111l11_opy_
    CONFIG[bstack1l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⌂")] = str(bstack1l11lll1l_opy_) + str(__version__)
    command_executor = bstack1llll1llll_opy_(bstack1l1ll1l11l_opy_, CONFIG)
    logger.debug(bstack1l1111111_opy_.format(command_executor))
    proxy = bstack1lll1l11l_opy_(CONFIG, proxy)
    bstack1l11llll1_opy_ = 0
    try:
        if bstack11111ll1l_opy_ is True:
            bstack1l11llll1_opy_ = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⌃")))
    except:
        bstack1l11llll1_opy_ = 0
    bstack1l1lll1ll1_opy_ = bstack11lll1l1ll_opy_(CONFIG, bstack1l11llll1_opy_)
    logger.debug(bstack111ll1111_opy_.format(str(bstack1l1lll1ll1_opy_)))
    bstack1ll111l11_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⌄"))[bstack1l11llll1_opy_]
    if bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⌅") in CONFIG and CONFIG[bstack1l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⌆")]:
        bstack11lll11l1l_opy_(bstack1l1lll1ll1_opy_, bstack1111ll11l_opy_)
    if bstack1l11ll1lll_opy_.bstack11ll1111l1_opy_(CONFIG, bstack1l11llll1_opy_) and bstack1l11ll1lll_opy_.bstack111111l1l_opy_(bstack1l1lll1ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll11ll11_opy_(bstack1llll1ll1ll_opy_):
            bstack1l11ll1lll_opy_.set_capabilities(bstack1l1lll1ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll1llll1_opy_ = bstack1l1l1l1l1l_opy_(desired_capabilities)
        bstack1lll1llll1_opy_[bstack1l1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⌇")] = bstack1l1l111l11_opy_(CONFIG)
        bstack11l1l11l1l_opy_ = bstack11lll1l1ll_opy_(bstack1lll1llll1_opy_)
        if bstack11l1l11l1l_opy_:
            bstack1l1lll1ll1_opy_ = update(bstack11l1l11l1l_opy_, bstack1l1lll1ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1lllll11ll_opy_(options, bstack1l1lll1ll1_opy_)
    if not options:
        options = bstack1ll1l1111l_opy_(bstack1l1lll1ll1_opy_)
    if proxy and bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⌈")):
        options.proxy(proxy)
    if options and bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⌉")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1111l1l1l_opy_() < version.parse(bstack1l1ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⌊")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1lll1ll1_opy_)
    logger.info(bstack1l1llll1ll_opy_)
    bstack1l11l1llll_opy_.end(EVENTS.bstack1l1l11ll11_opy_.value, EVENTS.bstack1l1l11ll11_opy_.value + bstack1l1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⌋"),
                               EVENTS.bstack1l1l11ll11_opy_.value + bstack1l1ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⌌"), True, None)
    if bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⌍")):
        bstack11llllll11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⌎")):
        bstack11llllll11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ⌏")):
        bstack11llllll11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11llllll11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11lll1l1l1_opy_ = bstack1l1ll1_opy_ (u"ࠩࠪ⌐")
        if bstack1111l1l1l_opy_() >= version.parse(bstack1l1ll1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ⌑")):
            bstack11lll1l1l1_opy_ = self.caps.get(bstack1l1ll1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⌒"))
        else:
            bstack11lll1l1l1_opy_ = self.capabilities.get(bstack1l1ll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⌓"))
        if bstack11lll1l1l1_opy_:
            bstack1l11l1ll1_opy_(bstack11lll1l1l1_opy_)
            if bstack1111l1l1l_opy_() <= version.parse(bstack1l1ll1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭⌔")):
                self.command_executor._url = bstack1l1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⌕") + bstack1l1ll1l11l_opy_ + bstack1l1ll1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ⌖")
            else:
                self.command_executor._url = bstack1l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ⌗") + bstack11lll1l1l1_opy_ + bstack1l1ll1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ⌘")
            logger.debug(bstack1l1l111111_opy_.format(bstack11lll1l1l1_opy_))
        else:
            logger.debug(bstack1llll1ll_opy_.format(bstack1l1ll1_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ⌙")))
    except Exception as e:
        logger.debug(bstack1llll1ll_opy_.format(e))
    bstack1l11l11ll_opy_ = self.session_id
    if bstack1l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⌚") in bstack1l11lll1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⌛"), None)
        if item:
            bstack1llll1l111l1_opy_ = getattr(item, bstack1l1ll1_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ⌜"), False)
            if not getattr(item, bstack1l1ll1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⌝"), None) and bstack1llll1l111l1_opy_:
                setattr(store[bstack1l1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⌞")], bstack1l1ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⌟"), self)
        bstack1l11l111l1_opy_ = getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ⌠"), None)
        if bstack1l11l111l1_opy_ and bstack1l11l111l1_opy_.get(bstack1l1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⌡"), bstack1l1ll1_opy_ (u"࠭ࠧ⌢")) == bstack1l1ll1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⌣"):
            bstack1l1lll1l_opy_.bstack11l11l1l_opy_(self)
    bstack1ll1l11lll_opy_.append(self)
    if bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⌤") in CONFIG and bstack1l1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⌥") in CONFIG[bstack1l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⌦")][bstack1l11llll1_opy_]:
        bstack11111ll1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⌧")][bstack1l11llll1_opy_][bstack1l1ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌨")]
    logger.debug(bstack1l1l11ll_opy_.format(bstack1l11l11ll_opy_))
@measure(event_name=EVENTS.bstack1ll11111l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack1llll1ll1l_opy_=bstack11111ll1_opy_)
def bstack1lllll1ll_opy_(self, url):
    global bstack1lll1ll11_opy_
    global CONFIG
    try:
        bstack11ll1lllll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1ll1l_opy_.format(str(err)))
    try:
        bstack1lll1ll11_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll11l1ll_opy_ = str(e)
            if any(err_msg in bstack1ll11l1ll_opy_ for err_msg in bstack1l1lllll1l_opy_):
                bstack11ll1lllll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1ll1l_opy_.format(str(err)))
        raise e
def bstack1111llll1_opy_(item, when):
    global bstack1l11l1lll_opy_
    try:
        bstack1l11l1lll_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1l1lll_opy_(item, call, rep):
    global bstack1l1lll1l11_opy_
    global bstack1ll1l11lll_opy_
    name = bstack1l1ll1_opy_ (u"࠭ࠧ〈")
    try:
        if rep.when == bstack1l1ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ〉"):
            bstack1l11l11ll_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1ll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌫"))
            try:
                if (str(skipSessionName).lower() != bstack1l1ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⌬")):
                    name = str(rep.nodeid)
                    bstack1lllllll11_opy_ = bstack111111ll1_opy_(bstack1l1ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⌭"), name, bstack1l1ll1_opy_ (u"ࠫࠬ⌮"), bstack1l1ll1_opy_ (u"ࠬ࠭⌯"), bstack1l1ll1_opy_ (u"࠭ࠧ⌰"), bstack1l1ll1_opy_ (u"ࠧࠨ⌱"))
                    os.environ[bstack1l1ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⌲")] = name
                    for driver in bstack1ll1l11lll_opy_:
                        if bstack1l11l11ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1lllllll11_opy_)
            except Exception as e:
                logger.debug(bstack1l1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⌳").format(str(e)))
            try:
                bstack1l111l1lll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⌴"):
                    status = bstack1l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⌵") if rep.outcome.lower() == bstack1l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⌶") else bstack1l1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌷")
                    reason = bstack1l1ll1_opy_ (u"ࠧࠨ⌸")
                    if status == bstack1l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⌹"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ⌺") if status == bstack1l1ll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⌻") else bstack1l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⌼")
                    data = name + bstack1l1ll1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ⌽") if status == bstack1l1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌾") else name + bstack1l1ll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ⌿") + reason
                    bstack1ll1lllll_opy_ = bstack111111ll1_opy_(bstack1l1ll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⍀"), bstack1l1ll1_opy_ (u"ࠩࠪ⍁"), bstack1l1ll1_opy_ (u"ࠪࠫ⍂"), bstack1l1ll1_opy_ (u"ࠫࠬ⍃"), level, data)
                    for driver in bstack1ll1l11lll_opy_:
                        if bstack1l11l11ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1lllll_opy_)
            except Exception as e:
                logger.debug(bstack1l1ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⍄").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ⍅").format(str(e)))
    bstack1l1lll1l11_opy_(item, call, rep)
notset = Notset()
def bstack11l1l1l1l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll1lll1l_opy_
    if str(name).lower() == bstack1l1ll1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ⍆"):
        return bstack1l1ll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ⍇")
    else:
        return bstack1lll1lll1l_opy_(self, name, default, skip)
def bstack1l111ll11l_opy_(self):
    global CONFIG
    global bstack1lll1llll_opy_
    try:
        proxy = bstack11l1lll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1ll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⍈")):
                proxies = bstack11l1l11ll1_opy_(proxy, bstack1llll1llll_opy_())
                if len(proxies) > 0:
                    protocol, bstack111l11l11_opy_ = proxies.popitem()
                    if bstack1l1ll1_opy_ (u"ࠥ࠾࠴࠵ࠢ⍉") in bstack111l11l11_opy_:
                        return bstack111l11l11_opy_
                    else:
                        return bstack1l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⍊") + bstack111l11l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ⍋").format(str(e)))
    return bstack1lll1llll_opy_(self)
def bstack11ll11111l_opy_():
    return (bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⍌") in CONFIG or bstack1l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⍍") in CONFIG) and bstack11l1l1l1l_opy_() and bstack1111l1l1l_opy_() >= version.parse(
        bstack1ll1ll1111_opy_)
def bstack1l11ll11l1_opy_(self,
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
    global bstack11111ll1_opy_
    global bstack11111ll1l_opy_
    global bstack1l11lll1l_opy_
    CONFIG[bstack1l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⍎")] = str(bstack1l11lll1l_opy_) + str(__version__)
    bstack1l11llll1_opy_ = 0
    try:
        if bstack11111ll1l_opy_ is True:
            bstack1l11llll1_opy_ = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⍏")))
    except:
        bstack1l11llll1_opy_ = 0
    CONFIG[bstack1l1ll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ⍐")] = True
    bstack1l1lll1ll1_opy_ = bstack11lll1l1ll_opy_(CONFIG, bstack1l11llll1_opy_)
    logger.debug(bstack111ll1111_opy_.format(str(bstack1l1lll1ll1_opy_)))
    if CONFIG.get(bstack1l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⍑")):
        bstack11lll11l1l_opy_(bstack1l1lll1ll1_opy_, bstack1111ll11l_opy_)
    if bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⍒") in CONFIG and bstack1l1ll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⍓") in CONFIG[bstack1l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⍔")][bstack1l11llll1_opy_]:
        bstack11111ll1_opy_ = CONFIG[bstack1l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⍕")][bstack1l11llll1_opy_][bstack1l1ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⍖")]
    import urllib
    import json
    if bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⍗") in CONFIG and str(CONFIG[bstack1l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⍘")]).lower() != bstack1l1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⍙"):
        bstack1lll1lllll_opy_ = bstack1l1l1ll1l_opy_()
        bstack1111l1l11_opy_ = bstack1lll1lllll_opy_ + urllib.parse.quote(json.dumps(bstack1l1lll1ll1_opy_))
    else:
        bstack1111l1l11_opy_ = bstack1l1ll1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ⍚") + urllib.parse.quote(json.dumps(bstack1l1lll1ll1_opy_))
    browser = self.connect(bstack1111l1l11_opy_)
    return browser
def bstack1l1l1lllll_opy_():
    global bstack11l1l1ll11_opy_
    global bstack1l11lll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1ll1111l_opy_
        if not bstack1l1lll11111_opy_():
            global bstack1l11111111_opy_
            if not bstack1l11111111_opy_:
                from bstack_utils.helper import bstack1l111l11l_opy_, bstack1l11ll111l_opy_
                bstack1l11111111_opy_ = bstack1l111l11l_opy_()
                bstack1l11ll111l_opy_(bstack1l11lll1l_opy_)
            BrowserType.connect = bstack1l1ll1111l_opy_
            return
        BrowserType.launch = bstack1l11ll11l1_opy_
        bstack11l1l1ll11_opy_ = True
    except Exception as e:
        pass
def bstack1llll1lll1ll_opy_():
    global CONFIG
    global bstack1l1lllllll_opy_
    global bstack1l1ll1l11l_opy_
    global bstack1111ll11l_opy_
    global bstack11111ll1l_opy_
    global bstack111111l11_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭⍛")))
    bstack1l1lllllll_opy_ = eval(os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ⍜")))
    bstack1l1ll1l11l_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ⍝"))
    bstack11ll111l1l_opy_(CONFIG, bstack1l1lllllll_opy_)
    bstack111111l11_opy_ = bstack11lll1ll_opy_.bstack111l1lll1_opy_(CONFIG, bstack111111l11_opy_)
    if cli.bstack1ll1lll1l1_opy_():
        bstack1l1l111l_opy_.invoke(bstack1l11111l1l_opy_.CONNECT, bstack1l1l1lll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⍞"), bstack1l1ll1_opy_ (u"ࠫ࠵࠭⍟")))
        cli.bstack1llll11111l_opy_(cli_context.platform_index)
        cli.bstack1ll1lll1l1l_opy_(bstack1llll1llll_opy_(bstack1l1ll1l11l_opy_, CONFIG), cli_context.platform_index, bstack1ll1l1111l_opy_)
        cli.bstack1ll1lll11l1_opy_()
        logger.debug(bstack1l1ll1_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⍠") + str(cli_context.platform_index) + bstack1l1ll1_opy_ (u"ࠨࠢ⍡"))
        return # skip all existing bstack1llll1l11l1l_opy_
    global bstack11llllll11_opy_
    global bstack111l11l1l_opy_
    global bstack1lll11111_opy_
    global bstack11l111l1l1_opy_
    global bstack11l1111l11_opy_
    global bstack11l1l11ll_opy_
    global bstack11ll11lll1_opy_
    global bstack1lll1ll11_opy_
    global bstack1lll1llll_opy_
    global bstack1lll1lll1l_opy_
    global bstack1l11l1lll_opy_
    global bstack1l1lll1l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11llllll11_opy_ = webdriver.Remote.__init__
        bstack111l11l1l_opy_ = WebDriver.quit
        bstack11ll11lll1_opy_ = WebDriver.close
        bstack1lll1ll11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⍢") in CONFIG or bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⍣") in CONFIG) and bstack11l1l1l1l_opy_():
        if bstack1111l1l1l_opy_() < version.parse(bstack1ll1ll1111_opy_):
            logger.error(bstack1l1l1111l_opy_.format(bstack1111l1l1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⍤")) and callable(getattr(RemoteConnection, bstack1l1ll1_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⍥"))):
                    bstack1lll1llll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1lll1llll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11lll1l11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll1lll1l_opy_ = Config.getoption
        from _pytest import runner
        bstack1l11l1lll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l111l11ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1lll1l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ⍦"))
    bstack1111ll11l_opy_ = CONFIG.get(bstack1l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⍧"), {}).get(bstack1l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⍨"))
    bstack11111ll1l_opy_ = True
    bstack111ll1l1l_opy_(bstack11llll11ll_opy_)
if (bstack11l111lllll_opy_()):
    bstack1llll1lll1ll_opy_()
@bstack111l1111ll_opy_(class_method=False)
def bstack1llll1ll1111_opy_(hook_name, event, bstack1l11111l1ll_opy_=None):
    if hook_name not in [bstack1l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⍩"), bstack1l1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⍪"), bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⍫"), bstack1l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⍬"), bstack1l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⍭"), bstack1l1ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⍮"), bstack1l1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⍯"), bstack1l1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⍰")]:
        return
    node = store[bstack1l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⍱")]
    if hook_name in [bstack1l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⍲"), bstack1l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⍳")]:
        node = store[bstack1l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ⍴")]
    elif hook_name in [bstack1l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⍵"), bstack1l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⍶")]:
        node = store[bstack1l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ⍷")]
    hook_type = bstack11111l11l1l_opy_(hook_name)
    if event == bstack1l1ll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⍸"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_[hook_type], bstack1ll1lllll1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l111l_opy_ = {
            bstack1l1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⍹"): uuid,
            bstack1l1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⍺"): bstack1llllll1l_opy_(),
            bstack1l1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⍻"): bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⍼"),
            bstack1l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⍽"): hook_type,
            bstack1l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⍾"): hook_name
        }
        store[bstack1l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⍿")].append(uuid)
        bstack1llll1l1llll_opy_ = node.nodeid
        if hook_type == bstack1l1ll1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⎀"):
            if not _111l111l1l_opy_.get(bstack1llll1l1llll_opy_, None):
                _111l111l1l_opy_[bstack1llll1l1llll_opy_] = {bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⎁"): []}
            _111l111l1l_opy_[bstack1llll1l1llll_opy_][bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⎂")].append(bstack111l1l111l_opy_[bstack1l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⎃")])
        _111l111l1l_opy_[bstack1llll1l1llll_opy_ + bstack1l1ll1_opy_ (u"࠭࠭ࠨ⎄") + hook_name] = bstack111l1l111l_opy_
        bstack1llll1ll111l_opy_(node, bstack111l1l111l_opy_, bstack1l1ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⎅"))
    elif event == bstack1l1ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⎆"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1llll111_opy_[hook_type], bstack1ll1lllll1l_opy_.POST, node, None, bstack1l11111l1ll_opy_)
            return
        bstack111lll111l_opy_ = node.nodeid + bstack1l1ll1_opy_ (u"ࠩ࠰ࠫ⎇") + hook_name
        _111l111l1l_opy_[bstack111lll111l_opy_][bstack1l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⎈")] = bstack1llllll1l_opy_()
        bstack1llll1lll111_opy_(_111l111l1l_opy_[bstack111lll111l_opy_][bstack1l1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎉")])
        bstack1llll1ll111l_opy_(node, _111l111l1l_opy_[bstack111lll111l_opy_], bstack1l1ll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⎊"), bstack1llll1ll1l11_opy_=bstack1l11111l1ll_opy_)
def bstack1llll1l11111_opy_():
    global bstack1llll1l1l11l_opy_
    if bstack1ll11l111l_opy_():
        bstack1llll1l1l11l_opy_ = bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⎋")
    else:
        bstack1llll1l1l11l_opy_ = bstack1l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⎌")
@bstack1l1lll1l_opy_.bstack1lllll1lllll_opy_
def bstack1llll1l1111l_opy_():
    bstack1llll1l11111_opy_()
    if cli.is_running():
        try:
            bstack111ll1lll1l_opy_(bstack1llll1ll1111_opy_)
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⎍").format(e))
        return
    if bstack11l1l1l1l_opy_():
        bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
        bstack1l1ll1_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ⎎")
        if bstack11lll111ll_opy_.get_property(bstack1l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⎏")):
            if CONFIG.get(bstack1l1ll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ⎐")) is not None and int(CONFIG[bstack1l1ll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⎑")]) > 1:
                bstack11l1l1111_opy_(bstack11l11l11l1_opy_)
            return
        bstack11l1l1111_opy_(bstack11l11l11l1_opy_)
    try:
        bstack111ll1lll1l_opy_(bstack1llll1ll1111_opy_)
    except Exception as e:
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⎒").format(e))
bstack1llll1l1111l_opy_()