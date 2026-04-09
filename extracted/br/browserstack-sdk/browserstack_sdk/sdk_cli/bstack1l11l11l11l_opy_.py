# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1l1lll111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l111l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1ll1ll111_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from bstack_utils.bstack1111l1llll_opy_ import bstack1111llll1_opy_
import browserstack_sdk
class bstack1l1l1l11ll1_opy_(bstack1l11ll11111_opy_):
    bstack11l1l11l1ll_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨ៺")
    bstack11l11ll1lll_opy_ = bstack11ll11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣ៻")
    bstack11l1l1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣ៼")
    def __init__(self, bstack1l1lllll1ll_opy_):
        super().__init__()
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll11lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11l11llllll_opy_)
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11llll1ll1l_opy_)
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.POST), self.bstack11l11lllll1_opy_)
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.POST), self.bstack11l1l111l11_opy_)
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.QUIT, bstack111llll1ll_opy_.POST), self.bstack11l11lll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11llllll_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦ៽"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ៾")), str):
                    url = kwargs.get(bstack11ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ៿"))
                elif hasattr(kwargs.get(bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᠀")), bstack11ll11_opy_ (u"࠭࡟ࡤ࡮࡬ࡩࡳࡺ࡟ࡤࡱࡱࡪ࡮࡭ࠧ᠁")):
                    url = kwargs.get(bstack11ll11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ᠂"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᠃"))._url
            except Exception as e:
                url = bstack11ll11_opy_ (u"ࠩࠪ᠄")
                self.logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡶࡱࠦࡦࡳࡱࡰࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࢁࡽࠣ᠅").format(e))
            self.logger.info(bstack11ll11_opy_ (u"ࠦࡗ࡫࡭ࡰࡶࡨࠤࡘ࡫ࡲࡷࡧࡵࠤࡆࡪࡤࡳࡧࡶࡷࠥࡨࡥࡪࡰࡪࠤࡵࡧࡳࡴࡧࡧࠤࡦࡹࠠ࠻ࠢࡾࢁࠧ᠆").format(str(url)))
            bstack11l1l111l1l_opy_ = None
            driver_rank = None
            try:
                bstack11l1l111l1l_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11l1l111l1l_opy_ is not None:
                    bstack11l1l111ll1_opy_ = str(bstack11l1l111l1l_opy_)
                    if bstack11ll11_opy_ (u"ࠧࠩࠢ᠇") in bstack11l1l111ll1_opy_:
                        bstack11l1l11lll1_opy_ = bstack11l1l111ll1_opy_.rsplit(bstack11ll11_opy_ (u"ࠨࠣࠣ᠈"), 1)[1]
                        try:
                            driver_rank = int(bstack11l1l11lll1_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡥࡹࡶࡵࡥࡨࡺࡩ࡯ࡩࠣࡨࡷ࡯ࡶࡦࡴࠣࡶࡦࡴ࡫ࠡࡨࡵࡳࡲࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻࡦࡺࡳࡰ࡮ࡩࡩࡵࡡ࡯ࡥࡧ࡫࡬ࡾࠩ࠽ࠤࠧ᠉") + str(e) + bstack11ll11_opy_ (u"ࠣࠤ᠊"))
            except Exception as e:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬࠻ࠢࠥ᠋") + str(e) + bstack11ll11_opy_ (u"ࠥࠦ᠌"))
            self.bstack11l1l111lll_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack11ll11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵࡣࡷࡧ࡮࡬࠿ࡾࡨࡷ࡯ࡶࡦࡴࡢࡶࡦࡴ࡫ࡾࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿ࡫࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᠍") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨ᠎"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11llll1ll1l_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll111l1111_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11l1l11l1ll_opy_, False):
            return
        if not f.bstack1l1llll1l1l_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_):
            return
        platform_index = f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_)
        if f.bstack1l111111ll1_opy_(method_name, *args) and len(args) > 1:
            bstack1l111ll1ll_opy_ = datetime.now()
            hub_url = bstack1l1l1ll11ll_opy_.hub_url(driver)
            self.logger.warning(bstack11ll11_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲ࠽ࠣ᠏") + str(hub_url) + bstack11ll11_opy_ (u"ࠢࠣ᠐"))
            bstack11l11llll1l_opy_ = args[1][bstack11ll11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢ᠑")] if isinstance(args[1], dict) and bstack11ll11_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᠒") in args[1] else None
            bstack11l11lll1l1_opy_ = bstack11ll11_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣ᠓")
            if isinstance(bstack11l11llll1l_opy_, dict):
                bstack1l111ll1ll_opy_ = datetime.now()
                r = self.bstack11l11lll111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤ᠔"), datetime.now() - bstack1l111ll1ll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11ll11_opy_ (u"ࠧࡹ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫࠿ࠦࠢ᠕") + str(r) + bstack11ll11_opy_ (u"ࠨࠢ᠖"))
                        return
                    if r.hub_url:
                        f.bstack11l1l1l1l11_opy_(instance, driver, r.hub_url)
                        f.bstack1l1l1111l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11l1l11l1ll_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ᠗"), e)
    def bstack11l11lllll1_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l1l1ll11ll_opy_.session_id(driver)
            if session_id:
                bstack11l1l1l11l1_opy_ = bstack11ll11_opy_ (u"ࠣࡽࢀ࠾ࡸࡺࡡࡳࡶࠥ᠘").format(session_id)
                bstack1ll111lll_opy_.mark(bstack11l1l1l11l1_opy_)
    def bstack11l1l111l11_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll111l1111_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11l11ll1lll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l1l1ll11ll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡭ࡻࡢࡠࡷࡵࡰࡂࠨ᠙") + str(hub_url) + bstack11ll11_opy_ (u"ࠥࠦ᠚"))
            return
        framework_session_id = bstack1l1l1ll11ll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡃࠢ᠛") + str(framework_session_id) + bstack11ll11_opy_ (u"ࠧࠨ᠜"))
            return
        if bstack1l1l1ll11ll_opy_.bstack11l11llll11_opy_(*args) == bstack1l1l1ll11ll_opy_.bstack11l1l1l1lll_opy_:
            bstack11l1l1111l1_opy_ = bstack11ll11_opy_ (u"ࠨࡻࡾ࠼ࡨࡲࡩࠨ᠝").format(framework_session_id)
            bstack11l1l1l11l1_opy_ = bstack11ll11_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤ᠞").format(framework_session_id)
            bstack1ll111lll_opy_.end(
                label=bstack11ll11_opy_ (u"ࠣࡵࡧ࡯࠿ࡪࡲࡪࡸࡨࡶ࠿ࡶ࡯ࡴࡶ࠰࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠦ᠟"),
                start=bstack11l1l1l11l1_opy_,
                end=bstack11l1l1111l1_opy_,
                status=True,
                failure=None
            )
            bstack1l111ll1ll_opy_ = datetime.now()
            r = self.bstack11l1l1ll1l1_opy_(
                ref,
                f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣᠠ"), datetime.now() - bstack1l111ll1ll_opy_)
            f.bstack1l1l1111l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11l11ll1lll_opy_, r.success)
    def bstack11l11lll11l_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll111l1111_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11l1l1l1ll1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l1l1ll11ll_opy_.session_id(driver)
        hub_url = bstack1l1l1ll11ll_opy_.hub_url(driver)
        bstack1l111ll1ll_opy_ = datetime.now()
        r = self.bstack11l1l1l1111_opy_(
            ref,
            f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣᠡ"), datetime.now() - bstack1l111ll1ll_opy_)
        f.bstack1l1l1111l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack11l1l1l1ll1_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll11ll1l_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11l1llll1l1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11l1l11l11l_opy_ = int(driver_rank)
                is_secondary_driver = bstack11l1l11l11l_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᠢ") + str(req) + bstack11ll11_opy_ (u"ࠧࠨᠣ"))
        try:
            r = self.bstack1l1l111l1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᠤ") + str(r.success) + bstack11ll11_opy_ (u"ࠢࠣᠥ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᠦ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᠧ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l1111ll_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11l11lll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l11111l1l1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᠨ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷ࠾ࠥࠨᠩ") + str(req) + bstack11ll11_opy_ (u"ࠧࠨᠪ"))
        try:
            r = self.bstack1l1l111l1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᠫ") + str(r.success) + bstack11ll11_opy_ (u"ࠢࠣᠬ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᠭ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᠮ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l11111l_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11l1l1ll1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11111l1l1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᠯ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸ࠿ࠦࠢᠰ") + str(req) + bstack11ll11_opy_ (u"ࠧࠨᠱ"))
        try:
            r = self.bstack1l1l111l1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᠲ") + str(r) + bstack11ll11_opy_ (u"ࠢࠣᠳ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᠴ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᠵ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l1ll11l_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11l1l1l1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l11111l1l1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᠶ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨᠷ") + str(req) + bstack11ll11_opy_ (u"ࠧࠨᠸ"))
        try:
            r = self.bstack1l1l111l1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᠹ") + str(r) + bstack11ll11_opy_ (u"ࠢࠣᠺ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᠻ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᠼ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111ll11_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack11l1l111lll_opy_(self, instance: bstack1l1lll111ll_opy_, url: str, f: bstack1l1l1ll11ll_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11l1l1ll1ll_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠪࡓ࡛ࡋࡒࡓࡋࡇࡉࡤࡒࡏࡂࡆࡢࡘࡊ࡙ࡔࡊࡐࡊࠫᠽ"))
        if bstack11l1l1ll1ll_opy_ is not None:
            browserstack_sdk.bstack1111ll111_opy_ = bstack11l1l1ll1ll_opy_.lower() == bstack11ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩᠾ")
        bstack11l1l1l11ll_opy_ = version.parse(f.framework_version)
        bstack11l1l11llll_opy_ = f.platform_index
        bstack11l1l11l111_opy_ = kwargs.get(bstack11ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᠿ"))
        bstack11l1l11ll1l_opy_ = kwargs.get(bstack11ll11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᡀ"))
        bstack1111l1ll_opy_ = {}
        bstack11l11lll1ll_opy_ = {}
        bstack11l1l11l1l1_opy_ = None
        bstack11l1l1l111l_opy_ = {}
        if bstack11l1l11ll1l_opy_ is not None or bstack11l1l11l111_opy_ is not None: # check top level caps
            if bstack11l1l11ll1l_opy_ is not None:
                bstack11l1l1l111l_opy_[bstack11ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡁ")] = bstack11l1l11ll1l_opy_
            if bstack11l1l11l111_opy_ is not None and callable(getattr(bstack11l1l11l111_opy_, bstack11ll11_opy_ (u"ࠣࡶࡲࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᡂ"))):
                bstack11l1l1l111l_opy_[bstack11ll11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࡢࡥࡸࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᡃ")] = bstack11l1l11l111_opy_.to_capabilities()
        response = self.bstack11l1llll1l1_opy_(bstack11l1l11llll_opy_, url, instance.ref(), json.dumps(bstack11l1l1l111l_opy_).encode(bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᡄ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1111l1ll_opy_ = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᡅ")))
            if browserstack_sdk.bstack1111ll111_opy_:
                def bstack11l1l1ll111_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l1l1ll111_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1111l1ll_opy_ = bstack11l1l1ll111_opy_(bstack1111l1ll_opy_)
                try:
                    bstack11l1l111111_opy_ = None
                    if isinstance(bstack1111l1ll_opy_, dict):
                        if bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡆ") in bstack1111l1ll_opy_:
                            bstack11l1l111111_opy_ = bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᡇ"))
                        elif isinstance(bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"ࠧࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠬᡈ")), dict):
                            bstack11l1l111111_opy_ = bstack1111l1ll_opy_[bstack11ll11_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᡉ")].get(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᡊ"))
                        if isinstance(bstack11l1l111111_opy_, dict) and bstack11ll11_opy_ (u"ࠪࡳࡻ࡫ࡲࡳ࡫ࡧࡩࡑࡵࡡࡥࡖࡨࡷࡹ࡯࡮ࡨࠩᡋ") in bstack11l1l111111_opy_:
                            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡗ࡫࡭ࡰࡸ࡬ࡲ࡬ࠦ࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡸࡴࠦࡨࡶࡤࠥᡌ"))
                            try:
                                bstack11l1l111111_opy_.pop(bstack11ll11_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᡍ"), None)
                            except Exception:
                                pass
                            if bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᡎ") in bstack1111l1ll_opy_:
                                bstack1111l1ll_opy_[bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᡏ")] = bstack11l1l111111_opy_
                            if isinstance(bstack1111l1ll_opy_.get(bstack11ll11_opy_ (u"ࠨࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭࠭ᡐ")), dict):
                                bstack1111l1ll_opy_[bstack11ll11_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᡑ")][bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᡒ")] = bstack11l1l111111_opy_
                except Exception:
                    pass
            if not bstack1111l1ll_opy_ and not browserstack_sdk.bstack1111ll111_opy_:
                return
            bstack11l1l11l1l1_opy_ = f.bstack1l11l111l11_opy_[bstack11ll11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡣࡴࡶࡴࡪࡱࡱࡷࡤ࡬ࡲࡰ࡯ࡢࡧࡦࡶࡳࠣᡓ")](bstack1111l1ll_opy_)
        if bstack11l1l11l111_opy_ is not None and bstack11l1l1l11ll_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᡔ")):
            bstack11l11lll1ll_opy_ = None
        if (
                not bstack11l1l11l111_opy_ and not bstack11l1l11ll1l_opy_
        ) or (
                bstack11l1l1l11ll_opy_ < version.parse(bstack11ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᡕ"))
        ):
            bstack11l11lll1ll_opy_ = {}
            bstack11l11lll1ll_opy_.update(bstack1111l1ll_opy_)
        self.logger.info(bstack11l111l11_opy_)
        if browserstack_sdk.bstack1111ll111_opy_:
            bstack11l1l1l1l1l_opy_ = bstack11l1l11l1l1_opy_ if bstack11l1l11l1l1_opy_ else bstack11l1l11l111_opy_
            if bstack11l1l1l1l1l_opy_:
                bstack1ll1l11ll1_opy_ = bstack1111llll1_opy_(bstack11l1l1l1l1l_opy_, bstack111lll111_opy_=bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᡖ"))
                if bstack11l1l1l1l1l_opy_ is bstack11l1l11l111_opy_ and not bstack11l1l11l1l1_opy_:
                    bstack11l1l11l1l1_opy_ = bstack11l1l1l1l1l_opy_
            kwargs.update({bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᡗ"): bstack1ll1ll111_opy_})
        elif os.environ.get(bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧᡘ")).lower().__eq__(bstack11ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣᡙ")):
            kwargs.update({bstack11ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᡚ"): f.bstack11l1l11ll11_opy_})
        if bstack11l1l1l11ll_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᡛ")):
            if bstack11l1l11ll1l_opy_ is not None:
                del kwargs[bstack11ll11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᡜ")]
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᡝ"): bstack11l1l11l1l1_opy_,
                    bstack11ll11_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᡞ"): True,
                    bstack11ll11_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᡟ"): None,
                }
            )
        elif bstack11l1l1l11ll_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᡠ")):
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᡡ"): bstack11l11lll1ll_opy_,
                    bstack11ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨᡢ"): bstack11l1l11l1l1_opy_,
                    bstack11ll11_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᡣ"): True,
                    bstack11ll11_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᡤ"): None,
                }
            )
        elif bstack11l1l1l11ll_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᡥ")):
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᡦ"): bstack11l11lll1ll_opy_,
                    bstack11ll11_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᡧ"): True,
                    bstack11ll11_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᡨ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᡩ"): bstack11l11lll1ll_opy_,
                    bstack11ll11_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᡪ"): True,
                    bstack11ll11_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᡫ"): None,
                }
            )