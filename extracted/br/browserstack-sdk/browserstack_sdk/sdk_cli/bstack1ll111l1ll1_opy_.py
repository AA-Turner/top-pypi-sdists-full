# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1l1l11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1l1111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
class bstack1ll1l1111l1_opy_(bstack1lll1l1l1l1_opy_):
    bstack1l1111l111l_opy_ = bstack11lllll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨᑺ")
    bstack1l111l11l11_opy_ = bstack11lllll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᑻ")
    bstack1l1111ll1l1_opy_ = bstack11lllll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᑼ")
    def __init__(self, bstack1ll1l1lll1l_opy_):
        super().__init__()
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1llllll_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11111l111_opy_)
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l1l1l111ll_opy_)
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.POST), self.bstack1l1111l11ll_opy_)
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.POST), self.bstack1l1111lllll_opy_)
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.QUIT, bstack1lll1ll11ll_opy_.POST), self.bstack1l1111lll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11111l111_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lllll_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᑽ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11lllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᑾ")), str):
                    url = kwargs.get(bstack11lllll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᑿ"))
                elif hasattr(kwargs.get(bstack11lllll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᒀ")), bstack11lllll_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧᒁ")):
                    url = kwargs.get(bstack11lllll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᒂ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᒃ"))._url
            except Exception as e:
                url = bstack11lllll_opy_ (u"ࠩࠪᒄ")
                self.logger.error(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡶࡱࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࢁࡽࠣᒅ").format(e))
            self.logger.info(bstack11lllll_opy_ (u"ࠦࡗ࡫࡭ࡰࡶࡨࠤࡘ࡫ࡲࡷࡧࡵࠤࡆࡪࡤࡳࡧࡶࡷࠥࡨࡥࡪࡰࡪࠤࡵࡧࡳࡴࡧࡧࠤࡦࡹࠠ࠻ࠢࡾࢁࠧᒆ").format(str(url)))
            bstack1l1111ll11l_opy_ = None
            driver_rank = None
            try:
                bstack1l1111ll11l_opy_ = BrowserStackHelper.get_driver_label()
                if bstack1l1111ll11l_opy_ is not None:
                    bstack1l111l11l1l_opy_ = str(bstack1l1111ll11l_opy_)
                    if bstack11lllll_opy_ (u"ࠧࠩࠢᒇ") in bstack1l111l11l1l_opy_:
                        bstack1l111111ll1_opy_ = bstack1l111l11l1l_opy_.rsplit(bstack11lllll_opy_ (u"ࠨࠣࠣᒈ"), 1)[1]
                        try:
                            driver_rank = int(bstack1l111111ll1_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡥࡹࡶࡵࡥࡨࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫ࠡࡨࡵࡳࡲࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻࡦࡺࡳࡰ࡮ࡩࡩࡵࡡ࡯ࡥࡧ࡫࡬ࡾࠩ࠽ࠤࠧᒉ") + str(e) + bstack11lllll_opy_ (u"ࠣࠤᒊ"))
            except Exception as e:
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬࠻ࠢࠥᒋ") + str(e) + bstack11lllll_opy_ (u"ࠥࠦᒌ"))
            self.bstack1l1111l1l1l_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack11lllll_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵࡣࡷࡧ࡮࡬࠿ࡾࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫ࡾࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿ࡫࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᒍ") + str(kwargs) + bstack11lllll_opy_ (u"ࠧࠨᒎ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1l1l111ll_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll1l1l111_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_, False):
            return
        if not f.bstack1lll111ll11_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_):
            return
        platform_index = f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_)
        if f.bstack1l1lll1l11l_opy_(method_name, *args) and len(args) > 1:
            bstack1l1111l111_opy_ = datetime.now()
            hub_url = bstack1lll11lllll_opy_.hub_url(driver)
            self.logger.warning(bstack11lllll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᒏ") + str(hub_url) + bstack11lllll_opy_ (u"ࠢࠣᒐ"))
            bstack1l111l111l1_opy_ = args[1][bstack11lllll_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒑ")] if isinstance(args[1], dict) and bstack11lllll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᒒ") in args[1] else None
            bstack1l1111l1l11_opy_ = bstack11lllll_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣᒓ")
            if isinstance(bstack1l111l111l1_opy_, dict):
                bstack1l1111l111_opy_ = datetime.now()
                r = self.bstack1l1111lll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᒔ"), datetime.now() - bstack1l1111l111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11lllll_opy_ (u"ࠧࡹ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫࠿ࠦࠢᒕ") + str(r) + bstack11lllll_opy_ (u"ࠨࠢᒖ"))
                        return
                    if r.hub_url:
                        f.bstack1l111l111ll_opy_(instance, driver, r.hub_url)
                        f.bstack1lll1ll1lll_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11lllll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᒗ"), e)
    def bstack1l1111l11ll_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll11lllll_opy_.session_id(driver)
            if session_id:
                bstack1l11111l1ll_opy_ = bstack11lllll_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᒘ").format(session_id)
                bstack1lll11l1ll_opy_.mark(bstack1l11111l1ll_opy_)
    def bstack1l1111lllll_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1l1l111_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111l11l11_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll11lllll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11lllll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᒙ") + str(hub_url) + bstack11lllll_opy_ (u"ࠥࠦᒚ"))
            return
        framework_session_id = bstack1lll11lllll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᒛ") + str(framework_session_id) + bstack11lllll_opy_ (u"ࠧࠨᒜ"))
            return
        if bstack1lll11lllll_opy_.bstack1l111111l1l_opy_(*args) == bstack1lll11lllll_opy_.bstack1l11111ll11_opy_:
            bstack1l1111l1111_opy_ = bstack11lllll_opy_ (u"ࠨࡻࡾ࠼ࡨࡲࡩࠨᒝ").format(framework_session_id)
            bstack1l11111l1ll_opy_ = bstack11lllll_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᒞ").format(framework_session_id)
            bstack1lll11l1ll_opy_.end(
                label=bstack11lllll_opy_ (u"ࠣࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠦᒟ"),
                start=bstack1l11111l1ll_opy_,
                end=bstack1l1111l1111_opy_,
                status=True,
                failure=None
            )
            bstack1l1111l111_opy_ = datetime.now()
            r = self.bstack1l11111lll1_opy_(
                ref,
                f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᒠ"), datetime.now() - bstack1l1111l111_opy_)
            f.bstack1lll1ll1lll_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111l11l11_opy_, r.success)
    def bstack1l1111lll11_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1l1l111_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l1111ll1l1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll11lllll_opy_.session_id(driver)
        hub_url = bstack1lll11lllll_opy_.hub_url(driver)
        bstack1l1111l111_opy_ = datetime.now()
        r = self.bstack1l1111ll111_opy_(
            ref,
            f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᒡ"), datetime.now() - bstack1l1111l111_opy_)
        f.bstack1lll1ll1lll_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l1111ll1l1_opy_, r.success)
    @measure(event_name=EVENTS.bstack111l11llll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l11l11l11l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack1l1111l1ll1_opy_ = int(driver_rank)
                is_secondary_driver = bstack1l1111l1ll1_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᒢ") + str(req) + bstack11lllll_opy_ (u"ࠧࠨᒣ"))
        try:
            r = self.bstack1ll1l1l1ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᒤ") + str(r.success) + bstack11lllll_opy_ (u"ࠢࠣᒥ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᒦ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥᒧ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111l1111l_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1111lll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒨ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᒩ") + str(req) + bstack11lllll_opy_ (u"ࠧࠨᒪ"))
        try:
            r = self.bstack1ll1l1l1ll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᒫ") + str(r.success) + bstack11lllll_opy_ (u"ࠢࠣᒬ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᒭ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥᒮ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11111llll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l11111lll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒯ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢᒰ") + str(req) + bstack11lllll_opy_ (u"ࠧࠨᒱ"))
        try:
            r = self.bstack1ll1l1l1ll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᒲ") + str(r) + bstack11lllll_opy_ (u"ࠢࠣᒳ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᒴ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥᒵ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111ll1ll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1111ll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒶ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨᒷ") + str(req) + bstack11lllll_opy_ (u"ࠧࠨᒸ"))
        try:
            r = self.bstack1ll1l1l1ll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᒹ") + str(r) + bstack11lllll_opy_ (u"ࠢࠣᒺ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᒻ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥᒼ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11ll1_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1111l1l1l_opy_(self, instance: bstack1lll1l1l11l_opy_, url: str, f: bstack1lll11lllll_opy_, driver_rank: int, kwargs):
        bstack1l1111l1lll_opy_ = version.parse(f.framework_version)
        bstack1l1111l11l1_opy_ = f.platform_index
        bstack1l11111l11l_opy_ = kwargs.get(bstack11lllll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᒽ"))
        bstack1l11111l1l1_opy_ = kwargs.get(bstack11lllll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᒾ"))
        bstack1l111llll1l_opy_ = {}
        bstack1l11111ll1l_opy_ = {}
        bstack1l111111lll_opy_ = None
        bstack1l1111llll1_opy_ = {}
        if bstack1l11111l1l1_opy_ is not None or bstack1l11111l11l_opy_ is not None: # check top level caps
            if bstack1l11111l1l1_opy_ is not None:
                bstack1l1111llll1_opy_[bstack11lllll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᒿ")] = bstack1l11111l1l1_opy_
            if bstack1l11111l11l_opy_ is not None and callable(getattr(bstack1l11111l11l_opy_, bstack11lllll_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᓀ"))):
                bstack1l1111llll1_opy_[bstack11lllll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᓁ")] = bstack1l11111l11l_opy_.to_capabilities()
        response = self.bstack1l11l11l11l_opy_(bstack1l1111l11l1_opy_, url, instance.ref(), json.dumps(bstack1l1111llll1_opy_).encode(bstack11lllll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᓂ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1l111llll1l_opy_ = json.loads(response.capabilities.decode(bstack11lllll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᓃ")))
            if not bstack1l111llll1l_opy_: # empty caps bstack1l11l111111_opy_ bstack1l111lllll1_opy_ bstack1l111lll1l1_opy_ bstack1ll11l111ll_opy_ or error in processing
                return
            bstack1l111111lll_opy_ = f.bstack1ll1l11l1l1_opy_[bstack11lllll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᓄ")](bstack1l111llll1l_opy_)
        if bstack1l11111l11l_opy_ is not None and bstack1l1111l1lll_opy_ >= version.parse(bstack11lllll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᓅ")):
            bstack1l11111ll1l_opy_ = None
        if (
                not bstack1l11111l11l_opy_ and not bstack1l11111l1l1_opy_
        ) or (
                bstack1l1111l1lll_opy_ < version.parse(bstack11lllll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᓆ"))
        ):
            bstack1l11111ll1l_opy_ = {}
            bstack1l11111ll1l_opy_.update(bstack1l111llll1l_opy_)
        self.logger.info(bstack1l1l1111ll_opy_)
        if os.environ.get(bstack11lllll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤᓇ")).lower().__eq__(bstack11lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧᓈ")):
            kwargs.update(
                {
                    bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᓉ"): f.bstack1l111l11111_opy_,
                }
            )
        if bstack1l1111l1lll_opy_ >= version.parse(bstack11lllll_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᓊ")):
            if bstack1l11111l1l1_opy_ is not None:
                del kwargs[bstack11lllll_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᓋ")]
            kwargs.update(
                {
                    bstack11lllll_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᓌ"): bstack1l111111lll_opy_,
                    bstack11lllll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᓍ"): True,
                    bstack11lllll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᓎ"): None,
                }
            )
        elif bstack1l1111l1lll_opy_ >= version.parse(bstack11lllll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᓏ")):
            kwargs.update(
                {
                    bstack11lllll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᓐ"): bstack1l11111ll1l_opy_,
                    bstack11lllll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᓑ"): bstack1l111111lll_opy_,
                    bstack11lllll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᓒ"): True,
                    bstack11lllll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᓓ"): None,
                }
            )
        elif bstack1l1111l1lll_opy_ >= version.parse(bstack11lllll_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᓔ")):
            kwargs.update(
                {
                    bstack11lllll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᓕ"): bstack1l11111ll1l_opy_,
                    bstack11lllll_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᓖ"): True,
                    bstack11lllll_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᓗ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11lllll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᓘ"): bstack1l11111ll1l_opy_,
                    bstack11lllll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᓙ"): True,
                    bstack11lllll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᓚ"): None,
                }
            )