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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll11ll111l_opy_,
    TestHookState,
    bstack1lll1l1l1ll_opy_,
    bstack1ll11lllll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l111l11lll_opy_
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll1111111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1llll1lll_opy_ import bstack1l1ll1l1lll_opy_
from bstack_utils.bstack1111l1l1l1_opy_ import bstack11l111ll11_opy_
bstack1l11ll111ll_opy_ = bstack1l111l11lll_opy_()
bstack11ll11ll1l1_opy_ = 1.0
bstack1l11ll11ll1_opy_ = bstack1111_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤ៶")
bstack11l1l1ll1ll_opy_ = bstack1111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ៷")
bstack11l1ll1111l_opy_ = bstack1111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣ៸")
bstack11l1l1llll1_opy_ = bstack1111_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ៹")
bstack11l1l1lll11_opy_ = bstack1111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ៺")
_1l111l1l11l_opy_ = set()
class bstack1ll11ll1l1l_opy_(TestFramework):
    bstack11l1l1l1ll1_opy_ = bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡱࡥࡺࡹࡲࡶࡩࡹࠢ៻")
    bstack11ll11lll11_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨ៼")
    bstack11ll11ll1ll_opy_ = bstack1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ៽")
    bstack11ll11l111l_opy_ = bstack1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧ៾")
    bstack11ll1111l1l_opy_ = bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢ៿")
    bstack11l1l1l111l_opy_: bool
    bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_ = None
    bstack1lll111l111_opy_ = None
    bstack11ll11llll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll11l1l1l_opy_: Dict[str, str],
        bstack1l1ll111l11_opy_: List[str] = [bstack1111_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠨ᠀")],
        bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_ = None,
        bstack1lll111l111_opy_=None
    ):
        super().__init__(bstack1l1ll111l11_opy_, bstack11ll11l1l1l_opy_, bstack1ll1lllll1l_opy_)
        self.bstack11l1l1l111l_opy_ = any(bstack1111_opy_ (u"ࠨࡲࡰࡤࡲࡸࠧ᠁") in item.lower() for item in bstack1l1ll111l11_opy_)
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
    def track_event(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1ll11ll1l1l_opy_.bstack11ll11llll1_opy_:
            bstack11ll11lll1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1111_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠦ᠂").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l1l1l111l_opy_:
            self.logger.warning(bstack1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࡽࢀࠦ᠃").format(str(self.bstack1l1ll111l11_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤ᠄").format(args, kwargs))
            return
        instance = self.__11ll11l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠦ᠅").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1ll11ll1l1l_opy_.bstack11ll11llll1_opy_:
                bstack1l1l1llll1_opy_ = bstack1111_opy_ (u"ࠦࠧ᠆")
                name = bstack1111_opy_ (u"ࠧࠨ᠇")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l1l1lllll_opy_.value)
                    name = str(EVENTS.bstack11l1l1lllll_opy_.name) + bstack1111_opy_ (u"ࠨ࠺ࠣ᠈") + str(test_framework_state.name)
                else:
                    bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l1ll11111_opy_.value)
                    name = str(EVENTS.bstack11l1ll11111_opy_.name) + bstack1111_opy_ (u"ࠢ࠻ࠤ᠉") + str(test_framework_state.name)
                TestFramework.bstack11ll11ll11l_opy_(instance, name, bstack1l1l1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧ᠊").format(e))
        try:
            if not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack11llll1ll1l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1ll11ll1l1l_opy_.__11l1l1l11ll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1111_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠧ᠋").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_):
                    TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠦ᠌").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l11l1l111l_opy_):
                    TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥ᠍").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1ll11ll1l1l_opy_.__11l1ll1llll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1lll11ll_opy_(instance, *args)
                self.__11l1lllll11_opy_(instance)
            elif test_framework_state in bstack1ll11ll1l1l_opy_.bstack11ll11llll1_opy_:
                self.__11l1ll1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠣ᠎").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1111l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1ll11ll1l1l_opy_.bstack11ll11llll1_opy_:
                bstack1l1l1llll1_opy_ = bstack1111_opy_ (u"ࠨࠢ᠏")
                name = bstack1111_opy_ (u"ࠢࠣ᠐")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1l1lllll_opy_.name) + bstack1111_opy_ (u"ࠣ࠼ࠥ᠑") + str(test_framework_state.name)
                    bstack1l1l1llll1_opy_ = TestFramework.bstack11ll11111ll_opy_(instance, name)
                    bstack1l11l1ll_opy_.end(EVENTS.bstack11l1l1lllll_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᠒"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᠓"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1ll11111_opy_.name) + bstack1111_opy_ (u"ࠦ࠿ࠨ᠔") + str(test_framework_state.name)
                    bstack1l1l1llll1_opy_ = TestFramework.bstack11ll11111ll_opy_(instance, name)
                    bstack1l11l1ll_opy_.end(EVENTS.bstack11l1ll11111_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᠕"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᠖"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ᠗").format(e))
    def bstack1l11l11l111_opy_(self):
        return self.bstack11l1l1l111l_opy_
    def bstack1l111l1ll11_opy_(self):
        return False
    def __11l1l1l1lll_opy_(self, *args):
        bstack1111_opy_ (u"ࠣࠤࠥࡔࡦࡸࡳࡦࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡷ࡫ࡳࡶ࡮ࡷࠤࡴࡨࡪࡦࡥࡷࠦࠧࠨ᠘")
        if len(args) > 1 and hasattr(args[1], bstack1111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ᠙")):
            result = args[1]
            if result:
                return TestFramework.bstack1l111ll11ll_opy_(result, [bstack1111_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᠚"), bstack1111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ᠛"), bstack1111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡸ࡮ࡳࡥࠣ᠜"), bstack1111_opy_ (u"ࠨࡥ࡯ࡦࡷ࡭ࡲ࡫ࠢ᠝"), bstack1111_opy_ (u"ࠢࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠧ᠞")])
        return None
    def __11l1lll11ll_opy_(self, instance: bstack1ll11ll111l_opy_, *args):
        result = self.__11l1l1l1lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll1111_opy_ = None
        status = result.get(bstack1111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᠟"), bstack1111_opy_ (u"ࠤࡑࡓ࡙ࠦࡒࡖࡐࠥᠠ"))
        if status == bstack1111_opy_ (u"ࠥࡊࡆࡏࡌࠣᠡ") and result.get(bstack1111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᠢ")):
            failure = [{bstack1111_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᠣ"): [result.get(bstack1111_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᠤ"), bstack1111_opy_ (u"ࠢࠣᠥ"))]}]
            bstack1lll1ll1111_opy_ = bstack1111_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᠦ")
        bstack11l1lll1111_opy_ = TestFramework.bstack11l1ll11ll1_opy_
        if status == bstack1111_opy_ (u"ࠤࡓࡅࡘ࡙ࠢᠧ"):
            bstack11l1lll1111_opy_ = bstack1111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᠨ")
        elif status == bstack1111_opy_ (u"ࠦࡋࡇࡉࡍࠤᠩ"):
            bstack11l1lll1111_opy_ = bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᠪ")
        elif status == bstack1111_opy_ (u"ࠨࡓࡌࡋࡓࠦᠫ"):
            bstack11l1lll1111_opy_ = bstack1111_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᠬ")
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
            instance = self.__11l1l1l1l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l1l1l1l11_opy_(test) if test else None
                if target:
                    self.__11l1l1ll11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᠭ"), None)
            elif hasattr(args[0], bstack1111_opy_ (u"ࠤ࡬ࡨࠧᠮ")) if len(args) > 0 else False:
                target = args[0].id
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
        bstack11ll1l1l1l1_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack1ll11ll1l1l_opy_.bstack11ll11lll11_opy_, {})
        if not key in bstack11ll1l1l1l1_opy_:
            bstack11ll1l1l1l1_opy_[key] = []
        bstack11ll1111ll1_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack1ll11ll1l1l_opy_.bstack11ll11ll1ll_opy_, {})
        if not key in bstack11ll1111ll1_opy_:
            bstack11ll1111ll1_opy_[key] = []
        bstack11ll1l11ll1_opy_ = {
            bstack1ll11ll1l1l_opy_.bstack11ll11lll11_opy_: bstack11ll1l1l1l1_opy_,
            bstack1ll11ll1l1l_opy_.bstack11ll11ll1ll_opy_: bstack11ll1111ll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1111_opy_ (u"ࠥࠦᠯ")
            if len(args) > 0 and hasattr(args[0], bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᠰ")):
                hook_name = args[0].name
            hook = {
                bstack1111_opy_ (u"ࠧࡱࡥࡺࠤᠱ"): key,
                TestFramework.bstack11l1lll1l1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1l111_opy_: TestFramework.bstack11ll1l11l1l_opy_,
                TestFramework.bstack11ll1111111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll11l11_opy_: [],
                TestFramework.bstack11ll1l1ll1l_opy_: hook_name,
                TestFramework.bstack11ll1l1l11l_opy_: bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()
            }
            bstack11ll1l1l1l1_opy_[key].append(hook)
            bstack11ll1l11ll1_opy_[bstack1ll11ll1l1l_opy_.bstack11ll11l111l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1lllllll_opy_ = bstack11ll1l1l1l1_opy_.get(key, [])
            hook = bstack11l1lllllll_opy_.pop() if bstack11l1lllllll_opy_ else None
            if hook:
                result = self.__11l1l1l1lll_opy_(*args)
                if result:
                    bstack11ll1l1111l_opy_ = result.get(bstack1111_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᠲ"), TestFramework.bstack11ll1l11l1l_opy_)
                    if bstack11ll1l1111l_opy_ == bstack1111_opy_ (u"ࠢࡑࡃࡖࡗࠧᠳ"):
                        bstack11ll1l1111l_opy_ = bstack1111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᠴ")
                    elif bstack11ll1l1111l_opy_ == bstack1111_opy_ (u"ࠤࡉࡅࡎࡒࠢᠵ"):
                        bstack11ll1l1111l_opy_ = bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᠶ")
                    if bstack11ll1l1111l_opy_ != TestFramework.bstack11ll1l11l1l_opy_:
                        hook[TestFramework.bstack11l1ll1l111_opy_] = bstack11ll1l1111l_opy_
                hook[TestFramework.bstack11ll111l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1l1l11l_opy_] = bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()
                self.bstack11ll111llll_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l111l1_opy_, [])
                if logs:
                    self.bstack1l11l1l1lll_opy_(instance, logs)
                bstack11ll1111ll1_opy_[key].append(hook)
                bstack11ll1l11ll1_opy_[bstack1ll11ll1l1l_opy_.bstack11ll1111l1l_opy_] = key
        TestFramework.bstack11l1llll111_opy_(instance, bstack11ll1l11ll1_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂ࠴ࡻࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࡻࡾࠤᠷ").format(key, test_hook_state, bstack11ll1l1l1l1_opy_, bstack11ll1111ll1_opy_))
    def __11l1l1l1l1l_opy_(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1111_opy_ (u"ࠧࠨࠢࡕࡴࡤࡧࡰࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡨࡺࡪࡴࡴࡴࠢࠫࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡱࡻࡷࡩࡸࡺࠠࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࠥࠦࠧᠸ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᠹ"), None)
        bstack1lll111lll1_opy_ = getattr(keyword, bstack1111_opy_ (u"ࠢࡵࡻࡳࡩࠧᠺ"), None)
        test_id = kwargs.get(bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᠻ"), None)
        if not test_id:
            self.logger.debug(bstack1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠ࡭ࡨࡽࡼࡵࡲࡥࡡࡨࡺࡪࡴࡴ࠻ࠢࡱࡳࠥࡺࡥࡴࡶࡢ࡭ࡩࠦࡩ࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠ࡬ࡧࡼࡻࡴࡸࡤ࠾ࡽࢀࠦᠼ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll1l1l1lll_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡲࡴࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡡ࡬ࡨࡂࢁࡽࠣᠽ").format(test_id))
            return None
        bstack11l1l1l1111_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack1ll11ll1l1l_opy_.bstack11l1l1l1ll1_opy_, {})
        if os.getenv(bstack1111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡏࡊ࡟ࡗࡐࡔࡇࡗࠧᠾ"), bstack1111_opy_ (u"ࠧ࠷ࠢᠿ")) == bstack1111_opy_ (u"ࠨ࠱ࠣᡀ"):
            bstack11l1l1l11l1_opy_ = bstack1111_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨᡁ").format(bstack1lll111lll1_opy_, keyword_name)
            bstack11l1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1l11lll1_opy_ = {
                bstack1111_opy_ (u"ࠣ࡭ࡨࡽࠧᡂ"): bstack11l1l1l11l1_opy_,
                bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᡃ"): keyword_name,
                bstack1111_opy_ (u"ࠥࡸࡾࡶࡥࠣᡄ"): bstack1lll111lll1_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l1l11lll1_opy_[bstack1111_opy_ (u"ࠦࡺࡻࡩࡥࠤᡅ")] = uuid4().__str__()
                bstack11l1l11lll1_opy_[bstack1ll11ll1l1l_opy_.bstack11ll1111111_opy_] = bstack11l1ll1lll1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1l11lll1_opy_[bstack1ll11ll1l1l_opy_.bstack11ll111l111_opy_] = bstack11l1ll1lll1_opy_
                if len(args) > 1 and hasattr(args[1], bstack1111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᡆ")):
                    bstack11l1l11lll1_opy_[bstack1111_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᡇ")] = args[1].status
            if bstack11l1l1l11l1_opy_ in bstack11l1l1l1111_opy_:
                bstack11l1l1l1111_opy_[bstack11l1l1l11l1_opy_].update(bstack11l1l11lll1_opy_)
                self.logger.debug(bstack1111_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡ࡭ࡨࡽࡼࡵࡲࡥ࠿ࡾࢁࠥࡺࡹࡱࡧࡀࡿࢂࠨᡈ").format(keyword_name, bstack1lll111lll1_opy_))
            else:
                bstack11l1l1l1111_opy_[bstack11l1l1l11l1_opy_] = bstack11l1l11lll1_opy_
                self.logger.debug(bstack1111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠ࡬ࡧࡼࡻࡴࡸࡤ࠾ࡽࢀࠤࡹࡿࡰࡦ࠿ࡾࢁࠧᡉ").format(keyword_name, bstack1lll111lll1_opy_))
        TestFramework.bstack1lll1l11l1l_opy_(instance, bstack1ll11ll1l1l_opy_.bstack11l1l1l1ll1_opy_, bstack11l1l1l1111_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡭ࡨࡽࡼࡵࡲࡥࡵࡀࡿࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠦᡊ").format(len(bstack11l1l1l1111_opy_), instance.ref()))
        return instance
    def __11l1l1ll11l_opy_(
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
            bstack1ll11ll1l1l_opy_.bstack11l1l1l1ll1_opy_: {},
            bstack1ll11ll1l1l_opy_.bstack11ll11ll1ll_opy_: {},
            bstack1ll11ll1l1l_opy_.bstack11ll11lll11_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1111_opy_ (u"ࠥࡷࡴࡻࡲࡤࡧࠥᡋ")):
            TestFramework.bstack1lll1l11l1l_opy_(ob, TestFramework.bstack11l1llll11l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l11l1l_opy_(ob, TestFramework.bstack1l1l11l1ll1_opy_, context.platform_index)
        TestFramework.bstack1lll1111lll_opy_[ctx.id] = ob
        self.logger.debug(bstack1111_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࢀࠤࡦࡸࡧࡴ࠿ࡾࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࡽࢀࠦᡌ").format(ctx.id, target, args, TestFramework.bstack1lll1111lll_opy_.keys()))
        return ob
    def bstack1l11l11111l_opy_(self, instance: bstack1ll11ll111l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11l1l11_opy_ = (
            bstack1ll11ll1l1l_opy_.bstack11ll11l111l_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1ll11ll1l1l_opy_.bstack11ll1111l1l_opy_
        )
        hook = bstack1ll11ll1l1l_opy_.bstack11ll11lllll_opy_(instance, bstack11ll11l1l11_opy_)
        entries = hook.get(TestFramework.bstack11l1ll11l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, []))
        return entries
    def bstack1l11l11ll11_opy_(self, instance: bstack1ll11ll111l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11l1l11_opy_ = (
            bstack1ll11ll1l1l_opy_.bstack11ll11l111l_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1ll11ll1l1l_opy_.bstack11ll1111l1l_opy_
        )
        bstack1ll11ll1l1l_opy_.bstack11ll1l1l111_opy_(instance, bstack11ll11l1l11_opy_)
        TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, []).clear()
    def bstack11ll111llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᡍ")
        global _1l111l1l11l_opy_
        platform_index = os.environ[bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᡎ")]
        bstack1l111l111l1_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), bstack11l1l1llll1_opy_)
        if not os.path.exists(bstack1l111l111l1_opy_) or not os.path.isdir(bstack1l111l111l1_opy_):
            self.logger.debug(bstack1111_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࡷࠥࡺ࡯ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡾࢁࠧᡏ").format(bstack1l111l111l1_opy_))
            return
        logs = hook.get(bstack1111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᡐ"), [])
        with os.scandir(bstack1l111l111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111l1l11l_opy_:
                    self.logger.info(bstack1111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᡑ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111_opy_ (u"ࠥࠦᡒ")
                    log_entry = bstack1ll11lllll1_opy_(
                        kind=bstack1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᡓ"),
                        message=bstack1111_opy_ (u"ࠧࠨᡔ"),
                        level=bstack1111_opy_ (u"ࠨࠢᡕ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111l11ll1_opy_=entry.stat().st_size,
                        bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᡖ"),
                        bstack1llll_opy_=os.path.abspath(entry.path),
                        bstack11ll11l1111_opy_=hook.get(TestFramework.bstack11l1lll1l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111l1l11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᡗ")]
        bstack11ll111ll1l_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), bstack11l1l1llll1_opy_, bstack11l1l1lll11_opy_)
        if not os.path.exists(bstack11ll111ll1l_opy_) or not os.path.isdir(bstack11ll111ll1l_opy_):
            self.logger.info(bstack1111_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᡘ").format(bstack11ll111ll1l_opy_))
        else:
            self.logger.info(bstack1111_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᡙ").format(bstack11ll111ll1l_opy_))
            with os.scandir(bstack11ll111ll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111l1l11l_opy_:
                        self.logger.info(bstack1111_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᡚ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111_opy_ (u"ࠧࠨᡛ")
                        log_entry = bstack1ll11lllll1_opy_(
                            kind=bstack1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᡜ"),
                            message=bstack1111_opy_ (u"ࠢࠣᡝ"),
                            level=bstack1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᡞ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111l11ll1_opy_=entry.stat().st_size,
                            bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᡟ"),
                            bstack1llll_opy_=os.path.abspath(entry.path),
                            bstack1l111l1111l_opy_=hook.get(TestFramework.bstack11l1lll1l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111l1l11l_opy_.add(abs_path)
        hook[bstack1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᡠ")] = logs
    def bstack1l11l1l1lll_opy_(
        self,
        bstack1l111ll11l1_opy_: bstack1ll11ll111l_opy_,
        entries: List[bstack1ll11lllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᡡ"))
        req.platform_index = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l11l1ll1_opy_)
        req.client_worker_id = bstack1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᡢ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll11l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll11l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll11l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l1111l11_opy_, bstack1111_opy_ (u"ࠨࠢᡣ"))
            log_entry.test_framework_version = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l111llll11_opy_, bstack1111_opy_ (u"ࠢࠣᡤ"))
            log_entry.uuid = entry.bstack11ll11l1111_opy_ or bstack1111_opy_ (u"ࠣࠤᡥ")
            log_entry.test_framework_state = bstack1l111ll11l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᡦ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1111_opy_ (u"ࠥࠦᡧ")
            if entry.kind == bstack1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᡨ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111l11ll1_opy_
                log_entry.file_path = entry.bstack1llll_opy_
        def bstack1l111ll1111_opy_():
            bstack1l1llll111_opy_ = datetime.now()
            try:
                self.bstack1lll111l111_opy_.LogCreatedEvent(req)
                bstack1l111ll11l1_opy_.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᡩ"), datetime.now() - bstack1l1llll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᡪ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1lllll1l_opy_.enqueue(bstack1l111ll1111_opy_)
    def __11l1lllll11_opy_(self, instance) -> None:
        bstack1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᡫ")
        bstack11ll1l11ll1_opy_ = {bstack1111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᡬ"): bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1llll111_opy_(instance, bstack11ll1l11ll1_opy_)
    @staticmethod
    def bstack11ll11lllll_opy_(instance: bstack1ll11ll111l_opy_, bstack11ll11l1l11_opy_: str):
        bstack11l1llll1l1_opy_ = (
            bstack1ll11ll1l1l_opy_.bstack11ll11ll1ll_opy_
            if bstack11ll11l1l11_opy_ == bstack1ll11ll1l1l_opy_.bstack11ll1111l1l_opy_
            else bstack1ll11ll1l1l_opy_.bstack11ll11lll11_opy_
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
        hook = bstack1ll11ll1l1l_opy_.bstack11ll11lllll_opy_(instance, bstack11ll11l1l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll11l11_opy_, []).clear()
    @staticmethod
    def __11l1ll1llll_opy_(instance: bstack1ll11ll111l_opy_, *args):
        bstack1111_opy_ (u"ࠤࠥࠦࡕࡸ࡯ࡤࡧࡶࡷࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࡸࠨࠢࠣᡭ")
        if len(args) < 1:
            return
        if os.getenv(bstack1111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᡮ"), bstack1111_opy_ (u"ࠦ࠶ࠨᡯ")) != bstack1111_opy_ (u"ࠧ࠷ࠢᡰ"):
            bstack1ll11ll1l1l_opy_.logger.warning(bstack1111_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠ࡭ࡱࡪࡷࠧᡱ"))
            return
        message = args[0]
        if not hasattr(message, bstack1111_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᡲ")):
            return
        is_screenshot = hasattr(message, bstack1111_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᡳ")) and message.kind == bstack1111_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᡴ")
        log_entry = bstack1ll11lllll1_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack1l111l1l1l1_opy_,
            message=message.message if hasattr(message, bstack1111_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᡵ")) else bstack1111_opy_ (u"ࠦࠧᡶ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦᡷ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1111_opy_ (u"ࠨ࡚ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠦᡸ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1111_opy_ (u"ࠢࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥ᡹")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11ll1l111ll_opy_ = {
            bstack1111_opy_ (u"ࠣࡕࡈࡘ࡚ࡖࠢ᡺"): (bstack1ll11ll1l1l_opy_.bstack11ll11l111l_opy_, bstack1ll11ll1l1l_opy_.bstack11ll11lll11_opy_),
            bstack1111_opy_ (u"ࠤࡗࡉࡆࡘࡄࡐ࡙ࡑࠦ᡻"): (bstack1ll11ll1l1l_opy_.bstack11ll1111l1l_opy_, bstack1ll11ll1l1l_opy_.bstack11ll11ll1ll_opy_),
        }
        bstack11l1l1ll111_opy_ = None
        if len(args) > 1:
            bstack11l1l1ll111_opy_ = args[1]
        if bstack11l1l1ll111_opy_ and bstack11l1l1ll111_opy_ in bstack11ll1l111ll_opy_:
            bstack11l1ll111ll_opy_, bstack11l1llll1l1_opy_ = bstack11ll1l111ll_opy_[bstack11l1l1ll111_opy_]
            bstack11ll111111l_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1ll111ll_opy_, None)
            bstack11ll111ll11_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1llll1l1_opy_, None) if bstack11ll111111l_opy_ else None
            if isinstance(bstack11ll111ll11_opy_, dict) and len(bstack11ll111ll11_opy_.get(bstack11ll111111l_opy_, [])) > 0:
                hook = bstack11ll111ll11_opy_[bstack11ll111111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll11l11_opy_ in hook:
                    hook[TestFramework.bstack11l1ll11l11_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l1l1l11ll_opy_(test) -> Dict[str, Any]:
        bstack1111_opy_ (u"ࠥࠦࠧࡖࡡࡳࡵࡨࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡴࡦࡵࡷࠤࡴࡨࡪࡦࡥࡷࠦࠧࠨ᡼")
        test_id = bstack1ll11ll1l1l_opy_.__11l1l1l1l11_opy_(test)
        test_name = test.name if hasattr(test, bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᡽")) else None
        bstack11l1lllll1l_opy_ = str(test.source) if hasattr(test, bstack1111_opy_ (u"ࠧࡹ࡯ࡶࡴࡦࡩࠧ᡾")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1111_opy_ (u"ࠨࡴࡢࡩࡶࠦ᡿")) else []
        bstack11l1l11llll_opy_ =bstack1111_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤᢀ").format(bstack1111_opy_ (u"ࠣࠢࠥᢁ").join(test_tags), test_name) if test_tags else test_name
        bstack11l1l1ll1l1_opy_ = []
        if bstack11l1lllll1l_opy_:
            from browserstack_sdk.bstack1111111l1l_opy_ import RobotHandler
            bstack11l1l1ll1l1_opy_ = RobotHandler.bstack11111l1l11_opy_(bstack11l1lllll1l_opy_)
        if not bstack11l1l1ll1l1_opy_ and test_name:
            bstack11l1l1ll1l1_opy_ = [test_name]
        return {
            TestFramework.bstack1l1l11l1l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1ll1l_opy_: test_id,
            TestFramework.bstack1l1l11lll11_opy_: test_name,
            TestFramework.bstack1l1111lll11_opy_: test_id,
            TestFramework.bstack11l1lll11l1_opy_: bstack11l1lllll1l_opy_,
            TestFramework.bstack11l1ll11l1l_opy_: test_tags,
            TestFramework.bstack11ll111lll1_opy_: bstack11l1l11llll_opy_,
            TestFramework.bstack11lllll111l_opy_: TestFramework.bstack11l1ll11ll1_opy_,
            TestFramework.bstack11ll1lll1l1_opy_: test_id,
            TestFramework.bstack11l1l1lll1l_opy_: bstack11l1l1ll1l1_opy_
        }
    @staticmethod
    def __11l1l1l1l11_opy_(test):
        bstack1111_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡࡷࡱ࡭ࡶࡻࡥࠡࡶࡨࡷࡹࠦࡉࡅࠢࡩࡶࡴࡳࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡷࡩࡸࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤᢂ")
        if hasattr(test, bstack1111_opy_ (u"ࠥ࡭ࡩࠨᢃ")):
            return test.id
        elif hasattr(test, bstack1111_opy_ (u"ࠦࡱࡵ࡮ࡨࡰࡤࡱࡪࠨᢄ")):
            return test.longname
        elif hasattr(test, bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᢅ")):
            return test.name
        return None