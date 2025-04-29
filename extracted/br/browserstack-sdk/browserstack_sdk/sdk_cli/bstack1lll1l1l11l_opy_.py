# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll1ll11l_opy_ import bstack1ll1llll1l1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import (
    bstack11111lll11_opy_,
    bstack1111111l1l_opy_,
    bstack111111ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lllll1_opy_ import bstack1lll11ll1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lllllll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1llll1l1_opy_ import bstack1lll1llll1l_opy_
class bstack1llllll1111_opy_(bstack1ll1llll1l1_opy_):
    bstack1l1l111llll_opy_ = bstack1llllll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨኺ")
    bstack1l1l11l1111_opy_ = bstack1llllll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣኻ")
    bstack1l1l11l11ll_opy_ = bstack1llllll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣኼ")
    def __init__(self, bstack1lllll11lll_opy_):
        super().__init__()
        bstack1lll11ll1ll_opy_.bstack1ll1l111l1l_opy_((bstack11111lll11_opy_.bstack1111111l11_opy_, bstack1111111l1l_opy_.PRE), self.bstack1l1l11l1l11_opy_)
        bstack1lll11ll1ll_opy_.bstack1ll1l111l1l_opy_((bstack11111lll11_opy_.bstack11111l111l_opy_, bstack1111111l1l_opy_.PRE), self.bstack1ll11ll1l11_opy_)
        bstack1lll11ll1ll_opy_.bstack1ll1l111l1l_opy_((bstack11111lll11_opy_.bstack11111l111l_opy_, bstack1111111l1l_opy_.POST), self.bstack1l1l1l1l111_opy_)
        bstack1lll11ll1ll_opy_.bstack1ll1l111l1l_opy_((bstack11111lll11_opy_.bstack11111l111l_opy_, bstack1111111l1l_opy_.POST), self.bstack1l1l11ll11l_opy_)
        bstack1lll11ll1ll_opy_.bstack1ll1l111l1l_opy_((bstack11111lll11_opy_.QUIT, bstack1111111l1l_opy_.POST), self.bstack1l1l11l1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l1l11_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1llllll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦኽ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1l11lll11_opy_(instance, f, kwargs)
            self.logger.debug(bstack1llllll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀ࡬࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾ࠼ࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኾ") + str(kwargs) + bstack1llllll_opy_ (u"ࠦࠧ኿"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11ll1l11_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack111111lll1_opy_(instance, bstack1llllll1111_opy_.bstack1l1l111llll_opy_, False):
            return
        if not f.bstack11111lll1l_opy_(instance, bstack1lll11ll1ll_opy_.bstack1ll11lll1l1_opy_):
            return
        platform_index = f.bstack111111lll1_opy_(instance, bstack1lll11ll1ll_opy_.bstack1ll11lll1l1_opy_)
        if f.bstack1ll11lll1ll_opy_(method_name, *args) and len(args) > 1:
            bstack11l1ll1l1_opy_ = datetime.now()
            hub_url = bstack1lll11ll1ll_opy_.hub_url(driver)
            self.logger.warning(bstack1llllll_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢዀ") + str(hub_url) + bstack1llllll_opy_ (u"ࠨࠢ዁"))
            bstack1l1l11ll111_opy_ = args[1][bstack1llllll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨዂ")] if isinstance(args[1], dict) and bstack1llllll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢዃ") in args[1] else None
            bstack1l1l11l11l1_opy_ = bstack1llllll_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢዄ")
            if isinstance(bstack1l1l11ll111_opy_, dict):
                bstack11l1ll1l1_opy_ = datetime.now()
                r = self.bstack1l1l1l11111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lll11111_opy_(bstack1llllll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣዅ"), datetime.now() - bstack11l1ll1l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1llllll_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨ዆") + str(r) + bstack1llllll_opy_ (u"ࠧࠨ዇"))
                        return
                    if r.hub_url:
                        f.bstack1l1l1l11ll1_opy_(instance, driver, r.hub_url)
                        f.bstack1111l11lll_opy_(instance, bstack1llllll1111_opy_.bstack1l1l111llll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1llllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧወ"), e)
    def bstack1l1l1l1l111_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll11ll1ll_opy_.session_id(driver)
            if session_id:
                bstack1l1l1l111l1_opy_ = bstack1llllll_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤዉ").format(session_id)
                bstack1lll1llll1l_opy_.mark(bstack1l1l1l111l1_opy_)
    def bstack1l1l11ll11l_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111111lll1_opy_(instance, bstack1llllll1111_opy_.bstack1l1l11l1111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll11ll1ll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1llllll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧዊ") + str(hub_url) + bstack1llllll_opy_ (u"ࠤࠥዋ"))
            return
        framework_session_id = bstack1lll11ll1ll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1llllll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨዌ") + str(framework_session_id) + bstack1llllll_opy_ (u"ࠦࠧው"))
            return
        if bstack1lll11ll1ll_opy_.bstack1l1l11l1l1l_opy_(*args) == bstack1lll11ll1ll_opy_.bstack1l1l1l11lll_opy_:
            bstack1l1l11l1lll_opy_ = bstack1llllll_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧዎ").format(framework_session_id)
            bstack1l1l1l111l1_opy_ = bstack1llllll_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣዏ").format(framework_session_id)
            bstack1lll1llll1l_opy_.end(
                label=bstack1llllll_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥዐ"),
                start=bstack1l1l1l111l1_opy_,
                end=bstack1l1l11l1lll_opy_,
                status=True,
                failure=None
            )
            bstack11l1ll1l1_opy_ = datetime.now()
            r = self.bstack1l1l1l1l1l1_opy_(
                ref,
                f.bstack111111lll1_opy_(instance, bstack1lll11ll1ll_opy_.bstack1ll11lll1l1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lll11111_opy_(bstack1llllll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢዑ"), datetime.now() - bstack11l1ll1l1_opy_)
            f.bstack1111l11lll_opy_(instance, bstack1llllll1111_opy_.bstack1l1l11l1111_opy_, r.success)
    def bstack1l1l11l1ll1_opy_(
        self,
        f: bstack1lll11ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack111111ll11_opy_, str],
        bstack1111111lll_opy_: Tuple[bstack11111lll11_opy_, bstack1111111l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack111111lll1_opy_(instance, bstack1llllll1111_opy_.bstack1l1l11l11ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll11ll1ll_opy_.session_id(driver)
        hub_url = bstack1lll11ll1ll_opy_.hub_url(driver)
        bstack11l1ll1l1_opy_ = datetime.now()
        r = self.bstack1l1l1l11l1l_opy_(
            ref,
            f.bstack111111lll1_opy_(instance, bstack1lll11ll1ll_opy_.bstack1ll11lll1l1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lll11111_opy_(bstack1llllll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢዒ"), datetime.now() - bstack11l1ll1l1_opy_)
        f.bstack1111l11lll_opy_(instance, bstack1llllll1111_opy_.bstack1l1l11l11ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l11lll1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l1ll1111l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1llllll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣዓ") + str(req) + bstack1llllll_opy_ (u"ࠦࠧዔ"))
        try:
            r = self.bstack1lllll1llll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1llllll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣዕ") + str(r.success) + bstack1llllll_opy_ (u"ࠨࠢዖ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llllll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ዗") + str(e) + bstack1llllll_opy_ (u"ࠣࠤዘ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11llll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l1l1l11111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1llllll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦዙ") + str(req) + bstack1llllll_opy_ (u"ࠥࠦዚ"))
        try:
            r = self.bstack1lllll1llll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1llllll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢዛ") + str(r.success) + bstack1llllll_opy_ (u"ࠧࠨዜ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llllll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦዝ") + str(e) + bstack1llllll_opy_ (u"ࠢࠣዞ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l11l11_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l1l1l1l1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1llllll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦዟ") + str(req) + bstack1llllll_opy_ (u"ࠤࠥዠ"))
        try:
            r = self.bstack1lllll1llll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1llllll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧዡ") + str(r) + bstack1llllll_opy_ (u"ࠦࠧዢ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llllll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥዣ") + str(e) + bstack1llllll_opy_ (u"ࠨࠢዤ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1111l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l1l1l11l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1ll11lll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1llllll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤዥ") + str(req) + bstack1llllll_opy_ (u"ࠣࠤዦ"))
        try:
            r = self.bstack1lllll1llll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1llllll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦዧ") + str(r) + bstack1llllll_opy_ (u"ࠥࠦየ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1llllll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤዩ") + str(e) + bstack1llllll_opy_ (u"ࠧࠨዪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l11l1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l1l11lll11_opy_(self, instance: bstack111111ll11_opy_, f: bstack1lll11ll1ll_opy_, kwargs):
        bstack1l1l11lllll_opy_ = version.parse(f.framework_version)
        bstack1l1l11ll1ll_opy_ = kwargs.get(bstack1llllll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢያ"))
        bstack1l1l1l111ll_opy_ = kwargs.get(bstack1llllll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢዬ"))
        bstack1l1ll11111l_opy_ = {}
        bstack1l1l1l1l11l_opy_ = {}
        bstack1l1l11lll1l_opy_ = None
        bstack1l1l11ll1l1_opy_ = {}
        if bstack1l1l1l111ll_opy_ is not None or bstack1l1l11ll1ll_opy_ is not None: # check top level caps
            if bstack1l1l1l111ll_opy_ is not None:
                bstack1l1l11ll1l1_opy_[bstack1llllll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨይ")] = bstack1l1l1l111ll_opy_
            if bstack1l1l11ll1ll_opy_ is not None and callable(getattr(bstack1l1l11ll1ll_opy_, bstack1llllll_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዮ"))):
                bstack1l1l11ll1l1_opy_[bstack1llllll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ዯ")] = bstack1l1l11ll1ll_opy_.to_capabilities()
        response = self.bstack1l1ll1111l1_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1l11ll1l1_opy_).encode(bstack1llllll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥደ")))
        if response is not None and response.capabilities:
            bstack1l1ll11111l_opy_ = json.loads(response.capabilities.decode(bstack1llllll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦዱ")))
            if not bstack1l1ll11111l_opy_: # empty caps bstack1l1ll111l11_opy_ bstack1l1l1llll1l_opy_ bstack1l1ll11ll1l_opy_ bstack1lll1l11lll_opy_ or error in processing
                return
            bstack1l1l11lll1l_opy_ = f.bstack1llll1l1ll1_opy_[bstack1llllll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥዲ")](bstack1l1ll11111l_opy_)
        if bstack1l1l11ll1ll_opy_ is not None and bstack1l1l11lllll_opy_ >= version.parse(bstack1llllll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ዳ")):
            bstack1l1l1l1l11l_opy_ = None
        if (
                not bstack1l1l11ll1ll_opy_ and not bstack1l1l1l111ll_opy_
        ) or (
                bstack1l1l11lllll_opy_ < version.parse(bstack1llllll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧዴ"))
        ):
            bstack1l1l1l1l11l_opy_ = {}
            bstack1l1l1l1l11l_opy_.update(bstack1l1ll11111l_opy_)
        self.logger.info(bstack11lllllll1_opy_)
        if os.environ.get(bstack1llllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧድ")).lower().__eq__(bstack1llllll_opy_ (u"ࠥࡸࡷࡻࡥࠣዶ")):
            kwargs.update(
                {
                    bstack1llllll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢዷ"): f.bstack1l1l11l111l_opy_,
                }
            )
        if bstack1l1l11lllll_opy_ >= version.parse(bstack1llllll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬዸ")):
            if bstack1l1l1l111ll_opy_ is not None:
                del kwargs[bstack1llllll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨዹ")]
            kwargs.update(
                {
                    bstack1llllll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣዺ"): bstack1l1l11lll1l_opy_,
                    bstack1llllll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧዻ"): True,
                    bstack1llllll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤዼ"): None,
                }
            )
        elif bstack1l1l11lllll_opy_ >= version.parse(bstack1llllll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩዽ")):
            kwargs.update(
                {
                    bstack1llllll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዾ"): bstack1l1l1l1l11l_opy_,
                    bstack1llllll_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨዿ"): bstack1l1l11lll1l_opy_,
                    bstack1llllll_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥጀ"): True,
                    bstack1llllll_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢጁ"): None,
                }
            )
        elif bstack1l1l11lllll_opy_ >= version.parse(bstack1llllll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨጂ")):
            kwargs.update(
                {
                    bstack1llllll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጃ"): bstack1l1l1l1l11l_opy_,
                    bstack1llllll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢጄ"): True,
                    bstack1llllll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦጅ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1llllll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧጆ"): bstack1l1l1l1l11l_opy_,
                    bstack1llllll_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥጇ"): True,
                    bstack1llllll_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢገ"): None,
                }
            )