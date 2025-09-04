# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
class bstack1lll1111111_opy_(bstack1lll1lll111_opy_):
    bstack1l11l1lllll_opy_ = bstack1111l1l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢ፪")
    bstack1l11lll1ll1_opy_ = bstack1111l1l_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤ፫")
    bstack1l11ll11l11_opy_ = bstack1111l1l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤ፬")
    def __init__(self, bstack1ll1l1lll11_opy_):
        super().__init__()
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1lllll1ll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l11ll1l1l1_opy_)
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1ll1111111l_opy_)
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.POST), self.bstack1l11ll1l111_opy_)
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.POST), self.bstack1l11ll1lll1_opy_)
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.QUIT, bstack1llll1lllll_opy_.POST), self.bstack1l11lll1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1l1l1_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l1l_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧ፭"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1111l1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፮")), str):
                    url = kwargs.get(bstack1111l1l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ፯"))
                elif hasattr(kwargs.get(bstack1111l1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ፰")), bstack1111l1l_opy_ (u"ࠧࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠨ፱")):
                    url = kwargs.get(bstack1111l1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፲"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1111l1l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ፳"))._url
            except Exception as e:
                url = bstack1111l1l_opy_ (u"ࠪࠫ፴")
                self.logger.error(bstack1111l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡷࡲࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࡻࡾࠤ፵").format(e))
            self.logger.info(bstack1111l1l_opy_ (u"ࠧࡘࡥ࡮ࡱࡷࡩ࡙ࠥࡥࡳࡸࡨࡶࠥࡇࡤࡥࡴࡨࡷࡸࠦࡢࡦ࡫ࡱ࡫ࠥࡶࡡࡴࡵࡨࡨࠥࡧࡳࠡ࠼ࠣࡿࢂࠨ፶").format(str(url)))
            self.bstack1l11ll11ll1_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1111l1l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦ፷").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll1111111l_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lllll1l11l_opy_(instance, bstack1lll1111111_opy_.bstack1l11l1lllll_opy_, False):
            return
        if not f.bstack1llll1l11ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_):
            return
        platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_)
        if f.bstack1ll11ll111l_opy_(method_name, *args) and len(args) > 1:
            bstack1ll1l1lll_opy_ = datetime.now()
            hub_url = bstack1lll1l111ll_opy_.hub_url(driver)
            self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤ፸") + str(hub_url) + bstack1111l1l_opy_ (u"ࠣࠤ፹"))
            bstack1l11ll1l11l_opy_ = args[1][bstack1111l1l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ፺")] if isinstance(args[1], dict) and bstack1111l1l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ፻") in args[1] else None
            bstack1l11lll1111_opy_ = bstack1111l1l_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤ፼")
            if isinstance(bstack1l11ll1l11l_opy_, dict):
                bstack1ll1l1lll_opy_ = datetime.now()
                r = self.bstack1l11ll1llll_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥ፽"), datetime.now() - bstack1ll1l1lll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1111l1l_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀࠠࠣ፾") + str(r) + bstack1111l1l_opy_ (u"ࠢࠣ፿"))
                        return
                    if r.hub_url:
                        f.bstack1l11ll11lll_opy_(instance, driver, r.hub_url)
                        f.bstack1lllllllll1_opy_(instance, bstack1lll1111111_opy_.bstack1l11l1lllll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1111l1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᎀ"), e)
    def bstack1l11ll1l111_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1l111ll_opy_.session_id(driver)
            if session_id:
                bstack1l11lll11ll_opy_ = bstack1111l1l_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᎁ").format(session_id)
                bstack1lll11111ll_opy_.mark(bstack1l11lll11ll_opy_)
    def bstack1l11ll1lll1_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1l11l_opy_(instance, bstack1lll1111111_opy_.bstack1l11lll1ll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1l111ll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᎂ") + str(hub_url) + bstack1111l1l_opy_ (u"ࠦࠧᎃ"))
            return
        framework_session_id = bstack1lll1l111ll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᎄ") + str(framework_session_id) + bstack1111l1l_opy_ (u"ࠨࠢᎅ"))
            return
        if bstack1lll1l111ll_opy_.bstack1l11ll111l1_opy_(*args) == bstack1lll1l111ll_opy_.bstack1l11ll1ll1l_opy_:
            bstack1l11l1ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢᎆ").format(framework_session_id)
            bstack1l11lll11ll_opy_ = bstack1111l1l_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᎇ").format(framework_session_id)
            bstack1lll11111ll_opy_.end(
                label=bstack1111l1l_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧᎈ"),
                start=bstack1l11lll11ll_opy_,
                end=bstack1l11l1ll1ll_opy_,
                status=True,
                failure=None
            )
            bstack1ll1l1lll_opy_ = datetime.now()
            r = self.bstack1l11ll1l1ll_opy_(
                ref,
                f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᎉ"), datetime.now() - bstack1ll1l1lll_opy_)
            f.bstack1lllllllll1_opy_(instance, bstack1lll1111111_opy_.bstack1l11lll1ll1_opy_, r.success)
    def bstack1l11lll1l11_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1l11l_opy_(instance, bstack1lll1111111_opy_.bstack1l11ll11l11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1l111ll_opy_.session_id(driver)
        hub_url = bstack1lll1l111ll_opy_.hub_url(driver)
        bstack1ll1l1lll_opy_ = datetime.now()
        r = self.bstack1l11ll11l1l_opy_(
            ref,
            f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᎊ"), datetime.now() - bstack1ll1l1lll_opy_)
        f.bstack1lllllllll1_opy_(instance, bstack1lll1111111_opy_.bstack1l11ll11l11_opy_, r.success)
    @measure(event_name=EVENTS.bstack11l11111l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l1l111l1ll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥᎋ") + str(req) + bstack1111l1l_opy_ (u"ࠨࠢᎌ"))
        try:
            r = self.bstack1ll1ll11l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᎍ") + str(r.success) + bstack1111l1l_opy_ (u"ࠣࠤᎎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎏ") + str(e) + bstack1111l1l_opy_ (u"ࠥࠦ᎐"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1111l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l11ll1llll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨ᎑") + str(req) + bstack1111l1l_opy_ (u"ࠧࠨ᎒"))
        try:
            r = self.bstack1ll1ll11l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤ᎓") + str(r.success) + bstack1111l1l_opy_ (u"ࠢࠣ᎔"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᎕") + str(e) + bstack1111l1l_opy_ (u"ࠤࠥ᎖"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1llll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l11ll1l1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨ᎗") + str(req) + bstack1111l1l_opy_ (u"ࠦࠧ᎘"))
        try:
            r = self.bstack1ll1ll11l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢ᎙") + str(r) + bstack1111l1l_opy_ (u"ࠨࠢ᎚"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ᎛") + str(e) + bstack1111l1l_opy_ (u"ࠣࠤ᎜"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1ll11_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l11ll11l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦ᎝") + str(req) + bstack1111l1l_opy_ (u"ࠥࠦ᎞"))
        try:
            r = self.bstack1ll1ll11l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨ᎟") + str(r) + bstack1111l1l_opy_ (u"ࠧࠨᎠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᎡ") + str(e) + bstack1111l1l_opy_ (u"ࠢࠣᎢ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l11ll11ll1_opy_(self, instance: bstack1llllllll1l_opy_, url: str, f: bstack1lll1l111ll_opy_, kwargs):
        bstack1l11lll11l1_opy_ = version.parse(f.framework_version)
        bstack1l11l1lll1l_opy_ = kwargs.get(bstack1111l1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᎣ"))
        bstack1l11l1lll11_opy_ = kwargs.get(bstack1111l1l_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎤ"))
        bstack1l1l11l1l1l_opy_ = {}
        bstack1l11ll11111_opy_ = {}
        bstack1l11lll111l_opy_ = None
        bstack1l11lll1l1l_opy_ = {}
        if bstack1l11l1lll11_opy_ is not None or bstack1l11l1lll1l_opy_ is not None: # check top level caps
            if bstack1l11l1lll11_opy_ is not None:
                bstack1l11lll1l1l_opy_[bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᎥ")] = bstack1l11l1lll11_opy_
            if bstack1l11l1lll1l_opy_ is not None and callable(getattr(bstack1l11l1lll1l_opy_, bstack1111l1l_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎦ"))):
                bstack1l11lll1l1l_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᎧ")] = bstack1l11l1lll1l_opy_.to_capabilities()
        response = self.bstack1l1l111l1ll_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11lll1l1l_opy_).encode(bstack1111l1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᎨ")))
        if response is not None and response.capabilities:
            bstack1l1l11l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1111l1l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᎩ")))
            if not bstack1l1l11l1l1l_opy_: # empty caps bstack1l1l11l1ll1_opy_ bstack1l1l11ll111_opy_ bstack1l1l111l11l_opy_ bstack1llll11l111_opy_ or error in processing
                return
            bstack1l11lll111l_opy_ = f.bstack1lll1l11l1l_opy_[bstack1111l1l_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧᎪ")](bstack1l1l11l1l1l_opy_)
        if bstack1l11l1lll1l_opy_ is not None and bstack1l11lll11l1_opy_ >= version.parse(bstack1111l1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᎫ")):
            bstack1l11ll11111_opy_ = None
        if (
                not bstack1l11l1lll1l_opy_ and not bstack1l11l1lll11_opy_
        ) or (
                bstack1l11lll11l1_opy_ < version.parse(bstack1111l1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᎬ"))
        ):
            bstack1l11ll11111_opy_ = {}
            bstack1l11ll11111_opy_.update(bstack1l1l11l1l1l_opy_)
        self.logger.info(bstack1ll111l1_opy_)
        if os.environ.get(bstack1111l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᎭ")).lower().__eq__(bstack1111l1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᎮ")):
            kwargs.update(
                {
                    bstack1111l1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᎯ"): f.bstack1l11ll111ll_opy_,
                }
            )
        if bstack1l11lll11l1_opy_ >= version.parse(bstack1111l1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᎰ")):
            if bstack1l11l1lll11_opy_ is not None:
                del kwargs[bstack1111l1l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎱ")]
            kwargs.update(
                {
                    bstack1111l1l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᎲ"): bstack1l11lll111l_opy_,
                    bstack1111l1l_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᎳ"): True,
                    bstack1111l1l_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᎴ"): None,
                }
            )
        elif bstack1l11lll11l1_opy_ >= version.parse(bstack1111l1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᎵ")):
            kwargs.update(
                {
                    bstack1111l1l_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎶ"): bstack1l11ll11111_opy_,
                    bstack1111l1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᎷ"): bstack1l11lll111l_opy_,
                    bstack1111l1l_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᎸ"): True,
                    bstack1111l1l_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᎹ"): None,
                }
            )
        elif bstack1l11lll11l1_opy_ >= version.parse(bstack1111l1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᎺ")):
            kwargs.update(
                {
                    bstack1111l1l_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᎻ"): bstack1l11ll11111_opy_,
                    bstack1111l1l_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᎼ"): True,
                    bstack1111l1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᎽ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1111l1l_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᎾ"): bstack1l11ll11111_opy_,
                    bstack1111l1l_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᎿ"): True,
                    bstack1111l1l_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᏀ"): None,
                }
            )