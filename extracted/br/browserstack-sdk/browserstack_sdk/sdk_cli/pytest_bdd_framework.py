# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11llll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1ll_opy_ import bstack11l1l1l11ll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1lllll1_opy_,
    TestHookState,
    bstack1ll1l11lll1_opy_,
    bstack1l1l11lll1l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1111l1lll_opy_
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1ll11l1l1_opy_ import bstack1l1l11lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1111ll_opy_ import bstack1ll11lllll1_opy_
bstack1l11111l1l1_opy_ = bstack1l1111l1lll_opy_()
bstack11lllll111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣឡ")
bstack11l11ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧអ")
bstack11l1ll11ll1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤឣ")
bstack11l1l1lll11_opy_ = 1.0
_1l11111llll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l11ll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦឤ")
    bstack11l11l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥឥ")
    bstack11l1l1lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧឦ")
    bstack11l11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤឧ")
    bstack11l1l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦឨ")
    bstack11l1l1llll1_opy_: bool
    bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_  = None
    bstack11l11llllll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1l111111_opy_: Dict[str, str],
        bstack1l11l1l11ll_opy_: List[str]=[bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨឩ")],
        bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_ = None,
        bstack1l1llll1lll_opy_=None
    ):
        super().__init__(bstack1l11l1l11ll_opy_, bstack11l1l111111_opy_, bstack1ll1l1111ll_opy_)
        self.bstack11l1l1llll1_opy_ = any(bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢឪ") in item.lower() for item in bstack1l11l1l11ll_opy_)
        self.bstack1l1llll1lll_opy_ = bstack1l1llll1lll_opy_
    def track_event(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l11llllll_opy_:
            bstack11l1l1l11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧឫ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠧࠨឬ"))
            return
        if not self.bstack11l1l1llll1_opy_:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢឭ") + str(str(self.bstack1l11l1l11ll_opy_)) + bstack1ll1lll_opy_ (u"ࠢࠣឮ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥឯ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥឰ"))
            return
        instance = self.__11l1lll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤឱ") + str(args) + bstack1ll1lll_opy_ (u"ࠦࠧឲ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l11llllll_opy_ and test_hook_state == TestHookState.PRE:
                bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11111l1l_opy_.value)
                name = str(EVENTS.bstack11111l1l_opy_.name)+bstack1ll1lll_opy_ (u"ࠧࡀࠢឳ")+str(test_framework_state.name)
                TestFramework.bstack11l1l11111l_opy_(instance, name, bstack111l1l1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥ឴").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack11ll1lll111_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11l11lllll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ឵") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠣࠤា"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l111l1l111_opy_):
                    TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l111l1l111_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l11llll1l_opy_(instance, args)
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢិ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠥࠦី"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l111ll1l11_opy_):
                    TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢឹ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠧࠨឺ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l1ll11lll_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l11l1l1ll_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1ll111l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1ll1ll11_opy_(instance, *args)
                self.__11l1ll1l11l_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l11llllll_opy_:
                self.__11l11lll1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢុ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠢࠣូ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1l11lll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l11llllll_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack11111l1l_opy_.name)+bstack1ll1lll_opy_ (u"ࠣ࠼ࠥួ")+str(test_framework_state.name)
                bstack111l1l1l1_opy_ = TestFramework.bstack11l1lll111l_opy_(instance, name)
                bstack1l1l11ll1_opy_.end(EVENTS.bstack11111l1l_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤើ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣឿ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦៀ").format(e))
    def bstack1l111l1l1ll_opy_(self):
        return self.bstack11l1l1llll1_opy_
    def bstack1l1111111ll_opy_(self):
        return False
    def __11l11ll1ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤេ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1111lll11_opy_(rep, [bstack1ll1lll_opy_ (u"ࠨࡷࡩࡧࡱࠦែ"), bstack1ll1lll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣៃ"), bstack1ll1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣោ"), bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤៅ"), bstack1ll1lll_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦំ"), bstack1ll1lll_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥះ")])
        return None
    def __11l1ll1ll11_opy_(self, instance: bstack1l1l1lllll1_opy_, *args):
        result = self.__11l11ll1ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lll11ll_opy_ = None
        if result.get(bstack1ll1lll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨៈ"), None) == bstack1ll1lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ៉") and len(args) > 1 and getattr(args[1], bstack1ll1lll_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣ៊"), None) is not None:
            failure = [{bstack1ll1lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ់"): [args[1].excinfo.exconly(), result.get(bstack1ll1lll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣ៌"), None)]}]
            bstack1ll1lll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ៍") if bstack1ll1lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ៎") in getattr(args[1].excinfo, bstack1ll1lll_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢ៏"), bstack1ll1lll_opy_ (u"ࠨࠢ័")) else bstack1ll1lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ៑")
        bstack11l1l1l11l1_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ្"), TestFramework.bstack11l11l1lll1_opy_)
        if bstack11l1l1l11l1_opy_ != TestFramework.bstack11l11l1lll1_opy_:
            TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l1111ll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l1lllll_opy_(instance, {
            TestFramework.bstack11ll1llll11_opy_: failure,
            TestFramework.bstack11l1l1l1ll1_opy_: bstack1ll1lll11ll_opy_,
            TestFramework.bstack11lll1111ll_opy_: bstack11l1l1l11l1_opy_,
        })
    def __11l1lll1l11_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l1lll11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lllll11l1_opy_ bstack11l1l11ll1l_opy_ this to be bstack1ll1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ៓")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l11ll1lll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1lll_opy_ (u"ࠥࡲࡴࡪࡥࠣ។"), None), bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ៕"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧࠥ៖"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll1lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨៗ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll11ll11l1_opy_(target) if target else None
        return instance
    def __11l11lll1ll_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1lll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, PytestBDDFramework.bstack11l11l1l1l1_opy_, {})
        if not key in bstack11l1lll1lll_opy_:
            bstack11l1lll1lll_opy_[key] = []
        bstack11l1l11l111_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, PytestBDDFramework.bstack11l1l1lll1l_opy_, {})
        if not key in bstack11l1l11l111_opy_:
            bstack11l1l11l111_opy_[key] = []
        bstack11l11llll11_opy_ = {
            PytestBDDFramework.bstack11l11l1l1l1_opy_: bstack11l1lll1lll_opy_,
            PytestBDDFramework.bstack11l1l1lll1l_opy_: bstack11l1l11l111_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll1lll_opy_ (u"ࠢ࡬ࡧࡼࠦ៘"): key,
                TestFramework.bstack11l1l111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11l11ll111l_opy_: TestFramework.bstack11l1l111l1l_opy_,
                TestFramework.bstack11l1lll11ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1lll1l1l_opy_: [],
                TestFramework.bstack11l11ll1l11_opy_: hook_name,
                TestFramework.bstack11l1ll11l11_opy_: bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()
            }
            bstack11l1lll1lll_opy_[key].append(hook)
            bstack11l11llll11_opy_[PytestBDDFramework.bstack11l11l1ll11_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1l1ll1ll_opy_ = bstack11l1lll1lll_opy_.get(key, [])
            hook = bstack11l1l1ll1ll_opy_.pop() if bstack11l1l1ll1ll_opy_ else None
            if hook:
                result = self.__11l11ll1ll1_opy_(*args)
                if result:
                    bstack11l1l1ll11l_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ៙"), TestFramework.bstack11l1l111l1l_opy_)
                    if bstack11l1l1ll11l_opy_ != TestFramework.bstack11l1l111l1l_opy_:
                        hook[TestFramework.bstack11l11ll111l_opy_] = bstack11l1l1ll11l_opy_
                hook[TestFramework.bstack11l1l11l1l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1ll11l11_opy_] = bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1l1111ll_opy_, [])
                self.bstack1l111ll11ll_opy_(instance, logs)
                bstack11l1l11l111_opy_[key].append(hook)
                bstack11l11llll11_opy_[PytestBDDFramework.bstack11l1l11l11l_opy_] = key
        TestFramework.bstack11l1l1lllll_opy_(instance, bstack11l11llll11_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣ៚") + str(bstack11l1l11l111_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦ៛"))
    def __11l1lll11l1_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1111lll11_opy_(args[0], [bstack1ll1lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥៜ"), bstack1ll1lll_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨ៝"), bstack1ll1lll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨ៞"), bstack1ll1lll_opy_ (u"ࠢࡪࡦࡶࠦ៟"), bstack1ll1lll_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥ០"), bstack1ll1lll_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤ១")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll1lll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ២")) else fixturedef.get(bstack1ll1lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ៣"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1lll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥ៤")) else None
        node = request.node if hasattr(request, bstack1ll1lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ៥")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ៦")) else None
        baseid = fixturedef.get(bstack1ll1lll_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣ៧"), None) or bstack1ll1lll_opy_ (u"ࠤࠥ៨")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1lll_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣ៩")):
            target = PytestBDDFramework.__11l11ll11l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1lll_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨ៪")) else None
            if target and not TestFramework.bstack1ll11ll11l1_opy_(target):
                self.__11l11ll1lll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ៫") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠨࠢ៬"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧ៭") + str(target) + bstack1ll1lll_opy_ (u"ࠣࠤ៮"))
            return None
        instance = TestFramework.bstack1ll11ll11l1_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦ៯") + str(target) + bstack1ll1lll_opy_ (u"ࠥࠦ៰"))
            return None
        bstack11l1l1111l1_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, PytestBDDFramework.bstack11l11ll11ll_opy_, {})
        if os.getenv(bstack1ll1lll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧ៱"), bstack1ll1lll_opy_ (u"ࠧ࠷ࠢ៲")) == bstack1ll1lll_opy_ (u"ࠨ࠱ࠣ៳"):
            bstack11l11l1llll_opy_ = bstack1ll1lll_opy_ (u"ࠢ࠻ࠤ៴").join((scope, fixturename))
            bstack11l11lll111_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1lll1111_opy_ = {
                bstack1ll1lll_opy_ (u"ࠣ࡭ࡨࡽࠧ៵"): bstack11l11l1llll_opy_,
                bstack1ll1lll_opy_ (u"ࠤࡷࡥ࡬ࡹࠢ៶"): PytestBDDFramework.__11l1ll11111_opy_(request.node, scenario),
                bstack1ll1lll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦ៷"): fixturedef,
                bstack1ll1lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ៸"): scope,
                bstack1ll1lll_opy_ (u"ࠧࡺࡹࡱࡧࠥ៹"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥ៺"), None)):
                    bstack11l1lll1111_opy_[bstack1ll1lll_opy_ (u"ࠢࡵࡻࡳࡩࠧ៻")] = TestFramework.bstack1l111l11lll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1lll1111_opy_[bstack1ll1lll_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ៼")] = uuid4().__str__()
                bstack11l1lll1111_opy_[PytestBDDFramework.bstack11l1lll11ll_opy_] = bstack11l11lll111_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1lll1111_opy_[PytestBDDFramework.bstack11l1l11l1l1_opy_] = bstack11l11lll111_opy_
            if bstack11l11l1llll_opy_ in bstack11l1l1111l1_opy_:
                bstack11l1l1111l1_opy_[bstack11l11l1llll_opy_].update(bstack11l1lll1111_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥ៽") + str(bstack11l1l1111l1_opy_[bstack11l11l1llll_opy_]) + bstack1ll1lll_opy_ (u"ࠥࠦ៾"))
            else:
                bstack11l1l1111l1_opy_[bstack11l11l1llll_opy_] = bstack11l1lll1111_opy_
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢ៿") + str(len(bstack11l1l1111l1_opy_)) + bstack1ll1lll_opy_ (u"ࠧࠨ᠀"))
        TestFramework.bstack1lll1111ll_opy_(instance, PytestBDDFramework.bstack11l11ll11ll_opy_, bstack11l1l1111l1_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᠁") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠢࠣ᠂"))
        return instance
    def __11l11ll1lll_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11llll1l_opy_.create_context(target)
        ob = bstack1l1l1lllll1_opy_(ctx, self.bstack1l11l1l11ll_opy_, self.bstack11l1l111111_opy_, test_framework_state)
        TestFramework.bstack11l1l1lllll_opy_(ob, {
            TestFramework.bstack1l11ll1l111_opy_: context.test_framework_name,
            TestFramework.bstack1l11111111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1l1l111l_opy_: [],
            PytestBDDFramework.bstack11l11ll11ll_opy_: {},
            PytestBDDFramework.bstack11l1l1lll1l_opy_: {},
            PytestBDDFramework.bstack11l11l1l1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1111ll_opy_(ob, TestFramework.bstack11l11l1ll1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1111ll_opy_(ob, TestFramework.bstack1l11l1ll11l_opy_, context.platform_index)
        TestFramework.bstack1111l1ll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣ᠃") + str(TestFramework.bstack1111l1ll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠤࠥ᠄"))
        return ob
    @staticmethod
    def __11l11llll1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭᠅"): id(step),
                bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ᠆"): step.name,
                bstack1ll1lll_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭᠇"): step.keyword,
            })
        meta = {
            bstack1ll1lll_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ᠈"): {
                bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᠉"): feature.name,
                bstack1ll1lll_opy_ (u"ࠨࡲࡤࡸ࡭࠭᠊"): feature.filename,
                bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ᠋"): feature.description
            },
            bstack1ll1lll_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ᠌"): {
                bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᠍"): scenario.name
            },
            bstack1ll1lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᠎"): steps,
            bstack1ll1lll_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨ᠏"): PytestBDDFramework.__11l1l1ll1l1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l11ll1l1l_opy_: meta
            }
        )
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᠐")
        global _1l11111llll_opy_
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᠑")]
        bstack1l1111lll1l_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), bstack11l11ll1111_opy_)
        if not os.path.exists(bstack1l1111lll1l_opy_) or not os.path.isdir(bstack1l1111lll1l_opy_):
            return
        logs = hook.get(bstack1ll1lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢ᠒"), [])
        with os.scandir(bstack1l1111lll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111llll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣ᠓").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1lll_opy_ (u"ࠦࠧ᠔")
                    log_entry = bstack1l1l11lll1l_opy_(
                        kind=bstack1ll1lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢ᠕"),
                        message=bstack1ll1lll_opy_ (u"ࠨࠢ᠖"),
                        level=bstack1ll1lll_opy_ (u"ࠢࠣ᠗"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1111llll1_opy_=entry.stat().st_size,
                        bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣ᠘"),
                        bstack111lll_opy_=os.path.abspath(entry.path),
                        bstack11l1ll11l1l_opy_=hook.get(TestFramework.bstack11l1l111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111llll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᠙")]
        bstack11l1l111ll1_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), bstack11l11ll1111_opy_, bstack11l1ll11ll1_opy_)
        if not os.path.exists(bstack11l1l111ll1_opy_) or not os.path.isdir(bstack11l1l111ll1_opy_):
            self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧ᠚").format(bstack11l1l111ll1_opy_))
        else:
            self.logger.info(bstack1ll1lll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥ᠛").format(bstack11l1l111ll1_opy_))
            with os.scandir(bstack11l1l111ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111llll_opy_:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ᠜").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1lll_opy_ (u"ࠨࠢ᠝")
                        log_entry = bstack1l1l11lll1l_opy_(
                            kind=bstack1ll1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᠞"),
                            message=bstack1ll1lll_opy_ (u"ࠣࠤ᠟"),
                            level=bstack1ll1lll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᠠ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1111llll1_opy_=entry.stat().st_size,
                            bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᠡ"),
                            bstack111lll_opy_=os.path.abspath(entry.path),
                            bstack1l1111lllll_opy_=hook.get(TestFramework.bstack11l1l111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111llll_opy_.add(abs_path)
        hook[bstack1ll1lll_opy_ (u"ࠦࡱࡵࡧࡴࠤᠢ")] = logs
    def bstack1l111ll11ll_opy_(
        self,
        bstack11llllll1l1_opy_: bstack1l1l1lllll1_opy_,
        entries: List[bstack1l1l11lll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᠣ"))
        req.platform_index = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11l1ll11l_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᠤ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack11llllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack11llllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack11llllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11ll1l111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.uuid = entry.bstack11l1ll11l1l_opy_ if entry.bstack11l1ll11l1l_opy_ else TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11ll11l1l_opy_)
            log_entry.test_framework_state = bstack11llllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᠥ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll1lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᠦ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1111llll1_opy_
                log_entry.file_path = entry.bstack111lll_opy_
        def bstack1l11111l1ll_opy_():
            bstack11lllll111_opy_ = datetime.now()
            try:
                self.bstack1l1llll1lll_opy_.LogCreatedEvent(req)
                bstack11llllll1l1_opy_.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᠧ"), datetime.now() - bstack11lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᠨ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l1111ll_opy_.enqueue(bstack1l11111l1ll_opy_)
    def __11l1ll1l11l_opy_(self, instance) -> None:
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᠩ")
        bstack11l11llll11_opy_ = {bstack1ll1lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᠪ"): bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()}
        TestFramework.bstack11l1l1lllll_opy_(instance, bstack11l11llll11_opy_)
    @staticmethod
    def __11l1ll11lll_opy_(instance, args):
        request, bstack11l1l11l1ll_opy_ = args
        bstack11l1l1l1l11_opy_ = id(bstack11l1l11l1ll_opy_)
        bstack11l1l111l11_opy_ = instance.data[TestFramework.bstack11l11ll1l1l_opy_]
        step = next(filter(lambda st: st[bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᠫ")] == bstack11l1l1l1l11_opy_, bstack11l1l111l11_opy_[bstack1ll1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᠬ")]), None)
        step.update({
            bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᠭ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11l1l111l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᠮ")]) if st[bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ᠯ")] == step[bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧᠰ")]), None)
        if index is not None:
            bstack11l1l111l11_opy_[bstack1ll1lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᠱ")][index] = step
        instance.data[TestFramework.bstack11l11ll1l1l_opy_] = bstack11l1l111l11_opy_
    @staticmethod
    def __11l11l1l1ll_opy_(instance, args):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᠲ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11l1l11l1ll_opy_ = args[1]
        bstack11l1l1l1l11_opy_ = id(bstack11l1l11l1ll_opy_)
        bstack11l1l111l11_opy_ = instance.data[TestFramework.bstack11l11ll1l1l_opy_]
        step = None
        if bstack11l1l1l1l11_opy_ is not None and bstack11l1l111l11_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᠳ")):
            step = next(filter(lambda st: st[bstack1ll1lll_opy_ (u"ࠨ࡫ࡧࠫᠴ")] == bstack11l1l1l1l11_opy_, bstack11l1l111l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᠵ")]), None)
            step.update({
                bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᠶ"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll1lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᠷ"): bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᠸ"),
                bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᠹ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᠺ"): bstack1ll1lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᠻ"),
                })
        index = next((i for i, st in enumerate(bstack11l1l111l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᠼ")]) if st[bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭ᠽ")] == step[bstack1ll1lll_opy_ (u"ࠫ࡮ࡪࠧᠾ")]), None)
        if index is not None:
            bstack11l1l111l11_opy_[bstack1ll1lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᠿ")][index] = step
        instance.data[TestFramework.bstack11l11ll1l1l_opy_] = bstack11l1l111l11_opy_
    @staticmethod
    def __11l1l1ll1l1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll1lll_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᡀ")):
                examples = list(node.callspec.params[bstack1ll1lll_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᡁ")].values())
            return examples
        except:
            return []
    def bstack1l1111ll1ll_opy_(self, instance: bstack1l1l1lllll1_opy_, bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1ll1llll_opy_ = (
            PytestBDDFramework.bstack11l11l1ll11_opy_
            if bstack1ll11l1l111_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1l11l11l_opy_
        )
        hook = PytestBDDFramework.bstack11l1l1l1lll_opy_(instance, bstack11l1ll1llll_opy_)
        entries = hook.get(TestFramework.bstack11l1lll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, []))
        return entries
    def bstack1l111l1ll11_opy_(self, instance: bstack1l1l1lllll1_opy_, bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1ll1llll_opy_ = (
            PytestBDDFramework.bstack11l11l1ll11_opy_
            if bstack1ll11l1l111_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1l11l11l_opy_
        )
        PytestBDDFramework.bstack11l1ll1111l_opy_(instance, bstack11l1ll1llll_opy_)
        TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, []).clear()
    @staticmethod
    def bstack11l1l1l1lll_opy_(instance: bstack1l1l1lllll1_opy_, bstack11l1ll1llll_opy_: str):
        bstack11l1ll1ll1l_opy_ = (
            PytestBDDFramework.bstack11l1l1lll1l_opy_
            if bstack11l1ll1llll_opy_ == PytestBDDFramework.bstack11l1l11l11l_opy_
            else PytestBDDFramework.bstack11l11l1l1l1_opy_
        )
        bstack11l1l1ll111_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1llll_opy_, None)
        bstack11l1l1l1l1l_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1ll1l_opy_, None) if bstack11l1l1ll111_opy_ else None
        return (
            bstack11l1l1l1l1l_opy_[bstack11l1l1ll111_opy_][-1]
            if isinstance(bstack11l1l1l1l1l_opy_, dict) and len(bstack11l1l1l1l1l_opy_.get(bstack11l1l1ll111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll1111l_opy_(instance: bstack1l1l1lllll1_opy_, bstack11l1ll1llll_opy_: str):
        hook = PytestBDDFramework.bstack11l1l1l1lll_opy_(instance, bstack11l1ll1llll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1lll1l1l_opy_, []).clear()
    @staticmethod
    def __11l1ll111l1_opy_(instance: bstack1l1l1lllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᡂ"), None)):
            return
        if os.getenv(bstack1ll1lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᡃ"), bstack1ll1lll_opy_ (u"ࠥ࠵ࠧᡄ")) != bstack1ll1lll_opy_ (u"ࠦ࠶ࠨᡅ"):
            PytestBDDFramework.logger.warning(bstack1ll1lll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᡆ"))
            return
        bstack11l1ll1lll1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᡇ"): (PytestBDDFramework.bstack11l11l1ll11_opy_, PytestBDDFramework.bstack11l11l1l1l1_opy_),
            bstack1ll1lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᡈ"): (PytestBDDFramework.bstack11l1l11l11l_opy_, PytestBDDFramework.bstack11l1l1lll1l_opy_),
        }
        for when in (bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᡉ"), bstack1ll1lll_opy_ (u"ࠤࡦࡥࡱࡲࠢᡊ"), bstack1ll1lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᡋ")):
            bstack11l11lll1l1_opy_ = args[1].get_records(when)
            if not bstack11l11lll1l1_opy_:
                continue
            records = [
                bstack1l1l11lll1l_opy_(
                    kind=TestFramework.bstack1l1111l1ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1lll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᡌ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1lll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᡍ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l11lll1l1_opy_
                if isinstance(getattr(r, bstack1ll1lll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᡎ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1ll1l1ll_opy_, bstack11l1ll1ll1l_opy_ = bstack11l1ll1lll1_opy_.get(when, (None, None))
            bstack11l1l11llll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1l1ll_opy_, None) if bstack11l1ll1l1ll_opy_ else None
            bstack11l1l1l1l1l_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1ll1l_opy_, None) if bstack11l1l11llll_opy_ else None
            if isinstance(bstack11l1l1l1l1l_opy_, dict) and len(bstack11l1l1l1l1l_opy_.get(bstack11l1l11llll_opy_, [])) > 0:
                hook = bstack11l1l1l1l1l_opy_[bstack11l1l11llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1lll1l1l_opy_ in hook:
                    hook[TestFramework.bstack11l1lll1l1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l11lllll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l1l1l1111_opy_(request.node, scenario)
        bstack11l1ll111ll_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l1ll111ll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l11ll11l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1lll111_opy_: test_id,
            TestFramework.bstack1l11lll1l1l_opy_: test_name,
            TestFramework.bstack11lll1lllll_opy_: test_id,
            TestFramework.bstack11l1ll1l1l1_opy_: bstack11l1ll111ll_opy_,
            TestFramework.bstack11l1ll1l111_opy_: PytestBDDFramework.__11l1ll11111_opy_(feature, scenario),
            TestFramework.bstack11l11lll11l_opy_: code,
            TestFramework.bstack11lll1111ll_opy_: TestFramework.bstack11l11l1lll1_opy_,
            TestFramework.bstack11ll11l1111_opy_: test_name
        }
    @staticmethod
    def __11l1l1l1111_opy_(node, scenario):
        if hasattr(node, bstack1ll1lll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᡏ")):
            parts = node.nodeid.rsplit(bstack1ll1lll_opy_ (u"ࠣ࡝ࠥᡐ"))
            params = parts[-1]
            return bstack1ll1lll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᡑ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l1ll11111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᡒ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll1lll_opy_ (u"ࠫࡹࡧࡧࡴࠩᡓ")) else [])
    @staticmethod
    def __11l11ll11l1_opy_(location):
        return bstack1ll1lll_opy_ (u"ࠧࡀ࠺ࠣᡔ").join(filter(lambda x: isinstance(x, str), location))