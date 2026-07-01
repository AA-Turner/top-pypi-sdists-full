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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    AutomationFrameworkBrowser,
)
from bstack_utils.helper import  bstack11llll11_opy_
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestFrameworkTest, TestHookState, LogEntry
from typing import Tuple, Any
import threading
from bstack_utils.bstack1lllllllll_opy_ import bstack1lll11l1l1l_opy_
from browserstack_sdk.sdk_cli.module_webdriver_test import WebDriverTestModule
from bstack_utils.percy import bstack11ll1l1111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l11l1l1lll_opy_(BaseModule):
    def __init__(self, bstack11l1l1ll1l1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11l1l1ll1l1_opy_ = bstack11l1l1ll1l1_opy_
        self.percy = bstack11ll1l1111_opy_()
        self.bstack111lll1l1l_opy_ = bstack1lll11l1l1l_opy_()
        self.bstack11l1l1l1l11_opy_()
        SeleniumFramework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.PRE), self.bstack11l1l1ll1ll_opy_)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.POST), self.on_after_test)
    def is_enabled(self) -> bool:
        return True
    def resolve_test_instance(self, instance: AutomationFrameworkBrowser, driver: object):
        test_instances = TestFramework.get_context_instances(instance.context)
        for t in test_instances:
            driver_instances = TestFramework.get_state(t, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
            if any(instance is d[1] for d in driver_instances) or instance == driver:
                return t
    def bstack11l1l1ll1ll_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not SeleniumFramework.is_execute_request(method_name):
                return
            platform_index = f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX, 0)
            test_instance = self.resolve_test_instance(instance, driver)
            bstack11l1l1l1ll1_opy_ = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_RERUN_NAME, None)
            if not bstack11l1l1l1ll1_opy_:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᦰ"))
                return
            driver_command = f.parse_command_name(*args)
            for command in bstack1ll1l1l111_opy_:
                if command == driver_command:
                    self.bstack1llll1111ll_opy_(driver, platform_index)
            bstack1l11l111ll_opy_ = self.percy.bstack1l1ll1l1lll_opy_()
            if driver_command in bstack1l1l1llll1_opy_[bstack1l11l111ll_opy_]:
                self.bstack111lll1l1l_opy_.bstack1l11l11111_opy_(bstack11l1l1l1ll1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᦱ"), e)
    def on_after_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.performance_tester import PerformanceTester
        driver_instances = f.get_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
        if not driver_instances:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᦲ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠨࠢᦳ"))
            return
        if len(driver_instances) > 1:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᦴ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠣࠤᦵ"))
        bstack11l1l1ll111_opy_, bstack11l1l1lll1l_opy_ = driver_instances[0]
        driver = bstack11l1l1ll111_opy_()
        if not driver:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᦶ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠥࠦᦷ"))
            return
        bstack11l1l1llll1_opy_ = {
            TestFramework.KEY_TEST_NAME: bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᦸ"),
            TestFramework.KEY_TEST_UUID: bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᦹ"),
            TestFramework.KEY_TEST_RERUN_NAME: bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᦺ")
        }
        bstack11l1l1l11ll_opy_ = { key: f.get_state(instance, key) for key in bstack11l1l1llll1_opy_ }
        bstack11l1l1ll11l_opy_ = [key for key, value in bstack11l1l1l11ll_opy_.items() if not value]
        if bstack11l1l1ll11l_opy_:
            for key in bstack11l1l1ll11l_opy_:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᦻ") + str(key) + bstack1l1llll_opy_ (u"ࠣࠤᦼ"))
            return
        platform_index = f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX, 0)
        if self.bstack11l1l1ll1l1_opy_.percy_capture_mode == bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᦽ"):
            bstack11lll11lll_opy_ = bstack11l1l1l11ll_opy_.get(TestFramework.KEY_TEST_RERUN_NAME) + bstack1l1llll_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᦾ")
            random_label = PerformanceTester.mark_start(EVENTS.bstack11l1l1l1lll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11lll11lll_opy_,
                bstack1lll1llll1l_opy_=bstack11l1l1l11ll_opy_[TestFramework.KEY_TEST_NAME],
                bstack11l1l11ll1_opy_=bstack11l1l1l11ll_opy_[TestFramework.KEY_TEST_UUID],
                bstack1llllll11l_opy_=platform_index
            )
            PerformanceTester.end(EVENTS.bstack11l1l1l1lll_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᦿ"), random_label+bstack1l1llll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᧀ"), True, None, None, None, None, test_name=bstack11lll11lll_opy_)
    def bstack1llll1111ll_opy_(self, driver, platform_index):
        if self.bstack111lll1l1l_opy_.bstack11l111lll1_opy_() is True or self.bstack111lll1l1l_opy_.capturing() is True:
            return
        self.bstack111lll1l1l_opy_.bstack111ll111l1_opy_()
        while not self.bstack111lll1l1l_opy_.bstack11l111lll1_opy_():
            bstack11l1l1l1ll1_opy_ = self.bstack111lll1l1l_opy_.bstack11ll1l1l11_opy_()
            self.bstack11ll111111_opy_(driver, bstack11l1l1l1ll1_opy_, platform_index)
        self.bstack111lll1l1l_opy_.bstack1llll1l11ll_opy_()
    def bstack11ll111111_opy_(self, driver, bstack1l1l1l11ll1_opy_, platform_index, test=None):
        from bstack_utils.performance_tester import PerformanceTester
        random_label = PerformanceTester.mark_start(EVENTS.bstack111l1111ll_opy_.value)
        if test != None:
            bstack1lll1llll1l_opy_ = getattr(test, bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᧁ"), None)
            bstack11l1l11ll1_opy_ = getattr(test, bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᧂ"), None)
            PercySDK.screenshot(driver, bstack1l1l1l11ll1_opy_, bstack1lll1llll1l_opy_=bstack1lll1llll1l_opy_, bstack11l1l11ll1_opy_=bstack11l1l11ll1_opy_, bstack1llllll11l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1l1l11ll1_opy_)
        PerformanceTester.end(EVENTS.bstack111l1111ll_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᧃ"), random_label+bstack1l1llll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᧄ"), True, None, None, None, None, test_name=bstack1l1l1l11ll1_opy_)
    def bstack11l1l1l1l11_opy_(self):
        os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᧅ")] = str(self.bstack11l1l1ll1l1_opy_.success)
        os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᧆ")] = str(self.bstack11l1l1ll1l1_opy_.percy_capture_mode)
        self.percy.bstack11l1l1l1l1l_opy_(self.bstack11l1l1ll1l1_opy_.is_percy_auto_enabled)
        self.percy.bstack11l1l1lll11_opy_(self.bstack11l1l1ll1l1_opy_.percy_build_id)