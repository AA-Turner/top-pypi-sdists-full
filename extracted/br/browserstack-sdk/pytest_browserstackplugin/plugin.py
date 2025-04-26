# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1l111lll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11ll1ll11l_opy_, bstack1l11ll1ll_opy_, update, bstack1ll1ll1l1_opy_,
                                       bstack11111111_opy_, bstack11l1ll1l1_opy_, bstack1l11ll111_opy_, bstack11lllll11_opy_,
                                       bstack1l1ll111_opy_, bstack1lll11ll1_opy_, bstack1l111ll111_opy_, bstack11l11ll1_opy_,
                                       bstack1ll111ll1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1lll1lllll_opy_)
from browserstack_sdk.bstack1ll1lll11l_opy_ import bstack1ll11l11ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11111llll_opy_
from bstack_utils.capture import bstack11l111ll1l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack111111111_opy_, bstack11l1lll11l_opy_, bstack1ll1l1ll1l_opy_, \
    bstack1111l1ll1_opy_
from bstack_utils.helper import bstack11l11l1ll1_opy_, bstack11l1l1ll1ll_opy_, bstack111l1lll1l_opy_, bstack111l11l1_opy_, bstack1l1ll1lllll_opy_, bstack11lll111l1_opy_, \
    bstack11l1l11llll_opy_, \
    bstack11l1ll1l111_opy_, bstack11l11lllll_opy_, bstack1ll1llll_opy_, bstack11l1ll1l1l1_opy_, bstack11llllll1l_opy_, Notset, \
    bstack11l1lll1_opy_, bstack11l1l11111l_opy_, bstack11l1l1l1ll1_opy_, Result, bstack11l1l1111l1_opy_, bstack11l1l1ll1l1_opy_, bstack111l1ll1ll_opy_, \
    bstack1l1111l11_opy_, bstack11lll1l1_opy_, bstack11ll1l1l11_opy_, bstack11ll1111111_opy_
from bstack_utils.bstack11l11ll1111_opy_ import bstack11l11l1lll1_opy_
from bstack_utils.messages import bstack1lllllll11_opy_, bstack1l11ll11_opy_, bstack11lllll11l_opy_, bstack1l11l111l_opy_, bstack1l1l1lll1_opy_, \
    bstack111ll1lll_opy_, bstack1ll1lll1_opy_, bstack1ll111111l_opy_, bstack1l1lll1111_opy_, bstack1ll111lll1_opy_, \
    bstack1l111l1111_opy_, bstack1l11llll1_opy_
from bstack_utils.proxy import bstack1lll1ll111_opy_, bstack11ll1l1111_opy_
from bstack_utils.bstack11lll11l_opy_ import bstack111l1l11lll_opy_, bstack111l1l1l1ll_opy_, bstack111l1l111l1_opy_, bstack111l1l11l1l_opy_, \
    bstack111l1l1l1l1_opy_, bstack111l1l11l11_opy_, bstack111l1l111ll_opy_, bstack1ll1l111l1_opy_, bstack111l1l1l11l_opy_
from bstack_utils.bstack1l11111l11_opy_ import bstack11llll11_opy_
from bstack_utils.bstack11ll1111l_opy_ import bstack11ll11l111_opy_, bstack11ll111l11_opy_, bstack11l1l1l1ll_opy_, \
    bstack11l1111l1_opy_, bstack1lll111l11_opy_
from bstack_utils.bstack11l1111l11_opy_ import bstack111lll1ll1_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111l1llll_opy_
import bstack_utils.accessibility as bstack11ll1l1ll1_opy_
from bstack_utils.bstack111llll11l_opy_ import bstack111ll1ll1_opy_
from bstack_utils.bstack11l111l11_opy_ import bstack11l111l11_opy_
from browserstack_sdk.__init__ import bstack1l1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1_opy_ import bstack1ll1lllll1_opy_, bstack1ll11l11l_opy_, bstack1ll1l111_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1l111l_opy_, bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1lllll1_opy_ import bstack1ll1lllll1_opy_, bstack1ll11l11l_opy_, bstack1ll1l111_opy_
bstack111l11ll1_opy_ = None
bstack11ll1llll1_opy_ = None
bstack11l1ll11ll_opy_ = None
bstack1l111ll11_opy_ = None
bstack11l11l11_opy_ = None
bstack1l11l1lll_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack111l1ll1_opy_ = None
bstack1ll1llllll_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack11lllll1_opy_ = None
bstack1l11ll11l_opy_ = None
bstack1ll1111ll_opy_ = bstack1l11lll_opy_ (u"ࠨࠩὥ")
CONFIG = {}
bstack1ll1l11111_opy_ = False
bstack1l1llll1l_opy_ = bstack1l11lll_opy_ (u"ࠩࠪὦ")
bstack1l1l11l1_opy_ = bstack1l11lll_opy_ (u"ࠪࠫὧ")
bstack1ll11ll1_opy_ = False
bstack1l11l1111l_opy_ = []
bstack11l1l1lll1_opy_ = bstack111111111_opy_
bstack11111l1llll_opy_ = bstack1l11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫὨ")
bstack1l111l1l11_opy_ = {}
bstack1lll111l_opy_ = None
bstack11ll111ll1_opy_ = False
logger = bstack11111llll_opy_.get_logger(__name__, bstack11l1l1lll1_opy_)
store = {
    bstack1l11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩὩ"): []
}
bstack11111l1lll1_opy_ = False
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
cli_context = bstack1l11l1l111l_opy_(
    test_framework_name=bstack1llllll11l_opy_[bstack1l11lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪὪ")] if bstack11llllll1l_opy_() else bstack1llllll11l_opy_[bstack1l11lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧὫ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11ll11llll_opy_(page, bstack1ll11111ll_opy_):
    try:
        page.evaluate(bstack1l11lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤὬ"),
                      bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭Ὥ") + json.dumps(
                          bstack1ll11111ll_opy_) + bstack1l11lll_opy_ (u"ࠥࢁࢂࠨὮ"))
    except Exception as e:
        print(bstack1l11lll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤὯ"), e)
def bstack11ll111111_opy_(page, message, level):
    try:
        page.evaluate(bstack1l11lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨὰ"), bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫά") + json.dumps(
            message) + bstack1l11lll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪὲ") + json.dumps(level) + bstack1l11lll_opy_ (u"ࠨࡿࢀࠫέ"))
    except Exception as e:
        print(bstack1l11lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧὴ"), e)
def pytest_configure(config):
    global bstack1l1llll1l_opy_
    global CONFIG
    bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
    config.args = bstack111l1llll_opy_.bstack1111l11l1l1_opy_(config.args)
    bstack11lll1l1ll_opy_.bstack1l1ll1111_opy_(bstack11ll1l1l11_opy_(config.getoption(bstack1l11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧή"))))
    try:
        bstack11111llll_opy_.bstack11l11l11lll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll1lllll1_opy_.invoke(bstack1ll11l11l_opy_.CONNECT, bstack1ll1l111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫὶ"), bstack1l11lll_opy_ (u"ࠬ࠶ࠧί")))
        config = json.loads(os.environ.get(bstack1l11lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧὸ"), bstack1l11lll_opy_ (u"ࠢࡼࡿࠥό")))
        cli.bstack1lll1ll1ll1_opy_(bstack1ll1llll_opy_(bstack1l1llll1l_opy_, CONFIG), cli_context.platform_index, bstack1ll1ll1l1_opy_)
    if cli.bstack1lll1ll111l_opy_(bstack1lll1llll11_opy_):
        cli.bstack1lll11l1lll_opy_()
        logger.debug(bstack1l11lll_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢὺ") + str(cli_context.platform_index) + bstack1l11lll_opy_ (u"ࠤࠥύ"))
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.BEFORE_ALL, bstack1lll1l1l11l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l11lll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣὼ"), None)
    if cli.is_running() and when == bstack1l11lll_opy_ (u"ࠦࡨࡧ࡬࡭ࠤώ"):
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.LOG_REPORT, bstack1lll1l1l11l_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ὾"):
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.BEFORE_EACH, bstack1lll1l1l11l_opy_.POST, item, call, outcome)
        elif when == bstack1l11lll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ὿"):
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.LOG_REPORT, bstack1lll1l1l11l_opy_.POST, item, call, outcome)
        elif when == bstack1l11lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᾀ"):
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.AFTER_EACH, bstack1lll1l1l11l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111l111111_opy_
    bstack1111l111ll1_opy_ = item.config.getoption(bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᾁ"))
    plugins = item.config.getoption(bstack1l11lll_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥᾂ"))
    report = outcome.get_result()
    bstack11111ll11ll_opy_(item, call, report)
    if bstack1l11lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣᾃ") not in plugins or bstack11llllll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l11lll_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧᾄ"), None)
    page = getattr(item, bstack1l11lll_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦᾅ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1111l11l111_opy_(item, report, summary, bstack1111l111ll1_opy_)
    if (page is not None):
        bstack11111lll1l1_opy_(item, report, summary, bstack1111l111ll1_opy_)
def bstack1111l11l111_opy_(item, report, summary, bstack1111l111ll1_opy_):
    if report.when == bstack1l11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᾆ") and report.skipped:
        bstack111l1l1l11l_opy_(report)
    if report.when in [bstack1l11lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᾇ"), bstack1l11lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᾈ")]:
        return
    if not bstack1l1ll1lllll_opy_():
        return
    try:
        if (str(bstack1111l111ll1_opy_).lower() != bstack1l11lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᾉ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨᾊ") + json.dumps(
                    report.nodeid) + bstack1l11lll_opy_ (u"ࠫࢂࢃࠧᾋ"))
        os.environ[bstack1l11lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᾌ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l11lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨᾍ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11lll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᾎ")))
    bstack1lll11l1l1_opy_ = bstack1l11lll_opy_ (u"ࠣࠤᾏ")
    bstack111l1l1l11l_opy_(report)
    if not passed:
        try:
            bstack1lll11l1l1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l11lll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᾐ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll11l1l1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l11lll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᾑ")))
        bstack1lll11l1l1_opy_ = bstack1l11lll_opy_ (u"ࠦࠧᾒ")
        if not passed:
            try:
                bstack1lll11l1l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11lll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᾓ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll11l1l1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᾔ")
                    + json.dumps(bstack1l11lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᾕ"))
                    + bstack1l11lll_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᾖ")
                )
            else:
                item._driver.execute_script(
                    bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᾗ")
                    + json.dumps(str(bstack1lll11l1l1_opy_))
                    + bstack1l11lll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᾘ")
                )
        except Exception as e:
            summary.append(bstack1l11lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᾙ").format(e))
def bstack11111l1ll11_opy_(test_name, error_message):
    try:
        bstack11111llll1l_opy_ = []
        bstack111l111l_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᾚ"), bstack1l11lll_opy_ (u"࠭࠰ࠨᾛ"))
        bstack1l1l1111l_opy_ = {bstack1l11lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᾜ"): test_name, bstack1l11lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᾝ"): error_message, bstack1l11lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᾞ"): bstack111l111l_opy_}
        bstack1111l1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11lll_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᾟ"))
        if os.path.exists(bstack1111l1111l1_opy_):
            with open(bstack1111l1111l1_opy_) as f:
                bstack11111llll1l_opy_ = json.load(f)
        bstack11111llll1l_opy_.append(bstack1l1l1111l_opy_)
        with open(bstack1111l1111l1_opy_, bstack1l11lll_opy_ (u"ࠫࡼ࠭ᾠ")) as f:
            json.dump(bstack11111llll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᾡ") + str(e))
def bstack11111lll1l1_opy_(item, report, summary, bstack1111l111ll1_opy_):
    if report.when in [bstack1l11lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᾢ"), bstack1l11lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᾣ")]:
        return
    if (str(bstack1111l111ll1_opy_).lower() != bstack1l11lll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᾤ")):
        bstack11ll11llll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l11lll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᾥ")))
    bstack1lll11l1l1_opy_ = bstack1l11lll_opy_ (u"ࠥࠦᾦ")
    bstack111l1l1l11l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll11l1l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l11lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᾧ").format(e)
                )
        try:
            if passed:
                bstack1lll111l11_opy_(getattr(item, bstack1l11lll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᾨ"), None), bstack1l11lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᾩ"))
            else:
                error_message = bstack1l11lll_opy_ (u"ࠧࠨᾪ")
                if bstack1lll11l1l1_opy_:
                    bstack11ll111111_opy_(item._page, str(bstack1lll11l1l1_opy_), bstack1l11lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᾫ"))
                    bstack1lll111l11_opy_(getattr(item, bstack1l11lll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᾬ"), None), bstack1l11lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᾭ"), str(bstack1lll11l1l1_opy_))
                    error_message = str(bstack1lll11l1l1_opy_)
                else:
                    bstack1lll111l11_opy_(getattr(item, bstack1l11lll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᾮ"), None), bstack1l11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᾯ"))
                bstack11111l1ll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l11lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᾰ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l11lll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᾱ"), default=bstack1l11lll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᾲ"), help=bstack1l11lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᾳ"))
    parser.addoption(bstack1l11lll_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᾴ"), default=bstack1l11lll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ᾵"), help=bstack1l11lll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᾶ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l11lll_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣᾷ"), action=bstack1l11lll_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨᾸ"), default=bstack1l11lll_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣᾹ"),
                         help=bstack1l11lll_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣᾺ"))
def bstack111llll111_opy_(log):
    if not (log[bstack1l11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫΆ")] and log[bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᾼ")].strip()):
        return
    active = bstack111llllll1_opy_()
    log = {
        bstack1l11lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᾽"): log[bstack1l11lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬι")],
        bstack1l11lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᾿"): bstack111l1lll1l_opy_().isoformat() + bstack1l11lll_opy_ (u"ࠨ࡜ࠪ῀"),
        bstack1l11lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ῁"): log[bstack1l11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫῂ")],
    }
    if active:
        if active[bstack1l11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩῃ")] == bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪῄ"):
            log[bstack1l11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭῅")] = active[bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧῆ")]
        elif active[bstack1l11lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ῇ")] == bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺࠧῈ"):
            log[bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪΈ")] = active[bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫῊ")]
    bstack111ll1ll1_opy_.bstack1l1l111ll_opy_([log])
def bstack111llllll1_opy_():
    if len(store[bstack1l11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩΉ")]) > 0 and store[bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪῌ")][-1]:
        return {
            bstack1l11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ῍"): bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭῎"),
            bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ῏"): store[bstack1l11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧῐ")][-1]
        }
    if store.get(bstack1l11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨῑ"), None):
        return {
            bstack1l11lll_opy_ (u"ࠬࡺࡹࡱࡧࠪῒ"): bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࠫΐ"),
            bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ῔"): store[bstack1l11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ῕")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.INIT_TEST, bstack1lll1l1l11l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.INIT_TEST, bstack1lll1l1l11l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll1111_opy_ = True
        bstack1l11l11lll_opy_ = bstack11ll1l1ll1_opy_.bstack111ll1l1l_opy_(bstack11l1ll1l111_opy_(item.own_markers))
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1llll11_opy_):
            item._a11y_test_case = bstack1l11l11lll_opy_
            if bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨῖ"), None):
                driver = getattr(item, bstack1l11lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫῗ"), None)
                item._a11y_started = bstack11ll1l1ll1_opy_.bstack1lll1l11l1_opy_(driver, bstack1l11l11lll_opy_)
        if not bstack111ll1ll1_opy_.on() or bstack11111l1llll_opy_ != bstack1l11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫῘ"):
            return
        global current_test_uuid #, bstack11l11111ll_opy_
        bstack111l111ll1_opy_ = {
            bstack1l11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪῙ"): uuid4().__str__(),
            bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪῚ"): bstack111l1lll1l_opy_().isoformat() + bstack1l11lll_opy_ (u"࡛ࠧࠩΊ")
        }
        current_test_uuid = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭῜")]
        store[bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭῝")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ῞")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l1ll11l_opy_[item.nodeid] = {**_111l1ll11l_opy_[item.nodeid], **bstack111l111ll1_opy_}
        bstack1111l11l11l_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack1l11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ῟"))
    except Exception as err:
        print(bstack1l11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧῠ"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪῡ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.BEFORE_EACH, bstack1lll1l1l11l_opy_.PRE, item, bstack1l11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ῢ"))
        return # skip all existing bstack1111l111111_opy_
    global bstack11111l1lll1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1ll1l1l1_opy_():
        atexit.register(bstack1l111l11l_opy_)
        if not bstack11111l1lll1_opy_:
            try:
                bstack11111lllll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11ll1111111_opy_():
                    bstack11111lllll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111lllll1_opy_:
                    signal.signal(s, bstack1111l111l11_opy_)
                bstack11111l1lll1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l11lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤΰ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l11lll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l11lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩῤ")
    try:
        if not bstack111ll1ll1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l111ll1_opy_ = {
            bstack1l11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῥ"): uuid,
            bstack1l11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨῦ"): bstack111l1lll1l_opy_().isoformat() + bstack1l11lll_opy_ (u"ࠬࡠࠧῧ"),
            bstack1l11lll_opy_ (u"࠭ࡴࡺࡲࡨࠫῨ"): bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬῩ"),
            bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫῪ"): bstack1l11lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧΎ"),
            bstack1l11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭Ῥ"): bstack1l11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ῭")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ΅")] = item
        store[bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ`")] = [uuid]
        if not _111l1ll11l_opy_.get(item.nodeid, None):
            _111l1ll11l_opy_[item.nodeid] = {bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭῰"): [], bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ῱"): []}
        _111l1ll11l_opy_[item.nodeid][bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨῲ")].append(bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῳ")])
        _111l1ll11l_opy_[item.nodeid + bstack1l11lll_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫῴ")] = bstack111l111ll1_opy_
        bstack11111ll111l_opy_(item, bstack111l111ll1_opy_, bstack1l11lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭῵"))
    except Exception as err:
        print(bstack1l11lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩῶ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.AFTER_EACH, bstack1lll1l1l11l_opy_.PRE, item, bstack1l11lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩῷ"))
        return # skip all existing bstack1111l111111_opy_
    try:
        global bstack1l111l1l11_opy_
        bstack111l111l_opy_ = 0
        if bstack1ll11ll1_opy_ is True:
            bstack111l111l_opy_ = int(os.environ.get(bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨῸ")))
        if bstack1l1l111lll_opy_.bstack1l111l111_opy_() == bstack1l11lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢΌ"):
            if bstack1l1l111lll_opy_.bstack1lll11l1_opy_() == bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧῺ"):
                bstack11111llll11_opy_ = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧΏ"), None)
                bstack1l111l111l_opy_ = bstack11111llll11_opy_ + bstack1l11lll_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣῼ")
                driver = getattr(item, bstack1l11lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ´"), None)
                bstack11l11l1l1_opy_ = getattr(item, bstack1l11lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ῾"), None)
                bstack1l1ll11l11_opy_ = getattr(item, bstack1l11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭῿"), None)
                PercySDK.screenshot(driver, bstack1l111l111l_opy_, bstack11l11l1l1_opy_=bstack11l11l1l1_opy_, bstack1l1ll11l11_opy_=bstack1l1ll11l11_opy_, bstack1ll11l1l11_opy_=bstack111l111l_opy_)
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1llll11_opy_):
            if getattr(item, bstack1l11lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ "), False):
                bstack1ll11l11ll_opy_.bstack1l1l1ll11l_opy_(getattr(item, bstack1l11lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ "), None), bstack1l111l1l11_opy_, logger, item)
        if not bstack111ll1ll1_opy_.on():
            return
        bstack111l111ll1_opy_ = {
            bstack1l11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ "): uuid4().__str__(),
            bstack1l11lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ "): bstack111l1lll1l_opy_().isoformat() + bstack1l11lll_opy_ (u"࡚࠭ࠨ "),
            bstack1l11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ "): bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ "),
            bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ "): bstack1l11lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ "),
            bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ "): bstack1l11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ ")
        }
        _111l1ll11l_opy_[item.nodeid + bstack1l11lll_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ​")] = bstack111l111ll1_opy_
        bstack11111ll111l_opy_(item, bstack111l111ll1_opy_, bstack1l11lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ‌"))
    except Exception as err:
        print(bstack1l11lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ‍"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l11l1l_opy_(fixturedef.argname):
        store[bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ‎")] = request.node
    elif bstack111l1l1l1l1_opy_(fixturedef.argname):
        store[bstack1l11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ‏")] = request.node
    if not bstack111ll1ll1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.SETUP_FIXTURE, bstack1lll1l1l11l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.SETUP_FIXTURE, bstack1lll1l1l11l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l111111_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.SETUP_FIXTURE, bstack1lll1l1l11l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.SETUP_FIXTURE, bstack1lll1l1l11l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l111111_opy_
    try:
        fixture = {
            bstack1l11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ‐"): fixturedef.argname,
            bstack1l11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ‑"): bstack11l1l11llll_opy_(outcome),
            bstack1l11lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ‒"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ–")]
        if not _111l1ll11l_opy_.get(current_test_item.nodeid, None):
            _111l1ll11l_opy_[current_test_item.nodeid] = {bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ—"): []}
        _111l1ll11l_opy_[current_test_item.nodeid][bstack1l11lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ―")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l11lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭‖"), str(err))
if bstack11llllll1l_opy_() and bstack111ll1ll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.STEP, bstack1lll1l1l11l_opy_.PRE, request, step)
            return
        try:
            _111l1ll11l_opy_[request.node.nodeid][bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ‗")].bstack1l11l1111_opy_(id(step))
        except Exception as err:
            print(bstack1l11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ‘"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.STEP, bstack1lll1l1l11l_opy_.POST, request, step, exception)
            return
        try:
            _111l1ll11l_opy_[request.node.nodeid][bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ’")].bstack11l111l1ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l11lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ‚"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.STEP, bstack1lll1l1l11l_opy_.POST, request, step)
            return
        try:
            bstack11l1111l11_opy_: bstack111lll1ll1_opy_ = _111l1ll11l_opy_[request.node.nodeid][bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ‛")]
            bstack11l1111l11_opy_.bstack11l111l1ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l11lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭“"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111l1llll_opy_
        try:
            if not bstack111ll1ll1_opy_.on() or bstack11111l1llll_opy_ != bstack1l11lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ”"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ„"), None)
            if not _111l1ll11l_opy_.get(request.node.nodeid, None):
                _111l1ll11l_opy_[request.node.nodeid] = {}
            bstack11l1111l11_opy_ = bstack111lll1ll1_opy_.bstack111l1111l11_opy_(
                scenario, feature, request.node,
                name=bstack111l1l11l11_opy_(request.node, scenario),
                started_at=bstack11lll111l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l11lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ‟"),
                tags=bstack111l1l111ll_opy_(feature, scenario),
                bstack11l111ll11_opy_=bstack111ll1ll1_opy_.bstack11l1111lll_opy_(driver) if driver and driver.session_id else {}
            )
            _111l1ll11l_opy_[request.node.nodeid][bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ†")] = bstack11l1111l11_opy_
            bstack11111llllll_opy_(bstack11l1111l11_opy_.uuid)
            bstack111ll1ll1_opy_.bstack11l111l11l_opy_(bstack1l11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ‡"), bstack11l1111l11_opy_)
        except Exception as err:
            print(bstack1l11lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ•"), str(err))
def bstack11111lll1ll_opy_(bstack11l1111l1l_opy_):
    if bstack11l1111l1l_opy_ in store[bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭‣")]:
        store[bstack1l11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ․")].remove(bstack11l1111l1l_opy_)
def bstack11111llllll_opy_(test_uuid):
    store[bstack1l11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ‥")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111ll1ll1_opy_.bstack1111ll11l11_opy_
def bstack11111ll11ll_opy_(item, call, report):
    logger.debug(bstack1l11lll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ…"))
    global bstack11111l1llll_opy_
    bstack1lll11l11_opy_ = bstack11lll111l1_opy_()
    if hasattr(report, bstack1l11lll_opy_ (u"࠭ࡳࡵࡱࡳࠫ‧")):
        bstack1lll11l11_opy_ = bstack11l1l1111l1_opy_(report.stop)
    elif hasattr(report, bstack1l11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ ")):
        bstack1lll11l11_opy_ = bstack11l1l1111l1_opy_(report.start)
    try:
        if getattr(report, bstack1l11lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ "), bstack1l11lll_opy_ (u"ࠩࠪ‪")) == bstack1l11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ‫"):
            logger.debug(bstack1l11lll_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭‬").format(getattr(report, bstack1l11lll_opy_ (u"ࠬࡽࡨࡦࡰࠪ‭"), bstack1l11lll_opy_ (u"࠭ࠧ‮")).__str__(), bstack11111l1llll_opy_))
            if bstack11111l1llll_opy_ == bstack1l11lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ "):
                _111l1ll11l_opy_[item.nodeid][bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭‰")] = bstack1lll11l11_opy_
                bstack1111l11l11l_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ‱"), report, call)
                store[bstack1l11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ′")] = None
            elif bstack11111l1llll_opy_ == bstack1l11lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ″"):
                bstack11l1111l11_opy_ = _111l1ll11l_opy_[item.nodeid][bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ‴")]
                bstack11l1111l11_opy_.set(hooks=_111l1ll11l_opy_[item.nodeid].get(bstack1l11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ‵"), []))
                exception, bstack11l1111ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1111ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l11lll_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭‶"), bstack1l11lll_opy_ (u"ࠨࠩ‷"))]
                bstack11l1111l11_opy_.stop(time=bstack1lll11l11_opy_, result=Result(result=getattr(report, bstack1l11lll_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ‸"), bstack1l11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ‹")), exception=exception, bstack11l1111ll1_opy_=bstack11l1111ll1_opy_))
                bstack111ll1ll1_opy_.bstack11l111l11l_opy_(bstack1l11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭›"), _111l1ll11l_opy_[item.nodeid][bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ※")])
        elif getattr(report, bstack1l11lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ‼"), bstack1l11lll_opy_ (u"ࠧࠨ‽")) in [bstack1l11lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ‾"), bstack1l11lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ‿")]:
            logger.debug(bstack1l11lll_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⁀").format(getattr(report, bstack1l11lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁁"), bstack1l11lll_opy_ (u"ࠬ࠭⁂")).__str__(), bstack11111l1llll_opy_))
            bstack11l11111l1_opy_ = item.nodeid + bstack1l11lll_opy_ (u"࠭࠭ࠨ⁃") + getattr(report, bstack1l11lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⁄"), bstack1l11lll_opy_ (u"ࠨࠩ⁅"))
            if getattr(report, bstack1l11lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⁆"), False):
                hook_type = bstack1l11lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⁇") if getattr(report, bstack1l11lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁈"), bstack1l11lll_opy_ (u"ࠬ࠭⁉")) == bstack1l11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⁊") else bstack1l11lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⁋")
                _111l1ll11l_opy_[bstack11l11111l1_opy_] = {
                    bstack1l11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁌"): uuid4().__str__(),
                    bstack1l11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁍"): bstack1lll11l11_opy_,
                    bstack1l11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⁎"): hook_type
                }
            _111l1ll11l_opy_[bstack11l11111l1_opy_][bstack1l11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁏")] = bstack1lll11l11_opy_
            bstack11111lll1ll_opy_(_111l1ll11l_opy_[bstack11l11111l1_opy_][bstack1l11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁐")])
            bstack11111ll111l_opy_(item, _111l1ll11l_opy_[bstack11l11111l1_opy_], bstack1l11lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⁑"), report, call)
            if getattr(report, bstack1l11lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⁒"), bstack1l11lll_opy_ (u"ࠨࠩ⁓")) == bstack1l11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⁔"):
                if getattr(report, bstack1l11lll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⁕"), bstack1l11lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⁖")) == bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⁗"):
                    bstack111l111ll1_opy_ = {
                        bstack1l11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⁘"): uuid4().__str__(),
                        bstack1l11lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⁙"): bstack11lll111l1_opy_(),
                        bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁚"): bstack11lll111l1_opy_()
                    }
                    _111l1ll11l_opy_[item.nodeid] = {**_111l1ll11l_opy_[item.nodeid], **bstack111l111ll1_opy_}
                    bstack1111l11l11l_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⁛"))
                    bstack1111l11l11l_opy_(item, _111l1ll11l_opy_[item.nodeid], bstack1l11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁜"), report, call)
    except Exception as err:
        print(bstack1l11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ⁝"), str(err))
def bstack11111ll1ll1_opy_(test, bstack111l111ll1_opy_, result=None, call=None, bstack11l11llll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l1111l11_opy_ = {
        bstack1l11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁞"): bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ ")],
        bstack1l11lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⁠"): bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭⁡"),
        bstack1l11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⁢"): test.name,
        bstack1l11lll_opy_ (u"ࠪࡦࡴࡪࡹࠨ⁣"): {
            bstack1l11lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⁤"): bstack1l11lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⁥"),
            bstack1l11lll_opy_ (u"࠭ࡣࡰࡦࡨࠫ⁦"): inspect.getsource(test.obj)
        },
        bstack1l11lll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⁧"): test.name,
        bstack1l11lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⁨"): test.name,
        bstack1l11lll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⁩"): bstack111l1llll_opy_.bstack111ll1ll11_opy_(test),
        bstack1l11lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭⁪"): file_path,
        bstack1l11lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⁫"): file_path,
        bstack1l11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⁬"): bstack1l11lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⁭"),
        bstack1l11lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⁮"): file_path,
        bstack1l11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⁯"): bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁰")],
        bstack1l11lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ⁱ"): bstack1l11lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⁲"),
        bstack1l11lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⁳"): {
            bstack1l11lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ⁴"): test.nodeid
        },
        bstack1l11lll_opy_ (u"ࠧࡵࡣࡪࡷࠬ⁵"): bstack11l1ll1l111_opy_(test.own_markers)
    }
    if bstack11l11llll1_opy_ in [bstack1l11lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⁶"), bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁷")]:
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠪࡱࡪࡺࡡࠨ⁸")] = {
            bstack1l11lll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⁹"): bstack111l111ll1_opy_.get(bstack1l11lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⁺"), [])
        }
    if bstack11l11llll1_opy_ == bstack1l11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⁻"):
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁼")] = bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⁽")
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⁾")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩⁿ")]
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₀")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₁")]
    if result:
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭₂")] = result.outcome
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ₃")] = result.duration * 1000
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₄")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₅")]
        if result.failed:
            bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ₆")] = bstack111ll1ll1_opy_.bstack1111l1llll_opy_(call.excinfo.typename)
            bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ₇")] = bstack111ll1ll1_opy_.bstack1111ll111ll_opy_(call.excinfo, result)
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ₈")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ₉")]
    if outcome:
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₊")] = bstack11l1l11llll_opy_(outcome)
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ₋")] = 0
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₌")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ₍")]
        if bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₎")] == bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ₏"):
            bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬₐ")] = bstack1l11lll_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨₑ")  # bstack11111lll11l_opy_
            bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩₒ")] = [{bstack1l11lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬₓ"): [bstack1l11lll_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧₔ")]}]
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪₕ")] = bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫₖ")]
    return bstack11l1111l11_opy_
def bstack11111ll1l1l_opy_(test, bstack111lll1l1l_opy_, bstack11l11llll1_opy_, result, call, outcome, bstack11111lll111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩₗ")]
    hook_name = bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪₘ")]
    hook_data = {
        bstack1l11lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ₙ"): bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧₚ")],
        bstack1l11lll_opy_ (u"ࠪࡸࡾࡶࡥࠨₛ"): bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩₜ"),
        bstack1l11lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₝"): bstack1l11lll_opy_ (u"࠭ࡻࡾࠩ₞").format(bstack111l1l1l1ll_opy_(hook_name)),
        bstack1l11lll_opy_ (u"ࠧࡣࡱࡧࡽࠬ₟"): {
            bstack1l11lll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭₠"): bstack1l11lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ₡"),
            bstack1l11lll_opy_ (u"ࠪࡧࡴࡪࡥࠨ₢"): None
        },
        bstack1l11lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ₣"): test.name,
        bstack1l11lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ₤"): bstack111l1llll_opy_.bstack111ll1ll11_opy_(test, hook_name),
        bstack1l11lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ₥"): file_path,
        bstack1l11lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ₦"): file_path,
        bstack1l11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₧"): bstack1l11lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ₨"),
        bstack1l11lll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ₩"): file_path,
        bstack1l11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₪"): bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₫")],
        bstack1l11lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ€"): bstack1l11lll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ₭") if bstack11111l1llll_opy_ == bstack1l11lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ₮") else bstack1l11lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ₯"),
        bstack1l11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭₰"): hook_type
    }
    bstack111l1111l1l_opy_ = bstack111ll1l1ll_opy_(_111l1ll11l_opy_.get(test.nodeid, None))
    if bstack111l1111l1l_opy_:
        hook_data[bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ₱")] = bstack111l1111l1l_opy_
    if result:
        hook_data[bstack1l11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₲")] = result.outcome
        hook_data[bstack1l11lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ₳")] = result.duration * 1000
        hook_data[bstack1l11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₴")] = bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₵")]
        if result.failed:
            hook_data[bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ₶")] = bstack111ll1ll1_opy_.bstack1111l1llll_opy_(call.excinfo.typename)
            hook_data[bstack1l11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ₷")] = bstack111ll1ll1_opy_.bstack1111ll111ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₸")] = bstack11l1l11llll_opy_(outcome)
        hook_data[bstack1l11lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭₹")] = 100
        hook_data[bstack1l11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ₺")] = bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₻")]
        if hook_data[bstack1l11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₼")] == bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ₽"):
            hook_data[bstack1l11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ₾")] = bstack1l11lll_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ₿")  # bstack11111lll11l_opy_
            hook_data[bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⃀")] = [{bstack1l11lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⃁"): [bstack1l11lll_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ⃂")]}]
    if bstack11111lll111_opy_:
        hook_data[bstack1l11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⃃")] = bstack11111lll111_opy_.result
        hook_data[bstack1l11lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⃄")] = bstack11l1l11111l_opy_(bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⃅")], bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⃆")])
        hook_data[bstack1l11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⃇")] = bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃈")]
        if hook_data[bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⃉")] == bstack1l11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⃊"):
            hook_data[bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⃋")] = bstack111ll1ll1_opy_.bstack1111l1llll_opy_(bstack11111lll111_opy_.exception_type)
            hook_data[bstack1l11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⃌")] = [{bstack1l11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⃍"): bstack11l1l1l1ll1_opy_(bstack11111lll111_opy_.exception)}]
    return hook_data
def bstack1111l11l11l_opy_(test, bstack111l111ll1_opy_, bstack11l11llll1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l11lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⃎").format(bstack11l11llll1_opy_))
    bstack11l1111l11_opy_ = bstack11111ll1ll1_opy_(test, bstack111l111ll1_opy_, result, call, bstack11l11llll1_opy_, outcome)
    driver = getattr(test, bstack1l11lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⃏"), None)
    if bstack11l11llll1_opy_ == bstack1l11lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⃐") and driver:
        bstack11l1111l11_opy_[bstack1l11lll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧ⃑")] = bstack111ll1ll1_opy_.bstack11l1111lll_opy_(driver)
    if bstack11l11llll1_opy_ == bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦ⃒ࠪ"):
        bstack11l11llll1_opy_ = bstack1l11lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨ⃓ࠬ")
    bstack111lll1l11_opy_ = {
        bstack1l11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⃔"): bstack11l11llll1_opy_,
        bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⃕"): bstack11l1111l11_opy_
    }
    bstack111ll1ll1_opy_.bstack11lllll1l_opy_(bstack111lll1l11_opy_)
    if bstack11l11llll1_opy_ == bstack1l11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⃖"):
        threading.current_thread().bstackTestMeta = {bstack1l11lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⃗"): bstack1l11lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨ⃘ࠩ")}
    elif bstack11l11llll1_opy_ == bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧ⃙ࠫ"):
        threading.current_thread().bstackTestMeta = {bstack1l11lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ⃚ࠪ"): getattr(result, bstack1l11lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⃛"), bstack1l11lll_opy_ (u"ࠬ࠭⃜"))}
def bstack11111ll111l_opy_(test, bstack111l111ll1_opy_, bstack11l11llll1_opy_, result=None, call=None, outcome=None, bstack11111lll111_opy_=None):
    logger.debug(bstack1l11lll_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⃝").format(bstack11l11llll1_opy_))
    hook_data = bstack11111ll1l1l_opy_(test, bstack111l111ll1_opy_, bstack11l11llll1_opy_, result, call, outcome, bstack11111lll111_opy_)
    bstack111lll1l11_opy_ = {
        bstack1l11lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⃞"): bstack11l11llll1_opy_,
        bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪ⃟"): hook_data
    }
    bstack111ll1ll1_opy_.bstack11lllll1l_opy_(bstack111lll1l11_opy_)
def bstack111ll1l1ll_opy_(bstack111l111ll1_opy_):
    if not bstack111l111ll1_opy_:
        return None
    if bstack111l111ll1_opy_.get(bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⃠"), None):
        return getattr(bstack111l111ll1_opy_[bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⃡")], bstack1l11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⃢"), None)
    return bstack111l111ll1_opy_.get(bstack1l11lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⃣"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.LOG, bstack1lll1l1l11l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_.LOG, bstack1lll1l1l11l_opy_.POST, request, caplog)
        return # skip all existing bstack1111l111111_opy_
    try:
        if not bstack111ll1ll1_opy_.on():
            return
        places = [bstack1l11lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⃤"), bstack1l11lll_opy_ (u"ࠧࡤࡣ࡯ࡰ⃥ࠬ"), bstack1l11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ⃦ࠪ")]
        logs = []
        for bstack11111ll11l1_opy_ in places:
            records = caplog.get_records(bstack11111ll11l1_opy_)
            bstack11111ll1lll_opy_ = bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃧") if bstack11111ll11l1_opy_ == bstack1l11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⃨") else bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃩")
            bstack11111l1l1ll_opy_ = request.node.nodeid + (bstack1l11lll_opy_ (u"⃪ࠬ࠭") if bstack11111ll11l1_opy_ == bstack1l11lll_opy_ (u"࠭ࡣࡢ࡮࡯⃫ࠫ") else bstack1l11lll_opy_ (u"ࠧ࠮⃬ࠩ") + bstack11111ll11l1_opy_)
            test_uuid = bstack111ll1l1ll_opy_(_111l1ll11l_opy_.get(bstack11111l1l1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1l1ll1l1_opy_(record.message):
                    continue
                logs.append({
                    bstack1l11lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳ⃭ࠫ"): bstack11l1l1ll1ll_opy_(record.created).isoformat() + bstack1l11lll_opy_ (u"ࠩ࡝⃮ࠫ"),
                    bstack1l11lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭⃯ࠩ"): record.levelname,
                    bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃰"): record.message,
                    bstack11111ll1lll_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111ll1ll1_opy_.bstack1l1l111ll_opy_(logs)
    except Exception as err:
        print(bstack1l11lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ⃱"), str(err))
def bstack1lll111ll_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11ll111ll1_opy_
    bstack1lll1111l_opy_ = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ⃲"), None) and bstack11l11l1ll1_opy_(
            threading.current_thread(), bstack1l11lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⃳"), None)
    bstack1ll1l1l1l1_opy_ = getattr(driver, bstack1l11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⃴"), None) != None and getattr(driver, bstack1l11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⃵"), None) == True
    if sequence == bstack1l11lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⃶") and driver != None:
      if not bstack11ll111ll1_opy_ and bstack1l1ll1lllll_opy_() and bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃷") in CONFIG and CONFIG[bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃸")] == True and bstack11l111l11_opy_.bstack1llll111l1_opy_(driver_command) and (bstack1ll1l1l1l1_opy_ or bstack1lll1111l_opy_) and not bstack1lll1lllll_opy_(args):
        try:
          bstack11ll111ll1_opy_ = True
          logger.debug(bstack1l11lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ⃹").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l11lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ⃺").format(str(err)))
        bstack11ll111ll1_opy_ = False
    if sequence == bstack1l11lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⃻"):
        if driver_command == bstack1l11lll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭⃼"):
            bstack111ll1ll1_opy_.bstack11ll1ll111_opy_({
                bstack1l11lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ⃽"): response[bstack1l11lll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ⃾")],
                bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃿"): store[bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ℀")]
            })
def bstack1l111l11l_opy_():
    global bstack1l11l1111l_opy_
    bstack11111llll_opy_.bstack11ll1l11ll_opy_()
    logging.shutdown()
    bstack111ll1ll1_opy_.bstack111l11ll1l_opy_()
    for driver in bstack1l11l1111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111l111l11_opy_(*args):
    global bstack1l11l1111l_opy_
    bstack111ll1ll1_opy_.bstack111l11ll1l_opy_()
    for driver in bstack1l11l1111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1111ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack11lll1llll_opy_=bstack1lll111l_opy_)
def bstack1lll1l111_opy_(self, *args, **kwargs):
    bstack1l1111l1ll_opy_ = bstack111l11ll1_opy_(self, *args, **kwargs)
    bstack1l1lll1l1l_opy_ = getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ℁"), None)
    if bstack1l1lll1l1l_opy_ and bstack1l1lll1l1l_opy_.get(bstack1l11lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨℂ"), bstack1l11lll_opy_ (u"ࠩࠪ℃")) == bstack1l11lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ℄"):
        bstack111ll1ll1_opy_.bstack1ll1l1l1l_opy_(self)
    return bstack1l1111l1ll_opy_
@measure(event_name=EVENTS.bstack1llll11l1_opy_, stage=STAGE.bstack1l1111l1_opy_, bstack11lll1llll_opy_=bstack1lll111l_opy_)
def bstack1l111l11_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
    if bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ℅")):
        return
    bstack11lll1l1ll_opy_.bstack111111l1l_opy_(bstack1l11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ℆"), True)
    global bstack1ll1111ll_opy_
    global bstack11ll11l11l_opy_
    bstack1ll1111ll_opy_ = framework_name
    logger.info(bstack1l11llll1_opy_.format(bstack1ll1111ll_opy_.split(bstack1l11lll_opy_ (u"࠭࠭ࠨℇ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll1lllll_opy_():
            Service.start = bstack1l11ll111_opy_
            Service.stop = bstack11lllll11_opy_
            webdriver.Remote.get = bstack11ll1ll1_opy_
            webdriver.Remote.__init__ = bstack1l1l1ll111_opy_
            if not isinstance(os.getenv(bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ℈")), str):
                return
            WebDriver.close = bstack1l1ll111_opy_
            WebDriver.quit = bstack1lll1lll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111ll1ll1_opy_.on():
            webdriver.Remote.__init__ = bstack1lll1l111_opy_
        bstack11ll11l11l_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l11lll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭℉")):
        bstack11ll11l11l_opy_ = eval(os.environ.get(bstack1l11lll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧℊ")))
    if not bstack11ll11l11l_opy_:
        bstack1l111ll111_opy_(bstack1l11lll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧℋ"), bstack1l111l1111_opy_)
    if bstack1ll11ll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._11l11l1ll_opy_ = bstack1l1l1l111_opy_
        except Exception as e:
            logger.error(bstack111ll1lll_opy_.format(str(e)))
    if bstack1l11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫℌ") in str(framework_name).lower():
        if not bstack1l1ll1lllll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11111111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1ll1l1_opy_
            Config.getoption = bstack1lllll1ll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1ll1111l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1111l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack11lll1llll_opy_=bstack1lll111l_opy_)
def bstack1lll1lll_opy_(self):
    global bstack1ll1111ll_opy_
    global bstack1l1111111l_opy_
    global bstack11ll1llll1_opy_
    try:
        if bstack1l11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬℍ") in bstack1ll1111ll_opy_ and self.session_id != None and bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪℎ"), bstack1l11lll_opy_ (u"ࠧࠨℏ")) != bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩℐ"):
            bstack1ll111l1ll_opy_ = bstack1l11lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩℑ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l11lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪℒ")
            bstack11lll1l1_opy_(logger, True)
            if self != None:
                bstack11l1111l1_opy_(self, bstack1ll111l1ll_opy_, bstack1l11lll_opy_ (u"ࠫ࠱ࠦࠧℓ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1llll11_opy_):
            item = store.get(bstack1l11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ℔"), None)
            if item is not None and bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬℕ"), None):
                bstack1ll11l11ll_opy_.bstack1l1l1ll11l_opy_(self, bstack1l111l1l11_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l11lll_opy_ (u"ࠧࠨ№")
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ℗") + str(e))
    bstack11ll1llll1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11lll1l11l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack11lll1llll_opy_=bstack1lll111l_opy_)
def bstack1l1l1ll111_opy_(self, command_executor,
             desired_capabilities=None, bstack1l1l1l1l1l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1111111l_opy_
    global bstack1lll111l_opy_
    global bstack1ll11ll1_opy_
    global bstack1ll1111ll_opy_
    global bstack111l11ll1_opy_
    global bstack1l11l1111l_opy_
    global bstack1l1llll1l_opy_
    global bstack1l1l11l1_opy_
    global bstack1l111l1l11_opy_
    CONFIG[bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ℘")] = str(bstack1ll1111ll_opy_) + str(__version__)
    command_executor = bstack1ll1llll_opy_(bstack1l1llll1l_opy_, CONFIG)
    logger.debug(bstack1l11l111l_opy_.format(command_executor))
    proxy = bstack1ll111ll1l_opy_(CONFIG, proxy)
    bstack111l111l_opy_ = 0
    try:
        if bstack1ll11ll1_opy_ is True:
            bstack111l111l_opy_ = int(os.environ.get(bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪℙ")))
    except:
        bstack111l111l_opy_ = 0
    bstack1ll1ll1ll1_opy_ = bstack11ll1ll11l_opy_(CONFIG, bstack111l111l_opy_)
    logger.debug(bstack1ll111111l_opy_.format(str(bstack1ll1ll1ll1_opy_)))
    bstack1l111l1l11_opy_ = CONFIG.get(bstack1l11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧℚ"))[bstack111l111l_opy_]
    if bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩℛ") in CONFIG and CONFIG[bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪℜ")]:
        bstack11l1l1l1ll_opy_(bstack1ll1ll1ll1_opy_, bstack1l1l11l1_opy_)
    if bstack11ll1l1ll1_opy_.bstack111llll11_opy_(CONFIG, bstack111l111l_opy_) and bstack11ll1l1ll1_opy_.bstack11l1ll1l1l_opy_(bstack1ll1ll1ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1llll11_opy_):
            bstack11ll1l1ll1_opy_.set_capabilities(bstack1ll1ll1ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1lllll1l_opy_ = bstack1l11ll1ll_opy_(desired_capabilities)
        bstack1l1lllll1l_opy_[bstack1l11lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧℝ")] = bstack11l1lll1_opy_(CONFIG)
        bstack11lll1ll1l_opy_ = bstack11ll1ll11l_opy_(bstack1l1lllll1l_opy_)
        if bstack11lll1ll1l_opy_:
            bstack1ll1ll1ll1_opy_ = update(bstack11lll1ll1l_opy_, bstack1ll1ll1ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1lll11ll1_opy_(options, bstack1ll1ll1ll1_opy_)
    if not options:
        options = bstack1ll1ll1l1_opy_(bstack1ll1ll1ll1_opy_)
    if proxy and bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ℞")):
        options.proxy(proxy)
    if options and bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ℟")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l11lllll_opy_() < version.parse(bstack1l11lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ℠")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1ll1ll1_opy_)
    logger.info(bstack11lllll11l_opy_)
    bstack1l111lll_opy_.end(EVENTS.bstack1llll11l1_opy_.value, EVENTS.bstack1llll11l1_opy_.value + bstack1l11lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ℡"),
                               EVENTS.bstack1llll11l1_opy_.value + bstack1l11lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ™"), True, None)
    if bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭℣")):
        bstack111l11ll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ℤ")):
        bstack111l11ll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1l1l1l1l1l_opy_=bstack1l1l1l1l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ℥")):
        bstack111l11ll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1l1l1l1l_opy_=bstack1l1l1l1l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack111l11ll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1l1l1l1l1l_opy_=bstack1l1l1l1l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11l11llll_opy_ = bstack1l11lll_opy_ (u"ࠩࠪΩ")
        if bstack11l11lllll_opy_() >= version.parse(bstack1l11lll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ℧")):
            bstack11l11llll_opy_ = self.caps.get(bstack1l11lll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦℨ"))
        else:
            bstack11l11llll_opy_ = self.capabilities.get(bstack1l11lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ℩"))
        if bstack11l11llll_opy_:
            bstack1l1111l11_opy_(bstack11l11llll_opy_)
            if bstack11l11lllll_opy_() <= version.parse(bstack1l11lll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭K")):
                self.command_executor._url = bstack1l11lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣÅ") + bstack1l1llll1l_opy_ + bstack1l11lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧℬ")
            else:
                self.command_executor._url = bstack1l11lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦℭ") + bstack11l11llll_opy_ + bstack1l11lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ℮")
            logger.debug(bstack1l11ll11_opy_.format(bstack11l11llll_opy_))
        else:
            logger.debug(bstack1lllllll11_opy_.format(bstack1l11lll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧℯ")))
    except Exception as e:
        logger.debug(bstack1lllllll11_opy_.format(e))
    bstack1l1111111l_opy_ = self.session_id
    if bstack1l11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬℰ") in bstack1ll1111ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪℱ"), None)
        if item:
            bstack1111l111l1l_opy_ = getattr(item, bstack1l11lll_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬℲ"), False)
            if not getattr(item, bstack1l11lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩℳ"), None) and bstack1111l111l1l_opy_:
                setattr(store[bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ℴ")], bstack1l11lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫℵ"), self)
        bstack1l1lll1l1l_opy_ = getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬℶ"), None)
        if bstack1l1lll1l1l_opy_ and bstack1l1lll1l1l_opy_.get(bstack1l11lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬℷ"), bstack1l11lll_opy_ (u"࠭ࠧℸ")) == bstack1l11lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨℹ"):
            bstack111ll1ll1_opy_.bstack1ll1l1l1l_opy_(self)
    bstack1l11l1111l_opy_.append(self)
    if bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ℺") in CONFIG and bstack1l11lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ℻") in CONFIG[bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ℼ")][bstack111l111l_opy_]:
        bstack1lll111l_opy_ = CONFIG[bstack1l11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧℽ")][bstack111l111l_opy_][bstack1l11lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪℾ")]
    logger.debug(bstack1ll111lll1_opy_.format(bstack1l1111111l_opy_))
@measure(event_name=EVENTS.bstack1l1l11ll1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_, bstack11lll1llll_opy_=bstack1lll111l_opy_)
def bstack11ll1ll1_opy_(self, url):
    global bstack111l1ll1_opy_
    global CONFIG
    try:
        bstack11ll111l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1lll1111_opy_.format(str(err)))
    try:
        bstack111l1ll1_opy_(self, url)
    except Exception as e:
        try:
            bstack11l1ll111l_opy_ = str(e)
            if any(err_msg in bstack11l1ll111l_opy_ for err_msg in bstack1ll1l1ll1l_opy_):
                bstack11ll111l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1lll1111_opy_.format(str(err)))
        raise e
def bstack111111l11_opy_(item, when):
    global bstack11lllll1_opy_
    try:
        bstack11lllll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1ll1111l_opy_(item, call, rep):
    global bstack1l11ll11l_opy_
    global bstack1l11l1111l_opy_
    name = bstack1l11lll_opy_ (u"࠭ࠧℿ")
    try:
        if rep.when == bstack1l11lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⅀"):
            bstack1l1111111l_opy_ = threading.current_thread().bstackSessionId
            bstack1111l111ll1_opy_ = item.config.getoption(bstack1l11lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⅁"))
            try:
                if (str(bstack1111l111ll1_opy_).lower() != bstack1l11lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⅂")):
                    name = str(rep.nodeid)
                    bstack1ll1lll1l_opy_ = bstack11ll11l111_opy_(bstack1l11lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⅃"), name, bstack1l11lll_opy_ (u"ࠫࠬ⅄"), bstack1l11lll_opy_ (u"ࠬ࠭ⅅ"), bstack1l11lll_opy_ (u"࠭ࠧⅆ"), bstack1l11lll_opy_ (u"ࠧࠨⅇ"))
                    os.environ[bstack1l11lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫⅈ")] = name
                    for driver in bstack1l11l1111l_opy_:
                        if bstack1l1111111l_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1lll1l_opy_)
            except Exception as e:
                logger.debug(bstack1l11lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩⅉ").format(str(e)))
            try:
                bstack1ll1l111l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l11lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⅊"):
                    status = bstack1l11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⅋") if rep.outcome.lower() == bstack1l11lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⅌") else bstack1l11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⅍")
                    reason = bstack1l11lll_opy_ (u"ࠧࠨⅎ")
                    if status == bstack1l11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⅏"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l11lll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ⅐") if status == bstack1l11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⅑") else bstack1l11lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⅒")
                    data = name + bstack1l11lll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ⅓") if status == bstack1l11lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⅔") else name + bstack1l11lll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ⅕") + reason
                    bstack1111l11l1_opy_ = bstack11ll11l111_opy_(bstack1l11lll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⅖"), bstack1l11lll_opy_ (u"ࠩࠪ⅗"), bstack1l11lll_opy_ (u"ࠪࠫ⅘"), bstack1l11lll_opy_ (u"ࠫࠬ⅙"), level, data)
                    for driver in bstack1l11l1111l_opy_:
                        if bstack1l1111111l_opy_ == driver.session_id:
                            driver.execute_script(bstack1111l11l1_opy_)
            except Exception as e:
                logger.debug(bstack1l11lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⅚").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ⅛").format(str(e)))
    bstack1l11ll11l_opy_(item, call, rep)
notset = Notset()
def bstack1lllll1ll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1l1l1l1_opy_
    if str(name).lower() == bstack1l11lll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧ⅜"):
        return bstack1l11lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ⅝")
    else:
        return bstack1l1l1l1l1_opy_(self, name, default, skip)
def bstack1l1l1l111_opy_(self):
    global CONFIG
    global bstack1llll1l1ll_opy_
    try:
        proxy = bstack1lll1ll111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l11lll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⅞")):
                proxies = bstack11ll1l1111_opy_(proxy, bstack1ll1llll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1lll111_opy_ = proxies.popitem()
                    if bstack1l11lll_opy_ (u"ࠥ࠾࠴࠵ࠢ⅟") in bstack1ll1lll111_opy_:
                        return bstack1ll1lll111_opy_
                    else:
                        return bstack1l11lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧⅠ") + bstack1ll1lll111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤⅡ").format(str(e)))
    return bstack1llll1l1ll_opy_(self)
def bstack1ll11ll1l_opy_():
    return (bstack1l11lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩⅢ") in CONFIG or bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫⅣ") in CONFIG) and bstack111l11l1_opy_() and bstack11l11lllll_opy_() >= version.parse(
        bstack11l1lll11l_opy_)
def bstack11l11111_opy_(self,
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
    global bstack1lll111l_opy_
    global bstack1ll11ll1_opy_
    global bstack1ll1111ll_opy_
    CONFIG[bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪⅤ")] = str(bstack1ll1111ll_opy_) + str(__version__)
    bstack111l111l_opy_ = 0
    try:
        if bstack1ll11ll1_opy_ is True:
            bstack111l111l_opy_ = int(os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩⅥ")))
    except:
        bstack111l111l_opy_ = 0
    CONFIG[bstack1l11lll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤⅦ")] = True
    bstack1ll1ll1ll1_opy_ = bstack11ll1ll11l_opy_(CONFIG, bstack111l111l_opy_)
    logger.debug(bstack1ll111111l_opy_.format(str(bstack1ll1ll1ll1_opy_)))
    if CONFIG.get(bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨⅧ")):
        bstack11l1l1l1ll_opy_(bstack1ll1ll1ll1_opy_, bstack1l1l11l1_opy_)
    if bstack1l11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨⅨ") in CONFIG and bstack1l11lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫⅩ") in CONFIG[bstack1l11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅪ")][bstack111l111l_opy_]:
        bstack1lll111l_opy_ = CONFIG[bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫⅫ")][bstack111l111l_opy_][bstack1l11lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅬ")]
    import urllib
    import json
    if bstack1l11lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧⅭ") in CONFIG and str(CONFIG[bstack1l11lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨⅮ")]).lower() != bstack1l11lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫⅯ"):
        bstack1lll11l1ll_opy_ = bstack1l1lll111_opy_()
        bstack111l1111_opy_ = bstack1lll11l1ll_opy_ + urllib.parse.quote(json.dumps(bstack1ll1ll1ll1_opy_))
    else:
        bstack111l1111_opy_ = bstack1l11lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨⅰ") + urllib.parse.quote(json.dumps(bstack1ll1ll1ll1_opy_))
    browser = self.connect(bstack111l1111_opy_)
    return browser
def bstack1ll11111_opy_():
    global bstack11ll11l11l_opy_
    global bstack1ll1111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l1llllll_opy_
        if not bstack1l1ll1lllll_opy_():
            global bstack11l11ll111_opy_
            if not bstack11l11ll111_opy_:
                from bstack_utils.helper import bstack11l1l111l1_opy_, bstack11ll11ll11_opy_
                bstack11l11ll111_opy_ = bstack11l1l111l1_opy_()
                bstack11ll11ll11_opy_(bstack1ll1111ll_opy_)
            BrowserType.connect = bstack11l1llllll_opy_
            return
        BrowserType.launch = bstack11l11111_opy_
        bstack11ll11l11l_opy_ = True
    except Exception as e:
        pass
def bstack1111l1111ll_opy_():
    global CONFIG
    global bstack1ll1l11111_opy_
    global bstack1l1llll1l_opy_
    global bstack1l1l11l1_opy_
    global bstack1ll11ll1_opy_
    global bstack11l1l1lll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ⅱ")))
    bstack1ll1l11111_opy_ = eval(os.environ.get(bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩⅲ")))
    bstack1l1llll1l_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩⅳ"))
    bstack11l11ll1_opy_(CONFIG, bstack1ll1l11111_opy_)
    bstack11l1l1lll1_opy_ = bstack11111llll_opy_.bstack1l1ll1ll1_opy_(CONFIG, bstack11l1l1lll1_opy_)
    if cli.bstack1l1l1ll11_opy_():
        bstack1ll1lllll1_opy_.invoke(bstack1ll11l11l_opy_.CONNECT, bstack1ll1l111_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪⅴ"), bstack1l11lll_opy_ (u"ࠫ࠵࠭ⅵ")))
        cli.bstack1llll1l1lll_opy_(cli_context.platform_index)
        cli.bstack1lll1ll1ll1_opy_(bstack1ll1llll_opy_(bstack1l1llll1l_opy_, CONFIG), cli_context.platform_index, bstack1ll1ll1l1_opy_)
        cli.bstack1lll11l1lll_opy_()
        logger.debug(bstack1l11lll_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦⅶ") + str(cli_context.platform_index) + bstack1l11lll_opy_ (u"ࠨࠢⅷ"))
        return # skip all existing bstack1111l111111_opy_
    global bstack111l11ll1_opy_
    global bstack11ll1llll1_opy_
    global bstack11l1ll11ll_opy_
    global bstack1l111ll11_opy_
    global bstack11l11l11_opy_
    global bstack1l11l1lll_opy_
    global bstack1l1ll1l1l_opy_
    global bstack111l1ll1_opy_
    global bstack1llll1l1ll_opy_
    global bstack1l1l1l1l1_opy_
    global bstack11lllll1_opy_
    global bstack1l11ll11l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111l11ll1_opy_ = webdriver.Remote.__init__
        bstack11ll1llll1_opy_ = WebDriver.quit
        bstack1l1ll1l1l_opy_ = WebDriver.close
        bstack111l1ll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l11lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪⅸ") in CONFIG or bstack1l11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬⅹ") in CONFIG) and bstack111l11l1_opy_():
        if bstack11l11lllll_opy_() < version.parse(bstack11l1lll11l_opy_):
            logger.error(bstack1ll1lll1_opy_.format(bstack11l11lllll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1llll1l1ll_opy_ = RemoteConnection._11l11l1ll_opy_
            except Exception as e:
                logger.error(bstack111ll1lll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1l1l1l1_opy_ = Config.getoption
        from _pytest import runner
        bstack11lllll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l1lll1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l11ll11l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪⅺ"))
    bstack1l1l11l1_opy_ = CONFIG.get(bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧⅻ"), {}).get(bstack1l11lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ⅼ"))
    bstack1ll11ll1_opy_ = True
    bstack1l111l11_opy_(bstack1111l1ll1_opy_)
if (bstack11l1ll1l1l1_opy_()):
    bstack1111l1111ll_opy_()
@bstack111l1ll1ll_opy_(class_method=False)
def bstack11111ll1l11_opy_(hook_name, event, bstack1l11l1l1l1l_opy_=None):
    if hook_name not in [bstack1l11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ⅽ"), bstack1l11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪⅾ"), bstack1l11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ⅿ"), bstack1l11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪↀ"), bstack1l11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧↁ"), bstack1l11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫↂ"), bstack1l11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪↃ"), bstack1l11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧↄ")]:
        return
    node = store[bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪↅ")]
    if hook_name in [bstack1l11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ↆ"), bstack1l11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪↇ")]:
        node = store[bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨↈ")]
    elif hook_name in [bstack1l11lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ↉"), bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ↊")]:
        node = store[bstack1l11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ↋")]
    hook_type = bstack111l1l111l1_opy_(hook_name)
    if event == bstack1l11lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭↌"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_[hook_type], bstack1lll1l1l11l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111lll1l1l_opy_ = {
            bstack1l11lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↍"): uuid,
            bstack1l11lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ↎"): bstack11lll111l1_opy_(),
            bstack1l11lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ↏"): bstack1l11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ←"),
            bstack1l11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ↑"): hook_type,
            bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ→"): hook_name
        }
        store[bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ↓")].append(uuid)
        bstack1111l111lll_opy_ = node.nodeid
        if hook_type == bstack1l11lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ↔"):
            if not _111l1ll11l_opy_.get(bstack1111l111lll_opy_, None):
                _111l1ll11l_opy_[bstack1111l111lll_opy_] = {bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ↕"): []}
            _111l1ll11l_opy_[bstack1111l111lll_opy_][bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ↖")].append(bstack111lll1l1l_opy_[bstack1l11lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ↗")])
        _111l1ll11l_opy_[bstack1111l111lll_opy_ + bstack1l11lll_opy_ (u"ࠫ࠲࠭↘") + hook_name] = bstack111lll1l1l_opy_
        bstack11111ll111l_opy_(node, bstack111lll1l1l_opy_, bstack1l11lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭↙"))
    elif event == bstack1l11lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ↚"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1111ll_opy_[hook_type], bstack1lll1l1l11l_opy_.POST, node, None, bstack1l11l1l1l1l_opy_)
            return
        bstack11l11111l1_opy_ = node.nodeid + bstack1l11lll_opy_ (u"ࠧ࠮ࠩ↛") + hook_name
        _111l1ll11l_opy_[bstack11l11111l1_opy_][bstack1l11lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭↜")] = bstack11lll111l1_opy_()
        bstack11111lll1ll_opy_(_111l1ll11l_opy_[bstack11l11111l1_opy_][bstack1l11lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ↝")])
        bstack11111ll111l_opy_(node, _111l1ll11l_opy_[bstack11l11111l1_opy_], bstack1l11lll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ↞"), bstack11111lll111_opy_=bstack1l11l1l1l1l_opy_)
def bstack1111l11111l_opy_():
    global bstack11111l1llll_opy_
    if bstack11llllll1l_opy_():
        bstack11111l1llll_opy_ = bstack1l11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ↟")
    else:
        bstack11111l1llll_opy_ = bstack1l11lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ↠")
@bstack111ll1ll1_opy_.bstack1111ll11l11_opy_
def bstack11111l1ll1l_opy_():
    bstack1111l11111l_opy_()
    if cli.is_running():
        try:
            bstack11l11l1lll1_opy_(bstack11111ll1l11_opy_)
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ↡").format(e))
        return
    if bstack111l11l1_opy_():
        bstack11lll1l1ll_opy_ = Config.bstack1lll1l1lll_opy_()
        bstack1l11lll_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡀࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡭ࡥࡵࡵࠣࡹࡸ࡫ࡤࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠲ࡽࡲࡢࡲࡳ࡭ࡳ࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡸࠥ࡯ࡳࠡࡲࡤࡸࡨ࡮ࡥࡥࠢ࡬ࡲࠥࡧࠠࡥ࡫ࡩࡪࡪࡸࡥ࡯ࡶࠣࡴࡷࡵࡣࡦࡵࡶࠤ࡮ࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡶࡵࠣࡻࡪࠦ࡮ࡦࡧࡧࠤࡹࡵࠠࡶࡵࡨࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡖࡡࡵࡥ࡫ࠬࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡨࡢࡰࡧࡰࡪࡸࠩࠡࡨࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࠩࠪ↢")
        if bstack11lll1l1ll_opy_.get_property(bstack1l11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ↣")):
            if CONFIG.get(bstack1l11lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ↤")) is not None and int(CONFIG[bstack1l11lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ↥")]) > 1:
                bstack11llll11_opy_(bstack1lll111ll_opy_)
            return
        bstack11llll11_opy_(bstack1lll111ll_opy_)
    try:
        bstack11l11l1lll1_opy_(bstack11111ll1l11_opy_)
    except Exception as e:
        logger.debug(bstack1l11lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ↦").format(e))
bstack11111l1ll1l_opy_()