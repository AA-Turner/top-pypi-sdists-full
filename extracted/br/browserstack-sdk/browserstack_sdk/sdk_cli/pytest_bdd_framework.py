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
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11ll11l_opy_,
    TestHookState,
    bstack1ll1lll1l1l_opy_,
    bstack11lllllll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1ll1lllll_opy_
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l11l_opy_ import bstack1l1ll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
bstack11l1llll1l1_opy_ = bstack1l1ll1lllll_opy_()
bstack11ll111llll_opy_ = bstack111l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦ᥹")
bstack111ll11l1l1_opy_ = bstack111l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ᥺")
bstack111lll1ll1l_opy_ = bstack111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ᥻")
bstack111ll111ll1_opy_ = 1.0
_11ll1111l1l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack111lll11111_opy_ = bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ᥼")
    bstack111ll11l111_opy_ = bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨ᥽")
    bstack111ll1lll11_opy_ = bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ᥾")
    bstack111ll111lll_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧ᥿")
    bstack111ll1l1ll1_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᦀ")
    bstack111l1llll1l_opy_: bool
    bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_  = None
    bstack1l1l1l1lll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1lll1l111_opy_: Dict[str, str],
        bstack1l1ll1ll11l_opy_: List[str]=[bstack111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᦁ")],
        bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_ = None,
        bstack11l11lll11_opy_=None
    ):
        super().__init__(bstack1l1ll1ll11l_opy_, bstack1l1lll1l111_opy_, bstack1l1l1ll11l1_opy_)
        self.bstack111l1llll1l_opy_ = any(bstack111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᦂ") in item.lower() for item in bstack1l1ll1ll11l_opy_)
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
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_:
            bstack111l1llllll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᦃ") + str(test_hook_state) + bstack111l_opy_ (u"ࠣࠤᦄ"))
            return
        if not self.bstack111l1llll1l_opy_:
            self.logger.warning(bstack111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᦅ") + str(str(self.bstack1l1ll1ll11l_opy_)) + bstack111l_opy_ (u"ࠥࠦᦆ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᦇ") + str(kwargs) + bstack111l_opy_ (u"ࠧࠨᦈ"))
            return
        instance = self.__111lll11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᦉ") + str(args) + bstack111l_opy_ (u"ࠢࠣᦊ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111ll1l111_opy_.value)
                name = str(EVENTS.bstack111ll1l111_opy_.name)+bstack111l_opy_ (u"ࠣ࠼ࠥᦋ")+str(test_framework_state.name)
                TestFramework.bstack111ll1llll1_opy_(instance, name, bstack1l1l111lll_opy_)
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᦌ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1ll111l1l_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111ll111l11_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack111l_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᦍ") + str(test_hook_state) + bstack111l_opy_ (u"ࠦࠧᦎ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__111ll1ll11l_opy_(instance, args)
                    self.logger.debug(bstack111l_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᦏ") + str(test_hook_state) + bstack111l_opy_ (u"ࠨࠢᦐ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᦑ") + str(test_hook_state) + bstack111l_opy_ (u"ࠣࠤᦒ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__111lll1l1ll_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__111llll111l_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__111ll1lllll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll1lll1_opy_(instance, *args)
                self.__1l1l1l11l11_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_:
                self.__111ll1111l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᦓ") + str(instance.ref()) + bstack111l_opy_ (u"ࠥࠦᦔ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l1l11lll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack111ll1l111_opy_.name)+bstack111l_opy_ (u"ࠦ࠿ࠨᦕ")+str(test_framework_state.name)
                bstack1l1l111lll_opy_ = TestFramework.bstack111ll1l1lll_opy_(instance, name)
                bstack11lll11111_opy_.end(EVENTS.bstack111ll1l111_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᦖ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᦗ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᦘ").format(e))
    def bstack1l1l1llll1l_opy_(self):
        return self.bstack111l1llll1l_opy_
    def bstack1l1lll11111_opy_(self):
        return False
    def __111lll111ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᦙ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11l1ll1ll11_opy_(rep, [bstack111l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᦚ"), bstack111l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᦛ"), bstack111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᦜ"), bstack111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᦝ"), bstack111l_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᦞ"), bstack111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᦟ")])
        return None
    def __111lll1lll1_opy_(self, instance: bstack1l1l11ll11l_opy_, *args):
        result = self.__111lll111ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        if result.get(bstack111l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᦠ"), None) == bstack111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᦡ") and len(args) > 1 and getattr(args[1], bstack111l_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᦢ"), None) is not None:
            failure = [{bstack111l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᦣ"): [args[1].excinfo.exconly(), result.get(bstack111l_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᦤ"), None)]}]
            bstack1ll111l1l1l_opy_ = bstack111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᦥ") if bstack111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᦦ") in getattr(args[1].excinfo, bstack111l_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᦧ"), bstack111l_opy_ (u"ࠤࠥᦨ")) else bstack111l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᦩ")
        bstack111lll1l11l_opy_ = result.get(bstack111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᦪ"), TestFramework.bstack1l1lll11l11_opy_)
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
            target = None # bstack11l1ll111l1_opy_ bstack111lll1l1l1_opy_ this to be bstack111l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᦫ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111llll11l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack111l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᦬"), None), bstack111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᦭"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111l_opy_ (u"ࠣࡰࡲࡨࡪࠨ᦮"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᦯"), None):
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
        bstack1l1ll1l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, PytestBDDFramework.bstack111ll11l111_opy_, {})
        if not key in bstack1l1ll1l11ll_opy_:
            bstack1l1ll1l11ll_opy_[key] = []
        bstack1l1l11lll11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, PytestBDDFramework.bstack111ll1lll11_opy_, {})
        if not key in bstack1l1l11lll11_opy_:
            bstack1l1l11lll11_opy_[key] = []
        bstack1l1ll11l1l1_opy_ = {
            PytestBDDFramework.bstack111ll11l111_opy_: bstack1l1ll1l11ll_opy_,
            PytestBDDFramework.bstack111ll1lll11_opy_: bstack1l1l11lll11_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack111l_opy_ (u"ࠥ࡯ࡪࡿࠢᦰ"): key,
                TestFramework.bstack1l1ll11llll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1ll11ll1l_opy_: TestFramework.bstack1l1ll11lll1_opy_,
                TestFramework.bstack1l1l11llll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1ll11l111_opy_: [],
                TestFramework.bstack1l1ll11l1ll_opy_: hook_name,
                TestFramework.bstack111lll1l111_opy_: bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()
            }
            bstack1l1ll1l11ll_opy_[key].append(hook)
            bstack1l1ll11l1l1_opy_[PytestBDDFramework.bstack111ll111lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack1l1l1l1llll_opy_ = bstack1l1ll1l11ll_opy_.get(key, [])
            hook = bstack1l1l1l1llll_opy_.pop() if bstack1l1l1l1llll_opy_ else None
            if hook:
                result = self.__111lll111ll_opy_(*args)
                if result:
                    bstack111ll11111l_opy_ = result.get(bstack111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᦱ"), TestFramework.bstack1l1ll11lll1_opy_)
                    if bstack111ll11111l_opy_ != TestFramework.bstack1l1ll11lll1_opy_:
                        hook[TestFramework.bstack1l1ll11ll1l_opy_] = bstack111ll11111l_opy_
                hook[TestFramework.bstack1l1ll1ll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111lll1l111_opy_] = bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()
                self.bstack111ll1lll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll1l1l1l_opy_, [])
                self.bstack11l1lll11_opy_(instance, logs)
                bstack1l1l11lll11_opy_[key].append(hook)
                bstack1l1ll11l1l1_opy_[PytestBDDFramework.bstack111ll1l1ll1_opy_] = key
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᦲ") + str(bstack1l1l11lll11_opy_) + bstack111l_opy_ (u"ࠨࠢᦳ"))
    def __111lll1ll11_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11l1ll1ll11_opy_(args[0], [bstack111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᦴ"), bstack111l_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᦵ"), bstack111l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᦶ"), bstack111l_opy_ (u"ࠥ࡭ࡩࡹࠢᦷ"), bstack111l_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᦸ"), bstack111l_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᦹ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack111l_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᦺ")) else fixturedef.get(bstack111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᦻ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᦼ")) else None
        node = request.node if hasattr(request, bstack111l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᦽ")) else None
        target = request.node.nodeid if hasattr(node, bstack111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᦾ")) else None
        baseid = fixturedef.get(bstack111l_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᦿ"), None) or bstack111l_opy_ (u"ࠧࠨᧀ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111l_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᧁ")):
            target = PytestBDDFramework.__111lll111l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᧂ")) else None
            if target and not TestFramework.bstack1l1l1l1l11l_opy_(target):
                self.__111llll11l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᧃ") + str(test_hook_state) + bstack111l_opy_ (u"ࠤࠥᧄ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᧅ") + str(target) + bstack111l_opy_ (u"ࠦࠧᧆ"))
            return None
        instance = TestFramework.bstack1l1l1l1l11l_opy_(target)
        if not instance:
            self.logger.warning(bstack111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᧇ") + str(target) + bstack111l_opy_ (u"ࠨࠢᧈ"))
            return None
        bstack111ll11lll1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, PytestBDDFramework.bstack111lll11111_opy_, {})
        if os.getenv(bstack111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᧉ"), bstack111l_opy_ (u"ࠣ࠳ࠥ᧊")) == bstack111l_opy_ (u"ࠤ࠴ࠦ᧋"):
            bstack111ll1l111l_opy_ = bstack111l_opy_ (u"ࠥ࠾ࠧ᧌").join((scope, fixturename))
            bstack111lll11l11_opy_ = datetime.now(tz=timezone.utc)
            bstack111ll1l1111_opy_ = {
                bstack111l_opy_ (u"ࠦࡰ࡫ࡹࠣ᧍"): bstack111ll1l111l_opy_,
                bstack111l_opy_ (u"ࠧࡺࡡࡨࡵࠥ᧎"): PytestBDDFramework.__111ll1ll111_opy_(request.node, scenario),
                bstack111l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢ᧏"): fixturedef,
                bstack111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᧐"): scope,
                bstack111l_opy_ (u"ࠣࡶࡼࡴࡪࠨ᧑"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack111l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨ᧒"), None)):
                    bstack111ll1l1111_opy_[bstack111l_opy_ (u"ࠥࡸࡾࡶࡥࠣ᧓")] = TestFramework.bstack11l1lll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111ll1l1111_opy_[bstack111l_opy_ (u"ࠦࡺࡻࡩࡥࠤ᧔")] = uuid4().__str__()
                bstack111ll1l1111_opy_[PytestBDDFramework.bstack1l1l11llll1_opy_] = bstack111lll11l11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111ll1l1111_opy_[PytestBDDFramework.bstack1l1ll1ll1ll_opy_] = bstack111lll11l11_opy_
            if bstack111ll1l111l_opy_ in bstack111ll11lll1_opy_:
                bstack111ll11lll1_opy_[bstack111ll1l111l_opy_].update(bstack111ll1l1111_opy_)
                self.logger.debug(bstack111l_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨ᧕") + str(bstack111ll11lll1_opy_[bstack111ll1l111l_opy_]) + bstack111l_opy_ (u"ࠨࠢ᧖"))
            else:
                bstack111ll11lll1_opy_[bstack111ll1l111l_opy_] = bstack111ll1l1111_opy_
                self.logger.debug(bstack111l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥ᧗") + str(len(bstack111ll11lll1_opy_)) + bstack111l_opy_ (u"ࠣࠤ᧘"))
        TestFramework.bstack1l11l1ll11_opy_(instance, PytestBDDFramework.bstack111lll11111_opy_, bstack111ll11lll1_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᧙") + str(instance.ref()) + bstack111l_opy_ (u"ࠥࠦ᧚"))
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
            PytestBDDFramework.bstack111lll11111_opy_: {},
            PytestBDDFramework.bstack111ll1lll11_opy_: {},
            PytestBDDFramework.bstack111ll11l111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l11l1ll11_opy_(ob, TestFramework.bstack111ll1l11l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l11l1ll11_opy_(ob, TestFramework.bstack1l1l1l11ll1_opy_, context.platform_index)
        TestFramework.bstack1l111l111_opy_[ctx.id] = ob
        self.logger.debug(bstack111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦ᧛") + str(TestFramework.bstack1l111l111_opy_.keys()) + bstack111l_opy_ (u"ࠧࠨ᧜"))
        return ob
    @staticmethod
    def __111ll1ll11l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l_opy_ (u"࠭ࡩࡥࠩ᧝"): id(step),
                bstack111l_opy_ (u"ࠧࡵࡧࡻࡸࠬ᧞"): step.name,
                bstack111l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ᧟"): step.keyword,
            })
        meta = {
            bstack111l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ᧠"): {
                bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ᧡"): feature.name,
                bstack111l_opy_ (u"ࠫࡵࡧࡴࡩࠩ᧢"): feature.filename,
                bstack111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᧣"): feature.description
            },
            bstack111l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ᧤"): {
                bstack111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᧥"): scenario.name
            },
            bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᧦"): steps,
            bstack111l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ᧧"): PytestBDDFramework.__111ll111l1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l1lll11ll1_opy_: meta
            }
        )
    def bstack111ll1lll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᧨")
        global _11ll1111l1l_opy_
        platform_index = os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᧩")]
        bstack1l1l1l1l1ll_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), bstack111ll11l1l1_opy_)
        if not os.path.exists(bstack1l1l1l1l1ll_opy_) or not os.path.isdir(bstack1l1l1l1l1ll_opy_):
            return
        logs = hook.get(bstack111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥ᧪"), [])
        with os.scandir(bstack1l1l1l1l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1111l1l_opy_:
                    self.logger.info(bstack111l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦ᧫").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l_opy_ (u"ࠢࠣ᧬")
                    log_entry = bstack11lllllll1_opy_(
                        kind=bstack111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᧭"),
                        message=bstack111l_opy_ (u"ࠤࠥ᧮"),
                        level=bstack111l_opy_ (u"ࠥࠦ᧯"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                        bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᧰"),
                        bstack1lllllll_opy_=os.path.abspath(entry.path),
                        bstack111ll1ll1ll_opy_=hook.get(TestFramework.bstack1l1ll11llll_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1111l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᧱")]
        bstack111llll1111_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), bstack111ll11l1l1_opy_, bstack111lll1ll1l_opy_)
        if not os.path.exists(bstack111llll1111_opy_) or not os.path.isdir(bstack111llll1111_opy_):
            self.logger.info(bstack111l_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣ᧲").format(bstack111llll1111_opy_))
        else:
            self.logger.info(bstack111l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ᧳").format(bstack111llll1111_opy_))
            with os.scandir(bstack111llll1111_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1111l1l_opy_:
                        self.logger.info(bstack111l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨ᧴").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l_opy_ (u"ࠤࠥ᧵")
                        log_entry = bstack11lllllll1_opy_(
                            kind=bstack111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ᧶"),
                            message=bstack111l_opy_ (u"ࠦࠧ᧷"),
                            level=bstack111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤ᧸"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                            bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ᧹"),
                            bstack1lllllll_opy_=os.path.abspath(entry.path),
                            bstack11ll1111111_opy_=hook.get(TestFramework.bstack1l1ll11llll_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1111l1l_opy_.add(abs_path)
        hook[bstack111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ᧺")] = logs
    def bstack11l1lll11_opy_(
        self,
        bstack1lll1l1lll_opy_: bstack1l1l11ll11l_opy_,
        entries: List[bstack11lllllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧ᧻"))
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1l11ll1_opy_)
        req.client_worker_id = bstack111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᧼").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1lll1l1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1lll1l1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1lll1l1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1ll1l1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1lll1l1_opy_)
            log_entry.uuid = entry.bstack111ll1ll1ll_opy_ if entry.bstack111ll1ll1ll_opy_ else TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1lll11l_opy_)
            log_entry.test_framework_state = bstack1lll1l1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᧽"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᧾"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack11ll11l1ll1_opy_():
            bstack1lllllll1ll_opy_ = datetime.now()
            try:
                self.bstack11l11lll11_opy_.LogCreatedEvent(req)
                bstack1lll1l1lll_opy_.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ᧿"), datetime.now() - bstack1lllllll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᨀ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1l1ll11l1_opy_.enqueue(bstack11ll11l1ll1_opy_)
    def __1l1l1l11l11_opy_(self, instance) -> None:
        bstack111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᨁ")
        bstack1l1ll11l1l1_opy_ = {bstack111l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᨂ"): bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()}
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
    @staticmethod
    def __111lll1l1ll_opy_(instance, args):
        request, bstack111ll1l11ll_opy_ = args
        bstack111ll1111ll_opy_ = id(bstack111ll1l11ll_opy_)
        bstack111ll111111_opy_ = instance.data[TestFramework.bstack1l1lll11ll1_opy_]
        step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠩ࡬ࡨࠬᨃ")] == bstack111ll1111ll_opy_, bstack111ll111111_opy_[bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᨄ")]), None)
        step.update({
            bstack111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᨅ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack111ll111111_opy_[bstack111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᨆ")]) if st[bstack111l_opy_ (u"࠭ࡩࡥࠩᨇ")] == step[bstack111l_opy_ (u"ࠧࡪࡦࠪᨈ")]), None)
        if index is not None:
            bstack111ll111111_opy_[bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᨉ")][index] = step
        instance.data[TestFramework.bstack1l1lll11ll1_opy_] = bstack111ll111111_opy_
    @staticmethod
    def __111llll111l_opy_(instance, args):
        bstack111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᨊ")
        bstack1ll1l1ll11l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111ll1l11ll_opy_ = args[1]
        bstack111ll1111ll_opy_ = id(bstack111ll1l11ll_opy_)
        bstack111ll111111_opy_ = instance.data[TestFramework.bstack1l1lll11ll1_opy_]
        step = None
        if bstack111ll1111ll_opy_ is not None and bstack111ll111111_opy_.get(bstack111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᨋ")):
            step = next(filter(lambda st: st[bstack111l_opy_ (u"ࠫ࡮ࡪࠧᨌ")] == bstack111ll1111ll_opy_, bstack111ll111111_opy_[bstack111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᨍ")]), None)
            step.update({
                bstack111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᨎ"): bstack1ll1l1ll11l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᨏ"): bstack111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᨐ"),
                bstack111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᨑ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᨒ"): bstack111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᨓ"),
                })
        index = next((i for i, st in enumerate(bstack111ll111111_opy_[bstack111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᨔ")]) if st[bstack111l_opy_ (u"࠭ࡩࡥࠩᨕ")] == step[bstack111l_opy_ (u"ࠧࡪࡦࠪᨖ")]), None)
        if index is not None:
            bstack111ll111111_opy_[bstack111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᨗ")][index] = step
        instance.data[TestFramework.bstack1l1lll11ll1_opy_] = bstack111ll111111_opy_
    @staticmethod
    def __111ll111l1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack111l_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦᨘࠫ")):
                examples = list(node.callspec.params[bstack111l_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᨙ")].values())
            return examples
        except:
            return []
    def bstack1l1lll1111l_opy_(self, instance: bstack1l1l11ll11l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11ll1_opy_ = (
            PytestBDDFramework.bstack111ll111lll_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111ll1l1ll1_opy_
        )
        hook = PytestBDDFramework.bstack111ll1ll1l1_opy_(instance, bstack111lll11ll1_opy_)
        entries = hook.get(TestFramework.bstack1l1ll11l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, []))
        return entries
    def bstack1l1l1l11111_opy_(self, instance: bstack1l1l11ll11l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11ll1_opy_ = (
            PytestBDDFramework.bstack111ll111lll_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111ll1l1ll1_opy_
        )
        PytestBDDFramework.bstack111ll11ll11_opy_(instance, bstack111lll11ll1_opy_)
        TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, []).clear()
    @staticmethod
    def bstack111ll1ll1l1_opy_(instance: bstack1l1l11ll11l_opy_, bstack111lll11ll1_opy_: str):
        bstack111ll11l1ll_opy_ = (
            PytestBDDFramework.bstack111ll1lll11_opy_
            if bstack111lll11ll1_opy_ == PytestBDDFramework.bstack111ll1l1ll1_opy_
            else PytestBDDFramework.bstack111ll11l111_opy_
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
        hook = PytestBDDFramework.bstack111ll1ll1l1_opy_(instance, bstack111lll11ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1ll11l111_opy_, []).clear()
    @staticmethod
    def __111ll1lllll_opy_(instance: bstack1l1l11ll11l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᨚ"), None)):
            return
        if os.getenv(bstack111l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᨛ"), bstack111l_opy_ (u"ࠨ࠱ࠣ᨜")) != bstack111l_opy_ (u"ࠢ࠲ࠤ᨝"):
            PytestBDDFramework.logger.warning(bstack111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥ᨞"))
            return
        bstack111lll1111l_opy_ = {
            bstack111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ᨟"): (PytestBDDFramework.bstack111ll111lll_opy_, PytestBDDFramework.bstack111ll11l111_opy_),
            bstack111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᨠ"): (PytestBDDFramework.bstack111ll1l1ll1_opy_, PytestBDDFramework.bstack111ll1lll11_opy_),
        }
        for when in (bstack111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᨡ"), bstack111l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᨢ"), bstack111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᨣ")):
            bstack111l1lllll1_opy_ = args[1].get_records(when)
            if not bstack111l1lllll1_opy_:
                continue
            records = [
                bstack11lllllll1_opy_(
                    kind=TestFramework.bstack11l1lllll11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᨤ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111l_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᨥ")) and r.created
                        else None
                    ),
                )
                for r in bstack111l1lllll1_opy_
                if isinstance(getattr(r, bstack111l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᨦ"), None), str) and r.message.strip()
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
    def __111ll111l11_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__111ll11ll1l_opy_(request.node, scenario)
        bstack111ll11llll_opy_ = feature.filename
        if not test_id or not test_name or not bstack111ll11llll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l1lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1ll111l1l_opy_: test_id,
            TestFramework.bstack1l1ll1lll1l_opy_: test_name,
            TestFramework.bstack1l1ll11ll11_opy_: test_id,
            TestFramework.bstack1l1ll111lll_opy_: bstack111ll11llll_opy_,
            TestFramework.bstack1l1ll1ll1l1_opy_: PytestBDDFramework.__111ll1ll111_opy_(feature, scenario),
            TestFramework.bstack1l1ll111l11_opy_: code,
            TestFramework.bstack1l1ll1lll11_opy_: TestFramework.bstack1l1lll11l11_opy_,
            TestFramework.bstack1l1l1lll1ll_opy_: test_name
        }
    @staticmethod
    def __111ll11ll1l_opy_(node, scenario):
        if hasattr(node, bstack111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᨧ")):
            parts = node.nodeid.rsplit(bstack111l_opy_ (u"ࠦࡠࠨᨨ"))
            params = parts[-1]
            return bstack111l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᨩ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __111ll1ll111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack111l_opy_ (u"࠭ࡴࡢࡩࡶࠫᨪ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack111l_opy_ (u"ࠧࡵࡣࡪࡷࠬᨫ")) else [])
    @staticmethod
    def __111lll111l1_opy_(location):
        return bstack111l_opy_ (u"ࠣ࠼࠽ࠦᨬ").join(filter(lambda x: isinstance(x, str), location))