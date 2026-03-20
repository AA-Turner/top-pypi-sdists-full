# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11ll1111_opy_
from browserstack_sdk.sdk_cli.utils.bstack11111l1l1_opy_ import bstack11l1l1llll1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111l1111_opy_,
    TestHookState,
    bstack1ll1ll111ll_opy_,
    bstack1l1ll1111ll_opy_,
)
import traceback
from bstack_utils.helper import bstack11lllll1lll_opy_
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll111l1l11_opy_ import bstack1l1lll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
bstack1l1111l1lll_opy_ = bstack11lllll1lll_opy_()
bstack1l1111l11ll_opy_ = bstack11lll1_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤឆ")
bstack11l1lllll11_opy_ = bstack11lll1_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨជ")
bstack11l1lllll1l_opy_ = bstack11lll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥឈ")
bstack11l1ll11l11_opy_ = 1.0
_1l11111l1ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l11ll1ll1_opy_ = bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧញ")
    bstack11l1ll1ll11_opy_ = bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦដ")
    bstack11l1l111lll_opy_ = bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨឋ")
    bstack11l1ll1lll1_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥឌ")
    bstack11l1lll11l1_opy_ = bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧឍ")
    bstack11ll1111111_opy_: bool
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_  = None
    bstack11l1ll11l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1llll111_opy_: Dict[str, str],
        bstack1l11ll1l11l_opy_: List[str]=[bstack11lll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢណ")],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_ = None,
        bstack1l1lll11l11_opy_=None
    ):
        super().__init__(bstack1l11ll1l11l_opy_, bstack11l1llll111_opy_, bstack1ll1l11l1l1_opy_)
        self.bstack11ll1111111_opy_ = any(bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣត") in item.lower() for item in bstack1l11ll1l11l_opy_)
        self.bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_
    def track_event(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack11l1ll11l1l_opy_:
            bstack11l1l1llll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack11lll1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨថ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠨࠢទ"))
            return
        if not self.bstack11ll1111111_opy_:
            self.logger.warning(bstack11lll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣធ") + str(str(self.bstack1l11ll1l11l_opy_)) + bstack11lll1_opy_ (u"ࠣࠤន"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11lll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦប") + str(kwargs) + bstack11lll1_opy_ (u"ࠥࠦផ"))
            return
        instance = self.__11l1l11llll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥព") + str(args) + bstack11lll1_opy_ (u"ࠧࠨភ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll11l1l_opy_ and test_hook_state == TestHookState.PRE:
                bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1ll111111l_opy_.value)
                name = str(EVENTS.bstack1ll111111l_opy_.name)+bstack11lll1_opy_ (u"ࠨ࠺ࠣម")+str(test_framework_state.name)
                TestFramework.bstack11l1l1lll11_opy_(instance, name, bstack11lllll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦយ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11lll111lll_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11l1ll111l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11lll1_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣរ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠤࠥល"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1llll_opy_):
                    TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1llll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1l1111l1_opy_(instance, args)
                    self.logger.debug(bstack11lll1_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣវ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠦࠧឝ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1111l_opy_):
                    TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lll1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣឞ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠨࠢស"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11ll11111l1_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l1l11111l_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1l1l1lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l1l1l1l_opy_(instance, *args)
                self.__11l11lll1l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1ll11l1l_opy_:
                self.__11l1l1ll111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣហ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠣࠤឡ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll11l1l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1ll111111l_opy_.name)+bstack11lll1_opy_ (u"ࠤ࠽ࠦអ")+str(test_framework_state.name)
                bstack11lllll1_opy_ = TestFramework.bstack11l1l1l1l11_opy_(instance, name)
                bstack1llll11l_opy_.end(EVENTS.bstack1ll111111l_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥឣ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤឤ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧឥ").format(e))
    def bstack1l111ll1l11_opy_(self):
        return self.bstack11ll1111111_opy_
    def bstack11lllll1l1l_opy_(self):
        return False
    def __11l1ll11lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11lll1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥឦ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1111ll111_opy_(rep, [bstack11lll1_opy_ (u"ࠢࡸࡪࡨࡲࠧឧ"), bstack11lll1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤឨ"), bstack11lll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤឩ"), bstack11lll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥឪ"), bstack11lll1_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧឫ"), bstack11lll1_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦឬ")])
        return None
    def __11l1l1l1l1l_opy_(self, instance: bstack1ll111l1111_opy_, *args):
        result = self.__11l1ll11lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lllll11_opy_ = None
        if result.get(bstack11lll1_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢឭ"), None) == bstack11lll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢឮ") and len(args) > 1 and getattr(args[1], bstack11lll1_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤឯ"), None) is not None:
            failure = [{bstack11lll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬឰ"): [args[1].excinfo.exconly(), result.get(bstack11lll1_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤឱ"), None)]}]
            bstack1ll1lllll11_opy_ = bstack11lll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧឲ") if bstack11lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣឳ") in getattr(args[1].excinfo, bstack11lll1_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣ឴"), bstack11lll1_opy_ (u"ࠢࠣ឵")) else bstack11lll1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤា")
        bstack11l11lllll1_opy_ = result.get(bstack11lll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥិ"), TestFramework.bstack11l11ll1lll_opy_)
        if bstack11l11lllll1_opy_ != TestFramework.bstack11l11ll1lll_opy_:
            TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1ll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l11lll1_opy_(instance, {
            TestFramework.bstack11lll1l1111_opy_: failure,
            TestFramework.bstack11l11llll11_opy_: bstack1ll1lllll11_opy_,
            TestFramework.bstack11lll11111l_opy_: bstack11l11lllll1_opy_,
        })
    def __11l1l11llll_opy_(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l1l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l1111l1l11_opy_ bstack11l1lll111l_opy_ this to be bstack11lll1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥី")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l1l11l11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack11lll1_opy_ (u"ࠦࡳࡵࡤࡦࠤឹ"), None), bstack11lll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧឺ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11lll1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦុ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11lll1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢូ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll11l11l11_opy_(target) if target else None
        return instance
    def __11l1l1ll111_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1llll11l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, PytestBDDFramework.bstack11l1ll1ll11_opy_, {})
        if not key in bstack11l1llll11l_opy_:
            bstack11l1llll11l_opy_[key] = []
        bstack11l1l111l1l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, PytestBDDFramework.bstack11l1l111lll_opy_, {})
        if not key in bstack11l1l111l1l_opy_:
            bstack11l1l111l1l_opy_[key] = []
        bstack11l1l1lll1l_opy_ = {
            PytestBDDFramework.bstack11l1ll1ll11_opy_: bstack11l1llll11l_opy_,
            PytestBDDFramework.bstack11l1l111lll_opy_: bstack11l1l111l1l_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11lll1_opy_ (u"ࠣ࡭ࡨࡽࠧួ"): key,
                TestFramework.bstack11l1l1ll11l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1ll1l_opy_: TestFramework.bstack11l1l111ll1_opy_,
                TestFramework.bstack11l1ll1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1llllll1_opy_: [],
                TestFramework.bstack11l1lll11ll_opy_: hook_name,
                TestFramework.bstack11l1l1l1111_opy_: bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()
            }
            bstack11l1llll11l_opy_[key].append(hook)
            bstack11l1l1lll1l_opy_[PytestBDDFramework.bstack11l1ll1lll1_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1llll_opy_ = bstack11l1llll11l_opy_.get(key, [])
            hook = bstack11l1ll1llll_opy_.pop() if bstack11l1ll1llll_opy_ else None
            if hook:
                result = self.__11l1ll11lll_opy_(*args)
                if result:
                    bstack11l1l1l11ll_opy_ = result.get(bstack11lll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥើ"), TestFramework.bstack11l1l111ll1_opy_)
                    if bstack11l1l1l11ll_opy_ != TestFramework.bstack11l1l111ll1_opy_:
                        hook[TestFramework.bstack11l1ll1ll1l_opy_] = bstack11l1l1l11ll_opy_
                hook[TestFramework.bstack11l1l1l11l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1111_opy_] = bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()
                self.bstack11l1ll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1l1ll1l1_opy_, [])
                self.bstack11lllll1ll1_opy_(instance, logs)
                bstack11l1l111l1l_opy_[key].append(hook)
                bstack11l1l1lll1l_opy_[PytestBDDFramework.bstack11l1lll11l1_opy_] = key
        TestFramework.bstack11l1l11lll1_opy_(instance, bstack11l1l1lll1l_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤឿ") + str(bstack11l1l111l1l_opy_) + bstack11lll1_opy_ (u"ࠦࠧៀ"))
    def __11l1l1lllll_opy_(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1111ll111_opy_(args[0], [bstack11lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦេ"), bstack11lll1_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢែ"), bstack11lll1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢៃ"), bstack11lll1_opy_ (u"ࠣ࡫ࡧࡷࠧោ"), bstack11lll1_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦៅ"), bstack11lll1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥំ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11lll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥះ")) else fixturedef.get(bstack11lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦៈ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11lll1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦ៉")) else None
        node = request.node if hasattr(request, bstack11lll1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧ៊")) else None
        target = request.node.nodeid if hasattr(node, bstack11lll1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ់")) else None
        baseid = fixturedef.get(bstack11lll1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤ៌"), None) or bstack11lll1_opy_ (u"ࠥࠦ៍")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11lll1_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤ៎")):
            target = PytestBDDFramework.__11l1ll1l1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11lll1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢ៏")) else None
            if target and not TestFramework.bstack1ll11l11l11_opy_(target):
                self.__11l1l11l11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11lll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣ័") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠢࠣ៑"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11lll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨ្") + str(target) + bstack11lll1_opy_ (u"ࠤࠥ៓"))
            return None
        instance = TestFramework.bstack1ll11l11l11_opy_(target)
        if not instance:
            self.logger.warning(bstack11lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧ។") + str(target) + bstack11lll1_opy_ (u"ࠦࠧ៕"))
            return None
        bstack11l1l11l1ll_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, PytestBDDFramework.bstack11l11ll1ll1_opy_, {})
        if os.getenv(bstack11lll1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨ៖"), bstack11lll1_opy_ (u"ࠨ࠱ࠣៗ")) == bstack11lll1_opy_ (u"ࠢ࠲ࠤ៘"):
            bstack11l11ll1l1l_opy_ = bstack11lll1_opy_ (u"ࠣ࠼ࠥ៙").join((scope, fixturename))
            bstack11l1l1111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1ll11111_opy_ = {
                bstack11lll1_opy_ (u"ࠤ࡮ࡩࡾࠨ៚"): bstack11l11ll1l1l_opy_,
                bstack11lll1_opy_ (u"ࠥࡸࡦ࡭ࡳࠣ៛"): PytestBDDFramework.__11ll111111l_opy_(request.node, scenario),
                bstack11lll1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧៜ"): fixturedef,
                bstack11lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦ៝"): scope,
                bstack11lll1_opy_ (u"ࠨࡴࡺࡲࡨࠦ៞"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack11lll1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦ៟"), None)):
                    bstack11l1ll11111_opy_[bstack11lll1_opy_ (u"ࠣࡶࡼࡴࡪࠨ០")] = TestFramework.bstack1l1111lll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1ll11111_opy_[bstack11lll1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ១")] = uuid4().__str__()
                bstack11l1ll11111_opy_[PytestBDDFramework.bstack11l1ll1l1ll_opy_] = bstack11l1l1111ll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1ll11111_opy_[PytestBDDFramework.bstack11l1l1l11l1_opy_] = bstack11l1l1111ll_opy_
            if bstack11l11ll1l1l_opy_ in bstack11l1l11l1ll_opy_:
                bstack11l1l11l1ll_opy_[bstack11l11ll1l1l_opy_].update(bstack11l1ll11111_opy_)
                self.logger.debug(bstack11lll1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦ២") + str(bstack11l1l11l1ll_opy_[bstack11l11ll1l1l_opy_]) + bstack11lll1_opy_ (u"ࠦࠧ៣"))
            else:
                bstack11l1l11l1ll_opy_[bstack11l11ll1l1l_opy_] = bstack11l1ll11111_opy_
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣ៤") + str(len(bstack11l1l11l1ll_opy_)) + bstack11lll1_opy_ (u"ࠨࠢ៥"))
        TestFramework.bstack1ll1ll1l1l_opy_(instance, PytestBDDFramework.bstack11l11ll1ll1_opy_, bstack11l1l11l1ll_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ៦") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠣࠤ៧"))
        return instance
    def __11l1l11l11l_opy_(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11ll1111_opy_.create_context(target)
        ob = bstack1ll111l1111_opy_(ctx, self.bstack1l11ll1l11l_opy_, self.bstack11l1llll111_opy_, test_framework_state)
        TestFramework.bstack11l1l11lll1_opy_(ob, {
            TestFramework.bstack1l11lll111l_opy_: context.test_framework_name,
            TestFramework.bstack1l111l11lll_opy_: context.test_framework_version,
            TestFramework.bstack11l1l11ll1l_opy_: [],
            PytestBDDFramework.bstack11l11ll1ll1_opy_: {},
            PytestBDDFramework.bstack11l1l111lll_opy_: {},
            PytestBDDFramework.bstack11l1ll1ll11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1ll1l1l_opy_(ob, TestFramework.bstack11l11lll11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1ll1l1l_opy_(ob, TestFramework.bstack1l11lll1ll1_opy_, context.platform_index)
        TestFramework.bstack11l1lll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11lll1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤ៨") + str(TestFramework.bstack11l1lll111_opy_.keys()) + bstack11lll1_opy_ (u"ࠥࠦ៩"))
        return ob
    @staticmethod
    def __11l1l1111l1_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lll1_opy_ (u"ࠫ࡮ࡪࠧ៪"): id(step),
                bstack11lll1_opy_ (u"ࠬࡺࡥࡹࡶࠪ៫"): step.name,
                bstack11lll1_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ៬"): step.keyword,
            })
        meta = {
            bstack11lll1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ៭"): {
                bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭៮"): feature.name,
                bstack11lll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ៯"): feature.filename,
                bstack11lll1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ៰"): feature.description
            },
            bstack11lll1_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭៱"): {
                bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ៲"): scenario.name
            },
            bstack11lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ៳"): steps,
            bstack11lll1_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩ៴"): PytestBDDFramework.__11l1lll1l1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11l1lll1l11_opy_: meta
            }
        )
    def bstack11l1ll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11lll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ៵")
        global _1l11111l1ll_opy_
        platform_index = os.environ[bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ៶")]
        bstack1l1111l111l_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), bstack11l1lllll11_opy_)
        if not os.path.exists(bstack1l1111l111l_opy_) or not os.path.isdir(bstack1l1111l111l_opy_):
            return
        logs = hook.get(bstack11lll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ៷"), [])
        with os.scandir(bstack1l1111l111l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111l1ll_opy_:
                    self.logger.info(bstack11lll1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤ៸").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11lll1_opy_ (u"ࠧࠨ៹")
                    log_entry = bstack1l1ll1111ll_opy_(
                        kind=bstack11lll1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ៺"),
                        message=bstack11lll1_opy_ (u"ࠢࠣ៻"),
                        level=bstack11lll1_opy_ (u"ࠣࠤ៼"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11111111l_opy_=entry.stat().st_size,
                        bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ៽"),
                        bstack11111l1_opy_=os.path.abspath(entry.path),
                        bstack11l1l11ll11_opy_=hook.get(TestFramework.bstack11l1l1ll11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111l1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ៾")]
        bstack11l1lll1lll_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), bstack11l1lllll11_opy_, bstack11l1lllll1l_opy_)
        if not os.path.exists(bstack11l1lll1lll_opy_) or not os.path.isdir(bstack11l1lll1lll_opy_):
            self.logger.info(bstack11lll1_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨ៿").format(bstack11l1lll1lll_opy_))
        else:
            self.logger.info(bstack11lll1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦ᠀").format(bstack11l1lll1lll_opy_))
            with os.scandir(bstack11l1lll1lll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack11lll1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦ᠁").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11lll1_opy_ (u"ࠢࠣ᠂")
                        log_entry = bstack1l1ll1111ll_opy_(
                            kind=bstack11lll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᠃"),
                            message=bstack11lll1_opy_ (u"ࠤࠥ᠄"),
                            level=bstack11lll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ᠅"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11111111l_opy_=entry.stat().st_size,
                            bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᠆"),
                            bstack11111l1_opy_=os.path.abspath(entry.path),
                            bstack1l111l111ll_opy_=hook.get(TestFramework.bstack11l1l1ll11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111l1ll_opy_.add(abs_path)
        hook[bstack11lll1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥ᠇")] = logs
    def bstack11lllll1ll1_opy_(
        self,
        bstack1l1111lllll_opy_: bstack1ll111l1111_opy_,
        entries: List[bstack1l1ll1111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11lll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥ᠈"))
        req.platform_index = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll1ll1_opy_)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ᠉").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111lllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111lllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111lllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l111l11lll_opy_)
            log_entry.uuid = entry.bstack11l1l11ll11_opy_ if entry.bstack11l1l11ll11_opy_ else TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11llll11l_opy_)
            log_entry.test_framework_state = bstack1l1111lllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᠊"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11lll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᠋"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11111111l_opy_
                log_entry.file_path = entry.bstack11111l1_opy_
        def bstack1l111111ll1_opy_():
            bstack111ll1l1_opy_ = datetime.now()
            try:
                self.bstack1l1lll11l11_opy_.LogCreatedEvent(req)
                bstack1l1111lllll_opy_.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ᠌"), datetime.now() - bstack111ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥ᠍").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l111111ll1_opy_)
    def __11l11lll1l1_opy_(self, instance) -> None:
        bstack11lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᠎")
        bstack11l1l1lll1l_opy_ = {bstack11lll1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣ᠏"): bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()}
        TestFramework.bstack11l1l11lll1_opy_(instance, bstack11l1l1lll1l_opy_)
    @staticmethod
    def __11ll11111l1_opy_(instance, args):
        request, bstack11l11lll111_opy_ = args
        bstack11l1llll1l1_opy_ = id(bstack11l11lll111_opy_)
        bstack11l1lll1ll1_opy_ = instance.data[TestFramework.bstack11l1lll1l11_opy_]
        step = next(filter(lambda st: st[bstack11lll1_opy_ (u"ࠧࡪࡦࠪ᠐")] == bstack11l1llll1l1_opy_, bstack11l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᠑")]), None)
        step.update({
            bstack11lll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᠒"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᠓")]) if st[bstack11lll1_opy_ (u"ࠫ࡮ࡪࠧ᠔")] == step[bstack11lll1_opy_ (u"ࠬ࡯ࡤࠨ᠕")]), None)
        if index is not None:
            bstack11l1lll1ll1_opy_[bstack11lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᠖")][index] = step
        instance.data[TestFramework.bstack11l1lll1l11_opy_] = bstack11l1lll1ll1_opy_
    @staticmethod
    def __11l1l11111l_opy_(instance, args):
        bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡮ࡥ࡯ࠢ࡯ࡩࡳࠦࡡࡳࡩࡶࠤ࡮ࡹࠠ࠳࠮ࠣ࡭ࡹࠦࡳࡪࡩࡱ࡭࡫࡯ࡥࡴࠢࡷ࡬ࡪࡸࡥࠡ࡫ࡶࠤࡳࡵࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠱ࠥࡡࡲࡦࡳࡸࡩࡸࡺࠬࠡࡵࡷࡩࡵࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠳ࠡࡶ࡫ࡩࡳࠦࡴࡩࡧࠣࡰࡦࡹࡴࠡࡸࡤࡰࡺ࡫ࠠࡪࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᠗")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11l11lll111_opy_ = args[1]
        bstack11l1llll1l1_opy_ = id(bstack11l11lll111_opy_)
        bstack11l1lll1ll1_opy_ = instance.data[TestFramework.bstack11l1lll1l11_opy_]
        step = None
        if bstack11l1llll1l1_opy_ is not None and bstack11l1lll1ll1_opy_.get(bstack11lll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᠘")):
            step = next(filter(lambda st: st[bstack11lll1_opy_ (u"ࠩ࡬ࡨࠬ᠙")] == bstack11l1llll1l1_opy_, bstack11l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᠚")]), None)
            step.update({
                bstack11lll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᠛"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11lll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᠜"): bstack11lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᠝"),
                bstack11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ᠞"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11lll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᠟"): bstack11lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᠠ"),
                })
        index = next((i for i, st in enumerate(bstack11l1lll1ll1_opy_[bstack11lll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᠡ")]) if st[bstack11lll1_opy_ (u"ࠫ࡮ࡪࠧᠢ")] == step[bstack11lll1_opy_ (u"ࠬ࡯ࡤࠨᠣ")]), None)
        if index is not None:
            bstack11l1lll1ll1_opy_[bstack11lll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᠤ")][index] = step
        instance.data[TestFramework.bstack11l1lll1l11_opy_] = bstack11l1lll1ll1_opy_
    @staticmethod
    def __11l1lll1l1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11lll1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᠥ")):
                examples = list(node.callspec.params[bstack11lll1_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᠦ")].values())
            return examples
        except:
            return []
    def bstack1l1111111l1_opy_(self, instance: bstack1ll111l1111_opy_, bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1l111l_opy_ = (
            PytestBDDFramework.bstack11l1ll1lll1_opy_
            if bstack1ll1l111111_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1lll11l1_opy_
        )
        hook = PytestBDDFramework.bstack11l1ll1111l_opy_(instance, bstack11l1l1l111l_opy_)
        entries = hook.get(TestFramework.bstack11l1llllll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, []))
        return entries
    def bstack1l1111llll1_opy_(self, instance: bstack1ll111l1111_opy_, bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1l111l_opy_ = (
            PytestBDDFramework.bstack11l1ll1lll1_opy_
            if bstack1ll1l111111_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack11l1lll11l1_opy_
        )
        PytestBDDFramework.bstack11l1l1l1ll1_opy_(instance, bstack11l1l1l111l_opy_)
        TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, []).clear()
    @staticmethod
    def bstack11l1ll1111l_opy_(instance: bstack1ll111l1111_opy_, bstack11l1l1l111l_opy_: str):
        bstack11l11llll1l_opy_ = (
            PytestBDDFramework.bstack11l1l111lll_opy_
            if bstack11l1l1l111l_opy_ == PytestBDDFramework.bstack11l1lll11l1_opy_
            else PytestBDDFramework.bstack11l1ll1ll11_opy_
        )
        bstack11l1llll1ll_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack11l1l1l111l_opy_, None)
        bstack11l1l111111_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack11l11llll1l_opy_, None) if bstack11l1llll1ll_opy_ else None
        return (
            bstack11l1l111111_opy_[bstack11l1llll1ll_opy_][-1]
            if isinstance(bstack11l1l111111_opy_, dict) and len(bstack11l1l111111_opy_.get(bstack11l1llll1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1l1l1ll1_opy_(instance: bstack1ll111l1111_opy_, bstack11l1l1l111l_opy_: str):
        hook = PytestBDDFramework.bstack11l1ll1111l_opy_(instance, bstack11l1l1l111l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1llllll1_opy_, []).clear()
    @staticmethod
    def __11l1l1l1lll_opy_(instance: bstack1ll111l1111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11lll1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᠧ"), None)):
            return
        if os.getenv(bstack11lll1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᠨ"), bstack11lll1_opy_ (u"ࠦ࠶ࠨᠩ")) != bstack11lll1_opy_ (u"ࠧ࠷ࠢᠪ"):
            PytestBDDFramework.logger.warning(bstack11lll1_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᠫ"))
            return
        bstack11l1l11l1l1_opy_ = {
            bstack11lll1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᠬ"): (PytestBDDFramework.bstack11l1ll1lll1_opy_, PytestBDDFramework.bstack11l1ll1ll11_opy_),
            bstack11lll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᠭ"): (PytestBDDFramework.bstack11l1lll11l1_opy_, PytestBDDFramework.bstack11l1l111lll_opy_),
        }
        for when in (bstack11lll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᠮ"), bstack11lll1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᠯ"), bstack11lll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᠰ")):
            bstack11l11lll1ll_opy_ = args[1].get_records(when)
            if not bstack11l11lll1ll_opy_:
                continue
            records = [
                bstack1l1ll1111ll_opy_(
                    kind=TestFramework.bstack11lllll1l11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11lll1_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᠱ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11lll1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᠲ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l11lll1ll_opy_
                if isinstance(getattr(r, bstack11lll1_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᠳ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1ll11ll1_opy_, bstack11l11llll1l_opy_ = bstack11l1l11l1l1_opy_.get(when, (None, None))
            bstack11l1lllllll_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack11l1ll11ll1_opy_, None) if bstack11l1ll11ll1_opy_ else None
            bstack11l1l111111_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack11l11llll1l_opy_, None) if bstack11l1lllllll_opy_ else None
            if isinstance(bstack11l1l111111_opy_, dict) and len(bstack11l1l111111_opy_.get(bstack11l1lllllll_opy_, [])) > 0:
                hook = bstack11l1l111111_opy_[bstack11l1lllllll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1llllll1_opy_ in hook:
                    hook[TestFramework.bstack11l1llllll1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l1ll111l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__11l1l11l111_opy_(request.node, scenario)
        bstack11l11llllll_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l11llllll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l11llll11l_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111lll_opy_: test_id,
            TestFramework.bstack1l11ll1llll_opy_: test_name,
            TestFramework.bstack11lllll1111_opy_: test_id,
            TestFramework.bstack11l1lll1111_opy_: bstack11l11llllll_opy_,
            TestFramework.bstack11l1ll1l11l_opy_: PytestBDDFramework.__11ll111111l_opy_(feature, scenario),
            TestFramework.bstack11l1l111l11_opy_: code,
            TestFramework.bstack11lll11111l_opy_: TestFramework.bstack11l11ll1lll_opy_,
            TestFramework.bstack11ll11ll11l_opy_: test_name
        }
    @staticmethod
    def __11l1l11l111_opy_(node, scenario):
        if hasattr(node, bstack11lll1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᠴ")):
            parts = node.nodeid.rsplit(bstack11lll1_opy_ (u"ࠤ࡞ࠦᠵ"))
            params = parts[-1]
            return bstack11lll1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᠶ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll111111l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11lll1_opy_ (u"ࠫࡹࡧࡧࡴࠩᠷ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11lll1_opy_ (u"ࠬࡺࡡࡨࡵࠪᠸ")) else [])
    @staticmethod
    def __11l1ll1l1l1_opy_(location):
        return bstack11lll1_opy_ (u"ࠨ࠺࠻ࠤᠹ").join(filter(lambda x: isinstance(x, str), location))