# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack1ll11ll1l11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll111ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack111l11llll_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from bstack_utils.bstack11l1l11l_opy_ import bstack11l1ll111_opy_
import browserstack_sdk
class bstack1ll1111l111_opy_(bstack1ll111l11ll_opy_):
    bstack11ll1l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦᚶ")
    bstack11ll1ll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨᚷ")
    bstack11ll11ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨᚸ")
    def __init__(self, bstack1ll1l1l1l1l_opy_):
        super().__init__()
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11ll1l111l1_opy_)
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE), self.bstack1l11l11ll1l_opy_)
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.POST), self.bstack11ll11lllll_opy_)
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.POST), self.bstack11ll11l1ll1_opy_)
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.QUIT, bstack1l11l11l1_opy_.POST), self.bstack11ll11ll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l111l1_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᚹ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1ll1lll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᚺ")), str):
                    url = kwargs.get(bstack1ll1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᚻ"))
                elif hasattr(kwargs.get(bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᚼ")), bstack1ll1lll_opy_ (u"ࠫࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠬᚽ")):
                    url = kwargs.get(bstack1ll1lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᚾ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᚿ"))._url
            except Exception as e:
                url = bstack1ll1lll_opy_ (u"ࠧࠨᛀ")
                self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡴ࡯ࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࢂࠨᛁ").format(e))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡕࡩࡲࡵࡴࡦࠢࡖࡩࡷࡼࡥࡳࠢࡄࡨࡩࡸࡥࡴࡵࠣࡦࡪ࡯࡮ࡨࠢࡳࡥࡸࡹࡥࡥࠢࡤࡷࠥࡀࠠࡼࡿࠥᛂ").format(str(url)))
            bstack11ll11llll1_opy_ = None
            driver_rank = None
            try:
                bstack11ll11llll1_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11ll11llll1_opy_ is not None:
                    bstack11ll1l111ll_opy_ = str(bstack11ll11llll1_opy_)
                    if bstack1ll1lll_opy_ (u"ࠥࠧࠧᛃ") in bstack11ll1l111ll_opy_:
                        bstack11ll1l11l11_opy_ = bstack11ll1l111ll_opy_.rsplit(bstack1ll1lll_opy_ (u"ࠦࠨࠨᛄ"), 1)[1]
                        try:
                            driver_rank = int(bstack11ll1l11l11_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡪࡾࡴࡳࡣࡦࡸ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡴࡤࡲࡰࠦࡦࡳࡱࡰࠤࡱࡧࡢࡦ࡮ࠣࠫࢀ࡫ࡸࡱ࡮࡬ࡧ࡮ࡺ࡟࡭ࡣࡥࡩࡱࢃࠧ࠻ࠢࠥᛅ") + str(e) + bstack1ll1lll_opy_ (u"ࠨࠢᛆ"))
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࡀࠠࠣᛇ") + str(e) + bstack1ll1lll_opy_ (u"ࠣࠤᛈ"))
            self.bstack11ll11ll1ll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳࡡࡵࡥࡳࡱ࠽ࡼࡦࡵ࡭ࡻ࡫ࡲࡠࡴࡤࡲࡰࢃࠠࡥࡴ࡬ࡺࡪࡸ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡩ࠲ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࡀࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᛉ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᛊ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11l11ll1l_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1l11llll_opy_(instance, bstack1ll1111l111_opy_.bstack11ll1l11l1l_opy_, False):
            return
        if not f.bstack1ll1l1lll1l_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_):
            return
        platform_index = f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_)
        if f.bstack1l11l1l11l1_opy_(method_name, *args) and len(args) > 1:
            bstack11lllll111_opy_ = datetime.now()
            hub_url = bstack1ll111l1111_opy_.hub_url(driver)
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᛋ") + str(hub_url) + bstack1ll1lll_opy_ (u"ࠧࠨᛌ"))
            bstack11ll1l11lll_opy_ = args[1][bstack1ll1lll_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᛍ")] if isinstance(args[1], dict) and bstack1ll1lll_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᛎ") in args[1] else None
            bstack11ll1l1111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᛏ")
            if isinstance(bstack11ll1l11lll_opy_, dict):
                bstack11lllll111_opy_ = datetime.now()
                r = self.bstack11ll1l1ll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢᛐ"), datetime.now() - bstack11lllll111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡷࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩ࠽ࠤࠧᛑ") + str(r) + bstack1ll1lll_opy_ (u"ࠦࠧᛒ"))
                        return
                    if r.hub_url:
                        f.bstack11ll11l1l1l_opy_(instance, driver, r.hub_url)
                        f.bstack1lll1111ll_opy_(instance, bstack1ll1111l111_opy_.bstack11ll1l11l1l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᛓ"), e)
    def bstack11ll11lllll_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll111l1111_opy_.session_id(driver)
            if session_id:
                bstack11ll1l11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᛔ").format(session_id)
                bstack1l1l11ll1_opy_.mark(bstack11ll1l11ll1_opy_)
    def bstack11ll11l1ll1_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1l11llll_opy_(instance, bstack1ll1111l111_opy_.bstack11ll1ll11l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll111l1111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᛕ") + str(hub_url) + bstack1ll1lll_opy_ (u"ࠣࠤᛖ"))
            return
        framework_session_id = bstack1ll111l1111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᛗ") + str(framework_session_id) + bstack1ll1lll_opy_ (u"ࠥࠦᛘ"))
            return
        if bstack1ll111l1111_opy_.bstack11ll11l11ll_opy_(*args) == bstack1ll111l1111_opy_.bstack11ll11l1l11_opy_:
            bstack11ll1l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠺ࡦࡰࡧࠦᛙ").format(framework_session_id)
            bstack11ll1l11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢᛚ").format(framework_session_id)
            bstack1l1l11ll1_opy_.end(
                label=bstack1ll1lll_opy_ (u"ࠨࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠤᛛ"),
                start=bstack11ll1l11ll1_opy_,
                end=bstack11ll1l1l1l1_opy_,
                status=True,
                failure=None
            )
            bstack11lllll111_opy_ = datetime.now()
            r = self.bstack11ll1ll1111_opy_(
                ref,
                f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨᛜ"), datetime.now() - bstack11lllll111_opy_)
            f.bstack1lll1111ll_opy_(instance, bstack1ll1111l111_opy_.bstack11ll1ll11l1_opy_, r.success)
    def bstack11ll11ll111_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1l11llll_opy_(instance, bstack1ll1111l111_opy_.bstack11ll11ll11l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll111l1111_opy_.session_id(driver)
        hub_url = bstack1ll111l1111_opy_.hub_url(driver)
        bstack11lllll111_opy_ = datetime.now()
        r = self.bstack11ll11lll1l_opy_(
            ref,
            f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨᛝ"), datetime.now() - bstack11lllll111_opy_)
        f.bstack1lll1111ll_opy_(instance, bstack1ll1111l111_opy_.bstack11ll11ll11l_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll11l1l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11lll11llll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11ll11l1lll_opy_ = int(driver_rank)
                is_secondary_driver = bstack11ll11l1lll_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᛞ") + str(req) + bstack1ll1lll_opy_ (u"ࠥࠦᛟ"))
        try:
            r = self.bstack1l1llll1lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᛠ") + str(r.success) + bstack1ll1lll_opy_ (u"ࠧࠨᛡ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᛢ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᛣ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l1ll11_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11ll1l1ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᛤ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᛥ") + str(req) + bstack1ll1lll_opy_ (u"ࠥࠦᛦ"))
        try:
            r = self.bstack1l1llll1lll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᛧ") + str(r.success) + bstack1ll1lll_opy_ (u"ࠧࠨᛨ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᛩ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᛪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l1llll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11ll1ll1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᛫").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶ࠽ࠤࠧ᛬") + str(req) + bstack1ll1lll_opy_ (u"ࠥࠦ᛭"))
        try:
            r = self.bstack1l1llll1lll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᛮ") + str(r) + bstack1ll1lll_opy_ (u"ࠧࠨᛯ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᛰ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᛱ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l1l1ll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11ll11lll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᛲ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦᛳ") + str(req) + bstack1ll1lll_opy_ (u"ࠥࠦᛴ"))
        try:
            r = self.bstack1l1llll1lll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᛵ") + str(r) + bstack1ll1lll_opy_ (u"ࠧࠨᛶ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᛷ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᛸ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1l1111_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11ll11ll1ll_opy_(self, instance: bstack1ll11ll1l11_opy_, url: str, f: bstack1ll111l1111_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11ll1l1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡑ࡙ࡉࡗࡘࡉࡅࡇࡢࡐࡔࡇࡄࡠࡖࡈࡗ࡙ࡏࡎࡈࠩ᛹"))
        if bstack11ll1l1lll1_opy_ is not None:
            browserstack_sdk.bstack111l1ll1l_opy_ = bstack11ll1l1lll1_opy_.lower() == bstack1ll1lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᛺")
        bstack11ll1l11111_opy_ = version.parse(f.framework_version)
        bstack11ll1ll1l11_opy_ = f.platform_index
        bstack11ll11ll1l1_opy_ = kwargs.get(bstack1ll1lll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦ᛻"))
        bstack11ll1l1l111_opy_ = kwargs.get(bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᛼"))
        bstack1ll111ll1l_opy_ = {}
        bstack11ll11l111l_opy_ = {}
        bstack11ll1ll111l_opy_ = None
        bstack11ll1l1l11l_opy_ = {}
        if bstack11ll1l1l111_opy_ is not None or bstack11ll11ll1l1_opy_ is not None: # check top level caps
            if bstack11ll1l1l111_opy_ is not None:
                bstack11ll1l1l11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᛽")] = bstack11ll1l1l111_opy_
            if bstack11ll11ll1l1_opy_ is not None and callable(getattr(bstack11ll11ll1l1_opy_, bstack1ll1lll_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᛾"))):
                bstack11ll1l1l11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᛿")] = bstack11ll11ll1l1_opy_.to_capabilities()
        response = self.bstack11lll11llll_opy_(bstack11ll1ll1l11_opy_, url, instance.ref(), json.dumps(bstack11ll1l1l11l_opy_).encode(bstack1ll1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᜀ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1ll111ll1l_opy_ = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᜁ")))
            if browserstack_sdk.bstack111l1ll1l_opy_:
                def bstack11ll11l11l1_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11ll11l11l1_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1ll111ll1l_opy_ = bstack11ll11l11l1_opy_(bstack1ll111ll1l_opy_)
                try:
                    bstack11ll11lll11_opy_ = None
                    if isinstance(bstack1ll111ll1l_opy_, dict):
                        if bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᜂ") in bstack1ll111ll1l_opy_:
                            bstack11ll11lll11_opy_ = bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᜃ"))
                        elif isinstance(bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠪᜄ")), dict):
                            bstack11ll11lll11_opy_ = bstack1ll111ll1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᜅ")].get(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᜆ"))
                        if isinstance(bstack11ll11lll11_opy_, dict) and bstack1ll1lll_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧᜇ") in bstack11ll11lll11_opy_:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡕࡩࡲࡵࡶࡪࡰࡪࠤࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠣࡪࡷࡵ࡭ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡶࡲࠤ࡭ࡻࡢࠣᜈ"))
                            try:
                                bstack11ll11lll11_opy_.pop(bstack1ll1lll_opy_ (u"ࠪࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩᜉ"), None)
                            except Exception:
                                pass
                            if bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᜊ") in bstack1ll111ll1l_opy_:
                                bstack1ll111ll1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᜋ")] = bstack11ll11lll11_opy_
                            if isinstance(bstack1ll111ll1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᜌ")), dict):
                                bstack1ll111ll1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᜍ")][bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᜎ")] = bstack11ll11lll11_opy_
                except Exception:
                    pass
            if not bstack1ll111ll1l_opy_ and not browserstack_sdk.bstack111l1ll1l_opy_:
                return
            bstack11ll1ll111l_opy_ = f.bstack1l1l1ll1ll1_opy_[bstack1ll1lll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨᜏ")](bstack1ll111ll1l_opy_)
        if bstack11ll11ll1l1_opy_ is not None and bstack11ll1l11111_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᜐ")):
            bstack11ll11l111l_opy_ = None
        if (
                not bstack11ll11ll1l1_opy_ and not bstack11ll1l1l111_opy_
        ) or (
                bstack11ll1l11111_opy_ < version.parse(bstack1ll1lll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᜑ"))
        ):
            bstack11ll11l111l_opy_ = {}
            bstack11ll11l111l_opy_.update(bstack1ll111ll1l_opy_)
        self.logger.info(bstack1ll111ll11_opy_)
        if browserstack_sdk.bstack111l1ll1l_opy_:
            bstack11ll1ll1l1l_opy_ = bstack11ll1ll111l_opy_ if bstack11ll1ll111l_opy_ else bstack11ll11ll1l1_opy_
            if bstack11ll1ll1l1l_opy_:
                bstack1ll1l11111_opy_ = bstack11l1ll111_opy_(bstack11ll1ll1l1l_opy_, bstack11111ll1ll_opy_=bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᜒ"))
                if bstack11ll1ll1l1l_opy_ is bstack11ll11ll1l1_opy_ and not bstack11ll1ll111l_opy_:
                    bstack11ll1ll111l_opy_ = bstack11ll1ll1l1l_opy_
            kwargs.update({bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᜓ"): bstack111l11llll_opy_})
        elif os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐ᜔ࠥ")).lower().__eq__(bstack1ll1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᜕")):
            kwargs.update({bstack1ll1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᜖"): f.bstack11ll1ll11ll_opy_})
        if bstack11ll1l11111_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪ᜗")):
            if bstack11ll1l1l111_opy_ is not None:
                del kwargs[bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᜘")]
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨ᜙"): bstack11ll1ll111l_opy_,
                    bstack1ll1lll_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥ᜚"): True,
                    bstack1ll1lll_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢ᜛"): None,
                }
            )
        elif bstack11ll1l11111_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ᜜")):
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ᜝"): bstack11ll11l111l_opy_,
                    bstack1ll1lll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦ᜞"): bstack11ll1ll111l_opy_,
                    bstack1ll1lll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᜟ"): True,
                    bstack1ll1lll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᜠ"): None,
                }
            )
        elif bstack11ll1l11111_opy_ >= version.parse(bstack1ll1lll_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ᜡ")):
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᜢ"): bstack11ll11l111l_opy_,
                    bstack1ll1lll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᜣ"): True,
                    bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᜤ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᜥ"): bstack11ll11l111l_opy_,
                    bstack1ll1lll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᜦ"): True,
                    bstack1ll1lll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᜧ"): None,
                }
            )