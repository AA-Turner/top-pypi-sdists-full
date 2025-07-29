# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l111111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11lllll1l1_opy_, bstack11111ll11_opy_, update, bstack11ll11lll_opy_,
                                       bstack1ll1llll11_opy_, bstack11ll1ll111_opy_, bstack1l111l1l1l_opy_, bstack1l1lll11_opy_,
                                       bstack1lll1l11l_opy_, bstack111l1l1ll_opy_, bstack11llll11ll_opy_,
                                       bstack1ll1llllll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack111111ll1_opy_)
from browserstack_sdk.bstack11l11l111_opy_ import bstack11lll111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll11l1ll_opy_
from bstack_utils.capture import bstack111lll1l1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11lll11111_opy_, bstack11lll11ll_opy_, bstack11l1lll1l1_opy_, \
    bstack111lllllll_opy_
from bstack_utils.helper import bstack11ll1111ll_opy_, bstack11l111llll1_opy_, bstack111l1111ll_opy_, bstack1lllllll1l_opy_, bstack1l1ll11l11l_opy_, bstack1lll111111_opy_, \
    bstack11l11ll1111_opy_, \
    bstack11l1111l1l1_opy_, bstack111l11lll_opy_, bstack1111l1111_opy_, bstack11l11l1llll_opy_, bstack1llll111ll_opy_, Notset, \
    bstack1l1lllll_opy_, bstack11l1111ll1l_opy_, bstack111lllll111_opy_, Result, bstack11l11l111ll_opy_, bstack11l11ll1ll1_opy_, bstack111l1lll11_opy_, \
    bstack1ll111ll1_opy_, bstack1lll111l11_opy_, bstack11l1111ll_opy_, bstack11l111l1l11_opy_
from bstack_utils.bstack111ll1l11l1_opy_ import bstack111ll1l11ll_opy_
from bstack_utils.messages import bstack11l1ll11l1_opy_, bstack11lll1l1l1_opy_, bstack1lll11l11l_opy_, bstack11l111llll_opy_, bstack1l1l11ll11_opy_, \
    bstack1l111ll1l_opy_, bstack11lll1lll_opy_, bstack111llllll1_opy_, bstack11ll1lll_opy_, bstack11llllll1l_opy_, \
    bstack11l1ll11l_opy_, bstack1l111111ll_opy_, bstack1lll1l1l1l_opy_
from bstack_utils.proxy import bstack1l1ll1l1ll_opy_, bstack111llllll_opy_
from bstack_utils.bstack1l1l1l111_opy_ import bstack11111l11111_opy_, bstack11111l1111l_opy_, bstack111111lll1l_opy_, bstack11111l111l1_opy_, \
    bstack111111llll1_opy_, bstack11111l11l11_opy_, bstack11111l11l1l_opy_, bstack1lll1111l_opy_, bstack11111l11ll1_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1l1lllllll_opy_
from bstack_utils.bstack1l1111l1l1_opy_ import bstack11l1l1l1l_opy_, bstack1l11111l_opy_, bstack11l1l1lll_opy_, \
    bstack1l1lll11ll_opy_, bstack1l1l111l11_opy_
from bstack_utils.bstack111ll1llll_opy_ import bstack111ll111l1_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l11l1l1l1_opy_
import bstack_utils.accessibility as bstack11ll1ll11_opy_
from bstack_utils.bstack111llll11l_opy_ import bstack1l1lll1lll_opy_
from bstack_utils.bstack1l111l111_opy_ import bstack1l111l111_opy_
from bstack_utils.bstack1l11ll11_opy_ import bstack1ll11l11l1_opy_
from browserstack_sdk.__init__ import bstack1l1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l111l_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack11l111ll11_opy_ import bstack11l111ll11_opy_, bstack1l1l1llll_opy_, bstack1l1llllll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111l11l1l_opy_, bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l111ll11_opy_ import bstack11l111ll11_opy_, bstack1l1l1llll_opy_, bstack1l1llllll1_opy_
bstack1lll1111ll_opy_ = None
bstack1111l111_opy_ = None
bstack1l1ll1llll_opy_ = None
bstack1l1llll11l_opy_ = None
bstack111llll11_opy_ = None
bstack1l1l1l11_opy_ = None
bstack1l1ll111l_opy_ = None
bstack11l1ll111_opy_ = None
bstack11lllll11_opy_ = None
bstack11l1l111l_opy_ = None
bstack1111lllll_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack1lllll1ll1_opy_ = None
bstack1l1l1ll1ll_opy_ = bstackl_opy_ (u"ࠨࠩⅹ")
CONFIG = {}
bstack1ll1l1ll11_opy_ = False
bstack11lll11l1l_opy_ = bstackl_opy_ (u"ࠩࠪⅺ")
bstack1lll111lll_opy_ = bstackl_opy_ (u"ࠪࠫⅻ")
bstack11l11l11_opy_ = False
bstack1ll111l1ll_opy_ = []
bstack1ll11ll11l_opy_ = bstack11lll11111_opy_
bstack1llll1ll1l11_opy_ = bstackl_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫⅼ")
bstack11l11111ll_opy_ = {}
bstack11l11lllll_opy_ = None
bstack11ll1lll1_opy_ = False
logger = bstack1ll11l1ll_opy_.get_logger(__name__, bstack1ll11ll11l_opy_)
store = {
    bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩⅽ"): []
}
bstack1llll1ll111l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111llllll_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111l11l1l_opy_(
    test_framework_name=bstack111lllll1_opy_[bstackl_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪⅾ")] if bstack1llll111ll_opy_() else bstack111lllll1_opy_[bstackl_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧⅿ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l11ll1ll_opy_(page, bstack11ll111111_opy_):
    try:
        page.evaluate(bstackl_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤↀ"),
                      bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ↁ") + json.dumps(
                          bstack11ll111111_opy_) + bstackl_opy_ (u"ࠥࢁࢂࠨↂ"))
    except Exception as e:
        print(bstackl_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤↃ"), e)
def bstack1l1l1l1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstackl_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨↄ"), bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫↅ") + json.dumps(
            message) + bstackl_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪↆ") + json.dumps(level) + bstackl_opy_ (u"ࠨࡿࢀࠫↇ"))
    except Exception as e:
        print(bstackl_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧↈ"), e)
def pytest_configure(config):
    global bstack11lll11l1l_opy_
    global CONFIG
    bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
    config.args = bstack1l11l1l1l1_opy_.bstack1llll1ll1ll1_opy_(config.args)
    bstack1l1llll1l1_opy_.bstack1ll11lllll_opy_(bstack11l1111ll_opy_(config.getoption(bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ↉"))))
    try:
        bstack1ll11l1ll_opy_.bstack111l1lll11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11l111ll11_opy_.invoke(bstack1l1l1llll_opy_.CONNECT, bstack1l1llllll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ↊"), bstackl_opy_ (u"ࠬ࠶ࠧ↋")))
        config = json.loads(os.environ.get(bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ↌"), bstackl_opy_ (u"ࠢࡼࡿࠥ↍")))
        cli.bstack1lll11llll1_opy_(bstack1111l1111_opy_(bstack11lll11l1l_opy_, CONFIG), cli_context.platform_index, bstack11ll11lll_opy_)
    if cli.bstack1ll1ll1l1l1_opy_(bstack1lll11l111l_opy_):
        cli.bstack1lll1l1111l_opy_()
        logger.debug(bstackl_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ↎") + str(cli_context.platform_index) + bstackl_opy_ (u"ࠤࠥ↏"))
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.BEFORE_ALL, bstack1lll111l111_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstackl_opy_ (u"ࠥࡻ࡭࡫࡮ࠣ←"), None)
    if cli.is_running() and when == bstackl_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ↑"):
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.LOG_REPORT, bstack1lll111l111_opy_.PRE, item, call)
    outcome = yield
    if when == bstackl_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ→"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstackl_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ↓")))
        if not passed:
            config = json.loads(os.environ.get(bstackl_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ↔"), bstackl_opy_ (u"ࠣࡽࢀࠦ↕")))
            if bstack1ll11l11l1_opy_.bstack1ll11ll1l_opy_(config):
                bstack1111l1l1l11_opy_ = bstack1ll11l11l1_opy_.bstack1ll11l1111_opy_(config)
                if item.execution_count > bstack1111l1l1l11_opy_:
                    print(bstackl_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡲࡦࡶࡵ࡭ࡪࡹ࠺ࠡࠩ↖"), report.nodeid, os.environ.get(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ↗")))
                    bstack1ll11l11l1_opy_.bstack111l1l11l11_opy_(report.nodeid)
            else:
                print(bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠫ↘"), report.nodeid, os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ↙")))
                bstack1ll11l11l1_opy_.bstack111l1l11l11_opy_(report.nodeid)
        else:
            print(bstackl_opy_ (u"࠭ࡔࡦࡵࡷࠤࡵࡧࡳࡴࡧࡧ࠾ࠥ࠭↚"), report.nodeid, os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ↛")))
    if cli.is_running():
        if when == bstackl_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ↜"):
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.BEFORE_EACH, bstack1lll111l111_opy_.POST, item, call, outcome)
        elif when == bstackl_opy_ (u"ࠤࡦࡥࡱࡲࠢ↝"):
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.LOG_REPORT, bstack1lll111l111_opy_.POST, item, call, outcome)
        elif when == bstackl_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ↞"):
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.AFTER_EACH, bstack1lll111l111_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    skipSessionName = item.config.getoption(bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭↟"))
    plugins = item.config.getoption(bstackl_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨ↠"))
    report = outcome.get_result()
    os.environ[bstackl_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ↡")] = report.nodeid
    bstack1llll11ll11l_opy_(item, call, report)
    if bstackl_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧ↢") not in plugins or bstack1llll111ll_opy_():
        return
    summary = []
    driver = getattr(item, bstackl_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤ↣"), None)
    page = getattr(item, bstackl_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣ↤"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll11lll1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll1l1llll_opy_(item, report, summary, skipSessionName)
def bstack1llll11lll1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ↥") and report.skipped:
        bstack11111l11ll1_opy_(report)
    if report.when in [bstackl_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ↦"), bstackl_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ↧")]:
        return
    if not bstack1l1ll11l11l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫ↨")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ↩") + json.dumps(
                    report.nodeid) + bstackl_opy_ (u"ࠨࡿࢀࠫ↪"))
        os.environ[bstackl_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ↫")] = report.nodeid
    except Exception as e:
        summary.append(
            bstackl_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥ↬").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstackl_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ↭")))
    bstack1lll1ll1ll_opy_ = bstackl_opy_ (u"ࠧࠨ↮")
    bstack11111l11ll1_opy_(report)
    if not passed:
        try:
            bstack1lll1ll1ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstackl_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ↯").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1ll1ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstackl_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ↰")))
        bstack1lll1ll1ll_opy_ = bstackl_opy_ (u"ࠣࠤ↱")
        if not passed:
            try:
                bstack1lll1ll1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstackl_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ↲").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1ll1ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ↳")
                    + json.dumps(bstackl_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧ↴"))
                    + bstackl_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ↵")
                )
            else:
                item._driver.execute_script(
                    bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ↶")
                    + json.dumps(str(bstack1lll1ll1ll_opy_))
                    + bstackl_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ↷")
                )
        except Exception as e:
            summary.append(bstackl_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨ↸").format(e))
def bstack1llll1l111l1_opy_(test_name, error_message):
    try:
        bstack1llll11lll11_opy_ = []
        bstack1ll11l11l_opy_ = os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ↹"), bstackl_opy_ (u"ࠪ࠴ࠬ↺"))
        bstack1l111ll11l_opy_ = {bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ↻"): test_name, bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ↼"): error_message, bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ↽"): bstack1ll11l11l_opy_}
        bstack1llll1l1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ↾"))
        if os.path.exists(bstack1llll1l1ll11_opy_):
            with open(bstack1llll1l1ll11_opy_) as f:
                bstack1llll11lll11_opy_ = json.load(f)
        bstack1llll11lll11_opy_.append(bstack1l111ll11l_opy_)
        with open(bstack1llll1l1ll11_opy_, bstackl_opy_ (u"ࠨࡹࠪ↿")) as f:
            json.dump(bstack1llll11lll11_opy_, f)
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ⇀") + str(e))
def bstack1llll1l1llll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstackl_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⇁"), bstackl_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⇂")]:
        return
    if (str(skipSessionName).lower() != bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ⇃")):
        bstack11l11ll1ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstackl_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⇄")))
    bstack1lll1ll1ll_opy_ = bstackl_opy_ (u"ࠢࠣ⇅")
    bstack11111l11ll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll1ll1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstackl_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⇆").format(e)
                )
        try:
            if passed:
                bstack1l1l111l11_opy_(getattr(item, bstackl_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⇇"), None), bstackl_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ⇈"))
            else:
                error_message = bstackl_opy_ (u"ࠫࠬ⇉")
                if bstack1lll1ll1ll_opy_:
                    bstack1l1l1l1l1l_opy_(item._page, str(bstack1lll1ll1ll_opy_), bstackl_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ⇊"))
                    bstack1l1l111l11_opy_(getattr(item, bstackl_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⇋"), None), bstackl_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ⇌"), str(bstack1lll1ll1ll_opy_))
                    error_message = str(bstack1lll1ll1ll_opy_)
                else:
                    bstack1l1l111l11_opy_(getattr(item, bstackl_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⇍"), None), bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⇎"))
                bstack1llll1l111l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstackl_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ⇏").format(e))
def pytest_addoption(parser):
    parser.addoption(bstackl_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ⇐"), default=bstackl_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⇑"), help=bstackl_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⇒"))
    parser.addoption(bstackl_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ⇓"), default=bstackl_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ⇔"), help=bstackl_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ⇕"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstackl_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ⇖"), action=bstackl_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ⇗"), default=bstackl_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ⇘"),
                         help=bstackl_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ⇙"))
def bstack111ll1lll1_opy_(log):
    if not (log[bstackl_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⇚")] and log[bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⇛")].strip()):
        return
    active = bstack111ll11lll_opy_()
    log = {
        bstackl_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⇜"): log[bstackl_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⇝")],
        bstackl_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⇞"): bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"ࠬࡠࠧ⇟"),
        bstackl_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⇠"): log[bstackl_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⇡")],
    }
    if active:
        if active[bstackl_opy_ (u"ࠨࡶࡼࡴࡪ࠭⇢")] == bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⇣"):
            log[bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⇤")] = active[bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⇥")]
        elif active[bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪ⇦")] == bstackl_opy_ (u"࠭ࡴࡦࡵࡷࠫ⇧"):
            log[bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⇨")] = active[bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⇩")]
    bstack1l1lll1lll_opy_.bstack1l1l1l1ll1_opy_([log])
def bstack111ll11lll_opy_():
    if len(store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⇪")]) > 0 and store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⇫")][-1]:
        return {
            bstackl_opy_ (u"ࠫࡹࡿࡰࡦࠩ⇬"): bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⇭"),
            bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⇮"): store[bstackl_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇯")][-1]
        }
    if store.get(bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⇰"), None):
        return {
            bstackl_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⇱"): bstackl_opy_ (u"ࠪࡸࡪࡹࡴࠨ⇲"),
            bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⇳"): store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⇴")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.INIT_TEST, bstack1lll111l111_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.INIT_TEST, bstack1lll111l111_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llll11l1lll_opy_ = True
        bstack111l1l1l1_opy_ = bstack11ll1ll11_opy_.bstack1l111lll_opy_(bstack11l1111l1l1_opy_(item.own_markers))
        if not cli.bstack1ll1ll1l1l1_opy_(bstack1lll11l111l_opy_):
            item._a11y_test_case = bstack111l1l1l1_opy_
            if bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⇵"), None):
                driver = getattr(item, bstackl_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⇶"), None)
                item._a11y_started = bstack11ll1ll11_opy_.bstack1ll1l11111_opy_(driver, bstack111l1l1l1_opy_)
        if not bstack1l1lll1lll_opy_.on() or bstack1llll1ll1l11_opy_ != bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⇷"):
            return
        global current_test_uuid #, bstack111ll11l11_opy_
        bstack111l1lllll_opy_ = {
            bstackl_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⇸"): uuid4().__str__(),
            bstackl_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⇹"): bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"ࠫ࡟࠭⇺")
        }
        current_test_uuid = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠬࡻࡵࡪࡦࠪ⇻")]
        store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⇼")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⇽")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111llllll_opy_[item.nodeid] = {**_1111llllll_opy_[item.nodeid], **bstack111l1lllll_opy_}
        bstack1llll1l11111_opy_(item, _1111llllll_opy_[item.nodeid], bstackl_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⇾"))
    except Exception as err:
        print(bstackl_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫ⇿"), str(err))
def pytest_runtest_setup(item):
    store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ∀")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.BEFORE_EACH, bstack1lll111l111_opy_.PRE, item, bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ∁"))
    if bstack1ll11l11l1_opy_.bstack111l11l1ll1_opy_():
            bstack1llll1l1l111_opy_ = bstackl_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡧࡳࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ∂")
            logger.error(bstack1llll1l1l111_opy_)
            bstack111l1lllll_opy_ = {
                bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ∃"): uuid4().__str__(),
                bstackl_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ∄"): bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"ࠨ࡜ࠪ∅"),
                bstackl_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∆"): bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"ࠪ࡞ࠬ∇"),
                bstackl_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ∈"): bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭∉"),
                bstackl_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭∊"): bstack1llll1l1l111_opy_,
                bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭∋"): [],
                bstackl_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ∌"): []
            }
            bstack1llll1l11111_opy_(item, bstack111l1lllll_opy_, bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ∍"))
            pytest.skip(bstack1llll1l1l111_opy_)
            return # skip all existing bstack1llll1l11l1l_opy_
    global bstack1llll1ll111l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11l1llll_opy_():
        atexit.register(bstack11l1ll1111_opy_)
        if not bstack1llll1ll111l_opy_:
            try:
                bstack1llll1l1111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l111l1l11_opy_():
                    bstack1llll1l1111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1l1111l_opy_:
                    signal.signal(s, bstack1llll11ll1l1_opy_)
                bstack1llll1ll111l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstackl_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦ∎") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l11111_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstackl_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ∏")
    try:
        if not bstack1l1lll1lll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1lllll_opy_ = {
            bstackl_opy_ (u"ࠬࡻࡵࡪࡦࠪ∐"): uuid,
            bstackl_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ∑"): bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"࡛ࠧࠩ−"),
            bstackl_opy_ (u"ࠨࡶࡼࡴࡪ࠭∓"): bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ∔"),
            bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭∕"): bstackl_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ∖"),
            bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ∗"): bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ∘")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstackl_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ∙")] = item
        store[bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ√")] = [uuid]
        if not _1111llllll_opy_.get(item.nodeid, None):
            _1111llllll_opy_[item.nodeid] = {bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ∛"): [], bstackl_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ∜"): []}
        _1111llllll_opy_[item.nodeid][bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ∝")].append(bstack111l1lllll_opy_[bstackl_opy_ (u"ࠬࡻࡵࡪࡦࠪ∞")])
        _1111llllll_opy_[item.nodeid + bstackl_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭∟")] = bstack111l1lllll_opy_
        bstack1llll1l11l11_opy_(item, bstack111l1lllll_opy_, bstackl_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ∠"))
    except Exception as err:
        print(bstackl_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ∡"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.AFTER_EACH, bstack1lll111l111_opy_.PRE, item, bstackl_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ∢"))
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        global bstack11l11111ll_opy_
        bstack1ll11l11l_opy_ = 0
        if bstack11l11l11_opy_ is True:
            bstack1ll11l11l_opy_ = int(os.environ.get(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ∣")))
        if bstack111l1ll1l_opy_.bstack1l11lll11_opy_() == bstackl_opy_ (u"ࠦࡹࡸࡵࡦࠤ∤"):
            if bstack111l1ll1l_opy_.bstack1l1l111111_opy_() == bstackl_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ∥"):
                bstack1llll1ll11l1_opy_ = bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ∦"), None)
                bstack1l1l1lll11_opy_ = bstack1llll1ll11l1_opy_ + bstackl_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥ∧")
                driver = getattr(item, bstackl_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ∨"), None)
                bstack11ll1111l_opy_ = getattr(item, bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ∩"), None)
                bstack1ll1lllll1_opy_ = getattr(item, bstackl_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ∪"), None)
                PercySDK.screenshot(driver, bstack1l1l1lll11_opy_, bstack11ll1111l_opy_=bstack11ll1111l_opy_, bstack1ll1lllll1_opy_=bstack1ll1lllll1_opy_, bstack111l11ll_opy_=bstack1ll11l11l_opy_)
        if not cli.bstack1ll1ll1l1l1_opy_(bstack1lll11l111l_opy_):
            if getattr(item, bstackl_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ∫"), False):
                bstack11lll111l_opy_.bstack11l1ll1l_opy_(getattr(item, bstackl_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭∬"), None), bstack11l11111ll_opy_, logger, item)
        if not bstack1l1lll1lll_opy_.on():
            return
        bstack111l1lllll_opy_ = {
            bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ∭"): uuid4().__str__(),
            bstackl_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ∮"): bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"ࠨ࡜ࠪ∯"),
            bstackl_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ∰"): bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ∱"),
            bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ∲"): bstackl_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ∳"),
            bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ∴"): bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ∵")
        }
        _1111llllll_opy_[item.nodeid + bstackl_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ∶")] = bstack111l1lllll_opy_
        bstack1llll1l11l11_opy_(item, bstack111l1lllll_opy_, bstackl_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ∷"))
    except Exception as err:
        print(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩ∸"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111l111l1_opy_(fixturedef.argname):
        store[bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ∹")] = request.node
    elif bstack111111llll1_opy_(fixturedef.argname):
        store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ∺")] = request.node
    if not bstack1l1lll1lll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.SETUP_FIXTURE, bstack1lll111l111_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.SETUP_FIXTURE, bstack1lll111l111_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.SETUP_FIXTURE, bstack1lll111l111_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.SETUP_FIXTURE, bstack1lll111l111_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        fixture = {
            bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ∻"): fixturedef.argname,
            bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ∼"): bstack11l11ll1111_opy_(outcome),
            bstackl_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ∽"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭∾")]
        if not _1111llllll_opy_.get(current_test_item.nodeid, None):
            _1111llllll_opy_[current_test_item.nodeid] = {bstackl_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ∿"): []}
        _1111llllll_opy_[current_test_item.nodeid][bstackl_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭≀")].append(fixture)
    except Exception as err:
        logger.debug(bstackl_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ≁"), str(err))
if bstack1llll111ll_opy_() and bstack1l1lll1lll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.STEP, bstack1lll111l111_opy_.PRE, request, step)
            return
        try:
            _1111llllll_opy_[request.node.nodeid][bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ≂")].bstack1ll1lll1l_opy_(id(step))
        except Exception as err:
            print(bstackl_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ≃"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.STEP, bstack1lll111l111_opy_.POST, request, step, exception)
            return
        try:
            _1111llllll_opy_[request.node.nodeid][bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ≄")].bstack111ll1l11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstackl_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭≅"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.STEP, bstack1lll111l111_opy_.POST, request, step)
            return
        try:
            bstack111ll1llll_opy_: bstack111ll111l1_opy_ = _1111llllll_opy_[request.node.nodeid][bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭≆")]
            bstack111ll1llll_opy_.bstack111ll1l11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstackl_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ≇"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1ll1l11_opy_
        try:
            if not bstack1l1lll1lll_opy_.on() or bstack1llll1ll1l11_opy_ != bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ≈"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ≉"), None)
            if not _1111llllll_opy_.get(request.node.nodeid, None):
                _1111llllll_opy_[request.node.nodeid] = {}
            bstack111ll1llll_opy_ = bstack111ll111l1_opy_.bstack1lllllll1l1l_opy_(
                scenario, feature, request.node,
                name=bstack11111l11l11_opy_(request.node, scenario),
                started_at=bstack1lll111111_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstackl_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ≊"),
                tags=bstack11111l11l1l_opy_(feature, scenario),
                bstack111lll1lll_opy_=bstack1l1lll1lll_opy_.bstack111ll1111l_opy_(driver) if driver and driver.session_id else {}
            )
            _1111llllll_opy_[request.node.nodeid][bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ≋")] = bstack111ll1llll_opy_
            bstack1llll1l1l11l_opy_(bstack111ll1llll_opy_.uuid)
            bstack1l1lll1lll_opy_.bstack111lll111l_opy_(bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ≌"), bstack111ll1llll_opy_)
        except Exception as err:
            print(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ≍"), str(err))
def bstack1llll11llll1_opy_(bstack111ll1ll11_opy_):
    if bstack111ll1ll11_opy_ in store[bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ≎")]:
        store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ≏")].remove(bstack111ll1ll11_opy_)
def bstack1llll1l1l11l_opy_(test_uuid):
    store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ≐")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1lll1lll_opy_.bstack1lllll1ll11l_opy_
def bstack1llll11ll11l_opy_(item, call, report):
    logger.debug(bstackl_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩ≑"))
    global bstack1llll1ll1l11_opy_
    bstack111lllll11_opy_ = bstack1lll111111_opy_()
    if hasattr(report, bstackl_opy_ (u"ࠨࡵࡷࡳࡵ࠭≒")):
        bstack111lllll11_opy_ = bstack11l11l111ll_opy_(report.stop)
    elif hasattr(report, bstackl_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ≓")):
        bstack111lllll11_opy_ = bstack11l11l111ll_opy_(report.start)
    try:
        if getattr(report, bstackl_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ≔"), bstackl_opy_ (u"ࠫࠬ≕")) == bstackl_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ≖"):
            logger.debug(bstackl_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ≗").format(getattr(report, bstackl_opy_ (u"ࠧࡸࡪࡨࡲࠬ≘"), bstackl_opy_ (u"ࠨࠩ≙")).__str__(), bstack1llll1ll1l11_opy_))
            if bstack1llll1ll1l11_opy_ == bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ≚"):
                _1111llllll_opy_[item.nodeid][bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≛")] = bstack111lllll11_opy_
                bstack1llll1l11111_opy_(item, _1111llllll_opy_[item.nodeid], bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭≜"), report, call)
                store[bstackl_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ≝")] = None
            elif bstack1llll1ll1l11_opy_ == bstackl_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ≞"):
                bstack111ll1llll_opy_ = _1111llllll_opy_[item.nodeid][bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ≟")]
                bstack111ll1llll_opy_.set(hooks=_1111llllll_opy_[item.nodeid].get(bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ≠"), []))
                exception, bstack111ll1l1ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111ll1l1ll_opy_ = [call.excinfo.exconly(), getattr(report, bstackl_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ≡"), bstackl_opy_ (u"ࠪࠫ≢"))]
                bstack111ll1llll_opy_.stop(time=bstack111lllll11_opy_, result=Result(result=getattr(report, bstackl_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ≣"), bstackl_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ≤")), exception=exception, bstack111ll1l1ll_opy_=bstack111ll1l1ll_opy_))
                bstack1l1lll1lll_opy_.bstack111lll111l_opy_(bstackl_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ≥"), _1111llllll_opy_[item.nodeid][bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ≦")])
        elif getattr(report, bstackl_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭≧"), bstackl_opy_ (u"ࠩࠪ≨")) in [bstackl_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ≩"), bstackl_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭≪")]:
            logger.debug(bstackl_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ≫").format(getattr(report, bstackl_opy_ (u"࠭ࡷࡩࡧࡱࠫ≬"), bstackl_opy_ (u"ࠧࠨ≭")).__str__(), bstack1llll1ll1l11_opy_))
            bstack111ll1l1l1_opy_ = item.nodeid + bstackl_opy_ (u"ࠨ࠯ࠪ≮") + getattr(report, bstackl_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ≯"), bstackl_opy_ (u"ࠪࠫ≰"))
            if getattr(report, bstackl_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ≱"), False):
                hook_type = bstackl_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ≲") if getattr(report, bstackl_opy_ (u"࠭ࡷࡩࡧࡱࠫ≳"), bstackl_opy_ (u"ࠧࠨ≴")) == bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ≵") else bstackl_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭≶")
                _1111llllll_opy_[bstack111ll1l1l1_opy_] = {
                    bstackl_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ≷"): uuid4().__str__(),
                    bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ≸"): bstack111lllll11_opy_,
                    bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ≹"): hook_type
                }
            _1111llllll_opy_[bstack111ll1l1l1_opy_][bstackl_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≺")] = bstack111lllll11_opy_
            bstack1llll11llll1_opy_(_1111llllll_opy_[bstack111ll1l1l1_opy_][bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ≻")])
            bstack1llll1l11l11_opy_(item, _1111llllll_opy_[bstack111ll1l1l1_opy_], bstackl_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ≼"), report, call)
            if getattr(report, bstackl_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ≽"), bstackl_opy_ (u"ࠪࠫ≾")) == bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ≿"):
                if getattr(report, bstackl_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⊀"), bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⊁")) == bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⊂"):
                    bstack111l1lllll_opy_ = {
                        bstackl_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊃"): uuid4().__str__(),
                        bstackl_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⊄"): bstack1lll111111_opy_(),
                        bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⊅"): bstack1lll111111_opy_()
                    }
                    _1111llllll_opy_[item.nodeid] = {**_1111llllll_opy_[item.nodeid], **bstack111l1lllll_opy_}
                    bstack1llll1l11111_opy_(item, _1111llllll_opy_[item.nodeid], bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⊆"))
                    bstack1llll1l11111_opy_(item, _1111llllll_opy_[item.nodeid], bstackl_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⊇"), report, call)
    except Exception as err:
        print(bstackl_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ⊈"), str(err))
def bstack1llll1ll11ll_opy_(test, bstack111l1lllll_opy_, result=None, call=None, bstack1l111ll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111ll1llll_opy_ = {
        bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⊉"): bstack111l1lllll_opy_[bstackl_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊊")],
        bstackl_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⊋"): bstackl_opy_ (u"ࠪࡸࡪࡹࡴࠨ⊌"),
        bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⊍"): test.name,
        bstackl_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⊎"): {
            bstackl_opy_ (u"࠭࡬ࡢࡰࡪࠫ⊏"): bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⊐"),
            bstackl_opy_ (u"ࠨࡥࡲࡨࡪ࠭⊑"): inspect.getsource(test.obj)
        },
        bstackl_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⊒"): test.name,
        bstackl_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⊓"): test.name,
        bstackl_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⊔"): bstack1l11l1l1l1_opy_.bstack111l11llll_opy_(test),
        bstackl_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⊕"): file_path,
        bstackl_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⊖"): file_path,
        bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⊗"): bstackl_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⊘"),
        bstackl_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⊙"): file_path,
        bstackl_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⊚"): bstack111l1lllll_opy_[bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⊛")],
        bstackl_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⊜"): bstackl_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⊝"),
        bstackl_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⊞"): {
            bstackl_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⊟"): test.nodeid
        },
        bstackl_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⊠"): bstack11l1111l1l1_opy_(test.own_markers)
    }
    if bstack1l111ll111_opy_ in [bstackl_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⊡"), bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⊢")]:
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠬࡳࡥࡵࡣࠪ⊣")] = {
            bstackl_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⊤"): bstack111l1lllll_opy_.get(bstackl_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⊥"), [])
        }
    if bstack1l111ll111_opy_ == bstackl_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⊦"):
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊧")] = bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⊨")
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⊩")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⊪")]
        bstack111ll1llll_opy_[bstackl_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⊫")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊬")]
    if result:
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⊭")] = result.outcome
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⊮")] = result.duration * 1000
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⊯")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⊰")]
        if result.failed:
            bstack111ll1llll_opy_[bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⊱")] = bstack1l1lll1lll_opy_.bstack111111ll11_opy_(call.excinfo.typename)
            bstack111ll1llll_opy_[bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⊲")] = bstack1l1lll1lll_opy_.bstack1lllll111lll_opy_(call.excinfo, result)
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⊳")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⊴")]
    if outcome:
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊵")] = bstack11l11ll1111_opy_(outcome)
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⊶")] = 0
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⊷")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⊸")]
        if bstack111ll1llll_opy_[bstackl_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⊹")] == bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⊺"):
            bstack111ll1llll_opy_[bstackl_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⊻")] = bstackl_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⊼")  # bstack1llll1l11lll_opy_
            bstack111ll1llll_opy_[bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⊽")] = [{bstackl_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⊾"): [bstackl_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⊿")]}]
        bstack111ll1llll_opy_[bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⋀")] = bstack111l1lllll_opy_[bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⋁")]
    return bstack111ll1llll_opy_
def bstack1llll1ll1111_opy_(test, bstack1111llll1l_opy_, bstack1l111ll111_opy_, result, call, outcome, bstack1llll1l11ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1111llll1l_opy_[bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⋂")]
    hook_name = bstack1111llll1l_opy_[bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⋃")]
    hook_data = {
        bstackl_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⋄"): bstack1111llll1l_opy_[bstackl_opy_ (u"ࠫࡺࡻࡩࡥࠩ⋅")],
        bstackl_opy_ (u"ࠬࡺࡹࡱࡧࠪ⋆"): bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⋇"),
        bstackl_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⋈"): bstackl_opy_ (u"ࠨࡽࢀࠫ⋉").format(bstack11111l1111l_opy_(hook_name)),
        bstackl_opy_ (u"ࠩࡥࡳࡩࡿࠧ⋊"): {
            bstackl_opy_ (u"ࠪࡰࡦࡴࡧࠨ⋋"): bstackl_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⋌"),
            bstackl_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⋍"): None
        },
        bstackl_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⋎"): test.name,
        bstackl_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⋏"): bstack1l11l1l1l1_opy_.bstack111l11llll_opy_(test, hook_name),
        bstackl_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⋐"): file_path,
        bstackl_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⋑"): file_path,
        bstackl_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋒"): bstackl_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⋓"),
        bstackl_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⋔"): file_path,
        bstackl_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⋕"): bstack1111llll1l_opy_[bstackl_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⋖")],
        bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⋗"): bstackl_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ⋘") if bstack1llll1ll1l11_opy_ == bstackl_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⋙") else bstackl_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⋚"),
        bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⋛"): hook_type
    }
    bstack1ll1l1111ll_opy_ = bstack111l1ll11l_opy_(_1111llllll_opy_.get(test.nodeid, None))
    if bstack1ll1l1111ll_opy_:
        hook_data[bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⋜")] = bstack1ll1l1111ll_opy_
    if result:
        hook_data[bstackl_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⋝")] = result.outcome
        hook_data[bstackl_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⋞")] = result.duration * 1000
        hook_data[bstackl_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⋟")] = bstack1111llll1l_opy_[bstackl_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⋠")]
        if result.failed:
            hook_data[bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⋡")] = bstack1l1lll1lll_opy_.bstack111111ll11_opy_(call.excinfo.typename)
            hook_data[bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⋢")] = bstack1l1lll1lll_opy_.bstack1lllll111lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstackl_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⋣")] = bstack11l11ll1111_opy_(outcome)
        hook_data[bstackl_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⋤")] = 100
        hook_data[bstackl_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⋥")] = bstack1111llll1l_opy_[bstackl_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⋦")]
        if hook_data[bstackl_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋧")] == bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⋨"):
            hook_data[bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⋩")] = bstackl_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⋪")  # bstack1llll1l11lll_opy_
            hook_data[bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⋫")] = [{bstackl_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⋬"): [bstackl_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⋭")]}]
    if bstack1llll1l11ll1_opy_:
        hook_data[bstackl_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋮")] = bstack1llll1l11ll1_opy_.result
        hook_data[bstackl_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⋯")] = bstack11l1111ll1l_opy_(bstack1111llll1l_opy_[bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⋰")], bstack1111llll1l_opy_[bstackl_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⋱")])
        hook_data[bstackl_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⋲")] = bstack1111llll1l_opy_[bstackl_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⋳")]
        if hook_data[bstackl_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⋴")] == bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⋵"):
            hook_data[bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⋶")] = bstack1l1lll1lll_opy_.bstack111111ll11_opy_(bstack1llll1l11ll1_opy_.exception_type)
            hook_data[bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⋷")] = [{bstackl_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⋸"): bstack111lllll111_opy_(bstack1llll1l11ll1_opy_.exception)}]
    return hook_data
def bstack1llll1l11111_opy_(test, bstack111l1lllll_opy_, bstack1l111ll111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstackl_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ⋹").format(bstack1l111ll111_opy_))
    bstack111ll1llll_opy_ = bstack1llll1ll11ll_opy_(test, bstack111l1lllll_opy_, result, call, bstack1l111ll111_opy_, outcome)
    driver = getattr(test, bstackl_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⋺"), None)
    if bstack1l111ll111_opy_ == bstackl_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⋻") and driver:
        bstack111ll1llll_opy_[bstackl_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ⋼")] = bstack1l1lll1lll_opy_.bstack111ll1111l_opy_(driver)
    if bstack1l111ll111_opy_ == bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⋽"):
        bstack1l111ll111_opy_ = bstackl_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⋾")
    bstack111l1l1ll1_opy_ = {
        bstackl_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⋿"): bstack1l111ll111_opy_,
        bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⌀"): bstack111ll1llll_opy_
    }
    bstack1l1lll1lll_opy_.bstack1l1lll1l_opy_(bstack111l1l1ll1_opy_)
    if bstack1l111ll111_opy_ == bstackl_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⌁"):
        threading.current_thread().bstackTestMeta = {bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⌂"): bstackl_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⌃")}
    elif bstack1l111ll111_opy_ == bstackl_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⌄"):
        threading.current_thread().bstackTestMeta = {bstackl_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⌅"): getattr(result, bstackl_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⌆"), bstackl_opy_ (u"ࠧࠨ⌇"))}
def bstack1llll1l11l11_opy_(test, bstack111l1lllll_opy_, bstack1l111ll111_opy_, result=None, call=None, outcome=None, bstack1llll1l11ll1_opy_=None):
    logger.debug(bstackl_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⌈").format(bstack1l111ll111_opy_))
    hook_data = bstack1llll1ll1111_opy_(test, bstack111l1lllll_opy_, bstack1l111ll111_opy_, result, call, outcome, bstack1llll1l11ll1_opy_)
    bstack111l1l1ll1_opy_ = {
        bstackl_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⌉"): bstack1l111ll111_opy_,
        bstackl_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ⌊"): hook_data
    }
    bstack1l1lll1lll_opy_.bstack1l1lll1l_opy_(bstack111l1l1ll1_opy_)
def bstack111l1ll11l_opy_(bstack111l1lllll_opy_):
    if not bstack111l1lllll_opy_:
        return None
    if bstack111l1lllll_opy_.get(bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⌋"), None):
        return getattr(bstack111l1lllll_opy_[bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⌌")], bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⌍"), None)
    return bstack111l1lllll_opy_.get(bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⌎"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.LOG, bstack1lll111l111_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_.LOG, bstack1lll111l111_opy_.POST, request, caplog)
        return # skip all existing bstack1llll1l11l1l_opy_
    try:
        if not bstack1l1lll1lll_opy_.on():
            return
        places = [bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⌏"), bstackl_opy_ (u"ࠩࡦࡥࡱࡲࠧ⌐"), bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⌑")]
        logs = []
        for bstack1llll11ll1ll_opy_ in places:
            records = caplog.get_records(bstack1llll11ll1ll_opy_)
            bstack1llll1l1l1l1_opy_ = bstackl_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⌒") if bstack1llll11ll1ll_opy_ == bstackl_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⌓") else bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⌔")
            bstack1llll1l1lll1_opy_ = request.node.nodeid + (bstackl_opy_ (u"ࠧࠨ⌕") if bstack1llll11ll1ll_opy_ == bstackl_opy_ (u"ࠨࡥࡤࡰࡱ࠭⌖") else bstackl_opy_ (u"ࠩ࠰ࠫ⌗") + bstack1llll11ll1ll_opy_)
            test_uuid = bstack111l1ll11l_opy_(_1111llllll_opy_.get(bstack1llll1l1lll1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l11ll1ll1_opy_(record.message):
                    continue
                logs.append({
                    bstackl_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⌘"): bstack11l111llll1_opy_(record.created).isoformat() + bstackl_opy_ (u"ࠫ࡟࠭⌙"),
                    bstackl_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⌚"): record.levelname,
                    bstackl_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⌛"): record.message,
                    bstack1llll1l1l1l1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1lll1lll_opy_.bstack1l1l1l1ll1_opy_(logs)
    except Exception as err:
        print(bstackl_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ⌜"), str(err))
def bstack1111l11ll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11ll1lll1_opy_
    bstack1llll1111_opy_ = bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ⌝"), None) and bstack11ll1111ll_opy_(
            threading.current_thread(), bstackl_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⌞"), None)
    bstack1l1l11111l_opy_ = getattr(driver, bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⌟"), None) != None and getattr(driver, bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⌠"), None) == True
    if sequence == bstackl_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⌡") and driver != None:
      if not bstack11ll1lll1_opy_ and bstack1l1ll11l11l_opy_() and bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⌢") in CONFIG and CONFIG[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⌣")] == True and bstack1l111l111_opy_.bstack1ll1111l1_opy_(driver_command) and (bstack1l1l11111l_opy_ or bstack1llll1111_opy_) and not bstack111111ll1_opy_(args):
        try:
          bstack11ll1lll1_opy_ = True
          logger.debug(bstackl_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ⌤").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstackl_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ⌥").format(str(err)))
        bstack11ll1lll1_opy_ = False
    if sequence == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⌦"):
        if driver_command == bstackl_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ⌧"):
            bstack1l1lll1lll_opy_.bstack111ll11l1_opy_({
                bstackl_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⌨"): response[bstackl_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ〈")],
                bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ〉"): store[bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⌫")]
            })
def bstack11l1ll1111_opy_():
    global bstack1ll111l1ll_opy_
    bstack1ll11l1ll_opy_.bstack1l11llll1l_opy_()
    logging.shutdown()
    bstack1l1lll1lll_opy_.bstack111l11lll1_opy_()
    for driver in bstack1ll111l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll11ll1l1_opy_(*args):
    global bstack1ll111l1ll_opy_
    bstack1l1lll1lll_opy_.bstack111l11lll1_opy_()
    for driver in bstack1ll111l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.bstack1l1111ll1_opy_, bstack11111l11_opy_=bstack11l11lllll_opy_)
def bstack11ll11l1l1_opy_(self, *args, **kwargs):
    bstack11ll1l111l_opy_ = bstack1lll1111ll_opy_(self, *args, **kwargs)
    bstack1ll1l11l1_opy_ = getattr(threading.current_thread(), bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⌬"), None)
    if bstack1ll1l11l1_opy_ and bstack1ll1l11l1_opy_.get(bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⌭"), bstackl_opy_ (u"ࠫࠬ⌮")) == bstackl_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⌯"):
        bstack1l1lll1lll_opy_.bstack1l1ll11l11_opy_(self)
    return bstack11ll1l111l_opy_
@measure(event_name=EVENTS.bstack1lll1ll1_opy_, stage=STAGE.bstack11llll1l1_opy_, bstack11111l11_opy_=bstack11l11lllll_opy_)
def bstack11ll1111l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
    if bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⌰")):
        return
    bstack1l1llll1l1_opy_.bstack1l1ll1lll1_opy_(bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⌱"), True)
    global bstack1l1l1ll1ll_opy_
    global bstack1l111111l1_opy_
    bstack1l1l1ll1ll_opy_ = framework_name
    logger.info(bstack1l111111ll_opy_.format(bstack1l1l1ll1ll_opy_.split(bstackl_opy_ (u"ࠨ࠯ࠪ⌲"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll11l11l_opy_():
            Service.start = bstack1l111l1l1l_opy_
            Service.stop = bstack1l1lll11_opy_
            webdriver.Remote.get = bstack1l111l11l1_opy_
            webdriver.Remote.__init__ = bstack1lll111l_opy_
            if not isinstance(os.getenv(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ⌳")), str):
                return
            WebDriver.quit = bstack11l1111ll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1lll1lll_opy_.on():
            webdriver.Remote.__init__ = bstack11ll11l1l1_opy_
        bstack1l111111l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstackl_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⌴")):
        bstack1l111111l1_opy_ = eval(os.environ.get(bstackl_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⌵")))
    if not bstack1l111111l1_opy_:
        bstack111l1l1ll_opy_(bstackl_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ⌶"), bstack11l1ll11l_opy_)
    if bstack1111l11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstackl_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⌷")) and callable(getattr(RemoteConnection, bstackl_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⌸"))):
                RemoteConnection._get_proxy_url = bstack1llllll1l_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1llllll1l_opy_
        except Exception as e:
            logger.error(bstack1l111ll1l_opy_.format(str(e)))
    if bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⌹") in str(framework_name).lower():
        if not bstack1l1ll11l11l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1llll11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1ll111_opy_
            Config.getoption = bstack111111l11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll11l1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll11ll11_opy_, stage=STAGE.bstack1l1111ll1_opy_, bstack11111l11_opy_=bstack11l11lllll_opy_)
def bstack11l1111ll1_opy_(self):
    global bstack1l1l1ll1ll_opy_
    global bstack11ll11l111_opy_
    global bstack1111l111_opy_
    try:
        if bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⌺") in bstack1l1l1ll1ll_opy_ and self.session_id != None and bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ⌻"), bstackl_opy_ (u"ࠫࠬ⌼")) != bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⌽"):
            bstack1ll1l11lll_opy_ = bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌿")
            bstack1lll111l11_opy_(logger, True)
            if os.environ.get(bstackl_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⍀"), None):
                self.execute_script(
                    bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ⍁") + json.dumps(
                        os.environ.get(bstackl_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⍂"))) + bstackl_opy_ (u"ࠫࢂࢃࠧ⍃"))
            if self != None:
                bstack1l1lll11ll_opy_(self, bstack1ll1l11lll_opy_, bstackl_opy_ (u"ࠬ࠲ࠠࠨ⍄").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll1ll1l1l1_opy_(bstack1lll11l111l_opy_):
            item = store.get(bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⍅"), None)
            if item is not None and bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⍆"), None):
                bstack11lll111l_opy_.bstack11l1ll1l_opy_(self, bstack11l11111ll_opy_, logger, item)
        threading.current_thread().testStatus = bstackl_opy_ (u"ࠨࠩ⍇")
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ⍈") + str(e))
    bstack1111l111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l11lll1_opy_, stage=STAGE.bstack1l1111ll1_opy_, bstack11111l11_opy_=bstack11l11lllll_opy_)
def bstack1lll111l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll11l111_opy_
    global bstack11l11lllll_opy_
    global bstack11l11l11_opy_
    global bstack1l1l1ll1ll_opy_
    global bstack1lll1111ll_opy_
    global bstack1ll111l1ll_opy_
    global bstack11lll11l1l_opy_
    global bstack1lll111lll_opy_
    global bstack11l11111ll_opy_
    CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⍉")] = str(bstack1l1l1ll1ll_opy_) + str(__version__)
    command_executor = bstack1111l1111_opy_(bstack11lll11l1l_opy_, CONFIG)
    logger.debug(bstack11l111llll_opy_.format(command_executor))
    proxy = bstack1ll1llllll_opy_(CONFIG, proxy)
    bstack1ll11l11l_opy_ = 0
    try:
        if bstack11l11l11_opy_ is True:
            bstack1ll11l11l_opy_ = int(os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⍊")))
    except:
        bstack1ll11l11l_opy_ = 0
    bstack1llllllll1_opy_ = bstack11lllll1l1_opy_(CONFIG, bstack1ll11l11l_opy_)
    logger.debug(bstack111llllll1_opy_.format(str(bstack1llllllll1_opy_)))
    bstack11l11111ll_opy_ = CONFIG.get(bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⍋"))[bstack1ll11l11l_opy_]
    if bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⍌") in CONFIG and CONFIG[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⍍")]:
        bstack11l1l1lll_opy_(bstack1llllllll1_opy_, bstack1lll111lll_opy_)
    if bstack11ll1ll11_opy_.bstack1l1111l1l_opy_(CONFIG, bstack1ll11l11l_opy_) and bstack11ll1ll11_opy_.bstack1lll1l111l_opy_(bstack1llllllll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll1ll1l1l1_opy_(bstack1lll11l111l_opy_):
            bstack11ll1ll11_opy_.set_capabilities(bstack1llllllll1_opy_, CONFIG)
    if desired_capabilities:
        bstack11l111l11_opy_ = bstack11111ll11_opy_(desired_capabilities)
        bstack11l111l11_opy_[bstackl_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⍎")] = bstack1l1lllll_opy_(CONFIG)
        bstack1l11l111ll_opy_ = bstack11lllll1l1_opy_(bstack11l111l11_opy_)
        if bstack1l11l111ll_opy_:
            bstack1llllllll1_opy_ = update(bstack1l11l111ll_opy_, bstack1llllllll1_opy_)
        desired_capabilities = None
    if options:
        bstack1lll1l11l_opy_(options, bstack1llllllll1_opy_)
    if not options:
        options = bstack11ll11lll_opy_(bstack1llllllll1_opy_)
    if proxy and bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⍏")):
        options.proxy(proxy)
    if options and bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⍐")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l11lll_opy_() < version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⍑")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1llllllll1_opy_)
    logger.info(bstack1lll11l11l_opy_)
    bstack11l111111_opy_.end(EVENTS.bstack1lll1ll1_opy_.value, EVENTS.bstack1lll1ll1_opy_.value + bstackl_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⍒"),
                               EVENTS.bstack1lll1ll1_opy_.value + bstackl_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⍓"), True, None)
    try:
        if bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⍔")):
            bstack1lll1111ll_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⍕")):
            bstack1lll1111ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ⍖")):
            bstack1lll1111ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1lll1111ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11lll1llll_opy_:
        logger.error(bstack1lll1l1l1l_opy_.format(bstackl_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩ⍗"), str(bstack11lll1llll_opy_)))
        raise bstack11lll1llll_opy_
    try:
        bstack1l11l111_opy_ = bstackl_opy_ (u"ࠫࠬ⍘")
        if bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭⍙")):
            bstack1l11l111_opy_ = self.caps.get(bstackl_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⍚"))
        else:
            bstack1l11l111_opy_ = self.capabilities.get(bstackl_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⍛"))
        if bstack1l11l111_opy_:
            bstack1ll111ll1_opy_(bstack1l11l111_opy_)
            if bstack111l11lll_opy_() <= version.parse(bstackl_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ⍜")):
                self.command_executor._url = bstackl_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⍝") + bstack11lll11l1l_opy_ + bstackl_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ⍞")
            else:
                self.command_executor._url = bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ⍟") + bstack1l11l111_opy_ + bstackl_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ⍠")
            logger.debug(bstack11lll1l1l1_opy_.format(bstack1l11l111_opy_))
        else:
            logger.debug(bstack11l1ll11l1_opy_.format(bstackl_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ⍡")))
    except Exception as e:
        logger.debug(bstack11l1ll11l1_opy_.format(e))
    bstack11ll11l111_opy_ = self.session_id
    if bstackl_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⍢") in bstack1l1l1ll1ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstackl_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⍣"), None)
        if item:
            bstack1llll1l111ll_opy_ = getattr(item, bstackl_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ⍤"), False)
            if not getattr(item, bstackl_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⍥"), None) and bstack1llll1l111ll_opy_:
                setattr(store[bstackl_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⍦")], bstackl_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⍧"), self)
        bstack1ll1l11l1_opy_ = getattr(threading.current_thread(), bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⍨"), None)
        if bstack1ll1l11l1_opy_ and bstack1ll1l11l1_opy_.get(bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⍩"), bstackl_opy_ (u"ࠨࠩ⍪")) == bstackl_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⍫"):
            bstack1l1lll1lll_opy_.bstack1l1ll11l11_opy_(self)
    bstack1ll111l1ll_opy_.append(self)
    if bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⍬") in CONFIG and bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⍭") in CONFIG[bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⍮")][bstack1ll11l11l_opy_]:
        bstack11l11lllll_opy_ = CONFIG[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⍯")][bstack1ll11l11l_opy_][bstackl_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⍰")]
    logger.debug(bstack11llllll1l_opy_.format(bstack11ll11l111_opy_))
@measure(event_name=EVENTS.bstack11l1l1ll1_opy_, stage=STAGE.bstack1l1111ll1_opy_, bstack11111l11_opy_=bstack11l11lllll_opy_)
def bstack1l111l11l1_opy_(self, url):
    global bstack11lllll11_opy_
    global CONFIG
    try:
        bstack1l11111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll1lll_opy_.format(str(err)))
    try:
        bstack11lllll11_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll1ll1ll_opy_ = str(e)
            if any(err_msg in bstack1ll1ll1ll_opy_ for err_msg in bstack11l1lll1l1_opy_):
                bstack1l11111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll1lll_opy_.format(str(err)))
        raise e
def bstack1lll1111l1_opy_(item, when):
    global bstack1l1ll1l11_opy_
    try:
        bstack1l1ll1l11_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll11l1_opy_(item, call, rep):
    global bstack1lllll1ll1_opy_
    global bstack1ll111l1ll_opy_
    name = bstackl_opy_ (u"ࠨࠩ⍱")
    try:
        if rep.when == bstackl_opy_ (u"ࠩࡦࡥࡱࡲࠧ⍲"):
            bstack11ll11l111_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstackl_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⍳"))
            try:
                if (str(skipSessionName).lower() != bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩ⍴")):
                    name = str(rep.nodeid)
                    bstack11l11111_opy_ = bstack11l1l1l1l_opy_(bstackl_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⍵"), name, bstackl_opy_ (u"࠭ࠧ⍶"), bstackl_opy_ (u"ࠧࠨ⍷"), bstackl_opy_ (u"ࠨࠩ⍸"), bstackl_opy_ (u"ࠩࠪ⍹"))
                    os.environ[bstackl_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⍺")] = name
                    for driver in bstack1ll111l1ll_opy_:
                        if bstack11ll11l111_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11111_opy_)
            except Exception as e:
                logger.debug(bstackl_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⍻").format(str(e)))
            try:
                bstack1lll1111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstackl_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⍼"):
                    status = bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⍽") if rep.outcome.lower() == bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⍾") else bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⍿")
                    reason = bstackl_opy_ (u"ࠩࠪ⎀")
                    if status == bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⎁"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstackl_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ⎂") if status == bstackl_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⎃") else bstackl_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⎄")
                    data = name + bstackl_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ⎅") if status == bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⎆") else name + bstackl_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ⎇") + reason
                    bstack111111l1l_opy_ = bstack11l1l1l1l_opy_(bstackl_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⎈"), bstackl_opy_ (u"ࠫࠬ⎉"), bstackl_opy_ (u"ࠬ࠭⎊"), bstackl_opy_ (u"࠭ࠧ⎋"), level, data)
                    for driver in bstack1ll111l1ll_opy_:
                        if bstack11ll11l111_opy_ == driver.session_id:
                            driver.execute_script(bstack111111l1l_opy_)
            except Exception as e:
                logger.debug(bstackl_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⎌").format(str(e)))
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ⎍").format(str(e)))
    bstack1lllll1ll1_opy_(item, call, rep)
notset = Notset()
def bstack111111l11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1111lllll_opy_
    if str(name).lower() == bstackl_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ⎎"):
        return bstackl_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ⎏")
    else:
        return bstack1111lllll_opy_(self, name, default, skip)
def bstack1llllll1l_opy_(self):
    global CONFIG
    global bstack1l1ll111l_opy_
    try:
        proxy = bstack1l1ll1l1ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstackl_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ⎐")):
                proxies = bstack111llllll_opy_(proxy, bstack1111l1111_opy_())
                if len(proxies) > 0:
                    protocol, bstack11llll11_opy_ = proxies.popitem()
                    if bstackl_opy_ (u"ࠧࡀ࠯࠰ࠤ⎑") in bstack11llll11_opy_:
                        return bstack11llll11_opy_
                    else:
                        return bstackl_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⎒") + bstack11llll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ⎓").format(str(e)))
    return bstack1l1ll111l_opy_(self)
def bstack1111l11l_opy_():
    return (bstackl_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⎔") in CONFIG or bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⎕") in CONFIG) and bstack1lllllll1l_opy_() and bstack111l11lll_opy_() >= version.parse(
        bstack11lll11ll_opy_)
def bstack1l111ll1ll_opy_(self,
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
    global bstack11l11lllll_opy_
    global bstack11l11l11_opy_
    global bstack1l1l1ll1ll_opy_
    CONFIG[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⎖")] = str(bstack1l1l1ll1ll_opy_) + str(__version__)
    bstack1ll11l11l_opy_ = 0
    try:
        if bstack11l11l11_opy_ is True:
            bstack1ll11l11l_opy_ = int(os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⎗")))
    except:
        bstack1ll11l11l_opy_ = 0
    CONFIG[bstackl_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ⎘")] = True
    bstack1llllllll1_opy_ = bstack11lllll1l1_opy_(CONFIG, bstack1ll11l11l_opy_)
    logger.debug(bstack111llllll1_opy_.format(str(bstack1llllllll1_opy_)))
    if CONFIG.get(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⎙")):
        bstack11l1l1lll_opy_(bstack1llllllll1_opy_, bstack1lll111lll_opy_)
    if bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⎚") in CONFIG and bstackl_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⎛") in CONFIG[bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⎜")][bstack1ll11l11l_opy_]:
        bstack11l11lllll_opy_ = CONFIG[bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⎝")][bstack1ll11l11l_opy_][bstackl_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⎞")]
    import urllib
    import json
    if bstackl_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⎟") in CONFIG and str(CONFIG[bstackl_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⎠")]).lower() != bstackl_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭⎡"):
        bstack1llll111l1_opy_ = bstack1l1111l1ll_opy_()
        bstack1llll1l11l_opy_ = bstack1llll111l1_opy_ + urllib.parse.quote(json.dumps(bstack1llllllll1_opy_))
    else:
        bstack1llll1l11l_opy_ = bstackl_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ⎢") + urllib.parse.quote(json.dumps(bstack1llllllll1_opy_))
    browser = self.connect(bstack1llll1l11l_opy_)
    return browser
def bstack1l1lll1ll1_opy_():
    global bstack1l111111l1_opy_
    global bstack1l1l1ll1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lllll1111_opy_
        if not bstack1l1ll11l11l_opy_():
            global bstack11l1111l1_opy_
            if not bstack11l1111l1_opy_:
                from bstack_utils.helper import bstack1lll11ll1l_opy_, bstack1111ll111_opy_
                bstack11l1111l1_opy_ = bstack1lll11ll1l_opy_()
                bstack1111ll111_opy_(bstack1l1l1ll1ll_opy_)
            BrowserType.connect = bstack1lllll1111_opy_
            return
        BrowserType.launch = bstack1l111ll1ll_opy_
        bstack1l111111l1_opy_ = True
    except Exception as e:
        pass
def bstack1llll1l1ll1l_opy_():
    global CONFIG
    global bstack1ll1l1ll11_opy_
    global bstack11lll11l1l_opy_
    global bstack1lll111lll_opy_
    global bstack11l11l11_opy_
    global bstack1ll11ll11l_opy_
    CONFIG = json.loads(os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ⎣")))
    bstack1ll1l1ll11_opy_ = eval(os.environ.get(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⎤")))
    bstack11lll11l1l_opy_ = os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ⎥"))
    bstack11llll11ll_opy_(CONFIG, bstack1ll1l1ll11_opy_)
    bstack1ll11ll11l_opy_ = bstack1ll11l1ll_opy_.bstack1111l11l1_opy_(CONFIG, bstack1ll11ll11l_opy_)
    if cli.bstack11l11llll1_opy_():
        bstack11l111ll11_opy_.invoke(bstack1l1l1llll_opy_.CONNECT, bstack1l1llllll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⎦"), bstackl_opy_ (u"࠭࠰ࠨ⎧")))
        cli.bstack1ll1ll11lll_opy_(cli_context.platform_index)
        cli.bstack1lll11llll1_opy_(bstack1111l1111_opy_(bstack11lll11l1l_opy_, CONFIG), cli_context.platform_index, bstack11ll11lll_opy_)
        cli.bstack1lll1l1111l_opy_()
        logger.debug(bstackl_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⎨") + str(cli_context.platform_index) + bstackl_opy_ (u"ࠣࠤ⎩"))
        return # skip all existing bstack1llll1l11l1l_opy_
    global bstack1lll1111ll_opy_
    global bstack1111l111_opy_
    global bstack1l1ll1llll_opy_
    global bstack1l1llll11l_opy_
    global bstack111llll11_opy_
    global bstack1l1l1l11_opy_
    global bstack11l1ll111_opy_
    global bstack11lllll11_opy_
    global bstack1l1ll111l_opy_
    global bstack1111lllll_opy_
    global bstack1l1ll1l11_opy_
    global bstack1lllll1ll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll1111ll_opy_ = webdriver.Remote.__init__
        bstack1111l111_opy_ = WebDriver.quit
        bstack11l1ll111_opy_ = WebDriver.close
        bstack11lllll11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstackl_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⎪") in CONFIG or bstackl_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⎫") in CONFIG) and bstack1lllllll1l_opy_():
        if bstack111l11lll_opy_() < version.parse(bstack11lll11ll_opy_):
            logger.error(bstack11lll1lll_opy_.format(bstack111l11lll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstackl_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⎬")) and callable(getattr(RemoteConnection, bstackl_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⎭"))):
                    bstack1l1ll111l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1ll111l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l111ll1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1111lllll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1ll1l11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l11ll11_opy_)
    try:
        from pytest_bdd import reporting
        bstack1lllll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstackl_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ⎮"))
    bstack1lll111lll_opy_ = CONFIG.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⎯"), {}).get(bstackl_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⎰"))
    bstack11l11l11_opy_ = True
    bstack11ll1111l1_opy_(bstack111lllllll_opy_)
if (bstack11l11l1llll_opy_()):
    bstack1llll1l1ll1l_opy_()
@bstack111l1lll11_opy_(class_method=False)
def bstack1llll11lllll_opy_(hook_name, event, bstack11llllll1ll_opy_=None):
    if hook_name not in [bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⎱"), bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⎲"), bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⎳"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⎴"), bstackl_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⎵"), bstackl_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⎶"), bstackl_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⎷"), bstackl_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ⎸")]:
        return
    node = store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⎹")]
    if hook_name in [bstackl_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⎺"), bstackl_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⎻")]:
        node = store[bstackl_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ⎼")]
    elif hook_name in [bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⎽"), bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⎾")]:
        node = store[bstackl_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⎿")]
    hook_type = bstack111111lll1l_opy_(hook_name)
    if event == bstackl_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⏀"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_[hook_type], bstack1lll111l111_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1111llll1l_opy_ = {
            bstackl_opy_ (u"ࠫࡺࡻࡩࡥࠩ⏁"): uuid,
            bstackl_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⏂"): bstack1lll111111_opy_(),
            bstackl_opy_ (u"࠭ࡴࡺࡲࡨࠫ⏃"): bstackl_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⏄"),
            bstackl_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⏅"): hook_type,
            bstackl_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⏆"): hook_name
        }
        store[bstackl_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⏇")].append(uuid)
        bstack1llll11ll111_opy_ = node.nodeid
        if hook_type == bstackl_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⏈"):
            if not _1111llllll_opy_.get(bstack1llll11ll111_opy_, None):
                _1111llllll_opy_[bstack1llll11ll111_opy_] = {bstackl_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⏉"): []}
            _1111llllll_opy_[bstack1llll11ll111_opy_][bstackl_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⏊")].append(bstack1111llll1l_opy_[bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⏋")])
        _1111llllll_opy_[bstack1llll11ll111_opy_ + bstackl_opy_ (u"ࠨ࠯ࠪ⏌") + hook_name] = bstack1111llll1l_opy_
        bstack1llll1l11l11_opy_(node, bstack1111llll1l_opy_, bstackl_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⏍"))
    elif event == bstackl_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⏎"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l11l1l_opy_[hook_type], bstack1lll111l111_opy_.POST, node, None, bstack11llllll1ll_opy_)
            return
        bstack111ll1l1l1_opy_ = node.nodeid + bstackl_opy_ (u"ࠫ࠲࠭⏏") + hook_name
        _1111llllll_opy_[bstack111ll1l1l1_opy_][bstackl_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⏐")] = bstack1lll111111_opy_()
        bstack1llll11llll1_opy_(_1111llllll_opy_[bstack111ll1l1l1_opy_][bstackl_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⏑")])
        bstack1llll1l11l11_opy_(node, _1111llllll_opy_[bstack111ll1l1l1_opy_], bstackl_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⏒"), bstack1llll1l11ll1_opy_=bstack11llllll1ll_opy_)
def bstack1llll11l1ll1_opy_():
    global bstack1llll1ll1l11_opy_
    if bstack1llll111ll_opy_():
        bstack1llll1ll1l11_opy_ = bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⏓")
    else:
        bstack1llll1ll1l11_opy_ = bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⏔")
@bstack1l1lll1lll_opy_.bstack1lllll1ll11l_opy_
def bstack1llll1l1l1ll_opy_():
    bstack1llll11l1ll1_opy_()
    if cli.is_running():
        try:
            bstack111ll1l11ll_opy_(bstack1llll11lllll_opy_)
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⏕").format(e))
        return
    if bstack1lllllll1l_opy_():
        bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
        bstackl_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ⏖")
        if bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⏗")):
            if CONFIG.get(bstackl_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⏘")) is not None and int(CONFIG[bstackl_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⏙")]) > 1:
                bstack1l1lllllll_opy_(bstack1111l11ll_opy_)
            return
        bstack1l1lllllll_opy_(bstack1111l11ll_opy_)
    try:
        bstack111ll1l11ll_opy_(bstack1llll11lllll_opy_)
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⏚").format(e))
bstack1llll1l1l1ll_opy_()