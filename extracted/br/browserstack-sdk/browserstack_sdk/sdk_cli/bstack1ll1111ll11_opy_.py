# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11ll11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack11l1ll1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1l111l1_opy_,
    TestHookState,
    bstack1ll1l11llll_opy_,
    bstack1l1l1l1lll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l11111l11l_opy_
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll11llll11_opy_ import bstack1ll11llllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1llllll_opy_ import bstack1l1ll1l11ll_opy_
from bstack_utils.bstack111l111l_opy_ import bstack11l11l1lll_opy_
bstack11llll1l1ll_opy_ = bstack1l11111l11l_opy_()
bstack11l11l1lll1_opy_ = 1.0
bstack11lllll1l1l_opy_ = bstack1ll11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᤊ")
bstack11l11l11lll_opy_ = bstack1ll11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᤋ")
bstack11l11l11l1l_opy_ = bstack1ll11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᤌ")
bstack11l11l11ll1_opy_ = bstack1ll11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᤍ")
bstack11l11l111ll_opy_ = bstack1ll11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᤎ")
_1l1111111l1_opy_ = set()
class bstack1l1lll1l1l1_opy_(TestFramework):
    bstack11l111l1ll1_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᤏ")
    bstack11l1lll11l1_opy_ = bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᤐ")
    bstack11l1l1ll111_opy_ = bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᤑ")
    bstack11l1l1ll1ll_opy_ = bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᤒ")
    bstack11l11lll11l_opy_ = bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᤓ")
    bstack11l111l1l11_opy_: bool
    bstack1ll11llll11_opy_: bstack1ll11llllll_opy_ = None
    bstack1l1ll1ll111_opy_ = None
    bstack11l1l1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l11l1l1ll_opy_: Dict[str, str],
        bstack1l1l111lll1_opy_: List[str] = [bstack1ll11_opy_ (u"ࠣࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤᤔ")],
        bstack1ll11llll11_opy_: bstack1ll11llllll_opy_ = None,
        bstack1l1ll1ll111_opy_=None
    ):
        super().__init__(bstack1l1l111lll1_opy_, bstack11l11l1l1ll_opy_, bstack1ll11llll11_opy_)
        self.bstack11l111l1l11_opy_ = any(bstack1ll11_opy_ (u"ࠤࡵࡳࡧࡵࡴࠣᤕ") in item.lower() for item in bstack1l1l111lll1_opy_)
        self.bstack1l1ll1ll111_opy_ = bstack1l1ll1ll111_opy_
    def track_event(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1lll1l1l1_opy_.bstack11l1l1l1l1l_opy_:
            bstack11l1ll1l11l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢᤖ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l111l1l11_opy_:
            self.logger.warning(bstack1ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࢀࢃࠢᤗ").format(str(self.bstack1l1l111lll1_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᤘ").format(args, kwargs))
            return
        instance = self.__11l11ll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠢᤙ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1lll1l1l1_opy_.bstack11l1l1l1l1l_opy_:
                bstack1l11ll1ll1_opy_ = bstack1ll11_opy_ (u"ࠢࠣᤚ")
                name = bstack1ll11_opy_ (u"ࠣࠤᤛ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l11l11l11_opy_.value)
                    name = str(EVENTS.bstack11l11l11l11_opy_.name) + bstack1ll11_opy_ (u"ࠤ࠽ࠦᤜ") + str(test_framework_state.name)
                else:
                    bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l11l111l1_opy_.value)
                    name = str(EVENTS.bstack11l11l111l1_opy_.name) + bstack1ll11_opy_ (u"ࠥ࠾ࠧᤝ") + str(test_framework_state.name)
                TestFramework.bstack11l1l1lll1l_opy_(instance, name, bstack1l11ll1ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᤞ").format(e))
        try:
            if not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack11lll111111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1lll1l1l1_opy_.__11l111lllll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll11_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣ᤟").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l111ll1111_opy_):
                    TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack1l111ll1111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢᤠ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack11lllll1lll_opy_):
                    TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack11lllll1lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠨᤡ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1lll1l1l1_opy_.__11l1ll11ll1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l111l11_opy_(instance, *args)
                self.__11l1ll1l1l1_opy_(instance)
            elif test_framework_state in bstack1l1lll1l1l1_opy_.bstack11l1l1l1l1l_opy_:
                self.__11l11l1l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠦᤢ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l11llll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1lll1l1l1_opy_.bstack11l1l1l1l1l_opy_:
                bstack1l11ll1ll1_opy_ = bstack1ll11_opy_ (u"ࠤࠥᤣ")
                name = bstack1ll11_opy_ (u"ࠥࠦᤤ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l11l11_opy_.name) + bstack1ll11_opy_ (u"ࠦ࠿ࠨᤥ") + str(test_framework_state.name)
                    bstack1l11ll1ll1_opy_ = TestFramework.bstack11l1l1ll11l_opy_(instance, name)
                    bstack11ll11l1ll_opy_.end(EVENTS.bstack11l11l11l11_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᤦ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᤧ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11l111l1_opy_.name) + bstack1ll11_opy_ (u"ࠢ࠻ࠤᤨ") + str(test_framework_state.name)
                    bstack1l11ll1ll1_opy_ = TestFramework.bstack11l1l1ll11l_opy_(instance, name)
                    bstack11ll11l1ll_opy_.end(EVENTS.bstack11l11l111l1_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᤩ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᤪ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᤫ").format(e))
    def bstack11lllllll1l_opy_(self):
        return self.bstack11l111l1l11_opy_
    def bstack1l111l1l11l_opy_(self):
        return False
    def __11l111lll1l_opy_(self, *args):
        bstack1ll11_opy_ (u"ࠦࠧࠨࡐࡢࡴࡶࡩࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡧࡶࡹࡱࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤ᤬")
        if len(args) > 1 and hasattr(args[1], bstack1ll11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᤭")):
            result = args[1]
            if result:
                return TestFramework.bstack1l111l11l1l_opy_(result, [bstack1ll11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᤮"), bstack1ll11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ᤯"), bstack1ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡴࡪ࡯ࡨࠦᤰ"), bstack1ll11_opy_ (u"ࠤࡨࡲࡩࡺࡩ࡮ࡧࠥᤱ"), bstack1ll11_opy_ (u"ࠥࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠣᤲ")])
        return None
    def __11l1l111l11_opy_(self, instance: bstack1l1l1l111l1_opy_, *args):
        result = self.__11l111lll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lll111l_opy_ = None
        status = result.get(bstack1ll11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᤳ"), bstack1ll11_opy_ (u"ࠧࡔࡏࡕࠢࡕ࡙ࡓࠨᤴ"))
        if status == bstack1ll11_opy_ (u"ࠨࡆࡂࡋࡏࠦᤵ") and result.get(bstack1ll11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᤶ")):
            failure = [{bstack1ll11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᤷ"): [result.get(bstack1ll11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᤸ"), bstack1ll11_opy_ (u"᤹ࠥࠦ"))]}]
            bstack1ll1lll111l_opy_ = bstack1ll11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ᤺")
        bstack11l1lll11ll_opy_ = TestFramework.bstack11l1lll1l1l_opy_
        if status == bstack1ll11_opy_ (u"ࠧࡖࡁࡔࡕ᤻ࠥ"):
            bstack11l1lll11ll_opy_ = bstack1ll11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ᤼")
        elif status == bstack1ll11_opy_ (u"ࠢࡇࡃࡌࡐࠧ᤽"):
            bstack11l1lll11ll_opy_ = bstack1ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ᤾")
        elif status == bstack1ll11_opy_ (u"ࠤࡖࡏࡎࡖࠢ᤿"):
            bstack11l1lll11ll_opy_ = bstack1ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦ᥀")
        if bstack11l1lll11ll_opy_ != TestFramework.bstack11l1lll1l1l_opy_:
            TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack1l111l1l1l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l1l1111_opy_(instance, {
            TestFramework.bstack11ll1lll1ll_opy_: failure,
            TestFramework.bstack11l1l111l1l_opy_: bstack1ll1lll111l_opy_,
            TestFramework.bstack11lll11l111_opy_: bstack11l1lll11ll_opy_,
        })
    def __11l11ll1l11_opy_(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l111ll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l111l1l1l_opy_(test) if test else None
                if target:
                    self.__11l111l1lll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧ᥁"), None)
            elif hasattr(args[0], bstack1ll11_opy_ (u"ࠧ࡯ࡤࠣ᥂")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1ll111l1lll_opy_(target) if target else None
        return instance
    def __11l11l1l11l_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l11lllll1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lll1l1l1_opy_.bstack11l1lll11l1_opy_, {})
        if not key in bstack11l11lllll1_opy_:
            bstack11l11lllll1_opy_[key] = []
        bstack11l1l11llll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lll1l1l1_opy_.bstack11l1l1ll111_opy_, {})
        if not key in bstack11l1l11llll_opy_:
            bstack11l1l11llll_opy_[key] = []
        bstack11l11l1l111_opy_ = {
            bstack1l1lll1l1l1_opy_.bstack11l1lll11l1_opy_: bstack11l11lllll1_opy_,
            bstack1l1lll1l1l1_opy_.bstack11l1l1ll111_opy_: bstack11l1l11llll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1ll11_opy_ (u"ࠨࠢ᥃")
            if len(args) > 0 and hasattr(args[0], bstack1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᥄")):
                hook_name = args[0].name
            hook = {
                bstack1ll11_opy_ (u"ࠣ࡭ࡨࡽࠧ᥅"): key,
                TestFramework.bstack11l1l11ll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1l11lll1_opy_: TestFramework.bstack11l11l1l1l1_opy_,
                TestFramework.bstack11l11l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1l111ll1_opy_: [],
                TestFramework.bstack11l1ll1111l_opy_: hook_name,
                TestFramework.bstack11l1l1l1lll_opy_: bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()
            }
            bstack11l11lllll1_opy_[key].append(hook)
            bstack11l11l1l111_opy_[bstack1l1lll1l1l1_opy_.bstack11l1l1ll1ll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll11l1l_opy_ = bstack11l11lllll1_opy_.get(key, [])
            hook = bstack11l1ll11l1l_opy_.pop() if bstack11l1ll11l1l_opy_ else None
            if hook:
                result = self.__11l111lll1l_opy_(*args)
                if result:
                    bstack11l1ll11lll_opy_ = result.get(bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ᥆"), TestFramework.bstack11l11l1l1l1_opy_)
                    if bstack11l1ll11lll_opy_ == bstack1ll11_opy_ (u"ࠥࡔࡆ࡙ࡓࠣ᥇"):
                        bstack11l1ll11lll_opy_ = bstack1ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ᥈")
                    elif bstack11l1ll11lll_opy_ == bstack1ll11_opy_ (u"ࠧࡌࡁࡊࡎࠥ᥉"):
                        bstack11l1ll11lll_opy_ = bstack1ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ᥊")
                    if bstack11l1ll11lll_opy_ != TestFramework.bstack11l11l1l1l1_opy_:
                        hook[TestFramework.bstack11l1l11lll1_opy_] = bstack11l1ll11lll_opy_
                hook[TestFramework.bstack11l1ll111l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1lll_opy_] = bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll111ll_opy_, [])
                if logs:
                    self.bstack11llllll1ll_opy_(instance, logs)
                bstack11l1l11llll_opy_[key].append(hook)
                bstack11l11l1l111_opy_[bstack1l1lll1l1l1_opy_.bstack11l11lll11l_opy_] = key
        TestFramework.bstack11l1l1l1111_opy_(instance, bstack11l11l1l111_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾ࠰ࡾࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࡾࢁࠧ᥋").format(key, test_hook_state, bstack11l11lllll1_opy_, bstack11l1l11llll_opy_))
    def __11l111ll1ll_opy_(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll11_opy_ (u"ࠣࠤࠥࡘࡷࡧࡣ࡬ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࡸࡱࡵࡨࠥ࡫ࡶࡦࡰࡷࡷࠥ࠮ࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡴࡾࡺࡥࡴࡶࠣࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࠨࠢࠣ᥌")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᥍"), None)
        bstack1ll1l11lll1_opy_ = getattr(keyword, bstack1ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣ᥎"), None)
        test_id = kwargs.get(bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧ᥏"), None)
        if not test_id:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡰ࡫ࡹࡸࡱࡵࡨࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡴ࡯ࠡࡶࡨࡷࡹࡥࡩࡥࠢ࡬ࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠢᥐ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll111l1lll_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤࡱࡥࡺࡹࡲࡶࡩࡥࡥࡷࡧࡱࡸ࠿ࠦ࡮ࡰࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤ࡯ࡤ࠾ࡽࢀࠦᥑ").format(test_id))
            return None
        bstack11l111ll1l1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lll1l1l1_opy_.bstack11l111l1ll1_opy_, {})
        if os.getenv(bstack1ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡋࡆ࡛࡚ࡓࡗࡊࡓࠣᥒ"), bstack1ll11_opy_ (u"ࠣ࠳ࠥᥓ")) == bstack1ll11_opy_ (u"ࠤ࠴ࠦᥔ"):
            bstack11l111lll11_opy_ = bstack1ll11_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤᥕ").format(bstack1ll1l11lll1_opy_, keyword_name)
            bstack11l1ll1llll_opy_ = datetime.now(tz=timezone.utc)
            bstack11l111ll111_opy_ = {
                bstack1ll11_opy_ (u"ࠦࡰ࡫ࡹࠣᥖ"): bstack11l111lll11_opy_,
                bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᥗ"): keyword_name,
                bstack1ll11_opy_ (u"ࠨࡴࡺࡲࡨࠦᥘ"): bstack1ll1l11lll1_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l111ll111_opy_[bstack1ll11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᥙ")] = uuid4().__str__()
                bstack11l111ll111_opy_[bstack1l1lll1l1l1_opy_.bstack11l11l1ll11_opy_] = bstack11l1ll1llll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l111ll111_opy_[bstack1l1lll1l1l1_opy_.bstack11l1ll111l1_opy_] = bstack11l1ll1llll_opy_
                if len(args) > 1 and hasattr(args[1], bstack1ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᥚ")):
                    bstack11l111ll111_opy_[bstack1ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᥛ")] = args[1].status
            if bstack11l111lll11_opy_ in bstack11l111ll1l1_opy_:
                bstack11l111ll1l1_opy_[bstack11l111lll11_opy_].update(bstack11l111ll111_opy_)
                self.logger.debug(bstack1ll11_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠡࡶࡼࡴࡪࡃࡻࡾࠤᥜ").format(keyword_name, bstack1ll1l11lll1_opy_))
            else:
                bstack11l111ll1l1_opy_[bstack11l111lll11_opy_] = bstack11l111ll111_opy_
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠠࡵࡻࡳࡩࡂࢁࡽࠣᥝ").format(keyword_name, bstack1ll1l11lll1_opy_))
        TestFramework.bstack1l11lllll_opy_(instance, bstack1l1lll1l1l1_opy_.bstack11l111l1ll1_opy_, bstack11l111ll1l1_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡸࡃࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠢᥞ").format(len(bstack11l111ll1l1_opy_), instance.ref()))
        return instance
    def __11l111l1lll_opy_(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11ll11ll_opy_.create_context(target)
        ob = bstack1l1l1l111l1_opy_(ctx, self.bstack1l1l111lll1_opy_, self.bstack11l11l1l1ll_opy_, test_framework_state)
        TestFramework.bstack11l1l1l1111_opy_(ob, {
            TestFramework.bstack1l11l11llll_opy_: context.test_framework_name,
            TestFramework.bstack1l11111lll1_opy_: context.test_framework_version,
            TestFramework.bstack11l11l1ll1l_opy_: [],
            bstack1l1lll1l1l1_opy_.bstack11l111l1ll1_opy_: {},
            bstack1l1lll1l1l1_opy_.bstack11l1l1ll111_opy_: {},
            bstack1l1lll1l1l1_opy_.bstack11l1lll11l1_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1ll11_opy_ (u"ࠨࡳࡰࡷࡵࡧࡪࠨᥟ")):
            TestFramework.bstack1l11lllll_opy_(ob, TestFramework.bstack11l1l11l1l1_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1l11lllll_opy_(ob, TestFramework.bstack1l11llll11l_opy_, context.platform_index)
        TestFramework.bstack1l1l111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࢀࢃࠢᥠ").format(ctx.id, target, args, TestFramework.bstack1l1l111l_opy_.keys()))
        return ob
    def bstack1l1111l1l1l_opy_(self, instance: bstack1l1l1l111l1_opy_, bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1ll1l1_opy_ = (
            bstack1l1lll1l1l1_opy_.bstack11l1l1ll1ll_opy_
            if bstack1ll11l11lll_opy_[1] == TestHookState.PRE
            else bstack1l1lll1l1l1_opy_.bstack11l11lll11l_opy_
        )
        hook = bstack1l1lll1l1l1_opy_.bstack11l1l11l11l_opy_(instance, bstack11l1l1ll1l1_opy_)
        entries = hook.get(TestFramework.bstack11l1l111ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, []))
        return entries
    def bstack1l1111llll1_opy_(self, instance: bstack1l1l1l111l1_opy_, bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1ll1l1_opy_ = (
            bstack1l1lll1l1l1_opy_.bstack11l1l1ll1ll_opy_
            if bstack1ll11l11lll_opy_[1] == TestHookState.PRE
            else bstack1l1lll1l1l1_opy_.bstack11l11lll11l_opy_
        )
        bstack1l1lll1l1l1_opy_.bstack11l1l1l11l1_opy_(instance, bstack11l1l1ll1l1_opy_)
        TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, []).clear()
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᥡ")
        global _1l1111111l1_opy_
        platform_index = os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᥢ")]
        bstack1l111l111ll_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), bstack11l11l11ll1_opy_)
        if not os.path.exists(bstack1l111l111ll_opy_) or not os.path.isdir(bstack1l111l111ll_opy_):
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᥣ").format(bstack1l111l111ll_opy_))
            return
        logs = hook.get(bstack1ll11_opy_ (u"ࠦࡱࡵࡧࡴࠤᥤ"), [])
        with os.scandir(bstack1l111l111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1111111l1_opy_:
                    self.logger.info(bstack1ll11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᥥ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll11_opy_ (u"ࠨࠢᥦ")
                    log_entry = bstack1l1l1l1lll1_opy_(
                        kind=bstack1ll11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᥧ"),
                        message=bstack1ll11_opy_ (u"ࠣࠤᥨ"),
                        level=bstack1ll11_opy_ (u"ࠤࠥᥩ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11llll1lll1_opy_=entry.stat().st_size,
                        bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᥪ"),
                        bstack1l11ll_opy_=os.path.abspath(entry.path),
                        bstack11l1l1lllll_opy_=hook.get(TestFramework.bstack11l1l11ll1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1111111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᥫ")]
        bstack11l1l1llll1_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), bstack11l11l11ll1_opy_, bstack11l11l111ll_opy_)
        if not os.path.exists(bstack11l1l1llll1_opy_) or not os.path.isdir(bstack11l1l1llll1_opy_):
            self.logger.info(bstack1ll11_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᥬ").format(bstack11l1l1llll1_opy_))
        else:
            self.logger.info(bstack1ll11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᥭ").format(bstack11l1l1llll1_opy_))
            with os.scandir(bstack11l1l1llll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1111111l1_opy_:
                        self.logger.info(bstack1ll11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧ᥮").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll11_opy_ (u"ࠣࠤ᥯")
                        log_entry = bstack1l1l1l1lll1_opy_(
                            kind=bstack1ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᥰ"),
                            message=bstack1ll11_opy_ (u"ࠥࠦᥱ"),
                            level=bstack1ll11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᥲ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11llll1lll1_opy_=entry.stat().st_size,
                            bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᥳ"),
                            bstack1l11ll_opy_=os.path.abspath(entry.path),
                            bstack1l111l1ll11_opy_=hook.get(TestFramework.bstack11l1l11ll1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1111111l1_opy_.add(abs_path)
        hook[bstack1ll11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᥴ")] = logs
    def bstack11llllll1ll_opy_(
        self,
        bstack1l1111ll11l_opy_: bstack1l1l1l111l1_opy_,
        entries: List[bstack1l1l1l1lll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦ᥵"))
        req.platform_index = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11llll11l_opy_)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᥶").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111ll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111ll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111ll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11l11llll_opy_, bstack1ll11_opy_ (u"ࠤࠥ᥷"))
            log_entry.test_framework_version = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11111lll1_opy_, bstack1ll11_opy_ (u"ࠥࠦ᥸"))
            log_entry.uuid = entry.bstack11l1l1lllll_opy_ or bstack1ll11_opy_ (u"ࠦࠧ᥹")
            log_entry.test_framework_state = bstack1l1111ll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ᥺"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll11_opy_ (u"ࠨࠢ᥻")
            if entry.kind == bstack1ll11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᥼"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11llll1lll1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l111l1llll_opy_():
            bstack11l111ll1_opy_ = datetime.now()
            try:
                self.bstack1l1ll1ll111_opy_.LogCreatedEvent(req)
                bstack1l1111ll11l_opy_.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ᥽"), datetime.now() - bstack11l111ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣ᥾").format(str(e)))
                traceback.print_exc()
        self.bstack1ll11llll11_opy_.enqueue(bstack1l111l1llll_opy_)
    def __11l1ll1l1l1_opy_(self, instance) -> None:
        bstack1ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᥿")
        bstack11l11l1l111_opy_ = {bstack1ll11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᦀ"): bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l1l1111_opy_(instance, bstack11l11l1l111_opy_)
    @staticmethod
    def bstack11l1l11l11l_opy_(instance: bstack1l1l1l111l1_opy_, bstack11l1l1ll1l1_opy_: str):
        bstack11l11lll1l1_opy_ = (
            bstack1l1lll1l1l1_opy_.bstack11l1l1ll111_opy_
            if bstack11l1l1ll1l1_opy_ == bstack1l1lll1l1l1_opy_.bstack11l11lll11l_opy_
            else bstack1l1lll1l1l1_opy_.bstack11l1lll11l1_opy_
        )
        bstack11l11ll1lll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack11l1l1ll1l1_opy_, None)
        bstack11l1l1111ll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack11l11lll1l1_opy_, None) if bstack11l11ll1lll_opy_ else None
        return (
            bstack11l1l1111ll_opy_[bstack11l11ll1lll_opy_][-1]
            if isinstance(bstack11l1l1111ll_opy_, dict) and len(bstack11l1l1111ll_opy_.get(bstack11l11ll1lll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1l1l11l1_opy_(instance: bstack1l1l1l111l1_opy_, bstack11l1l1ll1l1_opy_: str):
        hook = bstack1l1lll1l1l1_opy_.bstack11l1l11l11l_opy_(instance, bstack11l1l1ll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1l111ll1_opy_, []).clear()
    @staticmethod
    def __11l1ll11ll1_opy_(instance: bstack1l1l1l111l1_opy_, *args):
        bstack1ll11_opy_ (u"ࠧࠨࠢࡑࡴࡲࡧࡪࡹࡳࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࡴࠤࠥࠦᦁ")
        if len(args) < 1:
            return
        if os.getenv(bstack1ll11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᦂ"), bstack1ll11_opy_ (u"ࠢ࠲ࠤᦃ")) != bstack1ll11_opy_ (u"ࠣ࠳ࠥᦄ"):
            bstack1l1lll1l1l1_opy_.logger.warning(bstack1ll11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡰࡴ࡭ࡳࠣᦅ"))
            return
        message = args[0]
        if not hasattr(message, bstack1ll11_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᦆ")):
            return
        is_screenshot = hasattr(message, bstack1ll11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᦇ")) and message.kind == bstack1ll11_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᦈ")
        log_entry = bstack1l1l1l1lll1_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11lllllllll_opy_,
            message=message.message if hasattr(message, bstack1ll11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᦉ")) else bstack1ll11_opy_ (u"ࠢࠣᦊ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1ll11_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᦋ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1ll11_opy_ (u"ࠤࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠢᦌ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1ll11_opy_ (u"ࠥࡸ࡮ࡳࡥࡴࡶࡤࡱࡵࠨᦍ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l11lll1ll_opy_ = {
            bstack1ll11_opy_ (u"ࠦࡘࡋࡔࡖࡒࠥᦎ"): (bstack1l1lll1l1l1_opy_.bstack11l1l1ll1ll_opy_, bstack1l1lll1l1l1_opy_.bstack11l1lll11l1_opy_),
            bstack1ll11_opy_ (u"࡚ࠧࡅࡂࡔࡇࡓ࡜ࡔࠢᦏ"): (bstack1l1lll1l1l1_opy_.bstack11l11lll11l_opy_, bstack1l1lll1l1l1_opy_.bstack11l1l1ll111_opy_),
        }
        bstack11l111ll11l_opy_ = None
        if len(args) > 1:
            bstack11l111ll11l_opy_ = args[1]
        if bstack11l111ll11l_opy_ and bstack11l111ll11l_opy_ in bstack11l11lll1ll_opy_:
            bstack11l11ll1ll1_opy_, bstack11l11lll1l1_opy_ = bstack11l11lll1ll_opy_[bstack11l111ll11l_opy_]
            bstack11l1lll111l_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack11l11ll1ll1_opy_, None)
            bstack11l1l1111ll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack11l11lll1l1_opy_, None) if bstack11l1lll111l_opy_ else None
            if isinstance(bstack11l1l1111ll_opy_, dict) and len(bstack11l1l1111ll_opy_.get(bstack11l1lll111l_opy_, [])) > 0:
                hook = bstack11l1l1111ll_opy_[bstack11l1lll111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1l111ll1_opy_ in hook:
                    hook[TestFramework.bstack11l1l111ll1_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l111lllll_opy_(test) -> Dict[str, Any]:
        bstack1ll11_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡷࡩࡸࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤᦐ")
        test_id = bstack1l1lll1l1l1_opy_.__11l111l1l1l_opy_(test)
        test_name = test.name if hasattr(test, bstack1ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦑ")) else None
        bstack11l1lll1l11_opy_ = str(test.source) if hasattr(test, bstack1ll11_opy_ (u"ࠣࡵࡲࡹࡷࡩࡥࠣᦒ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1ll11_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᦓ")) else []
        bstack11l111llll1_opy_ =bstack1ll11_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧᦔ").format(bstack1ll11_opy_ (u"ࠦࠥࠨᦕ").join(test_tags), test_name) if test_tags else test_name
        bstack11l11l11111_opy_ = []
        if bstack11l1lll1l11_opy_:
            from browserstack_sdk.bstack1lll1ll11l1_opy_ import RobotHandler
            bstack11l11l11111_opy_ = RobotHandler.bstack1lll1l1ll11_opy_(bstack11l1lll1l11_opy_)
        if not bstack11l11l11111_opy_ and test_name:
            bstack11l11l11111_opy_ = [test_name]
        return {
            TestFramework.bstack1l11l1lll11_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111111_opy_: test_id,
            TestFramework.bstack1l11ll1ll1l_opy_: test_name,
            TestFramework.bstack11lll1llll1_opy_: test_id,
            TestFramework.bstack11l1lll1111_opy_: bstack11l1lll1l11_opy_,
            TestFramework.bstack11l11l1llll_opy_: test_tags,
            TestFramework.bstack11l1l1l1ll1_opy_: bstack11l111llll1_opy_,
            TestFramework.bstack11lll11l111_opy_: TestFramework.bstack11l1lll1l1l_opy_,
            TestFramework.bstack11ll1111l1l_opy_: test_id,
            TestFramework.bstack11l11l1111l_opy_: bstack11l11l11111_opy_
        }
    @staticmethod
    def __11l111l1l1l_opy_(test):
        bstack1ll11_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡺࡴࡩࡲࡷࡨࠤࡹ࡫ࡳࡵࠢࡌࡈࠥ࡬ࡲࡰ࡯ࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡺࡥࡴࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧᦖ")
        if hasattr(test, bstack1ll11_opy_ (u"ࠨࡩࡥࠤᦗ")):
            return test.id
        elif hasattr(test, bstack1ll11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡳࡧ࡭ࡦࠤᦘ")):
            return test.longname
        elif hasattr(test, bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᦙ")):
            return test.name
        return None