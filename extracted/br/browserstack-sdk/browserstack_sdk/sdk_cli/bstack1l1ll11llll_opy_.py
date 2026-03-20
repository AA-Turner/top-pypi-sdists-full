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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111l1111_opy_,
    TestHookState,
    bstack1ll1ll111ll_opy_,
    bstack1l1ll1111ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11lllll1lll_opy_
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll111l1l11_opy_ import bstack1l1lll1lll1_opy_
from bstack_utils.bstack1llll11l11_opy_ import bstack1ll1l1l1l1_opy_
bstack1l1111l1lll_opy_ = bstack11lllll1lll_opy_()
bstack11l1ll11l11_opy_ = 1.0
bstack1l1111l11ll_opy_ = bstack11lll1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᣞ")
bstack11l11l1llll_opy_ = bstack11lll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᣟ")
bstack11l11ll11ll_opy_ = bstack11lll1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᣠ")
bstack11l11ll1111_opy_ = bstack11lll1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᣡ")
bstack11l11l1ll1l_opy_ = bstack11lll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᣢ")
_1l11111l1ll_opy_ = set()
class bstack1l1llll111l_opy_(TestFramework):
    bstack11l11l1l1l1_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᣣ")
    bstack11l1ll1ll11_opy_ = bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᣤ")
    bstack11l1l111lll_opy_ = bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᣥ")
    bstack11l1ll1lll1_opy_ = bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᣦ")
    bstack11l1lll11l1_opy_ = bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᣧ")
    bstack11l11l1l1ll_opy_: bool
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_ = None
    bstack1l1lll11l11_opy_ = None
    bstack11l1ll11l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1llll111_opy_: Dict[str, str],
        bstack1l11ll1l11l_opy_: List[str] = [bstack11lll1_opy_ (u"ࠨࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠢᣨ")],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_ = None,
        bstack1l1lll11l11_opy_=None
    ):
        super().__init__(bstack1l11ll1l11l_opy_, bstack11l1llll111_opy_, bstack1ll1l11l1l1_opy_)
        self.bstack11l11l1l1ll_opy_ = any(bstack11lll1_opy_ (u"ࠢࡳࡱࡥࡳࡹࠨᣩ") in item.lower() for item in bstack1l11ll1l11l_opy_)
        self.bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_
    def track_event(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1llll111l_opy_.bstack11l1ll11l1l_opy_:
            bstack11l1l1llll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack11lll1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠧᣪ").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l11l1l1ll_opy_:
            self.logger.warning(bstack11lll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࡾࢁࠧᣫ").format(str(self.bstack1l11ll1l11l_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᣬ").format(args, kwargs))
            return
        instance = self.__11l1l11llll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠤࡦࡸࡧࡴ࠿ࡾࢁࠧᣭ").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1llll111l_opy_.bstack11l1ll11l1l_opy_:
                bstack11lllll1_opy_ = bstack11lll1_opy_ (u"ࠧࠨᣮ")
                name = bstack11lll1_opy_ (u"ࠨࠢᣯ")
                if (test_hook_state == TestHookState.PRE):
                    bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l11l1lll1_opy_.value)
                    name = str(EVENTS.bstack11l11l1lll1_opy_.name) + bstack11lll1_opy_ (u"ࠢ࠻ࠤᣰ") + str(test_framework_state.name)
                else:
                    bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l11ll11l1_opy_.value)
                    name = str(EVENTS.bstack11l11ll11l1_opy_.name) + bstack11lll1_opy_ (u"ࠣ࠼ࠥᣱ") + str(test_framework_state.name)
                TestFramework.bstack11l1l1lll11_opy_(instance, name, bstack11lllll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᣲ").format(e))
        try:
            if not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11lll111lll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1llll111l_opy_.__11l11l11ll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11lll1_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠨᣳ").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1llll_opy_):
                    TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lll1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡸࡨࡲࡹࡃࡻࡾ࠰ࡾࢁࠧᣴ").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1111l_opy_):
                    TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lll1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠦᣵ").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1llll111l_opy_.__11l1l1l1lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l1l1l1l_opy_(instance, *args)
                self.__11l11lll1l1_opy_(instance)
            elif test_framework_state in bstack1l1llll111l_opy_.bstack11l1ll11l1l_opy_:
                self.__11l1l1ll111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠤ᣶").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1llll111l_opy_.bstack11l1ll11l1l_opy_:
                bstack11lllll1_opy_ = bstack11lll1_opy_ (u"ࠢࠣ᣷")
                name = bstack11lll1_opy_ (u"ࠣࠤ᣸")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l1lll1_opy_.name) + bstack11lll1_opy_ (u"ࠤ࠽ࠦ᣹") + str(test_framework_state.name)
                    bstack11lllll1_opy_ = TestFramework.bstack11l1l1l1l11_opy_(instance, name)
                    bstack1llll11l_opy_.end(EVENTS.bstack11l11l1lll1_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᣺"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᣻"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11ll11l1_opy_.name) + bstack11lll1_opy_ (u"ࠧࡀࠢ᣼") + str(test_framework_state.name)
                    bstack11lllll1_opy_ = TestFramework.bstack11l1l1l1l11_opy_(instance, name)
                    bstack1llll11l_opy_.end(EVENTS.bstack11l11ll11l1_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᣽"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᣾"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ᣿").format(e))
    def bstack11lllll1l1l_opy_(self):
        return self.bstack11l11l1l1ll_opy_
    def bstack1l111ll1l11_opy_(self):
        return False
    def __11l11l1l11l_opy_(self, *args):
        bstack11lll1_opy_ (u"ࠤࠥࠦࡕࡧࡲࡴࡧࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡸࡥࡴࡷ࡯ࡸࠥࡵࡢ࡫ࡧࡦࡸࠧࠨࠢᤀ")
        if len(args) > 1 and hasattr(args[1], bstack11lll1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᤁ")):
            result = args[1]
            if result:
                return TestFramework.bstack1l1111ll111_opy_(result, [bstack11lll1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᤂ"), bstack11lll1_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᤃ"), bstack11lll1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡹ࡯࡭ࡦࠤᤄ"), bstack11lll1_opy_ (u"ࠢࡦࡰࡧࡸ࡮ࡳࡥࠣᤅ"), bstack11lll1_opy_ (u"ࠣࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪࠨᤆ")])
        return None
    def __11l1l1l1l1l_opy_(self, instance: bstack1ll111l1111_opy_, *args):
        result = self.__11l11l1l11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lllll11_opy_ = None
        status = result.get(bstack11lll1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᤇ"), bstack11lll1_opy_ (u"ࠥࡒࡔ࡚ࠠࡓࡗࡑࠦᤈ"))
        if status == bstack11lll1_opy_ (u"ࠦࡋࡇࡉࡍࠤᤉ") and result.get(bstack11lll1_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᤊ")):
            failure = [{bstack11lll1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᤋ"): [result.get(bstack11lll1_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᤌ"), bstack11lll1_opy_ (u"ࠣࠤᤍ"))]}]
            bstack1ll1lllll11_opy_ = bstack11lll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᤎ")
        bstack11l11lllll1_opy_ = TestFramework.bstack11l11ll1lll_opy_
        if status == bstack11lll1_opy_ (u"ࠥࡔࡆ࡙ࡓࠣᤏ"):
            bstack11l11lllll1_opy_ = bstack11lll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᤐ")
        elif status == bstack11lll1_opy_ (u"ࠧࡌࡁࡊࡎࠥᤑ"):
            bstack11l11lllll1_opy_ = bstack11lll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᤒ")
        elif status == bstack11lll1_opy_ (u"ࠢࡔࡍࡌࡔࠧᤓ"):
            bstack11l11lllll1_opy_ = bstack11lll1_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᤔ")
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
            instance = self.__11l11l11l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l11l11lll_opy_(test) if test else None
                if target:
                    self.__11l11l1111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᤕ"), None)
            elif hasattr(args[0], bstack11lll1_opy_ (u"ࠥ࡭ࡩࠨᤖ")) if len(args) > 0 else False:
                target = args[0].id
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
        bstack11l1llll11l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack1l1llll111l_opy_.bstack11l1ll1ll11_opy_, {})
        if not key in bstack11l1llll11l_opy_:
            bstack11l1llll11l_opy_[key] = []
        bstack11l1l111l1l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack1l1llll111l_opy_.bstack11l1l111lll_opy_, {})
        if not key in bstack11l1l111l1l_opy_:
            bstack11l1l111l1l_opy_[key] = []
        bstack11l1l1lll1l_opy_ = {
            bstack1l1llll111l_opy_.bstack11l1ll1ll11_opy_: bstack11l1llll11l_opy_,
            bstack1l1llll111l_opy_.bstack11l1l111lll_opy_: bstack11l1l111l1l_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack11lll1_opy_ (u"ࠦࠧᤗ")
            if len(args) > 0 and hasattr(args[0], bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᤘ")):
                hook_name = args[0].name
            hook = {
                bstack11lll1_opy_ (u"ࠨ࡫ࡦࡻࠥᤙ"): key,
                TestFramework.bstack11l1l1ll11l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1ll1l_opy_: TestFramework.bstack11l1l111ll1_opy_,
                TestFramework.bstack11l1ll1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1llllll1_opy_: [],
                TestFramework.bstack11l1lll11ll_opy_: hook_name,
                TestFramework.bstack11l1l1l1111_opy_: bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()
            }
            bstack11l1llll11l_opy_[key].append(hook)
            bstack11l1l1lll1l_opy_[bstack1l1llll111l_opy_.bstack11l1ll1lll1_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1llll_opy_ = bstack11l1llll11l_opy_.get(key, [])
            hook = bstack11l1ll1llll_opy_.pop() if bstack11l1ll1llll_opy_ else None
            if hook:
                result = self.__11l11l1l11l_opy_(*args)
                if result:
                    bstack11l1l1l11ll_opy_ = result.get(bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᤚ"), TestFramework.bstack11l1l111ll1_opy_)
                    if bstack11l1l1l11ll_opy_ == bstack11lll1_opy_ (u"ࠣࡒࡄࡗࡘࠨᤛ"):
                        bstack11l1l1l11ll_opy_ = bstack11lll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᤜ")
                    elif bstack11l1l1l11ll_opy_ == bstack11lll1_opy_ (u"ࠥࡊࡆࡏࡌࠣᤝ"):
                        bstack11l1l1l11ll_opy_ = bstack11lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᤞ")
                    if bstack11l1l1l11ll_opy_ != TestFramework.bstack11l1l111ll1_opy_:
                        hook[TestFramework.bstack11l1ll1ll1l_opy_] = bstack11l1l1l11ll_opy_
                hook[TestFramework.bstack11l1l1l11l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1111_opy_] = bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()
                self.bstack11l1ll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1l1ll1l1_opy_, [])
                if logs:
                    self.bstack11lllll1ll1_opy_(instance, logs)
                bstack11l1l111l1l_opy_[key].append(hook)
                bstack11l1l1lll1l_opy_[bstack1l1llll111l_opy_.bstack11l1lll11l1_opy_] = key
        TestFramework.bstack11l1l11lll1_opy_(instance, bstack11l1l1lll1l_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃ࠮ࡼࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࡼࡿࠥ᤟").format(key, test_hook_state, bstack11l1llll11l_opy_, bstack11l1l111l1l_opy_))
    def __11l11l11l1l_opy_(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack11lll1_opy_ (u"ࠨࠢࠣࡖࡵࡥࡨࡱࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣࡩࡻ࡫࡮ࡵࡵࠣࠬࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡲࡼࡸࡪࡹࡴࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࠦࠧࠨᤠ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᤡ"), None)
        bstack1ll1ll11lll_opy_ = getattr(keyword, bstack11lll1_opy_ (u"ࠣࡶࡼࡴࡪࠨᤢ"), None)
        test_id = kwargs.get(bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᤣ"), None)
        if not test_id:
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡲࡴࠦࡴࡦࡵࡷࡣ࡮ࡪࠠࡪࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡ࡭ࡨࡽࡼࡵࡲࡥ࠿ࡾࢁࠧᤤ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll11l11l11_opy_(test_id)
        if not instance:
            self.logger.warning(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡯ࡪࡿࡷࡰࡴࡧࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡳࡵࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥࡺࡥࡴࡶࡢ࡭ࡩࡃࡻࡾࠤᤥ").format(test_id))
            return None
        bstack11l11l111l1_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack1l1llll111l_opy_.bstack11l11l1l1l1_opy_, {})
        if os.getenv(bstack11lll1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡐࡋ࡙ࡘࡑࡕࡈࡘࠨᤦ"), bstack11lll1_opy_ (u"ࠨ࠱ࠣᤧ")) == bstack11lll1_opy_ (u"ࠢ࠲ࠤᤨ"):
            bstack11l11l111ll_opy_ = bstack11lll1_opy_ (u"ࠣࡽࢀ࠾ࢀࢃࠢᤩ").format(bstack1ll1ll11lll_opy_, keyword_name)
            bstack11l1l1111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11l1l111_opy_ = {
                bstack11lll1_opy_ (u"ࠤ࡮ࡩࡾࠨᤪ"): bstack11l11l111ll_opy_,
                bstack11lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᤫ"): keyword_name,
                bstack11lll1_opy_ (u"ࠦࡹࡿࡰࡦࠤ᤬"): bstack1ll1ll11lll_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l11l1l111_opy_[bstack11lll1_opy_ (u"ࠧࡻࡵࡪࡦࠥ᤭")] = uuid4().__str__()
                bstack11l11l1l111_opy_[bstack1l1llll111l_opy_.bstack11l1ll1l1ll_opy_] = bstack11l1l1111ll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11l1l111_opy_[bstack1l1llll111l_opy_.bstack11l1l1l11l1_opy_] = bstack11l1l1111ll_opy_
                if len(args) > 1 and hasattr(args[1], bstack11lll1_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᤮")):
                    bstack11l11l1l111_opy_[bstack11lll1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᤯")] = args[1].status
            if bstack11l11l111ll_opy_ in bstack11l11l111l1_opy_:
                bstack11l11l111l1_opy_[bstack11l11l111ll_opy_].update(bstack11l11l1l111_opy_)
                self.logger.debug(bstack11lll1_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢ࡮ࡩࡾࡽ࡯ࡳࡦࡀࡿࢂࠦࡴࡺࡲࡨࡁࢀࢃࠢᤰ").format(keyword_name, bstack1ll1ll11lll_opy_))
            else:
                bstack11l11l111l1_opy_[bstack11l11l111ll_opy_] = bstack11l11l1l111_opy_
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡭ࡨࡽࡼࡵࡲࡥ࠿ࡾࢁࠥࡺࡹࡱࡧࡀࡿࢂࠨᤱ").format(keyword_name, bstack1ll1ll11lll_opy_))
        TestFramework.bstack1ll1ll1l1l_opy_(instance, bstack1l1llll111l_opy_.bstack11l11l1l1l1_opy_, bstack11l11l111l1_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡮ࡩࡾࡽ࡯ࡳࡦࡶࡁࢀࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠧᤲ").format(len(bstack11l11l111l1_opy_), instance.ref()))
        return instance
    def __11l11l1111l_opy_(
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
            bstack1l1llll111l_opy_.bstack11l11l1l1l1_opy_: {},
            bstack1l1llll111l_opy_.bstack11l1l111lll_opy_: {},
            bstack1l1llll111l_opy_.bstack11l1ll1ll11_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack11lll1_opy_ (u"ࠦࡸࡵࡵࡳࡥࡨࠦᤳ")):
            TestFramework.bstack1ll1ll1l1l_opy_(ob, TestFramework.bstack11l11lll11l_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1ll1l1l_opy_(ob, TestFramework.bstack1l11lll1ll1_opy_, context.platform_index)
        TestFramework.bstack11l1lll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11lll1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࡾࢁࠧᤴ").format(ctx.id, target, args, TestFramework.bstack11l1lll111_opy_.keys()))
        return ob
    def bstack1l1111111l1_opy_(self, instance: bstack1ll111l1111_opy_, bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1l111l_opy_ = (
            bstack1l1llll111l_opy_.bstack11l1ll1lll1_opy_
            if bstack1ll1l111111_opy_[1] == TestHookState.PRE
            else bstack1l1llll111l_opy_.bstack11l1lll11l1_opy_
        )
        hook = bstack1l1llll111l_opy_.bstack11l1ll1111l_opy_(instance, bstack11l1l1l111l_opy_)
        entries = hook.get(TestFramework.bstack11l1llllll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, []))
        return entries
    def bstack1l1111llll1_opy_(self, instance: bstack1ll111l1111_opy_, bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1l111l_opy_ = (
            bstack1l1llll111l_opy_.bstack11l1ll1lll1_opy_
            if bstack1ll1l111111_opy_[1] == TestHookState.PRE
            else bstack1l1llll111l_opy_.bstack11l1lll11l1_opy_
        )
        bstack1l1llll111l_opy_.bstack11l1l1l1ll1_opy_(instance, bstack11l1l1l111l_opy_)
        TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, []).clear()
    def bstack11l1ll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᤵ")
        global _1l11111l1ll_opy_
        platform_index = os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᤶ")]
        bstack1l1111l111l_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), bstack11l11ll1111_opy_)
        if not os.path.exists(bstack1l1111l111l_opy_) or not os.path.isdir(bstack1l1111l111l_opy_):
            self.logger.debug(bstack11lll1_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᤷ").format(bstack1l1111l111l_opy_))
            return
        logs = hook.get(bstack11lll1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᤸ"), [])
        with os.scandir(bstack1l1111l111l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111l1ll_opy_:
                    self.logger.info(bstack11lll1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽ᤹ࠣ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11lll1_opy_ (u"ࠦࠧ᤺")
                    log_entry = bstack1l1ll1111ll_opy_(
                        kind=bstack11lll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚᤻ࠢ"),
                        message=bstack11lll1_opy_ (u"ࠨࠢ᤼"),
                        level=bstack11lll1_opy_ (u"ࠢࠣ᤽"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11111111l_opy_=entry.stat().st_size,
                        bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣ᤾"),
                        bstack11111l1_opy_=os.path.abspath(entry.path),
                        bstack11l1l11ll11_opy_=hook.get(TestFramework.bstack11l1l1ll11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111l1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᤿")]
        bstack11l1lll1lll_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), bstack11l11ll1111_opy_, bstack11l11l1ll1l_opy_)
        if not os.path.exists(bstack11l1lll1lll_opy_) or not os.path.isdir(bstack11l1lll1lll_opy_):
            self.logger.info(bstack11lll1_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧ᥀").format(bstack11l1lll1lll_opy_))
        else:
            self.logger.info(bstack11lll1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥ᥁").format(bstack11l1lll1lll_opy_))
            with os.scandir(bstack11l1lll1lll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack11lll1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ᥂").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11lll1_opy_ (u"ࠨࠢ᥃")
                        log_entry = bstack1l1ll1111ll_opy_(
                            kind=bstack11lll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᥄"),
                            message=bstack11lll1_opy_ (u"ࠣࠤ᥅"),
                            level=bstack11lll1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨ᥆"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11111111l_opy_=entry.stat().st_size,
                            bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥ᥇"),
                            bstack11111l1_opy_=os.path.abspath(entry.path),
                            bstack1l111l111ll_opy_=hook.get(TestFramework.bstack11l1l1ll11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111l1ll_opy_.add(abs_path)
        hook[bstack11lll1_opy_ (u"ࠦࡱࡵࡧࡴࠤ᥈")] = logs
    def bstack11lllll1ll1_opy_(
        self,
        bstack1l1111lllll_opy_: bstack1ll111l1111_opy_,
        entries: List[bstack1l1ll1111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11lll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤ᥉"))
        req.platform_index = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll1ll1_opy_)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᥊").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111lllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111lllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111lllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll111l_opy_, bstack11lll1_opy_ (u"ࠢࠣ᥋"))
            log_entry.test_framework_version = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l111l11lll_opy_, bstack11lll1_opy_ (u"ࠣࠤ᥌"))
            log_entry.uuid = entry.bstack11l1l11ll11_opy_ or bstack11lll1_opy_ (u"ࠤࠥ᥍")
            log_entry.test_framework_state = bstack1l1111lllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᥎"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11lll1_opy_ (u"ࠦࠧ᥏")
            if entry.kind == bstack11lll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᥐ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11111111l_opy_
                log_entry.file_path = entry.bstack11111l1_opy_
        def bstack1l111111ll1_opy_():
            bstack111ll1l1_opy_ = datetime.now()
            try:
                self.bstack1l1lll11l11_opy_.LogCreatedEvent(req)
                bstack1l1111lllll_opy_.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᥑ"), datetime.now() - bstack111ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᥒ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l111111ll1_opy_)
    def __11l11lll1l1_opy_(self, instance) -> None:
        bstack11lll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᥓ")
        bstack11l1l1lll1l_opy_ = {bstack11lll1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᥔ"): bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l11lll1_opy_(instance, bstack11l1l1lll1l_opy_)
    @staticmethod
    def bstack11l1ll1111l_opy_(instance: bstack1ll111l1111_opy_, bstack11l1l1l111l_opy_: str):
        bstack11l11llll1l_opy_ = (
            bstack1l1llll111l_opy_.bstack11l1l111lll_opy_
            if bstack11l1l1l111l_opy_ == bstack1l1llll111l_opy_.bstack11l1lll11l1_opy_
            else bstack1l1llll111l_opy_.bstack11l1ll1ll11_opy_
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
        hook = bstack1l1llll111l_opy_.bstack11l1ll1111l_opy_(instance, bstack11l1l1l111l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1llllll1_opy_, []).clear()
    @staticmethod
    def __11l1l1l1lll_opy_(instance: bstack1ll111l1111_opy_, *args):
        bstack11lll1_opy_ (u"ࠥࠦࠧࡖࡲࡰࡥࡨࡷࡸࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࡹࠢࠣࠤᥕ")
        if len(args) < 1:
            return
        if os.getenv(bstack11lll1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᥖ"), bstack11lll1_opy_ (u"ࠧ࠷ࠢᥗ")) != bstack11lll1_opy_ (u"ࠨ࠱ࠣᥘ"):
            bstack1l1llll111l_opy_.logger.warning(bstack11lll1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡ࡮ࡲ࡫ࡸࠨᥙ"))
            return
        message = args[0]
        if not hasattr(message, bstack11lll1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᥚ")):
            return
        is_screenshot = hasattr(message, bstack11lll1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᥛ")) and message.kind == bstack11lll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᥜ")
        log_entry = bstack1l1ll1111ll_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11lllll1l11_opy_,
            message=message.message if hasattr(message, bstack11lll1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᥝ")) else bstack11lll1_opy_ (u"ࠧࠨᥞ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack11lll1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧᥟ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack11lll1_opy_ (u"࡛ࠢࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠧᥠ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack11lll1_opy_ (u"ࠣࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦᥡ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l1l11l1l1_opy_ = {
            bstack11lll1_opy_ (u"ࠤࡖࡉ࡙࡛ࡐࠣᥢ"): (bstack1l1llll111l_opy_.bstack11l1ll1lll1_opy_, bstack1l1llll111l_opy_.bstack11l1ll1ll11_opy_),
            bstack11lll1_opy_ (u"ࠥࡘࡊࡇࡒࡅࡑ࡚ࡒࠧᥣ"): (bstack1l1llll111l_opy_.bstack11l1lll11l1_opy_, bstack1l1llll111l_opy_.bstack11l1l111lll_opy_),
        }
        bstack11l11l1ll11_opy_ = None
        if len(args) > 1:
            bstack11l11l1ll11_opy_ = args[1]
        if bstack11l11l1ll11_opy_ and bstack11l11l1ll11_opy_ in bstack11l1l11l1l1_opy_:
            bstack11l1ll11ll1_opy_, bstack11l11llll1l_opy_ = bstack11l1l11l1l1_opy_[bstack11l11l1ll11_opy_]
            bstack11l1lllllll_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack11l1ll11ll1_opy_, None)
            bstack11l1l111111_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack11l11llll1l_opy_, None) if bstack11l1lllllll_opy_ else None
            if isinstance(bstack11l1l111111_opy_, dict) and len(bstack11l1l111111_opy_.get(bstack11l1lllllll_opy_, [])) > 0:
                hook = bstack11l1l111111_opy_[bstack11l1lllllll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1llllll1_opy_ in hook:
                    hook[TestFramework.bstack11l1llllll1_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l11l11ll1_opy_(test) -> Dict[str, Any]:
        bstack11lll1_opy_ (u"ࠦࠧࠨࡐࡢࡴࡶࡩࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡵࡧࡶࡸࠥࡵࡢ࡫ࡧࡦࡸࠧࠨࠢᥤ")
        test_id = bstack1l1llll111l_opy_.__11l11l11lll_opy_(test)
        test_name = test.name if hasattr(test, bstack11lll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᥥ")) else None
        bstack11l11llllll_opy_ = str(test.source) if hasattr(test, bstack11lll1_opy_ (u"ࠨࡳࡰࡷࡵࡧࡪࠨᥦ")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack11lll1_opy_ (u"ࠢࡵࡣࡪࡷࠧᥧ")) else []
        bstack11l11l11l11_opy_ =bstack11lll1_opy_ (u"ࠣࡽࢀࠤࡡࡴࠠࡼࡿࠥᥨ").format(bstack11lll1_opy_ (u"ࠤࠣࠦᥩ").join(test_tags), test_name) if test_tags else test_name
        bstack11l11ll111l_opy_ = []
        if bstack11l11llllll_opy_:
            from browserstack_sdk.bstack1llll11l111_opy_ import RobotHandler
            bstack11l11ll111l_opy_ = RobotHandler.bstack1lllll11l11_opy_(bstack11l11llllll_opy_)
        if not bstack11l11ll111l_opy_ and test_name:
            bstack11l11ll111l_opy_ = [test_name]
        return {
            TestFramework.bstack1l11llll11l_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111lll_opy_: test_id,
            TestFramework.bstack1l11ll1llll_opy_: test_name,
            TestFramework.bstack11lllll1111_opy_: test_id,
            TestFramework.bstack11l1lll1111_opy_: bstack11l11llllll_opy_,
            TestFramework.bstack11l1ll1l11l_opy_: test_tags,
            TestFramework.bstack11l1l111l11_opy_: bstack11l11l11l11_opy_,
            TestFramework.bstack11lll11111l_opy_: TestFramework.bstack11l11ll1lll_opy_,
            TestFramework.bstack11ll11ll11l_opy_: test_id,
            TestFramework.bstack11l11ll1l11_opy_: bstack11l11ll111l_opy_
        }
    @staticmethod
    def __11l11l11lll_opy_(test):
        bstack11lll1_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡸࡲ࡮ࡷࡵࡦࠢࡷࡩࡸࡺࠠࡊࡆࠣࡪࡷࡵ࡭ࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡸࡪࡹࡴࠡࡱࡥ࡮ࡪࡩࡴࠣࠤࠥᥪ")
        if hasattr(test, bstack11lll1_opy_ (u"ࠦ࡮ࡪࠢᥫ")):
            return test.id
        elif hasattr(test, bstack11lll1_opy_ (u"ࠧࡲ࡯࡯ࡩࡱࡥࡲ࡫ࠢᥬ")):
            return test.longname
        elif hasattr(test, bstack11lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᥭ")):
            return test.name
        return None