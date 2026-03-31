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
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1l111l1_opy_,
    TestHookState,
    bstack1ll1l11llll_opy_,
    bstack1l1l1l1lll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l11111l11l_opy_
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1l1llllll_opy_ import bstack1l1ll1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11llll11_opy_ import bstack1ll11llllll_opy_
bstack11llll1l1ll_opy_ = bstack1l11111l11l_opy_()
bstack11lllll1l1l_opy_ = bstack1ll11_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦឲ")
bstack11l1ll1lll1_opy_ = bstack1ll11_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣឳ")
bstack11l1l1l1l11_opy_ = bstack1ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ឴")
bstack11l11l1lll1_opy_ = 1.0
_1l1111111l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l11ll111l_opy_ = bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ឵")
    bstack11l1lll11l1_opy_ = bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨា")
    bstack11l1l1ll111_opy_ = bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣិ")
    bstack11l1l1ll1ll_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧី")
    bstack11l11lll11l_opy_ = bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢឹ")
    bstack11l1l111111_opy_: bool
    bstack1ll11llll11_opy_: bstack1ll11llllll_opy_  = None
    bstack11l1l1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l11l1l1ll_opy_: Dict[str, str],
        bstack1l1l111lll1_opy_: List[str]=[bstack1ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤឺ")],
        bstack1ll11llll11_opy_: bstack1ll11llllll_opy_ = None,
        bstack1l1ll1ll111_opy_=None
    ):
        super().__init__(bstack1l1l111lll1_opy_, bstack11l11l1l1ll_opy_, bstack1ll11llll11_opy_)
        self.bstack11l1l111111_opy_ = any(bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥុ") in item.lower() for item in bstack1l1l111lll1_opy_)
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
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l1l1l1l1l_opy_:
            bstack11l1ll1l11l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣូ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠣࠤួ"))
            return
        if not self.bstack11l1l111111_opy_:
            self.logger.warning(bstack1ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥើ") + str(str(self.bstack1l1l111lll1_opy_)) + bstack1ll11_opy_ (u"ࠥࠦឿ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨៀ") + str(kwargs) + bstack1ll11_opy_ (u"ࠧࠨេ"))
            return
        instance = self.__11l11ll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧែ") + str(args) + bstack1ll11_opy_ (u"ࠢࠣៃ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1l1l1l1l_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11l1l1l1_opy_.value)
                name = str(EVENTS.bstack11l1l1l1_opy_.name)+bstack1ll11_opy_ (u"ࠣ࠼ࠥោ")+str(test_framework_state.name)
                TestFramework.bstack11l1l1lll1l_opy_(instance, name, bstack1l11ll1ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨៅ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack11lll111111_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11l1l11l111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll11_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥំ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠦࠧះ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l111ll1111_opy_):
                    TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack1l111ll1111_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1ll1l111_opy_(instance, args)
                    self.logger.debug(bstack1ll11_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥៈ") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠨࠢ៉"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack11lllll1lll_opy_):
                    TestFramework.bstack1l11lllll_opy_(instance, TestFramework.bstack11lllll1lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ៊") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠣࠤ់"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l1l1l11ll_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1l1lll11_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1ll11ll1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l111l11_opy_(instance, *args)
                self.__11l1ll1l1l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1l1l1l1l_opy_:
                self.__11l11l1l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ៌") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠥࠦ៍"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l11llll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1l1l1l1l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack11l1l1l1_opy_.name)+bstack1ll11_opy_ (u"ࠦ࠿ࠨ៎")+str(test_framework_state.name)
                bstack1l11ll1ll1_opy_ = TestFramework.bstack11l1l1ll11l_opy_(instance, name)
                bstack11ll11l1ll_opy_.end(EVENTS.bstack11l1l1l1_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ៏"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ័"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ៑").format(e))
    def bstack1l111l1l11l_opy_(self):
        return self.bstack11l1l111111_opy_
    def bstack11lllllll1l_opy_(self):
        return False
    def __11l1ll11111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸ្ࠧ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111l11l1l_opy_(rep, [bstack1ll11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ៓"), bstack1ll11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ។"), bstack1ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ៕"), bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ៖"), bstack1ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢៗ"), bstack1ll11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ៘")])
        return None
    def __11l1l111l11_opy_(self, instance: bstack1l1l1l111l1_opy_, *args):
        result = self.__11l1ll11111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lll111l_opy_ = None
        if result.get(bstack1ll11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ៙"), None) == bstack1ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ៚") and len(args) > 1 and getattr(args[1], bstack1ll11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦ៛"), None) is not None:
            failure = [{bstack1ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧៜ"): [args[1].excinfo.exconly(), result.get(bstack1ll11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦ៝"), None)]}]
            bstack1ll1lll111l_opy_ = bstack1ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ៞") if bstack1ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ៟") in getattr(args[1].excinfo, bstack1ll11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥ០"), bstack1ll11_opy_ (u"ࠤࠥ១")) else bstack1ll11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ២")
        bstack11l1lll11ll_opy_ = result.get(bstack1ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ៣"), TestFramework.bstack11l1lll1l1l_opy_)
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
            target = None # bstack1l111ll11l1_opy_ bstack11l1l1111l1_opy_ this to be bstack1ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ៤")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l11llllll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ៥"), None), bstack1ll11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ៦"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll11_opy_ (u"ࠣࡰࡲࡨࡪࠨ៧"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ៨"), None):
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
        bstack11l11lllll1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, PytestBDDFramework.bstack11l1lll11l1_opy_, {})
        if not key in bstack11l11lllll1_opy_:
            bstack11l11lllll1_opy_[key] = []
        bstack11l1l11llll_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, PytestBDDFramework.bstack11l1l1ll111_opy_, {})
        if not key in bstack11l1l11llll_opy_:
            bstack11l1l11llll_opy_[key] = []
        bstack11l11l1l111_opy_ = {
            PytestBDDFramework.bstack11l1lll11l1_opy_: bstack11l11lllll1_opy_,
            PytestBDDFramework.bstack11l1l1ll111_opy_: bstack11l1l11llll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll11_opy_ (u"ࠥ࡯ࡪࡿࠢ៩"): key,
                TestFramework.bstack11l1l11ll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1l11lll1_opy_: TestFramework.bstack11l11l1l1l1_opy_,
                TestFramework.bstack11l11l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1l111ll1_opy_: [],
                TestFramework.bstack11l1ll1111l_opy_: hook_name,
                TestFramework.bstack11l1l1l1lll_opy_: bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()
            }
            bstack11l11lllll1_opy_[key].append(hook)
            bstack11l11l1l111_opy_[PytestBDDFramework.bstack11l1l1ll1ll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll11l1l_opy_ = bstack11l11lllll1_opy_.get(key, [])
            hook = bstack11l1ll11l1l_opy_.pop() if bstack11l1ll11l1l_opy_ else None
            if hook:
                result = self.__11l1ll11111_opy_(*args)
                if result:
                    bstack11l1ll11lll_opy_ = result.get(bstack1ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ៪"), TestFramework.bstack11l11l1l1l1_opy_)
                    if bstack11l1ll11lll_opy_ != TestFramework.bstack11l11l1l1l1_opy_:
                        hook[TestFramework.bstack11l1l11lll1_opy_] = bstack11l1ll11lll_opy_
                hook[TestFramework.bstack11l1ll111l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1lll_opy_] = bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll111ll_opy_, [])
                self.bstack11llllll1ll_opy_(instance, logs)
                bstack11l1l11llll_opy_[key].append(hook)
                bstack11l11l1l111_opy_[PytestBDDFramework.bstack11l11lll11l_opy_] = key
        TestFramework.bstack11l1l1l1111_opy_(instance, bstack11l11l1l111_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦ៫") + str(bstack11l1l11llll_opy_) + bstack1ll11_opy_ (u"ࠨࠢ៬"))
    def __11l1l111lll_opy_(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111l11l1l_opy_(args[0], [bstack1ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ៭"), bstack1ll11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤ៮"), bstack1ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤ៯"), bstack1ll11_opy_ (u"ࠥ࡭ࡩࡹࠢ៰"), bstack1ll11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨ៱"), bstack1ll11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧ៲")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ៳")) else fixturedef.get(bstack1ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ៴"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨ៵")) else None
        node = request.node if hasattr(request, bstack1ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ៶")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ៷")) else None
        baseid = fixturedef.get(bstack1ll11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦ៸"), None) or bstack1ll11_opy_ (u"ࠧࠨ៹")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦ៺")):
            target = PytestBDDFramework.__11l1l1l111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤ៻")) else None
            if target and not TestFramework.bstack1ll111l1lll_opy_(target):
                self.__11l11llllll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ៼") + str(test_hook_state) + bstack1ll11_opy_ (u"ࠤࠥ៽"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣ៾") + str(target) + bstack1ll11_opy_ (u"ࠦࠧ៿"))
            return None
        instance = TestFramework.bstack1ll111l1lll_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢ᠀") + str(target) + bstack1ll11_opy_ (u"ࠨࠢ᠁"))
            return None
        bstack11l11ll11l1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, PytestBDDFramework.bstack11l11ll111l_opy_, {})
        if os.getenv(bstack1ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣ᠂"), bstack1ll11_opy_ (u"ࠣ࠳ࠥ᠃")) == bstack1ll11_opy_ (u"ࠤ࠴ࠦ᠄"):
            bstack11l1ll1ll11_opy_ = bstack1ll11_opy_ (u"ࠥ࠾ࠧ᠅").join((scope, fixturename))
            bstack11l1ll1llll_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11ll1l1l_opy_ = {
                bstack1ll11_opy_ (u"ࠦࡰ࡫ࡹࠣ᠆"): bstack11l1ll1ll11_opy_,
                bstack1ll11_opy_ (u"ࠧࡺࡡࡨࡵࠥ᠇"): PytestBDDFramework.__11l11lll111_opy_(request.node, scenario),
                bstack1ll11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢ᠈"): fixturedef,
                bstack1ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᠉"): scope,
                bstack1ll11_opy_ (u"ࠣࡶࡼࡴࡪࠨ᠊"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨ᠋"), None)):
                    bstack11l11ll1l1l_opy_[bstack1ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣ᠌")] = TestFramework.bstack1l111l11l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l11ll1l1l_opy_[bstack1ll11_opy_ (u"ࠦࡺࡻࡩࡥࠤ᠍")] = uuid4().__str__()
                bstack11l11ll1l1l_opy_[PytestBDDFramework.bstack11l11l1ll11_opy_] = bstack11l1ll1llll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11ll1l1l_opy_[PytestBDDFramework.bstack11l1ll111l1_opy_] = bstack11l1ll1llll_opy_
            if bstack11l1ll1ll11_opy_ in bstack11l11ll11l1_opy_:
                bstack11l11ll11l1_opy_[bstack11l1ll1ll11_opy_].update(bstack11l11ll1l1l_opy_)
                self.logger.debug(bstack1ll11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨ᠎") + str(bstack11l11ll11l1_opy_[bstack11l1ll1ll11_opy_]) + bstack1ll11_opy_ (u"ࠨࠢ᠏"))
            else:
                bstack11l11ll11l1_opy_[bstack11l1ll1ll11_opy_] = bstack11l11ll1l1l_opy_
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥ᠐") + str(len(bstack11l11ll11l1_opy_)) + bstack1ll11_opy_ (u"ࠣࠤ᠑"))
        TestFramework.bstack1l11lllll_opy_(instance, PytestBDDFramework.bstack11l11ll111l_opy_, bstack11l11ll11l1_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᠒") + str(instance.ref()) + bstack1ll11_opy_ (u"ࠥࠦ᠓"))
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
            PytestBDDFramework.bstack11l11ll111l_opy_: {},
            PytestBDDFramework.bstack11l1l1ll111_opy_: {},
            PytestBDDFramework.bstack11l1lll11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l11lllll_opy_(ob, TestFramework.bstack11l1l11l1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l11lllll_opy_(ob, TestFramework.bstack1l11llll11l_opy_, context.platform_index)
        TestFramework.bstack1l1l111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦ᠔") + str(TestFramework.bstack1l1l111l_opy_.keys()) + bstack1ll11_opy_ (u"ࠧࠨ᠕"))
        return ob
    @staticmethod
    def __11l1ll1l111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll11_opy_ (u"࠭ࡩࡥࠩ᠖"): id(step),
                bstack1ll11_opy_ (u"ࠧࡵࡧࡻࡸࠬ᠗"): step.name,
                bstack1ll11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ᠘"): step.keyword,
            })
        meta = {
            bstack1ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ᠙"): {
                bstack1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᠚"): feature.name,
                bstack1ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩ᠛"): feature.filename,
                bstack1ll11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᠜"): feature.description
            },
            bstack1ll11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ᠝"): {
                bstack1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᠞"): scenario.name
            },
            bstack1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᠟"): steps,
            bstack1ll11_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᠠ"): PytestBDDFramework.__11l11ll11ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l1l11l1ll_opy_: meta
            }
        )
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᠡ")
        global _1l1111111l1_opy_
        platform_index = os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᠢ")]
        bstack1l111l111ll_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), bstack11l1ll1lll1_opy_)
        if not os.path.exists(bstack1l111l111ll_opy_) or not os.path.isdir(bstack1l111l111ll_opy_):
            return
        logs = hook.get(bstack1ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᠣ"), [])
        with os.scandir(bstack1l111l111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1111111l1_opy_:
                    self.logger.info(bstack1ll11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᠤ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll11_opy_ (u"ࠢࠣᠥ")
                    log_entry = bstack1l1l1l1lll1_opy_(
                        kind=bstack1ll11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᠦ"),
                        message=bstack1ll11_opy_ (u"ࠤࠥᠧ"),
                        level=bstack1ll11_opy_ (u"ࠥࠦᠨ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11llll1lll1_opy_=entry.stat().st_size,
                        bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᠩ"),
                        bstack1l11ll_opy_=os.path.abspath(entry.path),
                        bstack11l1l1lllll_opy_=hook.get(TestFramework.bstack11l1l11ll1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1111111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᠪ")]
        bstack11l1l1llll1_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), bstack11l1ll1lll1_opy_, bstack11l1l1l1l11_opy_)
        if not os.path.exists(bstack11l1l1llll1_opy_) or not os.path.isdir(bstack11l1l1llll1_opy_):
            self.logger.info(bstack1ll11_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᠫ").format(bstack11l1l1llll1_opy_))
        else:
            self.logger.info(bstack1ll11_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᠬ").format(bstack11l1l1llll1_opy_))
            with os.scandir(bstack11l1l1llll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1111111l1_opy_:
                        self.logger.info(bstack1ll11_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᠭ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll11_opy_ (u"ࠤࠥᠮ")
                        log_entry = bstack1l1l1l1lll1_opy_(
                            kind=bstack1ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᠯ"),
                            message=bstack1ll11_opy_ (u"ࠦࠧᠰ"),
                            level=bstack1ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᠱ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11llll1lll1_opy_=entry.stat().st_size,
                            bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᠲ"),
                            bstack1l11ll_opy_=os.path.abspath(entry.path),
                            bstack1l111l1ll11_opy_=hook.get(TestFramework.bstack11l1l11ll1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1111111l1_opy_.add(abs_path)
        hook[bstack1ll11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᠳ")] = logs
    def bstack11llllll1ll_opy_(
        self,
        bstack1l1111ll11l_opy_: bstack1l1l1l111l1_opy_,
        entries: List[bstack1l1l1l1lll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᠴ"))
        req.platform_index = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11llll11l_opy_)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᠵ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111ll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111ll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111ll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11l11llll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11111lll1_opy_)
            log_entry.uuid = entry.bstack11l1l1lllll_opy_ if entry.bstack11l1l1lllll_opy_ else TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11l1lll11_opy_)
            log_entry.test_framework_state = bstack1l1111ll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᠶ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᠷ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11llll1lll1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l111l1llll_opy_():
            bstack11l111ll1_opy_ = datetime.now()
            try:
                self.bstack1l1ll1ll111_opy_.LogCreatedEvent(req)
                bstack1l1111ll11l_opy_.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᠸ"), datetime.now() - bstack11l111ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᠹ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll11llll11_opy_.enqueue(bstack1l111l1llll_opy_)
    def __11l1ll1l1l1_opy_(self, instance) -> None:
        bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᠺ")
        bstack11l11l1l111_opy_ = {bstack1ll11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᠻ"): bstack1l1ll1l11ll_opy_.bstack11l1ll11l11_opy_()}
        TestFramework.bstack11l1l1l1111_opy_(instance, bstack11l11l1l111_opy_)
    @staticmethod
    def __11l1l1l11ll_opy_(instance, args):
        request, bstack11l11llll11_opy_ = args
        bstack11l11ll1111_opy_ = id(bstack11l11llll11_opy_)
        bstack11l1l11111l_opy_ = instance.data[TestFramework.bstack11l1l11l1ll_opy_]
        step = next(filter(lambda st: st[bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬᠼ")] == bstack11l11ll1111_opy_, bstack11l1l11111l_opy_[bstack1ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᠽ")]), None)
        step.update({
            bstack1ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᠾ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11l1l11111l_opy_[bstack1ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᠿ")]) if st[bstack1ll11_opy_ (u"࠭ࡩࡥࠩᡀ")] == step[bstack1ll11_opy_ (u"ࠧࡪࡦࠪᡁ")]), None)
        if index is not None:
            bstack11l1l11111l_opy_[bstack1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᡂ")][index] = step
        instance.data[TestFramework.bstack11l1l11l1ll_opy_] = bstack11l1l11111l_opy_
    @staticmethod
    def __11l1l1lll11_opy_(instance, args):
        bstack1ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᡃ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11l11llll11_opy_ = args[1]
        bstack11l11ll1111_opy_ = id(bstack11l11llll11_opy_)
        bstack11l1l11111l_opy_ = instance.data[TestFramework.bstack11l1l11l1ll_opy_]
        step = None
        if bstack11l11ll1111_opy_ is not None and bstack11l1l11111l_opy_.get(bstack1ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᡄ")):
            step = next(filter(lambda st: st[bstack1ll11_opy_ (u"ࠫ࡮ࡪࠧᡅ")] == bstack11l11ll1111_opy_, bstack11l1l11111l_opy_[bstack1ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᡆ")]), None)
            step.update({
                bstack1ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᡇ"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᡈ"): bstack1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᡉ"),
                bstack1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᡊ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᡋ"): bstack1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᡌ"),
                })
        index = next((i for i, st in enumerate(bstack11l1l11111l_opy_[bstack1ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᡍ")]) if st[bstack1ll11_opy_ (u"࠭ࡩࡥࠩᡎ")] == step[bstack1ll11_opy_ (u"ࠧࡪࡦࠪᡏ")]), None)
        if index is not None:
            bstack11l1l11111l_opy_[bstack1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᡐ")][index] = step
        instance.data[TestFramework.bstack11l1l11l1ll_opy_] = bstack11l1l11111l_opy_
    @staticmethod
    def __11l11ll11ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᡑ")):
                examples = list(node.callspec.params[bstack1ll11_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᡒ")].values())
            return examples
        except:
            return []
    def bstack1l1111l1l1l_opy_(self, instance: bstack1l1l1l111l1_opy_, bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1ll1l1_opy_ = (
            PytestBDDFramework.bstack11l1l1ll1ll_opy_
            if bstack1ll11l11lll_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l11lll11l_opy_
        )
        hook = PytestBDDFramework.bstack11l1l11l11l_opy_(instance, bstack11l1l1ll1l1_opy_)
        entries = hook.get(TestFramework.bstack11l1l111ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, []))
        return entries
    def bstack1l1111llll1_opy_(self, instance: bstack1l1l1l111l1_opy_, bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1ll1l1_opy_ = (
            PytestBDDFramework.bstack11l1l1ll1ll_opy_
            if bstack1ll11l11lll_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l11lll11l_opy_
        )
        PytestBDDFramework.bstack11l1l1l11l1_opy_(instance, bstack11l1l1ll1l1_opy_)
        TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11l11l1ll1l_opy_, []).clear()
    @staticmethod
    def bstack11l1l11l11l_opy_(instance: bstack1l1l1l111l1_opy_, bstack11l1l1ll1l1_opy_: str):
        bstack11l11lll1l1_opy_ = (
            PytestBDDFramework.bstack11l1l1ll111_opy_
            if bstack11l1l1ll1l1_opy_ == PytestBDDFramework.bstack11l11lll11l_opy_
            else PytestBDDFramework.bstack11l1lll11l1_opy_
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
        hook = PytestBDDFramework.bstack11l1l11l11l_opy_(instance, bstack11l1l1ll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1l111ll1_opy_, []).clear()
    @staticmethod
    def __11l1ll11ll1_opy_(instance: bstack1l1l1l111l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᡓ"), None)):
            return
        if os.getenv(bstack1ll11_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᡔ"), bstack1ll11_opy_ (u"ࠨ࠱ࠣᡕ")) != bstack1ll11_opy_ (u"ࠢ࠲ࠤᡖ"):
            PytestBDDFramework.logger.warning(bstack1ll11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᡗ"))
            return
        bstack11l11lll1ll_opy_ = {
            bstack1ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᡘ"): (PytestBDDFramework.bstack11l1l1ll1ll_opy_, PytestBDDFramework.bstack11l1lll11l1_opy_),
            bstack1ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᡙ"): (PytestBDDFramework.bstack11l11lll11l_opy_, PytestBDDFramework.bstack11l1l1ll111_opy_),
        }
        for when in (bstack1ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᡚ"), bstack1ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᡛ"), bstack1ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᡜ")):
            bstack11l1ll1ll1l_opy_ = args[1].get_records(when)
            if not bstack11l1ll1ll1l_opy_:
                continue
            records = [
                bstack1l1l1l1lll1_opy_(
                    kind=TestFramework.bstack11lllllllll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᡝ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᡞ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1ll1ll1l_opy_
                if isinstance(getattr(r, bstack1ll11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᡟ"), None), str) and r.message.strip()
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
    def __11l1l11l111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l1ll1l1ll_opy_(request.node, scenario)
        bstack11l1lll1l11_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l1lll1l11_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l11l1lll11_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111111_opy_: test_id,
            TestFramework.bstack1l11ll1ll1l_opy_: test_name,
            TestFramework.bstack11lll1llll1_opy_: test_id,
            TestFramework.bstack11l1lll1111_opy_: bstack11l1lll1l11_opy_,
            TestFramework.bstack11l11l1llll_opy_: PytestBDDFramework.__11l11lll111_opy_(feature, scenario),
            TestFramework.bstack11l1l1l1ll1_opy_: code,
            TestFramework.bstack11lll11l111_opy_: TestFramework.bstack11l1lll1l1l_opy_,
            TestFramework.bstack11ll1111l1l_opy_: test_name
        }
    @staticmethod
    def __11l1ll1l1ll_opy_(node, scenario):
        if hasattr(node, bstack1ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᡠ")):
            parts = node.nodeid.rsplit(bstack1ll11_opy_ (u"ࠦࡠࠨᡡ"))
            params = parts[-1]
            return bstack1ll11_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᡢ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l11lll111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᡣ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᡤ")) else [])
    @staticmethod
    def __11l1l1l111l_opy_(location):
        return bstack1ll11_opy_ (u"ࠣ࠼࠽ࠦᡥ").join(filter(lambda x: isinstance(x, str), location))