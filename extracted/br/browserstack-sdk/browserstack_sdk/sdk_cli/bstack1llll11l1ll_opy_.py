# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1lll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllll1l1l1_opy_,
    bstack1llllllllll_opy_,
    bstack1lllllllll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import bstack1ll1lllllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l111ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack111ll111l_opy_ import bstack1lll11l111l_opy_
class bstack1ll1l1lllll_opy_(bstack1lll11l11ll_opy_):
    bstack1l11ll1l111_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤ፥")
    bstack1l11ll111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦ፦")
    bstack1l11ll1ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦ፧")
    def __init__(self, bstack1lll11111l1_opy_):
        super().__init__()
        bstack1ll1lllllll_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack1111111l1l_opy_, bstack1llllllllll_opy_.PRE), self.bstack1l11ll11lll_opy_)
        bstack1ll1lllllll_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack11111111l1_opy_, bstack1llllllllll_opy_.PRE), self.bstack1ll11111ll1_opy_)
        bstack1ll1lllllll_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack11111111l1_opy_, bstack1llllllllll_opy_.POST), self.bstack1l11ll111ll_opy_)
        bstack1ll1lllllll_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.bstack11111111l1_opy_, bstack1llllllllll_opy_.POST), self.bstack1l11ll11l1l_opy_)
        bstack1ll1lllllll_opy_.bstack1ll1l11lll1_opy_((bstack1lllll1l1l1_opy_.QUIT, bstack1llllllllll_opy_.POST), self.bstack1l11ll1lll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll11lll_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1ll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢ፨"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1l1ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ፩")), str):
                    url = kwargs.get(bstack1l1l1ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ፪"))
                elif hasattr(kwargs.get(bstack1l1l1ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ፫")), bstack1l1l1ll_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪ፬")):
                    url = kwargs.get(bstack1l1l1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ፭"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1l1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ፮"))._url
            except Exception as e:
                url = bstack1l1l1ll_opy_ (u"ࠬ࠭፯")
                self.logger.error(bstack1l1l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦ፰").format(e))
            self.logger.info(bstack1l1l1ll_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣ፱").format(str(url)))
            self.bstack1l11ll11111_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l1l1ll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁ࠿ࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨ፲").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11111ll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llll1llll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l11ll1l111_opy_, False):
            return
        if not f.bstack1llllll11ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll1l11l1ll_opy_):
            return
        platform_index = f.bstack1llll1llll1_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll1l11l1ll_opy_)
        if f.bstack1ll1111llll_opy_(method_name, *args) and len(args) > 1:
            bstack1lll111ll1_opy_ = datetime.now()
            hub_url = bstack1ll1lllllll_opy_.hub_url(driver)
            self.logger.warning(bstack1l1l1ll_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦ፳") + str(hub_url) + bstack1l1l1ll_opy_ (u"ࠥࠦ፴"))
            bstack1l11lll11l1_opy_ = args[1][bstack1l1l1ll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ፵")] if isinstance(args[1], dict) and bstack1l1l1ll_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ፶") in args[1] else None
            bstack1l11llll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦ፷")
            if isinstance(bstack1l11lll11l1_opy_, dict):
                bstack1lll111ll1_opy_ = datetime.now()
                r = self.bstack1l11ll1111l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧ፸"), datetime.now() - bstack1lll111ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1l1ll_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥ፹") + str(r) + bstack1l1l1ll_opy_ (u"ࠤࠥ፺"))
                        return
                    if r.hub_url:
                        f.bstack1l11lll1l11_opy_(instance, driver, r.hub_url)
                        f.bstack1lllllll111_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l11ll1l111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1l1ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ፻"), e)
    def bstack1l11ll111ll_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1lllllll_opy_.session_id(driver)
            if session_id:
                bstack1l11llll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨ፼").format(session_id)
                bstack1lll11l111l_opy_.mark(bstack1l11llll11l_opy_)
    def bstack1l11ll11l1l_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll1llll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l11ll111l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1lllllll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1l1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤ፽") + str(hub_url) + bstack1l1l1ll_opy_ (u"ࠨࠢ፾"))
            return
        framework_session_id = bstack1ll1lllllll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1l1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥ፿") + str(framework_session_id) + bstack1l1l1ll_opy_ (u"ࠣࠤᎀ"))
            return
        if bstack1ll1lllllll_opy_.bstack1l11ll11l11_opy_(*args) == bstack1ll1lllllll_opy_.bstack1l11lll1lll_opy_:
            bstack1l11lll111l_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤᎁ").format(framework_session_id)
            bstack1l11llll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᎂ").format(framework_session_id)
            bstack1lll11l111l_opy_.end(
                label=bstack1l1l1ll_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢᎃ"),
                start=bstack1l11llll11l_opy_,
                end=bstack1l11lll111l_opy_,
                status=True,
                failure=None
            )
            bstack1lll111ll1_opy_ = datetime.now()
            r = self.bstack1l11llll1l1_opy_(
                ref,
                f.bstack1llll1llll1_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll1l11l1ll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᎄ"), datetime.now() - bstack1lll111ll1_opy_)
            f.bstack1lllllll111_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l11ll111l1_opy_, r.success)
    def bstack1l11ll1lll1_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllllll1_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1lllll1l1l1_opy_, bstack1llllllllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll1llll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l11ll1ll11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1lllllll_opy_.session_id(driver)
        hub_url = bstack1ll1lllllll_opy_.hub_url(driver)
        bstack1lll111ll1_opy_ = datetime.now()
        r = self.bstack1l11lll1111_opy_(
            ref,
            f.bstack1llll1llll1_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll1l11l1ll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1ll11ll_opy_(bstack1l1l1ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᎅ"), datetime.now() - bstack1lll111ll1_opy_)
        f.bstack1lllllll111_opy_(instance, bstack1ll1l1lllll_opy_.bstack1l11ll1ll11_opy_, r.success)
    @measure(event_name=EVENTS.bstack11ll1lll11_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l1l11l1ll1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᎆ") + str(req) + bstack1l1l1ll_opy_ (u"ࠣࠤᎇ"))
        try:
            r = self.bstack1lll11ll1l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᎈ") + str(r.success) + bstack1l1l1ll_opy_ (u"ࠥࠦᎉ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᎊ") + str(e) + bstack1l1l1ll_opy_ (u"ࠧࠨᎋ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11llll111_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l11ll1111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l111ll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᎌ") + str(req) + bstack1l1l1ll_opy_ (u"ࠢࠣᎍ"))
        try:
            r = self.bstack1lll11ll1l1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᎎ") + str(r.success) + bstack1l1l1ll_opy_ (u"ࠤࠥᎏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ᎐") + str(e) + bstack1l1l1ll_opy_ (u"ࠦࠧ᎑"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll1ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l11llll1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l111ll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣ᎒") + str(req) + bstack1l1l1ll_opy_ (u"ࠨࠢ᎓"))
        try:
            r = self.bstack1lll11ll1l1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤ᎔") + str(r) + bstack1l1l1ll_opy_ (u"ࠣࠤ᎕"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ᎖") + str(e) + bstack1l1l1ll_opy_ (u"ࠥࠦ᎗"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1ll1l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l11lll1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l111ll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨ᎘") + str(req) + bstack1l1l1ll_opy_ (u"ࠧࠨ᎙"))
        try:
            r = self.bstack1lll11ll1l1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ᎚") + str(r) + bstack1l1l1ll_opy_ (u"ࠢࠣ᎛"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᎜") + str(e) + bstack1l1l1ll_opy_ (u"ࠤࠥ᎝"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll111ll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1l11ll11111_opy_(self, instance: bstack1lllllllll1_opy_, url: str, f: bstack1ll1lllllll_opy_, kwargs):
        bstack1l11ll1llll_opy_ = version.parse(f.framework_version)
        bstack1l11ll1l1l1_opy_ = kwargs.get(bstack1l1l1ll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦ᎞"))
        bstack1l11lll11ll_opy_ = kwargs.get(bstack1l1l1ll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᎟"))
        bstack1l1l11l1l1l_opy_ = {}
        bstack1l11lll1l1l_opy_ = {}
        bstack1l11ll1l1ll_opy_ = None
        bstack1l11ll1l11l_opy_ = {}
        if bstack1l11lll11ll_opy_ is not None or bstack1l11ll1l1l1_opy_ is not None: # check top level caps
            if bstack1l11lll11ll_opy_ is not None:
                bstack1l11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᎠ")] = bstack1l11lll11ll_opy_
            if bstack1l11ll1l1l1_opy_ is not None and callable(getattr(bstack1l11ll1l1l1_opy_, bstack1l1l1ll_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎡ"))):
                bstack1l11ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᎢ")] = bstack1l11ll1l1l1_opy_.to_capabilities()
        response = self.bstack1l1l11l1ll1_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11ll1l11l_opy_).encode(bstack1l1l1ll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᎣ")))
        if response is not None and response.capabilities:
            bstack1l1l11l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1l1l1ll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᎤ")))
            if not bstack1l1l11l1l1l_opy_: # empty caps bstack1l1l11l1lll_opy_ bstack1l1l1l11111_opy_ bstack1l1l11l1l11_opy_ bstack1ll1ll1l1l1_opy_ or error in processing
                return
            bstack1l11ll1l1ll_opy_ = f.bstack1ll1l1lll11_opy_[bstack1l1l1ll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᎥ")](bstack1l1l11l1l1l_opy_)
        if bstack1l11ll1l1l1_opy_ is not None and bstack1l11ll1llll_opy_ >= version.parse(bstack1l1l1ll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᎦ")):
            bstack1l11lll1l1l_opy_ = None
        if (
                not bstack1l11ll1l1l1_opy_ and not bstack1l11lll11ll_opy_
        ) or (
                bstack1l11ll1llll_opy_ < version.parse(bstack1l1l1ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᎧ"))
        ):
            bstack1l11lll1l1l_opy_ = {}
            bstack1l11lll1l1l_opy_.update(bstack1l1l11l1l1l_opy_)
        self.logger.info(bstack1l111ll1ll_opy_)
        if os.environ.get(bstack1l1l1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤᎨ")).lower().__eq__(bstack1l1l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᎩ")):
            kwargs.update(
                {
                    bstack1l1l1ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᎪ"): f.bstack1l11ll11ll1_opy_,
                }
            )
        if bstack1l11ll1llll_opy_ >= version.parse(bstack1l1l1ll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᎫ")):
            if bstack1l11lll11ll_opy_ is not None:
                del kwargs[bstack1l1l1ll_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᎬ")]
            kwargs.update(
                {
                    bstack1l1l1ll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᎭ"): bstack1l11ll1l1ll_opy_,
                    bstack1l1l1ll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᎮ"): True,
                    bstack1l1l1ll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᎯ"): None,
                }
            )
        elif bstack1l11ll1llll_opy_ >= version.parse(bstack1l1l1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭Ꮀ")):
            kwargs.update(
                {
                    bstack1l1l1ll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᎱ"): bstack1l11lll1l1l_opy_,
                    bstack1l1l1ll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᎲ"): bstack1l11ll1l1ll_opy_,
                    bstack1l1l1ll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᎳ"): True,
                    bstack1l1l1ll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᎴ"): None,
                }
            )
        elif bstack1l11ll1llll_opy_ >= version.parse(bstack1l1l1ll_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᎵ")):
            kwargs.update(
                {
                    bstack1l1l1ll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᎶ"): bstack1l11lll1l1l_opy_,
                    bstack1l1l1ll_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᎷ"): True,
                    bstack1l1l1ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᎸ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1l1ll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᎹ"): bstack1l11lll1l1l_opy_,
                    bstack1l1l1ll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᎺ"): True,
                    bstack1l1l1ll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᎻ"): None,
                }
            )