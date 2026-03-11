# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11lll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1111l_opy_ import bstack11ll111l1ll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll11l1ll1l_opy_,
    TestHookState,
    bstack1lll11l1l1l_opy_,
    bstack1l1ll11l111_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1111ll1ll_opy_
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll111ll1ll_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l111_opy_ import bstack1ll1ll1l11l_opy_
bstack1l1111l1lll_opy_ = bstack1l1111ll1ll_opy_()
bstack1l111ll1111_opy_ = bstack1ll111_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᜆ")
bstack11l1lll1l1l_opy_ = bstack1ll111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᜇ")
bstack11ll111111l_opy_ = bstack1ll111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᜈ")
bstack11ll11llll1_opy_ = 1.0
_1l111ll1lll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11ll111lll1_opy_ = bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᜉ")
    bstack11ll11ll1l1_opy_ = bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᜊ")
    bstack11ll11l111l_opy_ = bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᜋ")
    bstack11ll11l1lll_opy_ = bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᜌ")
    bstack11l1l1l111l_opy_ = bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᜍ")
    bstack11ll111ll11_opy_: bool
    bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_  = None
    bstack11l1ll11lll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1lll11ll_opy_: Dict[str, str],
        bstack1l11lll1l1l_opy_: List[str]=[bstack1ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᜎ")],
        bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_ = None,
        bstack1ll1lll11ll_opy_=None
    ):
        super().__init__(bstack1l11lll1l1l_opy_, bstack11l1lll11ll_opy_, bstack1ll1ll1l111_opy_)
        self.bstack11ll111ll11_opy_ = any(bstack1ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᜏ") in item.lower() for item in bstack1l11lll1l1l_opy_)
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
    def track_event(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l1ll11lll_opy_:
            bstack11ll111l1ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᜐ") + str(test_hook_state) + bstack1ll111_opy_ (u"ࠦࠧᜑ"))
            return
        if not self.bstack11ll111ll11_opy_:
            self.logger.warning(bstack1ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᜒ") + str(str(self.bstack1l11lll1l1l_opy_)) + bstack1ll111_opy_ (u"ࠨࠢᜓ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ᜔") + str(kwargs) + bstack1ll111_opy_ (u"ࠣࠤ᜕"))
            return
        instance = self.__11l1lllllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣ᜖") + str(args) + bstack1ll111_opy_ (u"ࠥࠦ᜗"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll11lll_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1l111l1l1l_opy_.value)
                name = str(EVENTS.bstack1l111l1l1l_opy_.name)+bstack1ll111_opy_ (u"ࠦ࠿ࠨ᜘")+str(test_framework_state.name)
                TestFramework.bstack11l1ll1ll11_opy_(instance, name, bstack1l1l1l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤ᜙").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack11llll1lll1_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11l1lllll1l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᜚") + str(test_hook_state) + bstack1ll111_opy_ (u"ࠢࠣ᜛"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l1111ll111_opy_):
                    TestFramework.bstack1ll1ll1lll1_opy_(instance, TestFramework.bstack1l1111ll111_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1l1ll11l_opy_(instance, args)
                    self.logger.debug(bstack1ll111_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᜜") + str(test_hook_state) + bstack1ll111_opy_ (u"ࠤࠥ᜝"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_):
                    TestFramework.bstack1ll1ll1lll1_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᜞") + str(test_hook_state) + bstack1ll111_opy_ (u"ࠦࠧᜟ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l1l1l11l1_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1llll11l_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11ll11111ll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll11l1l1l_opy_(instance, *args)
                self.__11l1l1ll111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1ll11lll_opy_:
                self.__11l1ll1llll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᜠ") + str(instance.ref()) + bstack1ll111_opy_ (u"ࠨࠢᜡ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll11l1111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll11lll_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1l111l1l1l_opy_.name)+bstack1ll111_opy_ (u"ࠢ࠻ࠤᜢ")+str(test_framework_state.name)
                bstack1l1l1l111_opy_ = TestFramework.bstack11l1llll1l1_opy_(instance, name)
                bstack111ll11111_opy_.end(EVENTS.bstack1l111l1l1l_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᜣ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᜤ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᜥ").format(e))
    def bstack1l111ll111l_opy_(self):
        return self.bstack11ll111ll11_opy_
    def bstack1l1111lllll_opy_(self):
        return False
    def __11l1l1l1l1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᜦ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11l1111l1_opy_(rep, [bstack1ll111_opy_ (u"ࠧࡽࡨࡦࡰࠥᜧ"), bstack1ll111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᜨ"), bstack1ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᜩ"), bstack1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᜪ"), bstack1ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᜫ"), bstack1ll111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᜬ")])
        return None
    def __11ll11l1l1l_opy_(self, instance: bstack1ll11l1ll1l_opy_, *args):
        result = self.__11l1l1l1l1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll11ll1l1_opy_ = None
        if result.get(bstack1ll111_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᜭ"), None) == bstack1ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᜮ") and len(args) > 1 and getattr(args[1], bstack1ll111_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᜯ"), None) is not None:
            failure = [{bstack1ll111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᜰ"): [args[1].excinfo.exconly(), result.get(bstack1ll111_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᜱ"), None)]}]
            bstack1lll11ll1l1_opy_ = bstack1ll111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᜲ") if bstack1ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᜳ") in getattr(args[1].excinfo, bstack1ll111_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨ᜴"), bstack1ll111_opy_ (u"ࠧࠨ᜵")) else bstack1ll111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ᜶")
        bstack11ll1111lll_opy_ = result.get(bstack1ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ᜷"), TestFramework.bstack11l1lll1111_opy_)
        if bstack11ll1111lll_opy_ != TestFramework.bstack11l1lll1111_opy_:
            TestFramework.bstack1ll1ll1lll1_opy_(instance, TestFramework.bstack1l111llll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1ll1lll1_opy_(instance, {
            TestFramework.bstack11llll11111_opy_: failure,
            TestFramework.bstack11l1llllll1_opy_: bstack1lll11ll1l1_opy_,
            TestFramework.bstack11lll1llll1_opy_: bstack11ll1111lll_opy_,
        })
    def __11l1lllllll_opy_(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11ll111l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l1l1111_opy_ bstack11l1l1l1ll1_opy_ this to be bstack1ll111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᜸")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll1111ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ᜹"), None), bstack1ll111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᜺"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll111_opy_ (u"ࠦࡳࡵࡤࡦࠤ᜻"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᜼"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1l1ll1l1_opy_(target) if target else None
        return instance
    def __11l1ll1llll_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1l1ll1l1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, PytestBDDFramework.bstack11ll11ll1l1_opy_, {})
        if not key in bstack11l1l1ll1l1_opy_:
            bstack11l1l1ll1l1_opy_[key] = []
        bstack11l1l1lll11_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, PytestBDDFramework.bstack11ll11l111l_opy_, {})
        if not key in bstack11l1l1lll11_opy_:
            bstack11l1l1lll11_opy_[key] = []
        bstack11l1ll1ll1l_opy_ = {
            PytestBDDFramework.bstack11ll11ll1l1_opy_: bstack11l1l1ll1l1_opy_,
            PytestBDDFramework.bstack11ll11l111l_opy_: bstack11l1l1lll11_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll111_opy_ (u"ࠨ࡫ࡦࡻࠥ᜽"): key,
                TestFramework.bstack11l1l1lll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll11111_opy_: TestFramework.bstack11l1l1l1l11_opy_,
                TestFramework.bstack11l1ll11l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1111111_opy_: [],
                TestFramework.bstack11l1llll111_opy_: hook_name,
                TestFramework.bstack11l1ll1l1l1_opy_: bstack1l1lllll11l_opy_.bstack11ll1111l11_opy_()
            }
            bstack11l1l1ll1l1_opy_[key].append(hook)
            bstack11l1ll1ll1l_opy_[PytestBDDFramework.bstack11ll11l1lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1111l_opy_ = bstack11l1l1ll1l1_opy_.get(key, [])
            hook = bstack11l1ll1111l_opy_.pop() if bstack11l1ll1111l_opy_ else None
            if hook:
                result = self.__11l1l1l1l1l_opy_(*args)
                if result:
                    bstack11l1ll111l1_opy_ = result.get(bstack1ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ᜾"), TestFramework.bstack11l1l1l1l11_opy_)
                    if bstack11l1ll111l1_opy_ != TestFramework.bstack11l1l1l1l11_opy_:
                        hook[TestFramework.bstack11l1ll11111_opy_] = bstack11l1ll111l1_opy_
                hook[TestFramework.bstack11l1llll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1ll1l1l1_opy_] = bstack1l1lllll11l_opy_.bstack11ll1111l11_opy_()
                self.bstack11l1l1l1lll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1lll111l_opy_, [])
                self.bstack1l11l11l11l_opy_(instance, logs)
                bstack11l1l1lll11_opy_[key].append(hook)
                bstack11l1ll1ll1l_opy_[PytestBDDFramework.bstack11l1l1l111l_opy_] = key
        TestFramework.bstack11l1ll1lll1_opy_(instance, bstack11l1ll1ll1l_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢ᜿") + str(bstack11l1l1lll11_opy_) + bstack1ll111_opy_ (u"ࠤࠥᝀ"))
    def __11ll111l1l1_opy_(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11l1111l1_opy_(args[0], [bstack1ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᝁ"), bstack1ll111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᝂ"), bstack1ll111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᝃ"), bstack1ll111_opy_ (u"ࠨࡩࡥࡵࠥᝄ"), bstack1ll111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᝅ"), bstack1ll111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᝆ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll111_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᝇ")) else fixturedef.get(bstack1ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᝈ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᝉ")) else None
        node = request.node if hasattr(request, bstack1ll111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᝊ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᝋ")) else None
        baseid = fixturedef.get(bstack1ll111_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᝌ"), None) or bstack1ll111_opy_ (u"ࠣࠤᝍ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll111_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᝎ")):
            target = PytestBDDFramework.__11ll11lll11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll111_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᝏ")) else None
            if target and not TestFramework.bstack1ll1l1ll1l1_opy_(target):
                self.__11ll1111ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᝐ") + str(test_hook_state) + bstack1ll111_opy_ (u"ࠧࠨᝑ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᝒ") + str(target) + bstack1ll111_opy_ (u"ࠢࠣᝓ"))
            return None
        instance = TestFramework.bstack1ll1l1ll1l1_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥ᝔") + str(target) + bstack1ll111_opy_ (u"ࠤࠥ᝕"))
            return None
        bstack11ll111ll1l_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, PytestBDDFramework.bstack11ll111lll1_opy_, {})
        if os.getenv(bstack1ll111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦ᝖"), bstack1ll111_opy_ (u"ࠦ࠶ࠨ᝗")) == bstack1ll111_opy_ (u"ࠧ࠷ࠢ᝘"):
            bstack11l1l1lllll_opy_ = bstack1ll111_opy_ (u"ࠨ࠺ࠣ᝙").join((scope, fixturename))
            bstack11ll11l1l11_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1ll11l11_opy_ = {
                bstack1ll111_opy_ (u"ࠢ࡬ࡧࡼࠦ᝚"): bstack11l1l1lllll_opy_,
                bstack1ll111_opy_ (u"ࠣࡶࡤ࡫ࡸࠨ᝛"): PytestBDDFramework.__11l1l1llll1_opy_(request.node, scenario),
                bstack1ll111_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥ᝜"): fixturedef,
                bstack1ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ᝝"): scope,
                bstack1ll111_opy_ (u"ࠦࡹࡿࡰࡦࠤ᝞"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤ᝟"), None)):
                    bstack11l1ll11l11_opy_[bstack1ll111_opy_ (u"ࠨࡴࡺࡲࡨࠦᝠ")] = TestFramework.bstack1l111llllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1ll11l11_opy_[bstack1ll111_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᝡ")] = uuid4().__str__()
                bstack11l1ll11l11_opy_[PytestBDDFramework.bstack11l1ll11l1l_opy_] = bstack11ll11l1l11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1ll11l11_opy_[PytestBDDFramework.bstack11l1llll1ll_opy_] = bstack11ll11l1l11_opy_
            if bstack11l1l1lllll_opy_ in bstack11ll111ll1l_opy_:
                bstack11ll111ll1l_opy_[bstack11l1l1lllll_opy_].update(bstack11l1ll11l11_opy_)
                self.logger.debug(bstack1ll111_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᝢ") + str(bstack11ll111ll1l_opy_[bstack11l1l1lllll_opy_]) + bstack1ll111_opy_ (u"ࠤࠥᝣ"))
            else:
                bstack11ll111ll1l_opy_[bstack11l1l1lllll_opy_] = bstack11l1ll11l11_opy_
                self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᝤ") + str(len(bstack11ll111ll1l_opy_)) + bstack1ll111_opy_ (u"ࠦࠧᝥ"))
        TestFramework.bstack1ll1ll1lll1_opy_(instance, PytestBDDFramework.bstack11ll111lll1_opy_, bstack11ll111ll1l_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᝦ") + str(instance.ref()) + bstack1ll111_opy_ (u"ࠨࠢᝧ"))
        return instance
    def __11ll1111ll1_opy_(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11lll1ll_opy_.create_context(target)
        ob = bstack1ll11l1ll1l_opy_(ctx, self.bstack1l11lll1l1l_opy_, self.bstack11l1lll11ll_opy_, test_framework_state)
        TestFramework.bstack11l1ll1lll1_opy_(ob, {
            TestFramework.bstack1l11llllll1_opy_: context.test_framework_name,
            TestFramework.bstack1l111l111ll_opy_: context.test_framework_version,
            TestFramework.bstack11l1lll1ll1_opy_: [],
            PytestBDDFramework.bstack11ll111lll1_opy_: {},
            PytestBDDFramework.bstack11ll11l111l_opy_: {},
            PytestBDDFramework.bstack11ll11ll1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1ll1lll1_opy_(ob, TestFramework.bstack11ll111l11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1ll1lll1_opy_(ob, TestFramework.bstack1l1l1l1ll11_opy_, context.platform_index)
        TestFramework.bstack1ll1llllll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᝨ") + str(TestFramework.bstack1ll1llllll1_opy_.keys()) + bstack1ll111_opy_ (u"ࠣࠤᝩ"))
        return ob
    @staticmethod
    def __11l1l1ll11l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll111_opy_ (u"ࠩ࡬ࡨࠬᝪ"): id(step),
                bstack1ll111_opy_ (u"ࠪࡸࡪࡾࡴࠨᝫ"): step.name,
                bstack1ll111_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᝬ"): step.keyword,
            })
        meta = {
            bstack1ll111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭᝭"): {
                bstack1ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝮ"): feature.name,
                bstack1ll111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᝯ"): feature.filename,
                bstack1ll111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᝰ"): feature.description
            },
            bstack1ll111_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ᝱"): {
                bstack1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨᝲ"): scenario.name
            },
            bstack1ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᝳ"): steps,
            bstack1ll111_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧ᝴"): PytestBDDFramework.__11ll11l11l1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l1lll1lll_opy_: meta
            }
        )
    def bstack11l1l1l1lll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ᝵")
        global _1l111ll1lll_opy_
        platform_index = os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᝶")]
        bstack1l111l11111_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l111ll1111_opy_ + str(platform_index)), bstack11l1lll1l1l_opy_)
        if not os.path.exists(bstack1l111l11111_opy_) or not os.path.isdir(bstack1l111l11111_opy_):
            return
        logs = hook.get(bstack1ll111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᝷"), [])
        with os.scandir(bstack1l111l11111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111ll1lll_opy_:
                    self.logger.info(bstack1ll111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ᝸").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll111_opy_ (u"ࠥࠦ᝹")
                    log_entry = bstack1l1ll11l111_opy_(
                        kind=bstack1ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᝺"),
                        message=bstack1ll111_opy_ (u"ࠧࠨ᝻"),
                        level=bstack1ll111_opy_ (u"ࠨࠢ᝼"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111lll111_opy_=entry.stat().st_size,
                        bstack1l111lllll1_opy_=bstack1ll111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ᝽"),
                        bstack11l111_opy_=os.path.abspath(entry.path),
                        bstack11l1lllll11_opy_=hook.get(TestFramework.bstack11l1l1lll1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111ll1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᝾")]
        bstack11ll11l11ll_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l111ll1111_opy_ + str(platform_index)), bstack11l1lll1l1l_opy_, bstack11ll111111l_opy_)
        if not os.path.exists(bstack11ll11l11ll_opy_) or not os.path.isdir(bstack11ll11l11ll_opy_):
            self.logger.info(bstack1ll111_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦ᝿").format(bstack11ll11l11ll_opy_))
        else:
            self.logger.info(bstack1ll111_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤក").format(bstack11ll11l11ll_opy_))
            with os.scandir(bstack11ll11l11ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111ll1lll_opy_:
                        self.logger.info(bstack1ll111_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤខ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll111_opy_ (u"ࠧࠨគ")
                        log_entry = bstack1l1ll11l111_opy_(
                            kind=bstack1ll111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣឃ"),
                            message=bstack1ll111_opy_ (u"ࠢࠣង"),
                            level=bstack1ll111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧច"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111lll111_opy_=entry.stat().st_size,
                            bstack1l111lllll1_opy_=bstack1ll111_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤឆ"),
                            bstack11l111_opy_=os.path.abspath(entry.path),
                            bstack1l11l1l11ll_opy_=hook.get(TestFramework.bstack11l1l1lll1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111ll1lll_opy_.add(abs_path)
        hook[bstack1ll111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣជ")] = logs
    def bstack1l11l11l11l_opy_(
        self,
        bstack1l111l11l1l_opy_: bstack1ll11l1ll1l_opy_,
        entries: List[bstack1l1ll11l111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣឈ"))
        req.platform_index = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack1ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦញ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111l11l1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111l11l1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111l11l1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l11llllll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l111l111ll_opy_)
            log_entry.uuid = entry.bstack11l1lllll11_opy_ if entry.bstack11l1lllll11_opy_ else TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l1l1ll11ll_opy_)
            log_entry.test_framework_state = bstack1l111l11l1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧដ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤឋ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111lll111_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1111l1l11_opy_():
            bstack1ll1l1l111_opy_ = datetime.now()
            try:
                self.bstack1ll1lll11ll_opy_.LogCreatedEvent(req)
                bstack1l111l11l1l_opy_.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧឌ"), datetime.now() - bstack1ll1l1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣឍ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1ll1l111_opy_.enqueue(bstack1l1111l1l11_opy_)
    def __11l1l1ll111_opy_(self, instance) -> None:
        bstack1ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣណ")
        bstack11l1ll1ll1l_opy_ = {bstack1ll111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨត"): bstack1l1lllll11l_opy_.bstack11ll1111l11_opy_()}
        TestFramework.bstack11l1ll1lll1_opy_(instance, bstack11l1ll1ll1l_opy_)
    @staticmethod
    def __11l1l1l11l1_opy_(instance, args):
        request, bstack11ll11lll1l_opy_ = args
        bstack11ll11l1ll1_opy_ = id(bstack11ll11lll1l_opy_)
        bstack11l1l1l11ll_opy_ = instance.data[TestFramework.bstack11l1lll1lll_opy_]
        step = next(filter(lambda st: st[bstack1ll111_opy_ (u"ࠬ࡯ࡤࠨថ")] == bstack11ll11l1ll1_opy_, bstack11l1l1l11ll_opy_[bstack1ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬទ")]), None)
        step.update({
            bstack1ll111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫធ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11l1l1l11ll_opy_[bstack1ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧន")]) if st[bstack1ll111_opy_ (u"ࠩ࡬ࡨࠬប")] == step[bstack1ll111_opy_ (u"ࠪ࡭ࡩ࠭ផ")]), None)
        if index is not None:
            bstack11l1l1l11ll_opy_[bstack1ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪព")][index] = step
        instance.data[TestFramework.bstack11l1lll1lll_opy_] = bstack11l1l1l11ll_opy_
    @staticmethod
    def __11l1llll11l_opy_(instance, args):
        bstack1ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣភ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll11lll1l_opy_ = args[1]
        bstack11ll11l1ll1_opy_ = id(bstack11ll11lll1l_opy_)
        bstack11l1l1l11ll_opy_ = instance.data[TestFramework.bstack11l1lll1lll_opy_]
        step = None
        if bstack11ll11l1ll1_opy_ is not None and bstack11l1l1l11ll_opy_.get(bstack1ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬម")):
            step = next(filter(lambda st: st[bstack1ll111_opy_ (u"ࠧࡪࡦࠪយ")] == bstack11ll11l1ll1_opy_, bstack11l1l1l11ll_opy_[bstack1ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧរ")]), None)
            step.update({
                bstack1ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧល"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪវ"): bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫឝ"),
                bstack1ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ឞ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ស"): bstack1ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧហ"),
                })
        index = next((i for i, st in enumerate(bstack11l1l1l11ll_opy_[bstack1ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧឡ")]) if st[bstack1ll111_opy_ (u"ࠩ࡬ࡨࠬអ")] == step[bstack1ll111_opy_ (u"ࠪ࡭ࡩ࠭ឣ")]), None)
        if index is not None:
            bstack11l1l1l11ll_opy_[bstack1ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪឤ")][index] = step
        instance.data[TestFramework.bstack11l1lll1lll_opy_] = bstack11l1l1l11ll_opy_
    @staticmethod
    def __11ll11l11l1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧឥ")):
                examples = list(node.callspec.params[bstack1ll111_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬឦ")].values())
            return examples
        except:
            return []
    def bstack1l11111l1ll_opy_(self, instance: bstack1ll11l1ll1l_opy_, bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111l1l_opy_ = (
            PytestBDDFramework.bstack11ll11l1lll_opy_
            if bstack1ll1l1l1l1l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1l1l111l_opy_
        )
        hook = PytestBDDFramework.bstack11ll11ll111_opy_(instance, bstack11ll1111l1l_opy_)
        entries = hook.get(TestFramework.bstack11ll1111111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11l1lll1ll1_opy_, []))
        return entries
    def bstack1l11l11111l_opy_(self, instance: bstack1ll11l1ll1l_opy_, bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111l1l_opy_ = (
            PytestBDDFramework.bstack11ll11l1lll_opy_
            if bstack1ll1l1l1l1l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1l1l111l_opy_
        )
        PytestBDDFramework.bstack11l1ll1l1ll_opy_(instance, bstack11ll1111l1l_opy_)
        TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11l1lll1ll1_opy_, []).clear()
    @staticmethod
    def bstack11ll11ll111_opy_(instance: bstack1ll11l1ll1l_opy_, bstack11ll1111l1l_opy_: str):
        bstack11ll11ll1ll_opy_ = (
            PytestBDDFramework.bstack11ll11l111l_opy_
            if bstack11ll1111l1l_opy_ == PytestBDDFramework.bstack11l1l1l111l_opy_
            else PytestBDDFramework.bstack11ll11ll1l1_opy_
        )
        bstack11ll11ll11l_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11ll1111l1l_opy_, None)
        bstack11ll11111l1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11ll11ll1ll_opy_, None) if bstack11ll11ll11l_opy_ else None
        return (
            bstack11ll11111l1_opy_[bstack11ll11ll11l_opy_][-1]
            if isinstance(bstack11ll11111l1_opy_, dict) and len(bstack11ll11111l1_opy_.get(bstack11ll11ll11l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll1l1ll_opy_(instance: bstack1ll11l1ll1l_opy_, bstack11ll1111l1l_opy_: str):
        hook = PytestBDDFramework.bstack11ll11ll111_opy_(instance, bstack11ll1111l1l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1111111_opy_, []).clear()
    @staticmethod
    def __11ll11111ll_opy_(instance: bstack1ll11l1ll1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧឧ"), None)):
            return
        if os.getenv(bstack1ll111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧឨ"), bstack1ll111_opy_ (u"ࠤ࠴ࠦឩ")) != bstack1ll111_opy_ (u"ࠥ࠵ࠧឪ"):
            PytestBDDFramework.logger.warning(bstack1ll111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨឫ"))
            return
        bstack11l1ll11ll1_opy_ = {
            bstack1ll111_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦឬ"): (PytestBDDFramework.bstack11ll11l1lll_opy_, PytestBDDFramework.bstack11ll11ll1l1_opy_),
            bstack1ll111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣឭ"): (PytestBDDFramework.bstack11l1l1l111l_opy_, PytestBDDFramework.bstack11ll11l111l_opy_),
        }
        for when in (bstack1ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨឮ"), bstack1ll111_opy_ (u"ࠣࡥࡤࡰࡱࠨឯ"), bstack1ll111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦឰ")):
            bstack11l1ll1l111_opy_ = args[1].get_records(when)
            if not bstack11l1ll1l111_opy_:
                continue
            records = [
                bstack1l1ll11l111_opy_(
                    kind=TestFramework.bstack1l11l11ll1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll111_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨឱ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧឲ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1ll1l111_opy_
                if isinstance(getattr(r, bstack1ll111_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨឳ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1lll11l1_opy_, bstack11ll11ll1ll_opy_ = bstack11l1ll11ll1_opy_.get(when, (None, None))
            bstack11l1ll1l11l_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11l1lll11l1_opy_, None) if bstack11l1lll11l1_opy_ else None
            bstack11ll11111l1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11ll11ll1ll_opy_, None) if bstack11l1ll1l11l_opy_ else None
            if isinstance(bstack11ll11111l1_opy_, dict) and len(bstack11ll11111l1_opy_.get(bstack11l1ll1l11l_opy_, [])) > 0:
                hook = bstack11ll11111l1_opy_[bstack11l1ll1l11l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1111111_opy_ in hook:
                    hook[TestFramework.bstack11ll1111111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11l1lll1ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l1lllll1l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l1l1ll1ll_opy_(request.node, scenario)
        bstack11l1ll111ll_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l1ll111ll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l1ll11ll_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1lll1_opy_: test_id,
            TestFramework.bstack1l1l11llll1_opy_: test_name,
            TestFramework.bstack1l11111l1l1_opy_: test_id,
            TestFramework.bstack11ll111l111_opy_: bstack11l1ll111ll_opy_,
            TestFramework.bstack11ll111llll_opy_: PytestBDDFramework.__11l1l1llll1_opy_(feature, scenario),
            TestFramework.bstack11l1lll1l11_opy_: code,
            TestFramework.bstack11lll1llll1_opy_: TestFramework.bstack11l1lll1111_opy_,
            TestFramework.bstack11ll1l1l1ll_opy_: test_name
        }
    @staticmethod
    def __11l1l1ll1ll_opy_(node, scenario):
        if hasattr(node, bstack1ll111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ឴")):
            parts = node.nodeid.rsplit(bstack1ll111_opy_ (u"ࠢ࡜ࠤ឵"))
            params = parts[-1]
            return bstack1ll111_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣា").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l1l1llll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧិ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨី")) else [])
    @staticmethod
    def __11ll11lll11_opy_(location):
        return bstack1ll111_opy_ (u"ࠦ࠿ࡀࠢឹ").join(filter(lambda x: isinstance(x, str), location))