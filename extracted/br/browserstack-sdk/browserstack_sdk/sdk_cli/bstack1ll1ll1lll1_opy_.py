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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11ll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
class bstack1lll1l1lll1_opy_(bstack1llll1l1l11_opy_):
    bstack1l11lll1lll_opy_ = bstack111l111_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣ፝")
    bstack1l11l1lllll_opy_ = bstack111l111_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥ፞")
    bstack1l11lll11l1_opy_ = bstack111l111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥ፟")
    def __init__(self, bstack1ll1l1lll1l_opy_):
        super().__init__()
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l11lll1l1l_opy_)
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll11111l1l_opy_)
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.POST), self.bstack1l11ll11lll_opy_)
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.POST), self.bstack1l11ll111ll_opy_)
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.QUIT, bstack1llllll1111_opy_.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll1l1l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111l111_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨ፠"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack111l111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ፡")), str):
                    url = kwargs.get(bstack111l111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ።"))
                elif hasattr(kwargs.get(bstack111l111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ፣")), bstack111l111_opy_ (u"ࠨࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠩ፤")):
                    url = kwargs.get(bstack111l111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ፥"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack111l111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ፦"))._url
            except Exception as e:
                url = bstack111l111_opy_ (u"ࠫࠬ፧")
                self.logger.error(bstack111l111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡸ࡬ࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࡼࡿࠥ፨").format(e))
            self.logger.info(bstack111l111_opy_ (u"ࠨࡒࡦ࡯ࡲࡸࡪࠦࡓࡦࡴࡹࡩࡷࠦࡁࡥࡦࡵࡩࡸࡹࠠࡣࡧ࡬ࡲ࡬ࠦࡰࡢࡵࡶࡩࡩࠦࡡࡴࠢ࠽ࠤࢀࢃࠢ፩").format(str(url)))
            self.bstack1l11lll1ll1_opy_(instance, url, f, kwargs)
            self.logger.info(bstack111l111_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧ፪").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11111l1l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1111111l1l_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11lll1lll_opy_, False):
            return
        if not f.bstack1lllll1l111_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_):
            return
        platform_index = f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_)
        if f.bstack1ll1l11l11l_opy_(method_name, *args) and len(args) > 1:
            bstack1l1111lll_opy_ = datetime.now()
            hub_url = bstack1lll1l11l11_opy_.hub_url(driver)
            self.logger.warning(bstack111l111_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥ፫") + str(hub_url) + bstack111l111_opy_ (u"ࠤࠥ፬"))
            bstack1l11ll1l11l_opy_ = args[1][bstack111l111_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ፭")] if isinstance(args[1], dict) and bstack111l111_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ፮") in args[1] else None
            bstack1l11ll1llll_opy_ = bstack111l111_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥ፯")
            if isinstance(bstack1l11ll1l11l_opy_, dict):
                bstack1l1111lll_opy_ = datetime.now()
                r = self.bstack1l11ll111l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦ፰"), datetime.now() - bstack1l1111lll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack111l111_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤ፱") + str(r) + bstack111l111_opy_ (u"ࠣࠤ፲"))
                        return
                    if r.hub_url:
                        f.bstack1l11ll1l111_opy_(instance, driver, r.hub_url)
                        f.bstack1111111111_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11lll1lll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack111l111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ፳"), e)
    def bstack1l11ll11lll_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1l11l11_opy_.session_id(driver)
            if session_id:
                bstack1l11lll1l11_opy_ = bstack111l111_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧ፴").format(session_id)
                bstack1llll1111l1_opy_.mark(bstack1l11lll1l11_opy_)
    def bstack1l11ll111ll_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1111111l1l_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11l1lllll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1l11l11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack111l111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣ፵") + str(hub_url) + bstack111l111_opy_ (u"ࠧࠨ፶"))
            return
        framework_session_id = bstack1lll1l11l11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤ፷") + str(framework_session_id) + bstack111l111_opy_ (u"ࠢࠣ፸"))
            return
        if bstack1lll1l11l11_opy_.bstack1l11llll11l_opy_(*args) == bstack1lll1l11l11_opy_.bstack1l11llll1l1_opy_:
            bstack1l11ll1ll1l_opy_ = bstack111l111_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣ፹").format(framework_session_id)
            bstack1l11lll1l11_opy_ = bstack111l111_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦ፺").format(framework_session_id)
            bstack1llll1111l1_opy_.end(
                label=bstack111l111_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨ፻"),
                start=bstack1l11lll1l11_opy_,
                end=bstack1l11ll1ll1l_opy_,
                status=True,
                failure=None
            )
            bstack1l1111lll_opy_ = datetime.now()
            r = self.bstack1l11llll111_opy_(
                ref,
                f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥ፼"), datetime.now() - bstack1l1111lll_opy_)
            f.bstack1111111111_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11l1lllll_opy_, r.success)
    def bstack1l11lll111l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1111111l1l_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11lll11l1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1l11l11_opy_.session_id(driver)
        hub_url = bstack1lll1l11l11_opy_.hub_url(driver)
        bstack1l1111lll_opy_ = datetime.now()
        r = self.bstack1l11lll1111_opy_(
            ref,
            f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥ፽"), datetime.now() - bstack1l1111lll_opy_)
        f.bstack1111111111_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11lll11l1_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lllll11l_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l1l11ll1l1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack111l111_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦ፾") + str(req) + bstack111l111_opy_ (u"ࠢࠣ፿"))
        try:
            r = self.bstack1lll1l11l1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᎀ") + str(r.success) + bstack111l111_opy_ (u"ࠤࠥᎁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᎂ") + str(e) + bstack111l111_opy_ (u"ࠦࠧᎃ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1111l_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l11ll111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack111l111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᎄ") + str(req) + bstack111l111_opy_ (u"ࠨࠢᎅ"))
        try:
            r = self.bstack1lll1l11l1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᎆ") + str(r.success) + bstack111l111_opy_ (u"ࠣࠤᎇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎈ") + str(e) + bstack111l111_opy_ (u"ࠥࠦᎉ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll11ll1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l11llll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack111l111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢᎊ") + str(req) + bstack111l111_opy_ (u"ࠧࠨᎋ"))
        try:
            r = self.bstack1lll1l11l1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᎌ") + str(r) + bstack111l111_opy_ (u"ࠢࠣᎍ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᎎ") + str(e) + bstack111l111_opy_ (u"ࠤࠥᎏ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll11ll_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l11lll1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack111l111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧ᎐") + str(req) + bstack111l111_opy_ (u"ࠦࠧ᎑"))
        try:
            r = self.bstack1lll1l11l1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢ᎒") + str(r) + bstack111l111_opy_ (u"ࠨࠢ᎓"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ᎔") + str(e) + bstack111l111_opy_ (u"ࠣࠤ᎕"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l111l1l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l11lll1ll1_opy_(self, instance: bstack1lllll1ll1l_opy_, url: str, f: bstack1lll1l11l11_opy_, kwargs):
        bstack1l11ll1l1ll_opy_ = version.parse(f.framework_version)
        bstack1l11ll11111_opy_ = kwargs.get(bstack111l111_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥ᎖"))
        bstack1l11ll1l1l1_opy_ = kwargs.get(bstack111l111_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᎗"))
        bstack1l1l11ll11l_opy_ = {}
        bstack1l11ll11l11_opy_ = {}
        bstack1l11ll1lll1_opy_ = None
        bstack1l11ll11l1l_opy_ = {}
        if bstack1l11ll1l1l1_opy_ is not None or bstack1l11ll11111_opy_ is not None: # check top level caps
            if bstack1l11ll1l1l1_opy_ is not None:
                bstack1l11ll11l1l_opy_[bstack111l111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᎘")] = bstack1l11ll1l1l1_opy_
            if bstack1l11ll11111_opy_ is not None and callable(getattr(bstack1l11ll11111_opy_, bstack111l111_opy_ (u"ࠧࡺ࡯ࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᎙"))):
                bstack1l11ll11l1l_opy_[bstack111l111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡢࡵࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᎚")] = bstack1l11ll11111_opy_.to_capabilities()
        response = self.bstack1l1l11ll1l1_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll11l1l_opy_).encode(bstack111l111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᎛")))
        if response is not None and response.capabilities:
            bstack1l1l11ll11l_opy_ = json.loads(response.capabilities.decode(bstack111l111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᎜")))
            if not bstack1l1l11ll11l_opy_: # empty caps bstack1l1l11l1l1l_opy_ bstack1l1l11l1lll_opy_ bstack1l1l11l11ll_opy_ bstack1ll1l1ll1l1_opy_ or error in processing
                return
            bstack1l11ll1lll1_opy_ = f.bstack1ll1ll1l1l1_opy_[bstack111l111_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨ᎝")](bstack1l1l11ll11l_opy_)
        if bstack1l11ll11111_opy_ is not None and bstack1l11ll1l1ll_opy_ >= version.parse(bstack111l111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ᎞")):
            bstack1l11ll11l11_opy_ = None
        if (
                not bstack1l11ll11111_opy_ and not bstack1l11ll1l1l1_opy_
        ) or (
                bstack1l11ll1l1ll_opy_ < version.parse(bstack111l111_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ᎟"))
        ):
            bstack1l11ll11l11_opy_ = {}
            bstack1l11ll11l11_opy_.update(bstack1l1l11ll11l_opy_)
        self.logger.info(bstack1l11ll1l1l_opy_)
        if os.environ.get(bstack111l111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᎠ")).lower().__eq__(bstack111l111_opy_ (u"ࠨࡴࡳࡷࡨࠦᎡ")):
            kwargs.update(
                {
                    bstack111l111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᎢ"): f.bstack1l11ll1ll11_opy_,
                }
            )
        if bstack1l11ll1l1ll_opy_ >= version.parse(bstack111l111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᎣ")):
            if bstack1l11ll1l1l1_opy_ is not None:
                del kwargs[bstack111l111_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎤ")]
            kwargs.update(
                {
                    bstack111l111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᎥ"): bstack1l11ll1lll1_opy_,
                    bstack111l111_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᎦ"): True,
                    bstack111l111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᎧ"): None,
                }
            )
        elif bstack1l11ll1l1ll_opy_ >= version.parse(bstack111l111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᎨ")):
            kwargs.update(
                {
                    bstack111l111_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᎩ"): bstack1l11ll11l11_opy_,
                    bstack111l111_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᎪ"): bstack1l11ll1lll1_opy_,
                    bstack111l111_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᎫ"): True,
                    bstack111l111_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᎬ"): None,
                }
            )
        elif bstack1l11ll1l1ll_opy_ >= version.parse(bstack111l111_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᎭ")):
            kwargs.update(
                {
                    bstack111l111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᎮ"): bstack1l11ll11l11_opy_,
                    bstack111l111_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᎯ"): True,
                    bstack111l111_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᎰ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack111l111_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎱ"): bstack1l11ll11l11_opy_,
                    bstack111l111_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᎲ"): True,
                    bstack111l111_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᎳ"): None,
                }
            )