# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1ll1l111ll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1lllllll_opy_, bstack1lllllll1_opy_, update, bstack1ll11l1l11_opy_,
                                       bstack1l1ll1ll1l_opy_, bstack11ll1lllll_opy_, bstack1l111lll11_opy_, bstack11l1l1ll1_opy_,
                                       bstack1111ll11l_opy_, bstack1l1l1l1ll_opy_, bstack1l111l1l1l_opy_,
                                       bstack1l1l1ll111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack111lll1ll_opy_)
from browserstack_sdk.bstack1l1l1lllll_opy_ import bstack1llll1l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1111ll111_opy_
from bstack_utils.capture import bstack111ll1lll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11llll111_opy_, bstack11l1l1111_opy_, bstack1ll11ll11l_opy_, \
    bstack111lllll_opy_
from bstack_utils.helper import bstack1ll11l1l1l_opy_, bstack11l1l1ll1l1_opy_, bstack111l1lll11_opy_, bstack1l1l1l1l1l_opy_, bstack1l1ll11l1ll_opy_, bstack1llllllll1_opy_, \
    bstack11l1l1l1l11_opy_, \
    bstack11l111111l1_opy_, bstack11l1ll1ll_opy_, bstack11llll1l1l_opy_, bstack11l11111111_opy_, bstack111ll111_opy_, Notset, \
    bstack1ll1lll1ll_opy_, bstack11l11l11lll_opy_, bstack11l1l1l11l1_opy_, Result, bstack11l111l1ll1_opy_, bstack11l11l1lll1_opy_, bstack111l1ll1l1_opy_, \
    bstack111l11lll_opy_, bstack11l111ll1_opy_, bstack1ll111ll1_opy_, bstack11l1l1lll1l_opy_
from bstack_utils.bstack111llllll1l_opy_ import bstack111llll11l1_opy_
from bstack_utils.messages import bstack1111l111l_opy_, bstack11lll11l1_opy_, bstack11lll11l1l_opy_, bstack11l1ll1ll1_opy_, bstack11l1l1ll1l_opy_, \
    bstack1l1l111ll1_opy_, bstack1l11ll1ll_opy_, bstack11lll11lll_opy_, bstack11ll11l11_opy_, bstack1l1l1lll1l_opy_, \
    bstack1l1l1111_opy_, bstack1llllllll_opy_
from bstack_utils.proxy import bstack11l1l1lll_opy_, bstack11l111l11l_opy_
from bstack_utils.bstack1lll1l1111_opy_ import bstack1111l1lll1l_opy_, bstack1111ll11l11_opy_, bstack1111l1ll1l1_opy_, bstack1111l1ll11l_opy_, \
    bstack1111l1llll1_opy_, bstack1111ll1111l_opy_, bstack1111ll111l1_opy_, bstack1l1lll11l_opy_, bstack1111ll11l1l_opy_
from bstack_utils.bstack1l1ll11l11_opy_ import bstack1llll1l1l_opy_
from bstack_utils.bstack111ll1ll_opy_ import bstack1lll1ll11_opy_, bstack11ll111l1l_opy_, bstack1lll111l1l_opy_, \
    bstack1lll11l1ll_opy_, bstack1l1ll1ll11_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack111llllll1_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack11l1ll111_opy_
import bstack_utils.accessibility as bstack1l11l11ll1_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack11111ll1l_opy_
from bstack_utils.bstack11ll1l1ll_opy_ import bstack11ll1l1ll_opy_
from bstack_utils.bstack1ll1ll1l_opy_ import bstack1lllll1l11_opy_
from browserstack_sdk.__init__ import bstack1ll1111lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l111l_opy_ import bstack1ll1llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11ll_opy_ import bstack1l1ll11ll_opy_, bstack11ll1l111_opy_, bstack11ll1111l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1l1lll_opy_, bstack1lll11lllll_opy_, bstack1lllll1111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l1ll11ll_opy_ import bstack1l1ll11ll_opy_, bstack11ll1l111_opy_, bstack11ll1111l_opy_
bstack1l1l11111l_opy_ = None
bstack1l1ll11111_opy_ = None
bstack1ll1l11lll_opy_ = None
bstack11ll1llll_opy_ = None
bstack11l1ll11_opy_ = None
bstack1l111l1l1_opy_ = None
bstack1l1111l1ll_opy_ = None
bstack11l11l1lll_opy_ = None
bstack1llll11ll_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1l1111l1_opy_ = None
bstack1ll11l1111_opy_ = None
bstack1lllll11l_opy_ = bstack111lll_opy_ (u"ࠨࠩ₧")
CONFIG = {}
bstack11lll111l_opy_ = False
bstack11ll1111ll_opy_ = bstack111lll_opy_ (u"ࠩࠪ₨")
bstack1l1lll11l1_opy_ = bstack111lll_opy_ (u"ࠪࠫ₩")
bstack1lllll111_opy_ = False
bstack1ll11111l_opy_ = []
bstack11llll1lll_opy_ = bstack11llll111_opy_
bstack1lllllll1ll1_opy_ = bstack111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ₪")
bstack1111llll_opy_ = {}
bstack11l1l1llll_opy_ = None
bstack1l1l1l1l1_opy_ = False
logger = bstack1111ll111_opy_.get_logger(__name__, bstack11llll1lll_opy_)
store = {
    bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ₫"): []
}
bstack1lllllll1l1l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11lll1_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l1l1lll_opy_(
    test_framework_name=bstack1ll1l1l111_opy_[bstack111lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ€")] if bstack111ll111_opy_() else bstack1ll1l1l111_opy_[bstack111lll_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧ₭")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1ll111l1l_opy_(page, bstack1111llll1_opy_):
    try:
        page.evaluate(bstack111lll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ₮"),
                      bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭₯") + json.dumps(
                          bstack1111llll1_opy_) + bstack111lll_opy_ (u"ࠥࢁࢂࠨ₰"))
    except Exception as e:
        print(bstack111lll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ₱"), e)
def bstack111lllll1_opy_(page, message, level):
    try:
        page.evaluate(bstack111lll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ₲"), bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ₳") + json.dumps(
            message) + bstack111lll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ₴") + json.dumps(level) + bstack111lll_opy_ (u"ࠨࡿࢀࠫ₵"))
    except Exception as e:
        print(bstack111lll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ₶"), e)
def pytest_configure(config):
    global bstack11ll1111ll_opy_
    global CONFIG
    bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
    config.args = bstack11l1ll111_opy_.bstack11111111111_opy_(config.args)
    bstack1ll1l11ll_opy_.bstack11ll111ll1_opy_(bstack1ll111ll1_opy_(config.getoption(bstack111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ₷"))))
    try:
        bstack1111ll111_opy_.bstack111ll1ll1l1_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.CONNECT, bstack11ll1111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ₸"), bstack111lll_opy_ (u"ࠬ࠶ࠧ₹")))
        config = json.loads(os.environ.get(bstack111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ₺"), bstack111lll_opy_ (u"ࠢࡼࡿࠥ₻")))
        cli.bstack1llll11ll11_opy_(bstack11llll1l1l_opy_(bstack11ll1111ll_opy_, CONFIG), cli_context.platform_index, bstack1ll11l1l11_opy_)
    if cli.bstack1llll111l11_opy_(bstack1ll1llll11l_opy_):
        cli.bstack1lll1l111ll_opy_()
        logger.debug(bstack111lll_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ₼") + str(cli_context.platform_index) + bstack111lll_opy_ (u"ࠤࠥ₽"))
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.BEFORE_ALL, bstack1lllll1111l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack111lll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣ₾"), None)
    if cli.is_running() and when == bstack111lll_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ₿"):
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.LOG_REPORT, bstack1lllll1111l_opy_.PRE, item, call)
    outcome = yield
    if when == bstack111lll_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ⃀"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111lll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⃁")))
        if not passed:
            config = json.loads(os.environ.get(bstack111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ⃂"), bstack111lll_opy_ (u"ࠣࡽࢀࠦ⃃")))
            if bstack1lllll1l11_opy_.bstack1l1111111_opy_(config):
                bstack111l1llll1l_opy_ = bstack1lllll1l11_opy_.bstack1l1ll1l1l_opy_(config)
                if item.execution_count > bstack111l1llll1l_opy_:
                    print(bstack111lll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡲࡦࡶࡵ࡭ࡪࡹ࠺ࠡࠩ⃄"), report.nodeid, os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⃅")))
                    bstack1lllll1l11_opy_.bstack111ll111lll_opy_(report.nodeid)
            else:
                print(bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠫ⃆"), report.nodeid, os.environ.get(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⃇")))
                bstack1lllll1l11_opy_.bstack111ll111lll_opy_(report.nodeid)
        else:
            print(bstack111lll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡵࡧࡳࡴࡧࡧ࠾ࠥ࠭⃈"), report.nodeid, os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⃉")))
    if cli.is_running():
        if when == bstack111lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⃊"):
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.BEFORE_EACH, bstack1lllll1111l_opy_.POST, item, call, outcome)
        elif when == bstack111lll_opy_ (u"ࠤࡦࡥࡱࡲࠢ⃋"):
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.LOG_REPORT, bstack1lllll1111l_opy_.POST, item, call, outcome)
        elif when == bstack111lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ⃌"):
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.AFTER_EACH, bstack1lllll1111l_opy_.POST, item, call, outcome)
        return # skip all existing bstack1lllllllll1l_opy_
    skipSessionName = item.config.getoption(bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⃍"))
    plugins = item.config.getoption(bstack111lll_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨ⃎"))
    report = outcome.get_result()
    os.environ[bstack111lll_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⃏")] = report.nodeid
    bstack1lllllll11ll_opy_(item, call, report)
    if bstack111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧ⃐") not in plugins or bstack111ll111_opy_():
        return
    summary = []
    driver = getattr(item, bstack111lll_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤ⃑"), None)
    page = getattr(item, bstack111lll_opy_ (u"ࠤࡢࡴࡦ࡭ࡥ⃒ࠣ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1llllll11lll_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1llllllll1ll_opy_(item, report, summary, skipSessionName)
def bstack1llllll11lll_opy_(item, report, summary, skipSessionName):
    if report.when == bstack111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱ⃓ࠩ") and report.skipped:
        bstack1111ll11l1l_opy_(report)
    if report.when in [bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⃔"), bstack111lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⃕")]:
        return
    if not bstack1l1ll11l1ll_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack111lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ⃖")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ⃗") + json.dumps(
                    report.nodeid) + bstack111lll_opy_ (u"ࠨࡿࢀ⃘ࠫ"))
        os.environ[bstack111lll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉ⃙ࠬ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111lll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿ⃚ࠥ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111lll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⃛")))
    bstack11ll11l11l_opy_ = bstack111lll_opy_ (u"ࠧࠨ⃜")
    bstack1111ll11l1l_opy_(report)
    if not passed:
        try:
            bstack11ll11l11l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111lll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⃝").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll11l11l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111lll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⃞")))
        bstack11ll11l11l_opy_ = bstack111lll_opy_ (u"ࠣࠤ⃟")
        if not passed:
            try:
                bstack11ll11l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111lll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⃠").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11ll11l11l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ⃡")
                    + json.dumps(bstack111lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧ⃢"))
                    + bstack111lll_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ⃣")
                )
            else:
                item._driver.execute_script(
                    bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⃤")
                    + json.dumps(str(bstack11ll11l11l_opy_))
                    + bstack111lll_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ⃥ࠥ")
                )
        except Exception as e:
            summary.append(bstack111lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨ⃦").format(e))
def bstack1llllllll111_opy_(test_name, error_message):
    try:
        bstack1lllllllll11_opy_ = []
        bstack1l11l11l1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⃧"), bstack111lll_opy_ (u"ࠪ࠴⃨ࠬ"))
        bstack11l1l1l1ll_opy_ = {bstack111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⃩"): test_name, bstack111lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵ⃪ࠫ"): error_message, bstack111lll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ⃫ࠬ"): bstack1l11l11l1l_opy_}
        bstack1llllll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲ⃬ࠬ"))
        if os.path.exists(bstack1llllll1l11l_opy_):
            with open(bstack1llllll1l11l_opy_) as f:
                bstack1lllllllll11_opy_ = json.load(f)
        bstack1lllllllll11_opy_.append(bstack11l1l1l1ll_opy_)
        with open(bstack1llllll1l11l_opy_, bstack111lll_opy_ (u"ࠨࡹ⃭ࠪ")) as f:
            json.dump(bstack1lllllllll11_opy_, f)
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿⃮ࠦࠧ") + str(e))
def bstack1llllllll1ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack111lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⃯"), bstack111lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⃰")]:
        return
    if (str(skipSessionName).lower() != bstack111lll_opy_ (u"ࠬࡺࡲࡶࡧࠪ⃱")):
        bstack1ll111l1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111lll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⃲")))
    bstack11ll11l11l_opy_ = bstack111lll_opy_ (u"ࠢࠣ⃳")
    bstack1111ll11l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11ll11l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111lll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⃴").format(e)
                )
        try:
            if passed:
                bstack1l1ll1ll11_opy_(getattr(item, bstack111lll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⃵"), None), bstack111lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ⃶"))
            else:
                error_message = bstack111lll_opy_ (u"ࠫࠬ⃷")
                if bstack11ll11l11l_opy_:
                    bstack111lllll1_opy_(item._page, str(bstack11ll11l11l_opy_), bstack111lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ⃸"))
                    bstack1l1ll1ll11_opy_(getattr(item, bstack111lll_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⃹"), None), bstack111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ⃺"), str(bstack11ll11l11l_opy_))
                    error_message = str(bstack11ll11l11l_opy_)
                else:
                    bstack1l1ll1ll11_opy_(getattr(item, bstack111lll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⃻"), None), bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⃼"))
                bstack1llllllll111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111lll_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ⃽").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack111lll_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ⃾"), default=bstack111lll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⃿"), help=bstack111lll_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ℀"))
    parser.addoption(bstack111lll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ℁"), default=bstack111lll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢℂ"), help=bstack111lll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ℃"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111lll_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ℄"), action=bstack111lll_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ℅"), default=bstack111lll_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ℆"),
                         help=bstack111lll_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧℇ"))
def bstack11l1111111_opy_(log):
    if not (log[bstack111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ℈")] and log[bstack111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ℉")].strip()):
        return
    active = bstack111ll1ll1l_opy_()
    log = {
        bstack111lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨℊ"): log[bstack111lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩℋ")],
        bstack111lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧℌ"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠬࡠࠧℍ"),
        bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧℎ"): log[bstack111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨℏ")],
    }
    if active:
        if active[bstack111lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ℐ")] == bstack111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧℑ"):
            log[bstack111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪℒ")] = active[bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫℓ")]
        elif active[bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ℔")] == bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࠫℕ"):
            log[bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ№")] = active[bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ℗")]
    bstack11111ll1l_opy_.bstack11l1111ll_opy_([log])
def bstack111ll1ll1l_opy_():
    if len(store[bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭℘")]) > 0 and store[bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧℙ")][-1]:
        return {
            bstack111lll_opy_ (u"ࠫࡹࡿࡰࡦࠩℚ"): bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪℛ"),
            bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ℜ"): store[bstack111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫℝ")][-1]
        }
    if store.get(bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ℞"), None):
        return {
            bstack111lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ℟"): bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࠨ℠"),
            bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ℡"): store[bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ™")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.INIT_TEST, bstack1lllll1111l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.INIT_TEST, bstack1lllll1111l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1llllllll1l1_opy_ = True
        bstack111l11l1l_opy_ = bstack1l11l11ll1_opy_.bstack11lllllll1_opy_(bstack11l111111l1_opy_(item.own_markers))
        if not cli.bstack1llll111l11_opy_(bstack1ll1llll11l_opy_):
            item._a11y_test_case = bstack111l11l1l_opy_
            if bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ℣"), None):
                driver = getattr(item, bstack111lll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨℤ"), None)
                item._a11y_started = bstack1l11l11ll1_opy_.bstack1ll1l1l1l1_opy_(driver, bstack111l11l1l_opy_)
        if not bstack11111ll1l_opy_.on() or bstack1lllllll1ll1_opy_ != bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ℥"):
            return
        global current_test_uuid #, bstack111lll11ll_opy_
        bstack111l1ll11l_opy_ = {
            bstack111lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧΩ"): uuid4().__str__(),
            bstack111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ℧"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠫ࡟࠭ℨ")
        }
        current_test_uuid = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ℩")]
        store[bstack111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪK")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬÅ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11lll1_opy_[item.nodeid] = {**_111l11lll1_opy_[item.nodeid], **bstack111l1ll11l_opy_}
        bstack1lllllll1l11_opy_(item, _111l11lll1_opy_[item.nodeid], bstack111lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩℬ"))
    except Exception as err:
        print(bstack111lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫℭ"), str(err))
def pytest_runtest_setup(item):
    store[bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ℮")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.BEFORE_EACH, bstack1lllll1111l_opy_.PRE, item, bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪℯ"))
    if bstack1lllll1l11_opy_.bstack111ll11llll_opy_():
            bstack1llllllll11l_opy_ = bstack111lll_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡧࡳࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤℰ")
            logger.error(bstack1llllllll11l_opy_)
            bstack111l1ll11l_opy_ = {
                bstack111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫℱ"): uuid4().__str__(),
                bstack111lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫℲ"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠨ࡜ࠪℳ"),
                bstack111lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧℴ"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠪ࡞ࠬℵ"),
                bstack111lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫℶ"): bstack111lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ℷ"),
                bstack111lll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ℸ"): bstack1llllllll11l_opy_,
                bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ℹ"): [],
                bstack111lll_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ℺"): []
            }
            bstack1lllllll1l11_opy_(item, bstack111l1ll11l_opy_, bstack111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ℻"))
            pytest.skip(bstack1llllllll11l_opy_)
            return # skip all existing bstack1lllllllll1l_opy_
    global bstack1lllllll1l1l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11111111_opy_():
        atexit.register(bstack1ll1lll111_opy_)
        if not bstack1lllllll1l1l_opy_:
            try:
                bstack1lllllll1111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l1lll1l_opy_():
                    bstack1lllllll1111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lllllll1111_opy_:
                    signal.signal(s, bstack1lllllll11l1_opy_)
                bstack1lllllll1l1l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦℼ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111l1lll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫℽ")
    try:
        if not bstack11111ll1l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l1ll11l_opy_ = {
            bstack111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪℾ"): uuid,
            bstack111lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪℿ"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"࡛ࠧࠩ⅀"),
            bstack111lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⅁"): bstack111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⅂"),
            bstack111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⅃"): bstack111lll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⅄"),
            bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨⅅ"): bstack111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬⅆ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫⅇ")] = item
        store[bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬⅈ")] = [uuid]
        if not _111l11lll1_opy_.get(item.nodeid, None):
            _111l11lll1_opy_[item.nodeid] = {bstack111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨⅉ"): [], bstack111lll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⅊"): []}
        _111l11lll1_opy_[item.nodeid][bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⅋")].append(bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⅌")])
        _111l11lll1_opy_[item.nodeid + bstack111lll_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭⅍")] = bstack111l1ll11l_opy_
        bstack1llllll1l1l1_opy_(item, bstack111l1ll11l_opy_, bstack111lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅎ"))
    except Exception as err:
        print(bstack111lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ⅏"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.AFTER_EACH, bstack1lllll1111l_opy_.PRE, item, bstack111lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⅐"))
        return # skip all existing bstack1lllllllll1l_opy_
    try:
        global bstack1111llll_opy_
        bstack1l11l11l1l_opy_ = 0
        if bstack1lllll111_opy_ is True:
            bstack1l11l11l1l_opy_ = int(os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⅑")))
        if bstack11l1ll1l11_opy_.bstack11l1ll11l1_opy_() == bstack111lll_opy_ (u"ࠦࡹࡸࡵࡦࠤ⅒"):
            if bstack11l1ll1l11_opy_.bstack1ll111ll11_opy_() == bstack111lll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⅓"):
                bstack1llllll1l111_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⅔"), None)
                bstack1l1ll111l1_opy_ = bstack1llllll1l111_opy_ + bstack111lll_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥ⅕")
                driver = getattr(item, bstack111lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⅖"), None)
                bstack1lllllll11_opy_ = getattr(item, bstack111lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⅗"), None)
                bstack111111ll_opy_ = getattr(item, bstack111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⅘"), None)
                PercySDK.screenshot(driver, bstack1l1ll111l1_opy_, bstack1lllllll11_opy_=bstack1lllllll11_opy_, bstack111111ll_opy_=bstack111111ll_opy_, bstack1lll1l1lll_opy_=bstack1l11l11l1l_opy_)
        if not cli.bstack1llll111l11_opy_(bstack1ll1llll11l_opy_):
            if getattr(item, bstack111lll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ⅙"), False):
                bstack1llll1l111_opy_.bstack1ll1ll1ll_opy_(getattr(item, bstack111lll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⅚"), None), bstack1111llll_opy_, logger, item)
        if not bstack11111ll1l_opy_.on():
            return
        bstack111l1ll11l_opy_ = {
            bstack111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⅛"): uuid4().__str__(),
            bstack111lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⅜"): bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠨ࡜ࠪ⅝"),
            bstack111lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⅞"): bstack111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⅟"),
            bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧⅠ"): bstack111lll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩⅡ"),
            bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩⅢ"): bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩⅣ")
        }
        _111l11lll1_opy_[item.nodeid + bstack111lll_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫⅤ")] = bstack111l1ll11l_opy_
        bstack1llllll1l1l1_opy_(item, bstack111l1ll11l_opy_, bstack111lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪⅥ"))
    except Exception as err:
        print(bstack111lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩⅦ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1111l1ll11l_opy_(fixturedef.argname):
        store[bstack111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪⅧ")] = request.node
    elif bstack1111l1llll1_opy_(fixturedef.argname):
        store[bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪⅨ")] = request.node
    if not bstack11111ll1l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.SETUP_FIXTURE, bstack1lllll1111l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.SETUP_FIXTURE, bstack1lllll1111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1lllllllll1l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.SETUP_FIXTURE, bstack1lllll1111l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.SETUP_FIXTURE, bstack1lllll1111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1lllllllll1l_opy_
    try:
        fixture = {
            bstack111lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⅩ"): fixturedef.argname,
            bstack111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧⅪ"): bstack11l1l1l1l11_opy_(outcome),
            bstack111lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪⅫ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭Ⅼ")]
        if not _111l11lll1_opy_.get(current_test_item.nodeid, None):
            _111l11lll1_opy_[current_test_item.nodeid] = {bstack111lll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬⅭ"): []}
        _111l11lll1_opy_[current_test_item.nodeid][bstack111lll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭Ⅾ")].append(fixture)
    except Exception as err:
        logger.debug(bstack111lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨⅯ"), str(err))
if bstack111ll111_opy_() and bstack11111ll1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.STEP, bstack1lllll1111l_opy_.PRE, request, step)
            return
        try:
            _111l11lll1_opy_[request.node.nodeid][bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩⅰ")].bstack11l11l1l1l_opy_(id(step))
        except Exception as err:
            print(bstack111lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬⅱ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.STEP, bstack1lllll1111l_opy_.POST, request, step, exception)
            return
        try:
            _111l11lll1_opy_[request.node.nodeid][bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫⅲ")].bstack111ll1l1l1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111lll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ⅳ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.STEP, bstack1lllll1111l_opy_.POST, request, step)
            return
        try:
            bstack11l111111l_opy_: bstack111llllll1_opy_ = _111l11lll1_opy_[request.node.nodeid][bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ⅴ")]
            bstack11l111111l_opy_.bstack111ll1l1l1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨⅵ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lllllll1ll1_opy_
        try:
            if not bstack11111ll1l_opy_.on() or bstack1lllllll1ll1_opy_ != bstack111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩⅶ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬⅷ"), None)
            if not _111l11lll1_opy_.get(request.node.nodeid, None):
                _111l11lll1_opy_[request.node.nodeid] = {}
            bstack11l111111l_opy_ = bstack111llllll1_opy_.bstack11111ll11ll_opy_(
                scenario, feature, request.node,
                name=bstack1111ll1111l_opy_(request.node, scenario),
                started_at=bstack1llllllll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111lll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩⅸ"),
                tags=bstack1111ll111l1_opy_(feature, scenario),
                bstack111lll1l11_opy_=bstack11111ll1l_opy_.bstack111lll1lll_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11lll1_opy_[request.node.nodeid][bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫⅹ")] = bstack11l111111l_opy_
            bstack1lllllllllll_opy_(bstack11l111111l_opy_.uuid)
            bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪⅺ"), bstack11l111111l_opy_)
        except Exception as err:
            print(bstack111lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬⅻ"), str(err))
def bstack1llllll1111l_opy_(bstack111ll1llll_opy_):
    if bstack111ll1llll_opy_ in store[bstack111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨⅼ")]:
        store[bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩⅽ")].remove(bstack111ll1llll_opy_)
def bstack1lllllllllll_opy_(test_uuid):
    store[bstack111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪⅾ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack11111ll1l_opy_.bstack11111l11l1l_opy_
def bstack1lllllll11ll_opy_(item, call, report):
    logger.debug(bstack111lll_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩⅿ"))
    global bstack1lllllll1ll1_opy_
    bstack111l1l1l1_opy_ = bstack1llllllll1_opy_()
    if hasattr(report, bstack111lll_opy_ (u"ࠨࡵࡷࡳࡵ࠭ↀ")):
        bstack111l1l1l1_opy_ = bstack11l111l1ll1_opy_(report.stop)
    elif hasattr(report, bstack111lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨↁ")):
        bstack111l1l1l1_opy_ = bstack11l111l1ll1_opy_(report.start)
    try:
        if getattr(report, bstack111lll_opy_ (u"ࠪࡻ࡭࡫࡮ࠨↂ"), bstack111lll_opy_ (u"ࠫࠬↃ")) == bstack111lll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪↄ"):
            logger.debug(bstack111lll_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨↅ").format(getattr(report, bstack111lll_opy_ (u"ࠧࡸࡪࡨࡲࠬↆ"), bstack111lll_opy_ (u"ࠨࠩↇ")).__str__(), bstack1lllllll1ll1_opy_))
            if bstack1lllllll1ll1_opy_ == bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩↈ"):
                _111l11lll1_opy_[item.nodeid][bstack111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ↉")] = bstack111l1l1l1_opy_
                bstack1lllllll1l11_opy_(item, _111l11lll1_opy_[item.nodeid], bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭↊"), report, call)
                store[bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ↋")] = None
            elif bstack1lllllll1ll1_opy_ == bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ↌"):
                bstack11l111111l_opy_ = _111l11lll1_opy_[item.nodeid][bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ↍")]
                bstack11l111111l_opy_.set(hooks=_111l11lll1_opy_[item.nodeid].get(bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ↎"), []))
                exception, bstack111lll111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll111l_opy_ = [call.excinfo.exconly(), getattr(report, bstack111lll_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ↏"), bstack111lll_opy_ (u"ࠪࠫ←"))]
                bstack11l111111l_opy_.stop(time=bstack111l1l1l1_opy_, result=Result(result=getattr(report, bstack111lll_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ↑"), bstack111lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ→")), exception=exception, bstack111lll111l_opy_=bstack111lll111l_opy_))
                bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ↓"), _111l11lll1_opy_[item.nodeid][bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ↔")])
        elif getattr(report, bstack111lll_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭↕"), bstack111lll_opy_ (u"ࠩࠪ↖")) in [bstack111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ↗"), bstack111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭↘")]:
            logger.debug(bstack111lll_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ↙").format(getattr(report, bstack111lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ↚"), bstack111lll_opy_ (u"ࠧࠨ↛")).__str__(), bstack1lllllll1ll1_opy_))
            bstack111llll11l_opy_ = item.nodeid + bstack111lll_opy_ (u"ࠨ࠯ࠪ↜") + getattr(report, bstack111lll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ↝"), bstack111lll_opy_ (u"ࠪࠫ↞"))
            if getattr(report, bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ↟"), False):
                hook_type = bstack111lll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ↠") if getattr(report, bstack111lll_opy_ (u"࠭ࡷࡩࡧࡱࠫ↡"), bstack111lll_opy_ (u"ࠧࠨ↢")) == bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ↣") else bstack111lll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭↤")
                _111l11lll1_opy_[bstack111llll11l_opy_] = {
                    bstack111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ↥"): uuid4().__str__(),
                    bstack111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ↦"): bstack111l1l1l1_opy_,
                    bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ↧"): hook_type
                }
            _111l11lll1_opy_[bstack111llll11l_opy_][bstack111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ↨")] = bstack111l1l1l1_opy_
            bstack1llllll1111l_opy_(_111l11lll1_opy_[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↩")])
            bstack1llllll1l1l1_opy_(item, _111l11lll1_opy_[bstack111llll11l_opy_], bstack111lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ↪"), report, call)
            if getattr(report, bstack111lll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ↫"), bstack111lll_opy_ (u"ࠪࠫ↬")) == bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ↭"):
                if getattr(report, bstack111lll_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭↮"), bstack111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭↯")) == bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ↰"):
                    bstack111l1ll11l_opy_ = {
                        bstack111lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↱"): uuid4().__str__(),
                        bstack111lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭↲"): bstack1llllllll1_opy_(),
                        bstack111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ↳"): bstack1llllllll1_opy_()
                    }
                    _111l11lll1_opy_[item.nodeid] = {**_111l11lll1_opy_[item.nodeid], **bstack111l1ll11l_opy_}
                    bstack1lllllll1l11_opy_(item, _111l11lll1_opy_[item.nodeid], bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ↴"))
                    bstack1lllllll1l11_opy_(item, _111l11lll1_opy_[item.nodeid], bstack111lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ↵"), report, call)
    except Exception as err:
        print(bstack111lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ↶"), str(err))
def bstack1llllll11l1l_opy_(test, bstack111l1ll11l_opy_, result=None, call=None, bstack1ll1111l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l111111l_opy_ = {
        bstack111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ↷"): bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↸")],
        bstack111lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ↹"): bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࠨ↺"),
        bstack111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ↻"): test.name,
        bstack111lll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ↼"): {
            bstack111lll_opy_ (u"࠭࡬ࡢࡰࡪࠫ↽"): bstack111lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ↾"),
            bstack111lll_opy_ (u"ࠨࡥࡲࡨࡪ࠭↿"): inspect.getsource(test.obj)
        },
        bstack111lll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⇀"): test.name,
        bstack111lll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⇁"): test.name,
        bstack111lll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⇂"): bstack11l1ll111_opy_.bstack1111lllll1_opy_(test),
        bstack111lll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⇃"): file_path,
        bstack111lll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⇄"): file_path,
        bstack111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⇅"): bstack111lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⇆"),
        bstack111lll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⇇"): file_path,
        bstack111lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⇈"): bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⇉")],
        bstack111lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⇊"): bstack111lll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⇋"),
        bstack111lll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⇌"): {
            bstack111lll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⇍"): test.nodeid
        },
        bstack111lll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⇎"): bstack11l111111l1_opy_(test.own_markers)
    }
    if bstack1ll1111l1l_opy_ in [bstack111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⇏"), bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⇐")]:
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠬࡳࡥࡵࡣࠪ⇑")] = {
            bstack111lll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⇒"): bstack111l1ll11l_opy_.get(bstack111lll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⇓"), [])
        }
    if bstack1ll1111l1l_opy_ == bstack111lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⇔"):
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⇕")] = bstack111lll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⇖")
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⇗")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⇘")]
        bstack11l111111l_opy_[bstack111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⇙")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⇚")]
    if result:
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⇛")] = result.outcome
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⇜")] = result.duration * 1000
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⇝")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⇞")]
        if result.failed:
            bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⇟")] = bstack11111ll1l_opy_.bstack11111lllll_opy_(call.excinfo.typename)
            bstack11l111111l_opy_[bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⇠")] = bstack11111ll1l_opy_.bstack111111llll1_opy_(call.excinfo, result)
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⇡")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⇢")]
    if outcome:
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⇣")] = bstack11l1l1l1l11_opy_(outcome)
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⇤")] = 0
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⇥")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⇦")]
        if bstack11l111111l_opy_[bstack111lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⇧")] == bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⇨"):
            bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⇩")] = bstack111lll_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⇪")  # bstack1llllll111ll_opy_
            bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⇫")] = [{bstack111lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⇬"): [bstack111lll_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⇭")]}]
        bstack11l111111l_opy_[bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⇮")] = bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⇯")]
    return bstack11l111111l_opy_
def bstack1llllllllll1_opy_(test, bstack111l11l1l1_opy_, bstack1ll1111l1l_opy_, result, call, outcome, bstack1llllll1llll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⇰")]
    hook_name = bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⇱")]
    hook_data = {
        bstack111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⇲"): bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠫࡺࡻࡩࡥࠩ⇳")],
        bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⇴"): bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⇵"),
        bstack111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⇶"): bstack111lll_opy_ (u"ࠨࡽࢀࠫ⇷").format(bstack1111ll11l11_opy_(hook_name)),
        bstack111lll_opy_ (u"ࠩࡥࡳࡩࡿࠧ⇸"): {
            bstack111lll_opy_ (u"ࠪࡰࡦࡴࡧࠨ⇹"): bstack111lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⇺"),
            bstack111lll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⇻"): None
        },
        bstack111lll_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⇼"): test.name,
        bstack111lll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⇽"): bstack11l1ll111_opy_.bstack1111lllll1_opy_(test, hook_name),
        bstack111lll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⇾"): file_path,
        bstack111lll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⇿"): file_path,
        bstack111lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ∀"): bstack111lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ∁"),
        bstack111lll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ∂"): file_path,
        bstack111lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ∃"): bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ∄")],
        bstack111lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ∅"): bstack111lll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ∆") if bstack1lllllll1ll1_opy_ == bstack111lll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ∇") else bstack111lll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ∈"),
        bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ∉"): hook_type
    }
    bstack11111ll11l1_opy_ = bstack111l1llll1_opy_(_111l11lll1_opy_.get(test.nodeid, None))
    if bstack11111ll11l1_opy_:
        hook_data[bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ∊")] = bstack11111ll11l1_opy_
    if result:
        hook_data[bstack111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ∋")] = result.outcome
        hook_data[bstack111lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ∌")] = result.duration * 1000
        hook_data[bstack111lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∍")] = bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ∎")]
        if result.failed:
            hook_data[bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ∏")] = bstack11111ll1l_opy_.bstack11111lllll_opy_(call.excinfo.typename)
            hook_data[bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭∐")] = bstack11111ll1l_opy_.bstack111111llll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭∑")] = bstack11l1l1l1l11_opy_(outcome)
        hook_data[bstack111lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ−")] = 100
        hook_data[bstack111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭∓")] = bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ∔")]
        if hook_data[bstack111lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ∕")] == bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ∖"):
            hook_data[bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ∗")] = bstack111lll_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ∘")  # bstack1llllll111ll_opy_
            hook_data[bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ∙")] = [{bstack111lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ√"): [bstack111lll_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭∛")]}]
    if bstack1llllll1llll_opy_:
        hook_data[bstack111lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ∜")] = bstack1llllll1llll_opy_.result
        hook_data[bstack111lll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ∝")] = bstack11l11l11lll_opy_(bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ∞")], bstack111l11l1l1_opy_[bstack111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ∟")])
        hook_data[bstack111lll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ∠")] = bstack111l11l1l1_opy_[bstack111lll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭∡")]
        if hook_data[bstack111lll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ∢")] == bstack111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ∣"):
            hook_data[bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ∤")] = bstack11111ll1l_opy_.bstack11111lllll_opy_(bstack1llllll1llll_opy_.exception_type)
            hook_data[bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭∥")] = [{bstack111lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ∦"): bstack11l1l1l11l1_opy_(bstack1llllll1llll_opy_.exception)}]
    return hook_data
def bstack1lllllll1l11_opy_(test, bstack111l1ll11l_opy_, bstack1ll1111l1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack111lll_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ∧").format(bstack1ll1111l1l_opy_))
    bstack11l111111l_opy_ = bstack1llllll11l1l_opy_(test, bstack111l1ll11l_opy_, result, call, bstack1ll1111l1l_opy_, outcome)
    driver = getattr(test, bstack111lll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ∨"), None)
    if bstack1ll1111l1l_opy_ == bstack111lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ∩") and driver:
        bstack11l111111l_opy_[bstack111lll_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ∪")] = bstack11111ll1l_opy_.bstack111lll1lll_opy_(driver)
    if bstack1ll1111l1l_opy_ == bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ∫"):
        bstack1ll1111l1l_opy_ = bstack111lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ∬")
    bstack111l11llll_opy_ = {
        bstack111lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ∭"): bstack1ll1111l1l_opy_,
        bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ∮"): bstack11l111111l_opy_
    }
    bstack11111ll1l_opy_.bstack11111111l_opy_(bstack111l11llll_opy_)
    if bstack1ll1111l1l_opy_ == bstack111lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ∯"):
        threading.current_thread().bstackTestMeta = {bstack111lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ∰"): bstack111lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ∱")}
    elif bstack1ll1111l1l_opy_ == bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭∲"):
        threading.current_thread().bstackTestMeta = {bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ∳"): getattr(result, bstack111lll_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ∴"), bstack111lll_opy_ (u"ࠧࠨ∵"))}
def bstack1llllll1l1l1_opy_(test, bstack111l1ll11l_opy_, bstack1ll1111l1l_opy_, result=None, call=None, outcome=None, bstack1llllll1llll_opy_=None):
    logger.debug(bstack111lll_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ∶").format(bstack1ll1111l1l_opy_))
    hook_data = bstack1llllllllll1_opy_(test, bstack111l1ll11l_opy_, bstack1ll1111l1l_opy_, result, call, outcome, bstack1llllll1llll_opy_)
    bstack111l11llll_opy_ = {
        bstack111lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭∷"): bstack1ll1111l1l_opy_,
        bstack111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ∸"): hook_data
    }
    bstack11111ll1l_opy_.bstack11111111l_opy_(bstack111l11llll_opy_)
def bstack111l1llll1_opy_(bstack111l1ll11l_opy_):
    if not bstack111l1ll11l_opy_:
        return None
    if bstack111l1ll11l_opy_.get(bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ∹"), None):
        return getattr(bstack111l1ll11l_opy_[bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ∺")], bstack111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ∻"), None)
    return bstack111l1ll11l_opy_.get(bstack111lll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ∼"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.LOG, bstack1lllll1111l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_.LOG, bstack1lllll1111l_opy_.POST, request, caplog)
        return # skip all existing bstack1lllllllll1l_opy_
    try:
        if not bstack11111ll1l_opy_.on():
            return
        places = [bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ∽"), bstack111lll_opy_ (u"ࠩࡦࡥࡱࡲࠧ∾"), bstack111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ∿")]
        logs = []
        for bstack1lllllll111l_opy_ in places:
            records = caplog.get_records(bstack1lllllll111l_opy_)
            bstack1llllll1lll1_opy_ = bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ≀") if bstack1lllllll111l_opy_ == bstack111lll_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ≁") else bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭≂")
            bstack1llllll111l1_opy_ = request.node.nodeid + (bstack111lll_opy_ (u"ࠧࠨ≃") if bstack1lllllll111l_opy_ == bstack111lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭≄") else bstack111lll_opy_ (u"ࠩ࠰ࠫ≅") + bstack1lllllll111l_opy_)
            test_uuid = bstack111l1llll1_opy_(_111l11lll1_opy_.get(bstack1llllll111l1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11l11l1lll1_opy_(record.message):
                    continue
                logs.append({
                    bstack111lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭≆"): bstack11l1l1ll1l1_opy_(record.created).isoformat() + bstack111lll_opy_ (u"ࠫ࡟࠭≇"),
                    bstack111lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ≈"): record.levelname,
                    bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ≉"): record.message,
                    bstack1llllll1lll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack11111ll1l_opy_.bstack11l1111ll_opy_(logs)
    except Exception as err:
        print(bstack111lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ≊"), str(err))
def bstack11lll1ll11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l1l1l1_opy_
    bstack1lll11l1_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ≋"), None) and bstack1ll11l1l1l_opy_(
            threading.current_thread(), bstack111lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ≌"), None)
    bstack1l1l11ll11_opy_ = getattr(driver, bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ≍"), None) != None and getattr(driver, bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ≎"), None) == True
    if sequence == bstack111lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ≏") and driver != None:
      if not bstack1l1l1l1l1_opy_ and bstack1l1ll11l1ll_opy_() and bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭≐") in CONFIG and CONFIG[bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ≑")] == True and bstack11ll1l1ll_opy_.bstack1l1ll1lll_opy_(driver_command) and (bstack1l1l11ll11_opy_ or bstack1lll11l1_opy_) and not bstack111lll1ll_opy_(args):
        try:
          bstack1l1l1l1l1_opy_ = True
          logger.debug(bstack111lll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ≒").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111lll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ≓").format(str(err)))
        bstack1l1l1l1l1_opy_ = False
    if sequence == bstack111lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ≔"):
        if driver_command == bstack111lll_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ≕"):
            bstack11111ll1l_opy_.bstack1l111lll_opy_({
                bstack111lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ≖"): response[bstack111lll_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ≗")],
                bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ≘"): store[bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ≙")]
            })
def bstack1ll1lll111_opy_():
    global bstack1ll11111l_opy_
    bstack1111ll111_opy_.bstack1l111l111l_opy_()
    logging.shutdown()
    bstack11111ll1l_opy_.bstack111ll11l11_opy_()
    for driver in bstack1ll11111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllllll11l1_opy_(*args):
    global bstack1ll11111l_opy_
    bstack11111ll1l_opy_.bstack111ll11l11_opy_()
    for driver in bstack1ll11111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111ll11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll11l1ll1_opy_(self, *args, **kwargs):
    bstack1l1l1llll_opy_ = bstack1l1l11111l_opy_(self, *args, **kwargs)
    bstack111l1lll1_opy_ = getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ≚"), None)
    if bstack111l1lll1_opy_ and bstack111l1lll1_opy_.get(bstack111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ≛"), bstack111lll_opy_ (u"ࠫࠬ≜")) == bstack111lll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭≝"):
        bstack11111ll1l_opy_.bstack111111lll_opy_(self)
    return bstack1l1l1llll_opy_
@measure(event_name=EVENTS.bstack1l1ll1llll_opy_, stage=STAGE.bstack1ll11l111l_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll1ll1l1l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
    if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ≞")):
        return
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ≟"), True)
    global bstack1lllll11l_opy_
    global bstack1lll1111_opy_
    bstack1lllll11l_opy_ = framework_name
    logger.info(bstack1llllllll_opy_.format(bstack1lllll11l_opy_.split(bstack111lll_opy_ (u"ࠨ࠯ࠪ≠"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1ll11l1ll_opy_():
            Service.start = bstack1l111lll11_opy_
            Service.stop = bstack11l1l1ll1_opy_
            webdriver.Remote.get = bstack1ll111lll1_opy_
            webdriver.Remote.__init__ = bstack11ll111111_opy_
            if not isinstance(os.getenv(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ≡")), str):
                return
            WebDriver.quit = bstack1ll1ll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack11111ll1l_opy_.on():
            webdriver.Remote.__init__ = bstack1ll11l1ll1_opy_
        bstack1lll1111_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack111lll_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ≢")):
        bstack1lll1111_opy_ = eval(os.environ.get(bstack111lll_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ≣")))
    if not bstack1lll1111_opy_:
        bstack1l1l1l1ll_opy_(bstack111lll_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ≤"), bstack1l1l1111_opy_)
    if bstack1l1111ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack111lll_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ≥")) and callable(getattr(RemoteConnection, bstack111lll_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ≦"))):
                RemoteConnection._get_proxy_url = bstack1lll11ll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1lll11ll_opy_
        except Exception as e:
            logger.error(bstack1l1l111ll1_opy_.format(str(e)))
    if bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ≧") in str(framework_name).lower():
        if not bstack1l1ll11l1ll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1ll1ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1lllll_opy_
            Config.getoption = bstack1l1lllll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll111111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll1ll11l_opy_(self):
    global bstack1lllll11l_opy_
    global bstack1l11ll11l1_opy_
    global bstack1l1ll11111_opy_
    try:
        if bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ≨") in bstack1lllll11l_opy_ and self.session_id != None and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ≩"), bstack111lll_opy_ (u"ࠫࠬ≪")) != bstack111lll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭≫"):
            bstack11lll11l11_opy_ = bstack111lll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭≬") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111lll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ≭")
            bstack11l111ll1_opy_(logger, True)
            if os.environ.get(bstack111lll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ≮"), None):
                self.execute_script(
                    bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ≯") + json.dumps(
                        os.environ.get(bstack111lll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭≰"))) + bstack111lll_opy_ (u"ࠫࢂࢃࠧ≱"))
            if self != None:
                bstack1lll11l1ll_opy_(self, bstack11lll11l11_opy_, bstack111lll_opy_ (u"ࠬ࠲ࠠࠨ≲").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll111l11_opy_(bstack1ll1llll11l_opy_):
            item = store.get(bstack111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ≳"), None)
            if item is not None and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭≴"), None):
                bstack1llll1l111_opy_.bstack1ll1ll1ll_opy_(self, bstack1111llll_opy_, logger, item)
        threading.current_thread().testStatus = bstack111lll_opy_ (u"ࠨࠩ≵")
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ≶") + str(e))
    bstack1l1ll11111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1l1l11l_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack11ll111111_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll1l111_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11ll11l1_opy_
    global bstack11l1l1llll_opy_
    global bstack1lllll111_opy_
    global bstack1lllll11l_opy_
    global bstack1l1l11111l_opy_
    global bstack1ll11111l_opy_
    global bstack11ll1111ll_opy_
    global bstack1l1lll11l1_opy_
    global bstack1111llll_opy_
    CONFIG[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ≷")] = str(bstack1lllll11l_opy_) + str(__version__)
    command_executor = bstack11llll1l1l_opy_(bstack11ll1111ll_opy_, CONFIG)
    logger.debug(bstack11l1ll1ll1_opy_.format(command_executor))
    proxy = bstack1l1l1ll111_opy_(CONFIG, proxy)
    bstack1l11l11l1l_opy_ = 0
    try:
        if bstack1lllll111_opy_ is True:
            bstack1l11l11l1l_opy_ = int(os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ≸")))
    except:
        bstack1l11l11l1l_opy_ = 0
    bstack11llll1ll1_opy_ = bstack1l1lllllll_opy_(CONFIG, bstack1l11l11l1l_opy_)
    logger.debug(bstack11lll11lll_opy_.format(str(bstack11llll1ll1_opy_)))
    bstack1111llll_opy_ = CONFIG.get(bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ≹"))[bstack1l11l11l1l_opy_]
    if bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ≺") in CONFIG and CONFIG[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ≻")]:
        bstack1lll111l1l_opy_(bstack11llll1ll1_opy_, bstack1l1lll11l1_opy_)
    if bstack1l11l11ll1_opy_.bstack1111111l1_opy_(CONFIG, bstack1l11l11l1l_opy_) and bstack1l11l11ll1_opy_.bstack111l1111l_opy_(bstack11llll1ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll111l11_opy_(bstack1ll1llll11l_opy_):
            bstack1l11l11ll1_opy_.set_capabilities(bstack11llll1ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1llll111ll_opy_ = bstack1lllllll1_opy_(desired_capabilities)
        bstack1llll111ll_opy_[bstack111lll_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ≼")] = bstack1ll1lll1ll_opy_(CONFIG)
        bstack11l1l111l1_opy_ = bstack1l1lllllll_opy_(bstack1llll111ll_opy_)
        if bstack11l1l111l1_opy_:
            bstack11llll1ll1_opy_ = update(bstack11l1l111l1_opy_, bstack11llll1ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1111ll11l_opy_(options, bstack11llll1ll1_opy_)
    if not options:
        options = bstack1ll11l1l11_opy_(bstack11llll1ll1_opy_)
    if proxy and bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ≽")):
        options.proxy(proxy)
    if options and bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ≾")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1ll1ll_opy_() < version.parse(bstack111lll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ≿")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11llll1ll1_opy_)
    logger.info(bstack11lll11l1l_opy_)
    bstack1ll1l111ll_opy_.end(EVENTS.bstack1l1ll1llll_opy_.value, EVENTS.bstack1l1ll1llll_opy_.value + bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⊀"),
                               EVENTS.bstack1l1ll1llll_opy_.value + bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⊁"), True, None)
    if bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⊂")):
        bstack1l1l11111l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⊃")):
        bstack1l1l11111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1ll1l111_opy_=bstack1ll1l111_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ⊄")):
        bstack1l1l11111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll1l111_opy_=bstack1ll1l111_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1l11111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll1l111_opy_=bstack1ll1l111_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1llll1ll1l_opy_ = bstack111lll_opy_ (u"ࠪࠫ⊅")
        if bstack11l1ll1ll_opy_() >= version.parse(bstack111lll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ⊆")):
            bstack1llll1ll1l_opy_ = self.caps.get(bstack111lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⊇"))
        else:
            bstack1llll1ll1l_opy_ = self.capabilities.get(bstack111lll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⊈"))
        if bstack1llll1ll1l_opy_:
            bstack111l11lll_opy_(bstack1llll1ll1l_opy_)
            if bstack11l1ll1ll_opy_() <= version.parse(bstack111lll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ⊉")):
                self.command_executor._url = bstack111lll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⊊") + bstack11ll1111ll_opy_ + bstack111lll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ⊋")
            else:
                self.command_executor._url = bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ⊌") + bstack1llll1ll1l_opy_ + bstack111lll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ⊍")
            logger.debug(bstack11lll11l1_opy_.format(bstack1llll1ll1l_opy_))
        else:
            logger.debug(bstack1111l111l_opy_.format(bstack111lll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ⊎")))
    except Exception as e:
        logger.debug(bstack1111l111l_opy_.format(e))
    bstack1l11ll11l1_opy_ = self.session_id
    if bstack111lll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⊏") in bstack1lllll11l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⊐"), None)
        if item:
            bstack1llllll11ll1_opy_ = getattr(item, bstack111lll_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭⊑"), False)
            if not getattr(item, bstack111lll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⊒"), None) and bstack1llllll11ll1_opy_:
                setattr(store[bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⊓")], bstack111lll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⊔"), self)
        bstack111l1lll1_opy_ = getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⊕"), None)
        if bstack111l1lll1_opy_ and bstack111l1lll1_opy_.get(bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⊖"), bstack111lll_opy_ (u"ࠧࠨ⊗")) == bstack111lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⊘"):
            bstack11111ll1l_opy_.bstack111111lll_opy_(self)
    bstack1ll11111l_opy_.append(self)
    if bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⊙") in CONFIG and bstack111lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⊚") in CONFIG[bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⊛")][bstack1l11l11l1l_opy_]:
        bstack11l1l1llll_opy_ = CONFIG[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⊜")][bstack1l11l11l1l_opy_][bstack111lll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⊝")]
    logger.debug(bstack1l1l1lll1l_opy_.format(bstack1l11ll11l1_opy_))
@measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l11l11l_opy_=bstack11l1l1llll_opy_)
def bstack1ll111lll1_opy_(self, url):
    global bstack1llll11ll_opy_
    global CONFIG
    try:
        bstack11ll111l1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll11l11_opy_.format(str(err)))
    try:
        bstack1llll11ll_opy_(self, url)
    except Exception as e:
        try:
            bstack111l1lll_opy_ = str(e)
            if any(err_msg in bstack111l1lll_opy_ for err_msg in bstack1ll11ll11l_opy_):
                bstack11ll111l1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll11l11_opy_.format(str(err)))
        raise e
def bstack1l1l1ll11_opy_(item, when):
    global bstack1l1111l1_opy_
    try:
        bstack1l1111l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll111111_opy_(item, call, rep):
    global bstack1ll11l1111_opy_
    global bstack1ll11111l_opy_
    name = bstack111lll_opy_ (u"ࠧࠨ⊞")
    try:
        if rep.when == bstack111lll_opy_ (u"ࠨࡥࡤࡰࡱ࠭⊟"):
            bstack1l11ll11l1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack111lll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⊠"))
            try:
                if (str(skipSessionName).lower() != bstack111lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ⊡")):
                    name = str(rep.nodeid)
                    bstack11ll1111l1_opy_ = bstack1lll1ll11_opy_(bstack111lll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⊢"), name, bstack111lll_opy_ (u"ࠬ࠭⊣"), bstack111lll_opy_ (u"࠭ࠧ⊤"), bstack111lll_opy_ (u"ࠧࠨ⊥"), bstack111lll_opy_ (u"ࠨࠩ⊦"))
                    os.environ[bstack111lll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⊧")] = name
                    for driver in bstack1ll11111l_opy_:
                        if bstack1l11ll11l1_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll1111l1_opy_)
            except Exception as e:
                logger.debug(bstack111lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⊨").format(str(e)))
            try:
                bstack1l1lll11l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111lll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⊩"):
                    status = bstack111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⊪") if rep.outcome.lower() == bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⊫") else bstack111lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⊬")
                    reason = bstack111lll_opy_ (u"ࠨࠩ⊭")
                    if status == bstack111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⊮"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111lll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ⊯") if status == bstack111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⊰") else bstack111lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⊱")
                    data = name + bstack111lll_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ⊲") if status == bstack111lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⊳") else name + bstack111lll_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫ⊴") + reason
                    bstack1l1111l111_opy_ = bstack1lll1ll11_opy_(bstack111lll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ⊵"), bstack111lll_opy_ (u"ࠪࠫ⊶"), bstack111lll_opy_ (u"ࠫࠬ⊷"), bstack111lll_opy_ (u"ࠬ࠭⊸"), level, data)
                    for driver in bstack1ll11111l_opy_:
                        if bstack1l11ll11l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1111l111_opy_)
            except Exception as e:
                logger.debug(bstack111lll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⊹").format(str(e)))
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ⊺").format(str(e)))
    bstack1ll11l1111_opy_(item, call, rep)
notset = Notset()
def bstack1l1lllll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll1l11ll1_opy_
    if str(name).lower() == bstack111lll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ⊻"):
        return bstack111lll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ⊼")
    else:
        return bstack1ll1l11ll1_opy_(self, name, default, skip)
def bstack1lll11ll_opy_(self):
    global CONFIG
    global bstack1l1111l1ll_opy_
    try:
        proxy = bstack11l1l1lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111lll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ⊽")):
                proxies = bstack11l111l11l_opy_(proxy, bstack11llll1l1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lllll1111_opy_ = proxies.popitem()
                    if bstack111lll_opy_ (u"ࠦ࠿࠵࠯ࠣ⊾") in bstack1lllll1111_opy_:
                        return bstack1lllll1111_opy_
                    else:
                        return bstack111lll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⊿") + bstack1lllll1111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ⋀").format(str(e)))
    return bstack1l1111l1ll_opy_(self)
def bstack1l1111ll1_opy_():
    return (bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⋁") in CONFIG or bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⋂") in CONFIG) and bstack1l1l1l1l1l_opy_() and bstack11l1ll1ll_opy_() >= version.parse(
        bstack11l1l1111_opy_)
def bstack1l1l1l1lll_opy_(self,
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
    global bstack11l1l1llll_opy_
    global bstack1lllll111_opy_
    global bstack1lllll11l_opy_
    CONFIG[bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⋃")] = str(bstack1lllll11l_opy_) + str(__version__)
    bstack1l11l11l1l_opy_ = 0
    try:
        if bstack1lllll111_opy_ is True:
            bstack1l11l11l1l_opy_ = int(os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⋄")))
    except:
        bstack1l11l11l1l_opy_ = 0
    CONFIG[bstack111lll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ⋅")] = True
    bstack11llll1ll1_opy_ = bstack1l1lllllll_opy_(CONFIG, bstack1l11l11l1l_opy_)
    logger.debug(bstack11lll11lll_opy_.format(str(bstack11llll1ll1_opy_)))
    if CONFIG.get(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⋆")):
        bstack1lll111l1l_opy_(bstack11llll1ll1_opy_, bstack1l1lll11l1_opy_)
    if bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⋇") in CONFIG and bstack111lll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⋈") in CONFIG[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⋉")][bstack1l11l11l1l_opy_]:
        bstack11l1l1llll_opy_ = CONFIG[bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⋊")][bstack1l11l11l1l_opy_][bstack111lll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⋋")]
    import urllib
    import json
    if bstack111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⋌") in CONFIG and str(CONFIG[bstack111lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⋍")]).lower() != bstack111lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⋎"):
        bstack1ll1l1111l_opy_ = bstack1ll1111lll_opy_()
        bstack11ll111l11_opy_ = bstack1ll1l1111l_opy_ + urllib.parse.quote(json.dumps(bstack11llll1ll1_opy_))
    else:
        bstack11ll111l11_opy_ = bstack111lll_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ⋏") + urllib.parse.quote(json.dumps(bstack11llll1ll1_opy_))
    browser = self.connect(bstack11ll111l11_opy_)
    return browser
def bstack1ll1lll11l_opy_():
    global bstack1lll1111_opy_
    global bstack1lllll11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1lll11_opy_
        if not bstack1l1ll11l1ll_opy_():
            global bstack1lll1lllll_opy_
            if not bstack1lll1lllll_opy_:
                from bstack_utils.helper import bstack11l1llll1_opy_, bstack1lll11ll11_opy_
                bstack1lll1lllll_opy_ = bstack11l1llll1_opy_()
                bstack1lll11ll11_opy_(bstack1lllll11l_opy_)
            BrowserType.connect = bstack1ll1lll11_opy_
            return
        BrowserType.launch = bstack1l1l1l1lll_opy_
        bstack1lll1111_opy_ = True
    except Exception as e:
        pass
def bstack1llllll1ll1l_opy_():
    global CONFIG
    global bstack11lll111l_opy_
    global bstack11ll1111ll_opy_
    global bstack1l1lll11l1_opy_
    global bstack1lllll111_opy_
    global bstack11llll1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ⋐")))
    bstack11lll111l_opy_ = eval(os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ⋑")))
    bstack11ll1111ll_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ⋒"))
    bstack1l111l1l1l_opy_(CONFIG, bstack11lll111l_opy_)
    bstack11llll1lll_opy_ = bstack1111ll111_opy_.bstack1llll1111l_opy_(CONFIG, bstack11llll1lll_opy_)
    if cli.bstack11l11l111l_opy_():
        bstack1l1ll11ll_opy_.invoke(bstack11ll1l111_opy_.CONNECT, bstack11ll1111l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⋓"), bstack111lll_opy_ (u"ࠬ࠶ࠧ⋔")))
        cli.bstack1ll1lll1111_opy_(cli_context.platform_index)
        cli.bstack1llll11ll11_opy_(bstack11llll1l1l_opy_(bstack11ll1111ll_opy_, CONFIG), cli_context.platform_index, bstack1ll11l1l11_opy_)
        cli.bstack1lll1l111ll_opy_()
        logger.debug(bstack111lll_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⋕") + str(cli_context.platform_index) + bstack111lll_opy_ (u"ࠢࠣ⋖"))
        return # skip all existing bstack1lllllllll1l_opy_
    global bstack1l1l11111l_opy_
    global bstack1l1ll11111_opy_
    global bstack1ll1l11lll_opy_
    global bstack11ll1llll_opy_
    global bstack11l1ll11_opy_
    global bstack1l111l1l1_opy_
    global bstack11l11l1lll_opy_
    global bstack1llll11ll_opy_
    global bstack1l1111l1ll_opy_
    global bstack1ll1l11ll1_opy_
    global bstack1l1111l1_opy_
    global bstack1ll11l1111_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l11111l_opy_ = webdriver.Remote.__init__
        bstack1l1ll11111_opy_ = WebDriver.quit
        bstack11l11l1lll_opy_ = WebDriver.close
        bstack1llll11ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⋗") in CONFIG or bstack111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⋘") in CONFIG) and bstack1l1l1l1l1l_opy_():
        if bstack11l1ll1ll_opy_() < version.parse(bstack11l1l1111_opy_):
            logger.error(bstack1l11ll1ll_opy_.format(bstack11l1ll1ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack111lll_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⋙")) and callable(getattr(RemoteConnection, bstack111lll_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⋚"))):
                    bstack1l1111l1ll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1111l1ll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1l111ll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll1l11ll1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1111l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11l1l1ll1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll11l1111_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭⋛"))
    bstack1l1lll11l1_opy_ = CONFIG.get(bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ⋜"), {}).get(bstack111lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⋝"))
    bstack1lllll111_opy_ = True
    bstack1ll1ll1l1l_opy_(bstack111lllll_opy_)
if (bstack11l11111111_opy_()):
    bstack1llllll1ll1l_opy_()
@bstack111l1ll1l1_opy_(class_method=False)
def bstack1llllll1ll11_opy_(hook_name, event, bstack1l11l1l11ll_opy_=None):
    if hook_name not in [bstack111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⋞"), bstack111lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭⋟"), bstack111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⋠"), bstack111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⋡"), bstack111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⋢"), bstack111lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⋣"), bstack111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⋤"), bstack111lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ⋥")]:
        return
    node = store[bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⋦")]
    if hook_name in [bstack111lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⋧"), bstack111lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⋨")]:
        node = store[bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ⋩")]
    elif hook_name in [bstack111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⋪"), bstack111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⋫")]:
        node = store[bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭⋬")]
    hook_type = bstack1111l1ll1l1_opy_(hook_name)
    if event == bstack111lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⋭"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_[hook_type], bstack1lllll1111l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l11l1l1_opy_ = {
            bstack111lll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⋮"): uuid,
            bstack111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⋯"): bstack1llllllll1_opy_(),
            bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⋰"): bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⋱"),
            bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⋲"): hook_type,
            bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⋳"): hook_name
        }
        store[bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⋴")].append(uuid)
        bstack1llllll1l1ll_opy_ = node.nodeid
        if hook_type == bstack111lll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⋵"):
            if not _111l11lll1_opy_.get(bstack1llllll1l1ll_opy_, None):
                _111l11lll1_opy_[bstack1llllll1l1ll_opy_] = {bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⋶"): []}
            _111l11lll1_opy_[bstack1llllll1l1ll_opy_][bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⋷")].append(bstack111l11l1l1_opy_[bstack111lll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⋸")])
        _111l11lll1_opy_[bstack1llllll1l1ll_opy_ + bstack111lll_opy_ (u"ࠧ࠮ࠩ⋹") + hook_name] = bstack111l11l1l1_opy_
        bstack1llllll1l1l1_opy_(node, bstack111l11l1l1_opy_, bstack111lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⋺"))
    elif event == bstack111lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⋻"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11lllll_opy_[hook_type], bstack1lllll1111l_opy_.POST, node, None, bstack1l11l1l11ll_opy_)
            return
        bstack111llll11l_opy_ = node.nodeid + bstack111lll_opy_ (u"ࠪ࠱ࠬ⋼") + hook_name
        _111l11lll1_opy_[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⋽")] = bstack1llllllll1_opy_()
        bstack1llllll1111l_opy_(_111l11lll1_opy_[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠬࡻࡵࡪࡦࠪ⋾")])
        bstack1llllll1l1l1_opy_(node, _111l11lll1_opy_[bstack111llll11l_opy_], bstack111lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⋿"), bstack1llllll1llll_opy_=bstack1l11l1l11ll_opy_)
def bstack1lllllll1lll_opy_():
    global bstack1lllllll1ll1_opy_
    if bstack111ll111_opy_():
        bstack1lllllll1ll1_opy_ = bstack111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ⌀")
    else:
        bstack1lllllll1ll1_opy_ = bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⌁")
@bstack11111ll1l_opy_.bstack11111l11l1l_opy_
def bstack1llllll11l11_opy_():
    bstack1lllllll1lll_opy_()
    if cli.is_running():
        try:
            bstack111llll11l1_opy_(bstack1llllll1ll11_opy_)
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⌂").format(e))
        return
    if bstack1l1l1l1l1l_opy_():
        bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
        bstack111lll_opy_ (u"ࠪࠫࠬࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡃࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡩࡨࡸࡸࠦࡵࡴࡧࡧࠤ࡫ࡵࡲࠡࡣ࠴࠵ࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠮ࡹࡵࡥࡵࡶࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡶࡰࡱࠢࡁࠤ࠶࠲ࠠ࡮ࡱࡧࡣࡪࡾࡥࡤࡷࡷࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡳࡷࡱࠤࡧ࡫ࡣࡢࡷࡶࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡯࡮ࠡࡣࠣࡨ࡮࡬ࡦࡦࡴࡨࡲࡹࠦࡰࡳࡱࡦࡩࡸࡹࠠࡪࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡹࡸࠦࡷࡦࠢࡱࡩࡪࡪࠠࡵࡱࠣࡹࡸ࡫ࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࡒࡤࡸࡨ࡮ࠨࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠬࠤ࡫ࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠫࠬ࠭⌃")
        if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ⌄")):
            if CONFIG.get(bstack111lll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ⌅")) is not None and int(CONFIG[bstack111lll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⌆")]) > 1:
                bstack1llll1l1l_opy_(bstack11lll1ll11_opy_)
            return
        bstack1llll1l1l_opy_(bstack11lll1ll11_opy_)
    try:
        bstack111llll11l1_opy_(bstack1llllll1ll11_opy_)
    except Exception as e:
        logger.debug(bstack111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ⌇").format(e))
bstack1llllll11l11_opy_()