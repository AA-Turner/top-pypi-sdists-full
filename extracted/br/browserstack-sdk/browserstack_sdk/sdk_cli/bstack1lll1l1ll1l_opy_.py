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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1lllllll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll1lll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
class bstack1ll1l1lll11_opy_(bstack1ll1l1llll1_opy_):
    bstack1l11lll1111_opy_ = bstack1l11ll1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧ፨")
    bstack1l11ll11111_opy_ = bstack1l11ll1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢ፩")
    bstack1l11ll1lll1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢ፪")
    def __init__(self, bstack1ll1l1lll1l_opy_):
        super().__init__()
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1llll1lll1l_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l11ll1ll11_opy_)
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1llllllll_opy_)
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.POST), self.bstack1l11l1llll1_opy_)
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.POST), self.bstack1l11ll11l1l_opy_)
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.QUIT, bstack1llll1l11ll_opy_.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1ll11_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l11ll1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥ፫"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l11ll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ፬")), str):
                    url = kwargs.get(bstack1l11ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ፭"))
                elif hasattr(kwargs.get(bstack1l11ll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፮")), bstack1l11ll1_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭፯")):
                    url = kwargs.get(bstack1l11ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ፰"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l11ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ፱"))._url
            except Exception as e:
                url = bstack1l11ll1_opy_ (u"ࠨࠩ፲")
                self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢ፳").format(e))
            self.logger.info(bstack1l11ll1_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦ፴").format(str(url)))
            self.bstack1l11ll1l111_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l11ll1_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤ፵").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1llllllll_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llllllllll_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11lll1111_opy_, False):
            return
        if not f.bstack1lllll11l11_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_):
            return
        platform_index = f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_)
        if f.bstack1ll11l1lll1_opy_(method_name, *args) and len(args) > 1:
            bstack1l11ll1ll_opy_ = datetime.now()
            hub_url = bstack1ll1l1l1lll_opy_.hub_url(driver)
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢ፶") + str(hub_url) + bstack1l11ll1_opy_ (u"ࠨࠢ፷"))
            bstack1l11ll1ll1l_opy_ = args[1][bstack1l11ll1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ፸")] if isinstance(args[1], dict) and bstack1l11ll1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ፹") in args[1] else None
            bstack1l11l1lll1l_opy_ = bstack1l11ll1_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢ፺")
            if isinstance(bstack1l11ll1ll1l_opy_, dict):
                bstack1l11ll1ll_opy_ = datetime.now()
                r = self.bstack1l11lll1l11_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣ፻"), datetime.now() - bstack1l11ll1ll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l11ll1_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨ፼") + str(r) + bstack1l11ll1_opy_ (u"ࠧࠨ፽"))
                        return
                    if r.hub_url:
                        f.bstack1l11ll1l1ll_opy_(instance, driver, r.hub_url)
                        f.bstack1llllll1ll1_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11lll1111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ፾"), e)
    def bstack1l11l1llll1_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1l1l1lll_opy_.session_id(driver)
            if session_id:
                bstack1l11l1lllll_opy_ = bstack1l11ll1_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤ፿").format(session_id)
                bstack1lll11111l1_opy_.mark(bstack1l11l1lllll_opy_)
    def bstack1l11ll11l1l_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllllllll_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11ll11111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1l1l1lll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᎀ") + str(hub_url) + bstack1l11ll1_opy_ (u"ࠤࠥᎁ"))
            return
        framework_session_id = bstack1ll1l1l1lll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᎂ") + str(framework_session_id) + bstack1l11ll1_opy_ (u"ࠦࠧᎃ"))
            return
        if bstack1ll1l1l1lll_opy_.bstack1l11ll1l11l_opy_(*args) == bstack1ll1l1l1lll_opy_.bstack1l11ll111ll_opy_:
            bstack1l11l1lll11_opy_ = bstack1l11ll1_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᎄ").format(framework_session_id)
            bstack1l11l1lllll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᎅ").format(framework_session_id)
            bstack1lll11111l1_opy_.end(
                label=bstack1l11ll1_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᎆ"),
                start=bstack1l11l1lllll_opy_,
                end=bstack1l11l1lll11_opy_,
                status=True,
                failure=None
            )
            bstack1l11ll1ll_opy_ = datetime.now()
            r = self.bstack1l11lll11ll_opy_(
                ref,
                f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᎇ"), datetime.now() - bstack1l11ll1ll_opy_)
            f.bstack1llllll1ll1_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11ll11111_opy_, r.success)
    def bstack1l11lll111l_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllllllll_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11ll1lll1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1l1l1lll_opy_.session_id(driver)
        hub_url = bstack1ll1l1l1lll_opy_.hub_url(driver)
        bstack1l11ll1ll_opy_ = datetime.now()
        r = self.bstack1l11ll1llll_opy_(
            ref,
            f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᎈ"), datetime.now() - bstack1l11ll1ll_opy_)
        f.bstack1llllll1ll1_opy_(instance, bstack1ll1l1lll11_opy_.bstack1l11ll1lll1_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1111l1l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l1l11l1l11_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᎉ") + str(req) + bstack1l11ll1_opy_ (u"ࠦࠧᎊ"))
        try:
            r = self.bstack1lll111111l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᎋ") + str(r.success) + bstack1l11ll1_opy_ (u"ࠨࠢᎌ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᎍ") + str(e) + bstack1l11ll1_opy_ (u"ࠣࠤᎎ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll11l11_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l11lll1l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᎏ") + str(req) + bstack1l11ll1_opy_ (u"ࠥࠦ᎐"))
        try:
            r = self.bstack1lll111111l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢ᎑") + str(r.success) + bstack1l11ll1_opy_ (u"ࠧࠨ᎒"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦ᎓") + str(e) + bstack1l11ll1_opy_ (u"ࠢࠣ᎔"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1ll1ll_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l11lll11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦ᎕") + str(req) + bstack1l11ll1_opy_ (u"ࠤࠥ᎖"))
        try:
            r = self.bstack1lll111111l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧ᎗") + str(r) + bstack1l11ll1_opy_ (u"ࠦࠧ᎘"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ᎙") + str(e) + bstack1l11ll1_opy_ (u"ࠨࠢ᎚"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1111l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l11ll1llll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤ᎛") + str(req) + bstack1l11ll1_opy_ (u"ࠣࠤ᎜"))
        try:
            r = self.bstack1lll111111l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦ᎝") + str(r) + bstack1l11ll1_opy_ (u"ࠥࠦ᎞"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤ᎟") + str(e) + bstack1l11ll1_opy_ (u"ࠧࠨᎠ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1111111l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l11ll1l111_opy_(self, instance: bstack1lllllll111_opy_, url: str, f: bstack1ll1l1l1lll_opy_, kwargs):
        bstack1l11lll1l1l_opy_ = version.parse(f.framework_version)
        bstack1l11l1ll1l1_opy_ = kwargs.get(bstack1l11ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᎡ"))
        bstack1l11ll11lll_opy_ = kwargs.get(bstack1l11ll1_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᎢ"))
        bstack1l1l111l11l_opy_ = {}
        bstack1l11ll111l1_opy_ = {}
        bstack1l11ll11ll1_opy_ = None
        bstack1l11ll1l1l1_opy_ = {}
        if bstack1l11ll11lll_opy_ is not None or bstack1l11l1ll1l1_opy_ is not None: # check top level caps
            if bstack1l11ll11lll_opy_ is not None:
                bstack1l11ll1l1l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᎣ")] = bstack1l11ll11lll_opy_
            if bstack1l11l1ll1l1_opy_ is not None and callable(getattr(bstack1l11l1ll1l1_opy_, bstack1l11ll1_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᎤ"))):
                bstack1l11ll1l1l1_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭Ꭵ")] = bstack1l11l1ll1l1_opy_.to_capabilities()
        response = self.bstack1l1l11l1l11_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll1l1l1_opy_).encode(bstack1l11ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᎦ")))
        if response is not None and response.capabilities:
            bstack1l1l111l11l_opy_ = json.loads(response.capabilities.decode(bstack1l11ll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᎧ")))
            if not bstack1l1l111l11l_opy_: # empty caps bstack1l1l111ll11_opy_ bstack1l1l111l1l1_opy_ bstack1l1l11ll11l_opy_ bstack1lll1ll1lll_opy_ or error in processing
                return
            bstack1l11ll11ll1_opy_ = f.bstack1lll1111l1l_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᎨ")](bstack1l1l111l11l_opy_)
        if bstack1l11l1ll1l1_opy_ is not None and bstack1l11lll1l1l_opy_ >= version.parse(bstack1l11ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭Ꭹ")):
            bstack1l11ll111l1_opy_ = None
        if (
                not bstack1l11l1ll1l1_opy_ and not bstack1l11ll11lll_opy_
        ) or (
                bstack1l11lll1l1l_opy_ < version.parse(bstack1l11ll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᎪ"))
        ):
            bstack1l11ll111l1_opy_ = {}
            bstack1l11ll111l1_opy_.update(bstack1l1l111l11l_opy_)
        self.logger.info(bstack11lll1lll1_opy_)
        if os.environ.get(bstack1l11ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᎫ")).lower().__eq__(bstack1l11ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣᎬ")):
            kwargs.update(
                {
                    bstack1l11ll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᎭ"): f.bstack1l11lll11l1_opy_,
                }
            )
        if bstack1l11lll1l1l_opy_ >= version.parse(bstack1l11ll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᎮ")):
            if bstack1l11ll11lll_opy_ is not None:
                del kwargs[bstack1l11ll1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎯ")]
            kwargs.update(
                {
                    bstack1l11ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᎰ"): bstack1l11ll11ll1_opy_,
                    bstack1l11ll1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᎱ"): True,
                    bstack1l11ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᎲ"): None,
                }
            )
        elif bstack1l11lll1l1l_opy_ >= version.parse(bstack1l11ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᎳ")):
            kwargs.update(
                {
                    bstack1l11ll1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᎴ"): bstack1l11ll111l1_opy_,
                    bstack1l11ll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᎵ"): bstack1l11ll11ll1_opy_,
                    bstack1l11ll1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᎶ"): True,
                    bstack1l11ll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᎷ"): None,
                }
            )
        elif bstack1l11lll1l1l_opy_ >= version.parse(bstack1l11ll1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᎸ")):
            kwargs.update(
                {
                    bstack1l11ll1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎹ"): bstack1l11ll111l1_opy_,
                    bstack1l11ll1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᎺ"): True,
                    bstack1l11ll1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᎻ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l11ll1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᎼ"): bstack1l11ll111l1_opy_,
                    bstack1l11ll1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᎽ"): True,
                    bstack1l11ll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᎾ"): None,
                }
            )