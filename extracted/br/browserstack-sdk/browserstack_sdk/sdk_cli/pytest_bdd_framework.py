# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll1l1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l11ll11_opy_ import bstack11ll11l1ll1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111l1l1l_opy_,
    TestHookState,
    bstack1lll1l11l1l_opy_,
    bstack1ll11ll1l1l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l111l11lll_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll1111ll11_opy_ import bstack1l1ll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1ll1lllll1l_opy_
bstack1l11l1lllll_opy_ = bstack1l111l11lll_opy_()
bstack1l111l1l111_opy_ = bstack1lll1l_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢ᚝")
bstack11ll111l11l_opy_ = bstack1lll1l_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦ᚞")
bstack11l1lll1ll1_opy_ = bstack1lll1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ᚟")
bstack11ll1111111_opy_ = 1.0
_1l111ll1l1l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11ll1l1ll11_opy_ = bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᚠ")
    bstack11l1ll1lll1_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᚡ")
    bstack11ll11lll1l_opy_ = bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᚢ")
    bstack11l1lll1lll_opy_ = bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᚣ")
    bstack11ll11111l1_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᚤ")
    bstack11l1lll1l1l_opy_: bool
    bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_  = None
    bstack11l1lll11l1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1llll1ll_opy_: Dict[str, str],
        bstack1l1l1ll1l1l_opy_: List[str]=[bstack1lll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᚥ")],
        bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_ = None,
        bstack1lll111lll1_opy_=None
    ):
        super().__init__(bstack1l1l1ll1l1l_opy_, bstack11l1llll1ll_opy_, bstack1lll111111l_opy_)
        self.bstack11l1lll1l1l_opy_ = any(bstack1lll1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᚦ") in item.lower() for item in bstack1l1l1ll1l1l_opy_)
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
    def track_event(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l1lll11l1_opy_:
            bstack11ll11l1ll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᚧ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠦࠧᚨ"))
            return
        if not self.bstack11l1lll1l1l_opy_:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᚩ") + str(str(self.bstack1l1l1ll1l1l_opy_)) + bstack1lll1l_opy_ (u"ࠨࠢᚪ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᚫ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠣࠤᚬ"))
            return
        instance = self.__11ll11ll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᚭ") + str(args) + bstack1lll1l_opy_ (u"ࠥࠦᚮ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1lll11l1_opy_ and test_hook_state == TestHookState.PRE:
                bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11lll1l1l1_opy_.value)
                name = str(EVENTS.bstack11lll1l1l1_opy_.name)+bstack1lll1l_opy_ (u"ࠦ࠿ࠨᚯ")+str(test_framework_state.name)
                TestFramework.bstack11ll1l11l1l_opy_(instance, name, bstack1ll111111l_opy_)
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᚰ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack11lllll1111_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll1ll1111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᚱ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠢࠣᚲ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l111l11l1l_opy_):
                    TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l111l11l1l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1ll1ll1l_opy_(instance, args)
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᚳ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠤࠥᚴ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_):
                    TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᚵ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠦࠧᚶ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11ll1ll111l_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1lll111l_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11ll111llll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll1111l11_opy_(instance, *args)
                self.__11ll1l1111l_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1lll11l1_opy_:
                self.__11ll11llll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᚷ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠨࠢᚸ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1lll11l1_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack11lll1l1l1_opy_.name)+bstack1lll1l_opy_ (u"ࠢ࠻ࠤᚹ")+str(test_framework_state.name)
                bstack1ll111111l_opy_ = TestFramework.bstack11ll111111l_opy_(instance, name)
                bstack1l11l11ll1_opy_.end(EVENTS.bstack11lll1l1l1_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᚺ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᚻ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᚼ").format(e))
    def bstack1l11l111lll_opy_(self):
        return self.bstack11l1lll1l1l_opy_
    def bstack1l11l1l11l1_opy_(self):
        return False
    def __11ll1l1ll1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1lll1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᚽ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111l1l1l1_opy_(rep, [bstack1lll1l_opy_ (u"ࠧࡽࡨࡦࡰࠥᚾ"), bstack1lll1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᚿ"), bstack1lll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᛀ"), bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᛁ"), bstack1lll1l_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᛂ"), bstack1lll1l_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᛃ")])
        return None
    def __11ll1111l11_opy_(self, instance: bstack1ll111l1l1l_opy_, *args):
        result = self.__11ll1l1ll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll111l_opy_ = None
        if result.get(bstack1lll1l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᛄ"), None) == bstack1lll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᛅ") and len(args) > 1 and getattr(args[1], bstack1lll1l_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᛆ"), None) is not None:
            failure = [{bstack1lll1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᛇ"): [args[1].excinfo.exconly(), result.get(bstack1lll1l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᛈ"), None)]}]
            bstack1lll1ll111l_opy_ = bstack1lll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᛉ") if bstack1lll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᛊ") in getattr(args[1].excinfo, bstack1lll1l_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᛋ"), bstack1lll1l_opy_ (u"ࠧࠨᛌ")) else bstack1lll1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᛍ")
        bstack11ll1l1l111_opy_ = result.get(bstack1lll1l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᛎ"), TestFramework.bstack11l1ll1llll_opy_)
        if bstack11ll1l1l111_opy_ != TestFramework.bstack11l1ll1llll_opy_:
            TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1l111ll_opy_(instance, {
            TestFramework.bstack11llllll1l1_opy_: failure,
            TestFramework.bstack11ll111ll11_opy_: bstack1lll1ll111l_opy_,
            TestFramework.bstack1l1111111l1_opy_: bstack11ll1l1l111_opy_,
        })
    def __11ll11ll1l1_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11ll1l11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll1ll1_opy_ bstack11l1lllll11_opy_ this to be bstack1lll1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᛏ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll11111ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1lll1l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᛐ"), None), bstack1lll1l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᛑ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1lll1l_opy_ (u"ࠦࡳࡵࡤࡦࠤᛒ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1lll1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᛓ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1l1l111l_opy_(target) if target else None
        return instance
    def __11ll11llll1_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1l11_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, PytestBDDFramework.bstack11l1ll1lll1_opy_, {})
        if not key in bstack11l1lll1l11_opy_:
            bstack11l1lll1l11_opy_[key] = []
        bstack11l1llllll1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, PytestBDDFramework.bstack11ll11lll1l_opy_, {})
        if not key in bstack11l1llllll1_opy_:
            bstack11l1llllll1_opy_[key] = []
        bstack11ll11ll111_opy_ = {
            PytestBDDFramework.bstack11l1ll1lll1_opy_: bstack11l1lll1l11_opy_,
            PytestBDDFramework.bstack11ll11lll1l_opy_: bstack11l1llllll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1lll1l_opy_ (u"ࠨ࡫ࡦࡻࠥᛔ"): key,
                TestFramework.bstack11ll1111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11l1llll11l_opy_: TestFramework.bstack11ll11ll1ll_opy_,
                TestFramework.bstack11ll1l1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1l111l1_opy_: [],
                TestFramework.bstack11ll1111l1l_opy_: hook_name,
                TestFramework.bstack11ll11l11ll_opy_: bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()
            }
            bstack11l1lll1l11_opy_[key].append(hook)
            bstack11ll11ll111_opy_[PytestBDDFramework.bstack11l1lll1lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11ll11l1111_opy_ = bstack11l1lll1l11_opy_.get(key, [])
            hook = bstack11ll11l1111_opy_.pop() if bstack11ll11l1111_opy_ else None
            if hook:
                result = self.__11ll1l1ll1l_opy_(*args)
                if result:
                    bstack11l1ll1l1ll_opy_ = result.get(bstack1lll1l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᛕ"), TestFramework.bstack11ll11ll1ll_opy_)
                    if bstack11l1ll1l1ll_opy_ != TestFramework.bstack11ll11ll1ll_opy_:
                        hook[TestFramework.bstack11l1llll11l_opy_] = bstack11l1ll1l1ll_opy_
                hook[TestFramework.bstack11l1llll1l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll11l11ll_opy_] = bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()
                self.bstack11l1lll11ll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll11ll1_opy_, [])
                self.bstack1l111l1lll1_opy_(instance, logs)
                bstack11l1llllll1_opy_[key].append(hook)
                bstack11ll11ll111_opy_[PytestBDDFramework.bstack11ll11111l1_opy_] = key
        TestFramework.bstack11ll1l111ll_opy_(instance, bstack11ll11ll111_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᛖ") + str(bstack11l1llllll1_opy_) + bstack1lll1l_opy_ (u"ࠤࠥᛗ"))
    def __11ll1l11lll_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111l1l1l1_opy_(args[0], [bstack1lll1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᛘ"), bstack1lll1l_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᛙ"), bstack1lll1l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᛚ"), bstack1lll1l_opy_ (u"ࠨࡩࡥࡵࠥᛛ"), bstack1lll1l_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᛜ"), bstack1lll1l_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᛝ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1lll1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᛞ")) else fixturedef.get(bstack1lll1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᛟ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1lll1l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᛠ")) else None
        node = request.node if hasattr(request, bstack1lll1l_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᛡ")) else None
        target = request.node.nodeid if hasattr(node, bstack1lll1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᛢ")) else None
        baseid = fixturedef.get(bstack1lll1l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᛣ"), None) or bstack1lll1l_opy_ (u"ࠣࠤᛤ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1lll1l_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᛥ")):
            target = PytestBDDFramework.__11ll111ll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1lll1l_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᛦ")) else None
            if target and not TestFramework.bstack1ll1l1l111l_opy_(target):
                self.__11ll11111ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᛧ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠧࠨᛨ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᛩ") + str(target) + bstack1lll1l_opy_ (u"ࠢࠣᛪ"))
            return None
        instance = TestFramework.bstack1ll1l1l111l_opy_(target)
        if not instance:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥ᛫") + str(target) + bstack1lll1l_opy_ (u"ࠤࠥ᛬"))
            return None
        bstack11l1ll1l111_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, PytestBDDFramework.bstack11ll1l1ll11_opy_, {})
        if os.getenv(bstack1lll1l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦ᛭"), bstack1lll1l_opy_ (u"ࠦ࠶ࠨᛮ")) == bstack1lll1l_opy_ (u"ࠧ࠷ࠢᛯ"):
            bstack11ll1l1lll1_opy_ = bstack1lll1l_opy_ (u"ࠨ࠺ࠣᛰ").join((scope, fixturename))
            bstack11ll11l11l1_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll1l11l11_opy_ = {
                bstack1lll1l_opy_ (u"ࠢ࡬ࡧࡼࠦᛱ"): bstack11ll1l1lll1_opy_,
                bstack1lll1l_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᛲ"): PytestBDDFramework.__11ll111l1ll_opy_(request.node, scenario),
                bstack1lll1l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᛳ"): fixturedef,
                bstack1lll1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᛴ"): scope,
                bstack1lll1l_opy_ (u"ࠦࡹࡿࡰࡦࠤᛵ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1lll1l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᛶ"), None)):
                    bstack11ll1l11l11_opy_[bstack1lll1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᛷ")] = TestFramework.bstack1l11l11l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11ll1l11l11_opy_[bstack1lll1l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᛸ")] = uuid4().__str__()
                bstack11ll1l11l11_opy_[PytestBDDFramework.bstack11ll1l1l1ll_opy_] = bstack11ll11l11l1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11ll1l11l11_opy_[PytestBDDFramework.bstack11l1llll1l1_opy_] = bstack11ll11l11l1_opy_
            if bstack11ll1l1lll1_opy_ in bstack11l1ll1l111_opy_:
                bstack11l1ll1l111_opy_[bstack11ll1l1lll1_opy_].update(bstack11ll1l11l11_opy_)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤ᛹") + str(bstack11l1ll1l111_opy_[bstack11ll1l1lll1_opy_]) + bstack1lll1l_opy_ (u"ࠤࠥ᛺"))
            else:
                bstack11l1ll1l111_opy_[bstack11ll1l1lll1_opy_] = bstack11ll1l11l11_opy_
                self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨ᛻") + str(len(bstack11l1ll1l111_opy_)) + bstack1lll1l_opy_ (u"ࠦࠧ᛼"))
        TestFramework.bstack1lll1l11lll_opy_(instance, PytestBDDFramework.bstack11ll1l1ll11_opy_, bstack11l1ll1l111_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ᛽") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠨࠢ᛾"))
        return instance
    def __11ll11111ll_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1ll1l1ll_opy_.create_context(target)
        ob = bstack1ll111l1l1l_opy_(ctx, self.bstack1l1l1ll1l1l_opy_, self.bstack11l1llll1ll_opy_, test_framework_state)
        TestFramework.bstack11ll1l111ll_opy_(ob, {
            TestFramework.bstack1l1l111ll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l11l11l1ll_opy_: context.test_framework_version,
            TestFramework.bstack11l1ll11l1l_opy_: [],
            PytestBDDFramework.bstack11ll1l1ll11_opy_: {},
            PytestBDDFramework.bstack11ll11lll1l_opy_: {},
            PytestBDDFramework.bstack11l1ll1lll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1l11lll_opy_(ob, TestFramework.bstack11ll11lll11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l11lll_opy_(ob, TestFramework.bstack1l1l1lll111_opy_, context.platform_index)
        TestFramework.bstack1lll1l1111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢ᛿") + str(TestFramework.bstack1lll1l1111l_opy_.keys()) + bstack1lll1l_opy_ (u"ࠣࠤᜀ"))
        return ob
    @staticmethod
    def __11l1ll1ll1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬᜁ"): id(step),
                bstack1lll1l_opy_ (u"ࠪࡸࡪࡾࡴࠨᜂ"): step.name,
                bstack1lll1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᜃ"): step.keyword,
            })
        meta = {
            bstack1lll1l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᜄ"): {
                bstack1lll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᜅ"): feature.name,
                bstack1lll1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᜆ"): feature.filename,
                bstack1lll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᜇ"): feature.description
            },
            bstack1lll1l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᜈ"): {
                bstack1lll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᜉ"): scenario.name
            },
            bstack1lll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᜊ"): steps,
            bstack1lll1l_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᜋ"): PytestBDDFramework.__11ll1l1l11l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11ll11lllll_opy_: meta
            }
        )
    def bstack11l1lll11ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1lll1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᜌ")
        global _1l111ll1l1l_opy_
        platform_index = os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᜍ")]
        bstack1l11l1111l1_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), bstack11ll111l11l_opy_)
        if not os.path.exists(bstack1l11l1111l1_opy_) or not os.path.isdir(bstack1l11l1111l1_opy_):
            return
        logs = hook.get(bstack1lll1l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᜎ"), [])
        with os.scandir(bstack1l11l1111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111ll1l1l_opy_:
                    self.logger.info(bstack1lll1l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᜏ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1lll1l_opy_ (u"ࠥࠦᜐ")
                    log_entry = bstack1ll11ll1l1l_opy_(
                        kind=bstack1lll1l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᜑ"),
                        message=bstack1lll1l_opy_ (u"ࠧࠨᜒ"),
                        level=bstack1lll1l_opy_ (u"ࠨࠢᜓ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11l11llll_opy_=entry.stat().st_size,
                        bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊ᜔ࠢ"),
                        bstack1ll11ll_opy_=os.path.abspath(entry.path),
                        bstack11ll11l111l_opy_=hook.get(TestFramework.bstack11ll1111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l111ll1l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᜕")]
        bstack11l1ll1ll11_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), bstack11ll111l11l_opy_, bstack11l1lll1ll1_opy_)
        if not os.path.exists(bstack11l1ll1ll11_opy_) or not os.path.isdir(bstack11l1ll1ll11_opy_):
            self.logger.info(bstack1lll1l_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦ᜖").format(bstack11l1ll1ll11_opy_))
        else:
            self.logger.info(bstack1lll1l_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤ᜗").format(bstack11l1ll1ll11_opy_))
            with os.scandir(bstack11l1ll1ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111ll1l1l_opy_:
                        self.logger.info(bstack1lll1l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤ᜘").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1lll1l_opy_ (u"ࠧࠨ᜙")
                        log_entry = bstack1ll11ll1l1l_opy_(
                            kind=bstack1lll1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᜚"),
                            message=bstack1lll1l_opy_ (u"ࠢࠣ᜛"),
                            level=bstack1lll1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᜜"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11l11llll_opy_=entry.stat().st_size,
                            bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ᜝"),
                            bstack1ll11ll_opy_=os.path.abspath(entry.path),
                            bstack1l111llll1l_opy_=hook.get(TestFramework.bstack11ll1111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l111ll1l1l_opy_.add(abs_path)
        hook[bstack1lll1l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ᜞")] = logs
    def bstack1l111l1lll1_opy_(
        self,
        bstack1l111ll1lll_opy_: bstack1ll111l1l1l_opy_,
        entries: List[bstack1ll11ll1l1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1lll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᜟ"))
        req.platform_index = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l1lll111_opy_)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᜠ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l111ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l11l11l1ll_opy_)
            log_entry.uuid = entry.bstack11ll11l111l_opy_ if entry.bstack11ll11l111l_opy_ else TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l1l1ll1l_opy_)
            log_entry.test_framework_state = bstack1l111ll1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1lll1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᜡ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1lll1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᜢ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11llll_opy_
                log_entry.file_path = entry.bstack1ll11ll_opy_
        def bstack1l11ll11ll1_opy_():
            bstack1l1l11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.LogCreatedEvent(req)
                bstack1l111ll1lll_opy_.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᜣ"), datetime.now() - bstack1l1l11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1lll1l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᜤ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll111111l_opy_.enqueue(bstack1l11ll11ll1_opy_)
    def __11ll1l1111l_opy_(self, instance) -> None:
        bstack1lll1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᜥ")
        bstack11ll11ll111_opy_ = {bstack1lll1l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᜦ"): bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()}
        TestFramework.bstack11ll1l111ll_opy_(instance, bstack11ll11ll111_opy_)
    @staticmethod
    def __11ll1ll111l_opy_(instance, args):
        request, bstack11l1ll11lll_opy_ = args
        bstack11ll1l1llll_opy_ = id(bstack11l1ll11lll_opy_)
        bstack11ll11ll11l_opy_ = instance.data[TestFramework.bstack11ll11lllll_opy_]
        step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"ࠬ࡯ࡤࠨᜧ")] == bstack11ll1l1llll_opy_, bstack11ll11ll11l_opy_[bstack1lll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᜨ")]), None)
        step.update({
            bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᜩ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11ll11ll11l_opy_[bstack1lll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᜪ")]) if st[bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬᜫ")] == step[bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭ᜬ")]), None)
        if index is not None:
            bstack11ll11ll11l_opy_[bstack1lll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᜭ")][index] = step
        instance.data[TestFramework.bstack11ll11lllll_opy_] = bstack11ll11ll11l_opy_
    @staticmethod
    def __11l1lll111l_opy_(instance, args):
        bstack1lll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᜮ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11l1ll11lll_opy_ = args[1]
        bstack11ll1l1llll_opy_ = id(bstack11l1ll11lll_opy_)
        bstack11ll11ll11l_opy_ = instance.data[TestFramework.bstack11ll11lllll_opy_]
        step = None
        if bstack11ll1l1llll_opy_ is not None and bstack11ll11ll11l_opy_.get(bstack1lll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᜯ")):
            step = next(filter(lambda st: st[bstack1lll1l_opy_ (u"ࠧࡪࡦࠪᜰ")] == bstack11ll1l1llll_opy_, bstack11ll11ll11l_opy_[bstack1lll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᜱ")]), None)
            step.update({
                bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᜲ"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1lll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜳ"): bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ᜴ࠫ"),
                bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭᜵"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1lll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᜶"): bstack1lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᜷"),
                })
        index = next((i for i, st in enumerate(bstack11ll11ll11l_opy_[bstack1lll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᜸")]) if st[bstack1lll1l_opy_ (u"ࠩ࡬ࡨࠬ᜹")] == step[bstack1lll1l_opy_ (u"ࠪ࡭ࡩ࠭᜺")]), None)
        if index is not None:
            bstack11ll11ll11l_opy_[bstack1lll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᜻")][index] = step
        instance.data[TestFramework.bstack11ll11lllll_opy_] = bstack11ll11ll11l_opy_
    @staticmethod
    def __11ll1l1l11l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1lll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ᜼")):
                examples = list(node.callspec.params[bstack1lll1l_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬ᜽")].values())
            return examples
        except:
            return []
    def bstack1l11ll1l11l_opy_(self, instance: bstack1ll111l1l1l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111ll1_opy_ = (
            PytestBDDFramework.bstack11l1lll1lll_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11ll11111l1_opy_
        )
        hook = PytestBDDFramework.bstack11l1ll1l1l1_opy_(instance, bstack11ll1111ll1_opy_)
        entries = hook.get(TestFramework.bstack11ll1l111l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, []))
        return entries
    def bstack1l11l1lll11_opy_(self, instance: bstack1ll111l1l1l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111ll1_opy_ = (
            PytestBDDFramework.bstack11l1lll1lll_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11ll11111l1_opy_
        )
        PytestBDDFramework.bstack11ll11l1l1l_opy_(instance, bstack11ll1111ll1_opy_)
        TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, []).clear()
    @staticmethod
    def bstack11l1ll1l1l1_opy_(instance: bstack1ll111l1l1l_opy_, bstack11ll1111ll1_opy_: str):
        bstack11l1ll11l11_opy_ = (
            PytestBDDFramework.bstack11ll11lll1l_opy_
            if bstack11ll1111ll1_opy_ == PytestBDDFramework.bstack11ll11111l1_opy_
            else PytestBDDFramework.bstack11l1ll1lll1_opy_
        )
        bstack11ll111l1l1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11ll1111ll1_opy_, None)
        bstack11ll11l1lll_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11l1ll11l11_opy_, None) if bstack11ll111l1l1_opy_ else None
        return (
            bstack11ll11l1lll_opy_[bstack11ll111l1l1_opy_][-1]
            if isinstance(bstack11ll11l1lll_opy_, dict) and len(bstack11ll11l1lll_opy_.get(bstack11ll111l1l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll11l1l1l_opy_(instance: bstack1ll111l1l1l_opy_, bstack11ll1111ll1_opy_: str):
        hook = PytestBDDFramework.bstack11l1ll1l1l1_opy_(instance, bstack11ll1111ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1l111l1_opy_, []).clear()
    @staticmethod
    def __11ll111llll_opy_(instance: bstack1ll111l1l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1lll1l_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧ᜾"), None)):
            return
        if os.getenv(bstack1lll1l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧ᜿"), bstack1lll1l_opy_ (u"ࠤ࠴ࠦᝀ")) != bstack1lll1l_opy_ (u"ࠥ࠵ࠧᝁ"):
            PytestBDDFramework.logger.warning(bstack1lll1l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᝂ"))
            return
        bstack11l1lll1111_opy_ = {
            bstack1lll1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᝃ"): (PytestBDDFramework.bstack11l1lll1lll_opy_, PytestBDDFramework.bstack11l1ll1lll1_opy_),
            bstack1lll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᝄ"): (PytestBDDFramework.bstack11ll11111l1_opy_, PytestBDDFramework.bstack11ll11lll1l_opy_),
        }
        for when in (bstack1lll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᝅ"), bstack1lll1l_opy_ (u"ࠣࡥࡤࡰࡱࠨᝆ"), bstack1lll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᝇ")):
            bstack11l1lllllll_opy_ = args[1].get_records(when)
            if not bstack11l1lllllll_opy_:
                continue
            records = [
                bstack1ll11ll1l1l_opy_(
                    kind=TestFramework.bstack1l111l1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1lll1l_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᝈ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1lll1l_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᝉ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1lllllll_opy_
                if isinstance(getattr(r, bstack1lll1l_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᝊ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll111l111_opy_, bstack11l1ll11l11_opy_ = bstack11l1lll1111_opy_.get(when, (None, None))
            bstack11ll1l1l1l1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11ll111l111_opy_, None) if bstack11ll111l111_opy_ else None
            bstack11ll11l1lll_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11l1ll11l11_opy_, None) if bstack11ll1l1l1l1_opy_ else None
            if isinstance(bstack11ll11l1lll_opy_, dict) and len(bstack11ll11l1lll_opy_.get(bstack11ll1l1l1l1_opy_, [])) > 0:
                hook = bstack11ll11l1lll_opy_[bstack11ll1l1l1l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1l111l1_opy_ in hook:
                    hook[TestFramework.bstack11ll1l111l1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1ll1111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11ll11l1l11_opy_(request.node, scenario)
        bstack11l1llll111_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l1llll111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l1l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11lllll1111_opy_: test_id,
            TestFramework.bstack1l1l111llll_opy_: test_name,
            TestFramework.bstack1l1111ll1l1_opy_: test_id,
            TestFramework.bstack11ll111lll1_opy_: bstack11l1llll111_opy_,
            TestFramework.bstack11l1lllll1l_opy_: PytestBDDFramework.__11ll111l1ll_opy_(feature, scenario),
            TestFramework.bstack11ll1l11ll1_opy_: code,
            TestFramework.bstack1l1111111l1_opy_: TestFramework.bstack11l1ll1llll_opy_,
            TestFramework.bstack11lll1111l1_opy_: test_name
        }
    @staticmethod
    def __11ll11l1l11_opy_(node, scenario):
        if hasattr(node, bstack1lll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᝋ")):
            parts = node.nodeid.rsplit(bstack1lll1l_opy_ (u"ࠢ࡜ࠤᝌ"))
            params = parts[-1]
            return bstack1lll1l_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᝍ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll111l1ll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1lll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᝎ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1lll1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᝏ")) else [])
    @staticmethod
    def __11ll111ll1l_opy_(location):
        return bstack1lll1l_opy_ (u"ࠦ࠿ࡀࠢᝐ").join(filter(lambda x: isinstance(x, str), location))