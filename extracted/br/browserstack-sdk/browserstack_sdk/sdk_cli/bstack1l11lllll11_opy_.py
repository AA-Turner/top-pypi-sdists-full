# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1l11lll1l1l_opy_ import bstack1l11ll1l111_opy_
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
    bstack1l1ll11ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11ll1llll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11ll11l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1l1lll1l1l_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.bstack1l11ll1111_opy_ import bstack1l11l1l1l1_opy_
import browserstack_sdk
class bstack1l11l1lll1l_opy_(bstack1l11ll1l111_opy_):
    bstack11l1l111l11_opy_ = bstack1ll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤ៽")
    bstack11l11ll1ll1_opy_ = bstack1ll_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦ៾")
    bstack11l11lll111_opy_ = bstack1ll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦ៿")
    def __init__(self, bstack1ll1111ll11_opy_):
        super().__init__()
        bstack1l11ll1llll_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1l1l1l11l_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l11ll1l11_opy_)
        bstack1l11ll1llll_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_, bstack1llll11lll_opy_.PRE), self.bstack11lllll111l_opy_)
        bstack1l11ll1llll_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_, bstack1llll11lll_opy_.POST), self.bstack11l1l11111l_opy_)
        bstack1l11ll1llll_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_, bstack1llll11lll_opy_.POST), self.bstack11l1l1l111l_opy_)
        bstack1l11ll1llll_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.QUIT, bstack1llll11lll_opy_.POST), self.bstack11l1l1l11ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l11ll1l11_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢ᠀"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1ll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᠁")), str):
                    url = kwargs.get(bstack1ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ᠂"))
                elif hasattr(kwargs.get(bstack1ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦ᠃")), bstack1ll_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪ᠄")):
                    url = kwargs.get(bstack1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᠅"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢ᠆"))._url
            except Exception as e:
                url = bstack1ll_opy_ (u"ࠬ࠭᠇")
                self.logger.error(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦ᠈").format(e))
            self.logger.info(bstack1ll_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣ᠉").format(str(url)))
            bstack11l11ll1lll_opy_ = None
            driver_rank = None
            try:
                bstack11l11ll1lll_opy_ = BrowserStackHelper.get_driver_label()
                if bstack11l11ll1lll_opy_ is not None:
                    bstack11l1l11l1ll_opy_ = str(bstack11l11ll1lll_opy_)
                    if bstack1ll_opy_ (u"ࠣࠥࠥ᠊") in bstack11l1l11l1ll_opy_:
                        bstack11l1l1l1l1l_opy_ = bstack11l1l11l1ll_opy_.rsplit(bstack1ll_opy_ (u"ࠤࠦࠦ᠋"), 1)[1]
                        try:
                            driver_rank = int(bstack11l1l1l1l1l_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡨࡼࡹࡸࡡࡤࡶ࡬ࡲ࡬ࠦࡤࡳ࡫ࡹࡩࡷࠦࡲࡢࡰ࡮ࠤ࡫ࡸ࡯࡮ࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡩࡽࡶ࡬ࡪࡥ࡬ࡸࡤࡲࡡࡣࡧ࡯ࢁࠬࡀࠠࠣ᠌") + str(e) + bstack1ll_opy_ (u"ࠦࠧ᠍"))
            except Exception as e:
                self.logger.debug(bstack1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯࠾ࠥࠨ᠎") + str(e) + bstack1ll_opy_ (u"ࠨࠢ᠏"))
            self.bstack11l1l11lll1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1ll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡳࡣࡱ࡯ࡂࢁࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࢁࠥࡪࡲࡪࡸࡨࡶ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡧ࠰ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀ࠾ࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᠐") + str(kwargs) + bstack1ll_opy_ (u"ࠣࠤ᠑"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11lllll111l_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1ll11111l11_opy_(instance, bstack1l11l1lll1l_opy_.bstack11l1l111l11_opy_, False):
            return
        if not f.bstack1ll11111lll_opy_(instance, bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_):
            return
        platform_index = f.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_)
        if f.bstack1l11111l1l1_opy_(method_name, *args) and len(args) > 1:
            bstack1l1111ll_opy_ = datetime.now()
            hub_url = bstack1l11ll1llll_opy_.hub_url(driver)
            self.logger.warning(bstack1ll_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦ᠒") + str(hub_url) + bstack1ll_opy_ (u"ࠥࠦ᠓"))
            bstack11l11lllll1_opy_ = args[1][bstack1ll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᠔")] if isinstance(args[1], dict) and bstack1ll_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᠕") in args[1] else None
            bstack11l11lll1ll_opy_ = bstack1ll_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦ᠖")
            if isinstance(bstack11l11lllll1_opy_, dict):
                bstack1l1111ll_opy_ = datetime.now()
                r = self.bstack11l11lll1l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧ᠗"), datetime.now() - bstack1l1111ll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥ᠘") + str(r) + bstack1ll_opy_ (u"ࠤࠥ᠙"))
                        return
                    if r.hub_url:
                        f.bstack11l11ll11ll_opy_(instance, driver, r.hub_url)
                        f.bstack1l1l1l1l_opy_(instance, bstack1l11l1lll1l_opy_.bstack11l1l111l11_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ᠚"), e)
    def bstack11l1l11111l_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1l11ll1llll_opy_.session_id(driver)
            if session_id:
                bstack11l1l1l1ll1_opy_ = bstack1ll_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨ᠛").format(session_id)
                bstack1l11l1ll11_opy_.mark(bstack11l1l1l1ll1_opy_)
    def bstack11l1l1l111l_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll11111l11_opy_(instance, bstack1l11l1lll1l_opy_.bstack11l11ll1ll1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1l11ll1llll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤ᠜") + str(hub_url) + bstack1ll_opy_ (u"ࠨࠢ᠝"))
            return
        framework_session_id = bstack1l11ll1llll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥ᠞") + str(framework_session_id) + bstack1ll_opy_ (u"ࠣࠤ᠟"))
            return
        if bstack1l11ll1llll_opy_.bstack11l11lll11l_opy_(*args) == bstack1l11ll1llll_opy_.bstack11l1l111l1l_opy_:
            bstack11l1l111111_opy_ = bstack1ll_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤᠠ").format(framework_session_id)
            bstack11l1l1l1ll1_opy_ = bstack1ll_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᠡ").format(framework_session_id)
            bstack1l11l1ll11_opy_.end(
                label=bstack1ll_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢᠢ"),
                start=bstack11l1l1l1ll1_opy_,
                end=bstack11l1l111111_opy_,
                status=True,
                failure=None
            )
            bstack1l1111ll_opy_ = datetime.now()
            r = self.bstack11l11ll11l1_opy_(
                ref,
                f.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᠣ"), datetime.now() - bstack1l1111ll_opy_)
            f.bstack1l1l1l1l_opy_(instance, bstack1l11l1lll1l_opy_.bstack11l11ll1ll1_opy_, r.success)
    def bstack11l1l1l11ll_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1ll11111l11_opy_(instance, bstack1l11l1lll1l_opy_.bstack11l11lll111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1l11ll1llll_opy_.session_id(driver)
        hub_url = bstack1l11ll1llll_opy_.hub_url(driver)
        bstack1l1111ll_opy_ = datetime.now()
        r = self.bstack11l11llll11_opy_(
            ref,
            f.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᠤ"), datetime.now() - bstack1l1111ll_opy_)
        f.bstack1l1l1l1l_opy_(instance, bstack1l11l1lll1l_opy_.bstack11l11lll111_opy_, r.success)
    @measure(event_name=EVENTS.bstack11l1ll111l_opy_, stage=STAGE.bstack11llll111l_opy_)
    def bstack11l1ll1llll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11l1l1l11l1_opy_ = int(driver_rank)
                is_secondary_driver = bstack11l1l1l11l1_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᠥ") + str(req) + bstack1ll_opy_ (u"ࠣࠤᠦ"))
        try:
            r = self.bstack1ll11ll11l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᠧ") + str(r.success) + bstack1ll_opy_ (u"ࠥࠦᠨ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᠩ") + str(e) + bstack1ll_opy_ (u"ࠧࠨᠪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l1l1l11_opy_, stage=STAGE.bstack11llll111l_opy_)
    def bstack11l11lll1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l111l1ll11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᠫ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᠬ") + str(req) + bstack1ll_opy_ (u"ࠣࠤᠭ"))
        try:
            r = self.bstack1ll11ll11l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᠮ") + str(r.success) + bstack1ll_opy_ (u"ࠥࠦᠯ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᠰ") + str(e) + bstack1ll_opy_ (u"ࠧࠨᠱ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l11llll_opy_, stage=STAGE.bstack11llll111l_opy_)
    def bstack11l11ll11l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l111l1ll11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᠲ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴ࠻ࠢࠥᠳ") + str(req) + bstack1ll_opy_ (u"ࠣࠤᠴ"))
        try:
            r = self.bstack1ll11ll11l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᠵ") + str(r) + bstack1ll_opy_ (u"ࠥࠦᠶ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᠷ") + str(e) + bstack1ll_opy_ (u"ࠧࠨᠸ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1l11l11l_opy_, stage=STAGE.bstack11llll111l_opy_)
    def bstack11l11llll11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l111l1ll11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᠹ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤᠺ") + str(req) + bstack1ll_opy_ (u"ࠣࠤᠻ"))
        try:
            r = self.bstack1ll11ll11l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᠼ") + str(r) + bstack1ll_opy_ (u"ࠥࠦᠽ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᠾ") + str(e) + bstack1ll_opy_ (u"ࠧࠨᠿ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1llll11_opy_, stage=STAGE.bstack11llll111l_opy_)
    def bstack11l1l11lll1_opy_(self, instance: bstack1l1ll11ll11_opy_, url: str, f: bstack1l11ll1llll_opy_, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack11l1l111lll_opy_ = os.environ.get(bstack1ll_opy_ (u"࠭ࡏࡗࡇࡕࡖࡎࡊࡅࡠࡎࡒࡅࡉࡥࡔࡆࡕࡗࡍࡓࡍࠧᡀ"))
        if bstack11l1l111lll_opy_ is not None:
            browserstack_sdk.bstack1lll111111_opy_ = bstack11l1l111lll_opy_.lower() == bstack1ll_opy_ (u"ࠧࡵࡴࡸࡩࠬᡁ")
        bstack11l1l11ll1l_opy_ = version.parse(f.framework_version)
        bstack11l1l11l111_opy_ = f.platform_index
        bstack11l1l111ll1_opy_ = kwargs.get(bstack1ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᡂ"))
        bstack11l1l1111ll_opy_ = kwargs.get(bstack1ll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᡃ"))
        bstack1111l111ll_opy_ = {}
        bstack11l11llll1l_opy_ = {}
        bstack11l1l11ll11_opy_ = None
        bstack11l1l1l1111_opy_ = {}
        if bstack11l1l1111ll_opy_ is not None or bstack11l1l111ll1_opy_ is not None: # check top level caps
            if bstack11l1l1111ll_opy_ is not None:
                bstack11l1l1l1111_opy_[bstack1ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᡄ")] = bstack11l1l1111ll_opy_
            if bstack11l1l111ll1_opy_ is not None and callable(getattr(bstack11l1l111ll1_opy_, bstack1ll_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᡅ"))):
                bstack11l1l1l1111_opy_[bstack1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡆ")] = bstack11l1l111ll1_opy_.to_capabilities()
        response = self.bstack11l1ll1llll_opy_(bstack11l1l11l111_opy_, url, instance.ref(), json.dumps(bstack11l1l1l1111_opy_).encode(bstack1ll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᡇ")), driver_rank)
        if response is not None and response.capabilities:
            bstack1111l111ll_opy_ = json.loads(response.capabilities.decode(bstack1ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᡈ")))
            if browserstack_sdk.bstack1lll111111_opy_:
                def bstack11l1l11l1l1_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l1l11l1l1_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack1111l111ll_opy_ = bstack11l1l11l1l1_opy_(bstack1111l111ll_opy_)
                try:
                    bstack11l11ll1l1l_opy_ = None
                    if isinstance(bstack1111l111ll_opy_, dict):
                        if bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᡉ") in bstack1111l111ll_opy_:
                            bstack11l11ll1l1l_opy_ = bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᡊ"))
                        elif isinstance(bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᡋ")), dict):
                            bstack11l11ll1l1l_opy_ = bstack1111l111ll_opy_[bstack1ll_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᡌ")].get(bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᡍ"))
                        if isinstance(bstack11l11ll1l1l_opy_, dict) and bstack1ll_opy_ (u"࠭࡯ࡷࡧࡵࡶ࡮ࡪࡥࡍࡱࡤࡨ࡙࡫ࡳࡵ࡫ࡱ࡫ࠬᡎ") in bstack11l11ll1l1l_opy_:
                            self.logger.debug(bstack1ll_opy_ (u"ࠢࡓࡧࡰࡳࡻ࡯࡮ࡨࠢࡲࡺࡪࡸࡲࡪࡦࡨࡐࡴࡧࡤࡕࡧࡶࡸ࡮ࡴࡧࠡࡨࡵࡳࡲࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡨࡥࡧࡱࡵࡩࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡴࡰࠢ࡫ࡹࡧࠨᡏ"))
                            try:
                                bstack11l11ll1l1l_opy_.pop(bstack1ll_opy_ (u"ࠨࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠧᡐ"), None)
                            except Exception:
                                pass
                            if bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᡑ") in bstack1111l111ll_opy_:
                                bstack1111l111ll_opy_[bstack1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᡒ")] = bstack11l11ll1l1l_opy_
                            if isinstance(bstack1111l111ll_opy_.get(bstack1ll_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᡓ")), dict):
                                bstack1111l111ll_opy_[bstack1ll_opy_ (u"ࠬࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠪᡔ")][bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᡕ")] = bstack11l11ll1l1l_opy_
                except Exception:
                    pass
            if not bstack1111l111ll_opy_ and not browserstack_sdk.bstack1lll111111_opy_:
                return
            bstack11l1l11ll11_opy_ = f.bstack1l1l11ll11l_opy_[bstack1ll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᡖ")](bstack1111l111ll_opy_)
        if bstack11l1l111ll1_opy_ is not None and bstack11l1l11ll1l_opy_ >= version.parse(bstack1ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᡗ")):
            bstack11l11llll1l_opy_ = None
        if (
                not bstack11l1l111ll1_opy_ and not bstack11l1l1111ll_opy_
        ) or (
                bstack11l1l11ll1l_opy_ < version.parse(bstack1ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᡘ"))
        ):
            bstack11l11llll1l_opy_ = {}
            bstack11l11llll1l_opy_.update(bstack1111l111ll_opy_)
        self.logger.info(bstack11ll11l111_opy_)
        if browserstack_sdk.bstack1lll111111_opy_:
            bstack11l11llllll_opy_ = bstack11l1l11ll11_opy_ if bstack11l1l11ll11_opy_ else bstack11l1l111ll1_opy_
            if bstack11l11llllll_opy_:
                bstack1llll11ll1_opy_ = bstack1l11l1l1l1_opy_(bstack11l11llllll_opy_, bstack1ll1l1l1_opy_=bstack1ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᡙ"))
                if bstack11l11llllll_opy_ is bstack11l1l111ll1_opy_ and not bstack11l1l11ll11_opy_:
                    bstack11l1l11ll11_opy_ = bstack11l11llllll_opy_
            kwargs.update({bstack1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᡚ"): bstack1l1lll1l1l_opy_})
        elif os.environ.get(bstack1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᡛ")).lower().__eq__(bstack1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᡜ")):
            kwargs.update({bstack1ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᡝ"): f.bstack11l1l1111l1_opy_})
        if bstack11l1l11ll1l_opy_ >= version.parse(bstack1ll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᡞ")):
            if bstack11l1l1111ll_opy_ is not None:
                del kwargs[bstack1ll_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᡟ")]
            kwargs.update(
                {
                    bstack1ll_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᡠ"): bstack11l1l11ll11_opy_,
                    bstack1ll_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᡡ"): True,
                    bstack1ll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᡢ"): None,
                }
            )
        elif bstack11l1l11ll1l_opy_ >= version.parse(bstack1ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᡣ")):
            kwargs.update(
                {
                    bstack1ll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᡤ"): bstack11l11llll1l_opy_,
                    bstack1ll_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᡥ"): bstack11l1l11ll11_opy_,
                    bstack1ll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᡦ"): True,
                    bstack1ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᡧ"): None,
                }
            )
        elif bstack11l1l11ll1l_opy_ >= version.parse(bstack1ll_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᡨ")):
            kwargs.update(
                {
                    bstack1ll_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᡩ"): bstack11l11llll1l_opy_,
                    bstack1ll_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᡪ"): True,
                    bstack1ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᡫ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᡬ"): bstack11l11llll1l_opy_,
                    bstack1ll_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᡭ"): True,
                    bstack1ll_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᡮ"): None,
                }
            )