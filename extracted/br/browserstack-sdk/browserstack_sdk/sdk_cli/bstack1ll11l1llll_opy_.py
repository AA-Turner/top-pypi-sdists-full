# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1llll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll11l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack11ll1llll1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11llll1ll1_opy_
import browserstack_sdk
class bstack1ll111111l1_opy_(bstack1ll11l1ll11_opy_):
    bstack11lll1l1lll_opy_ = bstack1lll1l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᖴ")
    bstack11lll1ll1l1_opy_ = bstack1lll1l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᖵ")
    bstack11llll11lll_opy_ = bstack1lll1l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᖶ")
    def __init__(self, bstack1ll1111llll_opy_):
        super().__init__()
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_, bstack1ll1llll111_opy_.PRE), self.bstack11lll1l11l1_opy_)
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l11llll1l1_opy_)
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.POST), self.bstack11lll1ll111_opy_)
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.POST), self.bstack11lll1ll1ll_opy_)
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.QUIT, bstack1ll1llll111_opy_.POST), self.bstack11llll1l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1l11l1_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1lll1l_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᖷ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1lll1l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᖸ")), str):
                    url = kwargs.get(bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᖹ"))
                elif hasattr(kwargs.get(bstack1lll1l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᖺ")), bstack1lll1l_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᖻ")):
                    url = kwargs.get(bstack1lll1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᖼ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᖽ"))._url
            except Exception as e:
                url = bstack1lll1l_opy_ (u"ࠨࠩᖾ")
                self.logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᖿ").format(e))
            self.logger.info(bstack1lll1l_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᗀ").format(str(url)))
            bstack11llll1lll1_opy_ = None
            driver_rank = None
            try:
                bstack11llll1lll1_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11llll1lll1_opy_ is not None:
                    bstack11lll11lll1_opy_ = str(bstack11llll1lll1_opy_)
                    if bstack1lll1l_opy_ (u"ࠦࠨࠨᗁ") in bstack11lll11lll1_opy_:
                        bstack11llll111ll_opy_ = bstack11lll11lll1_opy_.rsplit(bstack1lll1l_opy_ (u"ࠧࠩࠢᗂ"), 1)[1]
                        try:
                            driver_rank = int(bstack11llll111ll_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡫ࡸࡵࡴࡤࡧࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱࠠࡧࡴࡲࡱࠥࡲࡡࡣࡧ࡯ࠤࠬࢁࡥࡹࡲ࡯࡭ࡨ࡯ࡴࡠ࡮ࡤࡦࡪࡲࡽࠨ࠼ࠣࠦᗃ") + str(e) + bstack1lll1l_opy_ (u"ࠢࠣᗄ"))
            except Exception as e:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲ࠺ࠡࠤᗅ") + str(e) + bstack1lll1l_opy_ (u"ࠤࠥᗆ"))
            self.bstack11llll1l111_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1lll1l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫࠾ࡽࡧࡶ࡮ࡼࡥࡳࡡࡵࡥࡳࡱࡽࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡪ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᗇ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠦࠧᗈ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11llll1l1_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll111l1l1_opy_(instance, bstack1ll111111l1_opy_.bstack11lll1l1lll_opy_, False):
            return
        if not f.bstack1ll1l1l1l1l_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_):
            return
        platform_index = f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_)
        if f.bstack1l1l1ll1l11_opy_(method_name, *args) and len(args) > 1:
            bstack1l1l11ll1_opy_ = datetime.now()
            hub_url = bstack1ll11l11l11_opy_.hub_url(driver)
            self.logger.warning(bstack1lll1l_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᗉ") + str(hub_url) + bstack1lll1l_opy_ (u"ࠨࠢᗊ"))
            bstack11lll1l1ll1_opy_ = args[1][bstack1lll1l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᗋ")] if isinstance(args[1], dict) and bstack1lll1l_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᗌ") in args[1] else None
            bstack11lll1l1l1l_opy_ = bstack1lll1l_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᗍ")
            if isinstance(bstack11lll1l1ll1_opy_, dict):
                bstack1l1l11ll1_opy_ = datetime.now()
                r = self.bstack11llll1ll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᗎ"), datetime.now() - bstack1l1l11ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1lll1l_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᗏ") + str(r) + bstack1lll1l_opy_ (u"ࠧࠨᗐ"))
                        return
                    if r.hub_url:
                        f.bstack11lll1l1111_opy_(instance, driver, r.hub_url)
                        f.bstack1lll1l11lll_opy_(instance, bstack1ll111111l1_opy_.bstack11lll1l1lll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1lll1l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᗑ"), e)
    def bstack11lll1ll111_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll11l11l11_opy_.session_id(driver)
            if session_id:
                bstack11llll111l1_opy_ = bstack1lll1l_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᗒ").format(session_id)
                bstack1l11l11ll1_opy_.mark(bstack11llll111l1_opy_)
    def bstack11lll1ll1ll_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll111l1l1_opy_(instance, bstack1ll111111l1_opy_.bstack11lll1ll1l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll11l11l11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᗓ") + str(hub_url) + bstack1lll1l_opy_ (u"ࠤࠥᗔ"))
            return
        framework_session_id = bstack1ll11l11l11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᗕ") + str(framework_session_id) + bstack1lll1l_opy_ (u"ࠦࠧᗖ"))
            return
        if bstack1ll11l11l11_opy_.bstack11lll1lll11_opy_(*args) == bstack1ll11l11l11_opy_.bstack11llll1l11l_opy_:
            bstack11lll11ll1l_opy_ = bstack1lll1l_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᗗ").format(framework_session_id)
            bstack11llll111l1_opy_ = bstack1lll1l_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᗘ").format(framework_session_id)
            bstack1l11l11ll1_opy_.end(
                label=bstack1lll1l_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᗙ"),
                start=bstack11llll111l1_opy_,
                end=bstack11lll11ll1l_opy_,
                status=True,
                failure=None
            )
            bstack1l1l11ll1_opy_ = datetime.now()
            r = self.bstack11llll11ll1_opy_(
                ref,
                f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᗚ"), datetime.now() - bstack1l1l11ll1_opy_)
            f.bstack1lll1l11lll_opy_(instance, bstack1ll111111l1_opy_.bstack11lll1ll1l1_opy_, r.success)
    def bstack11llll1l1l1_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll111l1l1_opy_(instance, bstack1ll111111l1_opy_.bstack11llll11lll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll11l11l11_opy_.session_id(driver)
        hub_url = bstack1ll11l11l11_opy_.hub_url(driver)
        bstack1l1l11ll1_opy_ = datetime.now()
        r = self.bstack11lll11l1ll_opy_(
            ref,
            f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᗛ"), datetime.now() - bstack1l1l11ll1_opy_)
        f.bstack1lll1l11lll_opy_(instance, bstack1ll111111l1_opy_.bstack11llll11lll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll1lll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l11111ll11_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11lll1llll1_opy_ = int(driver_rank)
                is_secondary_driver = bstack11lll1llll1_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᗜ") + str(req) + bstack1lll1l_opy_ (u"ࠦࠧᗝ"))
        try:
            r = self.bstack1lll111lll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᗞ") + str(r.success) + bstack1lll1l_opy_ (u"ࠨࠢᗟ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᗠ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᗡ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1l11ll_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack11llll1ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᗢ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᗣ") + str(req) + bstack1lll1l_opy_ (u"ࠦࠧᗤ"))
        try:
            r = self.bstack1lll111lll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᗥ") + str(r.success) + bstack1lll1l_opy_ (u"ࠨࠢᗦ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᗧ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᗨ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1ll11_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack11llll11ll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᗩ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᗪ") + str(req) + bstack1lll1l_opy_ (u"ࠦࠧᗫ"))
        try:
            r = self.bstack1lll111lll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᗬ") + str(r) + bstack1lll1l_opy_ (u"ࠨࠢᗭ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᗮ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᗯ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll11l1l1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack11lll11l1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᗰ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᗱ") + str(req) + bstack1lll1l_opy_ (u"ࠦࠧᗲ"))
        try:
            r = self.bstack1lll111lll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᗳ") + str(r) + bstack1lll1l_opy_ (u"ࠨࠢᗴ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᗵ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᗶ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l111l1l1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack11llll1l111_opy_(self, instance: bstack1ll1llll11l_opy_, url: str, f: bstack1ll11l11l11_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11lll11llll_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪᗷ"))
        if bstack11lll11llll_opy_ is not None:
            browserstack_sdk.bstack1l11l1l1l1_opy_ = bstack11lll11llll_opy_.lower() == bstack1lll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᗸ")
        bstack11lll1l1l11_opy_ = version.parse(f.framework_version)
        bstack11llll1l1ll_opy_ = f.platform_index
        bstack11lll1lll1l_opy_ = kwargs.get(bstack1lll1l_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᗹ"))
        bstack11lll1l111l_opy_ = kwargs.get(bstack1lll1l_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᗺ"))
        bstack1lll11l1ll1_opy_ = {}
        bstack11llll11111_opy_ = {}
        bstack11llll1111l_opy_ = None
        bstack11llll11l1l_opy_ = {}
        if bstack11lll1l111l_opy_ is not None or bstack11lll1lll1l_opy_ is not None: # check top level caps
            if bstack11lll1l111l_opy_ is not None:
                bstack11llll11l1l_opy_[bstack1lll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᗻ")] = bstack11lll1l111l_opy_
            if bstack11lll1lll1l_opy_ is not None and callable(getattr(bstack11lll1lll1l_opy_, bstack1lll1l_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᗼ"))):
                bstack11llll11l1l_opy_[bstack1lll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᗽ")] = bstack11lll1lll1l_opy_.to_capabilities()
        response = self.bstack1l11111ll11_opy_(bstack11llll1l1ll_opy_, url, instance.ref(), json.dumps(bstack11llll11l1l_opy_).encode(bstack1lll1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᗾ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1lll11l1ll1_opy_ = json.loads(response.capabilities.decode(bstack1lll1l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᗿ")))
            if browserstack_sdk.bstack1l11l1l1l1_opy_:
                def bstack11llll11l11_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11llll11l11_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1lll11l1ll1_opy_ = bstack11llll11l11_opy_(bstack1lll11l1ll1_opy_)
                try:
                    bstack11lll11ll11_opy_ = None
                    if isinstance(bstack1lll11l1ll1_opy_, dict):
                        if bstack1lll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘀ") in bstack1lll11l1ll1_opy_:
                            bstack11lll11ll11_opy_ = bstack1lll11l1ll1_opy_.get(bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘁ"))
                        elif isinstance(bstack1lll11l1ll1_opy_.get(bstack1lll1l_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᘂ")), dict):
                            bstack11lll11ll11_opy_ = bstack1lll11l1ll1_opy_[bstack1lll1l_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᘃ")].get(bstack1lll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘄ"))
                        if isinstance(bstack11lll11ll11_opy_, dict) and bstack1lll1l_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨᘅ") in bstack11lll11ll11_opy_:
                            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡖࡪࡳ࡯ࡷ࡫ࡱ࡫ࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡫ࡸ࡯࡮ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡤࡨࡪࡴࡸࡥࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡳࠥ࡮ࡵࡣࠤᘆ"))
                            try:
                                bstack11lll11ll11_opy_.pop(bstack1lll1l_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪᘇ"), None)
                            except Exception:
                                pass
                            if bstack1lll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘈ") in bstack1lll11l1ll1_opy_:
                                bstack1lll11l1ll1_opy_[bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘉ")] = bstack11lll11ll11_opy_
                            if isinstance(bstack1lll11l1ll1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᘊ")), dict):
                                bstack1lll11l1ll1_opy_[bstack1lll1l_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᘋ")][bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᘌ")] = bstack11lll11ll11_opy_
                except Exception:
                    pass
            if not bstack1lll11l1ll1_opy_ and not browserstack_sdk.bstack1l11l1l1l1_opy_:
                return
            bstack11llll1111l_opy_ = f.bstack1ll111l1ll1_opy_[bstack1lll1l_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᘍ")](bstack1lll11l1ll1_opy_)
        if bstack11lll1lll1l_opy_ is not None and bstack11lll1l1l11_opy_ >= version.parse(bstack1lll1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᘎ")):
            bstack11llll11111_opy_ = None
        if (
                not bstack11lll1lll1l_opy_ and not bstack11lll1l111l_opy_
        ) or (
                bstack11lll1l1l11_opy_ < version.parse(bstack1lll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᘏ"))
        ):
            bstack11llll11111_opy_ = {}
            bstack11llll11111_opy_.update(bstack1lll11l1ll1_opy_)
        self.logger.info(bstack1ll11l1l1_opy_)
        if browserstack_sdk.bstack1l11l1l1l1_opy_:
            bstack11lll1ll11l_opy_ = bstack11llll1111l_opy_ if bstack11llll1111l_opy_ else bstack11lll1lll1l_opy_
            if bstack11lll1ll11l_opy_:
                bstack11lll1l11_opy_ = bstack11llll1ll1_opy_(bstack11lll1ll11l_opy_, bstack111l11l1ll_opy_=bstack1lll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᘐ"))
                if bstack11lll1ll11l_opy_ is bstack11lll1lll1l_opy_ and not bstack11llll1111l_opy_:
                    bstack11llll1111l_opy_ = bstack11lll1ll11l_opy_
            kwargs.update({bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᘑ"): bstack11ll1llll1_opy_})
        elif os.environ.get(bstack1lll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦᘒ")).lower().__eq__(bstack1lll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᘓ")):
            kwargs.update({bstack1lll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᘔ"): f.bstack11lll1lllll_opy_})
        if bstack11lll1l1l11_opy_ >= version.parse(bstack1lll1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᘕ")):
            if bstack11lll1l111l_opy_ is not None:
                del kwargs[bstack1lll1l_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᘖ")]
            kwargs.update(
                {
                    bstack1lll1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᘗ"): bstack11llll1111l_opy_,
                    bstack1lll1l_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᘘ"): True,
                    bstack1lll1l_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᘙ"): None,
                }
            )
        elif bstack11lll1l1l11_opy_ >= version.parse(bstack1lll1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᘚ")):
            kwargs.update(
                {
                    bstack1lll1l_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᘛ"): bstack11llll11111_opy_,
                    bstack1lll1l_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᘜ"): bstack11llll1111l_opy_,
                    bstack1lll1l_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᘝ"): True,
                    bstack1lll1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᘞ"): None,
                }
            )
        elif bstack11lll1l1l11_opy_ >= version.parse(bstack1lll1l_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᘟ")):
            kwargs.update(
                {
                    bstack1lll1l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᘠ"): bstack11llll11111_opy_,
                    bstack1lll1l_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᘡ"): True,
                    bstack1lll1l_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᘢ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1lll1l_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᘣ"): bstack11llll11111_opy_,
                    bstack1lll1l_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᘤ"): True,
                    bstack1lll1l_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᘥ"): None,
                }
            )