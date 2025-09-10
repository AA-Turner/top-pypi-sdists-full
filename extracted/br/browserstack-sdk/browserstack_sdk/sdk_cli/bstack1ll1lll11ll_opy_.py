# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
class bstack1ll1lll1l11_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l11ll1lll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨ፩")
    bstack1l11ll11l11_opy_ = bstack1ll11ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣ፪")
    bstack1l11l1lllll_opy_ = bstack1ll11ll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣ፫")
    def __init__(self, bstack1ll1ll1l11l_opy_):
        super().__init__()
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l11l1lll1l_opy_)
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1llllllll_opy_)
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.POST), self.bstack1l11ll1l1ll_opy_)
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.POST), self.bstack1l11lll11ll_opy_)
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.QUIT, bstack1lllll111ll_opy_.POST), self.bstack1l11ll1ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1lll1l_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11ll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦ፬"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1ll11ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ፭")), str):
                    url = kwargs.get(bstack1ll11ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፮"))
                elif hasattr(kwargs.get(bstack1ll11ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ፯")), bstack1ll11ll_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧ፰")):
                    url = kwargs.get(bstack1ll11ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ፱"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1ll11ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፲"))._url
            except Exception as e:
                url = bstack1ll11ll_opy_ (u"ࠩࠪ፳")
                self.logger.error(bstack1ll11ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡶࡱࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࢁࡽࠣ፴").format(e))
            self.logger.info(bstack1ll11ll_opy_ (u"ࠦࡗ࡫࡭ࡰࡶࡨࠤࡘ࡫ࡲࡷࡧࡵࠤࡆࡪࡤࡳࡧࡶࡷࠥࡨࡥࡪࡰࡪࠤࡵࡧࡳࡴࡧࡧࠤࡦࡹࠠ࠻ࠢࡾࢁࠧ፵").format(str(url)))
            self.bstack1l11ll11ll1_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾ࠼ࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽ࡮ࡻࡦࡸࡧࡴࡿࠥ፶").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1llllllll_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llll1lllll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l11ll1lll1_opy_, False):
            return
        if not f.bstack1llllll1lll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_):
            return
        platform_index = f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_)
        if f.bstack1ll111lll11_opy_(method_name, *args) and len(args) > 1:
            bstack1ll111l11_opy_ = datetime.now()
            hub_url = bstack1ll1l1ll111_opy_.hub_url(driver)
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲ࠽ࠣ፷") + str(hub_url) + bstack1ll11ll_opy_ (u"ࠢࠣ፸"))
            bstack1l11ll11l1l_opy_ = args[1][bstack1ll11ll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ፹")] if isinstance(args[1], dict) and bstack1ll11ll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ፺") in args[1] else None
            bstack1l11l1lll11_opy_ = bstack1ll11ll_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣ፻")
            if isinstance(bstack1l11ll11l1l_opy_, dict):
                bstack1ll111l11_opy_ = datetime.now()
                r = self.bstack1l11ll1111l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤ፼"), datetime.now() - bstack1ll111l11_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡹ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫࠿ࠦࠢ፽") + str(r) + bstack1ll11ll_opy_ (u"ࠨࠢ፾"))
                        return
                    if r.hub_url:
                        f.bstack1l11l1llll1_opy_(instance, driver, r.hub_url)
                        f.bstack1llll1l1lll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l11ll1lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll11ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ፿"), e)
    def bstack1l11ll1l1ll_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1l1ll111_opy_.session_id(driver)
            if session_id:
                bstack1l11lll1111_opy_ = bstack1ll11ll_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᎀ").format(session_id)
                bstack1ll1ll11ll1_opy_.mark(bstack1l11lll1111_opy_)
    def bstack1l11lll11ll_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll1lllll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l11ll11l11_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1l1ll111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᎁ") + str(hub_url) + bstack1ll11ll_opy_ (u"ࠥࠦᎂ"))
            return
        framework_session_id = bstack1ll1l1ll111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᎃ") + str(framework_session_id) + bstack1ll11ll_opy_ (u"ࠧࠨᎄ"))
            return
        if bstack1ll1l1ll111_opy_.bstack1l11ll111ll_opy_(*args) == bstack1ll1l1ll111_opy_.bstack1l11lll1l11_opy_:
            bstack1l11lll11l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡻࡾ࠼ࡨࡲࡩࠨᎅ").format(framework_session_id)
            bstack1l11lll1111_opy_ = bstack1ll11ll_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᎆ").format(framework_session_id)
            bstack1ll1ll11ll1_opy_.end(
                label=bstack1ll11ll_opy_ (u"ࠣࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠦᎇ"),
                start=bstack1l11lll1111_opy_,
                end=bstack1l11lll11l1_opy_,
                status=True,
                failure=None
            )
            bstack1ll111l11_opy_ = datetime.now()
            r = self.bstack1l11lll1l1l_opy_(
                ref,
                f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᎈ"), datetime.now() - bstack1ll111l11_opy_)
            f.bstack1llll1l1lll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l11ll11l11_opy_, r.success)
    def bstack1l11ll1ll11_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll1lllll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l11l1lllll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1l1ll111_opy_.session_id(driver)
        hub_url = bstack1ll1l1ll111_opy_.hub_url(driver)
        bstack1ll111l11_opy_ = datetime.now()
        r = self.bstack1l11ll11111_opy_(
            ref,
            f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᎉ"), datetime.now() - bstack1ll111l11_opy_)
        f.bstack1llll1l1lll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1l11l1lllll_opy_, r.success)
    @measure(event_name=EVENTS.bstack11ll1ll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l1l11l1111_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᎊ") + str(req) + bstack1ll11ll_opy_ (u"ࠧࠨᎋ"))
        try:
            r = self.bstack1ll1llllll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᎌ") + str(r.success) + bstack1ll11ll_opy_ (u"ࠢࠣᎍ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᎎ") + str(e) + bstack1ll11ll_opy_ (u"ࠤࠥᎏ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1l111_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l11ll1111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧ᎐") + str(req) + bstack1ll11ll_opy_ (u"ࠦࠧ᎑"))
        try:
            r = self.bstack1ll1llllll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣ᎒") + str(r.success) + bstack1ll11ll_opy_ (u"ࠨࠢ᎓"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ᎔") + str(e) + bstack1ll11ll_opy_ (u"ࠣࠤ᎕"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1ll1l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l11lll1l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶ࠽ࠤࠧ᎖") + str(req) + bstack1ll11ll_opy_ (u"ࠥࠦ᎗"))
        try:
            r = self.bstack1ll1llllll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨ᎘") + str(r) + bstack1ll11ll_opy_ (u"ࠧࠨ᎙"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦ᎚") + str(e) + bstack1ll11ll_opy_ (u"ࠢࠣ᎛"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll111l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l11ll11111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰ࠻ࠢࠥ᎜") + str(req) + bstack1ll11ll_opy_ (u"ࠤࠥ᎝"))
        try:
            r = self.bstack1ll1llllll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧ᎞") + str(r) + bstack1ll11ll_opy_ (u"ࠦࠧ᎟"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᎠ") + str(e) + bstack1ll11ll_opy_ (u"ࠨࠢᎡ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11ll1l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l11ll11ll1_opy_(self, instance: bstack1llll1ll111_opy_, url: str, f: bstack1ll1l1ll111_opy_, kwargs):
        bstack1l11ll11lll_opy_ = version.parse(f.framework_version)
        bstack1l11l1ll1ll_opy_ = kwargs.get(bstack1ll11ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᎢ"))
        bstack1l11ll1ll1l_opy_ = kwargs.get(bstack1ll11ll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎣ"))
        bstack1l1l11l11ll_opy_ = {}
        bstack1l11ll1llll_opy_ = {}
        bstack1l11ll1l11l_opy_ = None
        bstack1l11ll111l1_opy_ = {}
        if bstack1l11ll1ll1l_opy_ is not None or bstack1l11l1ll1ll_opy_ is not None: # check top level caps
            if bstack1l11ll1ll1l_opy_ is not None:
                bstack1l11ll111l1_opy_[bstack1ll11ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᎤ")] = bstack1l11ll1ll1l_opy_
            if bstack1l11l1ll1ll_opy_ is not None and callable(getattr(bstack1l11l1ll1ll_opy_, bstack1ll11ll_opy_ (u"ࠥࡸࡴࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᎥ"))):
                bstack1l11ll111l1_opy_[bstack1ll11ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࡤࡧࡳࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᎦ")] = bstack1l11l1ll1ll_opy_.to_capabilities()
        response = self.bstack1l1l11l1111_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll111l1_opy_).encode(bstack1ll11ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᎧ")))
        if response is not None and response.capabilities:
            bstack1l1l11l11ll_opy_ = json.loads(response.capabilities.decode(bstack1ll11ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᎨ")))
            if not bstack1l1l11l11ll_opy_: # empty caps bstack1l1l111llll_opy_ bstack1l1l11l1l11_opy_ bstack1l1l11l1l1l_opy_ bstack1ll1l1llll1_opy_ or error in processing
                return
            bstack1l11ll1l11l_opy_ = f.bstack1lll1111l1l_opy_[bstack1ll11ll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᎩ")](bstack1l1l11l11ll_opy_)
        if bstack1l11l1ll1ll_opy_ is not None and bstack1l11ll11lll_opy_ >= version.parse(bstack1ll11ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᎪ")):
            bstack1l11ll1llll_opy_ = None
        if (
                not bstack1l11l1ll1ll_opy_ and not bstack1l11ll1ll1l_opy_
        ) or (
                bstack1l11ll11lll_opy_ < version.parse(bstack1ll11ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᎫ"))
        ):
            bstack1l11ll1llll_opy_ = {}
            bstack1l11ll1llll_opy_.update(bstack1l1l11l11ll_opy_)
        self.logger.info(bstack1lll1ll1ll_opy_)
        if os.environ.get(bstack1ll11ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᎬ")).lower().__eq__(bstack1ll11ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᎭ")):
            kwargs.update(
                {
                    bstack1ll11ll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᎮ"): f.bstack1l11ll1l1l1_opy_,
                }
            )
        if bstack1l11ll11lll_opy_ >= version.parse(bstack1ll11ll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭Ꭿ")):
            if bstack1l11ll1ll1l_opy_ is not None:
                del kwargs[bstack1ll11ll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᎰ")]
            kwargs.update(
                {
                    bstack1ll11ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᎱ"): bstack1l11ll1l11l_opy_,
                    bstack1ll11ll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᎲ"): True,
                    bstack1ll11ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᎳ"): None,
                }
            )
        elif bstack1l11ll11lll_opy_ >= version.parse(bstack1ll11ll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᎴ")):
            kwargs.update(
                {
                    bstack1ll11ll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᎵ"): bstack1l11ll1llll_opy_,
                    bstack1ll11ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᎶ"): bstack1l11ll1l11l_opy_,
                    bstack1ll11ll_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᎷ"): True,
                    bstack1ll11ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᎸ"): None,
                }
            )
        elif bstack1l11ll11lll_opy_ >= version.parse(bstack1ll11ll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᎹ")):
            kwargs.update(
                {
                    bstack1ll11ll_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᎺ"): bstack1l11ll1llll_opy_,
                    bstack1ll11ll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᎻ"): True,
                    bstack1ll11ll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᎼ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll11ll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎽ"): bstack1l11ll1llll_opy_,
                    bstack1ll11ll_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᎾ"): True,
                    bstack1ll11ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᎿ"): None,
                }
            )