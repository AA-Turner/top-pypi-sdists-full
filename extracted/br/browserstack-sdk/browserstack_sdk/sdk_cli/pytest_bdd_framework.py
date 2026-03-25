# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll11l111ll_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack11l111l1l1_opy_ import bstack11l1ll11lll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1llll1lll_opy_,
    TestHookState,
    bstack1ll1ll11ll1_opy_,
    bstack1l1l1l1lll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l111ll1111_opy_
from bstack_utils.bstack11l1l1ll_opy_ import bstack111l1111l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1llllllll_opy_ import bstack1l1ll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l11l1ll_opy_
bstack1l11111l1l1_opy_ = bstack1l111ll1111_opy_()
bstack1l111111ll1_opy_ = bstack1l1_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧញ")
bstack11l1ll1llll_opy_ = bstack1l1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤដ")
bstack11l1llllll1_opy_ = bstack1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨឋ")
bstack11l11ll1lll_opy_ = 1.0
_1l111l11l1l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l1l1l11l1_opy_ = bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣឌ")
    bstack11l1llll1l1_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢឍ")
    bstack11l1ll1l1l1_opy_ = bstack1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤណ")
    bstack11l1ll1ll1l_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨត")
    bstack11l1l11l111_opy_ = bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣថ")
    bstack11l1l1111l1_opy_: bool
    bstack1ll1l11l1l1_opy_: bstack1ll1l11l1ll_opy_  = None
    bstack11l1l1l111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1l1l11ll_opy_: Dict[str, str],
        bstack1l1l11ll11l_opy_: List[str]=[bstack1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥទ")],
        bstack1ll1l11l1l1_opy_: bstack1ll1l11l1ll_opy_ = None,
        bstack1l1ll11l111_opy_=None
    ):
        super().__init__(bstack1l1l11ll11l_opy_, bstack11l1l1l11ll_opy_, bstack1ll1l11l1l1_opy_)
        self.bstack11l1l1111l1_opy_ = any(bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦធ") in item.lower() for item in bstack1l1l11ll11l_opy_)
        self.bstack1l1ll11l111_opy_ = bstack1l1ll11l111_opy_
    def track_event(
        self,
        context: bstack1ll1ll11ll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l1l1l111l_opy_:
            bstack11l1ll11lll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤន") + str(test_hook_state) + bstack1l1_opy_ (u"ࠤࠥប"))
            return
        if not self.bstack11l1l1111l1_opy_:
            self.logger.warning(bstack1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦផ") + str(str(self.bstack1l1l11ll11l_opy_)) + bstack1l1_opy_ (u"ࠦࠧព"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢភ") + str(kwargs) + bstack1l1_opy_ (u"ࠨࠢម"))
            return
        instance = self.__11l1lll111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨយ") + str(args) + bstack1l1_opy_ (u"ࠣࠤរ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1l1l111l_opy_ and test_hook_state == TestHookState.PRE:
                bstack111l1l111_opy_ = bstack111l1111l_opy_.bstack1ll1l1l1l_opy_(EVENTS.bstack1l1l11l1_opy_.value)
                name = str(EVENTS.bstack1l1l11l1_opy_.name)+bstack1l1_opy_ (u"ࠤ࠽ࠦល")+str(test_framework_state.name)
                TestFramework.bstack11l1l1lll1l_opy_(instance, name, bstack111l1l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢវ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack11lll11ll1l_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11l11ll11l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦឝ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠧࠨឞ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack1l1111l1lll_opy_):
                    TestFramework.bstack1ll1l11lll_opy_(instance, TestFramework.bstack1l1111l1lll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1llll1ll_opy_(instance, args)
                    self.logger.debug(bstack1l1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦស") + str(test_hook_state) + bstack1l1_opy_ (u"ࠢࠣហ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack11llllll11l_opy_):
                    TestFramework.bstack1ll1l11lll_opy_(instance, TestFramework.bstack11llllll11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦឡ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠤࠥអ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l1l1l1ll1_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1l11l1l1_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1ll11l11_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l11ll1l_opy_(instance, *args)
                self.__11l1l1l1111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1l1l111l_opy_:
                self.__11l1ll1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦឣ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠦࠧឤ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll11l1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1l1l111l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1l1l11l1_opy_.name)+bstack1l1_opy_ (u"ࠧࡀࠢឥ")+str(test_framework_state.name)
                bstack111l1l111_opy_ = TestFramework.bstack11l1l1111ll_opy_(instance, name)
                bstack111l1111l_opy_.end(EVENTS.bstack1l1l11l1_opy_.value, bstack111l1l111_opy_+bstack1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨឦ"), bstack111l1l111_opy_+bstack1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧឧ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣឨ").format(e))
    def bstack1l1111ll11l_opy_(self):
        return self.bstack11l1l1111l1_opy_
    def bstack1l1111l1l1l_opy_(self):
        return False
    def __11l1l11lll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨឩ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1111lll11_opy_(rep, [bstack1l1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣឪ"), bstack1l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧឫ"), bstack1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧឬ"), bstack1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨឭ"), bstack1l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣឮ"), bstack1l1_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢឯ")])
        return None
    def __11l1l11ll1l_opy_(self, instance: bstack1l1llll1lll_opy_, *args):
        result = self.__11l1l11lll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1llll1ll_opy_ = None
        if result.get(bstack1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥឰ"), None) == bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥឱ") and len(args) > 1 and getattr(args[1], bstack1l1_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧឲ"), None) is not None:
            failure = [{bstack1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨឳ"): [args[1].excinfo.exconly(), result.get(bstack1l1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧ឴"), None)]}]
            bstack1ll1llll1ll_opy_ = bstack1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ឵") if bstack1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦា") in getattr(args[1].excinfo, bstack1l1_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦិ"), bstack1l1_opy_ (u"ࠥࠦី")) else bstack1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧឹ")
        bstack11l11ll1l1l_opy_ = result.get(bstack1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨឺ"), TestFramework.bstack11l1l1lllll_opy_)
        if bstack11l11ll1l1l_opy_ != TestFramework.bstack11l1l1lllll_opy_:
            TestFramework.bstack1ll1l11lll_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l1ll111_opy_(instance, {
            TestFramework.bstack11lll1l11l1_opy_: failure,
            TestFramework.bstack11l11lll11l_opy_: bstack1ll1llll1ll_opy_,
            TestFramework.bstack11ll1lllll1_opy_: bstack11l11ll1l1l_opy_,
        })
    def __11l1lll111l_opy_(
        self,
        context: bstack1ll1ll11ll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l11lllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111lll111_opy_ bstack11l1l1ll1ll_opy_ this to be bstack1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨុ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l1lll1ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧូ"), None), bstack1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣួ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢើ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥឿ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll11l1l11l_opy_(target) if target else None
        return instance
    def __11l1ll1l1ll_opy_(
        self,
        instance: bstack1l1llll1lll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l11lll1l1_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, PytestBDDFramework.bstack11l1llll1l1_opy_, {})
        if not key in bstack11l11lll1l1_opy_:
            bstack11l11lll1l1_opy_[key] = []
        bstack11l1ll1l111_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, PytestBDDFramework.bstack11l1ll1l1l1_opy_, {})
        if not key in bstack11l1ll1l111_opy_:
            bstack11l1ll1l111_opy_[key] = []
        bstack11l1l1llll1_opy_ = {
            PytestBDDFramework.bstack11l1llll1l1_opy_: bstack11l11lll1l1_opy_,
            PytestBDDFramework.bstack11l1ll1l1l1_opy_: bstack11l1ll1l111_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1_opy_ (u"ࠦࡰ࡫ࡹࠣៀ"): key,
                TestFramework.bstack11l11ll1ll1_opy_: uuid4().__str__(),
                TestFramework.bstack11l1l111ll1_opy_: TestFramework.bstack11l1ll1lll1_opy_,
                TestFramework.bstack11l1ll1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1lll11ll_opy_: [],
                TestFramework.bstack11l1lll11l1_opy_: hook_name,
                TestFramework.bstack11l1l11111l_opy_: bstack1l1ll1ll1ll_opy_.bstack11l1ll1111l_opy_()
            }
            bstack11l11lll1l1_opy_[key].append(hook)
            bstack11l1l1llll1_opy_[PytestBDDFramework.bstack11l1ll1ll1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1lll1lll_opy_ = bstack11l11lll1l1_opy_.get(key, [])
            hook = bstack11l1lll1lll_opy_.pop() if bstack11l1lll1lll_opy_ else None
            if hook:
                result = self.__11l1l11lll1_opy_(*args)
                if result:
                    bstack11l11llll1l_opy_ = result.get(bstack1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨេ"), TestFramework.bstack11l1ll1lll1_opy_)
                    if bstack11l11llll1l_opy_ != TestFramework.bstack11l1ll1lll1_opy_:
                        hook[TestFramework.bstack11l1l111ll1_opy_] = bstack11l11llll1l_opy_
                hook[TestFramework.bstack11l11ll1l11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l11111l_opy_] = bstack1l1ll1ll1ll_opy_.bstack11l1ll1111l_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l11lll1ll_opy_, [])
                self.bstack11lllllll11_opy_(instance, logs)
                bstack11l1ll1l111_opy_[key].append(hook)
                bstack11l1l1llll1_opy_[PytestBDDFramework.bstack11l1l11l111_opy_] = key
        TestFramework.bstack11l1l1ll111_opy_(instance, bstack11l1l1llll1_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧែ") + str(bstack11l1ll1l111_opy_) + bstack1l1_opy_ (u"ࠢࠣៃ"))
    def __11l11lllll1_opy_(
        self,
        context: bstack1ll1ll11ll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1111lll11_opy_(args[0], [bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢោ"), bstack1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥៅ"), bstack1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥំ"), bstack1l1_opy_ (u"ࠦ࡮ࡪࡳࠣះ"), bstack1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢៈ"), bstack1l1_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨ៉")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ៊")) else fixturedef.get(bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ់"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢ៌")) else None
        node = request.node if hasattr(request, bstack1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣ៍")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ៎")) else None
        baseid = fixturedef.get(bstack1l1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧ៏"), None) or bstack1l1_opy_ (u"ࠨࠢ័")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧ៑")):
            target = PytestBDDFramework.__11l1l1l1lll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰ្ࠥ")) else None
            if target and not TestFramework.bstack1ll11l1l11l_opy_(target):
                self.__11l1lll1ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ៓") + str(test_hook_state) + bstack1l1_opy_ (u"ࠥࠦ។"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤ៕") + str(target) + bstack1l1_opy_ (u"ࠧࠨ៖"))
            return None
        instance = TestFramework.bstack1ll11l1l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣៗ") + str(target) + bstack1l1_opy_ (u"ࠢࠣ៘"))
            return None
        bstack11l1llll11l_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, PytestBDDFramework.bstack11l1l1l11l1_opy_, {})
        if os.getenv(bstack1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤ៙"), bstack1l1_opy_ (u"ࠤ࠴ࠦ៚")) == bstack1l1_opy_ (u"ࠥ࠵ࠧ៛"):
            bstack11l1l111l11_opy_ = bstack1l1_opy_ (u"ࠦ࠿ࠨៜ").join((scope, fixturename))
            bstack11l1l1l1l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11ll11ll_opy_ = {
                bstack1l1_opy_ (u"ࠧࡱࡥࡺࠤ៝"): bstack11l1l111l11_opy_,
                bstack1l1_opy_ (u"ࠨࡴࡢࡩࡶࠦ៞"): PytestBDDFramework.__11l1ll1l11l_opy_(request.node, scenario),
                bstack1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣ៟"): fixturedef,
                bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ០"): scope,
                bstack1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ១"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ២"), None)):
                    bstack11l11ll11ll_opy_[bstack1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤ៣")] = TestFramework.bstack1l11111l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l11ll11ll_opy_[bstack1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥ៤")] = uuid4().__str__()
                bstack11l11ll11ll_opy_[PytestBDDFramework.bstack11l1ll1ll11_opy_] = bstack11l1l1l1l1l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11ll11ll_opy_[PytestBDDFramework.bstack11l11ll1l11_opy_] = bstack11l1l1l1l1l_opy_
            if bstack11l1l111l11_opy_ in bstack11l1llll11l_opy_:
                bstack11l1llll11l_opy_[bstack11l1l111l11_opy_].update(bstack11l11ll11ll_opy_)
                self.logger.debug(bstack1l1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢ៥") + str(bstack11l1llll11l_opy_[bstack11l1l111l11_opy_]) + bstack1l1_opy_ (u"ࠢࠣ៦"))
            else:
                bstack11l1llll11l_opy_[bstack11l1l111l11_opy_] = bstack11l11ll11ll_opy_
                self.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦ៧") + str(len(bstack11l1llll11l_opy_)) + bstack1l1_opy_ (u"ࠤࠥ៨"))
        TestFramework.bstack1ll1l11lll_opy_(instance, PytestBDDFramework.bstack11l1l1l11l1_opy_, bstack11l1llll11l_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ៩") + str(instance.ref()) + bstack1l1_opy_ (u"ࠦࠧ៪"))
        return instance
    def __11l1lll1ll1_opy_(
        self,
        context: bstack1ll1ll11ll1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11l11l11_opy_.create_context(target)
        ob = bstack1l1llll1lll_opy_(ctx, self.bstack1l1l11ll11l_opy_, self.bstack11l1l1l11ll_opy_, test_framework_state)
        TestFramework.bstack11l1l1ll111_opy_(ob, {
            TestFramework.bstack1l11lll1l11_opy_: context.test_framework_name,
            TestFramework.bstack1l111l111l1_opy_: context.test_framework_version,
            TestFramework.bstack11l1ll11ll1_opy_: [],
            PytestBDDFramework.bstack11l1l1l11l1_opy_: {},
            PytestBDDFramework.bstack11l1ll1l1l1_opy_: {},
            PytestBDDFramework.bstack11l1llll1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1l11lll_opy_(ob, TestFramework.bstack11l1lll1l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1l11lll_opy_(ob, TestFramework.bstack1l1l1111l1l_opy_, context.platform_index)
        TestFramework.bstack1l11l111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧ៫") + str(TestFramework.bstack1l11l111l_opy_.keys()) + bstack1l1_opy_ (u"ࠨࠢ៬"))
        return ob
    @staticmethod
    def __11l1llll1ll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1_opy_ (u"ࠧࡪࡦࠪ៭"): id(step),
                bstack1l1_opy_ (u"ࠨࡶࡨࡼࡹ࠭៮"): step.name,
                bstack1l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ៯"): step.keyword,
            })
        meta = {
            bstack1l1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫ៰"): {
                bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ៱"): feature.name,
                bstack1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ៲"): feature.filename,
                bstack1l1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ៳"): feature.description
            },
            bstack1l1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ៴"): {
                bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭៵"): scenario.name
            },
            bstack1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ៶"): steps,
            bstack1l1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬ៷"): PytestBDDFramework.__11l1lllll1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l1l1lll11_opy_: meta
            }
        )
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ៸")
        global _1l111l11l1l_opy_
        platform_index = os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ៹")]
        bstack1l111ll1ll1_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack1l111111ll1_opy_ + str(platform_index)), bstack11l1ll1llll_opy_)
        if not os.path.exists(bstack1l111ll1ll1_opy_) or not os.path.isdir(bstack1l111ll1ll1_opy_):
            return
        logs = hook.get(bstack1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦ៺"), [])
        with os.scandir(bstack1l111ll1ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111l11l1l_opy_:
                    self.logger.info(bstack1l1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧ៻").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1_opy_ (u"ࠣࠤ៼")
                    log_entry = bstack1l1l1l1lll1_opy_(
                        kind=bstack1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ៽"),
                        message=bstack1l1_opy_ (u"ࠥࠦ៾"),
                        level=bstack1l1_opy_ (u"ࠦࠧ៿"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11lllllllll_opy_=entry.stat().st_size,
                        bstack1l111l1ll11_opy_=bstack1l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧ᠀"),
                        bstack1llllll1_opy_=os.path.abspath(entry.path),
                        bstack11l1ll11111_opy_=hook.get(TestFramework.bstack11l11ll1ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l111l11l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᠁")]
        bstack11l1llll111_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack1l111111ll1_opy_ + str(platform_index)), bstack11l1ll1llll_opy_, bstack11l1llllll1_opy_)
        if not os.path.exists(bstack11l1llll111_opy_) or not os.path.isdir(bstack11l1llll111_opy_):
            self.logger.info(bstack1l1_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤ᠂").format(bstack11l1llll111_opy_))
        else:
            self.logger.info(bstack1l1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢ᠃").format(bstack11l1llll111_opy_))
            with os.scandir(bstack11l1llll111_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111l11l1l_opy_:
                        self.logger.info(bstack1l1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ᠄").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1_opy_ (u"ࠥࠦ᠅")
                        log_entry = bstack1l1l1l1lll1_opy_(
                            kind=bstack1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᠆"),
                            message=bstack1l1_opy_ (u"ࠧࠨ᠇"),
                            level=bstack1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ᠈"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11lllllllll_opy_=entry.stat().st_size,
                            bstack1l111l1ll11_opy_=bstack1l1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ᠉"),
                            bstack1llllll1_opy_=os.path.abspath(entry.path),
                            bstack1l11111ll1l_opy_=hook.get(TestFramework.bstack11l11ll1ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l111l11l1l_opy_.add(abs_path)
        hook[bstack1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᠊")] = logs
    def bstack11lllllll11_opy_(
        self,
        bstack1l11111l1ll_opy_: bstack1l1llll1lll_opy_,
        entries: List[bstack1l1l1l1lll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨ᠋"))
        req.platform_index = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l1l1111l1l_opy_)
        req.client_worker_id = bstack1l1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᠌").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11111l1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11111l1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11111l1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l11lll1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l111l111l1_opy_)
            log_entry.uuid = entry.bstack11l1ll11111_opy_ if entry.bstack11l1ll11111_opy_ else TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l11l1lll1l_opy_)
            log_entry.test_framework_state = bstack1l11111l1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᠍"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢ᠎"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lllllllll_opy_
                log_entry.file_path = entry.bstack1llllll1_opy_
        def bstack1l1111llll1_opy_():
            bstack1l1lll11l1_opy_ = datetime.now()
            try:
                self.bstack1l1ll11l111_opy_.LogCreatedEvent(req)
                bstack1l11111l1ll_opy_.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ᠏"), datetime.now() - bstack1l1lll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨ᠐").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l1111llll1_opy_)
    def __11l1l1l1111_opy_(self, instance) -> None:
        bstack1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᠑")
        bstack11l1l1llll1_opy_ = {bstack1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦ᠒"): bstack1l1ll1ll1ll_opy_.bstack11l1ll1111l_opy_()}
        TestFramework.bstack11l1l1ll111_opy_(instance, bstack11l1l1llll1_opy_)
    @staticmethod
    def __11l1l1l1ll1_opy_(instance, args):
        request, bstack11l1ll111l1_opy_ = args
        bstack11l1lll1l1l_opy_ = id(bstack11l1ll111l1_opy_)
        bstack11l1lllllll_opy_ = instance.data[TestFramework.bstack11l1l1lll11_opy_]
        step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠪ࡭ࡩ࠭᠓")] == bstack11l1lll1l1l_opy_, bstack11l1lllllll_opy_[bstack1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᠔")]), None)
        step.update({
            bstack1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᠕"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11l1lllllll_opy_[bstack1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᠖")]) if st[bstack1l1_opy_ (u"ࠧࡪࡦࠪ᠗")] == step[bstack1l1_opy_ (u"ࠨ࡫ࡧࠫ᠘")]), None)
        if index is not None:
            bstack11l1lllllll_opy_[bstack1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᠙")][index] = step
        instance.data[TestFramework.bstack11l1l1lll11_opy_] = bstack11l1lllllll_opy_
    @staticmethod
    def __11l1l11l1l1_opy_(instance, args):
        bstack1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᠚")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11l1ll111l1_opy_ = args[1]
        bstack11l1lll1l1l_opy_ = id(bstack11l1ll111l1_opy_)
        bstack11l1lllllll_opy_ = instance.data[TestFramework.bstack11l1l1lll11_opy_]
        step = None
        if bstack11l1lll1l1l_opy_ is not None and bstack11l1lllllll_opy_.get(bstack1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᠛")):
            step = next(filter(lambda st: st[bstack1l1_opy_ (u"ࠬ࡯ࡤࠨ᠜")] == bstack11l1lll1l1l_opy_, bstack11l1lllllll_opy_[bstack1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᠝")]), None)
            step.update({
                bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᠞"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᠟"): bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᠠ"),
                bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᠡ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᠢ"): bstack1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᠣ"),
                })
        index = next((i for i, st in enumerate(bstack11l1lllllll_opy_[bstack1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᠤ")]) if st[bstack1l1_opy_ (u"ࠧࡪࡦࠪᠥ")] == step[bstack1l1_opy_ (u"ࠨ࡫ࡧࠫᠦ")]), None)
        if index is not None:
            bstack11l1lllllll_opy_[bstack1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᠧ")][index] = step
        instance.data[TestFramework.bstack11l1l1lll11_opy_] = bstack11l1lllllll_opy_
    @staticmethod
    def __11l1lllll1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᠨ")):
                examples = list(node.callspec.params[bstack1l1_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᠩ")].values())
            return examples
        except:
            return []
    def bstack1l1111l1111_opy_(self, instance: bstack1l1llll1lll_opy_, bstack1ll11ll1lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l111111_opy_ = (
            PytestBDDFramework.bstack11l1ll1ll1l_opy_
            if bstack1ll11ll1lll_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1l11l111_opy_
        )
        hook = PytestBDDFramework.bstack11l1lllll11_opy_(instance, bstack11l1l111111_opy_)
        entries = hook.get(TestFramework.bstack11l1lll11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack11l1ll11ll1_opy_, []))
        return entries
    def bstack1l111ll1l11_opy_(self, instance: bstack1l1llll1lll_opy_, bstack1ll11ll1lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l111111_opy_ = (
            PytestBDDFramework.bstack11l1ll1ll1l_opy_
            if bstack1ll11ll1lll_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1l11l111_opy_
        )
        PytestBDDFramework.bstack11l1lll1111_opy_(instance, bstack11l1l111111_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack11l1ll11ll1_opy_, []).clear()
    @staticmethod
    def bstack11l1lllll11_opy_(instance: bstack1l1llll1lll_opy_, bstack11l1l111111_opy_: str):
        bstack11l1l111l1l_opy_ = (
            PytestBDDFramework.bstack11l1ll1l1l1_opy_
            if bstack11l1l111111_opy_ == PytestBDDFramework.bstack11l1l11l111_opy_
            else PytestBDDFramework.bstack11l1llll1l1_opy_
        )
        bstack11l1l1ll11l_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, bstack11l1l111111_opy_, None)
        bstack11l1l11llll_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, bstack11l1l111l1l_opy_, None) if bstack11l1l1ll11l_opy_ else None
        return (
            bstack11l1l11llll_opy_[bstack11l1l1ll11l_opy_][-1]
            if isinstance(bstack11l1l11llll_opy_, dict) and len(bstack11l1l11llll_opy_.get(bstack11l1l1ll11l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1lll1111_opy_(instance: bstack1l1llll1lll_opy_, bstack11l1l111111_opy_: str):
        hook = PytestBDDFramework.bstack11l1lllll11_opy_(instance, bstack11l1l111111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1lll11ll_opy_, []).clear()
    @staticmethod
    def __11l1ll11l11_opy_(instance: bstack1l1llll1lll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᠪ"), None)):
            return
        if os.getenv(bstack1l1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᠫ"), bstack1l1_opy_ (u"ࠢ࠲ࠤᠬ")) != bstack1l1_opy_ (u"ࠣ࠳ࠥᠭ"):
            PytestBDDFramework.logger.warning(bstack1l1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᠮ"))
            return
        bstack11l1l11l1ll_opy_ = {
            bstack1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᠯ"): (PytestBDDFramework.bstack11l1ll1ll1l_opy_, PytestBDDFramework.bstack11l1llll1l1_opy_),
            bstack1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᠰ"): (PytestBDDFramework.bstack11l1l11l111_opy_, PytestBDDFramework.bstack11l1ll1l1l1_opy_),
        }
        for when in (bstack1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᠱ"), bstack1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᠲ"), bstack1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᠳ")):
            bstack11l11llll11_opy_ = args[1].get_records(when)
            if not bstack11l11llll11_opy_:
                continue
            records = [
                bstack1l1l1l1lll1_opy_(
                    kind=TestFramework.bstack11lllll1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᠴ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᠵ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l11llll11_opy_
                if isinstance(getattr(r, bstack1l1_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᠶ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1l1l1l11_opy_, bstack11l1l111l1l_opy_ = bstack11l1l11l1ll_opy_.get(when, (None, None))
            bstack11l1l1ll1l1_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, bstack11l1l1l1l11_opy_, None) if bstack11l1l1l1l11_opy_ else None
            bstack11l1l11llll_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, bstack11l1l111l1l_opy_, None) if bstack11l1l1ll1l1_opy_ else None
            if isinstance(bstack11l1l11llll_opy_, dict) and len(bstack11l1l11llll_opy_.get(bstack11l1l1ll1l1_opy_, [])) > 0:
                hook = bstack11l1l11llll_opy_[bstack11l1l1ll1l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1lll11ll_opy_ in hook:
                    hook[TestFramework.bstack11l1lll11ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack11l1ll11ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l11ll11l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l11llllll_opy_(request.node, scenario)
        bstack11l11lll111_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l11lll111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l11l1lll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11lll11ll1l_opy_: test_id,
            TestFramework.bstack1l11llll111_opy_: test_name,
            TestFramework.bstack11llll1l111_opy_: test_id,
            TestFramework.bstack11l1l111lll_opy_: bstack11l11lll111_opy_,
            TestFramework.bstack11l1ll111ll_opy_: PytestBDDFramework.__11l1ll1l11l_opy_(feature, scenario),
            TestFramework.bstack11l1l11l11l_opy_: code,
            TestFramework.bstack11ll1lllll1_opy_: TestFramework.bstack11l1l1lllll_opy_,
            TestFramework.bstack11ll11l11ll_opy_: test_name
        }
    @staticmethod
    def __11l11llllll_opy_(node, scenario):
        if hasattr(node, bstack1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᠷ")):
            parts = node.nodeid.rsplit(bstack1l1_opy_ (u"ࠧࡡࠢᠸ"))
            params = parts[-1]
            return bstack1l1_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᠹ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l1ll1l11l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬᠺ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᠻ")) else [])
    @staticmethod
    def __11l1l1l1lll_opy_(location):
        return bstack1l1_opy_ (u"ࠤ࠽࠾ࠧᠼ").join(filter(lambda x: isinstance(x, str), location))