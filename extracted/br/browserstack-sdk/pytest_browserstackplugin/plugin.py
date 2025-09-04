# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lllll1ll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll1111_opy_, bstack1l111111l_opy_, update, bstack1l1l1l1l1l_opy_,
                                       bstack1111l1lll_opy_, bstack111ll1l1_opy_, bstack111l1l11l_opy_, bstack1llll1l1l1_opy_,
                                       bstack1l111lll_opy_, bstack11l1111ll1_opy_, bstack1lll1l11_opy_,
                                       bstack11lll111ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1111111l1_opy_)
from browserstack_sdk.bstack1l111llll1_opy_ import bstack11l1ll1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11l1111l1_opy_
from bstack_utils.capture import bstack111ll1ll1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll111ll11_opy_, bstack1lllll11l_opy_, bstack11ll11111_opy_, \
    bstack11l11111_opy_
from bstack_utils.helper import bstack1l11l1lll_opy_, bstack11l111l1l11_opy_, bstack1111l1lll1_opy_, bstack1l11l111l1_opy_, bstack1l1ll1l1l1l_opy_, bstack1ll111ll1l_opy_, \
    bstack11l111l111l_opy_, \
    bstack111lll111l1_opy_, bstack1ll1l1lll1_opy_, bstack111llllll1_opy_, bstack111lllll111_opy_, bstack1ll1l1l1l1_opy_, Notset, \
    bstack11l1l1l11_opy_, bstack111ll1l1l1l_opy_, bstack11l111lllll_opy_, Result, bstack111lll11lll_opy_, bstack11l111l1lll_opy_, error_handler, \
    bstack11lllll1l1_opy_, bstack111111ll_opy_, bstack1lll1l11l_opy_, bstack11l111lll1l_opy_
from bstack_utils.bstack111ll1111ll_opy_ import bstack111ll11l1ll_opy_
from bstack_utils.messages import bstack1l1l111l1l_opy_, bstack1lllll1l11_opy_, bstack1ll111l1_opy_, bstack1l1111ll11_opy_, bstack11ll1l1l_opy_, \
    bstack1ll1l1111_opy_, bstack11l1111l11_opy_, bstack1ll1ll1l11_opy_, bstack1l111ll1_opy_, bstack1l1l1l11l_opy_, \
    bstack111l1ll1_opy_, bstack1l11ll1lll_opy_, bstack11ll1lll1_opy_
from bstack_utils.proxy import bstack1l11l11ll_opy_, bstack111ll11l1_opy_
from bstack_utils.bstack1l1l11111l_opy_ import bstack1llllllll1l1_opy_, bstack1lllllll1ll1_opy_, bstack1lllllllll1l_opy_, bstack1lllllllll11_opy_, \
    bstack1lllllll1l1l_opy_, bstack1111111111l_opy_, bstack1llllllll11l_opy_, bstack11l1llllll_opy_, bstack1llllllll111_opy_
from bstack_utils.bstack1ll11l111l_opy_ import bstack11llllll1_opy_
from bstack_utils.bstack1ll1l11l11_opy_ import bstack1ll1l1l1l_opy_, bstack1l1l1111l1_opy_, bstack1l1lll1l1_opy_, \
    bstack1l11111l1l_opy_, bstack1l11l11l1l_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack111l1lllll_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1ll11lll1_opy_
import bstack_utils.accessibility as bstack1lll1111l1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1lllll1_opy_
from bstack_utils.bstack1ll1ll1ll1_opy_ import bstack1ll1ll1ll1_opy_
from bstack_utils.bstack11llllll_opy_ import bstack111l1llll_opy_
from browserstack_sdk.__init__ import bstack11l11l1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_, bstack1l111l1111_opy_, bstack11l11l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111ll111l_opy_, bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_, bstack1l111l1111_opy_, bstack11l11l11l1_opy_
bstack1l1llll11_opy_ = None
bstack11lllll11l_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1ll1111l11_opy_ = None
bstack11l11ll1l1_opy_ = None
bstack1l1ll1l1l1_opy_ = None
bstack1ll1l1llll_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack1111l11l1_opy_ = None
bstack1lll1llll1_opy_ = None
bstack11lll111l1_opy_ = None
bstack1l1llll11l_opy_ = None
bstack1l111111l1_opy_ = None
bstack1l111l11l1_opy_ = bstack1111l1l_opy_ (u"ࠫࠬ∈")
CONFIG = {}
bstack111lll111_opy_ = False
bstack1l111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠬ࠭∉")
bstack1lll1ll11_opy_ = bstack1111l1l_opy_ (u"࠭ࠧ∊")
bstack11llll1lll_opy_ = False
bstack1l11l11l1_opy_ = []
bstack1l1ll11l1l_opy_ = bstack1ll111ll11_opy_
bstack1llll1111ll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ∋")
bstack111111ll1_opy_ = {}
bstack1lllllllll_opy_ = None
bstack11111l111_opy_ = False
logger = bstack11l1111l1_opy_.get_logger(__name__, bstack1l1ll11l1l_opy_)
store = {
    bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ∌"): []
}
bstack1llll1111l1l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l1l1l1l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l111ll111l_opy_(
    test_framework_name=bstack11l111l11_opy_[bstack1111l1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭∍")] if bstack1ll1l1l1l1_opy_() else bstack11l111l11_opy_[bstack1111l1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪ∎")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1lll1ll1ll_opy_(page, bstack1ll1lll1ll_opy_):
    try:
        page.evaluate(bstack1111l1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ∏"),
                      bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩ∐") + json.dumps(
                          bstack1ll1lll1ll_opy_) + bstack1111l1l_opy_ (u"ࠨࡽࡾࠤ∑"))
    except Exception as e:
        print(bstack1111l1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ−"), e)
def bstack11l1l1ll1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1111l1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ∓"), bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ∔") + json.dumps(
            message) + bstack1111l1l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭∕") + json.dumps(level) + bstack1111l1l_opy_ (u"ࠫࢂࢃࠧ∖"))
    except Exception as e:
        print(bstack1111l1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ∗"), e)
def pytest_configure(config):
    global bstack1l111l1ll_opy_
    global CONFIG
    bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
    config.args = bstack1ll11lll1_opy_.bstack1llll111lll1_opy_(config.args)
    bstack1l1ll11l1_opy_.bstack11l1l1lll_opy_(bstack1lll1l11l_opy_(config.getoption(bstack1111l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ∘"))))
    try:
        bstack11l1111l1_opy_.bstack111l1ll11ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.CONNECT, bstack11l11l11l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ∙"), bstack1111l1l_opy_ (u"ࠨ࠲ࠪ√")))
        config = json.loads(os.environ.get(bstack1111l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣ∛"), bstack1111l1l_opy_ (u"ࠥࡿࢂࠨ∜")))
        cli.bstack1lll11l1111_opy_(bstack111llllll1_opy_(bstack1l111l1ll_opy_, CONFIG), cli_context.platform_index, bstack1l1l1l1l1l_opy_)
    if cli.bstack1llll111ll1_opy_(bstack1lll1l11lll_opy_):
        cli.bstack1ll1lll1ll1_opy_()
        logger.debug(bstack1111l1l_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥ∝") + str(cli_context.platform_index) + bstack1111l1l_opy_ (u"ࠧࠨ∞"))
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.BEFORE_ALL, bstack1ll1llll1ll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1111l1l_opy_ (u"ࠨࡷࡩࡧࡱࠦ∟"), None)
    if cli.is_running() and when == bstack1111l1l_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ∠"):
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.LOG_REPORT, bstack1ll1llll1ll_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1111l1l_opy_ (u"ࠣࡥࡤࡰࡱࠨ∡"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111l1l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ∢")))
        if not passed:
            config = json.loads(os.environ.get(bstack1111l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤ∣"), bstack1111l1l_opy_ (u"ࠦࢀࢃࠢ∤")))
            if bstack111l1llll_opy_.bstack11111ll1l_opy_(config):
                bstack1111l11llll_opy_ = bstack111l1llll_opy_.bstack1l1ll1llll_opy_(config)
                if item.execution_count > bstack1111l11llll_opy_:
                    print(bstack1111l1l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡵࡩࡹࡸࡩࡦࡵ࠽ࠤࠬ∥"), report.nodeid, os.environ.get(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ∦")))
                    bstack111l1llll_opy_.bstack111l111llll_opy_(report.nodeid)
            else:
                print(bstack1111l1l_opy_ (u"ࠧࡕࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࠧ∧"), report.nodeid, os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭∨")))
                bstack111l1llll_opy_.bstack111l111llll_opy_(report.nodeid)
        else:
            print(bstack1111l1l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡱࡣࡶࡷࡪࡪ࠺ࠡࠩ∩"), report.nodeid, os.environ.get(bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ∪")))
    if cli.is_running():
        if when == bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ∫"):
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.BEFORE_EACH, bstack1ll1llll1ll_opy_.POST, item, call, outcome)
        elif when == bstack1111l1l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ∬"):
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.LOG_REPORT, bstack1ll1llll1ll_opy_.POST, item, call, outcome)
        elif when == bstack1111l1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ∭"):
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.AFTER_EACH, bstack1ll1llll1ll_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1111l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ∮"))
    plugins = item.config.getoption(bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤ∯"))
    report = outcome.get_result()
    os.environ[bstack1111l1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ∰")] = report.nodeid
    bstack1lll1lll1l11_opy_(item, call, report)
    if bstack1111l1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣ∱") not in plugins or bstack1ll1l1l1l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111l1l_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧ∲"), None)
    page = getattr(item, bstack1111l1l_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦ∳"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1lll1lll1l1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1lll1llll11l_opy_(item, report, summary, skipSessionName)
def bstack1lll1lll1l1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ∴") and report.skipped:
        bstack1llllllll111_opy_(report)
    if report.when in [bstack1111l1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ∵"), bstack1111l1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ∶")]:
        return
    if not bstack1l1ll1l1l1l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1111l1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ∷")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ∸") + json.dumps(
                    report.nodeid) + bstack1111l1l_opy_ (u"ࠫࢂࢃࠧ∹"))
        os.environ[bstack1111l1l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ∺")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1111l1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨ∻").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111l1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ∼")))
    bstack11ll111lll_opy_ = bstack1111l1l_opy_ (u"ࠣࠤ∽")
    bstack1llllllll111_opy_(report)
    if not passed:
        try:
            bstack11ll111lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111l1l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ∾").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll111lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1111l1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ∿")))
        bstack11ll111lll_opy_ = bstack1111l1l_opy_ (u"ࠦࠧ≀")
        if not passed:
            try:
                bstack11ll111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111l1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ≁").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll111lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ≂")
                    + json.dumps(bstack1111l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣ≃"))
                    + bstack1111l1l_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ≄")
                )
            else:
                item._driver.execute_script(
                    bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ≅")
                    + json.dumps(str(bstack11ll111lll_opy_))
                    + bstack1111l1l_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨ≆")
                )
        except Exception as e:
            summary.append(bstack1111l1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤ≇").format(e))
def bstack1lll1lll111l_opy_(test_name, error_message):
    try:
        bstack1lll1lll11ll_opy_ = []
        bstack11lll11l_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ≈"), bstack1111l1l_opy_ (u"࠭࠰ࠨ≉"))
        bstack1lll1lllll_opy_ = {bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ≊"): test_name, bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ≋"): error_message, bstack1111l1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ≌"): bstack11lll11l_opy_}
        bstack1llll111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ≍"))
        if os.path.exists(bstack1llll111l11l_opy_):
            with open(bstack1llll111l11l_opy_) as f:
                bstack1lll1lll11ll_opy_ = json.load(f)
        bstack1lll1lll11ll_opy_.append(bstack1lll1lllll_opy_)
        with open(bstack1llll111l11l_opy_, bstack1111l1l_opy_ (u"ࠫࡼ࠭≎")) as f:
            json.dump(bstack1lll1lll11ll_opy_, f)
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪ≏") + str(e))
def bstack1lll1llll11l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1111l1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ≐"), bstack1111l1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ≑")]:
        return
    if (str(skipSessionName).lower() != bstack1111l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭≒")):
        bstack1lll1ll1ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111l1l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ≓")))
    bstack11ll111lll_opy_ = bstack1111l1l_opy_ (u"ࠥࠦ≔")
    bstack1llllllll111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11ll111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111l1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ≕").format(e)
                )
        try:
            if passed:
                bstack1l11l11l1l_opy_(getattr(item, bstack1111l1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ≖"), None), bstack1111l1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ≗"))
            else:
                error_message = bstack1111l1l_opy_ (u"ࠧࠨ≘")
                if bstack11ll111lll_opy_:
                    bstack11l1l1ll1l_opy_(item._page, str(bstack11ll111lll_opy_), bstack1111l1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ≙"))
                    bstack1l11l11l1l_opy_(getattr(item, bstack1111l1l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ≚"), None), bstack1111l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ≛"), str(bstack11ll111lll_opy_))
                    error_message = str(bstack11ll111lll_opy_)
                else:
                    bstack1l11l11l1l_opy_(getattr(item, bstack1111l1l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ≜"), None), bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ≝"))
                bstack1lll1lll111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1111l1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥ≞").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1111l1l_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ≟"), default=bstack1111l1l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ≠"), help=bstack1111l1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ≡"))
    parser.addoption(bstack1111l1l_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ≢"), default=bstack1111l1l_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ≣"), help=bstack1111l1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ≤"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111l1l_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣ≥"), action=bstack1111l1l_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨ≦"), default=bstack1111l1l_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣ≧"),
                         help=bstack1111l1l_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣ≨"))
def bstack111ll1llll_opy_(log):
    if not (log[bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ≩")] and log[bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ≪")].strip()):
        return
    active = bstack111ll1l1l1_opy_()
    log = {
        bstack1111l1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ≫"): log[bstack1111l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ≬")],
        bstack1111l1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ≭"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"ࠨ࡜ࠪ≮"),
        bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ≯"): log[bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ≰")],
    }
    if active:
        if active[bstack1111l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ≱")] == bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ≲"):
            log[bstack1111l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭≳")] = active[bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ≴")]
        elif active[bstack1111l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭≵")] == bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺࠧ≶"):
            log[bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ≷")] = active[bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ≸")]
    bstack11l1lllll1_opy_.bstack11l11l1l1l_opy_([log])
def bstack111ll1l1l1_opy_():
    if len(store[bstack1111l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ≹")]) > 0 and store[bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ≺")][-1]:
        return {
            bstack1111l1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ≻"): bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭≼"),
            bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ≽"): store[bstack1111l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ≾")][-1]
        }
    if store.get(bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ≿"), None):
        return {
            bstack1111l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⊀"): bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫ⊁"),
            bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⊂"): store[bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⊃")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.INIT_TEST, bstack1ll1llll1ll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.INIT_TEST, bstack1ll1llll1ll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1lll1ll1ll1l_opy_ = True
        bstack1ll1l111_opy_ = bstack1lll1111l1_opy_.bstack11l111ll_opy_(bstack111lll111l1_opy_(item.own_markers))
        if not cli.bstack1llll111ll1_opy_(bstack1lll1l11lll_opy_):
            item._a11y_test_case = bstack1ll1l111_opy_
            if bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⊄"), None):
                driver = getattr(item, bstack1111l1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⊅"), None)
                item._a11y_started = bstack1lll1111l1_opy_.bstack11l1ll1l1l_opy_(driver, bstack1ll1l111_opy_)
        if not bstack11l1lllll1_opy_.on() or bstack1llll1111ll1_opy_ != bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⊆"):
            return
        global current_test_uuid #, bstack111lll11l1_opy_
        bstack111l1l1111_opy_ = {
            bstack1111l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⊇"): uuid4().__str__(),
            bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊈"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"࡛ࠧࠩ⊉")
        }
        current_test_uuid = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊊")]
        store[bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⊋")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⊌")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l1l1l1l_opy_[item.nodeid] = {**_111l1l1l1l_opy_[item.nodeid], **bstack111l1l1111_opy_}
        bstack1llll111111l_opy_(item, _111l1l1l1l_opy_[item.nodeid], bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⊍"))
    except Exception as err:
        print(bstack1111l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧ⊎"), str(err))
def pytest_runtest_setup(item):
    store[bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⊏")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.BEFORE_EACH, bstack1ll1llll1ll_opy_.PRE, item, bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⊐"))
    if bstack111l1llll_opy_.bstack111l1111lll_opy_():
            bstack1lll1lllllll_opy_ = bstack1111l1l_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡣࡶࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠧ⊑")
            logger.error(bstack1lll1lllllll_opy_)
            bstack111l1l1111_opy_ = {
                bstack1111l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⊒"): uuid4().__str__(),
                bstack1111l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⊓"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"ࠫ࡟࠭⊔"),
                bstack1111l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⊕"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"࡚࠭ࠨ⊖"),
                bstack1111l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⊗"): bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⊘"),
                bstack1111l1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ⊙"): bstack1lll1lllllll_opy_,
                bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⊚"): [],
                bstack1111l1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⊛"): []
            }
            bstack1llll111111l_opy_(item, bstack111l1l1111_opy_, bstack1111l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⊜"))
            pytest.skip(bstack1lll1lllllll_opy_)
            return # skip all existing operations
    global bstack1llll1111l1l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111lllll111_opy_():
        atexit.register(bstack11l11l111_opy_)
        if not bstack1llll1111l1l_opy_:
            try:
                bstack1lll1lllll11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l111lll1l_opy_():
                    bstack1lll1lllll11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll1lllll11_opy_:
                    signal.signal(s, bstack1lll1llll111_opy_)
                bstack1llll1111l1l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢ⊝") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llllllll1l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1111l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⊞")
    try:
        if not bstack11l1lllll1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1l1111_opy_ = {
            bstack1111l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊟"): uuid,
            bstack1111l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⊠"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"ࠪ࡞ࠬ⊡"),
            bstack1111l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ⊢"): bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⊣"),
            bstack1111l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⊤"): bstack1111l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⊥"),
            bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⊦"): bstack1111l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⊧")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1111l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⊨")] = item
        store[bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⊩")] = [uuid]
        if not _111l1l1l1l_opy_.get(item.nodeid, None):
            _111l1l1l1l_opy_[item.nodeid] = {bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⊪"): [], bstack1111l1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⊫"): []}
        _111l1l1l1l_opy_[item.nodeid][bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⊬")].append(bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊭")])
        _111l1l1l1l_opy_[item.nodeid + bstack1111l1l_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩ⊮")] = bstack111l1l1111_opy_
        bstack1llll1111lll_opy_(item, bstack111l1l1111_opy_, bstack1111l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⊯"))
    except Exception as err:
        print(bstack1111l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ⊰"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.AFTER_EACH, bstack1ll1llll1ll_opy_.PRE, item, bstack1111l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⊱"))
        return # skip all existing operations
    try:
        global bstack111111ll1_opy_
        bstack11lll11l_opy_ = 0
        if bstack11llll1lll_opy_ is True:
            bstack11lll11l_opy_ = int(os.environ.get(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⊲")))
        if bstack1llll111l1_opy_.bstack11lll1l1l_opy_() == bstack1111l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧ⊳"):
            if bstack1llll111l1_opy_.bstack1l1l1l11_opy_() == bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ⊴"):
                bstack1llll11111l1_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⊵"), None)
                bstack11l1ll1111_opy_ = bstack1llll11111l1_opy_ + bstack1111l1l_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ⊶")
                driver = getattr(item, bstack1111l1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⊷"), None)
                bstack1ll1l1111l_opy_ = getattr(item, bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⊸"), None)
                bstack1l1l11l11_opy_ = getattr(item, bstack1111l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⊹"), None)
                PercySDK.screenshot(driver, bstack11l1ll1111_opy_, bstack1ll1l1111l_opy_=bstack1ll1l1111l_opy_, bstack1l1l11l11_opy_=bstack1l1l11l11_opy_, bstack1l11l11ll1_opy_=bstack11lll11l_opy_)
        if not cli.bstack1llll111ll1_opy_(bstack1lll1l11lll_opy_):
            if getattr(item, bstack1111l1l_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ⊺"), False):
                bstack11l1ll1ll1_opy_.bstack1l1l11llll_opy_(getattr(item, bstack1111l1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⊻"), None), bstack111111ll1_opy_, logger, item)
        if not bstack11l1lllll1_opy_.on():
            return
        bstack111l1l1111_opy_ = {
            bstack1111l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⊼"): uuid4().__str__(),
            bstack1111l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⊽"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"ࠫ࡟࠭⊾"),
            bstack1111l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⊿"): bstack1111l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⋀"),
            bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⋁"): bstack1111l1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⋂"),
            bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⋃"): bstack1111l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⋄")
        }
        _111l1l1l1l_opy_[item.nodeid + bstack1111l1l_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧ⋅")] = bstack111l1l1111_opy_
        bstack1llll1111lll_opy_(item, bstack111l1l1111_opy_, bstack1111l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⋆"))
    except Exception as err:
        print(bstack1111l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬ⋇"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lllllllll11_opy_(fixturedef.argname):
        store[bstack1111l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭⋈")] = request.node
    elif bstack1lllllll1l1l_opy_(fixturedef.argname):
        store[bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭⋉")] = request.node
    if not bstack11l1lllll1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.SETUP_FIXTURE, bstack1ll1llll1ll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.SETUP_FIXTURE, bstack1ll1llll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.SETUP_FIXTURE, bstack1ll1llll1ll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.SETUP_FIXTURE, bstack1ll1llll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1111l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⋊"): fixturedef.argname,
            bstack1111l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⋋"): bstack11l111l111l_opy_(outcome),
            bstack1111l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⋌"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1111l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⋍")]
        if not _111l1l1l1l_opy_.get(current_test_item.nodeid, None):
            _111l1l1l1l_opy_[current_test_item.nodeid] = {bstack1111l1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⋎"): []}
        _111l1l1l1l_opy_[current_test_item.nodeid][bstack1111l1l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⋏")].append(fixture)
    except Exception as err:
        logger.debug(bstack1111l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ⋐"), str(err))
if bstack1ll1l1l1l1_opy_() and bstack11l1lllll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.STEP, bstack1ll1llll1ll_opy_.PRE, request, step)
            return
        try:
            _111l1l1l1l_opy_[request.node.nodeid][bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⋑")].bstack11ll11l1_opy_(id(step))
        except Exception as err:
            print(bstack1111l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ⋒"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.STEP, bstack1ll1llll1ll_opy_.POST, request, step, exception)
            return
        try:
            _111l1l1l1l_opy_[request.node.nodeid][bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⋓")].bstack111ll1l11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1111l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ⋔"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.STEP, bstack1ll1llll1ll_opy_.POST, request, step)
            return
        try:
            bstack111ll1l1ll_opy_: bstack111l1lllll_opy_ = _111l1l1l1l_opy_[request.node.nodeid][bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⋕")]
            bstack111ll1l1ll_opy_.bstack111ll1l11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1111l1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ⋖"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1111ll1_opy_
        try:
            if not bstack11l1lllll1_opy_.on() or bstack1llll1111ll1_opy_ != bstack1111l1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⋗"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ⋘"), None)
            if not _111l1l1l1l_opy_.get(request.node.nodeid, None):
                _111l1l1l1l_opy_[request.node.nodeid] = {}
            bstack111ll1l1ll_opy_ = bstack111l1lllll_opy_.bstack1lllll1l11l1_opy_(
                scenario, feature, request.node,
                name=bstack1111111111l_opy_(request.node, scenario),
                started_at=bstack1ll111ll1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1111l1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ⋙"),
                tags=bstack1llllllll11l_opy_(feature, scenario),
                bstack111lll11ll_opy_=bstack11l1lllll1_opy_.bstack111ll11ll1_opy_(driver) if driver and driver.session_id else {}
            )
            _111l1l1l1l_opy_[request.node.nodeid][bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⋚")] = bstack111ll1l1ll_opy_
            bstack1lll1ll1llll_opy_(bstack111ll1l1ll_opy_.uuid)
            bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⋛"), bstack111ll1l1ll_opy_)
        except Exception as err:
            print(bstack1111l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ⋜"), str(err))
def bstack1llll11111ll_opy_(bstack111ll11l1l_opy_):
    if bstack111ll11l1l_opy_ in store[bstack1111l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⋝")]:
        store[bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⋞")].remove(bstack111ll11l1l_opy_)
def bstack1lll1ll1llll_opy_(test_uuid):
    store[bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⋟")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack11l1lllll1_opy_.bstack1llll1l1l1ll_opy_
def bstack1lll1lll1l11_opy_(item, call, report):
    logger.debug(bstack1111l1l_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡵࡸࠬ⋠"))
    global bstack1llll1111ll1_opy_
    bstack11ll11l11l_opy_ = bstack1ll111ll1l_opy_()
    if hasattr(report, bstack1111l1l_opy_ (u"ࠫࡸࡺ࡯ࡱࠩ⋡")):
        bstack11ll11l11l_opy_ = bstack111lll11lll_opy_(report.stop)
    elif hasattr(report, bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫ⋢")):
        bstack11ll11l11l_opy_ = bstack111lll11lll_opy_(report.start)
    try:
        if getattr(report, bstack1111l1l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⋣"), bstack1111l1l_opy_ (u"ࠧࠨ⋤")) == bstack1111l1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭⋥"):
            logger.debug(bstack1111l1l_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ⋦").format(getattr(report, bstack1111l1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⋧"), bstack1111l1l_opy_ (u"ࠫࠬ⋨")).__str__(), bstack1llll1111ll1_opy_))
            if bstack1llll1111ll1_opy_ == bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⋩"):
                _111l1l1l1l_opy_[item.nodeid][bstack1111l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⋪")] = bstack11ll11l11l_opy_
                bstack1llll111111l_opy_(item, _111l1l1l1l_opy_[item.nodeid], bstack1111l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⋫"), report, call)
                store[bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⋬")] = None
            elif bstack1llll1111ll1_opy_ == bstack1111l1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ⋭"):
                bstack111ll1l1ll_opy_ = _111l1l1l1l_opy_[item.nodeid][bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⋮")]
                bstack111ll1l1ll_opy_.set(hooks=_111l1l1l1l_opy_[item.nodeid].get(bstack1111l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⋯"), []))
                exception, bstack111ll1111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111ll1111l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1111l1l_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫ⋰"), bstack1111l1l_opy_ (u"࠭ࠧ⋱"))]
                bstack111ll1l1ll_opy_.stop(time=bstack11ll11l11l_opy_, result=Result(result=getattr(report, bstack1111l1l_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⋲"), bstack1111l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⋳")), exception=exception, bstack111ll1111l_opy_=bstack111ll1111l_opy_))
                bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⋴"), _111l1l1l1l_opy_[item.nodeid][bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⋵")])
        elif getattr(report, bstack1111l1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⋶"), bstack1111l1l_opy_ (u"ࠬ࠭⋷")) in [bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⋸"), bstack1111l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⋹")]:
            logger.debug(bstack1111l1l_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ⋺").format(getattr(report, bstack1111l1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⋻"), bstack1111l1l_opy_ (u"ࠪࠫ⋼")).__str__(), bstack1llll1111ll1_opy_))
            bstack111lll1111_opy_ = item.nodeid + bstack1111l1l_opy_ (u"ࠫ࠲࠭⋽") + getattr(report, bstack1111l1l_opy_ (u"ࠬࡽࡨࡦࡰࠪ⋾"), bstack1111l1l_opy_ (u"࠭ࠧ⋿"))
            if getattr(report, bstack1111l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⌀"), False):
                hook_type = bstack1111l1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⌁") if getattr(report, bstack1111l1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⌂"), bstack1111l1l_opy_ (u"ࠪࠫ⌃")) == bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⌄") else bstack1111l1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⌅")
                _111l1l1l1l_opy_[bstack111lll1111_opy_] = {
                    bstack1111l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⌆"): uuid4().__str__(),
                    bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⌇"): bstack11ll11l11l_opy_,
                    bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⌈"): hook_type
                }
            _111l1l1l1l_opy_[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⌉")] = bstack11ll11l11l_opy_
            bstack1llll11111ll_opy_(_111l1l1l1l_opy_[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⌊")])
            bstack1llll1111lll_opy_(item, _111l1l1l1l_opy_[bstack111lll1111_opy_], bstack1111l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⌋"), report, call)
            if getattr(report, bstack1111l1l_opy_ (u"ࠬࡽࡨࡦࡰࠪ⌌"), bstack1111l1l_opy_ (u"࠭ࠧ⌍")) == bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⌎"):
                if getattr(report, bstack1111l1l_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⌏"), bstack1111l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⌐")) == bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⌑"):
                    bstack111l1l1111_opy_ = {
                        bstack1111l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⌒"): uuid4().__str__(),
                        bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⌓"): bstack1ll111ll1l_opy_(),
                        bstack1111l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⌔"): bstack1ll111ll1l_opy_()
                    }
                    _111l1l1l1l_opy_[item.nodeid] = {**_111l1l1l1l_opy_[item.nodeid], **bstack111l1l1111_opy_}
                    bstack1llll111111l_opy_(item, _111l1l1l1l_opy_[item.nodeid], bstack1111l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⌕"))
                    bstack1llll111111l_opy_(item, _111l1l1l1l_opy_[item.nodeid], bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⌖"), report, call)
    except Exception as err:
        print(bstack1111l1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧ⌗"), str(err))
def bstack1llll1111l11_opy_(test, bstack111l1l1111_opy_, result=None, call=None, bstack1llll1111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111ll1l1ll_opy_ = {
        bstack1111l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⌘"): bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⌙")],
        bstack1111l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⌚"): bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࠫ⌛"),
        bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⌜"): test.name,
        bstack1111l1l_opy_ (u"ࠨࡤࡲࡨࡾ࠭⌝"): {
            bstack1111l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⌞"): bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⌟"),
            bstack1111l1l_opy_ (u"ࠫࡨࡵࡤࡦࠩ⌠"): inspect.getsource(test.obj)
        },
        bstack1111l1l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⌡"): test.name,
        bstack1111l1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⌢"): test.name,
        bstack1111l1l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⌣"): bstack1ll11lll1_opy_.bstack1111lll111_opy_(test),
        bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⌤"): file_path,
        bstack1111l1l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⌥"): file_path,
        bstack1111l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⌦"): bstack1111l1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⌧"),
        bstack1111l1l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⌨"): file_path,
        bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ〈"): bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ〉")],
        bstack1111l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⌫"): bstack1111l1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⌬"),
        bstack1111l1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭⌭"): {
            bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ⌮"): test.nodeid
        },
        bstack1111l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ⌯"): bstack111lll111l1_opy_(test.own_markers)
    }
    if bstack1llll1111_opy_ in [bstack1111l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⌰"), bstack1111l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⌱")]:
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭⌲")] = {
            bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⌳"): bstack111l1l1111_opy_.get(bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⌴"), [])
        }
    if bstack1llll1111_opy_ == bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⌵"):
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⌶")] = bstack1111l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⌷")
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⌸")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⌹")]
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⌺")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⌻")]
    if result:
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⌼")] = result.outcome
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⌽")] = result.duration * 1000
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⌾")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⌿")]
        if result.failed:
            bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⍀")] = bstack11l1lllll1_opy_.bstack111111l1ll_opy_(call.excinfo.typename)
            bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⍁")] = bstack11l1lllll1_opy_.bstack1llll1l11111_opy_(call.excinfo, result)
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⍂")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⍃")]
    if outcome:
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⍄")] = bstack11l111l111l_opy_(outcome)
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⍅")] = 0
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⍆")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⍇")]
        if bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⍈")] == bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⍉"):
            bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⍊")] = bstack1111l1l_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭⍋")  # bstack1llll1111111_opy_
            bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⍌")] = [{bstack1111l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⍍"): [bstack1111l1l_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⍎")]}]
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⍏")] = bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⍐")]
    return bstack111ll1l1ll_opy_
def bstack1llll111l111_opy_(test, bstack111l1l1lll_opy_, bstack1llll1111_opy_, result, call, outcome, bstack1lll1lll1ll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⍑")]
    hook_name = bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⍒")]
    hook_data = {
        bstack1111l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⍓"): bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⍔")],
        bstack1111l1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⍕"): bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⍖"),
        bstack1111l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ⍗"): bstack1111l1l_opy_ (u"ࠫࢀࢃࠧ⍘").format(bstack1lllllll1ll1_opy_(hook_name)),
        bstack1111l1l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⍙"): {
            bstack1111l1l_opy_ (u"࠭࡬ࡢࡰࡪࠫ⍚"): bstack1111l1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⍛"),
            bstack1111l1l_opy_ (u"ࠨࡥࡲࡨࡪ࠭⍜"): None
        },
        bstack1111l1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ⍝"): test.name,
        bstack1111l1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⍞"): bstack1ll11lll1_opy_.bstack1111lll111_opy_(test, hook_name),
        bstack1111l1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⍟"): file_path,
        bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⍠"): file_path,
        bstack1111l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⍡"): bstack1111l1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⍢"),
        bstack1111l1l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⍣"): file_path,
        bstack1111l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⍤"): bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⍥")],
        bstack1111l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⍦"): bstack1111l1l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ⍧") if bstack1llll1111ll1_opy_ == bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⍨") else bstack1111l1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⍩"),
        bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⍪"): hook_type
    }
    bstack1ll11lll111_opy_ = bstack1111ll1ll1_opy_(_111l1l1l1l_opy_.get(test.nodeid, None))
    if bstack1ll11lll111_opy_:
        hook_data[bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ⍫")] = bstack1ll11lll111_opy_
    if result:
        hook_data[bstack1111l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⍬")] = result.outcome
        hook_data[bstack1111l1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⍭")] = result.duration * 1000
        hook_data[bstack1111l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⍮")] = bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⍯")]
        if result.failed:
            hook_data[bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⍰")] = bstack11l1lllll1_opy_.bstack111111l1ll_opy_(call.excinfo.typename)
            hook_data[bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⍱")] = bstack11l1lllll1_opy_.bstack1llll1l11111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1111l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⍲")] = bstack11l111l111l_opy_(outcome)
        hook_data[bstack1111l1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⍳")] = 100
        hook_data[bstack1111l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⍴")] = bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⍵")]
        if hook_data[bstack1111l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⍶")] == bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⍷"):
            hook_data[bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⍸")] = bstack1111l1l_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⍹")  # bstack1llll1111111_opy_
            hook_data[bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⍺")] = [{bstack1111l1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⍻"): [bstack1111l1l_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⍼")]}]
    if bstack1lll1lll1ll1_opy_:
        hook_data[bstack1111l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⍽")] = bstack1lll1lll1ll1_opy_.result
        hook_data[bstack1111l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⍾")] = bstack111ll1l1l1l_opy_(bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⍿")], bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⎀")])
        hook_data[bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⎁")] = bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⎂")]
        if hook_data[bstack1111l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⎃")] == bstack1111l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⎄"):
            hook_data[bstack1111l1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⎅")] = bstack11l1lllll1_opy_.bstack111111l1ll_opy_(bstack1lll1lll1ll1_opy_.exception_type)
            hook_data[bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⎆")] = [{bstack1111l1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⎇"): bstack11l111lllll_opy_(bstack1lll1lll1ll1_opy_.exception)}]
    return hook_data
def bstack1llll111111l_opy_(test, bstack111l1l1111_opy_, bstack1llll1111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1111l1l_opy_ (u"ࠪࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ⎈").format(bstack1llll1111_opy_))
    bstack111ll1l1ll_opy_ = bstack1llll1111l11_opy_(test, bstack111l1l1111_opy_, result, call, bstack1llll1111_opy_, outcome)
    driver = getattr(test, bstack1111l1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⎉"), None)
    if bstack1llll1111_opy_ == bstack1111l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⎊") and driver:
        bstack111ll1l1ll_opy_[bstack1111l1l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ⎋")] = bstack11l1lllll1_opy_.bstack111ll11ll1_opy_(driver)
    if bstack1llll1111_opy_ == bstack1111l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⎌"):
        bstack1llll1111_opy_ = bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⎍")
    bstack111l1ll111_opy_ = {
        bstack1111l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⎎"): bstack1llll1111_opy_,
        bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⎏"): bstack111ll1l1ll_opy_
    }
    bstack11l1lllll1_opy_.bstack111lll1l_opy_(bstack111l1ll111_opy_)
    if bstack1llll1111_opy_ == bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⎐"):
        threading.current_thread().bstackTestMeta = {bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⎑"): bstack1111l1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⎒")}
    elif bstack1llll1111_opy_ == bstack1111l1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⎓"):
        threading.current_thread().bstackTestMeta = {bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⎔"): getattr(result, bstack1111l1l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⎕"), bstack1111l1l_opy_ (u"ࠪࠫ⎖"))}
def bstack1llll1111lll_opy_(test, bstack111l1l1111_opy_, bstack1llll1111_opy_, result=None, call=None, outcome=None, bstack1lll1lll1ll1_opy_=None):
    logger.debug(bstack1111l1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡡ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡨࡰࡱ࡮ࠤࡩࡧࡴࡢ࠮ࠣࡩࡻ࡫࡮ࡵࡖࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ⎗").format(bstack1llll1111_opy_))
    hook_data = bstack1llll111l111_opy_(test, bstack111l1l1111_opy_, bstack1llll1111_opy_, result, call, outcome, bstack1lll1lll1ll1_opy_)
    bstack111l1ll111_opy_ = {
        bstack1111l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⎘"): bstack1llll1111_opy_,
        bstack1111l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ⎙"): hook_data
    }
    bstack11l1lllll1_opy_.bstack111lll1l_opy_(bstack111l1ll111_opy_)
def bstack1111ll1ll1_opy_(bstack111l1l1111_opy_):
    if not bstack111l1l1111_opy_:
        return None
    if bstack111l1l1111_opy_.get(bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⎚"), None):
        return getattr(bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⎛")], bstack1111l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⎜"), None)
    return bstack111l1l1111_opy_.get(bstack1111l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⎝"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.LOG, bstack1ll1llll1ll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_.LOG, bstack1ll1llll1ll_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack11l1lllll1_opy_.on():
            return
        places = [bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⎞"), bstack1111l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⎟"), bstack1111l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⎠")]
        logs = []
        for bstack1lll1llll1l1_opy_ in places:
            records = caplog.get_records(bstack1lll1llll1l1_opy_)
            bstack1lll1llllll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⎡") if bstack1lll1llll1l1_opy_ == bstack1111l1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭⎢") else bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⎣")
            bstack1lll1lll1111_opy_ = request.node.nodeid + (bstack1111l1l_opy_ (u"ࠪࠫ⎤") if bstack1lll1llll1l1_opy_ == bstack1111l1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⎥") else bstack1111l1l_opy_ (u"ࠬ࠳ࠧ⎦") + bstack1lll1llll1l1_opy_)
            test_uuid = bstack1111ll1ll1_opy_(_111l1l1l1l_opy_.get(bstack1lll1lll1111_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l111l1lll_opy_(record.message):
                    continue
                logs.append({
                    bstack1111l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⎧"): bstack11l111l1l11_opy_(record.created).isoformat() + bstack1111l1l_opy_ (u"࡛ࠧࠩ⎨"),
                    bstack1111l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⎩"): record.levelname,
                    bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⎪"): record.message,
                    bstack1lll1llllll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack11l1lllll1_opy_.bstack11l11l1l1l_opy_(logs)
    except Exception as err:
        print(bstack1111l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ⎫"), str(err))
def bstack1l11lllll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11111l111_opy_
    bstack11l1111111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ⎬"), None) and bstack1l11l1lll_opy_(
            threading.current_thread(), bstack1111l1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⎭"), None)
    bstack1ll1l111l_opy_ = getattr(driver, bstack1111l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭⎮"), None) != None and getattr(driver, bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⎯"), None) == True
    if sequence == bstack1111l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⎰") and driver != None:
      if not bstack11111l111_opy_ and bstack1l1ll1l1l1l_opy_() and bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⎱") in CONFIG and CONFIG[bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎲")] == True and bstack1ll1ll1ll1_opy_.bstack1ll111l11_opy_(driver_command) and (bstack1ll1l111l_opy_ or bstack11l1111111_opy_) and not bstack1111111l1_opy_(args):
        try:
          bstack11111l111_opy_ = True
          logger.debug(bstack1111l1l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭⎳").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1111l1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ⎴").format(str(err)))
        bstack11111l111_opy_ = False
    if sequence == bstack1111l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ⎵"):
        if driver_command == bstack1111l1l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ⎶"):
            bstack11l1lllll1_opy_.bstack1111l1ll_opy_({
                bstack1111l1l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ⎷"): response[bstack1111l1l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ⎸")],
                bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⎹"): store[bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⎺")]
            })
def bstack11l11l111_opy_():
    global bstack1l11l11l1_opy_
    bstack11l1111l1_opy_.bstack1l11ll1l11_opy_()
    logging.shutdown()
    bstack11l1lllll1_opy_.bstack111l1l11ll_opy_()
    for driver in bstack1l11l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1llll111_opy_(*args):
    global bstack1l11l11l1_opy_
    bstack11l1lllll1_opy_.bstack111l1l11ll_opy_()
    for driver in bstack1l11l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11111lll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l11l1l111_opy_(self, *args, **kwargs):
    bstack11l1l11lll_opy_ = bstack1l1llll11_opy_(self, *args, **kwargs)
    bstack1llll1l1_opy_ = getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⎻"), None)
    if bstack1llll1l1_opy_ and bstack1llll1l1_opy_.get(bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⎼"), bstack1111l1l_opy_ (u"ࠧࠨ⎽")) == bstack1111l1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⎾"):
        bstack11l1lllll1_opy_.bstack111lll1ll_opy_(self)
    return bstack11l1l11lll_opy_
@measure(event_name=EVENTS.bstack1l111l111_opy_, stage=STAGE.bstack1111l11ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1l11l1ll11_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
    if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭⎿")):
        return
    bstack1l1ll11l1_opy_.bstack1ll1l111l1_opy_(bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ⏀"), True)
    global bstack1l111l11l1_opy_
    global bstack11ll11l1l_opy_
    bstack1l111l11l1_opy_ = framework_name
    logger.info(bstack1l11ll1lll_opy_.format(bstack1l111l11l1_opy_.split(bstack1111l1l_opy_ (u"ࠫ࠲࠭⏁"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll1l1l1l_opy_():
            Service.start = bstack111l1l11l_opy_
            Service.stop = bstack1llll1l1l1_opy_
            webdriver.Remote.get = bstack11ll11lll1_opy_
            webdriver.Remote.__init__ = bstack11l1lll1_opy_
            if not isinstance(os.getenv(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭⏂")), str):
                return
            WebDriver.quit = bstack1llll11l1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack11l1lllll1_opy_.on():
            webdriver.Remote.__init__ = bstack1l11l1l111_opy_
        bstack11ll11l1l_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1111l1l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ⏃")):
        bstack11ll11l1l_opy_ = eval(os.environ.get(bstack1111l1l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ⏄")))
    if not bstack11ll11l1l_opy_:
        bstack11l1111ll1_opy_(bstack1111l1l_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ⏅"), bstack111l1ll1_opy_)
    if bstack111llllll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⏆")) and callable(getattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⏇"))):
                RemoteConnection._get_proxy_url = bstack1l1l1l111_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1l1l111_opy_
        except Exception as e:
            logger.error(bstack1ll1l1111_opy_.format(str(e)))
    if bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⏈") in str(framework_name).lower():
        if not bstack1l1ll1l1l1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1111l1lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll1l1_opy_
            Config.getoption = bstack11l11llll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l11l1ll1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1lll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack1llll11l1l_opy_(self):
    global bstack1l111l11l1_opy_
    global bstack11111l1ll_opy_
    global bstack11lllll11l_opy_
    try:
        if bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⏉") in bstack1l111l11l1_opy_ and self.session_id != None and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ⏊"), bstack1111l1l_opy_ (u"ࠧࠨ⏋")) != bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⏌"):
            bstack1l1l11l11l_opy_ = bstack1111l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⏍") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⏎")
            bstack111111ll_opy_(logger, True)
            if os.environ.get(bstack1111l1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⏏"), None):
                self.execute_script(
                    bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ⏐") + json.dumps(
                        os.environ.get(bstack1111l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⏑"))) + bstack1111l1l_opy_ (u"ࠧࡾࡿࠪ⏒"))
            if self != None:
                bstack1l11111l1l_opy_(self, bstack1l1l11l11l_opy_, bstack1111l1l_opy_ (u"ࠨ࠮ࠣࠫ⏓").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll111ll1_opy_(bstack1lll1l11lll_opy_):
            item = store.get(bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⏔"), None)
            if item is not None and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⏕"), None):
                bstack11l1ll1ll1_opy_.bstack1l1l11llll_opy_(self, bstack111111ll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1111l1l_opy_ (u"ࠫࠬ⏖")
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ⏗") + str(e))
    bstack11lllll11l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l11ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11l1lll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11111l1ll_opy_
    global bstack1lllllllll_opy_
    global bstack11llll1lll_opy_
    global bstack1l111l11l1_opy_
    global bstack1l1llll11_opy_
    global bstack1l11l11l1_opy_
    global bstack1l111l1ll_opy_
    global bstack1lll1ll11_opy_
    global bstack111111ll1_opy_
    CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⏘")] = str(bstack1l111l11l1_opy_) + str(__version__)
    command_executor = bstack111llllll1_opy_(bstack1l111l1ll_opy_, CONFIG)
    logger.debug(bstack1l1111ll11_opy_.format(command_executor))
    proxy = bstack11lll111ll_opy_(CONFIG, proxy)
    bstack11lll11l_opy_ = 0
    try:
        if bstack11llll1lll_opy_ is True:
            bstack11lll11l_opy_ = int(os.environ.get(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⏙")))
    except:
        bstack11lll11l_opy_ = 0
    bstack1l1ll1ll1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11lll11l_opy_)
    logger.debug(bstack1ll1ll1l11_opy_.format(str(bstack1l1ll1ll1l_opy_)))
    bstack111111ll1_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⏚"))[bstack11lll11l_opy_]
    if bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⏛") in CONFIG and CONFIG[bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⏜")]:
        bstack1l1lll1l1_opy_(bstack1l1ll1ll1l_opy_, bstack1lll1ll11_opy_)
    if bstack1lll1111l1_opy_.bstack1llll1l1l_opy_(CONFIG, bstack11lll11l_opy_) and bstack1lll1111l1_opy_.bstack1l1lll1lll_opy_(bstack1l1ll1ll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll111ll1_opy_(bstack1lll1l11lll_opy_):
            bstack1lll1111l1_opy_.set_capabilities(bstack1l1ll1ll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll1l1l11_opy_ = bstack1l111111l_opy_(desired_capabilities)
        bstack11ll1l1l11_opy_[bstack1111l1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ⏝")] = bstack11l1l1l11_opy_(CONFIG)
        bstack1llll11ll_opy_ = bstack1lll1111_opy_(bstack11ll1l1l11_opy_)
        if bstack1llll11ll_opy_:
            bstack1l1ll1ll1l_opy_ = update(bstack1llll11ll_opy_, bstack1l1ll1ll1l_opy_)
        desired_capabilities = None
    if options:
        bstack1l111lll_opy_(options, bstack1l1ll1ll1l_opy_)
    if not options:
        options = bstack1l1l1l1l1l_opy_(bstack1l1ll1ll1l_opy_)
    if proxy and bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ⏞")):
        options.proxy(proxy)
    if options and bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⏟")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1l1lll1_opy_() < version.parse(bstack1111l1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⏠")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1ll1ll1l_opy_)
    logger.info(bstack1ll111l1_opy_)
    bstack1lllll1ll_opy_.end(EVENTS.bstack1l111l111_opy_.value, EVENTS.bstack1l111l111_opy_.value + bstack1111l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⏡"),
                               EVENTS.bstack1l111l111_opy_.value + bstack1111l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⏢"), True, None)
    try:
        if bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⏣")):
            bstack1l1llll11_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⏤")):
            bstack1l1llll11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ⏥")):
            bstack1l1llll11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l1llll11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11l1111l_opy_:
        logger.error(bstack11ll1lll1_opy_.format(bstack1111l1l_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠬ⏦"), str(bstack11l1111l_opy_)))
        raise bstack11l1111l_opy_
    try:
        bstack1lllll1ll1_opy_ = bstack1111l1l_opy_ (u"ࠧࠨ⏧")
        if bstack1ll1l1lll1_opy_() >= version.parse(bstack1111l1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩ⏨")):
            bstack1lllll1ll1_opy_ = self.caps.get(bstack1111l1l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ⏩"))
        else:
            bstack1lllll1ll1_opy_ = self.capabilities.get(bstack1111l1l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⏪"))
        if bstack1lllll1ll1_opy_:
            bstack11lllll1l1_opy_(bstack1lllll1ll1_opy_)
            if bstack1ll1l1lll1_opy_() <= version.parse(bstack1111l1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ⏫")):
                self.command_executor._url = bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⏬") + bstack1l111l1ll_opy_ + bstack1111l1l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ⏭")
            else:
                self.command_executor._url = bstack1111l1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ⏮") + bstack1lllll1ll1_opy_ + bstack1111l1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ⏯")
            logger.debug(bstack1lllll1l11_opy_.format(bstack1lllll1ll1_opy_))
        else:
            logger.debug(bstack1l1l111l1l_opy_.format(bstack1111l1l_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ⏰")))
    except Exception as e:
        logger.debug(bstack1l1l111l1l_opy_.format(e))
    bstack11111l1ll_opy_ = self.session_id
    if bstack1111l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⏱") in bstack1l111l11l1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⏲"), None)
        if item:
            bstack1lll1lll1lll_opy_ = getattr(item, bstack1111l1l_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪ⏳"), False)
            if not getattr(item, bstack1111l1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⏴"), None) and bstack1lll1lll1lll_opy_:
                setattr(store[bstack1111l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⏵")], bstack1111l1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⏶"), self)
        bstack1llll1l1_opy_ = getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⏷"), None)
        if bstack1llll1l1_opy_ and bstack1llll1l1_opy_.get(bstack1111l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⏸"), bstack1111l1l_opy_ (u"ࠫࠬ⏹")) == bstack1111l1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⏺"):
            bstack11l1lllll1_opy_.bstack111lll1ll_opy_(self)
    bstack1l11l11l1_opy_.append(self)
    if bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⏻") in CONFIG and bstack1111l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⏼") in CONFIG[bstack1111l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⏽")][bstack11lll11l_opy_]:
        bstack1lllllllll_opy_ = CONFIG[bstack1111l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⏾")][bstack11lll11l_opy_][bstack1111l1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⏿")]
    logger.debug(bstack1l1l1l11l_opy_.format(bstack11111l1ll_opy_))
@measure(event_name=EVENTS.bstack11l11111l_opy_, stage=STAGE.bstack1l1111l1ll_opy_, bstack1ll1l1ll_opy_=bstack1lllllllll_opy_)
def bstack11ll11lll1_opy_(self, url):
    global bstack1111l11l1_opy_
    global CONFIG
    try:
        bstack1l1l1111l1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l111ll1_opy_.format(str(err)))
    try:
        bstack1111l11l1_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll1llll11_opy_ = str(e)
            if any(err_msg in bstack1ll1llll11_opy_ for err_msg in bstack11ll11111_opy_):
                bstack1l1l1111l1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l111ll1_opy_.format(str(err)))
        raise e
def bstack11l111ll11_opy_(item, when):
    global bstack1l1llll11l_opy_
    try:
        bstack1l1llll11l_opy_(item, when)
    except Exception as e:
        pass
def bstack1l11l1ll1_opy_(item, call, rep):
    global bstack1l111111l1_opy_
    global bstack1l11l11l1_opy_
    name = bstack1111l1l_opy_ (u"ࠫࠬ␀")
    try:
        if rep.when == bstack1111l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ␁"):
            bstack11111l1ll_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1111l1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ␂"))
            try:
                if (str(skipSessionName).lower() != bstack1111l1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ␃")):
                    name = str(rep.nodeid)
                    bstack11lll11ll1_opy_ = bstack1ll1l1l1l_opy_(bstack1111l1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ␄"), name, bstack1111l1l_opy_ (u"ࠩࠪ␅"), bstack1111l1l_opy_ (u"ࠪࠫ␆"), bstack1111l1l_opy_ (u"ࠫࠬ␇"), bstack1111l1l_opy_ (u"ࠬ࠭␈"))
                    os.environ[bstack1111l1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ␉")] = name
                    for driver in bstack1l11l11l1_opy_:
                        if bstack11111l1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11lll11ll1_opy_)
            except Exception as e:
                logger.debug(bstack1111l1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ␊").format(str(e)))
            try:
                bstack11l1llllll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ␋"):
                    status = bstack1111l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ␌") if rep.outcome.lower() == bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ␍") else bstack1111l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ␎")
                    reason = bstack1111l1l_opy_ (u"ࠬ࠭␏")
                    if status == bstack1111l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭␐"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1111l1l_opy_ (u"ࠧࡪࡰࡩࡳࠬ␑") if status == bstack1111l1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ␒") else bstack1111l1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ␓")
                    data = name + bstack1111l1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ␔") if status == bstack1111l1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ␕") else name + bstack1111l1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ␖") + reason
                    bstack11l1ll111l_opy_ = bstack1ll1l1l1l_opy_(bstack1111l1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ␗"), bstack1111l1l_opy_ (u"ࠧࠨ␘"), bstack1111l1l_opy_ (u"ࠨࠩ␙"), bstack1111l1l_opy_ (u"ࠩࠪ␚"), level, data)
                    for driver in bstack1l11l11l1_opy_:
                        if bstack11111l1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1ll111l_opy_)
            except Exception as e:
                logger.debug(bstack1111l1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ␛").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ␜").format(str(e)))
    bstack1l111111l1_opy_(item, call, rep)
notset = Notset()
def bstack11l11llll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11lll111l1_opy_
    if str(name).lower() == bstack1111l1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ␝"):
        return bstack1111l1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ␞")
    else:
        return bstack11lll111l1_opy_(self, name, default, skip)
def bstack1l1l1l111_opy_(self):
    global CONFIG
    global bstack1ll1l1llll_opy_
    try:
        proxy = bstack1l11l11ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111l1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ␟")):
                proxies = bstack111ll11l1_opy_(proxy, bstack111llllll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111l111l_opy_ = proxies.popitem()
                    if bstack1111l1l_opy_ (u"ࠣ࠼࠲࠳ࠧ␠") in bstack1l111l111l_opy_:
                        return bstack1l111l111l_opy_
                    else:
                        return bstack1111l1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ␡") + bstack1l111l111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111l1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ␢").format(str(e)))
    return bstack1ll1l1llll_opy_(self)
def bstack111llllll_opy_():
    return (bstack1111l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ␣") in CONFIG or bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ␤") in CONFIG) and bstack1l11l111l1_opy_() and bstack1ll1l1lll1_opy_() >= version.parse(
        bstack1lllll11l_opy_)
def bstack1l1ll1l11_opy_(self,
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
    global bstack1lllllllll_opy_
    global bstack11llll1lll_opy_
    global bstack1l111l11l1_opy_
    CONFIG[bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ␥")] = str(bstack1l111l11l1_opy_) + str(__version__)
    bstack11lll11l_opy_ = 0
    try:
        if bstack11llll1lll_opy_ is True:
            bstack11lll11l_opy_ = int(os.environ.get(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ␦")))
    except:
        bstack11lll11l_opy_ = 0
    CONFIG[bstack1111l1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ␧")] = True
    bstack1l1ll1ll1l_opy_ = bstack1lll1111_opy_(CONFIG, bstack11lll11l_opy_)
    logger.debug(bstack1ll1ll1l11_opy_.format(str(bstack1l1ll1ll1l_opy_)))
    if CONFIG.get(bstack1111l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭␨")):
        bstack1l1lll1l1_opy_(bstack1l1ll1ll1l_opy_, bstack1lll1ll11_opy_)
    if bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭␩") in CONFIG and bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ␪") in CONFIG[bstack1111l1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ␫")][bstack11lll11l_opy_]:
        bstack1lllllllll_opy_ = CONFIG[bstack1111l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ␬")][bstack11lll11l_opy_][bstack1111l1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ␭")]
    import urllib
    import json
    if bstack1111l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ␮") in CONFIG and str(CONFIG[bstack1111l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭␯")]).lower() != bstack1111l1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ␰"):
        bstack11l11lll1l_opy_ = bstack11l11l1111_opy_()
        bstack1lll11l11l_opy_ = bstack11l11lll1l_opy_ + urllib.parse.quote(json.dumps(bstack1l1ll1ll1l_opy_))
    else:
        bstack1lll11l11l_opy_ = bstack1111l1l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭␱") + urllib.parse.quote(json.dumps(bstack1l1ll1ll1l_opy_))
    browser = self.connect(bstack1lll11l11l_opy_)
    return browser
def bstack11ll1l1l1l_opy_():
    global bstack11ll11l1l_opy_
    global bstack1l111l11l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1llll1lll1_opy_
        if not bstack1l1ll1l1l1l_opy_():
            global bstack1l1l111ll1_opy_
            if not bstack1l1l111ll1_opy_:
                from bstack_utils.helper import bstack11l1l1ll1_opy_, bstack1lll111l11_opy_
                bstack1l1l111ll1_opy_ = bstack11l1l1ll1_opy_()
                bstack1lll111l11_opy_(bstack1l111l11l1_opy_)
            BrowserType.connect = bstack1llll1lll1_opy_
            return
        BrowserType.launch = bstack1l1ll1l11_opy_
        bstack11ll11l1l_opy_ = True
    except Exception as e:
        pass
def bstack1lll1ll1lll1_opy_():
    global CONFIG
    global bstack111lll111_opy_
    global bstack1l111l1ll_opy_
    global bstack1lll1ll11_opy_
    global bstack11llll1lll_opy_
    global bstack1l1ll11l1l_opy_
    CONFIG = json.loads(os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ␲")))
    bstack111lll111_opy_ = eval(os.environ.get(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ␳")))
    bstack1l111l1ll_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ␴"))
    bstack1lll1l11_opy_(CONFIG, bstack111lll111_opy_)
    bstack1l1ll11l1l_opy_ = bstack11l1111l1_opy_.configure_logger(CONFIG, bstack1l1ll11l1l_opy_)
    if cli.bstack111llll1l1_opy_():
        bstack11lllll1ll_opy_.invoke(bstack1l111l1111_opy_.CONNECT, bstack11l11l11l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ␵"), bstack1111l1l_opy_ (u"ࠩ࠳ࠫ␶")))
        cli.bstack1lll1111ll1_opy_(cli_context.platform_index)
        cli.bstack1lll11l1111_opy_(bstack111llllll1_opy_(bstack1l111l1ll_opy_, CONFIG), cli_context.platform_index, bstack1l1l1l1l1l_opy_)
        cli.bstack1ll1lll1ll1_opy_()
        logger.debug(bstack1111l1l_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ␷") + str(cli_context.platform_index) + bstack1111l1l_opy_ (u"ࠦࠧ␸"))
        return # skip all existing operations
    global bstack1l1llll11_opy_
    global bstack11lllll11l_opy_
    global bstack1llll1l1ll_opy_
    global bstack1ll1111l11_opy_
    global bstack11l11ll1l1_opy_
    global bstack1l1ll1l1l1_opy_
    global bstack1ll1ll1111_opy_
    global bstack1111l11l1_opy_
    global bstack1ll1l1llll_opy_
    global bstack11lll111l1_opy_
    global bstack1l1llll11l_opy_
    global bstack1l111111l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1llll11_opy_ = webdriver.Remote.__init__
        bstack11lllll11l_opy_ = WebDriver.quit
        bstack1ll1ll1111_opy_ = WebDriver.close
        bstack1111l11l1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1111l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ␹") in CONFIG or bstack1111l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ␺") in CONFIG) and bstack1l11l111l1_opy_():
        if bstack1ll1l1lll1_opy_() < version.parse(bstack1lllll11l_opy_):
            logger.error(bstack11l1111l11_opy_.format(bstack1ll1l1lll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ␻")) and callable(getattr(RemoteConnection, bstack1111l1l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ␼"))):
                    bstack1ll1l1llll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1ll1l1llll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1ll1l1111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11lll111l1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1llll11l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11ll1l1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l111111l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ␽"))
    bstack1lll1ll11_opy_ = CONFIG.get(bstack1111l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ␾"), {}).get(bstack1111l1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭␿"))
    bstack11llll1lll_opy_ = True
    bstack1l11l1ll11_opy_(bstack11l11111_opy_)
if (bstack111lllll111_opy_()):
    bstack1lll1ll1lll1_opy_()
@error_handler(class_method=False)
def bstack1llll111l1l1_opy_(hook_name, event, bstack1l111l1llll_opy_=None):
    if hook_name not in [bstack1111l1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⑀"), bstack1111l1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⑁"), bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⑂"), bstack1111l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⑃"), bstack1111l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⑄"), bstack1111l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⑅"), bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ⑆"), bstack1111l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⑇")]:
        return
    node = store[bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⑈")]
    if hook_name in [bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⑉"), bstack1111l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⑊")]:
        node = store[bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ⑋")]
    elif hook_name in [bstack1111l1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⑌"), bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⑍")]:
        node = store[bstack1111l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ⑎")]
    hook_type = bstack1lllllllll1l_opy_(hook_name)
    if event == bstack1111l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⑏"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_[hook_type], bstack1ll1llll1ll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1l1lll_opy_ = {
            bstack1111l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⑐"): uuid,
            bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⑑"): bstack1ll111ll1l_opy_(),
            bstack1111l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⑒"): bstack1111l1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⑓"),
            bstack1111l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⑔"): hook_type,
            bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⑕"): hook_name
        }
        store[bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⑖")].append(uuid)
        bstack1lll1llll1ll_opy_ = node.nodeid
        if hook_type == bstack1111l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⑗"):
            if not _111l1l1l1l_opy_.get(bstack1lll1llll1ll_opy_, None):
                _111l1l1l1l_opy_[bstack1lll1llll1ll_opy_] = {bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⑘"): []}
            _111l1l1l1l_opy_[bstack1lll1llll1ll_opy_][bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⑙")].append(bstack111l1l1lll_opy_[bstack1111l1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⑚")])
        _111l1l1l1l_opy_[bstack1lll1llll1ll_opy_ + bstack1111l1l_opy_ (u"ࠫ࠲࠭⑛") + hook_name] = bstack111l1l1lll_opy_
        bstack1llll1111lll_opy_(node, bstack111l1l1lll_opy_, bstack1111l1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⑜"))
    elif event == bstack1111l1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ⑝"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lllll1_opy_[hook_type], bstack1ll1llll1ll_opy_.POST, node, None, bstack1l111l1llll_opy_)
            return
        bstack111lll1111_opy_ = node.nodeid + bstack1111l1l_opy_ (u"ࠧ࠮ࠩ⑞") + hook_name
        _111l1l1l1l_opy_[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⑟")] = bstack1ll111ll1l_opy_()
        bstack1llll11111ll_opy_(_111l1l1l1l_opy_[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ①")])
        bstack1llll1111lll_opy_(node, _111l1l1l1l_opy_[bstack111lll1111_opy_], bstack1111l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ②"), bstack1lll1lll1ll1_opy_=bstack1l111l1llll_opy_)
def bstack1lll1lll11l1_opy_():
    global bstack1llll1111ll1_opy_
    if bstack1ll1l1l1l1_opy_():
        bstack1llll1111ll1_opy_ = bstack1111l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ③")
    else:
        bstack1llll1111ll1_opy_ = bstack1111l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ④")
@bstack11l1lllll1_opy_.bstack1llll1l1l1ll_opy_
def bstack1lll1lllll1l_opy_():
    bstack1lll1lll11l1_opy_()
    if cli.is_running():
        try:
            bstack111ll11l1ll_opy_(bstack1llll111l1l1_opy_)
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⑤").format(e))
        return
    if bstack1l11l111l1_opy_():
        bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
        bstack1111l1l_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡀࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡭ࡥࡵࡵࠣࡹࡸ࡫ࡤࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠲ࡽࡲࡢࡲࡳ࡭ࡳ࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡸࠥ࡯ࡳࠡࡲࡤࡸࡨ࡮ࡥࡥࠢ࡬ࡲࠥࡧࠠࡥ࡫ࡩࡪࡪࡸࡥ࡯ࡶࠣࡴࡷࡵࡣࡦࡵࡶࠤ࡮ࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡶࡵࠣࡻࡪࠦ࡮ࡦࡧࡧࠤࡹࡵࠠࡶࡵࡨࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡖࡡࡵࡥ࡫ࠬࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡨࡢࡰࡧࡰࡪࡸࠩࠡࡨࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࠩࠪ⑥")
        if bstack1l1ll11l1_opy_.get_property(bstack1111l1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⑦")):
            if CONFIG.get(bstack1111l1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⑧")) is not None and int(CONFIG[bstack1111l1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⑨")]) > 1:
                bstack11llllll1_opy_(bstack1l11lllll_opy_)
            return
        bstack11llllll1_opy_(bstack1l11lllll_opy_)
    try:
        bstack111ll11l1ll_opy_(bstack1llll111l1l1_opy_)
    except Exception as e:
        logger.debug(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⑩").format(e))
bstack1lll1lllll1l_opy_()