# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
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
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1ll1ll11lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1lll1_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import bstack1ll1l1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1ll1lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1lll_opy_ import bstack1ll1ll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1l1111l1_opy_ import bstack1l1111l1_opy_, bstack1l11lll111_opy_, bstack1ll1111l1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import bstack1llllllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1ll1l1lllll_opy_
from bstack_utils.helper import Notset, bstack1lll11ll11l_opy_, get_cli_dir, bstack1lll1lllll1_opy_, bstack1l11llll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1l1ll1_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack1111l1l11_opy_
from bstack_utils.helper import Notset, bstack1lll11ll11l_opy_, get_cli_dir, bstack1lll1lllll1_opy_, bstack1l11llll11_opy_, bstack1l1ll1ll1l_opy_, bstack1ll1l1ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1lll11l1111_opy_, bstack1lll111l1l1_opy_, bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import bstack1lllllll111_opy_, bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_
from bstack_utils.constants import *
from bstack_utils.bstack11l1l111l1_opy_ import bstack1111l1lll_opy_
from bstack_utils import bstack1lll1l1l1l_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1ll1l1ll_opy_, bstack11l1111lll_opy_
logger = bstack1lll1l1l1l_opy_.get_logger(__name__, bstack1lll1l1l1l_opy_.bstack1llll11l1l1_opy_())
def bstack1lll11llll1_opy_(bs_config):
    bstack1lll1lll111_opy_ = None
    bstack1lll1l1111l_opy_ = None
    try:
        bstack1lll1l1111l_opy_ = get_cli_dir()
        bstack1lll1lll111_opy_ = bstack1lll1lllll1_opy_(bstack1lll1l1111l_opy_)
        bstack1ll1l1ll11l_opy_ = bstack1lll11ll11l_opy_(bstack1lll1lll111_opy_, bstack1lll1l1111l_opy_, bs_config)
        bstack1lll1lll111_opy_ = bstack1ll1l1ll11l_opy_ if bstack1ll1l1ll11l_opy_ else bstack1lll1lll111_opy_
        if not bstack1lll1lll111_opy_:
            raise ValueError(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠢႪ"))
    except Exception as ex:
        logger.debug(bstack1l11ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡱࡧࡴࡦࡵࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࢀࢃࠢႫ").format(ex))
        bstack1lll1lll111_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠣႬ"))
        if bstack1lll1lll111_opy_:
            logger.debug(bstack1l11ll1_opy_ (u"ࠨࡆࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠤ࡫ࡸ࡯࡮ࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺ࠺ࠡࠤႭ") + str(bstack1lll1lll111_opy_) + bstack1l11ll1_opy_ (u"ࠢࠣႮ"))
        else:
            logger.debug(bstack1l11ll1_opy_ (u"ࠣࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࡁࠠࡴࡧࡷࡹࡵࠦ࡭ࡢࡻࠣࡦࡪࠦࡩ࡯ࡥࡲࡱࡵࡲࡥࡵࡧ࠱ࠦႯ"))
    return bstack1lll1lll111_opy_, bstack1lll1l1111l_opy_
bstack1llll11llll_opy_ = bstack1l11ll1_opy_ (u"ࠤ࠼࠽࠾࠿ࠢႰ")
bstack1ll1ll1111l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡶࡪࡧࡤࡺࠤႱ")
bstack1ll1lll11l1_opy_ = bstack1l11ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣႲ")
bstack1ll1ll111ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡒࡉࡔࡖࡈࡒࡤࡇࡄࡅࡔࠥႳ")
bstack1111lll1_opy_ = bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤႴ")
bstack1lll11l11ll_opy_ = re.compile(bstack1l11ll1_opy_ (u"ࡲࠣࠪࡂ࡭࠮࠴ࠪࠩࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑࡼࡃࡕࠬ࠲࠯ࠨႵ"))
bstack1ll1ll1llll_opy_ = bstack1l11ll1_opy_ (u"ࠣࡦࡨࡺࡪࡲ࡯ࡱ࡯ࡨࡲࡹࠨႶ")
bstack1lll1ll111l_opy_ = [
    bstack1l11lll111_opy_.bstack11lll11l_opy_,
    bstack1l11lll111_opy_.CONNECT,
    bstack1l11lll111_opy_.bstack1l1111ll_opy_,
]
class SDKCLI:
    _1ll1llllll1_opy_ = None
    process: Union[None, Any]
    bstack1lll1l11111_opy_: bool
    bstack1ll1ll1l1l1_opy_: bool
    bstack1llll11l11l_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll1l1ll11_opy_: Union[None, grpc.Channel]
    bstack1lll1ll11l1_opy_: str
    test_framework: TestFramework
    bstack1lllllll1ll_opy_: bstack1llllllll1l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll11ll111_opy_: bstack1ll1ll1l111_opy_
    accessibility: bstack1lll11l111l_opy_
    bstack1l1lll1ll_opy_: bstack1111l1l11_opy_
    ai: bstack1ll1ll11lll_opy_
    bstack1lll1lll1ll_opy_: bstack1lll111llll_opy_
    bstack1llll1l111l_opy_: List[bstack1ll1l1llll1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1l11ll1_opy_: Any
    bstack1lll1llll11_opy_: Dict[str, timedelta]
    bstack1llll1l1111_opy_: str
    bstack1111111ll1_opy_: bstack11111111ll_opy_
    def __new__(cls):
        if not cls._1ll1llllll1_opy_:
            cls._1ll1llllll1_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1ll1llllll1_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1l11111_opy_ = False
        self.bstack1lll1l1ll11_opy_ = None
        self.bstack1lll111111l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1ll111ll_opy_, None)
        self.bstack1lll11l1l11_opy_ = os.environ.get(bstack1ll1lll11l1_opy_, bstack1l11ll1_opy_ (u"ࠤࠥႷ")) == bstack1l11ll1_opy_ (u"ࠥࠦႸ")
        self.bstack1ll1ll1l1l1_opy_ = False
        self.bstack1llll11l11l_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1l11ll1_opy_ = None
        self.test_framework = None
        self.bstack1lllllll1ll_opy_ = None
        self.bstack1lll1ll11l1_opy_=bstack1l11ll1_opy_ (u"ࠦࠧႹ")
        self.session_framework = None
        self.logger = bstack1lll1l1l1l_opy_.get_logger(self.__class__.__name__, bstack1lll1l1l1l_opy_.bstack1llll11l1l1_opy_())
        self.bstack1lll1llll11_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111111ll1_opy_ = bstack11111111ll_opy_()
        self.bstack1lll111ll11_opy_ = None
        self.bstack1llll1111l1_opy_ = None
        self.bstack1lll11ll111_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1llll1l111l_opy_ = []
    def bstack1llll1llll_opy_(self):
        return os.environ.get(bstack1111lll1_opy_).lower().__eq__(bstack1l11ll1_opy_ (u"ࠧࡺࡲࡶࡧࠥႺ"))
    def is_enabled(self, config):
        if bstack1l11ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪႻ") in config and str(config[bstack1l11ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫႼ")]).lower() != bstack1l11ll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧႽ"):
            return False
        bstack1ll1ll11111_opy_ = [bstack1l11ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤႾ"), bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢႿ")]
        bstack1ll1l1l111l_opy_ = config.get(bstack1l11ll1_opy_ (u"ࠦ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢჀ")) in bstack1ll1ll11111_opy_ or os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭Ⴡ")) in bstack1ll1ll11111_opy_
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤჂ")] = str(bstack1ll1l1l111l_opy_) # bstack1lll1l11l1l_opy_ bstack1ll1l1ll111_opy_ VAR to bstack1lll1l1llll_opy_ is binary running
        return bstack1ll1l1l111l_opy_
    def bstack1111llll_opy_(self):
        for event in bstack1lll1ll111l_opy_:
            bstack1l1111l1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l1111l1_opy_.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡼࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࢂࠦ࠽࠿ࠢࡾࡥࡷ࡭ࡳࡾࠢࠥჃ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠣࠤჄ"))
            )
        bstack1l1111l1_opy_.register(bstack1l11lll111_opy_.bstack11lll11l_opy_, self.__1lll1l11lll_opy_)
        bstack1l1111l1_opy_.register(bstack1l11lll111_opy_.CONNECT, self.__1lll1ll1l11_opy_)
        bstack1l1111l1_opy_.register(bstack1l11lll111_opy_.bstack1l1111ll_opy_, self.__1lll1l1l11l_opy_)
        bstack1l1111l1_opy_.register(bstack1l11lll111_opy_.bstack1l11ll11_opy_, self.__1ll1llll11l_opy_)
    def bstack1ll1l1ll_opy_(self):
        return not self.bstack1lll11l1l11_opy_ and os.environ.get(bstack1ll1lll11l1_opy_, bstack1l11ll1_opy_ (u"ࠤࠥჅ")) != bstack1l11ll1_opy_ (u"ࠥࠦ჆")
    def is_running(self):
        if self.bstack1lll11l1l11_opy_:
            return self.bstack1lll1l11111_opy_
        else:
            return bool(self.bstack1lll1l1ll11_opy_)
    def bstack1ll1l1ll1ll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1llll1l111l_opy_) and cli.is_running()
    def __1ll1l1l11ll_opy_(self, bstack1llll11l1ll_opy_=10):
        if self.bstack1lll111111l_opy_:
            return
        bstack1l11ll1ll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1ll111ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡠࠨჇ") + str(id(self)) + bstack1l11ll1_opy_ (u"ࠧࡣࠠࡤࡱࡱࡲࡪࡩࡴࡪࡰࡪࠦ჈"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l11ll1_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡡࡳࡶࡴࡾࡹࠣ჉"), 0), (bstack1l11ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠳࡫࡮ࡢࡤ࡯ࡩࡤ࡮ࡴࡵࡲࡶࡣࡵࡸ࡯ࡹࡻࠥ჊"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1llll11l1ll_opy_)
        self.bstack1lll1l1ll11_opy_ = channel
        self.bstack1lll111111l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll1l1ll11_opy_)
        self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡣࡰࡰࡱࡩࡨࡺࠢ჋"), datetime.now() - bstack1l11ll1ll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1ll111ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧ࠾ࠥ࡯ࡳࡠࡥ࡫࡭ࡱࡪ࡟ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤ჌") + str(self.bstack1ll1l1ll_opy_()) + bstack1l11ll1_opy_ (u"ࠥࠦჍ"))
    def __1lll1l1l11l_opy_(self, event_name):
        if self.bstack1ll1l1ll_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡹࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡄࡎࡌࠦ჎"))
        self.__1lll1ll1ll1_opy_()
    def __1ll1llll11l_opy_(self, event_name, bstack1ll1lll11ll_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1l11ll1_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠧ჏"))
        bstack1llll1111ll_opy_ = Path(bstack1llll111ll1_opy_ (u"ࠨࡻࡴࡧ࡯ࡪ࠳ࡩ࡬ࡪࡡࡧ࡭ࡷࢃ࠯ࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࡴ࠰࡭ࡷࡴࡴࠢა"))
        if self.bstack1lll1l1111l_opy_ and bstack1llll1111ll_opy_.exists():
            with open(bstack1llll1111ll_opy_, bstack1l11ll1_opy_ (u"ࠧࡳࠩბ"), encoding=bstack1l11ll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧგ")) as fp:
                data = json.load(fp)
                try:
                    bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧდ"), bstack1111l1lll_opy_(bstack11l1l11lll_opy_), data, {
                        bstack1l11ll1_opy_ (u"ࠪࡥࡺࡺࡨࠨე"): (self.config[bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ვ")], self.config[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨზ")])
                    })
                except Exception as e:
                    logger.debug(bstack11l1111lll_opy_.format(str(e)))
            bstack1llll1111ll_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1lll11lll1l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1lll1l11lll_opy_(self, event_name: str, data):
        from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
        self.bstack1lll1ll11l1_opy_, self.bstack1lll1l1111l_opy_ = bstack1lll11llll1_opy_(data.bs_config)
        os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡝ࡒࡊࡖࡄࡆࡑࡋ࡟ࡅࡋࡕࠫთ")] = self.bstack1lll1l1111l_opy_
        if not self.bstack1lll1ll11l1_opy_ or not self.bstack1lll1l1111l_opy_:
            raise ValueError(bstack1l11ll1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡆࡐࡎࠦࡢࡪࡰࡤࡶࡾࠨი"))
        if self.bstack1ll1l1ll_opy_():
            self.__1lll1ll1l11_opy_(event_name, bstack1ll1111l1_opy_())
            return
        try:
            bstack1lll11111l1_opy_.end(EVENTS.bstack1l111lll_opy_.value, EVENTS.bstack1l111lll_opy_.value + bstack1l11ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣკ"), EVENTS.bstack1l111lll_opy_.value + bstack1l11ll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢლ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1l11ll1_opy_ (u"ࠥࡇࡴࡳࡰ࡭ࡧࡷࡩ࡙ࠥࡄࡌࠢࡖࡩࡹࡻࡰ࠯ࠤმ"))
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࢁࡽࠣნ").format(e))
        start = datetime.now()
        is_started = self.__1llll11lll1_opy_()
        self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠧࡹࡰࡢࡹࡱࡣࡹ࡯࡭ࡦࠤო"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1l1l11ll_opy_()
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨࡣࡰࡰࡱࡩࡨࡺ࡟ࡵ࡫ࡰࡩࠧპ"), datetime.now() - start)
            start = datetime.now()
            self.__1lll111l111_opy_(data)
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧჟ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll11lll11_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1lll1ll1l11_opy_(self, event_name: str, data: bstack1ll1111l1_opy_):
        if not self.bstack1ll1l1ll_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡮࡯ࡧࡦࡸ࠿ࠦ࡮ࡰࡶࠣࡥࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧრ"))
            return
        bin_session_id = os.environ.get(bstack1ll1lll11l1_opy_)
        start = datetime.now()
        self.__1ll1l1l11ll_opy_()
        self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣს"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠦࡴࡰࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡈࡒࡉࠡࠤტ") + str(bin_session_id) + bstack1l11ll1_opy_ (u"ࠦࠧუ"))
        start = datetime.now()
        self.__1lll111l11l_opy_()
        self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥფ"), datetime.now() - start)
    def __1lll1111l11_opy_(self):
        if not self.bstack1lll111111l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡣࡢࡰࡱࡳࡹࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࠢࡰࡳࡩࡻ࡬ࡦࡵࠥქ"))
            return
        bstack1lll1l1l1ll_opy_ = {
            bstack1l11ll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦღ"): (bstack1ll1ll1ll1l_opy_, bstack1ll1lll1l1l_opy_, bstack1ll1l1lllll_opy_),
            bstack1l11ll1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥყ"): (bstack1ll1l1lll11_opy_, bstack1llll11111l_opy_, bstack1ll1l1l1lll_opy_),
        }
        if not self.bstack1lll111ll11_opy_ and self.session_framework in bstack1lll1l1l1ll_opy_:
            bstack1ll1l1l1l1l_opy_, bstack1lll11111ll_opy_, bstack1ll1lll1ll1_opy_ = bstack1lll1l1l1ll_opy_[self.session_framework]
            bstack1lll1l111l1_opy_ = bstack1lll11111ll_opy_()
            self.bstack1llll1111l1_opy_ = bstack1lll1l111l1_opy_
            self.bstack1lll111ll11_opy_ = bstack1ll1lll1ll1_opy_
            self.bstack1llll1l111l_opy_.append(bstack1lll1l111l1_opy_)
            self.bstack1llll1l111l_opy_.append(bstack1ll1l1l1l1l_opy_(self.bstack1llll1111l1_opy_))
        if not self.bstack1lll11ll111_opy_ and self.config_observability and self.config_observability.success: # bstack1lll1ll1lll_opy_
            self.bstack1lll11ll111_opy_ = bstack1ll1ll1l111_opy_(self.bstack1lll111ll11_opy_, self.bstack1llll1111l1_opy_) # bstack1ll1lllllll_opy_
            self.bstack1llll1l111l_opy_.append(self.bstack1lll11ll111_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll11l111l_opy_(self.bstack1lll111ll11_opy_, self.bstack1llll1111l1_opy_)
            self.bstack1llll1l111l_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l11ll1_opy_ (u"ࠤࡶࡩࡱ࡬ࡈࡦࡣ࡯ࠦშ"), False) == True:
            self.ai = bstack1ll1ll11lll_opy_()
            self.bstack1llll1l111l_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1l11ll1_opy_ and self.bstack1lll1l11ll1_opy_.success:
            self.percy = bstack1lll111llll_opy_(self.bstack1lll1l11ll1_opy_)
            self.bstack1llll1l111l_opy_.append(self.percy)
        for mod in self.bstack1llll1l111l_opy_:
            if not mod.bstack1lll1111lll_opy_():
                mod.configure(self.bstack1lll111111l_opy_, self.config, self.cli_bin_session_id, self.bstack1111111ll1_opy_)
    def __1lll1111ll1_opy_(self):
        for mod in self.bstack1llll1l111l_opy_:
            if mod.bstack1lll1111lll_opy_():
                mod.configure(self.bstack1lll111111l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll1llll1l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1lll111l111_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1ll1l1l1_opy_:
            return
        self.__1llll11l111_opy_(data)
        bstack1l11ll1ll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥჩ")
        req.sdk_language = bstack1l11ll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦც")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll11l11ll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡡࠢძ") + str(id(self)) + bstack1l11ll1_opy_ (u"ࠨ࡝ࠡ࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧწ"))
            r = self.bstack1lll111111l_opy_.StartBinSession(req)
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡢࡴࡷࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჭ"), datetime.now() - bstack1l11ll1ll_opy_)
            os.environ[bstack1ll1lll11l1_opy_] = r.bin_session_id
            self.__1ll1l1ll1l1_opy_(r)
            self.__1lll1111l11_opy_()
            self.bstack1111111ll1_opy_.start()
            self.bstack1ll1ll1l1l1_opy_ = True
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣ࡝ࠥხ") + str(id(self)) + bstack1l11ll1_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢჯ"))
        except grpc.bstack1lll1lll11l_opy_ as bstack1lll111ll1l_opy_:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧჰ") + str(bstack1lll111ll1l_opy_) + bstack1l11ll1_opy_ (u"ࠦࠧჱ"))
            traceback.print_exc()
            raise bstack1lll111ll1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤჲ") + str(e) + bstack1l11ll1_opy_ (u"ࠨࠢჳ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll11ll11_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1lll111l11l_opy_(self):
        if not self.bstack1ll1l1ll_opy_() or not self.cli_bin_session_id or self.bstack1llll11l11l_opy_:
            return
        bstack1l11ll1ll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧჴ"), bstack1l11ll1_opy_ (u"ࠨ࠲ࠪჵ")))
        try:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤ࡞ࠦჶ") + str(id(self)) + bstack1l11ll1_opy_ (u"ࠥࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧჷ"))
            r = self.bstack1lll111111l_opy_.ConnectBinSession(req)
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣჸ"), datetime.now() - bstack1l11ll1ll_opy_)
            self.__1ll1l1ll1l1_opy_(r)
            self.__1lll1111l11_opy_()
            self.bstack1111111ll1_opy_.start()
            self.bstack1llll11l11l_opy_ = True
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡡࠢჹ") + str(id(self)) + bstack1l11ll1_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧჺ"))
        except grpc.bstack1lll1lll11l_opy_ as bstack1lll111ll1l_opy_:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡴࡪ࡯ࡨࡳࡪࡻࡴ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ჻") + str(bstack1lll111ll1l_opy_) + bstack1l11ll1_opy_ (u"ࠣࠤჼ"))
            traceback.print_exc()
            raise bstack1lll111ll1l_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨჽ") + str(e) + bstack1l11ll1_opy_ (u"ࠥࠦჾ"))
            traceback.print_exc()
            raise e
    def __1ll1l1ll1l1_opy_(self, r):
        self.bstack1ll1llll111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l11ll1_opy_ (u"ࠦࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡵࡨࡶࡻ࡫ࡲࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠥჿ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l11ll1_opy_ (u"ࠧ࡫࡭ࡱࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡵ࡯ࡦࠥᄀ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l11ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡪࡸࡣࡺࠢ࡬ࡷࠥࡹࡥ࡯ࡶࠣࡳࡳࡲࡹࠡࡣࡶࠤࡵࡧࡲࡵࠢࡲࡪࠥࡺࡨࡦࠢࠥࡇࡴࡴ࡮ࡦࡥࡷࡆ࡮ࡴࡓࡦࡵࡶ࡭ࡴࡴࠬࠣࠢࡤࡲࡩࠦࡴࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡩࡴࠢࡤࡰࡸࡵࠠࡶࡵࡨࡨࠥࡨࡹࠡࡕࡷࡥࡷࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡦࡴࡨࡪࡴࡸࡥ࠭ࠢࡑࡳࡳ࡫ࠠࡩࡣࡱࡨࡱ࡯࡮ࡨࠢ࡬ࡷࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᄁ")
        self.bstack1lll1l11ll1_opy_ = getattr(r, bstack1l11ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᄂ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᄃ")] = self.config_testhub.jwt
        os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᄄ")] = self.config_testhub.build_hashed_id
    def bstack1lll1ll1111_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll1l11111_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1ll1lll111l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1ll1lll111l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1ll1111_opy_(event_name=EVENTS.bstack1lll11ll1ll_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1llll11lll1_opy_(self, bstack1llll11l1ll_opy_=10):
        if self.bstack1lll1l11111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡷࡹࡧࡲࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠧᄅ"))
            return True
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥᄆ"))
        if os.getenv(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡇࡑ࡚ࠧᄇ")) == bstack1ll1ll1llll_opy_:
            self.cli_bin_session_id = bstack1ll1ll1llll_opy_
            self.cli_listen_addr = bstack1l11ll1_opy_ (u"ࠨࡵ࡯࡫ࡻ࠾࠴ࡺ࡭ࡱ࠱ࡶࡨࡰ࠳ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠮ࠧࡶ࠲ࡸࡵࡣ࡬ࠤᄈ") % (self.cli_bin_session_id)
            self.bstack1lll1l11111_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1ll11l1_opy_, bstack1l11ll1_opy_ (u"ࠢࡴࡦ࡮ࠦᄉ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1ll11ll1_opy_ compat for text=True in bstack1lll1l1lll1_opy_ python
            encoding=bstack1l11ll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᄊ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1ll1llll1ll_opy_ = threading.Thread(target=self.__1lll1l11l11_opy_, args=(bstack1llll11l1ll_opy_,))
        bstack1ll1llll1ll_opy_.start()
        bstack1ll1llll1ll_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡵࡳࡥࡼࡴ࠺ࠡࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡸࡥࡵࡷࡵࡲࡨࡵࡤࡦࡿࠣࡳࡺࡺ࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡴࡶࡧࡳࡺࡺ࠮ࡳࡧࡤࡨ࠭࠯ࡽࠡࡧࡵࡶࡂࠨᄋ") + str(self.process.stderr.read()) + bstack1l11ll1_opy_ (u"ࠥࠦᄌ"))
        if not self.bstack1lll1l11111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡠࠨᄍ") + str(id(self)) + bstack1l11ll1_opy_ (u"ࠧࡣࠠࡤ࡮ࡨࡥࡳࡻࡰࠣᄎ"))
            self.__1lll1ll1ll1_opy_()
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡶࡲࡰࡥࡨࡷࡸࡥࡲࡦࡣࡧࡽ࠿ࠦࠢᄏ") + str(self.bstack1lll1l11111_opy_) + bstack1l11ll1_opy_ (u"ࠢࠣᄐ"))
        return self.bstack1lll1l11111_opy_
    def __1lll1l11l11_opy_(self, bstack1lll1l1l111_opy_=10):
        bstack1lll11l1lll_opy_ = time.time()
        while self.process and time.time() - bstack1lll11l1lll_opy_ < bstack1lll1l1l111_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l11ll1_opy_ (u"ࠣ࡫ࡧࡁࠧᄑ") in line:
                    self.cli_bin_session_id = line.split(bstack1l11ll1_opy_ (u"ࠤ࡬ࡨࡂࠨᄒ"))[-1:][0].strip()
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡧࡱ࡯࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠻ࠤᄓ") + str(self.cli_bin_session_id) + bstack1l11ll1_opy_ (u"ࠦࠧᄔ"))
                    continue
                if bstack1l11ll1_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨᄕ") in line:
                    self.cli_listen_addr = line.split(bstack1l11ll1_opy_ (u"ࠨ࡬ࡪࡵࡷࡩࡳࡃࠢᄖ"))[-1:][0].strip()
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡤ࡮࡬ࡣࡱ࡯ࡳࡵࡧࡱࡣࡦࡪࡤࡳ࠼ࠥᄗ") + str(self.cli_listen_addr) + bstack1l11ll1_opy_ (u"ࠣࠤᄘ"))
                    continue
                if bstack1l11ll1_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣᄙ") in line:
                    port = line.split(bstack1l11ll1_opy_ (u"ࠥࡴࡴࡸࡴ࠾ࠤᄚ"))[-1:][0].strip()
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡵࡵࡲࡵ࠼ࠥᄛ") + str(port) + bstack1l11ll1_opy_ (u"ࠧࠨᄜ"))
                    continue
                if line.strip() == bstack1ll1ll1111l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l11ll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡏࡏࡠࡕࡗࡖࡊࡇࡍࠣᄝ"), bstack1l11ll1_opy_ (u"ࠢ࠲ࠤᄞ")) == bstack1l11ll1_opy_ (u"ࠣ࠳ࠥᄟ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1l11111_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡨࡶࡷࡵࡲ࠻ࠢࠥᄠ") + str(e) + bstack1l11ll1_opy_ (u"ࠥࠦᄡ"))
        return False
    @measure(event_name=EVENTS.bstack1lll11l11l1_opy_, stage=STAGE.bstack11lllll111_opy_)
    def __1lll1ll1ll1_opy_(self):
        if self.bstack1lll1l1ll11_opy_:
            self.bstack1111111ll1_opy_.stop()
            start = datetime.now()
            if self.bstack1lll1ll1l1l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1llll11l11l_opy_:
                    self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᄢ"), datetime.now() - start)
                else:
                    self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠧࡹࡴࡰࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤᄣ"), datetime.now() - start)
            self.__1lll1111ll1_opy_()
            start = datetime.now()
            self.bstack1lll1l1ll11_opy_.close()
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨࡤࡪࡵࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᄤ"), datetime.now() - start)
            self.bstack1lll1l1ll11_opy_ = None
        if self.process:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡴࡶࡲࡴࠧᄥ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣ࡭࡬ࡰࡱࡥࡴࡪ࡯ࡨࠦᄦ"), datetime.now() - start)
            self.process = None
            if self.bstack1lll11l1l11_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1ll11l1l_opy_()
                self.logger.info(
                    bstack1l11ll1_opy_ (u"ࠤ࡙࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠤᄧ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᄨ")] = self.config_testhub.build_hashed_id
        self.bstack1lll1l11111_opy_ = False
    def __1llll11l111_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1l11ll1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᄩ")] = selenium.__version__
            data.frameworks.append(bstack1l11ll1_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᄪ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1l11ll1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᄫ")] = __version__
            data.frameworks.append(bstack1l11ll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᄬ"))
        except:
            pass
    def bstack1lll1ll11ll_opy_(self, hub_url: str, platform_index: int, bstack11111l111_opy_: Any):
        if self.bstack1lllllll1ll_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡵࡨࡰࡪࡴࡩࡶ࡯࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧᄭ"))
            return
        try:
            bstack1l11ll1ll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l11ll1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᄮ")
            self.bstack1lllllll1ll_opy_ = bstack1ll1l1l1lll_opy_(
                cli.config.get(bstack1l11ll1_opy_ (u"ࠥ࡬ࡺࡨࡕࡳ࡮ࠥᄯ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll1111l1l_opy_={bstack1l11ll1_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣᄰ"): bstack11111l111_opy_}
            )
            def bstack1lll11l1ll1_opy_(self):
                return
            if self.config.get(bstack1l11ll1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠢᄱ"), True):
                Service.start = bstack1lll11l1ll1_opy_
                Service.stop = bstack1lll11l1ll1_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1111l1l11_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll1l111ll_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᄲ"), datetime.now() - bstack1l11ll1ll_opy_)
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡶࡩࡱ࡫࡮ࡪࡷࡰ࠾ࠥࠨᄳ") + str(e) + bstack1l11ll1_opy_ (u"ࠣࠤᄴ"))
    def bstack1ll1ll1ll11_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1llll11l1l_opy_
            self.bstack1lllllll1ll_opy_ = bstack1ll1l1lllll_opy_(
                platform_index,
                framework_name=bstack1l11ll1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᄵ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠼ࠣࠦᄶ") + str(e) + bstack1l11ll1_opy_ (u"ࠦࠧᄷ"))
            pass
    def bstack1lll1llllll_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢᄸ"))
            return
        if bstack1l11llll11_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᄹ"): pytest.__version__ }, [bstack1l11ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᄺ")], self.bstack1111111ll1_opy_, self.bstack1lll111111l_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1llll111l1l_opy_({ bstack1l11ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᄻ"): pytest.__version__ }, [bstack1l11ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᄼ")], self.bstack1111111ll1_opy_, self.bstack1lll111111l_opy_)
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡹࡵࡧࡶࡸ࠿ࠦࠢᄽ") + str(e) + bstack1l11ll1_opy_ (u"ࠦࠧᄾ"))
        self.bstack1lll111l1ll_opy_()
    def bstack1lll111l1ll_opy_(self):
        if not self.bstack1llll1llll_opy_():
            return
        bstack1lll1llll_opy_ = None
        def bstack1l111l1ll1_opy_(config, startdir):
            return bstack1l11ll1_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥᄿ").format(bstack1l11ll1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᅀ"))
        def bstack11lllll1_opy_():
            return
        def bstack11ll1l1ll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l11ll1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᅁ"):
                return bstack1l11ll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᅂ")
            else:
                return bstack1lll1llll_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1lll1llll_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1l111l1ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11lllll1_opy_
            Config.getoption = bstack11ll1l1ll_opy_
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡵࡥ࡫ࠤࡵࡿࡴࡦࡵࡷࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡦࡰࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠼ࠣࠦᅃ") + str(e) + bstack1l11ll1_opy_ (u"ࠥࠦᅄ"))
    def bstack1ll1l1l1l11_opy_(self):
        bstack1lll111ll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1lll111ll_opy_, dict):
            if cli.config_observability:
                bstack1lll111ll_opy_.update(
                    {bstack1l11ll1_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᅅ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l11ll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣᅆ") in accessibility.get(bstack1l11ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᅇ"), {}):
                    bstack1lll11l1l1l_opy_ = accessibility.get(bstack1l11ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᅈ"))
                    bstack1lll11l1l1l_opy_.update({ bstack1l11ll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠤᅉ"): bstack1lll11l1l1l_opy_.pop(bstack1l11ll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧᅊ")) })
                bstack1lll111ll_opy_.update({bstack1l11ll1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᅋ"): accessibility })
        return bstack1lll111ll_opy_
    @measure(event_name=EVENTS.bstack1ll1ll1l11l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1lll1ll1l1l_opy_(self, bstack1llll11ll1l_opy_: str = None, bstack1lll1lll1l1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll111111l_opy_:
            return
        bstack1l11ll1ll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1llll11ll1l_opy_:
            req.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
        if bstack1lll1lll1l1_opy_:
            req.bstack1lll1lll1l1_opy_ = bstack1lll1lll1l1_opy_
        try:
            r = self.bstack1lll111111l_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡸࡴࡶ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᅌ"), datetime.now() - bstack1l11ll1ll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack111l1l11_opy_(self, key: str, value: timedelta):
        tag = bstack1l11ll1_opy_ (u"ࠧࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧᅍ") if self.bstack1ll1l1ll_opy_() else bstack1l11ll1_opy_ (u"ࠨ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷࠧᅎ")
        self.bstack1lll1llll11_opy_[bstack1l11ll1_opy_ (u"ࠢ࠻ࠤᅏ").join([tag + bstack1l11ll1_opy_ (u"ࠣ࠯ࠥᅐ") + str(id(self)), key])] += value
    def bstack1ll11l1l_opy_(self):
        if not os.getenv(bstack1l11ll1_opy_ (u"ࠤࡇࡉࡇ࡛ࡇࡠࡒࡈࡖࡋࠨᅑ"), bstack1l11ll1_opy_ (u"ࠥ࠴ࠧᅒ")) == bstack1l11ll1_opy_ (u"ࠦ࠶ࠨᅓ"):
            return
        bstack1llll111lll_opy_ = dict()
        bstack1llllll1lll_opy_ = []
        if self.test_framework:
            bstack1llllll1lll_opy_.extend(list(self.test_framework.bstack1llllll1lll_opy_.values()))
        if self.bstack1lllllll1ll_opy_:
            bstack1llllll1lll_opy_.extend(list(self.bstack1lllllll1ll_opy_.bstack1llllll1lll_opy_.values()))
        for instance in bstack1llllll1lll_opy_:
            if not instance.platform_index in bstack1llll111lll_opy_:
                bstack1llll111lll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1llll111lll_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1lllll1l_opy_().items():
                report[k] += v
                report[k.split(bstack1l11ll1_opy_ (u"ࠧࡀࠢᅔ"))[0]] += v
        bstack1lll11lllll_opy_ = sorted([(k, v) for k, v in self.bstack1lll1llll11_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1ll1ll111l1_opy_ = 0
        for r in bstack1lll11lllll_opy_:
            bstack1lll1111111_opy_ = r[1].total_seconds()
            bstack1ll1ll111l1_opy_ += bstack1lll1111111_opy_
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡿࡷࡡ࠰࡞ࡿࡀࠦᅕ") + str(bstack1lll1111111_opy_) + bstack1l11ll1_opy_ (u"ࠢࠣᅖ"))
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠣ࠯࠰ࠦᅗ"))
        bstack1ll1lll1111_opy_ = []
        for platform_index, report in bstack1llll111lll_opy_.items():
            bstack1ll1lll1111_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1ll1lll1111_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1ll1lll111_opy_ = set()
        bstack1ll1lllll11_opy_ = 0
        for r in bstack1ll1lll1111_opy_:
            bstack1lll1111111_opy_ = r[2].total_seconds()
            bstack1ll1lllll11_opy_ += bstack1lll1111111_opy_
            bstack1ll1lll111_opy_.add(r[0])
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡷࡩࡸࡺ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠯ࡾࡶࡠ࠶࡝ࡾ࠼ࡾࡶࡠ࠷࡝ࡾ࠿ࠥᅘ") + str(bstack1lll1111111_opy_) + bstack1l11ll1_opy_ (u"ࠥࠦᅙ"))
        if self.bstack1ll1l1ll_opy_():
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦ࠲࠳ࠢᅚ"))
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠿ࡾࡸࡴࡺࡡ࡭ࡡࡦࡰ࡮ࢃࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡳ࠮ࡽࡶࡸࡷ࠮ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠫࢀࡁࠧᅛ") + str(bstack1ll1lllll11_opy_) + bstack1l11ll1_opy_ (u"ࠨࠢᅜ"))
        else:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࡀࠦᅝ") + str(bstack1ll1ll111l1_opy_) + bstack1l11ll1_opy_ (u"ࠣࠤᅞ"))
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠤ࠰࠱ࠧᅟ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files
        )
        if not self.bstack1lll111111l_opy_:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡄࡣࡱࡲࡴࡺࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᅠ"))
            return None
        response = self.bstack1lll111111l_opy_.TestOrchestration(request)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵ࠯ࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠯ࡶࡩࡸࡹࡩࡰࡰࡀࡿࢂࠨᅡ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1ll1llll111_opy_(self, r):
        if r is not None and getattr(r, bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧ࠭ᅢ"), None) and getattr(r.testhub, bstack1l11ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᅣ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l11ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᅤ")))
            for bstack1lll11ll1l1_opy_, err in errors.items():
                if err[bstack1l11ll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᅥ")] == bstack1l11ll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᅦ"):
                    self.logger.info(err[bstack1l11ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᅧ")])
                else:
                    self.logger.error(err[bstack1l11ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᅨ")])
    def bstack1l111llll_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()