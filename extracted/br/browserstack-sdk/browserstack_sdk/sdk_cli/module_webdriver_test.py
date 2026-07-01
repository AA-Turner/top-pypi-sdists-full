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
import threading
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    bstack1l111l1l_opy_,
    AutomationFrameworkBrowser,
    bstack1l11ll1l1l1_opy_,
)
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, TestFrameworkTest
from browserstack_sdk.sdk_cli.bstack11l1lll1ll1_opy_ import bstack11l1l1lllll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import is_bstack_automation
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class WebDriverTestModule(bstack11l1l1lllll_opy_):
    bstack11l11l1ll11_opy_ = bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡵ࡭ࡻ࡫ࡲࡴࠤᬿ")
    KEY_AUTOMATION_SESSIONS = bstack1l1llll_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᭀ")
    KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS = bstack1l1llll_opy_ (u"ࠧࡴ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡹࠢᭁ")
    bstack11l11l11ll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᭂ")
    bstack11l111ll1ll_opy_ = bstack1l1llll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡲࡦࡨࡶࠦᭃ")
    KEY_CBT_SESSION_CREATED = bstack1l1llll_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡣࡳࡧࡤࡸࡪࡪ᭄ࠢ")
    bstack11l11l111l1_opy_ = bstack1l1llll_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᭅ")
    bstack11l111llll1_opy_ = bstack1l1llll_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠣᭆ")
    def __init__(self):
        super().__init__(bstack11l1ll11111_opy_=self.bstack11l11l1ll11_opy_, frameworks=[SeleniumFramework.NAME])
        if not self.is_enabled():
            return
        TestFramework.set_hook_callback((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack111lll11111_opy_)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.PRE), self.on_before_test)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.POST), self.on_after_test)
    def is_enabled(self) -> bool:
        return True
    def bstack111lll11111_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1lll1111_opy_ = self.bstack11l1lllll11_opy_(instance.context)
        driver_instances = self.bstack111ll1ll1ll_opy_(instance.context, bstack11l1lll1111_opy_=bstack11l1lll1111_opy_)
        if not driver_instances:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢᭇ") + str(hook_info) + bstack1l1llll_opy_ (u"ࠧࠨᭈ"))
        f.set_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, driver_instances)
        bstack111lll1l111_opy_ = self.bstack111ll1ll1ll_opy_(instance.context, bstack111ll1lllll_opy_=False, bstack11l1lll1111_opy_=bstack11l1lll1111_opy_)
        f.set_state(instance, WebDriverTestModule.KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS, bstack111lll1l111_opy_)
    def on_before_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111lll11111_opy_(f, instance, hook_info, *args, **kwargs)
        if not f.get_state(instance, WebDriverTestModule.bstack11l11l111l1_opy_, False):
            self.__111lll11l11_opy_(f,instance,hook_info)
    def on_after_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111lll11111_opy_(f, instance, hook_info, *args, **kwargs)
        if not f.get_state(instance, WebDriverTestModule.bstack11l11l111l1_opy_, False):
            self.__111lll11l11_opy_(f, instance, hook_info)
        if not f.get_state(instance, WebDriverTestModule.bstack11l111llll1_opy_, False):
            self.__111ll1llll1_opy_(f, instance, hook_info)
    def bstack111lll111ll_opy_(
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
        if not f.bstack11l1ll1l11l_opy_(instance):
            return
        if f.get_state(instance, WebDriverTestModule.bstack11l111llll1_opy_, False):
            return
        driver.execute_script(
            bstack1l1llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦᭉ").format(
                json.dumps(
                    {
                        bstack1l1llll_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢᭊ"): bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᭋ"),
                        bstack1l1llll_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧᭌ"): {bstack1l1llll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᭍"): result},
                    }
                )
            )
        )
        f.set_state(instance, WebDriverTestModule.bstack11l111llll1_opy_, True)
    def bstack111ll1ll1ll_opy_(self, context: bstack1l11ll1l1l1_opy_, bstack111ll1lllll_opy_= True, bstack11l1lll1111_opy_=None):
        if bstack111ll1lllll_opy_:
            driver_instances = self.bstack11l1lll11ll_opy_(context, reverse=True, _11l1llll111_opy_=bstack11l1lll1111_opy_)
        else:
            driver_instances = self.bstack11l1lll1l11_opy_(context, reverse=True, _11l1llll111_opy_=bstack11l1lll1111_opy_)
        return [f for f in driver_instances if f[1].state != AutomationFrameworkState.QUIT]
    @measure(event_name=EVENTS.bstack111llll111_opy_, stage=STAGE.SINGLE)
    def __111ll1llll1_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤ᭎")).get(bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ᭏")):
            driver_instances = f.get_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
            if not driver_instances:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤ᭐") + str(hook_info) + bstack1l1llll_opy_ (u"ࠢࠣ᭑"))
                return
            for bstack11l1l1ll111_opy_, _ in driver_instances:
                driver = bstack11l1l1ll111_opy_()
                status = f.get_state(instance, TestFramework.KEY_TEST_RESULT, None)
                if not status:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥ᭒") + str(hook_info) + bstack1l1llll_opy_ (u"ࠤࠥ᭓"))
                    return
                bstack11l11l1l1l1_opy_ = {bstack1l1llll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᭔"): status.lower()}
                bstack11l1l1l1_opy_ = f.get_state(instance, TestFramework.KEY_TEST_FAILURE, None)
                if status.lower() == bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᭕") and bstack11l1l1l1_opy_ is not None:
                    bstack11l11l1l1l1_opy_[bstack1l1llll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ᭖")] = bstack11l1l1l1_opy_[0][bstack1l1llll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᭗")][0] if isinstance(bstack11l1l1l1_opy_, list) else str(bstack11l1l1l1_opy_)
                driver.execute_script(
                    bstack1l1llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧ᭘").format(
                        json.dumps(
                            {
                                bstack1l1llll_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣ᭙"): bstack1l1llll_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ᭚"),
                                bstack1l1llll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ᭛"): bstack11l11l1l1l1_opy_,
                            }
                        )
                    )
                )
            f.set_state(instance, WebDriverTestModule.bstack11l111llll1_opy_, True)
    @measure(event_name=EVENTS.bstack1ll1111lll1_opy_, stage=STAGE.SINGLE)
    def __111lll11l11_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠤ᭜")).get(bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ᭝")):
            test_name = f.get_state(instance, TestFramework.KEY_AUTOMATE_SESSION_NAME, None)
            if not test_name:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧ᭞"))
                return
            driver_instances = f.get_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
            if not driver_instances:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤ᭟") + str(hook_info) + bstack1l1llll_opy_ (u"ࠣࠤ᭠"))
                return
            for bstack11l1l1ll111_opy_, bstack111ll1lll11_opy_ in driver_instances:
                if not SeleniumFramework.bstack11l1ll1l11l_opy_(bstack111ll1lll11_opy_):
                    continue
                driver = bstack11l1l1ll111_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢ᭡").format(
                        json.dumps(
                            {
                                bstack1l1llll_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥ᭢"): bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ᭣"),
                                bstack1l1llll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ᭤"): {bstack1l1llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᭥"): test_name},
                            }
                        )
                    )
                )
            f.set_state(instance, WebDriverTestModule.bstack11l11l111l1_opy_, True)
    def mark_o11y_sync(
        self,
        instance: TestFrameworkTest,
        f: TestFramework,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111lll11111_opy_(f, instance, hook_info, *args, **kwargs)
        driver_instances = [d for d, _ in f.get_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])]
        if not driver_instances:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢ᭦"))
            return
        if not is_bstack_automation():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ᭧"))
            return
        for bstack111lll1l11l_opy_ in driver_instances:
            driver = bstack111lll1l11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1llll_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢ᭨") + str(timestamp)
            driver.execute_script(
                bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣ᭩").format(
                    json.dumps(
                        {
                            bstack1l1llll_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦ᭪"): bstack1l1llll_opy_ (u"ࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ᭫"),
                            bstack1l1llll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ᭬"): {
                                bstack1l1llll_opy_ (u"ࠢࡵࡻࡳࡩࠧ᭭"): bstack1l1llll_opy_ (u"ࠣࡃࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠧ᭮"),
                                bstack1l1llll_opy_ (u"ࠤࡧࡥࡹࡧࠢ᭯"): data,
                                bstack1l1llll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤ᭰"): bstack1l1llll_opy_ (u"ࠦࡩ࡫ࡢࡶࡩࠥ᭱")
                            }
                        }
                    )
                )
            )
    def get_cbt_event(
        self,
        instance: TestFrameworkTest,
        f: TestFramework,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack111lll11111_opy_(f, instance, hook_info, *args, **kwargs)
        keys = [
            WebDriverTestModule.KEY_AUTOMATION_SESSIONS,
            WebDriverTestModule.KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS,
        ]
        driver_instances = []
        for key in keys:
            driver_instances.extend(f.get_state(instance, key, []))
        if not driver_instances:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡢࡰࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡴࡰࠢ࡯࡭ࡳࡱࠢ᭲"))
            return
        if f.get_state(instance, WebDriverTestModule.KEY_CBT_SESSION_CREATED, False):
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡄࡄࡗࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡲࡦࡣࡷࡩࡩࠨ᭳"))
            return
        self.ensure_bin_session()
        time_start = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.get_state(instance, TestFramework.KEY_PLATFORM_INDEX)
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ᭴").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_NAME)
        req.test_framework_version = TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION)
        req.test_framework_state = hook_info[0].name
        req.test_hook_state = hook_info[1].name
        req.test_uuid = TestFramework.get_state(instance, TestFramework.KEY_TEST_UUID)
        for bstack11l1l1ll111_opy_, driver in driver_instances:
            bstack1l11lll1l1l_opy_ = driver.data.get(bstack1l1llll_opy_ (u"ࠣࡴࡤࡲࡰࠨ᭵"))
            bstack111lll11ll1_opy_ = False
            if bstack1l11lll1l1l_opy_ is None:
                bstack111lll11ll1_opy_ = True
            else:
                try:
                    bstack111lll11ll1_opy_ = int(bstack1l11lll1l1l_opy_) == 1
                except (TypeError, ValueError):
                    bstack111lll11ll1_opy_ = False
            if bstack111lll11ll1_opy_:
                try:
                    webdriver = bstack11l1l1ll111_opy_()
                    if webdriver is None:
                        self.logger.debug(bstack1l1llll_opy_ (u"ࠤ࡚ࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠡࠪࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠥ࡫ࡸࡱ࡫ࡵࡩࡩ࠯ࠢ᭶"))
                        continue
                    session = req.automation_sessions.add()
                    session.provider = (
                        bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤ᭷")
                        if SeleniumFramework.get_state(driver, SeleniumFramework.bstack111lll11l1l_opy_, False)
                        else bstack1l1llll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥ᭸")
                    )
                    session.ref = driver.ref()
                    session.hub_url = SeleniumFramework.get_state(driver, SeleniumFramework.bstack11lll111_opy_, bstack1l1llll_opy_ (u"ࠧࠨ᭹"))
                    session.framework_name = driver.framework_name
                    session.framework_version = driver.framework_version
                    session.framework_session_id = SeleniumFramework.get_state(driver, SeleniumFramework.bstack111lllll_opy_, bstack1l1llll_opy_ (u"ࠨࠢ᭺"))
                    try:
                        from bstack_utils.helper import bstack11ll11lll1_opy_, bstack111lll111l1_opy_
                        if bstack11ll11lll1_opy_():
                            session.provider = bstack1l1llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨ᭻")
                            session.product = bstack1l1llll_opy_ (u"ࠣ࡮ࡲࡥࡩ࡚ࡥࡴࡶ࡬ࡲ࡬ࠨ᭼")
                            _111lll1111l_opy_ = bstack111lll111l1_opy_()
                            if _111lll1111l_opy_:
                                session.framework_session_id = _111lll1111l_opy_
                    except Exception as _111ll1lll1l_opy_:
                        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡏࡘࡘࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡖࡩࡸࡹࡩࡰࡰࠣࡸࡦ࡭ࡧࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ᭽").format(_111ll1lll1l_opy_))
                    caps = None
                    if hasattr(webdriver, bstack1l1llll_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤ᭾")):
                        try:
                            caps = webdriver.capabilities
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡪࡩࡳࡧࡦࡸࡱࡿࠠࡧࡴࡲࡱࠥࡪࡲࡪࡸࡨࡶ࠳ࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ᭿"))
                        except Exception as e:
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠢࠥᮀ") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢᮁ"))
                    try:
                        bstack111lll11lll_opy_ = json.dumps(caps).encode(bstack1l1llll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᮂ")) if caps else bstack111lll1l1l1_opy_ (u"ࠣࡽࢀࠦᮃ")
                        req.capabilities = bstack111lll11lll_opy_
                    except Exception as e:
                        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡪࡩࡹࡥࡣࡣࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤࡸ࡫ࡲࡪࡣ࡯࡭ࡿ࡫ࠠࡤࡣࡳࡷࠥ࡬࡯ࡳࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࠧᮄ") + str(e) + bstack1l1llll_opy_ (u"ࠥࠦᮅ"))
                except Exception as e:
                    self.logger.error(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡶࡨࡱ࠿ࠦࠢᮆ") + str(str(e)) + bstack1l1llll_opy_ (u"ࠧࠨᮇ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack11ll111ll11_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        driver_instances = f.get_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
        if not is_bstack_automation() and len(driver_instances) == 0:
            driver_instances = f.get_state(instance, WebDriverTestModule.KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS, [])
        if not driver_instances:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᮈ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠢࠣᮉ"))
            return {}
        for bstack11l1l1ll111_opy_, bstack11l1l1lll1l_opy_ in driver_instances:
            bstack1l11lll1l1l_opy_ = bstack11l1l1lll1l_opy_.data.get(bstack1l1llll_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᮊ"))
            self.logger.info(bstack1l1llll_opy_ (u"ࠤࡪࡩࡳ࡫ࡲࡢࡶࡨࡣࡵࡲࡡࡵࡨࡲࡶࡲࡥࡤࡦࡶࡤ࡭ࡱࡹࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱ࠺ࠡࠤᮋ") + str(bstack1l11lll1l1l_opy_) + bstack1l1llll_opy_ (u"ࠥࠦᮌ"))
            if bstack1l11lll1l1l_opy_ is None or bstack1l11lll1l1l_opy_ == bstack1l1llll_opy_ (u"ࠫ࠶࠭ᮍ"):
                driver = bstack11l1l1ll111_opy_()
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧ࡭ࡥ࡯ࡧࡵࡥࡹ࡫࡟ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡧࡩࡹࡧࡩ࡭ࡵࠣࡪࡪࡺࡣࡩࡧࡧࠤࡩࡸࡩࡷࡧࡵ࠾ࠥࠨᮎ") + str(bstack11l1l1lll1l_opy_.data[bstack1l1llll_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᮏ")]) + bstack1l1llll_opy_ (u"ࠢࠣᮐ"))
                if not driver:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᮑ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠤࠥᮒ"))
                    return {}
                capabilities = f.get_state(bstack11l1l1lll1l_opy_, SeleniumFramework.bstack1l111lll_opy_)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡫ࡪࡴࡥࡳࡣࡷࡩࡤࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࠤᮓ") + str(capabilities) + bstack1l1llll_opy_ (u"ࠦࠧᮔ"))
                if not capabilities:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᮕ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠨࠢᮖ"))
                    return {}
                return capabilities.get(bstack1l1llll_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧᮗ"), {})
        return None
    def bstack11ll11lll1l_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        driver_instances = f.get_state(instance, WebDriverTestModule.KEY_AUTOMATION_SESSIONS, [])
        if not is_bstack_automation() and len(driver_instances) == 0:
            driver_instances = f.get_state(instance, WebDriverTestModule.KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS, [])
        if not driver_instances:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᮘ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠤࠥᮙ"))
            return
        if len(driver_instances) > 1:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᮚ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠦࠧᮛ"))
        for bstack11l1l1ll111_opy_, bstack11l1l1lll1l_opy_ in driver_instances:
            driver = bstack11l1l1ll111_opy_()
            bstack1l11lll1l1l_opy_ = bstack11l1l1lll1l_opy_.data.get(bstack1l1llll_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᮜ"))
            self.logger.info(bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡧࡶ࡮ࡼࡥࡳࠢࡵࡥࡳࡱ࠺ࠡࠤᮝ") + str(bstack1l11lll1l1l_opy_) + bstack1l1llll_opy_ (u"ࠢࠣᮞ"))
            if (bstack1l11lll1l1l_opy_ is None or int(bstack1l11lll1l1l_opy_) == 1) and driver:
                return driver
        return None