# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1ll11ll1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11l11l1_opy_, bstack1l1l1l1111_opy_, update, bstack1ll11111l_opy_,
                                       bstack1ll1l11l_opy_, bstack11ll1ll1l1_opy_, bstack11111l111_opy_, bstack11lllll1ll_opy_,
                                       bstack1ll1l1l11_opy_, bstack1lll11l1l1_opy_, bstack11l11l111l_opy_,
                                       bstack11l1l1111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111l11ll_opy_)
from browserstack_sdk.bstack1l1ll11ll1_opy_ import bstack1l111l1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1111l1ll1_opy_
from bstack_utils.capture import bstack111ll1lll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11ll11ll_opy_, bstack1lll111ll_opy_, bstack1ll1ll11ll_opy_, \
    bstack11l11l1lll_opy_
from bstack_utils.helper import bstack111ll1lll_opy_, bstack11l1111llll_opy_, bstack1111llll11_opy_, bstack1111llll1_opy_, bstack1l1ll111ll1_opy_, bstack1l11l11ll_opy_, \
    bstack11l11lll1ll_opy_, \
    bstack11l11l1111l_opy_, bstack1lll1ll1_opy_, bstack11ll11l111_opy_, bstack11l1l11l1l1_opy_, bstack111ll11l_opy_, Notset, \
    bstack1llll11l1l_opy_, bstack11l1l11l1ll_opy_, bstack11l1l111ll1_opy_, Result, bstack11l1l11ll11_opy_, bstack11l111llll1_opy_, bstack111l1lll11_opy_, \
    bstack1lll111lll_opy_, bstack1lll1l1l1_opy_, bstack1l111ll1l_opy_, bstack11l1111l1l1_opy_
from bstack_utils.bstack111lll1ll1l_opy_ import bstack111lll11l11_opy_
from bstack_utils.messages import bstack111l1ll11_opy_, bstack11ll11lll1_opy_, bstack1l11ll1l1l_opy_, bstack11ll11ll11_opy_, bstack11ll1l1l1l_opy_, \
    bstack11ll1111l_opy_, bstack11ll1l11ll_opy_, bstack11llll1111_opy_, bstack1ll1l11l11_opy_, bstack11llll1l11_opy_, \
    bstack1ll111ll_opy_, bstack11l1l11ll1_opy_
from bstack_utils.proxy import bstack1l111111l1_opy_, bstack1ll1lll1_opy_
from bstack_utils.bstack1l1lllllll_opy_ import bstack11111l1llll_opy_, bstack11111l1ll11_opy_, bstack11111ll1111_opy_, bstack11111ll11l1_opy_, \
    bstack11111ll111l_opy_, bstack11111ll11ll_opy_, bstack11111l1l1ll_opy_, bstack1ll11lll11_opy_, bstack11111ll1ll1_opy_
from bstack_utils.bstack1ll111111_opy_ import bstack1l1l11l111_opy_
from bstack_utils.bstack1l1l11l11l_opy_ import bstack11l1lll11_opy_, bstack1l1lll11ll_opy_, bstack1lll1lllll_opy_, \
    bstack11l1l1l11l_opy_, bstack11lll1l11l_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack111ll11ll1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1ll11_opy_
import bstack_utils.accessibility as bstack11l11lll11_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack1l1l1l1ll_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack11llll1l1l_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack111l11l1l_opy_
from browserstack_sdk.__init__ import bstack11lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111ll_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack11111l11l_opy_ import bstack11111l11l_opy_, bstack11l11l1l_opy_, bstack11ll1111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l11l1l1_opy_, bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11111l11l_opy_ import bstack11111l11l_opy_, bstack11l11l1l_opy_, bstack11ll1111ll_opy_
bstack1l1llll1_opy_ = None
bstack11llll1l_opy_ = None
bstack1ll1l1lll1_opy_ = None
bstack111ll1l1_opy_ = None
bstack11l1l1ll1l_opy_ = None
bstack11l11l1l1l_opy_ = None
bstack11ll11111l_opy_ = None
bstack1ll1111ll1_opy_ = None
bstack11lllllll_opy_ = None
bstack1l1l1ll111_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11l111l1_opy_ = None
bstack1ll111ll1_opy_ = None
bstack1lll11l1ll_opy_ = bstack11ll11_opy_ (u"ࠩࠪℑ")
CONFIG = {}
bstack1ll1lllll1_opy_ = False
bstack11lll111ll_opy_ = bstack11ll11_opy_ (u"ࠪࠫℒ")
bstack11llllll11_opy_ = bstack11ll11_opy_ (u"ࠫࠬℓ")
bstack111lll1ll_opy_ = False
bstack1l11ll1ll1_opy_ = []
bstack11lllll11l_opy_ = bstack11ll11ll_opy_
bstack1llll1l11l1l_opy_ = bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ℔")
bstack1lll1ll1ll_opy_ = {}
bstack11ll11lll_opy_ = None
bstack11l1ll1l11_opy_ = False
logger = bstack1111l1ll1_opy_.get_logger(__name__, bstack11lllll11l_opy_)
store = {
    bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪℕ"): []
}
bstack1lllll111111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1111lll111_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l11l1l1_opy_(
    test_framework_name=bstack1lllll1l1_opy_[bstack11ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࠭ࡃࡆࡇࠫ№")] if bstack111ll11l_opy_() else bstack1lllll1l1_opy_[bstack11ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࠨ℗")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1111ll1l_opy_(page, bstack11l1l1ll11_opy_):
    try:
        page.evaluate(bstack11ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ℘"),
                      bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧℙ") + json.dumps(
                          bstack11l1l1ll11_opy_) + bstack11ll11_opy_ (u"ࠦࢂࢃࠢℚ"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥℛ"), e)
def bstack1l11l111l_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢℜ"), bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬℝ") + json.dumps(
            message) + bstack11ll11_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫ℞") + json.dumps(level) + bstack11ll11_opy_ (u"ࠩࢀࢁࠬ℟"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨ℠"), e)
def pytest_configure(config):
    global bstack11lll111ll_opy_
    global CONFIG
    bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
    config.args = bstack11l1ll11_opy_.bstack1lllll11111l_opy_(config.args)
    bstack1l1ll1llll_opy_.bstack1111111l_opy_(bstack1l111ll1l_opy_(config.getoption(bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ℡"))))
    try:
        bstack1111l1ll1_opy_.bstack111ll1lll1l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.CONNECT, bstack11ll1111ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ™"), bstack11ll11_opy_ (u"࠭࠰ࠨ℣")))
        config = json.loads(os.environ.get(bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨℤ"), bstack11ll11_opy_ (u"ࠣࡽࢀࠦ℥")))
        cli.bstack1ll1lll11l1_opy_(bstack11ll11l111_opy_(bstack11lll111ll_opy_, CONFIG), cli_context.platform_index, bstack1ll11111l_opy_)
    if cli.bstack1lll1111lll_opy_(bstack1llll11l11l_opy_):
        cli.bstack1ll1lll111l_opy_()
        logger.debug(bstack11ll11_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣΩ") + str(cli_context.platform_index) + bstack11ll11_opy_ (u"ࠥࠦ℧"))
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.BEFORE_ALL, bstack1ll1l1lll11_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11ll11_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤℨ"), None)
    if cli.is_running() and when == bstack11ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ℩"):
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.LOG_REPORT, bstack1ll1l1lll11_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࠦK"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤÅ")))
        if not passed:
            config = json.loads(os.environ.get(bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢℬ"), bstack11ll11_opy_ (u"ࠤࡾࢁࠧℭ")))
            if bstack111l11l1l_opy_.bstack1llll1ll11_opy_(config):
                bstack111l11111l1_opy_ = bstack111l11l1l_opy_.bstack11ll1llll_opy_(config)
                if item.execution_count > bstack111l11111l1_opy_:
                    print(bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡳࡧࡷࡶ࡮࡫ࡳ࠻ࠢࠪ℮"), report.nodeid, os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩℯ")))
                    bstack111l11l1l_opy_.bstack111l1l111l1_opy_(report.nodeid)
            else:
                print(bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠬℰ"), report.nodeid, os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫℱ")))
                bstack111l11l1l_opy_.bstack111l1l111l1_opy_(report.nodeid)
        else:
            print(bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࠥࡶࡡࡴࡵࡨࡨ࠿ࠦࠧℲ"), report.nodeid, os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ℳ")))
    if cli.is_running():
        if when == bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣℴ"):
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.BEFORE_EACH, bstack1ll1l1lll11_opy_.POST, item, call, outcome)
        elif when == bstack11ll11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣℵ"):
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.LOG_REPORT, bstack1ll1l1lll11_opy_.POST, item, call, outcome)
        elif when == bstack11ll11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨℶ"):
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.AFTER_EACH, bstack1ll1l1lll11_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llll1l11ll1_opy_
    skipSessionName = item.config.getoption(bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧℷ"))
    plugins = item.config.getoption(bstack11ll11_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢℸ"))
    report = outcome.get_result()
    os.environ[bstack11ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪℹ")] = report.nodeid
    bstack1llll1l1llll_opy_(item, call, report)
    if bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨ℺") not in plugins or bstack111ll11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll11_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥ℻"), None)
    page = getattr(item, bstack11ll11_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤℼ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll1llllll_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll1l1l1l1_opy_(item, report, summary, skipSessionName)
def bstack1llll1llllll_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪℽ") and report.skipped:
        bstack11111ll1ll1_opy_(report)
    if report.when in [bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦℾ"), bstack11ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣℿ")]:
        return
    if not bstack1l1ll111ll1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ⅀")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⅁") + json.dumps(
                    report.nodeid) + bstack11ll11_opy_ (u"ࠩࢀࢁࠬ⅂"))
        os.environ[bstack11ll11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⅃")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦ⅄").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢⅅ")))
    bstack1lll11l11_opy_ = bstack11ll11_opy_ (u"ࠨࠢⅆ")
    bstack11111ll1ll1_opy_(report)
    if not passed:
        try:
            bstack1lll11l11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢⅇ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll11l11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥⅈ")))
        bstack1lll11l11_opy_ = bstack11ll11_opy_ (u"ࠤࠥⅉ")
        if not passed:
            try:
                bstack1lll11l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⅊").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll11l11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⅋")
                    + json.dumps(bstack11ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨ⅌"))
                    + bstack11ll11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ⅍")
                )
            else:
                item._driver.execute_script(
                    bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬⅎ")
                    + json.dumps(str(bstack1lll11l11_opy_))
                    + bstack11ll11_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ⅏")
                )
        except Exception as e:
            summary.append(bstack11ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢ⅐").format(e))
def bstack1llll1l1l1ll_opy_(test_name, error_message):
    try:
        bstack1llll1lll111_opy_ = []
        bstack1l111l111l_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⅑"), bstack11ll11_opy_ (u"ࠫ࠵࠭⅒"))
        bstack11l111111_opy_ = {bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⅓"): test_name, bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⅔"): error_message, bstack11ll11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⅕"): bstack1l111l111l_opy_}
        bstack1llll1l1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⅖"))
        if os.path.exists(bstack1llll1l1l11l_opy_):
            with open(bstack1llll1l1l11l_opy_) as f:
                bstack1llll1lll111_opy_ = json.load(f)
        bstack1llll1lll111_opy_.append(bstack11l111111_opy_)
        with open(bstack1llll1l1l11l_opy_, bstack11ll11_opy_ (u"ࠩࡺࠫ⅗")) as f:
            json.dump(bstack1llll1lll111_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨ⅘") + str(e))
def bstack1llll1l1l1l1_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⅙"), bstack11ll11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⅚")]:
        return
    if (str(skipSessionName).lower() != bstack11ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫ⅛")):
        bstack1111ll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⅜")))
    bstack1lll11l11_opy_ = bstack11ll11_opy_ (u"ࠣࠤ⅝")
    bstack11111ll1ll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll11l11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⅞").format(e)
                )
        try:
            if passed:
                bstack11lll1l11l_opy_(getattr(item, bstack11ll11_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⅟"), None), bstack11ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦⅠ"))
            else:
                error_message = bstack11ll11_opy_ (u"ࠬ࠭Ⅱ")
                if bstack1lll11l11_opy_:
                    bstack1l11l111l_opy_(item._page, str(bstack1lll11l11_opy_), bstack11ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧⅢ"))
                    bstack11lll1l11l_opy_(getattr(item, bstack11ll11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭Ⅳ"), None), bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣⅤ"), str(bstack1lll11l11_opy_))
                    error_message = str(bstack1lll11l11_opy_)
                else:
                    bstack11lll1l11l_opy_(getattr(item, bstack11ll11_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨⅥ"), None), bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥⅦ"))
                bstack1llll1l1l1ll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣⅧ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11ll11_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤⅨ"), default=bstack11ll11_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧⅩ"), help=bstack11ll11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨⅪ"))
    parser.addoption(bstack11ll11_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢⅫ"), default=bstack11ll11_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣⅬ"), help=bstack11ll11_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤⅭ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll11_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨⅮ"), action=bstack11ll11_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦⅯ"), default=bstack11ll11_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨⅰ"),
                         help=bstack11ll11_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨⅱ"))
def bstack111ll1l1l1_opy_(log):
    if not (log[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩⅲ")] and log[bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪⅳ")].strip()):
        return
    active = bstack111llll1l1_opy_()
    log = {
        bstack11ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩⅴ"): log[bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪⅵ")],
        bstack11ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨⅶ"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"࡚࠭ࠨⅷ"),
        bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨⅸ"): log[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩⅹ")],
    }
    if active:
        if active[bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧⅺ")] == bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨⅻ"):
            log[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅼ")] = active[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅽ")]
        elif active[bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫⅾ")] == bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࠬⅿ"):
            log[bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨↀ")] = active[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩↁ")]
    bstack1l1l1l1ll_opy_.bstack11ll1lllll_opy_([log])
def bstack111llll1l1_opy_():
    if len(store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧↂ")]) > 0 and store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨↃ")][-1]:
        return {
            bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪↄ"): bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫↅ"),
            bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧↆ"): store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬↇ")][-1]
        }
    if store.get(bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ↈ"), None):
        return {
            bstack11ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ↉"): bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ↊"),
            bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ↋"): store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ↌")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.INIT_TEST, bstack1ll1l1lll11_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.INIT_TEST, bstack1ll1l1lll11_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llll1l1l111_opy_ = True
        bstack1ll1l11l1l_opy_ = bstack11l11lll11_opy_.bstack1ll1lllll_opy_(bstack11l11l1111l_opy_(item.own_markers))
        if not cli.bstack1lll1111lll_opy_(bstack1llll11l11l_opy_):
            item._a11y_test_case = bstack1ll1l11l1l_opy_
            if bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭↍"), None):
                driver = getattr(item, bstack11ll11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ↎"), None)
                item._a11y_started = bstack11l11lll11_opy_.bstack1l1111l1l1_opy_(driver, bstack1ll1l11l1l_opy_)
        if not bstack1l1l1l1ll_opy_.on() or bstack1llll1l11l1l_opy_ != bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ↏"):
            return
        global current_test_uuid #, bstack111ll1llll_opy_
        bstack111l11ll11_opy_ = {
            bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ←"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ↑"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧ→")
        }
        current_test_uuid = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↓")]
        store[bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ↔")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↕")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1111lll111_opy_[item.nodeid] = {**_1111lll111_opy_[item.nodeid], **bstack111l11ll11_opy_}
        bstack1llll1ll11ll_opy_(item, _1111lll111_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ↖"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬ↗"), str(err))
def pytest_runtest_setup(item):
    store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ↘")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.BEFORE_EACH, bstack1ll1l1lll11_opy_.PRE, item, bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ↙"))
    if bstack111l11l1l_opy_.bstack111l11lllll_opy_():
            bstack1llll1l111ll_opy_ = bstack11ll11_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡡࡴࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥ↚")
            logger.error(bstack1llll1l111ll_opy_)
            bstack111l11ll11_opy_ = {
                bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↛"): uuid4().__str__(),
                bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ↜"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠩ࡝ࠫ↝"),
                bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ↞"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠫ࡟࠭↟"),
                bstack11ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ↠"): bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ↡"),
                bstack11ll11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ↢"): bstack1llll1l111ll_opy_,
                bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ↣"): [],
                bstack11ll11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ↤"): []
            }
            bstack1llll1ll11ll_opy_(item, bstack111l11ll11_opy_, bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ↥"))
            pytest.skip(bstack1llll1l111ll_opy_)
            return # skip all existing bstack1llll1l11ll1_opy_
    global bstack1lllll111111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l11l1l1_opy_():
        atexit.register(bstack1ll11l1ll_opy_)
        if not bstack1lllll111111_opy_:
            try:
                bstack1llll1lll1l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1111l1l1_opy_():
                    bstack1llll1lll1l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1lll1l1_opy_:
                    signal.signal(s, bstack1llll1llll1l_opy_)
                bstack1lllll111111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧ↦") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l1llll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ↧")
    try:
        if not bstack1l1l1l1ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11ll11_opy_ = {
            bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↨"): uuid,
            bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↩"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠨ࡜ࠪ↪"),
            bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ↫"): bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ↬"),
            bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ↭"): bstack11ll11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ↮"),
            bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ↯"): bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭↰")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ↱")] = item
        store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭↲")] = [uuid]
        if not _1111lll111_opy_.get(item.nodeid, None):
            _1111lll111_opy_[item.nodeid] = {bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ↳"): [], bstack11ll11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭↴"): []}
        _1111lll111_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ↵")].append(bstack111l11ll11_opy_[bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↶")])
        _1111lll111_opy_[item.nodeid + bstack11ll11_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧ↷")] = bstack111l11ll11_opy_
        bstack1llll1ll1l11_opy_(item, bstack111l11ll11_opy_, bstack11ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ↸"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ↹"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.AFTER_EACH, bstack1ll1l1lll11_opy_.PRE, item, bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ↺"))
        return # skip all existing bstack1llll1l11ll1_opy_
    try:
        global bstack1lll1ll1ll_opy_
        bstack1l111l111l_opy_ = 0
        if bstack111lll1ll_opy_ is True:
            bstack1l111l111l_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ↻")))
        if bstack1l1111ll1_opy_.bstack11ll1ll1l_opy_() == bstack11ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥ↼"):
            if bstack1l1111ll1_opy_.bstack1l1l11l1_opy_() == bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ↽"):
                bstack1llll1l1ll11_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ↾"), None)
                bstack1ll1ll1ll1_opy_ = bstack1llll1l1ll11_opy_ + bstack11ll11_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ↿")
                driver = getattr(item, bstack11ll11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⇀"), None)
                bstack1l1lll11l1_opy_ = getattr(item, bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⇁"), None)
                bstack1l1111111_opy_ = getattr(item, bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇂"), None)
                PercySDK.screenshot(driver, bstack1ll1ll1ll1_opy_, bstack1l1lll11l1_opy_=bstack1l1lll11l1_opy_, bstack1l1111111_opy_=bstack1l1111111_opy_, bstack11ll1lll1_opy_=bstack1l111l111l_opy_)
        if not cli.bstack1lll1111lll_opy_(bstack1llll11l11l_opy_):
            if getattr(item, bstack11ll11_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬ⇃"), False):
                bstack1l111l1l_opy_.bstack1l1l1ll11l_opy_(getattr(item, bstack11ll11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⇄"), None), bstack1lll1ll1ll_opy_, logger, item)
        if not bstack1l1l1l1ll_opy_.on():
            return
        bstack111l11ll11_opy_ = {
            bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⇅"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⇆"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠩ࡝ࠫ⇇"),
            bstack11ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ⇈"): bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⇉"),
            bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⇊"): bstack11ll11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⇋"),
            bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⇌"): bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⇍")
        }
        _1111lll111_opy_[item.nodeid + bstack11ll11_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬ⇎")] = bstack111l11ll11_opy_
        bstack1llll1ll1l11_opy_(item, bstack111l11ll11_opy_, bstack11ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⇏"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪ⇐"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111ll11l1_opy_(fixturedef.argname):
        store[bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ⇑")] = request.node
    elif bstack11111ll111l_opy_(fixturedef.argname):
        store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ⇒")] = request.node
    if not bstack1l1l1l1ll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.SETUP_FIXTURE, bstack1ll1l1lll11_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.SETUP_FIXTURE, bstack1ll1l1lll11_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11ll1_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.SETUP_FIXTURE, bstack1ll1l1lll11_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.SETUP_FIXTURE, bstack1ll1l1lll11_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1l11ll1_opy_
    try:
        fixture = {
            bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⇓"): fixturedef.argname,
            bstack11ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇔"): bstack11l11lll1ll_opy_(outcome),
            bstack11ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⇕"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⇖")]
        if not _1111lll111_opy_.get(current_test_item.nodeid, None):
            _1111lll111_opy_[current_test_item.nodeid] = {bstack11ll11_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⇗"): []}
        _1111lll111_opy_[current_test_item.nodeid][bstack11ll11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⇘")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ⇙"), str(err))
if bstack111ll11l_opy_() and bstack1l1l1l1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.STEP, bstack1ll1l1lll11_opy_.PRE, request, step)
            return
        try:
            _1111lll111_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⇚")].bstack11l1llll11_opy_(id(step))
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭⇛"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.STEP, bstack1ll1l1lll11_opy_.POST, request, step, exception)
            return
        try:
            _1111lll111_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⇜")].bstack111ll1ll11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ⇝"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.STEP, bstack1ll1l1lll11_opy_.POST, request, step)
            return
        try:
            bstack111lll1ll1_opy_: bstack111ll11ll1_opy_ = _1111lll111_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⇞")]
            bstack111lll1ll1_opy_.bstack111ll1ll11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ⇟"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1l11l1l_opy_
        try:
            if not bstack1l1l1l1ll_opy_.on() or bstack1llll1l11l1l_opy_ != bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⇠"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.PRE, request, feature, scenario)
                return
            driver = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭⇡"), None)
            if not _1111lll111_opy_.get(request.node.nodeid, None):
                _1111lll111_opy_[request.node.nodeid] = {}
            bstack111lll1ll1_opy_ = bstack111ll11ll1_opy_.bstack11111111ll1_opy_(
                scenario, feature, request.node,
                name=bstack11111ll11ll_opy_(request.node, scenario),
                started_at=bstack1l11l11ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⇢"),
                tags=bstack11111l1l1ll_opy_(feature, scenario),
                bstack111lll11l1_opy_=bstack1l1l1l1ll_opy_.bstack111ll1l111_opy_(driver) if driver and driver.session_id else {}
            )
            _1111lll111_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⇣")] = bstack111lll1ll1_opy_
            bstack1llll1lll11l_opy_(bstack111lll1ll1_opy_.uuid)
            bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⇤"), bstack111lll1ll1_opy_)
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭⇥"), str(err))
def bstack1llll1l1lll1_opy_(bstack111llll111_opy_):
    if bstack111llll111_opy_ in store[bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⇦")]:
        store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⇧")].remove(bstack111llll111_opy_)
def bstack1llll1lll11l_opy_(test_uuid):
    store[bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⇨")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1l1l1ll_opy_.bstack1lllll1ll11l_opy_
def bstack1llll1l1llll_opy_(item, call, report):
    logger.debug(bstack11ll11_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡳࡶࠪ⇩"))
    global bstack1llll1l11l1l_opy_
    bstack1l1llllll1_opy_ = bstack1l11l11ll_opy_()
    if hasattr(report, bstack11ll11_opy_ (u"ࠩࡶࡸࡴࡶࠧ⇪")):
        bstack1l1llllll1_opy_ = bstack11l1l11ll11_opy_(report.stop)
    elif hasattr(report, bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ⇫")):
        bstack1l1llllll1_opy_ = bstack11l1l11ll11_opy_(report.start)
    try:
        if getattr(report, bstack11ll11_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⇬"), bstack11ll11_opy_ (u"ࠬ࠭⇭")) == bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⇮"):
            logger.debug(bstack11ll11_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ⇯").format(getattr(report, bstack11ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⇰"), bstack11ll11_opy_ (u"ࠩࠪ⇱")).__str__(), bstack1llll1l11l1l_opy_))
            if bstack1llll1l11l1l_opy_ == bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⇲"):
                _1111lll111_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⇳")] = bstack1l1llllll1_opy_
                bstack1llll1ll11ll_opy_(item, _1111lll111_opy_[item.nodeid], bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⇴"), report, call)
                store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⇵")] = None
            elif bstack1llll1l11l1l_opy_ == bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ⇶"):
                bstack111lll1ll1_opy_ = _1111lll111_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⇷")]
                bstack111lll1ll1_opy_.set(hooks=_1111lll111_opy_[item.nodeid].get(bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⇸"), []))
                exception, bstack111ll1ll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111ll1ll1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll11_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩ⇹"), bstack11ll11_opy_ (u"ࠫࠬ⇺"))]
                bstack111lll1ll1_opy_.stop(time=bstack1l1llllll1_opy_, result=Result(result=getattr(report, bstack11ll11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⇻"), bstack11ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⇼")), exception=exception, bstack111ll1ll1l_opy_=bstack111ll1ll1l_opy_))
                bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⇽"), _1111lll111_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⇾")])
        elif getattr(report, bstack11ll11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⇿"), bstack11ll11_opy_ (u"ࠪࠫ∀")) in [bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ∁"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ∂")]:
            logger.debug(bstack11ll11_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ∃").format(getattr(report, bstack11ll11_opy_ (u"ࠧࡸࡪࡨࡲࠬ∄"), bstack11ll11_opy_ (u"ࠨࠩ∅")).__str__(), bstack1llll1l11l1l_opy_))
            bstack111ll11lll_opy_ = item.nodeid + bstack11ll11_opy_ (u"ࠩ࠰ࠫ∆") + getattr(report, bstack11ll11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ∇"), bstack11ll11_opy_ (u"ࠫࠬ∈"))
            if getattr(report, bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭∉"), False):
                hook_type = bstack11ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ∊") if getattr(report, bstack11ll11_opy_ (u"ࠧࡸࡪࡨࡲࠬ∋"), bstack11ll11_opy_ (u"ࠨࠩ∌")) == bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ∍") else bstack11ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ∎")
                _1111lll111_opy_[bstack111ll11lll_opy_] = {
                    bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ∏"): uuid4().__str__(),
                    bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ∐"): bstack1l1llllll1_opy_,
                    bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ∑"): hook_type
                }
            _1111lll111_opy_[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ−")] = bstack1l1llllll1_opy_
            bstack1llll1l1lll1_opy_(_1111lll111_opy_[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭∓")])
            bstack1llll1ll1l11_opy_(item, _1111lll111_opy_[bstack111ll11lll_opy_], bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ∔"), report, call)
            if getattr(report, bstack11ll11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ∕"), bstack11ll11_opy_ (u"ࠫࠬ∖")) == bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ∗"):
                if getattr(report, bstack11ll11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ∘"), bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ∙")) == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ√"):
                    bstack111l11ll11_opy_ = {
                        bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ∛"): uuid4().__str__(),
                        bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ∜"): bstack1l11l11ll_opy_(),
                        bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ∝"): bstack1l11l11ll_opy_()
                    }
                    _1111lll111_opy_[item.nodeid] = {**_1111lll111_opy_[item.nodeid], **bstack111l11ll11_opy_}
                    bstack1llll1ll11ll_opy_(item, _1111lll111_opy_[item.nodeid], bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭∞"))
                    bstack1llll1ll11ll_opy_(item, _1111lll111_opy_[item.nodeid], bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ∟"), report, call)
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬ∠"), str(err))
def bstack1llll1ll1l1l_opy_(test, bstack111l11ll11_opy_, result=None, call=None, bstack1l1ll11l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lll1ll1_opy_ = {
        bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭∡"): bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ∢")],
        bstack11ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ∣"): bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ∤"),
        bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ∥"): test.name,
        bstack11ll11_opy_ (u"࠭ࡢࡰࡦࡼࠫ∦"): {
            bstack11ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ∧"): bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ∨"),
            bstack11ll11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ∩"): inspect.getsource(test.obj)
        },
        bstack11ll11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ∪"): test.name,
        bstack11ll11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ∫"): test.name,
        bstack11ll11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ∬"): bstack11l1ll11_opy_.bstack111ll111ll_opy_(test),
        bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ∭"): file_path,
        bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ∮"): file_path,
        bstack11ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ∯"): bstack11ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ∰"),
        bstack11ll11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ∱"): file_path,
        bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ∲"): bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ∳")],
        bstack11ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ∴"): bstack11ll11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ∵"),
        bstack11ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ∶"): {
            bstack11ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭∷"): test.nodeid
        },
        bstack11ll11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ∸"): bstack11l11l1111l_opy_(test.own_markers)
    }
    if bstack1l1ll11l1l_opy_ in [bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ∹"), bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ∺")]:
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"࠭࡭ࡦࡶࡤࠫ∻")] = {
            bstack11ll11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ∼"): bstack111l11ll11_opy_.get(bstack11ll11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ∽"), [])
        }
    if bstack1l1ll11l1l_opy_ == bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ∾"):
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ∿")] = bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ≀")
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ≁")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≂")]
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ≃")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭≄")]
    if result:
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ≅")] = result.outcome
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ≆")] = result.duration * 1000
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≇")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≈")]
        if result.failed:
            bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ≉")] = bstack1l1l1l1ll_opy_.bstack11111l111l_opy_(call.excinfo.typename)
            bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ≊")] = bstack1l1l1l1ll_opy_.bstack1llllll11lll_opy_(call.excinfo, result)
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ≋")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ≌")]
    if outcome:
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ≍")] = bstack11l11lll1ll_opy_(outcome)
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ≎")] = 0
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≏")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≐")]
        if bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ≑")] == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ≒"):
            bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ≓")] = bstack11ll11_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ≔")  # bstack1llll1llll11_opy_
            bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ≕")] = [{bstack11ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ≖"): [bstack11ll11_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ≗")]}]
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭≘")] = bstack111l11ll11_opy_[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ≙")]
    return bstack111lll1ll1_opy_
def bstack1llll1l11l11_opy_(test, bstack111l1l1lll_opy_, bstack1l1ll11l1l_opy_, result, call, outcome, bstack1llll1l111l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ≚")]
    hook_name = bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭≛")]
    hook_data = {
        bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ≜"): bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ≝")],
        bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ≞"): bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ≟"),
        bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭≠"): bstack11ll11_opy_ (u"ࠩࡾࢁࠬ≡").format(bstack11111l1ll11_opy_(hook_name)),
        bstack11ll11_opy_ (u"ࠪࡦࡴࡪࡹࠨ≢"): {
            bstack11ll11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ≣"): bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ≤"),
            bstack11ll11_opy_ (u"࠭ࡣࡰࡦࡨࠫ≥"): None
        },
        bstack11ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭≦"): test.name,
        bstack11ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ≧"): bstack11l1ll11_opy_.bstack111ll111ll_opy_(test, hook_name),
        bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ≨"): file_path,
        bstack11ll11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ≩"): file_path,
        bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ≪"): bstack11ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭≫"),
        bstack11ll11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ≬"): file_path,
        bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ≭"): bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ≮")],
        bstack11ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ≯"): bstack11ll11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ≰") if bstack1llll1l11l1l_opy_ == bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ≱") else bstack11ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ≲"),
        bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ≳"): hook_type
    }
    bstack1111111ll11_opy_ = bstack111l11l111_opy_(_1111lll111_opy_.get(test.nodeid, None))
    if bstack1111111ll11_opy_:
        hook_data[bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ≴")] = bstack1111111ll11_opy_
    if result:
        hook_data[bstack11ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≵")] = result.outcome
        hook_data[bstack11ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ≶")] = result.duration * 1000
        hook_data[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≷")] = bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≸")]
        if result.failed:
            hook_data[bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ≹")] = bstack1l1l1l1ll_opy_.bstack11111l111l_opy_(call.excinfo.typename)
            hook_data[bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ≺")] = bstack1l1l1l1ll_opy_.bstack1llllll11lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ≻")] = bstack11l11lll1ll_opy_(outcome)
        hook_data[bstack11ll11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ≼")] = 100
        hook_data[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ≽")] = bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≾")]
        if hook_data[bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ≿")] == bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⊀"):
            hook_data[bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⊁")] = bstack11ll11_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⊂")  # bstack1llll1llll11_opy_
            hook_data[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⊃")] = [{bstack11ll11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⊄"): [bstack11ll11_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⊅")]}]
    if bstack1llll1l111l1_opy_:
        hook_data[bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⊆")] = bstack1llll1l111l1_opy_.result
        hook_data[bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⊇")] = bstack11l1l11l1ll_opy_(bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊈")], bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊉")])
        hook_data[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊊")] = bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⊋")]
        if hook_data[bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⊌")] == bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⊍"):
            hook_data[bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⊎")] = bstack1l1l1l1ll_opy_.bstack11111l111l_opy_(bstack1llll1l111l1_opy_.exception_type)
            hook_data[bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⊏")] = [{bstack11ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⊐"): bstack11l1l111ll1_opy_(bstack1llll1l111l1_opy_.exception)}]
    return hook_data
def bstack1llll1ll11ll_opy_(test, bstack111l11ll11_opy_, bstack1l1ll11l1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11ll11_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ⊑").format(bstack1l1ll11l1l_opy_))
    bstack111lll1ll1_opy_ = bstack1llll1ll1l1l_opy_(test, bstack111l11ll11_opy_, result, call, bstack1l1ll11l1l_opy_, outcome)
    driver = getattr(test, bstack11ll11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⊒"), None)
    if bstack1l1ll11l1l_opy_ == bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⊓") and driver:
        bstack111lll1ll1_opy_[bstack11ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⊔")] = bstack1l1l1l1ll_opy_.bstack111ll1l111_opy_(driver)
    if bstack1l1ll11l1l_opy_ == bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⊕"):
        bstack1l1ll11l1l_opy_ = bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⊖")
    bstack111l1l1ll1_opy_ = {
        bstack11ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⊗"): bstack1l1ll11l1l_opy_,
        bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⊘"): bstack111lll1ll1_opy_
    }
    bstack1l1l1l1ll_opy_.bstack1l1l11lll1_opy_(bstack111l1l1ll1_opy_)
    if bstack1l1ll11l1l_opy_ == bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⊙"):
        threading.current_thread().bstackTestMeta = {bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⊚"): bstack11ll11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⊛")}
    elif bstack1l1ll11l1l_opy_ == bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⊜"):
        threading.current_thread().bstackTestMeta = {bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⊝"): getattr(result, bstack11ll11_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⊞"), bstack11ll11_opy_ (u"ࠨࠩ⊟"))}
def bstack1llll1ll1l11_opy_(test, bstack111l11ll11_opy_, bstack1l1ll11l1l_opy_, result=None, call=None, outcome=None, bstack1llll1l111l1_opy_=None):
    logger.debug(bstack11ll11_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⊠").format(bstack1l1ll11l1l_opy_))
    hook_data = bstack1llll1l11l11_opy_(test, bstack111l11ll11_opy_, bstack1l1ll11l1l_opy_, result, call, outcome, bstack1llll1l111l1_opy_)
    bstack111l1l1ll1_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⊡"): bstack1l1ll11l1l_opy_,
        bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭⊢"): hook_data
    }
    bstack1l1l1l1ll_opy_.bstack1l1l11lll1_opy_(bstack111l1l1ll1_opy_)
def bstack111l11l111_opy_(bstack111l11ll11_opy_):
    if not bstack111l11ll11_opy_:
        return None
    if bstack111l11ll11_opy_.get(bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⊣"), None):
        return getattr(bstack111l11ll11_opy_[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⊤")], bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⊥"), None)
    return bstack111l11ll11_opy_.get(bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊦"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.LOG, bstack1ll1l1lll11_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_.LOG, bstack1ll1l1lll11_opy_.POST, request, caplog)
        return # skip all existing bstack1llll1l11ll1_opy_
    try:
        if not bstack1l1l1l1ll_opy_.on():
            return
        places = [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⊧"), bstack11ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⊨"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⊩")]
        logs = []
        for bstack1llll1ll1111_opy_ in places:
            records = caplog.get_records(bstack1llll1ll1111_opy_)
            bstack1llll1lllll1_opy_ = bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⊪") if bstack1llll1ll1111_opy_ == bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⊫") else bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⊬")
            bstack1llll1l1ll1l_opy_ = request.node.nodeid + (bstack11ll11_opy_ (u"ࠨࠩ⊭") if bstack1llll1ll1111_opy_ == bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࠧ⊮") else bstack11ll11_opy_ (u"ࠪ࠱ࠬ⊯") + bstack1llll1ll1111_opy_)
            test_uuid = bstack111l11l111_opy_(_1111lll111_opy_.get(bstack1llll1l1ll1l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l111llll1_opy_(record.message):
                    continue
                logs.append({
                    bstack11ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⊰"): bstack11l1111llll_opy_(record.created).isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧ⊱"),
                    bstack11ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⊲"): record.levelname,
                    bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⊳"): record.message,
                    bstack1llll1lllll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1l1l1ll_opy_.bstack11ll1lllll_opy_(logs)
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ⊴"), str(err))
def bstack1l1l1l1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1ll1l11_opy_
    bstack11111111l_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭⊵"), None) and bstack111ll1lll_opy_(
            threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⊶"), None)
    bstack1l11l1lll_opy_ = getattr(driver, bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⊷"), None) != None and getattr(driver, bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⊸"), None) == True
    if sequence == bstack11ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⊹") and driver != None:
      if not bstack11l1ll1l11_opy_ and bstack1l1ll111ll1_opy_() and bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⊺") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⊻")] == True and bstack11llll1l1l_opy_.bstack1l1ll1l11l_opy_(driver_command) and (bstack1l11l1lll_opy_ or bstack11111111l_opy_) and not bstack1l111l11ll_opy_(args):
        try:
          bstack11l1ll1l11_opy_ = True
          logger.debug(bstack11ll11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ⊼").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨ⊽").format(str(err)))
        bstack11l1ll1l11_opy_ = False
    if sequence == bstack11ll11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⊾"):
        if driver_command == bstack11ll11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ⊿"):
            bstack1l1l1l1ll_opy_.bstack111lll11l_opy_({
                bstack11ll11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ⋀"): response[bstack11ll11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭⋁")],
                bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⋂"): store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⋃")]
            })
def bstack1ll11l1ll_opy_():
    global bstack1l11ll1ll1_opy_
    bstack1111l1ll1_opy_.bstack11ll1l1ll1_opy_()
    logging.shutdown()
    bstack1l1l1l1ll_opy_.bstack111l111111_opy_()
    for driver in bstack1l11ll1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1llll1l_opy_(*args):
    global bstack1l11ll1ll1_opy_
    bstack1l1l1l1ll_opy_.bstack111l111111_opy_()
    for driver in bstack1l11ll1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11lll111l1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1ll111ll1l_opy_(self, *args, **kwargs):
    bstack1l11l1ll_opy_ = bstack1l1llll1_opy_(self, *args, **kwargs)
    bstack1lll1lll_opy_ = getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⋄"), None)
    if bstack1lll1lll_opy_ and bstack1lll1lll_opy_.get(bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⋅"), bstack11ll11_opy_ (u"ࠬ࠭⋆")) == bstack11ll11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⋇"):
        bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(self)
    return bstack1l11l1ll_opy_
@measure(event_name=EVENTS.bstack1l11llllll_opy_, stage=STAGE.bstack11l11l11l1_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1ll1ll111l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
    if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⋈")):
        return
    bstack1l1ll1llll_opy_.bstack1l111lll11_opy_(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⋉"), True)
    global bstack1lll11l1ll_opy_
    global bstack1ll111ll11_opy_
    bstack1lll11l1ll_opy_ = framework_name
    logger.info(bstack11l1l11ll1_opy_.format(bstack1lll11l1ll_opy_.split(bstack11ll11_opy_ (u"ࠩ࠰ࠫ⋊"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll111ll1_opy_():
            Service.start = bstack11111l111_opy_
            Service.stop = bstack11lllll1ll_opy_
            webdriver.Remote.get = bstack111111l11_opy_
            webdriver.Remote.__init__ = bstack1ll11ll11l_opy_
            if not isinstance(os.getenv(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ⋋")), str):
                return
            WebDriver.quit = bstack1l1l1111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1l1l1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1ll111ll1l_opy_
        bstack1ll111ll11_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11ll11_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⋌")):
        bstack1ll111ll11_opy_ = eval(os.environ.get(bstack11ll11_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ⋍")))
    if not bstack1ll111ll11_opy_:
        bstack1lll11l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ⋎"), bstack1ll111ll_opy_)
    if bstack11l1ll111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⋏")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⋐"))):
                RemoteConnection._get_proxy_url = bstack11l11l11_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11l11l11_opy_
        except Exception as e:
            logger.error(bstack11ll1111l_opy_.format(str(e)))
    if bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⋑") in str(framework_name).lower():
        if not bstack1l1ll111ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1l11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1ll1l1_opy_
            Config.getoption = bstack111l1l11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1l1lll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11lll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1l1l1111_opy_(self):
    global bstack1lll11l1ll_opy_
    global bstack11ll1111l1_opy_
    global bstack11llll1l_opy_
    try:
        if bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⋒") in bstack1lll11l1ll_opy_ and self.session_id != None and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ⋓"), bstack11ll11_opy_ (u"ࠬ࠭⋔")) != bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⋕"):
            bstack1l1l111l1l_opy_ = bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⋖") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⋗")
            bstack1lll1l1l1_opy_(logger, True)
            if os.environ.get(bstack11ll11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⋘"), None):
                self.execute_script(
                    bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ⋙") + json.dumps(
                        os.environ.get(bstack11ll11_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⋚"))) + bstack11ll11_opy_ (u"ࠬࢃࡽࠨ⋛"))
            if self != None:
                bstack11l1l1l11l_opy_(self, bstack1l1l111l1l_opy_, bstack11ll11_opy_ (u"࠭ࠬࠡࠩ⋜").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1111lll_opy_(bstack1llll11l11l_opy_):
            item = store.get(bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⋝"), None)
            if item is not None and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⋞"), None):
                bstack1l111l1l_opy_.bstack1l1l1ll11l_opy_(self, bstack1lll1ll1ll_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll11_opy_ (u"ࠩࠪ⋟")
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ⋠") + str(e))
    bstack11llll1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1llll1l11l_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack1ll11ll11l_opy_(self, command_executor,
             desired_capabilities=None, bstack1l1l11ll11_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11ll1111l1_opy_
    global bstack11ll11lll_opy_
    global bstack111lll1ll_opy_
    global bstack1lll11l1ll_opy_
    global bstack1l1llll1_opy_
    global bstack1l11ll1ll1_opy_
    global bstack11lll111ll_opy_
    global bstack11llllll11_opy_
    global bstack1lll1ll1ll_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⋡")] = str(bstack1lll11l1ll_opy_) + str(__version__)
    command_executor = bstack11ll11l111_opy_(bstack11lll111ll_opy_, CONFIG)
    logger.debug(bstack11ll11ll11_opy_.format(command_executor))
    proxy = bstack11l1l1111_opy_(CONFIG, proxy)
    bstack1l111l111l_opy_ = 0
    try:
        if bstack111lll1ll_opy_ is True:
            bstack1l111l111l_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⋢")))
    except:
        bstack1l111l111l_opy_ = 0
    bstack1lll1ll11_opy_ = bstack1l11l11l1_opy_(CONFIG, bstack1l111l111l_opy_)
    logger.debug(bstack11llll1111_opy_.format(str(bstack1lll1ll11_opy_)))
    bstack1lll1ll1ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⋣"))[bstack1l111l111l_opy_]
    if bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⋤") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⋥")]:
        bstack1lll1lllll_opy_(bstack1lll1ll11_opy_, bstack11llllll11_opy_)
    if bstack11l11lll11_opy_.bstack11lll11l1l_opy_(CONFIG, bstack1l111l111l_opy_) and bstack11l11lll11_opy_.bstack1ll1ll111_opy_(bstack1lll1ll11_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1111lll_opy_(bstack1llll11l11l_opy_):
            bstack11l11lll11_opy_.set_capabilities(bstack1lll1ll11_opy_, CONFIG)
    if desired_capabilities:
        bstack11lllll111_opy_ = bstack1l1l1l1111_opy_(desired_capabilities)
        bstack11lllll111_opy_[bstack11ll11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⋦")] = bstack1llll11l1l_opy_(CONFIG)
        bstack1l11llll1l_opy_ = bstack1l11l11l1_opy_(bstack11lllll111_opy_)
        if bstack1l11llll1l_opy_:
            bstack1lll1ll11_opy_ = update(bstack1l11llll1l_opy_, bstack1lll1ll11_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1l1l11_opy_(options, bstack1lll1ll11_opy_)
    if not options:
        options = bstack1ll11111l_opy_(bstack1lll1ll11_opy_)
    if proxy and bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⋧")):
        options.proxy(proxy)
    if options and bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⋨")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1ll1_opy_() < version.parse(bstack11ll11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⋩")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll1ll11_opy_)
    logger.info(bstack1l11ll1l1l_opy_)
    bstack1ll11ll1_opy_.end(EVENTS.bstack1l11llllll_opy_.value, EVENTS.bstack1l11llllll_opy_.value + bstack11ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⋪"),
                               EVENTS.bstack1l11llllll_opy_.value + bstack11ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⋫"), True, None)
    if bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⋬")):
        bstack1l1llll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⋭")):
        bstack1l1llll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1l1l11ll11_opy_=bstack1l1l11ll11_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ⋮")):
        bstack1l1llll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1l11ll11_opy_=bstack1l1l11ll11_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1llll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1l11ll11_opy_=bstack1l1l11ll11_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack111l1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࠬ⋯")
        if bstack1lll1ll1_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭⋰")):
            bstack111l1l11l_opy_ = self.caps.get(bstack11ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⋱"))
        else:
            bstack111l1l11l_opy_ = self.capabilities.get(bstack11ll11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⋲"))
        if bstack111l1l11l_opy_:
            bstack1lll111lll_opy_(bstack111l1l11l_opy_)
            if bstack1lll1ll1_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ⋳")):
                self.command_executor._url = bstack11ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⋴") + bstack11lll111ll_opy_ + bstack11ll11_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ⋵")
            else:
                self.command_executor._url = bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ⋶") + bstack111l1l11l_opy_ + bstack11ll11_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ⋷")
            logger.debug(bstack11ll11lll1_opy_.format(bstack111l1l11l_opy_))
        else:
            logger.debug(bstack111l1ll11_opy_.format(bstack11ll11_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ⋸")))
    except Exception as e:
        logger.debug(bstack111l1ll11_opy_.format(e))
    bstack11ll1111l1_opy_ = self.session_id
    if bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⋹") in bstack1lll11l1ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⋺"), None)
        if item:
            bstack1llll1ll1lll_opy_ = getattr(item, bstack11ll11_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ⋻"), False)
            if not getattr(item, bstack11ll11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⋼"), None) and bstack1llll1ll1lll_opy_:
                setattr(store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⋽")], bstack11ll11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⋾"), self)
        bstack1lll1lll_opy_ = getattr(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⋿"), None)
        if bstack1lll1lll_opy_ and bstack1lll1lll_opy_.get(bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⌀"), bstack11ll11_opy_ (u"ࠨࠩ⌁")) == bstack11ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⌂"):
            bstack1l1l1l1ll_opy_.bstack1l1l111ll_opy_(self)
    bstack1l11ll1ll1_opy_.append(self)
    if bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⌃") in CONFIG and bstack11ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⌄") in CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⌅")][bstack1l111l111l_opy_]:
        bstack11ll11lll_opy_ = CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⌆")][bstack1l111l111l_opy_][bstack11ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⌇")]
    logger.debug(bstack11llll1l11_opy_.format(bstack11ll1111l1_opy_))
@measure(event_name=EVENTS.bstack111llll1_opy_, stage=STAGE.bstack1lll11llll_opy_, bstack1111llll_opy_=bstack11ll11lll_opy_)
def bstack111111l11_opy_(self, url):
    global bstack11lllllll_opy_
    global CONFIG
    try:
        bstack1l1lll11ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1l11l11_opy_.format(str(err)))
    try:
        bstack11lllllll_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll1l1ll1_opy_ = str(e)
            if any(err_msg in bstack1ll1l1ll1_opy_ for err_msg in bstack1ll1ll11ll_opy_):
                bstack1l1lll11ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1l11l11_opy_.format(str(err)))
        raise e
def bstack11111lll_opy_(item, when):
    global bstack11l111l1_opy_
    try:
        bstack11l111l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l1lll1_opy_(item, call, rep):
    global bstack1ll111ll1_opy_
    global bstack1l11ll1ll1_opy_
    name = bstack11ll11_opy_ (u"ࠨࠩ⌈")
    try:
        if rep.when == bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࠧ⌉"):
            bstack11ll1111l1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⌊"))
            try:
                if (str(skipSessionName).lower() != bstack11ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩ⌋")):
                    name = str(rep.nodeid)
                    bstack11ll11l11_opy_ = bstack11l1lll11_opy_(bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⌌"), name, bstack11ll11_opy_ (u"࠭ࠧ⌍"), bstack11ll11_opy_ (u"ࠧࠨ⌎"), bstack11ll11_opy_ (u"ࠨࠩ⌏"), bstack11ll11_opy_ (u"ࠩࠪ⌐"))
                    os.environ[bstack11ll11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⌑")] = name
                    for driver in bstack1l11ll1ll1_opy_:
                        if bstack11ll1111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll11l11_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⌒").format(str(e)))
            try:
                bstack1ll11lll11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⌓"):
                    status = bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⌔") if rep.outcome.lower() == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌕") else bstack11ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⌖")
                    reason = bstack11ll11_opy_ (u"ࠩࠪ⌗")
                    if status == bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⌘"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ⌙") if status == bstack11ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⌚") else bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⌛")
                    data = name + bstack11ll11_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ⌜") if status == bstack11ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⌝") else name + bstack11ll11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ⌞") + reason
                    bstack11111ll11_opy_ = bstack11l1lll11_opy_(bstack11ll11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⌟"), bstack11ll11_opy_ (u"ࠫࠬ⌠"), bstack11ll11_opy_ (u"ࠬ࠭⌡"), bstack11ll11_opy_ (u"࠭ࠧ⌢"), level, data)
                    for driver in bstack1l11ll1ll1_opy_:
                        if bstack11ll1111l1_opy_ == driver.session_id:
                            driver.execute_script(bstack11111ll11_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⌣").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ⌤").format(str(e)))
    bstack1ll111ll1_opy_(item, call, rep)
notset = Notset()
def bstack111l1l11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll11ll1_opy_
    if str(name).lower() == bstack11ll11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ⌥"):
        return bstack11ll11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ⌦")
    else:
        return bstack1lll11ll1_opy_(self, name, default, skip)
def bstack11l11l11_opy_(self):
    global CONFIG
    global bstack11ll11111l_opy_
    try:
        proxy = bstack1l111111l1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ⌧")):
                proxies = bstack1ll1lll1_opy_(proxy, bstack11ll11l111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l11l1ll1l_opy_ = proxies.popitem()
                    if bstack11ll11_opy_ (u"ࠧࡀ࠯࠰ࠤ⌨") in bstack1l11l1ll1l_opy_:
                        return bstack1l11l1ll1l_opy_
                    else:
                        return bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ〈") + bstack1l11l1ll1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ〉").format(str(e)))
    return bstack11ll11111l_opy_(self)
def bstack11l1ll111l_opy_():
    return (bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⌫") in CONFIG or bstack11ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⌬") in CONFIG) and bstack1111llll1_opy_() and bstack1lll1ll1_opy_() >= version.parse(
        bstack1lll111ll_opy_)
def bstack1l1ll1l1ll_opy_(self,
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
    global bstack11ll11lll_opy_
    global bstack111lll1ll_opy_
    global bstack1lll11l1ll_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⌭")] = str(bstack1lll11l1ll_opy_) + str(__version__)
    bstack1l111l111l_opy_ = 0
    try:
        if bstack111lll1ll_opy_ is True:
            bstack1l111l111l_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⌮")))
    except:
        bstack1l111l111l_opy_ = 0
    CONFIG[bstack11ll11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ⌯")] = True
    bstack1lll1ll11_opy_ = bstack1l11l11l1_opy_(CONFIG, bstack1l111l111l_opy_)
    logger.debug(bstack11llll1111_opy_.format(str(bstack1lll1ll11_opy_)))
    if CONFIG.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⌰")):
        bstack1lll1lllll_opy_(bstack1lll1ll11_opy_, bstack11llllll11_opy_)
    if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⌱") in CONFIG and bstack11ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⌲") in CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⌳")][bstack1l111l111l_opy_]:
        bstack11ll11lll_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⌴")][bstack1l111l111l_opy_][bstack11ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⌵")]
    import urllib
    import json
    if bstack11ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⌶") in CONFIG and str(CONFIG[bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⌷")]).lower() != bstack11ll11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭⌸"):
        bstack1l1111l1l_opy_ = bstack11lll1l11_opy_()
        bstack1lll1l11l1_opy_ = bstack1l1111l1l_opy_ + urllib.parse.quote(json.dumps(bstack1lll1ll11_opy_))
    else:
        bstack1lll1l11l1_opy_ = bstack11ll11_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ⌹") + urllib.parse.quote(json.dumps(bstack1lll1ll11_opy_))
    browser = self.connect(bstack1lll1l11l1_opy_)
    return browser
def bstack11ll111l_opy_():
    global bstack1ll111ll11_opy_
    global bstack1lll11l1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1lllll1_opy_
        if not bstack1l1ll111ll1_opy_():
            global bstack1ll11ll1l1_opy_
            if not bstack1ll11ll1l1_opy_:
                from bstack_utils.helper import bstack1ll1111l_opy_, bstack1l111ll1ll_opy_
                bstack1ll11ll1l1_opy_ = bstack1ll1111l_opy_()
                bstack1l111ll1ll_opy_(bstack1lll11l1ll_opy_)
            BrowserType.connect = bstack1l1lllll1_opy_
            return
        BrowserType.launch = bstack1l1ll1l1ll_opy_
        bstack1ll111ll11_opy_ = True
    except Exception as e:
        pass
def bstack1llll1ll1ll1_opy_():
    global CONFIG
    global bstack1ll1lllll1_opy_
    global bstack11lll111ll_opy_
    global bstack11llllll11_opy_
    global bstack111lll1ll_opy_
    global bstack11lllll11l_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ⌺")))
    bstack1ll1lllll1_opy_ = eval(os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⌻")))
    bstack11lll111ll_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ⌼"))
    bstack11l11l111l_opy_(CONFIG, bstack1ll1lllll1_opy_)
    bstack11lllll11l_opy_ = bstack1111l1ll1_opy_.bstack1lll11l1_opy_(CONFIG, bstack11lllll11l_opy_)
    if cli.bstack1l11111lll_opy_():
        bstack11111l11l_opy_.invoke(bstack11l11l1l_opy_.CONNECT, bstack11ll1111ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⌽"), bstack11ll11_opy_ (u"࠭࠰ࠨ⌾")))
        cli.bstack1ll1lll1ll1_opy_(cli_context.platform_index)
        cli.bstack1ll1lll11l1_opy_(bstack11ll11l111_opy_(bstack11lll111ll_opy_, CONFIG), cli_context.platform_index, bstack1ll11111l_opy_)
        cli.bstack1ll1lll111l_opy_()
        logger.debug(bstack11ll11_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⌿") + str(cli_context.platform_index) + bstack11ll11_opy_ (u"ࠣࠤ⍀"))
        return # skip all existing bstack1llll1l11ll1_opy_
    global bstack1l1llll1_opy_
    global bstack11llll1l_opy_
    global bstack1ll1l1lll1_opy_
    global bstack111ll1l1_opy_
    global bstack11l1l1ll1l_opy_
    global bstack11l11l1l1l_opy_
    global bstack1ll1111ll1_opy_
    global bstack11lllllll_opy_
    global bstack11ll11111l_opy_
    global bstack1lll11ll1_opy_
    global bstack11l111l1_opy_
    global bstack1ll111ll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1llll1_opy_ = webdriver.Remote.__init__
        bstack11llll1l_opy_ = WebDriver.quit
        bstack1ll1111ll1_opy_ = WebDriver.close
        bstack11lllllll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⍁") in CONFIG or bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⍂") in CONFIG) and bstack1111llll1_opy_():
        if bstack1lll1ll1_opy_() < version.parse(bstack1lll111ll_opy_):
            logger.error(bstack11ll1l11ll_opy_.format(bstack1lll1ll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11ll11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⍃")) and callable(getattr(RemoteConnection, bstack11ll11_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⍄"))):
                    bstack11ll11111l_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack11ll11111l_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11ll1111l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll11ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack11l111l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11ll1l1l1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll111ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ⍅"))
    bstack11llllll11_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⍆"), {}).get(bstack11ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⍇"))
    bstack111lll1ll_opy_ = True
    bstack1ll1ll111l_opy_(bstack11l11l1lll_opy_)
if (bstack11l1l11l1l1_opy_()):
    bstack1llll1ll1ll1_opy_()
@bstack111l1lll11_opy_(class_method=False)
def bstack1llll1ll11l1_opy_(hook_name, event, bstack1l11111llll_opy_=None):
    if hook_name not in [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⍈"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⍉"), bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⍊"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⍋"), bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⍌"), bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⍍"), bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⍎"), bstack11ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ⍏")]:
        return
    node = store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⍐")]
    if hook_name in [bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⍑"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⍒")]:
        node = store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ⍓")]
    elif hook_name in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⍔"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⍕")]:
        node = store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⍖")]
    hook_type = bstack11111ll1111_opy_(hook_name)
    if event == bstack11ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⍗"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_[hook_type], bstack1ll1l1lll11_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l1lll_opy_ = {
            bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⍘"): uuid,
            bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⍙"): bstack1l11l11ll_opy_(),
            bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⍚"): bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⍛"),
            bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⍜"): hook_type,
            bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⍝"): hook_name
        }
        store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⍞")].append(uuid)
        bstack1llll1lll1ll_opy_ = node.nodeid
        if hook_type == bstack11ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⍟"):
            if not _1111lll111_opy_.get(bstack1llll1lll1ll_opy_, None):
                _1111lll111_opy_[bstack1llll1lll1ll_opy_] = {bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⍠"): []}
            _1111lll111_opy_[bstack1llll1lll1ll_opy_][bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⍡")].append(bstack111l1l1lll_opy_[bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⍢")])
        _1111lll111_opy_[bstack1llll1lll1ll_opy_ + bstack11ll11_opy_ (u"ࠨ࠯ࠪ⍣") + hook_name] = bstack111l1l1lll_opy_
        bstack1llll1ll1l11_opy_(node, bstack111l1l1lll_opy_, bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⍤"))
    elif event == bstack11ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⍥"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll11111l_opy_[hook_type], bstack1ll1l1lll11_opy_.POST, node, None, bstack1l11111llll_opy_)
            return
        bstack111ll11lll_opy_ = node.nodeid + bstack11ll11_opy_ (u"ࠫ࠲࠭⍦") + hook_name
        _1111lll111_opy_[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⍧")] = bstack1l11l11ll_opy_()
        bstack1llll1l1lll1_opy_(_1111lll111_opy_[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⍨")])
        bstack1llll1ll1l11_opy_(node, _1111lll111_opy_[bstack111ll11lll_opy_], bstack11ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⍩"), bstack1llll1l111l1_opy_=bstack1l11111llll_opy_)
def bstack1llll1ll111l_opy_():
    global bstack1llll1l11l1l_opy_
    if bstack111ll11l_opy_():
        bstack1llll1l11l1l_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⍪")
    else:
        bstack1llll1l11l1l_opy_ = bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⍫")
@bstack1l1l1l1ll_opy_.bstack1lllll1ll11l_opy_
def bstack1llll1l11lll_opy_():
    bstack1llll1ll111l_opy_()
    if cli.is_running():
        try:
            bstack111lll11l11_opy_(bstack1llll1ll11l1_opy_)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⍬").format(e))
        return
    if bstack1111llll1_opy_():
        bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
        bstack11ll11_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ⍭")
        if bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⍮")):
            if CONFIG.get(bstack11ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⍯")) is not None and int(CONFIG[bstack11ll11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⍰")]) > 1:
                bstack1l1l11l111_opy_(bstack1l1l1l1l1l_opy_)
            return
        bstack1l1l11l111_opy_(bstack1l1l1l1l1l_opy_)
    try:
        bstack111lll11l11_opy_(bstack1llll1ll11l1_opy_)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⍱").format(e))
bstack1llll1l11lll_opy_()