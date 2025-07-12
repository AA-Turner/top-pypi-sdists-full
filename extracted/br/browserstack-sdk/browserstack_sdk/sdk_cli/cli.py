# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1l1l1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll11ll_opy_ import bstack1l111ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lll111111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll11lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll111lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack111111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l1l_opy_ import bstack1ll1l1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack111lllllll_opy_ import bstack111lllllll_opy_, bstack11l1ll1ll_opy_, bstack11lll1l1l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1l1l11ll11l_opy_ import bstack1l1l11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1ll1lll1l1l_opy_
from bstack_utils.helper import Notset, bstack1l11l111ll1_opy_, get_cli_dir, bstack1l11l1ll1ll_opy_, bstack1ll11ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l1l1_opy_ import bstack1l1lll1l1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll111l1_opy_ import bstack11ll1ll11l_opy_
from bstack_utils.helper import Notset, bstack1l11l111ll1_opy_, get_cli_dir, bstack1l11l1ll1ll_opy_, bstack1ll11ll111_opy_, bstack1lllll1111_opy_, bstack1l1l1l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lllll111ll_opy_, bstack1lll1lll1ll_opy_, bstack1llll11ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack1lll1llll11_opy_, bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1l1lll1l1l_opy_ import bstack11111111_opy_
from bstack_utils import bstack1l11l1l1l_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111l1l1l_opy_, bstack111l1lll_opy_
logger = bstack1l11l1l1l_opy_.get_logger(__name__, bstack1l11l1l1l_opy_.bstack1l11ll11l1l_opy_())
def bstack1l111lll11l_opy_(bs_config):
    bstack1l11l1lll1l_opy_ = None
    bstack1l111ll1lll_opy_ = None
    try:
        bstack1l111ll1lll_opy_ = get_cli_dir()
        bstack1l11l1lll1l_opy_ = bstack1l11l1ll1ll_opy_(bstack1l111ll1lll_opy_)
        bstack1l11ll111ll_opy_ = bstack1l11l111ll1_opy_(bstack1l11l1lll1l_opy_, bstack1l111ll1lll_opy_, bs_config)
        bstack1l11l1lll1l_opy_ = bstack1l11ll111ll_opy_ if bstack1l11ll111ll_opy_ else bstack1l11l1lll1l_opy_
        if not bstack1l11l1lll1l_opy_:
            raise ValueError(bstack11l1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥᑗ"))
    except Exception as ex:
        logger.debug(bstack11l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡭ࡣࡷࡩࡸࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡼࡿࠥᑘ").format(ex))
        bstack1l11l1lll1l_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦᑙ"))
        if bstack1l11l1lll1l_opy_:
            logger.debug(bstack11l1111_opy_ (u"ࠤࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡴࡲࡱࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࠧᑚ") + str(bstack1l11l1lll1l_opy_) + bstack11l1111_opy_ (u"ࠥࠦᑛ"))
        else:
            logger.debug(bstack11l1111_opy_ (u"ࠦࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠽ࠣࡷࡪࡺࡵࡱࠢࡰࡥࡾࠦࡢࡦࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠢᑜ"))
    return bstack1l11l1lll1l_opy_, bstack1l111ll1lll_opy_
bstack1l111lll1l1_opy_ = bstack11l1111_opy_ (u"ࠧ࠿࠹࠺࠻ࠥᑝ")
bstack1l1111lllll_opy_ = bstack11l1111_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧᑞ")
bstack1l1111ll1l1_opy_ = bstack11l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᑟ")
bstack1l111llll1l_opy_ = bstack11l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨᑠ")
bstack11l11llll1_opy_ = bstack11l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᑡ")
bstack1l111l1l1l1_opy_ = re.compile(bstack11l1111_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤᑢ"))
bstack1l11l1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤᑣ")
bstack1l11ll1111l_opy_ = [
    bstack11l1ll1ll_opy_.bstack11ll1l1ll1_opy_,
    bstack11l1ll1ll_opy_.CONNECT,
    bstack11l1ll1ll_opy_.bstack1ll11l1l_opy_,
]
class SDKCLI:
    _1l111l111ll_opy_ = None
    process: Union[None, Any]
    bstack1l11l1l111l_opy_: bool
    bstack1l11ll1lll1_opy_: bool
    bstack1l11ll11l11_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1l11ll1l11l_opy_: Union[None, grpc.Channel]
    bstack1l11l1lllll_opy_: str
    test_framework: TestFramework
    bstack1llllll11ll_opy_: bstack1ll1lllll11_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1l111ll1l11_opy_: bstack1llll1111ll_opy_
    accessibility: bstack1l111ll11l1_opy_
    bstack1l1ll111l1_opy_: bstack11ll1ll11l_opy_
    ai: bstack1lll111111l_opy_
    bstack1l11l1ll1l1_opy_: bstack1lll11lll11_opy_
    bstack1l111l1l11l_opy_: List[bstack1lll1lllll1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1l1111lll11_opy_: Any
    bstack1l11l11l11l_opy_: Dict[str, timedelta]
    bstack1l11lll111l_opy_: str
    bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_
    def __new__(cls):
        if not cls._1l111l111ll_opy_:
            cls._1l111l111ll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1l111l111ll_opy_
    def __init__(self):
        self.process = None
        self.bstack1l11l1l111l_opy_ = False
        self.bstack1l11ll1l11l_opy_ = None
        self.bstack1lll1llll1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1l111llll1l_opy_, None)
        self.bstack1l111l1111l_opy_ = os.environ.get(bstack1l1111ll1l1_opy_, bstack11l1111_opy_ (u"ࠧࠨᑤ")) == bstack11l1111_opy_ (u"ࠨࠢᑥ")
        self.bstack1l11ll1lll1_opy_ = False
        self.bstack1l11ll11l11_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1l1111lll11_opy_ = None
        self.test_framework = None
        self.bstack1llllll11ll_opy_ = None
        self.bstack1l11l1lllll_opy_=bstack11l1111_opy_ (u"ࠢࠣᑦ")
        self.session_framework = None
        self.logger = bstack1l11l1l1l_opy_.get_logger(self.__class__.__name__, bstack1l11l1l1l_opy_.bstack1l11ll11l1l_opy_())
        self.bstack1l11l11l11l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1llll1l1l1l_opy_ = bstack1ll1llllll1_opy_()
        self.bstack1llll1l111l_opy_ = None
        self.bstack1llll1ll11l_opy_ = None
        self.bstack1l111ll1l11_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1l111l1l11l_opy_ = []
    def bstack1l11lll1l_opy_(self):
        return os.environ.get(bstack11l11llll1_opy_).lower().__eq__(bstack11l1111_opy_ (u"ࠣࡶࡵࡹࡪࠨᑧ"))
    def is_enabled(self, config):
        if bstack11l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᑨ") in config and str(config[bstack11l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᑩ")]).lower() != bstack11l1111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᑪ"):
            return False
        bstack1l11l1111l1_opy_ = [bstack11l1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᑫ"), bstack11l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᑬ")]
        bstack1l11l1l1111_opy_ = config.get(bstack11l1111_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᑭ")) in bstack1l11l1111l1_opy_ or os.environ.get(bstack11l1111_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩᑮ")) in bstack1l11l1111l1_opy_
        os.environ[bstack11l1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᑯ")] = str(bstack1l11l1l1111_opy_) # bstack1l111l1lll1_opy_ bstack1l11l1ll111_opy_ VAR to bstack1l11lll1111_opy_ is binary running
        return bstack1l11l1l1111_opy_
    def bstack1ll11lll_opy_(self):
        for event in bstack1l11ll1111l_opy_:
            bstack111lllllll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack111lllllll_opy_.logger.debug(bstack11l1111_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨᑰ") + str(kwargs) + bstack11l1111_opy_ (u"ࠦࠧᑱ"))
            )
        bstack111lllllll_opy_.register(bstack11l1ll1ll_opy_.bstack11ll1l1ll1_opy_, self.__1l1111llll1_opy_)
        bstack111lllllll_opy_.register(bstack11l1ll1ll_opy_.CONNECT, self.__1l11ll1ll1l_opy_)
        bstack111lllllll_opy_.register(bstack11l1ll1ll_opy_.bstack1ll11l1l_opy_, self.__1l111lll111_opy_)
        bstack111lllllll_opy_.register(bstack11l1ll1ll_opy_.bstack1ll11ll1l_opy_, self.__1l111l11ll1_opy_)
    def bstack111l1ll1l_opy_(self):
        return not self.bstack1l111l1111l_opy_ and os.environ.get(bstack1l1111ll1l1_opy_, bstack11l1111_opy_ (u"ࠧࠨᑲ")) != bstack11l1111_opy_ (u"ࠨࠢᑳ")
    def is_running(self):
        if self.bstack1l111l1111l_opy_:
            return self.bstack1l11l1l111l_opy_
        else:
            return bool(self.bstack1l11ll1l11l_opy_)
    def bstack1l1111ll1ll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1l111l1l11l_opy_) and cli.is_running()
    def __1l11l1lll11_opy_(self, bstack1l11l111lll_opy_=10):
        if self.bstack1lll1llll1l_opy_:
            return
        bstack1ll1l1l1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1l111llll1l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡜ࠤᑴ") + str(id(self)) + bstack11l1111_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢᑵ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11l1111_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦᑶ"), 0), (bstack11l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨᑷ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1l11l111lll_opy_)
        self.bstack1l11ll1l11l_opy_ = channel
        self.bstack1lll1llll1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1l11ll1l11l_opy_)
        self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥᑸ"), datetime.now() - bstack1ll1l1l1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1l111llll1l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧᑹ") + str(self.bstack111l1ll1l_opy_()) + bstack11l1111_opy_ (u"ࠨࠢᑺ"))
    def __1l111lll111_opy_(self, event_name):
        if self.bstack111l1ll1l_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢᑻ"))
        self.__1l11l11ll1l_opy_()
    def __1l111l11ll1_opy_(self, event_name, bstack1l11ll1l1l1_opy_ = None, bstack1l1l1lll11_opy_=1):
        if bstack1l1l1lll11_opy_ == 1:
            self.logger.error(bstack11l1111_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣᑼ"))
        bstack1l11ll1ll11_opy_ = Path(bstack1lll1111lll_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥᑽ"))
        if self.bstack1l111ll1lll_opy_ and bstack1l11ll1ll11_opy_.exists():
            with open(bstack1l11ll1ll11_opy_, bstack11l1111_opy_ (u"ࠪࡶࠬᑾ"), encoding=bstack11l1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᑿ")) as fp:
                data = json.load(fp)
                try:
                    bstack1lllll1111_opy_(bstack11l1111_opy_ (u"ࠬࡖࡏࡔࡖࠪᒀ"), bstack11111111_opy_(bstack1l1l1ll111_opy_), data, {
                        bstack11l1111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᒁ"): (self.config[bstack11l1111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᒂ")], self.config[bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᒃ")])
                    })
                except Exception as e:
                    logger.debug(bstack111l1lll_opy_.format(str(e)))
            bstack1l11ll1ll11_opy_.unlink()
        sys.exit(bstack1l1l1lll11_opy_)
    @measure(event_name=EVENTS.bstack1l111l11l1l_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1l1111llll1_opy_(self, event_name: str, data):
        from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
        self.bstack1l11l1lllll_opy_, self.bstack1l111ll1lll_opy_ = bstack1l111lll11l_opy_(data.bs_config)
        os.environ[bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧᒄ")] = self.bstack1l111ll1lll_opy_
        if not self.bstack1l11l1lllll_opy_ or not self.bstack1l111ll1lll_opy_:
            raise ValueError(bstack11l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤᒅ"))
        if self.bstack111l1ll1l_opy_():
            self.__1l11ll1ll1l_opy_(event_name, bstack11lll1l1l_opy_())
            return
        try:
            bstack1lll1l1l11l_opy_.end(EVENTS.bstack1111lll1l_opy_.value, EVENTS.bstack1111lll1l_opy_.value + bstack11l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᒆ"), EVENTS.bstack1111lll1l_opy_.value + bstack11l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᒇ"), status=True, failure=None, test_name=None)
            logger.debug(bstack11l1111_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧᒈ"))
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦᒉ").format(e))
        start = datetime.now()
        is_started = self.__1l11l1l1lll_opy_()
        self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧᒊ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1l11l1lll11_opy_()
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᒋ"), datetime.now() - start)
            start = datetime.now()
            self.__1l111l11lll_opy_(data)
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᒌ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1l11ll1l111_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1l11ll1ll1l_opy_(self, event_name: str, data: bstack11lll1l1l_opy_):
        if not self.bstack111l1ll1l_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᒍ"))
            return
        bin_session_id = os.environ.get(bstack1l1111ll1l1_opy_)
        start = datetime.now()
        self.__1l11l1lll11_opy_()
        self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᒎ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧᒏ") + str(bin_session_id) + bstack11l1111_opy_ (u"ࠢࠣᒐ"))
        start = datetime.now()
        self.__1l11ll111l1_opy_()
        self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᒑ"), datetime.now() - start)
    def __1l11l11llll_opy_(self):
        if not self.bstack1lll1llll1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨᒒ"))
            return
        bstack1l111l1l111_opy_ = {
            bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᒓ"): (bstack1ll1ll111l1_opy_, bstack1ll1l1l1111_opy_, bstack1ll1lll1l1l_opy_),
            bstack11l1111_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᒔ"): (bstack1ll111lll11_opy_, bstack111111l1ll_opy_, bstack1lll1ll1l1l_opy_),
        }
        if not self.bstack1llll1l111l_opy_ and self.session_framework in bstack1l111l1l111_opy_:
            bstack1l1111ll11l_opy_, bstack1l1111lll1l_opy_, bstack1l11l1l1l1l_opy_ = bstack1l111l1l111_opy_[self.session_framework]
            bstack1l11l11l1ll_opy_ = bstack1l1111lll1l_opy_()
            self.bstack1llll1ll11l_opy_ = bstack1l11l11l1ll_opy_
            self.bstack1llll1l111l_opy_ = bstack1l11l1l1l1l_opy_
            self.bstack1l111l1l11l_opy_.append(bstack1l11l11l1ll_opy_)
            self.bstack1l111l1l11l_opy_.append(bstack1l1111ll11l_opy_(self.bstack1llll1ll11l_opy_))
        if not self.bstack1l111ll1l11_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1l1ll1l1_opy_
            self.bstack1l111ll1l11_opy_ = bstack1llll1111ll_opy_(self.bstack1llll1l111l_opy_, self.bstack1llll1ll11l_opy_) # bstack1l111l11l11_opy_
            self.bstack1l111l1l11l_opy_.append(self.bstack1l111ll1l11_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1l111ll11l1_opy_(self.bstack1llll1l111l_opy_, self.bstack1llll1ll11l_opy_)
            self.bstack1l111l1l11l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11l1111_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢᒕ"), False) == True:
            self.ai = bstack1lll111111l_opy_()
            self.bstack1l111l1l11l_opy_.append(self.ai)
        if not self.percy and self.bstack1l1111lll11_opy_ and self.bstack1l1111lll11_opy_.success:
            self.percy = bstack1lll11lll11_opy_(self.bstack1l1111lll11_opy_)
            self.bstack1l111l1l11l_opy_.append(self.percy)
        for mod in self.bstack1l111l1l11l_opy_:
            if not mod.bstack1ll1lllllll_opy_():
                mod.configure(self.bstack1lll1llll1l_opy_, self.config, self.cli_bin_session_id, self.bstack1llll1l1l1l_opy_)
    def __1l111ll111l_opy_(self):
        for mod in self.bstack1l111l1l11l_opy_:
            if mod.bstack1ll1lllllll_opy_():
                mod.configure(self.bstack1lll1llll1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1l11l1l11l1_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1l111l11lll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1l11ll1lll1_opy_:
            return
        self.__1l111l1l1ll_opy_(data)
        bstack1ll1l1l1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11l1111_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᒖ")
        req.sdk_language = bstack11l1111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᒗ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1l111l1l1l1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣ࡝ࠥᒘ") + str(id(self)) + bstack11l1111_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᒙ"))
            r = self.bstack1lll1llll1l_opy_.StartBinSession(req)
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᒚ"), datetime.now() - bstack1ll1l1l1_opy_)
            os.environ[bstack1l1111ll1l1_opy_] = r.bin_session_id
            self.__1l11ll11111_opy_(r)
            self.__1l11l11llll_opy_()
            self.bstack1llll1l1l1l_opy_.start()
            self.bstack1l11ll1lll1_opy_ = True
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡠࠨᒛ") + str(id(self)) + bstack11l1111_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥᒜ"))
        except grpc.bstack1l11ll1l1ll_opy_ as bstack1l111lll1ll_opy_:
            self.logger.error(bstack11l1111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᒝ") + str(bstack1l111lll1ll_opy_) + bstack11l1111_opy_ (u"ࠢࠣᒞ"))
            traceback.print_exc()
            raise bstack1l111lll1ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒟ") + str(e) + bstack11l1111_opy_ (u"ࠤࠥᒠ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1ll11l_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1l11ll111l1_opy_(self):
        if not self.bstack111l1ll1l_opy_() or not self.cli_bin_session_id or self.bstack1l11ll11l11_opy_:
            return
        bstack1ll1l1l1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒡ"), bstack11l1111_opy_ (u"ࠫ࠵࠭ᒢ")))
        try:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡡࠢᒣ") + str(id(self)) + bstack11l1111_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᒤ"))
            r = self.bstack1lll1llll1l_opy_.ConnectBinSession(req)
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᒥ"), datetime.now() - bstack1ll1l1l1_opy_)
            self.__1l11ll11111_opy_(r)
            self.__1l11l11llll_opy_()
            self.bstack1llll1l1l1l_opy_.start()
            self.bstack1l11ll11l11_opy_ = True
            self.logger.debug(bstack11l1111_opy_ (u"ࠣ࡝ࠥᒦ") + str(id(self)) + bstack11l1111_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣᒧ"))
        except grpc.bstack1l11ll1l1ll_opy_ as bstack1l111lll1ll_opy_:
            self.logger.error(bstack11l1111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒨ") + str(bstack1l111lll1ll_opy_) + bstack11l1111_opy_ (u"ࠦࠧᒩ"))
            traceback.print_exc()
            raise bstack1l111lll1ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᒪ") + str(e) + bstack11l1111_opy_ (u"ࠨࠢᒫ"))
            traceback.print_exc()
            raise e
    def __1l11ll11111_opy_(self, r):
        self.bstack1l11l11l111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11l1111_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᒬ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11l1111_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨᒭ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒮ")
        self.bstack1l1111lll11_opy_ = getattr(r, bstack11l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᒯ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᒰ")] = self.config_testhub.jwt
        os.environ[bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᒱ")] = self.config_testhub.build_hashed_id
    def bstack1l11l1l1l11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1l11l1l111l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1l11l11l1l1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1l11l11l1l1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1l11l1l1l11_opy_(event_name=EVENTS.bstack1l11l1111ll_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1l11l1l1lll_opy_(self, bstack1l11l111lll_opy_=10):
        if self.bstack1l11l1l111l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣᒲ"))
            return True
        self.logger.debug(bstack11l1111_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᒳ"))
        if os.getenv(bstack11l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣᒴ")) == bstack1l11l1l1ll1_opy_:
            self.cli_bin_session_id = bstack1l11l1l1ll1_opy_
            self.cli_listen_addr = bstack11l1111_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧᒵ") % (self.cli_bin_session_id)
            self.bstack1l11l1l111l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1l11l1lllll_opy_, bstack11l1111_opy_ (u"ࠥࡷࡩࡱࠢᒶ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1l11l1l11ll_opy_ compat for text=True in bstack1l11ll11ll1_opy_ python
            encoding=bstack11l1111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᒷ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1l111ll1ll1_opy_ = threading.Thread(target=self.__1l111llll11_opy_, args=(bstack1l11l111lll_opy_,))
        bstack1l111ll1ll1_opy_.start()
        bstack1l111ll1ll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤᒸ") + str(self.process.stderr.read()) + bstack11l1111_opy_ (u"ࠨࠢᒹ"))
        if not self.bstack1l11l1l111l_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡜ࠤᒺ") + str(id(self)) + bstack11l1111_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦᒻ"))
            self.__1l11l11ll1l_opy_()
        self.logger.debug(bstack11l1111_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥᒼ") + str(self.bstack1l11l1l111l_opy_) + bstack11l1111_opy_ (u"ࠥࠦᒽ"))
        return self.bstack1l11l1l111l_opy_
    def __1l111llll11_opy_(self, bstack1l11ll11lll_opy_=10):
        bstack1l111l1ll1l_opy_ = time.time()
        while self.process and time.time() - bstack1l111l1ll1l_opy_ < bstack1l11ll11lll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11l1111_opy_ (u"ࠦ࡮ࡪ࠽ࠣᒾ") in line:
                    self.cli_bin_session_id = line.split(bstack11l1111_opy_ (u"ࠧ࡯ࡤ࠾ࠤᒿ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1111_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧᓀ") + str(self.cli_bin_session_id) + bstack11l1111_opy_ (u"ࠢࠣᓁ"))
                    continue
                if bstack11l1111_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᓂ") in line:
                    self.cli_listen_addr = line.split(bstack11l1111_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᓃ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1111_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨᓄ") + str(self.cli_listen_addr) + bstack11l1111_opy_ (u"ࠦࠧᓅ"))
                    continue
                if bstack11l1111_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᓆ") in line:
                    port = line.split(bstack11l1111_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᓇ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1111_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨᓈ") + str(port) + bstack11l1111_opy_ (u"ࠣࠤᓉ"))
                    continue
                if line.strip() == bstack1l1111lllll_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11l1111_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦᓊ"), bstack11l1111_opy_ (u"ࠥ࠵ࠧᓋ")) == bstack11l1111_opy_ (u"ࠦ࠶ࠨᓌ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1l11l1l111l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11l1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨᓍ") + str(e) + bstack11l1111_opy_ (u"ࠨࠢᓎ"))
        return False
    @measure(event_name=EVENTS.bstack1l1111l1lll_opy_, stage=STAGE.bstack1111llll1_opy_)
    def __1l11l11ll1l_opy_(self):
        if self.bstack1l11ll1l11l_opy_:
            self.bstack1llll1l1l1l_opy_.stop()
            start = datetime.now()
            if self.bstack1l11l11lll1_opy_():
                self.cli_bin_session_id = None
                if self.bstack1l11ll11l11_opy_:
                    self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᓏ"), datetime.now() - start)
                else:
                    self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᓐ"), datetime.now() - start)
            self.__1l111ll111l_opy_()
            start = datetime.now()
            self.bstack1l11ll1l11l_opy_.close()
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᓑ"), datetime.now() - start)
            self.bstack1l11ll1l11l_opy_ = None
        if self.process:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡷࡹࡵࡰࠣᓒ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢᓓ"), datetime.now() - start)
            self.process = None
            if self.bstack1l111l1111l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack111lllll_opy_()
                self.logger.info(
                    bstack11l1111_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠣᓔ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11l1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᓕ")] = self.config_testhub.build_hashed_id
        self.bstack1l11l1l111l_opy_ = False
    def __1l111l1l1ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11l1111_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᓖ")] = selenium.__version__
            data.frameworks.append(bstack11l1111_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᓗ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11l1111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᓘ")] = __version__
            data.frameworks.append(bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᓙ"))
        except:
            pass
    def bstack1l11l111111_opy_(self, hub_url: str, platform_index: int, bstack11lll1l11l_opy_: Any):
        if self.bstack1llllll11ll_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᓚ"))
            return
        try:
            bstack1ll1l1l1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11l1111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᓛ")
            self.bstack1llllll11ll_opy_ = bstack1lll1ll1l1l_opy_(
                cli.config.get(bstack11l1111_opy_ (u"ࠨࡨࡶࡤࡘࡶࡱࠨᓜ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll11l11l11_opy_={bstack11l1111_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᓝ"): bstack11lll1l11l_opy_}
            )
            def bstack1l11l11111l_opy_(self):
                return
            if self.config.get(bstack11l1111_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥᓞ"), True):
                Service.start = bstack1l11l11111l_opy_
                Service.stop = bstack1l11l11111l_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11ll1ll11l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1l1lll1l1ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᓟ"), datetime.now() - bstack1ll1l1l1_opy_)
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤᓠ") + str(e) + bstack11l1111_opy_ (u"ࠦࠧᓡ"))
    def bstack1l111l11111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1llll1ll1l_opy_
            self.bstack1llllll11ll_opy_ = bstack1ll1lll1l1l_opy_(
                platform_index,
                framework_name=bstack11l1111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᓢ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࠢᓣ") + str(e) + bstack11l1111_opy_ (u"ࠢࠣᓤ"))
            pass
    def bstack1l111l111l1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᓥ"))
            return
        if bstack1ll11ll111_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᓦ"): pytest.__version__ }, [bstack11l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᓧ")], self.bstack1llll1l1l1l_opy_, self.bstack1lll1llll1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1l1l11ll1l1_opy_({ bstack11l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᓨ"): pytest.__version__ }, [bstack11l1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᓩ")], self.bstack1llll1l1l1l_opy_, self.bstack1lll1llll1l_opy_)
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥᓪ") + str(e) + bstack11l1111_opy_ (u"ࠢࠣᓫ"))
        self.bstack1l111l1llll_opy_()
    def bstack1l111l1llll_opy_(self):
        if not self.bstack1l11lll1l_opy_():
            return
        bstack1lllll1ll1_opy_ = None
        def bstack11lll1111l_opy_(config, startdir):
            return bstack11l1111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨᓬ").format(bstack11l1111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᓭ"))
        def bstack1ll1ll111_opy_():
            return
        def bstack1llll1lll1_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11l1111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪᓮ"):
                return bstack11l1111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᓯ")
            else:
                return bstack1lllll1ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1lllll1ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11lll1111l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1ll111_opy_
            Config.getoption = bstack1llll1lll1_opy_
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢᓰ") + str(e) + bstack11l1111_opy_ (u"ࠨࠢᓱ"))
    def bstack1l111l1ll11_opy_(self):
        bstack11l11l11_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11l11l11_opy_, dict):
            if cli.config_observability:
                bstack11l11l11_opy_.update(
                    {bstack11l1111_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᓲ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦᓳ") in accessibility.get(bstack11l1111_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᓴ"), {}):
                    bstack1l111lllll1_opy_ = accessibility.get(bstack11l1111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᓵ"))
                    bstack1l111lllll1_opy_.update({ bstack11l1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧᓶ"): bstack1l111lllll1_opy_.pop(bstack11l1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣᓷ")) })
                bstack11l11l11_opy_.update({bstack11l1111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᓸ"): accessibility })
        return bstack11l11l11_opy_
    @measure(event_name=EVENTS.bstack1l111ll11ll_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1l11l11lll1_opy_(self, bstack1l111ll1111_opy_: str = None, bstack1l11l11ll11_opy_: str = None, bstack1l1l1lll11_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll1llll1l_opy_:
            return
        bstack1ll1l1l1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1l1l1lll11_opy_:
            req.bstack1l1l1lll11_opy_ = bstack1l1l1lll11_opy_
        if bstack1l111ll1111_opy_:
            req.bstack1l111ll1111_opy_ = bstack1l111ll1111_opy_
        if bstack1l11l11ll11_opy_:
            req.bstack1l11l11ll11_opy_ = bstack1l11l11ll11_opy_
        try:
            r = self.bstack1lll1llll1l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡰࡲࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓹ"), datetime.now() - bstack1ll1l1l1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1llll1l1l_opy_(self, key: str, value: timedelta):
        tag = bstack11l1111_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᓺ") if self.bstack111l1ll1l_opy_() else bstack11l1111_opy_ (u"ࠤࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᓻ")
        self.bstack1l11l11l11l_opy_[bstack11l1111_opy_ (u"ࠥ࠾ࠧᓼ").join([tag + bstack11l1111_opy_ (u"ࠦ࠲ࠨᓽ") + str(id(self)), key])] += value
    def bstack111lllll_opy_(self):
        if not os.getenv(bstack11l1111_opy_ (u"ࠧࡊࡅࡃࡗࡊࡣࡕࡋࡒࡇࠤᓾ"), bstack11l1111_opy_ (u"ࠨ࠰ࠣᓿ")) == bstack11l1111_opy_ (u"ࠢ࠲ࠤᔀ"):
            return
        bstack1l111llllll_opy_ = dict()
        bstack1ll11llllll_opy_ = []
        if self.test_framework:
            bstack1ll11llllll_opy_.extend(list(self.test_framework.bstack1ll11llllll_opy_.values()))
        if self.bstack1llllll11ll_opy_:
            bstack1ll11llllll_opy_.extend(list(self.bstack1llllll11ll_opy_.bstack1ll11llllll_opy_.values()))
        for instance in bstack1ll11llllll_opy_:
            if not instance.platform_index in bstack1l111llllll_opy_:
                bstack1l111llllll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1l111llllll_opy_[instance.platform_index]
            for k, v in instance.bstack1l1l1111lll_opy_().items():
                report[k] += v
                report[k.split(bstack11l1111_opy_ (u"ࠣ࠼ࠥᔁ"))[0]] += v
        bstack1l11l111l11_opy_ = sorted([(k, v) for k, v in self.bstack1l11l11l11l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1l11ll1llll_opy_ = 0
        for r in bstack1l11l111l11_opy_:
            bstack1l1111ll111_opy_ = r[1].total_seconds()
            bstack1l11ll1llll_opy_ += bstack1l1111ll111_opy_
            self.logger.debug(bstack11l1111_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡻࡳ࡝࠳ࡡࢂࡃࠢᔂ") + str(bstack1l1111ll111_opy_) + bstack11l1111_opy_ (u"ࠥࠦᔃ"))
        self.logger.debug(bstack11l1111_opy_ (u"ࠦ࠲࠳ࠢᔄ"))
        bstack1l11l1llll1_opy_ = []
        for platform_index, report in bstack1l111llllll_opy_.items():
            bstack1l11l1llll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1l11l1llll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l111ll11_opy_ = set()
        bstack1l11l111l1l_opy_ = 0
        for r in bstack1l11l1llll1_opy_:
            bstack1l1111ll111_opy_ = r[2].total_seconds()
            bstack1l11l111l1l_opy_ += bstack1l1111ll111_opy_
            bstack1l111ll11_opy_.add(r[0])
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࢁࡲ࡜࠲ࡠࢁ࠿ࢁࡲ࡜࠳ࡠࢁࡂࠨᔅ") + str(bstack1l1111ll111_opy_) + bstack11l1111_opy_ (u"ࠨࠢᔆ"))
        if self.bstack111l1ll1l_opy_():
            self.logger.debug(bstack11l1111_opy_ (u"ࠢ࠮࠯ࠥᔇ"))
            self.logger.debug(bstack11l1111_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࢁࡴࡰࡶࡤࡰࡤࡩ࡬ࡪࡿࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠱ࢀࡹࡴࡳࠪࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠮ࢃ࠽ࠣᔈ") + str(bstack1l11l111l1l_opy_) + bstack11l1111_opy_ (u"ࠤࠥᔉ"))
        else:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࠢᔊ") + str(bstack1l11ll1llll_opy_) + bstack11l1111_opy_ (u"ࠦࠧᔋ"))
        self.logger.debug(bstack11l1111_opy_ (u"ࠧ࠳࠭ࠣᔌ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1lll1llll1l_opy_:
            self.logger.error(bstack11l1111_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᔍ"))
            return None
        response = self.bstack1lll1llll1l_opy_.TestOrchestration(request)
        self.logger.debug(bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤᔎ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1l11l11l111_opy_(self, r):
        if r is not None and getattr(r, bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩᔏ"), None) and getattr(r.testhub, bstack11l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᔐ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11l1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᔑ")))
            for bstack1l111ll1l1l_opy_, err in errors.items():
                if err[bstack11l1111_opy_ (u"ࠫࡹࡿࡰࡦࠩᔒ")] == bstack11l1111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᔓ"):
                    self.logger.info(err[bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᔔ")])
                else:
                    self.logger.error(err[bstack11l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᔕ")])
    def bstack1ll1l111l_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()