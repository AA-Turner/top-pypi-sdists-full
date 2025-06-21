# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11ll1ll1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11ll1l1ll_opy_, bstack1l1ll1ll1_opy_, update, bstack1111l1ll_opy_,
                                       bstack1lll1l111_opy_, bstack11l111l111_opy_, bstack1111lll11_opy_, bstack1ll1ll111_opy_,
                                       bstack1l11l11l11_opy_, bstack1l1ll1111l_opy_, bstack1l111l111_opy_,
                                       bstack11lllll1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11111l1_opy_)
from browserstack_sdk.bstack11lll1111l_opy_ import bstack1l1l1l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1llll1l111_opy_
from bstack_utils.capture import bstack111llll11l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll1ll1l_opy_, bstack11ll1ll11l_opy_, bstack1ll1ll1l1l_opy_, \
    bstack11111llll_opy_
from bstack_utils.helper import bstack111l1ll1l_opy_, bstack11l11l11l11_opy_, bstack111ll111l1_opy_, bstack11l11l11l1_opy_, bstack1l1lll11ll1_opy_, bstack1lllll1l1l_opy_, \
    bstack11l11ll11ll_opy_, \
    bstack11l1l11llll_opy_, bstack11lll1l11l_opy_, bstack11l111llll_opy_, bstack11l11l11lll_opy_, bstack11lll111l1_opy_, Notset, \
    bstack111l1l1l1_opy_, bstack11l11ll11l1_opy_, bstack11l111l1l1l_opy_, Result, bstack11l1111l111_opy_, bstack11l11l1l1ll_opy_, bstack111ll11111_opy_, \
    bstack11lll111_opy_, bstack1ll1ll11ll_opy_, bstack1lll1l1lll_opy_, bstack11l11llllll_opy_
from bstack_utils.bstack111lll1l1l1_opy_ import bstack111lll111l1_opy_
from bstack_utils.messages import bstack1ll11l1lll_opy_, bstack11l111l1l_opy_, bstack1l1111l1ll_opy_, bstack1l11l1ll_opy_, bstack1l1ll111l_opy_, \
    bstack1llll1ll11_opy_, bstack1llllll11l_opy_, bstack11ll1ll1ll_opy_, bstack1ll1llll_opy_, bstack1ll1lllll1_opy_, \
    bstack1lll1llll_opy_, bstack1l1ll11l1l_opy_
from bstack_utils.proxy import bstack11l1111ll1_opy_, bstack1ll1l11lll_opy_
from bstack_utils.bstack1l11lllll_opy_ import bstack11111ll1ll1_opy_, bstack11111ll111l_opy_, bstack11111l1l1l1_opy_, bstack11111ll1l1l_opy_, \
    bstack11111ll1l11_opy_, bstack11111l1lll1_opy_, bstack11111l1l11l_opy_, bstack1l1l1lll11_opy_, bstack11111l1l1ll_opy_
from bstack_utils.bstack111ll1111_opy_ import bstack11l1l11111_opy_
from bstack_utils.bstack1111ll1l_opy_ import bstack11l11ll1_opy_, bstack1ll1l11l11_opy_, bstack11ll11l1l_opy_, \
    bstack1111ll1ll_opy_, bstack11llll1l_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack111lllll1l_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack11l1l1l1ll_opy_
import bstack_utils.accessibility as bstack1ll1l11ll_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack111llllll_opy_
from bstack_utils.bstack1111ll1l1_opy_ import bstack1111ll1l1_opy_
from bstack_utils.bstack1llll1llll_opy_ import bstack1ll11111l_opy_
from browserstack_sdk.__init__ import bstack11ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll1l1111_opy_
from browserstack_sdk.sdk_cli.bstack11lll11l1l_opy_ import bstack11lll11l1l_opy_, bstack1l11ll11l1_opy_, bstack1111l111l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l1111l1l1l_opy_, bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11lll11l1l_opy_ import bstack11lll11l1l_opy_, bstack1l11ll11l1_opy_, bstack1111l111l_opy_
bstack11lll111ll_opy_ = None
bstack1l1l11ll1_opy_ = None
bstack1ll1ll111l_opy_ = None
bstack11l11111l1_opy_ = None
bstack11l1ll1l1l_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack1l1l1ll1l1_opy_ = None
bstack1l11l11ll_opy_ = None
bstack11ll11l111_opy_ = None
bstack11l1l11l11_opy_ = None
bstack1llll111ll_opy_ = None
bstack1111l1ll1_opy_ = None
bstack11ll1lll1_opy_ = None
bstack11l11llll1_opy_ = bstack1l1l1l1_opy_ (u"ࠪࠫℒ")
CONFIG = {}
bstack11ll1lll1l_opy_ = False
bstack1l1lll11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠫࠬℓ")
bstack1ll1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭℔")
bstack1l1l111111_opy_ = False
bstack1lll1l11l1_opy_ = []
bstack11l1l1l1l1_opy_ = bstack1ll1ll1l_opy_
bstack1llll1llll1l_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ℕ")
bstack11lll1lll1_opy_ = {}
bstack11llll11_opy_ = None
bstack1lll111l1_opy_ = False
logger = bstack1llll1l111_opy_.get_logger(__name__, bstack11l1l1l1l1_opy_)
store = {
    bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ№"): []
}
bstack1llll1lll11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111ll11l11_opy_ = {}
current_test_uuid = None
cli_context = bstack1l1111l1l1l_opy_(
    test_framework_name=bstack1ll1lll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ℗")] if bstack11lll111l1_opy_() else bstack1ll1lll11_opy_[bstack1l1l1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩ℘")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l11l1lll_opy_(page, bstack1lll1l11l_opy_):
    try:
        page.evaluate(bstack1l1l1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦℙ"),
                      bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨℚ") + json.dumps(
                          bstack1lll1l11l_opy_) + bstack1l1l1l1_opy_ (u"ࠧࢃࡽࠣℛ"))
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦℜ"), e)
def bstack1ll1l111l1_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣℝ"), bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭℞") + json.dumps(
            message) + bstack1l1l1l1_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ℟") + json.dumps(level) + bstack1l1l1l1_opy_ (u"ࠪࢁࢂ࠭℠"))
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ℡"), e)
def pytest_configure(config):
    global bstack1l1lll11l1_opy_
    global CONFIG
    bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
    config.args = bstack11l1l1l1ll_opy_.bstack1lllll11111l_opy_(config.args)
    bstack11lll11111_opy_.bstack111l11l1_opy_(bstack1lll1l1lll_opy_(config.getoption(bstack1l1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ™"))))
    try:
        bstack1llll1l111_opy_.bstack111ll1l1l11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11lll11l1l_opy_.invoke(bstack1l11ll11l1_opy_.CONNECT, bstack1111l111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭℣"), bstack1l1l1l1_opy_ (u"ࠧ࠱ࠩℤ")))
        config = json.loads(os.environ.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢ℥"), bstack1l1l1l1_opy_ (u"ࠤࡾࢁࠧΩ")))
        cli.bstack1lll11l111l_opy_(bstack11l111llll_opy_(bstack1l1lll11l1_opy_, CONFIG), cli_context.platform_index, bstack1111l1ll_opy_)
    if cli.bstack1ll1lllll1l_opy_(bstack1llll1l1111_opy_):
        cli.bstack1llll11ll11_opy_()
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ℧") + str(cli_context.platform_index) + bstack1l1l1l1_opy_ (u"ࠦࠧℨ"))
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.BEFORE_ALL, bstack1lll1lll111_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1l1l1_opy_ (u"ࠧࡽࡨࡦࡰࠥ℩"), None)
    if cli.is_running() and when == bstack1l1l1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦK"):
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.LOG_REPORT, bstack1lll1lll111_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1l1l1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧÅ"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥℬ")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣℭ"), bstack1l1l1l1_opy_ (u"ࠥࡿࢂࠨ℮")))
            if bstack1ll11111l_opy_.bstack1ll11l11l1_opy_(config):
                bstack1111l1lll11_opy_ = bstack1ll11111l_opy_.bstack1l11ll1l1l_opy_(config)
                if item.execution_count > bstack1111l1lll11_opy_:
                    print(bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡴࡨࡸࡷ࡯ࡥࡴ࠼ࠣࠫℯ"), report.nodeid, os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪℰ")))
                    bstack1ll11111l_opy_.bstack111l11ll1ll_opy_(report.nodeid)
            else:
                print(bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥ࠭ℱ"), report.nodeid, os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬℲ")))
                bstack1ll11111l_opy_.bstack111l11ll1ll_opy_(report.nodeid)
        else:
            print(bstack1l1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࠦࡰࡢࡵࡶࡩࡩࡀࠠࠨℳ"), report.nodeid, os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧℴ")))
    if cli.is_running():
        if when == bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤℵ"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.BEFORE_EACH, bstack1lll1lll111_opy_.POST, item, call, outcome)
        elif when == bstack1l1l1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤℶ"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.LOG_REPORT, bstack1lll1lll111_opy_.POST, item, call, outcome)
        elif when == bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢℷ"):
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.AFTER_EACH, bstack1lll1lll111_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llll1ll11l1_opy_
    skipSessionName = item.config.getoption(bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨℸ"))
    plugins = item.config.getoption(bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣℹ"))
    report = outcome.get_result()
    os.environ[bstack1l1l1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ℺")] = report.nodeid
    bstack1llll1l1l11l_opy_(item, call, report)
    if bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢ℻") not in plugins or bstack11lll111l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l1l1_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦℼ"), None)
    page = getattr(item, bstack1l1l1l1_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥℽ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll1l1ll1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll1l1l1ll_opy_(item, report, summary, skipSessionName)
def bstack1llll1l1ll1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫℾ") and report.skipped:
        bstack11111l1l1ll_opy_(report)
    if report.when in [bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧℿ"), bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ⅀")]:
        return
    if not bstack1l1lll11ll1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭⅁")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ⅂") + json.dumps(
                    report.nodeid) + bstack1l1l1l1_opy_ (u"ࠪࢁࢂ࠭⅃"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⅄")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧⅅ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣⅆ")))
    bstack111l1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠢࠣⅇ")
    bstack11111l1l1ll_opy_(report)
    if not passed:
        try:
            bstack111l1l111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣⅈ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111l1l111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦⅉ")))
        bstack111l1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠥࠦ⅊")
        if not passed:
            try:
                bstack111l1l111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ⅋").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111l1l111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ⅌")
                    + json.dumps(bstack1l1l1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢ⅍"))
                    + bstack1l1l1l1_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥⅎ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭⅏")
                    + json.dumps(str(bstack111l1l111_opy_))
                    + bstack1l1l1l1_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ⅐")
                )
        except Exception as e:
            summary.append(bstack1l1l1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣ⅑").format(e))
def bstack1llll1ll1l1l_opy_(test_name, error_message):
    try:
        bstack1llll1l111ll_opy_ = []
        bstack1ll111l111_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⅒"), bstack1l1l1l1_opy_ (u"ࠬ࠶ࠧ⅓"))
        bstack1ll11ll1_opy_ = {bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⅔"): test_name, bstack1l1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⅕"): error_message, bstack1l1l1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ⅖"): bstack1ll111l111_opy_}
        bstack1llll1llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ⅗"))
        if os.path.exists(bstack1llll1llllll_opy_):
            with open(bstack1llll1llllll_opy_) as f:
                bstack1llll1l111ll_opy_ = json.load(f)
        bstack1llll1l111ll_opy_.append(bstack1ll11ll1_opy_)
        with open(bstack1llll1llllll_opy_, bstack1l1l1l1_opy_ (u"ࠪࡻࠬ⅘")) as f:
            json.dump(bstack1llll1l111ll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩ⅙") + str(e))
def bstack1llll1l1l1ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⅚"), bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ⅛")]:
        return
    if (str(skipSessionName).lower() != bstack1l1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ⅜")):
        bstack11l11l1lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⅝")))
    bstack111l1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠤࠥ⅞")
    bstack11111l1l1ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111l1l111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⅟").format(e)
                )
        try:
            if passed:
                bstack11llll1l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪⅠ"), None), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧⅡ"))
            else:
                error_message = bstack1l1l1l1_opy_ (u"࠭ࠧⅢ")
                if bstack111l1l111_opy_:
                    bstack1ll1l111l1_opy_(item._page, str(bstack111l1l111_opy_), bstack1l1l1l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨⅣ"))
                    bstack11llll1l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧⅤ"), None), bstack1l1l1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤⅥ"), str(bstack111l1l111_opy_))
                    error_message = str(bstack111l1l111_opy_)
                else:
                    bstack11llll1l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩⅦ"), None), bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦⅧ"))
                bstack1llll1ll1l1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l1l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤⅨ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1l1l1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥⅩ"), default=bstack1l1l1l1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨⅪ"), help=bstack1l1l1l1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢⅫ"))
    parser.addoption(bstack1l1l1l1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣⅬ"), default=bstack1l1l1l1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤⅭ"), help=bstack1l1l1l1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥⅮ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l1l1_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢⅯ"), action=bstack1l1l1l1_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧⅰ"), default=bstack1l1l1l1_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢⅱ"),
                         help=bstack1l1l1l1_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢⅲ"))
def bstack111ll1l1l1_opy_(log):
    if not (log[bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪⅳ")] and log[bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⅴ")].strip()):
        return
    active = bstack111ll1l11l_opy_()
    log = {
        bstack1l1l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪⅵ"): log[bstack1l1l1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫⅶ")],
        bstack1l1l1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩⅷ"): bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"࡛ࠧࠩⅸ"),
        bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩⅹ"): log[bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪⅺ")],
    }
    if active:
        if active[bstack1l1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨⅻ")] == bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩⅼ"):
            log[bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅽ")] = active[bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ⅾ")]
        elif active[bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬⅿ")] == bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ↀ"):
            log[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩↁ")] = active[bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪↂ")]
    bstack111llllll_opy_.bstack1111l1111_opy_([log])
def bstack111ll1l11l_opy_():
    if len(store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨↃ")]) > 0 and store[bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩↄ")][-1]:
        return {
            bstack1l1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫↅ"): bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬↆ"),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨↇ"): store[bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ↈ")][-1]
        }
    if store.get(bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ↉"), None):
        return {
            bstack1l1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ↊"): bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ↋"),
            bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭↌"): store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ↍")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.INIT_TEST, bstack1lll1lll111_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.INIT_TEST, bstack1lll1lll111_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llll1ll1111_opy_ = True
        bstack1l111lll11_opy_ = bstack1ll1l11ll_opy_.bstack11lll1llll_opy_(bstack11l1l11llll_opy_(item.own_markers))
        if not cli.bstack1ll1lllll1l_opy_(bstack1llll1l1111_opy_):
            item._a11y_test_case = bstack1l111lll11_opy_
            if bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ↎"), None):
                driver = getattr(item, bstack1l1l1l1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ↏"), None)
                item._a11y_started = bstack1ll1l11ll_opy_.bstack1l1l1l111l_opy_(driver, bstack1l111lll11_opy_)
        if not bstack111llllll_opy_.on() or bstack1llll1llll1l_opy_ != bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ←"):
            return
        global current_test_uuid #, bstack111lll1lll_opy_
        bstack111l11l11l_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ↑"): uuid4().__str__(),
            bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ→"): bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"࡚࠭ࠨ↓")
        }
        current_test_uuid = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↔")]
        store[bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ↕")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ↖")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111ll11l11_opy_[item.nodeid] = {**_111ll11l11_opy_[item.nodeid], **bstack111l11l11l_opy_}
        bstack1llll1l1lll1_opy_(item, _111ll11l11_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ↗"))
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭↘"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ↙")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.BEFORE_EACH, bstack1lll1lll111_opy_.PRE, item, bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ↚"))
    if bstack1ll11111l_opy_.bstack111l11llll1_opy_():
            bstack1llll1llll11_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡢࡵࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦ↛")
            logger.error(bstack1llll1llll11_opy_)
            bstack111l11l11l_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↜"): uuid4().__str__(),
                bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭↝"): bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬ↞"),
                bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ↟"): bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠬࡠࠧ↠"),
                bstack1l1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭↡"): bstack1l1l1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ↢"),
                bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ↣"): bstack1llll1llll11_opy_,
                bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ↤"): [],
                bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ↥"): []
            }
            bstack1llll1l1lll1_opy_(item, bstack111l11l11l_opy_, bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ↦"))
            pytest.skip(bstack1llll1llll11_opy_)
            return # skip all existing bstack1llll1ll11l1_opy_
    global bstack1llll1lll11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11l11lll_opy_():
        atexit.register(bstack1l1llll1l1_opy_)
        if not bstack1llll1lll11l_opy_:
            try:
                bstack1llll1ll111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l11llllll_opy_():
                    bstack1llll1ll111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1ll111l_opy_:
                    signal.signal(s, bstack1llll1l11l11_opy_)
                bstack1llll1lll11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ↧") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111ll1ll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭↨")
    try:
        if not bstack111llllll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11l11l_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↩"): uuid,
            bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ↪"): bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠩ࡝ࠫ↫"),
            bstack1l1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ↬"): bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ↭"),
            bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ↮"): bstack1l1l1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ↯"),
            bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ↰"): bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ↱")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭↲")] = item
        store[bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ↳")] = [uuid]
        if not _111ll11l11_opy_.get(item.nodeid, None):
            _111ll11l11_opy_[item.nodeid] = {bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ↴"): [], bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ↵"): []}
        _111ll11l11_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ↶")].append(bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↷")])
        _111ll11l11_opy_[item.nodeid + bstack1l1l1l1_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ↸")] = bstack111l11l11l_opy_
        bstack1llll1ll1l11_opy_(item, bstack111l11l11l_opy_, bstack1l1l1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ↹"))
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭↺"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.AFTER_EACH, bstack1lll1lll111_opy_.PRE, item, bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭↻"))
        return # skip all existing bstack1llll1ll11l1_opy_
    try:
        global bstack11lll1lll1_opy_
        bstack1ll111l111_opy_ = 0
        if bstack1l1l111111_opy_ is True:
            bstack1ll111l111_opy_ = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ↼")))
        if bstack11lllll1_opy_.bstack1l111l11_opy_() == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ↽"):
            if bstack11lllll1_opy_.bstack111l1ll11_opy_() == bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ↾"):
                bstack1llll1ll1ll1_opy_ = bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ↿"), None)
                bstack1l1ll111ll_opy_ = bstack1llll1ll1ll1_opy_ + bstack1l1l1l1_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧ⇀")
                driver = getattr(item, bstack1l1l1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⇁"), None)
                bstack11l1111l_opy_ = getattr(item, bstack1l1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⇂"), None)
                bstack1ll1l1l11l_opy_ = getattr(item, bstack1l1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⇃"), None)
                PercySDK.screenshot(driver, bstack1l1ll111ll_opy_, bstack11l1111l_opy_=bstack11l1111l_opy_, bstack1ll1l1l11l_opy_=bstack1ll1l1l11l_opy_, bstack1l111l1lll_opy_=bstack1ll111l111_opy_)
        if not cli.bstack1ll1lllll1l_opy_(bstack1llll1l1111_opy_):
            if getattr(item, bstack1l1l1l1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭⇄"), False):
                bstack1l1l1l11_opy_.bstack11l1llll1l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⇅"), None), bstack11lll1lll1_opy_, logger, item)
        if not bstack111llllll_opy_.on():
            return
        bstack111l11l11l_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⇆"): uuid4().__str__(),
            bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⇇"): bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬ⇈"),
            bstack1l1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⇉"): bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⇊"),
            bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⇋"): bstack1l1l1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⇌"),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⇍"): bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⇎")
        }
        _111ll11l11_opy_[item.nodeid + bstack1l1l1l1_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⇏")] = bstack111l11l11l_opy_
        bstack1llll1ll1l11_opy_(item, bstack111l11l11l_opy_, bstack1l1l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⇐"))
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫ⇑"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111ll1l1l_opy_(fixturedef.argname):
        store[bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ⇒")] = request.node
    elif bstack11111ll1l11_opy_(fixturedef.argname):
        store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ⇓")] = request.node
    if not bstack111llllll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll111_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll111_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1ll11l1_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll111_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll111_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1ll11l1_opy_
    try:
        fixture = {
            bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭⇔"): fixturedef.argname,
            bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⇕"): bstack11l11ll11ll_opy_(outcome),
            bstack1l1l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⇖"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⇗")]
        if not _111ll11l11_opy_.get(current_test_item.nodeid, None):
            _111ll11l11_opy_[current_test_item.nodeid] = {bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⇘"): []}
        _111ll11l11_opy_[current_test_item.nodeid][bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⇙")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ⇚"), str(err))
if bstack11lll111l1_opy_() and bstack111llllll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.STEP, bstack1lll1lll111_opy_.PRE, request, step)
            return
        try:
            _111ll11l11_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⇛")].bstack1l11111l_opy_(id(step))
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ⇜"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.STEP, bstack1lll1lll111_opy_.POST, request, step, exception)
            return
        try:
            _111ll11l11_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⇝")].bstack111llll1ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ⇞"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.STEP, bstack1lll1lll111_opy_.POST, request, step)
            return
        try:
            bstack111lll1l1l_opy_: bstack111lllll1l_opy_ = _111ll11l11_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⇟")]
            bstack111lll1l1l_opy_.bstack111llll1ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ⇠"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1llll1l_opy_
        try:
            if not bstack111llllll_opy_.on() or bstack1llll1llll1l_opy_ != bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⇡"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.PRE, request, feature, scenario)
                return
            driver = bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ⇢"), None)
            if not _111ll11l11_opy_.get(request.node.nodeid, None):
                _111ll11l11_opy_[request.node.nodeid] = {}
            bstack111lll1l1l_opy_ = bstack111lllll1l_opy_.bstack11111111l11_opy_(
                scenario, feature, request.node,
                name=bstack11111l1lll1_opy_(request.node, scenario),
                started_at=bstack1lllll1l1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ⇣"),
                tags=bstack11111l1l11l_opy_(feature, scenario),
                bstack111ll1lll1_opy_=bstack111llllll_opy_.bstack111lll1l11_opy_(driver) if driver and driver.session_id else {}
            )
            _111ll11l11_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⇤")] = bstack111lll1l1l_opy_
            bstack1llll1l1l111_opy_(bstack111lll1l1l_opy_.uuid)
            bstack111llllll_opy_.bstack111ll1ll1l_opy_(bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⇥"), bstack111lll1l1l_opy_)
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ⇦"), str(err))
def bstack1llll1lllll1_opy_(bstack111lll11ll_opy_):
    if bstack111lll11ll_opy_ in store[bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⇧")]:
        store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇨")].remove(bstack111lll11ll_opy_)
def bstack1llll1l1l111_opy_(test_uuid):
    store[bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⇩")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111llllll_opy_.bstack1lllll1lll11_opy_
def bstack1llll1l1l11l_opy_(item, call, report):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡴࡷࠫ⇪"))
    global bstack1llll1llll1l_opy_
    bstack11ll1llll1_opy_ = bstack1lllll1l1l_opy_()
    if hasattr(report, bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡵࡰࠨ⇫")):
        bstack11ll1llll1_opy_ = bstack11l1111l111_opy_(report.stop)
    elif hasattr(report, bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ⇬")):
        bstack11ll1llll1_opy_ = bstack11l1111l111_opy_(report.start)
    try:
        if getattr(report, bstack1l1l1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪ⇭"), bstack1l1l1l1_opy_ (u"࠭ࠧ⇮")) == bstack1l1l1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⇯"):
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ⇰").format(getattr(report, bstack1l1l1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⇱"), bstack1l1l1l1_opy_ (u"ࠪࠫ⇲")).__str__(), bstack1llll1llll1l_opy_))
            if bstack1llll1llll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⇳"):
                _111ll11l11_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⇴")] = bstack11ll1llll1_opy_
                bstack1llll1l1lll1_opy_(item, _111ll11l11_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⇵"), report, call)
                store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⇶")] = None
            elif bstack1llll1llll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ⇷"):
                bstack111lll1l1l_opy_ = _111ll11l11_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⇸")]
                bstack111lll1l1l_opy_.set(hooks=_111ll11l11_opy_[item.nodeid].get(bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⇹"), []))
                exception, bstack111lll1ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll1ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1l1l1_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪ⇺"), bstack1l1l1l1_opy_ (u"ࠬ࠭⇻"))]
                bstack111lll1l1l_opy_.stop(time=bstack11ll1llll1_opy_, result=Result(result=getattr(report, bstack1l1l1l1_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⇼"), bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⇽")), exception=exception, bstack111lll1ll1_opy_=bstack111lll1ll1_opy_))
                bstack111llllll_opy_.bstack111ll1ll1l_opy_(bstack1l1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⇾"), _111ll11l11_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⇿")])
        elif getattr(report, bstack1l1l1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ∀"), bstack1l1l1l1_opy_ (u"ࠫࠬ∁")) in [bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ∂"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ∃")]:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ∄").format(getattr(report, bstack1l1l1l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭∅"), bstack1l1l1l1_opy_ (u"ࠩࠪ∆")).__str__(), bstack1llll1llll1l_opy_))
            bstack111lll1111_opy_ = item.nodeid + bstack1l1l1l1_opy_ (u"ࠪ࠱ࠬ∇") + getattr(report, bstack1l1l1l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ∈"), bstack1l1l1l1_opy_ (u"ࠬ࠭∉"))
            if getattr(report, bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ∊"), False):
                hook_type = bstack1l1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ∋") if getattr(report, bstack1l1l1l1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭∌"), bstack1l1l1l1_opy_ (u"ࠩࠪ∍")) == bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ∎") else bstack1l1l1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ∏")
                _111ll11l11_opy_[bstack111lll1111_opy_] = {
                    bstack1l1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ∐"): uuid4().__str__(),
                    bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ∑"): bstack11ll1llll1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ−"): hook_type
                }
            _111ll11l11_opy_[bstack111lll1111_opy_][bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭∓")] = bstack11ll1llll1_opy_
            bstack1llll1lllll1_opy_(_111ll11l11_opy_[bstack111lll1111_opy_][bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ∔")])
            bstack1llll1ll1l11_opy_(item, _111ll11l11_opy_[bstack111lll1111_opy_], bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ∕"), report, call)
            if getattr(report, bstack1l1l1l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ∖"), bstack1l1l1l1_opy_ (u"ࠬ࠭∗")) == bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ∘"):
                if getattr(report, bstack1l1l1l1_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ∙"), bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ√")) == bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ∛"):
                    bstack111l11l11l_opy_ = {
                        bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ∜"): uuid4().__str__(),
                        bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ∝"): bstack1lllll1l1l_opy_(),
                        bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ∞"): bstack1lllll1l1l_opy_()
                    }
                    _111ll11l11_opy_[item.nodeid] = {**_111ll11l11_opy_[item.nodeid], **bstack111l11l11l_opy_}
                    bstack1llll1l1lll1_opy_(item, _111ll11l11_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ∟"))
                    bstack1llll1l1lll1_opy_(item, _111ll11l11_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ∠"), report, call)
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭∡"), str(err))
def bstack1llll1l11ll1_opy_(test, bstack111l11l11l_opy_, result=None, call=None, bstack11lll1ll11_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lll1l1l_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ∢"): bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ∣")],
        bstack1l1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ∤"): bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ∥"),
        bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ∦"): test.name,
        bstack1l1l1l1_opy_ (u"ࠧࡣࡱࡧࡽࠬ∧"): {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭∨"): bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ∩"),
            bstack1l1l1l1_opy_ (u"ࠪࡧࡴࡪࡥࠨ∪"): inspect.getsource(test.obj)
        },
        bstack1l1l1l1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ∫"): test.name,
        bstack1l1l1l1_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ∬"): test.name,
        bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭∭"): bstack11l1l1l1ll_opy_.bstack1111llllll_opy_(test),
        bstack1l1l1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ∮"): file_path,
        bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ∯"): file_path,
        bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ∰"): bstack1l1l1l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ∱"),
        bstack1l1l1l1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ∲"): file_path,
        bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ∳"): bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ∴")],
        bstack1l1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ∵"): bstack1l1l1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ∶"),
        bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ∷"): {
            bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧ∸"): test.nodeid
        },
        bstack1l1l1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩ∹"): bstack11l1l11llll_opy_(test.own_markers)
    }
    if bstack11lll1ll11_opy_ in [bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭∺"), bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ∻")]:
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ∼")] = {
            bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ∽"): bstack111l11l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ∾"), [])
        }
    if bstack11lll1ll11_opy_ == bstack1l1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ∿"):
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ≀")] = bstack1l1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭≁")
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ≂")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭≃")]
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭≄")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ≅")]
    if result:
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ≆")] = result.outcome
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ≇")] = result.duration * 1000
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≈")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≉")]
        if result.failed:
            bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭≊")] = bstack111llllll_opy_.bstack11111l11ll_opy_(call.excinfo.typename)
            bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ≋")] = bstack111llllll_opy_.bstack1lllll1ll1l1_opy_(call.excinfo, result)
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ≌")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ≍")]
    if outcome:
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ≎")] = bstack11l11ll11ll_opy_(outcome)
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭≏")] = 0
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ≐")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ≑")]
        if bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≒")] == bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ≓"):
            bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ≔")] = bstack1l1l1l1_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ≕")  # bstack1llll1lll1l1_opy_
            bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭≖")] = [{bstack1l1l1l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ≗"): [bstack1l1l1l1_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ≘")]}]
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ≙")] = bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ≚")]
    return bstack111lll1l1l_opy_
def bstack1llll1l1ll11_opy_(test, bstack111l1ll111_opy_, bstack11lll1ll11_opy_, result, call, outcome, bstack1llll1l1l1l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭≛")]
    hook_name = bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ≜")]
    hook_data = {
        bstack1l1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ≝"): bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ≞")],
        bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ≟"): bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭≠"),
        bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ≡"): bstack1l1l1l1_opy_ (u"ࠪࡿࢂ࠭≢").format(bstack11111ll111l_opy_(hook_name)),
        bstack1l1l1l1_opy_ (u"ࠫࡧࡵࡤࡺࠩ≣"): {
            bstack1l1l1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ≤"): bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭≥"),
            bstack1l1l1l1_opy_ (u"ࠧࡤࡱࡧࡩࠬ≦"): None
        },
        bstack1l1l1l1_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ≧"): test.name,
        bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ≨"): bstack11l1l1l1ll_opy_.bstack1111llllll_opy_(test, hook_name),
        bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭≩"): file_path,
        bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭≪"): file_path,
        bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ≫"): bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ≬"),
        bstack1l1l1l1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ≭"): file_path,
        bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ≮"): bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭≯")],
        bstack1l1l1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭≰"): bstack1l1l1l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭≱") if bstack1llll1llll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ≲") else bstack1l1l1l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭≳"),
        bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ≴"): hook_type
    }
    bstack1llllllll1ll_opy_ = bstack111l1111ll_opy_(_111ll11l11_opy_.get(test.nodeid, None))
    if bstack1llllllll1ll_opy_:
        hook_data[bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭≵")] = bstack1llllllll1ll_opy_
    if result:
        hook_data[bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ≶")] = result.outcome
        hook_data[bstack1l1l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ≷")] = result.duration * 1000
        hook_data[bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≸")] = bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≹")]
        if result.failed:
            hook_data[bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ≺")] = bstack111llllll_opy_.bstack11111l11ll_opy_(call.excinfo.typename)
            hook_data[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ≻")] = bstack111llllll_opy_.bstack1lllll1ll1l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ≼")] = bstack11l11ll11ll_opy_(outcome)
        hook_data[bstack1l1l1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ≽")] = 100
        hook_data[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≾")] = bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≿")]
        if hook_data[bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⊀")] == bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⊁"):
            hook_data[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⊂")] = bstack1l1l1l1_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⊃")  # bstack1llll1lll1l1_opy_
            hook_data[bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⊄")] = [{bstack1l1l1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⊅"): [bstack1l1l1l1_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⊆")]}]
    if bstack1llll1l1l1l1_opy_:
        hook_data[bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⊇")] = bstack1llll1l1l1l1_opy_.result
        hook_data[bstack1l1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⊈")] = bstack11l11ll11l1_opy_(bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⊉")], bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊊")])
        hook_data[bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⊋")] = bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⊌")]
        if hook_data[bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⊍")] == bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⊎"):
            hook_data[bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⊏")] = bstack111llllll_opy_.bstack11111l11ll_opy_(bstack1llll1l1l1l1_opy_.exception_type)
            hook_data[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⊐")] = [{bstack1l1l1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⊑"): bstack11l111l1l1l_opy_(bstack1llll1l1l1l1_opy_.exception)}]
    return hook_data
def bstack1llll1l1lll1_opy_(test, bstack111l11l11l_opy_, bstack11lll1ll11_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⊒").format(bstack11lll1ll11_opy_))
    bstack111lll1l1l_opy_ = bstack1llll1l11ll1_opy_(test, bstack111l11l11l_opy_, result, call, bstack11lll1ll11_opy_, outcome)
    driver = getattr(test, bstack1l1l1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⊓"), None)
    if bstack11lll1ll11_opy_ == bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⊔") and driver:
        bstack111lll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ⊕")] = bstack111llllll_opy_.bstack111lll1l11_opy_(driver)
    if bstack11lll1ll11_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⊖"):
        bstack11lll1ll11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⊗")
    bstack1111lll111_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⊘"): bstack11lll1ll11_opy_,
        bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⊙"): bstack111lll1l1l_opy_
    }
    bstack111llllll_opy_.bstack11111111l_opy_(bstack1111lll111_opy_)
    if bstack11lll1ll11_opy_ == bstack1l1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⊚"):
        threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⊛"): bstack1l1l1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⊜")}
    elif bstack11lll1ll11_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⊝"):
        threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⊞"): getattr(result, bstack1l1l1l1_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⊟"), bstack1l1l1l1_opy_ (u"ࠩࠪ⊠"))}
def bstack1llll1ll1l11_opy_(test, bstack111l11l11l_opy_, bstack11lll1ll11_opy_, result=None, call=None, outcome=None, bstack1llll1l1l1l1_opy_=None):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡴࡤࡠࡪࡲࡳࡰࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥ࡮࡯ࡰ࡭ࠣࡨࡦࡺࡡ࠭ࠢࡨࡺࡪࡴࡴࡕࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ⊡").format(bstack11lll1ll11_opy_))
    hook_data = bstack1llll1l1ll11_opy_(test, bstack111l11l11l_opy_, bstack11lll1ll11_opy_, result, call, outcome, bstack1llll1l1l1l1_opy_)
    bstack1111lll111_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⊢"): bstack11lll1ll11_opy_,
        bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ⊣"): hook_data
    }
    bstack111llllll_opy_.bstack11111111l_opy_(bstack1111lll111_opy_)
def bstack111l1111ll_opy_(bstack111l11l11l_opy_):
    if not bstack111l11l11l_opy_:
        return None
    if bstack111l11l11l_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⊤"), None):
        return getattr(bstack111l11l11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⊥")], bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊦"), None)
    return bstack111l11l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⊧"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.LOG, bstack1lll1lll111_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_.LOG, bstack1lll1lll111_opy_.POST, request, caplog)
        return # skip all existing bstack1llll1ll11l1_opy_
    try:
        if not bstack111llllll_opy_.on():
            return
        places = [bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⊨"), bstack1l1l1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⊩"), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⊪")]
        logs = []
        for bstack1llll1lll1ll_opy_ in places:
            records = caplog.get_records(bstack1llll1lll1ll_opy_)
            bstack1llll1l1llll_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⊫") if bstack1llll1lll1ll_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⊬") else bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⊭")
            bstack1llll1ll11ll_opy_ = request.node.nodeid + (bstack1l1l1l1_opy_ (u"ࠩࠪ⊮") if bstack1llll1lll1ll_opy_ == bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⊯") else bstack1l1l1l1_opy_ (u"ࠫ࠲࠭⊰") + bstack1llll1lll1ll_opy_)
            test_uuid = bstack111l1111ll_opy_(_111ll11l11_opy_.get(bstack1llll1ll11ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l11l1l1ll_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1l1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⊱"): bstack11l11l11l11_opy_(record.created).isoformat() + bstack1l1l1l1_opy_ (u"࡚࠭ࠨ⊲"),
                    bstack1l1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⊳"): record.levelname,
                    bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⊴"): record.message,
                    bstack1llll1l1llll_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111llllll_opy_.bstack1111l1111_opy_(logs)
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭⊵"), str(err))
def bstack11l11l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1lll111l1_opy_
    bstack11l1ll1lll_opy_ = bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ⊶"), None) and bstack111l1ll1l_opy_(
            threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⊷"), None)
    bstack11lll11ll_opy_ = getattr(driver, bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⊸"), None) != None and getattr(driver, bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭⊹"), None) == True
    if sequence == bstack1l1l1l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ⊺") and driver != None:
      if not bstack1lll111l1_opy_ and bstack1l1lll11ll1_opy_() and bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⊻") in CONFIG and CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⊼")] == True and bstack1111ll1l1_opy_.bstack11l11lllll_opy_(driver_command) and (bstack11lll11ll_opy_ or bstack11l1ll1lll_opy_) and not bstack1l11111l1_opy_(args):
        try:
          bstack1lll111l1_opy_ = True
          logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ⊽").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ⊾").format(str(err)))
        bstack1lll111l1_opy_ = False
    if sequence == bstack1l1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ⊿"):
        if driver_command == bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ⋀"):
            bstack111llllll_opy_.bstack11llll1111_opy_({
                bstack1l1l1l1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭⋁"): response[bstack1l1l1l1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ⋂")],
                bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⋃"): store[bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⋄")]
            })
def bstack1l1llll1l1_opy_():
    global bstack1lll1l11l1_opy_
    bstack1llll1l111_opy_.bstack1l1l1l1lll_opy_()
    logging.shutdown()
    bstack111llllll_opy_.bstack111l1lllll_opy_()
    for driver in bstack1lll1l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l11l11_opy_(*args):
    global bstack1lll1l11l1_opy_
    bstack111llllll_opy_.bstack111l1lllll_opy_()
    for driver in bstack1lll1l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l11ll1l_opy_, stage=STAGE.bstack1l1lll1lll_opy_, bstack1l11l1l11l_opy_=bstack11llll11_opy_)
def bstack1l11ll1l11_opy_(self, *args, **kwargs):
    bstack11l11ll11l_opy_ = bstack11lll111ll_opy_(self, *args, **kwargs)
    bstack1l1lll111l_opy_ = getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ⋅"), None)
    if bstack1l1lll111l_opy_ and bstack1l1lll111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⋆"), bstack1l1l1l1_opy_ (u"࠭ࠧ⋇")) == bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⋈"):
        bstack111llllll_opy_.bstack1ll111l1ll_opy_(self)
    return bstack11l11ll11l_opy_
@measure(event_name=EVENTS.bstack1l1llll1_opy_, stage=STAGE.bstack1ll11l11ll_opy_, bstack1l11l1l11l_opy_=bstack11llll11_opy_)
def bstack11l1lll11l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
    if bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⋉")):
        return
    bstack11lll11111_opy_.bstack1llll1111_opy_(bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭⋊"), True)
    global bstack11l11llll1_opy_
    global bstack11llll1ll_opy_
    bstack11l11llll1_opy_ = framework_name
    logger.info(bstack1l1ll11l1l_opy_.format(bstack11l11llll1_opy_.split(bstack1l1l1l1_opy_ (u"ࠪ࠱ࠬ⋋"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lll11ll1_opy_():
            Service.start = bstack1111lll11_opy_
            Service.stop = bstack1ll1ll111_opy_
            webdriver.Remote.get = bstack1ll111ll_opy_
            webdriver.Remote.__init__ = bstack11ll111l_opy_
            if not isinstance(os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ⋌")), str):
                return
            WebDriver.quit = bstack1l1l111lll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111llllll_opy_.on():
            webdriver.Remote.__init__ = bstack1l11ll1l11_opy_
        bstack11llll1ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1l1l1_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ⋍")):
        bstack11llll1ll_opy_ = eval(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ⋎")))
    if not bstack11llll1ll_opy_:
        bstack1l1ll1111l_opy_(bstack1l1l1l1_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ⋏"), bstack1lll1llll_opy_)
    if bstack111ll111_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1l1l1_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⋐")) and callable(getattr(RemoteConnection, bstack1l1l1l1_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⋑"))):
                RemoteConnection._get_proxy_url = bstack11l1l1llll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11l1l1llll_opy_
        except Exception as e:
            logger.error(bstack1llll1ll11_opy_.format(str(e)))
    if bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⋒") in str(framework_name).lower():
        if not bstack1l1lll11ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1lll1l111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l111l111_opy_
            Config.getoption = bstack11l11ll1l1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11llll1ll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1111l1l_opy_, stage=STAGE.bstack1l1lll1lll_opy_, bstack1l11l1l11l_opy_=bstack11llll11_opy_)
def bstack1l1l111lll_opy_(self):
    global bstack11l11llll1_opy_
    global bstack1lll111ll1_opy_
    global bstack1l1l11ll1_opy_
    try:
        if bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⋓") in bstack11l11llll1_opy_ and self.session_id != None and bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ⋔"), bstack1l1l1l1_opy_ (u"࠭ࠧ⋕")) != bstack1l1l1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⋖"):
            bstack11lll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⋗") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⋘")
            bstack1ll1ll11ll_opy_(logger, True)
            if os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⋙"), None):
                self.execute_script(
                    bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ⋚") + json.dumps(
                        os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⋛"))) + bstack1l1l1l1_opy_ (u"࠭ࡽࡾࠩ⋜"))
            if self != None:
                bstack1111ll1ll_opy_(self, bstack11lll1l11_opy_, bstack1l1l1l1_opy_ (u"ࠧ࠭ࠢࠪ⋝").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll1lllll1l_opy_(bstack1llll1l1111_opy_):
            item = store.get(bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⋞"), None)
            if item is not None and bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⋟"), None):
                bstack1l1l1l11_opy_.bstack11l1llll1l_opy_(self, bstack11lll1lll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1l1l1_opy_ (u"ࠪࠫ⋠")
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ⋡") + str(e))
    bstack1l1l11ll1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11l11l1l11_opy_, stage=STAGE.bstack1l1lll1lll_opy_, bstack1l11l1l11l_opy_=bstack11llll11_opy_)
def bstack11ll111l_opy_(self, command_executor,
             desired_capabilities=None, bstack1l1l11l1l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll111ll1_opy_
    global bstack11llll11_opy_
    global bstack1l1l111111_opy_
    global bstack11l11llll1_opy_
    global bstack11lll111ll_opy_
    global bstack1lll1l11l1_opy_
    global bstack1l1lll11l1_opy_
    global bstack1ll1l111_opy_
    global bstack11lll1lll1_opy_
    CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⋢")] = str(bstack11l11llll1_opy_) + str(__version__)
    command_executor = bstack11l111llll_opy_(bstack1l1lll11l1_opy_, CONFIG)
    logger.debug(bstack1l11l1ll_opy_.format(command_executor))
    proxy = bstack11lllll1ll_opy_(CONFIG, proxy)
    bstack1ll111l111_opy_ = 0
    try:
        if bstack1l1l111111_opy_ is True:
            bstack1ll111l111_opy_ = int(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⋣")))
    except:
        bstack1ll111l111_opy_ = 0
    bstack1l11l11ll1_opy_ = bstack11ll1l1ll_opy_(CONFIG, bstack1ll111l111_opy_)
    logger.debug(bstack11ll1ll1ll_opy_.format(str(bstack1l11l11ll1_opy_)))
    bstack11lll1lll1_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⋤"))[bstack1ll111l111_opy_]
    if bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⋥") in CONFIG and CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⋦")]:
        bstack11ll11l1l_opy_(bstack1l11l11ll1_opy_, bstack1ll1l111_opy_)
    if bstack1ll1l11ll_opy_.bstack1l1l1ll1_opy_(CONFIG, bstack1ll111l111_opy_) and bstack1ll1l11ll_opy_.bstack11ll1l1l1_opy_(bstack1l11l11ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll1lllll1l_opy_(bstack1llll1l1111_opy_):
            bstack1ll1l11ll_opy_.set_capabilities(bstack1l11l11ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll1111ll1_opy_ = bstack1l1ll1ll1_opy_(desired_capabilities)
        bstack1ll1111ll1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⋧")] = bstack111l1l1l1_opy_(CONFIG)
        bstack1l1111l11l_opy_ = bstack11ll1l1ll_opy_(bstack1ll1111ll1_opy_)
        if bstack1l1111l11l_opy_:
            bstack1l11l11ll1_opy_ = update(bstack1l1111l11l_opy_, bstack1l11l11ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l11l11l11_opy_(options, bstack1l11l11ll1_opy_)
    if not options:
        options = bstack1111l1ll_opy_(bstack1l11l11ll1_opy_)
    if proxy and bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⋨")):
        options.proxy(proxy)
    if options and bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⋩")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11lll1l11l_opy_() < version.parse(bstack1l1l1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⋪")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11l11ll1_opy_)
    logger.info(bstack1l1111l1ll_opy_)
    bstack11ll1ll1_opy_.end(EVENTS.bstack1l1llll1_opy_.value, EVENTS.bstack1l1llll1_opy_.value + bstack1l1l1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⋫"),
                               EVENTS.bstack1l1llll1_opy_.value + bstack1l1l1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ⋬"), True, None)
    if bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⋭")):
        bstack11lll111ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⋮")):
        bstack11lll111ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1l1l11l1l_opy_=bstack1l1l11l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ⋯")):
        bstack11lll111ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1l11l1l_opy_=bstack1l1l11l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11lll111ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1l11l1l_opy_=bstack1l1l11l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l11lll11_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭⋰")
        if bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ⋱")):
            bstack1l11lll11_opy_ = self.caps.get(bstack1l1l1l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⋲"))
        else:
            bstack1l11lll11_opy_ = self.capabilities.get(bstack1l1l1l1_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ⋳"))
        if bstack1l11lll11_opy_:
            bstack11lll111_opy_(bstack1l11lll11_opy_)
            if bstack11lll1l11l_opy_() <= version.parse(bstack1l1l1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ⋴")):
                self.command_executor._url = bstack1l1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⋵") + bstack1l1lll11l1_opy_ + bstack1l1l1l1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ⋶")
            else:
                self.command_executor._url = bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ⋷") + bstack1l11lll11_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ⋸")
            logger.debug(bstack11l111l1l_opy_.format(bstack1l11lll11_opy_))
        else:
            logger.debug(bstack1ll11l1lll_opy_.format(bstack1l1l1l1_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ⋹")))
    except Exception as e:
        logger.debug(bstack1ll11l1lll_opy_.format(e))
    bstack1lll111ll1_opy_ = self.session_id
    if bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⋺") in bstack11l11llll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⋻"), None)
        if item:
            bstack1llll1ll1lll_opy_ = getattr(item, bstack1l1l1l1_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⋼"), False)
            if not getattr(item, bstack1l1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⋽"), None) and bstack1llll1ll1lll_opy_:
                setattr(store[bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⋾")], bstack1l1l1l1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⋿"), self)
        bstack1l1lll111l_opy_ = getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⌀"), None)
        if bstack1l1lll111l_opy_ and bstack1l1lll111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⌁"), bstack1l1l1l1_opy_ (u"ࠩࠪ⌂")) == bstack1l1l1l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⌃"):
            bstack111llllll_opy_.bstack1ll111l1ll_opy_(self)
    bstack1lll1l11l1_opy_.append(self)
    if bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⌄") in CONFIG and bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌅") in CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⌆")][bstack1ll111l111_opy_]:
        bstack11llll11_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⌇")][bstack1ll111l111_opy_][bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⌈")]
    logger.debug(bstack1ll1lllll1_opy_.format(bstack1lll111ll1_opy_))
@measure(event_name=EVENTS.bstack1l1lllll1l_opy_, stage=STAGE.bstack1l1lll1lll_opy_, bstack1l11l1l11l_opy_=bstack11llll11_opy_)
def bstack1ll111ll_opy_(self, url):
    global bstack11ll11l111_opy_
    global CONFIG
    try:
        bstack1ll1l11l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1llll_opy_.format(str(err)))
    try:
        bstack11ll11l111_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll111llll_opy_ = str(e)
            if any(err_msg in bstack1ll111llll_opy_ for err_msg in bstack1ll1ll1l1l_opy_):
                bstack1ll1l11l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1llll_opy_.format(str(err)))
        raise e
def bstack11llllll1l_opy_(item, when):
    global bstack1111l1ll1_opy_
    try:
        bstack1111l1ll1_opy_(item, when)
    except Exception as e:
        pass
def bstack11llll1ll1_opy_(item, call, rep):
    global bstack11ll1lll1_opy_
    global bstack1lll1l11l1_opy_
    name = bstack1l1l1l1_opy_ (u"ࠩࠪ⌉")
    try:
        if rep.when == bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⌊"):
            bstack1lll111ll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1l1l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⌋"))
            try:
                if (str(skipSessionName).lower() != bstack1l1l1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪ⌌")):
                    name = str(rep.nodeid)
                    bstack11llll11l_opy_ = bstack11l11ll1_opy_(bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⌍"), name, bstack1l1l1l1_opy_ (u"ࠧࠨ⌎"), bstack1l1l1l1_opy_ (u"ࠨࠩ⌏"), bstack1l1l1l1_opy_ (u"ࠩࠪ⌐"), bstack1l1l1l1_opy_ (u"ࠪࠫ⌑"))
                    os.environ[bstack1l1l1l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⌒")] = name
                    for driver in bstack1lll1l11l1_opy_:
                        if bstack1lll111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11llll11l_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⌓").format(str(e)))
            try:
                bstack1l1l1lll11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⌔"):
                    status = bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌕") if rep.outcome.lower() == bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⌖") else bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⌗")
                    reason = bstack1l1l1l1_opy_ (u"ࠪࠫ⌘")
                    if status == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⌙"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ⌚") if status == bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌛") else bstack1l1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⌜")
                    data = name + bstack1l1l1l1_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ⌝") if status == bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⌞") else name + bstack1l1l1l1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭⌟") + reason
                    bstack1l11ll1111_opy_ = bstack11l11ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭⌠"), bstack1l1l1l1_opy_ (u"ࠬ࠭⌡"), bstack1l1l1l1_opy_ (u"࠭ࠧ⌢"), bstack1l1l1l1_opy_ (u"ࠧࠨ⌣"), level, data)
                    for driver in bstack1lll1l11l1_opy_:
                        if bstack1lll111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11ll1111_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⌤").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭⌥").format(str(e)))
    bstack11ll1lll1_opy_(item, call, rep)
notset = Notset()
def bstack11l11ll1l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll111ll_opy_
    if str(name).lower() == bstack1l1l1l1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ⌦"):
        return bstack1l1l1l1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ⌧")
    else:
        return bstack1llll111ll_opy_(self, name, default, skip)
def bstack11l1l1llll_opy_(self):
    global CONFIG
    global bstack1l1l1ll1l1_opy_
    try:
        proxy = bstack11l1111ll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l1l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ⌨")):
                proxies = bstack1ll1l11lll_opy_(proxy, bstack11l111llll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11l1l11_opy_ = proxies.popitem()
                    if bstack1l1l1l1_opy_ (u"ࠨ࠺࠰࠱ࠥ〈") in bstack1ll11l1l11_opy_:
                        return bstack1ll11l1l11_opy_
                    else:
                        return bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ〉") + bstack1ll11l1l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ⌫").format(str(e)))
    return bstack1l1l1ll1l1_opy_(self)
def bstack111ll111_opy_():
    return (bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⌬") in CONFIG or bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⌭") in CONFIG) and bstack11l11l11l1_opy_() and bstack11lll1l11l_opy_() >= version.parse(
        bstack11ll1ll11l_opy_)
def bstack1lll1lll1l_opy_(self,
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
    global bstack11llll11_opy_
    global bstack1l1l111111_opy_
    global bstack11l11llll1_opy_
    CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⌮")] = str(bstack11l11llll1_opy_) + str(__version__)
    bstack1ll111l111_opy_ = 0
    try:
        if bstack1l1l111111_opy_ is True:
            bstack1ll111l111_opy_ = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⌯")))
    except:
        bstack1ll111l111_opy_ = 0
    CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ⌰")] = True
    bstack1l11l11ll1_opy_ = bstack11ll1l1ll_opy_(CONFIG, bstack1ll111l111_opy_)
    logger.debug(bstack11ll1ll1ll_opy_.format(str(bstack1l11l11ll1_opy_)))
    if CONFIG.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⌱")):
        bstack11ll11l1l_opy_(bstack1l11l11ll1_opy_, bstack1ll1l111_opy_)
    if bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⌲") in CONFIG and bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⌳") in CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⌴")][bstack1ll111l111_opy_]:
        bstack11llll11_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⌵")][bstack1ll111l111_opy_][bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⌶")]
    import urllib
    import json
    if bstack1l1l1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⌷") in CONFIG and str(CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⌸")]).lower() != bstack1l1l1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⌹"):
        bstack11ll1l1111_opy_ = bstack11ll1ll11_opy_()
        bstack1ll111l1_opy_ = bstack11ll1l1111_opy_ + urllib.parse.quote(json.dumps(bstack1l11l11ll1_opy_))
    else:
        bstack1ll111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ⌺") + urllib.parse.quote(json.dumps(bstack1l11l11ll1_opy_))
    browser = self.connect(bstack1ll111l1_opy_)
    return browser
def bstack1l1111l1l_opy_():
    global bstack11llll1ll_opy_
    global bstack11l11llll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11llll111l_opy_
        if not bstack1l1lll11ll1_opy_():
            global bstack1ll11111ll_opy_
            if not bstack1ll11111ll_opy_:
                from bstack_utils.helper import bstack1111l1l1_opy_, bstack11l1ll1111_opy_
                bstack1ll11111ll_opy_ = bstack1111l1l1_opy_()
                bstack11l1ll1111_opy_(bstack11l11llll1_opy_)
            BrowserType.connect = bstack11llll111l_opy_
            return
        BrowserType.launch = bstack1lll1lll1l_opy_
        bstack11llll1ll_opy_ = True
    except Exception as e:
        pass
def bstack1llll1lll111_opy_():
    global CONFIG
    global bstack11ll1lll1l_opy_
    global bstack1l1lll11l1_opy_
    global bstack1ll1l111_opy_
    global bstack1l1l111111_opy_
    global bstack11l1l1l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ⌻")))
    bstack11ll1lll1l_opy_ = eval(os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⌼")))
    bstack1l1lll11l1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ⌽"))
    bstack1l111l111_opy_(CONFIG, bstack11ll1lll1l_opy_)
    bstack11l1l1l1l1_opy_ = bstack1llll1l111_opy_.bstack11l1l11ll_opy_(CONFIG, bstack11l1l1l1l1_opy_)
    if cli.bstack1ll1l11l1_opy_():
        bstack11lll11l1l_opy_.invoke(bstack1l11ll11l1_opy_.CONNECT, bstack1111l111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⌾"), bstack1l1l1l1_opy_ (u"ࠧ࠱ࠩ⌿")))
        cli.bstack1llll1l1ll1_opy_(cli_context.platform_index)
        cli.bstack1lll11l111l_opy_(bstack11l111llll_opy_(bstack1l1lll11l1_opy_, CONFIG), cli_context.platform_index, bstack1111l1ll_opy_)
        cli.bstack1llll11ll11_opy_()
        logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⍀") + str(cli_context.platform_index) + bstack1l1l1l1_opy_ (u"ࠤࠥ⍁"))
        return # skip all existing bstack1llll1ll11l1_opy_
    global bstack11lll111ll_opy_
    global bstack1l1l11ll1_opy_
    global bstack1ll1ll111l_opy_
    global bstack11l11111l1_opy_
    global bstack11l1ll1l1l_opy_
    global bstack1ll1l111ll_opy_
    global bstack1l11l11ll_opy_
    global bstack11ll11l111_opy_
    global bstack1l1l1ll1l1_opy_
    global bstack1llll111ll_opy_
    global bstack1111l1ll1_opy_
    global bstack11ll1lll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11lll111ll_opy_ = webdriver.Remote.__init__
        bstack1l1l11ll1_opy_ = WebDriver.quit
        bstack1l11l11ll_opy_ = WebDriver.close
        bstack11ll11l111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⍂") in CONFIG or bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⍃") in CONFIG) and bstack11l11l11l1_opy_():
        if bstack11lll1l11l_opy_() < version.parse(bstack11ll1ll11l_opy_):
            logger.error(bstack1llllll11l_opy_.format(bstack11lll1l11l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1l1l1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⍄")) and callable(getattr(RemoteConnection, bstack1l1l1l1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⍅"))):
                    bstack1l1l1ll1l1_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1l1ll1l1_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1llll1ll11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll111ll_opy_ = Config.getoption
        from _pytest import runner
        bstack1111l1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1ll111l_opy_)
    try:
        from pytest_bdd import reporting
        bstack11ll1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ⍆"))
    bstack1ll1l111_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ⍇"), {}).get(bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⍈"))
    bstack1l1l111111_opy_ = True
    bstack11l1lll11l_opy_(bstack11111llll_opy_)
if (bstack11l11l11lll_opy_()):
    bstack1llll1lll111_opy_()
@bstack111ll11111_opy_(class_method=False)
def bstack1lllll111111_opy_(hook_name, event, bstack1l1111ll1ll_opy_=None):
    if hook_name not in [bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⍉"), bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⍊"), bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⍋"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⍌"), bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⍍"), bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⍎"), bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⍏"), bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ⍐")]:
        return
    node = store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⍑")]
    if hook_name in [bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⍒"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⍓")]:
        node = store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭⍔")]
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⍕"), bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⍖")]:
        node = store[bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⍗")]
    hook_type = bstack11111l1l1l1_opy_(hook_name)
    if event == bstack1l1l1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⍘"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_[hook_type], bstack1lll1lll111_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1ll111_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⍙"): uuid,
            bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⍚"): bstack1lllll1l1l_opy_(),
            bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⍛"): bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭⍜"),
            bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⍝"): hook_type,
            bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⍞"): hook_name
        }
        store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⍟")].append(uuid)
        bstack1llll1l11l1l_opy_ = node.nodeid
        if hook_type == bstack1l1l1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⍠"):
            if not _111ll11l11_opy_.get(bstack1llll1l11l1l_opy_, None):
                _111ll11l11_opy_[bstack1llll1l11l1l_opy_] = {bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⍡"): []}
            _111ll11l11_opy_[bstack1llll1l11l1l_opy_][bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⍢")].append(bstack111l1ll111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⍣")])
        _111ll11l11_opy_[bstack1llll1l11l1l_opy_ + bstack1l1l1l1_opy_ (u"ࠩ࠰ࠫ⍤") + hook_name] = bstack111l1ll111_opy_
        bstack1llll1ll1l11_opy_(node, bstack111l1ll111_opy_, bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⍥"))
    elif event == bstack1l1l1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⍦"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1ll11l11_opy_[hook_type], bstack1lll1lll111_opy_.POST, node, None, bstack1l1111ll1ll_opy_)
            return
        bstack111lll1111_opy_ = node.nodeid + bstack1l1l1l1_opy_ (u"ࠬ࠳ࠧ⍧") + hook_name
        _111ll11l11_opy_[bstack111lll1111_opy_][bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⍨")] = bstack1lllll1l1l_opy_()
        bstack1llll1lllll1_opy_(_111ll11l11_opy_[bstack111lll1111_opy_][bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⍩")])
        bstack1llll1ll1l11_opy_(node, _111ll11l11_opy_[bstack111lll1111_opy_], bstack1l1l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⍪"), bstack1llll1l1l1l1_opy_=bstack1l1111ll1ll_opy_)
def bstack1llll1l111l1_opy_():
    global bstack1llll1llll1l_opy_
    if bstack11lll111l1_opy_():
        bstack1llll1llll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⍫")
    else:
        bstack1llll1llll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⍬")
@bstack111llllll_opy_.bstack1lllll1lll11_opy_
def bstack1llll1l11lll_opy_():
    bstack1llll1l111l1_opy_()
    if cli.is_running():
        try:
            bstack111lll111l1_opy_(bstack1lllll111111_opy_)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⍭").format(e))
        return
    if bstack11l11l11l1_opy_():
        bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
        bstack1l1l1l1_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ⍮")
        if bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⍯")):
            if CONFIG.get(bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⍰")) is not None and int(CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⍱")]) > 1:
                bstack11l1l11111_opy_(bstack11l11l1l_opy_)
            return
        bstack11l1l11111_opy_(bstack11l11l1l_opy_)
    try:
        bstack111lll111l1_opy_(bstack1lllll111111_opy_)
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⍲").format(e))
bstack1llll1l11lll_opy_()