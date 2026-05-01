# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1l1lll_opy_ import bstack1l1ll1l1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1llllll_opy_ import bstack111ll1ll1l1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1ll11l1_opy_,
    TestHookState,
    bstack1ll1lllll1l_opy_,
    bstack11l1l1l1ll_opy_,
)
import traceback
from bstack_utils.helper import bstack11ll11l1lll_opy_
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1l11ll1l1_opy_ import bstack1l11ll1111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1lll1111l_opy_
bstack11ll11l1ll1_opy_ = bstack11ll11l1lll_opy_()
bstack11ll1ll1l11_opy_ = bstack111ll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᤒ")
bstack111lllll111_opy_ = bstack111ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᤓ")
bstack111lll11l11_opy_ = bstack111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᤔ")
bstack111llll1l1l_opy_ = 1.0
_11ll111lll1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack111lll1l11l_opy_ = bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᤕ")
    bstack111ll1l1ll1_opy_ = bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᤖ")
    bstack111lll11l1l_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᤗ")
    bstack111lllll11l_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᤘ")
    bstack111llll1ll1_opy_ = bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᤙ")
    bstack11l1111ll1l_opy_: bool
    bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_  = None
    bstack111llll111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll11l_opy_: Dict[str, str],
        bstack1l1l11l1111_opy_: List[str]=[bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᤚ")],
        bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_ = None,
        bstack111111ll1l_opy_=None
    ):
        super().__init__(bstack1l1l11l1111_opy_, bstack1l11llll11l_opy_, bstack1l1ll1llll1_opy_)
        self.bstack11l1111ll1l_opy_ = any(bstack111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᤛ") in item.lower() for item in bstack1l1l11l1111_opy_)
        self.bstack111111ll1l_opy_ = bstack111111ll1l_opy_
    def track_event(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in PytestBDDFramework.bstack111llll111l_opy_:
            bstack111ll1ll1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᤜ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠥࠦᤝ"))
            return
        if not self.bstack11l1111ll1l_opy_:
            self.logger.warning(bstack111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᤞ") + str(str(self.bstack1l1l11l1111_opy_)) + bstack111ll_opy_ (u"ࠧࠨ᤟"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᤠ") + str(kwargs) + bstack111ll_opy_ (u"ࠢࠣᤡ"))
            return
        instance = self.__11l11111lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᤢ") + str(args) + bstack111ll_opy_ (u"ࠤࠥᤣ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111llll111l_opy_ and test_hook_state == TestHookState.PRE:
                bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack11l111111l_opy_.value)
                name = str(EVENTS.bstack11l111111l_opy_.name)+bstack111ll_opy_ (u"ࠥ࠾ࠧᤤ")+str(test_framework_state.name)
                TestFramework.bstack111ll1l1l1l_opy_(instance, name, bstack11111l11l_opy_)
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᤥ").format(e))
        try:
            if test_framework_state == TestFrameworkState.TEST:
                if not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_) and test_hook_state == TestHookState.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__111lll11111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack111ll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᤦ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠨࠢᤧ"))
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__111ll1lll11_opy_(instance, args)
                    self.logger.debug(bstack111ll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᤨ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠣࠤᤩ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11llll_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11lll11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᤪ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠥࠦᤫ"))
            elif test_framework_state == TestFrameworkState.STEP:
                if test_hook_state == TestHookState.PRE:
                    PytestBDDFramework.__111llll1lll_opy_(instance, args)
                elif test_hook_state == TestHookState.POST:
                    PytestBDDFramework.__111ll1l111l_opy_(instance, args)
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                PytestBDDFramework.__111lll1ll11_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111ll1ll111_opy_(instance, *args)
                self.__111llll11l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack111llll111l_opy_:
                self.__111ll11l1l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ᤬") + str(instance.ref()) + bstack111ll_opy_ (u"ࠧࠨ᤭"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111ll1l1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack111llll111l_opy_ and test_hook_state == TestHookState.POST:
                name = str(EVENTS.bstack11l111111l_opy_.name)+bstack111ll_opy_ (u"ࠨ࠺ࠣ᤮")+str(test_framework_state.name)
                bstack11111l11l_opy_ = TestFramework.bstack111ll1lllll_opy_(instance, name)
                bstack111l1l1l_opy_.end(EVENTS.bstack11l111111l_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᤯"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᤰ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᤱ").format(e))
    def bstack11ll1l111ll_opy_(self):
        return self.bstack11l1111ll1l_opy_
    def bstack11ll1ll1l1l_opy_(self):
        return False
    def __11l1111lll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᤲ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11lll1111ll_opy_(rep, [bstack111ll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᤳ"), bstack111ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᤴ"), bstack111ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᤵ"), bstack111ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᤶ"), bstack111ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᤷ"), bstack111ll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᤸ")])
        return None
    def __111ll1ll111_opy_(self, instance: bstack1l1l1ll11l1_opy_, *args):
        result = self.__11l1111lll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l111l_opy_ = None
        if result.get(bstack111ll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨ᤹ࠦ"), None) == bstack111ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ᤺") and len(args) > 1 and getattr(args[1], bstack111ll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨ᤻"), None) is not None:
            failure = [{bstack111ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᤼"): [args[1].excinfo.exconly(), result.get(bstack111ll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ᤽"), None)]}]
            bstack1ll111l111l_opy_ = bstack111ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ᤾") if bstack111ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ᤿") in getattr(args[1].excinfo, bstack111ll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧ᥀"), bstack111ll_opy_ (u"ࠦࠧ᥁")) else bstack111ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ᥂")
        bstack111llllll1l_opy_ = result.get(bstack111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᥃"), TestFramework.bstack11l11111111_opy_)
        if bstack111llllll1l_opy_ != TestFramework.bstack11l11111111_opy_:
            TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11lll11111l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l11111l11_opy_(instance, {
            TestFramework.bstack11l1l1ll1ll_opy_: failure,
            TestFramework.bstack111lll1l1l1_opy_: bstack1ll111l111l_opy_,
            TestFramework.bstack11l1ll11l11_opy_: bstack111llllll1l_opy_,
        })
    def __11l11111lll_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll1l1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1111l1l_opy_ bstack111ll111l11_opy_ this to be bstack111ll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᥄")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111lllllll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack111ll_opy_ (u"ࠣࡰࡲࡨࡪࠨ᥅"), None), bstack111ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᥆"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111ll_opy_ (u"ࠥࡲࡴࡪࡥࠣ᥇"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack111ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᥈"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1l1llllll_opy_(target) if target else None
        return instance
    def __111ll11l1l1_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack111ll1l1lll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, PytestBDDFramework.bstack111ll1l1ll1_opy_, {})
        if not key in bstack111ll1l1lll_opy_:
            bstack111ll1l1lll_opy_[key] = []
        bstack111lll111l1_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, PytestBDDFramework.bstack111lll11l1l_opy_, {})
        if not key in bstack111lll111l1_opy_:
            bstack111lll111l1_opy_[key] = []
        bstack111llllllll_opy_ = {
            PytestBDDFramework.bstack111ll1l1ll1_opy_: bstack111ll1l1lll_opy_,
            PytestBDDFramework.bstack111lll11l1l_opy_: bstack111lll111l1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack111ll_opy_ (u"ࠧࡱࡥࡺࠤ᥉"): key,
                TestFramework.bstack111llll1111_opy_: uuid4().__str__(),
                TestFramework.bstack111ll1l11l1_opy_: TestFramework.bstack111lll1lll1_opy_,
                TestFramework.bstack111lll1llll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll11l111_opy_: [],
                TestFramework.bstack111ll11ll1l_opy_: hook_name,
                TestFramework.bstack11l11111l1l_opy_: bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()
            }
            bstack111ll1l1lll_opy_[key].append(hook)
            bstack111llllllll_opy_[PytestBDDFramework.bstack111lllll11l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l111l111l_opy_ = bstack111ll1l1lll_opy_.get(key, [])
            hook = bstack11l111l111l_opy_.pop() if bstack11l111l111l_opy_ else None
            if hook:
                result = self.__11l1111lll1_opy_(*args)
                if result:
                    bstack111ll11l11l_opy_ = result.get(bstack111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᥊"), TestFramework.bstack111lll1lll1_opy_)
                    if bstack111ll11l11l_opy_ != TestFramework.bstack111lll1lll1_opy_:
                        hook[TestFramework.bstack111ll1l11l1_opy_] = bstack111ll11l11l_opy_
                hook[TestFramework.bstack111llll1l11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l11111l1l_opy_] = bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()
                self.bstack111lll1l1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll111lll_opy_, [])
                self.bstack1l1111ll1l_opy_(instance, logs)
                bstack111lll111l1_opy_[key].append(hook)
                bstack111llllllll_opy_[PytestBDDFramework.bstack111llll1ll1_opy_] = key
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨ᥋") + str(bstack111lll111l1_opy_) + bstack111ll_opy_ (u"ࠣࠤ᥌"))
    def __111ll1l1111_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11lll1111ll_opy_(args[0], [bstack111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ᥍"), bstack111ll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦ᥎"), bstack111ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦ᥏"), bstack111ll_opy_ (u"ࠧ࡯ࡤࡴࠤᥐ"), bstack111ll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᥑ"), bstack111ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᥒ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack111ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᥓ")) else fixturedef.get(bstack111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᥔ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111ll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᥕ")) else None
        node = request.node if hasattr(request, bstack111ll_opy_ (u"ࠦࡳࡵࡤࡦࠤᥖ")) else None
        target = request.node.nodeid if hasattr(node, bstack111ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᥗ")) else None
        baseid = fixturedef.get(bstack111ll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᥘ"), None) or bstack111ll_opy_ (u"ࠢࠣᥙ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111ll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᥚ")):
            target = PytestBDDFramework.__11l1111llll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᥛ")) else None
            if target and not TestFramework.bstack1l1l1llllll_opy_(target):
                self.__111lllllll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᥜ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠦࠧᥝ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᥞ") + str(target) + bstack111ll_opy_ (u"ࠨࠢᥟ"))
            return None
        instance = TestFramework.bstack1l1l1llllll_opy_(target)
        if not instance:
            self.logger.warning(bstack111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᥠ") + str(target) + bstack111ll_opy_ (u"ࠣࠤᥡ"))
            return None
        bstack111ll1ll11l_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, PytestBDDFramework.bstack111lll1l11l_opy_, {})
        if os.getenv(bstack111ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᥢ"), bstack111ll_opy_ (u"ࠥ࠵ࠧᥣ")) == bstack111ll_opy_ (u"ࠦ࠶ࠨᥤ"):
            bstack11l111111l1_opy_ = bstack111ll_opy_ (u"ࠧࡀࠢᥥ").join((scope, fixturename))
            bstack11l111111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack111ll1ll1ll_opy_ = {
                bstack111ll_opy_ (u"ࠨ࡫ࡦࡻࠥᥦ"): bstack11l111111l1_opy_,
                bstack111ll_opy_ (u"ࠢࡵࡣࡪࡷࠧᥧ"): PytestBDDFramework.__111ll1l11ll_opy_(request.node, scenario),
                bstack111ll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᥨ"): fixturedef,
                bstack111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᥩ"): scope,
                bstack111ll_opy_ (u"ࠥࡸࡾࡶࡥࠣᥪ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᥫ"), None)):
                    bstack111ll1ll1ll_opy_[bstack111ll_opy_ (u"ࠧࡺࡹࡱࡧࠥᥬ")] = TestFramework.bstack11ll1l11l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111ll1ll1ll_opy_[bstack111ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᥭ")] = uuid4().__str__()
                bstack111ll1ll1ll_opy_[PytestBDDFramework.bstack111lll1llll_opy_] = bstack11l111111ll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111ll1ll1ll_opy_[PytestBDDFramework.bstack111llll1l11_opy_] = bstack11l111111ll_opy_
            if bstack11l111111l1_opy_ in bstack111ll1ll11l_opy_:
                bstack111ll1ll11l_opy_[bstack11l111111l1_opy_].update(bstack111ll1ll1ll_opy_)
                self.logger.debug(bstack111ll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣ᥮") + str(bstack111ll1ll11l_opy_[bstack11l111111l1_opy_]) + bstack111ll_opy_ (u"ࠣࠤ᥯"))
            else:
                bstack111ll1ll11l_opy_[bstack11l111111l1_opy_] = bstack111ll1ll1ll_opy_
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᥰ") + str(len(bstack111ll1ll11l_opy_)) + bstack111ll_opy_ (u"ࠥࠦᥱ"))
        TestFramework.bstack11ll11l1_opy_(instance, PytestBDDFramework.bstack111lll1l11l_opy_, bstack111ll1ll11l_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᥲ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠧࠨᥳ"))
        return instance
    def __111lllllll1_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        ob = bstack1l1l1ll11l1_opy_(ctx, self.bstack1l1l11l1111_opy_, self.bstack1l11llll11l_opy_, test_framework_state)
        TestFramework.bstack11l11111l11_opy_(ob, {
            TestFramework.bstack1l1111l111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll1l11l1l_opy_: context.test_framework_version,
            TestFramework.bstack111lll1ll1l_opy_: [],
            PytestBDDFramework.bstack111lll1l11l_opy_: {},
            PytestBDDFramework.bstack111lll11l1l_opy_: {},
            PytestBDDFramework.bstack111ll1l1ll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11ll11l1_opy_(ob, TestFramework.bstack11l1111l1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11ll11l1_opy_(ob, TestFramework.bstack1l111111111_opy_, context.platform_index)
        TestFramework.bstack111l11l1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack111ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᥴ") + str(TestFramework.bstack111l11l1l1_opy_.keys()) + bstack111ll_opy_ (u"ࠢࠣ᥵"))
        return ob
    @staticmethod
    def __111ll1lll11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111ll_opy_ (u"ࠨ࡫ࡧࠫ᥶"): id(step),
                bstack111ll_opy_ (u"ࠩࡷࡩࡽࡺࠧ᥷"): step.name,
                bstack111ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ᥸"): step.keyword,
            })
        meta = {
            bstack111ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬ᥹"): {
                bstack111ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᥺"): feature.name,
                bstack111ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ᥻"): feature.filename,
                bstack111ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᥼"): feature.description
            },
            bstack111ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ᥽"): {
                bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᥾"): scenario.name
            },
            bstack111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᥿"): steps,
            bstack111ll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᦀ"): PytestBDDFramework.__111ll11llll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack111ll111ll1_opy_: meta
            }
        )
    def bstack111lll1l1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᦁ")
        global _11ll111lll1_opy_
        platform_index = os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᦂ")]
        bstack11ll11lllll_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), bstack111lllll111_opy_)
        if not os.path.exists(bstack11ll11lllll_opy_) or not os.path.isdir(bstack11ll11lllll_opy_):
            return
        logs = hook.get(bstack111ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᦃ"), [])
        with os.scandir(bstack11ll11lllll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll111lll1_opy_:
                    self.logger.info(bstack111ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᦄ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111ll_opy_ (u"ࠤࠥᦅ")
                    log_entry = bstack11l1l1l1ll_opy_(
                        kind=bstack111ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᦆ"),
                        message=bstack111ll_opy_ (u"ࠦࠧᦇ"),
                        level=bstack111ll_opy_ (u"ࠧࠨᦈ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1lll111_opy_=entry.stat().st_size,
                        bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᦉ"),
                        bstack111l1_opy_=os.path.abspath(entry.path),
                        bstack111llllll11_opy_=hook.get(TestFramework.bstack111llll1111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll111lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᦊ")]
        bstack111lllll1l1_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), bstack111lllll111_opy_, bstack111lll11l11_opy_)
        if not os.path.exists(bstack111lllll1l1_opy_) or not os.path.isdir(bstack111lllll1l1_opy_):
            self.logger.info(bstack111ll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᦋ").format(bstack111lllll1l1_opy_))
        else:
            self.logger.info(bstack111ll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᦌ").format(bstack111lllll1l1_opy_))
            with os.scandir(bstack111lllll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll111lll1_opy_:
                        self.logger.info(bstack111ll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᦍ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111ll_opy_ (u"ࠦࠧᦎ")
                        log_entry = bstack11l1l1l1ll_opy_(
                            kind=bstack111ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᦏ"),
                            message=bstack111ll_opy_ (u"ࠨࠢᦐ"),
                            level=bstack111ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᦑ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1lll111_opy_=entry.stat().st_size,
                            bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᦒ"),
                            bstack111l1_opy_=os.path.abspath(entry.path),
                            bstack11lll11ll1l_opy_=hook.get(TestFramework.bstack111llll1111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll111lll1_opy_.add(abs_path)
        hook[bstack111ll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᦓ")] = logs
    def bstack1l1111ll1l_opy_(
        self,
        bstack1llllllll_opy_: bstack1l1l1ll11l1_opy_,
        entries: List[bstack11l1l1l1ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᦔ"))
        req.platform_index = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l111111111_opy_)
        req.client_worker_id = bstack111ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᦕ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1llllllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1llllllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1llllllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l1111l111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack11ll1l11l1l_opy_)
            log_entry.uuid = entry.bstack111llllll11_opy_ if entry.bstack111llllll11_opy_ else TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.test_framework_state = bstack1llllllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᦖ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᦗ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1lll111_opy_
                log_entry.file_path = entry.bstack111l1_opy_
        def bstack11lll111lll_opy_():
            bstack1l11111lll_opy_ = datetime.now()
            try:
                self.bstack111111ll1l_opy_.LogCreatedEvent(req)
                bstack1llllllll_opy_.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᦘ"), datetime.now() - bstack1l11111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᦙ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1ll1llll1_opy_.enqueue(bstack11lll111lll_opy_)
    def __111llll11l1_opy_(self, instance) -> None:
        bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᦚ")
        bstack111llllllll_opy_ = {bstack111ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᦛ"): bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()}
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        bstack1l11ll1111l_opy_.bstack111lll11lll_opy_()
    @staticmethod
    def __111llll1lll_opy_(instance, args):
        request, bstack111lll11ll1_opy_ = args
        bstack111ll11lll1_opy_ = id(bstack111lll11ll1_opy_)
        bstack111ll1lll1l_opy_ = instance.data[TestFramework.bstack111ll111ll1_opy_]
        step = next(filter(lambda st: st[bstack111ll_opy_ (u"ࠫ࡮ࡪࠧᦜ")] == bstack111ll11lll1_opy_, bstack111ll1lll1l_opy_[bstack111ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᦝ")]), None)
        step.update({
            bstack111ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᦞ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack111ll1lll1l_opy_[bstack111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᦟ")]) if st[bstack111ll_opy_ (u"ࠨ࡫ࡧࠫᦠ")] == step[bstack111ll_opy_ (u"ࠩ࡬ࡨࠬᦡ")]), None)
        if index is not None:
            bstack111ll1lll1l_opy_[bstack111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᦢ")][index] = step
        instance.data[TestFramework.bstack111ll111ll1_opy_] = bstack111ll1lll1l_opy_
    @staticmethod
    def __111ll1l111l_opy_(instance, args):
        bstack111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᦣ")
        bstack1ll1l1l11l1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack111lll11ll1_opy_ = args[1]
        bstack111ll11lll1_opy_ = id(bstack111lll11ll1_opy_)
        bstack111ll1lll1l_opy_ = instance.data[TestFramework.bstack111ll111ll1_opy_]
        step = None
        if bstack111ll11lll1_opy_ is not None and bstack111ll1lll1l_opy_.get(bstack111ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᦤ")):
            step = next(filter(lambda st: st[bstack111ll_opy_ (u"࠭ࡩࡥࠩᦥ")] == bstack111ll11lll1_opy_, bstack111ll1lll1l_opy_[bstack111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᦦ")]), None)
            step.update({
                bstack111ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᦧ"): bstack1ll1l1l11l1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack111ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᦨ"): bstack111ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᦩ"),
                bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᦪ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack111ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᦫ"): bstack111ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᦬"),
                })
        index = next((i for i, st in enumerate(bstack111ll1lll1l_opy_[bstack111ll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᦭")]) if st[bstack111ll_opy_ (u"ࠨ࡫ࡧࠫ᦮")] == step[bstack111ll_opy_ (u"ࠩ࡬ࡨࠬ᦯")]), None)
        if index is not None:
            bstack111ll1lll1l_opy_[bstack111ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᦰ")][index] = step
        instance.data[TestFramework.bstack111ll111ll1_opy_] = bstack111ll1lll1l_opy_
    @staticmethod
    def __111ll11llll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack111ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᦱ")):
                examples = list(node.callspec.params[bstack111ll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᦲ")].values())
            return examples
        except:
            return []
    def bstack11lll111l1l_opy_(self, instance: bstack1l1l1ll11l1_opy_, bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1111l11l_opy_ = (
            PytestBDDFramework.bstack111lllll11l_opy_
            if bstack1l1l1lll11l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111llll1ll1_opy_
        )
        hook = PytestBDDFramework.bstack111ll11ll11_opy_(instance, bstack11l1111l11l_opy_)
        entries = hook.get(TestFramework.bstack111ll11l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, []))
        return entries
    def bstack11lll11l1ll_opy_(self, instance: bstack1l1l1ll11l1_opy_, bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1111l11l_opy_ = (
            PytestBDDFramework.bstack111lllll11l_opy_
            if bstack1l1l1lll11l_opy_[1] == TestHookState.PRE
            else PytestBDDFramework.bstack111llll1ll1_opy_
        )
        PytestBDDFramework.bstack11l1111111l_opy_(instance, bstack11l1111l11l_opy_)
        TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, []).clear()
    @staticmethod
    def bstack111ll11ll11_opy_(instance: bstack1l1l1ll11l1_opy_, bstack11l1111l11l_opy_: str):
        bstack111lll1111l_opy_ = (
            PytestBDDFramework.bstack111lll11l1l_opy_
            if bstack11l1111l11l_opy_ == PytestBDDFramework.bstack111llll1ll1_opy_
            else PytestBDDFramework.bstack111ll1l1ll1_opy_
        )
        bstack11l1111ll11_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack11l1111l11l_opy_, None)
        bstack111lllll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1111l_opy_, None) if bstack11l1111ll11_opy_ else None
        return (
            bstack111lllll1ll_opy_[bstack11l1111ll11_opy_][-1]
            if isinstance(bstack111lllll1ll_opy_, dict) and len(bstack111lllll1ll_opy_.get(bstack11l1111ll11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111111l_opy_(instance: bstack1l1l1ll11l1_opy_, bstack11l1111l11l_opy_: str):
        hook = PytestBDDFramework.bstack111ll11ll11_opy_(instance, bstack11l1111l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll11l111_opy_, []).clear()
    @staticmethod
    def __111lll1ll11_opy_(instance: bstack1l1l1ll11l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111ll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᦳ"), None)):
            return
        if os.getenv(bstack111ll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᦴ"), bstack111ll_opy_ (u"ࠣ࠳ࠥᦵ")) != bstack111ll_opy_ (u"ࠤ࠴ࠦᦶ"):
            PytestBDDFramework.logger.warning(bstack111ll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᦷ"))
            return
        bstack111llll11ll_opy_ = {
            bstack111ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᦸ"): (PytestBDDFramework.bstack111lllll11l_opy_, PytestBDDFramework.bstack111ll1l1ll1_opy_),
            bstack111ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᦹ"): (PytestBDDFramework.bstack111llll1ll1_opy_, PytestBDDFramework.bstack111lll11l1l_opy_),
        }
        for when in (bstack111ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᦺ"), bstack111ll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᦻ"), bstack111ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᦼ")):
            bstack111ll111l1l_opy_ = args[1].get_records(when)
            if not bstack111ll111l1l_opy_:
                continue
            records = [
                bstack11l1l1l1ll_opy_(
                    kind=TestFramework.bstack11ll1l1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111ll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᦽ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111ll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᦾ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll111l1l_opy_
                if isinstance(getattr(r, bstack111ll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᦿ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111lll1l111_opy_, bstack111lll1111l_opy_ = bstack111llll11ll_opy_.get(when, (None, None))
            bstack11l111l1111_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1l111_opy_, None) if bstack111lll1l111_opy_ else None
            bstack111lllll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1111l_opy_, None) if bstack11l111l1111_opy_ else None
            if isinstance(bstack111lllll1ll_opy_, dict) and len(bstack111lllll1ll_opy_.get(bstack11l111l1111_opy_, [])) > 0:
                hook = bstack111lllll1ll_opy_[bstack11l111l1111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll11l111_opy_ in hook:
                    hook[TestFramework.bstack111ll11l111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll11111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        test_id = request.node.nodeid
        test_name = PytestBDDFramework.__111lll111ll_opy_(request.node, scenario)
        bstack11l1111l111_opy_ = feature.filename
        if not test_id or not test_name or not bstack11l1111l111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l11111111l_opy_: uuid4().__str__(),
            TestFramework.bstack11l1l1ll11l_opy_: test_id,
            TestFramework.bstack1l1111lll11_opy_: test_name,
            TestFramework.bstack11l1llll111_opy_: test_id,
            TestFramework.bstack11l1111l1ll_opy_: bstack11l1111l111_opy_,
            TestFramework.bstack111ll1llll1_opy_: PytestBDDFramework.__111ll1l11ll_opy_(feature, scenario),
            TestFramework.bstack111ll11l1ll_opy_: code,
            TestFramework.bstack11l1ll11l11_opy_: TestFramework.bstack11l11111111_opy_,
            TestFramework.bstack11l11l1111l_opy_: test_name
        }
    @staticmethod
    def __111lll111ll_opy_(node, scenario):
        if hasattr(node, bstack111ll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᧀ")):
            parts = node.nodeid.rsplit(bstack111ll_opy_ (u"ࠨ࡛ࠣᧁ"))
            params = parts[-1]
            return bstack111ll_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᧂ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __111ll1l11ll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack111ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᧃ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᧄ")) else [])
    @staticmethod
    def __11l1111llll_opy_(location):
        return bstack111ll_opy_ (u"ࠥ࠾࠿ࠨᧅ").join(filter(lambda x: isinstance(x, str), location))