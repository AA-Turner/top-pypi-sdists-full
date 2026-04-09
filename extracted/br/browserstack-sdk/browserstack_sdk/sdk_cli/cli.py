# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
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
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.bstack1l1lllll1ll_opy_ import bstack1l1llllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1lll11_opy_ import bstack1l1l11l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l11lll11_opy_ import bstack1l1l1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11l11l_opy_ import bstack1l1l1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1l1l111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l11l111l_opy_ import bstack1l1l11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1lll_opy_ import bstack1l11l11llll_opy_
from browserstack_sdk.sdk_cli.bstack11llll1ll_opy_ import bstack1ll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack111ll1l11_opy_ import bstack111ll1l11_opy_, Events, bstack1l1ll1lll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1l11lll1l_opy_ import bstack1l11l1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack1lll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll1_opy_ import bstack1111l11l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11llll1l1_opy_ import bstack1l11l11l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l11l1l1l1l_opy_ import bstack1l1l1lll1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1lll1l_opy_ import bstack1ll111l1l1_opy_
from bstack_utils.helper import Notset, bstack1ll1l11l1ll_opy_, get_cli_dir, bstack1ll1l1l111l_opy_, bstack1lll1l111_opy_, bstack1l11lll11l_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l111ll1l_opy_, TestHookState, bstack1111lll111_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack1l1lll111ll_opy_, bstack11111l1ll_opy_, bstack111llll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11lll11l11_opy_ import bstack1111l11l1_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from bstack_utils.accessibility_scripts import accessibility_scripts
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1lllll_opy_, bstack1111l1lll_opy_
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l111ll1_opy_ import bstack1l1l11l11ll_opy_
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1l1l1ll1111_opy_(bs_config):
    bstack1l11lllll1l_opy_ = None
    bstack1ll1l111lll_opy_ = None
    try:
        bstack1ll1l111lll_opy_ = get_cli_dir()
        bstack1l11lllll1l_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦᑵ"))
        if not bstack1l11lllll1l_opy_:
            bstack1l11lllll1l_opy_ = bstack1ll1l1l111l_opy_(bstack1ll1l111lll_opy_)
            bstack1l11ll1ll11_opy_ = bstack1ll1l11l1ll_opy_(bstack1l11lllll1l_opy_, bstack1ll1l111lll_opy_, bs_config)
            bstack1l11lllll1l_opy_ = bstack1l11ll1ll11_opy_ if bstack1l11ll1ll11_opy_ else bstack1l11lllll1l_opy_
        if not bstack1l11lllll1l_opy_:
            raise ValueError(bstack11ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡇࡑࡏࠠࡱࡣࡷ࡬ࠥ࡯࡮ࠡࡶ࡫ࡩࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡳࡷࠦࡩ࡯ࠢࡷ࡬ࡪࠦ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡦࡰ࡮ࡧࡩࡷࠨᑶ"))
    except Exception as ex:
        logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡹࡵࠦࡃࡍࡋࠣࡴࡦࡺࡨ࠻ࠢࠥᑷ") + str(ex) + bstack11ll11_opy_ (u"ࠦࠧᑸ"))
    return bstack1l11lllll1l_opy_, bstack1ll1l111lll_opy_
bstack1l1l11ll11l_opy_ = bstack11ll11_opy_ (u"ࠧ࠿࠹࠺࠻ࠥᑹ")
bstack1l1l11111l1_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧᑺ")
bstack1l11l1l11ll_opy_ = bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᑻ")
bstack1l11lllllll_opy_ = bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨᑼ")
BROWSERSTACK_AUTOMATION = bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᑽ")
bstack1l11ll1l11l_opy_ = re.compile(bstack11ll11_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤᑾ"))
bstack1l11l11l111_opy_ = bstack11ll11_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤᑿ")
bstack1l11llll1ll_opy_ = bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡕࡒࡄࡇࡢࡊࡆࡒࡌࡃࡃࡆࡏࠧᒀ")
bstack1l11lllll11_opy_ = [
    Events.bstack1l1lll1l_opy_,
    Events.CONNECT,
    Events.bstack1l1l11111_opy_,
]
def _1l11ll11l11_opy_():
    bstack11ll11_opy_ (u"ࠨࠢࠣࡈࡤࡰࡱࡨࡡࡤ࡭ࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࠡ࡮࡬ࡦࡷࡧࡲࡺࠢ࠿ࠤ࠶࠿࠮࠵࠰࠳ࠤࡼ࡮ࡥࡳࡧࠣࡆࡷࡵࡷࡴࡧࡵ࠲ࡪࡴࡴࡳࡻ࠱࡫ࡪࡺ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡴࠢࡧࡳࡪࡹ࡮ࠨࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠥࠦࠧᒁ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1l1l11ll1ll_opy_ = Path(Browser.__file__).parent / bstack11ll11_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡲࠣᒂ") / bstack11ll11_opy_ (u"ࠣࡲࡤࡧࡰࡧࡧࡦ࠰࡭ࡷࡴࡴࠢᒃ")
        bstack1l1l1l1llll_opy_ = json.loads(bstack1l1l11ll1ll_opy_.read_text())
        match = re.search(bstack11ll11_opy_ (u"ࡴࠥࡠࡩ࠱࡜࠯࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭ࠥᒄ"), bstack1l1l1l1llll_opy_[bstack11ll11_opy_ (u"ࠥࡨࡪࡶࡥ࡯ࡦࡨࡲࡨ࡯ࡥࡴࠤᒅ")][bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᒆ")])
        bstack1l1l11l1ll1_opy_ = match.group(0) if match else bstack11ll11_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨᒇ")
    except Exception:
        bstack1l1l11l1ll1_opy_ = bstack11ll11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢᒈ")
    return SimpleNamespace(version=bstack1l1l11l1ll1_opy_)
class SDKCLI:
    _1ll1111ll11_opy_ = None
    process: Union[None, Any]
    bstack1l11l1l1111_opy_: bool
    bstack1l1l1111111_opy_: bool
    bstack1l1l1l1ll11_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l11l1l1lll_opy_: Union[None, grpc.Channel]
    bstack1l1l1ll1l1l_opy_: str
    test_framework: TestFramework
    bstack11l1l1l11_opy_: bstack1lll1111ll_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1111lll1l_opy_: bstack1ll1llll11_opy_
    accessibility: bstack1l1llllll1l_opy_
    bstack1ll1lll1l_opy_: bstack1ll111l1l1_opy_
    ai: bstack1l1l11l1l1l_opy_
    bstack1l1l1ll11l1_opy_: bstack1l1l1lll111_opy_
    bstack1l11llll11l_opy_: List[bstack1l11ll11111_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l11ll1111l_opy_: Any
    bstack1l1l1111lll_opy_: Dict[str, timedelta]
    bstack1l1l1l1lll1_opy_: str
    bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_
    def __new__(cls):
        if not cls._1ll1111ll11_opy_:
            cls._1ll1111ll11_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1111ll11_opy_
    def __init__(self):
        self.process = None
        self.bstack1l11l1l1111_opy_ = False
        self.bstack1l11l1l1lll_opy_ = None
        self.bstack1l1l111l1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l11lllllll_opy_, None)
        self.bstack1l11l1ll1l1_opy_ = os.environ.get(bstack1l11l1l11ll_opy_, bstack11ll11_opy_ (u"ࠢࠣᒉ")) == bstack11ll11_opy_ (u"ࠣࠤᒊ")
        self.bstack1l1l1111111_opy_ = False
        self.bstack1l1l1l1ll11_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l11ll1111l_opy_ = None
        self.test_framework = None
        self.bstack11l1l1l11_opy_ = None
        self.bstack1l1l1ll1l1l_opy_=bstack11ll11_opy_ (u"ࠤࠥᒋ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.get_log_level())
        self.bstack1l1l1111lll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1l1lll11ll1_opy_ = bstack1l1lll1l11l_opy_()
        self.bstack1l1l1lll1ll_opy_ = False
        self.bstack1l11ll1l111_opy_ = None
        self.bstack1l11lll1l11_opy_ = None
        self.bstack1111lll1l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l11llll11l_opy_ = []
    def bstack1llll1l1l_opy_(self):
        return os.environ.get(BROWSERSTACK_AUTOMATION).lower().__eq__(bstack11ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣᒌ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1l11llll1ll_opy_, bstack11ll11_opy_ (u"ࠫࠬᒍ")).lower() in [bstack11ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪᒎ"), bstack11ll11_opy_ (u"࠭࠱ࠨᒏ"), bstack11ll11_opy_ (u"ࠧࡺࡧࡶࠫᒐ")]:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡈࡲࡶࡨ࡯࡮ࡨࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡵࡤࡦࠢࡧࡹࡪࠦࡴࡰࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠤᒑ"))
            os.environ[bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᒒ")] = bstack11ll11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᒓ")
            return False
        if bstack11ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᒔ") in config and str(config[bstack11ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᒕ")]).lower() != bstack11ll11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᒖ"):
            return False
        bstack1l1l111l1ll_opy_ = [bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᒗ"), bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᒘ"), bstack11ll11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠥᒙ")]
        if is_robot_playwright_installed():
            bstack1l1l111l1ll_opy_.append(bstack11ll11_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࠤᒚ"))
            bstack1l1l111l1ll_opy_.append(bstack11ll11_opy_ (u"ࠦࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠧᒛ"))
        bstack1l1l1111ll1_opy_ = config.get(bstack11ll11_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣᒜ")) in bstack1l1l111l1ll_opy_ or os.environ.get(bstack11ll11_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧᒝ")) in bstack1l1l111l1ll_opy_
        os.environ[bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥᒞ")] = str(bstack1l1l1111ll1_opy_) # bstack1l1l1111l1l_opy_ bstack1l1l1l1l111_opy_ VAR to bstack1l1l1l1ll1l_opy_ is binary running
        return bstack1l1l1111ll1_opy_
    def bstack11llllll1_opy_(self):
        for event in bstack1l11lllll11_opy_:
            bstack111ll1l11_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack111ll1l11_opy_.logger.debug(bstack11ll11_opy_ (u"ࠣࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠠ࠾ࡀࠣࡿࡦࡸࡧࡴࡿࠣࠦᒟ") + str(kwargs) + bstack11ll11_opy_ (u"ࠤࠥᒠ"))
            )
        bstack111ll1l11_opy_.register(Events.bstack1l1lll1l_opy_, self.__1l1l1lll11l_opy_)
        bstack111ll1l11_opy_.register(Events.CONNECT, self.__1l1l1l111ll_opy_)
        bstack111ll1l11_opy_.register(Events.bstack1l1l11111_opy_, self.__1l11ll11ll1_opy_)
        bstack111ll1l11_opy_.register(Events.bstack1l1l11111l_opy_, self.__1l1l11llll1_opy_)
    def bstack11lllll1l_opy_(self):
        return not self.bstack1l11l1ll1l1_opy_ and os.environ.get(bstack1l11l1l11ll_opy_, bstack11ll11_opy_ (u"ࠥࠦᒡ")) != bstack11ll11_opy_ (u"ࠦࠧᒢ")
    def is_running(self):
        if self.bstack1l11l1ll1l1_opy_:
            return self.bstack1l11l1l1111_opy_
        else:
            return bool(self.bstack1l11l1l1lll_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack11ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᒣ"))
                and self.config_observability.options.allow_screenshots == bstack11ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫᒤ")
            )
        except Exception:
            return False
    def bstack111l1l1ll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l11llll11l_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l11l1111ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l11l1l111l_opy_(self, bstack1l1l1111l11_opy_=10):
        if self.bstack1l1l111l1_opy_:
            return
        bstack1l111ll1ll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l11lllllll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11ll11_opy_ (u"ࠢ࡜ࠤᒥ") + str(id(self)) + bstack11ll11_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢᒦ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦᒧ"), 0), (bstack11ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨᒨ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1l1111l11_opy_)
        self.bstack1l11l1l1lll_opy_ = channel
        self.bstack1l1l111l1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l11l1l1lll_opy_)
        self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥᒩ"), datetime.now() - bstack1l111ll1ll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l11lllllll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧᒪ") + str(self.bstack11lllll1l_opy_()) + bstack11ll11_opy_ (u"ࠨࠢᒫ"))
    def __1l11ll11ll1_opy_(self, event_name):
        if self.bstack11lllll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢᒬ"))
        self.__1l1l111111l_opy_()
    @measure(event_name=EVENTS.bstack1l11ll1l1ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l1l11llll1_opy_(self, event_name, bstack1l1l1ll1l11_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣᒭ"))
        bstack1l1l1l1l1l1_opy_ = Path(bstack1l1ll1lll11_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥᒮ"))
        if self.bstack1ll1l111lll_opy_ and bstack1l1l1l1l1l1_opy_.exists():
            with open(bstack1l1l1l1l1l1_opy_, bstack11ll11_opy_ (u"ࠪࡶࠬᒯ"), encoding=bstack11ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᒰ")) as fp:
                data = json.load(fp)
                try:
                    bstack1l11lll11l_opy_(bstack11ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪᒱ"), bstack1111l11l1_opy_(bstack1l11l11lll_opy_), data, {
                        bstack11ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᒲ"): (self.config[bstack11ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᒳ")], self.config[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᒴ")])
                    })
                except Exception as e:
                    logger.debug(bstack1111l1lll_opy_.format(str(e)))
            bstack1l1l1l1l1l1_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l11l1ll111_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l1l1lll11l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
        self.bstack1l1l1ll1l1l_opy_, self.bstack1ll1l111lll_opy_ = bstack1l1l1ll1111_opy_(data.bs_config)
        os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧᒵ")] = self.bstack1ll1l111lll_opy_
        if not self.bstack1l1l1ll1l1l_opy_ or not self.bstack1ll1l111lll_opy_:
            raise ValueError(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤᒶ"))
        if self.bstack11lllll1l_opy_():
            self.__1l1l1l111ll_opy_(event_name, bstack1l1ll1lll_opy_())
            return
        try:
            logger.debug(bstack11ll11_opy_ (u"ࠦࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡓࡅࡍࠣࡗࡪࡺࡵࡱ࠰ࠥᒷ"))
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤᒸ").format(e))
        start = datetime.now()
        is_started = self.__1l11lll111l_opy_()
        self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠨࡳࡱࡣࡺࡲࡤࡺࡩ࡮ࡧࠥᒹ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l11l1l111l_opy_()
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨᒺ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1l111l1l1_opy_(data)
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᒻ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l11l1ll1ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l1l1l111ll_opy_(self, event_name: str, data: bstack1l1ll1lll_opy_):
        if not self.bstack11lllll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᒼ"))
            return
        bin_session_id = os.environ.get(bstack1l11l1l11ll_opy_)
        start = datetime.now()
        self.__1l11l1l111l_opy_()
        self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤᒽ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊࠢࠥᒾ") + str(bin_session_id) + bstack11ll11_opy_ (u"ࠧࠨᒿ"))
        start = datetime.now()
        self.__1l1l1l1111l_opy_()
        self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᓀ"), datetime.now() - start)
    def __1l11l11111l_opy_(self):
        if not self.bstack1l1l111l1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦᓁ"))
            return
        bstack1l11lll11ll_opy_ = {
            bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᓂ"): (bstack1l1l11ll111_opy_, bstack1l11l11llll_opy_, bstack1111l11l1l_opy_),
            bstack11ll11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᓃ"): (bstack1l1l1l11ll1_opy_, bstack1l1l111ll11_opy_, bstack1l1l1ll11ll_opy_),
        }
        if not self.bstack1l11ll1l111_opy_ and self.session_framework in bstack1l11lll11ll_opy_:
            bstack1l11lll1ll1_opy_, bstack1l11llllll1_opy_, bstack1l11ll11l1l_opy_ = bstack1l11lll11ll_opy_[self.session_framework]
            bstack1l11l111lll_opy_ = bstack1l11llllll1_opy_()
            self.bstack1l11lll1l11_opy_ = bstack1l11l111lll_opy_
            self.bstack1l11ll1l111_opy_ = bstack1l11ll11l1l_opy_
            self.bstack1l11llll11l_opy_.append(bstack1l11l111lll_opy_)
            self.bstack1l11llll11l_opy_.append(bstack1l11lll1ll1_opy_(self.bstack1l11lll1l11_opy_))
        if not self.bstack1111lll1l_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1111lll1l_opy_ = bstack1ll1llll11_opy_(self.bstack1l11ll1l111_opy_, self.bstack1l11lll1l11_opy_)
            self.bstack1l11llll11l_opy_.append(self.bstack1111lll1l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l1llllll1l_opy_(self.bstack1l11ll1l111_opy_, self.bstack1l11lll1l11_opy_)
            self.bstack1l11llll11l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11ll11_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧᓄ"), False) == True:
            self.ai = bstack1l1l11l1l1l_opy_()
            self.bstack1l11llll11l_opy_.append(self.ai)
        if not self.percy and self.bstack1l11ll1111l_opy_ and self.bstack1l11ll1111l_opy_.success:
            self.percy = bstack1l1l1lll111_opy_(self.bstack1l11ll1111l_opy_)
            self.bstack1l11llll11l_opy_.append(self.percy)
        for mod in self.bstack1l11llll11l_opy_:
            if not mod.bstack1l1l1llll11_opy_():
                mod.configure(self.bstack1l1l111l1_opy_, self.config, self.cli_bin_session_id, self.bstack1l1lll11ll1_opy_)
    def __1l11l111l1l_opy_(self):
        for mod in self.bstack1l11llll11l_opy_:
            if mod.bstack1l1l1llll11_opy_():
                mod.configure(self.bstack1l1l111l1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l1l1l11l11_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l1l111l1l1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l1l1111111_opy_:
            return
        self.__1l11lll1111_opy_(data)
        bstack1l111ll1ll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦᓅ")
        req.sdk_language = bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧᓆ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l11ll1l11l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᓇ"), bstack11ll11_opy_ (u"ࠧ࠱ࠩᓈ")))
            req.client_worker_id = bstack11ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᓉ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡪࡤࡪࡰࡪࠤࡼࡵࡲ࡬ࡧࡵࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹ࠼ࠣࡿࢂࠨᓊ").format(e))
        try:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡟ࠧᓋ") + str(id(self)) + bstack11ll11_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᓌ"))
            r = self.bstack1l1l111l1_opy_.StartBinSession(req)
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᓍ"), datetime.now() - bstack1l111ll1ll_opy_)
            os.environ[bstack1l11l1l11ll_opy_] = r.bin_session_id
            self.__1l11l1l1l11_opy_(r)
            self.__1l11l11111l_opy_()
            if not self.bstack1l1l1lll1ll_opy_:
                self.bstack1l1lll11ll1_opy_.start()
                self.bstack1l1l1lll1ll_opy_ = True
                atexit.register(self.__1l1l11l1lll_opy_)
            self.bstack1l1l1111111_opy_ = True
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡛ࠣᓎ") + str(id(self)) + bstack11ll11_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧᓏ"))
        except grpc.bstack1l11ll1llll_opy_ as bstack1l11l1l1ll1_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᓐ") + str(bstack1l11l1l1ll1_opy_) + bstack11ll11_opy_ (u"ࠤࠥᓑ"))
            traceback.print_exc()
            raise bstack1l11l1l1ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᓒ") + str(e) + bstack11ll11_opy_ (u"ࠦࠧᓓ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11111ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l1l1l1111l_opy_(self):
        if not self.bstack11lllll1l_opy_() or not self.cli_bin_session_id or self.bstack1l1l1l1ll11_opy_:
            return
        bstack1l111ll1ll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᓔ"), bstack11ll11_opy_ (u"࠭࠰ࠨᓕ")))
        req.client_worker_id = bstack11ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᓖ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡝ࠥᓗ") + str(id(self)) + bstack11ll11_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᓘ"))
            r = self.bstack1l1l111l1_opy_.ConnectBinSession(req)
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᓙ"), datetime.now() - bstack1l111ll1ll_opy_)
            self.__1l11l1l1l11_opy_(r)
            self.__1l11l11111l_opy_()
            if not self.bstack1l1l1lll1ll_opy_:
                self.bstack1l1lll11ll1_opy_.start()
                self.bstack1l1l1lll1ll_opy_ = True
                atexit.register(self.__1l1l11l1lll_opy_)
            self.bstack1l1l1l1ll11_opy_ = True
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࠨᓚ") + str(id(self)) + bstack11ll11_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦᓛ"))
        except grpc.bstack1l11ll1llll_opy_ as bstack1l11l1l1ll1_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᓜ") + str(bstack1l11l1l1ll1_opy_) + bstack11ll11_opy_ (u"ࠢࠣᓝ"))
            traceback.print_exc()
            raise bstack1l11l1l1ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᓞ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᓟ"))
            traceback.print_exc()
            raise e
    def __1l11l1l1l11_opy_(self, r):
        self.bstack1l1l11ll1l1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11ll11_opy_ (u"ࠥࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤᓠ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11ll11_opy_ (u"ࠦࡪࡳࡰࡵࡻࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡻ࡮ࡥࠤᓡ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡩࡷࡩࡹࠡ࡫ࡶࠤࡸ࡫࡮ࡵࠢࡲࡲࡱࡿࠠࡢࡵࠣࡴࡦࡸࡴࠡࡱࡩࠤࡹ࡮ࡥࠡࠤࡆࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠲ࠢࠡࡣࡱࡨࠥࡺࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡣ࡯ࡷࡴࠦࡵࡴࡧࡧࠤࡧࡿࠠࡔࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࡳࡧࡩࡳࡷ࡫ࠬࠡࡐࡲࡲࡪࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡ࡫ࡶࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᓢ")
        self.bstack1l11ll1111l_opy_ = getattr(r, bstack11ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᓣ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᓤ")] = self.config_testhub.jwt
        os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᓥ")] = self.config_testhub.build_hashed_id
        if self.config.get(bstack11ll11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᓦ")) == bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦᓧ"):
            if self.config_accessibility and self.config_accessibility.success:
                try:
                    options = self.config_accessibility.options
                    if options:
                        bstack1l11ll1ll1l_opy_ = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᓨ"), bstack11ll11_opy_ (u"ࠬࢁࡽࠨᓩ")))
                        if options.capabilities:
                            for bstack11l1l1l111_opy_ in options.capabilities:
                                if bstack11l1l1l111_opy_.name == bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᓪ"):
                                    os.environ[bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᓫ")] = bstack11l1l1l111_opy_.value
                                    self.logger.debug(bstack11ll11_opy_ (u"ࠣࡕࡨࡸࠥࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠣࡪࡷࡵ࡭ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࠣᓬ"))
                                elif bstack11l1l1l111_opy_.name == bstack11ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᓭ"):
                                    bstack1l11ll1ll1l_opy_[bstack11ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᓮ")] = bstack11l1l1l111_opy_.value
                                    self.logger.debug(bstack11ll11_opy_ (u"ࠦࡘ࡫ࡴࠡࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨᓯ").format(bstack11l1l1l111_opy_.value))
                        os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᓰ")] = json.dumps(bstack1l11ll1ll1l_opy_)
                        if options.scripts:
                            scripts = {script.name: script.command for script in options.scripts}
                            accessibility_scripts.bstack1ll1ll1l1_opy_(scripts)
                            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡕࡱࡦࡤࡸࡪࡪࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࡾࢁࠧᓱ").format(list(scripts.keys())))
                        if options.commands_to_wrap and options.commands_to_wrap.commands:
                            commands = [{bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓲ"): cmd.name} for cmd in options.commands_to_wrap.commands]
                            accessibility_scripts.bstack1l1l111l11l_opy_(commands)
                            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡗࡳࡨࡦࡺࡥࡥࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᓳ").format(len(commands)))
                        accessibility_scripts.store()
                except Exception as e:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡿࢂࠨᓴ").format(e))
        if is_robot_playwright_installed():
            bstack1l11ll1l1l1_opy_ = json.loads(r.config)
            bstack1l11llll111_opy_ = bstack1l11ll1l1l1_opy_.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᓵ"), {}).get(bstack11ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᓶ"), bstack11ll11_opy_ (u"ࠬ࠭ᓷ"))
            os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᓸ")] = bstack1l11llll111_opy_
    def bstack1l1l1ll1ll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l11l1l1111_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1l1l111l1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1l1l111l1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l1l1ll1ll1_opy_(event_name=EVENTS.bstack1l11ll11lll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l11lll111l_opy_(self, bstack1l1l1111l11_opy_=10):
        if self.bstack1l11l1l1111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤᓹ"))
            return True
        self.logger.debug(bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢᓺ"))
        if os.getenv(bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤᓻ")) == bstack1l11l11l111_opy_:
            self.cli_bin_session_id = bstack1l11l11l111_opy_
            self.cli_listen_addr = bstack11ll11_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨᓼ") % (self.cli_bin_session_id)
            self.bstack1l11l1l1111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1l1ll1l1l_opy_, bstack11ll11_opy_ (u"ࠦࡸࡪ࡫ࠣᓽ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l11l11ll1l_opy_ compat for text=True in bstack1l1l111lll1_opy_ python
            encoding=bstack11ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᓾ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1l11lllll_opy_ = threading.Thread(target=self.__1l11lll11l1_opy_, args=(bstack1l1l1111l11_opy_,))
        bstack1l1l11lllll_opy_.start()
        bstack1l1l11lllll_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥᓿ") + str(self.process.stderr.read()) + bstack11ll11_opy_ (u"ࠢࠣᔀ"))
        if not self.bstack1l11l1l1111_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡝ࠥᔁ") + str(id(self)) + bstack11ll11_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧᔂ"))
            self.__1l1l111111l_opy_()
        self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦᔃ") + str(self.bstack1l11l1l1111_opy_) + bstack11ll11_opy_ (u"ࠦࠧᔄ"))
        return self.bstack1l11l1l1111_opy_
    def __1l11lll11l1_opy_(self, bstack1l11lll1l1l_opy_=10):
        bstack1l11l11ll11_opy_ = time.time()
        while self.process and time.time() - bstack1l11l11ll11_opy_ < bstack1l11lll1l1l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11ll11_opy_ (u"ࠧ࡯ࡤ࠾ࠤᔅ") in line:
                    self.cli_bin_session_id = line.split(bstack11ll11_opy_ (u"ࠨࡩࡥ࠿ࠥᔆ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll11_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨᔇ") + str(self.cli_bin_session_id) + bstack11ll11_opy_ (u"ࠣࠤᔈ"))
                    continue
                if bstack11ll11_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᔉ") in line:
                    self.cli_listen_addr = line.split(bstack11ll11_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦᔊ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll11_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢᔋ") + str(self.cli_listen_addr) + bstack11ll11_opy_ (u"ࠧࠨᔌ"))
                    continue
                if bstack11ll11_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᔍ") in line:
                    port = line.split(bstack11ll11_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨᔎ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll11_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢᔏ") + str(port) + bstack11ll11_opy_ (u"ࠤࠥᔐ"))
                    continue
                if line.strip() == bstack1l1l11111l1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11ll11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧᔑ"), bstack11ll11_opy_ (u"ࠦ࠶ࠨᔒ")) == bstack11ll11_opy_ (u"ࠧ࠷ࠢᔓ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l11l1l1111_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢᔔ") + str(e) + bstack11ll11_opy_ (u"ࠢࠣᔕ"))
        return False
    def __1l1l11l1lll_opy_(self):
        bstack11ll11_opy_ (u"ࠣࠤࠥࡇࡱ࡫ࡡ࡯ࡷࡳࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡬࡯ࡳࠢࡤࡷࡾࡴࡣࡠࡦ࡬ࡷࡵࡧࡴࡤࡪࡨࡶ࠱ࠦࡣࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡤࡸࡪࡾࡩࡵࠢࡷࡳࠥ࡫࡮ࡴࡷࡵࡩࠥࡺࡡࡴ࡭ࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠢࠣࠤᔖ")
        if self.bstack1l1lll11ll1_opy_ and self.bstack1l1l1lll1ll_opy_:
            try:
                self.bstack1l1lll11ll1_opy_.stop()
                self.bstack1l1l1lll1ll_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l11l1l11l1_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def __1l1l111111l_opy_(self):
        if self.bstack1l11l1l1lll_opy_:
            if self.bstack1l1lll11ll1_opy_ and self.bstack1l1l1lll1ll_opy_:
                try:
                    atexit.unregister(self.__1l1l11l1lll_opy_)
                except ValueError:
                    pass
                self.bstack1l1lll11ll1_opy_.stop()
                self.bstack1l1l1lll1ll_opy_ = False
            start = datetime.now()
            if self.bstack1l11ll111ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1l1l1ll11_opy_:
                    self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᔗ"), datetime.now() - start)
                else:
                    self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢᔘ"), datetime.now() - start)
            self.__1l11l111l1l_opy_()
            start = datetime.now()
            bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(bstack11ll11_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࠤᔙ"))
            self.bstack1l11l1l1lll_opy_.close()
            bstack1ll111lll_opy_.end(bstack11ll11_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࠥᔚ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᔛ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᔜ"), True, None, None, None, None)
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠣࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥᔝ"), datetime.now() - start)
            self.bstack1l11l1l1lll_opy_ = None
        if self.process:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡸࡴࡶࠢᔞ"))
            start = datetime.now()
            bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(bstack11ll11_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡰ࡯࡬࡭ࠤᔟ"))
            self.process.terminate()
            bstack1ll111lll_opy_.end(bstack11ll11_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡱࡩ࡭࡮ࠥᔠ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔡ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔢ"), True, None, None, None, None)
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠢ࡬࡫࡯ࡰࡤࡺࡩ࡮ࡧࠥᔣ"), datetime.now() - start)
            self.process = None
            if self.bstack1l11l1ll1l1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack111l1ll1ll_opy_()
                self.logger.info(
                    bstack11ll11_opy_ (u"ࠣࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠣᔤ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᔥ")] = self.config_testhub.build_hashed_id
        self.bstack1l11l1l1111_opy_ = False
    def __1l11lll1111_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack11ll11_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᔦ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1l111lllll1_opy_ = get_pw_version()
            except:
                bstack1l111lllll1_opy_ = _1l11ll11l11_opy_()
            data.framework_versions[bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᔧ")] = bstack1l111lllll1_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack11ll11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᔨ")] = selenium.__version__
                data.frameworks.append(bstack11ll11_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᔩ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᔪ")] = __version__
                data.frameworks.append(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᔫ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡑࡳࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡨࡪࡺࡥࡤࡶࡨࡨࠧᔬ"))
    def bstack1l11l11l1l1_opy_(self, hub_url: str, platform_index: int, bstack1llllll1111_opy_: Any):
        if self.bstack11l1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢᔭ"))
            return
        try:
            bstack1l111ll1ll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᔮ")
            self.bstack11l1l1l11_opy_ = bstack1l1l1ll11ll_opy_(
                cli.config.get(bstack11ll11_opy_ (u"ࠧ࡮ࡵࡣࡗࡵࡰࠧᔯ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l11l111l11_opy_={bstack11ll11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᔰ"): bstack1llllll1111_opy_}
            )
            def bstack1l1l11l11l1_opy_(self):
                return
            if self.config.get(bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤᔱ"), True):
                Service.start = bstack1l1l11l11l1_opy_
                Service.stop = bstack1l1l11l11l1_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1ll111l1l1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1l1lll1l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᔲ"), datetime.now() - bstack1l111ll1ll_opy_)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣᔳ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦᔴ"))
    def bstack1lll1lll1l_opy_(self, platform_index: int):
        if self.bstack11l1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᔵ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack1l11l11lll1_opy_
                self.bstack11l1l1l11_opy_ = bstack1111l11l1l_opy_(
                    platform_index,
                    framework_name=bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᔶ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l11ll11l11_opy_
                from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1l1ll11111l_opy_
                bstack1l111lllll1_opy_ = get_pw_version()
                self.bstack11l1l1l11_opy_ = bstack1111l11l1l_opy_(
                    platform_index,
                    framework_name=bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᔷ"),
                    framework_version=bstack1l111lllll1_opy_.version,
                    classes=[],
                )
                ctx = bstack1l1ll11111l_opy_.create_context(self.bstack11l1l1l11_opy_)
                bstack1lll1111ll_opy_.bstack11111l111l_opy_[ctx.id] = bstack1l1lll111ll_opy_(
                    ctx, bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᔸ"), bstack1l111lllll1_opy_, bstack11111l1ll_opy_.bstack1ll11lll1_opy_
                )
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࠤᔹ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᔺ"))
            pass
    def bstack11lllll1l1_opy_(self, framework_name: str = None):
        if self.test_framework:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨᔻ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1l1l11l11ll_opy_({ bstack11ll11_opy_ (u"ࠦࡷࡵࡢࡰࡶ࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨᔼ"): VERSION }, [bstack11ll11_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦᔽ")], self.bstack1l1lll11ll1_opy_, self.bstack1l1l111l1_opy_)
                return
            except Exception as e:
                self.logger.error(bstack11ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡴࡲࡦࡴࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠽ࠤࠧᔾ") + str(e) + bstack11ll11_opy_ (u"ࠢࠣᔿ"))
        bstack1l1l11l1111_opy_ = framework_name
        if bstack1l1l11l1111_opy_ == bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩᕀ"):
            import sys
            python_version = bstack11ll11_opy_ (u"ࠤࡾࢁ࠳ࢁࡽ࠯ࡽࢀࠦᕁ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
            self.test_framework = bstack1l11l11l1ll_opy_(
                bstack1l1l1ll111l_opy_={bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫᕂ"): python_version},
                bstack1l1l11l1l11_opy_=[bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬᕃ")],
                bstack1l1lll11ll1_opy_=self.bstack1l1lll11ll1_opy_,
                bstack1l1l111l1_opy_=self.bstack1l1l111l1_opy_
            )
            self.logger.info(bstack11ll11_opy_ (u"ࠧࡏ࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡬࡯ࡳࠢࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠣࡸࡪࡹࡴࡴࠤᕄ"))
            return
        if bstack1lll1l111_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᕅ"): pytest.__version__ }, [bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᕆ")], self.bstack1l1lll11ll1_opy_, self.bstack1l1l111l1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l11l1ll11l_opy_({ bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᕇ"): pytest.__version__ }, [bstack11ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᕈ")], self.bstack1l1lll11ll1_opy_, self.bstack1l1l111l1_opy_)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࠢᕉ") + str(e) + bstack11ll11_opy_ (u"ࠦࠧᕊ"))
        self.bstack1l11l1lll1l_opy_()
    def bstack1l11l1lll1l_opy_(self):
        if not self.bstack1llll1l1l_opy_():
            return
        bstack1l1l11l1l_opy_ = None
        def bstack11l11lll_opy_(config, startdir):
            return bstack11ll11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥᕋ").format(bstack11ll11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᕌ"))
        def bstack111111ll1l_opy_():
            return
        def bstack11ll11l111_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11ll11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᕍ"):
                return bstack11ll11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᕎ")
            else:
                return bstack1l1l11l1l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1l11l1l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l11lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111111ll1l_opy_
            Config.getoption = bstack11ll11l111_opy_
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡵࡥ࡫ࠤࡵࡿࡴࡦࡵࡷࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡦࡰࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠼ࠣࠦᕏ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦᕐ"))
    def bstack1l11l1llll1_opy_(self):
        bstack1ll1l11l1l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll1l11l1l_opy_, dict):
            if cli.config_observability:
                bstack1ll1l11l1l_opy_.update(
                    {bstack11ll11_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᕑ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣᕒ") in accessibility.get(bstack11ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᕓ"), {}):
                    bstack1l1l1llll1l_opy_ = accessibility.get(bstack11ll11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᕔ"))
                    bstack1l1l1llll1l_opy_.update({ bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠤᕕ"): bstack1l1l1llll1l_opy_.pop(bstack11ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧᕖ")) })
                bstack1ll1l11l1l_opy_.update({bstack11ll11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᕗ"): accessibility })
        return bstack1ll1l11l1l_opy_
    @measure(event_name=EVENTS.bstack1l1l1l1l11l_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack1l11ll111ll_opy_(self, bstack1l1l1l11l1l_opy_: str = None, bstack1l11lll1lll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1l1l111l1_opy_:
            return
        bstack1l111ll1ll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᕘ"), bstack11ll11_opy_ (u"ࠬ࠶ࠧᕙ")))
        req.client_worker_id = bstack11ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᕚ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l1l1l11l1l_opy_:
            req.bstack1l1l1l11l1l_opy_ = bstack1l1l1l11l1l_opy_
        if bstack1l11lll1lll_opy_:
            req.bstack1l11lll1lll_opy_ = bstack1l11lll1lll_opy_
        try:
            r = self.bstack1l1l111l1_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡰࡲࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᕛ"), datetime.now() - bstack1l111ll1ll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1l1l1111ll_opy_(self, key: str, value: timedelta):
        tag = bstack11ll11_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᕜ") if self.bstack11lllll1l_opy_() else bstack11ll11_opy_ (u"ࠤࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᕝ")
        self.bstack1l1l1111lll_opy_[bstack11ll11_opy_ (u"ࠥ࠾ࠧᕞ").join([tag + bstack11ll11_opy_ (u"ࠦ࠲ࠨᕟ") + str(id(self)), key])] += value
    def bstack111l1ll1ll_opy_(self):
        if not os.getenv(bstack11ll11_opy_ (u"ࠧࡊࡅࡃࡗࡊࡣࡕࡋࡒࡇࠤᕠ"), bstack11ll11_opy_ (u"ࠨ࠰ࠣᕡ")) == bstack11ll11_opy_ (u"ࠢ࠲ࠤᕢ"):
            return
        bstack1l11l1111l1_opy_ = dict()
        bstack11111l111l_opy_ = []
        if self.test_framework:
            bstack11111l111l_opy_.extend(list(self.test_framework.bstack11111l111l_opy_.values()))
        if self.bstack11l1l1l11_opy_:
            bstack11111l111l_opy_.extend(list(self.bstack11l1l1l11_opy_.bstack11111l111l_opy_.values()))
        for instance in bstack11111l111l_opy_:
            if not instance.platform_index in bstack1l11l1111l1_opy_:
                bstack1l11l1111l1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l11l1111l1_opy_[instance.platform_index]
            for k, v in instance.bstack1l11ll1lll1_opy_().items():
                report[k] += v
                report[k.split(bstack11ll11_opy_ (u"ࠣ࠼ࠥᕣ"))[0]] += v
        bstack1l11ll111l1_opy_ = sorted([(k, v) for k, v in self.bstack1l1l1111lll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l1l111llll_opy_ = 0
        for r in bstack1l11ll111l1_opy_:
            bstack1l1l1l1l1ll_opy_ = r[1].total_seconds()
            bstack1l1l111llll_opy_ += bstack1l1l1l1l1ll_opy_
            self.logger.debug(bstack11ll11_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡻࡳ࡝࠳ࡡࢂࡃࠢᕤ") + str(bstack1l1l1l1l1ll_opy_) + bstack11ll11_opy_ (u"ࠥࠦᕥ"))
        self.logger.debug(bstack11ll11_opy_ (u"ࠦ࠲࠳ࠢᕦ"))
        bstack1l1l1l11lll_opy_ = []
        for platform_index, report in bstack1l11l1111l1_opy_.items():
            bstack1l1l1l11lll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l1l1l11lll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l1ll1111_opy_ = set()
        bstack1l11l1lllll_opy_ = 0
        for r in bstack1l1l1l11lll_opy_:
            bstack1l1l1l1l1ll_opy_ = r[2].total_seconds()
            bstack1l11l1lllll_opy_ += bstack1l1l1l1l1ll_opy_
            bstack1l1ll1111_opy_.add(r[0])
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࢁࡲ࡜࠲ࡠࢁ࠿ࢁࡲ࡜࠳ࡠࢁࡂࠨᕧ") + str(bstack1l1l1l1l1ll_opy_) + bstack11ll11_opy_ (u"ࠨࠢᕨ"))
        if self.bstack11lllll1l_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠢ࠮࠯ࠥᕩ"))
            self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࢁࡴࡰࡶࡤࡰࡤࡩ࡬ࡪࡿࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠱ࢀࡹࡴࡳࠪࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠮ࢃ࠽ࠣᕪ") + str(bstack1l11l1lllll_opy_) + bstack11ll11_opy_ (u"ࠤࠥᕫ"))
        else:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࠢᕬ") + str(bstack1l1l111llll_opy_) + bstack11ll11_opy_ (u"ࠦࠧᕭ"))
        self.logger.debug(bstack11ll11_opy_ (u"ࠧ࠳࠭ࠣᕮ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᕯ"), bstack11ll11_opy_ (u"ࠧ࠱ࠩᕰ"))),
            client_worker_id=bstack11ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᕱ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1l1l111l1_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠤࡦࡰ࡮ࡥࡳࡦࡴࡹ࡭ࡨ࡫ࠠࡪࡵࠣࡲࡴࡺࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨ࠳ࠦࡃࡢࡰࡱࡳࡹࠦࡰࡦࡴࡩࡳࡷࡳࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨᕲ"))
            return None
        response = self.bstack1l1l111l1_opy_.TestOrchestration(request)
        self.logger.debug(bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴ࠮ࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠮ࡵࡨࡷࡸ࡯࡯࡯࠿ࡾࢁࠧᕳ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l1l11ll1l1_opy_(self, r):
        if r is not None and getattr(r, bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࠬᕴ"), None) and getattr(r.testhub, bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᕵ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᕶ")))
            for bstack1l1l111l111_opy_, err in errors.items():
                if err[bstack11ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬᕷ")] == bstack11ll11_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᕸ"):
                    self.logger.info(err[bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᕹ")])
                else:
                    self.logger.error(err[bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕺ")])
    def bstack1l1ll1llll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()