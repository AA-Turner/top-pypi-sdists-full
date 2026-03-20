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
bstack1l1111l11ll_opy_ = bstack11lll1_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᠺ")
bstack11l11l1llll_opy_ = bstack11lll1_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᠻ")
bstack11l11ll11ll_opy_ = bstack11lll1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᠼ")
bstack11l11ll1111_opy_ = bstack11lll1_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᠽ")
bstack11l11l1ll1l_opy_ = bstack11lll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᠾ")
_1l11111l1ll_opy_ = set()
class bstack1l1ll1111l1_opy_(TestFramework):
    bstack11l11ll1ll1_opy_ = bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᠿ")
    bstack11l1ll1ll11_opy_ = bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᡀ")
    bstack11l1l111lll_opy_ = bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᡁ")
    bstack11l1ll1lll1_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᡂ")
    bstack11l1lll11l1_opy_ = bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᡃ")
    bstack11ll1111111_opy_: bool
    bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_  = None
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
        bstack1l11ll1l11l_opy_: List[str]=[bstack11lll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᡄ")],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_=None,
        bstack1l1lll11l11_opy_=None
    ):
        super().__init__(bstack1l11ll1l11l_opy_, bstack11l1llll111_opy_, bstack1ll1l11l1l1_opy_)
        self.bstack11ll1111111_opy_ = any(bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᡅ") in item.lower() for item in bstack1l11ll1l11l_opy_)
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
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1ll1111l1_opy_.bstack11l1ll11l1l_opy_:
            bstack11l1l1llll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack11lll1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᡆ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠨࠢᡇ"))
            return
        if not self.bstack11ll1111111_opy_:
            self.logger.warning(bstack11lll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᡈ") + str(str(self.bstack1l11ll1l11l_opy_)) + bstack11lll1_opy_ (u"ࠣࠤᡉ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11lll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᡊ") + str(kwargs) + bstack11lll1_opy_ (u"ࠥࠦᡋ"))
            return
        instance = self.__11l1l11llll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᡌ") + str(args) + bstack11lll1_opy_ (u"ࠧࠨᡍ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1ll1111l1_opy_.bstack11l1ll11l1l_opy_:
                bstack11lllll1_opy_ = bstack11lll1_opy_ (u"ࠨࠢᡎ")
                name = bstack11lll1_opy_ (u"ࠢࠣᡏ")
                if (test_hook_state == TestHookState.PRE):
                    bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l11l1lll1_opy_.value)
                    name = str(EVENTS.bstack11l11l1lll1_opy_.name)+bstack11lll1_opy_ (u"ࠣ࠼ࠥᡐ")+str(test_framework_state.name)
                else:
                    bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l11ll11l1_opy_.value)
                    name = str(EVENTS.bstack11l11ll11l1_opy_.name)+bstack11lll1_opy_ (u"ࠤ࠽ࠦᡑ")+str(test_framework_state.name)
                TestFramework.bstack11l1l1lll11_opy_(instance, name, bstack11lllll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᡒ").format(e))
        try:
            if not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11lll111lll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1ll1111l1_opy_.__11l1ll111l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11lll1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᡓ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠧࠨᡔ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1llll_opy_):
                    TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lll1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᡕ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠢࠣᡖ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1111l_opy_):
                    TestFramework.bstack1ll1ll1l1l_opy_(instance, TestFramework.bstack1l111l1111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lll1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᡗ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠤࠥᡘ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1ll1111l1_opy_.__11l1l1l1lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1l1l1l1l_opy_(instance, *args)
                self.__11l11lll1l1_opy_(instance)
            elif test_framework_state in bstack1l1ll1111l1_opy_.bstack11l1ll11l1l_opy_:
                self.__11l1l1ll111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᡙ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠦࠧᡚ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1ll1111l1_opy_.bstack11l1ll11l1l_opy_:
                bstack11lllll1_opy_ = bstack11lll1_opy_ (u"ࠧࠨᡛ")
                name = bstack11lll1_opy_ (u"ࠨࠢᡜ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l1lll1_opy_.name)+bstack11lll1_opy_ (u"ࠢ࠻ࠤᡝ")+str(test_framework_state.name)
                    bstack11lllll1_opy_ = TestFramework.bstack11l1l1l1l11_opy_(instance, name)
                    bstack1llll11l_opy_.end(EVENTS.bstack11l11l1lll1_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᡞ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᡟ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11ll11l1_opy_.name)+bstack11lll1_opy_ (u"ࠥ࠾ࠧᡠ")+str(test_framework_state.name)
                    bstack11lllll1_opy_ = TestFramework.bstack11l1l1l1l11_opy_(instance, name)
                    bstack1llll11l_opy_.end(EVENTS.bstack11l11ll11l1_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᡡ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᡢ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᡣ").format(e))
    def bstack1l111ll1l11_opy_(self):
        return self.bstack11ll1111111_opy_
    def bstack11lllll1l1l_opy_(self):
        return False
    def __11l1ll11lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11lll1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᡤ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1111ll111_opy_(rep, [bstack11lll1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᡥ"), bstack11lll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᡦ"), bstack11lll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᡧ"), bstack11lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᡨ"), bstack11lll1_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᡩ"), bstack11lll1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᡪ")])
        return None
    def __11l1l1l1l1l_opy_(self, instance: bstack1ll111l1111_opy_, *args):
        result = self.__11l1ll11lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lllll11_opy_ = None
        if result.get(bstack11lll1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᡫ"), None) == bstack11lll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᡬ") and len(args) > 1 and getattr(args[1], bstack11lll1_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᡭ"), None) is not None:
            failure = [{bstack11lll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᡮ"): [args[1].excinfo.exconly(), result.get(bstack11lll1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᡯ"), None)]}]
            bstack1ll1lllll11_opy_ = bstack11lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᡰ") if bstack11lll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᡱ") in getattr(args[1].excinfo, bstack11lll1_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᡲ"), bstack11lll1_opy_ (u"ࠣࠤᡳ")) else bstack11lll1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᡴ")
        bstack11l11lllll1_opy_ = result.get(bstack11lll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᡵ"), TestFramework.bstack11l11ll1lll_opy_)
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
            target = None # bstack1l1111l1l11_opy_ bstack11l1lll111l_opy_ this to be bstack11lll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᡶ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l1l11l11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack11lll1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᡷ"), None), bstack11lll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᡸ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11lll1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᡹"), None):
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
        bstack11l1llll11l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1111l1_opy_.bstack11l1ll1ll11_opy_, {})
        if not key in bstack11l1llll11l_opy_:
            bstack11l1llll11l_opy_[key] = []
        bstack11l1l111l1l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1111l1_opy_.bstack11l1l111lll_opy_, {})
        if not key in bstack11l1l111l1l_opy_:
            bstack11l1l111l1l_opy_[key] = []
        bstack11l1l1lll1l_opy_ = {
            bstack1l1ll1111l1_opy_.bstack11l1ll1ll11_opy_: bstack11l1llll11l_opy_,
            bstack1l1ll1111l1_opy_.bstack11l1l111lll_opy_: bstack11l1l111l1l_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack11lll1_opy_ (u"ࠣ࡭ࡨࡽࠧ᡺"): key,
                TestFramework.bstack11l1l1ll11l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1ll1l_opy_: TestFramework.bstack11l1l111ll1_opy_,
                TestFramework.bstack11l1ll1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1llllll1_opy_: [],
                TestFramework.bstack11l1lll11ll_opy_: args[1] if len(args) > 1 else bstack11lll1_opy_ (u"ࠩࠪ᡻"),
                TestFramework.bstack11l1l1l1111_opy_: bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()
            }
            bstack11l1llll11l_opy_[key].append(hook)
            bstack11l1l1lll1l_opy_[bstack1l1ll1111l1_opy_.bstack11l1ll1lll1_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll1llll_opy_ = bstack11l1llll11l_opy_.get(key, [])
            hook = bstack11l1ll1llll_opy_.pop() if bstack11l1ll1llll_opy_ else None
            if hook:
                result = self.__11l1ll11lll_opy_(*args)
                if result:
                    bstack11l1l1l11ll_opy_ = result.get(bstack11lll1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᡼"), TestFramework.bstack11l1l111ll1_opy_)
                    if bstack11l1l1l11ll_opy_ != TestFramework.bstack11l1l111ll1_opy_:
                        hook[TestFramework.bstack11l1ll1ll1l_opy_] = bstack11l1l1l11ll_opy_
                hook[TestFramework.bstack11l1l1l11l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1111_opy_]= bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()
                self.bstack11l1ll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1l1ll1l1_opy_, [])
                if logs: self.bstack11lllll1ll1_opy_(instance, logs)
                bstack11l1l111l1l_opy_[key].append(hook)
                bstack11l1l1lll1l_opy_[bstack1l1ll1111l1_opy_.bstack11l1lll11l1_opy_] = key
        TestFramework.bstack11l1l11lll1_opy_(instance, bstack11l1l1lll1l_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥ᡽") + str(bstack11l1l111l1l_opy_) + bstack11lll1_opy_ (u"ࠧࠨ᡾"))
    def __11l1l1lllll_opy_(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1111ll111_opy_(args[0], [bstack11lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ᡿"), bstack11lll1_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᢀ"), bstack11lll1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᢁ"), bstack11lll1_opy_ (u"ࠤ࡬ࡨࡸࠨᢂ"), bstack11lll1_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᢃ"), bstack11lll1_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᢄ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᢅ")) else fixturedef.get(bstack11lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᢆ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11lll1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᢇ")) else None
        node = request.node if hasattr(request, bstack11lll1_opy_ (u"ࠣࡰࡲࡨࡪࠨᢈ")) else None
        target = request.node.nodeid if hasattr(node, bstack11lll1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᢉ")) else None
        baseid = fixturedef.get(bstack11lll1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᢊ"), None) or bstack11lll1_opy_ (u"ࠦࠧᢋ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11lll1_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᢌ")):
            target = bstack1l1ll1111l1_opy_.__11l1ll1l1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11lll1_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᢍ")) else None
            if target and not TestFramework.bstack1ll11l11l11_opy_(target):
                self.__11l1l11l11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11lll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᢎ") + str(test_hook_state) + bstack11lll1_opy_ (u"ࠣࠤᢏ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11lll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᢐ") + str(target) + bstack11lll1_opy_ (u"ࠥࠦᢑ"))
            return None
        instance = TestFramework.bstack1ll11l11l11_opy_(target)
        if not instance:
            self.logger.warning(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᢒ") + str(target) + bstack11lll1_opy_ (u"ࠧࠨᢓ"))
            return None
        bstack11l1l11l1ll_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, bstack1l1ll1111l1_opy_.bstack11l11ll1ll1_opy_, {})
        if os.getenv(bstack11lll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᢔ"), bstack11lll1_opy_ (u"ࠢ࠲ࠤᢕ")) == bstack11lll1_opy_ (u"ࠣ࠳ࠥᢖ"):
            bstack11l11ll1l1l_opy_ = bstack11lll1_opy_ (u"ࠤ࠽ࠦᢗ").join((scope, fixturename))
            bstack11l1l1111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1ll11111_opy_ = {
                bstack11lll1_opy_ (u"ࠥ࡯ࡪࡿࠢᢘ"): bstack11l11ll1l1l_opy_,
                bstack11lll1_opy_ (u"ࠦࡹࡧࡧࡴࠤᢙ"): bstack1l1ll1111l1_opy_.__11ll111111l_opy_(request.node),
                bstack11lll1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᢚ"): fixturedef,
                bstack11lll1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᢛ"): scope,
                bstack11lll1_opy_ (u"ࠢࡵࡻࡳࡩࠧᢜ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack11lll1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᢝ"), None)):
                    bstack11l1ll11111_opy_[bstack11lll1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᢞ")] = TestFramework.bstack1l1111lll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1ll11111_opy_[bstack11lll1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᢟ")] = uuid4().__str__()
                bstack11l1ll11111_opy_[bstack1l1ll1111l1_opy_.bstack11l1ll1l1ll_opy_] = bstack11l1l1111ll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1ll11111_opy_[bstack1l1ll1111l1_opy_.bstack11l1l1l11l1_opy_] = bstack11l1l1111ll_opy_
            if bstack11l11ll1l1l_opy_ in bstack11l1l11l1ll_opy_:
                bstack11l1l11l1ll_opy_[bstack11l11ll1l1l_opy_].update(bstack11l1ll11111_opy_)
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᢠ") + str(bstack11l1l11l1ll_opy_[bstack11l11ll1l1l_opy_]) + bstack11lll1_opy_ (u"ࠧࠨᢡ"))
            else:
                bstack11l1l11l1ll_opy_[bstack11l11ll1l1l_opy_] = bstack11l1ll11111_opy_
                self.logger.debug(bstack11lll1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᢢ") + str(len(bstack11l1l11l1ll_opy_)) + bstack11lll1_opy_ (u"ࠢࠣᢣ"))
        TestFramework.bstack1ll1ll1l1l_opy_(instance, bstack1l1ll1111l1_opy_.bstack11l11ll1ll1_opy_, bstack11l1l11l1ll_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᢤ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠤࠥᢥ"))
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
            bstack1l1ll1111l1_opy_.bstack11l11ll1ll1_opy_: {},
            bstack1l1ll1111l1_opy_.bstack11l1l111lll_opy_: {},
            bstack1l1ll1111l1_opy_.bstack11l1ll1ll11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1ll1l1l_opy_(ob, TestFramework.bstack11l11lll11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1ll1l1l_opy_(ob, TestFramework.bstack1l11lll1ll1_opy_, context.platform_index)
        TestFramework.bstack11l1lll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11lll1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᢦ") + str(TestFramework.bstack11l1lll111_opy_.keys()) + bstack11lll1_opy_ (u"ࠦࠧᢧ"))
        return ob
    def bstack1l1111111l1_opy_(self, instance: bstack1ll111l1111_opy_, bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1l111l_opy_ = (
            bstack1l1ll1111l1_opy_.bstack11l1ll1lll1_opy_
            if bstack1ll1l111111_opy_[1] == TestHookState.PRE
            else bstack1l1ll1111l1_opy_.bstack11l1lll11l1_opy_
        )
        hook = bstack1l1ll1111l1_opy_.bstack11l1ll1111l_opy_(instance, bstack11l1l1l111l_opy_)
        entries = hook.get(TestFramework.bstack11l1llllll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, []))
        return entries
    def bstack1l1111llll1_opy_(self, instance: bstack1ll111l1111_opy_, bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1l1l111l_opy_ = (
            bstack1l1ll1111l1_opy_.bstack11l1ll1lll1_opy_
            if bstack1ll1l111111_opy_[1] == TestHookState.PRE
            else bstack1l1ll1111l1_opy_.bstack11l1lll11l1_opy_
        )
        bstack1l1ll1111l1_opy_.bstack11l1l1l1ll1_opy_(instance, bstack11l1l1l111l_opy_)
        TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack11l1l11ll1l_opy_, []).clear()
    def bstack11l1ll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᢨ")
        global _1l11111l1ll_opy_
        platform_index = os.environ[bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ᢩ࠭")]
        bstack1l1111l111l_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), bstack11l11ll1111_opy_)
        if not os.path.exists(bstack1l1111l111l_opy_) or not os.path.isdir(bstack1l1111l111l_opy_):
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࡷࠥࡺ࡯ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡾࢁࠧᢪ").format(bstack1l1111l111l_opy_))
            return
        logs = hook.get(bstack11lll1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᢫"), [])
        with os.scandir(bstack1l1111l111l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111l1ll_opy_:
                    self.logger.info(bstack11lll1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ᢬").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11lll1_opy_ (u"ࠥࠦ᢭")
                    log_entry = bstack1l1ll1111ll_opy_(
                        kind=bstack11lll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᢮"),
                        message=bstack11lll1_opy_ (u"ࠧࠨ᢯"),
                        level=bstack11lll1_opy_ (u"ࠨࠢᢰ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11111111l_opy_=entry.stat().st_size,
                        bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᢱ"),
                        bstack11111l1_opy_=os.path.abspath(entry.path),
                        bstack11l1l11ll11_opy_=hook.get(TestFramework.bstack11l1l1ll11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111l1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᢲ")]
        bstack11l1lll1lll_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), bstack11l11ll1111_opy_, bstack11l11l1ll1l_opy_)
        if not os.path.exists(bstack11l1lll1lll_opy_) or not os.path.isdir(bstack11l1lll1lll_opy_):
            self.logger.info(bstack11lll1_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᢳ").format(bstack11l1lll1lll_opy_))
        else:
            self.logger.info(bstack11lll1_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᢴ").format(bstack11l1lll1lll_opy_))
            with os.scandir(bstack11l1lll1lll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack11lll1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᢵ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11lll1_opy_ (u"ࠧࠨᢶ")
                        log_entry = bstack1l1ll1111ll_opy_(
                            kind=bstack11lll1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᢷ"),
                            message=bstack11lll1_opy_ (u"ࠢࠣᢸ"),
                            level=bstack11lll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᢹ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11111111l_opy_=entry.stat().st_size,
                            bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᢺ"),
                            bstack11111l1_opy_=os.path.abspath(entry.path),
                            bstack1l111l111ll_opy_=hook.get(TestFramework.bstack11l1l1ll11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111l1ll_opy_.add(abs_path)
        hook[bstack11lll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᢻ")] = logs
    def bstack11lllll1ll1_opy_(
        self,
        bstack1l1111lllll_opy_: bstack1ll111l1111_opy_,
        entries: List[bstack1l1ll1111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᢼ"))
        req.platform_index = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll1ll1_opy_)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᢽ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111lllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111lllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111lllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l111l11lll_opy_)
            log_entry.uuid = entry.bstack11l1l11ll11_opy_
            log_entry.test_framework_state = bstack1l1111lllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᢾ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11lll1_opy_ (u"ࠢࠣᢿ")
            if entry.kind == bstack11lll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᣀ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11111111l_opy_
                log_entry.file_path = entry.bstack11111l1_opy_
        def bstack1l111111ll1_opy_():
            bstack111ll1l1_opy_ = datetime.now()
            try:
                self.bstack1l1lll11l11_opy_.LogCreatedEvent(req)
                bstack1l1111lllll_opy_.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᣁ"), datetime.now() - bstack111ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᣂ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l111111ll1_opy_)
    def __11l11lll1l1_opy_(self, instance) -> None:
        bstack11lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᣃ")
        bstack11l1l1lll1l_opy_ = {bstack11lll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᣄ"): bstack1l1lll1lll1_opy_.bstack11l1l1ll1ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l11lll1_opy_(instance, bstack11l1l1lll1l_opy_)
    @staticmethod
    def bstack11l1ll1111l_opy_(instance: bstack1ll111l1111_opy_, bstack11l1l1l111l_opy_: str):
        bstack11l11llll1l_opy_ = (
            bstack1l1ll1111l1_opy_.bstack11l1l111lll_opy_
            if bstack11l1l1l111l_opy_ == bstack1l1ll1111l1_opy_.bstack11l1lll11l1_opy_
            else bstack1l1ll1111l1_opy_.bstack11l1ll1ll11_opy_
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
        hook = bstack1l1ll1111l1_opy_.bstack11l1ll1111l_opy_(instance, bstack11l1l1l111l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1llllll1_opy_, []).clear()
    @staticmethod
    def __11l1l1l1lll_opy_(instance: bstack1ll111l1111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11lll1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᣅ"), None)):
            return
        if os.getenv(bstack11lll1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᣆ"), bstack11lll1_opy_ (u"ࠣ࠳ࠥᣇ")) != bstack11lll1_opy_ (u"ࠤ࠴ࠦᣈ"):
            bstack1l1ll1111l1_opy_.logger.warning(bstack11lll1_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᣉ"))
            return
        bstack11l1l11l1l1_opy_ = {
            bstack11lll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᣊ"): (bstack1l1ll1111l1_opy_.bstack11l1ll1lll1_opy_, bstack1l1ll1111l1_opy_.bstack11l1ll1ll11_opy_),
            bstack11lll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᣋ"): (bstack1l1ll1111l1_opy_.bstack11l1lll11l1_opy_, bstack1l1ll1111l1_opy_.bstack11l1l111lll_opy_),
        }
        for when in (bstack11lll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᣌ"), bstack11lll1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᣍ"), bstack11lll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᣎ")):
            bstack11l11lll1ll_opy_ = args[1].get_records(when)
            if not bstack11l11lll1ll_opy_:
                continue
            records = [
                bstack1l1ll1111ll_opy_(
                    kind=TestFramework.bstack11lllll1l11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11lll1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᣏ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11lll1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᣐ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l11lll1ll_opy_
                if isinstance(getattr(r, bstack11lll1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᣑ"), None), str) and r.message.strip()
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
    def __11l1ll111l1_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1ll1111l1_opy_.__11l1ll1l1l1_opy_(test.location) if hasattr(test, bstack11lll1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᣒ")) else getattr(test, bstack11lll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᣓ"), None)
        test_name = test.name if hasattr(test, bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᣔ")) else None
        bstack11l11llllll_opy_ = test.fspath.strpath if hasattr(test, bstack11lll1_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᣕ")) and test.fspath else None
        if not test_id or not test_name or not bstack11l11llllll_opy_:
            return None
        code = None
        if hasattr(test, bstack11lll1_opy_ (u"ࠤࡲࡦ࡯ࠨᣖ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l11ll111l_opy_ = []
        try:
            bstack11l11ll111l_opy_ = bstack1ll1l1l1l1_opy_.bstack1lllll11l11_opy_(test)
        except:
            bstack1l1ll1111l1_opy_.logger.warning(bstack11lll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᣗ"))
        return {
            TestFramework.bstack1l11llll11l_opy_: uuid4().__str__(),
            TestFramework.bstack11lll111lll_opy_: test_id,
            TestFramework.bstack1l11ll1llll_opy_: test_name,
            TestFramework.bstack11lllll1111_opy_: getattr(test, bstack11lll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᣘ"), None),
            TestFramework.bstack11l1lll1111_opy_: bstack11l11llllll_opy_,
            TestFramework.bstack11l1ll1l11l_opy_: bstack1l1ll1111l1_opy_.__11ll111111l_opy_(test),
            TestFramework.bstack11l1l111l11_opy_: code,
            TestFramework.bstack11lll11111l_opy_: TestFramework.bstack11l11ll1lll_opy_,
            TestFramework.bstack11ll11ll11l_opy_: test_id,
            TestFramework.bstack11l11ll1l11_opy_: bstack11l11ll111l_opy_
        }
    @staticmethod
    def __11ll111111l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11lll1_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᣙ"), [])
            markers.extend([getattr(m, bstack11lll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᣚ"), None) for m in own_markers if getattr(m, bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᣛ"), None)])
            current = getattr(current, bstack11lll1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᣜ"), None)
        return markers
    @staticmethod
    def __11l1ll1l1l1_opy_(location):
        return bstack11lll1_opy_ (u"ࠤ࠽࠾ࠧᣝ").join(filter(lambda x: isinstance(x, str), location))