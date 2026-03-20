# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1ll11llllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1ll1l1ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1lllll11l_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
from bstack_utils.bstack1l111l111l_opy_ import bstack1l1l1l1ll1_opy_
import browserstack_sdk
class bstack1l1l1ll11l1_opy_(bstack1l1lllllll1_opy_):
    bstack11ll1l1l1ll_opy_ = bstack11lll1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧ᚛")
    bstack11ll1l1111l_opy_ = bstack11lll1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢ᚜")
    bstack11ll1ll1ll1_opy_ = bstack11lll1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢ᚝")
    def __init__(self, bstack1ll1l1l11ll_opy_):
        super().__init__()
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.PRE), self.bstack11ll1ll1111_opy_)
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.PRE), self.bstack1l11l1l11ll_opy_)
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.POST), self.bstack11ll1lllll1_opy_)
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.POST), self.bstack11ll1l1ll11_opy_)
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.QUIT, bstack11lllll11l_opy_.POST), self.bstack11ll1l1lll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1ll1111_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11lll1_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥ᚞"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11lll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᚟")), str):
                    url = kwargs.get(bstack11lll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᚠ"))
                elif hasattr(kwargs.get(bstack11lll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᚡ")), bstack11lll1_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᚢ")):
                    url = kwargs.get(bstack11lll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᚣ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᚤ"))._url
            except Exception as e:
                url = bstack11lll1_opy_ (u"ࠨࠩᚥ")
                self.logger.error(bstack11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᚦ").format(e))
            self.logger.info(bstack11lll1_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᚧ").format(str(url)))
            bstack11ll11lll1l_opy_ = None
            driver_rank = None
            try:
                bstack11ll11lll1l_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11ll11lll1l_opy_ is not None:
                    bstack11ll11lll11_opy_ = str(bstack11ll11lll1l_opy_)
                    if bstack11lll1_opy_ (u"ࠦࠨࠨᚨ") in bstack11ll11lll11_opy_:
                        bstack11ll1lll11l_opy_ = bstack11ll11lll11_opy_.rsplit(bstack11lll1_opy_ (u"ࠧࠩࠢᚩ"), 1)[1]
                        try:
                            driver_rank = int(bstack11ll1lll11l_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡫ࡸࡵࡴࡤࡧࡹ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱࠠࡧࡴࡲࡱࠥࡲࡡࡣࡧ࡯ࠤࠬࢁࡥࡹࡲ࡯࡭ࡨ࡯ࡴࡠ࡮ࡤࡦࡪࡲࡽࠨ࠼ࠣࠦᚪ") + str(e) + bstack11lll1_opy_ (u"ࠢࠣᚫ"))
            except Exception as e:
                self.logger.debug(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲ࠺ࠡࠤᚬ") + str(e) + bstack11lll1_opy_ (u"ࠤࠥᚭ"))
            self.bstack11ll1llll1l_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack11lll1_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫࠾ࡽࡧࡶ࡮ࡼࡥࡳࡡࡵࡥࡳࡱࡽࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡪ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᚮ") + str(kwargs) + bstack11lll1_opy_ (u"ࠦࠧᚯ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11l1l11ll_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1l1l1111_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11ll1l1l1ll_opy_, False):
            return
        if not f.bstack1ll1lll1l11_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_):
            return
        platform_index = f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_)
        if f.bstack1l11lll11l1_opy_(method_name, *args) and len(args) > 1:
            bstack111ll1l1_opy_ = datetime.now()
            hub_url = bstack1ll111l11ll_opy_.hub_url(driver)
            self.logger.warning(bstack11lll1_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᚰ") + str(hub_url) + bstack11lll1_opy_ (u"ࠨࠢᚱ"))
            bstack11ll1ll1lll_opy_ = args[1][bstack11lll1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᚲ")] if isinstance(args[1], dict) and bstack11lll1_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᚳ") in args[1] else None
            bstack11ll1llll11_opy_ = bstack11lll1_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᚴ")
            if isinstance(bstack11ll1ll1lll_opy_, dict):
                bstack111ll1l1_opy_ = datetime.now()
                r = self.bstack11ll1l11l11_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᚵ"), datetime.now() - bstack111ll1l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11lll1_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᚶ") + str(r) + bstack11lll1_opy_ (u"ࠧࠨᚷ"))
                        return
                    if r.hub_url:
                        f.bstack11ll1l11l1l_opy_(instance, driver, r.hub_url)
                        f.bstack1ll1ll1l1l_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11ll1l1l1ll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11lll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᚸ"), e)
    def bstack11ll1lllll1_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll111l11ll_opy_.session_id(driver)
            if session_id:
                bstack11ll11lllll_opy_ = bstack11lll1_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᚹ").format(session_id)
                bstack1llll11l_opy_.mark(bstack11ll11lllll_opy_)
    def bstack11ll1l1ll11_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1l1l1111_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11ll1l1111l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll111l11ll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11lll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᚺ") + str(hub_url) + bstack11lll1_opy_ (u"ࠤࠥᚻ"))
            return
        framework_session_id = bstack1ll111l11ll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᚼ") + str(framework_session_id) + bstack11lll1_opy_ (u"ࠦࠧᚽ"))
            return
        if bstack1ll111l11ll_opy_.bstack11ll1ll1l11_opy_(*args) == bstack1ll111l11ll_opy_.bstack11ll11llll1_opy_:
            bstack11ll1l1l111_opy_ = bstack11lll1_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᚾ").format(framework_session_id)
            bstack11ll11lllll_opy_ = bstack11lll1_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᚿ").format(framework_session_id)
            bstack1llll11l_opy_.end(
                label=bstack11lll1_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᛀ"),
                start=bstack11ll11lllll_opy_,
                end=bstack11ll1l1l111_opy_,
                status=True,
                failure=None
            )
            bstack111ll1l1_opy_ = datetime.now()
            r = self.bstack11ll1l11lll_opy_(
                ref,
                f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᛁ"), datetime.now() - bstack111ll1l1_opy_)
            f.bstack1ll1ll1l1l_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11ll1l1111l_opy_, r.success)
    def bstack11ll1l1lll1_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1l1l1111_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11ll1ll1ll1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll111l11ll_opy_.session_id(driver)
        hub_url = bstack1ll111l11ll_opy_.hub_url(driver)
        bstack111ll1l1_opy_ = datetime.now()
        r = self.bstack11ll1l1l1l1_opy_(
            ref,
            f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᛂ"), datetime.now() - bstack111ll1l1_opy_)
        f.bstack1ll1ll1l1l_opy_(instance, bstack1l1l1ll11l1_opy_.bstack11ll1ll1ll1_opy_, r.success)
    @measure(event_name=EVENTS.bstack1111l1l11l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11llll1111l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11ll1llllll_opy_ = int(driver_rank)
                is_secondary_driver = bstack11ll1llllll_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᛃ") + str(req) + bstack11lll1_opy_ (u"ࠦࠧᛄ"))
        try:
            r = self.bstack1l1lll11l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᛅ") + str(r.success) + bstack11lll1_opy_ (u"ࠨࠢᛆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᛇ") + str(e) + bstack11lll1_opy_ (u"ࠣࠤᛈ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l111ll_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11ll1l11l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11lll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᛉ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᛊ") + str(req) + bstack11lll1_opy_ (u"ࠦࠧᛋ"))
        try:
            r = self.bstack1l1lll11l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᛌ") + str(r.success) + bstack11lll1_opy_ (u"ࠨࠢᛍ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᛎ") + str(e) + bstack11lll1_opy_ (u"ࠣࠤᛏ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll111111_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11ll1l11lll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11lll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᛐ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᛑ") + str(req) + bstack11lll1_opy_ (u"ࠦࠧᛒ"))
        try:
            r = self.bstack1l1lll11l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᛓ") + str(r) + bstack11lll1_opy_ (u"ࠨࠢᛔ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᛕ") + str(e) + bstack11lll1_opy_ (u"ࠣࠤᛖ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l1ll1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11ll1l1l1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11lll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᛗ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᛘ") + str(req) + bstack11lll1_opy_ (u"ࠦࠧᛙ"))
        try:
            r = self.bstack1l1lll11l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᛚ") + str(r) + bstack11lll1_opy_ (u"ࠨࠢᛛ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᛜ") + str(e) + bstack11lll1_opy_ (u"ࠣࠤᛝ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111l11l1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11ll1llll1l_opy_(self, instance: bstack1ll11llllll_opy_, url: str, f: bstack1ll111l11ll_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11ll1l1l11l_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠩࡒ࡚ࡊࡘࡒࡊࡆࡈࡣࡑࡕࡁࡅࡡࡗࡉࡘ࡚ࡉࡏࡉࠪᛞ"))
        if bstack11ll1l1l11l_opy_ is not None:
            browserstack_sdk.bstack1111lll1ll_opy_ = bstack11ll1l1l11l_opy_.lower() == bstack11lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨᛟ")
        bstack11ll1ll11ll_opy_ = version.parse(f.framework_version)
        bstack11ll1lll111_opy_ = f.platform_index
        bstack11ll1l11111_opy_ = kwargs.get(bstack11lll1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᛠ"))
        bstack11ll1ll11l1_opy_ = kwargs.get(bstack11lll1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᛡ"))
        bstack111llll1_opy_ = {}
        bstack11ll1lll1ll_opy_ = {}
        bstack11ll1ll1l1l_opy_ = None
        bstack11ll1l1llll_opy_ = {}
        if bstack11ll1ll11l1_opy_ is not None or bstack11ll1l11111_opy_ is not None: # check top level caps
            if bstack11ll1ll11l1_opy_ is not None:
                bstack11ll1l1llll_opy_[bstack11lll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛢ")] = bstack11ll1ll11l1_opy_
            if bstack11ll1l11111_opy_ is not None and callable(getattr(bstack11ll1l11111_opy_, bstack11lll1_opy_ (u"ࠢࡵࡱࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᛣ"))):
                bstack11ll1l1llll_opy_[bstack11lll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡤࡷࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛤ")] = bstack11ll1l11111_opy_.to_capabilities()
        response = self.bstack11llll1111l_opy_(bstack11ll1lll111_opy_, url, instance.ref(), json.dumps(bstack11ll1l1llll_opy_).encode(bstack11lll1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᛥ")), driver_rank)
        if response is not None and response.capabilities:
            bstack111llll1_opy_ = json.loads(response.capabilities.decode(bstack11lll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᛦ")))
            if browserstack_sdk.bstack1111lll1ll_opy_:
                def bstack11ll1ll111l_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11ll1ll111l_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack111llll1_opy_ = bstack11ll1ll111l_opy_(bstack111llll1_opy_)
                try:
                    bstack11ll1l111l1_opy_ = None
                    if isinstance(bstack111llll1_opy_, dict):
                        if bstack11lll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᛧ") in bstack111llll1_opy_:
                            bstack11ll1l111l1_opy_ = bstack111llll1_opy_.get(bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛨ"))
                        elif isinstance(bstack111llll1_opy_.get(bstack11lll1_opy_ (u"࠭ࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠫᛩ")), dict):
                            bstack11ll1l111l1_opy_ = bstack111llll1_opy_[bstack11lll1_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᛪ")].get(bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᛫"))
                        if isinstance(bstack11ll1l111l1_opy_, dict) and bstack11lll1_opy_ (u"ࠩࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠨ᛬") in bstack11ll1l111l1_opy_:
                            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡖࡪࡳ࡯ࡷ࡫ࡱ࡫ࠥࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠤ࡫ࡸ࡯࡮ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡤࡨࡪࡴࡸࡥࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡷࡳࠥ࡮ࡵࡣࠤ᛭"))
                            try:
                                bstack11ll1l111l1_opy_.pop(bstack11lll1_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪᛮ"), None)
                            except Exception:
                                pass
                            if bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛯ") in bstack111llll1_opy_:
                                bstack111llll1_opy_[bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᛰ")] = bstack11ll1l111l1_opy_
                            if isinstance(bstack111llll1_opy_.get(bstack11lll1_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᛱ")), dict):
                                bstack111llll1_opy_[bstack11lll1_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᛲ")][bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᛳ")] = bstack11ll1l111l1_opy_
                except Exception:
                    pass
            if not bstack111llll1_opy_ and not browserstack_sdk.bstack1111lll1ll_opy_:
                return
            bstack11ll1ll1l1l_opy_ = f.bstack1l1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᛴ")](bstack111llll1_opy_)
        if bstack11ll1l11111_opy_ is not None and bstack11ll1ll11ll_opy_ >= version.parse(bstack11lll1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᛵ")):
            bstack11ll1lll1ll_opy_ = None
        if (
                not bstack11ll1l11111_opy_ and not bstack11ll1ll11l1_opy_
        ) or (
                bstack11ll1ll11ll_opy_ < version.parse(bstack11lll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᛶ"))
        ):
            bstack11ll1lll1ll_opy_ = {}
            bstack11ll1lll1ll_opy_.update(bstack111llll1_opy_)
        self.logger.info(bstack1ll1l1ll1l_opy_)
        if browserstack_sdk.bstack1111lll1ll_opy_:
            bstack11ll1l11ll1_opy_ = bstack11ll1ll1l1l_opy_ if bstack11ll1ll1l1l_opy_ else bstack11ll1l11111_opy_
            if bstack11ll1l11ll1_opy_:
                bstack11l1ll11l1_opy_ = bstack1l1l1l1ll1_opy_(bstack11ll1l11ll1_opy_, bstack1l1ll1l11l_opy_=bstack11lll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᛷ"))
                if bstack11ll1l11ll1_opy_ is bstack11ll1l11111_opy_ and not bstack11ll1ll1l1l_opy_:
                    bstack11ll1ll1l1l_opy_ = bstack11ll1l11ll1_opy_
            kwargs.update({bstack11lll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᛸ"): bstack1lllll11l_opy_})
        elif os.environ.get(bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦ᛹")).lower().__eq__(bstack11lll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᛺")):
            kwargs.update({bstack11lll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᛻"): f.bstack11ll1lll1l1_opy_})
        if bstack11ll1ll11ll_opy_ >= version.parse(bstack11lll1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ᛼")):
            if bstack11ll1ll11l1_opy_ is not None:
                del kwargs[bstack11lll1_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᛽")]
            kwargs.update(
                {
                    bstack11lll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢ᛾"): bstack11ll1ll1l1l_opy_,
                    bstack11lll1_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦ᛿"): True,
                    bstack11lll1_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᜀ"): None,
                }
            )
        elif bstack11ll1ll11ll_opy_ >= version.parse(bstack11lll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᜁ")):
            kwargs.update(
                {
                    bstack11lll1_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᜂ"): bstack11ll1lll1ll_opy_,
                    bstack11lll1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᜃ"): bstack11ll1ll1l1l_opy_,
                    bstack11lll1_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᜄ"): True,
                    bstack11lll1_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᜅ"): None,
                }
            )
        elif bstack11ll1ll11ll_opy_ >= version.parse(bstack11lll1_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧᜆ")):
            kwargs.update(
                {
                    bstack11lll1_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᜇ"): bstack11ll1lll1ll_opy_,
                    bstack11lll1_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᜈ"): True,
                    bstack11lll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᜉ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11lll1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᜊ"): bstack11ll1lll1ll_opy_,
                    bstack11lll1_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᜋ"): True,
                    bstack11lll1_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᜌ"): None,
                }
            )