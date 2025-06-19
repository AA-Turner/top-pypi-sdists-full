# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1llllll111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
class bstack1lllll111ll_opy_(bstack1lll1l11ll1_opy_):
    bstack1l1l11l111l_opy_ = bstack111lll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦደ")
    bstack1l1l11l1111_opy_ = bstack111lll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨዱ")
    bstack1l1l11l1l1l_opy_ = bstack111lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨዲ")
    def __init__(self, bstack1ll1ll1l1l1_opy_):
        super().__init__()
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack1lllllll1l1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1l111l1l1_opy_)
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1ll11l111ll_opy_)
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.POST), self.bstack1l1l1111l1l_opy_)
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.POST), self.bstack1l1l1111lll_opy_)
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.QUIT, bstack11111l1ll1_opy_.POST), self.bstack1l11llllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1l1_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111lll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤዳ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack111lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦዴ")), str):
                    url = kwargs.get(bstack111lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧድ"))
                elif hasattr(kwargs.get(bstack111lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨዶ")), bstack111lll_opy_ (u"ࠫࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠬዷ")):
                    url = kwargs.get(bstack111lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣዸ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack111lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤዹ"))._url
            except Exception as e:
                url = bstack111lll_opy_ (u"ࠧࠨዺ")
                self.logger.error(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡴ࡯ࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࢂࠨዻ").format(e))
            self.logger.info(bstack111lll_opy_ (u"ࠤࡕࡩࡲࡵࡴࡦࠢࡖࡩࡷࡼࡥࡳࠢࡄࡨࡩࡸࡥࡴࡵࠣࡦࡪ࡯࡮ࡨࠢࡳࡥࡸࡹࡥࡥࠢࡤࡷࠥࡀࠠࡼࡿࠥዼ").format(str(url)))
            self.bstack1l1l111lll1_opy_(instance, url, f, kwargs)
            self.logger.info(bstack111lll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣዽ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11l111ll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1llllll1l1l_opy_(instance, bstack1lllll111ll_opy_.bstack1l1l11l111l_opy_, False):
            return
        if not f.bstack11111111ll_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_):
            return
        platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_)
        if f.bstack1ll1l11l111_opy_(method_name, *args) and len(args) > 1:
            bstack11ll1ll1_opy_ = datetime.now()
            hub_url = bstack1llll111lll_opy_.hub_url(driver)
            self.logger.warning(bstack111lll_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࡂࠨዾ") + str(hub_url) + bstack111lll_opy_ (u"ࠧࠨዿ"))
            bstack1l1l111ll11_opy_ = args[1][bstack111lll_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧጀ")] if isinstance(args[1], dict) and bstack111lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጁ") in args[1] else None
            bstack1l1l1111111_opy_ = bstack111lll_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨጂ")
            if isinstance(bstack1l1l111ll11_opy_, dict):
                bstack11ll1ll1_opy_ = datetime.now()
                r = self.bstack1l1l11l1l11_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢጃ"), datetime.now() - bstack11ll1ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack111lll_opy_ (u"ࠥࡷࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩ࠽ࠤࠧጄ") + str(r) + bstack111lll_opy_ (u"ࠦࠧጅ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l1111ll1_opy_(instance, driver, r.hub_url)
                        f.bstack11111ll111_opy_(instance, bstack1lllll111ll_opy_.bstack1l1l11l111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack111lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦጆ"), e)
    def bstack1l1l1111l1l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llll111lll_opy_.session_id(driver)
            if session_id:
                bstack1l1l111ll1l_opy_ = bstack111lll_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣጇ").format(session_id)
                bstack1llll1l1l11_opy_.mark(bstack1l1l111ll1l_opy_)
    def bstack1l1l1111lll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllll1l1l_opy_(instance, bstack1lllll111ll_opy_.bstack1l1l11l1111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llll111lll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦገ") + str(hub_url) + bstack111lll_opy_ (u"ࠣࠤጉ"))
            return
        framework_session_id = bstack1llll111lll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧጊ") + str(framework_session_id) + bstack111lll_opy_ (u"ࠥࠦጋ"))
            return
        if bstack1llll111lll_opy_.bstack1l1l111l11l_opy_(*args) == bstack1llll111lll_opy_.bstack1l1l111l1ll_opy_:
            bstack1l1l11111l1_opy_ = bstack111lll_opy_ (u"ࠦࢀࢃ࠺ࡦࡰࡧࠦጌ").format(framework_session_id)
            bstack1l1l111ll1l_opy_ = bstack111lll_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢግ").format(framework_session_id)
            bstack1llll1l1l11_opy_.end(
                label=bstack111lll_opy_ (u"ࠨࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠤጎ"),
                start=bstack1l1l111ll1l_opy_,
                end=bstack1l1l11111l1_opy_,
                status=True,
                failure=None
            )
            bstack11ll1ll1_opy_ = datetime.now()
            r = self.bstack1l1l11l11ll_opy_(
                ref,
                f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨጏ"), datetime.now() - bstack11ll1ll1_opy_)
            f.bstack11111ll111_opy_(instance, bstack1lllll111ll_opy_.bstack1l1l11l1111_opy_, r.success)
    def bstack1l11llllll1_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llllll1l1l_opy_(instance, bstack1lllll111ll_opy_.bstack1l1l11l1l1l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llll111lll_opy_.session_id(driver)
        hub_url = bstack1llll111lll_opy_.hub_url(driver)
        bstack11ll1ll1_opy_ = datetime.now()
        r = self.bstack1l1l1111l11_opy_(
            ref,
            f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨጐ"), datetime.now() - bstack11ll1ll1_opy_)
        f.bstack11111ll111_opy_(instance, bstack1lllll111ll_opy_.bstack1l1l11l1l1l_opy_, r.success)
    @measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l1ll111l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack111lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢ጑") + str(req) + bstack111lll_opy_ (u"ࠥࠦጒ"))
        try:
            r = self.bstack1lll1ll1l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢጓ") + str(r.success) + bstack111lll_opy_ (u"ࠧࠨጔ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦጕ") + str(e) + bstack111lll_opy_ (u"ࠢࠣ጖"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lllll1l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l11l1l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack111lll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥ጗") + str(req) + bstack111lll_opy_ (u"ࠤࠥጘ"))
        try:
            r = self.bstack1lll1ll1l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨጙ") + str(r.success) + bstack111lll_opy_ (u"ࠦࠧጚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥጛ") + str(e) + bstack111lll_opy_ (u"ࠨࠢጜ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l11l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l11l11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack111lll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴ࠻ࠢࠥጝ") + str(req) + bstack111lll_opy_ (u"ࠣࠤጞ"))
        try:
            r = self.bstack1lll1ll1l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦጟ") + str(r) + bstack111lll_opy_ (u"ࠥࠦጠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጡ") + str(e) + bstack111lll_opy_ (u"ࠧࠨጢ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l1lll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l1111l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack111lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࡀࠠࠣጣ") + str(req) + bstack111lll_opy_ (u"ࠢࠣጤ"))
        try:
            r = self.bstack1lll1ll1l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥጥ") + str(r) + bstack111lll_opy_ (u"ࠤࠥጦ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣጧ") + str(e) + bstack111lll_opy_ (u"ࠦࠧጨ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l11l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l111lll1_opy_(self, instance: bstack1llllll111l_opy_, url: str, f: bstack1llll111lll_opy_, kwargs):
        bstack1l11lllllll_opy_ = version.parse(f.framework_version)
        bstack1l1l111llll_opy_ = kwargs.get(bstack111lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨጩ"))
        bstack1l1l111l111_opy_ = kwargs.get(bstack111lll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጪ"))
        bstack1l1l1l1llll_opy_ = {}
        bstack1l1l11l1ll1_opy_ = {}
        bstack1l1l11ll111_opy_ = None
        bstack1l1l111111l_opy_ = {}
        if bstack1l1l111l111_opy_ is not None or bstack1l1l111llll_opy_ is not None: # check top level caps
            if bstack1l1l111l111_opy_ is not None:
                bstack1l1l111111l_opy_[bstack111lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧጫ")] = bstack1l1l111l111_opy_
            if bstack1l1l111llll_opy_ is not None and callable(getattr(bstack1l1l111llll_opy_, bstack111lll_opy_ (u"ࠣࡶࡲࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጬ"))):
                bstack1l1l111111l_opy_[bstack111lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࡢࡥࡸࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬጭ")] = bstack1l1l111llll_opy_.to_capabilities()
        response = self.bstack1l1l1ll111l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1l111111l_opy_).encode(bstack111lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤጮ")))
        if response is not None and response.capabilities:
            bstack1l1l1l1llll_opy_ = json.loads(response.capabilities.decode(bstack111lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥጯ")))
            if not bstack1l1l1l1llll_opy_: # empty caps bstack1l1l1ll1lll_opy_ bstack1l1l1l1ll1l_opy_ bstack1l1l1l1lll1_opy_ bstack1lll1l11l1l_opy_ or error in processing
                return
            bstack1l1l11ll111_opy_ = f.bstack1llll1l1ll1_opy_[bstack111lll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤጰ")](bstack1l1l1l1llll_opy_)
        if bstack1l1l111llll_opy_ is not None and bstack1l11lllllll_opy_ >= version.parse(bstack111lll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬጱ")):
            bstack1l1l11l1ll1_opy_ = None
        if (
                not bstack1l1l111llll_opy_ and not bstack1l1l111l111_opy_
        ) or (
                bstack1l11lllllll_opy_ < version.parse(bstack111lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ጲ"))
        ):
            bstack1l1l11l1ll1_opy_ = {}
            bstack1l1l11l1ll1_opy_.update(bstack1l1l1l1llll_opy_)
        self.logger.info(bstack11lll11l1l_opy_)
        if os.environ.get(bstack111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦጳ")).lower().__eq__(bstack111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢጴ")):
            kwargs.update(
                {
                    bstack111lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨጵ"): f.bstack1l1l11111ll_opy_,
                }
            )
        if bstack1l11lllllll_opy_ >= version.parse(bstack111lll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫጶ")):
            if bstack1l1l111l111_opy_ is not None:
                del kwargs[bstack111lll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧጷ")]
            kwargs.update(
                {
                    bstack111lll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢጸ"): bstack1l1l11ll111_opy_,
                    bstack111lll_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦጹ"): True,
                    bstack111lll_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣጺ"): None,
                }
            )
        elif bstack1l11lllllll_opy_ >= version.parse(bstack111lll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨጻ")):
            kwargs.update(
                {
                    bstack111lll_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጼ"): bstack1l1l11l1ll1_opy_,
                    bstack111lll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧጽ"): bstack1l1l11ll111_opy_,
                    bstack111lll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤጾ"): True,
                    bstack111lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨጿ"): None,
                }
            )
        elif bstack1l11lllllll_opy_ >= version.parse(bstack111lll_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧፀ")):
            kwargs.update(
                {
                    bstack111lll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣፁ"): bstack1l1l11l1ll1_opy_,
                    bstack111lll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨፂ"): True,
                    bstack111lll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥፃ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack111lll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦፄ"): bstack1l1l11l1ll1_opy_,
                    bstack111lll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤፅ"): True,
                    bstack111lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨፆ"): None,
                }
            )