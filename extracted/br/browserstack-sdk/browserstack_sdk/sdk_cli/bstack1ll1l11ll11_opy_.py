# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1lll1111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11llll11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1llllll1l1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from bstack_utils.bstack1ll1ll11ll_opy_ import bstack111l1ll1l_opy_
import browserstack_sdk
class bstack1ll111ll1l1_opy_(bstack1ll1l1l11l1_opy_):
    bstack11llll1lll1_opy_ = bstack11ll111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᔚ")
    bstack11lllll11l1_opy_ = bstack11ll111_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᔛ")
    bstack11llll1111l_opy_ = bstack11ll111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᔜ")
    def __init__(self, bstack1ll111l1111_opy_):
        super().__init__()
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack11llll11l11_opy_)
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l1l11l1ll1_opy_)
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.POST), self.bstack11llll1ll11_opy_)
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.POST), self.bstack11llll11lll_opy_)
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.QUIT, bstack1lll111l1l1_opy_.POST), self.bstack1l1111111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll11l11_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll111_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᔝ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔞ")), str):
                    url = kwargs.get(bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔟ"))
                elif hasattr(kwargs.get(bstack11ll111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᔠ")), bstack11ll111_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᔡ")):
                    url = kwargs.get(bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᔢ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᔣ"))._url
            except Exception as e:
                url = bstack11ll111_opy_ (u"ࠨࠩᔤ")
                self.logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᔥ").format(e))
            self.logger.info(bstack11ll111_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᔦ").format(str(url)))
            bstack11llllll11l_opy_ = None
            driver_rank = None
            try:
                bstack11llllll11l_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11llllll11l_opy_ is not None:
                    bstack11lllllll11_opy_ = str(bstack11llllll11l_opy_)
                    if bstack11ll111_opy_ (u"ࠦࠨࠨᔧ") in bstack11lllllll11_opy_:
                        bstack1l11111111l_opy_ = bstack11lllllll11_opy_.rsplit(bstack11ll111_opy_ (u"ࠧࠩࠢᔨ"), 1)[1]
                        try:
                            driver_rank = int(bstack1l11111111l_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡫ࡸࡵࡴࡤࡧࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱࠠࡧࡴࡲࡱࠥࡲࡡࡣࡧ࡯ࠤࠬࢁࡥࡹࡲ࡯࡭ࡨ࡯ࡴࡠ࡮ࡤࡦࡪࡲࡽࠨ࠼ࠣࠦᔩ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣᔪ"))
            except Exception as e:
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲ࠺ࠡࠤᔫ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥᔬ"))
            self.bstack11llll1llll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack11ll111_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫࠾ࡽࡧࡶ࡮ࡼࡥࡳࡡࡵࡥࡳࡱࡽࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡪ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᔭ") + str(kwargs) + bstack11ll111_opy_ (u"ࠦࠧᔮ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1l11l1ll1_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1lllll11_opy_(instance, bstack1ll111ll1l1_opy_.bstack11llll1lll1_opy_, False):
            return
        if not f.bstack1ll1lll111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_):
            return
        platform_index = f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_)
        if f.bstack1l1l11lll1l_opy_(method_name, *args) and len(args) > 1:
            bstack11lll11111_opy_ = datetime.now()
            hub_url = bstack1ll1111ll11_opy_.hub_url(driver)
            self.logger.warning(bstack11ll111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᔯ") + str(hub_url) + bstack11ll111_opy_ (u"ࠨࠢᔰ"))
            bstack11lllll1111_opy_ = args[1][bstack11ll111_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᔱ")] if isinstance(args[1], dict) and bstack11ll111_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᔲ") in args[1] else None
            bstack11llllll111_opy_ = bstack11ll111_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᔳ")
            if isinstance(bstack11lllll1111_opy_, dict):
                bstack11lll11111_opy_ = datetime.now()
                r = self.bstack11lllll11ll_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᔴ"), datetime.now() - bstack11lll11111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11ll111_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᔵ") + str(r) + bstack11ll111_opy_ (u"ࠧࠨᔶ"))
                        return
                    if r.hub_url:
                        f.bstack11lllll1l1l_opy_(instance, driver, r.hub_url)
                        f.bstack1lll11l1111_opy_(instance, bstack1ll111ll1l1_opy_.bstack11llll1lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᔷ"), e)
    def bstack11llll1ll11_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1111ll11_opy_.session_id(driver)
            if session_id:
                bstack11lllll1ll1_opy_ = bstack11ll111_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᔸ").format(session_id)
                bstack1111l1l1l_opy_.mark(bstack11lllll1ll1_opy_)
    def bstack11llll11lll_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lllll11_opy_(instance, bstack1ll111ll1l1_opy_.bstack11lllll11l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1111ll11_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᔹ") + str(hub_url) + bstack11ll111_opy_ (u"ࠤࠥᔺ"))
            return
        framework_session_id = bstack1ll1111ll11_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᔻ") + str(framework_session_id) + bstack11ll111_opy_ (u"ࠦࠧᔼ"))
            return
        if bstack1ll1111ll11_opy_.bstack11llll1l111_opy_(*args) == bstack1ll1111ll11_opy_.bstack11lllll111l_opy_:
            bstack11llll11l1l_opy_ = bstack11ll111_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᔽ").format(framework_session_id)
            bstack11lllll1ll1_opy_ = bstack11ll111_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᔾ").format(framework_session_id)
            bstack1111l1l1l_opy_.end(
                label=bstack11ll111_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᔿ"),
                start=bstack11lllll1ll1_opy_,
                end=bstack11llll11l1l_opy_,
                status=True,
                failure=None
            )
            bstack11lll11111_opy_ = datetime.now()
            r = self.bstack11llll111l1_opy_(
                ref,
                f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᕀ"), datetime.now() - bstack11lll11111_opy_)
            f.bstack1lll11l1111_opy_(instance, bstack1ll111ll1l1_opy_.bstack11lllll11l1_opy_, r.success)
    def bstack1l1111111ll_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lllll11_opy_(instance, bstack1ll111ll1l1_opy_.bstack11llll1111l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1111ll11_opy_.session_id(driver)
        hub_url = bstack1ll1111ll11_opy_.hub_url(driver)
        bstack11lll11111_opy_ = datetime.now()
        r = self.bstack11lllllll1l_opy_(
            ref,
            f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᕁ"), datetime.now() - bstack11lll11111_opy_)
        f.bstack1lll11l1111_opy_(instance, bstack1ll111ll1l1_opy_.bstack11llll1111l_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1l1l1l1l_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l1111ll1ll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11llllll1l1_opy_ = int(driver_rank)
                is_secondary_driver = bstack11llllll1l1_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᕂ") + str(req) + bstack11ll111_opy_ (u"ࠦࠧᕃ"))
        try:
            r = self.bstack1l1llllll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᕄ") + str(r.success) + bstack11ll111_opy_ (u"ࠨࠢᕅ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕆ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᕇ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111111l1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack11lllll11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕈ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᕉ") + str(req) + bstack11ll111_opy_ (u"ࠦࠧᕊ"))
        try:
            r = self.bstack1l1llllll1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᕋ") + str(r.success) + bstack11ll111_opy_ (u"ࠨࠢᕌ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕍ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᕎ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111111111_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack11llll111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕏ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᕐ") + str(req) + bstack11ll111_opy_ (u"ࠦࠧᕑ"))
        try:
            r = self.bstack1l1llllll1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᕒ") + str(r) + bstack11ll111_opy_ (u"ࠨࠢᕓ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕔ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᕕ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1l1l1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack11lllllll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᕖ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᕗ") + str(req) + bstack11ll111_opy_ (u"ࠦࠧᕘ"))
        try:
            r = self.bstack1l1llllll1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᕙ") + str(r) + bstack11ll111_opy_ (u"ࠨࠢᕚ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᕛ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤᕜ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll111lll_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack11llll1llll_opy_(self, instance: bstack1ll1lll1111_opy_, url: str, f: bstack1ll1111ll11_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11llll1l11l_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪᕝ"))
        if bstack11llll1l11l_opy_ is not None:
            browserstack_sdk.bstack1ll1lllll1_opy_ = bstack11llll1l11l_opy_.lower() == bstack11ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨᕞ")
        bstack11lllll1l11_opy_ = version.parse(f.framework_version)
        bstack11lllllllll_opy_ = f.platform_index
        bstack11llllll1ll_opy_ = kwargs.get(bstack11ll111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᕟ"))
        bstack11llll11111_opy_ = kwargs.get(bstack11ll111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕠ"))
        bstack1l111l1111l_opy_ = {}
        bstack11llll111ll_opy_ = {}
        bstack1l111111l11_opy_ = None
        bstack11lllll1lll_opy_ = {}
        if bstack11llll11111_opy_ is not None or bstack11llllll1ll_opy_ is not None: # check top level caps
            if bstack11llll11111_opy_ is not None:
                bstack11lllll1lll_opy_[bstack11ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᕡ")] = bstack11llll11111_opy_
            if bstack11llllll1ll_opy_ is not None and callable(getattr(bstack11llllll1ll_opy_, bstack11ll111_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᕢ"))):
                bstack11lllll1lll_opy_[bstack11ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᕣ")] = bstack11llllll1ll_opy_.to_capabilities()
        response = self.bstack1l1111ll1ll_opy_(bstack11lllllllll_opy_, url, instance.ref(), json.dumps(bstack11lllll1lll_opy_).encode(bstack11ll111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᕤ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1l111l1111l_opy_ = json.loads(response.capabilities.decode(bstack11ll111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᕥ")))
            if browserstack_sdk.bstack1ll1lllll1_opy_:
                def bstack11llll1ll1l_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11llll1ll1l_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1l111l1111l_opy_ = bstack11llll1ll1l_opy_(bstack1l111l1111l_opy_)
                try:
                    bstack11llll1l1ll_opy_ = None
                    if isinstance(bstack1l111l1111l_opy_, dict):
                        if bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᕦ") in bstack1l111l1111l_opy_:
                            bstack11llll1l1ll_opy_ = bstack1l111l1111l_opy_.get(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕧ"))
                        elif isinstance(bstack1l111l1111l_opy_.get(bstack11ll111_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᕨ")), dict):
                            bstack11llll1l1ll_opy_ = bstack1l111l1111l_opy_[bstack11ll111_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᕩ")].get(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᕪ"))
                        if isinstance(bstack11llll1l1ll_opy_, dict) and bstack11ll111_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨᕫ") in bstack11llll1l1ll_opy_:
                            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡖࡪࡳ࡯ࡷ࡫ࡱ࡫ࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡫ࡸ࡯࡮ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡤࡨࡪࡴࡸࡥࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡳࠥ࡮ࡵࡣࠤᕬ"))
                            try:
                                bstack11llll1l1ll_opy_.pop(bstack11ll111_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪᕭ"), None)
                            except Exception:
                                pass
                            if bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕮ") in bstack1l111l1111l_opy_:
                                bstack1l111l1111l_opy_[bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᕯ")] = bstack11llll1l1ll_opy_
                            if isinstance(bstack1l111l1111l_opy_.get(bstack11ll111_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᕰ")), dict):
                                bstack1l111l1111l_opy_[bstack11ll111_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᕱ")][bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᕲ")] = bstack11llll1l1ll_opy_
                except Exception:
                    pass
            if not bstack1l111l1111l_opy_ and not browserstack_sdk.bstack1ll1lllll1_opy_:
                return
            bstack1l111111l11_opy_ = f.bstack1ll1l1l1111_opy_[bstack11ll111_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᕳ")](bstack1l111l1111l_opy_)
        if bstack11llllll1ll_opy_ is not None and bstack11lllll1l11_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᕴ")):
            bstack11llll111ll_opy_ = None
        if (
                not bstack11llllll1ll_opy_ and not bstack11llll11111_opy_
        ) or (
                bstack11lllll1l11_opy_ < version.parse(bstack11ll111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᕵ"))
        ):
            bstack11llll111ll_opy_ = {}
            bstack11llll111ll_opy_.update(bstack1l111l1111l_opy_)
        self.logger.info(bstack11llll11ll_opy_)
        if browserstack_sdk.bstack1ll1lllll1_opy_:
            bstack11llllllll1_opy_ = bstack1l111111l11_opy_ if bstack1l111111l11_opy_ else bstack11llllll1ll_opy_
            if bstack11llllllll1_opy_:
                bstack1l1ll1l1l1_opy_ = bstack111l1ll1l_opy_(bstack11llllllll1_opy_, bstack11l1ll1l1_opy_=bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᕶ"))
                if bstack11llllllll1_opy_ is bstack11llllll1ll_opy_ and not bstack1l111111l11_opy_:
                    bstack1l111111l11_opy_ = bstack11llllllll1_opy_
            kwargs.update({bstack11ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᕷ"): bstack1llllll1l1_opy_})
        elif os.environ.get(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦᕸ")).lower().__eq__(bstack11ll111_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᕹ")):
            kwargs.update({bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᕺ"): f.bstack11llll11ll1_opy_})
        if bstack11lllll1l11_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᕻ")):
            if bstack11llll11111_opy_ is not None:
                del kwargs[bstack11ll111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕼ")]
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᕽ"): bstack1l111111l11_opy_,
                    bstack11ll111_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᕾ"): True,
                    bstack11ll111_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᕿ"): None,
                }
            )
        elif bstack11lllll1l11_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᖀ")):
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᖁ"): bstack11llll111ll_opy_,
                    bstack11ll111_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᖂ"): bstack1l111111l11_opy_,
                    bstack11ll111_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᖃ"): True,
                    bstack11ll111_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᖄ"): None,
                }
            )
        elif bstack11lllll1l11_opy_ >= version.parse(bstack11ll111_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᖅ")):
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᖆ"): bstack11llll111ll_opy_,
                    bstack11ll111_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᖇ"): True,
                    bstack11ll111_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᖈ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11ll111_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᖉ"): bstack11llll111ll_opy_,
                    bstack11ll111_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᖊ"): True,
                    bstack11ll111_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᖋ"): None,
                }
            )