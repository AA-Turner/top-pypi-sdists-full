# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll1l11l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
class bstack1lll1111lll_opy_(bstack1llll11l11l_opy_):
    bstack1l11llll11l_opy_ = bstack11l1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥ፟")
    bstack1l11llll1ll_opy_ = bstack11l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧ፠")
    bstack1l11ll11l11_opy_ = bstack11l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧ፡")
    def __init__(self, bstack1lll1ll1lll_opy_):
        super().__init__()
        bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll11ll_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l11lll11ll_opy_)
        bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll111l_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1ll11111ll1_opy_)
        bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll111l_opy_, bstack1llll1lll11_opy_.POST), self.bstack1l11lll1l11_opy_)
        bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll111l_opy_, bstack1llll1lll11_opy_.POST), self.bstack1l11ll1l111_opy_)
        bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.QUIT, bstack1llll1lll11_opy_.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll11ll_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣ።"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ፣")), str):
                    url = kwargs.get(bstack11l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፤"))
                elif hasattr(kwargs.get(bstack11l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ፥")), bstack11l1_opy_ (u"ࠪࡣࡨࡲࡩࡦࡰࡷࡣࡨࡵ࡮ࡧ࡫ࡪࠫ፦")):
                    url = kwargs.get(bstack11l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፧"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ፨"))._url
            except Exception as e:
                url = bstack11l1_opy_ (u"࠭ࠧ፩")
                self.logger.error(bstack11l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡳ࡮ࠣࡪࡷࡵ࡭ࠡࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࢁࠧ፪").format(e))
            self.logger.info(bstack11l1_opy_ (u"ࠣࡔࡨࡱࡴࡺࡥࠡࡕࡨࡶࡻ࡫ࡲࠡࡃࡧࡨࡷ࡫ࡳࡴࠢࡥࡩ࡮ࡴࡧࠡࡲࡤࡷࡸ࡫ࡤࠡࡣࡶࠤ࠿ࠦࡻࡾࠤ፫").format(str(url)))
            self.bstack1l11ll1l11l_opy_(instance, url, f, kwargs)
            self.logger.info(bstack11l1_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࡀࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁ࡫ࡸࡣࡵ࡫ࡸࢃࠢ፬").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11111ll1_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lllllllll1_opy_(instance, bstack1lll1111lll_opy_.bstack1l11llll11l_opy_, False):
            return
        if not f.bstack1llll1llll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_):
            return
        platform_index = f.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_)
        if f.bstack1ll111l1111_opy_(method_name, *args) and len(args) > 1:
            bstack11ll111l1l_opy_ = datetime.now()
            hub_url = bstack1llll1l11l1_opy_.hub_url(driver)
            self.logger.warning(bstack11l1_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧ፭") + str(hub_url) + bstack11l1_opy_ (u"ࠦࠧ፮"))
            bstack1l11lll1111_opy_ = args[1][bstack11l1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ፯")] if isinstance(args[1], dict) and bstack11l1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ፰") in args[1] else None
            bstack1l11lll1lll_opy_ = bstack11l1_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧ፱")
            if isinstance(bstack1l11lll1111_opy_, dict):
                bstack11ll111l1l_opy_ = datetime.now()
                r = self.bstack1l11llll111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll11lll11_opy_(bstack11l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨ፲"), datetime.now() - bstack11ll111l1l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l1_opy_ (u"ࠤࡶࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨ࠼ࠣࠦ፳") + str(r) + bstack11l1_opy_ (u"ࠥࠦ፴"))
                        return
                    if r.hub_url:
                        f.bstack1l11lll1ll1_opy_(instance, driver, r.hub_url)
                        f.bstack1111111lll_opy_(instance, bstack1lll1111lll_opy_.bstack1l11llll11l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ፵"), e)
    def bstack1l11lll1l11_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llll1l11l1_opy_.session_id(driver)
            if session_id:
                bstack1l11ll1ll11_opy_ = bstack11l1_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢ፶").format(session_id)
                bstack1ll1ll11111_opy_.mark(bstack1l11ll1ll11_opy_)
    def bstack1l11ll1l111_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllllllll1_opy_(instance, bstack1lll1111lll_opy_.bstack1l11llll1ll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llll1l11l1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡪࡸࡦࡤࡻࡲ࡭࠿ࠥ፷") + str(hub_url) + bstack11l1_opy_ (u"ࠢࠣ፸"))
            return
        framework_session_id = bstack1llll1l11l1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦ፹") + str(framework_session_id) + bstack11l1_opy_ (u"ࠤࠥ፺"))
            return
        if bstack1llll1l11l1_opy_.bstack1l11lllll11_opy_(*args) == bstack1llll1l11l1_opy_.bstack1l11ll1llll_opy_:
            bstack1l11lllll1l_opy_ = bstack11l1_opy_ (u"ࠥࡿࢂࡀࡥ࡯ࡦࠥ፻").format(framework_session_id)
            bstack1l11ll1ll11_opy_ = bstack11l1_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨ፼").format(framework_session_id)
            bstack1ll1ll11111_opy_.end(
                label=bstack11l1_opy_ (u"ࠧࡹࡤ࡬࠼ࡧࡶ࡮ࡼࡥࡳ࠼ࡳࡳࡸࡺ࠭ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠣ፽"),
                start=bstack1l11ll1ll11_opy_,
                end=bstack1l11lllll1l_opy_,
                status=True,
                failure=None
            )
            bstack11ll111l1l_opy_ = datetime.now()
            r = self.bstack1l11lll11l1_opy_(
                ref,
                f.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll11lll11_opy_(bstack11l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧ፾"), datetime.now() - bstack11ll111l1l_opy_)
            f.bstack1111111lll_opy_(instance, bstack1lll1111lll_opy_.bstack1l11llll1ll_opy_, r.success)
    def bstack1l11lll111l_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllllllll1_opy_(instance, bstack1lll1111lll_opy_.bstack1l11ll11l11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llll1l11l1_opy_.session_id(driver)
        hub_url = bstack1llll1l11l1_opy_.hub_url(driver)
        bstack11ll111l1l_opy_ = datetime.now()
        r = self.bstack1l11ll1l1l1_opy_(
            ref,
            f.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll11lll11_opy_(bstack11l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧ፿"), datetime.now() - bstack11ll111l1l_opy_)
        f.bstack1111111lll_opy_(instance, bstack1lll1111lll_opy_.bstack1l11ll11l11_opy_, r.success)
    @measure(event_name=EVENTS.bstack1ll11l1ll1_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def bstack1l1l11l11ll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11l1_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᎀ") + str(req) + bstack11l1_opy_ (u"ࠤࠥᎁ"))
        try:
            r = self.bstack1ll1llllll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨᎂ") + str(r.success) + bstack11l1_opy_ (u"ࠦࠧᎃ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᎄ") + str(e) + bstack11l1_opy_ (u"ࠨࠢᎅ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1lll1_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def bstack1l11llll111_opy_(
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
        self.logger.debug(bstack11l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᎆ") + str(req) + bstack11l1_opy_ (u"ࠣࠤᎇ"))
        try:
            r = self.bstack1ll1llllll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᎈ") + str(r.success) + bstack11l1_opy_ (u"ࠥࠦᎉ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᎊ") + str(e) + bstack11l1_opy_ (u"ࠧࠨᎋ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll1l1l_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def bstack1l11lll11l1_opy_(
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
        self.logger.debug(bstack11l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤᎌ") + str(req) + bstack11l1_opy_ (u"ࠢࠣᎍ"))
        try:
            r = self.bstack1ll1llllll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᎎ") + str(r) + bstack11l1_opy_ (u"ࠤࠥᎏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ᎐") + str(e) + bstack11l1_opy_ (u"ࠦࠧ᎑"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1ll1l_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def bstack1l11ll1l1l1_opy_(
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
        self.logger.debug(bstack11l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴ࠿ࠦࠢ᎒") + str(req) + bstack11l1_opy_ (u"ࠨࠢ᎓"))
        try:
            r = self.bstack1ll1llllll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤ᎔") + str(r) + bstack11l1_opy_ (u"ࠣࠤ᎕"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ᎖") + str(e) + bstack11l1_opy_ (u"ࠥࠦ᎗"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll1llll_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def bstack1l11ll1l11l_opy_(self, instance: bstack1lllll1ll1l_opy_, url: str, f: bstack1llll1l11l1_opy_, kwargs):
        bstack1l11ll11ll1_opy_ = version.parse(f.framework_version)
        bstack1l11ll111l1_opy_ = kwargs.get(bstack11l1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧ᎘"))
        bstack1l11ll11lll_opy_ = kwargs.get(bstack11l1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᎙"))
        bstack1l1l11ll1l1_opy_ = {}
        bstack1l11llll1l1_opy_ = {}
        bstack1l11ll1l1ll_opy_ = None
        bstack1l11ll11l1l_opy_ = {}
        if bstack1l11ll11lll_opy_ is not None or bstack1l11ll111l1_opy_ is not None: # check top level caps
            if bstack1l11ll11lll_opy_ is not None:
                bstack1l11ll11l1l_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᎚")] = bstack1l11ll11lll_opy_
            if bstack1l11ll111l1_opy_ is not None and callable(getattr(bstack1l11ll111l1_opy_, bstack11l1_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ᎛"))):
                bstack1l11ll11l1l_opy_[bstack11l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᎜")] = bstack1l11ll111l1_opy_.to_capabilities()
        response = self.bstack1l1l11l11ll_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll11l1l_opy_).encode(bstack11l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᎝")))
        if response is not None and response.capabilities:
            bstack1l1l11ll1l1_opy_ = json.loads(response.capabilities.decode(bstack11l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᎞")))
            if not bstack1l1l11ll1l1_opy_: # empty caps bstack1l1l11l1l1l_opy_ bstack1l1l11l1111_opy_ bstack1l1l11ll1ll_opy_ bstack1lll111l111_opy_ or error in processing
                return
            bstack1l11ll1l1ll_opy_ = f.bstack1lll1l1ll1l_opy_[bstack11l1_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣ᎟")](bstack1l1l11ll1l1_opy_)
        if bstack1l11ll111l1_opy_ is not None and bstack1l11ll11ll1_opy_ >= version.parse(bstack11l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᎠ")):
            bstack1l11llll1l1_opy_ = None
        if (
                not bstack1l11ll111l1_opy_ and not bstack1l11ll11lll_opy_
        ) or (
                bstack1l11ll11ll1_opy_ < version.parse(bstack11l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᎡ"))
        ):
            bstack1l11llll1l1_opy_ = {}
            bstack1l11llll1l1_opy_.update(bstack1l1l11ll1l1_opy_)
        self.logger.info(bstack11lll11lll_opy_)
        if os.environ.get(bstack11l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠥᎢ")).lower().__eq__(bstack11l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᎣ")):
            kwargs.update(
                {
                    bstack11l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᎤ"): f.bstack1l11ll111ll_opy_,
                }
            )
        if bstack1l11ll11ll1_opy_ >= version.parse(bstack11l1_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᎥ")):
            if bstack1l11ll11lll_opy_ is not None:
                del kwargs[bstack11l1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᎦ")]
            kwargs.update(
                {
                    bstack11l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᎧ"): bstack1l11ll1l1ll_opy_,
                    bstack11l1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᎨ"): True,
                    bstack11l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᎩ"): None,
                }
            )
        elif bstack1l11ll11ll1_opy_ >= version.parse(bstack11l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᎪ")):
            kwargs.update(
                {
                    bstack11l1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎫ"): bstack1l11llll1l1_opy_,
                    bstack11l1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᎬ"): bstack1l11ll1l1ll_opy_,
                    bstack11l1_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᎭ"): True,
                    bstack11l1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᎮ"): None,
                }
            )
        elif bstack1l11ll11ll1_opy_ >= version.parse(bstack11l1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭Ꭿ")):
            kwargs.update(
                {
                    bstack11l1_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᎰ"): bstack1l11llll1l1_opy_,
                    bstack11l1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᎱ"): True,
                    bstack11l1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᎲ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l1_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᎳ"): bstack1l11llll1l1_opy_,
                    bstack11l1_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᎴ"): True,
                    bstack11l1_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᎵ"): None,
                }
            )