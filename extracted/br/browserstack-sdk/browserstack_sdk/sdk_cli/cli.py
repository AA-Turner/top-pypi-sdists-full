# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1ll1ll11lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1l1l_opy_ import bstack1lll1llllll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l11l_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111lll_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack11l11lll1l_opy_ import bstack11l11lll1l_opy_, bstack1llllll1l1_opy_, bstack1111111ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1llllll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll111111l_opy_
from bstack_utils.helper import Notset, bstack1lll1ll11ll_opy_, get_cli_dir, bstack1ll1ll1lll1_opy_, bstack1lll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1lll_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1l11_opy_ import bstack1lllll1lll_opy_
from bstack_utils.helper import Notset, bstack1lll1ll11ll_opy_, get_cli_dir, bstack1ll1ll1lll1_opy_, bstack1lll111l_opy_, bstack11lll1111_opy_, bstack11l1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1ll111l_opy_, bstack1ll1l1lll1l_opy_, bstack1lll1111l1l_opy_, bstack1lll111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111l1l_opy_, bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11ll111l1l_opy_ import bstack111l11ll_opy_
from bstack_utils import bstack11l1l1l111_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1l1ll11_opy_, bstack1l1lll11l1_opy_
logger = bstack11l1l1l111_opy_.get_logger(__name__, bstack11l1l1l111_opy_.bstack1llll11l1ll_opy_())
def bstack1lll1lll11l_opy_(bs_config):
    bstack1lll111l111_opy_ = None
    bstack1lll1l1111l_opy_ = None
    try:
        bstack1lll1l1111l_opy_ = get_cli_dir()
        bstack1lll111l111_opy_ = bstack1ll1ll1lll1_opy_(bstack1lll1l1111l_opy_)
        bstack1lll1111111_opy_ = bstack1lll1ll11ll_opy_(bstack1lll111l111_opy_, bstack1lll1l1111l_opy_, bs_config)
        bstack1lll111l111_opy_ = bstack1lll1111111_opy_ if bstack1lll1111111_opy_ else bstack1lll111l111_opy_
        if not bstack1lll111l111_opy_:
            raise ValueError(bstack11ll1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥၧ"))
    except Exception as ex:
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠ࡭ࡣࡷࡩࡸࡺࠠࡣ࡫ࡱࡥࡷࡿࠠࡼࡿࠥၨ").format(ex))
        bstack1lll111l111_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦၩ"))
        if bstack1lll111l111_opy_:
            logger.debug(bstack11ll1l1_opy_ (u"ࠤࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡴࡲࡱࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠽ࠤࠧၪ") + str(bstack1lll111l111_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦၫ"))
        else:
            logger.debug(bstack11ll1l1_opy_ (u"ࠦࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠽ࠣࡷࡪࡺࡵࡱࠢࡰࡥࡾࠦࡢࡦࠢ࡬ࡲࡨࡵ࡭ࡱ࡮ࡨࡸࡪ࠴ࠢၬ"))
    return bstack1lll111l111_opy_, bstack1lll1l1111l_opy_
bstack1lll11ll111_opy_ = bstack11ll1l1_opy_ (u"ࠧ࠿࠹࠺࠻ࠥၭ")
bstack1lll11l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠨࡲࡦࡣࡧࡽࠧၮ")
bstack1ll1ll1111l_opy_ = bstack11ll1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦၯ")
bstack1ll1ll11111_opy_ = bstack11ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡎࡌࡗ࡙ࡋࡎࡠࡃࡇࡈࡗࠨၰ")
bstack111lll111_opy_ = bstack11ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧၱ")
bstack1lll11lll11_opy_ = re.compile(bstack11ll1l1_opy_ (u"ࡵࠦ࠭ࡅࡩࠪ࠰࠭ࠬࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡿࡆࡘ࠯࠮ࠫࠤၲ"))
bstack1lll11111ll_opy_ = bstack11ll1l1_opy_ (u"ࠦࡩ࡫ࡶࡦ࡮ࡲࡴࡲ࡫࡮ࡵࠤၳ")
bstack1lll11llll1_opy_ = [
    bstack1llllll1l1_opy_.bstack1l111ll1l_opy_,
    bstack1llllll1l1_opy_.CONNECT,
    bstack1llllll1l1_opy_.bstack11l1l1ll1l_opy_,
]
class SDKCLI:
    _1llll11l1l1_opy_ = None
    process: Union[None, Any]
    bstack1ll1ll11l11_opy_: bool
    bstack1llll1l1l1l_opy_: bool
    bstack1llll11l111_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1llll11ll1l_opy_: Union[None, grpc.Channel]
    bstack1lll11lll1l_opy_: str
    test_framework: TestFramework
    bstack1111111ll1_opy_: bstack1llllll1111_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1ll1ll11_opy_: bstack1lll11lllll_opy_
    accessibility: bstack1lll11l1ll1_opy_
    bstack1l1l1l1l11_opy_: bstack1lllll1lll_opy_
    ai: bstack1ll1ll11lll_opy_
    bstack1llll1ll111_opy_: bstack1lll1l1l1l1_opy_
    bstack1ll1lll1l11_opy_: List[bstack1lll1ll1l1l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1lllll1_opy_: Any
    bstack1llll1l1111_opy_: Dict[str, timedelta]
    bstack1lll11l1111_opy_: str
    bstack111111lll1_opy_: bstack111111ll11_opy_
    def __new__(cls):
        if not cls._1llll11l1l1_opy_:
            cls._1llll11l1l1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1llll11l1l1_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1ll11l11_opy_ = False
        self.bstack1llll11ll1l_opy_ = None
        self.bstack1lll1l1ll1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1ll11111_opy_, None)
        self.bstack1ll1ll1l11l_opy_ = os.environ.get(bstack1ll1ll1111l_opy_, bstack11ll1l1_opy_ (u"ࠧࠨၴ")) == bstack11ll1l1_opy_ (u"ࠨࠢၵ")
        self.bstack1llll1l1l1l_opy_ = False
        self.bstack1llll11l111_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1lllll1_opy_ = None
        self.test_framework = None
        self.bstack1111111ll1_opy_ = None
        self.bstack1lll11lll1l_opy_=bstack11ll1l1_opy_ (u"ࠢࠣၶ")
        self.session_framework = None
        self.logger = bstack11l1l1l111_opy_.get_logger(self.__class__.__name__, bstack11l1l1l111_opy_.bstack1llll11l1ll_opy_())
        self.bstack1llll1l1111_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack111111lll1_opy_ = bstack111111ll11_opy_()
        self.bstack1ll1l1ll1l1_opy_ = None
        self.bstack1ll1ll1ll1l_opy_ = None
        self.bstack1ll1ll1ll11_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1lll1l11_opy_ = []
    def bstack1ll1l1lll1_opy_(self):
        return os.environ.get(bstack111lll111_opy_).lower().__eq__(bstack11ll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨၷ"))
    def is_enabled(self, config):
        if bstack11ll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ၸ") in config and str(config[bstack11ll1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧၹ")]).lower() != bstack11ll1l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪၺ"):
            return False
        bstack1lll111llll_opy_ = [bstack11ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧၻ"), bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥၼ")]
        bstack1ll1ll111l1_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥၽ")) in bstack1lll111llll_opy_ or os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩၾ")) in bstack1lll111llll_opy_
        os.environ[bstack11ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧၿ")] = str(bstack1ll1ll111l1_opy_) # bstack1llll111lll_opy_ bstack1lll1l1llll_opy_ VAR to bstack1ll1llllll1_opy_ is binary running
        return bstack1ll1ll111l1_opy_
    def bstack111l111ll_opy_(self):
        for event in bstack1lll11llll1_opy_:
            bstack11l11lll1l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11l11lll1l_opy_.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨႀ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠦࠧႁ"))
            )
        bstack11l11lll1l_opy_.register(bstack1llllll1l1_opy_.bstack1l111ll1l_opy_, self.__1lll1llll11_opy_)
        bstack11l11lll1l_opy_.register(bstack1llllll1l1_opy_.CONNECT, self.__1ll1lll11ll_opy_)
        bstack11l11lll1l_opy_.register(bstack1llllll1l1_opy_.bstack11l1l1ll1l_opy_, self.__1lll11ll11l_opy_)
        bstack11l11lll1l_opy_.register(bstack1llllll1l1_opy_.bstack11l1ll11l_opy_, self.__1llll1111ll_opy_)
    def bstack1ll1ll111_opy_(self):
        return not self.bstack1ll1ll1l11l_opy_ and os.environ.get(bstack1ll1ll1111l_opy_, bstack11ll1l1_opy_ (u"ࠧࠨႂ")) != bstack11ll1l1_opy_ (u"ࠨࠢႃ")
    def is_running(self):
        if self.bstack1ll1ll1l11l_opy_:
            return self.bstack1ll1ll11l11_opy_
        else:
            return bool(self.bstack1llll11ll1l_opy_)
    def bstack1lll11l11l1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1lll1l11_opy_) and cli.is_running()
    def __1llll11111l_opy_(self, bstack1lll111l11l_opy_=10):
        if self.bstack1lll1l1ll1l_opy_:
            return
        bstack11ll11ll1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1ll11111_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢ࡜ࠤႄ") + str(id(self)) + bstack11ll1l1_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢႅ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11ll1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦႆ"), 0), (bstack11ll1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨႇ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll111l11l_opy_)
        self.bstack1llll11ll1l_opy_ = channel
        self.bstack1lll1l1ll1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1llll11ll1l_opy_)
        self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥႈ"), datetime.now() - bstack11ll11ll1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1ll11111_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧႉ") + str(self.bstack1ll1ll111_opy_()) + bstack11ll1l1_opy_ (u"ࠨࠢႊ"))
    def __1lll11ll11l_opy_(self, event_name):
        if self.bstack1ll1ll111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢႋ"))
        self.__1lll1l1l11l_opy_()
    def __1llll1111ll_opy_(self, event_name, bstack1lll111lll1_opy_ = None, bstack1ll1lll111_opy_=1):
        if bstack1ll1lll111_opy_ == 1:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣႌ"))
        bstack1ll1l1lllll_opy_ = Path(bstack1llll1111l1_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰႍࠥ"))
        if self.bstack1lll1l1111l_opy_ and bstack1ll1l1lllll_opy_.exists():
            with open(bstack1ll1l1lllll_opy_, bstack11ll1l1_opy_ (u"ࠪࡶࠬႎ"), encoding=bstack11ll1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪႏ")) as fp:
                data = json.load(fp)
                try:
                    bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡖࡏࡔࡖࠪ႐"), bstack111l11ll_opy_(bstack11lll11lll_opy_), data, {
                        bstack11ll1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ႑"): (self.config[bstack11ll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ႒")], self.config[bstack11ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ႓")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1lll11l1_opy_.format(str(e)))
            bstack1ll1l1lllll_opy_.unlink()
        sys.exit(bstack1ll1lll111_opy_)
    @measure(event_name=EVENTS.bstack1lll1111ll1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def __1lll1llll11_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
        self.bstack1lll11lll1l_opy_, self.bstack1lll1l1111l_opy_ = bstack1lll1lll11l_opy_(data.bs_config)
        os.environ[bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧ႔")] = self.bstack1lll1l1111l_opy_
        if not self.bstack1lll11lll1l_opy_ or not self.bstack1lll1l1111l_opy_:
            raise ValueError(bstack11ll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤ႕"))
        if self.bstack1ll1ll111_opy_():
            self.__1ll1lll11ll_opy_(event_name, bstack1111111ll_opy_())
            return
        try:
            bstack1llll11lll1_opy_.end(EVENTS.bstack1l1111lll_opy_.value, EVENTS.bstack1l1111lll_opy_.value + bstack11ll1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ႖"), EVENTS.bstack1l1111lll_opy_.value + bstack11ll1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ႗"), status=True, failure=None, test_name=None)
            logger.debug(bstack11ll1l1_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧ႘"))
        except Exception as e:
            logger.debug(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦ႙").format(e))
        start = datetime.now()
        is_started = self.__1ll1llll111_opy_()
        self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧႚ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1llll11111l_opy_()
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣႛ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1ll1l111_opy_(data)
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣႜ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll111ll11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def __1ll1lll11ll_opy_(self, event_name: str, data: bstack1111111ll_opy_):
        if not self.bstack1ll1ll111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣႝ"))
            return
        bin_session_id = os.environ.get(bstack1ll1ll1111l_opy_)
        start = datetime.now()
        self.__1llll11111l_opy_()
        self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦ႞"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧ႟") + str(bin_session_id) + bstack11ll1l1_opy_ (u"ࠢࠣႠ"))
        start = datetime.now()
        self.__1ll1lll1111_opy_()
        self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨႡ"), datetime.now() - start)
    def __1ll1lll1ll1_opy_(self):
        if not self.bstack1lll1l1ll1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨႢ"))
            return
        bstack1llll11ll11_opy_ = {
            bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢႣ"): (bstack1lll1llllll_opy_, bstack1lll1l111ll_opy_, bstack1lll111111l_opy_),
            bstack11ll1l1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨႤ"): (bstack1lll1l1l1ll_opy_, bstack1lll111l1l1_opy_, bstack1ll1lllllll_opy_),
        }
        if not self.bstack1ll1l1ll1l1_opy_ and self.session_framework in bstack1llll11ll11_opy_:
            bstack1ll1l1ll1ll_opy_, bstack1lll1l1ll11_opy_, bstack1llll1ll11l_opy_ = bstack1llll11ll11_opy_[self.session_framework]
            bstack1ll1lll11l1_opy_ = bstack1lll1l1ll11_opy_()
            self.bstack1ll1ll1ll1l_opy_ = bstack1ll1lll11l1_opy_
            self.bstack1ll1l1ll1l1_opy_ = bstack1llll1ll11l_opy_
            self.bstack1ll1lll1l11_opy_.append(bstack1ll1lll11l1_opy_)
            self.bstack1ll1lll1l11_opy_.append(bstack1ll1l1ll1ll_opy_(self.bstack1ll1ll1ll1l_opy_))
        if not self.bstack1ll1ll1ll11_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1lllll11_opy_
            self.bstack1ll1ll1ll11_opy_ = bstack1lll11lllll_opy_(self.bstack1ll1l1ll1l1_opy_, self.bstack1ll1ll1ll1l_opy_) # bstack1lll1l1l111_opy_
            self.bstack1ll1lll1l11_opy_.append(self.bstack1ll1ll1ll11_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll11l1ll1_opy_(self.bstack1ll1l1ll1l1_opy_, self.bstack1ll1ll1ll1l_opy_)
            self.bstack1ll1lll1l11_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11ll1l1_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢႥ"), False) == True:
            self.ai = bstack1ll1ll11lll_opy_()
            self.bstack1ll1lll1l11_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1lllll1_opy_ and self.bstack1lll1lllll1_opy_.success:
            self.percy = bstack1lll1l1l1l1_opy_(self.bstack1lll1lllll1_opy_)
            self.bstack1ll1lll1l11_opy_.append(self.percy)
        for mod in self.bstack1ll1lll1l11_opy_:
            if not mod.bstack1lll1ll1ll1_opy_():
                mod.configure(self.bstack1lll1l1ll1l_opy_, self.config, self.cli_bin_session_id, self.bstack111111lll1_opy_)
    def __1lll1l1lll1_opy_(self):
        for mod in self.bstack1ll1lll1l11_opy_:
            if mod.bstack1lll1ll1ll1_opy_():
                mod.configure(self.bstack1lll1l1ll1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1ll1l1l1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def __1ll1ll1l111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1llll1l1l1l_opy_:
            return
        self.__1lll11l11ll_opy_(data)
        bstack11ll11ll1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨႦ")
        req.sdk_language = bstack11ll1l1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢႧ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll11lll11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣ࡝ࠥႨ") + str(id(self)) + bstack11ll1l1_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣႩ"))
            r = self.bstack1lll1l1ll1l_opy_.StartBinSession(req)
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧႪ"), datetime.now() - bstack11ll11ll1_opy_)
            os.environ[bstack1ll1ll1111l_opy_] = r.bin_session_id
            self.__1ll1ll11l1l_opy_(r)
            self.__1ll1lll1ll1_opy_()
            self.bstack111111lll1_opy_.start()
            self.bstack1llll1l1l1l_opy_ = True
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡠࠨႫ") + str(id(self)) + bstack11ll1l1_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥႬ"))
        except grpc.bstack1lll1l11l11_opy_ as bstack1llll1l11ll_opy_:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣႭ") + str(bstack1llll1l11ll_opy_) + bstack11ll1l1_opy_ (u"ࠢࠣႮ"))
            traceback.print_exc()
            raise bstack1llll1l11ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧႯ") + str(e) + bstack11ll1l1_opy_ (u"ࠤࠥႰ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1llll11l_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def __1ll1lll1111_opy_(self):
        if not self.bstack1ll1ll111_opy_() or not self.cli_bin_session_id or self.bstack1llll11l111_opy_:
            return
        bstack11ll11ll1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪႱ"), bstack11ll1l1_opy_ (u"ࠫ࠵࠭Ⴒ")))
        try:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡡࠢႳ") + str(id(self)) + bstack11ll1l1_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣႴ"))
            r = self.bstack1lll1l1ll1l_opy_.ConnectBinSession(req)
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦႵ"), datetime.now() - bstack11ll11ll1_opy_)
            self.__1ll1ll11l1l_opy_(r)
            self.__1ll1lll1ll1_opy_()
            self.bstack111111lll1_opy_.start()
            self.bstack1llll11l111_opy_ = True
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣ࡝ࠥႶ") + str(id(self)) + bstack11ll1l1_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣႷ"))
        except grpc.bstack1lll1l11l11_opy_ as bstack1llll1l11ll_opy_:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧႸ") + str(bstack1llll1l11ll_opy_) + bstack11ll1l1_opy_ (u"ࠦࠧႹ"))
            traceback.print_exc()
            raise bstack1llll1l11ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤႺ") + str(e) + bstack11ll1l1_opy_ (u"ࠨࠢႻ"))
            traceback.print_exc()
            raise e
    def __1ll1ll11l1l_opy_(self, r):
        self.bstack1lll11ll1ll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11ll1l1_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨႼ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11ll1l1_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨႽ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11ll1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦႾ")
        self.bstack1lll1lllll1_opy_ = getattr(r, bstack11ll1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩႿ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨჀ")] = self.config_testhub.jwt
        os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪჁ")] = self.config_testhub.build_hashed_id
    def bstack1lll111l1ll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1ll11l11_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll1ll11ll1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll1ll11ll1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll111l1ll_opy_(event_name=EVENTS.bstack1lll1l11ll1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def __1ll1llll111_opy_(self, bstack1lll111l11l_opy_=10):
        if self.bstack1ll1ll11l11_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣჂ"))
            return True
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨჃ"))
        if os.getenv(bstack11ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣჄ")) == bstack1lll11111ll_opy_:
            self.cli_bin_session_id = bstack1lll11111ll_opy_
            self.cli_listen_addr = bstack11ll1l1_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧჅ") % (self.cli_bin_session_id)
            self.bstack1ll1ll11l11_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll11lll1l_opy_, bstack11ll1l1_opy_ (u"ࠥࡷࡩࡱࠢ჆")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1lll1lll_opy_ compat for text=True in bstack1lll11l1l11_opy_ python
            encoding=bstack11ll1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥჇ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll1lll1l1_opy_ = threading.Thread(target=self.__1lll1ll11l1_opy_, args=(bstack1lll111l11l_opy_,))
        bstack1lll1lll1l1_opy_.start()
        bstack1lll1lll1l1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤ჈") + str(self.process.stderr.read()) + bstack11ll1l1_opy_ (u"ࠨࠢ჉"))
        if not self.bstack1ll1ll11l11_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢ࡜ࠤ჊") + str(id(self)) + bstack11ll1l1_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦ჋"))
            self.__1lll1l1l11l_opy_()
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥ჌") + str(self.bstack1ll1ll11l11_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦჍ"))
        return self.bstack1ll1ll11l11_opy_
    def __1lll1ll11l1_opy_(self, bstack1lll1lll111_opy_=10):
        bstack1llll1l111l_opy_ = time.time()
        while self.process and time.time() - bstack1llll1l111l_opy_ < bstack1lll1lll111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11ll1l1_opy_ (u"ࠦ࡮ࡪ࠽ࠣ჎") in line:
                    self.cli_bin_session_id = line.split(bstack11ll1l1_opy_ (u"ࠧ࡯ࡤ࠾ࠤ჏"))[-1:][0].strip()
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧა") + str(self.cli_bin_session_id) + bstack11ll1l1_opy_ (u"ࠢࠣბ"))
                    continue
                if bstack11ll1l1_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤგ") in line:
                    self.cli_listen_addr = line.split(bstack11ll1l1_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥდ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨე") + str(self.cli_listen_addr) + bstack11ll1l1_opy_ (u"ࠦࠧვ"))
                    continue
                if bstack11ll1l1_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦზ") in line:
                    port = line.split(bstack11ll1l1_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧთ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨი") + str(port) + bstack11ll1l1_opy_ (u"ࠣࠤკ"))
                    continue
                if line.strip() == bstack1lll11l1l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11ll1l1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦლ"), bstack11ll1l1_opy_ (u"ࠥ࠵ࠧმ")) == bstack11ll1l1_opy_ (u"ࠦ࠶ࠨნ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1ll11l11_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨო") + str(e) + bstack11ll1l1_opy_ (u"ࠨࠢპ"))
        return False
    @measure(event_name=EVENTS.bstack1lll1l11l1l_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def __1lll1l1l11l_opy_(self):
        if self.bstack1llll11ll1l_opy_:
            self.bstack111111lll1_opy_.stop()
            start = datetime.now()
            if self.bstack1llll111111_opy_():
                self.cli_bin_session_id = None
                if self.bstack1llll11l111_opy_:
                    self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦჟ"), datetime.now() - start)
                else:
                    self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧრ"), datetime.now() - start)
            self.__1lll1l1lll1_opy_()
            start = datetime.now()
            self.bstack1llll11ll1l_opy_.close()
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦს"), datetime.now() - start)
            self.bstack1llll11ll1l_opy_ = None
        if self.process:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡷࡹࡵࡰࠣტ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢუ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll1ll1l11l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l11l11ll_opy_()
                self.logger.info(
                    bstack11ll1l1_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠣფ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11ll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬქ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1ll11l11_opy_ = False
    def __1lll11l11ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11ll1l1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤღ")] = selenium.__version__
            data.frameworks.append(bstack11ll1l1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥყ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11ll1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨშ")] = __version__
            data.frameworks.append(bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢჩ"))
        except:
            pass
    def bstack1ll1l1lll11_opy_(self, hub_url: str, platform_index: int, bstack1lll1l1ll_opy_: Any):
        if self.bstack1111111ll1_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣც"))
            return
        try:
            bstack11ll11ll1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11ll1l1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢძ")
            self.bstack1111111ll1_opy_ = bstack1ll1lllllll_opy_(
                cli.config.get(bstack11ll1l1_opy_ (u"ࠨࡨࡶࡤࡘࡶࡱࠨწ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1llll1l1_opy_={bstack11ll1l1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦჭ"): bstack1lll1l1ll_opy_}
            )
            def bstack1ll1lll111l_opy_(self):
                return
            if self.config.get(bstack11ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥხ"), True):
                Service.start = bstack1ll1lll111l_opy_
                Service.stop = bstack1ll1lll111l_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1lllll1lll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1llll1l11l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥჯ"), datetime.now() - bstack11ll11ll1_opy_)
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤჰ") + str(e) + bstack11ll1l1_opy_ (u"ࠦࠧჱ"))
    def bstack1lll11111l1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l11lll1l_opy_
            self.bstack1111111ll1_opy_ = bstack1lll111111l_opy_(
                platform_index,
                framework_name=bstack11ll1l1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤჲ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࠢჳ") + str(e) + bstack11ll1l1_opy_ (u"ࠢࠣჴ"))
            pass
    def bstack1lll1ll1lll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥჵ"))
            return
        if bstack1lll111l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11ll1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤჶ"): pytest.__version__ }, [bstack11ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢჷ")], self.bstack111111lll1_opy_, self.bstack1lll1l1ll1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1llll1ll_opy_({ bstack11ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦჸ"): pytest.__version__ }, [bstack11ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧჹ")], self.bstack111111lll1_opy_, self.bstack1lll1l1ll1l_opy_)
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥჺ") + str(e) + bstack11ll1l1_opy_ (u"ࠢࠣ჻"))
        self.bstack1llll1l1l11_opy_()
    def bstack1llll1l1l11_opy_(self):
        if not self.bstack1ll1l1lll1_opy_():
            return
        bstack1l1l1ll11l_opy_ = None
        def bstack11111lll1_opy_(config, startdir):
            return bstack11ll1l1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨჼ").format(bstack11ll1l1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣჽ"))
        def bstack111l1ll11_opy_():
            return
        def bstack1l1ll1ll1l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11ll1l1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪჾ"):
                return bstack11ll1l1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥჿ")
            else:
                return bstack1l1l1ll11l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1l1ll11l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11111lll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111l1ll11_opy_
            Config.getoption = bstack1l1ll1ll1l_opy_
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢᄀ") + str(e) + bstack11ll1l1_opy_ (u"ࠨࠢᄁ"))
    def bstack1lll1111l11_opy_(self):
        bstack1l111l1ll1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1l111l1ll1_opy_, dict):
            if cli.config_observability:
                bstack1l111l1ll1_opy_.update(
                    {bstack11ll1l1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᄂ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11ll1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦᄃ") in accessibility.get(bstack11ll1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᄄ"), {}):
                    bstack1lll11l111l_opy_ = accessibility.get(bstack11ll1l1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᄅ"))
                    bstack1lll11l111l_opy_.update({ bstack11ll1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧᄆ"): bstack1lll11l111l_opy_.pop(bstack11ll1l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣᄇ")) })
                bstack1l111l1ll1_opy_.update({bstack11ll1l1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᄈ"): accessibility })
        return bstack1l111l1ll1_opy_
    @measure(event_name=EVENTS.bstack1lll1lll1ll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1llll111111_opy_(self, bstack1llll111l1l_opy_: str = None, bstack1llll111l11_opy_: str = None, bstack1ll1lll111_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll1l1ll1l_opy_:
            return
        bstack11ll11ll1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1ll1lll111_opy_:
            req.bstack1ll1lll111_opy_ = bstack1ll1lll111_opy_
        if bstack1llll111l1l_opy_:
            req.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
        if bstack1llll111l11_opy_:
            req.bstack1llll111l11_opy_ = bstack1llll111l11_opy_
        try:
            r = self.bstack1lll1l1ll1l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡰࡲࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᄉ"), datetime.now() - bstack11ll11ll1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11l111ll_opy_(self, key: str, value: timedelta):
        tag = bstack11ll1l1_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᄊ") if self.bstack1ll1ll111_opy_() else bstack11ll1l1_opy_ (u"ࠤࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᄋ")
        self.bstack1llll1l1111_opy_[bstack11ll1l1_opy_ (u"ࠥ࠾ࠧᄌ").join([tag + bstack11ll1l1_opy_ (u"ࠦ࠲ࠨᄍ") + str(id(self)), key])] += value
    def bstack1l11l11ll_opy_(self):
        if not os.getenv(bstack11ll1l1_opy_ (u"ࠧࡊࡅࡃࡗࡊࡣࡕࡋࡒࡇࠤᄎ"), bstack11ll1l1_opy_ (u"ࠨ࠰ࠣᄏ")) == bstack11ll1l1_opy_ (u"ࠢ࠲ࠤᄐ"):
            return
        bstack1ll1l1llll1_opy_ = dict()
        bstack1llllll11l1_opy_ = []
        if self.test_framework:
            bstack1llllll11l1_opy_.extend(list(self.test_framework.bstack1llllll11l1_opy_.values()))
        if self.bstack1111111ll1_opy_:
            bstack1llllll11l1_opy_.extend(list(self.bstack1111111ll1_opy_.bstack1llllll11l1_opy_.values()))
        for instance in bstack1llllll11l1_opy_:
            if not instance.platform_index in bstack1ll1l1llll1_opy_:
                bstack1ll1l1llll1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll1l1llll1_opy_[instance.platform_index]
            for k, v in instance.bstack1lll1llll1l_opy_().items():
                report[k] += v
                report[k.split(bstack11ll1l1_opy_ (u"ࠣ࠼ࠥᄑ"))[0]] += v
        bstack1lll1l11111_opy_ = sorted([(k, v) for k, v in self.bstack1llll1l1111_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1llll1l1ll1_opy_ = 0
        for r in bstack1lll1l11111_opy_:
            bstack1llll11llll_opy_ = r[1].total_seconds()
            bstack1llll1l1ll1_opy_ += bstack1llll11llll_opy_
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡻࡳ࡝࠳ࡡࢂࡃࠢᄒ") + str(bstack1llll11llll_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦᄓ"))
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠦ࠲࠳ࠢᄔ"))
        bstack1ll1ll1l1ll_opy_ = []
        for platform_index, report in bstack1ll1l1llll1_opy_.items():
            bstack1ll1ll1l1ll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1ll1l1ll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l11llll1_opy_ = set()
        bstack1lll1ll1111_opy_ = 0
        for r in bstack1ll1ll1l1ll_opy_:
            bstack1llll11llll_opy_ = r[2].total_seconds()
            bstack1lll1ll1111_opy_ += bstack1llll11llll_opy_
            bstack1l11llll1_opy_.add(r[0])
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࢁࡲ࡜࠲ࡠࢁ࠿ࢁࡲ࡜࠳ࡠࢁࡂࠨᄕ") + str(bstack1llll11llll_opy_) + bstack11ll1l1_opy_ (u"ࠨࠢᄖ"))
        if self.bstack1ll1ll111_opy_():
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢ࠮࠯ࠥᄗ"))
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࢁࡴࡰࡶࡤࡰࡤࡩ࡬ࡪࡿࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠱ࢀࡹࡴࡳࠪࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠮ࢃ࠽ࠣᄘ") + str(bstack1lll1ll1111_opy_) + bstack11ll1l1_opy_ (u"ࠤࠥᄙ"))
        else:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࠢᄚ") + str(bstack1llll1l1ll1_opy_) + bstack11ll1l1_opy_ (u"ࠦࠧᄛ"))
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠧ࠳࠭ࠣᄜ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1lll1l1ll1l_opy_:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᄝ"))
            return None
        response = self.bstack1lll1l1ll1l_opy_.TestOrchestration(request)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤᄞ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1lll11ll1ll_opy_(self, r):
        if r is not None and getattr(r, bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩᄟ"), None) and getattr(r.testhub, bstack11ll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᄠ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11ll1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᄡ")))
            for bstack1lll11l1lll_opy_, err in errors.items():
                if err[bstack11ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩᄢ")] == bstack11ll1l1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᄣ"):
                    self.logger.info(err[bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄤ")])
                else:
                    self.logger.error(err[bstack11ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᄥ")])
    def bstack11l11l11_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()