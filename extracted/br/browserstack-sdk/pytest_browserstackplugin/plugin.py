# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l11111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll1ll11_opy_, bstack1lllll1l1_opy_, update, bstack1ll11ll11l_opy_,
                                       bstack11l11lll1_opy_, bstack111ll1ll_opy_, bstack1l1l111ll1_opy_, bstack1l1ll111l_opy_,
                                       bstack1l1l11l11_opy_, bstack1111l1l1_opy_, bstack1l111l1111_opy_,
                                       bstack1ll11l11l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll1lll11_opy_)
from browserstack_sdk.bstack11l11l1ll_opy_ import bstack1ll1ll1l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1l11111_opy_
from bstack_utils.capture import bstack111ll1l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack111111lll_opy_, bstack11lllll11l_opy_, bstack1ll1l11l_opy_, \
    bstack1lll1lllll_opy_
from bstack_utils.helper import bstack1l11l1l1ll_opy_, bstack11l11ll1l11_opy_, bstack111l1111ll_opy_, bstack11l11ll111_opy_, bstack1l1lll11l1l_opy_, bstack11l11ll1l1_opy_, \
    bstack11l11l1111l_opy_, \
    bstack11l11ll1111_opy_, bstack1l1l1ll111_opy_, bstack11ll11llll_opy_, bstack111ll1l1lll_opy_, bstack1l111lll_opy_, Notset, \
    bstack1lll1l1l_opy_, bstack111llll1ll1_opy_, bstack111lll1ll11_opy_, Result, bstack11l11l1ll1l_opy_, bstack111lll11l1l_opy_, error_handler, \
    bstack1l1ll111_opy_, bstack1ll11111l_opy_, bstack11lll1111_opy_, bstack111llllll1l_opy_
from bstack_utils.bstack111ll111lll_opy_ import bstack111ll111l1l_opy_
from bstack_utils.messages import bstack1l1l11ll1l_opy_, bstack1l11l1ll_opy_, bstack1l1111ll1_opy_, bstack1l111l11l1_opy_, bstack1ll1lll111_opy_, \
    bstack1l1lll11_opy_, bstack1l11ll1111_opy_, bstack1ll111ll1l_opy_, bstack11ll11l1_opy_, bstack1lll1lll1_opy_, \
    bstack1l111lllll_opy_, bstack11l1l1lll1_opy_, bstack11l1ll11ll_opy_
from bstack_utils.proxy import bstack1llll1ll1_opy_, bstack11lll11ll1_opy_
from bstack_utils.bstack1ll11l11ll_opy_ import bstack11111111ll1_opy_, bstack1lllllllll11_opy_, bstack1llllllll1ll_opy_, bstack11111111111_opy_, \
    bstack1111111111l_opy_, bstack1lllllllllll_opy_, bstack111111111ll_opy_, bstack11l1111111_opy_, bstack11111111l11_opy_
from bstack_utils.bstack111lll11_opy_ import bstack1ll111l1l_opy_
from bstack_utils.bstack11l1lll111_opy_ import bstack1111ll1ll_opy_, bstack11l11111ll_opy_, bstack11l111l1l_opy_, \
    bstack11l1ll1l_opy_, bstack1ll11ll11_opy_
from bstack_utils.bstack111ll1lll1_opy_ import bstack111ll1l1ll_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack1ll11l1ll1_opy_
import bstack_utils.accessibility as bstack1llllll1l1_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack1lll11111l_opy_
from bstack_utils.bstack1l1ll1lll_opy_ import bstack1l1ll1lll_opy_
from bstack_utils.bstack111l111ll_opy_ import bstack1l11llll1_opy_
from browserstack_sdk.__init__ import bstack1l1lll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l_opy_ import bstack1llll1l1l_opy_, bstack11lll1111l_opy_, bstack1l1l11llll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11lllll1lll_opy_, bstack1ll1lll111l_opy_, bstack1lll111111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1llll1l1l_opy_ import bstack1llll1l1l_opy_, bstack11lll1111l_opy_, bstack1l1l11llll_opy_
bstack1l111l11_opy_ = None
bstack1lll11l1l_opy_ = None
bstack11ll11ll1l_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack1l1111111l_opy_ = None
bstack1l11l1l1l1_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1ll1llll_opy_ = None
bstack11llllll11_opy_ = None
bstack1l1111l111_opy_ = None
bstack11l1l111l1_opy_ = None
bstack11ll1l1ll1_opy_ = None
bstack1ll1lll1ll_opy_ = None
bstack1l11l1l11_opy_ = bstack1111lll_opy_ (u"࠭ࠧ∃")
CONFIG = {}
bstack1111llll1_opy_ = False
bstack1ll11ll1_opy_ = bstack1111lll_opy_ (u"ࠧࠨ∄")
bstack1111l1l1l_opy_ = bstack1111lll_opy_ (u"ࠨࠩ∅")
bstack1l1lll11l1_opy_ = False
bstack1ll1l1111l_opy_ = []
bstack1lll1l1ll1_opy_ = bstack111111lll_opy_
bstack1llll11111l1_opy_ = bstack1111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ∆")
bstack11ll1lll11_opy_ = {}
bstack1lll1lll11_opy_ = None
bstack1l1l1l11_opy_ = False
logger = bstack1l1l11111_opy_.get_logger(__name__, bstack1lll1l1ll1_opy_)
store = {
    bstack1111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ∇"): []
}
bstack1lll1lllll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l111l11_opy_ = {}
current_test_uuid = None
cli_context = bstack11lllll1lll_opy_(
    test_framework_name=bstack1l1l11l1l_opy_[bstack1111lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨ∈")] if bstack1l111lll_opy_() else bstack1l1l11l1l_opy_[bstack1111lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬ∉")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack111ll1lll_opy_(page, bstack1l11l111l_opy_):
    try:
        page.evaluate(bstack1111lll_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ∊"),
                      bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ∋") + json.dumps(
                          bstack1l11l111l_opy_) + bstack1111lll_opy_ (u"ࠣࡿࢀࠦ∌"))
    except Exception as e:
        print(bstack1111lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ∍"), e)
def bstack11l111111_opy_(page, message, level):
    try:
        page.evaluate(bstack1111lll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ∎"), bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ∏") + json.dumps(
            message) + bstack1111lll_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ∐") + json.dumps(level) + bstack1111lll_opy_ (u"࠭ࡽࡾࠩ∑"))
    except Exception as e:
        print(bstack1111lll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥ−"), e)
def pytest_configure(config):
    global bstack1ll11ll1_opy_
    global CONFIG
    bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
    config.args = bstack1ll11l1ll1_opy_.bstack1llll11l1l11_opy_(config.args)
    bstack1ll111ll11_opy_.bstack111111111_opy_(bstack11lll1111_opy_(config.getoption(bstack1111lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ∓"))))
    try:
        bstack1l1l11111_opy_.bstack111l1l1l1l1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1llll1l1l_opy_.invoke(bstack11lll1111l_opy_.CONNECT, bstack1l1l11llll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ∔"), bstack1111lll_opy_ (u"ࠪ࠴ࠬ∕")))
        config = json.loads(os.environ.get(bstack1111lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ∖"), bstack1111lll_opy_ (u"ࠧࢁࡽࠣ∗")))
        cli.bstack1llll11llll_opy_(bstack11ll11llll_opy_(bstack1ll11ll1_opy_, CONFIG), cli_context.platform_index, bstack1ll11ll11l_opy_)
    if cli.bstack1ll1lllllll_opy_(bstack1lll1111l1l_opy_):
        cli.bstack1lll1l11l11_opy_()
        logger.debug(bstack1111lll_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ∘") + str(cli_context.platform_index) + bstack1111lll_opy_ (u"ࠢࠣ∙"))
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.BEFORE_ALL, bstack1lll111111l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1111lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨ√"), None)
    if cli.is_running() and when == bstack1111lll_opy_ (u"ࠤࡦࡥࡱࡲࠢ∛"):
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.LOG_REPORT, bstack1lll111111l_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1111lll_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ∜"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ∝")))
        if not passed:
            config = json.loads(os.environ.get(bstack1111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦ∞"), bstack1111lll_opy_ (u"ࠨࡻࡾࠤ∟")))
            if bstack1l11llll1_opy_.bstack1l1llllll1_opy_(config):
                bstack1111l11111l_opy_ = bstack1l11llll1_opy_.bstack11ll1llll_opy_(config)
                if item.execution_count > bstack1111l11111l_opy_:
                    print(bstack1111lll_opy_ (u"ࠧࡕࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡷ࡫ࡴࡳ࡫ࡨࡷ࠿ࠦࠧ∠"), report.nodeid, os.environ.get(bstack1111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭∡")))
                    bstack1l11llll1_opy_.bstack111l111l1ll_opy_(report.nodeid)
            else:
                print(bstack1111lll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࠩ∢"), report.nodeid, os.environ.get(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ∣")))
                bstack1l11llll1_opy_.bstack111l111l1ll_opy_(report.nodeid)
        else:
            print(bstack1111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡳࡥࡸࡹࡥࡥ࠼ࠣࠫ∤"), report.nodeid, os.environ.get(bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ∥")))
    if cli.is_running():
        if when == bstack1111lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ∦"):
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.BEFORE_EACH, bstack1lll111111l_opy_.POST, item, call, outcome)
        elif when == bstack1111lll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ∧"):
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.LOG_REPORT, bstack1lll111111l_opy_.POST, item, call, outcome)
        elif when == bstack1111lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ∨"):
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.AFTER_EACH, bstack1lll111111l_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ∩"))
    plugins = item.config.getoption(bstack1111lll_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦ∪"))
    report = outcome.get_result()
    os.environ[bstack1111lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ∫")] = report.nodeid
    bstack1lll1llllll1_opy_(item, call, report)
    if bstack1111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥ∬") not in plugins or bstack1l111lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111lll_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢ∭"), None)
    page = getattr(item, bstack1111lll_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨ∮"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll111lll1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll111l111_opy_(item, report, summary, skipSessionName)
def bstack1llll111lll1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ∯") and report.skipped:
        bstack11111111l11_opy_(report)
    if report.when in [bstack1111lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ∰"), bstack1111lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ∱")]:
        return
    if not bstack1l1lll11l1l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1111lll_opy_ (u"ࠫࡹࡸࡵࡦࠩ∲")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ∳") + json.dumps(
                    report.nodeid) + bstack1111lll_opy_ (u"࠭ࡽࡾࠩ∴"))
        os.environ[bstack1111lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ∵")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1111lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣ∶").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111lll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ∷")))
    bstack1l1lllll1l_opy_ = bstack1111lll_opy_ (u"ࠥࠦ∸")
    bstack11111111l11_opy_(report)
    if not passed:
        try:
            bstack1l1lllll1l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ∹").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1lllll1l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1111lll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ∺")))
        bstack1l1lllll1l_opy_ = bstack1111lll_opy_ (u"ࠨࠢ∻")
        if not passed:
            try:
                bstack1l1lllll1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111lll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ∼").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1lllll1l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ∽")
                    + json.dumps(bstack1111lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥ∾"))
                    + bstack1111lll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨ∿")
                )
            else:
                item._driver.execute_script(
                    bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ≀")
                    + json.dumps(str(bstack1l1lllll1l_opy_))
                    + bstack1111lll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ≁")
                )
        except Exception as e:
            summary.append(bstack1111lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦ≂").format(e))
def bstack1llll111ll11_opy_(test_name, error_message):
    try:
        bstack1lll1llll111_opy_ = []
        bstack1111ll11_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ≃"), bstack1111lll_opy_ (u"ࠨ࠲ࠪ≄"))
        bstack1ll1lll1_opy_ = {bstack1111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ≅"): test_name, bstack1111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ≆"): error_message, bstack1111lll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ≇"): bstack1111ll11_opy_}
        bstack1llll111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ≈"))
        if os.path.exists(bstack1llll111l11l_opy_):
            with open(bstack1llll111l11l_opy_) as f:
                bstack1lll1llll111_opy_ = json.load(f)
        bstack1lll1llll111_opy_.append(bstack1ll1lll1_opy_)
        with open(bstack1llll111l11l_opy_, bstack1111lll_opy_ (u"࠭ࡷࠨ≉")) as f:
            json.dump(bstack1lll1llll111_opy_, f)
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬ≊") + str(e))
def bstack1llll111l111_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1111lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ≋"), bstack1111lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ≌")]:
        return
    if (str(skipSessionName).lower() != bstack1111lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ≍")):
        bstack111ll1lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1111lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ≎")))
    bstack1l1lllll1l_opy_ = bstack1111lll_opy_ (u"ࠧࠨ≏")
    bstack11111111l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1lllll1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1111lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ≐").format(e)
                )
        try:
            if passed:
                bstack1ll11ll11_opy_(getattr(item, bstack1111lll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭≑"), None), bstack1111lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ≒"))
            else:
                error_message = bstack1111lll_opy_ (u"ࠩࠪ≓")
                if bstack1l1lllll1l_opy_:
                    bstack11l111111_opy_(item._page, str(bstack1l1lllll1l_opy_), bstack1111lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ≔"))
                    bstack1ll11ll11_opy_(getattr(item, bstack1111lll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ≕"), None), bstack1111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ≖"), str(bstack1l1lllll1l_opy_))
                    error_message = str(bstack1l1lllll1l_opy_)
                else:
                    bstack1ll11ll11_opy_(getattr(item, bstack1111lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ≗"), None), bstack1111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ≘"))
                bstack1llll111ll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1111lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧ≙").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1111lll_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨ≚"), default=bstack1111lll_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ≛"), help=bstack1111lll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ≜"))
    parser.addoption(bstack1111lll_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ≝"), default=bstack1111lll_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ≞"), help=bstack1111lll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ≟"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111lll_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥ≠"), action=bstack1111lll_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣ≡"), default=bstack1111lll_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥ≢"),
                         help=bstack1111lll_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥ≣"))
def bstack111ll1llll_opy_(log):
    if not (log[bstack1111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭≤")] and log[bstack1111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ≥")].strip()):
        return
    active = bstack111ll11ll1_opy_()
    log = {
        bstack1111lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭≦"): log[bstack1111lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ≧")],
        bstack1111lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ≨"): bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"ࠪ࡞ࠬ≩"),
        bstack1111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ≪"): log[bstack1111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭≫")],
    }
    if active:
        if active[bstack1111lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ≬")] == bstack1111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ≭"):
            log[bstack1111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ≮")] = active[bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ≯")]
        elif active[bstack1111lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ≰")] == bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ≱"):
            log[bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ≲")] = active[bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭≳")]
    bstack1lll11111l_opy_.bstack1lll1ll1ll_opy_([log])
def bstack111ll11ll1_opy_():
    if len(store[bstack1111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ≴")]) > 0 and store[bstack1111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ≵")][-1]:
        return {
            bstack1111lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ≶"): bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ≷"),
            bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ≸"): store[bstack1111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ≹")][-1]
        }
    if store.get(bstack1111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ≺"), None):
        return {
            bstack1111lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ≻"): bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭≼"),
            bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ≽"): store[bstack1111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ≾")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.INIT_TEST, bstack1lll111111l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.INIT_TEST, bstack1lll111111l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1lll1llll1l1_opy_ = True
        bstack11l1ll11_opy_ = bstack1llllll1l1_opy_.bstack11llll111l_opy_(bstack11l11ll1111_opy_(item.own_markers))
        if not cli.bstack1ll1lllllll_opy_(bstack1lll1111l1l_opy_):
            item._a11y_test_case = bstack11l1ll11_opy_
            if bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ≿"), None):
                driver = getattr(item, bstack1111lll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⊀"), None)
                item._a11y_started = bstack1llllll1l1_opy_.bstack11111llll_opy_(driver, bstack11l1ll11_opy_)
        if not bstack1lll11111l_opy_.on() or bstack1llll11111l1_opy_ != bstack1111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⊁"):
            return
        global current_test_uuid #, bstack111lll1ll1_opy_
        bstack1111lllll1_opy_ = {
            bstack1111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⊂"): uuid4().__str__(),
            bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⊃"): bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"ࠩ࡝ࠫ⊄")
        }
        current_test_uuid = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⊅")]
        store[bstack1111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⊆")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⊇")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l111l11_opy_[item.nodeid] = {**_111l111l11_opy_[item.nodeid], **bstack1111lllll1_opy_}
        bstack1lll1lll11ll_opy_(item, _111l111l11_opy_[item.nodeid], bstack1111lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⊈"))
    except Exception as err:
        print(bstack1111lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩ⊉"), str(err))
def pytest_runtest_setup(item):
    store[bstack1111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⊊")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.BEFORE_EACH, bstack1lll111111l_opy_.PRE, item, bstack1111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⊋"))
    if bstack1l11llll1_opy_.bstack111l111ll11_opy_():
            bstack1lll1lll1l1l_opy_ = bstack1111lll_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡥࡸࠦࡴࡩࡧࠣࡥࡧࡵࡲࡵࠢࡥࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢ⊌")
            logger.error(bstack1lll1lll1l1l_opy_)
            bstack1111lllll1_opy_ = {
                bstack1111lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⊍"): uuid4().__str__(),
                bstack1111lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊎"): bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"࡚࠭ࠨ⊏"),
                bstack1111lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊐"): bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"ࠨ࡜ࠪ⊑"),
                bstack1111lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊒"): bstack1111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⊓"),
                bstack1111lll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ⊔"): bstack1lll1lll1l1l_opy_,
                bstack1111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⊕"): [],
                bstack1111lll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⊖"): []
            }
            bstack1lll1lll11ll_opy_(item, bstack1111lllll1_opy_, bstack1111lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⊗"))
            pytest.skip(bstack1lll1lll1l1l_opy_)
            return # skip all existing operations
    global bstack1lll1lllll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111ll1l1lll_opy_():
        atexit.register(bstack11l11ll11l_opy_)
        if not bstack1lll1lllll11_opy_:
            try:
                bstack1llll1111l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111llllll1l_opy_():
                    bstack1llll1111l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll1111l1l_opy_:
                    signal.signal(s, bstack1lll1llll1ll_opy_)
                bstack1lll1lllll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤ⊘") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111111ll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1111lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⊙")
    try:
        if not bstack1lll11111l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack1111lllll1_opy_ = {
            bstack1111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⊚"): uuid,
            bstack1111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⊛"): bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"ࠬࡠࠧ⊜"),
            bstack1111lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ⊝"): bstack1111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⊞"),
            bstack1111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⊟"): bstack1111lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⊠"),
            bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⊡"): bstack1111lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⊢")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⊣")] = item
        store[bstack1111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⊤")] = [uuid]
        if not _111l111l11_opy_.get(item.nodeid, None):
            _111l111l11_opy_[item.nodeid] = {bstack1111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⊥"): [], bstack1111lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⊦"): []}
        _111l111l11_opy_[item.nodeid][bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⊧")].append(bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⊨")])
        _111l111l11_opy_[item.nodeid + bstack1111lll_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ⊩")] = bstack1111lllll1_opy_
        bstack1llll111l1l1_opy_(item, bstack1111lllll1_opy_, bstack1111lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⊪"))
    except Exception as err:
        print(bstack1111lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ⊫"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.AFTER_EACH, bstack1lll111111l_opy_.PRE, item, bstack1111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⊬"))
        return # skip all existing operations
    try:
        global bstack11ll1lll11_opy_
        bstack1111ll11_opy_ = 0
        if bstack1l1lll11l1_opy_ is True:
            bstack1111ll11_opy_ = int(os.environ.get(bstack1111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⊭")))
        if bstack1llllllll_opy_.bstack11l1ll11l1_opy_() == bstack1111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⊮"):
            if bstack1llllllll_opy_.bstack11l1lll1_opy_() == bstack1111lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ⊯"):
                bstack1lll1lll11l1_opy_ = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⊰"), None)
                bstack11l11l1l1l_opy_ = bstack1lll1lll11l1_opy_ + bstack1111lll_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣ⊱")
                driver = getattr(item, bstack1111lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⊲"), None)
                bstack1l1111ll1l_opy_ = getattr(item, bstack1111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⊳"), None)
                bstack1l1l11l1_opy_ = getattr(item, bstack1111lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⊴"), None)
                PercySDK.screenshot(driver, bstack11l11l1l1l_opy_, bstack1l1111ll1l_opy_=bstack1l1111ll1l_opy_, bstack1l1l11l1_opy_=bstack1l1l11l1_opy_, bstack111lll1l1_opy_=bstack1111ll11_opy_)
        if not cli.bstack1ll1lllllll_opy_(bstack1lll1111l1l_opy_):
            if getattr(item, bstack1111lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ⊵"), False):
                bstack1ll1ll1l11_opy_.bstack11l11l1lll_opy_(getattr(item, bstack1111lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⊶"), None), bstack11ll1lll11_opy_, logger, item)
        if not bstack1lll11111l_opy_.on():
            return
        bstack1111lllll1_opy_ = {
            bstack1111lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⊷"): uuid4().__str__(),
            bstack1111lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊸"): bstack111l1111ll_opy_().isoformat() + bstack1111lll_opy_ (u"࡚࠭ࠨ⊹"),
            bstack1111lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⊺"): bstack1111lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭⊻"),
            bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⊼"): bstack1111lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⊽"),
            bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⊾"): bstack1111lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⊿")
        }
        _111l111l11_opy_[item.nodeid + bstack1111lll_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⋀")] = bstack1111lllll1_opy_
        bstack1llll111l1l1_opy_(item, bstack1111lllll1_opy_, bstack1111lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⋁"))
    except Exception as err:
        print(bstack1111lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ⋂"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111111111_opy_(fixturedef.argname):
        store[bstack1111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ⋃")] = request.node
    elif bstack1111111111l_opy_(fixturedef.argname):
        store[bstack1111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⋄")] = request.node
    if not bstack1lll11111l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.SETUP_FIXTURE, bstack1lll111111l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.SETUP_FIXTURE, bstack1lll111111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.SETUP_FIXTURE, bstack1lll111111l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.SETUP_FIXTURE, bstack1lll111111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⋅"): fixturedef.argname,
            bstack1111lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⋆"): bstack11l11l1111l_opy_(outcome),
            bstack1111lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⋇"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⋈")]
        if not _111l111l11_opy_.get(current_test_item.nodeid, None):
            _111l111l11_opy_[current_test_item.nodeid] = {bstack1111lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⋉"): []}
        _111l111l11_opy_[current_test_item.nodeid][bstack1111lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⋊")].append(fixture)
    except Exception as err:
        logger.debug(bstack1111lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭⋋"), str(err))
if bstack1l111lll_opy_() and bstack1lll11111l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.STEP, bstack1lll111111l_opy_.PRE, request, step)
            return
        try:
            _111l111l11_opy_[request.node.nodeid][bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⋌")].bstack11lll1l11l_opy_(id(step))
        except Exception as err:
            print(bstack1111lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ⋍"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.STEP, bstack1lll111111l_opy_.POST, request, step, exception)
            return
        try:
            _111l111l11_opy_[request.node.nodeid][bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⋎")].bstack111ll11l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1111lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ⋏"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.STEP, bstack1lll111111l_opy_.POST, request, step)
            return
        try:
            bstack111ll1lll1_opy_: bstack111ll1l1ll_opy_ = _111l111l11_opy_[request.node.nodeid][bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⋐")]
            bstack111ll1lll1_opy_.bstack111ll11l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1111lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭⋑"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll11111l1_opy_
        try:
            if not bstack1lll11111l_opy_.on() or bstack1llll11111l1_opy_ != bstack1111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⋒"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ⋓"), None)
            if not _111l111l11_opy_.get(request.node.nodeid, None):
                _111l111l11_opy_[request.node.nodeid] = {}
            bstack111ll1lll1_opy_ = bstack111ll1l1ll_opy_.bstack1lllll11ll11_opy_(
                scenario, feature, request.node,
                name=bstack1lllllllllll_opy_(request.node, scenario),
                started_at=bstack11l11ll1l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1111lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ⋔"),
                tags=bstack111111111ll_opy_(feature, scenario),
                bstack111ll11lll_opy_=bstack1lll11111l_opy_.bstack111ll111l1_opy_(driver) if driver and driver.session_id else {}
            )
            _111l111l11_opy_[request.node.nodeid][bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⋕")] = bstack111ll1lll1_opy_
            bstack1llll111ll1l_opy_(bstack111ll1lll1_opy_.uuid)
            bstack1lll11111l_opy_.bstack111llll111_opy_(bstack1111lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⋖"), bstack111ll1lll1_opy_)
        except Exception as err:
            print(bstack1111lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ⋗"), str(err))
def bstack1lll1lll1ll1_opy_(bstack111ll11l11_opy_):
    if bstack111ll11l11_opy_ in store[bstack1111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⋘")]:
        store[bstack1111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⋙")].remove(bstack111ll11l11_opy_)
def bstack1llll111ll1l_opy_(test_uuid):
    store[bstack1111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⋚")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1lll11111l_opy_.bstack1llll1l111ll_opy_
def bstack1lll1llllll1_opy_(item, call, report):
    logger.debug(bstack1111lll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ⋛"))
    global bstack1llll11111l1_opy_
    bstack1lll1l1111_opy_ = bstack11l11ll1l1_opy_()
    if hasattr(report, bstack1111lll_opy_ (u"࠭ࡳࡵࡱࡳࠫ⋜")):
        bstack1lll1l1111_opy_ = bstack11l11l1ll1l_opy_(report.stop)
    elif hasattr(report, bstack1111lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭⋝")):
        bstack1lll1l1111_opy_ = bstack11l11l1ll1l_opy_(report.start)
    try:
        if getattr(report, bstack1111lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⋞"), bstack1111lll_opy_ (u"ࠩࠪ⋟")) == bstack1111lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⋠"):
            logger.debug(bstack1111lll_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭⋡").format(getattr(report, bstack1111lll_opy_ (u"ࠬࡽࡨࡦࡰࠪ⋢"), bstack1111lll_opy_ (u"࠭ࠧ⋣")).__str__(), bstack1llll11111l1_opy_))
            if bstack1llll11111l1_opy_ == bstack1111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⋤"):
                _111l111l11_opy_[item.nodeid][bstack1111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⋥")] = bstack1lll1l1111_opy_
                bstack1lll1lll11ll_opy_(item, _111l111l11_opy_[item.nodeid], bstack1111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⋦"), report, call)
                store[bstack1111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⋧")] = None
            elif bstack1llll11111l1_opy_ == bstack1111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ⋨"):
                bstack111ll1lll1_opy_ = _111l111l11_opy_[item.nodeid][bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⋩")]
                bstack111ll1lll1_opy_.set(hooks=_111l111l11_opy_[item.nodeid].get(bstack1111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⋪"), []))
                exception, bstack111ll111ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111ll111ll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1111lll_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭⋫"), bstack1111lll_opy_ (u"ࠨࠩ⋬"))]
                bstack111ll1lll1_opy_.stop(time=bstack1lll1l1111_opy_, result=Result(result=getattr(report, bstack1111lll_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⋭"), bstack1111lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⋮")), exception=exception, bstack111ll111ll_opy_=bstack111ll111ll_opy_))
                bstack1lll11111l_opy_.bstack111llll111_opy_(bstack1111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⋯"), _111l111l11_opy_[item.nodeid][bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⋰")])
        elif getattr(report, bstack1111lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⋱"), bstack1111lll_opy_ (u"ࠧࠨ⋲")) in [bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⋳"), bstack1111lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⋴")]:
            logger.debug(bstack1111lll_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⋵").format(getattr(report, bstack1111lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⋶"), bstack1111lll_opy_ (u"ࠬ࠭⋷")).__str__(), bstack1llll11111l1_opy_))
            bstack111lll1111_opy_ = item.nodeid + bstack1111lll_opy_ (u"࠭࠭ࠨ⋸") + getattr(report, bstack1111lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⋹"), bstack1111lll_opy_ (u"ࠨࠩ⋺"))
            if getattr(report, bstack1111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⋻"), False):
                hook_type = bstack1111lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⋼") if getattr(report, bstack1111lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⋽"), bstack1111lll_opy_ (u"ࠬ࠭⋾")) == bstack1111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⋿") else bstack1111lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⌀")
                _111l111l11_opy_[bstack111lll1111_opy_] = {
                    bstack1111lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⌁"): uuid4().__str__(),
                    bstack1111lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⌂"): bstack1lll1l1111_opy_,
                    bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⌃"): hook_type
                }
            _111l111l11_opy_[bstack111lll1111_opy_][bstack1111lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⌄")] = bstack1lll1l1111_opy_
            bstack1lll1lll1ll1_opy_(_111l111l11_opy_[bstack111lll1111_opy_][bstack1111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⌅")])
            bstack1llll111l1l1_opy_(item, _111l111l11_opy_[bstack111lll1111_opy_], bstack1111lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⌆"), report, call)
            if getattr(report, bstack1111lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⌇"), bstack1111lll_opy_ (u"ࠨࠩ⌈")) == bstack1111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⌉"):
                if getattr(report, bstack1111lll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⌊"), bstack1111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⌋")) == bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⌌"):
                    bstack1111lllll1_opy_ = {
                        bstack1111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⌍"): uuid4().__str__(),
                        bstack1111lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⌎"): bstack11l11ll1l1_opy_(),
                        bstack1111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⌏"): bstack11l11ll1l1_opy_()
                    }
                    _111l111l11_opy_[item.nodeid] = {**_111l111l11_opy_[item.nodeid], **bstack1111lllll1_opy_}
                    bstack1lll1lll11ll_opy_(item, _111l111l11_opy_[item.nodeid], bstack1111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⌐"))
                    bstack1lll1lll11ll_opy_(item, _111l111l11_opy_[item.nodeid], bstack1111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⌑"), report, call)
    except Exception as err:
        print(bstack1111lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ⌒"), str(err))
def bstack1llll1111lll_opy_(test, bstack1111lllll1_opy_, result=None, call=None, bstack1lllll111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111ll1lll1_opy_ = {
        bstack1111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⌓"): bstack1111lllll1_opy_[bstack1111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⌔")],
        bstack1111lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⌕"): bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭⌖"),
        bstack1111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⌗"): test.name,
        bstack1111lll_opy_ (u"ࠪࡦࡴࡪࡹࠨ⌘"): {
            bstack1111lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⌙"): bstack1111lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⌚"),
            bstack1111lll_opy_ (u"࠭ࡣࡰࡦࡨࠫ⌛"): inspect.getsource(test.obj)
        },
        bstack1111lll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⌜"): test.name,
        bstack1111lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⌝"): test.name,
        bstack1111lll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⌞"): bstack1ll11l1ll1_opy_.bstack111l111l1l_opy_(test),
        bstack1111lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⌟"): file_path,
        bstack1111lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⌠"): file_path,
        bstack1111lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⌡"): bstack1111lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⌢"),
        bstack1111lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⌣"): file_path,
        bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⌤"): bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⌥")],
        bstack1111lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⌦"): bstack1111lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⌧"),
        bstack1111lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⌨"): {
            bstack1111lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ〈"): test.nodeid
        },
        bstack1111lll_opy_ (u"ࠧࡵࡣࡪࡷࠬ〉"): bstack11l11ll1111_opy_(test.own_markers)
    }
    if bstack1lllll111_opy_ in [bstack1111lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⌫"), bstack1111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⌬")]:
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠪࡱࡪࡺࡡࠨ⌭")] = {
            bstack1111lll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⌮"): bstack1111lllll1_opy_.get(bstack1111lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⌯"), [])
        }
    if bstack1lllll111_opy_ == bstack1111lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⌰"):
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⌱")] = bstack1111lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⌲")
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⌳")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⌴")]
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⌵")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⌶")]
    if result:
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⌷")] = result.outcome
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⌸")] = result.duration * 1000
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⌹")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⌺")]
        if result.failed:
            bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⌻")] = bstack1lll11111l_opy_.bstack111111ll1l_opy_(call.excinfo.typename)
            bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⌼")] = bstack1lll11111l_opy_.bstack1llll1l1l11l_opy_(call.excinfo, result)
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⌽")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⌾")]
    if outcome:
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⌿")] = bstack11l11l1111l_opy_(outcome)
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⍀")] = 0
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⍁")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⍂")]
        if bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⍃")] == bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⍄"):
            bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⍅")] = bstack1111lll_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⍆")  # bstack1llll1111ll1_opy_
            bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⍇")] = [{bstack1111lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⍈"): [bstack1111lll_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⍉")]}]
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⍊")] = bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⍋")]
    return bstack111ll1lll1_opy_
def bstack1llll111l1ll_opy_(test, bstack111l1ll1ll_opy_, bstack1lllll111_opy_, result, call, outcome, bstack1lll1lllllll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⍌")]
    hook_name = bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⍍")]
    hook_data = {
        bstack1111lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⍎"): bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⍏")],
        bstack1111lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⍐"): bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⍑"),
        bstack1111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⍒"): bstack1111lll_opy_ (u"࠭ࡻࡾࠩ⍓").format(bstack1lllllllll11_opy_(hook_name)),
        bstack1111lll_opy_ (u"ࠧࡣࡱࡧࡽࠬ⍔"): {
            bstack1111lll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⍕"): bstack1111lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⍖"),
            bstack1111lll_opy_ (u"ࠪࡧࡴࡪࡥࠨ⍗"): None
        },
        bstack1111lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⍘"): test.name,
        bstack1111lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⍙"): bstack1ll11l1ll1_opy_.bstack111l111l1l_opy_(test, hook_name),
        bstack1111lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⍚"): file_path,
        bstack1111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⍛"): file_path,
        bstack1111lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⍜"): bstack1111lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⍝"),
        bstack1111lll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⍞"): file_path,
        bstack1111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⍟"): bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⍠")],
        bstack1111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⍡"): bstack1111lll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ⍢") if bstack1llll11111l1_opy_ == bstack1111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⍣") else bstack1111lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⍤"),
        bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⍥"): hook_type
    }
    bstack1ll1111lll1_opy_ = bstack1111lll11l_opy_(_111l111l11_opy_.get(test.nodeid, None))
    if bstack1ll1111lll1_opy_:
        hook_data[bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ⍦")] = bstack1ll1111lll1_opy_
    if result:
        hook_data[bstack1111lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⍧")] = result.outcome
        hook_data[bstack1111lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⍨")] = result.duration * 1000
        hook_data[bstack1111lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⍩")] = bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⍪")]
        if result.failed:
            hook_data[bstack1111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⍫")] = bstack1lll11111l_opy_.bstack111111ll1l_opy_(call.excinfo.typename)
            hook_data[bstack1111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⍬")] = bstack1lll11111l_opy_.bstack1llll1l1l11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1111lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⍭")] = bstack11l11l1111l_opy_(outcome)
        hook_data[bstack1111lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⍮")] = 100
        hook_data[bstack1111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⍯")] = bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⍰")]
        if hook_data[bstack1111lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⍱")] == bstack1111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⍲"):
            hook_data[bstack1111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⍳")] = bstack1111lll_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ⍴")  # bstack1llll1111ll1_opy_
            hook_data[bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⍵")] = [{bstack1111lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⍶"): [bstack1111lll_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ⍷")]}]
    if bstack1lll1lllllll_opy_:
        hook_data[bstack1111lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⍸")] = bstack1lll1lllllll_opy_.result
        hook_data[bstack1111lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⍹")] = bstack111llll1ll1_opy_(bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⍺")], bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⍻")])
        hook_data[bstack1111lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⍼")] = bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⍽")]
        if hook_data[bstack1111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⍾")] == bstack1111lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⍿"):
            hook_data[bstack1111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⎀")] = bstack1lll11111l_opy_.bstack111111ll1l_opy_(bstack1lll1lllllll_opy_.exception_type)
            hook_data[bstack1111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⎁")] = [{bstack1111lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⎂"): bstack111lll1ll11_opy_(bstack1lll1lllllll_opy_.exception)}]
    return hook_data
def bstack1lll1lll11ll_opy_(test, bstack1111lllll1_opy_, bstack1lllll111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1111lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⎃").format(bstack1lllll111_opy_))
    bstack111ll1lll1_opy_ = bstack1llll1111lll_opy_(test, bstack1111lllll1_opy_, result, call, bstack1lllll111_opy_, outcome)
    driver = getattr(test, bstack1111lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⎄"), None)
    if bstack1lllll111_opy_ == bstack1111lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⎅") and driver:
        bstack111ll1lll1_opy_[bstack1111lll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ⎆")] = bstack1lll11111l_opy_.bstack111ll111l1_opy_(driver)
    if bstack1lllll111_opy_ == bstack1111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⎇"):
        bstack1lllll111_opy_ = bstack1111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⎈")
    bstack111l11l11l_opy_ = {
        bstack1111lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⎉"): bstack1lllll111_opy_,
        bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⎊"): bstack111ll1lll1_opy_
    }
    bstack1lll11111l_opy_.bstack1ll1l1lll1_opy_(bstack111l11l11l_opy_)
    if bstack1lllll111_opy_ == bstack1111lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⎋"):
        threading.current_thread().bstackTestMeta = {bstack1111lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⎌"): bstack1111lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⎍")}
    elif bstack1lllll111_opy_ == bstack1111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⎎"):
        threading.current_thread().bstackTestMeta = {bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⎏"): getattr(result, bstack1111lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⎐"), bstack1111lll_opy_ (u"ࠬ࠭⎑"))}
def bstack1llll111l1l1_opy_(test, bstack1111lllll1_opy_, bstack1lllll111_opy_, result=None, call=None, outcome=None, bstack1lll1lllllll_opy_=None):
    logger.debug(bstack1111lll_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⎒").format(bstack1lllll111_opy_))
    hook_data = bstack1llll111l1ll_opy_(test, bstack1111lllll1_opy_, bstack1lllll111_opy_, result, call, outcome, bstack1lll1lllllll_opy_)
    bstack111l11l11l_opy_ = {
        bstack1111lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⎓"): bstack1lllll111_opy_,
        bstack1111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ⎔"): hook_data
    }
    bstack1lll11111l_opy_.bstack1ll1l1lll1_opy_(bstack111l11l11l_opy_)
def bstack1111lll11l_opy_(bstack1111lllll1_opy_):
    if not bstack1111lllll1_opy_:
        return None
    if bstack1111lllll1_opy_.get(bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⎕"), None):
        return getattr(bstack1111lllll1_opy_[bstack1111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⎖")], bstack1111lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎗"), None)
    return bstack1111lllll1_opy_.get(bstack1111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⎘"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.LOG, bstack1lll111111l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_.LOG, bstack1lll111111l_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack1lll11111l_opy_.on():
            return
        places = [bstack1111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⎙"), bstack1111lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⎚"), bstack1111lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⎛")]
        logs = []
        for bstack1llll1111111_opy_ in places:
            records = caplog.get_records(bstack1llll1111111_opy_)
            bstack1llll1111l11_opy_ = bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⎜") if bstack1llll1111111_opy_ == bstack1111lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⎝") else bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⎞")
            bstack1llll11111ll_opy_ = request.node.nodeid + (bstack1111lll_opy_ (u"ࠬ࠭⎟") if bstack1llll1111111_opy_ == bstack1111lll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⎠") else bstack1111lll_opy_ (u"ࠧ࠮ࠩ⎡") + bstack1llll1111111_opy_)
            test_uuid = bstack1111lll11l_opy_(_111l111l11_opy_.get(bstack1llll11111ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111lll11l1l_opy_(record.message):
                    continue
                logs.append({
                    bstack1111lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⎢"): bstack11l11ll1l11_opy_(record.created).isoformat() + bstack1111lll_opy_ (u"ࠩ࡝ࠫ⎣"),
                    bstack1111lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⎤"): record.levelname,
                    bstack1111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⎥"): record.message,
                    bstack1llll1111l11_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1lll11111l_opy_.bstack1lll1ll1ll_opy_(logs)
    except Exception as err:
        print(bstack1111lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ⎦"), str(err))
def bstack11l1111l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l1l11_opy_
    bstack1l1l11ll_opy_ = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ⎧"), None) and bstack1l11l1l1ll_opy_(
            threading.current_thread(), bstack1111lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⎨"), None)
    bstack1111l1111_opy_ = getattr(driver, bstack1111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⎩"), None) != None and getattr(driver, bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⎪"), None) == True
    if sequence == bstack1111lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⎫") and driver != None:
      if not bstack1l1l1l11_opy_ and bstack1l1lll11l1l_opy_() and bstack1111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎬") in CONFIG and CONFIG[bstack1111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⎭")] == True and bstack1l1ll1lll_opy_.bstack1lll1l1l1l_opy_(driver_command) and (bstack1111l1111_opy_ or bstack1l1l11ll_opy_) and not bstack1ll1lll11_opy_(args):
        try:
          bstack1l1l1l11_opy_ = True
          logger.debug(bstack1111lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ⎮").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1111lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ⎯").format(str(err)))
        bstack1l1l1l11_opy_ = False
    if sequence == bstack1111lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⎰"):
        if driver_command == bstack1111lll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭⎱"):
            bstack1lll11111l_opy_.bstack1ll1ll11ll_opy_({
                bstack1111lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ⎲"): response[bstack1111lll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ⎳")],
                bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⎴"): store[bstack1111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⎵")]
            })
def bstack11l11ll11l_opy_():
    global bstack1ll1l1111l_opy_
    bstack1l1l11111_opy_.bstack1ll1l11111_opy_()
    logging.shutdown()
    bstack1lll11111l_opy_.bstack111l1l1ll1_opy_()
    for driver in bstack1ll1l1111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1llll1ll_opy_(*args):
    global bstack1ll1l1111l_opy_
    bstack1lll11111l_opy_.bstack111l1l1ll1_opy_()
    for driver in bstack1ll1l1111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll111_opy_, stage=STAGE.bstack11111lll_opy_, bstack11llllll1_opy_=bstack1lll1lll11_opy_)
def bstack1lllll11l1_opy_(self, *args, **kwargs):
    bstack11l11llll1_opy_ = bstack1l111l11_opy_(self, *args, **kwargs)
    bstack11lll1l1ll_opy_ = getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⎶"), None)
    if bstack11lll1l1ll_opy_ and bstack11lll1l1ll_opy_.get(bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⎷"), bstack1111lll_opy_ (u"ࠩࠪ⎸")) == bstack1111lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⎹"):
        bstack1lll11111l_opy_.bstack11l1lll1l_opy_(self)
    return bstack11l11llll1_opy_
@measure(event_name=EVENTS.bstack1l11ll1l_opy_, stage=STAGE.bstack1l1l1l111l_opy_, bstack11llllll1_opy_=bstack1lll1lll11_opy_)
def bstack1lllll11l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
    if bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⎺")):
        return
    bstack1ll111ll11_opy_.bstack11111l1l_opy_(bstack1111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⎻"), True)
    global bstack1l11l1l11_opy_
    global bstack1l11l11ll_opy_
    bstack1l11l1l11_opy_ = framework_name
    logger.info(bstack11l1l1lll1_opy_.format(bstack1l11l1l11_opy_.split(bstack1111lll_opy_ (u"࠭࠭ࠨ⎼"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lll11l1l_opy_():
            Service.start = bstack1l1l111ll1_opy_
            Service.stop = bstack1l1ll111l_opy_
            webdriver.Remote.get = bstack1l1lllll1_opy_
            webdriver.Remote.__init__ = bstack11ll11ll_opy_
            if not isinstance(os.getenv(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ⎽")), str):
                return
            WebDriver.quit = bstack11ll1l1l1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1lll11111l_opy_.on():
            webdriver.Remote.__init__ = bstack1lllll11l1_opy_
        bstack1l11l11ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1111lll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭⎾")):
        bstack1l11l11ll_opy_ = eval(os.environ.get(bstack1111lll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⎿")))
    if not bstack1l11l11ll_opy_:
        bstack1111l1l1_opy_(bstack1111lll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ⏀"), bstack1l111lllll_opy_)
    if bstack11lllll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1111lll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⏁")) and callable(getattr(RemoteConnection, bstack1111lll_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⏂"))):
                RemoteConnection._get_proxy_url = bstack1ll1ll1l1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1ll1ll1l1_opy_
        except Exception as e:
            logger.error(bstack1l1lll11_opy_.format(str(e)))
    if bstack1111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⏃") in str(framework_name).lower():
        if not bstack1l1lll11l1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l11lll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll1ll_opy_
            Config.getoption = bstack11llll11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l111ll1ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111l1ll1l_opy_, stage=STAGE.bstack11111lll_opy_, bstack11llllll1_opy_=bstack1lll1lll11_opy_)
def bstack11ll1l1l1l_opy_(self):
    global bstack1l11l1l11_opy_
    global bstack11l1111ll1_opy_
    global bstack1lll11l1l_opy_
    try:
        if bstack1111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⏄") in bstack1l11l1l11_opy_ and self.session_id != None and bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ⏅"), bstack1111lll_opy_ (u"ࠩࠪ⏆")) != bstack1111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⏇"):
            bstack11lll11ll_opy_ = bstack1111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⏈") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⏉")
            bstack1ll11111l_opy_(logger, True)
            if os.environ.get(bstack1111lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⏊"), None):
                self.execute_script(
                    bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ⏋") + json.dumps(
                        os.environ.get(bstack1111lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⏌"))) + bstack1111lll_opy_ (u"ࠩࢀࢁࠬ⏍"))
            if self != None:
                bstack11l1ll1l_opy_(self, bstack11lll11ll_opy_, bstack1111lll_opy_ (u"ࠪ࠰ࠥ࠭⏎").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll1lllllll_opy_(bstack1lll1111l1l_opy_):
            item = store.get(bstack1111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⏏"), None)
            if item is not None and bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⏐"), None):
                bstack1ll1ll1l11_opy_.bstack11l11l1lll_opy_(self, bstack11ll1lll11_opy_, logger, item)
        threading.current_thread().testStatus = bstack1111lll_opy_ (u"࠭ࠧ⏑")
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ⏒") + str(e))
    bstack1lll11l1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack11111lll_opy_, bstack11llllll1_opy_=bstack1lll1lll11_opy_)
def bstack11ll11ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11l1111ll1_opy_
    global bstack1lll1lll11_opy_
    global bstack1l1lll11l1_opy_
    global bstack1l11l1l11_opy_
    global bstack1l111l11_opy_
    global bstack1ll1l1111l_opy_
    global bstack1ll11ll1_opy_
    global bstack1111l1l1l_opy_
    global bstack11ll1lll11_opy_
    CONFIG[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ⏓")] = str(bstack1l11l1l11_opy_) + str(__version__)
    command_executor = bstack11ll11llll_opy_(bstack1ll11ll1_opy_, CONFIG)
    logger.debug(bstack1l111l11l1_opy_.format(command_executor))
    proxy = bstack1ll11l11l_opy_(CONFIG, proxy)
    bstack1111ll11_opy_ = 0
    try:
        if bstack1l1lll11l1_opy_ is True:
            bstack1111ll11_opy_ = int(os.environ.get(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⏔")))
    except:
        bstack1111ll11_opy_ = 0
    bstack1ll11ll1l_opy_ = bstack1l1ll1ll11_opy_(CONFIG, bstack1111ll11_opy_)
    logger.debug(bstack1ll111ll1l_opy_.format(str(bstack1ll11ll1l_opy_)))
    bstack11ll1lll11_opy_ = CONFIG.get(bstack1111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⏕"))[bstack1111ll11_opy_]
    if bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⏖") in CONFIG and CONFIG[bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⏗")]:
        bstack11l111l1l_opy_(bstack1ll11ll1l_opy_, bstack1111l1l1l_opy_)
    if bstack1llllll1l1_opy_.bstack1l1l1lll1l_opy_(CONFIG, bstack1111ll11_opy_) and bstack1llllll1l1_opy_.bstack1111111l_opy_(bstack1ll11ll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll1lllllll_opy_(bstack1lll1111l1l_opy_):
            bstack1llllll1l1_opy_.set_capabilities(bstack1ll11ll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack1l11llll11_opy_ = bstack1lllll1l1_opy_(desired_capabilities)
        bstack1l11llll11_opy_[bstack1111lll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭⏘")] = bstack1lll1l1l_opy_(CONFIG)
        bstack11ll1lll1_opy_ = bstack1l1ll1ll11_opy_(bstack1l11llll11_opy_)
        if bstack11ll1lll1_opy_:
            bstack1ll11ll1l_opy_ = update(bstack11ll1lll1_opy_, bstack1ll11ll1l_opy_)
        desired_capabilities = None
    if options:
        bstack1l1l11l11_opy_(options, bstack1ll11ll1l_opy_)
    if not options:
        options = bstack1ll11ll11l_opy_(bstack1ll11ll1l_opy_)
    if proxy and bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⏙")):
        options.proxy(proxy)
    if options and bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⏚")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1l1ll111_opy_() < version.parse(bstack1111lll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⏛")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll11ll1l_opy_)
    logger.info(bstack1l1111ll1_opy_)
    bstack11l11111_opy_.end(EVENTS.bstack1l11ll1l_opy_.value, EVENTS.bstack1l11ll1l_opy_.value + bstack1111lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⏜"),
                               EVENTS.bstack1l11ll1l_opy_.value + bstack1111lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⏝"), True, None)
    try:
        if bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ⏞")):
            bstack1l111l11_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⏟")):
            bstack1l111l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ⏠")):
            bstack1l111l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l111l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1l111l11ll_opy_:
        logger.error(bstack11l1ll11ll_opy_.format(bstack1111lll_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠧ⏡"), str(bstack1l111l11ll_opy_)))
        raise bstack1l111l11ll_opy_
    try:
        bstack111l11ll1_opy_ = bstack1111lll_opy_ (u"ࠩࠪ⏢")
        if bstack1l1l1ll111_opy_() >= version.parse(bstack1111lll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ⏣")):
            bstack111l11ll1_opy_ = self.caps.get(bstack1111lll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⏤"))
        else:
            bstack111l11ll1_opy_ = self.capabilities.get(bstack1111lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⏥"))
        if bstack111l11ll1_opy_:
            bstack1l1ll111_opy_(bstack111l11ll1_opy_)
            if bstack1l1l1ll111_opy_() <= version.parse(bstack1111lll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭⏦")):
                self.command_executor._url = bstack1111lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⏧") + bstack1ll11ll1_opy_ + bstack1111lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ⏨")
            else:
                self.command_executor._url = bstack1111lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ⏩") + bstack111l11ll1_opy_ + bstack1111lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ⏪")
            logger.debug(bstack1l11l1ll_opy_.format(bstack111l11ll1_opy_))
        else:
            logger.debug(bstack1l1l11ll1l_opy_.format(bstack1111lll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧ⏫")))
    except Exception as e:
        logger.debug(bstack1l1l11ll1l_opy_.format(e))
    bstack11l1111ll1_opy_ = self.session_id
    if bstack1111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⏬") in bstack1l11l1l11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⏭"), None)
        if item:
            bstack1lll1lll1l11_opy_ = getattr(item, bstack1111lll_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ⏮"), False)
            if not getattr(item, bstack1111lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⏯"), None) and bstack1lll1lll1l11_opy_:
                setattr(store[bstack1111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⏰")], bstack1111lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⏱"), self)
        bstack11lll1l1ll_opy_ = getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ⏲"), None)
        if bstack11lll1l1ll_opy_ and bstack11lll1l1ll_opy_.get(bstack1111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⏳"), bstack1111lll_opy_ (u"࠭ࠧ⏴")) == bstack1111lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⏵"):
            bstack1lll11111l_opy_.bstack11l1lll1l_opy_(self)
    bstack1ll1l1111l_opy_.append(self)
    if bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⏶") in CONFIG and bstack1111lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⏷") in CONFIG[bstack1111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⏸")][bstack1111ll11_opy_]:
        bstack1lll1lll11_opy_ = CONFIG[bstack1111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⏹")][bstack1111ll11_opy_][bstack1111lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⏺")]
    logger.debug(bstack1lll1lll1_opy_.format(bstack11l1111ll1_opy_))
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack11111lll_opy_, bstack11llllll1_opy_=bstack1lll1lll11_opy_)
def bstack1l1lllll1_opy_(self, url):
    global bstack11llllll11_opy_
    global CONFIG
    try:
        bstack11l11111ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll11l1_opy_.format(str(err)))
    try:
        bstack11llllll11_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11111111_opy_ = str(e)
            if any(err_msg in bstack1l11111111_opy_ for err_msg in bstack1ll1l11l_opy_):
                bstack11l11111ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll11l1_opy_.format(str(err)))
        raise e
def bstack111l1l11l_opy_(item, when):
    global bstack11ll1l1ll1_opy_
    try:
        bstack11ll1l1ll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l111ll1ll_opy_(item, call, rep):
    global bstack1ll1lll1ll_opy_
    global bstack1ll1l1111l_opy_
    name = bstack1111lll_opy_ (u"࠭ࠧ⏻")
    try:
        if rep.when == bstack1111lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⏼"):
            bstack11l1111ll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1111lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⏽"))
            try:
                if (str(skipSessionName).lower() != bstack1111lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⏾")):
                    name = str(rep.nodeid)
                    bstack11l11l11l1_opy_ = bstack1111ll1ll_opy_(bstack1111lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⏿"), name, bstack1111lll_opy_ (u"ࠫࠬ␀"), bstack1111lll_opy_ (u"ࠬ࠭␁"), bstack1111lll_opy_ (u"࠭ࠧ␂"), bstack1111lll_opy_ (u"ࠧࠨ␃"))
                    os.environ[bstack1111lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ␄")] = name
                    for driver in bstack1ll1l1111l_opy_:
                        if bstack11l1111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11l11l1_opy_)
            except Exception as e:
                logger.debug(bstack1111lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ␅").format(str(e)))
            try:
                bstack11l1111111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ␆"):
                    status = bstack1111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ␇") if rep.outcome.lower() == bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ␈") else bstack1111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭␉")
                    reason = bstack1111lll_opy_ (u"ࠧࠨ␊")
                    if status == bstack1111lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ␋"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1111lll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ␌") if status == bstack1111lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ␍") else bstack1111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ␎")
                    data = name + bstack1111lll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ␏") if status == bstack1111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭␐") else name + bstack1111lll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ␑") + reason
                    bstack1l1l1l1l_opy_ = bstack1111ll1ll_opy_(bstack1111lll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ␒"), bstack1111lll_opy_ (u"ࠩࠪ␓"), bstack1111lll_opy_ (u"ࠪࠫ␔"), bstack1111lll_opy_ (u"ࠫࠬ␕"), level, data)
                    for driver in bstack1ll1l1111l_opy_:
                        if bstack11l1111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1l1l_opy_)
            except Exception as e:
                logger.debug(bstack1111lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ␖").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ␗").format(str(e)))
    bstack1ll1lll1ll_opy_(item, call, rep)
notset = Notset()
def bstack11llll11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11l1l111l1_opy_
    if str(name).lower() == bstack1111lll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ␘"):
        return bstack1111lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ␙")
    else:
        return bstack11l1l111l1_opy_(self, name, default, skip)
def bstack1ll1ll1l1_opy_(self):
    global CONFIG
    global bstack1l1lll1l11_opy_
    try:
        proxy = bstack1llll1ll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111lll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ␚")):
                proxies = bstack11lll11ll1_opy_(proxy, bstack11ll11llll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1111l11_opy_ = proxies.popitem()
                    if bstack1111lll_opy_ (u"ࠥ࠾࠴࠵ࠢ␛") in bstack1ll1111l11_opy_:
                        return bstack1ll1111l11_opy_
                    else:
                        return bstack1111lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ␜") + bstack1ll1111l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤ␝").format(str(e)))
    return bstack1l1lll1l11_opy_(self)
def bstack11lllll1l_opy_():
    return (bstack1111lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ␞") in CONFIG or bstack1111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ␟") in CONFIG) and bstack11l11ll111_opy_() and bstack1l1l1ll111_opy_() >= version.parse(
        bstack11lllll11l_opy_)
def bstack11llll1lll_opy_(self,
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
    global bstack1lll1lll11_opy_
    global bstack1l1lll11l1_opy_
    global bstack1l11l1l11_opy_
    CONFIG[bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ␠")] = str(bstack1l11l1l11_opy_) + str(__version__)
    bstack1111ll11_opy_ = 0
    try:
        if bstack1l1lll11l1_opy_ is True:
            bstack1111ll11_opy_ = int(os.environ.get(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ␡")))
    except:
        bstack1111ll11_opy_ = 0
    CONFIG[bstack1111lll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ␢")] = True
    bstack1ll11ll1l_opy_ = bstack1l1ll1ll11_opy_(CONFIG, bstack1111ll11_opy_)
    logger.debug(bstack1ll111ll1l_opy_.format(str(bstack1ll11ll1l_opy_)))
    if CONFIG.get(bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ␣")):
        bstack11l111l1l_opy_(bstack1ll11ll1l_opy_, bstack1111l1l1l_opy_)
    if bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ␤") in CONFIG and bstack1111lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ␥") in CONFIG[bstack1111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ␦")][bstack1111ll11_opy_]:
        bstack1lll1lll11_opy_ = CONFIG[bstack1111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ␧")][bstack1111ll11_opy_][bstack1111lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ␨")]
    import urllib
    import json
    if bstack1111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ␩") in CONFIG and str(CONFIG[bstack1111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ␪")]).lower() != bstack1111lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ␫"):
        bstack11l11111l_opy_ = bstack1l1lll1ll_opy_()
        bstack1l1lll1lll_opy_ = bstack11l11111l_opy_ + urllib.parse.quote(json.dumps(bstack1ll11ll1l_opy_))
    else:
        bstack1l1lll1lll_opy_ = bstack1111lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨ␬") + urllib.parse.quote(json.dumps(bstack1ll11ll1l_opy_))
    browser = self.connect(bstack1l1lll1lll_opy_)
    return browser
def bstack11l1l1l11l_opy_():
    global bstack1l11l11ll_opy_
    global bstack1l11l1l11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111llll1_opy_
        if not bstack1l1lll11l1l_opy_():
            global bstack1lll111l_opy_
            if not bstack1lll111l_opy_:
                from bstack_utils.helper import bstack1l1ll11ll1_opy_, bstack1llllll11l_opy_
                bstack1lll111l_opy_ = bstack1l1ll11ll1_opy_()
                bstack1llllll11l_opy_(bstack1l11l1l11_opy_)
            BrowserType.connect = bstack1l111llll1_opy_
            return
        BrowserType.launch = bstack11llll1lll_opy_
        bstack1l11l11ll_opy_ = True
    except Exception as e:
        pass
def bstack1lll1lll1lll_opy_():
    global CONFIG
    global bstack1111llll1_opy_
    global bstack1ll11ll1_opy_
    global bstack1111l1l1l_opy_
    global bstack1l1lll11l1_opy_
    global bstack1lll1l1ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭␭")))
    bstack1111llll1_opy_ = eval(os.environ.get(bstack1111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ␮")))
    bstack1ll11ll1_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ␯"))
    bstack1l111l1111_opy_(CONFIG, bstack1111llll1_opy_)
    bstack1lll1l1ll1_opy_ = bstack1l1l11111_opy_.configure_logger(CONFIG, bstack1lll1l1ll1_opy_)
    if cli.bstack11l1lll11_opy_():
        bstack1llll1l1l_opy_.invoke(bstack11lll1111l_opy_.CONNECT, bstack1l1l11llll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ␰"), bstack1111lll_opy_ (u"ࠫ࠵࠭␱")))
        cli.bstack1lll1111111_opy_(cli_context.platform_index)
        cli.bstack1llll11llll_opy_(bstack11ll11llll_opy_(bstack1ll11ll1_opy_, CONFIG), cli_context.platform_index, bstack1ll11ll11l_opy_)
        cli.bstack1lll1l11l11_opy_()
        logger.debug(bstack1111lll_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ␲") + str(cli_context.platform_index) + bstack1111lll_opy_ (u"ࠨࠢ␳"))
        return # skip all existing operations
    global bstack1l111l11_opy_
    global bstack1lll11l1l_opy_
    global bstack11ll11ll1l_opy_
    global bstack1ll1ll1111_opy_
    global bstack1l1111111l_opy_
    global bstack1l11l1l1l1_opy_
    global bstack1ll1llll_opy_
    global bstack11llllll11_opy_
    global bstack1l1lll1l11_opy_
    global bstack11l1l111l1_opy_
    global bstack11ll1l1ll1_opy_
    global bstack1ll1lll1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l111l11_opy_ = webdriver.Remote.__init__
        bstack1lll11l1l_opy_ = WebDriver.quit
        bstack1ll1llll_opy_ = WebDriver.close
        bstack11llllll11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1111lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ␴") in CONFIG or bstack1111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ␵") in CONFIG) and bstack11l11ll111_opy_():
        if bstack1l1l1ll111_opy_() < version.parse(bstack11lllll11l_opy_):
            logger.error(bstack1l11ll1111_opy_.format(bstack1l1l1ll111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1111lll_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ␶")) and callable(getattr(RemoteConnection, bstack1111lll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ␷"))):
                    bstack1l1lll1l11_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1lll1l11_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1lll11_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11l1l111l1_opy_ = Config.getoption
        from _pytest import runner
        bstack11ll1l1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1ll1lll111_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll1lll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ␸"))
    bstack1111l1l1l_opy_ = CONFIG.get(bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ␹"), {}).get(bstack1111lll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ␺"))
    bstack1l1lll11l1_opy_ = True
    bstack1lllll11l_opy_(bstack1lll1lllll_opy_)
if (bstack111ll1l1lll_opy_()):
    bstack1lll1lll1lll_opy_()
@error_handler(class_method=False)
def bstack1lll1lllll1l_opy_(hook_name, event, bstack1l111l1l111_opy_=None):
    if hook_name not in [bstack1111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ␻"), bstack1111lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ␼"), bstack1111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ␽"), bstack1111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ␾"), bstack1111lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ␿"), bstack1111lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⑀"), bstack1111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⑁"), bstack1111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⑂")]:
        return
    node = store[bstack1111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⑃")]
    if hook_name in [bstack1111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⑄"), bstack1111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⑅")]:
        node = store[bstack1111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ⑆")]
    elif hook_name in [bstack1111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⑇"), bstack1111lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⑈")]:
        node = store[bstack1111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ⑉")]
    hook_type = bstack1llllllll1ll_opy_(hook_name)
    if event == bstack1111lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ⑊"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_[hook_type], bstack1lll111111l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1ll1ll_opy_ = {
            bstack1111lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⑋"): uuid,
            bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⑌"): bstack11l11ll1l1_opy_(),
            bstack1111lll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⑍"): bstack1111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⑎"),
            bstack1111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⑏"): hook_type,
            bstack1111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⑐"): hook_name
        }
        store[bstack1111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⑑")].append(uuid)
        bstack1llll111llll_opy_ = node.nodeid
        if hook_type == bstack1111lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⑒"):
            if not _111l111l11_opy_.get(bstack1llll111llll_opy_, None):
                _111l111l11_opy_[bstack1llll111llll_opy_] = {bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⑓"): []}
            _111l111l11_opy_[bstack1llll111llll_opy_][bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⑔")].append(bstack111l1ll1ll_opy_[bstack1111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⑕")])
        _111l111l11_opy_[bstack1llll111llll_opy_ + bstack1111lll_opy_ (u"࠭࠭ࠨ⑖") + hook_name] = bstack111l1ll1ll_opy_
        bstack1llll111l1l1_opy_(node, bstack111l1ll1ll_opy_, bstack1111lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⑗"))
    elif event == bstack1111lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⑘"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll1lll111l_opy_[hook_type], bstack1lll111111l_opy_.POST, node, None, bstack1l111l1l111_opy_)
            return
        bstack111lll1111_opy_ = node.nodeid + bstack1111lll_opy_ (u"ࠩ࠰ࠫ⑙") + hook_name
        _111l111l11_opy_[bstack111lll1111_opy_][bstack1111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⑚")] = bstack11l11ll1l1_opy_()
        bstack1lll1lll1ll1_opy_(_111l111l11_opy_[bstack111lll1111_opy_][bstack1111lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⑛")])
        bstack1llll111l1l1_opy_(node, _111l111l11_opy_[bstack111lll1111_opy_], bstack1111lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⑜"), bstack1lll1lllllll_opy_=bstack1l111l1l111_opy_)
def bstack1llll111111l_opy_():
    global bstack1llll11111l1_opy_
    if bstack1l111lll_opy_():
        bstack1llll11111l1_opy_ = bstack1111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⑝")
    else:
        bstack1llll11111l1_opy_ = bstack1111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⑞")
@bstack1lll11111l_opy_.bstack1llll1l111ll_opy_
def bstack1lll1llll11l_opy_():
    bstack1llll111111l_opy_()
    if cli.is_running():
        try:
            bstack111ll111l1l_opy_(bstack1lll1lllll1l_opy_)
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⑟").format(e))
        return
    if bstack11l11ll111_opy_():
        bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
        bstack1111lll_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ①")
        if bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ②")):
            if CONFIG.get(bstack1111lll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ③")) is not None and int(CONFIG[bstack1111lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ④")]) > 1:
                bstack1ll111l1l_opy_(bstack11l1111l_opy_)
            return
        bstack1ll111l1l_opy_(bstack11l1111l_opy_)
    try:
        bstack111ll111l1l_opy_(bstack1lll1lllll1l_opy_)
    except Exception as e:
        logger.debug(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ⑤").format(e))
bstack1lll1llll11l_opy_()