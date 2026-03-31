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
bstack11lllll1l1l_opy_ = bstack1ll11_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᡦ")
bstack11l11l11lll_opy_ = bstack1ll11_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᡧ")
bstack11l11l11l1l_opy_ = bstack1ll11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᡨ")
bstack11l11l11ll1_opy_ = bstack1ll11_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᡩ")
bstack11l11l111ll_opy_ = bstack1ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᡪ")
_1l1111111l1_opy_ = set()
class bstack1l1lllll1l1_opy_(TestFramework):
    bstack11l11ll111l_opy_ = bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᡫ")
    bstack11l1lll11l1_opy_ = bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᡬ")
    bstack11l1l1ll111_opy_ = bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᡭ")
    bstack11l1l1ll1ll_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᡮ")
    bstack11l11lll11l_opy_ = bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᡯ")
    bstack11l1l111111_opy_: bool
    bstack1ll11llll11_opy_: bstack1ll11llllll_opy_  = None
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
        bstack1l1l111lll1_opy_: List[str]=[bstack1ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᡰ")],
        bstack1ll11llll11_opy_: bstack1ll11llllll_opy_=None,
        bstack1l1ll1ll111_opy_=None
    ):
        super().__init__(bstack1l1l111lll1_opy_, bstack11l11l1l1ll_opy_, bstack1ll11llll11_opy_)
        self.bstack11l1l111111_opy_ = any(bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᡱ") in item.lower() for item in bstack1l1l111lll1_opy_)
        self.bstack1l1ll1ll111_opy_ = bstack1l1ll1ll111_opy_
    def track_event(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1lllll1l1_opy_.bstack11l1l1l1l1l_opy_:
            bstack11l1ll1l11l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᡲ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠣࠤᡳ"))
            return
        if not self.bstack11l1l111111_opy_:
            self.logger.warning(bstack1ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᡴ") + str(str(self.bstack1l1l111lll1_opy_)) + bstack1ll11_opy_ (u"ࠥࠦᡵ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᡶ") + str(kwargs) + bstack1ll11_opy_ (u"ࠧࠨᡷ"))
            return
        instance = self.__11l11ll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᡸ") + str(args) + bstack1ll11_opy_ (u"ࠢࠣ᡹"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1lllll1l1_opy_.bstack11l1l1l1l1l_opy_:
                bstack1l11ll1ll1_opy_ = bstack1ll11_opy_ (u"ࠣࠤ᡺")
                name = bstack1ll11_opy_ (u"ࠤࠥ᡻")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l11l11l11_opy_.value)
                    name = str(EVENTS.bstack11l11l11l11_opy_.name)+bstack1ll11_opy_ (u"ࠥ࠾ࠧ᡼")+str(test_framework_state.name)
                else:
                    bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l11l111l1_opy_.value)
                    name = str(EVENTS.bstack11l11l111l1_opy_.name)+bstack1ll11_opy_ (u"ࠦ࠿ࠨ᡽")+str(test_framework_state.name)
                TestFramework.bstack11l1l1lll1l_opy_(instance, name, bstack1l11ll1ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤ᡾").format(e))
        try:
            if not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack11lll111111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1lllll1l1_opy_.__11l1l11l111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᡿") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠢࠣᢀ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l111ll1111_opy_):
                    TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack1l111ll1111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᢁ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠤࠥᢂ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack11lllll1lll_opy_):
                    TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack11lllll1lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᢃ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠦࠧᢄ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1lllll1l1_opy_.__11l1ll11ll1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l111l11_opy_(instance, *args)
                self.__11l1ll1l1l1_opy_(instance)
            elif test_framework_state in bstack1l1lllll1l1_opy_.bstack11l1l1l1l1l_opy_:
                self.__11l11l1l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᢅ") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠨࠢᢆ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l11llll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1lllll1l1_opy_.bstack11l1l1l1l1l_opy_:
                bstack1l11ll1ll1_opy_ = bstack1ll11_opy_ (u"ࠢࠣᢇ")
                name = bstack1ll11_opy_ (u"ࠣࠤᢈ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l11l11_opy_.name)+bstack1ll11_opy_ (u"ࠤ࠽ࠦᢉ")+str(test_framework_state.name)
                    bstack1l11ll1ll1_opy_ = TestFramework.bstack11l1l1ll11l_opy_(instance, name)
                    bstack11ll11l1ll_opy_.end(EVENTS.bstack11l11l11l11_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᢊ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᢋ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11l111l1_opy_.name)+bstack1ll11_opy_ (u"ࠧࡀࠢᢌ")+str(test_framework_state.name)
                    bstack1l11ll1ll1_opy_ = TestFramework.bstack11l1l1ll11l_opy_(instance, name)
                    bstack11ll11l1ll_opy_.end(EVENTS.bstack11l11l111l1_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᢍ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᢎ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᢏ").format(e))
    def bstack1l111l1l11l_opy_(self):
        return self.bstack11l1l111111_opy_
    def bstack11lllllll1l_opy_(self):
        return False
    def __11l1ll11111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᢐ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111l11l1l_opy_(rep, [bstack1ll11_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᢑ"), bstack1ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᢒ"), bstack1ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᢓ"), bstack1ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᢔ"), bstack1ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᢕ"), bstack1ll11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᢖ")])
        return None
    def __11l1l111l11_opy_(self, instance: bstack1l1l1l111l1_opy_, *args):
        result = self.__11l1ll11111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lll111l_opy_ = None
        if result.get(bstack1ll11_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᢗ"), None) == bstack1ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᢘ") and len(args) > 1 and getattr(args[1], bstack1ll11_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᢙ"), None) is not None:
            failure = [{bstack1ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᢚ"): [args[1].excinfo.exconly(), result.get(bstack1ll11_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᢛ"), None)]}]
            bstack1ll1lll111l_opy_ = bstack1ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᢜ") if bstack1ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᢝ") in getattr(args[1].excinfo, bstack1ll11_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᢞ"), bstack1ll11_opy_ (u"ࠥࠦᢟ")) else bstack1ll11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᢠ")
        bstack11l1lll11ll_opy_ = result.get(bstack1ll11_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᢡ"), TestFramework.bstack11l1lll1l1l_opy_)
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
            instance = self.__11l1l111lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll11l1_opy_ bstack11l1l1111l1_opy_ this to be bstack1ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᢢ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l11llllll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll11_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᢣ"), None), bstack1ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᢤ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᢥ"), None):
                target = args[0].nodeid
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
        bstack11l11lllll1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lllll1l1_opy_.bstack11l1lll11l1_opy_, {})
        if not key in bstack11l11lllll1_opy_:
            bstack11l11lllll1_opy_[key] = []
        bstack11l1l11llll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lllll1l1_opy_.bstack11l1l1ll111_opy_, {})
        if not key in bstack11l1l11llll_opy_:
            bstack11l1l11llll_opy_[key] = []
        bstack11l11l1l111_opy_ = {
            bstack1l1lllll1l1_opy_.bstack11l1lll11l1_opy_: bstack11l11lllll1_opy_,
            bstack1l1lllll1l1_opy_.bstack11l1l1ll111_opy_: bstack11l1l11llll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1ll11_opy_ (u"ࠥ࡯ࡪࡿࠢᢦ"): key,
                TestFramework.bstack11l1l11ll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1l11lll1_opy_: TestFramework.bstack11l11l1l1l1_opy_,
                TestFramework.bstack11l11l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1l111ll1_opy_: [],
                TestFramework.bstack11l1ll1111l_opy_: args[1] if len(args) > 1 else bstack1ll11_opy_ (u"ࠫࠬᢧ"),
                TestFramework.bstack11l1l1l1lll_opy_: bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()
            }
            bstack11l11lllll1_opy_[key].append(hook)
            bstack11l11l1l111_opy_[bstack1l1lllll1l1_opy_.bstack11l1l1ll1ll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll11l1l_opy_ = bstack11l11lllll1_opy_.get(key, [])
            hook = bstack11l1ll11l1l_opy_.pop() if bstack11l1ll11l1l_opy_ else None
            if hook:
                result = self.__11l1ll11111_opy_(*args)
                if result:
                    bstack11l1ll11lll_opy_ = result.get(bstack1ll11_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᢨ"), TestFramework.bstack11l11l1l1l1_opy_)
                    if bstack11l1ll11lll_opy_ != TestFramework.bstack11l11l1l1l1_opy_:
                        hook[TestFramework.bstack11l1l11lll1_opy_] = bstack11l1ll11lll_opy_
                hook[TestFramework.bstack11l1ll111l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1lll_opy_]= bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll111ll_opy_, [])
                if logs: self.bstack11llllll1ll_opy_(instance, logs)
                bstack11l1l11llll_opy_[key].append(hook)
                bstack11l11l1l111_opy_[bstack1l1lllll1l1_opy_.bstack11l11lll11l_opy_] = key
        TestFramework.bstack11l1l1l1111_opy_(instance, bstack11l11l1l111_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁᢩࠧ") + str(bstack11l1l11llll_opy_) + bstack1ll11_opy_ (u"ࠢࠣᢪ"))
    def __11l1l111lll_opy_(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111l11l1l_opy_(args[0], [bstack1ll11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᢫"), bstack1ll11_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥ᢬"), bstack1ll11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥ᢭"), bstack1ll11_opy_ (u"ࠦ࡮ࡪࡳࠣ᢮"), bstack1ll11_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢ᢯"), bstack1ll11_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᢰ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᢱ")) else fixturedef.get(bstack1ll11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᢲ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᢳ")) else None
        node = request.node if hasattr(request, bstack1ll11_opy_ (u"ࠥࡲࡴࡪࡥࠣᢴ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᢵ")) else None
        baseid = fixturedef.get(bstack1ll11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᢶ"), None) or bstack1ll11_opy_ (u"ࠨࠢᢷ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll11_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᢸ")):
            target = bstack1l1lllll1l1_opy_.__11l1l1l111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll11_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᢹ")) else None
            if target and not TestFramework.bstack1ll111l1lll_opy_(target):
                self.__11l11llllll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᢺ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠥࠦᢻ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᢼ") + str(target) + bstack1ll11_opy_ (u"ࠧࠨᢽ"))
            return None
        instance = TestFramework.bstack1ll111l1lll_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᢾ") + str(target) + bstack1ll11_opy_ (u"ࠢࠣᢿ"))
            return None
        bstack11l11ll11l1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack1l1lllll1l1_opy_.bstack11l11ll111l_opy_, {})
        if os.getenv(bstack1ll11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᣀ"), bstack1ll11_opy_ (u"ࠤ࠴ࠦᣁ")) == bstack1ll11_opy_ (u"ࠥ࠵ࠧᣂ"):
            bstack11l1ll1ll11_opy_ = bstack1ll11_opy_ (u"ࠦ࠿ࠨᣃ").join((scope, fixturename))
            bstack11l1ll1llll_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11ll1l1l_opy_ = {
                bstack1ll11_opy_ (u"ࠧࡱࡥࡺࠤᣄ"): bstack11l1ll1ll11_opy_,
                bstack1ll11_opy_ (u"ࠨࡴࡢࡩࡶࠦᣅ"): bstack1l1lllll1l1_opy_.__11l11lll111_opy_(request.node),
                bstack1ll11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᣆ"): fixturedef,
                bstack1ll11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᣇ"): scope,
                bstack1ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᣈ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᣉ"), None)):
                    bstack11l11ll1l1l_opy_[bstack1ll11_opy_ (u"ࠦࡹࡿࡰࡦࠤᣊ")] = TestFramework.bstack1l111l11l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l11ll1l1l_opy_[bstack1ll11_opy_ (u"ࠧࡻࡵࡪࡦࠥᣋ")] = uuid4().__str__()
                bstack11l11ll1l1l_opy_[bstack1l1lllll1l1_opy_.bstack11l11l1ll11_opy_] = bstack11l1ll1llll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11ll1l1l_opy_[bstack1l1lllll1l1_opy_.bstack11l1ll111l1_opy_] = bstack11l1ll1llll_opy_
            if bstack11l1ll1ll11_opy_ in bstack11l11ll11l1_opy_:
                bstack11l11ll11l1_opy_[bstack11l1ll1ll11_opy_].update(bstack11l11ll1l1l_opy_)
                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᣌ") + str(bstack11l11ll11l1_opy_[bstack11l1ll1ll11_opy_]) + bstack1ll11_opy_ (u"ࠢࠣᣍ"))
            else:
                bstack11l11ll11l1_opy_[bstack11l1ll1ll11_opy_] = bstack11l11ll1l1l_opy_
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᣎ") + str(len(bstack11l11ll11l1_opy_)) + bstack1ll11_opy_ (u"ࠤࠥᣏ"))
        TestFramework.bstack1l11lllll_opy_(instance, bstack1l1lllll1l1_opy_.bstack11l11ll111l_opy_, bstack11l11ll11l1_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᣐ") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠦࠧᣑ"))
        return instance
    def __11l11llllll_opy_(
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
            bstack1l1lllll1l1_opy_.bstack11l11ll111l_opy_: {},
            bstack1l1lllll1l1_opy_.bstack11l1l1ll111_opy_: {},
            bstack1l1lllll1l1_opy_.bstack11l1lll11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l11lllll_opy_(ob, TestFramework.bstack11l1l11l1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l11lllll_opy_(ob, TestFramework.bstack1l11llll11l_opy_, context.platform_index)
        TestFramework.bstack1l1l111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᣒ") + str(TestFramework.bstack1l1l111l_opy_.keys()) + bstack1ll11_opy_ (u"ࠨࠢᣓ"))
        return ob
    def bstack1l1111l1l1l_opy_(self, instance: bstack1l1l1l111l1_opy_, bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1ll1l1_opy_ = (
            bstack1l1lllll1l1_opy_.bstack11l1l1ll1ll_opy_
            if bstack1ll11l11lll_opy_[1] == TestHookState.PRE
            else bstack1l1lllll1l1_opy_.bstack11l11lll11l_opy_
        )
        hook = bstack1l1lllll1l1_opy_.bstack11l1l11l11l_opy_(instance, bstack11l1l1ll1l1_opy_)
        entries = hook.get(TestFramework.bstack11l1l111ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, []))
        return entries
    def bstack1l1111llll1_opy_(self, instance: bstack1l1l1l111l1_opy_, bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1ll1l1_opy_ = (
            bstack1l1lllll1l1_opy_.bstack11l1l1ll1ll_opy_
            if bstack1ll11l11lll_opy_[1] == TestHookState.PRE
            else bstack1l1lllll1l1_opy_.bstack11l11lll11l_opy_
        )
        bstack1l1lllll1l1_opy_.bstack11l1l1l11l1_opy_(instance, bstack11l1l1ll1l1_opy_)
        TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, []).clear()
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᣔ")
        global _1l1111111l1_opy_
        platform_index = os.environ[bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᣕ")]
        bstack1l111l111ll_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), bstack11l11l11ll1_opy_)
        if not os.path.exists(bstack1l111l111ll_opy_) or not os.path.isdir(bstack1l111l111ll_opy_):
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢᣖ").format(bstack1l111l111ll_opy_))
            return
        logs = hook.get(bstack1ll11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᣗ"), [])
        with os.scandir(bstack1l111l111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1111111l1_opy_:
                    self.logger.info(bstack1ll11_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᣘ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll11_opy_ (u"ࠧࠨᣙ")
                    log_entry = bstack1l1l1l1lll1_opy_(
                        kind=bstack1ll11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᣚ"),
                        message=bstack1ll11_opy_ (u"ࠢࠣᣛ"),
                        level=bstack1ll11_opy_ (u"ࠣࠤᣜ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11llll1lll1_opy_=entry.stat().st_size,
                        bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᣝ"),
                        bstack1l11ll_opy_=os.path.abspath(entry.path),
                        bstack11l1l1lllll_opy_=hook.get(TestFramework.bstack11l1l11ll1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1111111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᣞ")]
        bstack11l1l1llll1_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), bstack11l11l11ll1_opy_, bstack11l11l111ll_opy_)
        if not os.path.exists(bstack11l1l1llll1_opy_) or not os.path.isdir(bstack11l1l1llll1_opy_):
            self.logger.info(bstack1ll11_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᣟ").format(bstack11l1l1llll1_opy_))
        else:
            self.logger.info(bstack1ll11_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᣠ").format(bstack11l1l1llll1_opy_))
            with os.scandir(bstack11l1l1llll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1111111l1_opy_:
                        self.logger.info(bstack1ll11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᣡ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll11_opy_ (u"ࠢࠣᣢ")
                        log_entry = bstack1l1l1l1lll1_opy_(
                            kind=bstack1ll11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᣣ"),
                            message=bstack1ll11_opy_ (u"ࠤࠥᣤ"),
                            level=bstack1ll11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᣥ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11llll1lll1_opy_=entry.stat().st_size,
                            bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᣦ"),
                            bstack1l11ll_opy_=os.path.abspath(entry.path),
                            bstack1l111l1ll11_opy_=hook.get(TestFramework.bstack11l1l11ll1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1111111l1_opy_.add(abs_path)
        hook[bstack1ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᣧ")] = logs
    def bstack11llllll1ll_opy_(
        self,
        bstack1l1111ll11l_opy_: bstack1l1l1l111l1_opy_,
        entries: List[bstack1l1l1l1lll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᣨ"))
        req.platform_index = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11llll11l_opy_)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᣩ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111ll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111ll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111ll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11l11llll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11111lll1_opy_)
            log_entry.uuid = entry.bstack11l1l1lllll_opy_
            log_entry.test_framework_state = bstack1l1111ll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᣪ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll11_opy_ (u"ࠤࠥᣫ")
            if entry.kind == bstack1ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᣬ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11llll1lll1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l111l1llll_opy_():
            bstack11l111ll1_opy_ = datetime.now()
            try:
                self.bstack1l1ll1ll111_opy_.LogCreatedEvent(req)
                bstack1l1111ll11l_opy_.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᣭ"), datetime.now() - bstack11l111ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᣮ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll11llll11_opy_.enqueue(bstack1l111l1llll_opy_)
    def __11l1ll1l1l1_opy_(self, instance) -> None:
        bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᣯ")
        bstack11l11l1l111_opy_ = {bstack1ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᣰ"): bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l1l1111_opy_(instance, bstack11l11l1l111_opy_)
    @staticmethod
    def bstack11l1l11l11l_opy_(instance: bstack1l1l1l111l1_opy_, bstack11l1l1ll1l1_opy_: str):
        bstack11l11lll1l1_opy_ = (
            bstack1l1lllll1l1_opy_.bstack11l1l1ll111_opy_
            if bstack11l1l1ll1l1_opy_ == bstack1l1lllll1l1_opy_.bstack11l11lll11l_opy_
            else bstack1l1lllll1l1_opy_.bstack11l1lll11l1_opy_
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
        hook = bstack1l1lllll1l1_opy_.bstack11l1l11l11l_opy_(instance, bstack11l1l1ll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1l111ll1_opy_, []).clear()
    @staticmethod
    def __11l1ll11ll1_opy_(instance: bstack1l1l1l111l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᣱ"), None)):
            return
        if os.getenv(bstack1ll11_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᣲ"), bstack1ll11_opy_ (u"ࠥ࠵ࠧᣳ")) != bstack1ll11_opy_ (u"ࠦ࠶ࠨᣴ"):
            bstack1l1lllll1l1_opy_.logger.warning(bstack1ll11_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᣵ"))
            return
        bstack11l11lll1ll_opy_ = {
            bstack1ll11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ᣶"): (bstack1l1lllll1l1_opy_.bstack11l1l1ll1ll_opy_, bstack1l1lllll1l1_opy_.bstack11l1lll11l1_opy_),
            bstack1ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ᣷"): (bstack1l1lllll1l1_opy_.bstack11l11lll11l_opy_, bstack1l1lllll1l1_opy_.bstack11l1l1ll111_opy_),
        }
        for when in (bstack1ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ᣸"), bstack1ll11_opy_ (u"ࠤࡦࡥࡱࡲࠢ᣹"), bstack1ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ᣺")):
            bstack11l1ll1ll1l_opy_ = args[1].get_records(when)
            if not bstack11l1ll1ll1l_opy_:
                continue
            records = [
                bstack1l1l1l1lll1_opy_(
                    kind=TestFramework.bstack11lllllllll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll11_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢ᣻")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll11_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨ᣼")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1ll1ll1l_opy_
                if isinstance(getattr(r, bstack1ll11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᣽"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l11ll1ll1_opy_, bstack11l11lll1l1_opy_ = bstack11l11lll1ll_opy_.get(when, (None, None))
            bstack11l1lll111l_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack11l11ll1ll1_opy_, None) if bstack11l11ll1ll1_opy_ else None
            bstack11l1l1111ll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, bstack11l11lll1l1_opy_, None) if bstack11l1lll111l_opy_ else None
            if isinstance(bstack11l1l1111ll_opy_, dict) and len(bstack11l1l1111ll_opy_.get(bstack11l1lll111l_opy_, [])) > 0:
                hook = bstack11l1l1111ll_opy_[bstack11l1lll111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1l111ll1_opy_ in hook:
                    hook[TestFramework.bstack11l1l111ll1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l1l11l111_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1lllll1l1_opy_.__11l1l1l111l_opy_(test.location) if hasattr(test, bstack1ll11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤ᣾")) else getattr(test, bstack1ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᣿"), None)
        test_name = test.name if hasattr(test, bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤀ")) else None
        bstack11l1lll1l11_opy_ = test.fspath.strpath if hasattr(test, bstack1ll11_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᤁ")) and test.fspath else None
        if not test_id or not test_name or not bstack11l1lll1l11_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll11_opy_ (u"ࠦࡴࡨࡪࠣᤂ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l11l11111_opy_ = []
        try:
            bstack11l11l11111_opy_ = bstack11l11l1lll_opy_.bstack1lll1l1ll11_opy_(test)
        except:
            bstack1l1lllll1l1_opy_.logger.warning(bstack1ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᤃ"))
        return {
            TestFramework.bstack1l11l1lll11_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111111_opy_: test_id,
            TestFramework.bstack1l11ll1ll1l_opy_: test_name,
            TestFramework.bstack11lll1llll1_opy_: getattr(test, bstack1ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᤄ"), None),
            TestFramework.bstack11l1lll1111_opy_: bstack11l1lll1l11_opy_,
            TestFramework.bstack11l11l1llll_opy_: bstack1l1lllll1l1_opy_.__11l11lll111_opy_(test),
            TestFramework.bstack11l1l1l1ll1_opy_: code,
            TestFramework.bstack11lll11l111_opy_: TestFramework.bstack11l1lll1l1l_opy_,
            TestFramework.bstack11ll1111l1l_opy_: test_id,
            TestFramework.bstack11l11l1111l_opy_: bstack11l11l11111_opy_
        }
    @staticmethod
    def __11l11lll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll11_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᤅ"), [])
            markers.extend([getattr(m, bstack1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᤆ"), None) for m in own_markers if getattr(m, bstack1ll11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤇ"), None)])
            current = getattr(current, bstack1ll11_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᤈ"), None)
        return markers
    @staticmethod
    def __11l1l1l111l_opy_(location):
        return bstack1ll11_opy_ (u"ࠦ࠿ࡀࠢᤉ").join(filter(lambda x: isinstance(x, str), location))