# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll11111l_opy_ import bstack1l1ll1l1l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack111ll11l1_opy_ import bstack111lll11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11l11ll_opy_,
    TestHookState,
    bstack1ll1ll1ll11_opy_,
    bstack111l1111ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11lll1l1111_opy_
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l111lll_opy_ import bstack1l11lll1lll_opy_
from bstack_utils.bstack1l1l11l1_opy_ import bstack111l111ll1_opy_
bstack11ll11ll111_opy_ = bstack11lll1l1111_opy_()
bstack111lll1ll11_opy_ = 1.0
bstack11lll111lll_opy_ = bstack1ll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᩀ")
bstack111ll111ll1_opy_ = bstack1ll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᩁ")
bstack111ll11l1l1_opy_ = bstack1ll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᩂ")
bstack111ll1111ll_opy_ = bstack1ll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᩃ")
bstack111ll111l11_opy_ = bstack1ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᩄ")
_11ll11l1l11_opy_ = set()
class bstack1l1l1111l1l_opy_(TestFramework):
    bstack111l1llllll_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᩅ")
    bstack111ll11l1ll_opy_ = bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᩆ")
    bstack111lll111l1_opy_ = bstack1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᩇ")
    bstack111llll1l1l_opy_ = bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᩈ")
    bstack111ll1l1lll_opy_ = bstack1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᩉ")
    bstack111ll11111l_opy_: bool
    bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_ = None
    bstack1ll11ll11l_opy_ = None
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1ll1l_opy_: Dict[str, str],
        bstack1l1l111111l_opy_: List[str] = [bstack1ll_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦᩊ")],
        bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_ = None,
        bstack1ll11ll11l_opy_=None
    ):
        super().__init__(bstack1l1l111111l_opy_, bstack1l11ll1ll1l_opy_, bstack1l1lll11ll1_opy_)
        self.bstack111ll11111l_opy_ = any(bstack1ll_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥᩋ") in item.lower() for item in bstack1l1l111111l_opy_)
        self.bstack1ll11ll11l_opy_ = bstack1ll11ll11l_opy_
    def track_event(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l1111l1l_opy_.bstack111ll1l1l1l_opy_:
            bstack111lll11l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤᩌ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111ll11111l_opy_:
            self.logger.warning(bstack1ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࡻࡾࠤᩍ").format(str(self.bstack1l1l111111l_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᩎ").format(args, kwargs))
            return
        instance = self.__111ll1l1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠤᩏ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1l1111l1l_opy_.bstack111ll1l1l1l_opy_:
                bstack1lll1lll11_opy_ = bstack1ll_opy_ (u"ࠤࠥᩐ")
                name = bstack1ll_opy_ (u"ࠥࠦᩑ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111ll111lll_opy_.value)
                    name = str(EVENTS.bstack111ll111lll_opy_.name) + bstack1ll_opy_ (u"ࠦ࠿ࠨᩒ") + str(test_framework_state.name)
                else:
                    bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111ll11l111_opy_.value)
                    name = str(EVENTS.bstack111ll11l111_opy_.name) + bstack1ll_opy_ (u"ࠧࡀࠢᩓ") + str(test_framework_state.name)
                TestFramework.bstack11l1111l1l1_opy_(instance, name, bstack1lll1lll11_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᩔ").format(e))
        try:
            if not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11l1ll11111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l1111l1l_opy_.__111l1lll1l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥᩕ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤᩖ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11lll111111_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11lll111111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣᩗ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l1111l1l_opy_.__111llll1lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll11ll1_opy_(instance, *args)
                self.__11l11111l11_opy_(instance)
            elif test_framework_state in bstack1l1l1111l1l_opy_.bstack111ll1l1l1l_opy_:
                self.__111ll1ll11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠨᩘ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111ll1ll1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1l1111l1l_opy_.bstack111ll1l1l1l_opy_:
                bstack1lll1lll11_opy_ = bstack1ll_opy_ (u"ࠦࠧᩙ")
                name = bstack1ll_opy_ (u"ࠧࠨᩚ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll111lll_opy_.name) + bstack1ll_opy_ (u"ࠨ࠺ࠣᩛ") + str(test_framework_state.name)
                    bstack1lll1lll11_opy_ = TestFramework.bstack111ll1ll111_opy_(instance, name)
                    bstack1l11l1ll11_opy_.end(EVENTS.bstack111ll111lll_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᩜ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᩝ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll11l111_opy_.name) + bstack1ll_opy_ (u"ࠤ࠽ࠦᩞ") + str(test_framework_state.name)
                    bstack1lll1lll11_opy_ = TestFramework.bstack111ll1ll111_opy_(instance, name)
                    bstack1l11l1ll11_opy_.end(EVENTS.bstack111ll11l111_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᩟"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᩠"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᩡ").format(e))
    def bstack11ll1ll1l11_opy_(self):
        return self.bstack111ll11111l_opy_
    def bstack11ll1l11lll_opy_(self):
        return False
    def __111l1lll1ll_opy_(self, *args):
        bstack1ll_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡵࡩࡸࡻ࡬ࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦᩢ")
        if len(args) > 1 and hasattr(args[1], bstack1ll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᩣ")):
            result = args[1]
            if result:
                return TestFramework.bstack11lll11llll_opy_(result, [bstack1ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᩤ"), bstack1ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᩥ"), bstack1ll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡶ࡬ࡱࡪࠨᩦ"), bstack1ll_opy_ (u"ࠦࡪࡴࡤࡵ࡫ࡰࡩࠧᩧ"), bstack1ll_opy_ (u"ࠧ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠥᩨ")])
        return None
    def __111lll11ll1_opy_(self, instance: bstack1l1l11l11ll_opy_, *args):
        result = self.__111l1lll1ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1lll_opy_ = None
        status = result.get(bstack1ll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᩩ"), bstack1ll_opy_ (u"ࠢࡏࡑࡗࠤࡗ࡛ࡎࠣᩪ"))
        if status == bstack1ll_opy_ (u"ࠣࡈࡄࡍࡑࠨᩫ") and result.get(bstack1ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᩬ")):
            failure = [{bstack1ll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᩭ"): [result.get(bstack1ll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᩮ"), bstack1ll_opy_ (u"ࠧࠨᩯ"))]}]
            bstack1ll111l1lll_opy_ = bstack1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᩰ")
        bstack111lll1l1l1_opy_ = TestFramework.bstack11l111ll111_opy_
        if status == bstack1ll_opy_ (u"ࠢࡑࡃࡖࡗࠧᩱ"):
            bstack111lll1l1l1_opy_ = bstack1ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᩲ")
        elif status == bstack1ll_opy_ (u"ࠤࡉࡅࡎࡒࠢᩳ"):
            bstack111lll1l1l1_opy_ = bstack1ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᩴ")
        elif status == bstack1ll_opy_ (u"ࠦࡘࡑࡉࡑࠤ᩵"):
            bstack111lll1l1l1_opy_ = bstack1ll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨ᩶")
        if bstack111lll1l1l1_opy_ != TestFramework.bstack11l111ll111_opy_:
            TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack111lllllll1_opy_(instance, {
            TestFramework.bstack11l1ll11l11_opy_: failure,
            TestFramework.bstack111ll1l1l11_opy_: bstack1ll111l1lll_opy_,
            TestFramework.bstack11l1ll11lll_opy_: bstack111lll1l1l1_opy_,
        })
    def __111ll1l1ll1_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111l1llll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111ll1111l1_opy_(test) if test else None
                if target:
                    self.__111l1lllll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢ᩷"), None)
            elif hasattr(args[0], bstack1ll_opy_ (u"ࠢࡪࡦࠥ᩸")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1l1ll1lll1l_opy_(target) if target else None
        return instance
    def __111ll1ll11l_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l111111ll_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1l1l1111l1l_opy_.bstack111ll11l1ll_opy_, {})
        if not key in bstack11l111111ll_opy_:
            bstack11l111111ll_opy_[key] = []
        bstack111lll1lll1_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1l1l1111l1l_opy_.bstack111lll111l1_opy_, {})
        if not key in bstack111lll1lll1_opy_:
            bstack111lll1lll1_opy_[key] = []
        bstack111lll11111_opy_ = {
            bstack1l1l1111l1l_opy_.bstack111ll11l1ll_opy_: bstack11l111111ll_opy_,
            bstack1l1l1111l1l_opy_.bstack111lll111l1_opy_: bstack111lll1lll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1ll_opy_ (u"ࠣࠤ᩹")
            if len(args) > 0 and hasattr(args[0], bstack1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᩺")):
                hook_name = args[0].name
            hook = {
                bstack1ll_opy_ (u"ࠥ࡯ࡪࡿࠢ᩻"): key,
                TestFramework.bstack111lllll111_opy_: uuid4().__str__(),
                TestFramework.bstack11l1111lll1_opy_: TestFramework.bstack11l1111ll1l_opy_,
                TestFramework.bstack11l11111ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l11ll_opy_: [],
                TestFramework.bstack111ll1llll1_opy_: hook_name,
                TestFramework.bstack11l111l1ll1_opy_: bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()
            }
            bstack11l111111ll_opy_[key].append(hook)
            bstack111lll11111_opy_[bstack1l1l1111l1l_opy_.bstack111llll1l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111lll1llll_opy_ = bstack11l111111ll_opy_.get(key, [])
            hook = bstack111lll1llll_opy_.pop() if bstack111lll1llll_opy_ else None
            if hook:
                result = self.__111l1lll1ll_opy_(*args)
                if result:
                    bstack11l11111l1l_opy_ = result.get(bstack1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᩼"), TestFramework.bstack11l1111ll1l_opy_)
                    if bstack11l11111l1l_opy_ == bstack1ll_opy_ (u"ࠧࡖࡁࡔࡕࠥ᩽"):
                        bstack11l11111l1l_opy_ = bstack1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ᩾")
                    elif bstack11l11111l1l_opy_ == bstack1ll_opy_ (u"ࠢࡇࡃࡌࡐ᩿ࠧ"):
                        bstack11l11111l1l_opy_ = bstack1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ᪀")
                    if bstack11l11111l1l_opy_ != TestFramework.bstack11l1111ll1l_opy_:
                        hook[TestFramework.bstack11l1111lll1_opy_] = bstack11l11111l1l_opy_
                hook[TestFramework.bstack111lllll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l111l1ll1_opy_] = bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()
                self.bstack111lll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111llll1111_opy_, [])
                if logs:
                    self.bstack11lll1lll1_opy_(instance, logs)
                bstack111lll1lll1_opy_[key].append(hook)
                bstack111lll11111_opy_[bstack1l1l1111l1l_opy_.bstack111ll1l1lll_opy_] = key
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀ࠲ࢀࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࢀࢃࠢ᪁").format(key, test_hook_state, bstack11l111111ll_opy_, bstack111lll1lll1_opy_))
    def __111l1llll1l_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll_opy_ (u"࡚ࠥࠦࠧࡲࡢࡥ࡮ࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡦࡸࡨࡲࡹࡹࠠࠩࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࠣࠤࠥ᪂")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪃"), None)
        bstack1ll111l1l11_opy_ = getattr(keyword, bstack1ll_opy_ (u"ࠧࡺࡹࡱࡧࠥ᪄"), None)
        test_id = kwargs.get(bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢ᪅"), None)
        if not test_id:
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥ࡫ࡦࡻࡺࡳࡷࡪ࡟ࡦࡸࡨࡲࡹࡀࠠ࡯ࡱࠣࡸࡪࡹࡴࡠ࡫ࡧࠤ࡮ࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠤ᪆").format(keyword_name))
            return None
        instance = TestFramework.bstack1l1ll1lll1l_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟࡬ࡧࡼࡻࡴࡸࡤࡠࡧࡹࡩࡳࡺ࠺ࠡࡰࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡷࡩࡸࡺ࡟ࡪࡦࡀࡿࢂࠨ᪇").format(test_id))
            return None
        bstack111l1lll11l_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1l1l1111l1l_opy_.bstack111l1llllll_opy_, {})
        if os.getenv(bstack1ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡍࡈ࡝࡜ࡕࡒࡅࡕࠥ᪈"), bstack1ll_opy_ (u"ࠥ࠵ࠧ᪉")) == bstack1ll_opy_ (u"ࠦ࠶ࠨ᪊"):
            bstack111ll111111_opy_ = bstack1ll_opy_ (u"ࠧࢁࡽ࠻ࡽࢀࠦ᪋").format(bstack1ll111l1l11_opy_, keyword_name)
            bstack11l111l1l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1ll1lll_opy_ = {
                bstack1ll_opy_ (u"ࠨ࡫ࡦࡻࠥ᪌"): bstack111ll111111_opy_,
                bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪍"): keyword_name,
                bstack1ll_opy_ (u"ࠣࡶࡼࡴࡪࠨ᪎"): bstack1ll111l1l11_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l1ll1lll_opy_[bstack1ll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ᪏")] = uuid4().__str__()
                bstack111l1ll1lll_opy_[bstack1l1l1111l1l_opy_.bstack11l11111ll1_opy_] = bstack11l111l1l1l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1ll1lll_opy_[bstack1l1l1111l1l_opy_.bstack111lllll1ll_opy_] = bstack11l111l1l1l_opy_
                if len(args) > 1 and hasattr(args[1], bstack1ll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᪐")):
                    bstack111l1ll1lll_opy_[bstack1ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᪑")] = args[1].status
            if bstack111ll111111_opy_ in bstack111l1lll11l_opy_:
                bstack111l1lll11l_opy_[bstack111ll111111_opy_].update(bstack111l1ll1lll_opy_)
                self.logger.debug(bstack1ll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠣࡸࡾࡶࡥ࠾ࡽࢀࠦ᪒").format(keyword_name, bstack1ll111l1l11_opy_))
            else:
                bstack111l1lll11l_opy_[bstack111ll111111_opy_] = bstack111l1ll1lll_opy_
                self.logger.debug(bstack1ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠢࡷࡽࡵ࡫࠽ࡼࡿࠥ᪓").format(keyword_name, bstack1ll111l1l11_opy_))
        TestFramework.bstack1l1l1l1l_opy_(instance, bstack1l1l1111l1l_opy_.bstack111l1llllll_opy_, bstack111l1lll11l_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪࡳ࠾ࡽࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠤ᪔").format(len(bstack111l1lll11l_opy_), instance.ref()))
        return instance
    def __111l1lllll1_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l11_opy_.create_context(target)
        ob = bstack1l1l11l11ll_opy_(ctx, self.bstack1l1l111111l_opy_, self.bstack1l11ll1ll1l_opy_, test_framework_state)
        TestFramework.bstack111lllllll1_opy_(ob, {
            TestFramework.bstack1l11111111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11ll_opy_: context.test_framework_version,
            TestFramework.bstack111ll11llll_opy_: [],
            bstack1l1l1111l1l_opy_.bstack111l1llllll_opy_: {},
            bstack1l1l1111l1l_opy_.bstack111lll111l1_opy_: {},
            bstack1l1l1111l1l_opy_.bstack111ll11l1ll_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1ll_opy_ (u"ࠣࡵࡲࡹࡷࡩࡥࠣ᪕")):
            TestFramework.bstack1l1l1l1l_opy_(ob, TestFramework.bstack111lll1ll1l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1l1l1l1l_opy_(ob, TestFramework.bstack1l1111l11l1_opy_, context.platform_index)
        TestFramework.bstack1l111l11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࡻࡾࠤ᪖").format(ctx.id, target, args, TestFramework.bstack1l111l11l_opy_.keys()))
        return ob
    def bstack11ll11llll1_opy_(self, instance: bstack1l1l11l11ll_opy_, bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            bstack1l1l1111l1l_opy_.bstack111llll1l1l_opy_
            if bstack1l1ll1lll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1111l1l_opy_.bstack111ll1l1lll_opy_
        )
        hook = bstack1l1l1111l1l_opy_.bstack111lll1111l_opy_(instance, bstack11l11111111_opy_)
        entries = hook.get(TestFramework.bstack11l111l11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, []))
        return entries
    def bstack11ll1l1lll1_opy_(self, instance: bstack1l1l11l11ll_opy_, bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            bstack1l1l1111l1l_opy_.bstack111llll1l1l_opy_
            if bstack1l1ll1lll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1111l1l_opy_.bstack111ll1l1lll_opy_
        )
        bstack1l1l1111l1l_opy_.bstack11l1111llll_opy_(instance, bstack11l11111111_opy_)
        TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, []).clear()
    def bstack111lll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᪗")
        global _11ll11l1l11_opy_
        platform_index = os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᪘")]
        bstack11ll11l1ll1_opy_ = os.path.join(bstack11ll11ll111_opy_, (bstack11lll111lll_opy_ + str(platform_index)), bstack111ll1111ll_opy_)
        if not os.path.exists(bstack11ll11l1ll1_opy_) or not os.path.isdir(bstack11ll11l1ll1_opy_):
            self.logger.debug(bstack1ll_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥ᪙").format(bstack11ll11l1ll1_opy_))
            return
        logs = hook.get(bstack1ll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦ᪚"), [])
        with os.scandir(bstack11ll11l1ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll11l1l11_opy_:
                    self.logger.info(bstack1ll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧ᪛").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll_opy_ (u"ࠣࠤ᪜")
                    log_entry = bstack111l1111ll_opy_(
                        kind=bstack1ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᪝"),
                        message=bstack1ll_opy_ (u"ࠥࠦ᪞"),
                        level=bstack1ll_opy_ (u"ࠦࠧ᪟"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1ll1111_opy_=entry.stat().st_size,
                        bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧ᪠"),
                        bstack1ll11l1_opy_=os.path.abspath(entry.path),
                        bstack11l111l111l_opy_=hook.get(TestFramework.bstack111lllll111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll11l1l11_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᪡")]
        bstack111lllll1l1_opy_ = os.path.join(bstack11ll11ll111_opy_, (bstack11lll111lll_opy_ + str(platform_index)), bstack111ll1111ll_opy_, bstack111ll111l11_opy_)
        if not os.path.exists(bstack111lllll1l1_opy_) or not os.path.isdir(bstack111lllll1l1_opy_):
            self.logger.info(bstack1ll_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤ᪢").format(bstack111lllll1l1_opy_))
        else:
            self.logger.info(bstack1ll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢ᪣").format(bstack111lllll1l1_opy_))
            with os.scandir(bstack111lllll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll11l1l11_opy_:
                        self.logger.info(bstack1ll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ᪤").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll_opy_ (u"ࠥࠦ᪥")
                        log_entry = bstack111l1111ll_opy_(
                            kind=bstack1ll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᪦"),
                            message=bstack1ll_opy_ (u"ࠧࠨᪧ"),
                            level=bstack1ll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ᪨"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1ll1111_opy_=entry.stat().st_size,
                            bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ᪩"),
                            bstack1ll11l1_opy_=os.path.abspath(entry.path),
                            bstack11lll1l11l1_opy_=hook.get(TestFramework.bstack111lllll111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll11l1l11_opy_.add(abs_path)
        hook[bstack1ll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᪪")] = logs
    def bstack11lll1lll1_opy_(
        self,
        bstack111111l1l1_opy_: bstack1l1l11l11ll_opy_,
        entries: List[bstack111l1111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨ᪫"))
        req.platform_index = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l1111l11l1_opy_)
        req.client_worker_id = bstack1ll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᪬").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack111111l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack111111l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack111111l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l11111111l_opy_, bstack1ll_opy_ (u"ࠦࠧ᪭"))
            log_entry.test_framework_version = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack11ll11l11ll_opy_, bstack1ll_opy_ (u"ࠧࠨ᪮"))
            log_entry.uuid = entry.bstack11l111l111l_opy_ or bstack1ll_opy_ (u"ࠨࠢ᪯")
            log_entry.test_framework_state = bstack111111l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᪰"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll_opy_ (u"ࠣࠤ᪱")
            if entry.kind == bstack1ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᪲"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1ll1111_opy_
                log_entry.file_path = entry.bstack1ll11l1_opy_
        def bstack11ll1l111l1_opy_():
            bstack1l1111ll_opy_ = datetime.now()
            try:
                self.bstack1ll11ll11l_opy_.LogCreatedEvent(req)
                bstack111111l1l1_opy_.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ᪳"), datetime.now() - bstack1l1111ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥ᪴").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11ll1_opy_.enqueue(bstack11ll1l111l1_opy_)
    def __11l11111l11_opy_(self, instance) -> None:
        bstack1ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤ᪵ࠥ")
        bstack111lll11111_opy_ = {bstack1ll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡ᪶ࠣ"): bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        bstack1l11lll1lll_opy_.bstack111llll11l1_opy_()
    @staticmethod
    def bstack111lll1111l_opy_(instance: bstack1l1l11l11ll_opy_, bstack11l11111111_opy_: str):
        bstack111lll1l1ll_opy_ = (
            bstack1l1l1111l1l_opy_.bstack111lll111l1_opy_
            if bstack11l11111111_opy_ == bstack1l1l1111l1l_opy_.bstack111ll1l1lll_opy_
            else bstack1l1l1111l1l_opy_.bstack111ll11l1ll_opy_
        )
        bstack111ll1l1111_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack11l11111111_opy_, None)
        bstack111ll11ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll1l1ll_opy_, None) if bstack111ll1l1111_opy_ else None
        return (
            bstack111ll11ll11_opy_[bstack111ll1l1111_opy_][-1]
            if isinstance(bstack111ll11ll11_opy_, dict) and len(bstack111ll11ll11_opy_.get(bstack111ll1l1111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111llll_opy_(instance: bstack1l1l11l11ll_opy_, bstack11l11111111_opy_: str):
        hook = bstack1l1l1111l1l_opy_.bstack111lll1111l_opy_(instance, bstack11l11111111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l111l11ll_opy_, []).clear()
    @staticmethod
    def __111llll1lll_opy_(instance: bstack1l1l11l11ll_opy_, *args):
        bstack1ll_opy_ (u"ࠢࠣࠤࡓࡶࡴࡩࡥࡴࡵࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࡶࠦࠧࠨ᪷")
        if len(args) < 1:
            return
        if os.getenv(bstack1ll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗ᪸ࠧ"), bstack1ll_opy_ (u"ࠤ࠴᪹ࠦ")) != bstack1ll_opy_ (u"ࠥ࠵᪺ࠧ"):
            bstack1l1l1111l1l_opy_.logger.warning(bstack1ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡲ࡯ࡨࡵࠥ᪻"))
            return
        message = args[0]
        if not hasattr(message, bstack1ll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨ᪼")):
            return
        is_screenshot = hasattr(message, bstack1ll_opy_ (u"࠭࡫ࡪࡰࡧ᪽ࠫ")) and message.kind == bstack1ll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᪾")
        log_entry = bstack111l1111ll_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11ll11ll11l_opy_,
            message=message.message if hasattr(message, bstack1ll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᪿ")) else bstack1ll_opy_ (u"ࠤᫀࠥ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1ll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤ᫁")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1ll_opy_ (u"ࠦࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠤ᫂")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1ll_opy_ (u"ࠧࡺࡩ࡮ࡧࡶࡸࡦࡳࡰ᫃ࠣ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111lll11lll_opy_ = {
            bstack1ll_opy_ (u"ࠨࡓࡆࡖࡘࡔ᫄ࠧ"): (bstack1l1l1111l1l_opy_.bstack111llll1l1l_opy_, bstack1l1l1111l1l_opy_.bstack111ll11l1ll_opy_),
            bstack1ll_opy_ (u"ࠢࡕࡇࡄࡖࡉࡕࡗࡏࠤ᫅"): (bstack1l1l1111l1l_opy_.bstack111ll1l1lll_opy_, bstack1l1l1111l1l_opy_.bstack111lll111l1_opy_),
        }
        bstack111l1lll111_opy_ = None
        if len(args) > 1:
            bstack111l1lll111_opy_ = args[1]
        if bstack111l1lll111_opy_ and bstack111l1lll111_opy_ in bstack111lll11lll_opy_:
            bstack111lll11l1l_opy_, bstack111lll1l1ll_opy_ = bstack111lll11lll_opy_[bstack111l1lll111_opy_]
            bstack11l1111ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll11l1l_opy_, None)
            bstack111ll11ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll1l1ll_opy_, None) if bstack11l1111ll11_opy_ else None
            if isinstance(bstack111ll11ll11_opy_, dict) and len(bstack111ll11ll11_opy_.get(bstack11l1111ll11_opy_, [])) > 0:
                hook = bstack111ll11ll11_opy_[bstack11l1111ll11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l111l11ll_opy_ in hook:
                    hook[TestFramework.bstack11l111l11ll_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1lll1l1_opy_(test) -> Dict[str, Any]:
        bstack1ll_opy_ (u"ࠣࠤࠥࡔࡦࡸࡳࡦࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡹ࡫ࡳࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦ᫆")
        test_id = bstack1l1l1111l1l_opy_.__111ll1111l1_opy_(test)
        test_name = test.name if hasattr(test, bstack1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫇")) else None
        bstack111llllll1l_opy_ = str(test.source) if hasattr(test, bstack1ll_opy_ (u"ࠥࡷࡴࡻࡲࡤࡧࠥ᫈")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1ll_opy_ (u"ࠦࡹࡧࡧࡴࠤ᫉")) else []
        bstack111l1llll11_opy_ =bstack1ll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃ᫊ࠢ").format(bstack1ll_opy_ (u"ࠨࠠࠣ᫋").join(test_tags), test_name) if test_tags else test_name
        bstack111ll111l1l_opy_ = []
        if bstack111llllll1l_opy_:
            from browserstack_sdk.bstack1lll1l1l1l1_opy_ import RobotHandler
            bstack111ll111l1l_opy_ = RobotHandler.bstack1lll11ll111_opy_(bstack111llllll1l_opy_)
        if not bstack111ll111l1l_opy_ and test_name:
            bstack111ll111l1l_opy_ = [test_name]
        return {
            TestFramework.bstack1l1111ll1l1_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll11111_opy_: test_id,
            TestFramework.bstack1l111111lll_opy_: test_name,
            TestFramework.bstack11ll111l1ll_opy_: test_id,
            TestFramework.bstack111llllllll_opy_: bstack111llllll1l_opy_,
            TestFramework.bstack11l111l1l11_opy_: test_tags,
            TestFramework.bstack111ll1ll1ll_opy_: bstack111l1llll11_opy_,
            TestFramework.bstack11l1ll11lll_opy_: TestFramework.bstack11l111ll111_opy_,
            TestFramework.bstack11l11l1l1ll_opy_: test_id,
            TestFramework.bstack111ll11l11l_opy_: bstack111ll111l1l_opy_
        }
    @staticmethod
    def __111ll1111l1_opy_(test):
        bstack1ll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡵ࡯࡫ࡴࡹࡪࠦࡴࡦࡵࡷࠤࡎࡊࠠࡧࡴࡲࡱࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡵࡧࡶࡸࠥࡵࡢ࡫ࡧࡦࡸࠧࠨࠢᫌ")
        if hasattr(test, bstack1ll_opy_ (u"ࠣ࡫ࡧࠦᫍ")):
            return test.id
        elif hasattr(test, bstack1ll_opy_ (u"ࠤ࡯ࡳࡳ࡭࡮ࡢ࡯ࡨࠦᫎ")):
            return test.longname
        elif hasattr(test, bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫏")):
            return test.name
        return None