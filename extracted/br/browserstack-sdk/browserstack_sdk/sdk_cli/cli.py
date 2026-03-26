# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
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
from browserstack_sdk.sdk_cli.bstack1ll1l1111ll_opy_ import bstack1ll11lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l1l_opy_ import bstack1ll1ll1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1lll_opy_ import bstack1l1l1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1l11_opy_ import bstack1l1lll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111llll_opy_ import bstack1ll1111l111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1111_opy_ import bstack1l1llll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1llll1l_opy_ import bstack1ll111l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1l1l1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l111l1lll_opy_ import bstack1lll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack11llllll11_opy_ import bstack11llllll11_opy_, Events, bstack1l1llll1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1l1l1l1l111_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack11ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1ll11l1l1_opy_ import bstack1l1l11lll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1ll_opy_ import bstack11l1111l1l_opy_
from bstack_utils.helper import Notset, bstack1lll1l11l11_opy_, get_cli_dir, bstack1lll1l11lll_opy_, bstack1111ll11_opy_, bstack111lll1l11_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1lllll1_opy_, TestHookState, bstack1l1l11lll1l_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack1ll11ll1l11_opy_, bstack11lll111_opy_, bstack1l11l11l1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack111111111_opy_ import bstack1l11l1ll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1111ll1l_opy_, bstack11lll1ll1l_opy_
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l11l1_opy_ import bstack1ll1111l1ll_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1l1ll1l11ll_opy_(bs_config):
    bstack1l1l1ll111l_opy_ = None
    bstack1lll1l1l1l1_opy_ = None
    try:
        bstack1lll1l1l1l1_opy_ = get_cli_dir()
        bstack1l1l1ll111l_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠣፌ"))
        if not bstack1l1l1ll111l_opy_:
            bstack1l1l1ll111l_opy_ = bstack1lll1l11lll_opy_(bstack1lll1l1l1l1_opy_)
            bstack1l1ll1ll1l1_opy_ = bstack1lll1l11l11_opy_(bstack1l1l1ll111l_opy_, bstack1lll1l1l1l1_opy_, bs_config)
            bstack1l1l1ll111l_opy_ = bstack1l1ll1ll1l1_opy_ if bstack1l1ll1ll1l1_opy_ else bstack1l1l1ll111l_opy_
        if not bstack1l1l1ll111l_opy_:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡄࡎࡌࠤࡵࡧࡴࡩࠢ࡬ࡲࠥࡺࡨࡦࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡰࡴࠣ࡭ࡳࠦࡴࡩࡧࠣ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡪࡴࡲࡤࡦࡴࠥፍ"))
    except Exception as ex:
        logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡇࡑࡏࠠࡱࡣࡷ࡬࠿ࠦࠢፎ") + str(ex) + bstack1ll1lll_opy_ (u"ࠣࠤፏ"))
    return bstack1l1l1ll111l_opy_, bstack1lll1l1l1l1_opy_
bstack1l1l1l11lll_opy_ = bstack1ll1lll_opy_ (u"ࠤ࠼࠽࠾࠿ࠢፐ")
bstack1l1ll1lll11_opy_ = bstack1ll1lll_opy_ (u"ࠥࡶࡪࡧࡤࡺࠤፑ")
bstack1l1l1l111l1_opy_ = bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣፒ")
bstack1l1ll1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡒࡉࡔࡖࡈࡒࡤࡇࡄࡅࡔࠥፓ")
BROWSERSTACK_AUTOMATION = bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤፔ")
bstack1l1l1l1l11l_opy_ = re.compile(bstack1ll1lll_opy_ (u"ࡲࠣࠪࡂ࡭࠮࠴ࠪࠩࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑࡼࡃࡕࠬ࠲࠯ࠨፕ"))
bstack1l1ll1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡦࡨࡺࡪࡲ࡯ࡱ࡯ࡨࡲࡹࠨፖ")
bstack1l1ll11ll11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠤፗ")
bstack1l1ll1l1lll_opy_ = [
    Events.bstack1ll1l1lll_opy_,
    Events.CONNECT,
    Events.bstack111l1111ll_opy_,
]
def _1l1l1llllll_opy_():
    bstack1ll1lll_opy_ (u"ࠥࠦࠧࡌࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࠥࡲࡩࡣࡴࡤࡶࡾࠦ࠼ࠡ࠳࠼࠲࠹࠴࠰ࠡࡹ࡫ࡩࡷ࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲ࠯ࡧࡱࡸࡷࡿ࠮ࡨࡧࡷࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡸࠦࡤࡰࡧࡶࡲࠬࡺࠠࡦࡺ࡬ࡷࡹ࠴ࠢࠣࠤፘ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l1l1l1ll1l_opy_ = Path(Browser.__file__).parent / bstack1ll1lll_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡶࠧፙ") / bstack1ll1lll_opy_ (u"ࠧࡶࡡࡤ࡭ࡤ࡫ࡪ࠴ࡪࡴࡱࡱࠦፚ")
        bstack1l1ll1ll11l_opy_ = json.loads(bstack1l1l1l1ll1l_opy_.read_text())
        match = re.search(bstack1ll1lll_opy_ (u"ࡸࠢ࡝ࡦ࠮ࡠ࠳ࡢࡤࠬ࡞࠱ࡠࡩ࠱ࠢ፛"), bstack1l1ll1ll11l_opy_[bstack1ll1lll_opy_ (u"ࠢࡥࡧࡳࡩࡳࡪࡥ࡯ࡥ࡬ࡩࡸࠨ፜")][bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ፝")])
        bstack1l1llll111l_opy_ = match.group(0) if match else bstack1ll1lll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ፞")
    except Exception:
        bstack1l1llll111l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ፟")
    return SimpleNamespace(version=bstack1l1llll111l_opy_)
class SDKCLI:
    _1ll1l111ll1_opy_ = None
    process: Union[None, Any]
    bstack1l1ll111lll_opy_: bool
    bstack1ll111l1lll_opy_: bool
    bstack1l1ll11l11l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l1l1lll11l_opy_: Union[None, grpc.Channel]
    bstack1l1lll11lll_opy_: str
    test_framework: TestFramework
    bstack111l11ll11_opy_: bstack11ll11l1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l1l1l11ll1_opy_: bstack1lll11ll1_opy_
    accessibility: bstack1ll1ll1l1l1_opy_
    bstack1l1l1l1ll_opy_: bstack11l1111l1l_opy_
    ai: bstack1l1l1lll1l1_opy_
    bstack1ll1111ll1l_opy_: bstack1l1lll1ll1l_opy_
    bstack1l1ll11ll1l_opy_: List[bstack1ll111l11ll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l1lll111l1_opy_: Any
    bstack1l1ll111l11_opy_: Dict[str, timedelta]
    bstack1l1l1l1l1l1_opy_: str
    bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_
    def __new__(cls):
        if not cls._1ll1l111ll1_opy_:
            cls._1ll1l111ll1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1l111ll1_opy_
    def __init__(self):
        self.process = None
        self.bstack1l1ll111lll_opy_ = False
        self.bstack1l1l1lll11l_opy_ = None
        self.bstack1l1llll1lll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l1ll1111ll_opy_, None)
        self.bstack1l1lll1111l_opy_ = os.environ.get(bstack1l1l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠦࠧ፠")) == bstack1ll1lll_opy_ (u"ࠧࠨ፡")
        self.bstack1ll111l1lll_opy_ = False
        self.bstack1l1ll11l11l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l1lll111l1_opy_ = None
        self.test_framework = None
        self.bstack111l11ll11_opy_ = None
        self.bstack1l1lll11lll_opy_=bstack1ll1lll_opy_ (u"ࠨࠢ።")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l1ll111l11_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1ll1l1111ll_opy_ = bstack1ll11lllll1_opy_()
        self.bstack1ll111111l1_opy_ = False
        self.bstack1l1ll1ll1ll_opy_ = None
        self.bstack1l1lll111ll_opy_ = None
        self.bstack1l1l1l11ll1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l1ll11ll1l_opy_ = []
    def bstack1111111l11_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ፣"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l1ll11ll11_opy_, bstack1ll1lll_opy_ (u"ࠨࠩ፤")).lower() in [bstack1ll1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ፥"), bstack1ll1lll_opy_ (u"ࠪ࠵ࠬ፦"), bstack1ll1lll_opy_ (u"ࠫࡾ࡫ࡳࠨ፧")]:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌ࡯ࡳࡥ࡬ࡲ࡬ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࡯ࡲࡨࡪࠦࡤࡶࡧࠣࡸࡴࠦࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡏࡓࡅࡈࡣࡋࡇࡌࡍࡄࡄࡇࡐࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠨ፨"))
            os.environ[bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤ፩")] = bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ፪")
            return False
        if bstack1ll1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ፫") in config and str(config[bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭፬")]).lower() != bstack1ll1lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ፭"):
            return False
        bstack1ll111l111l_opy_ = [bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦ፮"), bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ፯"), bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠢ፰")]
        if is_robot_playwright_installed():
            bstack1ll111l111l_opy_.append(bstack1ll1lll_opy_ (u"ࠢࡳࡱࡥࡳࡹࠨ፱"))
            bstack1ll111l111l_opy_.append(bstack1ll1lll_opy_ (u"ࠣࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠤ፲"))
        bstack1l1lll1l11l_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧ፳")) in bstack1ll111l111l_opy_ or os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ፴")) in bstack1ll111l111l_opy_
        os.environ[bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢ፵")] = str(bstack1l1lll1l11l_opy_) # bstack1ll11111ll1_opy_ bstack1l1ll111111_opy_ VAR to bstack1ll1111lll1_opy_ is binary running
        return bstack1l1lll1l11l_opy_
    def bstack1lll111l1_opy_(self):
        for event in bstack1l1ll1l1lll_opy_:
            bstack11llllll11_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11llllll11_opy_.logger.debug(bstack1ll1lll_opy_ (u"ࠧࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠤࡂࡄࠠࡼࡣࡵ࡫ࡸࢃࠠࠣ፶") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢ፷"))
            )
        bstack11llllll11_opy_.register(Events.bstack1ll1l1lll_opy_, self.__1l1ll111l1l_opy_)
        bstack11llllll11_opy_.register(Events.CONNECT, self.__1l1ll11llll_opy_)
        bstack11llllll11_opy_.register(Events.bstack111l1111ll_opy_, self.__1l1llll1111_opy_)
        bstack11llllll11_opy_.register(Events.bstack1111ll1l1_opy_, self.__1l1l11llll1_opy_)
    def bstack1l11lll1l_opy_(self):
        return not self.bstack1l1lll1111l_opy_ and os.environ.get(bstack1l1l1l111l1_opy_, bstack1ll1lll_opy_ (u"ࠢࠣ፸")) != bstack1ll1lll_opy_ (u"ࠣࠤ፹")
    def is_running(self):
        if self.bstack1l1lll1111l_opy_:
            return self.bstack1l1ll111lll_opy_
        else:
            return bool(self.bstack1l1l1lll11l_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ፺"))
                and self.config_observability.options.allow_screenshots == bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ፻")
            )
        except Exception:
            return False
    def bstack1l1l111ll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l1ll11ll1l_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l1ll1lllll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1l1l111ll_opy_(self, bstack1l1lllll1ll_opy_=10):
        if self.bstack1l1llll1lll_opy_:
            return
        bstack11lllll111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l1ll1111ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࠨ፼") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠧࡣࠠࡤࡱࡱࡲࡪࡩࡴࡪࡰࡪࠦ፽"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1ll1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡡࡳࡶࡴࡾࡹࠣ፾"), 0), (bstack1ll1lll_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡶࡣࡵࡸ࡯ࡹࡻࠥ፿"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1lllll1ll_opy_)
        self.bstack1l1l1lll11l_opy_ = channel
        self.bstack1l1llll1lll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l1l1lll11l_opy_)
        self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺࠢᎀ"), datetime.now() - bstack11lllll111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l1ll1111ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧ࠾ࠥ࡯ࡳࡠࡥ࡫࡭ࡱࡪ࡟ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤᎁ") + str(self.bstack1l11lll1l_opy_()) + bstack1ll1lll_opy_ (u"ࠥࠦᎂ"))
    def __1l1llll1111_opy_(self, event_name):
        if self.bstack1l11lll1l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡄࡎࡌࠦᎃ"))
        self.__1l1llll1ll1_opy_()
    @measure(event_name=EVENTS.bstack1ll11111lll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1l11llll1_opy_(self, event_name, bstack1ll1111ll11_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1ll1lll_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠧᎄ"))
        bstack1l1llll1l1l_opy_ = Path(bstack1ll11l1ll11_opy_ (u"ࠨࡻࡴࡧ࡯ࡪ࠳ࡩ࡬ࡪࡡࡧ࡭ࡷࢃ࠯ࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࡴ࠰࡭ࡷࡴࡴࠢᎅ"))
        if self.bstack1lll1l1l1l1_opy_ and bstack1l1llll1l1l_opy_.exists():
            with open(bstack1l1llll1l1l_opy_, bstack1ll1lll_opy_ (u"ࠧࡳࠩᎆ"), encoding=bstack1ll1lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᎇ")) as fp:
                data = json.load(fp)
                try:
                    bstack111lll1l11_opy_(bstack1ll1lll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᎈ"), bstack1l11l1ll_opy_(bstack1l111111ll_opy_), data, {
                        bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺࡨࠨᎉ"): (self.config[bstack1ll1lll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᎊ")], self.config[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᎋ")])
                    })
                except Exception as e:
                    logger.debug(bstack11lll1ll1l_opy_.format(str(e)))
            bstack1l1llll1l1l_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l1lllll1l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1ll111l1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
        self.bstack1l1lll11lll_opy_, self.bstack1lll1l1l1l1_opy_ = bstack1l1ll1l11ll_opy_(data.bs_config)
        os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡝ࡒࡊࡖࡄࡆࡑࡋ࡟ࡅࡋࡕࠫᎌ")] = self.bstack1lll1l1l1l1_opy_
        if not self.bstack1l1lll11lll_opy_ or not self.bstack1lll1l1l1l1_opy_:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠨᎍ"))
        if self.bstack1l11lll1l_opy_():
            self.__1l1ll11llll_opy_(event_name, bstack1l1llll1_opy_())
            return
        try:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡅࡲࡱࡵࡲࡥࡵࡧࠣࡗࡉࡑࠠࡔࡧࡷࡹࡵ࠴ࠢᎎ"))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡿࢂࠨᎏ").format(e))
        start = datetime.now()
        is_started = self.__1l1ll1l11l1_opy_()
        self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠥࡷࡵࡧࡷ࡯ࡡࡷ࡭ࡲ࡫ࠢ᎐"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l1l1l111ll_opy_()
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥ᎑"), datetime.now() - start)
            start = datetime.now()
            self.__1l1l1l1111l_opy_(data)
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥ᎒"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1llll11l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1ll11llll_opy_(self, event_name: str, data: bstack1l1llll1_opy_):
        if not self.bstack1l11lll1l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࡳࡵࡴࠡࡣࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥ᎓"))
            return
        bin_session_id = os.environ.get(bstack1l1l1l111l1_opy_)
        start = datetime.now()
        self.__1l1l1l111ll_opy_()
        self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨ᎔"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡆࡐࡎࠦࠢ᎕") + str(bin_session_id) + bstack1ll1lll_opy_ (u"ࠤࠥ᎖"))
        start = datetime.now()
        self.__1l1l1llll11_opy_()
        self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣ᎗"), datetime.now() - start)
    def __1l1llllll11_opy_(self):
        if not self.bstack1l1llll1lll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠ࡮ࡱࡧࡹࡱ࡫ࡳࠣ᎘"))
            return
        bstack1l1ll11lll1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ᎙"): (bstack1ll111l1ll1_opy_, bstack1l1l1ll1l1l_opy_, bstack111l111ll_opy_),
            bstack1ll1lll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣ᎚"): (bstack1ll1111l111_opy_, bstack1l1llll11ll_opy_, bstack1ll111l1111_opy_),
        }
        if not self.bstack1l1ll1ll1ll_opy_ and self.session_framework in bstack1l1ll11lll1_opy_:
            bstack1l1lll11l1l_opy_, bstack1l1ll1l1111_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1ll11lll1_opy_[self.session_framework]
            bstack1l1l1l11111_opy_ = bstack1l1ll1l1111_opy_()
            self.bstack1l1lll111ll_opy_ = bstack1l1l1l11111_opy_
            self.bstack1l1ll1ll1ll_opy_ = bstack1l1ll1l1ll1_opy_
            self.bstack1l1ll11ll1l_opy_.append(bstack1l1l1l11111_opy_)
            self.bstack1l1ll11ll1l_opy_.append(bstack1l1lll11l1l_opy_(self.bstack1l1lll111ll_opy_))
        if not self.bstack1l1l1l11ll1_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1l1l1l11ll1_opy_ = bstack1lll11ll1_opy_(self.bstack1l1ll1ll1ll_opy_, self.bstack1l1lll111ll_opy_)
            self.bstack1l1ll11ll1l_opy_.append(self.bstack1l1l1l11ll1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1ll1l1l1_opy_(self.bstack1l1ll1ll1ll_opy_, self.bstack1l1lll111ll_opy_)
            self.bstack1l1ll11ll1l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1ll1lll_opy_ (u"ࠢࡴࡧ࡯ࡪࡍ࡫ࡡ࡭ࠤ᎛"), False) == True:
            self.ai = bstack1l1l1lll1l1_opy_()
            self.bstack1l1ll11ll1l_opy_.append(self.ai)
        if not self.percy and self.bstack1l1lll111l1_opy_ and self.bstack1l1lll111l1_opy_.success:
            self.percy = bstack1l1lll1ll1l_opy_(self.bstack1l1lll111l1_opy_)
            self.bstack1l1ll11ll1l_opy_.append(self.percy)
        for mod in self.bstack1l1ll11ll1l_opy_:
            if not mod.bstack1ll111l1l11_opy_():
                mod.configure(self.bstack1l1llll1lll_opy_, self.config, self.cli_bin_session_id, self.bstack1ll1l1111ll_opy_)
    def __1l1lll1llll_opy_(self):
        for mod in self.bstack1l1ll11ll1l_opy_:
            if mod.bstack1ll111l1l11_opy_():
                mod.configure(self.bstack1l1llll1lll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l1llll1l11_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1l1l1111l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll111l1lll_opy_:
            return
        self.__1l1ll11111l_opy_(data)
        bstack11lllll111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1ll1lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣ᎜")
        req.sdk_language = bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ᎝")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l1l1l1l11l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᎞"), bstack1ll1lll_opy_ (u"ࠫ࠵࠭᎟")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᎠ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡧࡨ࡮ࡴࡧࠡࡹࡲࡶࡰ࡫ࡲࠡࡣࡱࡨࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡰࡧࡩࡽࡀࠠࡼࡿࠥᎡ").format(e))
        try:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡜ࠤᎢ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᎣ"))
            r = self.bstack1l1llll1lll_opy_.StartBinSession(req)
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᎤ"), datetime.now() - bstack11lllll111_opy_)
            os.environ[bstack1l1l1l111l1_opy_] = r.bin_session_id
            self.__1l1lll1l1l1_opy_(r)
            self.__1l1llllll11_opy_()
            if not self.bstack1ll111111l1_opy_:
                self.bstack1ll1l1111ll_opy_.start()
                self.bstack1ll111111l1_opy_ = True
                atexit.register(self.__1l1l1l1l1ll_opy_)
            self.bstack1ll111l1lll_opy_ = True
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࠧᎥ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤᎦ"))
        except grpc.bstack1ll11111l1l_opy_ as bstack1l1lllll11l_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎧ") + str(bstack1l1lllll11l_opy_) + bstack1ll1lll_opy_ (u"ࠨࠢᎨ"))
            traceback.print_exc()
            raise bstack1l1lllll11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᎩ") + str(e) + bstack1ll1lll_opy_ (u"ࠣࠤᎪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll1lll1l_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1l1llll11_opy_(self):
        if not self.bstack1l11lll1l_opy_() or not self.cli_bin_session_id or self.bstack1l1ll11l11l_opy_:
            return
        bstack11lllll111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᎫ"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬᎬ")))
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᎭ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡡࠢᎮ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᎯ"))
            r = self.bstack1l1llll1lll_opy_.ConnectBinSession(req)
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᎰ"), datetime.now() - bstack11lllll111_opy_)
            self.__1l1lll1l1l1_opy_(r)
            self.__1l1llllll11_opy_()
            if not self.bstack1ll111111l1_opy_:
                self.bstack1ll1l1111ll_opy_.start()
                self.bstack1ll111111l1_opy_ = True
                atexit.register(self.__1l1l1l1l1ll_opy_)
            self.bstack1l1ll11l11l_opy_ = True
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࠥᎱ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣᎲ"))
        except grpc.bstack1ll11111l1l_opy_ as bstack1l1lllll11l_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᎳ") + str(bstack1l1lllll11l_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᎴ"))
            traceback.print_exc()
            raise bstack1l1lllll11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᎵ") + str(e) + bstack1ll1lll_opy_ (u"ࠨࠢᎶ"))
            traceback.print_exc()
            raise e
    def __1l1lll1l1l1_opy_(self, r):
        self.bstack1l1l1l11l1l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1ll1lll_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᎷ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1ll1lll_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨᎸ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᎹ")
        self.bstack1l1lll111l1_opy_ = getattr(r, bstack1ll1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᎺ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᎻ")] = self.config_testhub.jwt
        os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᎼ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1l1l11l11_opy_ = json.loads(r.config)
            bstack1l1ll1l1l1l_opy_ = bstack1l1l1l11l11_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᎽ"), {}).get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᎾ"), bstack1ll1lll_opy_ (u"ࠨࠩᎿ"))
            os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᏀ")] = bstack1l1ll1l1l1l_opy_
    def bstack1l1lll11111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l1ll111lll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1lll1lll1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1lll1lll1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l1lll11111_opy_(event_name=EVENTS.bstack1ll11111111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1ll1l11l1_opy_(self, bstack1l1lllll1ll_opy_=10):
        if self.bstack1l1ll111lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠧᏁ"))
            return True
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥᏂ"))
        if os.getenv(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡇࡑ࡚ࠧᏃ")) == bstack1l1ll1l111l_opy_:
            self.cli_bin_session_id = bstack1l1ll1l111l_opy_
            self.cli_listen_addr = bstack1ll1lll_opy_ (u"ࠨࡵ࡯࡫ࡻ࠾࠴ࡺ࡭ࡱ࠱ࡶࡨࡰ࠳ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠮ࠧࡶ࠲ࡸࡵࡣ࡬ࠤᏄ") % (self.cli_bin_session_id)
            self.bstack1l1ll111lll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1lll11lll_opy_, bstack1ll1lll_opy_ (u"ࠢࡴࡦ࡮ࠦᏅ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l1l1l1ll11_opy_ compat for text=True in bstack1l1lll11ll1_opy_ python
            encoding=bstack1ll1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᏆ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1lll1ll11_opy_ = threading.Thread(target=self.__1l1l1ll11l1_opy_, args=(bstack1l1lllll1ll_opy_,))
        bstack1l1lll1ll11_opy_.start()
        bstack1l1lll1ll11_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡵࡳࡥࡼࡴ࠺ࠡࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦࡿࠣࡳࡺࡺ࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡴࡶࡧࡳࡺࡺ࠮ࡳࡧࡤࡨ࠭࠯ࡽࠡࡧࡵࡶࡂࠨᏇ") + str(self.process.stderr.read()) + bstack1ll1lll_opy_ (u"ࠥࠦᏈ"))
        if not self.bstack1l1ll111lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡠࠨᏉ") + str(id(self)) + bstack1ll1lll_opy_ (u"ࠧࡣࠠࡤ࡮ࡨࡥࡳࡻࡰࠣᏊ"))
            self.__1l1llll1ll1_opy_()
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡶࡲࡰࡥࡨࡷࡸࡥࡲࡦࡣࡧࡽ࠿ࠦࠢᏋ") + str(self.bstack1l1ll111lll_opy_) + bstack1ll1lll_opy_ (u"ࠢࠣᏌ"))
        return self.bstack1l1ll111lll_opy_
    def __1l1l1ll11l1_opy_(self, bstack1ll111111ll_opy_=10):
        bstack1l1l1l1lll1_opy_ = time.time()
        while self.process and time.time() - bstack1l1l1l1lll1_opy_ < bstack1ll111111ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1ll1lll_opy_ (u"ࠣ࡫ࡧࡁࠧᏍ") in line:
                    self.cli_bin_session_id = line.split(bstack1ll1lll_opy_ (u"ࠤ࡬ࡨࡂࠨᏎ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡧࡱ࡯࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠻ࠤᏏ") + str(self.cli_bin_session_id) + bstack1ll1lll_opy_ (u"ࠦࠧᏐ"))
                    continue
                if bstack1ll1lll_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨᏑ") in line:
                    self.cli_listen_addr = line.split(bstack1ll1lll_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢᏒ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡱ࡯ࡳࡵࡧࡱࡣࡦࡪࡤࡳ࠼ࠥᏓ") + str(self.cli_listen_addr) + bstack1ll1lll_opy_ (u"ࠣࠤᏔ"))
                    continue
                if bstack1ll1lll_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣᏕ") in line:
                    port = line.split(bstack1ll1lll_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤᏖ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡵࡵࡲࡵ࠼ࠥᏗ") + str(port) + bstack1ll1lll_opy_ (u"ࠧࠨᏘ"))
                    continue
                if line.strip() == bstack1l1ll1lll11_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1ll1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡏࡏࡠࡕࡗࡖࡊࡇࡍࠣᏙ"), bstack1ll1lll_opy_ (u"ࠢ࠲ࠤᏚ")) == bstack1ll1lll_opy_ (u"ࠣ࠳ࠥᏛ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l1ll111lll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲ࠻ࠢࠥᏜ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᏝ"))
        return False
    def __1l1l1l1l1ll_opy_(self):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡃ࡭ࡧࡤࡲࡺࡶࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡨࡲࡶࠥࡧࡳࡺࡰࡦࡣࡩ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲ࠭ࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡧࡴࡦࡺ࡬ࡸࠥࡺ࡯ࠡࡧࡱࡷࡺࡸࡥࠡࡶࡤࡷࡰࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠥࠦࠧᏞ")
        if self.bstack1ll1l1111ll_opy_ and self.bstack1ll111111l1_opy_:
            try:
                self.bstack1ll1l1111ll_opy_.stop()
                self.bstack1ll111111l1_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1ll1l1l11_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def __1l1llll1ll1_opy_(self):
        if self.bstack1l1l1lll11l_opy_:
            if self.bstack1ll1l1111ll_opy_ and self.bstack1ll111111l1_opy_:
                try:
                    atexit.unregister(self.__1l1l1l1l1ll_opy_)
                except ValueError:
                    pass
                self.bstack1ll1l1111ll_opy_.stop()
                self.bstack1ll111111l1_opy_ = False
            start = datetime.now()
            if self.bstack1l1l11lllll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1ll11l11l_opy_:
                    self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤᏟ"), datetime.now() - start)
                else:
                    self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᏠ"), datetime.now() - start)
            self.__1l1lll1llll_opy_()
            start = datetime.now()
            bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(bstack1ll1lll_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࠧᏡ"))
            self.bstack1l1l1lll11l_opy_.close()
            bstack1l1l11ll1_opy_.end(bstack1ll1lll_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࠨᏢ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᏣ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᏤ"), True, None, None, None, None)
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠦࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨᏥ"), datetime.now() - start)
            self.bstack1l1l1lll11l_opy_ = None
        if self.process:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡴࡰࡲࠥᏦ"))
            start = datetime.now()
            bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(bstack1ll1lll_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺࡬࡫࡯ࡰࠧᏧ"))
            self.process.terminate()
            bstack1l1l11ll1_opy_.end(bstack1ll1lll_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻࡭࡬ࡰࡱࠨᏨ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᏩ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᏪ"), True, None, None, None, None)
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠥ࡯࡮ࡲ࡬ࡠࡶ࡬ࡱࡪࠨᏫ"), datetime.now() - start)
            self.process = None
            if self.bstack1l1lll1111l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11llllll1_opy_()
                self.logger.info(
                    bstack1ll1lll_opy_ (u"࡛ࠦ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠦᏬ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᏭ")] = self.config_testhub.build_hashed_id
        self.bstack1l1ll111lll_opy_ = False
    def __1l1ll11111l_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᏮ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1l1ll11ll_opy_ = get_pw_version()
            except:
                bstack1l1l1ll11ll_opy_ = _1l1l1llllll_opy_()
            data.framework_versions[bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᏯ")] = bstack1l1l1ll11ll_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack1ll1lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᏰ")] = selenium.__version__
                data.frameworks.append(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᏱ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1ll1lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᏲ")] = __version__
                data.frameworks.append(bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᏳ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡔ࡯ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡤࡦࡶࡨࡧࡹ࡫ࡤࠣᏴ"))
    def bstack1ll111l1l1l_opy_(self, hub_url: str, platform_index: int, bstack1l1l1llll_opy_: Any):
        if self.bstack111l11ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᏵ"))
            return
        try:
            bstack11lllll111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1ll1lll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤ᏶")
            self.bstack111l11ll11_opy_ = bstack1ll111l1111_opy_(
                cli.config.get(bstack1ll1lll_opy_ (u"ࠣࡪࡸࡦ࡚ࡸ࡬ࠣ᏷"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1l1ll1ll1_opy_={bstack1ll1lll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨᏸ"): bstack1l1l1llll_opy_}
            )
            def bstack1ll11111l11_opy_(self):
                return
            if self.config.get(bstack1ll1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠧᏹ"), True):
                Service.start = bstack1ll11111l11_opy_
                Service.stop = bstack1ll11111l11_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11l1111l1l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1l11lll11_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᏺ"), datetime.now() - bstack11lllll111_opy_)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠼ࠣࠦᏻ") + str(e) + bstack1ll1lll_opy_ (u"ࠨࠢᏼ"))
    def bstack111l11l11l_opy_(self, platform_index: int):
        if self.bstack111l11ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨᏽ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1ll1111l1l1_opy_
                self.bstack111l11ll11_opy_ = bstack111l111ll_opy_(
                    platform_index,
                    framework_name=bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ᏾"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l1l1llllll_opy_
                from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11llll1l_opy_
                bstack1l1l1ll11ll_opy_ = get_pw_version()
                self.bstack111l11ll11_opy_ = bstack111l111ll_opy_(
                    platform_index,
                    framework_name=bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᏿"),
                    framework_version=bstack1l1l1ll11ll_opy_.version,
                    classes=[],
                )
                ctx = bstack1ll11llll1l_opy_.create_context(self.bstack111l11ll11_opy_)
                bstack11ll11l1_opy_.bstack1111l1ll1l_opy_[ctx.id] = bstack1ll11ll1l11_opy_(
                    ctx, bstack1ll1lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ᐀"), bstack1l1l1ll11ll_opy_, bstack11lll111_opy_.bstack1l111ll1l1_opy_
                )
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠽ࠤࠧᐁ") + str(e) + bstack1ll1lll_opy_ (u"ࠧࠨᐂ"))
            pass
    def bstack1111111ll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᐃ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1ll1111l1ll_opy_({ bstack1ll1lll_opy_ (u"ࠢࡳࡱࡥࡳࡹ࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤᐄ"): VERSION }, [bstack1ll1lll_opy_ (u"ࠣࡴࡲࡦࡴࡺࠢᐅ")], self.bstack1ll1l1111ll_opy_, self.bstack1l1llll1lll_opy_)
                return
            except Exception as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡷࡵࡢࡰࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡀࠠࠣᐆ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᐇ"))
        if bstack1111ll11_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᐈ"): pytest.__version__ }, [bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᐉ")], self.bstack1ll1l1111ll_opy_, self.bstack1l1llll1lll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1l1l1l111_opy_({ bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᐊ"): pytest.__version__ }, [bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᐋ")], self.bstack1ll1l1111ll_opy_, self.bstack1l1llll1lll_opy_)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࠧᐌ") + str(e) + bstack1ll1lll_opy_ (u"ࠤࠥᐍ"))
        self.bstack1l1ll11l1ll_opy_()
    def bstack1l1ll11l1ll_opy_(self):
        if not self.bstack1111111l11_opy_():
            return
        bstack1ll1llll11_opy_ = None
        def bstack11lll11l1l_opy_(config, startdir):
            return bstack1ll1lll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣᐎ").format(bstack1ll1lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᐏ"))
        def bstack1ll11l1111_opy_():
            return
        def bstack1l1111lll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1ll1lll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬᐐ"):
                return bstack1ll1lll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᐑ")
            else:
                return bstack1ll1llll11_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll1llll11_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11lll11l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll11l1111_opy_
            Config.getoption = bstack1l1111lll_opy_
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡳࡽࡹ࡫ࡳࡵࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࡫ࡵࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠺ࠡࠤᐒ") + str(e) + bstack1ll1lll_opy_ (u"ࠣࠤᐓ"))
    def bstack1l1l1lll111_opy_(self):
        bstack1ll111l1l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll111l1l1_opy_, dict):
            if cli.config_observability:
                bstack1ll111l1l1_opy_.update(
                    {bstack1ll1lll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᐔ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨᐕ") in accessibility.get(bstack1ll1lll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᐖ"), {}):
                    bstack1l1l1lll1ll_opy_ = accessibility.get(bstack1ll1lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᐗ"))
                    bstack1l1l1lll1ll_opy_.update({ bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠢᐘ"): bstack1l1l1lll1ll_opy_.pop(bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥᐙ")) })
                bstack1ll111l1l1_opy_.update({bstack1ll1lll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣᐚ"): accessibility })
        return bstack1ll111l1l1_opy_
    @measure(event_name=EVENTS.bstack1l1ll1111l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1l1l11lllll_opy_(self, bstack1l1ll1ll111_opy_: str = None, bstack1l1ll111ll1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1l1llll1lll_opy_:
            return
        bstack11lllll111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᐛ"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬᐜ")))
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᐝ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l1ll1ll111_opy_:
            req.bstack1l1ll1ll111_opy_ = bstack1l1ll1ll111_opy_
        if bstack1l1ll111ll1_opy_:
            req.bstack1l1ll111ll1_opy_ = bstack1l1ll111ll1_opy_
        try:
            r = self.bstack1l1llll1lll_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡵࡰࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᐞ"), datetime.now() - bstack11lllll111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll1111l11_opy_(self, key: str, value: timedelta):
        tag = bstack1ll1lll_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᐟ") if self.bstack1l11lll1l_opy_() else bstack1ll1lll_opy_ (u"ࠢ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᐠ")
        self.bstack1l1ll111l11_opy_[bstack1ll1lll_opy_ (u"ࠣ࠼ࠥᐡ").join([tag + bstack1ll1lll_opy_ (u"ࠤ࠰ࠦᐢ") + str(id(self)), key])] += value
    def bstack11llllll1_opy_(self):
        if not os.getenv(bstack1ll1lll_opy_ (u"ࠥࡈࡊࡈࡕࡈࡡࡓࡉࡗࡌࠢᐣ"), bstack1ll1lll_opy_ (u"ࠦ࠵ࠨᐤ")) == bstack1ll1lll_opy_ (u"ࠧ࠷ࠢᐥ"):
            return
        bstack1l1llllll1l_opy_ = dict()
        bstack1111l1ll1l_opy_ = []
        if self.test_framework:
            bstack1111l1ll1l_opy_.extend(list(self.test_framework.bstack1111l1ll1l_opy_.values()))
        if self.bstack111l11ll11_opy_:
            bstack1111l1ll1l_opy_.extend(list(self.bstack111l11ll11_opy_.bstack1111l1ll1l_opy_.values()))
        for instance in bstack1111l1ll1l_opy_:
            if not instance.platform_index in bstack1l1llllll1l_opy_:
                bstack1l1llllll1l_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l1llllll1l_opy_[instance.platform_index]
            for k, v in instance.bstack1l1lll1l111_opy_().items():
                report[k] += v
                report[k.split(bstack1ll1lll_opy_ (u"ࠨ࠺ࠣᐦ"))[0]] += v
        bstack1ll1111l11l_opy_ = sorted([(k, v) for k, v in self.bstack1l1ll111l11_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1lll11l11_opy_ = 0
        for r in bstack1ll1111l11l_opy_:
            bstack1l1lllll111_opy_ = r[1].total_seconds()
            bstack1l1lll11l11_opy_ += bstack1l1lllll111_opy_
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࢀࡸ࡛࠱࡟ࢀࡁࠧᐧ") + str(bstack1l1lllll111_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᐨ"))
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࠰࠱ࠧᐩ"))
        bstack1l1lllllll1_opy_ = []
        for platform_index, report in bstack1l1llllll1l_opy_.items():
            bstack1l1lllllll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l1lllllll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack111l11l111_opy_ = set()
        bstack1l1l1l1llll_opy_ = 0
        for r in bstack1l1lllllll1_opy_:
            bstack1l1lllll111_opy_ = r[2].total_seconds()
            bstack1l1l1l1llll_opy_ += bstack1l1lllll111_opy_
            bstack111l11l111_opy_.add(r[0])
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࡿࡷࡡ࠰࡞ࡿ࠽ࡿࡷࡡ࠱࡞ࡿࡀࠦᐪ") + str(bstack1l1lllll111_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᐫ"))
        if self.bstack1l11lll1l_opy_():
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࠳࠭ࠣᐬ"))
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࡀࡿࡹࡵࡴࡢ࡮ࡢࡧࡱ࡯ࡽࠡࡶࡨࡷࡹࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ࠯ࡾࡷࡹࡸࠨࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠬࢁࡂࠨᐭ") + str(bstack1l1l1l1llll_opy_) + bstack1ll1lll_opy_ (u"ࠢࠣᐮ"))
        else:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࠧᐯ") + str(bstack1l1lll11l11_opy_) + bstack1ll1lll_opy_ (u"ࠤࠥᐰ"))
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥ࠱࠲ࠨᐱ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐲ"), bstack1ll1lll_opy_ (u"ࠬ࠶ࠧᐳ"))),
            client_worker_id=bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᐴ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1l1llll1lll_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡸ࡫ࡲࡷ࡫ࡦࡩࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᐵ"))
            return None
        response = self.bstack1l1llll1lll_opy_.TestOrchestration(request)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹ࠳࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠳ࡳࡦࡵࡶ࡭ࡴࡴ࠽ࡼࡿࠥᐶ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l1l1l11l1l_opy_(self, r):
        if r is not None and getattr(r, bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࠪᐷ"), None) and getattr(r.testhub, bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᐸ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1ll1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᐹ")))
            for bstack1l1ll1llll1_opy_, err in errors.items():
                if err[bstack1ll1lll_opy_ (u"ࠬࡺࡹࡱࡧࠪᐺ")] == bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᐻ"):
                    self.logger.info(err[bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᐼ")])
                else:
                    self.logger.error(err[bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᐽ")])
    def bstack1111l1l111_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()