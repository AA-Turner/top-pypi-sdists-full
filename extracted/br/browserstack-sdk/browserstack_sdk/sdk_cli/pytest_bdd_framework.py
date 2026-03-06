# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1llll1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll11lll_opy_ import bstack11ll11lll1l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll11ll111l_opy_,
    TestHookState,
    bstack1lll1l1l1ll_opy_,
    bstack1ll11lllll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l111l11lll_opy_
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1llll1lll_opy_ import bstack1l1ll1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll1111111_opy_
bstack1l11ll111ll_opy_ = bstack1l111l11lll_opy_()
bstack1l11ll11ll1_opy_ = bstack1111_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣ᚞")
bstack11ll11l1lll_opy_ = bstack1111_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧ᚟")
bstack11ll1l1llll_opy_ = bstack1111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᚠ")
bstack11ll11ll1l1_opy_ = 1.0
_1l111l1l11l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11ll1111lll_opy_ = bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᚡ")
    bstack11ll11lll11_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᚢ")
    bstack11ll11ll1ll_opy_ = bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᚣ")
    bstack11ll11l111l_opy_ = bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᚤ")
    bstack11ll1111l1l_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᚥ")
    bstack11ll11ll111_opy_: bool
    bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_  = None
    bstack11ll11llll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll11l1l1l_opy_: Dict[str, str],
        bstack1l1ll111l11_opy_: List[str]=[bstack1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᚦ")],
        bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_ = None,
        bstack1lll111l111_opy_=None
    ):
        super().__init__(bstack1l1ll111l11_opy_, bstack11ll11l1l1l_opy_, bstack1ll1lllll1l_opy_)
        self.bstack11ll11ll111_opy_ = any(bstack1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᚧ") in item.lower() for item in bstack1l1ll111l11_opy_)
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
    def track_event(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11ll11llll1_opy_:
            bstack11ll11lll1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᚨ") + str(test_hook_state) + bstack1111_opy_ (u"ࠧࠨᚩ"))
            return
        if not self.bstack11ll11ll111_opy_:
            self.logger.warning(bstack1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᚪ") + str(str(self.bstack1l1ll111l11_opy_)) + bstack1111_opy_ (u"ࠢࠣᚫ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᚬ") + str(kwargs) + bstack1111_opy_ (u"ࠤࠥᚭ"))
            return
        instance = self.__11ll11l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᚮ") + str(args) + bstack1111_opy_ (u"ࠦࠧᚯ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11ll11llll1_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1ll1l1lll_opy_.value)
                name = str(EVENTS.bstack1ll1l1lll_opy_.name)+bstack1111_opy_ (u"ࠧࡀࠢᚰ")+str(test_framework_state.name)
                TestFramework.bstack11ll11ll11l_opy_(instance, name, bstack1l1l1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᚱ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack11llll1ll1l_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll111l1l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1111_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᚲ") + str(test_hook_state) + bstack1111_opy_ (u"ࠣࠤᚳ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_):
                    TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1ll1ll1l_opy_(instance, args)
                    self.logger.debug(bstack1111_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᚴ") + str(test_hook_state) + bstack1111_opy_ (u"ࠥࠦᚵ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l11l1l111l_opy_):
                    TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᚶ") + str(test_hook_state) + bstack1111_opy_ (u"ࠧࠨᚷ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11ll1l11111_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1lll1l11_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1ll1llll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1lll11ll_opy_(instance, *args)
                self.__11l1lllll11_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11ll11llll1_opy_:
                self.__11l1ll1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᚸ") + str(instance.ref()) + bstack1111_opy_ (u"ࠢࠣᚹ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1111l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11ll11llll1_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1ll1l1lll_opy_.name)+bstack1111_opy_ (u"ࠣ࠼ࠥᚺ")+str(test_framework_state.name)
                bstack1l1l1llll1_opy_ = TestFramework.bstack11ll11111ll_opy_(instance, name)
                bstack1l11l1ll_opy_.end(EVENTS.bstack1ll1l1lll_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᚻ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᚼ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᚽ").format(e))
    def bstack1l111l1ll11_opy_(self):
        return self.bstack11ll11ll111_opy_
    def bstack1l11l11l111_opy_(self):
        return False
    def __11l1lll1lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᚾ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111ll11ll_opy_(rep, [bstack1111_opy_ (u"ࠨࡷࡩࡧࡱࠦᚿ"), bstack1111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᛀ"), bstack1111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᛁ"), bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᛂ"), bstack1111_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᛃ"), bstack1111_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᛄ")])
        return None
    def __11l1lll11ll_opy_(self, instance: bstack1ll11ll111l_opy_, *args):
        result = self.__11l1lll1lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll1111_opy_ = None
        if result.get(bstack1111_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᛅ"), None) == bstack1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᛆ") and len(args) > 1 and getattr(args[1], bstack1111_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᛇ"), None) is not None:
            failure = [{bstack1111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᛈ"): [args[1].excinfo.exconly(), result.get(bstack1111_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᛉ"), None)]}]
            bstack1lll1ll1111_opy_ = bstack1111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᛊ") if bstack1111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᛋ") in getattr(args[1].excinfo, bstack1111_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᛌ"), bstack1111_opy_ (u"ࠨࠢᛍ")) else bstack1111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᛎ")
        bstack11l1lll1111_opy_ = result.get(bstack1111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᛏ"), TestFramework.bstack11l1ll11ll1_opy_)
        if bstack11l1lll1111_opy_ != TestFramework.bstack11l1ll11ll1_opy_:
            TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1llll111_opy_(instance, {
            TestFramework.bstack11lllll11l1_opy_: failure,
            TestFramework.bstack11l1ll1ll11_opy_: bstack1lll1ll1111_opy_,
            TestFramework.bstack11lllll111l_opy_: bstack11l1lll1111_opy_,
        })
    def __11ll11l11ll_opy_(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11ll1l1l1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l11111_opy_ bstack11ll11111l1_opy_ this to be bstack1111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᛐ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll1l1ll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1111_opy_ (u"ࠥࡲࡴࡪࡥࠣᛑ"), None), bstack1111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᛒ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᛓ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᛔ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1l1l1lll_opy_(target) if target else None
        return instance
    def __11l1ll1l1ll_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11ll1l1l1l1_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, PytestBDDFramework.bstack11ll11lll11_opy_, {})
        if not key in bstack11ll1l1l1l1_opy_:
            bstack11ll1l1l1l1_opy_[key] = []
        bstack11ll1111ll1_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, PytestBDDFramework.bstack11ll11ll1ll_opy_, {})
        if not key in bstack11ll1111ll1_opy_:
            bstack11ll1111ll1_opy_[key] = []
        bstack11ll1l11ll1_opy_ = {
            PytestBDDFramework.bstack11ll11lll11_opy_: bstack11ll1l1l1l1_opy_,
            PytestBDDFramework.bstack11ll11ll1ll_opy_: bstack11ll1111ll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1111_opy_ (u"ࠢ࡬ࡧࡼࠦᛕ"): key,
                TestFramework.bstack11l1lll1l1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1l111_opy_: TestFramework.bstack11ll1l11l1l_opy_,
                TestFramework.bstack11ll1111111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll11l11_opy_: [],
                TestFramework.bstack11ll1l1ll1l_opy_: hook_name,
                TestFramework.bstack11ll1l1l11l_opy_: bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()
            }
            bstack11ll1l1l1l1_opy_[key].append(hook)
            bstack11ll1l11ll1_opy_[PytestBDDFramework.bstack11ll11l111l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1lllllll_opy_ = bstack11ll1l1l1l1_opy_.get(key, [])
            hook = bstack11l1lllllll_opy_.pop() if bstack11l1lllllll_opy_ else None
            if hook:
                result = self.__11l1lll1lll_opy_(*args)
                if result:
                    bstack11ll1l1111l_opy_ = result.get(bstack1111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᛖ"), TestFramework.bstack11ll1l11l1l_opy_)
                    if bstack11ll1l1111l_opy_ != TestFramework.bstack11ll1l11l1l_opy_:
                        hook[TestFramework.bstack11l1ll1l111_opy_] = bstack11ll1l1111l_opy_
                hook[TestFramework.bstack11ll111l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1l1l11l_opy_] = bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()
                self.bstack11ll111llll_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l111l1_opy_, [])
                self.bstack1l11l1l1lll_opy_(instance, logs)
                bstack11ll1111ll1_opy_[key].append(hook)
                bstack11ll1l11ll1_opy_[PytestBDDFramework.bstack11ll1111l1l_opy_] = key
        TestFramework.bstack11l1llll111_opy_(instance, bstack11ll1l11ll1_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᛗ") + str(bstack11ll1111ll1_opy_) + bstack1111_opy_ (u"ࠥࠦᛘ"))
    def __11ll1l1l1ll_opy_(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111ll11ll_opy_(args[0], [bstack1111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᛙ"), bstack1111_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᛚ"), bstack1111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᛛ"), bstack1111_opy_ (u"ࠢࡪࡦࡶࠦᛜ"), bstack1111_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᛝ"), bstack1111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᛞ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᛟ")) else fixturedef.get(bstack1111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᛠ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᛡ")) else None
        node = request.node if hasattr(request, bstack1111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᛢ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᛣ")) else None
        baseid = fixturedef.get(bstack1111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᛤ"), None) or bstack1111_opy_ (u"ࠤࠥᛥ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᛦ")):
            target = PytestBDDFramework.__11ll1l11l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᛧ")) else None
            if target and not TestFramework.bstack1ll1l1l1lll_opy_(target):
                self.__11ll1l1ll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᛨ") + str(test_hook_state) + bstack1111_opy_ (u"ࠨࠢᛩ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᛪ") + str(target) + bstack1111_opy_ (u"ࠣࠤ᛫"))
            return None
        instance = TestFramework.bstack1ll1l1l1lll_opy_(target)
        if not instance:
            self.logger.warning(bstack1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦ᛬") + str(target) + bstack1111_opy_ (u"ࠥࠦ᛭"))
            return None
        bstack11l1llll1ll_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, PytestBDDFramework.bstack11ll1111lll_opy_, {})
        if os.getenv(bstack1111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᛮ"), bstack1111_opy_ (u"ࠧ࠷ࠢᛯ")) == bstack1111_opy_ (u"ࠨ࠱ࠣᛰ"):
            bstack11l1lll111l_opy_ = bstack1111_opy_ (u"ࠢ࠻ࠤᛱ").join((scope, fixturename))
            bstack11l1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll111l1ll_opy_ = {
                bstack1111_opy_ (u"ࠣ࡭ࡨࡽࠧᛲ"): bstack11l1lll111l_opy_,
                bstack1111_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᛳ"): PytestBDDFramework.__11l1lll1ll1_opy_(request.node, scenario),
                bstack1111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᛴ"): fixturedef,
                bstack1111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᛵ"): scope,
                bstack1111_opy_ (u"ࠧࡺࡹࡱࡧࠥᛶ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᛷ"), None)):
                    bstack11ll111l1ll_opy_[bstack1111_opy_ (u"ࠢࡵࡻࡳࡩࠧᛸ")] = TestFramework.bstack1l11l1l1111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11ll111l1ll_opy_[bstack1111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ᛹")] = uuid4().__str__()
                bstack11ll111l1ll_opy_[PytestBDDFramework.bstack11ll1111111_opy_] = bstack11l1ll1lll1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11ll111l1ll_opy_[PytestBDDFramework.bstack11ll111l111_opy_] = bstack11l1ll1lll1_opy_
            if bstack11l1lll111l_opy_ in bstack11l1llll1ll_opy_:
                bstack11l1llll1ll_opy_[bstack11l1lll111l_opy_].update(bstack11ll111l1ll_opy_)
                self.logger.debug(bstack1111_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥ᛺") + str(bstack11l1llll1ll_opy_[bstack11l1lll111l_opy_]) + bstack1111_opy_ (u"ࠥࠦ᛻"))
            else:
                bstack11l1llll1ll_opy_[bstack11l1lll111l_opy_] = bstack11ll111l1ll_opy_
                self.logger.debug(bstack1111_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢ᛼") + str(len(bstack11l1llll1ll_opy_)) + bstack1111_opy_ (u"ࠧࠨ᛽"))
        TestFramework.bstack1lll1l11l1l_opy_(instance, PytestBDDFramework.bstack11ll1111lll_opy_, bstack11l1llll1ll_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᛾") + str(instance.ref()) + bstack1111_opy_ (u"ࠢࠣ᛿"))
        return instance
    def __11ll1l1ll11_opy_(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1llll1l1_opy_.create_context(target)
        ob = bstack1ll11ll111l_opy_(ctx, self.bstack1l1ll111l11_opy_, self.bstack11ll11l1l1l_opy_, test_framework_state)
        TestFramework.bstack11l1llll111_opy_(ob, {
            TestFramework.bstack1l1l1111l11_opy_: context.test_framework_name,
            TestFramework.bstack1l111llll11_opy_: context.test_framework_version,
            TestFramework.bstack11ll1l11lll_opy_: [],
            PytestBDDFramework.bstack11ll1111lll_opy_: {},
            PytestBDDFramework.bstack11ll11ll1ll_opy_: {},
            PytestBDDFramework.bstack11ll11lll11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1l11l1l_opy_(ob, TestFramework.bstack11l1llll11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l11l1l_opy_(ob, TestFramework.bstack1l1l11l1ll1_opy_, context.platform_index)
        TestFramework.bstack1lll1111lll_opy_[ctx.id] = ob
        self.logger.debug(bstack1111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᜀ") + str(TestFramework.bstack1lll1111lll_opy_.keys()) + bstack1111_opy_ (u"ࠤࠥᜁ"))
        return ob
    @staticmethod
    def __11l1ll1ll1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111_opy_ (u"ࠪ࡭ࡩ࠭ᜂ"): id(step),
                bstack1111_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᜃ"): step.name,
                bstack1111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ᜄ"): step.keyword,
            })
        meta = {
            bstack1111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᜅ"): {
                bstack1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᜆ"): feature.name,
                bstack1111_opy_ (u"ࠨࡲࡤࡸ࡭࠭ᜇ"): feature.filename,
                bstack1111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᜈ"): feature.description
            },
            bstack1111_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᜉ"): {
                bstack1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᜊ"): scenario.name
            },
            bstack1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᜋ"): steps,
            bstack1111_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᜌ"): PytestBDDFramework.__11ll11l11l1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11ll11l1ll1_opy_: meta
            }
        )
    def bstack11ll111llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᜍ")
        global _1l111l1l11l_opy_
        platform_index = os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᜎ")]
        bstack1l111l111l1_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), bstack11ll11l1lll_opy_)
        if not os.path.exists(bstack1l111l111l1_opy_) or not os.path.isdir(bstack1l111l111l1_opy_):
            return
        logs = hook.get(bstack1111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᜏ"), [])
        with os.scandir(bstack1l111l111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111l1l11l_opy_:
                    self.logger.info(bstack1111_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᜐ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111_opy_ (u"ࠦࠧᜑ")
                    log_entry = bstack1ll11lllll1_opy_(
                        kind=bstack1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᜒ"),
                        message=bstack1111_opy_ (u"ࠨࠢᜓ"),
                        level=bstack1111_opy_ (u"᜔ࠢࠣ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111l11ll1_opy_=entry.stat().st_size,
                        bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄ᜕ࠣ"),
                        bstack1llll_opy_=os.path.abspath(entry.path),
                        bstack11ll11l1111_opy_=hook.get(TestFramework.bstack11l1lll1l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111l1l11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᜖")]
        bstack11ll111ll1l_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), bstack11ll11l1lll_opy_, bstack11ll1l1llll_opy_)
        if not os.path.exists(bstack11ll111ll1l_opy_) or not os.path.isdir(bstack11ll111ll1l_opy_):
            self.logger.info(bstack1111_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧ᜗").format(bstack11ll111ll1l_opy_))
        else:
            self.logger.info(bstack1111_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥ᜘").format(bstack11ll111ll1l_opy_))
            with os.scandir(bstack11ll111ll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111l1l11l_opy_:
                        self.logger.info(bstack1111_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ᜙").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111_opy_ (u"ࠨࠢ᜚")
                        log_entry = bstack1ll11lllll1_opy_(
                            kind=bstack1111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᜛"),
                            message=bstack1111_opy_ (u"ࠣࠤ᜜"),
                            level=bstack1111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨ᜝"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111l11ll1_opy_=entry.stat().st_size,
                            bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥ᜞"),
                            bstack1llll_opy_=os.path.abspath(entry.path),
                            bstack1l111l1111l_opy_=hook.get(TestFramework.bstack11l1lll1l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111l1l11l_opy_.add(abs_path)
        hook[bstack1111_opy_ (u"ࠦࡱࡵࡧࡴࠤᜟ")] = logs
    def bstack1l11l1l1lll_opy_(
        self,
        bstack1l111ll11l1_opy_: bstack1ll11ll111l_opy_,
        entries: List[bstack1ll11lllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᜠ"))
        req.platform_index = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l11l1ll1_opy_)
        req.client_worker_id = bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᜡ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll11l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll11l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll11l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l1111l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l111llll11_opy_)
            log_entry.uuid = entry.bstack11ll11l1111_opy_ if entry.bstack11ll11l1111_opy_ else TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l11l1l1l_opy_)
            log_entry.test_framework_state = bstack1l111ll11l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᜢ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᜣ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111l11ll1_opy_
                log_entry.file_path = entry.bstack1llll_opy_
        def bstack1l111ll1111_opy_():
            bstack1l1llll111_opy_ = datetime.now()
            try:
                self.bstack1lll111l111_opy_.LogCreatedEvent(req)
                bstack1l111ll11l1_opy_.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᜤ"), datetime.now() - bstack1l1llll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᜥ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1lllll1l_opy_.enqueue(bstack1l111ll1111_opy_)
    def __11l1lllll11_opy_(self, instance) -> None:
        bstack1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᜦ")
        bstack11ll1l11ll1_opy_ = {bstack1111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᜧ"): bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()}
        TestFramework.bstack11l1llll111_opy_(instance, bstack11ll1l11ll1_opy_)
    @staticmethod
    def __11ll1l11111_opy_(instance, args):
        request, bstack11l1llllll1_opy_ = args
        bstack11ll1l1lll1_opy_ = id(bstack11l1llllll1_opy_)
        bstack11ll111l11l_opy_ = instance.data[TestFramework.bstack11ll11l1ll1_opy_]
        step = next(filter(lambda st: st[bstack1111_opy_ (u"࠭ࡩࡥࠩᜨ")] == bstack11ll1l1lll1_opy_, bstack11ll111l11l_opy_[bstack1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᜩ")]), None)
        step.update({
            bstack1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜪ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11ll111l11l_opy_[bstack1111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᜫ")]) if st[bstack1111_opy_ (u"ࠪ࡭ࡩ࠭ᜬ")] == step[bstack1111_opy_ (u"ࠫ࡮ࡪࠧᜭ")]), None)
        if index is not None:
            bstack11ll111l11l_opy_[bstack1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᜮ")][index] = step
        instance.data[TestFramework.bstack11ll11l1ll1_opy_] = bstack11ll111l11l_opy_
    @staticmethod
    def __11l1lll1l11_opy_(instance, args):
        bstack1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᜯ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11l1llllll1_opy_ = args[1]
        bstack11ll1l1lll1_opy_ = id(bstack11l1llllll1_opy_)
        bstack11ll111l11l_opy_ = instance.data[TestFramework.bstack11ll11l1ll1_opy_]
        step = None
        if bstack11ll1l1lll1_opy_ is not None and bstack11ll111l11l_opy_.get(bstack1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᜰ")):
            step = next(filter(lambda st: st[bstack1111_opy_ (u"ࠨ࡫ࡧࠫᜱ")] == bstack11ll1l1lll1_opy_, bstack11ll111l11l_opy_[bstack1111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᜲ")]), None)
            step.update({
                bstack1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜳ"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷ᜴ࠫ"): bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᜵"),
                bstack1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᜶"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᜷"): bstack1111_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ᜸"),
                })
        index = next((i for i, st in enumerate(bstack11ll111l11l_opy_[bstack1111_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᜹")]) if st[bstack1111_opy_ (u"ࠪ࡭ࡩ࠭᜺")] == step[bstack1111_opy_ (u"ࠫ࡮ࡪࠧ᜻")]), None)
        if index is not None:
            bstack11ll111l11l_opy_[bstack1111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᜼")][index] = step
        instance.data[TestFramework.bstack11ll11l1ll1_opy_] = bstack11ll111l11l_opy_
    @staticmethod
    def __11ll11l11l1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ᜽")):
                examples = list(node.callspec.params[bstack1111_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭᜾")].values())
            return examples
        except:
            return []
    def bstack1l11l11111l_opy_(self, instance: bstack1ll11ll111l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11l1l11_opy_ = (
            PytestBDDFramework.bstack11ll11l111l_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11ll1111l1l_opy_
        )
        hook = PytestBDDFramework.bstack11ll11lllll_opy_(instance, bstack11ll11l1l11_opy_)
        entries = hook.get(TestFramework.bstack11l1ll11l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, []))
        return entries
    def bstack1l11l11ll11_opy_(self, instance: bstack1ll11ll111l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11l1l11_opy_ = (
            PytestBDDFramework.bstack11ll11l111l_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11ll1111l1l_opy_
        )
        PytestBDDFramework.bstack11ll1l1l111_opy_(instance, bstack11ll11l1l11_opy_)
        TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, []).clear()
    @staticmethod
    def bstack11ll11lllll_opy_(instance: bstack1ll11ll111l_opy_, bstack11ll11l1l11_opy_: str):
        bstack11l1llll1l1_opy_ = (
            PytestBDDFramework.bstack11ll11ll1ll_opy_
            if bstack11ll11l1l11_opy_ == PytestBDDFramework.bstack11ll1111l1l_opy_
            else PytestBDDFramework.bstack11ll11lll11_opy_
        )
        bstack11l1ll1l11l_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11ll11l1l11_opy_, None)
        bstack11ll111ll11_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1llll1l1_opy_, None) if bstack11l1ll1l11l_opy_ else None
        return (
            bstack11ll111ll11_opy_[bstack11l1ll1l11l_opy_][-1]
            if isinstance(bstack11ll111ll11_opy_, dict) and len(bstack11ll111ll11_opy_.get(bstack11l1ll1l11l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll1l1l111_opy_(instance: bstack1ll11ll111l_opy_, bstack11ll11l1l11_opy_: str):
        hook = PytestBDDFramework.bstack11ll11lllll_opy_(instance, bstack11ll11l1l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll11l11_opy_, []).clear()
    @staticmethod
    def __11l1ll1llll_opy_(instance: bstack1ll11ll111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨ᜿"), None)):
            return
        if os.getenv(bstack1111_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᝀ"), bstack1111_opy_ (u"ࠥ࠵ࠧᝁ")) != bstack1111_opy_ (u"ࠦ࠶ࠨᝂ"):
            PytestBDDFramework.logger.warning(bstack1111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᝃ"))
            return
        bstack11ll1l111ll_opy_ = {
            bstack1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᝄ"): (PytestBDDFramework.bstack11ll11l111l_opy_, PytestBDDFramework.bstack11ll11lll11_opy_),
            bstack1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᝅ"): (PytestBDDFramework.bstack11ll1111l1l_opy_, PytestBDDFramework.bstack11ll11ll1ll_opy_),
        }
        for when in (bstack1111_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᝆ"), bstack1111_opy_ (u"ࠤࡦࡥࡱࡲࠢᝇ"), bstack1111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᝈ")):
            bstack11l1ll111l1_opy_ = args[1].get_records(when)
            if not bstack11l1ll111l1_opy_:
                continue
            records = [
                bstack1ll11lllll1_opy_(
                    kind=TestFramework.bstack1l111l1l1l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᝉ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᝊ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1ll111l1_opy_
                if isinstance(getattr(r, bstack1111_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᝋ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1ll111ll_opy_, bstack11l1llll1l1_opy_ = bstack11ll1l111ll_opy_.get(when, (None, None))
            bstack11ll111111l_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1ll111ll_opy_, None) if bstack11l1ll111ll_opy_ else None
            bstack11ll111ll11_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1llll1l1_opy_, None) if bstack11ll111111l_opy_ else None
            if isinstance(bstack11ll111ll11_opy_, dict) and len(bstack11ll111ll11_opy_.get(bstack11ll111111l_opy_, [])) > 0:
                hook = bstack11ll111ll11_opy_[bstack11ll111111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll11l11_opy_ in hook:
                    hook[TestFramework.bstack11l1ll11l11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll111l1l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l1ll11lll_opy_(request.node, scenario)
        bstack11l1lllll1l_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l1lllll1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l11l1l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1ll1l_opy_: test_id,
            TestFramework.bstack1l1l11lll11_opy_: test_name,
            TestFramework.bstack1l1111lll11_opy_: test_id,
            TestFramework.bstack11l1lll11l1_opy_: bstack11l1lllll1l_opy_,
            TestFramework.bstack11l1ll11l1l_opy_: PytestBDDFramework.__11l1lll1ll1_opy_(feature, scenario),
            TestFramework.bstack11ll111lll1_opy_: code,
            TestFramework.bstack11lllll111l_opy_: TestFramework.bstack11l1ll11ll1_opy_,
            TestFramework.bstack11ll1lll1l1_opy_: test_name
        }
    @staticmethod
    def __11l1ll11lll_opy_(node, scenario):
        if hasattr(node, bstack1111_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᝌ")):
            parts = node.nodeid.rsplit(bstack1111_opy_ (u"ࠣ࡝ࠥᝍ"))
            params = parts[-1]
            return bstack1111_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᝎ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l1lll1ll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᝏ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1111_opy_ (u"ࠫࡹࡧࡧࡴࠩᝐ")) else [])
    @staticmethod
    def __11ll1l11l11_opy_(location):
        return bstack1111_opy_ (u"ࠧࡀ࠺ࠣᝑ").join(filter(lambda x: isinstance(x, str), location))