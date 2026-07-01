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
UPLOADED_ATTACHMENTS_PREFIX = bstack1l1llll_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᱮ")
bstack111l1l1l111_opy_ = bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᱯ")
bstack111l1l11ll1_opy_ = bstack1l1llll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᱰ")
bstack111l1l111l1_opy_ = bstack1l1llll_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᱱ")
bstack111l1l111ll_opy_ = bstack1l1llll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᱲ")
_processed_attachments = set()
class bstack1l1111ll11l_opy_(TestFramework):
    bstack11l1ll1l1ll_opy_ = bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᱳ")
    KEY_HOOKS_STARTED = bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᱴ")
    KEY_HOOKS_FINISHED = bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᱵ")
    KEY_HOOK_LAST_STARTED = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᱶ")
    KEY_HOOK_LAST_FINISHED = bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᱷ")
    bstack111l1l1ll11_opy_: bool
    async_dispatcher: AsyncDispatcher  = None
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
        test_frameworks: List[str]=[bstack1l1llll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᱸ")],
        async_dispatcher: AsyncDispatcher=None,
        cli_service=None
    ):
        super().__init__(test_frameworks, test_framework_versions, async_dispatcher)
        self.bstack111l1l1ll11_opy_ = any(bstack1l1llll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᱹ") in item.lower() for item in test_frameworks)
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
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1111ll11l_opy_.hook_events:
            bstack111ll11l1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᱺ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠦࠧᱻ"))
            return
        if not self.bstack111l1l1ll11_opy_:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᱼ") + str(str(self.test_frameworks)) + bstack1l1llll_opy_ (u"ࠨࠢᱽ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ᱾") + str(kwargs) + bstack1l1llll_opy_ (u"ࠣࠤ᱿"))
            return
        instance = self.__resolve_instance(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᲀ") + str(args) + bstack1l1llll_opy_ (u"ࠥࠦᲁ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1111ll11l_opy_.hook_events:
                random_label = bstack1l1llll_opy_ (u"ࠦࠧᲂ")
                name = bstack1l1llll_opy_ (u"ࠧࠨᲃ")
                if (test_hook_state == TestHookState.PRE):
                    random_label = PerformanceTester.mark_start(EVENTS.bstack111l1l11l11_opy_.value)
                    name = str(EVENTS.bstack111l1l11l11_opy_.name)+bstack1l1llll_opy_ (u"ࠨ࠺ࠣᲄ")+str(test_framework_state.name)
                else:
                    random_label = PerformanceTester.mark_start(EVENTS.bstack111l1l11l1l_opy_.value)
                    name = str(EVENTS.bstack111l1l11l1l_opy_.name)+bstack1l1llll_opy_ (u"ࠢ࠻ࠤᲅ")+str(test_framework_state.name)
                TestFramework.bstack111l1ll11ll_opy_(instance, name, random_label)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᲆ").format(e))
        try:
            if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ID) and test_hook_state == TestHookState.PRE:
                test = bstack1l1111ll11l_opy_.__111ll1l1111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᲇ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠥࠦᲈ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.has_state(instance, TestFramework.KEY_TEST_STARTED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_STARTED_AT, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᲉ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠧࠨᲊ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.has_state(instance, TestFramework.KEY_TEST_ENDED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_ENDED_AT, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᲋") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠢࠣ᲌"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1111ll11l_opy_.__111ll111lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__load_test_result(instance, *args)
                self.__load_custom_tags(instance)
            elif test_framework_state in bstack1l1111ll11l_opy_.hook_events:
                self.__track_hook_event(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᲍") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠤࠥ᲎"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.run_hooks(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1111ll11l_opy_.hook_events:
                random_label = bstack1l1llll_opy_ (u"ࠥࠦ᲏")
                name = bstack1l1llll_opy_ (u"ࠦࠧᲐ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111l1l11l11_opy_.name)+bstack1l1llll_opy_ (u"ࠧࡀࠢᲑ")+str(test_framework_state.name)
                    random_label = TestFramework.bstack111ll111l11_opy_(instance, name)
                    PerformanceTester.end(EVENTS.bstack111l1l11l11_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᲒ"), random_label+bstack1l1llll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᲓ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111l1l11l1l_opy_.name)+bstack1l1llll_opy_ (u"ࠣ࠼ࠥᲔ")+str(test_framework_state.name)
                    random_label = TestFramework.bstack111ll111l11_opy_(instance, name)
                    PerformanceTester.end(EVENTS.bstack111l1l11l1l_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᲕ"), random_label+bstack1l1llll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᲖ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᲗ").format(e))
    def is_pytest_framework(self):
        return self.bstack111l1l1ll11_opy_
    def is_robot_framework(self):
        return False
    def is_behave_framework(self):
        return False
    def __111l1ll1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1llll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᲘ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.extract_keys(rep, [bstack1l1llll_opy_ (u"ࠨࡷࡩࡧࡱࠦᲙ"), bstack1l1llll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᲚ"), bstack1l1llll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᲛ"), bstack1l1llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᲜ"), bstack1l1llll_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᲝ"), bstack1l1llll_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᲞ")])
        return None
    def __load_test_result(self, instance: TestFrameworkTest, *args):
        result = self.__111l1ll1l11_opy_(*args)
        if not result:
            return
        failure = None
        failure_type = None
        if result.get(bstack1l1llll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᲟ"), None) == bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᲠ") and len(args) > 1 and getattr(args[1], bstack1l1llll_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᲡ"), None) is not None:
            failure = [{bstack1l1llll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᲢ"): [args[1].excinfo.exconly(), result.get(bstack1l1llll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᲣ"), None)]}]
            failure_type = bstack1l1llll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᲤ") if bstack1l1llll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᲥ") in getattr(args[1].excinfo, bstack1l1llll_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᲦ"), bstack1l1llll_opy_ (u"ࠨࠢᲧ")) else bstack1l1llll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᲨ")
        test_result = result.get(bstack1l1llll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᲩ"), TestFramework.DEFAULT_TEST_RESULT)
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
            target = None # we bstack111ll11ll11_opy_ this to be bstack1l1llll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᲪ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111ll1l111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1llll_opy_ (u"ࠥࡲࡴࡪࡥࠣᲫ"), None), bstack1l1llll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᲬ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᲭ"), None):
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
        hooks_started = TestFramework.get_state(instance, bstack1l1111ll11l_opy_.KEY_HOOKS_STARTED, {})
        if not key in hooks_started:
            hooks_started[key] = []
        hooks_finished = TestFramework.get_state(instance, bstack1l1111ll11l_opy_.KEY_HOOKS_FINISHED, {})
        if not key in hooks_finished:
            hooks_finished[key] = []
        updates = {
            bstack1l1111ll11l_opy_.KEY_HOOKS_STARTED: hooks_started,
            bstack1l1111ll11l_opy_.KEY_HOOKS_FINISHED: hooks_finished,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1l1llll_opy_ (u"ࠨ࡫ࡦࡻࠥᲮ"): key,
                TestFramework.KEY_HOOK_ID: uuid4().__str__(),
                TestFramework.KEY_HOOK_RESULT: TestFramework.DEFAULT_HOOK_RESULT,
                TestFramework.KEY_EVENT_STARTED_AT: datetime.now(tz=timezone.utc),
                TestFramework.KEY_HOOK_LOGS: [],
                TestFramework.KEY_HOOK_NAME: args[1] if len(args) > 1 else bstack1l1llll_opy_ (u"ࠧࠨᲯ"),
                TestFramework.KEY_CUSTOM_TAGS: CustomTagManager.get_test_level_custom_metadata()
            }
            hooks_started[key].append(hook)
            updates[bstack1l1111ll11l_opy_.KEY_HOOK_LAST_STARTED] = key
        elif test_hook_state == TestHookState.POST:
            hooks_list = hooks_started.get(key, [])
            hook = hooks_list.pop() if hooks_list else None
            if hook:
                result = self.__111l1ll1l11_opy_(*args)
                if result:
                    hook_result = result.get(bstack1l1llll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᲰ"), TestFramework.DEFAULT_HOOK_RESULT)
                    if hook_result != TestFramework.DEFAULT_HOOK_RESULT:
                        hook[TestFramework.KEY_HOOK_RESULT] = hook_result
                hook[TestFramework.KEY_EVENT_ENDED_AT] = datetime.now(tz=timezone.utc)
                hook[TestFramework.KEY_CUSTOM_TAGS]= CustomTagManager.get_test_level_custom_metadata()
                self.bstack111ll11lll1_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll111111_opy_, [])
                if logs: self.send_log_created_event(instance, logs)
                hooks_finished[key].append(hook)
                updates[bstack1l1111ll11l_opy_.KEY_HOOK_LAST_FINISHED] = key
        TestFramework.set_state_entries(instance, updates)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᲱ") + str(hooks_finished) + bstack1l1llll_opy_ (u"ࠥࠦᲲ"))
    def __111l1ll1l1l_opy_(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.extract_keys(args[0], [bstack1l1llll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᲳ"), bstack1l1llll_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᲴ"), bstack1l1llll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᲵ"), bstack1l1llll_opy_ (u"ࠢࡪࡦࡶࠦᲶ"), bstack1l1llll_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᲷ"), bstack1l1llll_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᲸ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1llll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᲹ")) else fixturedef.get(bstack1l1llll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᲺ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1llll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥ᲻")) else None
        node = request.node if hasattr(request, bstack1l1llll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᲼")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1llll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᲽ")) else None
        baseid = fixturedef.get(bstack1l1llll_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᲾ"), None) or bstack1l1llll_opy_ (u"ࠤࠥᲿ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1llll_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣ᳀")):
            target = bstack1l1111ll11l_opy_.__111l1llll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1llll_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨ᳁")) else None
            if target and not TestFramework.get_tracked_instance(target):
                self.__111ll1l111l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࢀࠤࡳࡵࡤࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥ᳂").format(target, fixturename, node, test_framework_state, test_hook_state))
        if not fixturedef or not scope or not target:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀࢃࠠࡴࡥࡲࡴࡪࡃࡻࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࢁࠧ᳃").format(test_framework_state, test_hook_state, fixturedef, scope, target))
            return None
        instance = TestFramework.get_tracked_instance(target)
        if not instance:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡶ࡬ࡦࡸࡥࡥ࠯ࡶࡧࡴࡶࡥࠡࡨ࡬ࡼࡹࡻࡲࡦࠢࡨࡺࡪࡴࡴࠡࠪࡱࡳࠥࡶࡥࡳ࠯ࡷࡩࡸࡺࠠࡪࡰࡶࡸࡦࡴࡣࡦࠫࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡿࠥ᳄").format(test_framework_state, test_hook_state, fixturename, scope, baseid, target))
            return None
        bstack111ll11ll1l_opy_ = TestFramework.get_state(instance, bstack1l1111ll11l_opy_.bstack11l1ll1l1ll_opy_, {})
        if os.getenv(bstack1l1llll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤ᳅"), bstack1l1llll_opy_ (u"ࠤ࠴ࠦ᳆")) == bstack1l1llll_opy_ (u"ࠥ࠵ࠧ᳇"):
            bstack111l1lll11l_opy_ = bstack1l1llll_opy_ (u"ࠦ࠿ࠨ᳈").join((scope, fixturename))
            bstack111l1ll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1lll1l1_opy_ = {
                bstack1l1llll_opy_ (u"ࠧࡱࡥࡺࠤ᳉"): bstack111l1lll11l_opy_,
                bstack1l1llll_opy_ (u"ࠨࡴࡢࡩࡶࠦ᳊"): bstack1l1111ll11l_opy_.__111l1ll1ll1_opy_(request.node),
                bstack1l1llll_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣ᳋"): fixturedef,
                bstack1l1llll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᳌"): scope,
                bstack1l1llll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᳍"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1l1llll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ᳎"), None)):
                    bstack111l1lll1l1_opy_[bstack1l1llll_opy_ (u"ࠦࡹࡿࡰࡦࠤ᳏")] = TestFramework.object_fqcn(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111l1lll1l1_opy_[bstack1l1llll_opy_ (u"ࠧࡻࡵࡪࡦࠥ᳐")] = uuid4().__str__()
                bstack111l1lll1l1_opy_[bstack1l1111ll11l_opy_.KEY_EVENT_STARTED_AT] = bstack111l1ll111l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1lll1l1_opy_[bstack1l1111ll11l_opy_.KEY_EVENT_ENDED_AT] = bstack111l1ll111l_opy_
            if bstack111l1lll11l_opy_ in bstack111ll11ll1l_opy_:
                bstack111ll11ll1l_opy_[bstack111l1lll11l_opy_].update(bstack111l1lll1l1_opy_)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢ᳑") + str(bstack111ll11ll1l_opy_[bstack111l1lll11l_opy_]) + bstack1l1llll_opy_ (u"ࠢࠣ᳒"))
            else:
                bstack111ll11ll1l_opy_[bstack111l1lll11l_opy_] = bstack111l1lll1l1_opy_
                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦ᳓") + str(len(bstack111ll11ll1l_opy_)) + bstack1l1llll_opy_ (u"ࠤ᳔ࠥ"))
        TestFramework.set_state(instance, bstack1l1111ll11l_opy_.bstack11l1ll1l1ll_opy_, bstack111ll11ll1l_opy_)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿᳕ࠥ") + str(instance.ref()) + bstack1l1llll_opy_ (u"᳖ࠦࠧ"))
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
            bstack1l1111ll11l_opy_.bstack11l1ll1l1ll_opy_: {},
            bstack1l1111ll11l_opy_.KEY_HOOKS_FINISHED: {},
            bstack1l1111ll11l_opy_.KEY_HOOKS_STARTED: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.set_state(ob, TestFramework.KEY_TEST_LOCATION, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.set_state(ob, TestFramework.KEY_PLATFORM_INDEX, context.platform_index)
        TestFramework.instances[ctx.id] = ob
        self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁ᳗ࠧ") + str(TestFramework.instances.keys()) + bstack1l1llll_opy_ (u"ࠨ᳘ࠢ"))
        return ob
    def get_log_entries(self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]):
        bstack111ll111ll1_opy_ = (
            bstack1l1111ll11l_opy_.KEY_HOOK_LAST_STARTED
            if hook_info[1] == TestHookState.PRE
            else bstack1l1111ll11l_opy_.KEY_HOOK_LAST_FINISHED
        )
        hook = bstack1l1111ll11l_opy_.bstack111l1ll11l1_opy_(instance, bstack111ll111ll1_opy_)
        entries = hook.get(TestFramework.KEY_HOOK_LOGS, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []))
        return entries
    def clear_logs(self, instance: TestFrameworkTest, hook_info: Tuple[TestFrameworkState, TestHookState]):
        bstack111ll111ll1_opy_ = (
            bstack1l1111ll11l_opy_.KEY_HOOK_LAST_STARTED
            if hook_info[1] == TestHookState.PRE
            else bstack1l1111ll11l_opy_.KEY_HOOK_LAST_FINISHED
        )
        bstack1l1111ll11l_opy_.bstack111l1lll111_opy_(instance, bstack111ll111ll1_opy_)
        TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, []).clear()
    def bstack111ll11lll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᳙")
        global _processed_attachments
        platform_index = os.environ[bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᳚")]
        attachment_dir = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), bstack111l1l111l1_opy_)
        if not os.path.exists(attachment_dir) or not os.path.isdir(attachment_dir):
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢ᳛").format(attachment_dir))
            return
        logs = hook.get(bstack1l1llll_opy_ (u"ࠥࡰࡴ࡭ࡳ᳜ࠣ"), [])
        with os.scandir(attachment_dir) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _processed_attachments:
                    self.logger.info(bstack1l1llll_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤ᳝").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1llll_opy_ (u"ࠧࠨ᳞")
                    log_entry = LogEntry(
                        kind=bstack1l1llll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔ᳟ࠣ"),
                        message=bstack1l1llll_opy_ (u"ࠢࠣ᳠"),
                        level=bstack1l1llll_opy_ (u"ࠣࠤ᳡"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        fileSize=entry.stat().st_size,
                        attachmentType=bstack1l1llll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ᳢"),
                        filePath=os.path.abspath(entry.path),
                        hook_run_uuid=hook.get(TestFramework.KEY_HOOK_ID)
                    )
                    logs.append(log_entry)
                    _processed_attachments.add(abs_path)
        platform_index = os.environ[bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ᳣࡚ࠪ")]
        bstack111l1lll1ll_opy_ = os.path.join(BROWSERSTACK_ROOT_DIR, (UPLOADED_ATTACHMENTS_PREFIX + str(platform_index)), bstack111l1l111l1_opy_, bstack111l1l111ll_opy_)
        if not os.path.exists(bstack111l1lll1ll_opy_) or not os.path.isdir(bstack111l1lll1ll_opy_):
            self.logger.info(bstack1l1llll_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨ᳤").format(bstack111l1lll1ll_opy_))
        else:
            self.logger.info(bstack1l1llll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀ᳥ࠦ").format(bstack111l1lll1ll_opy_))
            with os.scandir(bstack111l1lll1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _processed_attachments:
                        self.logger.info(bstack1l1llll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀ᳦ࠦ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1llll_opy_ (u"᳧ࠢࠣ")
                        log_entry = LogEntry(
                            kind=bstack1l1llll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖ᳨ࠥ"),
                            message=bstack1l1llll_opy_ (u"ࠤࠥᳩ"),
                            level=bstack1l1llll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᳪ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            fileSize=entry.stat().st_size,
                            attachmentType=bstack1l1llll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᳫ"),
                            filePath=os.path.abspath(entry.path),
                            build_run_uuid=hook.get(TestFramework.KEY_HOOK_ID)
                        )
                        logs.append(log_entry)
                        _processed_attachments.add(abs_path)
        hook[bstack1l1llll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᳬ")] = logs
    def send_log_created_event(
        self,
        test_instance: TestFrameworkTest,
        entries: List[LogEntry],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆ᳭ࠥ"))
        req.platform_index = TestFramework.get_state(test_instance, TestFramework.KEY_PLATFORM_INDEX)
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᳮ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(test_instance.context.hash)
        req.execution_context.thread_id = str(test_instance.context.thread_id)
        req.execution_context.process_id = str(test_instance.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_NAME)
            log_entry.test_framework_version = TestFramework.get_state(test_instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION)
            log_entry.uuid = entry.hook_run_uuid
            log_entry.test_framework_state = test_instance.state.name
            log_entry.message = entry.message.encode(bstack1l1llll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᳯ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1llll_opy_ (u"ࠤࠥᳰ")
            if entry.kind == bstack1l1llll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᳱ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.fileSize
                log_entry.file_path = entry.filePath
        def make_grpc_request():
            time_start = datetime.now()
            try:
                self.cli_service.LogCreatedEvent(req)
                test_instance.add_benchmark(bstack1l1llll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᳲ"), datetime.now() - time_start)
            except grpc.RpcError as e:
                self.log_error(bstack1l1llll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᳳ").format(str(e)))
                traceback.print_exc()
        self.async_dispatcher.enqueue(make_grpc_request)
    def __load_custom_tags(self, instance) -> None:
        bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᳴")
        updates = {bstack1l1llll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᳵ"): CustomTagManager.get_test_level_custom_metadata()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.set_state_entries(instance, updates)
        CustomTagManager.reset_test_level_custom_metadata()
    @staticmethod
    def bstack111l1ll11l1_opy_(instance: TestFrameworkTest, bstack111ll111ll1_opy_: str):
        bstack111ll1111ll_opy_ = (
            bstack1l1111ll11l_opy_.KEY_HOOKS_FINISHED
            if bstack111ll111ll1_opy_ == bstack1l1111ll11l_opy_.KEY_HOOK_LAST_FINISHED
            else bstack1l1111ll11l_opy_.KEY_HOOKS_STARTED
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
        hook = bstack1l1111ll11l_opy_.bstack111l1ll11l1_opy_(instance, bstack111ll111ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.KEY_HOOK_LOGS, []).clear()
    @staticmethod
    def __111ll111lll_opy_(instance: TestFrameworkTest, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᳶ"), None)):
            return
        if os.getenv(bstack1l1llll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨ᳷"), bstack1l1llll_opy_ (u"ࠥ࠵ࠧ᳸")) != bstack1l1llll_opy_ (u"ࠦ࠶ࠨ᳹"):
            bstack1l1111ll11l_opy_.logger.warning(bstack1l1llll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᳺ"))
            return
        bstack111l1ll1lll_opy_ = {
            bstack1l1llll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ᳻"): (bstack1l1111ll11l_opy_.KEY_HOOK_LAST_STARTED, bstack1l1111ll11l_opy_.KEY_HOOKS_STARTED),
            bstack1l1llll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ᳼"): (bstack1l1111ll11l_opy_.KEY_HOOK_LAST_FINISHED, bstack1l1111ll11l_opy_.KEY_HOOKS_FINISHED),
        }
        for when in (bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ᳽"), bstack1l1llll_opy_ (u"ࠤࡦࡥࡱࡲࠢ᳾"), bstack1l1llll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ᳿")):
            bstack111l1llll11_opy_ = args[1].get_records(when)
            if not bstack111l1llll11_opy_:
                continue
            records = [
                LogEntry(
                    kind=TestFramework.KIND_LOG,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1llll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᴀ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1llll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᴁ")) and r.created
                        else None
                    ),
                )
                for r in bstack111l1llll11_opy_
                if isinstance(getattr(r, bstack1l1llll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᴂ"), None), str) and r.message.strip()
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
    def __111ll1l1111_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1111ll11l_opy_.__111l1llll1l_opy_(test.location) if hasattr(test, bstack1l1llll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᴃ")) else getattr(test, bstack1l1llll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᴄ"), None)
        test_name = test.name if hasattr(test, bstack1l1llll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴅ")) else None
        bstack111ll11l111_opy_ = test.fspath.strpath if hasattr(test, bstack1l1llll_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᴆ")) and test.fspath else None
        if not test_id or not test_name or not bstack111ll11l111_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1llll_opy_ (u"ࠦࡴࡨࡪࠣᴇ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except Exception as e:
                bstack1l1111ll11l_opy_.logger.debug(bstack1l1llll_opy_ (u"ࠧ࡯࡮ࡴࡲࡨࡧࡹ࠴ࡧࡦࡶࡶࡳࡺࡸࡣࡦࠢࡩࡳࡷࠦࡴࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧᴈ").format(type(e).__name__, e), exc_info=True)
        bstack111l1l11lll_opy_ = []
        try:
            bstack111l1l11lll_opy_ = bstack1ll111ll_opy_.bstack1llll1ll1_opy_(test)
        except Exception as e:
            bstack1l1111ll11l_opy_.logger.warning(bstack1l1llll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᴉ"))
            bstack1l1111ll11l_opy_.logger.debug(bstack1l1llll_opy_ (u"ࠢࡨࡧࡷࡣࡸࡩ࡯ࡱࡧࡢࡳ࡫ࡥࡴࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽ࠻ࠢࡾࢁࠧᴊ").format(type(e).__name__, e), exc_info=True)
        return {
            TestFramework.KEY_TEST_UUID: uuid4().__str__(),
            TestFramework.KEY_TEST_ID: test_id,
            TestFramework.KEY_TEST_NAME: test_name,
            TestFramework.KEY_TEST_RERUN_NAME: getattr(test, bstack1l1llll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᴋ"), None),
            TestFramework.KEY_TEST_FILE_PATH: bstack111ll11l111_opy_,
            TestFramework.KEY_TEST_TAGS: bstack1l1111ll11l_opy_.__111l1ll1ll1_opy_(test),
            TestFramework.bstack111l1l1l1ll_opy_: code,
            TestFramework.KEY_TEST_RESULT: TestFramework.DEFAULT_TEST_RESULT,
            TestFramework.KEY_AUTOMATE_SESSION_NAME: test_id,
            TestFramework.KEY_TEST_SCOPES: bstack111l1l11lll_opy_
        }
    @staticmethod
    def __111l1ll1ll1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1llll_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᴌ"), [])
            markers.extend([getattr(m, bstack1l1llll_opy_ (u"ࠥࡲࡦࡳࡥࠣᴍ"), None) for m in own_markers if getattr(m, bstack1l1llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᴎ"), None)])
            current = getattr(current, bstack1l1llll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᴏ"), None)
        return markers
    @staticmethod
    def __111l1llll1l_opy_(location):
        return bstack1l1llll_opy_ (u"ࠨ࠺࠻ࠤᴐ").join(filter(lambda x: isinstance(x, str), location))