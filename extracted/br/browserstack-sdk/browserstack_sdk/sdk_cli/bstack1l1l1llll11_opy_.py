# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1l1l111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11l11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack111l1ll11l_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from bstack_utils.bstack111l111ll1_opy_ import bstack11l1ll1l_opy_
import browserstack_sdk
class bstack1ll11111111_opy_(bstack1ll11111l11_opy_):
    bstack11ll1llllll_opy_ = bstack1ll111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᘝ")
    bstack11ll1llll1l_opy_ = bstack1ll111_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᘞ")
    bstack11ll1llll11_opy_ = bstack1ll111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᘟ")
    def __init__(self, bstack1l1ll1ll1l1_opy_):
        super().__init__()
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l1lll11_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack11lll1l1ll1_opy_)
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack1l11ll111ll_opy_)
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.POST), self.bstack11lll111lll_opy_)
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.POST), self.bstack11lll11l1l1_opy_)
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.QUIT, bstack1ll1l11ll1l_opy_.POST), self.bstack11lll11111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1l1ll1_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll111_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᘠ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1ll111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᘡ")), str):
                    url = kwargs.get(bstack1ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᘢ"))
                elif hasattr(kwargs.get(bstack1ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᘣ")), bstack1ll111_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᘤ")):
                    url = kwargs.get(bstack1ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᘥ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᘦ"))._url
            except Exception as e:
                url = bstack1ll111_opy_ (u"ࠨࠩᘧ")
                self.logger.error(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᘨ").format(e))
            self.logger.info(bstack1ll111_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᘩ").format(str(url)))
            bstack11lll11lll1_opy_ = None
            driver_rank = None
            try:
                bstack11lll11lll1_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11lll11lll1_opy_ is not None:
                    bstack11lll1l11l1_opy_ = str(bstack11lll11lll1_opy_)
                    if bstack1ll111_opy_ (u"ࠦࠨࠨᘪ") in bstack11lll1l11l1_opy_:
                        bstack11lll11l1ll_opy_ = bstack11lll1l11l1_opy_.rsplit(bstack1ll111_opy_ (u"ࠧࠩࠢᘫ"), 1)[1]
                        try:
                            driver_rank = int(bstack11lll11l1ll_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡫ࡸࡵࡴࡤࡧࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱࠠࡧࡴࡲࡱࠥࡲࡡࡣࡧ࡯ࠤࠬࢁࡥࡹࡲ࡯࡭ࡨ࡯ࡴࡠ࡮ࡤࡦࡪࡲࡽࠨ࠼ࠣࠦᘬ") + str(e) + bstack1ll111_opy_ (u"ࠢࠣᘭ"))
            except Exception as e:
                self.logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲ࠺ࠡࠤᘮ") + str(e) + bstack1ll111_opy_ (u"ࠤࠥᘯ"))
            self.bstack11lll1111ll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1ll111_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫࠾ࡽࡧࡶ࡮ࡼࡥࡳࡡࡵࡥࡳࡱࡽࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡪ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᘰ") + str(kwargs) + bstack1ll111_opy_ (u"ࠦࠧᘱ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11ll111ll_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll111lll1_opy_(instance, bstack1ll11111111_opy_.bstack11ll1llllll_opy_, False):
            return
        if not f.bstack1ll1l1lllll_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_):
            return
        platform_index = f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_)
        if f.bstack1l1l11l1ll1_opy_(method_name, *args) and len(args) > 1:
            bstack1ll1l1l111_opy_ = datetime.now()
            hub_url = bstack1ll11lll111_opy_.hub_url(driver)
            self.logger.warning(bstack1ll111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᘲ") + str(hub_url) + bstack1ll111_opy_ (u"ࠨࠢᘳ"))
            bstack11lll1l1111_opy_ = args[1][bstack1ll111_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᘴ")] if isinstance(args[1], dict) and bstack1ll111_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᘵ") in args[1] else None
            bstack11lll111111_opy_ = bstack1ll111_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᘶ")
            if isinstance(bstack11lll1l1111_opy_, dict):
                bstack1ll1l1l111_opy_ = datetime.now()
                r = self.bstack11lll1l1l11_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᘷ"), datetime.now() - bstack1ll1l1l111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll111_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᘸ") + str(r) + bstack1ll111_opy_ (u"ࠧࠨᘹ"))
                        return
                    if r.hub_url:
                        f.bstack11lll1ll1ll_opy_(instance, driver, r.hub_url)
                        f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11111111_opy_.bstack11ll1llllll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᘺ"), e)
    def bstack11lll111lll_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll11lll111_opy_.session_id(driver)
            if session_id:
                bstack11lll11ll1l_opy_ = bstack1ll111_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᘻ").format(session_id)
                bstack111ll11111_opy_.mark(bstack11lll11ll1l_opy_)
    def bstack11lll11l1l1_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll111lll1_opy_(instance, bstack1ll11111111_opy_.bstack11ll1llll1l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll11lll111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᘼ") + str(hub_url) + bstack1ll111_opy_ (u"ࠤࠥᘽ"))
            return
        framework_session_id = bstack1ll11lll111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᘾ") + str(framework_session_id) + bstack1ll111_opy_ (u"ࠦࠧᘿ"))
            return
        if bstack1ll11lll111_opy_.bstack11lll11llll_opy_(*args) == bstack1ll11lll111_opy_.bstack11ll1ll1lll_opy_:
            bstack11lll1l1l1l_opy_ = bstack1ll111_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᙀ").format(framework_session_id)
            bstack11lll11ll1l_opy_ = bstack1ll111_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᙁ").format(framework_session_id)
            bstack111ll11111_opy_.end(
                label=bstack1ll111_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᙂ"),
                start=bstack11lll11ll1l_opy_,
                end=bstack11lll1l1l1l_opy_,
                status=True,
                failure=None
            )
            bstack1ll1l1l111_opy_ = datetime.now()
            r = self.bstack11lll111l1l_opy_(
                ref,
                f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᙃ"), datetime.now() - bstack1ll1l1l111_opy_)
            f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11111111_opy_.bstack11ll1llll1l_opy_, r.success)
    def bstack11lll11111l_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll111lll1_opy_(instance, bstack1ll11111111_opy_.bstack11ll1llll11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll11lll111_opy_.session_id(driver)
        hub_url = bstack1ll11lll111_opy_.hub_url(driver)
        bstack1ll1l1l111_opy_ = datetime.now()
        r = self.bstack11lll1ll11l_opy_(
            ref,
            f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᙄ"), datetime.now() - bstack1ll1l1l111_opy_)
        f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11111111_opy_.bstack11ll1llll11_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1lll1l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11lllllll1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11ll1lll11l_opy_ = int(driver_rank)
                is_secondary_driver = bstack11ll1lll11l_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᙅ") + str(req) + bstack1ll111_opy_ (u"ࠦࠧᙆ"))
        try:
            r = self.bstack1ll1lll11ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᙇ") + str(r.success) + bstack1ll111_opy_ (u"ࠨࠢᙈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᙉ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᙊ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll11l111_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11lll1l1l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᙋ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᙌ") + str(req) + bstack1ll111_opy_ (u"ࠦࠧᙍ"))
        try:
            r = self.bstack1ll1lll11ll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᙎ") + str(r.success) + bstack1ll111_opy_ (u"ࠨࠢᙏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᙐ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᙑ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1ll111_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11lll111l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᙒ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᙓ") + str(req) + bstack1ll111_opy_ (u"ࠦࠧᙔ"))
        try:
            r = self.bstack1ll1lll11ll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᙕ") + str(r) + bstack1ll111_opy_ (u"ࠨࠢᙖ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᙗ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᙘ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1lll1l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11lll1ll11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᙙ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᙚ") + str(req) + bstack1ll111_opy_ (u"ࠦࠧᙛ"))
        try:
            r = self.bstack1ll1lll11ll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᙜ") + str(r) + bstack1ll111_opy_ (u"ࠨࠢᙝ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᙞ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᙟ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll11l111_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11lll1111ll_opy_(self, instance: bstack1ll1l1l111l_opy_, url: str, f: bstack1ll11lll111_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11lll11ll11_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪᙠ"))
        if bstack11lll11ll11_opy_ is not None:
            browserstack_sdk.bstack1ll1111l1l_opy_ = bstack11lll11ll11_opy_.lower() == bstack1ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨᙡ")
        bstack11lll1111l1_opy_ = version.parse(f.framework_version)
        bstack11ll1lll1ll_opy_ = f.platform_index
        bstack11ll1lll111_opy_ = kwargs.get(bstack1ll111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᙢ"))
        bstack11lll1ll1l1_opy_ = kwargs.get(bstack1ll111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᙣ"))
        bstack1lll1111ll1_opy_ = {}
        bstack11lll111l11_opy_ = {}
        bstack11ll1lllll1_opy_ = None
        bstack11lll11l11l_opy_ = {}
        if bstack11lll1ll1l1_opy_ is not None or bstack11ll1lll111_opy_ is not None: # check top level caps
            if bstack11lll1ll1l1_opy_ is not None:
                bstack11lll11l11l_opy_[bstack1ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᙤ")] = bstack11lll1ll1l1_opy_
            if bstack11ll1lll111_opy_ is not None and callable(getattr(bstack11ll1lll111_opy_, bstack1ll111_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᙥ"))):
                bstack11lll11l11l_opy_[bstack1ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᙦ")] = bstack11ll1lll111_opy_.to_capabilities()
        response = self.bstack11lllllll1l_opy_(bstack11ll1lll1ll_opy_, url, instance.ref(), json.dumps(bstack11lll11l11l_opy_).encode(bstack1ll111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᙧ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1lll1111ll1_opy_ = json.loads(response.capabilities.decode(bstack1ll111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᙨ")))
            if browserstack_sdk.bstack1ll1111l1l_opy_:
                def bstack11lll111ll1_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11lll111ll1_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1lll1111ll1_opy_ = bstack11lll111ll1_opy_(bstack1lll1111ll1_opy_)
                try:
                    bstack11lll1l11ll_opy_ = None
                    if isinstance(bstack1lll1111ll1_opy_, dict):
                        if bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᙩ") in bstack1lll1111ll1_opy_:
                            bstack11lll1l11ll_opy_ = bstack1lll1111ll1_opy_.get(bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙪ"))
                        elif isinstance(bstack1lll1111ll1_opy_.get(bstack1ll111_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᙫ")), dict):
                            bstack11lll1l11ll_opy_ = bstack1lll1111ll1_opy_[bstack1ll111_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᙬ")].get(bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᙭"))
                        if isinstance(bstack11lll1l11ll_opy_, dict) and bstack1ll111_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨ᙮") in bstack11lll1l11ll_opy_:
                            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡖࡪࡳ࡯ࡷ࡫ࡱ࡫ࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡫ࡸ࡯࡮ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡤࡨࡪࡴࡸࡥࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡳࠥ࡮ࡵࡣࠤᙯ"))
                            try:
                                bstack11lll1l11ll_opy_.pop(bstack1ll111_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪᙰ"), None)
                            except Exception:
                                pass
                            if bstack1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙱ") in bstack1lll1111ll1_opy_:
                                bstack1lll1111ll1_opy_[bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᙲ")] = bstack11lll1l11ll_opy_
                            if isinstance(bstack1lll1111ll1_opy_.get(bstack1ll111_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᙳ")), dict):
                                bstack1lll1111ll1_opy_[bstack1ll111_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᙴ")][bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᙵ")] = bstack11lll1l11ll_opy_
                except Exception:
                    pass
            if not bstack1lll1111ll1_opy_ and not browserstack_sdk.bstack1ll1111l1l_opy_:
                return
            bstack11ll1lllll1_opy_ = f.bstack1l1llllll1l_opy_[bstack1ll111_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᙶ")](bstack1lll1111ll1_opy_)
        if bstack11ll1lll111_opy_ is not None and bstack11lll1111l1_opy_ >= version.parse(bstack1ll111_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᙷ")):
            bstack11lll111l11_opy_ = None
        if (
                not bstack11ll1lll111_opy_ and not bstack11lll1ll1l1_opy_
        ) or (
                bstack11lll1111l1_opy_ < version.parse(bstack1ll111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᙸ"))
        ):
            bstack11lll111l11_opy_ = {}
            bstack11lll111l11_opy_.update(bstack1lll1111ll1_opy_)
        self.logger.info(bstack1l11l11l11_opy_)
        if browserstack_sdk.bstack1ll1111l1l_opy_:
            bstack11lll1l111l_opy_ = bstack11ll1lllll1_opy_ if bstack11ll1lllll1_opy_ else bstack11ll1lll111_opy_
            if bstack11lll1l111l_opy_:
                bstack111lll1l1_opy_ = bstack11l1ll1l_opy_(bstack11lll1l111l_opy_, bstack1l11l111l_opy_=bstack1ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᙹ"))
                if bstack11lll1l111l_opy_ is bstack11ll1lll111_opy_ and not bstack11ll1lllll1_opy_:
                    bstack11ll1lllll1_opy_ = bstack11lll1l111l_opy_
            kwargs.update({bstack1ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᙺ"): bstack111l1ll11l_opy_})
        elif os.environ.get(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦᙻ")).lower().__eq__(bstack1ll111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᙼ")):
            kwargs.update({bstack1ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᙽ"): f.bstack11lll1l1lll_opy_})
        if bstack11lll1111l1_opy_ >= version.parse(bstack1ll111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᙾ")):
            if bstack11lll1ll1l1_opy_ is not None:
                del kwargs[bstack1ll111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᙿ")]
            kwargs.update(
                {
                    bstack1ll111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢ "): bstack11ll1lllll1_opy_,
                    bstack1ll111_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᚁ"): True,
                    bstack1ll111_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᚂ"): None,
                }
            )
        elif bstack11lll1111l1_opy_ >= version.parse(bstack1ll111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᚃ")):
            kwargs.update(
                {
                    bstack1ll111_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᚄ"): bstack11lll111l11_opy_,
                    bstack1ll111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᚅ"): bstack11ll1lllll1_opy_,
                    bstack1ll111_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᚆ"): True,
                    bstack1ll111_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᚇ"): None,
                }
            )
        elif bstack11lll1111l1_opy_ >= version.parse(bstack1ll111_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᚈ")):
            kwargs.update(
                {
                    bstack1ll111_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᚉ"): bstack11lll111l11_opy_,
                    bstack1ll111_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᚊ"): True,
                    bstack1ll111_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᚋ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll111_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᚌ"): bstack11lll111l11_opy_,
                    bstack1ll111_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᚍ"): True,
                    bstack1ll111_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᚎ"): None,
                }
            )