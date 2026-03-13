# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1l1lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack111ll1ll1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from bstack_utils.bstack11lll11l11_opy_ import bstack1l111l11l_opy_
import browserstack_sdk
class bstack1l1lll11ll1_opy_(bstack1ll1111l1ll_opy_):
    bstack11ll1ll1l1l_opy_ = bstack1111l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᙠ")
    bstack11lll11l11l_opy_ = bstack1111l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᙡ")
    bstack11ll1lll1l1_opy_ = bstack1111l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᙢ")
    def __init__(self, bstack1ll11l1ll1l_opy_):
        super().__init__()
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll1l111l1l_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11ll1lllll1_opy_)
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack1l11ll1l111_opy_)
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.POST), self.bstack11lll111111_opy_)
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.POST), self.bstack11lll111l11_opy_)
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.QUIT, bstack1ll1ll1111l_opy_.POST), self.bstack11lll1l1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1lllll1_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1111l_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᙣ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᙤ")), str):
                    url = kwargs.get(bstack1111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᙥ"))
                elif hasattr(kwargs.get(bstack1111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᙦ")), bstack1111l_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪᙧ")):
                    url = kwargs.get(bstack1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᙨ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᙩ"))._url
            except Exception as e:
                url = bstack1111l_opy_ (u"ࠬ࠭ᙪ")
                self.logger.error(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦᙫ").format(e))
            self.logger.info(bstack1111l_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣᙬ").format(str(url)))
            bstack11lll11111l_opy_ = None
            driver_rank = None
            try:
                bstack11lll11111l_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11lll11111l_opy_ is not None:
                    bstack11lll111l1l_opy_ = str(bstack11lll11111l_opy_)
                    if bstack1111l_opy_ (u"ࠣࠥࠥ᙭") in bstack11lll111l1l_opy_:
                        bstack11lll1l11ll_opy_ = bstack11lll111l1l_opy_.rsplit(bstack1111l_opy_ (u"ࠤࠦࠦ᙮"), 1)[1]
                        try:
                            driver_rank = int(bstack11lll1l11ll_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡨࡼࡹࡸࡡࡤࡶ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮ࠤ࡫ࡸ࡯࡮ࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡩࡽࡶ࡬ࡪࡥ࡬ࡸࡤࡲࡡࡣࡧ࡯ࢁࠬࡀࠠࠣᙯ") + str(e) + bstack1111l_opy_ (u"ࠦࠧᙰ"))
            except Exception as e:
                self.logger.debug(bstack1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯࠾ࠥࠨᙱ") + str(e) + bstack1111l_opy_ (u"ࠨࠢᙲ"))
            self.bstack11lll1l1111_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1111l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡳࡣࡱ࡯ࡂࢁࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࢁࠥࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡧ࠰ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᙳ") + str(kwargs) + bstack1111l_opy_ (u"ࠣࠤᙴ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11ll1l111_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1lll1l11_opy_(instance, bstack1l1lll11ll1_opy_.bstack11ll1ll1l1l_opy_, False):
            return
        if not f.bstack1ll1l1l11ll_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_):
            return
        platform_index = f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_)
        if f.bstack1l1l11l11ll_opy_(method_name, *args) and len(args) > 1:
            bstack1lll1l11l_opy_ = datetime.now()
            hub_url = bstack1ll111ll1ll_opy_.hub_url(driver)
            self.logger.warning(bstack1111l_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᙵ") + str(hub_url) + bstack1111l_opy_ (u"ࠥࠦᙶ"))
            bstack11lll11l1l1_opy_ = args[1][bstack1111l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᙷ")] if isinstance(args[1], dict) and bstack1111l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᙸ") in args[1] else None
            bstack11lll1l1l1l_opy_ = bstack1111l_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦᙹ")
            if isinstance(bstack11lll11l1l1_opy_, dict):
                bstack1lll1l11l_opy_ = datetime.now()
                r = self.bstack11ll1llll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᙺ"), datetime.now() - bstack1lll1l11l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1111l_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥᙻ") + str(r) + bstack1111l_opy_ (u"ࠤࠥᙼ"))
                        return
                    if r.hub_url:
                        f.bstack11lll111ll1_opy_(instance, driver, r.hub_url)
                        f.bstack1ll1lllll11_opy_(instance, bstack1l1lll11ll1_opy_.bstack11ll1ll1l1l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᙽ"), e)
    def bstack11lll111111_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll111ll1ll_opy_.session_id(driver)
            if session_id:
                bstack11lll111lll_opy_ = bstack1111l_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨᙾ").format(session_id)
                bstack1l11ll1l1_opy_.mark(bstack11lll111lll_opy_)
    def bstack11lll111l11_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lll1l11_opy_(instance, bstack1l1lll11ll1_opy_.bstack11lll11l11l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll111ll1ll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᙿ") + str(hub_url) + bstack1111l_opy_ (u"ࠨࠢ "))
            return
        framework_session_id = bstack1ll111ll1ll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᚁ") + str(framework_session_id) + bstack1111l_opy_ (u"ࠣࠤᚂ"))
            return
        if bstack1ll111ll1ll_opy_.bstack11lll1l1lll_opy_(*args) == bstack1ll111ll1ll_opy_.bstack11lll1l11l1_opy_:
            bstack11ll1lll1ll_opy_ = bstack1111l_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤᚃ").format(framework_session_id)
            bstack11lll111lll_opy_ = bstack1111l_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᚄ").format(framework_session_id)
            bstack1l11ll1l1_opy_.end(
                label=bstack1111l_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢᚅ"),
                start=bstack11lll111lll_opy_,
                end=bstack11ll1lll1ll_opy_,
                status=True,
                failure=None
            )
            bstack1lll1l11l_opy_ = datetime.now()
            r = self.bstack11lll11lll1_opy_(
                ref,
                f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᚆ"), datetime.now() - bstack1lll1l11l_opy_)
            f.bstack1ll1lllll11_opy_(instance, bstack1l1lll11ll1_opy_.bstack11lll11l11l_opy_, r.success)
    def bstack11lll1l1l11_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lll1l11_opy_(instance, bstack1l1lll11ll1_opy_.bstack11ll1lll1l1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll111ll1ll_opy_.session_id(driver)
        hub_url = bstack1ll111ll1ll_opy_.hub_url(driver)
        bstack1lll1l11l_opy_ = datetime.now()
        r = self.bstack11lll11llll_opy_(
            ref,
            f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᚇ"), datetime.now() - bstack1lll1l11l_opy_)
        f.bstack1ll1lllll11_opy_(instance, bstack1l1lll11ll1_opy_.bstack11ll1lll1l1_opy_, r.success)
    @measure(event_name=EVENTS.bstack1111ll1ll1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack11lllll1111_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11lll11l1ll_opy_ = int(driver_rank)
                is_secondary_driver = bstack11lll11l1ll_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᚈ") + str(req) + bstack1111l_opy_ (u"ࠣࠤᚉ"))
        try:
            r = self.bstack1ll1ll1lll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᚊ") + str(r.success) + bstack1111l_opy_ (u"ࠥࠦᚋ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᚌ") + str(e) + bstack1111l_opy_ (u"ࠧࠨᚍ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1ll1lll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack11ll1llll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᚎ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᚏ") + str(req) + bstack1111l_opy_ (u"ࠣࠤᚐ"))
        try:
            r = self.bstack1ll1ll1lll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᚑ") + str(r.success) + bstack1111l_opy_ (u"ࠥࠦᚒ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᚓ") + str(e) + bstack1111l_opy_ (u"ࠧࠨᚔ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1ll1ll1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack11lll11lll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᚕ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴ࠻ࠢࠥᚖ") + str(req) + bstack1111l_opy_ (u"ࠣࠤᚗ"))
        try:
            r = self.bstack1ll1ll1lll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᚘ") + str(r) + bstack1111l_opy_ (u"ࠥࠦᚙ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᚚ") + str(e) + bstack1111l_opy_ (u"ࠧࠨ᚛"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1lll111_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack11lll11llll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᚜").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤ᚝") + str(req) + bstack1111l_opy_ (u"ࠣࠤ᚞"))
        try:
            r = self.bstack1ll1ll1lll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦ᚟") + str(r) + bstack1111l_opy_ (u"ࠥࠦᚠ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᚡ") + str(e) + bstack1111l_opy_ (u"ࠧࠨᚢ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1lll111_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack11lll1l1111_opy_(self, instance: bstack1ll1l1lll1l_opy_, url: str, f: bstack1ll111ll1ll_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11lll1111ll_opy_ = os.environ.get(bstack1111l_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧᚣ"))
        if bstack11lll1111ll_opy_ is not None:
            browserstack_sdk.bstack11l1l1l1l_opy_ = bstack11lll1111ll_opy_.lower() == bstack1111l_opy_ (u"ࠧࡵࡴࡸࡩࠬᚤ")
        bstack11lll11ll1l_opy_ = version.parse(f.framework_version)
        bstack11ll1llllll_opy_ = f.platform_index
        bstack11ll1llll11_opy_ = kwargs.get(bstack1111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᚥ"))
        bstack11ll1ll1l11_opy_ = kwargs.get(bstack1111l_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᚦ"))
        bstack1lll111l1l1_opy_ = {}
        bstack11lll11l111_opy_ = {}
        bstack11lll1l1ll1_opy_ = None
        bstack11lll1111l1_opy_ = {}
        if bstack11ll1ll1l11_opy_ is not None or bstack11ll1llll11_opy_ is not None: # check top level caps
            if bstack11ll1ll1l11_opy_ is not None:
                bstack11lll1111l1_opy_[bstack1111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᚧ")] = bstack11ll1ll1l11_opy_
            if bstack11ll1llll11_opy_ is not None and callable(getattr(bstack11ll1llll11_opy_, bstack1111l_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᚨ"))):
                bstack11lll1111l1_opy_[bstack1111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚩ")] = bstack11ll1llll11_opy_.to_capabilities()
        response = self.bstack11lllll1111_opy_(bstack11ll1llllll_opy_, url, instance.ref(), json.dumps(bstack11lll1111l1_opy_).encode(bstack1111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᚪ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1lll111l1l1_opy_ = json.loads(response.capabilities.decode(bstack1111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᚫ")))
            if browserstack_sdk.bstack11l1l1l1l_opy_:
                def bstack11ll1lll11l_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11ll1lll11l_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1lll111l1l1_opy_ = bstack11ll1lll11l_opy_(bstack1lll111l1l1_opy_)
                try:
                    bstack11lll1ll111_opy_ = None
                    if isinstance(bstack1lll111l1l1_opy_, dict):
                        if bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚬ") in bstack1lll111l1l1_opy_:
                            bstack11lll1ll111_opy_ = bstack1lll111l1l1_opy_.get(bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚭ"))
                        elif isinstance(bstack1lll111l1l1_opy_.get(bstack1111l_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᚮ")), dict):
                            bstack11lll1ll111_opy_ = bstack1lll111l1l1_opy_[bstack1111l_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᚯ")].get(bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚰ"))
                        if isinstance(bstack11lll1ll111_opy_, dict) and bstack1111l_opy_ (u"࠭࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠬᚱ") in bstack11lll1ll111_opy_:
                            self.logger.debug(bstack1111l_opy_ (u"ࠢࡓࡧࡰࡳࡻ࡯࡮ࡨࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡࡨࡵࡳࡲࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡨࡥࡧࡱࡵࡩࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡰࠢ࡫ࡹࡧࠨᚲ"))
                            try:
                                bstack11lll1ll111_opy_.pop(bstack1111l_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧᚳ"), None)
                            except Exception:
                                pass
                            if bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚴ") in bstack1lll111l1l1_opy_:
                                bstack1lll111l1l1_opy_[bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚵ")] = bstack11lll1ll111_opy_
                            if isinstance(bstack1lll111l1l1_opy_.get(bstack1111l_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᚶ")), dict):
                                bstack1lll111l1l1_opy_[bstack1111l_opy_ (u"ࠬࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠪᚷ")][bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚸ")] = bstack11lll1ll111_opy_
                except Exception:
                    pass
            if not bstack1lll111l1l1_opy_ and not browserstack_sdk.bstack11l1l1l1l_opy_:
                return
            bstack11lll1l1ll1_opy_ = f.bstack1l1ll111l11_opy_[bstack1111l_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᚹ")](bstack1lll111l1l1_opy_)
        if bstack11ll1llll11_opy_ is not None and bstack11lll11ll1l_opy_ >= version.parse(bstack1111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᚺ")):
            bstack11lll11l111_opy_ = None
        if (
                not bstack11ll1llll11_opy_ and not bstack11ll1ll1l11_opy_
        ) or (
                bstack11lll11ll1l_opy_ < version.parse(bstack1111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᚻ"))
        ):
            bstack11lll11l111_opy_ = {}
            bstack11lll11l111_opy_.update(bstack1lll111l1l1_opy_)
        self.logger.info(bstack111l11l11_opy_)
        if browserstack_sdk.bstack11l1l1l1l_opy_:
            bstack11lll11ll11_opy_ = bstack11lll1l1ll1_opy_ if bstack11lll1l1ll1_opy_ else bstack11ll1llll11_opy_
            if bstack11lll11ll11_opy_:
                bstack1l1lllll11_opy_ = bstack1l111l11l_opy_(bstack11lll11ll11_opy_, bstack1l11ll111_opy_=bstack1111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᚼ"))
                if bstack11lll11ll11_opy_ is bstack11ll1llll11_opy_ and not bstack11lll1l1ll1_opy_:
                    bstack11lll1l1ll1_opy_ = bstack11lll11ll11_opy_
            kwargs.update({bstack1111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᚽ"): bstack111ll1ll1_opy_})
        elif os.environ.get(bstack1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᚾ")).lower().__eq__(bstack1111l_opy_ (u"ࠨࡴࡳࡷࡨࠦᚿ")):
            kwargs.update({bstack1111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᛀ"): f.bstack11lll1l111l_opy_})
        if bstack11lll11ll1l_opy_ >= version.parse(bstack1111l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᛁ")):
            if bstack11ll1ll1l11_opy_ is not None:
                del kwargs[bstack1111l_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᛂ")]
            kwargs.update(
                {
                    bstack1111l_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᛃ"): bstack11lll1l1ll1_opy_,
                    bstack1111l_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᛄ"): True,
                    bstack1111l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᛅ"): None,
                }
            )
        elif bstack11lll11ll1l_opy_ >= version.parse(bstack1111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᛆ")):
            kwargs.update(
                {
                    bstack1111l_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᛇ"): bstack11lll11l111_opy_,
                    bstack1111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᛈ"): bstack11lll1l1ll1_opy_,
                    bstack1111l_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᛉ"): True,
                    bstack1111l_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᛊ"): None,
                }
            )
        elif bstack11lll11ll1l_opy_ >= version.parse(bstack1111l_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᛋ")):
            kwargs.update(
                {
                    bstack1111l_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᛌ"): bstack11lll11l111_opy_,
                    bstack1111l_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᛍ"): True,
                    bstack1111l_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᛎ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1111l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᛏ"): bstack11lll11l111_opy_,
                    bstack1111l_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᛐ"): True,
                    bstack1111l_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᛑ"): None,
                }
            )