# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll11l1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
class bstack1lll1l1l1ll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1l11llll11l_opy_ = bstack11ll1l1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤጟ")
    bstack1l11llllll1_opy_ = bstack11ll1l1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦጠ")
    bstack1l11ll11l1l_opy_ = bstack11ll1l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦጡ")
    def __init__(self, bstack1ll1ll1llll_opy_):
        super().__init__()
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack11111111l1_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l11lll1111_opy_)
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1ll1111l111_opy_)
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.POST), self.bstack1l11ll1llll_opy_)
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.POST), self.bstack1l11lll1ll1_opy_)
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.QUIT, bstack1llllll1ll1_opy_.POST), self.bstack1l1l1111111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll1111_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll1l1_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢጢ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11ll1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጣ")), str):
                    url = kwargs.get(bstack11ll1l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥጤ"))
                elif hasattr(kwargs.get(bstack11ll1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦጥ")), bstack11ll1l1_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪጦ")):
                    url = kwargs.get(bstack11ll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨጧ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11ll1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢጨ"))._url
            except Exception as e:
                url = bstack11ll1l1_opy_ (u"ࠬ࠭ጩ")
                self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦጪ").format(e))
            self.logger.info(bstack11ll1l1_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣጫ").format(str(url)))
            self.bstack1l11lll1lll_opy_(instance, url, f, kwargs)
            self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁ࠿ࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨጬ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll1111l111_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack11111111ll_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1l11llll11l_opy_, False):
            return
        if not f.bstack1lllll1l111_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_):
            return
        platform_index = f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_)
        if f.bstack1ll11l1111l_opy_(method_name, *args) and len(args) > 1:
            bstack11ll11ll1_opy_ = datetime.now()
            hub_url = bstack1ll1lllllll_opy_.hub_url(driver)
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦጭ") + str(hub_url) + bstack11ll1l1_opy_ (u"ࠥࠦጮ"))
            bstack1l11ll11lll_opy_ = args[1][bstack11ll1l1_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጯ")] if isinstance(args[1], dict) and bstack11ll1l1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦጰ") in args[1] else None
            bstack1l11ll1lll1_opy_ = bstack11ll1l1_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦጱ")
            if isinstance(bstack1l11ll11lll_opy_, dict):
                bstack11ll11ll1_opy_ = datetime.now()
                r = self.bstack1l11ll1l1l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧጲ"), datetime.now() - bstack11ll11ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥጳ") + str(r) + bstack11ll1l1_opy_ (u"ࠤࠥጴ"))
                        return
                    if r.hub_url:
                        f.bstack1l11llll1l1_opy_(instance, driver, r.hub_url)
                        f.bstack1lllll1ll1l_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1l11llll11l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤጵ"), e)
    def bstack1l11ll1llll_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1lllllll_opy_.session_id(driver)
            if session_id:
                bstack1l11lll111l_opy_ = bstack11ll1l1_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨጶ").format(session_id)
                bstack1llll11lll1_opy_.mark(bstack1l11lll111l_opy_)
    def bstack1l11lll1ll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack11111111ll_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1l11llllll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1lllllll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤጷ") + str(hub_url) + bstack11ll1l1_opy_ (u"ࠨࠢጸ"))
            return
        framework_session_id = bstack1ll1lllllll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥጹ") + str(framework_session_id) + bstack11ll1l1_opy_ (u"ࠣࠤጺ"))
            return
        if bstack1ll1lllllll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1lllllll_opy_.bstack1l11ll1l111_opy_:
            bstack1l11lllll11_opy_ = bstack11ll1l1_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤጻ").format(framework_session_id)
            bstack1l11lll111l_opy_ = bstack11ll1l1_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧጼ").format(framework_session_id)
            bstack1llll11lll1_opy_.end(
                label=bstack11ll1l1_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢጽ"),
                start=bstack1l11lll111l_opy_,
                end=bstack1l11lllll11_opy_,
                status=True,
                failure=None
            )
            bstack11ll11ll1_opy_ = datetime.now()
            r = self.bstack1l11lll11ll_opy_(
                ref,
                f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦጾ"), datetime.now() - bstack11ll11ll1_opy_)
            f.bstack1lllll1ll1l_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1l11llllll1_opy_, r.success)
    def bstack1l1l1111111_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack11111111ll_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1l11ll11l1l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1lllllll_opy_.session_id(driver)
        hub_url = bstack1ll1lllllll_opy_.hub_url(driver)
        bstack11ll11ll1_opy_ = datetime.now()
        r = self.bstack1l11lll1l11_opy_(
            ref,
            f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦጿ"), datetime.now() - bstack11ll11ll1_opy_)
        f.bstack1lllll1ll1l_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1l11ll11l1l_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1l1lll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l1l11ll111_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧፀ") + str(req) + bstack11ll1l1_opy_ (u"ࠣࠤፁ"))
        try:
            r = self.bstack1lll1l1ll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧፂ") + str(r.success) + bstack11ll1l1_opy_ (u"ࠥࠦፃ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤፄ") + str(e) + bstack11ll1l1_opy_ (u"ࠧࠨፅ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11llll111_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l11ll1l1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣፆ") + str(req) + bstack11ll1l1_opy_ (u"ࠢࠣፇ"))
        try:
            r = self.bstack1lll1l1ll1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦፈ") + str(r.success) + bstack11ll1l1_opy_ (u"ࠤࠥፉ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣፊ") + str(e) + bstack11ll1l1_opy_ (u"ࠦࠧፋ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11llll1ll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l11lll11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣፌ") + str(req) + bstack11ll1l1_opy_ (u"ࠨࠢፍ"))
        try:
            r = self.bstack1lll1l1ll1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤፎ") + str(r) + bstack11ll1l1_opy_ (u"ࠣࠤፏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢፐ") + str(e) + bstack11ll1l1_opy_ (u"ࠥࠦፑ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll11l1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l11lll1l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨፒ") + str(req) + bstack11ll1l1_opy_ (u"ࠧࠨፓ"))
        try:
            r = self.bstack1lll1l1ll1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣፔ") + str(r) + bstack11ll1l1_opy_ (u"ࠢࠣፕ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨፖ") + str(e) + bstack11ll1l1_opy_ (u"ࠤࠥፗ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1ll1l1l_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l11lll1lll_opy_(self, instance: bstack1111111l1l_opy_, url: str, f: bstack1ll1lllllll_opy_, kwargs):
        bstack1l11ll1l1ll_opy_ = version.parse(f.framework_version)
        bstack1l11lll1l1l_opy_ = kwargs.get(bstack11ll1l1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦፘ"))
        bstack1l11ll1ll1l_opy_ = kwargs.get(bstack11ll1l1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦፙ"))
        bstack1l1l1l11l1l_opy_ = {}
        bstack1l11lllllll_opy_ = {}
        bstack1l11lllll1l_opy_ = None
        bstack1l11ll11ll1_opy_ = {}
        if bstack1l11ll1ll1l_opy_ is not None or bstack1l11lll1l1l_opy_ is not None: # check top level caps
            if bstack1l11ll1ll1l_opy_ is not None:
                bstack1l11ll11ll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬፚ")] = bstack1l11ll1ll1l_opy_
            if bstack1l11lll1l1l_opy_ is not None and callable(getattr(bstack1l11lll1l1l_opy_, bstack11ll1l1_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ፛"))):
                bstack1l11ll11ll1_opy_[bstack11ll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ፜")] = bstack1l11lll1l1l_opy_.to_capabilities()
        response = self.bstack1l1l11ll111_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll11ll1_opy_).encode(bstack11ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ፝")))
        if response is not None and response.capabilities:
            bstack1l1l1l11l1l_opy_ = json.loads(response.capabilities.decode(bstack11ll1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ፞")))
            if not bstack1l1l1l11l1l_opy_: # empty caps bstack1l1l11ll11l_opy_ bstack1l1l1l111ll_opy_ bstack1l1l1l111l1_opy_ bstack1ll1lllll11_opy_ or error in processing
                return
            bstack1l11lllll1l_opy_ = f.bstack1ll1llll1l1_opy_[bstack11ll1l1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢ፟")](bstack1l1l1l11l1l_opy_)
        if bstack1l11lll1l1l_opy_ is not None and bstack1l11ll1l1ll_opy_ >= version.parse(bstack11ll1l1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ፠")):
            bstack1l11lllllll_opy_ = None
        if (
                not bstack1l11lll1l1l_opy_ and not bstack1l11ll1ll1l_opy_
        ) or (
                bstack1l11ll1l1ll_opy_ < version.parse(bstack11ll1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ፡"))
        ):
            bstack1l11lllllll_opy_ = {}
            bstack1l11lllllll_opy_.update(bstack1l1l1l11l1l_opy_)
        self.logger.info(bstack1ll11l1ll1_opy_)
        if os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤ።")).lower().__eq__(bstack11ll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ፣")):
            kwargs.update(
                {
                    bstack11ll1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፤"): f.bstack1l11ll1ll11_opy_,
                }
            )
        if bstack1l11ll1l1ll_opy_ >= version.parse(bstack11ll1l1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ፥")):
            if bstack1l11ll1ll1l_opy_ is not None:
                del kwargs[bstack11ll1l1_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ፦")]
            kwargs.update(
                {
                    bstack11ll1l1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧ፧"): bstack1l11lllll1l_opy_,
                    bstack11ll1l1_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤ፨"): True,
                    bstack11ll1l1_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨ፩"): None,
                }
            )
        elif bstack1l11ll1l1ll_opy_ >= version.parse(bstack11ll1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭፪")):
            kwargs.update(
                {
                    bstack11ll1l1_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ፫"): bstack1l11lllllll_opy_,
                    bstack11ll1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥ፬"): bstack1l11lllll1l_opy_,
                    bstack11ll1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢ፭"): True,
                    bstack11ll1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦ፮"): None,
                }
            )
        elif bstack1l11ll1l1ll_opy_ >= version.parse(bstack11ll1l1_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ፯")):
            kwargs.update(
                {
                    bstack11ll1l1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ፰"): bstack1l11lllllll_opy_,
                    bstack11ll1l1_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦ፱"): True,
                    bstack11ll1l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣ፲"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11ll1l1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ፳"): bstack1l11lllllll_opy_,
                    bstack11ll1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢ፴"): True,
                    bstack11ll1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦ፵"): None,
                }
            )