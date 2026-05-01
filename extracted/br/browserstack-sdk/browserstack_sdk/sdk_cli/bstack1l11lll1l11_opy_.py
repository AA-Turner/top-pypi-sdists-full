# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack1l1ll111lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l111lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack11l1111l1l_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from bstack_utils.bstack111111ll1_opy_ import bstack1l1l1l1ll_opy_
import browserstack_sdk
class bstack1l11l11ll1l_opy_(bstack1l11l1l11ll_opy_):
    bstack11l11ll1111_opy_ = bstack111ll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᠧ")
    bstack11l1l111lll_opy_ = bstack111ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᠨ")
    bstack11l11ll1l11_opy_ = bstack111ll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᠩ")
    def __init__(self, bstack1l1llll11l1_opy_):
        super().__init__()
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11l11lll111_opy_)
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11llll11l1l_opy_)
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.POST), self.bstack11l11ll11l1_opy_)
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.POST), self.bstack11l1l1111ll_opy_)
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.QUIT, bstack1l1l111lll_opy_.POST), self.bstack11l11ll11ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11lll111_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack111ll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᠪ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack111ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᠫ")), str):
                    url = kwargs.get(bstack111ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᠬ"))
                elif hasattr(kwargs.get(bstack111ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᠭ")), bstack111ll_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪᠮ")):
                    url = kwargs.get(bstack111ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᠯ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack111ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᠰ"))._url
            except Exception as e:
                url = bstack111ll_opy_ (u"ࠬ࠭ᠱ")
                self.logger.error(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦᠲ").format(e))
            self.logger.info(bstack111ll_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣᠳ").format(str(url)))
            bstack11l11l1ll11_opy_ = None
            driver_rank = None
            try:
                bstack11l11l1ll11_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11l11l1ll11_opy_ is not None:
                    bstack11l11l1llll_opy_ = str(bstack11l11l1ll11_opy_)
                    if bstack111ll_opy_ (u"ࠣࠥࠥᠴ") in bstack11l11l1llll_opy_:
                        bstack11l1l11l1ll_opy_ = bstack11l11l1llll_opy_.rsplit(bstack111ll_opy_ (u"ࠤࠦࠦᠵ"), 1)[1]
                        try:
                            driver_rank = int(bstack11l1l11l1ll_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡨࡼࡹࡸࡡࡤࡶ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮ࠤ࡫ࡸ࡯࡮ࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡩࡽࡶ࡬ࡪࡥ࡬ࡸࡤࡲࡡࡣࡧ࡯ࢁࠬࡀࠠࠣᠶ") + str(e) + bstack111ll_opy_ (u"ࠦࠧᠷ"))
            except Exception as e:
                self.logger.debug(bstack111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯࠾ࠥࠨᠸ") + str(e) + bstack111ll_opy_ (u"ࠨࠢᠹ"))
            self.bstack11l1l11ll11_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack111ll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡳࡣࡱ࡯ࡂࢁࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࢁࠥࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡧ࠰ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᠺ") + str(kwargs) + bstack111ll_opy_ (u"ࠣࠤᠻ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11llll11l1l_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1l1llll1111_opy_(instance, bstack1l11l11ll1l_opy_.bstack11l11ll1111_opy_, False):
            return
        if not f.bstack1l1lllll1l1_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_):
            return
        platform_index = f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_)
        if f.bstack11lllll111l_opy_(method_name, *args) and len(args) > 1:
            bstack1l11111lll_opy_ = datetime.now()
            hub_url = bstack1l11lll111l_opy_.hub_url(driver)
            self.logger.warning(bstack111ll_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᠼ") + str(hub_url) + bstack111ll_opy_ (u"ࠥࠦᠽ"))
            bstack11l1l11ll1l_opy_ = args[1][bstack111ll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᠾ")] if isinstance(args[1], dict) and bstack111ll_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᠿ") in args[1] else None
            bstack11l11lll1l1_opy_ = bstack111ll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦᡀ")
            if isinstance(bstack11l1l11ll1l_opy_, dict):
                bstack1l11111lll_opy_ = datetime.now()
                r = self.bstack11l11l1ll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᡁ"), datetime.now() - bstack1l11111lll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack111ll_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥᡂ") + str(r) + bstack111ll_opy_ (u"ࠤࠥᡃ"))
                        return
                    if r.hub_url:
                        f.bstack11l1l11l111_opy_(instance, driver, r.hub_url)
                        f.bstack11ll11l1_opy_(instance, bstack1l11l11ll1l_opy_.bstack11l11ll1111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack111ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᡄ"), e)
    def bstack11l11ll11l1_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l11lll111l_opy_.session_id(driver)
            if session_id:
                bstack11l1l1111l1_opy_ = bstack111ll_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨᡅ").format(session_id)
                bstack111l1l1l_opy_.mark(bstack11l1l1111l1_opy_)
    def bstack11l1l1111ll_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1l1llll1111_opy_(instance, bstack1l11l11ll1l_opy_.bstack11l1l111lll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l11lll111l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᡆ") + str(hub_url) + bstack111ll_opy_ (u"ࠨࠢᡇ"))
            return
        framework_session_id = bstack1l11lll111l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᡈ") + str(framework_session_id) + bstack111ll_opy_ (u"ࠣࠤᡉ"))
            return
        if bstack1l11lll111l_opy_.bstack11l11ll1l1l_opy_(*args) == bstack1l11lll111l_opy_.bstack11l11ll1lll_opy_:
            bstack11l11ll111l_opy_ = bstack111ll_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤᡊ").format(framework_session_id)
            bstack11l1l1111l1_opy_ = bstack111ll_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᡋ").format(framework_session_id)
            bstack111l1l1l_opy_.end(
                label=bstack111ll_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢᡌ"),
                start=bstack11l1l1111l1_opy_,
                end=bstack11l11ll111l_opy_,
                status=True,
                failure=None
            )
            bstack1l11111lll_opy_ = datetime.now()
            r = self.bstack11l11l1lll1_opy_(
                ref,
                f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᡍ"), datetime.now() - bstack1l11111lll_opy_)
            f.bstack11ll11l1_opy_(instance, bstack1l11l11ll1l_opy_.bstack11l1l111lll_opy_, r.success)
    def bstack11l11ll11ll_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1l1llll1111_opy_(instance, bstack1l11l11ll1l_opy_.bstack11l11ll1l11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l11lll111l_opy_.session_id(driver)
        hub_url = bstack1l11lll111l_opy_.hub_url(driver)
        bstack1l11111lll_opy_ = datetime.now()
        r = self.bstack11l11llll1l_opy_(
            ref,
            f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᡎ"), datetime.now() - bstack1l11111lll_opy_)
        f.bstack11ll11l1_opy_(instance, bstack1l11l11ll1l_opy_.bstack11l11ll1l11_opy_, r.success)
    @measure(event_name=EVENTS.bstack111111111l_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11l1lll11l1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
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
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᡏ") + str(req) + bstack111ll_opy_ (u"ࠣࠤᡐ"))
        try:
            r = self.bstack111111ll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᡑ") + str(r.success) + bstack111ll_opy_ (u"ࠥࠦᡒ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᡓ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᡔ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l111ll1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11l11l1ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack11llllll111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack111ll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᡕ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᡖ") + str(req) + bstack111ll_opy_ (u"ࠣࠤᡗ"))
        try:
            r = self.bstack111111ll1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᡘ") + str(r.success) + bstack111ll_opy_ (u"ࠥࠦᡙ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᡚ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᡛ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11lllll1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11l11l1lll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack11llllll111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack111ll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᡜ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴ࠻ࠢࠥᡝ") + str(req) + bstack111ll_opy_ (u"ࠣࠤᡞ"))
        try:
            r = self.bstack111111ll1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᡟ") + str(r) + bstack111ll_opy_ (u"ࠥࠦᡠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᡡ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᡢ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11llllll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11l11llll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack11llllll111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack111ll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᡣ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤᡤ") + str(req) + bstack111ll_opy_ (u"ࠣࠤᡥ"))
        try:
            r = self.bstack111111ll1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᡦ") + str(r) + bstack111ll_opy_ (u"ࠥࠦᡧ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᡨ") + str(e) + bstack111ll_opy_ (u"ࠧࠨᡩ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111lllll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11l1l11ll11_opy_(self, instance: bstack1l1ll111lll_opy_, url: str, f: bstack1l11lll111l_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11l11llll11_opy_ = os.environ.get(bstack111ll_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧᡪ"))
        if bstack11l11llll11_opy_ is not None:
            browserstack_sdk.bstack111111lll_opy_ = bstack11l11llll11_opy_.lower() == bstack111ll_opy_ (u"ࠧࡵࡴࡸࡩࠬᡫ")
        bstack11l11ll1ll1_opy_ = version.parse(f.framework_version)
        bstack11l1l111l11_opy_ = f.platform_index
        bstack11l1l111l1l_opy_ = kwargs.get(bstack111ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᡬ"))
        bstack11l11lll11l_opy_ = kwargs.get(bstack111ll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᡭ"))
        bstack1l11ll1l1_opy_ = {}
        bstack11l11lll1ll_opy_ = {}
        bstack11l1l11l1l1_opy_ = None
        bstack11l11l1l1ll_opy_ = {}
        if bstack11l11lll11l_opy_ is not None or bstack11l1l111l1l_opy_ is not None: # check top level caps
            if bstack11l11lll11l_opy_ is not None:
                bstack11l11l1l1ll_opy_[bstack111ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᡮ")] = bstack11l11lll11l_opy_
            if bstack11l1l111l1l_opy_ is not None and callable(getattr(bstack11l1l111l1l_opy_, bstack111ll_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᡯ"))):
                bstack11l11l1l1ll_opy_[bstack111ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡰ")] = bstack11l1l111l1l_opy_.to_capabilities()
        response = self.bstack11l1lll11l1_opy_(bstack11l1l111l11_opy_, url, instance.ref(), json.dumps(bstack11l11l1l1ll_opy_).encode(bstack111ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᡱ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1l11ll1l1_opy_ = json.loads(response.capabilities.decode(bstack111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᡲ")))
            if browserstack_sdk.bstack111111lll_opy_:
                def bstack11l1l11111l_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l1l11111l_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1l11ll1l1_opy_ = bstack11l1l11111l_opy_(bstack1l11ll1l1_opy_)
                try:
                    bstack11l1l11l11l_opy_ = None
                    if isinstance(bstack1l11ll1l1_opy_, dict):
                        if bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᡳ") in bstack1l11ll1l1_opy_:
                            bstack11l1l11l11l_opy_ = bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᡴ"))
                        elif isinstance(bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᡵ")), dict):
                            bstack11l1l11l11l_opy_ = bstack1l11ll1l1_opy_[bstack111ll_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᡶ")].get(bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡷ"))
                        if isinstance(bstack11l1l11l11l_opy_, dict) and bstack111ll_opy_ (u"࠭࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠬᡸ") in bstack11l1l11l11l_opy_:
                            self.logger.debug(bstack111ll_opy_ (u"ࠢࡓࡧࡰࡳࡻ࡯࡮ࡨࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡࡨࡵࡳࡲࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡨࡥࡧࡱࡵࡩࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡰࠢ࡫ࡹࡧࠨ᡹"))
                            try:
                                bstack11l1l11l11l_opy_.pop(bstack111ll_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧ᡺"), None)
                            except Exception:
                                pass
                            if bstack111ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᡻") in bstack1l11ll1l1_opy_:
                                bstack1l11ll1l1_opy_[bstack111ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᡼")] = bstack11l1l11l11l_opy_
                            if isinstance(bstack1l11ll1l1_opy_.get(bstack111ll_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩ᡽")), dict):
                                bstack1l11ll1l1_opy_[bstack111ll_opy_ (u"ࠬࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠪ᡾")][bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᡿")] = bstack11l1l11l11l_opy_
                except Exception:
                    pass
            if not bstack1l11ll1l1_opy_ and not browserstack_sdk.bstack111111lll_opy_:
                return
            bstack11l1l11l1l1_opy_ = f.bstack1l11l11lll1_opy_[bstack111ll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᢀ")](bstack1l11ll1l1_opy_)
        if bstack11l1l111l1l_opy_ is not None and bstack11l11ll1ll1_opy_ >= version.parse(bstack111ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᢁ")):
            bstack11l11lll1ll_opy_ = None
        if (
                not bstack11l1l111l1l_opy_ and not bstack11l11lll11l_opy_
        ) or (
                bstack11l11ll1ll1_opy_ < version.parse(bstack111ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᢂ"))
        ):
            bstack11l11lll1ll_opy_ = {}
            bstack11l11lll1ll_opy_.update(bstack1l11ll1l1_opy_)
        self.logger.info(bstack111l111lll_opy_)
        if browserstack_sdk.bstack111111lll_opy_:
            bstack11l1l111111_opy_ = bstack11l1l11l1l1_opy_ if bstack11l1l11l1l1_opy_ else bstack11l1l111l1l_opy_
            if bstack11l1l111111_opy_:
                bstack11l11l11ll_opy_ = bstack1l1l1l1ll_opy_(bstack11l1l111111_opy_, bstack11l1ll1111_opy_=bstack111ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᢃ"))
                if bstack11l1l111111_opy_ is bstack11l1l111l1l_opy_ and not bstack11l1l11l1l1_opy_:
                    bstack11l1l11l1l1_opy_ = bstack11l1l111111_opy_
            kwargs.update({bstack111ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᢄ"): bstack11l1111l1l_opy_})
        elif os.environ.get(bstack111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᢅ")).lower().__eq__(bstack111ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᢆ")):
            kwargs.update({bstack111ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᢇ"): f.bstack11l1l11llll_opy_})
        if bstack11l11ll1ll1_opy_ >= version.parse(bstack111ll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᢈ")):
            if bstack11l11lll11l_opy_ is not None:
                del kwargs[bstack111ll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᢉ")]
            kwargs.update(
                {
                    bstack111ll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᢊ"): bstack11l1l11l1l1_opy_,
                    bstack111ll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᢋ"): True,
                    bstack111ll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᢌ"): None,
                }
            )
        elif bstack11l11ll1ll1_opy_ >= version.parse(bstack111ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᢍ")):
            kwargs.update(
                {
                    bstack111ll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᢎ"): bstack11l11lll1ll_opy_,
                    bstack111ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᢏ"): bstack11l1l11l1l1_opy_,
                    bstack111ll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᢐ"): True,
                    bstack111ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᢑ"): None,
                }
            )
        elif bstack11l11ll1ll1_opy_ >= version.parse(bstack111ll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᢒ")):
            kwargs.update(
                {
                    bstack111ll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᢓ"): bstack11l11lll1ll_opy_,
                    bstack111ll_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᢔ"): True,
                    bstack111ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᢕ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack111ll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᢖ"): bstack11l11lll1ll_opy_,
                    bstack111ll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᢗ"): True,
                    bstack111ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᢘ"): None,
                }
            )