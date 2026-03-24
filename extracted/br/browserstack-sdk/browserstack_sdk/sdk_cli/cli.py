# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
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
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1ll1ll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l11l1_opy_ import bstack1ll1111111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1l1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llllll1l_opy_ import bstack1ll111l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111lll_opy_ import bstack1l1ll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllllll1_opy_ import bstack1l1lll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1111_opy_ import bstack1l1ll111l11_opy_
from browserstack_sdk.sdk_cli.bstack11ll111lll_opy_ import bstack1llll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l111111ll_opy_ import bstack1l111111ll_opy_, Events, bstack11lll111_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1l1l11lll_opy_ import bstack1l1l1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import bstack111lll11l_opy_
from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1l1llllll_opy_ import bstack1l1llll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack111l1ll1ll_opy_ import bstack11l1l11l_opy_
from bstack_utils.helper import Notset, bstack1lll1ll1l1l_opy_, get_cli_dir, bstack1lll1ll11ll_opy_, bstack1l11ll1lll_opy_, bstack111l1l111l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111lllll_opy_, TestHookState, bstack1l1l1l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import bstack1ll11l1l111_opy_, bstack111l11ll_opy_, bstack1lll1ll11_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l1l1111l_opy_ import bstack11l1l1111_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll11ll1ll_opy_, bstack1lllll1l1_opy_
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11111_opy_ import bstack1l1l1ll1ll1_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1l1ll1lll1l_opy_(bs_config):
    bstack1l1lll1llll_opy_ = None
    bstack1lll1lll1ll_opy_ = None
    try:
        bstack1lll1lll1ll_opy_ = get_cli_dir()
        bstack1l1lll1llll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧጴ"))
        if not bstack1l1lll1llll_opy_:
            bstack1l1lll1llll_opy_ = bstack1lll1ll11ll_opy_(bstack1lll1lll1ll_opy_)
            bstack1l1ll1l111l_opy_ = bstack1lll1ll1l1l_opy_(bstack1l1lll1llll_opy_, bstack1lll1lll1ll_opy_, bs_config)
            bstack1l1lll1llll_opy_ = bstack1l1ll1l111l_opy_ if bstack1l1ll1l111l_opy_ else bstack1l1lll1llll_opy_
        if not bstack1l1lll1llll_opy_:
            raise ValueError(bstack1ll1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡈࡒࡉࠡࡲࡤࡸ࡭ࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡴࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡧࡱ࡯ࡨࡪࡸࠢጵ"))
    except Exception as ex:
        logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡪࡺࡴࡪࡰࡪࠤࡺࡶࠠࡄࡎࡌࠤࡵࡧࡴࡩ࠼ࠣࠦጶ") + str(ex) + bstack1ll1lll_opy_ (u"ࠧࠨጷ"))
    return bstack1l1lll1llll_opy_, bstack1lll1lll1ll_opy_
bstack1l1l1lllll1_opy_ = bstack1ll1lll_opy_ (u"ࠨ࠹࠺࠻࠼ࠦጸ")
bstack1ll111lll11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨጹ")
bstack1ll1111lll1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧጺ")
bstack1ll11111l11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢጻ")
BROWSERSTACK_AUTOMATION = bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨጼ")
bstack1ll11111l1l_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥጽ"))
bstack1ll111ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥጾ")
bstack1l1ll1l1l11_opy_ = bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡏࡓࡅࡈࡣࡋࡇࡌࡍࡄࡄࡇࡐࠨጿ")
bstack1l1ll111l1l_opy_ = [
    Events.bstack1lll11l11l_opy_,
    Events.CONNECT,
    Events.bstack11l11ll1ll_opy_,
]
def _1l1ll11l111_opy_():
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࡉࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠣࡀࠥ࠷࠹࠯࠶࠱࠴ࠥࡽࡨࡦࡴࡨࠤࡇࡸ࡯ࡸࡵࡨࡶ࠳࡫࡮ࡵࡴࡼ࠲࡬࡫ࡴࡠࡸࡨࡶࡸ࡯࡯࡯ࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤࡪࡾࡩࡴࡶ࠱ࠦࠧࠨፀ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l1l1l11l1l_opy_ = Path(Browser.__file__).parent / bstack1ll1lll_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡳࠤፁ") / bstack1ll1lll_opy_ (u"ࠤࡳࡥࡨࡱࡡࡨࡧ࠱࡮ࡸࡵ࡮ࠣፂ")
        bstack1ll1111l1l1_opy_ = json.loads(bstack1l1l1l11l1l_opy_.read_text())
        match = re.search(bstack1ll1lll_opy_ (u"ࡵࠦࡡࡪࠫ࡝࠰࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࠦፃ"), bstack1ll1111l1l1_opy_[bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡰࡦࡰࡧࡩࡳࡩࡩࡦࡵࠥፄ")][bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤፅ")])
        bstack1ll11111111_opy_ = match.group(0) if match else bstack1ll1lll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢፆ")
    except Exception:
        bstack1ll11111111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣፇ")
    return SimpleNamespace(version=bstack1ll11111111_opy_)
class SDKCLI:
    _1ll1ll1ll11_opy_ = None
    process: Union[None, Any]
    bstack1l1ll1111ll_opy_: bool
    bstack1l1l1ll1111_opy_: bool
    bstack1l1l1l1l1l1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l1llll1ll1_opy_: Union[None, grpc.Channel]
    bstack1l1llll11l1_opy_: str
    test_framework: TestFramework
    bstack1ll11ll1_opy_: bstack111lll11l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l1ll1l11l1_opy_: bstack1llll1ll1l_opy_
    accessibility: bstack1ll1ll11ll1_opy_
    bstack111l1ll1ll_opy_: bstack11l1l11l_opy_
    ai: bstack1ll1111111l_opy_
    bstack1l1lll1l1ll_opy_: bstack1l1l1llll1l_opy_
    bstack1l1ll1l1lll_opy_: List[bstack1l1llll1l11_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l1lll1111l_opy_: Any
    bstack1l1ll1l11ll_opy_: Dict[str, timedelta]
    bstack1l1l1lll11l_opy_: str
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_
    def __new__(cls):
        if not cls._1ll1ll1ll11_opy_:
            cls._1ll1ll1ll11_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1ll1ll11_opy_
    def __init__(self):
        self.process = None
        self.bstack1l1ll1111ll_opy_ = False
        self.bstack1l1llll1ll1_opy_ = None
        self.bstack1l1ll1l1ll1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll11111l11_opy_, None)
        self.bstack1l1ll11l1ll_opy_ = os.environ.get(bstack1ll1111lll1_opy_, bstack1ll1lll_opy_ (u"ࠣࠤፈ")) == bstack1ll1lll_opy_ (u"ࠤࠥፉ")
        self.bstack1l1l1ll1111_opy_ = False
        self.bstack1l1l1l1l1l1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l1lll1111l_opy_ = None
        self.test_framework = None
        self.bstack1ll11ll1_opy_ = None
        self.bstack1l1llll11l1_opy_=bstack1ll1lll_opy_ (u"ࠥࠦፊ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l1ll1l11ll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l111lll_opy_()
        self.bstack1ll111111l1_opy_ = False
        self.bstack1l1llllll11_opy_ = None
        self.bstack1l1lllll1ll_opy_ = None
        self.bstack1l1ll1l11l1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l1ll1l1lll_opy_ = []
    def bstack1l111llll_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack1ll1lll_opy_ (u"ࠦࡹࡸࡵࡦࠤፋ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l1ll1l1l11_opy_, bstack1ll1lll_opy_ (u"ࠬ࠭ፌ")).lower() in [bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫፍ"), bstack1ll1lll_opy_ (u"ࠧ࠲ࠩፎ"), bstack1ll1lll_opy_ (u"ࠨࡻࡨࡷࠬፏ")]:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡳࡷࡩࡩ࡯ࡩࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡳ࡯ࡥࡧࠣࡨࡺ࡫ࠠࡵࡱࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡓࡗࡉࡅࡠࡈࡄࡐࡑࡈࡁࡄࡍࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠥፐ"))
            os.environ[bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨፑ")] = bstack1ll1lll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥፒ")
            return False
        if bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩፓ") in config and str(config[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪፔ")]).lower() != bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ፕ"):
            return False
        bstack1l1llllllll_opy_ = [bstack1ll1lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣፖ"), bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨፗ"), bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦፘ")]
        if is_robot_playwright_installed():
            bstack1l1llllllll_opy_.append(bstack1ll1lll_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥፙ"))
            bstack1l1llllllll_opy_.append(bstack1ll1lll_opy_ (u"ࠧࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠨፚ"))
        bstack1l1ll111ll1_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ፛")) in bstack1l1llllllll_opy_ or os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨ፜")) in bstack1l1llllllll_opy_
        os.environ[bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦ፝")] = str(bstack1l1ll111ll1_opy_) # bstack1ll1111l111_opy_ bstack1l1l1l1lll1_opy_ VAR to bstack1l1ll111111_opy_ is binary running
        return bstack1l1ll111ll1_opy_
    def bstack11lll11ll1_opy_(self):
        for event in bstack1l1ll111l1l_opy_:
            bstack1l111111ll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l111111ll_opy_.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠡ࠿ࡁࠤࢀࡧࡲࡨࡵࢀࠤࠧ፞") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦ፟"))
            )
        bstack1l111111ll_opy_.register(Events.bstack1lll11l11l_opy_, self.__1ll1111ll1l_opy_)
        bstack1l111111ll_opy_.register(Events.CONNECT, self.__1ll11111ll1_opy_)
        bstack1l111111ll_opy_.register(Events.bstack11l11ll1ll_opy_, self.__1l1lllll1l1_opy_)
        bstack1l111111ll_opy_.register(Events.bstack111l1l1111_opy_, self.__1l1l1l11ll1_opy_)
    def bstack111llllll_opy_(self):
        return not self.bstack1l1ll11l1ll_opy_ and os.environ.get(bstack1ll1111lll1_opy_, bstack1ll1lll_opy_ (u"ࠦࠧ፠")) != bstack1ll1lll_opy_ (u"ࠧࠨ፡")
    def is_running(self):
        if self.bstack1l1ll11l1ll_opy_:
            return self.bstack1l1ll1111ll_opy_
        else:
            return bool(self.bstack1l1llll1ll1_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1ll1lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ።"))
                and self.config_observability.options.allow_screenshots == bstack1ll1lll_opy_ (u"ࠧࡵࡴࡸࡩࠬ፣")
            )
        except Exception:
            return False
    def bstack1llll11ll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l1ll1l1lll_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l1ll11llll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1l1ll11111l_opy_(self, bstack1l1ll1ll11l_opy_=10):
        if self.bstack1l1ll1l1ll1_opy_:
            return
        bstack1ll1l111l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll11111l11_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࠥ፤") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣ፥"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1ll1lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧ፦"), 0), (bstack1ll1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢ፧"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1ll1ll11l_opy_)
        self.bstack1l1llll1ll1_opy_ = channel
        self.bstack1l1ll1l1ll1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l1llll1ll1_opy_)
        self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦ፨"), datetime.now() - bstack1ll1l111l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll11111l11_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨ፩") + str(self.bstack111llllll_opy_()) + bstack1ll1lll_opy_ (u"ࠢࠣ፪"))
    def __1l1lllll1l1_opy_(self, event_name):
        if self.bstack111llllll_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣ፫"))
        self.__1l1lll1l1l1_opy_()
    @measure(event_name=EVENTS.bstack1ll111ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1l1l1l11ll1_opy_(self, event_name, bstack1l1l1l1ll1l_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤ፬"))
        bstack1l1l1l1ll11_opy_ = Path(bstack1ll11ll11l1_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦ፭"))
        if self.bstack1lll1lll1ll_opy_ and bstack1l1l1l1ll11_opy_.exists():
            with open(bstack1l1l1l1ll11_opy_, bstack1ll1lll_opy_ (u"ࠫࡷ࠭፮"), encoding=bstack1ll1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ፯")) as fp:
                data = json.load(fp)
                try:
                    bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"࠭ࡐࡐࡕࡗࠫ፰"), bstack11l1l1111_opy_(bstack1111ll111_opy_), data, {
                        bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ፱"): (self.config[bstack1ll1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ፲")], self.config[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ፳")])
                    })
                except Exception as e:
                    logger.debug(bstack1lllll1l1_opy_.format(str(e)))
            bstack1l1l1l1ll11_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l1l1ll11l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1ll1111ll1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
        self.bstack1l1llll11l1_opy_, self.bstack1lll1lll1ll_opy_ = bstack1l1ll1lll1l_opy_(data.bs_config)
        os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨ፴")] = self.bstack1lll1lll1ll_opy_
        if not self.bstack1l1llll11l1_opy_ or not self.bstack1lll1lll1ll_opy_:
            raise ValueError(bstack1ll1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥ፵"))
        if self.bstack111llllll_opy_():
            self.__1ll11111ll1_opy_(event_name, bstack11lll111_opy_())
            return
        try:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡔࡆࡎࠤࡘ࡫ࡴࡶࡲ࠱ࠦ፶"))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥ፷").format(e))
        start = datetime.now()
        is_started = self.__1l1lll11lll_opy_()
        self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠢࡴࡲࡤࡻࡳࡥࡴࡪ࡯ࡨࠦ፸"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l1ll11111l_opy_()
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢ፹"), datetime.now() - start)
            start = datetime.now()
            self.__1l1ll11lll1_opy_(data)
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢ፺"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1lll1l11l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1ll11111ll1_opy_(self, event_name: str, data: bstack11lll111_opy_):
        if not self.bstack111llllll_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࡰࡲࡸࠥࡧࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢ፻"))
            return
        bin_session_id = os.environ.get(bstack1ll1111lll1_opy_)
        start = datetime.now()
        self.__1l1ll11111l_opy_()
        self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥ፼"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡃࡍࡋࠣࠦ፽") + str(bin_session_id) + bstack1ll1lll_opy_ (u"ࠨࠢ፾"))
        start = datetime.now()
        self.__1l1ll11l11l_opy_()
        self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧ፿"), datetime.now() - start)
    def __1l1l1ll1l11_opy_(self):
        if not self.bstack1l1ll1l1ll1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡥࡤࡲࡳࡵࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡲࡵࡤࡶ࡮ࡨࡷࠧᎀ"))
            return
        bstack1l1l1ll1lll_opy_ = {
            bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᎁ"): (bstack1l1lll1l111_opy_, bstack1l1ll111l11_opy_, bstack11ll1l1l_opy_),
            bstack1ll1lll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᎂ"): (bstack1ll111l1l11_opy_, bstack1l1ll1ll1l1_opy_, bstack1l1llll1111_opy_),
        }
        if not self.bstack1l1llllll11_opy_ and self.session_framework in bstack1l1l1ll1lll_opy_:
            bstack1l1ll11l1l1_opy_, bstack1l1ll1ll1ll_opy_, bstack1ll111l1lll_opy_ = bstack1l1l1ll1lll_opy_[self.session_framework]
            bstack1l1l1lll111_opy_ = bstack1l1ll1ll1ll_opy_()
            self.bstack1l1lllll1ll_opy_ = bstack1l1l1lll111_opy_
            self.bstack1l1llllll11_opy_ = bstack1ll111l1lll_opy_
            self.bstack1l1ll1l1lll_opy_.append(bstack1l1l1lll111_opy_)
            self.bstack1l1ll1l1lll_opy_.append(bstack1l1ll11l1l1_opy_(self.bstack1l1lllll1ll_opy_))
        if not self.bstack1l1ll1l11l1_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1l1ll1l11l1_opy_ = bstack1llll1ll1l_opy_(self.bstack1l1llllll11_opy_, self.bstack1l1lllll1ll_opy_)
            self.bstack1l1ll1l1lll_opy_.append(self.bstack1l1ll1l11l1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1ll11ll1_opy_(self.bstack1l1llllll11_opy_, self.bstack1l1lllll1ll_opy_)
            self.bstack1l1ll1l1lll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1ll1lll_opy_ (u"ࠦࡸ࡫࡬ࡧࡊࡨࡥࡱࠨᎃ"), False) == True:
            self.ai = bstack1ll1111111l_opy_()
            self.bstack1l1ll1l1lll_opy_.append(self.ai)
        if not self.percy and self.bstack1l1lll1111l_opy_ and self.bstack1l1lll1111l_opy_.success:
            self.percy = bstack1l1l1llll1l_opy_(self.bstack1l1lll1111l_opy_)
            self.bstack1l1ll1l1lll_opy_.append(self.percy)
        for mod in self.bstack1l1ll1l1lll_opy_:
            if not mod.bstack1l1l1ll111l_opy_():
                mod.configure(self.bstack1l1ll1l1ll1_opy_, self.config, self.cli_bin_session_id, self.bstack1ll1l11l1l1_opy_)
    def __1l1l1l11l11_opy_(self):
        for mod in self.bstack1l1ll1l1lll_opy_:
            if mod.bstack1l1l1ll111l_opy_():
                mod.configure(self.bstack1l1ll1l1ll1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll111l111l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1l1ll11lll1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l1l1ll1111_opy_:
            return
        self.__1l1ll11ll11_opy_(data)
        bstack1ll1l111l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧᎄ")
        req.sdk_language = bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᎅ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll11111l1l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᎆ"), bstack1ll1lll_opy_ (u"ࠨ࠲ࠪᎇ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᎈ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡽ࡯ࡳ࡭ࡨࡶࠥࡧ࡮ࡥࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤ࡮ࡴࡤࡦࡺ࠽ࠤࢀࢃࠢᎉ").format(e))
        try:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࠨᎊ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᎋ"))
            r = self.bstack1l1ll1l1ll1_opy_.StartBinSession(req)
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᎌ"), datetime.now() - bstack1ll1l111l_opy_)
            os.environ[bstack1ll1111lll1_opy_] = r.bin_session_id
            self.__1l1ll1lllll_opy_(r)
            self.__1l1l1ll1l11_opy_()
            if not self.bstack1ll111111l1_opy_:
                self.bstack1ll1l11l1l1_opy_.start()
                self.bstack1ll111111l1_opy_ = True
                atexit.register(self.__1l1ll1111l1_opy_)
            self.bstack1l1l1ll1111_opy_ = True
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡜ࠤᎍ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨᎎ"))
        except grpc.bstack1l1ll11ll1l_opy_ as bstack1l1lllll111_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᎏ") + str(bstack1l1lllll111_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦ᎐"))
            traceback.print_exc()
            raise bstack1l1lllll111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ᎑") + str(e) + bstack1ll1lll_opy_ (u"ࠧࠨ᎒"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll111l1l1l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1l1ll11l11l_opy_(self):
        if not self.bstack111llllll_opy_() or not self.cli_bin_session_id or self.bstack1l1l1l1l1l1_opy_:
            return
        bstack1ll1l111l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᎓"), bstack1ll1lll_opy_ (u"ࠧ࠱ࠩ᎔")))
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᎕").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࠦ᎖") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧ᎗"))
            r = self.bstack1l1ll1l1ll1_opy_.ConnectBinSession(req)
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᎘"), datetime.now() - bstack1ll1l111l_opy_)
            self.__1l1ll1lllll_opy_(r)
            self.__1l1l1ll1l11_opy_()
            if not self.bstack1ll111111l1_opy_:
                self.bstack1ll1l11l1l1_opy_.start()
                self.bstack1ll111111l1_opy_ = True
                atexit.register(self.__1l1ll1111l1_opy_)
            self.bstack1l1l1l1l1l1_opy_ = True
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࠢ᎙") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧ᎚"))
        except grpc.bstack1l1ll11ll1l_opy_ as bstack1l1lllll111_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ᎛") + str(bstack1l1lllll111_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤ᎜"))
            traceback.print_exc()
            raise bstack1l1lllll111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᎝") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦ᎞"))
            traceback.print_exc()
            raise e
    def __1l1ll1lllll_opy_(self, r):
        self.bstack1l1lllll11l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1ll1lll_opy_ (u"ࠦࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡵࡨࡶࡻ࡫ࡲࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ᎟") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠧ࡫࡭ࡱࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡵ࡯ࡦࠥᎠ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡪࡸࡣࡺࠢ࡬ࡷࠥࡹࡥ࡯ࡶࠣࡳࡳࡲࡹࠡࡣࡶࠤࡵࡧࡲࡵࠢࡲࡪࠥࡺࡨࡦࠢࠥࡇࡴࡴ࡮ࡦࡥࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠬࠣࠢࡤࡲࡩࠦࡴࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡩࡴࠢࡤࡰࡸࡵࠠࡶࡵࡨࡨࠥࡨࡹࠡࡕࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡦࡴࡨࡪࡴࡸࡥ࠭ࠢࡑࡳࡳ࡫ࠠࡩࡣࡱࡨࡱ࡯࡮ࡨࠢ࡬ࡷࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᎡ")
        self.bstack1l1lll1111l_opy_ = getattr(r, bstack1ll1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ꭲ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᎣ")] = self.config_testhub.jwt
        os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᎤ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1ll1lll11_opy_ = json.loads(r.config)
            bstack1ll111ll111_opy_ = bstack1l1ll1lll11_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᎥ"), {}).get(bstack1ll1lll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ꭶ"), bstack1ll1lll_opy_ (u"ࠬ࠭Ꭷ"))
            os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᎨ")] = bstack1ll111ll111_opy_
    def bstack1l1lll1ll11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l1ll1111ll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1lll1lll1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1lll1lll1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l1lll1ll11_opy_(event_name=EVENTS.bstack1ll111l1ll1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1l1lll11lll_opy_(self, bstack1l1ll1ll11l_opy_=10):
        if self.bstack1l1ll1111ll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤᎩ"))
            return True
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢᎪ"))
        if os.getenv(bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤᎫ")) == bstack1ll111ll1l1_opy_:
            self.cli_bin_session_id = bstack1ll111ll1l1_opy_
            self.cli_listen_addr = bstack1ll1lll_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨᎬ") % (self.cli_bin_session_id)
            self.bstack1l1ll1111ll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1llll11l1_opy_, bstack1ll1lll_opy_ (u"ࠦࡸࡪ࡫ࠣᎭ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l1lll11l1l_opy_ compat for text=True in bstack1ll1111llll_opy_ python
            encoding=bstack1ll1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᎮ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1ll1l1l1l_opy_ = threading.Thread(target=self.__1ll111lll1l_opy_, args=(bstack1l1ll1ll11l_opy_,))
        bstack1l1ll1l1l1l_opy_.start()
        bstack1l1ll1l1l1l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥᎯ") + str(self.process.stderr.read()) + bstack1ll1lll_opy_ (u"ࠢࠣᎰ"))
        if not self.bstack1l1ll1111ll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࠥᎱ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧᎲ"))
            self.__1l1lll1l1l1_opy_()
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦᎳ") + str(self.bstack1l1ll1111ll_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᎴ"))
        return self.bstack1l1ll1111ll_opy_
    def __1ll111lll1l_opy_(self, bstack1l1l1lll1ll_opy_=10):
        bstack1ll11111lll_opy_ = time.time()
        while self.process and time.time() - bstack1ll11111lll_opy_ < bstack1l1l1lll1ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1ll1lll_opy_ (u"ࠧ࡯ࡤ࠾ࠤᎵ") in line:
                    self.cli_bin_session_id = line.split(bstack1ll1lll_opy_ (u"ࠨࡩࡥ࠿ࠥᎶ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨᎷ") + str(self.cli_bin_session_id) + bstack1ll1lll_opy_ (u"ࠣࠤᎸ"))
                    continue
                if bstack1ll1lll_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᎹ") in line:
                    self.cli_listen_addr = line.split(bstack1ll1lll_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦᎺ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢᎻ") + str(self.cli_listen_addr) + bstack1ll1lll_opy_ (u"ࠧࠨᎼ"))
                    continue
                if bstack1ll1lll_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᎽ") in line:
                    port = line.split(bstack1ll1lll_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨᎾ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢᎿ") + str(port) + bstack1ll1lll_opy_ (u"ࠤࠥᏀ"))
                    continue
                if line.strip() == bstack1ll111lll11_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1ll1lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧᏁ"), bstack1ll1lll_opy_ (u"ࠦ࠶ࠨᏂ")) == bstack1ll1lll_opy_ (u"ࠧ࠷ࠢᏃ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l1ll1111ll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢᏄ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᏅ"))
        return False
    def __1l1ll1111l1_opy_(self):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࡇࡱ࡫ࡡ࡯ࡷࡳࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡬࡯ࡳࠢࡤࡷࡾࡴࡣࡠࡦ࡬ࡷࡵࡧࡴࡤࡪࡨࡶ࠱ࠦࡣࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡤࡸࡪࡾࡩࡵࠢࡷࡳࠥ࡫࡮ࡴࡷࡵࡩࠥࡺࡡࡴ࡭ࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠢࠣࠤᏆ")
        if self.bstack1ll1l11l1l1_opy_ and self.bstack1ll111111l1_opy_:
            try:
                self.bstack1ll1l11l1l1_opy_.stop()
                self.bstack1ll111111l1_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1l1ll1l1l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def __1l1lll1l1l1_opy_(self):
        if self.bstack1l1llll1ll1_opy_:
            if self.bstack1ll1l11l1l1_opy_ and self.bstack1ll111111l1_opy_:
                try:
                    atexit.unregister(self.__1l1ll1111l1_opy_)
                except ValueError:
                    pass
                self.bstack1ll1l11l1l1_opy_.stop()
                self.bstack1ll111111l1_opy_ = False
            start = datetime.now()
            if self.bstack1l1l1l1l111_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1l1l1l1l1_opy_:
                    self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᏇ"), datetime.now() - start)
                else:
                    self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢᏈ"), datetime.now() - start)
            self.__1l1l1l11l11_opy_()
            start = datetime.now()
            bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(bstack1ll1lll_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࠤᏉ"))
            self.bstack1l1llll1ll1_opy_.close()
            bstack1lll1lll11_opy_.end(bstack1ll1lll_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࠥᏊ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᏋ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᏌ"), True, None, None, None, None)
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠣࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥᏍ"), datetime.now() - start)
            self.bstack1l1llll1ll1_opy_ = None
        if self.process:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡴࡶࠢᏎ"))
            start = datetime.now()
            bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(bstack1ll1lll_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡰ࡯࡬࡭ࠤᏏ"))
            self.process.terminate()
            bstack1lll1lll11_opy_.end(bstack1ll1lll_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡱࡩ࡭࡮ࠥᏐ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏑ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏒ"), True, None, None, None, None)
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠢ࡬࡫࡯ࡰࡤࡺࡩ࡮ࡧࠥᏓ"), datetime.now() - start)
            self.process = None
            if self.bstack1l1ll11l1ll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack111ll1ll1_opy_()
                self.logger.info(
                    bstack1ll1lll_opy_ (u"ࠣࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠣᏔ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᏕ")] = self.config_testhub.build_hashed_id
        self.bstack1l1ll1111ll_opy_ = False
    def __1l1ll11ll11_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1ll1lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᏖ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1ll1llll1_opy_ = get_pw_version()
            except:
                bstack1l1ll1llll1_opy_ = _1l1ll11l111_opy_()
            data.framework_versions[bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᏗ")] = bstack1l1ll1llll1_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack1ll1lll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᏘ")] = selenium.__version__
                data.frameworks.append(bstack1ll1lll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᏙ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᏚ")] = __version__
                data.frameworks.append(bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᏛ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡑࡳࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡨࡪࡺࡥࡤࡶࡨࡨࠧᏜ"))
    def bstack1l1l1llll11_opy_(self, hub_url: str, platform_index: int, bstack1l11l11ll1_opy_: Any):
        if self.bstack1ll11ll1_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢᏝ"))
            return
        try:
            bstack1ll1l111l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1ll1lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᏞ")
            self.bstack1ll11ll1_opy_ = bstack1l1llll1111_opy_(
                cli.config.get(bstack1ll1lll_opy_ (u"ࠧ࡮ࡵࡣࡗࡵࡰࠧᏟ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1lll111ll_opy_={bstack1ll1lll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᏠ"): bstack1l11l11ll1_opy_}
            )
            def bstack1ll111111ll_opy_(self):
                return
            if self.config.get(bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤᏡ"), True):
                Service.start = bstack1ll111111ll_opy_
                Service.stop = bstack1ll111111ll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11l1l11l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1llll1l1l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᏢ"), datetime.now() - bstack1ll1l111l_opy_)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣᏣ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᏤ"))
    def bstack1l1lll1ll1_opy_(self, platform_index: int):
        if self.bstack1ll11ll1_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᏥ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l1l1lll1l1_opy_
                self.bstack1ll11ll1_opy_ = bstack11ll1l1l_opy_(
                    platform_index,
                    framework_name=bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᏦ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l1ll11l111_opy_
                from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1ll11l1ll1l_opy_
                bstack1l1ll1llll1_opy_ = get_pw_version()
                self.bstack1ll11ll1_opy_ = bstack11ll1l1l_opy_(
                    platform_index,
                    framework_name=bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᏧ"),
                    framework_version=bstack1l1ll1llll1_opy_.version,
                    classes=[],
                )
                ctx = bstack1ll11l1ll1l_opy_.create_context(self.bstack1ll11ll1_opy_)
                bstack111lll11l_opy_.bstack111llll1l_opy_[ctx.id] = bstack1ll11l1l111_opy_(
                    ctx, bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᏨ"), bstack1l1ll1llll1_opy_, bstack111l11ll_opy_.bstack11ll1lll1_opy_
                )
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࠤᏩ") + str(e) + bstack1ll1lll_opy_ (u"ࠤࠥᏪ"))
            pass
    def bstack1lll1l1ll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧᏫ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1l1l1ll1ll1_opy_({ bstack1ll1lll_opy_ (u"ࠦࡷࡵࡢࡰࡶ࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨᏬ"): VERSION }, [bstack1ll1lll_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦᏭ")], self.bstack1ll1l11l1l1_opy_, self.bstack1l1ll1l1ll1_opy_)
                return
            except Exception as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡴࡲࡦࡴࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠽ࠤࠧᏮ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᏯ"))
        if bstack1l11ll1lll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1ll1lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᏰ"): pytest.__version__ }, [bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᏱ")], self.bstack1ll1l11l1l1_opy_, self.bstack1l1ll1l1ll1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1l1ll11ll_opy_({ bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᏲ"): pytest.__version__ }, [bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᏳ")], self.bstack1ll1l11l1l1_opy_, self.bstack1l1ll1l1ll1_opy_)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤᏴ") + str(e) + bstack1ll1lll_opy_ (u"ࠨࠢᏵ"))
        self.bstack1ll1111l11l_opy_()
    def bstack1ll1111l11l_opy_(self):
        if not self.bstack1l111llll_opy_():
            return
        bstack1ll1ll1l_opy_ = None
        def bstack11l1l11lll_opy_(config, startdir):
            return bstack1ll1lll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧ᏶").format(bstack1ll1lll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ᏷"))
        def bstack1l1l1111_opy_():
            return
        def bstack11ll11l11_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1ll1lll_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩᏸ"):
                return bstack1ll1lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᏹ")
            else:
                return bstack1ll1ll1l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll1ll1l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l1l11lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1111_opy_
            Config.getoption = bstack11ll11l11_opy_
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨᏺ") + str(e) + bstack1ll1lll_opy_ (u"ࠧࠨᏻ"))
    def bstack1ll111ll11l_opy_(self):
        bstack11lll11l1l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11lll11l1l_opy_, dict):
            if cli.config_observability:
                bstack11lll11l1l_opy_.update(
                    {bstack1ll1lll_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᏼ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥᏽ") in accessibility.get(bstack1ll1lll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤ᏾"), {}):
                    bstack1l1llll1lll_opy_ = accessibility.get(bstack1ll1lll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥ᏿"))
                    bstack1l1llll1lll_opy_.update({ bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦ᐀"): bstack1l1llll1lll_opy_.pop(bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢᐁ")) })
                bstack11lll11l1l_opy_.update({bstack1ll1lll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᐂ"): accessibility })
        return bstack11lll11l1l_opy_
    @measure(event_name=EVENTS.bstack1l1llll11ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l1l1l1l111_opy_(self, bstack1l1lll11l11_opy_: str = None, bstack1l1l1l1l11l_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1l1ll1l1ll1_opy_:
            return
        bstack1ll1l111l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᐃ"), bstack1ll1lll_opy_ (u"ࠧ࠱ࠩᐄ")))
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᐅ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l1lll11l11_opy_:
            req.bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_
        if bstack1l1l1l1l11l_opy_:
            req.bstack1l1l1l1l11l_opy_ = bstack1l1l1l1l11l_opy_
        try:
            r = self.bstack1l1ll1l1ll1_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡲࡴࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᐆ"), datetime.now() - bstack1ll1l111l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1111lll11_opy_(self, key: str, value: timedelta):
        tag = bstack1ll1lll_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥᐇ") if self.bstack111llllll_opy_() else bstack1ll1lll_opy_ (u"ࠦࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࠥᐈ")
        self.bstack1l1ll1l11ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡀࠢᐉ").join([tag + bstack1ll1lll_opy_ (u"ࠨ࠭ࠣᐊ") + str(id(self)), key])] += value
    def bstack111ll1ll1_opy_(self):
        if not os.getenv(bstack1ll1lll_opy_ (u"ࠢࡅࡇࡅ࡙ࡌࡥࡐࡆࡔࡉࠦᐋ"), bstack1ll1lll_opy_ (u"ࠣ࠲ࠥᐌ")) == bstack1ll1lll_opy_ (u"ࠤ࠴ࠦᐍ"):
            return
        bstack1ll111l11ll_opy_ = dict()
        bstack111llll1l_opy_ = []
        if self.test_framework:
            bstack111llll1l_opy_.extend(list(self.test_framework.bstack111llll1l_opy_.values()))
        if self.bstack1ll11ll1_opy_:
            bstack111llll1l_opy_.extend(list(self.bstack1ll11ll1_opy_.bstack111llll1l_opy_.values()))
        for instance in bstack111llll1l_opy_:
            if not instance.platform_index in bstack1ll111l11ll_opy_:
                bstack1ll111l11ll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll111l11ll_opy_[instance.platform_index]
            for k, v in instance.bstack1l1ll1ll111_opy_().items():
                report[k] += v
                report[k.split(bstack1ll1lll_opy_ (u"ࠥ࠾ࠧᐎ"))[0]] += v
        bstack1l1lll1ll1l_opy_ = sorted([(k, v) for k, v in self.bstack1l1ll1l11ll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1llll111l_opy_ = 0
        for r in bstack1l1lll1ll1l_opy_:
            bstack1l1l1l1llll_opy_ = r[1].total_seconds()
            bstack1l1llll111l_opy_ += bstack1l1l1l1llll_opy_
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻ࡽࡵ࡟࠵ࡣࡽ࠾ࠤᐏ") + str(bstack1l1l1l1llll_opy_) + bstack1ll1lll_opy_ (u"ࠧࠨᐐ"))
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࠭࠮ࠤᐑ"))
        bstack1l1lll111l1_opy_ = []
        for platform_index, report in bstack1ll111l11ll_opy_.items():
            bstack1l1lll111l1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l1lll111l1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack111lll1lll_opy_ = set()
        bstack1l1ll1l1111_opy_ = 0
        for r in bstack1l1lll111l1_opy_:
            bstack1l1l1l1llll_opy_ = r[2].total_seconds()
            bstack1l1ll1l1111_opy_ += bstack1l1l1l1llll_opy_
            bstack111lll1lll_opy_.add(r[0])
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࡼࡴ࡞࠴ࡢࢃ࠺ࡼࡴ࡞࠵ࡢࢃ࠽ࠣᐒ") + str(bstack1l1l1l1llll_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᐓ"))
        if self.bstack111llllll_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࠰࠱ࠧᐔ"))
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࡼࡶࡲࡸࡦࡲ࡟ࡤ࡮࡬ࢁࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠳ࡻࡴࡶࡵࠬࡵࡲࡡࡵࡨࡲࡶࡲࡹࠩࡾ࠿ࠥᐕ") + str(bstack1l1ll1l1111_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᐖ"))
        else:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤᐗ") + str(bstack1l1llll111l_opy_) + bstack1ll1lll_opy_ (u"ࠨࠢᐘ"))
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࠮࠯ࠥᐙ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᐚ"), bstack1ll1lll_opy_ (u"ࠩ࠳ࠫᐛ"))),
            client_worker_id=bstack1ll1lll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᐜ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1l1ll1l1ll1_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡨࡲࡩࡠࡵࡨࡶࡻ࡯ࡣࡦࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣᐝ"))
            return None
        response = self.bstack1l1ll1l1ll1_opy_.TestOrchestration(request)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶ࠰ࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠰ࡷࡪࡹࡳࡪࡱࡱࡁࢀࢃࠢᐞ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l1lllll11l_opy_(self, r):
        if r is not None and getattr(r, bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࠧᐟ"), None) and getattr(r.testhub, bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᐠ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1ll1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᐡ")))
            for bstack1ll1111ll11_opy_, err in errors.items():
                if err[bstack1ll1lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᐢ")] == bstack1ll1lll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᐣ"):
                    self.logger.info(err[bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᐤ")])
                else:
                    self.logger.error(err[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᐥ")])
    def bstack1l11llll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()