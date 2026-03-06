# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1ll1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111111lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1l11l1l1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from bstack_utils.bstack1ll1111l_opy_ import bstack1llllll1ll_opy_
import browserstack_sdk
class bstack1l1lll1l1ll_opy_(bstack1ll111l1l1l_opy_):
    bstack11llll1l111_opy_ = bstack1111_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨᖵ")
    bstack11llll111l1_opy_ = bstack1111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᖶ")
    bstack11lll1lll11_opy_ = bstack1111_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᖷ")
    def __init__(self, bstack1ll11ll1l11_opy_):
        super().__init__()
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack11llll11lll_opy_)
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l11llll1ll_opy_)
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.POST), self.bstack11llll11111_opy_)
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.POST), self.bstack11lll11lll1_opy_)
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.QUIT, bstack1ll1l1lll1l_opy_.POST), self.bstack11llll111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll11lll_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᖸ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᖹ")), str):
                    url = kwargs.get(bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖺ"))
                elif hasattr(kwargs.get(bstack1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᖻ")), bstack1111_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧᖼ")):
                    url = kwargs.get(bstack1111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖽ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᖾ"))._url
            except Exception as e:
                url = bstack1111_opy_ (u"ࠩࠪᖿ")
                self.logger.error(bstack1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡶࡱࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࢁࡽࠣᗀ").format(e))
            self.logger.info(bstack1111_opy_ (u"ࠦࡗ࡫࡭ࡰࡶࡨࠤࡘ࡫ࡲࡷࡧࡵࠤࡆࡪࡤࡳࡧࡶࡷࠥࡨࡥࡪࡰࡪࠤࡵࡧࡳࡴࡧࡧࠤࡦࡹࠠ࠻ࠢࡾࢁࠧᗁ").format(str(url)))
            bstack11lll1l1ll1_opy_ = None
            driver_rank = None
            try:
                bstack11lll1l1ll1_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11lll1l1ll1_opy_ is not None:
                    bstack11llll11l11_opy_ = str(bstack11lll1l1ll1_opy_)
                    if bstack1111_opy_ (u"ࠧࠩࠢᗂ") in bstack11llll11l11_opy_:
                        bstack11llll1l1l1_opy_ = bstack11llll11l11_opy_.rsplit(bstack1111_opy_ (u"ࠨࠣࠣᗃ"), 1)[1]
                        try:
                            driver_rank = int(bstack11llll1l1l1_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡥࡹࡶࡵࡥࡨࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫ࠡࡨࡵࡳࡲࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻࡦࡺࡳࡰ࡮ࡩࡩࡵࡡ࡯ࡥࡧ࡫࡬ࡾࠩ࠽ࠤࠧᗄ") + str(e) + bstack1111_opy_ (u"ࠣࠤᗅ"))
            except Exception as e:
                self.logger.debug(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬࠻ࠢࠥᗆ") + str(e) + bstack1111_opy_ (u"ࠥࠦᗇ"))
            self.bstack11llll1l1ll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1111_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵࡣࡷࡧ࡮࡬࠿ࡾࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫ࡾࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿ࡫࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᗈ") + str(kwargs) + bstack1111_opy_ (u"ࠧࠨᗉ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11llll1ll_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll1l11111_opy_(instance, bstack1l1lll1l1ll_opy_.bstack11llll1l111_opy_, False):
            return
        if not f.bstack1ll1l1l1ll1_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_):
            return
        platform_index = f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_)
        if f.bstack1l1l1lllll1_opy_(method_name, *args) and len(args) > 1:
            bstack1l1llll111_opy_ = datetime.now()
            hub_url = bstack1ll11l11111_opy_.hub_url(driver)
            self.logger.warning(bstack1111_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᗊ") + str(hub_url) + bstack1111_opy_ (u"ࠢࠣᗋ"))
            bstack11llll1ll11_opy_ = args[1][bstack1111_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᗌ")] if isinstance(args[1], dict) and bstack1111_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᗍ") in args[1] else None
            bstack11lll11ll11_opy_ = bstack1111_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣᗎ")
            if isinstance(bstack11llll1ll11_opy_, dict):
                bstack1l1llll111_opy_ = datetime.now()
                r = self.bstack11lll1ll1l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᗏ"), datetime.now() - bstack1l1llll111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1111_opy_ (u"ࠧࡹ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫࠿ࠦࠢᗐ") + str(r) + bstack1111_opy_ (u"ࠨࠢᗑ"))
                        return
                    if r.hub_url:
                        f.bstack11llll1111l_opy_(instance, driver, r.hub_url)
                        f.bstack1lll1l11l1l_opy_(instance, bstack1l1lll1l1ll_opy_.bstack11llll1l111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᗒ"), e)
    def bstack11llll11111_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll11l11111_opy_.session_id(driver)
            if session_id:
                bstack11lll1lllll_opy_ = bstack1111_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᗓ").format(session_id)
                bstack1l11l1ll_opy_.mark(bstack11lll1lllll_opy_)
    def bstack11lll11lll1_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1l11111_opy_(instance, bstack1l1lll1l1ll_opy_.bstack11llll111l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll11l11111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᗔ") + str(hub_url) + bstack1111_opy_ (u"ࠥࠦᗕ"))
            return
        framework_session_id = bstack1ll11l11111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᗖ") + str(framework_session_id) + bstack1111_opy_ (u"ࠧࠨᗗ"))
            return
        if bstack1ll11l11111_opy_.bstack11lll1ll1ll_opy_(*args) == bstack1ll11l11111_opy_.bstack11lll1ll111_opy_:
            bstack11lll11l1l1_opy_ = bstack1111_opy_ (u"ࠨࡻࡾ࠼ࡨࡲࡩࠨᗘ").format(framework_session_id)
            bstack11lll1lllll_opy_ = bstack1111_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᗙ").format(framework_session_id)
            bstack1l11l1ll_opy_.end(
                label=bstack1111_opy_ (u"ࠣࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠦᗚ"),
                start=bstack11lll1lllll_opy_,
                end=bstack11lll11l1l1_opy_,
                status=True,
                failure=None
            )
            bstack1l1llll111_opy_ = datetime.now()
            r = self.bstack11lll1l111l_opy_(
                ref,
                f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᗛ"), datetime.now() - bstack1l1llll111_opy_)
            f.bstack1lll1l11l1l_opy_(instance, bstack1l1lll1l1ll_opy_.bstack11llll111l1_opy_, r.success)
    def bstack11llll111ll_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1l11111_opy_(instance, bstack1l1lll1l1ll_opy_.bstack11lll1lll11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll11l11111_opy_.session_id(driver)
        hub_url = bstack1ll11l11111_opy_.hub_url(driver)
        bstack1l1llll111_opy_ = datetime.now()
        r = self.bstack11lll1l1l11_opy_(
            ref,
            f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᗜ"), datetime.now() - bstack1l1llll111_opy_)
        f.bstack1lll1l11l1l_opy_(instance, bstack1l1lll1l1ll_opy_.bstack11lll1lll11_opy_, r.success)
    @measure(event_name=EVENTS.bstack11lll1l1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l111111l11_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11llll11l1l_opy_ = int(driver_rank)
                is_secondary_driver = bstack11llll11l1l_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᗝ") + str(req) + bstack1111_opy_ (u"ࠧࠨᗞ"))
        try:
            r = self.bstack1lll111l111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᗟ") + str(r.success) + bstack1111_opy_ (u"ࠢࠣᗠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᗡ") + str(e) + bstack1111_opy_ (u"ࠤࠥᗢ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1l11l1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack11lll1ll1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᗣ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᗤ") + str(req) + bstack1111_opy_ (u"ࠧࠨᗥ"))
        try:
            r = self.bstack1lll111l111_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᗦ") + str(r.success) + bstack1111_opy_ (u"ࠢࠣᗧ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᗨ") + str(e) + bstack1111_opy_ (u"ࠤࠥᗩ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1llll1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack11lll1l111l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᗪ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢᗫ") + str(req) + bstack1111_opy_ (u"ࠧࠨᗬ"))
        try:
            r = self.bstack1lll111l111_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᗭ") + str(r) + bstack1111_opy_ (u"ࠢࠣᗮ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᗯ") + str(e) + bstack1111_opy_ (u"ࠤࠥᗰ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll11l11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack11lll1l1l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᗱ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨᗲ") + str(req) + bstack1111_opy_ (u"ࠧࠨᗳ"))
        try:
            r = self.bstack1lll111l111_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᗴ") + str(r) + bstack1111_opy_ (u"ࠢࠣᗵ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᗶ") + str(e) + bstack1111_opy_ (u"ࠤࠥᗷ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1111_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack11llll1l1ll_opy_(self, instance: bstack1ll1ll1l111_opy_, url: str, f: bstack1ll11l11111_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11lll1lll1l_opy_ = os.environ.get(bstack1111_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫᗸ"))
        if bstack11lll1lll1l_opy_ is not None:
            browserstack_sdk.bstack11l1l11l11_opy_ = bstack11lll1lll1l_opy_.lower() == bstack1111_opy_ (u"ࠫࡹࡸࡵࡦࠩᗹ")
        bstack11lll1l1l1l_opy_ = version.parse(f.framework_version)
        bstack11lll1l1111_opy_ = f.platform_index
        bstack11lll1ll11l_opy_ = kwargs.get(bstack1111_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᗺ"))
        bstack11lll11llll_opy_ = kwargs.get(bstack1111_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᗻ"))
        bstack1lll1111ll1_opy_ = {}
        bstack11llll11ll1_opy_ = {}
        bstack11llll1l11l_opy_ = None
        bstack11lll11ll1l_opy_ = {}
        if bstack11lll11llll_opy_ is not None or bstack11lll1ll11l_opy_ is not None: # check top level caps
            if bstack11lll11llll_opy_ is not None:
                bstack11lll11ll1l_opy_[bstack1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᗼ")] = bstack11lll11llll_opy_
            if bstack11lll1ll11l_opy_ is not None and callable(getattr(bstack11lll1ll11l_opy_, bstack1111_opy_ (u"ࠣࡶࡲࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᗽ"))):
                bstack11lll11ll1l_opy_[bstack1111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࡢࡥࡸࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᗾ")] = bstack11lll1ll11l_opy_.to_capabilities()
        response = self.bstack1l111111l11_opy_(bstack11lll1l1111_opy_, url, instance.ref(), json.dumps(bstack11lll11ll1l_opy_).encode(bstack1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᗿ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᘀ")))
            if browserstack_sdk.bstack11l1l11l11_opy_:
                def bstack11lll11l111_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11lll11l111_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1lll1111ll1_opy_ = bstack11lll11l111_opy_(bstack1lll1111ll1_opy_)
                try:
                    bstack11lll1l1lll_opy_ = None
                    if isinstance(bstack1lll1111ll1_opy_, dict):
                        if bstack1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘁ") in bstack1lll1111ll1_opy_:
                            bstack11lll1l1lll_opy_ = bstack1lll1111ll1_opy_.get(bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘂ"))
                        elif isinstance(bstack1lll1111ll1_opy_.get(bstack1111_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᘃ")), dict):
                            bstack11lll1l1lll_opy_ = bstack1lll1111ll1_opy_[bstack1111_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᘄ")].get(bstack1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᘅ"))
                        if isinstance(bstack11lll1l1lll_opy_, dict) and bstack1111_opy_ (u"ࠪࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩᘆ") in bstack11lll1l1lll_opy_:
                            self.logger.debug(bstack1111_opy_ (u"ࠦࡗ࡫࡭ࡰࡸ࡬ࡲ࡬ࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡴࠦࡨࡶࡤࠥᘇ"))
                            try:
                                bstack11lll1l1lll_opy_.pop(bstack1111_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᘈ"), None)
                            except Exception:
                                pass
                            if bstack1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘉ") in bstack1lll1111ll1_opy_:
                                bstack1lll1111ll1_opy_[bstack1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘊ")] = bstack11lll1l1lll_opy_
                            if isinstance(bstack1lll1111ll1_opy_.get(bstack1111_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᘋ")), dict):
                                bstack1lll1111ll1_opy_[bstack1111_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᘌ")][bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘍ")] = bstack11lll1l1lll_opy_
                except Exception:
                    pass
            if not bstack1lll1111ll1_opy_ and not browserstack_sdk.bstack11l1l11l11_opy_:
                return
            bstack11llll1l11l_opy_ = f.bstack1l1llll111l_opy_[bstack1111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣᘎ")](bstack1lll1111ll1_opy_)
        if bstack11lll1ll11l_opy_ is not None and bstack11lll1l1l1l_opy_ >= version.parse(bstack1111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᘏ")):
            bstack11llll11ll1_opy_ = None
        if (
                not bstack11lll1ll11l_opy_ and not bstack11lll11llll_opy_
        ) or (
                bstack11lll1l1l1l_opy_ < version.parse(bstack1111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᘐ"))
        ):
            bstack11llll11ll1_opy_ = {}
            bstack11llll11ll1_opy_.update(bstack1lll1111ll1_opy_)
        self.logger.info(bstack111111lll_opy_)
        if browserstack_sdk.bstack11l1l11l11_opy_:
            bstack11lll1l11ll_opy_ = bstack11llll1l11l_opy_ if bstack11llll1l11l_opy_ else bstack11lll1ll11l_opy_
            if bstack11lll1l11ll_opy_:
                bstack11l11lll11_opy_ = bstack1llllll1ll_opy_(bstack11lll1l11ll_opy_, bstack1l1l1111ll_opy_=bstack1111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᘑ"))
                if bstack11lll1l11ll_opy_ is bstack11lll1ll11l_opy_ and not bstack11llll1l11l_opy_:
                    bstack11llll1l11l_opy_ = bstack11lll1l11ll_opy_
            kwargs.update({bstack1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᘒ"): bstack1l11l1l1_opy_})
        elif os.environ.get(bstack1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᘓ")).lower().__eq__(bstack1111_opy_ (u"ࠥࡸࡷࡻࡥࠣᘔ")):
            kwargs.update({bstack1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᘕ"): f.bstack11lll11l1ll_opy_})
        if bstack11lll1l1l1l_opy_ >= version.parse(bstack1111_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᘖ")):
            if bstack11lll11llll_opy_ is not None:
                del kwargs[bstack1111_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᘗ")]
            kwargs.update(
                {
                    bstack1111_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᘘ"): bstack11llll1l11l_opy_,
                    bstack1111_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᘙ"): True,
                    bstack1111_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᘚ"): None,
                }
            )
        elif bstack11lll1l1l1l_opy_ >= version.parse(bstack1111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᘛ")):
            kwargs.update(
                {
                    bstack1111_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᘜ"): bstack11llll11ll1_opy_,
                    bstack1111_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᘝ"): bstack11llll1l11l_opy_,
                    bstack1111_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᘞ"): True,
                    bstack1111_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᘟ"): None,
                }
            )
        elif bstack11lll1l1l1l_opy_ >= version.parse(bstack1111_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᘠ")):
            kwargs.update(
                {
                    bstack1111_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᘡ"): bstack11llll11ll1_opy_,
                    bstack1111_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᘢ"): True,
                    bstack1111_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᘣ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᘤ"): bstack11llll11ll1_opy_,
                    bstack1111_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᘥ"): True,
                    bstack1111_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᘦ"): None,
                }
            )