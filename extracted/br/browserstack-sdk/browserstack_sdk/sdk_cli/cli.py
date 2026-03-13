# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
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
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1ll1ll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1ll1l_opy_ import bstack1ll11l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1l1llll111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1l1ll1lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11lll_opy_ import bstack1l1lll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1ll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll11l_opy_ import bstack1l1lllll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll11l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11_opy_ import bstack11l1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1111ll11_opy_ import bstack1111ll11_opy_, Events, bstack1lllll111l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1ll1l1ll1_opy_ import bstack1l1ll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll11l11111_opy_ import bstack1ll111lll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1l11_opy_ import bstack111l11l1_opy_
from bstack_utils.helper import Notset, bstack1llll1l111l_opy_, get_cli_dir, bstack1llll1l11ll_opy_, bstack111ll11ll1_opy_, bstack1llll1ll1_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111lllll_opy_, TestHookState, bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1l1lll1l_opy_, bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1lll111l_opy_ import bstack11lll1ll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l11ll11_opy_, bstack11ll11l1_opy_
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1llll_opy_ import bstack1l1llllll11_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1l1l1lllll1_opy_(bs_config):
    bstack1l1llll1lll_opy_ = None
    bstack1llll1l1111_opy_ = None
    try:
        bstack1llll1l1111_opy_ = get_cli_dir()
        bstack1l1llll1lll_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦጉ"))
        if not bstack1l1llll1lll_opy_:
            bstack1l1llll1lll_opy_ = bstack1llll1l11ll_opy_(bstack1llll1l1111_opy_)
            bstack1l1lll11l1l_opy_ = bstack1llll1l111l_opy_(bstack1l1llll1lll_opy_, bstack1llll1l1111_opy_, bs_config)
            bstack1l1llll1lll_opy_ = bstack1l1lll11l1l_opy_ if bstack1l1lll11l1l_opy_ else bstack1l1llll1lll_opy_
        if not bstack1l1llll1lll_opy_:
            raise ValueError(bstack1111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡇࡑࡏࠠࡱࡣࡷ࡬ࠥ࡯࡮ࠡࡶ࡫ࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡳࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡦࡰ࡮ࡧࡩࡷࠨጊ"))
    except Exception as ex:
        logger.error(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࠦࡃࡍࡋࠣࡴࡦࡺࡨ࠻ࠢࠥጋ") + str(ex) + bstack1111l_opy_ (u"ࠦࠧጌ"))
    return bstack1l1llll1lll_opy_, bstack1llll1l1111_opy_
bstack1ll11l11l11_opy_ = bstack1111l_opy_ (u"ࠧ࠿࠹࠺࠻ࠥግ")
bstack1l1ll1ll111_opy_ = bstack1111l_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧጎ")
bstack1l1lll1lll1_opy_ = bstack1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦጏ")
bstack1l1lll1llll_opy_ = bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨጐ")
BROWSERSTACK_AUTOMATION = bstack1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧ጑")
bstack1ll11111l11_opy_ = re.compile(bstack1111l_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤጒ"))
bstack1ll11111lll_opy_ = bstack1111l_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤጓ")
bstack1l1lllll1l1_opy_ = bstack1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡕࡒࡄࡇࡢࡊࡆࡒࡌࡃࡃࡆࡏࠧጔ")
bstack1l1ll111lll_opy_ = [
    Events.bstack11l111ll1_opy_,
    Events.CONNECT,
    Events.bstack1ll1l1lll_opy_,
]
def _1ll1111l11l_opy_():
    bstack1111l_opy_ (u"ࠨࠢࠣࡈࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࠿ࠤ࠶࠿࠮࠵࠰࠳ࠤࡼ࡮ࡥࡳࡧࠣࡆࡷࡵࡷࡴࡧࡵ࠲ࡪࡴࡴࡳࡻ࠱࡫ࡪࡺ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡴࠢࡧࡳࡪࡹ࡮ࠨࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥࠦࠧጕ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l1llll11ll_opy_ = Path(Browser.__file__).parent / bstack1111l_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡲࠣ጖") / bstack1111l_opy_ (u"ࠣࡲࡤࡧࡰࡧࡧࡦ࠰࡭ࡷࡴࡴࠢ጗")
        bstack1ll111111ll_opy_ = json.loads(bstack1l1llll11ll_opy_.read_text())
        match = re.search(bstack1111l_opy_ (u"ࡴࠥࡠࡩ࠱࡜࠯࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭ࠥጘ"), bstack1ll111111ll_opy_[bstack1111l_opy_ (u"ࠥࡨࡪࡶࡥ࡯ࡦࡨࡲࡨ࡯ࡥࡴࠤጙ")][bstack1111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣጚ")])
        bstack1l1l1llll1l_opy_ = match.group(0) if match else bstack1111l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨጛ")
    except Exception:
        bstack1l1l1llll1l_opy_ = bstack1111l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢጜ")
    return SimpleNamespace(version=bstack1l1l1llll1l_opy_)
class SDKCLI:
    _1ll11l111ll_opy_ = None
    process: Union[None, Any]
    bstack1l1llll1l11_opy_: bool
    bstack1l1l1lll11l_opy_: bool
    bstack1l1lll1111l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll111l1l1l_opy_: Union[None, grpc.Channel]
    bstack1l1lll11lll_opy_: str
    test_framework: TestFramework
    bstack1ll1ll1l11l_opy_: bstack1ll1llll111_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l1lll1l1l1_opy_: bstack11l1l111ll_opy_
    accessibility: bstack1ll11l1l11l_opy_
    bstack1l1ll1l11_opy_: bstack111l11l1_opy_
    ai: bstack1l1llll111l_opy_
    bstack1l1llll11l1_opy_: bstack1l1ll1lll1l_opy_
    bstack1ll11111111_opy_: List[bstack1ll1111l1ll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll11ll1l11_opy_: Any
    bstack1l1ll11ll1l_opy_: Dict[str, timedelta]
    bstack1ll1111l111_opy_: str
    bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_
    def __new__(cls):
        if not cls._1ll11l111ll_opy_:
            cls._1ll11l111ll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll11l111ll_opy_
    def __init__(self):
        self.process = None
        self.bstack1l1llll1l11_opy_ = False
        self.bstack1ll111l1l1l_opy_ = None
        self.bstack1ll1ll1lll1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l1lll1llll_opy_, None)
        self.bstack1ll111l111l_opy_ = os.environ.get(bstack1l1lll1lll1_opy_, bstack1111l_opy_ (u"ࠢࠣጝ")) == bstack1111l_opy_ (u"ࠣࠤጞ")
        self.bstack1l1l1lll11l_opy_ = False
        self.bstack1l1lll1111l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll11ll1l11_opy_ = None
        self.test_framework = None
        self.bstack1ll1ll1l11l_opy_ = None
        self.bstack1l1lll11lll_opy_=bstack1111l_opy_ (u"ࠤࠥጟ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l1ll11ll1l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1ll1ll11lll_opy_ = bstack1ll1ll11l11_opy_()
        self.bstack1l1lllll11l_opy_ = False
        self.bstack1ll111ll111_opy_ = None
        self.bstack1l1lll1l11l_opy_ = None
        self.bstack1l1lll1l1l1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll11111111_opy_ = []
    def bstack11l1ll11ll_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack1111l_opy_ (u"ࠥࡸࡷࡻࡥࠣጠ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l1lllll1l1_opy_, bstack1111l_opy_ (u"ࠫࠬጡ")).lower() in [bstack1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪጢ"), bstack1111l_opy_ (u"࠭࠱ࠨጣ"), bstack1111l_opy_ (u"ࠧࡺࡧࡶࠫጤ")]:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡈࡲࡶࡨ࡯࡮ࡨࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡵࡤࡦࠢࡧࡹࡪࠦࡴࡰࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠤጥ"))
            os.environ[bstack1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧጦ")] = bstack1111l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤጧ")
            return False
        if bstack1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨጨ") in config and str(config[bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩጩ")]).lower() != bstack1111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬጪ"):
            return False
        bstack1ll11ll11ll_opy_ = [bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢጫ"), bstack1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧጬ"), bstack1111l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠥጭ")]
        if is_robot_playwright_installed():
            bstack1ll11ll11ll_opy_.append(bstack1111l_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࠤጮ"))
            bstack1ll11ll11ll_opy_.append(bstack1111l_opy_ (u"ࠦࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠧጯ"))
        bstack1ll1111ll11_opy_ = config.get(bstack1111l_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣጰ")) in bstack1ll11ll11ll_opy_ or os.environ.get(bstack1111l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧጱ")) in bstack1ll11ll11ll_opy_
        os.environ[bstack1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥጲ")] = str(bstack1ll1111ll11_opy_) # bstack1l1ll1l111l_opy_ bstack1ll111l1111_opy_ VAR to bstack1ll111lll1l_opy_ is binary running
        return bstack1ll1111ll11_opy_
    def bstack1l1l1lll1l_opy_(self):
        for event in bstack1l1ll111lll_opy_:
            bstack1111ll11_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1111ll11_opy_.logger.debug(bstack1111l_opy_ (u"ࠣࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠠ࠾ࡀࠣࡿࡦࡸࡧࡴࡿࠣࠦጳ") + str(kwargs) + bstack1111l_opy_ (u"ࠤࠥጴ"))
            )
        bstack1111ll11_opy_.register(Events.bstack11l111ll1_opy_, self.__1l1l1lll1ll_opy_)
        bstack1111ll11_opy_.register(Events.CONNECT, self.__1ll111l1lll_opy_)
        bstack1111ll11_opy_.register(Events.bstack1ll1l1lll_opy_, self.__1ll11l1l1ll_opy_)
        bstack1111ll11_opy_.register(Events.bstack1l1llllll_opy_, self.__1l1ll1111ll_opy_)
    def bstack11l1l111_opy_(self):
        return not self.bstack1ll111l111l_opy_ and os.environ.get(bstack1l1lll1lll1_opy_, bstack1111l_opy_ (u"ࠥࠦጵ")) != bstack1111l_opy_ (u"ࠦࠧጶ")
    def is_running(self):
        if self.bstack1ll111l111l_opy_:
            return self.bstack1l1llll1l11_opy_
        else:
            return bool(self.bstack1ll111l1l1l_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ጷ"))
                and self.config_observability.options.allow_screenshots == bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫጸ")
            )
        except Exception:
            return False
    def bstack1lllll1ll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll11111111_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll111l1l11_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1ll11l1ll11_opy_(self, bstack1ll11l1l1l1_opy_=10):
        if self.bstack1ll1ll1lll1_opy_:
            return
        bstack1lll1l11l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l1lll1llll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1111l_opy_ (u"ࠢ࡜ࠤጹ") + str(id(self)) + bstack1111l_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢጺ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1111l_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦጻ"), 0), (bstack1111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨጼ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll11l1l1l1_opy_)
        self.bstack1ll111l1l1l_opy_ = channel
        self.bstack1ll1ll1lll1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll111l1l1l_opy_)
        self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥጽ"), datetime.now() - bstack1lll1l11l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l1lll1llll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1111l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧጾ") + str(self.bstack11l1l111_opy_()) + bstack1111l_opy_ (u"ࠨࠢጿ"))
    def __1ll11l1l1ll_opy_(self, event_name):
        if self.bstack11l1l111_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢፀ"))
        self.__1l1ll1l11l1_opy_()
    @measure(event_name=EVENTS.bstack1ll1111ll1l_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1l1ll1111ll_opy_(self, event_name, bstack1l1ll1l1lll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1111l_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣፁ"))
        bstack1l1ll1ll1l1_opy_ = Path(bstack1ll1l11l1ll_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥፂ"))
        if self.bstack1llll1l1111_opy_ and bstack1l1ll1ll1l1_opy_.exists():
            with open(bstack1l1ll1ll1l1_opy_, bstack1111l_opy_ (u"ࠪࡶࠬፃ"), encoding=bstack1111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪፄ")) as fp:
                data = json.load(fp)
                try:
                    bstack1llll1ll1_opy_(bstack1111l_opy_ (u"ࠬࡖࡏࡔࡖࠪፅ"), bstack11lll1ll_opy_(bstack1l111l1111_opy_), data, {
                        bstack1111l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫፆ"): (self.config[bstack1111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩፇ")], self.config[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫፈ")])
                    })
                except Exception as e:
                    logger.debug(bstack11ll11l1_opy_.format(str(e)))
            bstack1l1ll1ll1l1_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l1ll1lll11_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1l1l1lll1ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
        self.bstack1l1lll11lll_opy_, self.bstack1llll1l1111_opy_ = bstack1l1l1lllll1_opy_(data.bs_config)
        os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧፉ")] = self.bstack1llll1l1111_opy_
        if not self.bstack1l1lll11lll_opy_ or not self.bstack1llll1l1111_opy_:
            raise ValueError(bstack1111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤፊ"))
        if self.bstack11l1l111_opy_():
            self.__1ll111l1lll_opy_(event_name, bstack1lllll111l_opy_())
            return
        try:
            logger.debug(bstack1111l_opy_ (u"ࠦࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡓࡅࡍࠣࡗࡪࡺࡵࡱ࠰ࠥፋ"))
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤፌ").format(e))
        start = datetime.now()
        is_started = self.__1l1lll111l1_opy_()
        self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡳࡱࡣࡺࡲࡤࡺࡩ࡮ࡧࠥፍ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll11l1ll11_opy_()
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨፎ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1lll1ll11_opy_(data)
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨፏ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1ll11llll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1ll111l1lll_opy_(self, event_name: str, data: bstack1lllll111l_opy_):
        if not self.bstack11l1l111_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨፐ"))
            return
        bin_session_id = os.environ.get(bstack1l1lll1lll1_opy_)
        start = datetime.now()
        self.__1ll11l1ll11_opy_()
        self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤፑ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1111l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊࠢࠥፒ") + str(bin_session_id) + bstack1111l_opy_ (u"ࠧࠨፓ"))
        start = datetime.now()
        self.__1l1ll11l11l_opy_()
        self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦፔ"), datetime.now() - start)
    def __1ll11ll1l1l_opy_(self):
        if not self.bstack1ll1ll1lll1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦፕ"))
            return
        bstack1ll111111l1_opy_ = {
            bstack1111l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧፖ"): (bstack1l1lllll1ll_opy_, bstack1ll11l1lll1_opy_, bstack1ll1llllll1_opy_),
            bstack1111l_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦፗ"): (bstack1l1lll11ll1_opy_, bstack1l1ll11l1ll_opy_, bstack1ll111ll1ll_opy_),
        }
        if not self.bstack1ll111ll111_opy_ and self.session_framework in bstack1ll111111l1_opy_:
            bstack1l1ll1l1l1l_opy_, bstack1ll11ll11l1_opy_, bstack1ll111l11ll_opy_ = bstack1ll111111l1_opy_[self.session_framework]
            bstack1l1llll1ll1_opy_ = bstack1ll11ll11l1_opy_()
            self.bstack1l1lll1l11l_opy_ = bstack1l1llll1ll1_opy_
            self.bstack1ll111ll111_opy_ = bstack1ll111l11ll_opy_
            self.bstack1ll11111111_opy_.append(bstack1l1llll1ll1_opy_)
            self.bstack1ll11111111_opy_.append(bstack1l1ll1l1l1l_opy_(self.bstack1l1lll1l11l_opy_))
        if not self.bstack1l1lll1l1l1_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1l1lll1l1l1_opy_ = bstack11l1l111ll_opy_(self.bstack1ll111ll111_opy_, self.bstack1l1lll1l11l_opy_)
            self.bstack1ll11111111_opy_.append(self.bstack1l1lll1l1l1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll11l1l11l_opy_(self.bstack1ll111ll111_opy_, self.bstack1l1lll1l11l_opy_)
            self.bstack1ll11111111_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1111l_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧፘ"), False) == True:
            self.ai = bstack1l1llll111l_opy_()
            self.bstack1ll11111111_opy_.append(self.ai)
        if not self.percy and self.bstack1ll11ll1l11_opy_ and self.bstack1ll11ll1l11_opy_.success:
            self.percy = bstack1l1ll1lll1l_opy_(self.bstack1ll11ll1l11_opy_)
            self.bstack1ll11111111_opy_.append(self.percy)
        for mod in self.bstack1ll11111111_opy_:
            if not mod.bstack1l1lllll111_opy_():
                mod.configure(self.bstack1ll1ll1lll1_opy_, self.config, self.cli_bin_session_id, self.bstack1ll1ll11lll_opy_)
    def __1l1lll11l11_opy_(self):
        for mod in self.bstack1ll11111111_opy_:
            if mod.bstack1l1lllll111_opy_():
                mod.configure(self.bstack1ll1ll1lll1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l1ll1l11ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1l1lll1ll11_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l1l1lll11l_opy_:
            return
        self.__1l1ll1llll1_opy_(data)
        bstack1lll1l11l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1111l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦፙ")
        req.sdk_language = bstack1111l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧፚ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll11111l11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭፛"), bstack1111l_opy_ (u"ࠧ࠱ࠩ፜")))
            req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ፝").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡪࡤࡪࡰࡪࠤࡼࡵࡲ࡬ࡧࡵࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹ࠼ࠣࡿࢂࠨ፞").format(e))
        try:
            self.logger.debug(bstack1111l_opy_ (u"ࠥ࡟ࠧ፟") + str(id(self)) + bstack1111l_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥ፠"))
            r = self.bstack1ll1ll1lll1_opy_.StartBinSession(req)
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢ፡"), datetime.now() - bstack1lll1l11l_opy_)
            os.environ[bstack1l1lll1lll1_opy_] = r.bin_session_id
            self.__1ll11111l1l_opy_(r)
            self.__1ll11ll1l1l_opy_()
            if not self.bstack1l1lllll11l_opy_:
                self.bstack1ll1ll11lll_opy_.start()
                self.bstack1l1lllll11l_opy_ = True
                atexit.register(self.__1l1ll1l1111_opy_)
            self.bstack1l1l1lll11l_opy_ = True
            self.logger.debug(bstack1111l_opy_ (u"ࠨ࡛ࠣ።") + str(id(self)) + bstack1111l_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧ፣"))
        except grpc.bstack1l1l1llllll_opy_ as bstack1l1ll1ll1ll_opy_:
            self.logger.error(bstack1111l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ፤") + str(bstack1l1ll1ll1ll_opy_) + bstack1111l_opy_ (u"ࠤࠥ፥"))
            traceback.print_exc()
            raise bstack1l1ll1ll1ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ፦") + str(e) + bstack1111l_opy_ (u"ࠦࠧ፧"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1lll1l1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1l1ll11l11l_opy_(self):
        if not self.bstack11l1l111_opy_() or not self.cli_bin_session_id or self.bstack1l1lll1111l_opy_:
            return
        bstack1lll1l11l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ፨"), bstack1111l_opy_ (u"࠭࠰ࠨ፩")))
        req.client_worker_id = bstack1111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ፪").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1111l_opy_ (u"ࠣ࡝ࠥ፫") + str(id(self)) + bstack1111l_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦ፬"))
            r = self.bstack1ll1ll1lll1_opy_.ConnectBinSession(req)
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢ፭"), datetime.now() - bstack1lll1l11l_opy_)
            self.__1ll11111l1l_opy_(r)
            self.__1ll11ll1l1l_opy_()
            if not self.bstack1l1lllll11l_opy_:
                self.bstack1ll1ll11lll_opy_.start()
                self.bstack1l1lllll11l_opy_ = True
                atexit.register(self.__1l1ll1l1111_opy_)
            self.bstack1l1lll1111l_opy_ = True
            self.logger.debug(bstack1111l_opy_ (u"ࠦࡠࠨ፮") + str(id(self)) + bstack1111l_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦ፯"))
        except grpc.bstack1l1l1llllll_opy_ as bstack1l1ll1ll1ll_opy_:
            self.logger.error(bstack1111l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ፰") + str(bstack1l1ll1ll1ll_opy_) + bstack1111l_opy_ (u"ࠢࠣ፱"))
            traceback.print_exc()
            raise bstack1l1ll1ll1ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ፲") + str(e) + bstack1111l_opy_ (u"ࠤࠥ፳"))
            traceback.print_exc()
            raise e
    def __1ll11111l1l_opy_(self, r):
        self.bstack1l1lll1ll1l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1111l_opy_ (u"ࠥࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤ፴") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1111l_opy_ (u"ࠦࡪࡳࡰࡵࡻࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡻ࡮ࡥࠤ፵"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡩࡷࡩࡹࠡ࡫ࡶࠤࡸ࡫࡮ࡵࠢࡲࡲࡱࡿࠠࡢࡵࠣࡴࡦࡸࡴࠡࡱࡩࠤࡹ࡮ࡥࠡࠤࡆࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠲ࠢࠡࡣࡱࡨࠥࡺࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡣ࡯ࡷࡴࠦࡵࡴࡧࡧࠤࡧࡿࠠࡔࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࡳࡧࡩࡳࡷ࡫ࠬࠡࡐࡲࡲࡪࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡ࡫ࡶࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ፶")
        self.bstack1ll11ll1l11_opy_ = getattr(r, bstack1111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ፷"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ፸")] = self.config_testhub.jwt
        os.environ[bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭፹")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1llllll1l_opy_ = json.loads(r.config)
            bstack1ll1111lll1_opy_ = bstack1l1llllll1l_opy_.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭፺"), {}).get(bstack1111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ፻"), bstack1111l_opy_ (u"ࠫࠬ፼"))
            os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ፽")] = bstack1ll1111lll1_opy_
    def bstack1ll11ll1ll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l1llll1l11_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll11l111l1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll11l111l1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll11ll1ll1_opy_(event_name=EVENTS.bstack1l1ll111ll1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1l1lll111l1_opy_(self, bstack1ll11l1l1l1_opy_=10):
        if self.bstack1l1llll1l11_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣ፾"))
            return True
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨ፿"))
        if os.getenv(bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣᎀ")) == bstack1ll11111lll_opy_:
            self.cli_bin_session_id = bstack1ll11111lll_opy_
            self.cli_listen_addr = bstack1111l_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧᎁ") % (self.cli_bin_session_id)
            self.bstack1l1llll1l11_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1lll11lll_opy_, bstack1111l_opy_ (u"ࠥࡷࡩࡱࠢᎂ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll11l1l111_opy_ compat for text=True in bstack1ll111l1ll1_opy_ python
            encoding=bstack1111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᎃ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll11l1111l_opy_ = threading.Thread(target=self.__1l1ll11ll11_opy_, args=(bstack1ll11l1l1l1_opy_,))
        bstack1ll11l1111l_opy_.start()
        bstack1ll11l1111l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤᎄ") + str(self.process.stderr.read()) + bstack1111l_opy_ (u"ࠨࠢᎅ"))
        if not self.bstack1l1llll1l11_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠢ࡜ࠤᎆ") + str(id(self)) + bstack1111l_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦᎇ"))
            self.__1l1ll1l11l1_opy_()
        self.logger.debug(bstack1111l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥᎈ") + str(self.bstack1l1llll1l11_opy_) + bstack1111l_opy_ (u"ࠥࠦᎉ"))
        return self.bstack1l1llll1l11_opy_
    def __1l1ll11ll11_opy_(self, bstack1ll11ll1111_opy_=10):
        bstack1l1llll1l1l_opy_ = time.time()
        while self.process and time.time() - bstack1l1llll1l1l_opy_ < bstack1ll11ll1111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1111l_opy_ (u"ࠦ࡮ࡪ࠽ࠣᎊ") in line:
                    self.cli_bin_session_id = line.split(bstack1111l_opy_ (u"ࠧ࡯ࡤ࠾ࠤᎋ"))[-1:][0].strip()
                    self.logger.debug(bstack1111l_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧᎌ") + str(self.cli_bin_session_id) + bstack1111l_opy_ (u"ࠢࠣᎍ"))
                    continue
                if bstack1111l_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᎎ") in line:
                    self.cli_listen_addr = line.split(bstack1111l_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᎏ"))[-1:][0].strip()
                    self.logger.debug(bstack1111l_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨ᎐") + str(self.cli_listen_addr) + bstack1111l_opy_ (u"ࠦࠧ᎑"))
                    continue
                if bstack1111l_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦ᎒") in line:
                    port = line.split(bstack1111l_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧ᎓"))[-1:][0].strip()
                    self.logger.debug(bstack1111l_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨ᎔") + str(port) + bstack1111l_opy_ (u"ࠣࠤ᎕"))
                    continue
                if line.strip() == bstack1l1ll1ll111_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦ᎖"), bstack1111l_opy_ (u"ࠥ࠵ࠧ᎗")) == bstack1111l_opy_ (u"ࠦ࠶ࠨ᎘"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l1llll1l11_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨ᎙") + str(e) + bstack1111l_opy_ (u"ࠨࠢ᎚"))
        return False
    def __1l1ll1l1111_opy_(self):
        bstack1111l_opy_ (u"ࠢࠣࠤࡆࡰࡪࡧ࡮ࡶࡲࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡫ࡵࡲࠡࡣࡶࡽࡳࡩ࡟ࡥ࡫ࡶࡴࡦࡺࡣࡩࡧࡵ࠰ࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡣࡷࡩࡽ࡯ࡴࠡࡶࡲࠤࡪࡴࡳࡶࡴࡨࠤࡹࡧࡳ࡬ࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨࠢࠣ᎛")
        if self.bstack1ll1ll11lll_opy_ and self.bstack1l1lllll11l_opy_:
            try:
                self.bstack1ll1ll11lll_opy_.stop()
                self.bstack1l1lllll11l_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1lll111ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def __1l1ll1l11l1_opy_(self):
        if self.bstack1ll111l1l1l_opy_:
            if self.bstack1ll1ll11lll_opy_ and self.bstack1l1lllll11l_opy_:
                try:
                    atexit.unregister(self.__1l1ll1l1111_opy_)
                except ValueError:
                    pass
                self.bstack1ll1ll11lll_opy_.stop()
                self.bstack1l1lllll11l_opy_ = False
            start = datetime.now()
            if self.bstack1l1ll111l1l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1lll1111l_opy_:
                    self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧ᎜"), datetime.now() - start)
                else:
                    self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨ᎝"), datetime.now() - start)
            self.__1l1lll11l11_opy_()
            start = datetime.now()
            bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(bstack1111l_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࠣ᎞"))
            self.bstack1ll111l1l1l_opy_.close()
            bstack1l11ll1l1_opy_.end(bstack1111l_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࠤ᎟"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᎠ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᎡ"), True, None, None, None, None)
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠢࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤᎢ"), datetime.now() - start)
            self.bstack1ll111l1l1l_opy_ = None
        if self.process:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡵࡷࡳࡵࠨᎣ"))
            start = datetime.now()
            bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(bstack1111l_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽࡯࡮ࡲ࡬ࠣᎤ"))
            self.process.terminate()
            bstack1l11ll1l1_opy_.end(bstack1111l_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡰ࡯࡬࡭ࠤᎥ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᎦ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᎧ"), True, None, None, None, None)
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨ࡫ࡪ࡮࡯ࡣࡹ࡯࡭ࡦࠤᎨ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll111l111l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l11l1l11l_opy_()
                self.logger.info(
                    bstack1111l_opy_ (u"ࠢࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠢᎩ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1111l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᎪ")] = self.config_testhub.build_hashed_id
        self.bstack1l1llll1l11_opy_ = False
    def __1l1ll1llll1_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1111l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᎫ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1ll1lllll_opy_ = get_pw_version()
            except:
                bstack1l1ll1lllll_opy_ = _1ll1111l11l_opy_()
            data.framework_versions[bstack1111l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᎬ")] = bstack1l1ll1lllll_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack1111l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᎭ")] = selenium.__version__
                data.frameworks.append(bstack1111l_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᎮ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1111l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᎯ")] = __version__
                data.frameworks.append(bstack1111l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᎰ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack1111l_opy_ (u"ࠣࡐࡲࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧࠦᎱ"))
    def bstack1ll11111ll1_opy_(self, hub_url: str, platform_index: int, bstack1l11l1111l_opy_: Any):
        if self.bstack1ll1ll1l11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨᎲ"))
            return
        try:
            bstack1lll1l11l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1111l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᎳ")
            self.bstack1ll1ll1l11l_opy_ = bstack1ll111ll1ll_opy_(
                cli.config.get(bstack1111l_opy_ (u"ࠦ࡭ࡻࡢࡖࡴ࡯ࠦᎴ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1ll111l11_opy_={bstack1111l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤᎵ"): bstack1l11l1111l_opy_}
            )
            def bstack1ll111ll1l1_opy_(self):
                return
            if self.config.get(bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠣᎶ"), True):
                Service.start = bstack1ll111ll1l1_opy_
                Service.stop = bstack1ll111ll1l1_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack111l11l1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll111lll11_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᎷ"), datetime.now() - bstack1lll1l11l_opy_)
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࠢᎸ") + str(e) + bstack1111l_opy_ (u"ࠤࠥᎹ"))
    def bstack1lll11llll_opy_(self, platform_index: int):
        if self.bstack1ll1ll1l11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᎺ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1ll1111llll_opy_
                self.bstack1ll1ll1l11l_opy_ = bstack1ll1llllll1_opy_(
                    platform_index,
                    framework_name=bstack1111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᎻ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1ll1111l11l_opy_
                from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll1l1ll1l1_opy_
                bstack1l1ll1lllll_opy_ = get_pw_version()
                self.bstack1ll1ll1l11l_opy_ = bstack1ll1llllll1_opy_(
                    platform_index,
                    framework_name=bstack1111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᎼ"),
                    framework_version=bstack1l1ll1lllll_opy_.version,
                    classes=[],
                )
                ctx = bstack1ll1l1ll1l1_opy_.create_context(self.bstack1ll1ll1l11l_opy_)
                bstack1ll1llll111_opy_.bstack1ll1lll111l_opy_[ctx.id] = bstack1ll1l1lll1l_opy_(
                    ctx, bstack1111l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᎽ"), bstack1l1ll1lllll_opy_, bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_
                )
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣᎾ") + str(e) + bstack1111l_opy_ (u"ࠣࠤᎿ"))
            pass
    def bstack1ll1llll1l_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᏀ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1l1llllll11_opy_({ bstack1111l_opy_ (u"ࠥࡶࡴࡨ࡯ࡵ࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᏁ"): VERSION }, [bstack1111l_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥᏂ")], self.bstack1ll1ll11lll_opy_, self.bstack1ll1ll1lll1_opy_)
                return
            except Exception as e:
                self.logger.error(bstack1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡳࡱࡥࡳࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࠦᏃ") + str(e) + bstack1111l_opy_ (u"ࠨࠢᏄ"))
        if bstack111ll11ll1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᏅ"): pytest.__version__ }, [bstack1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᏆ")], self.bstack1ll1ll11lll_opy_, self.bstack1ll1ll1lll1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1ll11lll1_opy_({ bstack1111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᏇ"): pytest.__version__ }, [bstack1111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᏈ")], self.bstack1ll1ll11lll_opy_, self.bstack1ll1ll1lll1_opy_)
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࠣᏉ") + str(e) + bstack1111l_opy_ (u"ࠧࠨᏊ"))
        self.bstack1l1lll11111_opy_()
    def bstack1l1lll11111_opy_(self):
        if not self.bstack11l1ll11ll_opy_():
            return
        bstack1l11l1l1_opy_ = None
        def bstack1111ll11l_opy_(config, startdir):
            return bstack1111l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦᏋ").format(bstack1111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᏌ"))
        def bstack1l1l1l11_opy_():
            return
        def bstack1l1111ll1l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1111l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᏍ"):
                return bstack1111l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᏎ")
            else:
                return bstack1l11l1l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l11l1l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1111ll11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l11_opy_
            Config.getoption = bstack1l1111ll1l_opy_
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬ࠥࡶࡹࡵࡧࡶࡸࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠽ࠤࠧᏏ") + str(e) + bstack1111l_opy_ (u"ࠦࠧᏐ"))
    def bstack1l1lll1l111_opy_(self):
        bstack11111ll11_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11111ll11_opy_, dict):
            if cli.config_observability:
                bstack11111ll11_opy_.update(
                    {bstack1111l_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᏑ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᏒ") in accessibility.get(bstack1111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᏓ"), {}):
                    bstack1l1ll11l111_opy_ = accessibility.get(bstack1111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᏔ"))
                    bstack1l1ll11l111_opy_.update({ bstack1111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠥᏕ"): bstack1l1ll11l111_opy_.pop(bstack1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨᏖ")) })
                bstack11111ll11_opy_.update({bstack1111l_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᏗ"): accessibility })
        return bstack11111ll11_opy_
    @measure(event_name=EVENTS.bstack1l1ll111111_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l1ll111l1l_opy_(self, bstack1l1ll11111l_opy_: str = None, bstack1l1llll1111_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1ll1lll1_opy_:
            return
        bstack1lll1l11l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᏘ"), bstack1111l_opy_ (u"࠭࠰ࠨᏙ")))
        req.client_worker_id = bstack1111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᏚ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l1ll11111l_opy_:
            req.bstack1l1ll11111l_opy_ = bstack1l1ll11111l_opy_
        if bstack1l1llll1111_opy_:
            req.bstack1l1llll1111_opy_ = bstack1l1llll1111_opy_
        try:
            r = self.bstack1ll1ll1lll1_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᏛ"), datetime.now() - bstack1lll1l11l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1l11ll11_opy_(self, key: str, value: timedelta):
        tag = bstack1111l_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᏜ") if self.bstack11l1l111_opy_() else bstack1111l_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᏝ")
        self.bstack1l1ll11ll1l_opy_[bstack1111l_opy_ (u"ࠦ࠿ࠨᏞ").join([tag + bstack1111l_opy_ (u"ࠧ࠳ࠢᏟ") + str(id(self)), key])] += value
    def bstack1l11l1l11l_opy_(self):
        if not os.getenv(bstack1111l_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥᏠ"), bstack1111l_opy_ (u"ࠢ࠱ࠤᏡ")) == bstack1111l_opy_ (u"ࠣ࠳ࠥᏢ"):
            return
        bstack1ll111l11l1_opy_ = dict()
        bstack1ll1lll111l_opy_ = []
        if self.test_framework:
            bstack1ll1lll111l_opy_.extend(list(self.test_framework.bstack1ll1lll111l_opy_.values()))
        if self.bstack1ll1ll1l11l_opy_:
            bstack1ll1lll111l_opy_.extend(list(self.bstack1ll1ll1l11l_opy_.bstack1ll1lll111l_opy_.values()))
        for instance in bstack1ll1lll111l_opy_:
            if not instance.platform_index in bstack1ll111l11l1_opy_:
                bstack1ll111l11l1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll111l11l1_opy_[instance.platform_index]
            for k, v in instance.bstack1l1lll1l1ll_opy_().items():
                report[k] += v
                report[k.split(bstack1111l_opy_ (u"ࠤ࠽ࠦᏣ"))[0]] += v
        bstack1l1ll1l1l11_opy_ = sorted([(k, v) for k, v in self.bstack1l1ll11ll1l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1ll1111l1_opy_ = 0
        for r in bstack1l1ll1l1l11_opy_:
            bstack1ll111llll1_opy_ = r[1].total_seconds()
            bstack1l1ll1111l1_opy_ += bstack1ll111llll1_opy_
            self.logger.debug(bstack1111l_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣᏤ") + str(bstack1ll111llll1_opy_) + bstack1111l_opy_ (u"ࠦࠧᏥ"))
        self.logger.debug(bstack1111l_opy_ (u"ࠧ࠳࠭ࠣᏦ"))
        bstack1ll11l11ll1_opy_ = []
        for platform_index, report in bstack1ll111l11l1_opy_.items():
            bstack1ll11l11ll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll11l11ll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1111l11l11_opy_ = set()
        bstack1ll1111111l_opy_ = 0
        for r in bstack1ll11l11ll1_opy_:
            bstack1ll111llll1_opy_ = r[2].total_seconds()
            bstack1ll1111111l_opy_ += bstack1ll111llll1_opy_
            bstack1111l11l11_opy_.add(r[0])
            self.logger.debug(bstack1111l_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢᏧ") + str(bstack1ll111llll1_opy_) + bstack1111l_opy_ (u"ࠢࠣᏨ"))
        if self.bstack11l1l111_opy_():
            self.logger.debug(bstack1111l_opy_ (u"ࠣ࠯࠰ࠦᏩ"))
            self.logger.debug(bstack1111l_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤᏪ") + str(bstack1ll1111111l_opy_) + bstack1111l_opy_ (u"ࠥࠦᏫ"))
        else:
            self.logger.debug(bstack1111l_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᏬ") + str(bstack1l1ll1111l1_opy_) + bstack1111l_opy_ (u"ࠧࠨᏭ"))
        self.logger.debug(bstack1111l_opy_ (u"ࠨ࠭࠮ࠤᏮ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᏯ"), bstack1111l_opy_ (u"ࠨ࠲ࠪᏰ"))),
            client_worker_id=bstack1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᏱ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1ll1lll1_opy_:
            self.logger.error(bstack1111l_opy_ (u"ࠥࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡄࡣࡱࡲࡴࡺࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᏲ"))
            return None
        response = self.bstack1ll1ll1lll1_opy_.TestOrchestration(request)
        self.logger.debug(bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵ࠯ࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠯ࡶࡩࡸࡹࡩࡰࡰࡀࡿࢂࠨᏳ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l1lll1ll1l_opy_(self, r):
        if r is not None and getattr(r, bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭Ᏼ"), None) and getattr(r.testhub, bstack1111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭Ᏽ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᏶")))
            for bstack1ll11ll111l_opy_, err in errors.items():
                if err[bstack1111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭᏷")] == bstack1111l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᏸ"):
                    self.logger.info(err[bstack1111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᏹ")])
                else:
                    self.logger.error(err[bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᏺ")])
    def bstack1l1l1l1l_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()