# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1l1111_opy_ import bstack1l1l1llllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack111l1l111l_opy_ import bstack111llll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l11111l_opy_,
    TestHookState,
    bstack1ll1l1ll111_opy_,
    bstack1llll11ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11ll111ll11_opy_
from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll111ll_opy_ import bstack1l1lll111l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll11l1_opy_ import bstack1l1l1lll1ll_opy_
from bstack_utils.bstack1lll111111_opy_ import bstack1l1ll1l1ll_opy_
bstack11lll1l1111_opy_ = bstack11ll111ll11_opy_()
bstack111ll1l11l1_opy_ = 1.0
bstack11ll111l1l1_opy_ = bstack1l111l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᩙ")
bstack111ll11l111_opy_ = bstack1l111l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᩚ")
bstack111ll11111l_opy_ = bstack1l111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᩛ")
bstack111ll1111l1_opy_ = bstack1l111l_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᩜ")
bstack111ll111l11_opy_ = bstack1l111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᩝ")
_11ll1ll11l1_opy_ = set()
class bstack1l1l111llll_opy_(TestFramework):
    bstack111ll111111_opy_ = bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡬ࡧࡼࡻࡴࡸࡤࡴࠤᩞ")
    bstack11l111l1111_opy_ = bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ᩟")
    bstack111lll1l1ll_opy_ = bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦ᩠ࠥ")
    bstack11l11111l11_opy_ = bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᩡ")
    bstack111lllll11l_opy_ = bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᩢ")
    bstack111l1llll1l_opy_: bool
    bstack1l1lll111ll_opy_: bstack1l1lll111l1_opy_ = None
    bstack1l1l1111l1_opy_ = None
    bstack111ll1l1ll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11lll1lll_opy_: Dict[str, str],
        bstack1l11llllll1_opy_: List[str] = [bstack1l111l_opy_ (u"ࠢࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠣᩣ")],
        bstack1l1lll111ll_opy_: bstack1l1lll111l1_opy_ = None,
        bstack1l1l1111l1_opy_=None
    ):
        super().__init__(bstack1l11llllll1_opy_, bstack1l11lll1lll_opy_, bstack1l1lll111ll_opy_)
        self.bstack111l1llll1l_opy_ = any(bstack1l111l_opy_ (u"ࠣࡴࡲࡦࡴࡺࠢᩤ") in item.lower() for item in bstack1l11llllll1_opy_)
        self.bstack1l1l1111l1_opy_ = bstack1l1l1111l1_opy_
    def track_event(
        self,
        context: bstack1ll1l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l111llll_opy_.bstack111ll1l1ll1_opy_:
            bstack111llll1lll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠨᩥ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111l1llll1l_opy_:
            self.logger.warning(bstack1l111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࡿࢂࠨᩦ").format(str(self.bstack1l11llllll1_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᩧ").format(args, kwargs))
            return
        instance = self.__111lll1111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠨᩨ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1l111llll_opy_.bstack111ll1l1ll1_opy_:
                bstack1l11l11l_opy_ = bstack1l111l_opy_ (u"ࠨࠢᩩ")
                name = bstack1l111l_opy_ (u"ࠢࠣᩪ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack111ll111l1l_opy_.value)
                    name = str(EVENTS.bstack111ll111l1l_opy_.name) + bstack1l111l_opy_ (u"ࠣ࠼ࠥᩫ") + str(test_framework_state.name)
                else:
                    bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack111ll111ll1_opy_.value)
                    name = str(EVENTS.bstack111ll111ll1_opy_.name) + bstack1l111l_opy_ (u"ࠤ࠽ࠦᩬ") + str(test_framework_state.name)
                TestFramework.bstack111llll1ll1_opy_(instance, name, bstack1l11l11l_opy_)
        except Exception as e:
            self.logger.debug(bstack1l111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᩭ").format(e))
        try:
            if not TestFramework.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack11l1l1lllll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l111llll_opy_.__111l1lll1l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l111l_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢᩮ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_):
                    TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l111l_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠨᩯ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack11lll11ll11_opy_):
                    TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack11lll11ll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l111l_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠧᩰ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l111llll_opy_.__111ll1lll11_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lllll1ll_opy_(instance, *args)
                self.__111lllll111_opy_(instance)
            elif test_framework_state in bstack1l1l111llll_opy_.bstack111ll1l1ll1_opy_:
                self.__11l11111ll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠥᩱ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111llll1111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1l111llll_opy_.bstack111ll1l1ll1_opy_:
                bstack1l11l11l_opy_ = bstack1l111l_opy_ (u"ࠣࠤᩲ")
                name = bstack1l111l_opy_ (u"ࠤࠥᩳ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll111l1l_opy_.name) + bstack1l111l_opy_ (u"ࠥ࠾ࠧᩴ") + str(test_framework_state.name)
                    bstack1l11l11l_opy_ = TestFramework.bstack111lll1lll1_opy_(instance, name)
                    bstack111ll11l1_opy_.end(EVENTS.bstack111ll111l1l_opy_.value, bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᩵"), bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᩶"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll111ll1_opy_.name) + bstack1l111l_opy_ (u"ࠨ࠺ࠣ᩷") + str(test_framework_state.name)
                    bstack1l11l11l_opy_ = TestFramework.bstack111lll1lll1_opy_(instance, name)
                    bstack111ll11l1_opy_.end(EVENTS.bstack111ll111ll1_opy_.value, bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᩸"), bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᩹"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ᩺").format(e))
    def bstack11ll1llllll_opy_(self):
        return self.bstack111l1llll1l_opy_
    def bstack11lll1l111l_opy_(self):
        return False
    def __111l1lll11l_opy_(self, *args):
        bstack1l111l_opy_ (u"ࠥࠦࠧࡖࡡࡳࡵࡨࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡲࡦࡵࡸࡰࡹࠦ࡯ࡣ࡬ࡨࡧࡹࠨࠢࠣ᩻")
        if len(args) > 1 and hasattr(args[1], bstack1l111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᩼")):
            result = args[1]
            if result:
                return TestFramework.bstack11lll1l11ll_opy_(result, [bstack1l111l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᩽"), bstack1l111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᩾"), bstack1l111l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡺࡩ࡮ࡧ᩿ࠥ"), bstack1l111l_opy_ (u"ࠣࡧࡱࡨࡹ࡯࡭ࡦࠤ᪀"), bstack1l111l_opy_ (u"ࠤࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠢ᪁")])
        return None
    def __111lllll1ll_opy_(self, instance: bstack1l11l11111l_opy_, *args):
        result = self.__111l1lll11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        status = result.get(bstack1l111l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᪂"), bstack1l111l_opy_ (u"ࠦࡓࡕࡔࠡࡔࡘࡒࠧ᪃"))
        if status == bstack1l111l_opy_ (u"ࠧࡌࡁࡊࡎࠥ᪄") and result.get(bstack1l111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᪅")):
            failure = [{bstack1l111l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ᪆"): [result.get(bstack1l111l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ᪇"), bstack1l111l_opy_ (u"ࠤࠥ᪈"))]}]
            bstack1ll111l1l1l_opy_ = bstack1l111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ᪉")
        bstack111lll1l1l1_opy_ = TestFramework.bstack111ll1ll11l_opy_
        if status == bstack1l111l_opy_ (u"ࠦࡕࡇࡓࡔࠤ᪊"):
            bstack111lll1l1l1_opy_ = bstack1l111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ᪋")
        elif status == bstack1l111l_opy_ (u"ࠨࡆࡂࡋࡏࠦ᪌"):
            bstack111lll1l1l1_opy_ = bstack1l111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ᪍")
        elif status == bstack1l111l_opy_ (u"ࠣࡕࡎࡍࡕࠨ᪎"):
            bstack111lll1l1l1_opy_ = bstack1l111l_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥ᪏")
        if bstack111lll1l1l1_opy_ != TestFramework.bstack111ll1ll11l_opy_:
            TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack11ll11llll1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack111lllll1l1_opy_(instance, {
            TestFramework.bstack11l1ll1l111_opy_: failure,
            TestFramework.bstack111ll1l1lll_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack11l1l1ll1l1_opy_: bstack111lll1l1l1_opy_,
        })
    def __111lll1111l_opy_(
        self,
        context: bstack1ll1l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111l1ll1l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111l1ll1lll_opy_(test) if test else None
                if target:
                    self.__111l1lll111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦ᪐"), None)
            elif hasattr(args[0], bstack1l111l_opy_ (u"ࠦ࡮ࡪࠢ᪑")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1l1ll111l1l_opy_(target) if target else None
        return instance
    def __11l11111ll1_opy_(
        self,
        instance: bstack1l11l11111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l111l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l1l111llll_opy_.bstack11l111l1111_opy_, {})
        if not key in bstack11l111l11ll_opy_:
            bstack11l111l11ll_opy_[key] = []
        bstack111ll1ll1l1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l1l111llll_opy_.bstack111lll1l1ll_opy_, {})
        if not key in bstack111ll1ll1l1_opy_:
            bstack111ll1ll1l1_opy_[key] = []
        bstack111lllllll1_opy_ = {
            bstack1l1l111llll_opy_.bstack11l111l1111_opy_: bstack11l111l11ll_opy_,
            bstack1l1l111llll_opy_.bstack111lll1l1ll_opy_: bstack111ll1ll1l1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1l111l_opy_ (u"ࠧࠨ᪒")
            if len(args) > 0 and hasattr(args[0], bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᪓")):
                hook_name = args[0].name
            hook = {
                bstack1l111l_opy_ (u"ࠢ࡬ࡧࡼࠦ᪔"): key,
                TestFramework.bstack111ll1ll1ll_opy_: uuid4().__str__(),
                TestFramework.bstack111lll1l111_opy_: TestFramework.bstack11l1111l111_opy_,
                TestFramework.bstack11l1111l11l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111lll1llll_opy_: [],
                TestFramework.bstack111lll11ll1_opy_: hook_name,
                TestFramework.bstack111ll1lllll_opy_: bstack1l1l1lll1ll_opy_.bstack111lll11lll_opy_()
            }
            bstack11l111l11ll_opy_[key].append(hook)
            bstack111lllllll1_opy_[bstack1l1l111llll_opy_.bstack11l11111l11_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llll11ll_opy_ = bstack11l111l11ll_opy_.get(key, [])
            hook = bstack111llll11ll_opy_.pop() if bstack111llll11ll_opy_ else None
            if hook:
                result = self.__111l1lll11l_opy_(*args)
                if result:
                    bstack11l111111l1_opy_ = result.get(bstack1l111l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᪕"), TestFramework.bstack11l1111l111_opy_)
                    if bstack11l111111l1_opy_ == bstack1l111l_opy_ (u"ࠤࡓࡅࡘ࡙ࠢ᪖"):
                        bstack11l111111l1_opy_ = bstack1l111l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ᪗")
                    elif bstack11l111111l1_opy_ == bstack1l111l_opy_ (u"ࠦࡋࡇࡉࡍࠤ᪘"):
                        bstack11l111111l1_opy_ = bstack1l111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᪙")
                    if bstack11l111111l1_opy_ != TestFramework.bstack11l1111l111_opy_:
                        hook[TestFramework.bstack111lll1l111_opy_] = bstack11l111111l1_opy_
                hook[TestFramework.bstack111ll1l1111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111ll1lllll_opy_] = bstack1l1l1lll1ll_opy_.bstack111lll11lll_opy_()
                self.bstack111ll11llll_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll1l1l1l_opy_, [])
                if logs:
                    self.bstack111ll1llll_opy_(instance, logs)
                bstack111ll1ll1l1_opy_[key].append(hook)
                bstack111lllllll1_opy_[bstack1l1l111llll_opy_.bstack111lllll11l_opy_] = key
        TestFramework.bstack111lllll1l1_opy_(instance, bstack111lllllll1_opy_)
        self.logger.debug(bstack1l111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽ࠯ࡽࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࡽࢀࠦ᪚").format(key, test_hook_state, bstack11l111l11ll_opy_, bstack111ll1ll1l1_opy_))
    def __111l1ll1l1l_opy_(
        self,
        context: bstack1ll1l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l111l_opy_ (u"ࠢࠣࠤࡗࡶࡦࡩ࡫ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡪࡼࡥ࡯ࡶࡶࠤ࠭ࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡳࡽࡹ࡫ࡳࡵࠢࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࠧࠨࠢ᪛")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1l111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪜"), None)
        bstack1l1lllllll1_opy_ = getattr(keyword, bstack1l111l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᪝"), None)
        test_id = kwargs.get(bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦ᪞"), None)
        if not test_id:
            self.logger.debug(bstack1l111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡯ࡪࡿࡷࡰࡴࡧࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡳࡵࠠࡵࡧࡶࡸࡤ࡯ࡤࠡ࡫ࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢ࡮ࡩࡾࡽ࡯ࡳࡦࡀࡿࢂࠨ᪟").format(keyword_name))
            return None
        instance = TestFramework.bstack1l1ll111l1l_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1l111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡰ࡫ࡹࡸࡱࡵࡨࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡴ࡯ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡴࡦࡵࡷࡣ࡮ࡪ࠽ࡼࡿࠥ᪠").format(test_id))
            return None
        bstack111l1lll1ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l1l111llll_opy_.bstack111ll111111_opy_, {})
        if os.getenv(bstack1l111l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡑࡅ࡚࡙ࡒࡖࡉ࡙ࠢ᪡"), bstack1l111l_opy_ (u"ࠢ࠲ࠤ᪢")) == bstack1l111l_opy_ (u"ࠣ࠳ࠥ᪣"):
            bstack111l1ll1ll1_opy_ = bstack1l111l_opy_ (u"ࠤࡾࢁ࠿ࢁࡽࠣ᪤").format(bstack1l1lllllll1_opy_, keyword_name)
            bstack11l11111lll_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1llllll_opy_ = {
                bstack1l111l_opy_ (u"ࠥ࡯ࡪࡿࠢ᪥"): bstack111l1ll1ll1_opy_,
                bstack1l111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪦"): keyword_name,
                bstack1l111l_opy_ (u"ࠧࡺࡹࡱࡧࠥᪧ"): bstack1l1lllllll1_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l1llllll_opy_[bstack1l111l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦ᪨")] = uuid4().__str__()
                bstack111l1llllll_opy_[bstack1l1l111llll_opy_.bstack11l1111l11l_opy_] = bstack11l11111lll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1llllll_opy_[bstack1l1l111llll_opy_.bstack111ll1l1111_opy_] = bstack11l11111lll_opy_
                if len(args) > 1 and hasattr(args[1], bstack1l111l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᪩")):
                    bstack111l1llllll_opy_[bstack1l111l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᪪")] = args[1].status
            if bstack111l1ll1ll1_opy_ in bstack111l1lll1ll_opy_:
                bstack111l1lll1ll_opy_[bstack111l1ll1ll1_opy_].update(bstack111l1llllll_opy_)
                self.logger.debug(bstack1l111l_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠠࡵࡻࡳࡩࡂࢁࡽࠣ᪫").format(keyword_name, bstack1l1lllllll1_opy_))
            else:
                bstack111l1lll1ll_opy_[bstack111l1ll1ll1_opy_] = bstack111l1llllll_opy_
                self.logger.debug(bstack1l111l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡮ࡩࡾࡽ࡯ࡳࡦࡀࡿࢂࠦࡴࡺࡲࡨࡁࢀࢃࠢ᪬").format(keyword_name, bstack1l1lllllll1_opy_))
        TestFramework.bstack11111ll11l_opy_(instance, bstack1l1l111llll_opy_.bstack111ll111111_opy_, bstack111l1lll1ll_opy_)
        self.logger.debug(bstack1l111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡷࡂࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠨ᪭").format(len(bstack111l1lll1ll_opy_), instance.ref()))
        return instance
    def __111l1lll111_opy_(
        self,
        context: bstack1ll1l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1l1llllll_opy_.create_context(target)
        ob = bstack1l11l11111l_opy_(ctx, self.bstack1l11llllll1_opy_, self.bstack1l11lll1lll_opy_, test_framework_state)
        TestFramework.bstack111lllll1l1_opy_(ob, {
            TestFramework.bstack11lllllll1l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11ll_opy_: context.test_framework_version,
            TestFramework.bstack111llllll11_opy_: [],
            bstack1l1l111llll_opy_.bstack111ll111111_opy_: {},
            bstack1l1l111llll_opy_.bstack111lll1l1ll_opy_: {},
            bstack1l1l111llll_opy_.bstack11l111l1111_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1l111l_opy_ (u"ࠧࡹ࡯ࡶࡴࡦࡩࠧ᪮")):
            TestFramework.bstack11111ll11l_opy_(ob, TestFramework.bstack11l111l111l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack11111ll11l_opy_(ob, TestFramework.bstack1l111l1111l_opy_, context.platform_index)
        TestFramework.bstack1l1l1111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l111l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࡿࢂࠨ᪯").format(ctx.id, target, args, TestFramework.bstack1l1l1111l_opy_.keys()))
        return ob
    def bstack11ll1l1lll1_opy_(self, instance: bstack1l11l11111l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            bstack1l1l111llll_opy_.bstack11l11111l11_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else bstack1l1l111llll_opy_.bstack111lllll11l_opy_
        )
        hook = bstack1l1l111llll_opy_.bstack11l1111l1ll_opy_(instance, bstack11l11111111_opy_)
        entries = hook.get(TestFramework.bstack111lll1llll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack111llllll11_opy_, []))
        return entries
    def bstack11ll1l111ll_opy_(self, instance: bstack1l11l11111l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            bstack1l1l111llll_opy_.bstack11l11111l11_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else bstack1l1l111llll_opy_.bstack111lllll11l_opy_
        )
        bstack1l1l111llll_opy_.bstack11l11111l1l_opy_(instance, bstack11l11111111_opy_)
        TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack111llllll11_opy_, []).clear()
    def bstack111ll11llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᪰")
        global _11ll1ll11l1_opy_
        platform_index = os.environ[bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᪱")]
        bstack11lll1l1lll_opy_ = os.path.join(bstack11lll1l1111_opy_, (bstack11ll111l1l1_opy_ + str(platform_index)), bstack111ll1111l1_opy_)
        if not os.path.exists(bstack11lll1l1lll_opy_) or not os.path.isdir(bstack11lll1l1lll_opy_):
            self.logger.debug(bstack1l111l_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢ᪲").format(bstack11lll1l1lll_opy_))
            return
        logs = hook.get(bstack1l111l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ᪳"), [])
        with os.scandir(bstack11lll1l1lll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1ll11l1_opy_:
                    self.logger.info(bstack1l111l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤ᪴").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l111l_opy_ (u"ࠧࠨ᪵")
                    log_entry = bstack1llll11ll_opy_(
                        kind=bstack1l111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔ᪶ࠣ"),
                        message=bstack1l111l_opy_ (u"᪷ࠢࠣ"),
                        level=bstack1l111l_opy_ (u"ࠣࠤ᪸"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11lll11llll_opy_=entry.stat().st_size,
                        bstack11ll1l1l111_opy_=bstack1l111l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ᪹"),
                        bstack111l11l_opy_=os.path.abspath(entry.path),
                        bstack111ll1ll111_opy_=hook.get(TestFramework.bstack111ll1ll1ll_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1ll11l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚᪺ࠪ")]
        bstack11l111l1l11_opy_ = os.path.join(bstack11lll1l1111_opy_, (bstack11ll111l1l1_opy_ + str(platform_index)), bstack111ll1111l1_opy_, bstack111ll111l11_opy_)
        if not os.path.exists(bstack11l111l1l11_opy_) or not os.path.isdir(bstack11l111l1l11_opy_):
            self.logger.info(bstack1l111l_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨ᪻").format(bstack11l111l1l11_opy_))
        else:
            self.logger.info(bstack1l111l_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦ᪼").format(bstack11l111l1l11_opy_))
            with os.scandir(bstack11l111l1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1ll11l1_opy_:
                        self.logger.info(bstack1l111l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀ᪽ࠦ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l111l_opy_ (u"ࠢࠣ᪾")
                        log_entry = bstack1llll11ll_opy_(
                            kind=bstack1l111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖᪿࠥ"),
                            message=bstack1l111l_opy_ (u"ࠤᫀࠥ"),
                            level=bstack1l111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ᫁"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11lll11llll_opy_=entry.stat().st_size,
                            bstack11ll1l1l111_opy_=bstack1l111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᫂"),
                            bstack111l11l_opy_=os.path.abspath(entry.path),
                            bstack11ll1ll11ll_opy_=hook.get(TestFramework.bstack111ll1ll1ll_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1ll11l1_opy_.add(abs_path)
        hook[bstack1l111l_opy_ (u"ࠧࡲ࡯ࡨࡵ᫃ࠥ")] = logs
    def bstack111ll1llll_opy_(
        self,
        bstack11l1l11111_opy_: bstack1l11l11111l_opy_,
        entries: List[bstack1llll11ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆ᫄ࠥ"))
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack1l111l1111l_opy_)
        req.client_worker_id = bstack1l111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ᫅").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack11l1l11111_opy_.context.hash)
        req.execution_context.thread_id = str(bstack11l1l11111_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack11l1l11111_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack11lllllll1l_opy_, bstack1l111l_opy_ (u"ࠣࠤ᫆"))
            log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack11ll11l11ll_opy_, bstack1l111l_opy_ (u"ࠤࠥ᫇"))
            log_entry.uuid = entry.bstack111ll1ll111_opy_ or bstack1l111l_opy_ (u"ࠥࠦ᫈")
            log_entry.test_framework_state = bstack11l1l11111_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᫉"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l111l_opy_ (u"ࠧࠨ᫊")
            if entry.kind == bstack1l111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᫋"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lll11llll_opy_
                log_entry.file_path = entry.bstack111l11l_opy_
        def bstack11ll1lllll1_opy_():
            bstack1ll111l111_opy_ = datetime.now()
            try:
                self.bstack1l1l1111l1_opy_.LogCreatedEvent(req)
                bstack11l1l11111_opy_.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᫌ"), datetime.now() - bstack1ll111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᫍ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll111ll_opy_.enqueue(bstack11ll1lllll1_opy_)
    def __111lllll111_opy_(self, instance) -> None:
        bstack1l111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᫎ")
        bstack111lllllll1_opy_ = {bstack1l111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ᫏"): bstack1l1l1lll1ll_opy_.bstack111lll11lll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack111lllll1l1_opy_(instance, bstack111lllllll1_opy_)
        bstack1l1l1lll1ll_opy_.bstack111lll111l1_opy_()
    @staticmethod
    def bstack11l1111l1ll_opy_(instance: bstack1l11l11111l_opy_, bstack11l11111111_opy_: str):
        bstack111ll11ll1l_opy_ = (
            bstack1l1l111llll_opy_.bstack111lll1l1ll_opy_
            if bstack11l11111111_opy_ == bstack1l1l111llll_opy_.bstack111lllll11l_opy_
            else bstack1l1l111llll_opy_.bstack11l111l1111_opy_
        )
        bstack11l111l11l1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack11l11111111_opy_, None)
        bstack111ll1l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11ll1l_opy_, None) if bstack11l111l11l1_opy_ else None
        return (
            bstack111ll1l11ll_opy_[bstack11l111l11l1_opy_][-1]
            if isinstance(bstack111ll1l11ll_opy_, dict) and len(bstack111ll1l11ll_opy_.get(bstack11l111l11l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l11111l1l_opy_(instance: bstack1l11l11111l_opy_, bstack11l11111111_opy_: str):
        hook = bstack1l1l111llll_opy_.bstack11l1111l1ll_opy_(instance, bstack11l11111111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111lll1llll_opy_, []).clear()
    @staticmethod
    def __111ll1lll11_opy_(instance: bstack1l11l11111l_opy_, *args):
        bstack1l111l_opy_ (u"ࠦࠧࠨࡐࡳࡱࡦࡩࡸࡹࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡯ࡳ࡬ࠦ࡭ࡦࡵࡶࡥ࡬࡫ࡳࠣࠤࠥ᫐")
        if len(args) < 1:
            return
        if os.getenv(bstack1l111l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤ᫑"), bstack1l111l_opy_ (u"ࠨ࠱ࠣ᫒")) != bstack1l111l_opy_ (u"ࠢ࠲ࠤ᫓"):
            bstack1l1l111llll_opy_.logger.warning(bstack1l111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢ࡯ࡳ࡬ࡹࠢ᫔"))
            return
        message = args[0]
        if not hasattr(message, bstack1l111l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ᫕")):
            return
        is_screenshot = hasattr(message, bstack1l111l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ᫖")) and message.kind == bstack1l111l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨ᫗")
        log_entry = bstack1llll11ll_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11ll1lll11l_opy_,
            message=message.message if hasattr(message, bstack1l111l_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨ᫘")) else bstack1l111l_opy_ (u"ࠨࠢ᫙"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1l111l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࠨ᫚")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1l111l_opy_ (u"ࠣࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠨ᫛")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1l111l_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠧ᫜")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111ll1llll1_opy_ = {
            bstack1l111l_opy_ (u"ࠥࡗࡊ࡚ࡕࡑࠤ᫝"): (bstack1l1l111llll_opy_.bstack11l11111l11_opy_, bstack1l1l111llll_opy_.bstack11l111l1111_opy_),
            bstack1l111l_opy_ (u"࡙ࠦࡋࡁࡓࡆࡒ࡛ࡓࠨ᫞"): (bstack1l1l111llll_opy_.bstack111lllll11l_opy_, bstack1l1l111llll_opy_.bstack111lll1l1ll_opy_),
        }
        bstack111l1llll11_opy_ = None
        if len(args) > 1:
            bstack111l1llll11_opy_ = args[1]
        if bstack111l1llll11_opy_ and bstack111l1llll11_opy_ in bstack111ll1llll1_opy_:
            bstack11l1111llll_opy_, bstack111ll11ll1l_opy_ = bstack111ll1llll1_opy_[bstack111l1llll11_opy_]
            bstack11l1111111l_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack11l1111llll_opy_, None)
            bstack111ll1l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11ll1l_opy_, None) if bstack11l1111111l_opy_ else None
            if isinstance(bstack111ll1l11ll_opy_, dict) and len(bstack111ll1l11ll_opy_.get(bstack11l1111111l_opy_, [])) > 0:
                hook = bstack111ll1l11ll_opy_[bstack11l1111111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111lll1llll_opy_ in hook:
                    hook[TestFramework.bstack111lll1llll_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack111llllll11_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1lll1l1_opy_(test) -> Dict[str, Any]:
        bstack1l111l_opy_ (u"ࠧࠨࠢࡑࡣࡵࡷࡪࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡶࡨࡷࡹࠦ࡯ࡣ࡬ࡨࡧࡹࠨࠢࠣ᫟")
        test_id = bstack1l1l111llll_opy_.__111l1ll1lll_opy_(test)
        test_name = test.name if hasattr(test, bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᫠")) else None
        bstack111llll11l1_opy_ = str(test.source) if hasattr(test, bstack1l111l_opy_ (u"ࠢࡴࡱࡸࡶࡨ࡫ࠢ᫡")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1l111l_opy_ (u"ࠣࡶࡤ࡫ࡸࠨ᫢")) else []
        bstack111l1lllll1_opy_ =bstack1l111l_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦ᫣").format(bstack1l111l_opy_ (u"ࠥࠤࠧ᫤").join(test_tags), test_name) if test_tags else test_name
        bstack111ll111lll_opy_ = []
        if bstack111llll11l1_opy_:
            from browserstack_sdk.bstack1lll1lll111_opy_ import RobotHandler
            bstack111ll111lll_opy_ = RobotHandler.bstack1lll1l1l1l1_opy_(bstack111llll11l1_opy_)
        if not bstack111ll111lll_opy_ and test_name:
            bstack111ll111lll_opy_ = [test_name]
        return {
            TestFramework.bstack1l11111llll_opy_: uuid4().__str__(),
            TestFramework.bstack11l1l1lllll_opy_: test_id,
            TestFramework.bstack11llllll11l_opy_: test_name,
            TestFramework.bstack11ll1111l11_opy_: test_id,
            TestFramework.bstack11l111111ll_opy_: bstack111llll11l1_opy_,
            TestFramework.bstack111lll11l1l_opy_: test_tags,
            TestFramework.bstack111llll111l_opy_: bstack111l1lllll1_opy_,
            TestFramework.bstack11l1l1ll1l1_opy_: TestFramework.bstack111ll1ll11l_opy_,
            TestFramework.bstack11l11l11lll_opy_: test_id,
            TestFramework.bstack111ll1111ll_opy_: bstack111ll111lll_opy_
        }
    @staticmethod
    def __111l1ll1lll_opy_(test):
        bstack1l111l_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡹࡳ࡯ࡱࡶࡧࠣࡸࡪࡹࡴࠡࡋࡇࠤ࡫ࡸ࡯࡮ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡹ࡫ࡳࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦ᫥")
        if hasattr(test, bstack1l111l_opy_ (u"ࠧ࡯ࡤࠣ᫦")):
            return test.id
        elif hasattr(test, bstack1l111l_opy_ (u"ࠨ࡬ࡰࡰࡪࡲࡦࡳࡥࠣ᫧")):
            return test.longname
        elif hasattr(test, bstack1l111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫨")):
            return test.name
        return None