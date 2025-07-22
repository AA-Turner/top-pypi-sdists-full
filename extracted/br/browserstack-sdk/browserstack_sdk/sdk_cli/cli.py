# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111ll_opy_ import bstack1lll111111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack1ll1ll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1lll1_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1ll1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l111l_opy_ import bstack1ll1lll111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111lll_opy_ import bstack1lll111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1l_opy_ import bstack1ll1l1ll1l_opy_, bstack111ll1ll_opy_, bstack1l11ll1l11_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll1111111_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack11111111ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1ll1llll11l_opy_
from bstack_utils.helper import Notset, bstack1lll111ll11_opy_, get_cli_dir, bstack1lll111l1l1_opy_, bstack11l1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll111l111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1111lll1l_opy_ import bstack1lll1ll1ll_opy_
from bstack_utils.helper import Notset, bstack1lll111ll11_opy_, get_cli_dir, bstack1lll111l1l1_opy_, bstack11l1l11l_opy_, bstack1llll111l_opy_, bstack1ll1l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1lll_opy_, bstack1lll1lllll1_opy_, bstack1lll111llll_opy_, bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1lllll1ll1l_opy_, bstack1lllllll11l_opy_, bstack1llllll1111_opy_
from bstack_utils.constants import *
from bstack_utils.bstack111111ll_opy_ import bstack1ll1l1ll_opy_
from bstack_utils import bstack1l1111ll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1llll1_opy_, bstack11l111lll1_opy_
logger = bstack1l1111ll_opy_.get_logger(__name__, bstack1l1111ll_opy_.bstack1lll1llll1l_opy_())
def bstack1lll1111lll_opy_(bs_config):
    bstack1ll1ll11l1l_opy_ = None
    bstack1lll1ll11l1_opy_ = None
    try:
        bstack1lll1ll11l1_opy_ = get_cli_dir()
        bstack1ll1ll11l1l_opy_ = bstack1lll111l1l1_opy_(bstack1lll1ll11l1_opy_)
        bstack1ll1ll11111_opy_ = bstack1lll111ll11_opy_(bstack1ll1ll11l1l_opy_, bstack1lll1ll11l1_opy_, bs_config)
        bstack1ll1ll11l1l_opy_ = bstack1ll1ll11111_opy_ if bstack1ll1ll11111_opy_ else bstack1ll1ll11l1l_opy_
        if not bstack1ll1ll11l1l_opy_:
            raise ValueError(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠦႠ"))
    except Exception as ex:
        logger.debug(bstack111l111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡ࡮ࡤࡸࡪࡹࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡽࢀࠦႡ").format(ex))
        bstack1ll1ll11l1l_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧႢ"))
        if bstack1ll1ll11l1l_opy_:
            logger.debug(bstack111l111_opy_ (u"ࠥࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡵࡳࡲࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠾ࠥࠨႣ") + str(bstack1ll1ll11l1l_opy_) + bstack111l111_opy_ (u"ࠦࠧႤ"))
        else:
            logger.debug(bstack111l111_opy_ (u"ࠧࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶ࠾ࠤࡸ࡫ࡴࡶࡲࠣࡱࡦࡿࠠࡣࡧࠣ࡭ࡳࡩ࡯࡮ࡲ࡯ࡩࡹ࡫࠮ࠣႥ"))
    return bstack1ll1ll11l1l_opy_, bstack1lll1ll11l1_opy_
bstack1llll1l1l1l_opy_ = bstack111l111_opy_ (u"ࠨ࠹࠺࠻࠼ࠦႦ")
bstack1llll11ll1l_opy_ = bstack111l111_opy_ (u"ࠢࡳࡧࡤࡨࡾࠨႧ")
bstack1lll1111ll1_opy_ = bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧႨ")
bstack1llll11l11l_opy_ = bstack111l111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡏࡍࡘ࡚ࡅࡏࡡࡄࡈࡉࡘࠢႩ")
bstack11l1l111_opy_ = bstack111l111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨႪ")
bstack1lll11l1lll_opy_ = re.compile(bstack111l111_opy_ (u"ࡶࠧ࠮࠿ࡪࠫ࠱࠮࠭ࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࢀࡇ࡙ࠩ࠯ࠬࠥႫ"))
bstack1llll1l11ll_opy_ = bstack111l111_opy_ (u"ࠧࡪࡥࡷࡧ࡯ࡳࡵࡳࡥ࡯ࡶࠥႬ")
bstack1ll1l1l1lll_opy_ = [
    bstack111ll1ll_opy_.bstack1llllll111_opy_,
    bstack111ll1ll_opy_.CONNECT,
    bstack111ll1ll_opy_.bstack111llll1_opy_,
]
class SDKCLI:
    _1llll11l1ll_opy_ = None
    process: Union[None, Any]
    bstack1lll1ll1111_opy_: bool
    bstack1ll1llll1ll_opy_: bool
    bstack1llll111l1l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1llll1l1lll_opy_: Union[None, grpc.Channel]
    bstack1ll1lll11l1_opy_: str
    test_framework: TestFramework
    bstack1llll1lll1l_opy_: bstack11111111ll_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll1ll1ll1_opy_: bstack1lll111l11l_opy_
    accessibility: bstack1lll11ll11l_opy_
    bstack1111lll1l_opy_: bstack1lll1ll1ll_opy_
    ai: bstack1lll111111l_opy_
    bstack1ll1lll1l1l_opy_: bstack1ll1ll11ll1_opy_
    bstack1ll1l1ll11l_opy_: List[bstack1llll1l1l11_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll11l1ll1_opy_: Any
    bstack1ll1lllllll_opy_: Dict[str, timedelta]
    bstack1ll1ll1l1ll_opy_: str
    bstack1111111lll_opy_: bstack111111l1l1_opy_
    def __new__(cls):
        if not cls._1llll11l1ll_opy_:
            cls._1llll11l1ll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1llll11l1ll_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1ll1111_opy_ = False
        self.bstack1llll1l1lll_opy_ = None
        self.bstack1lll1l11l1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1llll11l11l_opy_, None)
        self.bstack1lll1ll1l1l_opy_ = os.environ.get(bstack1lll1111ll1_opy_, bstack111l111_opy_ (u"ࠨࠢႭ")) == bstack111l111_opy_ (u"ࠢࠣႮ")
        self.bstack1ll1llll1ll_opy_ = False
        self.bstack1llll111l1l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll11l1ll1_opy_ = None
        self.test_framework = None
        self.bstack1llll1lll1l_opy_ = None
        self.bstack1ll1lll11l1_opy_=bstack111l111_opy_ (u"ࠣࠤႯ")
        self.session_framework = None
        self.logger = bstack1l1111ll_opy_.get_logger(self.__class__.__name__, bstack1l1111ll_opy_.bstack1lll1llll1l_opy_())
        self.bstack1ll1lllllll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111111lll_opy_ = bstack111111l1l1_opy_()
        self.bstack1lll1l1ll1l_opy_ = None
        self.bstack1ll1ll1ll11_opy_ = None
        self.bstack1lll1ll1ll1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1ll1l1ll11l_opy_ = []
    def bstack1lllll1lll_opy_(self):
        return os.environ.get(bstack11l1l111_opy_).lower().__eq__(bstack111l111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢႰ"))
    def is_enabled(self, config):
        if bstack111l111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧႱ") in config and str(config[bstack111l111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨႲ")]).lower() != bstack111l111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫႳ"):
            return False
        bstack1ll1llll111_opy_ = [bstack111l111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨႴ"), bstack111l111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦႵ")]
        bstack1ll1ll1llll_opy_ = config.get(bstack111l111_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦႶ")) in bstack1ll1llll111_opy_ or os.environ.get(bstack111l111_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪႷ")) in bstack1ll1llll111_opy_
        os.environ[bstack111l111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨႸ")] = str(bstack1ll1ll1llll_opy_) # bstack1ll1l1llll1_opy_ bstack1llll11lll1_opy_ VAR to bstack1lll1111l11_opy_ is binary running
        return bstack1ll1ll1llll_opy_
    def bstack1ll1111lll_opy_(self):
        for event in bstack1ll1l1l1lll_opy_:
            bstack1ll1l1ll1l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1ll1l1ll1l_opy_.logger.debug(bstack111l111_opy_ (u"ࠦࢀ࡫ࡶࡦࡰࡷࡣࡳࡧ࡭ࡦࡿࠣࡁࡃࠦࡻࡢࡴࡪࡷࢂࠦࠢႹ") + str(kwargs) + bstack111l111_opy_ (u"ࠧࠨႺ"))
            )
        bstack1ll1l1ll1l_opy_.register(bstack111ll1ll_opy_.bstack1llllll111_opy_, self.__1ll1ll1111l_opy_)
        bstack1ll1l1ll1l_opy_.register(bstack111ll1ll_opy_.CONNECT, self.__1lll11l1111_opy_)
        bstack1ll1l1ll1l_opy_.register(bstack111ll1ll_opy_.bstack111llll1_opy_, self.__1lll11ll111_opy_)
        bstack1ll1l1ll1l_opy_.register(bstack111ll1ll_opy_.bstack1lll111ll_opy_, self.__1ll1l1ll111_opy_)
    def bstack1l1l1lll1l_opy_(self):
        return not self.bstack1lll1ll1l1l_opy_ and os.environ.get(bstack1lll1111ll1_opy_, bstack111l111_opy_ (u"ࠨࠢႻ")) != bstack111l111_opy_ (u"ࠢࠣႼ")
    def is_running(self):
        if self.bstack1lll1ll1l1l_opy_:
            return self.bstack1lll1ll1111_opy_
        else:
            return bool(self.bstack1llll1l1lll_opy_)
    def bstack1lll111lll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1ll1l1ll11l_opy_) and cli.is_running()
    def __1lll1111l1l_opy_(self, bstack1lll11l111l_opy_=10):
        if self.bstack1lll1l11l1l_opy_:
            return
        bstack1l1111lll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1llll11l11l_opy_, self.cli_listen_addr)
        self.logger.debug(bstack111l111_opy_ (u"ࠣ࡝ࠥႽ") + str(id(self)) + bstack111l111_opy_ (u"ࠤࡠࠤࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡴࡧࠣႾ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack111l111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡥࡰࡳࡱࡻࡽࠧႿ"), 0), (bstack111l111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶࡳࡠࡲࡵࡳࡽࡿࠢჀ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll11l111l_opy_)
        self.bstack1llll1l1lll_opy_ = channel
        self.bstack1lll1l11l1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1llll1l1lll_opy_)
        self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࠦჁ"), datetime.now() - bstack1l1111lll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1llll11l11l_opy_] = self.cli_listen_addr
        self.logger.debug(bstack111l111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤ࠻ࠢ࡬ࡷࡤࡩࡨࡪ࡮ࡧࡣࡵࡸ࡯ࡤࡧࡶࡷࡂࠨჂ") + str(self.bstack1l1l1lll1l_opy_()) + bstack111l111_opy_ (u"ࠢࠣჃ"))
    def __1lll11ll111_opy_(self, event_name):
        if self.bstack1l1l1lll1l_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡴࡶࡰࡪࡰࡪࠤࡈࡒࡉࠣჄ"))
        self.__1lll1lll11l_opy_()
    def __1ll1l1ll111_opy_(self, event_name, bstack1lll11111l1_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack111l111_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠤჅ"))
        bstack1ll1lll11ll_opy_ = Path(bstack1lll11l11ll_opy_ (u"ࠥࡿࡸ࡫࡬ࡧ࠰ࡦࡰ࡮ࡥࡤࡪࡴࢀ࠳ࡺࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࡸ࠴ࡪࡴࡱࡱࠦ჆"))
        if self.bstack1lll1ll11l1_opy_ and bstack1ll1lll11ll_opy_.exists():
            with open(bstack1ll1lll11ll_opy_, bstack111l111_opy_ (u"ࠫࡷ࠭Ⴧ"), encoding=bstack111l111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ჈")) as fp:
                data = json.load(fp)
                try:
                    bstack1llll111l_opy_(bstack111l111_opy_ (u"࠭ࡐࡐࡕࡗࠫ჉"), bstack1ll1l1ll_opy_(bstack1111ll111_opy_), data, {
                        bstack111l111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ჊"): (self.config[bstack111l111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ჋")], self.config[bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ჌")])
                    })
                except Exception as e:
                    logger.debug(bstack11l111lll1_opy_.format(str(e)))
            bstack1ll1lll11ll_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1llll11111l_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1ll1ll1111l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
        self.bstack1ll1lll11l1_opy_, self.bstack1lll1ll11l1_opy_ = bstack1lll1111lll_opy_(data.bs_config)
        os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡ࡚ࡖࡎ࡚ࡁࡃࡎࡈࡣࡉࡏࡒࠨჍ")] = self.bstack1lll1ll11l1_opy_
        if not self.bstack1ll1lll11l1_opy_ or not self.bstack1lll1ll11l1_opy_:
            raise ValueError(bstack111l111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠣࡦ࡮ࡴࡡࡳࡻࠥ჎"))
        if self.bstack1l1l1lll1l_opy_():
            self.__1lll11l1111_opy_(event_name, bstack1l11ll1l11_opy_())
            return
        try:
            bstack1llll1111l1_opy_.end(EVENTS.bstack1ll11l11l1_opy_.value, EVENTS.bstack1ll11l11l1_opy_.value + bstack111l111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ჏"), EVENTS.bstack1ll11l11l1_opy_.value + bstack111l111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦა"), status=True, failure=None, test_name=None)
            logger.debug(bstack111l111_opy_ (u"ࠢࡄࡱࡰࡴࡱ࡫ࡴࡦࠢࡖࡈࡐࠦࡓࡦࡶࡸࡴ࠳ࠨბ"))
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡾࢁࠧგ").format(e))
        start = datetime.now()
        is_started = self.__1ll1l1lll11_opy_()
        self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠤࡶࡴࡦࡽ࡮ࡠࡶ࡬ࡱࡪࠨდ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lll1111l1l_opy_()
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤე"), datetime.now() - start)
            start = datetime.now()
            self.__1lll1l1l111_opy_(data)
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤვ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll1l1l1l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1lll11l1111_opy_(self, event_name: str, data: bstack1l11ll1l11_opy_):
        if not self.bstack1l1l1lll1l_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡲࡳ࡫ࡣࡵ࠼ࠣࡲࡴࡺࠠࡢࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤზ"))
            return
        bin_session_id = os.environ.get(bstack1lll1111ll1_opy_)
        start = datetime.now()
        self.__1lll1111l1l_opy_()
        self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧთ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack111l111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠣࡸࡴࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡅࡏࡍࠥࠨი") + str(bin_session_id) + bstack111l111_opy_ (u"ࠣࠤკ"))
        start = datetime.now()
        self.__1lll1l111l1_opy_()
        self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢლ"), datetime.now() - start)
    def __1lll1llll11_opy_(self):
        if not self.bstack1lll1l11l1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡧࡦࡴ࡮ࡰࡶࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦ࡭ࡰࡦࡸࡰࡪࡹࠢმ"))
            return
        bstack1lll111ll1l_opy_ = {
            bstack111l111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣნ"): (bstack1lll1lll1l1_opy_, bstack1ll1lll111l_opy_, bstack1ll1llll11l_opy_),
            bstack111l111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢო"): (bstack1lll1l1lll1_opy_, bstack1ll1ll1ll1l_opy_, bstack1lll1l11l11_opy_),
        }
        if not self.bstack1lll1l1ll1l_opy_ and self.session_framework in bstack1lll111ll1l_opy_:
            bstack1lll11llll1_opy_, bstack1lll1l11ll1_opy_, bstack1llll1l11l1_opy_ = bstack1lll111ll1l_opy_[self.session_framework]
            bstack1ll1lllll11_opy_ = bstack1lll1l11ll1_opy_()
            self.bstack1ll1ll1ll11_opy_ = bstack1ll1lllll11_opy_
            self.bstack1lll1l1ll1l_opy_ = bstack1llll1l11l1_opy_
            self.bstack1ll1l1ll11l_opy_.append(bstack1ll1lllll11_opy_)
            self.bstack1ll1l1ll11l_opy_.append(bstack1lll11llll1_opy_(self.bstack1ll1ll1ll11_opy_))
        if not self.bstack1lll1ll1ll1_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1l1ll1l1_opy_
            self.bstack1lll1ll1ll1_opy_ = bstack1lll111l11l_opy_(self.bstack1lll1l1ll1l_opy_, self.bstack1ll1ll1ll11_opy_) # bstack1lll1ll111l_opy_
            self.bstack1ll1l1ll11l_opy_.append(self.bstack1lll1ll1ll1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll11ll11l_opy_(self.bstack1lll1l1ll1l_opy_, self.bstack1ll1ll1ll11_opy_)
            self.bstack1ll1l1ll11l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack111l111_opy_ (u"ࠨࡳࡦ࡮ࡩࡌࡪࡧ࡬ࠣპ"), False) == True:
            self.ai = bstack1lll111111l_opy_()
            self.bstack1ll1l1ll11l_opy_.append(self.ai)
        if not self.percy and self.bstack1lll11l1ll1_opy_ and self.bstack1lll11l1ll1_opy_.success:
            self.percy = bstack1ll1ll11ll1_opy_(self.bstack1lll11l1ll1_opy_)
            self.bstack1ll1l1ll11l_opy_.append(self.percy)
        for mod in self.bstack1ll1l1ll11l_opy_:
            if not mod.bstack1ll1ll111l1_opy_():
                mod.configure(self.bstack1lll1l11l1l_opy_, self.config, self.cli_bin_session_id, self.bstack1111111lll_opy_)
    def __1lll1l1l1ll_opy_(self):
        for mod in self.bstack1ll1l1ll11l_opy_:
            if mod.bstack1ll1ll111l1_opy_():
                mod.configure(self.bstack1lll1l11l1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1lll1111_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1lll1l1l111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1llll1ll_opy_:
            return
        self.__1lll1lll1ll_opy_(data)
        bstack1l1111lll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack111l111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢჟ")
        req.sdk_language = bstack111l111_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣრ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll11l1lll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack111l111_opy_ (u"ࠤ࡞ࠦს") + str(id(self)) + bstack111l111_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤტ"))
            r = self.bstack1lll1l11l1l_opy_.StartBinSession(req)
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨუ"), datetime.now() - bstack1l1111lll_opy_)
            os.environ[bstack1lll1111ll1_opy_] = r.bin_session_id
            self.__1llll111l11_opy_(r)
            self.__1lll1llll11_opy_()
            self.bstack1111111lll_opy_.start()
            self.bstack1ll1llll1ll_opy_ = True
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡡࠢფ") + str(id(self)) + bstack111l111_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦქ"))
        except grpc.bstack1ll1ll1l11l_opy_ as bstack1lll1llllll_opy_:
            self.logger.error(bstack111l111_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤღ") + str(bstack1lll1llllll_opy_) + bstack111l111_opy_ (u"ࠣࠤყ"))
            traceback.print_exc()
            raise bstack1lll1llllll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨშ") + str(e) + bstack111l111_opy_ (u"ࠥࠦჩ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll11lllll_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1lll1l111l1_opy_(self):
        if not self.bstack1l1l1lll1l_opy_() or not self.cli_bin_session_id or self.bstack1llll111l1l_opy_:
            return
        bstack1l1111lll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫც"), bstack111l111_opy_ (u"ࠬ࠶ࠧძ")))
        try:
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡛ࠣწ") + str(id(self)) + bstack111l111_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჭ"))
            r = self.bstack1lll1l11l1l_opy_.ConnectBinSession(req)
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧხ"), datetime.now() - bstack1l1111lll_opy_)
            self.__1llll111l11_opy_(r)
            self.__1lll1llll11_opy_()
            self.bstack1111111lll_opy_.start()
            self.bstack1llll111l1l_opy_ = True
            self.logger.debug(bstack111l111_opy_ (u"ࠤ࡞ࠦჯ") + str(id(self)) + bstack111l111_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤჰ"))
        except grpc.bstack1ll1ll1l11l_opy_ as bstack1lll1llllll_opy_:
            self.logger.error(bstack111l111_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨჱ") + str(bstack1lll1llllll_opy_) + bstack111l111_opy_ (u"ࠧࠨჲ"))
            traceback.print_exc()
            raise bstack1lll1llllll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥჳ") + str(e) + bstack111l111_opy_ (u"ࠢࠣჴ"))
            traceback.print_exc()
            raise e
    def __1llll111l11_opy_(self, r):
        self.bstack1lll1ll11ll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack111l111_opy_ (u"ࠣࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠢჵ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack111l111_opy_ (u"ࠤࡨࡱࡵࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡹࡳࡪࠢჶ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack111l111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡧࡵࡧࡾࠦࡩࡴࠢࡶࡩࡳࡺࠠࡰࡰ࡯ࡽࠥࡧࡳࠡࡲࡤࡶࡹࠦ࡯ࡧࠢࡷ࡬ࡪࠦࠢࡄࡱࡱࡲࡪࡩࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠰ࠧࠦࡡ࡯ࡦࠣࡸ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡡ࡭ࡵࡲࠤࡺࡹࡥࡥࠢࡥࡽ࡙ࠥࡴࡢࡴࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬ࡪࡸࡥࡧࡱࡵࡩ࠱ࠦࡎࡰࡰࡨࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡩࡴࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧჷ")
        self.bstack1lll11l1ll1_opy_ = getattr(r, bstack111l111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪჸ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩჹ")] = self.config_testhub.jwt
        os.environ[bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫჺ")] = self.config_testhub.build_hashed_id
    def bstack1ll1ll1l111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll1ll1111_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll11l1l11_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll11l1l11_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll1ll1l111_opy_(event_name=EVENTS.bstack1ll1ll11lll_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1ll1l1lll11_opy_(self, bstack1lll11l111l_opy_=10):
        if self.bstack1lll1ll1111_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡴࡶࡤࡶࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡴࡸࡲࡳ࡯࡮ࡨࠤ჻"))
            return True
        self.logger.debug(bstack111l111_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢჼ"))
        if os.getenv(bstack111l111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡋࡎࡗࠤჽ")) == bstack1llll1l11ll_opy_:
            self.cli_bin_session_id = bstack1llll1l11ll_opy_
            self.cli_listen_addr = bstack111l111_opy_ (u"ࠥࡹࡳ࡯ࡸ࠻࠱ࡷࡱࡵ࠵ࡳࡥ࡭࠰ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࠫࡳ࠯ࡵࡲࡧࡰࠨჾ") % (self.cli_bin_session_id)
            self.bstack1lll1ll1111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1ll1lll11l1_opy_, bstack111l111_opy_ (u"ࠦࡸࡪ࡫ࠣჿ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1llll11l111_opy_ compat for text=True in bstack1lll1l1l11l_opy_ python
            encoding=bstack111l111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᄀ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1ll11l11_opy_ = threading.Thread(target=self.__1llll111111_opy_, args=(bstack1lll11l111l_opy_,))
        bstack1ll1ll11l11_opy_.start()
        bstack1ll1ll11l11_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡹࡰࡢࡹࡱ࠾ࠥࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࢃࠠࡰࡷࡷࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡸࡺࡤࡰࡷࡷ࠲ࡷ࡫ࡡࡥࠪࠬࢁࠥ࡫ࡲࡳ࠿ࠥᄁ") + str(self.process.stderr.read()) + bstack111l111_opy_ (u"ࠢࠣᄂ"))
        if not self.bstack1lll1ll1111_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠣ࡝ࠥᄃ") + str(id(self)) + bstack111l111_opy_ (u"ࠤࡠࠤࡨࡲࡥࡢࡰࡸࡴࠧᄄ"))
            self.__1lll1lll11l_opy_()
        self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡳࡶࡴࡩࡥࡴࡵࡢࡶࡪࡧࡤࡺ࠼ࠣࠦᄅ") + str(self.bstack1lll1ll1111_opy_) + bstack111l111_opy_ (u"ࠦࠧᄆ"))
        return self.bstack1lll1ll1111_opy_
    def __1llll111111_opy_(self, bstack1lll1ll1l11_opy_=10):
        bstack1llll11l1l1_opy_ = time.time()
        while self.process and time.time() - bstack1llll11l1l1_opy_ < bstack1lll1ll1l11_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack111l111_opy_ (u"ࠧ࡯ࡤ࠾ࠤᄇ") in line:
                    self.cli_bin_session_id = line.split(bstack111l111_opy_ (u"ࠨࡩࡥ࠿ࠥᄈ"))[-1:][0].strip()
                    self.logger.debug(bstack111l111_opy_ (u"ࠢࡤ࡮࡬ࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨ࠿ࠨᄉ") + str(self.cli_bin_session_id) + bstack111l111_opy_ (u"ࠣࠤᄊ"))
                    continue
                if bstack111l111_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᄋ") in line:
                    self.cli_listen_addr = line.split(bstack111l111_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦᄌ"))[-1:][0].strip()
                    self.logger.debug(bstack111l111_opy_ (u"ࠦࡨࡲࡩࡠ࡮࡬ࡷࡹ࡫࡮ࡠࡣࡧࡨࡷࡀࠢᄍ") + str(self.cli_listen_addr) + bstack111l111_opy_ (u"ࠧࠨᄎ"))
                    continue
                if bstack111l111_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᄏ") in line:
                    port = line.split(bstack111l111_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨᄐ"))[-1:][0].strip()
                    self.logger.debug(bstack111l111_opy_ (u"ࠣࡲࡲࡶࡹࡀࠢᄑ") + str(port) + bstack111l111_opy_ (u"ࠤࠥᄒ"))
                    continue
                if line.strip() == bstack1llll11ll1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack111l111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡌࡓࡤ࡙ࡔࡓࡇࡄࡑࠧᄓ"), bstack111l111_opy_ (u"ࠦ࠶ࠨᄔ")) == bstack111l111_opy_ (u"ࠧ࠷ࠢᄕ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1ll1111_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack111l111_opy_ (u"ࠨࡥࡳࡴࡲࡶ࠿ࠦࠢᄖ") + str(e) + bstack111l111_opy_ (u"ࠢࠣᄗ"))
        return False
    @measure(event_name=EVENTS.bstack1lll111l1ll_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def __1lll1lll11l_opy_(self):
        if self.bstack1llll1l1lll_opy_:
            self.bstack1111111lll_opy_.stop()
            start = datetime.now()
            if self.bstack1lll1l1ll11_opy_():
                self.cli_bin_session_id = None
                if self.bstack1llll111l1l_opy_:
                    self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᄘ"), datetime.now() - start)
                else:
                    self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᄙ"), datetime.now() - start)
            self.__1lll1l1l1ll_opy_()
            start = datetime.now()
            self.bstack1llll1l1lll_opy_.close()
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥࡨ࡮ࡹࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧᄚ"), datetime.now() - start)
            self.bstack1llll1l1lll_opy_ = None
        if self.process:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡸࡺ࡯ࡱࠤᄛ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧࡱࡩ࡭࡮ࡢࡸ࡮ࡳࡥࠣᄜ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll1ll1l1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1llllllll_opy_()
                self.logger.info(
                    bstack111l111_opy_ (u"ࠨࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤᄝ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack111l111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᄞ")] = self.config_testhub.build_hashed_id
        self.bstack1lll1ll1111_opy_ = False
    def __1lll1lll1ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack111l111_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᄟ")] = selenium.__version__
            data.frameworks.append(bstack111l111_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᄠ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack111l111_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᄡ")] = __version__
            data.frameworks.append(bstack111l111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᄢ"))
        except:
            pass
    def bstack1lll11lll1l_opy_(self, hub_url: str, platform_index: int, bstack1l11l1ll1l_opy_: Any):
        if self.bstack1llll1lll1l_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡶࡩࡹࠦࡵࡱࠤᄣ"))
            return
        try:
            bstack1l1111lll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack111l111_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᄤ")
            self.bstack1llll1lll1l_opy_ = bstack1lll1l11l11_opy_(
                cli.config.get(bstack111l111_opy_ (u"ࠢࡩࡷࡥ࡙ࡷࡲࠢᄥ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1ll1l1l1_opy_={bstack111l111_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧᄦ"): bstack1l11l1ll1l_opy_}
            )
            def bstack1lll11lll11_opy_(self):
                return
            if self.config.get(bstack111l111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦᄧ"), True):
                Service.start = bstack1lll11lll11_opy_
                Service.stop = bstack1lll11lll11_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1lll1ll1ll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll111l111_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᄨ"), datetime.now() - bstack1l1111lll_opy_)
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥᄩ") + str(e) + bstack111l111_opy_ (u"ࠧࠨᄪ"))
    def bstack1ll1lll1ll1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1lll11l1_opy_
            self.bstack1llll1lll1l_opy_ = bstack1ll1llll11l_opy_(
                platform_index,
                framework_name=bstack111l111_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᄫ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣᄬ") + str(e) + bstack111l111_opy_ (u"ࠣࠤᄭ"))
            pass
    def bstack1lll11l11l1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦᄮ"))
            return
        if bstack11l1l11l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack111l111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᄯ"): pytest.__version__ }, [bstack111l111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᄰ")], self.bstack1111111lll_opy_, self.bstack1lll1l11l1l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1lll1l111ll_opy_({ bstack111l111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᄱ"): pytest.__version__ }, [bstack111l111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᄲ")], self.bstack1111111lll_opy_, self.bstack1lll1l11l1l_opy_)
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦᄳ") + str(e) + bstack111l111_opy_ (u"ࠣࠤᄴ"))
        self.bstack1ll1llllll1_opy_()
    def bstack1ll1llllll1_opy_(self):
        if not self.bstack1lllll1lll_opy_():
            return
        bstack1l1lll11l_opy_ = None
        def bstack11ll11ll1l_opy_(config, startdir):
            return bstack111l111_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢᄵ").format(bstack111l111_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᄶ"))
        def bstack1l111l1ll_opy_():
            return
        def bstack1l11111ll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack111l111_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫᄷ"):
                return bstack111l111_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦᄸ")
            else:
                return bstack1l1lll11l_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1l1lll11l_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11ll11ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l111l1ll_opy_
            Config.getoption = bstack1l11111ll_opy_
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣᄹ") + str(e) + bstack111l111_opy_ (u"ࠢࠣᄺ"))
    def bstack1lll1l11111_opy_(self):
        bstack11l1111l11_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack11l1111l11_opy_, dict):
            if cli.config_observability:
                bstack11l1111l11_opy_.update(
                    {bstack111l111_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣᄻ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack111l111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧᄼ") in accessibility.get(bstack111l111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᄽ"), {}):
                    bstack1lll11l1l1l_opy_ = accessibility.get(bstack111l111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᄾ"))
                    bstack1lll11l1l1l_opy_.update({ bstack111l111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨᄿ"): bstack1lll11l1l1l_opy_.pop(bstack111l111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᅀ")) })
                bstack11l1111l11_opy_.update({bstack111l111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᅁ"): accessibility })
        return bstack11l1111l11_opy_
    @measure(event_name=EVENTS.bstack1lll1l11lll_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1lll1l1ll11_opy_(self, bstack1llll11ll11_opy_: str = None, bstack1lll11ll1l1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll1l11l1l_opy_:
            return
        bstack1l1111lll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1llll11ll11_opy_:
            req.bstack1llll11ll11_opy_ = bstack1llll11ll11_opy_
        if bstack1lll11ll1l1_opy_:
            req.bstack1lll11ll1l1_opy_ = bstack1lll11ll1l1_opy_
        try:
            r = self.bstack1lll1l11l1l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᅂ"), datetime.now() - bstack1l1111lll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack111111l1_opy_(self, key: str, value: timedelta):
        tag = bstack111l111_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᅃ") if self.bstack1l1l1lll1l_opy_() else bstack111l111_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤᅄ")
        self.bstack1ll1lllllll_opy_[bstack111l111_opy_ (u"ࠦ࠿ࠨᅅ").join([tag + bstack111l111_opy_ (u"ࠧ࠳ࠢᅆ") + str(id(self)), key])] += value
    def bstack1llllllll_opy_(self):
        if not os.getenv(bstack111l111_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥᅇ"), bstack111l111_opy_ (u"ࠢ࠱ࠤᅈ")) == bstack111l111_opy_ (u"ࠣ࠳ࠥᅉ"):
            return
        bstack1lll11111ll_opy_ = dict()
        bstack1lllll1llll_opy_ = []
        if self.test_framework:
            bstack1lllll1llll_opy_.extend(list(self.test_framework.bstack1lllll1llll_opy_.values()))
        if self.bstack1llll1lll1l_opy_:
            bstack1lllll1llll_opy_.extend(list(self.bstack1llll1lll1l_opy_.bstack1lllll1llll_opy_.values()))
        for instance in bstack1lllll1llll_opy_:
            if not instance.platform_index in bstack1lll11111ll_opy_:
                bstack1lll11111ll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll11111ll_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1l1lllll_opy_().items():
                report[k] += v
                report[k.split(bstack111l111_opy_ (u"ࠤ࠽ࠦᅊ"))[0]] += v
        bstack1llll1l1ll1_opy_ = sorted([(k, v) for k, v in self.bstack1ll1lllllll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1llll1l1_opy_ = 0
        for r in bstack1llll1l1ll1_opy_:
            bstack1llll11llll_opy_ = r[1].total_seconds()
            bstack1ll1llll1l1_opy_ += bstack1llll11llll_opy_
            self.logger.debug(bstack111l111_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣᅋ") + str(bstack1llll11llll_opy_) + bstack111l111_opy_ (u"ࠦࠧᅌ"))
        self.logger.debug(bstack111l111_opy_ (u"ࠧ࠳࠭ࠣᅍ"))
        bstack1ll1lllll1l_opy_ = []
        for platform_index, report in bstack1lll11111ll_opy_.items():
            bstack1ll1lllll1l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1lllll1l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1lllll11ll_opy_ = set()
        bstack1ll1l1ll1ll_opy_ = 0
        for r in bstack1ll1lllll1l_opy_:
            bstack1llll11llll_opy_ = r[2].total_seconds()
            bstack1ll1l1ll1ll_opy_ += bstack1llll11llll_opy_
            bstack1lllll11ll_opy_.add(r[0])
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢᅎ") + str(bstack1llll11llll_opy_) + bstack111l111_opy_ (u"ࠢࠣᅏ"))
        if self.bstack1l1l1lll1l_opy_():
            self.logger.debug(bstack111l111_opy_ (u"ࠣ࠯࠰ࠦᅐ"))
            self.logger.debug(bstack111l111_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤᅑ") + str(bstack1ll1l1ll1ll_opy_) + bstack111l111_opy_ (u"ࠥࠦᅒ"))
        else:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣᅓ") + str(bstack1ll1llll1l1_opy_) + bstack111l111_opy_ (u"ࠧࠨᅔ"))
        self.logger.debug(bstack111l111_opy_ (u"ࠨ࠭࠮ࠤᅕ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1lll1l11l1l_opy_:
            self.logger.error(bstack111l111_opy_ (u"ࠢࡤ࡮࡬ࡣࡸ࡫ࡲࡷ࡫ࡦࡩࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡈࡧ࡮࡯ࡱࡷࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᅖ"))
            return None
        response = self.bstack1lll1l11l1l_opy_.TestOrchestration(request)
        self.logger.debug(bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹ࠳࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠳ࡳࡦࡵࡶ࡭ࡴࡴ࠽ࡼࡿࠥᅗ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1lll1ll11ll_opy_(self, r):
        if r is not None and getattr(r, bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࠪᅘ"), None) and getattr(r.testhub, bstack111l111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᅙ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack111l111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᅚ")))
            for bstack1lll1lll111_opy_, err in errors.items():
                if err[bstack111l111_opy_ (u"ࠬࡺࡹࡱࡧࠪᅛ")] == bstack111l111_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᅜ"):
                    self.logger.info(err[bstack111l111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅝ")])
                else:
                    self.logger.error(err[bstack111l111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅞ")])
    def bstack11l1l1l1_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()