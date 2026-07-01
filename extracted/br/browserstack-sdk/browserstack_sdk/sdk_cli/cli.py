# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import errno
import json
from shutil import which
import subprocess
import threading
import time
from bstack_utils.constants import bstack11lll1l11l1_opy_, bstack1lll1l11111_opy_, bstack1l11l1l1l11_opy_, bstack11lll1lll1l_opy_
import sys
import grpc
import os
import atexit
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.bstack111l1l11l_opy_ import bstack111ll111l_opy_
from browserstack_sdk.sdk_cli.bstack11llll111ll_opy_ import bstack1l11111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l111111lll_opy_ import bstack1l11l1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l111ll1l1l_opy_ import bstack1l1111l1l1l_opy_
from browserstack_sdk.sdk_cli.module_webdriver_test import WebDriverTestModule
from browserstack_sdk.sdk_cli.bstack1l1111l1lll_opy_ import bstack1l11l11l111_opy_
from browserstack_sdk.sdk_cli.bstack11lll1lllll_opy_ import bstack1l11111llll_opy_
from browserstack_sdk.sdk_cli.module_event_dispatcher import EventDispatcherModule
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack111ll11ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l11l111l1l_opy_ import bstack1l1111ll11l_opy_
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
from browserstack_sdk.sdk_cli.bstack11llllll111_opy_ import bstack1l1111lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.custom_tag_manager import CustomTagManager
from browserstack_sdk.sdk_cli.utils.bstack111111ll1l_opy_ import FileUploader
from bstack_utils.helper import Notset, bstack1l11l11ll_opy_, get_cli_dir, bstack1l11l1111_opy_, bstack1llll1l11l1_opy_, bstack1111ll1111_opy_, is_robot_playwright_installed, is_behave_playwright_installed, is_robot_with_playwright, robot_pw_binary_flow, is_raw_robot_pw_binary_flow
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestFrameworkTest, TestHookState, LogEntry
from browserstack_sdk.sdk_cli.automation_framework import AutomationFrameworkBrowser, AutomationFrameworkState, HookState
from bstack_utils.constants import *
from bstack_utils.bstack1lll11111l1_opy_ import bstack11l11111l1_opy_
from bstack_utils import logger_utils
from bstack_utils.performance_tester import PerformanceTester
from bstack_utils.accessibility_scripts import accessibility_scripts
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111111ll1_opy_, bstack1l1llll1l11_opy_
from bstack_utils.performance_tester import PerformanceTester
from browserstack_sdk.sdk_cli.bstack1l111l1111l_opy_ import bstack11llll111l1_opy_
from browserstack_sdk.sdk_cli.behave_framework import BehaveFramework
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
_1l111lll111_opy_ = threading.Lock()
_1l11l111111_opy_ = False
def _1l1111l1111_opy_(reason=None, cause=None):
    global _1l11l111111_opy_
    with _1l111lll111_opy_:
        if _1l11l111111_opy_:
            return
        _1l11l111111_opy_ = True
    lines = [
        bstack1l1llll_opy_ (u"ࠢࠣᛜ"),
        bstack1l1llll_opy_ (u"ࠣ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠦᛝ"),
        bstack1l1llll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡇ࡯࡮ࡢࡴࡼࠤࡈࡒࡉࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣ⠘ࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡧ࡭ࡷ࡫ࡣࡵࠢࡩࡰࡴࡽ࠮ࠡࠤᛞ") +
        bstack1l1llll_opy_ (u"ࠥࡍ࡫ࠦࡳࡥ࡭࠰ࡥࡸࡹࡥࡵࡵ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠦࡩࡴࠢࡥࡰࡴࡩ࡫ࡦࡦࠣࡦࡾࠦࡹࡰࡷࡵࠤ࡫࡯ࡲࡦࡹࡤࡰࡱ࠲ࠠࡸࡪ࡬ࡸࡪࡲࡩࡴࡶࠣ࡭ࡹ࠴ࠢᛟ"),
    ]
    if reason:
        lines.append(bstack1l1llll_opy_ (u"ࠦࡗ࡫ࡡࡴࡱࡱ࠾ࠥࢁࡽࠣᛠ").format(reason))
    if cause is not None:
        lines.append(bstack1l1llll_opy_ (u"ࠧࡉࡡࡶࡵࡨ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧᛡ").format(type(cause).__name__, cause))
    lines.append(bstack1l1llll_opy_ (u"ࠨ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠤᛢ"))
    bstack1l111l1l11l_opy_ = bstack1l1llll_opy_ (u"ࠢ࡝ࡰࠥᛣ").join(lines)
    try:
        print(bstack1l111l1l11l_opy_, file=sys.stderr, flush=True)
    except Exception as ex:
        try:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡻࡦࡸ࡮ࡪࡰࡪࠤࡸࡺࡤࡦࡴࡵࠤࡼࡸࡩࡵࡧࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦᛤ").format(type(ex).__name__, ex))
        except Exception:
            pass
    try:
        logger.warning(bstack1l111l1l11l_opy_)
    except Exception as ex:
        try:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡼࡧࡲ࡯࡫ࡱ࡫ࠥࡲ࡯ࡨࡩࡨࡶ࠳ࡽࡡࡳࡰ࡬ࡲ࡬ࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿ࠽ࠤࢀࢃࠢᛥ").format(type(ex).__name__, ex))
        except Exception:
            pass
def bstack1l11l1ll11l_opy_(bs_config):
    bstack1l111l1l1l1_opy_ = None
    bstack1l11ll11l_opy_ = None
    try:
        bstack1l11ll11l_opy_ = get_cli_dir()
        bstack1l111l1l1l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨᛦ"))
        if not bstack1l111l1l1l1_opy_:
            bstack1l111l1l1l1_opy_ = bstack1l11l1111_opy_(bstack1l11ll11l_opy_)
            bstack11llll11l1l_opy_ = bstack1l11l11ll_opy_(bstack1l111l1l1l1_opy_, bstack1l11ll11l_opy_, bs_config)
            bstack1l111l1l1l1_opy_ = bstack11llll11l1l_opy_ if bstack11llll11l1l_opy_ else bstack1l111l1l1l1_opy_
        if not bstack1l111l1l1l1_opy_:
            raise ValueError(bstack1l1llll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡉࡌࡊࠢࡳࡥࡹ࡮ࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡵࡲࠡ࡫ࡱࠤࡹ࡮ࡥࠡ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡨࡲࡰࡩ࡫ࡲࠣᛧ"))
    except Exception as ex:
        logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡅࡏࡍࠥࡶࡡࡵࡪ࠽ࠤࠧᛨ") + str(ex) + bstack1l1llll_opy_ (u"ࠨࠢᛩ"))
    return bstack1l111l1l1l1_opy_, bstack1l11ll11l_opy_
bstack11llll1l1l1_opy_ = bstack1l1llll_opy_ (u"ࠢ࠺࠻࠼࠽ࠧᛪ")
bstack1l111lllll1_opy_ = bstack1l1llll_opy_ (u"ࠣࡴࡨࡥࡩࡿࠢ᛫")
bstack1l1111l1l11_opy_ = bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨ᛬")
bstack11lllllll1l_opy_ = bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡐࡎ࡙ࡔࡆࡐࡢࡅࡉࡊࡒࠣ᛭")
BROWSERSTACK_AUTOMATION = bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᛮ")
bstack11llllll11l_opy_ = re.compile(bstack1l1llll_opy_ (u"ࡷࠨࠨࡀ࡫ࠬ࠲࠯࠮ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࢁࡈࡓࠪ࠰࠭ࠦᛯ"))
bstack11lll1lll11_opy_ = bstack1l1llll_opy_ (u"ࠨࡤࡦࡸࡨࡰࡴࡶ࡭ࡦࡰࡷࠦᛰ")
bstack1l111llll1l_opy_ = bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡐࡔࡆࡉࡤࡌࡁࡍࡎࡅࡅࡈࡑࠢᛱ")
bstack1l111l111ll_opy_ = [
    Events.bstack1llll1lll1_opy_,
    Events.CONNECT,
    Events.bstack1l1l1111111_opy_,
]
def _11lll11ll1l_opy_():
    bstack1l1llll_opy_ (u"ࠣࠤࠥࡊࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡁࠦ࠱࠺࠰࠷࠲࠵ࠦࡷࡩࡧࡵࡩࠥࡈࡲࡰࡹࡶࡩࡷ࠴ࡥ࡯ࡶࡵࡽ࠳࡭ࡥࡵࡡࡹࡩࡷࡹࡩࡰࡰࡶࠤࡩࡵࡥࡴࡰࠪࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠧࠨࠢᛲ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l111l1l111_opy_ = Path(Browser.__file__).parent / bstack1l1llll_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡴࠥᛳ") / bstack1l1llll_opy_ (u"ࠥࡴࡦࡩ࡫ࡢࡩࡨ࠲࡯ࡹ࡯࡯ࠤᛴ")
        bstack1l11l11lll1_opy_ = json.loads(bstack1l111l1l111_opy_.read_text())
        match = re.search(bstack1l1llll_opy_ (u"ࡶࠧࡢࡤࠬ࡞࠱ࡠࡩ࠱࡜࠯࡞ࡧ࠯ࠧᛵ"), bstack1l11l11lll1_opy_[bstack1l1llll_opy_ (u"ࠧࡪࡥࡱࡧࡱࡨࡪࡴࡣࡪࡧࡶࠦᛶ")][bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᛷ")])
        bstack1l111lll1ll_opy_ = match.group(0) if match else bstack1l1llll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣᛸ")
    except Exception:
        bstack1l111lll1ll_opy_ = bstack1l1llll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ᛹")
    return SimpleNamespace(version=bstack1l111lll1ll_opy_)
class SDKCLI:
    _instance = None
    process: Union[None, Any]
    bstack11lllll1lll_opy_: bool
    bstack11llll1111l_opy_: bool
    bstack1l11l11l11l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l11l1l1l1l_opy_: Union[None, grpc.Channel]
    bstack1l11111111l_opy_: str
    test_framework: TestFramework
    automation_framework: bstack1l111l1l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    event_dispatcher: EventDispatcherModule
    accessibility: bstack111ll111l_opy_
    bstack111111ll1l_opy_: FileUploader
    ai: bstack1l11111ll1l_opy_
    bstack11lll11lll1_opy_: bstack1l11l1l1lll_opy_
    bstack1l11l11l1ll_opy_: List[BaseModule]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack11lll1llll1_opy_: Any
    bstack1l111llll11_opy_: Dict[str, timedelta]
    bstack1l11l1l111l_opy_: str
    async_dispatcher: AsyncDispatcher
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SDKCLI, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        self.process = None
        self.bstack11lllll1lll_opy_ = False
        self.bstack1l11l1l1l1l_opy_ = None
        self.cli_service = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack11lllllll1l_opy_, None)
        self.bstack111l111l1l_opy_ = os.environ.get(bstack1l1111l1l11_opy_, bstack1l1llll_opy_ (u"ࠤࠥ᛺")) == bstack1l1llll_opy_ (u"ࠥࠦ᛻")
        self.bstack11llll1111l_opy_ = False
        self.bstack1l11l11l11l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack11lll1llll1_opy_ = None
        self.test_framework = None
        self.automation_framework = None
        self.bstack1l11111111l_opy_=bstack1l1llll_opy_ (u"ࠦࠧ᛼")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l111llll11_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.async_dispatcher = AsyncDispatcher()
        self.bstack1l11l1l1111_opy_ = False
        self.module_automation_framework = None
        self.module_automation_framework_test = None
        self.event_dispatcher = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l11l11l1ll_opy_ = []
    def bstack111l11l11l_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack1l1llll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᛽"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l111llll1l_opy_, bstack1l1llll_opy_ (u"࠭ࠧ᛾")).lower() in [bstack1l1llll_opy_ (u"ࠧࡵࡴࡸࡩࠬ᛿"), bstack1l1llll_opy_ (u"ࠨ࠳ࠪᜀ"), bstack1l1llll_opy_ (u"ࠩࡼࡩࡸ࠭ᜁ")]:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡴࡸࡣࡪࡰࡪࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡰࡦࡨࠤࡩࡻࡥࠡࡶࡲࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠦᜂ"))
            os.environ[bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᜃ")] = bstack1l1llll_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᜄ")
            return False
        if bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᜅ") in config and str(config[bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᜆ")]).lower() != bstack1l1llll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᜇ"):
            return False
        bstack11lllll1ll1_opy_ = [bstack1l1llll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᜈ"), bstack1l1llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᜉ"), bstack1l1llll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠧᜊ")]
        if robot_pw_binary_flow():
            bstack11lllll1ll1_opy_.append(bstack1l1llll_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦᜋ"))
            bstack11lllll1ll1_opy_.append(bstack1l1llll_opy_ (u"ࠨࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠢᜌ"))
            bstack11lllll1ll1_opy_.append(bstack1l1llll_opy_ (u"ࠢࡱࡣࡥࡳࡹࠨᜍ"))
        if is_behave_playwright_installed():
            bstack11lllll1ll1_opy_.append(bstack1l1llll_opy_ (u"ࠣࡤࡨ࡬ࡦࡼࡥࠣᜎ"))
        bstack1l111l11ll1_opy_ = config.get(bstack1l1llll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᜏ")) in bstack11lllll1ll1_opy_ or os.environ.get(bstack1l1llll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫᜐ")) in bstack11lllll1ll1_opy_
        os.environ[bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᜑ")] = str(bstack1l111l11ll1_opy_) # bstack11llllllll1_opy_ bstack1l1111l111l_opy_ VAR to bstack1l11l111lll_opy_ is binary running
        return bstack1l111l11ll1_opy_
    def bstack1lllllll1l_opy_(self):
        for event in bstack1l111l111ll_opy_:
            bstack111ll1l11_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack111ll1l11_opy_.logger.debug(bstack1l1llll_opy_ (u"ࠧࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠤࡂࡄࠠࡼࡣࡵ࡫ࡸࢃࠠࠣᜒ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠨࠢᜓ"))
            )
        bstack111ll1l11_opy_.register(Events.bstack1llll1lll1_opy_, self.__1l11l11llll_opy_)
        bstack111ll1l11_opy_.register(Events.CONNECT, self.__11lll1l1lll_opy_)
        bstack111ll1l11_opy_.register(Events.bstack1l1l1111111_opy_, self.__11lllllllll_opy_)
        bstack111ll1l11_opy_.register(Events.bstack1lllll1l11l_opy_, self.__1l111ll1lll_opy_)
    def bstack111l1ll11_opy_(self):
        return not self.bstack111l111l1l_opy_ and os.environ.get(bstack1l1111l1l11_opy_, bstack1l1llll_opy_ (u"᜔ࠢࠣ")) != bstack1l1llll_opy_ (u"ࠣࠤ᜕")
    def is_running(self):
        if self.bstack111l111l1l_opy_:
            return self.bstack11lllll1lll_opy_
        else:
            return bool(self.bstack1l11l1l1l1l_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1l1llll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᜖"))
                and self.config_observability.options.allow_screenshots == bstack1l1llll_opy_ (u"ࠪࡸࡷࡻࡥࠨ᜗")
            )
        except Exception:
            return False
    def bstack1l1ll1l1111_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l11l11l1ll_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l11111l111_opy_, stage=STAGE.SINGLE)
    def __1l111ll1111_opy_(self, bstack11lll1l11ll_opy_=10):
        if self.cli_service:
            return
        time_start = datetime.now()
        cli_listen_addr = os.environ.get(bstack11lllllll1l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡠࠨ᜘") + str(id(self)) + bstack1l1llll_opy_ (u"ࠧࡣࠠࡤࡱࡱࡲࡪࡩࡴࡪࡰࡪࠦ᜙"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l1llll_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡡࡳࡶࡴࡾࡹࠣ᜚"), 0), (bstack1l1llll_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡶࡣࡵࡸ࡯ࡹࡻࠥ᜛"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack11lll1l11ll_opy_)
        self.bstack1l11l1l1l1l_opy_ = channel
        self.cli_service = sdk_pb2_grpc.SDKStub(self.bstack1l11l1l1l1l_opy_)
        self.add_benchmark(bstack1l1llll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺࠢ᜜"), datetime.now() - time_start)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack11lllllll1l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧ࠾ࠥ࡯ࡳࡠࡥ࡫࡭ࡱࡪ࡟ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤ᜝") + str(self.bstack111l1ll11_opy_()) + bstack1l1llll_opy_ (u"ࠥࠦ᜞"))
    def __11lllllllll_opy_(self, event_name):
        if self.bstack111l1ll11_opy_():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡄࡎࡌࠦᜟ"))
        self.__1l111ll111l_opy_()
    @measure(event_name=EVENTS.bstack1l11l1111l1_opy_, stage=STAGE.SINGLE)
    def __1l111ll1lll_opy_(self, event_name, bstack11llll1l1ll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1l1llll_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠧᜠ"))
        bstack1l1111ll1l1_opy_ = Path(bstack1l11lll11ll_opy_ (u"ࠨࡻࡴࡧ࡯ࡪ࠳ࡩ࡬ࡪࡡࡧ࡭ࡷࢃ࠯ࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࡴ࠰࡭ࡷࡴࡴࠢᜡ"))
        if self.bstack1l11ll11l_opy_ and bstack1l1111ll1l1_opy_.exists():
            with open(bstack1l1111ll1l1_opy_, bstack1l1llll_opy_ (u"ࠧࡳࠩᜢ"), encoding=bstack1l1llll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᜣ")) as fp:
                data = json.load(fp)
                try:
                    bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᜤ"), bstack11l11111l1_opy_(bstack1111l11lll_opy_), data, {
                        bstack1l1llll_opy_ (u"ࠪࡥࡺࡺࡨࠨᜥ"): (self.config[bstack1l1llll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᜦ")], self.config[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᜧ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1llll1l11_opy_.format(str(e)))
            bstack1l1111ll1l1_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack11llllll1ll_opy_, stage=STAGE.SINGLE)
    def __1l11l11llll_opy_(self, event_name: str, data):
        from bstack_utils.performance_tester import PerformanceTester
        self.bstack1l11111111l_opy_, self.bstack1l11ll11l_opy_ = bstack1l11l1ll11l_opy_(data.bs_config)
        os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡝ࡒࡊࡖࡄࡆࡑࡋ࡟ࡅࡋࡕࠫᜨ")] = self.bstack1l11ll11l_opy_
        if not self.bstack1l11111111l_opy_ or not self.bstack1l11ll11l_opy_:
            raise ValueError(bstack1l1llll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠨᜩ"))
        if self.bstack111l1ll11_opy_():
            self.__11lll1l1lll_opy_(event_name, bstack111ll11ll_opy_())
            return
        try:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡅࡲࡱࡵࡲࡥࡵࡧࠣࡗࡉࡑࠠࡔࡧࡷࡹࡵ࠴ࠢᜪ"))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡿࢂࠨᜫ").format(e))
        start = datetime.now()
        try:
            is_started = self.__1l1111111l1_opy_()
        except Exception as bstack11lll1ll1ll_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡤࡹࡴࡢࡴࡷࠤࡷࡧࡩࡴࡧࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧᜬ").format(type(bstack11lll1ll1ll_opy_).__name__, bstack11lll1ll1ll_opy_))
            _1l1111l1111_opy_(reason=bstack1l1llll_opy_ (u"ࠦࡧ࡯࡮ࡢࡴࡼࠤࡸࡶࡡࡸࡰࠣࡶࡦ࡯ࡳࡦࡦࠥᜭ"), cause=bstack11lll1ll1ll_opy_)
            is_started = False
        self.add_benchmark(bstack1l1llll_opy_ (u"ࠧࡹࡰࡢࡹࡱࡣࡹ࡯࡭ࡦࠤᜮ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l111ll1111_opy_()
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧᜯ"), datetime.now() - start)
            start = datetime.now()
            self.__1l11111l1l1_opy_(data)
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᜰ"), datetime.now() - start)
        else:
            _1l1111l1111_opy_(reason=bstack1l1llll_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡧ࡭ࡩࠦ࡮ࡰࡶࠣࡦࡪࡩ࡯࡮ࡧࠣࡶࡪࡧࡤࡺࠤᜱ"))
    @measure(event_name=EVENTS.bstack1l1111l1ll1_opy_, stage=STAGE.SINGLE)
    def __11lll1l1lll_opy_(self, event_name: str, data: bstack111ll11ll_opy_):
        if not self.bstack111l1ll11_opy_():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᜲ"))
            return
        bin_session_id = os.environ.get(bstack1l1111l1l11_opy_)
        start = datetime.now()
        self.__1l111ll1111_opy_()
        self.add_benchmark(bstack1l1llll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤᜳ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊ᜴ࠢࠥ") + str(bin_session_id) + bstack1l1llll_opy_ (u"ࠧࠨ᜵"))
        start = datetime.now()
        self.__11lll1ll1l1_opy_()
        self.add_benchmark(bstack1l1llll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦ᜶"), datetime.now() - start)
    def __1l111ll1l11_opy_(self):
        if not self.cli_service or not self.cli_bin_session_id:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦ᜷"))
            return
        bstack1l11111l11l_opy_ = {
            bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ᜸"): (bstack1l11l11l111_opy_, bstack1l11111llll_opy_, bstack111ll111_opy_),
            bstack1l1llll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ᜹"): (bstack1l1111l1l1l_opy_, WebDriverTestModule, SeleniumFramework),
        }
        if not self.module_automation_framework and self.session_framework in bstack1l11111l11l_opy_:
            bstack1l111ll11l1_opy_, bstack1l11111ll11_opy_, bstack11lll1l1ll1_opy_ = bstack1l11111l11l_opy_[self.session_framework]
            bstack11llll11lll_opy_ = bstack1l11111ll11_opy_()
            self.module_automation_framework_test = bstack11llll11lll_opy_
            self.module_automation_framework = bstack11lll1l1ll1_opy_
            self.bstack1l11l11l1ll_opy_.append(bstack11llll11lll_opy_)
            self.bstack1l11l11l1ll_opy_.append(bstack1l111ll11l1_opy_(self.module_automation_framework_test))
        if not self.event_dispatcher and self.config_observability and self.config_observability.success:
            self.event_dispatcher = EventDispatcherModule(self.module_automation_framework, self.module_automation_framework_test)
            self.bstack1l11l11l1ll_opy_.append(self.event_dispatcher)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack111ll111l_opy_(self.module_automation_framework, self.module_automation_framework_test)
            self.bstack1l11l11l1ll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l1llll_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧ᜺"), False) == True:
            self.ai = bstack1l11111ll1l_opy_()
            self.bstack1l11l11l1ll_opy_.append(self.ai)
        if not self.percy and self.bstack11lll1llll1_opy_ and self.bstack11lll1llll1_opy_.success:
            self.percy = bstack1l11l1l1lll_opy_(self.bstack11lll1llll1_opy_)
            self.bstack1l11l11l1ll_opy_.append(self.percy)
        for mod in self.bstack1l11l11l1ll_opy_:
            if not mod.bstack1l11l1ll111_opy_():
                mod.configure(self.cli_service, self.config, self.cli_bin_session_id, self.async_dispatcher)
    def __1l111l11l11_opy_(self):
        for mod in self.bstack1l11l11l1ll_opy_:
            if mod.bstack1l11l1ll111_opy_():
                mod.configure(self.cli_service, None, None, None)
    @measure(event_name=EVENTS.bstack1l111ll1ll1_opy_, stage=STAGE.SINGLE)
    def __1l11111l1l1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack11llll1111l_opy_:
            return
        _11llll11l11_opy_ = bstack1l1llll_opy_ (u"ࠫࢀࢃ࠺ࡼࡿ࠽ࡿࢂ࠭᜻").format(os.getpid(), id(self), self.cli_bin_session_id)
        if os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡕࡉࡌࡏࡓࡕࡇࡕࡉࡉ࠭᜼"), bstack1l1llll_opy_ (u"࠭ࠧ᜽")) == _11llll11l11_opy_:
            self.bstack11llll1111l_opy_ = True
            return
        self.__1l111l1l1ll_opy_(data)
        time_start = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l1llll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ᜾")
        req.sdk_language = bstack1l1llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ᜿")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack11llllll11l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            import json as _1lllllll1l1_opy_
            _11llll1ll11_opy_ = _1lllllll1l1_opy_.loads(os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡉࡓࡗ࡝ࡁࡓࡆࡢࡇࡑࡏ࡟ࡂࡔࡊࡗࠬᝀ"), bstack1l1llll_opy_ (u"ࠪ࡟ࡢ࠭ᝁ")))
            if _11llll1ll11_opy_:
                req.cli_args.extend(_11llll1ll11_opy_)
        except Exception as _e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤ࡫ࡵࡲࡸࡣࡵࡨ࡮ࡴࡧࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤ࡮࡬ࠤࡦࡸࡧࡴ࠼ࠣࠦᝂ") + str(_e) + bstack1l1llll_opy_ (u"ࠧࠨᝃ"))
        try:
            req.platform_index = str(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᝄ"), bstack1l1llll_opy_ (u"ࠧ࠱ࠩᝅ")))
            req.client_worker_id = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᝆ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡪࡤࡪࡰࡪࠤࡼࡵࡲ࡬ࡧࡵࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹ࠼ࠣࡿࢂࠨᝇ").format(e))
        try:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡟ࠧᝈ") + str(id(self)) + bstack1l1llll_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᝉ"))
            r = self.cli_service.StartBinSession(req)
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᝊ"), datetime.now() - time_start)
            os.environ[bstack1l1111l1l11_opy_] = r.bin_session_id
            os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡖࡊࡍࡉࡔࡖࡈࡖࡊࡊࠧᝋ")] = bstack1l1llll_opy_ (u"ࠧࡼࡿ࠽ࡿࢂࡀࡻࡾࠩᝌ").format(os.getpid(), id(self), r.bin_session_id)
            self.__1l11111l1ll_opy_(r)
            self.__1l111ll1l11_opy_()
            if not self.bstack1l11l1l1111_opy_:
                self.async_dispatcher.start()
                self.bstack1l11l1l1111_opy_ = True
                atexit.register(self.__1l11l11111l_opy_)
            self.bstack11llll1111l_opy_ = True
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡝ࠥᝍ") + str(id(self)) + bstack1l1llll_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢᝎ"))
        except grpc.FutureTimeoutError as bstack11llll1l111_opy_:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᝏ") + str(bstack11llll1l111_opy_) + bstack1l1llll_opy_ (u"ࠦࠧᝐ"))
            traceback.print_exc()
            raise bstack11llll1l111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᝑ") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢᝒ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1llll_opy_, stage=STAGE.SINGLE)
    def __11lll1ll1l1_opy_(self):
        if not self.bstack111l1ll11_opy_() or not self.cli_bin_session_id or self.bstack1l11l11l11l_opy_:
            return
        time_start = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᝓ"), bstack1l1llll_opy_ (u"ࠨ࠲ࠪ᝔")))
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᝕").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡟ࠧ᝖") + str(id(self)) + bstack1l1llll_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨ᝗"))
            r = self.cli_service.ConnectBinSession(req)
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤ᝘"), datetime.now() - time_start)
            self.__1l11111l1ll_opy_(r)
            self.__1l111ll1l11_opy_()
            if not self.bstack1l11l1l1111_opy_:
                self.async_dispatcher.start()
                self.bstack1l11l1l1111_opy_ = True
                atexit.register(self.__1l11l11111l_opy_)
            self.bstack1l11l11l11l_opy_ = True
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡛ࠣ᝙") + str(id(self)) + bstack1l1llll_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨ᝚"))
        except grpc.FutureTimeoutError as bstack11llll1l111_opy_:
            self.logger.error(bstack1l1llll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ᝛") + str(bstack11llll1l111_opy_) + bstack1l1llll_opy_ (u"ࠤࠥ᝜"))
            traceback.print_exc()
            _1l1111l1111_opy_(reason=bstack1l1llll_opy_ (u"ࠥࡧ࡭࡯࡬ࡥࠢࡦࡳࡳࡴࡥࡤࡶࠣࡸࡴࠦࡢࡪࡰࡤࡶࡾࠦࡴࡪ࡯ࡨࡨࠥࡵࡵࡵࠤ᝝"), cause=bstack11llll1l111_opy_)
            raise bstack11llll1l111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ᝞") + str(e) + bstack1l1llll_opy_ (u"ࠧࠨ᝟"))
            traceback.print_exc()
            _1l1111l1111_opy_(reason=bstack1l1llll_opy_ (u"ࠨࡣࡩ࡫࡯ࡨࠥࡩ࡯࡯ࡰࡨࡧࡹࠦࡴࡰࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡥ࡮ࡲࡥࡥࠤᝠ"), cause=e)
            raise e
    def __1l11111l1ll_opy_(self, r):
        self.bstack11lllll1l11_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l1llll_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᝡ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l1llll_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨᝢ"))
        if r.session_framework in (bstack1l1llll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᝣ"), bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᝤ")):
            self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡨࡶࡨࡿࠠࡪࡵࠣࡷࡪࡴࡴࠡࡱࡱࡰࡾࠦࡡࡴࠢࡳࡥࡷࡺࠠࡰࡨࠣࡸ࡭࡫ࠠࠣࡅࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠱ࠨࠠࡢࡰࡧࠤࡹ࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤ࡮ࡹࠠࡢ࡮ࡶࡳࠥࡻࡳࡦࡦࠣࡦࡾࠦࡓࡵࡣࡵࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡫ࡲࡦࡨࡲࡶࡪ࠲ࠠࡏࡱࡱࡩࠥ࡮ࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡪࡵࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᝥ")
        self.bstack11lll1llll1_opy_ = getattr(r, bstack1l1llll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᝦ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᝧ")] = self.config_testhub.jwt
        os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᝨ")] = self.config_testhub.build_hashed_id
        if self.config.get(bstack1l1llll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦᝩ")) == bstack1l1llll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠥᝪ"):
            if self.config_accessibility and self.config_accessibility.success:
                try:
                    options = self.config_accessibility.options
                    if options:
                        bstack1l11l1ll1l1_opy_ = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᝫ"), bstack1l1llll_opy_ (u"ࠫࢀࢃࠧᝬ")))
                        if options.capabilities:
                            for bstack11lll1lll1_opy_ in options.capabilities:
                                if bstack11lll1lll1_opy_.name == bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪ᝭"):
                                    os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᝮ")] = bstack11lll1lll1_opy_.value
                                    self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡔࡧࡷࠤࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠢࡩࡶࡴࡳࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠢᝯ"))
                                elif bstack11lll1lll1_opy_.name == bstack1l1llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᝰ"):
                                    bstack1l11l1ll1l1_opy_[bstack1l1llll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᝱")] = bstack11lll1lll1_opy_.value
                                    self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡗࡪࡺࠠࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠧᝲ").format(bstack11lll1lll1_opy_.value))
                        os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᝳ")] = json.dumps(bstack1l11l1ll1l1_opy_)
                        if options.scripts:
                            scripts = {script.name: script.command for script in options.scripts}
                            accessibility_scripts.bstack1ll1l1ll1l_opy_(scripts)
                            self.logger.debug(bstack1l1llll_opy_ (u"࡛ࠧࡰࡥࡣࡷࡩࡩࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡴ࡬ࡴࡹࡹ࠺ࠡࡽࢀࠦ᝴").format(list(scripts.keys())))
                        if options.commands_to_wrap and options.commands_to_wrap.commands:
                            commands = [{bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᝵"): cmd.name} for cmd in options.commands_to_wrap.commands]
                            accessibility_scripts.bstack11lll1l1l1l_opy_(commands)
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡖࡲࡧࡥࡹ࡫ࡤࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠠࡤࡱࡰࡱࡦࡴࡤࡴࠤ᝶").format(len(commands)))
                        accessibility_scripts.store()
                except Exception as e:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡾࢁࠧ᝷").format(e))
        if robot_pw_binary_flow():
            bstack11lll11llll_opy_ = json.loads(r.config)
            bstack1l111111l1l_opy_ = bstack11lll11llll_opy_.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭᝸"), {}).get(bstack1l1llll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ᝹"), bstack1l1llll_opy_ (u"ࠫࠬ᝺"))
            os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᝻")] = bstack1l111111l1l_opy_
    def bstack1l11l1l11ll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack11lllll1lll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack11lllll1l1l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack11lllll1l1l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l11l1l11ll_opy_(event_name=EVENTS.bstack1l11111lll1_opy_, stage=STAGE.SINGLE)
    def __1l1111111l1_opy_(self, bstack11lll1l11ll_opy_=10):
        if self.bstack11lllll1lll_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣ᝼"))
            return True
        self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨ᝽"))
        if os.getenv(bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣ᝾")) == bstack11lll1lll11_opy_:
            self.cli_bin_session_id = bstack11lll1lll11_opy_
            self.cli_listen_addr = bstack1l1llll_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧ᝿") % (self.cli_bin_session_id)
            self.bstack11lllll1lll_opy_ = True
            return True
        for attempt in range(1, bstack1l11l1l1l11_opy_ + 1):
            try:
                self.process = subprocess.Popen(
                    [self.bstack1l11111111l_opy_, bstack1l1llll_opy_ (u"ࠥࡷࡩࡱࠢក")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=dict(os.environ),
                    text=True,
                    universal_newlines=True,
                    encoding=bstack1l1llll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥខ"),
                    bufsize=1,
                    close_fds=True,
                )
                break
            except OSError as e:
                bstack1l1111ll111_opy_ = (
                    (hasattr(e, bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡰࡲࠫគ")) and e.errno == getattr(errno, bstack1l1llll_opy_ (u"࠭ࡅࡕ࡚ࡗࡆࡘ࡟ࠧឃ"), 26)) or
                    (hasattr(e, bstack1l1llll_opy_ (u"ࠧࡸ࡫ࡱࡩࡷࡸ࡯ࡳࠩង")) and e.bstack11lll1ll111_opy_ == bstack11lll1l11l1_opy_)
                )
                if bstack1l1111ll111_opy_ and attempt < bstack1l11l1l1l11_opy_:
                    self.logger.warning(
                        bstack1l11lll11ll_opy_ (u"ࠣࡕࡳࡥࡼࡴࠠࡢࡶࡷࡩࡲࡶࡴࠡࡽࡤࡸࡹ࡫࡭ࡱࡶࢀ࠳ࢀࡓࡁ࡙ࡡࡖࡔࡆ࡝ࡎࡠࡔࡈࡘࡗࡏࡅࡔࡿࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨࠡࡤࡸࡷࡾࠦࡥࡳࡴࡲࡶ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡ࡫ࡱࠤࢀ࡙ࡐࡂ࡙ࡑࡣࡗࡋࡔࡓ࡛ࡢࡈࡊࡒࡁ࡚ࡡࡖࢁࡸࡀࠠࡼࡧࢀࠦច")
                    )
                    time.sleep(bstack11lll1lll1l_opy_)
                else:
                    raise
        bstack11llll11ll1_opy_ = dict(os.environ)
        if bstack1l1llll_opy_ (u"ࠩࡊࡖࡕࡉ࡟ࡗࡇࡕࡆࡔ࡙ࡉࡕ࡛ࠪឆ") not in bstack11llll11ll1_opy_:
            bstack11llll11ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡋࡗࡖࡃࡠࡘࡈࡖࡇࡕࡓࡊࡖ࡜ࠫជ")] = bstack1l1llll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪឈ")
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡡࡇࡓࡒࡆࡣࡋࡏࡘ࡞ࠢࡖࡩࡹࠦࡇࡓࡒࡆࡣ࡛ࡋࡒࡃࡑࡖࡍ࡙࡟࠽ࡆࡔࡕࡓࡗࠦࡴࡰࠢࡶࡹࡵࡶࡲࡦࡵࡶࠤ࡫ࡵࡲ࡬ࠢࡺࡥࡷࡴࡩ࡯ࡩࡶࠦញ"))
        else:
            logger.debug(bstack1l1llll_opy_ (u"ࠨ࡛ࡈࡔࡓࡇࡤࡌࡉ࡙࡟ࠣࡋࡗࡖࡃࡠࡘࡈࡖࡇࡕࡓࡊࡖ࡜ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡷࡳ࠿ࠦࡻࡾࠤដ").format(bstack11llll11ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡈࡔࡓࡇࡤ࡜ࡅࡓࡄࡒࡗࡎ࡚࡙ࠨឋ")]))
        self.process = subprocess.Popen(
            [self.bstack1l11111111l_opy_, bstack1l1llll_opy_ (u"ࠣࡵࡧ࡯ࠧឌ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=bstack11llll11ll1_opy_,
            text=True,
            universal_newlines=True, # bstack1l1111111ll_opy_ compat for text=True in bstack1l1111ll1ll_opy_ python
            encoding=bstack1l1llll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣឍ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l111l111l1_opy_ = threading.Thread(target=self.__11llllll1l1_opy_, args=(bstack11lll1l11ll_opy_,))
        bstack1l111l111l1_opy_.start()
        bstack1l111l111l1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡶࡴࡦࡽ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࢀࠤࡴࡻࡴ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡵࡷࡨࡴࡻࡴ࠯ࡴࡨࡥࡩ࠮ࠩࡾࠢࡨࡶࡷࡃࠢណ") + str(self.process.stderr.read()) + bstack1l1llll_opy_ (u"ࠦࠧត"))
        if not self.bstack11lllll1lll_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡡࠢថ") + str(id(self)) + bstack1l1llll_opy_ (u"ࠨ࡝ࠡࡥ࡯ࡩࡦࡴࡵࡱࠤទ"))
            self.__1l111ll111l_opy_()
        self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡰࡳࡱࡦࡩࡸࡹ࡟ࡳࡧࡤࡨࡾࡀࠠࠣធ") + str(self.bstack11lllll1lll_opy_) + bstack1l1llll_opy_ (u"ࠣࠤន"))
        return self.bstack11lllll1lll_opy_
    def __11llllll1l1_opy_(self, bstack1l1111llll1_opy_=10):
        bstack1l111ll11ll_opy_ = time.time()
        while self.process and time.time() - bstack1l111ll11ll_opy_ < bstack1l1111llll1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l1llll_opy_ (u"ࠤ࡬ࡨࡂࠨប") in line:
                    self.cli_bin_session_id = line.split(bstack1l1llll_opy_ (u"ࠥ࡭ࡩࡃࠢផ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡨࡲࡩࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠥព") + str(self.cli_bin_session_id) + bstack1l1llll_opy_ (u"ࠧࠨភ"))
                    continue
                if bstack1l1llll_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢម") in line:
                    self.cli_listen_addr = line.split(bstack1l1llll_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣយ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡥ࡯࡭ࡤࡲࡩࡴࡶࡨࡲࡤࡧࡤࡥࡴ࠽ࠦរ") + str(self.cli_listen_addr) + bstack1l1llll_opy_ (u"ࠤࠥល"))
                    continue
                if bstack1l1llll_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤវ") in line:
                    port = line.split(bstack1l1llll_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥឝ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡶ࡯ࡳࡶ࠽ࠦឞ") + str(port) + bstack1l1llll_opy_ (u"ࠨࠢស"))
                    continue
                if line.strip() == bstack1l111lllll1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l1llll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡉࡐࡡࡖࡘࡗࡋࡁࡎࠤហ"), bstack1l1llll_opy_ (u"ࠣ࠳ࠥឡ")) == bstack1l1llll_opy_ (u"ࠤ࠴ࠦអ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack11lllll1lll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳ࠼ࠣࠦឣ") + str(e) + bstack1l1llll_opy_ (u"ࠦࠧឤ"))
        return False
    def __1l11l11111l_opy_(self):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡳࡻࡰࠡࡪࡤࡲࡩࡲࡥࡳࠢࡩࡳࡷࠦࡡࡴࡻࡱࡧࡤࡪࡩࡴࡲࡤࡸࡨ࡮ࡥࡳ࠮ࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡡࡵࡧࡻ࡭ࡹࠦࡴࡰࠢࡨࡲࡸࡻࡲࡦࠢࡷࡥࡸࡱࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠦࠧࠨឥ")
        if self.async_dispatcher and self.bstack1l11l1l1111_opy_:
            try:
                self.async_dispatcher.stop()
                self.bstack1l11l1l1111_opy_ = False
            except Exception as e:
                self.logger.debug(
                    bstack1l1llll_opy_ (u"ࠨ࡟ࡠࡥ࡯ࡩࡦࡴࡵࡱࡡࡤࡷࡾࡴࡣࡠࡦ࡬ࡷࡵࡧࡴࡤࡪࡨࡶ࠿ࠦࡻࡾ࠼ࠣࡿࢂࠨឦ").format(type(e).__name__, e),
                )
    @measure(event_name=EVENTS.bstack1l111111l11_opy_, stage=STAGE.SINGLE)
    def __1l111ll111l_opy_(self):
        if self.bstack1l11l1l1l1l_opy_:
            if self.async_dispatcher and self.bstack1l11l1l1111_opy_:
                try:
                    atexit.unregister(self.__1l11l11111l_opy_)
                except ValueError:
                    pass
                self.async_dispatcher.stop()
                self.bstack1l11l1l1111_opy_ = False
            start = datetime.now()
            _1l11l1lll11_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡢࡇࡔࡕࡒࡅࡡࡇࡍࡗ࠭ឧ"), bstack1l1llll_opy_ (u"ࠨࠩឨ"))
            _11lllll11l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡤࡉࡏࡐࡔࡇࡣࡐࡋ࡙ࡠࡊࡄࡗࡍ࠭ឩ"), bstack1l1llll_opy_ (u"ࠪࠫឪ"))
            _11llll1l11l_opy_ = self.bstack111l111l1l_opy_ and bool(_1l11l1lll11_opy_) and bool(_11lllll11l1_opy_)
            if _11llll1l11l_opy_:
                try:
                    from browserstack_sdk import _1l1l1lll1l1_opy_, _1l1l111l1l_opy_
                    _1l1l1lll1l1_opy_(bstack111ll11111_opy_=_1l11l1lll11_opy_, bstack1l111l1lll_opy_=_11lllll11l1_opy_, bstack1llllllll11_opy_=max(90, _1l1l111l1l_opy_))
                except Exception as _e:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠦ࡫ࡵ࡬࡭ࡱࡺࡩࡷࠦࡤࡳࡣ࡬ࡲࠥࡽࡡࡪࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢឫ").format(_e))
            _11lll1l111l_opy_ = (not self.bstack111l111l1l_opy_) and bool(_1l11l1lll11_opy_) and bool(_11lllll11l1_opy_)
            if not _11lll1l111l_opy_ and self.bstack1l11l11ll1l_opy_():
                self.cli_bin_session_id = None
                self.add_benchmark(bstack1l1llll_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤឬ"), datetime.now() - start)
                if _11llll1l11l_opy_:
                    from browserstack_sdk import _1l1l11ll1l1_opy_
                    time.sleep(_1l1l11ll1l1_opy_)
            self.__1l111l11l11_opy_()
            start = datetime.now()
            random_label = PerformanceTester.mark_start(bstack1l1llll_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࠦឭ"))
            self.bstack1l11l1l1l1l_opy_.close()
            PerformanceTester.end(bstack1l1llll_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࠧឮ"), random_label+bstack1l1llll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣឯ"), random_label+bstack1l1llll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢឰ"), True, None, None, None, None)
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧឱ"), datetime.now() - start)
            self.bstack1l11l1l1l1l_opy_ = None
        if self.process:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡸࡺ࡯ࡱࠤឲ"))
            start = datetime.now()
            random_label = PerformanceTester.mark_start(bstack1l1llll_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡫ࡪ࡮࡯ࠦឳ"))
            self.process.terminate()
            try:
                self.process.wait(timeout=60)
            except subprocess.TimeoutExpired:
                try:
                    self.process.kill()
                    self.process.wait(timeout=5)
                except Exception as _e:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾࠦࡳࡶࡤࡳࡶࡴࡩࡥࡴࡵࠣࡪࡴࡸࡣࡦ࠯࡮࡭ࡱࡲࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦ឴").format(_e))
            except Exception as _e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿࠠࡴࡷࡥࡴࡷࡵࡣࡦࡵࡶࠤࡼࡧࡩࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨ឵").format(_e))
            PerformanceTester.end(bstack1l1llll_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡮࡭ࡱࡲࠢា"), random_label+bstack1l1llll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤិ"), random_label+bstack1l1llll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣី"), True, None, None, None, None)
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢឹ"), datetime.now() - start)
            self.process = None
            if self.bstack111l111l1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1lll11l1l_opy_()
                self.logger.info(
                    bstack1l1llll_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠧឺ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬុ")] = self.config_testhub.build_hashed_id
            elif not self.bstack111l111l1l_opy_:
                _11lll1l1111_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬូ"), bstack1l1llll_opy_ (u"ࠨࠩួ"))
                if _11lll1l1111_opy_:
                    self.logger.info(
                        bstack1l1llll_opy_ (u"ࠤ࡙࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤើ").format(
                            _11lll1l1111_opy_
                        )
                    )
            if self.bstack111l111l1l_opy_ and self.config_accessibility and self.config_accessibility.success and self.config_testhub:
                bstack1l111l1ll11_opy_ = isinstance(self.config, dict) and self.config.get(bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࠧឿ")) is not None
                if not bstack1l111l1ll11_opy_:
                    self.logger.info(
                        bstack1l1llll_opy_ (u"࡛ࠦ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦࡦ࠰ࡸࡪࡹࡴࡴ࠱ࡳࡶࡴࡰࡥࡤࡶࡶ࠳ࡵ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡢ࠰࠳ࡂࡸ࡭ࡈࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡶ࡯ࡳࡶ࠱ࡠࡳࠨៀ").format(
                            self.config_testhub.build_hashed_id
                        )
                    )
        self.bstack11lllll1lll_opy_ = False
    def __1l111l1l1ll_opy_(self, data):
        _1l1111l11ll_opy_ = is_raw_robot_pw_binary_flow()
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1l1llll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤេ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1lll11_opy_ = get_pw_version()
            except Exception:
                bstack1l1lll11_opy_ = _11lll11ll1l_opy_()
            data.framework_versions[bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥែ")] = bstack1l1lll11_opy_.version
        elif _1l1111l11ll_opy_:
            try:
                from playwright._repo_version import __version__
                bstack1l111lll1ll_opy_ = __version__
            except Exception:
                bstack1l111lll1ll_opy_ = _11lll11ll1l_opy_().version
            data.framework_versions[bstack1l1llll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦៃ")] = bstack1l111lll1ll_opy_
            data.frameworks.append(bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧោ"))
        elif data.test_framework == bstack1l1llll_opy_ (u"ࠤࡥࡩ࡭ࡧࡶࡦࠤៅ"):
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢំ")] = __version__
                data.frameworks.append(bstack1l1llll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣះ"))
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠥࡈࡩ࡯ࡣࡵࡽࠥࡌ࡬ࡰࡹ࠽ࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡷࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧៈ"))
            except ImportError:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠦࡂࡪࡰࡤࡶࡾࠦࡆ࡭ࡱࡺࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠯ࠤࡧࡻࡴࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡡࡤ࡭ࡤ࡫ࡪࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤ៉"))
        else:
            bstack1l111111111_opy_ = False
            try:
                import pytest_playwright
                bstack1l111111111_opy_ = True
            except ImportError:
                pass
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࡮ࡳࡰࡰࡴࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤ࠭ࡴ࡯࡯࠯ࡌࡱࡵࡵࡲࡵࡇࡵࡶࡴࡸࠩ࠻ࠢࡾࢁࠧ៊").format(e))
            bstack1l111111ll1_opy_ = None
            try:
                from playwright._repo_version import __version__ as _1l111l11111_opy_
                bstack1l111111ll1_opy_ = _1l111l11111_opy_
            except ImportError:
                pass
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࡥࡲࡦࡲࡲࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡯࡭ࡱࡱࡵࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥ࠮࡮ࡰࡰ࠰ࡍࡲࡶ࡯ࡳࡶࡈࡶࡷࡵࡲࠪ࠼ࠣࡿࢂࠨ់").format(e))
            if bstack1l111111111_opy_ and bstack1l111111ll1_opy_ is not None:
                data.framework_versions[bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ៌")] = bstack1l111111ll1_opy_
                data.frameworks.append(bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ៍"))
                self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡩ࡫ࡴࡦࡥࡷࡩࡩࠦࡰࡺࡶࡨࡷࡹ࠱ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠾ࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡴ࠿ࡾࢁࠧ៎").format(data.frameworks))
            else:
                try:
                    import selenium
                    data.framework_versions[bstack1l1llll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ៏")] = selenium.__version__
                    data.frameworks.append(bstack1l1llll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣ័"))
                except ImportError:
                    pass
                except Exception as e:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢ࡬ࡱࡵࡵࡲࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࠫࡲࡴࡴ࠭ࡊ࡯ࡳࡳࡷࡺࡅࡳࡴࡲࡶ࠮ࡀࠠࡼࡿࠥ៑").format(e))
                if bstack1l111111ll1_opy_ is not None:
                    data.framework_versions[bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ្ࠧ")] = bstack1l111111ll1_opy_
                    data.frameworks.append(bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ៓"))
            if not data.frameworks or data.frameworks == [data.test_framework]:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠥࡒࡴࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡤࡦࡶࡨࡧࡹ࡫ࡤࠡࠪࡳࡽࡹ࡫ࡳࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡥࡩ࡯ࡵࡷࡥࡱࡲࡥࡥ࠿ࠨࡷ࠱ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡢࡴࡰ࡭࡟ࡷࡧࡵࡷ࡮ࡵ࡮࠾ࠧࡶ࠰ࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪ࡯ࡳࡳࡷࡺࡥࡥ࠿ࠨࡷ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵࡀࠩࡸ࠯ࠠ⠕ࠢࡥ࡭ࡳࡧࡲࡺࠢࡺ࡭ࡱࡲࠠࡳࡧ࡭ࡩࡨࡺࠠࡢࡵࠣࠫࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪࠤࡺࡴ࡬ࡦࡵࡶࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡩࡴࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠩࡶࠤࡕࡿࡴࡩࡱࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠰ࠥ។"), bstack1l111111111_opy_, bstack1l111111ll1_opy_, bstack1l1llll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭៕") in data.frameworks, list(data.frameworks))
    def bstack11lllllll11_opy_(self, hub_url: str, platform_index: int, bstack1llll11ll11_opy_: Any):
        if self.automation_framework:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤ៖"))
            return
        try:
            time_start = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l1llll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣៗ")
            self.automation_framework = SeleniumFramework(
                cli.config.get(bstack1l1llll_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢ៘"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l11l11l1l1_opy_={bstack1l1llll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧ៙"): bstack1llll11ll11_opy_}
            )
            def bstack1l111l11lll_opy_(self):
                return
            if self.config.get(bstack1l1llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦ៚"), True):
                Service.start = bstack1l111l11lll_opy_
                Service.stop = bstack1l111l11lll_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(FileUploader.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(CustomTagManager.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦ៛"), datetime.now() - time_start)
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥៜ") + str(e) + bstack1l1llll_opy_ (u"ࠧࠨ៝"))
    def bstack1ll1111l11l_opy_(self, platform_index: int):
        if self.automation_framework:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧ៞"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import Browser
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l11l1l11l1_opy_
                bstack11lllll1111_opy_ = [BrowserType, Browser, BrowserContext, Connection]
                _1l11l11ll11_opy_ = None
                _1l11l111l11_opy_ = []
                for _path in (bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࡸࡿ࡮ࡤࡡࡤࡴ࡮࠭៟"), bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࡥࡩ࡮ࡲ࡯࠲ࡤࡧ࡮ࡥࡴࡲ࡭ࡩ࠭០"), bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠴ࡳࡺࡰࡦࡣࡦࡶࡩ࠯ࡡࡪࡩࡳ࡫ࡲࡢࡶࡨࡨࠬ១")):
                    try:
                        _1l1111lll11_opy_ = __import__(_path, fromlist=[bstack1l1llll_opy_ (u"ࠪࡅࡳࡪࡲࡰ࡫ࡧࠫ២")])
                        _1l11l11ll11_opy_ = getattr(_1l1111lll11_opy_, bstack1l1llll_opy_ (u"ࠫࡆࡴࡤࡳࡱ࡬ࡨࠬ៣"), None)
                        if _1l11l11ll11_opy_ is not None:
                            self.logger.info(bstack1l1llll_opy_ (u"ࠧࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡄࡲࡩࡸ࡯ࡪࡦࠣࡧࡱࡧࡳࡴࠢࡩࡳࡺࡴࡤࠡࡣࡷࠤࢀࢃࠢ៤").format(_path))
                            break
                        _1l11l111l11_opy_.append(bstack1l1llll_opy_ (u"ࠨࡻࡾ࠼ࠣࡱࡴࡪࡵ࡭ࡧࠣࡰࡴࡧࡤࡦࡦࠣࡦࡺࡺࠠࡂࡰࡧࡶࡴ࡯ࡤࠡࡣࡷࡸࡷ࡯ࡢࡶࡶࡨࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ៥").format(_path))
                    except Exception as _e:
                        _1l11l111l11_opy_.append(bstack1l1llll_opy_ (u"ࠢࡼࡿ࠽ࠤࢀࢃࠢ៦").format(_path, _e))
                if _1l11l11ll11_opy_ is not None:
                    bstack11lllll1111_opy_.append(_1l11l11ll11_opy_)
                else:
                    _1l11l1111ll_opy_ = (
                        self.logger.error if is_robot_with_playwright()
                        and not is_robot_playwright_installed()
                        else self.logger.warning
                    )
                    _11lllll11ll_opy_ = (
                        bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠳ࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࡮ࡰࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡤࡦࡱ࡫ࠠࡧࡴࡲࡱࠥࡧ࡮ࡺࠢ࡮ࡲࡴࡽ࡮ࠡࡲࡤࡸ࡭ࡁࠠࠣ៧")
                        + bstack1l1llll_opy_ (u"ࠤࡓ࡛ࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦࡨࡰࡱ࡮ࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡕࡴ࡬ࡩࡩࡀࠠࡼࡿ࠱ࠤࠧ៨")
                        + bstack1l1llll_opy_ (u"ࠥࡍ࡫ࠦࡹࡰࡷࠣࡥࡷ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡴࡤࡻࠥࡘ࡯ࡣࡱࡷ࠯ࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠬࡃࡱࡨࡷࡵࡩࡥ࠮ࠣࠦ៩")
                        + bstack1l1llll_opy_ (u"ࠦࡹ࡮ࡩࡴࠢࡇࡍࡘࡇࡂࡍࡇࡖࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡥࡤࡴࡹࡻࡲࡦࠢ࠰ࠤࠧ៪")
                        + bstack1l1llll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡸ࡫࡯ࡰࠥࡧࡰࡱࡧࡤࡶࠥࡧࡳࠡࠩࡨࡼࡹ࡫ࡲ࡯ࡣ࡯ࠤ࡬ࡸࡩࡥࠩࠣࡳࡳࠦࡔࡓࡃ࠱ࠤࡕ࡯࡮ࠡࡣࠣࠦ៫")
                        + bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡺࡪࡸࡳࡪࡱࡱࠤࡹ࡮ࡡࡵࠢࡨࡼࡵࡵࡲࡵࡵࠣࡅࡳࡪࡲࡰ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢࡲࡲࡪࠦ࡯ࡧࠢࠥ៬")
                        + bstack1l1llll_opy_ (u"ࠢࡵࡪࡨࠤࡰࡴ࡯ࡸࡰࠣࡴࡦࡺࡨࡴ࠰ࠥ៭")
                    )
                    _1l11l1111ll_opy_(_11lllll11ll_opy_.format(bstack1l1llll_opy_ (u"ࠨ࠽ࠣࠫ៮").join(_1l11l111l11_opy_)))
                self.automation_framework = bstack111ll111_opy_(
                    platform_index,
                    framework_name=bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ៯"),
                    framework_version=__version__,
                    classes=bstack11lllll1111_opy_,
                )
                try:
                    from playwright.sync_api import Page, Browser
                    for _11lllll111l_opy_ in (Page, Browser, BrowserContext):
                        if not hasattr(_11lllll111l_opy_, bstack1l1llll_opy_ (u"ࠥࡷࡪࡺ࡟ࡤࡷࡶࡸࡴࡳ࡟ࡵࡣࡪࠦ៰")):
                            _11lllll111l_opy_.set_custom_tag = staticmethod(CustomTagManager.set_custom_tag)
                except Exception as _e:
                    self.logger.warning(bstack1l1llll_opy_ (u"ࠦࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣ࡫ࡱࡨࠥࡹࡥࡵࡡࡦࡹࡸࡺ࡯࡮ࡡࡷࡥ࡬ࠦࡴࡰࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡣ࡭ࡣࡶࡷࡪࡹ࠺ࠡࡽࢀࠦ៱").format(_e))
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except Exception:
                    get_pw_version = _11lll11ll1l_opy_
                from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance
                bstack1l1lll11_opy_ = get_pw_version()
                self.automation_framework = bstack111ll111_opy_(
                    platform_index,
                    framework_name=bstack1l1llll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ៲"),
                    framework_version=bstack1l1lll11_opy_.version,
                    classes=[],
                )
                ctx = TrackedInstance.create_context(self.automation_framework)
                bstack1l111l1l_opy_.instances[ctx.id] = AutomationFrameworkBrowser(
                    ctx, bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ៳"), bstack1l1lll11_opy_, AutomationFrameworkState.CREATE
                )
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࡼࡿࠥ៴").format(e))
    def bstack1ll11l111_opy_(self, framework_name: str = None):
        if self.test_framework:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦ៵"))
            return
        if robot_pw_binary_flow():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack11llll111l1_opy_({ bstack1l1llll_opy_ (u"ࠤࡵࡳࡧࡵࡴ࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ៶"): VERSION }, [bstack1l1llll_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࠤ៷")], self.async_dispatcher, self.cli_service)
                self.logger.info(bstack1l1llll_opy_ (u"ࠦࡗࡵࡢࡰࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࠫࡺࢀࢃࠩࠣ៸").format(VERSION))
                return
            except Exception as e:
                self.logger.error(bstack1l1llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡳࡱࡥࡳࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂࠨ៹").format(e))
        if framework_name == bstack1l1llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭៺"):
            try:
                import behave as _11lllll1_opy_
                bstack1ll111lll1l_opy_ = getattr(_11lllll1_opy_, bstack1l1llll_opy_ (u"ࠧࡠࡡࡹࡩࡷࡹࡩࡰࡰࡢࡣࠬ៻"), None)
                if bstack1ll111lll1l_opy_ is None:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡄࡨ࡬ࡦࡼࡥࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࡀࠦࡵࡴ࡫ࡱ࡫ࠥࡪࡥࡧࡣࡸࡰࡹࠦࡶࡦࡴࡶ࡭ࡴࡴࠠ࠲࠰࠵࠲࠻ࠨ៼"))
                    bstack1ll111lll1l_opy_ = bstack1l1llll_opy_ (u"ࠩ࠴࠲࠷࠴࠶ࠨ៽")
                self.test_framework = BehaveFramework({bstack1l1llll_opy_ (u"ࠥࡦࡪ࡮ࡡࡷࡧࠥ៾"): bstack1ll111lll1l_opy_}, [bstack1l1llll_opy_ (u"ࠦࡧ࡫ࡨࡢࡸࡨࠦ៿")], self.async_dispatcher, self.cli_service)
                self.logger.info(bstack1l1llll_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧࠤ࠭ࡼࡻࡾࠫࠥ᠀").format(bstack1ll111lll1l_opy_))
                return
            except Exception as e:
                self.logger.error(bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠾ࠥࠨ᠁") + str(e) + bstack1l1llll_opy_ (u"ࠢࠣ᠂"))
        bstack1l11l1l1ll1_opy_ = framework_name
        if bstack1l11l1l1ll1_opy_ == bstack1l1llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ᠃"):
            import sys
            python_version = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠳ࢁࡽ࠯ࡽࢀࠦ᠄").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            self.test_framework = bstack1l1111lllll_opy_(
                test_framework_versions={bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ᠅"): python_version},
                test_frameworks=[bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬ᠆")],
                async_dispatcher=self.async_dispatcher,
                cli_service=self.cli_service
            )
            self.logger.info(bstack1l1llll_opy_ (u"ࠧࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡬࡯ࡳࠢࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠣࡸࡪࡹࡴࡴࠤ᠇"))
            return
        if bstack1llll1l11l1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l1llll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨ᠈"): pytest.__version__ }, [bstack1l1llll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ᠉")], self.async_dispatcher, self.cli_service)
            self.logger.info(bstack1l1llll_opy_ (u"ࠣࡒࡼࡸࡪࡹࡴࡃࡆࡇࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࠬࡻࢁࡽࠪࠤ᠊").format(pytest.__version__))
            return
        try:
            import pytest
            self.test_framework = bstack1l1111ll11l_opy_({ bstack1l1llll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤ᠋"): pytest.__version__ }, [bstack1l1llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥ᠌")], self.async_dispatcher, self.cli_service)
            self.logger.info(bstack1l1llll_opy_ (u"ࠦࡕࡿࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࠬࡻࢁࡽࠪࠤ᠍").format(pytest.__version__))
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤ᠎") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢ᠏"))
        self.bstack1l111l1ll1l_opy_()
    def bstack1l111l1ll1l_opy_(self):
        if not self.bstack111l11l11l_opy_():
            return
        bstack1l111l1ll1_opy_ = None
        def bstack1l1lll11l11_opy_(config, startdir):
            return bstack1l1llll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧ᠐").format(bstack1l1llll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ᠑"))
        def bstack111l11lll1_opy_():
            return
        def bstack11111l1ll1_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l1llll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩ᠒"):
                return bstack1l1llll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤ᠓")
            else:
                return bstack1l111l1ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l111l1ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l1lll11l11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l11lll1_opy_
            Config.getoption = bstack11111l1ll1_opy_
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨ᠔") + str(e) + bstack1l1llll_opy_ (u"ࠧࠨ᠕"))
    def bstack1l1111lll1l_opy_(self):
        bstack1ll11l11l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll11l11l1_opy_, dict):
            if cli.config_observability:
                bstack1ll11l11l1_opy_.update(
                    {bstack1l1llll_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨ᠖"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥ᠗") in accessibility.get(bstack1l1llll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤ᠘"), {}):
                    bstack11llll1lll1_opy_ = accessibility.get(bstack1l1llll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥ᠙"))
                    bstack11llll1lll1_opy_.update({ bstack1l1llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦ᠚"): bstack11llll1lll1_opy_.pop(bstack1l1llll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢ᠛")) })
                bstack1ll11l11l1_opy_.update({bstack1l1llll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧ᠜"): accessibility })
        return bstack1ll11l11l1_opy_
    def _1l111llllll_opy_(self, entries):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡴࡤࡦࡴࠣࡩࡳࡪ࠭ࡰࡨ࠰ࡦࡺ࡯࡬ࡥࠢࡦࡹࡸࡺ࡯࡮ࡧࡵ࠱ࡻ࡯ࡳࡪࡤ࡯ࡩࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡥ࡯ࡶࡵ࡭ࡪࡹࠠࡰࡰࠣࡸ࡭࡫ࠠࡤࡷࡶࡸࡴࡳࡥࡳࠩࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡳ࡯࡬ࡲࡦࡲ࠮ࠡࡇࡱࡸࡷ࡯ࡥࡴࠢࡦࡳࡲ࡫ࠠࡪࡰ࡯࡭ࡳ࡫ࠠࡰࡰࠣࡸ࡭࡫ࠠࡔࡶࡲࡴࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮ࡓࡧࡶࡴࡴࡴࡳࡦ࠮ࠣࡷࡴࠦ࡮ࡰࠌࠣࠤࠥࠦࠠࠡࠢࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥ࡮ࡡࡻࡣࡵࡨࠥ࡫ࡸࡪࡵࡷࡷࠥ࠮ࡡࡵࡱࡰ࡭ࡨࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡢࡪࡰࡤࡶࡾࠦࡳࡪࡦࡨ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡧࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡸ࡯ࡵࡱࠣࡧࡴࡴࡴࡳࡣࡦࡸࠥ࠮ࡃࡶࡵࡷࡳࡲ࡫ࡲࡗ࡫ࡶ࡭ࡧࡲࡥࡔࡷࡰࡱࡦࡸࡹࡆࡰࡷࡶࡾࠦࡩ࡯ࠢࡶࡨࡰ࠴ࡰࡳࡱࡷࡳ࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥ࡯ࡴࡦࡴࡤࡸࡪࠦࡢࡺࠢࡣࡷࡪࡼࡥࡳ࡫ࡷࡽࡥࠦࠫࠡࡢࡥࡳࡩࡿࡠࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡷࡳ࡫ࡷࡩࠥࡦࡢࡰࡦࡼࡤࠥࡼࡥࡳࡤࡤࡸ࡮ࡳࠠࠩࡤ࡬ࡲࡦࡸࡹࠡࡱࡺࡲࡸࠦࡴࡩࡧࠣࡴࡷࡵࡳࡦ࠮ࠣ࡭ࡳࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡢࡰࡺࠣࡦࡴࡸࡤࡦࡴࡶ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡧ࡭ࡵ࡯ࡴࡧࠣࡷࡹࡸࡥࡢ࡯ࠣࡦࡾࠦࡠࡴࡧࡹࡩࡷ࡯ࡴࡺࡢ࠽ࠤࡼࡧࡲ࡯࠱ࡺࡥࡷࡴࡩ࡯ࡩ࠲ࡩࡷࡸ࡯ࡳࠢ࠰ࡂࠥࡹࡴࡥࡧࡵࡶ࠱ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡼࡥࡳࡻࡷ࡬࡮ࡴࡧࠡࡧ࡯ࡷࡪࠦࠨࡪࡰࡩࡳࠥࡇࡎࡅࠢࡸࡲࡰࡴ࡯ࡸࡰ࠲ࡩࡲࡶࡴࡺ࠱ࡷࡽࡵࡵࠩࠡ࠯ࡁࠤࡸࡺࡤࡰࡷࡷࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡝ࡥࠡࡷࡶࡩࠥࡶࡲࡪࡰࡷࠬ࠮ࠦࡤࡪࡴࡨࡧࡹࡲࡹࠡࡶࡲࠤࡧࡿࡰࡢࡵࡶࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡲ࡯ࡨࡩࡨࡶࠬࡹࠠࡱࡧࡵ࠱ࡱ࡯࡮ࡦࠢࡳࡶࡪ࡬ࡩࡹࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡴࡸ࡭ࡢࡶࡷࡩࡷ࠲ࠠࡸࡪ࡬ࡧ࡭ࠦࡷࡰࡷ࡯ࡨࠥࡶࡲࡦࡨ࡬ࡼࠥࡵ࡮࡭ࡻࠣࡸ࡭࡫ࠠࡧ࡫ࡵࡷࡹࠦ࡬ࡪࡰࡨࠤࡴ࡬ࠠࡢࠢࡰࡹࡱࡺࡩ࠮࡮࡬ࡲࡪࠦࡢࡰࡦࡼࠎࠥࠦࠠࠡࠢࠣࠤࠥࡧ࡮ࡥࠢࡥࡶࡪࡧ࡫ࠡࡶ࡫ࡩࠥࡨࡩ࡯ࡣࡵࡽࠬࡹࠠࡣࡱࡻ࠱ࡧࡵࡲࡥࡧࡵࠤࡦࡲࡩࡨࡰࡰࡩࡳࡺ࠮ࠡࡕࡨࡺࡪࡸࡩࡵࡻ࠰ࡶࡴࡻࡴࡦࡦࠣࡷࡹࡸࡥࡢ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡰ࡫ࡥࡱࡵࠣࡇࡎࠦࡴࡰࡱ࡯࡭ࡳ࡭ࠠࠩࡹ࡫࡭ࡨ࡮ࠠࡵࡴࡨࡥࡹࡹࠠࡴࡶࡧࡩࡷࡸࠠࡸࡴ࡬ࡸࡪࡹࠠࡢࡵࠣࡪࡦ࡯࡬ࡶࡴࡨ࠱ࡸ࡯ࡧ࡯ࡣ࡯࠭ࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡲࡡࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࡥࡱࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡥ࡮ࡲࡵࡳࡧ࠰ࡸࡴࡲࡥࡳࡣࡱࡸ࠿ࠦࡡ࡯ࡻࠣࡩࡷࡸ࡯ࡳࠢ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡷࡼࡧ࡬࡭ࡱࡺࡩࡩࠦࠨࡪࡰࡦࡰࡺࡪࡩ࡯ࡩࠣࡥࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦ࡯ࡧࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡪࡰࡱࡩࡷࠦ࡬ࡰࡩࡪࡩࡷ࠴ࡤࡦࡤࡸ࡫ࠥ࡯ࡴࡴࡧ࡯ࡪ࠱ࠦࡳࡪࡰࡦࡩࠥࡹࡴࡥࡱࡸࡸ࠴ࡹࡴࡥࡧࡵࡶࠥࡳࡡࡺࠢࡥࡩࠥࡩ࡬ࡰࡵࡨࡨࠥࡨࡹࠡࡶ࡫ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࠤ࡭ࡧࡲ࡯ࡧࡶࡷࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡹࡨࡶࡶࡧࡳࡼࡴࠩࠡࡵࡲࠤ࡮ࡺࠠ࡯ࡧࡹࡩࡷࠦࡢࡳࡧࡤ࡯ࡸࠦࡳࡩࡷࡷࡨࡴࡽ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᠝")
        if not entries:
            return
        try:
            for entry in entries:
                body = getattr(entry, bstack1l1llll_opy_ (u"ࠧࡣࡱࡧࡽࠬ᠞"), bstack1l1llll_opy_ (u"ࠨࠩ᠟")) or bstack1l1llll_opy_ (u"ࠩࠪᠠ")
                if not body:
                    continue
                bstack1l11l111ll1_opy_ = (getattr(entry, bstack1l1llll_opy_ (u"ࠪࡷࡪࡼࡥࡳ࡫ࡷࡽࠬᠡ"), bstack1l1llll_opy_ (u"ࠫࠬᠢ")) or bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᠣ")).lower()
                stream = sys.stderr if bstack1l11l111ll1_opy_ in (bstack1l1llll_opy_ (u"࠭ࡷࡢࡴࡱࠫᠤ"), bstack1l1llll_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᠥ"), bstack1l1llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᠦ")) else sys.stdout
                print(body, file=stream)
        except Exception as err:
            try:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤ࡞ࡧࡺࡹࡴࡰ࡯ࡨࡶ࠲ࡼࡩࡴ࡫ࡥࡰࡪ࠳ࡳࡶ࡯ࡰࡥࡷࡿ࡝ࠡࡴࡨࡲࡩ࡫ࡲࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࠨࡷࠧᠧ"), err)
            except Exception:
                pass
    @measure(event_name=EVENTS.bstack1l111lll1l1_opy_, stage=STAGE.SINGLE)
    def bstack1l11l11ll1l_opy_(self, exit_signal: str = None, exit_reason: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.cli_service:
            return
        time_start = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᠨ"), bstack1l1llll_opy_ (u"ࠫ࠵࠭ᠩ")))
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᠪ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if exit_signal:
            req.exit_signal = exit_signal
        if exit_reason:
            req.exit_reason = exit_reason
        try:
            r = self.cli_service.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.add_benchmark(bstack1l1llll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺ࡯ࡱࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᠫ"), datetime.now() - time_start)
            self._1l111llllll_opy_(r.entries)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def add_benchmark(self, key: str, value: timedelta):
        tag = bstack1l1llll_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᠬ") if self.bstack111l1ll11_opy_() else bstack1l1llll_opy_ (u"ࠣ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᠭ")
        self.bstack1l111llll11_opy_[bstack1l1llll_opy_ (u"ࠤ࠽ࠦᠮ").join([tag + bstack1l1llll_opy_ (u"ࠥ࠱ࠧᠯ") + str(id(self)), key])] += value
    def bstack1l1lll11l1l_opy_(self):
        if not os.getenv(bstack1l1llll_opy_ (u"ࠦࡉࡋࡂࡖࡉࡢࡔࡊࡘࡆࠣᠰ"), bstack1l1llll_opy_ (u"ࠧ࠶ࠢᠱ")) == bstack1l1llll_opy_ (u"ࠨ࠱ࠣᠲ"):
            return
        bstack1l111l1lll1_opy_ = dict()
        instances = []
        if self.test_framework:
            instances.extend(list(self.test_framework.instances.values()))
        if self.automation_framework:
            instances.extend(list(self.automation_framework.instances.values()))
        for instance in instances:
            if not instance.platform_index in bstack1l111l1lll1_opy_:
                bstack1l111l1lll1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l111l1lll1_opy_[instance.platform_index]
            for k, v in instance.bstack1l1111l11l1_opy_().items():
                report[k] += v
                report[k.split(bstack1l1llll_opy_ (u"ࠢ࠻ࠤᠳ"))[0]] += v
        bstack1l111l1llll_opy_ = sorted([(k, v) for k, v in self.bstack1l111llll11_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack11lll1l1l11_opy_ = 0
        for r in bstack1l111l1llll_opy_:
            bstack1l111lll11l_opy_ = r[1].total_seconds()
            bstack11lll1l1l11_opy_ += bstack1l111lll11l_opy_
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࢁࡲ࡜࠲ࡠࢁࡂࠨᠴ") + str(bstack1l111lll11l_opy_) + bstack1l1llll_opy_ (u"ࠤࠥᠵ"))
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࠱࠲ࠨᠶ"))
        bstack11llll1ll1l_opy_ = []
        for platform_index, report in bstack1l111l1lll1_opy_.items():
            bstack11llll1ll1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack11llll1ll1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1ll11ll1_opy_ = set()
        bstack1l11l1ll1ll_opy_ = 0
        for r in bstack11llll1ll1l_opy_:
            bstack1l111lll11l_opy_ = r[2].total_seconds()
            bstack1l11l1ll1ll_opy_ += bstack1l111lll11l_opy_
            bstack1ll11ll1_opy_.add(r[0])
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࢀࡸ࡛࠱࡟ࢀ࠾ࢀࡸ࡛࠲࡟ࢀࡁࠧᠷ") + str(bstack1l111lll11l_opy_) + bstack1l1llll_opy_ (u"ࠧࠨᠸ"))
        if self.bstack111l1ll11_opy_():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࠭࠮ࠤᠹ"))
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࢀࡺ࡯ࡵࡣ࡯ࡣࡨࡲࡩࡾࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ࠰ࡿࡸࡺࡲࠩࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠭ࢂࡃࠢᠺ") + str(bstack1l11l1ll1ll_opy_) + bstack1l1llll_opy_ (u"ࠣࠤᠻ"))
        else:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࠨᠼ") + str(bstack11lll1l1l11_opy_) + bstack1l1llll_opy_ (u"ࠥࠦᠽ"))
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦ࠲࠳ࠢᠾ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᠿ"), bstack1l1llll_opy_ (u"࠭࠰ࠨᡀ"))),
            client_worker_id=bstack1l1llll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᡁ").format(threading.get_ident(), os.getpid())
        )
        if not self.cli_service:
            self.logger.error(bstack1l1llll_opy_ (u"ࠣࡥ࡯࡭ࡤࡹࡥࡳࡸ࡬ࡧࡪࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲ࠥࡉࡡ࡯ࡰࡲࡸࠥࡶࡥࡳࡨࡲࡶࡲࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᡂ"))
            return None
        response = self.cli_service.TestOrchestration(request)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࠭ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠭ࡴࡧࡶࡷ࡮ࡵ࡮࠾ࡽࢀࠦᡃ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack11lllll1l11_opy_(self, r):
        if r is not None and getattr(r, bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࠫᡄ"), None) and getattr(r.testhub, bstack1l1llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᡅ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l1llll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᡆ")))
            framework = (os.environ.get(bstack1l1llll_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧᡇ"), bstack1l1llll_opy_ (u"ࠧࠨᡈ")) or
                         os.environ.get(bstack1lll1l11111_opy_, bstack1l1llll_opy_ (u"ࠨࠩᡉ"))).lower()
            is_behave = bstack1l1llll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᡊ") in framework
            bstack11lll1ll11l_opy_ = {bstack1l1llll_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡌࡒ࡛ࡇࡌࡊࡆࡢࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࠨᡋ")}
            bstack11llll11111_opy_ = False
            for bstack1l111l11l1l_opy_, err in errors.items():
                if err[bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩᡌ")] == bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᡍ"):
                    self.logger.info(err[bstack1l1llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᡎ")])
                else:
                    self.logger.error(err[bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᡏ")])
                    if is_behave and bstack1l111l11l1l_opy_ in bstack11lll1ll11l_opy_:
                        print(err[bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡐ")], flush=True)
                        bstack11llll11111_opy_ = True
            if bstack11llll11111_opy_:
                self.logger.error(bstack1l1llll_opy_ (u"ࠤࡄࡦࡴࡸࡴࡪࡰࡪࠤࡇ࡫ࡨࡢࡸࡨࠤࡘࡊࡋࠡࡵࡷࡥࡷࡺࡵࡱࠢࡧࡹࡪࠦࡴࡰࠢࡩࡥࡹࡧ࡬ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡨࡶࡷࡵࡲ࠯ࠤᡑ"))
                sys.exit(1)
    def bstack1ll1ll1ll1_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()