# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll11ll1l_opy_ import bstack1l1ll11l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l111111l1_opy_ import bstack111lllll111_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l1ll1ll_opy_,
    TestHookState,
    bstack1lll11l111l_opy_,
    bstack111l1111l_opy_,
)
import traceback
from bstack_utils.helper import bstack11ll11ll11l_opy_
from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll1ll1_opy_ import bstack1l1l111111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11l11_opy_ import bstack1l1lll11ll1_opy_
bstack11ll11l1ll1_opy_ = bstack11ll11ll11l_opy_()
bstack11lll11111l_opy_ = bstack1ll1l11_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᣥ")
bstack111ll1lll1l_opy_ = bstack1ll1l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᣦ")
bstack11l111l111l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᣧ")
bstack111lll1ll1l_opy_ = 1.0
_11ll1llllll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack111lll11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᣨ")
    bstack11l111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᣩ")
    bstack111llll1111_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᣪ")
    bstack11l11111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᣫ")
    bstack111lllll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᣬ")
    bstack111llll1l11_opy_: bool
    bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_  = None
    bstack111lll1111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1l1l1l111_opy_: Dict[str, str],
        bstack1l111llllll_opy_: List[str]=[bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᣭ")],
        bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_ = None,
        bstack1llll11l11_opy_=None
    ):
        super().__init__(bstack1l111llllll_opy_, bstack1l1l1l1l111_opy_, bstack1l1lll11l11_opy_)
        self.bstack111llll1l11_opy_ = any(bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᣮ") in item.lower() for item in bstack1l111llllll_opy_)
        self.bstack1llll11l11_opy_ = bstack1llll11l11_opy_
    def track_event(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack111lll1111l_opy_:
            bstack111lllll111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᣯ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠢࠣᣰ"))
            return
        if not self.bstack111llll1l11_opy_:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᣱ") + str(str(self.bstack1l111llllll_opy_)) + bstack1ll1l11_opy_ (u"ࠤࠥᣲ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᣳ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠦࠧᣴ"))
            return
        instance = self.__11l111ll11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᣵ") + str(args) + bstack1ll1l11_opy_ (u"ࠨࠢ᣶"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111lll1111l_opy_ and test_hook_state == TestHookState.PRE:
                bstack1l111ll1ll_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack1llllll11_opy_.value)
                name = str(EVENTS.bstack1llllll11_opy_.name)+bstack1ll1l11_opy_ (u"ࠢ࠻ࠤ᣷")+str(test_framework_state.name)
                TestFramework.bstack111llll1ll1_opy_(instance, name, bstack1l111ll1ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧ᣸").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1ll1llll_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111lll1l1l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᣹") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠥࠦ᣺"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l1ll11_opy_):
                    TestFramework.bstack1ll11l1ll_opy_(instance, TestFramework.bstack11ll1l1ll11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11l1111ll1l_opy_(instance, args)
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᣻") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠧࠨ᣼"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11lll1111ll_opy_):
                    TestFramework.bstack1ll11l1ll_opy_(instance, TestFramework.bstack11lll1111ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᣽") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠢࠣ᣾"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__11l111ll111_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__11l111l1lll_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__11l1111l11l_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lllll11l_opy_(instance, *args)
                self.__111llll1lll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack111lll1111l_opy_:
                self.__111lll1l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᣿") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠤࠥᤀ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111llllllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111lll1111l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack1llllll11_opy_.name)+bstack1ll1l11_opy_ (u"ࠥ࠾ࠧᤁ")+str(test_framework_state.name)
                bstack1l111ll1ll_opy_ = TestFramework.bstack111lllll1l1_opy_(instance, name)
                bstack11l1111l1l_opy_.end(EVENTS.bstack1llllll11_opy_.value, bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᤂ"), bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᤃ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᤄ").format(e))
    def bstack11ll1l11lll_opy_(self):
        return self.bstack111llll1l11_opy_
    def bstack11ll1lll1l1_opy_(self):
        return False
    def __111lll1llll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᤅ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11ll1l1111l_opy_(rep, [bstack1ll1l11_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᤆ"), bstack1ll1l11_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᤇ"), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᤈ"), bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᤉ"), bstack1ll1l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᤊ"), bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᤋ")])
        return None
    def __111lllll11l_opy_(self, instance: bstack1l11l1ll1ll_opy_, *args):
        result = self.__111lll1llll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1lll_opy_ = None
        if result.get(bstack1ll1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᤌ"), None) == bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᤍ") and len(args) > 1 and getattr(args[1], bstack1ll1l11_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᤎ"), None) is not None:
            failure = [{bstack1ll1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᤏ"): [args[1].excinfo.exconly(), result.get(bstack1ll1l11_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᤐ"), None)]}]
            bstack1ll111l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᤑ") if bstack1ll1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᤒ") in getattr(args[1].excinfo, bstack1ll1l11_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᤓ"), bstack1ll1l11_opy_ (u"ࠣࠤᤔ")) else bstack1ll1l11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᤕ")
        bstack11l1111l111_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᤖ"), TestFramework.bstack11l111l11ll_opy_)
        if bstack11l1111l111_opy_ != TestFramework.bstack11l111l11ll_opy_:
            TestFramework.bstack1ll11l1ll_opy_(instance, TestFramework.bstack11ll1lll1ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l111lll1l_opy_(instance, {
            TestFramework.bstack11l1ll11l1l_opy_: failure,
            TestFramework.bstack111llllll1l_opy_: bstack1ll111l1lll_opy_,
            TestFramework.bstack11l1ll1ll11_opy_: bstack11l1111l111_opy_,
        })
    def __11l111ll11l_opy_(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111llllll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1lll111_opy_ bstack11l111ll1l1_opy_ this to be bstack1ll1l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᤗ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111lll1l111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᤘ"), None), bstack1ll1l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᤙ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1l11_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᤚ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᤛ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll1l1l1l_opy_(target) if target else None
        return instance
    def __111lll1l11l_opy_(
        self,
        instance: bstack1l11l1ll1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l111l1ll1_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, PytestBDDFramework.bstack11l111111ll_opy_, {})
        if not key in bstack11l111l1ll1_opy_:
            bstack11l111l1ll1_opy_[key] = []
        bstack111lll11lll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, PytestBDDFramework.bstack111llll1111_opy_, {})
        if not key in bstack111lll11lll_opy_:
            bstack111lll11lll_opy_[key] = []
        bstack11l111lll11_opy_ = {
            PytestBDDFramework.bstack11l111111ll_opy_: bstack11l111l1ll1_opy_,
            PytestBDDFramework.bstack111llll1111_opy_: bstack111lll11lll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll1l11_opy_ (u"ࠤ࡮ࡩࡾࠨᤜ"): key,
                TestFramework.bstack111llll111l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1111llll_opy_: TestFramework.bstack11l1111l1l1_opy_,
                TestFramework.bstack111ll1llll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll1l1lll_opy_: [],
                TestFramework.bstack111ll1l11l1_opy_: hook_name,
                TestFramework.bstack11l1111111l_opy_: bstack1l1l111111l_opy_.bstack111lll1ll11_opy_()
            }
            bstack11l111l1ll1_opy_[key].append(hook)
            bstack11l111lll11_opy_[PytestBDDFramework.bstack11l11111l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l11111ll1_opy_ = bstack11l111l1ll1_opy_.get(key, [])
            hook = bstack11l11111ll1_opy_.pop() if bstack11l11111ll1_opy_ else None
            if hook:
                result = self.__111lll1llll_opy_(*args)
                if result:
                    bstack11l111l11l1_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᤝ"), TestFramework.bstack11l1111l1l1_opy_)
                    if bstack11l111l11l1_opy_ != TestFramework.bstack11l1111l1l1_opy_:
                        hook[TestFramework.bstack11l1111llll_opy_] = bstack11l111l11l1_opy_
                hook[TestFramework.bstack111llll11ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1111111l_opy_] = bstack1l1l111111l_opy_.bstack111lll1ll11_opy_()
                self.bstack111lll11l11_opy_(hook)
                logs = hook.get(TestFramework.bstack111lll111l1_opy_, [])
                self.bstack1l1ll1lll_opy_(instance, logs)
                bstack111lll11lll_opy_[key].append(hook)
                bstack11l111lll11_opy_[PytestBDDFramework.bstack111lllll1ll_opy_] = key
        TestFramework.bstack11l111lll1l_opy_(instance, bstack11l111lll11_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᤞ") + str(bstack111lll11lll_opy_) + bstack1ll1l11_opy_ (u"ࠧࠨ᤟"))
    def __111llllll11_opy_(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11ll1l1111l_opy_(args[0], [bstack1ll1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᤠ"), bstack1ll1l11_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᤡ"), bstack1ll1l11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᤢ"), bstack1ll1l11_opy_ (u"ࠤ࡬ࡨࡸࠨᤣ"), bstack1ll1l11_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᤤ"), bstack1ll1l11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᤥ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll1l11_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᤦ")) else fixturedef.get(bstack1ll1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᤧ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1l11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᤨ")) else None
        node = request.node if hasattr(request, bstack1ll1l11_opy_ (u"ࠣࡰࡲࡨࡪࠨᤩ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᤪ")) else None
        baseid = fixturedef.get(bstack1ll1l11_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᤫ"), None) or bstack1ll1l11_opy_ (u"ࠦࠧ᤬")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1l11_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥ᤭")):
            target = PytestBDDFramework.__11l111111l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣ᤮")) else None
            if target and not TestFramework.bstack1l1ll1l1l1l_opy_(target):
                self.__111lll1l111_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᤯") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠣࠤᤰ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᤱ") + str(target) + bstack1ll1l11_opy_ (u"ࠥࠦᤲ"))
            return None
        instance = TestFramework.bstack1l1ll1l1l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᤳ") + str(target) + bstack1ll1l11_opy_ (u"ࠧࠨᤴ"))
            return None
        bstack111ll1l1ll1_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, PytestBDDFramework.bstack111lll11l1l_opy_, {})
        if os.getenv(bstack1ll1l11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᤵ"), bstack1ll1l11_opy_ (u"ࠢ࠲ࠤᤶ")) == bstack1ll1l11_opy_ (u"ࠣ࠳ࠥᤷ"):
            bstack111ll1lllll_opy_ = bstack1ll1l11_opy_ (u"ࠤ࠽ࠦᤸ").join((scope, fixturename))
            bstack111ll1lll11_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11111l11_opy_ = {
                bstack1ll1l11_opy_ (u"ࠥ࡯ࡪࡿ᤹ࠢ"): bstack111ll1lllll_opy_,
                bstack1ll1l11_opy_ (u"ࠦࡹࡧࡧࡴࠤ᤺"): PytestBDDFramework.__111ll1ll11l_opy_(request.node, scenario),
                bstack1ll1l11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨ᤻"): fixturedef,
                bstack1ll1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ᤼"): scope,
                bstack1ll1l11_opy_ (u"ࠢࡵࡻࡳࡩࠧ᤽"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll1l11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧ᤾"), None)):
                    bstack11l11111l11_opy_[bstack1ll1l11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᤿")] = TestFramework.bstack11ll1ll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l11111l11_opy_[bstack1ll1l11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ᥀")] = uuid4().__str__()
                bstack11l11111l11_opy_[PytestBDDFramework.bstack111ll1llll1_opy_] = bstack111ll1lll11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11111l11_opy_[PytestBDDFramework.bstack111llll11ll_opy_] = bstack111ll1lll11_opy_
            if bstack111ll1lllll_opy_ in bstack111ll1l1ll1_opy_:
                bstack111ll1l1ll1_opy_[bstack111ll1lllll_opy_].update(bstack11l11111l11_opy_)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧ᥁") + str(bstack111ll1l1ll1_opy_[bstack111ll1lllll_opy_]) + bstack1ll1l11_opy_ (u"ࠧࠨ᥂"))
            else:
                bstack111ll1l1ll1_opy_[bstack111ll1lllll_opy_] = bstack11l11111l11_opy_
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤ᥃") + str(len(bstack111ll1l1ll1_opy_)) + bstack1ll1l11_opy_ (u"ࠢࠣ᥄"))
        TestFramework.bstack1ll11l1ll_opy_(instance, PytestBDDFramework.bstack111lll11l1l_opy_, bstack111ll1l1ll1_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣ᥅") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠤࠥ᥆"))
        return instance
    def __111lll1l111_opy_(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll11l1l1_opy_.create_context(target)
        ob = bstack1l11l1ll1ll_opy_(ctx, self.bstack1l111llllll_opy_, self.bstack1l1l1l1l111_opy_, test_framework_state)
        TestFramework.bstack11l111lll1l_opy_(ob, {
            TestFramework.bstack11llllll1l1_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11l1_opy_: context.test_framework_version,
            TestFramework.bstack111llll1l1l_opy_: [],
            PytestBDDFramework.bstack111lll11l1l_opy_: {},
            PytestBDDFramework.bstack111llll1111_opy_: {},
            PytestBDDFramework.bstack11l111111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll11l1ll_opy_(ob, TestFramework.bstack111ll1l1l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll11l1ll_opy_(ob, TestFramework.bstack1l111ll1l1l_opy_, context.platform_index)
        TestFramework.bstack11l111111_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥ᥇") + str(TestFramework.bstack11l111111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠦࠧ᥈"))
        return ob
    @staticmethod
    def __11l1111ll1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ᥉"): id(step),
                bstack1ll1l11_opy_ (u"࠭ࡴࡦࡺࡷࠫ᥊"): step.name,
                bstack1ll1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ᥋"): step.keyword,
            })
        meta = {
            bstack1ll1l11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ᥌"): {
                bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᥍"): feature.name,
                bstack1ll1l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ᥎"): feature.filename,
                bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ᥏"): feature.description
            },
            bstack1ll1l11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᥐ"): {
                bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᥑ"): scenario.name
            },
            bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᥒ"): steps,
            bstack1ll1l11_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᥓ"): PytestBDDFramework.__11l11111111_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack111ll1ll111_opy_: meta
            }
        )
    def bstack111lll11l11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᥔ")
        global _11ll1llllll_opy_
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᥕ")]
        bstack11ll11l1l11_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11lll11111l_opy_ + str(platform_index)), bstack111ll1lll1l_opy_)
        if not os.path.exists(bstack11ll11l1l11_opy_) or not os.path.isdir(bstack11ll11l1l11_opy_):
            return
        logs = hook.get(bstack1ll1l11_opy_ (u"ࠦࡱࡵࡧࡴࠤᥖ"), [])
        with os.scandir(bstack11ll11l1l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1llllll_opy_:
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᥗ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1l11_opy_ (u"ࠨࠢᥘ")
                    log_entry = bstack111l1111l_opy_(
                        kind=bstack1ll1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᥙ"),
                        message=bstack1ll1l11_opy_ (u"ࠣࠤᥚ"),
                        level=bstack1ll1l11_opy_ (u"ࠤࠥᥛ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11lll1l111l_opy_=entry.stat().st_size,
                        bstack11ll1l1l1l1_opy_=bstack1ll1l11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᥜ"),
                        bstack11ll_opy_=os.path.abspath(entry.path),
                        bstack11l111l1l11_opy_=hook.get(TestFramework.bstack111llll111l_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1llllll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᥝ")]
        bstack11l111l1l1l_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11lll11111l_opy_ + str(platform_index)), bstack111ll1lll1l_opy_, bstack11l111l111l_opy_)
        if not os.path.exists(bstack11l111l1l1l_opy_) or not os.path.isdir(bstack11l111l1l1l_opy_):
            self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᥞ").format(bstack11l111l1l1l_opy_))
        else:
            self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᥟ").format(bstack11l111l1l1l_opy_))
            with os.scandir(bstack11l111l1l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1llllll_opy_:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᥠ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1l11_opy_ (u"ࠣࠤᥡ")
                        log_entry = bstack111l1111l_opy_(
                            kind=bstack1ll1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᥢ"),
                            message=bstack1ll1l11_opy_ (u"ࠥࠦᥣ"),
                            level=bstack1ll1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᥤ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11lll1l111l_opy_=entry.stat().st_size,
                            bstack11ll1l1l1l1_opy_=bstack1ll1l11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᥥ"),
                            bstack11ll_opy_=os.path.abspath(entry.path),
                            bstack11ll1ll1l1l_opy_=hook.get(TestFramework.bstack111llll111l_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1llllll_opy_.add(abs_path)
        hook[bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᥦ")] = logs
    def bstack1l1ll1lll_opy_(
        self,
        bstack1l11lll11l_opy_: bstack1l11l1ll1ll_opy_,
        entries: List[bstack111l1111l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᥧ"))
        req.platform_index = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack1l111ll1l1l_opy_)
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᥨ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11lll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11lll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11lll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11llllll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11ll11l11l1_opy_)
            log_entry.uuid = entry.bstack11l111l1l11_opy_ if entry.bstack11l111l1l11_opy_ else TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack1l111l1lll1_opy_)
            log_entry.test_framework_state = bstack1l11lll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᥩ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll1l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᥪ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lll1l111l_opy_
                log_entry.file_path = entry.bstack11ll_opy_
        def bstack11ll1lll11l_opy_():
            bstack1l1l11llll_opy_ = datetime.now()
            try:
                self.bstack1llll11l11_opy_.LogCreatedEvent(req)
                bstack1l11lll11l_opy_.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᥫ"), datetime.now() - bstack1l1l11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᥬ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l11_opy_.enqueue(bstack11ll1lll11l_opy_)
    def __111llll1lll_opy_(self, instance) -> None:
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᥭ")
        bstack11l111lll11_opy_ = {bstack1ll1l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤ᥮"): bstack1l1l111111l_opy_.bstack111lll1ll11_opy_()}
        TestFramework.bstack11l111lll1l_opy_(instance, bstack11l111lll11_opy_)
    @staticmethod
    def __11l111ll111_opy_(instance, args):
        request, bstack111lll111ll_opy_ = args
        bstack11l1111l1ll_opy_ = id(bstack111lll111ll_opy_)
        bstack111ll1ll1l1_opy_ = instance.data[TestFramework.bstack111ll1ll111_opy_]
        step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫ᥯")] == bstack11l1111l1ll_opy_, bstack111ll1ll1l1_opy_[bstack1ll1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᥰ")]), None)
        step.update({
            bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᥱ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack111ll1ll1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᥲ")]) if st[bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨᥳ")] == step[bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩᥴ")]), None)
        if index is not None:
            bstack111ll1ll1l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᥵")][index] = step
        instance.data[TestFramework.bstack111ll1ll111_opy_] = bstack111ll1ll1l1_opy_
    @staticmethod
    def __11l111l1lll_opy_(instance, args):
        bstack1ll1l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡽࡨࡦࡰࠣࡰࡪࡴࠠࡢࡴࡪࡷࠥ࡯ࡳࠡ࠴࠯ࠤ࡮ࡺࠠࡴ࡫ࡪࡲ࡮࡬ࡩࡦࡵࠣࡸ࡭࡫ࡲࡦࠢ࡬ࡷࠥࡴ࡯ࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠲࡛ࠦࡳࡧࡴࡹࡪࡹࡴ࠭ࠢࡶࡸࡪࡶ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠴ࠢࡷ࡬ࡪࡴࠠࡵࡪࡨࠤࡱࡧࡳࡵࠢࡹࡥࡱࡻࡥࠡ࡫ࡶࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᥶")
        bstack1ll1l1ll1ll_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111lll111ll_opy_ = args[1]
        bstack11l1111l1ll_opy_ = id(bstack111lll111ll_opy_)
        bstack111ll1ll1l1_opy_ = instance.data[TestFramework.bstack111ll1ll111_opy_]
        step = None
        if bstack11l1111l1ll_opy_ is not None and bstack111ll1ll1l1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᥷")):
            step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭᥸")] == bstack11l1111l1ll_opy_, bstack111ll1ll1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᥹")]), None)
            step.update({
                bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᥺"): bstack1ll1l1ll1ll_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᥻"): bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᥼"),
                bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᥽"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᥾"): bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᥿"),
                })
        index = next((i for i, st in enumerate(bstack111ll1ll1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᦀ")]) if st[bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨᦁ")] == step[bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩᦂ")]), None)
        if index is not None:
            bstack111ll1ll1l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᦃ")][index] = step
        instance.data[TestFramework.bstack111ll1ll111_opy_] = bstack111ll1ll1l1_opy_
    @staticmethod
    def __11l11111111_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll1l11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᦄ")):
                examples = list(node.callspec.params[bstack1ll1l11_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᦅ")].values())
            return examples
        except:
            return []
    def bstack11ll1l1l1ll_opy_(self, instance: bstack1l11l1ll1ll_opy_, bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l111l1111_opy_ = (
            PytestBDDFramework.bstack11l11111l1l_opy_
            if bstack1l1ll1ll1ll_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111lllll1ll_opy_
        )
        hook = PytestBDDFramework.bstack11l1111lll1_opy_(instance, bstack11l111l1111_opy_)
        entries = hook.get(TestFramework.bstack111ll1l1lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack111llll1l1l_opy_, []))
        return entries
    def bstack11lll11ll1l_opy_(self, instance: bstack1l11l1ll1ll_opy_, bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l111l1111_opy_ = (
            PytestBDDFramework.bstack11l11111l1l_opy_
            if bstack1l1ll1ll1ll_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111lllll1ll_opy_
        )
        PytestBDDFramework.bstack11l11111lll_opy_(instance, bstack11l111l1111_opy_)
        TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack111llll1l1l_opy_, []).clear()
    @staticmethod
    def bstack11l1111lll1_opy_(instance: bstack1l11l1ll1ll_opy_, bstack11l111l1111_opy_: str):
        bstack111lllllll1_opy_ = (
            PytestBDDFramework.bstack111llll1111_opy_
            if bstack11l111l1111_opy_ == PytestBDDFramework.bstack111lllll1ll_opy_
            else PytestBDDFramework.bstack11l111111ll_opy_
        )
        bstack11l111ll1ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack11l111l1111_opy_, None)
        bstack111ll1l11ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack111lllllll1_opy_, None) if bstack11l111ll1ll_opy_ else None
        return (
            bstack111ll1l11ll_opy_[bstack11l111ll1ll_opy_][-1]
            if isinstance(bstack111ll1l11ll_opy_, dict) and len(bstack111ll1l11ll_opy_.get(bstack11l111ll1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l11111lll_opy_(instance: bstack1l11l1ll1ll_opy_, bstack11l111l1111_opy_: str):
        hook = PytestBDDFramework.bstack11l1111lll1_opy_(instance, bstack11l111l1111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll1l1lll_opy_, []).clear()
    @staticmethod
    def __11l1111l11l_opy_(instance: bstack1l11l1ll1ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᦆ"), None)):
            return
        if os.getenv(bstack1ll1l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᦇ"), bstack1ll1l11_opy_ (u"ࠧ࠷ࠢᦈ")) != bstack1ll1l11_opy_ (u"ࠨ࠱ࠣᦉ"):
            PytestBDDFramework.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᦊ"))
            return
        bstack111llll11l1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᦋ"): (PytestBDDFramework.bstack11l11111l1l_opy_, PytestBDDFramework.bstack11l111111ll_opy_),
            bstack1ll1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᦌ"): (PytestBDDFramework.bstack111lllll1ll_opy_, PytestBDDFramework.bstack111llll1111_opy_),
        }
        for when in (bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᦍ"), bstack1ll1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᦎ"), bstack1ll1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᦏ")):
            bstack111ll1l1l1l_opy_ = args[1].get_records(when)
            if not bstack111ll1l1l1l_opy_:
                continue
            records = [
                bstack111l1111l_opy_(
                    kind=TestFramework.bstack11lll11l111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1l11_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᦐ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1l11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᦑ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll1l1l1l_opy_
                if isinstance(getattr(r, bstack1ll1l11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᦒ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111lll1lll1_opy_, bstack111lllllll1_opy_ = bstack111llll11l1_opy_.get(when, (None, None))
            bstack111ll1ll1ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack111lll1lll1_opy_, None) if bstack111lll1lll1_opy_ else None
            bstack111ll1l11ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack111lllllll1_opy_, None) if bstack111ll1ll1ll_opy_ else None
            if isinstance(bstack111ll1l11ll_opy_, dict) and len(bstack111ll1l11ll_opy_.get(bstack111ll1ll1ll_opy_, [])) > 0:
                hook = bstack111ll1l11ll_opy_[bstack111ll1ll1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll1l1lll_opy_ in hook:
                    hook[TestFramework.bstack111ll1l1lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack111llll1l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll1l1l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__111lll11ll1_opy_(request.node, scenario)
        bstack111lll1l1ll_opy_ = feature.filename
        if not test_id or not test_name or not bstack111lll1l1ll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l111l1lll1_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll1llll_opy_: test_id,
            TestFramework.bstack1l111ll11l1_opy_: test_name,
            TestFramework.bstack11ll111ll11_opy_: test_id,
            TestFramework.bstack11l1111ll11_opy_: bstack111lll1l1ll_opy_,
            TestFramework.bstack111ll1l111l_opy_: PytestBDDFramework.__111ll1ll11l_opy_(feature, scenario),
            TestFramework.bstack111lll11111_opy_: code,
            TestFramework.bstack11l1ll1ll11_opy_: TestFramework.bstack11l111l11ll_opy_,
            TestFramework.bstack11l11l1l11l_opy_: test_name
        }
    @staticmethod
    def __111lll11ll1_opy_(node, scenario):
        if hasattr(node, bstack1ll1l11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᦓ")):
            parts = node.nodeid.rsplit(bstack1ll1l11_opy_ (u"ࠥ࡟ࠧᦔ"))
            params = parts[-1]
            return bstack1ll1l11_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᦕ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __111ll1ll11l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᦖ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll1l11_opy_ (u"࠭ࡴࡢࡩࡶࠫᦗ")) else [])
    @staticmethod
    def __11l111111l1_opy_(location):
        return bstack1ll1l11_opy_ (u"ࠢ࠻࠼ࠥᦘ").join(filter(lambda x: isinstance(x, str), location))