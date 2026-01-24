# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l111lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
class bstack1ll1ll11lll_opy_(bstack1ll1ll111l1_opy_):
    bstack1l1111l1111_opy_ = bstack1l1111_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᑤ")
    bstack1l111l11l1l_opy_ = bstack1l1111_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᑥ")
    bstack1l1111l11ll_opy_ = bstack1l1111_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᑦ")
    def __init__(self, bstack1ll1l1l1111_opy_):
        super().__init__()
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l1111ll11l_opy_)
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l1l1ll11l1_opy_)
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.POST), self.bstack1l1111lllll_opy_)
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.POST), self.bstack1l111l1111l_opy_)
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.QUIT, bstack1lll1l1ll1l_opy_.POST), self.bstack1l1111l1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111ll11l_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1111_opy_ (u"ࠣࡡࡢ࡭ࡳ࡯ࡴࡠࡡࠥᑧ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᑨ")), str):
                    url = kwargs.get(bstack1l1111_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᑩ"))
                elif hasattr(kwargs.get(bstack1l1111_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᑪ")), bstack1l1111_opy_ (u"ࠬࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬࠭ᑫ")):
                    url = kwargs.get(bstack1l1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᑬ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᑭ"))._url
            except Exception as e:
                url = bstack1l1111_opy_ (u"ࠨࠩᑮ")
                self.logger.error(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡵࡰࠥ࡬ࡲࡰ࡯ࠣࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀࢃࠢᑯ").format(e))
            self.logger.info(bstack1l1111_opy_ (u"ࠥࡖࡪࡳ࡯ࡵࡧࠣࡗࡪࡸࡶࡦࡴࠣࡅࡩࡪࡲࡦࡵࡶࠤࡧ࡫ࡩ࡯ࡩࠣࡴࡦࡹࡳࡦࡦࠣࡥࡸࠦ࠺ࠡࡽࢀࠦᑰ").format(str(url)))
            self.bstack1l11111llll_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l1111_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽ࠻ࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤᑱ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1l1ll11l1_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll1l11lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1l1111l1111_opy_, False):
            return
        if not f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_):
            return
        platform_index = f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_)
        if f.bstack1l1lll1lll1_opy_(method_name, *args) and len(args) > 1:
            bstack1ll1lll11l_opy_ = datetime.now()
            hub_url = bstack1ll1l111l1l_opy_.hub_url(driver)
            self.logger.warning(bstack1l1111_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᑲ") + str(hub_url) + bstack1l1111_opy_ (u"ࠨࠢᑳ"))
            bstack1l1111l1ll1_opy_ = args[1][bstack1l1111_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᑴ")] if isinstance(args[1], dict) and bstack1l1111_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᑵ") in args[1] else None
            bstack1l1111lll11_opy_ = bstack1l1111_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢᑶ")
            if isinstance(bstack1l1111l1ll1_opy_, dict):
                bstack1ll1lll11l_opy_ = datetime.now()
                r = self.bstack1l111l111l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣᑷ"), datetime.now() - bstack1ll1lll11l_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1111_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨᑸ") + str(r) + bstack1l1111_opy_ (u"ࠧࠨᑹ"))
                        return
                    if r.hub_url:
                        f.bstack1l1111lll1l_opy_(instance, driver, r.hub_url)
                        f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll11lll_opy_.bstack1l1111l1111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧᑺ"), e)
    def bstack1l1111lllll_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1l111l1l_opy_.session_id(driver)
            if session_id:
                bstack1l1111ll1l1_opy_ = bstack1l1111_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤᑻ").format(session_id)
                bstack11ll111lll_opy_.mark(bstack1l1111ll1l1_opy_)
    def bstack1l111l1111l_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1l11lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1l111l11l1l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1l111l1l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧᑼ") + str(hub_url) + bstack1l1111_opy_ (u"ࠤࠥᑽ"))
            return
        framework_session_id = bstack1ll1l111l1l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨᑾ") + str(framework_session_id) + bstack1l1111_opy_ (u"ࠦࠧᑿ"))
            return
        if bstack1ll1l111l1l_opy_.bstack1l1111ll1ll_opy_(*args) == bstack1ll1l111l1l_opy_.bstack1l111l11111_opy_:
            bstack1l1111l1lll_opy_ = bstack1l1111_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧᒀ").format(framework_session_id)
            bstack1l1111ll1l1_opy_ = bstack1l1111_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᒁ").format(framework_session_id)
            bstack11ll111lll_opy_.end(
                label=bstack1l1111_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥᒂ"),
                start=bstack1l1111ll1l1_opy_,
                end=bstack1l1111l1lll_opy_,
                status=True,
                failure=None
            )
            bstack1ll1lll11l_opy_ = datetime.now()
            r = self.bstack1l1111l1l1l_opy_(
                ref,
                f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢᒃ"), datetime.now() - bstack1ll1lll11l_opy_)
            f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll11lll_opy_.bstack1l111l11l1l_opy_, r.success)
    def bstack1l1111l1l11_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1l11lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1l1111l11ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1l111l1l_opy_.session_id(driver)
        hub_url = bstack1ll1l111l1l_opy_.hub_url(driver)
        bstack1ll1lll11l_opy_ = datetime.now()
        r = self.bstack1l1111l11l1_opy_(
            ref,
            f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢᒄ"), datetime.now() - bstack1ll1lll11l_opy_)
        f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll11lll_opy_.bstack1l1111l11ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1llll1l1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l11l1111l1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᒅ") + str(req) + bstack1l1111_opy_ (u"ࠦࠧᒆ"))
        try:
            r = self.bstack1ll1111l1ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᒇ") + str(r.success) + bstack1l1111_opy_ (u"ࠨࠢᒈ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒉ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᒊ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111l11l11_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l111l111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᒋ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᒌ") + str(req) + bstack1l1111_opy_ (u"ࠦࠧᒍ"))
        try:
            r = self.bstack1ll1111l1ll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣᒎ") + str(r.success) + bstack1l1111_opy_ (u"ࠨࠢᒏ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒐ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᒑ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111l1l111_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l1111l1l1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᒒ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷ࠾ࠥࠨᒓ") + str(req) + bstack1l1111_opy_ (u"ࠦࠧᒔ"))
        try:
            r = self.bstack1ll1111l1ll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᒕ") + str(r) + bstack1l1111_opy_ (u"ࠨࠢᒖ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒗ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᒘ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111l111l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l1111l11l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᒙ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1111_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲ࠽ࠤࠧᒚ") + str(req) + bstack1l1111_opy_ (u"ࠦࠧᒛ"))
        try:
            r = self.bstack1ll1111l1ll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᒜ") + str(r) + bstack1l1111_opy_ (u"ࠨࠢᒝ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒞ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤᒟ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lllllll1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l11111llll_opy_(self, instance: bstack1lll1l1111l_opy_, url: str, f: bstack1ll1l111l1l_opy_, kwargs):
        bstack1l1111llll1_opy_ = version.parse(f.framework_version)
        bstack1l111l11lll_opy_ = kwargs.get(bstack1l1111_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᒠ"))
        bstack1l1111ll111_opy_ = kwargs.get(bstack1l1111_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᒡ"))
        bstack1l11l11l1l1_opy_ = {}
        bstack1l111l111ll_opy_ = {}
        bstack1l111l1l11l_opy_ = None
        bstack1l11111lll1_opy_ = {}
        if bstack1l1111ll111_opy_ is not None or bstack1l111l11lll_opy_ is not None: # check top level caps
            if bstack1l1111ll111_opy_ is not None:
                bstack1l11111lll1_opy_[bstack1l1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᒢ")] = bstack1l1111ll111_opy_
            if bstack1l111l11lll_opy_ is not None and callable(getattr(bstack1l111l11lll_opy_, bstack1l1111_opy_ (u"ࠧࡺ࡯ࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒣ"))):
                bstack1l11111lll1_opy_[bstack1l1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡢࡵࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᒤ")] = bstack1l111l11lll_opy_.to_capabilities()
        response = self.bstack1l11l1111l1_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11111lll1_opy_).encode(bstack1l1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᒥ")))
        if response is not None and response.capabilities:
            bstack1l11l11l1l1_opy_ = json.loads(response.capabilities.decode(bstack1l1111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒦ")))
            if not bstack1l11l11l1l1_opy_: # empty caps bstack1l11l11111l_opy_ bstack1l11l11l1ll_opy_ bstack1l11l11ll1l_opy_ bstack1ll1l11lll1_opy_ or error in processing
                return
            bstack1l111l1l11l_opy_ = f.bstack1lll11111l1_opy_[bstack1l1111_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡪࡷࡵ࡭ࡠࡥࡤࡴࡸࠨᒧ")](bstack1l11l11l1l1_opy_)
        if bstack1l111l11lll_opy_ is not None and bstack1l1111llll1_opy_ >= version.parse(bstack1l1111_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᒨ")):
            bstack1l111l111ll_opy_ = None
        if (
                not bstack1l111l11lll_opy_ and not bstack1l1111ll111_opy_
        ) or (
                bstack1l1111llll1_opy_ < version.parse(bstack1l1111_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᒩ"))
        ):
            bstack1l111l111ll_opy_ = {}
            bstack1l111l111ll_opy_.update(bstack1l11l11l1l1_opy_)
        self.logger.info(bstack1l111lll11_opy_)
        if os.environ.get(bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠣᒪ")).lower().__eq__(bstack1l1111_opy_ (u"ࠨࡴࡳࡷࡨࠦᒫ")):
            kwargs.update(
                {
                    bstack1l1111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᒬ"): f.bstack1l111l11ll1_opy_,
                }
            )
        if bstack1l1111llll1_opy_ >= version.parse(bstack1l1111_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᒭ")):
            if bstack1l1111ll111_opy_ is not None:
                del kwargs[bstack1l1111_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᒮ")]
            kwargs.update(
                {
                    bstack1l1111_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᒯ"): bstack1l111l1l11l_opy_,
                    bstack1l1111_opy_ (u"ࠦࡰ࡫ࡥࡱࡡࡤࡰ࡮ࡼࡥࠣᒰ"): True,
                    bstack1l1111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡢࡨࡪࡺࡥࡤࡶࡲࡶࠧᒱ"): None,
                }
            )
        elif bstack1l1111llll1_opy_ >= version.parse(bstack1l1111_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᒲ")):
            kwargs.update(
                {
                    bstack1l1111_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒳ"): bstack1l111l111ll_opy_,
                    bstack1l1111_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᒴ"): bstack1l111l1l11l_opy_,
                    bstack1l1111_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᒵ"): True,
                    bstack1l1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᒶ"): None,
                }
            )
        elif bstack1l1111llll1_opy_ >= version.parse(bstack1l1111_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᒷ")):
            kwargs.update(
                {
                    bstack1l1111_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᒸ"): bstack1l111l111ll_opy_,
                    bstack1l1111_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥᒹ"): True,
                    bstack1l1111_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢᒺ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1111_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᒻ"): bstack1l111l111ll_opy_,
                    bstack1l1111_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨᒼ"): True,
                    bstack1l1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥᒽ"): None,
                }
            )