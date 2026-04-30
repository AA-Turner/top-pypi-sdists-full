# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1ll11lll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack111111ll1l_opy_ import bstack11l111l111l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l1ll111_opy_,
    TestHookState,
    bstack1ll1lll111l_opy_,
    bstack11lll1ll1l_opy_,
)
import traceback
from bstack_utils.helper import bstack11lll11111l_opy_
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11ll1_opy_ import bstack1l1l1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll111l1_opy_
bstack11lll11l1ll_opy_ = bstack11lll11111l_opy_()
bstack11ll111ll11_opy_ = bstack1l1111l_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᤃ")
bstack111llll1111_opy_ = bstack1l1111l_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᤄ")
bstack111llll1ll1_opy_ = bstack1l1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᤅ")
bstack111llllll1l_opy_ = 1.0
_11ll111llll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack111ll1ll1l1_opy_ = bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᤆ")
    bstack111lll11l1l_opy_ = bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᤇ")
    bstack111ll1l1ll1_opy_ = bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᤈ")
    bstack111lllll111_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᤉ")
    bstack111ll1l11l1_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᤊ")
    bstack11l111l11ll_opy_: bool
    bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_  = None
    bstack111ll11ll11_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1l1l1lll111_opy_: List[str]=[bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᤋ")],
        bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_ = None,
        bstack11l1ll1lll_opy_=None
    ):
        super().__init__(bstack1l1l1lll111_opy_, bstack1l111lllll1_opy_, bstack1l1lll11l1l_opy_)
        self.bstack11l111l11ll_opy_ = any(bstack1l1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᤌ") in item.lower() for item in bstack1l1l1lll111_opy_)
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
    def track_event(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack111ll11ll11_opy_:
            bstack11l111l111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᤍ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠤࠥᤎ"))
            return
        if not self.bstack11l111l11ll_opy_:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᤏ") + str(str(self.bstack1l1l1lll111_opy_)) + bstack1l1111l_opy_ (u"ࠦࠧᤐ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᤑ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠨࠢᤒ"))
            return
        instance = self.__11l111l1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᤓ") + str(args) + bstack1l1111l_opy_ (u"ࠣࠤᤔ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111ll11ll11_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack1ll1ll1ll_opy_.value)
                name = str(EVENTS.bstack1ll1ll1ll_opy_.name)+bstack1l1111l_opy_ (u"ࠤ࠽ࠦᤕ")+str(test_framework_state.name)
                TestFramework.bstack111lll11ll1_opy_(instance, name, bstack1l11l1l11_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᤖ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11l1ll11111_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111ll1l111l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᤗ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠧࠨᤘ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11lll1111ll_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11lll1111ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__111llll11ll_opy_(instance, args)
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᤙ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠢࠣᤚ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᤛ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠤࠥᤜ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l111l1111_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l11111l1l_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l111111l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll11111_opy_(instance, *args)
                self.__11l1111llll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack111ll11ll11_opy_:
                self.__111ll1l1111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᤝ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠦࠧᤞ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111lllll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111ll11ll11_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1ll1ll1ll_opy_.name)+bstack1l1111l_opy_ (u"ࠧࡀࠢ᤟")+str(test_framework_state.name)
                bstack1l11l1l11_opy_ = TestFramework.bstack111ll1l1l11_opy_(instance, name)
                bstack11lll1111_opy_.end(EVENTS.bstack1ll1ll1ll_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᤠ"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᤡ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᤢ").format(e))
    def bstack11ll11l111l_opy_(self):
        return self.bstack11l111l11ll_opy_
    def bstack11ll1l11l1l_opy_(self):
        return False
    def __111lll1l11l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1111l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᤣ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11ll1lll1l1_opy_(rep, [bstack1l1111l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᤤ"), bstack1l1111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᤥ"), bstack1l1111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᤦ"), bstack1l1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᤧ"), bstack1l1111l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᤨ"), bstack1l1111l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᤩ")])
        return None
    def __111lll11111_opy_(self, instance: bstack1l11l1ll111_opy_, *args):
        result = self.__111lll1l11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        if result.get(bstack1l1111l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᤪ"), None) == bstack1l1111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᤫ") and len(args) > 1 and getattr(args[1], bstack1l1111l_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧ᤬"), None) is not None:
            failure = [{bstack1l1111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ᤭"): [args[1].excinfo.exconly(), result.get(bstack1l1111l_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧ᤮"), None)]}]
            bstack1ll111l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ᤯") if bstack1l1111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᤰ") in getattr(args[1].excinfo, bstack1l1111l_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᤱ"), bstack1l1111l_opy_ (u"ࠥࠦᤲ")) else bstack1l1111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᤳ")
        bstack111ll11l111_opy_ = result.get(bstack1l1111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᤴ"), TestFramework.bstack111lll1l1ll_opy_)
        if bstack111ll11l111_opy_ != TestFramework.bstack111lll1l1ll_opy_:
            TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11ll111l11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack111ll1lllll_opy_(instance, {
            TestFramework.bstack11l1l1ll11l_opy_: failure,
            TestFramework.bstack111ll11l1ll_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack11l1ll1111l_opy_: bstack111ll11l111_opy_,
        })
    def __11l111l1l11_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll11ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1l1l1ll_opy_ bstack111lll1111l_opy_ this to be bstack1l1111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᤵ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111ll1ll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᤶ"), None), bstack1l1111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᤷ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᤸ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦ᤹ࠥ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll1ll1ll_opy_(target) if target else None
        return instance
    def __111ll1l1111_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack111lll1l111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, PytestBDDFramework.bstack111lll11l1l_opy_, {})
        if not key in bstack111lll1l111_opy_:
            bstack111lll1l111_opy_[key] = []
        bstack111llllllll_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, PytestBDDFramework.bstack111ll1l1ll1_opy_, {})
        if not key in bstack111llllllll_opy_:
            bstack111llllllll_opy_[key] = []
        bstack111llllll11_opy_ = {
            PytestBDDFramework.bstack111lll11l1l_opy_: bstack111lll1l111_opy_,
            PytestBDDFramework.bstack111ll1l1ll1_opy_: bstack111llllllll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1111l_opy_ (u"ࠦࡰ࡫ࡹࠣ᤺"): key,
                TestFramework.bstack11l1111l111_opy_: uuid4().__str__(),
                TestFramework.bstack111lll111ll_opy_: TestFramework.bstack111ll1lll11_opy_,
                TestFramework.bstack111ll11lll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll111lll_opy_: [],
                TestFramework.bstack11l1111ll1l_opy_: hook_name,
                TestFramework.bstack111lll1llll_opy_: bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()
            }
            bstack111lll1l111_opy_[key].append(hook)
            bstack111llllll11_opy_[PytestBDDFramework.bstack111lllll111_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llll1lll_opy_ = bstack111lll1l111_opy_.get(key, [])
            hook = bstack111llll1lll_opy_.pop() if bstack111llll1lll_opy_ else None
            if hook:
                result = self.__111lll1l11l_opy_(*args)
                if result:
                    bstack11l1111l1l1_opy_ = result.get(bstack1l1111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨ᤻"), TestFramework.bstack111ll1lll11_opy_)
                    if bstack11l1111l1l1_opy_ != TestFramework.bstack111ll1lll11_opy_:
                        hook[TestFramework.bstack111lll111ll_opy_] = bstack11l1111l1l1_opy_
                hook[TestFramework.bstack11l111111ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111lll1llll_opy_] = bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()
                self.bstack11l1111l1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111llll1l1l_opy_, [])
                self.bstack1llll111ll_opy_(instance, logs)
                bstack111llllllll_opy_[key].append(hook)
                bstack111llllll11_opy_[PytestBDDFramework.bstack111ll1l11l1_opy_] = key
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧ᤼") + str(bstack111llllllll_opy_) + bstack1l1111l_opy_ (u"ࠢࠣ᤽"))
    def __111ll11ll1l_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11ll1lll1l1_opy_(args[0], [bstack1l1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᤾"), bstack1l1111l_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥ᤿"), bstack1l1111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥ᥀"), bstack1l1111l_opy_ (u"ࠦ࡮ࡪࡳࠣ᥁"), bstack1l1111l_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢ᥂"), bstack1l1111l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨ᥃")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᥄")) else fixturedef.get(bstack1l1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᥅"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1111l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢ᥆")) else None
        node = request.node if hasattr(request, bstack1l1111l_opy_ (u"ࠥࡲࡴࡪࡥࠣ᥇")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1111l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᥈")) else None
        baseid = fixturedef.get(bstack1l1111l_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧ᥉"), None) or bstack1l1111l_opy_ (u"ࠨࠢ᥊")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1111l_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧ᥋")):
            target = PytestBDDFramework.__111lll11lll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1111l_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥ᥌")) else None
            if target and not TestFramework.bstack1l1ll1ll1ll_opy_(target):
                self.__111ll1ll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ᥍") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠥࠦ᥎"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤ᥏") + str(target) + bstack1l1111l_opy_ (u"ࠧࠨᥐ"))
            return None
        instance = TestFramework.bstack1l1ll1ll1ll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᥑ") + str(target) + bstack1l1111l_opy_ (u"ࠢࠣᥒ"))
            return None
        bstack11l11111l11_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, PytestBDDFramework.bstack111ll1ll1l1_opy_, {})
        if os.getenv(bstack1l1111l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᥓ"), bstack1l1111l_opy_ (u"ࠤ࠴ࠦᥔ")) == bstack1l1111l_opy_ (u"ࠥ࠵ࠧᥕ"):
            bstack11l1111l11l_opy_ = bstack1l1111l_opy_ (u"ࠦ࠿ࠨᥖ").join((scope, fixturename))
            bstack111ll1l1lll_opy_ = datetime.now(tz=timezone.utc)
            bstack111ll11llll_opy_ = {
                bstack1l1111l_opy_ (u"ࠧࡱࡥࡺࠤᥗ"): bstack11l1111l11l_opy_,
                bstack1l1111l_opy_ (u"ࠨࡴࡢࡩࡶࠦᥘ"): PytestBDDFramework.__111lll1l1l1_opy_(request.node, scenario),
                bstack1l1111l_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᥙ"): fixturedef,
                bstack1l1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᥚ"): scope,
                bstack1l1111l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᥛ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᥜ"), None)):
                    bstack111ll11llll_opy_[bstack1l1111l_opy_ (u"ࠦࡹࡿࡰࡦࠤᥝ")] = TestFramework.bstack11lll11ll11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111ll11llll_opy_[bstack1l1111l_opy_ (u"ࠧࡻࡵࡪࡦࠥᥞ")] = uuid4().__str__()
                bstack111ll11llll_opy_[PytestBDDFramework.bstack111ll11lll1_opy_] = bstack111ll1l1lll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111ll11llll_opy_[PytestBDDFramework.bstack11l111111ll_opy_] = bstack111ll1l1lll_opy_
            if bstack11l1111l11l_opy_ in bstack11l11111l11_opy_:
                bstack11l11111l11_opy_[bstack11l1111l11l_opy_].update(bstack111ll11llll_opy_)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᥟ") + str(bstack11l11111l11_opy_[bstack11l1111l11l_opy_]) + bstack1l1111l_opy_ (u"ࠢࠣᥠ"))
            else:
                bstack11l11111l11_opy_[bstack11l1111l11l_opy_] = bstack111ll11llll_opy_
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᥡ") + str(len(bstack11l11111l11_opy_)) + bstack1l1111l_opy_ (u"ࠤࠥᥢ"))
        TestFramework.bstack111l1llll1_opy_(instance, PytestBDDFramework.bstack111ll1ll1l1_opy_, bstack11l11111l11_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᥣ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠦࠧᥤ"))
        return instance
    def __111ll1ll1ll_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll11lll1_opy_.create_context(target)
        ob = bstack1l11l1ll111_opy_(ctx, self.bstack1l1l1lll111_opy_, self.bstack1l111lllll1_opy_, test_framework_state)
        TestFramework.bstack111ll1lllll_opy_(ob, {
            TestFramework.bstack1l11111l11l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l1lll_opy_: context.test_framework_version,
            TestFramework.bstack111lll1lll1_opy_: [],
            PytestBDDFramework.bstack111ll1ll1l1_opy_: {},
            PytestBDDFramework.bstack111ll1l1ll1_opy_: {},
            PytestBDDFramework.bstack111lll11l1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111l1llll1_opy_(ob, TestFramework.bstack11l1111lll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111l1llll1_opy_(ob, TestFramework.bstack1l111l1l111_opy_, context.platform_index)
        TestFramework.bstack1lllll1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᥥ") + str(TestFramework.bstack1lllll1ll1_opy_.keys()) + bstack1l1111l_opy_ (u"ࠨࠢᥦ"))
        return ob
    @staticmethod
    def __111llll11ll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1111l_opy_ (u"ࠧࡪࡦࠪᥧ"): id(step),
                bstack1l1111l_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᥨ"): step.name,
                bstack1l1111l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᥩ"): step.keyword,
            })
        meta = {
            bstack1l1111l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᥪ"): {
                bstack1l1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᥫ"): feature.name,
                bstack1l1111l_opy_ (u"ࠬࡶࡡࡵࡪࠪᥬ"): feature.filename,
                bstack1l1111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᥭ"): feature.description
            },
            bstack1l1111l_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ᥮"): {
                bstack1l1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᥯"): scenario.name
            },
            bstack1l1111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᥰ"): steps,
            bstack1l1111l_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᥱ"): PytestBDDFramework.__111ll1llll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack111ll11l11l_opy_: meta
            }
        )
    def bstack11l1111l1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᥲ")
        global _11ll111llll_opy_
        platform_index = os.environ[bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᥳ")]
        bstack11lll11l111_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), bstack111llll1111_opy_)
        if not os.path.exists(bstack11lll11l111_opy_) or not os.path.isdir(bstack11lll11l111_opy_):
            return
        logs = hook.get(bstack1l1111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᥴ"), [])
        with os.scandir(bstack11lll11l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll111llll_opy_:
                    self.logger.info(bstack1l1111l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧ᥵").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1111l_opy_ (u"ࠣࠤ᥶")
                    log_entry = bstack11lll1ll1l_opy_(
                        kind=bstack1l1111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᥷"),
                        message=bstack1l1111l_opy_ (u"ࠥࠦ᥸"),
                        level=bstack1l1111l_opy_ (u"ࠦࠧ᥹"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll11l1111_opy_=entry.stat().st_size,
                        bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧ᥺"),
                        bstack111111_opy_=os.path.abspath(entry.path),
                        bstack111ll1l1l1l_opy_=hook.get(TestFramework.bstack11l1111l111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll111llll_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᥻")]
        bstack111llll11l1_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), bstack111llll1111_opy_, bstack111llll1ll1_opy_)
        if not os.path.exists(bstack111llll11l1_opy_) or not os.path.isdir(bstack111llll11l1_opy_):
            self.logger.info(bstack1l1111l_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤ᥼").format(bstack111llll11l1_opy_))
        else:
            self.logger.info(bstack1l1111l_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢ᥽").format(bstack111llll11l1_opy_))
            with os.scandir(bstack111llll11l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll111llll_opy_:
                        self.logger.info(bstack1l1111l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ᥾").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1111l_opy_ (u"ࠥࠦ᥿")
                        log_entry = bstack11lll1ll1l_opy_(
                            kind=bstack1l1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᦀ"),
                            message=bstack1l1111l_opy_ (u"ࠧࠨᦁ"),
                            level=bstack1l1111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᦂ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll11l1111_opy_=entry.stat().st_size,
                            bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᦃ"),
                            bstack111111_opy_=os.path.abspath(entry.path),
                            bstack11ll111l111_opy_=hook.get(TestFramework.bstack11l1111l111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll111llll_opy_.add(abs_path)
        hook[bstack1l1111l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᦄ")] = logs
    def bstack1llll111ll_opy_(
        self,
        bstack1l111ll1ll_opy_: bstack1l11l1ll111_opy_,
        entries: List[bstack11lll1ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᦅ"))
        req.platform_index = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l111l1l111_opy_)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᦆ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l11111l11l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11ll11l1lll_opy_)
            log_entry.uuid = entry.bstack111ll1l1l1l_opy_ if entry.bstack111ll1l1l1l_opy_ else TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11llllll111_opy_)
            log_entry.test_framework_state = bstack1l111ll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᦇ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᦈ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll11l1111_opy_
                log_entry.file_path = entry.bstack111111_opy_
        def bstack11ll11lll11_opy_():
            bstack11l11l1l_opy_ = datetime.now()
            try:
                self.bstack11l1ll1lll_opy_.LogCreatedEvent(req)
                bstack1l111ll1ll_opy_.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᦉ"), datetime.now() - bstack11l11l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᦊ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11lll11_opy_)
    def __11l1111llll_opy_(self, instance) -> None:
        bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᦋ")
        bstack111llllll11_opy_ = {bstack1l1111l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᦌ"): bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()}
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        bstack1l1l1l1lll1_opy_.bstack111lll1ll11_opy_()
    @staticmethod
    def __11l111l1111_opy_(instance, args):
        request, bstack111lll1ll1l_opy_ = args
        bstack111lllllll1_opy_ = id(bstack111lll1ll1l_opy_)
        bstack111lllll1l1_opy_ = instance.data[TestFramework.bstack111ll11l11l_opy_]
        step = next(filter(lambda st: st[bstack1l1111l_opy_ (u"ࠪ࡭ࡩ࠭ᦍ")] == bstack111lllllll1_opy_, bstack111lllll1l1_opy_[bstack1l1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᦎ")]), None)
        step.update({
            bstack1l1111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᦏ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack111lllll1l1_opy_[bstack1l1111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᦐ")]) if st[bstack1l1111l_opy_ (u"ࠧࡪࡦࠪᦑ")] == step[bstack1l1111l_opy_ (u"ࠨ࡫ࡧࠫᦒ")]), None)
        if index is not None:
            bstack111lllll1l1_opy_[bstack1l1111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᦓ")][index] = step
        instance.data[TestFramework.bstack111ll11l11l_opy_] = bstack111lllll1l1_opy_
    @staticmethod
    def __11l11111l1l_opy_(instance, args):
        bstack1l1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᦔ")
        bstack1lll111l111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111lll1ll1l_opy_ = args[1]
        bstack111lllllll1_opy_ = id(bstack111lll1ll1l_opy_)
        bstack111lllll1l1_opy_ = instance.data[TestFramework.bstack111ll11l11l_opy_]
        step = None
        if bstack111lllllll1_opy_ is not None and bstack111lllll1l1_opy_.get(bstack1l1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᦕ")):
            step = next(filter(lambda st: st[bstack1l1111l_opy_ (u"ࠬ࡯ࡤࠨᦖ")] == bstack111lllllll1_opy_, bstack111lllll1l1_opy_[bstack1l1111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᦗ")]), None)
            step.update({
                bstack1l1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᦘ"): bstack1lll111l111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᦙ"): bstack1l1111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᦚ"),
                bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᦛ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᦜ"): bstack1l1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᦝ"),
                })
        index = next((i for i, st in enumerate(bstack111lllll1l1_opy_[bstack1l1111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᦞ")]) if st[bstack1l1111l_opy_ (u"ࠧࡪࡦࠪᦟ")] == step[bstack1l1111l_opy_ (u"ࠨ࡫ࡧࠫᦠ")]), None)
        if index is not None:
            bstack111lllll1l1_opy_[bstack1l1111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᦡ")][index] = step
        instance.data[TestFramework.bstack111ll11l11l_opy_] = bstack111lllll1l1_opy_
    @staticmethod
    def __111ll1llll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᦢ")):
                examples = list(node.callspec.params[bstack1l1111l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᦣ")].values())
            return examples
        except:
            return []
    def bstack11lll1l111l_opy_(self, instance: bstack1l11l1ll111_opy_, bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            PytestBDDFramework.bstack111lllll111_opy_
            if bstack1l1ll1ll111_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111ll1l11l1_opy_
        )
        hook = PytestBDDFramework.bstack111ll1l11ll_opy_(instance, bstack111lll11l11_opy_)
        entries = hook.get(TestFramework.bstack111ll111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, []))
        return entries
    def bstack11ll1llll1l_opy_(self, instance: bstack1l11l1ll111_opy_, bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            PytestBDDFramework.bstack111lllll111_opy_
            if bstack1l1ll1ll111_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111ll1l11l1_opy_
        )
        PytestBDDFramework.bstack111lllll1ll_opy_(instance, bstack111lll11l11_opy_)
        TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, []).clear()
    @staticmethod
    def bstack111ll1l11ll_opy_(instance: bstack1l11l1ll111_opy_, bstack111lll11l11_opy_: str):
        bstack11l11111111_opy_ = (
            PytestBDDFramework.bstack111ll1l1ll1_opy_
            if bstack111lll11l11_opy_ == PytestBDDFramework.bstack111ll1l11l1_opy_
            else PytestBDDFramework.bstack111lll11l1l_opy_
        )
        bstack11l111l11l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack111lll11l11_opy_, None)
        bstack111lll111l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack11l11111111_opy_, None) if bstack11l111l11l1_opy_ else None
        return (
            bstack111lll111l1_opy_[bstack11l111l11l1_opy_][-1]
            if isinstance(bstack111lll111l1_opy_, dict) and len(bstack111lll111l1_opy_.get(bstack11l111l11l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack111lllll1ll_opy_(instance: bstack1l11l1ll111_opy_, bstack111lll11l11_opy_: str):
        hook = PytestBDDFramework.bstack111ll1l11ll_opy_(instance, bstack111lll11l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll111lll_opy_, []).clear()
    @staticmethod
    def __11l111111l1_opy_(instance: bstack1l11l1ll111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1111l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᦤ"), None)):
            return
        if os.getenv(bstack1l1111l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᦥ"), bstack1l1111l_opy_ (u"ࠢ࠲ࠤᦦ")) != bstack1l1111l_opy_ (u"ࠣ࠳ࠥᦧ"):
            PytestBDDFramework.logger.warning(bstack1l1111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᦨ"))
            return
        bstack111llll1l11_opy_ = {
            bstack1l1111l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᦩ"): (PytestBDDFramework.bstack111lllll111_opy_, PytestBDDFramework.bstack111lll11l1l_opy_),
            bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᦪ"): (PytestBDDFramework.bstack111ll1l11l1_opy_, PytestBDDFramework.bstack111ll1l1ll1_opy_),
        }
        for when in (bstack1l1111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᦫ"), bstack1l1111l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ᦬"), bstack1l1111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ᦭")):
            bstack111ll1lll1l_opy_ = args[1].get_records(when)
            if not bstack111ll1lll1l_opy_:
                continue
            records = [
                bstack11lll1ll1l_opy_(
                    kind=TestFramework.bstack11lll11llll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1111l_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦ᦮")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1111l_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥ᦯")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll1lll1l_opy_
                if isinstance(getattr(r, bstack1l1111l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᦰ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111llll111l_opy_, bstack11l11111111_opy_ = bstack111llll1l11_opy_.get(when, (None, None))
            bstack111ll1ll111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack111llll111l_opy_, None) if bstack111llll111l_opy_ else None
            bstack111lll111l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack11l11111111_opy_, None) if bstack111ll1ll111_opy_ else None
            if isinstance(bstack111lll111l1_opy_, dict) and len(bstack111lll111l1_opy_.get(bstack111ll1ll111_opy_, [])) > 0:
                hook = bstack111lll111l1_opy_[bstack111ll1ll111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll111lll_opy_ in hook:
                    hook[TestFramework.bstack111ll111lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111ll1l111l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l11111lll_opy_(request.node, scenario)
        bstack111ll11l1l1_opy_ = feature.filename
        if not test_id or not test_name or not bstack111ll11l1l1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack11llllll111_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll11111_opy_: test_id,
            TestFramework.bstack1l111l11l1l_opy_: test_name,
            TestFramework.bstack11ll11111l1_opy_: test_id,
            TestFramework.bstack11l1111ll11_opy_: bstack111ll11l1l1_opy_,
            TestFramework.bstack11l11111ll1_opy_: PytestBDDFramework.__111lll1l1l1_opy_(feature, scenario),
            TestFramework.bstack11l1111111l_opy_: code,
            TestFramework.bstack11l1ll1111l_opy_: TestFramework.bstack111lll1l1ll_opy_,
            TestFramework.bstack11l11l11l1l_opy_: test_name
        }
    @staticmethod
    def __11l11111lll_opy_(node, scenario):
        if hasattr(node, bstack1l1111l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᦱ")):
            parts = node.nodeid.rsplit(bstack1l1111l_opy_ (u"ࠧࡡࠢᦲ"))
            params = parts[-1]
            return bstack1l1111l_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᦳ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __111lll1l1l1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1111l_opy_ (u"ࠧࡵࡣࡪࡷࠬᦴ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᦵ")) else [])
    @staticmethod
    def __111lll11lll_opy_(location):
        return bstack1l1111l_opy_ (u"ࠤ࠽࠾ࠧᦶ").join(filter(lambda x: isinstance(x, str), location))