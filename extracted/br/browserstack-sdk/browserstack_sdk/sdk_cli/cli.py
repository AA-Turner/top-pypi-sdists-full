# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
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
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll11llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1ll11l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1l1llll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111ll1_opy_ import bstack1ll111111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1l1l1_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1l1l_opy_ import bstack1ll1l11llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll111_opy_ import bstack1ll1l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack11l1l1l11_opy_, bstack1lllllll1_opy_, bstack1l1111l1l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll11ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111l11_opy_ import bstack1l1lllll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1111ll_opy_ import bstack1ll11l1l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l111_opy_ import bstack1ll11l1ll_opy_
from bstack_utils.helper import Notset, bstack1lllll1ll11_opy_, get_cli_dir, bstack1llllll11l1_opy_, bstack1llll1ll1_opy_, bstack11l11llll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1llllll1l_opy_, bstack1l1llll111l_opy_, bstack1ll11lll1ll_opy_, bstack1ll11l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1ll1llll111_opy_, bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1ll1l11ll_opy_ import bstack11l11lll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1111l1_opy_, bstack1l1111lll1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1111l11l_opy_())
def bstack1ll1l1111l1_opy_(bs_config):
    bstack1ll1111111l_opy_ = None
    bstack1llllll1111_opy_ = None
    try:
        bstack1llllll1111_opy_ = get_cli_dir()
        bstack1ll1111111l_opy_ = bstack1llllll11l1_opy_(bstack1llllll1111_opy_)
        bstack1ll1ll1111l_opy_ = bstack1lllll1ll11_opy_(bstack1ll1111111l_opy_, bstack1llllll1111_opy_, bs_config)
        bstack1ll1111111l_opy_ = bstack1ll1ll1111l_opy_ if bstack1ll1ll1111l_opy_ else bstack1ll1111111l_opy_
        if not bstack1ll1111111l_opy_:
            raise ValueError(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨᇲ"))
    except Exception as ex:
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡰࡦࡺࡥࡴࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡿࢂࠨᇳ").format(ex))
        bstack1ll1111111l_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠢᇴ"))
        if bstack1ll1111111l_opy_:
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡷࡵ࡭ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࡀࠠࠣᇵ") + str(bstack1ll1111111l_opy_) + bstack11l1l11_opy_ (u"ࠨࠢᇶ"))
        else:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡏࡱࠣࡺࡦࡲࡩࡥࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࡀࠦࡳࡦࡶࡸࡴࠥࡳࡡࡺࠢࡥࡩࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠥᇷ"))
    return bstack1ll1111111l_opy_, bstack1llllll1111_opy_
bstack1ll1l1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠣ࠻࠼࠽࠾ࠨᇸ")
bstack1ll1ll111l1_opy_ = bstack11l1l11_opy_ (u"ࠤࡵࡩࡦࡪࡹࠣᇹ")
bstack1l1lll1l11l_opy_ = bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᇺ")
bstack1ll1l11l1l1_opy_ = bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡑࡏࡓࡕࡇࡑࡣࡆࡊࡄࡓࠤᇻ")
bstack1l1111111_opy_ = bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᇼ")
bstack1ll11l11l11_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡸࠢࠩࡁ࡬࠭࠳࠰ࠨࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࢂࡂࡔࠫ࠱࠮ࠧᇽ"))
bstack1ll11lll11l_opy_ = bstack11l1l11_opy_ (u"ࠢࡥࡧࡹࡩࡱࡵࡰ࡮ࡧࡱࡸࠧᇾ")
bstack1ll11lllll1_opy_ = bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡑࡕࡇࡊࡥࡆࡂࡎࡏࡆࡆࡉࡋࠣᇿ")
bstack1ll1l111ll1_opy_ = [
    bstack1lllllll1_opy_.bstack111l11ll_opy_,
    bstack1lllllll1_opy_.CONNECT,
    bstack1lllllll1_opy_.bstack1l111l1ll1_opy_,
]
class SDKCLI:
    _1ll1l11l111_opy_ = None
    process: Union[None, Any]
    bstack1ll1l1llll1_opy_: bool
    bstack1ll1l1l1111_opy_: bool
    bstack1ll1l111l1l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll11l111ll_opy_: Union[None, grpc.Channel]
    bstack1ll1l1lllll_opy_: str
    test_framework: TestFramework
    bstack1lll11111l1_opy_: bstack1lll11ll1l1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll11l1ll1l_opy_: bstack1ll1l1l1lll_opy_
    accessibility: bstack1ll11l11ll1_opy_
    bstack1l1l1l111_opy_: bstack1ll11l1ll_opy_
    ai: bstack1l1llll1l1l_opy_
    bstack1ll1111llll_opy_: bstack1ll111111l1_opy_
    bstack1ll1111ll1l_opy_: List[bstack1ll11llll11_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll11ll1lll_opy_: Any
    bstack1ll111l1l11_opy_: Dict[str, timedelta]
    bstack1l1lllll11l_opy_: str
    bstack1lll1l11111_opy_: bstack1lll11llll1_opy_
    def __new__(cls):
        if not cls._1ll1l11l111_opy_:
            cls._1ll1l11l111_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1l11l111_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1l1llll1_opy_ = False
        self.bstack1ll11l111ll_opy_ = None
        self.bstack1ll1ll11111_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1l11l1l1_opy_, None)
        self.bstack1ll11ll1111_opy_ = os.environ.get(bstack1l1lll1l11l_opy_, bstack11l1l11_opy_ (u"ࠤࠥሀ")) == bstack11l1l11_opy_ (u"ࠥࠦሁ")
        self.bstack1ll1l1l1111_opy_ = False
        self.bstack1ll1l111l1l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll11ll1lll_opy_ = None
        self.test_framework = None
        self.bstack1lll11111l1_opy_ = None
        self.bstack1ll1l1lllll_opy_=bstack11l1l11_opy_ (u"ࠦࠧሂ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.bstack1ll1111l11l_opy_())
        self.bstack1ll111l1l11_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lll1l11111_opy_ = bstack1lll11llll1_opy_()
        self.bstack1ll1l11ll11_opy_ = False
        self.bstack1ll11l1llll_opy_ = None
        self.bstack1l1llll1l11_opy_ = None
        self.bstack1ll11l1ll1l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1111ll1l_opy_ = []
    def bstack1lll1l1l_opy_(self):
        return os.environ.get(bstack1l1111111_opy_).lower().__eq__(bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥሃ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll11lllll1_opy_, bstack11l1l11_opy_ (u"࠭ࠧሄ")).lower() in [bstack11l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬህ"), bstack11l1l11_opy_ (u"ࠨ࠳ࠪሆ"), bstack11l1l11_opy_ (u"ࠩࡼࡩࡸ࠭ሇ")]:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡊࡴࡸࡣࡪࡰࡪࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡰࡦࡨࠤࡩࡻࡥࠡࡶࡲࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠦለ"))
            os.environ[bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢሉ")] = bstack11l1l11_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦሊ")
            return False
        if bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪላ") in config and str(config[bstack11l1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫሌ")]).lower() != bstack11l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧል"):
            return False
        bstack1ll11l1l11l_opy_ = [bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤሎ"), bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢሏ"), bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠧሐ")]
        if is_robot_playwright_installed():
            bstack1ll11l1l11l_opy_.append(bstack11l1l11_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦሑ"))
            bstack1ll11l1l11l_opy_.append(bstack11l1l11_opy_ (u"ࠨࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠢሒ"))
        bstack1ll11111l1l_opy_ = config.get(bstack11l1l11_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥሓ")) in bstack1ll11l1l11l_opy_ or os.environ.get(bstack11l1l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩሔ")) in bstack1ll11l1l11l_opy_
        os.environ[bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧሕ")] = str(bstack1ll11111l1l_opy_) # bstack1ll1l11lll1_opy_ bstack1ll1l1ll111_opy_ VAR to bstack1ll111ll11l_opy_ is binary running
        return bstack1ll11111l1l_opy_
    def bstack11ll1ll1_opy_(self):
        for event in bstack1ll1l111ll1_opy_:
            bstack11l1l1l11_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11l1l1l11_opy_.logger.debug(bstack11l1l11_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨሖ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧሗ"))
            )
        bstack11l1l1l11_opy_.register(bstack1lllllll1_opy_.bstack111l11ll_opy_, self.__1ll111111ll_opy_)
        bstack11l1l1l11_opy_.register(bstack1lllllll1_opy_.CONNECT, self.__1ll1ll1l111_opy_)
        bstack11l1l1l11_opy_.register(bstack1lllllll1_opy_.bstack1l111l1ll1_opy_, self.__1ll1111l1ll_opy_)
        bstack11l1l1l11_opy_.register(bstack1lllllll1_opy_.bstack1l1111ll1l_opy_, self.__1ll1l1l1l11_opy_)
    def bstack1lll11l1l_opy_(self):
        return not self.bstack1ll11ll1111_opy_ and os.environ.get(bstack1l1lll1l11l_opy_, bstack11l1l11_opy_ (u"ࠧࠨመ")) != bstack11l1l11_opy_ (u"ࠨࠢሙ")
    def is_running(self):
        if self.bstack1ll11ll1111_opy_:
            return self.bstack1ll1l1llll1_opy_
        else:
            return bool(self.bstack1ll11l111ll_opy_)
    def bstack1l1lll1l1ll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1111ll1l_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll11111lll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll111l111l_opy_(self, bstack1ll11l1111l_opy_=10):
        if self.bstack1ll1ll11111_opy_:
            return
        bstack111l11l1l1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1l11l1l1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࠤሚ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢማ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11l1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦሜ"), 0), (bstack11l1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨም"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll11l1111l_opy_)
        self.bstack1ll11l111ll_opy_ = channel
        self.bstack1ll1ll11111_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll11l111ll_opy_)
        self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥሞ"), datetime.now() - bstack111l11l1l1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1l11l1l1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧሟ") + str(self.bstack1lll11l1l_opy_()) + bstack11l1l11_opy_ (u"ࠨࠢሠ"))
    def __1ll1111l1ll_opy_(self, event_name):
        if self.bstack1lll11l1l_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢሡ"))
        self.__1ll11llll1l_opy_()
    @measure(event_name=EVENTS.bstack1ll1l1ll11l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll1l1l1l11_opy_(self, event_name, bstack1ll1l111l11_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣሢ"))
        bstack1ll111l11ll_opy_ = Path(bstack1lll11l11ll_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥሣ"))
        if self.bstack1llllll1111_opy_ and bstack1ll111l11ll_opy_.exists():
            with open(bstack1ll111l11ll_opy_, bstack11l1l11_opy_ (u"ࠪࡶࠬሤ"), encoding=bstack11l1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪሥ")) as fp:
                data = json.load(fp)
                try:
                    bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪሦ"), bstack11l11lll_opy_(bstack1l1111lll_opy_), data, {
                        bstack11l1l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫሧ"): (self.config[bstack11l1l11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩረ")], self.config[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫሩ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1111lll1_opy_.format(str(e)))
            bstack1ll111l11ll_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll1ll11ll1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll111111ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
        self.bstack1ll1l1lllll_opy_, self.bstack1llllll1111_opy_ = bstack1ll1l1111l1_opy_(data.bs_config)
        os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧሪ")] = self.bstack1llllll1111_opy_
        if not self.bstack1ll1l1lllll_opy_ or not self.bstack1llllll1111_opy_:
            raise ValueError(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤራ"))
        if self.bstack1lll11l1l_opy_():
            self.__1ll1ll1l111_opy_(event_name, bstack1l1111l1l_opy_())
            return
        try:
            logger.debug(bstack11l1l11_opy_ (u"ࠦࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡓࡅࡍࠣࡗࡪࡺࡵࡱ࠰ࠥሬ"))
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤር").format(e))
        start = datetime.now()
        is_started = self.__1ll1l1l111l_opy_()
        self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠨࡳࡱࡣࡺࡲࡤࡺࡩ࡮ࡧࠥሮ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll111l111l_opy_()
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨሯ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1lll1l111_opy_(data)
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨሰ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll1l1l1l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll1ll1l111_opy_(self, event_name: str, data: bstack1l1111l1l_opy_):
        if not self.bstack1lll11l1l_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨሱ"))
            return
        bin_session_id = os.environ.get(bstack1l1lll1l11l_opy_)
        start = datetime.now()
        self.__1ll111l111l_opy_()
        self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤሲ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊࠢࠥሳ") + str(bin_session_id) + bstack11l1l11_opy_ (u"ࠧࠨሴ"))
        start = datetime.now()
        self.__1ll111l11l1_opy_()
        self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦስ"), datetime.now() - start)
    def __1ll11ll111l_opy_(self):
        if not self.bstack1ll1ll11111_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦሶ"))
            return
        bstack1l1llllllll_opy_ = {
            bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧሷ"): (bstack1ll1l11llll_opy_, bstack1ll1l11l11l_opy_, bstack1l1lllll1ll_opy_),
            bstack11l1l11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦሸ"): (bstack1ll111l1111_opy_, bstack1ll111lll1l_opy_, bstack1l1lllll1l1_opy_),
        }
        if not self.bstack1ll11l1llll_opy_ and self.session_framework in bstack1l1llllllll_opy_:
            bstack1l1lllllll1_opy_, bstack1ll11l1l1ll_opy_, bstack1ll111l1ll1_opy_ = bstack1l1llllllll_opy_[self.session_framework]
            bstack1ll1111l111_opy_ = bstack1ll11l1l1ll_opy_()
            self.bstack1l1llll1l11_opy_ = bstack1ll1111l111_opy_
            self.bstack1ll11l1llll_opy_ = bstack1ll111l1ll1_opy_
            self.bstack1ll1111ll1l_opy_.append(bstack1ll1111l111_opy_)
            self.bstack1ll1111ll1l_opy_.append(bstack1l1lllllll1_opy_(self.bstack1l1llll1l11_opy_))
        if not self.bstack1ll11l1ll1l_opy_ and self.config_observability and self.config_observability.success: # bstack1l1llll1ll1_opy_
            self.bstack1ll11l1ll1l_opy_ = bstack1ll1l1l1lll_opy_(self.bstack1ll11l1llll_opy_, self.bstack1l1llll1l11_opy_) # bstack1l1lll11lll_opy_
            self.bstack1ll1111ll1l_opy_.append(self.bstack1ll11l1ll1l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll11l11ll1_opy_(self.bstack1ll11l1llll_opy_, self.bstack1l1llll1l11_opy_)
            self.bstack1ll1111ll1l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧሹ"), False) == True:
            self.ai = bstack1l1llll1l1l_opy_()
            self.bstack1ll1111ll1l_opy_.append(self.ai)
        if not self.percy and self.bstack1ll11ll1lll_opy_ and self.bstack1ll11ll1lll_opy_.success:
            self.percy = bstack1ll111111l1_opy_(self.bstack1ll11ll1lll_opy_)
            self.bstack1ll1111ll1l_opy_.append(self.percy)
        for mod in self.bstack1ll1111ll1l_opy_:
            if not mod.bstack1ll1l11l1ll_opy_():
                mod.configure(self.bstack1ll1ll11111_opy_, self.config, self.cli_bin_session_id, self.bstack1lll1l11111_opy_)
    def __1ll11ll1ll1_opy_(self):
        for mod in self.bstack1ll1111ll1l_opy_:
            if mod.bstack1ll1l11l1ll_opy_():
                mod.configure(self.bstack1ll1ll11111_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll111llll1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1l1lll1l111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1l1l1111_opy_:
            return
        self.__1ll1ll111ll_opy_(data)
        bstack111l11l1l1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦሺ")
        req.sdk_language = bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧሻ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll11l11l11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ሼ"), bstack11l1l11_opy_ (u"ࠧ࠱ࠩሽ")))
            req.client_worker_id = bstack11l1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢሾ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡪࡤࡪࡰࡪࠤࡼࡵࡲ࡬ࡧࡵࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹ࠼ࠣࡿࢂࠨሿ").format(e))
        try:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࠧቀ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥቁ"))
            r = self.bstack1ll1ll11111_opy_.StartBinSession(req)
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢቂ"), datetime.now() - bstack111l11l1l1_opy_)
            os.environ[bstack1l1lll1l11l_opy_] = r.bin_session_id
            self.__1ll111ll1ll_opy_(r)
            self.__1ll11ll111l_opy_()
            if not self.bstack1ll1l11ll11_opy_:
                self.bstack1lll1l11111_opy_.start()
                self.bstack1ll1l11ll11_opy_ = True
                atexit.register(self.__1ll111lll11_opy_)
            self.bstack1ll1l1l1111_opy_ = True
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡛ࠣቃ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧቄ"))
        except grpc.bstack1l1llll11ll_opy_ as bstack1ll11ll1l11_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥቅ") + str(bstack1ll11ll1l11_opy_) + bstack11l1l11_opy_ (u"ࠤࠥቆ"))
            traceback.print_exc()
            raise bstack1ll11ll1l11_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢቇ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧቈ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll111ll1l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll111l11l1_opy_(self):
        if not self.bstack1lll11l1l_opy_() or not self.cli_bin_session_id or self.bstack1ll1l111l1l_opy_:
            return
        bstack111l11l1l1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ቉"), bstack11l1l11_opy_ (u"࠭࠰ࠨቊ")))
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨቋ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡝ࠥቌ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦቍ"))
            r = self.bstack1ll1ll11111_opy_.ConnectBinSession(req)
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢ቎"), datetime.now() - bstack111l11l1l1_opy_)
            self.__1ll111ll1ll_opy_(r)
            self.__1ll11ll111l_opy_()
            if not self.bstack1ll1l11ll11_opy_:
                self.bstack1lll1l11111_opy_.start()
                self.bstack1ll1l11ll11_opy_ = True
                atexit.register(self.__1ll111lll11_opy_)
            self.bstack1ll1l111l1l_opy_ = True
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡠࠨ቏") + str(id(self)) + bstack11l1l11_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦቐ"))
        except grpc.bstack1l1llll11ll_opy_ as bstack1ll11ll1l11_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቑ") + str(bstack1ll11ll1l11_opy_) + bstack11l1l11_opy_ (u"ࠢࠣቒ"))
            traceback.print_exc()
            raise bstack1ll11ll1l11_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧቓ") + str(e) + bstack11l1l11_opy_ (u"ࠤࠥቔ"))
            traceback.print_exc()
            raise e
    def __1ll111ll1ll_opy_(self, r):
        self.bstack1ll11l11111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11l1l11_opy_ (u"ࠥࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤቕ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11l1l11_opy_ (u"ࠦࡪࡳࡰࡵࡻࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡻ࡮ࡥࠤቖ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡩࡷࡩࡹࠡ࡫ࡶࠤࡸ࡫࡮ࡵࠢࡲࡲࡱࡿࠠࡢࡵࠣࡴࡦࡸࡴࠡࡱࡩࠤࡹ࡮ࡥࠡࠤࡆࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠲ࠢࠡࡣࡱࡨࠥࡺࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡣ࡯ࡷࡴࠦࡵࡴࡧࡧࠤࡧࡿࠠࡔࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࡳࡧࡩࡳࡷ࡫ࠬࠡࡐࡲࡲࡪࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡ࡫ࡶࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ቗")
        self.bstack1ll11ll1lll_opy_ = getattr(r, bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬቘ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ቙")] = self.config_testhub.jwt
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ቚ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1lll1ll11_opy_ = json.loads(r.config)
            bstack1l1lll1lll1_opy_ = bstack1l1lll1ll11_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ቛ"), {}).get(bstack11l1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬቜ"), bstack11l1l11_opy_ (u"ࠫࠬቝ"))
            os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ቞")] = bstack1l1lll1lll1_opy_
    def bstack1ll1l1lll11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1l1llll1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll1111l1l1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll1111l1l1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll1l1lll11_opy_(event_name=EVENTS.bstack1ll11lll1l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll1l1l111l_opy_(self, bstack1ll11l1111l_opy_=10):
        if self.bstack1ll1l1llll1_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣ቟"))
            return True
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨበ"))
        if os.getenv(bstack11l1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣቡ")) == bstack1ll11lll11l_opy_:
            self.cli_bin_session_id = bstack1ll11lll11l_opy_
            self.cli_listen_addr = bstack11l1l11_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧቢ") % (self.cli_bin_session_id)
            self.bstack1ll1l1llll1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1ll1l1lllll_opy_, bstack11l1l11_opy_ (u"ࠥࡷࡩࡱࠢባ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll11l1l111_opy_ compat for text=True in bstack1l1llll1lll_opy_ python
            encoding=bstack11l1l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥቤ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1l11ll1l_opy_ = threading.Thread(target=self.__1ll1l1ll1l1_opy_, args=(bstack1ll11l1111l_opy_,))
        bstack1ll1l11ll1l_opy_.start()
        bstack1ll1l11ll1l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤብ") + str(self.process.stderr.read()) + bstack11l1l11_opy_ (u"ࠨࠢቦ"))
        if not self.bstack1ll1l1llll1_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࠤቧ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦቨ"))
            self.__1ll11llll1l_opy_()
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥቩ") + str(self.bstack1ll1l1llll1_opy_) + bstack11l1l11_opy_ (u"ࠥࠦቪ"))
        return self.bstack1ll1l1llll1_opy_
    def __1ll1l1ll1l1_opy_(self, bstack1ll11ll11ll_opy_=10):
        bstack1ll11l1ll11_opy_ = time.time()
        while self.process and time.time() - bstack1ll11l1ll11_opy_ < bstack1ll11ll11ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11l1l11_opy_ (u"ࠦ࡮ࡪ࠽ࠣቫ") in line:
                    self.cli_bin_session_id = line.split(bstack11l1l11_opy_ (u"ࠧ࡯ࡤ࠾ࠤቬ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧቭ") + str(self.cli_bin_session_id) + bstack11l1l11_opy_ (u"ࠢࠣቮ"))
                    continue
                if bstack11l1l11_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤቯ") in line:
                    self.cli_listen_addr = line.split(bstack11l1l11_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥተ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨቱ") + str(self.cli_listen_addr) + bstack11l1l11_opy_ (u"ࠦࠧቲ"))
                    continue
                if bstack11l1l11_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦታ") in line:
                    port = line.split(bstack11l1l11_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧቴ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨት") + str(port) + bstack11l1l11_opy_ (u"ࠣࠤቶ"))
                    continue
                if line.strip() == bstack1ll1ll111l1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11l1l11_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦቷ"), bstack11l1l11_opy_ (u"ࠥ࠵ࠧቸ")) == bstack11l1l11_opy_ (u"ࠦ࠶ࠨቹ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1l1llll1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨቺ") + str(e) + bstack11l1l11_opy_ (u"ࠨࠢቻ"))
        return False
    def __1ll111lll11_opy_(self):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࡆࡰࡪࡧ࡮ࡶࡲࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡫ࡵࡲࠡࡣࡶࡽࡳࡩ࡟ࡥ࡫ࡶࡴࡦࡺࡣࡩࡧࡵ࠰ࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡣࡷࡩࡽ࡯ࡴࠡࡶࡲࠤࡪࡴࡳࡶࡴࡨࠤࡹࡧࡳ࡬ࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨࠢࠣቼ")
        if self.bstack1lll1l11111_opy_ and self.bstack1ll1l11ll11_opy_:
            try:
                self.bstack1lll1l11111_opy_.stop()
                self.bstack1ll1l11ll11_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1lll1llll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def __1ll11llll1l_opy_(self):
        if self.bstack1ll11l111ll_opy_:
            if self.bstack1lll1l11111_opy_ and self.bstack1ll1l11ll11_opy_:
                try:
                    atexit.unregister(self.__1ll111lll11_opy_)
                except ValueError:
                    pass
                self.bstack1lll1l11111_opy_.stop()
                self.bstack1ll1l11ll11_opy_ = False
            start = datetime.now()
            if self.bstack1ll1ll11l11_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll1l111l1l_opy_:
                    self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧች"), datetime.now() - start)
                else:
                    self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨቾ"), datetime.now() - start)
            self.__1ll11ll1ll1_opy_()
            start = datetime.now()
            bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(bstack11l1l11_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࠣቿ"))
            self.bstack1ll11l111ll_opy_.close()
            bstack11ll1l1l1_opy_.end(bstack11l1l11_opy_ (u"ࠦࡸࡪ࡫࠻ࡥ࡯࡭࠿ࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࠤኀ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧኁ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦኂ"), True, None, None, None, None)
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠢࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤኃ"), datetime.now() - start)
            self.bstack1ll11l111ll_opy_ = None
        if self.process:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡷࡳࡵࠨኄ"))
            start = datetime.now()
            bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(bstack11l1l11_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽࡯࡮ࡲ࡬ࠣኅ"))
            self.process.terminate()
            bstack11ll1l1l1_opy_.end(bstack11l1l11_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡰ࡯࡬࡭ࠤኆ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦኇ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥኈ"), True, None, None, None, None)
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠨ࡫ࡪ࡮࡯ࡣࡹ࡯࡭ࡦࠤ኉"), datetime.now() - start)
            self.process = None
            if self.bstack1ll11ll1111_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11l1l11ll1_opy_()
                self.logger.info(
                    bstack11l1l11_opy_ (u"ࠢࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠢኊ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧኋ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1l1llll1_opy_ = False
    def __1ll1ll111ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11l1l11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦኌ")] = selenium.__version__
            data.frameworks.append(bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧኍ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ኎")] = __version__
            data.frameworks.append(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ኏"))
        except:
            pass
    def bstack1l1llll1111_opy_(self, hub_url: str, platform_index: int, bstack11ll1l11ll_opy_: Any):
        if self.bstack1lll11111l1_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥነ"))
            return
        try:
            bstack111l11l1l1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11l1l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤኑ")
            self.bstack1lll11111l1_opy_ = bstack1l1lllll1l1_opy_(
                cli.config.get(bstack11l1l11_opy_ (u"ࠣࡪࡸࡦ࡚ࡸ࡬ࠣኒ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll111l1l1l_opy_={bstack11l1l11_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨና"): bstack11ll1l11ll_opy_}
            )
            def bstack1ll1l111lll_opy_(self):
                return
            if self.config.get(bstack11l1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠧኔ"), True):
                Service.start = bstack1ll1l111lll_opy_
                Service.stop = bstack1ll1l111lll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1ll11l1ll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll11l1l1l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠧን"), datetime.now() - bstack111l11l1l1_opy_)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠼ࠣࠦኖ") + str(e) + bstack11l1l11_opy_ (u"ࠨࠢኗ"))
    def bstack1ll11lll111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1ll1l111l_opy_
            self.bstack1lll11111l1_opy_ = bstack1l1lllll1ll_opy_(
                platform_index,
                framework_name=bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦኘ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࠤኙ") + str(e) + bstack11l1l11_opy_ (u"ࠤࠥኚ"))
            pass
    def bstack1ll11llllll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧኛ"))
            return
        if bstack1llll1ll1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦኜ"): pytest.__version__ }, [bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤኝ")], self.bstack1lll1l11111_opy_, self.bstack1ll1ll11111_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll11ll11l1_opy_({ bstack11l1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨኞ"): pytest.__version__ }, [bstack11l1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢኟ")], self.bstack1lll1l11111_opy_, self.bstack1ll1ll11111_opy_)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࠧአ") + str(e) + bstack11l1l11_opy_ (u"ࠤࠥኡ"))
        self.bstack1ll1111lll1_opy_()
    def bstack1ll1111lll1_opy_(self):
        if not self.bstack1lll1l1l_opy_():
            return
        bstack1l11l1ll1_opy_ = None
        def bstack11llll11ll_opy_(config, startdir):
            return bstack11l1l11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣኢ").format(bstack11l1l11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥኣ"))
        def bstack1l11111ll1_opy_():
            return
        def bstack1l1l111l1_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11l1l11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬኤ"):
                return bstack11l1l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧእ")
            else:
                return bstack1l11l1ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l11l1ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11llll11ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11111ll1_opy_
            Config.getoption = bstack1l1l111l1_opy_
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡳࡽࡹ࡫ࡳࡵࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࡫ࡵࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠺ࠡࠤኦ") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤኧ"))
    def bstack1ll1l1l11ll_opy_(self):
        bstack1lllllll1l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1lllllll1l_opy_, dict):
            if cli.config_observability:
                bstack1lllllll1l_opy_.update(
                    {bstack11l1l11_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤከ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11l1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨኩ") in accessibility.get(bstack11l1l11_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧኪ"), {}):
                    bstack1l1llllll11_opy_ = accessibility.get(bstack11l1l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨካ"))
                    bstack1l1llllll11_opy_.update({ bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠢኬ"): bstack1l1llllll11_opy_.pop(bstack11l1l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥክ")) })
                bstack1lllllll1l_opy_.update({bstack11l1l11_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣኮ"): accessibility })
        return bstack1lllllll1l_opy_
    @measure(event_name=EVENTS.bstack1ll1l1lll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1ll1ll11l11_opy_(self, bstack1ll1l111111_opy_: str = None, bstack1l1lll11ll1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1ll11111_opy_:
            return
        bstack111l11l1l1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩኯ"), bstack11l1l11_opy_ (u"ࠪ࠴ࠬኰ")))
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ኱").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll1l111111_opy_:
            req.bstack1ll1l111111_opy_ = bstack1ll1l111111_opy_
        if bstack1l1lll11ll1_opy_:
            req.bstack1l1lll11ll1_opy_ = bstack1l1lll11ll1_opy_
        try:
            r = self.bstack1ll1ll11111_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡵࡰࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨኲ"), datetime.now() - bstack111l11l1l1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11l1lllll1_opy_(self, key: str, value: timedelta):
        tag = bstack11l1l11_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨኳ") if self.bstack1lll11l1l_opy_() else bstack11l1l11_opy_ (u"ࠢ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࠨኴ")
        self.bstack1ll111l1l11_opy_[bstack11l1l11_opy_ (u"ࠣ࠼ࠥኵ").join([tag + bstack11l1l11_opy_ (u"ࠤ࠰ࠦ኶") + str(id(self)), key])] += value
    def bstack11l1l11ll1_opy_(self):
        if not os.getenv(bstack11l1l11_opy_ (u"ࠥࡈࡊࡈࡕࡈࡡࡓࡉࡗࡌࠢ኷"), bstack11l1l11_opy_ (u"ࠦ࠵ࠨኸ")) == bstack11l1l11_opy_ (u"ࠧ࠷ࠢኹ"):
            return
        bstack1ll11111111_opy_ = dict()
        bstack1ll1ll1ll1l_opy_ = []
        if self.test_framework:
            bstack1ll1ll1ll1l_opy_.extend(list(self.test_framework.bstack1ll1ll1ll1l_opy_.values()))
        if self.bstack1lll11111l1_opy_:
            bstack1ll1ll1ll1l_opy_.extend(list(self.bstack1lll11111l1_opy_.bstack1ll1ll1ll1l_opy_.values()))
        for instance in bstack1ll1ll1ll1l_opy_:
            if not instance.platform_index in bstack1ll11111111_opy_:
                bstack1ll11111111_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll11111111_opy_[instance.platform_index]
            for k, v in instance.bstack1ll111l1lll_opy_().items():
                report[k] += v
                report[k.split(bstack11l1l11_opy_ (u"ࠨ࠺ࠣኺ"))[0]] += v
        bstack1ll11l11lll_opy_ = sorted([(k, v) for k, v in self.bstack1ll111l1l11_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1l11111l_opy_ = 0
        for r in bstack1ll11l11lll_opy_:
            bstack1ll1111ll11_opy_ = r[1].total_seconds()
            bstack1ll1l11111l_opy_ += bstack1ll1111ll11_opy_
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࢀࡸ࡛࠱࡟ࢀࡁࠧኻ") + str(bstack1ll1111ll11_opy_) + bstack11l1l11_opy_ (u"ࠣࠤኼ"))
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࠰࠱ࠧኽ"))
        bstack1l1lllll111_opy_ = []
        for platform_index, report in bstack1ll11111111_opy_.items():
            bstack1l1lllll111_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l1lllll111_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1ll111111_opy_ = set()
        bstack1ll11l11l1l_opy_ = 0
        for r in bstack1l1lllll111_opy_:
            bstack1ll1111ll11_opy_ = r[2].total_seconds()
            bstack1ll11l11l1l_opy_ += bstack1ll1111ll11_opy_
            bstack1ll111111_opy_.add(r[0])
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࡿࡷࡡ࠰࡞ࡿ࠽ࡿࡷࡡ࠱࡞ࡿࡀࠦኾ") + str(bstack1ll1111ll11_opy_) + bstack11l1l11_opy_ (u"ࠦࠧ኿"))
        if self.bstack1lll11l1l_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࠳࠭ࠣዀ"))
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࡀࡿࡹࡵࡴࡢ࡮ࡢࡧࡱ࡯ࡽࠡࡶࡨࡷࡹࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ࠯ࡾࡷࡹࡸࠨࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠬࢁࡂࠨ዁") + str(bstack1ll11l11l1l_opy_) + bstack11l1l11_opy_ (u"ࠢࠣዂ"))
        else:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࠧዃ") + str(bstack1ll1l11111l_opy_) + bstack11l1l11_opy_ (u"ࠤࠥዄ"))
        self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࠱࠲ࠨዅ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ዆"), bstack11l1l11_opy_ (u"ࠬ࠶ࠧ዇"))),
            client_worker_id=bstack11l1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧወ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1ll11111_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢࡤ࡮࡬ࡣࡸ࡫ࡲࡷ࡫ࡦࡩࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦዉ"))
            return None
        response = self.bstack1ll1ll11111_opy_.TestOrchestration(request)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹ࠳࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠳ࡳࡦࡵࡶ࡭ࡴࡴ࠽ࡼࡿࠥዊ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll11l11111_opy_(self, r):
        if r is not None and getattr(r, bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࠪዋ"), None) and getattr(r.testhub, bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪዌ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11l1l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥው")))
            for bstack1ll11l1lll1_opy_, err in errors.items():
                if err[bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪዎ")] == bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫዏ"):
                    self.logger.info(err[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨዐ")])
                else:
                    self.logger.error(err[bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩዑ")])
    def bstack11lll11lll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()