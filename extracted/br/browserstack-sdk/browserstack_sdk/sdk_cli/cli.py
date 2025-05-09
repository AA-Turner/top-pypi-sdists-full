# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1ll1lll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llllll_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll111_opy_ import bstack1lllll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1ll_opy_ import bstack1llll111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1lll1ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111_opy_ import bstack1ll1ll111_opy_, bstack1l1ll1l11_opy_, bstack11l1ll111l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1llll111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import bstack11111l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lll1lll111_opy_
from bstack_utils.helper import Notset, bstack1lllll1lll1_opy_, get_cli_dir, bstack1lll11lll11_opy_, bstack1l1111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1lll111111l_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1l1l_opy_ import bstack1l1l1ll1_opy_
from bstack_utils.helper import Notset, bstack1lllll1lll1_opy_, get_cli_dir, bstack1lll11lll11_opy_, bstack1l1111l111_opy_, bstack1lll1ll11l_opy_, bstack11llll11_opy_, bstack1l1ll11l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll111ll11_opy_, bstack1lll1ll1ll1_opy_, bstack1lll1l111l1_opy_, bstack1lll1111ll1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import bstack111111l1ll_opy_, bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l11lll1_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1l11lll_opy_, bstack11ll11ll11_opy_
logger = bstack1l11lll1_opy_.get_logger(__name__, bstack1l11lll1_opy_.bstack1ll1lllllll_opy_())
def bstack1lll1l1l1ll_opy_(bs_config):
    bstack1lll1ll1l1l_opy_ = None
    bstack1lllll11ll1_opy_ = None
    try:
        bstack1lllll11ll1_opy_ = get_cli_dir()
        bstack1lll1ll1l1l_opy_ = bstack1lll11lll11_opy_(bstack1lllll11ll1_opy_)
        bstack1llll11l11l_opy_ = bstack1lllll1lll1_opy_(bstack1lll1ll1l1l_opy_, bstack1lllll11ll1_opy_, bs_config)
        bstack1lll1ll1l1l_opy_ = bstack1llll11l11l_opy_ if bstack1llll11l11l_opy_ else bstack1lll1ll1l1l_opy_
        if not bstack1lll1ll1l1l_opy_:
            raise ValueError(bstack11lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨါ"))
    except Exception as ex:
        logger.debug(bstack11lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡰࡦࡺࡥࡴࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡿࢂࠨာ").format(ex))
        bstack1lll1ll1l1l_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡓࡅ࡙ࡎࠢိ"))
        if bstack1lll1ll1l1l_opy_:
            logger.debug(bstack11lll_opy_ (u"ࠧࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠣࡪࡷࡵ࡭ࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࡀࠠࠣီ") + str(bstack1lll1ll1l1l_opy_) + bstack11lll_opy_ (u"ࠨࠢု"))
        else:
            logger.debug(bstack11lll_opy_ (u"ࠢࡏࡱࠣࡺࡦࡲࡩࡥࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࡀࠦࡳࡦࡶࡸࡴࠥࡳࡡࡺࠢࡥࡩࠥ࡯࡮ࡤࡱࡰࡴࡱ࡫ࡴࡦ࠰ࠥူ"))
    return bstack1lll1ll1l1l_opy_, bstack1lllll11ll1_opy_
bstack1lll111ll1l_opy_ = bstack11lll_opy_ (u"ࠣ࠻࠼࠽࠾ࠨေ")
bstack1lll1l1l111_opy_ = bstack11lll_opy_ (u"ࠤࡵࡩࡦࡪࡹࠣဲ")
bstack1llll11llll_opy_ = bstack11lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢဳ")
bstack1lll1lllll1_opy_ = bstack11lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡑࡏࡓࡕࡇࡑࡣࡆࡊࡄࡓࠤဴ")
bstack1ll111l1_opy_ = bstack11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣဵ")
bstack1lll1l11lll_opy_ = re.compile(bstack11lll_opy_ (u"ࡸࠢࠩࡁ࡬࠭࠳࠰ࠨࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࢂࡂࡔࠫ࠱࠮ࠧံ"))
bstack1lllll1l11l_opy_ = bstack11lll_opy_ (u"ࠢࡥࡧࡹࡩࡱࡵࡰ࡮ࡧࡱࡸ့ࠧ")
bstack1lll11llll1_opy_ = [
    bstack1l1ll1l11_opy_.bstack11l1lll1_opy_,
    bstack1l1ll1l11_opy_.CONNECT,
    bstack1l1ll1l11_opy_.bstack11111l11_opy_,
]
class SDKCLI:
    _1lll1111l1l_opy_ = None
    process: Union[None, Any]
    bstack1lllll11l1l_opy_: bool
    bstack1lll11l1111_opy_: bool
    bstack1llll1l1111_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lllll1l1ll_opy_: Union[None, grpc.Channel]
    bstack1lll111lll1_opy_: str
    test_framework: TestFramework
    bstack11111l1l1l_opy_: bstack11111l1ll1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll11l1l1l_opy_: bstack1lll1l11l11_opy_
    accessibility: bstack1lll1l11ll1_opy_
    bstack1ll1l1l1l_opy_: bstack1l1l1ll1_opy_
    ai: bstack1ll1lll1ll1_opy_
    bstack1llll1lllll_opy_: bstack1lll11l11ll_opy_
    bstack1lll1ll11ll_opy_: List[bstack1lll1l1lll1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1llllll11ll_opy_: Any
    bstack1llll1l1lll_opy_: Dict[str, timedelta]
    bstack1lll1l1ll11_opy_: str
    bstack1111l1l1ll_opy_: bstack1111l1ll11_opy_
    def __new__(cls):
        if not cls._1lll1111l1l_opy_:
            cls._1lll1111l1l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll1111l1l_opy_
    def __init__(self):
        self.process = None
        self.bstack1lllll11l1l_opy_ = False
        self.bstack1lllll1l1ll_opy_ = None
        self.bstack1llllll1l11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll1lllll1_opy_, None)
        self.bstack1llll1llll1_opy_ = os.environ.get(bstack1llll11llll_opy_, bstack11lll_opy_ (u"ࠣࠤး")) == bstack11lll_opy_ (u"ࠤ္ࠥ")
        self.bstack1lll11l1111_opy_ = False
        self.bstack1llll1l1111_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1llllll11ll_opy_ = None
        self.test_framework = None
        self.bstack11111l1l1l_opy_ = None
        self.bstack1lll111lll1_opy_=bstack11lll_opy_ (u"်ࠥࠦ")
        self.session_framework = None
        self.logger = bstack1l11lll1_opy_.get_logger(self.__class__.__name__, bstack1l11lll1_opy_.bstack1ll1lllllll_opy_())
        self.bstack1llll1l1lll_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111l1l1ll_opy_ = bstack1111l1ll11_opy_()
        self.bstack1lll11l1ll1_opy_ = None
        self.bstack1lll1l111ll_opy_ = None
        self.bstack1lll11l1l1l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll1ll11ll_opy_ = []
    def bstack1l111l1ll1_opy_(self):
        return os.environ.get(bstack1ll111l1_opy_).lower().__eq__(bstack11lll_opy_ (u"ࠦࡹࡸࡵࡦࠤျ"))
    def is_enabled(self, config):
        if bstack11lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩြ") in config and str(config[bstack11lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪွ")]).lower() != bstack11lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ှ"):
            return False
        bstack1lll1111lll_opy_ = [bstack11lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣဿ"), bstack11lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ၀")]
        bstack1lll1lll1l1_opy_ = config.get(bstack11lll_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ၁")) in bstack1lll1111lll_opy_ or os.environ.get(bstack11lll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬ၂")) in bstack1lll1111lll_opy_
        os.environ[bstack11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣࡎ࡙࡟ࡓࡗࡑࡒࡎࡔࡇࠣ၃")] = str(bstack1lll1lll1l1_opy_) # bstack1lll11l1lll_opy_ bstack1llll111ll1_opy_ VAR to bstack1llll11111l_opy_ is binary running
        return bstack1lll1lll1l1_opy_
    def bstack1lll111l11_opy_(self):
        for event in bstack1lll11llll1_opy_:
            bstack1ll1ll111_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1ll1ll111_opy_.logger.debug(bstack11lll_opy_ (u"ࠨࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠥࡃ࠾ࠡࡽࡤࡶ࡬ࡹࡽࠡࠤ၄") + str(kwargs) + bstack11lll_opy_ (u"ࠢࠣ၅"))
            )
        bstack1ll1ll111_opy_.register(bstack1l1ll1l11_opy_.bstack11l1lll1_opy_, self.__1lll1l11l1l_opy_)
        bstack1ll1ll111_opy_.register(bstack1l1ll1l11_opy_.CONNECT, self.__1lll1llll1l_opy_)
        bstack1ll1ll111_opy_.register(bstack1l1ll1l11_opy_.bstack11111l11_opy_, self.__1lll1l1l11l_opy_)
        bstack1ll1ll111_opy_.register(bstack1l1ll1l11_opy_.bstack11l11111l_opy_, self.__1lllll11lll_opy_)
    def bstack111l11ll_opy_(self):
        return not self.bstack1llll1llll1_opy_ and os.environ.get(bstack1llll11llll_opy_, bstack11lll_opy_ (u"ࠣࠤ၆")) != bstack11lll_opy_ (u"ࠤࠥ၇")
    def is_running(self):
        if self.bstack1llll1llll1_opy_:
            return self.bstack1lllll11l1l_opy_
        else:
            return bool(self.bstack1lllll1l1ll_opy_)
    def bstack1lllll1ll11_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll1ll11ll_opy_) and cli.is_running()
    def __1lll11ll1ll_opy_(self, bstack1llll1l11ll_opy_=10):
        if self.bstack1llllll1l11_opy_:
            return
        bstack111ll1lll_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll1lllll1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11lll_opy_ (u"ࠥ࡟ࠧ၈") + str(id(self)) + bstack11lll_opy_ (u"ࠦࡢࠦࡣࡰࡰࡱࡩࡨࡺࡩ࡯ࡩࠥ၉"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡠࡲࡵࡳࡽࡿࠢ၊"), 0), (bstack11lll_opy_ (u"ࠨࡧࡳࡲࡦ࠲ࡪࡴࡡࡣ࡮ࡨࡣ࡭ࡺࡴࡱࡵࡢࡴࡷࡵࡸࡺࠤ။"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1llll1l11ll_opy_)
        self.bstack1lllll1l1ll_opy_ = channel
        self.bstack1llllll1l11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lllll1l1ll_opy_)
        self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࠨ၌"), datetime.now() - bstack111ll1lll_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll1lllll1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11lll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦ࠽ࠤ࡮ࡹ࡟ࡤࡪ࡬ࡰࡩࡥࡰࡳࡱࡦࡩࡸࡹ࠽ࠣ၍") + str(self.bstack111l11ll_opy_()) + bstack11lll_opy_ (u"ࠤࠥ၎"))
    def __1lll1l1l11l_opy_(self, event_name):
        if self.bstack111l11ll_opy_():
            self.logger.debug(bstack11lll_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡃࡍࡋࠥ၏"))
        self.__1lll11111ll_opy_()
    def __1lllll11lll_opy_(self, event_name, bstack1llll1ll111_opy_ = None, bstack1llll1111l_opy_=1):
        if bstack1llll1111l_opy_ == 1:
            self.logger.error(bstack11lll_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠦၐ"))
        bstack1lll111llll_opy_ = Path(bstack1lllll11l11_opy_ (u"ࠧࢁࡳࡦ࡮ࡩ࠲ࡨࡲࡩࡠࡦ࡬ࡶࢂ࠵ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࡳ࠯࡬ࡶࡳࡳࠨၑ"))
        if self.bstack1lllll11ll1_opy_ and bstack1lll111llll_opy_.exists():
            with open(bstack1lll111llll_opy_, bstack11lll_opy_ (u"࠭ࡲࠨၒ"), encoding=bstack11lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ၓ")) as fp:
                data = json.load(fp)
                try:
                    bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ၔ"), bstack11llll11_opy_(bstack11ll11l1_opy_), data, {
                        bstack11lll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧၕ"): (self.config[bstack11lll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬၖ")], self.config[bstack11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧၗ")])
                    })
                except Exception as e:
                    logger.debug(bstack11ll11ll11_opy_.format(str(e)))
            bstack1lll111llll_opy_.unlink()
        sys.exit(bstack1llll1111l_opy_)
    @measure(event_name=EVENTS.bstack1lll11ll11l_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1lll1l11l1l_opy_(self, event_name: str, data):
        from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
        self.bstack1lll111lll1_opy_, self.bstack1lllll11ll1_opy_ = bstack1lll1l1l1ll_opy_(data.bs_config)
        os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡜ࡘࡉࡕࡃࡅࡐࡊࡥࡄࡊࡔࠪၘ")] = self.bstack1lllll11ll1_opy_
        if not self.bstack1lll111lll1_opy_ or not self.bstack1lllll11ll1_opy_:
            raise ValueError(bstack11lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡪࡨࠤࡘࡊࡋࠡࡅࡏࡍࠥࡨࡩ࡯ࡣࡵࡽࠧၙ"))
        if self.bstack111l11ll_opy_():
            self.__1lll1llll1l_opy_(event_name, bstack11l1ll111l_opy_())
            return
        try:
            bstack1ll1llllll1_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, EVENTS.bstack1l1l11llll_opy_.value + bstack11lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢၚ"), EVENTS.bstack1l1l11llll_opy_.value + bstack11lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨၛ"), status=True, failure=None, test_name=None)
            logger.debug(bstack11lll_opy_ (u"ࠤࡆࡳࡲࡶ࡬ࡦࡶࡨࠤࡘࡊࡋࠡࡕࡨࡸࡺࡶ࠮ࠣၜ"))
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶࠤࢀࢃࠢၝ").format(e))
        start = datetime.now()
        is_started = self.__1ll1llll1ll_opy_()
        self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠦࡸࡶࡡࡸࡰࡢࡸ࡮ࡳࡥࠣၞ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lll11ll1ll_opy_()
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦၟ"), datetime.now() - start)
            start = datetime.now()
            self.__1llll1ll11l_opy_(data)
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦၠ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1llll11l1l1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1lll1llll1l_opy_(self, event_name: str, data: bstack11l1ll111l_opy_):
        if not self.bstack111l11ll_opy_():
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴ࡮ࡦࡥࡷ࠾ࠥࡴ࡯ࡵࠢࡤࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶࠦၡ"))
            return
        bin_session_id = os.environ.get(bstack1llll11llll_opy_)
        start = datetime.now()
        self.__1lll11ll1ll_opy_()
        self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢၢ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠥࡺ࡯ࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡇࡑࡏࠠࠣၣ") + str(bin_session_id) + bstack11lll_opy_ (u"ࠥࠦၤ"))
        start = datetime.now()
        self.__1lll1l1llll_opy_()
        self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡹ࡯࡭ࡦࠤၥ"), datetime.now() - start)
    def __1llll11ll11_opy_(self):
        if not self.bstack1llllll1l11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11lll_opy_ (u"ࠧࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࠡ࡯ࡲࡨࡺࡲࡥࡴࠤၦ"))
            return
        bstack1llll11l1ll_opy_ = {
            bstack11lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥၧ"): (bstack1lll1ll111l_opy_, bstack1lll1l1111l_opy_, bstack1lll1lll111_opy_),
            bstack11lll_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤၨ"): (bstack1lllll1ll1l_opy_, bstack1llll111l1l_opy_, bstack1lll1ll1lll_opy_),
        }
        if not self.bstack1lll11l1ll1_opy_ and self.session_framework in bstack1llll11l1ll_opy_:
            bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_, bstack1llll1lll11_opy_ = bstack1llll11l1ll_opy_[self.session_framework]
            bstack1lll11111l1_opy_ = bstack1lll1l1ll1l_opy_()
            self.bstack1lll1l111ll_opy_ = bstack1lll11111l1_opy_
            self.bstack1lll11l1ll1_opy_ = bstack1llll1lll11_opy_
            self.bstack1lll1ll11ll_opy_.append(bstack1lll11111l1_opy_)
            self.bstack1lll1ll11ll_opy_.append(bstack1lll11l11l1_opy_(self.bstack1lll1l111ll_opy_))
        if not self.bstack1lll11l1l1l_opy_ and self.config_observability and self.config_observability.success: # bstack1lll1l1l1l1_opy_
            self.bstack1lll11l1l1l_opy_ = bstack1lll1l11l11_opy_(self.bstack1lll11l1ll1_opy_, self.bstack1lll1l111ll_opy_) # bstack1lll11lll1l_opy_
            self.bstack1lll1ll11ll_opy_.append(self.bstack1lll11l1l1l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll1l11ll1_opy_(self.bstack1lll11l1ll1_opy_, self.bstack1lll1l111ll_opy_)
            self.bstack1lll1ll11ll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11lll_opy_ (u"ࠣࡵࡨࡰ࡫ࡎࡥࡢ࡮ࠥၩ"), False) == True:
            self.ai = bstack1ll1lll1ll1_opy_()
            self.bstack1lll1ll11ll_opy_.append(self.ai)
        if not self.percy and self.bstack1llllll11ll_opy_ and self.bstack1llllll11ll_opy_.success:
            self.percy = bstack1lll11l11ll_opy_(self.bstack1llllll11ll_opy_)
            self.bstack1lll1ll11ll_opy_.append(self.percy)
        for mod in self.bstack1lll1ll11ll_opy_:
            if not mod.bstack1lllll1111l_opy_():
                mod.configure(self.bstack1llllll1l11_opy_, self.config, self.cli_bin_session_id, self.bstack1111l1l1ll_opy_)
    def __1llll111lll_opy_(self):
        for mod in self.bstack1lll1ll11ll_opy_:
            if mod.bstack1lllll1111l_opy_():
                mod.configure(self.bstack1llllll1l11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1llll1l11l1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1llll1ll11l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lll11l1111_opy_:
            return
        self.__1lll111l1ll_opy_(data)
        bstack111ll1lll_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11lll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤၪ")
        req.sdk_language = bstack11lll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥၫ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll1l11lll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11lll_opy_ (u"ࠦࡠࠨၬ") + str(id(self)) + bstack11lll_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦၭ"))
            r = self.bstack1llllll1l11_opy_.StartBinSession(req)
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣၮ"), datetime.now() - bstack111ll1lll_opy_)
            os.environ[bstack1llll11llll_opy_] = r.bin_session_id
            self.__1ll1lll1lll_opy_(r)
            self.__1llll11ll11_opy_()
            self.bstack1111l1l1ll_opy_.start()
            self.bstack1lll11l1111_opy_ = True
            self.logger.debug(bstack11lll_opy_ (u"ࠢ࡜ࠤၯ") + str(id(self)) + bstack11lll_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࠨၰ"))
        except grpc.bstack1llll1l1l11_opy_ as bstack1ll1llll1l1_opy_:
            self.logger.error(bstack11lll_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦၱ") + str(bstack1ll1llll1l1_opy_) + bstack11lll_opy_ (u"ࠥࠦၲ"))
            traceback.print_exc()
            raise bstack1ll1llll1l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11lll_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣၳ") + str(e) + bstack11lll_opy_ (u"ࠧࠨၴ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll1l1l1l_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1lll1l1llll_opy_(self):
        if not self.bstack111l11ll_opy_() or not self.cli_bin_session_id or self.bstack1llll1l1111_opy_:
            return
        bstack111ll1lll_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ၵ"), bstack11lll_opy_ (u"ࠧ࠱ࠩၶ")))
        try:
            self.logger.debug(bstack11lll_opy_ (u"ࠣ࡝ࠥၷ") + str(id(self)) + bstack11lll_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦၸ"))
            r = self.bstack1llllll1l11_opy_.ConnectBinSession(req)
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢၹ"), datetime.now() - bstack111ll1lll_opy_)
            self.__1ll1lll1lll_opy_(r)
            self.__1llll11ll11_opy_()
            self.bstack1111l1l1ll_opy_.start()
            self.bstack1llll1l1111_opy_ = True
            self.logger.debug(bstack11lll_opy_ (u"ࠦࡠࠨၺ") + str(id(self)) + bstack11lll_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠦၻ"))
        except grpc.bstack1llll1l1l11_opy_ as bstack1ll1llll1l1_opy_:
            self.logger.error(bstack11lll_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣၼ") + str(bstack1ll1llll1l1_opy_) + bstack11lll_opy_ (u"ࠢࠣၽ"))
            traceback.print_exc()
            raise bstack1ll1llll1l1_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11lll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧၾ") + str(e) + bstack11lll_opy_ (u"ࠤࠥၿ"))
            traceback.print_exc()
            raise e
    def __1ll1lll1lll_opy_(self, r):
        self.bstack1lllll1l111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11lll_opy_ (u"ࠥࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤႀ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11lll_opy_ (u"ࠦࡪࡳࡰࡵࡻࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡻ࡮ࡥࠤႁ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡩࡷࡩࡹࠡ࡫ࡶࠤࡸ࡫࡮ࡵࠢࡲࡲࡱࡿࠠࡢࡵࠣࡴࡦࡸࡴࠡࡱࡩࠤࡹ࡮ࡥࠡࠤࡆࡳࡳࡴࡥࡤࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠲ࠢࠡࡣࡱࡨࠥࡺࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡣ࡯ࡷࡴࠦࡵࡴࡧࡧࠤࡧࡿࠠࡔࡶࡤࡶࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࡳࡧࡩࡳࡷ࡫ࠬࠡࡐࡲࡲࡪࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡ࡫ࡶࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢႂ")
        self.bstack1llllll11ll_opy_ = getattr(r, bstack11lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬႃ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫႄ")] = self.config_testhub.jwt
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ႅ")] = self.config_testhub.build_hashed_id
    def bstack1llllll1ll1_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lllll11l1l_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llllll1lll_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llllll1lll_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1llllll1ll1_opy_(event_name=EVENTS.bstack1llll1ll1ll_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1ll1llll1ll_opy_(self, bstack1llll1l11ll_opy_=10):
        if self.bstack1lllll11l1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡶࡸࡦࡸࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡶࡺࡴ࡮ࡪࡰࡪࠦႆ"))
            return True
        self.logger.debug(bstack11lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤႇ"))
        if os.getenv(bstack11lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡆࡐ࡙ࠦႈ")) == bstack1lllll1l11l_opy_:
            self.cli_bin_session_id = bstack1lllll1l11l_opy_
            self.cli_listen_addr = bstack11lll_opy_ (u"ࠧࡻ࡮ࡪࡺ࠽࠳ࡹࡳࡰ࠰ࡵࡧ࡯࠲ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࠦࡵ࠱ࡷࡴࡩ࡫ࠣႉ") % (self.cli_bin_session_id)
            self.bstack1lllll11l1l_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll111lll1_opy_, bstack11lll_opy_ (u"ࠨࡳࡥ࡭ࠥႊ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1ll1lllll11_opy_ compat for text=True in bstack1llll1l111l_opy_ python
            encoding=bstack11lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨႋ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll111l11l_opy_ = threading.Thread(target=self.__1llll1l1ll1_opy_, args=(bstack1llll1l11ll_opy_,))
        bstack1lll111l11l_opy_.start()
        bstack1lll111l11l_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11lll_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡴࡲࡤࡻࡳࡀࠠࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࡁࢀࡹࡥ࡭ࡨ࠱ࡴࡷࡵࡣࡦࡵࡶ࠲ࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥࡾࠢࡲࡹࡹࡃࡻࡴࡧ࡯ࡪ࠳ࡶࡲࡰࡥࡨࡷࡸ࠴ࡳࡵࡦࡲࡹࡹ࠴ࡲࡦࡣࡧࠬ࠮ࢃࠠࡦࡴࡵࡁࠧႌ") + str(self.process.stderr.read()) + bstack11lll_opy_ (u"ࠤႍࠥ"))
        if not self.bstack1lllll11l1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠥ࡟ࠧႎ") + str(id(self)) + bstack11lll_opy_ (u"ࠦࡢࠦࡣ࡭ࡧࡤࡲࡺࡶࠢႏ"))
            self.__1lll11111ll_opy_()
        self.logger.debug(bstack11lll_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡵࡸ࡯ࡤࡧࡶࡷࡤࡸࡥࡢࡦࡼ࠾ࠥࠨ႐") + str(self.bstack1lllll11l1l_opy_) + bstack11lll_opy_ (u"ࠨࠢ႑"))
        return self.bstack1lllll11l1l_opy_
    def __1llll1l1ll1_opy_(self, bstack1llllll111l_opy_=10):
        bstack1llllll1l1l_opy_ = time.time()
        while self.process and time.time() - bstack1llllll1l1l_opy_ < bstack1llllll111l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11lll_opy_ (u"ࠢࡪࡦࡀࠦ႒") in line:
                    self.cli_bin_session_id = line.split(bstack11lll_opy_ (u"ࠣ࡫ࡧࡁࠧ႓"))[-1:][0].strip()
                    self.logger.debug(bstack11lll_opy_ (u"ࠤࡦࡰ࡮ࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠺ࠣ႔") + str(self.cli_bin_session_id) + bstack11lll_opy_ (u"ࠥࠦ႕"))
                    continue
                if bstack11lll_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧ႖") in line:
                    self.cli_listen_addr = line.split(bstack11lll_opy_ (u"ࠧࡲࡩࡴࡶࡨࡲࡂࠨ႗"))[-1:][0].strip()
                    self.logger.debug(bstack11lll_opy_ (u"ࠨࡣ࡭࡫ࡢࡰ࡮ࡹࡴࡦࡰࡢࡥࡩࡪࡲ࠻ࠤ႘") + str(self.cli_listen_addr) + bstack11lll_opy_ (u"ࠢࠣ႙"))
                    continue
                if bstack11lll_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢႚ") in line:
                    port = line.split(bstack11lll_opy_ (u"ࠤࡳࡳࡷࡺ࠽ࠣႛ"))[-1:][0].strip()
                    self.logger.debug(bstack11lll_opy_ (u"ࠥࡴࡴࡸࡴ࠻ࠤႜ") + str(port) + bstack11lll_opy_ (u"ࠦࠧႝ"))
                    continue
                if line.strip() == bstack1lll1l1l111_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡎࡕ࡟ࡔࡖࡕࡉࡆࡓࠢ႞"), bstack11lll_opy_ (u"ࠨ࠱ࠣ႟")) == bstack11lll_opy_ (u"ࠢ࠲ࠤႠ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lllll11l1l_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11lll_opy_ (u"ࠣࡧࡵࡶࡴࡸ࠺ࠡࠤႡ") + str(e) + bstack11lll_opy_ (u"ࠤࠥႢ"))
        return False
    @measure(event_name=EVENTS.bstack1lllll111l1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def __1lll11111ll_opy_(self):
        if self.bstack1lllll1l1ll_opy_:
            self.bstack1111l1l1ll_opy_.stop()
            start = datetime.now()
            if self.bstack1llll1111ll_opy_():
                self.cli_bin_session_id = None
                if self.bstack1llll1l1111_opy_:
                    self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢႣ"), datetime.now() - start)
                else:
                    self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣႤ"), datetime.now() - start)
            self.__1llll111lll_opy_()
            start = datetime.now()
            self.bstack1lllll1l1ll_opy_.close()
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠧࡪࡩࡴࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢႥ"), datetime.now() - start)
            self.bstack1lllll1l1ll_opy_ = None
        if self.process:
            self.logger.debug(bstack11lll_opy_ (u"ࠨࡳࡵࡱࡳࠦႦ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠢ࡬࡫࡯ࡰࡤࡺࡩ࡮ࡧࠥႧ"), datetime.now() - start)
            self.process = None
            if self.bstack1llll1llll1_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1ll1ll1l1_opy_()
                self.logger.info(
                    bstack11lll_opy_ (u"ࠣࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠦႨ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨႩ")] = self.config_testhub.build_hashed_id
        self.bstack1lllll11l1l_opy_ = False
    def __1lll111l1ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11lll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႪ")] = selenium.__version__
            data.frameworks.append(bstack11lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨႫ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤႬ")] = __version__
            data.frameworks.append(bstack11lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥႭ"))
        except:
            pass
    def bstack1lllll1l1l1_opy_(self, hub_url: str, platform_index: int, bstack111ll1ll1_opy_: Any):
        if self.bstack11111l1l1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠡࡵࡨࡸࡺࡶࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦႮ"))
            return
        try:
            bstack111ll1lll_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11lll_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥႯ")
            self.bstack11111l1l1l_opy_ = bstack1lll1ll1lll_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lll11ll111_opy_={bstack11lll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨႰ"): bstack111ll1ll1_opy_}
            )
            def bstack1llll111111_opy_(self):
                return
            if self.config.get(bstack11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠧႱ"), True):
                Service.start = bstack1llll111111_opy_
                Service.stop = bstack1llll111111_opy_
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
            WebDriver.upload_attachment = staticmethod(bstack1l1l1ll1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1llll11l111_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႲ"), datetime.now() - bstack111ll1lll_opy_)
        except Exception as e:
            self.logger.error(bstack11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠼ࠣࠦႳ") + str(e) + bstack11lll_opy_ (u"ࠨࠢႴ"))
    def bstack1llll1ll1l1_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack11lll1ll1_opy_
            self.bstack11111l1l1l_opy_ = bstack1lll1lll111_opy_(
                platform_index,
                framework_name=bstack11lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦႵ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠺ࠡࠤႶ") + str(e) + bstack11lll_opy_ (u"ࠤࠥႷ"))
            pass
    def bstack1llllll1111_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11lll_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡹࡥࡵࠢࡸࡴࠧႸ"))
            return
        if bstack1l1111l111_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦႹ"): pytest.__version__ }, [bstack11lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤႺ")], self.bstack1111l1l1ll_opy_, self.bstack1llllll1l11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1llll111l11_opy_({ bstack11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨႻ"): pytest.__version__ }, [bstack11lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢႼ")], self.bstack1111l1l1ll_opy_, self.bstack1llllll1l11_opy_)
        except Exception as e:
            self.logger.error(bstack11lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡾࡺࡥࡴࡶ࠽ࠤࠧႽ") + str(e) + bstack11lll_opy_ (u"ࠤࠥႾ"))
        self.bstack1lllll1llll_opy_()
    def bstack1lllll1llll_opy_(self):
        if not self.bstack1l111l1ll1_opy_():
            return
        bstack1lll11111_opy_ = None
        def bstack1ll1lll111_opy_(config, startdir):
            return bstack11lll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣႿ").format(bstack11lll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥჀ"))
        def bstack1llll1l111_opy_():
            return
        def bstack11111l111_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11lll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬჁ"):
                return bstack11lll_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧჂ")
            else:
                return bstack1lll11111_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1lll11111_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack1ll1lll111_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1llll1l111_opy_
            Config.getoption = bstack11111l111_opy_
        except Exception as e:
            self.logger.error(bstack11lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡺࡣࡩࠢࡳࡽࡹ࡫ࡳࡵࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤ࡫ࡵࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠺ࠡࠤჃ") + str(e) + bstack11lll_opy_ (u"ࠣࠤჄ"))
    def bstack1llll11lll1_opy_(self):
        bstack1ll1llll11_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1ll1llll11_opy_, dict):
            if cli.config_observability:
                bstack1ll1llll11_opy_.update(
                    {bstack11lll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤჅ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨ჆") in accessibility.get(bstack11lll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧჇ"), {}):
                    bstack1lllll11111_opy_ = accessibility.get(bstack11lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨ჈"))
                    bstack1lllll11111_opy_.update({ bstack11lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠢ჉"): bstack1lllll11111_opy_.pop(bstack11lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࡡࡷࡳࡤࡽࡲࡢࡲࠥ჊")) })
                bstack1ll1llll11_opy_.update({bstack11lll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣ჋"): accessibility })
        return bstack1ll1llll11_opy_
    @measure(event_name=EVENTS.bstack1lll1111l11_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1llll1111ll_opy_(self, bstack1lll1ll11l1_opy_: str = None, bstack1lll111l111_opy_: str = None, bstack1llll1111l_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llllll1l11_opy_:
            return
        bstack111ll1lll_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1llll1111l_opy_:
            req.bstack1llll1111l_opy_ = bstack1llll1111l_opy_
        if bstack1lll1ll11l1_opy_:
            req.bstack1lll1ll11l1_opy_ = bstack1lll1ll11l1_opy_
        if bstack1lll111l111_opy_:
            req.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
        try:
            r = self.bstack1llllll1l11_opy_.StopBinSession(req)
            SDKCLI.bstack1lll1llll11_opy_ = r.bstack1lll1llll11_opy_
            SDKCLI.bstack1l1lllll1l_opy_ = r.bstack1l1lllll1l_opy_
            self.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡲࡴࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥ჌"), datetime.now() - bstack111ll1lll_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11ll111111_opy_(self, key: str, value: timedelta):
        tag = bstack11lll_opy_ (u"ࠥࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥჍ") if self.bstack111l11ll_opy_() else bstack11lll_opy_ (u"ࠦࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵࠥ჎")
        self.bstack1llll1l1lll_opy_[bstack11lll_opy_ (u"ࠧࡀࠢ჏").join([tag + bstack11lll_opy_ (u"ࠨ࠭ࠣა") + str(id(self)), key])] += value
    def bstack1ll1ll1l1_opy_(self):
        if not os.getenv(bstack11lll_opy_ (u"ࠢࡅࡇࡅ࡙ࡌࡥࡐࡆࡔࡉࠦბ"), bstack11lll_opy_ (u"ࠣ࠲ࠥგ")) == bstack11lll_opy_ (u"ࠤ࠴ࠦდ"):
            return
        bstack1lll1111111_opy_ = dict()
        bstack111111111l_opy_ = []
        if self.test_framework:
            bstack111111111l_opy_.extend(list(self.test_framework.bstack111111111l_opy_.values()))
        if self.bstack11111l1l1l_opy_:
            bstack111111111l_opy_.extend(list(self.bstack11111l1l1l_opy_.bstack111111111l_opy_.values()))
        for instance in bstack111111111l_opy_:
            if not instance.platform_index in bstack1lll1111111_opy_:
                bstack1lll1111111_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll1111111_opy_[instance.platform_index]
            for k, v in instance.bstack1lll11l111l_opy_().items():
                report[k] += v
                report[k.split(bstack11lll_opy_ (u"ࠥ࠾ࠧე"))[0]] += v
        bstack1llll11ll1l_opy_ = sorted([(k, v) for k, v in self.bstack1llll1l1lll_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll11ll1l1_opy_ = 0
        for r in bstack1llll11ll1l_opy_:
            bstack1llll1lll1l_opy_ = r[1].total_seconds()
            bstack1lll11ll1l1_opy_ += bstack1llll1lll1l_opy_
            self.logger.debug(bstack11lll_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻ࡽࡵ࡟࠵ࡣࡽ࠾ࠤვ") + str(bstack1llll1lll1l_opy_) + bstack11lll_opy_ (u"ࠧࠨზ"))
        self.logger.debug(bstack11lll_opy_ (u"ࠨ࠭࠮ࠤთ"))
        bstack1lll11lllll_opy_ = []
        for platform_index, report in bstack1lll1111111_opy_.items():
            bstack1lll11lllll_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll11lllll_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack11l1l1llll_opy_ = set()
        bstack1lll1ll1111_opy_ = 0
        for r in bstack1lll11lllll_opy_:
            bstack1llll1lll1l_opy_ = r[2].total_seconds()
            bstack1lll1ll1111_opy_ += bstack1llll1lll1l_opy_
            bstack11l1l1llll_opy_.add(r[0])
            self.logger.debug(bstack11lll_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡵࡧࡶࡸ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠭ࡼࡴ࡞࠴ࡢࢃ࠺ࡼࡴ࡞࠵ࡢࢃ࠽ࠣი") + str(bstack1llll1lll1l_opy_) + bstack11lll_opy_ (u"ࠣࠤკ"))
        if self.bstack111l11ll_opy_():
            self.logger.debug(bstack11lll_opy_ (u"ࠤ࠰࠱ࠧლ"))
            self.logger.debug(bstack11lll_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࡼࡶࡲࡸࡦࡲ࡟ࡤ࡮࡬ࢁࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠳ࡻࡴࡶࡵࠬࡵࡲࡡࡵࡨࡲࡶࡲࡹࠩࡾ࠿ࠥმ") + str(bstack1lll1ll1111_opy_) + bstack11lll_opy_ (u"ࠦࠧნ"))
        else:
            self.logger.debug(bstack11lll_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡩ࡬ࡪ࠼ࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠾ࠤო") + str(bstack1lll11ll1l1_opy_) + bstack11lll_opy_ (u"ࠨࠢპ"))
        self.logger.debug(bstack11lll_opy_ (u"ࠢ࠮࠯ࠥჟ"))
    def bstack1lllll1l111_opy_(self, r):
        if r is not None and getattr(r, bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩრ"), None) and getattr(r.testhub, bstack11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩს"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤტ")))
            for bstack1lll11l1l11_opy_, err in errors.items():
                if err[bstack11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩუ")] == bstack11lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪფ"):
                    self.logger.info(err[bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧქ")])
                else:
                    self.logger.error(err[bstack11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨღ")])
    def bstack1lllll1l1_opy_(self):
        return SDKCLI.bstack1lll1llll11_opy_, SDKCLI.bstack1l1lllll1l_opy_
cli = SDKCLI()