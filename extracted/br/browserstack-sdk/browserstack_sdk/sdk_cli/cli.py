# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
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
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l11_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1ll1l11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll1ll_opy_ import bstack1ll1111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11lllll1_opy_ import bstack1ll1l111l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1ll111l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1111l1_opy_ import bstack1l1ll1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11111_opy_ import bstack1l11l11111_opy_, bstack11ll111111_opy_, bstack111l1ll1l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll11l1l1l1_opy_ import bstack1ll111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import bstack1ll1ll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l111_opy_ import bstack1ll11lll1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l111ll_opy_ import bstack1l1ll111l_opy_
from bstack_utils.helper import Notset, bstack1lllll1l11l_opy_, get_cli_dir, bstack1lllll11lll_opy_, bstack11lll1111l_opy_, bstack1l11l11ll1_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1lllllll1_opy_, bstack1ll11l111ll_opy_, bstack1l1lllll1ll_opy_, bstack1l1lll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import bstack1ll1l1ll1ll_opy_, bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack111ll1111l_opy_ import bstack11l111ll1_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111l1l11ll_opy_, bstack111ll111_opy_
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll111l11l1_opy_())
def bstack1l1lll1lll1_opy_(bs_config):
    bstack1ll11lll111_opy_ = None
    bstack1llll1lllll_opy_ = None
    try:
        bstack1llll1lllll_opy_ = get_cli_dir()
        bstack1ll11lll111_opy_ = bstack1lllll11lll_opy_(bstack1llll1lllll_opy_)
        bstack1ll11llll1l_opy_ = bstack1lllll1l11l_opy_(bstack1ll11lll111_opy_, bstack1llll1lllll_opy_, bs_config)
        bstack1ll11lll111_opy_ = bstack1ll11llll1l_opy_ if bstack1ll11llll1l_opy_ else bstack1ll11lll111_opy_
        if not bstack1ll11lll111_opy_:
            raise ValueError(bstack11l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦᇩ"))
    except Exception as ex:
        logger.debug(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦᇪ").format(ex))
        bstack1ll11lll111_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧᇫ"))
        if bstack1ll11lll111_opy_:
            logger.debug(bstack11l11_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨᇬ") + str(bstack1ll11lll111_opy_) + bstack11l11_opy_ (u"ࠦࠧᇭ"))
        else:
            logger.debug(bstack11l11_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣᇮ"))
    return bstack1ll11lll111_opy_, bstack1llll1lllll_opy_
bstack1ll11111l11_opy_ = bstack11l11_opy_ (u"ࠨ࠹࠺࠻࠼ࠦᇯ")
bstack1l1llll1l1l_opy_ = bstack11l11_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨᇰ")
bstack1ll11ll1l11_opy_ = bstack11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᇱ")
bstack1ll11ll11ll_opy_ = bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢᇲ")
bstack111l1l11_opy_ = bstack11l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᇳ")
bstack1ll111l1ll1_opy_ = re.compile(bstack11l11_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥᇴ"))
bstack1l1llll1ll1_opy_ = bstack11l11_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥᇵ")
bstack1ll111ll1l1_opy_ = bstack11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡏࡓࡅࡈࡣࡋࡇࡌࡍࡄࡄࡇࡐࠨᇶ")
bstack1ll11l1l1ll_opy_ = [
    bstack11ll111111_opy_.bstack1l1llllll1_opy_,
    bstack11ll111111_opy_.CONNECT,
    bstack11ll111111_opy_.bstack11l1l111l1_opy_,
]
class SDKCLI:
    _1ll11111lll_opy_ = None
    process: Union[None, Any]
    bstack1ll1l1l11l1_opy_: bool
    bstack1ll111lllll_opy_: bool
    bstack1ll11l1l111_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll11lll1ll_opy_: Union[None, grpc.Channel]
    bstack1l1lll1ll1l_opy_: str
    test_framework: TestFramework
    bstack1lll1111l1l_opy_: bstack1ll1ll11l11_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l1ll11l_opy_: bstack1ll11ll1lll_opy_
    accessibility: bstack1ll1111ll11_opy_
    bstack1l11l111ll_opy_: bstack1l1ll111l_opy_
    ai: bstack1ll1l11l11l_opy_
    bstack1ll11ll111l_opy_: bstack1ll1l11l1l1_opy_
    bstack1ll1111llll_opy_: List[bstack1l1ll1lll11_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll111l1111_opy_: Any
    bstack1l1ll1ll1l1_opy_: Dict[str, timedelta]
    bstack1ll1l11l1ll_opy_: str
    bstack1lll111lll1_opy_: bstack1lll11l111l_opy_
    def __new__(cls):
        if not cls._1ll11111lll_opy_:
            cls._1ll11111lll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll11111lll_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1l1l11l1_opy_ = False
        self.bstack1ll11lll1ll_opy_ = None
        self.bstack1ll1l1l1lll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll11ll11ll_opy_, None)
        self.bstack1ll1l1l1l1l_opy_ = os.environ.get(bstack1ll11ll1l11_opy_, bstack11l11_opy_ (u"ࠢࠣᇷ")) == bstack11l11_opy_ (u"ࠣࠤᇸ")
        self.bstack1ll111lllll_opy_ = False
        self.bstack1ll11l1l111_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll111l1111_opy_ = None
        self.test_framework = None
        self.bstack1lll1111l1l_opy_ = None
        self.bstack1l1lll1ll1l_opy_=bstack11l11_opy_ (u"ࠤࠥᇹ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.bstack1ll111l11l1_opy_())
        self.bstack1l1ll1ll1l1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lll111lll1_opy_ = bstack1lll11l111l_opy_()
        self.bstack1ll11l1ll11_opy_ = False
        self.bstack1ll1111ll1l_opy_ = None
        self.bstack1ll111l1l1l_opy_ = None
        self.bstack1ll1l1ll11l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1111llll_opy_ = []
    def bstack1ll111l11_opy_(self):
        return os.environ.get(bstack111l1l11_opy_).lower().__eq__(bstack11l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᇺ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll111ll1l1_opy_, bstack11l11_opy_ (u"ࠫࠬᇻ")).lower() in [bstack11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪᇼ"), bstack11l11_opy_ (u"࠭࠱ࠨᇽ"), bstack11l11_opy_ (u"ࠧࡺࡧࡶࠫᇾ")]:
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡈࡲࡶࡨ࡯࡮ࡨࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡵࡤࡦࠢࡧࡹࡪࠦࡴࡰࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠤᇿ"))
            os.environ[bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧሀ")] = bstack11l11_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤሁ")
            return False
        if bstack11l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨሂ") in config and str(config[bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩሃ")]).lower() != bstack11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬሄ"):
            return False
        bstack1ll1l1111ll_opy_ = [bstack11l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢህ"), bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧሆ")]
        if is_robot_playwright_installed():
            bstack1ll1l1111ll_opy_.append(bstack11l11_opy_ (u"ࠤࡵࡳࡧࡵࡴࠣሇ"))
            bstack1ll1l1111ll_opy_.append(bstack11l11_opy_ (u"ࠥࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠦለ"))
        bstack1ll11l11l11_opy_ = config.get(bstack11l11_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢሉ")) in bstack1ll1l1111ll_opy_ or os.environ.get(bstack11l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ሊ")) in bstack1ll1l1111ll_opy_
        os.environ[bstack11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤላ")] = str(bstack1ll11l11l11_opy_) # bstack1l1lll111l1_opy_ bstack1ll111l11ll_opy_ VAR to bstack1ll1l1l1111_opy_ is binary running
        return bstack1ll11l11l11_opy_
    def bstack1l1l11ll1l_opy_(self):
        for event in bstack1ll11l1l1ll_opy_:
            bstack1l11l11111_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l11l11111_opy_.logger.debug(bstack11l11_opy_ (u"ࠢࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂࠦ࠽࠿ࠢࡾࡥࡷ࡭ࡳࡾࠢࠥሌ") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤል"))
            )
        bstack1l11l11111_opy_.register(bstack11ll111111_opy_.bstack1l1llllll1_opy_, self.__1ll111111ll_opy_)
        bstack1l11l11111_opy_.register(bstack11ll111111_opy_.CONNECT, self.__1l1ll1lllll_opy_)
        bstack1l11l11111_opy_.register(bstack11ll111111_opy_.bstack11l1l111l1_opy_, self.__1ll1l111111_opy_)
        bstack1l11l11111_opy_.register(bstack11ll111111_opy_.bstack111111l1l_opy_, self.__1ll1111l1ll_opy_)
    def bstack11111l1l_opy_(self):
        return not self.bstack1ll1l1l1l1l_opy_ and os.environ.get(bstack1ll11ll1l11_opy_, bstack11l11_opy_ (u"ࠤࠥሎ")) != bstack11l11_opy_ (u"ࠥࠦሏ")
    def is_running(self):
        if self.bstack1ll1l1l1l1l_opy_:
            return self.bstack1ll1l1l11l1_opy_
        else:
            return bool(self.bstack1ll11lll1ll_opy_)
    def bstack1l1ll1ll11l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1111llll_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1l1ll1ll1ll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1ll11lll11l_opy_(self, bstack1ll11l111l1_opy_=10):
        if self.bstack1ll1l1l1lll_opy_:
            return
        bstack1lllll111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll11ll11ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11l11_opy_ (u"ࠦࡠࠨሐ") + str(id(self)) + bstack11l11_opy_ (u"ࠧࡣࠠࡤࡱࡱࡲࡪࡩࡴࡪࡰࡪࠦሑ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11l11_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡡࡳࡶࡴࡾࡹࠣሒ"), 0), (bstack11l11_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡶࡣࡵࡸ࡯ࡹࡻࠥሓ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll11l111l1_opy_)
        self.bstack1ll11lll1ll_opy_ = channel
        self.bstack1ll1l1l1lll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll11lll1ll_opy_)
        self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺࠢሔ"), datetime.now() - bstack1lllll111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll11ll11ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11l11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧ࠾ࠥ࡯ࡳࡠࡥ࡫࡭ࡱࡪ࡟ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤሕ") + str(self.bstack11111l1l_opy_()) + bstack11l11_opy_ (u"ࠥࠦሖ"))
    def __1ll1l111111_opy_(self, event_name):
        if self.bstack11111l1l_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡄࡎࡌࠦሗ"))
        self.__1ll11l1111l_opy_()
    @measure(event_name=EVENTS.bstack1ll111ll11l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1ll1111l1ll_opy_(self, event_name, bstack1l1lll11l11_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack11l11_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠧመ"))
        bstack1ll1l1ll111_opy_ = Path(bstack1ll1lllll11_opy_ (u"ࠨࡻࡴࡧ࡯ࡪ࠳ࡩ࡬ࡪࡡࡧ࡭ࡷࢃ࠯ࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࡴ࠰࡭ࡷࡴࡴࠢሙ"))
        if self.bstack1llll1lllll_opy_ and bstack1ll1l1ll111_opy_.exists():
            with open(bstack1ll1l1ll111_opy_, bstack11l11_opy_ (u"ࠧࡳࠩሚ"), encoding=bstack11l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧማ")) as fp:
                data = json.load(fp)
                try:
                    bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧሜ"), bstack11l111ll1_opy_(bstack1ll11l1ll_opy_), data, {
                        bstack11l11_opy_ (u"ࠪࡥࡺࡺࡨࠨም"): (self.config[bstack11l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ሞ")], self.config[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨሟ")])
                    })
                except Exception as e:
                    logger.debug(bstack111ll111_opy_.format(str(e)))
            bstack1ll1l1ll111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll11l1l11l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1ll111111ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
        self.bstack1l1lll1ll1l_opy_, self.bstack1llll1lllll_opy_ = bstack1l1lll1lll1_opy_(data.bs_config)
        os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡝ࡒࡊࡖࡄࡆࡑࡋ࡟ࡅࡋࡕࠫሠ")] = self.bstack1llll1lllll_opy_
        if not self.bstack1l1lll1ll1l_opy_ or not self.bstack1llll1lllll_opy_:
            raise ValueError(bstack11l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠨሡ"))
        if self.bstack11111l1l_opy_():
            self.__1l1ll1lllll_opy_(event_name, bstack111l1ll1l_opy_())
            return
        try:
            logger.debug(bstack11l11_opy_ (u"ࠣࡅࡲࡱࡵࡲࡥࡵࡧࠣࡗࡉࡑࠠࡔࡧࡷࡹࡵ࠴ࠢሢ"))
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡿࢂࠨሣ").format(e))
        start = datetime.now()
        is_started = self.__1ll11ll11l1_opy_()
        self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠥࡷࡵࡧࡷ࡯ࡡࡷ࡭ࡲ࡫ࠢሤ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll11lll11l_opy_()
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥሥ"), datetime.now() - start)
            start = datetime.now()
            self.__1l1lll1ll11_opy_(data)
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥሦ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l1lll1111l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1l1ll1lllll_opy_(self, event_name: str, data: bstack111l1ll1l_opy_):
        if not self.bstack11111l1l_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࡳࡵࡴࠡࡣࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥሧ"))
            return
        bin_session_id = os.environ.get(bstack1ll11ll1l11_opy_)
        start = datetime.now()
        self.__1ll11lll11l_opy_()
        self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨረ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡆࡐࡎࠦࠢሩ") + str(bin_session_id) + bstack11l11_opy_ (u"ࠤࠥሪ"))
        start = datetime.now()
        self.__1l1lll1l1l1_opy_()
        self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣራ"), datetime.now() - start)
    def __1ll11l1ll1l_opy_(self):
        if not self.bstack1ll1l1l1lll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠ࡮ࡱࡧࡹࡱ࡫ࡳࠣሬ"))
            return
        bstack1l1llllll1l_opy_ = {
            bstack11l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤር"): (bstack1ll111l111l_opy_, bstack1l1ll1ll111_opy_, bstack1l1lllll11l_opy_),
            bstack11l11_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣሮ"): (bstack1ll1111lll1_opy_, bstack1ll1l111l11_opy_, bstack1l1llllllll_opy_),
        }
        if not self.bstack1ll1111ll1l_opy_ and self.session_framework in bstack1l1llllll1l_opy_:
            bstack1ll111ll111_opy_, bstack1l1llll1111_opy_, bstack1ll11llllll_opy_ = bstack1l1llllll1l_opy_[self.session_framework]
            bstack1ll1l11lll1_opy_ = bstack1l1llll1111_opy_()
            self.bstack1ll111l1l1l_opy_ = bstack1ll1l11lll1_opy_
            self.bstack1ll1111ll1l_opy_ = bstack1ll11llllll_opy_
            self.bstack1ll1111llll_opy_.append(bstack1ll1l11lll1_opy_)
            self.bstack1ll1111llll_opy_.append(bstack1ll111ll111_opy_(self.bstack1ll111l1l1l_opy_))
        if not self.bstack1ll1l1ll11l_opy_ and self.config_observability and self.config_observability.success: # bstack1l1llll1lll_opy_
            self.bstack1ll1l1ll11l_opy_ = bstack1ll11ll1lll_opy_(self.bstack1ll1111ll1l_opy_, self.bstack1ll111l1l1l_opy_) # bstack1l1lllll1l1_opy_
            self.bstack1ll1111llll_opy_.append(self.bstack1ll1l1ll11l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1111ll11_opy_(self.bstack1ll1111ll1l_opy_, self.bstack1ll111l1l1l_opy_)
            self.bstack1ll1111llll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11l11_opy_ (u"ࠢࡴࡧ࡯ࡪࡍ࡫ࡡ࡭ࠤሯ"), False) == True:
            self.ai = bstack1ll1l11l11l_opy_()
            self.bstack1ll1111llll_opy_.append(self.ai)
        if not self.percy and self.bstack1ll111l1111_opy_ and self.bstack1ll111l1111_opy_.success:
            self.percy = bstack1ll1l11l1l1_opy_(self.bstack1ll111l1111_opy_)
            self.bstack1ll1111llll_opy_.append(self.percy)
        for mod in self.bstack1ll1111llll_opy_:
            if not mod.bstack1ll11111ll1_opy_():
                mod.configure(self.bstack1ll1l1l1lll_opy_, self.config, self.cli_bin_session_id, self.bstack1lll111lll1_opy_)
    def __1l1lll11111_opy_(self):
        for mod in self.bstack1ll1111llll_opy_:
            if mod.bstack1ll11111ll1_opy_():
                mod.configure(self.bstack1ll1l1l1lll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1l11111l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1l1lll1ll11_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll111lllll_opy_:
            return
        self.__1ll11l11111_opy_(data)
        bstack1lllll111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣሰ")
        req.sdk_language = bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤሱ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll111l1ll1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪሲ"), bstack11l11_opy_ (u"ࠫ࠵࠭ሳ")))
            req.client_worker_id = bstack11l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦሴ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡧࡨ࡮ࡴࡧࠡࡹࡲࡶࡰ࡫ࡲࠡࡣࡱࡨࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡰࡧࡩࡽࡀࠠࡼࡿࠥስ").format(e))
        try:
            self.logger.debug(bstack11l11_opy_ (u"ࠢ࡜ࠤሶ") + str(id(self)) + bstack11l11_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢሷ"))
            r = self.bstack1ll1l1l1lll_opy_.StartBinSession(req)
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦሸ"), datetime.now() - bstack1lllll111_opy_)
            os.environ[bstack1ll11ll1l11_opy_] = r.bin_session_id
            self.__1ll111l1lll_opy_(r)
            self.__1ll11l1ll1l_opy_()
            if not self.bstack1ll11l1ll11_opy_:
                self.bstack1lll111lll1_opy_.start()
                self.bstack1ll11l1ll11_opy_ = True
                atexit.register(self.__1ll1111111l_opy_)
            self.bstack1ll111lllll_opy_ = True
            self.logger.debug(bstack11l11_opy_ (u"ࠥ࡟ࠧሹ") + str(id(self)) + bstack11l11_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤሺ"))
        except grpc.bstack1ll11l1lll1_opy_ as bstack1ll11l11ll1_opy_:
            self.logger.error(bstack11l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሻ") + str(bstack1ll11l11ll1_opy_) + bstack11l11_opy_ (u"ࠨࠢሼ"))
            traceback.print_exc()
            raise bstack1ll11l11ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦሽ") + str(e) + bstack11l11_opy_ (u"ࠣࠤሾ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll1lll1l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1l1lll1l1l1_opy_(self):
        if not self.bstack11111l1l_opy_() or not self.cli_bin_session_id or self.bstack1ll11l1l111_opy_:
            return
        bstack1lllll111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩሿ"), bstack11l11_opy_ (u"ࠪ࠴ࠬቀ")))
        req.client_worker_id = bstack11l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥቁ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡡࠢቂ") + str(id(self)) + bstack11l11_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣቃ"))
            r = self.bstack1ll1l1l1lll_opy_.ConnectBinSession(req)
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦቄ"), datetime.now() - bstack1lllll111_opy_)
            self.__1ll111l1lll_opy_(r)
            self.__1ll11l1ll1l_opy_()
            if not self.bstack1ll11l1ll11_opy_:
                self.bstack1lll111lll1_opy_.start()
                self.bstack1ll11l1ll11_opy_ = True
                atexit.register(self.__1ll1111111l_opy_)
            self.bstack1ll11l1l111_opy_ = True
            self.logger.debug(bstack11l11_opy_ (u"ࠣ࡝ࠥቅ") + str(id(self)) + bstack11l11_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣቆ"))
        except grpc.bstack1ll11l1lll1_opy_ as bstack1ll11l11ll1_opy_:
            self.logger.error(bstack11l11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧቇ") + str(bstack1ll11l11ll1_opy_) + bstack11l11_opy_ (u"ࠦࠧቈ"))
            traceback.print_exc()
            raise bstack1ll11l11ll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ቉") + str(e) + bstack11l11_opy_ (u"ࠨࠢቊ"))
            traceback.print_exc()
            raise e
    def __1ll111l1lll_opy_(self, r):
        self.bstack1ll1l1l111l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11l11_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨቋ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11l11_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨቌ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦቍ")
        self.bstack1ll111l1111_opy_ = getattr(r, bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ቎"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ቏")] = self.config_testhub.jwt
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪቐ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1l1lll11lll_opy_ = json.loads(r.config)
            bstack1ll1l1l11ll_opy_ = bstack1l1lll11lll_opy_.get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪቑ"), {}).get(bstack11l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩቒ"), bstack11l11_opy_ (u"ࠨࠩቓ"))
            os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫቔ")] = bstack1ll1l1l11ll_opy_
    def bstack1ll1111l111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1l1l11l1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1ll1l1lll_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1ll1l1lll_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll1111l111_opy_(event_name=EVENTS.bstack1l1lll11ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1ll11ll11l1_opy_(self, bstack1ll11l111l1_opy_=10):
        if self.bstack1ll1l1l11l1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡷࡹࡧࡲࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠧቕ"))
            return True
        self.logger.debug(bstack11l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥቖ"))
        if os.getenv(bstack11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡇࡑ࡚ࠧ቗")) == bstack1l1llll1ll1_opy_:
            self.cli_bin_session_id = bstack1l1llll1ll1_opy_
            self.cli_listen_addr = bstack11l11_opy_ (u"ࠨࡵ࡯࡫ࡻ࠾࠴ࡺ࡭ࡱ࠱ࡶࡨࡰ࠳ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠮ࠧࡶ࠲ࡸࡵࡣ࡬ࠤቘ") % (self.cli_bin_session_id)
            self.bstack1ll1l1l11l1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1lll1ll1l_opy_, bstack11l11_opy_ (u"ࠢࡴࡦ࡮ࠦ቙")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1l111ll1_opy_ compat for text=True in bstack1ll111llll1_opy_ python
            encoding=bstack11l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቚ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll11llll11_opy_ = threading.Thread(target=self.__1ll11ll1ll1_opy_, args=(bstack1ll11l111l1_opy_,))
        bstack1ll11llll11_opy_.start()
        bstack1ll11llll11_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11l11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡵࡳࡥࡼࡴ࠺ࠡࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦࡿࠣࡳࡺࡺ࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡴࡶࡧࡳࡺࡺ࠮ࡳࡧࡤࡨ࠭࠯ࡽࠡࡧࡵࡶࡂࠨቛ") + str(self.process.stderr.read()) + bstack11l11_opy_ (u"ࠥࠦቜ"))
        if not self.bstack1ll1l1l11l1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡠࠨቝ") + str(id(self)) + bstack11l11_opy_ (u"ࠧࡣࠠࡤ࡮ࡨࡥࡳࡻࡰࠣ቞"))
            self.__1ll11l1111l_opy_()
        self.logger.debug(bstack11l11_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡶࡲࡰࡥࡨࡷࡸࡥࡲࡦࡣࡧࡽ࠿ࠦࠢ቟") + str(self.bstack1ll1l1l11l1_opy_) + bstack11l11_opy_ (u"ࠢࠣበ"))
        return self.bstack1ll1l1l11l1_opy_
    def __1ll11ll1ll1_opy_(self, bstack1l1lllll111_opy_=10):
        bstack1ll1l11llll_opy_ = time.time()
        while self.process and time.time() - bstack1ll1l11llll_opy_ < bstack1l1lllll111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11l11_opy_ (u"ࠣ࡫ࡧࡁࠧቡ") in line:
                    self.cli_bin_session_id = line.split(bstack11l11_opy_ (u"ࠤ࡬ࡨࡂࠨቢ"))[-1:][0].strip()
                    self.logger.debug(bstack11l11_opy_ (u"ࠥࡧࡱ࡯࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠻ࠤባ") + str(self.cli_bin_session_id) + bstack11l11_opy_ (u"ࠦࠧቤ"))
                    continue
                if bstack11l11_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨብ") in line:
                    self.cli_listen_addr = line.split(bstack11l11_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢቦ"))[-1:][0].strip()
                    self.logger.debug(bstack11l11_opy_ (u"ࠢࡤ࡮࡬ࡣࡱ࡯ࡳࡵࡧࡱࡣࡦࡪࡤࡳ࠼ࠥቧ") + str(self.cli_listen_addr) + bstack11l11_opy_ (u"ࠣࠤቨ"))
                    continue
                if bstack11l11_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣቩ") in line:
                    port = line.split(bstack11l11_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤቪ"))[-1:][0].strip()
                    self.logger.debug(bstack11l11_opy_ (u"ࠦࡵࡵࡲࡵ࠼ࠥቫ") + str(port) + bstack11l11_opy_ (u"ࠧࠨቬ"))
                    continue
                if line.strip() == bstack1l1llll1l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11l11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡏࡏࡠࡕࡗࡖࡊࡇࡍࠣቭ"), bstack11l11_opy_ (u"ࠢ࠲ࠤቮ")) == bstack11l11_opy_ (u"ࠣ࠳ࠥቯ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1l1l11l1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11l11_opy_ (u"ࠤࡨࡶࡷࡵࡲ࠻ࠢࠥተ") + str(e) + bstack11l11_opy_ (u"ࠥࠦቱ"))
        return False
    def __1ll1111111l_opy_(self):
        bstack11l11_opy_ (u"ࠦࠧࠨࡃ࡭ࡧࡤࡲࡺࡶࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࡨࡲࡶࠥࡧࡳࡺࡰࡦࡣࡩ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲ࠭ࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡧࡴࡦࡺ࡬ࡸࠥࡺ࡯ࠡࡧࡱࡷࡺࡸࡥࠡࡶࡤࡷࡰࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠥࠦࠧቲ")
        if self.bstack1lll111lll1_opy_ and self.bstack1ll11l1ll11_opy_:
            try:
                self.bstack1lll111lll1_opy_.stop()
                self.bstack1ll11l1ll11_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1ll11l1llll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1ll11l1111l_opy_(self):
        if self.bstack1ll11lll1ll_opy_:
            if self.bstack1lll111lll1_opy_ and self.bstack1ll11l1ll11_opy_:
                try:
                    atexit.unregister(self.__1ll1111111l_opy_)
                except ValueError:
                    pass
                self.bstack1lll111lll1_opy_.stop()
                self.bstack1ll11l1ll11_opy_ = False
            start = datetime.now()
            if self.bstack1l1lll1l1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll11l1l111_opy_:
                    self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤታ"), datetime.now() - start)
                else:
                    self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥቴ"), datetime.now() - start)
            self.__1l1lll11111_opy_()
            start = datetime.now()
            bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(bstack11l11_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࠧት"))
            self.bstack1ll11lll1ll_opy_.close()
            bstack111l1lllll_opy_.end(bstack11l11_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࠨቶ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤቷ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣቸ"), True, None, None, None, None)
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠦࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨቹ"), datetime.now() - start)
            self.bstack1ll11lll1ll_opy_ = None
        if self.process:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡹࡴࡰࡲࠥቺ"))
            start = datetime.now()
            bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(bstack11l11_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺࡬࡫࡯ࡰࠧቻ"))
            self.process.terminate()
            bstack111l1lllll_opy_.end(bstack11l11_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻࡭࡬ࡰࡱࠨቼ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣች"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢቾ"), True, None, None, None, None)
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠥ࡯࡮ࡲ࡬ࡠࡶ࡬ࡱࡪࠨቿ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll1l1l1l1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1lllll1l1l_opy_()
                self.logger.info(
                    bstack11l11_opy_ (u"࡛ࠦ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠦኀ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫኁ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1l1l11l1_opy_ = False
    def __1ll11l11111_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11l11_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣኂ")] = selenium.__version__
            data.frameworks.append(bstack11l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤኃ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧኄ")] = __version__
            data.frameworks.append(bstack11l11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨኅ"))
        except:
            pass
    def bstack1ll1l111l1l_opy_(self, hub_url: str, platform_index: int, bstack1111ll1ll1_opy_: Any):
        if self.bstack1lll1111l1l_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢኆ"))
            return
        try:
            bstack1lllll111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11l11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨኇ")
            self.bstack1lll1111l1l_opy_ = bstack1l1llllllll_opy_(
                cli.config.get(bstack11l11_opy_ (u"ࠧ࡮ࡵࡣࡗࡵࡰࠧኈ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1l1llll111l_opy_={bstack11l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥ኉"): bstack1111ll1ll1_opy_}
            )
            def bstack1ll11111l1l_opy_(self):
                return
            if self.config.get(bstack11l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤኊ"), True):
                Service.start = bstack1ll11111l1l_opy_
                Service.stop = bstack1ll11111l1l_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1l1ll111l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll11lll1l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤኋ"), datetime.now() - bstack1lllll111_opy_)
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣኌ") + str(e) + bstack11l11_opy_ (u"ࠥࠦኍ"))
    def bstack1ll1111l11l_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l111lll_opy_
            self.bstack1lll1111l1l_opy_ = bstack1l1lllll11l_opy_(
                platform_index,
                framework_name=bstack11l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ኎"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࠨ኏") + str(e) + bstack11l11_opy_ (u"ࠨࠢነ"))
            pass
    def bstack1ll11l11lll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤኑ"))
            return
        if bstack11lll1111l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣኒ"): pytest.__version__ }, [bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨና")], self.bstack1lll111lll1_opy_, self.bstack1ll1l1l1lll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll111lll1l_opy_({ bstack11l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥኔ"): pytest.__version__ }, [bstack11l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦን")], self.bstack1lll111lll1_opy_, self.bstack1ll1l1l1lll_opy_)
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤኖ") + str(e) + bstack11l11_opy_ (u"ࠨࠢኗ"))
        self.bstack1ll11ll1l1l_opy_()
    def bstack1ll11ll1l1l_opy_(self):
        if not self.bstack1ll111l11_opy_():
            return
        bstack1l111l1ll1_opy_ = None
        def bstack1l111llll1_opy_(config, startdir):
            return bstack11l11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧኘ").format(bstack11l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢኙ"))
        def bstack1l1l1ll1l1_opy_():
            return
        def bstack11l1ll1l1l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩኚ"):
                return bstack11l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤኛ")
            else:
                return bstack1l111l1ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l111l1ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l111llll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1ll1l1_opy_
            Config.getoption = bstack11l1ll1l1l_opy_
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨኜ") + str(e) + bstack11l11_opy_ (u"ࠧࠨኝ"))
    def bstack1ll1l1l1ll1_opy_(self):
        bstack11lllll1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11lllll1_opy_, dict):
            if cli.config_observability:
                bstack11lllll1_opy_.update(
                    {bstack11l11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨኞ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥኟ") in accessibility.get(bstack11l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤአ"), {}):
                    bstack1ll1l11ll11_opy_ = accessibility.get(bstack11l11_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥኡ"))
                    bstack1ll1l11ll11_opy_.update({ bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦኢ"): bstack1ll1l11ll11_opy_.pop(bstack11l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢኣ")) })
                bstack11lllll1_opy_.update({bstack11l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧኤ"): accessibility })
        return bstack11lllll1_opy_
    @measure(event_name=EVENTS.bstack1ll1l11l111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1lll1l1ll_opy_(self, bstack1l1lll111ll_opy_: str = None, bstack1l1llll1l11_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1l1l1lll_opy_:
            return
        bstack1lllll111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭እ"), bstack11l11_opy_ (u"ࠧ࠱ࠩኦ")))
        req.client_worker_id = bstack11l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢኧ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1l1lll111ll_opy_:
            req.bstack1l1lll111ll_opy_ = bstack1l1lll111ll_opy_
        if bstack1l1llll1l11_opy_:
            req.bstack1l1llll1l11_opy_ = bstack1l1llll1l11_opy_
        try:
            r = self.bstack1ll1l1l1lll_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡲࡴࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥከ"), datetime.now() - bstack1lllll111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1lll1ll1_opy_(self, key: str, value: timedelta):
        tag = bstack11l11_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥኩ") if self.bstack11111l1l_opy_() else bstack11l11_opy_ (u"ࠦࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࠥኪ")
        self.bstack1l1ll1ll1l1_opy_[bstack11l11_opy_ (u"ࠧࡀࠢካ").join([tag + bstack11l11_opy_ (u"ࠨ࠭ࠣኬ") + str(id(self)), key])] += value
    def bstack1lllll1l1l_opy_(self):
        if not os.getenv(bstack11l11_opy_ (u"ࠢࡅࡇࡅ࡙ࡌࡥࡐࡆࡔࡉࠦክ"), bstack11l11_opy_ (u"ࠣ࠲ࠥኮ")) == bstack11l11_opy_ (u"ࠤ࠴ࠦኯ"):
            return
        bstack1ll1l1l1l11_opy_ = dict()
        bstack1lll111l1l1_opy_ = []
        if self.test_framework:
            bstack1lll111l1l1_opy_.extend(list(self.test_framework.bstack1lll111l1l1_opy_.values()))
        if self.bstack1lll1111l1l_opy_:
            bstack1lll111l1l1_opy_.extend(list(self.bstack1lll1111l1l_opy_.bstack1lll111l1l1_opy_.values()))
        for instance in bstack1lll111l1l1_opy_:
            if not instance.platform_index in bstack1ll1l1l1l11_opy_:
                bstack1ll1l1l1l11_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll1l1l1l11_opy_[instance.platform_index]
            for k, v in instance.bstack1ll11ll1111_opy_().items():
                report[k] += v
                report[k.split(bstack11l11_opy_ (u"ࠥ࠾ࠧኰ"))[0]] += v
        bstack1l1ll1llll1_opy_ = sorted([(k, v) for k, v in self.bstack1l1ll1ll1l1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1l111lll_opy_ = 0
        for r in bstack1l1ll1llll1_opy_:
            bstack1l1llllll11_opy_ = r[1].total_seconds()
            bstack1ll1l111lll_opy_ += bstack1l1llllll11_opy_
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻ࡽࡵ࡟࠵ࡣࡽ࠾ࠤ኱") + str(bstack1l1llllll11_opy_) + bstack11l11_opy_ (u"ࠧࠨኲ"))
        self.logger.debug(bstack11l11_opy_ (u"ࠨ࠭࠮ࠤኳ"))
        bstack1ll11l11l1l_opy_ = []
        for platform_index, report in bstack1ll1l1l1l11_opy_.items():
            bstack1ll11l11l1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll11l11l1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1111llll1l_opy_ = set()
        bstack1ll111lll11_opy_ = 0
        for r in bstack1ll11l11l1l_opy_:
            bstack1l1llllll11_opy_ = r[2].total_seconds()
            bstack1ll111lll11_opy_ += bstack1l1llllll11_opy_
            bstack1111llll1l_opy_.add(r[0])
            self.logger.debug(bstack11l11_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࡼࡴ࡞࠴ࡢࢃ࠺ࡼࡴ࡞࠵ࡢࢃ࠽ࠣኴ") + str(bstack1l1llllll11_opy_) + bstack11l11_opy_ (u"ࠣࠤኵ"))
        if self.bstack11111l1l_opy_():
            self.logger.debug(bstack11l11_opy_ (u"ࠤ࠰࠱ࠧ኶"))
            self.logger.debug(bstack11l11_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࡼࡶࡲࡸࡦࡲ࡟ࡤ࡮࡬ࢁࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠳ࡻࡴࡶࡵࠬࡵࡲࡡࡵࡨࡲࡶࡲࡹࠩࡾ࠿ࠥ኷") + str(bstack1ll111lll11_opy_) + bstack11l11_opy_ (u"ࠦࠧኸ"))
        else:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤኹ") + str(bstack1ll1l111lll_opy_) + bstack11l11_opy_ (u"ࠨࠢኺ"))
        self.logger.debug(bstack11l11_opy_ (u"ࠢ࠮࠯ࠥኻ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨኼ"), bstack11l11_opy_ (u"ࠩ࠳ࠫኽ"))),
            client_worker_id=bstack11l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤኾ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1l1l1lll_opy_:
            self.logger.error(bstack11l11_opy_ (u"ࠦࡨࡲࡩࡠࡵࡨࡶࡻ࡯ࡣࡦࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ኿"))
            return None
        response = self.bstack1ll1l1l1lll_opy_.TestOrchestration(request)
        self.logger.debug(bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶ࠰ࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠰ࡷࡪࡹࡳࡪࡱࡱࡁࢀࢃࠢዀ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1l1l111l_opy_(self, r):
        if r is not None and getattr(r, bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࠧ዁"), None) and getattr(r.testhub, bstack11l11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧዂ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢዃ")))
            for bstack1ll1l11ll1l_opy_, err in errors.items():
                if err[bstack11l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧዄ")] == bstack11l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨዅ"):
                    self.logger.info(err[bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ዆")])
                else:
                    self.logger.error(err[bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭዇")])
    def bstack11l11ll1l_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()