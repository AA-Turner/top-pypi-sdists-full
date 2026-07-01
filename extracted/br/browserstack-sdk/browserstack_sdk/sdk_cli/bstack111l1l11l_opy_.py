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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    bstack1l111l1l_opy_,
    AutomationFrameworkBrowser,
)
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, TestFrameworkTest
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.module_webdriver_test import WebDriverTestModule
from browserstack_sdk.sdk_cli.bstack11lll1lllll_opy_ import bstack1l11111llll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
from bstack_utils.helper import bstack11ll1l11l11_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.accessibility import (
    is_browser_supported_for_accessibility,
    get_browser_display_name,
    get_min_version_for_browser,
    requires_chrome_options_validation,
    is_version_supported
)
from bstack_utils.performance_tester import PerformanceTester
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack111ll111l_opy_(BaseModule):
    bstack11ll111l1ll_opy_ = False
    bstack11ll11ll11l_opy_ = bstack1l1llll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦᡪ")
    bstack11ll111l11l_opy_ = bstack1l1llll_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᡫ")
    bstack11ll11l11l1_opy_ = bstack1l1llll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨᡬ")
    bstack11ll11l1lll_opy_ = bstack1l1llll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᡭ")
    bstack11ll1ll1l1l_opy_ = bstack1l1llll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦᡮ")
    bstack11ll1lll1l1_opy_ = bstack1l1llll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡪࡴࡡࡣ࡮ࡨࡨࠧᡯ")  # bstack11ll1ll11ll_opy_-driver A11y enabled flag (thread-safe)
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _111lll111_opy_ = threading.Event()
    _111lll111_opy_.set()
    def __init__(self, module_automation_framework, module_automation_framework_test):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.bstack11ll1llll11_opy_ = False
        self.bstack11ll1ll1l11_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack11ll11l1ll1_opy_ = False
        self.bstack11ll1l1l1l1_opy_ = dict()
        if not self.is_enabled():
            return
        self.automation_framework_test = module_automation_framework_test
        module_automation_framework.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.PRE), self.bstack111lllll1_opy_)
        module_automation_framework.set_hook_callback((AutomationFrameworkState.CREATE, HookState.PRE), self.bstack11ll11llll1_opy_)
        module_automation_framework.set_hook_callback((AutomationFrameworkState.CREATE, HookState.POST), self.bstack11ll11l1l1l_opy_)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.PRE), self.on_before_test)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.POST), self.on_after_test)
    def is_enabled(self) -> bool:
        return True
    def on_before_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not hasattr(instance, bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹࠧᡰ")) or not instance.test_frameworks:
            return
        tags = self._11lll111111_opy_(instance, args)
        test_framework = f.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_NAME)
        if self.bstack11ll1llll11_opy_:
            self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᡱ")] = f.get_state(instance, TestFramework.KEY_TEST_UUID)
        enabled = False
        if bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᡲ") in instance.test_frameworks:
            platform_index = f.get_state(instance, TestFramework.KEY_PLATFORM_INDEX)
            enabled = self.bstack11ll1l111ll_opy_(tags, self.config[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᡳ")][platform_index])
        elif test_framework == bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᡴ"):
            platform_index = f.get_state(instance, TestFramework.KEY_PLATFORM_INDEX)
            enabled = self.bstack11ll1l111ll_opy_(tags, self.config[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᡵ")][platform_index])
        elif is_robot_playwright_installed():
            enabled = self.is_enabled_testcase(tags)
            threading.current_thread().a11y_current_test_name = f.get_state(instance, TestFramework.KEY_TEST_NAME)
            threading.current_thread().a11y_current_test_uuid = f.get_state(instance, TestFramework.KEY_TEST_UUID)
            threading.current_thread().a11y_save_result_done = False
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡲࡰࡤࡲࡸ࠲ࡶࡷࠡࡶࡤ࡫ࡸ࠳࡯࡯࡮ࡼࠤࡨ࡮ࡥࡤ࡭࠯ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡁࢀࢃࠢᡶ").format(enabled))
        elif bstack1l1llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᡷ") in (instance.test_frameworks or []) or f.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_NAME) == bstack1l1llll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᡸ"):
            enabled = self.is_enabled_testcase(tags)
            threading.current_thread().a11y_current_test_name = f.get_state(instance, TestFramework.KEY_TEST_NAME)
            threading.current_thread().a11y_current_test_uuid = f.get_state(instance, TestFramework.KEY_TEST_UUID)
            threading.current_thread().a11y_save_result_done = False
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡥࡩ࡭ࡧࡶࡦࠢࡷࡥ࡬ࡹ࠭ࡰࡰ࡯ࡽࠥࡩࡨࡦࡥ࡮࠰ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡂࢁࡽࠣ᡹").format(enabled))
        elif isinstance(self.automation_framework_test, bstack1l11111llll_opy_):
            enabled = self.is_enabled_testcase(tags)
            threading.current_thread().a11y_current_test_name = f.get_state(instance, TestFramework.KEY_TEST_NAME)
            threading.current_thread().a11y_current_test_uuid = f.get_state(instance, TestFramework.KEY_TEST_UUID)
            threading.current_thread().a11y_save_result_done = False
            self.logger.info(bstack1l1llll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡴࡾࡺࡥࡴࡶ࠮ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡵࡣࡪࡷ࠲ࡵ࡮࡭ࡻࠣࡧ࡭࡫ࡣ࡬࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࡿࢂࠨ᡺").format(enabled))
        else:
            capabilities = self.automation_framework_test.bstack11ll111ll11_opy_(f, instance, hook_info, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧ᡻").format(hook_info, args, kwargs))
                return
            enabled = self.bstack11ll1l111ll_opy_(tags, capabilities)
        threading.current_thread().a11yEnabled = enabled
        f.set_state(instance, bstack111ll111l_opy_.bstack11ll1lll1l1_opy_, enabled)
        if self.automation_framework_test.pages and self.automation_framework_test.pages.values():
            bstack11ll1l1l11l_opy_ = list(self.automation_framework_test.pages.values())
            if bstack11ll1l1l11l_opy_ and isinstance(bstack11ll1l1l11l_opy_[0], (list, tuple)) and bstack11ll1l1l11l_opy_[0]:
                bstack11ll1l1ll1l_opy_ = bstack11ll1l1l11l_opy_[0][0]
                if callable(bstack11ll1l1ll1l_opy_):
                    page = bstack11ll1l1ll1l_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ᡼"))
                    def bstack11ll1lll11l_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1llll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ᡽"))
                    setattr(page, bstack1l1llll_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡳࠣ᡾"), get_results)
                    setattr(page, bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣ᡿"), bstack11ll1lll11l_opy_)
    def bstack11ll11llll1_opy_(
        self,
        f,
        target,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result,
        *args,
        **kwargs,
    ):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡤࡸࠥࡉࡒࡆࡃࡗࡉ࠳ࡖࡒࡆ࠰ࠣࡊࡴࡸࠠࡃࡧ࡫ࡥࡻ࡫ࠫࡑ࡙ࠣࡆ࡮ࡴࡡࡳࡻࠣࡊࡱࡵࡷ࠭ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡣࡵࡩࡳ࠭ࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡾ࡫ࡴࠋࠢࠣࠤࠥࠦࠠࠡࠢࠫࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡷࡱࡷࠥ࡯࡮ࡴ࡫ࡧࡩࠥࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡯ࡥࡺࡴࡣࡩ࠰ࡺࡶࡦࡶࡰࡦࡦࠫ࠭࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡏࡓࠡࡶ࡫ࡩࠥࡉࡒࡆࡃࡗࡉࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡲࡱࡿࠠࡳࡷࡱࠤࡹ࡮ࡥࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡧ࡭࡫ࡣ࡬ࠢࡺ࡬ࡪࡴࠠࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠥ࡯ࡳࠡࡣࡦࡸࡺࡧ࡬࡭ࡻࠣࡴࡴࡶࡵ࡭ࡣࡷࡩࡩ࠴ࠢࠣࠤᢀ")
        instance, method_name = exec
        enabled = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᢁ"), False)
        if not enabled:
            return
        capabilities = self.automation_framework_test.bstack11ll111ll11_opy_(None, None, None)
        if not capabilities or not capabilities.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᢂ")):
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡤࡳ࡫ࡹࡩࡷࡥࡣࡳࡧࡤࡸࡪࡀࠠ࡯ࡱࠣࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠡ࡫ࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠯ࠤࡩ࡫ࡦࡦࡴࡵ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡦ࡬ࡪࡩ࡫ࠣᢃ"))
            return
        bstack1l1l1l11l_opy_ = self.is_platform_supported(capabilities)
        enabled = enabled and bstack1l1l1l11l_opy_
        threading.current_thread().a11yEnabled = enabled
        f.set_state(instance, bstack111ll111l_opy_.bstack11ll1lll1l1_opy_, enabled)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡴࡨࡥࡹ࡫࠺ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡷࡺࡶࡰࡰࡴࡷࡩࡩࡃࡻࡾࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠿ࡾࢁࠧᢄ").format(bstack1l1l1l11l_opy_, enabled))
    def bstack11ll11l1l1l_opy_(
        self,
        f,
        target,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result,
        *args,
        **kwargs,
    ):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡢࡶࠣࡇࡗࡋࡁࡕࡇ࠱ࡔࡔ࡙ࡔࠡ⠖ࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡤࡲࡩࠦࡨࡶࡤࡢࡹࡷࡲࠠࡢࡴࡨࠤࡳࡵࡷࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡆࡪ࡮ࡡࡷࡧ࠮ࡔ࡜ࠦࡂࡪࡰࡤࡶࡾࠦࡆ࡭ࡱࡺ࠾ࠥࡩࡡ࡭࡮ࡶࠤ࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠢࡲࡲࠥࡩ࡯࡯ࡰࡨࡧࡹ࠵࡬ࡢࡷࡱࡧ࡭࠲ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡵࡲࠤࡹ࡮ࡡࡵࠢࡄ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࠪࡶࡧࡦࡴࠬࠡࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠲ࠠࡦࡶࡦ࠲࠮ࠦࡡࡳࡧࠣࡰࡴࡧࡤࡦࡦࠣࡺ࡮ࡧࠠࡨࡔࡓࡇࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡉ࡯࡯ࡨ࡬࡫ࠥࡨࡥࡧࡱࡵࡩࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡳࡷࡱࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠯ࡕ࡝࠺ࠡࡶ࡫ࡩࠥ࡬ࡩࡹࡶࡸࡶࡪ࠳ࡤࡳ࡫ࡹࡩࡳࠦࡠࡤࡱࡱࡲࡪࡩࡴࡡ࠱ࡣࡰࡦࡻ࡮ࡤࡪࡣࠤ࡫࡯ࡲࡦࡵࠣࡨࡺࡸࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳࠤ࠭ࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊ࠱ࡔࡗࡋࠩ࠭ࠢࡺ࡬࡮ࡩࡨࠡ࡫ࡶࠤࡇࡋࡆࡐࡔࡈࠤࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࠨࡕࡇࡖࡘ࠳ࡖࡒࡆࠫࠣࡻ࡭࡫ࡲࡦࠢࡣࡥ࠶࠷ࡹࡆࡰࡤࡦࡱ࡫ࡤࡡࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡ࡫ࡶࠤࡸ࡫ࡴ࠯࡚ࠢࡩࠥࡩࡡ࡯ࠩࡷࠤ࡬ࡧࡴࡦࠢࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡠࡢ࠳࠴ࡽࡊࡴࡡࡣ࡮ࡨࡨࡥࠦࡨࡦࡴࡨࠤ⠙ࠦࡩ࡯ࡵࡷࡩࡦࡪࠬࠡࡩࡤࡸࡪࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡤࡳ࡫ࡹࡩࡷ࠳࡬ࡦࡸࡨࡰࠥࡩࡡࡱࡵࠣࡸ࡭ࡧࡴࠡࡵࡤࡽࠏࠦࠠࠡࠢࠣࠤࠥࠦࡠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡃࡔࡳࡷࡨࡤ࠱ࠦࡷࡩ࡫ࡦ࡬ࠥࡧࡲࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡹࡵࡲࡦࡦࠣࡦࡾࠐࠠࠡࠢࠣࠤࠥࠦࠠࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡣࡱࡧࡵ࡯ࡥ࡫࠳ࡴࡴ࡟ࡤࡱࡱࡲࡪࡩࡴࠡࡣࡷࠤࡈࡘࡅࡂࡖࡈ࠲ࡕࡕࡓࡕ࠰ࠣࡓࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠦࡩ࡯࡫ࡷࠤࡳ࡫ࡶࡦࡴࠣࡶࡺࡴࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࡤࡲࡩࠦࡳࡦ࡮ࡩ࠲ࡸࡩࡲࡪࡲࡷࡷࡠ࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪࡡࠥࡹࡴࡢࡻࡶࠤࡪࡳࡰࡵࡻ࠯ࠤࡸࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳ࠵ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡡࡳ࡮ࡼ࠱ࡷ࡫ࡴࡶࡴࡱࠤ࡫ࡵࡲࠡࡧࡹࡩࡷࡿࠠࡱࡣࡪࡩࠥࡧࡣࡵ࡫ࡲࡲ࠳ࠨࠢࠣᢅ")
        instance, method_name = exec
        if method_name not in (bstack1l1llll_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᢆ"), bstack1l1llll_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧᢇ")):
            return
        enabled = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᢈ"), False)
        if not enabled:
            try:
                capabilities = f.bstack11lll111l11_opy_(instance, {}) or {}
            except Exception as _e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡩࡸࡩࡷࡧࡵࡣࡨࡸࡥࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡲࡢ࡫ࡶࡩࡩࡀࠠࠦࡵࠥᢉ"), _e)
                capabilities = {}
            bstack11ll1llllll_opy_ = bool(capabilities.get(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᢊ"), False))
            if not bstack11ll1llllll_opy_:
                self.logger.warning(
                    bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡤࡳ࡫ࡹࡩࡷࡥࡣࡳࡧࡤࡸࡪࡀࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࠨࡷࠥ⠚ࠠ࡯ࡧ࡬ࡸ࡭࡫ࡲࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡢ࠳࠴ࡽࡊࡴࡡࡣ࡮ࡨࡨࠥࡴ࡯ࡳࠢࡦࡥࡵࡹࠠࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠽ࡕࡴࡸࡩࠬࠦࡩࡴࠢࡶࡩࡹࡁࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࡳ࡯࡮ࡨࠢࡤࡲࡩࠦࡲࡦࡵࡸࡰࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡵ࡮࡭ࡵࡶࡥࡥࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᢋ"),
                    method_name,
                )
                return
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡴࡨࡥࡹ࡫࠺ࠡࡥࡤࡴࡸ࠳ࡢࡢࡵࡨࡨࠥࡧ࠱࠲ࡻࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡽࢀࠤࡧࡻࡴࠡࡆࡈࡊࡊࡘࡒࡊࡐࡊࠤࡦ࠷࠱ࡺࡇࡱࡥࡧࡲࡥࡥ࠿ࡗࡶࡺ࡫ࠠࡶࡰࡷ࡭ࡱࠦ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺࠠࡢࡲࡳࡰ࡮࡫ࡳࠡࡶ࡫ࡩࠥࡺࡡࡨࡵࠣࡪ࡮ࡲࡴࡦࡴࠣࠬ࡮ࡴࡣ࡭ࡷࡧࡩ࠴࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠬ࠿ࠥ࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠣࡻ࡮ࡲ࡬ࠡࡵࡷ࡭ࡱࡲࠠࡳࡷࡱࠤࡸࡵࠠࡴࡥࡵ࡭ࡵࡺࡳࠡ࡮ࡲࡥࡩࠦࡢࡦࡨࡲࡶࡪࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡤࡲࡨࡾࠨᢌ").format(method_name))
        self.bstack11ll1l1l111_opy_(f, exec, *args, **kwargs)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡵࡩࡦࡺࡥ࠻ࠢ࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠠࡤࡣ࡯ࡰࡪࡪࠠࡧࡱࡵࠤࢀࢃࠬࠡࡍࡈ࡝ࡤࡏࡎࡊࡖࡀࡿࢂࠨᢍ").format(
            method_name, f.get_state(instance, bstack111ll111l_opy_.bstack11ll11l11l1_opy_, False)))
    def bstack111lllll1_opy_(
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
            if f.bstack11ll111ll1l_opy_(method_name, *args):
                time_start = datetime.now()
                self.bstack11ll1l1l111_opy_(f, exec, *args, **kwargs)
                instance.add_benchmark(bstack1l1llll_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᢎ"), datetime.now() - time_start)
                return
            enabled = f.get_state(instance, bstack111ll111l_opy_.bstack11ll1lll1l1_opy_, False) \
                      or getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ᢏ"), False)
            if not enabled:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬ࠨᢐ"))
                return
            time_start = datetime.now()
            self.bstack11ll1l1l111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.add_benchmark(bstack1l1llll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᢑ"), datetime.now() - time_start)
            bstack1l11lll1l1l_opy_ = instance.data.get(bstack1l1llll_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᢒ"), None)
            if (
                not f.is_execute_request(method_name)
                or f.bstack11ll11ll111_opy_(method_name, *args)
                or f.bstack11ll11l1111_opy_(method_name, *args)
                or (bstack1l11lll1l1l_opy_ and int(bstack1l11lll1l1l_opy_)>1)
            ):
                return
            if not f.get_state(instance, bstack111ll111l_opy_.bstack11ll11l11l1_opy_, False):
                if not bstack111ll111l_opy_.bstack11ll111l1ll_opy_:
                    self.logger.warning(bstack1l1llll_opy_ (u"ࠧࡡࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡿࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᢓ").format(f.platform_index))
                    bstack111ll111l_opy_.bstack11ll111l1ll_opy_ = True
                return
            bstack11ll111lll1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack11ll111lll1_opy_:
                platform_index = f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX, 0)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿࢂࠨᢔ").format(platform_index, f.framework_name))
                return
            command_name = f.parse_command_name(*args)
            if not command_name:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻࡾࠤᢕ").format(f.framework_name, method_name))
                return
            if f.framework_name != bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᢖ"):
                bstack11ll11l1l11_opy_ = f.get_state(instance, bstack111ll111l_opy_.bstack11ll1ll1l1l_opy_, False)
                if command_name == bstack1l1llll_opy_ (u"ࠤࡪࡩࡹࠨᢗ") and not bstack11ll11l1l11_opy_:
                    f.set_state(instance, bstack111ll111l_opy_.bstack11ll1ll1l1l_opy_, True)
                    bstack11ll11l1l11_opy_ = True
                if not bstack11ll11l1l11_opy_ and not self.bstack11ll1llll11_opy_:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡲࡴࠦࡕࡓࡎࠣࡰࡴࡧࡤࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࡻࡾࠤᢘ").format(f.framework_name, command_name))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࡻࡾࠤᢙ").format(f.framework_name, command_name))
                return
            self.logger.info(bstack1l1llll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࡻࡾࠤᢚ").format(len(scripts_to_run), f.framework_name, command_name))
            scripts = [(s, bstack11ll111lll1_opy_[s]) for s in scripts_to_run if s in bstack11ll111lll1_opy_]
            for script_name, script_code in scripts:
                try:
                    time_start = datetime.now()
                    if script_name == bstack1l1llll_opy_ (u"ࠨࡳࡤࡣࡱࠦᢛ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack1l1llll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᢜ"): {
                                    bstack1l1llll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᢝ"): bstack1l1llll_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧᢞ"),
                                    bstack1l1llll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢᢟ"): [
                                        {
                                            bstack1l1llll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᢠ"): command_name
                                        }
                                    ]
                                },
                                bstack1l1llll_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᢡ"): {
                                    bstack1l1llll_opy_ (u"ࠨࡢࡰࡦࡼࠦᢢ"): {
                                        bstack1l1llll_opy_ (u"ࠢ࡮ࡵࡪࠦᢣ"): result.get(bstack1l1llll_opy_ (u"ࠣ࡯ࡶ࡫ࠧᢤ"), bstack1l1llll_opy_ (u"ࠤࠥᢥ")) if isinstance(result, dict) else bstack1l1llll_opy_ (u"ࠥࠦᢦ"),
                                        bstack1l1llll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᢧ"): result.get(bstack1l1llll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᢨ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack1l1llll_opy_ (u"ࠨᢩࠬࠣ"), bstack1l1llll_opy_ (u"ࠢ࠻ࠤᢪ"))))
                        except Exception as bstack1ll1111ll1l_opy_:
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ᢫").format(bstack1ll1111ll1l_opy_))
                    instance.add_benchmark(bstack1l1llll_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࠣ᢬") + script_name, datetime.now() - time_start)
                    if isinstance(result, dict) and not result.get(bstack1l1llll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ᢭"), True):
                        self.logger.warning(bstack1l1llll_opy_ (u"ࠦࡸࡱࡩࡱࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡸࡥ࡮ࡣ࡬ࡲ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴࡴ࠼ࠣࡿࢂࠨ᢮").format(result))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡿࠣࡩࡷࡸ࡯ࡳ࠿ࡾࢁࠧ᢯").format(script_name, e))
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧࠣࡩࡷࡸ࡯ࡳ࠿ࡾࢁࠧᢰ").format(e))
    def on_after_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_behave = (bstack1l1llll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᢱ") in (instance.test_frameworks or []) or
                     f.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_NAME) == bstack1l1llll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨᢲ"))
        enabled = f.get_state(instance, bstack111ll111l_opy_.bstack11ll1lll1l1_opy_, False)
        if is_behave:
            enabled = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡤ࠵࠶ࡿࡅ࡯ࡣࡥࡰࡪࡪࠧᢳ"), enabled)
        if bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᢴ") not in instance.test_frameworks and not is_behave:
            tags = self._11lll111111_opy_(instance, args)
            capabilities = self.automation_framework_test.bstack11ll111ll11_opy_(f, instance, hook_info, *args, **kwargs)
            enabled = self.bstack11ll1l111ll_opy_(tags, capabilities)
            threading.current_thread().a11yEnabled = enabled
            f.set_state(instance, bstack111ll111l_opy_.bstack11ll1lll1l1_opy_, enabled)
        elif is_behave and enabled:
            capabilities = self.automation_framework_test.bstack11ll111ll11_opy_(None, None, None)
            if capabilities:
                bstack11ll1l1ll11_opy_ = self.is_platform_supported(capabilities)
                if not bstack11ll1l1ll11_opy_:
                    enabled = False
                    threading.current_thread().a11yEnabled = enabled
                    f.set_state(instance, bstack111ll111l_opy_.bstack11ll1lll1l1_opy_, enabled)
        if not enabled:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᢵ"))
            return
        driver = self.automation_framework_test.bstack11ll11lll1l_opy_(f, instance, hook_info, *args, **kwargs)
        if driver is None and isinstance(self.automation_framework_test, bstack1l11111llll_opy_):
            driver = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡕࡧࡧࡦࠩᢶ"), None)
            if driver is not None:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡶࡵ࡬ࡲ࡬ࠦࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡖࡡࡨࡧࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥ࡬࡯ࡳࠢࡅࡩ࡭ࡧࡶࡦ࠭ࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᢷ"))
        test_name = f.get_state(instance, TestFramework.KEY_TEST_NAME)
        if not test_name:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᢸ"))
            return
        test_uuid = f.get_state(instance, TestFramework.KEY_TEST_UUID)
        if not test_uuid:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᢹ"))
            return
        if isinstance(self.automation_framework_test, bstack1l11111llll_opy_):
            framework_name = bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᢺ")
        else:
            framework_name = bstack1l1llll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᢻ")
        save_result_done = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡥࡻ࡫࡟ࡳࡧࡶࡹࡱࡺ࡟ࡥࡱࡱࡩࠬᢼ"), False)
        if not save_result_done:
            self.bstack11ll11lll_opy_(driver, test_name, framework_name, test_uuid)
            threading.current_thread().a11y_save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        random_label = PerformanceTester.mark_start(EVENTS.bstack11l111llll_opy_.value)
        enabled = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡈࡲࡦࡨ࡬ࡦࡦࠪᢽ"), False)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡅࡏࡖࡕ࡝ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡾ࠮ࠣࡱࡪࡺࡨࡰࡦࡀࡿࢂ࠲ࠠࡦࡰࡤࡦࡱ࡫ࡤ࠾ࡽࢀࠦᢾ").format(framework_name, method, enabled))
        if not enabled:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࠳࠴ࡽࠥࡊࡉࡔࡃࡅࡐࡊࡊࠠࠩࡣ࠴࠵ࡾࡋ࡮ࡢࡤ࡯ࡩࡩࡃࡆࡢ࡮ࡶࡩ࠮ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡿࠥᢿ").format(framework_name))
            return
        if driver is None and not is_robot_playwright_installed():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡫ࡶࠤࡓࡵ࡮ࡦࠢࠫࡰ࡮ࡱࡥ࡭ࡻࠣࡨࡪ࡬ࡥࡳࡴࡨࡨࠥࡩ࡬ࡰࡵࡨ࠭ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࡾࢁࠧᣀ").format(framework_name, method))
            return
        time_start = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack1l1llll_opy_ (u"ࠤࡶࡧࡦࡴࠢᣁ"), None)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡷࡨࡸࡩࡱࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࡃࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠢᣂ").format(script_code is not None, framework_name))
        if not script_code:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡤࡣࡱࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿࢂࠨᣃ").format(framework_name))
            return
        if self.bstack11ll1llll11_opy_:
            arg = dict()
            arg[bstack1l1llll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᣄ")] = method if method else bstack1l1llll_opy_ (u"ࠨࠢᣅ")
            arg[bstack1l1llll_opy_ (u"ࠢࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠢᣆ")] = self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣᣇ")]
            arg[bstack1l1llll_opy_ (u"ࠤࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠢᣈ")] = self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᣉ")]
            arg[bstack1l1llll_opy_ (u"ࠦࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣᣊ")] = self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠥᣋ")]
            arg[bstack1l1llll_opy_ (u"ࠨࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠥᣌ")] = self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨᣍ")]
            arg[bstack1l1llll_opy_ (u"ࠣࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠣᣎ")] = str(int(datetime.now().timestamp() * 1000))
            bstack11ll1l111l1_opy_ = self.bstack11ll1llll1l_opy_(bstack1l1llll_opy_ (u"ࠤࡶࡧࡦࡴࠢᣏ"), self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᣐ")])
            if bstack1l1llll_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡖࡲ࡯ࡪࡴࠢᣑ") in bstack11ll1l111l1_opy_:
                bstack11ll1l111l1_opy_ = bstack11ll1l111l1_opy_.copy()
                bstack11ll1l111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡋࡩࡦࡪࡥࡳࠤᣒ")] = bstack11ll1l111l1_opy_.pop(bstack1l1llll_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᣓ"))
            arg = bstack11ll1l11l11_opy_(arg, bstack11ll1l111l1_opy_)
            bstack11ll1l1111l_opy_ = script_code % json.dumps(arg)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢࡲࡳࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡁ࡙ࡸࡵࡦ࠮ࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡱࡪࡺࡨࡰࡦࡀࡿࢂࠨᣔ").format(method))
            driver.execute_script(bstack11ll1l1111l_opy_)
            return
        instance = bstack1l111l1l_opy_.get_tracked_instance(driver)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡻ࡮ࡥ࠿ࡾࢁ࠱ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡿࠥᣕ").format(instance is not None, framework_name))
        if instance:
            bstack11ll111llll_opy_ = bstack1l111l1l_opy_.get_state(instance, bstack111ll111l_opy_.bstack11ll11l1lll_opy_, False)
            if not bstack11ll111llll_opy_:
                bstack1l111l1l_opy_.set_state(instance, bstack111ll111l_opy_.bstack11ll11l1lll_opy_, True)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡶࡩࡹࠦࡉࡔࡡࡖࡇࡆࡔࡎࡊࡐࡊࡁ࡙ࡸࡵࡦࠢࡩࡳࡷࠦ࡭ࡦࡶ࡫ࡳࡩࡃࡻࡾࠤᣖ").format(method))
            else:
                self.logger.info(bstack1l1llll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࡻࡾࠤᣗ").format(framework_name, method))
                return
        self.logger.info(bstack1l1llll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡊ࡞ࡅࡄࡗࡗࡍࡓࡍࠠࡔࡅࡄࡒࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࡾࢁࠧᣘ").format(framework_name, method))
        bstack11ll11l11ll_opy_ = {bstack1l1llll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᣙ"): method if method else bstack1l1llll_opy_ (u"ࠨࠢᣚ")}
        _1l1llll11_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᣛ"), None)
        if _1l1llll11_opy_:
            bstack11ll11l11ll_opy_[bstack1l1llll_opy_ (u"ࠣࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠣᣜ")] = _1l1llll11_opy_
        else:
            try:
                if instance:
                    _1l1llll11_opy_ = bstack1l111l1l_opy_.get_state(instance, TestFramework.KEY_TEST_UUID, None)
                    if _1l1llll11_opy_:
                        bstack11ll11l11ll_opy_[bstack1l1llll_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᣝ")] = _1l1llll11_opy_
            except Exception:
                pass
        try:
            if framework_name == bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᣞ"):
                self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡨࡧ࡬࡭࡫ࡱ࡫ࠥࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨࠤ࡫ࡵࡲࠡࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠱ࠦ࡭ࡦࡶ࡫ࡳࡩࡃࡻࡾࠢࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥ࠿ࡾࢁࠧᣟ").format(method, bstack11ll11l11ll_opy_.get(bstack1l1llll_opy_ (u"ࠧࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠧᣠ"))))
                result = self.automation_framework_test.bstack11ll111l1l1_opy_(
                    driver, script_code, bstack11ll11l11ll_opy_
                )
            else:
                result = driver.execute_async_script(script_code, bstack11ll11l11ll_opy_)
            PerformanceTester.end(EVENTS.bstack11l111llll_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᣡ"), random_label+bstack1l1llll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᣢ"), True, None, command=method)
            if instance:
                instance.add_benchmark(bstack1l1llll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠧᣣ"), datetime.now() - time_start)
            return result
        finally:
            if instance:
                bstack1l111l1l_opy_.set_state(instance, bstack111ll111l_opy_.bstack11ll11l1lll_opy_, False)
    def bstack11ll1ll1lll_opy_(self, driver: object, framework_name, result_type: str):
        self.ensure_bin_session()
        req = structs.AccessibilityResultRequest()
        req.bin_session_id = self.bin_session_id
        req.bstack11ll11ll1l1_opy_ = self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᣤ")]
        req.result_type = result_type
        req.session_id = self.bin_session_id
        req.platform_index = str(os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᣥ"), bstack1l1llll_opy_ (u"ࠫ࠵࠭ᣦ")))
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᣧ").format(threading.get_ident(), os.getpid())
        try:
            r = self.cli_service.AccessibilityResult(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡼࡿࠥᣨ").format(r))
            else:
                bstack11ll1lllll1_opy_ = json.loads(r.bstack11ll111l111_opy_.decode(bstack1l1llll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᣩ")))
                if result_type == bstack1l1llll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᣪ"):
                    return bstack11ll1lllll1_opy_.get(bstack1l1llll_opy_ (u"ࠤࡧࡥࡹࡧࠢᣫ"), [])
                else:
                    return bstack11ll1lllll1_opy_.get(bstack1l1llll_opy_ (u"ࠥࡨࡦࡺࡡࠣᣬ"), {})
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡰࡱࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡤ࡮࡬࠾ࠥࢁࡽࠣᣭ").format(e))
    @measure(event_name=EVENTS.bstack1l11l111l1_opy_, stage=STAGE.SINGLE)
    def get_accessibility_results(self, driver, framework_name):
        bstack111ll111l_opy_._111lll111_opy_.clear()
        try:
            enabled = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡈࡲࡦࡨ࡬ࡦࡦࠪᣮ"), False)
            if not enabled:
                return
            if self.bstack11ll1llll11_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11ll1ll1lll_opy_(driver, framework_name, bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᣯ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1l1llll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᣰ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᣱ"), framework_name=framework_name)
            time_start = datetime.now()
            if framework_name == bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᣲ"):
                result = self.automation_framework_test.bstack11ll111l1l1_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1l111l1l_opy_.get_tracked_instance(driver)
            if instance:
                instance.add_benchmark(bstack1l1llll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᣳ"), datetime.now() - time_start)
            return result
        finally:
            bstack111ll111l_opy_._111lll111_opy_.set()
    @measure(event_name=EVENTS.bstack11l111111l_opy_, stage=STAGE.SINGLE)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack111ll111l_opy_._111lll111_opy_.clear()
        try:
            enabled = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡇࡱࡥࡧࡲࡥࡥࠩᣴ"), False)
            if not enabled:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᣵ"))
                return
            if self.bstack11ll1llll11_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11ll1ll1lll_opy_(driver, framework_name, bstack1l1llll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪ᣶"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1l1llll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦ᣷"), None)
            if not script_code:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡾࠤ᣸").format(framework_name))
                return
            self.perform_scan(driver, method=bstack1l1llll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣ᣹"), framework_name=framework_name)
            time_start = datetime.now()
            if framework_name == bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ᣺"):
                result = self.automation_framework_test.bstack11ll111l1l1_opy_(driver, script_code)
                bstack111ll111l_opy_._111lll111_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1l111l1l_opy_.get_tracked_instance(driver)
            if instance:
                instance.add_benchmark(bstack1l1llll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣ᣻"), datetime.now() - time_start)
            return result
        finally:
            bstack111ll111l_opy_._111lll111_opy_.set()
    @measure(event_name=EVENTS.bstack11ll11lll11_opy_, stage=STAGE.SINGLE)
    def bstack11ll1l1llll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.ensure_bin_session()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ᣼").format(threading.get_ident(), os.getpid())
        try:
            r = self.cli_service.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡼࡿࠥ᣽").format(r))
            else:
                self.bstack11ll11l111l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ᣾").format(e))
            traceback.print_exc()
            raise e
    def bstack11ll11l111l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ᣿"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack11ll1llll11_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᤀ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack11ll1ll1l11_opy_[bstack1l1llll_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᤁ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack11ll1ll1l11_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack11ll1l1lll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack11ll1l1lll1_opy_:
                        bstack11ll1l1lll1_opy_[command.method] = dict()
                    if command.name and not command.name in bstack11ll1l1lll1_opy_[command.method]:
                        bstack11ll1l1lll1_opy_[command.method][command.name] = list()
                    bstack11ll1l1lll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack11ll1l1lll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack11ll1l1l111_opy_(
        self,
        f: SeleniumFramework,
        exec: Tuple[AutomationFrameworkBrowser, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.automation_framework_test, bstack1l11111llll_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack1l1llll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᤂ"):
                    return
        if f.get_state(instance, bstack111ll111l_opy_.bstack11ll11l11l1_opy_, False) == True:
            return
        bstack11ll1l11ll1_opy_ = False
        desired_capabilities = f.bstack11lll111l11_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack11ll1l11l1l_opy_(instance)
            platform_index = f.get_state(instance, SeleniumFramework.KEY_PLATFORM_INDEX, 0)
            bstack11lll1111ll_opy_ = datetime.now()
            r = self.bstack11ll1l1llll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.add_benchmark(bstack1l1llll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᤃ"), datetime.now() - bstack11lll1111ll_opy_)
            bstack11ll1l11ll1_opy_ = r.success
            f.set_state(instance, bstack111ll111l_opy_.bstack11ll11l11l1_opy_, bstack11ll1l11ll1_opy_)
        else:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡺ࡭ࡱࡲࠠࡳࡧࡷࡶࡾࠦ࡯࡯ࠢࡱࡩࡽࡺࠠ࡬ࡧࡼࡻࡴࡸࡤࠣᤄ"))
    def is_enabled_testcase(self, test_tags):
        bstack11ll1l1llll_opy_ = self.config.get(bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᤅ"))
        if not bstack11ll1l1llll_opy_:
            return True
        try:
            include_tags = bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᤆ")] if bstack1l1llll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᤇ") in bstack11ll1l1llll_opy_ and isinstance(bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᤈ")], list) else []
            exclude_tags = bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᤉ")] if bstack1l1llll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᤊ") in bstack11ll1l1llll_opy_ and isinstance(bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᤋ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᤌ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack11ll1llll11_opy_:
                platform_name = caps.get(bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᤍ"))
                if platform_name is not None and str(platform_name).lower() == bstack1l1llll_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᤎ"):
                    platform_version = caps.get(bstack1l1llll_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᤏ")) or caps.get(bstack1l1llll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᤐ"))
                    if platform_version is not None and int(platform_version) < 11:
                        self.logger.warning(bstack1l1llll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠥࢁࡽ࠯ࠤᤑ").format(platform_version))
                        return False
                return True
            device_name = caps.get(bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᤒ"), {}).get(bstack1l1llll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᤓ"), caps.get(bstack1l1llll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᤔ"), bstack1l1llll_opy_ (u"ࠩࠪᤕ")))
            if device_name:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᤖ"))
                return False
            browser = caps.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᤗ"), bstack1l1llll_opy_ (u"ࠬ࠭ᤘ")).lower()
            if not is_browser_supported_for_accessibility(browser):
                bstack11ll11lllll_opy_ = bstack1l1llll_opy_ (u"࠭ࠬࠡࠩᤙ").join([get_browser_display_name(b) for b in ACCESSIBILITY_SUPPORTED_BROWSERS.keys()])
                self.logger.warning(bstack1l1llll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡼࡿࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᤚ").format(bstack11ll11lllll_opy_))
                return False
            bstack1ll1l1l1l_opy_ = self.config.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᤛ"), True)
            bstack11ll1ll1ll1_opy_ = self.config.get(bstack1l1llll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᤜ"), False)
            min_version = get_min_version_for_browser(browser, bstack1ll1l1l1l_opy_, bstack11ll1ll1ll1_opy_)
            if not min_version:
                self.logger.warning(bstack1l1llll_opy_ (u"ࠥࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡰ࡭ࡳ࡯࡭ࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡽࢀ࠲ࠧᤝ").format(browser))
                return False
            browser_version = caps.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᤞ"))
            if not browser_version:
                browser_version = caps.get(bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᤟"), {}).get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᤠ"), bstack1l1llll_opy_ (u"ࠧࠨᤡ"))
            bstack11ll1lll1ll_opy_ = str(browser_version).lower() if browser_version is not None else bstack1l1llll_opy_ (u"ࠨࠩᤢ")
            if bstack11ll1lll1ll_opy_:
                if bstack11ll1lll1ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᤣ")):
                    if bstack11ll1lll1ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᤤ")):
                        bstack11ll1l11lll_opy_ = bstack11ll1lll1ll_opy_[len(bstack1l1llll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬᤥ")):]
                        if bstack11ll1l11lll_opy_ and not bstack11ll1l11lll_opy_.isdigit():
                            self.logger.warning(bstack1l1llll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡨࡲࡶࡲࡧࡴࠡࠩࡾࢁࠬࡁࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࠪࡰࡦࡺࡥࡴࡶࠪࠤࡴࡸࠠࠨ࡮ࡤࡸࡪࡹࡴ࠮࠾ࡱࡹࡲࡨࡥࡳࡀࠪ࠲ࠧᤦ").format(browser_version))
                            return False
                else:
                    if not is_version_supported(bstack11ll1lll1ll_opy_, min_version):
                        display_name = get_browser_display_name(browser)
                        self.logger.warning(bstack1l1llll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡻࡾࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤࢀࢃࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠦᤧ").format(display_name, min_version))
                        return False
            if requires_chrome_options_validation(browser):
                bstack11ll1ll11l1_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᤨ"), {}).get(bstack1l1llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᤩ"))
                if not bstack11ll1ll11l1_opy_:
                    bstack11ll1ll11l1_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᤪ"), {})
                if not bstack11ll1ll11l1_opy_:
                    bstack11ll1ll11l1_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᤫ"), {})
                if bstack11ll1ll11l1_opy_ and any(arg == bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᤬") or (arg.startswith(bstack1l1llll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪ᤭")) and arg != bstack1l1llll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧ᤮"))
                                         for arg in bstack11ll1ll11l1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ᤯"), [])):
                    self.logger.warning(bstack1l1llll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᤰ"))
                    return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᤱ") + str(error))
            return False
    def bstack11ll1ll111l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack11ll1l11111_opy_ = {
            bstack1l1llll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᤲ"): test_uuid,
        }
        bstack11lll1111l1_opy_ = {}
        if result.success:
            bstack11lll1111l1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack11ll1l11l11_opy_(bstack11ll1l11111_opy_, bstack11lll1111l1_opy_)
    def bstack11ll1llll1l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡨࡸࡨ࡮ࠠࡤࡧࡱࡸࡷࡧ࡬ࠡࡣࡸࡸ࡭ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡳࡤࡴ࡬ࡴࡹࠦ࡮ࡢ࡯ࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡤࡣࡦ࡬ࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡨࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡫࡫ࡴࡤࡪࡨࡨ࠱ࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠢ࡯ࡳࡦࡪࡳࠡࡣࡱࡨࠥࡩࡡࡤࡪࡨࡷࠥ࡯ࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡎࡢ࡯ࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡸࡩࡲࡪࡲࡷࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡴࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡵࡶ࡫ࡧ࠾࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠬࠡࡧࡰࡴࡹࡿࠠࡥ࡫ࡦࡸࠥ࡯ࡦࠡࡧࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᤳ")
        try:
            if self.bstack11ll11l1ll1_opy_:
                return self.bstack11ll1l1l1l1_opy_
            self.ensure_bin_session()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1llll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᤴ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᤵ"), bstack1l1llll_opy_ (u"ࠧ࠱ࠩᤶ")))
            req.client_worker_id = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᤷ").format(threading.get_ident(), os.getpid())
            r = self.cli_service.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack11ll1l1l1l1_opy_ = self.bstack11ll1ll111l_opy_(test_uuid, r)
                self.bstack11ll11l1ll1_opy_ = True
            else:
                self.logger.error(bstack1l1llll_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࢁ࠿ࠦࡻࡾࠤᤸ").format(script_name, r.error))
                self.bstack11ll1l1l1l1_opy_ = dict()
            return self.bstack11ll1l1l1l1_opy_
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥࡪࡪࡺࡣࡩࡅࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡇ࠱࠲ࡻࡆࡳࡳ࡬ࡩࡨ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡪࡲࡪࡸࡨࡶࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡰࡢࡴࡤࡱࡸࠦࡦࡰࡴࠣࡿࢂࡀࠠࡼࡿ᤹ࠥ").format(script_name, traceback.format_exc()))
            return dict()
    def bstack11ll11lll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        random_label = None
        bstack111ll111l_opy_._111lll111_opy_.clear()
        try:
            self.ensure_bin_session()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1llll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦ᤺")
            req.script_name = bstack1l1llll_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵ᤻ࠥ")
            req.platform_index = str(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᤼"), bstack1l1llll_opy_ (u"ࠧ࠱ࠩ᤽")))
            req.client_worker_id = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᤾").format(threading.get_ident(), os.getpid())
            r = self.cli_service.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࢀࢃࠢ᤿").format(r.error))
            else:
                bstack11ll1l11111_opy_ = self.bstack11ll1ll111l_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack1l1llll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭᥀") + str(bstack11ll1l11111_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿࢂࠦࠢ᥁").format(framework_name))
                return
            random_label = PerformanceTester.mark_start(EVENTS.bstack11ll1ll1111_opy_.value)
            self.bstack11ll11ll1ll_opy_(driver, script_code, bstack11ll1l11111_opy_, framework_name)
            try:
                bstack11ll1lll111_opy_ = {
                    bstack1l1llll_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨ᥂"): {
                        bstack1l1llll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢ᥃"): bstack1l1llll_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡁࡗࡇࡢࡖࡊ࡙ࡕࡍࡖࡖࠦ᥄"),
                    },
                    bstack1l1llll_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ᥅"): {
                        bstack1l1llll_opy_ (u"ࠤࡥࡳࡩࡿࠢ᥆"): {
                            bstack1l1llll_opy_ (u"ࠥࡱࡸ࡭ࠢ᥇"): bstack1l1llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢ᥈"),
                            bstack1l1llll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨ᥉"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack11ll1lll111_opy_, separators=(bstack1l1llll_opy_ (u"࠭ࠬࠨ᥊"), bstack1l1llll_opy_ (u"ࠧ࠻ࠩ᥋"))))
            except Exception as bstack1ll1111ll1l_opy_:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡤࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ᥌").format(bstack1ll1111ll1l_opy_))
            self.logger.info(bstack1l1llll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᥍"))
            PerformanceTester.end(EVENTS.bstack11ll1ll1111_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᥎"), random_label+bstack1l1llll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᥏"), True, None, command=bstack1l1llll_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᥐ"),test_name=name)
        except Exception as bstack11ll1l1l1ll_opy_:
            self.logger.error(bstack1l1llll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠦࡵࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠩࡸࠨᥑ") % (name, bstack11ll1l1l1ll_opy_))
            PerformanceTester.end(EVENTS.bstack11ll1ll1111_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᥒ"), random_label+bstack1l1llll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᥓ"), False, bstack11ll1l1l1ll_opy_, command=bstack1l1llll_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᥔ"),test_name=name)
        finally:
            bstack111ll111l_opy_._111lll111_opy_.set()
    def stop_capture_before_browser_close(self, page=None):
        bstack1l1llll_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡹ࡫ࡩࡳࠦࡡࠡࡥ࡯ࡳࡸ࡫ࠠ࡬ࡧࡼࡻࡴࡸࡤࠡ࡫ࡶࠤࡦࡨ࡯ࡶࡶࠣࡸࡴࠦࡥࡹࡧࡦࡹࡹ࡫ࠬࠋࠢࠣࠤࠥࠦࠠࠡࠢࡲࡶࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡱࡣࡷࡧ࡭࡫ࡤࠡࡲࡤ࡫ࡪ࠴ࡣ࡭ࡱࡶࡩ࠭࠯ࠠࡪࡰࡷࡩࡷࡩࡥࡱࡶࡲࡶࠥ࡬࡯ࡳࠢࡅࡩ࡭ࡧࡶࡦ࠭ࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡂࡪࡰࡤࡶࡾࠦࡆ࡭ࡱࡺ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࠣࡴࡦ࡭ࡥࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࠤ࡮ࡹࠠࡵࡪࡨࠤࡱ࡯ࡶࡦࠢࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡢࡩࡨࠤࡴࡨࡪࡦࡥࡷࠤ࠭ࡨࡥࡧࡱࡵࡩࠥ࡯ࡴࠡ࡫ࡶࠤࡨࡲ࡯ࡴࡧࡧ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᥕ")
        _1l111l11_opy_ = threading.current_thread()
        enabled = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡇࡱࡥࡧࡲࡥࡥࠩᥖ"), False)
        save_result_done = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡦࡼࡥࡠࡴࡨࡷࡺࡲࡴࡠࡦࡲࡲࡪ࠭ᥗ"), False)
        if not enabled or save_result_done:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠣᥘ"))
            return
        test_name = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᥙ"), None)
        test_uuid = getattr(_1l111l11_opy_, bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᥚ"), None)
        if not test_name or not test_uuid:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡤࡣࡳࡸࡺࡸࡥࡠࡤࡨࡪࡴࡸࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࡠࡰࡤࡱࡪࠦ࡯ࡳࠢࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠣᥛ"))
            return
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࡡࡥࡩ࡫ࡵࡲࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦ࠼ࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡸࡺ࡯ࡱࡡࡷࡩࡸࡺ࡟ࡤࡣࡳࡸࡺࡸࡥࠣᥜ"))
        self.bstack11ll11lll_opy_(page, test_name, bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᥝ"), test_uuid)
        _1l111l11_opy_.a11y_save_result_done = True
    def bstack11ll11ll1ll_opy_(self, driver, script_code, bstack11ll1l11111_opy_, framework_name):
        if framework_name == bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᥞ"):
            self.automation_framework_test.bstack11ll111l1l1_opy_(driver, script_code, bstack11ll1l11111_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack11ll1l11111_opy_))
    def _11lll111111_opy_(self, instance: TestFrameworkTest, args: Tuple) -> list:
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᥟ")
        if bstack1l1llll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᥠ") in instance.test_frameworks:
            return args[2].tags if hasattr(args[2], bstack1l1llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᥡ")) else []
        if args and hasattr(args[0], bstack1l1llll_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᥢ")) and hasattr(args[0].scenario, bstack1l1llll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᥣ")):
            bstack11lll11111l_opy_ = args[0].scenario.tags
            return list(bstack11lll11111l_opy_) if bstack11lll11111l_opy_ else []
        if hasattr(args[0], bstack1l1llll_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩᥤ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack1l1llll_opy_ (u"ࠬࡺࡡࡨࡵࠪᥥ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack11ll1l111ll_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)