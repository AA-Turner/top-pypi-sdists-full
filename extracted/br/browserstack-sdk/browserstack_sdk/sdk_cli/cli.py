# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
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
from browserstack_sdk.sdk_cli.bstack1ll1ll1l111_opy_ import bstack1ll1ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1ll1l1_opy_ import bstack1ll11l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll1l1_opy_ import bstack1ll111111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll111_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1l11l_opy_ import bstack1l1ll111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1ll11111ll1_opy_
from browserstack_sdk.sdk_cli.bstack111l1l1111_opy_ import bstack1ll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111_opy_ import bstack1lll11111_opy_, Events, bstack1lll1111_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll1111l11l_opy_ import bstack1l1ll11llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll111ll1ll_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1111l_opy_ import bstack111ll11l1_opy_
from bstack_utils.helper import Notset, bstack1llll1l1l1l_opy_, get_cli_dir, bstack1llll1l1l11_opy_, bstack11l11l1111_opy_, bstack11111l1l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll11l1ll1l_opy_, TestHookState, bstack1l1ll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1l1l111l_opy_, bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l11ll11_opy_ import bstack1lll1l11_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111l1ll111_opy_, bstack1ll111l111_opy_
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1ll1_opy_ import bstack1ll11l1l111_opy_
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l111l_opy_())
def bstack1l1ll1l11l1_opy_(bs_config):
    bstack1ll11ll11ll_opy_ = None
    bstack1llll1ll111_opy_ = None
    try:
        bstack1llll1ll111_opy_ = get_cli_dir()
        bstack1ll11ll11ll_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨዓ"))
        if not bstack1ll11ll11ll_opy_:
            bstack1ll11ll11ll_opy_ = bstack1llll1l1l11_opy_(bstack1llll1ll111_opy_)
            bstack1l1ll1111l1_opy_ = bstack1llll1l1l1l_opy_(bstack1ll11ll11ll_opy_, bstack1llll1ll111_opy_, bs_config)
            bstack1ll11ll11ll_opy_ = bstack1l1ll1111l1_opy_ if bstack1l1ll1111l1_opy_ else bstack1ll11ll11ll_opy_
        if not bstack1ll11ll11ll_opy_:
            raise ValueError(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡉࡌࡊࠢࡳࡥࡹ࡮ࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡵࡲࠡ࡫ࡱࠤࡹ࡮ࡥࠡ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡨࡲࡰࡩ࡫ࡲࠣዔ"))
    except Exception as ex:
        logger.error(bstack1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࠡࡅࡏࡍࠥࡶࡡࡵࡪ࠽ࠤࠧዕ") + str(ex) + bstack1ll111_opy_ (u"ࠨࠢዖ"))
    return bstack1ll11ll11ll_opy_, bstack1llll1ll111_opy_
bstack1ll11ll1ll1_opy_ = bstack1ll111_opy_ (u"ࠢ࠺࠻࠼࠽ࠧ዗")
bstack1l1llll1l1l_opy_ = bstack1ll111_opy_ (u"ࠣࡴࡨࡥࡩࡿࠢዘ")
bstack1ll111111ll_opy_ = bstack1ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨዙ")
bstack1l1ll11l11l_opy_ = bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡐࡎ࡙ࡔࡆࡐࡢࡅࡉࡊࡒࠣዚ")
BROWSERSTACK_AUTOMATION = bstack1ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢዛ")
bstack1l1lll1ll11_opy_ = re.compile(bstack1ll111_opy_ (u"ࡷࠨࠨࡀ࡫ࠬ࠲࠯࠮ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࢁࡈࡓࠪ࠰࠭ࠦዜ"))
bstack1ll111l11l1_opy_ = bstack1ll111_opy_ (u"ࠨࡤࡦࡸࡨࡰࡴࡶ࡭ࡦࡰࡷࠦዝ")
bstack1ll11ll11l1_opy_ = bstack1ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡐࡔࡆࡉࡤࡌࡁࡍࡎࡅࡅࡈࡑࠢዞ")
bstack1ll11ll1111_opy_ = [
    Events.bstack11l1111l11_opy_,
    Events.CONNECT,
    Events.bstack111l11ll1l_opy_,
]
def _1ll11l1l1l1_opy_():
    bstack1ll111_opy_ (u"ࠣࠤࠥࡊࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡁࠦ࠱࠺࠰࠷࠲࠵ࠦࡷࡩࡧࡵࡩࠥࡈࡲࡰࡹࡶࡩࡷ࠴ࡥ࡯ࡶࡵࡽ࠳࡭ࡥࡵࡡࡹࡩࡷࡹࡩࡰࡰࡶࠤࡩࡵࡥࡴࡰࠪࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠧࠨࠢዟ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1ll11lll11l_opy_ = Path(Browser.__file__).parent / bstack1ll111_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡴࠥዠ") / bstack1ll111_opy_ (u"ࠥࡴࡦࡩ࡫ࡢࡩࡨ࠲࡯ࡹ࡯࡯ࠤዡ")
        bstack1ll11l1111l_opy_ = json.loads(bstack1ll11lll11l_opy_.read_text())
        match = re.search(bstack1ll111_opy_ (u"ࡶࠧࡢࡤࠬ࡞࠱ࡠࡩ࠱࡜࠯࡞ࡧ࠯ࠧዢ"), bstack1ll11l1111l_opy_[bstack1ll111_opy_ (u"ࠧࡪࡥࡱࡧࡱࡨࡪࡴࡣࡪࡧࡶࠦዣ")][bstack1ll111_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥዤ")])
        bstack1ll111ll11l_opy_ = match.group(0) if match else bstack1ll111_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣዥ")
    except Exception:
        bstack1ll111ll11l_opy_ = bstack1ll111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤዦ")
    return SimpleNamespace(version=bstack1ll111ll11l_opy_)
class SDKCLI:
    _1ll1111llll_opy_ = None
    process: Union[None, Any]
    bstack1l1llll1ll1_opy_: bool
    bstack1ll11ll1l1l_opy_: bool
    bstack1l1ll11ll11_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l1ll1111ll_opy_: Union[None, grpc.Channel]
    bstack1l1lll11111_opy_: str
    test_framework: TestFramework
    bstack1lll11111ll_opy_: bstack1ll1lllllll_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll11l11111_opy_: bstack1ll11l1lll_opy_
    accessibility: bstack1ll11l11lll_opy_
    bstack1l1ll1111l_opy_: bstack111ll11l1_opy_
    ai: bstack1ll111111l1_opy_
    bstack1l1lll1l1l1_opy_: bstack1l1lll1llll_opy_
    bstack1ll1111lll1_opy_: List[bstack1ll11111l11_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll111lll11_opy_: Any
    bstack1l1lllll1l1_opy_: Dict[str, timedelta]
    bstack1l1ll111l11_opy_: str
    bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_
    def __new__(cls):
        if not cls._1ll1111llll_opy_:
            cls._1ll1111llll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1111llll_opy_
    def __init__(self):
        self.process = None
        self.bstack1l1llll1ll1_opy_ = False
        self.bstack1l1ll1111ll_opy_ = None
        self.bstack1ll1lll11ll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l1ll11l11l_opy_, None)
        self.bstack1l1ll1ll1ll_opy_ = os.environ.get(bstack1ll111111ll_opy_, bstack1ll111_opy_ (u"ࠤࠥዧ")) == bstack1ll111_opy_ (u"ࠥࠦየ")
        self.bstack1ll11ll1l1l_opy_ = False
        self.bstack1l1ll11ll11_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll111lll11_opy_ = None
        self.test_framework = None
        self.bstack1lll11111ll_opy_ = None
        self.bstack1l1lll11111_opy_=bstack1ll111_opy_ (u"ࠦࠧዩ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.bstack1ll111l111l_opy_())
        self.bstack1l1lllll1l1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1ll1ll1l111_opy_ = bstack1ll1ll1l11l_opy_()
        self.bstack1l1ll1l11ll_opy_ = False
        self.bstack1l1ll1l1lll_opy_ = None
        self.bstack1l1lllllll1_opy_ = None
        self.bstack1ll11l11111_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1111lll1_opy_ = []
    def bstack1l111l111_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥዪ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll11ll11l1_opy_, bstack1ll111_opy_ (u"࠭ࠧያ")).lower() in [bstack1ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬዬ"), bstack1ll111_opy_ (u"ࠨ࠳ࠪይ"), bstack1ll111_opy_ (u"ࠩࡼࡩࡸ࠭ዮ")]:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡊࡴࡸࡣࡪࡰࡪࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡰࡦࡨࠤࡩࡻࡥࠡࡶࡲࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠦዯ"))
            os.environ[bstack1ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢደ")] = bstack1ll111_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦዱ")
            return False
        if bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪዲ") in config and str(config[bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫዳ")]).lower() != bstack1ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧዴ"):
            return False
        bstack1l1ll11111l_opy_ = [bstack1ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤድ"), bstack1ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢዶ"), bstack1ll111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠧዷ")]
        if is_robot_playwright_installed():
            bstack1l1ll11111l_opy_.append(bstack1ll111_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦዸ"))
            bstack1l1ll11111l_opy_.append(bstack1ll111_opy_ (u"ࠨࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠢዹ"))
        bstack1l1lll11ll1_opy_ = config.get(bstack1ll111_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥዺ")) in bstack1l1ll11111l_opy_ or os.environ.get(bstack1ll111_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩዻ")) in bstack1l1ll11111l_opy_
        os.environ[bstack1ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧዼ")] = str(bstack1l1lll11ll1_opy_) # bstack1l1lll1ll1l_opy_ bstack1l1llll1lll_opy_ VAR to bstack1ll111l1l1l_opy_ is binary running
        return bstack1l1lll11ll1_opy_
    def bstack1ll1l1ll1l_opy_(self):
        for event in bstack1ll11ll1111_opy_:
            bstack1lll11111_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1lll11111_opy_.logger.debug(bstack1ll111_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨዽ") + str(kwargs) + bstack1ll111_opy_ (u"ࠦࠧዾ"))
            )
        bstack1lll11111_opy_.register(Events.bstack11l1111l11_opy_, self.__1l1lll111ll_opy_)
        bstack1lll11111_opy_.register(Events.CONNECT, self.__1ll11l1l1ll_opy_)
        bstack1lll11111_opy_.register(Events.bstack111l11ll1l_opy_, self.__1ll11l11l1l_opy_)
        bstack1lll11111_opy_.register(Events.bstack1l111111ll_opy_, self.__1l1ll1l1l11_opy_)
    def bstack111ll1l1_opy_(self):
        return not self.bstack1l1ll1ll1ll_opy_ and os.environ.get(bstack1ll111111ll_opy_, bstack1ll111_opy_ (u"ࠧࠨዿ")) != bstack1ll111_opy_ (u"ࠨࠢጀ")
    def is_running(self):
        if self.bstack1l1ll1ll1ll_opy_:
            return self.bstack1l1llll1ll1_opy_
        else:
            return bool(self.bstack1l1ll1111ll_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1ll111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨጁ"))
                and self.config_observability.options.allow_screenshots == bstack1ll111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ጂ")
            )
        except Exception:
            return False
    def bstack11l1111ll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1111lll1_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll11l11ll1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1l1ll1l1l1l_opy_(self, bstack1l1ll1lll11_opy_=10):
        if self.bstack1ll1lll11ll_opy_:
            return
        bstack1ll1l1l111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l1ll11l11l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1ll111_opy_ (u"ࠤ࡞ࠦጃ") + str(id(self)) + bstack1ll111_opy_ (u"ࠥࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡯࡮ࡨࠤጄ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1ll111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶ࡟ࡱࡴࡲࡼࡾࠨጅ"), 0), (bstack1ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡴࡡࡳࡶࡴࡾࡹࠣጆ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1ll1lll11_opy_)
        self.bstack1l1ll1111ll_opy_ = channel
        self.bstack1ll1lll11ll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l1ll1111ll_opy_)
        self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࠧጇ"), datetime.now() - bstack1ll1l1l111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l1ll11l11l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥ࠼ࠣ࡭ࡸࡥࡣࡩ࡫࡯ࡨࡤࡶࡲࡰࡥࡨࡷࡸࡃࠢገ") + str(self.bstack111ll1l1_opy_()) + bstack1ll111_opy_ (u"ࠣࠤጉ"))
    def __1ll11l11l1l_opy_(self, event_name):
        if self.bstack111ll1l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡉࡌࡊࠤጊ"))
        self.__1l1ll11lll1_opy_()
    @measure(event_name=EVENTS.bstack1l1l1lllll1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1l1ll1l1l11_opy_(self, event_name, bstack1l1ll1llll1_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠥጋ"))
        bstack1ll1111ll1l_opy_ = Path(bstack1ll1l11llll_opy_ (u"ࠦࢀࡹࡥ࡭ࡨ࠱ࡧࡱ࡯࡟ࡥ࡫ࡵࢁ࠴ࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࡹ࠮࡫ࡵࡲࡲࠧጌ"))
        if self.bstack1llll1ll111_opy_ and bstack1ll1111ll1l_opy_.exists():
            with open(bstack1ll1111ll1l_opy_, bstack1ll111_opy_ (u"ࠬࡸࠧግ"), encoding=bstack1ll111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬጎ")) as fp:
                data = json.load(fp)
                try:
                    bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠧࡑࡑࡖࡘࠬጏ"), bstack1lll1l11_opy_(bstack1l1l11l11_opy_), data, {
                        bstack1ll111_opy_ (u"ࠨࡣࡸࡸ࡭࠭ጐ"): (self.config[bstack1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ጑")], self.config[bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ጒ")])
                    })
                except Exception as e:
                    logger.debug(bstack1ll111l111_opy_.format(str(e)))
            bstack1ll1111ll1l_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll11l11l11_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1l1lll111ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
        self.bstack1l1lll11111_opy_, self.bstack1llll1ll111_opy_ = bstack1l1ll1l11l1_opy_(data.bs_config)
        os.environ[bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡛ࡗࡏࡔࡂࡄࡏࡉࡤࡊࡉࡓࠩጓ")] = self.bstack1llll1ll111_opy_
        if not self.bstack1l1lll11111_opy_ or not self.bstack1llll1ll111_opy_:
            raise ValueError(bstack1ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡩࡧࠣࡗࡉࡑࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠦጔ"))
        if self.bstack111ll1l1_opy_():
            self.__1ll11l1l1ll_opy_(event_name, bstack1lll1111_opy_())
            return
        try:
            logger.debug(bstack1ll111_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧጕ"))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦ጖").format(e))
        start = datetime.now()
        is_started = self.__1ll111lll1l_opy_()
        self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧ጗"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l1ll1l1l1l_opy_()
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣጘ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1111l1l1_opy_(data)
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣጙ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1l1llllll_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1ll11l1l1ll_opy_(self, event_name: str, data: bstack1lll1111_opy_):
        if not self.bstack111ll1l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣጚ"))
            return
        bin_session_id = os.environ.get(bstack1ll111111ll_opy_)
        start = datetime.now()
        self.__1l1ll1l1l1l_opy_()
        self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦጛ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧጜ") + str(bin_session_id) + bstack1ll111_opy_ (u"ࠢࠣጝ"))
        start = datetime.now()
        self.__1l1ll111lll_opy_()
        self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨጞ"), datetime.now() - start)
    def __1l1ll1l1111_opy_(self):
        if not self.bstack1ll1lll11ll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨጟ"))
            return
        bstack1ll11l1ll11_opy_ = {
            bstack1ll111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢጠ"): (bstack1l1ll111l1l_opy_, bstack1ll11111ll1_opy_, bstack1lll111l1l1_opy_),
            bstack1ll111_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨጡ"): (bstack1ll11111111_opy_, bstack1ll111l1lll_opy_, bstack1ll11lll111_opy_),
        }
        if not self.bstack1l1ll1l1lll_opy_ and self.session_framework in bstack1ll11l1ll11_opy_:
            bstack1l1ll1l111l_opy_, bstack1ll11111lll_opy_, bstack1l1ll111111_opy_ = bstack1ll11l1ll11_opy_[self.session_framework]
            bstack1ll111l1111_opy_ = bstack1ll11111lll_opy_()
            self.bstack1l1lllllll1_opy_ = bstack1ll111l1111_opy_
            self.bstack1l1ll1l1lll_opy_ = bstack1l1ll111111_opy_
            self.bstack1ll1111lll1_opy_.append(bstack1ll111l1111_opy_)
            self.bstack1ll1111lll1_opy_.append(bstack1l1ll1l111l_opy_(self.bstack1l1lllllll1_opy_))
        if not self.bstack1ll11l11111_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1ll11l11111_opy_ = bstack1ll11l1lll_opy_(self.bstack1l1ll1l1lll_opy_, self.bstack1l1lllllll1_opy_)
            self.bstack1ll1111lll1_opy_.append(self.bstack1ll11l11111_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll11l11lll_opy_(self.bstack1l1ll1l1lll_opy_, self.bstack1l1lllllll1_opy_)
            self.bstack1ll1111lll1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1ll111_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢጢ"), False) == True:
            self.ai = bstack1ll111111l1_opy_()
            self.bstack1ll1111lll1_opy_.append(self.ai)
        if not self.percy and self.bstack1ll111lll11_opy_ and self.bstack1ll111lll11_opy_.success:
            self.percy = bstack1l1lll1llll_opy_(self.bstack1ll111lll11_opy_)
            self.bstack1ll1111lll1_opy_.append(self.percy)
        for mod in self.bstack1ll1111lll1_opy_:
            if not mod.bstack1ll11l1lll1_opy_():
                mod.configure(self.bstack1ll1lll11ll_opy_, self.config, self.cli_bin_session_id, self.bstack1ll1ll1l111_opy_)
    def __1ll1111l1ll_opy_(self):
        for mod in self.bstack1ll1111lll1_opy_:
            if mod.bstack1ll11l1lll1_opy_():
                mod.configure(self.bstack1ll1lll11ll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1111111l_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1ll1111l1l1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll11ll1l1l_opy_:
            return
        self.__1l1llll1111_opy_(data)
        bstack1ll1l1l111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1ll111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨጣ")
        req.sdk_language = bstack1ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢጤ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l1lll1ll11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨጥ"), bstack1ll111_opy_ (u"ࠩ࠳ࠫጦ")))
            req.client_worker_id = bstack1ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤጧ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡷࡰࡴ࡮ࡩࡷࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥ࡯࡮ࡥࡧࡻ࠾ࠥࢁࡽࠣጨ").format(e))
        try:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡡࠢጩ") + str(id(self)) + bstack1ll111_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧጪ"))
            r = self.bstack1ll1lll11ll_opy_.StartBinSession(req)
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤጫ"), datetime.now() - bstack1ll1l1l111_opy_)
            os.environ[bstack1ll111111ll_opy_] = r.bin_session_id
            self.__1l1lll111l1_opy_(r)
            self.__1l1ll1l1111_opy_()
            if not self.bstack1l1ll1l11ll_opy_:
                self.bstack1ll1ll1l111_opy_.start()
                self.bstack1l1ll1l11ll_opy_ = True
                atexit.register(self.__1l1lllll111_opy_)
            self.bstack1ll11ll1l1l_opy_ = True
            self.logger.debug(bstack1ll111_opy_ (u"ࠣ࡝ࠥጬ") + str(id(self)) + bstack1ll111_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢጭ"))
        except grpc.bstack1ll1111ll11_opy_ as bstack1l1lll11l1l_opy_:
            self.logger.error(bstack1ll111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧጮ") + str(bstack1l1lll11l1l_opy_) + bstack1ll111_opy_ (u"ࠦࠧጯ"))
            traceback.print_exc()
            raise bstack1l1lll11l1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጰ") + str(e) + bstack1ll111_opy_ (u"ࠨࠢጱ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll11l1l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1l1ll111lll_opy_(self):
        if not self.bstack111ll1l1_opy_() or not self.cli_bin_session_id or self.bstack1l1ll11ll11_opy_:
            return
        bstack1ll1l1l111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧጲ"), bstack1ll111_opy_ (u"ࠨ࠲ࠪጳ")))
        req.client_worker_id = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣጴ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡟ࠧጵ") + str(id(self)) + bstack1ll111_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨጶ"))
            r = self.bstack1ll1lll11ll_opy_.ConnectBinSession(req)
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤጷ"), datetime.now() - bstack1ll1l1l111_opy_)
            self.__1l1lll111l1_opy_(r)
            self.__1l1ll1l1111_opy_()
            if not self.bstack1l1ll1l11ll_opy_:
                self.bstack1ll1ll1l111_opy_.start()
                self.bstack1l1ll1l11ll_opy_ = True
                atexit.register(self.__1l1lllll111_opy_)
            self.bstack1l1ll11ll11_opy_ = True
            self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡛ࠣጸ") + str(id(self)) + bstack1ll111_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨጹ"))
        except grpc.bstack1ll1111ll11_opy_ as bstack1l1lll11l1l_opy_:
            self.logger.error(bstack1ll111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥጺ") + str(bstack1l1lll11l1l_opy_) + bstack1ll111_opy_ (u"ࠤࠥጻ"))
            traceback.print_exc()
            raise bstack1l1lll11l1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢጼ") + str(e) + bstack1ll111_opy_ (u"ࠦࠧጽ"))
            traceback.print_exc()
            raise e
    def __1l1lll111l1_opy_(self, r):
        self.bstack1ll11ll1l11_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1ll111_opy_ (u"ࠧࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦጾ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1ll111_opy_ (u"ࠨࡥ࡮ࡲࡷࡽࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡯ࡶࡰࡧࠦጿ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕ࡫ࡲࡤࡻࠣ࡭ࡸࠦࡳࡦࡰࡷࠤࡴࡴ࡬ࡺࠢࡤࡷࠥࡶࡡࡳࡶࠣࡳ࡫ࠦࡴࡩࡧࠣࠦࡈࡵ࡮࡯ࡧࡦࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠭ࠤࠣࡥࡳࡪࠠࡵࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡪࡵࠣࡥࡱࡹ࡯ࠡࡷࡶࡩࡩࠦࡢࡺࠢࡖࡸࡦࡸࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࡵࡩ࡫ࡵࡲࡦ࠮ࠣࡒࡴࡴࡥࠡࡪࡤࡲࡩࡲࡩ࡯ࡩࠣ࡭ࡸࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤፀ")
        self.bstack1ll111lll11_opy_ = getattr(r, bstack1ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧፁ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ፂ")] = self.config_testhub.jwt
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨፃ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1lll11lll_opy_ = json.loads(r.config)
            bstack1l1l1llll1l_opy_ = bstack1l1lll11lll_opy_.get(bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨፄ"), {}).get(bstack1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧፅ"), bstack1ll111_opy_ (u"࠭ࠧፆ"))
            os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩፇ")] = bstack1l1l1llll1l_opy_
    def bstack1ll11l1l11l_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l1llll1ll1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1lll1l111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1lll1l111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll11l1l11l_opy_(event_name=EVENTS.bstack1ll11ll111l_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1ll111lll1l_opy_(self, bstack1l1ll1lll11_opy_=10):
        if self.bstack1l1llll1ll1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠥፈ"))
            return True
        self.logger.debug(bstack1ll111_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣፉ"))
        if os.getenv(bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡅࡏࡘࠥፊ")) == bstack1ll111l11l1_opy_:
            self.cli_bin_session_id = bstack1ll111l11l1_opy_
            self.cli_listen_addr = bstack1ll111_opy_ (u"ࠦࡺࡴࡩࡹ࠼࠲ࡸࡲࡶ࠯ࡴࡦ࡮࠱ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࠥࡴ࠰ࡶࡳࡨࡱࠢፋ") % (self.cli_bin_session_id)
            self.bstack1l1llll1ll1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1lll11111_opy_, bstack1ll111_opy_ (u"ࠧࡹࡤ࡬ࠤፌ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l1ll1lllll_opy_ compat for text=True in bstack1ll11l1llll_opy_ python
            encoding=bstack1ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧፍ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1lll1lll1_opy_ = threading.Thread(target=self.__1l1ll1lll1l_opy_, args=(bstack1l1ll1lll11_opy_,))
        bstack1l1lll1lll1_opy_.start()
        bstack1l1lll1lll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡳࡱࡣࡺࡲ࠿ࠦࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫ࡽࠡࡱࡸࡸࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡹࡴࡥࡱࡸࡸ࠳ࡸࡥࡢࡦࠫ࠭ࢂࠦࡥࡳࡴࡀࠦፎ") + str(self.process.stderr.read()) + bstack1ll111_opy_ (u"ࠣࠤፏ"))
        if not self.bstack1l1llll1ll1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤ࡞ࠦፐ") + str(id(self)) + bstack1ll111_opy_ (u"ࠥࡡࠥࡩ࡬ࡦࡣࡱࡹࡵࠨፑ"))
            self.__1l1ll11lll1_opy_()
        self.logger.debug(bstack1ll111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡴࡷࡵࡣࡦࡵࡶࡣࡷ࡫ࡡࡥࡻ࠽ࠤࠧፒ") + str(self.bstack1l1llll1ll1_opy_) + bstack1ll111_opy_ (u"ࠧࠨፓ"))
        return self.bstack1l1llll1ll1_opy_
    def __1l1ll1lll1l_opy_(self, bstack1l1llllll11_opy_=10):
        bstack1l1llll11l1_opy_ = time.time()
        while self.process and time.time() - bstack1l1llll11l1_opy_ < bstack1l1llllll11_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1ll111_opy_ (u"ࠨࡩࡥ࠿ࠥፔ") in line:
                    self.cli_bin_session_id = line.split(bstack1ll111_opy_ (u"ࠢࡪࡦࡀࠦፕ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll111_opy_ (u"ࠣࡥ࡯࡭ࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠢፖ") + str(self.cli_bin_session_id) + bstack1ll111_opy_ (u"ࠤࠥፗ"))
                    continue
                if bstack1ll111_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦፘ") in line:
                    self.cli_listen_addr = line.split(bstack1ll111_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧፙ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll111_opy_ (u"ࠧࡩ࡬ࡪࡡ࡯࡭ࡸࡺࡥ࡯ࡡࡤࡨࡩࡸ࠺ࠣፚ") + str(self.cli_listen_addr) + bstack1ll111_opy_ (u"ࠨࠢ፛"))
                    continue
                if bstack1ll111_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨ፜") in line:
                    port = line.split(bstack1ll111_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢ፝"))[-1:][0].strip()
                    self.logger.debug(bstack1ll111_opy_ (u"ࠤࡳࡳࡷࡺ࠺ࠣ፞") + str(port) + bstack1ll111_opy_ (u"ࠥࠦ፟"))
                    continue
                if line.strip() == bstack1l1llll1l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1ll111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡍࡔࡥࡓࡕࡔࡈࡅࡒࠨ፠"), bstack1ll111_opy_ (u"ࠧ࠷ࠢ፡")) == bstack1ll111_opy_ (u"ࠨ࠱ࠣ።"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l1llll1ll1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࡀࠠࠣ፣") + str(e) + bstack1ll111_opy_ (u"ࠣࠤ፤"))
        return False
    def __1l1lllll111_opy_(self):
        bstack1ll111_opy_ (u"ࠤࠥࠦࡈࡲࡥࡢࡰࡸࡴࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡦࡰࡴࠣࡥࡸࡿ࡮ࡤࡡࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷ࠲ࠠࡤࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡥࡹ࡫ࡸࡪࡶࠣࡸࡴࠦࡥ࡯ࡵࡸࡶࡪࠦࡴࡢࡵ࡮ࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣࠤࠥ፥")
        if self.bstack1ll1ll1l111_opy_ and self.bstack1l1ll1l11ll_opy_:
            try:
                self.bstack1ll1ll1l111_opy_.stop()
                self.bstack1l1ll1l11ll_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1ll11lll1l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def __1l1ll11lll1_opy_(self):
        if self.bstack1l1ll1111ll_opy_:
            if self.bstack1ll1ll1l111_opy_ and self.bstack1l1ll1l11ll_opy_:
                try:
                    atexit.unregister(self.__1l1lllll111_opy_)
                except ValueError:
                    pass
                self.bstack1ll1ll1l111_opy_.stop()
                self.bstack1l1ll1l11ll_opy_ = False
            start = datetime.now()
            if self.bstack1l1lll1l1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1ll11ll11_opy_:
                    self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢ፦"), datetime.now() - start)
                else:
                    self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣ፧"), datetime.now() - start)
            self.__1ll1111l1ll_opy_()
            start = datetime.now()
            bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(bstack1ll111_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࠥ፨"))
            self.bstack1l1ll1111ll_opy_.close()
            bstack111ll11111_opy_.end(bstack1ll111_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࠦ፩"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ፪"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ፫"), True, None, None, None, None)
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦ፬"), datetime.now() - start)
            self.bstack1l1ll1111ll_opy_ = None
        if self.process:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡹࡵࡰࠣ፭"))
            start = datetime.now()
            bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(bstack1ll111_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡱࡩ࡭࡮ࠥ፮"))
            self.process.terminate()
            bstack111ll11111_opy_.end(bstack1ll111_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡫ࡪ࡮࡯ࠦ፯"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ፰"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ፱"), True, None, None, None, None)
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣ࡭࡬ࡰࡱࡥࡴࡪ࡯ࡨࠦ፲"), datetime.now() - start)
            self.process = None
            if self.bstack1l1ll1ll1ll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l11lllll_opy_()
                self.logger.info(
                    bstack1ll111_opy_ (u"ࠤ࡙࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤ፳").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1ll111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ፴")] = self.config_testhub.build_hashed_id
        self.bstack1l1llll1ll1_opy_ = False
    def __1l1llll1111_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1ll111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ፵"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1lll1111l_opy_ = get_pw_version()
            except:
                bstack1l1lll1111l_opy_ = _1ll11l1l1l1_opy_()
            data.framework_versions[bstack1ll111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ፶")] = bstack1l1lll1111l_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack1ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣ፷")] = selenium.__version__
                data.frameworks.append(bstack1ll111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ፸"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ፹")] = __version__
                data.frameworks.append(bstack1ll111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ፺"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack1ll111_opy_ (u"ࠥࡒࡴࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡩ࡫ࡴࡦࡥࡷࡩࡩࠨ፻"))
    def bstack1ll111l1ll1_opy_(self, hub_url: str, platform_index: int, bstack1l11ll1ll_opy_: Any):
        if self.bstack1lll11111ll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣ፼"))
            return
        try:
            bstack1ll1l1l111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1ll111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ፽")
            self.bstack1lll11111ll_opy_ = bstack1ll11lll111_opy_(
                cli.config.get(bstack1ll111_opy_ (u"ࠨࡨࡶࡤࡘࡶࡱࠨ፾"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1llllll1l_opy_={bstack1ll111_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦ፿"): bstack1l11ll1ll_opy_}
            )
            def bstack1l1lllll1ll_opy_(self):
                return
            if self.config.get(bstack1ll111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥᎀ"), True):
                Service.start = bstack1l1lllll1ll_opy_
                Service.stop = bstack1l1lllll1ll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack111ll11l1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1lllll11l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᎁ"), datetime.now() - bstack1ll1l1l111_opy_)
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤᎂ") + str(e) + bstack1ll111_opy_ (u"ࠦࠧᎃ"))
    def bstack1lll111l11_opy_(self, platform_index: int):
        if self.bstack1lll11111ll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᎄ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l1ll1ll111_opy_
                self.bstack1lll11111ll_opy_ = bstack1lll111l1l1_opy_(
                    platform_index,
                    framework_name=bstack1ll111_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᎅ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1ll11l1l1l1_opy_
                from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11lll1ll_opy_
                bstack1l1lll1111l_opy_ = get_pw_version()
                self.bstack1lll11111ll_opy_ = bstack1lll111l1l1_opy_(
                    platform_index,
                    framework_name=bstack1ll111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᎆ"),
                    framework_version=bstack1l1lll1111l_opy_.version,
                    classes=[],
                )
                ctx = bstack1ll11lll1ll_opy_.create_context(self.bstack1lll11111ll_opy_)
                bstack1ll1lllllll_opy_.bstack1ll1llllll1_opy_[ctx.id] = bstack1ll1l1l111l_opy_(
                    ctx, bstack1ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᎇ"), bstack1l1lll1111l_opy_, bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_
                )
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠻ࠢࠥᎈ") + str(e) + bstack1ll111_opy_ (u"ࠥࠦᎉ"))
            pass
    def bstack111ll1ll11_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡵࡿࡴࡦࡵࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨᎊ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1ll11l1l111_opy_({ bstack1ll111_opy_ (u"ࠧࡸ࡯ࡣࡱࡷ࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢᎋ"): VERSION }, [bstack1ll111_opy_ (u"ࠨࡲࡰࡤࡲࡸࠧᎌ")], self.bstack1ll1ll1l111_opy_, self.bstack1ll1lll11ll_opy_)
                return
            except Exception as e:
                self.logger.error(bstack1ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡵࡳࡧࡵࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠾ࠥࠨᎍ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᎎ"))
        if bstack11l11l1111_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᎏ"): pytest.__version__ }, [bstack1ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ᎐")], self.bstack1ll1ll1l111_opy_, self.bstack1ll1lll11ll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1ll11llll_opy_({ bstack1ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦ᎑"): pytest.__version__ }, [bstack1ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧ᎒")], self.bstack1ll1ll1l111_opy_, self.bstack1ll1lll11ll_opy_)
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥ᎓") + str(e) + bstack1ll111_opy_ (u"ࠢࠣ᎔"))
        self.bstack1l1lll11l11_opy_()
    def bstack1l1lll11l11_opy_(self):
        if not self.bstack1l111l111_opy_():
            return
        bstack1l11l11l1_opy_ = None
        def bstack1ll11ll1_opy_(config, startdir):
            return bstack1ll111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨ᎕").format(bstack1ll111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ᎖"))
        def bstack11ll111ll1_opy_():
            return
        def bstack1lll1ll111_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1ll111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪ᎗"):
                return bstack1ll111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥ᎘")
            else:
                return bstack1l11l11l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l11l11l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1ll11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll111ll1_opy_
            Config.getoption = bstack1lll1ll111_opy_
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢ᎙") + str(e) + bstack1ll111_opy_ (u"ࠨࠢ᎚"))
    def bstack1l1ll11ll1l_opy_(self):
        bstack1ll11ll11l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll11ll11l_opy_, dict):
            if cli.config_observability:
                bstack1ll11ll11l_opy_.update(
                    {bstack1ll111_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ᎛"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1ll111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦ᎜") in accessibility.get(bstack1ll111_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥ᎝"), {}):
                    bstack1l1ll11l1ll_opy_ = accessibility.get(bstack1ll111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦ᎞"))
                    bstack1l1ll11l1ll_opy_.update({ bstack1ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧ᎟"): bstack1l1ll11l1ll_opy_.pop(bstack1ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣᎠ")) })
                bstack1ll11ll11l_opy_.update({bstack1ll111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᎡ"): accessibility })
        return bstack1ll11ll11l_opy_
    @measure(event_name=EVENTS.bstack1l1llll1l11_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l1lll1l1ll_opy_(self, bstack1l1llll111l_opy_: str = None, bstack1ll11111l1l_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1lll11ll_opy_:
            return
        bstack1ll1l1l111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᎢ"), bstack1ll111_opy_ (u"ࠨ࠲ࠪᎣ")))
        req.client_worker_id = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᎤ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l1llll111l_opy_:
            req.bstack1l1llll111l_opy_ = bstack1l1llll111l_opy_
        if bstack1ll11111l1l_opy_:
            req.bstack1ll11111l1l_opy_ = bstack1ll11111l1l_opy_
        try:
            r = self.bstack1ll1lll11ll_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡳࡵࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᎥ"), datetime.now() - bstack1ll1l1l111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11l11l1ll1_opy_(self, key: str, value: timedelta):
        tag = bstack1ll111_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࠦᎦ") if self.bstack111ll1l1_opy_() else bstack1ll111_opy_ (u"ࠧࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶࠦᎧ")
        self.bstack1l1lllll1l1_opy_[bstack1ll111_opy_ (u"ࠨ࠺ࠣᎨ").join([tag + bstack1ll111_opy_ (u"ࠢ࠮ࠤᎩ") + str(id(self)), key])] += value
    def bstack1l11lllll_opy_(self):
        if not os.getenv(bstack1ll111_opy_ (u"ࠣࡆࡈࡆ࡚ࡍ࡟ࡑࡇࡕࡊࠧᎪ"), bstack1ll111_opy_ (u"ࠤ࠳ࠦᎫ")) == bstack1ll111_opy_ (u"ࠥ࠵ࠧᎬ"):
            return
        bstack1ll111lllll_opy_ = dict()
        bstack1ll1llllll1_opy_ = []
        if self.test_framework:
            bstack1ll1llllll1_opy_.extend(list(self.test_framework.bstack1ll1llllll1_opy_.values()))
        if self.bstack1lll11111ll_opy_:
            bstack1ll1llllll1_opy_.extend(list(self.bstack1lll11111ll_opy_.bstack1ll1llllll1_opy_.values()))
        for instance in bstack1ll1llllll1_opy_:
            if not instance.platform_index in bstack1ll111lllll_opy_:
                bstack1ll111lllll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll111lllll_opy_[instance.platform_index]
            for k, v in instance.bstack1ll11l111ll_opy_().items():
                report[k] += v
                report[k.split(bstack1ll111_opy_ (u"ࠦ࠿ࠨᎭ"))[0]] += v
        bstack1ll1111l111_opy_ = sorted([(k, v) for k, v in self.bstack1l1lllll1l1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll11ll1lll_opy_ = 0
        for r in bstack1ll1111l111_opy_:
            bstack1ll11l111l1_opy_ = r[1].total_seconds()
            bstack1ll11ll1lll_opy_ += bstack1ll11l111l1_opy_
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡾࡶࡠ࠶࡝ࡾ࠿ࠥᎮ") + str(bstack1ll11l111l1_opy_) + bstack1ll111_opy_ (u"ࠨࠢᎯ"))
        self.logger.debug(bstack1ll111_opy_ (u"ࠢ࠮࠯ࠥᎰ"))
        bstack1l1ll111ll1_opy_ = []
        for platform_index, report in bstack1ll111lllll_opy_.items():
            bstack1l1ll111ll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l1ll111ll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11l1l11111_opy_ = set()
        bstack1ll111l11ll_opy_ = 0
        for r in bstack1l1ll111ll1_opy_:
            bstack1ll11l111l1_opy_ = r[2].total_seconds()
            bstack1ll111l11ll_opy_ += bstack1ll11l111l1_opy_
            bstack11l1l11111_opy_.add(r[0])
            self.logger.debug(bstack1ll111_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡶࡨࡷࡹࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭࠮ࡽࡵ࡟࠵ࡣࡽ࠻ࡽࡵ࡟࠶ࡣࡽ࠾ࠤᎱ") + str(bstack1ll11l111l1_opy_) + bstack1ll111_opy_ (u"ࠤࠥᎲ"))
        if self.bstack111ll1l1_opy_():
            self.logger.debug(bstack1ll111_opy_ (u"ࠥ࠱࠲ࠨᎳ"))
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻ࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠾ࡽࡷࡳࡹࡧ࡬ࡠࡥ࡯࡭ࢂࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲࡹ࠭ࡼࡵࡷࡶ࠭ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠪࡿࡀࠦᎴ") + str(bstack1ll111l11ll_opy_) + bstack1ll111_opy_ (u"ࠧࠨᎵ"))
        else:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࠥᎶ") + str(bstack1ll11ll1lll_opy_) + bstack1ll111_opy_ (u"ࠢࠣᎷ"))
        self.logger.debug(bstack1ll111_opy_ (u"ࠣ࠯࠰ࠦᎸ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᎹ"), bstack1ll111_opy_ (u"ࠪ࠴ࠬᎺ"))),
            client_worker_id=bstack1ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᎻ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1lll11ll_opy_:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡩ࡬ࡪࡡࡶࡩࡷࡼࡩࡤࡧࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᎼ"))
            return None
        response = self.bstack1ll1lll11ll_opy_.TestOrchestration(request)
        self.logger.debug(bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷ࠱ࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲࡂࢁࡽࠣᎽ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll11ll1l11_opy_(self, r):
        if r is not None and getattr(r, bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࠨᎾ"), None) and getattr(r.testhub, bstack1ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᎿ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1ll111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᏀ")))
            for bstack1ll111l1l11_opy_, err in errors.items():
                if err[bstack1ll111_opy_ (u"ࠪࡸࡾࡶࡥࠨᏁ")] == bstack1ll111_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᏂ"):
                    self.logger.info(err[bstack1ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ꮓ")])
                else:
                    self.logger.error(err[bstack1ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᏄ")])
    def bstack1lll1111ll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()