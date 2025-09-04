# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll11_opy_ import bstack1lll111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1l1_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11111_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1lll1111111_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l1l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1ll1ll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l111_opy_ import bstack1lll11111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack11lllll1ll_opy_ import bstack11lllll1ll_opy_, bstack1l111l1111_opy_, bstack11l11l11l1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llllllll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1ll1lll1lll_opy_
from bstack_utils.helper import Notset, bstack1ll1l1lll1l_opy_, get_cli_dir, bstack1ll1l1l1lll_opy_, bstack1ll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1l11l_opy_ import bstack1ll1lll11l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll11_opy_ import bstack1llllllll_opy_
from bstack_utils.helper import Notset, bstack1ll1l1lll1l_opy_, get_cli_dir, bstack1ll1l1l1lll_opy_, bstack1ll1l1l1l1_opy_, bstack1ll111l111_opy_, bstack11llll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lllll1_opy_, bstack1lll1l1ll1l_opy_, bstack1ll1llll1ll_opy_, bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llllllll1l_opy_, bstack1lllll11111_opy_, bstack1llll1lllll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1llll111ll_opy_ import bstack11l11l11_opy_
from bstack_utils import bstack11l1111l1_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11lllllll_opy_, bstack11lllll111_opy_
logger = bstack11l1111l1_opy_.get_logger(__name__, bstack11l1111l1_opy_.bstack1lll11llll1_opy_())
def bstack1llll111111_opy_(bs_config):
    bstack1llll111lll_opy_ = None
    bstack1lll11l1l11_opy_ = None
    try:
        bstack1lll11l1l11_opy_ = get_cli_dir()
        bstack1llll111lll_opy_ = bstack1ll1l1l1lll_opy_(bstack1lll11l1l11_opy_)
        bstack1lll1ll1lll_opy_ = bstack1ll1l1lll1l_opy_(bstack1llll111lll_opy_, bstack1lll11l1l11_opy_, bs_config)
        bstack1llll111lll_opy_ = bstack1lll1ll1lll_opy_ if bstack1lll1ll1lll_opy_ else bstack1llll111lll_opy_
        if not bstack1llll111lll_opy_:
            raise ValueError(bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤႬ"))
    except Exception as ex:
        logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡬ࡢࡶࡨࡷࡹࠦࡢࡪࡰࡤࡶࡾࠦࡻࡾࠤႭ").format(ex))
        bstack1llll111lll_opy_ = os.environ.get(bstack1111l1l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥႮ"))
        if bstack1llll111lll_opy_:
            logger.debug(bstack1111l1l_opy_ (u"ࠣࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡳࡱࡰࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࠦႯ") + str(bstack1llll111lll_opy_) + bstack1111l1l_opy_ (u"ࠤࠥႰ"))
        else:
            logger.debug(bstack1111l1l_opy_ (u"ࠥࡒࡴࠦࡶࡢ࡮࡬ࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠼ࠢࡶࡩࡹࡻࡰࠡ࡯ࡤࡽࠥࡨࡥࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨႱ"))
    return bstack1llll111lll_opy_, bstack1lll11l1l11_opy_
bstack1ll1ll11lll_opy_ = bstack1111l1l_opy_ (u"ࠦ࠾࠿࠹࠺ࠤႲ")
bstack1lll1lll11l_opy_ = bstack1111l1l_opy_ (u"ࠧࡸࡥࡢࡦࡼࠦႳ")
bstack1ll1l1ll111_opy_ = bstack1111l1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥႴ")
bstack1ll1l1l1l1l_opy_ = bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡍࡋࡖࡘࡊࡔ࡟ࡂࡆࡇࡖࠧႵ")
bstack11111l11l_opy_ = bstack1111l1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦႶ")
bstack1ll1llllll1_opy_ = re.compile(bstack1111l1l_opy_ (u"ࡴࠥࠬࡄ࡯ࠩ࠯ࠬࠫࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡾࡅࡗ࠮࠴ࠪࠣႷ"))
bstack1lll11ll1l1_opy_ = bstack1111l1l_opy_ (u"ࠥࡨࡪࡼࡥ࡭ࡱࡳࡱࡪࡴࡴࠣႸ")
bstack1lll1111l1l_opy_ = [
    bstack1l111l1111_opy_.bstack11l11ll1ll_opy_,
    bstack1l111l1111_opy_.CONNECT,
    bstack1l111l1111_opy_.bstack1l11111ll1_opy_,
]
class SDKCLI:
    _1lll11l11l1_opy_ = None
    process: Union[None, Any]
    bstack1lll1l1ll11_opy_: bool
    bstack1lll11ll111_opy_: bool
    bstack1lll11lllll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll1lll1ll_opy_: Union[None, grpc.Channel]
    bstack1ll1ll1ll11_opy_: str
    test_framework: TestFramework
    bstack1lllll1ll1l_opy_: bstack1llllllll11_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll11l11ll_opy_: bstack1lll1l11lll_opy_
    accessibility: bstack1lll111ll1l_opy_
    bstack1l1l1ll11_opy_: bstack1llllllll_opy_
    ai: bstack1lll1lll1l1_opy_
    bstack1ll1llll1l1_opy_: bstack1llll1l11l1_opy_
    bstack1ll1ll1l111_opy_: List[bstack1lll1lll111_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1ll111l_opy_: Any
    bstack1llll111l11_opy_: Dict[str, timedelta]
    bstack1lll11l1ll1_opy_: str
    bstack1111111ll1_opy_: bstack1111111lll_opy_
    def __new__(cls):
        if not cls._1lll11l11l1_opy_:
            cls._1lll11l11l1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll11l11l1_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1l1ll11_opy_ = False
        self.bstack1lll1lll1ll_opy_ = None
        self.bstack1ll1ll11l11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1l1l1l1l_opy_, None)
        self.bstack1lll1l1l1ll_opy_ = os.environ.get(bstack1ll1l1ll111_opy_, bstack1111l1l_opy_ (u"ࠦࠧႹ")) == bstack1111l1l_opy_ (u"ࠧࠨႺ")
        self.bstack1lll11ll111_opy_ = False
        self.bstack1lll11lllll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1ll111l_opy_ = None
        self.test_framework = None
        self.bstack1lllll1ll1l_opy_ = None
        self.bstack1ll1ll1ll11_opy_=bstack1111l1l_opy_ (u"ࠨࠢႻ")
        self.session_framework = None
        self.logger = bstack11l1111l1_opy_.get_logger(self.__class__.__name__, bstack11l1111l1_opy_.bstack1lll11llll1_opy_())
        self.bstack1llll111l11_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111111ll1_opy_ = bstack1111111lll_opy_()
        self.bstack1ll1l1l1l11_opy_ = None
        self.bstack1lll1l11111_opy_ = None
        self.bstack1lll11l11ll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1ll1l111_opy_ = []
    def bstack111l1l11_opy_(self):
        return os.environ.get(bstack11111l11l_opy_).lower().__eq__(bstack1111l1l_opy_ (u"ࠢࡵࡴࡸࡩࠧႼ"))
    def is_enabled(self, config):
        if bstack1111l1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬႽ") in config and str(config[bstack1111l1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Ⴞ")]).lower() != bstack1111l1l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩႿ"):
            return False
        bstack1lll1ll11l1_opy_ = [bstack1111l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦჀ"), bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤჁ")]
        bstack1ll1l1l11ll_opy_ = config.get(bstack1111l1l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤჂ")) in bstack1lll1ll11l1_opy_ or os.environ.get(bstack1111l1l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨჃ")) in bstack1lll1ll11l1_opy_
        os.environ[bstack1111l1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦჄ")] = str(bstack1ll1l1l11ll_opy_) # bstack1ll1ll1lll1_opy_ bstack1ll1l1ll11l_opy_ VAR to bstack1lll1l1l1l1_opy_ is binary running
        return bstack1ll1l1l11ll_opy_
    def bstack1lllll11l1_opy_(self):
        for event in bstack1lll1111l1l_opy_:
            bstack11lllll1ll_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11lllll1ll_opy_.logger.debug(bstack1111l1l_opy_ (u"ࠤࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠡ࠿ࡁࠤࢀࡧࡲࡨࡵࢀࠤࠧჅ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠥࠦ჆"))
            )
        bstack11lllll1ll_opy_.register(bstack1l111l1111_opy_.bstack11l11ll1ll_opy_, self.__1ll1ll1111l_opy_)
        bstack11lllll1ll_opy_.register(bstack1l111l1111_opy_.CONNECT, self.__1ll1ll111l1_opy_)
        bstack11lllll1ll_opy_.register(bstack1l111l1111_opy_.bstack1l11111ll1_opy_, self.__1ll1ll1llll_opy_)
        bstack11lllll1ll_opy_.register(bstack1l111l1111_opy_.bstack1l11111l_opy_, self.__1ll1lllll1l_opy_)
    def bstack111llll1l1_opy_(self):
        return not self.bstack1lll1l1l1ll_opy_ and os.environ.get(bstack1ll1l1ll111_opy_, bstack1111l1l_opy_ (u"ࠦࠧჇ")) != bstack1111l1l_opy_ (u"ࠧࠨ჈")
    def is_running(self):
        if self.bstack1lll1l1l1ll_opy_:
            return self.bstack1lll1l1ll11_opy_
        else:
            return bool(self.bstack1lll1lll1ll_opy_)
    def bstack1llll111ll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1ll1l111_opy_) and cli.is_running()
    def __1ll1l1llll1_opy_(self, bstack1ll1ll11ll1_opy_=10):
        if self.bstack1ll1ll11l11_opy_:
            return
        bstack1ll1l1lll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1l1l1l1l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡛ࠣ჉") + str(id(self)) + bstack1111l1l_opy_ (u"ࠢ࡞ࠢࡦࡳࡳࡴࡥࡤࡶ࡬ࡲ࡬ࠨ჊"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1111l1l_opy_ (u"ࠣࡩࡵࡴࡨ࠴ࡥ࡯ࡣࡥࡰࡪࡥࡨࡵࡶࡳࡣࡵࡸ࡯ࡹࡻࠥ჋"), 0), (bstack1111l1l_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡸࡥࡰࡳࡱࡻࡽࠧ჌"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll1ll11ll1_opy_)
        self.bstack1lll1lll1ll_opy_ = channel
        self.bstack1ll1ll11l11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll1lll1ll_opy_)
        self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࠤჍ"), datetime.now() - bstack1ll1l1lll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1l1l1l1l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࡀࠠࡪࡵࡢࡧ࡭࡯࡬ࡥࡡࡳࡶࡴࡩࡥࡴࡵࡀࠦ჎") + str(self.bstack111llll1l1_opy_()) + bstack1111l1l_opy_ (u"ࠧࠨ჏"))
    def __1ll1ll1llll_opy_(self, event_name):
        if self.bstack111llll1l1_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡴࡶࡲࡴࡵ࡯࡮ࡨࠢࡆࡐࡎࠨა"))
        self.__1lll111111l_opy_()
    def __1ll1lllll1l_opy_(self, event_name, bstack1lll1llll1l_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1111l1l_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠢბ"))
        bstack1ll1lllll11_opy_ = Path(bstack1lll11lll1l_opy_ (u"ࠣࡽࡶࡩࡱ࡬࠮ࡤ࡮࡬ࡣࡩ࡯ࡲࡾ࠱ࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࡶ࠲࡯ࡹ࡯࡯ࠤგ"))
        if self.bstack1lll11l1l11_opy_ and bstack1ll1lllll11_opy_.exists():
            with open(bstack1ll1lllll11_opy_, bstack1111l1l_opy_ (u"ࠩࡵࠫდ"), encoding=bstack1111l1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩე")) as fp:
                data = json.load(fp)
                try:
                    bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠫࡕࡕࡓࡕࠩვ"), bstack11l11l11_opy_(bstack1ll11lllll_opy_), data, {
                        bstack1111l1l_opy_ (u"ࠬࡧࡵࡵࡪࠪზ"): (self.config[bstack1111l1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨთ")], self.config[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪი")])
                    })
                except Exception as e:
                    logger.debug(bstack11lllll111_opy_.format(str(e)))
            bstack1ll1lllll11_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll1ll1l11l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1ll1ll1111l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
        self.bstack1ll1ll1ll11_opy_, self.bstack1lll11l1l11_opy_ = bstack1llll111111_opy_(data.bs_config)
        os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡘࡔࡌࡘࡆࡈࡌࡆࡡࡇࡍࡗ࠭კ")] = self.bstack1lll11l1l11_opy_
        if not self.bstack1ll1ll1ll11_opy_ or not self.bstack1lll11l1l11_opy_:
            raise ValueError(bstack1111l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠣლ"))
        if self.bstack111llll1l1_opy_():
            self.__1ll1ll111l1_opy_(event_name, bstack11l11l11l1_opy_())
            return
        try:
            bstack1lll11111ll_opy_.end(EVENTS.bstack1l111l111_opy_.value, EVENTS.bstack1l111l111_opy_.value + bstack1111l1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥმ"), EVENTS.bstack1l111l111_opy_.value + bstack1111l1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤნ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1111l1l_opy_ (u"ࠧࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡔࡆࡎࠤࡘ࡫ࡴࡶࡲ࠱ࠦო"))
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥპ").format(e))
        start = datetime.now()
        is_started = self.__1ll1lll1l11_opy_()
        self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠢࡴࡲࡤࡻࡳࡥࡴࡪ࡯ࡨࠦჟ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1l1llll1_opy_()
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢრ"), datetime.now() - start)
            start = datetime.now()
            self.__1lll1l11l11_opy_(data)
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢს"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1llll11l1ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1ll1ll111l1_opy_(self, event_name: str, data: bstack11l11l11l1_opy_):
        if not self.bstack111llll1l1_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࡰࡲࡸࠥࡧࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢტ"))
            return
        bin_session_id = os.environ.get(bstack1ll1l1ll111_opy_)
        start = datetime.now()
        self.__1ll1l1llll1_opy_()
        self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥუ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡃࡍࡋࠣࠦფ") + str(bin_session_id) + bstack1111l1l_opy_ (u"ࠨࠢქ"))
        start = datetime.now()
        self.__1ll1lllllll_opy_()
        self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧღ"), datetime.now() - start)
    def __1lll1ll11ll_opy_(self):
        if not self.bstack1ll1ll11l11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡥࡤࡲࡳࡵࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡲࡵࡤࡶ࡮ࡨࡷࠧყ"))
            return
        bstack1lll1ll1111_opy_ = {
            bstack1111l1l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨშ"): (bstack1ll1ll111ll_opy_, bstack1lll11111l1_opy_, bstack1ll1lll1lll_opy_),
            bstack1111l1l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧჩ"): (bstack1lll1111111_opy_, bstack1llll11lll1_opy_, bstack1lll1l111ll_opy_),
        }
        if not self.bstack1ll1l1l1l11_opy_ and self.session_framework in bstack1lll1ll1111_opy_:
            bstack1lll1llllll_opy_, bstack1llll11llll_opy_, bstack1lll1111lll_opy_ = bstack1lll1ll1111_opy_[self.session_framework]
            bstack1ll1lll1111_opy_ = bstack1llll11llll_opy_()
            self.bstack1lll1l11111_opy_ = bstack1ll1lll1111_opy_
            self.bstack1ll1l1l1l11_opy_ = bstack1lll1111lll_opy_
            self.bstack1ll1ll1l111_opy_.append(bstack1ll1lll1111_opy_)
            self.bstack1ll1ll1l111_opy_.append(bstack1lll1llllll_opy_(self.bstack1lll1l11111_opy_))
        if not self.bstack1lll11l11ll_opy_ and self.config_observability and self.config_observability.success: # bstack1llll11l111_opy_
            self.bstack1lll11l11ll_opy_ = bstack1lll1l11lll_opy_(self.bstack1ll1l1l1l11_opy_, self.bstack1lll1l11111_opy_) # bstack1llll11ll1l_opy_
            self.bstack1ll1ll1l111_opy_.append(self.bstack1lll11l11ll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll111ll1l_opy_(self.bstack1ll1l1l1l11_opy_, self.bstack1lll1l11111_opy_)
            self.bstack1ll1ll1l111_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1111l1l_opy_ (u"ࠦࡸ࡫࡬ࡧࡊࡨࡥࡱࠨც"), False) == True:
            self.ai = bstack1lll1lll1l1_opy_()
            self.bstack1ll1ll1l111_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1ll111l_opy_ and self.bstack1lll1ll111l_opy_.success:
            self.percy = bstack1llll1l11l1_opy_(self.bstack1lll1ll111l_opy_)
            self.bstack1ll1ll1l111_opy_.append(self.percy)
        for mod in self.bstack1ll1ll1l111_opy_:
            if not mod.bstack1lll1ll1ll1_opy_():
                mod.configure(self.bstack1ll1ll11l11_opy_, self.config, self.cli_bin_session_id, self.bstack1111111ll1_opy_)
    def __1lll1l1111l_opy_(self):
        for mod in self.bstack1ll1ll1l111_opy_:
            if mod.bstack1lll1ll1ll1_opy_():
                mod.configure(self.bstack1ll1ll11l11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll11ll1ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1lll1l11l11_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll11ll111_opy_:
            return
        self.__1lll111ll11_opy_(data)
        bstack1ll1l1lll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧძ")
        req.sdk_language = bstack1111l1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨწ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll1llllll1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢ࡜ࠤჭ") + str(id(self)) + bstack1111l1l_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢხ"))
            r = self.bstack1ll1ll11l11_opy_.StartBinSession(req)
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦჯ"), datetime.now() - bstack1ll1l1lll_opy_)
            os.environ[bstack1ll1l1ll111_opy_] = r.bin_session_id
            self.__1lll11l1lll_opy_(r)
            self.__1lll1ll11ll_opy_()
            self.bstack1111111ll1_opy_.start()
            self.bstack1lll11ll111_opy_ = True
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥ࡟ࠧჰ") + str(id(self)) + bstack1111l1l_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤჱ"))
        except grpc.bstack1lll1l1lll1_opy_ as bstack1ll1lll11ll_opy_:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢჲ") + str(bstack1ll1lll11ll_opy_) + bstack1111l1l_opy_ (u"ࠨࠢჳ"))
            traceback.print_exc()
            raise bstack1ll1lll11ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦჴ") + str(e) + bstack1111l1l_opy_ (u"ࠣࠤჵ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1l11ll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1ll1lllllll_opy_(self):
        if not self.bstack111llll1l1_opy_() or not self.cli_bin_session_id or self.bstack1lll11lllll_opy_:
            return
        bstack1ll1l1lll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩჶ"), bstack1111l1l_opy_ (u"ࠪ࠴ࠬჷ")))
        try:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡠࠨჸ") + str(id(self)) + bstack1111l1l_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢჹ"))
            r = self.bstack1ll1ll11l11_opy_.ConnectBinSession(req)
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥჺ"), datetime.now() - bstack1ll1l1lll_opy_)
            self.__1lll11l1lll_opy_(r)
            self.__1lll1ll11ll_opy_()
            self.bstack1111111ll1_opy_.start()
            self.bstack1lll11lllll_opy_ = True
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢ࡜ࠤ჻") + str(id(self)) + bstack1111l1l_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢჼ"))
        except grpc.bstack1lll1l1lll1_opy_ as bstack1ll1lll11ll_opy_:
            self.logger.error(bstack1111l1l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦჽ") + str(bstack1ll1lll11ll_opy_) + bstack1111l1l_opy_ (u"ࠥࠦჾ"))
            traceback.print_exc()
            raise bstack1ll1lll11ll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣჿ") + str(e) + bstack1111l1l_opy_ (u"ࠧࠨᄀ"))
            traceback.print_exc()
            raise e
    def __1lll11l1lll_opy_(self, r):
        self.bstack1llll1l111l_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1111l1l_opy_ (u"ࠨࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧᄁ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1111l1l_opy_ (u"ࠢࡦ࡯ࡳࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡷࡱࡨࠧᄂ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1111l1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡥࡳࡥࡼࠤ࡮ࡹࠠࡴࡧࡱࡸࠥࡵ࡮࡭ࡻࠣࡥࡸࠦࡰࡢࡴࡷࠤࡴ࡬ࠠࡵࡪࡨࠤࠧࡉ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠮ࠥࠤࡦࡴࡤࠡࡶ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡦࡲࡳࡰࠢࡸࡷࡪࡪࠠࡣࡻࠣࡗࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡨࡶࡪ࡬࡯ࡳࡧ࠯ࠤࡓࡵ࡮ࡦࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤ࡮ࡹࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᄃ")
        self.bstack1lll1ll111l_opy_ = getattr(r, bstack1111l1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᄄ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᄅ")] = self.config_testhub.jwt
        os.environ[bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᄆ")] = self.config_testhub.build_hashed_id
    def bstack1ll1l1l1ll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll1l1ll11_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llll1111ll_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llll1111ll_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll1l1l1ll1_opy_(event_name=EVENTS.bstack1lll1111l11_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1ll1lll1l11_opy_(self, bstack1ll1ll11ll1_opy_=10):
        if self.bstack1lll1l1ll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡹࡴࡢࡴࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠢᄇ"))
            return True
        self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᄈ"))
        if os.getenv(bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡉࡓ࡜ࠢᄉ")) == bstack1lll11ll1l1_opy_:
            self.cli_bin_session_id = bstack1lll11ll1l1_opy_
            self.cli_listen_addr = bstack1111l1l_opy_ (u"ࠣࡷࡱ࡭ࡽࡀ࠯ࡵ࡯ࡳ࠳ࡸࡪ࡫࠮ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࠩࡸ࠴ࡳࡰࡥ࡮ࠦᄊ") % (self.cli_bin_session_id)
            self.bstack1lll1l1ll11_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1ll1ll1ll11_opy_, bstack1111l1l_opy_ (u"ࠤࡶࡨࡰࠨᄋ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1llll111_opy_ compat for text=True in bstack1ll1ll1ll1l_opy_ python
            encoding=bstack1111l1l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᄌ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll1l1l111_opy_ = threading.Thread(target=self.__1lll1ll1l1l_opy_, args=(bstack1ll1ll11ll1_opy_,))
        bstack1lll1l1l111_opy_.start()
        bstack1lll1l1l111_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡷࡵࡧࡷ࡯࠼ࠣࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࢁࠥࡵࡵࡵ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡶࡸࡩࡵࡵࡵ࠰ࡵࡩࡦࡪࠨࠪࡿࠣࡩࡷࡸ࠽ࠣᄍ") + str(self.process.stderr.read()) + bstack1111l1l_opy_ (u"ࠧࠨᄎ"))
        if not self.bstack1lll1l1ll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡛ࠣᄏ") + str(id(self)) + bstack1111l1l_opy_ (u"ࠢ࡞ࠢࡦࡰࡪࡧ࡮ࡶࡲࠥᄐ"))
            self.__1lll111111l_opy_()
        self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡱࡴࡲࡧࡪࡹࡳࡠࡴࡨࡥࡩࡿ࠺ࠡࠤᄑ") + str(self.bstack1lll1l1ll11_opy_) + bstack1111l1l_opy_ (u"ࠤࠥᄒ"))
        return self.bstack1lll1l1ll11_opy_
    def __1lll1ll1l1l_opy_(self, bstack1ll1l1l11l1_opy_=10):
        bstack1llll1111l1_opy_ = time.time()
        while self.process and time.time() - bstack1llll1111l1_opy_ < bstack1ll1l1l11l1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1111l1l_opy_ (u"ࠥ࡭ࡩࡃࠢᄓ") in line:
                    self.cli_bin_session_id = line.split(bstack1111l1l_opy_ (u"ࠦ࡮ࡪ࠽ࠣᄔ"))[-1:][0].strip()
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡪࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦ࠽ࠦᄕ") + str(self.cli_bin_session_id) + bstack1111l1l_opy_ (u"ࠨࠢᄖ"))
                    continue
                if bstack1111l1l_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣᄗ") in line:
                    self.cli_listen_addr = line.split(bstack1111l1l_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᄘ"))[-1:][0].strip()
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡦࡰ࡮ࡥ࡬ࡪࡵࡷࡩࡳࡥࡡࡥࡦࡵ࠾ࠧᄙ") + str(self.cli_listen_addr) + bstack1111l1l_opy_ (u"ࠥࠦᄚ"))
                    continue
                if bstack1111l1l_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥᄛ") in line:
                    port = line.split(bstack1111l1l_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᄜ"))[-1:][0].strip()
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡰࡰࡴࡷ࠾ࠧᄝ") + str(port) + bstack1111l1l_opy_ (u"ࠢࠣᄞ"))
                    continue
                if line.strip() == bstack1lll1lll11l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1111l1l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡊࡑࡢࡗ࡙ࡘࡅࡂࡏࠥᄟ"), bstack1111l1l_opy_ (u"ࠤ࠴ࠦᄠ")) == bstack1111l1l_opy_ (u"ࠥ࠵ࠧᄡ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1l1ll11_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡪࡸࡲࡰࡴ࠽ࠤࠧᄢ") + str(e) + bstack1111l1l_opy_ (u"ࠧࠨᄣ"))
        return False
    @measure(event_name=EVENTS.bstack1llll1l1111_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def __1lll111111l_opy_(self):
        if self.bstack1lll1lll1ll_opy_:
            self.bstack1111111ll1_opy_.stop()
            start = datetime.now()
            if self.bstack1lll11lll11_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll11lllll_opy_:
                    self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᄤ"), datetime.now() - start)
                else:
                    self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᄥ"), datetime.now() - start)
            self.__1lll1l1111l_opy_()
            start = datetime.now()
            self.bstack1lll1lll1ll_opy_.close()
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥᄦ"), datetime.now() - start)
            self.bstack1lll1lll1ll_opy_ = None
        if self.process:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡶࡸࡴࡶࠢᄧ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥ࡯࡮ࡲ࡬ࡠࡶ࡬ࡱࡪࠨᄨ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll1l1l1ll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11lll1l111_opy_()
                self.logger.info(
                    bstack1111l1l_opy_ (u"࡛ࠦ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠦᄩ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᄪ")] = self.config_testhub.build_hashed_id
        self.bstack1lll1l1ll11_opy_ = False
    def __1lll111ll11_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1111l1l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᄫ")] = selenium.__version__
            data.frameworks.append(bstack1111l1l_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᄬ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᄭ")] = __version__
            data.frameworks.append(bstack1111l1l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᄮ"))
        except:
            pass
    def bstack1lll11l1111_opy_(self, hub_url: str, platform_index: int, bstack1l1l1l1l1l_opy_: Any):
        if self.bstack1lllll1ll1l_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢᄯ"))
            return
        try:
            bstack1ll1l1lll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1111l1l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᄰ")
            self.bstack1lllll1ll1l_opy_ = bstack1lll1l111ll_opy_(
                cli.config.get(bstack1111l1l_opy_ (u"ࠧ࡮ࡵࡣࡗࡵࡰࠧᄱ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll1l11l1l_opy_={bstack1111l1l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᄲ"): bstack1l1l1l1l1l_opy_}
            )
            def bstack1llll11l11l_opy_(self):
                return
            if self.config.get(bstack1111l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠤᄳ"), True):
                Service.start = bstack1llll11l11l_opy_
                Service.stop = bstack1llll11l11l_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1llllllll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1lll11l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᄴ"), datetime.now() - bstack1ll1l1lll_opy_)
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࠣᄵ") + str(e) + bstack1111l1l_opy_ (u"ࠥࠦᄶ"))
    def bstack1lll1111ll1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1llll1lll1_opy_
            self.bstack1lllll1ll1l_opy_ = bstack1ll1lll1lll_opy_(
                platform_index,
                framework_name=bstack1111l1l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᄷ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠾ࠥࠨᄸ") + str(e) + bstack1111l1l_opy_ (u"ࠨࠢᄹ"))
            pass
    def bstack1ll1lll1ll1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᄺ"))
            return
        if bstack1ll1l1l1l1_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᄻ"): pytest.__version__ }, [bstack1111l1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᄼ")], self.bstack1111111ll1_opy_, self.bstack1ll1ll11l11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lll111llll_opy_({ bstack1111l1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᄽ"): pytest.__version__ }, [bstack1111l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᄾ")], self.bstack1111111ll1_opy_, self.bstack1ll1ll11l11_opy_)
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡻࡷࡩࡸࡺ࠺ࠡࠤᄿ") + str(e) + bstack1111l1l_opy_ (u"ࠨࠢᅀ"))
        self.bstack1lll111lll1_opy_()
    def bstack1lll111lll1_opy_(self):
        if not self.bstack111l1l11_opy_():
            return
        bstack11lll111l1_opy_ = None
        def bstack1111l1lll_opy_(config, startdir):
            return bstack1111l1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧᅁ").format(bstack1111l1l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᅂ"))
        def bstack111ll1l1_opy_():
            return
        def bstack11l11llll1_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1111l1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩᅃ"):
                return bstack1111l1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᅄ")
            else:
                return bstack11lll111l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11lll111l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1111l1lll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll1l1_opy_
            Config.getoption = bstack11l11llll1_opy_
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡷࡧ࡭ࠦࡰࡺࡶࡨࡷࡹࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡨࡲࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠾ࠥࠨᅅ") + str(e) + bstack1111l1l_opy_ (u"ࠧࠨᅆ"))
    def bstack1ll1lll1l1l_opy_(self):
        bstack11ll11ll11_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11ll11ll11_opy_, dict):
            if cli.config_observability:
                bstack11ll11ll11_opy_.update(
                    {bstack1111l1l_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᅇ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1111l1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥᅈ") in accessibility.get(bstack1111l1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᅉ"), {}):
                    bstack1lll11ll11l_opy_ = accessibility.get(bstack1111l1l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᅊ"))
                    bstack1lll11ll11l_opy_.update({ bstack1111l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠦᅋ"): bstack1lll11ll11l_opy_.pop(bstack1111l1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࡥࡴࡰࡡࡺࡶࡦࡶࠢᅌ")) })
                bstack11ll11ll11_opy_.update({bstack1111l1l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᅍ"): accessibility })
        return bstack11ll11ll11_opy_
    @measure(event_name=EVENTS.bstack1lll111l1l1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1lll11lll11_opy_(self, bstack1lll11l1l1l_opy_: str = None, bstack1llll11ll11_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1ll11l11_opy_:
            return
        bstack1ll1l1lll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1lll11l1l1l_opy_:
            req.bstack1lll11l1l1l_opy_ = bstack1lll11l1l1l_opy_
        if bstack1llll11ll11_opy_:
            req.bstack1llll11ll11_opy_ = bstack1llll11ll11_opy_
        try:
            r = self.bstack1ll1ll11l11_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺ࡯ࡱࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᅎ"), datetime.now() - bstack1ll1l1lll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11l11lll_opy_(self, key: str, value: timedelta):
        tag = bstack1111l1l_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᅏ") if self.bstack111llll1l1_opy_() else bstack1111l1l_opy_ (u"ࠣ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹࠢᅐ")
        self.bstack1llll111l11_opy_[bstack1111l1l_opy_ (u"ࠤ࠽ࠦᅑ").join([tag + bstack1111l1l_opy_ (u"ࠥ࠱ࠧᅒ") + str(id(self)), key])] += value
    def bstack11lll1l111_opy_(self):
        if not os.getenv(bstack1111l1l_opy_ (u"ࠦࡉࡋࡂࡖࡉࡢࡔࡊࡘࡆࠣᅓ"), bstack1111l1l_opy_ (u"ࠧ࠶ࠢᅔ")) == bstack1111l1l_opy_ (u"ࠨ࠱ࠣᅕ"):
            return
        bstack1lll1ll1l11_opy_ = dict()
        bstack1111111111_opy_ = []
        if self.test_framework:
            bstack1111111111_opy_.extend(list(self.test_framework.bstack1111111111_opy_.values()))
        if self.bstack1lllll1ll1l_opy_:
            bstack1111111111_opy_.extend(list(self.bstack1lllll1ll1l_opy_.bstack1111111111_opy_.values()))
        for instance in bstack1111111111_opy_:
            if not instance.platform_index in bstack1lll1ll1l11_opy_:
                bstack1lll1ll1l11_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll1ll1l11_opy_[instance.platform_index]
            for k, v in instance.bstack1llll11l1l1_opy_().items():
                report[k] += v
                report[k.split(bstack1111l1l_opy_ (u"ࠢ࠻ࠤᅖ"))[0]] += v
        bstack1lll11l111l_opy_ = sorted([(k, v) for k, v in self.bstack1llll111l11_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1lll111l_opy_ = 0
        for r in bstack1lll11l111l_opy_:
            bstack1ll1ll1l1l1_opy_ = r[1].total_seconds()
            bstack1ll1lll111l_opy_ += bstack1ll1ll1l1l1_opy_
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࢁࡲ࡜࠲ࡠࢁࡂࠨᅗ") + str(bstack1ll1ll1l1l1_opy_) + bstack1111l1l_opy_ (u"ࠤࠥᅘ"))
        self.logger.debug(bstack1111l1l_opy_ (u"ࠥ࠱࠲ࠨᅙ"))
        bstack1lll111l1ll_opy_ = []
        for platform_index, report in bstack1lll1ll1l11_opy_.items():
            bstack1lll111l1ll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll111l1ll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1lllll1l1l_opy_ = set()
        bstack1llll11111l_opy_ = 0
        for r in bstack1lll111l1ll_opy_:
            bstack1ll1ll1l1l1_opy_ = r[2].total_seconds()
            bstack1llll11111l_opy_ += bstack1ll1ll1l1l1_opy_
            bstack1lllll1l1l_opy_.add(r[0])
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࢀࡸ࡛࠱࡟ࢀ࠾ࢀࡸ࡛࠲࡟ࢀࡁࠧᅚ") + str(bstack1ll1ll1l1l1_opy_) + bstack1111l1l_opy_ (u"ࠧࠨᅛ"))
        if self.bstack111llll1l1_opy_():
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࠭࠮ࠤᅜ"))
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࢀࡺ࡯ࡵࡣ࡯ࡣࡨࡲࡩࡾࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ࠰ࡿࡸࡺࡲࠩࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠭ࢂࡃࠢᅝ") + str(bstack1llll11111l_opy_) + bstack1111l1l_opy_ (u"ࠣࠤᅞ"))
        else:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࠨᅟ") + str(bstack1ll1lll111l_opy_) + bstack1111l1l_opy_ (u"ࠥࠦᅠ"))
        self.logger.debug(bstack1111l1l_opy_ (u"ࠦ࠲࠳ࠢᅡ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1ll1ll11l11_opy_:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡩ࡬ࡪࡡࡶࡩࡷࡼࡩࡤࡧࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡆࡥࡳࡴ࡯ࡵࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᅢ"))
            return None
        response = self.bstack1ll1ll11l11_opy_.TestOrchestration(request)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷ࠱ࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠱ࡸ࡫ࡳࡴ࡫ࡲࡲࡂࢁࡽࠣᅣ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1llll1l111l_opy_(self, r):
        if r is not None and getattr(r, bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࠨᅤ"), None) and getattr(r.testhub, bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᅥ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1111l1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᅦ")))
            for bstack1ll1ll1l1ll_opy_, err in errors.items():
                if err[bstack1111l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᅧ")] == bstack1111l1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᅨ"):
                    self.logger.info(err[bstack1111l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅩ")])
                else:
                    self.logger.error(err[bstack1111l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅪ")])
    def bstack1l1l11l111_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()