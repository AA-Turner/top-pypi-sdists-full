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
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    TestFrameworkTest,
    TestHookState,
    TestFrameworkContext,
    LogEntry,
)
import traceback
from bstack_utils.helper import get_writable_dir
from bstack_utils.performance_tester import PerformanceTester
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.custom_tag_manager import CustomTagManager
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
BROWSERSTACK_ROOT_DIR = get_writable_dir()
UPLOADED_ATTACHMENTS_PREFIX = bstack1l1llll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᮼ")
bstack111l1lllll1_opy_ = bstack1l1llll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᮽ")
bstack111l1l1l1l1_opy_ = bstack1l1llll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᮾ")
bstack111ll11l11l_opy_ = 1.0
_processed_attachments = set()
class PytestBDDFramework(TestFramework):
    bstack11l1ll1l1ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᮿ")
    KEY_HOOKS_STARTED = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᯀ")
    KEY_HOOKS_FINISHED = bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᯁ")
    KEY_HOOK_LAST_STARTED = bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᯂ")
    KEY_HOOK_LAST_FINISHED = bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᯃ")
    bstack111l1l1ll11_opy_: bool
    async_dispatcher: AsyncDispatcher  = None
    hook_events = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        test_framework_versions: Dict[str, str],
        test_frameworks: List[str]=[bstack1l1llll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᯄ")],
        async_dispatcher: AsyncDispatcher = None,
        cli_service=None
    ):
        super().__init__(test_frameworks, test_framework_versions, async_dispatcher)
        self.bstack111l1l1ll11_opy_ = any(bstack1l1llll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᯅ") in item.lower() for item in test_frameworks)
        self.cli_service = cli_service
    def track_event(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.hook_events:
            bstack111ll11l1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᯆ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠨࠢᯇ"))
            return
        if not self.bstack111l1l1ll11_opy_:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᯈ") + str(str(self.test_frameworks)) + bstack1l1llll_opy_ (u"ࠣࠤᯉ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᯊ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠥࠦᯋ"))
            return
        instance = self.__resolve_instance(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᯌ") + str(args) + bstack1l1llll_opy_ (u"ࠧࠨᯍ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.hook_events and test_hook_state == TestHookState.PRE:
                random_label = PerformanceTester.mark_start(EVENTS.bstack1ll11lll1l_opy_.value)
                name = str(EVENTS.bstack1ll11lll1l_opy_.name)+bstack1l1llll_opy_ (u"ࠨ࠺ࠣᯎ")+str(test_framework_state.name)
                TestFramework.bstack111l1ll11ll_opy_(instance, name, random_label)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᯏ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ID) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111ll1l1111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᯐ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠤࠥᯑ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.has_state(instance, TestFramework.KEY_TEST_STARTED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_STARTED_AT, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__111l1l1ll1l_opy_(instance, args)
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᯒ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠦࠧᯓ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.has_state(instance, TestFramework.KEY_TEST_ENDED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_ENDED_AT, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᯔ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠨࠢᯕ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__111l1l1llll_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__111ll11llll_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__111ll111lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__load_test_result(instance, *args)
                self.__load_custom_tags(instance)
            elif test_framework_state in PytestBDDFramework.hook_events:
                self.__track_hook_event(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᯖ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠣࠤᯗ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.run_hooks(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.hook_events and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1ll11lll1l_opy_.name)+bstack1l1llll_opy_ (u"ࠤ࠽ࠦᯘ")+str(test_framework_state.name)
                random_label = TestFramework.bstack111ll111l11_opy_(instance, name)
                PerformanceTester.end(EVENTS.bstack1ll11lll1l_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᯙ"), random_label+bstack1l1llll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᯚ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᯛ").format(e))
    def is_pytest_framework(self):
        return self.bstack111l1l1ll11_opy_
    def is_robot_framework(self):
        return False
    def is_behave_framework(self):
        return False
    def __111l1ll1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᯜ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.extract_keys(rep, [bstack1l1llll_opy_ (u"ࠢࡸࡪࡨࡲࠧᯝ"), bstack1l1llll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᯞ"), bstack1l1llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᯟ"), bstack1l1llll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᯠ"), bstack1l1llll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᯡ"), bstack1l1llll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᯢ")])
        return None
    def __load_test_result(self, instance: TestFrameworkTest, *args):
        result = self.__111l1ll1l11_opy_(*args)
        if not result:
            return
        failure = None
        failure_type = None
        if result.get(bstack1l1llll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᯣ"), None) == bstack1l1llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᯤ") and len(args) > 1 and getattr(args[1], bstack1l1llll_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᯥ"), None) is not None:
            failure = [{bstack1l1llll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩ᯦ࠬ"): [args[1].excinfo.exconly(), result.get(bstack1l1llll_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᯧ"), None)]}]
            failure_type = bstack1l1llll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᯨ") if bstack1l1llll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᯩ") in getattr(args[1].excinfo, bstack1l1llll_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᯪ"), bstack1l1llll_opy_ (u"ࠢࠣᯫ")) else bstack1l1llll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᯬ")
        test_result = result.get(bstack1l1llll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᯭ"), TestFramework.DEFAULT_TEST_RESULT)
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
            instance = self.__111l1ll1l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # we bstack111ll11ll11_opy_ this to be bstack1l1llll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᯮ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111ll1l111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1llll_opy_ (u"ࠦࡳࡵࡤࡦࠤᯯ"), None), bstack1l1llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᯰ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1llll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᯱ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1llll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪ᯲ࠢ"), None):
                target = args[0].nodeid
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
        hooks_started = TestFramework.get_state(instance, PytestBDDFramework.KEY_HOOKS_STARTED, {})
        if not key in hooks_started:
            hooks_started[key] = []
        hooks_finished = TestFramework.get_state(instance, PytestBDDFramework.KEY_HOOKS_FINISHED, {})
        if not key in hooks_finished:
            hooks_finished[key] = []
        updates = {
            PytestBDDFramework.KEY_HOOKS_STARTED: hooks_started,
            PytestBDDFramework.KEY_HOOKS_FINISHED: hooks_finished,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1llll_opy_ (u"ࠣ࡭ࡨࡽ᯳ࠧ"): key,
                TestFramework.KEY_HOOK_ID: uuid4().__str__(),
                TestFramework.KEY_HOOK_RESULT: TestFramework.DEFAULT_HOOK_RESULT,
                TestFramework.KEY_EVENT_STARTED_AT: datetime.now(tz=timezone.utc),
                TestFramework.KEY_HOOK_LOGS: [],
                TestFramework.KEY_HOOK_NAME: hook_name,
                TestFramework.KEY_CUSTOM_TAGS: CustomTagManager.get_test_level_custom_metadata()
            }
            hooks_started[key].append(hook)
            updates[PytestBDDFramework.KEY_HOOK_LAST_STARTED] = key
        elif test_hook_state == TestHookState.POST:
            hooks_list = hooks_started.get(key, [])
            hook = hooks_list.pop() if hooks_list else None
            if hook:
                result = self.__111l1ll1l11_opy_(*args)
                if result:
                    hook_result = result.get(bstack1l1llll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥ᯴"), TestFramework.DEFAULT_HOOK_RESULT)
                    if hook_result != TestFramework.DEFAULT_HOOK_RESULT:
                        hook[TestFramework.KEY_HOOK_RESULT] = hook_result
                hook[TestFramework.KEY_EVENT_ENDED_AT] = datetime.now(tz=timezone.utc)
                hook[TestFramework.KEY_CUSTOM_TAGS] = CustomTagManager.get_test_level_custom_metadata()
                self.bstack111ll11lll1_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll111111_opy_, [])
                self.send_log_created_event(instance, logs)
                hooks_finished[key].append(hook)
                updates[PytestBDDFramework.KEY_HOOK_LAST_FINISHED] = key
        TestFramework.set_state_entries(instance, updates)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤ᯵") + str(hooks_finished) + bstack1l1llll_opy_ (u"ࠦࠧ᯶"))
    def __111l1ll1l1l_opy_(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.extract_keys(args[0], [bstack1l1llll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦ᯷"), bstack1l1llll_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢ᯸"), bstack1l1llll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢ᯹"), bstack1l1llll_opy_ (u"ࠣ࡫ࡧࡷࠧ᯺"), bstack1l1llll_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦ᯻"), bstack1l1llll_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥ᯼")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1llll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ᯽")) else fixturedef.get(bstack1l1llll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦ᯾"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1llll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦ᯿")) else None
        node = request.node if hasattr(request, bstack1l1llll_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᰀ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1llll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᰁ")) else None
        baseid = fixturedef.get(bstack1l1llll_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᰂ"), None) or bstack1l1llll_opy_ (u"ࠥࠦᰃ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1llll_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᰄ")):
            target = PytestBDDFramework.__111l1llll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1llll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᰅ")) else None
            if target and not TestFramework.get_tracked_instance(target):
                self.__111ll1l111l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࢁࠥࡴ࡯ࡥࡧࡀࡿࢂࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠦᰆ").format(target, fixturename, node, test_framework_state, test_hook_state))
        if not fixturedef or not scope or not target:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࢂࠨᰇ").format(test_framework_state, test_hook_state, fixturedef, scope, target))
            return None
        instance = TestFramework.get_tracked_instance(target)
        if not instance:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡷ࡭ࡧࡲࡦࡦ࠰ࡷࡨࡵࡰࡦࠢࡩ࡭ࡽࡺࡵࡳࡧࠣࡩࡻ࡫࡮ࡵࠢࠫࡲࡴࠦࡰࡦࡴ࠰ࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠬࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࢀࠦᰈ").format(test_framework_state, test_hook_state, fixturename, scope, baseid, target))
            return None
        bstack111ll11ll1l_opy_ = TestFramework.get_state(instance, PytestBDDFramework.bstack11l1ll1l1ll_opy_, {})
        if os.getenv(bstack1l1llll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᰉ"), bstack1l1llll_opy_ (u"ࠥ࠵ࠧᰊ")) == bstack1l1llll_opy_ (u"ࠦ࠶ࠨᰋ"):
            bstack111l1lll11l_opy_ = bstack1l1llll_opy_ (u"ࠧࡀࠢᰌ").join((scope, fixturename))
            bstack111l1ll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1lll1l1_opy_ = {
                bstack1l1llll_opy_ (u"ࠨ࡫ࡦࡻࠥᰍ"): bstack111l1lll11l_opy_,
                bstack1l1llll_opy_ (u"ࠢࡵࡣࡪࡷࠧᰎ"): PytestBDDFramework.__111l1ll1ll1_opy_(request.node, scenario),
                bstack1l1llll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᰏ"): fixturedef,
                bstack1l1llll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᰐ"): scope,
                bstack1l1llll_opy_ (u"ࠥࡸࡾࡶࡥࠣᰑ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1l1llll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᰒ"), None)):
                    bstack111l1lll1l1_opy_[bstack1l1llll_opy_ (u"ࠧࡺࡹࡱࡧࠥᰓ")] = TestFramework.object_fqcn(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111l1lll1l1_opy_[bstack1l1llll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᰔ")] = uuid4().__str__()
                bstack111l1lll1l1_opy_[PytestBDDFramework.KEY_EVENT_STARTED_AT] = bstack111l1ll111l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1lll1l1_opy_[PytestBDDFramework.KEY_EVENT_ENDED_AT] = bstack111l1ll111l_opy_
            if bstack111l1lll11l_opy_ in bstack111ll11ll1l_opy_:
                bstack111ll11ll1l_opy_[bstack111l1lll11l_opy_].update(bstack111l1lll1l1_opy_)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᰕ") + str(bstack111ll11ll1l_opy_[bstack111l1lll11l_opy_]) + bstack1l1llll_opy_ (u"ࠣࠤᰖ"))
            else:
                bstack111ll11ll1l_opy_[bstack111l1lll11l_opy_] = bstack111l1lll1l1_opy_
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᰗ") + str(len(bstack111ll11ll1l_opy_)) + bstack1l1llll_opy_ (u"ࠥࠦᰘ"))
        TestFramework.set_state(instance, PytestBDDFramework.bstack11l1ll1l1ll_opy_, bstack111ll11ll1l_opy_)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᰙ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠧࠨᰚ"))
        return instance
    def __111ll1l111l_opy_(
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
            PytestBDDFramework.bstack11l1ll1l1ll_opy_: {},
            PytestBDDFramework.KEY_HOOKS_FINISHED: {},
            PytestBDDFramework.KEY_HOOKS_STARTED: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.set_state(ob, TestFramework.KEY_TEST_LOCATION, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.set_state(ob, TestFramework.KEY_PLATFORM_INDEX, context.platform_index)
        TestFramework.instances[ctx.id] = ob
        self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᰛ") + str(TestFramework.instances.keys()) + bstack1l1llll_opy_ (u"ࠢࠣᰜ"))
        return ob
    @staticmethod
    def __111l1l1ll1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1llll_opy_ (u"ࠨ࡫ࡧࠫᰝ"): id(step),
                bstack1l1llll_opy_ (u"ࠩࡷࡩࡽࡺࠧᰞ"): step.name,
                bstack1l1llll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᰟ"): step.keyword,
            })
        meta = {
            bstack1l1llll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᰠ"): {
                bstack1l1llll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᰡ"): feature.name,
                bstack1l1llll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᰢ"): feature.filename,
                bstack1l1llll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᰣ"): feature.description
            },
            bstack1l1llll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᰤ"): {
                bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᰥ"): scenario.name
            },
            bstack1l1llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᰦ"): steps,
            bstack1l1llll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᰧ"): PytestBDDFramework.__111l1l1l11l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.KEY_TEST_META: meta
            }
        )
    def bstack111ll11lll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᰨ")
        global _processed_attachments
        platform_index = os.environ[bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᰩ")]
        attachment_dir = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), bstack111l1lllll1_opy_)
        if not os.path.exists(attachment_dir) or not os.path.isdir(attachment_dir):
            return
        logs = hook.get(bstack1l1llll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᰪ"), [])
        with os.scandir(attachment_dir) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _processed_attachments:
                    self.logger.info(bstack1l1llll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᰫ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1llll_opy_ (u"ࠤࠥᰬ")
                    log_entry = LogEntry(
                        kind=bstack1l1llll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᰭ"),
                        message=bstack1l1llll_opy_ (u"ࠦࠧᰮ"),
                        level=bstack1l1llll_opy_ (u"ࠧࠨᰯ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        fileSize=entry.stat().st_size,
                        attachmentType=bstack1l1llll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᰰ"),
                        filePath=os.path.abspath(entry.path),
                        hook_run_uuid=hook.get(TestFramework.KEY_HOOK_ID)
                    )
                    logs.append(log_entry)
                    _processed_attachments.add(abs_path)
        platform_index = os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᰱ")]
        bstack111l1lll1ll_opy_ = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), bstack111l1lllll1_opy_, bstack111l1l1l1l1_opy_)
        if not os.path.exists(bstack111l1lll1ll_opy_) or not os.path.isdir(bstack111l1lll1ll_opy_):
            self.logger.info(bstack1l1llll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᰲ").format(bstack111l1lll1ll_opy_))
        else:
            self.logger.info(bstack1l1llll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᰳ").format(bstack111l1lll1ll_opy_))
            with os.scandir(bstack111l1lll1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _processed_attachments:
                        self.logger.info(bstack1l1llll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᰴ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1llll_opy_ (u"ࠦࠧᰵ")
                        log_entry = LogEntry(
                            kind=bstack1l1llll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᰶ"),
                            message=bstack1l1llll_opy_ (u"ࠨ᰷ࠢ"),
                            level=bstack1l1llll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ᰸"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            fileSize=entry.stat().st_size,
                            attachmentType=bstack1l1llll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣ᰹"),
                            filePath=os.path.abspath(entry.path),
                            build_run_uuid=hook.get(TestFramework.KEY_HOOK_ID)
                        )
                        logs.append(log_entry)
                        _processed_attachments.add(abs_path)
        hook[bstack1l1llll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢ᰺")] = logs
    def send_log_created_event(
        self,
        test_instance: TestFrameworkTest,
        entries: List[LogEntry],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢ᰻"))
        req.platform_index = TestFramework.get_state(test_instance, TestFramework.KEY_PLATFORM_INDEX)
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ᰼").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(test_instance.context.hash)
        req.execution_context.thread_id = str(test_instance.context.thread_id)
        req.execution_context.process_id = str(test_instance.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_NAME)
            log_entry.test_framework_version = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION)
            log_entry.uuid = entry.hook_run_uuid if entry.hook_run_uuid else TestFramework.get_state(test_instance, TestFramework.KEY_TEST_UUID)
            log_entry.test_framework_state = test_instance.state.name
            log_entry.message = entry.message.encode(bstack1l1llll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ᰽"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1llll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᰾"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.fileSize
                log_entry.file_path = entry.filePath
        def make_grpc_request():
            time_start = datetime.now()
            try:
                self.cli_service.LogCreatedEvent(req)
                test_instance.add_benchmark(bstack1l1llll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ᰿"), datetime.now() - time_start)
            except grpc.RpcError as e:
                self.log_error(bstack1l1llll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ᱀").format(str(e)))
                traceback.print_exc()
        self.async_dispatcher.enqueue(make_grpc_request)
    def __load_custom_tags(self, instance) -> None:
        bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᱁")
        updates = {bstack1l1llll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ᱂"): CustomTagManager.get_test_level_custom_metadata()}
        TestFramework.set_state_entries(instance, updates)
        CustomTagManager.reset_test_level_custom_metadata()
    @staticmethod
    def __111l1l1llll_opy_(instance, args):
        request, bstack111l1ll1111_opy_ = args
        bstack111ll111l1l_opy_ = id(bstack111l1ll1111_opy_)
        test_meta = instance.data[TestFramework.KEY_TEST_META]
        step = next(filter(lambda st: st[bstack1l1llll_opy_ (u"ࠫ࡮ࡪࠧ᱃")] == bstack111ll111l1l_opy_, test_meta[bstack1l1llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᱄")]), None)
        step.update({
            bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᱅"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(test_meta[bstack1l1llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᱆")]) if st[bstack1l1llll_opy_ (u"ࠨ࡫ࡧࠫ᱇")] == step[bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬ᱈")]), None)
        if index is not None:
            test_meta[bstack1l1llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᱉")][index] = step
        instance.data[TestFramework.KEY_TEST_META] = test_meta
    @staticmethod
    def __111ll11llll_opy_(instance, args):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᱊")
        bstack1ll1ll1ll_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111l1ll1111_opy_ = args[1]
        bstack111ll111l1l_opy_ = id(bstack111l1ll1111_opy_)
        test_meta = instance.data[TestFramework.KEY_TEST_META]
        step = None
        if bstack111ll111l1l_opy_ is not None and test_meta.get(bstack1l1llll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᱋")):
            step = next(filter(lambda st: st[bstack1l1llll_opy_ (u"࠭ࡩࡥࠩ᱌")] == bstack111ll111l1l_opy_, test_meta[bstack1l1llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᱍ")]), None)
            step.update({
                bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᱎ"): bstack1ll1ll1ll_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᱏ"): bstack1l1llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᱐"),
                bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᱑"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᱒"): bstack1l1llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᱓"),
                })
        index = next((i for i, st in enumerate(test_meta[bstack1l1llll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᱔")]) if st[bstack1l1llll_opy_ (u"ࠨ࡫ࡧࠫ᱕")] == step[bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬ᱖")]), None)
        if index is not None:
            test_meta[bstack1l1llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᱗")][index] = step
        instance.data[TestFramework.KEY_TEST_META] = test_meta
    @staticmethod
    def __111l1l1l11l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1llll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭᱘")):
                examples = list(node.callspec.params[bstack1l1llll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫ᱙")].values())
            return examples
        except Exception as e:
            from bstack_utils import logger_utils
            logger_utils.get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠨࡢࡥࡦࠣࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠥࡶࡡࡳࡵࡨࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧᱚ").format(type(e).__name__, e), exc_info=True)
            return []
    def get_log_entries(self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]):
        bstack111ll111ll1_opy_ = (
            PytestBDDFramework.KEY_HOOK_LAST_STARTED
            if hook_info[1] == TestHookState.PRE
            else PytestBDDFramework.KEY_HOOK_LAST_FINISHED
        )
        hook = PytestBDDFramework.bstack111l1ll11l1_opy_(instance, bstack111ll111ll1_opy_)
        entries = hook.get(TestFramework.KEY_HOOK_LOGS, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []))
        return entries
    def clear_logs(self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]):
        bstack111ll111ll1_opy_ = (
            PytestBDDFramework.KEY_HOOK_LAST_STARTED
            if hook_info[1] == TestHookState.PRE
            else PytestBDDFramework.KEY_HOOK_LAST_FINISHED
        )
        PytestBDDFramework.bstack111l1lll111_opy_(instance, bstack111ll111ll1_opy_)
        TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []).clear()
    @staticmethod
    def bstack111l1ll11l1_opy_(instance: TestFrameworkTest, bstack111ll111ll1_opy_: str):
        bstack111ll1111ll_opy_ = (
            PytestBDDFramework.KEY_HOOKS_FINISHED
            if bstack111ll111ll1_opy_ == PytestBDDFramework.KEY_HOOK_LAST_FINISHED
            else PytestBDDFramework.KEY_HOOKS_STARTED
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
        hook = PytestBDDFramework.bstack111l1ll11l1_opy_(instance, bstack111ll111ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.KEY_HOOK_LOGS, []).clear()
    @staticmethod
    def __111ll111lll_opy_(instance: TestFrameworkTest, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1llll_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᱛ"), None)):
            return
        if os.getenv(bstack1l1llll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᱜ"), bstack1l1llll_opy_ (u"ࠤ࠴ࠦᱝ")) != bstack1l1llll_opy_ (u"ࠥ࠵ࠧᱞ"):
            PytestBDDFramework.logger.warning(bstack1l1llll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᱟ"))
            return
        bstack111l1ll1lll_opy_ = {
            bstack1l1llll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᱠ"): (PytestBDDFramework.KEY_HOOK_LAST_STARTED, PytestBDDFramework.KEY_HOOKS_STARTED),
            bstack1l1llll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᱡ"): (PytestBDDFramework.KEY_HOOK_LAST_FINISHED, PytestBDDFramework.KEY_HOOKS_FINISHED),
        }
        for when in (bstack1l1llll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᱢ"), bstack1l1llll_opy_ (u"ࠣࡥࡤࡰࡱࠨᱣ"), bstack1l1llll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᱤ")):
            bstack111l1llll11_opy_ = args[1].get_records(when)
            if not bstack111l1llll11_opy_:
                continue
            records = [
                LogEntry(
                    kind=TestFramework.KIND_LOG,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1llll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᱥ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1llll_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᱦ")) and r.created
                        else None
                    ),
                )
                for r in bstack111l1llll11_opy_
                if isinstance(getattr(r, bstack1l1llll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᱧ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111l1l1lll1_opy_, bstack111ll1111ll_opy_ = bstack111l1ll1lll_opy_.get(when, (None, None))
            bstack111ll11l1ll_opy_ = TestFramework.get_state(instance, bstack111l1l1lll1_opy_, None) if bstack111l1l1lll1_opy_ else None
            bstack111l1llllll_opy_ = TestFramework.get_state(instance, bstack111ll1111ll_opy_, None) if bstack111ll11l1ll_opy_ else None
            if isinstance(bstack111l1llllll_opy_, dict) and len(bstack111l1llllll_opy_.get(bstack111ll11l1ll_opy_, [])) > 0:
                hook = bstack111l1llllll_opy_[bstack111ll11l1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.KEY_HOOK_LOGS in hook:
                    hook[TestFramework.KEY_HOOK_LOGS].extend(records)
                    continue
            logs = TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, [])
            logs.extend(records)
    @staticmethod
    def __111ll1l1111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__111ll1111l1_opy_(request.node, scenario)
        bstack111ll11l111_opy_ = feature.filename
        if not test_id or not test_name or not bstack111ll11l111_opy_:
            return None
        code = None
        return {
            TestFramework.KEY_TEST_UUID: uuid4().__str__(),
            TestFramework.KEY_TEST_ID: test_id,
            TestFramework.KEY_TEST_NAME: test_name,
            TestFramework.KEY_TEST_RERUN_NAME: test_id,
            TestFramework.KEY_TEST_FILE_PATH: bstack111ll11l111_opy_,
            TestFramework.KEY_TEST_TAGS: PytestBDDFramework.__111l1ll1ll1_opy_(feature, scenario),
            TestFramework.bstack111l1l1l1ll_opy_: code,
            TestFramework.KEY_TEST_RESULT: TestFramework.DEFAULT_TEST_RESULT,
            TestFramework.KEY_AUTOMATE_SESSION_NAME: test_name
        }
    @staticmethod
    def __111ll1111l1_opy_(node, scenario):
        if hasattr(node, bstack1l1llll_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᱨ")):
            parts = node.nodeid.rsplit(bstack1l1llll_opy_ (u"ࠢ࡜ࠤᱩ"))
            params = parts[-1]
            return bstack1l1llll_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᱪ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __111l1ll1ll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1llll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᱫ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1llll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᱬ")) else [])
    @staticmethod
    def __111l1llll1l_opy_(location):
        return bstack1l1llll_opy_ (u"ࠦ࠿ࡀࠢᱭ").join(filter(lambda x: isinstance(x, str), location))