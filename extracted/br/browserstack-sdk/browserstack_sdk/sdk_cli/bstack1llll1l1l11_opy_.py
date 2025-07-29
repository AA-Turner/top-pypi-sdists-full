# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llllllll1l_opy_,
    bstack11111111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1l1lll11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll11l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
class bstack1llll11l11l_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l11ll1lll1_opy_ = bstackl_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤ፞")
    bstack1l11ll111l1_opy_ = bstackl_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦ፟")
    bstack1l11ll11111_opy_ = bstackl_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦ፠")
    def __init__(self, bstack1llll111ll1_opy_):
        super().__init__()
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1lllll1l1l1_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1l11llll11l_opy_)
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1ll11111ll1_opy_)
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.POST), self.bstack1l11ll1111l_opy_)
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.POST), self.bstack1l11lll111l_opy_)
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.QUIT, bstack1llllllll1l_opy_.POST), self.bstack1l11ll11lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11llll11l_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstackl_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢ፡"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstackl_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ።")), str):
                    url = kwargs.get(bstackl_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ፣"))
                elif hasattr(kwargs.get(bstackl_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፤")), bstackl_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪ፥")):
                    url = kwargs.get(bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ፦"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstackl_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፧"))._url
            except Exception as e:
                url = bstackl_opy_ (u"ࠬ࠭፨")
                self.logger.error(bstackl_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦ፩").format(e))
            self.logger.info(bstackl_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣ፪").format(str(url)))
            self.bstack1l11l1llll1_opy_(instance, url, f, kwargs)
            self.logger.info(bstackl_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁ࠿ࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨ፫").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11111ll1_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llllll1l1l_opy_(instance, bstack1llll11l11l_opy_.bstack1l11ll1lll1_opy_, False):
            return
        if not f.bstack1lllll11111_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_):
            return
        platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_)
        if f.bstack1ll1111ll1l_opy_(method_name, *args) and len(args) > 1:
            bstack1l1ll11l1_opy_ = datetime.now()
            hub_url = bstack1ll1l1lll11_opy_.hub_url(driver)
            self.logger.warning(bstackl_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦ፬") + str(hub_url) + bstackl_opy_ (u"ࠥࠦ፭"))
            bstack1l11l1lllll_opy_ = args[1][bstackl_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ፮")] if isinstance(args[1], dict) and bstackl_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ፯") in args[1] else None
            bstack1l11lll11ll_opy_ = bstackl_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦ፰")
            if isinstance(bstack1l11l1lllll_opy_, dict):
                bstack1l1ll11l1_opy_ = datetime.now()
                r = self.bstack1l11ll1ll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧ፱"), datetime.now() - bstack1l1ll11l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstackl_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥ፲") + str(r) + bstackl_opy_ (u"ࠤࠥ፳"))
                        return
                    if r.hub_url:
                        f.bstack1l11lll11l1_opy_(instance, driver, r.hub_url)
                        f.bstack1lllllllll1_opy_(instance, bstack1llll11l11l_opy_.bstack1l11ll1lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstackl_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ፴"), e)
    def bstack1l11ll1111l_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1l1lll11_opy_.session_id(driver)
            if session_id:
                bstack1l11lll1ll1_opy_ = bstackl_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨ፵").format(session_id)
                bstack1lll11lll1l_opy_.mark(bstack1l11lll1ll1_opy_)
    def bstack1l11lll111l_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllll1l1l_opy_(instance, bstack1llll11l11l_opy_.bstack1l11ll111l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1l1lll11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstackl_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤ፶") + str(hub_url) + bstackl_opy_ (u"ࠨࠢ፷"))
            return
        framework_session_id = bstack1ll1l1lll11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstackl_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥ፸") + str(framework_session_id) + bstackl_opy_ (u"ࠣࠤ፹"))
            return
        if bstack1ll1l1lll11_opy_.bstack1l11llll111_opy_(*args) == bstack1ll1l1lll11_opy_.bstack1l11ll1llll_opy_:
            bstack1l11ll11l1l_opy_ = bstackl_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤ፺").format(framework_session_id)
            bstack1l11lll1ll1_opy_ = bstackl_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧ፻").format(framework_session_id)
            bstack1lll11lll1l_opy_.end(
                label=bstackl_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢ፼"),
                start=bstack1l11lll1ll1_opy_,
                end=bstack1l11ll11l1l_opy_,
                status=True,
                failure=None
            )
            bstack1l1ll11l1_opy_ = datetime.now()
            r = self.bstack1l11lll1lll_opy_(
                ref,
                f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦ፽"), datetime.now() - bstack1l1ll11l1_opy_)
            f.bstack1lllllllll1_opy_(instance, bstack1llll11l11l_opy_.bstack1l11ll111l1_opy_, r.success)
    def bstack1l11ll11lll_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllll1l1l_opy_(instance, bstack1llll11l11l_opy_.bstack1l11ll11111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1l1lll11_opy_.session_id(driver)
        hub_url = bstack1ll1l1lll11_opy_.hub_url(driver)
        bstack1l1ll11l1_opy_ = datetime.now()
        r = self.bstack1l11lll1111_opy_(
            ref,
            f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦ፾"), datetime.now() - bstack1l1ll11l1_opy_)
        f.bstack1lllllllll1_opy_(instance, bstack1llll11l11l_opy_.bstack1l11ll11111_opy_, r.success)
    @measure(event_name=EVENTS.bstack11l1l1ll1_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l1l11ll11l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstackl_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧ፿") + str(req) + bstackl_opy_ (u"ࠣࠤᎀ"))
        try:
            r = self.bstack1lll1l1l1ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstackl_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᎁ") + str(r.success) + bstackl_opy_ (u"ࠥࠦᎂ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᎃ") + str(e) + bstackl_opy_ (u"ࠧࠨᎄ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll11ll1_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l11ll1ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstackl_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᎅ") + str(req) + bstackl_opy_ (u"ࠢࠣᎆ"))
        try:
            r = self.bstack1lll1l1l1ll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstackl_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᎇ") + str(r.success) + bstackl_opy_ (u"ࠤࠥᎈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᎉ") + str(e) + bstackl_opy_ (u"ࠦࠧᎊ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1l1ll_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l11lll1lll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstackl_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣᎋ") + str(req) + bstackl_opy_ (u"ࠨࠢᎌ"))
        try:
            r = self.bstack1lll1l1l1ll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstackl_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᎍ") + str(r) + bstackl_opy_ (u"ࠣࠤᎎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎏ") + str(e) + bstackl_opy_ (u"ࠥࠦ᎐"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll1l1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l11lll1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstackl_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨ᎑") + str(req) + bstackl_opy_ (u"ࠧࠨ᎒"))
        try:
            r = self.bstack1lll1l1l1ll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstackl_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ᎓") + str(r) + bstackl_opy_ (u"ࠢࠣ᎔"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᎕") + str(e) + bstackl_opy_ (u"ࠤࠥ᎖"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll1_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l11l1llll1_opy_(self, instance: bstack11111111l1_opy_, url: str, f: bstack1ll1l1lll11_opy_, kwargs):
        bstack1l11ll1l111_opy_ = version.parse(f.framework_version)
        bstack1l11ll1l1l1_opy_ = kwargs.get(bstackl_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦ᎗"))
        bstack1l11lll1l11_opy_ = kwargs.get(bstackl_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᎘"))
        bstack1l1l11ll111_opy_ = {}
        bstack1l11ll1ll11_opy_ = {}
        bstack1l11ll111ll_opy_ = None
        bstack1l11ll1l11l_opy_ = {}
        if bstack1l11lll1l11_opy_ is not None or bstack1l11ll1l1l1_opy_ is not None: # check top level caps
            if bstack1l11lll1l11_opy_ is not None:
                bstack1l11ll1l11l_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᎙")] = bstack1l11lll1l11_opy_
            if bstack1l11ll1l1l1_opy_ is not None and callable(getattr(bstack1l11ll1l1l1_opy_, bstackl_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᎚"))):
                bstack1l11ll1l11l_opy_[bstackl_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᎛")] = bstack1l11ll1l1l1_opy_.to_capabilities()
        response = self.bstack1l1l11ll11l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll1l11l_opy_).encode(bstackl_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᎜")))
        if response is not None and response.capabilities:
            bstack1l1l11ll111_opy_ = json.loads(response.capabilities.decode(bstackl_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᎝")))
            if not bstack1l1l11ll111_opy_: # empty caps bstack1l1l11l1l11_opy_ bstack1l1l111ll11_opy_ bstack1l1l11lll1l_opy_ bstack1llll11l1l1_opy_ or error in processing
                return
            bstack1l11ll111ll_opy_ = f.bstack1lll1111ll1_opy_[bstackl_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢ᎞")](bstack1l1l11ll111_opy_)
        if bstack1l11ll1l1l1_opy_ is not None and bstack1l11ll1l111_opy_ >= version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ᎟")):
            bstack1l11ll1ll11_opy_ = None
        if (
                not bstack1l11ll1l1l1_opy_ and not bstack1l11lll1l11_opy_
        ) or (
                bstack1l11ll1l111_opy_ < version.parse(bstackl_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᎠ"))
        ):
            bstack1l11ll1ll11_opy_ = {}
            bstack1l11ll1ll11_opy_.update(bstack1l1l11ll111_opy_)
        self.logger.info(bstack1lll11l11l_opy_)
        if os.environ.get(bstackl_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤᎡ")).lower().__eq__(bstackl_opy_ (u"ࠢࡵࡴࡸࡩࠧᎢ")):
            kwargs.update(
                {
                    bstackl_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᎣ"): f.bstack1l11ll11l11_opy_,
                }
            )
        if bstack1l11ll1l111_opy_ >= version.parse(bstackl_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᎤ")):
            if bstack1l11lll1l11_opy_ is not None:
                del kwargs[bstackl_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᎥ")]
            kwargs.update(
                {
                    bstackl_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᎦ"): bstack1l11ll111ll_opy_,
                    bstackl_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᎧ"): True,
                    bstackl_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᎨ"): None,
                }
            )
        elif bstack1l11ll1l111_opy_ >= version.parse(bstackl_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭Ꭹ")):
            kwargs.update(
                {
                    bstackl_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎪ"): bstack1l11ll1ll11_opy_,
                    bstackl_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᎫ"): bstack1l11ll111ll_opy_,
                    bstackl_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᎬ"): True,
                    bstackl_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᎭ"): None,
                }
            )
        elif bstack1l11ll1l111_opy_ >= version.parse(bstackl_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᎮ")):
            kwargs.update(
                {
                    bstackl_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎯ"): bstack1l11ll1ll11_opy_,
                    bstackl_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᎰ"): True,
                    bstackl_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᎱ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstackl_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎲ"): bstack1l11ll1ll11_opy_,
                    bstackl_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᎳ"): True,
                    bstackl_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᎴ"): None,
                }
            )