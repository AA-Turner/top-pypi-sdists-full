# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1111_opy_ import bstack1ll1ll1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1ll1111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1l11111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l11l_opy_ import bstack1ll1ll11lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11lll_opy_ import bstack1ll11l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l11ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11llll1l_opy_ import bstack1ll111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l1ll_opy_ import bstack1ll11ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack1ll1111ll_opy_, bstack1ll1l11l_opy_, bstack1ll111llll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll11ll1l11_opy_ import bstack1ll1l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1ll1_opy_ import bstack1ll1ll11ll1_opy_
from bstack_utils.helper import Notset, bstack1ll111lllll_opy_, get_cli_dir, bstack1ll11lll11l_opy_, bstack1llllll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1lllll11_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1ll11_opy_ import bstack11ll1lll1_opy_
from bstack_utils.helper import Notset, bstack1ll111lllll_opy_, get_cli_dir, bstack1ll11lll11l_opy_, bstack1llllll1l_opy_, bstack1l1ll11111_opy_, bstack111l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll111ll_opy_, bstack1ll111l1lll_opy_, bstack1ll1l111111_opy_, bstack1ll11l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import bstack1lll1l1111l_opy_, bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l1lll1ll_opy_ import bstack111lll1l1_opy_
from bstack_utils import bstack111llll1ll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1ll1l111_opy_, bstack1ll1l1ll1_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
logger = bstack111llll1ll_opy_.get_logger(__name__, bstack111llll1ll_opy_.bstack1ll11l1l111_opy_())
def bstack1ll11ll1lll_opy_(bs_config):
    bstack1ll1ll11111_opy_ = None
    bstack1ll1lllll1l_opy_ = None
    try:
        bstack1ll1lllll1l_opy_ = get_cli_dir()
        bstack1ll1ll11111_opy_ = bstack1ll11lll11l_opy_(bstack1ll1lllll1l_opy_)
        bstack1ll1ll1l111_opy_ = bstack1ll111lllll_opy_(bstack1ll1ll11111_opy_, bstack1ll1lllll1l_opy_, bs_config)
        bstack1ll1ll11111_opy_ = bstack1ll1ll1l111_opy_ if bstack1ll1ll1l111_opy_ else bstack1ll1ll11111_opy_
        if not bstack1ll1ll11111_opy_:
            raise ValueError(bstack1l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨᅊ"))
    except Exception as ex:
        logger.debug(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡰࡦࡺࡥࡴࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡿࢂࠨᅋ").format(ex))
        bstack1ll1ll11111_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠢᅌ"))
        if bstack1ll1ll11111_opy_:
            logger.debug(bstack1l1111_opy_ (u"ࠧࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡷࡵ࡭ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࡀࠠࠣᅍ") + str(bstack1ll1ll11111_opy_) + bstack1l1111_opy_ (u"ࠨࠢᅎ"))
        else:
            logger.debug(bstack1l1111_opy_ (u"ࠢࡏࡱࠣࡺࡦࡲࡩࡥࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࡀࠦࡳࡦࡶࡸࡴࠥࡳࡡࡺࠢࡥࡩࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠥᅏ"))
    return bstack1ll1ll11111_opy_, bstack1ll1lllll1l_opy_
bstack1ll1l1l1l1l_opy_ = bstack1l1111_opy_ (u"ࠣ࠻࠼࠽࠾ࠨᅐ")
bstack1ll1lll1l1l_opy_ = bstack1l1111_opy_ (u"ࠤࡵࡩࡦࡪࡹࠣᅑ")
bstack1ll1l111ll1_opy_ = bstack1l1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᅒ")
bstack1ll11l11l11_opy_ = bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡑࡏࡓࡕࡇࡑࡣࡆࡊࡄࡓࠤᅓ")
bstack1l1llll1l1_opy_ = bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᅔ")
bstack1ll11ll11ll_opy_ = re.compile(bstack1l1111_opy_ (u"ࡸࠢࠩࡁ࡬࠭࠳࠰ࠨࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࢂࡂࡔࠫ࠱࠮ࠧᅕ"))
bstack1ll1lll11ll_opy_ = bstack1l1111_opy_ (u"ࠢࡥࡧࡹࡩࡱࡵࡰ࡮ࡧࡱࡸࠧᅖ")
bstack1lll1111lll_opy_ = bstack1l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡑࡕࡇࡊࡥࡆࡂࡎࡏࡆࡆࡉࡋࠣᅗ")
bstack1ll1l11ll11_opy_ = [
    bstack1ll1l11l_opy_.bstack1ll1l1ll11_opy_,
    bstack1ll1l11l_opy_.CONNECT,
    bstack1ll1l11l_opy_.bstack1l1l11ll11_opy_,
]
class SDKCLI:
    _1ll1ll1l11l_opy_ = None
    process: Union[None, Any]
    bstack1ll111ll111_opy_: bool
    bstack1ll111ll1l1_opy_: bool
    bstack1ll1l11llll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll11l1ll11_opy_: Union[None, grpc.Channel]
    bstack1lll1111l11_opy_: str
    test_framework: TestFramework
    bstack1lll11ll1l1_opy_: bstack1lll1ll1l1l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l111l11_opy_: bstack1ll11ll1111_opy_
    accessibility: bstack1ll1ll1l1l1_opy_
    bstack1llll1ll11_opy_: bstack11ll1lll1_opy_
    ai: bstack1ll1111ll1l_opy_
    bstack1ll1l1111ll_opy_: bstack1ll1l11111l_opy_
    bstack1ll11l111ll_opy_: List[bstack1ll1ll111l1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll1l111lll_opy_: Any
    bstack1lll111111l_opy_: Dict[str, timedelta]
    bstack1ll1ll1llll_opy_: str
    bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_
    def __new__(cls):
        if not cls._1ll1ll1l11l_opy_:
            cls._1ll1ll1l11l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1ll1l11l_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll111ll111_opy_ = False
        self.bstack1ll11l1ll11_opy_ = None
        self.bstack1ll1111l1ll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll11l11l11_opy_, None)
        self.bstack1lll111l111_opy_ = os.environ.get(bstack1ll1l111ll1_opy_, bstack1l1111_opy_ (u"ࠤࠥᅘ")) == bstack1l1111_opy_ (u"ࠥࠦᅙ")
        self.bstack1ll111ll1l1_opy_ = False
        self.bstack1ll1l11llll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll1l111lll_opy_ = None
        self.test_framework = None
        self.bstack1lll11ll1l1_opy_ = None
        self.bstack1lll1111l11_opy_=bstack1l1111_opy_ (u"ࠦࠧᅚ")
        self.session_framework = None
        self.logger = bstack111llll1ll_opy_.get_logger(self.__class__.__name__, bstack111llll1ll_opy_.bstack1ll11l1l111_opy_())
        self.bstack1lll111111l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lll1llll1l_opy_ = bstack1lll1lllll1_opy_()
        self.bstack1ll111l1ll1_opy_ = None
        self.bstack1ll1l1ll1ll_opy_ = None
        self.bstack1ll1l111l11_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll11l111ll_opy_ = []
    def bstack1l111111l1_opy_(self):
        return os.environ.get(bstack1l1llll1l1_opy_).lower().__eq__(bstack1l1111_opy_ (u"ࠧࡺࡲࡶࡧࠥᅛ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1lll1111lll_opy_, bstack1l1111_opy_ (u"࠭ࠧᅜ")).lower() in [bstack1l1111_opy_ (u"ࠧࡵࡴࡸࡩࠬᅝ"), bstack1l1111_opy_ (u"ࠨ࠳ࠪᅞ"), bstack1l1111_opy_ (u"ࠩࡼࡩࡸ࠭ᅟ")]:
            self.logger.debug(bstack1l1111_opy_ (u"ࠥࡊࡴࡸࡣࡪࡰࡪࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦ࡭ࡰࡦࡨࠤࡩࡻࡥࠡࡶࡲࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠦᅠ"))
            os.environ[bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᅡ")] = bstack1l1111_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᅢ")
            return False
        if bstack1l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᅣ") in config and str(config[bstack1l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᅤ")]).lower() != bstack1l1111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᅥ"):
            return False
        bstack1ll1l1llll1_opy_ = [bstack1l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᅦ"), bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᅧ")]
        bstack1ll1l1ll111_opy_ = config.get(bstack1l1111_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢᅨ")) in bstack1ll1l1llll1_opy_ or os.environ.get(bstack1l1111_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ᅩ")) in bstack1ll1l1llll1_opy_
        os.environ[bstack1l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤᅪ")] = str(bstack1ll1l1ll111_opy_) # bstack1lll1111111_opy_ bstack1lll111l1ll_opy_ VAR to bstack1lll111l11l_opy_ is binary running
        return bstack1ll1l1ll111_opy_
    def bstack1llll1l11_opy_(self):
        for event in bstack1ll1l11ll11_opy_:
            bstack1ll1111ll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1ll1111ll_opy_.logger.debug(bstack1l1111_opy_ (u"ࠢࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂࠦ࠽࠿ࠢࡾࡥࡷ࡭ࡳࡾࠢࠥᅫ") + str(kwargs) + bstack1l1111_opy_ (u"ࠣࠤᅬ"))
            )
        bstack1ll1111ll_opy_.register(bstack1ll1l11l_opy_.bstack1ll1l1ll11_opy_, self.__1ll111ll1ll_opy_)
        bstack1ll1111ll_opy_.register(bstack1ll1l11l_opy_.CONNECT, self.__1ll1l1lll1l_opy_)
        bstack1ll1111ll_opy_.register(bstack1ll1l11l_opy_.bstack1l1l11ll11_opy_, self.__1ll1l1l111l_opy_)
        bstack1ll1111ll_opy_.register(bstack1ll1l11l_opy_.bstack1l1l1l111l_opy_, self.__1ll1ll1ll1l_opy_)
    def bstack1l1l11llll_opy_(self):
        return not self.bstack1lll111l111_opy_ and os.environ.get(bstack1ll1l111ll1_opy_, bstack1l1111_opy_ (u"ࠤࠥᅭ")) != bstack1l1111_opy_ (u"ࠥࠦᅮ")
    def is_running(self):
        if self.bstack1lll111l111_opy_:
            return self.bstack1ll111ll111_opy_
        else:
            return bool(self.bstack1ll11l1ll11_opy_)
    def bstack1lll111ll11_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll11l111ll_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll1l1111l1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll111llll1_opy_(self, bstack1ll1llll1ll_opy_=10):
        if self.bstack1ll1111l1ll_opy_:
            return
        bstack1ll1lll11l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll11l11l11_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡠࠨᅯ") + str(id(self)) + bstack1l1111_opy_ (u"ࠧࡣࠠࡤࡱࡱࡲࡪࡩࡴࡪࡰࡪࠦᅰ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l1111_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡡࡳࡶࡴࡾࡹࠣᅱ"), 0), (bstack1l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡶࡣࡵࡸ࡯ࡹࡻࠥᅲ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll1llll1ll_opy_)
        self.bstack1ll11l1ll11_opy_ = channel
        self.bstack1ll1111l1ll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll11l1ll11_opy_)
        self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺࠢᅳ"), datetime.now() - bstack1ll1lll11l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll11l11l11_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l1111_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧ࠾ࠥ࡯ࡳࡠࡥ࡫࡭ࡱࡪ࡟ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤᅴ") + str(self.bstack1l1l11llll_opy_()) + bstack1l1111_opy_ (u"ࠥࠦᅵ"))
    def __1ll1l1l111l_opy_(self, event_name):
        if self.bstack1l1l11llll_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡄࡎࡌࠦᅶ"))
        self.__1ll11ll111l_opy_()
    @measure(event_name=EVENTS.bstack1ll11llll11_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll1ll1ll1l_opy_(self, event_name, bstack1ll111l11l1_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1l1111_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠧᅷ"))
        bstack1ll11l1l1ll_opy_ = Path(bstack1ll1ll1l1ll_opy_ (u"ࠨࡻࡴࡧ࡯ࡪ࠳ࡩ࡬ࡪࡡࡧ࡭ࡷࢃ࠯ࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࡴ࠰࡭ࡷࡴࡴࠢᅸ"))
        if self.bstack1ll1lllll1l_opy_ and bstack1ll11l1l1ll_opy_.exists():
            with open(bstack1ll11l1l1ll_opy_, bstack1l1111_opy_ (u"ࠧࡳࠩᅹ"), encoding=bstack1l1111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᅺ")) as fp:
                data = json.load(fp)
                try:
                    bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᅻ"), bstack111lll1l1_opy_(bstack1lll1l111_opy_), data, {
                        bstack1l1111_opy_ (u"ࠪࡥࡺࡺࡨࠨᅼ"): (self.config[bstack1l1111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᅽ")], self.config[bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᅾ")])
                    })
                except Exception as e:
                    logger.debug(bstack1ll1l1ll1_opy_.format(str(e)))
            bstack1ll11l1l1ll_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll11lll1l1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll111ll1ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
        self.bstack1lll1111l11_opy_, self.bstack1ll1lllll1l_opy_ = bstack1ll11ll1lll_opy_(data.bs_config)
        os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡝ࡒࡊࡖࡄࡆࡑࡋ࡟ࡅࡋࡕࠫᅿ")] = self.bstack1ll1lllll1l_opy_
        if not self.bstack1lll1111l11_opy_ or not self.bstack1ll1lllll1l_opy_:
            raise ValueError(bstack1l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠨᆀ"))
        if self.bstack1l1l11llll_opy_():
            self.__1ll1l1lll1l_opy_(event_name, bstack1ll111llll_opy_())
            return
        try:
            logger.debug(bstack1l1111_opy_ (u"ࠣࡅࡲࡱࡵࡲࡥࡵࡧࠣࡗࡉࡑࠠࡔࡧࡷࡹࡵ࠴ࠢᆁ"))
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡿࢂࠨᆂ").format(e))
        start = datetime.now()
        is_started = self.__1ll1l1lll11_opy_()
        self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥࡷࡵࡧࡷ࡯ࡡࡷ࡭ࡲ࡫ࠢᆃ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll111llll1_opy_()
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥᆄ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1111llll_opy_(data)
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᆅ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll11ll1l1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll1l1lll1l_opy_(self, event_name: str, data: bstack1ll111llll_opy_):
        if not self.bstack1l1l11llll_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࡳࡵࡴࠡࡣࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥᆆ"))
            return
        bin_session_id = os.environ.get(bstack1ll1l111ll1_opy_)
        start = datetime.now()
        self.__1ll111llll1_opy_()
        self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨᆇ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l1111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡆࡐࡎࠦࠢᆈ") + str(bin_session_id) + bstack1l1111_opy_ (u"ࠤࠥᆉ"))
        start = datetime.now()
        self.__1ll1lll1111_opy_()
        self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᆊ"), datetime.now() - start)
    def __1ll1lllllll_opy_(self):
        if not self.bstack1ll1111l1ll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠ࡮ࡱࡧࡹࡱ࡫ࡳࠣᆋ"))
            return
        bstack1ll1l1l1ll1_opy_ = {
            bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᆌ"): (bstack1ll1l11ll1l_opy_, bstack1ll111lll1l_opy_, bstack1ll1ll11ll1_opy_),
            bstack1l1111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᆍ"): (bstack1ll1ll11lll_opy_, bstack1ll11l1l1l1_opy_, bstack1ll1l111l1l_opy_),
        }
        if not self.bstack1ll111l1ll1_opy_ and self.session_framework in bstack1ll1l1l1ll1_opy_:
            bstack1ll1lll1lll_opy_, bstack1ll1ll11l1l_opy_, bstack1ll1111ll11_opy_ = bstack1ll1l1l1ll1_opy_[self.session_framework]
            bstack1ll1l1l1lll_opy_ = bstack1ll1ll11l1l_opy_()
            self.bstack1ll1l1ll1ll_opy_ = bstack1ll1l1l1lll_opy_
            self.bstack1ll111l1ll1_opy_ = bstack1ll1111ll11_opy_
            self.bstack1ll11l111ll_opy_.append(bstack1ll1l1l1lll_opy_)
            self.bstack1ll11l111ll_opy_.append(bstack1ll1lll1lll_opy_(self.bstack1ll1l1ll1ll_opy_))
        if not self.bstack1ll1l111l11_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1l11lll1_opy_
            self.bstack1ll1l111l11_opy_ = bstack1ll11ll1111_opy_(self.bstack1ll111l1ll1_opy_, self.bstack1ll1l1ll1ll_opy_) # bstack1ll111ll11l_opy_
            self.bstack1ll11l111ll_opy_.append(self.bstack1ll1l111l11_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1ll1l1l1_opy_(self.bstack1ll111l1ll1_opy_, self.bstack1ll1l1ll1ll_opy_)
            self.bstack1ll11l111ll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l1111_opy_ (u"ࠢࡴࡧ࡯ࡪࡍ࡫ࡡ࡭ࠤᆎ"), False) == True:
            self.ai = bstack1ll1111ll1l_opy_()
            self.bstack1ll11l111ll_opy_.append(self.ai)
        if not self.percy and self.bstack1ll1l111lll_opy_ and self.bstack1ll1l111lll_opy_.success:
            self.percy = bstack1ll1l11111l_opy_(self.bstack1ll1l111lll_opy_)
            self.bstack1ll11l111ll_opy_.append(self.percy)
        for mod in self.bstack1ll11l111ll_opy_:
            if not mod.bstack1ll11l1lll1_opy_():
                mod.configure(self.bstack1ll1111l1ll_opy_, self.config, self.cli_bin_session_id, self.bstack1lll1llll1l_opy_)
    def __1ll1lll11l1_opy_(self):
        for mod in self.bstack1ll11l111ll_opy_:
            if mod.bstack1ll11l1lll1_opy_():
                mod.configure(self.bstack1ll1111l1ll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1l1ll1l1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll1111llll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll111ll1l1_opy_:
            return
        self.__1ll11lll1ll_opy_(data)
        bstack1ll1lll11l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l1111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣᆏ")
        req.sdk_language = bstack1l1111_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤᆐ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll11ll11ll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᆑ"), bstack1l1111_opy_ (u"ࠫ࠵࠭ᆒ")))
            req.client_worker_id = bstack1l1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᆓ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡧࡨ࡮ࡴࡧࠡࡹࡲࡶࡰ࡫ࡲࠡࡣࡱࡨࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡰࡧࡩࡽࡀࠠࡼࡿࠥᆔ").format(e))
        try:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢ࡜ࠤᆕ") + str(id(self)) + bstack1l1111_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᆖ"))
            r = self.bstack1ll1111l1ll_opy_.StartBinSession(req)
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᆗ"), datetime.now() - bstack1ll1lll11l_opy_)
            os.environ[bstack1ll1l111ll1_opy_] = r.bin_session_id
            self.__1ll1llllll1_opy_(r)
            self.__1ll1lllllll_opy_()
            self.bstack1lll1llll1l_opy_.start()
            self.bstack1ll111ll1l1_opy_ = True
            self.logger.debug(bstack1l1111_opy_ (u"ࠥ࡟ࠧᆘ") + str(id(self)) + bstack1l1111_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤᆙ"))
        except grpc.bstack1lll1111l1l_opy_ as bstack1ll111l1l1l_opy_:
            self.logger.error(bstack1l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᆚ") + str(bstack1ll111l1l1l_opy_) + bstack1l1111_opy_ (u"ࠨࠢᆛ"))
            traceback.print_exc()
            raise bstack1ll111l1l1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᆜ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᆝ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1111l1l1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll1lll1111_opy_(self):
        if not self.bstack1l1l11llll_opy_() or not self.cli_bin_session_id or self.bstack1ll1l11llll_opy_:
            return
        bstack1ll1lll11l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᆞ"), bstack1l1111_opy_ (u"ࠪ࠴ࠬᆟ")))
        req.client_worker_id = bstack1l1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᆠ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡡࠢᆡ") + str(id(self)) + bstack1l1111_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆢ"))
            r = self.bstack1ll1111l1ll_opy_.ConnectBinSession(req)
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᆣ"), datetime.now() - bstack1ll1lll11l_opy_)
            self.__1ll1llllll1_opy_(r)
            self.__1ll1lllllll_opy_()
            self.bstack1lll1llll1l_opy_.start()
            self.bstack1ll1l11llll_opy_ = True
            self.logger.debug(bstack1l1111_opy_ (u"ࠣ࡝ࠥᆤ") + str(id(self)) + bstack1l1111_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣᆥ"))
        except grpc.bstack1lll1111l1l_opy_ as bstack1ll111l1l1l_opy_:
            self.logger.error(bstack1l1111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᆦ") + str(bstack1ll111l1l1l_opy_) + bstack1l1111_opy_ (u"ࠦࠧᆧ"))
            traceback.print_exc()
            raise bstack1ll111l1l1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᆨ") + str(e) + bstack1l1111_opy_ (u"ࠨࠢᆩ"))
            traceback.print_exc()
            raise e
    def __1ll1llllll1_opy_(self, r):
        self.bstack1ll1lll1ll1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l1111_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᆪ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l1111_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨᆫ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᆬ")
        self.bstack1ll1l111lll_opy_ = getattr(r, bstack1l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᆭ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᆮ")] = self.config_testhub.jwt
        os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᆯ")] = self.config_testhub.build_hashed_id
    def bstack1lll111l1l1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll111ll111_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll11l1ll1l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll11l1ll1l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll111l1l1_opy_(event_name=EVENTS.bstack1ll11l11111_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll1l1lll11_opy_(self, bstack1ll1llll1ll_opy_=10):
        if self.bstack1ll111ll111_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣᆰ"))
            return True
        self.logger.debug(bstack1l1111_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᆱ"))
        if os.getenv(bstack1l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣᆲ")) == bstack1ll1lll11ll_opy_:
            self.cli_bin_session_id = bstack1ll1lll11ll_opy_
            self.cli_listen_addr = bstack1l1111_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧᆳ") % (self.cli_bin_session_id)
            self.bstack1ll111ll111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1111l11_opy_, bstack1l1111_opy_ (u"ࠥࡷࡩࡱࠢᆴ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1l1l11ll_opy_ compat for text=True in bstack1ll11lll111_opy_ python
            encoding=bstack1l1111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᆵ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1l1l11l1_opy_ = threading.Thread(target=self.__1ll1l1ll11l_opy_, args=(bstack1ll1llll1ll_opy_,))
        bstack1ll1l1l11l1_opy_.start()
        bstack1ll1l1l11l1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤᆶ") + str(self.process.stderr.read()) + bstack1l1111_opy_ (u"ࠨࠢᆷ"))
        if not self.bstack1ll111ll111_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢ࡜ࠤᆸ") + str(id(self)) + bstack1l1111_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦᆹ"))
            self.__1ll11ll111l_opy_()
        self.logger.debug(bstack1l1111_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥᆺ") + str(self.bstack1ll111ll111_opy_) + bstack1l1111_opy_ (u"ࠥࠦᆻ"))
        return self.bstack1ll111ll111_opy_
    def __1ll1l1ll11l_opy_(self, bstack1ll1l11l111_opy_=10):
        bstack1ll111l1111_opy_ = time.time()
        while self.process and time.time() - bstack1ll111l1111_opy_ < bstack1ll1l11l111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l1111_opy_ (u"ࠦ࡮ࡪ࠽ࠣᆼ") in line:
                    self.cli_bin_session_id = line.split(bstack1l1111_opy_ (u"ࠧ࡯ࡤ࠾ࠤᆽ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1111_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧᆾ") + str(self.cli_bin_session_id) + bstack1l1111_opy_ (u"ࠢࠣᆿ"))
                    continue
                if bstack1l1111_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᇀ") in line:
                    self.cli_listen_addr = line.split(bstack1l1111_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᇁ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1111_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨᇂ") + str(self.cli_listen_addr) + bstack1l1111_opy_ (u"ࠦࠧᇃ"))
                    continue
                if bstack1l1111_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᇄ") in line:
                    port = line.split(bstack1l1111_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᇅ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1111_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨᇆ") + str(port) + bstack1l1111_opy_ (u"ࠣࠤᇇ"))
                    continue
                if line.strip() == bstack1ll1lll1l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l1111_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦᇈ"), bstack1l1111_opy_ (u"ࠥ࠵ࠧᇉ")) == bstack1l1111_opy_ (u"ࠦ࠶ࠨᇊ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll111ll111_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨᇋ") + str(e) + bstack1l1111_opy_ (u"ࠨࠢᇌ"))
        return False
    @measure(event_name=EVENTS.bstack1ll1ll1111l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def __1ll11ll111l_opy_(self):
        if self.bstack1ll11l1ll11_opy_:
            self.bstack1lll1llll1l_opy_.stop()
            start = datetime.now()
            if self.bstack1ll11l111l1_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll1l11llll_opy_:
                    self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᇍ"), datetime.now() - start)
                else:
                    self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᇎ"), datetime.now() - start)
            self.__1ll1lll11l1_opy_()
            start = datetime.now()
            bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(bstack1l1111_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽ࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺࠢᇏ"))
            self.bstack1ll11l1ll11_opy_.close()
            bstack11ll111lll_opy_.end(bstack1l1111_opy_ (u"ࠥࡷࡩࡱ࠺ࡤ࡮࡬࠾ࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࠣᇐ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᇑ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᇒ"), True, None, None, None, None)
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠨࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᇓ"), datetime.now() - start)
            self.bstack1ll11l1ll11_opy_ = None
        if self.process:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡴࡶࡲࡴࠧᇔ"))
            start = datetime.now()
            bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(bstack1l1111_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡮࡭ࡱࡲࠢᇕ"))
            self.process.terminate()
            bstack11ll111lll_opy_.end(bstack1l1111_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽࡯࡮ࡲ࡬ࠣᇖ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᇗ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᇘ"), True, None, None, None, None)
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣᇙ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll111l111_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1ll11ll1ll_opy_()
                self.logger.info(
                    bstack1l1111_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳࠨᇚ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l1111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᇛ")] = self.config_testhub.build_hashed_id
        self.bstack1ll111ll111_opy_ = False
    def __1ll11lll1ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1l1111_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᇜ")] = selenium.__version__
            data.frameworks.append(bstack1l1111_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᇝ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1l1111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᇞ")] = __version__
            data.frameworks.append(bstack1l1111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᇟ"))
        except:
            pass
    def bstack1ll111l1l11_opy_(self, hub_url: str, platform_index: int, bstack1l1l1lllll_opy_: Any):
        if self.bstack1lll11ll1l1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᇠ"))
            return
        try:
            bstack1ll1lll11l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l1111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᇡ")
            self.bstack1lll11ll1l1_opy_ = bstack1ll1l111l1l_opy_(
                cli.config.get(bstack1l1111_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢᇢ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll11111l1_opy_={bstack1l1111_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧᇣ"): bstack1l1l1lllll_opy_}
            )
            def bstack1ll1ll11l11_opy_(self):
                return
            if self.config.get(bstack1l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦᇤ"), True):
                Service.start = bstack1ll1ll11l11_opy_
                Service.stop = bstack1ll1ll11l11_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11ll1lll1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1ll1ll11_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᇥ"), datetime.now() - bstack1ll1lll11l_opy_)
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥᇦ") + str(e) + bstack1l1111_opy_ (u"ࠧࠨᇧ"))
    def bstack1lll1111ll1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1ll11111ll_opy_
            self.bstack1lll11ll1l1_opy_ = bstack1ll1ll11ll1_opy_(
                platform_index,
                framework_name=bstack1l1111_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᇨ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣᇩ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᇪ"))
            pass
    def bstack1ll11lllll1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᇫ"))
            return
        if bstack1llllll1l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᇬ"): pytest.__version__ }, [bstack1l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᇭ")], self.bstack1lll1llll1l_opy_, self.bstack1ll1111l1ll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1l1lllll_opy_({ bstack1l1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᇮ"): pytest.__version__ }, [bstack1l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᇯ")], self.bstack1lll1llll1l_opy_, self.bstack1ll1111l1ll_opy_)
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦᇰ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᇱ"))
        self.bstack1ll1llll111_opy_()
    def bstack1ll1llll111_opy_(self):
        if not self.bstack1l111111l1_opy_():
            return
        bstack1ll1l1l1l_opy_ = None
        def bstack1l1111111l_opy_(config, startdir):
            return bstack1l1111_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢᇲ").format(bstack1l1111_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᇳ"))
        def bstack11lllll11l_opy_():
            return
        def bstack11l111llll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l1111_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᇴ"):
                return bstack1l1111_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᇵ")
            else:
                return bstack1ll1l1l1l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll1l1l1l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l1111111l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11lllll11l_opy_
            Config.getoption = bstack11l111llll_opy_
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣᇶ") + str(e) + bstack1l1111_opy_ (u"ࠢࠣᇷ"))
    def bstack1ll11l11ll1_opy_(self):
        bstack1ll11l1l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll11l1l1_opy_, dict):
            if cli.config_observability:
                bstack1ll11l1l1_opy_.update(
                    {bstack1l1111_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣᇸ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l1111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧᇹ") in accessibility.get(bstack1l1111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᇺ"), {}):
                    bstack1ll11l11l1l_opy_ = accessibility.get(bstack1l1111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᇻ"))
                    bstack1ll11l11l1l_opy_.update({ bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨᇼ"): bstack1ll11l11l1l_opy_.pop(bstack1l1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᇽ")) })
                bstack1ll11l1l1_opy_.update({bstack1l1111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᇾ"): accessibility })
        return bstack1ll11l1l1_opy_
    @measure(event_name=EVENTS.bstack1ll1111lll1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1ll11l111l1_opy_(self, bstack1ll111lll11_opy_: str = None, bstack1ll11llllll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1111l1ll_opy_:
            return
        bstack1ll1lll11l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᇿ"), bstack1l1111_opy_ (u"ࠩ࠳ࠫሀ")))
        req.client_worker_id = bstack1l1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤሁ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll111lll11_opy_:
            req.bstack1ll111lll11_opy_ = bstack1ll111lll11_opy_
        if bstack1ll11llllll_opy_:
            req.bstack1ll11llllll_opy_ = bstack1ll11llllll_opy_
        try:
            r = self.bstack1ll1111l1ll_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧሂ"), datetime.now() - bstack1ll1lll11l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11l1l11ll_opy_(self, key: str, value: timedelta):
        tag = bstack1l1111_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧሃ") if self.bstack1l1l11llll_opy_() else bstack1l1111_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧሄ")
        self.bstack1lll111111l_opy_[bstack1l1111_opy_ (u"ࠢ࠻ࠤህ").join([tag + bstack1l1111_opy_ (u"ࠣ࠯ࠥሆ") + str(id(self)), key])] += value
    def bstack1ll11ll1ll_opy_(self):
        if not os.getenv(bstack1l1111_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨሇ"), bstack1l1111_opy_ (u"ࠥ࠴ࠧለ")) == bstack1l1111_opy_ (u"ࠦ࠶ࠨሉ"):
            return
        bstack1ll1llll11l_opy_ = dict()
        bstack1lll11ll1ll_opy_ = []
        if self.test_framework:
            bstack1lll11ll1ll_opy_.extend(list(self.test_framework.bstack1lll11ll1ll_opy_.values()))
        if self.bstack1lll11ll1l1_opy_:
            bstack1lll11ll1ll_opy_.extend(list(self.bstack1lll11ll1l1_opy_.bstack1lll11ll1ll_opy_.values()))
        for instance in bstack1lll11ll1ll_opy_:
            if not instance.platform_index in bstack1ll1llll11l_opy_:
                bstack1ll1llll11l_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll1llll11l_opy_[instance.platform_index]
            for k, v in instance.bstack1ll11l1111l_opy_().items():
                report[k] += v
                report[k.split(bstack1l1111_opy_ (u"ࠧࡀࠢሊ"))[0]] += v
        bstack1ll1ll1lll1_opy_ = sorted([(k, v) for k, v in self.bstack1lll111111l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll11ll11l1_opy_ = 0
        for r in bstack1ll1ll1lll1_opy_:
            bstack1ll1lll111l_opy_ = r[1].total_seconds()
            bstack1ll11ll11l1_opy_ += bstack1ll1lll111l_opy_
            self.logger.debug(bstack1l1111_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦላ") + str(bstack1ll1lll111l_opy_) + bstack1l1111_opy_ (u"ࠢࠣሌ"))
        self.logger.debug(bstack1l1111_opy_ (u"ࠣ࠯࠰ࠦል"))
        bstack1ll11l1llll_opy_ = []
        for platform_index, report in bstack1ll1llll11l_opy_.items():
            bstack1ll11l1llll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll11l1llll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l11l1ll_opy_ = set()
        bstack1ll111l11ll_opy_ = 0
        for r in bstack1ll11l1llll_opy_:
            bstack1ll1lll111l_opy_ = r[2].total_seconds()
            bstack1ll111l11ll_opy_ += bstack1ll1lll111l_opy_
            bstack1l11l1ll_opy_.add(r[0])
            self.logger.debug(bstack1l1111_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥሎ") + str(bstack1ll1lll111l_opy_) + bstack1l1111_opy_ (u"ࠥࠦሏ"))
        if self.bstack1l1l11llll_opy_():
            self.logger.debug(bstack1l1111_opy_ (u"ࠦ࠲࠳ࠢሐ"))
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧሑ") + str(bstack1ll111l11ll_opy_) + bstack1l1111_opy_ (u"ࠨࠢሒ"))
        else:
            self.logger.debug(bstack1l1111_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦሓ") + str(bstack1ll11ll11l1_opy_) + bstack1l1111_opy_ (u"ࠣࠤሔ"))
        self.logger.debug(bstack1l1111_opy_ (u"ࠤ࠰࠱ࠧሕ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪሖ"), bstack1l1111_opy_ (u"ࠫ࠵࠭ሗ"))),
            client_worker_id=bstack1l1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦመ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1111l1ll_opy_:
            self.logger.error(bstack1l1111_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥሙ"))
            return None
        response = self.bstack1ll1111l1ll_opy_.TestOrchestration(request)
        self.logger.debug(bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤሚ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1lll1ll1_opy_(self, r):
        if r is not None and getattr(r, bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩማ"), None) and getattr(r.testhub, bstack1l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩሜ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤም")))
            for bstack1ll1llll1l1_opy_, err in errors.items():
                if err[bstack1l1111_opy_ (u"ࠫࡹࡿࡰࡦࠩሞ")] == bstack1l1111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪሟ"):
                    self.logger.info(err[bstack1l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧሠ")])
                else:
                    self.logger.error(err[bstack1l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨሡ")])
    def bstack11lll111l_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()