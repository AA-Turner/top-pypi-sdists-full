# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11lllll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11llll1l_opy_, bstack1l11l11ll1_opy_, update, bstack11lll1l11l_opy_,
                                       bstack11lll1111l_opy_, bstack1ll1ll111_opy_, bstack11ll11111_opy_, bstack11l111ll11_opy_,
                                       bstack11lll1ll11_opy_, bstack11llll1lll_opy_, bstack1l111111l1_opy_,
                                       bstack111ll111l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll1l1ll1_opy_)
from browserstack_sdk.bstack1l1llll11_opy_ import bstack11lll111l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l11l1l1l_opy_
from bstack_utils.capture import bstack111ll11l1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l11l111l1_opy_, bstack1ll1111l_opy_, bstack1ll11l1lll_opy_, \
    bstack1lll1lll1_opy_
from bstack_utils.helper import bstack11ll1lll_opy_, bstack111l1l1llll_opy_, bstack111l111lll_opy_, bstack11111lll_opy_, bstack1llll1ll1l1_opy_, bstack1lllllllll_opy_, \
    bstack111l111111l_opy_, \
    bstack111l1ll11ll_opy_, bstack111l1l111_opy_, bstack11l111l1l1_opy_, bstack111l11l1111_opy_, bstack1ll11ll111_opy_, Notset, \
    bstack11111ll1_opy_, bstack111l1lll1l1_opy_, bstack111l11l1l1l_opy_, Result, bstack111l1llll11_opy_, bstack111l1l1l1ll_opy_, bstack111l11l1l1_opy_, \
    bstack111ll111_opy_, bstack11l1l1ll1_opy_, bstack11l1l1ll_opy_, bstack111ll111l1l_opy_
from bstack_utils.bstack1111ll1l1ll_opy_ import bstack1111ll1l11l_opy_
from bstack_utils.messages import bstack11l1l11lll_opy_, bstack11ll1lll11_opy_, bstack1l1111l1l1_opy_, bstack1ll11ll11l_opy_, bstack111l1ll11_opy_, \
    bstack1lll1l11l_opy_, bstack11ll111l_opy_, bstack1111111l_opy_, bstack1l1l11ll1_opy_, bstack11lll11l11_opy_, \
    bstack1llll1l1ll_opy_, bstack11l11lll_opy_
from bstack_utils.proxy import bstack1llll11111_opy_, bstack111ll1l1_opy_
from bstack_utils.bstack1l1111l1_opy_ import bstack11111l11l11_opy_, bstack11111l11l1l_opy_, bstack111111lllll_opy_, bstack11111l11111_opy_, \
    bstack11111l11ll1_opy_, bstack11111l1l111_opy_, bstack11111l1l1ll_opy_, bstack11ll1lllll_opy_, bstack11111l11lll_opy_
from bstack_utils.bstack1ll11l11_opy_ import bstack11l1lll1ll_opy_
from bstack_utils.bstack1l11l111ll_opy_ import bstack1l11111ll1_opy_, bstack1lll1l111_opy_, bstack11l1111ll1_opy_, \
    bstack1111l1l11_opy_, bstack11lllll11l_opy_
from bstack_utils.bstack111ll1ll1l_opy_ import bstack111ll1ll11_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll111ll_opy_
import bstack_utils.accessibility as bstack11llll1l11_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack111lll111_opy_
from bstack_utils.bstack11llll1111_opy_ import bstack11llll1111_opy_
from bstack_utils.bstack1lll1ll11l_opy_ import bstack1lllll111_opy_
from browserstack_sdk.__init__ import bstack11ll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack111lllllll_opy_ import bstack111lllllll_opy_, bstack11l1ll1ll_opy_, bstack11lll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l1l1l1l1l1_opy_, bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111lllllll_opy_ import bstack111lllllll_opy_, bstack11l1ll1ll_opy_, bstack11lll1l1l_opy_
bstack1l111ll1ll_opy_ = None
bstack1l11l1l11l_opy_ = None
bstack1l11lll11l_opy_ = None
bstack11l11l1l_opy_ = None
bstack1l1l11l1l1_opy_ = None
bstack11ll1111_opy_ = None
bstack11l11l11ll_opy_ = None
bstack11l1ll1l11_opy_ = None
bstack111lll1l_opy_ = None
bstack1llll11l11_opy_ = None
bstack1lllll1ll1_opy_ = None
bstack11ll11ll_opy_ = None
bstack1ll1lll1_opy_ = None
bstack11l1l11l1l_opy_ = bstack11l1111_opy_ (u"ࠪࠫⅴ")
CONFIG = {}
bstack1ll11l11ll_opy_ = False
bstack1l1l1l1111_opy_ = bstack11l1111_opy_ (u"ࠫࠬⅵ")
bstack1l1ll1ll11_opy_ = bstack11l1111_opy_ (u"ࠬ࠭ⅶ")
bstack111ll1l11_opy_ = False
bstack1lll1l11l1_opy_ = []
bstack1l1l1llll1_opy_ = bstack1l11l111l1_opy_
bstack1llll11lll1l_opy_ = bstack11l1111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ⅷ")
bstack1l11l1ll1l_opy_ = {}
bstack1l1111l1ll_opy_ = None
bstack11l1lll11_opy_ = False
logger = bstack1l11l1l1l_opy_.get_logger(__name__, bstack1l1l1llll1_opy_)
store = {
    bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫⅸ"): []
}
bstack1llll1l11lll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l1ll11l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l1l1l1l1l1_opy_(
    test_framework_name=bstack1l11lll1_opy_[bstack11l1111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬⅹ")] if bstack1ll11ll111_opy_() else bstack1l11lll1_opy_[bstack11l1111_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩⅺ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l111l1ll1_opy_(page, bstack1l1l1lllll_opy_):
    try:
        page.evaluate(bstack11l1111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦⅻ"),
                      bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨⅼ") + json.dumps(
                          bstack1l1l1lllll_opy_) + bstack11l1111_opy_ (u"ࠧࢃࡽࠣⅽ"))
    except Exception as e:
        print(bstack11l1111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦⅾ"), e)
def bstack11ll11ll1_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣⅿ"), bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ↀ") + json.dumps(
            message) + bstack11l1111_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬↁ") + json.dumps(level) + bstack11l1111_opy_ (u"ࠪࢁࢂ࠭ↂ"))
    except Exception as e:
        print(bstack11l1111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢↃ"), e)
def pytest_configure(config):
    global bstack1l1l1l1111_opy_
    global CONFIG
    bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
    config.args = bstack1l1ll111ll_opy_.bstack1llll1lll111_opy_(config.args)
    bstack1l1l11l1ll_opy_.bstack1ll1111ll1_opy_(bstack11l1l1ll_opy_(config.getoption(bstack11l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩↄ"))))
    try:
        bstack1l11l1l1l_opy_.bstack1111l11llll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111lllllll_opy_.invoke(bstack11l1ll1ll_opy_.CONNECT, bstack11lll1l1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ↅ"), bstack11l1111_opy_ (u"ࠧ࠱ࠩↆ")))
        config = json.loads(os.environ.get(bstack11l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢↇ"), bstack11l1111_opy_ (u"ࠤࡾࢁࠧↈ")))
        cli.bstack1l11l111111_opy_(bstack11l111l1l1_opy_(bstack1l1l1l1111_opy_, CONFIG), cli_context.platform_index, bstack11lll1l11l_opy_)
    if cli.bstack1l1111ll1ll_opy_(bstack1llll1111ll_opy_):
        cli.bstack1l111l111l1_opy_()
        logger.debug(bstack11l1111_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ↉") + str(cli_context.platform_index) + bstack11l1111_opy_ (u"ࠦࠧ↊"))
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.BEFORE_ALL, bstack1lll1lll1ll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11l1111_opy_ (u"ࠧࡽࡨࡦࡰࠥ↋"), None)
    if cli.is_running() and when == bstack11l1111_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ↌"):
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.LOG_REPORT, bstack1lll1lll1ll_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11l1111_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ↍"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1111_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ↎")))
        if not passed:
            config = json.loads(os.environ.get(bstack11l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠣ↏"), bstack11l1111_opy_ (u"ࠥࡿࢂࠨ←")))
            if bstack1lllll111_opy_.bstack11ll111ll1_opy_(config):
                bstack11ll11l1lll_opy_ = bstack1lllll111_opy_.bstack1l11ll1lll_opy_(config)
                if item.execution_count > bstack11ll11l1lll_opy_:
                    print(bstack11l1111_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡴࡨࡸࡷ࡯ࡥࡴ࠼ࠣࠫ↑"), report.nodeid, os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ→")))
                    bstack1lllll111_opy_.bstack11ll1ll1l1l_opy_(report.nodeid)
            else:
                print(bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥ࠭↓"), report.nodeid, os.environ.get(bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ↔")))
                bstack1lllll111_opy_.bstack11ll1ll1l1l_opy_(report.nodeid)
        else:
            print(bstack11l1111_opy_ (u"ࠨࡖࡨࡷࡹࠦࡰࡢࡵࡶࡩࡩࡀࠠࠨ↕"), report.nodeid, os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ↖")))
    if cli.is_running():
        if when == bstack11l1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ↗"):
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.BEFORE_EACH, bstack1lll1lll1ll_opy_.POST, item, call, outcome)
        elif when == bstack11l1111_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ↘"):
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.LOG_REPORT, bstack1lll1lll1ll_opy_.POST, item, call, outcome)
        elif when == bstack11l1111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ↙"):
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.AFTER_EACH, bstack1lll1lll1ll_opy_.POST, item, call, outcome)
        return # skip all existing bstack1llll1ll1l11_opy_
    skipSessionName = item.config.getoption(bstack11l1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ↚"))
    plugins = item.config.getoption(bstack11l1111_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣ↛"))
    report = outcome.get_result()
    os.environ[bstack11l1111_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ↜")] = report.nodeid
    bstack1llll1l1l1l1_opy_(item, call, report)
    if bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢ↝") not in plugins or bstack1ll11ll111_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1111_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦ↞"), None)
    page = getattr(item, bstack11l1111_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥ↟"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llll1l1l111_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llll1l11111_opy_(item, report, summary, skipSessionName)
def bstack1llll1l1l111_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ↠") and report.skipped:
        bstack11111l11lll_opy_(report)
    if report.when in [bstack11l1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ↡"), bstack11l1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ↢")]:
        return
    if not bstack1llll1ll1l1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11l1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭↣")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ↤") + json.dumps(
                    report.nodeid) + bstack11l1111_opy_ (u"ࠪࢁࢂ࠭↥"))
        os.environ[bstack11l1111_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ↦")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1111_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧ↧").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1111_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ↨")))
    bstack1l11lll11_opy_ = bstack11l1111_opy_ (u"ࠢࠣ↩")
    bstack11111l11lll_opy_(report)
    if not passed:
        try:
            bstack1l11lll11_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1111_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ↪").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11lll11_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1111_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ↫")))
        bstack1l11lll11_opy_ = bstack11l1111_opy_ (u"ࠥࠦ↬")
        if not passed:
            try:
                bstack1l11lll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1111_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦ↭").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11lll11_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩ↮")
                    + json.dumps(bstack11l1111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢ↯"))
                    + bstack11l1111_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ↰")
                )
            else:
                item._driver.execute_script(
                    bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭↱")
                    + json.dumps(str(bstack1l11lll11_opy_))
                    + bstack11l1111_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ↲")
                )
        except Exception as e:
            summary.append(bstack11l1111_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣ↳").format(e))
def bstack1llll1ll11ll_opy_(test_name, error_message):
    try:
        bstack1llll1ll1111_opy_ = []
        bstack11llllll11_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ↴"), bstack11l1111_opy_ (u"ࠬ࠶ࠧ↵"))
        bstack1l1llllll_opy_ = {bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ↶"): test_name, bstack11l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭↷"): error_message, bstack11l1111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ↸"): bstack11llllll11_opy_}
        bstack1llll1l1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1111_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ↹"))
        if os.path.exists(bstack1llll1l1lll1_opy_):
            with open(bstack1llll1l1lll1_opy_) as f:
                bstack1llll1ll1111_opy_ = json.load(f)
        bstack1llll1ll1111_opy_.append(bstack1l1llllll_opy_)
        with open(bstack1llll1l1lll1_opy_, bstack11l1111_opy_ (u"ࠪࡻࠬ↺")) as f:
            json.dump(bstack1llll1ll1111_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩ↻") + str(e))
def bstack1llll1l11111_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11l1111_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ↼"), bstack11l1111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ↽")]:
        return
    if (str(skipSessionName).lower() != bstack11l1111_opy_ (u"ࠧࡵࡴࡸࡩࠬ↾")):
        bstack1l111l1ll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1111_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ↿")))
    bstack1l11lll11_opy_ = bstack11l1111_opy_ (u"ࠤࠥ⇀")
    bstack11111l11lll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l11lll11_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1111_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⇁").format(e)
                )
        try:
            if passed:
                bstack11lllll11l_opy_(getattr(item, bstack11l1111_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ⇂"), None), bstack11l1111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ⇃"))
            else:
                error_message = bstack11l1111_opy_ (u"࠭ࠧ⇄")
                if bstack1l11lll11_opy_:
                    bstack11ll11ll1_opy_(item._page, str(bstack1l11lll11_opy_), bstack11l1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ⇅"))
                    bstack11lllll11l_opy_(getattr(item, bstack11l1111_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⇆"), None), bstack11l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⇇"), str(bstack1l11lll11_opy_))
                    error_message = str(bstack1l11lll11_opy_)
                else:
                    bstack11lllll11l_opy_(getattr(item, bstack11l1111_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⇈"), None), bstack11l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⇉"))
                bstack1llll1ll11ll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1111_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤ⇊").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11l1111_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ⇋"), default=bstack11l1111_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ⇌"), help=bstack11l1111_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ⇍"))
    parser.addoption(bstack11l1111_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ⇎"), default=bstack11l1111_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ⇏"), help=bstack11l1111_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ⇐"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1111_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢ⇑"), action=bstack11l1111_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧ⇒"), default=bstack11l1111_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢ⇓"),
                         help=bstack11l1111_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢ⇔"))
def bstack111ll11lll_opy_(log):
    if not (log[bstack11l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⇕")] and log[bstack11l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⇖")].strip()):
        return
    active = bstack111ll1l111_opy_()
    log = {
        bstack11l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⇗"): log[bstack11l1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⇘")],
        bstack11l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⇙"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"࡛ࠧࠩ⇚"),
        bstack11l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⇛"): log[bstack11l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⇜")],
    }
    if active:
        if active[bstack11l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ⇝")] == bstack11l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⇞"):
            log[bstack11l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⇟")] = active[bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⇠")]
        elif active[bstack11l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ⇡")] == bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭⇢"):
            log[bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⇣")] = active[bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⇤")]
    bstack111lll111_opy_.bstack11lll11l_opy_([log])
def bstack111ll1l111_opy_():
    if len(store[bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⇥")]) > 0 and store[bstack11l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⇦")][-1]:
        return {
            bstack11l1111_opy_ (u"࠭ࡴࡺࡲࡨࠫ⇧"): bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⇨"),
            bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⇩"): store[bstack11l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⇪")][-1]
        }
    if store.get(bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⇫"), None):
        return {
            bstack11l1111_opy_ (u"ࠫࡹࡿࡰࡦࠩ⇬"): bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࠪ⇭"),
            bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⇮"): store[bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⇯")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.INIT_TEST, bstack1lll1lll1ll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.INIT_TEST, bstack1lll1lll1ll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llll11ll11l_opy_ = True
        bstack11lll11lll_opy_ = bstack11llll1l11_opy_.bstack1lll111l1l_opy_(bstack111l1ll11ll_opy_(item.own_markers))
        if not cli.bstack1l1111ll1ll_opy_(bstack1llll1111ll_opy_):
            item._a11y_test_case = bstack11lll11lll_opy_
            if bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⇰"), None):
                driver = getattr(item, bstack11l1111_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⇱"), None)
                item._a11y_started = bstack11llll1l11_opy_.bstack11l11llll_opy_(driver, bstack11lll11lll_opy_)
        if not bstack111lll111_opy_.on() or bstack1llll11lll1l_opy_ != bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⇲"):
            return
        global current_test_uuid #, bstack111llll11l_opy_
        bstack111ll11111_opy_ = {
            bstack11l1111_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇳"): uuid4().__str__(),
            bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⇴"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"࡚࠭ࠨ⇵")
        }
        current_test_uuid = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⇶")]
        store[bstack11l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⇷")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⇸")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l1ll11l_opy_[item.nodeid] = {**_111l1ll11l_opy_[item.nodeid], **bstack111ll11111_opy_}
        bstack1llll1ll11l1_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack11l1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⇹"))
    except Exception as err:
        print(bstack11l1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭⇺"), str(err))
def pytest_runtest_setup(item):
    store[bstack11l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⇻")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.BEFORE_EACH, bstack1lll1lll1ll_opy_.PRE, item, bstack11l1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⇼"))
    if bstack1lllll111_opy_.bstack11ll1l1l111_opy_():
            bstack1llll1l111l1_opy_ = bstack11l1111_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡢࡵࠣࡸ࡭࡫ࠠࡢࡤࡲࡶࡹࠦࡢࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦ⇽")
            logger.error(bstack1llll1l111l1_opy_)
            bstack111ll11111_opy_ = {
                bstack11l1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⇾"): uuid4().__str__(),
                bstack11l1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⇿"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"ࠪ࡞ࠬ∀"),
                bstack11l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ∁"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"ࠬࡠࠧ∂"),
                bstack11l1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭∃"): bstack11l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ∄"),
                bstack11l1111_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ∅"): bstack1llll1l111l1_opy_,
                bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ∆"): [],
                bstack11l1111_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ∇"): []
            }
            bstack1llll1ll11l1_opy_(item, bstack111ll11111_opy_, bstack11l1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ∈"))
            pytest.skip(bstack1llll1l111l1_opy_)
            return # skip all existing bstack1llll1ll1l11_opy_
    global bstack1llll1l11lll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l11l1111_opy_():
        atexit.register(bstack111l1111_opy_)
        if not bstack1llll1l11lll_opy_:
            try:
                bstack1llll11ll1ll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111ll111l1l_opy_():
                    bstack1llll11ll1ll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1llll11ll1ll_opy_:
                    signal.signal(s, bstack1llll1l1l1ll_opy_)
                bstack1llll1l11lll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l1111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ∉") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11111l11l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭∊")
    try:
        if not bstack111lll111_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111ll11111_opy_ = {
            bstack11l1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ∋"): uuid,
            bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ∌"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"ࠩ࡝ࠫ∍"),
            bstack11l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ∎"): bstack11l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ∏"),
            bstack11l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ∐"): bstack11l1111_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ∑"),
            bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ−"): bstack11l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ∓")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭∔")] = item
        store[bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ∕")] = [uuid]
        if not _111l1ll11l_opy_.get(item.nodeid, None):
            _111l1ll11l_opy_[item.nodeid] = {bstack11l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ∖"): [], bstack11l1111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ∗"): []}
        _111l1ll11l_opy_[item.nodeid][bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ∘")].append(bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ∙")])
        _111l1ll11l_opy_[item.nodeid + bstack11l1111_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ√")] = bstack111ll11111_opy_
        bstack1llll1l1ll11_opy_(item, bstack111ll11111_opy_, bstack11l1111_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ∛"))
    except Exception as err:
        print(bstack11l1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭∜"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.AFTER_EACH, bstack1lll1lll1ll_opy_.PRE, item, bstack11l1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭∝"))
        return # skip all existing bstack1llll1ll1l11_opy_
    try:
        global bstack1l11l1ll1l_opy_
        bstack11llllll11_opy_ = 0
        if bstack111ll1l11_opy_ is True:
            bstack11llllll11_opy_ = int(os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ∞")))
        if bstack11ll11l111_opy_.bstack111ll1l1l_opy_() == bstack11l1111_opy_ (u"ࠨࡴࡳࡷࡨࠦ∟"):
            if bstack11ll11l111_opy_.bstack11ll111ll_opy_() == bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ∠"):
                bstack1llll1ll111l_opy_ = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ∡"), None)
                bstack111l11l1l_opy_ = bstack1llll1ll111l_opy_ + bstack11l1111_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧ∢")
                driver = getattr(item, bstack11l1111_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ∣"), None)
                bstack1lllll1l11_opy_ = getattr(item, bstack11l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ∤"), None)
                bstack111llllll1_opy_ = getattr(item, bstack11l1111_opy_ (u"ࠬࡻࡵࡪࡦࠪ∥"), None)
                PercySDK.screenshot(driver, bstack111l11l1l_opy_, bstack1lllll1l11_opy_=bstack1lllll1l11_opy_, bstack111llllll1_opy_=bstack111llllll1_opy_, bstack1l1lll1l1_opy_=bstack11llllll11_opy_)
        if not cli.bstack1l1111ll1ll_opy_(bstack1llll1111ll_opy_):
            if getattr(item, bstack11l1111_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭∦"), False):
                bstack11lll111l1_opy_.bstack1lll1l1l1_opy_(getattr(item, bstack11l1111_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ∧"), None), bstack1l11l1ll1l_opy_, logger, item)
        if not bstack111lll111_opy_.on():
            return
        bstack111ll11111_opy_ = {
            bstack11l1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭∨"): uuid4().__str__(),
            bstack11l1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭∩"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"ࠪ࡞ࠬ∪"),
            bstack11l1111_opy_ (u"ࠫࡹࡿࡰࡦࠩ∫"): bstack11l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ∬"),
            bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ∭"): bstack11l1111_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ∮"),
            bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ∯"): bstack11l1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ∰")
        }
        _111l1ll11l_opy_[item.nodeid + bstack11l1111_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭∱")] = bstack111ll11111_opy_
        bstack1llll1l1ll11_opy_(item, bstack111ll11111_opy_, bstack11l1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ∲"))
    except Exception as err:
        print(bstack11l1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫ∳"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11111l11111_opy_(fixturedef.argname):
        store[bstack11l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ∴")] = request.node
    elif bstack11111l11ll1_opy_(fixturedef.argname):
        store[bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ∵")] = request.node
    if not bstack111lll111_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll1ll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1ll1l11_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll1ll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.SETUP_FIXTURE, bstack1lll1lll1ll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1llll1ll1l11_opy_
    try:
        fixture = {
            bstack11l1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭∶"): fixturedef.argname,
            bstack11l1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ∷"): bstack111l111111l_opy_(outcome),
            bstack11l1111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ∸"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ∹")]
        if not _111l1ll11l_opy_.get(current_test_item.nodeid, None):
            _111l1ll11l_opy_[current_test_item.nodeid] = {bstack11l1111_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ∺"): []}
        _111l1ll11l_opy_[current_test_item.nodeid][bstack11l1111_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ∻")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ∼"), str(err))
if bstack1ll11ll111_opy_() and bstack111lll111_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.STEP, bstack1lll1lll1ll_opy_.PRE, request, step)
            return
        try:
            _111l1ll11l_opy_[request.node.nodeid][bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ∽")].bstack11l11lll1_opy_(id(step))
        except Exception as err:
            print(bstack11l1111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ∾"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.STEP, bstack1lll1lll1ll_opy_.POST, request, step, exception)
            return
        try:
            _111l1ll11l_opy_[request.node.nodeid][bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭∿")].bstack111ll1lll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ≀"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.STEP, bstack1lll1lll1ll_opy_.POST, request, step)
            return
        try:
            bstack111ll1ll1l_opy_: bstack111ll1ll11_opy_ = _111l1ll11l_opy_[request.node.nodeid][bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ≁")]
            bstack111ll1ll1l_opy_.bstack111ll1lll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ≂"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll11lll1l_opy_
        try:
            if not bstack111lll111_opy_.on() or bstack1llll11lll1l_opy_ != bstack11l1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ≃"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ≄"), None)
            if not _111l1ll11l_opy_.get(request.node.nodeid, None):
                _111l1ll11l_opy_[request.node.nodeid] = {}
            bstack111ll1ll1l_opy_ = bstack111ll1ll11_opy_.bstack1lllllllllll_opy_(
                scenario, feature, request.node,
                name=bstack11111l1l111_opy_(request.node, scenario),
                started_at=bstack1lllllllll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1111_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ≅"),
                tags=bstack11111l1l1ll_opy_(feature, scenario),
                bstack111lll11ll_opy_=bstack111lll111_opy_.bstack111lll1l11_opy_(driver) if driver and driver.session_id else {}
            )
            _111l1ll11l_opy_[request.node.nodeid][bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭≆")] = bstack111ll1ll1l_opy_
            bstack1llll11lll11_opy_(bstack111ll1ll1l_opy_.uuid)
            bstack111lll111_opy_.bstack111ll111ll_opy_(bstack11l1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ≇"), bstack111ll1ll1l_opy_)
        except Exception as err:
            print(bstack11l1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ≈"), str(err))
def bstack1llll1l1ll1l_opy_(bstack111ll11l11_opy_):
    if bstack111ll11l11_opy_ in store[bstack11l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ≉")]:
        store[bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ≊")].remove(bstack111ll11l11_opy_)
def bstack1llll11lll11_opy_(test_uuid):
    store[bstack11l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ≋")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111lll111_opy_.bstack1lllll1ll1ll_opy_
def bstack1llll1l1l1l1_opy_(item, call, report):
    logger.debug(bstack11l1111_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡴࡷࠫ≌"))
    global bstack1llll11lll1l_opy_
    bstack1l11l1111_opy_ = bstack1lllllllll_opy_()
    if hasattr(report, bstack11l1111_opy_ (u"ࠪࡷࡹࡵࡰࠨ≍")):
        bstack1l11l1111_opy_ = bstack111l1llll11_opy_(report.stop)
    elif hasattr(report, bstack11l1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ≎")):
        bstack1l11l1111_opy_ = bstack111l1llll11_opy_(report.start)
    try:
        if getattr(report, bstack11l1111_opy_ (u"ࠬࡽࡨࡦࡰࠪ≏"), bstack11l1111_opy_ (u"࠭ࠧ≐")) == bstack11l1111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ≑"):
            logger.debug(bstack11l1111_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ≒").format(getattr(report, bstack11l1111_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ≓"), bstack11l1111_opy_ (u"ࠪࠫ≔")).__str__(), bstack1llll11lll1l_opy_))
            if bstack1llll11lll1l_opy_ == bstack11l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ≕"):
                _111l1ll11l_opy_[item.nodeid][bstack11l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ≖")] = bstack1l11l1111_opy_
                bstack1llll1ll11l1_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ≗"), report, call)
                store[bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ≘")] = None
            elif bstack1llll11lll1l_opy_ == bstack11l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ≙"):
                bstack111ll1ll1l_opy_ = _111l1ll11l_opy_[item.nodeid][bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ≚")]
                bstack111ll1ll1l_opy_.set(hooks=_111l1ll11l_opy_[item.nodeid].get(bstack11l1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ≛"), []))
                exception, bstack111lll1l1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll1l1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l1111_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪ≜"), bstack11l1111_opy_ (u"ࠬ࠭≝"))]
                bstack111ll1ll1l_opy_.stop(time=bstack1l11l1111_opy_, result=Result(result=getattr(report, bstack11l1111_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ≞"), bstack11l1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ≟")), exception=exception, bstack111lll1l1l_opy_=bstack111lll1l1l_opy_))
                bstack111lll111_opy_.bstack111ll111ll_opy_(bstack11l1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ≠"), _111l1ll11l_opy_[item.nodeid][bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ≡")])
        elif getattr(report, bstack11l1111_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ≢"), bstack11l1111_opy_ (u"ࠫࠬ≣")) in [bstack11l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ≤"), bstack11l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ≥")]:
            logger.debug(bstack11l1111_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ≦").format(getattr(report, bstack11l1111_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭≧"), bstack11l1111_opy_ (u"ࠩࠪ≨")).__str__(), bstack1llll11lll1l_opy_))
            bstack111ll1l11l_opy_ = item.nodeid + bstack11l1111_opy_ (u"ࠪ࠱ࠬ≩") + getattr(report, bstack11l1111_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ≪"), bstack11l1111_opy_ (u"ࠬ࠭≫"))
            if getattr(report, bstack11l1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ≬"), False):
                hook_type = bstack11l1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ≭") if getattr(report, bstack11l1111_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭≮"), bstack11l1111_opy_ (u"ࠩࠪ≯")) == bstack11l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ≰") else bstack11l1111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ≱")
                _111l1ll11l_opy_[bstack111ll1l11l_opy_] = {
                    bstack11l1111_opy_ (u"ࠬࡻࡵࡪࡦࠪ≲"): uuid4().__str__(),
                    bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ≳"): bstack1l11l1111_opy_,
                    bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ≴"): hook_type
                }
            _111l1ll11l_opy_[bstack111ll1l11l_opy_][bstack11l1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭≵")] = bstack1l11l1111_opy_
            bstack1llll1l1ll1l_opy_(_111l1ll11l_opy_[bstack111ll1l11l_opy_][bstack11l1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ≶")])
            bstack1llll1l1ll11_opy_(item, _111l1ll11l_opy_[bstack111ll1l11l_opy_], bstack11l1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ≷"), report, call)
            if getattr(report, bstack11l1111_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ≸"), bstack11l1111_opy_ (u"ࠬ࠭≹")) == bstack11l1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ≺"):
                if getattr(report, bstack11l1111_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ≻"), bstack11l1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ≼")) == bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ≽"):
                    bstack111ll11111_opy_ = {
                        bstack11l1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ≾"): uuid4().__str__(),
                        bstack11l1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ≿"): bstack1lllllllll_opy_(),
                        bstack11l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⊀"): bstack1lllllllll_opy_()
                    }
                    _111l1ll11l_opy_[item.nodeid] = {**_111l1ll11l_opy_[item.nodeid], **bstack111ll11111_opy_}
                    bstack1llll1ll11l1_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⊁"))
                    bstack1llll1ll11l1_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack11l1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⊂"), report, call)
    except Exception as err:
        print(bstack11l1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭⊃"), str(err))
def bstack1llll11lllll_opy_(test, bstack111ll11111_opy_, result=None, call=None, bstack1l1l1l11l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111ll1ll1l_opy_ = {
        bstack11l1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⊄"): bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⊅")],
        bstack11l1111_opy_ (u"ࠫࡹࡿࡰࡦࠩ⊆"): bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࠪ⊇"),
        bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⊈"): test.name,
        bstack11l1111_opy_ (u"ࠧࡣࡱࡧࡽࠬ⊉"): {
            bstack11l1111_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⊊"): bstack11l1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⊋"),
            bstack11l1111_opy_ (u"ࠪࡧࡴࡪࡥࠨ⊌"): inspect.getsource(test.obj)
        },
        bstack11l1111_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⊍"): test.name,
        bstack11l1111_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⊎"): test.name,
        bstack11l1111_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⊏"): bstack1l1ll111ll_opy_.bstack1111lllll1_opy_(test),
        bstack11l1111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⊐"): file_path,
        bstack11l1111_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⊑"): file_path,
        bstack11l1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⊒"): bstack11l1111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⊓"),
        bstack11l1111_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⊔"): file_path,
        bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⊕"): bstack111ll11111_opy_[bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⊖")],
        bstack11l1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⊗"): bstack11l1111_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⊘"),
        bstack11l1111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ⊙"): {
            bstack11l1111_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧ⊚"): test.nodeid
        },
        bstack11l1111_opy_ (u"ࠫࡹࡧࡧࡴࠩ⊛"): bstack111l1ll11ll_opy_(test.own_markers)
    }
    if bstack1l1l1l11l_opy_ in [bstack11l1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⊜"), bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⊝")]:
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ⊞")] = {
            bstack11l1111_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⊟"): bstack111ll11111_opy_.get(bstack11l1111_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⊠"), [])
        }
    if bstack1l1l1l11l_opy_ == bstack11l1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⊡"):
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⊢")] = bstack11l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⊣")
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⊤")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⊥")]
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⊦")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⊧")]
    if result:
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⊨")] = result.outcome
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⊩")] = result.duration * 1000
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⊪")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⊫")]
        if result.failed:
            bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⊬")] = bstack111lll111_opy_.bstack111111llll_opy_(call.excinfo.typename)
            bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⊭")] = bstack111lll111_opy_.bstack1lllll1l1ll1_opy_(call.excinfo, result)
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⊮")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⊯")]
    if outcome:
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⊰")] = bstack111l111111l_opy_(outcome)
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⊱")] = 0
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⊲")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⊳")]
        if bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⊴")] == bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⊵"):
            bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⊶")] = bstack11l1111_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ⊷")  # bstack1llll1l1l11l_opy_
            bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⊸")] = [{bstack11l1111_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⊹"): [bstack11l1111_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ⊺")]}]
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⊻")] = bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⊼")]
    return bstack111ll1ll1l_opy_
def bstack1llll1ll1ll1_opy_(test, bstack111l1111ll_opy_, bstack1l1l1l11l_opy_, result, call, outcome, bstack1llll1ll1l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⊽")]
    hook_name = bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⊾")]
    hook_data = {
        bstack11l1111_opy_ (u"ࠬࡻࡵࡪࡦࠪ⊿"): bstack111l1111ll_opy_[bstack11l1111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⋀")],
        bstack11l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ⋁"): bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰ࠭⋂"),
        bstack11l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⋃"): bstack11l1111_opy_ (u"ࠪࡿࢂ࠭⋄").format(bstack11111l11l1l_opy_(hook_name)),
        bstack11l1111_opy_ (u"ࠫࡧࡵࡤࡺࠩ⋅"): {
            bstack11l1111_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⋆"): bstack11l1111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⋇"),
            bstack11l1111_opy_ (u"ࠧࡤࡱࡧࡩࠬ⋈"): None
        },
        bstack11l1111_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⋉"): test.name,
        bstack11l1111_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⋊"): bstack1l1ll111ll_opy_.bstack1111lllll1_opy_(test, hook_name),
        bstack11l1111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⋋"): file_path,
        bstack11l1111_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⋌"): file_path,
        bstack11l1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⋍"): bstack11l1111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⋎"),
        bstack11l1111_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⋏"): file_path,
        bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⋐"): bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⋑")],
        bstack11l1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⋒"): bstack11l1111_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭⋓") if bstack1llll11lll1l_opy_ == bstack11l1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⋔") else bstack11l1111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⋕"),
        bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⋖"): hook_type
    }
    bstack1l111111lll_opy_ = bstack111l11l111_opy_(_111l1ll11l_opy_.get(test.nodeid, None))
    if bstack1l111111lll_opy_:
        hook_data[bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭⋗")] = bstack1l111111lll_opy_
    if result:
        hook_data[bstack11l1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⋘")] = result.outcome
        hook_data[bstack11l1111_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⋙")] = result.duration * 1000
        hook_data[bstack11l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⋚")] = bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⋛")]
        if result.failed:
            hook_data[bstack11l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⋜")] = bstack111lll111_opy_.bstack111111llll_opy_(call.excinfo.typename)
            hook_data[bstack11l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⋝")] = bstack111lll111_opy_.bstack1lllll1l1ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⋞")] = bstack111l111111l_opy_(outcome)
        hook_data[bstack11l1111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⋟")] = 100
        hook_data[bstack11l1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⋠")] = bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⋡")]
        if hook_data[bstack11l1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⋢")] == bstack11l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⋣"):
            hook_data[bstack11l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⋤")] = bstack11l1111_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⋥")  # bstack1llll1l1l11l_opy_
            hook_data[bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⋦")] = [{bstack11l1111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⋧"): [bstack11l1111_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⋨")]}]
    if bstack1llll1ll1l1l_opy_:
        hook_data[bstack11l1111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⋩")] = bstack1llll1ll1l1l_opy_.result
        hook_data[bstack11l1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⋪")] = bstack111l1lll1l1_opy_(bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⋫")], bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⋬")])
        hook_data[bstack11l1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⋭")] = bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⋮")]
        if hook_data[bstack11l1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⋯")] == bstack11l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⋰"):
            hook_data[bstack11l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⋱")] = bstack111lll111_opy_.bstack111111llll_opy_(bstack1llll1ll1l1l_opy_.exception_type)
            hook_data[bstack11l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⋲")] = [{bstack11l1111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⋳"): bstack111l11l1l1l_opy_(bstack1llll1ll1l1l_opy_.exception)}]
    return hook_data
def bstack1llll1ll11l1_opy_(test, bstack111ll11111_opy_, bstack1l1l1l11l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11l1111_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⋴").format(bstack1l1l1l11l_opy_))
    bstack111ll1ll1l_opy_ = bstack1llll11lllll_opy_(test, bstack111ll11111_opy_, result, call, bstack1l1l1l11l_opy_, outcome)
    driver = getattr(test, bstack11l1111_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⋵"), None)
    if bstack1l1l1l11l_opy_ == bstack11l1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⋶") and driver:
        bstack111ll1ll1l_opy_[bstack11l1111_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ⋷")] = bstack111lll111_opy_.bstack111lll1l11_opy_(driver)
    if bstack1l1l1l11l_opy_ == bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⋸"):
        bstack1l1l1l11l_opy_ = bstack11l1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⋹")
    bstack111l11l11l_opy_ = {
        bstack11l1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⋺"): bstack1l1l1l11l_opy_,
        bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⋻"): bstack111ll1ll1l_opy_
    }
    bstack111lll111_opy_.bstack1l1l11lll1_opy_(bstack111l11l11l_opy_)
    if bstack1l1l1l11l_opy_ == bstack11l1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⋼"):
        threading.current_thread().bstackTestMeta = {bstack11l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⋽"): bstack11l1111_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⋾")}
    elif bstack1l1l1l11l_opy_ == bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⋿"):
        threading.current_thread().bstackTestMeta = {bstack11l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⌀"): getattr(result, bstack11l1111_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⌁"), bstack11l1111_opy_ (u"ࠩࠪ⌂"))}
def bstack1llll1l1ll11_opy_(test, bstack111ll11111_opy_, bstack1l1l1l11l_opy_, result=None, call=None, outcome=None, bstack1llll1ll1l1l_opy_=None):
    logger.debug(bstack11l1111_opy_ (u"ࠪࡷࡪࡴࡤࡠࡪࡲࡳࡰࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥ࡮࡯ࡰ࡭ࠣࡨࡦࡺࡡ࠭ࠢࡨࡺࡪࡴࡴࡕࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ⌃").format(bstack1l1l1l11l_opy_))
    hook_data = bstack1llll1ll1ll1_opy_(test, bstack111ll11111_opy_, bstack1l1l1l11l_opy_, result, call, outcome, bstack1llll1ll1l1l_opy_)
    bstack111l11l11l_opy_ = {
        bstack11l1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⌄"): bstack1l1l1l11l_opy_,
        bstack11l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧ⌅"): hook_data
    }
    bstack111lll111_opy_.bstack1l1l11lll1_opy_(bstack111l11l11l_opy_)
def bstack111l11l111_opy_(bstack111ll11111_opy_):
    if not bstack111ll11111_opy_:
        return None
    if bstack111ll11111_opy_.get(bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⌆"), None):
        return getattr(bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⌇")], bstack11l1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⌈"), None)
    return bstack111ll11111_opy_.get(bstack11l1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⌉"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.LOG, bstack1lll1lll1ll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_.LOG, bstack1lll1lll1ll_opy_.POST, request, caplog)
        return # skip all existing bstack1llll1ll1l11_opy_
    try:
        if not bstack111lll111_opy_.on():
            return
        places = [bstack11l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⌊"), bstack11l1111_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⌋"), bstack11l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⌌")]
        logs = []
        for bstack1llll11ll1l1_opy_ in places:
            records = caplog.get_records(bstack1llll11ll1l1_opy_)
            bstack1llll1l1111l_opy_ = bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⌍") if bstack1llll11ll1l1_opy_ == bstack11l1111_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⌎") else bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⌏")
            bstack1llll1l1llll_opy_ = request.node.nodeid + (bstack11l1111_opy_ (u"ࠩࠪ⌐") if bstack1llll11ll1l1_opy_ == bstack11l1111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⌑") else bstack11l1111_opy_ (u"ࠫ࠲࠭⌒") + bstack1llll11ll1l1_opy_)
            test_uuid = bstack111l11l111_opy_(_111l1ll11l_opy_.get(bstack1llll1l1llll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l1l1l1ll_opy_(record.message):
                    continue
                logs.append({
                    bstack11l1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⌓"): bstack111l1l1llll_opy_(record.created).isoformat() + bstack11l1111_opy_ (u"࡚࠭ࠨ⌔"),
                    bstack11l1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⌕"): record.levelname,
                    bstack11l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⌖"): record.message,
                    bstack1llll1l1111l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111lll111_opy_.bstack11lll11l_opy_(logs)
    except Exception as err:
        print(bstack11l1111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭⌗"), str(err))
def bstack1l11ll1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1lll11_opy_
    bstack1l1l1ll1l1_opy_ = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ⌘"), None) and bstack11ll1lll_opy_(
            threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⌙"), None)
    bstack1l111111_opy_ = getattr(driver, bstack11l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⌚"), None) != None and getattr(driver, bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭⌛"), None) == True
    if sequence == bstack11l1111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ⌜") and driver != None:
      if not bstack11l1lll11_opy_ and bstack1llll1ll1l1_opy_() and bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⌝") in CONFIG and CONFIG[bstack11l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⌞")] == True and bstack11llll1111_opy_.bstack1lll1ll1_opy_(driver_command) and (bstack1l111111_opy_ or bstack1l1l1ll1l1_opy_) and not bstack1ll1l1ll1_opy_(args):
        try:
          bstack11l1lll11_opy_ = True
          logger.debug(bstack11l1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ⌟").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l1111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ⌠").format(str(err)))
        bstack11l1lll11_opy_ = False
    if sequence == bstack11l1111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ⌡"):
        if driver_command == bstack11l1111_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ⌢"):
            bstack111lll111_opy_.bstack1l111l1l_opy_({
                bstack11l1111_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭⌣"): response[bstack11l1111_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ⌤")],
                bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⌥"): store[bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⌦")]
            })
def bstack111l1111_opy_():
    global bstack1lll1l11l1_opy_
    bstack1l11l1l1l_opy_.bstack11ll1ll1ll_opy_()
    logging.shutdown()
    bstack111lll111_opy_.bstack111l1l1l1l_opy_()
    for driver in bstack1lll1l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1l1l1ll_opy_(*args):
    global bstack1lll1l11l1_opy_
    bstack111lll111_opy_.bstack111l1l1l1l_opy_()
    for driver in bstack1lll1l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11ll111_opy_, stage=STAGE.bstack1111llll1_opy_, bstack1ll1ll11ll_opy_=bstack1l1111l1ll_opy_)
def bstack11ll1l1l_opy_(self, *args, **kwargs):
    bstack1l1ll1l1_opy_ = bstack1l111ll1ll_opy_(self, *args, **kwargs)
    bstack1l11ll1ll1_opy_ = getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ⌧"), None)
    if bstack1l11ll1ll1_opy_ and bstack1l11ll1ll1_opy_.get(bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⌨"), bstack11l1111_opy_ (u"࠭ࠧ〈")) == bstack11l1111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ〉"):
        bstack111lll111_opy_.bstack1l11ll11l_opy_(self)
    return bstack1l1ll1l1_opy_
@measure(event_name=EVENTS.bstack1111lll1l_opy_, stage=STAGE.bstack1l1l1ll1ll_opy_, bstack1ll1ll11ll_opy_=bstack1l1111l1ll_opy_)
def bstack1l1111lll1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
    if bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⌫")):
        return
    bstack1l1l11l1ll_opy_.bstack1ll1lll111_opy_(bstack11l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭⌬"), True)
    global bstack11l1l11l1l_opy_
    global bstack11lll11111_opy_
    bstack11l1l11l1l_opy_ = framework_name
    logger.info(bstack11l11lll_opy_.format(bstack11l1l11l1l_opy_.split(bstack11l1111_opy_ (u"ࠪ࠱ࠬ⌭"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1llll1ll1l1_opy_():
            Service.start = bstack11ll11111_opy_
            Service.stop = bstack11l111ll11_opy_
            webdriver.Remote.get = bstack1111l11ll_opy_
            webdriver.Remote.__init__ = bstack1l1111llll_opy_
            if not isinstance(os.getenv(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ⌮")), str):
                return
            WebDriver.quit = bstack1l11lll1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111lll111_opy_.on():
            webdriver.Remote.__init__ = bstack11ll1l1l_opy_
        bstack11lll11111_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11l1111_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ⌯")):
        bstack11lll11111_opy_ = eval(os.environ.get(bstack11l1111_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ⌰")))
    if not bstack11lll11111_opy_:
        bstack11llll1lll_opy_(bstack11l1111_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ⌱"), bstack1llll1l1ll_opy_)
    if bstack11l1lllll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11l1111_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⌲")) and callable(getattr(RemoteConnection, bstack11l1111_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪ⌳"))):
                RemoteConnection._get_proxy_url = bstack11111ll11_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11111ll11_opy_
        except Exception as e:
            logger.error(bstack1lll1l11l_opy_.format(str(e)))
    if bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⌴") in str(framework_name).lower():
        if not bstack1llll1ll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11lll1111l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1ll111_opy_
            Config.getoption = bstack1llll1lll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l1111l11_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11l1l1ll_opy_, stage=STAGE.bstack1111llll1_opy_, bstack1ll1ll11ll_opy_=bstack1l1111l1ll_opy_)
def bstack1l11lll1l1_opy_(self):
    global bstack11l1l11l1l_opy_
    global bstack1llll1ll1_opy_
    global bstack1l11l1l11l_opy_
    try:
        if bstack11l1111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⌵") in bstack11l1l11l1l_opy_ and self.session_id != None and bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩ⌶"), bstack11l1111_opy_ (u"࠭ࠧ⌷")) != bstack11l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⌸"):
            bstack1l1ll1lll_opy_ = bstack11l1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⌹") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⌺")
            bstack11l1l1ll1_opy_(logger, True)
            if os.environ.get(bstack11l1111_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⌻"), None):
                self.execute_script(
                    bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ⌼") + json.dumps(
                        os.environ.get(bstack11l1111_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⌽"))) + bstack11l1111_opy_ (u"࠭ࡽࡾࠩ⌾"))
            if self != None:
                bstack1111l1l11_opy_(self, bstack1l1ll1lll_opy_, bstack11l1111_opy_ (u"ࠧ࠭ࠢࠪ⌿").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l1111ll1ll_opy_(bstack1llll1111ll_opy_):
            item = store.get(bstack11l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⍀"), None)
            if item is not None and bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⍁"), None):
                bstack11lll111l1_opy_.bstack1lll1l1l1_opy_(self, bstack1l11l1ll1l_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l1111_opy_ (u"ࠪࠫ⍂")
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ⍃") + str(e))
    bstack1l11l1l11l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11lll11l1_opy_, stage=STAGE.bstack1111llll1_opy_, bstack1ll1ll11ll_opy_=bstack1l1111l1ll_opy_)
def bstack1l1111llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1ll1_opy_
    global bstack1l1111l1ll_opy_
    global bstack111ll1l11_opy_
    global bstack11l1l11l1l_opy_
    global bstack1l111ll1ll_opy_
    global bstack1lll1l11l1_opy_
    global bstack1l1l1l1111_opy_
    global bstack1l1ll1ll11_opy_
    global bstack1l11l1ll1l_opy_
    CONFIG[bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ⍄")] = str(bstack11l1l11l1l_opy_) + str(__version__)
    command_executor = bstack11l111l1l1_opy_(bstack1l1l1l1111_opy_, CONFIG)
    logger.debug(bstack1ll11ll11l_opy_.format(command_executor))
    proxy = bstack111ll111l_opy_(CONFIG, proxy)
    bstack11llllll11_opy_ = 0
    try:
        if bstack111ll1l11_opy_ is True:
            bstack11llllll11_opy_ = int(os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⍅")))
    except:
        bstack11llllll11_opy_ = 0
    bstack1111l1l1l_opy_ = bstack11llll1l_opy_(CONFIG, bstack11llllll11_opy_)
    logger.debug(bstack1111111l_opy_.format(str(bstack1111l1l1l_opy_)))
    bstack1l11l1ll1l_opy_ = CONFIG.get(bstack11l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⍆"))[bstack11llllll11_opy_]
    if bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⍇") in CONFIG and CONFIG[bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭⍈")]:
        bstack11l1111ll1_opy_(bstack1111l1l1l_opy_, bstack1l1ll1ll11_opy_)
    if bstack11llll1l11_opy_.bstack1l1ll1l1l1_opy_(CONFIG, bstack11llllll11_opy_) and bstack11llll1l11_opy_.bstack1l11l11l1l_opy_(bstack1111l1l1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l1111ll1ll_opy_(bstack1llll1111ll_opy_):
            bstack11llll1l11_opy_.set_capabilities(bstack1111l1l1l_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll1111_opy_ = bstack1l11l11ll1_opy_(desired_capabilities)
        bstack1lll1111_opy_[bstack11l1111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ⍉")] = bstack11111ll1_opy_(CONFIG)
        bstack1l1lll1l11_opy_ = bstack11llll1l_opy_(bstack1lll1111_opy_)
        if bstack1l1lll1l11_opy_:
            bstack1111l1l1l_opy_ = update(bstack1l1lll1l11_opy_, bstack1111l1l1l_opy_)
        desired_capabilities = None
    if options:
        bstack11lll1ll11_opy_(options, bstack1111l1l1l_opy_)
    if not options:
        options = bstack11lll1l11l_opy_(bstack1111l1l1l_opy_)
    if proxy and bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⍊")):
        options.proxy(proxy)
    if options and bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⍋")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l1l111_opy_() < version.parse(bstack11l1111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ⍌")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1111l1l1l_opy_)
    logger.info(bstack1l1111l1l1_opy_)
    bstack11lllll1l1_opy_.end(EVENTS.bstack1111lll1l_opy_.value, EVENTS.bstack1111lll1l_opy_.value + bstack11l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ⍍"),
                               EVENTS.bstack1111lll1l_opy_.value + bstack11l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ⍎"), True, None)
    if bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⍏")):
        bstack1l111ll1ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⍐")):
        bstack1l111ll1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ⍑")):
        bstack1l111ll1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l111ll1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11l1llll1l_opy_ = bstack11l1111_opy_ (u"ࠬ࠭⍒")
        if bstack111l1l111_opy_() >= version.parse(bstack11l1111_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ⍓")):
            bstack11l1llll1l_opy_ = self.caps.get(bstack11l1111_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⍔"))
        else:
            bstack11l1llll1l_opy_ = self.capabilities.get(bstack11l1111_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ⍕"))
        if bstack11l1llll1l_opy_:
            bstack111ll111_opy_(bstack11l1llll1l_opy_)
            if bstack111l1l111_opy_() <= version.parse(bstack11l1111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ⍖")):
                self.command_executor._url = bstack11l1111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⍗") + bstack1l1l1l1111_opy_ + bstack11l1111_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ⍘")
            else:
                self.command_executor._url = bstack11l1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ⍙") + bstack11l1llll1l_opy_ + bstack11l1111_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ⍚")
            logger.debug(bstack11ll1lll11_opy_.format(bstack11l1llll1l_opy_))
        else:
            logger.debug(bstack11l1l11lll_opy_.format(bstack11l1111_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ⍛")))
    except Exception as e:
        logger.debug(bstack11l1l11lll_opy_.format(e))
    bstack1llll1ll1_opy_ = self.session_id
    if bstack11l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⍜") in bstack11l1l11l1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⍝"), None)
        if item:
            bstack1llll1l11ll1_opy_ = getattr(item, bstack11l1111_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⍞"), False)
            if not getattr(item, bstack11l1111_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⍟"), None) and bstack1llll1l11ll1_opy_:
                setattr(store[bstack11l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⍠")], bstack11l1111_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⍡"), self)
        bstack1l11ll1ll1_opy_ = getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⍢"), None)
        if bstack1l11ll1ll1_opy_ and bstack1l11ll1ll1_opy_.get(bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⍣"), bstack11l1111_opy_ (u"ࠩࠪ⍤")) == bstack11l1111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⍥"):
            bstack111lll111_opy_.bstack1l11ll11l_opy_(self)
    bstack1lll1l11l1_opy_.append(self)
    if bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⍦") in CONFIG and bstack11l1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⍧") in CONFIG[bstack11l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⍨")][bstack11llllll11_opy_]:
        bstack1l1111l1ll_opy_ = CONFIG[bstack11l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⍩")][bstack11llllll11_opy_][bstack11l1111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⍪")]
    logger.debug(bstack11lll11l11_opy_.format(bstack1llll1ll1_opy_))
@measure(event_name=EVENTS.bstack1lll111111_opy_, stage=STAGE.bstack1111llll1_opy_, bstack1ll1ll11ll_opy_=bstack1l1111l1ll_opy_)
def bstack1111l11ll_opy_(self, url):
    global bstack111lll1l_opy_
    global CONFIG
    try:
        bstack1lll1l111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l11ll1_opy_.format(str(err)))
    try:
        bstack111lll1l_opy_(self, url)
    except Exception as e:
        try:
            bstack11l1111l1l_opy_ = str(e)
            if any(err_msg in bstack11l1111l1l_opy_ for err_msg in bstack1ll11l1lll_opy_):
                bstack1lll1l111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l11ll1_opy_.format(str(err)))
        raise e
def bstack1lllllll1_opy_(item, when):
    global bstack11ll11ll_opy_
    try:
        bstack11ll11ll_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1111l11_opy_(item, call, rep):
    global bstack1ll1lll1_opy_
    global bstack1lll1l11l1_opy_
    name = bstack11l1111_opy_ (u"ࠩࠪ⍫")
    try:
        if rep.when == bstack11l1111_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⍬"):
            bstack1llll1ll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11l1111_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⍭"))
            try:
                if (str(skipSessionName).lower() != bstack11l1111_opy_ (u"ࠬࡺࡲࡶࡧࠪ⍮")):
                    name = str(rep.nodeid)
                    bstack11lll1111_opy_ = bstack1l11111ll1_opy_(bstack11l1111_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⍯"), name, bstack11l1111_opy_ (u"ࠧࠨ⍰"), bstack11l1111_opy_ (u"ࠨࠩ⍱"), bstack11l1111_opy_ (u"ࠩࠪ⍲"), bstack11l1111_opy_ (u"ࠪࠫ⍳"))
                    os.environ[bstack11l1111_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⍴")] = name
                    for driver in bstack1lll1l11l1_opy_:
                        if bstack1llll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack11lll1111_opy_)
            except Exception as e:
                logger.debug(bstack11l1111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⍵").format(str(e)))
            try:
                bstack11ll1lllll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1111_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⍶"):
                    status = bstack11l1111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⍷") if rep.outcome.lower() == bstack11l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⍸") else bstack11l1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⍹")
                    reason = bstack11l1111_opy_ (u"ࠪࠫ⍺")
                    if status == bstack11l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⍻"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ⍼") if status == bstack11l1111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⍽") else bstack11l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⍾")
                    data = name + bstack11l1111_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ⍿") if status == bstack11l1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⎀") else name + bstack11l1111_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭⎁") + reason
                    bstack1l11l11ll_opy_ = bstack1l11111ll1_opy_(bstack11l1111_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭⎂"), bstack11l1111_opy_ (u"ࠬ࠭⎃"), bstack11l1111_opy_ (u"࠭ࠧ⎄"), bstack11l1111_opy_ (u"ࠧࠨ⎅"), level, data)
                    for driver in bstack1lll1l11l1_opy_:
                        if bstack1llll1ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11l11ll_opy_)
            except Exception as e:
                logger.debug(bstack11l1111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⎆").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭⎇").format(str(e)))
    bstack1ll1lll1_opy_(item, call, rep)
notset = Notset()
def bstack1llll1lll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lllll1ll1_opy_
    if str(name).lower() == bstack11l1111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ⎈"):
        return bstack11l1111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ⎉")
    else:
        return bstack1lllll1ll1_opy_(self, name, default, skip)
def bstack11111ll11_opy_(self):
    global CONFIG
    global bstack11l11l11ll_opy_
    try:
        proxy = bstack1llll11111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1111_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ⎊")):
                proxies = bstack111ll1l1_opy_(proxy, bstack11l111l1l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1ll1l11_opy_ = proxies.popitem()
                    if bstack11l1111_opy_ (u"ࠨ࠺࠰࠱ࠥ⎋") in bstack1ll1ll1l11_opy_:
                        return bstack1ll1ll1l11_opy_
                    else:
                        return bstack11l1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⎌") + bstack1ll1ll1l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ⎍").format(str(e)))
    return bstack11l11l11ll_opy_(self)
def bstack11l1lllll_opy_():
    return (bstack11l1111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⎎") in CONFIG or bstack11l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⎏") in CONFIG) and bstack11111lll_opy_() and bstack111l1l111_opy_() >= version.parse(
        bstack1ll1111l_opy_)
def bstack111ll11ll_opy_(self,
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
    global bstack1l1111l1ll_opy_
    global bstack111ll1l11_opy_
    global bstack11l1l11l1l_opy_
    CONFIG[bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⎐")] = str(bstack11l1l11l1l_opy_) + str(__version__)
    bstack11llllll11_opy_ = 0
    try:
        if bstack111ll1l11_opy_ is True:
            bstack11llllll11_opy_ = int(os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⎑")))
    except:
        bstack11llllll11_opy_ = 0
    CONFIG[bstack11l1111_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ⎒")] = True
    bstack1111l1l1l_opy_ = bstack11llll1l_opy_(CONFIG, bstack11llllll11_opy_)
    logger.debug(bstack1111111l_opy_.format(str(bstack1111l1l1l_opy_)))
    if CONFIG.get(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⎓")):
        bstack11l1111ll1_opy_(bstack1111l1l1l_opy_, bstack1l1ll1ll11_opy_)
    if bstack11l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⎔") in CONFIG and bstack11l1111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⎕") in CONFIG[bstack11l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⎖")][bstack11llllll11_opy_]:
        bstack1l1111l1ll_opy_ = CONFIG[bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⎗")][bstack11llllll11_opy_][bstack11l1111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⎘")]
    import urllib
    import json
    if bstack11l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⎙") in CONFIG and str(CONFIG[bstack11l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⎚")]).lower() != bstack11l1111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⎛"):
        bstack1l111l1l1_opy_ = bstack11ll11l1l1_opy_()
        bstack11lllll11_opy_ = bstack1l111l1l1_opy_ + urllib.parse.quote(json.dumps(bstack1111l1l1l_opy_))
    else:
        bstack11lllll11_opy_ = bstack11l1111_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ⎜") + urllib.parse.quote(json.dumps(bstack1111l1l1l_opy_))
    browser = self.connect(bstack11lllll11_opy_)
    return browser
def bstack11lll11ll_opy_():
    global bstack11lll11111_opy_
    global bstack11l1l11l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1llll1ll1l_opy_
        if not bstack1llll1ll1l1_opy_():
            global bstack1lll1ll1l1_opy_
            if not bstack1lll1ll1l1_opy_:
                from bstack_utils.helper import bstack11l1l1l1_opy_, bstack1lll11l1_opy_
                bstack1lll1ll1l1_opy_ = bstack11l1l1l1_opy_()
                bstack1lll11l1_opy_(bstack11l1l11l1l_opy_)
            BrowserType.connect = bstack1llll1ll1l_opy_
            return
        BrowserType.launch = bstack111ll11ll_opy_
        bstack11lll11111_opy_ = True
    except Exception as e:
        pass
def bstack1llll1l11l11_opy_():
    global CONFIG
    global bstack1ll11l11ll_opy_
    global bstack1l1l1l1111_opy_
    global bstack1l1ll1ll11_opy_
    global bstack111ll1l11_opy_
    global bstack1l1l1llll1_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ⎝")))
    bstack1ll11l11ll_opy_ = eval(os.environ.get(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⎞")))
    bstack1l1l1l1111_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ⎟"))
    bstack1l111111l1_opy_(CONFIG, bstack1ll11l11ll_opy_)
    bstack1l1l1llll1_opy_ = bstack1l11l1l1l_opy_.bstack11l11l1111_opy_(CONFIG, bstack1l1l1llll1_opy_)
    if cli.bstack111l1ll1l_opy_():
        bstack111lllllll_opy_.invoke(bstack11l1ll1ll_opy_.CONNECT, bstack11lll1l1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⎠"), bstack11l1111_opy_ (u"ࠧ࠱ࠩ⎡")))
        cli.bstack1l111l11111_opy_(cli_context.platform_index)
        cli.bstack1l11l111111_opy_(bstack11l111l1l1_opy_(bstack1l1l1l1111_opy_, CONFIG), cli_context.platform_index, bstack11lll1l11l_opy_)
        cli.bstack1l111l111l1_opy_()
        logger.debug(bstack11l1111_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⎢") + str(cli_context.platform_index) + bstack11l1111_opy_ (u"ࠤࠥ⎣"))
        return # skip all existing bstack1llll1ll1l11_opy_
    global bstack1l111ll1ll_opy_
    global bstack1l11l1l11l_opy_
    global bstack1l11lll11l_opy_
    global bstack11l11l1l_opy_
    global bstack1l1l11l1l1_opy_
    global bstack11ll1111_opy_
    global bstack11l1ll1l11_opy_
    global bstack111lll1l_opy_
    global bstack11l11l11ll_opy_
    global bstack1lllll1ll1_opy_
    global bstack11ll11ll_opy_
    global bstack1ll1lll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l111ll1ll_opy_ = webdriver.Remote.__init__
        bstack1l11l1l11l_opy_ = WebDriver.quit
        bstack11l1ll1l11_opy_ = WebDriver.close
        bstack111lll1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1111_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⎤") in CONFIG or bstack11l1111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⎥") in CONFIG) and bstack11111lll_opy_():
        if bstack111l1l111_opy_() < version.parse(bstack1ll1111l_opy_):
            logger.error(bstack11ll111l_opy_.format(bstack111l1l111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11l1111_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⎦")) and callable(getattr(RemoteConnection, bstack11l1111_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⎧"))):
                    bstack11l11l11ll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack11l11l11ll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1lll1l11l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lllll1ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack11ll11ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111l1ll11_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll1lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ⎨"))
    bstack1l1ll1ll11_opy_ = CONFIG.get(bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ⎩"), {}).get(bstack11l1111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⎪"))
    bstack111ll1l11_opy_ = True
    bstack1l1111lll1_opy_(bstack1lll1lll1_opy_)
if (bstack111l11l1111_opy_()):
    bstack1llll1l11l11_opy_()
@bstack111l11l1l1_opy_(class_method=False)
def bstack1llll1l111ll_opy_(hook_name, event, bstack1l1lll1ll11_opy_=None):
    if hook_name not in [bstack11l1111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⎫"), bstack11l1111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⎬"), bstack11l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⎭"), bstack11l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⎮"), bstack11l1111_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⎯"), bstack11l1111_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⎰"), bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⎱"), bstack11l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ⎲")]:
        return
    node = store[bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⎳")]
    if hook_name in [bstack11l1111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⎴"), bstack11l1111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⎵")]:
        node = store[bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭⎶")]
    elif hook_name in [bstack11l1111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⎷"), bstack11l1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⎸")]:
        node = store[bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⎹")]
    hook_type = bstack111111lllll_opy_(hook_name)
    if event == bstack11l1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⎺"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_[hook_type], bstack1lll1lll1ll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l1111ll_opy_ = {
            bstack11l1111_opy_ (u"ࠬࡻࡵࡪࡦࠪ⎻"): uuid,
            bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⎼"): bstack1lllllllll_opy_(),
            bstack11l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ⎽"): bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰ࠭⎾"),
            bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⎿"): hook_type,
            bstack11l1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⏀"): hook_name
        }
        store[bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⏁")].append(uuid)
        bstack1llll11llll1_opy_ = node.nodeid
        if hook_type == bstack11l1111_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⏂"):
            if not _111l1ll11l_opy_.get(bstack1llll11llll1_opy_, None):
                _111l1ll11l_opy_[bstack1llll11llll1_opy_] = {bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⏃"): []}
            _111l1ll11l_opy_[bstack1llll11llll1_opy_][bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⏄")].append(bstack111l1111ll_opy_[bstack11l1111_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⏅")])
        _111l1ll11l_opy_[bstack1llll11llll1_opy_ + bstack11l1111_opy_ (u"ࠩ࠰ࠫ⏆") + hook_name] = bstack111l1111ll_opy_
        bstack1llll1l1ll11_opy_(node, bstack111l1111ll_opy_, bstack11l1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⏇"))
    elif event == bstack11l1111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⏈"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll11l11_opy_[hook_type], bstack1lll1lll1ll_opy_.POST, node, None, bstack1l1lll1ll11_opy_)
            return
        bstack111ll1l11l_opy_ = node.nodeid + bstack11l1111_opy_ (u"ࠬ࠳ࠧ⏉") + hook_name
        _111l1ll11l_opy_[bstack111ll1l11l_opy_][bstack11l1111_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⏊")] = bstack1lllllllll_opy_()
        bstack1llll1l1ll1l_opy_(_111l1ll11l_opy_[bstack111ll1l11l_opy_][bstack11l1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⏋")])
        bstack1llll1l1ll11_opy_(node, _111l1ll11l_opy_[bstack111ll1l11l_opy_], bstack11l1111_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⏌"), bstack1llll1ll1l1l_opy_=bstack1l1lll1ll11_opy_)
def bstack1llll1l11l1l_opy_():
    global bstack1llll11lll1l_opy_
    if bstack1ll11ll111_opy_():
        bstack1llll11lll1l_opy_ = bstack11l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⏍")
    else:
        bstack1llll11lll1l_opy_ = bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⏎")
@bstack111lll111_opy_.bstack1lllll1ll1ll_opy_
def bstack1llll1ll1lll_opy_():
    bstack1llll1l11l1l_opy_()
    if cli.is_running():
        try:
            bstack1111ll1l11l_opy_(bstack1llll1l111ll_opy_)
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⏏").format(e))
        return
    if bstack11111lll_opy_():
        bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
        bstack11l1111_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ⏐")
        if bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⏑")):
            if CONFIG.get(bstack11l1111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⏒")) is not None and int(CONFIG[bstack11l1111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⏓")]) > 1:
                bstack11l1lll1ll_opy_(bstack1l11ll1l1l_opy_)
            return
        bstack11l1lll1ll_opy_(bstack1l11ll1l1l_opy_)
    try:
        bstack1111ll1l11l_opy_(bstack1llll1l111ll_opy_)
    except Exception as e:
        logger.debug(bstack11l1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⏔").format(e))
bstack1llll1ll1lll_opy_()