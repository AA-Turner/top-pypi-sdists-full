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
import json
import subprocess
import threading
import time
import sys
import grpc
import os
import atexit
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l11llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1l1l_opy_ import bstack1l1llll1111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1l1l1_opy_ import bstack1l1l1111lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11l11l_opy_ import bstack1l11llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1l11l_opy_ import bstack1l11llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll111ll_opy_ import bstack1l11l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l1ll_opy_ import bstack1l11ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1111l1_opy_ import bstack1l11lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack11ll1llll_opy_ import bstack111111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l111_opy_ import bstack1ll1l1l111_opy_, Events, bstack1ll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11l1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l1l1_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import bstack11ll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll11l1l_opy_ import bstack1l11l11ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l11lllllll_opy_ import bstack1l1l111111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11lll1_opy_ import bstack11lll1ll1_opy_
from bstack_utils.helper import Notset, bstack1ll1l111l1l_opy_, get_cli_dir, bstack1ll1l11l11l_opy_, bstack1ll1l1llll_opy_, bstack111l1l1ll1_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l111llll11_opy_, TestHookState, bstack1llll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import bstack1l1ll1ll111_opy_, bstack11l111l1l_opy_, bstack1111111ll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l11111l_opy_ import bstack11111l1ll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111111l1l_opy_, bstack1l1llllll_opy_
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111ll1l_opy_ import bstack1l1l11l1l11_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1l1l11lll11_opy_(bs_config):
    bstack1l11l111lll_opy_ = None
    bstack1ll1l11l1l1_opy_ = None
    try:
        bstack1ll1l11l1l1_opy_ = get_cli_dir()
        bstack1l11l111lll_opy_ = os.environ.get(bstack111ll11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨᒌ"))
        if not bstack1l11l111lll_opy_:
            bstack1l11l111lll_opy_ = bstack1ll1l11l11l_opy_(bstack1ll1l11l1l1_opy_)
            bstack1l1l1ll1l1l_opy_ = bstack1ll1l111l1l_opy_(bstack1l11l111lll_opy_, bstack1ll1l11l1l1_opy_, bs_config)
            bstack1l11l111lll_opy_ = bstack1l1l1ll1l1l_opy_ if bstack1l1l1ll1l1l_opy_ else bstack1l11l111lll_opy_
        if not bstack1l11l111lll_opy_:
            raise ValueError(bstack111ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡉࡌࡊࠢࡳࡥࡹ࡮ࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡵࡲࠡ࡫ࡱࠤࡹ࡮ࡥࠡ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡨࡲࡰࡩ࡫ࡲࠣᒍ"))
    except Exception as ex:
        logger.error(bstack111ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡅࡏࡍࠥࡶࡡࡵࡪ࠽ࠤࠧᒎ") + str(ex) + bstack111ll11_opy_ (u"ࠨࠢᒏ"))
    return bstack1l11l111lll_opy_, bstack1ll1l11l1l1_opy_
bstack1l1l11111ll_opy_ = bstack111ll11_opy_ (u"ࠢ࠺࠻࠼࠽ࠧᒐ")
bstack1l11ll1lll1_opy_ = bstack111ll11_opy_ (u"ࠣࡴࡨࡥࡩࡿࠢᒑ")
bstack1l11lllll1l_opy_ = bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᒒ")
bstack1l1l111ll11_opy_ = bstack111ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡐࡎ࡙ࡔࡆࡐࡢࡅࡉࡊࡒࠣᒓ")
BROWSERSTACK_AUTOMATION = bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᒔ")
bstack1l1l1lll11l_opy_ = re.compile(bstack111ll11_opy_ (u"ࡷࠨࠨࡀ࡫ࠬ࠲࠯࠮ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࢁࡈࡓࠪ࠰࠭ࠦᒕ"))
bstack1l1l1l11lll_opy_ = bstack111ll11_opy_ (u"ࠨࡤࡦࡸࡨࡰࡴࡶ࡭ࡦࡰࡷࠦᒖ")
bstack1l1l1ll111l_opy_ = bstack111ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡐࡔࡆࡉࡤࡌࡁࡍࡎࡅࡅࡈࡑࠢᒗ")
bstack1l11l11l111_opy_ = [
    Events.bstack111ll1llll_opy_,
    Events.CONNECT,
    Events.bstack11ll111ll1_opy_,
]
def _1l1l11ll1ll_opy_():
    bstack111ll11_opy_ (u"ࠣࠤࠥࡊࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡁࠦ࠱࠺࠰࠷࠲࠵ࠦࡷࡩࡧࡵࡩࠥࡈࡲࡰࡹࡶࡩࡷ࠴ࡥ࡯ࡶࡵࡽ࠳࡭ࡥࡵࡡࡹࡩࡷࡹࡩࡰࡰࡶࠤࡩࡵࡥࡴࡰࠪࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠧࠨࠢᒘ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l1l1111l11_opy_ = Path(Browser.__file__).parent / bstack111ll11_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡴࠥᒙ") / bstack111ll11_opy_ (u"ࠥࡴࡦࡩ࡫ࡢࡩࡨ࠲࡯ࡹ࡯࡯ࠤᒚ")
        bstack1l1l11l1111_opy_ = json.loads(bstack1l1l1111l11_opy_.read_text())
        match = re.search(bstack111ll11_opy_ (u"ࡶࠧࡢࡤࠬ࡞࠱ࡠࡩ࠱࡜࠯࡞ࡧ࠯ࠧᒛ"), bstack1l1l11l1111_opy_[bstack111ll11_opy_ (u"ࠧࡪࡥࡱࡧࡱࡨࡪࡴࡣࡪࡧࡶࠦᒜ")][bstack111ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᒝ")])
        bstack1l11l1l1lll_opy_ = match.group(0) if match else bstack111ll11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣᒞ")
    except Exception:
        bstack1l11l1l1lll_opy_ = bstack111ll11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤᒟ")
    return SimpleNamespace(version=bstack1l11l1l1lll_opy_)
class SDKCLI:
    _1l1lllll111_opy_ = None
    process: Union[None, Any]
    bstack1l11l1l11ll_opy_: bool
    bstack1l11lll1l1l_opy_: bool
    bstack1l1l11l111l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l11lll111l_opy_: Union[None, grpc.Channel]
    bstack1l11l11lll1_opy_: str
    test_framework: TestFramework
    bstack1ll111l111_opy_: bstack11ll11l1l1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1111ll1_opy_: bstack111111l11l_opy_
    accessibility: bstack1l1llll1111_opy_
    bstack1lll11lll1_opy_: bstack11lll1ll1_opy_
    ai: bstack1l1l1111lll_opy_
    bstack1l11lll1111_opy_: bstack1l11llllll1_opy_
    bstack1l11llll111_opy_: List[bstack1l11llll11l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l1l11ll11l_opy_: Any
    bstack1l1l11l11l1_opy_: Dict[str, timedelta]
    bstack1l1l1ll1ll1_opy_: str
    bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_
    def __new__(cls):
        if not cls._1l1lllll111_opy_:
            cls._1l1lllll111_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1l1lllll111_opy_
    def __init__(self):
        self.process = None
        self.bstack1l11l1l11ll_opy_ = False
        self.bstack1l11lll111l_opy_ = None
        self.bstack1l1l1l1l1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l1l111ll11_opy_, None)
        self.bstack1l1l111lll1_opy_ = os.environ.get(bstack1l11lllll1l_opy_, bstack111ll11_opy_ (u"ࠤࠥᒠ")) == bstack111ll11_opy_ (u"ࠥࠦᒡ")
        self.bstack1l11lll1l1l_opy_ = False
        self.bstack1l1l11l111l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l1l11ll11l_opy_ = None
        self.test_framework = None
        self.bstack1ll111l111_opy_ = None
        self.bstack1l11l11lll1_opy_=bstack111ll11_opy_ (u"ࠦࠧᒢ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l1l11l11l1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1l1lll11l1l_opy_ = bstack1l1lll11l11_opy_()
        self.bstack1l11l11ll11_opy_ = False
        self.bstack1l1l1ll11ll_opy_ = None
        self.bstack1l11l1l111l_opy_ = None
        self.bstack1ll1111ll1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l11llll111_opy_ = []
    def bstack11lll11l11_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack111ll11_opy_ (u"ࠧࡺࡲࡶࡧࠥᒣ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l1l1ll111l_opy_, bstack111ll11_opy_ (u"࠭ࠧᒤ")).lower() in [bstack111ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬᒥ"), bstack111ll11_opy_ (u"ࠨ࠳ࠪᒦ"), bstack111ll11_opy_ (u"ࠩࡼࡩࡸ࠭ᒧ")]:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡊࡴࡸࡣࡪࡰࡪࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡰࡦࡨࠤࡩࡻࡥࠡࡶࡲࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠦᒨ"))
            os.environ[bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᒩ")] = bstack111ll11_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᒪ")
            return False
        if bstack111ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᒫ") in config and str(config[bstack111ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᒬ")]).lower() != bstack111ll11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᒭ"):
            return False
        bstack1l11ll111l1_opy_ = [bstack111ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᒮ"), bstack111ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᒯ"), bstack111ll11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠧᒰ")]
        if is_robot_playwright_installed():
            bstack1l11ll111l1_opy_.append(bstack111ll11_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦᒱ"))
            bstack1l11ll111l1_opy_.append(bstack111ll11_opy_ (u"ࠨࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠢᒲ"))
        bstack1l11l11llll_opy_ = config.get(bstack111ll11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᒳ")) in bstack1l11ll111l1_opy_ or os.environ.get(bstack111ll11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩᒴ")) in bstack1l11ll111l1_opy_
        os.environ[bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᒵ")] = str(bstack1l11l11llll_opy_) # bstack1l1l1l1l111_opy_ bstack1l11l1llll1_opy_ VAR to bstack1l11ll11111_opy_ is binary running
        return bstack1l11l11llll_opy_
    def bstack1l11ll1l_opy_(self):
        for event in bstack1l11l11l111_opy_:
            bstack1ll1l1l111_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1ll1l1l111_opy_.logger.debug(bstack111ll11_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨᒶ") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧᒷ"))
            )
        bstack1ll1l1l111_opy_.register(Events.bstack111ll1llll_opy_, self.__1l1l1l1llll_opy_)
        bstack1ll1l1l111_opy_.register(Events.CONNECT, self.__1l1l11lllll_opy_)
        bstack1ll1l1l111_opy_.register(Events.bstack11ll111ll1_opy_, self.__1l11l111l11_opy_)
        bstack1ll1l1l111_opy_.register(Events.bstack1llllll1111_opy_, self.__1l11l1lll1l_opy_)
    def bstack11l1l1l11_opy_(self):
        return not self.bstack1l1l111lll1_opy_ and os.environ.get(bstack1l11lllll1l_opy_, bstack111ll11_opy_ (u"ࠧࠨᒸ")) != bstack111ll11_opy_ (u"ࠨࠢᒹ")
    def is_running(self):
        if self.bstack1l1l111lll1_opy_:
            return self.bstack1l11l1l11ll_opy_
        else:
            return bool(self.bstack1l11lll111l_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack111ll11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᒺ"))
                and self.config_observability.options.allow_screenshots == bstack111ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᒻ")
            )
        except Exception:
            return False
    def bstack1l11ll11l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l11llll111_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l11ll11lll_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l1l1lll1ll_opy_(self, bstack1l1l1ll1lll_opy_=10):
        if self.bstack1l1l1l1l1l_opy_:
            return
        bstack111l1lllll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l1l111ll11_opy_, self.cli_listen_addr)
        self.logger.debug(bstack111ll11_opy_ (u"ࠤ࡞ࠦᒼ") + str(id(self)) + bstack111ll11_opy_ (u"ࠥࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡯࡮ࡨࠤᒽ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack111ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶ࡟ࡱࡴࡲࡼࡾࠨᒾ"), 0), (bstack111ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡴࡡࡳࡶࡴࡾࡹࠣᒿ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1l1ll1lll_opy_)
        self.bstack1l11lll111l_opy_ = channel
        self.bstack1l1l1l1l1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l11lll111l_opy_)
        self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࠧᓀ"), datetime.now() - bstack111l1lllll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l1l111ll11_opy_] = self.cli_listen_addr
        self.logger.debug(bstack111ll11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥ࠼ࠣ࡭ࡸࡥࡣࡩ࡫࡯ࡨࡤࡶࡲࡰࡥࡨࡷࡸࡃࠢᓁ") + str(self.bstack11l1l1l11_opy_()) + bstack111ll11_opy_ (u"ࠣࠤᓂ"))
    def __1l11l111l11_opy_(self, event_name):
        if self.bstack11l1l1l11_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡉࡌࡊࠤᓃ"))
        self.__1l11lllll11_opy_()
    @measure(event_name=EVENTS.bstack1l1l11l1ll1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l11l1lll1l_opy_(self, event_name, bstack1l11ll1ll11_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack111ll11_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠥᓄ"))
        bstack1l1l1l111l1_opy_ = Path(bstack1l1ll1111ll_opy_ (u"ࠦࢀࡹࡥ࡭ࡨ࠱ࡧࡱ࡯࡟ࡥ࡫ࡵࢁ࠴ࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࡹ࠮࡫ࡵࡲࡲࠧᓅ"))
        if self.bstack1ll1l11l1l1_opy_ and bstack1l1l1l111l1_opy_.exists():
            with open(bstack1l1l1l111l1_opy_, bstack111ll11_opy_ (u"ࠬࡸࠧᓆ"), encoding=bstack111ll11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᓇ")) as fp:
                data = json.load(fp)
                try:
                    bstack111l1l1ll1_opy_(bstack111ll11_opy_ (u"ࠧࡑࡑࡖࡘࠬᓈ"), bstack11111l1ll_opy_(bstack1111l1lll_opy_), data, {
                        bstack111ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᓉ"): (self.config[bstack111ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᓊ")], self.config[bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᓋ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1llllll_opy_.format(str(e)))
            bstack1l1l1l111l1_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l11ll1l111_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l1l1l1llll_opy_(self, event_name: str, data):
        from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
        self.bstack1l11l11lll1_opy_, self.bstack1ll1l11l1l1_opy_ = bstack1l1l11lll11_opy_(data.bs_config)
        os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡛ࡗࡏࡔࡂࡄࡏࡉࡤࡊࡉࡓࠩᓌ")] = self.bstack1ll1l11l1l1_opy_
        if not self.bstack1l11l11lll1_opy_ or not self.bstack1ll1l11l1l1_opy_:
            raise ValueError(bstack111ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡩࡧࠣࡗࡉࡑࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠦᓍ"))
        if self.bstack11l1l1l11_opy_():
            self.__1l1l11lllll_opy_(event_name, bstack1ll1l1l1ll_opy_())
            return
        try:
            logger.debug(bstack111ll11_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧᓎ"))
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦᓏ").format(e))
        start = datetime.now()
        is_started = self.__1l1l1lll1l1_opy_()
        self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧᓐ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l1l1lll1ll_opy_()
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᓑ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1l1l11111_opy_(data)
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᓒ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1l1l11l11_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l1l11lllll_opy_(self, event_name: str, data: bstack1ll1l1l1ll_opy_):
        if not self.bstack11l1l1l11_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᓓ"))
            return
        bin_session_id = os.environ.get(bstack1l11lllll1l_opy_)
        start = datetime.now()
        self.__1l1l1lll1ll_opy_()
        self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᓔ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧᓕ") + str(bin_session_id) + bstack111ll11_opy_ (u"ࠢࠣᓖ"))
        start = datetime.now()
        self.__1l11l1l11l1_opy_()
        self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᓗ"), datetime.now() - start)
    def __1l1l1l11l1l_opy_(self):
        if not self.bstack1l1l1l1l1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack111ll11_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨᓘ"))
            return
        bstack1l11l11l1l1_opy_ = {
            bstack111ll11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᓙ"): (bstack1l11ll1llll_opy_, bstack1l11lll1l11_opy_, bstack111ll11111_opy_),
            bstack111ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᓚ"): (bstack1l11llll1ll_opy_, bstack1l11l1ll111_opy_, bstack1l11l11111l_opy_),
        }
        if not self.bstack1l1l1ll11ll_opy_ and self.session_framework in bstack1l11l11l1l1_opy_:
            bstack1l11l1111ll_opy_, bstack1l111llllll_opy_, bstack1l1l111l111_opy_ = bstack1l11l11l1l1_opy_[self.session_framework]
            bstack1l1l11111l1_opy_ = bstack1l111llllll_opy_()
            self.bstack1l11l1l111l_opy_ = bstack1l1l11111l1_opy_
            self.bstack1l1l1ll11ll_opy_ = bstack1l1l111l111_opy_
            self.bstack1l11llll111_opy_.append(bstack1l1l11111l1_opy_)
            self.bstack1l11llll111_opy_.append(bstack1l11l1111ll_opy_(self.bstack1l11l1l111l_opy_))
        if not self.bstack1ll1111ll1_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1ll1111ll1_opy_ = bstack111111l11l_opy_(self.bstack1l1l1ll11ll_opy_, self.bstack1l11l1l111l_opy_)
            self.bstack1l11llll111_opy_.append(self.bstack1ll1111ll1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l1llll1111_opy_(self.bstack1l1l1ll11ll_opy_, self.bstack1l11l1l111l_opy_)
            self.bstack1l11llll111_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack111ll11_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢᓛ"), False) == True:
            self.ai = bstack1l1l1111lll_opy_()
            self.bstack1l11llll111_opy_.append(self.ai)
        if not self.percy and self.bstack1l1l11ll11l_opy_ and self.bstack1l1l11ll11l_opy_.success:
            self.percy = bstack1l11llllll1_opy_(self.bstack1l1l11ll11l_opy_)
            self.bstack1l11llll111_opy_.append(self.percy)
        for mod in self.bstack1l11llll111_opy_:
            if not mod.bstack1l11ll1l11l_opy_():
                mod.configure(self.bstack1l1l1l1l1l_opy_, self.config, self.cli_bin_session_id, self.bstack1l1lll11l1l_opy_)
    def __1l1l11l1lll_opy_(self):
        for mod in self.bstack1l11llll111_opy_:
            if mod.bstack1l11ll1l11l_opy_():
                mod.configure(self.bstack1l1l1l1l1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l11lll11l1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l1l1l11111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l11lll1l1l_opy_:
            return
        self.__1l11ll1l1ll_opy_(data)
        bstack111l1lllll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack111ll11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᓜ")
        req.sdk_language = bstack111ll11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᓝ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l1l1lll11l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᓞ"), bstack111ll11_opy_ (u"ࠩ࠳ࠫᓟ")))
            req.client_worker_id = bstack111ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᓠ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡷࡰࡴ࡮ࡩࡷࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥ࡯࡮ࡥࡧࡻ࠾ࠥࢁࡽࠣᓡ").format(e))
        try:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡡࠢᓢ") + str(id(self)) + bstack111ll11_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓣ"))
            r = self.bstack1l1l1l1l1l_opy_.StartBinSession(req)
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᓤ"), datetime.now() - bstack111l1lllll_opy_)
            os.environ[bstack1l11lllll1l_opy_] = r.bin_session_id
            self.__1l1l1lll111_opy_(r)
            self.__1l1l1l11l1l_opy_()
            if not self.bstack1l11l11ll11_opy_:
                self.bstack1l1lll11l1l_opy_.start()
                self.bstack1l11l11ll11_opy_ = True
                atexit.register(self.__1l1l1l111ll_opy_)
            self.bstack1l11lll1l1l_opy_ = True
            self.logger.debug(bstack111ll11_opy_ (u"ࠣ࡝ࠥᓥ") + str(id(self)) + bstack111ll11_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢᓦ"))
        except grpc.bstack1l1l1ll1l11_opy_ as bstack1l11llll1l1_opy_:
            self.logger.error(bstack111ll11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᓧ") + str(bstack1l11llll1l1_opy_) + bstack111ll11_opy_ (u"ࠦࠧᓨ"))
            traceback.print_exc()
            raise bstack1l11llll1l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᓩ") + str(e) + bstack111ll11_opy_ (u"ࠨࠢᓪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1l1l11_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l11l1l11l1_opy_(self):
        if not self.bstack11l1l1l11_opy_() or not self.cli_bin_session_id or self.bstack1l1l11l111l_opy_:
            return
        bstack111l1lllll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᓫ"), bstack111ll11_opy_ (u"ࠨ࠲ࠪᓬ")))
        req.client_worker_id = bstack111ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᓭ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥ࡟ࠧᓮ") + str(id(self)) + bstack111ll11_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᓯ"))
            r = self.bstack1l1l1l1l1l_opy_.ConnectBinSession(req)
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᓰ"), datetime.now() - bstack111l1lllll_opy_)
            self.__1l1l1lll111_opy_(r)
            self.__1l1l1l11l1l_opy_()
            if not self.bstack1l11l11ll11_opy_:
                self.bstack1l1lll11l1l_opy_.start()
                self.bstack1l11l11ll11_opy_ = True
                atexit.register(self.__1l1l1l111ll_opy_)
            self.bstack1l1l11l111l_opy_ = True
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࠣᓱ") + str(id(self)) + bstack111ll11_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨᓲ"))
        except grpc.bstack1l1l1ll1l11_opy_ as bstack1l11llll1l1_opy_:
            self.logger.error(bstack111ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᓳ") + str(bstack1l11llll1l1_opy_) + bstack111ll11_opy_ (u"ࠤࠥᓴ"))
            traceback.print_exc()
            raise bstack1l11llll1l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᓵ") + str(e) + bstack111ll11_opy_ (u"ࠦࠧᓶ"))
            traceback.print_exc()
            raise e
    def __1l1l1lll111_opy_(self, r):
        self.bstack1l11ll11ll1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack111ll11_opy_ (u"ࠧࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᓷ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack111ll11_opy_ (u"ࠨࡥ࡮ࡲࡷࡽࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡯ࡶࡰࡧࠦᓸ"))
        if r.session_framework in (bstack111ll11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᓹ"), bstack111ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᓺ")):
            self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᓻ")
        self.bstack1l1l11ll11l_opy_ = getattr(r, bstack111ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᓼ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᓽ")] = self.config_testhub.jwt
        os.environ[bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᓾ")] = self.config_testhub.build_hashed_id
        if self.config.get(bstack111ll11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤᓿ")) == bstack111ll11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠣᔀ"):
            if self.config_accessibility and self.config_accessibility.success:
                try:
                    options = self.config_accessibility.options
                    if options:
                        bstack1l1l111llll_opy_ = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᔁ"), bstack111ll11_opy_ (u"ࠩࡾࢁࠬᔂ")))
                        if options.capabilities:
                            for bstack1lllll1l1l1_opy_ in options.capabilities:
                                if bstack1lllll1l1l1_opy_.name == bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᔃ"):
                                    os.environ[bstack111ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᔄ")] = bstack1lllll1l1l1_opy_.value
                                    self.logger.debug(bstack111ll11_opy_ (u"࡙ࠧࡥࡵࠢࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠠࡧࡴࡲࡱࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡩ࡯࡯ࡨ࡬࡫ࠧᔅ"))
                                elif bstack1lllll1l1l1_opy_.name == bstack111ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᔆ"):
                                    bstack1l1l111llll_opy_[bstack111ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔇ")] = bstack1lllll1l1l1_opy_.value
                                    self.logger.debug(bstack111ll11_opy_ (u"ࠣࡕࡨࡸࠥࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥᔈ").format(bstack1lllll1l1l1_opy_.value))
                        os.environ[bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᔉ")] = json.dumps(bstack1l1l111llll_opy_)
                        if options.scripts:
                            scripts = {script.name: script.command for script in options.scripts}
                            accessibility_scripts.bstack1l1l1l1l11_opy_(scripts)
                            self.logger.debug(bstack111ll11_opy_ (u"࡙ࠥࡵࡪࡡࡵࡧࡧࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࡻࡾࠤᔊ").format(list(scripts.keys())))
                        if options.commands_to_wrap and options.commands_to_wrap.commands:
                            commands = [{bstack111ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᔋ"): cmd.name} for cmd in options.commands_to_wrap.commands]
                            accessibility_scripts.bstack1l11lll11ll_opy_(commands)
                            self.logger.debug(bstack111ll11_opy_ (u"࡛ࠧࡰࡥࡣࡷࡩࡩࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡹࠢᔌ").format(len(commands)))
                        accessibility_scripts.store()
                except Exception as e:
                    self.logger.debug(bstack111ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿࠥᔍ").format(e))
        if is_robot_playwright_installed():
            bstack1l1l11llll1_opy_ = json.loads(r.config)
            bstack1l1l1111l1l_opy_ = bstack1l1l11llll1_opy_.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫᔎ"), {}).get(bstack111ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᔏ"), bstack111ll11_opy_ (u"ࠩࠪᔐ"))
            os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᔑ")] = bstack1l1l1111l1l_opy_
    def bstack1l11l111ll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l11l1l11ll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l11l111111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l11l111111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l11l111ll1_opy_(event_name=EVENTS.bstack1l1l11ll1l1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l1l1lll1l1_opy_(self, bstack1l1l1ll1lll_opy_=10):
        if self.bstack1l11l1l11ll_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡸࡺࡡࡳࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨᔒ"))
            return True
        self.logger.debug(bstack111ll11_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦᔓ"))
        if os.getenv(bstack111ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡈࡒ࡛ࠨᔔ")) == bstack1l1l1l11lll_opy_:
            self.cli_bin_session_id = bstack1l1l1l11lll_opy_
            self.cli_listen_addr = bstack111ll11_opy_ (u"ࠢࡶࡰ࡬ࡼ࠿࠵ࡴ࡮ࡲ࠲ࡷࡩࡱ࠭ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࠨࡷ࠳ࡹ࡯ࡤ࡭ࠥᔕ") % (self.cli_bin_session_id)
            self.bstack1l11l1l11ll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l11l11lll1_opy_, bstack111ll11_opy_ (u"ࠣࡵࡧ࡯ࠧᔖ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l11l111l1l_opy_ compat for text=True in bstack1l11ll1ll1l_opy_ python
            encoding=bstack111ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᔗ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l11l1lll11_opy_ = threading.Thread(target=self.__1l1l1ll11l1_opy_, args=(bstack1l1l1ll1lll_opy_,))
        bstack1l11l1lll11_opy_.start()
        bstack1l11l1lll11_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡶࡴࡦࡽ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࢀࠤࡴࡻࡴ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡵࡷࡨࡴࡻࡴ࠯ࡴࡨࡥࡩ࠮ࠩࡾࠢࡨࡶࡷࡃࠢᔘ") + str(self.process.stderr.read()) + bstack111ll11_opy_ (u"ࠦࠧᔙ"))
        if not self.bstack1l11l1l11ll_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡡࠢᔚ") + str(id(self)) + bstack111ll11_opy_ (u"ࠨ࡝ࠡࡥ࡯ࡩࡦࡴࡵࡱࠤᔛ"))
            self.__1l11lllll11_opy_()
        self.logger.debug(bstack111ll11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡰࡳࡱࡦࡩࡸࡹ࡟ࡳࡧࡤࡨࡾࡀࠠࠣᔜ") + str(self.bstack1l11l1l11ll_opy_) + bstack111ll11_opy_ (u"ࠣࠤᔝ"))
        return self.bstack1l11l1l11ll_opy_
    def __1l1l1ll11l1_opy_(self, bstack1l11lll1lll_opy_=10):
        bstack1l1l1l1l1ll_opy_ = time.time()
        while self.process and time.time() - bstack1l1l1l1l1ll_opy_ < bstack1l11lll1lll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack111ll11_opy_ (u"ࠤ࡬ࡨࡂࠨᔞ") in line:
                    self.cli_bin_session_id = line.split(bstack111ll11_opy_ (u"ࠥ࡭ࡩࡃࠢᔟ"))[-1:][0].strip()
                    self.logger.debug(bstack111ll11_opy_ (u"ࠦࡨࡲࡩࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠥᔠ") + str(self.cli_bin_session_id) + bstack111ll11_opy_ (u"ࠧࠨᔡ"))
                    continue
                if bstack111ll11_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢᔢ") in line:
                    self.cli_listen_addr = line.split(bstack111ll11_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣᔣ"))[-1:][0].strip()
                    self.logger.debug(bstack111ll11_opy_ (u"ࠣࡥ࡯࡭ࡤࡲࡩࡴࡶࡨࡲࡤࡧࡤࡥࡴ࠽ࠦᔤ") + str(self.cli_listen_addr) + bstack111ll11_opy_ (u"ࠤࠥᔥ"))
                    continue
                if bstack111ll11_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤᔦ") in line:
                    port = line.split(bstack111ll11_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥᔧ"))[-1:][0].strip()
                    self.logger.debug(bstack111ll11_opy_ (u"ࠧࡶ࡯ࡳࡶ࠽ࠦᔨ") + str(port) + bstack111ll11_opy_ (u"ࠨࠢᔩ"))
                    continue
                if line.strip() == bstack1l11ll1lll1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack111ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡉࡐࡡࡖࡘࡗࡋࡁࡎࠤᔪ"), bstack111ll11_opy_ (u"ࠣ࠳ࠥᔫ")) == bstack111ll11_opy_ (u"ࠤ࠴ࠦᔬ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l11l1l11ll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack111ll11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳ࠼ࠣࠦᔭ") + str(e) + bstack111ll11_opy_ (u"ࠦࠧᔮ"))
        return False
    def __1l1l1l111ll_opy_(self):
        bstack111ll11_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡳࡻࡰࠡࡪࡤࡲࡩࡲࡥࡳࠢࡩࡳࡷࠦࡡࡴࡻࡱࡧࡤࡪࡩࡴࡲࡤࡸࡨ࡮ࡥࡳ࠮ࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡡࡵࡧࡻ࡭ࡹࠦࡴࡰࠢࡨࡲࡸࡻࡲࡦࠢࡷࡥࡸࡱࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠦࠧࠨᔯ")
        if self.bstack1l1lll11l1l_opy_ and self.bstack1l11l11ll11_opy_:
            try:
                self.bstack1l1lll11l1l_opy_.stop()
                self.bstack1l11l11ll11_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1l11ll111_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def __1l11lllll11_opy_(self):
        if self.bstack1l11lll111l_opy_:
            if self.bstack1l1lll11l1l_opy_ and self.bstack1l11l11ll11_opy_:
                try:
                    atexit.unregister(self.__1l1l1l111ll_opy_)
                except ValueError:
                    pass
                self.bstack1l1lll11l1l_opy_.stop()
                self.bstack1l11l11ll11_opy_ = False
            start = datetime.now()
            if self.bstack1l1l1l11ll1_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1l11l111l_opy_:
                    self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᔰ"), datetime.now() - start)
                else:
                    self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᔱ"), datetime.now() - start)
            self.__1l1l11l1lll_opy_()
            start = datetime.now()
            bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(bstack111ll11_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࠨᔲ"))
            self.bstack1l11lll111l_opy_.close()
            bstack1ll1l11l1_opy_.end(bstack111ll11_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽ࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺࠢᔳ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᔴ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᔵ"), True, None, None, None, None)
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠧࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢᔶ"), datetime.now() - start)
            self.bstack1l11lll111l_opy_ = None
        if self.process:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨࡳࡵࡱࡳࠦᔷ"))
            start = datetime.now()
            bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(bstack111ll11_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻࡭࡬ࡰࡱࠨᔸ"))
            self.process.terminate()
            bstack1ll1l11l1_opy_.end(bstack111ll11_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡮࡭ࡱࡲࠢᔹ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᔺ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᔻ"), True, None, None, None, None)
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢᔼ"), datetime.now() - start)
            self.process = None
            if self.bstack1l1l111lll1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1l1l111l_opy_()
                self.logger.info(
                    bstack111ll11_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠧᔽ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᔾ")] = self.config_testhub.build_hashed_id
        self.bstack1l11l1l11ll_opy_ = False
    def __1l11ll1l1ll_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack111ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᔿ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l11l1ll1l1_opy_ = get_pw_version()
            except:
                bstack1l11l1ll1l1_opy_ = _1l1l11ll1ll_opy_()
            data.framework_versions[bstack111ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᕀ")] = bstack1l11l1ll1l1_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack111ll11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᕁ")] = selenium.__version__
                data.frameworks.append(bstack111ll11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᕂ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᕃ")] = __version__
                data.frameworks.append(bstack111ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᕄ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack111ll11_opy_ (u"ࠨࡎࡰࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡥࡧࡷࡩࡨࡺࡥࡥࠤᕅ"))
    def bstack1l1l11l11ll_opy_(self, hub_url: str, platform_index: int, bstack11l1111lll_opy_: Any):
        if self.bstack1ll111l111_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᕆ"))
            return
        try:
            bstack111l1lllll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack111ll11_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᕇ")
            self.bstack1ll111l111_opy_ = bstack1l11l11111l_opy_(
                cli.config.get(bstack111ll11_opy_ (u"ࠤ࡫ࡹࡧ࡛ࡲ࡭ࠤᕈ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l11l1lllll_opy_={bstack111ll11_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᕉ"): bstack11l1111lll_opy_}
            )
            def bstack1l11l1ll1ll_opy_(self):
                return
            if self.config.get(bstack111ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠨᕊ"), True):
                Service.start = bstack1l11l1ll1ll_opy_
                Service.stop = bstack1l11l1ll1ll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11lll1ll1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1l111111l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᕋ"), datetime.now() - bstack111l1lllll_opy_)
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡵࡨࡰࡪࡴࡩࡶ࡯࠽ࠤࠧᕌ") + str(e) + bstack111ll11_opy_ (u"ࠢࠣᕍ"))
    def bstack1l1l11111l_opy_(self, platform_index: int):
        if self.bstack1ll111l111_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢᕎ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l1l11l1l1l_opy_
                self.bstack1ll111l111_opy_ = bstack111ll11111_opy_(
                    platform_index,
                    framework_name=bstack111ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᕏ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l1l11ll1ll_opy_
                from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1l1ll1l1l1l_opy_
                bstack1l11l1ll1l1_opy_ = get_pw_version()
                self.bstack1ll111l111_opy_ = bstack111ll11111_opy_(
                    platform_index,
                    framework_name=bstack111ll11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᕐ"),
                    framework_version=bstack1l11l1ll1l1_opy_.version,
                    classes=[],
                )
                ctx = bstack1l1ll1l1l1l_opy_.create_context(self.bstack1ll111l111_opy_)
                bstack11ll11l1l1_opy_.bstack1111l11ll_opy_[ctx.id] = bstack1l1ll1ll111_opy_(
                    ctx, bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᕑ"), bstack1l11l1ll1l1_opy_, bstack11l111l1l_opy_.bstack1ll1l11ll1_opy_
                )
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࠨᕒ") + str(e) + bstack111ll11_opy_ (u"ࠨࠢᕓ"))
            pass
    def bstack111lll1lll_opy_(self, framework_name: str = None):
        if self.test_framework:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᕔ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1l1l11l1l11_opy_({ bstack111ll11_opy_ (u"ࠣࡴࡲࡦࡴࡺ࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᕕ"): VERSION }, [bstack111ll11_opy_ (u"ࠤࡵࡳࡧࡵࡴࠣᕖ")], self.bstack1l1lll11l1l_opy_, self.bstack1l1l1l1l1l_opy_)
                return
            except Exception as e:
                self.logger.error(bstack111ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠺ࠡࠤᕗ") + str(e) + bstack111ll11_opy_ (u"ࠦࠧᕘ"))
        bstack1l1l1l1111l_opy_ = framework_name
        if bstack1l1l1l1111l_opy_ == bstack111ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᕙ"):
            import sys
            python_version = bstack111ll11_opy_ (u"ࠨࡻࡾ࠰ࡾࢁ࠳ࢁࡽࠣᕚ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            self.test_framework = bstack1l11l11ll1l_opy_(
                bstack1l11ll1111l_opy_={bstack111ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨᕛ"): python_version},
                bstack1l11lll1ll1_opy_=[bstack111ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩᕜ")],
                bstack1l1lll11l1l_opy_=self.bstack1l1lll11l1l_opy_,
                bstack1l1l1l1l1l_opy_=self.bstack1l1l1l1l1l_opy_
            )
            self.logger.info(bstack111ll11_opy_ (u"ࠤࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪࠠࡗࡣࡱ࡭ࡱࡲࡡࡑࡻࡷ࡬ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡩࡳࡷࠦࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠠࡵࡧࡶࡸࡸࠨᕝ"))
            return
        if bstack1ll1l1llll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack111ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᕞ"): pytest.__version__ }, [bstack111ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᕟ")], self.bstack1l1lll11l1l_opy_, self.bstack1l1l1l1l1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l11l1l1111_opy_({ bstack111ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᕠ"): pytest.__version__ }, [bstack111ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᕡ")], self.bstack1l1lll11l1l_opy_, self.bstack1l1l1l1l1l_opy_)
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦᕢ") + str(e) + bstack111ll11_opy_ (u"ࠣࠤᕣ"))
        self.bstack1l1l11lll1l_opy_()
    def bstack1l1l11lll1l_opy_(self):
        if not self.bstack11lll11l11_opy_():
            return
        bstack11lll111l1_opy_ = None
        def bstack1l11l11l1l_opy_(config, startdir):
            return bstack111ll11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢᕤ").format(bstack111ll11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᕥ"))
        def bstack1lll1111l_opy_():
            return
        def bstack111ll1l11l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack111ll11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᕦ"):
                return bstack111ll11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᕧ")
            else:
                return bstack11lll111l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11lll111l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l11l11l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lll1111l_opy_
            Config.getoption = bstack111ll1l11l_opy_
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣᕨ") + str(e) + bstack111ll11_opy_ (u"ࠢࠣᕩ"))
    def bstack1l11l1l1l1l_opy_(self):
        bstack1l111l1l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1l111l1l1_opy_, dict):
            if cli.config_observability:
                bstack1l111l1l1_opy_.update(
                    {bstack111ll11_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣᕪ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack111ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧᕫ") in accessibility.get(bstack111ll11_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᕬ"), {}):
                    bstack1l111lllll1_opy_ = accessibility.get(bstack111ll11_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᕭ"))
                    bstack1l111lllll1_opy_.update({ bstack111ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨᕮ"): bstack1l111lllll1_opy_.pop(bstack111ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᕯ")) })
                bstack1l111l1l1_opy_.update({bstack111ll11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᕰ"): accessibility })
        return bstack1l111l1l1_opy_
    @measure(event_name=EVENTS.bstack1l11l1ll11l_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def bstack1l1l1l11ll1_opy_(self, bstack1l11l1l1ll1_opy_: str = None, bstack1l11ll1l1l1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1l1l1l1l1l_opy_:
            return
        bstack111l1lllll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᕱ"), bstack111ll11_opy_ (u"ࠩ࠳ࠫᕲ")))
        req.client_worker_id = bstack111ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᕳ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l11l1l1ll1_opy_:
            req.bstack1l11l1l1ll1_opy_ = bstack1l11l1l1ll1_opy_
        if bstack1l11ll1l1l1_opy_:
            req.bstack1l11ll1l1l1_opy_ = bstack1l11ll1l1l1_opy_
        try:
            r = self.bstack1l1l1l1l1l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᕴ"), datetime.now() - bstack111l1lllll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11ll11lll_opy_(self, key: str, value: timedelta):
        tag = bstack111ll11_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧᕵ") if self.bstack11l1l1l11_opy_() else bstack111ll11_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧᕶ")
        self.bstack1l1l11l11l1_opy_[bstack111ll11_opy_ (u"ࠢ࠻ࠤᕷ").join([tag + bstack111ll11_opy_ (u"ࠣ࠯ࠥᕸ") + str(id(self)), key])] += value
    def bstack1l1l1l111l_opy_(self):
        if not os.getenv(bstack111ll11_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨᕹ"), bstack111ll11_opy_ (u"ࠥ࠴ࠧᕺ")) == bstack111ll11_opy_ (u"ࠦ࠶ࠨᕻ"):
            return
        bstack1l1l1l1lll1_opy_ = dict()
        bstack1111l11ll_opy_ = []
        if self.test_framework:
            bstack1111l11ll_opy_.extend(list(self.test_framework.bstack1111l11ll_opy_.values()))
        if self.bstack1ll111l111_opy_:
            bstack1111l11ll_opy_.extend(list(self.bstack1ll111l111_opy_.bstack1111l11ll_opy_.values()))
        for instance in bstack1111l11ll_opy_:
            if not instance.platform_index in bstack1l1l1l1lll1_opy_:
                bstack1l1l1l1lll1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l1l1l1lll1_opy_[instance.platform_index]
            for k, v in instance.bstack1l11l11l1ll_opy_().items():
                report[k] += v
                report[k.split(bstack111ll11_opy_ (u"ࠧࡀࠢᕼ"))[0]] += v
        bstack1l1l111l11l_opy_ = sorted([(k, v) for k, v in self.bstack1l1l11l11l1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1l1111111_opy_ = 0
        for r in bstack1l1l111l11l_opy_:
            bstack1l11ll11l11_opy_ = r[1].total_seconds()
            bstack1l1l1111111_opy_ += bstack1l11ll11l11_opy_
            self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦᕽ") + str(bstack1l11ll11l11_opy_) + bstack111ll11_opy_ (u"ࠢࠣᕾ"))
        self.logger.debug(bstack111ll11_opy_ (u"ࠣ࠯࠰ࠦᕿ"))
        bstack1l111llll1l_opy_ = []
        for platform_index, report in bstack1l1l1l1lll1_opy_.items():
            bstack1l111llll1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l111llll1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11lll1l1ll_opy_ = set()
        bstack1l1l1ll1111_opy_ = 0
        for r in bstack1l111llll1l_opy_:
            bstack1l11ll11l11_opy_ = r[2].total_seconds()
            bstack1l1l1ll1111_opy_ += bstack1l11ll11l11_opy_
            bstack11lll1l1ll_opy_.add(r[0])
            self.logger.debug(bstack111ll11_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥᖀ") + str(bstack1l11ll11l11_opy_) + bstack111ll11_opy_ (u"ࠥࠦᖁ"))
        if self.bstack11l1l1l11_opy_():
            self.logger.debug(bstack111ll11_opy_ (u"ࠦ࠲࠳ࠢᖂ"))
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧᖃ") + str(bstack1l1l1ll1111_opy_) + bstack111ll11_opy_ (u"ࠨࠢᖄ"))
        else:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦᖅ") + str(bstack1l1l1111111_opy_) + bstack111ll11_opy_ (u"ࠣࠤᖆ"))
        self.logger.debug(bstack111ll11_opy_ (u"ࠤ࠰࠱ࠧᖇ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᖈ"), bstack111ll11_opy_ (u"ࠫ࠵࠭ᖉ"))),
            client_worker_id=bstack111ll11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᖊ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1l1l1l1l1l_opy_:
            self.logger.error(bstack111ll11_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᖋ"))
            return None
        response = self.bstack1l1l1l1l1l_opy_.TestOrchestration(request)
        self.logger.debug(bstack111ll11_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤᖌ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l11ll11ll1_opy_(self, r):
        if r is not None and getattr(r, bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩᖍ"), None) and getattr(r.testhub, bstack111ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᖎ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack111ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᖏ")))
            for bstack1l1l1l1ll11_opy_, err in errors.items():
                if err[bstack111ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩᖐ")] == bstack111ll11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᖑ"):
                    self.logger.info(err[bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖒ")])
                else:
                    self.logger.error(err[bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖓ")])
    def bstack111lll11l_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()