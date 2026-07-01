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
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    AutomationFrameworkBrowser,
)
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.module_base import BaseModule
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.performance_tester import PerformanceTester
import traceback
import os
import threading
import time
class bstack1l11111ll1l_opy_(BaseModule):
    bstack11ll111l1ll_opy_ = False
    def __init__(self):
        super().__init__()
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.PRE), self.bstack11l1lllllll_opy_)
    def is_enabled(self) -> bool:
        return True
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
        hub_url = f.hub_url(driver)
        if f.bstack11ll11111l1_opy_(hub_url):
            if not bstack1l11111ll1l_opy_.bstack11ll111l1ll_opy_:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࠥࡹࡥ࡭ࡨ࠰࡬ࡪࡧ࡬ࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᥦ") + str(hub_url) + bstack1l1llll_opy_ (u"ࠢࠣᥧ"))
                bstack1l11111ll1l_opy_.bstack11ll111l1ll_opy_ = True
            return
        command_name = f.parse_command_name(*args)
        bstack11ll1111ll1_opy_ = f.bstack11ll1111l1l_opy_(*args)
        if command_name and command_name.lower() == bstack1l1llll_opy_ (u"ࠣࡨ࡬ࡲࡩ࡫࡬ࡦ࡯ࡨࡲࡹࠨᥨ") and bstack11ll1111ll1_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack11ll1111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᥩ"), None), bstack11ll1111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᥪ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠦࢀࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡷࡶ࡭ࡳ࡭࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡹࡥࡱࡻࡥ࠾ࠤᥫ") + str(locator_value) + bstack1l1llll_opy_ (u"ࠧࠨᥬ"))
                return
            def bstack1l11ll1l1ll_opy_(driver, bstack11ll1111lll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack11ll1111lll_opy_(driver, *args, **kwargs)
                    response = self.bstack11ll1111l11_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1llll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᥭ") + str(locator_value) + bstack1l1llll_opy_ (u"ࠢࠣ᥮"))
                    else:
                        self.logger.warning(bstack1l1llll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦ᥯") + str(response) + bstack1l1llll_opy_ (u"ࠤࠥᥰ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__11l1lllll1l_opy_(
                        driver, bstack11ll1111lll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1l11ll1l1ll_opy_.__name__ = command_name
            return bstack1l11ll1l1ll_opy_
    def __11l1lllll1l_opy_(
        self,
        driver,
        bstack11ll1111lll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack11ll1111l11_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡺࡲࡪࡩࡪࡩࡷ࡫ࡤ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᥱ") + str(locator_value) + bstack1l1llll_opy_ (u"ࠦࠧᥲ"))
                bstack11ll11111ll_opy_ = self.bstack11ll111111l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1llll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣ࡬ࡪࡧ࡬ࡪࡰࡪࡣࡷ࡫ࡳࡶ࡮ࡷࡁࠧᥳ") + str(bstack11ll11111ll_opy_) + bstack1l1llll_opy_ (u"ࠨࠢᥴ"))
                if bstack11ll11111ll_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1llll_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨ᥵"): bstack11ll11111ll_opy_.locator_type,
                            bstack1l1llll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢ᥶"): bstack11ll11111ll_opy_.locator_value,
                        }
                    )
                    return bstack11ll1111lll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡌࡣࡉࡋࡂࡖࡉࠥ᥷"), False):
                    self.logger.info(bstack1l11lll11ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠲ࡳࡩࡴࡵ࡬ࡲ࡬ࡀࠠࡴ࡮ࡨࡩࡵ࠮࠳࠱ࠫࠣࡰࡪࡺࡴࡪࡰࡪࠤࡾࡵࡵࠡ࡫ࡱࡷࡵ࡫ࡣࡵࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡰࡴ࡭ࡳࠣ᥸"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢ᥹") + str(response) + bstack1l1llll_opy_ (u"ࠧࠨ᥺"))
        except Exception as err:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ᥻") + str(err) + bstack1l1llll_opy_ (u"ࠢࠣ᥼"))
        raise exception
    @measure(event_name=EVENTS.bstack11ll1111111_opy_, stage=STAGE.SINGLE)
    def bstack11ll1111l11_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1llll_opy_ (u"ࠣ࠲ࠥ᥽"),
    ):
        self.ensure_bin_session()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1llll_opy_ (u"ࠤࠥ᥾")
        req.locator_type = locator_type
        req.locator_value = locator_value
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᥿").format(threading.get_ident(), os.getpid())
        try:
            r = self.cli_service.AISelfHealStep(req)
            self.logger.info(bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᦀ") + str(r) + bstack1l1llll_opy_ (u"ࠧࠨᦁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᦂ") + str(e) + bstack1l1llll_opy_ (u"ࠢࠣᦃ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11l1llllll1_opy_, stage=STAGE.SINGLE)
    def bstack11ll111111l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1llll_opy_ (u"ࠣ࠲ࠥᦄ")):
        self.ensure_bin_session()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᦅ").format(threading.get_ident(), os.getpid())
        try:
            r = self.cli_service.AISelfHealGetResult(req)
            self.logger.info(bstack1l1llll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᦆ") + str(r) + bstack1l1llll_opy_ (u"ࠦࠧᦇ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᦈ") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢᦉ"))
            traceback.print_exc()
            raise e