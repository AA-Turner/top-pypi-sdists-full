# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
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
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll1111111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1l11_opy_ import bstack1l1ll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11l11_opy_ import bstack1l1lll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1ll11l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1ll11_opy_ import bstack1l1lll1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11lll_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111llll_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111_opy_ import bstack11111lll1_opy_
from browserstack_sdk.sdk_cli.bstack11l1lllll1_opy_ import bstack11l1lllll1_opy_, bstack1llll11l1_opy_, bstack11ll111l1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll111l11l1_opy_ import bstack1l1ll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1llll1lll_opy_ import bstack1l1ll1l1lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll11lll_opy_ import bstack111l1l1111_opy_
from bstack_utils.helper import Notset, bstack1lllll1l11l_opy_, get_cli_dir, bstack1lllll1l1l1_opy_, bstack1l1ll11l_opy_, bstack1llll1l1ll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll11ll111l_opy_, TestHookState, bstack1ll11lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1ll1ll1l111_opy_, bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l11lll1l_opy_ import bstack1l1ll1l1ll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11ll1ll11_opy_, bstack1l1lll1lll_opy_
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11111_opy_ import bstack1ll11ll1l1l_opy_
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111111l1_opy_())
def bstack1ll11l1ll1l_opy_(bs_config):
    bstack1l1lllll1l1_opy_ = None
    bstack1lllll1lll1_opy_ = None
    try:
        bstack1lllll1lll1_opy_ = get_cli_dir()
        bstack1l1lllll1l1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠢቫ"))
        if not bstack1l1lllll1l1_opy_:
            bstack1l1lllll1l1_opy_ = bstack1lllll1l1l1_opy_(bstack1lllll1lll1_opy_)
            bstack1ll11llll11_opy_ = bstack1lllll1l11l_opy_(bstack1l1lllll1l1_opy_, bstack1lllll1lll1_opy_, bs_config)
            bstack1l1lllll1l1_opy_ = bstack1ll11llll11_opy_ if bstack1ll11llll11_opy_ else bstack1l1lllll1l1_opy_
        if not bstack1l1lllll1l1_opy_:
            raise ValueError(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡃࡍࡋࠣࡴࡦࡺࡨࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦ࡯ࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡩࡳࡱࡪࡥࡳࠤቬ"))
    except Exception as ex:
        logger.error(bstack1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢࡆࡐࡎࠦࡰࡢࡶ࡫࠾ࠥࠨቭ") + str(ex) + bstack1111_opy_ (u"ࠢࠣቮ"))
    return bstack1l1lllll1l1_opy_, bstack1lllll1lll1_opy_
bstack1ll11llllll_opy_ = bstack1111_opy_ (u"ࠣ࠻࠼࠽࠾ࠨቯ")
bstack1l1lllll111_opy_ = bstack1111_opy_ (u"ࠤࡵࡩࡦࡪࡹࠣተ")
bstack1ll111lll1l_opy_ = bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢቱ")
bstack1l1lllll1ll_opy_ = bstack1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡑࡏࡓࡕࡇࡑࡣࡆࡊࡄࡓࠤቲ")
bstack1111ll1l_opy_ = bstack1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣታ")
bstack1l1llll1ll1_opy_ = re.compile(bstack1111_opy_ (u"ࡸࠢࠩࡁ࡬࠭࠳࠰ࠨࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࢂࡂࡔࠫ࠱࠮ࠧቴ"))
bstack1l1ll1l111l_opy_ = bstack1111_opy_ (u"ࠢࡥࡧࡹࡩࡱࡵࡰ࡮ࡧࡱࡸࠧት")
bstack1ll1l11ll1l_opy_ = bstack1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡑࡕࡇࡊࡥࡆࡂࡎࡏࡆࡆࡉࡋࠣቶ")
bstack1l1ll1l1111_opy_ = [
    bstack1llll11l1_opy_.bstack1ll1l111l1_opy_,
    bstack1llll11l1_opy_.CONNECT,
    bstack1llll11l1_opy_.bstack1ll1lll1l1_opy_,
]
def _1l1ll1l1ll1_opy_():
    bstack1111_opy_ (u"ࠤࠥࠦࡋࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࠤࡱ࡯ࡢࡳࡣࡵࡽࠥࡂࠠ࠲࠻࠱࠸࠳࠶ࠠࡸࡪࡨࡶࡪࠦࡂࡳࡱࡺࡷࡪࡸ࠮ࡦࡰࡷࡶࡾ࠴ࡧࡦࡶࡢࡺࡪࡸࡳࡪࡱࡱࡷࠥࡪ࡯ࡦࡵࡱࠫࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠨࠢࠣቷ")
    import re
    from types import SimpleNamespace
    try:
        import Browser
        bstack1ll11l11ll1_opy_ = Path(Browser.__file__).parent / bstack1111_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡵࠦቸ") / bstack1111_opy_ (u"ࠦࡵࡧࡣ࡬ࡣࡪࡩ࠳ࡰࡳࡰࡰࠥቹ")
        bstack1l1ll1l1l1l_opy_ = json.loads(bstack1ll11l11ll1_opy_.read_text())
        match = re.search(bstack1111_opy_ (u"ࡷࠨ࡜ࡥ࠭࡟࠲ࡡࡪࠫ࡝࠰࡟ࡨ࠰ࠨቺ"), bstack1l1ll1l1l1l_opy_[bstack1111_opy_ (u"ࠨࡤࡦࡲࡨࡲࡩ࡫࡮ࡤ࡫ࡨࡷࠧቻ")][bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦቼ")])
        bstack1ll111ll1l1_opy_ = match.group(0) if match else bstack1111_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤች")
    except Exception:
        bstack1ll111ll1l1_opy_ = bstack1111_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥቾ")
    return SimpleNamespace(version=bstack1ll111ll1l1_opy_)
class SDKCLI:
    _1ll1l11l1ll_opy_ = None
    process: Union[None, Any]
    bstack1ll111l1111_opy_: bool
    bstack1ll1l11l11l_opy_: bool
    bstack1l1lll111l1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll1l111111_opy_: Union[None, grpc.Channel]
    bstack1ll11ll1lll_opy_: str
    test_framework: TestFramework
    bstack1lll11lllll_opy_: bstack1lll11l1ll1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll111l11ll_opy_: bstack11111lll1_opy_
    accessibility: bstack1l1ll1l11l1_opy_
    bstack1llll11lll_opy_: bstack111l1l1111_opy_
    ai: bstack1l1lll1lll1_opy_
    bstack1l1llllll1l_opy_: bstack1ll11l1l1ll_opy_
    bstack1ll1l11111l_opy_: List[bstack1ll111l1l1l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l1lll111ll_opy_: Any
    bstack1ll11lll1ll_opy_: Dict[str, timedelta]
    bstack1l1ll1l1l11_opy_: str
    bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_
    def __new__(cls):
        if not cls._1ll1l11l1ll_opy_:
            cls._1ll1l11l1ll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1l11l1ll_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll111l1111_opy_ = False
        self.bstack1ll1l111111_opy_ = None
        self.bstack1lll111l111_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l1lllll1ll_opy_, None)
        self.bstack1ll1l11l111_opy_ = os.environ.get(bstack1ll111lll1l_opy_, bstack1111_opy_ (u"ࠥࠦቿ")) == bstack1111_opy_ (u"ࠦࠧኀ")
        self.bstack1ll1l11l11l_opy_ = False
        self.bstack1l1lll111l1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l1lll111ll_opy_ = None
        self.test_framework = None
        self.bstack1lll11lllll_opy_ = None
        self.bstack1ll11ll1lll_opy_=bstack1111_opy_ (u"ࠧࠨኁ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.bstack1ll111111l1_opy_())
        self.bstack1ll11lll1ll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1ll1lllll1l_opy_ = bstack1lll1111111_opy_()
        self.bstack1l1lllllll1_opy_ = False
        self.bstack1ll1l1111ll_opy_ = None
        self.bstack1ll11l1lll1_opy_ = None
        self.bstack1ll111l11ll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1l11111l_opy_ = []
    def bstack1ll11ll11l_opy_(self):
        return os.environ.get(bstack1111ll1l_opy_).lower().__eq__(bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦኂ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll1l11ll1l_opy_, bstack1111_opy_ (u"ࠧࠨኃ")).lower() in [bstack1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ኄ"), bstack1111_opy_ (u"ࠩ࠴ࠫኅ"), bstack1111_opy_ (u"ࠪࡽࡪࡹࠧኆ")]:
            self.logger.debug(bstack1111_opy_ (u"ࠦࡋࡵࡲࡤ࡫ࡱ࡫ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠ࡮ࡱࡧࡩࠥࡪࡵࡦࠢࡷࡳࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡕࡒࡄࡇࡢࡊࡆࡒࡌࡃࡃࡆࡏࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࠧኇ"))
            os.environ[bstack1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣኈ")] = bstack1111_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧ኉")
            return False
        if bstack1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫኊ") in config and str(config[bstack1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬኋ")]).lower() != bstack1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨኌ"):
            return False
        bstack1l1lll11ll1_opy_ = [bstack1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥኍ"), bstack1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ኎"), bstack1111_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨࠨ኏")]
        if is_robot_playwright_installed():
            bstack1l1lll11ll1_opy_.append(bstack1111_opy_ (u"ࠨࡲࡰࡤࡲࡸࠧነ"))
            bstack1l1lll11ll1_opy_.append(bstack1111_opy_ (u"ࠢࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠣኑ"))
        bstack1ll1111111l_opy_ = config.get(bstack1111_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦኒ")) in bstack1l1lll11ll1_opy_ or os.environ.get(bstack1111_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪና")) in bstack1l1lll11ll1_opy_
        os.environ[bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨኔ")] = str(bstack1ll1111111l_opy_) # bstack1ll11111l11_opy_ bstack1l1lll1l111_opy_ VAR to bstack1ll1111l1ll_opy_ is binary running
        return bstack1ll1111111l_opy_
    def bstack111l11l1l_opy_(self):
        for event in bstack1l1ll1l1111_opy_:
            bstack11l1lllll1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11l1lllll1_opy_.logger.debug(bstack1111_opy_ (u"ࠦࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠣࡁࡃࠦࡻࡢࡴࡪࡷࢂࠦࠢን") + str(kwargs) + bstack1111_opy_ (u"ࠧࠨኖ"))
            )
        bstack11l1lllll1_opy_.register(bstack1llll11l1_opy_.bstack1ll1l111l1_opy_, self.__1ll11lll11l_opy_)
        bstack11l1lllll1_opy_.register(bstack1llll11l1_opy_.CONNECT, self.__1l1llll11ll_opy_)
        bstack11l1lllll1_opy_.register(bstack1llll11l1_opy_.bstack1ll1lll1l1_opy_, self.__1l1llll1l11_opy_)
        bstack11l1lllll1_opy_.register(bstack1llll11l1_opy_.bstack11ll11l1l_opy_, self.__1l1ll1ll11l_opy_)
    def bstack1lll1l1lll_opy_(self):
        return not self.bstack1ll1l11l111_opy_ and os.environ.get(bstack1ll111lll1l_opy_, bstack1111_opy_ (u"ࠨࠢኗ")) != bstack1111_opy_ (u"ࠢࠣኘ")
    def is_running(self):
        if self.bstack1ll1l11l111_opy_:
            return self.bstack1ll111l1111_opy_
        else:
            return bool(self.bstack1ll1l111111_opy_)
    def is_screenshots_allowed(self):
        try:
            return (
                self.config_observability
                and self.config_observability.HasField(bstack1111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩኙ"))
                and self.config_observability.options.allow_screenshots == bstack1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧኚ")
            )
        except Exception:
            return False
    def bstack1l11ll11l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1l11111l_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll1111lll1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1l1ll1llll1_opy_(self, bstack1ll111l1ll1_opy_=10):
        if self.bstack1lll111l111_opy_:
            return
        bstack1l1llll111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l1lllll1ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1111_opy_ (u"ࠥ࡟ࠧኛ") + str(id(self)) + bstack1111_opy_ (u"ࠦࡢࠦࡣࡰࡰࡱࡩࡨࡺࡩ࡯ࡩࠥኜ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡠࡲࡵࡳࡽࡿࠢኝ"), 0), (bstack1111_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡵࡢࡴࡷࡵࡸࡺࠤኞ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll111l1ll1_opy_)
        self.bstack1ll1l111111_opy_ = channel
        self.bstack1lll111l111_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll1l111111_opy_)
        self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࠨኟ"), datetime.now() - bstack1l1llll111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l1lllll1ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦ࠽ࠤ࡮ࡹ࡟ࡤࡪ࡬ࡰࡩࡥࡰࡳࡱࡦࡩࡸࡹ࠽ࠣአ") + str(self.bstack1lll1l1lll_opy_()) + bstack1111_opy_ (u"ࠤࠥኡ"))
    def __1l1llll1l11_opy_(self, event_name):
        if self.bstack1lll1l1lll_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡃࡍࡋࠥኢ"))
        self.__1l1llllllll_opy_()
    @measure(event_name=EVENTS.bstack1ll111ll111_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1l1ll1ll11l_opy_(self, event_name, bstack1ll11ll11ll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1111_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠦኣ"))
        bstack1ll1l11l1l1_opy_ = Path(bstack1ll1l1l11l1_opy_ (u"ࠧࢁࡳࡦ࡮ࡩ࠲ࡨࡲࡩࡠࡦ࡬ࡶࢂ࠵ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࡳ࠯࡬ࡶࡳࡳࠨኤ"))
        if self.bstack1lllll1lll1_opy_ and bstack1ll1l11l1l1_opy_.exists():
            with open(bstack1ll1l11l1l1_opy_, bstack1111_opy_ (u"࠭ࡲࠨእ"), encoding=bstack1111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ኦ")) as fp:
                data = json.load(fp)
                try:
                    bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ኧ"), bstack1l1ll1l1ll_opy_(bstack11l1111ll_opy_), data, {
                        bstack1111_opy_ (u"ࠩࡤࡹࡹ࡮ࠧከ"): (self.config[bstack1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬኩ")], self.config[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧኪ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1lll1lll_opy_.format(str(e)))
            bstack1ll1l11l1l1_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll111lll11_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1ll11lll11l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
        self.bstack1ll11ll1lll_opy_, self.bstack1lllll1lll1_opy_ = bstack1ll11l1ll1l_opy_(data.bs_config)
        os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡜ࡘࡉࡕࡃࡅࡐࡊࡥࡄࡊࡔࠪካ")] = self.bstack1lllll1lll1_opy_
        if not self.bstack1ll11ll1lll_opy_ or not self.bstack1lllll1lll1_opy_:
            raise ValueError(bstack1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡪࡨࠤࡘࡊࡋࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠧኬ"))
        if self.bstack1lll1l1lll_opy_():
            self.__1l1llll11ll_opy_(event_name, bstack11ll111l1_opy_())
            return
        try:
            logger.debug(bstack1111_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨክ"))
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧኮ").format(e))
        start = datetime.now()
        is_started = self.__1ll11l11lll_opy_()
        self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨኯ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l1ll1llll1_opy_()
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤኰ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1lllll11l_opy_(data)
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤ኱"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll11l1ll11_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1l1llll11ll_opy_(self, event_name: str, data: bstack11ll111l1_opy_):
        if not self.bstack1lll1l1lll_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤኲ"))
            return
        bin_session_id = os.environ.get(bstack1ll111lll1l_opy_)
        start = datetime.now()
        self.__1l1ll1llll1_opy_()
        self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧኳ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨኴ") + str(bin_session_id) + bstack1111_opy_ (u"ࠣࠤኵ"))
        start = datetime.now()
        self.__1ll1111l1l1_opy_()
        self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢ኶"), datetime.now() - start)
    def __1ll11lll1l1_opy_(self):
        if not self.bstack1lll111l111_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢ኷"))
            return
        bstack1ll111l111l_opy_ = {
            bstack1111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣኸ"): (bstack1ll111ll1ll_opy_, bstack1ll111l1lll_opy_, bstack1lll11l11ll_opy_),
            bstack1111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢኹ"): (bstack1l1lll1l1ll_opy_, bstack1ll1l111l1l_opy_, bstack1ll11l11111_opy_),
        }
        if not self.bstack1ll1l1111ll_opy_ and self.session_framework in bstack1ll111l111l_opy_:
            bstack1ll1l1111l1_opy_, bstack1l1ll1ll111_opy_, bstack1l1ll1lll1l_opy_ = bstack1ll111l111l_opy_[self.session_framework]
            bstack1ll11111lll_opy_ = bstack1l1ll1ll111_opy_()
            self.bstack1ll11l1lll1_opy_ = bstack1ll11111lll_opy_
            self.bstack1ll1l1111ll_opy_ = bstack1l1ll1lll1l_opy_
            self.bstack1ll1l11111l_opy_.append(bstack1ll11111lll_opy_)
            self.bstack1ll1l11111l_opy_.append(bstack1ll1l1111l1_opy_(self.bstack1ll11l1lll1_opy_))
        if not self.bstack1ll111l11ll_opy_ and self.config_observability and self.config_observability.success:
            self.bstack1ll111l11ll_opy_ = bstack11111lll1_opy_(self.bstack1ll1l1111ll_opy_, self.bstack1ll11l1lll1_opy_)
            self.bstack1ll1l11111l_opy_.append(self.bstack1ll111l11ll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l1ll1l11l1_opy_(self.bstack1ll1l1111ll_opy_, self.bstack1ll11l1lll1_opy_)
            self.bstack1ll1l11111l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1111_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣኺ"), False) == True:
            self.ai = bstack1l1lll1lll1_opy_()
            self.bstack1ll1l11111l_opy_.append(self.ai)
        if not self.percy and self.bstack1l1lll111ll_opy_ and self.bstack1l1lll111ll_opy_.success:
            self.percy = bstack1ll11l1l1ll_opy_(self.bstack1l1lll111ll_opy_)
            self.bstack1ll1l11111l_opy_.append(self.percy)
        for mod in self.bstack1ll1l11111l_opy_:
            if not mod.bstack1ll111111ll_opy_():
                mod.configure(self.bstack1lll111l111_opy_, self.config, self.cli_bin_session_id, self.bstack1ll1lllll1l_opy_)
    def __1ll11111l1l_opy_(self):
        for mod in self.bstack1ll1l11111l_opy_:
            if mod.bstack1ll111111ll_opy_():
                mod.configure(self.bstack1lll111l111_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l1lll1111l_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1l1lllll11l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1l11l11l_opy_:
            return
        self.__1ll1111l111_opy_(data)
        bstack1l1llll111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢኻ")
        req.sdk_language = bstack1111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣኼ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l1llll1ll1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩኽ"), bstack1111_opy_ (u"ࠪ࠴ࠬኾ")))
            req.client_worker_id = bstack1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ኿").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡸࡱࡵ࡯ࡪࡸࠠࡢࡰࡧࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡩ࡯ࡦࡨࡼ࠿ࠦࡻࡾࠤዀ").format(e))
        try:
            self.logger.debug(bstack1111_opy_ (u"ࠨ࡛ࠣ዁") + str(id(self)) + bstack1111_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨዂ"))
            r = self.bstack1lll111l111_opy_.StartBinSession(req)
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥዃ"), datetime.now() - bstack1l1llll111_opy_)
            os.environ[bstack1ll111lll1l_opy_] = r.bin_session_id
            self.__1ll1l11ll11_opy_(r)
            self.__1ll11lll1l1_opy_()
            if not self.bstack1l1lllllll1_opy_:
                self.bstack1ll1lllll1l_opy_.start()
                self.bstack1l1lllllll1_opy_ = True
                atexit.register(self.__1ll1l111ll1_opy_)
            self.bstack1ll1l11l11l_opy_ = True
            self.logger.debug(bstack1111_opy_ (u"ࠤ࡞ࠦዄ") + str(id(self)) + bstack1111_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣዅ"))
        except grpc.bstack1ll1l111lll_opy_ as bstack1ll11l1l1l1_opy_:
            self.logger.error(bstack1111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ዆") + str(bstack1ll11l1l1l1_opy_) + bstack1111_opy_ (u"ࠧࠨ዇"))
            traceback.print_exc()
            raise bstack1ll11l1l1l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥወ") + str(e) + bstack1111_opy_ (u"ࠢࠣዉ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1l111l11_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1ll1111l1l1_opy_(self):
        if not self.bstack1lll1l1lll_opy_() or not self.cli_bin_session_id or self.bstack1l1lll111l1_opy_:
            return
        bstack1l1llll111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨዊ"), bstack1111_opy_ (u"ࠩ࠳ࠫዋ")))
        req.client_worker_id = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤዌ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1111_opy_ (u"ࠦࡠࠨው") + str(id(self)) + bstack1111_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢዎ"))
            r = self.bstack1lll111l111_opy_.ConnectBinSession(req)
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥዏ"), datetime.now() - bstack1l1llll111_opy_)
            self.__1ll1l11ll11_opy_(r)
            self.__1ll11lll1l1_opy_()
            if not self.bstack1l1lllllll1_opy_:
                self.bstack1ll1lllll1l_opy_.start()
                self.bstack1l1lllllll1_opy_ = True
                atexit.register(self.__1ll1l111ll1_opy_)
            self.bstack1l1lll111l1_opy_ = True
            self.logger.debug(bstack1111_opy_ (u"ࠢ࡜ࠤዐ") + str(id(self)) + bstack1111_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢዑ"))
        except grpc.bstack1ll1l111lll_opy_ as bstack1ll11l1l1l1_opy_:
            self.logger.error(bstack1111_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦዒ") + str(bstack1ll11l1l1l1_opy_) + bstack1111_opy_ (u"ࠥࠦዓ"))
            traceback.print_exc()
            raise bstack1ll11l1l1l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣዔ") + str(e) + bstack1111_opy_ (u"ࠧࠨዕ"))
            traceback.print_exc()
            raise e
    def __1ll1l11ll11_opy_(self, r):
        self.bstack1ll11l111l1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1111_opy_ (u"ࠨࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧዖ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1111_opy_ (u"ࠢࡦ࡯ࡳࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡷࡱࡨࠧ዗"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡥࡳࡥࡼࠤ࡮ࡹࠠࡴࡧࡱࡸࠥࡵ࡮࡭ࡻࠣࡥࡸࠦࡰࡢࡴࡷࠤࡴ࡬ࠠࡵࡪࡨࠤࠧࡉ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠮ࠥࠤࡦࡴࡤࠡࡶ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡦࡲࡳࡰࠢࡸࡷࡪࡪࠠࡣࡻࠣࡗࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡨࡶࡪ࡬࡯ࡳࡧ࠯ࠤࡓࡵ࡮ࡦࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤ࡮ࡹࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥዘ")
        self.bstack1l1lll111ll_opy_ = getattr(r, bstack1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨዙ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧዚ")] = self.config_testhub.jwt
        os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩዛ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1ll11lll111_opy_ = json.loads(r.config)
            bstack1ll11l11l11_opy_ = bstack1ll11lll111_opy_.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩዜ"), {}).get(bstack1111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨዝ"), bstack1111_opy_ (u"ࠧࠨዞ"))
            os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪዟ")] = bstack1ll11l11l11_opy_
    def bstack1ll11l111ll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll111l1111_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll11ll11l1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll11ll11l1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll11l111ll_opy_(event_name=EVENTS.bstack1l1llllll11_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1ll11l11lll_opy_(self, bstack1ll111l1ll1_opy_=10):
        if self.bstack1ll111l1111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠤࡶࡸࡦࡸࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠦዠ"))
            return True
        self.logger.debug(bstack1111_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤዡ"))
        if os.getenv(bstack1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡆࡐ࡙ࠦዢ")) == bstack1l1ll1l111l_opy_:
            self.cli_bin_session_id = bstack1l1ll1l111l_opy_
            self.cli_listen_addr = bstack1111_opy_ (u"ࠧࡻ࡮ࡪࡺ࠽࠳ࡹࡳࡰ࠰ࡵࡧ࡯࠲ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࠦࡵ࠱ࡷࡴࡩ࡫ࠣዣ") % (self.cli_bin_session_id)
            self.bstack1ll111l1111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1ll11ll1lll_opy_, bstack1111_opy_ (u"ࠨࡳࡥ࡭ࠥዤ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1111ll1l_opy_ compat for text=True in bstack1ll11ll1111_opy_ python
            encoding=bstack1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨዥ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1lll1l11l_opy_ = threading.Thread(target=self.__1ll1111l11l_opy_, args=(bstack1ll111l1ll1_opy_,))
        bstack1l1lll1l11l_opy_.start()
        bstack1l1lll1l11l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡴࡲࡤࡻࡳࡀࠠࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥࡾࠢࡲࡹࡹࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡳࡵࡦࡲࡹࡹ࠴ࡲࡦࡣࡧࠬ࠮ࢃࠠࡦࡴࡵࡁࠧዦ") + str(self.process.stderr.read()) + bstack1111_opy_ (u"ࠤࠥዧ"))
        if not self.bstack1ll111l1111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠥ࡟ࠧየ") + str(id(self)) + bstack1111_opy_ (u"ࠦࡢࠦࡣ࡭ࡧࡤࡲࡺࡶࠢዩ"))
            self.__1l1llllllll_opy_()
        self.logger.debug(bstack1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡵࡸ࡯ࡤࡧࡶࡷࡤࡸࡥࡢࡦࡼ࠾ࠥࠨዪ") + str(self.bstack1ll111l1111_opy_) + bstack1111_opy_ (u"ࠨࠢያ"))
        return self.bstack1ll111l1111_opy_
    def __1ll1111l11l_opy_(self, bstack1l1ll1l11ll_opy_=10):
        bstack1l1llll1l1l_opy_ = time.time()
        while self.process and time.time() - bstack1l1llll1l1l_opy_ < bstack1l1ll1l11ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1111_opy_ (u"ࠢࡪࡦࡀࠦዬ") in line:
                    self.cli_bin_session_id = line.split(bstack1111_opy_ (u"ࠣ࡫ࡧࡁࠧይ"))[-1:][0].strip()
                    self.logger.debug(bstack1111_opy_ (u"ࠤࡦࡰ࡮ࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠣዮ") + str(self.cli_bin_session_id) + bstack1111_opy_ (u"ࠥࠦዯ"))
                    continue
                if bstack1111_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧደ") in line:
                    self.cli_listen_addr = line.split(bstack1111_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨዱ"))[-1:][0].strip()
                    self.logger.debug(bstack1111_opy_ (u"ࠨࡣ࡭࡫ࡢࡰ࡮ࡹࡴࡦࡰࡢࡥࡩࡪࡲ࠻ࠤዲ") + str(self.cli_listen_addr) + bstack1111_opy_ (u"ࠢࠣዳ"))
                    continue
                if bstack1111_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢዴ") in line:
                    port = line.split(bstack1111_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣድ"))[-1:][0].strip()
                    self.logger.debug(bstack1111_opy_ (u"ࠥࡴࡴࡸࡴ࠻ࠤዶ") + str(port) + bstack1111_opy_ (u"ࠦࠧዷ"))
                    continue
                if line.strip() == bstack1l1lllll111_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡎࡕ࡟ࡔࡖࡕࡉࡆࡓࠢዸ"), bstack1111_opy_ (u"ࠨ࠱ࠣዹ")) == bstack1111_opy_ (u"ࠢ࠲ࠤዺ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll111l1111_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸ࠺ࠡࠤዻ") + str(e) + bstack1111_opy_ (u"ࠤࠥዼ"))
        return False
    def __1ll1l111ll1_opy_(self):
        bstack1111_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡱࡹࡵࠦࡨࡢࡰࡧࡰࡪࡸࠠࡧࡱࡵࠤࡦࡹࡹ࡯ࡥࡢࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࠬࠡࡥࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡦࡺࡥࡹ࡫ࡷࠤࡹࡵࠠࡦࡰࡶࡹࡷ࡫ࠠࡵࡣࡶ࡯ࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠤࠥࠦዽ")
        if self.bstack1ll1lllll1l_opy_ and self.bstack1l1lllllll1_opy_:
            try:
                self.bstack1ll1lllll1l_opy_.stop()
                self.bstack1l1lllllll1_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1ll11ll1ll1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def __1l1llllllll_opy_(self):
        if self.bstack1ll1l111111_opy_:
            if self.bstack1ll1lllll1l_opy_ and self.bstack1l1lllllll1_opy_:
                try:
                    atexit.unregister(self.__1ll1l111ll1_opy_)
                except ValueError:
                    pass
                self.bstack1ll1lllll1l_opy_.stop()
                self.bstack1l1lllllll1_opy_ = False
            start = datetime.now()
            if self.bstack1ll11l1111l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1lll111l1_opy_:
                    self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣዾ"), datetime.now() - start)
                else:
                    self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤዿ"), datetime.now() - start)
            self.__1ll11111l1l_opy_()
            start = datetime.now()
            bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(bstack1111_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࠦጀ"))
            self.bstack1ll1l111111_opy_.close()
            bstack1l11l1ll_opy_.end(bstack1111_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࠧጁ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣጂ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢጃ"), True, None, None, None, None)
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧጄ"), datetime.now() - start)
            self.bstack1ll1l111111_opy_ = None
        if self.process:
            self.logger.debug(bstack1111_opy_ (u"ࠦࡸࡺ࡯ࡱࠤጅ"))
            start = datetime.now()
            bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(bstack1111_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡫ࡪ࡮࡯ࠦጆ"))
            self.process.terminate()
            bstack1l11l1ll_opy_.end(bstack1111_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺࡬࡫࡯ࡰࠧጇ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢገ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨጉ"), True, None, None, None, None)
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤ࡮࡭ࡱࡲ࡟ࡵ࡫ࡰࡩࠧጊ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll1l11l111_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack111lll11ll_opy_()
                self.logger.info(
                    bstack1111_opy_ (u"࡚ࠥ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠥጋ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪጌ")] = self.config_testhub.build_hashed_id
        self.bstack1ll111l1111_opy_ = False
    def __1ll1111l111_opy_(self, data):
        if is_robot_playwright_installed():
            data.frameworks.append(bstack1111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤግ"))
            try:
                from Browser.entry.get_versions import get_pw_version
                bstack1ll11l1llll_opy_ = get_pw_version()
            except:
                bstack1ll11l1llll_opy_ = _1l1ll1l1ll1_opy_()
            data.framework_versions[bstack1111_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥጎ")] = bstack1ll11l1llll_opy_.version
        else:
            try:
                import selenium
                data.framework_versions[bstack1111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤጏ")] = selenium.__version__
                data.frameworks.append(bstack1111_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥጐ"))
            except:
                pass
            try:
                from playwright._repo_version import __version__
                data.framework_versions[bstack1111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ጑")] = __version__
                data.frameworks.append(bstack1111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢጒ"))
            except:
                pass
            if not data.frameworks:
                self.logger.debug(bstack1111_opy_ (u"ࠦࡓࡵࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡪࡥࡵࡧࡦࡸࡪࡪࠢጓ"))
    def bstack1l1ll1ll1ll_opy_(self, hub_url: str, platform_index: int, bstack11l111l111_opy_: Any):
        if self.bstack1lll11lllll_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤጔ"))
            return
        try:
            bstack1l1llll111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣጕ")
            self.bstack1lll11lllll_opy_ = bstack1ll11l11111_opy_(
                cli.config.get(bstack1111_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢ጖"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1llll111l_opy_={bstack1111_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧ጗"): bstack11l111l111_opy_}
            )
            def bstack1l1llll11l1_opy_(self):
                return
            if self.config.get(bstack1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦጘ"), True):
                Service.start = bstack1l1llll11l1_opy_
                Service.stop = bstack1l1llll11l1_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack111l1l1111_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1ll1l1lll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦጙ"), datetime.now() - bstack1l1llll111_opy_)
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥጚ") + str(e) + bstack1111_opy_ (u"ࠧࠨጛ"))
    def bstack1llll1ll1_opy_(self, platform_index: int):
        if self.bstack1lll11lllll_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧጜ"))
            return
        try:
            if not is_robot_playwright_installed():
                from playwright.sync_api import BrowserType
                from playwright.sync_api import BrowserContext
                from playwright._impl._connection import Connection
                from playwright._repo_version import __version__
                from bstack_utils.helper import bstack111lll111l_opy_
                self.bstack1lll11lllll_opy_ = bstack1lll11l11ll_opy_(
                    platform_index,
                    framework_name=bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦጝ"),
                    framework_version=__version__,
                    classes=[BrowserType, BrowserContext, Connection],
                )
            else:
                try:
                    from Browser.entry.get_versions import get_pw_version
                except:
                    get_pw_version = _1l1ll1l1ll1_opy_
                from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1llll1l1_opy_
                bstack1ll11l1llll_opy_ = get_pw_version()
                self.bstack1lll11lllll_opy_ = bstack1lll11l11ll_opy_(
                    platform_index,
                    framework_name=bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧጞ"),
                    framework_version=bstack1ll11l1llll_opy_.version,
                    classes=[],
                )
                ctx = bstack1ll1llll1l1_opy_.create_context(self.bstack1lll11lllll_opy_)
                bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_[ctx.id] = bstack1ll1ll1l111_opy_(
                    ctx, bstack1111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨጟ"), bstack1ll11l1llll_opy_, bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_
                )
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠼ࠣࠦጠ") + str(e) + bstack1111_opy_ (u"ࠦࠧጡ"))
            pass
    def bstack11l1lll11_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢጢ"))
            return
        if is_robot_playwright_installed():
            try:
                import robot
                from robot.version import VERSION
                self.test_framework = bstack1ll11ll1l1l_opy_({ bstack1111_opy_ (u"ࠨࡲࡰࡤࡲࡸ࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣጣ"): VERSION }, [bstack1111_opy_ (u"ࠢࡳࡱࡥࡳࡹࠨጤ")], self.bstack1ll1lllll1l_opy_, self.bstack1lll111l111_opy_)
                return
            except Exception as e:
                self.logger.error(bstack1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡶࡴࡨ࡯ࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠿ࠦࠢጥ") + str(e) + bstack1111_opy_ (u"ࠤࠥጦ"))
        if bstack1l1ll11l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥጧ"): pytest.__version__ }, [bstack1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣጨ")], self.bstack1ll1lllll1l_opy_, self.bstack1lll111l111_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1ll1ll1l1_opy_({ bstack1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧጩ"): pytest.__version__ }, [bstack1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨጪ")], self.bstack1ll1lllll1l_opy_, self.bstack1lll111l111_opy_)
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦጫ") + str(e) + bstack1111_opy_ (u"ࠣࠤጬ"))
        self.bstack1l1ll1lll11_opy_()
    def bstack1l1ll1lll11_opy_(self):
        if not self.bstack1ll11ll11l_opy_():
            return
        bstack1ll11lllll_opy_ = None
        def bstack11l1l1l111_opy_(config, startdir):
            return bstack1111_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢጭ").format(bstack1111_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤጮ"))
        def bstack1l11ll11ll_opy_():
            return
        def bstack111lll1lll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1111_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫጯ"):
                return bstack1111_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦጰ")
            else:
                return bstack1ll11lllll_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll11lllll_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l1l1l111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11ll11ll_opy_
            Config.getoption = bstack111lll1lll_opy_
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣጱ") + str(e) + bstack1111_opy_ (u"ࠢࠣጲ"))
    def bstack1ll111ll11l_opy_(self):
        bstack1llll1lll1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1llll1lll1_opy_, dict):
            if cli.config_observability:
                bstack1llll1lll1_opy_.update(
                    {bstack1111_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣጳ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧጴ") in accessibility.get(bstack1111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦጵ"), {}):
                    bstack1ll11111111_opy_ = accessibility.get(bstack1111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧጶ"))
                    bstack1ll11111111_opy_.update({ bstack1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨጷ"): bstack1ll11111111_opy_.pop(bstack1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤጸ")) })
                bstack1llll1lll1_opy_.update({bstack1111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢጹ"): accessibility })
        return bstack1llll1lll1_opy_
    @measure(event_name=EVENTS.bstack1ll11l1l111_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1ll11l1111l_opy_(self, bstack1ll11l1l11l_opy_: str = None, bstack1l1lll1llll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll111l111_opy_:
            return
        bstack1l1llll111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨጺ"), bstack1111_opy_ (u"ࠩ࠳ࠫጻ")))
        req.client_worker_id = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤጼ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll11l1l11l_opy_:
            req.bstack1ll11l1l11l_opy_ = bstack1ll11l1l11l_opy_
        if bstack1l1lll1llll_opy_:
            req.bstack1l1lll1llll_opy_ = bstack1l1lll1llll_opy_
        try:
            r = self.bstack1lll111l111_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧጽ"), datetime.now() - bstack1l1llll111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11ll1llll_opy_(self, key: str, value: timedelta):
        tag = bstack1111_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧጾ") if self.bstack1lll1l1lll_opy_() else bstack1111_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧጿ")
        self.bstack1ll11lll1ll_opy_[bstack1111_opy_ (u"ࠢ࠻ࠤፀ").join([tag + bstack1111_opy_ (u"ࠣ࠯ࠥፁ") + str(id(self)), key])] += value
    def bstack111lll11ll_opy_(self):
        if not os.getenv(bstack1111_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨፂ"), bstack1111_opy_ (u"ࠥ࠴ࠧፃ")) == bstack1111_opy_ (u"ࠦ࠶ࠨፄ"):
            return
        bstack1l1lll1l1l1_opy_ = dict()
        bstack1lll1111lll_opy_ = []
        if self.test_framework:
            bstack1lll1111lll_opy_.extend(list(self.test_framework.bstack1lll1111lll_opy_.values()))
        if self.bstack1lll11lllll_opy_:
            bstack1lll1111lll_opy_.extend(list(self.bstack1lll11lllll_opy_.bstack1lll1111lll_opy_.values()))
        for instance in bstack1lll1111lll_opy_:
            if not instance.platform_index in bstack1l1lll1l1l1_opy_:
                bstack1l1lll1l1l1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l1lll1l1l1_opy_[instance.platform_index]
            for k, v in instance.bstack1ll11111ll1_opy_().items():
                report[k] += v
                report[k.split(bstack1111_opy_ (u"ࠧࡀࠢፅ"))[0]] += v
        bstack1ll111llll1_opy_ = sorted([(k, v) for k, v in self.bstack1ll11lll1ll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll111lllll_opy_ = 0
        for r in bstack1ll111llll1_opy_:
            bstack1l1llll1111_opy_ = r[1].total_seconds()
            bstack1ll111lllll_opy_ += bstack1l1llll1111_opy_
            self.logger.debug(bstack1111_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦፆ") + str(bstack1l1llll1111_opy_) + bstack1111_opy_ (u"ࠢࠣፇ"))
        self.logger.debug(bstack1111_opy_ (u"ࠣ࠯࠰ࠦፈ"))
        bstack1ll11llll1l_opy_ = []
        for platform_index, report in bstack1l1lll1l1l1_opy_.items():
            bstack1ll11llll1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll11llll1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1lllll1l1l_opy_ = set()
        bstack1ll111l1l11_opy_ = 0
        for r in bstack1ll11llll1l_opy_:
            bstack1l1llll1111_opy_ = r[2].total_seconds()
            bstack1ll111l1l11_opy_ += bstack1l1llll1111_opy_
            bstack1lllll1l1l_opy_.add(r[0])
            self.logger.debug(bstack1111_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥፉ") + str(bstack1l1llll1111_opy_) + bstack1111_opy_ (u"ࠥࠦፊ"))
        if self.bstack1lll1l1lll_opy_():
            self.logger.debug(bstack1111_opy_ (u"ࠦ࠲࠳ࠢፋ"))
            self.logger.debug(bstack1111_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧፌ") + str(bstack1ll111l1l11_opy_) + bstack1111_opy_ (u"ࠨࠢፍ"))
        else:
            self.logger.debug(bstack1111_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦፎ") + str(bstack1ll111lllll_opy_) + bstack1111_opy_ (u"ࠣࠤፏ"))
        self.logger.debug(bstack1111_opy_ (u"ࠤ࠰࠱ࠧፐ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪፑ"), bstack1111_opy_ (u"ࠫ࠵࠭ፒ"))),
            client_worker_id=bstack1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦፓ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1lll111l111_opy_:
            self.logger.error(bstack1111_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥፔ"))
            return None
        response = self.bstack1lll111l111_opy_.TestOrchestration(request)
        self.logger.debug(bstack1111_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤፕ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll11l111l1_opy_(self, r):
        if r is not None and getattr(r, bstack1111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩፖ"), None) and getattr(r.testhub, bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩፗ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤፘ")))
            for bstack1l1ll1lllll_opy_, err in errors.items():
                if err[bstack1111_opy_ (u"ࠫࡹࡿࡰࡦࠩፙ")] == bstack1111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪፚ"):
                    self.logger.info(err[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ፛")])
                else:
                    self.logger.error(err[bstack1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ፜")])
    def bstack1ll1lll1l_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()