# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lll1ll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11l11ll11l_opy_, bstack1ll1lll1_opy_, update, bstack111ll1ll1_opy_,
                                       bstack1ll1lll111_opy_, bstack1llll1l111_opy_, bstack1l1llllll1_opy_, bstack1lllll1lll_opy_,
                                       bstack1111ll11l_opy_, bstack1l1ll11ll1_opy_, bstack1111l111_opy_, bstack1l11lll1l1_opy_,
                                       bstack1l11l1111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1lllllllll_opy_)
from browserstack_sdk.bstack1l1l1ll1ll_opy_ import bstack1ll11l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l11lll1_opy_
from bstack_utils.capture import bstack11l111ll11_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1ll1ll1l_opy_, bstack1l11l11lll_opy_, bstack1l11ll1l1_opy_, \
    bstack11llll1ll1_opy_
from bstack_utils.helper import bstack1llll11ll1_opy_, bstack11l1lll1ll1_opy_, bstack111l1l1ll1_opy_, bstack1lll11ll1l_opy_, bstack1l1lllll1l1_opy_, bstack11ll11l1ll_opy_, \
    bstack11l11lllll1_opy_, \
    bstack11l1ll1l1ll_opy_, bstack1lll1l1l11_opy_, bstack11l1lllll_opy_, bstack11ll11l1ll1_opy_, bstack1l1111l111_opy_, Notset, \
    bstack111l11l1l_opy_, bstack11l1l1ll1l1_opy_, bstack11ll111l1ll_opy_, Result, bstack11l1lll1l1l_opy_, bstack11ll11l1111_opy_, bstack111l11l1ll_opy_, \
    bstack1lll1l1l_opy_, bstack1l1ll11ll_opy_, bstack1l11lll11l_opy_, bstack11l1l1ll11l_opy_
from bstack_utils.bstack11l11l1lll1_opy_ import bstack11l11ll1l11_opy_
from bstack_utils.messages import bstack1l1l11l1ll_opy_, bstack11lll11l11_opy_, bstack1lll1llll1_opy_, bstack1111llll1_opy_, bstack11lllll1ll_opy_, \
    bstack1l11ll1ll1_opy_, bstack11ll1l11l_opy_, bstack11lll1l11l_opy_, bstack1l1llllll_opy_, bstack1ll111l111_opy_, \
    bstack1l1l111l1l_opy_, bstack1ll11lll_opy_
from bstack_utils.proxy import bstack1l1lll11_opy_, bstack1l111l1l1l_opy_
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack111l1l11ll1_opy_, bstack111l1l1111l_opy_, bstack111l1l111l1_opy_, bstack111l1l11l1l_opy_, \
    bstack111l11llll1_opy_, bstack111l1l11l11_opy_, bstack111l1l111ll_opy_, bstack11lll111_opy_, bstack111l1l11111_opy_
from bstack_utils.bstack11ll11ll1_opy_ import bstack11l11l1ll1_opy_
from bstack_utils.bstack1lll11111l_opy_ import bstack1l11l1lll1_opy_, bstack1l1l111l_opy_, bstack1l1l11111_opy_, \
    bstack1l1111lll1_opy_, bstack11l1l11l_opy_
from bstack_utils.bstack11l111l111_opy_ import bstack11l1111lll_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack1llll1ll1l_opy_
import bstack_utils.accessibility as bstack11l1lll11_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack11l1lll1ll_opy_
from bstack_utils.bstack1l1111l1_opy_ import bstack1l1111l1_opy_
from browserstack_sdk.__init__ import bstack1l1ll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111_opy_ import bstack1ll1ll111_opy_, bstack1l1ll1l11_opy_, bstack11l1ll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l111lll111_opy_, bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1ll111_opy_ import bstack1ll1ll111_opy_, bstack1l1ll1l11_opy_, bstack11l1ll111l_opy_
bstack1111ll1l1_opy_ = None
bstack11l1l11ll1_opy_ = None
bstack1l1111111l_opy_ = None
bstack11l1l1ll1_opy_ = None
bstack1111ll1l_opy_ = None
bstack111l11111_opy_ = None
bstack11111l1l1_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack1l111l1111_opy_ = None
bstack111l1l11_opy_ = None
bstack1lll11111_opy_ = None
bstack1llllllll_opy_ = None
bstack1l1l111ll_opy_ = None
bstack11ll1l1ll1_opy_ = bstack11lll_opy_ (u"ࠬ࠭ὰ")
CONFIG = {}
bstack1l111ll1_opy_ = False
bstack1l11lllll1_opy_ = bstack11lll_opy_ (u"࠭ࠧά")
bstack111lll1l1_opy_ = bstack11lll_opy_ (u"ࠧࠨὲ")
bstack11ll11111_opy_ = False
bstack1ll1l1ll11_opy_ = []
bstack1l1l11111l_opy_ = bstack1l1ll1ll1l_opy_
bstack11111l1l1ll_opy_ = bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨέ")
bstack1l11l11l1_opy_ = {}
bstack1l11l1l11_opy_ = None
bstack1l11l1l11l_opy_ = False
logger = bstack1l11lll1_opy_.get_logger(__name__, bstack1l1l11111l_opy_)
store = {
    bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ὴ"): []
}
bstack1111l1111l1_opy_ = False
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
cli_context = bstack1l111lll111_opy_(
    test_framework_name=bstack1ll1ll1l1l_opy_[bstack11lll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧή")] if bstack1l1111l111_opy_() else bstack1ll1ll1l1l_opy_[bstack11lll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫὶ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l1ll11_opy_(page, bstack1ll11lll11_opy_):
    try:
        page.evaluate(bstack11lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨί"),
                      bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪὸ") + json.dumps(
                          bstack1ll11lll11_opy_) + bstack11lll_opy_ (u"ࠢࡾࡿࠥό"))
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨὺ"), e)
def bstack11l11ll11_opy_(page, message, level):
    try:
        page.evaluate(bstack11lll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥύ"), bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨὼ") + json.dumps(
            message) + bstack11lll_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧώ") + json.dumps(level) + bstack11lll_opy_ (u"ࠬࢃࡽࠨ὾"))
    except Exception as e:
        print(bstack11lll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ὿"), e)
def pytest_configure(config):
    global bstack1l11lllll1_opy_
    global CONFIG
    bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
    config.args = bstack1llll1ll1l_opy_.bstack1111l11l111_opy_(config.args)
    bstack1llllll11_opy_.bstack11lll11111_opy_(bstack1l11lll11l_opy_(config.getoption(bstack11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᾀ"))))
    try:
        bstack1l11lll1_opy_.bstack11l111llll1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll1ll111_opy_.invoke(bstack1l1ll1l11_opy_.CONNECT, bstack11l1ll111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᾁ"), bstack11lll_opy_ (u"ࠩ࠳ࠫᾂ")))
        config = json.loads(os.environ.get(bstack11lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤᾃ"), bstack11lll_opy_ (u"ࠦࢀࢃࠢᾄ")))
        cli.bstack1lllll1l1l1_opy_(bstack11l1lllll_opy_(bstack1l11lllll1_opy_, CONFIG), cli_context.platform_index, bstack111ll1ll1_opy_)
    if cli.bstack1lllll1ll11_opy_(bstack1lll1l11l11_opy_):
        cli.bstack1llllll1111_opy_()
        logger.debug(bstack11lll_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦᾅ") + str(cli_context.platform_index) + bstack11lll_opy_ (u"ࠨࠢᾆ"))
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.BEFORE_ALL, bstack1lll1l111l1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11lll_opy_ (u"ࠢࡸࡪࡨࡲࠧᾇ"), None)
    if cli.is_running() and when == bstack11lll_opy_ (u"ࠣࡥࡤࡰࡱࠨᾈ"):
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.LOG_REPORT, bstack1lll1l111l1_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᾉ"):
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.BEFORE_EACH, bstack1lll1l111l1_opy_.POST, item, call, outcome)
        elif when == bstack11lll_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᾊ"):
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.LOG_REPORT, bstack1lll1l111l1_opy_.POST, item, call, outcome)
        elif when == bstack11lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᾋ"):
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.AFTER_EACH, bstack1lll1l111l1_opy_.POST, item, call, outcome)
        return # skip all existing bstack11111lll1ll_opy_
    bstack1111l111ll1_opy_ = item.config.getoption(bstack11lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᾌ"))
    plugins = item.config.getoption(bstack11lll_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢᾍ"))
    report = outcome.get_result()
    bstack11111ll1lll_opy_(item, call, report)
    if bstack11lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧᾎ") not in plugins or bstack1l1111l111_opy_():
        return
    summary = []
    driver = getattr(item, bstack11lll_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤᾏ"), None)
    page = getattr(item, bstack11lll_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣᾐ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11111ll1l1l_opy_(item, report, summary, bstack1111l111ll1_opy_)
    if (page is not None):
        bstack11111lll11l_opy_(item, report, summary, bstack1111l111ll1_opy_)
def bstack11111ll1l1l_opy_(item, report, summary, bstack1111l111ll1_opy_):
    if report.when == bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᾑ") and report.skipped:
        bstack111l1l11111_opy_(report)
    if report.when in [bstack11lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᾒ"), bstack11lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᾓ")]:
        return
    if not bstack1l1lllll1l1_opy_():
        return
    try:
        if (str(bstack1111l111ll1_opy_).lower() != bstack11lll_opy_ (u"࠭ࡴࡳࡷࡨࠫᾔ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬᾕ") + json.dumps(
                    report.nodeid) + bstack11lll_opy_ (u"ࠨࡿࢀࠫᾖ"))
        os.environ[bstack11lll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᾗ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11lll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥᾘ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᾙ")))
    bstack1lll111ll_opy_ = bstack11lll_opy_ (u"ࠧࠨᾚ")
    bstack111l1l11111_opy_(report)
    if not passed:
        try:
            bstack1lll111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᾛ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᾜ")))
        bstack1lll111ll_opy_ = bstack11lll_opy_ (u"ࠣࠤᾝ")
        if not passed:
            try:
                bstack1lll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᾞ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᾟ")
                    + json.dumps(bstack11lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧᾠ"))
                    + bstack11lll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᾡ")
                )
            else:
                item._driver.execute_script(
                    bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᾢ")
                    + json.dumps(str(bstack1lll111ll_opy_))
                    + bstack11lll_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᾣ")
                )
        except Exception as e:
            summary.append(bstack11lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨᾤ").format(e))
def bstack11111llll11_opy_(test_name, error_message):
    try:
        bstack11111ll1ll1_opy_ = []
        bstack1111l111l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᾥ"), bstack11lll_opy_ (u"ࠪ࠴ࠬᾦ"))
        bstack111l1lll_opy_ = {bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᾧ"): test_name, bstack11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᾨ"): error_message, bstack11lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᾩ"): bstack1111l111l_opy_}
        bstack11111llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᾪ"))
        if os.path.exists(bstack11111llllll_opy_):
            with open(bstack11111llllll_opy_) as f:
                bstack11111ll1ll1_opy_ = json.load(f)
        bstack11111ll1ll1_opy_.append(bstack111l1lll_opy_)
        with open(bstack11111llllll_opy_, bstack11lll_opy_ (u"ࠨࡹࠪᾫ")) as f:
            json.dump(bstack11111ll1ll1_opy_, f)
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧᾬ") + str(e))
def bstack11111lll11l_opy_(item, report, summary, bstack1111l111ll1_opy_):
    if report.when in [bstack11lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᾭ"), bstack11lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᾮ")]:
        return
    if (str(bstack1111l111ll1_opy_).lower() != bstack11lll_opy_ (u"ࠬࡺࡲࡶࡧࠪᾯ")):
        bstack11l1ll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11lll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᾰ")))
    bstack1lll111ll_opy_ = bstack11lll_opy_ (u"ࠢࠣᾱ")
    bstack111l1l11111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᾲ").format(e)
                )
        try:
            if passed:
                bstack11l1l11l_opy_(getattr(item, bstack11lll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᾳ"), None), bstack11lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᾴ"))
            else:
                error_message = bstack11lll_opy_ (u"ࠫࠬ᾵")
                if bstack1lll111ll_opy_:
                    bstack11l11ll11_opy_(item._page, str(bstack1lll111ll_opy_), bstack11lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᾶ"))
                    bstack11l1l11l_opy_(getattr(item, bstack11lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᾷ"), None), bstack11lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᾸ"), str(bstack1lll111ll_opy_))
                    error_message = str(bstack1lll111ll_opy_)
                else:
                    bstack11l1l11l_opy_(getattr(item, bstack11lll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᾹ"), None), bstack11lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᾺ"))
                bstack11111llll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11lll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢΆ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11lll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣᾼ"), default=bstack11lll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ᾽"), help=bstack11lll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧι"))
    parser.addoption(bstack11lll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ᾿"), default=bstack11lll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ῀"), help=bstack11lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ῁"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11lll_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧῂ"), action=bstack11lll_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥῃ"), default=bstack11lll_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧῄ"),
                         help=bstack11lll_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ῅"))
def bstack111llll1l1_opy_(log):
    if not (log[bstack11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨῆ")] and log[bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩῇ")].strip()):
        return
    active = bstack11l111l11l_opy_()
    log = {
        bstack11lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨῈ"): log[bstack11lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩΈ")],
        bstack11lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧῊ"): bstack111l1l1ll1_opy_().isoformat() + bstack11lll_opy_ (u"ࠬࡠࠧΉ"),
        bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧῌ"): log[bstack11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ῍")],
    }
    if active:
        if active[bstack11lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭῎")] == bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ῏"):
            log[bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῐ")] = active[bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫῑ")]
        elif active[bstack11lll_opy_ (u"ࠬࡺࡹࡱࡧࠪῒ")] == bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࠫΐ"):
            log[bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ῔")] = active[bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ῕")]
    bstack11l1lll1ll_opy_.bstack11l1l1ll11_opy_([log])
def bstack11l111l11l_opy_():
    if len(store[bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ῖ")]) > 0 and store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧῗ")][-1]:
        return {
            bstack11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩῘ"): bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪῙ"),
            bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ὶ"): store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫΊ")][-1]
        }
    if store.get(bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ῜"), None):
        return {
            bstack11lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ῝"): bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࠨ῞"),
            bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ῟"): store[bstack11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩῠ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.INIT_TEST, bstack1lll1l111l1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.INIT_TEST, bstack1lll1l111l1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.TEST, bstack1lll1l111l1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll1l11_opy_ = True
        bstack11lllllll_opy_ = bstack11l1lll11_opy_.bstack1l11l111l_opy_(bstack11l1ll1l1ll_opy_(item.own_markers))
        if not cli.bstack1lllll1ll11_opy_(bstack1lll1l11l11_opy_):
            item._a11y_test_case = bstack11lllllll_opy_
            if bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬῡ"), None):
                driver = getattr(item, bstack11lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨῢ"), None)
                item._a11y_started = bstack11l1lll11_opy_.bstack1ll1lll11l_opy_(driver, bstack11lllllll_opy_)
        if not bstack11l1lll1ll_opy_.on() or bstack11111l1l1ll_opy_ != bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨΰ"):
            return
        global current_test_uuid #, bstack111lllll11_opy_
        bstack111l1ll111_opy_ = {
            bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧῤ"): uuid4().__str__(),
            bstack11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧῥ"): bstack111l1l1ll1_opy_().isoformat() + bstack11lll_opy_ (u"ࠫ࡟࠭ῦ")
        }
        current_test_uuid = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪῧ")]
        store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪῨ")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬῩ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11ll11_opy_[item.nodeid] = {**_111l11ll11_opy_[item.nodeid], **bstack111l1ll111_opy_}
        bstack1111l111lll_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩῪ"))
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫΎ"), str(err))
def pytest_runtest_setup(item):
    store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧῬ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.BEFORE_EACH, bstack1lll1l111l1_opy_.PRE, item, bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ῭"))
        return # skip all existing bstack11111lll1ll_opy_
    global bstack1111l1111l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11l1ll1_opy_():
        atexit.register(bstack11ll1l1lll_opy_)
        if not bstack1111l1111l1_opy_:
            try:
                bstack11111l1l1l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1ll11l_opy_():
                    bstack11111l1l1l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111l1l1l1_opy_:
                    signal.signal(s, bstack11111l1l11l_opy_)
                bstack1111l1111l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ΅") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l11ll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭`")
    try:
        if not bstack11l1lll1ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1ll111_opy_ = {
            bstack11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ῰"): uuid,
            bstack11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ῱"): bstack111l1l1ll1_opy_().isoformat() + bstack11lll_opy_ (u"ࠩ࡝ࠫῲ"),
            bstack11lll_opy_ (u"ࠪࡸࡾࡶࡥࠨῳ"): bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩῴ"),
            bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ῵"): bstack11lll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫῶ"),
            bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪῷ"): bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧῸ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭Ό")] = item
        store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧῺ")] = [uuid]
        if not _111l11ll11_opy_.get(item.nodeid, None):
            _111l11ll11_opy_[item.nodeid] = {bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪΏ"): [], bstack11lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧῼ"): []}
        _111l11ll11_opy_[item.nodeid][bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ´")].append(bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ῾")])
        _111l11ll11_opy_[item.nodeid + bstack11lll_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ῿")] = bstack111l1ll111_opy_
        bstack1111l111111_opy_(item, bstack111l1ll111_opy_, bstack11lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ "))
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ "), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.TEST, bstack1lll1l111l1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.AFTER_EACH, bstack1lll1l111l1_opy_.PRE, item, bstack11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ "))
        return # skip all existing bstack11111lll1ll_opy_
    try:
        global bstack1l11l11l1_opy_
        bstack1111l111l_opy_ = 0
        if bstack11ll11111_opy_ is True:
            bstack1111l111l_opy_ = int(os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ ")))
        if bstack1lll1l11ll_opy_.bstack1l111lll11_opy_() == bstack11lll_opy_ (u"ࠨࡴࡳࡷࡨࠦ "):
            if bstack1lll1l11ll_opy_.bstack1ll1l11ll1_opy_() == bstack11lll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ "):
                bstack1111l111l11_opy_ = bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ "), None)
                bstack1lll1111_opy_ = bstack1111l111l11_opy_ + bstack11lll_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧ ")
                driver = getattr(item, bstack11lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ "), None)
                bstack1ll1l1llll_opy_ = getattr(item, bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ "), None)
                bstack1ll11ll11_opy_ = getattr(item, bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ "), None)
                PercySDK.screenshot(driver, bstack1lll1111_opy_, bstack1ll1l1llll_opy_=bstack1ll1l1llll_opy_, bstack1ll11ll11_opy_=bstack1ll11ll11_opy_, bstack1ll11111l1_opy_=bstack1111l111l_opy_)
        if not cli.bstack1lllll1ll11_opy_(bstack1lll1l11l11_opy_):
            if getattr(item, bstack11lll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭​"), False):
                bstack1ll11l11_opy_.bstack1ll11l11l_opy_(getattr(item, bstack11lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ‌"), None), bstack1l11l11l1_opy_, logger, item)
        if not bstack11l1lll1ll_opy_.on():
            return
        bstack111l1ll111_opy_ = {
            bstack11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭‍"): uuid4().__str__(),
            bstack11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭‎"): bstack111l1l1ll1_opy_().isoformat() + bstack11lll_opy_ (u"ࠪ࡞ࠬ‏"),
            bstack11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩ‐"): bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ‑"),
            bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ‒"): bstack11lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ–"),
            bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ—"): bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ―")
        }
        _111l11ll11_opy_[item.nodeid + bstack11lll_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭‖")] = bstack111l1ll111_opy_
        bstack1111l111111_opy_(item, bstack111l1ll111_opy_, bstack11lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ‗"))
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫ‘"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l11l1l_opy_(fixturedef.argname):
        store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ’")] = request.node
    elif bstack111l11llll1_opy_(fixturedef.argname):
        store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ‚")] = request.node
    if not bstack11l1lll1ll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.SETUP_FIXTURE, bstack1lll1l111l1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.SETUP_FIXTURE, bstack1lll1l111l1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111lll1ll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.SETUP_FIXTURE, bstack1lll1l111l1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.SETUP_FIXTURE, bstack1lll1l111l1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111lll1ll_opy_
    try:
        fixture = {
            bstack11lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭‛"): fixturedef.argname,
            bstack11lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ“"): bstack11l11lllll1_opy_(outcome),
            bstack11lll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ”"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ„")]
        if not _111l11ll11_opy_.get(current_test_item.nodeid, None):
            _111l11ll11_opy_[current_test_item.nodeid] = {bstack11lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ‟"): []}
        _111l11ll11_opy_[current_test_item.nodeid][bstack11lll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ†")].append(fixture)
    except Exception as err:
        logger.debug(bstack11lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ‡"), str(err))
if bstack1l1111l111_opy_() and bstack11l1lll1ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.STEP, bstack1lll1l111l1_opy_.PRE, request, step)
            return
        try:
            _111l11ll11_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ•")].bstack111l1llll_opy_(id(step))
        except Exception as err:
            print(bstack11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧ‣"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.STEP, bstack1lll1l111l1_opy_.POST, request, step, exception)
            return
        try:
            _111l11ll11_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭․")].bstack111lllllll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ‥"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.STEP, bstack1lll1l111l1_opy_.POST, request, step)
            return
        try:
            bstack11l111l111_opy_: bstack11l1111lll_opy_ = _111l11ll11_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ…")]
            bstack11l111l111_opy_.bstack111lllllll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ‧"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111l1l1ll_opy_
        try:
            if not bstack11l1lll1ll_opy_.on() or bstack11111l1l1ll_opy_ != bstack11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ "):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.TEST, bstack1lll1l111l1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ "), None)
            if not _111l11ll11_opy_.get(request.node.nodeid, None):
                _111l11ll11_opy_[request.node.nodeid] = {}
            bstack11l111l111_opy_ = bstack11l1111lll_opy_.bstack1111llll1ll_opy_(
                scenario, feature, request.node,
                name=bstack111l1l11l11_opy_(request.node, scenario),
                started_at=bstack11ll11l1ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ‪"),
                tags=bstack111l1l111ll_opy_(feature, scenario),
                bstack11l111111l_opy_=bstack11l1lll1ll_opy_.bstack11l11111ll_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11ll11_opy_[request.node.nodeid][bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭‫")] = bstack11l111l111_opy_
            bstack11111lll111_opy_(bstack11l111l111_opy_.uuid)
            bstack11l1lll1ll_opy_.bstack11l1111l11_opy_(bstack11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ‬"), bstack11l111l111_opy_)
        except Exception as err:
            print(bstack11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧ‭"), str(err))
def bstack11111ll111l_opy_(bstack111lll1lll_opy_):
    if bstack111lll1lll_opy_ in store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ‮")]:
        store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ ")].remove(bstack111lll1lll_opy_)
def bstack11111lll111_opy_(test_uuid):
    store[bstack11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ‰")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack11l1lll1ll_opy_.bstack1111ll1l1l1_opy_
def bstack11111ll1lll_opy_(item, call, report):
    logger.debug(bstack11lll_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡴࡷࠫ‱"))
    global bstack11111l1l1ll_opy_
    bstack11l1llllll_opy_ = bstack11ll11l1ll_opy_()
    if hasattr(report, bstack11lll_opy_ (u"ࠪࡷࡹࡵࡰࠨ′")):
        bstack11l1llllll_opy_ = bstack11l1lll1l1l_opy_(report.stop)
    elif hasattr(report, bstack11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪ″")):
        bstack11l1llllll_opy_ = bstack11l1lll1l1l_opy_(report.start)
    try:
        if getattr(report, bstack11lll_opy_ (u"ࠬࡽࡨࡦࡰࠪ‴"), bstack11lll_opy_ (u"࠭ࠧ‵")) == bstack11lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ‶"):
            logger.debug(bstack11lll_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪ‷").format(getattr(report, bstack11lll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ‸"), bstack11lll_opy_ (u"ࠪࠫ‹")).__str__(), bstack11111l1l1ll_opy_))
            if bstack11111l1l1ll_opy_ == bstack11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ›"):
                _111l11ll11_opy_[item.nodeid][bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ※")] = bstack11l1llllll_opy_
                bstack1111l111lll_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ‼"), report, call)
                store[bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ‽")] = None
            elif bstack11111l1l1ll_opy_ == bstack11lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ‾"):
                bstack11l111l111_opy_ = _111l11ll11_opy_[item.nodeid][bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ‿")]
                bstack11l111l111_opy_.set(hooks=_111l11ll11_opy_[item.nodeid].get(bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⁀"), []))
                exception, bstack11l11111l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l11111l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11lll_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪ⁁"), bstack11lll_opy_ (u"ࠬ࠭⁂"))]
                bstack11l111l111_opy_.stop(time=bstack11l1llllll_opy_, result=Result(result=getattr(report, bstack11lll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⁃"), bstack11lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⁄")), exception=exception, bstack11l11111l1_opy_=bstack11l11111l1_opy_))
                bstack11l1lll1ll_opy_.bstack11l1111l11_opy_(bstack11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⁅"), _111l11ll11_opy_[item.nodeid][bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⁆")])
        elif getattr(report, bstack11lll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⁇"), bstack11lll_opy_ (u"ࠫࠬ⁈")) in [bstack11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⁉"), bstack11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⁊")]:
            logger.debug(bstack11lll_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ⁋").format(getattr(report, bstack11lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⁌"), bstack11lll_opy_ (u"ࠩࠪ⁍")).__str__(), bstack11111l1l1ll_opy_))
            bstack11l1111ll1_opy_ = item.nodeid + bstack11lll_opy_ (u"ࠪ࠱ࠬ⁎") + getattr(report, bstack11lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁏"), bstack11lll_opy_ (u"ࠬ࠭⁐"))
            if getattr(report, bstack11lll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⁑"), False):
                hook_type = bstack11lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ⁒") if getattr(report, bstack11lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⁓"), bstack11lll_opy_ (u"ࠩࠪ⁔")) == bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⁕") else bstack11lll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ⁖")
                _111l11ll11_opy_[bstack11l1111ll1_opy_] = {
                    bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁗"): uuid4().__str__(),
                    bstack11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⁘"): bstack11l1llllll_opy_,
                    bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⁙"): hook_type
                }
            _111l11ll11_opy_[bstack11l1111ll1_opy_][bstack11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁚")] = bstack11l1llllll_opy_
            bstack11111ll111l_opy_(_111l11ll11_opy_[bstack11l1111ll1_opy_][bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⁛")])
            bstack1111l111111_opy_(item, _111l11ll11_opy_[bstack11l1111ll1_opy_], bstack11lll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁜"), report, call)
            if getattr(report, bstack11lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁝"), bstack11lll_opy_ (u"ࠬ࠭⁞")) == bstack11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ "):
                if getattr(report, bstack11lll_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⁠"), bstack11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⁡")) == bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⁢"):
                    bstack111l1ll111_opy_ = {
                        bstack11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⁣"): uuid4().__str__(),
                        bstack11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁤"): bstack11ll11l1ll_opy_(),
                        bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⁥"): bstack11ll11l1ll_opy_()
                    }
                    _111l11ll11_opy_[item.nodeid] = {**_111l11ll11_opy_[item.nodeid], **bstack111l1ll111_opy_}
                    bstack1111l111lll_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⁦"))
                    bstack1111l111lll_opy_(item, _111l11ll11_opy_[item.nodeid], bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⁧"), report, call)
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭⁨"), str(err))
def bstack11111lll1l1_opy_(test, bstack111l1ll111_opy_, result=None, call=None, bstack1llllllll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l111l111_opy_ = {
        bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⁩"): bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⁪")],
        bstack11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩ⁫"): bstack11lll_opy_ (u"ࠬࡺࡥࡴࡶࠪ⁬"),
        bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁭"): test.name,
        bstack11lll_opy_ (u"ࠧࡣࡱࡧࡽࠬ⁮"): {
            bstack11lll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭⁯"): bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⁰"),
            bstack11lll_opy_ (u"ࠪࡧࡴࡪࡥࠨⁱ"): inspect.getsource(test.obj)
        },
        bstack11lll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⁲"): test.name,
        bstack11lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⁳"): test.name,
        bstack11lll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⁴"): bstack1llll1ll1l_opy_.bstack111l1l11l1_opy_(test),
        bstack11lll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⁵"): file_path,
        bstack11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⁶"): file_path,
        bstack11lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⁷"): bstack11lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⁸"),
        bstack11lll_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⁹"): file_path,
        bstack11lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⁺"): bstack111l1ll111_opy_[bstack11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⁻")],
        bstack11lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⁼"): bstack11lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⁽"),
        bstack11lll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬ⁾"): {
            bstack11lll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧⁿ"): test.nodeid
        },
        bstack11lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ₀"): bstack11l1ll1l1ll_opy_(test.own_markers)
    }
    if bstack1llllllll1_opy_ in [bstack11lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭₁"), bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ₂")]:
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠧ࡮ࡧࡷࡥࠬ₃")] = {
            bstack11lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ₄"): bstack111l1ll111_opy_.get(bstack11lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ₅"), [])
        }
    if bstack1llllllll1_opy_ == bstack11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ₆"):
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₇")] = bstack11lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭₈")
        bstack11l111l111_opy_[bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ₉")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭₊")]
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₋")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₌")]
    if result:
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₍")] = result.outcome
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ₎")] = result.duration * 1000
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₏")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫₐ")]
        if result.failed:
            bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ₑ")] = bstack11l1lll1ll_opy_.bstack1111l1llll_opy_(call.excinfo.typename)
            bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩₒ")] = bstack11l1lll1ll_opy_.bstack1111l1lllll_opy_(call.excinfo, result)
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨₓ")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩₔ")]
    if outcome:
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫₕ")] = bstack11l11lllll1_opy_(outcome)
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ₖ")] = 0
        bstack11l111l111_opy_[bstack11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫₗ")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬₘ")]
        if bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨₙ")] == bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩₚ"):
            bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩₛ")] = bstack11lll_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬₜ")  # bstack11111ll1111_opy_
            bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭₝")] = [{bstack11lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ₞"): [bstack11lll_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ₟")]}]
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ₠")] = bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ₡")]
    return bstack11l111l111_opy_
def bstack1111l111l1l_opy_(test, bstack111l111l1l_opy_, bstack1llllllll1_opy_, result, call, outcome, bstack11111l1llll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭₢")]
    hook_name = bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ₣")]
    hook_data = {
        bstack11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ₤"): bstack111l111l1l_opy_[bstack11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ₥")],
        bstack11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ₦"): bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭₧"),
        bstack11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ₨"): bstack11lll_opy_ (u"ࠪࡿࢂ࠭₩").format(bstack111l1l1111l_opy_(hook_name)),
        bstack11lll_opy_ (u"ࠫࡧࡵࡤࡺࠩ₪"): {
            bstack11lll_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ₫"): bstack11lll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭€"),
            bstack11lll_opy_ (u"ࠧࡤࡱࡧࡩࠬ₭"): None
        },
        bstack11lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ₮"): test.name,
        bstack11lll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ₯"): bstack1llll1ll1l_opy_.bstack111l1l11l1_opy_(test, hook_name),
        bstack11lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭₰"): file_path,
        bstack11lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭₱"): file_path,
        bstack11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₲"): bstack11lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ₳"),
        bstack11lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ₴"): file_path,
        bstack11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ₵"): bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭₶")],
        bstack11lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭₷"): bstack11lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭₸") if bstack11111l1l1ll_opy_ == bstack11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ₹") else bstack11lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭₺"),
        bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ₻"): hook_type
    }
    bstack1111lllllll_opy_ = bstack111ll11l1l_opy_(_111l11ll11_opy_.get(test.nodeid, None))
    if bstack1111lllllll_opy_:
        hook_data[bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭₼")] = bstack1111lllllll_opy_
    if result:
        hook_data[bstack11lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ₽")] = result.outcome
        hook_data[bstack11lll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ₾")] = result.duration * 1000
        hook_data[bstack11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₿")] = bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⃀")]
        if result.failed:
            hook_data[bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⃁")] = bstack11l1lll1ll_opy_.bstack1111l1llll_opy_(call.excinfo.typename)
            hook_data[bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⃂")] = bstack11l1lll1ll_opy_.bstack1111l1lllll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⃃")] = bstack11l11lllll1_opy_(outcome)
        hook_data[bstack11lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⃄")] = 100
        hook_data[bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⃅")] = bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⃆")]
        if hook_data[bstack11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⃇")] == bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⃈"):
            hook_data[bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⃉")] = bstack11lll_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⃊")  # bstack11111ll1111_opy_
            hook_data[bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⃋")] = [{bstack11lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⃌"): [bstack11lll_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⃍")]}]
    if bstack11111l1llll_opy_:
        hook_data[bstack11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⃎")] = bstack11111l1llll_opy_.result
        hook_data[bstack11lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⃏")] = bstack11l1l1ll1l1_opy_(bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⃐")], bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⃑")])
        hook_data[bstack11lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺ⃒ࠧ")] = bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⃓")]
        if hook_data[bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⃔")] == bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⃕"):
            hook_data[bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⃖")] = bstack11l1lll1ll_opy_.bstack1111l1llll_opy_(bstack11111l1llll_opy_.exception_type)
            hook_data[bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⃗")] = [{bstack11lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨ⃘ࠫ"): bstack11ll111l1ll_opy_(bstack11111l1llll_opy_.exception)}]
    return hook_data
def bstack1111l111lll_opy_(test, bstack111l1ll111_opy_, bstack1llllllll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11lll_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠡ࠯ࠣࡿࢂ⃙࠭").format(bstack1llllllll1_opy_))
    bstack11l111l111_opy_ = bstack11111lll1l1_opy_(test, bstack111l1ll111_opy_, result, call, bstack1llllllll1_opy_, outcome)
    driver = getattr(test, bstack11lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵ⃚ࠫ"), None)
    if bstack1llllllll1_opy_ == bstack11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⃛") and driver:
        bstack11l111l111_opy_[bstack11lll_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ⃜")] = bstack11l1lll1ll_opy_.bstack11l11111ll_opy_(driver)
    if bstack1llllllll1_opy_ == bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⃝"):
        bstack1llllllll1_opy_ = bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⃞")
    bstack111l11ll1l_opy_ = {
        bstack11lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⃟"): bstack1llllllll1_opy_,
        bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⃠"): bstack11l111l111_opy_
    }
    bstack11l1lll1ll_opy_.bstack11111111_opy_(bstack111l11ll1l_opy_)
    if bstack1llllllll1_opy_ == bstack11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⃡"):
        threading.current_thread().bstackTestMeta = {bstack11lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⃢"): bstack11lll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⃣")}
    elif bstack1llllllll1_opy_ == bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⃤"):
        threading.current_thread().bstackTestMeta = {bstack11lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹ⃥ࠧ"): getattr(result, bstack11lll_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦ⃦ࠩ"), bstack11lll_opy_ (u"ࠩࠪ⃧"))}
def bstack1111l111111_opy_(test, bstack111l1ll111_opy_, bstack1llllllll1_opy_, result=None, call=None, outcome=None, bstack11111l1llll_opy_=None):
    logger.debug(bstack11lll_opy_ (u"ࠪࡷࡪࡴࡤࡠࡪࡲࡳࡰࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥ࡮࡯ࡰ࡭ࠣࡨࡦࡺࡡ࠭ࠢࡨࡺࡪࡴࡴࡕࡻࡳࡩࠥ࠳ࠠࡼࡿ⃨ࠪ").format(bstack1llllllll1_opy_))
    hook_data = bstack1111l111l1l_opy_(test, bstack111l1ll111_opy_, bstack1llllllll1_opy_, result, call, outcome, bstack11111l1llll_opy_)
    bstack111l11ll1l_opy_ = {
        bstack11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⃩"): bstack1llllllll1_opy_,
        bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ⃪ࠧ"): hook_data
    }
    bstack11l1lll1ll_opy_.bstack11111111_opy_(bstack111l11ll1l_opy_)
def bstack111ll11l1l_opy_(bstack111l1ll111_opy_):
    if not bstack111l1ll111_opy_:
        return None
    if bstack111l1ll111_opy_.get(bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢ⃫ࠩ"), None):
        return getattr(bstack111l1ll111_opy_[bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣ⃬ࠪ")], bstack11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ⃭࠭"), None)
    return bstack111l1ll111_opy_.get(bstack11lll_opy_ (u"ࠩࡸࡹ࡮ࡪ⃮ࠧ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.LOG, bstack1lll1l111l1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_.LOG, bstack1lll1l111l1_opy_.POST, request, caplog)
        return # skip all existing bstack11111lll1ll_opy_
    try:
        if not bstack11l1lll1ll_opy_.on():
            return
        places = [bstack11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ⃯ࠩ"), bstack11lll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⃰"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⃱")]
        logs = []
        for bstack11111lllll1_opy_ in places:
            records = caplog.get_records(bstack11111lllll1_opy_)
            bstack11111l1ll1l_opy_ = bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃲") if bstack11111lllll1_opy_ == bstack11lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⃳") else bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃴")
            bstack11111llll1l_opy_ = request.node.nodeid + (bstack11lll_opy_ (u"ࠩࠪ⃵") if bstack11111lllll1_opy_ == bstack11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⃶") else bstack11lll_opy_ (u"ࠫ࠲࠭⃷") + bstack11111lllll1_opy_)
            test_uuid = bstack111ll11l1l_opy_(_111l11ll11_opy_.get(bstack11111llll1l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll11l1111_opy_(record.message):
                    continue
                logs.append({
                    bstack11lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⃸"): bstack11l1lll1ll1_opy_(record.created).isoformat() + bstack11lll_opy_ (u"࡚࠭ࠨ⃹"),
                    bstack11lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⃺"): record.levelname,
                    bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⃻"): record.message,
                    bstack11111l1ll1l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack11l1lll1ll_opy_.bstack11l1l1ll11_opy_(logs)
    except Exception as err:
        print(bstack11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭⃼"), str(err))
def bstack11l111ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l11l1l11l_opy_
    bstack1l1111l11l_opy_ = bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ⃽"), None) and bstack1llll11ll1_opy_(
            threading.current_thread(), bstack11lll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⃾"), None)
    bstack1ll1lll1l_opy_ = getattr(driver, bstack11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⃿"), None) != None and getattr(driver, bstack11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭℀"), None) == True
    if sequence == bstack11lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ℁") and driver != None:
      if not bstack1l11l1l11l_opy_ and bstack1l1lllll1l1_opy_() and bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨℂ") in CONFIG and CONFIG[bstack11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ℃")] == True and bstack1l1111l1_opy_.bstack11l1111ll_opy_(driver_command) and (bstack1ll1lll1l_opy_ or bstack1l1111l11l_opy_) and not bstack1lllllllll_opy_(args):
        try:
          bstack1l11l1l11l_opy_ = True
          logger.debug(bstack11lll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬ℄").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11lll_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩ℅").format(str(err)))
        bstack1l11l1l11l_opy_ = False
    if sequence == bstack11lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ℆"):
        if driver_command == bstack11lll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪℇ"):
            bstack11l1lll1ll_opy_.bstack1l1llll11_opy_({
                bstack11lll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭℈"): response[bstack11lll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ℉")],
                bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩℊ"): store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧℋ")]
            })
def bstack11ll1l1lll_opy_():
    global bstack1ll1l1ll11_opy_
    bstack1l11lll1_opy_.bstack11l11l1ll_opy_()
    logging.shutdown()
    bstack11l1lll1ll_opy_.bstack111ll1l1ll_opy_()
    for driver in bstack1ll1l1ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111l1l11l_opy_(*args):
    global bstack1ll1l1ll11_opy_
    bstack11l1lll1ll_opy_.bstack111ll1l1ll_opy_()
    for driver in bstack1ll1l1ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll11l1111_opy_, stage=STAGE.bstack11l111ll_opy_, bstack1111l1ll1_opy_=bstack1l11l1l11_opy_)
def bstack1ll1lllll_opy_(self, *args, **kwargs):
    bstack1llll11lll_opy_ = bstack1111ll1l1_opy_(self, *args, **kwargs)
    bstack11lll1l1l1_opy_ = getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬℌ"), None)
    if bstack11lll1l1l1_opy_ and bstack11lll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬℍ"), bstack11lll_opy_ (u"࠭ࠧℎ")) == bstack11lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨℏ"):
        bstack11l1lll1ll_opy_.bstack1ll11l1l1l_opy_(self)
    return bstack1llll11lll_opy_
@measure(event_name=EVENTS.bstack1l1l11llll_opy_, stage=STAGE.bstack1llll111ll_opy_, bstack1111l1ll1_opy_=bstack1l11l1l11_opy_)
def bstack1111l11l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
    if bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬℐ")):
        return
    bstack1llllll11_opy_.bstack1llllll1l1_opy_(bstack11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ℑ"), True)
    global bstack11ll1l1ll1_opy_
    global bstack1l1l1l11_opy_
    bstack11ll1l1ll1_opy_ = framework_name
    logger.info(bstack1ll11lll_opy_.format(bstack11ll1l1ll1_opy_.split(bstack11lll_opy_ (u"ࠪ࠱ࠬℒ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lllll1l1_opy_():
            Service.start = bstack1l1llllll1_opy_
            Service.stop = bstack1lllll1lll_opy_
            webdriver.Remote.get = bstack11llll1lll_opy_
            webdriver.Remote.__init__ = bstack1llll1l1l1_opy_
            if not isinstance(os.getenv(bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬℓ")), str):
                return
            WebDriver.close = bstack1111ll11l_opy_
            WebDriver.quit = bstack11ll1lll11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack11l1lll1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1lllll_opy_
        bstack1l1l1l11_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11lll_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ℔")):
        bstack1l1l1l11_opy_ = eval(os.environ.get(bstack11lll_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫℕ")))
    if not bstack1l1l1l11_opy_:
        bstack1111l111_opy_(bstack11lll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ№"), bstack1l1l111l1l_opy_)
    if bstack1l1llll1ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l111l1l1_opy_ = bstack11l1l111l1_opy_
        except Exception as e:
            logger.error(bstack1l11ll1ll1_opy_.format(str(e)))
    if bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ℗") in str(framework_name).lower():
        if not bstack1l1lllll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1lll111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1llll1l111_opy_
            Config.getoption = bstack11111l111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11ll1lll1l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11llll_opy_, stage=STAGE.bstack11l111ll_opy_, bstack1111l1ll1_opy_=bstack1l11l1l11_opy_)
def bstack11ll1lll11_opy_(self):
    global bstack11ll1l1ll1_opy_
    global bstack1lllll1l1l_opy_
    global bstack11l1l11ll1_opy_
    try:
        if bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ℘") in bstack11ll1l1ll1_opy_ and self.session_id != None and bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧℙ"), bstack11lll_opy_ (u"ࠫࠬℚ")) != bstack11lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ℛ"):
            bstack11l1111l1_opy_ = bstack11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ℜ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧℝ")
            bstack1l1ll11ll_opy_(logger, True)
            if self != None:
                bstack1l1111lll1_opy_(self, bstack11l1111l1_opy_, bstack11lll_opy_ (u"ࠨ࠮ࠣࠫ℞").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lllll1ll11_opy_(bstack1lll1l11l11_opy_):
            item = store.get(bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭℟"), None)
            if item is not None and bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ℠"), None):
                bstack1ll11l11_opy_.bstack1ll11l11l_opy_(self, bstack1l11l11l1_opy_, logger, item)
        threading.current_thread().testStatus = bstack11lll_opy_ (u"ࠫࠬ℡")
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ™") + str(e))
    bstack11l1l11ll1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11ll111ll_opy_, stage=STAGE.bstack11l111ll_opy_, bstack1111l1ll1_opy_=bstack1l11l1l11_opy_)
def bstack1llll1l1l1_opy_(self, command_executor,
             desired_capabilities=None, bstack1l11lllll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lllll1l1l_opy_
    global bstack1l11l1l11_opy_
    global bstack11ll11111_opy_
    global bstack11ll1l1ll1_opy_
    global bstack1111ll1l1_opy_
    global bstack1ll1l1ll11_opy_
    global bstack1l11lllll1_opy_
    global bstack111lll1l1_opy_
    global bstack1l11l11l1_opy_
    CONFIG[bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ℣")] = str(bstack11ll1l1ll1_opy_) + str(__version__)
    command_executor = bstack11l1lllll_opy_(bstack1l11lllll1_opy_, CONFIG)
    logger.debug(bstack1111llll1_opy_.format(command_executor))
    proxy = bstack1l11l1111_opy_(CONFIG, proxy)
    bstack1111l111l_opy_ = 0
    try:
        if bstack11ll11111_opy_ is True:
            bstack1111l111l_opy_ = int(os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧℤ")))
    except:
        bstack1111l111l_opy_ = 0
    bstack1l1111ll1l_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1111l111l_opy_)
    logger.debug(bstack11lll1l11l_opy_.format(str(bstack1l1111ll1l_opy_)))
    bstack1l11l11l1_opy_ = CONFIG.get(bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ℥"))[bstack1111l111l_opy_]
    if bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ω") in CONFIG and CONFIG[bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ℧")]:
        bstack1l1l11111_opy_(bstack1l1111ll1l_opy_, bstack111lll1l1_opy_)
    if bstack11l1lll11_opy_.bstack11l1ll111_opy_(CONFIG, bstack1111l111l_opy_) and bstack11l1lll11_opy_.bstack1l1ll1l1l_opy_(bstack1l1111ll1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lllll1ll11_opy_(bstack1lll1l11l11_opy_):
            bstack11l1lll11_opy_.set_capabilities(bstack1l1111ll1l_opy_, CONFIG)
    if desired_capabilities:
        bstack11l1l1lll1_opy_ = bstack1ll1lll1_opy_(desired_capabilities)
        bstack11l1l1lll1_opy_[bstack11lll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫℨ")] = bstack111l11l1l_opy_(CONFIG)
        bstack1ll1111l1_opy_ = bstack11l11ll11l_opy_(bstack11l1l1lll1_opy_)
        if bstack1ll1111l1_opy_:
            bstack1l1111ll1l_opy_ = update(bstack1ll1111l1_opy_, bstack1l1111ll1l_opy_)
        desired_capabilities = None
    if options:
        bstack1l1ll11ll1_opy_(options, bstack1l1111ll1l_opy_)
    if not options:
        options = bstack111ll1ll1_opy_(bstack1l1111ll1l_opy_)
    if proxy and bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ℩")):
        options.proxy(proxy)
    if options and bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬK")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lll1l1l11_opy_() < version.parse(bstack11lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭Å")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1111ll1l_opy_)
    logger.info(bstack1lll1llll1_opy_)
    bstack1lll1ll1l1_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, EVENTS.bstack1l1l11llll_opy_.value + bstack11lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣℬ"),
                               EVENTS.bstack1l1l11llll_opy_.value + bstack11lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢℭ"), True, None)
    if bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ℮")):
        bstack1111ll1l1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪℯ")):
        bstack1111ll1l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1l11lllll_opy_=bstack1l11lllll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬℰ")):
        bstack1111ll1l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l11lllll_opy_=bstack1l11lllll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1111ll1l1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l11lllll_opy_=bstack1l11lllll_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll11l11ll_opy_ = bstack11lll_opy_ (u"࠭ࠧℱ")
        if bstack1lll1l1l11_opy_() >= version.parse(bstack11lll_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨℲ")):
            bstack1ll11l11ll_opy_ = self.caps.get(bstack11lll_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣℳ"))
        else:
            bstack1ll11l11ll_opy_ = self.capabilities.get(bstack11lll_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤℴ"))
        if bstack1ll11l11ll_opy_:
            bstack1lll1l1l_opy_(bstack1ll11l11ll_opy_)
            if bstack1lll1l1l11_opy_() <= version.parse(bstack11lll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪℵ")):
                self.command_executor._url = bstack11lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧℶ") + bstack1l11lllll1_opy_ + bstack11lll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤℷ")
            else:
                self.command_executor._url = bstack11lll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣℸ") + bstack1ll11l11ll_opy_ + bstack11lll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣℹ")
            logger.debug(bstack11lll11l11_opy_.format(bstack1ll11l11ll_opy_))
        else:
            logger.debug(bstack1l1l11l1ll_opy_.format(bstack11lll_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤ℺")))
    except Exception as e:
        logger.debug(bstack1l1l11l1ll_opy_.format(e))
    bstack1lllll1l1l_opy_ = self.session_id
    if bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ℻") in bstack11ll1l1ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧℼ"), None)
        if item:
            bstack11111l1ll11_opy_ = getattr(item, bstack11lll_opy_ (u"ࠫࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࡠࡵࡷࡥࡷࡺࡥࡥࠩℽ"), False)
            if not getattr(item, bstack11lll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ℾ"), None) and bstack11111l1ll11_opy_:
                setattr(store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪℿ")], bstack11lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⅀"), self)
        bstack11lll1l1l1_opy_ = getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⅁"), None)
        if bstack11lll1l1l1_opy_ and bstack11lll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⅂"), bstack11lll_opy_ (u"ࠪࠫ⅃")) == bstack11lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⅄"):
            bstack11l1lll1ll_opy_.bstack1ll11l1l1l_opy_(self)
    bstack1ll1l1ll11_opy_.append(self)
    if bstack11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨⅅ") in CONFIG and bstack11lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫⅆ") in CONFIG[bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅇ")][bstack1111l111l_opy_]:
        bstack1l11l1l11_opy_ = CONFIG[bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫⅈ")][bstack1111l111l_opy_][bstack11lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅉ")]
    logger.debug(bstack1ll111l111_opy_.format(bstack1lllll1l1l_opy_))
@measure(event_name=EVENTS.bstack111111l1_opy_, stage=STAGE.bstack11l111ll_opy_, bstack1111l1ll1_opy_=bstack1l11l1l11_opy_)
def bstack11llll1lll_opy_(self, url):
    global bstack1l111l1111_opy_
    global CONFIG
    try:
        bstack1l1l111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1llllll_opy_.format(str(err)))
    try:
        bstack1l111l1111_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11l1l1l_opy_ = str(e)
            if any(err_msg in bstack1l11l1l1l_opy_ for err_msg in bstack1l11ll1l1_opy_):
                bstack1l1l111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1llllll_opy_.format(str(err)))
        raise e
def bstack1lllll1l11_opy_(item, when):
    global bstack1llllllll_opy_
    try:
        bstack1llllllll_opy_(item, when)
    except Exception as e:
        pass
def bstack11ll1lll1l_opy_(item, call, rep):
    global bstack1l1l111ll_opy_
    global bstack1ll1l1ll11_opy_
    name = bstack11lll_opy_ (u"ࠪࠫ⅊")
    try:
        if rep.when == bstack11lll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⅋"):
            bstack1lllll1l1l_opy_ = threading.current_thread().bstackSessionId
            bstack1111l111ll1_opy_ = item.config.getoption(bstack11lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⅌"))
            try:
                if (str(bstack1111l111ll1_opy_).lower() != bstack11lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ⅍")):
                    name = str(rep.nodeid)
                    bstack11llll111_opy_ = bstack1l11l1lll1_opy_(bstack11lll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨⅎ"), name, bstack11lll_opy_ (u"ࠨࠩ⅏"), bstack11lll_opy_ (u"ࠩࠪ⅐"), bstack11lll_opy_ (u"ࠪࠫ⅑"), bstack11lll_opy_ (u"ࠫࠬ⅒"))
                    os.environ[bstack11lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⅓")] = name
                    for driver in bstack1ll1l1ll11_opy_:
                        if bstack1lllll1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack11llll111_opy_)
            except Exception as e:
                logger.debug(bstack11lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭⅔").format(str(e)))
            try:
                bstack11lll111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11lll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⅕"):
                    status = bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⅖") if rep.outcome.lower() == bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⅗") else bstack11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⅘")
                    reason = bstack11lll_opy_ (u"ࠫࠬ⅙")
                    if status == bstack11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⅚"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11lll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ⅛") if status == bstack11lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⅜") else bstack11lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⅝")
                    data = name + bstack11lll_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ⅞") if status == bstack11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⅟") else name + bstack11lll_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧⅠ") + reason
                    bstack1ll111l11l_opy_ = bstack1l11l1lll1_opy_(bstack11lll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧⅡ"), bstack11lll_opy_ (u"࠭ࠧⅢ"), bstack11lll_opy_ (u"ࠧࠨⅣ"), bstack11lll_opy_ (u"ࠨࠩⅤ"), level, data)
                    for driver in bstack1ll1l1ll11_opy_:
                        if bstack1lllll1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll111l11l_opy_)
            except Exception as e:
                logger.debug(bstack11lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭Ⅵ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧⅦ").format(str(e)))
    bstack1l1l111ll_opy_(item, call, rep)
notset = Notset()
def bstack11111l111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll11111_opy_
    if str(name).lower() == bstack11lll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫⅧ"):
        return bstack11lll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦⅨ")
    else:
        return bstack1lll11111_opy_(self, name, default, skip)
def bstack11l1l111l1_opy_(self):
    global CONFIG
    global bstack11111l1l1_opy_
    try:
        proxy = bstack1l1lll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11lll_opy_ (u"࠭࠮ࡱࡣࡦࠫⅩ")):
                proxies = bstack1l111l1l1l_opy_(proxy, bstack11l1lllll_opy_())
                if len(proxies) > 0:
                    protocol, bstack11llllll1l_opy_ = proxies.popitem()
                    if bstack11lll_opy_ (u"ࠢ࠻࠱࠲ࠦⅪ") in bstack11llllll1l_opy_:
                        return bstack11llllll1l_opy_
                    else:
                        return bstack11lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤⅫ") + bstack11llllll1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨⅬ").format(str(e)))
    return bstack11111l1l1_opy_(self)
def bstack1l1llll1ll_opy_():
    return (bstack11lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ⅽ") in CONFIG or bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨⅮ") in CONFIG) and bstack1lll11ll1l_opy_() and bstack1lll1l1l11_opy_() >= version.parse(
        bstack1l11l11lll_opy_)
def bstack1lll11l111_opy_(self,
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
    global bstack1l11l1l11_opy_
    global bstack11ll11111_opy_
    global bstack11ll1l1ll1_opy_
    CONFIG[bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧⅯ")] = str(bstack11ll1l1ll1_opy_) + str(__version__)
    bstack1111l111l_opy_ = 0
    try:
        if bstack11ll11111_opy_ is True:
            bstack1111l111l_opy_ = int(os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ⅰ")))
    except:
        bstack1111l111l_opy_ = 0
    CONFIG[bstack11lll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨⅱ")] = True
    bstack1l1111ll1l_opy_ = bstack11l11ll11l_opy_(CONFIG, bstack1111l111l_opy_)
    logger.debug(bstack11lll1l11l_opy_.format(str(bstack1l1111ll1l_opy_)))
    if CONFIG.get(bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬⅲ")):
        bstack1l1l11111_opy_(bstack1l1111ll1l_opy_, bstack111lll1l1_opy_)
    if bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬⅳ") in CONFIG and bstack11lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨⅴ") in CONFIG[bstack11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧⅵ")][bstack1111l111l_opy_]:
        bstack1l11l1l11_opy_ = CONFIG[bstack11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨⅶ")][bstack1111l111l_opy_][bstack11lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫⅷ")]
    import urllib
    import json
    if bstack11lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫⅸ") in CONFIG and str(CONFIG[bstack11lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬⅹ")]).lower() != bstack11lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨⅺ"):
        bstack1llll1l1l_opy_ = bstack1l1ll1ll1_opy_()
        bstack11ll1l11_opy_ = bstack1llll1l1l_opy_ + urllib.parse.quote(json.dumps(bstack1l1111ll1l_opy_))
    else:
        bstack11ll1l11_opy_ = bstack11lll_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬⅻ") + urllib.parse.quote(json.dumps(bstack1l1111ll1l_opy_))
    browser = self.connect(bstack11ll1l11_opy_)
    return browser
def bstack1l1l111lll_opy_():
    global bstack1l1l1l11_opy_
    global bstack11ll1l1ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11lll1ll1_opy_
        if not bstack1l1lllll1l1_opy_():
            global bstack11ll111l_opy_
            if not bstack11ll111l_opy_:
                from bstack_utils.helper import bstack11lll11ll1_opy_, bstack1l1llll1_opy_
                bstack11ll111l_opy_ = bstack11lll11ll1_opy_()
                bstack1l1llll1_opy_(bstack11ll1l1ll1_opy_)
            BrowserType.connect = bstack11lll1ll1_opy_
            return
        BrowserType.launch = bstack1lll11l111_opy_
        bstack1l1l1l11_opy_ = True
    except Exception as e:
        pass
def bstack1111l11111l_opy_():
    global CONFIG
    global bstack1l111ll1_opy_
    global bstack1l11lllll1_opy_
    global bstack111lll1l1_opy_
    global bstack11ll11111_opy_
    global bstack1l1l11111l_opy_
    CONFIG = json.loads(os.environ.get(bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪⅼ")))
    bstack1l111ll1_opy_ = eval(os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ⅽ")))
    bstack1l11lllll1_opy_ = os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ⅾ"))
    bstack1l11lll1l1_opy_(CONFIG, bstack1l111ll1_opy_)
    bstack1l1l11111l_opy_ = bstack1l11lll1_opy_.bstack1ll1l11111_opy_(CONFIG, bstack1l1l11111l_opy_)
    if cli.bstack111l11ll_opy_():
        bstack1ll1ll111_opy_.invoke(bstack1l1ll1l11_opy_.CONNECT, bstack11l1ll111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧⅿ"), bstack11lll_opy_ (u"ࠨ࠲ࠪↀ")))
        cli.bstack1llll1ll1l1_opy_(cli_context.platform_index)
        cli.bstack1lllll1l1l1_opy_(bstack11l1lllll_opy_(bstack1l11lllll1_opy_, CONFIG), cli_context.platform_index, bstack111ll1ll1_opy_)
        cli.bstack1llllll1111_opy_()
        logger.debug(bstack11lll_opy_ (u"ࠤࡆࡐࡎࠦࡩࡴࠢࡤࡧࡹ࡯ࡶࡦࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣↁ") + str(cli_context.platform_index) + bstack11lll_opy_ (u"ࠥࠦↂ"))
        return # skip all existing bstack11111lll1ll_opy_
    global bstack1111ll1l1_opy_
    global bstack11l1l11ll1_opy_
    global bstack1l1111111l_opy_
    global bstack11l1l1ll1_opy_
    global bstack1111ll1l_opy_
    global bstack111l11111_opy_
    global bstack1l11lll1ll_opy_
    global bstack1l111l1111_opy_
    global bstack11111l1l1_opy_
    global bstack1lll11111_opy_
    global bstack1llllllll_opy_
    global bstack1l1l111ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1111ll1l1_opy_ = webdriver.Remote.__init__
        bstack11l1l11ll1_opy_ = WebDriver.quit
        bstack1l11lll1ll_opy_ = WebDriver.close
        bstack1l111l1111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧↃ") in CONFIG or bstack11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩↄ") in CONFIG) and bstack1lll11ll1l_opy_():
        if bstack1lll1l1l11_opy_() < version.parse(bstack1l11l11lll_opy_):
            logger.error(bstack11ll1l11l_opy_.format(bstack1lll1l1l11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11111l1l1_opy_ = RemoteConnection._1l111l1l1_opy_
            except Exception as e:
                logger.error(bstack1l11ll1ll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll11111_opy_ = Config.getoption
        from _pytest import runner
        bstack1llllllll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11lllll1ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1l111ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧↅ"))
    bstack111lll1l1_opy_ = CONFIG.get(bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫↆ"), {}).get(bstack11lll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪↇ"))
    bstack11ll11111_opy_ = True
    bstack1111l11l1_opy_(bstack11llll1ll1_opy_)
if (bstack11ll11l1ll1_opy_()):
    bstack1111l11111l_opy_()
@bstack111l11l1ll_opy_(class_method=False)
def bstack11111ll11l1_opy_(hook_name, event, bstack1l11l111l1l_opy_=None):
    if hook_name not in [bstack11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪↈ"), bstack11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ↉"), bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ↊"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ↋"), bstack11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ↌"), bstack11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ↍"), bstack11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ↎"), bstack11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ↏")]:
        return
    node = store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ←")]
    if hook_name in [bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ↑"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ→")]:
        node = store[bstack11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ↓")]
    elif hook_name in [bstack11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ↔"), bstack11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ↕")]:
        node = store[bstack11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ↖")]
    hook_type = bstack111l1l111l1_opy_(hook_name)
    if event == bstack11lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ↗"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_[hook_type], bstack1lll1l111l1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l111l1l_opy_ = {
            bstack11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ↘"): uuid,
            bstack11lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ↙"): bstack11ll11l1ll_opy_(),
            bstack11lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ↚"): bstack11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ↛"),
            bstack11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ↜"): hook_type,
            bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ↝"): hook_name
        }
        store[bstack11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ↞")].append(uuid)
        bstack11111ll11ll_opy_ = node.nodeid
        if hook_type == bstack11lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ↟"):
            if not _111l11ll11_opy_.get(bstack11111ll11ll_opy_, None):
                _111l11ll11_opy_[bstack11111ll11ll_opy_] = {bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ↠"): []}
            _111l11ll11_opy_[bstack11111ll11ll_opy_][bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ↡")].append(bstack111l111l1l_opy_[bstack11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↢")])
        _111l11ll11_opy_[bstack11111ll11ll_opy_ + bstack11lll_opy_ (u"ࠨ࠯ࠪ↣") + hook_name] = bstack111l111l1l_opy_
        bstack1111l111111_opy_(node, bstack111l111l1l_opy_, bstack11lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ↤"))
    elif event == bstack11lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ↥"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll111ll11_opy_[hook_type], bstack1lll1l111l1_opy_.POST, node, None, bstack1l11l111l1l_opy_)
            return
        bstack11l1111ll1_opy_ = node.nodeid + bstack11lll_opy_ (u"ࠫ࠲࠭↦") + hook_name
        _111l11ll11_opy_[bstack11l1111ll1_opy_][bstack11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ↧")] = bstack11ll11l1ll_opy_()
        bstack11111ll111l_opy_(_111l11ll11_opy_[bstack11l1111ll1_opy_][bstack11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↨")])
        bstack1111l111111_opy_(node, _111l11ll11_opy_[bstack11l1111ll1_opy_], bstack11lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ↩"), bstack11111l1llll_opy_=bstack1l11l111l1l_opy_)
def bstack1111l1111ll_opy_():
    global bstack11111l1l1ll_opy_
    if bstack1l1111l111_opy_():
        bstack11111l1l1ll_opy_ = bstack11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ↪")
    else:
        bstack11111l1l1ll_opy_ = bstack11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ↫")
@bstack11l1lll1ll_opy_.bstack1111ll1l1l1_opy_
def bstack11111l1lll1_opy_():
    bstack1111l1111ll_opy_()
    if cli.is_running():
        try:
            bstack11l11ll1l11_opy_(bstack11111ll11l1_opy_)
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ↬").format(e))
        return
    if bstack1lll11ll1l_opy_():
        bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
        bstack11lll_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ↭")
        if bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ↮")):
            if CONFIG.get(bstack11lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭↯")) is not None and int(CONFIG[bstack11lll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ↰")]) > 1:
                bstack11l11l1ll1_opy_(bstack11l111ll1_opy_)
            return
        bstack11l11l1ll1_opy_(bstack11l111ll1_opy_)
    try:
        bstack11l11ll1l11_opy_(bstack11111ll11l1_opy_)
    except Exception as e:
        logger.debug(bstack11lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ↱").format(e))
bstack11111l1lll1_opy_()