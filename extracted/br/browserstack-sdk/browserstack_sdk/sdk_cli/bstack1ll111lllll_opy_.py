# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lll1llll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1111l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
class bstack1ll111lll11_opy_(bstack1lll1lllll1_opy_):
    bstack1ll11l1lll1_opy_ = bstack11l1111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢᇆ")
    bstack1ll111llll1_opy_ = bstack11l1111_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᇇ")
    bstack1ll11ll1ll1_opy_ = bstack11l1111_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᇈ")
    def __init__(self, bstack1ll11ll11ll_opy_):
        super().__init__()
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1ll11ll1lll_opy_)
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1lll111l1ll_opy_)
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1ll11l1l111_opy_)
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1ll11lll111_opy_)
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.QUIT, bstack1llllll1l1l_opy_.POST), self.bstack1ll11l11lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll1lll_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1111_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᇉ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11l1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᇊ")), str):
                    url = kwargs.get(bstack11l1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᇋ"))
                elif hasattr(kwargs.get(bstack11l1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᇌ")), bstack11l1111_opy_ (u"ࠧࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠨᇍ")):
                    url = kwargs.get(bstack11l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᇎ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11l1111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᇏ"))._url
            except Exception as e:
                url = bstack11l1111_opy_ (u"ࠪࠫᇐ")
                self.logger.error(bstack11l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡷࡲࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࡻࡾࠤᇑ").format(e))
            self.logger.info(bstack11l1111_opy_ (u"ࠧࡘࡥ࡮ࡱࡷࡩ࡙ࠥࡥࡳࡸࡨࡶࠥࡇࡤࡥࡴࡨࡷࡸࠦࡢࡦ࡫ࡱ࡫ࠥࡶࡡࡴࡵࡨࡨࠥࡧࡳࠡ࠼ࠣࡿࢂࠨᇒ").format(str(url)))
            self.bstack1ll11ll1l1l_opy_(instance, url, f, kwargs)
            self.logger.info(bstack11l1111_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᇓ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1lll111l1ll_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lllll1l11l_opy_(instance, bstack1ll111lll11_opy_.bstack1ll11l1lll1_opy_, False):
            return
        if not f.bstack1llllll1ll1_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_):
            return
        platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_)
        if f.bstack1ll11l11111_opy_(method_name, *args) and len(args) > 1:
            bstack1ll1l1l1_opy_ = datetime.now()
            hub_url = bstack1lll1ll1l1l_opy_.hub_url(driver)
            self.logger.warning(bstack11l1111_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᇔ") + str(hub_url) + bstack11l1111_opy_ (u"ࠣࠤᇕ"))
            bstack1ll11l1ll1l_opy_ = args[1][bstack11l1111_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᇖ")] if isinstance(args[1], dict) and bstack11l1111_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᇗ") in args[1] else None
            bstack1ll11l1l11l_opy_ = bstack11l1111_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᇘ")
            if isinstance(bstack1ll11l1ll1l_opy_, dict):
                bstack1ll1l1l1_opy_ = datetime.now()
                r = self.bstack1ll11l111l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥᇙ"), datetime.now() - bstack1ll1l1l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l1111_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀࠠࠣᇚ") + str(r) + bstack11l1111_opy_ (u"ࠢࠣᇛ"))
                        return
                    if r.hub_url:
                        f.bstack1ll11l11ll1_opy_(instance, driver, r.hub_url)
                        f.bstack1llll111l11_opy_(instance, bstack1ll111lll11_opy_.bstack1ll11l1lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᇜ"), e)
    def bstack1ll11l1l111_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1ll1l1l_opy_.session_id(driver)
            if session_id:
                bstack1ll11l11l1l_opy_ = bstack11l1111_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᇝ").format(session_id)
                bstack1lll1l1l11l_opy_.mark(bstack1ll11l11l1l_opy_)
    def bstack1ll11lll111_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1l11l_opy_(instance, bstack1ll111lll11_opy_.bstack1ll111llll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1ll1l1l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᇞ") + str(hub_url) + bstack11l1111_opy_ (u"ࠦࠧᇟ"))
            return
        framework_session_id = bstack1lll1ll1l1l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᇠ") + str(framework_session_id) + bstack11l1111_opy_ (u"ࠨࠢᇡ"))
            return
        if bstack1lll1ll1l1l_opy_.bstack1ll11l1l1ll_opy_(*args) == bstack1lll1ll1l1l_opy_.bstack1ll11ll1111_opy_:
            bstack1ll111ll1l1_opy_ = bstack11l1111_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢᇢ").format(framework_session_id)
            bstack1ll11l11l1l_opy_ = bstack11l1111_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᇣ").format(framework_session_id)
            bstack1lll1l1l11l_opy_.end(
                label=bstack11l1111_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧᇤ"),
                start=bstack1ll11l11l1l_opy_,
                end=bstack1ll111ll1l1_opy_,
                status=True,
                failure=None
            )
            bstack1ll1l1l1_opy_ = datetime.now()
            r = self.bstack1ll11l1l1l1_opy_(
                ref,
                f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᇥ"), datetime.now() - bstack1ll1l1l1_opy_)
            f.bstack1llll111l11_opy_(instance, bstack1ll111lll11_opy_.bstack1ll111llll1_opy_, r.success)
    def bstack1ll11l11lll_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1l11l_opy_(instance, bstack1ll111lll11_opy_.bstack1ll11ll1ll1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1ll1l1l_opy_.session_id(driver)
        hub_url = bstack1lll1ll1l1l_opy_.hub_url(driver)
        bstack1ll1l1l1_opy_ = datetime.now()
        r = self.bstack1ll11l1111l_opy_(
            ref,
            f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᇦ"), datetime.now() - bstack1ll1l1l1_opy_)
        f.bstack1llll111l11_opy_(instance, bstack1ll111lll11_opy_.bstack1ll11ll1ll1_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll111111_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1ll1ll1111l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11l1111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥᇧ") + str(req) + bstack11l1111_opy_ (u"ࠨࠢᇨ"))
        try:
            r = self.bstack1lll1llll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᇩ") + str(r.success) + bstack11l1111_opy_ (u"ࠣࠤᇪ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᇫ") + str(e) + bstack11l1111_opy_ (u"ࠥࠦᇬ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11ll11l1_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1ll11l111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11l1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᇭ") + str(req) + bstack11l1111_opy_ (u"ࠧࠨᇮ"))
        try:
            r = self.bstack1lll1llll1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᇯ") + str(r.success) + bstack11l1111_opy_ (u"ࠢࠣᇰ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᇱ") + str(e) + bstack11l1111_opy_ (u"ࠤࠥᇲ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l1ll11_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1ll11l1l1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11l1111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᇳ") + str(req) + bstack11l1111_opy_ (u"ࠦࠧᇴ"))
        try:
            r = self.bstack1lll1llll1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᇵ") + str(r) + bstack11l1111_opy_ (u"ࠨࠢᇶ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᇷ") + str(e) + bstack11l1111_opy_ (u"ࠣࠤᇸ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11l1llll_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1ll11l1111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11l1111_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦᇹ") + str(req) + bstack11l1111_opy_ (u"ࠥࠦᇺ"))
        try:
            r = self.bstack1lll1llll1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᇻ") + str(r) + bstack11l1111_opy_ (u"ࠧࠨᇼ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇽ") + str(e) + bstack11l1111_opy_ (u"ࠢࠣᇾ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll11l1_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1ll11ll1l1l_opy_(self, instance: bstack1lll1llll11_opy_, url: str, f: bstack1lll1ll1l1l_opy_, kwargs):
        bstack1ll11ll111l_opy_ = version.parse(f.framework_version)
        bstack1ll111ll1ll_opy_ = kwargs.get(bstack11l1111_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᇿ"))
        bstack1ll11ll1l11_opy_ = kwargs.get(bstack11l1111_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤሀ"))
        bstack1ll1l1llll1_opy_ = {}
        bstack1ll11l111ll_opy_ = {}
        bstack1ll111lll1l_opy_ = None
        bstack1ll111ll111_opy_ = {}
        if bstack1ll11ll1l11_opy_ is not None or bstack1ll111ll1ll_opy_ is not None: # check top level caps
            if bstack1ll11ll1l11_opy_ is not None:
                bstack1ll111ll111_opy_[bstack11l1111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪሁ")] = bstack1ll11ll1l11_opy_
            if bstack1ll111ll1ll_opy_ is not None and callable(getattr(bstack1ll111ll1ll_opy_, bstack11l1111_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨሂ"))):
                bstack1ll111ll111_opy_[bstack11l1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨሃ")] = bstack1ll111ll1ll_opy_.to_capabilities()
        response = self.bstack1ll1ll1111l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1ll111ll111_opy_).encode(bstack11l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧሄ")))
        if response is not None and response.capabilities:
            bstack1ll1l1llll1_opy_ = json.loads(response.capabilities.decode(bstack11l1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨህ")))
            if not bstack1ll1l1llll1_opy_: # empty caps bstack1ll1l1lll1l_opy_ bstack1ll1ll11lll_opy_ bstack1ll1ll11111_opy_ bstack1ll1l1ll1l1_opy_ or error in processing
                return
            bstack1ll111lll1l_opy_ = f.bstack1ll11l11l11_opy_[bstack11l1111_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧሆ")](bstack1ll1l1llll1_opy_)
        if bstack1ll111ll1ll_opy_ is not None and bstack1ll11ll111l_opy_ >= version.parse(bstack11l1111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨሇ")):
            bstack1ll11l111ll_opy_ = None
        if (
                not bstack1ll111ll1ll_opy_ and not bstack1ll11ll1l11_opy_
        ) or (
                bstack1ll11ll111l_opy_ < version.parse(bstack11l1111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩለ"))
        ):
            bstack1ll11l111ll_opy_ = {}
            bstack1ll11l111ll_opy_.update(bstack1ll1l1llll1_opy_)
        self.logger.info(bstack1l1111l1l1_opy_)
        if os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢሉ")).lower().__eq__(bstack11l1111_opy_ (u"ࠧࡺࡲࡶࡧࠥሊ")):
            kwargs.update(
                {
                    bstack11l1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤላ"): f.bstack1ll111ll11l_opy_,
                }
            )
        if bstack1ll11ll111l_opy_ >= version.parse(bstack11l1111_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧሌ")):
            if bstack1ll11ll1l11_opy_ is not None:
                del kwargs[bstack11l1111_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣል")]
            kwargs.update(
                {
                    bstack11l1111_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥሎ"): bstack1ll111lll1l_opy_,
                    bstack11l1111_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢሏ"): True,
                    bstack11l1111_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦሐ"): None,
                }
            )
        elif bstack1ll11ll111l_opy_ >= version.parse(bstack11l1111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫሑ")):
            kwargs.update(
                {
                    bstack11l1111_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨሒ"): bstack1ll11l111ll_opy_,
                    bstack11l1111_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣሓ"): bstack1ll111lll1l_opy_,
                    bstack11l1111_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧሔ"): True,
                    bstack11l1111_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤሕ"): None,
                }
            )
        elif bstack1ll11ll111l_opy_ >= version.parse(bstack11l1111_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪሖ")):
            kwargs.update(
                {
                    bstack11l1111_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦሗ"): bstack1ll11l111ll_opy_,
                    bstack11l1111_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤመ"): True,
                    bstack11l1111_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨሙ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l1111_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢሚ"): bstack1ll11l111ll_opy_,
                    bstack11l1111_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧማ"): True,
                    bstack11l1111_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤሜ"): None,
                }
            )