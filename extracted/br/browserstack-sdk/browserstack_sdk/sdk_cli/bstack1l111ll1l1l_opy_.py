# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
import inspect
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    AutomationFrameworkBrowser,
)
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1llll1llll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.constants import bstack1111l11ll_opy_
import threading
import os
from browserstack_sdk.browserstack_helper import BrowserStackHelper
from bstack_utils.performance_tester import PerformanceTester
from bstack_utils.bstack1111ll1l1l_opy_ import bstack1l1l1lll11l_opy_
import browserstack_sdk
class bstack1l1111l1l1l_opy_(BaseModule):
    bstack111lllll1l1_opy_ = bstack1l1llll_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡ࡬ࡲ࡮ࡺࠢᫌ")
    bstack111llll1lll_opy_ = bstack1l1llll_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵࠤᫍ")
    bstack111lll1ll11_opy_ = bstack1l1llll_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺ࡯ࡱࠤᫎ")
    def __init__(self, bstack111l1l11l_opy_):
        super().__init__()
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.CREATE, HookState.PRE), self.bstack111lll1ll1l_opy_)
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.PRE), self.bstack11l1lllllll_opy_)
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.POST), self.bstack11l111111ll_opy_)
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.POST), self.bstack111lll1lll1_opy_)
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.QUIT, HookState.POST), self.bstack11l111l111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack111lll1ll1l_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠥࡣࡤ࡯࡮ࡪࡶࡢࡣࠧ᫏"):
            return
        def wrapped(driver, init, *args, **kwargs):
            if args:
                try:
                    init_params = list(inspect.signature(init).parameters.values())
                    bstack11l111l1111_opy_ = any(
                        p.kind == inspect.Parameter.VAR_POSITIONAL for p in init_params
                    )
                    bstack11l11111lll_opy_ = [
                        p.name for p in init_params[1:]
                        if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                      inspect.Parameter.POSITIONAL_OR_KEYWORD)
                    ]
                    if not bstack11l111l1111_opy_ and len(args) <= len(bstack11l11111lll_opy_):
                        for value, name in zip(args, bstack11l11111lll_opy_):
                            if name not in kwargs:
                                kwargs[name] = value
                        args = ()
                except Exception as e:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠ࡯ࡱࡵࡱࡦࡲࡩࡻࡧࠣࡴࡴࡹࡩࡵ࡫ࡲࡲࡦࡲࠠࡥࡴ࡬ࡺࡪࡸࠠࡢࡴࡪࡷ࠿ࠦࡻࡾࠤ᫐").format(e))
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1llll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ᫑")), str):
                    url = kwargs.get(bstack1l1llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ᫒"))
                elif hasattr(kwargs.get(bstack1l1llll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥ᫓")), bstack1l1llll_opy_ (u"ࠨࡡࡦࡰ࡮࡫࡮ࡵࡡࡦࡳࡳ࡬ࡩࡨࠩ᫔")):
                    url = kwargs.get(bstack1l1llll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧ᫕"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᫖"))._url
            except Exception as e:
                url = bstack1l1llll_opy_ (u"ࠫࠬ᫗")
                self.logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡸ࡬ࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷࡀࠠࡼࡿࠥ᫘").format(e))
            self.logger.info(bstack1l1llll_opy_ (u"ࠨࡒࡦ࡯ࡲࡸࡪࠦࡓࡦࡴࡹࡩࡷࠦࡁࡥࡦࡵࡩࡸࡹࠠࡣࡧ࡬ࡲ࡬ࠦࡰࡢࡵࡶࡩࡩࠦࡡࡴࠢ࠽ࠤࢀࢃࠢ᫙").format(str(url)))
            bstack111lllll11l_opy_ = None
            driver_rank = None
            try:
                bstack111lllll11l_opy_ = BrowserStackHelper.get_driver_label()
                if bstack111lllll11l_opy_ is not None:
                    bstack111llll111l_opy_ = str(bstack111lllll11l_opy_)
                    if bstack1l1llll_opy_ (u"ࠢࠤࠤ᫚") in bstack111llll111l_opy_:
                        bstack11l1111111l_opy_ = bstack111llll111l_opy_.rsplit(bstack1l1llll_opy_ (u"ࠣࠥࠥ᫛"), 1)[1]
                        try:
                            driver_rank = int(bstack11l1111111l_opy_)
                        except ValueError as e:
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡧࡻࡸࡷࡧࡣࡵ࡫ࡱ࡫ࠥࡪࡲࡪࡸࡨࡶࠥࡸࡡ࡯࡭ࠣࡪࡷࡵ࡭ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽࡨࡼࡵࡲࡩࡤ࡫ࡷࡣࡱࡧࡢࡦ࡮ࢀࠫ࠿ࠦࠢ᫜") + str(e) + bstack1l1llll_opy_ (u"ࠥࠦ᫝"))
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡦࡸࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮࠽ࠤࠧ᫞") + str(e) + bstack1l1llll_opy_ (u"ࠧࠨ᫟"))
            self.bstack11l11111ll1_opy_(instance, url, f, driver_rank, kwargs)
            self.logger.info(bstack1l1llll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡲࡢࡰ࡮ࡁࢀࡪࡲࡪࡸࡨࡶࡤࡸࡡ࡯࡭ࢀࠤࡩࡸࡩࡷࡧࡵ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡦ࠯ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿ࠽ࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᫠") + str(kwargs) + bstack1l1llll_opy_ (u"ࠢࠣ᫡"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack11l1lllllll_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.get_state(instance, bstack1l1111l1l1l_opy_.bstack111lllll1l1_opy_, False):
            return
        if not f.has_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX):
            return
        platform_index = f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX)
        if f.bstack11ll111ll1l_opy_(method_name, *args) and len(args) > 1:
            time_start = datetime.now()
            hub_url = SeleniumFramework.hub_url(driver)
            self.logger.warning(bstack1l1llll_opy_ (u"ࠣࡪࡸࡦࡤࡻࡲ࡭࠿ࠥ᫢") + str(hub_url) + bstack1l1llll_opy_ (u"ࠤࠥ᫣"))
            bstack111lllll1ll_opy_ = args[1][bstack1l1llll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ᫤")] if isinstance(args[1], dict) and bstack1l1llll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ᫥") in args[1] else None
            bstack11l1111l11l_opy_ = bstack1l1llll_opy_ (u"ࠧࡧ࡬ࡸࡣࡼࡷࡒࡧࡴࡤࡪࠥ᫦")
            if isinstance(bstack111lllll1ll_opy_, dict):
                time_start = datetime.now()
                r = self.bstack11l111111l1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.add_benchmark(bstack1l1llll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡩ࡯࡫ࡷࠦ᫧"), datetime.now() - time_start)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1llll_opy_ (u"ࠢࡴࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭࠺ࠡࠤ᫨") + str(r) + bstack1l1llll_opy_ (u"ࠣࠤ᫩"))
                        return
                    if r.hub_url:
                        f.bstack111lll1llll_opy_(instance, driver, r.hub_url)
                        f.set_state(instance, bstack1l1111l1l1l_opy_.bstack111lllll1l1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1llll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ᫪"), e)
    def bstack11l111111ll_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = SeleniumFramework.session_id(driver)
            if session_id:
                bstack111lllll111_opy_ = bstack1l1llll_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧ᫫").format(session_id)
                PerformanceTester.mark(bstack111lllll111_opy_)
    def bstack111lll1lll1_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.get_state(instance, bstack1l1111l1l1l_opy_.bstack111llll1lll_opy_, False):
            return
        ref = instance.ref()
        hub_url = SeleniumFramework.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣ᫬") + str(hub_url) + bstack1l1llll_opy_ (u"ࠧࠨ᫭"))
            return
        framework_session_id = SeleniumFramework.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤ᫮") + str(framework_session_id) + bstack1l1llll_opy_ (u"ࠢࠣ᫯"))
            return
        if SeleniumFramework.bstack111lll1l1ll_opy_(*args) == SeleniumFramework.bstack111llll1111_opy_:
            bstack11l1111l1l1_opy_ = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠾ࡪࡴࡤࠣ᫰").format(framework_session_id)
            bstack111lllll111_opy_ = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠿ࡹࡴࡢࡴࡷࠦ᫱").format(framework_session_id)
            PerformanceTester.end(
                label=bstack1l1llll_opy_ (u"ࠥࡷࡩࡱ࠺ࡥࡴ࡬ࡺࡪࡸ࠺ࡱࡱࡶࡸ࠲࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡢࡶ࡬ࡳࡳࠨ᫲"),
                start=bstack111lllll111_opy_,
                end=bstack11l1111l1l1_opy_,
                status=True,
                failure=None
            )
            time_start = datetime.now()
            r = self.bstack11l1111ll1l_opy_(
                ref,
                f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.add_benchmark(bstack1l1llll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡸࡺࡡࡳࡶࠥ᫳"), datetime.now() - time_start)
            f.set_state(instance, bstack1l1111l1l1l_opy_.bstack111llll1lll_opy_, r.success)
    def bstack11l111l111l_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.get_state(instance, bstack1l1111l1l1l_opy_.bstack111lll1ll11_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = SeleniumFramework.session_id(driver)
        hub_url = SeleniumFramework.hub_url(driver)
        time_start = datetime.now()
        r = self.bstack111llllll11_opy_(
            ref,
            f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.add_benchmark(bstack1l1llll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡰࡲࠥ᫴"), datetime.now() - time_start)
        f.set_state(instance, bstack1l1111l1l1l_opy_.bstack111lll1ll11_opy_, r.success)
    @measure(event_name=EVENTS.bstack1l1llll1l1_opy_, stage=STAGE.SINGLE)
    def bstack11l11llllll_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes, driver_rank: int = None):
        is_secondary_driver = False
        if isinstance(driver_rank, int):
            is_secondary_driver = driver_rank > 1
        elif driver_rank is not None:
            try:
                bstack11l11111l11_opy_ = int(driver_rank)
                is_secondary_driver = bstack11l11111l11_opy_ > 1
            except (TypeError, ValueError):
                is_secondary_driver = False
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.is_secondary_driver = is_secondary_driver
        req.platform_index = 0 if req.is_secondary_driver else platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡹࡨࡦࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦ᫵") + str(req) + bstack1l1llll_opy_ (u"ࠢࠣ᫶"))
        try:
            r = self.cli_service.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦ᫷") + str(r.success) + bstack1l1llll_opy_ (u"ࠤࠥ᫸"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ᫹") + str(e) + bstack1l1llll_opy_ (u"ࠦࠧ᫺"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1111l1ll_opy_, stage=STAGE.SINGLE)
    def bstack11l111111l1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.ensure_bin_session()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ᫻").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣ᫼") + str(req) + bstack1l1llll_opy_ (u"ࠢࠣ᫽"))
        try:
            r = self.cli_service.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦ᫾") + str(r.success) + bstack1l1llll_opy_ (u"ࠤࠥ᫿"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᬀ") + str(e) + bstack1l1llll_opy_ (u"ࠦࠧᬁ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111llll11ll_opy_, stage=STAGE.SINGLE)
    def bstack11l1111ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.ensure_bin_session()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᬂ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺ࠺ࠡࠤᬃ") + str(req) + bstack1l1llll_opy_ (u"ࠢࠣᬄ"))
        try:
            r = self.cli_service.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᬅ") + str(r) + bstack1l1llll_opy_ (u"ࠤࠥᬆ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᬇ") + str(e) + bstack1l1llll_opy_ (u"ࠦࠧᬈ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack111llll1ll1_opy_, stage=STAGE.SINGLE)
    def bstack111llllll11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.ensure_bin_session()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᬉ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡳࡵࡀࠠࠣᬊ") + str(req) + bstack1l1llll_opy_ (u"ࠢࠣᬋ"))
        try:
            r = self.cli_service.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᬌ") + str(r) + bstack1l1llll_opy_ (u"ࠤࠥᬍ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᬎ") + str(e) + bstack1l1llll_opy_ (u"ࠦࠧᬏ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1lllll1l_opy_, stage=STAGE.SINGLE)
    def bstack11l11111ll1_opy_(self, instance: AutomationFrameworkBrowser, url: str, f: SeleniumFramework, driver_rank: int, kwargs):
        import browserstack_sdk, os
        bstack111llll11l1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠬࡕࡖࡆࡔࡕࡍࡉࡋ࡟ࡍࡑࡄࡈࡤ࡚ࡅࡔࡖࡌࡒࡌ࠭ᬐ"))
        if bstack111llll11l1_opy_ is not None:
            browserstack_sdk.bstack1l11l11l11_opy_ = bstack111llll11l1_opy_.lower() == bstack1l1llll_opy_ (u"࠭ࡴࡳࡷࡨࠫᬑ")
        bstack11l1111l111_opy_ = version.parse(f.framework_version)
        bstack111lllllll1_opy_ = f.platform_index
        bstack111llllllll_opy_ = kwargs.get(bstack1l1llll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᬒ"))
        bstack11l11111111_opy_ = kwargs.get(bstack1l1llll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᬓ"))
        bstack11l1ll11_opy_ = {}
        bstack111llllll1l_opy_ = {}
        bstack11l1111ll11_opy_ = None
        bstack111llll1l11_opy_ = {}
        if bstack11l11111111_opy_ is not None or bstack111llllllll_opy_ is not None: # check top level caps
            if bstack11l11111111_opy_ is not None:
                bstack111llll1l11_opy_[bstack1l1llll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᬔ")] = bstack11l11111111_opy_
            if bstack111llllllll_opy_ is not None and callable(getattr(bstack111llllllll_opy_, bstack1l1llll_opy_ (u"ࠥࡸࡴࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᬕ"))):
                bstack111llll1l11_opy_[bstack1l1llll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࡤࡧࡳࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᬖ")] = bstack111llllllll_opy_.to_capabilities()
        response = self.bstack11l11llllll_opy_(bstack111lllllll1_opy_, url, instance.ref(), json.dumps(bstack111llll1l11_opy_).encode(bstack1l1llll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᬗ")), driver_rank)
        if response is not None and response.capabilities:
            bstack11l1ll11_opy_ = json.loads(response.capabilities.decode(bstack1l1llll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᬘ")))
            if browserstack_sdk.bstack1l11l11l11_opy_:
                def bstack11l1111llll_opy_(d):
                    if not isinstance(d, dict):
                        return d
                    return {k: bstack11l1111llll_opy_(v) if isinstance(v, dict) else v
                            for k, v in d.items() if v is not None}
                bstack11l1ll11_opy_ = bstack11l1111llll_opy_(bstack11l1ll11_opy_)
                try:
                    bstack11l11111l1l_opy_ = None
                    if isinstance(bstack11l1ll11_opy_, dict):
                        if bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᬙ") in bstack11l1ll11_opy_:
                            bstack11l11111l1l_opy_ = bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᬚ"))
                        elif isinstance(bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠩࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠧᬛ")), dict):
                            bstack11l11111l1l_opy_ = bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᬜ")].get(bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᬝ"))
                        if isinstance(bstack11l11111l1l_opy_, dict) and bstack1l1llll_opy_ (u"ࠬࡵࡶࡦࡴࡵ࡭ࡩ࡫ࡌࡰࡣࡧࡘࡪࡹࡴࡪࡰࡪࠫᬞ") in bstack11l11111l1l_opy_:
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡒࡦ࡯ࡲࡺ࡮ࡴࡧࠡࡱࡹࡩࡷࡸࡩࡥࡧࡏࡳࡦࡪࡔࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡴࡲࡱࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡧ࡫ࡦࡰࡴࡨࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺ࡯ࠡࡪࡸࡦࠧᬟ"))
                            try:
                                bstack11l11111l1l_opy_.pop(bstack1l1llll_opy_ (u"ࠧࡰࡸࡨࡶࡷ࡯ࡤࡦࡎࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬࠭ᬠ"), None)
                            except Exception:
                                pass
                            if bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᬡ") in bstack11l1ll11_opy_:
                                bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᬢ")] = bstack11l11111l1l_opy_
                            if isinstance(bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠪࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠨᬣ")), dict):
                                bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠩᬤ")][bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᬥ")] = bstack11l11111l1l_opy_
                except Exception:
                    pass
            if not bstack11l1ll11_opy_ and not browserstack_sdk.bstack1l11l11l11_opy_:
                return
            bstack11l1111ll11_opy_ = f.bstack1l11l11l1l1_opy_[bstack1l1llll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥᬦ")](bstack11l1ll11_opy_)
        if bstack111llllllll_opy_ is not None and bstack11l1111l111_opy_ >= version.parse(bstack1l1llll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᬧ")):
            bstack111llllll1l_opy_ = None
        if (
                not bstack111llllllll_opy_ and not bstack11l11111111_opy_
        ) or (
                bstack11l1111l111_opy_ < version.parse(bstack1l1llll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᬨ"))
        ):
            bstack111llllll1l_opy_ = {}
            bstack111llllll1l_opy_.update(bstack11l1ll11_opy_)
        self.logger.info(bstack1llll1llll1_opy_)
        if browserstack_sdk.bstack1l11l11l11_opy_:
            bstack11l1111lll1_opy_ = bstack11l1111ll11_opy_ if bstack11l1111ll11_opy_ else bstack111llllllll_opy_
            if bstack11l1111lll1_opy_:
                bstack111111l1l1_opy_ = bstack1l1l1lll11l_opy_(bstack11l1111lll1_opy_, bstack1ll1111l1l_opy_=bstack1l1llll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᬩ"))
                if bstack11l1111lll1_opy_ is bstack111llllllll_opy_ and not bstack11l1111ll11_opy_:
                    bstack11l1111ll11_opy_ = bstack11l1111lll1_opy_
            kwargs.update({bstack1l1llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᬪ"): bstack1111l11ll_opy_})
        elif os.environ.get(bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢᬫ")).lower().__eq__(bstack1l1llll_opy_ (u"ࠧࡺࡲࡶࡧࠥᬬ")):
            kwargs.update({bstack1l1llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᬭ"): f.bstack111llll1l1l_opy_})
        if bstack11l1111l111_opy_ >= version.parse(bstack1l1llll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᬮ")):
            if bstack11l11111111_opy_ is not None:
                del kwargs[bstack1l1llll_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᬯ")]
            kwargs.update(
                {
                    bstack1l1llll_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᬰ"): bstack11l1111ll11_opy_,
                    bstack1l1llll_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᬱ"): True,
                    bstack1l1llll_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᬲ"): None,
                }
            )
        elif bstack11l1111l111_opy_ >= version.parse(bstack1l1llll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᬳ")):
            kwargs.update(
                {
                    bstack1l1llll_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨ᬴"): bstack111llllll1l_opy_,
                    bstack1l1llll_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣᬵ"): bstack11l1111ll11_opy_,
                    bstack1l1llll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᬶ"): True,
                    bstack1l1llll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᬷ"): None,
                }
            )
        elif bstack11l1111l111_opy_ >= version.parse(bstack1l1llll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᬸ")):
            kwargs.update(
                {
                    bstack1l1llll_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᬹ"): bstack111llllll1l_opy_,
                    bstack1l1llll_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᬺ"): True,
                    bstack1l1llll_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᬻ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1llll_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᬼ"): bstack111llllll1l_opy_,
                    bstack1l1llll_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧᬽ"): True,
                    bstack1l1llll_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤᬾ"): None,
                }
            )