# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack1l1ll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111ll1l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1l111l11ll_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from bstack_utils.bstack1lll1l1ll_opy_ import bstack11l1l11l1_opy_
import browserstack_sdk
class bstack1l1l1ll11l1_opy_(bstack1l1l1111111_opy_):
    bstack11l1l111ll1_opy_ = bstack1l1111l_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣ᠘")
    bstack11l11l1llll_opy_ = bstack1l1111l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥ᠙")
    bstack11l11lll1ll_opy_ = bstack1l1111l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥ᠚")
    def __init__(self, bstack1ll111111ll_opy_):
        super().__init__()
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1lll1l111_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l11ll1l1l_opy_)
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.PRE), self.bstack11llll11l1l_opy_)
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.POST), self.bstack11l11llll1l_opy_)
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.POST), self.bstack11l11ll11l1_opy_)
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.QUIT, bstack1111llll1l_opy_.POST), self.bstack11l1l1l111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11ll1l1l_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111l_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨ᠛"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᠜")), str):
                    url = kwargs.get(bstack1l1111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᠝"))
                elif hasattr(kwargs.get(bstack1l1111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ᠞")), bstack1l1111l_opy_ (u"ࠨࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠩ᠟")):
                    url = kwargs.get(bstack1l1111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᠠ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᠡ"))._url
            except Exception as e:
                url = bstack1l1111l_opy_ (u"ࠫࠬᠢ")
                self.logger.error(bstack1l1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡸ࡬ࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࡼࡿࠥᠣ").format(e))
            self.logger.info(bstack1l1111l_opy_ (u"ࠨࡒࡦ࡯ࡲࡸࡪࠦࡓࡦࡴࡹࡩࡷࠦࡁࡥࡦࡵࡩࡸࡹࠠࡣࡧ࡬ࡲ࡬ࠦࡰࡢࡵࡶࡩࡩࠦࡡࡴࠢ࠽ࠤࢀࢃࠢᠤ").format(str(url)))
            bstack11l11llll11_opy_ = None
            driver_rank = None
            try:
                bstack11l11llll11_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11l11llll11_opy_ is not None:
                    bstack11l1l1111ll_opy_ = str(bstack11l11llll11_opy_)
                    if bstack1l1111l_opy_ (u"ࠢࠤࠤᠥ") in bstack11l1l1111ll_opy_:
                        bstack11l1l111l11_opy_ = bstack11l1l1111ll_opy_.rsplit(bstack1l1111l_opy_ (u"ࠣࠥࠥᠦ"), 1)[1]
                        try:
                            driver_rank = int(bstack11l1l111l11_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡧࡻࡸࡷࡧࡣࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭ࠣࡪࡷࡵ࡭ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽࡨࡼࡵࡲࡩࡤ࡫ࡷࡣࡱࡧࡢࡦ࡮ࢀࠫ࠿ࠦࠢᠧ") + str(e) + bstack1l1111l_opy_ (u"ࠥࠦᠨ"))
            except Exception as e:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮࠽ࠤࠧᠩ") + str(e) + bstack1l1111l_opy_ (u"ࠧࠨᠪ"))
            self.bstack11l11ll1ll1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1l1111l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࡁࢀࡪࡲࡪࡸࡨࡶࡤࡸࡡ࡯࡭ࢀࠤࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡦ࠯ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᠫ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠢࠣᠬ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11llll11l1l_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11l1l111ll1_opy_, False):
            return
        if not f.bstack1l1lll1l111_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_):
            return
        platform_index = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_)
        if f.bstack1l111l1llll_opy_(method_name, *args) and len(args) > 1:
            bstack11l11l1l_opy_ = datetime.now()
            hub_url = bstack1l1l111l111_opy_.hub_url(driver)
            self.logger.warning(bstack1l1111l_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᠭ") + str(hub_url) + bstack1l1111l_opy_ (u"ࠤࠥᠮ"))
            bstack11l1l1111l1_opy_ = args[1][bstack1l1111l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᠯ")] if isinstance(args[1], dict) and bstack1l1111l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᠰ") in args[1] else None
            bstack11l1l111lll_opy_ = bstack1l1111l_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᠱ")
            if isinstance(bstack11l1l1111l1_opy_, dict):
                bstack11l11l1l_opy_ = datetime.now()
                r = self.bstack11l1l11l111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦᠲ"), datetime.now() - bstack11l11l1l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1111l_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤᠳ") + str(r) + bstack1l1111l_opy_ (u"ࠣࠤᠴ"))
                        return
                    if r.hub_url:
                        f.bstack11l11lllll1_opy_(instance, driver, r.hub_url)
                        f.bstack111l1llll1_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11l1l111ll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᠵ"), e)
    def bstack11l11llll1l_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l1l111l111_opy_.session_id(driver)
            if session_id:
                bstack11l1l111111_opy_ = bstack1l1111l_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᠶ").format(session_id)
                bstack11lll1111_opy_.mark(bstack11l1l111111_opy_)
    def bstack11l11ll11l1_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11l11l1llll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l1l111l111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᠷ") + str(hub_url) + bstack1l1111l_opy_ (u"ࠧࠨᠸ"))
            return
        framework_session_id = bstack1l1l111l111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᠹ") + str(framework_session_id) + bstack1l1111l_opy_ (u"ࠢࠣᠺ"))
            return
        if bstack1l1l111l111_opy_.bstack11l1l11l1ll_opy_(*args) == bstack1l1l111l111_opy_.bstack11l11lll111_opy_:
            bstack11l1l11l1l1_opy_ = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣᠻ").format(framework_session_id)
            bstack11l1l111111_opy_ = bstack1l1111l_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᠼ").format(framework_session_id)
            bstack11lll1111_opy_.end(
                label=bstack1l1111l_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨᠽ"),
                start=bstack11l1l111111_opy_,
                end=bstack11l1l11l1l1_opy_,
                status=True,
                failure=None
            )
            bstack11l11l1l_opy_ = datetime.now()
            r = self.bstack11l1l1l11l1_opy_(
                ref,
                f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥᠾ"), datetime.now() - bstack11l11l1l_opy_)
            f.bstack111l1llll1_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11l11l1llll_opy_, r.success)
    def bstack11l1l1l111l_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11l11lll1ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l1l111l111_opy_.session_id(driver)
        hub_url = bstack1l1l111l111_opy_.hub_url(driver)
        bstack11l11l1l_opy_ = datetime.now()
        r = self.bstack11l11ll1lll_opy_(
            ref,
            f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥᠿ"), datetime.now() - bstack11l11l1l_opy_)
        f.bstack111l1llll1_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11l11lll1ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack111l1111_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11l1ll1lll1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11l1l11111l_opy_ = int(driver_rank)
                is_secondary_driver = bstack11l1l11111l_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᡀ") + str(req) + bstack1l1111l_opy_ (u"ࠢࠣᡁ"))
        try:
            r = self.bstack11l1ll1lll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᡂ") + str(r.success) + bstack1l1111l_opy_ (u"ࠤࠥᡃ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᡄ") + str(e) + bstack1l1111l_opy_ (u"ࠦࠧᡅ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l11lll1_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11l1l11l111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᡆ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᡇ") + str(req) + bstack1l1111l_opy_ (u"ࠢࠣᡈ"))
        try:
            r = self.bstack11l1ll1lll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᡉ") + str(r.success) + bstack1l1111l_opy_ (u"ࠤࠥᡊ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᡋ") + str(e) + bstack1l1111l_opy_ (u"ࠦࠧᡌ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l111l1l_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11l1l1l11l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᡍ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤᡎ") + str(req) + bstack1l1111l_opy_ (u"ࠢࠣᡏ"))
        try:
            r = self.bstack11l1ll1lll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᡐ") + str(r) + bstack1l1111l_opy_ (u"ࠤࠥᡑ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᡒ") + str(e) + bstack1l1111l_opy_ (u"ࠦࠧᡓ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l11ll11ll_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11l11ll1lll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᡔ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࡀࠠࠣᡕ") + str(req) + bstack1l1111l_opy_ (u"ࠢࠣᡖ"))
        try:
            r = self.bstack11l1ll1lll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᡗ") + str(r) + bstack1l1111l_opy_ (u"ࠤࠥᡘ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᡙ") + str(e) + bstack1l1111l_opy_ (u"ࠦࠧᡚ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111l11l1ll_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11l11ll1ll1_opy_(self, instance: bstack1l1ll11l1ll_opy_, url: str, f: bstack1l1l111l111_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11l1l11llll_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ᡛ"))
        if bstack11l1l11llll_opy_ is not None:
            browserstack_sdk.bstack111l1ll11l_opy_ = bstack11l1l11llll_opy_.lower() == bstack1l1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫᡜ")
        bstack11l11ll1111_opy_ = version.parse(f.framework_version)
        bstack11l11l1lll1_opy_ = f.platform_index
        bstack11l1l1l1111_opy_ = kwargs.get(bstack1l1111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᡝ"))
        bstack11l11lll1l1_opy_ = kwargs.get(bstack1l1111l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᡞ"))
        bstack11111l1l1l_opy_ = {}
        bstack11l11ll111l_opy_ = {}
        bstack11l1l11ll1l_opy_ = None
        bstack11l11ll1l11_opy_ = {}
        if bstack11l11lll1l1_opy_ is not None or bstack11l1l1l1111_opy_ is not None: # check top level caps
            if bstack11l11lll1l1_opy_ is not None:
                bstack11l11ll1l11_opy_[bstack1l1111l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᡟ")] = bstack11l11lll1l1_opy_
            if bstack11l1l1l1111_opy_ is not None and callable(getattr(bstack11l1l1l1111_opy_, bstack1l1111l_opy_ (u"ࠥࡸࡴࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᡠ"))):
                bstack11l11ll1l11_opy_[bstack1l1111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࡤࡧࡳࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡡ")] = bstack11l1l1l1111_opy_.to_capabilities()
        response = self.bstack11l1ll1lll1_opy_(bstack11l11l1lll1_opy_, url, instance.ref(), json.dumps(bstack11l11ll1l11_opy_).encode(bstack1l1111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᡢ")), driver_rank)
        if response is not None and response.capabilities:
            bstack11111l1l1l_opy_ = json.loads(response.capabilities.decode(bstack1l1111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᡣ")))
            if browserstack_sdk.bstack111l1ll11l_opy_:
                def bstack11l11llllll_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l11llllll_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack11111l1l1l_opy_ = bstack11l11llllll_opy_(bstack11111l1l1l_opy_)
                try:
                    bstack11l1l11l11l_opy_ = None
                    if isinstance(bstack11111l1l1l_opy_, dict):
                        if bstack1l1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᡤ") in bstack11111l1l1l_opy_:
                            bstack11l1l11l11l_opy_ = bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᡥ"))
                        elif isinstance(bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᡦ")), dict):
                            bstack11l1l11l11l_opy_ = bstack11111l1l1l_opy_[bstack1l1111l_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᡧ")].get(bstack1l1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᡨ"))
                        if isinstance(bstack11l1l11l11l_opy_, dict) and bstack1l1111l_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᡩ") in bstack11l1l11l11l_opy_:
                            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡒࡦ࡯ࡲࡺ࡮ࡴࡧࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡴࡲࡱࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡧ࡫ࡦࡰࡴࡨࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺ࡯ࠡࡪࡸࡦࠧᡪ"))
                            try:
                                bstack11l1l11l11l_opy_.pop(bstack1l1111l_opy_ (u"ࠧࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬࠭ᡫ"), None)
                            except Exception:
                                pass
                            if bstack1l1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᡬ") in bstack11111l1l1l_opy_:
                                bstack11111l1l1l_opy_[bstack1l1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᡭ")] = bstack11l1l11l11l_opy_
                            if isinstance(bstack11111l1l1l_opy_.get(bstack1l1111l_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᡮ")), dict):
                                bstack11111l1l1l_opy_[bstack1l1111l_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᡯ")][bstack1l1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡰ")] = bstack11l1l11l11l_opy_
                except Exception:
                    pass
            if not bstack11111l1l1l_opy_ and not browserstack_sdk.bstack111l1ll11l_opy_:
                return
            bstack11l1l11ll1l_opy_ = f.bstack1l11lll1l11_opy_[bstack1l1111l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᡱ")](bstack11111l1l1l_opy_)
        if bstack11l1l1l1111_opy_ is not None and bstack11l11ll1111_opy_ >= version.parse(bstack1l1111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᡲ")):
            bstack11l11ll111l_opy_ = None
        if (
                not bstack11l1l1l1111_opy_ and not bstack11l11lll1l1_opy_
        ) or (
                bstack11l11ll1111_opy_ < version.parse(bstack1l1111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᡳ"))
        ):
            bstack11l11ll111l_opy_ = {}
            bstack11l11ll111l_opy_.update(bstack11111l1l1l_opy_)
        self.logger.info(bstack111ll1l1l1_opy_)
        if browserstack_sdk.bstack111l1ll11l_opy_:
            bstack11l1l11ll11_opy_ = bstack11l1l11ll1l_opy_ if bstack11l1l11ll1l_opy_ else bstack11l1l1l1111_opy_
            if bstack11l1l11ll11_opy_:
                bstack1ll1l11111_opy_ = bstack11l1l11l1_opy_(bstack11l1l11ll11_opy_, bstack1llllllll1l_opy_=bstack1l1111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᡴ"))
                if bstack11l1l11ll11_opy_ is bstack11l1l1l1111_opy_ and not bstack11l1l11ll1l_opy_:
                    bstack11l1l11ll1l_opy_ = bstack11l1l11ll11_opy_
            kwargs.update({bstack1l1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᡵ"): bstack1l111l11ll_opy_})
        elif os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᡶ")).lower().__eq__(bstack1l1111l_opy_ (u"ࠧࡺࡲࡶࡧࠥᡷ")):
            kwargs.update({bstack1l1111l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᡸ"): f.bstack11l11lll11l_opy_})
        if bstack11l11ll1111_opy_ >= version.parse(bstack1l1111l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ᡹")):
            if bstack11l11lll1l1_opy_ is not None:
                del kwargs[bstack1l1111l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᡺")]
            kwargs.update(
                {
                    bstack1l1111l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥ᡻"): bstack11l1l11ll1l_opy_,
                    bstack1l1111l_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢ᡼"): True,
                    bstack1l1111l_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦ᡽"): None,
                }
            )
        elif bstack11l11ll1111_opy_ >= version.parse(bstack1l1111l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ᡾")):
            kwargs.update(
                {
                    bstack1l1111l_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᡿"): bstack11l11ll111l_opy_,
                    bstack1l1111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᢀ"): bstack11l1l11ll1l_opy_,
                    bstack1l1111l_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᢁ"): True,
                    bstack1l1111l_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᢂ"): None,
                }
            )
        elif bstack11l11ll1111_opy_ >= version.parse(bstack1l1111l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᢃ")):
            kwargs.update(
                {
                    bstack1l1111l_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᢄ"): bstack11l11ll111l_opy_,
                    bstack1l1111l_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᢅ"): True,
                    bstack1l1111l_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᢆ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1111l_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᢇ"): bstack11l11ll111l_opy_,
                    bstack1l1111l_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᢈ"): True,
                    bstack1l1111l_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᢉ"): None,
                }
            )