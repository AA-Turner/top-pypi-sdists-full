# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11llll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1ll_opy_ import bstack11l1l1l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1lllll1_opy_,
    TestHookState,
    bstack1ll1l11lll1_opy_,
    bstack1l1l11lll1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1111l1lll_opy_
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1l1111ll_opy_ import bstack1ll11lllll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll11l1l1_opy_ import bstack1l1l11lll11_opy_
from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
bstack1l11111l1l1_opy_ = bstack1l1111l1lll_opy_()
bstack11l1l1lll11_opy_ = 1.0
bstack11lllll111l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤ᣹")
bstack11l11l111l1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ᣺")
bstack11l11l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣ᣻")
bstack11l11l11l11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ᣼")
bstack11l11l1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ᣽")
_1l11111llll_opy_ = set()
class bstack1ll1111l1ll_opy_(TestFramework):
    bstack11l11l11111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡱࡥࡺࡹࡲࡶࡩࡹࠢ᣾")
    bstack11l11l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨ᣿")
    bstack11l1l1lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᤀ")
    bstack11l11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᤁ")
    bstack11l1l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᤂ")
    bstack11l11l1111l_opy_: bool
    bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_ = None
    bstack1l1llll1lll_opy_ = None
    bstack11l11llllll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1l111111_opy_: Dict[str, str],
        bstack1l11l1l11ll_opy_: List[str] = [bstack1ll1lll_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨᤃ")],
        bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_ = None,
        bstack1l1llll1lll_opy_=None
    ):
        super().__init__(bstack1l11l1l11ll_opy_, bstack11l1l111111_opy_, bstack1ll1l1111ll_opy_)
        self.bstack11l11l1111l_opy_ = any(bstack1ll1lll_opy_ (u"ࠨࡲࡰࡤࡲࡸࠧᤄ") in item.lower() for item in bstack1l11l1l11ll_opy_)
        self.bstack1l1llll1lll_opy_ = bstack1l1llll1lll_opy_
    def track_event(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1ll1111l1ll_opy_.bstack11l11llllll_opy_:
            bstack11l1l1l11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦᤅ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l11l1111l_opy_:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࡽࢀࠦᤆ").format(str(self.bstack1l11l1l11ll_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᤇ").format(args, kwargs))
            return
        instance = self.__11l1lll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠦᤈ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1ll1111l1ll_opy_.bstack11l11llllll_opy_:
                bstack111l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠦࠧᤉ")
                name = bstack1ll1lll_opy_ (u"ࠧࠨᤊ")
                if (test_hook_state == TestHookState.PRE):
                    bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l111ll_opy_.value)
                    name = str(EVENTS.bstack11l11l111ll_opy_.name) + bstack1ll1lll_opy_ (u"ࠨ࠺ࠣᤋ") + str(test_framework_state.name)
                else:
                    bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l11ll1_opy_.value)
                    name = str(EVENTS.bstack11l11l11ll1_opy_.name) + bstack1ll1lll_opy_ (u"ࠢ࠻ࠤᤌ") + str(test_framework_state.name)
                TestFramework.bstack11l1l11111l_opy_(instance, name, bstack111l1l1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᤍ").format(e))
        try:
            if not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack11ll1lll111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1ll1111l1ll_opy_.__11l111ll11l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠧᤎ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l111l1l111_opy_):
                    TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l111l1l111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠦᤏ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l111ll1l11_opy_):
                    TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥᤐ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1ll1111l1ll_opy_.__11l1ll111l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1ll1ll11_opy_(instance, *args)
                self.__11l1ll1l11l_opy_(instance)
            elif test_framework_state in bstack1ll1111l1ll_opy_.bstack11l11llllll_opy_:
                self.__11l11lll1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠣᤑ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1l11lll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1ll1111l1ll_opy_.bstack11l11llllll_opy_:
                bstack111l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠨࠢᤒ")
                name = bstack1ll1lll_opy_ (u"ࠢࠣᤓ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l111ll_opy_.name) + bstack1ll1lll_opy_ (u"ࠣ࠼ࠥᤔ") + str(test_framework_state.name)
                    bstack111l1l1l1_opy_ = TestFramework.bstack11l1lll111l_opy_(instance, name)
                    bstack1l1l11ll1_opy_.end(EVENTS.bstack11l11l111ll_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᤕ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᤖ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11l11ll1_opy_.name) + bstack1ll1lll_opy_ (u"ࠦ࠿ࠨᤗ") + str(test_framework_state.name)
                    bstack111l1l1l1_opy_ = TestFramework.bstack11l1lll111l_opy_(instance, name)
                    bstack1l1l11ll1_opy_.end(EVENTS.bstack11l11l11ll1_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᤘ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᤙ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᤚ").format(e))
    def bstack1l1111111ll_opy_(self):
        return self.bstack11l11l1111l_opy_
    def bstack1l111l1l1ll_opy_(self):
        return False
    def __11l111ll1l1_opy_(self, *args):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࡔࡦࡸࡳࡦࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷ࡫ࡳࡶ࡮ࡷࠤࡴࡨࡪࡦࡥࡷࠦࠧࠨᤛ")
        if len(args) > 1 and hasattr(args[1], bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᤜ")):
            result = args[1]
            if result:
                return TestFramework.bstack1l1111lll11_opy_(result, [bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᤝ"), bstack1ll1lll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᤞ"), bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡸ࡮ࡳࡥࠣ᤟"), bstack1ll1lll_opy_ (u"ࠨࡥ࡯ࡦࡷ࡭ࡲ࡫ࠢᤠ"), bstack1ll1lll_opy_ (u"ࠢࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠧᤡ")])
        return None
    def __11l1ll1ll11_opy_(self, instance: bstack1l1l1lllll1_opy_, *args):
        result = self.__11l111ll1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lll11ll_opy_ = None
        status = result.get(bstack1ll1lll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᤢ"), bstack1ll1lll_opy_ (u"ࠤࡑࡓ࡙ࠦࡒࡖࡐࠥᤣ"))
        if status == bstack1ll1lll_opy_ (u"ࠥࡊࡆࡏࡌࠣᤤ") and result.get(bstack1ll1lll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᤥ")):
            failure = [{bstack1ll1lll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᤦ"): [result.get(bstack1ll1lll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᤧ"), bstack1ll1lll_opy_ (u"ࠢࠣᤨ"))]}]
            bstack1ll1lll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᤩ")
        bstack11l1l1l11l1_opy_ = TestFramework.bstack11l11l1lll1_opy_
        if status == bstack1ll1lll_opy_ (u"ࠤࡓࡅࡘ࡙ࠢᤪ"):
            bstack11l1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᤫ")
        elif status == bstack1ll1lll_opy_ (u"ࠦࡋࡇࡉࡍࠤ᤬"):
            bstack11l1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᤭")
        elif status == bstack1ll1lll_opy_ (u"ࠨࡓࡌࡋࡓࠦ᤮"):
            bstack11l1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣ᤯")
        if bstack11l1l1l11l1_opy_ != TestFramework.bstack11l11l1lll1_opy_:
            TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l1111ll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l1lllll_opy_(instance, {
            TestFramework.bstack11ll1llll11_opy_: failure,
            TestFramework.bstack11l1l1l1ll1_opy_: bstack1ll1lll11ll_opy_,
            TestFramework.bstack11lll1111ll_opy_: bstack11l1l1l11l1_opy_,
        })
    def __11l1lll1l11_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l111lll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l111ll1ll_opy_(test) if test else None
                if target:
                    self.__11l111lllll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᤰ"), None)
            elif hasattr(args[0], bstack1ll1lll_opy_ (u"ࠤ࡬ࡨࠧᤱ")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1ll11ll11l1_opy_(target) if target else None
        return instance
    def __11l11lll1ll_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1lll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack1ll1111l1ll_opy_.bstack11l11l1l1l1_opy_, {})
        if not key in bstack11l1lll1lll_opy_:
            bstack11l1lll1lll_opy_[key] = []
        bstack11l1l11l111_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack1ll1111l1ll_opy_.bstack11l1l1lll1l_opy_, {})
        if not key in bstack11l1l11l111_opy_:
            bstack11l1l11l111_opy_[key] = []
        bstack11l11llll11_opy_ = {
            bstack1ll1111l1ll_opy_.bstack11l11l1l1l1_opy_: bstack11l1lll1lll_opy_,
            bstack1ll1111l1ll_opy_.bstack11l1l1lll1l_opy_: bstack11l1l11l111_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1ll1lll_opy_ (u"ࠥࠦᤲ")
            if len(args) > 0 and hasattr(args[0], bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᤳ")):
                hook_name = args[0].name
            hook = {
                bstack1ll1lll_opy_ (u"ࠧࡱࡥࡺࠤᤴ"): key,
                TestFramework.bstack11l1l111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11l11ll111l_opy_: TestFramework.bstack11l1l111l1l_opy_,
                TestFramework.bstack11l1lll11ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1lll1l1l_opy_: [],
                TestFramework.bstack11l11ll1l11_opy_: hook_name,
                TestFramework.bstack11l1ll11l11_opy_: bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()
            }
            bstack11l1lll1lll_opy_[key].append(hook)
            bstack11l11llll11_opy_[bstack1ll1111l1ll_opy_.bstack11l11l1ll11_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1l1ll1ll_opy_ = bstack11l1lll1lll_opy_.get(key, [])
            hook = bstack11l1l1ll1ll_opy_.pop() if bstack11l1l1ll1ll_opy_ else None
            if hook:
                result = self.__11l111ll1l1_opy_(*args)
                if result:
                    bstack11l1l1ll11l_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᤵ"), TestFramework.bstack11l1l111l1l_opy_)
                    if bstack11l1l1ll11l_opy_ == bstack1ll1lll_opy_ (u"ࠢࡑࡃࡖࡗࠧᤶ"):
                        bstack11l1l1ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᤷ")
                    elif bstack11l1l1ll11l_opy_ == bstack1ll1lll_opy_ (u"ࠤࡉࡅࡎࡒࠢᤸ"):
                        bstack11l1l1ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦ᤹ࠥ")
                    if bstack11l1l1ll11l_opy_ != TestFramework.bstack11l1l111l1l_opy_:
                        hook[TestFramework.bstack11l11ll111l_opy_] = bstack11l1l1ll11l_opy_
                hook[TestFramework.bstack11l1l11l1l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1ll11l11_opy_] = bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1l1111ll_opy_, [])
                if logs:
                    self.bstack1l111ll11ll_opy_(instance, logs)
                bstack11l1l11l111_opy_[key].append(hook)
                bstack11l11llll11_opy_[bstack1ll1111l1ll_opy_.bstack11l1l11l11l_opy_] = key
        TestFramework.bstack11l1l1lllll_opy_(instance, bstack11l11llll11_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂ࠴ࡻࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࡻࡾࠤ᤺").format(key, test_hook_state, bstack11l1lll1lll_opy_, bstack11l1l11l111_opy_))
    def __11l111lll11_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡕࡴࡤࡧࡰࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡨࡺࡪࡴࡴࡴࠢࠫࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡱࡻࡷࡩࡸࡺࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ᤻ࠫࠥࠦࠧ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᤼"), None)
        bstack1ll1l11ll11_opy_ = getattr(keyword, bstack1ll1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧ᤽"), None)
        test_id = kwargs.get(bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤ᤾"), None)
        if not test_id:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠ࡭ࡨࡽࡼࡵࡲࡥࡡࡨࡺࡪࡴࡴ࠻ࠢࡱࡳࠥࡺࡥࡴࡶࡢ࡭ࡩࠦࡩ࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠ࡬ࡧࡼࡻࡴࡸࡤ࠾ࡽࢀࠦ᤿").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll11ll11l1_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡲࡴࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡡ࡬ࡨࡂࢁࡽࠣ᥀").format(test_id))
            return None
        bstack11l111llll1_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack1ll1111l1ll_opy_.bstack11l11l11111_opy_, {})
        if os.getenv(bstack1ll1lll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡏࡊ࡟ࡗࡐࡔࡇࡗࠧ᥁"), bstack1ll1lll_opy_ (u"ࠧ࠷ࠢ᥂")) == bstack1ll1lll_opy_ (u"ࠨ࠱ࠣ᥃"):
            bstack11l111l1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨ᥄").format(bstack1ll1l11ll11_opy_, keyword_name)
            bstack11l11lll111_opy_ = datetime.now(tz=timezone.utc)
            bstack11l111l1lll_opy_ = {
                bstack1ll1lll_opy_ (u"ࠣ࡭ࡨࡽࠧ᥅"): bstack11l111l1ll1_opy_,
                bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᥆"): keyword_name,
                bstack1ll1lll_opy_ (u"ࠥࡸࡾࡶࡥࠣ᥇"): bstack1ll1l11ll11_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l111l1lll_opy_[bstack1ll1lll_opy_ (u"ࠦࡺࡻࡩࡥࠤ᥈")] = uuid4().__str__()
                bstack11l111l1lll_opy_[bstack1ll1111l1ll_opy_.bstack11l1lll11ll_opy_] = bstack11l11lll111_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l111l1lll_opy_[bstack1ll1111l1ll_opy_.bstack11l1l11l1l1_opy_] = bstack11l11lll111_opy_
                if len(args) > 1 and hasattr(args[1], bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᥉")):
                    bstack11l111l1lll_opy_[bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᥊")] = args[1].status
            if bstack11l111l1ll1_opy_ in bstack11l111llll1_opy_:
                bstack11l111llll1_opy_[bstack11l111l1ll1_opy_].update(bstack11l111l1lll_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡ࡭ࡨࡽࡼࡵࡲࡥ࠿ࡾࢁࠥࡺࡹࡱࡧࡀࡿࢂࠨ᥋").format(keyword_name, bstack1ll1l11ll11_opy_))
            else:
                bstack11l111llll1_opy_[bstack11l111l1ll1_opy_] = bstack11l111l1lll_opy_
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠ࡬ࡧࡼࡻࡴࡸࡤ࠾ࡽࢀࠤࡹࡿࡰࡦ࠿ࡾࢁࠧ᥌").format(keyword_name, bstack1ll1l11ll11_opy_))
        TestFramework.bstack1lll1111ll_opy_(instance, bstack1ll1111l1ll_opy_.bstack11l11l11111_opy_, bstack11l111llll1_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡭ࡨࡽࡼࡵࡲࡥࡵࡀࡿࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠦ᥍").format(len(bstack11l111llll1_opy_), instance.ref()))
        return instance
    def __11l111lllll_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11llll1l_opy_.create_context(target)
        ob = bstack1l1l1lllll1_opy_(ctx, self.bstack1l11l1l11ll_opy_, self.bstack11l1l111111_opy_, test_framework_state)
        TestFramework.bstack11l1l1lllll_opy_(ob, {
            TestFramework.bstack1l11ll1l111_opy_: context.test_framework_name,
            TestFramework.bstack1l11111111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1l1l111l_opy_: [],
            bstack1ll1111l1ll_opy_.bstack11l11l11111_opy_: {},
            bstack1ll1111l1ll_opy_.bstack11l1l1lll1l_opy_: {},
            bstack1ll1111l1ll_opy_.bstack11l11l1l1l1_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1ll1lll_opy_ (u"ࠥࡷࡴࡻࡲࡤࡧࠥ᥎")):
            TestFramework.bstack1lll1111ll_opy_(ob, TestFramework.bstack11l11l1ll1l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1111ll_opy_(ob, TestFramework.bstack1l11l1ll11l_opy_, context.platform_index)
        TestFramework.bstack1111l1ll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࢀࠤࡦࡸࡧࡴ࠿ࡾࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࡽࢀࠦ᥏").format(ctx.id, target, args, TestFramework.bstack1111l1ll1l_opy_.keys()))
        return ob
    def bstack1l1111ll1ll_opy_(self, instance: bstack1l1l1lllll1_opy_, bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1ll1llll_opy_ = (
            bstack1ll1111l1ll_opy_.bstack11l11l1ll11_opy_
            if bstack1ll11l1l111_opy_[1] == TestHookState.PRE
            else bstack1ll1111l1ll_opy_.bstack11l1l11l11l_opy_
        )
        hook = bstack1ll1111l1ll_opy_.bstack11l1l1l1lll_opy_(instance, bstack11l1ll1llll_opy_)
        entries = hook.get(TestFramework.bstack11l1lll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, []))
        return entries
    def bstack1l111l1ll11_opy_(self, instance: bstack1l1l1lllll1_opy_, bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1ll1llll_opy_ = (
            bstack1ll1111l1ll_opy_.bstack11l11l1ll11_opy_
            if bstack1ll11l1l111_opy_[1] == TestHookState.PRE
            else bstack1ll1111l1ll_opy_.bstack11l1l11l11l_opy_
        )
        bstack1ll1111l1ll_opy_.bstack11l1ll1111l_opy_(instance, bstack11l1ll1llll_opy_)
        TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, []).clear()
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᥐ")
        global _1l11111llll_opy_
        platform_index = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᥑ")]
        bstack1l1111lll1l_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), bstack11l11l11l11_opy_)
        if not os.path.exists(bstack1l1111lll1l_opy_) or not os.path.isdir(bstack1l1111lll1l_opy_):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࡷࠥࡺ࡯ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡾࢁࠧᥒ").format(bstack1l1111lll1l_opy_))
            return
        logs = hook.get(bstack1ll1lll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᥓ"), [])
        with os.scandir(bstack1l1111lll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111llll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᥔ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1lll_opy_ (u"ࠥࠦᥕ")
                    log_entry = bstack1l1l11lll1l_opy_(
                        kind=bstack1ll1lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᥖ"),
                        message=bstack1ll1lll_opy_ (u"ࠧࠨᥗ"),
                        level=bstack1ll1lll_opy_ (u"ࠨࠢᥘ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1111llll1_opy_=entry.stat().st_size,
                        bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᥙ"),
                        bstack111lll_opy_=os.path.abspath(entry.path),
                        bstack11l1ll11l1l_opy_=hook.get(TestFramework.bstack11l1l111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111llll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᥚ")]
        bstack11l1l111ll1_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), bstack11l11l11l11_opy_, bstack11l11l1l11l_opy_)
        if not os.path.exists(bstack11l1l111ll1_opy_) or not os.path.isdir(bstack11l1l111ll1_opy_):
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᥛ").format(bstack11l1l111ll1_opy_))
        else:
            self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᥜ").format(bstack11l1l111ll1_opy_))
            with os.scandir(bstack11l1l111ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111llll_opy_:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᥝ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1lll_opy_ (u"ࠧࠨᥞ")
                        log_entry = bstack1l1l11lll1l_opy_(
                            kind=bstack1ll1lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᥟ"),
                            message=bstack1ll1lll_opy_ (u"ࠢࠣᥠ"),
                            level=bstack1ll1lll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᥡ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1111llll1_opy_=entry.stat().st_size,
                            bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᥢ"),
                            bstack111lll_opy_=os.path.abspath(entry.path),
                            bstack1l1111lllll_opy_=hook.get(TestFramework.bstack11l1l111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111llll_opy_.add(abs_path)
        hook[bstack1ll1lll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᥣ")] = logs
    def bstack1l111ll11ll_opy_(
        self,
        bstack11llllll1l1_opy_: bstack1l1l1lllll1_opy_,
        entries: List[bstack1l1l11lll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᥤ"))
        req.platform_index = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11l1ll11l_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᥥ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack11llllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack11llllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack11llllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11ll1l111_opy_, bstack1ll1lll_opy_ (u"ࠨࠢᥦ"))
            log_entry.test_framework_version = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11111111l_opy_, bstack1ll1lll_opy_ (u"ࠢࠣᥧ"))
            log_entry.uuid = entry.bstack11l1ll11l1l_opy_ or bstack1ll1lll_opy_ (u"ࠣࠤᥨ")
            log_entry.test_framework_state = bstack11llllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᥩ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1lll_opy_ (u"ࠥࠦᥪ")
            if entry.kind == bstack1ll1lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᥫ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1111llll1_opy_
                log_entry.file_path = entry.bstack111lll_opy_
        def bstack1l11111l1ll_opy_():
            bstack11lllll111_opy_ = datetime.now()
            try:
                self.bstack1l1llll1lll_opy_.LogCreatedEvent(req)
                bstack11llllll1l1_opy_.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᥬ"), datetime.now() - bstack11lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᥭ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l1111ll_opy_.enqueue(bstack1l11111l1ll_opy_)
    def __11l1ll1l11l_opy_(self, instance) -> None:
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ᥮")
        bstack11l11llll11_opy_ = {bstack1ll1lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥ᥯"): bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l1lllll_opy_(instance, bstack11l11llll11_opy_)
    @staticmethod
    def bstack11l1l1l1lll_opy_(instance: bstack1l1l1lllll1_opy_, bstack11l1ll1llll_opy_: str):
        bstack11l1ll1ll1l_opy_ = (
            bstack1ll1111l1ll_opy_.bstack11l1l1lll1l_opy_
            if bstack11l1ll1llll_opy_ == bstack1ll1111l1ll_opy_.bstack11l1l11l11l_opy_
            else bstack1ll1111l1ll_opy_.bstack11l11l1l1l1_opy_
        )
        bstack11l1l1ll111_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1llll_opy_, None)
        bstack11l1l1l1l1l_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1ll1l_opy_, None) if bstack11l1l1ll111_opy_ else None
        return (
            bstack11l1l1l1l1l_opy_[bstack11l1l1ll111_opy_][-1]
            if isinstance(bstack11l1l1l1l1l_opy_, dict) and len(bstack11l1l1l1l1l_opy_.get(bstack11l1l1ll111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll1111l_opy_(instance: bstack1l1l1lllll1_opy_, bstack11l1ll1llll_opy_: str):
        hook = bstack1ll1111l1ll_opy_.bstack11l1l1l1lll_opy_(instance, bstack11l1ll1llll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1lll1l1l_opy_, []).clear()
    @staticmethod
    def __11l1ll111l1_opy_(instance: bstack1l1l1lllll1_opy_, *args):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࡕࡸ࡯ࡤࡧࡶࡷࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࡸࠨࠢࠣᥰ")
        if len(args) < 1:
            return
        if os.getenv(bstack1ll1lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᥱ"), bstack1ll1lll_opy_ (u"ࠦ࠶ࠨᥲ")) != bstack1ll1lll_opy_ (u"ࠧ࠷ࠢᥳ"):
            bstack1ll1111l1ll_opy_.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠ࡭ࡱࡪࡷࠧᥴ"))
            return
        message = args[0]
        if not hasattr(message, bstack1ll1lll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ᥵")):
            return
        is_screenshot = hasattr(message, bstack1ll1lll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭᥶")) and message.kind == bstack1ll1lll_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭᥷")
        log_entry = bstack1l1l11lll1l_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack1l1111l1ll1_opy_,
            message=message.message if hasattr(message, bstack1ll1lll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ᥸")) else bstack1ll1lll_opy_ (u"ࠦࠧ᥹"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1ll1lll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦ᥺")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1ll1lll_opy_ (u"ࠨ࡚ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠦ᥻")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1ll1lll_opy_ (u"ࠢࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥ᥼")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l1ll1lll1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠣࡕࡈࡘ࡚ࡖࠢ᥽"): (bstack1ll1111l1ll_opy_.bstack11l11l1ll11_opy_, bstack1ll1111l1ll_opy_.bstack11l11l1l1l1_opy_),
            bstack1ll1lll_opy_ (u"ࠤࡗࡉࡆࡘࡄࡐ࡙ࡑࠦ᥾"): (bstack1ll1111l1ll_opy_.bstack11l1l11l11l_opy_, bstack1ll1111l1ll_opy_.bstack11l1l1lll1l_opy_),
        }
        bstack11l111ll111_opy_ = None
        if len(args) > 1:
            bstack11l111ll111_opy_ = args[1]
        if bstack11l111ll111_opy_ and bstack11l111ll111_opy_ in bstack11l1ll1lll1_opy_:
            bstack11l1ll1l1ll_opy_, bstack11l1ll1ll1l_opy_ = bstack11l1ll1lll1_opy_[bstack11l111ll111_opy_]
            bstack11l1l11llll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1l1ll_opy_, None)
            bstack11l1l1l1l1l_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1ll1l_opy_, None) if bstack11l1l11llll_opy_ else None
            if isinstance(bstack11l1l1l1l1l_opy_, dict) and len(bstack11l1l1l1l1l_opy_.get(bstack11l1l11llll_opy_, [])) > 0:
                hook = bstack11l1l1l1l1l_opy_[bstack11l1l11llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1lll1l1l_opy_ in hook:
                    hook[TestFramework.bstack11l1lll1l1l_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l111ll11l_opy_(test) -> Dict[str, Any]:
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࡖࡡࡳࡵࡨࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡴࡦࡵࡷࠤࡴࡨࡪࡦࡥࡷࠦࠧࠨ᥿")
        test_id = bstack1ll1111l1ll_opy_.__11l111ll1ll_opy_(test)
        test_name = test.name if hasattr(test, bstack1ll1lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦀ")) else None
        bstack11l1ll111ll_opy_ = str(test.source) if hasattr(test, bstack1ll1lll_opy_ (u"ࠧࡹ࡯ࡶࡴࡦࡩࠧᦁ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1ll1lll_opy_ (u"ࠨࡴࡢࡩࡶࠦᦂ")) else []
        bstack11l111lll1l_opy_ =bstack1ll1lll_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤᦃ").format(bstack1ll1lll_opy_ (u"ࠣࠢࠥᦄ").join(test_tags), test_name) if test_tags else test_name
        bstack11l11l1l111_opy_ = []
        if bstack11l1ll111ll_opy_:
            from browserstack_sdk.bstack1lll1llllll_opy_ import RobotHandler
            bstack11l11l1l111_opy_ = RobotHandler.bstack1lll1ll11l1_opy_(bstack11l1ll111ll_opy_)
        if not bstack11l11l1l111_opy_ and test_name:
            bstack11l11l1l111_opy_ = [test_name]
        return {
            TestFramework.bstack1l11ll11l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1lll111_opy_: test_id,
            TestFramework.bstack1l11lll1l1l_opy_: test_name,
            TestFramework.bstack11lll1lllll_opy_: test_id,
            TestFramework.bstack11l1ll1l1l1_opy_: bstack11l1ll111ll_opy_,
            TestFramework.bstack11l1ll1l111_opy_: test_tags,
            TestFramework.bstack11l11lll11l_opy_: bstack11l111lll1l_opy_,
            TestFramework.bstack11lll1111ll_opy_: TestFramework.bstack11l11l1lll1_opy_,
            TestFramework.bstack11ll11l1111_opy_: test_id,
            TestFramework.bstack11l11l11lll_opy_: bstack11l11l1l111_opy_
        }
    @staticmethod
    def __11l111ll1ll_opy_(test):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡷࡱ࡭ࡶࡻࡥࠡࡶࡨࡷࡹࠦࡉࡅࠢࡩࡶࡴࡳࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡷࡩࡸࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤᦅ")
        if hasattr(test, bstack1ll1lll_opy_ (u"ࠥ࡭ࡩࠨᦆ")):
            return test.id
        elif hasattr(test, bstack1ll1lll_opy_ (u"ࠦࡱࡵ࡮ࡨࡰࡤࡱࡪࠨᦇ")):
            return test.longname
        elif hasattr(test, bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᦈ")):
            return test.name
        return None