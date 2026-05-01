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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1ll11l1_opy_,
    TestHookState,
    bstack1ll1lllll1l_opy_,
    bstack11l1l1l1ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11ll11l1lll_opy_
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1lll1111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l11ll1l1_opy_ import bstack1l11ll1111l_opy_
from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
bstack11ll11l1ll1_opy_ = bstack11ll11l1lll_opy_()
bstack111llll1l1l_opy_ = 1.0
bstack11ll1ll1l11_opy_ = bstack111ll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᩪ")
bstack111ll1111ll_opy_ = bstack111ll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᩫ")
bstack111l1llll11_opy_ = bstack111ll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᩬ")
bstack111l1lllll1_opy_ = bstack111ll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᩭ")
bstack111l1llll1l_opy_ = bstack111ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᩮ")
_11ll111lll1_opy_ = set()
class bstack1l11l111ll1_opy_(TestFramework):
    bstack111l1ll1ll1_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᩯ")
    bstack111ll1l1ll1_opy_ = bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᩰ")
    bstack111lll11l1l_opy_ = bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᩱ")
    bstack111lllll11l_opy_ = bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᩲ")
    bstack111llll1ll1_opy_ = bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᩳ")
    bstack111l1ll11ll_opy_: bool
    bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_ = None
    bstack111111ll1l_opy_ = None
    bstack111llll111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll11l_opy_: Dict[str, str],
        bstack1l1l11l1111_opy_: List[str] = [bstack111ll_opy_ (u"ࠥࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦᩴ")],
        bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_ = None,
        bstack111111ll1l_opy_=None
    ):
        super().__init__(bstack1l1l11l1111_opy_, bstack1l11llll11l_opy_, bstack1l1ll1llll1_opy_)
        self.bstack111l1ll11ll_opy_ = any(bstack111ll_opy_ (u"ࠦࡷࡵࡢࡰࡶࠥ᩵") in item.lower() for item in bstack1l1l11l1111_opy_)
        self.bstack111111ll1l_opy_ = bstack111111ll1l_opy_
    def track_event(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l11l111ll1_opy_.bstack111llll111l_opy_:
            bstack111ll1ll1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111ll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠤ᩶").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111l1ll11ll_opy_:
            self.logger.warning(bstack111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࡻࡾࠤ᩷").format(str(self.bstack1l1l11l1111_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢ᩸").format(args, kwargs))
            return
        instance = self.__11l11111lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠤ᩹").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l11l111ll1_opy_.bstack111llll111l_opy_:
                bstack11111l11l_opy_ = bstack111ll_opy_ (u"ࠤࠥ᩺")
                name = bstack111ll_opy_ (u"ࠥࠦ᩻")
                if (test_hook_state == TestHookState.PRE):
                    bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111l1llllll_opy_.value)
                    name = str(EVENTS.bstack111l1llllll_opy_.name) + bstack111ll_opy_ (u"ࠦ࠿ࠨ᩼") + str(test_framework_state.name)
                else:
                    bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111ll1111l1_opy_.value)
                    name = str(EVENTS.bstack111ll1111l1_opy_.name) + bstack111ll_opy_ (u"ࠧࡀࠢ᩽") + str(test_framework_state.name)
                TestFramework.bstack111ll1l1l1l_opy_(instance, name, bstack11111l11l_opy_)
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥ᩾").format(e))
        try:
            if not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l11l111ll1_opy_.__111l1ll1lll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111ll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿ᩿ࠥ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤ᪀").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11llll_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11lll11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣ᪁").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l11l111ll1_opy_.__111lll1ll11_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111ll1ll111_opy_(instance, *args)
                self.__111llll11l1_opy_(instance)
            elif test_framework_state in bstack1l11l111ll1_opy_.bstack111llll111l_opy_:
                self.__111ll11l1l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠨ᪂").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111ll1l1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l11l111ll1_opy_.bstack111llll111l_opy_:
                bstack11111l11l_opy_ = bstack111ll_opy_ (u"ࠦࠧ᪃")
                name = bstack111ll_opy_ (u"ࠧࠨ᪄")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111l1llllll_opy_.name) + bstack111ll_opy_ (u"ࠨ࠺ࠣ᪅") + str(test_framework_state.name)
                    bstack11111l11l_opy_ = TestFramework.bstack111ll1lllll_opy_(instance, name)
                    bstack111l1l1l_opy_.end(EVENTS.bstack111l1llllll_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᪆"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᪇"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll1111l1_opy_.name) + bstack111ll_opy_ (u"ࠤ࠽ࠦ᪈") + str(test_framework_state.name)
                    bstack11111l11l_opy_ = TestFramework.bstack111ll1lllll_opy_(instance, name)
                    bstack111l1l1l_opy_.end(EVENTS.bstack111ll1111l1_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᪉"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᪊"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ᪋").format(e))
    def bstack11ll1ll1l1l_opy_(self):
        return self.bstack111l1ll11ll_opy_
    def bstack11ll1l111ll_opy_(self):
        return False
    def __111l1lll111_opy_(self, *args):
        bstack111ll_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡵࡩࡸࡻ࡬ࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦ᪌")
        if len(args) > 1 and hasattr(args[1], bstack111ll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᪍")):
            result = args[1]
            if result:
                return TestFramework.bstack11lll1111ll_opy_(result, [bstack111ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᪎"), bstack111ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ᪏"), bstack111ll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡶ࡬ࡱࡪࠨ᪐"), bstack111ll_opy_ (u"ࠦࡪࡴࡤࡵ࡫ࡰࡩࠧ᪑"), bstack111ll_opy_ (u"ࠧ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠥ᪒")])
        return None
    def __111ll1ll111_opy_(self, instance: bstack1l1l1ll11l1_opy_, *args):
        result = self.__111l1lll111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l111l_opy_ = None
        status = result.get(bstack111ll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᪓"), bstack111ll_opy_ (u"ࠢࡏࡑࡗࠤࡗ࡛ࡎࠣ᪔"))
        if status == bstack111ll_opy_ (u"ࠣࡈࡄࡍࡑࠨ᪕") and result.get(bstack111ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ᪖")):
            failure = [{bstack111ll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᪗"): [result.get(bstack111ll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ᪘"), bstack111ll_opy_ (u"ࠧࠨ᪙"))]}]
            bstack1ll111l111l_opy_ = bstack111ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᪚")
        bstack111llllll1l_opy_ = TestFramework.bstack11l11111111_opy_
        if status == bstack111ll_opy_ (u"ࠢࡑࡃࡖࡗࠧ᪛"):
            bstack111llllll1l_opy_ = bstack111ll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ᪜")
        elif status == bstack111ll_opy_ (u"ࠤࡉࡅࡎࡒࠢ᪝"):
            bstack111llllll1l_opy_ = bstack111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ᪞")
        elif status == bstack111ll_opy_ (u"ࠦࡘࡑࡉࡑࠤ᪟"):
            bstack111llllll1l_opy_ = bstack111ll_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨ᪠")
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
            instance = self.__111l1ll1l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111l1ll11l1_opy_(test) if test else None
                if target:
                    self.__111l1ll1l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢ᪡"), None)
            elif hasattr(args[0], bstack111ll_opy_ (u"ࠢࡪࡦࠥ᪢")) if len(args) > 0 else False:
                target = args[0].id
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
        bstack111ll1l1lll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack1l11l111ll1_opy_.bstack111ll1l1ll1_opy_, {})
        if not key in bstack111ll1l1lll_opy_:
            bstack111ll1l1lll_opy_[key] = []
        bstack111lll111l1_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack1l11l111ll1_opy_.bstack111lll11l1l_opy_, {})
        if not key in bstack111lll111l1_opy_:
            bstack111lll111l1_opy_[key] = []
        bstack111llllllll_opy_ = {
            bstack1l11l111ll1_opy_.bstack111ll1l1ll1_opy_: bstack111ll1l1lll_opy_,
            bstack1l11l111ll1_opy_.bstack111lll11l1l_opy_: bstack111lll111l1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack111ll_opy_ (u"ࠣࠤ᪣")
            if len(args) > 0 and hasattr(args[0], bstack111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪤")):
                hook_name = args[0].name
            hook = {
                bstack111ll_opy_ (u"ࠥ࡯ࡪࡿࠢ᪥"): key,
                TestFramework.bstack111llll1111_opy_: uuid4().__str__(),
                TestFramework.bstack111ll1l11l1_opy_: TestFramework.bstack111lll1lll1_opy_,
                TestFramework.bstack111lll1llll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll11l111_opy_: [],
                TestFramework.bstack111ll11ll1l_opy_: hook_name,
                TestFramework.bstack11l11111l1l_opy_: bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()
            }
            bstack111ll1l1lll_opy_[key].append(hook)
            bstack111llllllll_opy_[bstack1l11l111ll1_opy_.bstack111lllll11l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l111l111l_opy_ = bstack111ll1l1lll_opy_.get(key, [])
            hook = bstack11l111l111l_opy_.pop() if bstack11l111l111l_opy_ else None
            if hook:
                result = self.__111l1lll111_opy_(*args)
                if result:
                    bstack111ll11l11l_opy_ = result.get(bstack111ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᪦"), TestFramework.bstack111lll1lll1_opy_)
                    if bstack111ll11l11l_opy_ == bstack111ll_opy_ (u"ࠧࡖࡁࡔࡕࠥᪧ"):
                        bstack111ll11l11l_opy_ = bstack111ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ᪨")
                    elif bstack111ll11l11l_opy_ == bstack111ll_opy_ (u"ࠢࡇࡃࡌࡐࠧ᪩"):
                        bstack111ll11l11l_opy_ = bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ᪪")
                    if bstack111ll11l11l_opy_ != TestFramework.bstack111lll1lll1_opy_:
                        hook[TestFramework.bstack111ll1l11l1_opy_] = bstack111ll11l11l_opy_
                hook[TestFramework.bstack111llll1l11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l11111l1l_opy_] = bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()
                self.bstack111lll1l1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll111lll_opy_, [])
                if logs:
                    self.bstack1l1111ll1l_opy_(instance, logs)
                bstack111lll111l1_opy_[key].append(hook)
                bstack111llllllll_opy_[bstack1l11l111ll1_opy_.bstack111llll1ll1_opy_] = key
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀ࠲ࢀࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࢀࢃࠢ᪫").format(key, test_hook_state, bstack111ll1l1lll_opy_, bstack111lll111l1_opy_))
    def __111l1ll1l1l_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll_opy_ (u"࡚ࠥࠦࠧࡲࡢࡥ࡮ࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡫ࡦࡻࡺࡳࡷࡪࠠࡦࡸࡨࡲࡹࡹࠠࠩࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࠣࠤࠥ᪬")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪭"), None)
        bstack1ll1111l1ll_opy_ = getattr(keyword, bstack111ll_opy_ (u"ࠧࡺࡹࡱࡧࠥ᪮"), None)
        test_id = kwargs.get(bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢ᪯"), None)
        if not test_id:
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥ࡫ࡦࡻࡺࡳࡷࡪ࡟ࡦࡸࡨࡲࡹࡀࠠ࡯ࡱࠣࡸࡪࡹࡴࡠ࡫ࡧࠤ࡮ࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠤ᪰").format(keyword_name))
            return None
        instance = TestFramework.bstack1l1l1llllll_opy_(test_id)
        if not instance:
            self.logger.warning(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟࡬ࡧࡼࡻࡴࡸࡤࡠࡧࡹࡩࡳࡺ࠺ࠡࡰࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡷࡩࡸࡺ࡟ࡪࡦࡀࡿࢂࠨ᪱").format(test_id))
            return None
        bstack111l1lll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack1l11l111ll1_opy_.bstack111l1ll1ll1_opy_, {})
        if os.getenv(bstack111ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡍࡈ࡝࡜ࡕࡒࡅࡕࠥ᪲"), bstack111ll_opy_ (u"ࠥ࠵ࠧ᪳")) == bstack111ll_opy_ (u"ࠦ࠶ࠨ᪴"):
            bstack111l1ll111l_opy_ = bstack111ll_opy_ (u"ࠧࢁࡽ࠻ࡽࢀ᪵ࠦ").format(bstack1ll1111l1ll_opy_, keyword_name)
            bstack11l111111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1lll11l_opy_ = {
                bstack111ll_opy_ (u"ࠨ࡫ࡦࡻ᪶ࠥ"): bstack111l1ll111l_opy_,
                bstack111ll_opy_ (u"ࠢ࡯ࡣࡰࡩ᪷ࠧ"): keyword_name,
                bstack111ll_opy_ (u"ࠣࡶࡼࡴࡪࠨ᪸"): bstack1ll1111l1ll_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l1lll11l_opy_[bstack111ll_opy_ (u"ࠤࡸࡹ࡮ࡪ᪹ࠢ")] = uuid4().__str__()
                bstack111l1lll11l_opy_[bstack1l11l111ll1_opy_.bstack111lll1llll_opy_] = bstack11l111111ll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1lll11l_opy_[bstack1l11l111ll1_opy_.bstack111llll1l11_opy_] = bstack11l111111ll_opy_
                if len(args) > 1 and hasattr(args[1], bstack111ll_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵ᪺ࠥ")):
                    bstack111l1lll11l_opy_[bstack111ll_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᪻")] = args[1].status
            if bstack111l1ll111l_opy_ in bstack111l1lll1ll_opy_:
                bstack111l1lll1ll_opy_[bstack111l1ll111l_opy_].update(bstack111l1lll11l_opy_)
                self.logger.debug(bstack111ll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠣࡸࡾࡶࡥ࠾ࡽࢀࠦ᪼").format(keyword_name, bstack1ll1111l1ll_opy_))
            else:
                bstack111l1lll1ll_opy_[bstack111l1ll111l_opy_] = bstack111l1lll11l_opy_
                self.logger.debug(bstack111ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥࡱࡥࡺࡹࡲࡶࡩࡃࡻࡾࠢࡷࡽࡵ࡫࠽ࡼࡿ᪽ࠥ").format(keyword_name, bstack1ll1111l1ll_opy_))
        TestFramework.bstack11ll11l1_opy_(instance, bstack1l11l111ll1_opy_.bstack111l1ll1ll1_opy_, bstack111l1lll1ll_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪࡳ࠾ࡽࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠤ᪾").format(len(bstack111l1lll1ll_opy_), instance.ref()))
        return instance
    def __111l1ll1l11_opy_(
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
            bstack1l11l111ll1_opy_.bstack111l1ll1ll1_opy_: {},
            bstack1l11l111ll1_opy_.bstack111lll11l1l_opy_: {},
            bstack1l11l111ll1_opy_.bstack111ll1l1ll1_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack111ll_opy_ (u"ࠣࡵࡲࡹࡷࡩࡥᪿࠣ")):
            TestFramework.bstack11ll11l1_opy_(ob, TestFramework.bstack11l1111l1l1_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack11ll11l1_opy_(ob, TestFramework.bstack1l111111111_opy_, context.platform_index)
        TestFramework.bstack111l11l1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack111ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࡻࡾࠤᫀ").format(ctx.id, target, args, TestFramework.bstack111l11l1l1_opy_.keys()))
        return ob
    def bstack11lll111l1l_opy_(self, instance: bstack1l1l1ll11l1_opy_, bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1111l11l_opy_ = (
            bstack1l11l111ll1_opy_.bstack111lllll11l_opy_
            if bstack1l1l1lll11l_opy_[1] == TestHookState.PRE
            else bstack1l11l111ll1_opy_.bstack111llll1ll1_opy_
        )
        hook = bstack1l11l111ll1_opy_.bstack111ll11ll11_opy_(instance, bstack11l1111l11l_opy_)
        entries = hook.get(TestFramework.bstack111ll11l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, []))
        return entries
    def bstack11lll11l1ll_opy_(self, instance: bstack1l1l1ll11l1_opy_, bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1111l11l_opy_ = (
            bstack1l11l111ll1_opy_.bstack111lllll11l_opy_
            if bstack1l1l1lll11l_opy_[1] == TestHookState.PRE
            else bstack1l11l111ll1_opy_.bstack111llll1ll1_opy_
        )
        bstack1l11l111ll1_opy_.bstack11l1111111l_opy_(instance, bstack11l1111l11l_opy_)
        TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, []).clear()
    def bstack111lll1l1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᫁")
        global _11ll111lll1_opy_
        platform_index = os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᫂")]
        bstack11ll11lllll_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), bstack111l1lllll1_opy_)
        if not os.path.exists(bstack11ll11lllll_opy_) or not os.path.isdir(bstack11ll11lllll_opy_):
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿ᫃ࠥ").format(bstack11ll11lllll_opy_))
            return
        logs = hook.get(bstack111ll_opy_ (u"ࠨ࡬ࡰࡩࡶ᫄ࠦ"), [])
        with os.scandir(bstack11ll11lllll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll111lll1_opy_:
                    self.logger.info(bstack111ll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧ᫅").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111ll_opy_ (u"ࠣࠤ᫆")
                    log_entry = bstack11l1l1l1ll_opy_(
                        kind=bstack111ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᫇"),
                        message=bstack111ll_opy_ (u"ࠥࠦ᫈"),
                        level=bstack111ll_opy_ (u"ࠦࠧ᫉"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1lll111_opy_=entry.stat().st_size,
                        bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈ᫊ࠧ"),
                        bstack111l1_opy_=os.path.abspath(entry.path),
                        bstack111llllll11_opy_=hook.get(TestFramework.bstack111llll1111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll111lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᫋")]
        bstack111lllll1l1_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), bstack111l1lllll1_opy_, bstack111l1llll1l_opy_)
        if not os.path.exists(bstack111lllll1l1_opy_) or not os.path.isdir(bstack111lllll1l1_opy_):
            self.logger.info(bstack111ll_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᫌ").format(bstack111lllll1l1_opy_))
        else:
            self.logger.info(bstack111ll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᫍ").format(bstack111lllll1l1_opy_))
            with os.scandir(bstack111lllll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll111lll1_opy_:
                        self.logger.info(bstack111ll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᫎ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111ll_opy_ (u"ࠥࠦ᫏")
                        log_entry = bstack11l1l1l1ll_opy_(
                            kind=bstack111ll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᫐"),
                            message=bstack111ll_opy_ (u"ࠧࠨ᫑"),
                            level=bstack111ll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ᫒"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1lll111_opy_=entry.stat().st_size,
                            bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ᫓"),
                            bstack111l1_opy_=os.path.abspath(entry.path),
                            bstack11lll11ll1l_opy_=hook.get(TestFramework.bstack111llll1111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll111lll1_opy_.add(abs_path)
        hook[bstack111ll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᫔")] = logs
    def bstack1l1111ll1l_opy_(
        self,
        bstack1llllllll_opy_: bstack1l1l1ll11l1_opy_,
        entries: List[bstack11l1l1l1ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨ᫕"))
        req.platform_index = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l111111111_opy_)
        req.client_worker_id = bstack111ll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᫖").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1llllllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1llllllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1llllllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l1111l111l_opy_, bstack111ll_opy_ (u"ࠦࠧ᫗"))
            log_entry.test_framework_version = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack11ll1l11l1l_opy_, bstack111ll_opy_ (u"ࠧࠨ᫘"))
            log_entry.uuid = entry.bstack111llllll11_opy_ or bstack111ll_opy_ (u"ࠨࠢ᫙")
            log_entry.test_framework_state = bstack1llllllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᫚"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111ll_opy_ (u"ࠣࠤ᫛")
            if entry.kind == bstack111ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᫜"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1lll111_opy_
                log_entry.file_path = entry.bstack111l1_opy_
        def bstack11lll111lll_opy_():
            bstack1l11111lll_opy_ = datetime.now()
            try:
                self.bstack111111ll1l_opy_.LogCreatedEvent(req)
                bstack1llllllll_opy_.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ᫝"), datetime.now() - bstack1l11111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥ᫞").format(str(e)))
                traceback.print_exc()
        self.bstack1l1ll1llll1_opy_.enqueue(bstack11lll111lll_opy_)
    def __111llll11l1_opy_(self, instance) -> None:
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᫟")
        bstack111llllllll_opy_ = {bstack111ll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣ᫠"): bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        bstack1l11ll1111l_opy_.bstack111lll11lll_opy_()
    @staticmethod
    def bstack111ll11ll11_opy_(instance: bstack1l1l1ll11l1_opy_, bstack11l1111l11l_opy_: str):
        bstack111lll1111l_opy_ = (
            bstack1l11l111ll1_opy_.bstack111lll11l1l_opy_
            if bstack11l1111l11l_opy_ == bstack1l11l111ll1_opy_.bstack111llll1ll1_opy_
            else bstack1l11l111ll1_opy_.bstack111ll1l1ll1_opy_
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
        hook = bstack1l11l111ll1_opy_.bstack111ll11ll11_opy_(instance, bstack11l1111l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll11l111_opy_, []).clear()
    @staticmethod
    def __111lll1ll11_opy_(instance: bstack1l1l1ll11l1_opy_, *args):
        bstack111ll_opy_ (u"ࠢࠣࠤࡓࡶࡴࡩࡥࡴࡵࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡲ࡯ࡨࠢࡰࡩࡸࡹࡡࡨࡧࡶࠦࠧࠨ᫡")
        if len(args) < 1:
            return
        if os.getenv(bstack111ll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧ᫢"), bstack111ll_opy_ (u"ࠤ࠴ࠦ᫣")) != bstack111ll_opy_ (u"ࠥ࠵ࠧ᫤"):
            bstack1l11l111ll1_opy_.logger.warning(bstack111ll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡲ࡯ࡨࡵࠥ᫥"))
            return
        message = args[0]
        if not hasattr(message, bstack111ll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨ᫦")):
            return
        is_screenshot = hasattr(message, bstack111ll_opy_ (u"࠭࡫ࡪࡰࡧࠫ᫧")) and message.kind == bstack111ll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᫨")
        log_entry = bstack11l1l1l1ll_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11ll1l1l1ll_opy_,
            message=message.message if hasattr(message, bstack111ll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ᫩")) else bstack111ll_opy_ (u"ࠤࠥ᫪"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack111ll_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࠤ᫫")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack111ll_opy_ (u"ࠦࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠤ᫬")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack111ll_opy_ (u"ࠧࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠣ᫭")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111llll11ll_opy_ = {
            bstack111ll_opy_ (u"ࠨࡓࡆࡖࡘࡔࠧ᫮"): (bstack1l11l111ll1_opy_.bstack111lllll11l_opy_, bstack1l11l111ll1_opy_.bstack111ll1l1ll1_opy_),
            bstack111ll_opy_ (u"ࠢࡕࡇࡄࡖࡉࡕࡗࡏࠤ᫯"): (bstack1l11l111ll1_opy_.bstack111llll1ll1_opy_, bstack1l11l111ll1_opy_.bstack111lll11l1l_opy_),
        }
        bstack111l1lll1l1_opy_ = None
        if len(args) > 1:
            bstack111l1lll1l1_opy_ = args[1]
        if bstack111l1lll1l1_opy_ and bstack111l1lll1l1_opy_ in bstack111llll11ll_opy_:
            bstack111lll1l111_opy_, bstack111lll1111l_opy_ = bstack111llll11ll_opy_[bstack111l1lll1l1_opy_]
            bstack11l111l1111_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1l111_opy_, None)
            bstack111lllll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1111l_opy_, None) if bstack11l111l1111_opy_ else None
            if isinstance(bstack111lllll1ll_opy_, dict) and len(bstack111lllll1ll_opy_.get(bstack11l111l1111_opy_, [])) > 0:
                hook = bstack111lllll1ll_opy_[bstack11l111l1111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll11l111_opy_ in hook:
                    hook[TestFramework.bstack111ll11l111_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1ll1lll_opy_(test) -> Dict[str, Any]:
        bstack111ll_opy_ (u"ࠣࠤࠥࡔࡦࡸࡳࡦࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡹ࡫ࡳࡵࠢࡲࡦ࡯࡫ࡣࡵࠤࠥࠦ᫰")
        test_id = bstack1l11l111ll1_opy_.__111l1ll11l1_opy_(test)
        test_name = test.name if hasattr(test, bstack111ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫱")) else None
        bstack11l1111l111_opy_ = str(test.source) if hasattr(test, bstack111ll_opy_ (u"ࠥࡷࡴࡻࡲࡤࡧࠥ᫲")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack111ll_opy_ (u"ࠦࡹࡧࡧࡴࠤ᫳")) else []
        bstack111l1ll1111_opy_ =bstack111ll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢ᫴").format(bstack111ll_opy_ (u"ࠨࠠࠣ᫵").join(test_tags), test_name) if test_tags else test_name
        bstack111ll11111l_opy_ = []
        if bstack11l1111l111_opy_:
            from browserstack_sdk.bstack1lll11lll1l_opy_ import RobotHandler
            bstack111ll11111l_opy_ = RobotHandler.bstack1lll1l1l1l1_opy_(bstack11l1111l111_opy_)
        if not bstack111ll11111l_opy_ and test_name:
            bstack111ll11111l_opy_ = [test_name]
        return {
            TestFramework.bstack1l11111111l_opy_: uuid4().__str__(),
            TestFramework.bstack11l1l1ll11l_opy_: test_id,
            TestFramework.bstack1l1111lll11_opy_: test_name,
            TestFramework.bstack11l1llll111_opy_: test_id,
            TestFramework.bstack11l1111l1ll_opy_: bstack11l1111l111_opy_,
            TestFramework.bstack111ll1llll1_opy_: test_tags,
            TestFramework.bstack111ll11l1ll_opy_: bstack111l1ll1111_opy_,
            TestFramework.bstack11l1ll11l11_opy_: TestFramework.bstack11l11111111_opy_,
            TestFramework.bstack11l11l1111l_opy_: test_id,
            TestFramework.bstack111ll111111_opy_: bstack111ll11111l_opy_
        }
    @staticmethod
    def __111l1ll11l1_opy_(test):
        bstack111ll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡵ࡯࡫ࡴࡹࡪࠦࡴࡦࡵࡷࠤࡎࡊࠠࡧࡴࡲࡱࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡵࡧࡶࡸࠥࡵࡢ࡫ࡧࡦࡸࠧࠨࠢ᫶")
        if hasattr(test, bstack111ll_opy_ (u"ࠣ࡫ࡧࠦ᫷")):
            return test.id
        elif hasattr(test, bstack111ll_opy_ (u"ࠤ࡯ࡳࡳ࡭࡮ࡢ࡯ࡨࠦ᫸")):
            return test.longname
        elif hasattr(test, bstack111ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫹")):
            return test.name
        return None