# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1l1ll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1111l111l1_opy_ import bstack111l1llllll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11ll11l_opy_,
    TestHookState,
    bstack1ll1lll1l1l_opy_,
    bstack11lllllll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1ll1lllll_opy_
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l11l_opy_ import bstack1l1ll1111ll_opy_
from bstack_utils.bstack1l1l1111_opy_ import bstack111l1l1l11_opy_
bstack11l1llll1l1_opy_ = bstack1l1ll1lllll_opy_()
bstack111ll111ll1_opy_ = 1.0
bstack11ll111llll_opy_ = bstack111l_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᨭ")
bstack111l1lll111_opy_ = bstack111l_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᨮ")
bstack111l1lll11l_opy_ = bstack111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᨯ")
bstack111l1lll1l1_opy_ = bstack111l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᨰ")
bstack111l1ll1ll1_opy_ = bstack111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᨱ")
_11ll1111l1l_opy_ = set()
class bstack1l1111l1lll_opy_(TestFramework):
    bstack111lll11111_opy_ = bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᨲ")
    bstack111ll11l111_opy_ = bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᨳ")
    bstack111ll1lll11_opy_ = bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᨴ")
    bstack111ll111lll_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᨵ")
    bstack111ll1l1ll1_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᨶ")
    bstack111l1llll1l_opy_: bool
    bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_  = None
    bstack11l11lll11_opy_ = None
    bstack1l1l1l1lll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1lll1l111_opy_: Dict[str, str],
        bstack1l1ll1ll11l_opy_: List[str]=[bstack111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᨷ")],
        bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_=None,
        bstack11l11lll11_opy_=None
    ):
        super().__init__(bstack1l1ll1ll11l_opy_, bstack1l1lll1l111_opy_, bstack1l1l1ll11l1_opy_)
        self.bstack111l1llll1l_opy_ = any(bstack111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᨸ") in item.lower() for item in bstack1l1ll1ll11l_opy_)
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
    def track_event(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1111l1lll_opy_.bstack1l1l1l1lll1_opy_:
            bstack111l1llllll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᨹ") + str(test_hook_state) + bstack111l_opy_ (u"ࠣࠤᨺ"))
            return
        if not self.bstack111l1llll1l_opy_:
            self.logger.warning(bstack111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᨻ") + str(str(self.bstack1l1ll1ll11l_opy_)) + bstack111l_opy_ (u"ࠥࠦᨼ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᨽ") + str(kwargs) + bstack111l_opy_ (u"ࠧࠨᨾ"))
            return
        instance = self.__111lll11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᨿ") + str(args) + bstack111l_opy_ (u"ࠢࠣᩀ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1111l1lll_opy_.bstack1l1l1l1lll1_opy_:
                bstack1l1l111lll_opy_ = bstack111l_opy_ (u"ࠣࠤᩁ")
                name = bstack111l_opy_ (u"ࠤࠥᩂ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111l1llll11_opy_.value)
                    name = str(EVENTS.bstack111l1llll11_opy_.name)+bstack111l_opy_ (u"ࠥ࠾ࠧᩃ")+str(test_framework_state.name)
                else:
                    bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111l1lll1ll_opy_.value)
                    name = str(EVENTS.bstack111l1lll1ll_opy_.name)+bstack111l_opy_ (u"ࠦ࠿ࠨᩄ")+str(test_framework_state.name)
                TestFramework.bstack111ll1llll1_opy_(instance, name, bstack1l1l111lll_opy_)
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᩅ").format(e))
        try:
            if not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1ll111l1l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1111l1lll_opy_.__111ll111l11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111l_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᩆ") + str(test_hook_state) + bstack111l_opy_ (u"ࠢࠣᩇ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᩈ") + str(test_hook_state) + bstack111l_opy_ (u"ࠤࠥᩉ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᩊ") + str(test_hook_state) + bstack111l_opy_ (u"ࠦࠧᩋ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1111l1lll_opy_.__111ll1lllll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll1lll1_opy_(instance, *args)
                self.__1l1l1l11l11_opy_(instance)
            elif test_framework_state in bstack1l1111l1lll_opy_.bstack1l1l1l1lll1_opy_:
                self.__111ll1111l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᩌ") + str(instance.ref()) + bstack111l_opy_ (u"ࠨࠢᩍ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l1l11lll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1111l1lll_opy_.bstack1l1l1l1lll1_opy_:
                bstack1l1l111lll_opy_ = bstack111l_opy_ (u"ࠢࠣᩎ")
                name = bstack111l_opy_ (u"ࠣࠤᩏ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111l1llll11_opy_.name)+bstack111l_opy_ (u"ࠤ࠽ࠦᩐ")+str(test_framework_state.name)
                    bstack1l1l111lll_opy_ = TestFramework.bstack111ll1l1lll_opy_(instance, name)
                    bstack11lll11111_opy_.end(EVENTS.bstack111l1llll11_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᩑ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᩒ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111l1lll1ll_opy_.name)+bstack111l_opy_ (u"ࠧࡀࠢᩓ")+str(test_framework_state.name)
                    bstack1l1l111lll_opy_ = TestFramework.bstack111ll1l1lll_opy_(instance, name)
                    bstack11lll11111_opy_.end(EVENTS.bstack111l1lll1ll_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᩔ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᩕ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᩖ").format(e))
    def bstack1l1l1llll1l_opy_(self):
        return self.bstack111l1llll1l_opy_
    def bstack1l1lll11111_opy_(self):
        return False
    def __111lll111ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᩗ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11l1ll1ll11_opy_(rep, [bstack111l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᩘ"), bstack111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᩙ"), bstack111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᩚ"), bstack111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᩛ"), bstack111l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᩜ"), bstack111l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᩝ")])
        return None
    def __111lll1lll1_opy_(self, instance: bstack1l1l11ll11l_opy_, *args):
        result = self.__111lll111ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        if result.get(bstack111l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᩞ"), None) == bstack111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ᩟") and len(args) > 1 and getattr(args[1], bstack111l_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳ᩠ࠧ"), None) is not None:
            failure = [{bstack111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᩡ"): [args[1].excinfo.exconly(), result.get(bstack111l_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᩢ"), None)]}]
            bstack1ll111l1l1l_opy_ = bstack111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᩣ") if bstack111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᩤ") in getattr(args[1].excinfo, bstack111l_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᩥ"), bstack111l_opy_ (u"ࠥࠦᩦ")) else bstack111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᩧ")
        bstack111lll1l11l_opy_ = result.get(bstack111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᩨ"), TestFramework.bstack1l1lll11l11_opy_)
        if bstack111lll1l11l_opy_ != TestFramework.bstack1l1lll11l11_opy_:
            TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1l1l1111l_opy_(instance, {
            TestFramework.bstack1l1ll1111l1_opy_: failure,
            TestFramework.bstack1l1l1lll111_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack1l1ll1lll11_opy_: bstack111lll1l11l_opy_,
        })
    def __111lll11lll_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111lll1ll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11l1ll111l1_opy_ bstack111lll1l1l1_opy_ this to be bstack111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᩩ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111llll11l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack111l_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᩪ"), None), bstack111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᩫ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᩬ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1l1l1l11l_opy_(target) if target else None
        return instance
    def __111ll1111l1_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1ll1l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l1111l1lll_opy_.bstack111ll11l111_opy_, {})
        if not key in bstack1l1ll1l11ll_opy_:
            bstack1l1ll1l11ll_opy_[key] = []
        bstack1l1l11lll11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l1111l1lll_opy_.bstack111ll1lll11_opy_, {})
        if not key in bstack1l1l11lll11_opy_:
            bstack1l1l11lll11_opy_[key] = []
        bstack1l1ll11l1l1_opy_ = {
            bstack1l1111l1lll_opy_.bstack111ll11l111_opy_: bstack1l1ll1l11ll_opy_,
            bstack1l1111l1lll_opy_.bstack111ll1lll11_opy_: bstack1l1l11lll11_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack111l_opy_ (u"ࠥ࡯ࡪࡿࠢᩭ"): key,
                TestFramework.bstack1l1ll11llll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1ll11ll1l_opy_: TestFramework.bstack1l1ll11lll1_opy_,
                TestFramework.bstack1l1l11llll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1ll11l111_opy_: [],
                TestFramework.bstack1l1ll11l1ll_opy_: args[1] if len(args) > 1 else bstack111l_opy_ (u"ࠫࠬᩮ"),
                TestFramework.bstack111lll1l111_opy_: bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()
            }
            bstack1l1ll1l11ll_opy_[key].append(hook)
            bstack1l1ll11l1l1_opy_[bstack1l1111l1lll_opy_.bstack111ll111lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack1l1l1l1llll_opy_ = bstack1l1ll1l11ll_opy_.get(key, [])
            hook = bstack1l1l1l1llll_opy_.pop() if bstack1l1l1l1llll_opy_ else None
            if hook:
                result = self.__111lll111ll_opy_(*args)
                if result:
                    bstack111ll11111l_opy_ = result.get(bstack111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᩯ"), TestFramework.bstack1l1ll11lll1_opy_)
                    if bstack111ll11111l_opy_ != TestFramework.bstack1l1ll11lll1_opy_:
                        hook[TestFramework.bstack1l1ll11ll1l_opy_] = bstack111ll11111l_opy_
                hook[TestFramework.bstack1l1ll1ll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111lll1l111_opy_]= bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()
                self.bstack111ll1lll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll1l1l1l_opy_, [])
                if logs: self.bstack11l1lll11_opy_(instance, logs)
                bstack1l1l11lll11_opy_[key].append(hook)
                bstack1l1ll11l1l1_opy_[bstack1l1111l1lll_opy_.bstack111ll1l1ll1_opy_] = key
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᩰ") + str(bstack1l1l11lll11_opy_) + bstack111l_opy_ (u"ࠢࠣᩱ"))
    def __111lll1ll11_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11l1ll1ll11_opy_(args[0], [bstack111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᩲ"), bstack111l_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᩳ"), bstack111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᩴ"), bstack111l_opy_ (u"ࠦ࡮ࡪࡳࠣ᩵"), bstack111l_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢ᩶"), bstack111l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨ᩷")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᩸")) else fixturedef.get(bstack111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᩹"), None)
        fixturename = request.fixturename if hasattr(request, bstack111l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢ᩺")) else None
        node = request.node if hasattr(request, bstack111l_opy_ (u"ࠥࡲࡴࡪࡥࠣ᩻")) else None
        target = request.node.nodeid if hasattr(node, bstack111l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᩼")) else None
        baseid = fixturedef.get(bstack111l_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧ᩽"), None) or bstack111l_opy_ (u"ࠨࠢ᩾")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111l_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱ᩿ࠧ")):
            target = bstack1l1111l1lll_opy_.__111lll111l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111l_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥ᪀")) else None
            if target and not TestFramework.bstack1l1l1l1l11l_opy_(target):
                self.__111llll11l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ᪁") + str(test_hook_state) + bstack111l_opy_ (u"ࠥࠦ᪂"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤ᪃") + str(target) + bstack111l_opy_ (u"ࠧࠨ᪄"))
            return None
        instance = TestFramework.bstack1l1l1l1l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣ᪅") + str(target) + bstack111l_opy_ (u"ࠢࠣ᪆"))
            return None
        bstack111ll11lll1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l1111l1lll_opy_.bstack111lll11111_opy_, {})
        if os.getenv(bstack111l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤ᪇"), bstack111l_opy_ (u"ࠤ࠴ࠦ᪈")) == bstack111l_opy_ (u"ࠥ࠵ࠧ᪉"):
            bstack111ll1l111l_opy_ = bstack111l_opy_ (u"ࠦ࠿ࠨ᪊").join((scope, fixturename))
            bstack111lll11l11_opy_ = datetime.now(tz=timezone.utc)
            bstack111ll1l1111_opy_ = {
                bstack111l_opy_ (u"ࠧࡱࡥࡺࠤ᪋"): bstack111ll1l111l_opy_,
                bstack111l_opy_ (u"ࠨࡴࡢࡩࡶࠦ᪌"): bstack1l1111l1lll_opy_.__111ll1ll111_opy_(request.node),
                bstack111l_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣ᪍"): fixturedef,
                bstack111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᪎"): scope,
                bstack111l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᪏"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ᪐"), None)):
                    bstack111ll1l1111_opy_[bstack111l_opy_ (u"ࠦࡹࡿࡰࡦࠤ᪑")] = TestFramework.bstack11l1lll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111ll1l1111_opy_[bstack111l_opy_ (u"ࠧࡻࡵࡪࡦࠥ᪒")] = uuid4().__str__()
                bstack111ll1l1111_opy_[bstack1l1111l1lll_opy_.bstack1l1l11llll1_opy_] = bstack111lll11l11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111ll1l1111_opy_[bstack1l1111l1lll_opy_.bstack1l1ll1ll1ll_opy_] = bstack111lll11l11_opy_
            if bstack111ll1l111l_opy_ in bstack111ll11lll1_opy_:
                bstack111ll11lll1_opy_[bstack111ll1l111l_opy_].update(bstack111ll1l1111_opy_)
                self.logger.debug(bstack111l_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢ᪓") + str(bstack111ll11lll1_opy_[bstack111ll1l111l_opy_]) + bstack111l_opy_ (u"ࠢࠣ᪔"))
            else:
                bstack111ll11lll1_opy_[bstack111ll1l111l_opy_] = bstack111ll1l1111_opy_
                self.logger.debug(bstack111l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦ᪕") + str(len(bstack111ll11lll1_opy_)) + bstack111l_opy_ (u"ࠤࠥ᪖"))
        TestFramework.bstack1l11l1ll11_opy_(instance, bstack1l1111l1lll_opy_.bstack111lll11111_opy_, bstack111ll11lll1_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ᪗") + str(instance.ref()) + bstack111l_opy_ (u"ࠦࠧ᪘"))
        return instance
    def __111llll11l1_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1l1ll1l1l_opy_.create_context(target)
        ob = bstack1l1l11ll11l_opy_(ctx, self.bstack1l1ll1ll11l_opy_, self.bstack1l1lll1l111_opy_, test_framework_state)
        TestFramework.bstack1l1l1l1111l_opy_(ob, {
            TestFramework.bstack1l1ll1l1l11_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1lll1l1_opy_: context.test_framework_version,
            TestFramework.bstack1l1l11lllll_opy_: [],
            bstack1l1111l1lll_opy_.bstack111lll11111_opy_: {},
            bstack1l1111l1lll_opy_.bstack111ll1lll11_opy_: {},
            bstack1l1111l1lll_opy_.bstack111ll11l111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l11l1ll11_opy_(ob, TestFramework.bstack111ll1l11l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l11l1ll11_opy_(ob, TestFramework.bstack1l1l1l11ll1_opy_, context.platform_index)
        TestFramework.bstack1l111l111_opy_[ctx.id] = ob
        self.logger.debug(bstack111l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧ᪙") + str(TestFramework.bstack1l111l111_opy_.keys()) + bstack111l_opy_ (u"ࠨࠢ᪚"))
        return ob
    def bstack1l1lll1111l_opy_(self, instance: bstack1l1l11ll11l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11ll1_opy_ = (
            bstack1l1111l1lll_opy_.bstack111ll111lll_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else bstack1l1111l1lll_opy_.bstack111ll1l1ll1_opy_
        )
        hook = bstack1l1111l1lll_opy_.bstack111ll1ll1l1_opy_(instance, bstack111lll11ll1_opy_)
        entries = hook.get(TestFramework.bstack1l1ll11l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, []))
        return entries
    def bstack1l1l1l11111_opy_(self, instance: bstack1l1l11ll11l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11ll1_opy_ = (
            bstack1l1111l1lll_opy_.bstack111ll111lll_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else bstack1l1111l1lll_opy_.bstack111ll1l1ll1_opy_
        )
        bstack1l1111l1lll_opy_.bstack111ll11ll11_opy_(instance, bstack111lll11ll1_opy_)
        TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, []).clear()
    def bstack111ll1lll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᪛")
        global _11ll1111l1l_opy_
        platform_index = os.environ[bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᪜")]
        bstack1l1l1l1l1ll_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), bstack111l1lll1l1_opy_)
        if not os.path.exists(bstack1l1l1l1l1ll_opy_) or not os.path.isdir(bstack1l1l1l1l1ll_opy_):
            self.logger.debug(bstack111l_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢ᪝").format(bstack1l1l1l1l1ll_opy_))
            return
        logs = hook.get(bstack111l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ᪞"), [])
        with os.scandir(bstack1l1l1l1l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1111l1l_opy_:
                    self.logger.info(bstack111l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤ᪟").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l_opy_ (u"ࠧࠨ᪠")
                    log_entry = bstack11lllllll1_opy_(
                        kind=bstack111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᪡"),
                        message=bstack111l_opy_ (u"ࠢࠣ᪢"),
                        level=bstack111l_opy_ (u"ࠣࠤ᪣"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                        bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ᪤"),
                        bstack1lllllll_opy_=os.path.abspath(entry.path),
                        bstack111ll1ll1ll_opy_=hook.get(TestFramework.bstack1l1ll11llll_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1111l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᪥")]
        bstack111llll1111_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), bstack111l1lll1l1_opy_, bstack111l1ll1ll1_opy_)
        if not os.path.exists(bstack111llll1111_opy_) or not os.path.isdir(bstack111llll1111_opy_):
            self.logger.info(bstack111l_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨ᪦").format(bstack111llll1111_opy_))
        else:
            self.logger.info(bstack111l_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᪧ").format(bstack111llll1111_opy_))
            with os.scandir(bstack111llll1111_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1111l1l_opy_:
                        self.logger.info(bstack111l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦ᪨").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l_opy_ (u"ࠢࠣ᪩")
                        log_entry = bstack11lllllll1_opy_(
                            kind=bstack111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᪪"),
                            message=bstack111l_opy_ (u"ࠤࠥ᪫"),
                            level=bstack111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ᪬"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                            bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᪭"),
                            bstack1lllllll_opy_=os.path.abspath(entry.path),
                            bstack11ll1111111_opy_=hook.get(TestFramework.bstack1l1ll11llll_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1111l1l_opy_.add(abs_path)
        hook[bstack111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥ᪮")] = logs
    def bstack11l1lll11_opy_(
        self,
        bstack1lll1l1lll_opy_: bstack1l1l11ll11l_opy_,
        entries: List[bstack11lllllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥ᪯"))
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1l11ll1_opy_)
        req.client_worker_id = bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ᪰").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1lll1l1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1lll1l1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1lll1l1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1ll1l1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1lll1l1_opy_)
            log_entry.uuid = entry.bstack111ll1ll1ll_opy_
            log_entry.test_framework_state = bstack1lll1l1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᪱"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111l_opy_ (u"ࠤࠥ᪲")
            if entry.kind == bstack111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ᪳"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack11ll11l1ll1_opy_():
            bstack1lllllll1ll_opy_ = datetime.now()
            try:
                self.bstack11l11lll11_opy_.LogCreatedEvent(req)
                bstack1lll1l1lll_opy_.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ᪴"), datetime.now() - bstack1lllllll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀ᪵ࠦ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1l1ll11l1_opy_.enqueue(bstack11ll11l1ll1_opy_)
    def __1l1l1l11l11_opy_(self, instance) -> None:
        bstack111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤ᪶ࠥࠦ")
        bstack1l1ll11l1l1_opy_ = {bstack111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤ᪷"): bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
    @staticmethod
    def bstack111ll1ll1l1_opy_(instance: bstack1l1l11ll11l_opy_, bstack111lll11ll1_opy_: str):
        bstack111ll11l1ll_opy_ = (
            bstack1l1111l1lll_opy_.bstack111ll1lll11_opy_
            if bstack111lll11ll1_opy_ == bstack1l1111l1lll_opy_.bstack111ll1l1ll1_opy_
            else bstack1l1111l1lll_opy_.bstack111ll11l111_opy_
        )
        bstack111lll11l1l_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111lll11ll1_opy_, None)
        bstack111ll1l1l11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11l1ll_opy_, None) if bstack111lll11l1l_opy_ else None
        return (
            bstack111ll1l1l11_opy_[bstack111lll11l1l_opy_][-1]
            if isinstance(bstack111ll1l1l11_opy_, dict) and len(bstack111ll1l1l11_opy_.get(bstack111lll11l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack111ll11ll11_opy_(instance: bstack1l1l11ll11l_opy_, bstack111lll11ll1_opy_: str):
        hook = bstack1l1111l1lll_opy_.bstack111ll1ll1l1_opy_(instance, bstack111lll11ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1ll11l111_opy_, []).clear()
    @staticmethod
    def __111ll1lllll_opy_(instance: bstack1l1l11ll11l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨ᪸"), None)):
            return
        if os.getenv(bstack111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨ᪹"), bstack111l_opy_ (u"ࠥ࠵᪺ࠧ")) != bstack111l_opy_ (u"ࠦ࠶ࠨ᪻"):
            bstack1l1111l1lll_opy_.logger.warning(bstack111l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢ᪼"))
            return
        bstack111lll1111l_opy_ = {
            bstack111l_opy_ (u"ࠨࡳࡦࡶࡸࡴ᪽ࠧ"): (bstack1l1111l1lll_opy_.bstack111ll111lll_opy_, bstack1l1111l1lll_opy_.bstack111ll11l111_opy_),
            bstack111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ᪾"): (bstack1l1111l1lll_opy_.bstack111ll1l1ll1_opy_, bstack1l1111l1lll_opy_.bstack111ll1lll11_opy_),
        }
        for when in (bstack111l_opy_ (u"ࠣࡵࡨࡸࡺࡶᪿࠢ"), bstack111l_opy_ (u"ࠤࡦࡥࡱࡲᫀࠢ"), bstack111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ᫁")):
            bstack111l1lllll1_opy_ = args[1].get_records(when)
            if not bstack111l1lllll1_opy_:
                continue
            records = [
                bstack11lllllll1_opy_(
                    kind=TestFramework.bstack11l1lllll11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢ᫂")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨ᫃")) and r.created
                        else None
                    ),
                )
                for r in bstack111l1lllll1_opy_
                if isinstance(getattr(r, bstack111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫᫄ࠢ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111ll11l11l_opy_, bstack111ll11l1ll_opy_ = bstack111lll1111l_opy_.get(when, (None, None))
            bstack111lll1llll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11l11l_opy_, None) if bstack111ll11l11l_opy_ else None
            bstack111ll1l1l11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11l1ll_opy_, None) if bstack111lll1llll_opy_ else None
            if isinstance(bstack111ll1l1l11_opy_, dict) and len(bstack111ll1l1l11_opy_.get(bstack111lll1llll_opy_, [])) > 0:
                hook = bstack111ll1l1l11_opy_[bstack111lll1llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1ll11l111_opy_ in hook:
                    hook[TestFramework.bstack1l1ll11l111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111ll111l11_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1111l1lll_opy_.__111lll111l1_opy_(test.location) if hasattr(test, bstack111l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤ᫅")) else getattr(test, bstack111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᫆"), None)
        test_name = test.name if hasattr(test, bstack111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫇")) else None
        bstack111ll11llll_opy_ = test.fspath.strpath if hasattr(test, bstack111l_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥ᫈")) and test.fspath else None
        if not test_id or not test_name or not bstack111ll11llll_opy_:
            return None
        code = None
        if hasattr(test, bstack111l_opy_ (u"ࠦࡴࡨࡪࠣ᫉")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack111l1ll1lll_opy_ = []
        try:
            bstack111l1ll1lll_opy_ = bstack111l1l1l11_opy_.bstack1lll1ll1l11_opy_(test)
        except:
            bstack1l1111l1lll_opy_.logger.warning(bstack111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨ᫊"))
        return {
            TestFramework.bstack1l1l1lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1ll111l1l_opy_: test_id,
            TestFramework.bstack1l1ll1lll1l_opy_: test_name,
            TestFramework.bstack1l1ll11ll11_opy_: getattr(test, bstack111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨ᫋"), None),
            TestFramework.bstack1l1ll111lll_opy_: bstack111ll11llll_opy_,
            TestFramework.bstack1l1ll1ll1l1_opy_: bstack1l1111l1lll_opy_.__111ll1ll111_opy_(test),
            TestFramework.bstack1l1ll111l11_opy_: code,
            TestFramework.bstack1l1ll1lll11_opy_: TestFramework.bstack1l1lll11l11_opy_,
            TestFramework.bstack1l1l1lll1ll_opy_: test_id,
            TestFramework.bstack1l1l1l1ll1l_opy_: bstack111l1ll1lll_opy_
        }
    @staticmethod
    def __111ll1ll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack111l_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᫌ"), [])
            markers.extend([getattr(m, bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᫍ"), None) for m in own_markers if getattr(m, bstack111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᫎ"), None)])
            current = getattr(current, bstack111l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥ᫏"), None)
        return markers
    @staticmethod
    def __111lll111l1_opy_(location):
        return bstack111l_opy_ (u"ࠦ࠿ࡀࠢ᫐").join(filter(lambda x: isinstance(x, str), location))