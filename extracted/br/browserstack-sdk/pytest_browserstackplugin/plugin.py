# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lll1l1ll1_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1111llll_opy_, update, bstack11l1111lll_opy_,
                                       bstack1l11l11l1l_opy_, bstack1lll1111l_opy_, bstack11111ll111_opy_, bstack11l1111l1l_opy_,
                                       bstack1l111ll1ll_opy_, bstack1l11l11ll_opy_, bstack1ll1ll1l_opy_,
                                       bstack11l1l11l1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11ll1l1_opy_)
from browserstack_sdk.bstack111ll11l_opy_ import bstack1ll1l1lll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1llll11llll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1111ll1111_opy_, bstack11l1111l11_opy_, bstack1111111l1_opy_, \
    bstack1llllll11l1_opy_
from bstack_utils.helper import bstack111lll1ll1_opy_, bstack1llll1ll1ll1_opy_, bstack1lll1l1l11l_opy_, bstack11l11lllll_opy_, bstack1l111llll1_opy_, bstack1llllll1l11_opy_, \
    bstack1llll1l11lll_opy_, \
    bstack1llllll1l111_opy_, bstack11lll1l11_opy_, bstack11llll11_opy_, bstack1llllll111ll_opy_, bstack1ll1l1llll_opy_, Notset, \
    bstack1l1l1l11ll_opy_, bstack1lll111l11l_opy_, bstack1llll1lll1ll_opy_, Result, bstack1llll1l1111l_opy_, bstack1lllll1l11l1_opy_, error_handler, \
    bstack1111llllll_opy_, bstack11llllllll_opy_, bstack1111l11lll_opy_, bstack1lllll111ll1_opy_
from bstack_utils.bstack1lll1ll1l111_opy_ import bstack1lll1lll1111_opy_
from bstack_utils.messages import bstack1l1111111l_opy_, bstack11l1l1l1l1_opy_, bstack11l11ll11_opy_, bstack111ll11l1l_opy_, bstack1lll1lllll_opy_, \
    bstack1lllllllll1_opy_, bstack111ll11ll_opy_, CONFIG_FILE_CONTENT, bstack11ll1l1l11_opy_, bstack1l1llll111_opy_, \
    bstack1ll1lll1ll_opy_, bstack1llll1l1l_opy_, bstack11l1l11111_opy_
from bstack_utils.proxy import bstack1ll11111l_opy_, bstack11l1111l1_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack1ll1l111ll1l_opy_, bstack1ll1l1111l1l_opy_, bstack1ll1l111lll1_opy_, bstack1ll1l11111l1_opy_, \
    bstack1ll1l111ll11_opy_, bstack1ll1l111l11l_opy_, bstack1ll1l111l1ll_opy_, bstack1l111l11_opy_, bstack1ll1l1111l11_opy_
from bstack_utils.bstack1l11ll11l1_opy_ import bstack1ll11l1ll1_opy_
from bstack_utils.bstack1lll1lll_opy_ import bstack1lll1l1l11_opy_, bstack111l1ll111_opy_, update_caps_for_local, \
    bstack11111lll11_opy_, bstack1lll1l1l1l_opy_
from bstack_utils.bstack1llll1l11ll_opy_ import bstack1llll1l1l1l_opy_
from bstack_utils.bstack11lll111_opy_ import bstack1lll1l11l_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack111l11lll_opy_ import bstack1l1111ll11_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack11ll1llll_opy_ import bstack111111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l111_opy_ import bstack1ll1l1l111_opy_, Events, bstack1ll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1lll111l1l1_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1ll1l1l111_opy_ import bstack1ll1l1l111_opy_, Events, bstack1ll1l1l1ll_opy_
bstack1l11l1l1_opy_ = None
bstack11l1lllll_opy_ = None
bstack111l1l11ll_opy_ = None
bstack1ll11ll11l_opy_ = None
bstack11ll1l111_opy_ = None
bstack1l1l11ll11_opy_ = None
bstack11l1llllll_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1111lll1l_opy_ = None
bstack11111l1l1l_opy_ = None
bstack11lll111l1_opy_ = None
bstack11l11ll1l_opy_ = None
bstack11lll1llll_opy_ = None
FRAMEWORK_NAME = bstack111ll11_opy_ (u"ࠪࠫ⤜")
CONFIG = {}
bstack1l1l11l1l1_opy_ = False
bstack1l1111llll_opy_ = bstack111ll11_opy_ (u"ࠫࠬ⤝")
bstack1lllll11lll_opy_ = bstack111ll11_opy_ (u"ࠬ࠭⤞")
PARALLELISE_VANILLA_PYTHON = False
bstack111lllll1l_opy_ = []
bstack11l11l1ll_opy_ = bstack1111ll1111_opy_
bstack1l1llllllll1_opy_ = bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⤟")
bstack11llll1ll_opy_ = {}
SESSION_NAME = None
bstack11111lll1_opy_ = False
logger = logger_utils.get_logger(__name__, bstack11l11l1ll_opy_)
store = {
    bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⤠"): []
}
bstack1ll1111ll11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lll1llll1l_opy_ = {}
current_test_uuid = None
cli_context = bstack1lll111l1l1_opy_(
    test_framework_name=bstack11l111ll_opy_[bstack111ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬ⤡")] if bstack1ll1l1llll_opy_() else bstack11l111ll_opy_[bstack111ll11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࠩ⤢")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack11l1ll111_opy_):
    try:
        page.evaluate(bstack111ll11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ⤣"),
                      bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨ⤤") + json.dumps(
                          bstack11l1ll111_opy_) + bstack111ll11_opy_ (u"ࠧࢃࡽࠣ⤥"))
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦ⤦"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack111ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ⤧"), bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭⤨") + json.dumps(
            message) + bstack111ll11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ⤩") + json.dumps(level) + bstack111ll11_opy_ (u"ࠪࢁࢂ࠭⤪"))
    except Exception as e:
        print(bstack111ll11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ⤫"), e)
def _1ll1111ll111_opy_():
    bstack111ll11_opy_ (u"ࠧࠨࠢࡘࡣ࡯࡯ࠥࡉࡗࡅࠢࡸࡴࡼࡧࡲࡥࠢ࡯ࡳࡴࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿࡡ࡮࡮࠱ࠦࠧࠨ⤬")
    bstack1ll11111111l_opy_ = os.getcwd()
    while True:
        for name in (bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ⤭"), bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ⤮")):
            candidate = os.path.join(bstack1ll11111111l_opy_, name)
            if os.path.exists(candidate):
                return candidate
        parent = os.path.dirname(bstack1ll11111111l_opy_)
        if parent == bstack1ll11111111l_opy_:
            break
        bstack1ll11111111l_opy_ = parent
    return None
def _1ll111111ll1_opy_():
    bstack111ll11_opy_ (u"ࠣࠤࠥࡈࡪࡺࡥࡤࡶࠣ࡭࡫ࠦࡰࡺࡶࡨࡷࡹࠦࡷࡢࡵࠣࡰࡦࡻ࡮ࡤࡪࡨࡨࠥࡨࡹࠡࡣࡱࠤࡎࡊࡅࠡࡴࡸࡲࡳ࡫ࡲ࠯ࠌࠣࠤࠥࠦࡕࡴࡧࡶࠤࡸࡺࡡࡣ࡮ࡨ࠰ࠥࡲ࡯࡯ࡩ࠰ࡰ࡮ࡼࡥࡥࠢࡨࡲࡻࠦࡶࡢࡴࡶࠤࡸ࡫ࡴࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡦࡥࡱࡲࡹࠡࡤࡼࠤࡎࡊࡅࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࡓ࡝ࡈࡎࡁࡓࡏࡢࡌࡔ࡙ࡔࡆࡆࠣࠤࠥࠦ⠔ࠡࡌࡨࡸࡇࡸࡡࡪࡰࡶࠤࡕࡿࡃࡩࡣࡵࡱࠥ࠮ࡾ࠳࠲࠴࠷࠰࠯ࠊࠡࠢࠣࠤࠥࠦࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠢࠣ⠘ࠥࡐࡥࡵࡄࡵࡥ࡮ࡴࡳࠡࡋࡇࡉࡸࠦࡶࡪࡣࠣࡘࡪࡧ࡭ࡄ࡫ࡷࡽࠥࡶࡲࡰࡶࡲࡧࡴࡲࠠࠩ࠳࠳࠯ࠥࡿࡥࡢࡴࡶ࠭ࠏࠦࠠࠡࠢࠥࠦࠧ⤯")
    return os.environ.get(bstack111ll11_opy_ (u"ࠩࡓ࡝ࡈࡎࡁࡓࡏࡢࡌࡔ࡙ࡔࡆࡆࠪ⤰")) == bstack111ll11_opy_ (u"ࠪ࠵ࠬ⤱") or \
           bool(os.environ.get(bstack111ll11_opy_ (u"࡙ࠫࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠧ⤲")))
def pytest_configure(config):
    global bstack1l1111llll_opy_
    global CONFIG
    global bstack1l1l11l1l1_opy_
    if not os.environ.get(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠩ⤳")) and _1ll111111ll1_opy_():
        _1ll11111llll_opy_ = _1ll1111ll111_opy_()
        if _1ll11111llll_opy_:
            try:
                from browserstack_sdk import bstack1l11l1l11l_opy_
                if bstack1l11l1l11l_opy_(_1ll11111llll_opy_):
                    CONFIG = json.loads(os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬ⤴"), bstack111ll11_opy_ (u"ࠧࡼࡿࠪ⤵")))
                    bstack1l1111llll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ⤶"), bstack111ll11_opy_ (u"ࠩࠪ⤷"))
                    bstack1l1l11l1l1_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⤸"), bstack111ll11_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪ⤹")).lower() == bstack111ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪ⤺")
            except Exception as e:
                logger.error(bstack111ll11_opy_ (u"ࠨࡐ࡭ࡷࡪ࡭ࡳࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨ⤻").format(e))
    global_config = Config.bstack1lllll1lll1_opy_()
    config.args = bstack1lll1l11l_opy_.bstack1ll1111lllll_opy_(config.args)
    global_config.bstack1l1lll11l1_opy_(bstack1111l11lll_opy_(config.getoption(bstack111ll11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⤼"))))
    try:
        logger_utils.bstack1lll1l11l11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1ll1l1l111_opy_.invoke(Events.CONNECT, bstack1ll1l1l1ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⤽"), bstack111ll11_opy_ (u"ࠩ࠳ࠫ⤾")))
        config = json.loads(os.environ.get(bstack111ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤ⤿"), bstack111ll11_opy_ (u"ࠦࢀࢃࠢ⥀")))
        cli.bstack1l1l11l11ll_opy_(bstack11llll11_opy_(bstack1l1111llll_opy_, CONFIG), cli_context.platform_index, bstack11l1111lll_opy_)
    if cli.bstack1l11ll11l_opy_(bstack111111l11l_opy_):
        cli.bstack111lll1lll_opy_()
        logger.debug(bstack111ll11_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⥁") + str(cli_context.platform_index) + bstack111ll11_opy_ (u"ࠨࠢ⥂"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
def pytest_unconfigure(config):
    bstack111ll11_opy_ (u"ࠢࠣࠤࡕࡹࡳࠦࡓࡅࡍࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡾࡺࡥࡴࡶࠣࠬࡦࡴࡤࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠫࠣ࡭ࡸࠦࡳࡵ࡫࡯ࡰࠥࡧ࡬ࡪࡸࡨ࠲ࠏࠦࠠࠡࠢࡌࡲࠥࡶ࡬ࡶࡩ࡬ࡲࠥࡳ࡯ࡥࡧ࠯ࠤࡧࡹࡴࡢࡥ࡮ࡣࡪࡾࡩࡵࡡ࡫ࡥࡳࡪ࡬ࡦࡴࠣࡪ࡮ࡸࡥࡴࠢࡤࡸࠥࡧࡴࡦࡺ࡬ࡸࠥࡨࡵࡵࠢࡥࡽࠥࡺࡨࡦࡰࠍࠤࠥࠦࠠࡱࡻࡷࡩࡸࡺࠠࡩࡣࡶࠤࡹࡵࡲ࡯ࠢࡧࡳࡼࡴࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠱ࠤࡗࡻ࡮࡯࡫ࡱ࡫ࠥ࡯ࡴࠡࡪࡨࡶࡪࠦࡥ࡯ࡵࡸࡶࡪࡹࠊࠡࠢࠣࠤࡹ࡮ࡥࠡࡤࡸ࡭ࡱࡪࠠ࡭࡫ࡱ࡯ࠥࡧ࡮ࡥࠢࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡰࡩࡸࡹࡡࡨࡧࡶࠤࡷ࡫ࡡࡤࡪࠣࡸ࡭࡫ࠠࡤࡱࡱࡷࡴࡲࡥ࠯ࠤࠥࠦ⥃")
    if os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡆࡈࡣࡕࡒࡕࡈࡋࡑࡣࡒࡕࡄࡆࠩ⥄")) and cli.is_running():
        from browserstack_sdk import bstack1ll111l1_opy_
        bstack1ll111l1_opy_()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack111ll11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ⥅"), None)
    if cli.is_running() and when == bstack111ll11_opy_ (u"ࠥࡧࡦࡲ࡬ࠣ⥆"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack111ll11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⥇"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⥈")))
        if not passed:
            config = json.loads(os.environ.get(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠧ⥉"), bstack111ll11_opy_ (u"ࠢࡼࡿࠥ⥊")))
            if bstack1l1111ll11_opy_.bstack11111lll1l_opy_(config):
                bstack1ll1ll1111ll_opy_ = bstack1l1111ll11_opy_.bstack1l11l1l1l_opy_(config)
                if item.execution_count > bstack1ll1ll1111ll_opy_:
                    print(bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࡸࡥࡵࡴ࡬ࡩࡸࡀࠠࠨ⥋"), report.nodeid, os.environ.get(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⥌")))
                    bstack1l1111ll11_opy_.bstack1lll111l1lll_opy_(report.nodeid)
            else:
                print(bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠪ⥍"), report.nodeid, os.environ.get(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⥎")))
                bstack1l1111ll11_opy_.bstack1lll111l1lll_opy_(report.nodeid)
        else:
            print(bstack111ll11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡴࡦࡹࡳࡦࡦ࠽ࠤࠬ⥏"), report.nodeid, os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⥐")))
    if cli.is_running():
        if when == bstack111ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⥑"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack111ll11_opy_ (u"ࠣࡥࡤࡰࡱࠨ⥒"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack111ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ⥓"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack111ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⥔"))
    plugins = item.config.getoption(bstack111ll11_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧ⥕"))
    report = outcome.get_result()
    os.environ[bstack111ll11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⥖")] = report.nodeid
    bstack1ll111111l11_opy_(item, call, report)
    if bstack111ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦ⥗") not in plugins or bstack1ll1l1llll_opy_():
        return
    summary = []
    driver = getattr(item, bstack111ll11_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣ⥘"), None)
    page = getattr(item, bstack111ll11_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢ⥙"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll1111l11l1_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1l1llllll1ll_opy_(item, report, summary, skipSessionName)
def bstack1ll1111l11l1_opy_(item, report, summary, skipSessionName):
    if report.when == bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⥚") and report.skipped:
        bstack1ll1l1111l11_opy_(report)
    if report.when in [bstack111ll11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⥛"), bstack111ll11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⥜")]:
        return
    if not bstack1l111llll1_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack111ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪ⥝")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ⥞") + json.dumps(
                    report.nodeid) + bstack111ll11_opy_ (u"ࠧࡾࡿࠪ⥟"))
        os.environ[bstack111ll11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⥠")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤ⥡").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⥢")))
    bstack1l11l1lll_opy_ = bstack111ll11_opy_ (u"ࠦࠧ⥣")
    bstack1ll1l1111l11_opy_(report)
    if not passed:
        try:
            bstack1l11l1lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111ll11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ⥤").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11l1lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⥥")))
        bstack1l11l1lll_opy_ = bstack111ll11_opy_ (u"ࠢࠣ⥦")
        if not passed:
            try:
                bstack1l11l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111ll11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⥧").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11l1lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭⥨")
                    + json.dumps(bstack111ll11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦ⥩"))
                    + bstack111ll11_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢ⥪")
                )
            else:
                item._driver.execute_script(
                    bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ⥫")
                    + json.dumps(str(bstack1l11l1lll_opy_))
                    + bstack111ll11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ⥬")
                )
        except Exception as e:
            summary.append(bstack111ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧ⥭").format(e))
def bstack1ll1111111ll_opy_(test_name, error_message):
    try:
        bstack1ll111111l1l_opy_ = []
        bstack1l1ll11l1l_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⥮"), bstack111ll11_opy_ (u"ࠩ࠳ࠫ⥯"))
        bstack1llll1111l_opy_ = {bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⥰"): test_name, bstack111ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ⥱"): error_message, bstack111ll11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ⥲"): bstack1l1ll11l1l_opy_}
        bstack1ll111111111_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ⥳"))
        if os.path.exists(bstack1ll111111111_opy_):
            with open(bstack1ll111111111_opy_) as f:
                bstack1ll111111l1l_opy_ = json.load(f)
        bstack1ll111111l1l_opy_.append(bstack1llll1111l_opy_)
        with open(bstack1ll111111111_opy_, bstack111ll11_opy_ (u"ࠧࡸࠩ⥴")) as f:
            json.dump(bstack1ll111111l1l_opy_, f)
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭⥵") + str(e))
def bstack1l1llllll1ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack111ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ⥶"), bstack111ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ⥷")]:
        return
    if (str(skipSessionName).lower() != bstack111ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩ⥸")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111ll11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢ⥹")))
    bstack1l11l1lll_opy_ = bstack111ll11_opy_ (u"ࠨࠢ⥺")
    bstack1ll1l1111l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l11l1lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢ⥻").format(e)
                )
        try:
            if passed:
                bstack1lll1l1l1l_opy_(getattr(item, bstack111ll11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⥼"), None), bstack111ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ⥽"))
            else:
                error_message = bstack111ll11_opy_ (u"ࠪࠫ⥾")
                if bstack1l11l1lll_opy_:
                    playwright_annotate(item._page, str(bstack1l11l1lll_opy_), bstack111ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ⥿"))
                    bstack1lll1l1l1l_opy_(getattr(item, bstack111ll11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ⦀"), None), bstack111ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ⦁"), str(bstack1l11l1lll_opy_))
                    error_message = str(bstack1l11l1lll_opy_)
                else:
                    bstack1lll1l1l1l_opy_(getattr(item, bstack111ll11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭⦂"), None), bstack111ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ⦃"))
                bstack1ll1111111ll_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨ⦄").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack111ll11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ⦅"), default=bstack111ll11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ⦆"), help=bstack111ll11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ⦇"))
    parser.addoption(bstack111ll11_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ⦈"), default=bstack111ll11_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ⦉"), help=bstack111ll11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ⦊"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111ll11_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ⦋"), action=bstack111ll11_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ⦌"), default=bstack111ll11_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ⦍"),
                         help=bstack111ll11_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦ⦎"))
def bstack1llll11l1l1_opy_(log):
    if not (log[bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⦏")] and log[bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⦐")].strip()):
        return
    active = bstack1llll11l11l_opy_()
    log = {
        bstack111ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⦑"): log[bstack111ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⦒")],
        bstack111ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⦓"): bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"ࠫ࡟࠭⦔"),
        bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⦕"): log[bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⦖")],
    }
    if active:
        if active[bstack111ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬ⦗")] == bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭⦘"):
            log[bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⦙")] = active[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⦚")]
        elif active[bstack111ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⦛")] == bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪ⦜"):
            log[bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⦝")] = active[bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⦞")]
    TestHubHandler.bstack111ll11lll_opy_([log])
def bstack1llll11l11l_opy_():
    if len(store[bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⦟")]) > 0 and store[bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⦠")][-1]:
        return {
            bstack111ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ⦡"): bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⦢"),
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⦣"): store[bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⦤")][-1]
        }
    if store.get(bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⦥"), None):
        return {
            bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⦦"): bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࠧ⦧"),
            bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⦨"): store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⦩")]
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
        item._1ll1111l1l11_opy_ = True
        bstack111l11111_opy_ = a11y.is_enabled_testcase(bstack1llllll1l111_opy_(item.own_markers))
        if not cli.bstack1l11ll11l_opy_(bstack111111l11l_opy_):
            item._a11y_test_case = bstack111l11111_opy_
            if bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⦪"), None):
                driver = getattr(item, bstack111ll11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ⦫"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack111l11111_opy_)
        if not TestHubHandler.on() or bstack1l1llllllll1_opy_ != bstack111ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⦬"):
            return
        global current_test_uuid #, bstack1llll1l1lll_opy_
        bstack1lll1lllll1_opy_ = {
            bstack111ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⦭"): uuid4().__str__(),
            bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⦮"): bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"ࠪ࡞ࠬ⦯")
        }
        current_test_uuid = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⦰")]
        store[bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⦱")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⦲")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lll1llll1l_opy_[item.nodeid] = {**_1lll1llll1l_opy_[item.nodeid], **bstack1lll1lllll1_opy_}
        bstack1l1lllllllll_opy_(item, _1lll1llll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⦳"))
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪ⦴"), str(err))
def pytest_runtest_setup(item):
    store[bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⦵")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⦶"))
    if bstack1l1111ll11_opy_.bstack1lll11l11111_opy_():
            bstack1ll11111ll1l_opy_ = bstack111ll11_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡦࡹࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣ⦷")
            logger.error(bstack1ll11111ll1l_opy_)
            bstack1lll1lllll1_opy_ = {
                bstack111ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⦸"): uuid4().__str__(),
                bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⦹"): bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"࡛ࠧࠩ⦺"),
                bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⦻"): bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"ࠩ࡝ࠫ⦼"),
                bstack111ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⦽"): bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⦾"),
                bstack111ll11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⦿"): bstack1ll11111ll1l_opy_,
                bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⧀"): [],
                bstack111ll11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⧁"): []
            }
            bstack1l1lllllllll_opy_(item, bstack1lll1lllll1_opy_, bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⧂"))
            pytest.skip(bstack1ll11111ll1l_opy_)
            return # skip all existing operations
    global bstack1ll1111ll11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1llllll111ll_opy_():
        atexit.register(bstack1ll111l1_opy_)
        if not bstack1ll1111ll11l_opy_:
            try:
                bstack1ll11111lll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1lllll111ll1_opy_():
                    bstack1ll11111lll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11111lll1_opy_:
                    signal.signal(s, bstack1ll1l111lll_opy_)
                bstack1ll1111ll11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡳࡪࡩࡱࡥࡱࠦࡨࡢࡰࡧࡰࡪࡸࡳ࠻ࠢࠥ⧃") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1l111ll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⧄")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lll1lllll1_opy_ = {
            bstack111ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⧅"): uuid,
            bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⧆"): bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"࡚࠭ࠨ⧇"),
            bstack111ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬ⧈"): bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭⧉"),
            bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⧊"): bstack111ll11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ⧋"),
            bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ⧌"): bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⧍")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⧎")] = item
        store[bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⧏")] = [uuid]
        if not _1lll1llll1l_opy_.get(item.nodeid, None):
            _1lll1llll1l_opy_[item.nodeid] = {bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⧐"): [], bstack111ll11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⧑"): []}
        _1lll1llll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⧒")].append(bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⧓")])
        _1lll1llll1l_opy_[item.nodeid + bstack111ll11_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬ⧔")] = bstack1lll1lllll1_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll1111l1ll1_opy_(item, bstack1lll1lllll1_opy_, bstack111ll11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⧕"))
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪ⧖"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⧗"))
        return # skip all existing operations
    try:
        global bstack11llll1ll_opy_
        bstack1l1ll11l1l_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l1ll11l1l_opy_ = int(os.environ.get(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⧘")))
        if bstack1llll1l11l_opy_.bstack1llll11lll_opy_() == bstack111ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ⧙"):
            if bstack1llll1l11l_opy_.bstack11111l11l_opy_() == bstack111ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ⧚"):
                bstack1ll1111l111l_opy_ = bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⧛"), None)
                bstack1111llll1_opy_ = bstack1ll1111l111l_opy_ + bstack111ll11_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤ⧜")
                driver = getattr(item, bstack111ll11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⧝"), None)
                bstack1ll11l11ll_opy_ = getattr(item, bstack111ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⧞"), None)
                bstack1l11llll11_opy_ = getattr(item, bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⧟"), None)
                PercySDK.screenshot(driver, bstack1111llll1_opy_, bstack1ll11l11ll_opy_=bstack1ll11l11ll_opy_, bstack1l11llll11_opy_=bstack1l11llll11_opy_, bstack111l1l1lll_opy_=bstack1l1ll11l1l_opy_)
        if not cli.bstack1l11ll11l_opy_(bstack111111l11l_opy_):
            if getattr(item, bstack111ll11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪ⧠"), False):
                bstack1ll1l1lll1_opy_.bstack1lllllll1ll_opy_(getattr(item, bstack111ll11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⧡"), None), bstack11llll1ll_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lll1lllll1_opy_ = {
            bstack111ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⧢"): uuid4().__str__(),
            bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⧣"): bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"࡛ࠧࠩ⧤"),
            bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⧥"): bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⧦"),
            bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⧧"): bstack111ll11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ⧨"),
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⧩"): bstack111ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⧪")
        }
        _1lll1llll1l_opy_[item.nodeid + bstack111ll11_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⧫")] = bstack1lll1lllll1_opy_
        bstack1ll1111l1ll1_opy_(item, bstack1lll1lllll1_opy_, bstack111ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⧬"))
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨ⧭"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1ll1l11111l1_opy_(fixturedef.argname):
        store[bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⧮")] = request.node
    elif bstack1ll1l111ll11_opy_(fixturedef.argname):
        store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ⧯")] = request.node
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
            bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⧰"): fixturedef.argname,
            bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⧱"): bstack1llll1l11lll_opy_(outcome),
            bstack111ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⧲"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⧳")]
        if not _1lll1llll1l_opy_.get(current_test_item.nodeid, None):
            _1lll1llll1l_opy_[current_test_item.nodeid] = {bstack111ll11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ⧴"): []}
        _1lll1llll1l_opy_[current_test_item.nodeid][bstack111ll11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⧵")].append(fixture)
    except Exception as err:
        logger.debug(bstack111ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ⧶"), str(err))
if bstack1ll1l1llll_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1lll1llll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⧷")].bstack1lllllll111_opy_(id(step))
        except Exception as err:
            print(bstack111ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫ⧸"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1lll1llll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⧹")].bstack1llll11ll11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⧺"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            bstack1llll1l11ll_opy_: bstack1llll1l1l1l_opy_ = _1lll1llll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ⧻")]
            bstack1llll1l11ll_opy_.bstack1llll11ll11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧ⧼"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1l1llllllll1_opy_
        try:
            if not TestHubHandler.on() or bstack1l1llllllll1_opy_ != bstack111ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ⧽"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ⧾"), None)
            if not _1lll1llll1l_opy_.get(request.node.nodeid, None):
                _1lll1llll1l_opy_[request.node.nodeid] = {}
            bstack1llll1l11ll_opy_ = bstack1llll1l1l1l_opy_.bstack1ll11l1lllll_opy_(
                scenario, feature, request.node,
                name=bstack1ll1l111l11l_opy_(request.node, scenario),
                started_at=bstack1llllll1l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111ll11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ⧿"),
                tags=bstack1ll1l111l1ll_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llll111l1l_opy_(driver) if driver and driver.session_id else {}
            )
            _1lll1llll1l_opy_[request.node.nodeid][bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⨀")] = bstack1llll1l11ll_opy_
            bstack1ll1111l1111_opy_(bstack1llll1l11ll_opy_.uuid)
            TestHubHandler.bstack1llll1l11l1_opy_(bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⨁"), bstack1llll1l11ll_opy_)
        except Exception as err:
            print(bstack111ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ⨂"), str(err))
def bstack1ll11111l111_opy_(bstack1llll11ll1l_opy_):
    if bstack1llll11ll1l_opy_ in store[bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⨃")]:
        store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⨄")].remove(bstack1llll11ll1l_opy_)
def bstack1ll1111l1111_opy_(test_uuid):
    store[bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⨅")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll111ll1l11_opy_
def bstack1ll111111l11_opy_(item, call, report):
    logger.debug(bstack111ll11_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠨ⨆"))
    global bstack1l1llllllll1_opy_
    bstack11111lllll_opy_ = bstack1llllll1l11_opy_()
    if hasattr(report, bstack111ll11_opy_ (u"ࠧࡴࡶࡲࡴࠬ⨇")):
        bstack11111lllll_opy_ = bstack1llll1l1111l_opy_(report.stop)
    elif hasattr(report, bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧ⨈")):
        bstack11111lllll_opy_ = bstack1llll1l1111l_opy_(report.start)
    try:
        if getattr(report, bstack111ll11_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⨉"), bstack111ll11_opy_ (u"ࠪࠫ⨊")) == bstack111ll11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⨋"):
            logger.debug(bstack111ll11_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⨌").format(getattr(report, bstack111ll11_opy_ (u"࠭ࡷࡩࡧࡱࠫ⨍"), bstack111ll11_opy_ (u"ࠧࠨ⨎")).__str__(), bstack1l1llllllll1_opy_))
            if bstack1l1llllllll1_opy_ == bstack111ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⨏"):
                _1lll1llll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⨐")] = bstack11111lllll_opy_
                bstack1l1lllllllll_opy_(item, _1lll1llll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⨑"), report, call)
                store[bstack111ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⨒")] = None
            elif bstack1l1llllllll1_opy_ == bstack111ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ⨓"):
                bstack1llll1l11ll_opy_ = _1lll1llll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⨔")]
                bstack1llll1l11ll_opy_.set(hooks=_1lll1llll1l_opy_[item.nodeid].get(bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⨕"), []))
                exception, bstack1llll111lll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llll111lll_opy_ = [call.excinfo.exconly(), getattr(report, bstack111ll11_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧ⨖"), bstack111ll11_opy_ (u"ࠩࠪ⨗"))]
                bstack1llll1l11ll_opy_.stop(time=bstack11111lllll_opy_, result=Result(result=getattr(report, bstack111ll11_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ⨘"), bstack111ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⨙")), exception=exception, bstack1llll111lll_opy_=bstack1llll111lll_opy_))
                TestHubHandler.bstack1llll1l11l1_opy_(bstack111ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⨚"), _1lll1llll1l_opy_[item.nodeid][bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⨛")])
        elif getattr(report, bstack111ll11_opy_ (u"ࠧࡸࡪࡨࡲࠬ⨜"), bstack111ll11_opy_ (u"ࠨࠩ⨝")) in [bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ⨞"), bstack111ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⨟")]:
            logger.debug(bstack111ll11_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡸࡪࠦ࠭ࠡࡽࢀ࠰ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࠯ࠣࡿࢂ࠭⨠").format(getattr(report, bstack111ll11_opy_ (u"ࠬࡽࡨࡦࡰࠪ⨡"), bstack111ll11_opy_ (u"࠭ࠧ⨢")).__str__(), bstack1l1llllllll1_opy_))
            bstack1llll1l1l11_opy_ = item.nodeid + bstack111ll11_opy_ (u"ࠧ࠮ࠩ⨣") + getattr(report, bstack111ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⨤"), bstack111ll11_opy_ (u"ࠩࠪ⨥"))
            if getattr(report, bstack111ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⨦"), False):
                hook_type = bstack111ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⨧") if getattr(report, bstack111ll11_opy_ (u"ࠬࡽࡨࡦࡰࠪ⨨"), bstack111ll11_opy_ (u"࠭ࠧ⨩")) == bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⨪") else bstack111ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ⨫")
                _1lll1llll1l_opy_[bstack1llll1l1l11_opy_] = {
                    bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⨬"): uuid4().__str__(),
                    bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⨭"): bstack11111lllll_opy_,
                    bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⨮"): hook_type
                }
            _1lll1llll1l_opy_[bstack1llll1l1l11_opy_][bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⨯")] = bstack11111lllll_opy_
            bstack1ll11111l111_opy_(_1lll1llll1l_opy_[bstack1llll1l1l11_opy_][bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⨰")])
            bstack1ll1111l1ll1_opy_(item, _1lll1llll1l_opy_[bstack1llll1l1l11_opy_], bstack111ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⨱"), report, call)
            if getattr(report, bstack111ll11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⨲"), bstack111ll11_opy_ (u"ࠩࠪ⨳")) == bstack111ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⨴"):
                if getattr(report, bstack111ll11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⨵"), bstack111ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⨶")) == bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⨷"):
                    bstack1lll1lllll1_opy_ = {
                        bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⨸"): uuid4().__str__(),
                        bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⨹"): bstack1llllll1l11_opy_(),
                        bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⨺"): bstack1llllll1l11_opy_()
                    }
                    _1lll1llll1l_opy_[item.nodeid] = {**_1lll1llll1l_opy_[item.nodeid], **bstack1lll1lllll1_opy_}
                    bstack1l1lllllllll_opy_(item, _1lll1llll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⨻"))
                    bstack1l1lllllllll_opy_(item, _1lll1llll1l_opy_[item.nodeid], bstack111ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⨼"), report, call)
    except Exception as err:
        print(bstack111ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪ⨽"), str(err))
def bstack1ll11111l1l1_opy_(test, bstack1lll1lllll1_opy_, result=None, call=None, bstack11l111l11_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1llll1l11ll_opy_ = {
        bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⨾"): bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⨿")],
        bstack111ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⩀"): bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࠧ⩁"),
        bstack111ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ⩂"): test.name,
        bstack111ll11_opy_ (u"ࠫࡧࡵࡤࡺࠩ⩃"): {
            bstack111ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪ⩄"): bstack111ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⩅"),
            bstack111ll11_opy_ (u"ࠧࡤࡱࡧࡩࠬ⩆"): inspect.getsource(test.obj)
        },
        bstack111ll11_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⩇"): test.name,
        bstack111ll11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨ⩈"): test.name,
        bstack111ll11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ⩉"): bstack1lll1l11l_opy_.bstack1lll1l1l1l1_opy_(test),
        bstack111ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ⩊"): file_path,
        bstack111ll11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧ⩋"): file_path,
        bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⩌"): bstack111ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⩍"),
        bstack111ll11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭⩎"): file_path,
        bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⩏"): bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⩐")],
        bstack111ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⩑"): bstack111ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⩒"),
        bstack111ll11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩ⩓"): {
            bstack111ll11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫ⩔"): test.nodeid
        },
        bstack111ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⩕"): bstack1llllll1l111_opy_(test.own_markers)
    }
    if bstack11l111l11_opy_ in [bstack111ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⩖"), bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⩗")]:
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ⩘")] = {
            bstack111ll11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⩙"): bstack1lll1lllll1_opy_.get(bstack111ll11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⩚"), [])
        }
    if bstack11l111l11_opy_ == bstack111ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⩛"):
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⩜")] = bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⩝")
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⩞")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⩟")]
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⩠")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⩡")]
    if result:
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩢")] = result.outcome
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⩣")] = result.duration * 1000
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⩤")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩥")]
        if result.failed:
            bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⩦")] = TestHubHandler.bstack1ll111l1l1l_opy_(call.excinfo.typename)
            bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⩧")] = TestHubHandler.bstack1ll111lllll1_opy_(call.excinfo, result)
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⩨")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⩩")]
    if outcome:
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⩪")] = bstack1llll1l11lll_opy_(outcome)
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⩫")] = 0
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩬")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⩭")]
        if bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⩮")] == bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⩯"):
            bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭⩰")] = bstack111ll11_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ⩱")  # bstack1l1lllllll1l_opy_
            bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⩲")] = [{bstack111ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⩳"): [bstack111ll11_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ⩴")]}]
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⩵")] = bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⩶")]
    return bstack1llll1l11ll_opy_
def bstack1ll111111lll_opy_(test, bstack1lll1l11ll1_opy_, bstack11l111l11_opy_, result, call, outcome, bstack1ll1111ll1l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⩷")]
    hook_name = bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ⩸")]
    hook_data = {
        bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⩹"): bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⩺")],
        bstack111ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⩻"): bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⩼"),
        bstack111ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⩽"): bstack111ll11_opy_ (u"ࠧࡼࡿࠪ⩾").format(bstack1ll1l1111l1l_opy_(hook_name)),
        bstack111ll11_opy_ (u"ࠨࡤࡲࡨࡾ࠭⩿"): {
            bstack111ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ⪀"): bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⪁"),
            bstack111ll11_opy_ (u"ࠫࡨࡵࡤࡦࠩ⪂"): None
        },
        bstack111ll11_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ⪃"): test.name,
        bstack111ll11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭⪄"): bstack1lll1l11l_opy_.bstack1lll1l1l1l1_opy_(test, hook_name),
        bstack111ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ⪅"): file_path,
        bstack111ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪ⪆"): file_path,
        bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⪇"): bstack111ll11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⪈"),
        bstack111ll11_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩ⪉"): file_path,
        bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⪊"): bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⪋")],
        bstack111ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⪌"): bstack111ll11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ⪍") if bstack1l1llllllll1_opy_ == bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⪎") else bstack111ll11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⪏"),
        bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⪐"): hook_type
    }
    bstack1l111l11111_opy_ = bstack1lll11ll1l1_opy_(_1lll1llll1l_opy_.get(test.nodeid, None))
    if bstack1l111l11111_opy_:
        hook_data[bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ⪑")] = bstack1l111l11111_opy_
    if result:
        hook_data[bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⪒")] = result.outcome
        hook_data[bstack111ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⪓")] = result.duration * 1000
        hook_data[bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⪔")] = bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⪕")]
        if result.failed:
            hook_data[bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⪖")] = TestHubHandler.bstack1ll111l1l1l_opy_(call.excinfo.typename)
            hook_data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⪗")] = TestHubHandler.bstack1ll111lllll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⪘")] = bstack1llll1l11lll_opy_(outcome)
        hook_data[bstack111ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⪙")] = 100
        hook_data[bstack111ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⪚")] = bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⪛")]
        if hook_data[bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⪜")] == bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⪝"):
            hook_data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⪞")] = bstack111ll11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭⪟")  # bstack1l1lllllll1l_opy_
            hook_data[bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⪠")] = [{bstack111ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⪡"): [bstack111ll11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ⪢")]}]
    if bstack1ll1111ll1l1_opy_:
        hook_data[bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⪣")] = bstack1ll1111ll1l1_opy_.result
        hook_data[bstack111ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⪤")] = bstack1lll111l11l_opy_(bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⪥")], bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⪦")])
        hook_data[bstack111ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⪧")] = bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⪨")]
        if hook_data[bstack111ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⪩")] == bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⪪"):
            hook_data[bstack111ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩ⪫")] = TestHubHandler.bstack1ll111l1l1l_opy_(bstack1ll1111ll1l1_opy_.exception_type)
            hook_data[bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⪬")] = [{bstack111ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⪭"): bstack1llll1lll1ll_opy_(bstack1ll1111ll1l1_opy_.exception)}]
    return hook_data
def bstack1l1lllllllll_opy_(test, bstack1lll1lllll1_opy_, bstack11l111l11_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack111ll11_opy_ (u"࠭ࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡥࡷࡧࡱࡸ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠥ࠳ࠠࡼࡿࠪ⪮").format(bstack11l111l11_opy_))
    bstack1llll1l11ll_opy_ = bstack1ll11111l1l1_opy_(test, bstack1lll1lllll1_opy_, result, call, bstack11l111l11_opy_, outcome)
    driver = getattr(test, bstack111ll11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⪯"), None)
    if bstack11l111l11_opy_ == bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⪰") and driver:
        bstack1llll1l11ll_opy_[bstack111ll11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ⪱")] = TestHubHandler.bstack1llll111l1l_opy_(driver)
    if bstack11l111l11_opy_ == bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⪲"):
        bstack11l111l11_opy_ = bstack111ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⪳")
    bstack1lll1l1l1ll_opy_ = {
        bstack111ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⪴"): bstack11l111l11_opy_,
        bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⪵"): bstack1llll1l11ll_opy_
    }
    TestHubHandler.bstack1l1lll11_opy_(bstack1lll1l1l1ll_opy_)
    if bstack11l111l11_opy_ == bstack111ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⪶"):
        threading.current_thread().bstackTestMeta = {bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⪷"): bstack111ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⪸")}
    elif bstack11l111l11_opy_ == bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⪹"):
        threading.current_thread().bstackTestMeta = {bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⪺"): getattr(result, bstack111ll11_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⪻"), bstack111ll11_opy_ (u"࠭ࠧ⪼"))}
def bstack1ll1111l1ll1_opy_(test, bstack1lll1lllll1_opy_, bstack11l111l11_opy_, result=None, call=None, outcome=None, bstack1ll1111ll1l1_opy_=None):
    logger.debug(bstack111ll11_opy_ (u"ࠧࡴࡧࡱࡨࡤ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢ࡫ࡳࡴࡱࠠࡥࡣࡷࡥ࠱ࠦࡥࡷࡧࡱࡸ࡙ࡿࡰࡦࠢ࠰ࠤࢀࢃࠧ⪽").format(bstack11l111l11_opy_))
    hook_data = bstack1ll111111lll_opy_(test, bstack1lll1lllll1_opy_, bstack11l111l11_opy_, result, call, outcome, bstack1ll1111ll1l1_opy_)
    bstack1lll1l1l1ll_opy_ = {
        bstack111ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⪾"): bstack11l111l11_opy_,
        bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ⪿"): hook_data
    }
    TestHubHandler.bstack1l1lll11_opy_(bstack1lll1l1l1ll_opy_)
def bstack1lll11ll1l1_opy_(bstack1lll1lllll1_opy_):
    if not bstack1lll1lllll1_opy_:
        return None
    if bstack1lll1lllll1_opy_.get(bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⫀"), None):
        return getattr(bstack1lll1lllll1_opy_[bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⫁")], bstack111ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ⫂"), None)
    return bstack1lll1lllll1_opy_.get(bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⫃"), None)
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
        places = [bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⫄"), bstack111ll11_opy_ (u"ࠨࡥࡤࡰࡱ࠭⫅"), bstack111ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⫆")]
        logs = []
        for bstack1l1llllll1l1_opy_ in places:
            records = caplog.get_records(bstack1l1llllll1l1_opy_)
            bstack1ll1111l11ll_opy_ = bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⫇") if bstack1l1llllll1l1_opy_ == bstack111ll11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ⫈") else bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⫉")
            bstack1ll1111111l1_opy_ = request.node.nodeid + (bstack111ll11_opy_ (u"࠭ࠧ⫊") if bstack1l1llllll1l1_opy_ == bstack111ll11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ⫋") else bstack111ll11_opy_ (u"ࠨ࠯ࠪ⫌") + bstack1l1llllll1l1_opy_)
            test_uuid = bstack1lll11ll1l1_opy_(_1lll1llll1l_opy_.get(bstack1ll1111111l1_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1lllll1l11l1_opy_(record.message):
                    continue
                logs.append({
                    bstack111ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⫍"): bstack1llll1ll1ll1_opy_(record.created).isoformat() + bstack111ll11_opy_ (u"ࠪ࡞ࠬ⫎"),
                    bstack111ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⫏"): record.levelname,
                    bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⫐"): record.message,
                    bstack1ll1111l11ll_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack111ll11lll_opy_(logs)
    except Exception as err:
        print(bstack111ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪ⫑"), str(err))
def bstack11l111lll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11111lll1_opy_
    bstack1l1l111l11_opy_ = bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ⫒"), None) and bstack111lll1ll1_opy_(
            threading.current_thread(), bstack111ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⫓"), None)
    bstack1llll1l1l1_opy_ = getattr(driver, bstack111ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ⫔"), None) != None and getattr(driver, bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⫕"), None) == True
    if sequence == bstack111ll11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⫖") and driver != None:
      if not bstack11111lll1_opy_ and bstack1l111llll1_opy_() and bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⫗") in CONFIG and CONFIG[bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⫘")] == True and accessibility_scripts.bstack1llllll1lll_opy_(driver_command) and (bstack1llll1l1l1_opy_ or bstack1l1l111l11_opy_) and not bstack1ll11ll1l1_opy_(args):
        try:
          bstack11111lll1_opy_ = True
          logger.debug(bstack111ll11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩ⫙").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭⫚").format(str(err)))
        bstack11111lll1_opy_ = False
    if sequence == bstack111ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⫛"):
        if driver_command == bstack111ll11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ⫝̸"):
            TestHubHandler.bstack111111ll_opy_({
                bstack111ll11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⫝"): response[bstack111ll11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⫞")],
                bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⫟"): store[bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⫠")]
            })
def bstack1ll111l1_opy_():
    global bstack111lllll1l_opy_
    logger_utils.bstack11ll1ll1l_opy_()
    logging.shutdown()
    TestHubHandler.bstack1lll1lll111_opy_()
    for driver in bstack111lllll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l111lll_opy_(*args):
    global bstack111lllll1l_opy_
    TestHubHandler.bstack1lll1lll111_opy_()
    for driver in bstack111lllll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll11lllll_opy_, stage=STAGE.bstack1l1l1ll111_opy_, bstack1ll11l1l1_opy_=SESSION_NAME)
def bstack1llll1l1_opy_(self, *args, **kwargs):
    bstack11111ll1l1_opy_ = bstack1l11l1l1_opy_(self, *args, **kwargs)
    bstack11111l11_opy_ = getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡕࡧࡶࡸࡒ࡫ࡴࡢࠩ⫡"), None)
    if bstack11111l11_opy_ and bstack11111l11_opy_.get(bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⫢"), bstack111ll11_opy_ (u"ࠪࠫ⫣")) == bstack111ll11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⫤"):
        TestHubHandler.send_cbt_info(self)
    return bstack11111ll1l1_opy_
@measure(event_name=EVENTS.bstack11l1l111l1_opy_, stage=STAGE.bstack1l1111l1l_opy_, bstack1ll11l1l1_opy_=SESSION_NAME)
def bstack11lllll111_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.bstack1lllll1lll1_opy_()
    if global_config.get_property(bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⫥")):
        return
    global_config.bstack1l111l1ll1_opy_(bstack111ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⫦"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack1llll1l1l_opy_.format(FRAMEWORK_NAME.split(bstack111ll11_opy_ (u"ࠧ࠮ࠩ⫧"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l111llll1_opy_():
            Service.start = bstack11111ll111_opy_
            Service.stop = bstack11l1111l1l_opy_
            webdriver.Remote.get = bstack1ll1lll1l1_opy_
            webdriver.Remote.__init__ = bstack111l1ll1l_opy_
            if not isinstance(os.getenv(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ⫨")), str):
                return
            WebDriver.quit = bstack1l1l11ll1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1llll1l1_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack111ll11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ⫩")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack111ll11_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⫪")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack1l11l11ll_opy_(bstack111ll11_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ⫫"), bstack1ll1lll1ll_opy_)
    if bstack1llllllll11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack111ll11_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⫬")) and callable(getattr(RemoteConnection, bstack111ll11_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⫭"))):
                RemoteConnection._get_proxy_url = bstack11111l1ll1_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack11111l1ll1_opy_
        except Exception as e:
            logger.error(bstack1lllllllll1_opy_.format(str(e)))
    if bstack111ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⫮") in str(framework_name).lower():
        if not bstack1l111llll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l11l11l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lll1111l_opy_
            Config.getoption = bstack111ll1l11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1111ll1l1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l11l1l1_opy_, stage=STAGE.bstack1l1l1ll111_opy_, bstack1ll11l1l1_opy_=SESSION_NAME)
def bstack1l1l11ll1l_opy_(self):
    global FRAMEWORK_NAME
    global bstack1llll1lll1_opy_
    global bstack11l1lllll_opy_
    try:
        if bstack111ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⫯") in FRAMEWORK_NAME and self.session_id != None and bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭⫰"), bstack111ll11_opy_ (u"ࠪࠫ⫱")) != bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⫲"):
            bstack1llll1l11_opy_ = bstack111ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⫳") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⫴")
            bstack11llllllll_opy_(logger, True)
            if os.environ.get(bstack111ll11_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⫵"), None):
                self.execute_script(
                    bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭⫶") + json.dumps(
                        os.environ.get(bstack111ll11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⫷"))) + bstack111ll11_opy_ (u"ࠪࢁࢂ࠭⫸"))
            if self != None:
                bstack11111lll11_opy_(self, bstack1llll1l11_opy_, bstack111ll11_opy_ (u"ࠫ࠱ࠦࠧ⫹").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l11ll11l_opy_(bstack111111l11l_opy_):
            item = store.get(bstack111ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⫺"), None)
            if item is not None and bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⫻"), None):
                bstack1ll1l1lll1_opy_.bstack1lllllll1ll_opy_(self, bstack11llll1ll_opy_, logger, item)
        threading.current_thread().testStatus = bstack111ll11_opy_ (u"ࠧࠨ⫼")
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ⫽") + str(e))
    bstack11l1lllll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1llllllll_opy_, stage=STAGE.bstack1l1l1ll111_opy_, bstack1ll11l1l1_opy_=SESSION_NAME)
def bstack111l1ll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1lll1_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack1l11l1l1_opy_
    global bstack111lllll1l_opy_
    global bstack1l1111llll_opy_
    global bstack1lllll11lll_opy_
    global bstack11llll1ll_opy_
    CONFIG[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⫾")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack11llll11_opy_(bstack1l1111llll_opy_, CONFIG)
    logger.debug(bstack111ll11l1l_opy_.format(command_executor))
    proxy = bstack11l1l11l1l_opy_(CONFIG, proxy)
    bstack1l1ll11l1l_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l1ll11l1l_opy_ = int(os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⫿")))
    except:
        bstack1l1ll11l1l_opy_ = 0
    bstack1ll1111111_opy_ = get_caps(CONFIG, bstack1l1ll11l1l_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll1111111_opy_)))
    bstack11llll1ll_opy_ = CONFIG.get(bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⬀"))[bstack1l1ll11l1l_opy_]
    if bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⬁") in CONFIG and CONFIG[bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⬂")]:
        update_caps_for_local(bstack1ll1111111_opy_, bstack1lllll11lll_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack1l1ll11l1l_opy_) and a11y.is_platform_supported(bstack1ll1111111_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l11ll11l_opy_(bstack111111l11l_opy_):
            a11y.set_capabilities(bstack1ll1111111_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll11111ll_opy_ = bstack1111llll_opy_(desired_capabilities)
        bstack1ll11111ll_opy_[bstack111ll11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ⬃")] = bstack1l1l1l11ll_opy_(CONFIG)
        bstack11111lll_opy_ = get_caps(bstack1ll11111ll_opy_)
        if bstack11111lll_opy_:
            bstack1ll1111111_opy_ = update(bstack11111lll_opy_, bstack1ll1111111_opy_)
        desired_capabilities = None
    if options:
        bstack1l111ll1ll_opy_(options, bstack1ll1111111_opy_)
    if not options:
        options = bstack11l1111lll_opy_(bstack1ll1111111_opy_)
    if proxy and bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ⬄")):
        options.proxy(proxy)
    if options and bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ⬅")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11lll1l11_opy_() < version.parse(bstack111ll11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⬆")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1111111_opy_)
    logger.info(bstack11l11ll11_opy_)
    bstack1lll1l1ll1_opy_.end(EVENTS.bstack11l1l111l1_opy_.value, EVENTS.bstack11l1l111l1_opy_.value + bstack111ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ⬇"),
                               EVENTS.bstack11l1l111l1_opy_.value + bstack111ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ⬈"), True, None)
    try:
        if bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⬉")):
            bstack1l11l1l1_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⬊")):
            bstack1l11l1l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨ⬋")):
            bstack1l11l1l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack1l11l1l1_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1ll111llll_opy_:
        logger.error(bstack11l1l11111_opy_.format(bstack111ll11_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨ⬌"), str(bstack1ll111llll_opy_)))
        raise bstack1ll111llll_opy_
    try:
        bstack1l1l1l1lll_opy_ = bstack111ll11_opy_ (u"ࠪࠫ⬍")
        if bstack11lll1l11_opy_() >= version.parse(bstack111ll11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ⬎")):
            bstack1l1l1l1lll_opy_ = self.caps.get(bstack111ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ⬏"))
        else:
            bstack1l1l1l1lll_opy_ = self.capabilities.get(bstack111ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⬐"))
        if bstack1l1l1l1lll_opy_:
            bstack1111llllll_opy_(bstack1l1l1l1lll_opy_)
            if bstack11lll1l11_opy_() <= version.parse(bstack111ll11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ⬑")):
                self.command_executor._url = bstack111ll11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ⬒") + bstack1l1111llll_opy_ + bstack111ll11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ⬓")
            else:
                self.command_executor._url = bstack111ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ⬔") + bstack1l1l1l1lll_opy_ + bstack111ll11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ⬕")
            logger.debug(bstack11l1l1l1l1_opy_.format(bstack1l1l1l1lll_opy_))
        else:
            logger.debug(bstack1l1111111l_opy_.format(bstack111ll11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ⬖")))
    except Exception as e:
        logger.debug(bstack1l1111111l_opy_.format(e))
    bstack1llll1lll1_opy_ = self.session_id
    if bstack111ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⬗") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⬘"), None)
        if item:
            bstack1ll11111ll11_opy_ = getattr(item, bstack111ll11_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭⬙"), False)
            if not getattr(item, bstack111ll11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⬚"), None) and bstack1ll11111ll11_opy_:
                setattr(store[bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⬛")], bstack111ll11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⬜"), self)
        bstack11111l11_opy_ = getattr(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭⬝"), None)
        if bstack11111l11_opy_ and bstack11111l11_opy_.get(bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⬞"), bstack111ll11_opy_ (u"ࠧࠨ⬟")) == bstack111ll11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⬠"):
            TestHubHandler.send_cbt_info(self)
    bstack111lllll1l_opy_.append(self)
    if bstack111ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⬡") in CONFIG and bstack111ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⬢") in CONFIG[bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⬣")][bstack1l1ll11l1l_opy_]:
        SESSION_NAME = CONFIG[bstack111ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⬤")][bstack1l1ll11l1l_opy_][bstack111ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⬥")]
    logger.debug(bstack1l1llll111_opy_.format(bstack1llll1lll1_opy_))
@measure(event_name=EVENTS.bstack11l1l11l11_opy_, stage=STAGE.bstack1l1l1ll111_opy_, bstack1ll11l1l1_opy_=SESSION_NAME)
def bstack1ll1lll1l1_opy_(self, url):
    global bstack1111lll1l_opy_
    global CONFIG
    try:
        bstack111l1ll111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll1l1l11_opy_.format(str(err)))
    try:
        bstack1111lll1l_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack1111111l1_opy_):
                bstack111l1ll111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll1l1l11_opy_.format(str(err)))
        raise e
def bstack1111l1ll1_opy_(item, when):
    global bstack11l11ll1l_opy_
    try:
        bstack11l11ll1l_opy_(item, when)
    except Exception as e:
        pass
def bstack1111ll1l1_opy_(item, call, rep):
    global bstack11lll1llll_opy_
    global bstack111lllll1l_opy_
    name = bstack111ll11_opy_ (u"ࠧࠨ⬦")
    try:
        if rep.when == bstack111ll11_opy_ (u"ࠨࡥࡤࡰࡱ࠭⬧"):
            bstack1llll1lll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack111ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ⬨"))
            try:
                if (str(skipSessionName).lower() != bstack111ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ⬩")):
                    name = str(rep.nodeid)
                    bstack1llllllllll_opy_ = bstack1lll1l1l11_opy_(bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⬪"), name, bstack111ll11_opy_ (u"ࠬ࠭⬫"), bstack111ll11_opy_ (u"࠭ࠧ⬬"), bstack111ll11_opy_ (u"ࠧࠨ⬭"), bstack111ll11_opy_ (u"ࠨࠩ⬮"))
                    os.environ[bstack111ll11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⬯")] = name
                    for driver in bstack111lllll1l_opy_:
                        if bstack1llll1lll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1llllllllll_opy_)
            except Exception as e:
                logger.debug(bstack111ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⬰").format(str(e)))
            try:
                bstack1l111l11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111ll11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⬱"):
                    status = bstack111ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⬲") if rep.outcome.lower() == bstack111ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⬳") else bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⬴")
                    reason = bstack111ll11_opy_ (u"ࠨࠩ⬵")
                    if status == bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ⬶"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111ll11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ⬷") if status == bstack111ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⬸") else bstack111ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⬹")
                    data = name + bstack111ll11_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ⬺") if status == bstack111ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⬻") else name + bstack111ll11_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫ⬼") + reason
                    bstack1llll1l111_opy_ = bstack1lll1l1l11_opy_(bstack111ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ⬽"), bstack111ll11_opy_ (u"ࠪࠫ⬾"), bstack111ll11_opy_ (u"ࠫࠬ⬿"), bstack111ll11_opy_ (u"ࠬ࠭⭀"), level, data)
                    for driver in bstack111lllll1l_opy_:
                        if bstack1llll1lll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1l111_opy_)
            except Exception as e:
                logger.debug(bstack111ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪ⭁").format(str(e)))
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫ⭂").format(str(e)))
    bstack11lll1llll_opy_(item, call, rep)
notset = Notset()
def bstack111ll1l11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11lll111l1_opy_
    if str(name).lower() == bstack111ll11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ⭃"):
        return bstack111ll11_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ⭄")
    else:
        return bstack11lll111l1_opy_(self, name, default, skip)
def bstack11111l1ll1_opy_(self):
    global CONFIG
    global bstack11l1llllll_opy_
    try:
        proxy = bstack1ll11111l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111ll11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ⭅")):
                proxies = bstack11l1111l1_opy_(proxy, bstack11llll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l111111ll_opy_ = proxies.popitem()
                    if bstack111ll11_opy_ (u"ࠦ࠿࠵࠯ࠣ⭆") in bstack1l111111ll_opy_:
                        return bstack1l111111ll_opy_
                    else:
                        return bstack111ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ⭇") + bstack1l111111ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ⭈").format(str(e)))
    return bstack11l1llllll_opy_(self)
def bstack1llllllll11_opy_():
    return (bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⭉") in CONFIG or bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⭊") in CONFIG) and bstack11l11lllll_opy_() and bstack11lll1l11_opy_() >= version.parse(
        bstack11l1111l11_opy_)
def bstack1l1lll1111_opy_(self,
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
    CONFIG[bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ⭋")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack1l1ll11l1l_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack1l1ll11l1l_opy_ = int(os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⭌")))
    except:
        bstack1l1ll11l1l_opy_ = 0
    CONFIG[bstack111ll11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ⭍")] = True
    bstack1ll1111111_opy_ = get_caps(CONFIG, bstack1l1ll11l1l_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack1ll1111111_opy_)))
    if CONFIG.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ⭎")):
        update_caps_for_local(bstack1ll1111111_opy_, bstack1lllll11lll_opy_)
    if bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⭏") in CONFIG and bstack111ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⭐") in CONFIG[bstack111ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ⭑")][bstack1l1ll11l1l_opy_]:
        SESSION_NAME = CONFIG[bstack111ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⭒")][bstack1l1ll11l1l_opy_][bstack111ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ⭓")]
    import urllib
    import json
    if bstack111ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⭔") in CONFIG and str(CONFIG[bstack111ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⭕")]).lower() != bstack111ll11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⭖"):
        bstack1111lll1ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack1111lll1ll_opy_ + urllib.parse.quote(json.dumps(bstack1ll1111111_opy_))
    else:
        cdpUrl = bstack111ll11_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ⭗") + urllib.parse.quote(json.dumps(bstack1ll1111111_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l1l11l1l1l_opy_
        if not bstack1l111llll1_opy_():
            global bstack11llll111_opy_
            if not bstack11llll111_opy_:
                from bstack_utils.helper import bstack1ll1l1l1_opy_, bstack1lllll11l111_opy_
                bstack11llll111_opy_ = bstack1ll1l1l1_opy_()
                bstack1lllll11l111_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l1l11l1l1l_opy_
            return
        BrowserType.launch = bstack1l1lll1111_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1ll1111l1l1l_opy_():
    global CONFIG
    global bstack1l1l11l1l1_opy_
    global bstack1l1111llll_opy_
    global bstack1lllll11lll_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack11l11l1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ⭘")))
    bstack1l1l11l1l1_opy_ = eval(os.environ.get(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ⭙")))
    bstack1l1111llll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪ⭚"))
    bstack1ll1ll1l_opy_(CONFIG, bstack1l1l11l1l1_opy_)
    bstack11l11l1ll_opy_ = logger_utils.configure_logger(CONFIG, bstack11l11l1ll_opy_)
    if cli.bstack11l1l1l11_opy_():
        bstack1ll1l1l111_opy_.invoke(Events.CONNECT, bstack1ll1l1l1ll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⭛"), bstack111ll11_opy_ (u"ࠬ࠶ࠧ⭜")))
        cli.bstack1l1l11111l_opy_(cli_context.platform_index)
        cli.bstack1l1l11l11ll_opy_(bstack11llll11_opy_(bstack1l1111llll_opy_, CONFIG), cli_context.platform_index, bstack11l1111lll_opy_)
        cli.bstack111lll1lll_opy_()
        logger.debug(bstack111ll11_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⭝") + str(cli_context.platform_index) + bstack111ll11_opy_ (u"ࠢࠣ⭞"))
        return # skip all existing operations
    global bstack1l11l1l1_opy_
    global bstack11l1lllll_opy_
    global bstack111l1l11ll_opy_
    global bstack1ll11ll11l_opy_
    global bstack11ll1l111_opy_
    global bstack1l1l11ll11_opy_
    global bstack1l1ll1lll1_opy_
    global bstack1111lll1l_opy_
    global bstack11l1llllll_opy_
    global bstack11lll111l1_opy_
    global bstack11l11ll1l_opy_
    global bstack11lll1llll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11l1l1_opy_ = webdriver.Remote.__init__
        bstack11l1lllll_opy_ = WebDriver.quit
        bstack1l1ll1lll1_opy_ = WebDriver.close
        bstack1111lll1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack111ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⭟") in CONFIG or bstack111ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⭠") in CONFIG) and bstack11l11lllll_opy_():
        if bstack11lll1l11_opy_() < version.parse(bstack11l1111l11_opy_):
            logger.error(bstack111ll11ll_opy_.format(bstack11lll1l11_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack111ll11_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⭡")) and callable(getattr(RemoteConnection, bstack111ll11_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⭢"))):
                    bstack11l1llllll_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack11l1llllll_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1lllllllll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11lll111l1_opy_ = Config.getoption
        from _pytest import runner
        bstack11l11ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack111ll11_opy_ (u"ࠧࠫࡳ࠻ࠢࠨࡷࠧ⭣"), bstack1lll1lllll_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack11lll1llll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ⭤"))
    bstack1lllll11lll_opy_ = CONFIG.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ⭥"), {}).get(bstack111ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⭦"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack11lllll111_opy_(bstack1llllll11l1_opy_)
if (bstack1llllll111ll_opy_()):
    bstack1ll1111l1l1l_opy_()
@error_handler(class_method=False)
def bstack1ll11111l11l_opy_(hook_name, event, bstack11l111111ll_opy_=None):
    if hook_name not in [bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ⭧"), bstack111ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ⭨"), bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⭩"), bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⭪"), bstack111ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⭫"), bstack111ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⭬"), bstack111ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⭭"), bstack111ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ⭮")]:
        return
    node = store[bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⭯")]
    if hook_name in [bstack111ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⭰"), bstack111ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⭱")]:
        node = store[bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ⭲")]
    elif hook_name in [bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⭳"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⭴")]:
        node = store[bstack111ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⭵")]
    hook_type = bstack1ll1l111lll1_opy_(hook_name)
    if event == bstack111ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ⭶"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lll1l11ll1_opy_ = {
            bstack111ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩ⭷"): uuid,
            bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⭸"): bstack1llllll1l11_opy_(),
            bstack111ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⭹"): bstack111ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⭺"),
            bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⭻"): hook_type,
            bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⭼"): hook_name
        }
        store[bstack111ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⭽")].append(uuid)
        bstack1ll1111l1lll_opy_ = node.nodeid
        if hook_type == bstack111ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⭾"):
            if not _1lll1llll1l_opy_.get(bstack1ll1111l1lll_opy_, None):
                _1lll1llll1l_opy_[bstack1ll1111l1lll_opy_] = {bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⭿"): []}
            _1lll1llll1l_opy_[bstack1ll1111l1lll_opy_][bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⮀")].append(bstack1lll1l11ll1_opy_[bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⮁")])
        _1lll1llll1l_opy_[bstack1ll1111l1lll_opy_ + bstack111ll11_opy_ (u"ࠨ࠯ࠪ⮂") + hook_name] = bstack1lll1l11ll1_opy_
        bstack1ll1111l1ll1_opy_(node, bstack1lll1l11ll1_opy_, bstack111ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⮃"))
    elif event == bstack111ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⮄"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l111111ll_opy_)
            return
        bstack1llll1l1l11_opy_ = node.nodeid + bstack111ll11_opy_ (u"ࠫ࠲࠭⮅") + hook_name
        _1lll1llll1l_opy_[bstack1llll1l1l11_opy_][bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⮆")] = bstack1llllll1l11_opy_()
        bstack1ll11111l111_opy_(_1lll1llll1l_opy_[bstack1llll1l1l11_opy_][bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⮇")])
        bstack1ll1111l1ll1_opy_(node, _1lll1llll1l_opy_[bstack1llll1l1l11_opy_], bstack111ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⮈"), bstack1ll1111ll1l1_opy_=bstack11l111111ll_opy_)
def bstack1l1lllllll11_opy_():
    global bstack1l1llllllll1_opy_
    if bstack1ll1l1llll_opy_():
        bstack1l1llllllll1_opy_ = bstack111ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ⮉")
    else:
        bstack1l1llllllll1_opy_ = bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⮊")
@TestHubHandler.bstack1ll111ll1l11_opy_
def bstack1ll11111l1ll_opy_():
    bstack1l1lllllll11_opy_()
    if cli.is_running():
        try:
            bstack1lll1lll1111_opy_(bstack1ll11111l11l_opy_)
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ⮋").format(e))
        return
    if bstack11l11lllll_opy_():
        global_config = Config.bstack1lllll1lll1_opy_()
        bstack111ll11_opy_ (u"ࠫࠬ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡳࡴࡵࠦ࠽ࠡ࠳࠯ࠤࡲࡵࡤࡠࡧࡻࡩࡨࡻࡴࡦࠢࡪࡩࡹࡹࠠࡶࡵࡨࡨࠥ࡬࡯ࡳࠢࡤ࠵࠶ࡿࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠯ࡺࡶࡦࡶࡰࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡴࡸࡲࠥࡨࡥࡤࡣࡸࡷࡪࠦࡩࡵࠢ࡬ࡷࠥࡶࡡࡵࡥ࡫ࡩࡩࠦࡩ࡯ࠢࡤࠤࡩ࡯ࡦࡧࡧࡵࡩࡳࡺࠠࡱࡴࡲࡧࡪࡹࡳࠡ࡫ࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡺࡹࠠࡸࡧࠣࡲࡪ࡫ࡤࠡࡶࡲࠤࡺࡹࡥࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡓࡥࡹࡩࡨࠩࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡬ࡦࡴࡤ࡭ࡧࡵ࠭ࠥ࡬࡯ࡳࠢࡳࡴࡵࠦ࠾ࠡ࠳ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠬ࠭ࠧ⮌")
        if global_config.get_property(bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩ⮍")):
            if CONFIG.get(bstack111ll11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭⮎")) is not None and int(CONFIG[bstack111ll11_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⮏")]) > 1:
                bstack1ll11l1ll1_opy_(bstack11l111lll1_opy_)
            return
        bstack1ll11l1ll1_opy_(bstack11l111lll1_opy_)
    try:
        bstack1lll1lll1111_opy_(bstack1ll11111l11l_opy_)
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ⮐").format(e))
bstack1ll11111l1ll_opy_()