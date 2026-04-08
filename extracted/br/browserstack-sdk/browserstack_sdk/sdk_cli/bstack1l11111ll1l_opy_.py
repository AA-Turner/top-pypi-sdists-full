# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l111l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111lllllll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack111ll1lll_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack11111lll11_opy_
import browserstack_sdk
class bstack1l1111l1ll1_opy_(bstack1l111111l1l_opy_):
    bstack11l1111lll1_opy_ = bstack111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢᢎ")
    bstack11l111l1lll_opy_ = bstack111l_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᢏ")
    bstack11l111l1l11_opy_ = bstack111l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᢐ")
    def __init__(self, bstack1l1lll1ll11_opy_):
        super().__init__()
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack11llll111l_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l11l1ll11_opy_)
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11ll1l1llll_opy_)
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.POST), self.bstack11l11l111ll_opy_)
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.POST), self.bstack11l11l1lll1_opy_)
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.QUIT, bstack1lll1l11l1_opy_.POST), self.bstack11l111l1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11l1ll11_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᢑ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᢒ")), str):
                    url = kwargs.get(bstack111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᢓ"))
                elif hasattr(kwargs.get(bstack111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᢔ")), bstack111l_opy_ (u"ࠧࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠨᢕ")):
                    url = kwargs.get(bstack111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᢖ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᢗ"))._url
            except Exception as e:
                url = bstack111l_opy_ (u"ࠪࠫᢘ")
                self.logger.error(bstack111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡷࡲࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࡻࡾࠤᢙ").format(e))
            self.logger.info(bstack111l_opy_ (u"ࠧࡘࡥ࡮ࡱࡷࡩ࡙ࠥࡥࡳࡸࡨࡶࠥࡇࡤࡥࡴࡨࡷࡸࠦࡢࡦ࡫ࡱ࡫ࠥࡶࡡࡴࡵࡨࡨࠥࡧࡳࠡ࠼ࠣࡿࢂࠨᢚ").format(str(url)))
            bstack11l111ll1l1_opy_ = None
            driver_rank = None
            try:
                bstack11l111ll1l1_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11l111ll1l1_opy_ is not None:
                    bstack11l1111ll11_opy_ = str(bstack11l111ll1l1_opy_)
                    if bstack111l_opy_ (u"ࠨࠣࠣᢛ") in bstack11l1111ll11_opy_:
                        bstack11l11l11111_opy_ = bstack11l1111ll11_opy_.rsplit(bstack111l_opy_ (u"ࠢࠤࠤᢜ"), 1)[1]
                        try:
                            driver_rank = int(bstack11l11l11111_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡦࡺࡷࡶࡦࡩࡴࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬ࠢࡩࡶࡴࡳࠠ࡭ࡣࡥࡩࡱࠦࠧࡼࡧࡻࡴࡱ࡯ࡣࡪࡶࡢࡰࡦࡨࡥ࡭ࡿࠪ࠾ࠥࠨᢝ") + str(e) + bstack111l_opy_ (u"ࠤࠥᢞ"))
            except Exception as e:
                self.logger.debug(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭࠼ࠣࠦᢟ") + str(e) + bstack111l_opy_ (u"ࠦࠧᢠ"))
            self.bstack11l1111l1l1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack111l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤࡸࡡ࡯࡭ࡀࡿࡩࡸࡩࡷࡧࡵࡣࡷࡧ࡮࡬ࡿࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀ࡬࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾ࠼ࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᢡ") + str(kwargs) + bstack111l_opy_ (u"ࠨࠢᢢ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11ll1l1llll_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll111111ll_opy_(instance, bstack1l1111l1ll1_opy_.bstack11l1111lll1_opy_, False):
            return
        if not f.bstack1ll1111ll1l_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_):
            return
        platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_)
        if f.bstack11lll1l11l1_opy_(method_name, *args) and len(args) > 1:
            bstack1lllllll1ll_opy_ = datetime.now()
            hub_url = bstack1l11l11l11l_opy_.hub_url(driver)
            self.logger.warning(bstack111l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᢣ") + str(hub_url) + bstack111l_opy_ (u"ࠣࠤᢤ"))
            bstack11l111l111l_opy_ = args[1][bstack111l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᢥ")] if isinstance(args[1], dict) and bstack111l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᢦ") in args[1] else None
            bstack11l11l1111l_opy_ = bstack111l_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᢧ")
            if isinstance(bstack11l111l111l_opy_, dict):
                bstack1lllllll1ll_opy_ = datetime.now()
                r = self.bstack11l111l11ll_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥᢨ"), datetime.now() - bstack1lllllll1ll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack111l_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀᢩࠠࠣ") + str(r) + bstack111l_opy_ (u"ࠢࠣᢪ"))
                        return
                    if r.hub_url:
                        f.bstack11l111l1l1l_opy_(instance, driver, r.hub_url)
                        f.bstack1l11l1ll11_opy_(instance, bstack1l1111l1ll1_opy_.bstack11l1111lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ᢫"), e)
    def bstack11l11l111ll_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l11l11l11l_opy_.session_id(driver)
            if session_id:
                bstack11l11l11l1l_opy_ = bstack111l_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦ᢬").format(session_id)
                bstack11lll11111_opy_.mark(bstack11l11l11l1l_opy_)
    def bstack11l11l1lll1_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll111111ll_opy_(instance, bstack1l1111l1ll1_opy_.bstack11l111l1lll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l11l11l11l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢ᢭") + str(hub_url) + bstack111l_opy_ (u"ࠦࠧ᢮"))
            return
        framework_session_id = bstack1l11l11l11l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣ᢯") + str(framework_session_id) + bstack111l_opy_ (u"ࠨࠢᢰ"))
            return
        if bstack1l11l11l11l_opy_.bstack11l11l1l11l_opy_(*args) == bstack1l11l11l11l_opy_.bstack11l111ll11l_opy_:
            bstack11l111lllll_opy_ = bstack111l_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢᢱ").format(framework_session_id)
            bstack11l11l11l1l_opy_ = bstack111l_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᢲ").format(framework_session_id)
            bstack11lll11111_opy_.end(
                label=bstack111l_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧᢳ"),
                start=bstack11l11l11l1l_opy_,
                end=bstack11l111lllll_opy_,
                status=True,
                failure=None
            )
            bstack1lllllll1ll_opy_ = datetime.now()
            r = self.bstack11l111lll1l_opy_(
                ref,
                f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᢴ"), datetime.now() - bstack1lllllll1ll_opy_)
            f.bstack1l11l1ll11_opy_(instance, bstack1l1111l1ll1_opy_.bstack11l111l1lll_opy_, r.success)
    def bstack11l111l1ll1_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll111111ll_opy_(instance, bstack1l1111l1ll1_opy_.bstack11l111l1l11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l11l11l11l_opy_.session_id(driver)
        hub_url = bstack1l11l11l11l_opy_.hub_url(driver)
        bstack1lllllll1ll_opy_ = datetime.now()
        r = self.bstack11l11l1l111_opy_(
            ref,
            f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᢵ"), datetime.now() - bstack1lllllll1ll_opy_)
        f.bstack1l11l1ll11_opy_(instance, bstack1l1111l1ll1_opy_.bstack11l111l1l11_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1l11llll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l1l11ll1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11l1111l1ll_opy_ = int(driver_rank)
                is_secondary_driver = bstack11l1111l1ll_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack111l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥᢶ") + str(req) + bstack111l_opy_ (u"ࠨࠢᢷ"))
        try:
            r = self.bstack11l11lll11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᢸ") + str(r.success) + bstack111l_opy_ (u"ࠣࠤᢹ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᢺ") + str(e) + bstack111l_opy_ (u"ࠥࠦᢻ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11l11ll1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l111l11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack11lllll1111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᢼ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᢽ") + str(req) + bstack111l_opy_ (u"ࠨࠢᢾ"))
        try:
            r = self.bstack11l11lll11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᢿ") + str(r.success) + bstack111l_opy_ (u"ࠣࠤᣀ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᣁ") + str(e) + bstack111l_opy_ (u"ࠥࠦᣂ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l111l11l1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l111lll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack11lllll1111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᣃ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣᣄ") + str(req) + bstack111l_opy_ (u"ࠨࠢᣅ"))
        try:
            r = self.bstack11l11lll11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᣆ") + str(r) + bstack111l_opy_ (u"ࠣࠤᣇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᣈ") + str(e) + bstack111l_opy_ (u"ࠥࠦᣉ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l111llll1_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l11l1l111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack11lllll1111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᣊ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴ࠿ࠦࠢᣋ") + str(req) + bstack111l_opy_ (u"ࠨࠢᣌ"))
        try:
            r = self.bstack11l11lll11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᣍ") + str(r) + bstack111l_opy_ (u"ࠣࠤᣎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᣏ") + str(e) + bstack111l_opy_ (u"ࠥࠦᣐ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1lll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l1111l1l1_opy_(self, instance: bstack1l1l111l1l1_opy_, url: str, f: bstack1l11l11l11l_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11l111l1111_opy_ = os.environ.get(bstack111l_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬᣑ"))
        if bstack11l111l1111_opy_ is not None:
            browserstack_sdk.bstack1l1ll1l1_opy_ = bstack11l111l1111_opy_.lower() == bstack111l_opy_ (u"ࠬࡺࡲࡶࡧࠪᣒ")
        bstack11l11l111l1_opy_ = version.parse(f.framework_version)
        bstack11l11l11l11_opy_ = f.platform_index
        bstack11l11l1l1l1_opy_ = kwargs.get(bstack111l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᣓ"))
        bstack11l111ll1ll_opy_ = kwargs.get(bstack111l_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᣔ"))
        bstack1lllll1ll11_opy_ = {}
        bstack11l111lll11_opy_ = {}
        bstack11l111ll111_opy_ = None
        bstack11l11l1l1ll_opy_ = {}
        if bstack11l111ll1ll_opy_ is not None or bstack11l11l1l1l1_opy_ is not None: # check top level caps
            if bstack11l111ll1ll_opy_ is not None:
                bstack11l11l1l1ll_opy_[bstack111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᣕ")] = bstack11l111ll1ll_opy_
            if bstack11l11l1l1l1_opy_ is not None and callable(getattr(bstack11l11l1l1l1_opy_, bstack111l_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᣖ"))):
                bstack11l11l1l1ll_opy_[bstack111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᣗ")] = bstack11l11l1l1l1_opy_.to_capabilities()
        response = self.bstack11l1l11ll1l_opy_(bstack11l11l11l11_opy_, url, instance.ref(), json.dumps(bstack11l11l1l1ll_opy_).encode(bstack111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᣘ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1lllll1ll11_opy_ = json.loads(response.capabilities.decode(bstack111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᣙ")))
            if browserstack_sdk.bstack1l1ll1l1_opy_:
                def bstack11l11l11lll_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l11l11lll_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1lllll1ll11_opy_ = bstack11l11l11lll_opy_(bstack1lllll1ll11_opy_)
                try:
                    bstack11l1111ll1l_opy_ = None
                    if isinstance(bstack1lllll1ll11_opy_, dict):
                        if bstack111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᣚ") in bstack1lllll1ll11_opy_:
                            bstack11l1111ll1l_opy_ = bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᣛ"))
                        elif isinstance(bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᣜ")), dict):
                            bstack11l1111ll1l_opy_ = bstack1lllll1ll11_opy_[bstack111l_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᣝ")].get(bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᣞ"))
                        if isinstance(bstack11l1111ll1l_opy_, dict) and bstack111l_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪᣟ") in bstack11l1111ll1l_opy_:
                            self.logger.debug(bstack111l_opy_ (u"ࠧࡘࡥ࡮ࡱࡹ࡭ࡳ࡭ࠠࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡳࡱࡰࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹࡵࠠࡩࡷࡥࠦᣠ"))
                            try:
                                bstack11l1111ll1l_opy_.pop(bstack111l_opy_ (u"࠭࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠬᣡ"), None)
                            except Exception:
                                pass
                            if bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᣢ") in bstack1lllll1ll11_opy_:
                                bstack1lllll1ll11_opy_[bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᣣ")] = bstack11l1111ll1l_opy_
                            if isinstance(bstack1lllll1ll11_opy_.get(bstack111l_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᣤ")), dict):
                                bstack1lllll1ll11_opy_[bstack111l_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᣥ")][bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᣦ")] = bstack11l1111ll1l_opy_
                except Exception:
                    pass
            if not bstack1lllll1ll11_opy_ and not browserstack_sdk.bstack1l1ll1l1_opy_:
                return
            bstack11l111ll111_opy_ = f.bstack1l11l111l11_opy_[bstack111l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤᣧ")](bstack1lllll1ll11_opy_)
        if bstack11l11l1l1l1_opy_ is not None and bstack11l11l111l1_opy_ >= version.parse(bstack111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᣨ")):
            bstack11l111lll11_opy_ = None
        if (
                not bstack11l11l1l1l1_opy_ and not bstack11l111ll1ll_opy_
        ) or (
                bstack11l11l111l1_opy_ < version.parse(bstack111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᣩ"))
        ):
            bstack11l111lll11_opy_ = {}
            bstack11l111lll11_opy_.update(bstack1lllll1ll11_opy_)
        self.logger.info(bstack111lllllll_opy_)
        if browserstack_sdk.bstack1l1ll1l1_opy_:
            bstack11l11l1ll1l_opy_ = bstack11l111ll111_opy_ if bstack11l111ll111_opy_ else bstack11l11l1l1l1_opy_
            if bstack11l11l1ll1l_opy_:
                bstack1lllllllll1_opy_ = bstack11111lll11_opy_(bstack11l11l1ll1l_opy_, bstack11ll11l111_opy_=bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᣪ"))
                if bstack11l11l1ll1l_opy_ is bstack11l11l1l1l1_opy_ and not bstack11l111ll111_opy_:
                    bstack11l111ll111_opy_ = bstack11l11l1ll1l_opy_
            kwargs.update({bstack111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᣫ"): bstack111ll1lll_opy_})
        elif os.environ.get(bstack111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᣬ")).lower().__eq__(bstack111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᣭ")):
            kwargs.update({bstack111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᣮ"): f.bstack11l1111llll_opy_})
        if bstack11l11l111l1_opy_ >= version.parse(bstack111l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᣯ")):
            if bstack11l111ll1ll_opy_ is not None:
                del kwargs[bstack111l_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᣰ")]
            kwargs.update(
                {
                    bstack111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᣱ"): bstack11l111ll111_opy_,
                    bstack111l_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᣲ"): True,
                    bstack111l_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᣳ"): None,
                }
            )
        elif bstack11l11l111l1_opy_ >= version.parse(bstack111l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᣴ")):
            kwargs.update(
                {
                    bstack111l_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᣵ"): bstack11l111lll11_opy_,
                    bstack111l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢ᣶"): bstack11l111ll111_opy_,
                    bstack111l_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦ᣷"): True,
                    bstack111l_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣ᣸"): None,
                }
            )
        elif bstack11l11l111l1_opy_ >= version.parse(bstack111l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ᣹")):
            kwargs.update(
                {
                    bstack111l_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᣺"): bstack11l111lll11_opy_,
                    bstack111l_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣ᣻"): True,
                    bstack111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧ᣼"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack111l_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᣽"): bstack11l111lll11_opy_,
                    bstack111l_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦ᣾"): True,
                    bstack111l_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣ᣿"): None,
                }
            )