# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1l1l11ll1l_opy_,
    bstack1ll1llll1l_opy_,
    bstack1l1ll1lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11l1l1_opy_ import bstack1l11l1ll1l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1lll1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1ll1ll11_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111_opy_
import browserstack_sdk
class bstack1l11ll11ll1_opy_(bstack1l11ll1l11l_opy_):
    bstack11l11llll1l_opy_ = bstack1l111l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨ᠖")
    bstack11l11lll11l_opy_ = bstack1l111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣ᠗")
    bstack11l1l11ll1l_opy_ = bstack1l111l_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣ᠘")
    def __init__(self, bstack1l1lllll11l_opy_):
        super().__init__()
        bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1ll1ll1lll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l11ll11ll_opy_)
        bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11llll1l111_opy_)
        bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.POST), self.bstack11l1l11ll11_opy_)
        bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.POST), self.bstack11l1l1111l1_opy_)
        bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.QUIT, bstack1ll1llll1l_opy_.POST), self.bstack11l1l11111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11ll11ll_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l111l_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦ᠙"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᠚")), str):
                    url = kwargs.get(bstack1l111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ᠛"))
                elif hasattr(kwargs.get(bstack1l111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᠜")), bstack1l111l_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧ᠝")):
                    url = kwargs.get(bstack1l111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ᠞"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᠟"))._url
            except Exception as e:
                url = bstack1l111l_opy_ (u"ࠩࠪᠠ")
                self.logger.error(bstack1l111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡶࡱࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࢁࡽࠣᠡ").format(e))
            self.logger.info(bstack1l111l_opy_ (u"ࠦࡗ࡫࡭ࡰࡶࡨࠤࡘ࡫ࡲࡷࡧࡵࠤࡆࡪࡤࡳࡧࡶࡷࠥࡨࡥࡪࡰࡪࠤࡵࡧࡳࡴࡧࡧࠤࡦࡹࠠ࠻ࠢࡾࢁࠧᠢ").format(str(url)))
            bstack11l11ll1l11_opy_ = None
            driver_rank = None
            try:
                bstack11l11ll1l11_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11l11ll1l11_opy_ is not None:
                    bstack11l11ll1lll_opy_ = str(bstack11l11ll1l11_opy_)
                    if bstack1l111l_opy_ (u"ࠧࠩࠢᠣ") in bstack11l11ll1lll_opy_:
                        bstack11l1l1l11ll_opy_ = bstack11l11ll1lll_opy_.rsplit(bstack1l111l_opy_ (u"ࠨࠣࠣᠤ"), 1)[1]
                        try:
                            driver_rank = int(bstack11l1l1l11ll_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡥࡹࡶࡵࡥࡨࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫ࠡࡨࡵࡳࡲࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻࡦࡺࡳࡰ࡮ࡩࡩࡵࡡ࡯ࡥࡧ࡫࡬ࡾࠩ࠽ࠤࠧᠥ") + str(e) + bstack1l111l_opy_ (u"ࠣࠤᠦ"))
            except Exception as e:
                self.logger.debug(bstack1l111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬࠻ࠢࠥᠧ") + str(e) + bstack1l111l_opy_ (u"ࠥࠦᠨ"))
            self.bstack11l1l1l11l1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1l111l_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵࡣࡷࡧ࡮࡬࠿ࡾࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫ࡾࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿ࡫࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᠩ") + str(kwargs) + bstack1l111l_opy_ (u"ࠧࠨᠪ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11llll1l111_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll111111ll_opy_(instance, bstack1l11ll11ll1_opy_.bstack11l11llll1l_opy_, False):
            return
        if not f.bstack1l1lll1l1l1_opy_(instance, bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_):
            return
        platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_)
        if f.bstack1l111l111l1_opy_(method_name, *args) and len(args) > 1:
            bstack1ll111l111_opy_ = datetime.now()
            hub_url = bstack1l11l1ll1l1_opy_.hub_url(driver)
            self.logger.warning(bstack1l111l_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᠫ") + str(hub_url) + bstack1l111l_opy_ (u"ࠢࠣᠬ"))
            bstack11l11ll11l1_opy_ = args[1][bstack1l111l_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᠭ")] if isinstance(args[1], dict) and bstack1l111l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᠮ") in args[1] else None
            bstack11l11ll1111_opy_ = bstack1l111l_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣᠯ")
            if isinstance(bstack11l11ll11l1_opy_, dict):
                bstack1ll111l111_opy_ = datetime.now()
                r = self.bstack11l1l111l1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᠰ"), datetime.now() - bstack1ll111l111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l111l_opy_ (u"ࠧࡹ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫࠿ࠦࠢᠱ") + str(r) + bstack1l111l_opy_ (u"ࠨࠢᠲ"))
                        return
                    if r.hub_url:
                        f.bstack11l11lll111_opy_(instance, driver, r.hub_url)
                        f.bstack11111ll11l_opy_(instance, bstack1l11ll11ll1_opy_.bstack11l11llll1l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᠳ"), e)
    def bstack11l1l11ll11_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l11l1ll1l1_opy_.session_id(driver)
            if session_id:
                bstack11l11lllll1_opy_ = bstack1l111l_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥᠴ").format(session_id)
                bstack111ll11l1_opy_.mark(bstack11l11lllll1_opy_)
    def bstack11l1l1111l1_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll111111ll_opy_(instance, bstack1l11ll11ll1_opy_.bstack11l11lll11l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l11l1ll1l1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᠵ") + str(hub_url) + bstack1l111l_opy_ (u"ࠥࠦᠶ"))
            return
        framework_session_id = bstack1l11l1ll1l1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢᠷ") + str(framework_session_id) + bstack1l111l_opy_ (u"ࠧࠨᠸ"))
            return
        if bstack1l11l1ll1l1_opy_.bstack11l1l1l1111_opy_(*args) == bstack1l11l1ll1l1_opy_.bstack11l11llllll_opy_:
            bstack11l11ll1l1l_opy_ = bstack1l111l_opy_ (u"ࠨࡻࡾ࠼ࡨࡲࡩࠨᠹ").format(framework_session_id)
            bstack11l11lllll1_opy_ = bstack1l111l_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᠺ").format(framework_session_id)
            bstack111ll11l1_opy_.end(
                label=bstack1l111l_opy_ (u"ࠣࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠦᠻ"),
                start=bstack11l11lllll1_opy_,
                end=bstack11l11ll1l1l_opy_,
                status=True,
                failure=None
            )
            bstack1ll111l111_opy_ = datetime.now()
            r = self.bstack11l1l11l11l_opy_(
                ref,
                f.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᠼ"), datetime.now() - bstack1ll111l111_opy_)
            f.bstack11111ll11l_opy_(instance, bstack1l11ll11ll1_opy_.bstack11l11lll11l_opy_, r.success)
    def bstack11l1l11111l_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll111111ll_opy_(instance, bstack1l11ll11ll1_opy_.bstack11l1l11ll1l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l11l1ll1l1_opy_.session_id(driver)
        hub_url = bstack1l11l1ll1l1_opy_.hub_url(driver)
        bstack1ll111l111_opy_ = datetime.now()
        r = self.bstack11l11ll1ll1_opy_(
            ref,
            f.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᠽ"), datetime.now() - bstack1ll111l111_opy_)
        f.bstack11111ll11l_opy_(instance, bstack1l11ll11ll1_opy_.bstack11l1l11ll1l_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1lll1ll1_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11l1lll111l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11l1l11lll1_opy_ = int(driver_rank)
                is_secondary_driver = bstack11l1l11lll1_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l111l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᠾ") + str(req) + bstack1l111l_opy_ (u"ࠧࠨᠿ"))
        try:
            r = self.bstack1l1l1111l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᡀ") + str(r.success) + bstack1l111l_opy_ (u"ࠢࠣᡁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᡂ") + str(e) + bstack1l111l_opy_ (u"ࠤࠥᡃ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l111ll1_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11l1l111l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1111llll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᡄ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l111l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᡅ") + str(req) + bstack1l111l_opy_ (u"ࠧࠨᡆ"))
        try:
            r = self.bstack1l1l1111l1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᡇ") + str(r.success) + bstack1l111l_opy_ (u"ࠢࠣᡈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᡉ") + str(e) + bstack1l111l_opy_ (u"ࠤࠥᡊ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l111111_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11l1l11l11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1111llll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᡋ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l111l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢᡌ") + str(req) + bstack1l111l_opy_ (u"ࠧࠨᡍ"))
        try:
            r = self.bstack1l1l1111l1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᡎ") + str(r) + bstack1l111l_opy_ (u"ࠢࠣᡏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᡐ") + str(e) + bstack1l111l_opy_ (u"ࠤࠥᡑ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11ll111l_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11l11ll1ll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1111llll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᡒ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l111l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨᡓ") + str(req) + bstack1l111l_opy_ (u"ࠧࠨᡔ"))
        try:
            r = self.bstack1l1l1111l1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᡕ") + str(r) + bstack1l111l_opy_ (u"ࠢࠣᡖ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᡗ") + str(e) + bstack1l111l_opy_ (u"ࠤࠥᡘ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1ll11l_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11l1l1l11l1_opy_(self, instance: bstack1l1ll1lllll_opy_, url: str, f: bstack1l11l1ll1l1_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11l11lll1l1_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫᡙ"))
        if bstack11l11lll1l1_opy_ is not None:
            browserstack_sdk.bstack1llll11l1l_opy_ = bstack11l11lll1l1_opy_.lower() == bstack1l111l_opy_ (u"ࠫࡹࡸࡵࡦࠩᡚ")
        bstack11l1l11llll_opy_ = version.parse(f.framework_version)
        bstack11l1l1l1l11_opy_ = f.platform_index
        bstack11l1l11l111_opy_ = kwargs.get(bstack1l111l_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᡛ"))
        bstack11l1l11l1l1_opy_ = kwargs.get(bstack1l111l_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᡜ"))
        bstack11l111111_opy_ = {}
        bstack11l1l11l1ll_opy_ = {}
        bstack11l11llll11_opy_ = None
        bstack11l11lll1ll_opy_ = {}
        if bstack11l1l11l1l1_opy_ is not None or bstack11l1l11l111_opy_ is not None: # check top level caps
            if bstack11l1l11l1l1_opy_ is not None:
                bstack11l11lll1ll_opy_[bstack1l111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡝ")] = bstack11l1l11l1l1_opy_
            if bstack11l1l11l111_opy_ is not None and callable(getattr(bstack11l1l11l111_opy_, bstack1l111l_opy_ (u"ࠣࡶࡲࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᡞ"))):
                bstack11l11lll1ll_opy_[bstack1l111l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࡢࡥࡸࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᡟ")] = bstack11l1l11l111_opy_.to_capabilities()
        response = self.bstack11l1lll111l_opy_(bstack11l1l1l1l11_opy_, url, instance.ref(), json.dumps(bstack11l11lll1ll_opy_).encode(bstack1l111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᡠ")), driver_rank)
        if response is not None and response.capabilities:
            bstack11l111111_opy_ = json.loads(response.capabilities.decode(bstack1l111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᡡ")))
            if browserstack_sdk.bstack1llll11l1l_opy_:
                def bstack11l1l1111ll_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l1l1111ll_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack11l111111_opy_ = bstack11l1l1111ll_opy_(bstack11l111111_opy_)
                try:
                    bstack11l1l111l11_opy_ = None
                    if isinstance(bstack11l111111_opy_, dict):
                        if bstack1l111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡢ") in bstack11l111111_opy_:
                            bstack11l1l111l11_opy_ = bstack11l111111_opy_.get(bstack1l111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᡣ"))
                        elif isinstance(bstack11l111111_opy_.get(bstack1l111l_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᡤ")), dict):
                            bstack11l1l111l11_opy_ = bstack11l111111_opy_[bstack1l111l_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᡥ")].get(bstack1l111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᡦ"))
                        if isinstance(bstack11l1l111l11_opy_, dict) and bstack1l111l_opy_ (u"ࠪࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩᡧ") in bstack11l1l111l11_opy_:
                            self.logger.debug(bstack1l111l_opy_ (u"ࠦࡗ࡫࡭ࡰࡸ࡬ࡲ࡬ࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡴࠦࡨࡶࡤࠥᡨ"))
                            try:
                                bstack11l1l111l11_opy_.pop(bstack1l111l_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᡩ"), None)
                            except Exception:
                                pass
                            if bstack1l111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᡪ") in bstack11l111111_opy_:
                                bstack11l111111_opy_[bstack1l111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᡫ")] = bstack11l1l111l11_opy_
                            if isinstance(bstack11l111111_opy_.get(bstack1l111l_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᡬ")), dict):
                                bstack11l111111_opy_[bstack1l111l_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᡭ")][bstack1l111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᡮ")] = bstack11l1l111l11_opy_
                except Exception:
                    pass
            if not bstack11l111111_opy_ and not browserstack_sdk.bstack1llll11l1l_opy_:
                return
            bstack11l11llll11_opy_ = f.bstack1l1l1lll1l1_opy_[bstack1l111l_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣᡯ")](bstack11l111111_opy_)
        if bstack11l1l11l111_opy_ is not None and bstack11l1l11llll_opy_ >= version.parse(bstack1l111l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᡰ")):
            bstack11l1l11l1ll_opy_ = None
        if (
                not bstack11l1l11l111_opy_ and not bstack11l1l11l1l1_opy_
        ) or (
                bstack11l1l11llll_opy_ < version.parse(bstack1l111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᡱ"))
        ):
            bstack11l1l11l1ll_opy_ = {}
            bstack11l1l11l1ll_opy_.update(bstack11l111111_opy_)
        self.logger.info(bstack1lll1lll_opy_)
        if browserstack_sdk.bstack1llll11l1l_opy_:
            bstack11l1l111lll_opy_ = bstack11l11llll11_opy_ if bstack11l11llll11_opy_ else bstack11l1l11l111_opy_
            if bstack11l1l111lll_opy_:
                bstack111111ll1_opy_ = bstack11ll1111_opy_(bstack11l1l111lll_opy_, bstack1l11lll1l1_opy_=bstack1l111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᡲ"))
                if bstack11l1l111lll_opy_ is bstack11l1l11l111_opy_ and not bstack11l11llll11_opy_:
                    bstack11l11llll11_opy_ = bstack11l1l111lll_opy_
            kwargs.update({bstack1l111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᡳ"): bstack1ll1ll11_opy_})
        elif os.environ.get(bstack1l111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᡴ")).lower().__eq__(bstack1l111l_opy_ (u"ࠥࡸࡷࡻࡥࠣᡵ")):
            kwargs.update({bstack1l111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᡶ"): f.bstack11l1l1l111l_opy_})
        if bstack11l1l11llll_opy_ >= version.parse(bstack1l111l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᡷ")):
            if bstack11l1l11l1l1_opy_ is not None:
                del kwargs[bstack1l111l_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᡸ")]
            kwargs.update(
                {
                    bstack1l111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣ᡹"): bstack11l11llll11_opy_,
                    bstack1l111l_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧ᡺"): True,
                    bstack1l111l_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤ᡻"): None,
                }
            )
        elif bstack11l1l11llll_opy_ >= version.parse(bstack1l111l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ᡼")):
            kwargs.update(
                {
                    bstack1l111l_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᡽"): bstack11l1l11l1ll_opy_,
                    bstack1l111l_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨ᡾"): bstack11l11llll11_opy_,
                    bstack1l111l_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥ᡿"): True,
                    bstack1l111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᢀ"): None,
                }
            )
        elif bstack11l1l11llll_opy_ >= version.parse(bstack1l111l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᢁ")):
            kwargs.update(
                {
                    bstack1l111l_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᢂ"): bstack11l1l11l1ll_opy_,
                    bstack1l111l_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᢃ"): True,
                    bstack1l111l_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᢄ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l111l_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᢅ"): bstack11l1l11l1ll_opy_,
                    bstack1l111l_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᢆ"): True,
                    bstack1l111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᢇ"): None,
                }
            )