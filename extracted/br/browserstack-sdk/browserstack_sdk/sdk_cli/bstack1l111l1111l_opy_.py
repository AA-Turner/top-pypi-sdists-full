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
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance
from browserstack_sdk.sdk_cli.utils.bstack111111ll1l_opy_ import bstack111ll11l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    TestFrameworkTest,
    TestHookState,
    TestFrameworkContext,
    LogEntry,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import get_writable_dir
from bstack_utils.performance_tester import PerformanceTester
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
from browserstack_sdk.sdk_cli.utils.custom_tag_manager import CustomTagManager
from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
BROWSERSTACK_ROOT_DIR = get_writable_dir()
bstack111ll11l11l_opy_ = 1.0
UPLOADED_ATTACHMENTS_PREFIX = bstack1l1llll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᴑ")
bstack111l1l1l111_opy_ = bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᴒ")
bstack111l1l11ll1_opy_ = bstack1l1llll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᴓ")
bstack111l1l111l1_opy_ = bstack1l1llll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᴔ")
bstack111l1l111ll_opy_ = bstack1l1llll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᴕ")
_processed_attachments = set()
class bstack11llll111l1_opy_(TestFramework):
    bstack111l11lll11_opy_ = bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᴖ")
    KEY_HOOKS_STARTED = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᴗ")
    KEY_HOOKS_FINISHED = bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᴘ")
    KEY_HOOK_LAST_STARTED = bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᴙ")
    KEY_HOOK_LAST_FINISHED = bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᴚ")
    bstack111l11ll11l_opy_: bool
    async_dispatcher: AsyncDispatcher = None
    cli_service = None
    hook_events = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        test_framework_versions: Dict[str, str],
        test_frameworks: List[str] = [bstack1l1llll_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦᴛ")],
        async_dispatcher: AsyncDispatcher = None,
        cli_service=None
    ):
        super().__init__(test_frameworks, test_framework_versions, async_dispatcher)
        self.bstack111l11ll11l_opy_ = any(bstack1l1llll_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥᴜ") in item.lower() for item in test_frameworks)
        self.cli_service = cli_service
    def track_event(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack11llll111l1_opy_.hook_events:
            bstack111ll11l1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤᴝ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111l11ll11l_opy_:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࡻࡾࠤᴞ").format(str(self.test_frameworks)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᴟ").format(args, kwargs))
            return
        instance = self.__resolve_instance(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠤᴠ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack11llll111l1_opy_.hook_events:
                random_label = bstack1l1llll_opy_ (u"ࠤࠥᴡ")
                name = bstack1l1llll_opy_ (u"ࠥࠦᴢ")
                if (test_hook_state == TestHookState.PRE):
                    random_label = PerformanceTester.mark_start(EVENTS.bstack111l1l11l11_opy_.value)
                    name = str(EVENTS.bstack111l1l11l11_opy_.name) + bstack1l1llll_opy_ (u"ࠦ࠿ࠨᴣ") + str(test_framework_state.name)
                else:
                    random_label = PerformanceTester.mark_start(EVENTS.bstack111l1l11l1l_opy_.value)
                    name = str(EVENTS.bstack111l1l11l1l_opy_.name) + bstack1l1llll_opy_ (u"ࠧࡀࠢᴤ") + str(test_framework_state.name)
                TestFramework.bstack111l1ll11ll_opy_(instance, name, random_label)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᴥ").format(e))
        try:
            if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ID) and test_hook_state == TestHookState.PRE:
                test = bstack11llll111l1_opy_.__111l1l1111l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥᴦ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.has_state(instance, TestFramework.KEY_TEST_STARTED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_STARTED_AT, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤᴧ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.has_state(instance, TestFramework.KEY_TEST_ENDED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_ENDED_AT, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣᴨ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack11llll111l1_opy_.__111ll111lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__load_test_result(instance, *args)
                self.__load_custom_tags(instance)
            elif test_framework_state in bstack11llll111l1_opy_.hook_events:
                self.__track_hook_event(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠨᴩ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.run_hooks(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack11llll111l1_opy_.hook_events:
                random_label = bstack1l1llll_opy_ (u"ࠦࠧᴪ")
                name = bstack1l1llll_opy_ (u"ࠧࠨᴫ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111l1l11l11_opy_.name) + bstack1l1llll_opy_ (u"ࠨ࠺ࠣᴬ") + str(test_framework_state.name)
                    random_label = TestFramework.bstack111ll111l11_opy_(instance, name)
                    PerformanceTester.end(EVENTS.bstack111l1l11l11_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᴭ"), random_label + bstack1l1llll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᴮ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111l1l11l1l_opy_.name) + bstack1l1llll_opy_ (u"ࠤ࠽ࠦᴯ") + str(test_framework_state.name)
                    random_label = TestFramework.bstack111ll111l11_opy_(instance, name)
                    PerformanceTester.end(EVENTS.bstack111l1l11l1l_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᴰ"), random_label + bstack1l1llll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᴱ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᴲ").format(e))
    def is_robot_framework(self):
        return self.bstack111l11ll11l_opy_
    def is_pytest_framework(self):
        return False
    def is_behave_framework(self):
        return False
    def __111l11ll111_opy_(self, *args):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡵࡩࡸࡻ࡬ࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦᴳ")
        if len(args) > 1 and hasattr(args[1], bstack1l1llll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᴴ")):
            result = args[1]
            if result:
                return TestFramework.extract_keys(result, [bstack1l1llll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᴵ"), bstack1l1llll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᴶ"), bstack1l1llll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡶ࡬ࡱࡪࠨᴷ"), bstack1l1llll_opy_ (u"ࠦࡪࡴࡤࡵ࡫ࡰࡩࠧᴸ"), bstack1l1llll_opy_ (u"ࠧ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠥᴹ")])
        return None
    def __load_test_result(self, instance: TestFrameworkTest, *args):
        result = self.__111l11ll111_opy_(*args)
        if not result:
            return
        failure = None
        failure_type = None
        status = result.get(bstack1l1llll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᴺ"), bstack1l1llll_opy_ (u"ࠢࡏࡑࡗࠤࡗ࡛ࡎࠣᴻ"))
        if status == bstack1l1llll_opy_ (u"ࠣࡈࡄࡍࡑࠨᴼ") and result.get(bstack1l1llll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᴽ")):
            failure = [{bstack1l1llll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᴾ"): [result.get(bstack1l1llll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᴿ"), bstack1l1llll_opy_ (u"ࠧࠨᵀ"))]}]
            failure_type = bstack1l1llll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᵁ")
        test_result = TestFramework.DEFAULT_TEST_RESULT
        if status == bstack1l1llll_opy_ (u"ࠢࡑࡃࡖࡗࠧᵂ"):
            test_result = bstack1l1llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᵃ")
        elif status == bstack1l1llll_opy_ (u"ࠤࡉࡅࡎࡒࠢᵄ"):
            test_result = bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᵅ")
        elif status == bstack1l1llll_opy_ (u"ࠦࡘࡑࡉࡑࠤᵆ"):
            test_result = bstack1l1llll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᵇ")
        if test_result != TestFramework.DEFAULT_TEST_RESULT:
            TestFramework.set_state(instance, TestFramework.KEY_TEST_RESULT_AT, datetime.now(tz=timezone.utc))
        TestFramework.set_state_entries(instance, {
            TestFramework.KEY_TEST_FAILURE: failure,
            TestFramework.KEY_TEST_FAILURE_TYPE: failure_type,
            TestFramework.KEY_TEST_RESULT: test_result,
        })
    def __resolve_instance(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111l11llll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111l11l1lll_opy_(test) if test else None
                if target:
                    self.__111l11ll1l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢᵈ"), None)
            elif hasattr(args[0], bstack1l1llll_opy_ (u"ࠢࡪࡦࠥᵉ")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.get_tracked_instance(target) if target else None
        return instance
    def __track_hook_event(
        self,
        instance: TestFrameworkTest,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        hooks_started = TestFramework.get_state(instance, bstack11llll111l1_opy_.KEY_HOOKS_STARTED, {})
        if not key in hooks_started:
            hooks_started[key] = []
        hooks_finished = TestFramework.get_state(instance, bstack11llll111l1_opy_.KEY_HOOKS_FINISHED, {})
        if not key in hooks_finished:
            hooks_finished[key] = []
        updates = {
            bstack11llll111l1_opy_.KEY_HOOKS_STARTED: hooks_started,
            bstack11llll111l1_opy_.KEY_HOOKS_FINISHED: hooks_finished,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1l1llll_opy_ (u"ࠣࠤᵊ")
            if len(args) > 0 and hasattr(args[0], bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᵋ")):
                hook_name = args[0].name
            hook = {
                bstack1l1llll_opy_ (u"ࠥ࡯ࡪࡿࠢᵌ"): key,
                TestFramework.KEY_HOOK_ID: uuid4().__str__(),
                TestFramework.KEY_HOOK_RESULT: TestFramework.DEFAULT_HOOK_RESULT,
                TestFramework.KEY_EVENT_STARTED_AT: datetime.now(tz=timezone.utc),
                TestFramework.KEY_HOOK_LOGS: [],
                TestFramework.KEY_HOOK_NAME: hook_name,
                TestFramework.KEY_CUSTOM_TAGS: CustomTagManager.get_test_level_custom_metadata()
            }
            hooks_started[key].append(hook)
            updates[bstack11llll111l1_opy_.KEY_HOOK_LAST_STARTED] = key
        elif test_hook_state == TestHookState.POST:
            hooks_list = hooks_started.get(key, [])
            hook = hooks_list.pop() if hooks_list else None
            if hook:
                result = self.__111l11ll111_opy_(*args)
                if result:
                    hook_result = result.get(bstack1l1llll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᵍ"), TestFramework.DEFAULT_HOOK_RESULT)
                    if hook_result == bstack1l1llll_opy_ (u"ࠧࡖࡁࡔࡕࠥᵎ"):
                        hook_result = bstack1l1llll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᵏ")
                    elif hook_result == bstack1l1llll_opy_ (u"ࠢࡇࡃࡌࡐࠧᵐ"):
                        hook_result = bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᵑ")
                    if hook_result != TestFramework.DEFAULT_HOOK_RESULT:
                        hook[TestFramework.KEY_HOOK_RESULT] = hook_result
                hook[TestFramework.KEY_EVENT_ENDED_AT] = datetime.now(tz=timezone.utc)
                hook[TestFramework.KEY_CUSTOM_TAGS] = CustomTagManager.get_test_level_custom_metadata()
                self.bstack111ll11lll1_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll111111_opy_, [])
                if logs:
                    self.send_log_created_event(instance, logs)
                hooks_finished[key].append(hook)
                updates[bstack11llll111l1_opy_.KEY_HOOK_LAST_FINISHED] = key
        TestFramework.set_state_entries(instance, updates)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀ࠲ࢀࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࢀࢃࠢᵒ").format(key, test_hook_state, hooks_started, hooks_finished))
    def __111l11llll1_opy_(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1llll_opy_ (u"࡚ࠥࠦࠧࡲࡢࡥ࡮ࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡦࡸࡨࡲࡹࡹࠠࠩࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࠣࠤࠥᵓ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1l1llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᵔ"), None)
        bstack11l1111l1_opy_ = getattr(keyword, bstack1l1llll_opy_ (u"ࠧࡺࡹࡱࡧࠥᵕ"), None)
        test_id = kwargs.get(bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢᵖ"), None)
        if not test_id:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥ࡫ࡦࡻࡺࡳࡷࡪ࡟ࡦࡸࡨࡲࡹࡀࠠ࡯ࡱࠣࡸࡪࡹࡴࡠ࡫ࡧࠤ࡮ࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠤᵗ").format(keyword_name))
            return None
        instance = TestFramework.get_tracked_instance(test_id)
        if not instance:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟࡬ࡧࡼࡻࡴࡸࡤࡠࡧࡹࡩࡳࡺ࠺ࠡࡰࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡷࡩࡸࡺ࡟ࡪࡦࡀࡿࢂࠨᵘ").format(test_id))
            return None
        bstack111l1l11111_opy_ = TestFramework.get_state(instance, bstack11llll111l1_opy_.bstack111l11lll11_opy_, {})
        if os.getenv(bstack1l1llll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡍࡈ࡝࡜ࡕࡒࡅࡕࠥᵙ"), bstack1l1llll_opy_ (u"ࠥ࠵ࠧᵚ")) == bstack1l1llll_opy_ (u"ࠦ࠶ࠨᵛ"):
            bstack111l11l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦᵜ").format(bstack11l1111l1_opy_, keyword_name)
            bstack111l1ll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack111l11ll1ll_opy_ = {
                bstack1l1llll_opy_ (u"ࠨ࡫ࡦࡻࠥᵝ"): bstack111l11l1ll1_opy_,
                bstack1l1llll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᵞ"): keyword_name,
                bstack1l1llll_opy_ (u"ࠣࡶࡼࡴࡪࠨᵟ"): bstack11l1111l1_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l11ll1ll_opy_[bstack1l1llll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᵠ")] = uuid4().__str__()
                bstack111l11ll1ll_opy_[bstack11llll111l1_opy_.KEY_EVENT_STARTED_AT] = bstack111l1ll111l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l11ll1ll_opy_[bstack11llll111l1_opy_.KEY_EVENT_ENDED_AT] = bstack111l1ll111l_opy_
                if len(args) > 1 and hasattr(args[1], bstack1l1llll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᵡ")):
                    bstack111l11ll1ll_opy_[bstack1l1llll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᵢ")] = args[1].status
            if bstack111l11l1ll1_opy_ in bstack111l1l11111_opy_:
                bstack111l1l11111_opy_[bstack111l11l1ll1_opy_].update(bstack111l11ll1ll_opy_)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠣࡸࡾࡶࡥ࠾ࡽࢀࠦᵣ").format(keyword_name, bstack11l1111l1_opy_))
            else:
                bstack111l1l11111_opy_[bstack111l11l1ll1_opy_] = bstack111l11ll1ll_opy_
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠢࡷࡽࡵ࡫࠽ࡼࡿࠥᵤ").format(keyword_name, bstack11l1111l1_opy_))
        TestFramework.set_state(instance, bstack11llll111l1_opy_.bstack111l11lll11_opy_, bstack111l1l11111_opy_)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪࡳ࠾ࡽࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠤᵥ").format(len(bstack111l1l11111_opy_), instance.ref()))
        return instance
    def __111l11ll1l1_opy_(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = TrackedInstance.create_context(target)
        ob = TestFrameworkTest(ctx, self.test_frameworks, self.test_framework_versions, test_framework_state)
        TestFramework.set_state_entries(ob, {
            TestFramework.KEY_TEST_FRAMEWORK_NAME: context.test_framework_name,
            TestFramework.KEY_TEST_FRAMEWORK_VERSION: context.test_framework_version,
            TestFramework.KEY_TEST_LOGS: [],
            bstack11llll111l1_opy_.bstack111l11lll11_opy_: {},
            bstack11llll111l1_opy_.KEY_HOOKS_FINISHED: {},
            bstack11llll111l1_opy_.KEY_HOOKS_STARTED: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1l1llll_opy_ (u"ࠣࡵࡲࡹࡷࡩࡥࠣᵦ")):
            TestFramework.set_state(ob, TestFramework.KEY_TEST_LOCATION, str(test.source))
        if context.platform_index >= 0:
            TestFramework.set_state(ob, TestFramework.KEY_PLATFORM_INDEX, context.platform_index)
        TestFramework.instances[ctx.id] = ob
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࡻࡾࠤᵧ").format(ctx.id, target, args, TestFramework.instances.keys()))
        return ob
    def get_log_entries(self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]):
        bstack111ll111ll1_opy_ = (
            bstack11llll111l1_opy_.KEY_HOOK_LAST_STARTED
            if hook_info[1] == TestHookState.PRE
            else bstack11llll111l1_opy_.KEY_HOOK_LAST_FINISHED
        )
        hook = bstack11llll111l1_opy_.bstack111l1ll11l1_opy_(instance, bstack111ll111ll1_opy_)
        entries = hook.get(TestFramework.KEY_HOOK_LOGS, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []))
        return entries
    def clear_logs(self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]):
        bstack111ll111ll1_opy_ = (
            bstack11llll111l1_opy_.KEY_HOOK_LAST_STARTED
            if hook_info[1] == TestHookState.PRE
            else bstack11llll111l1_opy_.KEY_HOOK_LAST_FINISHED
        )
        bstack11llll111l1_opy_.bstack111l1lll111_opy_(instance, bstack111ll111ll1_opy_)
        TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []).clear()
    def bstack111ll11lll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᵨ")
        global _processed_attachments
        platform_index = os.environ[bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᵩ")]
        attachment_dir = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), bstack111l1l111l1_opy_)
        if not os.path.exists(attachment_dir) or not os.path.isdir(attachment_dir):
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᵪ").format(attachment_dir))
            return
        logs = hook.get(bstack1l1llll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᵫ"), [])
        with os.scandir(attachment_dir) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _processed_attachments:
                    self.logger.info(bstack1l1llll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᵬ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1llll_opy_ (u"ࠣࠤᵭ")
                    log_entry = LogEntry(
                        kind=bstack1l1llll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᵮ"),
                        message=bstack1l1llll_opy_ (u"ࠥࠦᵯ"),
                        level=bstack1l1llll_opy_ (u"ࠦࠧᵰ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        fileSize=entry.stat().st_size,
                        attachmentType=bstack1l1llll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᵱ"),
                        filePath=os.path.abspath(entry.path),
                        hook_run_uuid=hook.get(TestFramework.KEY_HOOK_ID)
                    )
                    logs.append(log_entry)
                    _processed_attachments.add(abs_path)
        platform_index = os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᵲ")]
        bstack111l1lll1ll_opy_ = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), bstack111l1l111l1_opy_, bstack111l1l111ll_opy_)
        if not os.path.exists(bstack111l1lll1ll_opy_) or not os.path.isdir(bstack111l1lll1ll_opy_):
            self.logger.info(bstack1l1llll_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᵳ").format(bstack111l1lll1ll_opy_))
        else:
            self.logger.info(bstack1l1llll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᵴ").format(bstack111l1lll1ll_opy_))
            with os.scandir(bstack111l1lll1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _processed_attachments:
                        self.logger.info(bstack1l1llll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᵵ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1llll_opy_ (u"ࠥࠦᵶ")
                        log_entry = LogEntry(
                            kind=bstack1l1llll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᵷ"),
                            message=bstack1l1llll_opy_ (u"ࠧࠨᵸ"),
                            level=bstack1l1llll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᵹ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            fileSize=entry.stat().st_size,
                            attachmentType=bstack1l1llll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᵺ"),
                            filePath=os.path.abspath(entry.path),
                            build_run_uuid=hook.get(TestFramework.KEY_HOOK_ID)
                        )
                        logs.append(log_entry)
                        _processed_attachments.add(abs_path)
        hook[bstack1l1llll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᵻ")] = logs
    def send_log_created_event(
        self,
        test_instance: TestFrameworkTest,
        entries: List[LogEntry],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᵼ"))
        req.platform_index = TestFramework.get_state(test_instance, TestFramework.KEY_PLATFORM_INDEX)
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᵽ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(test_instance.context.hash)
        req.execution_context.thread_id = str(test_instance.context.thread_id)
        req.execution_context.process_id = str(test_instance.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_NAME, bstack1l1llll_opy_ (u"ࠦࠧᵾ"))
            log_entry.test_framework_version = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION, bstack1l1llll_opy_ (u"ࠧࠨᵿ"))
            log_entry.uuid = entry.hook_run_uuid or bstack1l1llll_opy_ (u"ࠨࠢᶀ")
            log_entry.test_framework_state = test_instance.state.name
            log_entry.message = entry.message.encode(bstack1l1llll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᶁ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1llll_opy_ (u"ࠣࠤᶂ")
            if entry.kind == bstack1l1llll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᶃ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.fileSize
                log_entry.file_path = entry.filePath
        def make_grpc_request():
            time_start = datetime.now()
            try:
                self.cli_service.LogCreatedEvent(req)
                test_instance.add_benchmark(bstack1l1llll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᶄ"), datetime.now() - time_start)
            except grpc.RpcError as e:
                self.log_error(bstack1l1llll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᶅ").format(str(e)))
                traceback.print_exc()
        self.async_dispatcher.enqueue(make_grpc_request)
    def __load_custom_tags(self, instance) -> None:
        bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᶆ")
        updates = {bstack1l1llll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᶇ"): CustomTagManager.get_test_level_custom_metadata()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.set_state_entries(instance, updates)
        CustomTagManager.reset_test_level_custom_metadata()
    @staticmethod
    def bstack111l1ll11l1_opy_(instance: TestFrameworkTest, bstack111ll111ll1_opy_: str):
        bstack111ll1111ll_opy_ = (
            bstack11llll111l1_opy_.KEY_HOOKS_FINISHED
            if bstack111ll111ll1_opy_ == bstack11llll111l1_opy_.KEY_HOOK_LAST_FINISHED
            else bstack11llll111l1_opy_.KEY_HOOKS_STARTED
        )
        bstack111ll11111l_opy_ = TestFramework.get_state(instance, bstack111ll111ll1_opy_, None)
        bstack111l1llllll_opy_ = TestFramework.get_state(instance, bstack111ll1111ll_opy_, None) if bstack111ll11111l_opy_ else None
        return (
            bstack111l1llllll_opy_[bstack111ll11111l_opy_][-1]
            if isinstance(bstack111l1llllll_opy_, dict) and len(bstack111l1llllll_opy_.get(bstack111ll11111l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack111l1lll111_opy_(instance: TestFrameworkTest, bstack111ll111ll1_opy_: str):
        hook = bstack11llll111l1_opy_.bstack111l1ll11l1_opy_(instance, bstack111ll111ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.KEY_HOOK_LOGS, []).clear()
    @staticmethod
    def __111ll111lll_opy_(instance: TestFrameworkTest, *args):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡓࡶࡴࡩࡥࡴࡵࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࡶࠦࠧࠨᶈ")
        if len(args) < 1:
            return
        if os.getenv(bstack1l1llll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᶉ"), bstack1l1llll_opy_ (u"ࠤ࠴ࠦᶊ")) != bstack1l1llll_opy_ (u"ࠥ࠵ࠧᶋ"):
            bstack11llll111l1_opy_.logger.warning(bstack1l1llll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡲ࡯ࡨࡵࠥᶌ"))
            return
        message = args[0]
        if not hasattr(message, bstack1l1llll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᶍ")):
            return
        is_screenshot = hasattr(message, bstack1l1llll_opy_ (u"࠭࡫ࡪࡰࡧࠫᶎ")) and message.kind == bstack1l1llll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᶏ")
        log_entry = LogEntry(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.KIND_LOG,
            message=message.message if hasattr(message, bstack1l1llll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᶐ")) else bstack1l1llll_opy_ (u"ࠤࠥᶑ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1l1llll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤᶒ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1l1llll_opy_ (u"ࠦࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠤᶓ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1l1llll_opy_ (u"ࠧࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠣᶔ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111l1ll1lll_opy_ = {
            bstack1l1llll_opy_ (u"ࠨࡓࡆࡖࡘࡔࠧᶕ"): (bstack11llll111l1_opy_.KEY_HOOK_LAST_STARTED, bstack11llll111l1_opy_.KEY_HOOKS_STARTED),
            bstack1l1llll_opy_ (u"ࠢࡕࡇࡄࡖࡉࡕࡗࡏࠤᶖ"): (bstack11llll111l1_opy_.KEY_HOOK_LAST_FINISHED, bstack11llll111l1_opy_.KEY_HOOKS_FINISHED),
        }
        bstack111l11lll1l_opy_ = None
        if len(args) > 1:
            bstack111l11lll1l_opy_ = args[1]
        if bstack111l11lll1l_opy_ and bstack111l11lll1l_opy_ in bstack111l1ll1lll_opy_:
            bstack111l1l1lll1_opy_, bstack111ll1111ll_opy_ = bstack111l1ll1lll_opy_[bstack111l11lll1l_opy_]
            bstack111ll11l1ll_opy_ = TestFramework.get_state(instance, bstack111l1l1lll1_opy_, None)
            bstack111l1llllll_opy_ = TestFramework.get_state(instance, bstack111ll1111ll_opy_, None) if bstack111ll11l1ll_opy_ else None
            if isinstance(bstack111l1llllll_opy_, dict) and len(bstack111l1llllll_opy_.get(bstack111ll11l1ll_opy_, [])) > 0:
                hook = bstack111l1llllll_opy_[bstack111ll11l1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.KEY_HOOK_LOGS in hook:
                    hook[TestFramework.KEY_HOOK_LOGS].append(log_entry)
                    return
        logs = TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1l1111l_opy_(test) -> Dict[str, Any]:
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡔࡦࡸࡳࡦࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡹ࡫ࡳࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦᶗ")
        test_id = bstack11llll111l1_opy_.__111l11l1lll_opy_(test)
        test_name = test.name if hasattr(test, bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᶘ")) else None
        bstack111ll11l111_opy_ = str(test.source) if hasattr(test, bstack1l1llll_opy_ (u"ࠥࡷࡴࡻࡲࡤࡧࠥᶙ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1l1llll_opy_ (u"ࠦࡹࡧࡧࡴࠤᶚ")) else []
        bstack111l11lllll_opy_ =bstack1l1llll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢᶛ").format(bstack1l1llll_opy_ (u"ࠨࠠࠣᶜ").join(test_tags), test_name) if test_tags else test_name
        bstack111l1l11lll_opy_ = []
        if bstack111ll11l111_opy_:
            from browserstack_sdk.bstack11111l11_opy_ import RobotHandler
            bstack111l1l11lll_opy_ = RobotHandler.bstack1llll1ll1_opy_(bstack111ll11l111_opy_)
        if not bstack111l1l11lll_opy_ and test_name:
            bstack111l1l11lll_opy_ = [test_name]
        return {
            TestFramework.KEY_TEST_UUID: uuid4().__str__(),
            TestFramework.KEY_TEST_ID: test_id,
            TestFramework.KEY_TEST_NAME: test_name,
            TestFramework.KEY_TEST_RERUN_NAME: test_id,
            TestFramework.KEY_TEST_FILE_PATH: bstack111ll11l111_opy_,
            TestFramework.KEY_TEST_TAGS: test_tags,
            TestFramework.bstack111l1l1l1ll_opy_: bstack111l11lllll_opy_,
            TestFramework.KEY_TEST_RESULT: TestFramework.DEFAULT_TEST_RESULT,
            TestFramework.KEY_AUTOMATE_SESSION_NAME: test_id,
            TestFramework.KEY_TEST_SCOPES: bstack111l1l11lll_opy_
        }
    @staticmethod
    def __111l11l1lll_opy_(test):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡵ࡯࡫ࡴࡹࡪࠦࡴࡦࡵࡷࠤࡎࡊࠠࡧࡴࡲࡱࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡵࡧࡶࡸࠥࡵࡢ࡫ࡧࡦࡸࠧࠨࠢᶝ")
        if hasattr(test, bstack1l1llll_opy_ (u"ࠣ࡫ࡧࠦᶞ")):
            return test.id
        elif hasattr(test, bstack1l1llll_opy_ (u"ࠤ࡯ࡳࡳ࡭࡮ࡢ࡯ࡨࠦᶟ")):
            return test.longname
        elif hasattr(test, bstack1l1llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᶠ")):
            return test.name
        return None