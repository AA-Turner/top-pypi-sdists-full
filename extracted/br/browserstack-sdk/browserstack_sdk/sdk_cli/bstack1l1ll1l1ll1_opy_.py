# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11lll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1111l_opy_ import bstack11ll111l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll11l1ll1l_opy_,
    TestHookState,
    bstack1lll11l1l1l_opy_,
    bstack1l1ll11l111_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1111ll1ll_opy_
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1ll1l111_opy_ import bstack1ll1ll1l11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll111ll1ll_opy_ import bstack1l1lllll11l_opy_
from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
bstack1l1111l1lll_opy_ = bstack1l1111ll1ll_opy_()
bstack11ll11llll1_opy_ = 1.0
bstack1l111ll1111_opy_ = bstack1ll111_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᡞ")
bstack11l1l11l1ll_opy_ = bstack1ll111_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᡟ")
bstack11l1l11ll11_opy_ = bstack1ll111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᡠ")
bstack11l1l11llll_opy_ = bstack1ll111_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᡡ")
bstack11l1l11lll1_opy_ = bstack1ll111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᡢ")
_1l111ll1lll_opy_ = set()
class bstack1ll11l1l111_opy_(TestFramework):
    bstack11l11lllll1_opy_ = bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᡣ")
    bstack11ll11ll1l1_opy_ = bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᡤ")
    bstack11ll11l111l_opy_ = bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᡥ")
    bstack11ll11l1lll_opy_ = bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᡦ")
    bstack11l1l1l111l_opy_ = bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᡧ")
    bstack11l1l1111l1_opy_: bool
    bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_ = None
    bstack1ll1lll11ll_opy_ = None
    bstack11l1ll11lll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1lll11ll_opy_: Dict[str, str],
        bstack1l11lll1l1l_opy_: List[str] = [bstack1ll111_opy_ (u"ࠦࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧᡨ")],
        bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_ = None,
        bstack1ll1lll11ll_opy_=None
    ):
        super().__init__(bstack1l11lll1l1l_opy_, bstack11l1lll11ll_opy_, bstack1ll1ll1l111_opy_)
        self.bstack11l1l1111l1_opy_ = any(bstack1ll111_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦᡩ") in item.lower() for item in bstack1l11lll1l1l_opy_)
        self.bstack1ll1lll11ll_opy_ = bstack1ll1lll11ll_opy_
    def track_event(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1ll11l1l111_opy_.bstack11l1ll11lll_opy_:
            bstack11ll111l1ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll111_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᡪ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l1l1111l1_opy_:
            self.logger.warning(bstack1ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࡼࡿࠥᡫ").format(str(self.bstack1l11lll1l1l_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁࡽࠣᡬ").format(args, kwargs))
            return
        instance = self.__11l1lllllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠥᡭ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1ll11l1l111_opy_.bstack11l1ll11lll_opy_:
                bstack1l1l1l111_opy_ = bstack1ll111_opy_ (u"ࠥࠦᡮ")
                name = bstack1ll111_opy_ (u"ࠦࠧᡯ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11l1l11l11l_opy_.value)
                    name = str(EVENTS.bstack11l1l11l11l_opy_.name) + bstack1ll111_opy_ (u"ࠧࡀࠢᡰ") + str(test_framework_state.name)
                else:
                    bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack11l1l11l1l1_opy_.value)
                    name = str(EVENTS.bstack11l1l11l1l1_opy_.name) + bstack1ll111_opy_ (u"ࠨ࠺ࠣᡱ") + str(test_framework_state.name)
                TestFramework.bstack11l1ll1ll11_opy_(instance, name, bstack1l1l1l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᡲ").format(e))
        try:
            if not TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack11llll1lll1_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1ll11l1l111_opy_.__11l1l11111l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll111_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠦᡳ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l1111ll111_opy_):
                    TestFramework.bstack1ll1ll1lll1_opy_(instance, TestFramework.bstack1l1111ll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll111_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥᡴ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_):
                    TestFramework.bstack1ll1ll1lll1_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤᡵ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1ll11l1l111_opy_.__11ll11111ll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll11l1l1l_opy_(instance, *args)
                self.__11l1l1ll111_opy_(instance)
            elif test_framework_state in bstack1ll11l1l111_opy_.bstack11l1ll11lll_opy_:
                self.__11l1ll1llll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠢᡶ").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll11l1111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1ll11l1l111_opy_.bstack11l1ll11lll_opy_:
                bstack1l1l1l111_opy_ = bstack1ll111_opy_ (u"ࠧࠨᡷ")
                name = bstack1ll111_opy_ (u"ࠨࠢᡸ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1l11l11l_opy_.name) + bstack1ll111_opy_ (u"ࠢ࠻ࠤ᡹") + str(test_framework_state.name)
                    bstack1l1l1l111_opy_ = TestFramework.bstack11l1llll1l1_opy_(instance, name)
                    bstack111ll11111_opy_.end(EVENTS.bstack11l1l11l11l_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᡺"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᡻"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1l11l1l1_opy_.name) + bstack1ll111_opy_ (u"ࠥ࠾ࠧ᡼") + str(test_framework_state.name)
                    bstack1l1l1l111_opy_ = TestFramework.bstack11l1llll1l1_opy_(instance, name)
                    bstack111ll11111_opy_.end(EVENTS.bstack11l1l11l1l1_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᡽"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᡾"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ᡿").format(e))
    def bstack1l1111lllll_opy_(self):
        return self.bstack11l1l1111l1_opy_
    def bstack1l111ll111l_opy_(self):
        return False
    def __11l1l111lll_opy_(self, *args):
        bstack1ll111_opy_ (u"ࠢࠣࠤࡓࡥࡷࡹࡥࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡶࡪࡹࡵ࡭ࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧᢀ")
        if len(args) > 1 and hasattr(args[1], bstack1ll111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᢁ")):
            result = args[1]
            if result:
                return TestFramework.bstack1l11l1111l1_opy_(result, [bstack1ll111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᢂ"), bstack1ll111_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᢃ"), bstack1ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠢᢄ"), bstack1ll111_opy_ (u"ࠧ࡫࡮ࡥࡶ࡬ࡱࡪࠨᢅ"), bstack1ll111_opy_ (u"ࠨࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠦᢆ")])
        return None
    def __11ll11l1l1l_opy_(self, instance: bstack1ll11l1ll1l_opy_, *args):
        result = self.__11l1l111lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll11ll1l1_opy_ = None
        status = result.get(bstack1ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᢇ"), bstack1ll111_opy_ (u"ࠣࡐࡒࡘࠥࡘࡕࡏࠤᢈ"))
        if status == bstack1ll111_opy_ (u"ࠤࡉࡅࡎࡒࠢᢉ") and result.get(bstack1ll111_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᢊ")):
            failure = [{bstack1ll111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᢋ"): [result.get(bstack1ll111_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᢌ"), bstack1ll111_opy_ (u"ࠨࠢᢍ"))]}]
            bstack1lll11ll1l1_opy_ = bstack1ll111_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᢎ")
        bstack11ll1111lll_opy_ = TestFramework.bstack11l1lll1111_opy_
        if status == bstack1ll111_opy_ (u"ࠣࡒࡄࡗࡘࠨᢏ"):
            bstack11ll1111lll_opy_ = bstack1ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᢐ")
        elif status == bstack1ll111_opy_ (u"ࠥࡊࡆࡏࡌࠣᢑ"):
            bstack11ll1111lll_opy_ = bstack1ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᢒ")
        elif status == bstack1ll111_opy_ (u"࡙ࠧࡋࡊࡒࠥᢓ"):
            bstack11ll1111lll_opy_ = bstack1ll111_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᢔ")
        if bstack11ll1111lll_opy_ != TestFramework.bstack11l1lll1111_opy_:
            TestFramework.bstack1ll1ll1lll1_opy_(instance, TestFramework.bstack1l111llll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1ll1lll1_opy_(instance, {
            TestFramework.bstack11llll11111_opy_: failure,
            TestFramework.bstack11l1llllll1_opy_: bstack1lll11ll1l1_opy_,
            TestFramework.bstack11lll1llll1_opy_: bstack11ll1111lll_opy_,
        })
    def __11l1lllllll_opy_(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l1l111111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l11llll1l_opy_(test) if test else None
                if target:
                    self.__11l1l111l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᢕ"), None)
            elif hasattr(args[0], bstack1ll111_opy_ (u"ࠣ࡫ࡧࠦᢖ")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1ll1l1ll1l1_opy_(target) if target else None
        return instance
    def __11l1ll1llll_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1l1ll1l1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack1ll11l1l111_opy_.bstack11ll11ll1l1_opy_, {})
        if not key in bstack11l1l1ll1l1_opy_:
            bstack11l1l1ll1l1_opy_[key] = []
        bstack11l1l1lll11_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack1ll11l1l111_opy_.bstack11ll11l111l_opy_, {})
        if not key in bstack11l1l1lll11_opy_:
            bstack11l1l1lll11_opy_[key] = []
        bstack11l1ll1ll1l_opy_ = {
            bstack1ll11l1l111_opy_.bstack11ll11ll1l1_opy_: bstack11l1l1ll1l1_opy_,
            bstack1ll11l1l111_opy_.bstack11ll11l111l_opy_: bstack11l1l1lll11_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1ll111_opy_ (u"ࠤࠥᢗ")
            if len(args) > 0 and hasattr(args[0], bstack1ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᢘ")):
                hook_name = args[0].name
            hook = {
                bstack1ll111_opy_ (u"ࠦࡰ࡫ࡹࠣᢙ"): key,
                TestFramework.bstack11l1l1lll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll11111_opy_: TestFramework.bstack11l1l1l1l11_opy_,
                TestFramework.bstack11l1ll11l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1111111_opy_: [],
                TestFramework.bstack11l1llll111_opy_: hook_name,
                TestFramework.bstack11l1ll1l1l1_opy_: bstack1l1lllll11l_opy_.bstack11ll1111l11_opy_()
            }
            bstack11l1l1ll1l1_opy_[key].append(hook)
            bstack11l1ll1ll1l_opy_[bstack1ll11l1l111_opy_.bstack11ll11l1lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1111l_opy_ = bstack11l1l1ll1l1_opy_.get(key, [])
            hook = bstack11l1ll1111l_opy_.pop() if bstack11l1ll1111l_opy_ else None
            if hook:
                result = self.__11l1l111lll_opy_(*args)
                if result:
                    bstack11l1ll111l1_opy_ = result.get(bstack1ll111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᢚ"), TestFramework.bstack11l1l1l1l11_opy_)
                    if bstack11l1ll111l1_opy_ == bstack1ll111_opy_ (u"ࠨࡐࡂࡕࡖࠦᢛ"):
                        bstack11l1ll111l1_opy_ = bstack1ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᢜ")
                    elif bstack11l1ll111l1_opy_ == bstack1ll111_opy_ (u"ࠣࡈࡄࡍࡑࠨᢝ"):
                        bstack11l1ll111l1_opy_ = bstack1ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᢞ")
                    if bstack11l1ll111l1_opy_ != TestFramework.bstack11l1l1l1l11_opy_:
                        hook[TestFramework.bstack11l1ll11111_opy_] = bstack11l1ll111l1_opy_
                hook[TestFramework.bstack11l1llll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1ll1l1l1_opy_] = bstack1l1lllll11l_opy_.bstack11ll1111l11_opy_()
                self.bstack11l1l1l1lll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1lll111l_opy_, [])
                if logs:
                    self.bstack1l11l11l11l_opy_(instance, logs)
                bstack11l1l1lll11_opy_[key].append(hook)
                bstack11l1ll1ll1l_opy_[bstack1ll11l1l111_opy_.bstack11l1l1l111l_opy_] = key
        TestFramework.bstack11l1ll1lll1_opy_(instance, bstack11l1ll1ll1l_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁ࠳ࢁࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࢁࡽࠣᢟ").format(key, test_hook_state, bstack11l1l1ll1l1_opy_, bstack11l1l1lll11_opy_))
    def __11l1l111111_opy_(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll111_opy_ (u"ࠦࠧࠨࡔࡳࡣࡦ࡯ࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡬ࡧࡼࡻࡴࡸࡤࠡࡧࡹࡩࡳࡺࡳࠡࠪࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡰࡺࡶࡨࡷࡹࠦࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࠤࠥࠦᢠ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᢡ"), None)
        bstack1lll11l1l11_opy_ = getattr(keyword, bstack1ll111_opy_ (u"ࠨࡴࡺࡲࡨࠦᢢ"), None)
        test_id = kwargs.get(bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᢣ"), None)
        if not test_id:
            self.logger.debug(bstack1ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟࡬ࡧࡼࡻࡴࡸࡤࡠࡧࡹࡩࡳࡺ࠺ࠡࡰࡲࠤࡹ࡫ࡳࡵࡡ࡬ࡨࠥ࡯࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠥᢤ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll1l1ll1l1_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠ࡭ࡨࡽࡼࡵࡲࡥࡡࡨࡺࡪࡴࡴ࠻ࠢࡱࡳࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡸࡪࡹࡴࡠ࡫ࡧࡁࢀࢃࠢᢥ").format(test_id))
            return None
        bstack11l1l111ll1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack1ll11l1l111_opy_.bstack11l11lllll1_opy_, {})
        if os.getenv(bstack1ll111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡎࡉ࡞࡝ࡏࡓࡆࡖࠦᢦ"), bstack1ll111_opy_ (u"ࠦ࠶ࠨᢧ")) == bstack1ll111_opy_ (u"ࠧ࠷ࠢᢨ"):
            bstack11l1l11l111_opy_ = bstack1ll111_opy_ (u"ࠨࡻࡾ࠼ࡾࢁᢩࠧ").format(bstack1lll11l1l11_opy_, keyword_name)
            bstack11ll11l1l11_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1l111l11_opy_ = {
                bstack1ll111_opy_ (u"ࠢ࡬ࡧࡼࠦᢪ"): bstack11l1l11l111_opy_,
                bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨ᢫"): keyword_name,
                bstack1ll111_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᢬"): bstack1lll11l1l11_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l1l111l11_opy_[bstack1ll111_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ᢭")] = uuid4().__str__()
                bstack11l1l111l11_opy_[bstack1ll11l1l111_opy_.bstack11l1ll11l1l_opy_] = bstack11ll11l1l11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1l111l11_opy_[bstack1ll11l1l111_opy_.bstack11l1llll1ll_opy_] = bstack11ll11l1l11_opy_
                if len(args) > 1 and hasattr(args[1], bstack1ll111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᢮")):
                    bstack11l1l111l11_opy_[bstack1ll111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᢯")] = args[1].status
            if bstack11l1l11l111_opy_ in bstack11l1l111ll1_opy_:
                bstack11l1l111ll1_opy_[bstack11l1l11l111_opy_].update(bstack11l1l111l11_opy_)
                self.logger.debug(bstack1ll111_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠ࡬ࡧࡼࡻࡴࡸࡤ࠾ࡽࢀࠤࡹࡿࡰࡦ࠿ࡾࢁࠧᢰ").format(keyword_name, bstack1lll11l1l11_opy_))
            else:
                bstack11l1l111ll1_opy_[bstack11l1l11l111_opy_] = bstack11l1l111l11_opy_
                self.logger.debug(bstack1ll111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠣࡸࡾࡶࡥ࠾ࡽࢀࠦᢱ").format(keyword_name, bstack1lll11l1l11_opy_))
        TestFramework.bstack1ll1ll1lll1_opy_(instance, bstack1ll11l1l111_opy_.bstack11l11lllll1_opy_, bstack11l1l111ll1_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠ࡬ࡧࡼࡻࡴࡸࡤࡴ࠿ࡾࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠥᢲ").format(len(bstack11l1l111ll1_opy_), instance.ref()))
        return instance
    def __11l1l111l1l_opy_(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11lll1ll_opy_.create_context(target)
        ob = bstack1ll11l1ll1l_opy_(ctx, self.bstack1l11lll1l1l_opy_, self.bstack11l1lll11ll_opy_, test_framework_state)
        TestFramework.bstack11l1ll1lll1_opy_(ob, {
            TestFramework.bstack1l11llllll1_opy_: context.test_framework_name,
            TestFramework.bstack1l111l111ll_opy_: context.test_framework_version,
            TestFramework.bstack11l1lll1ll1_opy_: [],
            bstack1ll11l1l111_opy_.bstack11l11lllll1_opy_: {},
            bstack1ll11l1l111_opy_.bstack11ll11l111l_opy_: {},
            bstack1ll11l1l111_opy_.bstack11ll11ll1l1_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1ll111_opy_ (u"ࠤࡶࡳࡺࡸࡣࡦࠤᢳ")):
            TestFramework.bstack1ll1ll1lll1_opy_(ob, TestFramework.bstack11ll111l11l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1ll1lll1_opy_(ob, TestFramework.bstack1l1l1l1ll11_opy_, context.platform_index)
        TestFramework.bstack1ll1llllll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࡼࡿࠥᢴ").format(ctx.id, target, args, TestFramework.bstack1ll1llllll1_opy_.keys()))
        return ob
    def bstack1l11111l1ll_opy_(self, instance: bstack1ll11l1ll1l_opy_, bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111l1l_opy_ = (
            bstack1ll11l1l111_opy_.bstack11ll11l1lll_opy_
            if bstack1ll1l1l1l1l_opy_[1] == TestHookState.PRE
            else bstack1ll11l1l111_opy_.bstack11l1l1l111l_opy_
        )
        hook = bstack1ll11l1l111_opy_.bstack11ll11ll111_opy_(instance, bstack11ll1111l1l_opy_)
        entries = hook.get(TestFramework.bstack11ll1111111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11l1lll1ll1_opy_, []))
        return entries
    def bstack1l11l11111l_opy_(self, instance: bstack1ll11l1ll1l_opy_, bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111l1l_opy_ = (
            bstack1ll11l1l111_opy_.bstack11ll11l1lll_opy_
            if bstack1ll1l1l1l1l_opy_[1] == TestHookState.PRE
            else bstack1ll11l1l111_opy_.bstack11l1l1l111l_opy_
        )
        bstack1ll11l1l111_opy_.bstack11l1ll1l1ll_opy_(instance, bstack11ll1111l1l_opy_)
        TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11l1lll1ll1_opy_, []).clear()
    def bstack11l1l1l1lll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᢵ")
        global _1l111ll1lll_opy_
        platform_index = os.environ[bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᢶ")]
        bstack1l111l11111_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l111ll1111_opy_ + str(platform_index)), bstack11l1l11llll_opy_)
        if not os.path.exists(bstack1l111l11111_opy_) or not os.path.isdir(bstack1l111l11111_opy_):
            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦᢷ").format(bstack1l111l11111_opy_))
            return
        logs = hook.get(bstack1ll111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᢸ"), [])
        with os.scandir(bstack1l111l11111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111ll1lll_opy_:
                    self.logger.info(bstack1ll111_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᢹ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll111_opy_ (u"ࠤࠥᢺ")
                    log_entry = bstack1l1ll11l111_opy_(
                        kind=bstack1ll111_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᢻ"),
                        message=bstack1ll111_opy_ (u"ࠦࠧᢼ"),
                        level=bstack1ll111_opy_ (u"ࠧࠨᢽ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111lll111_opy_=entry.stat().st_size,
                        bstack1l111lllll1_opy_=bstack1ll111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᢾ"),
                        bstack11l111_opy_=os.path.abspath(entry.path),
                        bstack11l1lllll11_opy_=hook.get(TestFramework.bstack11l1l1lll1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111ll1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᢿ")]
        bstack11ll11l11ll_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l111ll1111_opy_ + str(platform_index)), bstack11l1l11llll_opy_, bstack11l1l11lll1_opy_)
        if not os.path.exists(bstack11ll11l11ll_opy_) or not os.path.isdir(bstack11ll11l11ll_opy_):
            self.logger.info(bstack1ll111_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᣀ").format(bstack11ll11l11ll_opy_))
        else:
            self.logger.info(bstack1ll111_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᣁ").format(bstack11ll11l11ll_opy_))
            with os.scandir(bstack11ll11l11ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111ll1lll_opy_:
                        self.logger.info(bstack1ll111_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᣂ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll111_opy_ (u"ࠦࠧᣃ")
                        log_entry = bstack1l1ll11l111_opy_(
                            kind=bstack1ll111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᣄ"),
                            message=bstack1ll111_opy_ (u"ࠨࠢᣅ"),
                            level=bstack1ll111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᣆ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111lll111_opy_=entry.stat().st_size,
                            bstack1l111lllll1_opy_=bstack1ll111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᣇ"),
                            bstack11l111_opy_=os.path.abspath(entry.path),
                            bstack1l11l1l11ll_opy_=hook.get(TestFramework.bstack11l1l1lll1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111ll1lll_opy_.add(abs_path)
        hook[bstack1ll111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᣈ")] = logs
    def bstack1l11l11l11l_opy_(
        self,
        bstack1l111l11l1l_opy_: bstack1ll11l1ll1l_opy_,
        entries: List[bstack1l1ll11l111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᣉ"))
        req.platform_index = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack1ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᣊ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111l11l1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111l11l1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111l11l1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l11llllll1_opy_, bstack1ll111_opy_ (u"ࠧࠨᣋ"))
            log_entry.test_framework_version = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l111l111ll_opy_, bstack1ll111_opy_ (u"ࠨࠢᣌ"))
            log_entry.uuid = entry.bstack11l1lllll11_opy_ or bstack1ll111_opy_ (u"ࠢࠣᣍ")
            log_entry.test_framework_state = bstack1l111l11l1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᣎ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll111_opy_ (u"ࠤࠥᣏ")
            if entry.kind == bstack1ll111_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᣐ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111lll111_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1111l1l11_opy_():
            bstack1ll1l1l111_opy_ = datetime.now()
            try:
                self.bstack1ll1lll11ll_opy_.LogCreatedEvent(req)
                bstack1l111l11l1l_opy_.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᣑ"), datetime.now() - bstack1ll1l1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᣒ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1ll1l111_opy_.enqueue(bstack1l1111l1l11_opy_)
    def __11l1l1ll111_opy_(self, instance) -> None:
        bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᣓ")
        bstack11l1ll1ll1l_opy_ = {bstack1ll111_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᣔ"): bstack1l1lllll11l_opy_.bstack11ll1111l11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1ll1lll1_opy_(instance, bstack11l1ll1ll1l_opy_)
    @staticmethod
    def bstack11ll11ll111_opy_(instance: bstack1ll11l1ll1l_opy_, bstack11ll1111l1l_opy_: str):
        bstack11ll11ll1ll_opy_ = (
            bstack1ll11l1l111_opy_.bstack11ll11l111l_opy_
            if bstack11ll1111l1l_opy_ == bstack1ll11l1l111_opy_.bstack11l1l1l111l_opy_
            else bstack1ll11l1l111_opy_.bstack11ll11ll1l1_opy_
        )
        bstack11ll11ll11l_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11ll1111l1l_opy_, None)
        bstack11ll11111l1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11ll11ll1ll_opy_, None) if bstack11ll11ll11l_opy_ else None
        return (
            bstack11ll11111l1_opy_[bstack11ll11ll11l_opy_][-1]
            if isinstance(bstack11ll11111l1_opy_, dict) and len(bstack11ll11111l1_opy_.get(bstack11ll11ll11l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll1l1ll_opy_(instance: bstack1ll11l1ll1l_opy_, bstack11ll1111l1l_opy_: str):
        hook = bstack1ll11l1l111_opy_.bstack11ll11ll111_opy_(instance, bstack11ll1111l1l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1111111_opy_, []).clear()
    @staticmethod
    def __11ll11111ll_opy_(instance: bstack1ll11l1ll1l_opy_, *args):
        bstack1ll111_opy_ (u"ࠣࠤࠥࡔࡷࡵࡣࡦࡵࡶࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࡷࠧࠨࠢᣕ")
        if len(args) < 1:
            return
        if os.getenv(bstack1ll111_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᣖ"), bstack1ll111_opy_ (u"ࠥ࠵ࠧᣗ")) != bstack1ll111_opy_ (u"ࠦ࠶ࠨᣘ"):
            bstack1ll11l1l111_opy_.logger.warning(bstack1ll111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦ࡬ࡰࡩࡶࠦᣙ"))
            return
        message = args[0]
        if not hasattr(message, bstack1ll111_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᣚ")):
            return
        is_screenshot = hasattr(message, bstack1ll111_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᣛ")) and message.kind == bstack1ll111_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᣜ")
        log_entry = bstack1l1ll11l111_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack1l11l11ll1l_opy_,
            message=message.message if hasattr(message, bstack1ll111_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᣝ")) else bstack1ll111_opy_ (u"ࠥࠦᣞ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1ll111_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᣟ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1ll111_opy_ (u"࡙ࠧࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠥᣠ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠤᣡ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l1ll11ll1_opy_ = {
            bstack1ll111_opy_ (u"ࠢࡔࡇࡗ࡙ࡕࠨᣢ"): (bstack1ll11l1l111_opy_.bstack11ll11l1lll_opy_, bstack1ll11l1l111_opy_.bstack11ll11ll1l1_opy_),
            bstack1ll111_opy_ (u"ࠣࡖࡈࡅࡗࡊࡏࡘࡐࠥᣣ"): (bstack1ll11l1l111_opy_.bstack11l1l1l111l_opy_, bstack1ll11l1l111_opy_.bstack11ll11l111l_opy_),
        }
        bstack11l1l1111ll_opy_ = None
        if len(args) > 1:
            bstack11l1l1111ll_opy_ = args[1]
        if bstack11l1l1111ll_opy_ and bstack11l1l1111ll_opy_ in bstack11l1ll11ll1_opy_:
            bstack11l1lll11l1_opy_, bstack11ll11ll1ll_opy_ = bstack11l1ll11ll1_opy_[bstack11l1l1111ll_opy_]
            bstack11l1ll1l11l_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11l1lll11l1_opy_, None)
            bstack11ll11111l1_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, bstack11ll11ll1ll_opy_, None) if bstack11l1ll1l11l_opy_ else None
            if isinstance(bstack11ll11111l1_opy_, dict) and len(bstack11ll11111l1_opy_.get(bstack11l1ll1l11l_opy_, [])) > 0:
                hook = bstack11ll11111l1_opy_[bstack11l1ll1l11l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1111111_opy_ in hook:
                    hook[TestFramework.bstack11ll1111111_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack11l1lll1ll1_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l1l11111l_opy_(test) -> Dict[str, Any]:
        bstack1ll111_opy_ (u"ࠤࠥࠦࡕࡧࡲࡴࡧࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡺࡥࡴࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧᣤ")
        test_id = bstack1ll11l1l111_opy_.__11l11llll1l_opy_(test)
        test_name = test.name if hasattr(test, bstack1ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᣥ")) else None
        bstack11l1ll111ll_opy_ = str(test.source) if hasattr(test, bstack1ll111_opy_ (u"ࠦࡸࡵࡵࡳࡥࡨࠦᣦ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1ll111_opy_ (u"ࠧࡺࡡࡨࡵࠥᣧ")) else []
        bstack11l11llllll_opy_ =bstack1ll111_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣᣨ").format(bstack1ll111_opy_ (u"ࠢࠡࠤᣩ").join(test_tags), test_name) if test_tags else test_name
        bstack11l1l1l1111_opy_ = []
        if bstack11l1ll111ll_opy_:
            from browserstack_sdk.bstack1llllllll11_opy_ import RobotHandler
            bstack11l1l1l1111_opy_ = RobotHandler.bstack111111l1l1_opy_(bstack11l1ll111ll_opy_)
        if not bstack11l1l1l1111_opy_ and test_name:
            bstack11l1l1l1111_opy_ = [test_name]
        return {
            TestFramework.bstack1l1l1ll11ll_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1lll1_opy_: test_id,
            TestFramework.bstack1l1l11llll1_opy_: test_name,
            TestFramework.bstack1l11111l1l1_opy_: test_id,
            TestFramework.bstack11ll111l111_opy_: bstack11l1ll111ll_opy_,
            TestFramework.bstack11ll111llll_opy_: test_tags,
            TestFramework.bstack11l1lll1l11_opy_: bstack11l11llllll_opy_,
            TestFramework.bstack11lll1llll1_opy_: TestFramework.bstack11l1lll1111_opy_,
            TestFramework.bstack11ll1l1l1ll_opy_: test_id,
            TestFramework.bstack11l1l11ll1l_opy_: bstack11l1l1l1111_opy_
        }
    @staticmethod
    def __11l11llll1l_opy_(test):
        bstack1ll111_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡶࡰ࡬ࡵࡺ࡫ࠠࡵࡧࡶࡸࠥࡏࡄࠡࡨࡵࡳࡲࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡶࡨࡷࡹࠦ࡯ࡣ࡬ࡨࡧࡹࠨࠢࠣᣪ")
        if hasattr(test, bstack1ll111_opy_ (u"ࠤ࡬ࡨࠧᣫ")):
            return test.id
        elif hasattr(test, bstack1ll111_opy_ (u"ࠥࡰࡴࡴࡧ࡯ࡣࡰࡩࠧᣬ")):
            return test.longname
        elif hasattr(test, bstack1ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᣭ")):
            return test.name
        return None