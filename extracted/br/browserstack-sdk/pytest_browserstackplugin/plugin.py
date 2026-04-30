# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack11l11lll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (get_caps, bstack1111111111_opy_, update, bstack1l111lll1_opy_,
                                       bstack11111ll1ll_opy_, bstack11llll111_opy_, bstack11lll11lll_opy_, bstack1ll11l111_opy_,
                                       bstack1l11ll1l_opy_, bstack111111l11l_opy_, bstack1ll1l1ll_opy_,
                                       bstack1lll1l11_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11llll1l_opy_)
from browserstack_sdk.bstack111lll1l_opy_ import bstack1l1l1ll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import logger_utils
from bstack_utils.capture import bstack1llll111lll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11l1l1111_opy_, bstack111l11l11_opy_, bstack1111llll1_opy_, \
    bstack1l1ll1ll1_opy_
from bstack_utils.helper import bstack11l11l11_opy_, bstack1llll1ll1l1l_opy_, bstack1lll11ll1ll_opy_, bstack11l1l1l11_opy_, bstack1lllllll11l_opy_, bstack1l111l1ll_opy_, \
    bstack1lllll1l1l11_opy_, \
    bstack1lllll11ll11_opy_, bstack111111lll_opy_, bstack1l11111l1l_opy_, bstack1lllll1111l1_opy_, bstack11111l111l_opy_, Notset, \
    bstack1l11l1l111_opy_, bstack1ll1l1ll1ll_opy_, bstack1lllll1lll11_opy_, Result, bstack1lllll1l11l1_opy_, bstack1llll1ll1l11_opy_, error_handler, \
    bstack11llll1l11_opy_, bstack1l1l1l11_opy_, bstack1ll111lll_opy_, bstack1llll1l1ll1l_opy_
from bstack_utils.bstack1lll1ll1l11l_opy_ import bstack1lll1ll1l111_opy_
from bstack_utils.messages import bstack1l1l111l1_opy_, bstack1lll11l1l_opy_, bstack111ll1l1l1_opy_, bstack11l1l1l11l_opy_, bstack1l1l111l_opy_, \
    bstack1l1l1lllll_opy_, bstack111111111l_opy_, CONFIG_FILE_CONTENT, bstack11111l1ll1_opy_, bstack1ll1l1ll11_opy_, \
    bstack11llllll11_opy_, bstack111lll11l1_opy_, bstack11ll11l1_opy_
from bstack_utils.proxy import bstack11l1ll11_opy_, bstack111ll111ll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack1ll1l1111lll_opy_, bstack1ll1l111ll11_opy_, bstack1ll1l1111l11_opy_, bstack1ll1l1111l1l_opy_, \
    bstack1ll1l111l111_opy_, bstack1ll1l11111l1_opy_, bstack1ll1l111ll1l_opy_, bstack1l111llll_opy_, bstack1ll1l11111ll_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack11lll1l11_opy_
from bstack_utils.bstack1l1111ll11_opy_ import bstack1l11111l11_opy_, bstack11l1l1ll1l_opy_, update_caps_for_local, \
    bstack11ll1l1111_opy_, bstack1l1llll1l1_opy_
from bstack_utils.bstack1llll1l1ll1_opy_ import bstack1llll1l11l1_opy_
from bstack_utils.bstack11l1l111l_opy_ import bstack1l1lll1l1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack11lll1lll_opy_ import bstack1lll1111ll_opy_
from browserstack_sdk.__init__ import get_turboscale_playwright_url
from browserstack_sdk.sdk_cli.bstack11l111l11_opy_ import bstack1l111l111l_opy_
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111lll1_opy_, Events, bstack111lll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1ll1lll111l_opy_, TestFrameworkState, TestHookState
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111lll1_opy_, Events, bstack111lll1lll_opy_
bstack11111l11_opy_ = None
bstack1llllllll_opy_ = None
bstack111l1ll1_opy_ = None
bstack1ll11ll1_opy_ = None
bstack11111lll_opy_ = None
bstack1ll1llll1_opy_ = None
bstack1lllll11_opy_ = None
bstack11lll11111_opy_ = None
bstack1lllllll1_opy_ = None
bstack1llllll1l_opy_ = None
bstack1l1ll111_opy_ = None
bstack1l1ll111l1_opy_ = None
bstack1llllll11l1_opy_ = None
FRAMEWORK_NAME = bstack1l1111l_opy_ (u"ࠫࠬ⤤")
CONFIG = {}
bstack1111llll11_opy_ = False
bstack1ll1111l1_opy_ = bstack1l1111l_opy_ (u"ࠬ࠭⤥")
bstack11ll1ll11_opy_ = bstack1l1111l_opy_ (u"࠭ࠧ⤦")
PARALLELISE_VANILLA_PYTHON = False
bstack111l11111l_opy_ = []
bstack11ll1lll1_opy_ = bstack11l1l1111_opy_
bstack1ll11111lll1_opy_ = bstack1l1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⤧")
bstack11l111l1l1_opy_ = {}
SESSION_NAME = None
bstack1l11l11111_opy_ = False
logger = logger_utils.get_logger(__name__, bstack11ll1lll1_opy_)
store = {
    bstack1l1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⤨"): []
}
bstack1ll1111111ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lll1l1l11l_opy_ = {}
current_test_uuid = None
cli_context = bstack1ll1lll111l_opy_(
    test_framework_name=bstack1l1l11llll_opy_[bstack1l1111l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭⤩")] if bstack11111l111l_opy_() else bstack1l1l11llll_opy_[bstack1l1111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࠪ⤪")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def playwright_set_session_name(page, bstack1l1l111l11_opy_):
    try:
        page.evaluate(bstack1l1111l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ⤫"),
                      bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩ⤬") + json.dumps(
                          bstack1l1l111l11_opy_) + bstack1l1111l_opy_ (u"ࠨࡽࡾࠤ⤭"))
    except Exception as e:
        print(bstack1l1111l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ⤮"), e)
def playwright_annotate(page, message, level):
    try:
        page.evaluate(bstack1l1111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ⤯"), bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ⤰") + json.dumps(
            message) + bstack1l1111l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭⤱") + json.dumps(level) + bstack1l1111l_opy_ (u"ࠫࢂࢃࠧ⤲"))
    except Exception as e:
        print(bstack1l1111l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ⤳"), e)
def _1l1llllll1l1_opy_():
    bstack1l1111l_opy_ (u"ࠨ࡙ࠢࠣࡤࡰࡰࠦࡃࡘࡆࠣࡹࡵࡽࡡࡳࡦࠣࡰࡴࡵ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯࠲ࠧࠨࠢ⤴")
    bstack1l1lllll1lll_opy_ = os.getcwd()
    while True:
        for name in (bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ⤵"), bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺࡣࡰࡰࠬ⤶")):
            candidate = os.path.join(bstack1l1lllll1lll_opy_, name)
            if os.path.exists(candidate):
                return candidate
        parent = os.path.dirname(bstack1l1lllll1lll_opy_)
        if parent == bstack1l1lllll1lll_opy_:
            break
        bstack1l1lllll1lll_opy_ = parent
    return None
def _1ll1111l11ll_opy_():
    bstack1l1111l_opy_ (u"ࠤࠥࠦࡉ࡫ࡴࡦࡥࡷࠤ࡮࡬ࠠࡱࡻࡷࡩࡸࡺࠠࡸࡣࡶࠤࡱࡧࡵ࡯ࡥ࡫ࡩࡩࠦࡢࡺࠢࡤࡲࠥࡏࡄࡆࠢࡵࡹࡳࡴࡥࡳ࠰ࠍࠤࠥࠦࠠࡖࡵࡨࡷࠥࡹࡴࡢࡤ࡯ࡩ࠱ࠦ࡬ࡰࡰࡪ࠱ࡱ࡯ࡶࡦࡦࠣࡩࡳࡼࠠࡷࡣࡵࡷࠥࡹࡥࡵࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡧࡦࡲ࡬ࡺࠢࡥࡽࠥࡏࡄࡆࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࡔ࡞ࡉࡈࡂࡔࡐࡣࡍࡕࡓࡕࡇࡇࠤࠥࠦࠠ⠕ࠢࡍࡩࡹࡈࡲࡢ࡫ࡱࡷࠥࡖࡹࡄࡪࡤࡶࡲࠦࠨࡿ࠴࠳࠵࠸࠱ࠩࠋࠢࠣࠤࠥࠦࠠࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠣࠤ⠙ࠦࡊࡦࡶࡅࡶࡦ࡯࡮ࡴࠢࡌࡈࡊࡹࠠࡷ࡫ࡤࠤ࡙࡫ࡡ࡮ࡅ࡬ࡸࡾࠦࡰࡳࡱࡷࡳࡨࡵ࡬ࠡࠪ࠴࠴࠰ࠦࡹࡦࡣࡵࡷ࠮ࠐࠠࠡࠢࠣࠦࠧࠨ⤷")
    return os.environ.get(bstack1l1111l_opy_ (u"ࠪࡔ࡞ࡉࡈࡂࡔࡐࡣࡍࡕࡓࡕࡇࡇࠫ⤸")) == bstack1l1111l_opy_ (u"ࠫ࠶࠭⤹") or \
           bool(os.environ.get(bstack1l1111l_opy_ (u"࡚ࠬࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠨ⤺")))
def pytest_configure(config):
    global bstack1ll1111l1_opy_
    global CONFIG
    global bstack1111llll11_opy_
    if not os.environ.get(bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠪ⤻")) and _1ll1111l11ll_opy_():
        _1ll1111l1l1l_opy_ = _1l1llllll1l1_opy_()
        if _1ll1111l1l1l_opy_:
            try:
                from browserstack_sdk import bstack11ll1111ll_opy_
                if bstack11ll1111ll_opy_(_1ll1111l1l1l_opy_):
                    CONFIG = json.loads(os.environ.get(bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭⤼"), bstack1l1111l_opy_ (u"ࠨࡽࢀࠫ⤽")))
                    bstack1ll1111l1_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ⤾"), bstack1l1111l_opy_ (u"ࠪࠫ⤿"))
                    bstack1111llll11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ⥀"), bstack1l1111l_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫ⥁")).lower() == bstack1l1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ⥂")
            except Exception as e:
                logger.error(bstack1l1111l_opy_ (u"ࠢࡑ࡮ࡸ࡫࡮ࡴࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢ⥃").format(e))
    global_config = Config.bstack111111l1ll_opy_()
    config.args = bstack1l1lll1l1_opy_.bstack1ll1111ll1l1_opy_(config.args)
    global_config.bstack11l1l1111l_opy_(bstack1ll111lll_opy_(config.getoption(bstack1l1111l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ⥄"))))
    try:
        logger_utils.bstack1lll1l1ll11l_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111111lll1_opy_.invoke(Events.CONNECT, bstack111lll1lll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⥅"), bstack1l1111l_opy_ (u"ࠪ࠴ࠬ⥆")))
        config = json.loads(os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ⥇"), bstack1l1111l_opy_ (u"ࠧࢁࡽࠣ⥈")))
        cli.bstack1l1l11l11ll_opy_(bstack1l11111l1l_opy_(bstack1ll1111l1_opy_, CONFIG), cli_context.platform_index, bstack1l111lll1_opy_)
    if cli.bstack1l1l11l111_opy_(bstack1l111l111l_opy_):
        cli.bstack11ll111lll_opy_()
        logger.debug(bstack1l1111l_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧ⥉") + str(cli_context.platform_index) + bstack1l1111l_opy_ (u"ࠢࠣ⥊"))
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_ALL, TestHookState.PRE, config)
def pytest_unconfigure(config):
    bstack1l1111l_opy_ (u"ࠣࠤࠥࡖࡺࡴࠠࡔࡆࡎࠤࡨࡲࡥࡢࡰࡸࡴࠥࡽࡨࡪ࡮ࡨࠤࡵࡿࡴࡦࡵࡷࠤ࠭ࡧ࡮ࡥࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠬࠤ࡮ࡹࠠࡴࡶ࡬ࡰࡱࠦࡡ࡭࡫ࡹࡩ࠳ࠐࠠࠡࠢࠣࡍࡳࠦࡰ࡭ࡷࡪ࡭ࡳࠦ࡭ࡰࡦࡨ࠰ࠥࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡪࡶࡢ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡫࡯ࡲࡦࡵࠣࡥࡹࠦࡡࡵࡧࡻ࡭ࡹࠦࡢࡶࡶࠣࡦࡾࠦࡴࡩࡧࡱࠎࠥࠦࠠࠡࡲࡼࡸࡪࡹࡴࠡࡪࡤࡷࠥࡺ࡯ࡳࡰࠣࡨࡴࡽ࡮ࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠲ࠥࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡩࡵࠢ࡫ࡩࡷ࡫ࠠࡦࡰࡶࡹࡷ࡫ࡳࠋࠢࠣࠤࠥࡺࡨࡦࠢࡥࡹ࡮ࡲࡤࠡ࡮࡬ࡲࡰࠦࡡ࡯ࡦࠣࡗࡉࡑࠠࡳࡷࡱࠤࡪࡴࡤࡦࡦࠣࡱࡪࡹࡳࡢࡩࡨࡷࠥࡸࡥࡢࡥ࡫ࠤࡹ࡮ࡥࠡࡥࡲࡲࡸࡵ࡬ࡦ࠰ࠥࠦࠧ⥋")
    if os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡇࡉࡤࡖࡌࡖࡉࡌࡒࡤࡓࡏࡅࡇࠪ⥌")) and cli.is_running():
        from browserstack_sdk import bstack1l11l11l_opy_
        bstack1l11l11l_opy_()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1111l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣ⥍"), None)
    if cli.is_running() and when == bstack1l1111l_opy_ (u"ࠦࡨࡧ࡬࡭ࠤ⥎"):
        cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.PRE, item, call)
    outcome = yield
    if when == bstack1l1111l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ⥏"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1111l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⥐")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࠨ⥑"), bstack1l1111l_opy_ (u"ࠣࡽࢀࠦ⥒")))
            if bstack1lll1111ll_opy_.bstack1111ll11l1_opy_(config):
                bstack1ll1l1ll1ll1_opy_ = bstack1lll1111ll_opy_.bstack1lll1llll1_opy_(config)
                if item.execution_count > bstack1ll1l1ll1ll1_opy_:
                    print(bstack1l1111l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡲࡦࡶࡵ࡭ࡪࡹ࠺ࠡࠩ⥓"), report.nodeid, os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⥔")))
                    bstack1lll1111ll_opy_.bstack1lll11l1l1ll_opy_(report.nodeid)
            else:
                print(bstack1l1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࠫ⥕"), report.nodeid, os.environ.get(bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⥖")))
                bstack1lll1111ll_opy_.bstack1lll11l1l1ll_opy_(report.nodeid)
        else:
            print(bstack1l1111l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡵࡧࡳࡴࡧࡧ࠾ࠥ࠭⥗"), report.nodeid, os.environ.get(bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⥘")))
    if cli.is_running():
        if when == bstack1l1111l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⥙"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.POST, item, call, outcome)
        elif when == bstack1l1111l_opy_ (u"ࠤࡦࡥࡱࡲࠢ⥚"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.LOG_REPORT, TestHookState.POST, item, call, outcome)
        elif when == bstack1l1111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ⥛"):
            cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l1111l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⥜"))
    plugins = item.config.getoption(bstack1l1111l_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨ⥝"))
    report = outcome.get_result()
    os.environ[bstack1l1111l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⥞")] = report.nodeid
    bstack1ll11111l111_opy_(item, call, report)
    if bstack1l1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧ⥟") not in plugins or bstack11111l111l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1111l_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤ⥠"), None)
    page = getattr(item, bstack1l1111l_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣ⥡"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1ll11111llll_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1ll111111l1l_opy_(item, report, summary, skipSessionName)
def bstack1ll11111llll_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⥢") and report.skipped:
        bstack1ll1l11111ll_opy_(report)
    if report.when in [bstack1l1111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ⥣"), bstack1l1111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ⥤")]:
        return
    if not bstack1lllllll11l_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ⥥")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬ⥦") + json.dumps(
                    report.nodeid) + bstack1l1111l_opy_ (u"ࠨࡿࢀࠫ⥧"))
        os.environ[bstack1l1111l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ⥨")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩ࠿ࠦࡻ࠱ࡿࠥ⥩").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1111l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⥪")))
    bstack1l1ll1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠧࠨ⥫")
    bstack1ll1l11111ll_opy_(report)
    if not passed:
        try:
            bstack1l1ll1l1ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1111l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⥬").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll1l1ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1111l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ⥭")))
        bstack1l1ll1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠣࠤ⥮")
        if not passed:
            try:
                bstack1l1ll1l1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1111l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤ⥯").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1ll1l1ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧ⥰")
                    + json.dumps(bstack1l1111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠥࠧ⥱"))
                    + bstack1l1111l_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣ⥲")
                )
            else:
                item._driver.execute_script(
                    bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⥳")
                    + json.dumps(str(bstack1l1ll1l1ll_opy_))
                    + bstack1l1111l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥ⥴")
                )
        except Exception as e:
            summary.append(bstack1l1111l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥ࠻ࠢࡾ࠴ࢂࠨ⥵").format(e))
def bstack1ll1111l111l_opy_(test_name, error_message):
    try:
        bstack1l1lllll1l1l_opy_ = []
        bstack11l1lllll1_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⥶"), bstack1l1111l_opy_ (u"ࠪ࠴ࠬ⥷"))
        bstack1lllll1ll1l_opy_ = {bstack1l1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⥸"): test_name, bstack1l1111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⥹"): error_message, bstack1l1111l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⥺"): bstack11l1lllll1_opy_}
        bstack1l1lllllll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ⥻"))
        if os.path.exists(bstack1l1lllllll1l_opy_):
            with open(bstack1l1lllllll1l_opy_) as f:
                bstack1l1lllll1l1l_opy_ = json.load(f)
        bstack1l1lllll1l1l_opy_.append(bstack1lllll1ll1l_opy_)
        with open(bstack1l1lllllll1l_opy_, bstack1l1111l_opy_ (u"ࠨࡹࠪ⥼")) as f:
            json.dump(bstack1l1lllll1l1l_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵ࡫ࡲࡴ࡫ࡶࡸ࡮ࡴࡧࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡹࡵࡧࡶࡸࠥ࡫ࡲࡳࡱࡵࡷ࠿ࠦࠧ⥽") + str(e))
def bstack1ll111111l1l_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1111l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ⥾"), bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ⥿")]:
        return
    if (str(skipSessionName).lower() != bstack1l1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪ⦀")):
        playwright_set_session_name(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1111l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ⦁")))
    bstack1l1ll1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠢࠣ⦂")
    bstack1ll1l11111ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1ll1l1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1111l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣ⦃").format(e)
                )
        try:
            if passed:
                bstack1l1llll1l1_opy_(getattr(item, bstack1l1111l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ⦄"), None), bstack1l1111l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ⦅"))
            else:
                error_message = bstack1l1111l_opy_ (u"ࠫࠬ⦆")
                if bstack1l1ll1l1ll_opy_:
                    playwright_annotate(item._page, str(bstack1l1ll1l1ll_opy_), bstack1l1111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ⦇"))
                    bstack1l1llll1l1_opy_(getattr(item, bstack1l1111l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⦈"), None), bstack1l1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ⦉"), str(bstack1l1ll1l1ll_opy_))
                    error_message = str(bstack1l1ll1l1ll_opy_)
                else:
                    bstack1l1llll1l1_opy_(getattr(item, bstack1l1111l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧ⦊"), None), bstack1l1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ⦋"))
                bstack1ll1111l111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ⦌").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1111l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ⦍"), default=bstack1l1111l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⦎"), help=bstack1l1111l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⦏"))
    parser.addoption(bstack1l1111l_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ⦐"), default=bstack1l1111l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢ⦑"), help=bstack1l1111l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ⦒"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1111l_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧ⦓"), action=bstack1l1111l_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥ⦔"), default=bstack1l1111l_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ⦕"),
                         help=bstack1l1111l_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ⦖"))
def bstack1llll1l1l11_opy_(log):
    if not (log[bstack1l1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⦗")] and log[bstack1l1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⦘")].strip()):
        return
    active = bstack1llll11l11l_opy_()
    log = {
        bstack1l1111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⦙"): log[bstack1l1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⦚")],
        bstack1l1111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⦛"): bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"ࠬࡠࠧ⦜"),
        bstack1l1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⦝"): log[bstack1l1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⦞")],
    }
    if active:
        if active[bstack1l1111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⦟")] == bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⦠"):
            log[bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⦡")] = active[bstack1l1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⦢")]
        elif active[bstack1l1111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⦣")] == bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࠫ⦤"):
            log[bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⦥")] = active[bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⦦")]
    TestHubHandler.bstack11l1lllll_opy_([log])
def bstack1llll11l11l_opy_():
    if len(store[bstack1l1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⦧")]) > 0 and store[bstack1l1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⦨")][-1]:
        return {
            bstack1l1111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ⦩"): bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⦪"),
            bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⦫"): store[bstack1l1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⦬")][-1]
        }
    if store.get(bstack1l1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⦭"), None):
        return {
            bstack1l1111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⦮"): bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⦯"),
            bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⦰"): store[bstack1l1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⦱")]
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
        item._1l1llllll111_opy_ = True
        bstack1l1lllll1l_opy_ = a11y.is_enabled_testcase(bstack1lllll11ll11_opy_(item.own_markers))
        if not cli.bstack1l1l11l111_opy_(bstack1l111l111l_opy_):
            item._a11y_test_case = bstack1l1lllll1l_opy_
            if bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⦲"), None):
                driver = getattr(item, bstack1l1111l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⦳"), None)
                item._a11y_started = a11y.start_test_capture(driver, bstack1l1lllll1l_opy_)
        if not TestHubHandler.on() or bstack1ll11111lll1_opy_ != bstack1l1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⦴"):
            return
        global current_test_uuid #, bstack1llll11lll1_opy_
        bstack1lll11lll11_opy_ = {
            bstack1l1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⦵"): uuid4().__str__(),
            bstack1l1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⦶"): bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"ࠫ࡟࠭⦷")
        }
        current_test_uuid = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⦸")]
        store[bstack1l1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⦹")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⦺")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lll1l1l11l_opy_[item.nodeid] = {**_1lll1l1l11l_opy_[item.nodeid], **bstack1lll11lll11_opy_}
        bstack1ll1111111l1_opy_(item, _1lll1l1l11l_opy_[item.nodeid], bstack1l1111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⦻"))
    except Exception as err:
        print(bstack1l1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡦࡥࡱࡲ࠺ࠡࡽࢀࠫ⦼"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⦽")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.BEFORE_EACH, TestHookState.PRE, item, bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⦾"))
    if bstack1lll1111ll_opy_.bstack1lll11l1llll_opy_():
            bstack1ll11111l1ll_opy_ = bstack1l1111l_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡧࡳࠡࡶ࡫ࡩࠥࡧࡢࡰࡴࡷࠤࡧࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ⦿")
            logger.error(bstack1ll11111l1ll_opy_)
            bstack1lll11lll11_opy_ = {
                bstack1l1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⧀"): uuid4().__str__(),
                bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⧁"): bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"ࠨ࡜ࠪ⧂"),
                bstack1l1111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⧃"): bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"ࠪ࡞ࠬ⧄"),
                bstack1l1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⧅"): bstack1l1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⧆"),
                bstack1l1111l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭⧇"): bstack1ll11111l1ll_opy_,
                bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⧈"): [],
                bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⧉"): []
            }
            bstack1ll1111111l1_opy_(item, bstack1lll11lll11_opy_, bstack1l1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ⧊"))
            pytest.skip(bstack1ll11111l1ll_opy_)
            return # skip all existing operations
    global bstack1ll1111111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1lllll1111l1_opy_():
        atexit.register(bstack1l11l11l_opy_)
        if not bstack1ll1111111ll_opy_:
            try:
                bstack1l1llllll1ll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1llll1l1ll1l_opy_():
                    bstack1l1llllll1ll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1l1llllll1ll_opy_:
                    signal.signal(s, bstack1ll1l111lll_opy_)
                bstack1ll1111111ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡨ࡫ࡶࡸࡪࡸࠠࡴ࡫ࡪࡲࡦࡲࠠࡩࡣࡱࡨࡱ࡫ࡲࡴ࠼ࠣࠦ⧋") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1ll1l1111lll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⧌")
    try:
        if not TestHubHandler.on():
            return
        uuid = uuid4().__str__()
        bstack1lll11lll11_opy_ = {
            bstack1l1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⧍"): uuid,
            bstack1l1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⧎"): bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"࡛ࠧࠩ⧏"),
            bstack1l1111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⧐"): bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⧑"),
            bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭⧒"): bstack1l1111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ⧓"),
            bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ⧔"): bstack1l1111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ⧕")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⧖")] = item
        store[bstack1l1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⧗")] = [uuid]
        if not _1lll1l1l11l_opy_.get(item.nodeid, None):
            _1lll1l1l11l_opy_[item.nodeid] = {bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⧘"): [], bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⧙"): []}
        _1lll1l1l11l_opy_[item.nodeid][bstack1l1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⧚")].append(bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⧛")])
        _1lll1l1l11l_opy_[item.nodeid + bstack1l1111l_opy_ (u"࠭࠭ࡴࡧࡷࡹࡵ࠭⧜")] = bstack1lll11lll11_opy_
        if cli.is_running():
            return # skip all existing operations
        bstack1ll11111ll1l_opy_(item, bstack1lll11lll11_opy_, bstack1l1111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⧝"))
    except Exception as err:
        print(bstack1l1111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫ⧞"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.POST, item)
        cli.test_framework.track_event(cli_context, TestFrameworkState.AFTER_EACH, TestHookState.PRE, item, bstack1l1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ⧟"))
        return # skip all existing operations
    try:
        global bstack11l111l1l1_opy_
        bstack11l1lllll1_opy_ = 0
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11l1lllll1_opy_ = int(os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ⧠")))
        if bstack11l111llll_opy_.bstack111l1l1l1_opy_() == bstack1l1111l_opy_ (u"ࠦࡹࡸࡵࡦࠤ⧡"):
            if bstack11l111llll_opy_.bstack11lll1ll_opy_() == bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⧢"):
                bstack1ll111111111_opy_ = bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⧣"), None)
                bstack11l1ll1l1_opy_ = bstack1ll111111111_opy_ + bstack1l1111l_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥ⧤")
                driver = getattr(item, bstack1l1111l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⧥"), None)
                bstack111ll11ll_opy_ = getattr(item, bstack1l1111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⧦"), None)
                bstack1ll111l1l_opy_ = getattr(item, bstack1l1111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⧧"), None)
                PercySDK.screenshot(driver, bstack11l1ll1l1_opy_, bstack111ll11ll_opy_=bstack111ll11ll_opy_, bstack1ll111l1l_opy_=bstack1ll111l1l_opy_, bstack1ll1l1l11l_opy_=bstack11l1lllll1_opy_)
        if not cli.bstack1l1l11l111_opy_(bstack1l111l111l_opy_):
            if getattr(item, bstack1l1111l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫ⧨"), False):
                bstack1l1l1ll1l_opy_.bstack1111ll1l_opy_(getattr(item, bstack1l1111l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⧩"), None), bstack11l111l1l1_opy_, logger, item)
        if not TestHubHandler.on():
            return
        bstack1lll11lll11_opy_ = {
            bstack1l1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⧪"): uuid4().__str__(),
            bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⧫"): bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"ࠨ࡜ࠪ⧬"),
            bstack1l1111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⧭"): bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⧮"),
            bstack1l1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ⧯"): bstack1l1111l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ⧰"),
            bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⧱"): bstack1l1111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⧲")
        }
        _1lll1l1l11l_opy_[item.nodeid + bstack1l1111l_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ⧳")] = bstack1lll11lll11_opy_
        bstack1ll11111ll1l_opy_(item, bstack1lll11lll11_opy_, bstack1l1111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⧴"))
    except Exception as err:
        print(bstack1l1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩ⧵"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1ll1l1111l1l_opy_(fixturedef.argname):
        store[bstack1l1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪ⧶")] = request.node
    elif bstack1ll1l111l111_opy_(fixturedef.argname):
        store[bstack1l1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪ⧷")] = request.node
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
            bstack1l1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⧸"): fixturedef.argname,
            bstack1l1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⧹"): bstack1lllll1l1l11_opy_(outcome),
            bstack1l1111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⧺"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭⧻")]
        if not _1lll1l1l11l_opy_.get(current_test_item.nodeid, None):
            _1lll1l1l11l_opy_[current_test_item.nodeid] = {bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⧼"): []}
        _1lll1l1l11l_opy_[current_test_item.nodeid][bstack1l1111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⧽")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ⧾"), str(err))
if bstack11111l111l_opy_() and TestHubHandler.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.PRE, request, step)
            return
        try:
            _1lll1l1l11l_opy_[request.node.nodeid][bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ⧿")].bstack11l1ll1l1l_opy_(id(step))
        except Exception as err:
            print(bstack1l1111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬ⨀"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step, exception)
            return
        try:
            _1lll1l1l11l_opy_[request.node.nodeid][bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⨁")].bstack1llll111l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭⨂"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState.STEP, TestHookState.POST, request, step)
            return
        try:
            bstack1llll1l1ll1_opy_: bstack1llll1l11l1_opy_ = _1lll1l1l11l_opy_[request.node.nodeid][bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⨃")]
            bstack1llll1l1ll1_opy_.bstack1llll111l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ⨄"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll11111lll1_opy_
        try:
            if not TestHubHandler.on() or bstack1ll11111lll1_opy_ != bstack1l1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ⨅"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, TestFrameworkState.TEST, TestHookState.PRE, request, feature, scenario)
                return
            driver = bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ⨆"), None)
            if not _1lll1l1l11l_opy_.get(request.node.nodeid, None):
                _1lll1l1l11l_opy_[request.node.nodeid] = {}
            bstack1llll1l1ll1_opy_ = bstack1llll1l11l1_opy_.bstack1ll11l1lll1l_opy_(
                scenario, feature, request.node,
                name=bstack1ll1l11111l1_opy_(request.node, scenario),
                started_at=bstack1l111l1ll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1111l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩ⨇"),
                tags=bstack1ll1l111ll1l_opy_(feature, scenario),
                integrations=TestHubHandler.bstack1llll11ll11_opy_(driver) if driver and driver.session_id else {}
            )
            _1lll1l1l11l_opy_[request.node.nodeid][bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ⨈")] = bstack1llll1l1ll1_opy_
            bstack1ll111111l11_opy_(bstack1llll1l1ll1_opy_.uuid)
            TestHubHandler.bstack1llll1111ll_opy_(bstack1l1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⨉"), bstack1llll1l1ll1_opy_)
        except Exception as err:
            print(bstack1l1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬ⨊"), str(err))
def bstack1l1lllllll11_opy_(bstack1llll111l11_opy_):
    if bstack1llll111l11_opy_ in store[bstack1l1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⨋")]:
        store[bstack1l1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⨌")].remove(bstack1llll111l11_opy_)
def bstack1ll111111l11_opy_(test_uuid):
    store[bstack1l1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⨍")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@TestHubHandler.bstack1ll111ll11l1_opy_
def bstack1ll11111l111_opy_(item, call, report):
    logger.debug(bstack1l1111l_opy_ (u"ࠧࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠩ⨎"))
    global bstack1ll11111lll1_opy_
    bstack1ll1lll11_opy_ = bstack1l111l1ll_opy_()
    if hasattr(report, bstack1l1111l_opy_ (u"ࠨࡵࡷࡳࡵ࠭⨏")):
        bstack1ll1lll11_opy_ = bstack1lllll1l11l1_opy_(report.stop)
    elif hasattr(report, bstack1l1111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨ⨐")):
        bstack1ll1lll11_opy_ = bstack1lllll1l11l1_opy_(report.start)
    try:
        if getattr(report, bstack1l1111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⨑"), bstack1l1111l_opy_ (u"ࠫࠬ⨒")) == bstack1l1111l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⨓"):
            logger.debug(bstack1l1111l_opy_ (u"࠭ࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡶࡸࡦࡺࡥࠡ࠯ࠣࡿࢂ࠲ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࠱ࠥࢁࡽࠨ⨔").format(getattr(report, bstack1l1111l_opy_ (u"ࠧࡸࡪࡨࡲࠬ⨕"), bstack1l1111l_opy_ (u"ࠨࠩ⨖")).__str__(), bstack1ll11111lll1_opy_))
            if bstack1ll11111lll1_opy_ == bstack1l1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⨗"):
                _1lll1l1l11l_opy_[item.nodeid][bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⨘")] = bstack1ll1lll11_opy_
                bstack1ll1111111l1_opy_(item, _1lll1l1l11l_opy_[item.nodeid], bstack1l1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⨙"), report, call)
                store[bstack1l1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⨚")] = None
            elif bstack1ll11111lll1_opy_ == bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ⨛"):
                bstack1llll1l1ll1_opy_ = _1lll1l1l11l_opy_[item.nodeid][bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⨜")]
                bstack1llll1l1ll1_opy_.set(hooks=_1lll1l1l11l_opy_[item.nodeid].get(bstack1l1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⨝"), []))
                exception, bstack1llll11ll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1llll11ll1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨ⨞"), bstack1l1111l_opy_ (u"ࠪࠫ⨟"))]
                bstack1llll1l1ll1_opy_.stop(time=bstack1ll1lll11_opy_, result=Result(result=getattr(report, bstack1l1111l_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬ⨠"), bstack1l1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⨡")), exception=exception, bstack1llll11ll1l_opy_=bstack1llll11ll1l_opy_))
                TestHubHandler.bstack1llll1111ll_opy_(bstack1l1111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⨢"), _1lll1l1l11l_opy_[item.nodeid][bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⨣")])
        elif getattr(report, bstack1l1111l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭⨤"), bstack1l1111l_opy_ (u"ࠩࠪ⨥")) in [bstack1l1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⨦"), bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⨧")]:
            logger.debug(bstack1l1111l_opy_ (u"ࠬ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡵࡷࡥࡹ࡫ࠠ࠮ࠢࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤࢀࢃࠧ⨨").format(getattr(report, bstack1l1111l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⨩"), bstack1l1111l_opy_ (u"ࠧࠨ⨪")).__str__(), bstack1ll11111lll1_opy_))
            bstack1lll1llllll_opy_ = item.nodeid + bstack1l1111l_opy_ (u"ࠨ࠯ࠪ⨫") + getattr(report, bstack1l1111l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⨬"), bstack1l1111l_opy_ (u"ࠪࠫ⨭"))
            if getattr(report, bstack1l1111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ⨮"), False):
                hook_type = bstack1l1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⨯") if getattr(report, bstack1l1111l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⨰"), bstack1l1111l_opy_ (u"ࠧࠨ⨱")) == bstack1l1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⨲") else bstack1l1111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⨳")
                _1lll1l1l11l_opy_[bstack1lll1llllll_opy_] = {
                    bstack1l1111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⨴"): uuid4().__str__(),
                    bstack1l1111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⨵"): bstack1ll1lll11_opy_,
                    bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⨶"): hook_type
                }
            _1lll1l1l11l_opy_[bstack1lll1llllll_opy_][bstack1l1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⨷")] = bstack1ll1lll11_opy_
            bstack1l1lllllll11_opy_(_1lll1l1l11l_opy_[bstack1lll1llllll_opy_][bstack1l1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⨸")])
            bstack1ll11111ll1l_opy_(item, _1lll1l1l11l_opy_[bstack1lll1llllll_opy_], bstack1l1111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⨹"), report, call)
            if getattr(report, bstack1l1111l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧ⨺"), bstack1l1111l_opy_ (u"ࠪࠫ⨻")) == bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ⨼"):
                if getattr(report, bstack1l1111l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭⨽"), bstack1l1111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⨾")) == bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⨿"):
                    bstack1lll11lll11_opy_ = {
                        bstack1l1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⩀"): uuid4().__str__(),
                        bstack1l1111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⩁"): bstack1l111l1ll_opy_(),
                        bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩂"): bstack1l111l1ll_opy_()
                    }
                    _1lll1l1l11l_opy_[item.nodeid] = {**_1lll1l1l11l_opy_[item.nodeid], **bstack1lll11lll11_opy_}
                    bstack1ll1111111l1_opy_(item, _1lll1l1l11l_opy_[item.nodeid], bstack1l1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⩃"))
                    bstack1ll1111111l1_opy_(item, _1lll1l1l11l_opy_[item.nodeid], bstack1l1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⩄"), report, call)
    except Exception as err:
        print(bstack1l1111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫ⩅"), str(err))
def bstack1l1llllll11l_opy_(test, bstack1lll11lll11_opy_, result=None, call=None, bstack111l1l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1llll1l1ll1_opy_ = {
        bstack1l1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⩆"): bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⩇")],
        bstack1l1111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⩈"): bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⩉"),
        bstack1l1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⩊"): test.name,
        bstack1l1111l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ⩋"): {
            bstack1l1111l_opy_ (u"࠭࡬ࡢࡰࡪࠫ⩌"): bstack1l1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⩍"),
            bstack1l1111l_opy_ (u"ࠨࡥࡲࡨࡪ࠭⩎"): inspect.getsource(test.obj)
        },
        bstack1l1111l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⩏"): test.name,
        bstack1l1111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⩐"): test.name,
        bstack1l1111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ⩑"): bstack1l1lll1l1_opy_.bstack1lll1l11ll1_opy_(test),
        bstack1l1111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ⩒"): file_path,
        bstack1l1111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ⩓"): file_path,
        bstack1l1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⩔"): bstack1l1111l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⩕"),
        bstack1l1111l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ⩖"): file_path,
        bstack1l1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⩗"): bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⩘")],
        bstack1l1111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⩙"): bstack1l1111l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⩚"),
        bstack1l1111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ⩛"): {
            bstack1l1111l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ⩜"): test.nodeid
        },
        bstack1l1111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⩝"): bstack1lllll11ll11_opy_(test.own_markers)
    }
    if bstack111l1l1l_opy_ in [bstack1l1111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ⩞"), bstack1l1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⩟")]:
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠬࡳࡥࡵࡣࠪ⩠")] = {
            bstack1l1111l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ⩡"): bstack1lll11lll11_opy_.get(bstack1l1111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⩢"), [])
        }
    if bstack111l1l1l_opy_ == bstack1l1111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⩣"):
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⩤")] = bstack1l1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ⩥")
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⩦")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⩧")]
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⩨")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⩩")]
    if result:
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⩪")] = result.outcome
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ⩫")] = result.duration * 1000
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⩬")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⩭")]
        if result.failed:
            bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⩮")] = TestHubHandler.bstack1ll111l1l1l_opy_(call.excinfo.typename)
            bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ⩯")] = TestHubHandler.bstack1ll111lll1ll_opy_(call.excinfo, result)
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⩰")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⩱")]
    if outcome:
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⩲")] = bstack1lllll1l1l11_opy_(outcome)
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ⩳")] = 0
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⩴")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⩵")]
        if bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⩶")] == bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⩷"):
            bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⩸")] = bstack1l1111l_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ⩹")  # bstack1ll111111ll1_opy_
            bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⩺")] = [{bstack1l1111l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⩻"): [bstack1l1111l_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩ⩼")]}]
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⩽")] = bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⩾")]
    return bstack1llll1l1ll1_opy_
def bstack1l1lllllllll_opy_(test, bstack1lll1l1l111_opy_, bstack111l1l1l_opy_, result, call, outcome, bstack1ll1111l1l11_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⩿")]
    hook_name = bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⪀")]
    hook_data = {
        bstack1l1111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⪁"): bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⪂")],
        bstack1l1111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⪃"): bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⪄"),
        bstack1l1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⪅"): bstack1l1111l_opy_ (u"ࠨࡽࢀࠫ⪆").format(bstack1ll1l111ll11_opy_(hook_name)),
        bstack1l1111l_opy_ (u"ࠩࡥࡳࡩࡿࠧ⪇"): {
            bstack1l1111l_opy_ (u"ࠪࡰࡦࡴࡧࠨ⪈"): bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⪉"),
            bstack1l1111l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⪊"): None
        },
        bstack1l1111l_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬ⪋"): test.name,
        bstack1l1111l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ⪌"): bstack1l1lll1l1_opy_.bstack1lll1l11ll1_opy_(test, hook_name),
        bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ⪍"): file_path,
        bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ⪎"): file_path,
        bstack1l1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⪏"): bstack1l1111l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⪐"),
        bstack1l1111l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪ⪑"): file_path,
        bstack1l1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⪒"): bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⪓")],
        bstack1l1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⪔"): bstack1l1111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ⪕") if bstack1ll11111lll1_opy_ == bstack1l1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ⪖") else bstack1l1111l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⪗"),
        bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⪘"): hook_type
    }
    bstack11llllll11l_opy_ = bstack1lll1l1ll11_opy_(_1lll1l1l11l_opy_.get(test.nodeid, None))
    if bstack11llllll11l_opy_:
        hook_data[bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ⪙")] = bstack11llllll11l_opy_
    if result:
        hook_data[bstack1l1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⪚")] = result.outcome
        hook_data[bstack1l1111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⪛")] = result.duration * 1000
        hook_data[bstack1l1111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⪜")] = bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⪝")]
        if result.failed:
            hook_data[bstack1l1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⪞")] = TestHubHandler.bstack1ll111l1l1l_opy_(call.excinfo.typename)
            hook_data[bstack1l1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⪟")] = TestHubHandler.bstack1ll111lll1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⪠")] = bstack1lllll1l1l11_opy_(outcome)
        hook_data[bstack1l1111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⪡")] = 100
        hook_data[bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⪢")] = bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⪣")]
        if hook_data[bstack1l1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⪤")] == bstack1l1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⪥"):
            hook_data[bstack1l1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⪦")] = bstack1l1111l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⪧")  # bstack1ll111111ll1_opy_
            hook_data[bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⪨")] = [{bstack1l1111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⪩"): [bstack1l1111l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⪪")]}]
    if bstack1ll1111l1l11_opy_:
        hook_data[bstack1l1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⪫")] = bstack1ll1111l1l11_opy_.result
        hook_data[bstack1l1111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⪬")] = bstack1ll1l1ll1ll_opy_(bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⪭")], bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⪮")])
        hook_data[bstack1l1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⪯")] = bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⪰")]
        if hook_data[bstack1l1111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ⪱")] == bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⪲"):
            hook_data[bstack1l1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ⪳")] = TestHubHandler.bstack1ll111l1l1l_opy_(bstack1ll1111l1l11_opy_.exception_type)
            hook_data[bstack1l1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭⪴")] = [{bstack1l1111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ⪵"): bstack1lllll1lll11_opy_(bstack1ll1111l1l11_opy_.exception)}]
    return hook_data
def bstack1ll1111111l1_opy_(test, bstack1lll11lll11_opy_, bstack111l1l1l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1111l_opy_ (u"ࠧࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡦࡸࡨࡲࡹࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡨࡧࡱࡩࡷࡧࡴࡦࠢࡷࡩࡸࡺࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࠦ࠭ࠡࡽࢀࠫ⪶").format(bstack111l1l1l_opy_))
    bstack1llll1l1ll1_opy_ = bstack1l1llllll11l_opy_(test, bstack1lll11lll11_opy_, result, call, bstack111l1l1l_opy_, outcome)
    driver = getattr(test, bstack1l1111l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ⪷"), None)
    if bstack111l1l1l_opy_ == bstack1l1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⪸") and driver:
        bstack1llll1l1ll1_opy_[bstack1l1111l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ⪹")] = TestHubHandler.bstack1llll11ll11_opy_(driver)
    if bstack111l1l1l_opy_ == bstack1l1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ⪺"):
        bstack111l1l1l_opy_ = bstack1l1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⪻")
    bstack1lll1ll111l_opy_ = {
        bstack1l1111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⪼"): bstack111l1l1l_opy_,
        bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⪽"): bstack1llll1l1ll1_opy_
    }
    TestHubHandler.bstack1111lll1l1_opy_(bstack1lll1ll111l_opy_)
    if bstack111l1l1l_opy_ == bstack1l1111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⪾"):
        threading.current_thread().bstackTestMeta = {bstack1l1111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⪿"): bstack1l1111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⫀")}
    elif bstack111l1l1l_opy_ == bstack1l1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⫁"):
        threading.current_thread().bstackTestMeta = {bstack1l1111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⫂"): getattr(result, bstack1l1111l_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧ⫃"), bstack1l1111l_opy_ (u"ࠧࠨ⫄"))}
def bstack1ll11111ll1l_opy_(test, bstack1lll11lll11_opy_, bstack111l1l1l_opy_, result=None, call=None, outcome=None, bstack1ll1111l1l11_opy_=None):
    logger.debug(bstack1l1111l_opy_ (u"ࠨࡵࡨࡲࡩࡥࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡧࡹࡩࡳࡺ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣ࡬ࡴࡵ࡫ࠡࡦࡤࡸࡦ࠲ࠠࡦࡸࡨࡲࡹ࡚ࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⫅").format(bstack111l1l1l_opy_))
    hook_data = bstack1l1lllllllll_opy_(test, bstack1lll11lll11_opy_, bstack111l1l1l_opy_, result, call, outcome, bstack1ll1111l1l11_opy_)
    bstack1lll1ll111l_opy_ = {
        bstack1l1111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⫆"): bstack111l1l1l_opy_,
        bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬ⫇"): hook_data
    }
    TestHubHandler.bstack1111lll1l1_opy_(bstack1lll1ll111l_opy_)
def bstack1lll1l1ll11_opy_(bstack1lll11lll11_opy_):
    if not bstack1lll11lll11_opy_:
        return None
    if bstack1lll11lll11_opy_.get(bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⫈"), None):
        return getattr(bstack1lll11lll11_opy_[bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⫉")], bstack1l1111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ⫊"), None)
    return bstack1lll11lll11_opy_.get(bstack1l1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⫋"), None)
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
        places = [bstack1l1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⫌"), bstack1l1111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⫍"), bstack1l1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ⫎")]
        logs = []
        for bstack1ll1111l1111_opy_ in places:
            records = caplog.get_records(bstack1ll1111l1111_opy_)
            bstack1ll11111l11l_opy_ = bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⫏") if bstack1ll1111l1111_opy_ == bstack1l1111l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⫐") else bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⫑")
            bstack1ll11111ll11_opy_ = request.node.nodeid + (bstack1l1111l_opy_ (u"ࠧࠨ⫒") if bstack1ll1111l1111_opy_ == bstack1l1111l_opy_ (u"ࠨࡥࡤࡰࡱ࠭⫓") else bstack1l1111l_opy_ (u"ࠩ࠰ࠫ⫔") + bstack1ll1111l1111_opy_)
            test_uuid = bstack1lll1l1ll11_opy_(_1lll1l1l11l_opy_.get(bstack1ll11111ll11_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack1llll1ll1l11_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⫕"): bstack1llll1ll1l1l_opy_(record.created).isoformat() + bstack1l1111l_opy_ (u"ࠫ࡟࠭⫖"),
                    bstack1l1111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⫗"): record.levelname,
                    bstack1l1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⫘"): record.message,
                    bstack1ll11111l11l_opy_: test_uuid
                })
        if len(logs) > 0:
            TestHubHandler.bstack11l1lllll_opy_(logs)
    except Exception as err:
        print(bstack1l1111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ⫙"), str(err))
def bstack11ll111l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l11l11111_opy_
    bstack1ll1l1lll_opy_ = bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ⫚"), None) and bstack11l11l11_opy_(
            threading.current_thread(), bstack1l1111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⫛"), None)
    bstack11llll11_opy_ = getattr(driver, bstack1l1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ⫝̸"), None) != None and getattr(driver, bstack1l1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ⫝"), None) == True
    if sequence == bstack1l1111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ⫞") and driver != None:
      if not bstack1l11l11111_opy_ and bstack1lllllll11l_opy_() and bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⫟") in CONFIG and CONFIG[bstack1l1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⫠")] == True and accessibility_scripts.bstack1111lllll_opy_(driver_command) and (bstack11llll11_opy_ or bstack1ll1l1lll_opy_) and not bstack1l11llll1l_opy_(args):
        try:
          bstack1l11l11111_opy_ = True
          logger.debug(bstack1l1111l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪ⫡").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧ⫢").format(str(err)))
        bstack1l11l11111_opy_ = False
    if sequence == bstack1l1111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⫣"):
        if driver_command == bstack1l1111l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ⫤"):
            TestHubHandler.bstack11l1lll1l_opy_({
                bstack1l1111l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⫥"): response[bstack1l1111l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ⫦")],
                bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⫧"): store[bstack1l1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⫨")]
            })
def bstack1l11l11l_opy_():
    global bstack111l11111l_opy_
    logger_utils.bstack11l1lll1_opy_()
    logging.shutdown()
    TestHubHandler.bstack1lll11l11ll_opy_()
    for driver in bstack111l11111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l111lll_opy_(*args):
    global bstack111l11111l_opy_
    TestHubHandler.bstack1lll11l11ll_opy_()
    for driver in bstack111l11111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1ll1l1l_opy_, stage=STAGE.bstack111ll11111_opy_, bstack1l111l111_opy_=SESSION_NAME)
def bstack1lll1l1l1_opy_(self, *args, **kwargs):
    bstack1lllll1l111_opy_ = bstack11111l11_opy_(self, *args, **kwargs)
    bstack111llllll1_opy_ = getattr(threading.current_thread(), bstack1l1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪ⫩"), None)
    if bstack111llllll1_opy_ and bstack111llllll1_opy_.get(bstack1l1111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⫪"), bstack1l1111l_opy_ (u"ࠫࠬ⫫")) == bstack1l1111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⫬"):
        TestHubHandler.send_cbt_info(self)
    return bstack1lllll1l111_opy_
@measure(event_name=EVENTS.bstack1l11l1lll_opy_, stage=STAGE.bstack1l1lll1lll_opy_, bstack1l111l111_opy_=SESSION_NAME)
def bstack111ll1l11_opy_(framework_name):
    from bstack_utils.config import Config
    global_config = Config.bstack111111l1ll_opy_()
    if global_config.get_property(bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⫭")):
        return
    global_config.bstack11l11lll1l_opy_(bstack1l1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ⫮"), True)
    global FRAMEWORK_NAME
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    FRAMEWORK_NAME = framework_name
    logger.info(bstack111lll11l1_opy_.format(FRAMEWORK_NAME.split(bstack1l1111l_opy_ (u"ࠨ࠯ࠪ⫯"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1lllllll11l_opy_():
            Service.start = bstack11lll11lll_opy_
            Service.stop = bstack1ll11l111_opy_
            webdriver.Remote.get = bstack1l111ll111_opy_
            webdriver.Remote.__init__ = bstack11l11l111l_opy_
            if not isinstance(os.getenv(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ⫰")), str):
                return
            WebDriver.quit = bstack11111ll1l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif TestHubHandler.on():
            webdriver.Remote.__init__ = bstack1lll1l1l1_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1111l_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ⫱")):
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = eval(os.environ.get(bstack1l1111l_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩ⫲")))
    if not SELENIUM_OR_PLAYWRIGHT_INSTALLED:
        bstack111111l11l_opy_(bstack1l1111l_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ⫳"), bstack11llllll11_opy_)
    if bstack11ll1l1l11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1111l_opy_ (u"࠭࡟ࡨࡧࡷࡣࡵࡸ࡯ࡹࡻࡢࡹࡷࡲࠧ⫴")) and callable(getattr(RemoteConnection, bstack1l1111l_opy_ (u"ࠧࡠࡩࡨࡸࡤࡶࡲࡰࡺࡼࡣࡺࡸ࡬ࠨ⫵"))):
                RemoteConnection._get_proxy_url = bstack1l1l1l111_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1l1l111_opy_
        except Exception as e:
            logger.error(bstack1l1l1lllll_opy_.format(str(e)))
    if bstack1l1111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⫶") in str(framework_name).lower():
        if not bstack1lllllll11l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11111ll1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11llll111_opy_
            Config.getoption = bstack1ll1llll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111l1ll111_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1l11ll_opy_, stage=STAGE.bstack111ll11111_opy_, bstack1l111l111_opy_=SESSION_NAME)
def bstack11111ll1l1_opy_(self):
    global FRAMEWORK_NAME
    global bstack1l1llll1_opy_
    global bstack1llllllll_opy_
    try:
        if bstack1l1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ⫷") in FRAMEWORK_NAME and self.session_id != None and bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ⫸"), bstack1l1111l_opy_ (u"ࠫࠬ⫹")) != bstack1l1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⫺"):
            bstack1lllll1ll_opy_ = bstack1l1111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⫻") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⫼")
            bstack1l1l1l11_opy_(logger, True)
            if os.environ.get(bstack1l1111l_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫ⫽"), None):
                self.execute_script(
                    bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ⫾") + json.dumps(
                        os.environ.get(bstack1l1111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⫿"))) + bstack1l1111l_opy_ (u"ࠫࢂࢃࠧ⬀"))
            if self != None:
                bstack11ll1l1111_opy_(self, bstack1lllll1ll_opy_, bstack1l1111l_opy_ (u"ࠬ࠲ࠠࠨ⬁").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1l1l11l111_opy_(bstack1l111l111l_opy_):
            item = store.get(bstack1l1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⬂"), None)
            if item is not None and bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⬃"), None):
                bstack1l1l1ll1l_opy_.bstack1111ll1l_opy_(self, bstack11l111l1l1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1111l_opy_ (u"ࠨࠩ⬄")
    except Exception as e:
        logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ⬅") + str(e))
    bstack1llllllll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack111l11l1ll_opy_, stage=STAGE.bstack111ll11111_opy_, bstack1l111l111_opy_=SESSION_NAME)
def bstack11l11l111l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1llll1_opy_
    global SESSION_NAME
    global PARALLELISE_VANILLA_PYTHON
    global FRAMEWORK_NAME
    global bstack11111l11_opy_
    global bstack111l11111l_opy_
    global bstack1ll1111l1_opy_
    global bstack11ll1ll11_opy_
    global bstack11l111l1l1_opy_
    CONFIG[bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⬆")] = str(FRAMEWORK_NAME) + str(__version__)
    command_executor = bstack1l11111l1l_opy_(bstack1ll1111l1_opy_, CONFIG)
    logger.debug(bstack11l1l1l11l_opy_.format(command_executor))
    proxy = bstack1lll1l11_opy_(CONFIG, proxy)
    bstack11l1lllll1_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11l1lllll1_opy_ = int(os.environ.get(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⬇")))
    except:
        bstack11l1lllll1_opy_ = 0
    bstack111ll1ll1_opy_ = get_caps(CONFIG, bstack11l1lllll1_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack111ll1ll1_opy_)))
    bstack11l111l1l1_opy_ = CONFIG.get(bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⬈"))[bstack11l1lllll1_opy_]
    if bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⬉") in CONFIG and CONFIG[bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ⬊")]:
        update_caps_for_local(bstack111ll1ll1_opy_, bstack11ll1ll11_opy_)
    if a11y.is_enabled_platform(CONFIG, bstack11l1lllll1_opy_) and a11y.is_platform_supported(bstack111ll1ll1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1l1l11l111_opy_(bstack1l111l111l_opy_):
            a11y.set_capabilities(bstack111ll1ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack11llll11l1_opy_ = bstack1111111111_opy_(desired_capabilities)
        bstack11llll11l1_opy_[bstack1l1111l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ⬋")] = bstack1l11l1l111_opy_(CONFIG)
        bstack11ll11ll11_opy_ = get_caps(bstack11llll11l1_opy_)
        if bstack11ll11ll11_opy_:
            bstack111ll1ll1_opy_ = update(bstack11ll11ll11_opy_, bstack111ll1ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l11ll1l_opy_(options, bstack111ll1ll1_opy_)
    if not options:
        options = bstack1l111lll1_opy_(bstack111ll1ll1_opy_)
    if proxy and bstack111111lll_opy_() >= version.parse(bstack1l1111l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ⬌")):
        options.proxy(proxy)
    if options and bstack111111lll_opy_() >= version.parse(bstack1l1111l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ⬍")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111111lll_opy_() < version.parse(bstack1l1111l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ⬎")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack111ll1ll1_opy_)
    logger.info(bstack111ll1l1l1_opy_)
    bstack11l11lll_opy_.end(EVENTS.bstack1l11l1lll_opy_.value, EVENTS.bstack1l11l1lll_opy_.value + bstack1l1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ⬏"),
                               EVENTS.bstack1l11l1lll_opy_.value + bstack1l1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ⬐"), True, None)
    try:
        if bstack111111lll_opy_() >= version.parse(bstack1l1111l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ⬑")):
            bstack11111l11_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack111111lll_opy_() >= version.parse(bstack1l1111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⬒")):
            bstack11111l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack111111lll_opy_() >= version.parse(bstack1l1111l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ⬓")):
            bstack11111l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack11111l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack111l1111l_opy_:
        logger.error(bstack11ll11l1_opy_.format(bstack1l1111l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠩ⬔"), str(bstack111l1111l_opy_)))
        raise bstack111l1111l_opy_
    try:
        bstack11l1l1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠫࠬ⬕")
        if bstack111111lll_opy_() >= version.parse(bstack1l1111l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭⬖")):
            bstack11l1l1l1ll_opy_ = self.caps.get(bstack1l1111l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ⬗"))
        else:
            bstack11l1l1l1ll_opy_ = self.capabilities.get(bstack1l1111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ⬘"))
        if bstack11l1l1l1ll_opy_:
            bstack11llll1l11_opy_(bstack11l1l1l1ll_opy_)
            if bstack111111lll_opy_() <= version.parse(bstack1l1111l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ⬙")):
                self.command_executor._url = bstack1l1111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ⬚") + bstack1ll1111l1_opy_ + bstack1l1111l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ⬛")
            else:
                self.command_executor._url = bstack1l1111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ⬜") + bstack11l1l1l1ll_opy_ + bstack1l1111l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ⬝")
            logger.debug(bstack1lll11l1l_opy_.format(bstack11l1l1l1ll_opy_))
        else:
            logger.debug(bstack1l1l111l1_opy_.format(bstack1l1111l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ⬞")))
    except Exception as e:
        logger.debug(bstack1l1l111l1_opy_.format(e))
    bstack1l1llll1_opy_ = self.session_id
    if bstack1l1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ⬟") in FRAMEWORK_NAME:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⬠"), None)
        if item:
            bstack1l1llllllll1_opy_ = getattr(item, bstack1l1111l_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ⬡"), False)
            if not getattr(item, bstack1l1111l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ⬢"), None) and bstack1l1llllllll1_opy_:
                setattr(store[bstack1l1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⬣")], bstack1l1111l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⬤"), self)
        bstack111llllll1_opy_ = getattr(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⬥"), None)
        if bstack111llllll1_opy_ and bstack111llllll1_opy_.get(bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⬦"), bstack1l1111l_opy_ (u"ࠨࠩ⬧")) == bstack1l1111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ⬨"):
            TestHubHandler.send_cbt_info(self)
    bstack111l11111l_opy_.append(self)
    if bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⬩") in CONFIG and bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⬪") in CONFIG[bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ⬫")][bstack11l1lllll1_opy_]:
        SESSION_NAME = CONFIG[bstack1l1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⬬")][bstack11l1lllll1_opy_][bstack1l1111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⬭")]
    logger.debug(bstack1ll1l1ll11_opy_.format(bstack1l1llll1_opy_))
@measure(event_name=EVENTS.bstack111l1111_opy_, stage=STAGE.bstack111ll11111_opy_, bstack1l111l111_opy_=SESSION_NAME)
def bstack1l111ll111_opy_(self, url):
    global bstack1lllllll1_opy_
    global CONFIG
    try:
        bstack11l1l1ll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11111l1ll1_opy_.format(str(err)))
    try:
        bstack1lllllll1_opy_(self, url)
    except Exception as e:
        try:
            parsed_error = str(e)
            if any(err_msg in parsed_error for err_msg in bstack1111llll1_opy_):
                bstack11l1l1ll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11111l1ll1_opy_.format(str(err)))
        raise e
def bstack1llllll1ll_opy_(item, when):
    global bstack1l1ll111l1_opy_
    try:
        bstack1l1ll111l1_opy_(item, when)
    except Exception as e:
        pass
def bstack111l1ll111_opy_(item, call, rep):
    global bstack1llllll11l1_opy_
    global bstack111l11111l_opy_
    name = bstack1l1111l_opy_ (u"ࠨࠩ⬮")
    try:
        if rep.when == bstack1l1111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⬯"):
            bstack1l1llll1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ⬰"))
            try:
                if (str(skipSessionName).lower() != bstack1l1111l_opy_ (u"ࠫࡹࡸࡵࡦࠩ⬱")):
                    name = str(rep.nodeid)
                    bstack1lllll1111_opy_ = bstack1l11111l11_opy_(bstack1l1111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⬲"), name, bstack1l1111l_opy_ (u"࠭ࠧ⬳"), bstack1l1111l_opy_ (u"ࠧࠨ⬴"), bstack1l1111l_opy_ (u"ࠨࠩ⬵"), bstack1l1111l_opy_ (u"ࠩࠪ⬶"))
                    os.environ[bstack1l1111l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⬷")] = name
                    for driver in bstack111l11111l_opy_:
                        if bstack1l1llll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lllll1111_opy_)
            except Exception as e:
                logger.debug(bstack1l1111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⬸").format(str(e)))
            try:
                bstack1l111llll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭⬹"):
                    status = bstack1l1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⬺") if rep.outcome.lower() == bstack1l1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⬻") else bstack1l1111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⬼")
                    reason = bstack1l1111l_opy_ (u"ࠩࠪ⬽")
                    if status == bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⬾"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ⬿") if status == bstack1l1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⭀") else bstack1l1111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⭁")
                    data = name + bstack1l1111l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ⭂") if status == bstack1l1111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⭃") else name + bstack1l1111l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ⭄") + reason
                    bstack1llll1111l_opy_ = bstack1l11111l11_opy_(bstack1l1111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ⭅"), bstack1l1111l_opy_ (u"ࠫࠬ⭆"), bstack1l1111l_opy_ (u"ࠬ࠭⭇"), bstack1l1111l_opy_ (u"࠭ࠧ⭈"), level, data)
                    for driver in bstack111l11111l_opy_:
                        if bstack1l1llll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1111l_opy_)
            except Exception as e:
                logger.debug(bstack1l1111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ⭉").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ⭊").format(str(e)))
    bstack1llllll11l1_opy_(item, call, rep)
notset = Notset()
def bstack1ll1llll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1ll111_opy_
    if str(name).lower() == bstack1l1111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ⭋"):
        return bstack1l1111l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ⭌")
    else:
        return bstack1l1ll111_opy_(self, name, default, skip)
def bstack1l1l1l111_opy_(self):
    global CONFIG
    global bstack1lllll11_opy_
    try:
        proxy = bstack11l1ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ⭍")):
                proxies = bstack111ll111ll_opy_(proxy, bstack1l11111l1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack11ll1l1lll_opy_ = proxies.popitem()
                    if bstack1l1111l_opy_ (u"ࠧࡀ࠯࠰ࠤ⭎") in bstack11ll1l1lll_opy_:
                        return bstack11ll1l1lll_opy_
                    else:
                        return bstack1l1111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⭏") + bstack11ll1l1lll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦ⭐").format(str(e)))
    return bstack1lllll11_opy_(self)
def bstack11ll1l1l11_opy_():
    return (bstack1l1111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⭑") in CONFIG or bstack1l1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⭒") in CONFIG) and bstack11l1l1l11_opy_() and bstack111111lll_opy_() >= version.parse(
        bstack111l11l11_opy_)
def bstack111l11lll1_opy_(self,
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
    CONFIG[bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⭓")] = str(FRAMEWORK_NAME) + str(__version__)
    bstack11l1lllll1_opy_ = 0
    try:
        if PARALLELISE_VANILLA_PYTHON is True:
            bstack11l1lllll1_opy_ = int(os.environ.get(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ⭔")))
    except:
        bstack11l1lllll1_opy_ = 0
    CONFIG[bstack1l1111l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ⭕")] = True
    bstack111ll1ll1_opy_ = get_caps(CONFIG, bstack11l1lllll1_opy_)
    logger.debug(CONFIG_FILE_CONTENT.format(str(bstack111ll1ll1_opy_)))
    if CONFIG.get(bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ⭖")):
        update_caps_for_local(bstack111ll1ll1_opy_, bstack11ll1ll11_opy_)
    if bstack1l1111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⭗") in CONFIG and bstack1l1111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⭘") in CONFIG[bstack1l1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⭙")][bstack11l1lllll1_opy_]:
        SESSION_NAME = CONFIG[bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⭚")][bstack11l1lllll1_opy_][bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⭛")]
    import urllib
    import json
    if bstack1l1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⭜") in CONFIG and str(CONFIG[bstack1l1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⭝")]).lower() != bstack1l1111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭⭞"):
        bstack11l111l1ll_opy_ = get_turboscale_playwright_url()
        cdpUrl = bstack11l111l1ll_opy_ + urllib.parse.quote(json.dumps(bstack111ll1ll1_opy_))
    else:
        cdpUrl = bstack1l1111l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ⭟") + urllib.parse.quote(json.dumps(bstack111ll1ll1_opy_))
    browser = self.connect(cdpUrl)
    return browser
def patch_playwright():
    global SELENIUM_OR_PLAYWRIGHT_INSTALLED
    global FRAMEWORK_NAME
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l111lll1l1_opy_
        if not bstack1lllllll11l_opy_():
            global bstack1l1l1ll11l_opy_
            if not bstack1l1l1ll11l_opy_:
                from bstack_utils.helper import bstack11l11ll1l_opy_, bstack1lllll1l1ll1_opy_
                bstack1l1l1ll11l_opy_ = bstack11l11ll1l_opy_()
                bstack1lllll1l1ll1_opy_(FRAMEWORK_NAME)
            BrowserType.connect = bstack1l111lll1l1_opy_
            return
        BrowserType.launch = bstack111l11lll1_opy_
        SELENIUM_OR_PLAYWRIGHT_INSTALLED = True
    except Exception as e:
        pass
def bstack1l1lllll1ll1_opy_():
    global CONFIG
    global bstack1111llll11_opy_
    global bstack1ll1111l1_opy_
    global bstack11ll1ll11_opy_
    global PARALLELISE_VANILLA_PYTHON
    global bstack11ll1lll1_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ⭠")))
    bstack1111llll11_opy_ = eval(os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ⭡")))
    bstack1ll1111l1_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ⭢"))
    bstack1ll1l1ll_opy_(CONFIG, bstack1111llll11_opy_)
    bstack11ll1lll1_opy_ = logger_utils.configure_logger(CONFIG, bstack11ll1lll1_opy_)
    if cli.bstack1l1ll1l1l_opy_():
        bstack111111lll1_opy_.invoke(Events.CONNECT, bstack111lll1lll_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ⭣"), bstack1l1111l_opy_ (u"࠭࠰ࠨ⭤")))
        cli.bstack11l111l1_opy_(cli_context.platform_index)
        cli.bstack1l1l11l11ll_opy_(bstack1l11111l1l_opy_(bstack1ll1111l1_opy_, CONFIG), cli_context.platform_index, bstack1l111lll1_opy_)
        cli.bstack11ll111lll_opy_()
        logger.debug(bstack1l1111l_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨ⭥") + str(cli_context.platform_index) + bstack1l1111l_opy_ (u"ࠣࠤ⭦"))
        return # skip all existing operations
    global bstack11111l11_opy_
    global bstack1llllllll_opy_
    global bstack111l1ll1_opy_
    global bstack1ll11ll1_opy_
    global bstack11111lll_opy_
    global bstack1ll1llll1_opy_
    global bstack11lll11111_opy_
    global bstack1lllllll1_opy_
    global bstack1lllll11_opy_
    global bstack1l1ll111_opy_
    global bstack1l1ll111l1_opy_
    global bstack1llllll11l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11111l11_opy_ = webdriver.Remote.__init__
        bstack1llllllll_opy_ = WebDriver.quit
        bstack11lll11111_opy_ = WebDriver.close
        bstack1lllllll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⭧") in CONFIG or bstack1l1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ⭨") in CONFIG) and bstack11l1l1l11_opy_():
        if bstack111111lll_opy_() < version.parse(bstack111l11l11_opy_):
            logger.error(bstack111111111l_opy_.format(bstack111111lll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1111l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⭩")) and callable(getattr(RemoteConnection, bstack1l1111l_opy_ (u"ࠬࡥࡧࡦࡶࡢࡴࡷࡵࡸࡺࡡࡸࡶࡱ࠭⭪"))):
                    bstack1lllll11_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1lllll11_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1l1l1lllll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1ll111_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1ll111l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warning(bstack1l1111l_opy_ (u"ࠨࠥࡴ࠼ࠣࠩࡸࠨ⭫"), bstack1l1l111l_opy_, str(e))
    try:
        from pytest_bdd import reporting
        bstack1llllll11l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1111l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ⭬"))
    bstack11ll1ll11_opy_ = CONFIG.get(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ⭭"), {}).get(bstack1l1111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⭮"))
    PARALLELISE_VANILLA_PYTHON = True
    bstack111ll1l11_opy_(bstack1l1ll1ll1_opy_)
if (bstack1lllll1111l1_opy_()):
    bstack1l1lllll1ll1_opy_()
@error_handler(class_method=False)
def bstack1ll1111l11l1_opy_(hook_name, event, bstack11l1111l1l1_opy_=None):
    if hook_name not in [bstack1l1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⭯"), bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⭰"), bstack1l1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⭱"), bstack1l1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⭲"), bstack1l1111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⭳"), bstack1l1111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⭴"), bstack1l1111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⭵"), bstack1l1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ⭶")]:
        return
    node = store[bstack1l1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⭷")]
    if hook_name in [bstack1l1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⭸"), bstack1l1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⭹")]:
        node = store[bstack1l1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭⭺")]
    elif hook_name in [bstack1l1111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⭻"), bstack1l1111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⭼")]:
        node = store[bstack1l1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⭽")]
    hook_type = bstack1ll1l1111l11_opy_(hook_name)
    if event == bstack1l1111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⭾"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack1lll1l1l111_opy_ = {
            bstack1l1111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⭿"): uuid,
            bstack1l1111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⮀"): bstack1l111l1ll_opy_(),
            bstack1l1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬ⮁"): bstack1l1111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭⮂"),
            bstack1l1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⮃"): hook_type,
            bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⮄"): hook_name
        }
        store[bstack1l1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⮅")].append(uuid)
        bstack1ll11111l1l1_opy_ = node.nodeid
        if hook_type == bstack1l1111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⮆"):
            if not _1lll1l1l11l_opy_.get(bstack1ll11111l1l1_opy_, None):
                _1lll1l1l11l_opy_[bstack1ll11111l1l1_opy_] = {bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⮇"): []}
            _1lll1l1l11l_opy_[bstack1ll11111l1l1_opy_][bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⮈")].append(bstack1lll1l1l111_opy_[bstack1l1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⮉")])
        _1lll1l1l11l_opy_[bstack1ll11111l1l1_opy_ + bstack1l1111l_opy_ (u"ࠩ࠰ࠫ⮊") + hook_name] = bstack1lll1l1l111_opy_
        bstack1ll11111ll1l_opy_(node, bstack1lll1l1l111_opy_, bstack1l1111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⮋"))
    elif event == bstack1l1111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⮌"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, TestFrameworkState[hook_type], TestHookState.POST, node, None, bstack11l1111l1l1_opy_)
            return
        bstack1lll1llllll_opy_ = node.nodeid + bstack1l1111l_opy_ (u"ࠬ࠳ࠧ⮍") + hook_name
        _1lll1l1l11l_opy_[bstack1lll1llllll_opy_][bstack1l1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⮎")] = bstack1l111l1ll_opy_()
        bstack1l1lllllll11_opy_(_1lll1l1l11l_opy_[bstack1lll1llllll_opy_][bstack1l1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⮏")])
        bstack1ll11111ll1l_opy_(node, _1lll1l1l11l_opy_[bstack1lll1llllll_opy_], bstack1l1111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⮐"), bstack1ll1111l1l11_opy_=bstack11l1111l1l1_opy_)
def bstack1ll111111lll_opy_():
    global bstack1ll11111lll1_opy_
    if bstack11111l111l_opy_():
        bstack1ll11111lll1_opy_ = bstack1l1111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⮑")
    else:
        bstack1ll11111lll1_opy_ = bstack1l1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⮒")
@TestHubHandler.bstack1ll111ll11l1_opy_
def bstack1ll11111111l_opy_():
    bstack1ll111111lll_opy_()
    if cli.is_running():
        try:
            bstack1lll1ll1l111_opy_(bstack1ll1111l11l1_opy_)
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⮓").format(e))
        return
    if bstack11l1l1l11_opy_():
        global_config = Config.bstack111111l1ll_opy_()
        bstack1l1111l_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ⮔")
        if global_config.get_property(bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⮕")):
            if CONFIG.get(bstack1l1111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⮖")) is not None and int(CONFIG[bstack1l1111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⮗")]) > 1:
                bstack11lll1l11_opy_(bstack11ll111l1_opy_)
            return
        bstack11lll1l11_opy_(bstack11ll111l1_opy_)
    try:
        bstack1lll1ll1l111_opy_(bstack1ll1111l11l1_opy_)
    except Exception as e:
        logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⮘").format(e))
bstack1ll11111111l_opy_()