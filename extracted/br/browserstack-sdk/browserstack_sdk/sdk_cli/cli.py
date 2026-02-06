# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
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
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1l1llllll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1lll1_opy_ import bstack1ll1l1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll111111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1ll1_opy_ import bstack1ll1l1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l11l_opy_ import bstack1ll11l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll1ll11lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1ll11lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll11_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack11l1ll1l_opy_ import bstack11l1ll1l_opy_, bstack1lll11l1l_opy_, bstack1llllll111_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll1ll1111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import bstack1lll1ll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1lll1lll11l_opy_
from bstack_utils.helper import Notset, bstack1ll111l1111_opy_, get_cli_dir, bstack1ll11ll111l_opy_, bstack11l111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll11ll11l1_opy_ import bstack1ll1l1l111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1lll_opy_ import bstack11l1111l11_opy_
from bstack_utils.helper import Notset, bstack1ll111l1111_opy_, get_cli_dir, bstack1ll11ll111l_opy_, bstack11l111l111_opy_, bstack111ll111_opy_, bstack111llll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11111l1l_opy_, bstack1ll11111ll1_opy_, bstack1ll11l1l11l_opy_, bstack1ll1l11ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import bstack1lll1l1l11l_opy_, bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11ll1l11_opy_ import bstack1l11l11ll_opy_
from bstack_utils import logger_utils
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l1l11ll_opy_, bstack11llll1111_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1ll1l1l1_opy_())
def bstack1ll111ll1l1_opy_(bs_config):
    bstack1ll1l11ll1l_opy_ = None
    bstack1ll111lll1l_opy_ = None
    try:
        bstack1ll111lll1l_opy_ = get_cli_dir()
        bstack1ll1l11ll1l_opy_ = bstack1ll11ll111l_opy_(bstack1ll111lll1l_opy_)
        bstack1ll1ll1l111_opy_ = bstack1ll111l1111_opy_(bstack1ll1l11ll1l_opy_, bstack1ll111lll1l_opy_, bs_config)
        bstack1ll1l11ll1l_opy_ = bstack1ll1ll1l111_opy_ if bstack1ll1ll1l111_opy_ else bstack1ll1l11ll1l_opy_
        if not bstack1ll1l11ll1l_opy_:
            raise ValueError(bstack11lllll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧᅬ"))
    except Exception as ex:
        logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢ࡯ࡥࡹ࡫ࡳࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡾࢁࠧᅭ").format(ex))
        bstack1ll1l11ll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨᅮ"))
        if bstack1ll1l11ll1l_opy_:
            logger.debug(bstack11lllll_opy_ (u"ࠦࡋࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠢࡩࡶࡴࡳࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸ࠿ࠦࠢᅯ") + str(bstack1ll1l11ll1l_opy_) + bstack11lllll_opy_ (u"ࠧࠨᅰ"))
        else:
            logger.debug(bstack11lllll_opy_ (u"ࠨࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠿ࠥࡹࡥࡵࡷࡳࠤࡲࡧࡹࠡࡤࡨࠤ࡮ࡴࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠤᅱ"))
    return bstack1ll1l11ll1l_opy_, bstack1ll111lll1l_opy_
bstack1ll1l111l1l_opy_ = bstack11lllll_opy_ (u"ࠢ࠺࠻࠼࠽ࠧᅲ")
bstack1ll1lll111l_opy_ = bstack11lllll_opy_ (u"ࠣࡴࡨࡥࡩࡿࠢᅳ")
bstack1ll1l1ll111_opy_ = bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᅴ")
bstack1ll1ll11ll1_opy_ = bstack11lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡐࡎ࡙ࡔࡆࡐࡢࡅࡉࡊࡒࠣᅵ")
bstack11ll1l1l11_opy_ = bstack11lllll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᅶ")
bstack1ll1l1l1l1l_opy_ = re.compile(bstack11lllll_opy_ (u"ࡷࠨࠨࡀ࡫ࠬ࠲࠯࠮ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࢁࡈࡓࠪ࠰࠭ࠦᅷ"))
bstack1ll1l111111_opy_ = bstack11lllll_opy_ (u"ࠨࡤࡦࡸࡨࡰࡴࡶ࡭ࡦࡰࡷࠦᅸ")
bstack1ll1l1ll1ll_opy_ = bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡐࡔࡆࡉࡤࡌࡁࡍࡎࡅࡅࡈࡑࠢᅹ")
bstack1ll1ll11l11_opy_ = [
    bstack1lll11l1l_opy_.bstack1l11ll11l1_opy_,
    bstack1lll11l1l_opy_.CONNECT,
    bstack1lll11l1l_opy_.bstack11l1l11l1_opy_,
]
class SDKCLI:
    _1ll11llll1l_opy_ = None
    process: Union[None, Any]
    bstack1ll11lll1l1_opy_: bool
    bstack1ll11ll11ll_opy_: bool
    bstack1ll11ll1ll1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll1lll11ll_opy_: Union[None, grpc.Channel]
    bstack1ll1l1l1111_opy_: str
    test_framework: TestFramework
    bstack1lll1l1ll11_opy_: bstack1lll1ll1ll1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l1lllllll1_opy_: bstack1ll11llll11_opy_
    accessibility: bstack1l1llllll11_opy_
    bstack1l1ll1lll_opy_: bstack11l1111l11_opy_
    ai: bstack1ll1l1ll11l_opy_
    bstack1l1lllll1ll_opy_: bstack1ll111111ll_opy_
    bstack1ll11111l11_opy_: List[bstack1lll1l1l1l1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll11l1l111_opy_: Any
    bstack1ll1ll111ll_opy_: Dict[str, timedelta]
    bstack1l1llll1lll_opy_: str
    bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_
    def __new__(cls):
        if not cls._1ll11llll1l_opy_:
            cls._1ll11llll1l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll11llll1l_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll11lll1l1_opy_ = False
        self.bstack1ll1lll11ll_opy_ = None
        self.bstack1ll1l1l1ll1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1ll11ll1_opy_, None)
        self.bstack1ll1l11llll_opy_ = os.environ.get(bstack1ll1l1ll111_opy_, bstack11lllll_opy_ (u"ࠣࠤᅺ")) == bstack11lllll_opy_ (u"ࠤࠥᅻ")
        self.bstack1ll11ll11ll_opy_ = False
        self.bstack1ll11ll1ll1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll11l1l111_opy_ = None
        self.test_framework = None
        self.bstack1lll1l1ll11_opy_ = None
        self.bstack1ll1l1l1111_opy_=bstack11lllll_opy_ (u"ࠥࠦᅼ")
        self.session_framework = None
        self.logger = logger_utils.get_logger(self.__class__.__name__, logger_utils.bstack1ll1ll1l1l1_opy_())
        self.bstack1ll1ll111ll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lll11ll111_opy_ = bstack1lll11l1lll_opy_()
        self.bstack1ll1111lll1_opy_ = False
        self.bstack1ll11lll111_opy_ = None
        self.bstack1ll1lll11l1_opy_ = None
        self.bstack1l1lllllll1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll11111l11_opy_ = []
    def bstack1l111lll1l_opy_(self):
        return os.environ.get(bstack11ll1l1l11_opy_).lower().__eq__(bstack11lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤᅽ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll1l1ll1ll_opy_, bstack11lllll_opy_ (u"ࠬ࠭ᅾ")).lower() in [bstack11lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫᅿ"), bstack11lllll_opy_ (u"ࠧ࠲ࠩᆀ"), bstack11lllll_opy_ (u"ࠨࡻࡨࡷࠬᆁ")]:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡉࡳࡷࡩࡩ࡯ࡩࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡳ࡯ࡥࡧࠣࡨࡺ࡫ࠠࡵࡱࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡓࡗࡉࡅࡠࡈࡄࡐࡑࡈࡁࡄࡍࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠥᆂ"))
            os.environ[bstack11lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨᆃ")] = bstack11lllll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᆄ")
            return False
        if bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᆅ") in config and str(config[bstack11lllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᆆ")]).lower() != bstack11lllll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᆇ"):
            return False
        bstack1ll11ll1l1l_opy_ = [bstack11lllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᆈ"), bstack11lllll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᆉ")]
        bstack1ll11111lll_opy_ = config.get(bstack11lllll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨᆊ")) in bstack1ll11ll1l1l_opy_ or os.environ.get(bstack11lllll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬᆋ")) in bstack1ll11ll1l1l_opy_
        os.environ[bstack11lllll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣᆌ")] = str(bstack1ll11111lll_opy_) # bstack1ll1l1ll1l1_opy_ bstack1ll111l11ll_opy_ VAR to bstack1ll1ll1llll_opy_ is binary running
        return bstack1ll11111lll_opy_
    def bstack1l1111ll_opy_(self):
        for event in bstack1ll1ll11l11_opy_:
            bstack11l1ll1l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11l1ll1l_opy_.logger.debug(bstack11lllll_opy_ (u"ࠨࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠥࡃ࠾ࠡࡽࡤࡶ࡬ࡹࡽࠡࠤᆍ") + str(kwargs) + bstack11lllll_opy_ (u"ࠢࠣᆎ"))
            )
        bstack11l1ll1l_opy_.register(bstack1lll11l1l_opy_.bstack1l11ll11l1_opy_, self.__1ll1111ll11_opy_)
        bstack11l1ll1l_opy_.register(bstack1lll11l1l_opy_.CONNECT, self.__1ll111ll1ll_opy_)
        bstack11l1ll1l_opy_.register(bstack1lll11l1l_opy_.bstack11l1l11l1_opy_, self.__1l1lllll111_opy_)
        bstack11l1ll1l_opy_.register(bstack1lll11l1l_opy_.bstack11ll1111_opy_, self.__1ll11l1l1l1_opy_)
    def bstack11llll11l_opy_(self):
        return not self.bstack1ll1l11llll_opy_ and os.environ.get(bstack1ll1l1ll111_opy_, bstack11lllll_opy_ (u"ࠣࠤᆏ")) != bstack11lllll_opy_ (u"ࠤࠥᆐ")
    def is_running(self):
        if self.bstack1ll1l11llll_opy_:
            return self.bstack1ll11lll1l1_opy_
        else:
            return bool(self.bstack1ll1lll11ll_opy_)
    def bstack1ll1111ll1l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll11111l11_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll111l1l1l_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll1l111l11_opy_(self, bstack1l1llllllll_opy_=10):
        if self.bstack1ll1l1l1ll1_opy_:
            return
        bstack1l1111l111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1ll11ll1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11lllll_opy_ (u"ࠥ࡟ࠧᆑ") + str(id(self)) + bstack11lllll_opy_ (u"ࠦࡢࠦࡣࡰࡰࡱࡩࡨࡺࡩ࡯ࡩࠥᆒ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11lllll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡠࡲࡵࡳࡽࡿࠢᆓ"), 0), (bstack11lllll_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡵࡢࡴࡷࡵࡸࡺࠤᆔ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l1llllllll_opy_)
        self.bstack1ll1lll11ll_opy_ = channel
        self.bstack1ll1l1l1ll1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll1lll11ll_opy_)
        self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࠨᆕ"), datetime.now() - bstack1l1111l111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1ll11ll1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11lllll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦ࠽ࠤ࡮ࡹ࡟ࡤࡪ࡬ࡰࡩࡥࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᆖ") + str(self.bstack11llll11l_opy_()) + bstack11lllll_opy_ (u"ࠤࠥᆗ"))
    def __1l1lllll111_opy_(self, event_name):
        if self.bstack11llll11l_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡃࡍࡋࠥᆘ"))
        self.__1ll1l111lll_opy_()
    @measure(event_name=EVENTS.bstack1ll11lllll1_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll11l1l1l1_opy_(self, event_name, bstack1ll1l1l11ll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack11lllll_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠦᆙ"))
        bstack1ll1111l111_opy_ = Path(bstack1llll11111l_opy_ (u"ࠧࢁࡳࡦ࡮ࡩ࠲ࡨࡲࡩࡠࡦ࡬ࡶࢂ࠵ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࡳ࠯࡬ࡶࡳࡳࠨᆚ"))
        if self.bstack1ll111lll1l_opy_ and bstack1ll1111l111_opy_.exists():
            with open(bstack1ll1111l111_opy_, bstack11lllll_opy_ (u"࠭ࡲࠨᆛ"), encoding=bstack11lllll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᆜ")) as fp:
                data = json.load(fp)
                try:
                    bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᆝ"), bstack1l11l11ll_opy_(bstack1lll1111l_opy_), data, {
                        bstack11lllll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᆞ"): (self.config[bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᆟ")], self.config[bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᆠ")])
                    })
                except Exception as e:
                    logger.debug(bstack11llll1111_opy_.format(str(e)))
            bstack1ll1111l111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll11l1l1ll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll1111ll11_opy_(self, event_name: str, data):
        from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
        self.bstack1ll1l1l1111_opy_, self.bstack1ll111lll1l_opy_ = bstack1ll111ll1l1_opy_(data.bs_config)
        os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡜ࡘࡉࡕࡃࡅࡐࡊࡥࡄࡊࡔࠪᆡ")] = self.bstack1ll111lll1l_opy_
        if not self.bstack1ll1l1l1111_opy_ or not self.bstack1ll111lll1l_opy_:
            raise ValueError(bstack11lllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡪࡨࠤࡘࡊࡋࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠧᆢ"))
        if self.bstack11llll11l_opy_():
            self.__1ll111ll1ll_opy_(event_name, bstack1llllll111_opy_())
            return
        try:
            logger.debug(bstack11lllll_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨᆣ"))
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧᆤ").format(e))
        start = datetime.now()
        is_started = self.__1ll111l11l1_opy_()
        self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨᆥ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1l111l11_opy_()
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤᆦ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1l11l111_opy_(data)
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤᆧ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll111llll1_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll111ll1ll_opy_(self, event_name: str, data: bstack1llllll111_opy_):
        if not self.bstack11llll11l_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᆨ"))
            return
        bin_session_id = os.environ.get(bstack1ll1l1ll111_opy_)
        start = datetime.now()
        self.__1ll1l111l11_opy_()
        self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧᆩ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨᆪ") + str(bin_session_id) + bstack11lllll_opy_ (u"ࠣࠤᆫ"))
        start = datetime.now()
        self.__1ll111ll11l_opy_()
        self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢᆬ"), datetime.now() - start)
    def __1ll1l1l11l1_opy_(self):
        if not self.bstack1ll1l1l1ll1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢᆭ"))
            return
        bstack1l1llllll1l_opy_ = {
            bstack11lllll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᆮ"): (bstack1ll1ll11lll_opy_, bstack1ll11lll11l_opy_, bstack1lll1lll11l_opy_),
            bstack11lllll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᆯ"): (bstack1ll1l1111l1_opy_, bstack1ll11l1llll_opy_, bstack1lll11lllll_opy_),
        }
        if not self.bstack1ll11lll111_opy_ and self.session_framework in bstack1l1llllll1l_opy_:
            bstack1ll111l111l_opy_, bstack1ll111l1l11_opy_, bstack1ll11l1ll11_opy_ = bstack1l1llllll1l_opy_[self.session_framework]
            bstack1ll1l1llll1_opy_ = bstack1ll111l1l11_opy_()
            self.bstack1ll1lll11l1_opy_ = bstack1ll1l1llll1_opy_
            self.bstack1ll11lll111_opy_ = bstack1ll11l1ll11_opy_
            self.bstack1ll11111l11_opy_.append(bstack1ll1l1llll1_opy_)
            self.bstack1ll11111l11_opy_.append(bstack1ll111l111l_opy_(self.bstack1ll1lll11l1_opy_))
        if not self.bstack1l1lllllll1_opy_ and self.config_observability and self.config_observability.success: # bstack1ll11l111ll_opy_
            self.bstack1l1lllllll1_opy_ = bstack1ll11llll11_opy_(self.bstack1ll11lll111_opy_, self.bstack1ll1lll11l1_opy_) # bstack1ll1ll1lll1_opy_
            self.bstack1ll11111l11_opy_.append(self.bstack1l1lllllll1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l1llllll11_opy_(self.bstack1ll11lll111_opy_, self.bstack1ll1lll11l1_opy_)
            self.bstack1ll11111l11_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11lllll_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣᆰ"), False) == True:
            self.ai = bstack1ll1l1ll11l_opy_()
            self.bstack1ll11111l11_opy_.append(self.ai)
        if not self.percy and self.bstack1ll11l1l111_opy_ and self.bstack1ll11l1l111_opy_.success:
            self.percy = bstack1ll111111ll_opy_(self.bstack1ll11l1l111_opy_)
            self.bstack1ll11111l11_opy_.append(self.percy)
        for mod in self.bstack1ll11111l11_opy_:
            if not mod.bstack1ll11l11111_opy_():
                mod.configure(self.bstack1ll1l1l1ll1_opy_, self.config, self.cli_bin_session_id, self.bstack1lll11ll111_opy_)
    def __1ll1111llll_opy_(self):
        for mod in self.bstack1ll11111l11_opy_:
            if mod.bstack1ll11l11111_opy_():
                mod.configure(self.bstack1ll1l1l1ll1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll11111111_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll1l11l111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll11ll11ll_opy_:
            return
        self.__1ll1l1lllll_opy_(data)
        bstack1l1111l111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11lllll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᆱ")
        req.sdk_language = bstack11lllll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣᆲ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll1l1l1l1l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᆳ"), bstack11lllll_opy_ (u"ࠪ࠴ࠬᆴ")))
            req.client_worker_id = bstack11lllll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᆵ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡸࡱࡵ࡯ࡪࡸࠠࡢࡰࡧࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡩ࡯ࡦࡨࡼ࠿ࠦࡻࡾࠤᆶ").format(e))
        try:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡛ࠣᆷ") + str(id(self)) + bstack11lllll_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᆸ"))
            r = self.bstack1ll1l1l1ll1_opy_.StartBinSession(req)
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᆹ"), datetime.now() - bstack1l1111l111_opy_)
            os.environ[bstack1ll1l1ll111_opy_] = r.bin_session_id
            self.__1ll1l1lll11_opy_(r)
            self.__1ll1l1l11l1_opy_()
            if not self.bstack1ll1111lll1_opy_:
                self.bstack1lll11ll111_opy_.start()
                self.bstack1ll1111lll1_opy_ = True
                atexit.register(self.__1ll1l11lll1_opy_)
            self.bstack1ll11ll11ll_opy_ = True
            self.logger.debug(bstack11lllll_opy_ (u"ࠤ࡞ࠦᆺ") + str(id(self)) + bstack11lllll_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣᆻ"))
        except grpc.bstack1ll11l1111l_opy_ as bstack1ll11ll1111_opy_:
            self.logger.error(bstack11lllll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆼ") + str(bstack1ll11ll1111_opy_) + bstack11lllll_opy_ (u"ࠧࠨᆽ"))
            traceback.print_exc()
            raise bstack1ll11ll1111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᆾ") + str(e) + bstack11lllll_opy_ (u"ࠢࠣᆿ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1ll1ll1l_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll111ll11l_opy_(self):
        if not self.bstack11llll11l_opy_() or not self.cli_bin_session_id or self.bstack1ll11ll1ll1_opy_:
            return
        bstack1l1111l111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᇀ"), bstack11lllll_opy_ (u"ࠩ࠳ࠫᇁ")))
        req.client_worker_id = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᇂ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡠࠨᇃ") + str(id(self)) + bstack11lllll_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᇄ"))
            r = self.bstack1ll1l1l1ll1_opy_.ConnectBinSession(req)
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥᇅ"), datetime.now() - bstack1l1111l111_opy_)
            self.__1ll1l1lll11_opy_(r)
            self.__1ll1l1l11l1_opy_()
            if not self.bstack1ll1111lll1_opy_:
                self.bstack1lll11ll111_opy_.start()
                self.bstack1ll1111lll1_opy_ = True
                atexit.register(self.__1ll1l11lll1_opy_)
            self.bstack1ll11ll1ll1_opy_ = True
            self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡜ࠤᇆ") + str(id(self)) + bstack11lllll_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢᇇ"))
        except grpc.bstack1ll11l1111l_opy_ as bstack1ll11ll1111_opy_:
            self.logger.error(bstack11lllll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇈ") + str(bstack1ll11ll1111_opy_) + bstack11lllll_opy_ (u"ࠥࠦᇉ"))
            traceback.print_exc()
            raise bstack1ll11ll1111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇊ") + str(e) + bstack11lllll_opy_ (u"ࠧࠨᇋ"))
            traceback.print_exc()
            raise e
    def __1ll1l1lll11_opy_(self, r):
        self.bstack1ll1ll1l1ll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11lllll_opy_ (u"ࠨࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᇌ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11lllll_opy_ (u"ࠢࡦ࡯ࡳࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡷࡱࡨࠧᇍ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡥࡳࡥࡼࠤ࡮ࡹࠠࡴࡧࡱࡸࠥࡵ࡮࡭ࡻࠣࡥࡸࠦࡰࡢࡴࡷࠤࡴ࡬ࠠࡵࡪࡨࠤࠧࡉ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠮ࠥࠤࡦࡴࡤࠡࡶ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡦࡲࡳࡰࠢࡸࡷࡪࡪࠠࡣࡻࠣࡗࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡨࡶࡪ࡬࡯ࡳࡧ࠯ࠤࡓࡵ࡮ࡦࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤ࡮ࡹࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᇎ")
        self.bstack1ll11l1l111_opy_ = getattr(r, bstack11lllll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᇏ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᇐ")] = self.config_testhub.jwt
        os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᇑ")] = self.config_testhub.build_hashed_id
    def bstack1ll11l11lll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll11lll1l1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l1llll1ll1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l1llll1ll1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll11l11lll_opy_(event_name=EVENTS.bstack1ll1111l11l_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll111l11l1_opy_(self, bstack1l1llllllll_opy_=10):
        if self.bstack1ll11lll1l1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡹࡴࡢࡴࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠢᇒ"))
            return True
        self.logger.debug(bstack11lllll_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᇓ"))
        if os.getenv(bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡉࡓ࡜ࠢᇔ")) == bstack1ll1l111111_opy_:
            self.cli_bin_session_id = bstack1ll1l111111_opy_
            self.cli_listen_addr = bstack11lllll_opy_ (u"ࠣࡷࡱ࡭ࡽࡀ࠯ࡵ࡯ࡳ࠳ࡸࡪ࡫࠮ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࠩࡸ࠴ࡳࡰࡥ࡮ࠦᇕ") % (self.cli_bin_session_id)
            self.bstack1ll11lll1l1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1ll1l1l1111_opy_, bstack11lllll_opy_ (u"ࠤࡶࡨࡰࠨᇖ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1ll11l1l_opy_ compat for text=True in bstack1ll1l1l1lll_opy_ python
            encoding=bstack11lllll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᇗ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll111ll111_opy_ = threading.Thread(target=self.__1ll11l11l11_opy_, args=(bstack1l1llllllll_opy_,))
        bstack1ll111ll111_opy_.start()
        bstack1ll111ll111_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11lllll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡷࡵࡧࡷ࡯࠼ࠣࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࢁࠥࡵࡵࡵ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡶࡸࡩࡵࡵࡵ࠰ࡵࡩࡦࡪࠨࠪࡿࠣࡩࡷࡸ࠽ࠣᇘ") + str(self.process.stderr.read()) + bstack11lllll_opy_ (u"ࠧࠨᇙ"))
        if not self.bstack1ll11lll1l1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡛ࠣᇚ") + str(id(self)) + bstack11lllll_opy_ (u"ࠢ࡞ࠢࡦࡰࡪࡧ࡮ࡶࡲࠥᇛ"))
            self.__1ll1l111lll_opy_()
        self.logger.debug(bstack11lllll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡱࡴࡲࡧࡪࡹࡳࡠࡴࡨࡥࡩࡿ࠺ࠡࠤᇜ") + str(self.bstack1ll11lll1l1_opy_) + bstack11lllll_opy_ (u"ࠤࠥᇝ"))
        return self.bstack1ll11lll1l1_opy_
    def __1ll11l11l11_opy_(self, bstack1ll1l1111ll_opy_=10):
        bstack1ll11l1ll1l_opy_ = time.time()
        while self.process and time.time() - bstack1ll11l1ll1l_opy_ < bstack1ll1l1111ll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11lllll_opy_ (u"ࠥ࡭ࡩࡃࠢᇞ") in line:
                    self.cli_bin_session_id = line.split(bstack11lllll_opy_ (u"ࠦ࡮ࡪ࠽ࠣᇟ"))[-1:][0].strip()
                    self.logger.debug(bstack11lllll_opy_ (u"ࠧࡩ࡬ࡪࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦ࠽ࠦᇠ") + str(self.cli_bin_session_id) + bstack11lllll_opy_ (u"ࠨࠢᇡ"))
                    continue
                if bstack11lllll_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣᇢ") in line:
                    self.cli_listen_addr = line.split(bstack11lllll_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᇣ"))[-1:][0].strip()
                    self.logger.debug(bstack11lllll_opy_ (u"ࠤࡦࡰ࡮ࡥ࡬ࡪࡵࡷࡩࡳࡥࡡࡥࡦࡵ࠾ࠧᇤ") + str(self.cli_listen_addr) + bstack11lllll_opy_ (u"ࠥࠦᇥ"))
                    continue
                if bstack11lllll_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥᇦ") in line:
                    port = line.split(bstack11lllll_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᇧ"))[-1:][0].strip()
                    self.logger.debug(bstack11lllll_opy_ (u"ࠨࡰࡰࡴࡷ࠾ࠧᇨ") + str(port) + bstack11lllll_opy_ (u"ࠢࠣᇩ"))
                    continue
                if line.strip() == bstack1ll1lll111l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11lllll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡊࡑࡢࡗ࡙ࡘࡅࡂࡏࠥᇪ"), bstack11lllll_opy_ (u"ࠤ࠴ࠦᇫ")) == bstack11lllll_opy_ (u"ࠥ࠵ࠧᇬ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll11lll1l1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11lllll_opy_ (u"ࠦࡪࡸࡲࡰࡴ࠽ࠤࠧᇭ") + str(e) + bstack11lllll_opy_ (u"ࠧࠨᇮ"))
        return False
    def __1ll1l11lll1_opy_(self):
        bstack11lllll_opy_ (u"ࠨࠢࠣࡅ࡯ࡩࡦࡴࡵࡱࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࡪࡴࡸࠠࡢࡵࡼࡲࡨࡥࡤࡪࡵࡳࡥࡹࡩࡨࡦࡴ࠯ࠤࡨࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡢࡶࡨࡼ࡮ࡺࠠࡵࡱࠣࡩࡳࡹࡵࡳࡧࠣࡸࡦࡹ࡫ࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠧࠨࠢᇯ")
        if self.bstack1lll11ll111_opy_ and self.bstack1ll1111lll1_opy_:
            try:
                self.bstack1lll11ll111_opy_.stop()
                self.bstack1ll1111lll1_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1ll1ll11111_opy_, stage=STAGE.bstack1llll11111_opy_)
    def __1ll1l111lll_opy_(self):
        if self.bstack1ll1lll11ll_opy_:
            if self.bstack1lll11ll111_opy_ and self.bstack1ll1111lll1_opy_:
                try:
                    atexit.unregister(self.__1ll1l11lll1_opy_)
                except ValueError:
                    pass
                self.bstack1lll11ll111_opy_.stop()
                self.bstack1ll1111lll1_opy_ = False
            start = datetime.now()
            if self.bstack1ll1l11l1ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll11ll1ll1_opy_:
                    self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᇰ"), datetime.now() - start)
                else:
                    self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᇱ"), datetime.now() - start)
            self.__1ll1111llll_opy_()
            start = datetime.now()
            bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(bstack11lllll_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽ࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺࠢᇲ"))
            self.bstack1ll1lll11ll_opy_.close()
            bstack1lll11l1ll_opy_.end(bstack11lllll_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࠣᇳ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᇴ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᇵ"), True, None, None, None, None)
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᇶ"), datetime.now() - start)
            self.bstack1ll1lll11ll_opy_ = None
        if self.process:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡴࡶࡲࡴࠧᇷ"))
            start = datetime.now()
            bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(bstack11lllll_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡮࡭ࡱࡲࠢᇸ"))
            self.process.terminate()
            bstack1lll11l1ll_opy_.end(bstack11lllll_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽࡯࡮ࡲ࡬ࠣᇹ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᇺ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᇻ"), True, None, None, None, None)
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣᇼ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll1l11llll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11l1l11111_opy_()
                self.logger.info(
                    bstack11lllll_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳࠨᇽ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11lllll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᇾ")] = self.config_testhub.build_hashed_id
        self.bstack1ll11lll1l1_opy_ = False
    def __1ll1l1lllll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11lllll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᇿ")] = selenium.__version__
            data.frameworks.append(bstack11lllll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦሀ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11lllll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢሁ")] = __version__
            data.frameworks.append(bstack11lllll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣሂ"))
        except:
            pass
    def bstack1ll1l111ll1_opy_(self, hub_url: str, platform_index: int, bstack1l111llll1_opy_: Any):
        if self.bstack1lll1l1ll11_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤሃ"))
            return
        try:
            bstack1l1111l111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11lllll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣሄ")
            self.bstack1lll1l1ll11_opy_ = bstack1lll11lllll_opy_(
                cli.config.get(bstack11lllll_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢህ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1l11l1l1_opy_={bstack11lllll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧሆ"): bstack1l111llll1_opy_}
            )
            def bstack1ll11llllll_opy_(self):
                return
            if self.config.get(bstack11lllll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦሇ"), True):
                Service.start = bstack1ll11llllll_opy_
                Service.stop = bstack1ll11llllll_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11l1111l11_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1l1l111l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦለ"), datetime.now() - bstack1l1111l111_opy_)
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥሉ") + str(e) + bstack11lllll_opy_ (u"ࠧࠨሊ"))
    def bstack1ll1lll1111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1ll1l11l1l_opy_
            self.bstack1lll1l1ll11_opy_ = bstack1lll1lll11l_opy_(
                platform_index,
                framework_name=bstack11lllll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥላ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣሌ") + str(e) + bstack11lllll_opy_ (u"ࠣࠤል"))
            pass
    def bstack1ll11ll1lll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦሎ"))
            return
        if bstack11l111l111_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11lllll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥሏ"): pytest.__version__ }, [bstack11lllll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣሐ")], self.bstack1lll11ll111_opy_, self.bstack1ll1l1l1ll1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1ll111l1_opy_({ bstack11lllll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧሑ"): pytest.__version__ }, [bstack11lllll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨሒ")], self.bstack1lll11ll111_opy_, self.bstack1ll1l1l1ll1_opy_)
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦሓ") + str(e) + bstack11lllll_opy_ (u"ࠣࠤሔ"))
        self.bstack1l1lllll1l1_opy_()
    def bstack1l1lllll1l1_opy_(self):
        if not self.bstack1l111lll1l_opy_():
            return
        bstack1ll1lll111_opy_ = None
        def bstack11ll1l11l_opy_(config, startdir):
            return bstack11lllll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢሕ").format(bstack11lllll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤሖ"))
        def bstack111l1111l_opy_():
            return
        def bstack11ll11l1_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11lllll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫሗ"):
                return bstack11lllll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦመ")
            else:
                return bstack1ll1lll111_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll1lll111_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11ll1l11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l1111l_opy_
            Config.getoption = bstack11ll11l1_opy_
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣሙ") + str(e) + bstack11lllll_opy_ (u"ࠢࠣሚ"))
    def bstack1ll1l11111l_opy_(self):
        bstack1l1ll11l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1l1ll11l1_opy_, dict):
            if cli.config_observability:
                bstack1l1ll11l1_opy_.update(
                    {bstack11lllll_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣማ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11lllll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧሜ") in accessibility.get(bstack11lllll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦም"), {}):
                    bstack1ll1111111l_opy_ = accessibility.get(bstack11lllll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧሞ"))
                    bstack1ll1111111l_opy_.update({ bstack11lllll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨሟ"): bstack1ll1111111l_opy_.pop(bstack11lllll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤሠ")) })
                bstack1l1ll11l1_opy_.update({bstack11lllll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢሡ"): accessibility })
        return bstack1l1ll11l1_opy_
    @measure(event_name=EVENTS.bstack1ll11l11ll1_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1ll1l11l1ll_opy_(self, bstack1ll11l111l1_opy_: str = None, bstack1ll11ll1l11_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1l1l1ll1_opy_:
            return
        bstack1l1111l111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨሢ"), bstack11lllll_opy_ (u"ࠩ࠳ࠫሣ")))
        req.client_worker_id = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤሤ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll11l111l1_opy_:
            req.bstack1ll11l111l1_opy_ = bstack1ll11l111l1_opy_
        if bstack1ll11ll1l11_opy_:
            req.bstack1ll11ll1l11_opy_ = bstack1ll11ll1l11_opy_
        try:
            r = self.bstack1ll1l1l1ll1_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧሥ"), datetime.now() - bstack1l1111l111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll1l1111l_opy_(self, key: str, value: timedelta):
        tag = bstack11lllll_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧሦ") if self.bstack11llll11l_opy_() else bstack11lllll_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧሧ")
        self.bstack1ll1ll111ll_opy_[bstack11lllll_opy_ (u"ࠢ࠻ࠤረ").join([tag + bstack11lllll_opy_ (u"ࠣ࠯ࠥሩ") + str(id(self)), key])] += value
    def bstack11l1l11111_opy_(self):
        if not os.getenv(bstack11lllll_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨሪ"), bstack11lllll_opy_ (u"ࠥ࠴ࠧራ")) == bstack11lllll_opy_ (u"ࠦ࠶ࠨሬ"):
            return
        bstack1l1lllll11l_opy_ = dict()
        bstack1ll1llll11l_opy_ = []
        if self.test_framework:
            bstack1ll1llll11l_opy_.extend(list(self.test_framework.bstack1ll1llll11l_opy_.values()))
        if self.bstack1lll1l1ll11_opy_:
            bstack1ll1llll11l_opy_.extend(list(self.bstack1lll1l1ll11_opy_.bstack1ll1llll11l_opy_.values()))
        for instance in bstack1ll1llll11l_opy_:
            if not instance.platform_index in bstack1l1lllll11l_opy_:
                bstack1l1lllll11l_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l1lllll11l_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1111l1l1_opy_().items():
                report[k] += v
                report[k.split(bstack11lllll_opy_ (u"ࠧࡀࠢር"))[0]] += v
        bstack1ll111111l1_opy_ = sorted([(k, v) for k, v in self.bstack1ll1ll111ll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll11l11l1l_opy_ = 0
        for r in bstack1ll111111l1_opy_:
            bstack1ll111lll11_opy_ = r[1].total_seconds()
            bstack1ll11l11l1l_opy_ += bstack1ll111lll11_opy_
            self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦሮ") + str(bstack1ll111lll11_opy_) + bstack11lllll_opy_ (u"ࠢࠣሯ"))
        self.logger.debug(bstack11lllll_opy_ (u"ࠣ࠯࠰ࠦሰ"))
        bstack1ll1l1l1l11_opy_ = []
        for platform_index, report in bstack1l1lllll11l_opy_.items():
            bstack1ll1l1l1l11_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1l1l1l11_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l1ll11l11_opy_ = set()
        bstack1ll111l1lll_opy_ = 0
        for r in bstack1ll1l1l1l11_opy_:
            bstack1ll111lll11_opy_ = r[2].total_seconds()
            bstack1ll111l1lll_opy_ += bstack1ll111lll11_opy_
            bstack1l1ll11l11_opy_.add(r[0])
            self.logger.debug(bstack11lllll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥሱ") + str(bstack1ll111lll11_opy_) + bstack11lllll_opy_ (u"ࠥࠦሲ"))
        if self.bstack11llll11l_opy_():
            self.logger.debug(bstack11lllll_opy_ (u"ࠦ࠲࠳ࠢሳ"))
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧሴ") + str(bstack1ll111l1lll_opy_) + bstack11lllll_opy_ (u"ࠨࠢስ"))
        else:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦሶ") + str(bstack1ll11l11l1l_opy_) + bstack11lllll_opy_ (u"ࠣࠤሷ"))
        self.logger.debug(bstack11lllll_opy_ (u"ࠤ࠰࠱ࠧሸ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪሹ"), bstack11lllll_opy_ (u"ࠫ࠵࠭ሺ"))),
            client_worker_id=bstack11lllll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦሻ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1l1l1ll1_opy_:
            self.logger.error(bstack11lllll_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥሼ"))
            return None
        response = self.bstack1ll1l1l1ll1_opy_.TestOrchestration(request)
        self.logger.debug(bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤሽ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1ll1l1ll_opy_(self, r):
        if r is not None and getattr(r, bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩሾ"), None) and getattr(r.testhub, bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩሿ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11lllll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤቀ")))
            for bstack1ll11lll1ll_opy_, err in errors.items():
                if err[bstack11lllll_opy_ (u"ࠫࡹࡿࡰࡦࠩቁ")] == bstack11lllll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪቂ"):
                    self.logger.info(err[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧቃ")])
                else:
                    self.logger.error(err[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨቄ")])
    def bstack111lll11_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()