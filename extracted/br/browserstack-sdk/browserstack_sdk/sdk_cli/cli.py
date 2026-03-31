# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
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
from browserstack_sdk.sdk_cli.bstack1ll11llll11_opy_ import bstack1ll11llllll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1ll1111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll1ll1_opy_ import bstack1l1l1lll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111ll_opy_ import bstack1l1l11ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111l1l_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l111_opy_ import bstack1l1l1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11ll11_opy_ import bstack1l1llllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l111l_opy_ import bstack1l1llll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1111l11l_opy_ import bstack1l11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l_opy_ import bstack1lll111l_opy_, Events, bstack11lll11ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import bstack111l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1l1llllll_opy_ import bstack1l1ll1l11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack1lll1l1ll_opy_
from bstack_utils.helper import Notset, bstack1lll1l1l11l_opy_, get_cli_dir, bstack1lll1l1l111_opy_, bstack1111l1111l_opy_, bstack1ll11l111l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1l111l1_opy_, TestHookState, bstack1l1l1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import bstack1ll111lllll_opy_, bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1ll1ll11ll_opy_ import bstack1llll1ll1l_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l11l1_opy_, bstack1111l11ll_opy_
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll11_opy_ import bstack1l1lll1l1l1_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll111l1111_opy_(bs_config):
    bstack1l1ll11l1ll_opy_ = None
    bstack1lll1l111ll_opy_ = None
    try:
        bstack1lll1l111ll_opy_ = get_cli_dir()
        bstack1l1ll11l1ll_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦ፝"))
        if not bstack1l1ll11l1ll_opy_:
            bstack1l1ll11l1ll_opy_ = bstack1lll1l1l111_opy_(bstack1lll1l111ll_opy_)
            bstack1l1lll1l11l_opy_ = bstack1lll1l1l11l_opy_(bstack1l1ll11l1ll_opy_, bstack1lll1l111ll_opy_, bs_config)
            bstack1l1ll11l1ll_opy_ = bstack1l1lll1l11l_opy_ if bstack1l1lll1l11l_opy_ else bstack1l1ll11l1ll_opy_
        if not bstack1l1ll11l1ll_opy_:
            raise ValueError(bstack1ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡇࡑࡏࠠࡱࡣࡷ࡬ࠥ࡯࡮ࠡࡶ࡫ࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡳࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡦࡰ࡮ࡧࡩࡷࠨ፞"))
    except Exception as ex:
        logger.error(bstack1ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࠦࡃࡍࡋࠣࡴࡦࡺࡨ࠻ࠢࠥ፟") + str(ex) + bstack1ll11_opy_ (u"ࠦࠧ፠"))
    return bstack1l1ll11l1ll_opy_, bstack1lll1l111ll_opy_
bstack1l1l1l1l1l1_opy_ = bstack1ll11_opy_ (u"ࠧ࠿࠹࠺࠻ࠥ፡")
bstack1l1lll11lll_opy_ = bstack1ll11_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧ።")
bstack1l1l1ll1lll_opy_ = bstack1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦ፣")
bstack1l1ll111111_opy_ = bstack1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨ፤")
BROWSERSTACK_AUTOMATION = bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧ፥")
bstack1l1ll11llll_opy_ = re.compile(bstack1ll11_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤ፦"))
bstack1ll111l1l11_opy_ = bstack1ll11_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤ፧")
bstack1ll1111ll1l_opy_ = bstack1ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡕࡒࡄࡇࡢࡊࡆࡒࡌࡃࡃࡆࡏࠧ፨")
bstack1l1ll111ll1_opy_ = [
    Events.bstack1111l111ll_opy_,
    Events.CONNECT,
    Events.bstack11lll1l11l_opy_,
]
def _1l1llll1l1l_opy_():
    bstack1ll11_opy_ (u"ࠨࠢࠣࡈࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࠿ࠤ࠶࠿࠮࠵࠰࠳ࠤࡼ࡮ࡥࡳࡧࠣࡆࡷࡵࡷࡴࡧࡵ࠲ࡪࡴࡴࡳࡻ࠱࡫ࡪࡺ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡴࠢࡧࡳࡪࡹ࡮ࠨࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥࠦࠧ፩")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l1l11lllll_opy_ = Path(Browser.__file__).parent / bstack1ll11_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡲࠣ፪") / bstack1ll11_opy_ (u"ࠣࡲࡤࡧࡰࡧࡧࡦ࠰࡭ࡷࡴࡴࠢ፫")
        bstack1l1llll1111_opy_ = json.loads(bstack1l1l11lllll_opy_.read_text())
        match = re.search(bstack1ll11_opy_ (u"ࡴࠥࡠࡩ࠱࡜࠯࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭ࠥ፬"), bstack1l1llll1111_opy_[bstack1ll11_opy_ (u"ࠥࡨࡪࡶࡥ࡯ࡦࡨࡲࡨ࡯ࡥࡴࠤ፭")][bstack1ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ፮")])
        bstack1l1ll1l1lll_opy_ = match.group(0) if match else bstack1ll11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ፯")
    except Exception:
        bstack1l1ll1l1lll_opy_ = bstack1ll11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ፰")
    return SimpleNamespace(version=bstack1l1ll1l1lll_opy_)
class SDKCLI:
    _1ll1l1ll1l1_opy_ = None
    process: Union[None, Any]
    bstack1ll111l1l1l_opy_: bool
    bstack1l1llll1l11_opy_: bool
    bstack1ll111l11l1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l1l11lll11_opy_: Union[None, grpc.Channel]
    bstack1l1llllllll_opy_: str
    test_framework: TestFramework
    bstack1l11111ll_opy_: bstack111l1ll111_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l1ll1lllll_opy_: bstack1l11l111l_opy_
    accessibility: bstack1ll1ll1111l_opy_
    bstack1l1lll1ll_opy_: bstack1lll1l1ll_opy_
    ai: bstack1l1l1lll1ll_opy_
    bstack1l1ll1l1l11_opy_: bstack1l1l11ll1ll_opy_
    bstack1l1lll111l1_opy_: List[bstack1ll111l11ll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l1lll11l11_opy_: Any
    bstack1l1l1ll1l1l_opy_: Dict[str, timedelta]
    bstack1l1lll1l111_opy_: str
    bstack1ll11llll11_opy_: bstack1ll11llllll_opy_
    def __new__(cls):
        if not cls._1ll1l1ll1l1_opy_:
            cls._1ll1l1ll1l1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1l1ll1l1_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll111l1l1l_opy_ = False
        self.bstack1l1l11lll11_opy_ = None
        self.bstack1l1ll1ll111_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l1ll111111_opy_, None)
        self.bstack1l1l11lll1l_opy_ = os.environ.get(bstack1l1l1ll1lll_opy_, bstack1ll11_opy_ (u"ࠢࠣ፱")) == bstack1ll11_opy_ (u"ࠣࠤ፲")
        self.bstack1l1llll1l11_opy_ = False
        self.bstack1ll111l11l1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l1lll11l11_opy_ = None
        self.test_framework = None
        self.bstack1l11111ll_opy_ = None
        self.bstack1l1llllllll_opy_=bstack1ll11_opy_ (u"ࠤࠥ፳")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l1l1ll1l1l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1ll11llll11_opy_ = bstack1ll11llllll_opy_()
        self.bstack1l1ll111lll_opy_ = False
        self.bstack1l1l11ll1l1_opy_ = None
        self.bstack1l1l1l1ll11_opy_ = None
        self.bstack1l1ll1lllll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l1lll111l1_opy_ = []
    def bstack1ll11l1l11_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack1ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣ፴"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll1111ll1l_opy_, bstack1ll11_opy_ (u"ࠫࠬ፵")).lower() in [bstack1ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪ፶"), bstack1ll11_opy_ (u"࠭࠱ࠨ፷"), bstack1ll11_opy_ (u"ࠧࡺࡧࡶࠫ፸")]:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡈࡲࡶࡨ࡯࡮ࡨࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡵࡤࡦࠢࡧࡹࡪࠦࡴࡰࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠤ፹"))
            os.environ[bstack1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧ፺")] = bstack1ll11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤ፻")
            return False
        if bstack1ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ፼") in config and str(config[bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ፽")]).lower() != bstack1ll11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ፾"):
            return False
        bstack1ll1111llll_opy_ = [bstack1ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢ፿"), bstack1ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᎀ"), bstack1ll11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠥᎁ")]
        if is_robot_playwright_installed():
            bstack1ll1111llll_opy_.append(bstack1ll11_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࠤᎂ"))
            bstack1ll1111llll_opy_.append(bstack1ll11_opy_ (u"ࠦࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠧᎃ"))
        bstack1l1l1lll1l1_opy_ = config.get(bstack1ll11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣᎄ")) in bstack1ll1111llll_opy_ or os.environ.get(bstack1ll11_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧᎅ")) in bstack1ll1111llll_opy_
        os.environ[bstack1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥᎆ")] = str(bstack1l1l1lll1l1_opy_) # bstack1l1lll1ll1l_opy_ bstack1ll11111lll_opy_ VAR to bstack1l1ll1lll1l_opy_ is binary running
        return bstack1l1l1lll1l1_opy_
    def bstack1lll1l1ll1_opy_(self):
        for event in bstack1l1ll111ll1_opy_:
            bstack1lll111l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1lll111l_opy_.logger.debug(bstack1ll11_opy_ (u"ࠣࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠠ࠾ࡀࠣࡿࡦࡸࡧࡴࡿࠣࠦᎇ") + str(kwargs) + bstack1ll11_opy_ (u"ࠤࠥᎈ"))
            )
        bstack1lll111l_opy_.register(Events.bstack1111l111ll_opy_, self.__1l1l11llll1_opy_)
        bstack1lll111l_opy_.register(Events.CONNECT, self.__1l1l1l111ll_opy_)
        bstack1lll111l_opy_.register(Events.bstack11lll1l11l_opy_, self.__1ll111l111l_opy_)
        bstack1lll111l_opy_.register(Events.bstack11111ll11l_opy_, self.__1ll11111l1l_opy_)
    def bstack1ll1111lll_opy_(self):
        return not self.bstack1l1l11lll1l_opy_ and os.environ.get(bstack1l1l1ll1lll_opy_, bstack1ll11_opy_ (u"ࠥࠦᎉ")) != bstack1ll11_opy_ (u"ࠦࠧᎊ")
    def is_running(self):
        if self.bstack1l1l11lll1l_opy_:
            return self.bstack1ll111l1l1l_opy_
        else:
            return bool(self.bstack1l1l11lll11_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᎋ"))
                and self.config_observability.options.allow_screenshots == bstack1ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫᎌ")
            )
        except Exception:
            return False
    def bstack11ll1lll11_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l1lll111l1_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l1lll1ll11_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1ll1l1l1l_opy_(self, bstack1l1lll1l1ll_opy_=10):
        if self.bstack1l1ll1ll111_opy_:
            return
        bstack11l111ll1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l1ll111111_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1ll11_opy_ (u"ࠢ࡜ࠤᎍ") + str(id(self)) + bstack1ll11_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢᎎ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦᎏ"), 0), (bstack1ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨ᎐"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1lll1l1ll_opy_)
        self.bstack1l1l11lll11_opy_ = channel
        self.bstack1l1ll1ll111_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l1l11lll11_opy_)
        self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥ᎑"), datetime.now() - bstack11l111ll1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l1ll111111_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧ᎒") + str(self.bstack1ll1111lll_opy_()) + bstack1ll11_opy_ (u"ࠨࠢ᎓"))
    def __1ll111l111l_opy_(self, event_name):
        if self.bstack1ll1111lll_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢ᎔"))
        self.__1l1l1ll1111_opy_()
    @measure(event_name=EVENTS.bstack1ll11111ll1_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1ll11111l1l_opy_(self, event_name, bstack1l1lll11ll1_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1ll11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣ᎕"))
        bstack1l1lll11111_opy_ = Path(bstack1ll11l1ll11_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥ᎖"))
        if self.bstack1lll1l111ll_opy_ and bstack1l1lll11111_opy_.exists():
            with open(bstack1l1lll11111_opy_, bstack1ll11_opy_ (u"ࠪࡶࠬ᎗"), encoding=bstack1ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᎘")) as fp:
                data = json.load(fp)
                try:
                    bstack1ll11l111l_opy_(bstack1ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪ᎙"), bstack1llll1ll1l_opy_(bstack11l11l1l11_opy_), data, {
                        bstack1ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ᎚"): (self.config[bstack1ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᎛")], self.config[bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᎜")])
                    })
                except Exception as e:
                    logger.debug(bstack1111l11ll_opy_.format(str(e)))
            bstack1l1lll11111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l1llllll11_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1l11llll1_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
        self.bstack1l1llllllll_opy_, self.bstack1lll1l111ll_opy_ = bstack1ll111l1111_opy_(data.bs_config)
        os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧ᎝")] = self.bstack1lll1l111ll_opy_
        if not self.bstack1l1llllllll_opy_ or not self.bstack1lll1l111ll_opy_:
            raise ValueError(bstack1ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤ᎞"))
        if self.bstack1ll1111lll_opy_():
            self.__1l1l1l111ll_opy_(event_name, bstack11lll11ll_opy_())
            return
        try:
            logger.debug(bstack1ll11_opy_ (u"ࠦࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡓࡅࡍࠣࡗࡪࡺࡵࡱ࠰ࠥ᎟"))
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤᎠ").format(e))
        start = datetime.now()
        is_started = self.__1l1l1l1l11l_opy_()
        self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠨࡳࡱࡣࡺࡲࡤࡺࡩ࡮ࡧࠥᎡ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l1ll1l1l1l_opy_()
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨᎢ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1lllll1ll_opy_(data)
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᎣ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1lll1111l_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1l1l111ll_opy_(self, event_name: str, data: bstack11lll11ll_opy_):
        if not self.bstack1ll1111lll_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᎤ"))
            return
        bin_session_id = os.environ.get(bstack1l1l1ll1lll_opy_)
        start = datetime.now()
        self.__1l1ll1l1l1l_opy_()
        self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤᎥ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1ll11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊࠢࠥᎦ") + str(bin_session_id) + bstack1ll11_opy_ (u"ࠧࠨᎧ"))
        start = datetime.now()
        self.__1l1l1lllll1_opy_()
        self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᎨ"), datetime.now() - start)
    def __1l1ll1ll1l1_opy_(self):
        if not self.bstack1l1ll1ll111_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦᎩ"))
            return
        bstack1l1l1llll1l_opy_ = {
            bstack1ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᎪ"): (bstack1l1llllll1l_opy_, bstack1l1llll11l1_opy_, bstack1l111lllll_opy_),
            bstack1ll11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᎫ"): (bstack1l1lllll11l_opy_, bstack1l1l1l11ll1_opy_, bstack1ll11111111_opy_),
        }
        if not self.bstack1l1l11ll1l1_opy_ and self.session_framework in bstack1l1l1llll1l_opy_:
            bstack1l1ll1l11l1_opy_, bstack1l1l1lll111_opy_, bstack1l1l1ll11l1_opy_ = bstack1l1l1llll1l_opy_[self.session_framework]
            bstack1ll1111111l_opy_ = bstack1l1l1lll111_opy_()
            self.bstack1l1l1l1ll11_opy_ = bstack1ll1111111l_opy_
            self.bstack1l1l11ll1l1_opy_ = bstack1l1l1ll11l1_opy_
            self.bstack1l1lll111l1_opy_.append(bstack1ll1111111l_opy_)
            self.bstack1l1lll111l1_opy_.append(bstack1l1ll1l11l1_opy_(self.bstack1l1l1l1ll11_opy_))
        if not self.bstack1l1ll1lllll_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1l1ll1lllll_opy_ = bstack1l11l111l_opy_(self.bstack1l1l11ll1l1_opy_, self.bstack1l1l1l1ll11_opy_)
            self.bstack1l1lll111l1_opy_.append(self.bstack1l1ll1lllll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1ll1111l_opy_(self.bstack1l1l11ll1l1_opy_, self.bstack1l1l1l1ll11_opy_)
            self.bstack1l1lll111l1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1ll11_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧᎬ"), False) == True:
            self.ai = bstack1l1l1lll1ll_opy_()
            self.bstack1l1lll111l1_opy_.append(self.ai)
        if not self.percy and self.bstack1l1lll11l11_opy_ and self.bstack1l1lll11l11_opy_.success:
            self.percy = bstack1l1l11ll1ll_opy_(self.bstack1l1lll11l11_opy_)
            self.bstack1l1lll111l1_opy_.append(self.percy)
        for mod in self.bstack1l1lll111l1_opy_:
            if not mod.bstack1l1l1l11lll_opy_():
                mod.configure(self.bstack1l1ll1ll111_opy_, self.config, self.cli_bin_session_id, self.bstack1ll11llll11_opy_)
    def __1l1ll1111l1_opy_(self):
        for mod in self.bstack1l1lll111l1_opy_:
            if mod.bstack1l1l1l11lll_opy_():
                mod.configure(self.bstack1l1ll1ll111_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l1ll1l1111_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1lllll1ll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l1llll1l11_opy_:
            return
        self.__1l1lllllll1_opy_(data)
        bstack11l111ll1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1ll11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦᎭ")
        req.sdk_language = bstack1ll11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧᎮ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l1ll11llll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꭿ"), bstack1ll11_opy_ (u"ࠧ࠱ࠩᎰ")))
            req.client_worker_id = bstack1ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᎱ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡪࡤࡪࡰࡪࠤࡼࡵࡲ࡬ࡧࡵࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹ࠼ࠣࡿࢂࠨᎲ").format(e))
        try:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥ࡟ࠧᎳ") + str(id(self)) + bstack1ll11_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᎴ"))
            r = self.bstack1l1ll1ll111_opy_.StartBinSession(req)
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᎵ"), datetime.now() - bstack11l111ll1_opy_)
            os.environ[bstack1l1l1ll1lll_opy_] = r.bin_session_id
            self.__1l1ll1l1ll1_opy_(r)
            self.__1l1ll1ll1l1_opy_()
            if not self.bstack1l1ll111lll_opy_:
                self.bstack1ll11llll11_opy_.start()
                self.bstack1l1ll111lll_opy_ = True
                atexit.register(self.__1l1lllll111_opy_)
            self.bstack1l1llll1l11_opy_ = True
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡛ࠣᎶ") + str(id(self)) + bstack1ll11_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧᎷ"))
        except grpc.bstack1l1l1l1ll1l_opy_ as bstack1l1l1ll1ll1_opy_:
            self.logger.error(bstack1ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᎸ") + str(bstack1l1l1ll1ll1_opy_) + bstack1ll11_opy_ (u"ࠤࠥᎹ"))
            traceback.print_exc()
            raise bstack1l1l1ll1ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎺ") + str(e) + bstack1ll11_opy_ (u"ࠦࠧᎻ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1111l_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1l1lllll1_opy_(self):
        if not self.bstack1ll1111lll_opy_() or not self.cli_bin_session_id or self.bstack1ll111l11l1_opy_:
            return
        bstack11l111ll1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᎼ"), bstack1ll11_opy_ (u"࠭࠰ࠨᎽ")))
        req.client_worker_id = bstack1ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᎾ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣ࡝ࠥᎿ") + str(id(self)) + bstack1ll11_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᏀ"))
            r = self.bstack1l1ll1ll111_opy_.ConnectBinSession(req)
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᏁ"), datetime.now() - bstack11l111ll1_opy_)
            self.__1l1ll1l1ll1_opy_(r)
            self.__1l1ll1ll1l1_opy_()
            if not self.bstack1l1ll111lll_opy_:
                self.bstack1ll11llll11_opy_.start()
                self.bstack1l1ll111lll_opy_ = True
                atexit.register(self.__1l1lllll111_opy_)
            self.bstack1ll111l11l1_opy_ = True
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡠࠨᏂ") + str(id(self)) + bstack1ll11_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦᏃ"))
        except grpc.bstack1l1l1l1ll1l_opy_ as bstack1l1l1ll1ll1_opy_:
            self.logger.error(bstack1ll11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᏄ") + str(bstack1l1l1ll1ll1_opy_) + bstack1ll11_opy_ (u"ࠢࠣᏅ"))
            traceback.print_exc()
            raise bstack1l1l1ll1ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᏆ") + str(e) + bstack1ll11_opy_ (u"ࠤࠥᏇ"))
            traceback.print_exc()
            raise e
    def __1l1ll1l1ll1_opy_(self, r):
        self.bstack1l1ll11l111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1ll11_opy_ (u"ࠥࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤᏈ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1ll11_opy_ (u"ࠦࡪࡳࡰࡵࡻࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡻ࡮ࡥࠤᏉ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡩࡷࡩࡹࠡ࡫ࡶࠤࡸ࡫࡮ࡵࠢࡲࡲࡱࡿࠠࡢࡵࠣࡴࡦࡸࡴࠡࡱࡩࠤࡹ࡮ࡥࠡࠤࡆࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠲ࠢࠡࡣࡱࡨࠥࡺࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡣ࡯ࡷࡴࠦࡵࡴࡧࡧࠤࡧࡿࠠࡔࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࡳࡧࡩࡳࡷ࡫ࠬࠡࡐࡲࡲࡪࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡ࡫ࡶࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᏊ")
        self.bstack1l1lll11l11_opy_ = getattr(r, bstack1ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᏋ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᏌ")] = self.config_testhub.jwt
        os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ꮝ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1ll11ll1l_opy_ = json.loads(r.config)
            bstack1l1l1ll111l_opy_ = bstack1l1ll11ll1l_opy_.get(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭Ꮞ"), {}).get(bstack1ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᏏ"), bstack1ll11_opy_ (u"ࠫࠬᏐ"))
            os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᏑ")] = bstack1l1l1ll111l_opy_
    def bstack1l1ll1llll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll111l1l1l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1l1l1llll_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1l1l1llll_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l1ll1llll1_opy_(event_name=EVENTS.bstack1l1l1ll1l11_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1l1l1l11l_opy_(self, bstack1l1lll1l1ll_opy_=10):
        if self.bstack1ll111l1l1l_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣᏒ"))
            return True
        self.logger.debug(bstack1ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᏓ"))
        if os.getenv(bstack1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣᏔ")) == bstack1ll111l1l11_opy_:
            self.cli_bin_session_id = bstack1ll111l1l11_opy_
            self.cli_listen_addr = bstack1ll11_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧᏕ") % (self.cli_bin_session_id)
            self.bstack1ll111l1l1l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1llllllll_opy_, bstack1ll11_opy_ (u"ࠥࡷࡩࡱࠢᏖ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l1ll11l11l_opy_ compat for text=True in bstack1ll1111l11l_opy_ python
            encoding=bstack1ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏗ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1l1l11l11_opy_ = threading.Thread(target=self.__1l1l1l1l111_opy_, args=(bstack1l1lll1l1ll_opy_,))
        bstack1l1l1l11l11_opy_.start()
        bstack1l1l1l11l11_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤᏘ") + str(self.process.stderr.read()) + bstack1ll11_opy_ (u"ࠨࠢᏙ"))
        if not self.bstack1ll111l1l1l_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢ࡜ࠤᏚ") + str(id(self)) + bstack1ll11_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦᏛ"))
            self.__1l1l1ll1111_opy_()
        self.logger.debug(bstack1ll11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥᏜ") + str(self.bstack1ll111l1l1l_opy_) + bstack1ll11_opy_ (u"ࠥࠦᏝ"))
        return self.bstack1ll111l1l1l_opy_
    def __1l1l1l1l111_opy_(self, bstack1l1ll11l1l1_opy_=10):
        bstack1l1l1llll11_opy_ = time.time()
        while self.process and time.time() - bstack1l1l1llll11_opy_ < bstack1l1ll11l1l1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1ll11_opy_ (u"ࠦ࡮ࡪ࠽ࠣᏞ") in line:
                    self.cli_bin_session_id = line.split(bstack1ll11_opy_ (u"ࠧ࡯ࡤ࠾ࠤᏟ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll11_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧᏠ") + str(self.cli_bin_session_id) + bstack1ll11_opy_ (u"ࠢࠣᏡ"))
                    continue
                if bstack1ll11_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᏢ") in line:
                    self.cli_listen_addr = line.split(bstack1ll11_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᏣ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll11_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨᏤ") + str(self.cli_listen_addr) + bstack1ll11_opy_ (u"ࠦࠧᏥ"))
                    continue
                if bstack1ll11_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᏦ") in line:
                    port = line.split(bstack1ll11_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᏧ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll11_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨᏨ") + str(port) + bstack1ll11_opy_ (u"ࠣࠤᏩ"))
                    continue
                if line.strip() == bstack1l1lll11lll_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1ll11_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦᏪ"), bstack1ll11_opy_ (u"ࠥ࠵ࠧᏫ")) == bstack1ll11_opy_ (u"ࠦ࠶ࠨᏬ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll111l1l1l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1ll11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨᏭ") + str(e) + bstack1ll11_opy_ (u"ࠨࠢᏮ"))
        return False
    def __1l1lllll111_opy_(self):
        bstack1ll11_opy_ (u"ࠢࠣࠤࡆࡰࡪࡧ࡮ࡶࡲࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡫ࡵࡲࠡࡣࡶࡽࡳࡩ࡟ࡥ࡫ࡶࡴࡦࡺࡣࡩࡧࡵ࠰ࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡣࡷࡩࡽ࡯ࡴࠡࡶࡲࠤࡪࡴࡳࡶࡴࡨࠤࡹࡧࡳ࡬ࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨࠢࠣᏯ")
        if self.bstack1ll11llll11_opy_ and self.bstack1l1ll111lll_opy_:
            try:
                self.bstack1ll11llll11_opy_.stop()
                self.bstack1l1ll111lll_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1ll111l11_opy_, stage=STAGE.bstack11111llll_opy_)
    def __1l1l1ll1111_opy_(self):
        if self.bstack1l1l11lll11_opy_:
            if self.bstack1ll11llll11_opy_ and self.bstack1l1ll111lll_opy_:
                try:
                    atexit.unregister(self.__1l1lllll111_opy_)
                except ValueError:
                    pass
                self.bstack1ll11llll11_opy_.stop()
                self.bstack1l1ll111lll_opy_ = False
            start = datetime.now()
            if self.bstack1l1ll1111ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll111l11l1_opy_:
                    self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᏰ"), datetime.now() - start)
                else:
                    self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᏱ"), datetime.now() - start)
            self.__1l1ll1111l1_opy_()
            start = datetime.now()
            bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(bstack1ll11_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࠣᏲ"))
            self.bstack1l1l11lll11_opy_.close()
            bstack11ll11l1ll_opy_.end(bstack1ll11_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࠤᏳ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏴ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏵ"), True, None, None, None, None)
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠢࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤ᏶"), datetime.now() - start)
            self.bstack1l1l11lll11_opy_ = None
        if self.process:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡵࡷࡳࡵࠨ᏷"))
            start = datetime.now()
            bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(bstack1ll11_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽࡯࡮ࡲ࡬ࠣᏸ"))
            self.process.terminate()
            bstack11ll11l1ll_opy_.end(bstack1ll11_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡰ࡯࡬࡭ࠤᏹ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᏺ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᏻ"), True, None, None, None, None)
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠨ࡫ࡪ࡮࡯ࡣࡹ࡯࡭ࡦࠤᏼ"), datetime.now() - start)
            self.process = None
            if self.bstack1l1l11lll1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1lllll1ll_opy_()
                self.logger.info(
                    bstack1ll11_opy_ (u"ࠢࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠢᏽ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1ll11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᏾")] = self.config_testhub.build_hashed_id
        self.bstack1ll111l1l1l_opy_ = False
    def __1l1lllllll1_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ᏿"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l1l1l11l1l_opy_ = get_pw_version()
            except:
                bstack1l1l1l11l1l_opy_ = _1l1llll1l1l_opy_()
            data.framework_versions[bstack1ll11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ᐀")] = bstack1l1l1l11l1l_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack1ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᐁ")] = selenium.__version__
                data.frameworks.append(bstack1ll11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᐂ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᐃ")] = __version__
                data.frameworks.append(bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᐄ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡐࡲࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦ࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧࠦᐅ"))
    def bstack1l1lll111ll_opy_(self, hub_url: str, platform_index: int, bstack1l1l11ll_opy_: Any):
        if self.bstack1l11111ll_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨᐆ"))
            return
        try:
            bstack11l111ll1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1ll11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᐇ")
            self.bstack1l11111ll_opy_ = bstack1ll11111111_opy_(
                cli.config.get(bstack1ll11_opy_ (u"ࠦ࡭ࡻࡢࡖࡴ࡯ࠦᐈ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1l1lll11l_opy_={bstack1ll11_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤᐉ"): bstack1l1l11ll_opy_}
            )
            def bstack1l1l1l1l1ll_opy_(self):
                return
            if self.config.get(bstack1ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠣᐊ"), True):
                Service.start = bstack1l1l1l1l1ll_opy_
                Service.stop = bstack1l1l1l1l1ll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1lll1l1ll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1ll1l11ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᐋ"), datetime.now() - bstack11l111ll1_opy_)
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࠢᐌ") + str(e) + bstack1ll11_opy_ (u"ࠤࠥᐍ"))
    def bstack11lll1111_opy_(self, platform_index: int):
        if self.bstack1l11111ll_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᐎ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l1l1ll11ll_opy_
                self.bstack1l11111ll_opy_ = bstack1l111lllll_opy_(
                    platform_index,
                    framework_name=bstack1ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᐏ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l1llll1l1l_opy_
                from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11ll11ll_opy_
                bstack1l1l1l11l1l_opy_ = get_pw_version()
                self.bstack1l11111ll_opy_ = bstack1l111lllll_opy_(
                    platform_index,
                    framework_name=bstack1ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᐐ"),
                    framework_version=bstack1l1l1l11l1l_opy_.version,
                    classes=[],
                )
                ctx = bstack1ll11ll11ll_opy_.create_context(self.bstack1l11111ll_opy_)
                bstack111l1ll111_opy_.bstack1l1l111l_opy_[ctx.id] = bstack1ll111lllll_opy_(
                    ctx, bstack1ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᐑ"), bstack1l1l1l11l1l_opy_, bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_
                )
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣᐒ") + str(e) + bstack1ll11_opy_ (u"ࠣࠤᐓ"))
            pass
    def bstack111111lll1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᐔ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1l1lll1l1l1_opy_({ bstack1ll11_opy_ (u"ࠥࡶࡴࡨ࡯ࡵ࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᐕ"): VERSION }, [bstack1ll11_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥᐖ")], self.bstack1ll11llll11_opy_, self.bstack1l1ll1ll111_opy_)
                return
            except Exception as e:
                self.logger.error(bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡳࡱࡥࡳࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࠦᐗ") + str(e) + bstack1ll11_opy_ (u"ࠨࠢᐘ"))
        if bstack1111l1111l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᐙ"): pytest.__version__ }, [bstack1ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᐚ")], self.bstack1ll11llll11_opy_, self.bstack1l1ll1ll111_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1lllll1l1_opy_({ bstack1ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᐛ"): pytest.__version__ }, [bstack1ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᐜ")], self.bstack1ll11llll11_opy_, self.bstack1l1ll1ll111_opy_)
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࠣᐝ") + str(e) + bstack1ll11_opy_ (u"ࠧࠨᐞ"))
        self.bstack1l1lll11l1l_opy_()
    def bstack1l1lll11l1l_opy_(self):
        if not self.bstack1ll11l1l11_opy_():
            return
        bstack111l1ll1l1_opy_ = None
        def bstack11l1l11ll_opy_(config, startdir):
            return bstack1ll11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦᐟ").format(bstack1ll11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᐠ"))
        def bstack1l1ll1111_opy_():
            return
        def bstack11l1l11l11_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1ll11_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᐡ"):
                return bstack1ll11_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᐢ")
            else:
                return bstack111l1ll1l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack111l1ll1l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l1l11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1ll1111_opy_
            Config.getoption = bstack11l1l11l11_opy_
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬ࠥࡶࡹࡵࡧࡶࡸࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠽ࠤࠧᐣ") + str(e) + bstack1ll11_opy_ (u"ࠦࠧᐤ"))
    def bstack1ll1111l1ll_opy_(self):
        bstack1ll1lllll1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll1lllll1_opy_, dict):
            if cli.config_observability:
                bstack1ll1lllll1_opy_.update(
                    {bstack1ll11_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᐥ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᐦ") in accessibility.get(bstack1ll11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᐧ"), {}):
                    bstack1ll1111l1l1_opy_ = accessibility.get(bstack1ll11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᐨ"))
                    bstack1ll1111l1l1_opy_.update({ bstack1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠥᐩ"): bstack1ll1111l1l1_opy_.pop(bstack1ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨᐪ")) })
                bstack1ll1lllll1_opy_.update({bstack1ll11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᐫ"): accessibility })
        return bstack1ll1lllll1_opy_
    @measure(event_name=EVENTS.bstack1l1llll1lll_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l1ll1111ll_opy_(self, bstack1ll1111lll1_opy_: str = None, bstack1l1ll11lll1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1l1ll1ll111_opy_:
            return
        bstack11l111ll1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᐬ"), bstack1ll11_opy_ (u"࠭࠰ࠨᐭ")))
        req.client_worker_id = bstack1ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᐮ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll1111lll1_opy_:
            req.bstack1ll1111lll1_opy_ = bstack1ll1111lll1_opy_
        if bstack1l1ll11lll1_opy_:
            req.bstack1l1ll11lll1_opy_ = bstack1l1ll11lll1_opy_
        try:
            r = self.bstack1l1ll1ll111_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᐯ"), datetime.now() - bstack11l111ll1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1111111ll1_opy_(self, key: str, value: timedelta):
        tag = bstack1ll11_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᐰ") if self.bstack1ll1111lll_opy_() else bstack1ll11_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᐱ")
        self.bstack1l1l1ll1l1l_opy_[bstack1ll11_opy_ (u"ࠦ࠿ࠨᐲ").join([tag + bstack1ll11_opy_ (u"ࠧ࠳ࠢᐳ") + str(id(self)), key])] += value
    def bstack1lllll1ll_opy_(self):
        if not os.getenv(bstack1ll11_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥᐴ"), bstack1ll11_opy_ (u"ࠢ࠱ࠤᐵ")) == bstack1ll11_opy_ (u"ࠣ࠳ࠥᐶ"):
            return
        bstack1l1ll1ll11l_opy_ = dict()
        bstack1l1l111l_opy_ = []
        if self.test_framework:
            bstack1l1l111l_opy_.extend(list(self.test_framework.bstack1l1l111l_opy_.values()))
        if self.bstack1l11111ll_opy_:
            bstack1l1l111l_opy_.extend(list(self.bstack1l11111ll_opy_.bstack1l1l111l_opy_.values()))
        for instance in bstack1l1l111l_opy_:
            if not instance.platform_index in bstack1l1ll1ll11l_opy_:
                bstack1l1ll1ll11l_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l1ll1ll11l_opy_[instance.platform_index]
            for k, v in instance.bstack1l1lll1llll_opy_().items():
                report[k] += v
                report[k.split(bstack1ll11_opy_ (u"ࠤ࠽ࠦᐷ"))[0]] += v
        bstack1l1lll1lll1_opy_ = sorted([(k, v) for k, v in self.bstack1l1l1ll1l1l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1ll1ll1ll_opy_ = 0
        for r in bstack1l1lll1lll1_opy_:
            bstack1ll11111l11_opy_ = r[1].total_seconds()
            bstack1l1ll1ll1ll_opy_ += bstack1ll11111l11_opy_
            self.logger.debug(bstack1ll11_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣᐸ") + str(bstack1ll11111l11_opy_) + bstack1ll11_opy_ (u"ࠦࠧᐹ"))
        self.logger.debug(bstack1ll11_opy_ (u"ࠧ࠳࠭ࠣᐺ"))
        bstack1l1ll11111l_opy_ = []
        for platform_index, report in bstack1l1ll1ll11l_opy_.items():
            bstack1l1ll11111l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l1ll11111l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack111ll1l111_opy_ = set()
        bstack1l1llll111l_opy_ = 0
        for r in bstack1l1ll11111l_opy_:
            bstack1ll11111l11_opy_ = r[2].total_seconds()
            bstack1l1llll111l_opy_ += bstack1ll11111l11_opy_
            bstack111ll1l111_opy_.add(r[0])
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢᐻ") + str(bstack1ll11111l11_opy_) + bstack1ll11_opy_ (u"ࠢࠣᐼ"))
        if self.bstack1ll1111lll_opy_():
            self.logger.debug(bstack1ll11_opy_ (u"ࠣ࠯࠰ࠦᐽ"))
            self.logger.debug(bstack1ll11_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤᐾ") + str(bstack1l1llll111l_opy_) + bstack1ll11_opy_ (u"ࠥࠦᐿ"))
        else:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᑀ") + str(bstack1l1ll1ll1ll_opy_) + bstack1ll11_opy_ (u"ࠧࠨᑁ"))
        self.logger.debug(bstack1ll11_opy_ (u"ࠨ࠭࠮ࠤᑂ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᑃ"), bstack1ll11_opy_ (u"ࠨ࠲ࠪᑄ"))),
            client_worker_id=bstack1ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᑅ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1l1ll1ll111_opy_:
            self.logger.error(bstack1ll11_opy_ (u"ࠥࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡄࡣࡱࡲࡴࡺࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᑆ"))
            return None
        response = self.bstack1l1ll1ll111_opy_.TestOrchestration(request)
        self.logger.debug(bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵ࠯ࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠯ࡶࡩࡸࡹࡩࡰࡰࡀࡿࢂࠨᑇ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l1ll11l111_opy_(self, r):
        if r is not None and getattr(r, bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭ᑈ"), None) and getattr(r.testhub, bstack1ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᑉ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1ll11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᑊ")))
            for bstack1l1ll1lll11_opy_, err in errors.items():
                if err[bstack1ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᑋ")] == bstack1ll11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᑌ"):
                    self.logger.info(err[bstack1ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᑍ")])
                else:
                    self.logger.error(err[bstack1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑎ")])
    def bstack1ll111l111_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()