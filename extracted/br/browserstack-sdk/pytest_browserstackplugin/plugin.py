# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11ll1ll111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll111l1_opy_, bstack1lll1llll_opy_, update, bstack11lll1l11_opy_,
                                       bstack1l1ll1ll1l_opy_, bstack1ll1l11l1_opy_, bstack1ll1111l11_opy_, bstack1ll11ll1l1_opy_,
                                       bstack11lll111ll_opy_, bstack1lll111111_opy_, bstack11l1ll11ll_opy_,
                                       bstack11ll11llll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11l1lll1l1_opy_)
from browserstack_sdk.bstack1l11ll1111_opy_ import bstack11l111l11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1111l1l_opy_
from bstack_utils.capture import bstack1111ll1111_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1ll1l11_opy_, bstack1l1l1ll1ll_opy_, bstack111l11ll11_opy_, \
    bstack111l1ll1l_opy_
from bstack_utils.helper import bstack111ll1l1_opy_, bstack1111llllll1_opy_, bstack11111lllll_opy_, bstack1llllllll_opy_, bstack1l1l1111ll1_opy_, bstack1ll1llll11_opy_, \
    bstack111l111lll1_opy_, \
    bstack111l111llll_opy_, bstack1l1lll1l_opy_, bstack1l1l111ll_opy_, bstack111ll1l1l1l_opy_, bstack1l1l1l1l1l_opy_, Notset, \
    bstack1ll111ll1l_opy_, bstack111l111l11l_opy_, bstack111ll1l1l11_opy_, Result, bstack111l11l1l1l_opy_, bstack111l1l111l1_opy_, error_handler, \
    bstack1llll1111_opy_, bstack11ll11ll1l_opy_, bstack1ll1lll1l_opy_, bstack111ll1llll1_opy_
from bstack_utils.bstack1111ll1lll1_opy_ import bstack1111ll1l11l_opy_
from bstack_utils.messages import bstack1l1l1lll_opy_, bstack1111l1l1_opy_, bstack111l1l1111_opy_, bstack1l1lllll_opy_, bstack1ll1l111ll_opy_, \
    bstack11lllll1ll_opy_, bstack1lllllll11_opy_, bstack1l11lll1l_opy_, bstack1ll1ll11l1_opy_, bstack1l1ll11l1l_opy_, \
    bstack1ll1l11ll1_opy_, bstack1lll11ll1l_opy_, bstack1ll1l1l11l_opy_
from bstack_utils.proxy import bstack11l11lll1l_opy_, bstack11l11l1l1_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack1llll111ll11_opy_, bstack1llll111l1ll_opy_, bstack1llll111l1l1_opy_, bstack1llll11111l1_opy_, \
    bstack1llll111llll_opy_, bstack1llll1111l1l_opy_, bstack1llll111l11l_opy_, bstack1l111ll1l_opy_, bstack1llll1111l11_opy_
from bstack_utils.bstack1l11llll1l_opy_ import bstack1ll111l111_opy_
from bstack_utils.bstack111lllll1_opy_ import bstack1111l11l_opy_, bstack11llll11ll_opy_, bstack11lll1l1_opy_, \
    bstack1lllll1l1_opy_, bstack11111l11l_opy_
from bstack_utils.bstack1111ll11ll_opy_ import bstack111l1111ll_opy_
from bstack_utils.bstack1111llll11_opy_ import bstack1ll11l1l1l_opy_
import bstack_utils.accessibility as bstack1l11l1l1l_opy_
from bstack_utils.bstack1111lllll1_opy_ import bstack1l11111l1l_opy_
from bstack_utils.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack11111l1l_opy_
from browserstack_sdk.__init__ import bstack1l111lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11ll1_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack11lll11ll1_opy_ import bstack11lll11ll1_opy_, bstack1l1ll1l1ll_opy_, bstack111lll11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11lll11llll_opy_, bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack11lll11ll1_opy_ import bstack11lll11ll1_opy_, bstack1l1ll1l1ll_opy_, bstack111lll11l1_opy_
bstack1lll1111_opy_ = None
bstack11ll1l1l1l_opy_ = None
bstack11ll11ll_opy_ = None
bstack111lll11l_opy_ = None
bstack1l1llll1_opy_ = None
bstack11ll111l1_opy_ = None
bstack1ll1l1llll_opy_ = None
bstack1l1l1l1ll1_opy_ = None
bstack11l1111l_opy_ = None
bstack1llll1ll_opy_ = None
bstack1l111111l1_opy_ = None
bstack1lllll11ll_opy_ = None
bstack11l11lll1_opy_ = None
bstack11l1lllll_opy_ = bstack11l1ll1_opy_ (u"ࠨࠩ⎢")
CONFIG = {}
bstack11l1111lll_opy_ = False
bstack11ll1l1l1_opy_ = bstack11l1ll1_opy_ (u"ࠩࠪ⎣")
bstack1lllll1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠪࠫ⎤")
bstack1l11lll11_opy_ = False
bstack11l1llll1_opy_ = []
bstack11l11l11_opy_ = bstack1l1ll1l11_opy_
bstack1ll1lllllll1_opy_ = bstack11l1ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⎥")
bstack1ll11l111_opy_ = {}
bstack1l1ll111l1_opy_ = None
bstack111llll1l1_opy_ = False
logger = bstack1l1111l1l_opy_.get_logger(__name__, bstack11l11l11_opy_)
store = {
    bstack11l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⎦"): []
}
bstack1lll111l11ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11111l111l_opy_ = {}
current_test_uuid = None
cli_context = bstack11lll11llll_opy_(
    test_framework_name=bstack1l1l1l11l1_opy_[bstack11l1ll1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠳ࡂࡅࡆࠪ⎧")] if bstack1l1l1l1l1l_opy_() else bstack1l1l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚ࠧ⎨")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11lll1l1l_opy_(page, bstack1ll111l1ll_opy_):
    try:
        page.evaluate(bstack11l1ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⎩"),
                      bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭⎪") + json.dumps(
                          bstack1ll111l1ll_opy_) + bstack11l1ll1_opy_ (u"ࠥࢁࢂࠨ⎫"))
    except Exception as e:
        print(bstack11l1ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤ⎬"), e)
def bstack1lll1ll11_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1ll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⎭"), bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ⎮") + json.dumps(
            message) + bstack11l1ll1_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪ⎯") + json.dumps(level) + bstack11l1ll1_opy_ (u"ࠨࡿࢀࠫ⎰"))
    except Exception as e:
        print(bstack11l1ll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧ⎱"), e)
def pytest_configure(config):
    global bstack11ll1l1l1_opy_
    global CONFIG
    bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
    config.args = bstack1ll11l1l1l_opy_.bstack1lll111ll11l_opy_(config.args)
    bstack11lll111l_opy_.bstack11ll1111_opy_(bstack1ll1lll1l_opy_(config.getoption(bstack11l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ⎲"))))
    try:
        bstack1l1111l1l_opy_.bstack1111l1ll1ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack11lll11ll1_opy_.invoke(bstack1l1ll1l1ll_opy_.CONNECT, bstack111lll11l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⎳"), bstack11l1ll1_opy_ (u"ࠬ࠶ࠧ⎴")))
        config = json.loads(os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ⎵"), bstack11l1ll1_opy_ (u"ࠢࡼࡿࠥ⎶")))
        cli.bstack1ll1ll1llll_opy_(bstack1l1l111ll_opy_(bstack11ll1l1l1_opy_, CONFIG), cli_context.platform_index, bstack11lll1l11_opy_)
    if cli.bstack1lll1111l1l_opy_(bstack1ll111l1lll_opy_):
        cli.bstack1ll111l1l1l_opy_()
        logger.debug(bstack11l1ll1_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⎷") + str(cli_context.platform_index) + bstack11l1ll1_opy_ (u"ࠤࠥ⎸"))
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.BEFORE_ALL, bstack1ll1111llll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11l1ll1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣ⎹"), None)
    if cli.is_running() and when == bstack11l1ll1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⎺"):
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.LOG_REPORT, bstack1ll1111llll_opy_.PRE, item, call)
    outcome = yield
    if when == bstack11l1ll1_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ⎻"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⎼")))
        if not passed:
            config = json.loads(os.environ.get(bstack11l1ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ⎽"), bstack11l1ll1_opy_ (u"ࠣࡽࢀࠦ⎾")))
            if bstack11111l1l_opy_.bstack1lll1l1l_opy_(config):
                bstack1llllll1l1l1_opy_ = bstack11111l1l_opy_.bstack11ll1ll1l1_opy_(config)
                if item.execution_count > bstack1llllll1l1l1_opy_:
                    print(bstack11l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡲࡦࡶࡵ࡭ࡪࡹ࠺ࠡࠩ⎿"), report.nodeid, os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⏀")))
                    bstack11111l1l_opy_.bstack1lllllllll1l_opy_(report.nodeid)
            else:
                print(bstack11l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠫ⏁"), report.nodeid, os.environ.get(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⏂")))
                bstack11111l1l_opy_.bstack1lllllllll1l_opy_(report.nodeid)
        else:
            print(bstack11l1ll1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡵࡧࡳࡴࡧࡧ࠾ࠥ࠭⏃"), report.nodeid, os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⏄")))
    if cli.is_running():
        if when == bstack11l1ll1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⏅"):
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.BEFORE_EACH, bstack1ll1111llll_opy_.POST, item, call, outcome)
        elif when == bstack11l1ll1_opy_ (u"ࠤࡦࡥࡱࡲࠢ⏆"):
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.LOG_REPORT, bstack1ll1111llll_opy_.POST, item, call, outcome)
        elif when == bstack11l1ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ⏇"):
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.AFTER_EACH, bstack1ll1111llll_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack11l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⏈"))
    plugins = item.config.getoption(bstack11l1ll1_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨ⏉"))
    report = outcome.get_result()
    os.environ[bstack11l1ll1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⏊")] = report.nodeid
    bstack1lll1111llll_opy_(item, call, report)
    if bstack11l1ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧ⏋") not in plugins or bstack1l1l1l1l1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1ll1_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤ⏌"), None)
    page = getattr(item, bstack11l1ll1_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣ⏍"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1lll111111l1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1lll11111l11_opy_(item, report, summary, skipSessionName)
def bstack1lll111111l1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⏎") and report.skipped:
        bstack1llll1111l11_opy_(report)
    if report.when in [bstack11l1ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⏏"), bstack11l1ll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⏐")]:
        return
    if not bstack1l1l1111ll1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack11l1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ⏑")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ⏒") + json.dumps(
                    report.nodeid) + bstack11l1ll1_opy_ (u"ࠨࡿࢀࠫ⏓"))
        os.environ[bstack11l1ll1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⏔")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1ll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥ⏕").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⏖")))
    bstack1l11111lll_opy_ = bstack11l1ll1_opy_ (u"ࠧࠨ⏗")
    bstack1llll1111l11_opy_(report)
    if not passed:
        try:
            bstack1l11111lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1ll1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⏘").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11111lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1ll1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⏙")))
        bstack1l11111lll_opy_ = bstack11l1ll1_opy_ (u"ࠣࠤ⏚")
        if not passed:
            try:
                bstack1l11111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⏛").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11111lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ⏜")
                    + json.dumps(bstack11l1ll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧ⏝"))
                    + bstack11l1ll1_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ⏞")
                )
            else:
                item._driver.execute_script(
                    bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⏟")
                    + json.dumps(str(bstack1l11111lll_opy_))
                    + bstack11l1ll1_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ⏠")
                )
        except Exception as e:
            summary.append(bstack11l1ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨ⏡").format(e))
def bstack1lll1111l11l_opy_(test_name, error_message):
    try:
        bstack1ll1lllll1l1_opy_ = []
        bstack11ll11l1ll_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⏢"), bstack11l1ll1_opy_ (u"ࠪ࠴ࠬ⏣"))
        bstack1ll11l1l11_opy_ = {bstack11l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⏤"): test_name, bstack11l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⏥"): error_message, bstack11l1ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⏦"): bstack11ll11l1ll_opy_}
        bstack1lll111l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ⏧"))
        if os.path.exists(bstack1lll111l111l_opy_):
            with open(bstack1lll111l111l_opy_) as f:
                bstack1ll1lllll1l1_opy_ = json.load(f)
        bstack1ll1lllll1l1_opy_.append(bstack1ll11l1l11_opy_)
        with open(bstack1lll111l111l_opy_, bstack11l1ll1_opy_ (u"ࠨࡹࠪ⏨")) as f:
            json.dump(bstack1ll1lllll1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ⏩") + str(e))
def bstack1lll11111l11_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11l1ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⏪"), bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⏫")]:
        return
    if (str(skipSessionName).lower() != bstack11l1ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪ⏬")):
        bstack11lll1l1l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⏭")))
    bstack1l11111lll_opy_ = bstack11l1ll1_opy_ (u"ࠢࠣ⏮")
    bstack1llll1111l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l11111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1ll1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⏯").format(e)
                )
        try:
            if passed:
                bstack11111l11l_opy_(getattr(item, bstack11l1ll1_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⏰"), None), bstack11l1ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ⏱"))
            else:
                error_message = bstack11l1ll1_opy_ (u"ࠫࠬ⏲")
                if bstack1l11111lll_opy_:
                    bstack1lll1ll11_opy_(item._page, str(bstack1l11111lll_opy_), bstack11l1ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ⏳"))
                    bstack11111l11l_opy_(getattr(item, bstack11l1ll1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⏴"), None), bstack11l1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ⏵"), str(bstack1l11111lll_opy_))
                    error_message = str(bstack1l11111lll_opy_)
                else:
                    bstack11111l11l_opy_(getattr(item, bstack11l1ll1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⏶"), None), bstack11l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⏷"))
                bstack1lll1111l11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1ll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ⏸").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11l1ll1_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ⏹"), default=bstack11l1ll1_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⏺"), help=bstack11l1ll1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⏻"))
    parser.addoption(bstack11l1ll1_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ⏼"), default=bstack11l1ll1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ⏽"), help=bstack11l1ll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ⏾"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1ll1_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ⏿"), action=bstack11l1ll1_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ␀"), default=bstack11l1ll1_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ␁"),
                         help=bstack11l1ll1_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ␂"))
def bstack1111l1llll_opy_(log):
    if not (log[bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ␃")] and log[bstack11l1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ␄")].strip()):
        return
    active = bstack1111lll11l_opy_()
    log = {
        bstack11l1ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ␅"): log[bstack11l1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ␆")],
        bstack11l1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ␇"): bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"ࠬࡠࠧ␈"),
        bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ␉"): log[bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ␊")],
    }
    if active:
        if active[bstack11l1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭␋")] == bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ␌"):
            log[bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ␍")] = active[bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ␎")]
        elif active[bstack11l1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ␏")] == bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ␐"):
            log[bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ␑")] = active[bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ␒")]
    bstack1l11111l1l_opy_.bstack1111llll1_opy_([log])
def bstack1111lll11l_opy_():
    if len(store[bstack11l1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭␓")]) > 0 and store[bstack11l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ␔")][-1]:
        return {
            bstack11l1ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ␕"): bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ␖"),
            bstack11l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭␗"): store[bstack11l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ␘")][-1]
        }
    if store.get(bstack11l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ␙"), None):
        return {
            bstack11l1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ␚"): bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨ␛"),
            bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ␜"): store[bstack11l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ␝")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.INIT_TEST, bstack1ll1111llll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.INIT_TEST, bstack1ll1111llll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1ll1lllll1ll_opy_ = True
        bstack1l11l1ll_opy_ = bstack1l11l1l1l_opy_.bstack1lll1l1lll_opy_(bstack111l111llll_opy_(item.own_markers))
        if not cli.bstack1lll1111l1l_opy_(bstack1ll111l1lll_opy_):
            item._a11y_test_case = bstack1l11l1ll_opy_
            if bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ␞"), None):
                driver = getattr(item, bstack11l1ll1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ␟"), None)
                item._a11y_started = bstack1l11l1l1l_opy_.bstack1ll1l1ll1l_opy_(driver, bstack1l11l1ll_opy_)
        if not bstack1l11111l1l_opy_.on() or bstack1ll1lllllll1_opy_ != bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ␠"):
            return
        global current_test_uuid #, bstack1111l1l1ll_opy_
        bstack111111ll1l_opy_ = {
            bstack11l1ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ␡"): uuid4().__str__(),
            bstack11l1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ␢"): bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"ࠫ࡟࠭␣")
        }
        current_test_uuid = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ␤")]
        store[bstack11l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ␥")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ␦")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11111l111l_opy_[item.nodeid] = {**_11111l111l_opy_[item.nodeid], **bstack111111ll1l_opy_}
        bstack1lll111l1l1l_opy_(item, _11111l111l_opy_[item.nodeid], bstack11l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ␧"))
    except Exception as err:
        print(bstack11l1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫ␨"), str(err))
def pytest_runtest_setup(item):
    store[bstack11l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ␩")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.BEFORE_EACH, bstack1ll1111llll_opy_.PRE, item, bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ␪"))
    if bstack11111l1l_opy_.bstack111111lll1l_opy_():
            bstack1ll1llllll11_opy_ = bstack11l1ll1_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡧࡳࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ␫")
            logger.error(bstack1ll1llllll11_opy_)
            bstack111111ll1l_opy_ = {
                bstack11l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ␬"): uuid4().__str__(),
                bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ␭"): bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"ࠨ࡜ࠪ␮"),
                bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ␯"): bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"ࠪ࡞ࠬ␰"),
                bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ␱"): bstack11l1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭␲"),
                bstack11l1ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭␳"): bstack1ll1llllll11_opy_,
                bstack11l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭␴"): [],
                bstack11l1ll1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ␵"): []
            }
            bstack1lll111l1l1l_opy_(item, bstack111111ll1l_opy_, bstack11l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ␶"))
            pytest.skip(bstack1ll1llllll11_opy_)
            return # skip all existing operations
    global bstack1lll111l11ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111ll1l1l1l_opy_():
        atexit.register(bstack111l1l11_opy_)
        if not bstack1lll111l11ll_opy_:
            try:
                bstack1lll111l11l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111ll1llll1_opy_():
                    bstack1lll111l11l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll111l11l1_opy_:
                    signal.signal(s, bstack1lll1111l1l1_opy_)
                bstack1lll111l11ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l1ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦ␷") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llll111ll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ␸")
    try:
        if not bstack1l11111l1l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111111ll1l_opy_ = {
            bstack11l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ␹"): uuid,
            bstack11l1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ␺"): bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"࡛ࠧࠩ␻"),
            bstack11l1ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭␼"): bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ␽"),
            bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭␾"): bstack11l1ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ␿"),
            bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⑀"): bstack11l1ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⑁")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⑂")] = item
        store[bstack11l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⑃")] = [uuid]
        if not _11111l111l_opy_.get(item.nodeid, None):
            _11111l111l_opy_[item.nodeid] = {bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⑄"): [], bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⑅"): []}
        _11111l111l_opy_[item.nodeid][bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⑆")].append(bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⑇")])
        _11111l111l_opy_[item.nodeid + bstack11l1ll1_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭⑈")] = bstack111111ll1l_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1lll11111l1l_opy_(item, bstack111111ll1l_opy_, bstack11l1ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⑉"))
    except Exception as err:
        print(bstack11l1ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ⑊"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.AFTER_EACH, bstack1ll1111llll_opy_.PRE, item, bstack11l1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⑋"))
        return # skip all existing operations
    try:
        global bstack1ll11l111_opy_
        bstack11ll11l1ll_opy_ = 0
        if bstack1l11lll11_opy_ is True:
            bstack11ll11l1ll_opy_ = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⑌")))
        if bstack111llll11_opy_.bstack1l11l111l_opy_() == bstack11l1ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤ⑍"):
            if bstack111llll11_opy_.bstack1l111l11_opy_() == bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⑎"):
                bstack1lll1111l1ll_opy_ = bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⑏"), None)
                bstack1l11ll1ll_opy_ = bstack1lll1111l1ll_opy_ + bstack11l1ll1_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥ⑐")
                driver = getattr(item, bstack11l1ll1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⑑"), None)
                bstack11l1ll1l1l_opy_ = getattr(item, bstack11l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⑒"), None)
                bstack11ll1l1l_opy_ = getattr(item, bstack11l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⑓"), None)
                PercySDK.screenshot(driver, bstack1l11ll1ll_opy_, bstack11l1ll1l1l_opy_=bstack11l1ll1l1l_opy_, bstack11ll1l1l_opy_=bstack11ll1l1l_opy_, bstack1lll1ll1l1_opy_=bstack11ll11l1ll_opy_)
        if not cli.bstack1lll1111l1l_opy_(bstack1ll111l1lll_opy_):
            if getattr(item, bstack11l1ll1_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ⑔"), False):
                bstack11l111l11l_opy_.bstack11l1l1l11l_opy_(getattr(item, bstack11l1ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⑕"), None), bstack1ll11l111_opy_, logger, item)
        if not bstack1l11111l1l_opy_.on():
            return
        bstack111111ll1l_opy_ = {
            bstack11l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⑖"): uuid4().__str__(),
            bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⑗"): bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"ࠨ࡜ࠪ⑘"),
            bstack11l1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⑙"): bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⑚"),
            bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⑛"): bstack11l1ll1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⑜"),
            bstack11l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⑝"): bstack11l1ll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⑞")
        }
        _11111l111l_opy_[item.nodeid + bstack11l1ll1_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ⑟")] = bstack111111ll1l_opy_
        bstack1lll11111l1l_opy_(item, bstack111111ll1l_opy_, bstack11l1ll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ①"))
    except Exception as err:
        print(bstack11l1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩ②"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1llll11111l1_opy_(fixturedef.argname):
        store[bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ③")] = request.node
    elif bstack1llll111llll_opy_(fixturedef.argname):
        store[bstack11l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ④")] = request.node
    if not bstack1l11111l1l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.SETUP_FIXTURE, bstack1ll1111llll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.SETUP_FIXTURE, bstack1ll1111llll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.SETUP_FIXTURE, bstack1ll1111llll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.SETUP_FIXTURE, bstack1ll1111llll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack11l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⑤"): fixturedef.argname,
            bstack11l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⑥"): bstack111l111lll1_opy_(outcome),
            bstack11l1ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⑦"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l1ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⑧")]
        if not _11111l111l_opy_.get(current_test_item.nodeid, None):
            _11111l111l_opy_[current_test_item.nodeid] = {bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⑨"): []}
        _11111l111l_opy_[current_test_item.nodeid][bstack11l1ll1_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⑩")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ⑪"), str(err))
if bstack1l1l1l1l1l_opy_() and bstack1l11111l1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.STEP, bstack1ll1111llll_opy_.PRE, request, step)
            return
        try:
            _11111l111l_opy_[request.node.nodeid][bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⑫")].bstack11lllll11_opy_(id(step))
        except Exception as err:
            print(bstack11l1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ⑬"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.STEP, bstack1ll1111llll_opy_.POST, request, step, exception)
            return
        try:
            _11111l111l_opy_[request.node.nodeid][bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⑭")].bstack1111l1l11l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭⑮"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.STEP, bstack1ll1111llll_opy_.POST, request, step)
            return
        try:
            bstack1111ll11ll_opy_: bstack111l1111ll_opy_ = _11111l111l_opy_[request.node.nodeid][bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⑯")]
            bstack1111ll11ll_opy_.bstack1111l1l11l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ⑰"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll1lllllll1_opy_
        try:
            if not bstack1l11111l1l_opy_.on() or bstack1ll1lllllll1_opy_ != bstack11l1ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⑱"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ⑲"), None)
            if not _11111l111l_opy_.get(request.node.nodeid, None):
                _11111l111l_opy_[request.node.nodeid] = {}
            bstack1111ll11ll_opy_ = bstack111l1111ll_opy_.bstack1lll1l1lll1l_opy_(
                scenario, feature, request.node,
                name=bstack1llll1111l1l_opy_(request.node, scenario),
                started_at=bstack1ll1llll11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ⑳"),
                tags=bstack1llll111l11l_opy_(feature, scenario),
                bstack1111l1l1l1_opy_=bstack1l11111l1l_opy_.bstack1111ll1l11_opy_(driver) if driver and driver.session_id else {}
            )
            _11111l111l_opy_[request.node.nodeid][bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⑴")] = bstack1111ll11ll_opy_
            bstack1lll111l1l11_opy_(bstack1111ll11ll_opy_.uuid)
            bstack1l11111l1l_opy_.bstack1111ll111l_opy_(bstack11l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⑵"), bstack1111ll11ll_opy_)
        except Exception as err:
            print(bstack11l1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ⑶"), str(err))
def bstack1lll1111lll1_opy_(bstack1111l1ll11_opy_):
    if bstack1111l1ll11_opy_ in store[bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⑷")]:
        store[bstack11l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⑸")].remove(bstack1111l1ll11_opy_)
def bstack1lll111l1l11_opy_(test_uuid):
    store[bstack11l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⑹")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l11111l1l_opy_.bstack1lll11l1lll1_opy_
def bstack1lll1111llll_opy_(item, call, report):
    logger.debug(bstack11l1ll1_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩ⑺"))
    global bstack1ll1lllllll1_opy_
    bstack11lll11l1l_opy_ = bstack1ll1llll11_opy_()
    if hasattr(report, bstack11l1ll1_opy_ (u"ࠨࡵࡷࡳࡵ࠭⑻")):
        bstack11lll11l1l_opy_ = bstack111l11l1l1l_opy_(report.stop)
    elif hasattr(report, bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ⑼")):
        bstack11lll11l1l_opy_ = bstack111l11l1l1l_opy_(report.start)
    try:
        if getattr(report, bstack11l1ll1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⑽"), bstack11l1ll1_opy_ (u"ࠫࠬ⑾")) == bstack11l1ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⑿"):
            logger.debug(bstack11l1ll1_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ⒀").format(getattr(report, bstack11l1ll1_opy_ (u"ࠧࡸࡪࡨࡲࠬ⒁"), bstack11l1ll1_opy_ (u"ࠨࠩ⒂")).__str__(), bstack1ll1lllllll1_opy_))
            if bstack1ll1lllllll1_opy_ == bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⒃"):
                _11111l111l_opy_[item.nodeid][bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⒄")] = bstack11lll11l1l_opy_
                bstack1lll111l1l1l_opy_(item, _11111l111l_opy_[item.nodeid], bstack11l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⒅"), report, call)
                store[bstack11l1ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⒆")] = None
            elif bstack1ll1lllllll1_opy_ == bstack11l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ⒇"):
                bstack1111ll11ll_opy_ = _11111l111l_opy_[item.nodeid][bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⒈")]
                bstack1111ll11ll_opy_.set(hooks=_11111l111l_opy_[item.nodeid].get(bstack11l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⒉"), []))
                exception, bstack1111llll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1111llll1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l1ll1_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ⒊"), bstack11l1ll1_opy_ (u"ࠪࠫ⒋"))]
                bstack1111ll11ll_opy_.stop(time=bstack11lll11l1l_opy_, result=Result(result=getattr(report, bstack11l1ll1_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⒌"), bstack11l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⒍")), exception=exception, bstack1111llll1l_opy_=bstack1111llll1l_opy_))
                bstack1l11111l1l_opy_.bstack1111ll111l_opy_(bstack11l1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⒎"), _11111l111l_opy_[item.nodeid][bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⒏")])
        elif getattr(report, bstack11l1ll1_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⒐"), bstack11l1ll1_opy_ (u"ࠩࠪ⒑")) in [bstack11l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⒒"), bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⒓")]:
            logger.debug(bstack11l1ll1_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⒔").format(getattr(report, bstack11l1ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫ⒕"), bstack11l1ll1_opy_ (u"ࠧࠨ⒖")).__str__(), bstack1ll1lllllll1_opy_))
            bstack1111ll1l1l_opy_ = item.nodeid + bstack11l1ll1_opy_ (u"ࠨ࠯ࠪ⒗") + getattr(report, bstack11l1ll1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⒘"), bstack11l1ll1_opy_ (u"ࠪࠫ⒙"))
            if getattr(report, bstack11l1ll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⒚"), False):
                hook_type = bstack11l1ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⒛") if getattr(report, bstack11l1ll1_opy_ (u"࠭ࡷࡩࡧࡱࠫ⒜"), bstack11l1ll1_opy_ (u"ࠧࠨ⒝")) == bstack11l1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⒞") else bstack11l1ll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⒟")
                _11111l111l_opy_[bstack1111ll1l1l_opy_] = {
                    bstack11l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⒠"): uuid4().__str__(),
                    bstack11l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⒡"): bstack11lll11l1l_opy_,
                    bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⒢"): hook_type
                }
            _11111l111l_opy_[bstack1111ll1l1l_opy_][bstack11l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⒣")] = bstack11lll11l1l_opy_
            bstack1lll1111lll1_opy_(_11111l111l_opy_[bstack1111ll1l1l_opy_][bstack11l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⒤")])
            bstack1lll11111l1l_opy_(item, _11111l111l_opy_[bstack1111ll1l1l_opy_], bstack11l1ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⒥"), report, call)
            if getattr(report, bstack11l1ll1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⒦"), bstack11l1ll1_opy_ (u"ࠪࠫ⒧")) == bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⒨"):
                if getattr(report, bstack11l1ll1_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⒩"), bstack11l1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⒪")) == bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⒫"):
                    bstack111111ll1l_opy_ = {
                        bstack11l1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⒬"): uuid4().__str__(),
                        bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⒭"): bstack1ll1llll11_opy_(),
                        bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⒮"): bstack1ll1llll11_opy_()
                    }
                    _11111l111l_opy_[item.nodeid] = {**_11111l111l_opy_[item.nodeid], **bstack111111ll1l_opy_}
                    bstack1lll111l1l1l_opy_(item, _11111l111l_opy_[item.nodeid], bstack11l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⒯"))
                    bstack1lll111l1l1l_opy_(item, _11111l111l_opy_[item.nodeid], bstack11l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⒰"), report, call)
    except Exception as err:
        print(bstack11l1ll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ⒱"), str(err))
def bstack1lll11111111_opy_(test, bstack111111ll1l_opy_, result=None, call=None, bstack1lllll1111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1111ll11ll_opy_ = {
        bstack11l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⒲"): bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⒳")],
        bstack11l1ll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⒴"): bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࠨ⒵"),
        bstack11l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩⒶ"): test.name,
        bstack11l1ll1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪⒷ"): {
            bstack11l1ll1_opy_ (u"࠭࡬ࡢࡰࡪࠫⒸ"): bstack11l1ll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧⒹ"),
            bstack11l1ll1_opy_ (u"ࠨࡥࡲࡨࡪ࠭Ⓔ"): inspect.getsource(test.obj)
        },
        bstack11l1ll1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ⓕ"): test.name,
        bstack11l1ll1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩⒼ"): test.name,
        bstack11l1ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫⒽ"): bstack1ll11l1l1l_opy_.bstack11111l11l1_opy_(test),
        bstack11l1ll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨⒾ"): file_path,
        bstack11l1ll1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨⒿ"): file_path,
        bstack11l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧⓀ"): bstack11l1ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩⓁ"),
        bstack11l1ll1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧⓂ"): file_path,
        bstack11l1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧⓃ"): bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨⓄ")],
        bstack11l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨⓅ"): bstack11l1ll1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭Ⓠ"),
        bstack11l1ll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪⓇ"): {
            bstack11l1ll1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬⓈ"): test.nodeid
        },
        bstack11l1ll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧⓉ"): bstack111l111llll_opy_(test.own_markers)
    }
    if bstack1lllll1111_opy_ in [bstack11l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫⓊ"), bstack11l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ⓥ")]:
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠬࡳࡥࡵࡣࠪⓌ")] = {
            bstack11l1ll1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨⓍ"): bstack111111ll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩⓎ"), [])
        }
    if bstack1lllll1111_opy_ == bstack11l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩⓏ"):
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩⓐ")] = bstack11l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫⓑ")
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪⓒ")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫⓓ")]
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫⓔ")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬⓕ")]
    if result:
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨⓖ")] = result.outcome
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪⓗ")] = result.duration * 1000
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨⓘ")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⓙ")]
        if result.failed:
            bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫⓚ")] = bstack1l11111l1l_opy_.bstack1llll11111l_opy_(call.excinfo.typename)
            bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧⓛ")] = bstack1l11111l1l_opy_.bstack1lll11l1ll1l_opy_(call.excinfo, result)
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ⓜ")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧⓝ")]
    if outcome:
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩⓞ")] = bstack111l111lll1_opy_(outcome)
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫⓟ")] = 0
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩⓠ")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪⓡ")]
        if bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ⓢ")] == bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧⓣ"):
            bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧⓤ")] = bstack11l1ll1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪⓥ")  # bstack1lll1111ll1l_opy_
            bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫⓦ")] = [{bstack11l1ll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧⓧ"): [bstack11l1ll1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩⓨ")]}]
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬⓩ")] = bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⓪")]
    return bstack1111ll11ll_opy_
def bstack1lll111111ll_opy_(test, bstack111111l1ll_opy_, bstack1lllll1111_opy_, result, call, outcome, bstack1ll1llllll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⓫")]
    hook_name = bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⓬")]
    hook_data = {
        bstack11l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⓭"): bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩ⓮")],
        bstack11l1ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ⓯"): bstack11l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⓰"),
        bstack11l1ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⓱"): bstack11l1ll1_opy_ (u"ࠨࡽࢀࠫ⓲").format(bstack1llll111l1ll_opy_(hook_name)),
        bstack11l1ll1_opy_ (u"ࠩࡥࡳࡩࡿࠧ⓳"): {
            bstack11l1ll1_opy_ (u"ࠪࡰࡦࡴࡧࠨ⓴"): bstack11l1ll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⓵"),
            bstack11l1ll1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⓶"): None
        },
        bstack11l1ll1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⓷"): test.name,
        bstack11l1ll1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⓸"): bstack1ll11l1l1l_opy_.bstack11111l11l1_opy_(test, hook_name),
        bstack11l1ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⓹"): file_path,
        bstack11l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⓺"): file_path,
        bstack11l1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⓻"): bstack11l1ll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⓼"),
        bstack11l1ll1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⓽"): file_path,
        bstack11l1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⓾"): bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⓿")],
        bstack11l1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ─"): bstack11l1ll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ━") if bstack1ll1lllllll1_opy_ == bstack11l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ│") else bstack11l1ll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ┃"),
        bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ┄"): hook_type
    }
    bstack1l1lll111l1_opy_ = bstack111111ll11_opy_(_11111l111l_opy_.get(test.nodeid, None))
    if bstack1l1lll111l1_opy_:
        hook_data[bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ┅")] = bstack1l1lll111l1_opy_
    if result:
        hook_data[bstack11l1ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ┆")] = result.outcome
        hook_data[bstack11l1ll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ┇")] = result.duration * 1000
        hook_data[bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ┈")] = bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ┉")]
        if result.failed:
            hook_data[bstack11l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ┊")] = bstack1l11111l1l_opy_.bstack1llll11111l_opy_(call.excinfo.typename)
            hook_data[bstack11l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭┋")] = bstack1l11111l1l_opy_.bstack1lll11l1ll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭┌")] = bstack111l111lll1_opy_(outcome)
        hook_data[bstack11l1ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ┍")] = 100
        hook_data[bstack11l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭┎")] = bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ┏")]
        if hook_data[bstack11l1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ┐")] == bstack11l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ┑"):
            hook_data[bstack11l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ┒")] = bstack11l1ll1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ┓")  # bstack1lll1111ll1l_opy_
            hook_data[bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ└")] = [{bstack11l1ll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ┕"): [bstack11l1ll1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭┖")]}]
    if bstack1ll1llllll1l_opy_:
        hook_data[bstack11l1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ┗")] = bstack1ll1llllll1l_opy_.result
        hook_data[bstack11l1ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ┘")] = bstack111l111l11l_opy_(bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ┙")], bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ┚")])
        hook_data[bstack11l1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ┛")] = bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭├")]
        if hook_data[bstack11l1ll1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ┝")] == bstack11l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ┞"):
            hook_data[bstack11l1ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ┟")] = bstack1l11111l1l_opy_.bstack1llll11111l_opy_(bstack1ll1llllll1l_opy_.exception_type)
            hook_data[bstack11l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭┠")] = [{bstack11l1ll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ┡"): bstack111ll1l1l11_opy_(bstack1ll1llllll1l_opy_.exception)}]
    return hook_data
def bstack1lll111l1l1l_opy_(test, bstack111111ll1l_opy_, bstack1lllll1111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11l1ll1_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ┢").format(bstack1lllll1111_opy_))
    bstack1111ll11ll_opy_ = bstack1lll11111111_opy_(test, bstack111111ll1l_opy_, result, call, bstack1lllll1111_opy_, outcome)
    driver = getattr(test, bstack11l1ll1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ┣"), None)
    if bstack1lllll1111_opy_ == bstack11l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ┤") and driver:
        bstack1111ll11ll_opy_[bstack11l1ll1_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ┥")] = bstack1l11111l1l_opy_.bstack1111ll1l11_opy_(driver)
    if bstack1lllll1111_opy_ == bstack11l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ┦"):
        bstack1lllll1111_opy_ = bstack11l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ┧")
    bstack11111l1l11_opy_ = {
        bstack11l1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ┨"): bstack1lllll1111_opy_,
        bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ┩"): bstack1111ll11ll_opy_
    }
    bstack1l11111l1l_opy_.bstack1111l11ll_opy_(bstack11111l1l11_opy_)
    if bstack1lllll1111_opy_ == bstack11l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ┪"):
        threading.current_thread().bstackTestMeta = {bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ┫"): bstack11l1ll1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ┬")}
    elif bstack1lllll1111_opy_ == bstack11l1ll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭┭"):
        threading.current_thread().bstackTestMeta = {bstack11l1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ┮"): getattr(result, bstack11l1ll1_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ┯"), bstack11l1ll1_opy_ (u"ࠧࠨ┰"))}
def bstack1lll11111l1l_opy_(test, bstack111111ll1l_opy_, bstack1lllll1111_opy_, result=None, call=None, outcome=None, bstack1ll1llllll1l_opy_=None):
    logger.debug(bstack11l1ll1_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ┱").format(bstack1lllll1111_opy_))
    hook_data = bstack1lll111111ll_opy_(test, bstack111111ll1l_opy_, bstack1lllll1111_opy_, result, call, outcome, bstack1ll1llllll1l_opy_)
    bstack11111l1l11_opy_ = {
        bstack11l1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭┲"): bstack1lllll1111_opy_,
        bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ┳"): hook_data
    }
    bstack1l11111l1l_opy_.bstack1111l11ll_opy_(bstack11111l1l11_opy_)
def bstack111111ll11_opy_(bstack111111ll1l_opy_):
    if not bstack111111ll1l_opy_:
        return None
    if bstack111111ll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ┴"), None):
        return getattr(bstack111111ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ┵")], bstack11l1ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ┶"), None)
    return bstack111111ll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ┷"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.LOG, bstack1ll1111llll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_.LOG, bstack1ll1111llll_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack1l11111l1l_opy_.on():
            return
        places = [bstack11l1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ┸"), bstack11l1ll1_opy_ (u"ࠩࡦࡥࡱࡲࠧ┹"), bstack11l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ┺")]
        logs = []
        for bstack1lll1111ll11_opy_ in places:
            records = caplog.get_records(bstack1lll1111ll11_opy_)
            bstack1lll11111ll1_opy_ = bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ┻") if bstack1lll1111ll11_opy_ == bstack11l1ll1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ┼") else bstack11l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┽")
            bstack1ll1llllllll_opy_ = request.node.nodeid + (bstack11l1ll1_opy_ (u"ࠧࠨ┾") if bstack1lll1111ll11_opy_ == bstack11l1ll1_opy_ (u"ࠨࡥࡤࡰࡱ࠭┿") else bstack11l1ll1_opy_ (u"ࠩ࠰ࠫ╀") + bstack1lll1111ll11_opy_)
            test_uuid = bstack111111ll11_opy_(_11111l111l_opy_.get(bstack1ll1llllllll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l1l111l1_opy_(record.message):
                    continue
                logs.append({
                    bstack11l1ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭╁"): bstack1111llllll1_opy_(record.created).isoformat() + bstack11l1ll1_opy_ (u"ࠫ࡟࠭╂"),
                    bstack11l1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ╃"): record.levelname,
                    bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ╄"): record.message,
                    bstack1lll11111ll1_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l11111l1l_opy_.bstack1111llll1_opy_(logs)
    except Exception as err:
        print(bstack11l1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ╅"), str(err))
def bstack1l1ll11l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack111llll1l1_opy_
    bstack111ll11ll1_opy_ = bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ╆"), None) and bstack111ll1l1_opy_(
            threading.current_thread(), bstack11l1ll1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ╇"), None)
    bstack1lll11l1l1_opy_ = getattr(driver, bstack11l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ╈"), None) != None and getattr(driver, bstack11l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ╉"), None) == True
    if sequence == bstack11l1ll1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ╊") and driver != None:
      if not bstack111llll1l1_opy_ and bstack1l1l1111ll1_opy_() and bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭╋") in CONFIG and CONFIG[bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ╌")] == True and bstack1lll1ll11l_opy_.bstack1111lll1l_opy_(driver_command) and (bstack1lll11l1l1_opy_ or bstack111ll11ll1_opy_) and not bstack11l1lll1l1_opy_(args):
        try:
          bstack111llll1l1_opy_ = True
          logger.debug(bstack11l1ll1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ╍").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l1ll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ╎").format(str(err)))
        bstack111llll1l1_opy_ = False
    if sequence == bstack11l1ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ╏"):
        if driver_command == bstack11l1ll1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ═"):
            bstack1l11111l1l_opy_.bstack1111l111_opy_({
                bstack11l1ll1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ║"): response[bstack11l1ll1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ╒")],
                bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ╓"): store[bstack11l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ╔")]
            })
def bstack111l1l11_opy_():
    global bstack11l1llll1_opy_
    bstack1l1111l1l_opy_.bstack11llllll1_opy_()
    logging.shutdown()
    bstack1l11111l1l_opy_.bstack111111llll_opy_()
    for driver in bstack11l1llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1111l1l1_opy_(*args):
    global bstack11l1llll1_opy_
    bstack1l11111l1l_opy_.bstack111111llll_opy_()
    for driver in bstack11l1llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111lll11_opy_, stage=STAGE.bstack11lll1l1l1_opy_, bstack1ll1l111l_opy_=bstack1l1ll111l1_opy_)
def bstack1l11ll11l_opy_(self, *args, **kwargs):
    bstack1llll11l1l_opy_ = bstack1lll1111_opy_(self, *args, **kwargs)
    bstack1ll11l1l1_opy_ = getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ╕"), None)
    if bstack1ll11l1l1_opy_ and bstack1ll11l1l1_opy_.get(bstack11l1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ╖"), bstack11l1ll1_opy_ (u"ࠫࠬ╗")) == bstack11l1ll1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭╘"):
        bstack1l11111l1l_opy_.bstack1l11l1l11l_opy_(self)
    return bstack1llll11l1l_opy_
@measure(event_name=EVENTS.bstack11llll1l1_opy_, stage=STAGE.bstack11ll1lll1l_opy_, bstack1ll1l111l_opy_=bstack1l1ll111l1_opy_)
def bstack1l1ll1l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
    if bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ╙")):
        return
    bstack11lll111l_opy_.bstack1l1l1111ll_opy_(bstack11l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ╚"), True)
    global bstack11l1lllll_opy_
    global bstack11l111ll_opy_
    bstack11l1lllll_opy_ = framework_name
    logger.info(bstack1lll11ll1l_opy_.format(bstack11l1lllll_opy_.split(bstack11l1ll1_opy_ (u"ࠨ࠯ࠪ╛"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1l1111ll1_opy_():
            Service.start = bstack1ll1111l11_opy_
            Service.stop = bstack1ll11ll1l1_opy_
            webdriver.Remote.get = bstack11l111lll1_opy_
            webdriver.Remote.__init__ = bstack1l111l1ll_opy_
            if not isinstance(os.getenv(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ╜")), str):
                return
            WebDriver.quit = bstack1ll1l1l1ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l11111l1l_opy_.on():
            webdriver.Remote.__init__ = bstack1l11ll11l_opy_
        bstack11l111ll_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ╝")):
        bstack11l111ll_opy_ = eval(os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ╞")))
    if not bstack11l111ll_opy_:
        bstack1lll111111_opy_(bstack11l1ll1_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ╟"), bstack1ll1l11ll1_opy_)
    if bstack111111ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack11l1ll1_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ╠")) and callable(getattr(RemoteConnection, bstack11l1ll1_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ╡"))):
                RemoteConnection._get_proxy_url = bstack1ll1lll111_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1ll1lll111_opy_
        except Exception as e:
            logger.error(bstack11lllll1ll_opy_.format(str(e)))
    if bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ╢") in str(framework_name).lower():
        if not bstack1l1l1111ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1ll1ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l11l1_opy_
            Config.getoption = bstack11111l111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l111ll111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1lll111l_opy_, stage=STAGE.bstack11lll1l1l1_opy_, bstack1ll1l111l_opy_=bstack1l1ll111l1_opy_)
def bstack1ll1l1l1ll_opy_(self):
    global bstack11l1lllll_opy_
    global bstack1111lll11_opy_
    global bstack11ll1l1l1l_opy_
    try:
        if bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ╣") in bstack11l1lllll_opy_ and self.session_id != None and bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ╤"), bstack11l1ll1_opy_ (u"ࠫࠬ╥")) != bstack11l1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭╦"):
            bstack1l1ll1l11l_opy_ = bstack11l1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭╧") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ╨")
            bstack11ll11ll1l_opy_(logger, True)
            if os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ╩"), None):
                self.execute_script(
                    bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ╪") + json.dumps(
                        os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭╫"))) + bstack11l1ll1_opy_ (u"ࠫࢂࢃࠧ╬"))
            if self != None:
                bstack1lllll1l1_opy_(self, bstack1l1ll1l11l_opy_, bstack11l1ll1_opy_ (u"ࠬ࠲ࠠࠨ╭").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1lll1111l1l_opy_(bstack1ll111l1lll_opy_):
            item = store.get(bstack11l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ╮"), None)
            if item is not None and bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭╯"), None):
                bstack11l111l11l_opy_.bstack11l1l1l11l_opy_(self, bstack1ll11l111_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l1ll1_opy_ (u"ࠨࠩ╰")
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ╱") + str(e))
    bstack11ll1l1l1l_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack111lll11ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_, bstack1ll1l111l_opy_=bstack1l1ll111l1_opy_)
def bstack1l111l1ll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1111lll11_opy_
    global bstack1l1ll111l1_opy_
    global bstack1l11lll11_opy_
    global bstack11l1lllll_opy_
    global bstack1lll1111_opy_
    global bstack11l1llll1_opy_
    global bstack11ll1l1l1_opy_
    global bstack1lllll1l1l_opy_
    global bstack1ll11l111_opy_
    CONFIG[bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ╲")] = str(bstack11l1lllll_opy_) + str(__version__)
    command_executor = bstack1l1l111ll_opy_(bstack11ll1l1l1_opy_, CONFIG)
    logger.debug(bstack1l1lllll_opy_.format(command_executor))
    proxy = bstack11ll11llll_opy_(CONFIG, proxy)
    bstack11ll11l1ll_opy_ = 0
    try:
        if bstack1l11lll11_opy_ is True:
            bstack11ll11l1ll_opy_ = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ╳")))
    except:
        bstack11ll11l1ll_opy_ = 0
    bstack1ll11llll_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11ll11l1ll_opy_)
    logger.debug(bstack1l11lll1l_opy_.format(str(bstack1ll11llll_opy_)))
    bstack1ll11l111_opy_ = CONFIG.get(bstack11l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ╴"))[bstack11ll11l1ll_opy_]
    if bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ╵") in CONFIG and CONFIG[bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ╶")]:
        bstack11lll1l1_opy_(bstack1ll11llll_opy_, bstack1lllll1l1l_opy_)
    if bstack1l11l1l1l_opy_.bstack1l11l11111_opy_(CONFIG, bstack11ll11l1ll_opy_) and bstack1l11l1l1l_opy_.bstack1lll1lll1_opy_(bstack1ll11llll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1lll1111l1l_opy_(bstack1ll111l1lll_opy_):
            bstack1l11l1l1l_opy_.set_capabilities(bstack1ll11llll_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1lll1ll1_opy_ = bstack1lll1llll_opy_(desired_capabilities)
        bstack1l1lll1ll1_opy_[bstack11l1ll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ╷")] = bstack1ll111ll1l_opy_(CONFIG)
        bstack111ll11l_opy_ = bstack1lll111l1_opy_(bstack1l1lll1ll1_opy_)
        if bstack111ll11l_opy_:
            bstack1ll11llll_opy_ = update(bstack111ll11l_opy_, bstack1ll11llll_opy_)
        desired_capabilities = None
    if options:
        bstack11lll111ll_opy_(options, bstack1ll11llll_opy_)
    if not options:
        options = bstack11lll1l11_opy_(bstack1ll11llll_opy_)
    if proxy and bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ╸")):
        options.proxy(proxy)
    if options and bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ╹")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1lll1l_opy_() < version.parse(bstack11l1ll1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ╺")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll11llll_opy_)
    logger.info(bstack111l1l1111_opy_)
    bstack11ll1ll111_opy_.end(EVENTS.bstack11llll1l1_opy_.value, EVENTS.bstack11llll1l1_opy_.value + bstack11l1ll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ╻"),
                               EVENTS.bstack11llll1l1_opy_.value + bstack11l1ll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ╼"), True, None)
    try:
        if bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ╽")):
            bstack1lll1111_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ╾")):
            bstack1lll1111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ╿")):
            bstack1lll1111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1lll1111_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack11l1l11ll1_opy_:
        logger.error(bstack1ll1l1l11l_opy_.format(bstack11l1ll1_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩ▀"), str(bstack11l1l11ll1_opy_)))
        raise bstack11l1l11ll1_opy_
    try:
        bstack11lllllll1_opy_ = bstack11l1ll1_opy_ (u"ࠫࠬ▁")
        if bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭▂")):
            bstack11lllllll1_opy_ = self.caps.get(bstack11l1ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ▃"))
        else:
            bstack11lllllll1_opy_ = self.capabilities.get(bstack11l1ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ▄"))
        if bstack11lllllll1_opy_:
            bstack1llll1111_opy_(bstack11lllllll1_opy_)
            if bstack1l1lll1l_opy_() <= version.parse(bstack11l1ll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ▅")):
                self.command_executor._url = bstack11l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ▆") + bstack11ll1l1l1_opy_ + bstack11l1ll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ▇")
            else:
                self.command_executor._url = bstack11l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ█") + bstack11lllllll1_opy_ + bstack11l1ll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ▉")
            logger.debug(bstack1111l1l1_opy_.format(bstack11lllllll1_opy_))
        else:
            logger.debug(bstack1l1l1lll_opy_.format(bstack11l1ll1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ▊")))
    except Exception as e:
        logger.debug(bstack1l1l1lll_opy_.format(e))
    bstack1111lll11_opy_ = self.session_id
    if bstack11l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ▋") in bstack11l1lllll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l1ll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ▌"), None)
        if item:
            bstack1lll111l1111_opy_ = getattr(item, bstack11l1ll1_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ▍"), False)
            if not getattr(item, bstack11l1ll1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ▎"), None) and bstack1lll111l1111_opy_:
                setattr(store[bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ▏")], bstack11l1ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭▐"), self)
        bstack1ll11l1l1_opy_ = getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ░"), None)
        if bstack1ll11l1l1_opy_ and bstack1ll11l1l1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ▒"), bstack11l1ll1_opy_ (u"ࠨࠩ▓")) == bstack11l1ll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ▔"):
            bstack1l11111l1l_opy_.bstack1l11l1l11l_opy_(self)
    bstack11l1llll1_opy_.append(self)
    if bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭▕") in CONFIG and bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ▖") in CONFIG[bstack11l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ▗")][bstack11ll11l1ll_opy_]:
        bstack1l1ll111l1_opy_ = CONFIG[bstack11l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ▘")][bstack11ll11l1ll_opy_][bstack11l1ll1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ▙")]
    logger.debug(bstack1l1ll11l1l_opy_.format(bstack1111lll11_opy_))
@measure(event_name=EVENTS.bstack1lllll111l_opy_, stage=STAGE.bstack11lll1l1l1_opy_, bstack1ll1l111l_opy_=bstack1l1ll111l1_opy_)
def bstack11l111lll1_opy_(self, url):
    global bstack11l1111l_opy_
    global CONFIG
    try:
        bstack11llll11ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1ll11l1_opy_.format(str(err)))
    try:
        bstack11l1111l_opy_(self, url)
    except Exception as e:
        try:
            bstack11ll1lll_opy_ = str(e)
            if any(err_msg in bstack11ll1lll_opy_ for err_msg in bstack111l11ll11_opy_):
                bstack11llll11ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1ll11l1_opy_.format(str(err)))
        raise e
def bstack11l11l111l_opy_(item, when):
    global bstack1lllll11ll_opy_
    try:
        bstack1lllll11ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1l111ll111_opy_(item, call, rep):
    global bstack11l11lll1_opy_
    global bstack11l1llll1_opy_
    name = bstack11l1ll1_opy_ (u"ࠨࠩ▚")
    try:
        if rep.when == bstack11l1ll1_opy_ (u"ࠩࡦࡥࡱࡲࠧ▛"):
            bstack1111lll11_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11l1ll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ▜"))
            try:
                if (str(skipSessionName).lower() != bstack11l1ll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ▝")):
                    name = str(rep.nodeid)
                    bstack1lll11ll11_opy_ = bstack1111l11l_opy_(bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭▞"), name, bstack11l1ll1_opy_ (u"࠭ࠧ▟"), bstack11l1ll1_opy_ (u"ࠧࠨ■"), bstack11l1ll1_opy_ (u"ࠨࠩ□"), bstack11l1ll1_opy_ (u"ࠩࠪ▢"))
                    os.environ[bstack11l1ll1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭▣")] = name
                    for driver in bstack11l1llll1_opy_:
                        if bstack1111lll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11ll11_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ▤").format(str(e)))
            try:
                bstack1l111ll1l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭▥"):
                    status = bstack11l1ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭▦") if rep.outcome.lower() == bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ▧") else bstack11l1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ▨")
                    reason = bstack11l1ll1_opy_ (u"ࠩࠪ▩")
                    if status == bstack11l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ▪"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ▫") if status == bstack11l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ▬") else bstack11l1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ▭")
                    data = name + bstack11l1ll1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ▮") if status == bstack11l1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ▯") else name + bstack11l1ll1_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ▰") + reason
                    bstack1l11ll1l_opy_ = bstack1111l11l_opy_(bstack11l1ll1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ▱"), bstack11l1ll1_opy_ (u"ࠫࠬ▲"), bstack11l1ll1_opy_ (u"ࠬ࠭△"), bstack11l1ll1_opy_ (u"࠭ࠧ▴"), level, data)
                    for driver in bstack11l1llll1_opy_:
                        if bstack1111lll11_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11ll1l_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ▵").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ▶").format(str(e)))
    bstack11l11lll1_opy_(item, call, rep)
notset = Notset()
def bstack11111l111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l111111l1_opy_
    if str(name).lower() == bstack11l1ll1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ▷"):
        return bstack11l1ll1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ▸")
    else:
        return bstack1l111111l1_opy_(self, name, default, skip)
def bstack1ll1lll111_opy_(self):
    global CONFIG
    global bstack1ll1l1llll_opy_
    try:
        proxy = bstack11l11lll1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1ll1_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ▹")):
                proxies = bstack11l11l1l1_opy_(proxy, bstack1l1l111ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1111ll1ll_opy_ = proxies.popitem()
                    if bstack11l1ll1_opy_ (u"ࠧࡀ࠯࠰ࠤ►") in bstack1111ll1ll_opy_:
                        return bstack1111ll1ll_opy_
                    else:
                        return bstack11l1ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ▻") + bstack1111ll1ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ▼").format(str(e)))
    return bstack1ll1l1llll_opy_(self)
def bstack111111ll1_opy_():
    return (bstack11l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ▽") in CONFIG or bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭▾") in CONFIG) and bstack1llllllll_opy_() and bstack1l1lll1l_opy_() >= version.parse(
        bstack1l1l1ll1ll_opy_)
def bstack111l1ll1_opy_(self,
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
    global bstack1l1ll111l1_opy_
    global bstack1l11lll11_opy_
    global bstack11l1lllll_opy_
    CONFIG[bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ▿")] = str(bstack11l1lllll_opy_) + str(__version__)
    bstack11ll11l1ll_opy_ = 0
    try:
        if bstack1l11lll11_opy_ is True:
            bstack11ll11l1ll_opy_ = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ◀")))
    except:
        bstack11ll11l1ll_opy_ = 0
    CONFIG[bstack11l1ll1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ◁")] = True
    bstack1ll11llll_opy_ = bstack1lll111l1_opy_(CONFIG, bstack11ll11l1ll_opy_)
    logger.debug(bstack1l11lll1l_opy_.format(str(bstack1ll11llll_opy_)))
    if CONFIG.get(bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ◂")):
        bstack11lll1l1_opy_(bstack1ll11llll_opy_, bstack1lllll1l1l_opy_)
    if bstack11l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ◃") in CONFIG and bstack11l1ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭◄") in CONFIG[bstack11l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ◅")][bstack11ll11l1ll_opy_]:
        bstack1l1ll111l1_opy_ = CONFIG[bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭◆")][bstack11ll11l1ll_opy_][bstack11l1ll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ◇")]
    import urllib
    import json
    if bstack11l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ◈") in CONFIG and str(CONFIG[bstack11l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ◉")]).lower() != bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭◊"):
        bstack11lll1ll_opy_ = bstack1l111lll11_opy_()
        bstack1ll11ll1ll_opy_ = bstack11lll1ll_opy_ + urllib.parse.quote(json.dumps(bstack1ll11llll_opy_))
    else:
        bstack1ll11ll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ○") + urllib.parse.quote(json.dumps(bstack1ll11llll_opy_))
    browser = self.connect(bstack1ll11ll1ll_opy_)
    return browser
def bstack1ll1ll11l_opy_():
    global bstack11l111ll_opy_
    global bstack11l1lllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1l1l1l_opy_
        if not bstack1l1l1111ll1_opy_():
            global bstack1lll1l1l11_opy_
            if not bstack1lll1l1l11_opy_:
                from bstack_utils.helper import bstack11ll111l1l_opy_, bstack11ll111l_opy_
                bstack1lll1l1l11_opy_ = bstack11ll111l1l_opy_()
                bstack11ll111l_opy_(bstack11l1lllll_opy_)
            BrowserType.connect = bstack1ll1l1l1l_opy_
            return
        BrowserType.launch = bstack111l1ll1_opy_
        bstack11l111ll_opy_ = True
    except Exception as e:
        pass
def bstack1ll1lllll111_opy_():
    global CONFIG
    global bstack11l1111lll_opy_
    global bstack11ll1l1l1_opy_
    global bstack1lllll1l1l_opy_
    global bstack1l11lll11_opy_
    global bstack11l11l11_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ◌")))
    bstack11l1111lll_opy_ = eval(os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ◍")))
    bstack11ll1l1l1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ◎"))
    bstack11l1ll11ll_opy_(CONFIG, bstack11l1111lll_opy_)
    bstack11l11l11_opy_ = bstack1l1111l1l_opy_.configure_logger(CONFIG, bstack11l11l11_opy_)
    if cli.bstack1l11lll1_opy_():
        bstack11lll11ll1_opy_.invoke(bstack1l1ll1l1ll_opy_.CONNECT, bstack111lll11l1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ●"), bstack11l1ll1_opy_ (u"࠭࠰ࠨ◐")))
        cli.bstack1ll1llll111_opy_(cli_context.platform_index)
        cli.bstack1ll1ll1llll_opy_(bstack1l1l111ll_opy_(bstack11ll1l1l1_opy_, CONFIG), cli_context.platform_index, bstack11lll1l11_opy_)
        cli.bstack1ll111l1l1l_opy_()
        logger.debug(bstack11l1ll1_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ◑") + str(cli_context.platform_index) + bstack11l1ll1_opy_ (u"ࠣࠤ◒"))
        return # skip all existing operations
    global bstack1lll1111_opy_
    global bstack11ll1l1l1l_opy_
    global bstack11ll11ll_opy_
    global bstack111lll11l_opy_
    global bstack1l1llll1_opy_
    global bstack11ll111l1_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack11l1111l_opy_
    global bstack1ll1l1llll_opy_
    global bstack1l111111l1_opy_
    global bstack1lllll11ll_opy_
    global bstack11l11lll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll1111_opy_ = webdriver.Remote.__init__
        bstack11ll1l1l1l_opy_ = WebDriver.quit
        bstack1l1l1l1ll1_opy_ = WebDriver.close
        bstack11l1111l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ◓") in CONFIG or bstack11l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ◔") in CONFIG) and bstack1llllllll_opy_():
        if bstack1l1lll1l_opy_() < version.parse(bstack1l1l1ll1ll_opy_):
            logger.error(bstack1lllllll11_opy_.format(bstack1l1lll1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack11l1ll1_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ◕")) and callable(getattr(RemoteConnection, bstack11l1ll1_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭◖"))):
                    bstack1ll1l1llll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1ll1l1llll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack11lllll1ll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l111111l1_opy_ = Config.getoption
        from _pytest import runner
        bstack1lllll11ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack11l1ll1_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨ◗"), bstack1ll1l111ll_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack11l11lll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ◘"))
    bstack1lllll1l1l_opy_ = CONFIG.get(bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ◙"), {}).get(bstack11l1ll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ◚"))
    bstack1l11lll11_opy_ = True
    bstack1l1ll1l1_opy_(bstack111l1ll1l_opy_)
if (bstack111ll1l1l1l_opy_()):
    bstack1ll1lllll111_opy_()
@error_handler(class_method=False)
def bstack1lll1111l111_opy_(hook_name, event, bstack11llll11l11_opy_=None):
    if hook_name not in [bstack11l1ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ◛"), bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ◜"), bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ◝"), bstack11l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ◞"), bstack11l1ll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ◟"), bstack11l1ll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ◠"), bstack11l1ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ◡"), bstack11l1ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ◢")]:
        return
    node = store[bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ◣")]
    if hook_name in [bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ◤"), bstack11l1ll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ◥")]:
        node = store[bstack11l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭◦")]
    elif hook_name in [bstack11l1ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭◧"), bstack11l1ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ◨")]:
        node = store[bstack11l1ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ◩")]
    hook_type = bstack1llll111l1l1_opy_(hook_name)
    if event == bstack11l1ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ◪"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_[hook_type], bstack1ll1111llll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111111l1ll_opy_ = {
            bstack11l1ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪ◫"): uuid,
            bstack11l1ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ◬"): bstack1ll1llll11_opy_(),
            bstack11l1ll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ◭"): bstack11l1ll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭◮"),
            bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ◯"): hook_type,
            bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭◰"): hook_name
        }
        store[bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ◱")].append(uuid)
        bstack1ll1lllll11l_opy_ = node.nodeid
        if hook_type == bstack11l1ll1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ◲"):
            if not _11111l111l_opy_.get(bstack1ll1lllll11l_opy_, None):
                _11111l111l_opy_[bstack1ll1lllll11l_opy_] = {bstack11l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ◳"): []}
            _11111l111l_opy_[bstack1ll1lllll11l_opy_][bstack11l1ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭◴")].append(bstack111111l1ll_opy_[bstack11l1ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭◵")])
        _11111l111l_opy_[bstack1ll1lllll11l_opy_ + bstack11l1ll1_opy_ (u"ࠩ࠰ࠫ◶") + hook_name] = bstack111111l1ll_opy_
        bstack1lll11111l1l_opy_(node, bstack111111l1ll_opy_, bstack11l1ll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ◷"))
    elif event == bstack11l1ll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ◸"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1ll11l1l1l1_opy_[hook_type], bstack1ll1111llll_opy_.POST, node, None, bstack11llll11l11_opy_)
            return
        bstack1111ll1l1l_opy_ = node.nodeid + bstack11l1ll1_opy_ (u"ࠬ࠳ࠧ◹") + hook_name
        _11111l111l_opy_[bstack1111ll1l1l_opy_][bstack11l1ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ◺")] = bstack1ll1llll11_opy_()
        bstack1lll1111lll1_opy_(_11111l111l_opy_[bstack1111ll1l1l_opy_][bstack11l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ◻")])
        bstack1lll11111l1l_opy_(node, _11111l111l_opy_[bstack1111ll1l1l_opy_], bstack11l1ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ◼"), bstack1ll1llllll1l_opy_=bstack11llll11l11_opy_)
def bstack1lll1111111l_opy_():
    global bstack1ll1lllllll1_opy_
    if bstack1l1l1l1l1l_opy_():
        bstack1ll1lllllll1_opy_ = bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭◽")
    else:
        bstack1ll1lllllll1_opy_ = bstack11l1ll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ◾")
@bstack1l11111l1l_opy_.bstack1lll11l1lll1_opy_
def bstack1lll11111lll_opy_():
    bstack1lll1111111l_opy_()
    if cli.is_running():
        try:
            bstack1111ll1l11l_opy_(bstack1lll1111l111_opy_)
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ◿").format(e))
        return
    if bstack1llllllll_opy_():
        bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
        bstack11l1ll1_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ☀")
        if bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ☁")):
            if CONFIG.get(bstack11l1ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ☂")) is not None and int(CONFIG[bstack11l1ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ☃")]) > 1:
                bstack1ll111l111_opy_(bstack1l1ll11l_opy_)
            return
        bstack1ll111l111_opy_(bstack1l1ll11l_opy_)
    try:
        bstack1111ll1l11l_opy_(bstack1lll1111l111_opy_)
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ☄").format(e))
bstack1lll11111lll_opy_()