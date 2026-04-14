# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1llll111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1l11llll_opy_, update, bstack11ll11l1l1_opy_,
                                       bstack1llll1lll1_opy_, bstack1l1ll1lll1_opy_, bstack1l1111l1l_opy_, bstack1l111l1lll_opy_,
                                       bstack1lll1lllll_opy_, bstack111l11111l_opy_, bstack111l111l_opy_,
                                       bstack1l111l1111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l111l1l1l_opy_)
from browserstack_sdk.bstack11l1llll1l_opy_ import bstack1ll11l1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1llll11l11l_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1lllll1l_opy_, bstack111lll1l1l_opy_, bstack1l1ll11ll1_opy_, \
    bstack111l1l11l_opy_
from bstack_utils.helper import bstack1l111l11l_opy_, bstack1lllll111ll1_opy_, bstack1lll11ll11l_opy_, bstack111l1111_opy_, bstack11ll1l1l1l_opy_, bstack111111l1l_opy_, \
    bstack1llll1ll1lll_opy_, \
    bstack1llll1l1l1ll_opy_, bstack1ll1l1ll11_opy_, bstack1l1lll111l_opy_, bstack1llll111llll_opy_, bstack11l1l1ll1_opy_, Notset, \
    bstack1ll111lll1_opy_, bstack1ll1ll1l11l_opy_, bstack1lllll11ll11_opy_, Result, bstack1lllll1111ll_opy_, bstack1llll11lll1l_opy_, error_handler, \
    bstack11l11l1111_opy_, bstack11l1lll1l_opy_, bstack111111lll1_opy_, bstack1llll11ll1ll_opy_
from bstack_utils.bstack1lll1ll1llll_opy_ import bstack1lll1ll1ll1l_opy_
from bstack_utils.messages import bstack11lllll11l_opy_, bstack111lll111l_opy_, bstack1lll1lll_opy_, bstack1l1ll11l1_opy_, bstack1l11l111_opy_, \
    bstack1l1ll111_opy_, bstack1l1l1ll11l_opy_, CONFIG_FILE_CONTENT, bstack1ll11ll11l_opy_, bstack1ll11111ll_opy_, \
    bstack11lll1l1l_opy_, bstack11lll11l1_opy_, bstack1llll1ll11_opy_
from bstack_utils.proxy import bstack1l1llll111_opy_, bstack1111111ll_opy_
from bstack_utils.bstack1111ll11_opy_ import bstack1ll1l11ll111_opy_, bstack1ll1l111llll_opy_, bstack1ll1l11l11ll_opy_, bstack1ll1l11ll1l1_opy_, \
    bstack1ll1l11l11l1_opy_, bstack1ll1l11l1111_opy_, bstack1ll1l111lll1_opy_, bstack11111l1l1_opy_, bstack1ll1l11ll11l_opy_
from bstack_utils.bstack11l1llllll_opy_ import bstack1llll111l1_opy_
from bstack_utils.bstack11ll11l1ll_opy_ import bstack1ll11l11ll_opy_, bstack1ll1l1lll1_opy_, update_caps_for_local, \
    bstack1llll111l_opy_, bstack11lll111l1_opy_
from bstack_utils.bstack1llll1l11ll_opy_ import bstack1llll1111l1_opy_
from bstack_utils.bstack1lll111111_opy_ import bstack1l1ll1l1ll_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1111l11l_opy_ import bstack1l1l111111_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack1l1l11l1l1_opy_ import bstack1l11111l1_opy_
from browserstack_sdk.sdk_cli.bstack111l11lll1_opy_ import bstack111l11lll1_opy_, Events, bstack1l1l1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1l1ll111_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111l11lll1_opy_ import bstack111l11lll1_opy_, Events, bstack1l1l1l1l_opy_
bstack1lll1ll1ll_opy_ = None
bstack1lll11l11_opy_ = None
bstack11111ll1_opy_ = None
bstack1l1l1l1l1l_opy_ = None
bstack1ll1l1lll_opy_ = None
bstack1l1111111_opy_ = None
bstack1ll1l11l11_opy_ = None
bstack111ll1l11_opy_ = None
bstack11ll11l11l_opy_ = None
bstack1l1ll11l11_opy_ = None
bstack1111111l_opy_ = None
bstack1l1l11l11l_opy_ = None
bstack11l11l11_opy_ = None
FRAMEWORK_NAME = bstack1l111l_opy_ (u"ࠬ࠭⤂")
CONFIG = {}
bstack1111l111_opy_ = False
bstack1111l1l1l_opy_ = bstack1l111l_opy_ (u"࠭ࠧ⤃")
bstack111lll1lll_opy_ = bstack1l111l_opy_ (u"ࠧࠨ⤄")
PARALLELISE_VANILLA_PYTHON = False
bstack1l1lll1l1_opy_ = []
bstack11111l1ll1_opy_ = bstack1l1lllll1l_opy_
bstack1ll111l11l11_opy_ = bstack1l111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⤅")
bstack1lllllllll1_opy_ = {}
SESSION_NAME = None
bstack11l1ll11l_opy_ = False
logger = logger_utils.get_logger(__name__, bstack11111l1ll1_opy_)
store = {
    bstack1l111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⤆"): []
}
bstack1ll1111lll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lll1ll11l1_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1l1ll111_opy_(
    test_framework_name=bstack1111111l1_opy_[bstack1l111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ⤇")] if bstack11l1l1ll1_opy_() else bstack1111111l1_opy_[bstack1l111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫ⤈")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack111l1l11l1_opy_):
    try:
        page.evaluate(bstack1l111l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⤉"),
                      bstack1l111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ⤊") + json.dumps(
                          bstack111l1l11l1_opy_) + bstack1l111l_opy_ (u"ࠢࡾࡿࠥ⤋"))
    except Exception as e:
        print(bstack1l111l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ⤌"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1l111l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ⤍"), bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ⤎") + json.dumps(
            message) + bstack1l111l_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ⤏") + json.dumps(level) + bstack1l111l_opy_ (u"ࠬࢃࡽࠨ⤐"))
    except Exception as e:
        print(bstack1l111l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ⤑"), e)
def _1ll11111l111_opy_():
    bstack1l111l_opy_ (u"ࠢࠣࠤ࡚ࡥࡱࡱࠠࡄ࡙ࡇࠤࡺࡶࡷࡢࡴࡧࠤࡱࡵ࡯࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡵࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰ࠳ࠨࠢࠣ⤒")
    bstack1ll111l111l1_opy_ = os.getcwd()
    while True:
        for name in (bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ⤓"), bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡤࡱࡱ࠭⤔")):
            candidate = os.path.join(bstack1ll111l111l1_opy_, name)
            if os.path.exists(candidate):
                return candidate
        parent = os.path.dirname(bstack1ll111l111l1_opy_)
        if parent == bstack1ll111l111l1_opy_:
            break
        bstack1ll111l111l1_opy_ = parent
    return None
def _1ll11111l1l1_opy_():
    bstack1l111l_opy_ (u"ࠥࠦࠧࡊࡥࡵࡧࡦࡸࠥ࡯ࡦࠡࡲࡼࡸࡪࡹࡴࠡࡹࡤࡷࠥࡲࡡࡶࡰࡦ࡬ࡪࡪࠠࡣࡻࠣࡥࡳࠦࡉࡅࡇࠣࡶࡺࡴ࡮ࡦࡴ࠱ࠎࠥࠦࠠࠡࡗࡶࡩࡸࠦࡳࡵࡣࡥࡰࡪ࠲ࠠ࡭ࡱࡱ࡫࠲ࡲࡩࡷࡧࡧࠤࡪࡴࡶࠡࡸࡤࡶࡸࠦࡳࡦࡶࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡨࡧ࡬࡭ࡻࠣࡦࡾࠦࡉࡅࡇࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࡕ࡟ࡃࡉࡃࡕࡑࡤࡎࡏࡔࡖࡈࡈࠥࠦࠠࠡ⠖ࠣࡎࡪࡺࡂࡳࡣ࡬ࡲࡸࠦࡐࡺࡅ࡫ࡥࡷࡳࠠࠩࢀ࠵࠴࠶࠹ࠫࠪࠌࠣࠤࠥࠦࠠࠡࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠤࠥ⠚ࠠࡋࡧࡷࡆࡷࡧࡩ࡯ࡵࠣࡍࡉࡋࡳࠡࡸ࡬ࡥ࡚ࠥࡥࡢ࡯ࡆ࡭ࡹࡿࠠࡱࡴࡲࡸࡴࡩ࡯࡭ࠢࠫ࠵࠵࠱ࠠࡺࡧࡤࡶࡸ࠯ࠊࠡࠢࠣࠤࠧࠨࠢ⤕")
    return os.environ.get(bstack1l111l_opy_ (u"ࠫࡕ࡟ࡃࡉࡃࡕࡑࡤࡎࡏࡔࡖࡈࡈࠬ⤖")) == bstack1l111l_opy_ (u"ࠬ࠷ࠧ⤗") or \
           bool(os.environ.get(bstack1l111l_opy_ (u"࠭ࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠩ⤘")))
def pytest_configure(config):
    global bstack1111l1l1l_opy_
    global CONFIG
    global bstack1111l111_opy_
    if not os.environ.get(bstack1l111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠫ⤙")) and _1ll11111l1l1_opy_():
        _1ll1111l11ll_opy_ = _1ll11111l111_opy_()
        if _1ll1111l11ll_opy_:
            try:
                from browserstack_sdk import bstack1l1l1ll11_opy_
                if bstack1l1l1ll11_opy_(_1ll1111l11ll_opy_):
                    CONFIG = json.loads(os.environ.get(bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ⤚"), bstack1l111l_opy_ (u"ࠩࡾࢁࠬ⤛")))
                    bstack1111l1l1l_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ⤜"), bstack1l111l_opy_ (u"ࠫࠬ⤝"))
                    bstack1111l111_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭⤞"), bstack1l111l_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬ⤟")).lower() == bstack1l111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ⤠")
            except Exception as e:
                logger.error(bstack1l111l_opy_ (u"ࠣࡒ࡯ࡹ࡬࡯࡮ࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ⤡").format(e))
    global_config = Config.bstack1ll11ll111_opy_()
    config.args = bstack1l1ll1l1ll_opy_.bstack1ll111l11lll_opy_(config.args)
    global_config.bstack1l1l111ll1_opy_(bstack111111lll1_opy_(config.getoption(bstack1l111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭⤢"))))
    try:
        logger_utils.bstack1lll1l1ll11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111l11lll1_opy_.invoke(Events.CONNECT, bstack1l1l1l1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⤣"), bstack1l111l_opy_ (u"ࠫ࠵࠭⤤")))
        config = json.loads(os.environ.get(bstack1l111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦ⤥"), bstack1l111l_opy_ (u"ࠨࡻࡾࠤ⤦")))
        cli.bstack1l11llll111_opy_(bstack1l1lll111l_opy_(bstack1111l1l1l_opy_, CONFIG), cli_context.platform_index, bstack11ll11l1l1_opy_)
    if cli.bstack1llll1ll1l_opy_(bstack1l11111l1_opy_):
        cli.bstack1ll1ll11ll_opy_()
        logger.debug(bstack1l111l_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⤧") + str(cli_context.platform_index) + bstack1l111l_opy_ (u"ࠣࠤ⤨"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
def pytest_unconfigure(config):
    bstack1l111l_opy_ (u"ࠤࠥࠦࡗࡻ࡮ࠡࡕࡇࡏࠥࡩ࡬ࡦࡣࡱࡹࡵࠦࡷࡩ࡫࡯ࡩࠥࡶࡹࡵࡧࡶࡸࠥ࠮ࡡ࡯ࡦࠣࡰࡴ࡭ࡧࡪࡰࡪ࠭ࠥ࡯ࡳࠡࡵࡷ࡭ࡱࡲࠠࡢ࡮࡬ࡺࡪ࠴ࠊࠡࠢࠣࠤࡎࡴࠠࡱ࡮ࡸ࡫࡮ࡴࠠ࡮ࡱࡧࡩ࠱ࠦࡢࡴࡶࡤࡧࡰࡥࡥࡹ࡫ࡷࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡬ࡩࡳࡧࡶࠤࡦࡺࠠࡢࡶࡨࡼ࡮ࡺࠠࡣࡷࡷࠤࡧࡿࠠࡵࡪࡨࡲࠏࠦࠠࠡࠢࡳࡽࡹ࡫ࡳࡵࠢ࡫ࡥࡸࠦࡴࡰࡴࡱࠤࡩࡵࡷ࡯ࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠳ࠦࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡪࡶࠣ࡬ࡪࡸࡥࠡࡧࡱࡷࡺࡸࡥࡴࠌࠣࠤࠥࠦࡴࡩࡧࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱࠠࡢࡰࡧࠤࡘࡊࡋࠡࡴࡸࡲࠥ࡫࡮ࡥࡧࡧࠤࡲ࡫ࡳࡴࡣࡪࡩࡸࠦࡲࡦࡣࡦ࡬ࠥࡺࡨࡦࠢࡦࡳࡳࡹ࡯࡭ࡧ࠱ࠦࠧࠨ⤩")
    if os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡈࡊࡥࡐࡍࡗࡊࡍࡓࡥࡍࡐࡆࡈࠫ⤪")) and cli.is_running():
        from browserstack_sdk import bstack11ll111lll_opy_
        bstack11ll111lll_opy_()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤ⤫"), None)
    if cli.is_running() and when == bstack1l111l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ⤬"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1l111l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⤭"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l111l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⤮")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠢ⤯"), bstack1l111l_opy_ (u"ࠤࡾࢁࠧ⤰")))
            if bstack1l1l111111_opy_.bstack11l111l11_opy_(config):
                bstack1ll1ll1lll11_opy_ = bstack1l1l111111_opy_.bstack1l1l111l_opy_(config)
                if item.execution_count > bstack1ll1ll1lll11_opy_:
                    print(bstack1l111l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡳࡧࡷࡶ࡮࡫ࡳ࠻ࠢࠪ⤱"), report.nodeid, os.environ.get(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⤲")))
                    bstack1l1l111111_opy_.bstack1lll1111l1ll_opy_(report.nodeid)
            else:
                print(bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࠬ⤳"), report.nodeid, os.environ.get(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⤴")))
                bstack1l1l111111_opy_.bstack1lll1111l1ll_opy_(report.nodeid)
        else:
            print(bstack1l111l_opy_ (u"ࠧࡕࡧࡶࡸࠥࡶࡡࡴࡵࡨࡨ࠿ࠦࠧ⤵"), report.nodeid, os.environ.get(bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⤶")))
    if cli.is_running():
        if when == bstack1l111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ⤷"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack1l111l_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⤸"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1l111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⤹"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⤺"))
    plugins = item.config.getoption(bstack1l111l_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢ⤻"))
    report = outcome.get_result()
    os.environ[bstack1l111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⤼")] = report.nodeid
    bstack1ll11111llll_opy_(item, call, report)
    if bstack1l111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨ⤽") not in plugins or bstack11l1l1ll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l111l_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥ⤾"), None)
    page = getattr(item, bstack1l111l_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤ⤿"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1111llll1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll1111l1l1l_opy_(item, report, summary, skipSessionName)
def bstack1ll1111llll1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⥀") and report.skipped:
        bstack1ll1l11ll11l_opy_(report)
    if report.when in [bstack1l111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⥁"), bstack1l111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ⥂")]:
        return
    if not bstack11ll1l1l1l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ⥃")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⥄") + json.dumps(
                    report.nodeid) + bstack1l111l_opy_ (u"ࠩࢀࢁࠬ⥅"))
        os.environ[bstack1l111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⥆")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦ⥇").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l111l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⥈")))
    bstack1111l111l1_opy_ = bstack1l111l_opy_ (u"ࠨࠢ⥉")
    bstack1ll1l11ll11l_opy_(report)
    if not passed:
        try:
            bstack1111l111l1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l111l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ⥊").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1111l111l1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l111l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⥋")))
        bstack1111l111l1_opy_ = bstack1l111l_opy_ (u"ࠤࠥ⥌")
        if not passed:
            try:
                bstack1111l111l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⥍").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1111l111l1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⥎")
                    + json.dumps(bstack1l111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨ⥏"))
                    + bstack1l111l_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ⥐")
                )
            else:
                item._driver.execute_script(
                    bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬ⥑")
                    + json.dumps(str(bstack1111l111l1_opy_))
                    + bstack1l111l_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦ⥒")
                )
        except Exception as e:
            summary.append(bstack1l111l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢ⥓").format(e))
def bstack1ll111111l1l_opy_(test_name, error_message):
    try:
        bstack1ll1111l1l11_opy_ = []
        bstack11111l1l1l_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⥔"), bstack1l111l_opy_ (u"ࠫ࠵࠭⥕"))
        bstack11l1l11l1_opy_ = {bstack1l111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⥖"): test_name, bstack1l111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⥗"): error_message, bstack1l111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭⥘"): bstack11111l1l1l_opy_}
        bstack1ll111111ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⥙"))
        if os.path.exists(bstack1ll111111ll1_opy_):
            with open(bstack1ll111111ll1_opy_) as f:
                bstack1ll1111l1l11_opy_ = json.load(f)
        bstack1ll1111l1l11_opy_.append(bstack11l1l11l1_opy_)
        with open(bstack1ll111111ll1_opy_, bstack1l111l_opy_ (u"ࠩࡺࠫ⥚")) as f:
            json.dump(bstack1ll1111l1l11_opy_, f)
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨ⥛") + str(e))
def bstack1ll1111l1l1l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⥜"), bstack1l111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⥝")]:
        return
    if (str(skipSessionName).lower() != bstack1l111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ⥞")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l111l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⥟")))
    bstack1111l111l1_opy_ = bstack1l111l_opy_ (u"ࠣࠤ⥠")
    bstack1ll1l11ll11l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1111l111l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l111l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⥡").format(e)
                )
        try:
            if passed:
                bstack11lll111l1_opy_(getattr(item, bstack1l111l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⥢"), None), bstack1l111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ⥣"))
            else:
                error_message = bstack1l111l_opy_ (u"ࠬ࠭⥤")
                if bstack1111l111l1_opy_:
                    playwright_annotate(item._page, str(bstack1111l111l1_opy_), bstack1l111l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ⥥"))
                    bstack11lll111l1_opy_(getattr(item, bstack1l111l_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭⥦"), None), bstack1l111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ⥧"), str(bstack1111l111l1_opy_))
                    error_message = str(bstack1111l111l1_opy_)
                else:
                    bstack11lll111l1_opy_(getattr(item, bstack1l111l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⥨"), None), bstack1l111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ⥩"))
                bstack1ll111111l1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣ⥪").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l111l_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ⥫"), default=bstack1l111l_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ⥬"), help=bstack1l111l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨ⥭"))
    parser.addoption(bstack1l111l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ⥮"), default=bstack1l111l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⥯"), help=bstack1l111l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⥰"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l111l_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨ⥱"), action=bstack1l111l_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦ⥲"), default=bstack1l111l_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨ⥳"),
                         help=bstack1l111l_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨ⥴"))
def bstack1llll11ll11_opy_(log):
    if not (log[bstack1l111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⥵")] and log[bstack1l111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⥶")].strip()):
        return
    active = bstack1llll111lll_opy_()
    log = {
        bstack1l111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⥷"): log[bstack1l111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⥸")],
        bstack1l111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⥹"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"࡚࠭ࠨ⥺"),
        bstack1l111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⥻"): log[bstack1l111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⥼")],
    }
    if active:
        if active[bstack1l111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⥽")] == bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⥾"):
            log[bstack1l111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⥿")] = active[bstack1l111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⦀")]
        elif active[bstack1l111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⦁")] == bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࠬ⦂"):
            log[bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⦃")] = active[bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⦄")]
    TestHubHandler.bstack1ll111l11_opy_([log])
def bstack1llll111lll_opy_():
    if len(store[bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⦅")]) > 0 and store[bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⦆")][-1]:
        return {
            bstack1l111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⦇"): bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⦈"),
            bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⦉"): store[bstack1l111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⦊")][-1]
        }
    if store.get(bstack1l111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⦋"), None):
        return {
            bstack1l111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ⦌"): bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⦍"),
            bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⦎"): store[bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⦏")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.INIT_TEST, TestHookState.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, item)
        return
    try:
        global CONFIG
        item._1ll1111lll1l_opy_ = True
        bstack1l1ll11111_opy_ = a11y.is_enabled_testcase(bstack1llll1l1l1ll_opy_(item.own_markers))
        if not cli.bstack1llll1ll1l_opy_(bstack1l11111l1_opy_):
            item._a11y_test_case = bstack1l1ll11111_opy_
            if bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⦐"), None):
                driver = getattr(item, bstack1l111l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⦑"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack1l1ll11111_opy_)
        if not TestHubHandler.on() or bstack1ll111l11l11_opy_ != bstack1l111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⦒"):
            return
        global current_test_uuid #, bstack1llll111l1l_opy_
        bstack1lll1llll11_opy_ = {
            bstack1l111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⦓"): uuid4().__str__(),
            bstack1l111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⦔"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"ࠬࡠࠧ⦕")
        }
        current_test_uuid = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⦖")]
        store[bstack1l111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⦗")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⦘")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lll1ll11l1_opy_[item.nodeid] = {**_1lll1ll11l1_opy_[item.nodeid], **bstack1lll1llll11_opy_}
        bstack1ll111l111ll_opy_(item, _1lll1ll11l1_opy_[item.nodeid], bstack1l111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⦙"))
    except Exception as err:
        print(bstack1l111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬ⦚"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⦛")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1l111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⦜"))
    if bstack1l1l111111_opy_.bstack1lll11l1l1ll_opy_():
            bstack1ll11111ll11_opy_ = bstack1l111l_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡡࡴࠢࡷ࡬ࡪࠦࡡࡣࡱࡵࡸࠥࡨࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡨࡼ࡮ࡹࡴࡴ࠰ࠥ⦝")
            logger.error(bstack1ll11111ll11_opy_)
            bstack1lll1llll11_opy_ = {
                bstack1l111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⦞"): uuid4().__str__(),
                bstack1l111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⦟"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"ࠩ࡝ࠫ⦠"),
                bstack1l111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⦡"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"ࠫ࡟࠭⦢"),
                bstack1l111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⦣"): bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⦤"),
                bstack1l111l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ⦥"): bstack1ll11111ll11_opy_,
                bstack1l111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⦦"): [],
                bstack1l111l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⦧"): []
            }
            bstack1ll111l111ll_opy_(item, bstack1lll1llll11_opy_, bstack1l111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⦨"))
            pytest.skip(bstack1ll11111ll11_opy_)
            return # skip all existing operations
    global bstack1ll1111lll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1llll111llll_opy_():
        atexit.register(bstack11ll111lll_opy_)
        if not bstack1ll1111lll11_opy_:
            try:
                bstack1ll111l11111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1llll11ll1ll_opy_():
                    bstack1ll111l11111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll111l11111_opy_:
                    signal.signal(s, bstack1ll1l11l111_opy_)
                bstack1ll1111lll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧ⦩") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1l11ll111_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⦪")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lll1llll11_opy_ = {
            bstack1l111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⦫"): uuid,
            bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⦬"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"ࠨ࡜ࠪ⦭"),
            bstack1l111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⦮"): bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⦯"),
            bstack1l111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⦰"): bstack1l111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⦱"),
            bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⦲"): bstack1l111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⦳")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⦴")] = item
        store[bstack1l111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⦵")] = [uuid]
        if not _1lll1ll11l1_opy_.get(item.nodeid, None):
            _1lll1ll11l1_opy_[item.nodeid] = {bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⦶"): [], bstack1l111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⦷"): []}
        _1lll1ll11l1_opy_[item.nodeid][bstack1l111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⦸")].append(bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⦹")])
        _1lll1ll11l1_opy_[item.nodeid + bstack1l111l_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧ⦺")] = bstack1lll1llll11_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1111l1lll_opy_(item, bstack1lll1llll11_opy_, bstack1l111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⦻"))
    except Exception as err:
        print(bstack1l111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ⦼"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1l111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⦽"))
        return # skip all existing operations
    try:
        global bstack1lllllllll1_opy_
        bstack11111l1l1l_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11111l1l1l_opy_ = int(os.environ.get(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⦾")))
        if bstack1llll1l11_opy_.bstack1111l11l11_opy_() == bstack1l111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ⦿"):
            if bstack1llll1l11_opy_.bstack1l1l1llll_opy_() == bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ⧀"):
                bstack1ll111l1111l_opy_ = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⧁"), None)
                bstack111l1l1ll1_opy_ = bstack1ll111l1111l_opy_ + bstack1l111l_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ⧂")
                driver = getattr(item, bstack1l111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⧃"), None)
                bstack1l1111l111_opy_ = getattr(item, bstack1l111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ⧄"), None)
                bstack1ll1ll11l_opy_ = getattr(item, bstack1l111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⧅"), None)
                PercySDK.screenshot(driver, bstack111l1l1ll1_opy_, bstack1l1111l111_opy_=bstack1l1111l111_opy_, bstack1ll1ll11l_opy_=bstack1ll1ll11l_opy_, bstack1ll1llll11_opy_=bstack11111l1l1l_opy_)
        if not cli.bstack1llll1ll1l_opy_(bstack1l11111l1_opy_):
            if getattr(item, bstack1l111l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬ⧆"), False):
                bstack1ll11l1lll_opy_.bstack11ll111111_opy_(getattr(item, bstack1l111l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⧇"), None), bstack1lllllllll1_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lll1llll11_opy_ = {
            bstack1l111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⧈"): uuid4().__str__(),
            bstack1l111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⧉"): bstack1lll11ll11l_opy_().isoformat() + bstack1l111l_opy_ (u"ࠩ࡝ࠫ⧊"),
            bstack1l111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ⧋"): bstack1l111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⧌"),
            bstack1l111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⧍"): bstack1l111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⧎"),
            bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ⧏"): bstack1l111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⧐")
        }
        _1lll1ll11l1_opy_[item.nodeid + bstack1l111l_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬ⧑")] = bstack1lll1llll11_opy_
        bstack1ll1111l1lll_opy_(item, bstack1lll1llll11_opy_, bstack1l111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⧒"))
    except Exception as err:
        print(bstack1l111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪ⧓"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1ll1l11ll1l1_opy_(fixturedef.argname):
        store[bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫ⧔")] = request.node
    elif bstack1ll1l11l11l1_opy_(fixturedef.argname):
        store[bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ⧕")] = request.node
    if not TestHubHandler.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.SETUP_FIXTURE, TestHookState.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1l111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⧖"): fixturedef.argname,
            bstack1l111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⧗"): bstack1llll1ll1lll_opy_(outcome),
            bstack1l111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⧘"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⧙")]
        if not _1lll1ll11l1_opy_.get(current_test_item.nodeid, None):
            _1lll1ll11l1_opy_[current_test_item.nodeid] = {bstack1l111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⧚"): []}
        _1lll1ll11l1_opy_[current_test_item.nodeid][bstack1l111l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⧛")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ⧜"), str(err))
if bstack11l1l1ll1_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1lll1ll11l1_opy_[request.node.nodeid][bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⧝")].bstack111lll111_opy_(id(step))
        except Exception as err:
            print(bstack1l111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭⧞"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1lll1ll11l1_opy_[request.node.nodeid][bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⧟")].bstack1llll1l1l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ⧠"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            bstack1llll1l11ll_opy_: bstack1llll1111l1_opy_ = _1lll1ll11l1_opy_[request.node.nodeid][bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⧡")]
            bstack1llll1l11ll_opy_.bstack1llll1l1l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩ⧢"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111l11l11_opy_
        try:
            if not TestHubHandler.on() or bstack1ll111l11l11_opy_ != bstack1l111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪ⧣"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭⧤"), None)
            if not _1lll1ll11l1_opy_.get(request.node.nodeid, None):
                _1lll1ll11l1_opy_[request.node.nodeid] = {}
            bstack1llll1l11ll_opy_ = bstack1llll1111l1_opy_.bstack1ll11ll11ll1_opy_(
                scenario, feature, request.node,
                name=bstack1ll1l11l1111_opy_(request.node, scenario),
                started_at=bstack111111l1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⧥"),
                tags=bstack1ll1l111lll1_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llll11l1l1_opy_(driver) if driver and driver.session_id else {}
            )
            _1lll1ll11l1_opy_[request.node.nodeid][bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⧦")] = bstack1llll1l11ll_opy_
            bstack1ll11111lll1_opy_(bstack1llll1l11ll_opy_.uuid)
            TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⧧"), bstack1llll1l11ll_opy_)
        except Exception as err:
            print(bstack1l111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭⧨"), str(err))
def bstack1ll1111l1ll1_opy_(bstack1llll1l11l1_opy_):
    if bstack1llll1l11l1_opy_ in store[bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⧩")]:
        store[bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⧪")].remove(bstack1llll1l11l1_opy_)
def bstack1ll11111lll1_opy_(test_uuid):
    store[bstack1l111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⧫")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll111lll1l1_opy_
def bstack1ll11111llll_opy_(item, call, report):
    logger.debug(bstack1l111l_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡳࡶࠪ⧬"))
    global bstack1ll111l11l11_opy_
    bstack111l1l11ll_opy_ = bstack111111l1l_opy_()
    if hasattr(report, bstack1l111l_opy_ (u"ࠩࡶࡸࡴࡶࠧ⧭")):
        bstack111l1l11ll_opy_ = bstack1lllll1111ll_opy_(report.stop)
    elif hasattr(report, bstack1l111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩ⧮")):
        bstack111l1l11ll_opy_ = bstack1lllll1111ll_opy_(report.start)
    try:
        if getattr(report, bstack1l111l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⧯"), bstack1l111l_opy_ (u"ࠬ࠭⧰")) == bstack1l111l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⧱"):
            logger.debug(bstack1l111l_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡴࡦࠢ࠰ࠤࢀࢃࠬࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡻࡾࠩ⧲").format(getattr(report, bstack1l111l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⧳"), bstack1l111l_opy_ (u"ࠩࠪ⧴")).__str__(), bstack1ll111l11l11_opy_))
            if bstack1ll111l11l11_opy_ == bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⧵"):
                _1lll1ll11l1_opy_[item.nodeid][bstack1l111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⧶")] = bstack111l1l11ll_opy_
                bstack1ll111l111ll_opy_(item, _1lll1ll11l1_opy_[item.nodeid], bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⧷"), report, call)
                store[bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⧸")] = None
            elif bstack1ll111l11l11_opy_ == bstack1l111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ⧹"):
                bstack1llll1l11ll_opy_ = _1lll1ll11l1_opy_[item.nodeid][bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⧺")]
                bstack1llll1l11ll_opy_.set(hooks=_1lll1ll11l1_opy_[item.nodeid].get(bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⧻"), []))
                exception, bstack1llll1l111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llll1l111l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l111l_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩ⧼"), bstack1l111l_opy_ (u"ࠫࠬ⧽"))]
                bstack1llll1l11ll_opy_.stop(time=bstack111l1l11ll_opy_, result=Result(result=getattr(report, bstack1l111l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⧾"), bstack1l111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⧿")), exception=exception, bstack1llll1l111l_opy_=bstack1llll1l111l_opy_))
                TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⨀"), _1lll1ll11l1_opy_[item.nodeid][bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⨁")])
        elif getattr(report, bstack1l111l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⨂"), bstack1l111l_opy_ (u"ࠪࠫ⨃")) in [bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⨄"), bstack1l111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ⨅")]:
            logger.debug(bstack1l111l_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ⨆").format(getattr(report, bstack1l111l_opy_ (u"ࠧࡸࡪࡨࡲࠬ⨇"), bstack1l111l_opy_ (u"ࠨࠩ⨈")).__str__(), bstack1ll111l11l11_opy_))
            bstack1llll11111l_opy_ = item.nodeid + bstack1l111l_opy_ (u"ࠩ࠰ࠫ⨉") + getattr(report, bstack1l111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⨊"), bstack1l111l_opy_ (u"ࠫࠬ⨋"))
            if getattr(report, bstack1l111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⨌"), False):
                hook_type = bstack1l111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⨍") if getattr(report, bstack1l111l_opy_ (u"ࠧࡸࡪࡨࡲࠬ⨎"), bstack1l111l_opy_ (u"ࠨࠩ⨏")) == bstack1l111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⨐") else bstack1l111l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ⨑")
                _1lll1ll11l1_opy_[bstack1llll11111l_opy_] = {
                    bstack1l111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⨒"): uuid4().__str__(),
                    bstack1l111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⨓"): bstack111l1l11ll_opy_,
                    bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⨔"): hook_type
                }
            _1lll1ll11l1_opy_[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⨕")] = bstack111l1l11ll_opy_
            bstack1ll1111l1ll1_opy_(_1lll1ll11l1_opy_[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⨖")])
            bstack1ll1111l1lll_opy_(item, _1lll1ll11l1_opy_[bstack1llll11111l_opy_], bstack1l111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⨗"), report, call)
            if getattr(report, bstack1l111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⨘"), bstack1l111l_opy_ (u"ࠫࠬ⨙")) == bstack1l111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⨚"):
                if getattr(report, bstack1l111l_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⨛"), bstack1l111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⨜")) == bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⨝"):
                    bstack1lll1llll11_opy_ = {
                        bstack1l111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⨞"): uuid4().__str__(),
                        bstack1l111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⨟"): bstack111111l1l_opy_(),
                        bstack1l111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⨠"): bstack111111l1l_opy_()
                    }
                    _1lll1ll11l1_opy_[item.nodeid] = {**_1lll1ll11l1_opy_[item.nodeid], **bstack1lll1llll11_opy_}
                    bstack1ll111l111ll_opy_(item, _1lll1ll11l1_opy_[item.nodeid], bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⨡"))
                    bstack1ll111l111ll_opy_(item, _1lll1ll11l1_opy_[item.nodeid], bstack1l111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⨢"), report, call)
    except Exception as err:
        print(bstack1l111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬ⨣"), str(err))
def bstack1ll1111lllll_opy_(test, bstack1lll1llll11_opy_, result=None, call=None, bstack1111ll11ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1llll1l11ll_opy_ = {
        bstack1l111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⨤"): bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⨥")],
        bstack1l111l_opy_ (u"ࠪࡸࡾࡶࡥࠨ⨦"): bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⨧"),
        bstack1l111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⨨"): test.name,
        bstack1l111l_opy_ (u"࠭ࡢࡰࡦࡼࠫ⨩"): {
            bstack1l111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⨪"): bstack1l111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⨫"),
            bstack1l111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⨬"): inspect.getsource(test.obj)
        },
        bstack1l111l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⨭"): test.name,
        bstack1l111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪ⨮"): test.name,
        bstack1l111l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬ⨯"): bstack1l1ll1l1ll_opy_.bstack1lll1l1l1l1_opy_(test),
        bstack1l111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ⨰"): file_path,
        bstack1l111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩ⨱"): file_path,
        bstack1l111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⨲"): bstack1l111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⨳"),
        bstack1l111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨ⨴"): file_path,
        bstack1l111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⨵"): bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⨶")],
        bstack1l111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⨷"): bstack1l111l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⨸"),
        bstack1l111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ⨹"): {
            bstack1l111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭⨺"): test.nodeid
        },
        bstack1l111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⨻"): bstack1llll1l1l1ll_opy_(test.own_markers)
    }
    if bstack1111ll11ll_opy_ in [bstack1l111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⨼"), bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⨽")]:
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"࠭࡭ࡦࡶࡤࠫ⨾")] = {
            bstack1l111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⨿"): bstack1lll1llll11_opy_.get(bstack1l111l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⩀"), [])
        }
    if bstack1111ll11ll_opy_ == bstack1l111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⩁"):
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⩂")] = bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⩃")
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⩄")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⩅")]
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⩆")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⩇")]
    if result:
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⩈")] = result.outcome
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⩉")] = result.duration * 1000
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⩊")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⩋")]
        if result.failed:
            bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⩌")] = TestHubHandler.bstack1ll111l1l1l_opy_(call.excinfo.typename)
            bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⩍")] = TestHubHandler.bstack1ll11l11l1l1_opy_(call.excinfo, result)
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⩎")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⩏")]
    if outcome:
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⩐")] = bstack1llll1ll1lll_opy_(outcome)
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⩑")] = 0
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⩒")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⩓")]
        if bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩔")] == bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⩕"):
            bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⩖")] = bstack1l111l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ⩗")  # bstack1ll1111ll11l_opy_
            bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⩘")] = [{bstack1l111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⩙"): [bstack1l111l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ⩚")]}]
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⩛")] = bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⩜")]
    return bstack1llll1l11ll_opy_
def bstack1ll11111l1ll_opy_(test, bstack1lll1l1ll1l_opy_, bstack1111ll11ll_opy_, result, call, outcome, bstack1ll1111ll111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⩝")]
    hook_name = bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⩞")]
    hook_data = {
        bstack1l111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⩟"): bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⩠")],
        bstack1l111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⩡"): bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⩢"),
        bstack1l111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⩣"): bstack1l111l_opy_ (u"ࠩࡾࢁࠬ⩤").format(bstack1ll1l111llll_opy_(hook_name)),
        bstack1l111l_opy_ (u"ࠪࡦࡴࡪࡹࠨ⩥"): {
            bstack1l111l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩ⩦"): bstack1l111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⩧"),
            bstack1l111l_opy_ (u"࠭ࡣࡰࡦࡨࠫ⩨"): None
        },
        bstack1l111l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⩩"): test.name,
        bstack1l111l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⩪"): bstack1l1ll1l1ll_opy_.bstack1lll1l1l1l1_opy_(test, hook_name),
        bstack1l111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⩫"): file_path,
        bstack1l111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⩬"): file_path,
        bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⩭"): bstack1l111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⩮"),
        bstack1l111l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⩯"): file_path,
        bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⩰"): bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⩱")],
        bstack1l111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⩲"): bstack1l111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬ⩳") if bstack1ll111l11l11_opy_ == bstack1l111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ⩴") else bstack1l111l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⩵"),
        bstack1l111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ⩶"): hook_type
    }
    bstack1l1111ll111_opy_ = bstack1lll1l11111_opy_(_1lll1ll11l1_opy_.get(test.nodeid, None))
    if bstack1l1111ll111_opy_:
        hook_data[bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ⩷")] = bstack1l1111ll111_opy_
    if result:
        hook_data[bstack1l111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⩸")] = result.outcome
        hook_data[bstack1l111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⩹")] = result.duration * 1000
        hook_data[bstack1l111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩺")] = bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⩻")]
        if result.failed:
            hook_data[bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⩼")] = TestHubHandler.bstack1ll111l1l1l_opy_(call.excinfo.typename)
            hook_data[bstack1l111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⩽")] = TestHubHandler.bstack1ll11l11l1l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩾")] = bstack1llll1ll1lll_opy_(outcome)
        hook_data[bstack1l111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⩿")] = 100
        hook_data[bstack1l111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⪀")] = bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⪁")]
        if hook_data[bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⪂")] == bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⪃"):
            hook_data[bstack1l111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ⪄")] = bstack1l111l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨ⪅")  # bstack1ll1111ll11l_opy_
            hook_data[bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ⪆")] = [{bstack1l111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ⪇"): [bstack1l111l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧ⪈")]}]
    if bstack1ll1111ll111_opy_:
        hook_data[bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⪉")] = bstack1ll1111ll111_opy_.result
        hook_data[bstack1l111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⪊")] = bstack1ll1ll1l11l_opy_(bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⪋")], bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⪌")])
        hook_data[bstack1l111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⪍")] = bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⪎")]
        if hook_data[bstack1l111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⪏")] == bstack1l111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⪐"):
            hook_data[bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⪑")] = TestHubHandler.bstack1ll111l1l1l_opy_(bstack1ll1111ll111_opy_.exception_type)
            hook_data[bstack1l111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⪒")] = [{bstack1l111l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⪓"): bstack1lllll11ll11_opy_(bstack1ll1111ll111_opy_.exception)}]
    return hook_data
def bstack1ll111l111ll_opy_(test, bstack1lll1llll11_opy_, bstack1111ll11ll_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l111l_opy_ (u"ࠨࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ⪔").format(bstack1111ll11ll_opy_))
    bstack1llll1l11ll_opy_ = bstack1ll1111lllll_opy_(test, bstack1lll1llll11_opy_, result, call, bstack1111ll11ll_opy_, outcome)
    driver = getattr(test, bstack1l111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⪕"), None)
    if bstack1111ll11ll_opy_ == bstack1l111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⪖") and driver:
        bstack1llll1l11ll_opy_[bstack1l111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ⪗")] = TestHubHandler.bstack1llll11l1l1_opy_(driver)
    if bstack1111ll11ll_opy_ == bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⪘"):
        bstack1111ll11ll_opy_ = bstack1l111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⪙")
    bstack1lll1l11lll_opy_ = {
        bstack1l111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⪚"): bstack1111ll11ll_opy_,
        bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⪛"): bstack1llll1l11ll_opy_
    }
    TestHubHandler.bstack1ll1lll11l_opy_(bstack1lll1l11lll_opy_)
    if bstack1111ll11ll_opy_ == bstack1l111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⪜"):
        threading.current_thread().bstackTestMeta = {bstack1l111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⪝"): bstack1l111l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⪞")}
    elif bstack1111ll11ll_opy_ == bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⪟"):
        threading.current_thread().bstackTestMeta = {bstack1l111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⪠"): getattr(result, bstack1l111l_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨ⪡"), bstack1l111l_opy_ (u"ࠨࠩ⪢"))}
def bstack1ll1111l1lll_opy_(test, bstack1lll1llll11_opy_, bstack1111ll11ll_opy_, result=None, call=None, outcome=None, bstack1ll1111ll111_opy_=None):
    logger.debug(bstack1l111l_opy_ (u"ࠩࡶࡩࡳࡪ࡟ࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡨࡺࡪࡴࡴ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤ࡭ࡵ࡯࡬ࠢࡧࡥࡹࡧࠬࠡࡧࡹࡩࡳࡺࡔࡺࡲࡨࠤ࠲ࠦࡻࡾࠩ⪣").format(bstack1111ll11ll_opy_))
    hook_data = bstack1ll11111l1ll_opy_(test, bstack1lll1llll11_opy_, bstack1111ll11ll_opy_, result, call, outcome, bstack1ll1111ll111_opy_)
    bstack1lll1l11lll_opy_ = {
        bstack1l111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⪤"): bstack1111ll11ll_opy_,
        bstack1l111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭⪥"): hook_data
    }
    TestHubHandler.bstack1ll1lll11l_opy_(bstack1lll1l11lll_opy_)
def bstack1lll1l11111_opy_(bstack1lll1llll11_opy_):
    if not bstack1lll1llll11_opy_:
        return None
    if bstack1lll1llll11_opy_.get(bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⪦"), None):
        return getattr(bstack1lll1llll11_opy_[bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⪧")], bstack1l111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⪨"), None)
    return bstack1lll1llll11_opy_.get(bstack1l111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⪩"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG, TestHookState.POST, request, caplog)
        return # skip all existing operations
    try:
        if not TestHubHandler.on():
            return
        places = [bstack1l111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⪪"), bstack1l111l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⪫"), bstack1l111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⪬")]
        logs = []
        for bstack1ll11111l11l_opy_ in places:
            records = caplog.get_records(bstack1ll11111l11l_opy_)
            bstack1ll1111ll1l1_opy_ = bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⪭") if bstack1ll11111l11l_opy_ == bstack1l111l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⪮") else bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⪯")
            bstack1ll1111ll1ll_opy_ = request.node.nodeid + (bstack1l111l_opy_ (u"ࠨࠩ⪰") if bstack1ll11111l11l_opy_ == bstack1l111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⪱") else bstack1l111l_opy_ (u"ࠪ࠱ࠬ⪲") + bstack1ll11111l11l_opy_)
            test_uuid = bstack1lll1l11111_opy_(_1lll1ll11l1_opy_.get(bstack1ll1111ll1ll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1llll11lll1l_opy_(record.message):
                    continue
                logs.append({
                    bstack1l111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⪳"): bstack1lllll111ll1_opy_(record.created).isoformat() + bstack1l111l_opy_ (u"ࠬࡠࠧ⪴"),
                    bstack1l111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⪵"): record.levelname,
                    bstack1l111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⪶"): record.message,
                    bstack1ll1111ll1l1_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack1ll111l11_opy_(logs)
    except Exception as err:
        print(bstack1l111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ⪷"), str(err))
def bstack1lll1lll1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l1ll11l_opy_
    bstack1l1ll1llll_opy_ = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭⪸"), None) and bstack1l111l11l_opy_(
            threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⪹"), None)
    bstack11l11ll1ll_opy_ = getattr(driver, bstack1l111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⪺"), None) != None and getattr(driver, bstack1l111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ⪻"), None) == True
    if sequence == bstack1l111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⪼") and driver != None:
      if not bstack11l1ll11l_opy_ and bstack11ll1l1l1l_opy_() and bstack1l111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⪽") in CONFIG and CONFIG[bstack1l111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⪾")] == True and accessibility_scripts.bstack1111l1111_opy_(driver_command) and (bstack11l11ll1ll_opy_ or bstack1l1ll1llll_opy_) and not bstack1l111l1l1l_opy_(args):
        try:
          bstack11l1ll11l_opy_ = True
          logger.debug(bstack1l111l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫ⪿").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨ⫀").format(str(err)))
        bstack11l1ll11l_opy_ = False
    if sequence == bstack1l111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⫁"):
        if driver_command == bstack1l111l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ⫂"):
            TestHubHandler.bstack1l1ll11lll_opy_({
                bstack1l111l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ⫃"): response[bstack1l111l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭⫄")],
                bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⫅"): store[bstack1l111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⫆")]
            })
def bstack11ll111lll_opy_():
    global bstack1l1lll1l1_opy_
    logger_utils.bstack1l1111l1l1_opy_()
    logging.shutdown()
    TestHubHandler.bstack1lll1l1lll1_opy_()
    for driver in bstack1l1lll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l11l111_opy_(*args):
    global bstack1l1lll1l1_opy_
    TestHubHandler.bstack1lll1l1lll1_opy_()
    for driver in bstack1l1lll1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1l11l_opy_, stage=STAGE.bstack1l11llll1_opy_, bstack1lll1l1l1l_opy_=SESSION_NAME)
def bstack1111l1ll11_opy_(self, *args, **kwargs):
    bstack1lllll11_opy_ = bstack1lll1ll1ll_opy_(self, *args, **kwargs)
    bstack11l111ll1l_opy_ = getattr(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⫇"), None)
    if bstack11l111ll1l_opy_ and bstack11l111ll1l_opy_.get(bstack1l111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⫈"), bstack1l111l_opy_ (u"ࠬ࠭⫉")) == bstack1l111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⫊"):
        TestHubHandler.send_cbt_info(self)
    return bstack1lllll11_opy_
@measure(event_name=EVENTS.bstack111l1111ll_opy_, stage=STAGE.bstack11111ll1l1_opy_, bstack1lll1l1l1l_opy_=SESSION_NAME)
def bstack1ll11l111_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.bstack1ll11ll111_opy_()
    if global_config.get_property(bstack1l111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⫋")):
        return
    global_config.bstack1llllll11ll_opy_(bstack1l111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ⫌"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack11lll11l1_opy_.format(FRAMEWORK_NAME.split(bstack1l111l_opy_ (u"ࠩ࠰ࠫ⫍"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11ll1l1l1l_opy_():
            Service.start = bstack1l1111l1l_opy_
            Service.stop = bstack1l111l1lll_opy_
            webdriver.Remote.get = bstack1l1111ll11_opy_
            webdriver.Remote.__init__ = bstack1111l11l1_opy_
            if not isinstance(os.getenv(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ⫎")), str):
                return
            WebDriver.quit = bstack11l1llll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1111l1ll11_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l111l_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⫏")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1l111l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ⫐")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack111l11111l_opy_(bstack1l111l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣ⫑"), bstack11lll1l1l_opy_)
    if bstack11llll1ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l111l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⫒")) and callable(getattr(RemoteConnection, bstack1l111l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩ⫓"))):
                RemoteConnection._get_proxy_url = bstack1111llll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1111llll_opy_
        except Exception as e:
            logger.error(bstack1l1ll111_opy_.format(str(e)))
    if bstack1l111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⫔") in str(framework_name).lower():
        if not bstack11ll1l1l1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1llll1lll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1ll1lll1_opy_
            Config.getoption = bstack1ll11l1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll11111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack111l11ll_opy_, stage=STAGE.bstack1l11llll1_opy_, bstack1lll1l1l1l_opy_=SESSION_NAME)
def bstack11l1llll1_opy_(self):
    global FRAMEWORK_NAME
    global bstack1ll11l111l_opy_
    global bstack1lll11l11_opy_
    try:
        if bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⫕") in FRAMEWORK_NAME and self.session_id != None and bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨ⫖"), bstack1l111l_opy_ (u"ࠬ࠭⫗")) != bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⫘"):
            bstack1lll1l1lll_opy_ = bstack1l111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⫙") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⫚")
            bstack11l1lll1l_opy_(logger, True)
            if os.environ.get(bstack1l111l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⫛"), None):
                self.execute_script(
                    bstack1l111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ⫝̸") + json.dumps(
                        os.environ.get(bstack1l111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⫝"))) + bstack1l111l_opy_ (u"ࠬࢃࡽࠨ⫞"))
            if self != None:
                bstack1llll111l_opy_(self, bstack1lll1l1lll_opy_, bstack1l111l_opy_ (u"࠭ࠬࠡࠩ⫟").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll1ll1l_opy_(bstack1l11111l1_opy_):
            item = store.get(bstack1l111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⫠"), None)
            if item is not None and bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⫡"), None):
                bstack1ll11l1lll_opy_.bstack11ll111111_opy_(self, bstack1lllllllll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l111l_opy_ (u"ࠩࠪ⫢")
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ⫣") + str(e))
    bstack1lll11l11_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1lll1ll11l_opy_, stage=STAGE.bstack1l11llll1_opy_, bstack1lll1l1l1l_opy_=SESSION_NAME)
def bstack1111l11l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll11l111l_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1lll1ll1ll_opy_
    global bstack1l1lll1l1_opy_
    global bstack1111l1l1l_opy_
    global bstack111lll1lll_opy_
    global bstack1lllllllll1_opy_
    CONFIG[bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⫤")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack1l1lll111l_opy_(bstack1111l1l1l_opy_, CONFIG)
    logger.debug(bstack1l1ll11l1_opy_.format(command_executor))
    proxy = bstack1l111l1111_opy_(CONFIG, proxy)
    bstack11111l1l1l_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11111l1l1l_opy_ = int(os.environ.get(bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⫥")))
    except:
        bstack11111l1l1l_opy_ = 0
    bstack1ll1llll_opy_ = get_caps(CONFIG, bstack11111l1l1l_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll1llll_opy_)))
    bstack1lllllllll1_opy_ = CONFIG.get(bstack1l111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⫦"))[bstack11111l1l1l_opy_]
    if bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⫧") in CONFIG and CONFIG[bstack1l111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ⫨")]:
        update_caps_for_local(bstack1ll1llll_opy_, bstack111lll1lll_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack11111l1l1l_opy_) and a11y.is_platform_supported(bstack1ll1llll_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll1ll1l_opy_(bstack1l11111l1_opy_):
            a11y.set_capabilities(bstack1ll1llll_opy_, CONFIG)
    if desired_capabilities:
        bstack1llll111ll_opy_ = bstack1l11llll_opy_(desired_capabilities)
        bstack1llll111ll_opy_[bstack1l111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ⫩")] = bstack1ll111lll1_opy_(CONFIG)
        bstack1ll1l1ll1_opy_ = get_caps(bstack1llll111ll_opy_)
        if bstack1ll1l1ll1_opy_:
            bstack1ll1llll_opy_ = update(bstack1ll1l1ll1_opy_, bstack1ll1llll_opy_)
        desired_capabilities = None
    if options:
        bstack1lll1lllll_opy_(options, bstack1ll1llll_opy_)
    if not options:
        options = bstack11ll11l1l1_opy_(bstack1ll1llll_opy_)
    if proxy and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ⫪")):
        options.proxy(proxy)
    if options and bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⫫")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1l1ll11_opy_() < version.parse(bstack1l111l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⫬")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1llll_opy_)
    logger.info(bstack1lll1lll_opy_)
    bstack1llll111_opy_.end(EVENTS.bstack111l1111ll_opy_.value, EVENTS.bstack111l1111ll_opy_.value + bstack1l111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ⫭"),
                               EVENTS.bstack111l1111ll_opy_.value + bstack1l111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ⫮"), True, None)
    try:
        if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⫯")):
            bstack1lll1ll1ll_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⫰")):
            bstack1lll1ll1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ⫱")):
            bstack1lll1ll1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1lll1ll1ll_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1l1111llll_opy_:
        logger.error(bstack1llll1ll11_opy_.format(bstack1l111l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠪ⫲"), str(bstack1l1111llll_opy_)))
        raise bstack1l1111llll_opy_
    try:
        bstack111lll11ll_opy_ = bstack1l111l_opy_ (u"ࠬ࠭⫳")
        if bstack1ll1l1ll11_opy_() >= version.parse(bstack1l111l_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ⫴")):
            bstack111lll11ll_opy_ = self.caps.get(bstack1l111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⫵"))
        else:
            bstack111lll11ll_opy_ = self.capabilities.get(bstack1l111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ⫶"))
        if bstack111lll11ll_opy_:
            bstack11l11l1111_opy_(bstack111lll11ll_opy_)
            if bstack1ll1l1ll11_opy_() <= version.parse(bstack1l111l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ⫷")):
                self.command_executor._url = bstack1l111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⫸") + bstack1111l1l1l_opy_ + bstack1l111l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ⫹")
            else:
                self.command_executor._url = bstack1l111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ⫺") + bstack111lll11ll_opy_ + bstack1l111l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ⫻")
            logger.debug(bstack111lll111l_opy_.format(bstack111lll11ll_opy_))
        else:
            logger.debug(bstack11lllll11l_opy_.format(bstack1l111l_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ⫼")))
    except Exception as e:
        logger.debug(bstack11lllll11l_opy_.format(e))
    bstack1ll11l111l_opy_ = self.session_id
    if bstack1l111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⫽") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⫾"), None)
        if item:
            bstack1ll111l11l1l_opy_ = getattr(item, bstack1l111l_opy_ (u"ࠪࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⫿"), False)
            if not getattr(item, bstack1l111l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⬀"), None) and bstack1ll111l11l1l_opy_:
                setattr(store[bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⬁")], bstack1l111l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⬂"), self)
        bstack11l111ll1l_opy_ = getattr(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ⬃"), None)
        if bstack11l111ll1l_opy_ and bstack11l111ll1l_opy_.get(bstack1l111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⬄"), bstack1l111l_opy_ (u"ࠩࠪ⬅")) == bstack1l111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⬆"):
            TestHubHandler.send_cbt_info(self)
    bstack1l1lll1l1_opy_.append(self)
    if bstack1l111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⬇") in CONFIG and bstack1l111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⬈") in CONFIG[bstack1l111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⬉")][bstack11111l1l1l_opy_]:
        SESSION_NAME = CONFIG[bstack1l111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⬊")][bstack11111l1l1l_opy_][bstack1l111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⬋")]
    logger.debug(bstack1ll11111ll_opy_.format(bstack1ll11l111l_opy_))
@measure(event_name=EVENTS.bstack1l1lll1ll1_opy_, stage=STAGE.bstack1l11llll1_opy_, bstack1lll1l1l1l_opy_=SESSION_NAME)
def bstack1l1111ll11_opy_(self, url):
    global bstack11ll11l11l_opy_
    global CONFIG
    try:
        bstack1ll1l1lll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll11ll11l_opy_.format(str(err)))
    try:
        bstack11ll11l11l_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack1l1ll11ll1_opy_):
                bstack1ll1l1lll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll11ll11l_opy_.format(str(err)))
        raise e
def bstack1l1lll1l11_opy_(item, when):
    global bstack1l1l11l11l_opy_
    try:
        bstack1l1l11l11l_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11111_opy_(item, call, rep):
    global bstack11l11l11_opy_
    global bstack1l1lll1l1_opy_
    name = bstack1l111l_opy_ (u"ࠩࠪ⬌")
    try:
        if rep.when == bstack1l111l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ⬍"):
            bstack1ll11l111l_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l111l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⬎"))
            try:
                if (str(skipSessionName).lower() != bstack1l111l_opy_ (u"ࠬࡺࡲࡶࡧࠪ⬏")):
                    name = str(rep.nodeid)
                    bstack1l1llll1l_opy_ = bstack1ll11l11ll_opy_(bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⬐"), name, bstack1l111l_opy_ (u"ࠧࠨ⬑"), bstack1l111l_opy_ (u"ࠨࠩ⬒"), bstack1l111l_opy_ (u"ࠩࠪ⬓"), bstack1l111l_opy_ (u"ࠪࠫ⬔"))
                    os.environ[bstack1l111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ⬕")] = name
                    for driver in bstack1l1lll1l1_opy_:
                        if bstack1ll11l111l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1llll1l_opy_)
            except Exception as e:
                logger.debug(bstack1l111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⬖").format(str(e)))
            try:
                bstack11111l1l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ⬗"):
                    status = bstack1l111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⬘") if rep.outcome.lower() == bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⬙") else bstack1l111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⬚")
                    reason = bstack1l111l_opy_ (u"ࠪࠫ⬛")
                    if status == bstack1l111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⬜"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l111l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ⬝") if status == bstack1l111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⬞") else bstack1l111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⬟")
                    data = name + bstack1l111l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ⬠") if status == bstack1l111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⬡") else name + bstack1l111l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭⬢") + reason
                    bstack111ll11ll_opy_ = bstack1ll11l11ll_opy_(bstack1l111l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭⬣"), bstack1l111l_opy_ (u"ࠬ࠭⬤"), bstack1l111l_opy_ (u"࠭ࠧ⬥"), bstack1l111l_opy_ (u"ࠧࠨ⬦"), level, data)
                    for driver in bstack1l1lll1l1_opy_:
                        if bstack1ll11l111l_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll11ll_opy_)
            except Exception as e:
                logger.debug(bstack1l111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ⬧").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭⬨").format(str(e)))
    bstack11l11l11_opy_(item, call, rep)
notset = Notset()
def bstack1ll11l1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1111111l_opy_
    if str(name).lower() == bstack1l111l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ⬩"):
        return bstack1l111l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ⬪")
    else:
        return bstack1111111l_opy_(self, name, default, skip)
def bstack1111llll_opy_(self):
    global CONFIG
    global bstack1ll1l11l11_opy_
    try:
        proxy = bstack1l1llll111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l111l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ⬫")):
                proxies = bstack1111111ll_opy_(proxy, bstack1l1lll111l_opy_())
                if len(proxies) > 0:
                    protocol, bstack11l1ll1l1_opy_ = proxies.popitem()
                    if bstack1l111l_opy_ (u"ࠨ࠺࠰࠱ࠥ⬬") in bstack11l1ll1l1_opy_:
                        return bstack11l1ll1l1_opy_
                    else:
                        return bstack1l111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⬭") + bstack11l1ll1l1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧ⬮").format(str(e)))
    return bstack1ll1l11l11_opy_(self)
def bstack11llll1ll_opy_():
    return (bstack1l111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⬯") in CONFIG or bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⬰") in CONFIG) and bstack111l1111_opy_() and bstack1ll1l1ll11_opy_() >= version.parse(
        bstack111lll1l1l_opy_)
def bstack11l1l11ll_opy_(self,
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
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    CONFIG[bstack1l111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭⬱")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack11111l1l1l_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11111l1l1l_opy_ = int(os.environ.get(bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⬲")))
    except:
        bstack11111l1l1l_opy_ = 0
    CONFIG[bstack1l111l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ⬳")] = True
    bstack1ll1llll_opy_ = get_caps(CONFIG, bstack11111l1l1l_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll1llll_opy_)))
    if CONFIG.get(bstack1l111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⬴")):
        update_caps_for_local(bstack1ll1llll_opy_, bstack111lll1lll_opy_)
    if bstack1l111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⬵") in CONFIG and bstack1l111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ⬶") in CONFIG[bstack1l111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⬷")][bstack11111l1l1l_opy_]:
        SESSION_NAME = CONFIG[bstack1l111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⬸")][bstack11111l1l1l_opy_][bstack1l111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⬹")]
    import urllib
    import json
    if bstack1l111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⬺") in CONFIG and str(CONFIG[bstack1l111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⬻")]).lower() != bstack1l111l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⬼"):
        bstack1llllll111l_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1llllll111l_opy_ + urllib.parse.quote(json.dumps(bstack1ll1llll_opy_))
    else:
        cdpUrl = bstack1l111l_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ⬽") + urllib.parse.quote(json.dumps(bstack1ll1llll_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l11l1lll_opy_
        if not bstack11ll1l1l1l_opy_():
            global bstack11l1lll1_opy_
            if not bstack11l1lll1_opy_:
                from bstack_utils.helper import bstack1l11l1l1_opy_, bstack1lllll1l1111_opy_
                bstack11l1lll1_opy_ = bstack1l11l1l1_opy_()
                bstack1lllll1l1111_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l1l11l1lll_opy_
            return
        BrowserType.launch = bstack11l1l11ll_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll11111ll1l_opy_():
    global CONFIG
    global bstack1111l111_opy_
    global bstack1111l1l1l_opy_
    global bstack111lll1lll_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack11111l1ll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ⬾")))
    bstack1111l111_opy_ = eval(os.environ.get(bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⬿")))
    bstack1111l1l1l_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ⭀"))
    bstack111l111l_opy_(CONFIG, bstack1111l111_opy_)
    bstack11111l1ll1_opy_ = logger_utils.configure_logger(CONFIG, bstack11111l1ll1_opy_)
    if cli.bstack1llll11111_opy_():
        bstack111l11lll1_opy_.invoke(Events.CONNECT, bstack1l1l1l1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⭁"), bstack1l111l_opy_ (u"ࠧ࠱ࠩ⭂")))
        cli.bstack111lll1l1_opy_(cli_context.platform_index)
        cli.bstack1l11llll111_opy_(bstack1l1lll111l_opy_(bstack1111l1l1l_opy_, CONFIG), cli_context.platform_index, bstack11ll11l1l1_opy_)
        cli.bstack1ll1ll11ll_opy_()
        logger.debug(bstack1l111l_opy_ (u"ࠣࡅࡏࡍࠥ࡯ࡳࠡࡣࡦࡸ࡮ࡼࡥࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢ⭃") + str(cli_context.platform_index) + bstack1l111l_opy_ (u"ࠤࠥ⭄"))
        return # skip all existing operations
    global bstack1lll1ll1ll_opy_
    global bstack1lll11l11_opy_
    global bstack11111ll1_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack1ll1l1lll_opy_
    global bstack1l1111111_opy_
    global bstack111ll1l11_opy_
    global bstack11ll11l11l_opy_
    global bstack1ll1l11l11_opy_
    global bstack1111111l_opy_
    global bstack1l1l11l11l_opy_
    global bstack11l11l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll1ll1ll_opy_ = webdriver.Remote.__init__
        bstack1lll11l11_opy_ = WebDriver.quit
        bstack111ll1l11_opy_ = WebDriver.close
        bstack11ll11l11l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⭅") in CONFIG or bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⭆") in CONFIG) and bstack111l1111_opy_():
        if bstack1ll1l1ll11_opy_() < version.parse(bstack111lll1l1l_opy_):
            logger.error(bstack1l1l1ll11l_opy_.format(bstack1ll1l1ll11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l111l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⭇")) and callable(getattr(RemoteConnection, bstack1l111l_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⭈"))):
                    bstack1ll1l11l11_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1ll1l11l11_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1ll111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1111111l_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l11l11l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1l111l_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢ⭉"), bstack1l11l111_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack11l11l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ⭊"))
    bstack111lll1lll_opy_ = CONFIG.get(bstack1l111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭⭋"), {}).get(bstack1l111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⭌"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack1ll11l111_opy_(bstack111l1l11l_opy_)
if (bstack1llll111llll_opy_()):
    bstack1ll11111ll1l_opy_()
@error_handler(class_method=False)
def bstack1ll1111l111l_opy_(hook_name, event, bstack11l111111l1_opy_=None):
    if hook_name not in [bstack1l111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ⭍"), bstack1l111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ⭎"), bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⭏"), bstack1l111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⭐"), bstack1l111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⭑"), bstack1l111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⭒"), bstack1l111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ⭓"), bstack1l111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭⭔")]:
        return
    node = store[bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⭕")]
    if hook_name in [bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⭖"), bstack1l111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⭗")]:
        node = store[bstack1l111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ⭘")]
    elif hook_name in [bstack1l111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⭙"), bstack1l111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⭚")]:
        node = store[bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⭛")]
    hook_type = bstack1ll1l11l11ll_opy_(hook_name)
    if event == bstack1l111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⭜"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lll1l1ll1l_opy_ = {
            bstack1l111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⭝"): uuid,
            bstack1l111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⭞"): bstack111111l1l_opy_(),
            bstack1l111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⭟"): bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⭠"),
            bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⭡"): hook_type,
            bstack1l111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⭢"): hook_name
        }
        store[bstack1l111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⭣")].append(uuid)
        bstack1ll1111l1111_opy_ = node.nodeid
        if hook_type == bstack1l111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ⭤"):
            if not _1lll1ll11l1_opy_.get(bstack1ll1111l1111_opy_, None):
                _1lll1ll11l1_opy_[bstack1ll1111l1111_opy_] = {bstack1l111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⭥"): []}
            _1lll1ll11l1_opy_[bstack1ll1111l1111_opy_][bstack1l111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⭦")].append(bstack1lll1l1ll1l_opy_[bstack1l111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⭧")])
        _1lll1ll11l1_opy_[bstack1ll1111l1111_opy_ + bstack1l111l_opy_ (u"ࠪ࠱ࠬ⭨") + hook_name] = bstack1lll1l1ll1l_opy_
        bstack1ll1111l1lll_opy_(node, bstack1lll1l1ll1l_opy_, bstack1l111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⭩"))
    elif event == bstack1l111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ⭪"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l111111l1_opy_)
            return
        bstack1llll11111l_opy_ = node.nodeid + bstack1l111l_opy_ (u"࠭࠭ࠨ⭫") + hook_name
        _1lll1ll11l1_opy_[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⭬")] = bstack111111l1l_opy_()
        bstack1ll1111l1ll1_opy_(_1lll1ll11l1_opy_[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⭭")])
        bstack1ll1111l1lll_opy_(node, _1lll1ll11l1_opy_[bstack1llll11111l_opy_], bstack1l111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⭮"), bstack1ll1111ll111_opy_=bstack11l111111l1_opy_)
def bstack1ll1111l11l1_opy_():
    global bstack1ll111l11l11_opy_
    if bstack11l1l1ll1_opy_():
        bstack1ll111l11l11_opy_ = bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⭯")
    else:
        bstack1ll111l11l11_opy_ = bstack1l111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⭰")
@TestHubHandler.bstack1ll111lll1l1_opy_
def bstack1ll111111lll_opy_():
    bstack1ll1111l11l1_opy_()
    if cli.is_running():
        try:
            bstack1lll1ll1ll1l_opy_(bstack1ll1111l111l_opy_)
        except Exception as e:
            logger.debug(bstack1l111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ⭱").format(e))
        return
    if bstack111l1111_opy_():
        global_config = Config.bstack1ll11ll111_opy_()
        bstack1l111l_opy_ (u"࠭ࠧࠨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡ࠿ࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤ࡬࡫ࡴࡴࠢࡸࡷࡪࡪࠠࡧࡱࡵࠤࡦ࠷࠱ࡺࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠱ࡼࡸࡡࡱࡲ࡬ࡲ࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡷࠤ࡮ࡹࠠࡱࡣࡷࡧ࡭࡫ࡤࠡ࡫ࡱࠤࡦࠦࡤࡪࡨࡩࡩࡷ࡫࡮ࡵࠢࡳࡶࡴࡩࡥࡴࡵࠣ࡭ࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡵࡴࠢࡺࡩࠥࡴࡥࡦࡦࠣࡸࡴࠦࡵࡴࡧࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡕࡧࡴࡤࡪࠫࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡮ࡡ࡯ࡦ࡯ࡩࡷ࠯ࠠࡧࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠧࠨࠩ⭲")
        if global_config.get_property(bstack1l111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⭳")):
            if CONFIG.get(bstack1l111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⭴")) is not None and int(CONFIG[bstack1l111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⭵")]) > 1:
                bstack1llll111l1_opy_(bstack1lll1lll1l_opy_)
            return
        bstack1llll111l1_opy_(bstack1lll1lll1l_opy_)
    try:
        bstack1lll1ll1ll1l_opy_(bstack1ll1111l111l_opy_)
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⭶").format(e))
bstack1ll111111lll_opy_()