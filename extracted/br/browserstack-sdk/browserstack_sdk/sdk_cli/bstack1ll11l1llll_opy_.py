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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111lllll_opy_,
    TestHookState,
    bstack1ll1lll11l1_opy_,
    bstack1l1lllllll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l111llll1l_opy_
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1ll1ll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll11l11111_opy_ import bstack1ll111lll11_opy_
from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
bstack1l111l1ll11_opy_ = bstack1l111llll1l_opy_()
bstack11ll11l1l1l_opy_ = 1.0
bstack1l1111l1l1l_opy_ = bstack1111l_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᢡ")
bstack11l1l11ll11_opy_ = bstack1111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᢢ")
bstack11l1l11l111_opy_ = bstack1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᢣ")
bstack11l1l111lll_opy_ = bstack1111l_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᢤ")
bstack11l1l11l1ll_opy_ = bstack1111l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᢥ")
_1l11111l1ll_opy_ = set()
class bstack1l1llllll11_opy_(TestFramework):
    bstack11l1l1111l1_opy_ = bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᢦ")
    bstack11ll11l111l_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᢧ")
    bstack11ll1111ll1_opy_ = bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᢨ")
    bstack11l1ll11l1l_opy_ = bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤᢩࠣ")
    bstack11l1lll1l11_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᢪ")
    bstack11l11lllll1_opy_: bool
    bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_ = None
    bstack1ll1ll1lll1_opy_ = None
    bstack11l1ll1l111_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1l11llll_opy_: Dict[str, str],
        bstack1l11lll111l_opy_: List[str] = [bstack1111l_opy_ (u"ࠣࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ᢫")],
        bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_ = None,
        bstack1ll1ll1lll1_opy_=None
    ):
        super().__init__(bstack1l11lll111l_opy_, bstack11l1l11llll_opy_, bstack1ll1ll11lll_opy_)
        self.bstack11l11lllll1_opy_ = any(bstack1111l_opy_ (u"ࠤࡵࡳࡧࡵࡴࠣ᢬") in item.lower() for item in bstack1l11lll111l_opy_)
        self.bstack1ll1ll1lll1_opy_ = bstack1ll1ll1lll1_opy_
    def track_event(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1llllll11_opy_.bstack11l1ll1l111_opy_:
            bstack11l1l1lll11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1111l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢ᢭").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l11lllll1_opy_:
            self.logger.warning(bstack1111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࢀࢃࠢ᢮").format(str(self.bstack1l11lll111l_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧ᢯").format(args, kwargs))
            return
        instance = self.__11ll11l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠢᢰ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1llllll11_opy_.bstack11l1ll1l111_opy_:
                bstack1l1llll1_opy_ = bstack1111l_opy_ (u"ࠢࠣᢱ")
                name = bstack1111l_opy_ (u"ࠣࠤᢲ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11l1l11ll1l_opy_.value)
                    name = str(EVENTS.bstack11l1l11ll1l_opy_.name) + bstack1111l_opy_ (u"ࠤ࠽ࠦᢳ") + str(test_framework_state.name)
                else:
                    bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11l1l111ll1_opy_.value)
                    name = str(EVENTS.bstack11l1l111ll1_opy_.name) + bstack1111l_opy_ (u"ࠥ࠾ࠧᢴ") + str(test_framework_state.name)
                TestFramework.bstack11l1ll1l11l_opy_(instance, name, bstack1l1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᢵ").format(e))
        try:
            if not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack11llll1l1l1_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1llllll11_opy_.__11l11llll11_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1111l_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣᢶ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11l111l11_opy_):
                    TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l111l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢᢷ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_):
                    TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠨᢸ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1llllll11_opy_.__11l1ll1l1l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll111l111_opy_(instance, *args)
                self.__11ll1111l1l_opy_(instance)
            elif test_framework_state in bstack1l1llllll11_opy_.bstack11l1ll1l111_opy_:
                self.__11ll111l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠦᢹ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1lll1ll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1llllll11_opy_.bstack11l1ll1l111_opy_:
                bstack1l1llll1_opy_ = bstack1111l_opy_ (u"ࠤࠥᢺ")
                name = bstack1111l_opy_ (u"ࠥࠦᢻ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1l11ll1l_opy_.name) + bstack1111l_opy_ (u"ࠦ࠿ࠨᢼ") + str(test_framework_state.name)
                    bstack1l1llll1_opy_ = TestFramework.bstack11l1lllllll_opy_(instance, name)
                    bstack1l11ll1l1_opy_.end(EVENTS.bstack11l1l11ll1l_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᢽ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᢾ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1l111ll1_opy_.name) + bstack1111l_opy_ (u"ࠢ࠻ࠤᢿ") + str(test_framework_state.name)
                    bstack1l1llll1_opy_ = TestFramework.bstack11l1lllllll_opy_(instance, name)
                    bstack1l11ll1l1_opy_.end(EVENTS.bstack11l1l111ll1_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᣀ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᣁ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᣂ").format(e))
    def bstack1l1111l11l1_opy_(self):
        return self.bstack11l11lllll1_opy_
    def bstack1l11111llll_opy_(self):
        return False
    def __11l1l111111_opy_(self, *args):
        bstack1111l_opy_ (u"ࠦࠧࠨࡐࡢࡴࡶࡩࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡧࡶࡹࡱࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤᣃ")
        if len(args) > 1 and hasattr(args[1], bstack1111l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᣄ")):
            result = args[1]
            if result:
                return TestFramework.bstack1l11111l1l1_opy_(result, [bstack1111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᣅ"), bstack1111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᣆ"), bstack1111l_opy_ (u"ࠣࡵࡷࡥࡷࡺࡴࡪ࡯ࡨࠦᣇ"), bstack1111l_opy_ (u"ࠤࡨࡲࡩࡺࡩ࡮ࡧࠥᣈ"), bstack1111l_opy_ (u"ࠥࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠣᣉ")])
        return None
    def __11ll111l111_opy_(self, instance: bstack1ll111lllll_opy_, *args):
        result = self.__11l1l111111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll11l1l1l_opy_ = None
        status = result.get(bstack1111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᣊ"), bstack1111l_opy_ (u"ࠧࡔࡏࡕࠢࡕ࡙ࡓࠨᣋ"))
        if status == bstack1111l_opy_ (u"ࠨࡆࡂࡋࡏࠦᣌ") and result.get(bstack1111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᣍ")):
            failure = [{bstack1111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᣎ"): [result.get(bstack1111l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᣏ"), bstack1111l_opy_ (u"ࠥࠦᣐ"))]}]
            bstack1lll11l1l1l_opy_ = bstack1111l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᣑ")
        bstack11l1llll1ll_opy_ = TestFramework.bstack11ll1111l11_opy_
        if status == bstack1111l_opy_ (u"ࠧࡖࡁࡔࡕࠥᣒ"):
            bstack11l1llll1ll_opy_ = bstack1111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᣓ")
        elif status == bstack1111l_opy_ (u"ࠢࡇࡃࡌࡐࠧᣔ"):
            bstack11l1llll1ll_opy_ = bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᣕ")
        elif status == bstack1111l_opy_ (u"ࠤࡖࡏࡎࡖࠢᣖ"):
            bstack11l1llll1ll_opy_ = bstack1111l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᣗ")
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
            instance = self.__11l11llll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l11llllll_opy_(test) if test else None
                if target:
                    self.__11l1l111l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᣘ"), None)
            elif hasattr(args[0], bstack1111l_opy_ (u"ࠧ࡯ࡤࠣᣙ")) if len(args) > 0 else False:
                target = args[0].id
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
        bstack11l1ll1111l_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack1l1llllll11_opy_.bstack11ll11l111l_opy_, {})
        if not key in bstack11l1ll1111l_opy_:
            bstack11l1ll1111l_opy_[key] = []
        bstack11ll11ll1ll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack1l1llllll11_opy_.bstack11ll1111ll1_opy_, {})
        if not key in bstack11ll11ll1ll_opy_:
            bstack11ll11ll1ll_opy_[key] = []
        bstack11l1lllll11_opy_ = {
            bstack1l1llllll11_opy_.bstack11ll11l111l_opy_: bstack11l1ll1111l_opy_,
            bstack1l1llllll11_opy_.bstack11ll1111ll1_opy_: bstack11ll11ll1ll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1111l_opy_ (u"ࠨࠢᣚ")
            if len(args) > 0 and hasattr(args[0], bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᣛ")):
                hook_name = args[0].name
            hook = {
                bstack1111l_opy_ (u"ࠣ࡭ࡨࡽࠧᣜ"): key,
                TestFramework.bstack11l1ll1l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack11ll111ll11_opy_: TestFramework.bstack11ll1111111_opy_,
                TestFramework.bstack11ll111l1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll11111_opy_: [],
                TestFramework.bstack11l1l1l1l11_opy_: hook_name,
                TestFramework.bstack11l1l1l1lll_opy_: bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()
            }
            bstack11l1ll1111l_opy_[key].append(hook)
            bstack11l1lllll11_opy_[bstack1l1llllll11_opy_.bstack11l1ll11l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll11lll_opy_ = bstack11l1ll1111l_opy_.get(key, [])
            hook = bstack11l1ll11lll_opy_.pop() if bstack11l1ll11lll_opy_ else None
            if hook:
                result = self.__11l1l111111_opy_(*args)
                if result:
                    bstack11l1l1ll11l_opy_ = result.get(bstack1111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᣝ"), TestFramework.bstack11ll1111111_opy_)
                    if bstack11l1l1ll11l_opy_ == bstack1111l_opy_ (u"ࠥࡔࡆ࡙ࡓࠣᣞ"):
                        bstack11l1l1ll11l_opy_ = bstack1111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᣟ")
                    elif bstack11l1l1ll11l_opy_ == bstack1111l_opy_ (u"ࠧࡌࡁࡊࡎࠥᣠ"):
                        bstack11l1l1ll11l_opy_ = bstack1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᣡ")
                    if bstack11l1l1ll11l_opy_ != TestFramework.bstack11ll1111111_opy_:
                        hook[TestFramework.bstack11ll111ll11_opy_] = bstack11l1l1ll11l_opy_
                hook[TestFramework.bstack11l1ll1llll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1lll_opy_] = bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()
                self.bstack11l1ll1ll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll1ll11_opy_, [])
                if logs:
                    self.bstack1l11l1l111l_opy_(instance, logs)
                bstack11ll11ll1ll_opy_[key].append(hook)
                bstack11l1lllll11_opy_[bstack1l1llllll11_opy_.bstack11l1lll1l11_opy_] = key
        TestFramework.bstack11ll1111lll_opy_(instance, bstack11l1lllll11_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾ࠰ࡾࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࡾࢁࠧᣢ").format(key, test_hook_state, bstack11l1ll1111l_opy_, bstack11ll11ll1ll_opy_))
    def __11l11llll1l_opy_(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1111l_opy_ (u"ࠣࠤࠥࡘࡷࡧࡣ࡬ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࡸࡱࡵࡨࠥ࡫ࡶࡦࡰࡷࡷࠥ࠮ࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡴࡾࡺࡥࡴࡶࠣࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࠨࠢࠣᣣ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᣤ"), None)
        bstack1ll1lll1ll1_opy_ = getattr(keyword, bstack1111l_opy_ (u"ࠥࡸࡾࡶࡥࠣᣥ"), None)
        test_id = kwargs.get(bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᣦ"), None)
        if not test_id:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡰ࡫ࡹࡸࡱࡵࡨࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡴ࡯ࠡࡶࡨࡷࡹࡥࡩࡥࠢ࡬ࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠢᣧ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll1l11l111_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤࡱࡥࡺࡹࡲࡶࡩࡥࡥࡷࡧࡱࡸ࠿ࠦ࡮ࡰࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤ࡯ࡤ࠾ࡽࢀࠦᣨ").format(test_id))
            return None
        bstack11l11lll1l1_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack1l1llllll11_opy_.bstack11l1l1111l1_opy_, {})
        if os.getenv(bstack1111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡋࡆ࡛࡚ࡓࡗࡊࡓࠣᣩ"), bstack1111l_opy_ (u"ࠣ࠳ࠥᣪ")) == bstack1111l_opy_ (u"ࠤ࠴ࠦᣫ"):
            bstack11l1l111l1l_opy_ = bstack1111l_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤᣬ").format(bstack1ll1lll1ll1_opy_, keyword_name)
            bstack11l1ll11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1l11111l_opy_ = {
                bstack1111l_opy_ (u"ࠦࡰ࡫ࡹࠣᣭ"): bstack11l1l111l1l_opy_,
                bstack1111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᣮ"): keyword_name,
                bstack1111l_opy_ (u"ࠨࡴࡺࡲࡨࠦᣯ"): bstack1ll1lll1ll1_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l1l11111l_opy_[bstack1111l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᣰ")] = uuid4().__str__()
                bstack11l1l11111l_opy_[bstack1l1llllll11_opy_.bstack11ll111l1l1_opy_] = bstack11l1ll11ll1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1l11111l_opy_[bstack1l1llllll11_opy_.bstack11l1ll1llll_opy_] = bstack11l1ll11ll1_opy_
                if len(args) > 1 and hasattr(args[1], bstack1111l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᣱ")):
                    bstack11l1l11111l_opy_[bstack1111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᣲ")] = args[1].status
            if bstack11l1l111l1l_opy_ in bstack11l11lll1l1_opy_:
                bstack11l11lll1l1_opy_[bstack11l1l111l1l_opy_].update(bstack11l1l11111l_opy_)
                self.logger.debug(bstack1111l_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠡࡶࡼࡴࡪࡃࡻࡾࠤᣳ").format(keyword_name, bstack1ll1lll1ll1_opy_))
            else:
                bstack11l11lll1l1_opy_[bstack11l1l111l1l_opy_] = bstack11l1l11111l_opy_
                self.logger.debug(bstack1111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠠࡵࡻࡳࡩࡂࢁࡽࠣᣴ").format(keyword_name, bstack1ll1lll1ll1_opy_))
        TestFramework.bstack1ll1lllll11_opy_(instance, bstack1l1llllll11_opy_.bstack11l1l1111l1_opy_, bstack11l11lll1l1_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡸࡃࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠢᣵ").format(len(bstack11l11lll1l1_opy_), instance.ref()))
        return instance
    def __11l1l111l11_opy_(
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
            bstack1l1llllll11_opy_.bstack11l1l1111l1_opy_: {},
            bstack1l1llllll11_opy_.bstack11ll1111ll1_opy_: {},
            bstack1l1llllll11_opy_.bstack11ll11l111l_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1111l_opy_ (u"ࠨࡳࡰࡷࡵࡧࡪࠨ᣶")):
            TestFramework.bstack1ll1lllll11_opy_(ob, TestFramework.bstack11l1ll111ll_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1lllll11_opy_(ob, TestFramework.bstack1l1l1l111ll_opy_, context.platform_index)
        TestFramework.bstack1ll1lll111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࢀࢃࠢ᣷").format(ctx.id, target, args, TestFramework.bstack1ll1lll111l_opy_.keys()))
        return ob
    def bstack1l111llllll_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11ll11l_opy_ = (
            bstack1l1llllll11_opy_.bstack11l1ll11l1l_opy_
            if bstack1ll1l111l11_opy_[1] == TestHookState.PRE
            else bstack1l1llllll11_opy_.bstack11l1lll1l11_opy_
        )
        hook = bstack1l1llllll11_opy_.bstack11l1lll1lll_opy_(instance, bstack11ll11ll11l_opy_)
        entries = hook.get(TestFramework.bstack11l1ll11111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, []))
        return entries
    def bstack1l111lll111_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11ll11l_opy_ = (
            bstack1l1llllll11_opy_.bstack11l1ll11l1l_opy_
            if bstack1ll1l111l11_opy_[1] == TestHookState.PRE
            else bstack1l1llllll11_opy_.bstack11l1lll1l11_opy_
        )
        bstack1l1llllll11_opy_.bstack11l1llll111_opy_(instance, bstack11ll11ll11l_opy_)
        TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, []).clear()
    def bstack11l1ll1ll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᣸")
        global _1l11111l1ll_opy_
        platform_index = os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᣹")]
        bstack1l111l1ll1l_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), bstack11l1l111lll_opy_)
        if not os.path.exists(bstack1l111l1ll1l_opy_) or not os.path.isdir(bstack1l111l1ll1l_opy_):
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣ᣺").format(bstack1l111l1ll1l_opy_))
            return
        logs = hook.get(bstack1111l_opy_ (u"ࠦࡱࡵࡧࡴࠤ᣻"), [])
        with os.scandir(bstack1l111l1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111l1ll_opy_:
                    self.logger.info(bstack1111l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ᣼").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111l_opy_ (u"ࠨࠢ᣽")
                    log_entry = bstack1l1lllllll1_opy_(
                        kind=bstack1111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᣾"),
                        message=bstack1111l_opy_ (u"ࠣࠤ᣿"),
                        level=bstack1111l_opy_ (u"ࠤࠥᤀ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11l11l1l1_opy_=entry.stat().st_size,
                        bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᤁ"),
                        bstack1llll1l_opy_=os.path.abspath(entry.path),
                        bstack11ll11l1111_opy_=hook.get(TestFramework.bstack11l1ll1l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111l1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᤂ")]
        bstack11ll11l1l11_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), bstack11l1l111lll_opy_, bstack11l1l11l1ll_opy_)
        if not os.path.exists(bstack11ll11l1l11_opy_) or not os.path.isdir(bstack11ll11l1l11_opy_):
            self.logger.info(bstack1111l_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᤃ").format(bstack11ll11l1l11_opy_))
        else:
            self.logger.info(bstack1111l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᤄ").format(bstack11ll11l1l11_opy_))
            with os.scandir(bstack11ll11l1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack1111l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᤅ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111l_opy_ (u"ࠣࠤᤆ")
                        log_entry = bstack1l1lllllll1_opy_(
                            kind=bstack1111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᤇ"),
                            message=bstack1111l_opy_ (u"ࠥࠦᤈ"),
                            level=bstack1111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᤉ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11l11l1l1_opy_=entry.stat().st_size,
                            bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᤊ"),
                            bstack1llll1l_opy_=os.path.abspath(entry.path),
                            bstack1l111ll11ll_opy_=hook.get(TestFramework.bstack11l1ll1l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111l1ll_opy_.add(abs_path)
        hook[bstack1111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᤋ")] = logs
    def bstack1l11l1l111l_opy_(
        self,
        bstack1l111lll1ll_opy_: bstack1ll111lllll_opy_,
        entries: List[bstack1l1lllllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᤌ"))
        req.platform_index = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l111ll_opy_)
        req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᤍ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111lll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111lll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111lll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l1ll1l_opy_, bstack1111l_opy_ (u"ࠤࠥᤎ"))
            log_entry.test_framework_version = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11l11ll1l_opy_, bstack1111l_opy_ (u"ࠥࠦᤏ"))
            log_entry.uuid = entry.bstack11ll11l1111_opy_ or bstack1111l_opy_ (u"ࠦࠧᤐ")
            log_entry.test_framework_state = bstack1l111lll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᤑ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1111l_opy_ (u"ࠨࠢᤒ")
            if entry.kind == bstack1111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᤓ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11l1l1_opy_
                log_entry.file_path = entry.bstack1llll1l_opy_
        def bstack1l11111lll1_opy_():
            bstack1lll1l11l_opy_ = datetime.now()
            try:
                self.bstack1ll1ll1lll1_opy_.LogCreatedEvent(req)
                bstack1l111lll1ll_opy_.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᤔ"), datetime.now() - bstack1lll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᤕ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1ll11lll_opy_.enqueue(bstack1l11111lll1_opy_)
    def __11ll1111l1l_opy_(self, instance) -> None:
        bstack1111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᤖ")
        bstack11l1lllll11_opy_ = {bstack1111l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᤗ"): bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll1111lll_opy_(instance, bstack11l1lllll11_opy_)
    @staticmethod
    def bstack11l1lll1lll_opy_(instance: bstack1ll111lllll_opy_, bstack11ll11ll11l_opy_: str):
        bstack11ll11ll1l1_opy_ = (
            bstack1l1llllll11_opy_.bstack11ll1111ll1_opy_
            if bstack11ll11ll11l_opy_ == bstack1l1llllll11_opy_.bstack11l1lll1l11_opy_
            else bstack1l1llllll11_opy_.bstack11ll11l111l_opy_
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
        hook = bstack1l1llllll11_opy_.bstack11l1lll1lll_opy_(instance, bstack11ll11ll11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll11111_opy_, []).clear()
    @staticmethod
    def __11l1ll1l1l1_opy_(instance: bstack1ll111lllll_opy_, *args):
        bstack1111l_opy_ (u"ࠧࠨࠢࡑࡴࡲࡧࡪࡹࡳࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࡴࠤࠥࠦᤘ")
        if len(args) < 1:
            return
        if os.getenv(bstack1111l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᤙ"), bstack1111l_opy_ (u"ࠢ࠲ࠤᤚ")) != bstack1111l_opy_ (u"ࠣ࠳ࠥᤛ"):
            bstack1l1llllll11_opy_.logger.warning(bstack1111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡰࡴ࡭ࡳࠣᤜ"))
            return
        message = args[0]
        if not hasattr(message, bstack1111l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᤝ")):
            return
        is_screenshot = hasattr(message, bstack1111l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᤞ")) and message.kind == bstack1111l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ᤟")
        log_entry = bstack1l1lllllll1_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack1l1111l1111_opy_,
            message=message.message if hasattr(message, bstack1111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᤠ")) else bstack1111l_opy_ (u"ࠢࠣᤡ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1111l_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢᤢ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1111l_opy_ (u"ࠤࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠢᤣ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡴࡶࡤࡱࡵࠨᤤ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l1lll11ll_opy_ = {
            bstack1111l_opy_ (u"ࠦࡘࡋࡔࡖࡒࠥᤥ"): (bstack1l1llllll11_opy_.bstack11l1ll11l1l_opy_, bstack1l1llllll11_opy_.bstack11ll11l111l_opy_),
            bstack1111l_opy_ (u"࡚ࠧࡅࡂࡔࡇࡓ࡜ࡔࠢᤦ"): (bstack1l1llllll11_opy_.bstack11l1lll1l11_opy_, bstack1l1llllll11_opy_.bstack11ll1111ll1_opy_),
        }
        bstack11l11lll1ll_opy_ = None
        if len(args) > 1:
            bstack11l11lll1ll_opy_ = args[1]
        if bstack11l11lll1ll_opy_ and bstack11l11lll1ll_opy_ in bstack11l1lll11ll_opy_:
            bstack11l1lll1l1l_opy_, bstack11ll11ll1l1_opy_ = bstack11l1lll11ll_opy_[bstack11l11lll1ll_opy_]
            bstack11ll11111ll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11l1lll1l1l_opy_, None)
            bstack11l1l1llll1_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11ll11ll1l1_opy_, None) if bstack11ll11111ll_opy_ else None
            if isinstance(bstack11l1l1llll1_opy_, dict) and len(bstack11l1l1llll1_opy_.get(bstack11ll11111ll_opy_, [])) > 0:
                hook = bstack11l1l1llll1_opy_[bstack11ll11111ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll11111_opy_ in hook:
                    hook[TestFramework.bstack11l1ll11111_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l11llll11_opy_(test) -> Dict[str, Any]:
        bstack1111l_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡷࡩࡸࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤᤧ")
        test_id = bstack1l1llllll11_opy_.__11l11llllll_opy_(test)
        test_name = test.name if hasattr(test, bstack1111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᤨ")) else None
        bstack11ll111ll1l_opy_ = str(test.source) if hasattr(test, bstack1111l_opy_ (u"ࠣࡵࡲࡹࡷࡩࡥࠣᤩ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1111l_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᤪ")) else []
        bstack11l1l1111ll_opy_ =bstack1111l_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧᤫ").format(bstack1111l_opy_ (u"ࠦࠥࠨ᤬").join(test_tags), test_name) if test_tags else test_name
        bstack11l1l11l11l_opy_ = []
        if bstack11ll111ll1l_opy_:
            from browserstack_sdk.bstack1llllll1l11_opy_ import RobotHandler
            bstack11l1l11l11l_opy_ = RobotHandler.bstack1lllll11ll1_opy_(bstack11ll111ll1l_opy_)
        if not bstack11l1l11l11l_opy_ and test_name:
            bstack11l1l11l11l_opy_ = [test_name]
        return {
            TestFramework.bstack1l11ll1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1l1l1_opy_: test_id,
            TestFramework.bstack1l1l111llll_opy_: test_name,
            TestFramework.bstack1l11111l111_opy_: test_id,
            TestFramework.bstack11l1ll111l1_opy_: bstack11ll111ll1l_opy_,
            TestFramework.bstack11l1lll111l_opy_: test_tags,
            TestFramework.bstack11l1ll11l11_opy_: bstack11l1l1111ll_opy_,
            TestFramework.bstack11lll1ll1l1_opy_: TestFramework.bstack11ll1111l11_opy_,
            TestFramework.bstack11ll1l1ll11_opy_: test_id,
            TestFramework.bstack11l1l11l1l1_opy_: bstack11l1l11l11l_opy_
        }
    @staticmethod
    def __11l11llllll_opy_(test):
        bstack1111l_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡺࡴࡩࡲࡷࡨࠤࡹ࡫ࡳࡵࠢࡌࡈࠥ࡬ࡲࡰ࡯ࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡺࡥࡴࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧ᤭")
        if hasattr(test, bstack1111l_opy_ (u"ࠨࡩࡥࠤ᤮")):
            return test.id
        elif hasattr(test, bstack1111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡳࡧ࡭ࡦࠤ᤯")):
            return test.longname
        elif hasattr(test, bstack1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᤰ")):
            return test.name
        return None