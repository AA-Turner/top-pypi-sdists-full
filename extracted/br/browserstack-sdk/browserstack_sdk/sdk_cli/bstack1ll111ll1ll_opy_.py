# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1l1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l1l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1l11lll11_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from bstack_utils.bstack11l111l11_opy_ import bstack111ll11ll1_opy_
import browserstack_sdk
class bstack1ll1111lll1_opy_(bstack1l1ll1lll11_opy_):
    bstack11lll1ll111_opy_ = bstack11l11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᔓ")
    bstack11llll1l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᔔ")
    bstack11lll1l11ll_opy_ = bstack11l11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᔕ")
    def __init__(self, bstack1ll111l1l11_opy_):
        super().__init__()
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1lll1111111_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack11llll1111l_opy_)
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l1l1111l11_opy_)
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.POST), self.bstack11llll1ll11_opy_)
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.POST), self.bstack11llll1l11l_opy_)
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.QUIT, bstack1ll1l1llll1_opy_.POST), self.bstack11lllll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll1111l_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l11_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᔖ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔗ")), str):
                    url = kwargs.get(bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔘ"))
                elif hasattr(kwargs.get(bstack11l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᔙ")), bstack11l11_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᔚ")):
                    url = kwargs.get(bstack11l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᔛ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᔜ"))._url
            except Exception as e:
                url = bstack11l11_opy_ (u"ࠨࠩᔝ")
                self.logger.error(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᔞ").format(e))
            self.logger.info(bstack11l11_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᔟ").format(str(url)))
            bstack11llll11lll_opy_ = None
            driver_rank = None
            try:
                bstack11llll11lll_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11llll11lll_opy_ is not None:
                    bstack11lll1ll1l1_opy_ = str(bstack11llll11lll_opy_)
                    if bstack11l11_opy_ (u"ࠦࠨࠨᔠ") in bstack11lll1ll1l1_opy_:
                        bstack11llll11l11_opy_ = bstack11lll1ll1l1_opy_.rsplit(bstack11l11_opy_ (u"ࠧࠩࠢᔡ"), 1)[1]
                        try:
                            driver_rank = int(bstack11llll11l11_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡫ࡸࡵࡴࡤࡧࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱࠠࡧࡴࡲࡱࠥࡲࡡࡣࡧ࡯ࠤࠬࢁࡥࡹࡲ࡯࡭ࡨ࡯ࡴࡠ࡮ࡤࡦࡪࡲࡽࠨ࠼ࠣࠦᔢ") + str(e) + bstack11l11_opy_ (u"ࠢࠣᔣ"))
            except Exception as e:
                self.logger.debug(bstack11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲ࠺ࠡࠤᔤ") + str(e) + bstack11l11_opy_ (u"ࠤࠥᔥ"))
            self.bstack11llll111ll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack11l11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫࠾ࡽࡧࡶ࡮ࡼࡥࡳࡡࡵࡥࡳࡱࡽࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡪ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᔦ") + str(kwargs) + bstack11l11_opy_ (u"ࠦࠧᔧ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1l1111l11_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll111111l_opy_(instance, bstack1ll1111lll1_opy_.bstack11lll1ll111_opy_, False):
            return
        if not f.bstack1ll1l1lll11_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_):
            return
        platform_index = f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_)
        if f.bstack1l1l11l1lll_opy_(method_name, *args) and len(args) > 1:
            bstack1lllll111_opy_ = datetime.now()
            hub_url = bstack1l1llllllll_opy_.hub_url(driver)
            self.logger.warning(bstack11l11_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᔨ") + str(hub_url) + bstack11l11_opy_ (u"ࠨࠢᔩ"))
            bstack11llll1l1l1_opy_ = args[1][bstack11l11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᔪ")] if isinstance(args[1], dict) and bstack11l11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᔫ") in args[1] else None
            bstack11llll1l111_opy_ = bstack11l11_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᔬ")
            if isinstance(bstack11llll1l1l1_opy_, dict):
                bstack1lllll111_opy_ = datetime.now()
                r = self.bstack11lll1l1ll1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᔭ"), datetime.now() - bstack1lllll111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l11_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᔮ") + str(r) + bstack11l11_opy_ (u"ࠧࠨᔯ"))
                        return
                    if r.hub_url:
                        f.bstack11lllll111l_opy_(instance, driver, r.hub_url)
                        f.bstack1ll1lll111l_opy_(instance, bstack1ll1111lll1_opy_.bstack11lll1ll111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᔰ"), e)
    def bstack11llll1ll11_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l1llllllll_opy_.session_id(driver)
            if session_id:
                bstack11llll11ll1_opy_ = bstack11l11_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᔱ").format(session_id)
                bstack111l1lllll_opy_.mark(bstack11llll11ll1_opy_)
    def bstack11llll1l11l_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll111111l_opy_(instance, bstack1ll1111lll1_opy_.bstack11llll1l1ll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l1llllllll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᔲ") + str(hub_url) + bstack11l11_opy_ (u"ࠤࠥᔳ"))
            return
        framework_session_id = bstack1l1llllllll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᔴ") + str(framework_session_id) + bstack11l11_opy_ (u"ࠦࠧᔵ"))
            return
        if bstack1l1llllllll_opy_.bstack11lllll1ll1_opy_(*args) == bstack1l1llllllll_opy_.bstack11llll111l1_opy_:
            bstack11lllll11ll_opy_ = bstack11l11_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᔶ").format(framework_session_id)
            bstack11llll11ll1_opy_ = bstack11l11_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᔷ").format(framework_session_id)
            bstack111l1lllll_opy_.end(
                label=bstack11l11_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᔸ"),
                start=bstack11llll11ll1_opy_,
                end=bstack11lllll11ll_opy_,
                status=True,
                failure=None
            )
            bstack1lllll111_opy_ = datetime.now()
            r = self.bstack11lll1llll1_opy_(
                ref,
                f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᔹ"), datetime.now() - bstack1lllll111_opy_)
            f.bstack1ll1lll111l_opy_(instance, bstack1ll1111lll1_opy_.bstack11llll1l1ll_opy_, r.success)
    def bstack11lllll11l1_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll111111l_opy_(instance, bstack1ll1111lll1_opy_.bstack11lll1l11ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l1llllllll_opy_.session_id(driver)
        hub_url = bstack1l1llllllll_opy_.hub_url(driver)
        bstack1lllll111_opy_ = datetime.now()
        r = self.bstack11lll1lll11_opy_(
            ref,
            f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᔺ"), datetime.now() - bstack1lllll111_opy_)
        f.bstack1ll1lll111l_opy_(instance, bstack1ll1111lll1_opy_.bstack11lll1l11ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll11111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l11111l11l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
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
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᔻ") + str(req) + bstack11l11_opy_ (u"ࠦࠧᔼ"))
        try:
            r = self.bstack1ll1l1l1lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᔽ") + str(r.success) + bstack11l11_opy_ (u"ࠨࠢᔾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᔿ") + str(e) + bstack11l11_opy_ (u"ࠣࠤᕀ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lllll1l1l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack11lll1l1ll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕁ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᕂ") + str(req) + bstack11l11_opy_ (u"ࠦࠧᕃ"))
        try:
            r = self.bstack1ll1l1l1lll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᕄ") + str(r.success) + bstack11l11_opy_ (u"ࠨࠢᕅ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕆ") + str(e) + bstack11l11_opy_ (u"ࠣࠤᕇ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1ll11l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack11lll1llll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕈ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᕉ") + str(req) + bstack11l11_opy_ (u"ࠦࠧᕊ"))
        try:
            r = self.bstack1ll1l1l1lll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᕋ") + str(r) + bstack11l11_opy_ (u"ࠨࠢᕌ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕍ") + str(e) + bstack11l11_opy_ (u"ࠣࠤᕎ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1l11l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack11lll1lll11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕏ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᕐ") + str(req) + bstack11l11_opy_ (u"ࠦࠧᕑ"))
        try:
            r = self.bstack1ll1l1l1lll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᕒ") + str(r) + bstack11l11_opy_ (u"ࠨࠢᕓ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕔ") + str(e) + bstack11l11_opy_ (u"ࠣࠤᕕ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack11llll111ll_opy_(self, instance: bstack1ll1l1ll1ll_opy_, url: str, f: bstack1l1llllllll_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11llll1ll1l_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪᕖ"))
        if bstack11llll1ll1l_opy_ is not None:
            browserstack_sdk.bstack1ll11l1111_opy_ = bstack11llll1ll1l_opy_.lower() == bstack11l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᕗ")
        bstack11llll1lll1_opy_ = version.parse(f.framework_version)
        bstack11lll1lllll_opy_ = f.platform_index
        bstack11lllll1111_opy_ = kwargs.get(bstack11l11_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᕘ"))
        bstack11llll11111_opy_ = kwargs.get(bstack11l11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕙ"))
        bstack1l1111ll1l1_opy_ = {}
        bstack11lllll1l11_opy_ = {}
        bstack11lll1l1lll_opy_ = None
        bstack11lll1l1l11_opy_ = {}
        if bstack11llll11111_opy_ is not None or bstack11lllll1111_opy_ is not None: # check top level caps
            if bstack11llll11111_opy_ is not None:
                bstack11lll1l1l11_opy_[bstack11l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᕚ")] = bstack11llll11111_opy_
            if bstack11lllll1111_opy_ is not None and callable(getattr(bstack11lllll1111_opy_, bstack11l11_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᕛ"))):
                bstack11lll1l1l11_opy_[bstack11l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᕜ")] = bstack11lllll1111_opy_.to_capabilities()
        response = self.bstack1l11111l11l_opy_(bstack11lll1lllll_opy_, url, instance.ref(), json.dumps(bstack11lll1l1l11_opy_).encode(bstack11l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᕝ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1l1111ll1l1_opy_ = json.loads(response.capabilities.decode(bstack11l11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᕞ")))
            if browserstack_sdk.bstack1ll11l1111_opy_:
                def bstack11lll1ll1ll_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11lll1ll1ll_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1l1111ll1l1_opy_ = bstack11lll1ll1ll_opy_(bstack1l1111ll1l1_opy_)
                try:
                    bstack11lll1lll1l_opy_ = None
                    if isinstance(bstack1l1111ll1l1_opy_, dict):
                        if bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᕟ") in bstack1l1111ll1l1_opy_:
                            bstack11lll1lll1l_opy_ = bstack1l1111ll1l1_opy_.get(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕠ"))
                        elif isinstance(bstack1l1111ll1l1_opy_.get(bstack11l11_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᕡ")), dict):
                            bstack11lll1lll1l_opy_ = bstack1l1111ll1l1_opy_[bstack11l11_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᕢ")].get(bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᕣ"))
                        if isinstance(bstack11lll1lll1l_opy_, dict) and bstack11l11_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨᕤ") in bstack11lll1lll1l_opy_:
                            self.logger.debug(bstack11l11_opy_ (u"ࠥࡖࡪࡳ࡯ࡷ࡫ࡱ࡫ࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡫ࡸ࡯࡮ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡤࡨࡪࡴࡸࡥࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡳࠥ࡮ࡵࡣࠤᕥ"))
                            try:
                                bstack11lll1lll1l_opy_.pop(bstack11l11_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪᕦ"), None)
                            except Exception:
                                pass
                            if bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕧ") in bstack1l1111ll1l1_opy_:
                                bstack1l1111ll1l1_opy_[bstack11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᕨ")] = bstack11lll1lll1l_opy_
                            if isinstance(bstack1l1111ll1l1_opy_.get(bstack11l11_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᕩ")), dict):
                                bstack1l1111ll1l1_opy_[bstack11l11_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᕪ")][bstack11l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᕫ")] = bstack11lll1lll1l_opy_
                except Exception:
                    pass
            if not bstack1l1111ll1l1_opy_ and not browserstack_sdk.bstack1ll11l1111_opy_:
                return
            bstack11lll1l1lll_opy_ = f.bstack1l1llll111l_opy_[bstack11l11_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᕬ")](bstack1l1111ll1l1_opy_)
        if bstack11lllll1111_opy_ is not None and bstack11llll1lll1_opy_ >= version.parse(bstack11l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᕭ")):
            bstack11lllll1l11_opy_ = None
        if (
                not bstack11lllll1111_opy_ and not bstack11llll11111_opy_
        ) or (
                bstack11llll1lll1_opy_ < version.parse(bstack11l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᕮ"))
        ):
            bstack11lllll1l11_opy_ = {}
            bstack11lllll1l11_opy_.update(bstack1l1111ll1l1_opy_)
        self.logger.info(bstack111l1l1l1_opy_)
        if browserstack_sdk.bstack1ll11l1111_opy_:
            bstack11llll1llll_opy_ = bstack11lll1l1lll_opy_ if bstack11lll1l1lll_opy_ else bstack11lllll1111_opy_
            if bstack11llll1llll_opy_:
                bstack1ll1l1ll11_opy_ = bstack111ll11ll1_opy_(bstack11llll1llll_opy_, bstack111111lll_opy_=bstack11l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᕯ"))
                if bstack11llll1llll_opy_ is bstack11lllll1111_opy_ and not bstack11lll1l1lll_opy_:
                    bstack11lll1l1lll_opy_ = bstack11llll1llll_opy_
            kwargs.update({bstack11l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᕰ"): bstack1l11lll11_opy_})
        elif os.environ.get(bstack11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦᕱ")).lower().__eq__(bstack11l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᕲ")):
            kwargs.update({bstack11l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᕳ"): f.bstack11lll1l1l1l_opy_})
        if bstack11llll1lll1_opy_ >= version.parse(bstack11l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᕴ")):
            if bstack11llll11111_opy_ is not None:
                del kwargs[bstack11l11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕵ")]
            kwargs.update(
                {
                    bstack11l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᕶ"): bstack11lll1l1lll_opy_,
                    bstack11l11_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᕷ"): True,
                    bstack11l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᕸ"): None,
                }
            )
        elif bstack11llll1lll1_opy_ >= version.parse(bstack11l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᕹ")):
            kwargs.update(
                {
                    bstack11l11_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᕺ"): bstack11lllll1l11_opy_,
                    bstack11l11_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᕻ"): bstack11lll1l1lll_opy_,
                    bstack11l11_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᕼ"): True,
                    bstack11l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᕽ"): None,
                }
            )
        elif bstack11llll1lll1_opy_ >= version.parse(bstack11l11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᕾ")):
            kwargs.update(
                {
                    bstack11l11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᕿ"): bstack11lllll1l11_opy_,
                    bstack11l11_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᖀ"): True,
                    bstack11l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᖁ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l11_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᖂ"): bstack11lllll1l11_opy_,
                    bstack11l11_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᖃ"): True,
                    bstack11l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᖄ"): None,
                }
            )