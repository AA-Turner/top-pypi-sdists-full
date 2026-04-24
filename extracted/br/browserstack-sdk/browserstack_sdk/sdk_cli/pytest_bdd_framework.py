# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1l1ll1l1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11lll1_opy_ import bstack111lll1111l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l111llll11_opy_,
    TestHookState,
    bstack1lll111l1l1_opy_,
    bstack1llll111ll_opy_,
)
import traceback
from bstack_utils.helper import bstack11ll1lll1ll_opy_
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l11lllllll_opy_ import bstack1l1l111111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll11l11_opy_
bstack11ll11ll1l1_opy_ = bstack11ll1lll1ll_opy_()
bstack11lll1l1111_opy_ = bstack111ll11_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᤁ")
bstack111ll11l1l1_opy_ = bstack111ll11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᤂ")
bstack111ll1l111l_opy_ = bstack111ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᤃ")
bstack111lllll1l1_opy_ = 1.0
_11ll1l11111_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack111lll11111_opy_ = bstack111ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᤄ")
    bstack111ll1ll111_opy_ = bstack111ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᤅ")
    bstack11l111111l1_opy_ = bstack111ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᤆ")
    bstack111ll1llll1_opy_ = bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᤇ")
    bstack111lll1l1l1_opy_ = bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᤈ")
    bstack111llllllll_opy_: bool
    bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_  = None
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1111l_opy_: Dict[str, str],
        bstack1l11lll1ll1_opy_: List[str]=[bstack111ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᤉ")],
        bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_ = None,
        bstack1l1l1l1l1l_opy_=None
    ):
        super().__init__(bstack1l11lll1ll1_opy_, bstack1l11ll1111l_opy_, bstack1l1lll11l1l_opy_)
        self.bstack111llllllll_opy_ = any(bstack111ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᤊ") in item.lower() for item in bstack1l11lll1ll1_opy_)
        self.bstack1l1l1l1l1l_opy_ = bstack1l1l1l1l1l_opy_
    def track_event(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_:
            bstack111lll1111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111ll11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᤋ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠢࠣᤌ"))
            return
        if not self.bstack111llllllll_opy_:
            self.logger.warning(bstack111ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᤍ") + str(str(self.bstack1l11lll1ll1_opy_)) + bstack111ll11_opy_ (u"ࠤࠥᤎ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᤏ") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧᤐ"))
            return
        instance = self.__111lll1l11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᤑ") + str(args) + bstack111ll11_opy_ (u"ࠨࠢᤒ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_ and test_hook_state == TestHookState.PRE:
                bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack1l111l111_opy_.value)
                name = str(EVENTS.bstack1l111l111_opy_.name)+bstack111ll11_opy_ (u"ࠢ࠻ࠤᤓ")+str(test_framework_state.name)
                TestFramework.bstack11l1111ll11_opy_(instance, name, bstack11111l11ll_opy_)
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᤔ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11l1l1l1l1l_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111lll1lll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack111ll11_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᤕ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠥࠦᤖ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11ll1l111l1_opy_):
                    TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11ll1l111l1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l11111111_opy_(instance, args)
                    self.logger.debug(bstack111ll11_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᤗ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠧࠨᤘ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11ll1l11l11_opy_):
                    TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11ll1l11l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᤙ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠢࠣᤚ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l11111lll_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__111ll1l11l1_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__111llll111l_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111ll11lll1_opy_(instance, *args)
                self.__111llll1l11_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_:
                self.__11l111l111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᤛ") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠤࠥᤜ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1111llll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111ll1l1l1l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1l111l111_opy_.name)+bstack111ll11_opy_ (u"ࠥ࠾ࠧᤝ")+str(test_framework_state.name)
                bstack11111l11ll_opy_ = TestFramework.bstack111ll1l1111_opy_(instance, name)
                bstack1ll1l11l1_opy_.end(EVENTS.bstack1l111l111_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᤞ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᤟"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᤠ").format(e))
    def bstack11ll1lll111_opy_(self):
        return self.bstack111llllllll_opy_
    def bstack11ll111llll_opy_(self):
        return False
    def __111ll1ll1l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111ll11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᤡ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11ll11ll11l_opy_(rep, [bstack111ll11_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᤢ"), bstack111ll11_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᤣ"), bstack111ll11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᤤ"), bstack111ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᤥ"), bstack111ll11_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᤦ"), bstack111ll11_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᤧ")])
        return None
    def __111ll11lll1_opy_(self, instance: bstack1l111llll11_opy_, *args):
        result = self.__111ll1ll1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        if result.get(bstack111ll11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᤨ"), None) == bstack111ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᤩ") and len(args) > 1 and getattr(args[1], bstack111ll11_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᤪ"), None) is not None:
            failure = [{bstack111ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᤫ"): [args[1].excinfo.exconly(), result.get(bstack111ll11_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥ᤬"), None)]}]
            bstack1ll111l1l1l_opy_ = bstack111ll11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ᤭") if bstack111ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ᤮") in getattr(args[1].excinfo, bstack111ll11_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤ᤯"), bstack111ll11_opy_ (u"ࠣࠤᤰ")) else bstack111ll11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᤱ")
        bstack111ll11ll1l_opy_ = result.get(bstack111ll11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᤲ"), TestFramework.bstack111ll11llll_opy_)
        if bstack111ll11ll1l_opy_ != TestFramework.bstack111ll11llll_opy_:
            TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11lll1l11l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l111l11ll_opy_(instance, {
            TestFramework.bstack11l1ll111ll_opy_: failure,
            TestFramework.bstack111lll1llll_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack11l1ll11111_opy_: bstack111ll11ll1l_opy_,
        })
    def __111lll1l11l_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111llllll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll11l111l_opy_ bstack111lll1l111_opy_ this to be bstack111ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᤳ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111lll1ll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᤴ"), None), bstack111ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᤵ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111ll11_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᤶ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack111ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᤷ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll111l11_opy_(target) if target else None
        return instance
    def __11l111l111l_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l11111l1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, PytestBDDFramework.bstack111ll1ll111_opy_, {})
        if not key in bstack11l11111l1l_opy_:
            bstack11l11111l1l_opy_[key] = []
        bstack111ll1lll1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, PytestBDDFramework.bstack11l111111l1_opy_, {})
        if not key in bstack111ll1lll1l_opy_:
            bstack111ll1lll1l_opy_[key] = []
        bstack111lll1ll1l_opy_ = {
            PytestBDDFramework.bstack111ll1ll111_opy_: bstack11l11111l1l_opy_,
            PytestBDDFramework.bstack11l111111l1_opy_: bstack111ll1lll1l_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack111ll11_opy_ (u"ࠤ࡮ࡩࡾࠨᤸ"): key,
                TestFramework.bstack11l11111l11_opy_: uuid4().__str__(),
                TestFramework.bstack111lll11ll1_opy_: TestFramework.bstack111ll11l1ll_opy_,
                TestFramework.bstack111ll1l1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l1111_opy_: [],
                TestFramework.bstack11l11111ll1_opy_: hook_name,
                TestFramework.bstack111ll1ll11l_opy_: bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()
            }
            bstack11l11111l1l_opy_[key].append(hook)
            bstack111lll1ll1l_opy_[PytestBDDFramework.bstack111ll1llll1_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llllll1l_opy_ = bstack11l11111l1l_opy_.get(key, [])
            hook = bstack111llllll1l_opy_.pop() if bstack111llllll1l_opy_ else None
            if hook:
                result = self.__111ll1ll1l1_opy_(*args)
                if result:
                    bstack11l111111ll_opy_ = result.get(bstack111ll11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨ᤹ࠦ"), TestFramework.bstack111ll11l1ll_opy_)
                    if bstack11l111111ll_opy_ != TestFramework.bstack111ll11l1ll_opy_:
                        hook[TestFramework.bstack111lll11ll1_opy_] = bstack11l111111ll_opy_
                hook[TestFramework.bstack111llll1lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111ll1ll11l_opy_] = bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()
                self.bstack111llll11ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll1lll11_opy_, [])
                self.bstack11l1ll11_opy_(instance, logs)
                bstack111ll1lll1l_opy_[key].append(hook)
                bstack111lll1ll1l_opy_[PytestBDDFramework.bstack111lll1l1l1_opy_] = key
        TestFramework.bstack11l111l11ll_opy_(instance, bstack111lll1ll1l_opy_)
        self.logger.debug(bstack111ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥ᤺") + str(bstack111ll1lll1l_opy_) + bstack111ll11_opy_ (u"ࠧࠨ᤻"))
    def __111llllll11_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11ll11ll11l_opy_(args[0], [bstack111ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ᤼"), bstack111ll11_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣ᤽"), bstack111ll11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣ᤾"), bstack111ll11_opy_ (u"ࠤ࡬ࡨࡸࠨ᤿"), bstack111ll11_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧ᥀"), bstack111ll11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦ᥁")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack111ll11_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦ᥂")) else fixturedef.get(bstack111ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ᥃"), None)
        fixturename = request.fixturename if hasattr(request, bstack111ll11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧ᥄")) else None
        node = request.node if hasattr(request, bstack111ll11_opy_ (u"ࠣࡰࡲࡨࡪࠨ᥅")) else None
        target = request.node.nodeid if hasattr(node, bstack111ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᥆")) else None
        baseid = fixturedef.get(bstack111ll11_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥ᥇"), None) or bstack111ll11_opy_ (u"ࠦࠧ᥈")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111ll11_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥ᥉")):
            target = PytestBDDFramework.__11l1111lll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111ll11_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣ᥊")) else None
            if target and not TestFramework.bstack1l1ll111l11_opy_(target):
                self.__111lll1ll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111ll11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᥋") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠣࠤ᥌"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢ᥍") + str(target) + bstack111ll11_opy_ (u"ࠥࠦ᥎"))
            return None
        instance = TestFramework.bstack1l1ll111l11_opy_(target)
        if not instance:
            self.logger.warning(bstack111ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨ᥏") + str(target) + bstack111ll11_opy_ (u"ࠧࠨᥐ"))
            return None
        bstack111lll111l1_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, PytestBDDFramework.bstack111lll11111_opy_, {})
        if os.getenv(bstack111ll11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᥑ"), bstack111ll11_opy_ (u"ࠢ࠲ࠤᥒ")) == bstack111ll11_opy_ (u"ࠣ࠳ࠥᥓ"):
            bstack11l1111l11l_opy_ = bstack111ll11_opy_ (u"ࠤ࠽ࠦᥔ").join((scope, fixturename))
            bstack111ll11l11l_opy_ = datetime.now(tz=timezone.utc)
            bstack111llll11l1_opy_ = {
                bstack111ll11_opy_ (u"ࠥ࡯ࡪࡿࠢᥕ"): bstack11l1111l11l_opy_,
                bstack111ll11_opy_ (u"ࠦࡹࡧࡧࡴࠤᥖ"): PytestBDDFramework.__111lll1l1ll_opy_(request.node, scenario),
                bstack111ll11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᥗ"): fixturedef,
                bstack111ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᥘ"): scope,
                bstack111ll11_opy_ (u"ࠢࡵࡻࡳࡩࠧᥙ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack111ll11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᥚ"), None)):
                    bstack111llll11l1_opy_[bstack111ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᥛ")] = TestFramework.bstack11ll11lllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111llll11l1_opy_[bstack111ll11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᥜ")] = uuid4().__str__()
                bstack111llll11l1_opy_[PytestBDDFramework.bstack111ll1l1ll1_opy_] = bstack111ll11l11l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111llll11l1_opy_[PytestBDDFramework.bstack111llll1lll_opy_] = bstack111ll11l11l_opy_
            if bstack11l1111l11l_opy_ in bstack111lll111l1_opy_:
                bstack111lll111l1_opy_[bstack11l1111l11l_opy_].update(bstack111llll11l1_opy_)
                self.logger.debug(bstack111ll11_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᥝ") + str(bstack111lll111l1_opy_[bstack11l1111l11l_opy_]) + bstack111ll11_opy_ (u"ࠧࠨᥞ"))
            else:
                bstack111lll111l1_opy_[bstack11l1111l11l_opy_] = bstack111llll11l1_opy_
                self.logger.debug(bstack111ll11_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᥟ") + str(len(bstack111lll111l1_opy_)) + bstack111ll11_opy_ (u"ࠢࠣᥠ"))
        TestFramework.bstack11l1ll11ll_opy_(instance, PytestBDDFramework.bstack111lll11111_opy_, bstack111lll111l1_opy_)
        self.logger.debug(bstack111ll11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᥡ") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠤࠥᥢ"))
        return instance
    def __111lll1ll11_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        ob = bstack1l111llll11_opy_(ctx, self.bstack1l11lll1ll1_opy_, self.bstack1l11ll1111l_opy_, test_framework_state)
        TestFramework.bstack11l111l11ll_opy_(ob, {
            TestFramework.bstack1l111ll11ll_opy_: context.test_framework_name,
            TestFramework.bstack11lll11111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1111ll1l_opy_: [],
            PytestBDDFramework.bstack111lll11111_opy_: {},
            PytestBDDFramework.bstack11l111111l1_opy_: {},
            PytestBDDFramework.bstack111ll1ll111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11l1ll11ll_opy_(ob, TestFramework.bstack111ll1l11ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11l1ll11ll_opy_(ob, TestFramework.bstack11llllll1ll_opy_, context.platform_index)
        TestFramework.bstack1111l11ll_opy_[ctx.id] = ob
        self.logger.debug(bstack111ll11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᥣ") + str(TestFramework.bstack1111l11ll_opy_.keys()) + bstack111ll11_opy_ (u"ࠦࠧᥤ"))
        return ob
    @staticmethod
    def __11l11111111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111ll11_opy_ (u"ࠬ࡯ࡤࠨᥥ"): id(step),
                bstack111ll11_opy_ (u"࠭ࡴࡦࡺࡷࠫᥦ"): step.name,
                bstack111ll11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᥧ"): step.keyword,
            })
        meta = {
            bstack111ll11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᥨ"): {
                bstack111ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᥩ"): feature.name,
                bstack111ll11_opy_ (u"ࠪࡴࡦࡺࡨࠨᥪ"): feature.filename,
                bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᥫ"): feature.description
            },
            bstack111ll11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᥬ"): {
                bstack111ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᥭ"): scenario.name
            },
            bstack111ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᥮"): steps,
            bstack111ll11_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪ᥯"): PytestBDDFramework.__111lllll111_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l111l1ll1_opy_: meta
            }
        )
    def bstack111llll11ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᥰ")
        global _11ll1l11111_opy_
        platform_index = os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᥱ")]
        bstack11lll11l1ll_opy_ = os.path.join(bstack11ll11ll1l1_opy_, (bstack11lll1l1111_opy_ + str(platform_index)), bstack111ll11l1l1_opy_)
        if not os.path.exists(bstack11lll11l1ll_opy_) or not os.path.isdir(bstack11lll11l1ll_opy_):
            return
        logs = hook.get(bstack111ll11_opy_ (u"ࠦࡱࡵࡧࡴࠤᥲ"), [])
        with os.scandir(bstack11lll11l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1l11111_opy_:
                    self.logger.info(bstack111ll11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᥳ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111ll11_opy_ (u"ࠨࠢᥴ")
                    log_entry = bstack1llll111ll_opy_(
                        kind=bstack111ll11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᥵"),
                        message=bstack111ll11_opy_ (u"ࠣࠤ᥶"),
                        level=bstack111ll11_opy_ (u"ࠤࠥ᥷"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1l1l1ll_opy_=entry.stat().st_size,
                        bstack11ll1ll1l1l_opy_=bstack111ll11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥ᥸"),
                        bstack1l11l11_opy_=os.path.abspath(entry.path),
                        bstack11l1111l1l1_opy_=hook.get(TestFramework.bstack11l11111l11_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1l11111_opy_.add(abs_path)
        platform_index = os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᥹")]
        bstack111llll1ll1_opy_ = os.path.join(bstack11ll11ll1l1_opy_, (bstack11lll1l1111_opy_ + str(platform_index)), bstack111ll11l1l1_opy_, bstack111ll1l111l_opy_)
        if not os.path.exists(bstack111llll1ll1_opy_) or not os.path.isdir(bstack111llll1ll1_opy_):
            self.logger.info(bstack111ll11_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢ᥺").format(bstack111llll1ll1_opy_))
        else:
            self.logger.info(bstack111ll11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧ᥻").format(bstack111llll1ll1_opy_))
            with os.scandir(bstack111llll1ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1l11111_opy_:
                        self.logger.info(bstack111ll11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧ᥼").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111ll11_opy_ (u"ࠣࠤ᥽")
                        log_entry = bstack1llll111ll_opy_(
                            kind=bstack111ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᥾"),
                            message=bstack111ll11_opy_ (u"ࠥࠦ᥿"),
                            level=bstack111ll11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᦀ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1l1l1ll_opy_=entry.stat().st_size,
                            bstack11ll1ll1l1l_opy_=bstack111ll11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᦁ"),
                            bstack1l11l11_opy_=os.path.abspath(entry.path),
                            bstack11ll111l1l1_opy_=hook.get(TestFramework.bstack11l11111l11_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1l11111_opy_.add(abs_path)
        hook[bstack111ll11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᦂ")] = logs
    def bstack11l1ll11_opy_(
        self,
        bstack1l1l1l11l_opy_: bstack1l111llll11_opy_,
        entries: List[bstack1llll111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᦃ"))
        req.platform_index = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack11llllll1ll_opy_)
        req.client_worker_id = bstack111ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᦄ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1l1l11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack1l111ll11ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack11lll11111l_opy_)
            log_entry.uuid = entry.bstack11l1111l1l1_opy_ if entry.bstack11l1111l1l1_opy_ else TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack1l111l1ll1l_opy_)
            log_entry.test_framework_state = bstack1l1l1l11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack111ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᦅ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᦆ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1l1l1ll_opy_
                log_entry.file_path = entry.bstack1l11l11_opy_
        def bstack11ll11l11l1_opy_():
            bstack111l1lllll_opy_ = datetime.now()
            try:
                self.bstack1l1l1l1l1l_opy_.LogCreatedEvent(req)
                bstack1l1l1l11l_opy_.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᦇ"), datetime.now() - bstack111l1lllll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᦈ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11l11l1_opy_)
    def __111llll1l11_opy_(self, instance) -> None:
        bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᦉ")
        bstack111lll1ll1l_opy_ = {bstack111ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᦊ"): bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()}
        TestFramework.bstack11l111l11ll_opy_(instance, bstack111lll1ll1l_opy_)
        bstack1l1l111111l_opy_.bstack111lll11lll_opy_()
    @staticmethod
    def __11l11111lll_opy_(instance, args):
        request, bstack111lllllll1_opy_ = args
        bstack11l111l11l1_opy_ = id(bstack111lllllll1_opy_)
        bstack111ll1lllll_opy_ = instance.data[TestFramework.bstack11l111l1ll1_opy_]
        step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠨ࡫ࡧࠫᦋ")] == bstack11l111l11l1_opy_, bstack111ll1lllll_opy_[bstack111ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᦌ")]), None)
        step.update({
            bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᦍ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack111ll1lllll_opy_[bstack111ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᦎ")]) if st[bstack111ll11_opy_ (u"ࠬ࡯ࡤࠨᦏ")] == step[bstack111ll11_opy_ (u"࠭ࡩࡥࠩᦐ")]), None)
        if index is not None:
            bstack111ll1lllll_opy_[bstack111ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᦑ")][index] = step
        instance.data[TestFramework.bstack11l111l1ll1_opy_] = bstack111ll1lllll_opy_
    @staticmethod
    def __111ll1l11l1_opy_(instance, args):
        bstack111ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡽࡨࡦࡰࠣࡰࡪࡴࠠࡢࡴࡪࡷࠥ࡯ࡳࠡ࠴࠯ࠤ࡮ࡺࠠࡴ࡫ࡪࡲ࡮࡬ࡩࡦࡵࠣࡸ࡭࡫ࡲࡦࠢ࡬ࡷࠥࡴ࡯ࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠲࡛ࠦࡳࡧࡴࡹࡪࡹࡴ࠭ࠢࡶࡸࡪࡶ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠴ࠢࡷ࡬ࡪࡴࠠࡵࡪࡨࠤࡱࡧࡳࡵࠢࡹࡥࡱࡻࡥࠡ࡫ࡶࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᦒ")
        bstack1ll1llll111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111lllllll1_opy_ = args[1]
        bstack11l111l11l1_opy_ = id(bstack111lllllll1_opy_)
        bstack111ll1lllll_opy_ = instance.data[TestFramework.bstack11l111l1ll1_opy_]
        step = None
        if bstack11l111l11l1_opy_ is not None and bstack111ll1lllll_opy_.get(bstack111ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᦓ")):
            step = next(filter(lambda st: st[bstack111ll11_opy_ (u"ࠪ࡭ࡩ࠭ᦔ")] == bstack11l111l11l1_opy_, bstack111ll1lllll_opy_[bstack111ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᦕ")]), None)
            step.update({
                bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᦖ"): bstack1ll1llll111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack111ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᦗ"): bstack111ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᦘ"),
                bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᦙ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack111ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᦚ"): bstack111ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᦛ"),
                })
        index = next((i for i, st in enumerate(bstack111ll1lllll_opy_[bstack111ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᦜ")]) if st[bstack111ll11_opy_ (u"ࠬ࡯ࡤࠨᦝ")] == step[bstack111ll11_opy_ (u"࠭ࡩࡥࠩᦞ")]), None)
        if index is not None:
            bstack111ll1lllll_opy_[bstack111ll11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᦟ")][index] = step
        instance.data[TestFramework.bstack11l111l1ll1_opy_] = bstack111ll1lllll_opy_
    @staticmethod
    def __111lllll111_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack111ll11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᦠ")):
                examples = list(node.callspec.params[bstack111ll11_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᦡ")].values())
            return examples
        except:
            return []
    def bstack11ll1ll11l1_opy_(self, instance: bstack1l111llll11_opy_, bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            PytestBDDFramework.bstack111ll1llll1_opy_
            if bstack1l1ll11l11l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111lll1l1l1_opy_
        )
        hook = PytestBDDFramework.bstack111llll1111_opy_(instance, bstack111lll11l11_opy_)
        entries = hook.get(TestFramework.bstack11l111l1111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, []))
        return entries
    def bstack11lll1l111l_opy_(self, instance: bstack1l111llll11_opy_, bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            PytestBDDFramework.bstack111ll1llll1_opy_
            if bstack1l1ll11l11l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111lll1l1l1_opy_
        )
        PytestBDDFramework.bstack11l1111111l_opy_(instance, bstack111lll11l11_opy_)
        TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, []).clear()
    @staticmethod
    def bstack111llll1111_opy_(instance: bstack1l111llll11_opy_, bstack111lll11l11_opy_: str):
        bstack111llll1l1l_opy_ = (
            PytestBDDFramework.bstack11l111111l1_opy_
            if bstack111lll11l11_opy_ == PytestBDDFramework.bstack111lll1l1l1_opy_
            else PytestBDDFramework.bstack111ll1ll111_opy_
        )
        bstack11l1111l111_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111lll11l11_opy_, None)
        bstack111ll1l1lll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111llll1l1l_opy_, None) if bstack11l1111l111_opy_ else None
        return (
            bstack111ll1l1lll_opy_[bstack11l1111l111_opy_][-1]
            if isinstance(bstack111ll1l1lll_opy_, dict) and len(bstack111ll1l1lll_opy_.get(bstack11l1111l111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111111l_opy_(instance: bstack1l111llll11_opy_, bstack111lll11l11_opy_: str):
        hook = PytestBDDFramework.bstack111llll1111_opy_(instance, bstack111lll11l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l111l1111_opy_, []).clear()
    @staticmethod
    def __111llll111l_opy_(instance: bstack1l111llll11_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᦢ"), None)):
            return
        if os.getenv(bstack111ll11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᦣ"), bstack111ll11_opy_ (u"ࠧ࠷ࠢᦤ")) != bstack111ll11_opy_ (u"ࠨ࠱ࠣᦥ"):
            PytestBDDFramework.logger.warning(bstack111ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᦦ"))
            return
        bstack11l111l1l11_opy_ = {
            bstack111ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᦧ"): (PytestBDDFramework.bstack111ll1llll1_opy_, PytestBDDFramework.bstack111ll1ll111_opy_),
            bstack111ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᦨ"): (PytestBDDFramework.bstack111lll1l1l1_opy_, PytestBDDFramework.bstack11l111111l1_opy_),
        }
        for when in (bstack111ll11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᦩ"), bstack111ll11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᦪ"), bstack111ll11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᦫ")):
            bstack11l111l1l1l_opy_ = args[1].get_records(when)
            if not bstack11l111l1l1l_opy_:
                continue
            records = [
                bstack1llll111ll_opy_(
                    kind=TestFramework.bstack11lll1111ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111ll11_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤ᦬")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111ll11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣ᦭")) and r.created
                        else None
                    ),
                )
                for r in bstack11l111l1l1l_opy_
                if isinstance(getattr(r, bstack111ll11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ᦮"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111ll11ll11_opy_, bstack111llll1l1l_opy_ = bstack11l111l1l11_opy_.get(when, (None, None))
            bstack111lllll1ll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111ll11ll11_opy_, None) if bstack111ll11ll11_opy_ else None
            bstack111ll1l1lll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111llll1l1l_opy_, None) if bstack111lllll1ll_opy_ else None
            if isinstance(bstack111ll1l1lll_opy_, dict) and len(bstack111ll1l1lll_opy_.get(bstack111lllll1ll_opy_, [])) > 0:
                hook = bstack111ll1l1lll_opy_[bstack111lllll1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l111l1111_opy_ in hook:
                    hook[TestFramework.bstack11l111l1111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll1lll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__111lll11l1l_opy_(request.node, scenario)
        bstack111lllll11l_opy_ = feature.filename
        if not test_id or not test_name or not bstack111lllll11l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l111l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11l1l1l1l1l_opy_: test_id,
            TestFramework.bstack1l111l1lll1_opy_: test_name,
            TestFramework.bstack11ll111111l_opy_: test_id,
            TestFramework.bstack11l1111l1ll_opy_: bstack111lllll11l_opy_,
            TestFramework.bstack111ll1l1l11_opy_: PytestBDDFramework.__111lll1l1ll_opy_(feature, scenario),
            TestFramework.bstack111lll111ll_opy_: code,
            TestFramework.bstack11l1ll11111_opy_: TestFramework.bstack111ll11llll_opy_,
            TestFramework.bstack11l11l1l1ll_opy_: test_name
        }
    @staticmethod
    def __111lll11l1l_opy_(node, scenario):
        if hasattr(node, bstack111ll11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ᦯")):
            parts = node.nodeid.rsplit(bstack111ll11_opy_ (u"ࠥ࡟ࠧᦰ"))
            params = parts[-1]
            return bstack111ll11_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᦱ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __111lll1l1ll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack111ll11_opy_ (u"ࠬࡺࡡࡨࡵࠪᦲ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack111ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᦳ")) else [])
    @staticmethod
    def __11l1111lll1_opy_(location):
        return bstack111ll11_opy_ (u"ࠢ࠻࠼ࠥᦴ").join(filter(lambda x: isinstance(x, str), location))