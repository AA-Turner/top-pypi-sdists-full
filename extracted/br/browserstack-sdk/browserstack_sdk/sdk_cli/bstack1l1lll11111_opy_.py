# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack111l1ll1ll_opy_ import bstack11l11ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111lllll_opy_,
    TestHookState,
    bstack1ll1lll1l11_opy_,
    bstack1l1l1l1l1ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11llllll1l1_opy_
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1llllll_opy_ import bstack1l1llll1l1l_opy_
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
bstack11lllllll1l_opy_ = bstack11llllll1l1_opy_()
bstack11l11llll11_opy_ = 1.0
bstack1l1111lllll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᣡ")
bstack11l11l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᣢ")
bstack11l11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᣣ")
bstack11l11l1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᣤ")
bstack11l11ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᣥ")
_11lllll1lll_opy_ = set()
class bstack1l1l1ll1ll1_opy_(TestFramework):
    bstack11l11l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᣦ")
    bstack11l11ll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᣧ")
    bstack11l1ll1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᣨ")
    bstack11l11lll111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᣩ")
    bstack11l1ll11lll_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᣪ")
    bstack11l11l1l11l_opy_: bool
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_ = None
    bstack1l1ll1l1ll1_opy_ = None
    bstack11l1l11l11l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l11lll11l_opy_: Dict[str, str],
        bstack1l11ll1l1ll_opy_: List[str] = [bstack1ll1lll_opy_ (u"ࠤࡵࡳࡧࡵࡴࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᣫ")],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_ = None,
        bstack1l1ll1l1ll1_opy_=None
    ):
        super().__init__(bstack1l11ll1l1ll_opy_, bstack11l11lll11l_opy_, bstack1ll1l11l1l1_opy_)
        self.bstack11l11l1l11l_opy_ = any(bstack1ll1lll_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࠤᣬ") in item.lower() for item in bstack1l11ll1l1ll_opy_)
        self.bstack1l1ll1l1ll1_opy_ = bstack1l1ll1l1ll1_opy_
    def track_event(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l1ll1ll1_opy_.bstack11l1l11l11l_opy_:
            bstack11l11ll11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᣭ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l11l1l11l_opy_:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࢁࡽࠣᣮ").format(str(self.bstack1l11ll1l1ll_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᣯ").format(args, kwargs))
            return
        instance = self.__11l1lll1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠣᣰ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1l1ll1ll1_opy_.bstack11l1l11l11l_opy_:
                bstack11ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࠤᣱ")
                name = bstack1ll1lll_opy_ (u"ࠤࠥᣲ")
                if (test_hook_state == TestHookState.PRE):
                    bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l1llll_opy_.value)
                    name = str(EVENTS.bstack11l11l1llll_opy_.name) + bstack1ll1lll_opy_ (u"ࠥ࠾ࠧᣳ") + str(test_framework_state.name)
                else:
                    bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l1ll1l_opy_.value)
                    name = str(EVENTS.bstack11l11l1ll1l_opy_.name) + bstack1ll1lll_opy_ (u"ࠦ࠿ࠨᣴ") + str(test_framework_state.name)
                TestFramework.bstack11l11ll1ll1_opy_(instance, name, bstack11ll1ll1l_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᣵ").format(e))
        try:
            if not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack11lll111lll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l1ll1ll1_opy_.__11l11l11lll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤ᣶").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l111ll11ll_opy_):
                    TestFramework.bstack1l1l11lll_opy_(instance, TestFramework.bstack1l111ll11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣ᣷").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l111ll1l11_opy_):
                    TestFramework.bstack1l1l11lll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢ᣸").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l1ll1ll1_opy_.__11l1l1ll111_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1lll11l1_opy_(instance, *args)
                self.__11l1l1ll1l1_opy_(instance)
            elif test_framework_state in bstack1l1l1ll1ll1_opy_.bstack11l1l11l11l_opy_:
                self.__11l1l1lll1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠧ᣹").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1l1ll1ll1_opy_.bstack11l1l11l11l_opy_:
                bstack11ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠥࠦ᣺")
                name = bstack1ll1lll_opy_ (u"ࠦࠧ᣻")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l1llll_opy_.name) + bstack1ll1lll_opy_ (u"ࠧࡀࠢ᣼") + str(test_framework_state.name)
                    bstack11ll1ll1l_opy_ = TestFramework.bstack11l1l111111_opy_(instance, name)
                    bstack1lll1lll11_opy_.end(EVENTS.bstack11l11l1llll_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᣽"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᣾"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11l1ll1l_opy_.name) + bstack1ll1lll_opy_ (u"ࠣ࠼ࠥ᣿") + str(test_framework_state.name)
                    bstack11ll1ll1l_opy_ = TestFramework.bstack11l1l111111_opy_(instance, name)
                    bstack1lll1lll11_opy_.end(EVENTS.bstack11l11l1ll1l_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᤀ"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᤁ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᤂ").format(e))
    def bstack1l111lll11l_opy_(self):
        return self.bstack11l11l1l11l_opy_
    def bstack1l1111111ll_opy_(self):
        return False
    def __11l11l111l1_opy_(self, *args):
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࡑࡣࡵࡷࡪࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡴࡨࡷࡺࡲࡴࠡࡱࡥ࡮ࡪࡩࡴࠣࠤࠥᤃ")
        if len(args) > 1 and hasattr(args[1], bstack1ll1lll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᤄ")):
            result = args[1]
            if result:
                return TestFramework.bstack1l111l11lll_opy_(result, [bstack1ll1lll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᤅ"), bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᤆ"), bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࡵ࡫ࡰࡩࠧᤇ"), bstack1ll1lll_opy_ (u"ࠥࡩࡳࡪࡴࡪ࡯ࡨࠦᤈ"), bstack1ll1lll_opy_ (u"ࠦࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠤᤉ")])
        return None
    def __11l1lll11l1_opy_(self, instance: bstack1ll111lllll_opy_, *args):
        result = self.__11l11l111l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1llll1ll_opy_ = None
        status = result.get(bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᤊ"), bstack1ll1lll_opy_ (u"ࠨࡎࡐࡖࠣࡖ࡚ࡔࠢᤋ"))
        if status == bstack1ll1lll_opy_ (u"ࠢࡇࡃࡌࡐࠧᤌ") and result.get(bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᤍ")):
            failure = [{bstack1ll1lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᤎ"): [result.get(bstack1ll1lll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᤏ"), bstack1ll1lll_opy_ (u"ࠦࠧᤐ"))]}]
            bstack1ll1llll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᤑ")
        bstack11l1l111l1l_opy_ = TestFramework.bstack11l1llll111_opy_
        if status == bstack1ll1lll_opy_ (u"ࠨࡐࡂࡕࡖࠦᤒ"):
            bstack11l1l111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᤓ")
        elif status == bstack1ll1lll_opy_ (u"ࠣࡈࡄࡍࡑࠨᤔ"):
            bstack11l1l111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᤕ")
        elif status == bstack1ll1lll_opy_ (u"ࠥࡗࡐࡏࡐࠣᤖ"):
            bstack11l1l111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᤗ")
        if bstack11l1l111l1l_opy_ != TestFramework.bstack11l1llll111_opy_:
            TestFramework.bstack1l1l11lll_opy_(instance, TestFramework.bstack1l1111ll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l11l1ll_opy_(instance, {
            TestFramework.bstack11lll11ll1l_opy_: failure,
            TestFramework.bstack11l1l1111ll_opy_: bstack1ll1llll1ll_opy_,
            TestFramework.bstack11lll11ll11_opy_: bstack11l1l111l1l_opy_,
        })
    def __11l1lll1111_opy_(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l11l11ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l11l11l11_opy_(test) if test else None
                if target:
                    self.__11l111lllll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᤘ"), None)
            elif hasattr(args[0], bstack1ll1lll_opy_ (u"ࠨࡩࡥࠤᤙ")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1ll1l111l1l_opy_(target) if target else None
        return instance
    def __11l1l1lll1l_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1ll11ll1_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack1l1l1ll1ll1_opy_.bstack11l11ll11l1_opy_, {})
        if not key in bstack11l1ll11ll1_opy_:
            bstack11l1ll11ll1_opy_[key] = []
        bstack11l1ll1l111_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack1l1l1ll1ll1_opy_.bstack11l1ll1lll1_opy_, {})
        if not key in bstack11l1ll1l111_opy_:
            bstack11l1ll1l111_opy_[key] = []
        bstack11l1ll1ll11_opy_ = {
            bstack1l1l1ll1ll1_opy_.bstack11l11ll11l1_opy_: bstack11l1ll11ll1_opy_,
            bstack1l1l1ll1ll1_opy_.bstack11l1ll1lll1_opy_: bstack11l1ll1l111_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1ll1lll_opy_ (u"ࠢࠣᤚ")
            if len(args) > 0 and hasattr(args[0], bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᤛ")):
                hook_name = args[0].name
            hook = {
                bstack1ll1lll_opy_ (u"ࠤ࡮ࡩࡾࠨᤜ"): key,
                TestFramework.bstack11l1lllll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1l11l_opy_: TestFramework.bstack11l1l1lll11_opy_,
                TestFramework.bstack11l11lllll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1l11ll11_opy_: [],
                TestFramework.bstack11l1l1l1l1l_opy_: hook_name,
                TestFramework.bstack11l11lll1ll_opy_: bstack1l1llll1l1l_opy_.bstack11l11llll1l_opy_()
            }
            bstack11l1ll11ll1_opy_[key].append(hook)
            bstack11l1ll1ll11_opy_[bstack1l1l1ll1ll1_opy_.bstack11l11lll111_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1llll_opy_ = bstack11l1ll11ll1_opy_.get(key, [])
            hook = bstack11l1ll1llll_opy_.pop() if bstack11l1ll1llll_opy_ else None
            if hook:
                result = self.__11l11l111l1_opy_(*args)
                if result:
                    bstack11l1l1l11l1_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᤝ"), TestFramework.bstack11l1l1lll11_opy_)
                    if bstack11l1l1l11l1_opy_ == bstack1ll1lll_opy_ (u"ࠦࡕࡇࡓࡔࠤᤞ"):
                        bstack11l1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ᤟")
                    elif bstack11l1l1l11l1_opy_ == bstack1ll1lll_opy_ (u"ࠨࡆࡂࡋࡏࠦᤠ"):
                        bstack11l1l1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᤡ")
                    if bstack11l1l1l11l1_opy_ != TestFramework.bstack11l1l1lll11_opy_:
                        hook[TestFramework.bstack11l1ll1l11l_opy_] = bstack11l1l1l11l1_opy_
                hook[TestFramework.bstack11l1ll11111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l11lll1ll_opy_] = bstack1l1llll1l1l_opy_.bstack11l11llll1l_opy_()
                self.bstack11l1l1llll1_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll1ll1l_opy_, [])
                if logs:
                    self.bstack1l111l1ll1l_opy_(instance, logs)
                bstack11l1ll1l111_opy_[key].append(hook)
                bstack11l1ll1ll11_opy_[bstack1l1l1ll1ll1_opy_.bstack11l1ll11lll_opy_] = key
        TestFramework.bstack11l1l11l1ll_opy_(instance, bstack11l1ll1ll11_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿ࠱ࡿࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࡿࢂࠨᤢ").format(key, test_hook_state, bstack11l1ll11ll1_opy_, bstack11l1ll1l111_opy_))
    def __11l11l11ll1_opy_(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll1lll_opy_ (u"ࠤ࡙ࠥࠦࡸࡡࡤ࡭ࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡱࡥࡺࡹࡲࡶࡩࠦࡥࡷࡧࡱࡸࡸࠦࠨࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡵࡿࡴࡦࡵࡷࠤ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࠢࠣࠤᤣ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᤤ"), None)
        bstack1ll1l11llll_opy_ = getattr(keyword, bstack1ll1lll_opy_ (u"ࠦࡹࡿࡰࡦࠤᤥ"), None)
        test_id = kwargs.get(bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᤦ"), None)
        if not test_id:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤࡱࡥࡺࡹࡲࡶࡩࡥࡥࡷࡧࡱࡸ࠿ࠦ࡮ࡰࠢࡷࡩࡸࡺ࡟ࡪࡦࠣ࡭ࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠣᤧ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll1l111l1l_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥ࡫ࡦࡻࡺࡳࡷࡪ࡟ࡦࡸࡨࡲࡹࡀࠠ࡯ࡱࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡥࡩࡥ࠿ࡾࢁࠧᤨ").format(test_id))
            return None
        bstack11l111llll1_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack1l1l1ll1ll1_opy_.bstack11l11l11l1l_opy_, {})
        if os.getenv(bstack1ll1lll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡌࡇ࡜࡛ࡔࡘࡄࡔࠤᤩ"), bstack1ll1lll_opy_ (u"ࠤ࠴ࠦᤪ")) == bstack1ll1lll_opy_ (u"ࠥ࠵ࠧᤫ"):
            bstack11l11l1111l_opy_ = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥ᤬").format(bstack1ll1l11llll_opy_, keyword_name)
            bstack11l11ll1l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11l111ll_opy_ = {
                bstack1ll1lll_opy_ (u"ࠧࡱࡥࡺࠤ᤭"): bstack11l11l1111l_opy_,
                bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᤮"): keyword_name,
                bstack1ll1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧ᤯"): bstack1ll1l11llll_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l11l111ll_opy_[bstack1ll1lll_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᤰ")] = uuid4().__str__()
                bstack11l11l111ll_opy_[bstack1l1l1ll1ll1_opy_.bstack11l11lllll1_opy_] = bstack11l11ll1l1l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11l111ll_opy_[bstack1l1l1ll1ll1_opy_.bstack11l1ll11111_opy_] = bstack11l11ll1l1l_opy_
                if len(args) > 1 and hasattr(args[1], bstack1ll1lll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᤱ")):
                    bstack11l11l111ll_opy_[bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᤲ")] = args[1].status
            if bstack11l11l1111l_opy_ in bstack11l111llll1_opy_:
                bstack11l111llll1_opy_[bstack11l11l1111l_opy_].update(bstack11l11l111ll_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠢࡷࡽࡵ࡫࠽ࡼࡿࠥᤳ").format(keyword_name, bstack1ll1l11llll_opy_))
            else:
                bstack11l111llll1_opy_[bstack11l11l1111l_opy_] = bstack11l11l111ll_opy_
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠡࡶࡼࡴࡪࡃࡻࡾࠤᤴ").format(keyword_name, bstack1ll1l11llll_opy_))
        TestFramework.bstack1l1l11lll_opy_(instance, bstack1l1l1ll1ll1_opy_.bstack11l11l11l1l_opy_, bstack11l111llll1_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡹ࠽ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠣᤵ").format(len(bstack11l111llll1_opy_), instance.ref()))
        return instance
    def __11l111lllll_opy_(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11l1ll1l_opy_.create_context(target)
        ob = bstack1ll111lllll_opy_(ctx, self.bstack1l11ll1l1ll_opy_, self.bstack11l11lll11l_opy_, test_framework_state)
        TestFramework.bstack11l1l11l1ll_opy_(ob, {
            TestFramework.bstack1l11lll111l_opy_: context.test_framework_name,
            TestFramework.bstack1l1111l1ll1_opy_: context.test_framework_version,
            TestFramework.bstack11l1lllll11_opy_: [],
            bstack1l1l1ll1ll1_opy_.bstack11l11l11l1l_opy_: {},
            bstack1l1l1ll1ll1_opy_.bstack11l1ll1lll1_opy_: {},
            bstack1l1l1ll1ll1_opy_.bstack11l11ll11l1_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1ll1lll_opy_ (u"ࠢࡴࡱࡸࡶࡨ࡫ࠢᤶ")):
            TestFramework.bstack1l1l11lll_opy_(ob, TestFramework.bstack11l11ll1lll_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1l1l11lll_opy_(ob, TestFramework.bstack1l11llll111_opy_, context.platform_index)
        TestFramework.bstack111llll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࢁࡽࠣᤷ").format(ctx.id, target, args, TestFramework.bstack111llll1l_opy_.keys()))
        return ob
    def bstack11llllll111_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1lll11ll_opy_ = (
            bstack1l1l1ll1ll1_opy_.bstack11l11lll111_opy_
            if bstack1ll11l1ll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1ll1ll1_opy_.bstack11l1ll11lll_opy_
        )
        hook = bstack1l1l1ll1ll1_opy_.bstack11l1l11llll_opy_(instance, bstack11l1lll11ll_opy_)
        entries = hook.get(TestFramework.bstack11l1l11ll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11l1lllll11_opy_, []))
        return entries
    def bstack1l111l1111l_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1lll11ll_opy_ = (
            bstack1l1l1ll1ll1_opy_.bstack11l11lll111_opy_
            if bstack1ll11l1ll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1ll1ll1_opy_.bstack11l1ll11lll_opy_
        )
        bstack1l1l1ll1ll1_opy_.bstack11l1ll111l1_opy_(instance, bstack11l1lll11ll_opy_)
        TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11l1lllll11_opy_, []).clear()
    def bstack11l1l1llll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᤸ")
        global _11lllll1lll_opy_
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚᤹ࠪ")]
        bstack1l1111111l1_opy_ = os.path.join(bstack11lllllll1l_opy_, (bstack1l1111lllll_opy_ + str(platform_index)), bstack11l11l1lll1_opy_)
        if not os.path.exists(bstack1l1111111l1_opy_) or not os.path.isdir(bstack1l1111111l1_opy_):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤ᤺").format(bstack1l1111111l1_opy_))
            return
        logs = hook.get(bstack1ll1lll_opy_ (u"ࠧࡲ࡯ࡨࡵ᤻ࠥ"), [])
        with os.scandir(bstack1l1111111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11lllll1lll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦ᤼").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1lll_opy_ (u"ࠢࠣ᤽")
                    log_entry = bstack1l1l1l1l1ll_opy_(
                        kind=bstack1ll1lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᤾"),
                        message=bstack1ll1lll_opy_ (u"ࠤࠥ᤿"),
                        level=bstack1ll1lll_opy_ (u"ࠥࠦ᥀"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111llll1l_opy_=entry.stat().st_size,
                        bstack11lllll1ll1_opy_=bstack1ll1lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᥁"),
                        bstack1l11111_opy_=os.path.abspath(entry.path),
                        bstack11l1ll111ll_opy_=hook.get(TestFramework.bstack11l1lllll1l_opy_)
                    )
                    logs.append(log_entry)
                    _11lllll1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᥂")]
        bstack11l1llll1l1_opy_ = os.path.join(bstack11lllllll1l_opy_, (bstack1l1111lllll_opy_ + str(platform_index)), bstack11l11l1lll1_opy_, bstack11l11ll1111_opy_)
        if not os.path.exists(bstack11l1llll1l1_opy_) or not os.path.isdir(bstack11l1llll1l1_opy_):
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣ᥃").format(bstack11l1llll1l1_opy_))
        else:
            self.logger.info(bstack1ll1lll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ᥄").format(bstack11l1llll1l1_opy_))
            with os.scandir(bstack11l1llll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11lllll1lll_opy_:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨ᥅").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1lll_opy_ (u"ࠤࠥ᥆")
                        log_entry = bstack1l1l1l1l1ll_opy_(
                            kind=bstack1ll1lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ᥇"),
                            message=bstack1ll1lll_opy_ (u"ࠦࠧ᥈"),
                            level=bstack1ll1lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤ᥉"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111llll1l_opy_=entry.stat().st_size,
                            bstack11lllll1ll1_opy_=bstack1ll1lll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ᥊"),
                            bstack1l11111_opy_=os.path.abspath(entry.path),
                            bstack1l111l11l1l_opy_=hook.get(TestFramework.bstack11l1lllll1l_opy_)
                        )
                        logs.append(log_entry)
                        _11lllll1lll_opy_.add(abs_path)
        hook[bstack1ll1lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ᥋")] = logs
    def bstack1l111l1ll1l_opy_(
        self,
        bstack1l1111ll111_opy_: bstack1ll111lllll_opy_,
        entries: List[bstack1l1l1l1l1ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧ᥌"))
        req.platform_index = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack1l11llll111_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᥍").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111ll111_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111ll111_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111ll111_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack1l11lll111l_opy_, bstack1ll1lll_opy_ (u"ࠥࠦ᥎"))
            log_entry.test_framework_version = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack1l1111l1ll1_opy_, bstack1ll1lll_opy_ (u"ࠦࠧ᥏"))
            log_entry.uuid = entry.bstack11l1ll111ll_opy_ or bstack1ll1lll_opy_ (u"ࠧࠨᥐ")
            log_entry.test_framework_state = bstack1l1111ll111_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᥑ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1lll_opy_ (u"ࠢࠣᥒ")
            if entry.kind == bstack1ll1lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᥓ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111llll1l_opy_
                log_entry.file_path = entry.bstack1l11111_opy_
        def bstack11llllll11l_opy_():
            bstack1ll1l111l_opy_ = datetime.now()
            try:
                self.bstack1l1ll1l1ll1_opy_.LogCreatedEvent(req)
                bstack1l1111ll111_opy_.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᥔ"), datetime.now() - bstack1ll1l111l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᥕ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack11llllll11l_opy_)
    def __11l1l1ll1l1_opy_(self, instance) -> None:
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᥖ")
        bstack11l1ll1ll11_opy_ = {bstack1ll1lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᥗ"): bstack1l1llll1l1l_opy_.bstack11l11llll1l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l11l1ll_opy_(instance, bstack11l1ll1ll11_opy_)
    @staticmethod
    def bstack11l1l11llll_opy_(instance: bstack1ll111lllll_opy_, bstack11l1lll11ll_opy_: str):
        bstack11l1l1lllll_opy_ = (
            bstack1l1l1ll1ll1_opy_.bstack11l1ll1lll1_opy_
            if bstack11l1lll11ll_opy_ == bstack1l1l1ll1ll1_opy_.bstack11l1ll11lll_opy_
            else bstack1l1l1ll1ll1_opy_.bstack11l11ll11l1_opy_
        )
        bstack11l11llllll_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1lll11ll_opy_, None)
        bstack11l1llll11l_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1l1lllll_opy_, None) if bstack11l11llllll_opy_ else None
        return (
            bstack11l1llll11l_opy_[bstack11l11llllll_opy_][-1]
            if isinstance(bstack11l1llll11l_opy_, dict) and len(bstack11l1llll11l_opy_.get(bstack11l11llllll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll111l1_opy_(instance: bstack1ll111lllll_opy_, bstack11l1lll11ll_opy_: str):
        hook = bstack1l1l1ll1ll1_opy_.bstack11l1l11llll_opy_(instance, bstack11l1lll11ll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1l11ll11_opy_, []).clear()
    @staticmethod
    def __11l1l1ll111_opy_(instance: bstack1ll111lllll_opy_, *args):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࡒࡵࡳࡨ࡫ࡳࡴࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦࡵࠥࠦࠧᥘ")
        if len(args) < 1:
            return
        if os.getenv(bstack1ll1lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᥙ"), bstack1ll1lll_opy_ (u"ࠣ࠳ࠥᥚ")) != bstack1ll1lll_opy_ (u"ࠤ࠴ࠦᥛ"):
            bstack1l1l1ll1ll1_opy_.logger.warning(bstack1ll1lll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡱࡵࡧࡴࠤᥜ"))
            return
        message = args[0]
        if not hasattr(message, bstack1ll1lll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᥝ")):
            return
        is_screenshot = hasattr(message, bstack1ll1lll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᥞ")) and message.kind == bstack1ll1lll_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᥟ")
        log_entry = bstack1l1l1l1l1ll_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack1l111lll1ll_opy_,
            message=message.message if hasattr(message, bstack1ll1lll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᥠ")) else bstack1ll1lll_opy_ (u"ࠣࠤᥡ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1ll1lll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬ࠣᥢ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1ll1lll_opy_ (u"ࠥࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠣᥣ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1ll1lll_opy_ (u"ࠦࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠢᥤ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l1l111lll_opy_ = {
            bstack1ll1lll_opy_ (u"࡙ࠧࡅࡕࡗࡓࠦᥥ"): (bstack1l1l1ll1ll1_opy_.bstack11l11lll111_opy_, bstack1l1l1ll1ll1_opy_.bstack11l11ll11l1_opy_),
            bstack1ll1lll_opy_ (u"ࠨࡔࡆࡃࡕࡈࡔ࡝ࡎࠣᥦ"): (bstack1l1l1ll1ll1_opy_.bstack11l1ll11lll_opy_, bstack1l1l1ll1ll1_opy_.bstack11l1ll1lll1_opy_),
        }
        bstack11l11l1l111_opy_ = None
        if len(args) > 1:
            bstack11l11l1l111_opy_ = args[1]
        if bstack11l11l1l111_opy_ and bstack11l11l1l111_opy_ in bstack11l1l111lll_opy_:
            bstack11l1l1ll11l_opy_, bstack11l1l1lllll_opy_ = bstack11l1l111lll_opy_[bstack11l11l1l111_opy_]
            bstack11l1l111l11_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1l1ll11l_opy_, None)
            bstack11l1llll11l_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1l1lllll_opy_, None) if bstack11l1l111l11_opy_ else None
            if isinstance(bstack11l1llll11l_opy_, dict) and len(bstack11l1llll11l_opy_.get(bstack11l1l111l11_opy_, [])) > 0:
                hook = bstack11l1llll11l_opy_[bstack11l1l111l11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1l11ll11_opy_ in hook:
                    hook[TestFramework.bstack11l1l11ll11_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11l1lllll11_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l11l11lll_opy_(test) -> Dict[str, Any]:
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࡓࡥࡷࡹࡥࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡸࡪࡹࡴࠡࡱࡥ࡮ࡪࡩࡴࠣࠤࠥᥧ")
        test_id = bstack1l1l1ll1ll1_opy_.__11l11l11l11_opy_(test)
        test_name = test.name if hasattr(test, bstack1ll1lll_opy_ (u"ࠣࡰࡤࡱࡪࠨᥨ")) else None
        bstack11l1l1ll1ll_opy_ = str(test.source) if hasattr(test, bstack1ll1lll_opy_ (u"ࠤࡶࡳࡺࡸࡣࡦࠤᥩ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1ll1lll_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᥪ")) else []
        bstack11l11l11111_opy_ =bstack1ll1lll_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨᥫ").format(bstack1ll1lll_opy_ (u"ࠧࠦࠢᥬ").join(test_tags), test_name) if test_tags else test_name
        bstack11l11l1l1ll_opy_ = []
        if bstack11l1l1ll1ll_opy_:
            from browserstack_sdk.bstack1llll1l1ll1_opy_ import RobotHandler
            bstack11l11l1l1ll_opy_ = RobotHandler.bstack1llll1l1111_opy_(bstack11l1l1ll1ll_opy_)
        if not bstack11l11l1l1ll_opy_ and test_name:
            bstack11l11l1l1ll_opy_ = [test_name]
        return {
            TestFramework.bstack1l1l1111l11_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111lll_opy_: test_id,
            TestFramework.bstack1l1l111111l_opy_: test_name,
            TestFramework.bstack11lllll1111_opy_: test_id,
            TestFramework.bstack11l1l1l1111_opy_: bstack11l1l1ll1ll_opy_,
            TestFramework.bstack11l1l1l1lll_opy_: test_tags,
            TestFramework.bstack11l1l11l1l1_opy_: bstack11l11l11111_opy_,
            TestFramework.bstack11lll11ll11_opy_: TestFramework.bstack11l1llll111_opy_,
            TestFramework.bstack11ll111llll_opy_: test_id,
            TestFramework.bstack11l11ll111l_opy_: bstack11l11l1l1ll_opy_
        }
    @staticmethod
    def __11l11l11l11_opy_(test):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡻ࡮ࡪࡳࡸࡩࠥࡺࡥࡴࡶࠣࡍࡉࠦࡦࡳࡱࡰࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡴࡦࡵࡷࠤࡴࡨࡪࡦࡥࡷࠦࠧࠨᥭ")
        if hasattr(test, bstack1ll1lll_opy_ (u"ࠢࡪࡦࠥ᥮")):
            return test.id
        elif hasattr(test, bstack1ll1lll_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡴࡡ࡮ࡧࠥ᥯")):
            return test.longname
        elif hasattr(test, bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᥰ")):
            return test.name
        return None