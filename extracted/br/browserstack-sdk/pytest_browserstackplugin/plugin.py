# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1llll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll1111111_opy_, bstack1l1ll1ll11_opy_, update, bstack1l11lll1ll_opy_,
                                       bstack1l1111lll_opy_, bstack1ll1l111_opy_, bstack1ll1lllll_opy_, bstack11l1ll1ll_opy_,
                                       bstack1l11l11111_opy_, bstack1ll1l11l1_opy_, bstack11lll1ll1l_opy_, bstack11l1l111l1_opy_,
                                       bstack1111l11ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1llll1ll11_opy_)
from browserstack_sdk.bstack11l1111ll_opy_ import bstack1lll1111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1llllll1ll_opy_
from bstack_utils.capture import bstack111llll1ll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l111111l1_opy_, bstack11ll11111_opy_, bstack1l11llll_opy_, \
    bstack1lll1l111l_opy_
from bstack_utils.helper import bstack1lll11l1_opy_, bstack11l1llll1ll_opy_, bstack111l1l1l11_opy_, bstack11ll1l1l11_opy_, bstack1l1lllll1l1_opy_, bstack1l11l1l11l_opy_, \
    bstack11l1l111ll1_opy_, \
    bstack11l1l11l11l_opy_, bstack1llll1ll1_opy_, bstack1l1l1ll11_opy_, bstack11l1ll111ll_opy_, bstack11l1ll1l11_opy_, Notset, \
    bstack1ll11ll1l_opy_, bstack11l1l1l1ll1_opy_, bstack11l1ll1ll1l_opy_, Result, bstack11l1l1l1l11_opy_, bstack11ll11ll11l_opy_, bstack111l1l1111_opy_, \
    bstack11lll1ll11_opy_, bstack1l1111111l_opy_, bstack11l1l1ll_opy_, bstack11l1ll1l11l_opy_
from bstack_utils.bstack11l11ll111l_opy_ import bstack11l11ll11ll_opy_
from bstack_utils.messages import bstack1ll1l11l_opy_, bstack11lllll1l1_opy_, bstack11lllllll1_opy_, bstack1l1llllll_opy_, bstack11lll1lll1_opy_, \
    bstack11l1lll1ll_opy_, bstack1l1l11ll11_opy_, bstack1l1l11l1l1_opy_, bstack111llll11_opy_, bstack1lll1ll1l_opy_, \
    bstack11ll111l11_opy_, bstack1lll1111ll_opy_
from bstack_utils.proxy import bstack1l111ll11l_opy_, bstack11l11lllll_opy_
from bstack_utils.bstack1l11llll1l_opy_ import bstack111l1l1ll1l_opy_, bstack111l1l1l111_opy_, bstack111l1l1l11l_opy_, bstack111l1l111ll_opy_, \
    bstack111l1l11111_opy_, bstack111l1l11lll_opy_, bstack111l1l11l11_opy_, bstack1l1l1llll1_opy_, bstack111l1l111l1_opy_
from bstack_utils.bstack11l111ll1_opy_ import bstack1ll1l1l1ll_opy_
from bstack_utils.bstack1l1l11l111_opy_ import bstack1111l111_opy_, bstack111lll1ll_opy_, bstack11ll1111l1_opy_, \
    bstack1ll1l1l1l1_opy_, bstack1ll1l1lll_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack11l111l11l_opy_
from bstack_utils.bstack11l1111ll1_opy_ import bstack1ll1l111l1_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack11l11111ll_opy_ import bstack11l11llll_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1l1llll1_opy_
from browserstack_sdk.__init__ import bstack1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1lll111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack11l1l11ll_opy_ import bstack11l1l11ll_opy_, bstack111ll1ll_opy_, bstack1ll1lllll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1111ll_opy_, bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11l1l11ll_opy_ import bstack11l1l11ll_opy_, bstack111ll1ll_opy_, bstack1ll1lllll1_opy_
bstack1llllll11l_opy_ = None
bstack11l1l11l_opy_ = None
bstack1l1llll1ll_opy_ = None
bstack111111l1_opy_ = None
bstack1l1l1l111_opy_ = None
bstack11ll11ll1_opy_ = None
bstack1l111l11_opy_ = None
bstack1ll111l111_opy_ = None
bstack11ll11l1l_opy_ = None
bstack1l111l11ll_opy_ = None
bstack11l11l1l1_opy_ = None
bstack11l11l1ll1_opy_ = None
bstack1l1l1ll1l1_opy_ = None
bstack1ll11ll1l1_opy_ = bstack1llllll_opy_ (u"ࠪࠫὧ")
CONFIG = {}
bstack11l1l11lll_opy_ = False
bstack1l1lll111l_opy_ = bstack1llllll_opy_ (u"ࠫࠬὨ")
bstack1l1l1l1111_opy_ = bstack1llllll_opy_ (u"ࠬ࠭Ὡ")
bstack11l1l1l1_opy_ = False
bstack1l11l1l111_opy_ = []
bstack1ll1l111ll_opy_ = bstack1l111111l1_opy_
bstack11111l1l1ll_opy_ = bstack1llllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭Ὢ")
bstack1ll1ll11l_opy_ = {}
bstack1llll1111l_opy_ = None
bstack1l1111l111_opy_ = False
logger = bstack1llllll1ll_opy_.get_logger(__name__, bstack1ll1l111ll_opy_)
store = {
    bstack1llllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫὫ"): []
}
bstack1111l1111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111ll1lll1_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l1111ll_opy_(
    test_framework_name=bstack1ll11111ll_opy_[bstack1llllll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬὬ")] if bstack11l1ll1l11_opy_() else bstack1ll11111ll_opy_[bstack1llllll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩὭ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l1l11ll1l_opy_(page, bstack1l1l1l11l_opy_):
    try:
        page.evaluate(bstack1llllll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦὮ"),
                      bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨὯ") + json.dumps(
                          bstack1l1l1l11l_opy_) + bstack1llllll_opy_ (u"ࠧࢃࡽࠣὰ"))
    except Exception as e:
        print(bstack1llllll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦά"), e)
def bstack1l11l1lll1_opy_(page, message, level):
    try:
        page.evaluate(bstack1llllll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣὲ"), bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭έ") + json.dumps(
            message) + bstack1llllll_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬὴ") + json.dumps(level) + bstack1llllll_opy_ (u"ࠪࢁࢂ࠭ή"))
    except Exception as e:
        print(bstack1llllll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢὶ"), e)
def pytest_configure(config):
    global bstack1l1lll111l_opy_
    global CONFIG
    bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
    config.args = bstack1ll1l111l1_opy_.bstack1111l11lll1_opy_(config.args)
    bstack1l1ll1l1l1_opy_.bstack1l11l111ll_opy_(bstack11l1l1ll_opy_(config.getoption(bstack1llllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩί"))))
    try:
        bstack1llllll1ll_opy_.bstack11l11l1111l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11l1l11ll_opy_.invoke(bstack111ll1ll_opy_.CONNECT, bstack1ll1lllll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ὸ"), bstack1llllll_opy_ (u"ࠧ࠱ࠩό")))
        config = json.loads(os.environ.get(bstack1llllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢὺ"), bstack1llllll_opy_ (u"ࠤࡾࢁࠧύ")))
        cli.bstack1ll1lllllll_opy_(bstack1l1l1ll11_opy_(bstack1l1lll111l_opy_, CONFIG), cli_context.platform_index, bstack1l11lll1ll_opy_)
    if cli.bstack1lll1ll1l11_opy_(bstack1lll111ll1l_opy_):
        cli.bstack1lll1l1ll1l_opy_()
        logger.debug(bstack1llllll_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤὼ") + str(cli_context.platform_index) + bstack1llllll_opy_ (u"ࠦࠧώ"))
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.BEFORE_ALL, bstack1lll1lll1l1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1llllll_opy_ (u"ࠧࡽࡨࡦࡰࠥ὾"), None)
    if cli.is_running() and when == bstack1llllll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ὿"):
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.LOG_REPORT, bstack1lll1lll1l1_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1llllll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᾀ"):
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.BEFORE_EACH, bstack1lll1lll1l1_opy_.POST, item, call, outcome)
        elif when == bstack1llllll_opy_ (u"ࠣࡥࡤࡰࡱࠨᾁ"):
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.LOG_REPORT, bstack1lll1lll1l1_opy_.POST, item, call, outcome)
        elif when == bstack1llllll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᾂ"):
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.AFTER_EACH, bstack1lll1lll1l1_opy_.POST, item, call, outcome)
        return # skip all existing bstack11111lll11l_opy_
    bstack11111l1ll11_opy_ = item.config.getoption(bstack1llllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᾃ"))
    plugins = item.config.getoption(bstack1llllll_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᾄ"))
    report = outcome.get_result()
    bstack1111l11111l_opy_(item, call, report)
    if bstack1llllll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᾅ") not in plugins or bstack11l1ll1l11_opy_():
        return
    summary = []
    driver = getattr(item, bstack1llllll_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᾆ"), None)
    page = getattr(item, bstack1llllll_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᾇ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1111l11l11l_opy_(item, report, summary, bstack11111l1ll11_opy_)
    if (page is not None):
        bstack1111l111111_opy_(item, report, summary, bstack11111l1ll11_opy_)
def bstack1111l11l11l_opy_(item, report, summary, bstack11111l1ll11_opy_):
    if report.when == bstack1llllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᾈ") and report.skipped:
        bstack111l1l111l1_opy_(report)
    if report.when in [bstack1llllll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᾉ"), bstack1llllll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᾊ")]:
        return
    if not bstack1l1lllll1l1_opy_():
        return
    try:
        if (str(bstack11111l1ll11_opy_).lower() != bstack1llllll_opy_ (u"ࠫࡹࡸࡵࡦࠩᾋ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᾌ") + json.dumps(
                    report.nodeid) + bstack1llllll_opy_ (u"࠭ࡽࡾࠩᾍ"))
        os.environ[bstack1llllll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᾎ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1llllll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᾏ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llllll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᾐ")))
    bstack1lllll111_opy_ = bstack1llllll_opy_ (u"ࠥࠦᾑ")
    bstack111l1l111l1_opy_(report)
    if not passed:
        try:
            bstack1lllll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1llllll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᾒ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllll111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1llllll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᾓ")))
        bstack1lllll111_opy_ = bstack1llllll_opy_ (u"ࠨࠢᾔ")
        if not passed:
            try:
                bstack1lllll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llllll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᾕ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllll111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᾖ")
                    + json.dumps(bstack1llllll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᾗ"))
                    + bstack1llllll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᾘ")
                )
            else:
                item._driver.execute_script(
                    bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᾙ")
                    + json.dumps(str(bstack1lllll111_opy_))
                    + bstack1llllll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᾚ")
                )
        except Exception as e:
            summary.append(bstack1llllll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᾛ").format(e))
def bstack1111l11l111_opy_(test_name, error_message):
    try:
        bstack11111ll1l11_opy_ = []
        bstack1ll111ll11_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᾜ"), bstack1llllll_opy_ (u"ࠨ࠲ࠪᾝ"))
        bstack1ll11l1l1_opy_ = {bstack1llllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᾞ"): test_name, bstack1llllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᾟ"): error_message, bstack1llllll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᾠ"): bstack1ll111ll11_opy_}
        bstack11111lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᾡ"))
        if os.path.exists(bstack11111lll1ll_opy_):
            with open(bstack11111lll1ll_opy_) as f:
                bstack11111ll1l11_opy_ = json.load(f)
        bstack11111ll1l11_opy_.append(bstack1ll11l1l1_opy_)
        with open(bstack11111lll1ll_opy_, bstack1llllll_opy_ (u"࠭ࡷࠨᾢ")) as f:
            json.dump(bstack11111ll1l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᾣ") + str(e))
def bstack1111l111111_opy_(item, report, summary, bstack11111l1ll11_opy_):
    if report.when in [bstack1llllll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᾤ"), bstack1llllll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᾥ")]:
        return
    if (str(bstack11111l1ll11_opy_).lower() != bstack1llllll_opy_ (u"ࠪࡸࡷࡻࡥࠨᾦ")):
        bstack1l1l11ll1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llllll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᾧ")))
    bstack1lllll111_opy_ = bstack1llllll_opy_ (u"ࠧࠨᾨ")
    bstack111l1l111l1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lllll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llllll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᾩ").format(e)
                )
        try:
            if passed:
                bstack1ll1l1lll_opy_(getattr(item, bstack1llllll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᾪ"), None), bstack1llllll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᾫ"))
            else:
                error_message = bstack1llllll_opy_ (u"ࠩࠪᾬ")
                if bstack1lllll111_opy_:
                    bstack1l11l1lll1_opy_(item._page, str(bstack1lllll111_opy_), bstack1llllll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᾭ"))
                    bstack1ll1l1lll_opy_(getattr(item, bstack1llllll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᾮ"), None), bstack1llllll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᾯ"), str(bstack1lllll111_opy_))
                    error_message = str(bstack1lllll111_opy_)
                else:
                    bstack1ll1l1lll_opy_(getattr(item, bstack1llllll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᾰ"), None), bstack1llllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᾱ"))
                bstack1111l11l111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1llllll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᾲ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1llllll_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᾳ"), default=bstack1llllll_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᾴ"), help=bstack1llllll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥ᾵"))
    parser.addoption(bstack1llllll_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᾶ"), default=bstack1llllll_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᾷ"), help=bstack1llllll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᾸ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1llllll_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᾹ"), action=bstack1llllll_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᾺ"), default=bstack1llllll_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥΆ"),
                         help=bstack1llllll_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᾼ"))
def bstack111lllllll_opy_(log):
    if not (log[bstack1llllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᾽")] and log[bstack1llllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧι")].strip()):
        return
    active = bstack111llll111_opy_()
    log = {
        bstack1llllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᾿"): log[bstack1llllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ῀")],
        bstack1llllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ῁"): bstack111l1l1l11_opy_().isoformat() + bstack1llllll_opy_ (u"ࠪ࡞ࠬῂ"),
        bstack1llllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬῃ"): log[bstack1llllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ῄ")],
    }
    if active:
        if active[bstack1llllll_opy_ (u"࠭ࡴࡺࡲࡨࠫ῅")] == bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬῆ"):
            log[bstack1llllll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨῇ")] = active[bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩῈ")]
        elif active[bstack1llllll_opy_ (u"ࠪࡸࡾࡶࡥࠨΈ")] == bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩῊ"):
            log[bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬΉ")] = active[bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ῌ")]
    bstack11l11llll_opy_.bstack11lll11l1l_opy_([log])
def bstack111llll111_opy_():
    if len(store[bstack1llllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ῍")]) > 0 and store[bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ῎")][-1]:
        return {
            bstack1llllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ῏"): bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨῐ"),
            bstack1llllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫῑ"): store[bstack1llllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩῒ")][-1]
        }
    if store.get(bstack1llllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪΐ"), None):
        return {
            bstack1llllll_opy_ (u"ࠧࡵࡻࡳࡩࠬ῔"): bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹ࠭῕"),
            bstack1llllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩῖ"): store[bstack1llllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧῗ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.INIT_TEST, bstack1lll1lll1l1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.INIT_TEST, bstack1lll1lll1l1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.TEST, bstack1lll1lll1l1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111ll1lll_opy_ = True
        bstack11l11l11l_opy_ = bstack11111l11l_opy_.bstack11l1ll11l_opy_(bstack11l1l11l11l_opy_(item.own_markers))
        if not cli.bstack1lll1ll1l11_opy_(bstack1lll111ll1l_opy_):
            item._a11y_test_case = bstack11l11l11l_opy_
            if bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪῘ"), None):
                driver = getattr(item, bstack1llllll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭Ῑ"), None)
                item._a11y_started = bstack11111l11l_opy_.bstack1l1ll1lll1_opy_(driver, bstack11l11l11l_opy_)
        if not bstack11l11llll_opy_.on() or bstack11111l1l1ll_opy_ != bstack1llllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭Ὶ"):
            return
        global current_test_uuid #, bstack11l111lll1_opy_
        bstack111l1l1lll_opy_ = {
            bstack1llllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬΊ"): uuid4().__str__(),
            bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ῜"): bstack111l1l1l11_opy_().isoformat() + bstack1llllll_opy_ (u"ࠩ࡝ࠫ῝")
        }
        current_test_uuid = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ῞")]
        store[bstack1llllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ῟")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠬࡻࡵࡪࡦࠪῠ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111ll1lll1_opy_[item.nodeid] = {**_111ll1lll1_opy_[item.nodeid], **bstack111l1l1lll_opy_}
        bstack11111ll1ll1_opy_(item, _111ll1lll1_opy_[item.nodeid], bstack1llllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧῡ"))
    except Exception as err:
        print(bstack1llllll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩῢ"), str(err))
def pytest_runtest_setup(item):
    store[bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬΰ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.BEFORE_EACH, bstack1lll1lll1l1_opy_.PRE, item, bstack1llllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨῤ"))
        return # skip all existing bstack11111lll11l_opy_
    global bstack1111l1111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l1ll111ll_opy_():
        atexit.register(bstack1l111ll1_opy_)
        if not bstack1111l1111ll_opy_:
            try:
                bstack11111ll1111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1ll1l11l_opy_():
                    bstack11111ll1111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111ll1111_opy_:
                    signal.signal(s, bstack1111l111ll1_opy_)
                bstack1111l1111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1llllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦῥ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l1ll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1llllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫῦ")
    try:
        if not bstack11l11llll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1l1lll_opy_ = {
            bstack1llllll_opy_ (u"ࠬࡻࡵࡪࡦࠪῧ"): uuid,
            bstack1llllll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪῨ"): bstack111l1l1l11_opy_().isoformat() + bstack1llllll_opy_ (u"࡛ࠧࠩῩ"),
            bstack1llllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ὺ"): bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧΎ"),
            bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭Ῥ"): bstack1llllll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ῭"),
            bstack1llllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ΅"): bstack1llllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ`")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1llllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ῰")] = item
        store[bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ῱")] = [uuid]
        if not _111ll1lll1_opy_.get(item.nodeid, None):
            _111ll1lll1_opy_[item.nodeid] = {bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨῲ"): [], bstack1llllll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬῳ"): []}
        _111ll1lll1_opy_[item.nodeid][bstack1llllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪῴ")].append(bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠬࡻࡵࡪࡦࠪ῵")])
        _111ll1lll1_opy_[item.nodeid + bstack1llllll_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭ῶ")] = bstack111l1l1lll_opy_
        bstack11111lllll1_opy_(item, bstack111l1l1lll_opy_, bstack1llllll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨῷ"))
    except Exception as err:
        print(bstack1llllll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫῸ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.TEST, bstack1lll1lll1l1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.AFTER_EACH, bstack1lll1lll1l1_opy_.PRE, item, bstack1llllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫΌ"))
        return # skip all existing bstack11111lll11l_opy_
    try:
        global bstack1ll1ll11l_opy_
        bstack1ll111ll11_opy_ = 0
        if bstack11l1l1l1_opy_ is True:
            bstack1ll111ll11_opy_ = int(os.environ.get(bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪῺ")))
        if bstack11lll1ll1_opy_.bstack1lll11111l_opy_() == bstack1llllll_opy_ (u"ࠦࡹࡸࡵࡦࠤΏ"):
            if bstack11lll1ll1_opy_.bstack1111lll11_opy_() == bstack1llllll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢῼ"):
                bstack11111l1llll_opy_ = bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ´"), None)
                bstack1ll1l11111_opy_ = bstack11111l1llll_opy_ + bstack1llllll_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥ῾")
                driver = getattr(item, bstack1llllll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ῿"), None)
                bstack1ll1lll1l_opy_ = getattr(item, bstack1llllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ "), None)
                bstack1l1l11l1ll_opy_ = getattr(item, bstack1llllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ "), None)
                PercySDK.screenshot(driver, bstack1ll1l11111_opy_, bstack1ll1lll1l_opy_=bstack1ll1lll1l_opy_, bstack1l1l11l1ll_opy_=bstack1l1l11l1ll_opy_, bstack1lll111lll_opy_=bstack1ll111ll11_opy_)
        if not cli.bstack1lll1ll1l11_opy_(bstack1lll111ll1l_opy_):
            if getattr(item, bstack1llllll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ "), False):
                bstack1lll1111l_opy_.bstack1l1ll1l1_opy_(getattr(item, bstack1llllll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ "), None), bstack1ll1ll11l_opy_, logger, item)
        if not bstack11l11llll_opy_.on():
            return
        bstack111l1l1lll_opy_ = {
            bstack1llllll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ "): uuid4().__str__(),
            bstack1llllll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ "): bstack111l1l1l11_opy_().isoformat() + bstack1llllll_opy_ (u"ࠨ࡜ࠪ "),
            bstack1llllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ "): bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ "),
            bstack1llllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ "): bstack1llllll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ "),
            bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ​"): bstack1llllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ‌")
        }
        _111ll1lll1_opy_[item.nodeid + bstack1llllll_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ‍")] = bstack111l1l1lll_opy_
        bstack11111lllll1_opy_(item, bstack111l1l1lll_opy_, bstack1llllll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ‎"))
    except Exception as err:
        print(bstack1llllll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩ‏"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l1l111ll_opy_(fixturedef.argname):
        store[bstack1llllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ‐")] = request.node
    elif bstack111l1l11111_opy_(fixturedef.argname):
        store[bstack1llllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ‑")] = request.node
    if not bstack11l11llll_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.SETUP_FIXTURE, bstack1lll1lll1l1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.SETUP_FIXTURE, bstack1lll1lll1l1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111lll11l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.SETUP_FIXTURE, bstack1lll1lll1l1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.SETUP_FIXTURE, bstack1lll1lll1l1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack11111lll11l_opy_
    try:
        fixture = {
            bstack1llllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ‒"): fixturedef.argname,
            bstack1llllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ–"): bstack11l1l111ll1_opy_(outcome),
            bstack1llllll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ—"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1llllll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭―")]
        if not _111ll1lll1_opy_.get(current_test_item.nodeid, None):
            _111ll1lll1_opy_[current_test_item.nodeid] = {bstack1llllll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ‖"): []}
        _111ll1lll1_opy_[current_test_item.nodeid][bstack1llllll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭‗")].append(fixture)
    except Exception as err:
        logger.debug(bstack1llllll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ‘"), str(err))
if bstack11l1ll1l11_opy_() and bstack11l11llll_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.STEP, bstack1lll1lll1l1_opy_.PRE, request, step)
            return
        try:
            _111ll1lll1_opy_[request.node.nodeid][bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ’")].bstack111l1l1ll_opy_(id(step))
        except Exception as err:
            print(bstack1llllll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ‚"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.STEP, bstack1lll1lll1l1_opy_.POST, request, step, exception)
            return
        try:
            _111ll1lll1_opy_[request.node.nodeid][bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ‛")].bstack11l1111l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1llllll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭“"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.STEP, bstack1lll1lll1l1_opy_.POST, request, step)
            return
        try:
            bstack111lllll11_opy_: bstack11l111l11l_opy_ = _111ll1lll1_opy_[request.node.nodeid][bstack1llllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭”")]
            bstack111lllll11_opy_.bstack11l1111l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1llllll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ„"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111l1l1ll_opy_
        try:
            if not bstack11l11llll_opy_.on() or bstack11111l1l1ll_opy_ != bstack1llllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ‟"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.TEST, bstack1lll1lll1l1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ†"), None)
            if not _111ll1lll1_opy_.get(request.node.nodeid, None):
                _111ll1lll1_opy_[request.node.nodeid] = {}
            bstack111lllll11_opy_ = bstack11l111l11l_opy_.bstack1111lll1ll1_opy_(
                scenario, feature, request.node,
                name=bstack111l1l11lll_opy_(request.node, scenario),
                started_at=bstack1l11l1l11l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1llllll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ‡"),
                tags=bstack111l1l11l11_opy_(feature, scenario),
                bstack11l11111l1_opy_=bstack11l11llll_opy_.bstack11l111llll_opy_(driver) if driver and driver.session_id else {}
            )
            _111ll1lll1_opy_[request.node.nodeid][bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ•")] = bstack111lllll11_opy_
            bstack11111llllll_opy_(bstack111lllll11_opy_.uuid)
            bstack11l11llll_opy_.bstack111llllll1_opy_(bstack1llllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ‣"), bstack111lllll11_opy_)
        except Exception as err:
            print(bstack1llllll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ․"), str(err))
def bstack11111ll111l_opy_(bstack11l111l1l1_opy_):
    if bstack11l111l1l1_opy_ in store[bstack1llllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ‥")]:
        store[bstack1llllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ…")].remove(bstack11l111l1l1_opy_)
def bstack11111llllll_opy_(test_uuid):
    store[bstack1llllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ‧")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack11l11llll_opy_.bstack1111ll1lll1_opy_
def bstack1111l11111l_opy_(item, call, report):
    logger.debug(bstack1llllll_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩ "))
    global bstack11111l1l1ll_opy_
    bstack1l1l1l1ll_opy_ = bstack1l11l1l11l_opy_()
    if hasattr(report, bstack1llllll_opy_ (u"ࠨࡵࡷࡳࡵ࠭ ")):
        bstack1l1l1l1ll_opy_ = bstack11l1l1l1l11_opy_(report.stop)
    elif hasattr(report, bstack1llllll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ‪")):
        bstack1l1l1l1ll_opy_ = bstack11l1l1l1l11_opy_(report.start)
    try:
        if getattr(report, bstack1llllll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ‫"), bstack1llllll_opy_ (u"ࠫࠬ‬")) == bstack1llllll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ‭"):
            logger.debug(bstack1llllll_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ‮").format(getattr(report, bstack1llllll_opy_ (u"ࠧࡸࡪࡨࡲࠬ "), bstack1llllll_opy_ (u"ࠨࠩ‰")).__str__(), bstack11111l1l1ll_opy_))
            if bstack11111l1l1ll_opy_ == bstack1llllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ‱"):
                _111ll1lll1_opy_[item.nodeid][bstack1llllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ′")] = bstack1l1l1l1ll_opy_
                bstack11111ll1ll1_opy_(item, _111ll1lll1_opy_[item.nodeid], bstack1llllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭″"), report, call)
                store[bstack1llllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ‴")] = None
            elif bstack11111l1l1ll_opy_ == bstack1llllll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ‵"):
                bstack111lllll11_opy_ = _111ll1lll1_opy_[item.nodeid][bstack1llllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ‶")]
                bstack111lllll11_opy_.set(hooks=_111ll1lll1_opy_[item.nodeid].get(bstack1llllll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ‷"), []))
                exception, bstack111llll1l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111llll1l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1llllll_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ‸"), bstack1llllll_opy_ (u"ࠪࠫ‹"))]
                bstack111lllll11_opy_.stop(time=bstack1l1l1l1ll_opy_, result=Result(result=getattr(report, bstack1llllll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ›"), bstack1llllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ※")), exception=exception, bstack111llll1l1_opy_=bstack111llll1l1_opy_))
                bstack11l11llll_opy_.bstack111llllll1_opy_(bstack1llllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ‼"), _111ll1lll1_opy_[item.nodeid][bstack1llllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ‽")])
        elif getattr(report, bstack1llllll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭‾"), bstack1llllll_opy_ (u"ࠩࠪ‿")) in [bstack1llllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⁀"), bstack1llllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⁁")]:
            logger.debug(bstack1llllll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⁂").format(getattr(report, bstack1llllll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⁃"), bstack1llllll_opy_ (u"ࠧࠨ⁄")).__str__(), bstack11111l1l1ll_opy_))
            bstack111llll11l_opy_ = item.nodeid + bstack1llllll_opy_ (u"ࠨ࠯ࠪ⁅") + getattr(report, bstack1llllll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⁆"), bstack1llllll_opy_ (u"ࠪࠫ⁇"))
            if getattr(report, bstack1llllll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⁈"), False):
                hook_type = bstack1llllll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⁉") if getattr(report, bstack1llllll_opy_ (u"࠭ࡷࡩࡧࡱࠫ⁊"), bstack1llllll_opy_ (u"ࠧࠨ⁋")) == bstack1llllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⁌") else bstack1llllll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⁍")
                _111ll1lll1_opy_[bstack111llll11l_opy_] = {
                    bstack1llllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⁎"): uuid4().__str__(),
                    bstack1llllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁏"): bstack1l1l1l1ll_opy_,
                    bstack1llllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⁐"): hook_type
                }
            _111ll1lll1_opy_[bstack111llll11l_opy_][bstack1llllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⁑")] = bstack1l1l1l1ll_opy_
            bstack11111ll111l_opy_(_111ll1lll1_opy_[bstack111llll11l_opy_][bstack1llllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁒")])
            bstack11111lllll1_opy_(item, _111ll1lll1_opy_[bstack111llll11l_opy_], bstack1llllll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⁓"), report, call)
            if getattr(report, bstack1llllll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⁔"), bstack1llllll_opy_ (u"ࠪࠫ⁕")) == bstack1llllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⁖"):
                if getattr(report, bstack1llllll_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⁗"), bstack1llllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⁘")) == bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⁙"):
                    bstack111l1l1lll_opy_ = {
                        bstack1llllll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁚"): uuid4().__str__(),
                        bstack1llllll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⁛"): bstack1l11l1l11l_opy_(),
                        bstack1llllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁜"): bstack1l11l1l11l_opy_()
                    }
                    _111ll1lll1_opy_[item.nodeid] = {**_111ll1lll1_opy_[item.nodeid], **bstack111l1l1lll_opy_}
                    bstack11111ll1ll1_opy_(item, _111ll1lll1_opy_[item.nodeid], bstack1llllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⁝"))
                    bstack11111ll1ll1_opy_(item, _111ll1lll1_opy_[item.nodeid], bstack1llllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⁞"), report, call)
    except Exception as err:
        print(bstack1llllll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ "), str(err))
def bstack11111lll1l1_opy_(test, bstack111l1l1lll_opy_, result=None, call=None, bstack11ll1llll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lllll11_opy_ = {
        bstack1llllll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁠"): bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁡")],
        bstack1llllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⁢"): bstack1llllll_opy_ (u"ࠪࡸࡪࡹࡴࠨ⁣"),
        bstack1llllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⁤"): test.name,
        bstack1llllll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⁥"): {
            bstack1llllll_opy_ (u"࠭࡬ࡢࡰࡪࠫ⁦"): bstack1llllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⁧"),
            bstack1llllll_opy_ (u"ࠨࡥࡲࡨࡪ࠭⁨"): inspect.getsource(test.obj)
        },
        bstack1llllll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⁩"): test.name,
        bstack1llllll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⁪"): test.name,
        bstack1llllll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⁫"): bstack1ll1l111l1_opy_.bstack111l11ll11_opy_(test),
        bstack1llllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⁬"): file_path,
        bstack1llllll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⁭"): file_path,
        bstack1llllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁮"): bstack1llllll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⁯"),
        bstack1llllll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⁰"): file_path,
        bstack1llllll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧⁱ"): bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁲")],
        bstack1llllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⁳"): bstack1llllll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⁴"),
        bstack1llllll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⁵"): {
            bstack1llllll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⁶"): test.nodeid
        },
        bstack1llllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⁷"): bstack11l1l11l11l_opy_(test.own_markers)
    }
    if bstack11ll1llll_opy_ in [bstack1llllll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⁸"), bstack1llllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⁹")]:
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠬࡳࡥࡵࡣࠪ⁺")] = {
            bstack1llllll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⁻"): bstack111l1l1lll_opy_.get(bstack1llllll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⁼"), [])
        }
    if bstack11ll1llll_opy_ == bstack1llllll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⁽"):
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⁾")] = bstack1llllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫⁿ")
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ₀")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ₁")]
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ₂")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ₃")]
    if result:
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₄")] = result.outcome
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ₅")] = result.duration * 1000
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ₆")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₇")]
        if result.failed:
            bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ₈")] = bstack11l11llll_opy_.bstack1111l1llll_opy_(call.excinfo.typename)
            bstack111lllll11_opy_[bstack1llllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ₉")] = bstack11l11llll_opy_.bstack1111lll1111_opy_(call.excinfo, result)
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭₊")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ₋")]
    if outcome:
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ₌")] = bstack11l1l111ll1_opy_(outcome)
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ₍")] = 0
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₎")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₏")]
        if bstack111lllll11_opy_[bstack1llllll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ₐ")] == bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧₑ"):
            bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧₒ")] = bstack1llllll_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪₓ")  # bstack11111lll111_opy_
            bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫₔ")] = [{bstack1llllll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧₕ"): [bstack1llllll_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩₖ")]}]
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬₗ")] = bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ₘ")]
    return bstack111lllll11_opy_
def bstack11111ll11l1_opy_(test, bstack111ll11l11_opy_, bstack11ll1llll_opy_, result, call, outcome, bstack1111l111l11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫₙ")]
    hook_name = bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬₚ")]
    hook_data = {
        bstack1llllll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨₛ"): bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠫࡺࡻࡩࡥࠩₜ")],
        bstack1llllll_opy_ (u"ࠬࡺࡹࡱࡧࠪ₝"): bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ₞"),
        bstack1llllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ₟"): bstack1llllll_opy_ (u"ࠨࡽࢀࠫ₠").format(bstack111l1l1l111_opy_(hook_name)),
        bstack1llllll_opy_ (u"ࠩࡥࡳࡩࡿࠧ₡"): {
            bstack1llllll_opy_ (u"ࠪࡰࡦࡴࡧࠨ₢"): bstack1llllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ₣"),
            bstack1llllll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ₤"): None
        },
        bstack1llllll_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ₥"): test.name,
        bstack1llllll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ₦"): bstack1ll1l111l1_opy_.bstack111l11ll11_opy_(test, hook_name),
        bstack1llllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ₧"): file_path,
        bstack1llllll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ₨"): file_path,
        bstack1llllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₩"): bstack1llllll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ₪"),
        bstack1llllll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ₫"): file_path,
        bstack1llllll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ€"): bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ₭")],
        bstack1llllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ₮"): bstack1llllll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ₯") if bstack11111l1l1ll_opy_ == bstack1llllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ₰") else bstack1llllll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ₱"),
        bstack1llllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ₲"): hook_type
    }
    bstack1111lllll1l_opy_ = bstack111l1l111l_opy_(_111ll1lll1_opy_.get(test.nodeid, None))
    if bstack1111lllll1l_opy_:
        hook_data[bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ₳")] = bstack1111lllll1l_opy_
    if result:
        hook_data[bstack1llllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₴")] = result.outcome
        hook_data[bstack1llllll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ₵")] = result.duration * 1000
        hook_data[bstack1llllll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₶")] = bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ₷")]
        if result.failed:
            hook_data[bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ₸")] = bstack11l11llll_opy_.bstack1111l1llll_opy_(call.excinfo.typename)
            hook_data[bstack1llllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭₹")] = bstack11l11llll_opy_.bstack1111lll1111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1llllll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭₺")] = bstack11l1l111ll1_opy_(outcome)
        hook_data[bstack1llllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ₻")] = 100
        hook_data[bstack1llllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₼")] = bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₽")]
        if hook_data[bstack1llllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ₾")] == bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ₿"):
            hook_data[bstack1llllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⃀")] = bstack1llllll_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⃁")  # bstack11111lll111_opy_
            hook_data[bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⃂")] = [{bstack1llllll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⃃"): [bstack1llllll_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⃄")]}]
    if bstack1111l111l11_opy_:
        hook_data[bstack1llllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⃅")] = bstack1111l111l11_opy_.result
        hook_data[bstack1llllll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⃆")] = bstack11l1l1l1ll1_opy_(bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⃇")], bstack111ll11l11_opy_[bstack1llllll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃈")])
        hook_data[bstack1llllll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⃉")] = bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⃊")]
        if hook_data[bstack1llllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⃋")] == bstack1llllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⃌"):
            hook_data[bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⃍")] = bstack11l11llll_opy_.bstack1111l1llll_opy_(bstack1111l111l11_opy_.exception_type)
            hook_data[bstack1llllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⃎")] = [{bstack1llllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⃏"): bstack11l1ll1ll1l_opy_(bstack1111l111l11_opy_.exception)}]
    return hook_data
def bstack11111ll1ll1_opy_(test, bstack111l1l1lll_opy_, bstack11ll1llll_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1llllll_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ⃐").format(bstack11ll1llll_opy_))
    bstack111lllll11_opy_ = bstack11111lll1l1_opy_(test, bstack111l1l1lll_opy_, result, call, bstack11ll1llll_opy_, outcome)
    driver = getattr(test, bstack1llllll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⃑"), None)
    if bstack11ll1llll_opy_ == bstack1llllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦ⃒ࠪ") and driver:
        bstack111lllll11_opy_[bstack1llllll_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴ⃓ࠩ")] = bstack11l11llll_opy_.bstack11l111llll_opy_(driver)
    if bstack11ll1llll_opy_ == bstack1llllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⃔"):
        bstack11ll1llll_opy_ = bstack1llllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⃕")
    bstack111lll11ll_opy_ = {
        bstack1llllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⃖"): bstack11ll1llll_opy_,
        bstack1llllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⃗"): bstack111lllll11_opy_
    }
    bstack11l11llll_opy_.bstack1lll1l1ll_opy_(bstack111lll11ll_opy_)
    if bstack11ll1llll_opy_ == bstack1llllll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥ⃘ࠩ"):
        threading.current_thread().bstackTestMeta = {bstack1llllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴ⃙ࠩ"): bstack1llllll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪ⃚ࠫ")}
    elif bstack11ll1llll_opy_ == bstack1llllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⃛"):
        threading.current_thread().bstackTestMeta = {bstack1llllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⃜"): getattr(result, bstack1llllll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⃝"), bstack1llllll_opy_ (u"ࠧࠨ⃞"))}
def bstack11111lllll1_opy_(test, bstack111l1l1lll_opy_, bstack11ll1llll_opy_, result=None, call=None, outcome=None, bstack1111l111l11_opy_=None):
    logger.debug(bstack1llllll_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⃟").format(bstack11ll1llll_opy_))
    hook_data = bstack11111ll11l1_opy_(test, bstack111l1l1lll_opy_, bstack11ll1llll_opy_, result, call, outcome, bstack1111l111l11_opy_)
    bstack111lll11ll_opy_ = {
        bstack1llllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⃠"): bstack11ll1llll_opy_,
        bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ⃡"): hook_data
    }
    bstack11l11llll_opy_.bstack1lll1l1ll_opy_(bstack111lll11ll_opy_)
def bstack111l1l111l_opy_(bstack111l1l1lll_opy_):
    if not bstack111l1l1lll_opy_:
        return None
    if bstack111l1l1lll_opy_.get(bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⃢"), None):
        return getattr(bstack111l1l1lll_opy_[bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⃣")], bstack1llllll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⃤"), None)
    return bstack111l1l1lll_opy_.get(bstack1llllll_opy_ (u"ࠧࡶࡷ࡬ࡨ⃥ࠬ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.LOG, bstack1lll1lll1l1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_.LOG, bstack1lll1lll1l1_opy_.POST, request, caplog)
        return # skip all existing bstack11111lll11l_opy_
    try:
        if not bstack11l11llll_opy_.on():
            return
        places = [bstack1llllll_opy_ (u"ࠨࡵࡨࡸࡺࡶ⃦ࠧ"), bstack1llllll_opy_ (u"ࠩࡦࡥࡱࡲࠧ⃧"), bstack1llllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ⃨ࠬ")]
        logs = []
        for bstack11111ll1l1l_opy_ in places:
            records = caplog.get_records(bstack11111ll1l1l_opy_)
            bstack11111l1ll1l_opy_ = bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃩") if bstack11111ll1l1l_opy_ == bstack1llllll_opy_ (u"ࠬࡩࡡ࡭࡮⃪ࠪ") else bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ⃫࠭")
            bstack1111l111lll_opy_ = request.node.nodeid + (bstack1llllll_opy_ (u"ࠧࠨ⃬") if bstack11111ll1l1l_opy_ == bstack1llllll_opy_ (u"ࠨࡥࡤࡰࡱ⃭࠭") else bstack1llllll_opy_ (u"ࠩ࠰⃮ࠫ") + bstack11111ll1l1l_opy_)
            test_uuid = bstack111l1l111l_opy_(_111ll1lll1_opy_.get(bstack1111l111lll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll11ll11l_opy_(record.message):
                    continue
                logs.append({
                    bstack1llllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ⃯࠭"): bstack11l1llll1ll_opy_(record.created).isoformat() + bstack1llllll_opy_ (u"ࠫ࡟࠭⃰"),
                    bstack1llllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⃱"): record.levelname,
                    bstack1llllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⃲"): record.message,
                    bstack11111l1ll1l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack11l11llll_opy_.bstack11lll11l1l_opy_(logs)
    except Exception as err:
        print(bstack1llllll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ⃳"), str(err))
def bstack1l1lll1l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1111l111_opy_
    bstack1ll11l1l11_opy_ = bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ⃴"), None) and bstack1lll11l1_opy_(
            threading.current_thread(), bstack1llllll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⃵"), None)
    bstack1l11ll1lll_opy_ = getattr(driver, bstack1llllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⃶"), None) != None and getattr(driver, bstack1llllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⃷"), None) == True
    if sequence == bstack1llllll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⃸") and driver != None:
      if not bstack1l1111l111_opy_ and bstack1l1lllll1l1_opy_() and bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃹") in CONFIG and CONFIG[bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃺")] == True and bstack1l1llll1_opy_.bstack11lll111l_opy_(driver_command) and (bstack1l11ll1lll_opy_ or bstack1ll11l1l11_opy_) and not bstack1llll1ll11_opy_(args):
        try:
          bstack1l1111l111_opy_ = True
          logger.debug(bstack1llllll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ⃻").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1llllll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ⃼").format(str(err)))
        bstack1l1111l111_opy_ = False
    if sequence == bstack1llllll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⃽"):
        if driver_command == bstack1llllll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ⃾"):
            bstack11l11llll_opy_.bstack1lll11ll11_opy_({
                bstack1llllll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⃿"): response[bstack1llllll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ℀")],
                bstack1llllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ℁"): store[bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬℂ")]
            })
def bstack1l111ll1_opy_():
    global bstack1l11l1l111_opy_
    bstack1llllll1ll_opy_.bstack11llll1ll1_opy_()
    logging.shutdown()
    bstack11l11llll_opy_.bstack111ll1l1l1_opy_()
    for driver in bstack1l11l1l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111l111ll1_opy_(*args):
    global bstack1l11l1l111_opy_
    bstack11l11llll_opy_.bstack111ll1l1l1_opy_()
    for driver in bstack1l11l1l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll1ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack11llll11l_opy_=bstack1llll1111l_opy_)
def bstack11ll1ll1l_opy_(self, *args, **kwargs):
    bstack1lllll1ll1_opy_ = bstack1llllll11l_opy_(self, *args, **kwargs)
    bstack1llll1ll1l_opy_ = getattr(threading.current_thread(), bstack1llllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ℃"), None)
    if bstack1llll1ll1l_opy_ and bstack1llll1ll1l_opy_.get(bstack1llllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ℄"), bstack1llllll_opy_ (u"ࠫࠬ℅")) == bstack1llllll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭℆"):
        bstack11l11llll_opy_.bstack11l111ll_opy_(self)
    return bstack1lllll1ll1_opy_
@measure(event_name=EVENTS.bstack11ll1l11l_opy_, stage=STAGE.bstack1lll11l1ll_opy_, bstack11llll11l_opy_=bstack1llll1111l_opy_)
def bstack1l1llllll1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
    if bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪℇ")):
        return
    bstack1l1ll1l1l1_opy_.bstack1ll1l11ll1_opy_(bstack1llllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ℈"), True)
    global bstack1ll11ll1l1_opy_
    global bstack11111l1l1_opy_
    bstack1ll11ll1l1_opy_ = framework_name
    logger.info(bstack1lll1111ll_opy_.format(bstack1ll11ll1l1_opy_.split(bstack1llllll_opy_ (u"ࠨ࠯ࠪ℉"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lllll1l1_opy_():
            Service.start = bstack1ll1lllll_opy_
            Service.stop = bstack11l1ll1ll_opy_
            webdriver.Remote.get = bstack1l1llll11_opy_
            webdriver.Remote.__init__ = bstack1lll11ll1_opy_
            if not isinstance(os.getenv(bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪℊ")), str):
                return
            WebDriver.close = bstack1l11l11111_opy_
            WebDriver.quit = bstack11llll111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack11l11llll_opy_.on():
            webdriver.Remote.__init__ = bstack11ll1ll1l_opy_
        bstack11111l1l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1llllll_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨℋ")):
        bstack11111l1l1_opy_ = eval(os.environ.get(bstack1llllll_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩℌ")))
    if not bstack11111l1l1_opy_:
        bstack11lll1ll1l_opy_(bstack1llllll_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢℍ"), bstack11ll111l11_opy_)
    if bstack1111ll1l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._11l1l1l111_opy_ = bstack11l1l11l11_opy_
        except Exception as e:
            logger.error(bstack11l1lll1ll_opy_.format(str(e)))
    if bstack1llllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ℎ") in str(framework_name).lower():
        if not bstack1l1lllll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1111lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l111_opy_
            Config.getoption = bstack1l1ll111l1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1l1l11ll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll111ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack11llll11l_opy_=bstack1llll1111l_opy_)
def bstack11llll111_opy_(self):
    global bstack1ll11ll1l1_opy_
    global bstack1ll11ll111_opy_
    global bstack11l1l11l_opy_
    try:
        if bstack1llllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧℏ") in bstack1ll11ll1l1_opy_ and self.session_id != None and bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬℐ"), bstack1llllll_opy_ (u"ࠩࠪℑ")) != bstack1llllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫℒ"):
            bstack11l1l11ll1_opy_ = bstack1llllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫℓ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1llllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ℔")
            bstack1l1111111l_opy_(logger, True)
            if self != None:
                bstack1ll1l1l1l1_opy_(self, bstack11l1l11ll1_opy_, bstack1llllll_opy_ (u"࠭ࠬࠡࠩℕ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1ll1l11_opy_(bstack1lll111ll1l_opy_):
            item = store.get(bstack1llllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ№"), None)
            if item is not None and bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ℗"), None):
                bstack1lll1111l_opy_.bstack1l1ll1l1_opy_(self, bstack1ll1ll11l_opy_, logger, item)
        threading.current_thread().testStatus = bstack1llllll_opy_ (u"ࠩࠪ℘")
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦℙ") + str(e))
    bstack11l1l11l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l11l11l1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack11llll11l_opy_=bstack1llll1111l_opy_)
def bstack1lll11ll1_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll11ll1ll_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll11ll111_opy_
    global bstack1llll1111l_opy_
    global bstack11l1l1l1_opy_
    global bstack1ll11ll1l1_opy_
    global bstack1llllll11l_opy_
    global bstack1l11l1l111_opy_
    global bstack1l1lll111l_opy_
    global bstack1l1l1l1111_opy_
    global bstack1ll1ll11l_opy_
    CONFIG[bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ℚ")] = str(bstack1ll11ll1l1_opy_) + str(__version__)
    command_executor = bstack1l1l1ll11_opy_(bstack1l1lll111l_opy_, CONFIG)
    logger.debug(bstack1l1llllll_opy_.format(command_executor))
    proxy = bstack1111l11ll_opy_(CONFIG, proxy)
    bstack1ll111ll11_opy_ = 0
    try:
        if bstack11l1l1l1_opy_ is True:
            bstack1ll111ll11_opy_ = int(os.environ.get(bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬℛ")))
    except:
        bstack1ll111ll11_opy_ = 0
    bstack1l1l11lll1_opy_ = bstack1ll1111111_opy_(CONFIG, bstack1ll111ll11_opy_)
    logger.debug(bstack1l1l11l1l1_opy_.format(str(bstack1l1l11lll1_opy_)))
    bstack1ll1ll11l_opy_ = CONFIG.get(bstack1llllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩℜ"))[bstack1ll111ll11_opy_]
    if bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫℝ") in CONFIG and CONFIG[bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ℞")]:
        bstack11ll1111l1_opy_(bstack1l1l11lll1_opy_, bstack1l1l1l1111_opy_)
    if bstack11111l11l_opy_.bstack1lllll11l_opy_(CONFIG, bstack1ll111ll11_opy_) and bstack11111l11l_opy_.bstack1lll1ll11_opy_(bstack1l1l11lll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1ll1l11_opy_(bstack1lll111ll1l_opy_):
            bstack11111l11l_opy_.set_capabilities(bstack1l1l11lll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll11lll1_opy_ = bstack1l1ll1ll11_opy_(desired_capabilities)
        bstack1ll11lll1_opy_[bstack1llllll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ℟")] = bstack1ll11ll1l_opy_(CONFIG)
        bstack1l111l1111_opy_ = bstack1ll1111111_opy_(bstack1ll11lll1_opy_)
        if bstack1l111l1111_opy_:
            bstack1l1l11lll1_opy_ = update(bstack1l111l1111_opy_, bstack1l1l11lll1_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1l11l1_opy_(options, bstack1l1l11lll1_opy_)
    if not options:
        options = bstack1l11lll1ll_opy_(bstack1l1l11lll1_opy_)
    if proxy and bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ℠")):
        options.proxy(proxy)
    if options and bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ℡")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1llll1ll1_opy_() < version.parse(bstack1llllll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ™")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1l11lll1_opy_)
    logger.info(bstack11lllllll1_opy_)
    bstack1llll1l1_opy_.end(EVENTS.bstack11ll1l11l_opy_.value, EVENTS.bstack11ll1l11l_opy_.value + bstack1llllll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ℣"),
                               EVENTS.bstack11ll1l11l_opy_.value + bstack1llllll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧℤ"), True, None)
    if bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ℥")):
        bstack1llllll11l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨΩ")):
        bstack1llllll11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1ll11ll1ll_opy_=bstack1ll11ll1ll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ℧")):
        bstack1llllll11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll11ll1ll_opy_=bstack1ll11ll1ll_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1llllll11l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll11ll1ll_opy_=bstack1ll11ll1ll_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack111ll1ll1_opy_ = bstack1llllll_opy_ (u"ࠫࠬℨ")
        if bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭℩")):
            bstack111ll1ll1_opy_ = self.caps.get(bstack1llllll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨK"))
        else:
            bstack111ll1ll1_opy_ = self.capabilities.get(bstack1llllll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢÅ"))
        if bstack111ll1ll1_opy_:
            bstack11lll1ll11_opy_(bstack111ll1ll1_opy_)
            if bstack1llll1ll1_opy_() <= version.parse(bstack1llllll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨℬ")):
                self.command_executor._url = bstack1llllll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥℭ") + bstack1l1lll111l_opy_ + bstack1llllll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ℮")
            else:
                self.command_executor._url = bstack1llllll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨℯ") + bstack111ll1ll1_opy_ + bstack1llllll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨℰ")
            logger.debug(bstack11lllll1l1_opy_.format(bstack111ll1ll1_opy_))
        else:
            logger.debug(bstack1ll1l11l_opy_.format(bstack1llllll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢℱ")))
    except Exception as e:
        logger.debug(bstack1ll1l11l_opy_.format(e))
    bstack1ll11ll111_opy_ = self.session_id
    if bstack1llllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧℲ") in bstack1ll11ll1l1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬℳ"), None)
        if item:
            bstack11111llll11_opy_ = getattr(item, bstack1llllll_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧℴ"), False)
            if not getattr(item, bstack1llllll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫℵ"), None) and bstack11111llll11_opy_:
                setattr(store[bstack1llllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨℶ")], bstack1llllll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ℷ"), self)
        bstack1llll1ll1l_opy_ = getattr(threading.current_thread(), bstack1llllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧℸ"), None)
        if bstack1llll1ll1l_opy_ and bstack1llll1ll1l_opy_.get(bstack1llllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧℹ"), bstack1llllll_opy_ (u"ࠨࠩ℺")) == bstack1llllll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ℻"):
            bstack11l11llll_opy_.bstack11l111ll_opy_(self)
    bstack1l11l1l111_opy_.append(self)
    if bstack1llllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ℼ") in CONFIG and bstack1llllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩℽ") in CONFIG[bstack1llllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨℾ")][bstack1ll111ll11_opy_]:
        bstack1llll1111l_opy_ = CONFIG[bstack1llllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩℿ")][bstack1ll111ll11_opy_][bstack1llllll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⅀")]
    logger.debug(bstack1lll1ll1l_opy_.format(bstack1ll11ll111_opy_))
@measure(event_name=EVENTS.bstack1l11lll1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_, bstack11llll11l_opy_=bstack1llll1111l_opy_)
def bstack1l1llll11_opy_(self, url):
    global bstack11ll11l1l_opy_
    global CONFIG
    try:
        bstack111lll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111llll11_opy_.format(str(err)))
    try:
        bstack11ll11l1l_opy_(self, url)
    except Exception as e:
        try:
            bstack11l111l11_opy_ = str(e)
            if any(err_msg in bstack11l111l11_opy_ for err_msg in bstack1l11llll_opy_):
                bstack111lll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111llll11_opy_.format(str(err)))
        raise e
def bstack111l111ll_opy_(item, when):
    global bstack11l11l1ll1_opy_
    try:
        bstack11l11l1ll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l1l11ll_opy_(item, call, rep):
    global bstack1l1l1ll1l1_opy_
    global bstack1l11l1l111_opy_
    name = bstack1llllll_opy_ (u"ࠨࠩ⅁")
    try:
        if rep.when == bstack1llllll_opy_ (u"ࠩࡦࡥࡱࡲࠧ⅂"):
            bstack1ll11ll111_opy_ = threading.current_thread().bstackSessionId
            bstack11111l1ll11_opy_ = item.config.getoption(bstack1llllll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⅃"))
            try:
                if (str(bstack11111l1ll11_opy_).lower() != bstack1llllll_opy_ (u"ࠫࡹࡸࡵࡦࠩ⅄")):
                    name = str(rep.nodeid)
                    bstack1l11ll1l1_opy_ = bstack1111l111_opy_(bstack1llllll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ⅅ"), name, bstack1llllll_opy_ (u"࠭ࠧⅆ"), bstack1llllll_opy_ (u"ࠧࠨⅇ"), bstack1llllll_opy_ (u"ࠨࠩⅈ"), bstack1llllll_opy_ (u"ࠩࠪⅉ"))
                    os.environ[bstack1llllll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⅊")] = name
                    for driver in bstack1l11l1l111_opy_:
                        if bstack1ll11ll111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack1llllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⅋").format(str(e)))
            try:
                bstack1l1l1llll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1llllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⅌"):
                    status = bstack1llllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⅍") if rep.outcome.lower() == bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧⅎ") else bstack1llllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⅏")
                    reason = bstack1llllll_opy_ (u"ࠩࠪ⅐")
                    if status == bstack1llllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⅑"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1llllll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ⅒") if status == bstack1llllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⅓") else bstack1llllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⅔")
                    data = name + bstack1llllll_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ⅕") if status == bstack1llllll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⅖") else name + bstack1llllll_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ⅗") + reason
                    bstack11l11lll1l_opy_ = bstack1111l111_opy_(bstack1llllll_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⅘"), bstack1llllll_opy_ (u"ࠫࠬ⅙"), bstack1llllll_opy_ (u"ࠬ࠭⅚"), bstack1llllll_opy_ (u"࠭ࠧ⅛"), level, data)
                    for driver in bstack1l11l1l111_opy_:
                        if bstack1ll11ll111_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11lll1l_opy_)
            except Exception as e:
                logger.debug(bstack1llllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⅜").format(str(e)))
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ⅝").format(str(e)))
    bstack1l1l1ll1l1_opy_(item, call, rep)
notset = Notset()
def bstack1l1ll111l1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11l11l1l1_opy_
    if str(name).lower() == bstack1llllll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ⅞"):
        return bstack1llllll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ⅟")
    else:
        return bstack11l11l1l1_opy_(self, name, default, skip)
def bstack11l1l11l11_opy_(self):
    global CONFIG
    global bstack1l111l11_opy_
    try:
        proxy = bstack1l111ll11l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1llllll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩⅠ")):
                proxies = bstack11l11lllll_opy_(proxy, bstack1l1l1ll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l11111l1l_opy_ = proxies.popitem()
                    if bstack1llllll_opy_ (u"ࠧࡀ࠯࠰ࠤⅡ") in bstack1l11111l1l_opy_:
                        return bstack1l11111l1l_opy_
                    else:
                        return bstack1llllll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢⅢ") + bstack1l11111l1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1llllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦⅣ").format(str(e)))
    return bstack1l111l11_opy_(self)
def bstack1111ll1l1_opy_():
    return (bstack1llllll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫⅤ") in CONFIG or bstack1llllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ⅵ") in CONFIG) and bstack11ll1l1l11_opy_() and bstack1llll1ll1_opy_() >= version.parse(
        bstack11ll11111_opy_)
def bstack1ll1ll1111_opy_(self,
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
    global bstack1llll1111l_opy_
    global bstack11l1l1l1_opy_
    global bstack1ll11ll1l1_opy_
    CONFIG[bstack1llllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬⅦ")] = str(bstack1ll11ll1l1_opy_) + str(__version__)
    bstack1ll111ll11_opy_ = 0
    try:
        if bstack11l1l1l1_opy_ is True:
            bstack1ll111ll11_opy_ = int(os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫⅧ")))
    except:
        bstack1ll111ll11_opy_ = 0
    CONFIG[bstack1llllll_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦⅨ")] = True
    bstack1l1l11lll1_opy_ = bstack1ll1111111_opy_(CONFIG, bstack1ll111ll11_opy_)
    logger.debug(bstack1l1l11l1l1_opy_.format(str(bstack1l1l11lll1_opy_)))
    if CONFIG.get(bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪⅩ")):
        bstack11ll1111l1_opy_(bstack1l1l11lll1_opy_, bstack1l1l1l1111_opy_)
    if bstack1llllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅪ") in CONFIG and bstack1llllll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ⅻ") in CONFIG[bstack1llllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬⅬ")][bstack1ll111ll11_opy_]:
        bstack1llll1111l_opy_ = CONFIG[bstack1llllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ⅽ")][bstack1ll111ll11_opy_][bstack1llllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩⅮ")]
    import urllib
    import json
    if bstack1llllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩⅯ") in CONFIG and str(CONFIG[bstack1llllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪⅰ")]).lower() != bstack1llllll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ⅱ"):
        bstack111l11ll1_opy_ = bstack1ll1lll11_opy_()
        bstack1l1l11ll1_opy_ = bstack111l11ll1_opy_ + urllib.parse.quote(json.dumps(bstack1l1l11lll1_opy_))
    else:
        bstack1l1l11ll1_opy_ = bstack1llllll_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪⅲ") + urllib.parse.quote(json.dumps(bstack1l1l11lll1_opy_))
    browser = self.connect(bstack1l1l11ll1_opy_)
    return browser
def bstack1l1l1lll_opy_():
    global bstack11111l1l1_opy_
    global bstack1ll11ll1l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11ll11l1_opy_
        if not bstack1l1lllll1l1_opy_():
            global bstack1ll11ll11_opy_
            if not bstack1ll11ll11_opy_:
                from bstack_utils.helper import bstack1ll1lll111_opy_, bstack1111ll1ll_opy_
                bstack1ll11ll11_opy_ = bstack1ll1lll111_opy_()
                bstack1111ll1ll_opy_(bstack1ll11ll1l1_opy_)
            BrowserType.connect = bstack1l11ll11l1_opy_
            return
        BrowserType.launch = bstack1ll1ll1111_opy_
        bstack11111l1l1_opy_ = True
    except Exception as e:
        pass
def bstack11111llll1l_opy_():
    global CONFIG
    global bstack11l1l11lll_opy_
    global bstack1l1lll111l_opy_
    global bstack1l1l1l1111_opy_
    global bstack11l1l1l1_opy_
    global bstack1ll1l111ll_opy_
    CONFIG = json.loads(os.environ.get(bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨⅳ")))
    bstack11l1l11lll_opy_ = eval(os.environ.get(bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫⅴ")))
    bstack1l1lll111l_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫⅵ"))
    bstack11l1l111l1_opy_(CONFIG, bstack11l1l11lll_opy_)
    bstack1ll1l111ll_opy_ = bstack1llllll1ll_opy_.bstack11ll11ll_opy_(CONFIG, bstack1ll1l111ll_opy_)
    if cli.bstack1l1lll11ll_opy_():
        bstack11l1l11ll_opy_.invoke(bstack111ll1ll_opy_.CONNECT, bstack1ll1lllll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬⅶ"), bstack1llllll_opy_ (u"࠭࠰ࠨⅷ")))
        cli.bstack1llllll1lll_opy_(cli_context.platform_index)
        cli.bstack1ll1lllllll_opy_(bstack1l1l1ll11_opy_(bstack1l1lll111l_opy_, CONFIG), cli_context.platform_index, bstack1l11lll1ll_opy_)
        cli.bstack1lll1l1ll1l_opy_()
        logger.debug(bstack1llllll_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨⅸ") + str(cli_context.platform_index) + bstack1llllll_opy_ (u"ࠣࠤⅹ"))
        return # skip all existing bstack11111lll11l_opy_
    global bstack1llllll11l_opy_
    global bstack11l1l11l_opy_
    global bstack1l1llll1ll_opy_
    global bstack111111l1_opy_
    global bstack1l1l1l111_opy_
    global bstack11ll11ll1_opy_
    global bstack1ll111l111_opy_
    global bstack11ll11l1l_opy_
    global bstack1l111l11_opy_
    global bstack11l11l1l1_opy_
    global bstack11l11l1ll1_opy_
    global bstack1l1l1ll1l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1llllll11l_opy_ = webdriver.Remote.__init__
        bstack11l1l11l_opy_ = WebDriver.quit
        bstack1ll111l111_opy_ = WebDriver.close
        bstack11ll11l1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1llllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬⅺ") in CONFIG or bstack1llllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧⅻ") in CONFIG) and bstack11ll1l1l11_opy_():
        if bstack1llll1ll1_opy_() < version.parse(bstack11ll11111_opy_):
            logger.error(bstack1l1l11ll11_opy_.format(bstack1llll1ll1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l111l11_opy_ = RemoteConnection._11l1l1l111_opy_
            except Exception as e:
                logger.error(bstack11l1lll1ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11l11l1l1_opy_ = Config.getoption
        from _pytest import runner
        bstack11l11l1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11lll1lll1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1l1ll1l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬⅼ"))
    bstack1l1l1l1111_opy_ = CONFIG.get(bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩⅽ"), {}).get(bstack1llllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨⅾ"))
    bstack11l1l1l1_opy_ = True
    bstack1l1llllll1_opy_(bstack1lll1l111l_opy_)
if (bstack11l1ll111ll_opy_()):
    bstack11111llll1l_opy_()
@bstack111l1l1111_opy_(class_method=False)
def bstack11111ll11ll_opy_(hook_name, event, bstack1l11l1l1111_opy_=None):
    if hook_name not in [bstack1llllll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨⅿ"), bstack1llllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬↀ"), bstack1llllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨↁ"), bstack1llllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬↂ"), bstack1llllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩↃ"), bstack1llllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ↄ"), bstack1llllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬↅ"), bstack1llllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩↆ")]:
        return
    node = store[bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬↇ")]
    if hook_name in [bstack1llllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨↈ"), bstack1llllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ↉")]:
        node = store[bstack1llllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ↊")]
    elif hook_name in [bstack1llllll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ↋"), bstack1llllll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ↌")]:
        node = store[bstack1llllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬ↍")]
    hook_type = bstack111l1l1l11l_opy_(hook_name)
    if event == bstack1llllll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ↎"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_[hook_type], bstack1lll1lll1l1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111ll11l11_opy_ = {
            bstack1llllll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ↏"): uuid,
            bstack1llllll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ←"): bstack1l11l1l11l_opy_(),
            bstack1llllll_opy_ (u"ࠫࡹࡿࡰࡦࠩ↑"): bstack1llllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ→"),
            bstack1llllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ↓"): hook_type,
            bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ↔"): hook_name
        }
        store[bstack1llllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ↕")].append(uuid)
        bstack1111l1111l1_opy_ = node.nodeid
        if hook_type == bstack1llllll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ↖"):
            if not _111ll1lll1_opy_.get(bstack1111l1111l1_opy_, None):
                _111ll1lll1_opy_[bstack1111l1111l1_opy_] = {bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ↗"): []}
            _111ll1lll1_opy_[bstack1111l1111l1_opy_][bstack1llllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ↘")].append(bstack111ll11l11_opy_[bstack1llllll_opy_ (u"ࠬࡻࡵࡪࡦࠪ↙")])
        _111ll1lll1_opy_[bstack1111l1111l1_opy_ + bstack1llllll_opy_ (u"࠭࠭ࠨ↚") + hook_name] = bstack111ll11l11_opy_
        bstack11111lllll1_opy_(node, bstack111ll11l11_opy_, bstack1llllll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ↛"))
    elif event == bstack1llllll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ↜"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lllll1lll1_opy_[hook_type], bstack1lll1lll1l1_opy_.POST, node, None, bstack1l11l1l1111_opy_)
            return
        bstack111llll11l_opy_ = node.nodeid + bstack1llllll_opy_ (u"ࠩ࠰ࠫ↝") + hook_name
        _111ll1lll1_opy_[bstack111llll11l_opy_][bstack1llllll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ↞")] = bstack1l11l1l11l_opy_()
        bstack11111ll111l_opy_(_111ll1lll1_opy_[bstack111llll11l_opy_][bstack1llllll_opy_ (u"ࠫࡺࡻࡩࡥࠩ↟")])
        bstack11111lllll1_opy_(node, _111ll1lll1_opy_[bstack111llll11l_opy_], bstack1llllll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ↠"), bstack1111l111l11_opy_=bstack1l11l1l1111_opy_)
def bstack11111l1lll1_opy_():
    global bstack11111l1l1ll_opy_
    if bstack11l1ll1l11_opy_():
        bstack11111l1l1ll_opy_ = bstack1llllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ↡")
    else:
        bstack11111l1l1ll_opy_ = bstack1llllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ↢")
@bstack11l11llll_opy_.bstack1111ll1lll1_opy_
def bstack1111l111l1l_opy_():
    bstack11111l1lll1_opy_()
    if cli.is_running():
        try:
            bstack11l11ll11ll_opy_(bstack11111ll11ll_opy_)
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ↣").format(e))
        return
    if bstack11ll1l1l11_opy_():
        bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
        bstack1llllll_opy_ (u"ࠩࠪࠫࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡂࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡨࡧࡷࡷࠥࡻࡳࡦࡦࠣࡪࡴࡸࠠࡢ࠳࠴ࡽࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠭ࡸࡴࡤࡴࡵ࡯࡮ࡨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡲࡶࡰࠣࡦࡪࡩࡡࡶࡵࡨࠤ࡮ࡺࠠࡪࡵࠣࡴࡦࡺࡣࡩࡧࡧࠤ࡮ࡴࠠࡢࠢࡧ࡭࡫࡬ࡥࡳࡧࡱࡸࠥࡶࡲࡰࡥࡨࡷࡸࠦࡩࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡸࡷࠥࡽࡥࠡࡰࡨࡩࡩࠦࡴࡰࠢࡸࡷࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࡑࡣࡷࡧ࡭࠮ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡪࡤࡲࡩࡲࡥࡳࠫࠣࡪࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ↤")
        if bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ↥")):
            if CONFIG.get(bstack1llllll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ↦")) is not None and int(CONFIG[bstack1llllll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ↧")]) > 1:
                bstack1ll1l1l1ll_opy_(bstack1l1lll1l1_opy_)
            return
        bstack1ll1l1l1ll_opy_(bstack1l1lll1l1_opy_)
    try:
        bstack11l11ll11ll_opy_(bstack11111ll11ll_opy_)
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ↨").format(e))
bstack1111l111l1l_opy_()