# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll11111l_opy_ import bstack1l1ll1l1l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack111ll11l1_opy_ import bstack111lll11l11_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11l11ll_opy_,
    TestHookState,
    bstack1ll1ll1ll11_opy_,
    bstack111l1111ll_opy_,
)
import traceback
from bstack_utils.helper import bstack11lll1l1111_opy_
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l11l111lll_opy_ import bstack1l11lll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll11l11_opy_
bstack11ll11ll111_opy_ = bstack11lll1l1111_opy_()
bstack11lll111lll_opy_ = bstack1ll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᣨ")
bstack111llll1ll1_opy_ = bstack1ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᣩ")
bstack111llll1l11_opy_ = bstack1ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᣪ")
bstack111lll1ll11_opy_ = 1.0
_11ll11l1l11_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack111ll1l11l1_opy_ = bstack1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᣫ")
    bstack111ll11l1ll_opy_ = bstack1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᣬ")
    bstack111lll111l1_opy_ = bstack1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᣭ")
    bstack111llll1l1l_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᣮ")
    bstack111ll1l1lll_opy_ = bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᣯ")
    bstack111llll11ll_opy_: bool
    bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_  = None
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1ll1l_opy_: Dict[str, str],
        bstack1l1l111111l_opy_: List[str]=[bstack1ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᣰ")],
        bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_ = None,
        bstack1ll11ll11l_opy_=None
    ):
        super().__init__(bstack1l1l111111l_opy_, bstack1l11ll1ll1l_opy_, bstack1l1lll11ll1_opy_)
        self.bstack111llll11ll_opy_ = any(bstack1ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᣱ") in item.lower() for item in bstack1l1l111111l_opy_)
        self.bstack1ll11ll11l_opy_ = bstack1ll11ll11l_opy_
    def track_event(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_:
            bstack111lll11l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᣲ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠥࠦᣳ"))
            return
        if not self.bstack111llll11ll_opy_:
            self.logger.warning(bstack1ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᣴ") + str(str(self.bstack1l1l111111l_opy_)) + bstack1ll_opy_ (u"ࠧࠨᣵ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᣶") + str(kwargs) + bstack1ll_opy_ (u"ࠢࠣ᣷"))
            return
        instance = self.__111ll1l1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢ᣸") + str(args) + bstack1ll_opy_ (u"ࠤࠥ᣹"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_ and test_hook_state == TestHookState.PRE:
                bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1l1ll1ll11_opy_.value)
                name = str(EVENTS.bstack1l1ll1ll11_opy_.name)+bstack1ll_opy_ (u"ࠥ࠾ࠧ᣺")+str(test_framework_state.name)
                TestFramework.bstack11l1111l1l1_opy_(instance, name, bstack1lll1lll11_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣ᣻").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11l1ll11111_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111lll1l111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ᣼") + str(test_hook_state) + bstack1ll_opy_ (u"ࠨࠢ᣽"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1111111l_opy_(instance, args)
                    self.logger.debug(bstack1ll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ᣾") + str(test_hook_state) + bstack1ll_opy_ (u"ࠣࠤ᣿"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11lll111111_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11lll111111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᤀ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠥࠦᤁ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__111llll111l_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1111l111_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__111llll1lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll11ll1_opy_(instance, *args)
                self.__11l11111l11_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_:
                self.__111ll1ll11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᤂ") + str(instance.ref()) + bstack1ll_opy_ (u"ࠧࠨᤃ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111ll1ll1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1l1ll1ll11_opy_.name)+bstack1ll_opy_ (u"ࠨ࠺ࠣᤄ")+str(test_framework_state.name)
                bstack1lll1lll11_opy_ = TestFramework.bstack111ll1ll111_opy_(instance, name)
                bstack1l11l1ll11_opy_.end(EVENTS.bstack1l1ll1ll11_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᤅ"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᤆ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᤇ").format(e))
    def bstack11ll1l11lll_opy_(self):
        return self.bstack111llll11ll_opy_
    def bstack11ll1ll1l11_opy_(self):
        return False
    def __11l1111l1ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᤈ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11lll11llll_opy_(rep, [bstack1ll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᤉ"), bstack1ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᤊ"), bstack1ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᤋ"), bstack1ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᤌ"), bstack1ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᤍ"), bstack1ll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᤎ")])
        return None
    def __111lll11ll1_opy_(self, instance: bstack1l1l11l11ll_opy_, *args):
        result = self.__11l1111l1ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1lll_opy_ = None
        if result.get(bstack1ll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᤏ"), None) == bstack1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᤐ") and len(args) > 1 and getattr(args[1], bstack1ll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᤑ"), None) is not None:
            failure = [{bstack1ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᤒ"): [args[1].excinfo.exconly(), result.get(bstack1ll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᤓ"), None)]}]
            bstack1ll111l1lll_opy_ = bstack1ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᤔ") if bstack1ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᤕ") in getattr(args[1].excinfo, bstack1ll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᤖ"), bstack1ll_opy_ (u"ࠦࠧᤗ")) else bstack1ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᤘ")
        bstack111lll1l1l1_opy_ = result.get(bstack1ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᤙ"), TestFramework.bstack11l111ll111_opy_)
        if bstack111lll1l1l1_opy_ != TestFramework.bstack11l111ll111_opy_:
            TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack111lllllll1_opy_(instance, {
            TestFramework.bstack11l1ll11l11_opy_: failure,
            TestFramework.bstack111ll1l1l11_opy_: bstack1ll111l1lll_opy_,
            TestFramework.bstack11l1ll11lll_opy_: bstack111lll1l1l1_opy_,
        })
    def __111ll1l1ll1_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll11ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1ll111l_opy_ bstack111lll1l11l_opy_ this to be bstack1ll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᤚ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111ll1lll1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll_opy_ (u"ࠣࡰࡲࡨࡪࠨᤛ"), None), bstack1ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᤜ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll_opy_ (u"ࠥࡲࡴࡪࡥࠣᤝ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᤞ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll1lll1l_opy_(target) if target else None
        return instance
    def __111ll1ll11l_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l111111ll_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, PytestBDDFramework.bstack111ll11l1ll_opy_, {})
        if not key in bstack11l111111ll_opy_:
            bstack11l111111ll_opy_[key] = []
        bstack111lll1lll1_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, PytestBDDFramework.bstack111lll111l1_opy_, {})
        if not key in bstack111lll1lll1_opy_:
            bstack111lll1lll1_opy_[key] = []
        bstack111lll11111_opy_ = {
            PytestBDDFramework.bstack111ll11l1ll_opy_: bstack11l111111ll_opy_,
            PytestBDDFramework.bstack111lll111l1_opy_: bstack111lll1lll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll_opy_ (u"ࠧࡱࡥࡺࠤ᤟"): key,
                TestFramework.bstack111lllll111_opy_: uuid4().__str__(),
                TestFramework.bstack11l1111lll1_opy_: TestFramework.bstack11l1111ll1l_opy_,
                TestFramework.bstack11l11111ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l11ll_opy_: [],
                TestFramework.bstack111ll1llll1_opy_: hook_name,
                TestFramework.bstack11l111l1ll1_opy_: bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()
            }
            bstack11l111111ll_opy_[key].append(hook)
            bstack111lll11111_opy_[PytestBDDFramework.bstack111llll1l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111lll1llll_opy_ = bstack11l111111ll_opy_.get(key, [])
            hook = bstack111lll1llll_opy_.pop() if bstack111lll1llll_opy_ else None
            if hook:
                result = self.__11l1111l1ll_opy_(*args)
                if result:
                    bstack11l11111l1l_opy_ = result.get(bstack1ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᤠ"), TestFramework.bstack11l1111ll1l_opy_)
                    if bstack11l11111l1l_opy_ != TestFramework.bstack11l1111ll1l_opy_:
                        hook[TestFramework.bstack11l1111lll1_opy_] = bstack11l11111l1l_opy_
                hook[TestFramework.bstack111lllll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l111l1ll1_opy_] = bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()
                self.bstack111lll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111llll1111_opy_, [])
                self.bstack11lll1lll1_opy_(instance, logs)
                bstack111lll1lll1_opy_[key].append(hook)
                bstack111lll11111_opy_[PytestBDDFramework.bstack111ll1l1lll_opy_] = key
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᤡ") + str(bstack111lll1lll1_opy_) + bstack1ll_opy_ (u"ࠣࠤᤢ"))
    def __111ll11ll1l_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11lll11llll_opy_(args[0], [bstack1ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᤣ"), bstack1ll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᤤ"), bstack1ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᤥ"), bstack1ll_opy_ (u"ࠧ࡯ࡤࡴࠤᤦ"), bstack1ll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᤧ"), bstack1ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᤨ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᤩ")) else fixturedef.get(bstack1ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᤪ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᤫ")) else None
        node = request.node if hasattr(request, bstack1ll_opy_ (u"ࠦࡳࡵࡤࡦࠤ᤬")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᤭")) else None
        baseid = fixturedef.get(bstack1ll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨ᤮"), None) or bstack1ll_opy_ (u"ࠢࠣ᤯")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᤰ")):
            target = PytestBDDFramework.__11l11111lll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᤱ")) else None
            if target and not TestFramework.bstack1l1ll1lll1l_opy_(target):
                self.__111ll1lll1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᤲ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠦࠧᤳ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᤴ") + str(target) + bstack1ll_opy_ (u"ࠨࠢᤵ"))
            return None
        instance = TestFramework.bstack1l1ll1lll1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᤶ") + str(target) + bstack1ll_opy_ (u"ࠣࠤᤷ"))
            return None
        bstack111llllll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, PytestBDDFramework.bstack111ll1l11l1_opy_, {})
        if os.getenv(bstack1ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᤸ"), bstack1ll_opy_ (u"ࠥ࠵᤹ࠧ")) == bstack1ll_opy_ (u"ࠦ࠶ࠨ᤺"):
            bstack11l111l1111_opy_ = bstack1ll_opy_ (u"ࠧࡀ᤻ࠢ").join((scope, fixturename))
            bstack11l111l1l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack11l111l1lll_opy_ = {
                bstack1ll_opy_ (u"ࠨ࡫ࡦࡻࠥ᤼"): bstack11l111l1111_opy_,
                bstack1ll_opy_ (u"ࠢࡵࡣࡪࡷࠧ᤽"): PytestBDDFramework.__11l111l11l1_opy_(request.node, scenario),
                bstack1ll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤ᤾"): fixturedef,
                bstack1ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ᤿"): scope,
                bstack1ll_opy_ (u"ࠥࡸࡾࡶࡥࠣ᥀"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣ᥁"), None)):
                    bstack11l111l1lll_opy_[bstack1ll_opy_ (u"ࠧࡺࡹࡱࡧࠥ᥂")] = TestFramework.bstack11ll11ll1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l111l1lll_opy_[bstack1ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦ᥃")] = uuid4().__str__()
                bstack11l111l1lll_opy_[PytestBDDFramework.bstack11l11111ll1_opy_] = bstack11l111l1l1l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l111l1lll_opy_[PytestBDDFramework.bstack111lllll1ll_opy_] = bstack11l111l1l1l_opy_
            if bstack11l111l1111_opy_ in bstack111llllll11_opy_:
                bstack111llllll11_opy_[bstack11l111l1111_opy_].update(bstack11l111l1lll_opy_)
                self.logger.debug(bstack1ll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣ᥄") + str(bstack111llllll11_opy_[bstack11l111l1111_opy_]) + bstack1ll_opy_ (u"ࠣࠤ᥅"))
            else:
                bstack111llllll11_opy_[bstack11l111l1111_opy_] = bstack11l111l1lll_opy_
                self.logger.debug(bstack1ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧ᥆") + str(len(bstack111llllll11_opy_)) + bstack1ll_opy_ (u"ࠥࠦ᥇"))
        TestFramework.bstack1l1l1l1l_opy_(instance, PytestBDDFramework.bstack111ll1l11l1_opy_, bstack111llllll11_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦ᥈") + str(instance.ref()) + bstack1ll_opy_ (u"ࠧࠨ᥉"))
        return instance
    def __111ll1lll1l_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l11_opy_.create_context(target)
        ob = bstack1l1l11l11ll_opy_(ctx, self.bstack1l1l111111l_opy_, self.bstack1l11ll1ll1l_opy_, test_framework_state)
        TestFramework.bstack111lllllll1_opy_(ob, {
            TestFramework.bstack1l11111111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11ll_opy_: context.test_framework_version,
            TestFramework.bstack111ll11llll_opy_: [],
            PytestBDDFramework.bstack111ll1l11l1_opy_: {},
            PytestBDDFramework.bstack111lll111l1_opy_: {},
            PytestBDDFramework.bstack111ll11l1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l1l1l1l_opy_(ob, TestFramework.bstack111lll1ll1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l1l1l1l_opy_(ob, TestFramework.bstack1l1111l11l1_opy_, context.platform_index)
        TestFramework.bstack1l111l11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨ᥊") + str(TestFramework.bstack1l111l11l_opy_.keys()) + bstack1ll_opy_ (u"ࠢࠣ᥋"))
        return ob
    @staticmethod
    def __11l1111111l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll_opy_ (u"ࠨ࡫ࡧࠫ᥌"): id(step),
                bstack1ll_opy_ (u"ࠩࡷࡩࡽࡺࠧ᥍"): step.name,
                bstack1ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ᥎"): step.keyword,
            })
        meta = {
            bstack1ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬ᥏"): {
                bstack1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᥐ"): feature.name,
                bstack1ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᥑ"): feature.filename,
                bstack1ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᥒ"): feature.description
            },
            bstack1ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᥓ"): {
                bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᥔ"): scenario.name
            },
            bstack1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᥕ"): steps,
            bstack1ll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᥖ"): PytestBDDFramework.__111ll1lllll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack111ll1l11ll_opy_: meta
            }
        )
    def bstack111lll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᥗ")
        global _11ll11l1l11_opy_
        platform_index = os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᥘ")]
        bstack11ll11l1ll1_opy_ = os.path.join(bstack11ll11ll111_opy_, (bstack11lll111lll_opy_ + str(platform_index)), bstack111llll1ll1_opy_)
        if not os.path.exists(bstack11ll11l1ll1_opy_) or not os.path.isdir(bstack11ll11l1ll1_opy_):
            return
        logs = hook.get(bstack1ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᥙ"), [])
        with os.scandir(bstack11ll11l1ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll11l1l11_opy_:
                    self.logger.info(bstack1ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᥚ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll_opy_ (u"ࠤࠥᥛ")
                    log_entry = bstack111l1111ll_opy_(
                        kind=bstack1ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᥜ"),
                        message=bstack1ll_opy_ (u"ࠦࠧᥝ"),
                        level=bstack1ll_opy_ (u"ࠧࠨᥞ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1ll1111_opy_=entry.stat().st_size,
                        bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᥟ"),
                        bstack1ll11l1_opy_=os.path.abspath(entry.path),
                        bstack11l111l111l_opy_=hook.get(TestFramework.bstack111lllll111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll11l1l11_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᥠ")]
        bstack111lllll1l1_opy_ = os.path.join(bstack11ll11ll111_opy_, (bstack11lll111lll_opy_ + str(platform_index)), bstack111llll1ll1_opy_, bstack111llll1l11_opy_)
        if not os.path.exists(bstack111lllll1l1_opy_) or not os.path.isdir(bstack111lllll1l1_opy_):
            self.logger.info(bstack1ll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᥡ").format(bstack111lllll1l1_opy_))
        else:
            self.logger.info(bstack1ll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᥢ").format(bstack111lllll1l1_opy_))
            with os.scandir(bstack111lllll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll11l1l11_opy_:
                        self.logger.info(bstack1ll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᥣ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll_opy_ (u"ࠦࠧᥤ")
                        log_entry = bstack111l1111ll_opy_(
                            kind=bstack1ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᥥ"),
                            message=bstack1ll_opy_ (u"ࠨࠢᥦ"),
                            level=bstack1ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᥧ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1ll1111_opy_=entry.stat().st_size,
                            bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᥨ"),
                            bstack1ll11l1_opy_=os.path.abspath(entry.path),
                            bstack11lll1l11l1_opy_=hook.get(TestFramework.bstack111lllll111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll11l1l11_opy_.add(abs_path)
        hook[bstack1ll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᥩ")] = logs
    def bstack11lll1lll1_opy_(
        self,
        bstack111111l1l1_opy_: bstack1l1l11l11ll_opy_,
        entries: List[bstack111l1111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᥪ"))
        req.platform_index = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l1111l11l1_opy_)
        req.client_worker_id = bstack1ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᥫ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack111111l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack111111l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack111111l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack11ll11l11ll_opy_)
            log_entry.uuid = entry.bstack11l111l111l_opy_ if entry.bstack11l111l111l_opy_ else TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l1111ll1l1_opy_)
            log_entry.test_framework_state = bstack111111l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᥬ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᥭ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1ll1111_opy_
                log_entry.file_path = entry.bstack1ll11l1_opy_
        def bstack11ll1l111l1_opy_():
            bstack1l1111ll_opy_ = datetime.now()
            try:
                self.bstack1ll11ll11l_opy_.LogCreatedEvent(req)
                bstack111111l1l1_opy_.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ᥮"), datetime.now() - bstack1l1111ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ᥯").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11ll1_opy_.enqueue(bstack11ll1l111l1_opy_)
    def __11l11111l11_opy_(self, instance) -> None:
        bstack1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᥰ")
        bstack111lll11111_opy_ = {bstack1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᥱ"): bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()}
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        bstack1l11lll1lll_opy_.bstack111llll11l1_opy_()
    @staticmethod
    def __111llll111l_opy_(instance, args):
        request, bstack111ll11lll1_opy_ = args
        bstack111lllll11l_opy_ = id(bstack111ll11lll1_opy_)
        bstack111ll1lll11_opy_ = instance.data[TestFramework.bstack111ll1l11ll_opy_]
        step = next(filter(lambda st: st[bstack1ll_opy_ (u"ࠫ࡮ࡪࠧᥲ")] == bstack111lllll11l_opy_, bstack111ll1lll11_opy_[bstack1ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᥳ")]), None)
        step.update({
            bstack1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᥴ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack111ll1lll11_opy_[bstack1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᥵")]) if st[bstack1ll_opy_ (u"ࠨ࡫ࡧࠫ᥶")] == step[bstack1ll_opy_ (u"ࠩ࡬ࡨࠬ᥷")]), None)
        if index is not None:
            bstack111ll1lll11_opy_[bstack1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᥸")][index] = step
        instance.data[TestFramework.bstack111ll1l11ll_opy_] = bstack111ll1lll11_opy_
    @staticmethod
    def __11l1111l111_opy_(instance, args):
        bstack1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᥹")
        bstack1ll1ll11l1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111ll11lll1_opy_ = args[1]
        bstack111lllll11l_opy_ = id(bstack111ll11lll1_opy_)
        bstack111ll1lll11_opy_ = instance.data[TestFramework.bstack111ll1l11ll_opy_]
        step = None
        if bstack111lllll11l_opy_ is not None and bstack111ll1lll11_opy_.get(bstack1ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᥺")):
            step = next(filter(lambda st: st[bstack1ll_opy_ (u"࠭ࡩࡥࠩ᥻")] == bstack111lllll11l_opy_, bstack111ll1lll11_opy_[bstack1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᥼")]), None)
            step.update({
                bstack1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᥽"): bstack1ll1ll11l1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᥾"): bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᥿"),
                bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᦀ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᦁ"): bstack1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᦂ"),
                })
        index = next((i for i, st in enumerate(bstack111ll1lll11_opy_[bstack1ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᦃ")]) if st[bstack1ll_opy_ (u"ࠨ࡫ࡧࠫᦄ")] == step[bstack1ll_opy_ (u"ࠩ࡬ࡨࠬᦅ")]), None)
        if index is not None:
            bstack111ll1lll11_opy_[bstack1ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᦆ")][index] = step
        instance.data[TestFramework.bstack111ll1l11ll_opy_] = bstack111ll1lll11_opy_
    @staticmethod
    def __111ll1lllll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᦇ")):
                examples = list(node.callspec.params[bstack1ll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᦈ")].values())
            return examples
        except:
            return []
    def bstack11ll11llll1_opy_(self, instance: bstack1l1l11l11ll_opy_, bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            PytestBDDFramework.bstack111llll1l1l_opy_
            if bstack1l1ll1lll11_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111ll1l1lll_opy_
        )
        hook = PytestBDDFramework.bstack111lll1111l_opy_(instance, bstack11l11111111_opy_)
        entries = hook.get(TestFramework.bstack11l111l11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, []))
        return entries
    def bstack11ll1l1lll1_opy_(self, instance: bstack1l1l11l11ll_opy_, bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            PytestBDDFramework.bstack111llll1l1l_opy_
            if bstack1l1ll1lll11_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111ll1l1lll_opy_
        )
        PytestBDDFramework.bstack11l1111llll_opy_(instance, bstack11l11111111_opy_)
        TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, []).clear()
    @staticmethod
    def bstack111lll1111l_opy_(instance: bstack1l1l11l11ll_opy_, bstack11l11111111_opy_: str):
        bstack111lll1l1ll_opy_ = (
            PytestBDDFramework.bstack111lll111l1_opy_
            if bstack11l11111111_opy_ == PytestBDDFramework.bstack111ll1l1lll_opy_
            else PytestBDDFramework.bstack111ll11l1ll_opy_
        )
        bstack111ll1l1111_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack11l11111111_opy_, None)
        bstack111ll11ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll1l1ll_opy_, None) if bstack111ll1l1111_opy_ else None
        return (
            bstack111ll11ll11_opy_[bstack111ll1l1111_opy_][-1]
            if isinstance(bstack111ll11ll11_opy_, dict) and len(bstack111ll11ll11_opy_.get(bstack111ll1l1111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111llll_opy_(instance: bstack1l1l11l11ll_opy_, bstack11l11111111_opy_: str):
        hook = PytestBDDFramework.bstack111lll1111l_opy_(instance, bstack11l11111111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l111l11ll_opy_, []).clear()
    @staticmethod
    def __111llll1lll_opy_(instance: bstack1l1l11l11ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᦉ"), None)):
            return
        if os.getenv(bstack1ll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᦊ"), bstack1ll_opy_ (u"ࠣ࠳ࠥᦋ")) != bstack1ll_opy_ (u"ࠤ࠴ࠦᦌ"):
            PytestBDDFramework.logger.warning(bstack1ll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᦍ"))
            return
        bstack111lll11lll_opy_ = {
            bstack1ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᦎ"): (PytestBDDFramework.bstack111llll1l1l_opy_, PytestBDDFramework.bstack111ll11l1ll_opy_),
            bstack1ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᦏ"): (PytestBDDFramework.bstack111ll1l1lll_opy_, PytestBDDFramework.bstack111lll111l1_opy_),
        }
        for when in (bstack1ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᦐ"), bstack1ll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᦑ"), bstack1ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᦒ")):
            bstack111ll1l111l_opy_ = args[1].get_records(when)
            if not bstack111ll1l111l_opy_:
                continue
            records = [
                bstack111l1111ll_opy_(
                    kind=TestFramework.bstack11ll11ll11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᦓ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᦔ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll1l111l_opy_
                if isinstance(getattr(r, bstack1ll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᦕ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111lll11l1l_opy_, bstack111lll1l1ll_opy_ = bstack111lll11lll_opy_.get(when, (None, None))
            bstack11l1111ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll11l1l_opy_, None) if bstack111lll11l1l_opy_ else None
            bstack111ll11ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll1l1ll_opy_, None) if bstack11l1111ll11_opy_ else None
            if isinstance(bstack111ll11ll11_opy_, dict) and len(bstack111ll11ll11_opy_.get(bstack11l1111ll11_opy_, [])) > 0:
                hook = bstack111ll11ll11_opy_[bstack11l1111ll11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l111l11ll_opy_ in hook:
                    hook[TestFramework.bstack11l111l11ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll1l111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l1111l11l_opy_(request.node, scenario)
        bstack111llllll1l_opy_ = feature.filename
        if not test_id or not test_name or not bstack111llllll1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1111ll1l1_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll11111_opy_: test_id,
            TestFramework.bstack1l111111lll_opy_: test_name,
            TestFramework.bstack11ll111l1ll_opy_: test_id,
            TestFramework.bstack111llllllll_opy_: bstack111llllll1l_opy_,
            TestFramework.bstack11l111l1l11_opy_: PytestBDDFramework.__11l111l11l1_opy_(feature, scenario),
            TestFramework.bstack111ll1ll1ll_opy_: code,
            TestFramework.bstack11l1ll11lll_opy_: TestFramework.bstack11l111ll111_opy_,
            TestFramework.bstack11l11l1l1ll_opy_: test_name
        }
    @staticmethod
    def __11l1111l11l_opy_(node, scenario):
        if hasattr(node, bstack1ll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᦖ")):
            parts = node.nodeid.rsplit(bstack1ll_opy_ (u"ࠨ࡛ࠣᦗ"))
            params = parts[-1]
            return bstack1ll_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᦘ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l111l11l1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᦙ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᦚ")) else [])
    @staticmethod
    def __11l11111lll_opy_(location):
        return bstack1ll_opy_ (u"ࠥ࠾࠿ࠨᦛ").join(filter(lambda x: isinstance(x, str), location))