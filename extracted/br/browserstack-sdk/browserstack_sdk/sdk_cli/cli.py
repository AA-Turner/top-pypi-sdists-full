# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack111111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11ll1_opy_ import bstack1llll1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1lll1ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1l11l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111ll_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack11111l11l_opy_ import bstack11111l11l_opy_, bstack11l11l1l_opy_, bstack11ll1111ll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l11_opy_ import bstack1lll1lll1l1_opy_
from bstack_utils.helper import Notset, bstack1ll1ll11l1l_opy_, get_cli_dir, bstack1ll1llll11l_opy_, bstack111ll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11ll_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1ll1_opy_ import bstack11111lll1_opy_
from bstack_utils.helper import Notset, bstack1ll1ll11l1l_opy_, get_cli_dir, bstack1ll1llll11l_opy_, bstack111ll11l_opy_, bstack1llll1ll_opy_, bstack11lll11111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll11111l_opy_, bstack1llll111l11_opy_, bstack1ll1l1lll11_opy_, bstack1lll11lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import bstack1llll1ll1ll_opy_, bstack1111111l11_opy_, bstack1llllll1111_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l1111ll1_opy_ import bstack11ll11l1ll_opy_
from bstack_utils import bstack1111l1ll1_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack111ll1l1l_opy_, bstack1l1111ll1l_opy_
logger = bstack1111l1ll1_opy_.get_logger(__name__, bstack1111l1ll1_opy_.bstack1lll1lll1ll_opy_())
def bstack1lll11llll1_opy_(bs_config):
    bstack1ll1ll1l111_opy_ = None
    bstack1lll1111l11_opy_ = None
    try:
        bstack1lll1111l11_opy_ = get_cli_dir()
        bstack1ll1ll1l111_opy_ = bstack1ll1llll11l_opy_(bstack1lll1111l11_opy_)
        bstack1llll11ll1l_opy_ = bstack1ll1ll11l1l_opy_(bstack1ll1ll1l111_opy_, bstack1lll1111l11_opy_, bs_config)
        bstack1ll1ll1l111_opy_ = bstack1llll11ll1l_opy_ if bstack1llll11ll1l_opy_ else bstack1ll1ll1l111_opy_
        if not bstack1ll1ll1l111_opy_:
            raise ValueError(bstack11ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤၦ"))
    except Exception as ex:
        logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡬ࡢࡶࡨࡷࡹࠦࡢࡪࡰࡤࡶࡾࠦࡻࡾࠤၧ").format(ex))
        bstack1ll1ll1l111_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥၨ"))
        if bstack1ll1ll1l111_opy_:
            logger.debug(bstack11ll11_opy_ (u"ࠣࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡳࡱࡰࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࠦၩ") + str(bstack1ll1ll1l111_opy_) + bstack11ll11_opy_ (u"ࠤࠥၪ"))
        else:
            logger.debug(bstack11ll11_opy_ (u"ࠥࡒࡴࠦࡶࡢ࡮࡬ࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠼ࠢࡶࡩࡹࡻࡰࠡ࡯ࡤࡽࠥࡨࡥࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨၫ"))
    return bstack1ll1ll1l111_opy_, bstack1lll1111l11_opy_
bstack1ll1llll111_opy_ = bstack11ll11_opy_ (u"ࠦ࠾࠿࠹࠺ࠤၬ")
bstack1ll1lll1l11_opy_ = bstack11ll11_opy_ (u"ࠧࡸࡥࡢࡦࡼࠦၭ")
bstack1lll1111ll1_opy_ = bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥၮ")
bstack1llll1111l1_opy_ = bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡍࡋࡖࡘࡊࡔ࡟ࡂࡆࡇࡖࠧၯ")
bstack11ll11l1_opy_ = bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦၰ")
bstack1ll1ll11l11_opy_ = re.compile(bstack11ll11_opy_ (u"ࡴࠥࠬࡄ࡯ࠩ࠯ࠬࠫࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡾࡅࡗ࠮࠴ࠪࠣၱ"))
bstack1ll1ll111l1_opy_ = bstack11ll11_opy_ (u"ࠥࡨࡪࡼࡥ࡭ࡱࡳࡱࡪࡴࡴࠣၲ")
bstack1lll1l1l111_opy_ = [
    bstack11l11l1l_opy_.bstack1l11l11lll_opy_,
    bstack11l11l1l_opy_.CONNECT,
    bstack11l11l1l_opy_.bstack1l11ll1l_opy_,
]
class SDKCLI:
    _1lll11l1111_opy_ = None
    process: Union[None, Any]
    bstack1llll1l1lll_opy_: bool
    bstack1lll1ll1ll1_opy_: bool
    bstack1ll1ll1ll1l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll11ll11l_opy_: Union[None, grpc.Channel]
    bstack1lll1111l1l_opy_: str
    test_framework: TestFramework
    bstack1lllll1lll1_opy_: bstack1111111ll1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1ll1111l_opy_: bstack1llll11l11l_opy_
    accessibility: bstack1llll1ll111_opy_
    bstack1l1ll1ll1_opy_: bstack11111lll1_opy_
    ai: bstack1lll1ll111l_opy_
    bstack1lll1l1111l_opy_: bstack1lll1llll11_opy_
    bstack1lll111lll1_opy_: List[bstack1ll1ll1llll_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1l1l11l_opy_: Any
    bstack1llll11l1ll_opy_: Dict[str, timedelta]
    bstack1lll111ll1l_opy_: str
    bstack111111l1ll_opy_: bstack111111ll1l_opy_
    def __new__(cls):
        if not cls._1lll11l1111_opy_:
            cls._1lll11l1111_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll11l1111_opy_
    def __init__(self):
        self.process = None
        self.bstack1llll1l1lll_opy_ = False
        self.bstack1lll11ll11l_opy_ = None
        self.bstack1llll1l1l11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1llll1111l1_opy_, None)
        self.bstack1lll111l1l1_opy_ = os.environ.get(bstack1lll1111ll1_opy_, bstack11ll11_opy_ (u"ࠦࠧၳ")) == bstack11ll11_opy_ (u"ࠧࠨၴ")
        self.bstack1lll1ll1ll1_opy_ = False
        self.bstack1ll1ll1ll1l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1l1l11l_opy_ = None
        self.test_framework = None
        self.bstack1lllll1lll1_opy_ = None
        self.bstack1lll1111l1l_opy_=bstack11ll11_opy_ (u"ࠨࠢၵ")
        self.session_framework = None
        self.logger = bstack1111l1ll1_opy_.get_logger(self.__class__.__name__, bstack1111l1ll1_opy_.bstack1lll1lll1ll_opy_())
        self.bstack1llll11l1ll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack111111l1ll_opy_ = bstack111111ll1l_opy_()
        self.bstack1ll1lllll11_opy_ = None
        self.bstack1lll1l111ll_opy_ = None
        self.bstack1ll1ll1111l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll111lll1_opy_ = []
    def bstack1l111lll1l_opy_(self):
        return os.environ.get(bstack11ll11l1_opy_).lower().__eq__(bstack11ll11_opy_ (u"ࠢࡵࡴࡸࡩࠧၶ"))
    def is_enabled(self, config):
        if bstack11ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬၷ") in config and str(config[bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ၸ")]).lower() != bstack11ll11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩၹ"):
            return False
        bstack1ll1ll111ll_opy_ = [bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦၺ"), bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤၻ")]
        bstack1lll111l1ll_opy_ = config.get(bstack11ll11_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤၼ")) in bstack1ll1ll111ll_opy_ or os.environ.get(bstack11ll11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨၽ")) in bstack1ll1ll111ll_opy_
        os.environ[bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦၾ")] = str(bstack1lll111l1ll_opy_) # bstack1lll1l11ll1_opy_ bstack1lll1lll11l_opy_ VAR to bstack1ll1lllllll_opy_ is binary running
        return bstack1lll111l1ll_opy_
    def bstack1ll1l111_opy_(self):
        for event in bstack1lll1l1l111_opy_:
            bstack11111l11l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11111l11l_opy_.logger.debug(bstack11ll11_opy_ (u"ࠤࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠡ࠿ࡁࠤࢀࡧࡲࡨࡵࢀࠤࠧၿ") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦႀ"))
            )
        bstack11111l11l_opy_.register(bstack11l11l1l_opy_.bstack1l11l11lll_opy_, self.__1lll1l1l1ll_opy_)
        bstack11111l11l_opy_.register(bstack11l11l1l_opy_.CONNECT, self.__1lll1ll11l1_opy_)
        bstack11111l11l_opy_.register(bstack11l11l1l_opy_.bstack1l11ll1l_opy_, self.__1ll1lll1lll_opy_)
        bstack11111l11l_opy_.register(bstack11l11l1l_opy_.bstack11llllll1l_opy_, self.__1llll1l1ll1_opy_)
    def bstack1l11111lll_opy_(self):
        return not self.bstack1lll111l1l1_opy_ and os.environ.get(bstack1lll1111ll1_opy_, bstack11ll11_opy_ (u"ࠦࠧႁ")) != bstack11ll11_opy_ (u"ࠧࠨႂ")
    def is_running(self):
        if self.bstack1lll111l1l1_opy_:
            return self.bstack1llll1l1lll_opy_
        else:
            return bool(self.bstack1lll11ll11l_opy_)
    def bstack1lll1111lll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll111lll1_opy_) and cli.is_running()
    def __1ll1ll1l1l1_opy_(self, bstack1ll1llll1ll_opy_=10):
        if self.bstack1llll1l1l11_opy_:
            return
        bstack1ll1lll1ll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1llll1111l1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡛ࠣႃ") + str(id(self)) + bstack11ll11_opy_ (u"ࠢ࡞ࠢࡦࡳࡳࡴࡥࡤࡶ࡬ࡲ࡬ࠨႄ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11ll11_opy_ (u"ࠣࡩࡵࡴࡨ࠴ࡥ࡯ࡣࡥࡰࡪࡥࡨࡵࡶࡳࡣࡵࡸ࡯ࡹࡻࠥႅ"), 0), (bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡸࡥࡰࡳࡱࡻࡽࠧႆ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll1llll1ll_opy_)
        self.bstack1lll11ll11l_opy_ = channel
        self.bstack1llll1l1l11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll11ll11l_opy_)
        self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࠤႇ"), datetime.now() - bstack1ll1lll1ll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1llll1111l1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࡀࠠࡪࡵࡢࡧ࡭࡯࡬ࡥࡡࡳࡶࡴࡩࡥࡴࡵࡀࠦႈ") + str(self.bstack1l11111lll_opy_()) + bstack11ll11_opy_ (u"ࠧࠨႉ"))
    def __1ll1lll1lll_opy_(self, event_name):
        if self.bstack1l11111lll_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡴࡶࡲࡴࡵ࡯࡮ࡨࠢࡆࡐࡎࠨႊ"))
        self.__1lll1ll1lll_opy_()
    def __1llll1l1ll1_opy_(self, event_name, bstack1lll1llllll_opy_ = None, bstack11lll111l_opy_=1):
        if bstack11lll111l_opy_ == 1:
            self.logger.error(bstack11ll11_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠢႋ"))
        bstack1ll1lll11ll_opy_ = Path(bstack1lll11ll111_opy_ (u"ࠣࡽࡶࡩࡱ࡬࠮ࡤ࡮࡬ࡣࡩ࡯ࡲࡾ࠱ࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࡶ࠲࡯ࡹ࡯࡯ࠤႌ"))
        if self.bstack1lll1111l11_opy_ and bstack1ll1lll11ll_opy_.exists():
            with open(bstack1ll1lll11ll_opy_, bstack11ll11_opy_ (u"ࠩࡵႍࠫ"), encoding=bstack11ll11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩႎ")) as fp:
                data = json.load(fp)
                try:
                    bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠫࡕࡕࡓࡕࠩႏ"), bstack11ll11l1ll_opy_(bstack1l1l1lll_opy_), data, {
                        bstack11ll11_opy_ (u"ࠬࡧࡵࡵࡪࠪ႐"): (self.config[bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ႑")], self.config[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ႒")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1111ll1l_opy_.format(str(e)))
            bstack1ll1lll11ll_opy_.unlink()
        sys.exit(bstack11lll111l_opy_)
    @measure(event_name=EVENTS.bstack1ll1llllll1_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1lll1l1l1ll_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
        self.bstack1lll1111l1l_opy_, self.bstack1lll1111l11_opy_ = bstack1lll11llll1_opy_(data.bs_config)
        os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡘࡔࡌࡘࡆࡈࡌࡆࡡࡇࡍࡗ࠭႓")] = self.bstack1lll1111l11_opy_
        if not self.bstack1lll1111l1l_opy_ or not self.bstack1lll1111l11_opy_:
            raise ValueError(bstack11ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠣ႔"))
        if self.bstack1l11111lll_opy_():
            self.__1lll1ll11l1_opy_(event_name, bstack11ll1111ll_opy_())
            return
        try:
            bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1l11llllll_opy_.value, EVENTS.bstack1l11llllll_opy_.value + bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ႕"), EVENTS.bstack1l11llllll_opy_.value + bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ႖"), status=True, failure=None, test_name=None)
            logger.debug(bstack11ll11_opy_ (u"ࠧࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡔࡆࡎࠤࡘ࡫ࡴࡶࡲ࠱ࠦ႗"))
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥ႘").format(e))
        start = datetime.now()
        is_started = self.__1ll1lllll1l_opy_()
        self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠢࡴࡲࡤࡻࡳࡥࡴࡪ࡯ࡨࠦ႙"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1ll1l1l1_opy_()
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢႚ"), datetime.now() - start)
            start = datetime.now()
            self.__1lll1l11111_opy_(data)
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢႛ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1llll1l111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1lll1ll11l1_opy_(self, event_name: str, data: bstack11ll1111ll_opy_):
        if not self.bstack1l11111lll_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࡰࡲࡸࠥࡧࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢႜ"))
            return
        bin_session_id = os.environ.get(bstack1lll1111ll1_opy_)
        start = datetime.now()
        self.__1ll1ll1l1l1_opy_()
        self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥႝ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡃࡍࡋࠣࠦ႞") + str(bin_session_id) + bstack11ll11_opy_ (u"ࠨࠢ႟"))
        start = datetime.now()
        self.__1ll1l1lll1l_opy_()
        self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧႠ"), datetime.now() - start)
    def __1lll1ll1111_opy_(self):
        if not self.bstack1llll1l1l11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡥࡤࡲࡳࡵࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡲࡵࡤࡶ࡮ࡨࡷࠧႡ"))
            return
        bstack1lll1l1lll1_opy_ = {
            bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨႢ"): (bstack1lll1l11l1l_opy_, bstack1llll111111_opy_, bstack1lll1lll1l1_opy_),
            bstack11ll11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႣ"): (bstack1ll1l1llll1_opy_, bstack1lll1l1l1l1_opy_, bstack1llll11l111_opy_),
        }
        if not self.bstack1ll1lllll11_opy_ and self.session_framework in bstack1lll1l1lll1_opy_:
            bstack1lll11lll1l_opy_, bstack1llll1l1l1l_opy_, bstack1ll1l1lllll_opy_ = bstack1lll1l1lll1_opy_[self.session_framework]
            bstack1lll11ll1l1_opy_ = bstack1llll1l1l1l_opy_()
            self.bstack1lll1l111ll_opy_ = bstack1lll11ll1l1_opy_
            self.bstack1ll1lllll11_opy_ = bstack1ll1l1lllll_opy_
            self.bstack1lll111lll1_opy_.append(bstack1lll11ll1l1_opy_)
            self.bstack1lll111lll1_opy_.append(bstack1lll11lll1l_opy_(self.bstack1lll1l111ll_opy_))
        if not self.bstack1ll1ll1111l_opy_ and self.config_observability and self.config_observability.success: # bstack1lll11111ll_opy_
            self.bstack1ll1ll1111l_opy_ = bstack1llll11l11l_opy_(self.bstack1ll1lllll11_opy_, self.bstack1lll1l111ll_opy_) # bstack1lll1111111_opy_
            self.bstack1lll111lll1_opy_.append(self.bstack1ll1ll1111l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1llll1ll111_opy_(self.bstack1ll1lllll11_opy_, self.bstack1lll1l111ll_opy_)
            self.bstack1lll111lll1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11ll11_opy_ (u"ࠦࡸ࡫࡬ࡧࡊࡨࡥࡱࠨႤ"), False) == True:
            self.ai = bstack1lll1ll111l_opy_()
            self.bstack1lll111lll1_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1l1l11l_opy_ and self.bstack1lll1l1l11l_opy_.success:
            self.percy = bstack1lll1llll11_opy_(self.bstack1lll1l1l11l_opy_)
            self.bstack1lll111lll1_opy_.append(self.percy)
        for mod in self.bstack1lll111lll1_opy_:
            if not mod.bstack1lll1ll1l1l_opy_():
                mod.configure(self.bstack1llll1l1l11_opy_, self.config, self.cli_bin_session_id, self.bstack111111l1ll_opy_)
    def __1llll1ll11l_opy_(self):
        for mod in self.bstack1lll111lll1_opy_:
            if mod.bstack1lll1ll1l1l_opy_():
                mod.configure(self.bstack1llll1l1l11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1llll11l1l1_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1lll1l11111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll1ll1ll1_opy_:
            return
        self.__1lll1l1llll_opy_(data)
        bstack1ll1lll1ll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧႥ")
        req.sdk_language = bstack11ll11_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨႦ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll1ll11l11_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢ࡜ࠤႧ") + str(id(self)) + bstack11ll11_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢႨ"))
            r = self.bstack1llll1l1l11_opy_.StartBinSession(req)
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦႩ"), datetime.now() - bstack1ll1lll1ll_opy_)
            os.environ[bstack1lll1111ll1_opy_] = r.bin_session_id
            self.__1lll111111l_opy_(r)
            self.__1lll1ll1111_opy_()
            self.bstack111111l1ll_opy_.start()
            self.bstack1lll1ll1ll1_opy_ = True
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡟ࠧႪ") + str(id(self)) + bstack11ll11_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤႫ"))
        except grpc.bstack1ll1ll1l11l_opy_ as bstack1lll1ll1l11_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢႬ") + str(bstack1lll1ll1l11_opy_) + bstack11ll11_opy_ (u"ࠨࠢႭ"))
            traceback.print_exc()
            raise bstack1lll1ll1l11_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦႮ") + str(e) + bstack11ll11_opy_ (u"ࠣࠤႯ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll1l1111_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1ll1l1lll1l_opy_(self):
        if not self.bstack1l11111lll_opy_() or not self.cli_bin_session_id or self.bstack1ll1ll1ll1l_opy_:
            return
        bstack1ll1lll1ll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩႰ"), bstack11ll11_opy_ (u"ࠪ࠴ࠬႱ")))
        try:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࠨႲ") + str(id(self)) + bstack11ll11_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢႳ"))
            r = self.bstack1llll1l1l11_opy_.ConnectBinSession(req)
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥႴ"), datetime.now() - bstack1ll1lll1ll_opy_)
            self.__1lll111111l_opy_(r)
            self.__1lll1ll1111_opy_()
            self.bstack111111l1ll_opy_.start()
            self.bstack1ll1ll1ll1l_opy_ = True
            self.logger.debug(bstack11ll11_opy_ (u"ࠢ࡜ࠤႵ") + str(id(self)) + bstack11ll11_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢႶ"))
        except grpc.bstack1ll1ll1l11l_opy_ as bstack1lll1ll1l11_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦႷ") + str(bstack1lll1ll1l11_opy_) + bstack11ll11_opy_ (u"ࠥࠦႸ"))
            traceback.print_exc()
            raise bstack1lll1ll1l11_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣႹ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨႺ"))
            traceback.print_exc()
            raise e
    def __1lll111111l_opy_(self, r):
        self.bstack1ll1lll1111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11ll11_opy_ (u"ࠨࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧႻ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11ll11_opy_ (u"ࠢࡦ࡯ࡳࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡷࡱࡨࠧႼ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡥࡳࡥࡼࠤ࡮ࡹࠠࡴࡧࡱࡸࠥࡵ࡮࡭ࡻࠣࡥࡸࠦࡰࡢࡴࡷࠤࡴ࡬ࠠࡵࡪࡨࠤࠧࡉ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠮ࠥࠤࡦࡴࡤࠡࡶ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡦࡲࡳࡰࠢࡸࡷࡪࡪࠠࡣࡻࠣࡗࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡨࡶࡪ࡬࡯ࡳࡧ࠯ࠤࡓࡵ࡮ࡦࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤ࡮ࡹࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥႽ")
        self.bstack1lll1l1l11l_opy_ = getattr(r, bstack11ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨႾ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧႿ")] = self.config_testhub.jwt
        os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩჀ")] = self.config_testhub.build_hashed_id
    def bstack1lll11l1ll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1llll1l1lll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll111l111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll111l111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll11l1ll1_opy_(event_name=EVENTS.bstack1llll111ll1_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1ll1lllll1l_opy_(self, bstack1ll1llll1ll_opy_=10):
        if self.bstack1llll1l1lll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡴࡢࡴࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠢჁ"))
            return True
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧჂ"))
        if os.getenv(bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡉࡓ࡜ࠢჃ")) == bstack1ll1ll111l1_opy_:
            self.cli_bin_session_id = bstack1ll1ll111l1_opy_
            self.cli_listen_addr = bstack11ll11_opy_ (u"ࠣࡷࡱ࡭ࡽࡀ࠯ࡵ࡯ࡳ࠳ࡸࡪ࡫࠮ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࠩࡸ࠴ࡳࡰࡥ࡮ࠦჄ") % (self.cli_bin_session_id)
            self.bstack1llll1l1lll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1111l1l_opy_, bstack11ll11_opy_ (u"ࠤࡶࡨࡰࠨჅ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll11l1lll_opy_ compat for text=True in bstack1lll111llll_opy_ python
            encoding=bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ჆"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1ll11lll_opy_ = threading.Thread(target=self.__1llll11llll_opy_, args=(bstack1ll1llll1ll_opy_,))
        bstack1ll1ll11lll_opy_.start()
        bstack1ll1ll11lll_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡷࡵࡧࡷ࡯࠼ࠣࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࢁࠥࡵࡵࡵ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡶࡸࡩࡵࡵࡵ࠰ࡵࡩࡦࡪࠨࠪࡿࠣࡩࡷࡸ࠽ࠣჇ") + str(self.process.stderr.read()) + bstack11ll11_opy_ (u"ࠧࠨ჈"))
        if not self.bstack1llll1l1lll_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡛ࠣ჉") + str(id(self)) + bstack11ll11_opy_ (u"ࠢ࡞ࠢࡦࡰࡪࡧ࡮ࡶࡲࠥ჊"))
            self.__1lll1ll1lll_opy_()
        self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡱࡴࡲࡧࡪࡹࡳࡠࡴࡨࡥࡩࡿ࠺ࠡࠤ჋") + str(self.bstack1llll1l1lll_opy_) + bstack11ll11_opy_ (u"ࠤࠥ჌"))
        return self.bstack1llll1l1lll_opy_
    def __1llll11llll_opy_(self, bstack1ll1ll11111_opy_=10):
        bstack1lll11l11l1_opy_ = time.time()
        while self.process and time.time() - bstack1lll11l11l1_opy_ < bstack1ll1ll11111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11ll11_opy_ (u"ࠥ࡭ࡩࡃࠢჍ") in line:
                    self.cli_bin_session_id = line.split(bstack11ll11_opy_ (u"ࠦ࡮ࡪ࠽ࠣ჎"))[-1:][0].strip()
                    self.logger.debug(bstack11ll11_opy_ (u"ࠧࡩ࡬ࡪࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦ࠽ࠦ჏") + str(self.cli_bin_session_id) + bstack11ll11_opy_ (u"ࠨࠢა"))
                    continue
                if bstack11ll11_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣბ") in line:
                    self.cli_listen_addr = line.split(bstack11ll11_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤგ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll11_opy_ (u"ࠤࡦࡰ࡮ࡥ࡬ࡪࡵࡷࡩࡳࡥࡡࡥࡦࡵ࠾ࠧდ") + str(self.cli_listen_addr) + bstack11ll11_opy_ (u"ࠥࠦე"))
                    continue
                if bstack11ll11_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥვ") in line:
                    port = line.split(bstack11ll11_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦზ"))[-1:][0].strip()
                    self.logger.debug(bstack11ll11_opy_ (u"ࠨࡰࡰࡴࡷ࠾ࠧთ") + str(port) + bstack11ll11_opy_ (u"ࠢࠣი"))
                    continue
                if line.strip() == bstack1ll1lll1l11_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11ll11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡊࡑࡢࡗ࡙ࡘࡅࡂࡏࠥკ"), bstack11ll11_opy_ (u"ࠤ࠴ࠦლ")) == bstack11ll11_opy_ (u"ࠥ࠵ࠧმ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1llll1l1lll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡪࡸࡲࡰࡴ࠽ࠤࠧნ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨო"))
        return False
    @measure(event_name=EVENTS.bstack1lll11l111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def __1lll1ll1lll_opy_(self):
        if self.bstack1lll11ll11l_opy_:
            self.bstack111111l1ll_opy_.stop()
            start = datetime.now()
            if self.bstack1lll1lll111_opy_():
                self.cli_bin_session_id = None
                if self.bstack1ll1ll1ll1l_opy_:
                    self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥპ"), datetime.now() - start)
                else:
                    self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦჟ"), datetime.now() - start)
            self.__1llll1ll11l_opy_()
            start = datetime.now()
            self.bstack1lll11ll11l_opy_.close()
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥრ"), datetime.now() - start)
            self.bstack1lll11ll11l_opy_ = None
        if self.process:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡸࡴࡶࠢს"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠥ࡯࡮ࡲ࡬ࡠࡶ࡬ࡱࡪࠨტ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll111l1l1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1ll11l11l_opy_()
                self.logger.info(
                    bstack11ll11_opy_ (u"࡛ࠦ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠢუ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫფ")] = self.config_testhub.build_hashed_id
        self.bstack1llll1l1lll_opy_ = False
    def __1lll1l1llll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11ll11_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣქ")] = selenium.__version__
            data.frameworks.append(bstack11ll11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤღ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧყ")] = __version__
            data.frameworks.append(bstack11ll11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨშ"))
        except:
            pass
    def bstack1ll1lll11l1_opy_(self, hub_url: str, platform_index: int, bstack1ll11111l_opy_: Any):
        if self.bstack1lllll1lll1_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢჩ"))
            return
        try:
            bstack1ll1lll1ll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨც")
            self.bstack1lllll1lll1_opy_ = bstack1llll11l111_opy_(
                cli.config.get(bstack11ll11_opy_ (u"ࠧ࡮ࡵࡣࡗࡵࡰࠧძ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll111l11l_opy_={bstack11ll11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥწ"): bstack1ll11111l_opy_}
            )
            def bstack1lll1l11l11_opy_(self):
                return
            if self.config.get(bstack11ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤჭ"), True):
                Service.start = bstack1lll1l11l11_opy_
                Service.stop = bstack1lll1l11l11_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11111lll1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll11ll1ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤხ"), datetime.now() - bstack1ll1lll1ll_opy_)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣჯ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦჰ"))
    def bstack1ll1lll1ll1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l1lllll1_opy_
            self.bstack1lllll1lll1_opy_ = bstack1lll1lll1l1_opy_(
                platform_index,
                framework_name=bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣჱ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࠨჲ") + str(e) + bstack11ll11_opy_ (u"ࠨࠢჳ"))
            pass
    def bstack1ll1lll111l_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤჴ"))
            return
        if bstack111ll11l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣჵ"): pytest.__version__ }, [bstack11ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨჶ")], self.bstack111111l1ll_opy_, self.bstack1llll1l1l11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lll1lllll1_opy_({ bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥჷ"): pytest.__version__ }, [bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦჸ")], self.bstack111111l1ll_opy_, self.bstack1llll1l1l11_opy_)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤჹ") + str(e) + bstack11ll11_opy_ (u"ࠨࠢჺ"))
        self.bstack1lll11l1l1l_opy_()
    def bstack1lll11l1l1l_opy_(self):
        if not self.bstack1l111lll1l_opy_():
            return
        bstack1lll11ll1_opy_ = None
        def bstack1ll1l11l_opy_(config, startdir):
            return bstack11ll11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧ჻").format(bstack11ll11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢჼ"))
        def bstack11ll1ll1l1_opy_():
            return
        def bstack111l1l11_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11ll11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩჽ"):
                return bstack11ll11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤჾ")
            else:
                return bstack1lll11ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1lll11ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1ll1l11l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1ll1l1_opy_
            Config.getoption = bstack111l1l11_opy_
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨჿ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨᄀ"))
    def bstack1llll1l11l1_opy_(self):
        bstack1ll111lll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll111lll_opy_, dict):
            if cli.config_observability:
                bstack1ll111lll_opy_.update(
                    {bstack11ll11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᄁ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11ll11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥᄂ") in accessibility.get(bstack11ll11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᄃ"), {}):
                    bstack1ll1llll1l1_opy_ = accessibility.get(bstack11ll11_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᄄ"))
                    bstack1ll1llll1l1_opy_.update({ bstack11ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦᄅ"): bstack1ll1llll1l1_opy_.pop(bstack11ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢᄆ")) })
                bstack1ll111lll_opy_.update({bstack11ll11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᄇ"): accessibility })
        return bstack1ll111lll_opy_
    @measure(event_name=EVENTS.bstack1lll111ll11_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1lll1lll111_opy_(self, bstack1lll1l1ll11_opy_: str = None, bstack1ll1ll1ll11_opy_: str = None, bstack11lll111l_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll1l1l11_opy_:
            return
        bstack1ll1lll1ll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack11lll111l_opy_:
            req.bstack11lll111l_opy_ = bstack11lll111l_opy_
        if bstack1lll1l1ll11_opy_:
            req.bstack1lll1l1ll11_opy_ = bstack1lll1l1ll11_opy_
        if bstack1ll1ll1ll11_opy_:
            req.bstack1ll1ll1ll11_opy_ = bstack1ll1ll1ll11_opy_
        try:
            r = self.bstack1llll1l1l11_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺ࡯ࡱࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᄈ"), datetime.now() - bstack1ll1lll1ll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll1l1l1l1_opy_(self, key: str, value: timedelta):
        tag = bstack11ll11_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᄉ") if self.bstack1l11111lll_opy_() else bstack11ll11_opy_ (u"ࠣ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᄊ")
        self.bstack1llll11l1ll_opy_[bstack11ll11_opy_ (u"ࠤ࠽ࠦᄋ").join([tag + bstack11ll11_opy_ (u"ࠥ࠱ࠧᄌ") + str(id(self)), key])] += value
    def bstack1ll11l11l_opy_(self):
        if not os.getenv(bstack11ll11_opy_ (u"ࠦࡉࡋࡂࡖࡉࡢࡔࡊࡘࡆࠣᄍ"), bstack11ll11_opy_ (u"ࠧ࠶ࠢᄎ")) == bstack11ll11_opy_ (u"ࠨ࠱ࠣᄏ"):
            return
        bstack1lll1l1ll1l_opy_ = dict()
        bstack1lllllll111_opy_ = []
        if self.test_framework:
            bstack1lllllll111_opy_.extend(list(self.test_framework.bstack1lllllll111_opy_.values()))
        if self.bstack1lllll1lll1_opy_:
            bstack1lllllll111_opy_.extend(list(self.bstack1lllll1lll1_opy_.bstack1lllllll111_opy_.values()))
        for instance in bstack1lllllll111_opy_:
            if not instance.platform_index in bstack1lll1l1ll1l_opy_:
                bstack1lll1l1ll1l_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll1l1ll1l_opy_[instance.platform_index]
            for k, v in instance.bstack1lll1l11lll_opy_().items():
                report[k] += v
                report[k.split(bstack11ll11_opy_ (u"ࠢ࠻ࠤᄐ"))[0]] += v
        bstack1lll1llll1l_opy_ = sorted([(k, v) for k, v in self.bstack1llll11l1ll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1lll1l1l_opy_ = 0
        for r in bstack1lll1llll1l_opy_:
            bstack1lll1ll11ll_opy_ = r[1].total_seconds()
            bstack1ll1lll1l1l_opy_ += bstack1lll1ll11ll_opy_
            self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࢁࡲ࡜࠲ࡠࢁࡂࠨᄑ") + str(bstack1lll1ll11ll_opy_) + bstack11ll11_opy_ (u"ࠤࠥᄒ"))
        self.logger.debug(bstack11ll11_opy_ (u"ࠥ࠱࠲ࠨᄓ"))
        bstack1llll111l1l_opy_ = []
        for platform_index, report in bstack1lll1l1ll1l_opy_.items():
            bstack1llll111l1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1llll111l1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11lllll1_opy_ = set()
        bstack1lll1l111l1_opy_ = 0
        for r in bstack1llll111l1l_opy_:
            bstack1lll1ll11ll_opy_ = r[2].total_seconds()
            bstack1lll1l111l1_opy_ += bstack1lll1ll11ll_opy_
            bstack11lllll1_opy_.add(r[0])
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࢀࡸ࡛࠱࡟ࢀ࠾ࢀࡸ࡛࠲࡟ࢀࡁࠧᄔ") + str(bstack1lll1ll11ll_opy_) + bstack11ll11_opy_ (u"ࠧࠨᄕ"))
        if self.bstack1l11111lll_opy_():
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࠭࠮ࠤᄖ"))
            self.logger.debug(bstack11ll11_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࢀࡺ࡯ࡵࡣ࡯ࡣࡨࡲࡩࡾࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ࠰ࡿࡸࡺࡲࠩࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠭ࢂࡃࠢᄗ") + str(bstack1lll1l111l1_opy_) + bstack11ll11_opy_ (u"ࠣࠤᄘ"))
        else:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࠨᄙ") + str(bstack1ll1lll1l1l_opy_) + bstack11ll11_opy_ (u"ࠥࠦᄚ"))
        self.logger.debug(bstack11ll11_opy_ (u"ࠦ࠲࠳ࠢᄛ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1llll1l1l11_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡩ࡬ࡪࡡࡶࡩࡷࡼࡩࡤࡧࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᄜ"))
            return None
        response = self.bstack1llll1l1l11_opy_.TestOrchestration(request)
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷ࠱ࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲࡂࢁࡽࠣᄝ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1lll1111_opy_(self, r):
        if r is not None and getattr(r, bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࠨᄞ"), None) and getattr(r.testhub, bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᄟ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᄠ")))
            for bstack1ll1ll1lll1_opy_, err in errors.items():
                if err[bstack11ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨᄡ")] == bstack11ll11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᄢ"):
                    self.logger.info(err[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄣ")])
                else:
                    self.logger.error(err[bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄤ")])
    def bstack11l1l1ll1_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()