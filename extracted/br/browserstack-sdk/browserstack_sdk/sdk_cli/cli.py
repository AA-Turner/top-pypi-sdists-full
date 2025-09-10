# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1ll11lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll1l111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111ll_opy_ import bstack1llll1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1lll1111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1ll1l1l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1l_opy_ import bstack1111ll1l_opy_, bstack11l1lll1l_opy_, bstack1l1llllll_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll11l111l_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1llllll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1111_opy_ import bstack1lll1lll111_opy_
from bstack_utils.helper import Notset, bstack1lll1ll11ll_opy_, get_cli_dir, bstack1llll11111l_opy_, bstack1llll1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll1ll11l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack11ll1lll11_opy_ import bstack111lll1ll_opy_
from bstack_utils.helper import Notset, bstack1lll1ll11ll_opy_, get_cli_dir, bstack1llll11111l_opy_, bstack1llll1l11_opy_, bstack1lllll1111_opy_, bstack11l111l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1ll11_opy_, bstack1lll11ll1l1_opy_, bstack1ll1lllll11_opy_, bstack1ll1l1l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1llll1ll111_opy_, bstack1lllll1l111_opy_, bstack1lllll111ll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1l1lll11l_opy_ import bstack11ll11111_opy_
from bstack_utils import bstack1lll1llll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l11llll_opy_, bstack1ll1ll11_opy_
logger = bstack1lll1llll_opy_.get_logger(__name__, bstack1lll1llll_opy_.bstack1lll1l1ll1l_opy_())
def bstack1lll11l11ll_opy_(bs_config):
    bstack1lll1l1l1l1_opy_ = None
    bstack1lll1ll1l11_opy_ = None
    try:
        bstack1lll1ll1l11_opy_ = get_cli_dir()
        bstack1lll1l1l1l1_opy_ = bstack1llll11111l_opy_(bstack1lll1ll1l11_opy_)
        bstack1lll11111ll_opy_ = bstack1lll1ll11ll_opy_(bstack1lll1l1l1l1_opy_, bstack1lll1ll1l11_opy_, bs_config)
        bstack1lll1l1l1l1_opy_ = bstack1lll11111ll_opy_ if bstack1lll11111ll_opy_ else bstack1lll1l1l1l1_opy_
        if not bstack1lll1l1l1l1_opy_:
            raise ValueError(bstack1ll11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠣႫ"))
    except Exception as ex:
        logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡲࡡࡵࡧࡶࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࢁࡽࠣႬ").format(ex))
        bstack1lll1l1l1l1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤႭ"))
        if bstack1lll1l1l1l1_opy_:
            logger.debug(bstack1ll11ll_opy_ (u"ࠢࡇࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠦࡴࡰࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠥ࡬ࡲࡰ࡯ࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠻ࠢࠥႮ") + str(bstack1lll1l1l1l1_opy_) + bstack1ll11ll_opy_ (u"ࠣࠤႯ"))
        else:
            logger.debug(bstack1ll11ll_opy_ (u"ࠤࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠻ࠡࡵࡨࡸࡺࡶࠠ࡮ࡣࡼࠤࡧ࡫ࠠࡪࡰࡦࡳࡲࡶ࡬ࡦࡶࡨ࠲ࠧႰ"))
    return bstack1lll1l1l1l1_opy_, bstack1lll1ll1l11_opy_
bstack1ll1l1ll11l_opy_ = bstack1ll11ll_opy_ (u"ࠥ࠽࠾࠿࠹ࠣႱ")
bstack1lll111llll_opy_ = bstack1ll11ll_opy_ (u"ࠦࡷ࡫ࡡࡥࡻࠥႲ")
bstack1lll11l1l1l_opy_ = bstack1ll11ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤႳ")
bstack1ll1ll11l11_opy_ = bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡌࡊࡕࡗࡉࡓࡥࡁࡅࡆࡕࠦႴ")
bstack11l1ll11l_opy_ = bstack1ll11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠥႵ")
bstack1lll1l1lll1_opy_ = re.compile(bstack1ll11ll_opy_ (u"ࡳࠤࠫࡃ࡮࠯࠮ࠫࠪࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡽࡄࡖ࠭࠳࠰ࠢႶ"))
bstack1ll1ll1ll11_opy_ = bstack1ll11ll_opy_ (u"ࠤࡧࡩࡻ࡫࡬ࡰࡲࡰࡩࡳࡺࠢႷ")
bstack1ll1ll111ll_opy_ = [
    bstack11l1lll1l_opy_.bstack1l1l111111_opy_,
    bstack11l1lll1l_opy_.CONNECT,
    bstack11l1lll1l_opy_.bstack1l111l1lll_opy_,
]
class SDKCLI:
    _1lll111l11l_opy_ = None
    process: Union[None, Any]
    bstack1ll1l1lll11_opy_: bool
    bstack1lll11lll11_opy_: bool
    bstack1lll111ll11_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1ll1llll1l1_opy_: Union[None, grpc.Channel]
    bstack1llll111l1l_opy_: str
    test_framework: TestFramework
    bstack1lllll1l1ll_opy_: bstack1llllll1111_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll1l11ll1_opy_: bstack1lll1lll1l1_opy_
    accessibility: bstack1ll1ll11lll_opy_
    bstack11ll1lll11_opy_: bstack111lll1ll_opy_
    ai: bstack1lll1l111l1_opy_
    bstack1lll1ll1ll1_opy_: bstack1llll1111l1_opy_
    bstack1lll1ll1lll_opy_: List[bstack1ll1l1l11l1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1ll1111_opy_: Any
    bstack1lll111111l_opy_: Dict[str, timedelta]
    bstack1lll111l1ll_opy_: str
    bstack1111111ll1_opy_: bstack11111111ll_opy_
    def __new__(cls):
        if not cls._1lll111l11l_opy_:
            cls._1lll111l11l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll111l11l_opy_
    def __init__(self):
        self.process = None
        self.bstack1ll1l1lll11_opy_ = False
        self.bstack1ll1llll1l1_opy_ = None
        self.bstack1ll1llllll1_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1ll11l11_opy_, None)
        self.bstack1ll1ll1llll_opy_ = os.environ.get(bstack1lll11l1l1l_opy_, bstack1ll11ll_opy_ (u"ࠥࠦႸ")) == bstack1ll11ll_opy_ (u"ࠦࠧႹ")
        self.bstack1lll11lll11_opy_ = False
        self.bstack1lll111ll11_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1ll1111_opy_ = None
        self.test_framework = None
        self.bstack1lllll1l1ll_opy_ = None
        self.bstack1llll111l1l_opy_=bstack1ll11ll_opy_ (u"ࠧࠨႺ")
        self.session_framework = None
        self.logger = bstack1lll1llll_opy_.get_logger(self.__class__.__name__, bstack1lll1llll_opy_.bstack1lll1l1ll1l_opy_())
        self.bstack1lll111111l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111111ll1_opy_ = bstack11111111ll_opy_()
        self.bstack1ll1lll1l1l_opy_ = None
        self.bstack1ll1ll1l1l1_opy_ = None
        self.bstack1lll1l11ll1_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll1ll1lll_opy_ = []
    def bstack11l1lll1ll_opy_(self):
        return os.environ.get(bstack11l1ll11l_opy_).lower().__eq__(bstack1ll11ll_opy_ (u"ࠨࡴࡳࡷࡨࠦႻ"))
    def is_enabled(self, config):
        if bstack1ll11ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫႼ") in config and str(config[bstack1ll11ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬႽ")]).lower() != bstack1ll11ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨႾ"):
            return False
        bstack1lll1llll11_opy_ = [bstack1ll11ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥႿ"), bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣჀ")]
        bstack1lll1llll1l_opy_ = config.get(bstack1ll11ll_opy_ (u"ࠧ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣჁ")) in bstack1lll1llll11_opy_ or os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧჂ")) in bstack1lll1llll11_opy_
        os.environ[bstack1ll11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥჃ")] = str(bstack1lll1llll1l_opy_) # bstack1lll1lll1ll_opy_ bstack1lll11lllll_opy_ VAR to bstack1llll11lll1_opy_ is binary running
        return bstack1lll1llll1l_opy_
    def bstack111l11ll1_opy_(self):
        for event in bstack1ll1ll111ll_opy_:
            bstack1111ll1l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1111ll1l_opy_.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠠ࠾ࡀࠣࡿࡦࡸࡧࡴࡿࠣࠦჄ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠤࠥჅ"))
            )
        bstack1111ll1l_opy_.register(bstack11l1lll1l_opy_.bstack1l1l111111_opy_, self.__1lll11l1lll_opy_)
        bstack1111ll1l_opy_.register(bstack11l1lll1l_opy_.CONNECT, self.__1lll11l1l11_opy_)
        bstack1111ll1l_opy_.register(bstack11l1lll1l_opy_.bstack1l111l1lll_opy_, self.__1ll1ll1111l_opy_)
        bstack1111ll1l_opy_.register(bstack11l1lll1l_opy_.bstack1ll1l1l1ll_opy_, self.__1lll1l11111_opy_)
    def bstack11l1l1l1ll_opy_(self):
        return not self.bstack1ll1ll1llll_opy_ and os.environ.get(bstack1lll11l1l1l_opy_, bstack1ll11ll_opy_ (u"ࠥࠦ჆")) != bstack1ll11ll_opy_ (u"ࠦࠧჇ")
    def is_running(self):
        if self.bstack1ll1ll1llll_opy_:
            return self.bstack1ll1l1lll11_opy_
        else:
            return bool(self.bstack1ll1llll1l1_opy_)
    def bstack1lll1lllll1_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll1ll1lll_opy_) and cli.is_running()
    def __1lll11lll1l_opy_(self, bstack1llll11llll_opy_=10):
        if self.bstack1ll1llllll1_opy_:
            return
        bstack1ll111l11_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1ll11l11_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡡࠢ჈") + str(id(self)) + bstack1ll11ll_opy_ (u"ࠨ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡱ࡫ࠧ჉"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1ll11ll_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡢࡴࡷࡵࡸࡺࠤ჊"), 0), (bstack1ll11ll_opy_ (u"ࠣࡩࡵࡴࡨ࠴ࡥ࡯ࡣࡥࡰࡪࡥࡨࡵࡶࡳࡷࡤࡶࡲࡰࡺࡼࠦ჋"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1llll11llll_opy_)
        self.bstack1ll1llll1l1_opy_ = channel
        self.bstack1ll1llllll1_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1ll1llll1l1_opy_)
        self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡤࡱࡱࡲࡪࡩࡴࠣ჌"), datetime.now() - bstack1ll111l11_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1ll11l11_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨ࠿ࠦࡩࡴࡡࡦ࡬࡮ࡲࡤࡠࡲࡵࡳࡨ࡫ࡳࡴ࠿ࠥჍ") + str(self.bstack11l1l1l1ll_opy_()) + bstack1ll11ll_opy_ (u"ࠦࠧ჎"))
    def __1ll1ll1111l_opy_(self, event_name):
        if self.bstack11l1l1l1ll_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡱࡳࡴ࡮ࡴࡧࠡࡅࡏࡍࠧ჏"))
        self.__1ll1llll11l_opy_()
    def __1lll1l11111_opy_(self, event_name, bstack1ll1l1ll1ll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠨა"))
        bstack1llll11l111_opy_ = Path(bstack1lll111ll1l_opy_ (u"ࠢࡼࡵࡨࡰ࡫࠴ࡣ࡭࡫ࡢࡨ࡮ࡸࡽ࠰ࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࡵ࠱࡮ࡸࡵ࡮ࠣბ"))
        if self.bstack1lll1ll1l11_opy_ and bstack1llll11l111_opy_.exists():
            with open(bstack1llll11l111_opy_, bstack1ll11ll_opy_ (u"ࠨࡴࠪგ"), encoding=bstack1ll11ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨდ")) as fp:
                data = json.load(fp)
                try:
                    bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨე"), bstack11ll11111_opy_(bstack111lll1lll_opy_), data, {
                        bstack1ll11ll_opy_ (u"ࠫࡦࡻࡴࡩࠩვ"): (self.config[bstack1ll11ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧზ")], self.config[bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩთ")])
                    })
                except Exception as e:
                    logger.debug(bstack1ll1ll11_opy_.format(str(e)))
            bstack1llll11l111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1ll1l1l1l1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1lll11l1lll_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
        self.bstack1llll111l1l_opy_, self.bstack1lll1ll1l11_opy_ = bstack1lll11l11ll_opy_(data.bs_config)
        os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡗࡓࡋࡗࡅࡇࡒࡅࡠࡆࡌࡖࠬი")] = self.bstack1lll1ll1l11_opy_
        if not self.bstack1llll111l1l_opy_ or not self.bstack1lll1ll1l11_opy_:
            raise ValueError(bstack1ll11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡇࡑࡏࠠࡣ࡫ࡱࡥࡷࡿࠢკ"))
        if self.bstack11l1l1l1ll_opy_():
            self.__1lll11l1l11_opy_(event_name, bstack1l1llllll_opy_())
            return
        try:
            bstack1ll1ll11ll1_opy_.end(EVENTS.bstack11ll1l111l_opy_.value, EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤლ"), EVENTS.bstack11ll1l111l_opy_.value + bstack1ll11ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣმ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1ll11ll_opy_ (u"ࠦࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦࡓࡅࡍࠣࡗࡪࡺࡵࡱ࠰ࠥნ"))
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡻࡾࠤო").format(e))
        start = datetime.now()
        is_started = self.__1lll1111lll_opy_()
        self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠨࡳࡱࡣࡺࡲࡤࡺࡩ࡮ࡧࠥპ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lll11lll1l_opy_()
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨჟ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1ll1l1ll_opy_(data)
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨრ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1ll1ll111l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1lll11l1l11_opy_(self, event_name: str, data: bstack1l1llllll_opy_):
        if not self.bstack11l1l1l1ll_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡯ࡰࡨࡧࡹࡀࠠ࡯ࡱࡷࠤࡦࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨს"))
            return
        bin_session_id = os.environ.get(bstack1lll11l1l1l_opy_)
        start = datetime.now()
        self.__1lll11lll1l_opy_()
        self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤტ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠠࡵࡱࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡉࡌࡊࠢࠥუ") + str(bin_session_id) + bstack1ll11ll_opy_ (u"ࠧࠨფ"))
        start = datetime.now()
        self.__1ll1lll111l_opy_()
        self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦქ"), datetime.now() - start)
    def __1lll1ll1l1l_opy_(self):
        if not self.bstack1ll1llllll1_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡤࡣࡱࡲࡴࡺࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࠣࡱࡴࡪࡵ࡭ࡧࡶࠦღ"))
            return
        bstack1ll1l1l11ll_opy_ = {
            bstack1ll11ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧყ"): (bstack1ll1l1l111l_opy_, bstack1lll1l1111l_opy_, bstack1lll1lll111_opy_),
            bstack1ll11ll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦშ"): (bstack1ll1lll1l11_opy_, bstack1lll1111ll1_opy_, bstack1ll1l1ll111_opy_),
        }
        if not self.bstack1ll1lll1l1l_opy_ and self.session_framework in bstack1ll1l1l11ll_opy_:
            bstack1llll111lll_opy_, bstack1lll1lll11l_opy_, bstack1llll111ll1_opy_ = bstack1ll1l1l11ll_opy_[self.session_framework]
            bstack1ll1l1l1l11_opy_ = bstack1lll1lll11l_opy_()
            self.bstack1ll1ll1l1l1_opy_ = bstack1ll1l1l1l11_opy_
            self.bstack1ll1lll1l1l_opy_ = bstack1llll111ll1_opy_
            self.bstack1lll1ll1lll_opy_.append(bstack1ll1l1l1l11_opy_)
            self.bstack1lll1ll1lll_opy_.append(bstack1llll111lll_opy_(self.bstack1ll1ll1l1l1_opy_))
        if not self.bstack1lll1l11ll1_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1l1llll1_opy_
            self.bstack1lll1l11ll1_opy_ = bstack1lll1lll1l1_opy_(self.bstack1ll1lll1l1l_opy_, self.bstack1ll1ll1l1l1_opy_) # bstack1ll1l1ll1l1_opy_
            self.bstack1lll1ll1lll_opy_.append(self.bstack1lll1l11ll1_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1ll1ll11lll_opy_(self.bstack1ll1lll1l1l_opy_, self.bstack1ll1ll1l1l1_opy_)
            self.bstack1lll1ll1lll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1ll11ll_opy_ (u"ࠥࡷࡪࡲࡦࡉࡧࡤࡰࠧჩ"), False) == True:
            self.ai = bstack1lll1l111l1_opy_()
            self.bstack1lll1ll1lll_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1ll1111_opy_ and self.bstack1lll1ll1111_opy_.success:
            self.percy = bstack1llll1111l1_opy_(self.bstack1lll1ll1111_opy_)
            self.bstack1lll1ll1lll_opy_.append(self.percy)
        for mod in self.bstack1lll1ll1lll_opy_:
            if not mod.bstack1llll11ll1l_opy_():
                mod.configure(self.bstack1ll1llllll1_opy_, self.config, self.cli_bin_session_id, self.bstack1111111ll1_opy_)
    def __1ll1lll1ll1_opy_(self):
        for mod in self.bstack1lll1ll1lll_opy_:
            if mod.bstack1llll11ll1l_opy_():
                mod.configure(self.bstack1ll1llllll1_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1ll1llll1ll_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1ll1ll1l1ll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll11lll11_opy_:
            return
        self.__1lll1l11l1l_opy_(data)
        bstack1ll111l11_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦც")
        req.sdk_language = bstack1ll11ll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧძ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll1l1lll1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡛ࠣწ") + str(id(self)) + bstack1ll11ll_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡶࡸࡦࡸࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨჭ"))
            r = self.bstack1ll1llllll1_opy_.StartBinSession(req)
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥხ"), datetime.now() - bstack1ll111l11_opy_)
            os.environ[bstack1lll11l1l1l_opy_] = r.bin_session_id
            self.__1lll1l1llll_opy_(r)
            self.__1lll1ll1l1l_opy_()
            self.bstack1111111ll1_opy_.start()
            self.bstack1lll11lll11_opy_ = True
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤ࡞ࠦჯ") + str(id(self)) + bstack1ll11ll_opy_ (u"ࠥࡡࠥࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣჰ"))
        except grpc.bstack1lll11llll1_opy_ as bstack1llll11l11l_opy_:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡸ࡮ࡳࡥࡰࡧࡸࡸ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨჱ") + str(bstack1llll11l11l_opy_) + bstack1ll11ll_opy_ (u"ࠧࠨჲ"))
            traceback.print_exc()
            raise bstack1llll11l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥჳ") + str(e) + bstack1ll11ll_opy_ (u"ࠢࠣჴ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll111l111_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1ll1lll111l_opy_(self):
        if not self.bstack11l1l1l1ll_opy_() or not self.cli_bin_session_id or self.bstack1lll111ll11_opy_:
            return
        bstack1ll111l11_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨჵ"), bstack1ll11ll_opy_ (u"ࠩ࠳ࠫჶ")))
        try:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡟ࠧჷ") + str(id(self)) + bstack1ll11ll_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨჸ"))
            r = self.bstack1ll1llllll1_opy_.ConnectBinSession(req)
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡧࡴࡴ࡮ࡦࡥࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჹ"), datetime.now() - bstack1ll111l11_opy_)
            self.__1lll1l1llll_opy_(r)
            self.__1lll1ll1l1l_opy_()
            self.bstack1111111ll1_opy_.start()
            self.bstack1lll111ll11_opy_ = True
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡛ࠣჺ") + str(id(self)) + bstack1ll11ll_opy_ (u"ࠢ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨ჻"))
        except grpc.bstack1lll11llll1_opy_ as bstack1llll11l11l_opy_:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥჼ") + str(bstack1llll11l11l_opy_) + bstack1ll11ll_opy_ (u"ࠤࠥჽ"))
            traceback.print_exc()
            raise bstack1llll11l11l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢჾ") + str(e) + bstack1ll11ll_opy_ (u"ࠦࠧჿ"))
            traceback.print_exc()
            raise e
    def __1lll1l1llll_opy_(self, r):
        self.bstack1lll1111111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1ll11ll_opy_ (u"ࠧࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᄀ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1ll11ll_opy_ (u"ࠨࡥ࡮ࡲࡷࡽࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡯ࡶࡰࡧࠦᄁ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1ll11ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕ࡫ࡲࡤࡻࠣ࡭ࡸࠦࡳࡦࡰࡷࠤࡴࡴ࡬ࡺࠢࡤࡷࠥࡶࡡࡳࡶࠣࡳ࡫ࠦࡴࡩࡧࠣࠦࡈࡵ࡮࡯ࡧࡦࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠭ࠤࠣࡥࡳࡪࠠࡵࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡪࡵࠣࡥࡱࡹ࡯ࠡࡷࡶࡩࡩࠦࡢࡺࠢࡖࡸࡦࡸࡴࡃ࡫ࡱࡗࡪࡹࡳࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࡵࡩ࡫ࡵࡲࡦ࠮ࠣࡒࡴࡴࡥࠡࡪࡤࡲࡩࡲࡩ࡯ࡩࠣ࡭ࡸࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᄂ")
        self.bstack1lll1ll1111_opy_ = getattr(r, bstack1ll11ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᄃ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᄄ")] = self.config_testhub.jwt
        os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᄅ")] = self.config_testhub.build_hashed_id
    def bstack1llll11ll11_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1ll1l1lll11_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llll111l11_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llll111l11_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1llll11ll11_opy_(event_name=EVENTS.bstack1ll1lll1lll_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1lll1111lll_opy_(self, bstack1llll11llll_opy_=10):
        if self.bstack1ll1l1lll11_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡸࡺࡡࡳࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨᄆ"))
            return True
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦᄇ"))
        if os.getenv(bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡈࡒ࡛ࠨᄈ")) == bstack1ll1ll1ll11_opy_:
            self.cli_bin_session_id = bstack1ll1ll1ll11_opy_
            self.cli_listen_addr = bstack1ll11ll_opy_ (u"ࠢࡶࡰ࡬ࡼ࠿࠵ࡴ࡮ࡲ࠲ࡷࡩࡱ࠭ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࠨࡷ࠳ࡹ࡯ࡤ࡭ࠥᄉ") % (self.cli_bin_session_id)
            self.bstack1ll1l1lll11_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1llll111l1l_opy_, bstack1ll11ll_opy_ (u"ࠣࡵࡧ࡯ࠧᄊ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll1llllll_opy_ compat for text=True in bstack1lll1111l11_opy_ python
            encoding=bstack1ll11ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᄋ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll1l11lll_opy_ = threading.Thread(target=self.__1llll1l111l_opy_, args=(bstack1llll11llll_opy_,))
        bstack1lll1l11lll_opy_.start()
        bstack1lll1l11lll_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡶࡴࡦࡽ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࡥࡲࡨࡪࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࢀࠤࡴࡻࡴ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡵࡷࡨࡴࡻࡴ࠯ࡴࡨࡥࡩ࠮ࠩࡾࠢࡨࡶࡷࡃࠢᄌ") + str(self.process.stderr.read()) + bstack1ll11ll_opy_ (u"ࠦࠧᄍ"))
        if not self.bstack1ll1l1lll11_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡡࠢᄎ") + str(id(self)) + bstack1ll11ll_opy_ (u"ࠨ࡝ࠡࡥ࡯ࡩࡦࡴࡵࡱࠤᄏ"))
            self.__1ll1llll11l_opy_()
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡰࡳࡱࡦࡩࡸࡹ࡟ࡳࡧࡤࡨࡾࡀࠠࠣᄐ") + str(self.bstack1ll1l1lll11_opy_) + bstack1ll11ll_opy_ (u"ࠣࠤᄑ"))
        return self.bstack1ll1l1lll11_opy_
    def __1llll1l111l_opy_(self, bstack1ll1ll1ll1l_opy_=10):
        bstack1lll1l1l1ll_opy_ = time.time()
        while self.process and time.time() - bstack1lll1l1l1ll_opy_ < bstack1ll1ll1ll1l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1ll11ll_opy_ (u"ࠤ࡬ࡨࡂࠨᄒ") in line:
                    self.cli_bin_session_id = line.split(bstack1ll11ll_opy_ (u"ࠥ࡭ࡩࡃࠢᄓ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡨࡲࡩࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠼ࠥᄔ") + str(self.cli_bin_session_id) + bstack1ll11ll_opy_ (u"ࠧࠨᄕ"))
                    continue
                if bstack1ll11ll_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢᄖ") in line:
                    self.cli_listen_addr = line.split(bstack1ll11ll_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣᄗ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡥ࡯࡭ࡤࡲࡩࡴࡶࡨࡲࡤࡧࡤࡥࡴ࠽ࠦᄘ") + str(self.cli_listen_addr) + bstack1ll11ll_opy_ (u"ࠤࠥᄙ"))
                    continue
                if bstack1ll11ll_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤᄚ") in line:
                    port = line.split(bstack1ll11ll_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥᄛ"))[-1:][0].strip()
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡶ࡯ࡳࡶ࠽ࠦᄜ") + str(port) + bstack1ll11ll_opy_ (u"ࠨࠢᄝ"))
                    continue
                if line.strip() == bstack1lll111llll_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1ll11ll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡉࡐࡡࡖࡘࡗࡋࡁࡎࠤᄞ"), bstack1ll11ll_opy_ (u"ࠣ࠳ࠥᄟ")) == bstack1ll11ll_opy_ (u"ࠤ࠴ࠦᄠ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1ll1l1lll11_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳ࠼ࠣࠦᄡ") + str(e) + bstack1ll11ll_opy_ (u"ࠦࠧᄢ"))
        return False
    @measure(event_name=EVENTS.bstack1lll111l1l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def __1ll1llll11l_opy_(self):
        if self.bstack1ll1llll1l1_opy_:
            self.bstack1111111ll1_opy_.stop()
            start = datetime.now()
            if self.bstack1ll1lllllll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll111ll11_opy_:
                    self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤᄣ"), datetime.now() - start)
                else:
                    self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥᄤ"), datetime.now() - start)
            self.__1ll1lll1ll1_opy_()
            start = datetime.now()
            self.bstack1ll1llll1l1_opy_.close()
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡥ࡫ࡶࡧࡴࡴ࡮ࡦࡥࡷࡣࡹ࡯࡭ࡦࠤᄥ"), datetime.now() - start)
            self.bstack1ll1llll1l1_opy_ = None
        if self.process:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡵࡷࡳࡵࠨᄦ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤ࡮࡭ࡱࡲ࡟ࡵ࡫ࡰࡩࠧᄧ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll1ll1llll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l11l1ll1l_opy_()
                self.logger.info(
                    bstack1ll11ll_opy_ (u"࡚ࠥ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠥᄨ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1ll11ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᄩ")] = self.config_testhub.build_hashed_id
        self.bstack1ll1l1lll11_opy_ = False
    def __1lll1l11l1l_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1ll11ll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᄪ")] = selenium.__version__
            data.frameworks.append(bstack1ll11ll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᄫ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1ll11ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᄬ")] = __version__
            data.frameworks.append(bstack1ll11ll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᄭ"))
        except:
            pass
    def bstack1llll1111ll_opy_(self, hub_url: str, platform_index: int, bstack1ll11111ll_opy_: Any):
        if self.bstack1lllll1l1ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡳࡦࡶࠣࡹࡵࠨᄮ"))
            return
        try:
            bstack1ll111l11_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1ll11ll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᄯ")
            self.bstack1lllll1l1ll_opy_ = bstack1ll1l1ll111_opy_(
                cli.config.get(bstack1ll11ll_opy_ (u"ࠦ࡭ࡻࡢࡖࡴ࡯ࠦᄰ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll1111l1l_opy_={bstack1ll11ll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤᄱ"): bstack1ll11111ll_opy_}
            )
            def bstack1lll11111l1_opy_(self):
                return
            if self.config.get(bstack1ll11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠣᄲ"), True):
                Service.start = bstack1lll11111l1_opy_
                Service.stop = bstack1lll11111l1_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack111lll1ll_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll1ll11l1_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᄳ"), datetime.now() - bstack1ll111l11_opy_)
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࠢᄴ") + str(e) + bstack1ll11ll_opy_ (u"ࠤࠥᄵ"))
    def bstack1lll1l1l11l_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack11111111l_opy_
            self.bstack1lllll1l1ll_opy_ = bstack1lll1lll111_opy_(
                platform_index,
                framework_name=bstack1ll11ll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᄶ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠽ࠤࠧᄷ") + str(e) + bstack1ll11ll_opy_ (u"ࠧࠨᄸ"))
            pass
    def bstack1lll1l11l11_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᄹ"))
            return
        if bstack1llll1l11_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1ll11ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᄺ"): pytest.__version__ }, [bstack1ll11ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᄻ")], self.bstack1111111ll1_opy_, self.bstack1ll1llllll1_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1llll111_opy_({ bstack1ll11ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᄼ"): pytest.__version__ }, [bstack1ll11ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᄽ")], self.bstack1111111ll1_opy_, self.bstack1ll1llllll1_opy_)
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࠣᄾ") + str(e) + bstack1ll11ll_opy_ (u"ࠧࠨᄿ"))
        self.bstack1ll1ll11111_opy_()
    def bstack1ll1ll11111_opy_(self):
        if not self.bstack11l1lll1ll_opy_():
            return
        bstack1ll1ll1111_opy_ = None
        def bstack11l111l1ll_opy_(config, startdir):
            return bstack1ll11ll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦᅀ").format(bstack1ll11ll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᅁ"))
        def bstack11l1ll1ll_opy_():
            return
        def bstack1l11l11l11_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1ll11ll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᅂ"):
                return bstack1ll11ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᅃ")
            else:
                return bstack1ll1ll1111_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1ll1ll1111_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l111l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11l1ll1ll_opy_
            Config.getoption = bstack1l11l11l11_opy_
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬ࠥࡶࡹࡵࡧࡶࡸࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠽ࠤࠧᅄ") + str(e) + bstack1ll11ll_opy_ (u"ࠦࠧᅅ"))
    def bstack1ll1ll1lll1_opy_(self):
        bstack1llll111ll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1llll111ll_opy_, dict):
            if cli.config_observability:
                bstack1llll111ll_opy_.update(
                    {bstack1ll11ll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᅆ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1ll11ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤᅇ") in accessibility.get(bstack1ll11ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᅈ"), {}):
                    bstack1lll11l1111_opy_ = accessibility.get(bstack1ll11ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᅉ"))
                    bstack1lll11l1111_opy_.update({ bstack1ll11ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠥᅊ"): bstack1lll11l1111_opy_.pop(bstack1ll11ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨᅋ")) })
                bstack1llll111ll_opy_.update({bstack1ll11ll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᅌ"): accessibility })
        return bstack1llll111ll_opy_
    @measure(event_name=EVENTS.bstack1llll11l1l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1ll1lllllll_opy_(self, bstack1ll1lllll1l_opy_: str = None, bstack1ll1ll1l111_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1llllll1_opy_:
            return
        bstack1ll111l11_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1ll1lllll1l_opy_:
            req.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_
        if bstack1ll1ll1l111_opy_:
            req.bstack1ll1ll1l111_opy_ = bstack1ll1ll1l111_opy_
        try:
            r = self.bstack1ll1llllll1_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡵࡰࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᅍ"), datetime.now() - bstack1ll111l11_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1lll1111l1_opy_(self, key: str, value: timedelta):
        tag = bstack1ll11ll_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᅎ") if self.bstack11l1l1l1ll_opy_() else bstack1ll11ll_opy_ (u"ࠢ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࠨᅏ")
        self.bstack1lll111111l_opy_[bstack1ll11ll_opy_ (u"ࠣ࠼ࠥᅐ").join([tag + bstack1ll11ll_opy_ (u"ࠤ࠰ࠦᅑ") + str(id(self)), key])] += value
    def bstack1l11l1ll1l_opy_(self):
        if not os.getenv(bstack1ll11ll_opy_ (u"ࠥࡈࡊࡈࡕࡈࡡࡓࡉࡗࡌࠢᅒ"), bstack1ll11ll_opy_ (u"ࠦ࠵ࠨᅓ")) == bstack1ll11ll_opy_ (u"ࠧ࠷ࠢᅔ"):
            return
        bstack1llll111111_opy_ = dict()
        bstack1lllllll111_opy_ = []
        if self.test_framework:
            bstack1lllllll111_opy_.extend(list(self.test_framework.bstack1lllllll111_opy_.values()))
        if self.bstack1lllll1l1ll_opy_:
            bstack1lllllll111_opy_.extend(list(self.bstack1lllll1l1ll_opy_.bstack1lllllll111_opy_.values()))
        for instance in bstack1lllllll111_opy_:
            if not instance.platform_index in bstack1llll111111_opy_:
                bstack1llll111111_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1llll111111_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1l1l1lll_opy_().items():
                report[k] += v
                report[k.split(bstack1ll11ll_opy_ (u"ࠨ࠺ࠣᅕ"))[0]] += v
        bstack1llll11l1ll_opy_ = sorted([(k, v) for k, v in self.bstack1lll111111l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll11ll11l_opy_ = 0
        for r in bstack1llll11l1ll_opy_:
            bstack1ll1ll11l1l_opy_ = r[1].total_seconds()
            bstack1lll11ll11l_opy_ += bstack1ll1ll11l1l_opy_
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࢀࡸ࡛࠱࡟ࢀࡁࠧᅖ") + str(bstack1ll1ll11l1l_opy_) + bstack1ll11ll_opy_ (u"ࠣࠤᅗ"))
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠤ࠰࠱ࠧᅘ"))
        bstack1lll11l1ll1_opy_ = []
        for platform_index, report in bstack1llll111111_opy_.items():
            bstack1lll11l1ll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll11l1ll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l111l1l_opy_ = set()
        bstack1lll111lll1_opy_ = 0
        for r in bstack1lll11l1ll1_opy_:
            bstack1ll1ll11l1l_opy_ = r[2].total_seconds()
            bstack1lll111lll1_opy_ += bstack1ll1ll11l1l_opy_
            bstack1l111l1l_opy_.add(r[0])
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࡿࡷࡡ࠰࡞ࡿ࠽ࡿࡷࡡ࠱࡞ࡿࡀࠦᅙ") + str(bstack1ll1ll11l1l_opy_) + bstack1ll11ll_opy_ (u"ࠦࠧᅚ"))
        if self.bstack11l1l1l1ll_opy_():
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧ࠳࠭ࠣᅛ"))
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࡀࡿࡹࡵࡴࡢ࡮ࡢࡧࡱ࡯ࡽࠡࡶࡨࡷࡹࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ࠯ࡾࡷࡹࡸࠨࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠬࢁࡂࠨᅜ") + str(bstack1lll111lll1_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣᅝ"))
        else:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࠧᅞ") + str(bstack1lll11ll11l_opy_) + bstack1ll11ll_opy_ (u"ࠤࠥᅟ"))
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࠱࠲ࠨᅠ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1ll1llllll1_opy_:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡨࡲࡩࡠࡵࡨࡶࡻ࡯ࡣࡦࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡅࡤࡲࡳࡵࡴࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣᅡ"))
            return None
        response = self.bstack1ll1llllll1_opy_.TestOrchestration(request)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶ࠰ࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠰ࡷࡪࡹࡳࡪࡱࡱࡁࢀࢃࠢᅢ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1lll1111111_opy_(self, r):
        if r is not None and getattr(r, bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨࠧᅣ"), None) and getattr(r.testhub, bstack1ll11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᅤ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1ll11ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᅥ")))
            for bstack1llll1l1111_opy_, err in errors.items():
                if err[bstack1ll11ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᅦ")] == bstack1ll11ll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᅧ"):
                    self.logger.info(err[bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅨ")])
                else:
                    self.logger.error(err[bstack1ll11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᅩ")])
    def bstack1ll1ll11ll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()