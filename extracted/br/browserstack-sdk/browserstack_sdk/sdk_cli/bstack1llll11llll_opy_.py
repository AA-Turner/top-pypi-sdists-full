# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1111111111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1111l1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
class bstack1lll1111l11_opy_(bstack1llll11l1ll_opy_):
    bstack1l1l1111ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧዿ")
    bstack1l1l1111111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢጀ")
    bstack1l1l11111ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢጁ")
    def __init__(self, bstack1lll11l11ll_opy_):
        super().__init__()
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1111111lll_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l111l111_opy_)
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1ll111l1111_opy_)
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.POST), self.bstack1l11lll11ll_opy_)
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.POST), self.bstack1l11lllll1l_opy_)
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.QUIT, bstack1lllll1llll_opy_.POST), self.bstack1l11lll1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l111_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥጂ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1l1l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧጃ")), str):
                    url = kwargs.get(bstack1l1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨጄ"))
                elif hasattr(kwargs.get(bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢጅ")), bstack1l1l1l1_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ጆ")):
                    url = kwargs.get(bstack1l1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጇ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1l1l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥገ"))._url
            except Exception as e:
                url = bstack1l1l1l1_opy_ (u"ࠨࠩጉ")
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢጊ").format(e))
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦጋ").format(str(url)))
            self.bstack1l1l1111l11_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤጌ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll111l1111_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lllll1ll11_opy_(instance, bstack1lll1111l11_opy_.bstack1l1l1111ll1_opy_, False):
            return
        if not f.bstack1lllllll1ll_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_):
            return
        platform_index = f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_)
        if f.bstack1ll111ll11l_opy_(method_name, *args) and len(args) > 1:
            bstack1l1ll1l1ll_opy_ = datetime.now()
            hub_url = bstack1llll111lll_opy_.hub_url(driver)
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢግ") + str(hub_url) + bstack1l1l1l1_opy_ (u"ࠨࠢጎ"))
            bstack1l1l1111lll_opy_ = args[1][bstack1l1l1l1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጏ")] if isinstance(args[1], dict) and bstack1l1l1l1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢጐ") in args[1] else None
            bstack1l11ll1llll_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢ጑")
            if isinstance(bstack1l1l1111lll_opy_, dict):
                bstack1l1ll1l1ll_opy_ = datetime.now()
                r = self.bstack1l11llll11l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣጒ"), datetime.now() - bstack1l1ll1l1ll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨጓ") + str(r) + bstack1l1l1l1_opy_ (u"ࠧࠨጔ"))
                        return
                    if r.hub_url:
                        f.bstack1l11llll1ll_opy_(instance, driver, r.hub_url)
                        f.bstack1lllll1111l_opy_(instance, bstack1lll1111l11_opy_.bstack1l1l1111ll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧጕ"), e)
    def bstack1l11lll11ll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llll111lll_opy_.session_id(driver)
            if session_id:
                bstack1l11lll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤ጖").format(session_id)
                bstack1lll1ll11l1_opy_.mark(bstack1l11lll1l1l_opy_)
    def bstack1l11lllll1l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1ll11_opy_(instance, bstack1lll1111l11_opy_.bstack1l1l1111111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llll111lll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧ጗") + str(hub_url) + bstack1l1l1l1_opy_ (u"ࠤࠥጘ"))
            return
        framework_session_id = bstack1llll111lll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨጙ") + str(framework_session_id) + bstack1l1l1l1_opy_ (u"ࠦࠧጚ"))
            return
        if bstack1llll111lll_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll111lll_opy_.bstack1l11lll111l_opy_:
            bstack1l11lll1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧጛ").format(framework_session_id)
            bstack1l11lll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣጜ").format(framework_session_id)
            bstack1lll1ll11l1_opy_.end(
                label=bstack1l1l1l1_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥጝ"),
                start=bstack1l11lll1l1l_opy_,
                end=bstack1l11lll1lll_opy_,
                status=True,
                failure=None
            )
            bstack1l1ll1l1ll_opy_ = datetime.now()
            r = self.bstack1l11llll111_opy_(
                ref,
                f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢጞ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            f.bstack1lllll1111l_opy_(instance, bstack1lll1111l11_opy_.bstack1l1l1111111_opy_, r.success)
    def bstack1l11lll1111_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1ll11_opy_(instance, bstack1lll1111l11_opy_.bstack1l1l11111ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llll111lll_opy_.session_id(driver)
        hub_url = bstack1llll111lll_opy_.hub_url(driver)
        bstack1l1ll1l1ll_opy_ = datetime.now()
        r = self.bstack1l1l111l11l_opy_(
            ref,
            f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢጟ"), datetime.now() - bstack1l1ll1l1ll_opy_)
        f.bstack1lllll1111l_opy_(instance, bstack1lll1111l11_opy_.bstack1l1l11111ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1lllll1l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l1l1l11lll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣጠ") + str(req) + bstack1l1l1l1_opy_ (u"ࠦࠧጡ"))
        try:
            r = self.bstack1ll1ll111l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣጢ") + str(r.success) + bstack1l1l1l1_opy_ (u"ࠨࠢጣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧጤ") + str(e) + bstack1l1l1l1_opy_ (u"ࠣࠤጥ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1111l1l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l11llll11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦጦ") + str(req) + bstack1l1l1l1_opy_ (u"ࠥࠦጧ"))
        try:
            r = self.bstack1ll1ll111l1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢጨ") + str(r.success) + bstack1l1l1l1_opy_ (u"ࠧࠨጩ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦጪ") + str(e) + bstack1l1l1l1_opy_ (u"ࠢࠣጫ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11ll1lll1_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l11llll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦጬ") + str(req) + bstack1l1l1l1_opy_ (u"ࠤࠥጭ"))
        try:
            r = self.bstack1ll1ll111l1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧጮ") + str(r) + bstack1l1l1l1_opy_ (u"ࠦࠧጯ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥጰ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢጱ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l111111l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l1l111l11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤጲ") + str(req) + bstack1l1l1l1_opy_ (u"ࠣࠤጳ"))
        try:
            r = self.bstack1ll1ll111l1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦጴ") + str(r) + bstack1l1l1l1_opy_ (u"ࠥࠦጵ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጶ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨጷ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11l1l11_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l1l1111l11_opy_(self, instance: bstack1111111111_opy_, url: str, f: bstack1llll111lll_opy_, kwargs):
        bstack1l11llllll1_opy_ = version.parse(f.framework_version)
        bstack1l11lll1l11_opy_ = kwargs.get(bstack1l1l1l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢጸ"))
        bstack1l11lllllll_opy_ = kwargs.get(bstack1l1l1l1_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢጹ"))
        bstack1l1l1l1111l_opy_ = {}
        bstack1l11llll1l1_opy_ = {}
        bstack1l11lll11l1_opy_ = None
        bstack1l11lllll11_opy_ = {}
        if bstack1l11lllllll_opy_ is not None or bstack1l11lll1l11_opy_ is not None: # check top level caps
            if bstack1l11lllllll_opy_ is not None:
                bstack1l11lllll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨጺ")] = bstack1l11lllllll_opy_
            if bstack1l11lll1l11_opy_ is not None and callable(getattr(bstack1l11lll1l11_opy_, bstack1l1l1l1_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦጻ"))):
                bstack1l11lllll11_opy_[bstack1l1l1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ጼ")] = bstack1l11lll1l11_opy_.to_capabilities()
        response = self.bstack1l1l1l11lll_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11lllll11_opy_).encode(bstack1l1l1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥጽ")))
        if response is not None and response.capabilities:
            bstack1l1l1l1111l_opy_ = json.loads(response.capabilities.decode(bstack1l1l1l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦጾ")))
            if not bstack1l1l1l1111l_opy_: # empty caps bstack1l1l1l11111_opy_ bstack1l1l1l1ll11_opy_ bstack1l1l1l1l1l1_opy_ bstack1ll1l1lll1l_opy_ or error in processing
                return
            bstack1l11lll11l1_opy_ = f.bstack1lll1l11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥጿ")](bstack1l1l1l1111l_opy_)
        if bstack1l11lll1l11_opy_ is not None and bstack1l11llllll1_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ፀ")):
            bstack1l11llll1l1_opy_ = None
        if (
                not bstack1l11lll1l11_opy_ and not bstack1l11lllllll_opy_
        ) or (
                bstack1l11llllll1_opy_ < version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧፁ"))
        ):
            bstack1l11llll1l1_opy_ = {}
            bstack1l11llll1l1_opy_.update(bstack1l1l1l1111l_opy_)
        self.logger.info(bstack1l1111l1ll_opy_)
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧፂ")).lower().__eq__(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣፃ")):
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢፄ"): f.bstack1l11lll1ll1_opy_,
                }
            )
        if bstack1l11llllll1_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬፅ")):
            if bstack1l11lllllll_opy_ is not None:
                del kwargs[bstack1l1l1l1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨፆ")]
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣፇ"): bstack1l11lll11l1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧፈ"): True,
                    bstack1l1l1l1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤፉ"): None,
                }
            )
        elif bstack1l11llllll1_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩፊ")):
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦፋ"): bstack1l11llll1l1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨፌ"): bstack1l11lll11l1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥፍ"): True,
                    bstack1l1l1l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢፎ"): None,
                }
            )
        elif bstack1l11llllll1_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨፏ")):
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤፐ"): bstack1l11llll1l1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢፑ"): True,
                    bstack1l1l1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦፒ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧፓ"): bstack1l11llll1l1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥፔ"): True,
                    bstack1l1l1l1_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢፕ"): None,
                }
            )