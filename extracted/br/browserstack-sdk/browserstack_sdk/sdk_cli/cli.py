# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111111l111_opy_ import bstack1111111lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1111l_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111lll_opy_ import bstack1ll1ll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111ll11_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l_opy_ import bstack1llll1l1l_opy_, bstack11lll1111l_opy_, bstack1l1l11llll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import bstack11111111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1llll1l1l11_opy_
from bstack_utils.helper import Notset, bstack1lll1l11ll1_opy_, get_cli_dir, bstack1ll1l1ll11l_opy_, bstack1l111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11l1_opy_ import bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1ll_opy_ import bstack11lll1ll_opy_
from bstack_utils.helper import Notset, bstack1lll1l11ll1_opy_, get_cli_dir, bstack1ll1l1ll11l_opy_, bstack1l111lll_opy_, bstack1l11l1l1_opy_, bstack1l1lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll111l_opy_, bstack1ll1ll1l1l1_opy_, bstack1lll111111l_opy_, bstack1ll1ll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import bstack1lllll1ll11_opy_, bstack1lllll1lll1_opy_, bstack1llllll1111_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1l111l1ll1_opy_ import bstack1ll11l11l1_opy_
from bstack_utils import bstack1l1l11111_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1111ll_opy_, bstack1l11ll1l11_opy_
logger = bstack1l1l11111_opy_.get_logger(__name__, bstack1l1l11111_opy_.bstack1lll11l111l_opy_())
def bstack1lll1lll1ll_opy_(bs_config):
    bstack1lll1111l11_opy_ = None
    bstack1lll11l1111_opy_ = None
    try:
        bstack1lll11l1111_opy_ = get_cli_dir()
        bstack1lll1111l11_opy_ = bstack1ll1l1ll11l_opy_(bstack1lll11l1111_opy_)
        bstack1ll1llll1ll_opy_ = bstack1lll1l11ll1_opy_(bstack1lll1111l11_opy_, bstack1lll11l1111_opy_, bs_config)
        bstack1lll1111l11_opy_ = bstack1ll1llll1ll_opy_ if bstack1ll1llll1ll_opy_ else bstack1lll1111l11_opy_
        if not bstack1lll1111l11_opy_:
            raise ValueError(bstack1111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦႧ"))
    except Exception as ex:
        logger.debug(bstack1111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦႨ").format(ex))
        bstack1lll1111l11_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧႩ"))
        if bstack1lll1111l11_opy_:
            logger.debug(bstack1111lll_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨႪ") + str(bstack1lll1111l11_opy_) + bstack1111lll_opy_ (u"ࠦࠧႫ"))
        else:
            logger.debug(bstack1111lll_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣႬ"))
    return bstack1lll1111l11_opy_, bstack1lll11l1111_opy_
bstack1lll1ll11l1_opy_ = bstack1111lll_opy_ (u"ࠨ࠹࠺࠻࠼ࠦႭ")
bstack1lll1lll1l1_opy_ = bstack1111lll_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨႮ")
bstack1lll11l1l1l_opy_ = bstack1111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧႯ")
bstack1lll111l111_opy_ = bstack1111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢႰ")
bstack1ll1l1l111_opy_ = bstack1111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨႱ")
bstack1lll1ll1l1l_opy_ = re.compile(bstack1111lll_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥႲ"))
bstack1ll1l1ll111_opy_ = bstack1111lll_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥႳ")
bstack1llll111111_opy_ = [
    bstack11lll1111l_opy_.bstack1lllllll1_opy_,
    bstack11lll1111l_opy_.CONNECT,
    bstack11lll1111l_opy_.bstack1l1l1111ll_opy_,
]
class SDKCLI:
    _1ll1ll11l11_opy_ = None
    process: Union[None, Any]
    bstack1llll11ll1l_opy_: bool
    bstack1lll1ll1l11_opy_: bool
    bstack1lll11111ll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1llll1111ll_opy_: Union[None, grpc.Channel]
    bstack1lll1ll11ll_opy_: str
    test_framework: TestFramework
    bstack1llllll1lll_opy_: bstack11111111l1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll111llll_opy_: bstack1lll1111l1l_opy_
    accessibility: bstack1lll1ll1lll_opy_
    bstack1llll1l1ll_opy_: bstack11lll1ll_opy_
    ai: bstack1llll11l1ll_opy_
    bstack1lll1llllll_opy_: bstack1llll111lll_opy_
    bstack1ll1l1lll11_opy_: List[bstack1llll11l111_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1ll1lll11l1_opy_: Any
    bstack1lll111lll1_opy_: Dict[str, timedelta]
    bstack1lll1ll111l_opy_: str
    bstack111111l111_opy_: bstack1111111lll_opy_
    def __new__(cls):
        if not cls._1ll1ll11l11_opy_:
            cls._1ll1ll11l11_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1ll11l11_opy_
    def __init__(self):
        self.process = None
        self.bstack1llll11ll1l_opy_ = False
        self.bstack1llll1111ll_opy_ = None
        self.bstack1lll1llll11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll111l111_opy_, None)
        self.bstack1lll11lllll_opy_ = os.environ.get(bstack1lll11l1l1l_opy_, bstack1111lll_opy_ (u"ࠨࠢႴ")) == bstack1111lll_opy_ (u"ࠢࠣႵ")
        self.bstack1lll1ll1l11_opy_ = False
        self.bstack1lll11111ll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1ll1lll11l1_opy_ = None
        self.test_framework = None
        self.bstack1llllll1lll_opy_ = None
        self.bstack1lll1ll11ll_opy_=bstack1111lll_opy_ (u"ࠣࠤႶ")
        self.session_framework = None
        self.logger = bstack1l1l11111_opy_.get_logger(self.__class__.__name__, bstack1l1l11111_opy_.bstack1lll11l111l_opy_())
        self.bstack1lll111lll1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack111111l111_opy_ = bstack1111111lll_opy_()
        self.bstack1lll11l1lll_opy_ = None
        self.bstack1llll1l1l1l_opy_ = None
        self.bstack1lll111llll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1l1lll11_opy_ = []
    def bstack11l1111l1l_opy_(self):
        return os.environ.get(bstack1ll1l1l111_opy_).lower().__eq__(bstack1111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢႷ"))
    def is_enabled(self, config):
        if bstack1111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧႸ") in config and str(config[bstack1111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨႹ")]).lower() != bstack1111lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫႺ"):
            return False
        bstack1ll1ll11ll1_opy_ = [bstack1111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨႻ"), bstack1111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦႼ")]
        bstack1lll11ll11l_opy_ = config.get(bstack1111lll_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦႽ")) in bstack1ll1ll11ll1_opy_ or os.environ.get(bstack1111lll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪႾ")) in bstack1ll1ll11ll1_opy_
        os.environ[bstack1111lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨႿ")] = str(bstack1lll11ll11l_opy_) # bstack1lll11lll11_opy_ bstack1lll1l1llll_opy_ VAR to bstack1ll1ll1lll1_opy_ is binary running
        return bstack1lll11ll11l_opy_
    def bstack11ll111lll_opy_(self):
        for event in bstack1llll111111_opy_:
            bstack1llll1l1l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1llll1l1l_opy_.logger.debug(bstack1111lll_opy_ (u"ࠦࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠣࡁࡃࠦࡻࡢࡴࡪࡷࢂࠦࠢჀ") + str(kwargs) + bstack1111lll_opy_ (u"ࠧࠨჁ"))
            )
        bstack1llll1l1l_opy_.register(bstack11lll1111l_opy_.bstack1lllllll1_opy_, self.__1ll1lll1l1l_opy_)
        bstack1llll1l1l_opy_.register(bstack11lll1111l_opy_.CONNECT, self.__1ll1lll1111_opy_)
        bstack1llll1l1l_opy_.register(bstack11lll1111l_opy_.bstack1l1l1111ll_opy_, self.__1lll11ll1l1_opy_)
        bstack1llll1l1l_opy_.register(bstack11lll1111l_opy_.bstack11ll1ll1ll_opy_, self.__1ll1llllll1_opy_)
    def bstack11l1lll11_opy_(self):
        return not self.bstack1lll11lllll_opy_ and os.environ.get(bstack1lll11l1l1l_opy_, bstack1111lll_opy_ (u"ࠨࠢჂ")) != bstack1111lll_opy_ (u"ࠢࠣჃ")
    def is_running(self):
        if self.bstack1lll11lllll_opy_:
            return self.bstack1llll11ll1l_opy_
        else:
            return bool(self.bstack1llll1111ll_opy_)
    def bstack1ll1lllllll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1l1lll11_opy_) and cli.is_running()
    def __1ll1l1ll1l1_opy_(self, bstack1lll111l1l1_opy_=10):
        if self.bstack1lll1llll11_opy_:
            return
        bstack11l1l1ll1l_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll111l111_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1111lll_opy_ (u"ࠣ࡝ࠥჄ") + str(id(self)) + bstack1111lll_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣჅ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1111lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧ჆"), 0), (bstack1111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢჇ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll111l1l1_opy_)
        self.bstack1llll1111ll_opy_ = channel
        self.bstack1lll1llll11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1llll1111ll_opy_)
        self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦ჈"), datetime.now() - bstack11l1l1ll1l_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll111l111_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨ჉") + str(self.bstack11l1lll11_opy_()) + bstack1111lll_opy_ (u"ࠢࠣ჊"))
    def __1lll11ll1l1_opy_(self, event_name):
        if self.bstack11l1lll11_opy_():
            self.logger.debug(bstack1111lll_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣ჋"))
        self.__1lll1l1l1l1_opy_()
    def __1ll1llllll1_opy_(self, event_name, bstack1lll1ll1ll1_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1111lll_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤ჌"))
        bstack1lll11ll111_opy_ = Path(bstack1llll1l1ll1_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦჍ"))
        if self.bstack1lll11l1111_opy_ and bstack1lll11ll111_opy_.exists():
            with open(bstack1lll11ll111_opy_, bstack1111lll_opy_ (u"ࠫࡷ࠭჎"), encoding=bstack1111lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ჏")) as fp:
                data = json.load(fp)
                try:
                    bstack1l11l1l1_opy_(bstack1111lll_opy_ (u"࠭ࡐࡐࡕࡗࠫა"), bstack1ll11l11l1_opy_(bstack1l1l11111l_opy_), data, {
                        bstack1111lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬბ"): (self.config[bstack1111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪგ")], self.config[bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬდ")])
                    })
                except Exception as e:
                    logger.debug(bstack1l11ll1l11_opy_.format(str(e)))
            bstack1lll11ll111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1llll111l11_opy_, stage=STAGE.bstack11111lll_opy_)
    def __1ll1lll1l1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
        self.bstack1lll1ll11ll_opy_, self.bstack1lll11l1111_opy_ = bstack1lll1lll1ll_opy_(data.bs_config)
        os.environ[bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨე")] = self.bstack1lll11l1111_opy_
        if not self.bstack1lll1ll11ll_opy_ or not self.bstack1lll11l1111_opy_:
            raise ValueError(bstack1111lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥვ"))
        if self.bstack11l1lll11_opy_():
            self.__1ll1lll1111_opy_(event_name, bstack1l1l11llll_opy_())
            return
        try:
            bstack1ll1llll11l_opy_.end(EVENTS.bstack1l11ll1l_opy_.value, EVENTS.bstack1l11ll1l_opy_.value + bstack1111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧზ"), EVENTS.bstack1l11ll1l_opy_.value + bstack1111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦთ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1111lll_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨი"))
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧკ").format(e))
        start = datetime.now()
        is_started = self.__1lll1l1ll11_opy_()
        self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨლ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1l1ll1l1_opy_()
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤმ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1llll111_opy_(data)
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤნ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll111ll1l_opy_, stage=STAGE.bstack11111lll_opy_)
    def __1ll1lll1111_opy_(self, event_name: str, data: bstack1l1l11llll_opy_):
        if not self.bstack11l1lll11_opy_():
            self.logger.debug(bstack1111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤო"))
            return
        bin_session_id = os.environ.get(bstack1lll11l1l1l_opy_)
        start = datetime.now()
        self.__1ll1l1ll1l1_opy_()
        self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧპ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1111lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨჟ") + str(bin_session_id) + bstack1111lll_opy_ (u"ࠣࠤრ"))
        start = datetime.now()
        self.__1llll111l1l_opy_()
        self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢს"), datetime.now() - start)
    def __1lll1lll111_opy_(self):
        if not self.bstack1lll1llll11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢტ"))
            return
        bstack1lll1l1lll1_opy_ = {
            bstack1111lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣუ"): (bstack1lll11l11ll_opy_, bstack1lll111l11l_opy_, bstack1llll1l1l11_opy_),
            bstack1111lll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢფ"): (bstack1ll1ll1ll11_opy_, bstack1lll11l1ll1_opy_, bstack1lll1lll11l_opy_),
        }
        if not self.bstack1lll11l1lll_opy_ and self.session_framework in bstack1lll1l1lll1_opy_:
            bstack1llll1l111l_opy_, bstack1lll1l1ll1l_opy_, bstack1lll1l1l11l_opy_ = bstack1lll1l1lll1_opy_[self.session_framework]
            bstack1lll11lll1l_opy_ = bstack1lll1l1ll1l_opy_()
            self.bstack1llll1l1l1l_opy_ = bstack1lll11lll1l_opy_
            self.bstack1lll11l1lll_opy_ = bstack1lll1l1l11l_opy_
            self.bstack1ll1l1lll11_opy_.append(bstack1lll11lll1l_opy_)
            self.bstack1ll1l1lll11_opy_.append(bstack1llll1l111l_opy_(self.bstack1llll1l1l1l_opy_))
        if not self.bstack1lll111llll_opy_ and self.config_observability and self.config_observability.success: # bstack1lll11ll1ll_opy_
            self.bstack1lll111llll_opy_ = bstack1lll1111l1l_opy_(self.bstack1lll11l1lll_opy_, self.bstack1llll1l1l1l_opy_) # bstack1llll11111l_opy_
            self.bstack1ll1l1lll11_opy_.append(self.bstack1lll111llll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll1ll1lll_opy_(self.bstack1lll11l1lll_opy_, self.bstack1llll1l1l1l_opy_)
            self.bstack1ll1l1lll11_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1111lll_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣქ"), False) == True:
            self.ai = bstack1llll11l1ll_opy_()
            self.bstack1ll1l1lll11_opy_.append(self.ai)
        if not self.percy and self.bstack1ll1lll11l1_opy_ and self.bstack1ll1lll11l1_opy_.success:
            self.percy = bstack1llll111lll_opy_(self.bstack1ll1lll11l1_opy_)
            self.bstack1ll1l1lll11_opy_.append(self.percy)
        for mod in self.bstack1ll1l1lll11_opy_:
            if not mod.bstack1llll11l1l1_opy_():
                mod.configure(self.bstack1lll1llll11_opy_, self.config, self.cli_bin_session_id, self.bstack111111l111_opy_)
    def __1ll1lll11ll_opy_(self):
        for mod in self.bstack1ll1l1lll11_opy_:
            if mod.bstack1llll11l1l1_opy_():
                mod.configure(self.bstack1lll1llll11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll1l1l111_opy_, stage=STAGE.bstack11111lll_opy_)
    def __1ll1llll111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll1ll1l11_opy_:
            return
        self.__1lll1l11l1l_opy_(data)
        bstack11l1l1ll1l_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1111lll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢღ")
        req.sdk_language = bstack1111lll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣყ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll1ll1l1l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤ࡞ࠦშ") + str(id(self)) + bstack1111lll_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჩ"))
            r = self.bstack1lll1llll11_opy_.StartBinSession(req)
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨც"), datetime.now() - bstack11l1l1ll1l_opy_)
            os.environ[bstack1lll11l1l1l_opy_] = r.bin_session_id
            self.__1llll1l11ll_opy_(r)
            self.__1lll1lll111_opy_()
            self.bstack111111l111_opy_.start()
            self.bstack1lll1ll1l11_opy_ = True
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡡࠢძ") + str(id(self)) + bstack1111lll_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦწ"))
        except grpc.bstack1llll11l11l_opy_ as bstack1ll1ll111l1_opy_:
            self.logger.error(bstack1111lll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤჭ") + str(bstack1ll1ll111l1_opy_) + bstack1111lll_opy_ (u"ࠣࠤხ"))
            traceback.print_exc()
            raise bstack1ll1ll111l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨჯ") + str(e) + bstack1111lll_opy_ (u"ࠥࠦჰ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1l1lllll_opy_, stage=STAGE.bstack11111lll_opy_)
    def __1llll111l1l_opy_(self):
        if not self.bstack11l1lll11_opy_() or not self.cli_bin_session_id or self.bstack1lll11111ll_opy_:
            return
        bstack11l1l1ll1l_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫჱ"), bstack1111lll_opy_ (u"ࠬ࠶ࠧჲ")))
        try:
            self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡛ࠣჳ") + str(id(self)) + bstack1111lll_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჴ"))
            r = self.bstack1lll1llll11_opy_.ConnectBinSession(req)
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧჵ"), datetime.now() - bstack11l1l1ll1l_opy_)
            self.__1llll1l11ll_opy_(r)
            self.__1lll1lll111_opy_()
            self.bstack111111l111_opy_.start()
            self.bstack1lll11111ll_opy_ = True
            self.logger.debug(bstack1111lll_opy_ (u"ࠤ࡞ࠦჶ") + str(id(self)) + bstack1111lll_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤჷ"))
        except grpc.bstack1llll11l11l_opy_ as bstack1ll1ll111l1_opy_:
            self.logger.error(bstack1111lll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨჸ") + str(bstack1ll1ll111l1_opy_) + bstack1111lll_opy_ (u"ࠧࠨჹ"))
            traceback.print_exc()
            raise bstack1ll1ll111l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥჺ") + str(e) + bstack1111lll_opy_ (u"ࠢࠣ჻"))
            traceback.print_exc()
            raise e
    def __1llll1l11ll_opy_(self, r):
        self.bstack1ll1lllll11_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1111lll_opy_ (u"ࠣࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢჼ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1111lll_opy_ (u"ࠤࡨࡱࡵࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡹࡳࡪࠢჽ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡧࡵࡧࡾࠦࡩࡴࠢࡶࡩࡳࡺࠠࡰࡰ࡯ࡽࠥࡧࡳࠡࡲࡤࡶࡹࠦ࡯ࡧࠢࡷ࡬ࡪࠦࠢࡄࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠰ࠧࠦࡡ࡯ࡦࠣࡸ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡡ࡭ࡵࡲࠤࡺࡹࡥࡥࠢࡥࡽ࡙ࠥࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡪࡸࡥࡧࡱࡵࡩ࠱ࠦࡎࡰࡰࡨࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡩࡴࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧჾ")
        self.bstack1ll1lll11l1_opy_ = getattr(r, bstack1111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪჿ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᄀ")] = self.config_testhub.jwt
        os.environ[bstack1111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᄁ")] = self.config_testhub.build_hashed_id
    def bstack1llll11ll11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1llll11ll1l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll1111ll1_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll1111ll1_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1llll11ll11_opy_(event_name=EVENTS.bstack1lll11l1l11_opy_, stage=STAGE.bstack11111lll_opy_)
    def __1lll1l1ll11_opy_(self, bstack1lll111l1l1_opy_=10):
        if self.bstack1llll11ll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤᄂ"))
            return True
        self.logger.debug(bstack1111lll_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢᄃ"))
        if os.getenv(bstack1111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤᄄ")) == bstack1ll1l1ll111_opy_:
            self.cli_bin_session_id = bstack1ll1l1ll111_opy_
            self.cli_listen_addr = bstack1111lll_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨᄅ") % (self.cli_bin_session_id)
            self.bstack1llll11ll1l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1ll11ll_opy_, bstack1111lll_opy_ (u"ࠦࡸࡪ࡫ࠣᄆ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1ll11l1l_opy_ compat for text=True in bstack1ll1lllll1l_opy_ python
            encoding=bstack1111lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᄇ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1l1llll1_opy_ = threading.Thread(target=self.__1lll1l111ll_opy_, args=(bstack1lll111l1l1_opy_,))
        bstack1ll1l1llll1_opy_.start()
        bstack1ll1l1llll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥᄈ") + str(self.process.stderr.read()) + bstack1111lll_opy_ (u"ࠢࠣᄉ"))
        if not self.bstack1llll11ll1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠣ࡝ࠥᄊ") + str(id(self)) + bstack1111lll_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧᄋ"))
            self.__1lll1l1l1l1_opy_()
        self.logger.debug(bstack1111lll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦᄌ") + str(self.bstack1llll11ll1l_opy_) + bstack1111lll_opy_ (u"ࠦࠧᄍ"))
        return self.bstack1llll11ll1l_opy_
    def __1lll1l111ll_opy_(self, bstack1lll11llll1_opy_=10):
        bstack1lll1l1111l_opy_ = time.time()
        while self.process and time.time() - bstack1lll1l1111l_opy_ < bstack1lll11llll1_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1111lll_opy_ (u"ࠧ࡯ࡤ࠾ࠤᄎ") in line:
                    self.cli_bin_session_id = line.split(bstack1111lll_opy_ (u"ࠨࡩࡥ࠿ࠥᄏ"))[-1:][0].strip()
                    self.logger.debug(bstack1111lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨᄐ") + str(self.cli_bin_session_id) + bstack1111lll_opy_ (u"ࠣࠤᄑ"))
                    continue
                if bstack1111lll_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᄒ") in line:
                    self.cli_listen_addr = line.split(bstack1111lll_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦᄓ"))[-1:][0].strip()
                    self.logger.debug(bstack1111lll_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢᄔ") + str(self.cli_listen_addr) + bstack1111lll_opy_ (u"ࠧࠨᄕ"))
                    continue
                if bstack1111lll_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᄖ") in line:
                    port = line.split(bstack1111lll_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨᄗ"))[-1:][0].strip()
                    self.logger.debug(bstack1111lll_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢᄘ") + str(port) + bstack1111lll_opy_ (u"ࠤࠥᄙ"))
                    continue
                if line.strip() == bstack1lll1lll1l1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1111lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧᄚ"), bstack1111lll_opy_ (u"ࠦ࠶ࠨᄛ")) == bstack1111lll_opy_ (u"ࠧ࠷ࠢᄜ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1llll11ll1l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1111lll_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢᄝ") + str(e) + bstack1111lll_opy_ (u"ࠢࠣᄞ"))
        return False
    @measure(event_name=EVENTS.bstack1ll1ll1l111_opy_, stage=STAGE.bstack11111lll_opy_)
    def __1lll1l1l1l1_opy_(self):
        if self.bstack1llll1111ll_opy_:
            self.bstack111111l111_opy_.stop()
            start = datetime.now()
            if self.bstack1llll1l1111_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll11111ll_opy_:
                    self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᄟ"), datetime.now() - start)
                else:
                    self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᄠ"), datetime.now() - start)
            self.__1ll1lll11ll_opy_()
            start = datetime.now()
            self.bstack1llll1111ll_opy_.close()
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧᄡ"), datetime.now() - start)
            self.bstack1llll1111ll_opy_ = None
        if self.process:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡸࡺ࡯ࡱࠤᄢ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣᄣ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll11lllll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11l1l11l11_opy_()
                self.logger.info(
                    bstack1111lll_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳࠨᄤ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1111lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᄥ")] = self.config_testhub.build_hashed_id
        self.bstack1llll11ll1l_opy_ = False
    def __1lll1l11l1l_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1111lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᄦ")] = selenium.__version__
            data.frameworks.append(bstack1111lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᄧ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1111lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᄨ")] = __version__
            data.frameworks.append(bstack1111lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᄩ"))
        except:
            pass
    def bstack1llll11llll_opy_(self, hub_url: str, platform_index: int, bstack1ll11ll11l_opy_: Any):
        if self.bstack1llllll1lll_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᄪ"))
            return
        try:
            bstack11l1l1ll1l_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1111lll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᄫ")
            self.bstack1llllll1lll_opy_ = bstack1lll1lll11l_opy_(
                cli.config.get(bstack1111lll_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢᄬ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll1l111l1_opy_={bstack1111lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧᄭ"): bstack1ll11ll11l_opy_}
            )
            def bstack1lll1ll1111_opy_(self):
                return
            if self.config.get(bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦᄮ"), True):
                Service.start = bstack1lll1ll1111_opy_
                Service.stop = bstack1lll1ll1111_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack11lll1ll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1ll1lll1l11_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᄯ"), datetime.now() - bstack11l1l1ll1l_opy_)
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥᄰ") + str(e) + bstack1111lll_opy_ (u"ࠧࠨᄱ"))
    def bstack1lll1111111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1l111llll1_opy_
            self.bstack1llllll1lll_opy_ = bstack1llll1l1l11_opy_(
                platform_index,
                framework_name=bstack1111lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᄲ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣᄳ") + str(e) + bstack1111lll_opy_ (u"ࠣࠤᄴ"))
            pass
    def bstack1lll1l11l11_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᄵ"))
            return
        if bstack1l111lll_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᄶ"): pytest.__version__ }, [bstack1111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᄷ")], self.bstack111111l111_opy_, self.bstack1lll1llll11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1lll1lll_opy_({ bstack1111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᄸ"): pytest.__version__ }, [bstack1111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᄹ")], self.bstack111111l111_opy_, self.bstack1lll1llll11_opy_)
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦᄺ") + str(e) + bstack1111lll_opy_ (u"ࠣࠤᄻ"))
        self.bstack1lll1lllll1_opy_()
    def bstack1lll1lllll1_opy_(self):
        if not self.bstack11l1111l1l_opy_():
            return
        bstack11l1l111l1_opy_ = None
        def bstack11l11lll1_opy_(config, startdir):
            return bstack1111lll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢᄼ").format(bstack1111lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᄽ"))
        def bstack111ll1ll_opy_():
            return
        def bstack11llll11l_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1111lll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᄾ"):
                return bstack1111lll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᄿ")
            else:
                return bstack11l1l111l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11l1l111l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l11lll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111ll1ll_opy_
            Config.getoption = bstack11llll11l_opy_
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣᅀ") + str(e) + bstack1111lll_opy_ (u"ࠢࠣᅁ"))
    def bstack1ll1ll11111_opy_(self):
        bstack1l1111llll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1l1111llll_opy_, dict):
            if cli.config_observability:
                bstack1l1111llll_opy_.update(
                    {bstack1111lll_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣᅂ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1111lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧᅃ") in accessibility.get(bstack1111lll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᅄ"), {}):
                    bstack1ll1llll1l1_opy_ = accessibility.get(bstack1111lll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᅅ"))
                    bstack1ll1llll1l1_opy_.update({ bstack1111lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨᅆ"): bstack1ll1llll1l1_opy_.pop(bstack1111lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᅇ")) })
                bstack1l1111llll_opy_.update({bstack1111lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᅈ"): accessibility })
        return bstack1l1111llll_opy_
    @measure(event_name=EVENTS.bstack1llll1l1lll_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1llll1l1111_opy_(self, bstack1ll1ll1l11l_opy_: str = None, bstack1lll1l1l1ll_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll1llll11_opy_:
            return
        bstack11l1l1ll1l_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll1ll1l11l_opy_:
            req.bstack1ll1ll1l11l_opy_ = bstack1ll1ll1l11l_opy_
        if bstack1lll1l1l1ll_opy_:
            req.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
        try:
            r = self.bstack1lll1llll11_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᅉ"), datetime.now() - bstack11l1l1ll1l_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1l11ll111_opy_(self, key: str, value: timedelta):
        tag = bstack1111lll_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᅊ") if self.bstack11l1lll11_opy_() else bstack1111lll_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᅋ")
        self.bstack1lll111lll1_opy_[bstack1111lll_opy_ (u"ࠦ࠿ࠨᅌ").join([tag + bstack1111lll_opy_ (u"ࠧ࠳ࠢᅍ") + str(id(self)), key])] += value
    def bstack11l1l11l11_opy_(self):
        if not os.getenv(bstack1111lll_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥᅎ"), bstack1111lll_opy_ (u"ࠢ࠱ࠤᅏ")) == bstack1111lll_opy_ (u"ࠣ࠳ࠥᅐ"):
            return
        bstack1ll1lll1ll1_opy_ = dict()
        bstack1lllllll11l_opy_ = []
        if self.test_framework:
            bstack1lllllll11l_opy_.extend(list(self.test_framework.bstack1lllllll11l_opy_.values()))
        if self.bstack1llllll1lll_opy_:
            bstack1lllllll11l_opy_.extend(list(self.bstack1llllll1lll_opy_.bstack1lllllll11l_opy_.values()))
        for instance in bstack1lllllll11l_opy_:
            if not instance.platform_index in bstack1ll1lll1ll1_opy_:
                bstack1ll1lll1ll1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1ll1lll1ll1_opy_[instance.platform_index]
            for k, v in instance.bstack1lll111l1ll_opy_().items():
                report[k] += v
                report[k.split(bstack1111lll_opy_ (u"ࠤ࠽ࠦᅑ"))[0]] += v
        bstack1lll1l11111_opy_ = sorted([(k, v) for k, v in self.bstack1lll111lll1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1ll11lll_opy_ = 0
        for r in bstack1lll1l11111_opy_:
            bstack1ll1l1l1lll_opy_ = r[1].total_seconds()
            bstack1ll1ll11lll_opy_ += bstack1ll1l1l1lll_opy_
            self.logger.debug(bstack1111lll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣᅒ") + str(bstack1ll1l1l1lll_opy_) + bstack1111lll_opy_ (u"ࠦࠧᅓ"))
        self.logger.debug(bstack1111lll_opy_ (u"ࠧ࠳࠭ࠣᅔ"))
        bstack1ll1l1ll1ll_opy_ = []
        for platform_index, report in bstack1ll1lll1ll1_opy_.items():
            bstack1ll1l1ll1ll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1l1ll1ll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l1ll1l1_opy_ = set()
        bstack1ll1ll1ll1l_opy_ = 0
        for r in bstack1ll1l1ll1ll_opy_:
            bstack1ll1l1l1lll_opy_ = r[2].total_seconds()
            bstack1ll1ll1ll1l_opy_ += bstack1ll1l1l1lll_opy_
            bstack1l1ll1l1_opy_.add(r[0])
            self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢᅕ") + str(bstack1ll1l1l1lll_opy_) + bstack1111lll_opy_ (u"ࠢࠣᅖ"))
        if self.bstack11l1lll11_opy_():
            self.logger.debug(bstack1111lll_opy_ (u"ࠣ࠯࠰ࠦᅗ"))
            self.logger.debug(bstack1111lll_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤᅘ") + str(bstack1ll1ll1ll1l_opy_) + bstack1111lll_opy_ (u"ࠥࠦᅙ"))
        else:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᅚ") + str(bstack1ll1ll11lll_opy_) + bstack1111lll_opy_ (u"ࠧࠨᅛ"))
        self.logger.debug(bstack1111lll_opy_ (u"ࠨ࠭࠮ࠤᅜ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1lll1llll11_opy_:
            self.logger.error(bstack1111lll_opy_ (u"ࠢࡤ࡮࡬ࡣࡸ࡫ࡲࡷ࡫ࡦࡩࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᅝ"))
            return None
        response = self.bstack1lll1llll11_opy_.TestOrchestration(request)
        self.logger.debug(bstack1111lll_opy_ (u"ࠣࡶࡨࡷࡹ࠳࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠳ࡳࡦࡵࡶ࡭ࡴࡴ࠽ࡼࡿࠥᅞ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1lllll11_opy_(self, r):
        if r is not None and getattr(r, bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࠪᅟ"), None) and getattr(r.testhub, bstack1111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᅠ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1111lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᅡ")))
            for bstack1ll1ll1l1ll_opy_, err in errors.items():
                if err[bstack1111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪᅢ")] == bstack1111lll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᅣ"):
                    self.logger.info(err[bstack1111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅤ")])
                else:
                    self.logger.error(err[bstack1111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅥ")])
    def bstack11l11l11_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()