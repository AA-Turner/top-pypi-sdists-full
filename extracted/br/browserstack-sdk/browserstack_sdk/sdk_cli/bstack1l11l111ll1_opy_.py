# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1l1ll11111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1lll1l_opy_ import bstack11l111l1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l111ll1l_opy_,
    TestHookState,
    bstack1ll1ll1ll1l_opy_,
    bstack1111lll111_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11ll1ll11ll_opy_
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll1l11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l1l1l1l_opy_ import bstack1l1l1lll1l1_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1lllll1l11_opy_
bstack11ll1llll1l_opy_ = bstack11ll1ll11ll_opy_()
bstack111lll1l1ll_opy_ = 1.0
bstack11ll1l1llll_opy_ = bstack11ll11_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᨽ")
bstack111ll11l1ll_opy_ = bstack11ll11_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᨾ")
bstack111ll11l11l_opy_ = bstack11ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᨿ")
bstack111ll11l111_opy_ = bstack11ll11_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᩀ")
bstack111ll11lll1_opy_ = bstack11ll11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᩁ")
_11lll1l1l1l_opy_ = set()
class bstack1l1l11l11ll_opy_(TestFramework):
    bstack111ll111111_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡬ࡧࡼࡻࡴࡸࡤࡴࠤᩂ")
    bstack111ll1l1111_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᩃ")
    bstack111ll1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᩄ")
    bstack111lll111l1_opy_ = bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᩅ")
    bstack11l11111l11_opy_ = bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᩆ")
    bstack111l1llll11_opy_: bool
    bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_ = None
    bstack1l1l111l1_opy_ = None
    bstack11l111ll1ll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1l1ll111l_opy_: Dict[str, str],
        bstack1l1l11l1l11_opy_: List[str] = [bstack11ll11_opy_ (u"ࠢࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣᩇ")],
        bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_ = None,
        bstack1l1l111l1_opy_=None
    ):
        super().__init__(bstack1l1l11l1l11_opy_, bstack1l1l1ll111l_opy_, bstack1l1lll11ll1_opy_)
        self.bstack111l1llll11_opy_ = any(bstack11ll11_opy_ (u"ࠣࡴࡲࡦࡴࡺࠢᩈ") in item.lower() for item in bstack1l1l11l1l11_opy_)
        self.bstack1l1l111l1_opy_ = bstack1l1l111l1_opy_
    def track_event(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l11l11ll_opy_.bstack11l111ll1ll_opy_:
            bstack11l111l1l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack11ll11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨᩉ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111l1llll11_opy_:
            self.logger.warning(bstack11ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࡿࢂࠨᩊ").format(str(self.bstack1l1l11l1l11_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᩋ").format(args, kwargs))
            return
        instance = self.__111lll11111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠨᩌ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1l11l11ll_opy_.bstack11l111ll1ll_opy_:
                bstack1111l1ll1l_opy_ = bstack11ll11_opy_ (u"ࠨࠢᩍ")
                name = bstack11ll11_opy_ (u"ࠢࠣᩎ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack111ll11l1l1_opy_.value)
                    name = str(EVENTS.bstack111ll11l1l1_opy_.name) + bstack11ll11_opy_ (u"ࠣ࠼ࠥᩏ") + str(test_framework_state.name)
                else:
                    bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack111ll11llll_opy_.value)
                    name = str(EVENTS.bstack111ll11llll_opy_.name) + bstack11ll11_opy_ (u"ࠤ࠽ࠦᩐ") + str(test_framework_state.name)
                TestFramework.bstack11l111l11ll_opy_(instance, name, bstack1111l1ll1l_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᩑ").format(e))
        try:
            if not TestFramework.bstack1l1llll1l1l_opy_(instance, TestFramework.bstack11l1ll1llll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l11l11ll_opy_.__111l1llllll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11ll11_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢᩒ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1llll1l1l_opy_(instance, TestFramework.bstack11ll11lll1l_opy_):
                    TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11ll11lll1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠨᩓ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1llll1l1l_opy_(instance, TestFramework.bstack11ll1l1111l_opy_):
                    TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11ll1l1111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠧᩔ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l11l11ll_opy_.__11l1111ll1l_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111ll1ll1ll_opy_(instance, *args)
                self.__111llll111l_opy_(instance)
            elif test_framework_state in bstack1l1l11l11ll_opy_.bstack11l111ll1ll_opy_:
                self.__11l1111l111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠥᩕ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l111ll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1l11l11ll_opy_.bstack11l111ll1ll_opy_:
                bstack1111l1ll1l_opy_ = bstack11ll11_opy_ (u"ࠣࠤᩖ")
                name = bstack11ll11_opy_ (u"ࠤࠥᩗ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll11l1l1_opy_.name) + bstack11ll11_opy_ (u"ࠥ࠾ࠧᩘ") + str(test_framework_state.name)
                    bstack1111l1ll1l_opy_ = TestFramework.bstack111llll1l1l_opy_(instance, name)
                    bstack1ll111lll_opy_.end(EVENTS.bstack111ll11l1l1_opy_.value, bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᩙ"), bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᩚ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll11llll_opy_.name) + bstack11ll11_opy_ (u"ࠨ࠺ࠣᩛ") + str(test_framework_state.name)
                    bstack1111l1ll1l_opy_ = TestFramework.bstack111llll1l1l_opy_(instance, name)
                    bstack1ll111lll_opy_.end(EVENTS.bstack111ll11llll_opy_.value, bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᩜ"), bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᩝ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᩞ").format(e))
    def bstack11ll1lll11l_opy_(self):
        return self.bstack111l1llll11_opy_
    def bstack11ll11l11l1_opy_(self):
        return False
    def __111ll1111l1_opy_(self, *args):
        bstack11ll11_opy_ (u"ࠥࠦࠧࡖࡡࡳࡵࡨࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡲࡦࡵࡸࡰࡹࠦ࡯ࡣ࡬ࡨࡧࡹࠨࠢࠣ᩟")
        if len(args) > 1 and hasattr(args[1], bstack11ll11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶ᩠ࠦ")):
            result = args[1]
            if result:
                return TestFramework.bstack11lll111l11_opy_(result, [bstack11ll11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᩡ"), bstack11ll11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᩢ"), bstack11ll11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡺࡩ࡮ࡧࠥᩣ"), bstack11ll11_opy_ (u"ࠣࡧࡱࡨࡹ࡯࡭ࡦࠤᩤ"), bstack11ll11_opy_ (u"ࠤࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠢᩥ")])
        return None
    def __111ll1ll1ll_opy_(self, instance: bstack1l1l111ll1l_opy_, *args):
        result = self.__111ll1111l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111ll11l_opy_ = None
        status = result.get(bstack11ll11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᩦ"), bstack11ll11_opy_ (u"ࠦࡓࡕࡔࠡࡔࡘࡒࠧᩧ"))
        if status == bstack11ll11_opy_ (u"ࠧࡌࡁࡊࡎࠥᩨ") and result.get(bstack11ll11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᩩ")):
            failure = [{bstack11ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᩪ"): [result.get(bstack11ll11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᩫ"), bstack11ll11_opy_ (u"ࠤࠥᩬ"))]}]
            bstack1ll111ll11l_opy_ = bstack11ll11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᩭ")
        bstack11l111l1111_opy_ = TestFramework.bstack11l111l1ll1_opy_
        if status == bstack11ll11_opy_ (u"ࠦࡕࡇࡓࡔࠤᩮ"):
            bstack11l111l1111_opy_ = bstack11ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᩯ")
        elif status == bstack11ll11_opy_ (u"ࠨࡆࡂࡋࡏࠦᩰ"):
            bstack11l111l1111_opy_ = bstack11ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᩱ")
        elif status == bstack11ll11_opy_ (u"ࠣࡕࡎࡍࡕࠨᩲ"):
            bstack11l111l1111_opy_ = bstack11ll11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᩳ")
        if bstack11l111l1111_opy_ != TestFramework.bstack11l111l1ll1_opy_:
            TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11ll1l11111_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1111llll_opy_(instance, {
            TestFramework.bstack11l1ll1lll1_opy_: failure,
            TestFramework.bstack11l111l111l_opy_: bstack1ll111ll11l_opy_,
            TestFramework.bstack11l1l1lll1l_opy_: bstack11l111l1111_opy_,
        })
    def __111lll11111_opy_(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll111ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111ll111l1l_opy_(test) if test else None
                if target:
                    self.__111ll111l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᩴ"), None)
            elif hasattr(args[0], bstack11ll11_opy_ (u"ࠦ࡮ࡪࠢ᩵")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1l1ll1ll111_opy_(target) if target else None
        return instance
    def __11l1111l111_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack111lll11l11_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack1l1l11l11ll_opy_.bstack111ll1l1111_opy_, {})
        if not key in bstack111lll11l11_opy_:
            bstack111lll11l11_opy_[key] = []
        bstack11l11111lll_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack1l1l11l11ll_opy_.bstack111ll1l1ll1_opy_, {})
        if not key in bstack11l11111lll_opy_:
            bstack11l11111lll_opy_[key] = []
        bstack11l111lll1l_opy_ = {
            bstack1l1l11l11ll_opy_.bstack111ll1l1111_opy_: bstack111lll11l11_opy_,
            bstack1l1l11l11ll_opy_.bstack111ll1l1ll1_opy_: bstack11l11111lll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack11ll11_opy_ (u"ࠧࠨ᩶")
            if len(args) > 0 and hasattr(args[0], bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᩷")):
                hook_name = args[0].name
            hook = {
                bstack11ll11_opy_ (u"ࠢ࡬ࡧࡼࠦ᩸"): key,
                TestFramework.bstack111ll1lll1l_opy_: uuid4().__str__(),
                TestFramework.bstack111lll1l111_opy_: TestFramework.bstack111lll1111l_opy_,
                TestFramework.bstack111llllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll1lll11_opy_: [],
                TestFramework.bstack11l111ll1l1_opy_: hook_name,
                TestFramework.bstack11l111l1lll_opy_: bstack1l1l1lll1l1_opy_.bstack111ll1l111l_opy_()
            }
            bstack111lll11l11_opy_[key].append(hook)
            bstack11l111lll1l_opy_[bstack1l1l11l11ll_opy_.bstack111lll111l1_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l11111l1l_opy_ = bstack111lll11l11_opy_.get(key, [])
            hook = bstack11l11111l1l_opy_.pop() if bstack11l11111l1l_opy_ else None
            if hook:
                result = self.__111ll1111l1_opy_(*args)
                if result:
                    bstack111ll1ll1l1_opy_ = result.get(bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᩹"), TestFramework.bstack111lll1111l_opy_)
                    if bstack111ll1ll1l1_opy_ == bstack11ll11_opy_ (u"ࠤࡓࡅࡘ࡙ࠢ᩺"):
                        bstack111ll1ll1l1_opy_ = bstack11ll11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ᩻")
                    elif bstack111ll1ll1l1_opy_ == bstack11ll11_opy_ (u"ࠦࡋࡇࡉࡍࠤ᩼"):
                        bstack111ll1ll1l1_opy_ = bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᩽")
                    if bstack111ll1ll1l1_opy_ != TestFramework.bstack111lll1111l_opy_:
                        hook[TestFramework.bstack111lll1l111_opy_] = bstack111ll1ll1l1_opy_
                hook[TestFramework.bstack111lll11ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l111l1lll_opy_] = bstack1l1l1lll1l1_opy_.bstack111ll1l111l_opy_()
                self.bstack111lll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111lll1ll11_opy_, [])
                if logs:
                    self.bstack11l1l11l1_opy_(instance, logs)
                bstack11l11111lll_opy_[key].append(hook)
                bstack11l111lll1l_opy_[bstack1l1l11l11ll_opy_.bstack11l11111l11_opy_] = key
        TestFramework.bstack11l1111llll_opy_(instance, bstack11l111lll1l_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽ࠯ࡽࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࡽࢀࠦ᩾").format(key, test_hook_state, bstack111lll11l11_opy_, bstack11l11111lll_opy_))
    def __111ll111ll1_opy_(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack11ll11_opy_ (u"ࠢࠣࠤࡗࡶࡦࡩ࡫ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡪࡼࡥ࡯ࡶࡶࠤ࠭ࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡳࡽࡹ࡫ࡳࡵࠢࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࠧࠨ᩿ࠢ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack11ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪀"), None)
        bstack1l1lll1lll1_opy_ = getattr(keyword, bstack11ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᪁"), None)
        test_id = kwargs.get(bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦ᪂"), None)
        if not test_id:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡯ࡪࡿࡷࡰࡴࡧࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡳࡵࠠࡵࡧࡶࡸࡤ࡯ࡤࠡ࡫ࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢ࡮ࡩࡾࡽ࡯ࡳࡦࡀࡿࢂࠨ᪃").format(keyword_name))
            return None
        instance = TestFramework.bstack1l1ll1ll111_opy_(test_id)
        if not instance:
            self.logger.warning(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡰ࡫ࡹࡸࡱࡵࡨࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡴ࡯ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡴࡦࡵࡷࡣ࡮ࡪ࠽ࡼࡿࠥ᪄").format(test_id))
            return None
        bstack111ll1111ll_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack1l1l11l11ll_opy_.bstack111ll111111_opy_, {})
        if os.getenv(bstack11ll11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡑࡅ࡚࡙ࡒࡖࡉ࡙ࠢ᪅"), bstack11ll11_opy_ (u"ࠢ࠲ࠤ᪆")) == bstack11ll11_opy_ (u"ࠣ࠳ࠥ᪇"):
            bstack111ll11111l_opy_ = bstack11ll11_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣ᪈").format(bstack1l1lll1lll1_opy_, keyword_name)
            bstack111ll1lllll_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1llll1l_opy_ = {
                bstack11ll11_opy_ (u"ࠥ࡯ࡪࡿࠢ᪉"): bstack111ll11111l_opy_,
                bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪊"): keyword_name,
                bstack11ll11_opy_ (u"ࠧࡺࡹࡱࡧࠥ᪋"): bstack1l1lll1lll1_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l1llll1l_opy_[bstack11ll11_opy_ (u"ࠨࡵࡶ࡫ࡧࠦ᪌")] = uuid4().__str__()
                bstack111l1llll1l_opy_[bstack1l1l11l11ll_opy_.bstack111llllll11_opy_] = bstack111ll1lllll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1llll1l_opy_[bstack1l1l11l11ll_opy_.bstack111lll11ll1_opy_] = bstack111ll1lllll_opy_
                if len(args) > 1 and hasattr(args[1], bstack11ll11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᪍")):
                    bstack111l1llll1l_opy_[bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᪎")] = args[1].status
            if bstack111ll11111l_opy_ in bstack111ll1111ll_opy_:
                bstack111ll1111ll_opy_[bstack111ll11111l_opy_].update(bstack111l1llll1l_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠠࡵࡻࡳࡩࡂࢁࡽࠣ᪏").format(keyword_name, bstack1l1lll1lll1_opy_))
            else:
                bstack111ll1111ll_opy_[bstack111ll11111l_opy_] = bstack111l1llll1l_opy_
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡮ࡩࡾࡽ࡯ࡳࡦࡀࡿࢂࠦࡴࡺࡲࡨࡁࢀࢃࠢ᪐").format(keyword_name, bstack1l1lll1lll1_opy_))
        TestFramework.bstack1l1l1111l1_opy_(instance, bstack1l1l11l11ll_opy_.bstack111ll111111_opy_, bstack111ll1111ll_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡷࡂࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠨ᪑").format(len(bstack111ll1111ll_opy_), instance.ref()))
        return instance
    def __111ll111l11_opy_(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll11111l_opy_.create_context(target)
        ob = bstack1l1l111ll1l_opy_(ctx, self.bstack1l1l11l1l11_opy_, self.bstack1l1l1ll111l_opy_, test_framework_state)
        TestFramework.bstack11l1111llll_opy_(ob, {
            TestFramework.bstack1l111ll1111_opy_: context.test_framework_name,
            TestFramework.bstack11lll1l111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1111lll1_opy_: [],
            bstack1l1l11l11ll_opy_.bstack111ll111111_opy_: {},
            bstack1l1l11l11ll_opy_.bstack111ll1l1ll1_opy_: {},
            bstack1l1l11l11ll_opy_.bstack111ll1l1111_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack11ll11_opy_ (u"ࠧࡹ࡯ࡶࡴࡦࡩࠧ᪒")):
            TestFramework.bstack1l1l1111l1_opy_(ob, TestFramework.bstack11l1111111l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1l1l1111l1_opy_(ob, TestFramework.bstack1l111l1lll1_opy_, context.platform_index)
        TestFramework.bstack11111l111l_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࡿࢂࠨ᪓").format(ctx.id, target, args, TestFramework.bstack11111l111l_opy_.keys()))
        return ob
    def bstack11lll1ll11l_opy_(self, instance: bstack1l1l111ll1l_opy_, bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll1llll_opy_ = (
            bstack1l1l11l11ll_opy_.bstack111lll111l1_opy_
            if bstack1l1ll1l11l1_opy_[1] == TestHookState.PRE
            else bstack1l1l11l11ll_opy_.bstack11l11111l11_opy_
        )
        hook = bstack1l1l11l11ll_opy_.bstack111ll1l1l11_opy_(instance, bstack111lll1llll_opy_)
        entries = hook.get(TestFramework.bstack111ll1lll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1111lll1_opy_, []))
        return entries
    def bstack11ll11llll1_opy_(self, instance: bstack1l1l111ll1l_opy_, bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll1llll_opy_ = (
            bstack1l1l11l11ll_opy_.bstack111lll111l1_opy_
            if bstack1l1ll1l11l1_opy_[1] == TestHookState.PRE
            else bstack1l1l11l11ll_opy_.bstack11l11111l11_opy_
        )
        bstack1l1l11l11ll_opy_.bstack111ll1l1l1l_opy_(instance, bstack111lll1llll_opy_)
        TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1111lll1_opy_, []).clear()
    def bstack111lll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᪔")
        global _11lll1l1l1l_opy_
        platform_index = os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᪕")]
        bstack11lll11ll11_opy_ = os.path.join(bstack11ll1llll1l_opy_, (bstack11ll1l1llll_opy_ + str(platform_index)), bstack111ll11l111_opy_)
        if not os.path.exists(bstack11lll11ll11_opy_) or not os.path.isdir(bstack11lll11ll11_opy_):
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢ᪖").format(bstack11lll11ll11_opy_))
            return
        logs = hook.get(bstack11ll11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ᪗"), [])
        with os.scandir(bstack11lll11ll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11lll1l1l1l_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤ᪘").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll11_opy_ (u"ࠧࠨ᪙")
                    log_entry = bstack1111lll111_opy_(
                        kind=bstack11ll11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᪚"),
                        message=bstack11ll11_opy_ (u"ࠢࠣ᪛"),
                        level=bstack11ll11_opy_ (u"ࠣࠤ᪜"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11lll1111l1_opy_=entry.stat().st_size,
                        bstack11ll1llllll_opy_=bstack11ll11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ᪝"),
                        bstack1l1l1l1_opy_=os.path.abspath(entry.path),
                        bstack11l111l11l1_opy_=hook.get(TestFramework.bstack111ll1lll1l_opy_)
                    )
                    logs.append(log_entry)
                    _11lll1l1l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᪞")]
        bstack111llll1l11_opy_ = os.path.join(bstack11ll1llll1l_opy_, (bstack11ll1l1llll_opy_ + str(platform_index)), bstack111ll11l111_opy_, bstack111ll11lll1_opy_)
        if not os.path.exists(bstack111llll1l11_opy_) or not os.path.isdir(bstack111llll1l11_opy_):
            self.logger.info(bstack11ll11_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨ᪟").format(bstack111llll1l11_opy_))
        else:
            self.logger.info(bstack11ll11_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦ᪠").format(bstack111llll1l11_opy_))
            with os.scandir(bstack111llll1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11lll1l1l1l_opy_:
                        self.logger.info(bstack11ll11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦ᪡").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll11_opy_ (u"ࠢࠣ᪢")
                        log_entry = bstack1111lll111_opy_(
                            kind=bstack11ll11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᪣"),
                            message=bstack11ll11_opy_ (u"ࠤࠥ᪤"),
                            level=bstack11ll11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ᪥"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11lll1111l1_opy_=entry.stat().st_size,
                            bstack11ll1llllll_opy_=bstack11ll11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᪦"),
                            bstack1l1l1l1_opy_=os.path.abspath(entry.path),
                            bstack11lll111lll_opy_=hook.get(TestFramework.bstack111ll1lll1l_opy_)
                        )
                        logs.append(log_entry)
                        _11lll1l1l1l_opy_.add(abs_path)
        hook[bstack11ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᪧ")] = logs
    def bstack11l1l11l1_opy_(
        self,
        bstack1l1llll1_opy_: bstack1l1l111ll1l_opy_,
        entries: List[bstack1111lll111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥ᪨"))
        req.platform_index = TestFramework.bstack1ll111l1111_opy_(bstack1l1llll1_opy_, TestFramework.bstack1l111l1lll1_opy_)
        req.client_worker_id = bstack11ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ᪩").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1llll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111l1111_opy_(bstack1l1llll1_opy_, TestFramework.bstack1l111ll1111_opy_, bstack11ll11_opy_ (u"ࠣࠤ᪪"))
            log_entry.test_framework_version = TestFramework.bstack1ll111l1111_opy_(bstack1l1llll1_opy_, TestFramework.bstack11lll1l111l_opy_, bstack11ll11_opy_ (u"ࠤࠥ᪫"))
            log_entry.uuid = entry.bstack11l111l11l1_opy_ or bstack11ll11_opy_ (u"ࠥࠦ᪬")
            log_entry.test_framework_state = bstack1l1llll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᪭"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll11_opy_ (u"ࠧࠨ᪮")
            if entry.kind == bstack11ll11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᪯"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lll1111l1_opy_
                log_entry.file_path = entry.bstack1l1l1l1_opy_
        def bstack11lll11l1l1_opy_():
            bstack1l111ll1ll_opy_ = datetime.now()
            try:
                self.bstack1l1l111l1_opy_.LogCreatedEvent(req)
                bstack1l1llll1_opy_.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ᪰"), datetime.now() - bstack1l111ll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ᪱").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11ll1_opy_.enqueue(bstack11lll11l1l1_opy_)
    def __111llll111l_opy_(self, instance) -> None:
        bstack11ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᪲")
        bstack11l111lll1l_opy_ = {bstack11ll11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ᪳"): bstack1l1l1lll1l1_opy_.bstack111ll1l111l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1111llll_opy_(instance, bstack11l111lll1l_opy_)
        bstack1l1l1lll1l1_opy_.bstack11l111ll111_opy_()
    @staticmethod
    def bstack111ll1l1l11_opy_(instance: bstack1l1l111ll1l_opy_, bstack111lll1llll_opy_: str):
        bstack111lll11lll_opy_ = (
            bstack1l1l11l11ll_opy_.bstack111ll1l1ll1_opy_
            if bstack111lll1llll_opy_ == bstack1l1l11l11ll_opy_.bstack11l11111l11_opy_
            else bstack1l1l11l11ll_opy_.bstack111ll1l1111_opy_
        )
        bstack11l1111l1ll_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack111lll1llll_opy_, None)
        bstack111lllll11l_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack111lll11lll_opy_, None) if bstack11l1111l1ll_opy_ else None
        return (
            bstack111lllll11l_opy_[bstack11l1111l1ll_opy_][-1]
            if isinstance(bstack111lllll11l_opy_, dict) and len(bstack111lllll11l_opy_.get(bstack11l1111l1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack111ll1l1l1l_opy_(instance: bstack1l1l111ll1l_opy_, bstack111lll1llll_opy_: str):
        hook = bstack1l1l11l11ll_opy_.bstack111ll1l1l11_opy_(instance, bstack111lll1llll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll1lll11_opy_, []).clear()
    @staticmethod
    def __11l1111ll1l_opy_(instance: bstack1l1l111ll1l_opy_, *args):
        bstack11ll11_opy_ (u"ࠦࠧࠨࡐࡳࡱࡦࡩࡸࡹࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫ࡳࠣࠤࠥ᪴")
        if len(args) < 1:
            return
        if os.getenv(bstack11ll11_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤ᪵"), bstack11ll11_opy_ (u"ࠨ࠱᪶ࠣ")) != bstack11ll11_opy_ (u"ࠢ࠲ࠤ᪷"):
            bstack1l1l11l11ll_opy_.logger.warning(bstack11ll11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢ࡯ࡳ࡬ࡹ᪸ࠢ"))
            return
        message = args[0]
        if not hasattr(message, bstack11ll11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧ᪹ࠥ")):
            return
        is_screenshot = hasattr(message, bstack11ll11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ᪺")) and message.kind == bstack11ll11_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ᪻")
        log_entry = bstack1111lll111_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11lll111l1l_opy_,
            message=message.message if hasattr(message, bstack11ll11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨ᪼")) else bstack11ll11_opy_ (u"ࠨ᪽ࠢ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack11ll11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨ᪾")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack11ll11_opy_ (u"ࠣࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠨᪿ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack11ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴᫀࠧ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111ll1ll111_opy_ = {
            bstack11ll11_opy_ (u"ࠥࡗࡊ࡚ࡕࡑࠤ᫁"): (bstack1l1l11l11ll_opy_.bstack111lll111l1_opy_, bstack1l1l11l11ll_opy_.bstack111ll1l1111_opy_),
            bstack11ll11_opy_ (u"࡙ࠦࡋࡁࡓࡆࡒ࡛ࡓࠨ᫂"): (bstack1l1l11l11ll_opy_.bstack11l11111l11_opy_, bstack1l1l11l11ll_opy_.bstack111ll1l1ll1_opy_),
        }
        bstack111ll111lll_opy_ = None
        if len(args) > 1:
            bstack111ll111lll_opy_ = args[1]
        if bstack111ll111lll_opy_ and bstack111ll111lll_opy_ in bstack111ll1ll111_opy_:
            bstack11l111111ll_opy_, bstack111lll11lll_opy_ = bstack111ll1ll111_opy_[bstack111ll111lll_opy_]
            bstack11l111111l1_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack11l111111ll_opy_, None)
            bstack111lllll11l_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack111lll11lll_opy_, None) if bstack11l111111l1_opy_ else None
            if isinstance(bstack111lllll11l_opy_, dict) and len(bstack111lllll11l_opy_.get(bstack11l111111l1_opy_, [])) > 0:
                hook = bstack111lllll11l_opy_[bstack11l111111l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll1lll11_opy_ in hook:
                    hook[TestFramework.bstack111ll1lll11_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1111lll1_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1llllll_opy_(test) -> Dict[str, Any]:
        bstack11ll11_opy_ (u"ࠧࠨࠢࡑࡣࡵࡷࡪࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡶࡨࡷࡹࠦ࡯ࡣ࡬ࡨࡧࡹࠨ᫃ࠢࠣ")
        test_id = bstack1l1l11l11ll_opy_.__111ll111l1l_opy_(test)
        test_name = test.name if hasattr(test, bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᫄ࠦ")) else None
        bstack111llll11ll_opy_ = str(test.source) if hasattr(test, bstack11ll11_opy_ (u"ࠢࡴࡱࡸࡶࡨ࡫ࠢ᫅")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack11ll11_opy_ (u"ࠣࡶࡤ࡫ࡸࠨ᫆")) else []
        bstack111l1lllll1_opy_ =bstack11ll11_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦ᫇").format(bstack11ll11_opy_ (u"ࠥࠤࠧ᫈").join(test_tags), test_name) if test_tags else test_name
        bstack111ll11ll11_opy_ = []
        if bstack111llll11ll_opy_:
            from browserstack_sdk.bstack1llll11111l_opy_ import RobotHandler
            bstack111ll11ll11_opy_ = RobotHandler.bstack1lll1l1llll_opy_(bstack111llll11ll_opy_)
        if not bstack111ll11ll11_opy_ and test_name:
            bstack111ll11ll11_opy_ = [test_name]
        return {
            TestFramework.bstack1l111l11l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll1llll_opy_: test_id,
            TestFramework.bstack1l11111l111_opy_: test_name,
            TestFramework.bstack11ll111ll11_opy_: test_id,
            TestFramework.bstack111ll1llll1_opy_: bstack111llll11ll_opy_,
            TestFramework.bstack111llll1ll1_opy_: test_tags,
            TestFramework.bstack11l111l1l1l_opy_: bstack111l1lllll1_opy_,
            TestFramework.bstack11l1l1lll1l_opy_: TestFramework.bstack11l111l1ll1_opy_,
            TestFramework.bstack11l11ll111l_opy_: test_id,
            TestFramework.bstack111ll11ll1l_opy_: bstack111ll11ll11_opy_
        }
    @staticmethod
    def __111ll111l1l_opy_(test):
        bstack11ll11_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡹࡳ࡯ࡱࡶࡧࠣࡸࡪࡹࡴࠡࡋࡇࠤ࡫ࡸ࡯࡮ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡹ࡫ࡳࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦ᫉")
        if hasattr(test, bstack11ll11_opy_ (u"ࠧ࡯ࡤ᫊ࠣ")):
            return test.id
        elif hasattr(test, bstack11ll11_opy_ (u"ࠨ࡬ࡰࡰࡪࡲࡦࡳࡥࠣ᫋")):
            return test.longname
        elif hasattr(test, bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᫌ")):
            return test.name
        return None