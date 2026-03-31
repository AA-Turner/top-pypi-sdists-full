# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack1ll111lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l1111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack111l11lll1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from bstack_utils.bstack1ll1ll11_opy_ import bstack1lll11l11l_opy_
import browserstack_sdk
class bstack1l1lllll11l_opy_(bstack1ll111l11ll_opy_):
    bstack11ll1l11ll1_opy_ = bstack1ll11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢᛇ")
    bstack11ll11l1111_opy_ = bstack1ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᛈ")
    bstack11ll1l11111_opy_ = bstack1ll11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᛉ")
    def __init__(self, bstack1ll1ll111l1_opy_):
        super().__init__()
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11ll11l111l_opy_)
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack1l11l111l11_opy_)
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.POST), self.bstack11ll1l111l1_opy_)
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.POST), self.bstack11ll1l1l1ll_opy_)
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.QUIT, bstack1ll11ll1ll_opy_.POST), self.bstack11ll1ll1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll11l111l_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll11_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧᛊ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᛋ")), str):
                    url = kwargs.get(bstack1ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᛌ"))
                elif hasattr(kwargs.get(bstack1ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᛍ")), bstack1ll11_opy_ (u"ࠧࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠨᛎ")):
                    url = kwargs.get(bstack1ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᛏ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᛐ"))._url
            except Exception as e:
                url = bstack1ll11_opy_ (u"ࠪࠫᛑ")
                self.logger.error(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡷࡲࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠿ࠦࡻࡾࠤᛒ").format(e))
            self.logger.info(bstack1ll11_opy_ (u"ࠧࡘࡥ࡮ࡱࡷࡩ࡙ࠥࡥࡳࡸࡨࡶࠥࡇࡤࡥࡴࡨࡷࡸࠦࡢࡦ࡫ࡱ࡫ࠥࡶࡡࡴࡵࡨࡨࠥࡧࡳࠡ࠼ࠣࡿࢂࠨᛓ").format(str(url)))
            bstack11ll11lllll_opy_ = None
            driver_rank = None
            try:
                bstack11ll11lllll_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11ll11lllll_opy_ is not None:
                    bstack11ll1l1l11l_opy_ = str(bstack11ll11lllll_opy_)
                    if bstack1ll11_opy_ (u"ࠨࠣࠣᛔ") in bstack11ll1l1l11l_opy_:
                        bstack11ll11l1ll1_opy_ = bstack11ll1l1l11l_opy_.rsplit(bstack1ll11_opy_ (u"ࠢࠤࠤᛕ"), 1)[1]
                        try:
                            driver_rank = int(bstack11ll11l1ll1_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡦࡺࡷࡶࡦࡩࡴࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡷࡧ࡮࡬ࠢࡩࡶࡴࡳࠠ࡭ࡣࡥࡩࡱࠦࠧࡼࡧࡻࡴࡱ࡯ࡣࡪࡶࡢࡰࡦࡨࡥ࡭ࡿࠪ࠾ࠥࠨᛖ") + str(e) + bstack1ll11_opy_ (u"ࠤࠥᛗ"))
            except Exception as e:
                self.logger.debug(bstack1ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭࠼ࠣࠦᛘ") + str(e) + bstack1ll11_opy_ (u"ࠦࠧᛙ"))
            self.bstack11ll11llll1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1ll11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤࡸࡡ࡯࡭ࡀࡿࡩࡸࡩࡷࡧࡵࡣࡷࡧ࡮࡬ࡿࠣࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀ࡬࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾ࠼ࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᛚ") + str(kwargs) + bstack1ll11_opy_ (u"ࠨࠢᛛ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l11l111l11_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lllll11l_opy_.bstack11ll1l11ll1_opy_, False):
            return
        if not f.bstack1ll1ll11111_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_):
            return
        platform_index = f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_)
        if f.bstack1l11ll1l1ll_opy_(method_name, *args) and len(args) > 1:
            bstack11l111ll1_opy_ = datetime.now()
            hub_url = bstack1ll11111111_opy_.hub_url(driver)
            self.logger.warning(bstack1ll11_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᛜ") + str(hub_url) + bstack1ll11_opy_ (u"ࠣࠤᛝ"))
            bstack11ll11lll11_opy_ = args[1][bstack1ll11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᛞ")] if isinstance(args[1], dict) and bstack1ll11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᛟ") in args[1] else None
            bstack11ll1l1l111_opy_ = bstack1ll11_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᛠ")
            if isinstance(bstack11ll11lll11_opy_, dict):
                bstack11l111ll1_opy_ = datetime.now()
                r = self.bstack11ll1l111ll_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥᛡ"), datetime.now() - bstack11l111ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll11_opy_ (u"ࠨࡳࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࡀࠠࠣᛢ") + str(r) + bstack1ll11_opy_ (u"ࠢࠣᛣ"))
                        return
                    if r.hub_url:
                        f.bstack11ll11lll1l_opy_(instance, driver, r.hub_url)
                        f.bstack1l11lllll_opy_(instance, bstack1l1lllll11l_opy_.bstack11ll1l11ll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᛤ"), e)
    def bstack11ll1l111l1_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll11111111_opy_.session_id(driver)
            if session_id:
                bstack11ll11ll1l1_opy_ = bstack1ll11_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᛥ").format(session_id)
                bstack11ll11l1ll_opy_.mark(bstack11ll11ll1l1_opy_)
    def bstack11ll1l1l1ll_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lllll11l_opy_.bstack11ll11l1111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll11111111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᛦ") + str(hub_url) + bstack1ll11_opy_ (u"ࠦࠧᛧ"))
            return
        framework_session_id = bstack1ll11111111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࠣᛨ") + str(framework_session_id) + bstack1ll11_opy_ (u"ࠨࠢᛩ"))
            return
        if bstack1ll11111111_opy_.bstack11ll11l1l11_opy_(*args) == bstack1ll11111111_opy_.bstack11ll1l11lll_opy_:
            bstack11ll1l1111l_opy_ = bstack1ll11_opy_ (u"ࠢࡼࡿ࠽ࡩࡳࡪࠢᛪ").format(framework_session_id)
            bstack11ll11ll1l1_opy_ = bstack1ll11_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥ᛫").format(framework_session_id)
            bstack11ll11l1ll_opy_.end(
                label=bstack1ll11_opy_ (u"ࠤࡶࡨࡰࡀࡤࡳ࡫ࡹࡩࡷࡀࡰࡰࡵࡷ࠱࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠧ᛬"),
                start=bstack11ll11ll1l1_opy_,
                end=bstack11ll1l1111l_opy_,
                status=True,
                failure=None
            )
            bstack11l111ll1_opy_ = datetime.now()
            r = self.bstack11ll111llll_opy_(
                ref,
                f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤ᛭"), datetime.now() - bstack11l111ll1_opy_)
            f.bstack1l11lllll_opy_(instance, bstack1l1lllll11l_opy_.bstack11ll11l1111_opy_, r.success)
    def bstack11ll1ll1111_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lllll11l_opy_.bstack11ll1l11111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll11111111_opy_.session_id(driver)
        hub_url = bstack1ll11111111_opy_.hub_url(driver)
        bstack11l111ll1_opy_ = datetime.now()
        r = self.bstack11ll11ll111_opy_(
            ref,
            f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᛮ"), datetime.now() - bstack11l111ll1_opy_)
        f.bstack1l11lllll_opy_(instance, bstack1l1lllll11l_opy_.bstack11ll1l11111_opy_, r.success)
    @measure(event_name=EVENTS.bstack1ll111111_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11lll1l1l11_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11ll1ll111l_opy_ = int(driver_rank)
                is_secondary_driver = bstack11ll1ll111l_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥᛯ") + str(req) + bstack1ll11_opy_ (u"ࠨࠢᛰ"))
        try:
            r = self.bstack1l1ll1ll111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᛱ") + str(r.success) + bstack1ll11_opy_ (u"ࠣࠤᛲ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᛳ") + str(e) + bstack1ll11_opy_ (u"ࠥࠦᛴ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll11ll11l_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11ll1l111ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᛵ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᛶ") + str(req) + bstack1ll11_opy_ (u"ࠨࠢᛷ"))
        try:
            r = self.bstack1l1ll1ll111_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࡵࡸࡧࡨ࡫ࡳࡴ࠿ࠥᛸ") + str(r.success) + bstack1ll11_opy_ (u"ࠣࠤ᛹"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ᛺") + str(e) + bstack1ll11_opy_ (u"ࠥࠦ᛻"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1l11l1l_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11ll111llll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ᛼").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣ᛽") + str(req) + bstack1ll11_opy_ (u"ࠨࠢ᛾"))
        try:
            r = self.bstack1l1ll1ll111_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤ᛿") + str(r) + bstack1ll11_opy_ (u"ࠣࠤᜀ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᜁ") + str(e) + bstack1ll11_opy_ (u"ࠥࠦᜂ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll11l11l1_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11ll11ll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᜃ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴ࠿ࠦࠢᜄ") + str(req) + bstack1ll11_opy_ (u"ࠨࠢᜅ"))
        try:
            r = self.bstack1l1ll1ll111_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᜆ") + str(r) + bstack1ll11_opy_ (u"ࠣࠤᜇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᜈ") + str(e) + bstack1ll11_opy_ (u"ࠥࠦᜉ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1ll111_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11ll11llll1_opy_(self, instance: bstack1ll111lllll_opy_, url: str, f: bstack1ll11111111_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11ll11ll1ll_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠫࡔ࡜ࡅࡓࡔࡌࡈࡊࡥࡌࡐࡃࡇࡣ࡙ࡋࡓࡕࡋࡑࡋࠬᜊ"))
        if bstack11ll11ll1ll_opy_ is not None:
            browserstack_sdk.bstack11l1l1ll11_opy_ = bstack11ll11ll1ll_opy_.lower() == bstack1ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪᜋ")
        bstack11ll1ll11l1_opy_ = version.parse(f.framework_version)
        bstack11ll11l1l1l_opy_ = f.platform_index
        bstack11ll11l1lll_opy_ = kwargs.get(bstack1ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᜌ"))
        bstack11ll1l1llll_opy_ = kwargs.get(bstack1ll11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᜍ"))
        bstack1111l1lll1_opy_ = {}
        bstack11ll11l11ll_opy_ = {}
        bstack11ll1ll11ll_opy_ = None
        bstack11ll1l1ll1l_opy_ = {}
        if bstack11ll1l1llll_opy_ is not None or bstack11ll11l1lll_opy_ is not None: # check top level caps
            if bstack11ll1l1llll_opy_ is not None:
                bstack11ll1l1ll1l_opy_[bstack1ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᜎ")] = bstack11ll1l1llll_opy_
            if bstack11ll11l1lll_opy_ is not None and callable(getattr(bstack11ll11l1lll_opy_, bstack1ll11_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᜏ"))):
                bstack11ll1l1ll1l_opy_[bstack1ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜐ")] = bstack11ll11l1lll_opy_.to_capabilities()
        response = self.bstack11lll1l1l11_opy_(bstack11ll11l1l1l_opy_, url, instance.ref(), json.dumps(bstack11ll1l1ll1l_opy_).encode(bstack1ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᜑ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1111l1lll1_opy_ = json.loads(response.capabilities.decode(bstack1ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᜒ")))
            if browserstack_sdk.bstack11l1l1ll11_opy_:
                def bstack11ll1l1lll1_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11ll1l1lll1_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1111l1lll1_opy_ = bstack11ll1l1lll1_opy_(bstack1111l1lll1_opy_)
                try:
                    bstack11ll1l11l11_opy_ = None
                    if isinstance(bstack1111l1lll1_opy_, dict):
                        if bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᜓ") in bstack1111l1lll1_opy_:
                            bstack11ll1l11l11_opy_ = bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᜔"))
                        elif isinstance(bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭᜕࠭")), dict):
                            bstack11ll1l11l11_opy_ = bstack1111l1lll1_opy_[bstack1ll11_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧ᜖")].get(bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᜗"))
                        if isinstance(bstack11ll1l11l11_opy_, dict) and bstack1ll11_opy_ (u"ࠫࡴࡼࡥࡳࡴ࡬ࡨࡪࡒ࡯ࡢࡦࡗࡩࡸࡺࡩ࡯ࡩࠪ᜘") in bstack11ll1l11l11_opy_:
                            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡘࡥ࡮ࡱࡹ࡭ࡳ࡭ࠠࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡳࡱࡰࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡪࡴࡤࡪࡰࡪࠤࡹࡵࠠࡩࡷࡥࠦ᜙"))
                            try:
                                bstack11ll1l11l11_opy_.pop(bstack1ll11_opy_ (u"࠭࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠬ᜚"), None)
                            except Exception:
                                pass
                            if bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᜛") in bstack1111l1lll1_opy_:
                                bstack1111l1lll1_opy_[bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᜜")] = bstack11ll1l11l11_opy_
                            if isinstance(bstack1111l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧ᜝")), dict):
                                bstack1111l1lll1_opy_[bstack1ll11_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨ᜞")][bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᜟ")] = bstack11ll1l11l11_opy_
                except Exception:
                    pass
            if not bstack1111l1lll1_opy_ and not browserstack_sdk.bstack11l1l1ll11_opy_:
                return
            bstack11ll1ll11ll_opy_ = f.bstack1l1l1lll11l_opy_[bstack1ll11_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤᜠ")](bstack1111l1lll1_opy_)
        if bstack11ll11l1lll_opy_ is not None and bstack11ll1ll11l1_opy_ >= version.parse(bstack1ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᜡ")):
            bstack11ll11l11ll_opy_ = None
        if (
                not bstack11ll11l1lll_opy_ and not bstack11ll1l1llll_opy_
        ) or (
                bstack11ll1ll11l1_opy_ < version.parse(bstack1ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᜢ"))
        ):
            bstack11ll11l11ll_opy_ = {}
            bstack11ll11l11ll_opy_.update(bstack1111l1lll1_opy_)
        self.logger.info(bstack1l1111l1_opy_)
        if browserstack_sdk.bstack11l1l1ll11_opy_:
            bstack11ll1l1l1l1_opy_ = bstack11ll1ll11ll_opy_ if bstack11ll1ll11ll_opy_ else bstack11ll11l1lll_opy_
            if bstack11ll1l1l1l1_opy_:
                bstack1llll11l_opy_ = bstack1lll11l11l_opy_(bstack11ll1l1l1l1_opy_, bstack1l1l11111l_opy_=bstack1ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᜣ"))
                if bstack11ll1l1l1l1_opy_ is bstack11ll11l1lll_opy_ and not bstack11ll1ll11ll_opy_:
                    bstack11ll1ll11ll_opy_ = bstack11ll1l1l1l1_opy_
            kwargs.update({bstack1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᜤ"): bstack111l11lll1_opy_})
        elif os.environ.get(bstack1ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓࠨᜥ")).lower().__eq__(bstack1ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤᜦ")):
            kwargs.update({bstack1ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᜧ"): f.bstack11ll1l1ll11_opy_})
        if bstack11ll1ll11l1_opy_ >= version.parse(bstack1ll11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᜨ")):
            if bstack11ll1l1llll_opy_ is not None:
                del kwargs[bstack1ll11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᜩ")]
            kwargs.update(
                {
                    bstack1ll11_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᜪ"): bstack11ll1ll11ll_opy_,
                    bstack1ll11_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᜫ"): True,
                    bstack1ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᜬ"): None,
                }
            )
        elif bstack11ll1ll11l1_opy_ >= version.parse(bstack1ll11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᜭ")):
            kwargs.update(
                {
                    bstack1ll11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᜮ"): bstack11ll11l11ll_opy_,
                    bstack1ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢᜯ"): bstack11ll1ll11ll_opy_,
                    bstack1ll11_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᜰ"): True,
                    bstack1ll11_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᜱ"): None,
                }
            )
        elif bstack11ll1ll11l1_opy_ >= version.parse(bstack1ll11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᜲ")):
            kwargs.update(
                {
                    bstack1ll11_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᜳ"): bstack11ll11l11ll_opy_,
                    bstack1ll11_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥ᜴ࠣ"): True,
                    bstack1ll11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧ᜵"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᜶"): bstack11ll11l11ll_opy_,
                    bstack1ll11_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦ᜷"): True,
                    bstack1ll11_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣ᜸"): None,
                }
            )