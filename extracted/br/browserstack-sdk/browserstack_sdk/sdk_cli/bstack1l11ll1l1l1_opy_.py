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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l1ll111_opy_,
    TestHookState,
    bstack1ll1lll111l_opy_,
    bstack11lll1ll1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11lll11111l_opy_
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll111l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11ll1_opy_ import bstack1l1l1l1lll1_opy_
from bstack_utils.bstack11l1l111l_opy_ import bstack1l1lll1l1_opy_
bstack11lll11l1ll_opy_ = bstack11lll11111l_opy_()
bstack111llllll1l_opy_ = 1.0
bstack11ll111ll11_opy_ = bstack1l1111l_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᩛ")
bstack111ll1111l1_opy_ = bstack1l1111l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᩜ")
bstack111l1llllll_opy_ = bstack1l1111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᩝ")
bstack111ll111111_opy_ = bstack1l1111l_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᩞ")
bstack111ll1111ll_opy_ = bstack1l1111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ᩟")
_11ll111llll_opy_ = set()
class bstack1l1l1l1l111_opy_(TestFramework):
    bstack111l1lll1l1_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡶ᩠ࠦ")
    bstack111lll11l1l_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᩡ")
    bstack111ll1l1ll1_opy_ = bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᩢ")
    bstack111lllll111_opy_ = bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᩣ")
    bstack111ll1l11l1_opy_ = bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᩤ")
    bstack111l1llll1l_opy_: bool
    bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_ = None
    bstack11l1ll1lll_opy_ = None
    bstack111ll11ll11_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1l1l1lll111_opy_: List[str] = [bstack1l1111l_opy_ (u"ࠤࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᩥ")],
        bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_ = None,
        bstack11l1ll1lll_opy_=None
    ):
        super().__init__(bstack1l1l1lll111_opy_, bstack1l111lllll1_opy_, bstack1l1lll11l1l_opy_)
        self.bstack111l1llll1l_opy_ = any(bstack1l1111l_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࠤᩦ") in item.lower() for item in bstack1l1l1lll111_opy_)
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
    def track_event(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l1l1l111_opy_.bstack111ll11ll11_opy_:
            bstack11l111l111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᩧ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111l1llll1l_opy_:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࢁࡽࠣᩨ").format(str(self.bstack1l1l1lll111_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᩩ").format(args, kwargs))
            return
        instance = self.__11l111l1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠣᩪ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1l1l1l111_opy_.bstack111ll11ll11_opy_:
                bstack1l11l1l11_opy_ = bstack1l1111l_opy_ (u"ࠣࠤᩫ")
                name = bstack1l1111l_opy_ (u"ࠤࠥᩬ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111ll111l1l_opy_.value)
                    name = str(EVENTS.bstack111ll111l1l_opy_.name) + bstack1l1111l_opy_ (u"ࠥ࠾ࠧᩭ") + str(test_framework_state.name)
                else:
                    bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111ll111l11_opy_.value)
                    name = str(EVENTS.bstack111ll111l11_opy_.name) + bstack1l1111l_opy_ (u"ࠦ࠿ࠨᩮ") + str(test_framework_state.name)
                TestFramework.bstack111lll11ll1_opy_(instance, name, bstack1l11l1l11_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᩯ").format(e))
        try:
            if not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11l1ll11111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l1l1l111_opy_.__111l1ll1l11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤᩰ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11lll1111ll_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11lll1111ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣᩱ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢᩲ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l1l1l111_opy_.__11l111111l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll11111_opy_(instance, *args)
                self.__11l1111llll_opy_(instance)
            elif test_framework_state in bstack1l1l1l1l111_opy_.bstack111ll11ll11_opy_:
                self.__111ll1l1111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠧᩳ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111lllll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1l1l1l111_opy_.bstack111ll11ll11_opy_:
                bstack1l11l1l11_opy_ = bstack1l1111l_opy_ (u"ࠥࠦᩴ")
                name = bstack1l1111l_opy_ (u"ࠦࠧ᩵")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll111l1l_opy_.name) + bstack1l1111l_opy_ (u"ࠧࡀࠢ᩶") + str(test_framework_state.name)
                    bstack1l11l1l11_opy_ = TestFramework.bstack111ll1l1l11_opy_(instance, name)
                    bstack11lll1111_opy_.end(EVENTS.bstack111ll111l1l_opy_.value, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᩷"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᩸"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll111l11_opy_.name) + bstack1l1111l_opy_ (u"ࠣ࠼ࠥ᩹") + str(test_framework_state.name)
                    bstack1l11l1l11_opy_ = TestFramework.bstack111ll1l1l11_opy_(instance, name)
                    bstack11lll1111_opy_.end(EVENTS.bstack111ll111l11_opy_.value, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᩺"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᩻"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᩼").format(e))
    def bstack11ll1l11l1l_opy_(self):
        return self.bstack111l1llll1l_opy_
    def bstack11ll11l111l_opy_(self):
        return False
    def __111l1llll11_opy_(self, *args):
        bstack1l1111l_opy_ (u"ࠧࠨࠢࡑࡣࡵࡷࡪࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡴࡨࡷࡺࡲࡴࠡࡱࡥ࡮ࡪࡩࡴࠣࠤࠥ᩽")
        if len(args) > 1 and hasattr(args[1], bstack1l1111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᩾")):
            result = args[1]
            if result:
                return TestFramework.bstack11ll1lll1l1_opy_(result, [bstack1l1111l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹ᩿ࠢ"), bstack1l1111l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ᪀"), bstack1l1111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡵ࡫ࡰࡩࠧ᪁"), bstack1l1111l_opy_ (u"ࠥࡩࡳࡪࡴࡪ࡯ࡨࠦ᪂"), bstack1l1111l_opy_ (u"ࠦࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠤ᪃")])
        return None
    def __111lll11111_opy_(self, instance: bstack1l11l1ll111_opy_, *args):
        result = self.__111l1llll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        status = result.get(bstack1l1111l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᪄"), bstack1l1111l_opy_ (u"ࠨࡎࡐࡖࠣࡖ࡚ࡔࠢ᪅"))
        if status == bstack1l1111l_opy_ (u"ࠢࡇࡃࡌࡐࠧ᪆") and result.get(bstack1l1111l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ᪇")):
            failure = [{bstack1l1111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ᪈"): [result.get(bstack1l1111l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ᪉"), bstack1l1111l_opy_ (u"ࠦࠧ᪊"))]}]
            bstack1ll111l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ᪋")
        bstack111ll11l111_opy_ = TestFramework.bstack111lll1l1ll_opy_
        if status == bstack1l1111l_opy_ (u"ࠨࡐࡂࡕࡖࠦ᪌"):
            bstack111ll11l111_opy_ = bstack1l1111l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ᪍")
        elif status == bstack1l1111l_opy_ (u"ࠣࡈࡄࡍࡑࠨ᪎"):
            bstack111ll11l111_opy_ = bstack1l1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᪏")
        elif status == bstack1l1111l_opy_ (u"ࠥࡗࡐࡏࡐࠣ᪐"):
            bstack111ll11l111_opy_ = bstack1l1111l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧ᪑")
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
            instance = self.__111l1ll1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111l1lll11l_opy_(test) if test else None
                if target:
                    self.__111l1ll1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨ᪒"), None)
            elif hasattr(args[0], bstack1l1111l_opy_ (u"ࠨࡩࡥࠤ᪓")) if len(args) > 0 else False:
                target = args[0].id
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
        bstack111lll1l111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l1l1l1l111_opy_.bstack111lll11l1l_opy_, {})
        if not key in bstack111lll1l111_opy_:
            bstack111lll1l111_opy_[key] = []
        bstack111llllllll_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l1l1l1l111_opy_.bstack111ll1l1ll1_opy_, {})
        if not key in bstack111llllllll_opy_:
            bstack111llllllll_opy_[key] = []
        bstack111llllll11_opy_ = {
            bstack1l1l1l1l111_opy_.bstack111lll11l1l_opy_: bstack111lll1l111_opy_,
            bstack1l1l1l1l111_opy_.bstack111ll1l1ll1_opy_: bstack111llllllll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1l1111l_opy_ (u"ࠢࠣ᪔")
            if len(args) > 0 and hasattr(args[0], bstack1l1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪕")):
                hook_name = args[0].name
            hook = {
                bstack1l1111l_opy_ (u"ࠤ࡮ࡩࡾࠨ᪖"): key,
                TestFramework.bstack11l1111l111_opy_: uuid4().__str__(),
                TestFramework.bstack111lll111ll_opy_: TestFramework.bstack111ll1lll11_opy_,
                TestFramework.bstack111ll11lll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll111lll_opy_: [],
                TestFramework.bstack11l1111ll1l_opy_: hook_name,
                TestFramework.bstack111lll1llll_opy_: bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()
            }
            bstack111lll1l111_opy_[key].append(hook)
            bstack111llllll11_opy_[bstack1l1l1l1l111_opy_.bstack111lllll111_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llll1lll_opy_ = bstack111lll1l111_opy_.get(key, [])
            hook = bstack111llll1lll_opy_.pop() if bstack111llll1lll_opy_ else None
            if hook:
                result = self.__111l1llll11_opy_(*args)
                if result:
                    bstack11l1111l1l1_opy_ = result.get(bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᪗"), TestFramework.bstack111ll1lll11_opy_)
                    if bstack11l1111l1l1_opy_ == bstack1l1111l_opy_ (u"ࠦࡕࡇࡓࡔࠤ᪘"):
                        bstack11l1111l1l1_opy_ = bstack1l1111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ᪙")
                    elif bstack11l1111l1l1_opy_ == bstack1l1111l_opy_ (u"ࠨࡆࡂࡋࡏࠦ᪚"):
                        bstack11l1111l1l1_opy_ = bstack1l1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ᪛")
                    if bstack11l1111l1l1_opy_ != TestFramework.bstack111ll1lll11_opy_:
                        hook[TestFramework.bstack111lll111ll_opy_] = bstack11l1111l1l1_opy_
                hook[TestFramework.bstack11l111111ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111lll1llll_opy_] = bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()
                self.bstack11l1111l1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111llll1l1l_opy_, [])
                if logs:
                    self.bstack1llll111ll_opy_(instance, logs)
                bstack111llllllll_opy_[key].append(hook)
                bstack111llllll11_opy_[bstack1l1l1l1l111_opy_.bstack111ll1l11l1_opy_] = key
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿ࠱ࡿࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࡿࢂࠨ᪜").format(key, test_hook_state, bstack111lll1l111_opy_, bstack111llllllll_opy_))
    def __111l1ll1ll1_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1111l_opy_ (u"ࠤ࡙ࠥࠦࡸࡡࡤ࡭ࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡱࡥࡺࡹࡲࡶࡩࠦࡥࡷࡧࡱࡸࡸࠦࠨࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡵࡿࡴࡦࡵࡷࠤ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࠢࠣࠤ᪝")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1l1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪞"), None)
        bstack1ll1111llll_opy_ = getattr(keyword, bstack1l1111l_opy_ (u"ࠦࡹࡿࡰࡦࠤ᪟"), None)
        test_id = kwargs.get(bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨ᪠"), None)
        if not test_id:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤࡱࡥࡺࡹࡲࡶࡩࡥࡥࡷࡧࡱࡸ࠿ࠦ࡮ࡰࠢࡷࡩࡸࡺ࡟ࡪࡦࠣ࡭ࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠣ᪡").format(keyword_name))
            return None
        instance = TestFramework.bstack1l1ll1ll1ll_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥ࡫ࡦࡻࡺࡳࡷࡪ࡟ࡦࡸࡨࡲࡹࡀࠠ࡯ࡱࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡥࡩࡥ࠿ࡾࢁࠧ᪢").format(test_id))
            return None
        bstack111l1ll11ll_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l1l1l1l111_opy_.bstack111l1lll1l1_opy_, {})
        if os.getenv(bstack1l1111l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡌࡇ࡜࡛ࡔࡘࡄࡔࠤ᪣"), bstack1l1111l_opy_ (u"ࠤ࠴ࠦ᪤")) == bstack1l1111l_opy_ (u"ࠥ࠵ࠧ᪥"):
            bstack111l1lll1ll_opy_ = bstack1l1111l_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥ᪦").format(bstack1ll1111llll_opy_, keyword_name)
            bstack111ll1l1lll_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1lllll1_opy_ = {
                bstack1l1111l_opy_ (u"ࠧࡱࡥࡺࠤᪧ"): bstack111l1lll1ll_opy_,
                bstack1l1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪨"): keyword_name,
                bstack1l1111l_opy_ (u"ࠢࡵࡻࡳࡩࠧ᪩"): bstack1ll1111llll_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l1lllll1_opy_[bstack1l1111l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ᪪")] = uuid4().__str__()
                bstack111l1lllll1_opy_[bstack1l1l1l1l111_opy_.bstack111ll11lll1_opy_] = bstack111ll1l1lll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1lllll1_opy_[bstack1l1l1l1l111_opy_.bstack11l111111ll_opy_] = bstack111ll1l1lll_opy_
                if len(args) > 1 and hasattr(args[1], bstack1l1111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ᪫")):
                    bstack111l1lllll1_opy_[bstack1l1111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᪬")] = args[1].status
            if bstack111l1lll1ll_opy_ in bstack111l1ll11ll_opy_:
                bstack111l1ll11ll_opy_[bstack111l1lll1ll_opy_].update(bstack111l1lllll1_opy_)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠢࡷࡽࡵ࡫࠽ࡼࡿࠥ᪭").format(keyword_name, bstack1ll1111llll_opy_))
            else:
                bstack111l1ll11ll_opy_[bstack111l1lll1ll_opy_] = bstack111l1lllll1_opy_
                self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠡࡶࡼࡴࡪࡃࡻࡾࠤ᪮").format(keyword_name, bstack1ll1111llll_opy_))
        TestFramework.bstack111l1llll1_opy_(instance, bstack1l1l1l1l111_opy_.bstack111l1lll1l1_opy_, bstack111l1ll11ll_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡹ࠽ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠣ᪯").format(len(bstack111l1ll11ll_opy_), instance.ref()))
        return instance
    def __111l1ll1l1l_opy_(
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
            bstack1l1l1l1l111_opy_.bstack111l1lll1l1_opy_: {},
            bstack1l1l1l1l111_opy_.bstack111ll1l1ll1_opy_: {},
            bstack1l1l1l1l111_opy_.bstack111lll11l1l_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1l1111l_opy_ (u"ࠢࡴࡱࡸࡶࡨ࡫ࠢ᪰")):
            TestFramework.bstack111l1llll1_opy_(ob, TestFramework.bstack11l1111lll1_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack111l1llll1_opy_(ob, TestFramework.bstack1l111l1l111_opy_, context.platform_index)
        TestFramework.bstack1lllll1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࢁࡽࠣ᪱").format(ctx.id, target, args, TestFramework.bstack1lllll1ll1_opy_.keys()))
        return ob
    def bstack11lll1l111l_opy_(self, instance: bstack1l11l1ll111_opy_, bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            bstack1l1l1l1l111_opy_.bstack111lllll111_opy_
            if bstack1l1ll1ll111_opy_[1] == TestHookState.PRE
            else bstack1l1l1l1l111_opy_.bstack111ll1l11l1_opy_
        )
        hook = bstack1l1l1l1l111_opy_.bstack111ll1l11ll_opy_(instance, bstack111lll11l11_opy_)
        entries = hook.get(TestFramework.bstack111ll111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, []))
        return entries
    def bstack11ll1llll1l_opy_(self, instance: bstack1l11l1ll111_opy_, bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            bstack1l1l1l1l111_opy_.bstack111lllll111_opy_
            if bstack1l1ll1ll111_opy_[1] == TestHookState.PRE
            else bstack1l1l1l1l111_opy_.bstack111ll1l11l1_opy_
        )
        bstack1l1l1l1l111_opy_.bstack111lllll1ll_opy_(instance, bstack111lll11l11_opy_)
        TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, []).clear()
    def bstack11l1111l1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᪲")
        global _11ll111llll_opy_
        platform_index = os.environ[bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᪳")]
        bstack11lll11l111_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), bstack111ll111111_opy_)
        if not os.path.exists(bstack11lll11l111_opy_) or not os.path.isdir(bstack11lll11l111_opy_):
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤ᪴").format(bstack11lll11l111_opy_))
            return
        logs = hook.get(bstack1l1111l_opy_ (u"ࠧࡲ࡯ࡨࡵ᪵ࠥ"), [])
        with os.scandir(bstack11lll11l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll111llll_opy_:
                    self.logger.info(bstack1l1111l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀ᪶ࠦ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1111l_opy_ (u"᪷ࠢࠣ")
                    log_entry = bstack11lll1ll1l_opy_(
                        kind=bstack1l1111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖ᪸ࠥ"),
                        message=bstack1l1111l_opy_ (u"ࠤ᪹ࠥ"),
                        level=bstack1l1111l_opy_ (u"᪺ࠥࠦ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll11l1111_opy_=entry.stat().st_size,
                        bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᪻"),
                        bstack111111_opy_=os.path.abspath(entry.path),
                        bstack111ll1l1l1l_opy_=hook.get(TestFramework.bstack11l1111l111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll111llll_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᪼")]
        bstack111llll11l1_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), bstack111ll111111_opy_, bstack111ll1111ll_opy_)
        if not os.path.exists(bstack111llll11l1_opy_) or not os.path.isdir(bstack111llll11l1_opy_):
            self.logger.info(bstack1l1111l_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽ᪽ࠣ").format(bstack111llll11l1_opy_))
        else:
            self.logger.info(bstack1l1111l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ᪾").format(bstack111llll11l1_opy_))
            with os.scandir(bstack111llll11l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll111llll_opy_:
                        self.logger.info(bstack1l1111l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᪿ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1111l_opy_ (u"ࠤᫀࠥ")
                        log_entry = bstack11lll1ll1l_opy_(
                            kind=bstack1l1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ᫁"),
                            message=bstack1l1111l_opy_ (u"ࠦࠧ᫂"),
                            level=bstack1l1111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤ᫃"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll11l1111_opy_=entry.stat().st_size,
                            bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ᫄"),
                            bstack111111_opy_=os.path.abspath(entry.path),
                            bstack11ll111l111_opy_=hook.get(TestFramework.bstack11l1111l111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll111llll_opy_.add(abs_path)
        hook[bstack1l1111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ᫅")] = logs
    def bstack1llll111ll_opy_(
        self,
        bstack1l111ll1ll_opy_: bstack1l11l1ll111_opy_,
        entries: List[bstack11lll1ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧ᫆"))
        req.platform_index = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l111l1l111_opy_)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᫇").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l11111l11l_opy_, bstack1l1111l_opy_ (u"ࠥࠦ᫈"))
            log_entry.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11ll11l1lll_opy_, bstack1l1111l_opy_ (u"ࠦࠧ᫉"))
            log_entry.uuid = entry.bstack111ll1l1l1l_opy_ or bstack1l1111l_opy_ (u"ࠧࠨ᫊")
            log_entry.test_framework_state = bstack1l111ll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ᫋"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1111l_opy_ (u"ࠢࠣᫌ")
            if entry.kind == bstack1l1111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᫍ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll11l1111_opy_
                log_entry.file_path = entry.bstack111111_opy_
        def bstack11ll11lll11_opy_():
            bstack11l11l1l_opy_ = datetime.now()
            try:
                self.bstack11l1ll1lll_opy_.LogCreatedEvent(req)
                bstack1l111ll1ll_opy_.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᫎ"), datetime.now() - bstack11l11l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤ᫏").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11lll11_opy_)
    def __11l1111llll_opy_(self, instance) -> None:
        bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᫐")
        bstack111llllll11_opy_ = {bstack1l1111l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢ᫑"): bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        bstack1l1l1l1lll1_opy_.bstack111lll1ll11_opy_()
    @staticmethod
    def bstack111ll1l11ll_opy_(instance: bstack1l11l1ll111_opy_, bstack111lll11l11_opy_: str):
        bstack11l11111111_opy_ = (
            bstack1l1l1l1l111_opy_.bstack111ll1l1ll1_opy_
            if bstack111lll11l11_opy_ == bstack1l1l1l1l111_opy_.bstack111ll1l11l1_opy_
            else bstack1l1l1l1l111_opy_.bstack111lll11l1l_opy_
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
        hook = bstack1l1l1l1l111_opy_.bstack111ll1l11ll_opy_(instance, bstack111lll11l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll111lll_opy_, []).clear()
    @staticmethod
    def __11l111111l1_opy_(instance: bstack1l11l1ll111_opy_, *args):
        bstack1l1111l_opy_ (u"ࠨࠢࠣࡒࡵࡳࡨ࡫ࡳࡴࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦࡵࠥࠦࠧ᫒")
        if len(args) < 1:
            return
        if os.getenv(bstack1l1111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦ᫓"), bstack1l1111l_opy_ (u"ࠣ࠳ࠥ᫔")) != bstack1l1111l_opy_ (u"ࠤ࠴ࠦ᫕"):
            bstack1l1l1l1l111_opy_.logger.warning(bstack1l1111l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡱࡵࡧࡴࠤ᫖"))
            return
        message = args[0]
        if not hasattr(message, bstack1l1111l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ᫗")):
            return
        is_screenshot = hasattr(message, bstack1l1111l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᫘")) and message.kind == bstack1l1111l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪ᫙")
        log_entry = bstack11lll1ll1l_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11lll11llll_opy_,
            message=message.message if hasattr(message, bstack1l1111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ᫚")) else bstack1l1111l_opy_ (u"ࠣࠤ᫛"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1l1111l_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣ᫜")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1l1111l_opy_ (u"ࠥࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠣ᫝")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1l1111l_opy_ (u"ࠦࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠢ᫞")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111llll1l11_opy_ = {
            bstack1l1111l_opy_ (u"࡙ࠧࡅࡕࡗࡓࠦ᫟"): (bstack1l1l1l1l111_opy_.bstack111lllll111_opy_, bstack1l1l1l1l111_opy_.bstack111lll11l1l_opy_),
            bstack1l1111l_opy_ (u"ࠨࡔࡆࡃࡕࡈࡔ࡝ࡎࠣ᫠"): (bstack1l1l1l1l111_opy_.bstack111ll1l11l1_opy_, bstack1l1l1l1l111_opy_.bstack111ll1l1ll1_opy_),
        }
        bstack111l1lll111_opy_ = None
        if len(args) > 1:
            bstack111l1lll111_opy_ = args[1]
        if bstack111l1lll111_opy_ and bstack111l1lll111_opy_ in bstack111llll1l11_opy_:
            bstack111llll111l_opy_, bstack11l11111111_opy_ = bstack111llll1l11_opy_[bstack111l1lll111_opy_]
            bstack111ll1ll111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack111llll111l_opy_, None)
            bstack111lll111l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack11l11111111_opy_, None) if bstack111ll1ll111_opy_ else None
            if isinstance(bstack111lll111l1_opy_, dict) and len(bstack111lll111l1_opy_.get(bstack111ll1ll111_opy_, [])) > 0:
                hook = bstack111lll111l1_opy_[bstack111ll1ll111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll111lll_opy_ in hook:
                    hook[TestFramework.bstack111ll111lll_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1ll1l11_opy_(test) -> Dict[str, Any]:
        bstack1l1111l_opy_ (u"ࠢࠣࠤࡓࡥࡷࡹࡥࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡸࡪࡹࡴࠡࡱࡥ࡮ࡪࡩࡴࠣࠤࠥ᫡")
        test_id = bstack1l1l1l1l111_opy_.__111l1lll11l_opy_(test)
        test_name = test.name if hasattr(test, bstack1l1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᫢")) else None
        bstack111ll11l1l1_opy_ = str(test.source) if hasattr(test, bstack1l1111l_opy_ (u"ࠤࡶࡳࡺࡸࡣࡦࠤ᫣")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1l1111l_opy_ (u"ࠥࡸࡦ࡭ࡳࠣ᫤")) else []
        bstack111l1ll1lll_opy_ =bstack1l1111l_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨ᫥").format(bstack1l1111l_opy_ (u"ࠧࠦࠢ᫦").join(test_tags), test_name) if test_tags else test_name
        bstack111ll111ll1_opy_ = []
        if bstack111ll11l1l1_opy_:
            from browserstack_sdk.bstack1lll1ll1lll_opy_ import RobotHandler
            bstack111ll111ll1_opy_ = RobotHandler.bstack1lll1l11ll1_opy_(bstack111ll11l1l1_opy_)
        if not bstack111ll111ll1_opy_ and test_name:
            bstack111ll111ll1_opy_ = [test_name]
        return {
            TestFramework.bstack11llllll111_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll11111_opy_: test_id,
            TestFramework.bstack1l111l11l1l_opy_: test_name,
            TestFramework.bstack11ll11111l1_opy_: test_id,
            TestFramework.bstack11l1111ll11_opy_: bstack111ll11l1l1_opy_,
            TestFramework.bstack11l11111ll1_opy_: test_tags,
            TestFramework.bstack11l1111111l_opy_: bstack111l1ll1lll_opy_,
            TestFramework.bstack11l1ll1111l_opy_: TestFramework.bstack111lll1l1ll_opy_,
            TestFramework.bstack11l11l11l1l_opy_: test_id,
            TestFramework.bstack111ll11111l_opy_: bstack111ll111ll1_opy_
        }
    @staticmethod
    def __111l1lll11l_opy_(test):
        bstack1l1111l_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡻ࡮ࡪࡳࡸࡩࠥࡺࡥࡴࡶࠣࡍࡉࠦࡦࡳࡱࡰࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡴࡦࡵࡷࠤࡴࡨࡪࡦࡥࡷࠦࠧࠨ᫧")
        if hasattr(test, bstack1l1111l_opy_ (u"ࠢࡪࡦࠥ᫨")):
            return test.id
        elif hasattr(test, bstack1l1111l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡴࡡ࡮ࡧࠥ᫩")):
            return test.longname
        elif hasattr(test, bstack1l1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫪")):
            return test.name
        return None