# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll11lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack111l1l1111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
class bstack1ll11ll1111_opy_(bstack1ll1l11l1ll_opy_):
    bstack1l111l1111l_opy_ = bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦᑪ")
    bstack1l11111ll11_opy_ = bstack11l1ll1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨᑫ")
    bstack1l1111l1111_opy_ = bstack11l1ll1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨᑬ")
    def __init__(self, bstack1ll1l11ll11_opy_):
        super().__init__()
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1l1l11l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11111lll1_opy_)
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l1l1ll1111_opy_)
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.POST), self.bstack1l1111ll1l1_opy_)
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.POST), self.bstack1l1111lll1l_opy_)
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.QUIT, bstack1lll1ll1l11_opy_.POST), self.bstack1l1111l111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11111lll1_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1ll1_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᑭ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11l1ll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᑮ")), str):
                    url = kwargs.get(bstack11l1ll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᑯ"))
                elif hasattr(kwargs.get(bstack11l1ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᑰ")), bstack11l1ll1_opy_ (u"ࠫࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠬᑱ")):
                    url = kwargs.get(bstack11l1ll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᑲ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11l1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᑳ"))._url
            except Exception as e:
                url = bstack11l1ll1_opy_ (u"ࠧࠨᑴ")
                self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡴ࡯ࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࢂࠨᑵ").format(e))
            self.logger.info(bstack11l1ll1_opy_ (u"ࠤࡕࡩࡲࡵࡴࡦࠢࡖࡩࡷࡼࡥࡳࠢࡄࡨࡩࡸࡥࡴࡵࠣࡦࡪ࡯࡮ࡨࠢࡳࡥࡸࡹࡥࡥࠢࡤࡷࠥࡀࠠࡼࡿࠥᑶ").format(str(url)))
            self.bstack1l111l111ll_opy_(instance, url, f, kwargs)
            self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣᑷ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1l1l1ll1111_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lll1ll11l1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l111l1111l_opy_, False):
            return
        if not f.bstack1lll11l1111_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_):
            return
        platform_index = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_)
        if f.bstack1l1ll11l1l1_opy_(method_name, *args) and len(args) > 1:
            bstack111ll1ll1_opy_ = datetime.now()
            hub_url = bstack1ll1ll1lll1_opy_.hub_url(driver)
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࡂࠨᑸ") + str(hub_url) + bstack11l1ll1_opy_ (u"ࠧࠨᑹ"))
            bstack1l1111lllll_opy_ = args[1][bstack11l1ll1_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᑺ")] if isinstance(args[1], dict) and bstack11l1ll1_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᑻ") in args[1] else None
            bstack1l1111l11ll_opy_ = bstack11l1ll1_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨᑼ")
            if isinstance(bstack1l1111lllll_opy_, dict):
                bstack111ll1ll1_opy_ = datetime.now()
                r = self.bstack1l1111ll11l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢᑽ"), datetime.now() - bstack111ll1ll1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡷࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩ࠽ࠤࠧᑾ") + str(r) + bstack11l1ll1_opy_ (u"ࠦࠧᑿ"))
                        return
                    if r.hub_url:
                        f.bstack1l1111l11l1_opy_(instance, driver, r.hub_url)
                        f.bstack1lll1l1111l_opy_(instance, bstack1ll11ll1111_opy_.bstack1l111l1111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l1ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᒀ"), e)
    def bstack1l1111ll1l1_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1ll1ll1lll1_opy_.session_id(driver)
            if session_id:
                bstack1l111l11ll1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣᒁ").format(session_id)
                bstack1ll1111ll_opy_.mark(bstack1l111l11ll1_opy_)
    def bstack1l1111lll1l_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1ll11l1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l11111ll11_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1ll1ll1lll1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᒂ") + str(hub_url) + bstack11l1ll1_opy_ (u"ࠣࠤᒃ"))
            return
        framework_session_id = bstack1ll1ll1lll1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧᒄ") + str(framework_session_id) + bstack11l1ll1_opy_ (u"ࠥࠦᒅ"))
            return
        if bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_(*args) == bstack1ll1ll1lll1_opy_.bstack1l11111llll_opy_:
            bstack1l1111l1l11_opy_ = bstack11l1ll1_opy_ (u"ࠦࢀࢃ࠺ࡦࡰࡧࠦᒆ").format(framework_session_id)
            bstack1l111l11ll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢᒇ").format(framework_session_id)
            bstack1ll1111ll_opy_.end(
                label=bstack11l1ll1_opy_ (u"ࠨࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠤᒈ"),
                start=bstack1l111l11ll1_opy_,
                end=bstack1l1111l1l11_opy_,
                status=True,
                failure=None
            )
            bstack111ll1ll1_opy_ = datetime.now()
            r = self.bstack1l11111l1ll_opy_(
                ref,
                f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨᒉ"), datetime.now() - bstack111ll1ll1_opy_)
            f.bstack1lll1l1111l_opy_(instance, bstack1ll11ll1111_opy_.bstack1l11111ll11_opy_, r.success)
    def bstack1l1111l111l_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lll1ll11l1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1111l1111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1ll1ll1lll1_opy_.session_id(driver)
        hub_url = bstack1ll1ll1lll1_opy_.hub_url(driver)
        bstack111ll1ll1_opy_ = datetime.now()
        r = self.bstack1l111l11111_opy_(
            ref,
            f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨᒊ"), datetime.now() - bstack111ll1ll1_opy_)
        f.bstack1lll1l1111l_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1111l1111_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lllll111l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l111lllll1_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢᒋ") + str(req) + bstack11l1ll1_opy_ (u"ࠥࠦᒌ"))
        try:
            r = self.bstack1ll1llll1ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᒍ") + str(r.success) + bstack11l1ll1_opy_ (u"ࠧࠨᒎ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᒏ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣᒐ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l111l11l1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l1111ll11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᒑ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦᒒ") + str(req) + bstack11l1ll1_opy_ (u"ࠥࠦᒓ"))
        try:
            r = self.bstack1ll1llll1ll_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢᒔ") + str(r.success) + bstack11l1ll1_opy_ (u"ࠧࠨᒕ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᒖ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣᒗ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1111llll1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l11111l1ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᒘ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶ࠽ࠤࠧᒙ") + str(req) + bstack11l1ll1_opy_ (u"ࠥࠦᒚ"))
        try:
            r = self.bstack1ll1llll1ll_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᒛ") + str(r) + bstack11l1ll1_opy_ (u"ࠧࠨᒜ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᒝ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣᒞ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11111ll1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l111l11111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᒟ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱ࠼ࠣࠦᒠ") + str(req) + bstack11l1ll1_opy_ (u"ࠥࠦᒡ"))
        try:
            r = self.bstack1ll1llll1ll_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᒢ") + str(r) + bstack11l1ll1_opy_ (u"ࠧࠨᒣ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᒤ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣᒥ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111lll11ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l111l111ll_opy_(self, instance: bstack1lll11lll1l_opy_, url: str, f: bstack1ll1ll1lll1_opy_, kwargs):
        bstack1l1111l1ll1_opy_ = version.parse(f.framework_version)
        bstack1l111l111l1_opy_ = kwargs.get(bstack11l1ll1_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤᒦ"))
        bstack1l111l11l11_opy_ = kwargs.get(bstack11l1ll1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᒧ"))
        bstack1l11l11111l_opy_ = {}
        bstack1l1111l1lll_opy_ = {}
        bstack1l1111lll11_opy_ = None
        bstack1l1111ll1ll_opy_ = {}
        if bstack1l111l11l11_opy_ is not None or bstack1l111l111l1_opy_ is not None: # check top level caps
            if bstack1l111l11l11_opy_ is not None:
                bstack1l1111ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᒨ")] = bstack1l111l11l11_opy_
            if bstack1l111l111l1_opy_ is not None and callable(getattr(bstack1l111l111l1_opy_, bstack11l1ll1_opy_ (u"ࠦࡹࡵ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᒩ"))):
                bstack1l1111ll1ll_opy_[bstack11l1ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸࡥࡡࡴࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᒪ")] = bstack1l111l111l1_opy_.to_capabilities()
        response = self.bstack1l111lllll1_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l1111ll1ll_opy_).encode(bstack11l1ll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᒫ")))
        if response is not None and response.capabilities:
            bstack1l11l11111l_opy_ = json.loads(response.capabilities.decode(bstack11l1ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᒬ")))
            if not bstack1l11l11111l_opy_: # empty caps bstack1l111llll1l_opy_ bstack1l11l1111ll_opy_ bstack1l11l11l111_opy_ bstack1ll1l1l11l1_opy_ or error in processing
                return
            bstack1l1111lll11_opy_ = f.bstack1ll1lll1l1l_opy_[bstack11l1ll1_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧᒭ")](bstack1l11l11111l_opy_)
        if bstack1l111l111l1_opy_ is not None and bstack1l1111l1ll1_opy_ >= version.parse(bstack11l1ll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᒮ")):
            bstack1l1111l1lll_opy_ = None
        if (
                not bstack1l111l111l1_opy_ and not bstack1l111l11l11_opy_
        ) or (
                bstack1l1111l1ll1_opy_ < version.parse(bstack11l1ll1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᒯ"))
        ):
            bstack1l1111l1lll_opy_ = {}
            bstack1l1111l1lll_opy_.update(bstack1l11l11111l_opy_)
        self.logger.info(bstack111l1l1111_opy_)
        if os.environ.get(bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᒰ")).lower().__eq__(bstack11l1ll1_opy_ (u"ࠧࡺࡲࡶࡧࠥᒱ")):
            kwargs.update(
                {
                    bstack11l1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᒲ"): f.bstack1l1111l1l1l_opy_,
                }
            )
        if bstack1l1111l1ll1_opy_ >= version.parse(bstack11l1ll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᒳ")):
            if bstack1l111l11l11_opy_ is not None:
                del kwargs[bstack11l1ll1_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᒴ")]
            kwargs.update(
                {
                    bstack11l1ll1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᒵ"): bstack1l1111lll11_opy_,
                    bstack11l1ll1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᒶ"): True,
                    bstack11l1ll1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᒷ"): None,
                }
            )
        elif bstack1l1111l1ll1_opy_ >= version.parse(bstack11l1ll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᒸ")):
            kwargs.update(
                {
                    bstack11l1ll1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᒹ"): bstack1l1111l1lll_opy_,
                    bstack11l1ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᒺ"): bstack1l1111lll11_opy_,
                    bstack11l1ll1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᒻ"): True,
                    bstack11l1ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᒼ"): None,
                }
            )
        elif bstack1l1111l1ll1_opy_ >= version.parse(bstack11l1ll1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᒽ")):
            kwargs.update(
                {
                    bstack11l1ll1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᒾ"): bstack1l1111l1lll_opy_,
                    bstack11l1ll1_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᒿ"): True,
                    bstack11l1ll1_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᓀ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l1ll1_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᓁ"): bstack1l1111l1lll_opy_,
                    bstack11l1ll1_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᓂ"): True,
                    bstack11l1ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᓃ"): None,
                }
            )