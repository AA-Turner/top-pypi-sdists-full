# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll1l1ll1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1l11_opy_ import bstack11l1l1lll11_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111lllll_opy_,
    TestHookState,
    bstack1ll1lll11l1_opy_,
    bstack1l1lllllll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l111llll1l_opy_
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll11l11111_opy_ import bstack1ll111lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1ll1ll11l11_opy_
bstack1l111l1ll11_opy_ = bstack1l111llll1l_opy_()
bstack1l1111l1l1l_opy_ = bstack1111l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᝉ")
bstack11l1l1l1111_opy_ = bstack1111l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᝊ")
bstack11l1l1lll1l_opy_ = bstack1111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᝋ")
bstack11ll11l1l1l_opy_ = 1.0
_1l11111l1ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l1l1l11l1_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᝌ")
    bstack11ll11l111l_opy_ = bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᝍ")
    bstack11ll1111ll1_opy_ = bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᝎ")
    bstack11l1ll11l1l_opy_ = bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᝏ")
    bstack11l1lll1l11_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᝐ")
    bstack11l1llll1l1_opy_: bool
    bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_  = None
    bstack11l1ll1l111_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1l11llll_opy_: Dict[str, str],
        bstack1l11lll111l_opy_: List[str]=[bstack1111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᝑ")],
        bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_ = None,
        bstack1ll1ll1lll1_opy_=None
    ):
        super().__init__(bstack1l11lll111l_opy_, bstack11l1l11llll_opy_, bstack1ll1ll11lll_opy_)
        self.bstack11l1llll1l1_opy_ = any(bstack1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᝒ") in item.lower() for item in bstack1l11lll111l_opy_)
        self.bstack1ll1ll1lll1_opy_ = bstack1ll1ll1lll1_opy_
    def track_event(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l1ll1l111_opy_:
            bstack11l1l1lll11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᝓ") + str(test_hook_state) + bstack1111l_opy_ (u"ࠣࠤ᝔"))
            return
        if not self.bstack11l1llll1l1_opy_:
            self.logger.warning(bstack1111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥ᝕") + str(str(self.bstack1l11lll111l_opy_)) + bstack1111l_opy_ (u"ࠥࠦ᝖"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᝗") + str(kwargs) + bstack1111l_opy_ (u"ࠧࠨ᝘"))
            return
        instance = self.__11ll11l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧ᝙") + str(args) + bstack1111l_opy_ (u"ࠢࠣ᝚"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll1l111_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l11ll1l1l_opy_.value)
                name = str(EVENTS.bstack1l11ll1l1l_opy_.name)+bstack1111l_opy_ (u"ࠣ࠼ࠥ᝛")+str(test_framework_state.name)
                TestFramework.bstack11l1ll1l11l_opy_(instance, name, bstack1l1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨ᝜").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack11llll1l1l1_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11l1lllll1l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1111l_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ᝝") + str(test_hook_state) + bstack1111l_opy_ (u"ࠦࠧ᝞"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11l111l11_opy_):
                    TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l111l11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11ll111llll_opy_(instance, args)
                    self.logger.debug(bstack1111l_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ᝟") + str(test_hook_state) + bstack1111l_opy_ (u"ࠨࠢᝠ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_):
                    TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᝡ") + str(test_hook_state) + bstack1111l_opy_ (u"ࠣࠤᝢ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l1l1l111l_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1l1ll1ll_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1ll1l1l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll111l111_opy_(instance, *args)
                self.__11ll1111l1l_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1ll1l111_opy_:
                self.__11ll111l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᝣ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠥࠦᝤ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1lll1ll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll1l111_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1l11ll1l1l_opy_.name)+bstack1111l_opy_ (u"ࠦ࠿ࠨᝥ")+str(test_framework_state.name)
                bstack1l1llll1_opy_ = TestFramework.bstack11l1lllllll_opy_(instance, name)
                bstack1l11ll1l1_opy_.end(EVENTS.bstack1l11ll1l1l_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᝦ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᝧ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᝨ").format(e))
    def bstack1l11111llll_opy_(self):
        return self.bstack11l1llll1l1_opy_
    def bstack1l1111l11l1_opy_(self):
        return False
    def __11ll11l11l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᝩ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11111l1l1_opy_(rep, [bstack1111l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᝪ"), bstack1111l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᝫ"), bstack1111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᝬ"), bstack1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᝭"), bstack1111l_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᝮ"), bstack1111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᝯ")])
        return None
    def __11ll111l111_opy_(self, instance: bstack1ll111lllll_opy_, *args):
        result = self.__11ll11l11l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll11l1l1l_opy_ = None
        if result.get(bstack1111l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᝰ"), None) == bstack1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᝱") and len(args) > 1 and getattr(args[1], bstack1111l_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᝲ"), None) is not None:
            failure = [{bstack1111l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᝳ"): [args[1].excinfo.exconly(), result.get(bstack1111l_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦ᝴"), None)]}]
            bstack1lll11l1l1l_opy_ = bstack1111l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᝵") if bstack1111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ᝶") in getattr(args[1].excinfo, bstack1111l_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥ᝷"), bstack1111l_opy_ (u"ࠤࠥ᝸")) else bstack1111l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ᝹")
        bstack11l1llll1ll_opy_ = result.get(bstack1111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᝺"), TestFramework.bstack11ll1111l11_opy_)
        if bstack11l1llll1ll_opy_ != TestFramework.bstack11ll1111l11_opy_:
            TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1111lll_opy_(instance, {
            TestFramework.bstack11llll11l11_opy_: failure,
            TestFramework.bstack11l1l1l11ll_opy_: bstack1lll11l1l1l_opy_,
            TestFramework.bstack11lll1ll1l1_opy_: bstack11l1llll1ll_opy_,
        })
    def __11ll11l11ll_opy_(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l1llll11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111llll11_opy_ bstack11l1llllll1_opy_ this to be bstack1111l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᝻")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll111111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1111l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᝼"), None), bstack1111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᝽"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111l_opy_ (u"ࠣࡰࡲࡨࡪࠨ᝾"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᝿"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1l11l111_opy_(target) if target else None
        return instance
    def __11ll111l11l_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1ll1111l_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, PytestBDDFramework.bstack11ll11l111l_opy_, {})
        if not key in bstack11l1ll1111l_opy_:
            bstack11l1ll1111l_opy_[key] = []
        bstack11ll11ll1ll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, PytestBDDFramework.bstack11ll1111ll1_opy_, {})
        if not key in bstack11ll11ll1ll_opy_:
            bstack11ll11ll1ll_opy_[key] = []
        bstack11l1lllll11_opy_ = {
            PytestBDDFramework.bstack11ll11l111l_opy_: bstack11l1ll1111l_opy_,
            PytestBDDFramework.bstack11ll1111ll1_opy_: bstack11ll11ll1ll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1111l_opy_ (u"ࠥ࡯ࡪࡿࠢក"): key,
                TestFramework.bstack11l1ll1l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack11ll111ll11_opy_: TestFramework.bstack11ll1111111_opy_,
                TestFramework.bstack11ll111l1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll11111_opy_: [],
                TestFramework.bstack11l1l1l1l11_opy_: hook_name,
                TestFramework.bstack11l1l1l1lll_opy_: bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()
            }
            bstack11l1ll1111l_opy_[key].append(hook)
            bstack11l1lllll11_opy_[PytestBDDFramework.bstack11l1ll11l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll11lll_opy_ = bstack11l1ll1111l_opy_.get(key, [])
            hook = bstack11l1ll11lll_opy_.pop() if bstack11l1ll11lll_opy_ else None
            if hook:
                result = self.__11ll11l11l1_opy_(*args)
                if result:
                    bstack11l1l1ll11l_opy_ = result.get(bstack1111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧខ"), TestFramework.bstack11ll1111111_opy_)
                    if bstack11l1l1ll11l_opy_ != TestFramework.bstack11ll1111111_opy_:
                        hook[TestFramework.bstack11ll111ll11_opy_] = bstack11l1l1ll11l_opy_
                hook[TestFramework.bstack11l1ll1llll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1lll_opy_] = bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()
                self.bstack11l1ll1ll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll1ll11_opy_, [])
                self.bstack1l11l1l111l_opy_(instance, logs)
                bstack11ll11ll1ll_opy_[key].append(hook)
                bstack11l1lllll11_opy_[PytestBDDFramework.bstack11l1lll1l11_opy_] = key
        TestFramework.bstack11ll1111lll_opy_(instance, bstack11l1lllll11_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦគ") + str(bstack11ll11ll1ll_opy_) + bstack1111l_opy_ (u"ࠨࠢឃ"))
    def __11l1llll11l_opy_(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11111l1l1_opy_(args[0], [bstack1111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨង"), bstack1111l_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤច"), bstack1111l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤឆ"), bstack1111l_opy_ (u"ࠥ࡭ࡩࡹࠢជ"), bstack1111l_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨឈ"), bstack1111l_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧញ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1111l_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧដ")) else fixturedef.get(bstack1111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨឋ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨឌ")) else None
        node = request.node if hasattr(request, bstack1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢឍ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥណ")) else None
        baseid = fixturedef.get(bstack1111l_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦត"), None) or bstack1111l_opy_ (u"ࠧࠨថ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111l_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦទ")):
            target = PytestBDDFramework.__11ll111lll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤធ")) else None
            if target and not TestFramework.bstack1ll1l11l111_opy_(target):
                self.__11ll111111l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥន") + str(test_hook_state) + bstack1111l_opy_ (u"ࠤࠥប"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣផ") + str(target) + bstack1111l_opy_ (u"ࠦࠧព"))
            return None
        instance = TestFramework.bstack1ll1l11l111_opy_(target)
        if not instance:
            self.logger.warning(bstack1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢភ") + str(target) + bstack1111l_opy_ (u"ࠨࠢម"))
            return None
        bstack11l1lll1111_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, PytestBDDFramework.bstack11l1l1l11l1_opy_, {})
        if os.getenv(bstack1111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣយ"), bstack1111l_opy_ (u"ࠣ࠳ࠥរ")) == bstack1111l_opy_ (u"ࠤ࠴ࠦល"):
            bstack11l1l11lll1_opy_ = bstack1111l_opy_ (u"ࠥ࠾ࠧវ").join((scope, fixturename))
            bstack11l1ll11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1l1ll111_opy_ = {
                bstack1111l_opy_ (u"ࠦࡰ࡫ࡹࠣឝ"): bstack11l1l11lll1_opy_,
                bstack1111l_opy_ (u"ࠧࡺࡡࡨࡵࠥឞ"): PytestBDDFramework.__11ll11ll111_opy_(request.node, scenario),
                bstack1111l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢស"): fixturedef,
                bstack1111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨហ"): scope,
                bstack1111l_opy_ (u"ࠣࡶࡼࡴࡪࠨឡ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1111l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨអ"), None)):
                    bstack11l1l1ll111_opy_[bstack1111l_opy_ (u"ࠥࡸࡾࡶࡥࠣឣ")] = TestFramework.bstack1l1111l11ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1l1ll111_opy_[bstack1111l_opy_ (u"ࠦࡺࡻࡩࡥࠤឤ")] = uuid4().__str__()
                bstack11l1l1ll111_opy_[PytestBDDFramework.bstack11ll111l1l1_opy_] = bstack11l1ll11ll1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1l1ll111_opy_[PytestBDDFramework.bstack11l1ll1llll_opy_] = bstack11l1ll11ll1_opy_
            if bstack11l1l11lll1_opy_ in bstack11l1lll1111_opy_:
                bstack11l1lll1111_opy_[bstack11l1l11lll1_opy_].update(bstack11l1l1ll111_opy_)
                self.logger.debug(bstack1111l_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨឥ") + str(bstack11l1lll1111_opy_[bstack11l1l11lll1_opy_]) + bstack1111l_opy_ (u"ࠨࠢឦ"))
            else:
                bstack11l1lll1111_opy_[bstack11l1l11lll1_opy_] = bstack11l1l1ll111_opy_
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥឧ") + str(len(bstack11l1lll1111_opy_)) + bstack1111l_opy_ (u"ࠣࠤឨ"))
        TestFramework.bstack1ll1lllll11_opy_(instance, PytestBDDFramework.bstack11l1l1l11l1_opy_, bstack11l1lll1111_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤឩ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠥࠦឪ"))
        return instance
    def __11ll111111l_opy_(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1l1ll1l1_opy_.create_context(target)
        ob = bstack1ll111lllll_opy_(ctx, self.bstack1l11lll111l_opy_, self.bstack11l1l11llll_opy_, test_framework_state)
        TestFramework.bstack11ll1111lll_opy_(ob, {
            TestFramework.bstack1l1l1l1ll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l11l11ll1l_opy_: context.test_framework_version,
            TestFramework.bstack11l1l1ll1l1_opy_: [],
            PytestBDDFramework.bstack11l1l1l11l1_opy_: {},
            PytestBDDFramework.bstack11ll1111ll1_opy_: {},
            PytestBDDFramework.bstack11ll11l111l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1lllll11_opy_(ob, TestFramework.bstack11l1ll111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1lllll11_opy_(ob, TestFramework.bstack1l1l1l111ll_opy_, context.platform_index)
        TestFramework.bstack1ll1lll111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦឫ") + str(TestFramework.bstack1ll1lll111l_opy_.keys()) + bstack1111l_opy_ (u"ࠧࠨឬ"))
        return ob
    @staticmethod
    def __11ll111llll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111l_opy_ (u"࠭ࡩࡥࠩឭ"): id(step),
                bstack1111l_opy_ (u"ࠧࡵࡧࡻࡸࠬឮ"): step.name,
                bstack1111l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩឯ"): step.keyword,
            })
        meta = {
            bstack1111l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪឰ"): {
                bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨឱ"): feature.name,
                bstack1111l_opy_ (u"ࠫࡵࡧࡴࡩࠩឲ"): feature.filename,
                bstack1111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪឳ"): feature.description
            },
            bstack1111l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ឴"): {
                bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ឵"): scenario.name
            },
            bstack1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧា"): steps,
            bstack1111l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫិ"): PytestBDDFramework.__11l1l1l1l1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l1l1lllll_opy_: meta
            }
        )
    def bstack11l1ll1ll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤី")
        global _1l11111l1ll_opy_
        platform_index = os.environ[bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫឹ")]
        bstack1l111l1ll1l_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), bstack11l1l1l1111_opy_)
        if not os.path.exists(bstack1l111l1ll1l_opy_) or not os.path.isdir(bstack1l111l1ll1l_opy_):
            return
        logs = hook.get(bstack1111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥឺ"), [])
        with os.scandir(bstack1l111l1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111l1ll_opy_:
                    self.logger.info(bstack1111l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦុ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111l_opy_ (u"ࠢࠣូ")
                    log_entry = bstack1l1lllllll1_opy_(
                        kind=bstack1111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥួ"),
                        message=bstack1111l_opy_ (u"ࠤࠥើ"),
                        level=bstack1111l_opy_ (u"ࠥࠦឿ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11l11l1l1_opy_=entry.stat().st_size,
                        bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦៀ"),
                        bstack1llll1l_opy_=os.path.abspath(entry.path),
                        bstack11ll11l1111_opy_=hook.get(TestFramework.bstack11l1ll1l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111l1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬេ")]
        bstack11ll11l1l11_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), bstack11l1l1l1111_opy_, bstack11l1l1lll1l_opy_)
        if not os.path.exists(bstack11ll11l1l11_opy_) or not os.path.isdir(bstack11ll11l1l11_opy_):
            self.logger.info(bstack1111l_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣែ").format(bstack11ll11l1l11_opy_))
        else:
            self.logger.info(bstack1111l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨៃ").format(bstack11ll11l1l11_opy_))
            with os.scandir(bstack11ll11l1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack1111l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨោ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111l_opy_ (u"ࠤࠥៅ")
                        log_entry = bstack1l1lllllll1_opy_(
                            kind=bstack1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧំ"),
                            message=bstack1111l_opy_ (u"ࠦࠧះ"),
                            level=bstack1111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤៈ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11l11l1l1_opy_=entry.stat().st_size,
                            bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ៉"),
                            bstack1llll1l_opy_=os.path.abspath(entry.path),
                            bstack1l111ll11ll_opy_=hook.get(TestFramework.bstack11l1ll1l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111l1ll_opy_.add(abs_path)
        hook[bstack1111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ៊")] = logs
    def bstack1l11l1l111l_opy_(
        self,
        bstack1l111lll1ll_opy_: bstack1ll111lllll_opy_,
        entries: List[bstack1l1lllllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧ់"))
        req.platform_index = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l111ll_opy_)
        req.client_worker_id = bstack1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ៌").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111lll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111lll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111lll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l1ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11l11ll1l_opy_)
            log_entry.uuid = entry.bstack11ll11l1111_opy_ if entry.bstack11ll11l1111_opy_ else TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11ll1ll1l_opy_)
            log_entry.test_framework_state = bstack1l111lll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ៍"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ៎"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11l1l1_opy_
                log_entry.file_path = entry.bstack1llll1l_opy_
        def bstack1l11111lll1_opy_():
            bstack1lll1l11l_opy_ = datetime.now()
            try:
                self.bstack1ll1ll1lll1_opy_.LogCreatedEvent(req)
                bstack1l111lll1ll_opy_.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ៏"), datetime.now() - bstack1lll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧ័").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1ll11lll_opy_.enqueue(bstack1l11111lll1_opy_)
    def __11ll1111l1l_opy_(self, instance) -> None:
        bstack1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ៑")
        bstack11l1lllll11_opy_ = {bstack1111l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣ្ࠥ"): bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()}
        TestFramework.bstack11ll1111lll_opy_(instance, bstack11l1lllll11_opy_)
    @staticmethod
    def __11l1l1l111l_opy_(instance, args):
        request, bstack11ll11111l1_opy_ = args
        bstack11l1l1l1ll1_opy_ = id(bstack11ll11111l1_opy_)
        bstack11l1ll1lll1_opy_ = instance.data[TestFramework.bstack11l1l1lllll_opy_]
        step = next(filter(lambda st: st[bstack1111l_opy_ (u"ࠩ࡬ࡨࠬ៓")] == bstack11l1l1l1ll1_opy_, bstack11l1ll1lll1_opy_[bstack1111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ។")]), None)
        step.update({
            bstack1111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ៕"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11l1ll1lll1_opy_[bstack1111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ៖")]) if st[bstack1111l_opy_ (u"࠭ࡩࡥࠩៗ")] == step[bstack1111l_opy_ (u"ࠧࡪࡦࠪ៘")]), None)
        if index is not None:
            bstack11l1ll1lll1_opy_[bstack1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ៙")][index] = step
        instance.data[TestFramework.bstack11l1l1lllll_opy_] = bstack11l1ll1lll1_opy_
    @staticmethod
    def __11l1l1ll1ll_opy_(instance, args):
        bstack1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ៚")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll11111l1_opy_ = args[1]
        bstack11l1l1l1ll1_opy_ = id(bstack11ll11111l1_opy_)
        bstack11l1ll1lll1_opy_ = instance.data[TestFramework.bstack11l1l1lllll_opy_]
        step = None
        if bstack11l1l1l1ll1_opy_ is not None and bstack11l1ll1lll1_opy_.get(bstack1111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ៛")):
            step = next(filter(lambda st: st[bstack1111l_opy_ (u"ࠫ࡮ࡪࠧៜ")] == bstack11l1l1l1ll1_opy_, bstack11l1ll1lll1_opy_[bstack1111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ៝")]), None)
            step.update({
                bstack1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ៞"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ៟"): bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ០"),
                bstack1111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ១"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ២"): bstack1111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ៣"),
                })
        index = next((i for i, st in enumerate(bstack11l1ll1lll1_opy_[bstack1111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ៤")]) if st[bstack1111l_opy_ (u"࠭ࡩࡥࠩ៥")] == step[bstack1111l_opy_ (u"ࠧࡪࡦࠪ៦")]), None)
        if index is not None:
            bstack11l1ll1lll1_opy_[bstack1111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ៧")][index] = step
        instance.data[TestFramework.bstack11l1l1lllll_opy_] = bstack11l1ll1lll1_opy_
    @staticmethod
    def __11l1l1l1l1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1111l_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫ៨")):
                examples = list(node.callspec.params[bstack1111l_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩ៩")].values())
            return examples
        except:
            return []
    def bstack1l111llllll_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11ll11l_opy_ = (
            PytestBDDFramework.bstack11l1ll11l1l_opy_
            if bstack1ll1l111l11_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1lll1l11_opy_
        )
        hook = PytestBDDFramework.bstack11l1lll1lll_opy_(instance, bstack11ll11ll11l_opy_)
        entries = hook.get(TestFramework.bstack11l1ll11111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, []))
        return entries
    def bstack1l111lll111_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11ll11l_opy_ = (
            PytestBDDFramework.bstack11l1ll11l1l_opy_
            if bstack1ll1l111l11_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1lll1l11_opy_
        )
        PytestBDDFramework.bstack11l1llll111_opy_(instance, bstack11ll11ll11l_opy_)
        TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, []).clear()
    @staticmethod
    def bstack11l1lll1lll_opy_(instance: bstack1ll111lllll_opy_, bstack11ll11ll11l_opy_: str):
        bstack11ll11ll1l1_opy_ = (
            PytestBDDFramework.bstack11ll1111ll1_opy_
            if bstack11ll11ll11l_opy_ == PytestBDDFramework.bstack11l1lll1l11_opy_
            else PytestBDDFramework.bstack11ll11l111l_opy_
        )
        bstack11ll11l1lll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11ll11ll11l_opy_, None)
        bstack11l1l1llll1_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11ll11ll1l1_opy_, None) if bstack11ll11l1lll_opy_ else None
        return (
            bstack11l1l1llll1_opy_[bstack11ll11l1lll_opy_][-1]
            if isinstance(bstack11l1l1llll1_opy_, dict) and len(bstack11l1l1llll1_opy_.get(bstack11ll11l1lll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1llll111_opy_(instance: bstack1ll111lllll_opy_, bstack11ll11ll11l_opy_: str):
        hook = PytestBDDFramework.bstack11l1lll1lll_opy_(instance, bstack11ll11ll11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll11111_opy_, []).clear()
    @staticmethod
    def __11l1ll1l1l1_opy_(instance: bstack1ll111lllll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤ៪"), None)):
            return
        if os.getenv(bstack1111l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤ៫"), bstack1111l_opy_ (u"ࠨ࠱ࠣ៬")) != bstack1111l_opy_ (u"ࠢ࠲ࠤ៭"):
            PytestBDDFramework.logger.warning(bstack1111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥ៮"))
            return
        bstack11l1lll11ll_opy_ = {
            bstack1111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ៯"): (PytestBDDFramework.bstack11l1ll11l1l_opy_, PytestBDDFramework.bstack11ll11l111l_opy_),
            bstack1111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ៰"): (PytestBDDFramework.bstack11l1lll1l11_opy_, PytestBDDFramework.bstack11ll1111ll1_opy_),
        }
        for when in (bstack1111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ៱"), bstack1111l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ៲"), bstack1111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ៳")):
            bstack11ll111l1ll_opy_ = args[1].get_records(when)
            if not bstack11ll111l1ll_opy_:
                continue
            records = [
                bstack1l1lllllll1_opy_(
                    kind=TestFramework.bstack1l1111l1111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥ៴")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111l_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤ៵")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll111l1ll_opy_
                if isinstance(getattr(r, bstack1111l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ៶"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1lll1l1l_opy_, bstack11ll11ll1l1_opy_ = bstack11l1lll11ll_opy_.get(when, (None, None))
            bstack11ll11111ll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11l1lll1l1l_opy_, None) if bstack11l1lll1l1l_opy_ else None
            bstack11l1l1llll1_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11ll11ll1l1_opy_, None) if bstack11ll11111ll_opy_ else None
            if isinstance(bstack11l1l1llll1_opy_, dict) and len(bstack11l1l1llll1_opy_.get(bstack11ll11111ll_opy_, [])) > 0:
                hook = bstack11l1l1llll1_opy_[bstack11ll11111ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll11111_opy_ in hook:
                    hook[TestFramework.bstack11l1ll11111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l1lllll1l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11ll11l1ll1_opy_(request.node, scenario)
        bstack11ll111ll1l_opy_ = feature.filename
        if not test_id or not test_name or not bstack11ll111ll1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l11ll1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1l1l1_opy_: test_id,
            TestFramework.bstack1l1l111llll_opy_: test_name,
            TestFramework.bstack1l11111l111_opy_: test_id,
            TestFramework.bstack11l1ll111l1_opy_: bstack11ll111ll1l_opy_,
            TestFramework.bstack11l1lll111l_opy_: PytestBDDFramework.__11ll11ll111_opy_(feature, scenario),
            TestFramework.bstack11l1ll11l11_opy_: code,
            TestFramework.bstack11lll1ll1l1_opy_: TestFramework.bstack11ll1111l11_opy_,
            TestFramework.bstack11ll1l1ll11_opy_: test_name
        }
    @staticmethod
    def __11ll11l1ll1_opy_(node, scenario):
        if hasattr(node, bstack1111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ៷")):
            parts = node.nodeid.rsplit(bstack1111l_opy_ (u"ࠦࡠࠨ៸"))
            params = parts[-1]
            return bstack1111l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ៹").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll11ll111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ៺")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1111l_opy_ (u"ࠧࡵࡣࡪࡷࠬ៻")) else [])
    @staticmethod
    def __11ll111lll1_opy_(location):
        return bstack1111l_opy_ (u"ࠣ࠼࠽ࠦ៼").join(filter(lambda x: isinstance(x, str), location))