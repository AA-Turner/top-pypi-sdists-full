# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11ll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
class bstack1ll1l1llll1_opy_(bstack1ll1ll1llll_opy_):
    bstack1l11lll1111_opy_ = bstack11ll11_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦዾ")
    bstack1l11lll1lll_opy_ = bstack11ll11_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨዿ")
    bstack1l1l1111111_opy_ = bstack11ll11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨጀ")
    def __init__(self, bstack1ll1ll11ll1_opy_):
        super().__init__()
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1llllll11l1_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l11lllll11_opy_)
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll111l1l11_opy_)
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.POST), self.bstack1l1l11111ll_opy_)
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.POST), self.bstack1l1l1111lll_opy_)
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.QUIT, bstack1llllll1111_opy_.POST), self.bstack1l11lllll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lllll11_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11ll11_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤጁ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦጂ")), str):
                    url = kwargs.get(bstack11ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧጃ"))
                elif hasattr(kwargs.get(bstack11ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨጄ")), bstack11ll11_opy_ (u"ࠫࡤࡩ࡬ࡪࡧࡱࡸࡤࡩ࡯࡯ࡨ࡬࡫ࠬጅ")):
                    url = kwargs.get(bstack11ll11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣጆ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack11ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤጇ"))._url
            except Exception as e:
                url = bstack11ll11_opy_ (u"ࠧࠨገ")
                self.logger.error(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡴ࡯ࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࢂࠨጉ").format(e))
            self.logger.info(bstack11ll11_opy_ (u"ࠤࡕࡩࡲࡵࡴࡦࠢࡖࡩࡷࡼࡥࡳࠢࡄࡨࡩࡸࡥࡴࡵࠣࡦࡪ࡯࡮ࡨࠢࡳࡥࡸࡹࡥࡥࠢࡤࡷࠥࡀࠠࡼࡿࠥጊ").format(str(url)))
            self.bstack1l1l1111l11_opy_(instance, url, f, kwargs)
            self.logger.info(bstack11ll11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃ࠺ࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣጋ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll111l1l11_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack1lllll1l1ll_opy_(instance, bstack1ll1l1llll1_opy_.bstack1l11lll1111_opy_, False):
            return
        if not f.bstack1lllll1l111_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_):
            return
        platform_index = f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_)
        if f.bstack1ll11lllll1_opy_(method_name, *args) and len(args) > 1:
            bstack1ll1lll1ll_opy_ = datetime.now()
            hub_url = bstack1llll11l111_opy_.hub_url(driver)
            self.logger.warning(bstack11ll11_opy_ (u"ࠦ࡭ࡻࡢࡠࡷࡵࡰࡂࠨጌ") + str(hub_url) + bstack11ll11_opy_ (u"ࠧࠨግ"))
            bstack1l1l1111ll1_opy_ = args[1][bstack11ll11_opy_ (u"ࠨࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧጎ")] if isinstance(args[1], dict) and bstack11ll11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጏ") in args[1] else None
            bstack1l1l111111l_opy_ = bstack11ll11_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨጐ")
            if isinstance(bstack1l1l1111ll1_opy_, dict):
                bstack1ll1lll1ll_opy_ = datetime.now()
                r = self.bstack1l11llll111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢ጑"), datetime.now() - bstack1ll1lll1ll_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11ll11_opy_ (u"ࠥࡷࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩ࠽ࠤࠧጒ") + str(r) + bstack11ll11_opy_ (u"ࠦࠧጓ"))
                        return
                    if r.hub_url:
                        f.bstack1l11llll1ll_opy_(instance, driver, r.hub_url)
                        f.bstack1llllllllll_opy_(instance, bstack1ll1l1llll1_opy_.bstack1l11lll1111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦጔ"), e)
    def bstack1l1l11111ll_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1llll11l111_opy_.session_id(driver)
            if session_id:
                bstack1l11llll11l_opy_ = bstack11ll11_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣጕ").format(session_id)
                bstack1ll1l1ll1l1_opy_.mark(bstack1l11llll11l_opy_)
    def bstack1l1l1111lll_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1l1ll_opy_(instance, bstack1ll1l1llll1_opy_.bstack1l11lll1lll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1llll11l111_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦ጖") + str(hub_url) + bstack11ll11_opy_ (u"ࠣࠤ጗"))
            return
        framework_session_id = bstack1llll11l111_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡁࠧጘ") + str(framework_session_id) + bstack11ll11_opy_ (u"ࠥࠦጙ"))
            return
        if bstack1llll11l111_opy_.bstack1l1l11111l1_opy_(*args) == bstack1llll11l111_opy_.bstack1l1l111l11l_opy_:
            bstack1l11lll11ll_opy_ = bstack11ll11_opy_ (u"ࠦࢀࢃ࠺ࡦࡰࡧࠦጚ").format(framework_session_id)
            bstack1l11llll11l_opy_ = bstack11ll11_opy_ (u"ࠧࢁࡽ࠻ࡵࡷࡥࡷࡺࠢጛ").format(framework_session_id)
            bstack1ll1l1ll1l1_opy_.end(
                label=bstack11ll11_opy_ (u"ࠨࡳࡥ࡭࠽ࡨࡷ࡯ࡶࡦࡴ࠽ࡴࡴࡹࡴ࠮࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡥࡹ࡯࡯࡯ࠤጜ"),
                start=bstack1l11llll11l_opy_,
                end=bstack1l11lll11ll_opy_,
                status=True,
                failure=None
            )
            bstack1ll1lll1ll_opy_ = datetime.now()
            r = self.bstack1l11ll1lll1_opy_(
                ref,
                f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࠨጝ"), datetime.now() - bstack1ll1lll1ll_opy_)
            f.bstack1llllllllll_opy_(instance, bstack1ll1l1llll1_opy_.bstack1l11lll1lll_opy_, r.success)
    def bstack1l11lllll1l_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1lllll1l1ll_opy_(instance, bstack1ll1l1llll1_opy_.bstack1l1l1111111_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1llll11l111_opy_.session_id(driver)
        hub_url = bstack1llll11l111_opy_.hub_url(driver)
        bstack1ll1lll1ll_opy_ = datetime.now()
        r = self.bstack1l11llll1l1_opy_(
            ref,
            f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࠨጞ"), datetime.now() - bstack1ll1lll1ll_opy_)
        f.bstack1llllllllll_opy_(instance, bstack1ll1l1llll1_opy_.bstack1l1l1111111_opy_, r.success)
    @measure(event_name=EVENTS.bstack111llll1_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l1l11lll1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack11ll11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢጟ") + str(req) + bstack11ll11_opy_ (u"ࠥࠦጠ"))
        try:
            r = self.bstack1llll1l1l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢጡ") + str(r.success) + bstack11ll11_opy_ (u"ࠧࠨጢ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦጣ") + str(e) + bstack11ll11_opy_ (u"ࠢࠣጤ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll111l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l11llll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11ll11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴ࠻ࠢࠥጥ") + str(req) + bstack11ll11_opy_ (u"ࠤࠥጦ"))
        try:
            r = self.bstack1llll1l1l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࡸࡻࡣࡤࡧࡶࡷࡂࠨጧ") + str(r.success) + bstack11ll11_opy_ (u"ࠦࠧጨ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥጩ") + str(e) + bstack11ll11_opy_ (u"ࠨࠢጪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lllllll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l11ll1lll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴ࠻ࠢࠥጫ") + str(req) + bstack11ll11_opy_ (u"ࠣࠤጬ"))
        try:
            r = self.bstack1llll1l1l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦጭ") + str(r) + bstack11ll11_opy_ (u"ࠥࠦጮ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤጯ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨጰ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll11l1_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l11llll1l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࡀࠠࠣጱ") + str(req) + bstack11ll11_opy_ (u"ࠢࠣጲ"))
        try:
            r = self.bstack1llll1l1l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥጳ") + str(r) + bstack11ll11_opy_ (u"ࠤࠥጴ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣጵ") + str(e) + bstack11ll11_opy_ (u"ࠦࠧጶ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1llll1l11l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l1l1111l11_opy_(self, instance: bstack1llll1ll1ll_opy_, url: str, f: bstack1llll11l111_opy_, kwargs):
        bstack1l11lll1l1l_opy_ = version.parse(f.framework_version)
        bstack1l1l111l111_opy_ = kwargs.get(bstack11ll11_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨጷ"))
        bstack1l11llllll1_opy_ = kwargs.get(bstack11ll11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጸ"))
        bstack1l1l11lllll_opy_ = {}
        bstack1l11lll1l11_opy_ = {}
        bstack1l1l1111l1l_opy_ = None
        bstack1l11lll1ll1_opy_ = {}
        if bstack1l11llllll1_opy_ is not None or bstack1l1l111l111_opy_ is not None: # check top level caps
            if bstack1l11llllll1_opy_ is not None:
                bstack1l11lll1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧጹ")] = bstack1l11llllll1_opy_
            if bstack1l1l111l111_opy_ is not None and callable(getattr(bstack1l1l111l111_opy_, bstack11ll11_opy_ (u"ࠣࡶࡲࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥጺ"))):
                bstack1l11lll1ll1_opy_[bstack11ll11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࡢࡥࡸࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬጻ")] = bstack1l1l111l111_opy_.to_capabilities()
        response = self.bstack1l1l11lll1l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11lll1ll1_opy_).encode(bstack11ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤጼ")))
        if response is not None and response.capabilities:
            bstack1l1l11lllll_opy_ = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥጽ")))
            if not bstack1l1l11lllll_opy_: # empty caps bstack1l1l1l11lll_opy_ bstack1l1l11llll1_opy_ bstack1l1l1l11ll1_opy_ bstack1lll11111ll_opy_ or error in processing
                return
            bstack1l1l1111l1l_opy_ = f.bstack1lll111l11l_opy_[bstack11ll11_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤጾ")](bstack1l1l11lllll_opy_)
        if bstack1l1l111l111_opy_ is not None and bstack1l11lll1l1l_opy_ >= version.parse(bstack11ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬጿ")):
            bstack1l11lll1l11_opy_ = None
        if (
                not bstack1l1l111l111_opy_ and not bstack1l11llllll1_opy_
        ) or (
                bstack1l11lll1l1l_opy_ < version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ፀ"))
        ):
            bstack1l11lll1l11_opy_ = {}
            bstack1l11lll1l11_opy_.update(bstack1l1l11lllll_opy_)
        self.logger.info(bstack1l11ll1l1l_opy_)
        if os.environ.get(bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦፁ")).lower().__eq__(bstack11ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢፂ")):
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨፃ"): f.bstack1l11ll1llll_opy_,
                }
            )
        if bstack1l11lll1l1l_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫፄ")):
            if bstack1l11llllll1_opy_ is not None:
                del kwargs[bstack11ll11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧፅ")]
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢፆ"): bstack1l1l1111l1l_opy_,
                    bstack11ll11_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦፇ"): True,
                    bstack11ll11_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣፈ"): None,
                }
            )
        elif bstack1l11lll1l1l_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨፉ")):
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥፊ"): bstack1l11lll1l11_opy_,
                    bstack11ll11_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧፋ"): bstack1l1l1111l1l_opy_,
                    bstack11ll11_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤፌ"): True,
                    bstack11ll11_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨፍ"): None,
                }
            )
        elif bstack1l11lll1l1l_opy_ >= version.parse(bstack11ll11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧፎ")):
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣፏ"): bstack1l11lll1l11_opy_,
                    bstack11ll11_opy_ (u"ࠤ࡮ࡩࡪࡶ࡟ࡢ࡮࡬ࡺࡪࠨፐ"): True,
                    bstack11ll11_opy_ (u"ࠥࡪ࡮ࡲࡥࡠࡦࡨࡸࡪࡩࡴࡰࡴࠥፑ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11ll11_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦፒ"): bstack1l11lll1l11_opy_,
                    bstack11ll11_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤፓ"): True,
                    bstack11ll11_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨፔ"): None,
                }
            )