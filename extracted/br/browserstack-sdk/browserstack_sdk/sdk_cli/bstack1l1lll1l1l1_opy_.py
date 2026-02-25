# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1ll1llll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11lll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1ll1ll1ll1_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from bstack_utils.bstack111l1lll11_opy_ import bstack1ll11111_opy_
import browserstack_sdk
class bstack1ll111l1111_opy_(bstack1ll11llll11_opy_):
    bstack11lllll111l_opy_ = bstack11l1l11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᔝ")
    bstack11llllllll1_opy_ = bstack11l1l11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥᔞ")
    bstack11lllllll1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥᔟ")
    def __init__(self, bstack1ll1ll11l1l_opy_):
        super().__init__()
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_, bstack1lll11l111l_opy_.PRE), self.bstack11llll111l1_opy_)
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l1l11l1l1l_opy_)
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.POST), self.bstack11llll11ll1_opy_)
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.POST), self.bstack11llllll11l_opy_)
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.QUIT, bstack1lll11l111l_opy_.POST), self.bstack11llll1l11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llll111l1_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᔠ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᔡ")), str):
                    url = kwargs.get(bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᔢ"))
                elif hasattr(kwargs.get(bstack11l1l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᔣ")), bstack11l1l11_opy_ (u"ࠨࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠩᔤ")):
                    url = kwargs.get(bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᔥ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11l1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᔦ"))._url
            except Exception as e:
                url = bstack11l1l11_opy_ (u"ࠫࠬᔧ")
                self.logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡸ࡬ࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࡼࡿࠥᔨ").format(e))
            self.logger.info(bstack11l1l11_opy_ (u"ࠨࡒࡦ࡯ࡲࡸࡪࠦࡓࡦࡴࡹࡩࡷࠦࡁࡥࡦࡵࡩࡸࡹࠠࡣࡧ࡬ࡲ࡬ࠦࡰࡢࡵࡶࡩࡩࠦࡡࡴࠢ࠽ࠤࢀࢃࠢᔩ").format(str(url)))
            bstack1l1111111l1_opy_ = None
            driver_rank = None
            try:
                bstack1l1111111l1_opy_ = BrowserStackHelper.get_driver_label()
                if bstack1l1111111l1_opy_ is not None:
                    bstack11llllll111_opy_ = str(bstack1l1111111l1_opy_)
                    if bstack11l1l11_opy_ (u"ࠢࠤࠤᔪ") in bstack11llllll111_opy_:
                        bstack11llll1l1l1_opy_ = bstack11llllll111_opy_.rsplit(bstack11l1l11_opy_ (u"ࠣࠥࠥᔫ"), 1)[1]
                        try:
                            driver_rank = int(bstack11llll1l1l1_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡧࡻࡸࡷࡧࡣࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭ࠣࡪࡷࡵ࡭ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽࡨࡼࡵࡲࡩࡤ࡫ࡷࡣࡱࡧࡢࡦ࡮ࢀࠫ࠿ࠦࠢᔬ") + str(e) + bstack11l1l11_opy_ (u"ࠥࠦᔭ"))
            except Exception as e:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮࠽ࠤࠧᔮ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨᔯ"))
            self.bstack11llll1llll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack11l1l11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࡁࢀࡪࡲࡪࡸࡨࡶࡤࡸࡡ࡯࡭ࢀࠤࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡦ࠯ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᔰ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠢࠣᔱ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1l11l1l1l_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll1lll111l_opy_(instance, bstack1ll111l1111_opy_.bstack11lllll111l_opy_, False):
            return
        if not f.bstack1lll111l111_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_):
            return
        platform_index = f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_)
        if f.bstack1l1ll1111l1_opy_(method_name, *args) and len(args) > 1:
            bstack111l11l1l1_opy_ = datetime.now()
            hub_url = bstack1l1lllll1l1_opy_.hub_url(driver)
            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥᔲ") + str(hub_url) + bstack11l1l11_opy_ (u"ࠤࠥᔳ"))
            bstack1l1111111ll_opy_ = args[1][bstack11l1l11_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᔴ")] if isinstance(args[1], dict) and bstack11l1l11_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᔵ") in args[1] else None
            bstack11llll111ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥᔶ")
            if isinstance(bstack1l1111111ll_opy_, dict):
                bstack111l11l1l1_opy_ = datetime.now()
                r = self.bstack1l111111111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦᔷ"), datetime.now() - bstack111l11l1l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l1l11_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤᔸ") + str(r) + bstack11l1l11_opy_ (u"ࠣࠤᔹ"))
                        return
                    if r.hub_url:
                        f.bstack11llll11l1l_opy_(instance, driver, r.hub_url)
                        f.bstack1lll111ll11_opy_(instance, bstack1ll111l1111_opy_.bstack11lllll111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᔺ"), e)
    def bstack11llll11ll1_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l1lllll1l1_opy_.session_id(driver)
            if session_id:
                bstack11llll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᔻ").format(session_id)
                bstack11ll1l1l1_opy_.mark(bstack11llll1ll1l_opy_)
    def bstack11llllll11l_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lll111l_opy_(instance, bstack1ll111l1111_opy_.bstack11llllllll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l1lllll1l1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣᔼ") + str(hub_url) + bstack11l1l11_opy_ (u"ࠧࠨᔽ"))
            return
        framework_session_id = bstack1l1lllll1l1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᔾ") + str(framework_session_id) + bstack11l1l11_opy_ (u"ࠢࠣᔿ"))
            return
        if bstack1l1lllll1l1_opy_.bstack11llll1l111_opy_(*args) == bstack1l1lllll1l1_opy_.bstack11lllll1lll_opy_:
            bstack11lllll11ll_opy_ = bstack11l1l11_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣᕀ").format(framework_session_id)
            bstack11llll1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦᕁ").format(framework_session_id)
            bstack11ll1l1l1_opy_.end(
                label=bstack11l1l11_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨᕂ"),
                start=bstack11llll1ll1l_opy_,
                end=bstack11lllll11ll_opy_,
                status=True,
                failure=None
            )
            bstack111l11l1l1_opy_ = datetime.now()
            r = self.bstack11llll1lll1_opy_(
                ref,
                f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥᕃ"), datetime.now() - bstack111l11l1l1_opy_)
            f.bstack1lll111ll11_opy_(instance, bstack1ll111l1111_opy_.bstack11llllllll1_opy_, r.success)
    def bstack11llll1l11l_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll1lll111l_opy_(instance, bstack1ll111l1111_opy_.bstack11lllllll1l_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l1lllll1l1_opy_.session_id(driver)
        hub_url = bstack1l1lllll1l1_opy_.hub_url(driver)
        bstack111l11l1l1_opy_ = datetime.now()
        r = self.bstack11llll1l1ll_opy_(
            ref,
            f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥᕄ"), datetime.now() - bstack111l11l1l1_opy_)
        f.bstack1lll111ll11_opy_(instance, bstack1ll111l1111_opy_.bstack11lllllll1l_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1ll1ll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l111l11lll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11llll11lll_opy_ = int(driver_rank)
                is_secondary_driver = bstack11llll11lll_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᕅ") + str(req) + bstack11l1l11_opy_ (u"ࠢࠣᕆ"))
        try:
            r = self.bstack1ll1ll11111_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᕇ") + str(r.success) + bstack11l1l11_opy_ (u"ࠤࠥᕈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕉ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧᕊ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lllll11l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l111111111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕋ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᕌ") + str(req) + bstack11l1l11_opy_ (u"ࠢࠣᕍ"))
        try:
            r = self.bstack1ll1ll11111_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᕎ") + str(r.success) + bstack11l1l11_opy_ (u"ࠤࠥᕏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕐ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧᕑ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lllll1l1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack11llll1lll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕒ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤᕓ") + str(req) + bstack11l1l11_opy_ (u"ࠢࠣᕔ"))
        try:
            r = self.bstack1ll1ll11111_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᕕ") + str(r) + bstack11l1l11_opy_ (u"ࠤࠥᕖ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕗ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧᕘ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llll1111l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack11llll1l1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕙ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࡀࠠࠣᕚ") + str(req) + bstack11l1l11_opy_ (u"ࠢࠣᕛ"))
        try:
            r = self.bstack1ll1ll11111_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᕜ") + str(r) + bstack11l1l11_opy_ (u"ࠤࠥᕝ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕞ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧᕟ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11llllllll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack11llll1llll_opy_(self, instance: bstack1ll1llll111_opy_, url: str, f: bstack1l1lllll1l1_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11lllll1111_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ᕠ"))
        if bstack11lllll1111_opy_ is not None:
            browserstack_sdk.bstack111ll1llll_opy_ = bstack11lllll1111_opy_.lower() == bstack11l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫᕡ")
        bstack11lllllllll_opy_ = version.parse(f.framework_version)
        bstack11llllll1l1_opy_ = f.platform_index
        bstack11llll1ll11_opy_ = kwargs.get(bstack11l1l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᕢ"))
        bstack1l11111111l_opy_ = kwargs.get(bstack11l1l11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᕣ"))
        bstack1l1111llll1_opy_ = {}
        bstack11lllll1ll1_opy_ = {}
        bstack11llll11l11_opy_ = None
        bstack11lllllll11_opy_ = {}
        if bstack1l11111111l_opy_ is not None or bstack11llll1ll11_opy_ is not None: # check top level caps
            if bstack1l11111111l_opy_ is not None:
                bstack11lllllll11_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᕤ")] = bstack1l11111111l_opy_
            if bstack11llll1ll11_opy_ is not None and callable(getattr(bstack11llll1ll11_opy_, bstack11l1l11_opy_ (u"ࠥࡸࡴࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᕥ"))):
                bstack11lllllll11_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࡤࡧࡳࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᕦ")] = bstack11llll1ll11_opy_.to_capabilities()
        response = self.bstack1l111l11lll_opy_(bstack11llllll1l1_opy_, url, instance.ref(), json.dumps(bstack11lllllll11_opy_).encode(bstack11l1l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᕧ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1l1111llll1_opy_ = json.loads(response.capabilities.decode(bstack11l1l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᕨ")))
            if browserstack_sdk.bstack111ll1llll_opy_:
                def bstack1l111111l11_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack1l111111l11_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1l1111llll1_opy_ = bstack1l111111l11_opy_(bstack1l1111llll1_opy_)
                try:
                    bstack11lllll1l11_opy_ = None
                    if isinstance(bstack1l1111llll1_opy_, dict):
                        if bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᕩ") in bstack1l1111llll1_opy_:
                            bstack11lllll1l11_opy_ = bstack1l1111llll1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᕪ"))
                        elif isinstance(bstack1l1111llll1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᕫ")), dict):
                            bstack11lllll1l11_opy_ = bstack1l1111llll1_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᕬ")].get(bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᕭ"))
                        if isinstance(bstack11lllll1l11_opy_, dict) and bstack11l1l11_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᕮ") in bstack11lllll1l11_opy_:
                            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡒࡦ࡯ࡲࡺ࡮ࡴࡧࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡴࡲࡱࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡧ࡫ࡦࡰࡴࡨࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺ࡯ࠡࡪࡸࡦࠧᕯ"))
                            try:
                                bstack11lllll1l11_opy_.pop(bstack11l1l11_opy_ (u"ࠧࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬࠭ᕰ"), None)
                            except Exception:
                                pass
                            if bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᕱ") in bstack1l1111llll1_opy_:
                                bstack1l1111llll1_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᕲ")] = bstack11lllll1l11_opy_
                            if isinstance(bstack1l1111llll1_opy_.get(bstack11l1l11_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᕳ")), dict):
                                bstack1l1111llll1_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᕴ")][bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᕵ")] = bstack11lllll1l11_opy_
                except Exception:
                    pass
            if not bstack1l1111llll1_opy_ and not browserstack_sdk.bstack111ll1llll_opy_:
                return
            bstack11llll11l11_opy_ = f.bstack1ll111l1l1l_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᕶ")](bstack1l1111llll1_opy_)
        if bstack11llll1ll11_opy_ is not None and bstack11lllllllll_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᕷ")):
            bstack11lllll1ll1_opy_ = None
        if (
                not bstack11llll1ll11_opy_ and not bstack1l11111111l_opy_
        ) or (
                bstack11lllllllll_opy_ < version.parse(bstack11l1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᕸ"))
        ):
            bstack11lllll1ll1_opy_ = {}
            bstack11lllll1ll1_opy_.update(bstack1l1111llll1_opy_)
        self.logger.info(bstack1l11lll1ll_opy_)
        if browserstack_sdk.bstack111ll1llll_opy_:
            bstack1l111111l1l_opy_ = bstack11llll11l11_opy_ if bstack11llll11l11_opy_ else bstack11llll1ll11_opy_
            if bstack1l111111l1l_opy_:
                bstack11l1l1lll_opy_ = bstack1ll11111_opy_(bstack1l111111l1l_opy_, bstack1lll1ll11_opy_=bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᕹ"))
                if bstack1l111111l1l_opy_ is bstack11llll1ll11_opy_ and not bstack11llll11l11_opy_:
                    bstack11llll11l11_opy_ = bstack1l111111l1l_opy_
            kwargs.update({bstack11l1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᕺ"): bstack1ll1ll1ll1_opy_})
        elif os.environ.get(bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᕻ")).lower().__eq__(bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᕼ")):
            kwargs.update({bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᕽ"): f.bstack11llllll1ll_opy_})
        if bstack11lllllllll_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᕾ")):
            if bstack1l11111111l_opy_ is not None:
                del kwargs[bstack11l1l11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᕿ")]
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᖀ"): bstack11llll11l11_opy_,
                    bstack11l1l11_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᖁ"): True,
                    bstack11l1l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᖂ"): None,
                }
            )
        elif bstack11lllllllll_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᖃ")):
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᖄ"): bstack11lllll1ll1_opy_,
                    bstack11l1l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᖅ"): bstack11llll11l11_opy_,
                    bstack11l1l11_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᖆ"): True,
                    bstack11l1l11_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᖇ"): None,
                }
            )
        elif bstack11lllllllll_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᖈ")):
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᖉ"): bstack11lllll1ll1_opy_,
                    bstack11l1l11_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᖊ"): True,
                    bstack11l1l11_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᖋ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᖌ"): bstack11lllll1ll1_opy_,
                    bstack11l1l11_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᖍ"): True,
                    bstack11l1l11_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᖎ"): None,
                }
            )