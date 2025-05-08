# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1ll11111l1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11l111l_opy_, bstack1l1l1lllll_opy_, update, bstack1l1l111l1l_opy_,
                                       bstack11ll1l11ll_opy_, bstack11ll11ll1l_opy_, bstack1l1l1llll_opy_, bstack1l1l1ll111_opy_,
                                       bstack1ll1ll1ll_opy_, bstack11ll1ll11_opy_, bstack1l11llll1_opy_, bstack1ll1lll1_opy_,
                                       bstack11l1l1ll11_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111l1l1l_opy_)
from browserstack_sdk.bstack11l1lll1l_opy_ import bstack1ll11l1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1l111l1_opy_
from bstack_utils.capture import bstack11l11111l1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1lll1l11l_opy_, bstack1l11l1llll_opy_, bstack1l1l1l11l1_opy_, \
    bstack1l11l11l_opy_
from bstack_utils.helper import bstack1l111l11_opy_, bstack11l1ll1llll_opy_, bstack111l1lll1l_opy_, bstack1ll1l1l11_opy_, bstack1ll1111lll1_opy_, bstack1l1ll1ll_opy_, \
    bstack11l1llllll1_opy_, \
    bstack11l1lll11ll_opy_, bstack11l1ll1l11_opy_, bstack1l1ll1llll_opy_, bstack11l1l11ll1l_opy_, bstack111lllll1_opy_, Notset, \
    bstack1llll1l1l_opy_, bstack11l1l1ll111_opy_, bstack11l1l11l1ll_opy_, Result, bstack11l1ll1ll1l_opy_, bstack11l1llll1l1_opy_, bstack111ll1ll1l_opy_, \
    bstack11llllllll_opy_, bstack11lllll11_opy_, bstack11l11llll1_opy_, bstack11l1ll111l1_opy_
from bstack_utils.bstack11l11l1lll1_opy_ import bstack11l11l1l1l1_opy_
from bstack_utils.messages import bstack1lllll1l1l_opy_, bstack1l1111111l_opy_, bstack1lll11l11_opy_, bstack111l1lll1_opy_, bstack11ll111ll_opy_, \
    bstack11111l1l1_opy_, bstack11l11ll11_opy_, bstack1l11ll1l1_opy_, bstack1l1l1lll11_opy_, bstack1l1ll1l1l_opy_, \
    bstack1ll1l111_opy_, bstack1l1ll111l_opy_
from bstack_utils.proxy import bstack1ll11lll_opy_, bstack11llllll_opy_
from bstack_utils.bstack1l11lll1l1_opy_ import bstack111l1l1l1l1_opy_, bstack111l1l1l1ll_opy_, bstack111l1l1l11l_opy_, bstack111l1l111l1_opy_, \
    bstack111l1l11111_opy_, bstack111l1l11l11_opy_, bstack111l1l11lll_opy_, bstack11l1111ll_opy_, bstack111l1l1111l_opy_
from bstack_utils.bstack11l11111_opy_ import bstack11l1lll1ll_opy_
from bstack_utils.bstack11ll1lll1l_opy_ import bstack11ll11lll1_opy_, bstack1l111ll1l_opy_, bstack1ll1llll1l_opy_, \
    bstack1ll111lll1_opy_, bstack1lll1ll11l_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack111llll11l_opy_
from bstack_utils.bstack11l111l111_opy_ import bstack1l11ll11ll_opy_
import bstack_utils.accessibility as bstack1l1l1l11l_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack111ll11l_opy_
from bstack_utils.bstack11ll11ll11_opy_ import bstack11ll11ll11_opy_
from browserstack_sdk.__init__ import bstack11ll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack1lll1ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack111ll1l1l_opy_ import bstack111ll1l1l_opy_, bstack1lllll1ll1_opy_, bstack11111lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1l1ll1_opy_, bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111ll1l1l_opy_ import bstack111ll1l1l_opy_, bstack1lllll1ll1_opy_, bstack11111lll1_opy_
bstack11lll1111_opy_ = None
bstack111ll11l1_opy_ = None
bstack11l1ll11l_opy_ = None
bstack11ll1llll_opy_ = None
bstack1l1111l11_opy_ = None
bstack1l1111l111_opy_ = None
bstack11111ll11_opy_ = None
bstack1l1l11llll_opy_ = None
bstack1111ll11_opy_ = None
bstack1llll111_opy_ = None
bstack11l1llll_opy_ = None
bstack1l11ll1lll_opy_ = None
bstack11l11ll111_opy_ = None
bstack11l11l1l_opy_ = bstack1l1lll_opy_ (u"ࠨࠩὬ")
CONFIG = {}
bstack11ll111l_opy_ = False
bstack1111l111_opy_ = bstack1l1lll_opy_ (u"ࠩࠪὭ")
bstack1ll1l11111_opy_ = bstack1l1lll_opy_ (u"ࠪࠫὮ")
bstack1ll111l11l_opy_ = False
bstack1l11lll1l_opy_ = []
bstack1ll1111l11_opy_ = bstack1lll1l11l_opy_
bstack11111lll11l_opy_ = bstack1l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫὯ")
bstack1l11l1111l_opy_ = {}
bstack11l1l1lll1_opy_ = None
bstack1ll111ll_opy_ = False
logger = bstack1ll1l111l1_opy_.get_logger(__name__, bstack1ll1111l11_opy_)
store = {
    bstack1l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩὰ"): []
}
bstack1111l11l111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111ll1l1l1_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l1l1ll1_opy_(
    test_framework_name=bstack1lll1lll11_opy_[bstack1l1lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪά")] if bstack111lllll1_opy_() else bstack1lll1lll11_opy_[bstack1l1lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧὲ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack111l1l1l1_opy_(page, bstack1l111l11ll_opy_):
    try:
        page.evaluate(bstack1l1lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤέ"),
                      bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ὴ") + json.dumps(
                          bstack1l111l11ll_opy_) + bstack1l1lll_opy_ (u"ࠥࢁࢂࠨή"))
    except Exception as e:
        print(bstack1l1lll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤὶ"), e)
def bstack11lll1ll1_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨί"), bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫὸ") + json.dumps(
            message) + bstack1l1lll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪό") + json.dumps(level) + bstack1l1lll_opy_ (u"ࠨࡿࢀࠫὺ"))
    except Exception as e:
        print(bstack1l1lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧύ"), e)
def pytest_configure(config):
    global bstack1111l111_opy_
    global CONFIG
    bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
    config.args = bstack1l11ll11ll_opy_.bstack1111l11l1ll_opy_(config.args)
    bstack11l1l1l1l_opy_.bstack1ll11l111l_opy_(bstack11l11llll1_opy_(config.getoption(bstack1l1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧὼ"))))
    try:
        bstack1ll1l111l1_opy_.bstack11l111l1ll1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111ll1l1l_opy_.invoke(bstack1lllll1ll1_opy_.CONNECT, bstack11111lll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫώ"), bstack1l1lll_opy_ (u"ࠬ࠶ࠧ὾")))
        config = json.loads(os.environ.get(bstack1l1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ὿"), bstack1l1lll_opy_ (u"ࠢࡼࡿࠥᾀ")))
        cli.bstack1llll11l1l1_opy_(bstack1l1ll1llll_opy_(bstack1111l111_opy_, CONFIG), cli_context.platform_index, bstack1l1l111l1l_opy_)
    if cli.bstack1lll1ll111l_opy_(bstack1lll1ll11l1_opy_):
        cli.bstack1lll1l111ll_opy_()
        logger.debug(bstack1l1lll_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢᾁ") + str(cli_context.platform_index) + bstack1l1lll_opy_ (u"ࠤࠥᾂ"))
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.BEFORE_ALL, bstack1llll1lll1l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1lll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᾃ"), None)
    if cli.is_running() and when == bstack1l1lll_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᾄ"):
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.LOG_REPORT, bstack1llll1lll1l_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1l1lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᾅ"):
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.POST, item, call, outcome)
        elif when == bstack1l1lll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᾆ"):
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.LOG_REPORT, bstack1llll1lll1l_opy_.POST, item, call, outcome)
        elif when == bstack1l1lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᾇ"):
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.AFTER_EACH, bstack1llll1lll1l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111l111ll1_opy_
    bstack1111l11l11l_opy_ = item.config.getoption(bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᾈ"))
    plugins = item.config.getoption(bstack1l1lll_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥᾉ"))
    report = outcome.get_result()
    bstack1111l111l1l_opy_(item, call, report)
    if bstack1l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣᾊ") not in plugins or bstack111lllll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1lll_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧᾋ"), None)
    page = getattr(item, bstack1l1lll_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦᾌ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11111ll11ll_opy_(item, report, summary, bstack1111l11l11l_opy_)
    if (page is not None):
        bstack11111ll111l_opy_(item, report, summary, bstack1111l11l11l_opy_)
def bstack11111ll11ll_opy_(item, report, summary, bstack1111l11l11l_opy_):
    if report.when == bstack1l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᾍ") and report.skipped:
        bstack111l1l1111l_opy_(report)
    if report.when in [bstack1l1lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᾎ"), bstack1l1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᾏ")]:
        return
    if not bstack1ll1111lll1_opy_():
        return
    try:
        if (str(bstack1111l11l11l_opy_).lower() != bstack1l1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᾐ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨᾑ") + json.dumps(
                    report.nodeid) + bstack1l1lll_opy_ (u"ࠫࢂࢃࠧᾒ"))
        os.environ[bstack1l1lll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᾓ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨᾔ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1lll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᾕ")))
    bstack1lllllll1l_opy_ = bstack1l1lll_opy_ (u"ࠣࠤᾖ")
    bstack111l1l1111l_opy_(report)
    if not passed:
        try:
            bstack1lllllll1l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1lll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᾗ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllllll1l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1lll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᾘ")))
        bstack1lllllll1l_opy_ = bstack1l1lll_opy_ (u"ࠦࠧᾙ")
        if not passed:
            try:
                bstack1lllllll1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1lll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᾚ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllllll1l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᾛ")
                    + json.dumps(bstack1l1lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᾜ"))
                    + bstack1l1lll_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᾝ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᾞ")
                    + json.dumps(str(bstack1lllllll1l_opy_))
                    + bstack1l1lll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᾟ")
                )
        except Exception as e:
            summary.append(bstack1l1lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᾠ").format(e))
def bstack11111llll1l_opy_(test_name, error_message):
    try:
        bstack11111lll1l1_opy_ = []
        bstack11l11l1l1l_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᾡ"), bstack1l1lll_opy_ (u"࠭࠰ࠨᾢ"))
        bstack11llll1ll1_opy_ = {bstack1l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᾣ"): test_name, bstack1l1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᾤ"): error_message, bstack1l1lll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᾥ"): bstack11l11l1l1l_opy_}
        bstack1111l111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᾦ"))
        if os.path.exists(bstack1111l111111_opy_):
            with open(bstack1111l111111_opy_) as f:
                bstack11111lll1l1_opy_ = json.load(f)
        bstack11111lll1l1_opy_.append(bstack11llll1ll1_opy_)
        with open(bstack1111l111111_opy_, bstack1l1lll_opy_ (u"ࠫࡼ࠭ᾧ")) as f:
            json.dump(bstack11111lll1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᾨ") + str(e))
def bstack11111ll111l_opy_(item, report, summary, bstack1111l11l11l_opy_):
    if report.when in [bstack1l1lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᾩ"), bstack1l1lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᾪ")]:
        return
    if (str(bstack1111l11l11l_opy_).lower() != bstack1l1lll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᾫ")):
        bstack111l1l1l1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1lll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᾬ")))
    bstack1lllllll1l_opy_ = bstack1l1lll_opy_ (u"ࠥࠦᾭ")
    bstack111l1l1111l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lllllll1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1lll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᾮ").format(e)
                )
        try:
            if passed:
                bstack1lll1ll11l_opy_(getattr(item, bstack1l1lll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᾯ"), None), bstack1l1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᾰ"))
            else:
                error_message = bstack1l1lll_opy_ (u"ࠧࠨᾱ")
                if bstack1lllllll1l_opy_:
                    bstack11lll1ll1_opy_(item._page, str(bstack1lllllll1l_opy_), bstack1l1lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᾲ"))
                    bstack1lll1ll11l_opy_(getattr(item, bstack1l1lll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᾳ"), None), bstack1l1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᾴ"), str(bstack1lllllll1l_opy_))
                    error_message = str(bstack1lllllll1l_opy_)
                else:
                    bstack1lll1ll11l_opy_(getattr(item, bstack1l1lll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ᾵"), None), bstack1l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᾶ"))
                bstack11111llll1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᾷ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1lll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᾸ"), default=bstack1l1lll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᾹ"), help=bstack1l1lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᾺ"))
    parser.addoption(bstack1l1lll_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤΆ"), default=bstack1l1lll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᾼ"), help=bstack1l1lll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ᾽"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1lll_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣι"), action=bstack1l1lll_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨ᾿"), default=bstack1l1lll_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣ῀"),
                         help=bstack1l1lll_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣ῁"))
def bstack111lllll1l_opy_(log):
    if not (log[bstack1l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫῂ")] and log[bstack1l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬῃ")].strip()):
        return
    active = bstack111lllll11_opy_()
    log = {
        bstack1l1lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫῄ"): log[bstack1l1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ῅")],
        bstack1l1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪῆ"): bstack111l1lll1l_opy_().isoformat() + bstack1l1lll_opy_ (u"ࠨ࡜ࠪῇ"),
        bstack1l1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪῈ"): log[bstack1l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫΈ")],
    }
    if active:
        if active[bstack1l1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩῊ")] == bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪΉ"):
            log[bstack1l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ῌ")] = active[bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ῍")]
        elif active[bstack1l1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭῎")] == bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺࠧ῏"):
            log[bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῐ")] = active[bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫῑ")]
    bstack111ll11l_opy_.bstack11lll11111_opy_([log])
def bstack111lllll11_opy_():
    if len(store[bstack1l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩῒ")]) > 0 and store[bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪΐ")][-1]:
        return {
            bstack1l1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ῔"): bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭῕"),
            bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩῖ"): store[bstack1l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧῗ")][-1]
        }
    if store.get(bstack1l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨῘ"), None):
        return {
            bstack1l1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪῙ"): bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࠫῚ"),
            bstack1l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧΊ"): store[bstack1l1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ῜")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.INIT_TEST, bstack1llll1lll1l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.INIT_TEST, bstack1llll1lll1l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1111l1111l1_opy_ = True
        bstack1111l1l1l_opy_ = bstack1l1l1l11l_opy_.bstack1ll1llll11_opy_(bstack11l1lll11ll_opy_(item.own_markers))
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1ll11l1_opy_):
            item._a11y_test_case = bstack1111l1l1l_opy_
            if bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ῝"), None):
                driver = getattr(item, bstack1l1lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ῞"), None)
                item._a11y_started = bstack1l1l1l11l_opy_.bstack1l1l11111l_opy_(driver, bstack1111l1l1l_opy_)
        if not bstack111ll11l_opy_.on() or bstack11111lll11l_opy_ != bstack1l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ῟"):
            return
        global current_test_uuid #, bstack11l111l11l_opy_
        bstack111l11lll1_opy_ = {
            bstack1l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪῠ"): uuid4().__str__(),
            bstack1l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪῡ"): bstack111l1lll1l_opy_().isoformat() + bstack1l1lll_opy_ (u"࡛ࠧࠩῢ")
        }
        current_test_uuid = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ΰ")]
        store[bstack1l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ῤ")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῥ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111ll1l1l1_opy_[item.nodeid] = {**_111ll1l1l1_opy_[item.nodeid], **bstack111l11lll1_opy_}
        bstack1111l11111l_opy_(item, _111ll1l1l1_opy_[item.nodeid], bstack1l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬῦ"))
    except Exception as err:
        print(bstack1l1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧῧ"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪῨ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.BEFORE_EACH, bstack1llll1lll1l_opy_.PRE, item, bstack1l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ῡ"))
        return # skip all existing bstack1111l111ll1_opy_
    global bstack1111l11l111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1l11ll1l_opy_():
        atexit.register(bstack1l1l11l11l_opy_)
        if not bstack1111l11l111_opy_:
            try:
                bstack1111l111l11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1ll111l1_opy_():
                    bstack1111l111l11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1111l111l11_opy_:
                    signal.signal(s, bstack1111l111lll_opy_)
                bstack1111l11l111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤῪ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l1l1l1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩΎ")
    try:
        if not bstack111ll11l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l11lll1_opy_ = {
            bstack1l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῬ"): uuid,
            bstack1l1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ῭"): bstack111l1lll1l_opy_().isoformat() + bstack1l1lll_opy_ (u"ࠬࡠࠧ΅"),
            bstack1l1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ`"): bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ῰"),
            bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ῱"): bstack1l1lll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧῲ"),
            bstack1l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ῳ"): bstack1l1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪῴ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ῵")] = item
        store[bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪῶ")] = [uuid]
        if not _111ll1l1l1_opy_.get(item.nodeid, None):
            _111ll1l1l1_opy_[item.nodeid] = {bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ῷ"): [], bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪῸ"): []}
        _111ll1l1l1_opy_[item.nodeid][bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨΌ")].append(bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨῺ")])
        _111ll1l1l1_opy_[item.nodeid + bstack1l1lll_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫΏ")] = bstack111l11lll1_opy_
        bstack11111l1ll11_opy_(item, bstack111l11lll1_opy_, bstack1l1lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ῼ"))
    except Exception as err:
        print(bstack1l1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ´"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.AFTER_EACH, bstack1llll1lll1l_opy_.PRE, item, bstack1l1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ῾"))
        return # skip all existing bstack1111l111ll1_opy_
    try:
        global bstack1l11l1111l_opy_
        bstack11l11l1l1l_opy_ = 0
        if bstack1ll111l11l_opy_ is True:
            bstack11l11l1l1l_opy_ = int(os.environ.get(bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ῿")))
        if bstack11ll1lllll_opy_.bstack1llllllll_opy_() == bstack1l1lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ "):
            if bstack11ll1lllll_opy_.bstack1llll1ll1l_opy_() == bstack1l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ "):
                bstack11111llllll_opy_ = bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ "), None)
                bstack1ll1ll111l_opy_ = bstack11111llllll_opy_ + bstack1l1lll_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣ ")
                driver = getattr(item, bstack1l1lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ "), None)
                bstack1l111lll11_opy_ = getattr(item, bstack1l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ "), None)
                bstack1lll1l1l1_opy_ = getattr(item, bstack1l1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ "), None)
                PercySDK.screenshot(driver, bstack1ll1ll111l_opy_, bstack1l111lll11_opy_=bstack1l111lll11_opy_, bstack1lll1l1l1_opy_=bstack1lll1l1l1_opy_, bstack1l1lll111_opy_=bstack11l11l1l1l_opy_)
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1ll11l1_opy_):
            if getattr(item, bstack1l1lll_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩ "), False):
                bstack1ll11l1ll1_opy_.bstack111l111l_opy_(getattr(item, bstack1l1lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ "), None), bstack1l11l1111l_opy_, logger, item)
        if not bstack111ll11l_opy_.on():
            return
        bstack111l11lll1_opy_ = {
            bstack1l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ "): uuid4().__str__(),
            bstack1l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ "): bstack111l1lll1l_opy_().isoformat() + bstack1l1lll_opy_ (u"࡚࠭ࠨ​"),
            bstack1l1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ‌"): bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰ࠭‍"),
            bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ‎"): bstack1l1lll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ‏"),
            bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ‐"): bstack1l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ‑")
        }
        _111ll1l1l1_opy_[item.nodeid + bstack1l1lll_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ‒")] = bstack111l11lll1_opy_
        bstack11111l1ll11_opy_(item, bstack111l11lll1_opy_, bstack1l1lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ–"))
    except Exception as err:
        print(bstack1l1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧ—"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l111l1_opy_(fixturedef.argname):
        store[bstack1l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ―")] = request.node
    elif bstack111l1l11111_opy_(fixturedef.argname):
        store[bstack1l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ‖")] = request.node
    if not bstack111ll11l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l111ll1_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.SETUP_FIXTURE, bstack1llll1lll1l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l111ll1_opy_
    try:
        fixture = {
            bstack1l1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ‗"): fixturedef.argname,
            bstack1l1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ‘"): bstack11l1llllll1_opy_(outcome),
            bstack1l1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ’"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ‚")]
        if not _111ll1l1l1_opy_.get(current_test_item.nodeid, None):
            _111ll1l1l1_opy_[current_test_item.nodeid] = {bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ‛"): []}
        _111ll1l1l1_opy_[current_test_item.nodeid][bstack1l1lll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ“")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭”"), str(err))
if bstack111lllll1_opy_() and bstack111ll11l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.STEP, bstack1llll1lll1l_opy_.PRE, request, step)
            return
        try:
            _111ll1l1l1_opy_[request.node.nodeid][bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ„")].bstack11l1ll1ll_opy_(id(step))
        except Exception as err:
            print(bstack1l1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪ‟"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.STEP, bstack1llll1lll1l_opy_.POST, request, step, exception)
            return
        try:
            _111ll1l1l1_opy_[request.node.nodeid][bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ†")].bstack111llllll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ‡"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.STEP, bstack1llll1lll1l_opy_.POST, request, step)
            return
        try:
            bstack111lll1lll_opy_: bstack111llll11l_opy_ = _111ll1l1l1_opy_[request.node.nodeid][bstack1l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ•")]
            bstack111lll1lll_opy_.bstack111llllll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭‣"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111lll11l_opy_
        try:
            if not bstack111ll11l_opy_.on() or bstack11111lll11l_opy_ != bstack1l1lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ․"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ‥"), None)
            if not _111ll1l1l1_opy_.get(request.node.nodeid, None):
                _111ll1l1l1_opy_[request.node.nodeid] = {}
            bstack111lll1lll_opy_ = bstack111llll11l_opy_.bstack1111llll11l_opy_(
                scenario, feature, request.node,
                name=bstack111l1l11l11_opy_(request.node, scenario),
                started_at=bstack1l1ll1ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ…"),
                tags=bstack111l1l11lll_opy_(feature, scenario),
                bstack111llll1l1_opy_=bstack111ll11l_opy_.bstack11l111111l_opy_(driver) if driver and driver.session_id else {}
            )
            _111ll1l1l1_opy_[request.node.nodeid][bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ‧")] = bstack111lll1lll_opy_
            bstack11111lll111_opy_(bstack111lll1lll_opy_.uuid)
            bstack111ll11l_opy_.bstack11l1111ll1_opy_(bstack1l1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ "), bstack111lll1lll_opy_)
        except Exception as err:
            print(bstack1l1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪ "), str(err))
def bstack11111lllll1_opy_(bstack11l1111l11_opy_):
    if bstack11l1111l11_opy_ in store[bstack1l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭‪")]:
        store[bstack1l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ‫")].remove(bstack11l1111l11_opy_)
def bstack11111lll111_opy_(test_uuid):
    store[bstack1l1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ‬")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111ll11l_opy_.bstack1111l1lll11_opy_
def bstack1111l111l1l_opy_(item, call, report):
    logger.debug(bstack1l1lll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠧ‭"))
    global bstack11111lll11l_opy_
    bstack1l1l1111l1_opy_ = bstack1l1ll1ll_opy_()
    if hasattr(report, bstack1l1lll_opy_ (u"࠭ࡳࡵࡱࡳࠫ‮")):
        bstack1l1l1111l1_opy_ = bstack11l1ll1ll1l_opy_(report.stop)
    elif hasattr(report, bstack1l1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ ")):
        bstack1l1l1111l1_opy_ = bstack11l1ll1ll1l_opy_(report.start)
    try:
        if getattr(report, bstack1l1lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭‰"), bstack1l1lll_opy_ (u"ࠩࠪ‱")) == bstack1l1lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ′"):
            logger.debug(bstack1l1lll_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭″").format(getattr(report, bstack1l1lll_opy_ (u"ࠬࡽࡨࡦࡰࠪ‴"), bstack1l1lll_opy_ (u"࠭ࠧ‵")).__str__(), bstack11111lll11l_opy_))
            if bstack11111lll11l_opy_ == bstack1l1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ‶"):
                _111ll1l1l1_opy_[item.nodeid][bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭‷")] = bstack1l1l1111l1_opy_
                bstack1111l11111l_opy_(item, _111ll1l1l1_opy_[item.nodeid], bstack1l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ‸"), report, call)
                store[bstack1l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ‹")] = None
            elif bstack11111lll11l_opy_ == bstack1l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ›"):
                bstack111lll1lll_opy_ = _111ll1l1l1_opy_[item.nodeid][bstack1l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ※")]
                bstack111lll1lll_opy_.set(hooks=_111ll1l1l1_opy_[item.nodeid].get(bstack1l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ‼"), []))
                exception, bstack11l1111l1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l1111l1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1lll_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭‽"), bstack1l1lll_opy_ (u"ࠨࠩ‾"))]
                bstack111lll1lll_opy_.stop(time=bstack1l1l1111l1_opy_, result=Result(result=getattr(report, bstack1l1lll_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ‿"), bstack1l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⁀")), exception=exception, bstack11l1111l1l_opy_=bstack11l1111l1l_opy_))
                bstack111ll11l_opy_.bstack11l1111ll1_opy_(bstack1l1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⁁"), _111ll1l1l1_opy_[item.nodeid][bstack1l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⁂")])
        elif getattr(report, bstack1l1lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⁃"), bstack1l1lll_opy_ (u"ࠧࠨ⁄")) in [bstack1l1lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⁅"), bstack1l1lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⁆")]:
            logger.debug(bstack1l1lll_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⁇").format(getattr(report, bstack1l1lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁈"), bstack1l1lll_opy_ (u"ࠬ࠭⁉")).__str__(), bstack11111lll11l_opy_))
            bstack111llll1ll_opy_ = item.nodeid + bstack1l1lll_opy_ (u"࠭࠭ࠨ⁊") + getattr(report, bstack1l1lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⁋"), bstack1l1lll_opy_ (u"ࠨࠩ⁌"))
            if getattr(report, bstack1l1lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⁍"), False):
                hook_type = bstack1l1lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⁎") if getattr(report, bstack1l1lll_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⁏"), bstack1l1lll_opy_ (u"ࠬ࠭⁐")) == bstack1l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⁑") else bstack1l1lll_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ⁒")
                _111ll1l1l1_opy_[bstack111llll1ll_opy_] = {
                    bstack1l1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁓"): uuid4().__str__(),
                    bstack1l1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁔"): bstack1l1l1111l1_opy_,
                    bstack1l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⁕"): hook_type
                }
            _111ll1l1l1_opy_[bstack111llll1ll_opy_][bstack1l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⁖")] = bstack1l1l1111l1_opy_
            bstack11111lllll1_opy_(_111ll1l1l1_opy_[bstack111llll1ll_opy_][bstack1l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁗")])
            bstack11111l1ll11_opy_(item, _111ll1l1l1_opy_[bstack111llll1ll_opy_], bstack1l1lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⁘"), report, call)
            if getattr(report, bstack1l1lll_opy_ (u"ࠧࡸࡪࡨࡲࠬ⁙"), bstack1l1lll_opy_ (u"ࠨࠩ⁚")) == bstack1l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⁛"):
                if getattr(report, bstack1l1lll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⁜"), bstack1l1lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⁝")) == bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⁞"):
                    bstack111l11lll1_opy_ = {
                        bstack1l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ "): uuid4().__str__(),
                        bstack1l1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⁠"): bstack1l1ll1ll_opy_(),
                        bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⁡"): bstack1l1ll1ll_opy_()
                    }
                    _111ll1l1l1_opy_[item.nodeid] = {**_111ll1l1l1_opy_[item.nodeid], **bstack111l11lll1_opy_}
                    bstack1111l11111l_opy_(item, _111ll1l1l1_opy_[item.nodeid], bstack1l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⁢"))
                    bstack1111l11111l_opy_(item, _111ll1l1l1_opy_[item.nodeid], bstack1l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁣"), report, call)
    except Exception as err:
        print(bstack1l1lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ⁤"), str(err))
def bstack11111l1lll1_opy_(test, bstack111l11lll1_opy_, result=None, call=None, bstack11l1l1l1l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lll1lll_opy_ = {
        bstack1l1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁥"): bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⁦")],
        bstack1l1lll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⁧"): bstack1l1lll_opy_ (u"ࠨࡶࡨࡷࡹ࠭⁨"),
        bstack1l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⁩"): test.name,
        bstack1l1lll_opy_ (u"ࠪࡦࡴࡪࡹࠨ⁪"): {
            bstack1l1lll_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⁫"): bstack1l1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⁬"),
            bstack1l1lll_opy_ (u"࠭ࡣࡰࡦࡨࠫ⁭"): inspect.getsource(test.obj)
        },
        bstack1l1lll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⁮"): test.name,
        bstack1l1lll_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ⁯"): test.name,
        bstack1l1lll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ⁰"): bstack1l11ll11ll_opy_.bstack111lll111l_opy_(test),
        bstack1l1lll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ⁱ"): file_path,
        bstack1l1lll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭⁲"): file_path,
        bstack1l1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⁳"): bstack1l1lll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⁴"),
        bstack1l1lll_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ⁵"): file_path,
        bstack1l1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⁶"): bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁷")],
        bstack1l1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⁸"): bstack1l1lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⁹"),
        bstack1l1lll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨ⁺"): {
            bstack1l1lll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪ⁻"): test.nodeid
        },
        bstack1l1lll_opy_ (u"ࠧࡵࡣࡪࡷࠬ⁼"): bstack11l1lll11ll_opy_(test.own_markers)
    }
    if bstack11l1l1l1l1_opy_ in [bstack1l1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⁽"), bstack1l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁾")]:
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠪࡱࡪࡺࡡࠨⁿ")] = {
            bstack1l1lll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭₀"): bstack111l11lll1_opy_.get(bstack1l1lll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ₁"), [])
        }
    if bstack11l1l1l1l1_opy_ == bstack1l1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ₂"):
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₃")] = bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ₄")
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ₅")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ₆")]
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₇")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₈")]
    if result:
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭₉")] = result.outcome
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ₊")] = result.duration * 1000
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₋")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₌")]
        if result.failed:
            bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ₍")] = bstack111ll11l_opy_.bstack1111ll1111_opy_(call.excinfo.typename)
            bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ₎")] = bstack111ll11l_opy_.bstack1111ll1l11l_opy_(call.excinfo, result)
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ₏")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬₐ")]
    if outcome:
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧₑ")] = bstack11l1llllll1_opy_(outcome)
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩₒ")] = 0
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧₓ")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨₔ")]
        if bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫₕ")] == bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬₖ"):
            bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬₗ")] = bstack1l1lll_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨₘ")  # bstack11111ll1l1l_opy_
            bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩₙ")] = [{bstack1l1lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬₚ"): [bstack1l1lll_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧₛ")]}]
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪₜ")] = bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ₝")]
    return bstack111lll1lll_opy_
def bstack11111l1llll_opy_(test, bstack111l11l1ll_opy_, bstack11l1l1l1l1_opy_, result, call, outcome, bstack11111ll11l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ₞")]
    hook_name = bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ₟")]
    hook_data = {
        bstack1l1lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭₠"): bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ₡")],
        bstack1l1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ₢"): bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ₣"),
        bstack1l1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₤"): bstack1l1lll_opy_ (u"࠭ࡻࡾࠩ₥").format(bstack111l1l1l1ll_opy_(hook_name)),
        bstack1l1lll_opy_ (u"ࠧࡣࡱࡧࡽࠬ₦"): {
            bstack1l1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭₧"): bstack1l1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ₨"),
            bstack1l1lll_opy_ (u"ࠪࡧࡴࡪࡥࠨ₩"): None
        },
        bstack1l1lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ₪"): test.name,
        bstack1l1lll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ₫"): bstack1l11ll11ll_opy_.bstack111lll111l_opy_(test, hook_name),
        bstack1l1lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ€"): file_path,
        bstack1l1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ₭"): file_path,
        bstack1l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₮"): bstack1l1lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ₯"),
        bstack1l1lll_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ₰"): file_path,
        bstack1l1lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₱"): bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₲")],
        bstack1l1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ₳"): bstack1l1lll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ₴") if bstack11111lll11l_opy_ == bstack1l1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ₵") else bstack1l1lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ₶"),
        bstack1l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭₷"): hook_type
    }
    bstack1111lll1ll1_opy_ = bstack111lll1l11_opy_(_111ll1l1l1_opy_.get(test.nodeid, None))
    if bstack1111lll1ll1_opy_:
        hook_data[bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ₸")] = bstack1111lll1ll1_opy_
    if result:
        hook_data[bstack1l1lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₹")] = result.outcome
        hook_data[bstack1l1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ₺")] = result.duration * 1000
        hook_data[bstack1l1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₻")] = bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₼")]
        if result.failed:
            hook_data[bstack1l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ₽")] = bstack111ll11l_opy_.bstack1111ll1111_opy_(call.excinfo.typename)
            hook_data[bstack1l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ₾")] = bstack111ll11l_opy_.bstack1111ll1l11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₿")] = bstack11l1llllll1_opy_(outcome)
        hook_data[bstack1l1lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⃀")] = 100
        hook_data[bstack1l1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃁")] = bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⃂")]
        if hook_data[bstack1l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⃃")] == bstack1l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⃄"):
            hook_data[bstack1l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⃅")] = bstack1l1lll_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬ⃆")  # bstack11111ll1l1l_opy_
            hook_data[bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⃇")] = [{bstack1l1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⃈"): [bstack1l1lll_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫ⃉")]}]
    if bstack11111ll11l1_opy_:
        hook_data[bstack1l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⃊")] = bstack11111ll11l1_opy_.result
        hook_data[bstack1l1lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⃋")] = bstack11l1l1ll111_opy_(bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⃌")], bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⃍")])
        hook_data[bstack1l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⃎")] = bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃏")]
        if hook_data[bstack1l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⃐")] == bstack1l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⃑"):
            hook_data[bstack1l1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⃒")] = bstack111ll11l_opy_.bstack1111ll1111_opy_(bstack11111ll11l1_opy_.exception_type)
            hook_data[bstack1l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨ⃓ࠫ")] = [{bstack1l1lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⃔"): bstack11l1l11l1ll_opy_(bstack11111ll11l1_opy_.exception)}]
    return hook_data
def bstack1111l11111l_opy_(test, bstack111l11lll1_opy_, bstack11l1l1l1l1_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1lll_opy_ (u"ࠬࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⃕").format(bstack11l1l1l1l1_opy_))
    bstack111lll1lll_opy_ = bstack11111l1lll1_opy_(test, bstack111l11lll1_opy_, result, call, bstack11l1l1l1l1_opy_, outcome)
    driver = getattr(test, bstack1l1lll_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⃖"), None)
    if bstack11l1l1l1l1_opy_ == bstack1l1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⃗") and driver:
        bstack111lll1lll_opy_[bstack1l1lll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹ⃘ࠧ")] = bstack111ll11l_opy_.bstack11l111111l_opy_(driver)
    if bstack11l1l1l1l1_opy_ == bstack1l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦ⃙ࠪ"):
        bstack11l1l1l1l1_opy_ = bstack1l1lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨ⃚ࠬ")
    bstack111ll11l11_opy_ = {
        bstack1l1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⃛"): bstack11l1l1l1l1_opy_,
        bstack1l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⃜"): bstack111lll1lll_opy_
    }
    bstack111ll11l_opy_.bstack11l1llll1_opy_(bstack111ll11l11_opy_)
    if bstack11l1l1l1l1_opy_ == bstack1l1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⃝"):
        threading.current_thread().bstackTestMeta = {bstack1l1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⃞"): bstack1l1lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⃟")}
    elif bstack11l1l1l1l1_opy_ == bstack1l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⃠"):
        threading.current_thread().bstackTestMeta = {bstack1l1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⃡"): getattr(result, bstack1l1lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⃢"), bstack1l1lll_opy_ (u"ࠬ࠭⃣"))}
def bstack11111l1ll11_opy_(test, bstack111l11lll1_opy_, bstack11l1l1l1l1_opy_, result=None, call=None, outcome=None, bstack11111ll11l1_opy_=None):
    logger.debug(bstack1l1lll_opy_ (u"࠭ࡳࡦࡰࡧࡣ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡪࡲࡳࡰࠦࡤࡢࡶࡤ࠰ࠥ࡫ࡶࡦࡰࡷࡘࡾࡶࡥࠡ࠯ࠣࡿࢂ࠭⃤").format(bstack11l1l1l1l1_opy_))
    hook_data = bstack11111l1llll_opy_(test, bstack111l11lll1_opy_, bstack11l1l1l1l1_opy_, result, call, outcome, bstack11111ll11l1_opy_)
    bstack111ll11l11_opy_ = {
        bstack1l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ⃥ࠫ"): bstack11l1l1l1l1_opy_,
        bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰ⃦ࠪ"): hook_data
    }
    bstack111ll11l_opy_.bstack11l1llll1_opy_(bstack111ll11l11_opy_)
def bstack111lll1l11_opy_(bstack111l11lll1_opy_):
    if not bstack111l11lll1_opy_:
        return None
    if bstack111l11lll1_opy_.get(bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⃧"), None):
        return getattr(bstack111l11lll1_opy_[bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ⃨࠭")], bstack1l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⃩"), None)
    return bstack111l11lll1_opy_.get(bstack1l1lll_opy_ (u"ࠬࡻࡵࡪࡦ⃪ࠪ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.LOG, bstack1llll1lll1l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_.LOG, bstack1llll1lll1l_opy_.POST, request, caplog)
        return # skip all existing bstack1111l111ll1_opy_
    try:
        if not bstack111ll11l_opy_.on():
            return
        places = [bstack1l1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴ⃫ࠬ"), bstack1l1lll_opy_ (u"ࠧࡤࡣ࡯ࡰ⃬ࠬ"), bstack1l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ⃭ࠪ")]
        logs = []
        for bstack11111llll11_opy_ in places:
            records = caplog.get_records(bstack11111llll11_opy_)
            bstack11111ll1ll1_opy_ = bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ⃮ࠩ") if bstack11111llll11_opy_ == bstack1l1lll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⃯") else bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃰")
            bstack11111lll1ll_opy_ = request.node.nodeid + (bstack1l1lll_opy_ (u"ࠬ࠭⃱") if bstack11111llll11_opy_ == bstack1l1lll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⃲") else bstack1l1lll_opy_ (u"ࠧ࠮ࠩ⃳") + bstack11111llll11_opy_)
            test_uuid = bstack111lll1l11_opy_(_111ll1l1l1_opy_.get(bstack11111lll1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l1llll1l1_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⃴"): bstack11l1ll1llll_opy_(record.created).isoformat() + bstack1l1lll_opy_ (u"ࠩ࡝ࠫ⃵"),
                    bstack1l1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⃶"): record.levelname,
                    bstack1l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃷"): record.message,
                    bstack11111ll1ll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111ll11l_opy_.bstack11lll11111_opy_(logs)
    except Exception as err:
        print(bstack1l1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ⃸"), str(err))
def bstack1l111ll11l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll111ll_opy_
    bstack1ll1111ll_opy_ = bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ⃹"), None) and bstack1l111l11_opy_(
            threading.current_thread(), bstack1l1lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⃺"), None)
    bstack11111l1ll_opy_ = getattr(driver, bstack1l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⃻"), None) != None and getattr(driver, bstack1l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⃼"), None) == True
    if sequence == bstack1l1lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⃽") and driver != None:
      if not bstack1ll111ll_opy_ and bstack1ll1111lll1_opy_() and bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃾") in CONFIG and CONFIG[bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃿")] == True and bstack11ll11ll11_opy_.bstack1ll11l1lll_opy_(driver_command) and (bstack11111l1ll_opy_ or bstack1ll1111ll_opy_) and not bstack1l111l1l1l_opy_(args):
        try:
          bstack1ll111ll_opy_ = True
          logger.debug(bstack1l1lll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨ℀").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1lll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬ℁").format(str(err)))
        bstack1ll111ll_opy_ = False
    if sequence == bstack1l1lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧℂ"):
        if driver_command == bstack1l1lll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭℃"):
            bstack111ll11l_opy_.bstack1l1ll11l11_opy_({
                bstack1l1lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ℄"): response[bstack1l1lll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ℅")],
                bstack1l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ℆"): store[bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪℇ")]
            })
def bstack1l1l11l11l_opy_():
    global bstack1l11lll1l_opy_
    bstack1ll1l111l1_opy_.bstack1l11l11l11_opy_()
    logging.shutdown()
    bstack111ll11l_opy_.bstack111ll111ll_opy_()
    for driver in bstack1l11lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111l111lll_opy_(*args):
    global bstack1l11lll1l_opy_
    bstack111ll11l_opy_.bstack111ll111ll_opy_()
    for driver in bstack1l11lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11ll111l_opy_, stage=STAGE.bstack1111lll1_opy_, bstack111lll1ll_opy_=bstack11l1l1lll1_opy_)
def bstack1llllll1ll_opy_(self, *args, **kwargs):
    bstack11ll1111l_opy_ = bstack11lll1111_opy_(self, *args, **kwargs)
    bstack1l1l1l111l_opy_ = getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ℈"), None)
    if bstack1l1l1l111l_opy_ and bstack1l1l1l111l_opy_.get(bstack1l1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ℉"), bstack1l1lll_opy_ (u"ࠩࠪℊ")) == bstack1l1lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫℋ"):
        bstack111ll11l_opy_.bstack1l1ll111l1_opy_(self)
    return bstack11ll1111l_opy_
@measure(event_name=EVENTS.bstack1l1lllll_opy_, stage=STAGE.bstack1ll1l1l1_opy_, bstack111lll1ll_opy_=bstack11l1l1lll1_opy_)
def bstack1lll1lll_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
    if bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨℌ")):
        return
    bstack11l1l1l1l_opy_.bstack1l111lll1_opy_(bstack1l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩℍ"), True)
    global bstack11l11l1l_opy_
    global bstack1l11111l1l_opy_
    bstack11l11l1l_opy_ = framework_name
    logger.info(bstack1l1ll111l_opy_.format(bstack11l11l1l_opy_.split(bstack1l1lll_opy_ (u"࠭࠭ࠨℎ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111lll1_opy_():
            Service.start = bstack1l1l1llll_opy_
            Service.stop = bstack1l1l1ll111_opy_
            webdriver.Remote.get = bstack1l1lll11l1_opy_
            webdriver.Remote.__init__ = bstack111lll11_opy_
            if not isinstance(os.getenv(bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨℏ")), str):
                return
            WebDriver.close = bstack1ll1ll1ll_opy_
            WebDriver.quit = bstack1lllll1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111ll11l_opy_.on():
            webdriver.Remote.__init__ = bstack1llllll1ll_opy_
        bstack1l11111l1l_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1lll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ℐ")):
        bstack1l11111l1l_opy_ = eval(os.environ.get(bstack1l1lll_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧℑ")))
    if not bstack1l11111l1l_opy_:
        bstack1l11llll1_opy_(bstack1l1lll_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧℒ"), bstack1ll1l111_opy_)
    if bstack1l1l1l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1lll1l1111_opy_ = bstack11111l1l_opy_
        except Exception as e:
            logger.error(bstack11111l1l1_opy_.format(str(e)))
    if bstack1l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫℓ") in str(framework_name).lower():
        if not bstack1ll1111lll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11ll1l11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll11ll1l_opy_
            Config.getoption = bstack1ll11111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1lll1ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11lll1ll_opy_, stage=STAGE.bstack1111lll1_opy_, bstack111lll1ll_opy_=bstack11l1l1lll1_opy_)
def bstack1lllll1l1_opy_(self):
    global bstack11l11l1l_opy_
    global bstack1l111111ll_opy_
    global bstack111ll11l1_opy_
    try:
        if bstack1l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ℔") in bstack11l11l1l_opy_ and self.session_id != None and bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪℕ"), bstack1l1lll_opy_ (u"ࠧࠨ№")) != bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ℗"):
            bstack1l1ll1ll1l_opy_ = bstack1l1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ℘") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪℙ")
            bstack11lllll11_opy_(logger, True)
            if self != None:
                bstack1ll111lll1_opy_(self, bstack1l1ll1ll1l_opy_, bstack1l1lll_opy_ (u"ࠫ࠱ࠦࠧℚ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1ll11l1_opy_):
            item = store.get(bstack1l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩℛ"), None)
            if item is not None and bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬℜ"), None):
                bstack1ll11l1ll1_opy_.bstack111l111l_opy_(self, bstack1l11l1111l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1lll_opy_ (u"ࠧࠨℝ")
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ℞") + str(e))
    bstack111ll11l1_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11lll1l1ll_opy_, stage=STAGE.bstack1111lll1_opy_, bstack111lll1ll_opy_=bstack11l1l1lll1_opy_)
def bstack111lll11_opy_(self, command_executor,
             desired_capabilities=None, bstack11lllll1_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l111111ll_opy_
    global bstack11l1l1lll1_opy_
    global bstack1ll111l11l_opy_
    global bstack11l11l1l_opy_
    global bstack11lll1111_opy_
    global bstack1l11lll1l_opy_
    global bstack1111l111_opy_
    global bstack1ll1l11111_opy_
    global bstack1l11l1111l_opy_
    CONFIG[bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ℟")] = str(bstack11l11l1l_opy_) + str(__version__)
    command_executor = bstack1l1ll1llll_opy_(bstack1111l111_opy_, CONFIG)
    logger.debug(bstack111l1lll1_opy_.format(command_executor))
    proxy = bstack11l1l1ll11_opy_(CONFIG, proxy)
    bstack11l11l1l1l_opy_ = 0
    try:
        if bstack1ll111l11l_opy_ is True:
            bstack11l11l1l1l_opy_ = int(os.environ.get(bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ℠")))
    except:
        bstack11l11l1l1l_opy_ = 0
    bstack1l1ll1111_opy_ = bstack1l11l111l_opy_(CONFIG, bstack11l11l1l1l_opy_)
    logger.debug(bstack1l11ll1l1_opy_.format(str(bstack1l1ll1111_opy_)))
    bstack1l11l1111l_opy_ = CONFIG.get(bstack1l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ℡"))[bstack11l11l1l1l_opy_]
    if bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ™") in CONFIG and CONFIG[bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ℣")]:
        bstack1ll1llll1l_opy_(bstack1l1ll1111_opy_, bstack1ll1l11111_opy_)
    if bstack1l1l1l11l_opy_.bstack1ll1llll1_opy_(CONFIG, bstack11l11l1l1l_opy_) and bstack1l1l1l11l_opy_.bstack111ll1lll_opy_(bstack1l1ll1111_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1ll111l_opy_(bstack1lll1ll11l1_opy_):
            bstack1l1l1l11l_opy_.set_capabilities(bstack1l1ll1111_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1l11ll11_opy_ = bstack1l1l1lllll_opy_(desired_capabilities)
        bstack1l1l11ll11_opy_[bstack1l1lll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧℤ")] = bstack1llll1l1l_opy_(CONFIG)
        bstack11ll11l11l_opy_ = bstack1l11l111l_opy_(bstack1l1l11ll11_opy_)
        if bstack11ll11l11l_opy_:
            bstack1l1ll1111_opy_ = update(bstack11ll11l11l_opy_, bstack1l1ll1111_opy_)
        desired_capabilities = None
    if options:
        bstack11ll1ll11_opy_(options, bstack1l1ll1111_opy_)
    if not options:
        options = bstack1l1l111l1l_opy_(bstack1l1ll1111_opy_)
    if proxy and bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ℥")):
        options.proxy(proxy)
    if options and bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨΩ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1ll1l11_opy_() < version.parse(bstack1l1lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ℧")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1ll1111_opy_)
    logger.info(bstack1lll11l11_opy_)
    bstack1ll11111l1_opy_.end(EVENTS.bstack1l1lllll_opy_.value, EVENTS.bstack1l1lllll_opy_.value + bstack1l1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦℨ"),
                               EVENTS.bstack1l1lllll_opy_.value + bstack1l1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ℩"), True, None)
    if bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭K")):
        bstack11lll1111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭Å")):
        bstack11lll1111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11lllll1_opy_=bstack11lllll1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨℬ")):
        bstack11lll1111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11lllll1_opy_=bstack11lllll1_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11lll1111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11lllll1_opy_=bstack11lllll1_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l1111ll_opy_ = bstack1l1lll_opy_ (u"ࠩࠪℭ")
        if bstack11l1ll1l11_opy_() >= version.parse(bstack1l1lll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫ℮")):
            bstack1l1111ll_opy_ = self.caps.get(bstack1l1lll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦℯ"))
        else:
            bstack1l1111ll_opy_ = self.capabilities.get(bstack1l1lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧℰ"))
        if bstack1l1111ll_opy_:
            bstack11llllllll_opy_(bstack1l1111ll_opy_)
            if bstack11l1ll1l11_opy_() <= version.parse(bstack1l1lll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ℱ")):
                self.command_executor._url = bstack1l1lll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣℲ") + bstack1111l111_opy_ + bstack1l1lll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧℳ")
            else:
                self.command_executor._url = bstack1l1lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦℴ") + bstack1l1111ll_opy_ + bstack1l1lll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦℵ")
            logger.debug(bstack1l1111111l_opy_.format(bstack1l1111ll_opy_))
        else:
            logger.debug(bstack1lllll1l1l_opy_.format(bstack1l1lll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧℶ")))
    except Exception as e:
        logger.debug(bstack1lllll1l1l_opy_.format(e))
    bstack1l111111ll_opy_ = self.session_id
    if bstack1l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬℷ") in bstack11l11l1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪℸ"), None)
        if item:
            bstack11111l1ll1l_opy_ = getattr(item, bstack1l1lll_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬℹ"), False)
            if not getattr(item, bstack1l1lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ℺"), None) and bstack11111l1ll1l_opy_:
                setattr(store[bstack1l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭℻")], bstack1l1lll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫℼ"), self)
        bstack1l1l1l111l_opy_ = getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬℽ"), None)
        if bstack1l1l1l111l_opy_ and bstack1l1l1l111l_opy_.get(bstack1l1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬℾ"), bstack1l1lll_opy_ (u"࠭ࠧℿ")) == bstack1l1lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⅀"):
            bstack111ll11l_opy_.bstack1l1ll111l1_opy_(self)
    bstack1l11lll1l_opy_.append(self)
    if bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⅁") in CONFIG and bstack1l1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⅂") in CONFIG[bstack1l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⅃")][bstack11l11l1l1l_opy_]:
        bstack11l1l1lll1_opy_ = CONFIG[bstack1l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⅄")][bstack11l11l1l1l_opy_][bstack1l1lll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪⅅ")]
    logger.debug(bstack1l1ll1l1l_opy_.format(bstack1l111111ll_opy_))
@measure(event_name=EVENTS.bstack1l1ll11l_opy_, stage=STAGE.bstack1111lll1_opy_, bstack111lll1ll_opy_=bstack11l1l1lll1_opy_)
def bstack1l1lll11l1_opy_(self, url):
    global bstack1111ll11_opy_
    global CONFIG
    try:
        bstack1l111ll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l1lll11_opy_.format(str(err)))
    try:
        bstack1111ll11_opy_(self, url)
    except Exception as e:
        try:
            bstack1l11l111ll_opy_ = str(e)
            if any(err_msg in bstack1l11l111ll_opy_ for err_msg in bstack1l1l1l11l1_opy_):
                bstack1l111ll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l1lll11_opy_.format(str(err)))
        raise e
def bstack1l11llll_opy_(item, when):
    global bstack1l11ll1lll_opy_
    try:
        bstack1l11ll1lll_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1lll1ll_opy_(item, call, rep):
    global bstack11l11ll111_opy_
    global bstack1l11lll1l_opy_
    name = bstack1l1lll_opy_ (u"࠭ࠧⅆ")
    try:
        if rep.when == bstack1l1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬⅇ"):
            bstack1l111111ll_opy_ = threading.current_thread().bstackSessionId
            bstack1111l11l11l_opy_ = item.config.getoption(bstack1l1lll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪⅈ"))
            try:
                if (str(bstack1111l11l11l_opy_).lower() != bstack1l1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧⅉ")):
                    name = str(rep.nodeid)
                    bstack1l1ll11lll_opy_ = bstack11ll11lll1_opy_(bstack1l1lll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⅊"), name, bstack1l1lll_opy_ (u"ࠫࠬ⅋"), bstack1l1lll_opy_ (u"ࠬ࠭⅌"), bstack1l1lll_opy_ (u"࠭ࠧ⅍"), bstack1l1lll_opy_ (u"ࠧࠨⅎ"))
                    os.environ[bstack1l1lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⅏")] = name
                    for driver in bstack1l11lll1l_opy_:
                        if bstack1l111111ll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll11lll_opy_)
            except Exception as e:
                logger.debug(bstack1l1lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ⅐").format(str(e)))
            try:
                bstack11l1111ll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⅑"):
                    status = bstack1l1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⅒") if rep.outcome.lower() == bstack1l1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⅓") else bstack1l1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⅔")
                    reason = bstack1l1lll_opy_ (u"ࠧࠨ⅕")
                    if status == bstack1l1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⅖"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1lll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ⅗") if status == bstack1l1lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⅘") else bstack1l1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⅙")
                    data = name + bstack1l1lll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ⅚") if status == bstack1l1lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⅛") else name + bstack1l1lll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪ⅜") + reason
                    bstack11llll1l_opy_ = bstack11ll11lll1_opy_(bstack1l1lll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ⅝"), bstack1l1lll_opy_ (u"ࠩࠪ⅞"), bstack1l1lll_opy_ (u"ࠪࠫ⅟"), bstack1l1lll_opy_ (u"ࠫࠬⅠ"), level, data)
                    for driver in bstack1l11lll1l_opy_:
                        if bstack1l111111ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11llll1l_opy_)
            except Exception as e:
                logger.debug(bstack1l1lll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩⅡ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪⅢ").format(str(e)))
    bstack11l11ll111_opy_(item, call, rep)
notset = Notset()
def bstack1ll11111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11l1llll_opy_
    if str(name).lower() == bstack1l1lll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧⅣ"):
        return bstack1l1lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢⅤ")
    else:
        return bstack11l1llll_opy_(self, name, default, skip)
def bstack11111l1l_opy_(self):
    global CONFIG
    global bstack11111ll11_opy_
    try:
        proxy = bstack1ll11lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1lll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧⅥ")):
                proxies = bstack11llllll_opy_(proxy, bstack1l1ll1llll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lllll11_opy_ = proxies.popitem()
                    if bstack1l1lll_opy_ (u"ࠥ࠾࠴࠵ࠢⅦ") in bstack1lllll11_opy_:
                        return bstack1lllll11_opy_
                    else:
                        return bstack1l1lll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧⅧ") + bstack1lllll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤⅨ").format(str(e)))
    return bstack11111ll11_opy_(self)
def bstack1l1l1l1l_opy_():
    return (bstack1l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩⅩ") in CONFIG or bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫⅪ") in CONFIG) and bstack1ll1l1l11_opy_() and bstack11l1ll1l11_opy_() >= version.parse(
        bstack1l11l1llll_opy_)
def bstack1llll11l_opy_(self,
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
    global bstack11l1l1lll1_opy_
    global bstack1ll111l11l_opy_
    global bstack11l11l1l_opy_
    CONFIG[bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪⅫ")] = str(bstack11l11l1l_opy_) + str(__version__)
    bstack11l11l1l1l_opy_ = 0
    try:
        if bstack1ll111l11l_opy_ is True:
            bstack11l11l1l1l_opy_ = int(os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩⅬ")))
    except:
        bstack11l11l1l1l_opy_ = 0
    CONFIG[bstack1l1lll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤⅭ")] = True
    bstack1l1ll1111_opy_ = bstack1l11l111l_opy_(CONFIG, bstack11l11l1l1l_opy_)
    logger.debug(bstack1l11ll1l1_opy_.format(str(bstack1l1ll1111_opy_)))
    if CONFIG.get(bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨⅮ")):
        bstack1ll1llll1l_opy_(bstack1l1ll1111_opy_, bstack1ll1l11111_opy_)
    if bstack1l1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨⅯ") in CONFIG and bstack1l1lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫⅰ") in CONFIG[bstack1l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅱ")][bstack11l11l1l1l_opy_]:
        bstack11l1l1lll1_opy_ = CONFIG[bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫⅲ")][bstack11l11l1l1l_opy_][bstack1l1lll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧⅳ")]
    import urllib
    import json
    if bstack1l1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧⅴ") in CONFIG and str(CONFIG[bstack1l1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨⅵ")]).lower() != bstack1l1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫⅶ"):
        bstack1l111llll1_opy_ = bstack11ll11l111_opy_()
        bstack111ll1111_opy_ = bstack1l111llll1_opy_ + urllib.parse.quote(json.dumps(bstack1l1ll1111_opy_))
    else:
        bstack111ll1111_opy_ = bstack1l1lll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨⅷ") + urllib.parse.quote(json.dumps(bstack1l1ll1111_opy_))
    browser = self.connect(bstack111ll1111_opy_)
    return browser
def bstack1ll1111ll1_opy_():
    global bstack1l11111l1l_opy_
    global bstack11l11l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11ll111lll_opy_
        if not bstack1ll1111lll1_opy_():
            global bstack1ll11l1ll_opy_
            if not bstack1ll11l1ll_opy_:
                from bstack_utils.helper import bstack1lll1l1l_opy_, bstack11l11lll_opy_
                bstack1ll11l1ll_opy_ = bstack1lll1l1l_opy_()
                bstack11l11lll_opy_(bstack11l11l1l_opy_)
            BrowserType.connect = bstack11ll111lll_opy_
            return
        BrowserType.launch = bstack1llll11l_opy_
        bstack1l11111l1l_opy_ = True
    except Exception as e:
        pass
def bstack11111ll1l11_opy_():
    global CONFIG
    global bstack11ll111l_opy_
    global bstack1111l111_opy_
    global bstack1ll1l11111_opy_
    global bstack1ll111l11l_opy_
    global bstack1ll1111l11_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ⅸ")))
    bstack11ll111l_opy_ = eval(os.environ.get(bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩⅹ")))
    bstack1111l111_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩⅺ"))
    bstack1ll1lll1_opy_(CONFIG, bstack11ll111l_opy_)
    bstack1ll1111l11_opy_ = bstack1ll1l111l1_opy_.bstack11l1ll11_opy_(CONFIG, bstack1ll1111l11_opy_)
    if cli.bstack1l1111llll_opy_():
        bstack111ll1l1l_opy_.invoke(bstack1lllll1ll1_opy_.CONNECT, bstack11111lll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪⅻ"), bstack1l1lll_opy_ (u"ࠫ࠵࠭ⅼ")))
        cli.bstack1lll1l1111l_opy_(cli_context.platform_index)
        cli.bstack1llll11l1l1_opy_(bstack1l1ll1llll_opy_(bstack1111l111_opy_, CONFIG), cli_context.platform_index, bstack1l1l111l1l_opy_)
        cli.bstack1lll1l111ll_opy_()
        logger.debug(bstack1l1lll_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦⅽ") + str(cli_context.platform_index) + bstack1l1lll_opy_ (u"ࠨࠢⅾ"))
        return # skip all existing bstack1111l111ll1_opy_
    global bstack11lll1111_opy_
    global bstack111ll11l1_opy_
    global bstack11l1ll11l_opy_
    global bstack11ll1llll_opy_
    global bstack1l1111l11_opy_
    global bstack1l1111l111_opy_
    global bstack1l1l11llll_opy_
    global bstack1111ll11_opy_
    global bstack11111ll11_opy_
    global bstack11l1llll_opy_
    global bstack1l11ll1lll_opy_
    global bstack11l11ll111_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11lll1111_opy_ = webdriver.Remote.__init__
        bstack111ll11l1_opy_ = WebDriver.quit
        bstack1l1l11llll_opy_ = WebDriver.close
        bstack1111ll11_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪⅿ") in CONFIG or bstack1l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬↀ") in CONFIG) and bstack1ll1l1l11_opy_():
        if bstack11l1ll1l11_opy_() < version.parse(bstack1l11l1llll_opy_):
            logger.error(bstack11l11ll11_opy_.format(bstack11l1ll1l11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11111ll11_opy_ = RemoteConnection._1lll1l1111_opy_
            except Exception as e:
                logger.error(bstack11111l1l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11l1llll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l11ll1lll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11ll111ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack11l11ll111_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪↁ"))
    bstack1ll1l11111_opy_ = CONFIG.get(bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧↂ"), {}).get(bstack1l1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ↄ"))
    bstack1ll111l11l_opy_ = True
    bstack1lll1lll_opy_(bstack1l11l11l_opy_)
if (bstack11l1l11ll1l_opy_()):
    bstack11111ll1l11_opy_()
@bstack111ll1ll1l_opy_(class_method=False)
def bstack11111ll1111_opy_(hook_name, event, bstack1l111lll11l_opy_=None):
    if hook_name not in [bstack1l1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ↄ"), bstack1l1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪↅ"), bstack1l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ↆ"), bstack1l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪↇ"), bstack1l1lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧↈ"), bstack1l1lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ↉"), bstack1l1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ↊"), bstack1l1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ↋")]:
        return
    node = store[bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ↌")]
    if hook_name in [bstack1l1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭↍"), bstack1l1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ↎")]:
        node = store[bstack1l1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨ↏")]
    elif hook_name in [bstack1l1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ←"), bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ↑")]:
        node = store[bstack1l1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ→")]
    hook_type = bstack111l1l1l11l_opy_(hook_name)
    if event == bstack1l1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭↓"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_[hook_type], bstack1llll1lll1l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l11l1ll_opy_ = {
            bstack1l1lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↔"): uuid,
            bstack1l1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ↕"): bstack1l1ll1ll_opy_(),
            bstack1l1lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ↖"): bstack1l1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ↗"),
            bstack1l1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ↘"): hook_type,
            bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ↙"): hook_name
        }
        store[bstack1l1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ↚")].append(uuid)
        bstack1111l1111ll_opy_ = node.nodeid
        if hook_type == bstack1l1lll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ↛"):
            if not _111ll1l1l1_opy_.get(bstack1111l1111ll_opy_, None):
                _111ll1l1l1_opy_[bstack1111l1111ll_opy_] = {bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ↜"): []}
            _111ll1l1l1_opy_[bstack1111l1111ll_opy_][bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ↝")].append(bstack111l11l1ll_opy_[bstack1l1lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ↞")])
        _111ll1l1l1_opy_[bstack1111l1111ll_opy_ + bstack1l1lll_opy_ (u"ࠫ࠲࠭↟") + hook_name] = bstack111l11l1ll_opy_
        bstack11111l1ll11_opy_(node, bstack111l11l1ll_opy_, bstack1l1lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭↠"))
    elif event == bstack1l1lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ↡"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1llll1ll1l1_opy_[hook_type], bstack1llll1lll1l_opy_.POST, node, None, bstack1l111lll11l_opy_)
            return
        bstack111llll1ll_opy_ = node.nodeid + bstack1l1lll_opy_ (u"ࠧ࠮ࠩ↢") + hook_name
        _111ll1l1l1_opy_[bstack111llll1ll_opy_][bstack1l1lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭↣")] = bstack1l1ll1ll_opy_()
        bstack11111lllll1_opy_(_111ll1l1l1_opy_[bstack111llll1ll_opy_][bstack1l1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ↤")])
        bstack11111l1ll11_opy_(node, _111ll1l1l1_opy_[bstack111llll1ll_opy_], bstack1l1lll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ↥"), bstack11111ll11l1_opy_=bstack1l111lll11l_opy_)
def bstack11111ll1lll_opy_():
    global bstack11111lll11l_opy_
    if bstack111lllll1_opy_():
        bstack11111lll11l_opy_ = bstack1l1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ↦")
    else:
        bstack11111lll11l_opy_ = bstack1l1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ↧")
@bstack111ll11l_opy_.bstack1111l1lll11_opy_
def bstack11111l1l1ll_opy_():
    bstack11111ll1lll_opy_()
    if cli.is_running():
        try:
            bstack11l11l1l1l1_opy_(bstack11111ll1111_opy_)
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ↨").format(e))
        return
    if bstack1ll1l1l11_opy_():
        bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
        bstack1l1lll_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡀࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡭ࡥࡵࡵࠣࡹࡸ࡫ࡤࠡࡨࡲࡶࠥࡧ࠱࠲ࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠲ࡽࡲࡢࡲࡳ࡭ࡳ࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡸࠥ࡯ࡳࠡࡲࡤࡸࡨ࡮ࡥࡥࠢ࡬ࡲࠥࡧࠠࡥ࡫ࡩࡪࡪࡸࡥ࡯ࡶࠣࡴࡷࡵࡣࡦࡵࡶࠤ࡮ࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡶࡵࠣࡻࡪࠦ࡮ࡦࡧࡧࠤࡹࡵࠠࡶࡵࡨࠤࡘ࡫࡬ࡦࡰ࡬ࡹࡲࡖࡡࡵࡥ࡫ࠬࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡨࡢࡰࡧࡰࡪࡸࠩࠡࡨࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࠩࠪ↩")
        if bstack11l1l1l1l_opy_.get_property(bstack1l1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ↪")):
            if CONFIG.get(bstack1l1lll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ↫")) is not None and int(CONFIG[bstack1l1lll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ↬")]) > 1:
                bstack11l1lll1ll_opy_(bstack1l111ll11l_opy_)
            return
        bstack11l1lll1ll_opy_(bstack1l111ll11l_opy_)
    try:
        bstack11l11l1l1l1_opy_(bstack11111ll1111_opy_)
    except Exception as e:
        logger.debug(bstack1l1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ↭").format(e))
bstack11111l1l1ll_opy_()