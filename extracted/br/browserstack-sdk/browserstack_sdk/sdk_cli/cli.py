# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack11111lll11_opy_ import bstack11111ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1lll111l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1ll1lll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1ll11_opy_ import bstack1lll1ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11lll_opy_ import bstack1lllll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l1l1_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l111l_opy_ import bstack1ll1llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11ll_opy_ import bstack1l1ll11ll_opy_, bstack11ll1l111_opy_, bstack11ll1111l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1lllll11l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1111111l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llllll1_opy_ import bstack1llll11lll1_opy_
from bstack_utils.helper import Notset, bstack1lll11l11l1_opy_, get_cli_dir, bstack1lll1lll11l_opy_, bstack111ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll1lll1_opy_ import bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll111_opy_ import bstack1lllllll1l_opy_
from bstack_utils.helper import Notset, bstack1lll11l11l1_opy_, get_cli_dir, bstack1lll1lll11l_opy_, bstack111ll111_opy_, bstack1l1ll1l111_opy_, bstack1l1ll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11lllll_opy_, bstack1lll1111l1l_opy_, bstack1lllll1111l_opy_, bstack1lll11111l1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1llllll111l_opy_, bstack1111111111_opy_, bstack11111l1ll1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l111l1_opy_ import bstack11l1l111_opy_
from bstack_utils import bstack1111ll111_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l11ll1l1_opy_, bstack1l1lllll1l_opy_
logger = bstack1111ll111_opy_.get_logger(__name__, bstack1111ll111_opy_.bstack1lllll1l11l_opy_())
def bstack1lll11ll111_opy_(bs_config):
    bstack1lll1l1l1l1_opy_ = None
    bstack1lll111l1l1_opy_ = None
    try:
        bstack1lll111l1l1_opy_ = get_cli_dir()
        bstack1lll1l1l1l1_opy_ = bstack1lll1lll11l_opy_(bstack1lll111l1l1_opy_)
        bstack1llll1lll11_opy_ = bstack1lll11l11l1_opy_(bstack1lll1l1l1l1_opy_, bstack1lll111l1l1_opy_, bs_config)
        bstack1lll1l1l1l1_opy_ = bstack1llll1lll11_opy_ if bstack1llll1lll11_opy_ else bstack1lll1l1l1l1_opy_
        if not bstack1lll1l1l1l1_opy_:
            raise ValueError(bstack111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦၚ"))
    except Exception as ex:
        logger.debug(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦၛ").format(ex))
        bstack1lll1l1l1l1_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧၜ"))
        if bstack1lll1l1l1l1_opy_:
            logger.debug(bstack111lll_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨၝ") + str(bstack1lll1l1l1l1_opy_) + bstack111lll_opy_ (u"ࠦࠧၞ"))
        else:
            logger.debug(bstack111lll_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣၟ"))
    return bstack1lll1l1l1l1_opy_, bstack1lll111l1l1_opy_
bstack1lll1l11111_opy_ = bstack111lll_opy_ (u"ࠨ࠹࠺࠻࠼ࠦၠ")
bstack1llll1l1l1l_opy_ = bstack111lll_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨၡ")
bstack1lll1ll1lll_opy_ = bstack111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧၢ")
bstack1lll1ll1l1l_opy_ = bstack111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢၣ")
bstack111lll111_opy_ = bstack111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨၤ")
bstack1llll111111_opy_ = re.compile(bstack111lll_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥၥ"))
bstack1lll11ll11l_opy_ = bstack111lll_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥၦ")
bstack1lll1l1l1ll_opy_ = [
    bstack11ll1l111_opy_.bstack111ll1lll_opy_,
    bstack11ll1l111_opy_.CONNECT,
    bstack11ll1l111_opy_.bstack11l1l1l11_opy_,
]
class SDKCLI:
    _1lll1lll1l1_opy_ = None
    process: Union[None, Any]
    bstack1lllll11ll1_opy_: bool
    bstack1lll11l1l11_opy_: bool
    bstack1lll1l1l111_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1llll11l111_opy_: Union[None, grpc.Channel]
    bstack1lll111l11l_opy_: str
    test_framework: TestFramework
    bstack1llllll1111_opy_: bstack1111111l11_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll1ll1ll1_opy_: bstack1ll1llll11l_opy_
    accessibility: bstack1lll111l111_opy_
    bstack1ll1ll111_opy_: bstack1lllllll1l_opy_
    ai: bstack1ll1lll1ll1_opy_
    bstack1llll1111l1_opy_: bstack1lll1ll111l_opy_
    bstack1ll1lllll11_opy_: List[bstack1lll1l11ll1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1llll1l111l_opy_: Any
    bstack1lll1l1l11l_opy_: Dict[str, timedelta]
    bstack1lll1l1ll1l_opy_: str
    bstack11111lll11_opy_: bstack11111ll11l_opy_
    def __new__(cls):
        if not cls._1lll1lll1l1_opy_:
            cls._1lll1lll1l1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll1lll1l1_opy_
    def __init__(self):
        self.process = None
        self.bstack1lllll11ll1_opy_ = False
        self.bstack1llll11l111_opy_ = None
        self.bstack1lll1ll1l11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll1ll1l1l_opy_, None)
        self.bstack1lll11l11ll_opy_ = os.environ.get(bstack1lll1ll1lll_opy_, bstack111lll_opy_ (u"ࠨࠢၧ")) == bstack111lll_opy_ (u"ࠢࠣၨ")
        self.bstack1lll11l1l11_opy_ = False
        self.bstack1lll1l1l111_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1llll1l111l_opy_ = None
        self.test_framework = None
        self.bstack1llllll1111_opy_ = None
        self.bstack1lll111l11l_opy_=bstack111lll_opy_ (u"ࠣࠤၩ")
        self.session_framework = None
        self.logger = bstack1111ll111_opy_.get_logger(self.__class__.__name__, bstack1111ll111_opy_.bstack1lllll1l11l_opy_())
        self.bstack1lll1l1l11l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack11111lll11_opy_ = bstack11111ll11l_opy_()
        self.bstack1ll1ll1llll_opy_ = None
        self.bstack1lll1llllll_opy_ = None
        self.bstack1lll1ll1ll1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1lllll11_opy_ = []
    def bstack1l1l111l1_opy_(self):
        return os.environ.get(bstack111lll111_opy_).lower().__eq__(bstack111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢၪ"))
    def is_enabled(self, config):
        if bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧၫ") in config and str(config[bstack111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨၬ")]).lower() != bstack111lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫၭ"):
            return False
        bstack1lll111llll_opy_ = [bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨၮ"), bstack111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦၯ")]
        bstack1lll11ll1ll_opy_ = config.get(bstack111lll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦၰ")) in bstack1lll111llll_opy_ or os.environ.get(bstack111lll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪၱ")) in bstack1lll111llll_opy_
        os.environ[bstack111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨၲ")] = str(bstack1lll11ll1ll_opy_) # bstack1ll1lllllll_opy_ bstack1llll11ll1l_opy_ VAR to bstack1ll1ll1l1ll_opy_ is binary running
        return bstack1lll11ll1ll_opy_
    def bstack1ll1l1l11l_opy_(self):
        for event in bstack1lll1l1l1ll_opy_:
            bstack1l1ll11ll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l1ll11ll_opy_.logger.debug(bstack111lll_opy_ (u"ࠦࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠣࡁࡃࠦࡻࡢࡴࡪࡷࢂࠦࠢၳ") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨၴ"))
            )
        bstack1l1ll11ll_opy_.register(bstack11ll1l111_opy_.bstack111ll1lll_opy_, self.__1ll1lll1l1l_opy_)
        bstack1l1ll11ll_opy_.register(bstack11ll1l111_opy_.CONNECT, self.__1llll11llll_opy_)
        bstack1l1ll11ll_opy_.register(bstack11ll1l111_opy_.bstack11l1l1l11_opy_, self.__1lllll11111_opy_)
        bstack1l1ll11ll_opy_.register(bstack11ll1l111_opy_.bstack1l111l1l11_opy_, self.__1ll1llll1l1_opy_)
    def bstack11l11l111l_opy_(self):
        return not self.bstack1lll11l11ll_opy_ and os.environ.get(bstack1lll1ll1lll_opy_, bstack111lll_opy_ (u"ࠨࠢၵ")) != bstack111lll_opy_ (u"ࠢࠣၶ")
    def is_running(self):
        if self.bstack1lll11l11ll_opy_:
            return self.bstack1lllll11ll1_opy_
        else:
            return bool(self.bstack1llll11l111_opy_)
    def bstack1llll111l11_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1lllll11_opy_) and cli.is_running()
    def __1llll1l11l1_opy_(self, bstack1lll11l1lll_opy_=10):
        if self.bstack1lll1ll1l11_opy_:
            return
        bstack11ll1ll1_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll1ll1l1l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack111lll_opy_ (u"ࠣ࡝ࠥၷ") + str(id(self)) + bstack111lll_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣၸ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack111lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧၹ"), 0), (bstack111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢၺ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll11l1lll_opy_)
        self.bstack1llll11l111_opy_ = channel
        self.bstack1lll1ll1l11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1llll11l111_opy_)
        self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦၻ"), datetime.now() - bstack11ll1ll1_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll1ll1l1l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack111lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨၼ") + str(self.bstack11l11l111l_opy_()) + bstack111lll_opy_ (u"ࠢࠣၽ"))
    def __1lllll11111_opy_(self, event_name):
        if self.bstack11l11l111l_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣၾ"))
        self.__1lll1lll111_opy_()
    def __1ll1llll1l1_opy_(self, event_name, bstack1lll11ll1l1_opy_ = None, bstack1l1l1l1111_opy_=1):
        if bstack1l1l1l1111_opy_ == 1:
            self.logger.error(bstack111lll_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤၿ"))
        bstack1llll1ll11l_opy_ = Path(bstack1lllll111l1_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦႀ"))
        if self.bstack1lll111l1l1_opy_ and bstack1llll1ll11l_opy_.exists():
            with open(bstack1llll1ll11l_opy_, bstack111lll_opy_ (u"ࠫࡷ࠭ႁ"), encoding=bstack111lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫႂ")) as fp:
                data = json.load(fp)
                try:
                    bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"࠭ࡐࡐࡕࡗࠫႃ"), bstack11l1l111_opy_(bstack11lll11ll1_opy_), data, {
                        bstack111lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬႄ"): (self.config[bstack111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪႅ")], self.config[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬႆ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1lllll1l_opy_.format(str(e)))
            bstack1llll1ll11l_opy_.unlink()
        sys.exit(bstack1l1l1l1111_opy_)
    @measure(event_name=EVENTS.bstack1lll1l111l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1ll1lll1l1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
        self.bstack1lll111l11l_opy_, self.bstack1lll111l1l1_opy_ = bstack1lll11ll111_opy_(data.bs_config)
        os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨႇ")] = self.bstack1lll111l1l1_opy_
        if not self.bstack1lll111l11l_opy_ or not self.bstack1lll111l1l1_opy_:
            raise ValueError(bstack111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥႈ"))
        if self.bstack11l11l111l_opy_():
            self.__1llll11llll_opy_(event_name, bstack11ll1111l_opy_())
            return
        try:
            bstack1llll1l1l11_opy_.end(EVENTS.bstack1l1ll1llll_opy_.value, EVENTS.bstack1l1ll1llll_opy_.value + bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧႉ"), EVENTS.bstack1l1ll1llll_opy_.value + bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦႊ"), status=True, failure=None, test_name=None)
            logger.debug(bstack111lll_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨႋ"))
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧႌ").format(e))
        start = datetime.now()
        is_started = self.__1lll11lll11_opy_()
        self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨႍ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1llll1l11l1_opy_()
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤႎ"), datetime.now() - start)
            start = datetime.now()
            self.__1lll1111ll1_opy_(data)
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤႏ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll1l11l11_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1llll11llll_opy_(self, event_name: str, data: bstack11ll1111l_opy_):
        if not self.bstack11l11l111l_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤ႐"))
            return
        bin_session_id = os.environ.get(bstack1lll1ll1lll_opy_)
        start = datetime.now()
        self.__1llll1l11l1_opy_()
        self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧ႑"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack111lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨ႒") + str(bin_session_id) + bstack111lll_opy_ (u"ࠣࠤ႓"))
        start = datetime.now()
        self.__1llll1l1lll_opy_()
        self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢ႔"), datetime.now() - start)
    def __1lll111l1ll_opy_(self):
        if not self.bstack1lll1ll1l11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack111lll_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢ႕"))
            return
        bstack1lll1l1llll_opy_ = {
            bstack111lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ႖"): (bstack1llll1ll1ll_opy_, bstack1lll1lllll1_opy_, bstack1llll11lll1_opy_),
            bstack111lll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢ႗"): (bstack1lllll111ll_opy_, bstack1lll1ll1111_opy_, bstack1llll111lll_opy_),
        }
        if not self.bstack1ll1ll1llll_opy_ and self.session_framework in bstack1lll1l1llll_opy_:
            bstack1llll111l1l_opy_, bstack1ll1ll1ll1l_opy_, bstack1llll1lll1l_opy_ = bstack1lll1l1llll_opy_[self.session_framework]
            bstack1llll1l1111_opy_ = bstack1ll1ll1ll1l_opy_()
            self.bstack1lll1llllll_opy_ = bstack1llll1l1111_opy_
            self.bstack1ll1ll1llll_opy_ = bstack1llll1lll1l_opy_
            self.bstack1ll1lllll11_opy_.append(bstack1llll1l1111_opy_)
            self.bstack1ll1lllll11_opy_.append(bstack1llll111l1l_opy_(self.bstack1lll1llllll_opy_))
        if not self.bstack1lll1ll1ll1_opy_ and self.config_observability and self.config_observability.success: # bstack1lll1l11l1l_opy_
            self.bstack1lll1ll1ll1_opy_ = bstack1ll1llll11l_opy_(self.bstack1ll1ll1llll_opy_, self.bstack1lll1llllll_opy_) # bstack1ll1lll11ll_opy_
            self.bstack1ll1lllll11_opy_.append(self.bstack1lll1ll1ll1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll111l111_opy_(self.bstack1ll1ll1llll_opy_, self.bstack1lll1llllll_opy_)
            self.bstack1ll1lllll11_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack111lll_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣ႘"), False) == True:
            self.ai = bstack1ll1lll1ll1_opy_()
            self.bstack1ll1lllll11_opy_.append(self.ai)
        if not self.percy and self.bstack1llll1l111l_opy_ and self.bstack1llll1l111l_opy_.success:
            self.percy = bstack1lll1ll111l_opy_(self.bstack1llll1l111l_opy_)
            self.bstack1ll1lllll11_opy_.append(self.percy)
        for mod in self.bstack1ll1lllll11_opy_:
            if not mod.bstack1lll1l11lll_opy_():
                mod.configure(self.bstack1lll1ll1l11_opy_, self.config, self.cli_bin_session_id, self.bstack11111lll11_opy_)
    def __1lll1111lll_opy_(self):
        for mod in self.bstack1ll1lllll11_opy_:
            if mod.bstack1lll1l11lll_opy_():
                mod.configure(self.bstack1lll1ll1l11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll11111ll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1lll1111ll1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll11l1l11_opy_:
            return
        self.__1lllll11l11_opy_(data)
        bstack11ll1ll1_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack111lll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ႙")
        req.sdk_language = bstack111lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣႚ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1llll111111_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack111lll_opy_ (u"ࠤ࡞ࠦႛ") + str(id(self)) + bstack111lll_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႜ"))
            r = self.bstack1lll1ll1l11_opy_.StartBinSession(req)
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨႝ"), datetime.now() - bstack11ll1ll1_opy_)
            os.environ[bstack1lll1ll1lll_opy_] = r.bin_session_id
            self.__1llll1111ll_opy_(r)
            self.__1lll111l1ll_opy_()
            self.bstack11111lll11_opy_.start()
            self.bstack1lll11l1l11_opy_ = True
            self.logger.debug(bstack111lll_opy_ (u"ࠧࡡࠢ႞") + str(id(self)) + bstack111lll_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦ႟"))
        except grpc.bstack1llll1lllll_opy_ as bstack1llll11l11l_opy_:
            self.logger.error(bstack111lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤႠ") + str(bstack1llll11l11l_opy_) + bstack111lll_opy_ (u"ࠣࠤႡ"))
            traceback.print_exc()
            raise bstack1llll11l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨႢ") + str(e) + bstack111lll_opy_ (u"ࠥࠦႣ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1111111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1llll1l1lll_opy_(self):
        if not self.bstack11l11l111l_opy_() or not self.cli_bin_session_id or self.bstack1lll1l1l111_opy_:
            return
        bstack11ll1ll1_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫႤ"), bstack111lll_opy_ (u"ࠬ࠶ࠧႥ")))
        try:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡛ࠣႦ") + str(id(self)) + bstack111lll_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤႧ"))
            r = self.bstack1lll1ll1l11_opy_.ConnectBinSession(req)
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧႨ"), datetime.now() - bstack11ll1ll1_opy_)
            self.__1llll1111ll_opy_(r)
            self.__1lll111l1ll_opy_()
            self.bstack11111lll11_opy_.start()
            self.bstack1lll1l1l111_opy_ = True
            self.logger.debug(bstack111lll_opy_ (u"ࠤ࡞ࠦႩ") + str(id(self)) + bstack111lll_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤႪ"))
        except grpc.bstack1llll1lllll_opy_ as bstack1llll11l11l_opy_:
            self.logger.error(bstack111lll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨႫ") + str(bstack1llll11l11l_opy_) + bstack111lll_opy_ (u"ࠧࠨႬ"))
            traceback.print_exc()
            raise bstack1llll11l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥႭ") + str(e) + bstack111lll_opy_ (u"ࠢࠣႮ"))
            traceback.print_exc()
            raise e
    def __1llll1111ll_opy_(self, r):
        self.bstack1lllll1l111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack111lll_opy_ (u"ࠣࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢႯ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack111lll_opy_ (u"ࠤࡨࡱࡵࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡹࡳࡪࠢႰ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡧࡵࡧࡾࠦࡩࡴࠢࡶࡩࡳࡺࠠࡰࡰ࡯ࡽࠥࡧࡳࠡࡲࡤࡶࡹࠦ࡯ࡧࠢࡷ࡬ࡪࠦࠢࡄࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠰ࠧࠦࡡ࡯ࡦࠣࡸ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡡ࡭ࡵࡲࠤࡺࡹࡥࡥࠢࡥࡽ࡙ࠥࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡪࡸࡥࡧࡱࡵࡩ࠱ࠦࡎࡰࡰࡨࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡩࡴࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧႱ")
        self.bstack1llll1l111l_opy_ = getattr(r, bstack111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪႲ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩႳ")] = self.config_testhub.jwt
        os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫႴ")] = self.config_testhub.build_hashed_id
    def bstack1lll1ll11ll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lllll11ll1_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llll11111l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llll11111l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1ll11ll_opy_(event_name=EVENTS.bstack1ll1lll1lll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1lll11lll11_opy_(self, bstack1lll11l1lll_opy_=10):
        if self.bstack1lllll11ll1_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤႵ"))
            return True
        self.logger.debug(bstack111lll_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢႶ"))
        if os.getenv(bstack111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤႷ")) == bstack1lll11ll11l_opy_:
            self.cli_bin_session_id = bstack1lll11ll11l_opy_
            self.cli_listen_addr = bstack111lll_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨႸ") % (self.cli_bin_session_id)
            self.bstack1lllll11ll1_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll111l11l_opy_, bstack111lll_opy_ (u"ࠦࡸࡪ࡫ࠣႹ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll1l1ll11_opy_ compat for text=True in bstack1lll111111l_opy_ python
            encoding=bstack111lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦႺ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll111lll1_opy_ = threading.Thread(target=self.__1ll1lllll1l_opy_, args=(bstack1lll11l1lll_opy_,))
        bstack1lll111lll1_opy_.start()
        bstack1lll111lll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥႻ") + str(self.process.stderr.read()) + bstack111lll_opy_ (u"ࠢࠣႼ"))
        if not self.bstack1lllll11ll1_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠣ࡝ࠥႽ") + str(id(self)) + bstack111lll_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧႾ"))
            self.__1lll1lll111_opy_()
        self.logger.debug(bstack111lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦႿ") + str(self.bstack1lllll11ll1_opy_) + bstack111lll_opy_ (u"ࠦࠧჀ"))
        return self.bstack1lllll11ll1_opy_
    def __1ll1lllll1l_opy_(self, bstack1ll1llll111_opy_=10):
        bstack1llll1l11ll_opy_ = time.time()
        while self.process and time.time() - bstack1llll1l11ll_opy_ < bstack1ll1llll111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack111lll_opy_ (u"ࠧ࡯ࡤ࠾ࠤჁ") in line:
                    self.cli_bin_session_id = line.split(bstack111lll_opy_ (u"ࠨࡩࡥ࠿ࠥჂ"))[-1:][0].strip()
                    self.logger.debug(bstack111lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨჃ") + str(self.cli_bin_session_id) + bstack111lll_opy_ (u"ࠣࠤჄ"))
                    continue
                if bstack111lll_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥჅ") in line:
                    self.cli_listen_addr = line.split(bstack111lll_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦ჆"))[-1:][0].strip()
                    self.logger.debug(bstack111lll_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢჇ") + str(self.cli_listen_addr) + bstack111lll_opy_ (u"ࠧࠨ჈"))
                    continue
                if bstack111lll_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧ჉") in line:
                    port = line.split(bstack111lll_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨ჊"))[-1:][0].strip()
                    self.logger.debug(bstack111lll_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢ჋") + str(port) + bstack111lll_opy_ (u"ࠤࠥ჌"))
                    continue
                if line.strip() == bstack1llll1l1l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack111lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧჍ"), bstack111lll_opy_ (u"ࠦ࠶ࠨ჎")) == bstack111lll_opy_ (u"ࠧ࠷ࠢ჏"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lllll11ll1_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack111lll_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢა") + str(e) + bstack111lll_opy_ (u"ࠢࠣბ"))
        return False
    @measure(event_name=EVENTS.bstack1lll11l1ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def __1lll1lll111_opy_(self):
        if self.bstack1llll11l111_opy_:
            self.bstack11111lll11_opy_.stop()
            start = datetime.now()
            if self.bstack1lll1llll1l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll1l1l111_opy_:
                    self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧგ"), datetime.now() - start)
                else:
                    self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨდ"), datetime.now() - start)
            self.__1lll1111lll_opy_()
            start = datetime.now()
            self.bstack1llll11l111_opy_.close()
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧე"), datetime.now() - start)
            self.bstack1llll11l111_opy_ = None
        if self.process:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡸࡺ࡯ࡱࠤვ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣზ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll11l11ll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11l1llll1l_opy_()
                self.logger.info(
                    bstack111lll_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤთ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack111lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ი")] = self.config_testhub.build_hashed_id
        self.bstack1lllll11ll1_opy_ = False
    def __1lllll11l11_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack111lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥკ")] = selenium.__version__
            data.frameworks.append(bstack111lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦლ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack111lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢმ")] = __version__
            data.frameworks.append(bstack111lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣნ"))
        except:
            pass
    def bstack1llll11ll11_opy_(self, hub_url: str, platform_index: int, bstack1ll11l1l11_opy_: Any):
        if self.bstack1llllll1111_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤო"))
            return
        try:
            bstack11ll1ll1_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack111lll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣპ")
            self.bstack1llllll1111_opy_ = bstack1llll111lll_opy_(
                cli.config.get(bstack111lll_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢჟ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1llll1l1ll1_opy_={bstack111lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧრ"): bstack1ll11l1l11_opy_}
            )
            def bstack1lll1l1lll1_opy_(self):
                return
            if self.config.get(bstack111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦს"), True):
                Service.start = bstack1lll1l1lll1_opy_
                Service.stop = bstack1lll1l1lll1_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1lllllll1l_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1llll1ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦტ"), datetime.now() - bstack11ll1ll1_opy_)
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥუ") + str(e) + bstack111lll_opy_ (u"ࠧࠨფ"))
    def bstack1ll1lll1111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1ll1lll11_opy_
            self.bstack1llllll1111_opy_ = bstack1llll11lll1_opy_(
                platform_index,
                framework_name=bstack111lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥქ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣღ") + str(e) + bstack111lll_opy_ (u"ࠣࠤყ"))
            pass
    def bstack1lll1l111ll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦშ"))
            return
        if bstack111ll111_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥჩ"): pytest.__version__ }, [bstack111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣც")], self.bstack11111lll11_opy_, self.bstack1lll1ll1l11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lllll11l1l_opy_({ bstack111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧძ"): pytest.__version__ }, [bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨწ")], self.bstack11111lll11_opy_, self.bstack1lll1ll1l11_opy_)
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦჭ") + str(e) + bstack111lll_opy_ (u"ࠣࠤხ"))
        self.bstack1lll1lll1ll_opy_()
    def bstack1lll1lll1ll_opy_(self):
        if not self.bstack1l1l111l1_opy_():
            return
        bstack1ll1l11ll1_opy_ = None
        def bstack1l1ll1ll1l_opy_(config, startdir):
            return bstack111lll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢჯ").format(bstack111lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤჰ"))
        def bstack11ll1lllll_opy_():
            return
        def bstack1l1lllll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack111lll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫჱ"):
                return bstack111lll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦჲ")
            else:
                return bstack1ll1l11ll1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll1l11ll1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l1ll1ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1lllll_opy_
            Config.getoption = bstack1l1lllll_opy_
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣჳ") + str(e) + bstack111lll_opy_ (u"ࠢࠣჴ"))
    def bstack1lll11l1l1l_opy_(self):
        bstack1111l1ll1_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1111l1ll1_opy_, dict):
            if cli.config_observability:
                bstack1111l1ll1_opy_.update(
                    {bstack111lll_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣჵ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack111lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧჶ") in accessibility.get(bstack111lll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦჷ"), {}):
                    bstack1lll1ll11l1_opy_ = accessibility.get(bstack111lll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧჸ"))
                    bstack1lll1ll11l1_opy_.update({ bstack111lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨჹ"): bstack1lll1ll11l1_opy_.pop(bstack111lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤჺ")) })
                bstack1111l1ll1_opy_.update({bstack111lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ჻"): accessibility })
        return bstack1111l1ll1_opy_
    @measure(event_name=EVENTS.bstack1ll1lll111l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1lll1llll1l_opy_(self, bstack1llll1ll111_opy_: str = None, bstack1lll111ll11_opy_: str = None, bstack1l1l1l1111_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll1ll1l11_opy_:
            return
        bstack11ll1ll1_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1l1l1l1111_opy_:
            req.bstack1l1l1l1111_opy_ = bstack1l1l1l1111_opy_
        if bstack1llll1ll111_opy_:
            req.bstack1llll1ll111_opy_ = bstack1llll1ll111_opy_
        if bstack1lll111ll11_opy_:
            req.bstack1lll111ll11_opy_ = bstack1lll111ll11_opy_
        try:
            r = self.bstack1lll1ll1l11_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჼ"), datetime.now() - bstack11ll1ll1_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1lllll1l1l_opy_(self, key: str, value: timedelta):
        tag = bstack111lll_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤჽ") if self.bstack11l11l111l_opy_() else bstack111lll_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤჾ")
        self.bstack1lll1l1l11l_opy_[bstack111lll_opy_ (u"ࠦ࠿ࠨჿ").join([tag + bstack111lll_opy_ (u"ࠧ࠳ࠢᄀ") + str(id(self)), key])] += value
    def bstack11l1llll1l_opy_(self):
        if not os.getenv(bstack111lll_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥᄁ"), bstack111lll_opy_ (u"ࠢ࠱ࠤᄂ")) == bstack111lll_opy_ (u"ࠣ࠳ࠥᄃ"):
            return
        bstack1llll11l1ll_opy_ = dict()
        bstack1lllll1ll11_opy_ = []
        if self.test_framework:
            bstack1lllll1ll11_opy_.extend(list(self.test_framework.bstack1lllll1ll11_opy_.values()))
        if self.bstack1llllll1111_opy_:
            bstack1lllll1ll11_opy_.extend(list(self.bstack1llllll1111_opy_.bstack1lllll1ll11_opy_.values()))
        for instance in bstack1lllll1ll11_opy_:
            if not instance.platform_index in bstack1llll11l1ll_opy_:
                bstack1llll11l1ll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1llll11l1ll_opy_[instance.platform_index]
            for k, v in instance.bstack1llll1llll1_opy_().items():
                report[k] += v
                report[k.split(bstack111lll_opy_ (u"ࠤ࠽ࠦᄄ"))[0]] += v
        bstack1lll1llll11_opy_ = sorted([(k, v) for k, v in self.bstack1lll1l1l11l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll11lll1l_opy_ = 0
        for r in bstack1lll1llll11_opy_:
            bstack1lll1l1111l_opy_ = r[1].total_seconds()
            bstack1lll11lll1l_opy_ += bstack1lll1l1111l_opy_
            self.logger.debug(bstack111lll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣᄅ") + str(bstack1lll1l1111l_opy_) + bstack111lll_opy_ (u"ࠦࠧᄆ"))
        self.logger.debug(bstack111lll_opy_ (u"ࠧ࠳࠭ࠣᄇ"))
        bstack1lll111ll1l_opy_ = []
        for platform_index, report in bstack1llll11l1ll_opy_.items():
            bstack1lll111ll1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll111ll1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11ll1l1lll_opy_ = set()
        bstack1lll1111l11_opy_ = 0
        for r in bstack1lll111ll1l_opy_:
            bstack1lll1l1111l_opy_ = r[2].total_seconds()
            bstack1lll1111l11_opy_ += bstack1lll1l1111l_opy_
            bstack11ll1l1lll_opy_.add(r[0])
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢᄈ") + str(bstack1lll1l1111l_opy_) + bstack111lll_opy_ (u"ࠢࠣᄉ"))
        if self.bstack11l11l111l_opy_():
            self.logger.debug(bstack111lll_opy_ (u"ࠣ࠯࠰ࠦᄊ"))
            self.logger.debug(bstack111lll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤᄋ") + str(bstack1lll1111l11_opy_) + bstack111lll_opy_ (u"ࠥࠦᄌ"))
        else:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᄍ") + str(bstack1lll11lll1l_opy_) + bstack111lll_opy_ (u"ࠧࠨᄎ"))
        self.logger.debug(bstack111lll_opy_ (u"ࠨ࠭࠮ࠤᄏ"))
    def bstack1lllll1l111_opy_(self, r):
        if r is not None and getattr(r, bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࠨᄐ"), None) and getattr(r.testhub, bstack111lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᄑ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack111lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᄒ")))
            for bstack1lll11llll1_opy_, err in errors.items():
                if err[bstack111lll_opy_ (u"ࠪࡸࡾࡶࡥࠨᄓ")] == bstack111lll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᄔ"):
                    self.logger.info(err[bstack111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᄕ")])
                else:
                    self.logger.error(err[bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᄖ")])
    def bstack11111llll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()