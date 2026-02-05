# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
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
from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1ll1llll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111lll_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l1l_opy_ import bstack1ll11ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l11_opy_ import bstack1ll1l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11lll1_opy_ import bstack1ll1l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11ll1_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack11lll11ll1_opy_ import bstack11lll11ll1_opy_, bstack1l1ll1l1ll_opy_, bstack111lll11l1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll1l1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll111ll1l1_opy_
from bstack_utils.helper import Notset, bstack1ll1l1l1l11_opy_, get_cli_dir, bstack1ll111lll11_opy_, bstack1l1l1l1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll1111ll1_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1111_opy_ import bstack11l1l1lll_opy_
from bstack_utils.helper import Notset, bstack1ll1l1l1l11_opy_, get_cli_dir, bstack1ll111lll11_opy_, bstack1l1l1l1l1l_opy_, bstack111l11l1ll_opy_, bstack1ll1111ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11l1l1l1_opy_, bstack1ll1ll111l1_opy_, bstack1ll1111llll_opy_, bstack1ll1lll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll11lll1l_opy_, bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1111l111l_opy_ import bstack11l1l1ll11_opy_
from bstack_utils import bstack1l1111l1l_opy_
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111l11l111_opy_, bstack11l1ll111_opy_
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
logger = bstack1l1111l1l_opy_.get_logger(__name__, bstack1l1111l1l_opy_.bstack1lll111l11l_opy_())
def bstack1lll111l111_opy_(bs_config):
    bstack1ll11lll1l1_opy_ = None
    bstack1ll11lll111_opy_ = None
    try:
        bstack1ll11lll111_opy_ = get_cli_dir()
        bstack1ll11lll1l1_opy_ = bstack1ll111lll11_opy_(bstack1ll11lll111_opy_)
        bstack1ll1l1ll11l_opy_ = bstack1ll1l1l1l11_opy_(bstack1ll11lll1l1_opy_, bstack1ll11lll111_opy_, bs_config)
        bstack1ll11lll1l1_opy_ = bstack1ll1l1ll11l_opy_ if bstack1ll1l1ll11l_opy_ else bstack1ll11lll1l1_opy_
        if not bstack1ll11lll1l1_opy_:
            raise ValueError(bstack11l1ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦᅏ"))
    except Exception as ex:
        logger.debug(bstack11l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦᅐ").format(ex))
        bstack1ll11lll1l1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧᅑ"))
        if bstack1ll11lll1l1_opy_:
            logger.debug(bstack11l1ll1_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨᅒ") + str(bstack1ll11lll1l1_opy_) + bstack11l1ll1_opy_ (u"ࠦࠧᅓ"))
        else:
            logger.debug(bstack11l1ll1_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣᅔ"))
    return bstack1ll11lll1l1_opy_, bstack1ll11lll111_opy_
bstack1ll111l1111_opy_ = bstack11l1ll1_opy_ (u"ࠨ࠹࠺࠻࠼ࠦᅕ")
bstack1ll1lll1111_opy_ = bstack11l1ll1_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨᅖ")
bstack1ll1111l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᅗ")
bstack1ll1l1ll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢᅘ")
bstack11l1111l1l_opy_ = bstack11l1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᅙ")
bstack1ll11llll1l_opy_ = re.compile(bstack11l1ll1_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥᅚ"))
bstack1lll1111l11_opy_ = bstack11l1ll1_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥᅛ")
bstack1ll11l111l1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡏࡓࡅࡈࡣࡋࡇࡌࡍࡄࡄࡇࡐࠨᅜ")
bstack1ll1lll1lll_opy_ = [
    bstack1l1ll1l1ll_opy_.bstack111l1l111l_opy_,
    bstack1l1ll1l1ll_opy_.CONNECT,
    bstack1l1ll1l1ll_opy_.bstack11ll1l1ll_opy_,
]
class SDKCLI:
    _1ll1l1lll11_opy_ = None
    process: Union[None, Any]
    bstack1ll1lllllll_opy_: bool
    bstack1ll1111ll11_opy_: bool
    bstack1ll11ll11l1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll111llll1_opy_: Union[None, grpc.Channel]
    bstack1ll1111l11l_opy_: str
    test_framework: TestFramework
    bstack1lll1l1lll1_opy_: bstack1lll111llll_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l1l11ll_opy_: bstack1ll111l1lll_opy_
    accessibility: bstack1ll1llll1l1_opy_
    bstack1lll1l1111_opy_: bstack11l1l1lll_opy_
    ai: bstack1lll111l1ll_opy_
    bstack1ll1l11ll1l_opy_: bstack1ll11l11111_opy_
    bstack1ll111ll1ll_opy_: List[bstack1ll1l11l1ll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll1ll11111_opy_: Any
    bstack1ll11l1l111_opy_: Dict[str, timedelta]
    bstack1ll1lll11l1_opy_: str
    bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_
    def __new__(cls):
        if not cls._1ll1l1lll11_opy_:
            cls._1ll1l1lll11_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1l1lll11_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1lllllll_opy_ = False
        self.bstack1ll111llll1_opy_ = None
        self.bstack1ll1llll1ll_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1l1ll1ll_opy_, None)
        self.bstack1ll11l11l1l_opy_ = os.environ.get(bstack1ll1111l1ll_opy_, bstack11l1ll1_opy_ (u"ࠢࠣᅝ")) == bstack11l1ll1_opy_ (u"ࠣࠤᅞ")
        self.bstack1ll1111ll11_opy_ = False
        self.bstack1ll11ll11l1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll1ll11111_opy_ = None
        self.test_framework = None
        self.bstack1lll1l1lll1_opy_ = None
        self.bstack1ll1111l11l_opy_=bstack11l1ll1_opy_ (u"ࠤࠥᅟ")
        self.session_framework = None
        self.logger = bstack1l1111l1l_opy_.get_logger(self.__class__.__name__, bstack1l1111l1l_opy_.bstack1lll111l11l_opy_())
        self.bstack1ll11l1l111_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lll1llll11_opy_ = bstack1lll1llll1l_opy_()
        self.bstack1ll111l111l_opy_ = False
        self.bstack1ll1lllll1l_opy_ = None
        self.bstack1ll1llllll1_opy_ = None
        self.bstack1ll1l1l11ll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll111ll1ll_opy_ = []
    def bstack1l1l1111l1_opy_(self):
        return os.environ.get(bstack11l1111l1l_opy_).lower().__eq__(bstack11l1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣᅠ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1ll11l111l1_opy_, bstack11l1ll1_opy_ (u"ࠫࠬᅡ")).lower() in [bstack11l1ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪᅢ"), bstack11l1ll1_opy_ (u"࠭࠱ࠨᅣ"), bstack11l1ll1_opy_ (u"ࠧࡺࡧࡶࠫᅤ")]:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡈࡲࡶࡨ࡯࡮ࡨࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡲࡵࡤࡦࠢࡧࡹࡪࠦࡴࡰࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡒࡖࡈࡋ࡟ࡇࡃࡏࡐࡇࡇࡃࡌࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠤᅥ"))
            os.environ[bstack11l1ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᅦ")] = bstack11l1ll1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᅧ")
            return False
        if bstack11l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᅨ") in config and str(config[bstack11l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᅩ")]).lower() != bstack11l1ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᅪ"):
            return False
        bstack1ll11l1llll_opy_ = [bstack11l1ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᅫ"), bstack11l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᅬ")]
        bstack1ll1lll1ll1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᅭ")) in bstack1ll11l1llll_opy_ or os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫᅮ")) in bstack1ll11l1llll_opy_
        os.environ[bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᅯ")] = str(bstack1ll1lll1ll1_opy_) # bstack1ll111l1ll1_opy_ bstack1ll11lllll1_opy_ VAR to bstack1ll11l1ll11_opy_ is binary running
        return bstack1ll1lll1ll1_opy_
    def bstack1ll111lll1_opy_(self):
        for event in bstack1ll1lll1lll_opy_:
            bstack11lll11ll1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11lll11ll1_opy_.logger.debug(bstack11l1ll1_opy_ (u"ࠧࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠤࡂࡄࠠࡼࡣࡵ࡫ࡸࢃࠠࠣᅰ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠨࠢᅱ"))
            )
        bstack11lll11ll1_opy_.register(bstack1l1ll1l1ll_opy_.bstack111l1l111l_opy_, self.__1ll11ll11ll_opy_)
        bstack11lll11ll1_opy_.register(bstack1l1ll1l1ll_opy_.CONNECT, self.__1ll1llll11l_opy_)
        bstack11lll11ll1_opy_.register(bstack1l1ll1l1ll_opy_.bstack11ll1l1ll_opy_, self.__1ll1l1111l1_opy_)
        bstack11lll11ll1_opy_.register(bstack1l1ll1l1ll_opy_.bstack11lllll11l_opy_, self.__1ll1ll1l1ll_opy_)
    def bstack1l11lll1_opy_(self):
        return not self.bstack1ll11l11l1l_opy_ and os.environ.get(bstack1ll1111l1ll_opy_, bstack11l1ll1_opy_ (u"ࠢࠣᅲ")) != bstack11l1ll1_opy_ (u"ࠣࠤᅳ")
    def is_running(self):
        if self.bstack1ll11l11l1l_opy_:
            return self.bstack1ll1lllllll_opy_
        else:
            return bool(self.bstack1ll111llll1_opy_)
    def bstack1lll1111l1l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll111ll1ll_opy_) and cli.is_running()
    @measure(event_name=EVENTS.bstack1ll111l11ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1ll11111lll_opy_(self, bstack1ll1l111ll1_opy_=10):
        if self.bstack1ll1llll1ll_opy_:
            return
        bstack111ll1ll1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1l1ll1ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤ࡞ࠦᅴ") + str(id(self)) + bstack11l1ll1_opy_ (u"ࠥࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡯࡮ࡨࠤᅵ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11l1ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶ࡟ࡱࡴࡲࡼࡾࠨᅶ"), 0), (bstack11l1ll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡴࡡࡳࡶࡴࡾࡹࠣᅷ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll1l111ll1_opy_)
        self.bstack1ll111llll1_opy_ = channel
        self.bstack1ll1llll1ll_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll111llll1_opy_)
        self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࠧᅸ"), datetime.now() - bstack111ll1ll1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1l1ll1ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥ࠼ࠣ࡭ࡸࡥࡣࡩ࡫࡯ࡨࡤࡶࡲࡰࡥࡨࡷࡸࡃࠢᅹ") + str(self.bstack1l11lll1_opy_()) + bstack11l1ll1_opy_ (u"ࠣࠤᅺ"))
    def __1ll1l1111l1_opy_(self, event_name):
        if self.bstack1l11lll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡉࡌࡊࠤᅻ"))
        self.__1lll111111l_opy_()
    @measure(event_name=EVENTS.bstack1ll11llllll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1ll1ll1l1ll_opy_(self, event_name, bstack1ll111ll111_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠥᅼ"))
        bstack1ll1ll1l11l_opy_ = Path(bstack1ll1ll11l1l_opy_ (u"ࠦࢀࡹࡥ࡭ࡨ࠱ࡧࡱ࡯࡟ࡥ࡫ࡵࢁ࠴ࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࡹ࠮࡫ࡵࡲࡲࠧᅽ"))
        if self.bstack1ll11lll111_opy_ and bstack1ll1ll1l11l_opy_.exists():
            with open(bstack1ll1ll1l11l_opy_, bstack11l1ll1_opy_ (u"ࠬࡸࠧᅾ"), encoding=bstack11l1ll1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᅿ")) as fp:
                data = json.load(fp)
                try:
                    bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬᆀ"), bstack11l1l1ll11_opy_(bstack11l11ll11_opy_), data, {
                        bstack11l1ll1_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᆁ"): (self.config[bstack11l1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᆂ")], self.config[bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᆃ")])
                    })
                except Exception as e:
                    logger.debug(bstack11l1ll111_opy_.format(str(e)))
            bstack1ll1ll1l11l_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll11l1ll1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1ll11ll11ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
        self.bstack1ll1111l11l_opy_, self.bstack1ll11lll111_opy_ = bstack1lll111l111_opy_(data.bs_config)
        os.environ[bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡛ࡗࡏࡔࡂࡄࡏࡉࡤࡊࡉࡓࠩᆄ")] = self.bstack1ll11lll111_opy_
        if not self.bstack1ll1111l11l_opy_ or not self.bstack1ll11lll111_opy_:
            raise ValueError(bstack11l1ll1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡩࡧࠣࡗࡉࡑࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠦᆅ"))
        if self.bstack1l11lll1_opy_():
            self.__1ll1llll11l_opy_(event_name, bstack111lll11l1_opy_())
            return
        try:
            logger.debug(bstack11l1ll1_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧᆆ"))
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦᆇ").format(e))
        start = datetime.now()
        is_started = self.__1ll1l1l1lll_opy_()
        self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧᆈ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll11111lll_opy_()
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᆉ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll11lll11l_opy_(data)
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᆊ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll11l1l1ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1ll1llll11l_opy_(self, event_name: str, data: bstack111lll11l1_opy_):
        if not self.bstack1l11lll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᆋ"))
            return
        bin_session_id = os.environ.get(bstack1ll1111l1ll_opy_)
        start = datetime.now()
        self.__1ll11111lll_opy_()
        self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᆌ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧᆍ") + str(bin_session_id) + bstack11l1ll1_opy_ (u"ࠢࠣᆎ"))
        start = datetime.now()
        self.__1lll1111111_opy_()
        self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᆏ"), datetime.now() - start)
    def __1ll11ll111l_opy_(self):
        if not self.bstack1ll1llll1ll_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨᆐ"))
            return
        bstack1lll1111lll_opy_ = {
            bstack11l1ll1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᆑ"): (bstack1ll1lllll11_opy_, bstack1ll1l1lllll_opy_, bstack1ll111ll1l1_opy_),
            bstack11l1ll1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᆒ"): (bstack1ll11ll1111_opy_, bstack1ll1l11l11l_opy_, bstack1ll1ll1lll1_opy_),
        }
        if not self.bstack1ll1lllll1l_opy_ and self.session_framework in bstack1lll1111lll_opy_:
            bstack1ll111lll1l_opy_, bstack1ll11l1111l_opy_, bstack1ll1l111111_opy_ = bstack1lll1111lll_opy_[self.session_framework]
            bstack1ll11l1lll1_opy_ = bstack1ll11l1111l_opy_()
            self.bstack1ll1llllll1_opy_ = bstack1ll11l1lll1_opy_
            self.bstack1ll1lllll1l_opy_ = bstack1ll1l111111_opy_
            self.bstack1ll111ll1ll_opy_.append(bstack1ll11l1lll1_opy_)
            self.bstack1ll111ll1ll_opy_.append(bstack1ll111lll1l_opy_(self.bstack1ll1llllll1_opy_))
        if not self.bstack1ll1l1l11ll_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1l1l11l1_opy_
            self.bstack1ll1l1l11ll_opy_ = bstack1ll111l1lll_opy_(self.bstack1ll1lllll1l_opy_, self.bstack1ll1llllll1_opy_) # bstack1ll111l11l1_opy_
            self.bstack1ll111ll1ll_opy_.append(self.bstack1ll1l1l11ll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1llll1l1_opy_(self.bstack1ll1lllll1l_opy_, self.bstack1ll1llllll1_opy_)
            self.bstack1ll111ll1ll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11l1ll1_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢᆓ"), False) == True:
            self.ai = bstack1lll111l1ll_opy_()
            self.bstack1ll111ll1ll_opy_.append(self.ai)
        if not self.percy and self.bstack1ll1ll11111_opy_ and self.bstack1ll1ll11111_opy_.success:
            self.percy = bstack1ll11l11111_opy_(self.bstack1ll1ll11111_opy_)
            self.bstack1ll111ll1ll_opy_.append(self.percy)
        for mod in self.bstack1ll111ll1ll_opy_:
            if not mod.bstack1ll11l1l11l_opy_():
                mod.configure(self.bstack1ll1llll1ll_opy_, self.config, self.cli_bin_session_id, self.bstack1lll1llll11_opy_)
    def __1ll1lll111l_opy_(self):
        for mod in self.bstack1ll111ll1ll_opy_:
            if mod.bstack1ll11l1l11l_opy_():
                mod.configure(self.bstack1ll1llll1ll_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1ll111ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1ll11lll11l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1111ll11_opy_:
            return
        self.__1ll1l1ll111_opy_(data)
        bstack111ll1ll1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11l1ll1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᆔ")
        req.sdk_language = bstack11l1ll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᆕ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll11llll1l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            req.platform_index = str(os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᆖ"), bstack11l1ll1_opy_ (u"ࠩ࠳ࠫᆗ")))
            req.client_worker_id = bstack11l1ll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᆘ").format(threading.get_ident(), os.getpid())
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡷࡰࡴ࡮ࡩࡷࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥ࡯࡮ࡥࡧࡻ࠾ࠥࢁࡽࠣᆙ").format(e))
        try:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡡࠢᆚ") + str(id(self)) + bstack11l1ll1_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᆛ"))
            r = self.bstack1ll1llll1ll_opy_.StartBinSession(req)
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᆜ"), datetime.now() - bstack111ll1ll1_opy_)
            os.environ[bstack1ll1111l1ll_opy_] = r.bin_session_id
            self.__1ll1l1l111l_opy_(r)
            self.__1ll11ll111l_opy_()
            if not self.bstack1ll111l111l_opy_:
                self.bstack1lll1llll11_opy_.start()
                self.bstack1ll111l111l_opy_ = True
                atexit.register(self.__1lll11111ll_opy_)
            self.bstack1ll1111ll11_opy_ = True
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣ࡝ࠥᆝ") + str(id(self)) + bstack11l1ll1_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢᆞ"))
        except grpc.bstack1ll1l1llll1_opy_ as bstack1ll11ll1lll_opy_:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᆟ") + str(bstack1ll11ll1lll_opy_) + bstack11l1ll1_opy_ (u"ࠦࠧᆠ"))
            traceback.print_exc()
            raise bstack1ll11ll1lll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᆡ") + str(e) + bstack11l1ll1_opy_ (u"ࠨࠢᆢ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l11l11_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1lll1111111_opy_(self):
        if not self.bstack1l11lll1_opy_() or not self.cli_bin_session_id or self.bstack1ll11ll11l1_opy_:
            return
        bstack111ll1ll1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᆣ"), bstack11l1ll1_opy_ (u"ࠨ࠲ࠪᆤ")))
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᆥ").format(threading.get_ident(), os.getpid())
        try:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥ࡟ࠧᆦ") + str(id(self)) + bstack11l1ll1_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᆧ"))
            r = self.bstack1ll1llll1ll_opy_.ConnectBinSession(req)
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᆨ"), datetime.now() - bstack111ll1ll1_opy_)
            self.__1ll1l1l111l_opy_(r)
            self.__1ll11ll111l_opy_()
            if not self.bstack1ll111l111l_opy_:
                self.bstack1lll1llll11_opy_.start()
                self.bstack1ll111l111l_opy_ = True
                atexit.register(self.__1lll11111ll_opy_)
            self.bstack1ll11ll11l1_opy_ = True
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡛ࠣᆩ") + str(id(self)) + bstack11l1ll1_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨᆪ"))
        except grpc.bstack1ll1l1llll1_opy_ as bstack1ll11ll1lll_opy_:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᆫ") + str(bstack1ll11ll1lll_opy_) + bstack11l1ll1_opy_ (u"ࠤࠥᆬ"))
            traceback.print_exc()
            raise bstack1ll11ll1lll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᆭ") + str(e) + bstack11l1ll1_opy_ (u"ࠦࠧᆮ"))
            traceback.print_exc()
            raise e
    def __1ll1l1l111l_opy_(self, r):
        self.bstack1ll11l111ll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11l1ll1_opy_ (u"ࠧࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᆯ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11l1ll1_opy_ (u"ࠨࡥ࡮ࡲࡷࡽࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡯ࡶࡰࡧࠦᆰ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11l1ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕ࡫ࡲࡤࡻࠣ࡭ࡸࠦࡳࡦࡰࡷࠤࡴࡴ࡬ࡺࠢࡤࡷࠥࡶࡡࡳࡶࠣࡳ࡫ࠦࡴࡩࡧࠣࠦࡈࡵ࡮࡯ࡧࡦࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠭ࠤࠣࡥࡳࡪࠠࡵࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡪࡵࠣࡥࡱࡹ࡯ࠡࡷࡶࡩࡩࠦࡢࡺࠢࡖࡸࡦࡸࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࡵࡩ࡫ࡵࡲࡦ࠮ࠣࡒࡴࡴࡥࠡࡪࡤࡲࡩࡲࡩ࡯ࡩࠣ࡭ࡸࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᆱ")
        self.bstack1ll1ll11111_opy_ = getattr(r, bstack11l1ll1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᆲ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᆳ")] = self.config_testhub.jwt
        os.environ[bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᆴ")] = self.config_testhub.build_hashed_id
    def bstack1ll1111l111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1lllllll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll111ll11l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll111ll11l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll1111l111_opy_(event_name=EVENTS.bstack1ll11ll1l11_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1ll1l1l1lll_opy_(self, bstack1ll1l111ll1_opy_=10):
        if self.bstack1ll1lllllll_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡸࡺࡡࡳࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨᆵ"))
            return True
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦᆶ"))
        if os.getenv(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡈࡒ࡛ࠨᆷ")) == bstack1lll1111l11_opy_:
            self.cli_bin_session_id = bstack1lll1111l11_opy_
            self.cli_listen_addr = bstack11l1ll1_opy_ (u"ࠢࡶࡰ࡬ࡼ࠿࠵ࡴ࡮ࡲ࠲ࡷࡩࡱ࠭ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࠨࡷ࠳ࡹ࡯ࡤ࡭ࠥᆸ") % (self.cli_bin_session_id)
            self.bstack1ll1lllllll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1ll1111l11l_opy_, bstack11l1ll1_opy_ (u"ࠣࡵࡧ࡯ࠧᆹ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1l11l111_opy_ compat for text=True in bstack1ll1l1l1ll1_opy_ python
            encoding=bstack11l1ll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᆺ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1l1l1l1l_opy_ = threading.Thread(target=self.__1ll1l11l1l1_opy_, args=(bstack1ll1l111ll1_opy_,))
        bstack1ll1l1l1l1l_opy_.start()
        bstack1ll1l1l1l1l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡶࡴࡦࡽ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࢀࠤࡴࡻࡴ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡵࡷࡨࡴࡻࡴ࠯ࡴࡨࡥࡩ࠮ࠩࡾࠢࡨࡶࡷࡃࠢᆻ") + str(self.process.stderr.read()) + bstack11l1ll1_opy_ (u"ࠦࠧᆼ"))
        if not self.bstack1ll1lllllll_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡡࠢᆽ") + str(id(self)) + bstack11l1ll1_opy_ (u"ࠨ࡝ࠡࡥ࡯ࡩࡦࡴࡵࡱࠤᆾ"))
            self.__1lll111111l_opy_()
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡰࡳࡱࡦࡩࡸࡹ࡟ࡳࡧࡤࡨࡾࡀࠠࠣᆿ") + str(self.bstack1ll1lllllll_opy_) + bstack11l1ll1_opy_ (u"ࠣࠤᇀ"))
        return self.bstack1ll1lllllll_opy_
    def __1ll1l11l1l1_opy_(self, bstack1lll11111l1_opy_=10):
        bstack1ll11ll1l1l_opy_ = time.time()
        while self.process and time.time() - bstack1ll11ll1l1l_opy_ < bstack1lll11111l1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11l1ll1_opy_ (u"ࠤ࡬ࡨࡂࠨᇁ") in line:
                    self.cli_bin_session_id = line.split(bstack11l1ll1_opy_ (u"ࠥ࡭ࡩࡃࠢᇂ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡨࡲࡩࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠥᇃ") + str(self.cli_bin_session_id) + bstack11l1ll1_opy_ (u"ࠧࠨᇄ"))
                    continue
                if bstack11l1ll1_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢᇅ") in line:
                    self.cli_listen_addr = line.split(bstack11l1ll1_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣᇆ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡥ࡯࡭ࡤࡲࡩࡴࡶࡨࡲࡤࡧࡤࡥࡴ࠽ࠦᇇ") + str(self.cli_listen_addr) + bstack11l1ll1_opy_ (u"ࠤࠥᇈ"))
                    continue
                if bstack11l1ll1_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤᇉ") in line:
                    port = line.split(bstack11l1ll1_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥᇊ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡶ࡯ࡳࡶ࠽ࠦᇋ") + str(port) + bstack11l1ll1_opy_ (u"ࠨࠢᇌ"))
                    continue
                if line.strip() == bstack1ll1lll1111_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11l1ll1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡉࡐࡡࡖࡘࡗࡋࡁࡎࠤᇍ"), bstack11l1ll1_opy_ (u"ࠣ࠳ࠥᇎ")) == bstack11l1ll1_opy_ (u"ࠤ࠴ࠦᇏ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1lllllll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇐ") + str(e) + bstack11l1ll1_opy_ (u"ࠦࠧᇑ"))
        return False
    def __1lll11111ll_opy_(self):
        bstack11l1ll1_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡳࡻࡰࠡࡪࡤࡲࡩࡲࡥࡳࠢࡩࡳࡷࠦࡡࡴࡻࡱࡧࡤࡪࡩࡴࡲࡤࡸࡨ࡮ࡥࡳ࠮ࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡡࡵࡧࡻ࡭ࡹࠦࡴࡰࠢࡨࡲࡸࡻࡲࡦࠢࡷࡥࡸࡱࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠦࠧࠨᇒ")
        if self.bstack1lll1llll11_opy_ and self.bstack1ll111l111l_opy_:
            try:
                self.bstack1lll1llll11_opy_.stop()
                self.bstack1ll111l111l_opy_ = False
            except Exception as e:
                pass
    @measure(event_name=EVENTS.bstack1ll11lll1ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def __1lll111111l_opy_(self):
        if self.bstack1ll111llll1_opy_:
            if self.bstack1lll1llll11_opy_ and self.bstack1ll111l111l_opy_:
                try:
                    atexit.unregister(self.__1lll11111ll_opy_)
                except ValueError:
                    pass
                self.bstack1lll1llll11_opy_.stop()
                self.bstack1ll111l111l_opy_ = False
            start = datetime.now()
            if self.bstack1ll1l1lll1l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll11ll11l1_opy_:
                    self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᇓ"), datetime.now() - start)
                else:
                    self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᇔ"), datetime.now() - start)
            self.__1ll1lll111l_opy_()
            start = datetime.now()
            bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(bstack11l1ll1_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼ࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࠨᇕ"))
            self.bstack1ll111llll1_opy_.close()
            bstack1ll1111ll_opy_.end(bstack11l1ll1_opy_ (u"ࠤࡶࡨࡰࡀࡣ࡭࡫࠽ࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺࠢᇖ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᇗ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᇘ"), True, None, None, None, None)
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠧࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢᇙ"), datetime.now() - start)
            self.bstack1ll111llll1_opy_ = None
        if self.process:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡳࡵࡱࡳࠦᇚ"))
            start = datetime.now()
            bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(bstack11l1ll1_opy_ (u"ࠢࡴࡦ࡮࠾ࡨࡲࡩ࠻࡭࡬ࡰࡱࠨᇛ"))
            self.process.terminate()
            bstack1ll1111ll_opy_.end(bstack11l1ll1_opy_ (u"ࠣࡵࡧ࡯࠿ࡩ࡬ࡪ࠼࡮࡭ࡱࡲࠢᇜ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᇝ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᇞ"), True, None, None, None, None)
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢᇟ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll11l11l1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1111l11l_opy_()
                self.logger.info(
                    bstack11l1ll1_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠧᇠ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᇡ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1lllllll_opy_ = False
    def __1ll1l1ll111_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11l1ll1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᇢ")] = selenium.__version__
            data.frameworks.append(bstack11l1ll1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᇣ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11l1ll1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᇤ")] = __version__
            data.frameworks.append(bstack11l1ll1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᇥ"))
        except:
            pass
    def bstack1ll1ll1llll_opy_(self, hub_url: str, platform_index: int, bstack11lll1l11_opy_: Any):
        if self.bstack1lll1l1lll1_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᇦ"))
            return
        try:
            bstack111ll1ll1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11l1ll1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᇧ")
            self.bstack1lll1l1lll1_opy_ = bstack1ll1ll1lll1_opy_(
                cli.config.get(bstack11l1ll1_opy_ (u"ࠨࡨࡶࡤࡘࡶࡱࠨᇨ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1lll1l1l_opy_={bstack11l1ll1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᇩ"): bstack11lll1l11_opy_}
            )
            def bstack1ll1111ll1l_opy_(self):
                return
            if self.config.get(bstack11l1ll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥᇪ"), True):
                Service.start = bstack1ll1111ll1l_opy_
                Service.stop = bstack1ll1111ll1l_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11l1l1lll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1ll1ll11_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᇫ"), datetime.now() - bstack111ll1ll1_opy_)
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤᇬ") + str(e) + bstack11l1ll1_opy_ (u"ࠦࠧᇭ"))
    def bstack1ll1llll111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1ll1l1l1l_opy_
            self.bstack1lll1l1lll1_opy_ = bstack1ll111ll1l1_opy_(
                platform_index,
                framework_name=bstack11l1ll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᇮ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࠢᇯ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣᇰ"))
            pass
    def bstack1ll111l1l1l_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᇱ"))
            return
        if bstack1l1l1l1l1l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11l1ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᇲ"): pytest.__version__ }, [bstack11l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᇳ")], self.bstack1lll1llll11_opy_, self.bstack1ll1llll1ll_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1l1ll1l1_opy_({ bstack11l1ll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᇴ"): pytest.__version__ }, [bstack11l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᇵ")], self.bstack1lll1llll11_opy_, self.bstack1ll1llll1ll_opy_)
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥᇶ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣᇷ"))
        self.bstack1ll1ll1ll1l_opy_()
    def bstack1ll1ll1ll1l_opy_(self):
        if not self.bstack1l1l1111l1_opy_():
            return
        bstack1l111111l1_opy_ = None
        def bstack1l1ll1ll1l_opy_(config, startdir):
            return bstack11l1ll1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨᇸ").format(bstack11l1ll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᇹ"))
        def bstack1ll1l11l1_opy_():
            return
        def bstack11111l111_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11l1ll1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪᇺ"):
                return bstack11l1ll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᇻ")
            else:
                return bstack1l111111l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l111111l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l1ll1ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1l11l1_opy_
            Config.getoption = bstack11111l111_opy_
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢᇼ") + str(e) + bstack11l1ll1_opy_ (u"ࠨࠢᇽ"))
    def bstack1ll11l11lll_opy_(self):
        bstack111l1l11l1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack111l1l11l1_opy_, dict):
            if cli.config_observability:
                bstack111l1l11l1_opy_.update(
                    {bstack11l1ll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᇾ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11l1ll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦᇿ") in accessibility.get(bstack11l1ll1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥሀ"), {}):
                    bstack1ll1l11llll_opy_ = accessibility.get(bstack11l1ll1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦሁ"))
                    bstack1ll1l11llll_opy_.update({ bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧሂ"): bstack1ll1l11llll_opy_.pop(bstack11l1ll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣሃ")) })
                bstack111l1l11l1_opy_.update({bstack11l1ll1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨሄ"): accessibility })
        return bstack111l1l11l1_opy_
    @measure(event_name=EVENTS.bstack1ll11ll1ll1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1ll1l1lll1l_opy_(self, bstack1ll1l11111l_opy_: str = None, bstack1lll111l1l1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1llll1ll_opy_:
            return
        bstack111ll1ll1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = str(os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧህ"), bstack11l1ll1_opy_ (u"ࠨ࠲ࠪሆ")))
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣሇ").format(threading.get_ident(), os.getpid())
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll1l11111l_opy_:
            req.bstack1ll1l11111l_opy_ = bstack1ll1l11111l_opy_
        if bstack1lll111l1l1_opy_:
            req.bstack1lll111l1l1_opy_ = bstack1lll111l1l1_opy_
        try:
            r = self.bstack1ll1llll1ll_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡳࡵࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦለ"), datetime.now() - bstack111ll1ll1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll1l11l_opy_(self, key: str, value: timedelta):
        tag = bstack11l1ll1_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࠦሉ") if self.bstack1l11lll1_opy_() else bstack11l1ll1_opy_ (u"ࠧࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶࠦሊ")
        self.bstack1ll11l1l111_opy_[bstack11l1ll1_opy_ (u"ࠨ࠺ࠣላ").join([tag + bstack11l1ll1_opy_ (u"ࠢ࠮ࠤሌ") + str(id(self)), key])] += value
    def bstack1l1111l11l_opy_(self):
        if not os.getenv(bstack11l1ll1_opy_ (u"ࠣࡆࡈࡆ࡚ࡍ࡟ࡑࡇࡕࡊࠧል"), bstack11l1ll1_opy_ (u"ࠤ࠳ࠦሎ")) == bstack11l1ll1_opy_ (u"ࠥ࠵ࠧሏ"):
            return
        bstack1ll1lll1l11_opy_ = dict()
        bstack1lll1ll11ll_opy_ = []
        if self.test_framework:
            bstack1lll1ll11ll_opy_.extend(list(self.test_framework.bstack1lll1ll11ll_opy_.values()))
        if self.bstack1lll1l1lll1_opy_:
            bstack1lll1ll11ll_opy_.extend(list(self.bstack1lll1l1lll1_opy_.bstack1lll1ll11ll_opy_.values()))
        for instance in bstack1lll1ll11ll_opy_:
            if not instance.platform_index in bstack1ll1lll1l11_opy_:
                bstack1ll1lll1l11_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll1lll1l11_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1ll11ll1_opy_().items():
                report[k] += v
                report[k.split(bstack11l1ll1_opy_ (u"ࠦ࠿ࠨሐ"))[0]] += v
        bstack1ll1ll1l111_opy_ = sorted([(k, v) for k, v in self.bstack1ll11l1l111_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1l1111ll_opy_ = 0
        for r in bstack1ll1ll1l111_opy_:
            bstack1ll11llll11_opy_ = r[1].total_seconds()
            bstack1ll1l1111ll_opy_ += bstack1ll11llll11_opy_
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡾࡶࡠ࠶࡝ࡾ࠿ࠥሑ") + str(bstack1ll11llll11_opy_) + bstack11l1ll1_opy_ (u"ࠨࠢሒ"))
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࠮࠯ࠥሓ"))
        bstack1ll1111lll1_opy_ = []
        for platform_index, report in bstack1ll1lll1l11_opy_.items():
            bstack1ll1111lll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1111lll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1ll1ll1ll_opy_ = set()
        bstack1ll1l1l1111_opy_ = 0
        for r in bstack1ll1111lll1_opy_:
            bstack1ll11llll11_opy_ = r[2].total_seconds()
            bstack1ll1l1l1111_opy_ += bstack1ll11llll11_opy_
            bstack1ll1ll1ll_opy_.add(r[0])
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡶࡨࡷࡹࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭࠮ࡽࡵ࡟࠵ࡣࡽ࠻ࡽࡵ࡟࠶ࡣࡽ࠾ࠤሔ") + str(bstack1ll11llll11_opy_) + bstack11l1ll1_opy_ (u"ࠤࠥሕ"))
        if self.bstack1l11lll1_opy_():
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥ࠱࠲ࠨሖ"))
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻ࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠾ࡽࡷࡳࡹࡧ࡬ࡠࡥ࡯࡭ࢂࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲࡹ࠭ࡼࡵࡷࡶ࠭ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠪࡿࡀࠦሗ") + str(bstack1ll1l1l1111_opy_) + bstack11l1ll1_opy_ (u"ࠧࠨመ"))
        else:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࠥሙ") + str(bstack1ll1l1111ll_opy_) + bstack11l1ll1_opy_ (u"ࠢࠣሚ"))
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠣ࠯࠰ࠦማ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata,
            platform_index=str(os.environ.get(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩሜ"), bstack11l1ll1_opy_ (u"ࠪ࠴ࠬም"))),
            client_worker_id=bstack11l1ll1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥሞ").format(threading.get_ident(), os.getpid())
        )
        if not self.bstack1ll1llll1ll_opy_:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡩ࡬ࡪࡡࡶࡩࡷࡼࡩࡤࡧࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤሟ"))
            return None
        response = self.bstack1ll1llll1ll_opy_.TestOrchestration(request)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷ࠱ࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲࡂࢁࡽࠣሠ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll11l111ll_opy_(self, r):
        if r is not None and getattr(r, bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࠨሡ"), None) and getattr(r.testhub, bstack11l1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨሢ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11l1ll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣሣ")))
            for bstack1ll1ll1111l_opy_, err in errors.items():
                if err[bstack11l1ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨሤ")] == bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩሥ"):
                    self.logger.info(err[bstack11l1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ሦ")])
                else:
                    self.logger.error(err[bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧሧ")])
    def bstack1l1111l11_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()