# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
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
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lll11lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1l11l_opy_ import bstack1ll11ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1ll111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11llll_opy_ import bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l111ll_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1lll_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1lll_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack111l1llll1_opy_ import bstack111l1llll1_opy_, bstack1l11lll1ll_opy_, bstack11ll1l11l1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll111111ll_opy_ import bstack1ll11l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1ll11l1111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1llll_opy_ import bstack1ll11ll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lllll11_opy_ import bstack11l1ll11l1_opy_
from bstack_utils.helper import Notset, bstack1lllll1ll1l_opy_, get_cli_dir, bstack1lllll1llll_opy_, bstack111l1lll_opy_, bstack1l1l11ll_opy_, is_robot_playwright_installed
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1ll1l111111_opy_, bstack1l1llll1l1l_opy_, bstack1ll1l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1lll1111_opy_, bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11ll1l11l_opy_ import bstack1l1l1111ll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l11111ll_opy_, bstack1lll11111_opy_
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1l11ll1l_opy_())
def bstack1ll11111ll1_opy_(bs_config):
    bstack1ll1l111lll_opy_ = None
    bstack1llllll1l11_opy_ = None
    try:
        bstack1llllll1l11_opy_ = get_cli_dir()
        bstack1ll1l111lll_opy_ = bstack1lllll1llll_opy_(bstack1llllll1l11_opy_)
        bstack1ll1l11lll1_opy_ = bstack1lllll1ll1l_opy_(bstack1ll1l111lll_opy_, bstack1llllll1l11_opy_, bs_config)
        bstack1ll1l111lll_opy_ = bstack1ll1l11lll1_opy_ if bstack1ll1l11lll1_opy_ else bstack1ll1l111lll_opy_
        if not bstack1ll1l111lll_opy_:
            raise ValueError(bstack11ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤᇮ"))
    except Exception as ex:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡬ࡢࡶࡨࡷࡹࠦࡢࡪࡰࡤࡶࡾࠦࡻࡾࠤᇯ").format(ex))
        bstack1ll1l111lll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥᇰ"))
        if bstack1ll1l111lll_opy_:
            logger.debug(bstack11ll111_opy_ (u"ࠣࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡳࡱࡰࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࠦᇱ") + str(bstack1ll1l111lll_opy_) + bstack11ll111_opy_ (u"ࠤࠥᇲ"))
        else:
            logger.debug(bstack11ll111_opy_ (u"ࠥࡒࡴࠦࡶࡢ࡮࡬ࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠼ࠢࡶࡩࡹࡻࡰࠡ࡯ࡤࡽࠥࡨࡥࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨᇳ"))
    return bstack1ll1l111lll_opy_, bstack1llllll1l11_opy_
bstack1l1lllll11l_opy_ = bstack11ll111_opy_ (u"ࠦ࠾࠿࠹࠺ࠤᇴ")
bstack1l1lll1ll1l_opy_ = bstack11ll111_opy_ (u"ࠧࡸࡥࡢࡦࡼࠦᇵ")
bstack1ll1l1l1l1l_opy_ = bstack11ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᇶ")
bstack1ll1l1111ll_opy_ = bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡍࡋࡖࡘࡊࡔ࡟ࡂࡆࡇࡖࠧᇷ")
bstack11ll11l11l_opy_ = bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦᇸ")
bstack1ll11111111_opy_ = re.compile(bstack11ll111_opy_ (u"ࡴࠥࠬࡄ࡯ࠩ࠯ࠬࠫࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡾࡅࡗ࠮࠴ࠪࠣᇹ"))
bstack1ll11l11lll_opy_ = bstack11ll111_opy_ (u"ࠥࡨࡪࡼࡥ࡭ࡱࡳࡱࡪࡴࡴࠣᇺ")
bstack1ll111llll1_opy_ = bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠦᇻ")
bstack1l1lll1l111_opy_ = [
    bstack1l11lll1ll_opy_.bstack11ll111l11_opy_,
    bstack1l11lll1ll_opy_.CONNECT,
    bstack1l11lll1ll_opy_.bstack1lllllll1_opy_,
]
class SDKCLI:
    _1ll1l1llll1_opy_ = None
    process: Union[None, Any]
    bstack1ll1ll1111l_opy_: bool
    bstack1ll1l1l1l11_opy_: bool
    bstack1l1lllllll1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll111l11ll_opy_: Union[None, grpc.Channel]
    bstack1l1lllll1l1_opy_: str
    test_framework: TestFramework
    bstack1lll11111ll_opy_: bstack1ll1ll1lll1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l11l11l_opy_: bstack1l1llll1l11_opy_
    accessibility: bstack1ll11l1ll11_opy_
    bstack1lllll11_opy_: bstack11l1ll11l1_opy_
    ai: bstack1ll11l11l11_opy_
    bstack1l1lllll1ll_opy_: bstack1ll11ll111l_opy_
    bstack1l1lll11ll1_opy_: List[bstack1ll1l1l11l1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll1111l1l1_opy_: Any
    bstack1ll1l1ll1l1_opy_: Dict[str, timedelta]
    bstack1ll11l1lll1_opy_: str
    bstack1lll11llll1_opy_: bstack1lll11lll11_opy_
    def __new__(cls):
        if not cls._1ll1l1llll1_opy_:
            cls._1ll1l1llll1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1l1llll1_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1ll1111l_opy_ = False
        self.bstack1ll111l11ll_opy_ = None
        self.bstack1l1llllll1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1l1111ll_opy_, None)
        self.bstack1l1lllll111_opy_ = os.environ.get(bstack1ll1l1l1l1l_opy_, bstack11ll111_opy_ (u"ࠧࠨᇼ")) == bstack11ll111_opy_ (u"ࠨࠢᇽ")
        self.bstack1ll1l1l1l11_opy_ = False
        self.bstack1l1lllllll1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll1111l1l1_opy_ = None
        self.test_framework = None
        self.bstack1lll11111ll_opy_ = None
        self.bstack1l1lllll1l1_opy_=bstack11ll111_opy_ (u"ࠢࠣᇾ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.bstack1ll1l11ll1l_opy_())
        self.bstack1ll1l1ll1l1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lll11llll1_opy_ = bstack1lll11lll11_opy_()
        self.bstack1ll111lll1l_opy_ = False
        self.bstack1ll11111l1l_opy_ = None
        self.bstack1l1llllll11_opy_ = None
        self.bstack1ll1l11l11l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l1lll11ll1_opy_ = []
    def bstack11l1llllll_opy_(self):
        return os.environ.get(bstack11ll11l11l_opy_).lower().__eq__(bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨᇿ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll111llll1_opy_, bstack11ll111_opy_ (u"ࠩࠪሀ")).lower() in [bstack11ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨሁ"), bstack11ll111_opy_ (u"ࠫ࠶࠭ሂ"), bstack11ll111_opy_ (u"ࠬࡿࡥࡴࠩሃ")]:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡆࡰࡴࡦ࡭ࡳ࡭ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡰࡳࡩ࡫ࠠࡥࡷࡨࠤࡹࡵࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡐࡔࡆࡉࡤࡌࡁࡍࡎࡅࡅࡈࡑࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠢሄ"))
            os.environ[bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥህ")] = bstack11ll111_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢሆ")
            return False
        if bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ሇ") in config and str(config[bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧለ")]).lower() != bstack11ll111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪሉ"):
            return False
        bstack1ll11l11111_opy_ = [bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧሊ"), bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥላ"), bstack11ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠣሌ")]
        if is_robot_playwright_installed():
            bstack1ll11l11111_opy_.append(bstack11ll111_opy_ (u"ࠣࡴࡲࡦࡴࡺࠢል"))
            bstack1ll11l11111_opy_.append(bstack11ll111_opy_ (u"ࠤࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠥሎ"))
        bstack1ll111l1l1l_opy_ = config.get(bstack11ll111_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨሏ")) in bstack1ll11l11111_opy_ or os.environ.get(bstack11ll111_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬሐ")) in bstack1ll11l11111_opy_
        os.environ[bstack11ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣሑ")] = str(bstack1ll111l1l1l_opy_) # bstack1ll1ll11ll1_opy_ bstack1l1lll1l1l1_opy_ VAR to bstack1ll11l11l1l_opy_ is binary running
        return bstack1ll111l1l1l_opy_
    def bstack11l11lllll_opy_(self):
        for event in bstack1l1lll1l111_opy_:
            bstack111l1llll1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack111l1llll1_opy_.logger.debug(bstack11ll111_opy_ (u"ࠨࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠥࡃ࠾ࠡࡽࡤࡶ࡬ࡹࡽࠡࠤሒ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣሓ"))
            )
        bstack111l1llll1_opy_.register(bstack1l11lll1ll_opy_.bstack11ll111l11_opy_, self.__1ll1ll111l1_opy_)
        bstack111l1llll1_opy_.register(bstack1l11lll1ll_opy_.CONNECT, self.__1ll11111l11_opy_)
        bstack111l1llll1_opy_.register(bstack1l11lll1ll_opy_.bstack1lllllll1_opy_, self.__1ll1111ll1l_opy_)
        bstack111l1llll1_opy_.register(bstack1l11lll1ll_opy_.bstack1ll1ll1ll_opy_, self.__1ll1l1l111l_opy_)
    def bstack1l11l1111_opy_(self):
        return not self.bstack1l1lllll111_opy_ and os.environ.get(bstack1ll1l1l1l1l_opy_, bstack11ll111_opy_ (u"ࠣࠤሔ")) != bstack11ll111_opy_ (u"ࠤࠥሕ")
    def is_running(self):
        if self.bstack1l1lllll111_opy_:
            return self.bstack1ll1ll1111l_opy_
        else:
            return bool(self.bstack1ll111l11ll_opy_)
    def bstack1ll11llllll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l1lll11ll1_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll1111lll1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll11l1l11l_opy_(self, bstack1ll11ll1lll_opy_=10):
        if self.bstack1l1llllll1l_opy_:
            return
        bstack11lll11111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1l1111ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࠧሖ") + str(id(self)) + bstack11ll111_opy_ (u"ࠦࡢࠦࡣࡰࡰࡱࡩࡨࡺࡩ࡯ࡩࠥሗ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡠࡲࡵࡳࡽࡿࠢመ"), 0), (bstack11ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡵࡢࡴࡷࡵࡸࡺࠤሙ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll11ll1lll_opy_)
        self.bstack1ll111l11ll_opy_ = channel
        self.bstack1l1llllll1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll111l11ll_opy_)
        self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࠨሚ"), datetime.now() - bstack11lll11111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1l1111ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦ࠽ࠤ࡮ࡹ࡟ࡤࡪ࡬ࡰࡩࡥࡰࡳࡱࡦࡩࡸࡹ࠽ࠣማ") + str(self.bstack1l11l1111_opy_()) + bstack11ll111_opy_ (u"ࠤࠥሜ"))
    def __1ll1111ll1l_opy_(self, event_name):
        if self.bstack1l11l1111_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡃࡍࡋࠥም"))
        self.__1l1llll1111_opy_()
    @measure(event_name=EVENTS.bstack1ll1111l11l_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll1l1l111l_opy_(self, event_name, bstack1ll111lll11_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠦሞ"))
        bstack1ll1l1ll111_opy_ = Path(bstack1lll11111l1_opy_ (u"ࠧࢁࡳࡦ࡮ࡩ࠲ࡨࡲࡩࡠࡦ࡬ࡶࢂ࠵ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࡳ࠯࡬ࡶࡳࡳࠨሟ"))
        if self.bstack1llllll1l11_opy_ and bstack1ll1l1ll111_opy_.exists():
            with open(bstack1ll1l1ll111_opy_, bstack11ll111_opy_ (u"࠭ࡲࠨሠ"), encoding=bstack11ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ሡ")) as fp:
                data = json.load(fp)
                try:
                    bstack1l1l11ll_opy_(bstack11ll111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ሢ"), bstack1l1l1111ll_opy_(bstack1l1l11l111_opy_), data, {
                        bstack11ll111_opy_ (u"ࠩࡤࡹࡹ࡮ࠧሣ"): (self.config[bstack11ll111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬሤ")], self.config[bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧሥ")])
                    })
                except Exception as e:
                    logger.debug(bstack1lll11111_opy_.format(str(e)))
            bstack1ll1l1ll111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1l1lll1ll11_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll1ll111l1_opy_(self, event_name: str, data):
        from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
        self.bstack1l1lllll1l1_opy_, self.bstack1llllll1l11_opy_ = bstack1ll11111ll1_opy_(data.bs_config)
        os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡜ࡘࡉࡕࡃࡅࡐࡊࡥࡄࡊࡔࠪሦ")] = self.bstack1llllll1l11_opy_
        if not self.bstack1l1lllll1l1_opy_ or not self.bstack1llllll1l11_opy_:
            raise ValueError(bstack11ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡪࡨࠤࡘࡊࡋࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠧሧ"))
        if self.bstack1l11l1111_opy_():
            self.__1ll11111l11_opy_(event_name, bstack11ll1l11l1_opy_())
            return
        try:
            logger.debug(bstack11ll111_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨረ"))
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧሩ").format(e))
        start = datetime.now()
        is_started = self.__1ll111l1l11_opy_()
        self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨሪ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll11l1l11l_opy_()
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤራ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll11l11ll1_opy_(data)
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤሬ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll1ll11111_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll11111l11_opy_(self, event_name: str, data: bstack11ll1l11l1_opy_):
        if not self.bstack1l11l1111_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤር"))
            return
        bin_session_id = os.environ.get(bstack1ll1l1l1l1l_opy_)
        start = datetime.now()
        self.__1ll11l1l11l_opy_()
        self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧሮ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨሯ") + str(bin_session_id) + bstack11ll111_opy_ (u"ࠣࠤሰ"))
        start = datetime.now()
        self.__1ll11lll1l1_opy_()
        self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢሱ"), datetime.now() - start)
    def __1ll11lll11l_opy_(self):
        if not self.bstack1l1llllll1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢሲ"))
            return
        bstack1ll1l1lllll_opy_ = {
            bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣሳ"): (bstack1ll11llll11_opy_, bstack1ll1l1ll1ll_opy_, bstack1ll11l1111l_opy_),
            bstack11ll111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢሴ"): (bstack1ll111ll1l1_opy_, bstack1ll11l1ll1l_opy_, bstack1ll1111ll11_opy_),
        }
        if not self.bstack1ll11111l1l_opy_ and self.session_framework in bstack1ll1l1lllll_opy_:
            bstack1l1llll1ll1_opy_, bstack1ll1ll11lll_opy_, bstack1ll1l11111l_opy_ = bstack1ll1l1lllll_opy_[self.session_framework]
            bstack1ll1111l111_opy_ = bstack1ll1ll11lll_opy_()
            self.bstack1l1llllll11_opy_ = bstack1ll1111l111_opy_
            self.bstack1ll11111l1l_opy_ = bstack1ll1l11111l_opy_
            self.bstack1l1lll11ll1_opy_.append(bstack1ll1111l111_opy_)
            self.bstack1l1lll11ll1_opy_.append(bstack1l1llll1ll1_opy_(self.bstack1l1llllll11_opy_))
        if not self.bstack1ll1l11l11l_opy_ and self.config_observability and self.config_observability.success: # bstack1ll11lll1ll_opy_
            self.bstack1ll1l11l11l_opy_ = bstack1l1llll1l11_opy_(self.bstack1ll11111l1l_opy_, self.bstack1l1llllll11_opy_) # bstack1l1lll1l1ll_opy_
            self.bstack1l1lll11ll1_opy_.append(self.bstack1ll1l11l11l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll11l1ll11_opy_(self.bstack1ll11111l1l_opy_, self.bstack1l1llllll11_opy_)
            self.bstack1l1lll11ll1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11ll111_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣስ"), False) == True:
            self.ai = bstack1ll11l11l11_opy_()
            self.bstack1l1lll11ll1_opy_.append(self.ai)
        if not self.percy and self.bstack1ll1111l1l1_opy_ and self.bstack1ll1111l1l1_opy_.success:
            self.percy = bstack1ll11ll111l_opy_(self.bstack1ll1111l1l1_opy_)
            self.bstack1l1lll11ll1_opy_.append(self.percy)
        for mod in self.bstack1l1lll11ll1_opy_:
            if not mod.bstack1l1lll11lll_opy_():
                mod.configure(self.bstack1l1llllll1l_opy_, self.config, self.cli_bin_session_id, self.bstack1lll11llll1_opy_)
    def __1ll11111lll_opy_(self):
        for mod in self.bstack1l1lll11ll1_opy_:
            if mod.bstack1l1lll11lll_opy_():
                mod.configure(self.bstack1l1llllll1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1l1lll11_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll11l11ll1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1l1l1l11_opy_:
            return
        self.__1ll1l111ll1_opy_(data)
        bstack11lll11111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢሶ")
        req.sdk_language = bstack11ll111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣሷ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll11111111_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩሸ"), bstack11ll111_opy_ (u"ࠪ࠴ࠬሹ")))
            req.client_worker_id = bstack11ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥሺ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡸࡱࡵ࡯ࡪࡸࠠࡢࡰࡧࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡩ࡯ࡦࡨࡼ࠿ࠦࡻࡾࠤሻ").format(e))
        try:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࠣሼ") + str(id(self)) + bstack11ll111_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨሽ"))
            r = self.bstack1l1llllll1l_opy_.StartBinSession(req)
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥሾ"), datetime.now() - bstack11lll11111_opy_)
            os.environ[bstack1ll1l1l1l1l_opy_] = r.bin_session_id
            self.__1ll1l11l1l1_opy_(r)
            self.__1ll11lll11l_opy_()
            if not self.bstack1ll111lll1l_opy_:
                self.bstack1lll11llll1_opy_.start()
                self.bstack1ll111lll1l_opy_ = True
                atexit.register(self.__1ll111ll111_opy_)
            self.bstack1ll1l1l1l11_opy_ = True
            self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡞ࠦሿ") + str(id(self)) + bstack11ll111_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣቀ"))
        except grpc.bstack1ll111l111l_opy_ as bstack1ll11lllll1_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቁ") + str(bstack1ll11lllll1_opy_) + bstack11ll111_opy_ (u"ࠧࠨቂ"))
            traceback.print_exc()
            raise bstack1ll11lllll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥቃ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣቄ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l1l1l1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll11lll1l1_opy_(self):
        if not self.bstack1l11l1111_opy_() or not self.cli_bin_session_id or self.bstack1l1lllllll1_opy_:
            return
        bstack11lll11111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨቅ"), bstack11ll111_opy_ (u"ࠩ࠳ࠫቆ")))
        req.client_worker_id = bstack11ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤቇ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡠࠨቈ") + str(id(self)) + bstack11ll111_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢ቉"))
            r = self.bstack1l1llllll1l_opy_.ConnectBinSession(req)
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥቊ"), datetime.now() - bstack11lll11111_opy_)
            self.__1ll1l11l1l1_opy_(r)
            self.__1ll11lll11l_opy_()
            if not self.bstack1ll111lll1l_opy_:
                self.bstack1lll11llll1_opy_.start()
                self.bstack1ll111lll1l_opy_ = True
                atexit.register(self.__1ll111ll111_opy_)
            self.bstack1l1lllllll1_opy_ = True
            self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡜ࠤቋ") + str(id(self)) + bstack11ll111_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢቌ"))
        except grpc.bstack1ll111l111l_opy_ as bstack1ll11lllll1_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦቍ") + str(bstack1ll11lllll1_opy_) + bstack11ll111_opy_ (u"ࠥࠦ቎"))
            traceback.print_exc()
            raise bstack1ll11lllll1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ቏") + str(e) + bstack11ll111_opy_ (u"ࠧࠨቐ"))
            traceback.print_exc()
            raise e
    def __1ll1l11l1l1_opy_(self, r):
        self.bstack1l1llllllll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11ll111_opy_ (u"ࠨࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧቑ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11ll111_opy_ (u"ࠢࡦ࡯ࡳࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡷࡱࡨࠧቒ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡥࡳࡥࡼࠤ࡮ࡹࠠࡴࡧࡱࡸࠥࡵ࡮࡭ࡻࠣࡥࡸࠦࡰࡢࡴࡷࠤࡴ࡬ࠠࡵࡪࡨࠤࠧࡉ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠮ࠥࠤࡦࡴࡤࠡࡶ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡦࡲࡳࡰࠢࡸࡷࡪࡪࠠࡣࡻࠣࡗࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡨࡶࡪ࡬࡯ࡳࡧ࠯ࠤࡓࡵ࡮ࡦࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤ࡮ࡹࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥቓ")
        self.bstack1ll1111l1l1_opy_ = getattr(r, bstack11ll111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨቔ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧቕ")] = self.config_testhub.jwt
        os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩቖ")] = self.config_testhub.build_hashed_id
        if is_robot_playwright_installed():
            bstack1ll11ll11ll_opy_ = json.loads(r.config)
            bstack1ll111111l1_opy_ = bstack1ll11ll11ll_opy_.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ቗"), {}).get(bstack11ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨቘ"), bstack11ll111_opy_ (u"ࠧࠨ቙"))
            os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪቚ")] = bstack1ll111111l1_opy_
    def bstack1ll11ll1l11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1ll1111l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll1l1ll11l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll1l1ll11l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll11ll1l11_opy_(event_name=EVENTS.bstack1l1llll1lll_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1ll111l1l11_opy_(self, bstack1ll11ll1lll_opy_=10):
        if self.bstack1ll1ll1111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡸࡦࡸࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠦቛ"))
            return True
        self.logger.debug(bstack11ll111_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤቜ"))
        if os.getenv(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡆࡐ࡙ࠦቝ")) == bstack1ll11l11lll_opy_:
            self.cli_bin_session_id = bstack1ll11l11lll_opy_
            self.cli_listen_addr = bstack11ll111_opy_ (u"ࠧࡻ࡮ࡪࡺ࠽࠳ࡹࡳࡰ࠰ࡵࡧ࡯࠲ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࠦࡵ࠱ࡷࡴࡩ࡫ࠣ቞") % (self.cli_bin_session_id)
            self.bstack1ll1ll1111l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l1lllll1l1_opy_, bstack11ll111_opy_ (u"ࠨࡳࡥ࡭ࠥ቟")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll111ll1ll_opy_ compat for text=True in bstack1ll11ll1ll1_opy_ python
            encoding=bstack11ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨበ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l1llll111l_opy_ = threading.Thread(target=self.__1ll111l1ll1_opy_, args=(bstack1ll11ll1lll_opy_,))
        bstack1l1llll111l_opy_.start()
        bstack1l1llll111l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡴࡲࡤࡻࡳࡀࠠࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥࡾࠢࡲࡹࡹࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡳࡵࡦࡲࡹࡹ࠴ࡲࡦࡣࡧࠬ࠮ࢃࠠࡦࡴࡵࡁࠧቡ") + str(self.process.stderr.read()) + bstack11ll111_opy_ (u"ࠤࠥቢ"))
        if not self.bstack1ll1ll1111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࠧባ") + str(id(self)) + bstack11ll111_opy_ (u"ࠦࡢࠦࡣ࡭ࡧࡤࡲࡺࡶࠢቤ"))
            self.__1l1llll1111_opy_()
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡵࡸ࡯ࡤࡧࡶࡷࡤࡸࡥࡢࡦࡼ࠾ࠥࠨብ") + str(self.bstack1ll1ll1111l_opy_) + bstack11ll111_opy_ (u"ࠨࠢቦ"))
        return self.bstack1ll1ll1111l_opy_
    def __1ll111l1ll1_opy_(self, bstack1ll1ll111ll_opy_=10):
        bstack1ll1l1lll1l_opy_ = time.time()
        while self.process and time.time() - bstack1ll1l1lll1l_opy_ < bstack1ll1ll111ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11ll111_opy_ (u"ࠢࡪࡦࡀࠦቧ") in line:
                    self.cli_bin_session_id = line.split(bstack11ll111_opy_ (u"ࠣ࡫ࡧࡁࠧቨ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll111_opy_ (u"ࠤࡦࡰ࡮ࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠣቩ") + str(self.cli_bin_session_id) + bstack11ll111_opy_ (u"ࠥࠦቪ"))
                    continue
                if bstack11ll111_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧቫ") in line:
                    self.cli_listen_addr = line.split(bstack11ll111_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨቬ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll111_opy_ (u"ࠨࡣ࡭࡫ࡢࡰ࡮ࡹࡴࡦࡰࡢࡥࡩࡪࡲ࠻ࠤቭ") + str(self.cli_listen_addr) + bstack11ll111_opy_ (u"ࠢࠣቮ"))
                    continue
                if bstack11ll111_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢቯ") in line:
                    port = line.split(bstack11ll111_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣተ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll111_opy_ (u"ࠥࡴࡴࡸࡴ࠻ࠤቱ") + str(port) + bstack11ll111_opy_ (u"ࠦࠧቲ"))
                    continue
                if line.strip() == bstack1l1lll1ll1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11ll111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡎࡕ࡟ࡔࡖࡕࡉࡆࡓࠢታ"), bstack11ll111_opy_ (u"ࠨ࠱ࠣቴ")) == bstack11ll111_opy_ (u"ࠢ࠲ࠤት"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1ll1111l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡧࡵࡶࡴࡸ࠺ࠡࠤቶ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥቷ"))
        return False
    def __1ll111ll111_opy_(self):
        bstack11ll111_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡱࡹࡵࠦࡨࡢࡰࡧࡰࡪࡸࠠࡧࡱࡵࠤࡦࡹࡹ࡯ࡥࡢࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࠬࠡࡥࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡦࡺࡥࡹ࡫ࡷࠤࡹࡵࠠࡦࡰࡶࡹࡷ࡫ࠠࡵࡣࡶ࡯ࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠤࠥࠦቸ")
        if self.bstack1lll11llll1_opy_ and self.bstack1ll111lll1l_opy_:
            try:
                self.bstack1lll11llll1_opy_.stop()
                self.bstack1ll111lll1l_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1l1lll1lll1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def __1l1llll1111_opy_(self):
        if self.bstack1ll111l11ll_opy_:
            if self.bstack1lll11llll1_opy_ and self.bstack1ll111lll1l_opy_:
                try:
                    atexit.unregister(self.__1ll111ll111_opy_)
                except ValueError:
                    pass
                self.bstack1lll11llll1_opy_.stop()
                self.bstack1ll111lll1l_opy_ = False
            start = datetime.now()
            if self.bstack1ll11ll1111_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l1lllllll1_opy_:
                    self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣቹ"), datetime.now() - start)
                else:
                    self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤቺ"), datetime.now() - start)
            self.__1ll11111lll_opy_()
            start = datetime.now()
            bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(bstack11ll111_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺ࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࠦቻ"))
            self.bstack1ll111l11ll_opy_.close()
            bstack1111l1l1l_opy_.end(bstack11ll111_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻ࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࠧቼ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣች"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢቾ"), True, None, None, None, None)
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧቿ"), datetime.now() - start)
            self.bstack1ll111l11ll_opy_ = None
        if self.process:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸࡺ࡯ࡱࠤኀ"))
            start = datetime.now()
            bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(bstack11ll111_opy_ (u"ࠧࡹࡤ࡬࠼ࡦࡰ࡮ࡀ࡫ࡪ࡮࡯ࠦኁ"))
            self.process.terminate()
            bstack1111l1l1l_opy_.end(bstack11ll111_opy_ (u"ࠨࡳࡥ࡭࠽ࡧࡱ࡯࠺࡬࡫࡯ࡰࠧኂ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢኃ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨኄ"), True, None, None, None, None)
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠤ࡮࡭ࡱࡲ࡟ࡵ࡫ࡰࡩࠧኅ"), datetime.now() - start)
            self.process = None
            if self.bstack1l1lllll111_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1lll1ll_opy_()
                self.logger.info(
                    bstack11ll111_opy_ (u"࡚ࠥ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠥኆ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11ll111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪኇ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1ll1111l_opy_ = False
    def __1ll1l111ll1_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11ll111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢኈ")] = selenium.__version__
            data.frameworks.append(bstack11ll111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣ኉"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦኊ")] = __version__
            data.frameworks.append(bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧኋ"))
        except:
            pass
    def bstack1ll111lllll_opy_(self, hub_url: str, platform_index: int, bstack1ll1ll1ll1_opy_: Any):
        if self.bstack1lll11111ll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨኌ"))
            return
        try:
            bstack11lll11111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11ll111_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧኍ")
            self.bstack1lll11111ll_opy_ = bstack1ll1111ll11_opy_(
                cli.config.get(bstack11ll111_opy_ (u"ࠦ࡭ࡻࡢࡖࡴ࡯ࠦ኎"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1l1l1111_opy_={bstack11ll111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤ኏"): bstack1ll1ll1ll1_opy_}
            )
            def bstack1ll11lll111_opy_(self):
                return
            if self.config.get(bstack11ll111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠣነ"), True):
                Service.start = bstack1ll11lll111_opy_
                Service.stop = bstack1ll11lll111_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11l1ll11l1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll11ll1l1l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣኑ"), datetime.now() - bstack11lll11111_opy_)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࠢኒ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥና"))
    def bstack1ll1l11l1ll_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l1ll1lll1_opy_
            self.bstack1lll11111ll_opy_ = bstack1ll11l1111l_opy_(
                platform_index,
                framework_name=bstack11ll111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢኔ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠽ࠤࠧን") + str(e) + bstack11ll111_opy_ (u"ࠧࠨኖ"))
            pass
    def bstack1ll1l11l111_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣኗ"))
            return
        if bstack111l1lll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢኘ"): pytest.__version__ }, [bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧኙ")], self.bstack1lll11llll1_opy_, self.bstack1l1llllll1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll11l1llll_opy_({ bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤኚ"): pytest.__version__ }, [bstack11ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥኛ")], self.bstack1lll11llll1_opy_, self.bstack1l1llllll1l_opy_)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࠣኜ") + str(e) + bstack11ll111_opy_ (u"ࠧࠨኝ"))
        self.bstack1l1lll11l1l_opy_()
    def bstack1l1lll11l1l_opy_(self):
        if not self.bstack11l1llllll_opy_():
            return
        bstack111ll1llll_opy_ = None
        def bstack111lll11_opy_(config, startdir):
            return bstack11ll111_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦኞ").format(bstack11ll111_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨኟ"))
        def bstack11llllll1_opy_():
            return
        def bstack11l11l1l11_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11ll111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨአ"):
                return bstack11ll111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣኡ")
            else:
                return bstack111ll1llll_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack111ll1llll_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack111lll11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11llllll1_opy_
            Config.getoption = bstack11l11l1l11_opy_
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬ࠥࡶࡹࡵࡧࡶࡸࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠽ࠤࠧኢ") + str(e) + bstack11ll111_opy_ (u"ࠦࠧኣ"))
    def bstack1ll1111llll_opy_(self):
        bstack11l11l1ll1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11l11l1ll1_opy_, dict):
            if cli.config_observability:
                bstack11l11l1ll1_opy_.update(
                    {bstack11ll111_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧኤ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤእ") in accessibility.get(bstack11ll111_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣኦ"), {}):
                    bstack1ll11llll1l_opy_ = accessibility.get(bstack11ll111_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤኧ"))
                    bstack1ll11llll1l_opy_.update({ bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠥከ"): bstack1ll11llll1l_opy_.pop(bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨኩ")) })
                bstack11l11l1ll1_opy_.update({bstack11ll111_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦኪ"): accessibility })
        return bstack11l11l1ll1_opy_
    @measure(event_name=EVENTS.bstack1ll11l111l1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1ll11ll1111_opy_(self, bstack1ll1l1111l1_opy_: str = None, bstack1l1llll11ll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1l1llllll1l_opy_:
            return
        bstack11lll11111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬካ"), bstack11ll111_opy_ (u"࠭࠰ࠨኬ")))
        req.client_worker_id = bstack11ll111_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨክ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll1l1111l1_opy_:
            req.bstack1ll1l1111l1_opy_ = bstack1ll1l1111l1_opy_
        if bstack1l1llll11ll_opy_:
            req.bstack1l1llll11ll_opy_ = bstack1l1llll11ll_opy_
        try:
            r = self.bstack1l1llllll1l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤኮ"), datetime.now() - bstack11lll11111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll1l1l11_opy_(self, key: str, value: timedelta):
        tag = bstack11ll111_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤኯ") if self.bstack1l11l1111_opy_() else bstack11ll111_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤኰ")
        self.bstack1ll1l1ll1l1_opy_[bstack11ll111_opy_ (u"ࠦ࠿ࠨ኱").join([tag + bstack11ll111_opy_ (u"ࠧ࠳ࠢኲ") + str(id(self)), key])] += value
    def bstack1l1lll1ll_opy_(self):
        if not os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥኳ"), bstack11ll111_opy_ (u"ࠢ࠱ࠤኴ")) == bstack11ll111_opy_ (u"ࠣ࠳ࠥኵ"):
            return
        bstack1ll111l11l1_opy_ = dict()
        bstack1ll1lll1ll1_opy_ = []
        if self.test_framework:
            bstack1ll1lll1ll1_opy_.extend(list(self.test_framework.bstack1ll1lll1ll1_opy_.values()))
        if self.bstack1lll11111ll_opy_:
            bstack1ll1lll1ll1_opy_.extend(list(self.bstack1lll11111ll_opy_.bstack1ll1lll1ll1_opy_.values()))
        for instance in bstack1ll1lll1ll1_opy_:
            if not instance.platform_index in bstack1ll111l11l1_opy_:
                bstack1ll111l11l1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll111l11l1_opy_[instance.platform_index]
            for k, v in instance.bstack1ll11l1l1ll_opy_().items():
                report[k] += v
                report[k.split(bstack11ll111_opy_ (u"ࠤ࠽ࠦ኶"))[0]] += v
        bstack1ll11l1l111_opy_ = sorted([(k, v) for k, v in self.bstack1ll1l1ll1l1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll111ll11l_opy_ = 0
        for r in bstack1ll11l1l111_opy_:
            bstack1ll1l111l1l_opy_ = r[1].total_seconds()
            bstack1ll111ll11l_opy_ += bstack1ll1l111l1l_opy_
            self.logger.debug(bstack11ll111_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣ኷") + str(bstack1ll1l111l1l_opy_) + bstack11ll111_opy_ (u"ࠦࠧኸ"))
        self.logger.debug(bstack11ll111_opy_ (u"ࠧ࠳࠭ࠣኹ"))
        bstack1ll1111l1ll_opy_ = []
        for platform_index, report in bstack1ll111l11l1_opy_.items():
            bstack1ll1111l1ll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1111l1ll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack111l1ll1ll_opy_ = set()
        bstack1ll1l1l1ll1_opy_ = 0
        for r in bstack1ll1111l1ll_opy_:
            bstack1ll1l111l1l_opy_ = r[2].total_seconds()
            bstack1ll1l1l1ll1_opy_ += bstack1ll1l111l1l_opy_
            bstack111l1ll1ll_opy_.add(r[0])
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢኺ") + str(bstack1ll1l111l1l_opy_) + bstack11ll111_opy_ (u"ࠢࠣኻ"))
        if self.bstack1l11l1111_opy_():
            self.logger.debug(bstack11ll111_opy_ (u"ࠣ࠯࠰ࠦኼ"))
            self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤኽ") + str(bstack1ll1l1l1ll1_opy_) + bstack11ll111_opy_ (u"ࠥࠦኾ"))
        else:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣ኿") + str(bstack1ll111ll11l_opy_) + bstack11ll111_opy_ (u"ࠧࠨዀ"))
        self.logger.debug(bstack11ll111_opy_ (u"ࠨ࠭࠮ࠤ዁"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧዂ"), bstack11ll111_opy_ (u"ࠨ࠲ࠪዃ"))),
            client_worker_id=bstack11ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣዄ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1l1llllll1l_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡄࡣࡱࡲࡴࡺࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢዅ"))
            return None
        response = self.bstack1l1llllll1l_opy_.TestOrchestration(request)
        self.logger.debug(bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵ࠯ࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠯ࡶࡩࡸࡹࡩࡰࡰࡀࡿࢂࠨ዆").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l1llllllll_opy_(self, r):
        if r is not None and getattr(r, bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭዇"), None) and getattr(r.testhub, bstack11ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ወ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11ll111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨዉ")))
            for bstack1ll1l111l11_opy_, err in errors.items():
                if err[bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ዊ")] == bstack11ll111_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧዋ"):
                    self.logger.info(err[bstack11ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫዌ")])
                else:
                    self.logger.error(err[bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬው")])
    def bstack11llll1111_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()