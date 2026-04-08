# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
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
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1ll11_opy_ import bstack1l1llll1lll_opy_
from browserstack_sdk.sdk_cli.bstack11lllllllll_opy_ import bstack1l11111llll_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1l11l_opy_ import bstack1l111ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll1l_opy_ import bstack1l1111l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l11111111l_opy_ import bstack1l1111l111l_opy_
from browserstack_sdk.sdk_cli.bstack1l111ll1l1l_opy_ import bstack1l11l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1lll1_opy_ import bstack1l1111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111lll1l_opy_ import bstack1l1ll111ll_opy_
from browserstack_sdk.sdk_cli.bstack111ll1111l_opy_ import bstack111ll1111l_opy_, Events, bstack1l11l111ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l111l11lll_opy_ import bstack1l1111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import bstack1l1l1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll_opy_ import bstack11ll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1l1ll1l1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l11l_opy_ import bstack1l1ll1111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1111l111l1_opy_ import bstack11111lll_opy_
from bstack_utils.helper import Notset, bstack1ll1l11lll1_opy_, get_cli_dir, bstack1ll1l111lll_opy_, bstack11llll11ll_opy_, bstack11111l1ll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l11ll11l_opy_, TestHookState, bstack11lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import bstack1l1l111l1l1_opy_, bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11ll1ll1l1_opy_ import bstack1l11llllll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1lll1ll11l_opy_, bstack1ll1ll1lll_opy_
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll1l_opy_ import bstack1l11l1l1ll1_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1l11l1ll1ll_opy_(bs_config):
    bstack1l11l1111l1_opy_ = None
    bstack1ll1l11l111_opy_ = None
    try:
        bstack1ll1l11l111_opy_ = get_cli_dir()
        bstack1l11l1111l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧᔉ"))
        if not bstack1l11l1111l1_opy_:
            bstack1l11l1111l1_opy_ = bstack1ll1l111lll_opy_(bstack1ll1l11l111_opy_)
            bstack1l11lll1111_opy_ = bstack1ll1l11lll1_opy_(bstack1l11l1111l1_opy_, bstack1ll1l11l111_opy_, bs_config)
            bstack1l11l1111l1_opy_ = bstack1l11lll1111_opy_ if bstack1l11lll1111_opy_ else bstack1l11l1111l1_opy_
        if not bstack1l11l1111l1_opy_:
            raise ValueError(bstack111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡈࡒࡉࠡࡲࡤࡸ࡭ࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡴࡸࠠࡪࡰࠣࡸ࡭࡫ࠠ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡧࡱ࡯ࡨࡪࡸࠢᔊ"))
    except Exception as ex:
        logger.error(bstack111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡪࡺࡴࡪࡰࡪࠤࡺࡶࠠࡄࡎࡌࠤࡵࡧࡴࡩ࠼ࠣࠦᔋ") + str(ex) + bstack111l_opy_ (u"ࠧࠨᔌ"))
    return bstack1l11l1111l1_opy_, bstack1ll1l11l111_opy_
bstack1l11ll111l1_opy_ = bstack111l_opy_ (u"ࠨ࠹࠺࠻࠼ࠦᔍ")
bstack1l111111l11_opy_ = bstack111l_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨᔎ")
bstack1l11l11llll_opy_ = bstack111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᔏ")
bstack1l111llll11_opy_ = bstack111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢᔐ")
BROWSERSTACK_AUTOMATION = bstack111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᔑ")
bstack1l111l1ll1l_opy_ = re.compile(bstack111l_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥᔒ"))
bstack1l111111ll1_opy_ = bstack111l_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥᔓ")
bstack1l11l1lllll_opy_ = bstack111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡏࡓࡅࡈࡣࡋࡇࡌࡍࡄࡄࡇࡐࠨᔔ")
bstack1l111l1ll11_opy_ = [
    Events.bstack11111l11l_opy_,
    Events.CONNECT,
    Events.bstack1l1ll1l111_opy_,
]
def _1l111l111l1_opy_():
    bstack111l_opy_ (u"ࠢࠣࠤࡉࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࠢ࡯࡭ࡧࡸࡡࡳࡻࠣࡀࠥ࠷࠹࠯࠶࠱࠴ࠥࡽࡨࡦࡴࡨࠤࡇࡸ࡯ࡸࡵࡨࡶ࠳࡫࡮ࡵࡴࡼ࠲࡬࡫ࡴࡠࡸࡨࡶࡸ࡯࡯࡯ࡵࠣࡨࡴ࡫ࡳ࡯ࠩࡷࠤࡪࡾࡩࡴࡶ࠱ࠦࠧࠨᔕ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l11111l1ll_opy_ = Path(Browser.__file__).parent / bstack111l_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡳࠤᔖ") / bstack111l_opy_ (u"ࠤࡳࡥࡨࡱࡡࡨࡧ࠱࡮ࡸࡵ࡮ࠣᔗ")
        bstack1l111lllll1_opy_ = json.loads(bstack1l11111l1ll_opy_.read_text())
        match = re.search(bstack111l_opy_ (u"ࡵࠦࡡࡪࠫ࡝࠰࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࠦᔘ"), bstack1l111lllll1_opy_[bstack111l_opy_ (u"ࠦࡩ࡫ࡰࡦࡰࡧࡩࡳࡩࡩࡦࡵࠥᔙ")][bstack111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᔚ")])
        bstack1l11111lll1_opy_ = match.group(0) if match else bstack111l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢᔛ")
    except Exception:
        bstack1l11111lll1_opy_ = bstack111l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣᔜ")
    return SimpleNamespace(version=bstack1l11111lll1_opy_)
class SDKCLI:
    _1ll1111111l_opy_ = None
    process: Union[None, Any]
    bstack11lllllll1l_opy_: bool
    bstack1l1111lll11_opy_: bool
    bstack1l111lll11l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l11111l1l1_opy_: Union[None, grpc.Channel]
    bstack1l11l1llll1_opy_: str
    test_framework: TestFramework
    bstack1ll1111111_opy_: bstack1l1l1ll11l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l1l1_opy_: bstack1l1ll111ll_opy_
    accessibility: bstack1l1llll1lll_opy_
    bstack1111l111l1_opy_: bstack11111lll_opy_
    ai: bstack1l11111llll_opy_
    bstack1l1111ll111_opy_: bstack1l111ll1lll_opy_
    bstack11lllllll11_opy_: List[bstack1l111111l1l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack11llllll1l1_opy_: Any
    bstack1l11l1111ll_opy_: Dict[str, timedelta]
    bstack1l111l1l111_opy_: str
    bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_
    def __new__(cls):
        if not cls._1ll1111111l_opy_:
            cls._1ll1111111l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1111111l_opy_
    def __init__(self):
        self.process = None
        self.bstack11lllllll1l_opy_ = False
        self.bstack1l11111l1l1_opy_ = None
        self.bstack11l11lll11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l111llll11_opy_, None)
        self.bstack1l11111l11l_opy_ = os.environ.get(bstack1l11l11llll_opy_, bstack111l_opy_ (u"ࠣࠤᔝ")) == bstack111l_opy_ (u"ࠤࠥᔞ")
        self.bstack1l1111lll11_opy_ = False
        self.bstack1l111lll11l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack11llllll1l1_opy_ = None
        self.test_framework = None
        self.bstack1ll1111111_opy_ = None
        self.bstack1l11l1llll1_opy_=bstack111l_opy_ (u"ࠥࠦᔟ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l11l1111ll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1l1l1ll11l1_opy_ = bstack1l1l11ll111_opy_()
        self.bstack1l11ll11lll_opy_ = False
        self.bstack1l111l1l1ll_opy_ = None
        self.bstack1l11ll1ll1l_opy_ = None
        self.bstack1ll1l1l1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack11lllllll11_opy_ = []
    def bstack11l1111l1l_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᔠ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l11l1lllll_opy_, bstack111l_opy_ (u"ࠬ࠭ᔡ")).lower() in [bstack111l_opy_ (u"࠭ࡴࡳࡷࡨࠫᔢ"), bstack111l_opy_ (u"ࠧ࠲ࠩᔣ"), bstack111l_opy_ (u"ࠨࡻࡨࡷࠬᔤ")]:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡉࡳࡷࡩࡩ࡯ࡩࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡳ࡯ࡥࡧࠣࡨࡺ࡫ࠠࡵࡱࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡓࡗࡉࡅࡠࡈࡄࡐࡑࡈࡁࡄࡍࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠥᔥ"))
            os.environ[bstack111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨᔦ")] = bstack111l_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᔧ")
            return False
        if bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᔨ") in config and str(config[bstack111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᔩ")]).lower() != bstack111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᔪ"):
            return False
        bstack1l11l1l1lll_opy_ = [bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᔫ"), bstack111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᔬ"), bstack111l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦᔭ")]
        if is_robot_playwright_installed():
            bstack1l11l1l1lll_opy_.append(bstack111l_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥᔮ"))
            bstack1l11l1l1lll_opy_.append(bstack111l_opy_ (u"ࠧࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠨᔯ"))
        bstack1l11l1ll111_opy_ = config.get(bstack111l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤᔰ")) in bstack1l11l1l1lll_opy_ or os.environ.get(bstack111l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨᔱ")) in bstack1l11l1l1lll_opy_
        os.environ[bstack111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦᔲ")] = str(bstack1l11l1ll111_opy_) # bstack1l11lll11l1_opy_ bstack1l111ll11l1_opy_ VAR to bstack1l111ll11ll_opy_ is binary running
        return bstack1l11l1ll111_opy_
    def bstack1l1l11lll1_opy_(self):
        for event in bstack1l111l1ll11_opy_:
            bstack111ll1111l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack111ll1111l_opy_.logger.debug(bstack111l_opy_ (u"ࠤࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠡ࠿ࡁࠤࢀࡧࡲࡨࡵࢀࠤࠧᔳ") + str(kwargs) + bstack111l_opy_ (u"ࠥࠦᔴ"))
            )
        bstack111ll1111l_opy_.register(Events.bstack11111l11l_opy_, self.__1l11l11lll1_opy_)
        bstack111ll1111l_opy_.register(Events.CONNECT, self.__1l1111111ll_opy_)
        bstack111ll1111l_opy_.register(Events.bstack1l1ll1l111_opy_, self.__1l11l1l111l_opy_)
        bstack111ll1111l_opy_.register(Events.bstack11ll1l11l1_opy_, self.__1l111lll111_opy_)
    def bstack1llll1ll11_opy_(self):
        return not self.bstack1l11111l11l_opy_ and os.environ.get(bstack1l11l11llll_opy_, bstack111l_opy_ (u"ࠦࠧᔵ")) != bstack111l_opy_ (u"ࠧࠨᔶ")
    def is_running(self):
        if self.bstack1l11111l11l_opy_:
            return self.bstack11lllllll1l_opy_
        else:
            return bool(self.bstack1l11111l1l1_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᔷ"))
                and self.config_observability.options.allow_screenshots == bstack111l_opy_ (u"ࠧࡵࡴࡸࡩࠬᔸ")
            )
        except Exception:
            return False
    def bstack1ll1lll11_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack11lllllll11_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l111ll1ll1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l111llll1l_opy_(self, bstack1l11l1l1111_opy_=10):
        if self.bstack11l11lll11_opy_:
            return
        bstack1lllllll1ll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l111llll11_opy_, self.cli_listen_addr)
        self.logger.debug(bstack111l_opy_ (u"ࠣ࡝ࠥᔹ") + str(id(self)) + bstack111l_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣᔺ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧᔻ"), 0), (bstack111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢᔼ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l11l1l1111_opy_)
        self.bstack1l11111l1l1_opy_ = channel
        self.bstack11l11lll11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l11111l1l1_opy_)
        self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦᔽ"), datetime.now() - bstack1lllllll1ll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l111llll11_opy_] = self.cli_listen_addr
        self.logger.debug(bstack111l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨᔾ") + str(self.bstack1llll1ll11_opy_()) + bstack111l_opy_ (u"ࠢࠣᔿ"))
    def __1l11l1l111l_opy_(self, event_name):
        if self.bstack1llll1ll11_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣᕀ"))
        self.__1l1111llll1_opy_()
    @measure(event_name=EVENTS.bstack1l111l11111_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l111lll111_opy_(self, event_name, bstack1l11l11l1ll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack111l_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤᕁ"))
        bstack1l11ll11l1l_opy_ = Path(bstack1l11lll11ll_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦᕂ"))
        if self.bstack1ll1l11l111_opy_ and bstack1l11ll11l1l_opy_.exists():
            with open(bstack1l11ll11l1l_opy_, bstack111l_opy_ (u"ࠫࡷ࠭ᕃ"), encoding=bstack111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᕄ")) as fp:
                data = json.load(fp)
                try:
                    bstack11111l1ll_opy_(bstack111l_opy_ (u"࠭ࡐࡐࡕࡗࠫᕅ"), bstack1l11llllll_opy_(bstack111lll111_opy_), data, {
                        bstack111l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᕆ"): (self.config[bstack111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᕇ")], self.config[bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᕈ")])
                    })
                except Exception as e:
                    logger.debug(bstack1ll1ll1lll_opy_.format(str(e)))
            bstack1l11ll11l1l_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l111llllll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l11l11lll1_opy_(self, event_name: str, data):
        from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
        self.bstack1l11l1llll1_opy_, self.bstack1ll1l11l111_opy_ = bstack1l11l1ll1ll_opy_(data.bs_config)
        os.environ[bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨᕉ")] = self.bstack1ll1l11l111_opy_
        if not self.bstack1l11l1llll1_opy_ or not self.bstack1ll1l11l111_opy_:
            raise ValueError(bstack111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥᕊ"))
        if self.bstack1llll1ll11_opy_():
            self.__1l1111111ll_opy_(event_name, bstack1l11l111ll_opy_())
            return
        try:
            logger.debug(bstack111l_opy_ (u"ࠧࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡔࡆࡎࠤࡘ࡫ࡴࡶࡲ࠱ࠦᕋ"))
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥᕌ").format(e))
        start = datetime.now()
        is_started = self.__1l11l1l11ll_opy_()
        self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠢࡴࡲࡤࡻࡳࡥࡴࡪ࡯ࡨࠦᕍ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l111llll1l_opy_()
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢᕎ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1111l11ll_opy_(data)
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢᕏ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1111lll1l_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l1111111ll_opy_(self, event_name: str, data: bstack1l11l111ll_opy_):
        if not self.bstack1llll1ll11_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࡰࡲࡸࠥࡧࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᕐ"))
            return
        bin_session_id = os.environ.get(bstack1l11l11llll_opy_)
        start = datetime.now()
        self.__1l111llll1l_opy_()
        self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥᕑ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack111l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡃࡍࡋࠣࠦᕒ") + str(bin_session_id) + bstack111l_opy_ (u"ࠨࠢᕓ"))
        start = datetime.now()
        self.__1l11111l111_opy_()
        self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᕔ"), datetime.now() - start)
    def __1l11l111l1l_opy_(self):
        if not self.bstack11l11lll11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡥࡤࡲࡳࡵࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡲࡵࡤࡶ࡮ࡨࡷࠧᕕ"))
            return
        bstack1l111l1111l_opy_ = {
            bstack111l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᕖ"): (bstack1l11l111lll_opy_, bstack1l1111ll1l1_opy_, bstack11ll1lllll_opy_),
            bstack111l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᕗ"): (bstack1l1111l1ll1_opy_, bstack1l1111l111l_opy_, bstack1l11l11l11l_opy_),
        }
        if not self.bstack1l111l1l1ll_opy_ and self.session_framework in bstack1l111l1111l_opy_:
            bstack1l11ll1111l_opy_, bstack1l1111l1111_opy_, bstack1l11ll1l1l1_opy_ = bstack1l111l1111l_opy_[self.session_framework]
            bstack1l11lll111l_opy_ = bstack1l1111l1111_opy_()
            self.bstack1l11ll1ll1l_opy_ = bstack1l11lll111l_opy_
            self.bstack1l111l1l1ll_opy_ = bstack1l11ll1l1l1_opy_
            self.bstack11lllllll11_opy_.append(bstack1l11lll111l_opy_)
            self.bstack11lllllll11_opy_.append(bstack1l11ll1111l_opy_(self.bstack1l11ll1ll1l_opy_))
        if not self.bstack1ll1l1l1_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1ll1l1l1_opy_ = bstack1l1ll111ll_opy_(self.bstack1l111l1l1ll_opy_, self.bstack1l11ll1ll1l_opy_)
            self.bstack11lllllll11_opy_.append(self.bstack1ll1l1l1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l1llll1lll_opy_(self.bstack1l111l1l1ll_opy_, self.bstack1l11ll1ll1l_opy_)
            self.bstack11lllllll11_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack111l_opy_ (u"ࠦࡸ࡫࡬ࡧࡊࡨࡥࡱࠨᕘ"), False) == True:
            self.ai = bstack1l11111llll_opy_()
            self.bstack11lllllll11_opy_.append(self.ai)
        if not self.percy and self.bstack11llllll1l1_opy_ and self.bstack11llllll1l1_opy_.success:
            self.percy = bstack1l111ll1lll_opy_(self.bstack11llllll1l1_opy_)
            self.bstack11lllllll11_opy_.append(self.percy)
        for mod in self.bstack11lllllll11_opy_:
            if not mod.bstack1l11l1lll1l_opy_():
                mod.configure(self.bstack11l11lll11_opy_, self.config, self.cli_bin_session_id, self.bstack1l1l1ll11l1_opy_)
    def __1l111ll111l_opy_(self):
        for mod in self.bstack11lllllll11_opy_:
            if mod.bstack1l11l1lll1l_opy_():
                mod.configure(self.bstack11l11lll11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l111l1l1l1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l1111l11ll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l1111lll11_opy_:
            return
        self.__1l111l11l11_opy_(data)
        bstack1lllllll1ll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack111l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧᕙ")
        req.sdk_language = bstack111l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᕚ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l111l1ll1l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᕛ"), bstack111l_opy_ (u"ࠨ࠲ࠪᕜ")))
            req.client_worker_id = bstack111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕝ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡽ࡯ࡳ࡭ࡨࡶࠥࡧ࡮ࡥࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤ࡮ࡴࡤࡦࡺ࠽ࠤࢀࢃࠢᕞ").format(e))
        try:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡠࠨᕟ") + str(id(self)) + bstack111l_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᕠ"))
            r = self.bstack11l11lll11_opy_.StartBinSession(req)
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᕡ"), datetime.now() - bstack1lllllll1ll_opy_)
            os.environ[bstack1l11l11llll_opy_] = r.bin_session_id
            self.__1l111lll1ll_opy_(r)
            self.__1l11l111l1l_opy_()
            if not self.bstack1l11ll11lll_opy_:
                self.bstack1l1l1ll11l1_opy_.start()
                self.bstack1l11ll11lll_opy_ = True
                atexit.register(self.__1l11l1l11l1_opy_)
            self.bstack1l1111lll11_opy_ = True
            self.logger.debug(bstack111l_opy_ (u"ࠢ࡜ࠤᕢ") + str(id(self)) + bstack111l_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨᕣ"))
        except grpc.bstack1l11l1ll1l1_opy_ as bstack1l111l1lll1_opy_:
            self.logger.error(bstack111l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᕤ") + str(bstack1l111l1lll1_opy_) + bstack111l_opy_ (u"ࠥࠦᕥ"))
            traceback.print_exc()
            raise bstack1l111l1lll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕦ") + str(e) + bstack111l_opy_ (u"ࠧࠨᕧ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111111l1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l11111l111_opy_(self):
        if not self.bstack1llll1ll11_opy_() or not self.cli_bin_session_id or self.bstack1l111lll11l_opy_:
            return
        bstack1lllllll1ll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᕨ"), bstack111l_opy_ (u"ࠧ࠱ࠩᕩ")))
        req.client_worker_id = bstack111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᕪ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack111l_opy_ (u"ࠤ࡞ࠦᕫ") + str(id(self)) + bstack111l_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᕬ"))
            r = self.bstack11l11lll11_opy_.ConnectBinSession(req)
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᕭ"), datetime.now() - bstack1lllllll1ll_opy_)
            self.__1l111lll1ll_opy_(r)
            self.__1l11l111l1l_opy_()
            if not self.bstack1l11ll11lll_opy_:
                self.bstack1l1l1ll11l1_opy_.start()
                self.bstack1l11ll11lll_opy_ = True
                atexit.register(self.__1l11l1l11l1_opy_)
            self.bstack1l111lll11l_opy_ = True
            self.logger.debug(bstack111l_opy_ (u"ࠧࡡࠢᕮ") + str(id(self)) + bstack111l_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧᕯ"))
        except grpc.bstack1l11l1ll1l1_opy_ as bstack1l111l1lll1_opy_:
            self.logger.error(bstack111l_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᕰ") + str(bstack1l111l1lll1_opy_) + bstack111l_opy_ (u"ࠣࠤᕱ"))
            traceback.print_exc()
            raise bstack1l111l1lll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᕲ") + str(e) + bstack111l_opy_ (u"ࠥࠦᕳ"))
            traceback.print_exc()
            raise e
    def __1l111lll1ll_opy_(self, r):
        self.bstack1l11l11111l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack111l_opy_ (u"ࠦࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡵࡨࡶࡻ࡫ࡲࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᕴ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack111l_opy_ (u"ࠧ࡫࡭ࡱࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡵ࡯ࡦࠥᕵ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡪࡸࡣࡺࠢ࡬ࡷࠥࡹࡥ࡯ࡶࠣࡳࡳࡲࡹࠡࡣࡶࠤࡵࡧࡲࡵࠢࡲࡪࠥࡺࡨࡦࠢࠥࡇࡴࡴ࡮ࡦࡥࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠬࠣࠢࡤࡲࡩࠦࡴࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡩࡴࠢࡤࡰࡸࡵࠠࡶࡵࡨࡨࠥࡨࡹࠡࡕࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡦࡴࡨࡪࡴࡸࡥ࠭ࠢࡑࡳࡳ࡫ࠠࡩࡣࡱࡨࡱ࡯࡮ࡨࠢ࡬ࡷࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᕶ")
        self.bstack11llllll1l1_opy_ = getattr(r, bstack111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᕷ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᕸ")] = self.config_testhub.jwt
        os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᕹ")] = self.config_testhub.build_hashed_id
        if self.config.get(bstack111l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨᕺ")) == bstack111l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠧᕻ"):
            if self.config_accessibility and self.config_accessibility.success:
                try:
                    options = self.config_accessibility.options
                    if options:
                        bstack1l11l1ll11l_opy_ = json.loads(os.getenv(bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᕼ"), bstack111l_opy_ (u"࠭ࡻࡾࠩᕽ")))
                        if options.capabilities:
                            for bstack1ll1lllll1_opy_ in options.capabilities:
                                if bstack1ll1lllll1_opy_.name == bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᕾ"):
                                    os.environ[bstack111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕿ")] = bstack1ll1lllll1_opy_.value
                                    self.logger.debug(bstack111l_opy_ (u"ࠤࡖࡩࡹࠦࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠤ࡫ࡸ࡯࡮ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡦࡳࡳ࡬ࡩࡨࠤᖀ"))
                                elif bstack1ll1lllll1_opy_.name == bstack111l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᖁ"):
                                    bstack1l11l1ll11l_opy_[bstack111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᖂ")] = bstack1ll1lllll1_opy_.value
                                    self.logger.debug(bstack111l_opy_ (u"࡙ࠧࡥࡵࠢࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢᖃ").format(bstack1ll1lllll1_opy_.value))
                        os.environ[bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᖄ")] = json.dumps(bstack1l11l1ll11l_opy_)
                        if options.scripts:
                            scripts = {script.name: script.command for script in options.scripts}
                            accessibility_scripts.bstack1l11l1l1_opy_(scripts)
                            self.logger.debug(bstack111l_opy_ (u"ࠢࡖࡲࡧࡥࡹ࡫ࡤࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡶ࡮ࡶࡴࡴ࠼ࠣࡿࢂࠨᖅ").format(list(scripts.keys())))
                        if options.commands_to_wrap and options.commands_to_wrap.commands:
                            commands = [{bstack111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᖆ"): cmd.name} for cmd in options.commands_to_wrap.commands]
                            accessibility_scripts.bstack1l11l11l1l1_opy_(commands)
                            self.logger.debug(bstack111l_opy_ (u"ࠤࡘࡴࡩࡧࡴࡦࡦࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡧࡴࡳ࡭ࡢࡰࡧࡷ࠿ࠦࡻࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡶࠦᖇ").format(len(commands)))
                        accessibility_scripts.store()
                except Exception as e:
                    self.logger.debug(bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡧࡴࡴࡦࡪࡩ࠽ࠤࢀࢃࠢᖈ").format(e))
        if is_robot_playwright_installed():
            bstack1l11ll11111_opy_ = json.loads(r.config)
            bstack1l11ll11l11_opy_ = bstack1l11ll11111_opy_.get(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᖉ"), {}).get(bstack111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᖊ"), bstack111l_opy_ (u"࠭ࠧᖋ"))
            os.environ[bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᖌ")] = bstack1l11ll11l11_opy_
    def bstack1l111ll1l11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack11lllllll1l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l111l11ll1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l111l11ll1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l111ll1l11_opy_(event_name=EVENTS.bstack1l11ll1ll11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l11l1l11ll_opy_(self, bstack1l11l1l1111_opy_=10):
        if self.bstack11lllllll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠥᖍ"))
            return True
        self.logger.debug(bstack111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᖎ"))
        if os.getenv(bstack111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡅࡏࡘࠥᖏ")) == bstack1l111111ll1_opy_:
            self.cli_bin_session_id = bstack1l111111ll1_opy_
            self.cli_listen_addr = bstack111l_opy_ (u"ࠦࡺࡴࡩࡹ࠼࠲ࡸࡲࡶ࠯ࡴࡦ࡮࠱ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࠥࡴ࠰ࡶࡳࡨࡱࠢᖐ") % (self.cli_bin_session_id)
            self.bstack11lllllll1l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l11l1llll1_opy_, bstack111l_opy_ (u"ࠧࡹࡤ࡬ࠤᖑ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l111111111_opy_ compat for text=True in bstack1l11ll11ll1_opy_ python
            encoding=bstack111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᖒ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l11l1l1l1l_opy_ = threading.Thread(target=self.__1l11ll111ll_opy_, args=(bstack1l11l1l1111_opy_,))
        bstack1l11l1l1l1l_opy_.start()
        bstack1l11l1l1l1l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack111l_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡳࡱࡣࡺࡲ࠿ࠦࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫ࡽࠡࡱࡸࡸࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡹࡴࡥࡱࡸࡸ࠳ࡸࡥࡢࡦࠫ࠭ࢂࠦࡥࡳࡴࡀࠦᖓ") + str(self.process.stderr.read()) + bstack111l_opy_ (u"ࠣࠤᖔ"))
        if not self.bstack11lllllll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠤ࡞ࠦᖕ") + str(id(self)) + bstack111l_opy_ (u"ࠥࡡࠥࡩ࡬ࡦࡣࡱࡹࡵࠨᖖ"))
            self.__1l1111llll1_opy_()
        self.logger.debug(bstack111l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡴࡷࡵࡣࡦࡵࡶࡣࡷ࡫ࡡࡥࡻ࠽ࠤࠧᖗ") + str(self.bstack11lllllll1l_opy_) + bstack111l_opy_ (u"ࠧࠨᖘ"))
        return self.bstack11lllllll1l_opy_
    def __1l11ll111ll_opy_(self, bstack1l111l111ll_opy_=10):
        bstack1l111l1llll_opy_ = time.time()
        while self.process and time.time() - bstack1l111l1llll_opy_ < bstack1l111l111ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack111l_opy_ (u"ࠨࡩࡥ࠿ࠥᖙ") in line:
                    self.cli_bin_session_id = line.split(bstack111l_opy_ (u"ࠢࡪࡦࡀࠦᖚ"))[-1:][0].strip()
                    self.logger.debug(bstack111l_opy_ (u"ࠣࡥ࡯࡭ࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠢᖛ") + str(self.cli_bin_session_id) + bstack111l_opy_ (u"ࠤࠥᖜ"))
                    continue
                if bstack111l_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦᖝ") in line:
                    self.cli_listen_addr = line.split(bstack111l_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧᖞ"))[-1:][0].strip()
                    self.logger.debug(bstack111l_opy_ (u"ࠧࡩ࡬ࡪࡡ࡯࡭ࡸࡺࡥ࡯ࡡࡤࡨࡩࡸ࠺ࠣᖟ") + str(self.cli_listen_addr) + bstack111l_opy_ (u"ࠨࠢᖠ"))
                    continue
                if bstack111l_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨᖡ") in line:
                    port = line.split(bstack111l_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢᖢ"))[-1:][0].strip()
                    self.logger.debug(bstack111l_opy_ (u"ࠤࡳࡳࡷࡺ࠺ࠣᖣ") + str(port) + bstack111l_opy_ (u"ࠥࠦᖤ"))
                    continue
                if line.strip() == bstack1l111111l11_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack111l_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡍࡔࡥࡓࡕࡔࡈࡅࡒࠨᖥ"), bstack111l_opy_ (u"ࠧ࠷ࠢᖦ")) == bstack111l_opy_ (u"ࠨ࠱ࠣᖧ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack11lllllll1l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࡀࠠࠣᖨ") + str(e) + bstack111l_opy_ (u"ࠣࠤᖩ"))
        return False
    def __1l11l1l11l1_opy_(self):
        bstack111l_opy_ (u"ࠤࠥࠦࡈࡲࡥࡢࡰࡸࡴࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡦࡰࡴࠣࡥࡸࡿ࡮ࡤࡡࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷ࠲ࠠࡤࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡥࡹ࡫ࡸࡪࡶࠣࡸࡴࠦࡥ࡯ࡵࡸࡶࡪࠦࡴࡢࡵ࡮ࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣࠤࠥᖪ")
        if self.bstack1l1l1ll11l1_opy_ and self.bstack1l11ll11lll_opy_:
            try:
                self.bstack1l1l1ll11l1_opy_.stop()
                self.bstack1l11ll11lll_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1111ll1ll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def __1l1111llll1_opy_(self):
        if self.bstack1l11111l1l1_opy_:
            if self.bstack1l1l1ll11l1_opy_ and self.bstack1l11ll11lll_opy_:
                try:
                    atexit.unregister(self.__1l11l1l11l1_opy_)
                except ValueError:
                    pass
                self.bstack1l1l1ll11l1_opy_.stop()
                self.bstack1l11ll11lll_opy_ = False
            start = datetime.now()
            if self.bstack1l11ll1l1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l111lll11l_opy_:
                    self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢᖫ"), datetime.now() - start)
                else:
                    self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᖬ"), datetime.now() - start)
            self.__1l111ll111l_opy_()
            start = datetime.now()
            bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(bstack111l_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࠥᖭ"))
            self.bstack1l11111l1l1_opy_.close()
            bstack11lll11111_opy_.end(bstack111l_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࠦᖮ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᖯ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᖰ"), True, None, None, None, None)
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᖱ"), datetime.now() - start)
            self.bstack1l11111l1l1_opy_ = None
        if self.process:
            self.logger.debug(bstack111l_opy_ (u"ࠥࡷࡹࡵࡰࠣᖲ"))
            start = datetime.now()
            bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(bstack111l_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡱࡩ࡭࡮ࠥᖳ"))
            self.process.terminate()
            bstack11lll11111_opy_.end(bstack111l_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡫ࡪ࡮࡯ࠦᖴ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᖵ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᖶ"), True, None, None, None, None)
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠣ࡭࡬ࡰࡱࡥࡴࡪ࡯ࡨࠦᖷ"), datetime.now() - start)
            self.process = None
            if self.bstack1l11111l11l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1lllll1lll_opy_()
                self.logger.info(
                    bstack111l_opy_ (u"ࠤ࡙࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤᖸ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᖹ")] = self.config_testhub.build_hashed_id
        self.bstack11lllllll1l_opy_ = False
    def __1l111l11l11_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᖺ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1111l1l1l_opy_ = get_pw_version()
            except:
                bstack1l1111l1l1l_opy_ = _1l111l111l1_opy_()
            data.framework_versions[bstack111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᖻ")] = bstack1l1111l1l1l_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack111l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᖼ")] = selenium.__version__
                data.frameworks.append(bstack111l_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᖽ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack111l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᖾ")] = __version__
                data.frameworks.append(bstack111l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᖿ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack111l_opy_ (u"ࠥࡒࡴࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡩ࡫ࡴࡦࡥࡷࡩࡩࠨᗀ"))
    def bstack1l11ll1l111_opy_(self, hub_url: str, platform_index: int, bstack11l111ll1_opy_: Any):
        if self.bstack1ll1111111_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᗁ"))
            return
        try:
            bstack1lllllll1ll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack111l_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᗂ")
            self.bstack1ll1111111_opy_ = bstack1l11l11l11l_opy_(
                cli.config.get(bstack111l_opy_ (u"ࠨࡨࡶࡤࡘࡶࡱࠨᗃ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l11l111l11_opy_={bstack111l_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᗄ"): bstack11l111ll1_opy_}
            )
            def bstack1l111ll1111_opy_(self):
                return
            if self.config.get(bstack111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥᗅ"), True):
                Service.start = bstack1l111ll1111_opy_
                Service.stop = bstack1l111ll1111_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11111lll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1ll1111ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᗆ"), datetime.now() - bstack1lllllll1ll_opy_)
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤᗇ") + str(e) + bstack111l_opy_ (u"ࠦࠧᗈ"))
    def bstack1l1lll111_opy_(self, platform_index: int):
        if self.bstack1ll1111111_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᗉ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l111lll1l1_opy_
                self.bstack1ll1111111_opy_ = bstack11ll1lllll_opy_(
                    platform_index,
                    framework_name=bstack111l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᗊ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l111l111l1_opy_
                from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1l1ll1l1l_opy_
                bstack1l1111l1l1l_opy_ = get_pw_version()
                self.bstack1ll1111111_opy_ = bstack11ll1lllll_opy_(
                    platform_index,
                    framework_name=bstack111l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᗋ"),
                    framework_version=bstack1l1111l1l1l_opy_.version,
                    classes=[],
                )
                ctx = bstack1l1l1ll1l1l_opy_.create_context(self.bstack1ll1111111_opy_)
                bstack1l1l1ll11l_opy_.bstack1l111l111_opy_[ctx.id] = bstack1l1l111l1l1_opy_(
                    ctx, bstack111l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᗌ"), bstack1l1111l1l1l_opy_, bstack11l1ll1l1_opy_.bstack11llll111l_opy_
                )
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠻ࠢࠥᗍ") + str(e) + bstack111l_opy_ (u"ࠥࠦᗎ"))
            pass
    def bstack111llll1l_opy_(self, framework_name: str = None):
        if self.test_framework:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢᗏ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1l11l1l1ll1_opy_({ bstack111l_opy_ (u"ࠧࡸ࡯ࡣࡱࡷ࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢᗐ"): VERSION }, [bstack111l_opy_ (u"ࠨࡲࡰࡤࡲࡸࠧᗑ")], self.bstack1l1l1ll11l1_opy_, self.bstack11l11lll11_opy_)
                return
            except Exception as e:
                self.logger.error(bstack111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡵࡳࡧࡵࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠾ࠥࠨᗒ") + str(e) + bstack111l_opy_ (u"ࠣࠤᗓ"))
        bstack1l1111l1l11_opy_ = framework_name
        if bstack1l1111l1l11_opy_ == bstack111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᗔ"):
            import sys
            python_version = bstack111l_opy_ (u"ࠥࡿࢂ࠴ࡻࡾ࠰ࡾࢁࠧᗕ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            self.test_framework = bstack1l1ll1l1111_opy_(
                bstack1l1lll1l111_opy_={bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬᗖ"): python_version},
                bstack1l1ll1ll11l_opy_=[bstack111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᗗ")],
                bstack1l1l1ll11l1_opy_=self.bstack1l1l1ll11l1_opy_,
                bstack11l11lll11_opy_=self.bstack11l11lll11_opy_
            )
            self.logger.info(bstack111l_opy_ (u"ࠨࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧࠤ࡛ࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡦࡰࡴࠣࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠤࡹ࡫ࡳࡵࡵࠥᗘ"))
            return
        if bstack11llll11ll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᗙ"): pytest.__version__ }, [bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᗚ")], self.bstack1l1l1ll11l1_opy_, self.bstack11l11lll11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1111l1lll_opy_({ bstack111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᗛ"): pytest.__version__ }, [bstack111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᗜ")], self.bstack1l1l1ll11l1_opy_, self.bstack11l11lll11_opy_)
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࠣᗝ") + str(e) + bstack111l_opy_ (u"ࠧࠨᗞ"))
        self.bstack1l11ll1llll_opy_()
    def bstack1l11ll1llll_opy_(self):
        if not self.bstack11l1111l1l_opy_():
            return
        bstack1l1111l1l_opy_ = None
        def bstack1l1l11l1l_opy_(config, startdir):
            return bstack111l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦᗟ").format(bstack111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᗠ"))
        def bstack11ll11ll_opy_():
            return
        def bstack1l11lll1ll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack111l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᗡ"):
                return bstack111l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᗢ")
            else:
                return bstack1l1111l1l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1111l1l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l1l11l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll11ll_opy_
            Config.getoption = bstack1l11lll1ll_opy_
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬ࠥࡶࡹࡵࡧࡶࡸࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠽ࠤࠧᗣ") + str(e) + bstack111l_opy_ (u"ࠦࠧᗤ"))
    def bstack1l11l11l111_opy_(self):
        bstack11l1l1l1l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11l1l1l1l1_opy_, dict):
            if cli.config_observability:
                bstack11l1l1l1l1_opy_.update(
                    {bstack111l_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᗥ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᗦ") in accessibility.get(bstack111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᗧ"), {}):
                    bstack1l11l111ll1_opy_ = accessibility.get(bstack111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᗨ"))
                    bstack1l11l111ll1_opy_.update({ bstack111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠥᗩ"): bstack1l11l111ll1_opy_.pop(bstack111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨᗪ")) })
                bstack11l1l1l1l1_opy_.update({bstack111l_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᗫ"): accessibility })
        return bstack11l1l1l1l1_opy_
    @measure(event_name=EVENTS.bstack1l11l111111_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack1l11ll1l1ll_opy_(self, bstack1l111l1l11l_opy_: str = None, bstack1l111111lll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack11l11lll11_opy_:
            return
        bstack1lllllll1ll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᗬ"), bstack111l_opy_ (u"࠭࠰ࠨᗭ")))
        req.client_worker_id = bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᗮ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l111l1l11l_opy_:
            req.bstack1l111l1l11l_opy_ = bstack1l111l1l11l_opy_
        if bstack1l111111lll_opy_:
            req.bstack1l111111lll_opy_ = bstack1l111111lll_opy_
        try:
            r = self.bstack11l11lll11_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᗯ"), datetime.now() - bstack1lllllll1ll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1lllll1111_opy_(self, key: str, value: timedelta):
        tag = bstack111l_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᗰ") if self.bstack1llll1ll11_opy_() else bstack111l_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᗱ")
        self.bstack1l11l1111ll_opy_[bstack111l_opy_ (u"ࠦ࠿ࠨᗲ").join([tag + bstack111l_opy_ (u"ࠧ࠳ࠢᗳ") + str(id(self)), key])] += value
    def bstack1lllll1lll_opy_(self):
        if not os.getenv(bstack111l_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥᗴ"), bstack111l_opy_ (u"ࠢ࠱ࠤᗵ")) == bstack111l_opy_ (u"ࠣ࠳ࠥᗶ"):
            return
        bstack1l1111l11l1_opy_ = dict()
        bstack1l111l111_opy_ = []
        if self.test_framework:
            bstack1l111l111_opy_.extend(list(self.test_framework.bstack1l111l111_opy_.values()))
        if self.bstack1ll1111111_opy_:
            bstack1l111l111_opy_.extend(list(self.bstack1ll1111111_opy_.bstack1l111l111_opy_.values()))
        for instance in bstack1l111l111_opy_:
            if not instance.platform_index in bstack1l1111l11l1_opy_:
                bstack1l1111l11l1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l1111l11l1_opy_[instance.platform_index]
            for k, v in instance.bstack1l111l11l1l_opy_().items():
                report[k] += v
                report[k.split(bstack111l_opy_ (u"ࠤ࠽ࠦᗷ"))[0]] += v
        bstack11llllllll1_opy_ = sorted([(k, v) for k, v in self.bstack1l11l1111ll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l11l1lll11_opy_ = 0
        for r in bstack11llllllll1_opy_:
            bstack1l11l11ll11_opy_ = r[1].total_seconds()
            bstack1l11l1lll11_opy_ += bstack1l11l11ll11_opy_
            self.logger.debug(bstack111l_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣᗸ") + str(bstack1l11l11ll11_opy_) + bstack111l_opy_ (u"ࠦࠧᗹ"))
        self.logger.debug(bstack111l_opy_ (u"ࠧ࠳࠭ࠣᗺ"))
        bstack11llllll1ll_opy_ = []
        for platform_index, report in bstack1l1111l11l1_opy_.items():
            bstack11llllll1ll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack11llllll1ll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1ll11ll1_opy_ = set()
        bstack1l1111ll11l_opy_ = 0
        for r in bstack11llllll1ll_opy_:
            bstack1l11l11ll11_opy_ = r[2].total_seconds()
            bstack1l1111ll11l_opy_ += bstack1l11l11ll11_opy_
            bstack1ll11ll1_opy_.add(r[0])
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢᗻ") + str(bstack1l11l11ll11_opy_) + bstack111l_opy_ (u"ࠢࠣᗼ"))
        if self.bstack1llll1ll11_opy_():
            self.logger.debug(bstack111l_opy_ (u"ࠣ࠯࠰ࠦᗽ"))
            self.logger.debug(bstack111l_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤᗾ") + str(bstack1l1111ll11l_opy_) + bstack111l_opy_ (u"ࠥࠦᗿ"))
        else:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᘀ") + str(bstack1l11l1lll11_opy_) + bstack111l_opy_ (u"ࠧࠨᘁ"))
        self.logger.debug(bstack111l_opy_ (u"ࠨ࠭࠮ࠤᘂ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᘃ"), bstack111l_opy_ (u"ࠨ࠲ࠪᘄ"))),
            client_worker_id=bstack111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᘅ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack11l11lll11_opy_:
            self.logger.error(bstack111l_opy_ (u"ࠥࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡄࡣࡱࡲࡴࡺࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᘆ"))
            return None
        response = self.bstack11l11lll11_opy_.TestOrchestration(request)
        self.logger.debug(bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵ࠯ࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠯ࡶࡩࡸࡹࡩࡰࡰࡀࡿࢂࠨᘇ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l11l11111l_opy_(self, r):
        if r is not None and getattr(r, bstack111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭ᘈ"), None) and getattr(r.testhub, bstack111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᘉ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᘊ")))
            for bstack1l11111ll11_opy_, err in errors.items():
                if err[bstack111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘋ")] == bstack111l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᘌ"):
                    self.logger.info(err[bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘍ")])
                else:
                    self.logger.error(err[bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘎ")])
    def bstack1l1l11ll1_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()