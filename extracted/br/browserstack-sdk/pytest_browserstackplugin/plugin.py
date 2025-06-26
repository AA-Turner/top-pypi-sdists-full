# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l1ll1111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll1l1l_opy_, bstack1llll11l1_opy_, update, bstack1lll1l1ll_opy_,
                                       bstack11111lll1_opy_, bstack111l1ll11_opy_, bstack11ll111ll_opy_, bstack1ll11l11l_opy_,
                                       bstack1l1lllll_opy_, bstack11l11ll1_opy_, bstack1l1lll1lll_opy_,
                                       bstack1llll11lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11l1l11l_opy_)
from browserstack_sdk.bstack1lll1l11l1_opy_ import bstack1l1lllllll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11l1l1l111_opy_
from bstack_utils.capture import bstack111llll1l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l11l1111_opy_, bstack1l1l11111_opy_, bstack1l11l1lll1_opy_, \
    bstack1llll111l1_opy_
from bstack_utils.helper import bstack11111ll1l_opy_, bstack111lllll1ll_opy_, bstack111ll111ll_opy_, bstack1ll1ll1l1_opy_, bstack1l1lll11111_opy_, bstack1ll1l11l11_opy_, \
    bstack111lllll111_opy_, \
    bstack11l11l1l1ll_opy_, bstack11l1ll111_opy_, bstack1ll11l11_opy_, bstack11l11l11lll_opy_, bstack1lll111l_opy_, Notset, \
    bstack1l1ll11l1l_opy_, bstack11l111l1111_opy_, bstack111llll1lll_opy_, Result, bstack111lll1l11l_opy_, bstack11l1l11l11l_opy_, bstack111l1llll1_opy_, \
    bstack11llllll1_opy_, bstack1llll1l1ll_opy_, bstack11l1l111ll_opy_, bstack111lll1l1ll_opy_
from bstack_utils.bstack111lll11lll_opy_ import bstack111ll1lll11_opy_
from bstack_utils.messages import bstack1l1llll1ll_opy_, bstack11ll1111l1_opy_, bstack1ll11l1ll1_opy_, bstack11ll1111ll_opy_, bstack11l1l11l_opy_, \
    bstack11ll1l1l1_opy_, bstack11lllll111_opy_, bstack11lll111ll_opy_, bstack1l11ll111l_opy_, bstack1ll111lll1_opy_, \
    bstack11ll1ll11l_opy_, bstack11ll1ll111_opy_
from bstack_utils.proxy import bstack1l1ll11l_opy_, bstack1l1l1ll1l1_opy_
from bstack_utils.bstack11l11l1lll_opy_ import bstack11111l1l1l1_opy_, bstack11111l1l1ll_opy_, bstack11111l11l1l_opy_, bstack11111l1l11l_opy_, \
    bstack11111l11l11_opy_, bstack11111l111l1_opy_, bstack11111l1ll11_opy_, bstack1lll1l11_opy_, bstack11111l111ll_opy_
from bstack_utils.bstack1l1111l111_opy_ import bstack1l1l1l1l1l_opy_
from bstack_utils.bstack11l1l111_opy_ import bstack1l11llll_opy_, bstack1ll1111ll_opy_, bstack1l111111l1_opy_, \
    bstack1l1ll11lll_opy_, bstack1lllll11_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack111ll1lll1_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack1l1111l1_opy_
import bstack_utils.accessibility as bstack1lll11l1_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack1l1l11ll11_opy_
from bstack_utils.bstack1ll111ll11_opy_ import bstack1ll111ll11_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack1ll1lll1_opy_
from browserstack_sdk.__init__ import bstack11l11llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111lll_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack11l11lll1l_opy_ import bstack11l11lll1l_opy_, bstack1llllll1l1_opy_, bstack1111111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111l11l11_opy_, bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l11lll1l_opy_ import bstack11l11lll1l_opy_, bstack1llllll1l1_opy_, bstack1111111ll_opy_
bstack1l11111l11_opy_ = None
bstack11l11l1l1_opy_ = None
bstack1ll11111l_opy_ = None
bstack1l1lll11_opy_ = None
bstack11llllll1l_opy_ = None
bstack1ll1l11111_opy_ = None
bstack111l1lll1_opy_ = None
bstack1l1111ll_opy_ = None
bstack1111l1l11_opy_ = None
bstack11l11llll_opy_ = None
bstack1l1l1ll11l_opy_ = None
bstack1lll111l11_opy_ = None
bstack1ll1llll_opy_ = None
bstack11l11lll11_opy_ = bstack11ll1l1_opy_ (u"ࠧࠨℲ")
CONFIG = {}
bstack1lll1ll111_opy_ = False
bstack1l1l11l1ll_opy_ = bstack11ll1l1_opy_ (u"ࠨࠩℳ")
bstack11ll1lllll_opy_ = bstack11ll1l1_opy_ (u"ࠩࠪℴ")
bstack1ll111l11l_opy_ = False
bstack1lll11lll1_opy_ = []
bstack1l111lll1l_opy_ = bstack1l11l1111_opy_
bstack1llll1l1l11l_opy_ = bstack11ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪℵ")
bstack111llll1_opy_ = {}
bstack1llll1ll1l_opy_ = None
bstack1ll1lll1l1_opy_ = False
logger = bstack11l1l1l111_opy_.get_logger(__name__, bstack1l111lll1l_opy_)
store = {
    bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨℶ"): []
}
bstack1llll1ll11l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11ll11_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111l11l11_opy_(
    test_framework_name=bstack11l1l1ll_opy_[bstack11ll1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩℷ")] if bstack1lll111l_opy_() else bstack11l1l1ll_opy_[bstack11ll1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭ℸ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1ll1111ll1_opy_(page, bstack11l111ll11_opy_):
    try:
        page.evaluate(bstack11ll1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣℹ"),
                      bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ℺") + json.dumps(
                          bstack11l111ll11_opy_) + bstack11ll1l1_opy_ (u"ࠤࢀࢁࠧ℻"))
    except Exception as e:
        print(bstack11ll1l1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣℼ"), e)
def bstack1l1l1111l_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧℽ"), bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪℾ") + json.dumps(
            message) + bstack11ll1l1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩℿ") + json.dumps(level) + bstack11ll1l1_opy_ (u"ࠧࡾࡿࠪ⅀"))
    except Exception as e:
        print(bstack11ll1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⅁"), e)
def pytest_configure(config):
    global bstack1l1l11l1ll_opy_
    global CONFIG
    bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
    config.args = bstack1l1111l1_opy_.bstack1llll1llll1l_opy_(config.args)
    bstack1111ll111_opy_.bstack1ll1l1l1_opy_(bstack11l1l111ll_opy_(config.getoption(bstack11ll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⅂"))))
    try:
        bstack11l1l1l111_opy_.bstack111ll1l1111_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11l11lll1l_opy_.invoke(bstack1llllll1l1_opy_.CONNECT, bstack1111111ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⅃"), bstack11ll1l1_opy_ (u"ࠫ࠵࠭⅄")))
        config = json.loads(os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦⅅ"), bstack11ll1l1_opy_ (u"ࠨࡻࡾࠤⅆ")))
        cli.bstack1ll1l1lll11_opy_(bstack1ll11l11_opy_(bstack1l1l11l1ll_opy_, CONFIG), cli_context.platform_index, bstack1lll1l1ll_opy_)
    if cli.bstack1lll11l11l1_opy_(bstack1lll11lllll_opy_):
        cli.bstack1lll1ll1lll_opy_()
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨⅇ") + str(cli_context.platform_index) + bstack11ll1l1_opy_ (u"ࠣࠤⅈ"))
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.BEFORE_ALL, bstack1lll1111l1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11ll1l1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢⅉ"), None)
    if cli.is_running() and when == bstack11ll1l1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⅊"):
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.LOG_REPORT, bstack1lll1111l1l_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11ll1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⅋"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll1l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⅌")))
        if not passed:
            config = json.loads(os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ⅍"), bstack11ll1l1_opy_ (u"ࠢࡼࡿࠥⅎ")))
            if bstack1ll1lll1_opy_.bstack1lll1l1l11_opy_(config):
                bstack1111lllllll_opy_ = bstack1ll1lll1_opy_.bstack1ll11l1111_opy_(config)
                if item.execution_count > bstack1111lllllll_opy_:
                    print(bstack11ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡸࡥࡵࡴ࡬ࡩࡸࡀࠠࠨ⅏"), report.nodeid, os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⅐")))
                    bstack1ll1lll1_opy_.bstack111l11ll111_opy_(report.nodeid)
            else:
                print(bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠪ⅑"), report.nodeid, os.environ.get(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⅒")))
                bstack1ll1lll1_opy_.bstack111l11ll111_opy_(report.nodeid)
        else:
            print(bstack11ll1l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡴࡦࡹࡳࡦࡦ࠽ࠤࠬ⅓"), report.nodeid, os.environ.get(bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⅔")))
    if cli.is_running():
        if when == bstack11ll1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⅕"):
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.BEFORE_EACH, bstack1lll1111l1l_opy_.POST, item, call, outcome)
        elif when == bstack11ll1l1_opy_ (u"ࠣࡥࡤࡰࡱࠨ⅖"):
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.LOG_REPORT, bstack1lll1111l1l_opy_.POST, item, call, outcome)
        elif when == bstack11ll1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ⅗"):
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.AFTER_EACH, bstack1lll1111l1l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    skipSessionName = item.config.getoption(bstack11ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⅘"))
    plugins = item.config.getoption(bstack11ll1l1_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧ⅙"))
    report = outcome.get_result()
    os.environ[bstack11ll1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⅚")] = report.nodeid
    bstack1llll1l11lll_opy_(item, call, report)
    if bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦ⅛") not in plugins or bstack1lll111l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll1l1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣ⅜"), None)
    page = getattr(item, bstack11ll1l1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢ⅝"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll1ll1l11_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll1ll1l1l_opy_(item, report, summary, skipSessionName)
def bstack1llll1ll1l11_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⅞") and report.skipped:
        bstack11111l111ll_opy_(report)
    if report.when in [bstack11ll1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⅟"), bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨⅠ")]:
        return
    if not bstack1l1lll11111_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11ll1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪⅡ")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫⅢ") + json.dumps(
                    report.nodeid) + bstack11ll1l1_opy_ (u"ࠧࡾࡿࠪⅣ"))
        os.environ[bstack11ll1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫⅤ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll1l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤⅥ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll1l1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧⅦ")))
    bstack1l1l1111_opy_ = bstack11ll1l1_opy_ (u"ࠦࠧⅧ")
    bstack11111l111ll_opy_(report)
    if not passed:
        try:
            bstack1l1l1111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧⅨ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll1l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣⅩ")))
        bstack1l1l1111_opy_ = bstack11ll1l1_opy_ (u"ࠢࠣⅪ")
        if not passed:
            try:
                bstack1l1l1111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣⅫ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭Ⅼ")
                    + json.dumps(bstack11ll1l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦⅭ"))
                    + bstack11ll1l1_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢⅮ")
                )
            else:
                item._driver.execute_script(
                    bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪⅯ")
                    + json.dumps(str(bstack1l1l1111_opy_))
                    + bstack11ll1l1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤⅰ")
                )
        except Exception as e:
            summary.append(bstack11ll1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧⅱ").format(e))
def bstack1llll1l11111_opy_(test_name, error_message):
    try:
        bstack1llll1ll1111_opy_ = []
        bstack1l1l111l_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨⅲ"), bstack11ll1l1_opy_ (u"ࠩ࠳ࠫⅳ"))
        bstack11111lll_opy_ = {bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨⅴ"): test_name, bstack11ll1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪⅵ"): error_message, bstack11ll1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫⅶ"): bstack1l1l111l_opy_}
        bstack1llll11llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫⅷ"))
        if os.path.exists(bstack1llll11llll1_opy_):
            with open(bstack1llll11llll1_opy_) as f:
                bstack1llll1ll1111_opy_ = json.load(f)
        bstack1llll1ll1111_opy_.append(bstack11111lll_opy_)
        with open(bstack1llll11llll1_opy_, bstack11ll1l1_opy_ (u"ࠧࡸࠩⅸ")) as f:
            json.dump(bstack1llll1ll1111_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ⅹ") + str(e))
def bstack1llll1ll1l1l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11ll1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣⅺ"), bstack11ll1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧⅻ")]:
        return
    if (str(skipSessionName).lower() != bstack11ll1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩⅼ")):
        bstack1ll1111ll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll1l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢⅽ")))
    bstack1l1l1111_opy_ = bstack11ll1l1_opy_ (u"ࠨࠢⅾ")
    bstack11111l111ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l1111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢⅿ").format(e)
                )
        try:
            if passed:
                bstack1lllll11_opy_(getattr(item, bstack11ll1l1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧↀ"), None), bstack11ll1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤↁ"))
            else:
                error_message = bstack11ll1l1_opy_ (u"ࠪࠫↂ")
                if bstack1l1l1111_opy_:
                    bstack1l1l1111l_opy_(item._page, str(bstack1l1l1111_opy_), bstack11ll1l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥↃ"))
                    bstack1lllll11_opy_(getattr(item, bstack11ll1l1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫↄ"), None), bstack11ll1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨↅ"), str(bstack1l1l1111_opy_))
                    error_message = str(bstack1l1l1111_opy_)
                else:
                    bstack1lllll11_opy_(getattr(item, bstack11ll1l1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ↆ"), None), bstack11ll1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣↇ"))
                bstack1llll1l11111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll1l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨↈ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11ll1l1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ↉"), default=bstack11ll1l1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ↊"), help=bstack11ll1l1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ↋"))
    parser.addoption(bstack11ll1l1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ↌"), default=bstack11ll1l1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ↍"), help=bstack11ll1l1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ↎"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll1l1_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ↏"), action=bstack11ll1l1_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ←"), default=bstack11ll1l1_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ↑"),
                         help=bstack11ll1l1_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦ→"))
def bstack111lll1lll_opy_(log):
    if not (log[bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ↓")] and log[bstack11ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ↔")].strip()):
        return
    active = bstack111llll111_opy_()
    log = {
        bstack11ll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ↕"): log[bstack11ll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ↖")],
        bstack11ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭↗"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"ࠫ࡟࠭↘"),
        bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭↙"): log[bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ↚")],
    }
    if active:
        if active[bstack11ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ↛")] == bstack11ll1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭↜"):
            log[bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ↝")] = active[bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ↞")]
        elif active[bstack11ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ↟")] == bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ↠"):
            log[bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭↡")] = active[bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ↢")]
    bstack1l1l11ll11_opy_.bstack1ll111l1l1_opy_([log])
def bstack111llll111_opy_():
    if len(store[bstack11ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ↣")]) > 0 and store[bstack11ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭↤")][-1]:
        return {
            bstack11ll1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ↥"): bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ↦"),
            bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ↧"): store[bstack11ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ↨")][-1]
        }
    if store.get(bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ↩"), None):
        return {
            bstack11ll1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭↪"): bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧ↫"),
            bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ↬"): store[bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ↭")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.INIT_TEST, bstack1lll1111l1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.INIT_TEST, bstack1lll1111l1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llll11lllll_opy_ = True
        bstack1lllllll1l_opy_ = bstack1lll11l1_opy_.bstack1lll11l1l1_opy_(bstack11l11l1l1ll_opy_(item.own_markers))
        if not cli.bstack1lll11l11l1_opy_(bstack1lll11lllll_opy_):
            item._a11y_test_case = bstack1lllllll1l_opy_
            if bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ↮"), None):
                driver = getattr(item, bstack11ll1l1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ↯"), None)
                item._a11y_started = bstack1lll11l1_opy_.bstack111ll1l1l_opy_(driver, bstack1lllllll1l_opy_)
        if not bstack1l1l11ll11_opy_.on() or bstack1llll1l1l11l_opy_ != bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ↰"):
            return
        global current_test_uuid #, bstack111ll1l111_opy_
        bstack111l11l11l_opy_ = {
            bstack11ll1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↱"): uuid4().__str__(),
            bstack11ll1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭↲"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"ࠪ࡞ࠬ↳")
        }
        current_test_uuid = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ↴")]
        store[bstack11ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ↵")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↶")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11ll11_opy_[item.nodeid] = {**_111l11ll11_opy_[item.nodeid], **bstack111l11l11l_opy_}
        bstack1llll1l1ll11_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11ll1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ↷"))
    except Exception as err:
        print(bstack11ll1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ↸"), str(err))
def pytest_runtest_setup(item):
    store[bstack11ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭↹")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.BEFORE_EACH, bstack1lll1111l1l_opy_.PRE, item, bstack11ll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ↺"))
    if bstack1ll1lll1_opy_.bstack111l1l1l1ll_opy_():
            bstack1llll1l1111l_opy_ = bstack11ll1l1_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡦࡹࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ↻")
            logger.error(bstack1llll1l1111l_opy_)
            bstack111l11l11l_opy_ = {
                bstack11ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ↼"): uuid4().__str__(),
                bstack11ll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ↽"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"࡛ࠧࠩ↾"),
                bstack11ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭↿"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"ࠩ࡝ࠫ⇀"),
                bstack11ll1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⇁"): bstack11ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⇂"),
                bstack11ll1l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⇃"): bstack1llll1l1111l_opy_,
                bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⇄"): [],
                bstack11ll1l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⇅"): []
            }
            bstack1llll1l1ll11_opy_(item, bstack111l11l11l_opy_, bstack11ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⇆"))
            pytest.skip(bstack1llll1l1111l_opy_)
            return # skip all existing bstack1llll1l11l1l_opy_
    global bstack1llll1ll11l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11l11lll_opy_():
        atexit.register(bstack11lll11l1l_opy_)
        if not bstack1llll1ll11l1_opy_:
            try:
                bstack1llll1ll1ll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111lll1l1ll_opy_():
                    bstack1llll1ll1ll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1ll1ll1_opy_:
                    signal.signal(s, bstack1llll1l1llll_opy_)
                bstack1llll1ll11l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ⇇") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l1l1l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⇈")
    try:
        if not bstack1l1l11ll11_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11l11l_opy_ = {
            bstack11ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇉"): uuid,
            bstack11ll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⇊"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"࡚࠭ࠨ⇋"),
            bstack11ll1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⇌"): bstack11ll1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭⇍"),
            bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⇎"): bstack11ll1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⇏"),
            bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⇐"): bstack11ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⇑")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⇒")] = item
        store[bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇓")] = [uuid]
        if not _111l11ll11_opy_.get(item.nodeid, None):
            _111l11ll11_opy_[item.nodeid] = {bstack11ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⇔"): [], bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⇕"): []}
        _111l11ll11_opy_[item.nodeid][bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⇖")].append(bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇗")])
        _111l11ll11_opy_[item.nodeid + bstack11ll1l1_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ⇘")] = bstack111l11l11l_opy_
        bstack1llll1l111ll_opy_(item, bstack111l11l11l_opy_, bstack11ll1l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⇙"))
    except Exception as err:
        print(bstack11ll1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ⇚"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.AFTER_EACH, bstack1lll1111l1l_opy_.PRE, item, bstack11ll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⇛"))
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        global bstack111llll1_opy_
        bstack1l1l111l_opy_ = 0
        if bstack1ll111l11l_opy_ is True:
            bstack1l1l111l_opy_ = int(os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⇜")))
        if bstack11ll1l11ll_opy_.bstack1l1ll1l11_opy_() == bstack11ll1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ⇝"):
            if bstack11ll1l11ll_opy_.bstack1ll1ll11ll_opy_() == bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ⇞"):
                bstack1llll1l1lll1_opy_ = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⇟"), None)
                bstack1111111l1_opy_ = bstack1llll1l1lll1_opy_ + bstack11ll1l1_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤ⇠")
                driver = getattr(item, bstack11ll1l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⇡"), None)
                bstack1ll1l1ll11_opy_ = getattr(item, bstack11ll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭⇢"), None)
                bstack11llll11l_opy_ = getattr(item, bstack11ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⇣"), None)
                PercySDK.screenshot(driver, bstack1111111l1_opy_, bstack1ll1l1ll11_opy_=bstack1ll1l1ll11_opy_, bstack11llll11l_opy_=bstack11llll11l_opy_, bstack111l11l1l_opy_=bstack1l1l111l_opy_)
        if not cli.bstack1lll11l11l1_opy_(bstack1lll11lllll_opy_):
            if getattr(item, bstack11ll1l1_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ⇤"), False):
                bstack1l1lllllll_opy_.bstack1l1lllll11_opy_(getattr(item, bstack11ll1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⇥"), None), bstack111llll1_opy_, logger, item)
        if not bstack1l1l11ll11_opy_.on():
            return
        bstack111l11l11l_opy_ = {
            bstack11ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⇦"): uuid4().__str__(),
            bstack11ll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⇧"): bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"࡛ࠧࠩ⇨"),
            bstack11ll1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭⇩"): bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⇪"),
            bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⇫"): bstack11ll1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ⇬"),
            bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⇭"): bstack11ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⇮")
        }
        _111l11ll11_opy_[item.nodeid + bstack11ll1l1_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⇯")] = bstack111l11l11l_opy_
        bstack1llll1l111ll_opy_(item, bstack111l11l11l_opy_, bstack11ll1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⇰"))
    except Exception as err:
        print(bstack11ll1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨ⇱"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111l1l11l_opy_(fixturedef.argname):
        store[bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⇲")] = request.node
    elif bstack11111l11l11_opy_(fixturedef.argname):
        store[bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⇳")] = request.node
    if not bstack1l1l11ll11_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.SETUP_FIXTURE, bstack1lll1111l1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.SETUP_FIXTURE, bstack1lll1111l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.SETUP_FIXTURE, bstack1lll1111l1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.SETUP_FIXTURE, bstack1lll1111l1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        fixture = {
            bstack11ll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⇴"): fixturedef.argname,
            bstack11ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⇵"): bstack111lllll111_opy_(outcome),
            bstack11ll1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⇶"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⇷")]
        if not _111l11ll11_opy_.get(current_test_item.nodeid, None):
            _111l11ll11_opy_[current_test_item.nodeid] = {bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⇸"): []}
        _111l11ll11_opy_[current_test_item.nodeid][bstack11ll1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⇹")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ⇺"), str(err))
if bstack1lll111l_opy_() and bstack1l1l11ll11_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.STEP, bstack1lll1111l1l_opy_.PRE, request, step)
            return
        try:
            _111l11ll11_opy_[request.node.nodeid][bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⇻")].bstack1llll1ll_opy_(id(step))
        except Exception as err:
            print(bstack11ll1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ⇼"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.STEP, bstack1lll1111l1l_opy_.POST, request, step, exception)
            return
        try:
            _111l11ll11_opy_[request.node.nodeid][bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⇽")].bstack111lll111l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⇾"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.STEP, bstack1lll1111l1l_opy_.POST, request, step)
            return
        try:
            bstack111ll1ll11_opy_: bstack111ll1lll1_opy_ = _111l11ll11_opy_[request.node.nodeid][bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⇿")]
            bstack111ll1ll11_opy_.bstack111lll111l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ∀"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1l1l11l_opy_
        try:
            if not bstack1l1l11ll11_opy_.on() or bstack1llll1l1l11l_opy_ != bstack11ll1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ∁"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ∂"), None)
            if not _111l11ll11_opy_.get(request.node.nodeid, None):
                _111l11ll11_opy_[request.node.nodeid] = {}
            bstack111ll1ll11_opy_ = bstack111ll1lll1_opy_.bstack1llllllll1l1_opy_(
                scenario, feature, request.node,
                name=bstack11111l111l1_opy_(request.node, scenario),
                started_at=bstack1ll1l11l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll1l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ∃"),
                tags=bstack11111l1ll11_opy_(feature, scenario),
                bstack111ll1l1ll_opy_=bstack1l1l11ll11_opy_.bstack111llll1ll_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11ll11_opy_[request.node.nodeid][bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ∄")] = bstack111ll1ll11_opy_
            bstack1llll1l11l11_opy_(bstack111ll1ll11_opy_.uuid)
            bstack1l1l11ll11_opy_.bstack111ll11lll_opy_(bstack11ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ∅"), bstack111ll1ll11_opy_)
        except Exception as err:
            print(bstack11ll1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ∆"), str(err))
def bstack1llll11lll1l_opy_(bstack111lllll11_opy_):
    if bstack111lllll11_opy_ in store[bstack11ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ∇")]:
        store[bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ∈")].remove(bstack111lllll11_opy_)
def bstack1llll1l11l11_opy_(test_uuid):
    store[bstack11ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ∉")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1l11ll11_opy_.bstack1lllll11llll_opy_
def bstack1llll1l11lll_opy_(item, call, report):
    logger.debug(bstack11ll1l1_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ∊"))
    global bstack1llll1l1l11l_opy_
    bstack1l1111l1l1_opy_ = bstack1ll1l11l11_opy_()
    if hasattr(report, bstack11ll1l1_opy_ (u"ࠧࡴࡶࡲࡴࠬ∋")):
        bstack1l1111l1l1_opy_ = bstack111lll1l11l_opy_(report.stop)
    elif hasattr(report, bstack11ll1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ∌")):
        bstack1l1111l1l1_opy_ = bstack111lll1l11l_opy_(report.start)
    try:
        if getattr(report, bstack11ll1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ∍"), bstack11ll1l1_opy_ (u"ࠪࠫ∎")) == bstack11ll1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ∏"):
            logger.debug(bstack11ll1l1_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ∐").format(getattr(report, bstack11ll1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫ∑"), bstack11ll1l1_opy_ (u"ࠧࠨ−")).__str__(), bstack1llll1l1l11l_opy_))
            if bstack1llll1l1l11l_opy_ == bstack11ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ∓"):
                _111l11ll11_opy_[item.nodeid][bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∔")] = bstack1l1111l1l1_opy_
                bstack1llll1l1ll11_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ∕"), report, call)
                store[bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ∖")] = None
            elif bstack1llll1l1l11l_opy_ == bstack11ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ∗"):
                bstack111ll1ll11_opy_ = _111l11ll11_opy_[item.nodeid][bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ∘")]
                bstack111ll1ll11_opy_.set(hooks=_111l11ll11_opy_[item.nodeid].get(bstack11ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭∙"), []))
                exception, bstack111lll11l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll11l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll1l1_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧ√"), bstack11ll1l1_opy_ (u"ࠩࠪ∛"))]
                bstack111ll1ll11_opy_.stop(time=bstack1l1111l1l1_opy_, result=Result(result=getattr(report, bstack11ll1l1_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ∜"), bstack11ll1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ∝")), exception=exception, bstack111lll11l1_opy_=bstack111lll11l1_opy_))
                bstack1l1l11ll11_opy_.bstack111ll11lll_opy_(bstack11ll1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ∞"), _111l11ll11_opy_[item.nodeid][bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ∟")])
        elif getattr(report, bstack11ll1l1_opy_ (u"ࠧࡸࡪࡨࡲࠬ∠"), bstack11ll1l1_opy_ (u"ࠨࠩ∡")) in [bstack11ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ∢"), bstack11ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ∣")]:
            logger.debug(bstack11ll1l1_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭∤").format(getattr(report, bstack11ll1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ∥"), bstack11ll1l1_opy_ (u"࠭ࠧ∦")).__str__(), bstack1llll1l1l11l_opy_))
            bstack111ll11ll1_opy_ = item.nodeid + bstack11ll1l1_opy_ (u"ࠧ࠮ࠩ∧") + getattr(report, bstack11ll1l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭∨"), bstack11ll1l1_opy_ (u"ࠩࠪ∩"))
            if getattr(report, bstack11ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ∪"), False):
                hook_type = bstack11ll1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ∫") if getattr(report, bstack11ll1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ∬"), bstack11ll1l1_opy_ (u"࠭ࠧ∭")) == bstack11ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭∮") else bstack11ll1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ∯")
                _111l11ll11_opy_[bstack111ll11ll1_opy_] = {
                    bstack11ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ∰"): uuid4().__str__(),
                    bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ∱"): bstack1l1111l1l1_opy_,
                    bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ∲"): hook_type
                }
            _111l11ll11_opy_[bstack111ll11ll1_opy_][bstack11ll1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ∳")] = bstack1l1111l1l1_opy_
            bstack1llll11lll1l_opy_(_111l11ll11_opy_[bstack111ll11ll1_opy_][bstack11ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ∴")])
            bstack1llll1l111ll_opy_(item, _111l11ll11_opy_[bstack111ll11ll1_opy_], bstack11ll1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ∵"), report, call)
            if getattr(report, bstack11ll1l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭∶"), bstack11ll1l1_opy_ (u"ࠩࠪ∷")) == bstack11ll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ∸"):
                if getattr(report, bstack11ll1l1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ∹"), bstack11ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ∺")) == bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭∻"):
                    bstack111l11l11l_opy_ = {
                        bstack11ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ∼"): uuid4().__str__(),
                        bstack11ll1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ∽"): bstack1ll1l11l11_opy_(),
                        bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∾"): bstack1ll1l11l11_opy_()
                    }
                    _111l11ll11_opy_[item.nodeid] = {**_111l11ll11_opy_[item.nodeid], **bstack111l11l11l_opy_}
                    bstack1llll1l1ll11_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ∿"))
                    bstack1llll1l1ll11_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭≀"), report, call)
    except Exception as err:
        print(bstack11ll1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ≁"), str(err))
def bstack1llll1l1ll1l_opy_(test, bstack111l11l11l_opy_, result=None, call=None, bstack11111l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111ll1ll11_opy_ = {
        bstack11ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ≂"): bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ≃")],
        bstack11ll1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭≄"): bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧ≅"),
        bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ≆"): test.name,
        bstack11ll1l1_opy_ (u"ࠫࡧࡵࡤࡺࠩ≇"): {
            bstack11ll1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ≈"): bstack11ll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭≉"),
            bstack11ll1l1_opy_ (u"ࠧࡤࡱࡧࡩࠬ≊"): inspect.getsource(test.obj)
        },
        bstack11ll1l1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ≋"): test.name,
        bstack11ll1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ≌"): test.name,
        bstack11ll1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ≍"): bstack1l1111l1_opy_.bstack1111lllll1_opy_(test),
        bstack11ll1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ≎"): file_path,
        bstack11ll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ≏"): file_path,
        bstack11ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭≐"): bstack11ll1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ≑"),
        bstack11ll1l1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭≒"): file_path,
        bstack11ll1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭≓"): bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ≔")],
        bstack11ll1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ≕"): bstack11ll1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ≖"),
        bstack11ll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ≗"): {
            bstack11ll1l1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ≘"): test.nodeid
        },
        bstack11ll1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭≙"): bstack11l11l1l1ll_opy_(test.own_markers)
    }
    if bstack11111l1l_opy_ in [bstack11ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ≚"), bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ≛")]:
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ≜")] = {
            bstack11ll1l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ≝"): bstack111l11l11l_opy_.get(bstack11ll1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ≞"), [])
        }
    if bstack11111l1l_opy_ == bstack11ll1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ≟"):
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≠")] = bstack11ll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ≡")
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ≢")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ≣")]
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≤")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≥")]
    if result:
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ≦")] = result.outcome
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ≧")] = result.duration * 1000
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ≨")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≩")]
        if result.failed:
            bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ≪")] = bstack1l1l11ll11_opy_.bstack11111l1111_opy_(call.excinfo.typename)
            bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭≫")] = bstack1l1l11ll11_opy_.bstack1lllll1l1lll_opy_(call.excinfo, result)
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≬")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭≭")]
    if outcome:
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≮")] = bstack111lllll111_opy_(outcome)
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ≯")] = 0
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≰")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≱")]
        if bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ≲")] == bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭≳"):
            bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭≴")] = bstack11ll1l1_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ≵")  # bstack1llll1ll1lll_opy_
            bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ≶")] = [{bstack11ll1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭≷"): [bstack11ll1l1_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ≸")]}]
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ≹")] = bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≺")]
    return bstack111ll1ll11_opy_
def bstack1llll1lll111_opy_(test, bstack111l111lll_opy_, bstack11111l1l_opy_, result, call, outcome, bstack1llll1ll11ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ≻")]
    hook_name = bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ≼")]
    hook_data = {
        bstack11ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ≽"): bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ≾")],
        bstack11ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ≿"): bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⊀"),
        bstack11ll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⊁"): bstack11ll1l1_opy_ (u"ࠧࡼࡿࠪ⊂").format(bstack11111l1l1ll_opy_(hook_name)),
        bstack11ll1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭⊃"): {
            bstack11ll1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⊄"): bstack11ll1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⊅"),
            bstack11ll1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩ⊆"): None
        },
        bstack11ll1l1_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⊇"): test.name,
        bstack11ll1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⊈"): bstack1l1111l1_opy_.bstack1111lllll1_opy_(test, hook_name),
        bstack11ll1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⊉"): file_path,
        bstack11ll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⊊"): file_path,
        bstack11ll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊋"): bstack11ll1l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⊌"),
        bstack11ll1l1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⊍"): file_path,
        bstack11ll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊎"): bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊏")],
        bstack11ll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⊐"): bstack11ll1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⊑") if bstack1llll1l1l11l_opy_ == bstack11ll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⊒") else bstack11ll1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⊓"),
        bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⊔"): hook_type
    }
    bstack1ll111l1111_opy_ = bstack111l11l1l1_opy_(_111l11ll11_opy_.get(test.nodeid, None))
    if bstack1ll111l1111_opy_:
        hook_data[bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⊕")] = bstack1ll111l1111_opy_
    if result:
        hook_data[bstack11ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⊖")] = result.outcome
        hook_data[bstack11ll1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⊗")] = result.duration * 1000
        hook_data[bstack11ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊘")] = bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⊙")]
        if result.failed:
            hook_data[bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⊚")] = bstack1l1l11ll11_opy_.bstack11111l1111_opy_(call.excinfo.typename)
            hook_data[bstack11ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⊛")] = bstack1l1l11ll11_opy_.bstack1lllll1l1lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⊜")] = bstack111lllll111_opy_(outcome)
        hook_data[bstack11ll1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⊝")] = 100
        hook_data[bstack11ll1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊞")] = bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊟")]
        if hook_data[bstack11ll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊠")] == bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⊡"):
            hook_data[bstack11ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⊢")] = bstack11ll1l1_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭⊣")  # bstack1llll1ll1lll_opy_
            hook_data[bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⊤")] = [{bstack11ll1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⊥"): [bstack11ll1l1_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⊦")]}]
    if bstack1llll1ll11ll_opy_:
        hook_data[bstack11ll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊧")] = bstack1llll1ll11ll_opy_.result
        hook_data[bstack11ll1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⊨")] = bstack11l111l1111_opy_(bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⊩")], bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⊪")])
        hook_data[bstack11ll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⊫")] = bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊬")]
        if hook_data[bstack11ll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⊭")] == bstack11ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⊮"):
            hook_data[bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⊯")] = bstack1l1l11ll11_opy_.bstack11111l1111_opy_(bstack1llll1ll11ll_opy_.exception_type)
            hook_data[bstack11ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⊰")] = [{bstack11ll1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⊱"): bstack111llll1lll_opy_(bstack1llll1ll11ll_opy_.exception)}]
    return hook_data
def bstack1llll1l1ll11_opy_(test, bstack111l11l11l_opy_, bstack11111l1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11ll1l1_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ⊲").format(bstack11111l1l_opy_))
    bstack111ll1ll11_opy_ = bstack1llll1l1ll1l_opy_(test, bstack111l11l11l_opy_, result, call, bstack11111l1l_opy_, outcome)
    driver = getattr(test, bstack11ll1l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⊳"), None)
    if bstack11111l1l_opy_ == bstack11ll1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⊴") and driver:
        bstack111ll1ll11_opy_[bstack11ll1l1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⊵")] = bstack1l1l11ll11_opy_.bstack111llll1ll_opy_(driver)
    if bstack11111l1l_opy_ == bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⊶"):
        bstack11111l1l_opy_ = bstack11ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⊷")
    bstack111l1l1l11_opy_ = {
        bstack11ll1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⊸"): bstack11111l1l_opy_,
        bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⊹"): bstack111ll1ll11_opy_
    }
    bstack1l1l11ll11_opy_.bstack11ll111ll1_opy_(bstack111l1l1l11_opy_)
    if bstack11111l1l_opy_ == bstack11ll1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⊺"):
        threading.current_thread().bstackTestMeta = {bstack11ll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⊻"): bstack11ll1l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⊼")}
    elif bstack11111l1l_opy_ == bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⊽"):
        threading.current_thread().bstackTestMeta = {bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⊾"): getattr(result, bstack11ll1l1_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⊿"), bstack11ll1l1_opy_ (u"࠭ࠧ⋀"))}
def bstack1llll1l111ll_opy_(test, bstack111l11l11l_opy_, bstack11111l1l_opy_, result=None, call=None, outcome=None, bstack1llll1ll11ll_opy_=None):
    logger.debug(bstack11ll1l1_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ⋁").format(bstack11111l1l_opy_))
    hook_data = bstack1llll1lll111_opy_(test, bstack111l11l11l_opy_, bstack11111l1l_opy_, result, call, outcome, bstack1llll1ll11ll_opy_)
    bstack111l1l1l11_opy_ = {
        bstack11ll1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⋂"): bstack11111l1l_opy_,
        bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ⋃"): hook_data
    }
    bstack1l1l11ll11_opy_.bstack11ll111ll1_opy_(bstack111l1l1l11_opy_)
def bstack111l11l1l1_opy_(bstack111l11l11l_opy_):
    if not bstack111l11l11l_opy_:
        return None
    if bstack111l11l11l_opy_.get(bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⋄"), None):
        return getattr(bstack111l11l11l_opy_[bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⋅")], bstack11ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⋆"), None)
    return bstack111l11l11l_opy_.get(bstack11ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⋇"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.LOG, bstack1lll1111l1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_.LOG, bstack1lll1111l1l_opy_.POST, request, caplog)
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        if not bstack1l1l11ll11_opy_.on():
            return
        places = [bstack11ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⋈"), bstack11ll1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭⋉"), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⋊")]
        logs = []
        for bstack1llll1l1l1l1_opy_ in places:
            records = caplog.get_records(bstack1llll1l1l1l1_opy_)
            bstack1llll11lll11_opy_ = bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⋋") if bstack1llll1l1l1l1_opy_ == bstack11ll1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⋌") else bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⋍")
            bstack1llll1l1l1ll_opy_ = request.node.nodeid + (bstack11ll1l1_opy_ (u"࠭ࠧ⋎") if bstack1llll1l1l1l1_opy_ == bstack11ll1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⋏") else bstack11ll1l1_opy_ (u"ࠨ࠯ࠪ⋐") + bstack1llll1l1l1l1_opy_)
            test_uuid = bstack111l11l1l1_opy_(_111l11ll11_opy_.get(bstack1llll1l1l1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1l11l11l_opy_(record.message):
                    continue
                logs.append({
                    bstack11ll1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⋑"): bstack111lllll1ll_opy_(record.created).isoformat() + bstack11ll1l1_opy_ (u"ࠪ࡞ࠬ⋒"),
                    bstack11ll1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⋓"): record.levelname,
                    bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⋔"): record.message,
                    bstack1llll11lll11_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1l11ll11_opy_.bstack1ll111l1l1_opy_(logs)
    except Exception as err:
        print(bstack11ll1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ⋕"), str(err))
def bstack1l1ll1ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll1lll1l1_opy_
    bstack1l11l11111_opy_ = bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ⋖"), None) and bstack11111ll1l_opy_(
            threading.current_thread(), bstack11ll1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⋗"), None)
    bstack11l111111l_opy_ = getattr(driver, bstack11ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⋘"), None) != None and getattr(driver, bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⋙"), None) == True
    if sequence == bstack11ll1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⋚") and driver != None:
      if not bstack1ll1lll1l1_opy_ and bstack1l1lll11111_opy_() and bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⋛") in CONFIG and CONFIG[bstack11ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⋜")] == True and bstack1ll111ll11_opy_.bstack1ll1l1l1ll_opy_(driver_command) and (bstack11l111111l_opy_ or bstack1l11l11111_opy_) and not bstack1l11l1l11l_opy_(args):
        try:
          bstack1ll1lll1l1_opy_ = True
          logger.debug(bstack11ll1l1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ⋝").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll1l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭⋞").format(str(err)))
        bstack1ll1lll1l1_opy_ = False
    if sequence == bstack11ll1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⋟"):
        if driver_command == bstack11ll1l1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ⋠"):
            bstack1l1l11ll11_opy_.bstack1l1111ll1l_opy_({
                bstack11ll1l1_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⋡"): response[bstack11ll1l1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⋢")],
                bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⋣"): store[bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⋤")]
            })
def bstack11lll11l1l_opy_():
    global bstack1lll11lll1_opy_
    bstack11l1l1l111_opy_.bstack1lll1l1ll1_opy_()
    logging.shutdown()
    bstack1l1l11ll11_opy_.bstack1111llll11_opy_()
    for driver in bstack1lll11lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l1llll_opy_(*args):
    global bstack1lll11lll1_opy_
    bstack1l1l11ll11_opy_.bstack1111llll11_opy_()
    for driver in bstack1lll11lll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11lll1l1l1_opy_, stage=STAGE.bstack11l1lll1l1_opy_, bstack11llll111l_opy_=bstack1llll1ll1l_opy_)
def bstack1ll1l111l1_opy_(self, *args, **kwargs):
    bstack11l1111l_opy_ = bstack1l11111l11_opy_(self, *args, **kwargs)
    bstack1llllll1ll_opy_ = getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⋥"), None)
    if bstack1llllll1ll_opy_ and bstack1llllll1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⋦"), bstack11ll1l1_opy_ (u"ࠪࠫ⋧")) == bstack11ll1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⋨"):
        bstack1l1l11ll11_opy_.bstack1l1l1l1ll1_opy_(self)
    return bstack11l1111l_opy_
@measure(event_name=EVENTS.bstack1l1111lll_opy_, stage=STAGE.bstack111l1l1l1_opy_, bstack11llll111l_opy_=bstack1llll1ll1l_opy_)
def bstack1l11ll11l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
    if bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⋩")):
        return
    bstack1111ll111_opy_.bstack1lll1lll_opy_(bstack11ll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⋪"), True)
    global bstack11l11lll11_opy_
    global bstack111lll11l_opy_
    bstack11l11lll11_opy_ = framework_name
    logger.info(bstack11ll1ll111_opy_.format(bstack11l11lll11_opy_.split(bstack11ll1l1_opy_ (u"ࠧ࠮ࠩ⋫"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lll11111_opy_():
            Service.start = bstack11ll111ll_opy_
            Service.stop = bstack1ll11l11l_opy_
            webdriver.Remote.get = bstack1lllll1l1_opy_
            webdriver.Remote.__init__ = bstack1l1ll111l1_opy_
            if not isinstance(os.getenv(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ⋬")), str):
                return
            WebDriver.quit = bstack11ll1ll1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1l11ll11_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1l111l1_opy_
        bstack111lll11l_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⋭")):
        bstack111lll11l_opy_ = eval(os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⋮")))
    if not bstack111lll11l_opy_:
        bstack11l11ll1_opy_(bstack11ll1l1_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ⋯"), bstack11ll1ll11l_opy_)
    if bstack11l1111111_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11ll1l1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⋰")) and callable(getattr(RemoteConnection, bstack11ll1l1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⋱"))):
                RemoteConnection._get_proxy_url = bstack1l1ll1lll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1ll1lll_opy_
        except Exception as e:
            logger.error(bstack11ll1l1l1_opy_.format(str(e)))
    if bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⋲") in str(framework_name).lower():
        if not bstack1l1lll11111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11111lll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l1ll11_opy_
            Config.getoption = bstack1l1ll1ll1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll111111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l111lll_opy_, stage=STAGE.bstack11l1lll1l1_opy_, bstack11llll111l_opy_=bstack1llll1ll1l_opy_)
def bstack11ll1ll1l_opy_(self):
    global bstack11l11lll11_opy_
    global bstack11ll11llll_opy_
    global bstack11l11l1l1_opy_
    try:
        if bstack11ll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⋳") in bstack11l11lll11_opy_ and self.session_id != None and bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭⋴"), bstack11ll1l1_opy_ (u"ࠪࠫ⋵")) != bstack11ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⋶"):
            bstack1l1111111l_opy_ = bstack11ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⋷") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⋸")
            bstack1llll1l1ll_opy_(logger, True)
            if os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⋹"), None):
                self.execute_script(
                    bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⋺") + json.dumps(
                        os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⋻"))) + bstack11ll1l1_opy_ (u"ࠪࢁࢂ࠭⋼"))
            if self != None:
                bstack1l1ll11lll_opy_(self, bstack1l1111111l_opy_, bstack11ll1l1_opy_ (u"ࠫ࠱ࠦࠧ⋽").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll11l11l1_opy_(bstack1lll11lllll_opy_):
            item = store.get(bstack11ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⋾"), None)
            if item is not None and bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⋿"), None):
                bstack1l1lllllll_opy_.bstack1l1lllll11_opy_(self, bstack111llll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll1l1_opy_ (u"ࠧࠨ⌀")
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ⌁") + str(e))
    bstack11l11l1l1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1ll1ll1l1l_opy_, stage=STAGE.bstack11l1lll1l1_opy_, bstack11llll111l_opy_=bstack1llll1ll1l_opy_)
def bstack1l1ll111l1_opy_(self, command_executor,
             desired_capabilities=None, bstack1111ll1l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll11llll_opy_
    global bstack1llll1ll1l_opy_
    global bstack1ll111l11l_opy_
    global bstack11l11lll11_opy_
    global bstack1l11111l11_opy_
    global bstack1lll11lll1_opy_
    global bstack1l1l11l1ll_opy_
    global bstack11ll1lllll_opy_
    global bstack111llll1_opy_
    CONFIG[bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⌂")] = str(bstack11l11lll11_opy_) + str(__version__)
    command_executor = bstack1ll11l11_opy_(bstack1l1l11l1ll_opy_, CONFIG)
    logger.debug(bstack11ll1111ll_opy_.format(command_executor))
    proxy = bstack1llll11lll_opy_(CONFIG, proxy)
    bstack1l1l111l_opy_ = 0
    try:
        if bstack1ll111l11l_opy_ is True:
            bstack1l1l111l_opy_ = int(os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⌃")))
    except:
        bstack1l1l111l_opy_ = 0
    bstack1l1ll111l_opy_ = bstack1l1ll1l1l_opy_(CONFIG, bstack1l1l111l_opy_)
    logger.debug(bstack11lll111ll_opy_.format(str(bstack1l1ll111l_opy_)))
    bstack111llll1_opy_ = CONFIG.get(bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⌄"))[bstack1l1l111l_opy_]
    if bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⌅") in CONFIG and CONFIG[bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⌆")]:
        bstack1l111111l1_opy_(bstack1l1ll111l_opy_, bstack11ll1lllll_opy_)
    if bstack1lll11l1_opy_.bstack1ll11l11ll_opy_(CONFIG, bstack1l1l111l_opy_) and bstack1lll11l1_opy_.bstack11l11l1l1l_opy_(bstack1l1ll111l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll11l11l1_opy_(bstack1lll11lllll_opy_):
            bstack1lll11l1_opy_.set_capabilities(bstack1l1ll111l_opy_, CONFIG)
    if desired_capabilities:
        bstack1llll11111_opy_ = bstack1llll11l1_opy_(desired_capabilities)
        bstack1llll11111_opy_[bstack11ll1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⌇")] = bstack1l1ll11l1l_opy_(CONFIG)
        bstack11l111l1l_opy_ = bstack1l1ll1l1l_opy_(bstack1llll11111_opy_)
        if bstack11l111l1l_opy_:
            bstack1l1ll111l_opy_ = update(bstack11l111l1l_opy_, bstack1l1ll111l_opy_)
        desired_capabilities = None
    if options:
        bstack1l1lllll_opy_(options, bstack1l1ll111l_opy_)
    if not options:
        options = bstack1lll1l1ll_opy_(bstack1l1ll111l_opy_)
    if proxy and bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⌈")):
        options.proxy(proxy)
    if options and bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⌉")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1ll111_opy_() < version.parse(bstack11ll1l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⌊")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1ll111l_opy_)
    logger.info(bstack1ll11l1ll1_opy_)
    bstack1l1ll1111_opy_.end(EVENTS.bstack1l1111lll_opy_.value, EVENTS.bstack1l1111lll_opy_.value + bstack11ll1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⌋"),
                               EVENTS.bstack1l1111lll_opy_.value + bstack11ll1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⌌"), True, None)
    if bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⌍")):
        bstack1l11111l11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⌎")):
        bstack1l11111l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1111ll1l_opy_=bstack1111ll1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ⌏")):
        bstack1l11111l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1111ll1l_opy_=bstack1111ll1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l11111l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1111ll1l_opy_=bstack1111ll1l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11lll11ll_opy_ = bstack11ll1l1_opy_ (u"ࠩࠪ⌐")
        if bstack11l1ll111_opy_() >= version.parse(bstack11ll1l1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ⌑")):
            bstack11lll11ll_opy_ = self.caps.get(bstack11ll1l1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⌒"))
        else:
            bstack11lll11ll_opy_ = self.capabilities.get(bstack11ll1l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⌓"))
        if bstack11lll11ll_opy_:
            bstack11llllll1_opy_(bstack11lll11ll_opy_)
            if bstack11l1ll111_opy_() <= version.parse(bstack11ll1l1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭⌔")):
                self.command_executor._url = bstack11ll1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⌕") + bstack1l1l11l1ll_opy_ + bstack11ll1l1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ⌖")
            else:
                self.command_executor._url = bstack11ll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ⌗") + bstack11lll11ll_opy_ + bstack11ll1l1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ⌘")
            logger.debug(bstack11ll1111l1_opy_.format(bstack11lll11ll_opy_))
        else:
            logger.debug(bstack1l1llll1ll_opy_.format(bstack11ll1l1_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ⌙")))
    except Exception as e:
        logger.debug(bstack1l1llll1ll_opy_.format(e))
    bstack11ll11llll_opy_ = self.session_id
    if bstack11ll1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⌚") in bstack11l11lll11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⌛"), None)
        if item:
            bstack1llll1l11ll1_opy_ = getattr(item, bstack11ll1l1_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ⌜"), False)
            if not getattr(item, bstack11ll1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⌝"), None) and bstack1llll1l11ll1_opy_:
                setattr(store[bstack11ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⌞")], bstack11ll1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⌟"), self)
        bstack1llllll1ll_opy_ = getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ⌠"), None)
        if bstack1llllll1ll_opy_ and bstack1llllll1ll_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⌡"), bstack11ll1l1_opy_ (u"࠭ࠧ⌢")) == bstack11ll1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⌣"):
            bstack1l1l11ll11_opy_.bstack1l1l1l1ll1_opy_(self)
    bstack1lll11lll1_opy_.append(self)
    if bstack11ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⌤") in CONFIG and bstack11ll1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⌥") in CONFIG[bstack11ll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⌦")][bstack1l1l111l_opy_]:
        bstack1llll1ll1l_opy_ = CONFIG[bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⌧")][bstack1l1l111l_opy_][bstack11ll1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌨")]
    logger.debug(bstack1ll111lll1_opy_.format(bstack11ll11llll_opy_))
@measure(event_name=EVENTS.bstack1l1l1lll_opy_, stage=STAGE.bstack11l1lll1l1_opy_, bstack11llll111l_opy_=bstack1llll1ll1l_opy_)
def bstack1lllll1l1_opy_(self, url):
    global bstack1111l1l11_opy_
    global CONFIG
    try:
        bstack1ll1111ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l11ll111l_opy_.format(str(err)))
    try:
        bstack1111l1l11_opy_(self, url)
    except Exception as e:
        try:
            bstack11l1l1llll_opy_ = str(e)
            if any(err_msg in bstack11l1l1llll_opy_ for err_msg in bstack1l11l1lll1_opy_):
                bstack1ll1111ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l11ll111l_opy_.format(str(err)))
        raise e
def bstack11l11l11l_opy_(item, when):
    global bstack1lll111l11_opy_
    try:
        bstack1lll111l11_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll111111_opy_(item, call, rep):
    global bstack1ll1llll_opy_
    global bstack1lll11lll1_opy_
    name = bstack11ll1l1_opy_ (u"࠭ࠧ〈")
    try:
        if rep.when == bstack11ll1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ〉"):
            bstack11ll11llll_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11ll1l1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌫"))
            try:
                if (str(skipSessionName).lower() != bstack11ll1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⌬")):
                    name = str(rep.nodeid)
                    bstack11lll11l11_opy_ = bstack1l11llll_opy_(bstack11ll1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⌭"), name, bstack11ll1l1_opy_ (u"ࠫࠬ⌮"), bstack11ll1l1_opy_ (u"ࠬ࠭⌯"), bstack11ll1l1_opy_ (u"࠭ࠧ⌰"), bstack11ll1l1_opy_ (u"ࠧࠨ⌱"))
                    os.environ[bstack11ll1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⌲")] = name
                    for driver in bstack1lll11lll1_opy_:
                        if bstack11ll11llll_opy_ == driver.session_id:
                            driver.execute_script(bstack11lll11l11_opy_)
            except Exception as e:
                logger.debug(bstack11ll1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⌳").format(str(e)))
            try:
                bstack1lll1l11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⌴"):
                    status = bstack11ll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⌵") if rep.outcome.lower() == bstack11ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⌶") else bstack11ll1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌷")
                    reason = bstack11ll1l1_opy_ (u"ࠧࠨ⌸")
                    if status == bstack11ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⌹"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll1l1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ⌺") if status == bstack11ll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⌻") else bstack11ll1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⌼")
                    data = name + bstack11ll1l1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ⌽") if status == bstack11ll1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌾") else name + bstack11ll1l1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ⌿") + reason
                    bstack1l1lll11ll_opy_ = bstack1l11llll_opy_(bstack11ll1l1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⍀"), bstack11ll1l1_opy_ (u"ࠩࠪ⍁"), bstack11ll1l1_opy_ (u"ࠪࠫ⍂"), bstack11ll1l1_opy_ (u"ࠫࠬ⍃"), level, data)
                    for driver in bstack1lll11lll1_opy_:
                        if bstack11ll11llll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1lll11ll_opy_)
            except Exception as e:
                logger.debug(bstack11ll1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⍄").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ⍅").format(str(e)))
    bstack1ll1llll_opy_(item, call, rep)
notset = Notset()
def bstack1l1ll1ll1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1l1ll11l_opy_
    if str(name).lower() == bstack11ll1l1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ⍆"):
        return bstack11ll1l1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ⍇")
    else:
        return bstack1l1l1ll11l_opy_(self, name, default, skip)
def bstack1l1ll1lll_opy_(self):
    global CONFIG
    global bstack111l1lll1_opy_
    try:
        proxy = bstack1l1ll11l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⍈")):
                proxies = bstack1l1l1ll1l1_opy_(proxy, bstack1ll11l11_opy_())
                if len(proxies) > 0:
                    protocol, bstack11l1ll11_opy_ = proxies.popitem()
                    if bstack11ll1l1_opy_ (u"ࠥ࠾࠴࠵ࠢ⍉") in bstack11l1ll11_opy_:
                        return bstack11l1ll11_opy_
                    else:
                        return bstack11ll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⍊") + bstack11l1ll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ⍋").format(str(e)))
    return bstack111l1lll1_opy_(self)
def bstack11l1111111_opy_():
    return (bstack11ll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⍌") in CONFIG or bstack11ll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⍍") in CONFIG) and bstack1ll1ll1l1_opy_() and bstack11l1ll111_opy_() >= version.parse(
        bstack1l1l11111_opy_)
def bstack1l1ll111ll_opy_(self,
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
    global bstack1llll1ll1l_opy_
    global bstack1ll111l11l_opy_
    global bstack11l11lll11_opy_
    CONFIG[bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⍎")] = str(bstack11l11lll11_opy_) + str(__version__)
    bstack1l1l111l_opy_ = 0
    try:
        if bstack1ll111l11l_opy_ is True:
            bstack1l1l111l_opy_ = int(os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⍏")))
    except:
        bstack1l1l111l_opy_ = 0
    CONFIG[bstack11ll1l1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ⍐")] = True
    bstack1l1ll111l_opy_ = bstack1l1ll1l1l_opy_(CONFIG, bstack1l1l111l_opy_)
    logger.debug(bstack11lll111ll_opy_.format(str(bstack1l1ll111l_opy_)))
    if CONFIG.get(bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⍑")):
        bstack1l111111l1_opy_(bstack1l1ll111l_opy_, bstack11ll1lllll_opy_)
    if bstack11ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⍒") in CONFIG and bstack11ll1l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⍓") in CONFIG[bstack11ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⍔")][bstack1l1l111l_opy_]:
        bstack1llll1ll1l_opy_ = CONFIG[bstack11ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⍕")][bstack1l1l111l_opy_][bstack11ll1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⍖")]
    import urllib
    import json
    if bstack11ll1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⍗") in CONFIG and str(CONFIG[bstack11ll1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⍘")]).lower() != bstack11ll1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⍙"):
        bstack1l1111l1ll_opy_ = bstack11l11llll1_opy_()
        bstack1lll11l1l_opy_ = bstack1l1111l1ll_opy_ + urllib.parse.quote(json.dumps(bstack1l1ll111l_opy_))
    else:
        bstack1lll11l1l_opy_ = bstack11ll1l1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ⍚") + urllib.parse.quote(json.dumps(bstack1l1ll111l_opy_))
    browser = self.connect(bstack1lll11l1l_opy_)
    return browser
def bstack111ll11l1_opy_():
    global bstack111lll11l_opy_
    global bstack11l11lll11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11lll1l_opy_
        if not bstack1l1lll11111_opy_():
            global bstack1l11ll1l_opy_
            if not bstack1l11ll1l_opy_:
                from bstack_utils.helper import bstack1lllll1111_opy_, bstack11l1lll111_opy_
                bstack1l11ll1l_opy_ = bstack1lllll1111_opy_()
                bstack11l1lll111_opy_(bstack11l11lll11_opy_)
            BrowserType.connect = bstack1l11lll1l_opy_
            return
        BrowserType.launch = bstack1l1ll111ll_opy_
        bstack111lll11l_opy_ = True
    except Exception as e:
        pass
def bstack1llll1lll11l_opy_():
    global CONFIG
    global bstack1lll1ll111_opy_
    global bstack1l1l11l1ll_opy_
    global bstack11ll1lllll_opy_
    global bstack1ll111l11l_opy_
    global bstack1l111lll1l_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭⍛")))
    bstack1lll1ll111_opy_ = eval(os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ⍜")))
    bstack1l1l11l1ll_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ⍝"))
    bstack1l1lll1lll_opy_(CONFIG, bstack1lll1ll111_opy_)
    bstack1l111lll1l_opy_ = bstack11l1l1l111_opy_.bstack1lll1ll1ll_opy_(CONFIG, bstack1l111lll1l_opy_)
    if cli.bstack1ll1ll111_opy_():
        bstack11l11lll1l_opy_.invoke(bstack1llllll1l1_opy_.CONNECT, bstack1111111ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⍞"), bstack11ll1l1_opy_ (u"ࠫ࠵࠭⍟")))
        cli.bstack1lll11111l1_opy_(cli_context.platform_index)
        cli.bstack1ll1l1lll11_opy_(bstack1ll11l11_opy_(bstack1l1l11l1ll_opy_, CONFIG), cli_context.platform_index, bstack1lll1l1ll_opy_)
        cli.bstack1lll1ll1lll_opy_()
        logger.debug(bstack11ll1l1_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⍠") + str(cli_context.platform_index) + bstack11ll1l1_opy_ (u"ࠨࠢ⍡"))
        return # skip all existing bstack1llll1l11l1l_opy_
    global bstack1l11111l11_opy_
    global bstack11l11l1l1_opy_
    global bstack1ll11111l_opy_
    global bstack1l1lll11_opy_
    global bstack11llllll1l_opy_
    global bstack1ll1l11111_opy_
    global bstack1l1111ll_opy_
    global bstack1111l1l11_opy_
    global bstack111l1lll1_opy_
    global bstack1l1l1ll11l_opy_
    global bstack1lll111l11_opy_
    global bstack1ll1llll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11111l11_opy_ = webdriver.Remote.__init__
        bstack11l11l1l1_opy_ = WebDriver.quit
        bstack1l1111ll_opy_ = WebDriver.close
        bstack1111l1l11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11ll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⍢") in CONFIG or bstack11ll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⍣") in CONFIG) and bstack1ll1ll1l1_opy_():
        if bstack11l1ll111_opy_() < version.parse(bstack1l1l11111_opy_):
            logger.error(bstack11lllll111_opy_.format(bstack11l1ll111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11ll1l1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⍤")) and callable(getattr(RemoteConnection, bstack11ll1l1_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⍥"))):
                    bstack111l1lll1_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack111l1lll1_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11ll1l1l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1l1ll11l_opy_ = Config.getoption
        from _pytest import runner
        bstack1lll111l11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11l1l11l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll1llll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ⍦"))
    bstack11ll1lllll_opy_ = CONFIG.get(bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⍧"), {}).get(bstack11ll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⍨"))
    bstack1ll111l11l_opy_ = True
    bstack1l11ll11l1_opy_(bstack1llll111l1_opy_)
if (bstack11l11l11lll_opy_()):
    bstack1llll1lll11l_opy_()
@bstack111l1llll1_opy_(class_method=False)
def bstack1llll1lll1l1_opy_(hook_name, event, bstack1l111111l11_opy_=None):
    if hook_name not in [bstack11ll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⍩"), bstack11ll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⍪"), bstack11ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⍫"), bstack11ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⍬"), bstack11ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⍭"), bstack11ll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⍮"), bstack11ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⍯"), bstack11ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⍰")]:
        return
    node = store[bstack11ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⍱")]
    if hook_name in [bstack11ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⍲"), bstack11ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⍳")]:
        node = store[bstack11ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ⍴")]
    elif hook_name in [bstack11ll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⍵"), bstack11ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⍶")]:
        node = store[bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ⍷")]
    hook_type = bstack11111l11l1l_opy_(hook_name)
    if event == bstack11ll1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⍸"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_[hook_type], bstack1lll1111l1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l111lll_opy_ = {
            bstack11ll1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⍹"): uuid,
            bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⍺"): bstack1ll1l11l11_opy_(),
            bstack11ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⍻"): bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⍼"),
            bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⍽"): hook_type,
            bstack11ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⍾"): hook_name
        }
        store[bstack11ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⍿")].append(uuid)
        bstack1llll1l1l111_opy_ = node.nodeid
        if hook_type == bstack11ll1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⎀"):
            if not _111l11ll11_opy_.get(bstack1llll1l1l111_opy_, None):
                _111l11ll11_opy_[bstack1llll1l1l111_opy_] = {bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⎁"): []}
            _111l11ll11_opy_[bstack1llll1l1l111_opy_][bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⎂")].append(bstack111l111lll_opy_[bstack11ll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⎃")])
        _111l11ll11_opy_[bstack1llll1l1l111_opy_ + bstack11ll1l1_opy_ (u"࠭࠭ࠨ⎄") + hook_name] = bstack111l111lll_opy_
        bstack1llll1l111ll_opy_(node, bstack111l111lll_opy_, bstack11ll1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⎅"))
    elif event == bstack11ll1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⎆"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1ll111l_opy_[hook_type], bstack1lll1111l1l_opy_.POST, node, None, bstack1l111111l11_opy_)
            return
        bstack111ll11ll1_opy_ = node.nodeid + bstack11ll1l1_opy_ (u"ࠩ࠰ࠫ⎇") + hook_name
        _111l11ll11_opy_[bstack111ll11ll1_opy_][bstack11ll1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⎈")] = bstack1ll1l11l11_opy_()
        bstack1llll11lll1l_opy_(_111l11ll11_opy_[bstack111ll11ll1_opy_][bstack11ll1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎉")])
        bstack1llll1l111ll_opy_(node, _111l11ll11_opy_[bstack111ll11ll1_opy_], bstack11ll1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⎊"), bstack1llll1ll11ll_opy_=bstack1l111111l11_opy_)
def bstack1llll1l111l1_opy_():
    global bstack1llll1l1l11l_opy_
    if bstack1lll111l_opy_():
        bstack1llll1l1l11l_opy_ = bstack11ll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⎋")
    else:
        bstack1llll1l1l11l_opy_ = bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⎌")
@bstack1l1l11ll11_opy_.bstack1lllll11llll_opy_
def bstack1llll1ll111l_opy_():
    bstack1llll1l111l1_opy_()
    if cli.is_running():
        try:
            bstack111ll1lll11_opy_(bstack1llll1lll1l1_opy_)
        except Exception as e:
            logger.debug(bstack11ll1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⎍").format(e))
        return
    if bstack1ll1ll1l1_opy_():
        bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
        bstack11ll1l1_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ⎎")
        if bstack1111ll111_opy_.get_property(bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⎏")):
            if CONFIG.get(bstack11ll1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ⎐")) is not None and int(CONFIG[bstack11ll1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⎑")]) > 1:
                bstack1l1l1l1l1l_opy_(bstack1l1ll1ll1_opy_)
            return
        bstack1l1l1l1l1l_opy_(bstack1l1ll1ll1_opy_)
    try:
        bstack111ll1lll11_opy_(bstack1llll1lll1l1_opy_)
    except Exception as e:
        logger.debug(bstack11ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⎒").format(e))
bstack1llll1ll111l_opy_()