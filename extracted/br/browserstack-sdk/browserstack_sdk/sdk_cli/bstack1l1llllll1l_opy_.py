# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack1ll11l1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack111l11l1l1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from bstack_utils.bstack1lllll1lll_opy_ import bstack1l1ll1111l_opy_
import browserstack_sdk
class bstack1ll111l1l11_opy_(bstack1l1llll1l11_opy_):
    bstack11ll1l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣ᚞")
    bstack11ll1llll11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥ᚟")
    bstack11ll1l1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥᚠ")
    def __init__(self, bstack1ll1ll1l1ll_opy_):
        super().__init__()
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack11ll1lll1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11ll1ll1l11_opy_)
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack1l11l1l1l11_opy_)
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.POST), self.bstack11ll1l11l11_opy_)
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.POST), self.bstack11ll1l1111l_opy_)
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.QUIT, bstack1lll1ll11_opy_.POST), self.bstack11ll1l11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1ll1l11_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1lll_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᚡ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1ll1lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᚢ")), str):
                    url = kwargs.get(bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᚣ"))
                elif hasattr(kwargs.get(bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᚤ")), bstack1ll1lll_opy_ (u"ࠨࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠩᚥ")):
                    url = kwargs.get(bstack1ll1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᚦ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᚧ"))._url
            except Exception as e:
                url = bstack1ll1lll_opy_ (u"ࠫࠬᚨ")
                self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡸ࡬ࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࡼࡿࠥᚩ").format(e))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡒࡦ࡯ࡲࡸࡪࠦࡓࡦࡴࡹࡩࡷࠦࡁࡥࡦࡵࡩࡸࡹࠠࡣࡧ࡬ࡲ࡬ࠦࡰࡢࡵࡶࡩࡩࠦࡡࡴࠢ࠽ࠤࢀࢃࠢᚪ").format(str(url)))
            bstack11ll11lllll_opy_ = None
            driver_rank = None
            try:
                bstack11ll11lllll_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11ll11lllll_opy_ is not None:
                    bstack11ll1ll11ll_opy_ = str(bstack11ll11lllll_opy_)
                    if bstack1ll1lll_opy_ (u"ࠢࠤࠤᚫ") in bstack11ll1ll11ll_opy_:
                        bstack11ll1ll1lll_opy_ = bstack11ll1ll11ll_opy_.rsplit(bstack1ll1lll_opy_ (u"ࠣࠥࠥᚬ"), 1)[1]
                        try:
                            driver_rank = int(bstack11ll1ll1lll_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡧࡻࡸࡷࡧࡣࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭ࠣࡪࡷࡵ࡭ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽࡨࡼࡵࡲࡩࡤ࡫ࡷࡣࡱࡧࡢࡦ࡮ࢀࠫ࠿ࠦࠢᚭ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᚮ"))
            except Exception as e:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮࠽ࠤࠧᚯ") + str(e) + bstack1ll1lll_opy_ (u"ࠧࠨᚰ"))
            self.bstack11ll1l111l1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࡁࢀࡪࡲࡪࡸࡨࡶࡤࡸࡡ࡯࡭ࢀࠤࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡦ࠯ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᚱ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠢࠣᚲ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11l1l1l11_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1lll11ll_opy_(instance, bstack1ll111l1l11_opy_.bstack11ll1l1ll11_opy_, False):
            return
        if not f.bstack1ll1l1l1ll1_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_):
            return
        platform_index = f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_)
        if f.bstack1l1l111l11l_opy_(method_name, *args) and len(args) > 1:
            bstack1ll1l111l_opy_ = datetime.now()
            hub_url = bstack1l1llll1111_opy_.hub_url(driver)
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᚳ") + str(hub_url) + bstack1ll1lll_opy_ (u"ࠤࠥᚴ"))
            bstack11ll1llll1l_opy_ = args[1][bstack1ll1lll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᚵ")] if isinstance(args[1], dict) and bstack1ll1lll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᚶ") in args[1] else None
            bstack11ll1l1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᚷ")
            if isinstance(bstack11ll1llll1l_opy_, dict):
                bstack1ll1l111l_opy_ = datetime.now()
                r = self.bstack11ll1ll1ll1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦᚸ"), datetime.now() - bstack1ll1l111l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤᚹ") + str(r) + bstack1ll1lll_opy_ (u"ࠣࠤᚺ"))
                        return
                    if r.hub_url:
                        f.bstack11ll11llll1_opy_(instance, driver, r.hub_url)
                        f.bstack1l1l11lll_opy_(instance, bstack1ll111l1l11_opy_.bstack11ll1l1ll11_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᚻ"), e)
    def bstack11ll1l11l11_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l1llll1111_opy_.session_id(driver)
            if session_id:
                bstack11ll1l1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᚼ").format(session_id)
                bstack1lll1lll11_opy_.mark(bstack11ll1l1l11l_opy_)
    def bstack11ll1l1111l_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lll11ll_opy_(instance, bstack1ll111l1l11_opy_.bstack11ll1llll11_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l1llll1111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᚽ") + str(hub_url) + bstack1ll1lll_opy_ (u"ࠧࠨᚾ"))
            return
        framework_session_id = bstack1l1llll1111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᚿ") + str(framework_session_id) + bstack1ll1lll_opy_ (u"ࠢࠣᛀ"))
            return
        if bstack1l1llll1111_opy_.bstack11ll1l11ll1_opy_(*args) == bstack1l1llll1111_opy_.bstack11ll1lll111_opy_:
            bstack11ll1ll111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣᛁ").format(framework_session_id)
            bstack11ll1l1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᛂ").format(framework_session_id)
            bstack1lll1lll11_opy_.end(
                label=bstack1ll1lll_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨᛃ"),
                start=bstack11ll1l1l11l_opy_,
                end=bstack11ll1ll111l_opy_,
                status=True,
                failure=None
            )
            bstack1ll1l111l_opy_ = datetime.now()
            r = self.bstack11ll1l111ll_opy_(
                ref,
                f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥᛄ"), datetime.now() - bstack1ll1l111l_opy_)
            f.bstack1l1l11lll_opy_(instance, bstack1ll111l1l11_opy_.bstack11ll1llll11_opy_, r.success)
    def bstack11ll1l11111_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lll11ll_opy_(instance, bstack1ll111l1l11_opy_.bstack11ll1l1ll1l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l1llll1111_opy_.session_id(driver)
        hub_url = bstack1l1llll1111_opy_.hub_url(driver)
        bstack1ll1l111l_opy_ = datetime.now()
        r = self.bstack11ll1l11l1l_opy_(
            ref,
            f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥᛅ"), datetime.now() - bstack1ll1l111l_opy_)
        f.bstack1l1l11lll_opy_(instance, bstack1ll111l1l11_opy_.bstack11ll1l1ll1l_opy_, r.success)
    @measure(event_name=EVENTS.bstack111ll1l11_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11lll1l1l1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11ll1ll11l1_opy_ = int(driver_rank)
                is_secondary_driver = bstack11ll1ll11l1_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᛆ") + str(req) + bstack1ll1lll_opy_ (u"ࠢࠣᛇ"))
        try:
            r = self.bstack1l1ll1l1ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᛈ") + str(r.success) + bstack1ll1lll_opy_ (u"ࠤࠥᛉ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᛊ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᛋ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll11ll1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11ll1ll1ll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l11l1ll111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᛌ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᛍ") + str(req) + bstack1ll1lll_opy_ (u"ࠢࠣᛎ"))
        try:
            r = self.bstack1l1ll1l1ll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᛏ") + str(r.success) + bstack1ll1lll_opy_ (u"ࠤࠥᛐ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᛑ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᛒ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l1l1ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11ll1l111ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11l1ll111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᛓ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤᛔ") + str(req) + bstack1ll1lll_opy_ (u"ࠢࠣᛕ"))
        try:
            r = self.bstack1l1ll1l1ll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᛖ") + str(r) + bstack1ll1lll_opy_ (u"ࠤࠥᛗ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᛘ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᛙ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll11ll1l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11ll1l11l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11l1ll111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᛚ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࡀࠠࠣᛛ") + str(req) + bstack1ll1lll_opy_ (u"ࠢࠣᛜ"))
        try:
            r = self.bstack1l1ll1l1ll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᛝ") + str(r) + bstack1ll1lll_opy_ (u"ࠤࠥᛞ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᛟ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᛠ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1111l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11ll1l111l1_opy_(self, instance: bstack1ll11l1l111_opy_, url: str, f: bstack1l1llll1111_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11ll1l11lll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ᛡ"))
        if bstack11ll1l11lll_opy_ is not None:
            browserstack_sdk.bstack1111l1l1l1_opy_ = bstack11ll1l11lll_opy_.lower() == bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫᛢ")
        bstack11ll1l1l1l1_opy_ = version.parse(f.framework_version)
        bstack11ll11ll11l_opy_ = f.platform_index
        bstack11ll1l1llll_opy_ = kwargs.get(bstack1ll1lll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᛣ"))
        bstack11ll1ll1111_opy_ = kwargs.get(bstack1ll1lll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᛤ"))
        bstack1ll1111lll_opy_ = {}
        bstack11ll11lll1l_opy_ = {}
        bstack11ll1lll11l_opy_ = None
        bstack11ll1l1l111_opy_ = {}
        if bstack11ll1ll1111_opy_ is not None or bstack11ll1l1llll_opy_ is not None: # check top level caps
            if bstack11ll1ll1111_opy_ is not None:
                bstack11ll1l1l111_opy_[bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᛥ")] = bstack11ll1ll1111_opy_
            if bstack11ll1l1llll_opy_ is not None and callable(getattr(bstack11ll1l1llll_opy_, bstack1ll1lll_opy_ (u"ࠥࡸࡴࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᛦ"))):
                bstack11ll1l1l111_opy_[bstack1ll1lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࡤࡧࡳࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᛧ")] = bstack11ll1l1llll_opy_.to_capabilities()
        response = self.bstack11lll1l1l1l_opy_(bstack11ll11ll11l_opy_, url, instance.ref(), json.dumps(bstack11ll1l1l111_opy_).encode(bstack1ll1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᛨ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1ll1111lll_opy_ = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᛩ")))
            if browserstack_sdk.bstack1111l1l1l1_opy_:
                def bstack11ll1lll1l1_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11ll1lll1l1_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1ll1111lll_opy_ = bstack11ll1lll1l1_opy_(bstack1ll1111lll_opy_)
                try:
                    bstack11ll11lll11_opy_ = None
                    if isinstance(bstack1ll1111lll_opy_, dict):
                        if bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᛪ") in bstack1ll1111lll_opy_:
                            bstack11ll11lll11_opy_ = bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᛫"))
                        elif isinstance(bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧ᛬")), dict):
                            bstack11ll11lll11_opy_ = bstack1ll1111lll_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨ᛭")].get(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᛮ"))
                        if isinstance(bstack11ll11lll11_opy_, dict) and bstack1ll1lll_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᛯ") in bstack11ll11lll11_opy_:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡒࡦ࡯ࡲࡺ࡮ࡴࡧࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡴࡲࡱࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡧ࡫ࡦࡰࡴࡨࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺ࡯ࠡࡪࡸࡦࠧᛰ"))
                            try:
                                bstack11ll11lll11_opy_.pop(bstack1ll1lll_opy_ (u"ࠧࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬࠭ᛱ"), None)
                            except Exception:
                                pass
                            if bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᛲ") in bstack1ll1111lll_opy_:
                                bstack1ll1111lll_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᛳ")] = bstack11ll11lll11_opy_
                            if isinstance(bstack1ll1111lll_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᛴ")), dict):
                                bstack1ll1111lll_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᛵ")][bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛶ")] = bstack11ll11lll11_opy_
                except Exception:
                    pass
            if not bstack1ll1111lll_opy_ and not browserstack_sdk.bstack1111l1l1l1_opy_:
                return
            bstack11ll1lll11l_opy_ = f.bstack1l1lll111ll_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᛷ")](bstack1ll1111lll_opy_)
        if bstack11ll1l1llll_opy_ is not None and bstack11ll1l1l1l1_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᛸ")):
            bstack11ll11lll1l_opy_ = None
        if (
                not bstack11ll1l1llll_opy_ and not bstack11ll1ll1111_opy_
        ) or (
                bstack11ll1l1l1l1_opy_ < version.parse(bstack1ll1lll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ᛹"))
        ):
            bstack11ll11lll1l_opy_ = {}
            bstack11ll11lll1l_opy_.update(bstack1ll1111lll_opy_)
        self.logger.info(bstack111ll1ll_opy_)
        if browserstack_sdk.bstack1111l1l1l1_opy_:
            bstack11ll1ll1l1l_opy_ = bstack11ll1lll11l_opy_ if bstack11ll1lll11l_opy_ else bstack11ll1l1llll_opy_
            if bstack11ll1ll1l1l_opy_:
                bstack1l11l1lll_opy_ = bstack1l1ll1111l_opy_(bstack11ll1ll1l1l_opy_, bstack111ll1lll_opy_=bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤ᛺"))
                if bstack11ll1ll1l1l_opy_ is bstack11ll1l1llll_opy_ and not bstack11ll1lll11l_opy_:
                    bstack11ll1lll11l_opy_ = bstack11ll1ll1l1l_opy_
            kwargs.update({bstack1ll1lll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᛻"): bstack111l11l1l1_opy_})
        elif os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢ᛼")).lower().__eq__(bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᛽")):
            kwargs.update({bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᛾"): f.bstack11ll1lll1ll_opy_})
        if bstack11ll1l1l1l1_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧ᛿")):
            if bstack11ll1ll1111_opy_ is not None:
                del kwargs[bstack1ll1lll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᜀ")]
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᜁ"): bstack11ll1lll11l_opy_,
                    bstack1ll1lll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᜂ"): True,
                    bstack1ll1lll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᜃ"): None,
                }
            )
        elif bstack11ll1l1l1l1_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᜄ")):
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᜅ"): bstack11ll11lll1l_opy_,
                    bstack1ll1lll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᜆ"): bstack11ll1lll11l_opy_,
                    bstack1ll1lll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᜇ"): True,
                    bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᜈ"): None,
                }
            )
        elif bstack11ll1l1l1l1_opy_ >= version.parse(bstack1ll1lll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᜉ")):
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᜊ"): bstack11ll11lll1l_opy_,
                    bstack1ll1lll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᜋ"): True,
                    bstack1ll1lll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᜌ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll1lll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᜍ"): bstack11ll11lll1l_opy_,
                    bstack1ll1lll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᜎ"): True,
                    bstack1ll1lll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᜏ"): None,
                }
            )