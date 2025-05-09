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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import (
    bstack1lllllll1l1_opy_,
    bstack1llllllll1l_opy_,
    bstack111111l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll1ll1lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1llll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
class bstack1lllll1ll1l_opy_(bstack1lll1l1lll1_opy_):
    bstack1l1l11ll1ll_opy_ = bstack11lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨኺ")
    bstack1l1l1l111l1_opy_ = bstack11lll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣኻ")
    bstack1l1l11ll111_opy_ = bstack11lll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣኼ")
    def __init__(self, bstack1ll1lllll1l_opy_):
        super().__init__()
        bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.bstack11111ll11l_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1l1l11l11l1_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.bstack11111lll1l_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1ll11ll11ll_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.bstack11111lll1l_opy_, bstack1llllllll1l_opy_.POST), self.bstack1l1l111llll_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.bstack11111lll1l_opy_, bstack1llllllll1l_opy_.POST), self.bstack1l1l11lll1l_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.QUIT, bstack1llllllll1l_opy_.POST), self.bstack1l1l111ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l11l1_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦኽ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨኾ")), str):
                    url = kwargs.get(bstack11lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ኿"))
                else:
                    url = kwargs.get(bstack11lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣዀ"))._client_config.remote_server_addr
            except Exception as e:
                url = bstack11lll_opy_ (u"࠭ࠧ዁")
                self.logger.error(bstack11lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡳ࡮ࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࢁࠧዂ").format(e))
            self.bstack1l1l11llll1_opy_(instance, url, f, kwargs)
            self.logger.debug(bstack11lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡪ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዃ") + str(kwargs) + bstack11lll_opy_ (u"ࠤࠥዄ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11ll11ll_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack111111l1l1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1l11ll1ll_opy_, False):
            return
        if not f.bstack11111ll111_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l1l111l_opy_):
            return
        platform_index = f.bstack111111l1l1_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l1l111l_opy_)
        if f.bstack1ll1l11ll1l_opy_(method_name, *args) and len(args) > 1:
            bstack111ll1lll_opy_ = datetime.now()
            hub_url = bstack1lll1ll1lll_opy_.hub_url(driver)
            self.logger.warning(bstack11lll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧዅ") + str(hub_url) + bstack11lll_opy_ (u"ࠦࠧ዆"))
            bstack1l1l11l1lll_opy_ = args[1][bstack11lll_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ዇")] if isinstance(args[1], dict) and bstack11lll_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧወ") in args[1] else None
            bstack1l1l11lll11_opy_ = bstack11lll_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧዉ")
            if isinstance(bstack1l1l11l1lll_opy_, dict):
                bstack111ll1lll_opy_ = datetime.now()
                r = self.bstack1l1l1l1111l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨዊ"), datetime.now() - bstack111ll1lll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11lll_opy_ (u"ࠤࡶࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨ࠼ࠣࠦዋ") + str(r) + bstack11lll_opy_ (u"ࠥࠦዌ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l1l11l1l_opy_(instance, driver, r.hub_url)
                        f.bstack11111llll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1l11ll1ll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥው"), e)
    def bstack1l1l111llll_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1ll1lll_opy_.session_id(driver)
            if session_id:
                bstack1l1l11l111l_opy_ = bstack11lll_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢዎ").format(session_id)
                bstack1ll1llllll1_opy_.mark(bstack1l1l11l111l_opy_)
    def bstack1l1l11lll1l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111111l1l1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1l1l111l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1ll1lll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥዏ") + str(hub_url) + bstack11lll_opy_ (u"ࠢࠣዐ"))
            return
        framework_session_id = bstack1lll1ll1lll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦዑ") + str(framework_session_id) + bstack11lll_opy_ (u"ࠤࠥዒ"))
            return
        if bstack1lll1ll1lll_opy_.bstack1l1l11l1l1l_opy_(*args) == bstack1lll1ll1lll_opy_.bstack1l1l1l11l11_opy_:
            bstack1l1l11l11ll_opy_ = bstack11lll_opy_ (u"ࠥࡿࢂࡀࡥ࡯ࡦࠥዓ").format(framework_session_id)
            bstack1l1l11l111l_opy_ = bstack11lll_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨዔ").format(framework_session_id)
            bstack1ll1llllll1_opy_.end(
                label=bstack11lll_opy_ (u"ࠧࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠣዕ"),
                start=bstack1l1l11l111l_opy_,
                end=bstack1l1l11l11ll_opy_,
                status=True,
                failure=None
            )
            bstack111ll1lll_opy_ = datetime.now()
            r = self.bstack1l1l1l111ll_opy_(
                ref,
                f.bstack111111l1l1_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l1l111l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧዖ"), datetime.now() - bstack111ll1lll_opy_)
            f.bstack11111llll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1l1l111l1_opy_, r.success)
    def bstack1l1l111ll1l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111111l1l1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1l11ll111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1ll1lll_opy_.session_id(driver)
        hub_url = bstack1lll1ll1lll_opy_.hub_url(driver)
        bstack111ll1lll_opy_ = datetime.now()
        r = self.bstack1l1l11l1111_opy_(
            ref,
            f.bstack111111l1l1_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l1l111l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧ዗"), datetime.now() - bstack111ll1lll_opy_)
        f.bstack11111llll1_opy_(instance, bstack1lllll1ll1l_opy_.bstack1l1l11ll111_opy_, r.success)
    @measure(event_name=EVENTS.bstack111111l1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1l1l1llll1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11lll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨዘ") + str(req) + bstack11lll_opy_ (u"ࠤࠥዙ"))
        try:
            r = self.bstack1llllll1l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11lll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨዚ") + str(r.success) + bstack11lll_opy_ (u"ࠦࠧዛ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥዜ") + str(e) + bstack11lll_opy_ (u"ࠨࠢዝ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l111lll1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1l1l1l1111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11llll11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11lll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤዞ") + str(req) + bstack11lll_opy_ (u"ࠣࠤዟ"))
        try:
            r = self.bstack1llllll1l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧዠ") + str(r.success) + bstack11lll_opy_ (u"ࠥࠦዡ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤዢ") + str(e) + bstack11lll_opy_ (u"ࠧࠨዣ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll1l1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1l1l1l111ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11llll11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤዤ") + str(req) + bstack11lll_opy_ (u"ࠢࠣዥ"))
        try:
            r = self.bstack1llllll1l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥዦ") + str(r) + bstack11lll_opy_ (u"ࠤࠥዧ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣየ") + str(e) + bstack11lll_opy_ (u"ࠦࠧዩ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1l111_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1l1l11l1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11llll11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11lll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴ࠿ࠦࠢዪ") + str(req) + bstack11lll_opy_ (u"ࠨࠢያ"))
        try:
            r = self.bstack1llllll1l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤዬ") + str(r) + bstack11lll_opy_ (u"ࠣࠤይ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢዮ") + str(e) + bstack11lll_opy_ (u"ࠥࠦዯ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll111ll_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1l1l11llll1_opy_(self, instance: bstack111111l1ll_opy_, url: str, f: bstack1lll1ll1lll_opy_, kwargs):
        bstack1l1l1l11111_opy_ = version.parse(f.framework_version)
        bstack1l1l11lllll_opy_ = kwargs.get(bstack11lll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧደ"))
        bstack1l1l11l1ll1_opy_ = kwargs.get(bstack11lll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧዱ"))
        bstack1l1ll111lll_opy_ = {}
        bstack1l1l1l11lll_opy_ = {}
        bstack1l1l11ll11l_opy_ = None
        bstack1l1l1l11ll1_opy_ = {}
        if bstack1l1l11l1ll1_opy_ is not None or bstack1l1l11lllll_opy_ is not None: # check top level caps
            if bstack1l1l11l1ll1_opy_ is not None:
                bstack1l1l1l11ll1_opy_[bstack11lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ዲ")] = bstack1l1l11l1ll1_opy_
            if bstack1l1l11lllll_opy_ is not None and callable(getattr(bstack1l1l11lllll_opy_, bstack11lll_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤዳ"))):
                bstack1l1l1l11ll1_opy_[bstack11lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫዴ")] = bstack1l1l11lllll_opy_.to_capabilities()
        response = self.bstack1l1l1llll1l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1l1l11ll1_opy_).encode(bstack11lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣድ")))
        if response is not None and response.capabilities:
            bstack1l1ll111lll_opy_ = json.loads(response.capabilities.decode(bstack11lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤዶ")))
            if not bstack1l1ll111lll_opy_: # empty caps bstack1l1l1lll1ll_opy_ bstack1l1ll11111l_opy_ bstack1l1ll111l1l_opy_ bstack1lll1l1l1l1_opy_ or error in processing
                return
            bstack1l1l11ll11l_opy_ = f.bstack1lll11ll111_opy_[bstack11lll_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣዷ")](bstack1l1ll111lll_opy_)
        if bstack1l1l11lllll_opy_ is not None and bstack1l1l1l11111_opy_ >= version.parse(bstack11lll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫዸ")):
            bstack1l1l1l11lll_opy_ = None
        if (
                not bstack1l1l11lllll_opy_ and not bstack1l1l11l1ll1_opy_
        ) or (
                bstack1l1l1l11111_opy_ < version.parse(bstack11lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬዹ"))
        ):
            bstack1l1l1l11lll_opy_ = {}
            bstack1l1l1l11lll_opy_.update(bstack1l1ll111lll_opy_)
        self.logger.info(bstack1lll1llll1_opy_)
        if os.environ.get(bstack11lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠥዺ")).lower().__eq__(bstack11lll_opy_ (u"ࠣࡶࡵࡹࡪࠨዻ")):
            kwargs.update(
                {
                    bstack11lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧዼ"): f.bstack1l1l11l1l11_opy_,
                }
            )
        if bstack1l1l1l11111_opy_ >= version.parse(bstack11lll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪዽ")):
            if bstack1l1l11l1ll1_opy_ is not None:
                del kwargs[bstack11lll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዾ")]
            kwargs.update(
                {
                    bstack11lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨዿ"): bstack1l1l11ll11l_opy_,
                    bstack11lll_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥጀ"): True,
                    bstack11lll_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢጁ"): None,
                }
            )
        elif bstack1l1l1l11111_opy_ >= version.parse(bstack11lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧጂ")):
            kwargs.update(
                {
                    bstack11lll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጃ"): bstack1l1l1l11lll_opy_,
                    bstack11lll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦጄ"): bstack1l1l11ll11l_opy_,
                    bstack11lll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣጅ"): True,
                    bstack11lll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧጆ"): None,
                }
            )
        elif bstack1l1l1l11111_opy_ >= version.parse(bstack11lll_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ጇ")):
            kwargs.update(
                {
                    bstack11lll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢገ"): bstack1l1l1l11lll_opy_,
                    bstack11lll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧጉ"): True,
                    bstack11lll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤጊ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11lll_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጋ"): bstack1l1l1l11lll_opy_,
                    bstack11lll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣጌ"): True,
                    bstack11lll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧግ"): None,
                }
            )