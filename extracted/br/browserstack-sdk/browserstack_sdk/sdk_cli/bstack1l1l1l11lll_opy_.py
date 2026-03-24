# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack111l1ll1ll_opy_ import bstack11l11ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111lllll_opy_,
    TestHookState,
    bstack1ll1lll1l11_opy_,
    bstack1l1l1l1l1ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11llllll1l1_opy_
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1llllll_opy_ import bstack1l1llll1l1l_opy_
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
bstack11lllllll1l_opy_ = bstack11llllll1l1_opy_()
bstack11l11llll11_opy_ = 1.0
bstack1l1111lllll_opy_ = bstack1ll1lll_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᠽ")
bstack11l11l1l1l1_opy_ = bstack1ll1lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᠾ")
bstack11l11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᠿ")
bstack11l11l1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᡀ")
bstack11l11ll1111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᡁ")
_11lllll1lll_opy_ = set()
class bstack1l1l1ll11ll_opy_(TestFramework):
    bstack11l1l1111l1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᡂ")
    bstack11l11ll11l1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᡃ")
    bstack11l1ll1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᡄ")
    bstack11l11lll111_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᡅ")
    bstack11l1ll11lll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᡆ")
    bstack11l1lll111l_opy_: bool
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_  = None
    bstack1l1ll1l1ll1_opy_ = None
    bstack11l1l11l11l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l11lll11l_opy_: Dict[str, str],
        bstack1l11ll1l1ll_opy_: List[str]=[bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᡇ")],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_=None,
        bstack1l1ll1l1ll1_opy_=None
    ):
        super().__init__(bstack1l11ll1l1ll_opy_, bstack11l11lll11l_opy_, bstack1ll1l11l1l1_opy_)
        self.bstack11l1lll111l_opy_ = any(bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᡈ") in item.lower() for item in bstack1l11ll1l1ll_opy_)
        self.bstack1l1ll1l1ll1_opy_ = bstack1l1ll1l1ll1_opy_
    def track_event(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l1ll11ll_opy_.bstack11l1l11l11l_opy_:
            bstack11l11ll11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᡉ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠤࠥᡊ"))
            return
        if not self.bstack11l1lll111l_opy_:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᡋ") + str(str(self.bstack1l11ll1l1ll_opy_)) + bstack1ll1lll_opy_ (u"ࠦࠧᡌ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᡍ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᡎ"))
            return
        instance = self.__11l1lll1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᡏ") + str(args) + bstack1ll1lll_opy_ (u"ࠣࠤᡐ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1l1ll11ll_opy_.bstack11l1l11l11l_opy_:
                bstack11ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࠥᡑ")
                name = bstack1ll1lll_opy_ (u"ࠥࠦᡒ")
                if (test_hook_state == TestHookState.PRE):
                    bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l1llll_opy_.value)
                    name = str(EVENTS.bstack11l11l1llll_opy_.name)+bstack1ll1lll_opy_ (u"ࠦ࠿ࠨᡓ")+str(test_framework_state.name)
                else:
                    bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l1ll1l_opy_.value)
                    name = str(EVENTS.bstack11l11l1ll1l_opy_.name)+bstack1ll1lll_opy_ (u"ࠧࡀࠢᡔ")+str(test_framework_state.name)
                TestFramework.bstack11l11ll1ll1_opy_(instance, name, bstack11ll1ll1l_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᡕ").format(e))
        try:
            if not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack11lll111lll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l1ll11ll_opy_.__11l1lll1l1l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᡖ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠣࠤᡗ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l111ll11ll_opy_):
                    TestFramework.bstack1l1l11lll_opy_(instance, TestFramework.bstack1l111ll11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᡘ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠥࠦᡙ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l111ll1l11_opy_):
                    TestFramework.bstack1l1l11lll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᡚ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠧࠨᡛ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l1ll11ll_opy_.__11l1l1ll111_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1lll11l1_opy_(instance, *args)
                self.__11l1l1ll1l1_opy_(instance)
            elif test_framework_state in bstack1l1l1ll11ll_opy_.bstack11l1l11l11l_opy_:
                self.__11l1l1lll1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᡜ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠢࠣᡝ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1l1ll11ll_opy_.bstack11l1l11l11l_opy_:
                bstack11ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࠤᡞ")
                name = bstack1ll1lll_opy_ (u"ࠤࠥᡟ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l1llll_opy_.name)+bstack1ll1lll_opy_ (u"ࠥ࠾ࠧᡠ")+str(test_framework_state.name)
                    bstack11ll1ll1l_opy_ = TestFramework.bstack11l1l111111_opy_(instance, name)
                    bstack1lll1lll11_opy_.end(EVENTS.bstack11l11l1llll_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᡡ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᡢ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11l1ll1l_opy_.name)+bstack1ll1lll_opy_ (u"ࠨ࠺ࠣᡣ")+str(test_framework_state.name)
                    bstack11ll1ll1l_opy_ = TestFramework.bstack11l1l111111_opy_(instance, name)
                    bstack1lll1lll11_opy_.end(EVENTS.bstack11l11l1ll1l_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᡤ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᡥ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᡦ").format(e))
    def bstack1l1111111ll_opy_(self):
        return self.bstack11l1lll111l_opy_
    def bstack1l111lll11l_opy_(self):
        return False
    def __11l1lllllll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᡧ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111l11lll_opy_(rep, [bstack1ll1lll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᡨ"), bstack1ll1lll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᡩ"), bstack1ll1lll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᡪ"), bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᡫ"), bstack1ll1lll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᡬ"), bstack1ll1lll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᡭ")])
        return None
    def __11l1lll11l1_opy_(self, instance: bstack1ll111lllll_opy_, *args):
        result = self.__11l1lllllll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1llll1ll_opy_ = None
        if result.get(bstack1ll1lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᡮ"), None) == bstack1ll1lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᡯ") and len(args) > 1 and getattr(args[1], bstack1ll1lll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᡰ"), None) is not None:
            failure = [{bstack1ll1lll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᡱ"): [args[1].excinfo.exconly(), result.get(bstack1ll1lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᡲ"), None)]}]
            bstack1ll1llll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᡳ") if bstack1ll1lll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᡴ") in getattr(args[1].excinfo, bstack1ll1lll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᡵ"), bstack1ll1lll_opy_ (u"ࠦࠧᡶ")) else bstack1ll1lll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᡷ")
        bstack11l1l111l1l_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᡸ"), TestFramework.bstack11l1llll111_opy_)
        if bstack11l1l111l1l_opy_ != TestFramework.bstack11l1llll111_opy_:
            TestFramework.bstack1l1l11lll_opy_(instance, TestFramework.bstack1l1111ll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l11l1ll_opy_(instance, {
            TestFramework.bstack11lll11ll1l_opy_: failure,
            TestFramework.bstack11l1l1111ll_opy_: bstack1ll1llll1ll_opy_,
            TestFramework.bstack11lll11ll11_opy_: bstack11l1l111l1l_opy_,
        })
    def __11l1lll1111_opy_(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l1llll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll1ll1_opy_ bstack11l1l11111l_opy_ this to be bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᡹")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l1ll11l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1lll_opy_ (u"ࠣࡰࡲࡨࡪࠨ᡺"), None), bstack1ll1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᡻"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᡼"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1l111l1l_opy_(target) if target else None
        return instance
    def __11l1l1lll1l_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1ll11ll1_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack1l1l1ll11ll_opy_.bstack11l11ll11l1_opy_, {})
        if not key in bstack11l1ll11ll1_opy_:
            bstack11l1ll11ll1_opy_[key] = []
        bstack11l1ll1l111_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack1l1l1ll11ll_opy_.bstack11l1ll1lll1_opy_, {})
        if not key in bstack11l1ll1l111_opy_:
            bstack11l1ll1l111_opy_[key] = []
        bstack11l1ll1ll11_opy_ = {
            bstack1l1l1ll11ll_opy_.bstack11l11ll11l1_opy_: bstack11l1ll11ll1_opy_,
            bstack1l1l1ll11ll_opy_.bstack11l1ll1lll1_opy_: bstack11l1ll1l111_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1ll1lll_opy_ (u"ࠦࡰ࡫ࡹࠣ᡽"): key,
                TestFramework.bstack11l1lllll1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1l11l_opy_: TestFramework.bstack11l1l1lll11_opy_,
                TestFramework.bstack11l11lllll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1l11ll11_opy_: [],
                TestFramework.bstack11l1l1l1l1l_opy_: args[1] if len(args) > 1 else bstack1ll1lll_opy_ (u"ࠬ࠭᡾"),
                TestFramework.bstack11l11lll1ll_opy_: bstack1l1llll1l1l_opy_.bstack11l11llll1l_opy_()
            }
            bstack11l1ll11ll1_opy_[key].append(hook)
            bstack11l1ll1ll11_opy_[bstack1l1l1ll11ll_opy_.bstack11l11lll111_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1llll_opy_ = bstack11l1ll11ll1_opy_.get(key, [])
            hook = bstack11l1ll1llll_opy_.pop() if bstack11l1ll1llll_opy_ else None
            if hook:
                result = self.__11l1lllllll_opy_(*args)
                if result:
                    bstack11l1l1l11l1_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᡿"), TestFramework.bstack11l1l1lll11_opy_)
                    if bstack11l1l1l11l1_opy_ != TestFramework.bstack11l1l1lll11_opy_:
                        hook[TestFramework.bstack11l1ll1l11l_opy_] = bstack11l1l1l11l1_opy_
                hook[TestFramework.bstack11l1ll11111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l11lll1ll_opy_]= bstack1l1llll1l1l_opy_.bstack11l11llll1l_opy_()
                self.bstack11l1l1llll1_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll1ll1l_opy_, [])
                if logs: self.bstack1l111l1ll1l_opy_(instance, logs)
                bstack11l1ll1l111_opy_[key].append(hook)
                bstack11l1ll1ll11_opy_[bstack1l1l1ll11ll_opy_.bstack11l1ll11lll_opy_] = key
        TestFramework.bstack11l1l11l1ll_opy_(instance, bstack11l1ll1ll11_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᢀ") + str(bstack11l1ll1l111_opy_) + bstack1ll1lll_opy_ (u"ࠣࠤᢁ"))
    def __11l1llll1ll_opy_(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111l11lll_opy_(args[0], [bstack1ll1lll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᢂ"), bstack1ll1lll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᢃ"), bstack1ll1lll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᢄ"), bstack1ll1lll_opy_ (u"ࠧ࡯ࡤࡴࠤᢅ"), bstack1ll1lll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᢆ"), bstack1ll1lll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᢇ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll1lll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᢈ")) else fixturedef.get(bstack1ll1lll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᢉ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1lll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᢊ")) else None
        node = request.node if hasattr(request, bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦࠤᢋ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᢌ")) else None
        baseid = fixturedef.get(bstack1ll1lll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᢍ"), None) or bstack1ll1lll_opy_ (u"ࠢࠣᢎ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1lll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᢏ")):
            target = bstack1l1l1ll11ll_opy_.__11l1l1l1ll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1lll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᢐ")) else None
            if target and not TestFramework.bstack1ll1l111l1l_opy_(target):
                self.__11l1ll11l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᢑ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠦࠧᢒ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᢓ") + str(target) + bstack1ll1lll_opy_ (u"ࠨࠢᢔ"))
            return None
        instance = TestFramework.bstack1ll1l111l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᢕ") + str(target) + bstack1ll1lll_opy_ (u"ࠣࠤᢖ"))
            return None
        bstack11l1l11lll1_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack1l1l1ll11ll_opy_.bstack11l1l1111l1_opy_, {})
        if os.getenv(bstack1ll1lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᢗ"), bstack1ll1lll_opy_ (u"ࠥ࠵ࠧᢘ")) == bstack1ll1lll_opy_ (u"ࠦ࠶ࠨᢙ"):
            bstack11l1l1l11ll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡀࠢᢚ").join((scope, fixturename))
            bstack11l11ll1l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1lll1l11_opy_ = {
                bstack1ll1lll_opy_ (u"ࠨ࡫ࡦࡻࠥᢛ"): bstack11l1l1l11ll_opy_,
                bstack1ll1lll_opy_ (u"ࠢࡵࡣࡪࡷࠧᢜ"): bstack1l1l1ll11ll_opy_.__11l1l11l111_opy_(request.node),
                bstack1ll1lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᢝ"): fixturedef,
                bstack1ll1lll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᢞ"): scope,
                bstack1ll1lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᢟ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᢠ"), None)):
                    bstack11l1lll1l11_opy_[bstack1ll1lll_opy_ (u"ࠧࡺࡹࡱࡧࠥᢡ")] = TestFramework.bstack1l111l111ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1lll1l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᢢ")] = uuid4().__str__()
                bstack11l1lll1l11_opy_[bstack1l1l1ll11ll_opy_.bstack11l11lllll1_opy_] = bstack11l11ll1l1l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1lll1l11_opy_[bstack1l1l1ll11ll_opy_.bstack11l1ll11111_opy_] = bstack11l11ll1l1l_opy_
            if bstack11l1l1l11ll_opy_ in bstack11l1l11lll1_opy_:
                bstack11l1l11lll1_opy_[bstack11l1l1l11ll_opy_].update(bstack11l1lll1l11_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᢣ") + str(bstack11l1l11lll1_opy_[bstack11l1l1l11ll_opy_]) + bstack1ll1lll_opy_ (u"ࠣࠤᢤ"))
            else:
                bstack11l1l11lll1_opy_[bstack11l1l1l11ll_opy_] = bstack11l1lll1l11_opy_
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᢥ") + str(len(bstack11l1l11lll1_opy_)) + bstack1ll1lll_opy_ (u"ࠥࠦᢦ"))
        TestFramework.bstack1l1l11lll_opy_(instance, bstack1l1l1ll11ll_opy_.bstack11l1l1111l1_opy_, bstack11l1l11lll1_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᢧ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠧࠨᢨ"))
        return instance
    def __11l1ll11l1l_opy_(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11l1ll1l_opy_.create_context(target)
        ob = bstack1ll111lllll_opy_(ctx, self.bstack1l11ll1l1ll_opy_, self.bstack11l11lll11l_opy_, test_framework_state)
        TestFramework.bstack11l1l11l1ll_opy_(ob, {
            TestFramework.bstack1l11lll111l_opy_: context.test_framework_name,
            TestFramework.bstack1l1111l1ll1_opy_: context.test_framework_version,
            TestFramework.bstack11l1lllll11_opy_: [],
            bstack1l1l1ll11ll_opy_.bstack11l1l1111l1_opy_: {},
            bstack1l1l1ll11ll_opy_.bstack11l1ll1lll1_opy_: {},
            bstack1l1l1ll11ll_opy_.bstack11l11ll11l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l1l11lll_opy_(ob, TestFramework.bstack11l11ll1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l1l11lll_opy_(ob, TestFramework.bstack1l11llll111_opy_, context.platform_index)
        TestFramework.bstack111llll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᢩ") + str(TestFramework.bstack111llll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠢࠣᢪ"))
        return ob
    def bstack11llllll111_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1lll11ll_opy_ = (
            bstack1l1l1ll11ll_opy_.bstack11l11lll111_opy_
            if bstack1ll11l1ll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1ll11ll_opy_.bstack11l1ll11lll_opy_
        )
        hook = bstack1l1l1ll11ll_opy_.bstack11l1l11llll_opy_(instance, bstack11l1lll11ll_opy_)
        entries = hook.get(TestFramework.bstack11l1l11ll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11l1lllll11_opy_, []))
        return entries
    def bstack1l111l1111l_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1lll11ll_opy_ = (
            bstack1l1l1ll11ll_opy_.bstack11l11lll111_opy_
            if bstack1ll11l1ll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1ll11ll_opy_.bstack11l1ll11lll_opy_
        )
        bstack1l1l1ll11ll_opy_.bstack11l1ll111l1_opy_(instance, bstack11l1lll11ll_opy_)
        TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11l1lllll11_opy_, []).clear()
    def bstack11l1l1llll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᢫")
        global _11lllll1lll_opy_
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᢬")]
        bstack1l1111111l1_opy_ = os.path.join(bstack11lllllll1l_opy_, (bstack1l1111lllll_opy_ + str(platform_index)), bstack11l11l1lll1_opy_)
        if not os.path.exists(bstack1l1111111l1_opy_) or not os.path.isdir(bstack1l1111111l1_opy_):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣ᢭").format(bstack1l1111111l1_opy_))
            return
        logs = hook.get(bstack1ll1lll_opy_ (u"ࠦࡱࡵࡧࡴࠤ᢮"), [])
        with os.scandir(bstack1l1111111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11lllll1lll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ᢯").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1lll_opy_ (u"ࠨࠢᢰ")
                    log_entry = bstack1l1l1l1l1ll_opy_(
                        kind=bstack1ll1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᢱ"),
                        message=bstack1ll1lll_opy_ (u"ࠣࠤᢲ"),
                        level=bstack1ll1lll_opy_ (u"ࠤࠥᢳ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111llll1l_opy_=entry.stat().st_size,
                        bstack11lllll1ll1_opy_=bstack1ll1lll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᢴ"),
                        bstack1l11111_opy_=os.path.abspath(entry.path),
                        bstack11l1ll111ll_opy_=hook.get(TestFramework.bstack11l1lllll1l_opy_)
                    )
                    logs.append(log_entry)
                    _11lllll1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᢵ")]
        bstack11l1llll1l1_opy_ = os.path.join(bstack11lllllll1l_opy_, (bstack1l1111lllll_opy_ + str(platform_index)), bstack11l11l1lll1_opy_, bstack11l11ll1111_opy_)
        if not os.path.exists(bstack11l1llll1l1_opy_) or not os.path.isdir(bstack11l1llll1l1_opy_):
            self.logger.info(bstack1ll1lll_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᢶ").format(bstack11l1llll1l1_opy_))
        else:
            self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᢷ").format(bstack11l1llll1l1_opy_))
            with os.scandir(bstack11l1llll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11lllll1lll_opy_:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᢸ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1lll_opy_ (u"ࠣࠤᢹ")
                        log_entry = bstack1l1l1l1l1ll_opy_(
                            kind=bstack1ll1lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᢺ"),
                            message=bstack1ll1lll_opy_ (u"ࠥࠦᢻ"),
                            level=bstack1ll1lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᢼ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111llll1l_opy_=entry.stat().st_size,
                            bstack11lllll1ll1_opy_=bstack1ll1lll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᢽ"),
                            bstack1l11111_opy_=os.path.abspath(entry.path),
                            bstack1l111l11l1l_opy_=hook.get(TestFramework.bstack11l1lllll1l_opy_)
                        )
                        logs.append(log_entry)
                        _11lllll1lll_opy_.add(abs_path)
        hook[bstack1ll1lll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᢾ")] = logs
    def bstack1l111l1ll1l_opy_(
        self,
        bstack1l1111ll111_opy_: bstack1ll111lllll_opy_,
        entries: List[bstack1l1l1l1l1ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᢿ"))
        req.platform_index = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack1l11llll111_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᣀ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111ll111_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111ll111_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111ll111_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack1l11lll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack1l1111l1ll1_opy_)
            log_entry.uuid = entry.bstack11l1ll111ll_opy_
            log_entry.test_framework_state = bstack1l1111ll111_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᣁ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1lll_opy_ (u"ࠥࠦᣂ")
            if entry.kind == bstack1ll1lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᣃ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111llll1l_opy_
                log_entry.file_path = entry.bstack1l11111_opy_
        def bstack11llllll11l_opy_():
            bstack1ll1l111l_opy_ = datetime.now()
            try:
                self.bstack1l1ll1l1ll1_opy_.LogCreatedEvent(req)
                bstack1l1111ll111_opy_.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᣄ"), datetime.now() - bstack1ll1l111l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᣅ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack11llllll11l_opy_)
    def __11l1l1ll1l1_opy_(self, instance) -> None:
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᣆ")
        bstack11l1ll1ll11_opy_ = {bstack1ll1lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᣇ"): bstack1l1llll1l1l_opy_.bstack11l11llll1l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l11l1ll_opy_(instance, bstack11l1ll1ll11_opy_)
    @staticmethod
    def bstack11l1l11llll_opy_(instance: bstack1ll111lllll_opy_, bstack11l1lll11ll_opy_: str):
        bstack11l1l1lllll_opy_ = (
            bstack1l1l1ll11ll_opy_.bstack11l1ll1lll1_opy_
            if bstack11l1lll11ll_opy_ == bstack1l1l1ll11ll_opy_.bstack11l1ll11lll_opy_
            else bstack1l1l1ll11ll_opy_.bstack11l11ll11l1_opy_
        )
        bstack11l11llllll_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1lll11ll_opy_, None)
        bstack11l1llll11l_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1l1lllll_opy_, None) if bstack11l11llllll_opy_ else None
        return (
            bstack11l1llll11l_opy_[bstack11l11llllll_opy_][-1]
            if isinstance(bstack11l1llll11l_opy_, dict) and len(bstack11l1llll11l_opy_.get(bstack11l11llllll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll111l1_opy_(instance: bstack1ll111lllll_opy_, bstack11l1lll11ll_opy_: str):
        hook = bstack1l1l1ll11ll_opy_.bstack11l1l11llll_opy_(instance, bstack11l1lll11ll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1l11ll11_opy_, []).clear()
    @staticmethod
    def __11l1l1ll111_opy_(instance: bstack1ll111lllll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᣈ"), None)):
            return
        if os.getenv(bstack1ll1lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᣉ"), bstack1ll1lll_opy_ (u"ࠦ࠶ࠨᣊ")) != bstack1ll1lll_opy_ (u"ࠧ࠷ࠢᣋ"):
            bstack1l1l1ll11ll_opy_.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᣌ"))
            return
        bstack11l1l111lll_opy_ = {
            bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᣍ"): (bstack1l1l1ll11ll_opy_.bstack11l11lll111_opy_, bstack1l1l1ll11ll_opy_.bstack11l11ll11l1_opy_),
            bstack1ll1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᣎ"): (bstack1l1l1ll11ll_opy_.bstack11l1ll11lll_opy_, bstack1l1l1ll11ll_opy_.bstack11l1ll1lll1_opy_),
        }
        for when in (bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᣏ"), bstack1ll1lll_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᣐ"), bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᣑ")):
            bstack11l1ll1111l_opy_ = args[1].get_records(when)
            if not bstack11l1ll1111l_opy_:
                continue
            records = [
                bstack1l1l1l1l1ll_opy_(
                    kind=TestFramework.bstack1l111lll1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1lll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᣒ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1lll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᣓ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1ll1111l_opy_
                if isinstance(getattr(r, bstack1ll1lll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᣔ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1l1ll11l_opy_, bstack11l1l1lllll_opy_ = bstack11l1l111lll_opy_.get(when, (None, None))
            bstack11l1l111l11_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1l1ll11l_opy_, None) if bstack11l1l1ll11l_opy_ else None
            bstack11l1llll11l_opy_ = TestFramework.bstack1ll1lll11ll_opy_(instance, bstack11l1l1lllll_opy_, None) if bstack11l1l111l11_opy_ else None
            if isinstance(bstack11l1llll11l_opy_, dict) and len(bstack11l1llll11l_opy_.get(bstack11l1l111l11_opy_, [])) > 0:
                hook = bstack11l1llll11l_opy_[bstack11l1l111l11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1l11ll11_opy_ in hook:
                    hook[TestFramework.bstack11l1l11ll11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack11l1lllll11_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l1lll1l1l_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1l1ll11ll_opy_.__11l1l1l1ll1_opy_(test.location) if hasattr(test, bstack1ll1lll_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᣕ")) else getattr(test, bstack1ll1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᣖ"), None)
        test_name = test.name if hasattr(test, bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᣗ")) else None
        bstack11l1l1ll1ll_opy_ = test.fspath.strpath if hasattr(test, bstack1ll1lll_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᣘ")) and test.fspath else None
        if not test_id or not test_name or not bstack11l1l1ll1ll_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll1lll_opy_ (u"ࠧࡵࡢ࡫ࠤᣙ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l11l1l1ll_opy_ = []
        try:
            bstack11l11l1l1ll_opy_ = bstack11lll1l11_opy_.bstack1llll1l1111_opy_(test)
        except:
            bstack1l1l1ll11ll_opy_.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᣚ"))
        return {
            TestFramework.bstack1l1l1111l11_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111lll_opy_: test_id,
            TestFramework.bstack1l1l111111l_opy_: test_name,
            TestFramework.bstack11lllll1111_opy_: getattr(test, bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᣛ"), None),
            TestFramework.bstack11l1l1l1111_opy_: bstack11l1l1ll1ll_opy_,
            TestFramework.bstack11l1l1l1lll_opy_: bstack1l1l1ll11ll_opy_.__11l1l11l111_opy_(test),
            TestFramework.bstack11l1l11l1l1_opy_: code,
            TestFramework.bstack11lll11ll11_opy_: TestFramework.bstack11l1llll111_opy_,
            TestFramework.bstack11ll111llll_opy_: test_id,
            TestFramework.bstack11l11ll111l_opy_: bstack11l11l1l1ll_opy_
        }
    @staticmethod
    def __11l1l11l111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll1lll_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᣜ"), [])
            markers.extend([getattr(m, bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᣝ"), None) for m in own_markers if getattr(m, bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣᣞ"), None)])
            current = getattr(current, bstack1ll1lll_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᣟ"), None)
        return markers
    @staticmethod
    def __11l1l1l1ll1_opy_(location):
        return bstack1ll1lll_opy_ (u"ࠧࡀ࠺ࠣᣠ").join(filter(lambda x: isinstance(x, str), location))