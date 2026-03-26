# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11llll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1ll_opy_ import bstack11l1l1l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1lllll1_opy_,
    TestHookState,
    bstack1ll1l11lll1_opy_,
    bstack1l1l11lll1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1111l1lll_opy_
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1ll1l1111ll_opy_ import bstack1ll11lllll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll11l1l1_opy_ import bstack1l1l11lll11_opy_
from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
bstack1l11111l1l1_opy_ = bstack1l1111l1lll_opy_()
bstack11l1l1lll11_opy_ = 1.0
bstack11lllll111l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᡕ")
bstack11l11l111l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᡖ")
bstack11l11l11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᡗ")
bstack11l11l11l11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᡘ")
bstack11l11l1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᡙ")
_1l11111llll_opy_ = set()
class bstack1l1l1l1l111_opy_(TestFramework):
    bstack11l11ll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᡚ")
    bstack11l11l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᡛ")
    bstack11l1l1lll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᡜ")
    bstack11l11l1ll11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᡝ")
    bstack11l1l11l11l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᡞ")
    bstack11l1l1llll1_opy_: bool
    bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_  = None
    bstack1l1llll1lll_opy_ = None
    bstack11l11llllll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1l111111_opy_: Dict[str, str],
        bstack1l11l1l11ll_opy_: List[str]=[bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᡟ")],
        bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_=None,
        bstack1l1llll1lll_opy_=None
    ):
        super().__init__(bstack1l11l1l11ll_opy_, bstack11l1l111111_opy_, bstack1ll1l1111ll_opy_)
        self.bstack11l1l1llll1_opy_ = any(bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᡠ") in item.lower() for item in bstack1l11l1l11ll_opy_)
        self.bstack1l1llll1lll_opy_ = bstack1l1llll1lll_opy_
    def track_event(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l1l1l111_opy_.bstack11l11llllll_opy_:
            bstack11l1l1l11ll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᡡ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠧࠨᡢ"))
            return
        if not self.bstack11l1l1llll1_opy_:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᡣ") + str(str(self.bstack1l11l1l11ll_opy_)) + bstack1ll1lll_opy_ (u"ࠢࠣᡤ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᡥ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥᡦ"))
            return
        instance = self.__11l1lll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᡧ") + str(args) + bstack1ll1lll_opy_ (u"ࠦࠧᡨ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1l1l1l111_opy_.bstack11l11llllll_opy_:
                bstack111l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࠨᡩ")
                name = bstack1ll1lll_opy_ (u"ࠨࠢᡪ")
                if (test_hook_state == TestHookState.PRE):
                    bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l111ll_opy_.value)
                    name = str(EVENTS.bstack11l11l111ll_opy_.name)+bstack1ll1lll_opy_ (u"ࠢ࠻ࠤᡫ")+str(test_framework_state.name)
                else:
                    bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11l11l11ll1_opy_.value)
                    name = str(EVENTS.bstack11l11l11ll1_opy_.name)+bstack1ll1lll_opy_ (u"ࠣ࠼ࠥᡬ")+str(test_framework_state.name)
                TestFramework.bstack11l1l11111l_opy_(instance, name, bstack111l1l1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᡭ").format(e))
        try:
            if not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack11ll1lll111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l1l1l111_opy_.__11l11lllll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᡮ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠦࠧᡯ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l111l1l111_opy_):
                    TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l111l1l111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᡰ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠨࠢᡱ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l111ll1l11_opy_):
                    TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᡲ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠣࠤᡳ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l1l1l111_opy_.__11l1ll111l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1ll1ll11_opy_(instance, *args)
                self.__11l1ll1l11l_opy_(instance)
            elif test_framework_state in bstack1l1l1l1l111_opy_.bstack11l11llllll_opy_:
                self.__11l11lll1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᡴ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠥࠦᡵ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1l11lll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1l1l1l111_opy_.bstack11l11llllll_opy_:
                bstack111l1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠦࠧᡶ")
                name = bstack1ll1lll_opy_ (u"ࠧࠨᡷ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l11l111ll_opy_.name)+bstack1ll1lll_opy_ (u"ࠨ࠺ࠣᡸ")+str(test_framework_state.name)
                    bstack111l1l1l1_opy_ = TestFramework.bstack11l1lll111l_opy_(instance, name)
                    bstack1l1l11ll1_opy_.end(EVENTS.bstack11l11l111ll_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᡹"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᡺"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l11l11ll1_opy_.name)+bstack1ll1lll_opy_ (u"ࠤ࠽ࠦ᡻")+str(test_framework_state.name)
                    bstack111l1l1l1_opy_ = TestFramework.bstack11l1lll111l_opy_(instance, name)
                    bstack1l1l11ll1_opy_.end(EVENTS.bstack11l11l11ll1_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᡼"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᡽"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ᡾").format(e))
    def bstack1l111l1l1ll_opy_(self):
        return self.bstack11l1l1llll1_opy_
    def bstack1l1111111ll_opy_(self):
        return False
    def __11l11ll1ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥ᡿"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1111lll11_opy_(rep, [bstack1ll1lll_opy_ (u"ࠢࡸࡪࡨࡲࠧᢀ"), bstack1ll1lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᢁ"), bstack1ll1lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᢂ"), bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᢃ"), bstack1ll1lll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᢄ"), bstack1ll1lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᢅ")])
        return None
    def __11l1ll1ll11_opy_(self, instance: bstack1l1l1lllll1_opy_, *args):
        result = self.__11l11ll1ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll1lll11ll_opy_ = None
        if result.get(bstack1ll1lll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᢆ"), None) == bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᢇ") and len(args) > 1 and getattr(args[1], bstack1ll1lll_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᢈ"), None) is not None:
            failure = [{bstack1ll1lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᢉ"): [args[1].excinfo.exconly(), result.get(bstack1ll1lll_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᢊ"), None)]}]
            bstack1ll1lll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᢋ") if bstack1ll1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᢌ") in getattr(args[1].excinfo, bstack1ll1lll_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᢍ"), bstack1ll1lll_opy_ (u"ࠢࠣᢎ")) else bstack1ll1lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᢏ")
        bstack11l1l1l11l1_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᢐ"), TestFramework.bstack11l11l1lll1_opy_)
        if bstack11l1l1l11l1_opy_ != TestFramework.bstack11l11l1lll1_opy_:
            TestFramework.bstack1lll1111ll_opy_(instance, TestFramework.bstack1l1111ll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l1l1lllll_opy_(instance, {
            TestFramework.bstack11ll1llll11_opy_: failure,
            TestFramework.bstack11l1l1l1ll1_opy_: bstack1ll1lll11ll_opy_,
            TestFramework.bstack11lll1111ll_opy_: bstack11l1l1l11l1_opy_,
        })
    def __11l1lll1l11_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11l1lll11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lllll11l1_opy_ bstack11l1l11ll1l_opy_ this to be bstack1ll1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᢑ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11l11ll1lll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦࠤᢒ"), None), bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᢓ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᢔ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll11ll11l1_opy_(target) if target else None
        return instance
    def __11l11lll1ll_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1lll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack1l1l1l1l111_opy_.bstack11l11l1l1l1_opy_, {})
        if not key in bstack11l1lll1lll_opy_:
            bstack11l1lll1lll_opy_[key] = []
        bstack11l1l11l111_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack1l1l1l1l111_opy_.bstack11l1l1lll1l_opy_, {})
        if not key in bstack11l1l11l111_opy_:
            bstack11l1l11l111_opy_[key] = []
        bstack11l11llll11_opy_ = {
            bstack1l1l1l1l111_opy_.bstack11l11l1l1l1_opy_: bstack11l1lll1lll_opy_,
            bstack1l1l1l1l111_opy_.bstack11l1l1lll1l_opy_: bstack11l1l11l111_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1ll1lll_opy_ (u"ࠢ࡬ࡧࡼࠦᢕ"): key,
                TestFramework.bstack11l1l111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11l11ll111l_opy_: TestFramework.bstack11l1l111l1l_opy_,
                TestFramework.bstack11l1lll11ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1lll1l1l_opy_: [],
                TestFramework.bstack11l11ll1l11_opy_: args[1] if len(args) > 1 else bstack1ll1lll_opy_ (u"ࠨࠩᢖ"),
                TestFramework.bstack11l1ll11l11_opy_: bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()
            }
            bstack11l1lll1lll_opy_[key].append(hook)
            bstack11l11llll11_opy_[bstack1l1l1l1l111_opy_.bstack11l11l1ll11_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1l1ll1ll_opy_ = bstack11l1lll1lll_opy_.get(key, [])
            hook = bstack11l1l1ll1ll_opy_.pop() if bstack11l1l1ll1ll_opy_ else None
            if hook:
                result = self.__11l11ll1ll1_opy_(*args)
                if result:
                    bstack11l1l1ll11l_opy_ = result.get(bstack1ll1lll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᢗ"), TestFramework.bstack11l1l111l1l_opy_)
                    if bstack11l1l1ll11l_opy_ != TestFramework.bstack11l1l111l1l_opy_:
                        hook[TestFramework.bstack11l11ll111l_opy_] = bstack11l1l1ll11l_opy_
                hook[TestFramework.bstack11l1l11l1l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1ll11l11_opy_]= bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()
                self.bstack11l1l11ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1l1111ll_opy_, [])
                if logs: self.bstack1l111ll11ll_opy_(instance, logs)
                bstack11l1l11l111_opy_[key].append(hook)
                bstack11l11llll11_opy_[bstack1l1l1l1l111_opy_.bstack11l1l11l11l_opy_] = key
        TestFramework.bstack11l1l1lllll_opy_(instance, bstack11l11llll11_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᢘ") + str(bstack11l1l11l111_opy_) + bstack1ll1lll_opy_ (u"ࠦࠧᢙ"))
    def __11l1lll11l1_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1111lll11_opy_(args[0], [bstack1ll1lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᢚ"), bstack1ll1lll_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᢛ"), bstack1ll1lll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᢜ"), bstack1ll1lll_opy_ (u"ࠣ࡫ࡧࡷࠧᢝ"), bstack1ll1lll_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᢞ"), bstack1ll1lll_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᢟ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll1lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᢠ")) else fixturedef.get(bstack1ll1lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᢡ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᢢ")) else None
        node = request.node if hasattr(request, bstack1ll1lll_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᢣ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᢤ")) else None
        baseid = fixturedef.get(bstack1ll1lll_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᢥ"), None) or bstack1ll1lll_opy_ (u"ࠥࠦᢦ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1lll_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᢧ")):
            target = bstack1l1l1l1l111_opy_.__11l11ll11l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1lll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᢨ")) else None
            if target and not TestFramework.bstack1ll11ll11l1_opy_(target):
                self.__11l11ll1lll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ᢩࠣ") + str(test_hook_state) + bstack1ll1lll_opy_ (u"ࠢࠣᢪ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨ᢫") + str(target) + bstack1ll1lll_opy_ (u"ࠤࠥ᢬"))
            return None
        instance = TestFramework.bstack1ll11ll11l1_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧ᢭") + str(target) + bstack1ll1lll_opy_ (u"ࠦࠧ᢮"))
            return None
        bstack11l1l1111l1_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack1l1l1l1l111_opy_.bstack11l11ll11ll_opy_, {})
        if os.getenv(bstack1ll1lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨ᢯"), bstack1ll1lll_opy_ (u"ࠨ࠱ࠣᢰ")) == bstack1ll1lll_opy_ (u"ࠢ࠲ࠤᢱ"):
            bstack11l11l1llll_opy_ = bstack1ll1lll_opy_ (u"ࠣ࠼ࠥᢲ").join((scope, fixturename))
            bstack11l11lll111_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1lll1111_opy_ = {
                bstack1ll1lll_opy_ (u"ࠤ࡮ࡩࡾࠨᢳ"): bstack11l11l1llll_opy_,
                bstack1ll1lll_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᢴ"): bstack1l1l1l1l111_opy_.__11l1ll11111_opy_(request.node),
                bstack1ll1lll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᢵ"): fixturedef,
                bstack1ll1lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᢶ"): scope,
                bstack1ll1lll_opy_ (u"ࠨࡴࡺࡲࡨࠦᢷ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᢸ"), None)):
                    bstack11l1lll1111_opy_[bstack1ll1lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᢹ")] = TestFramework.bstack1l111l11lll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1lll1111_opy_[bstack1ll1lll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᢺ")] = uuid4().__str__()
                bstack11l1lll1111_opy_[bstack1l1l1l1l111_opy_.bstack11l1lll11ll_opy_] = bstack11l11lll111_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1lll1111_opy_[bstack1l1l1l1l111_opy_.bstack11l1l11l1l1_opy_] = bstack11l11lll111_opy_
            if bstack11l11l1llll_opy_ in bstack11l1l1111l1_opy_:
                bstack11l1l1111l1_opy_[bstack11l11l1llll_opy_].update(bstack11l1lll1111_opy_)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᢻ") + str(bstack11l1l1111l1_opy_[bstack11l11l1llll_opy_]) + bstack1ll1lll_opy_ (u"ࠦࠧᢼ"))
            else:
                bstack11l1l1111l1_opy_[bstack11l11l1llll_opy_] = bstack11l1lll1111_opy_
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᢽ") + str(len(bstack11l1l1111l1_opy_)) + bstack1ll1lll_opy_ (u"ࠨࠢᢾ"))
        TestFramework.bstack1lll1111ll_opy_(instance, bstack1l1l1l1l111_opy_.bstack11l11ll11ll_opy_, bstack11l1l1111l1_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᢿ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠣࠤᣀ"))
        return instance
    def __11l11ll1lll_opy_(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll11llll1l_opy_.create_context(target)
        ob = bstack1l1l1lllll1_opy_(ctx, self.bstack1l11l1l11ll_opy_, self.bstack11l1l111111_opy_, test_framework_state)
        TestFramework.bstack11l1l1lllll_opy_(ob, {
            TestFramework.bstack1l11ll1l111_opy_: context.test_framework_name,
            TestFramework.bstack1l11111111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1l1l111l_opy_: [],
            bstack1l1l1l1l111_opy_.bstack11l11ll11ll_opy_: {},
            bstack1l1l1l1l111_opy_.bstack11l1l1lll1l_opy_: {},
            bstack1l1l1l1l111_opy_.bstack11l11l1l1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1111ll_opy_(ob, TestFramework.bstack11l11l1ll1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1111ll_opy_(ob, TestFramework.bstack1l11l1ll11l_opy_, context.platform_index)
        TestFramework.bstack1111l1ll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᣁ") + str(TestFramework.bstack1111l1ll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠥࠦᣂ"))
        return ob
    def bstack1l1111ll1ll_opy_(self, instance: bstack1l1l1lllll1_opy_, bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1ll1llll_opy_ = (
            bstack1l1l1l1l111_opy_.bstack11l11l1ll11_opy_
            if bstack1ll11l1l111_opy_[1] == TestHookState.PRE
            else bstack1l1l1l1l111_opy_.bstack11l1l11l11l_opy_
        )
        hook = bstack1l1l1l1l111_opy_.bstack11l1l1l1lll_opy_(instance, bstack11l1ll1llll_opy_)
        entries = hook.get(TestFramework.bstack11l1lll1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, []))
        return entries
    def bstack1l111l1ll11_opy_(self, instance: bstack1l1l1lllll1_opy_, bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1ll1llll_opy_ = (
            bstack1l1l1l1l111_opy_.bstack11l11l1ll11_opy_
            if bstack1ll11l1l111_opy_[1] == TestHookState.PRE
            else bstack1l1l1l1l111_opy_.bstack11l1l11l11l_opy_
        )
        bstack1l1l1l1l111_opy_.bstack11l1ll1111l_opy_(instance, bstack11l1ll1llll_opy_)
        TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, []).clear()
    def bstack11l1l11ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᣃ")
        global _1l11111llll_opy_
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᣄ")]
        bstack1l1111lll1l_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), bstack11l11l11l11_opy_)
        if not os.path.exists(bstack1l1111lll1l_opy_) or not os.path.isdir(bstack1l1111lll1l_opy_):
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦᣅ").format(bstack1l1111lll1l_opy_))
            return
        logs = hook.get(bstack1ll1lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᣆ"), [])
        with os.scandir(bstack1l1111lll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111llll_opy_:
                    self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᣇ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1lll_opy_ (u"ࠤࠥᣈ")
                    log_entry = bstack1l1l11lll1l_opy_(
                        kind=bstack1ll1lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᣉ"),
                        message=bstack1ll1lll_opy_ (u"ࠦࠧᣊ"),
                        level=bstack1ll1lll_opy_ (u"ࠧࠨᣋ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1111llll1_opy_=entry.stat().st_size,
                        bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᣌ"),
                        bstack111lll_opy_=os.path.abspath(entry.path),
                        bstack11l1ll11l1l_opy_=hook.get(TestFramework.bstack11l1l111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111llll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᣍ")]
        bstack11l1l111ll1_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), bstack11l11l11l11_opy_, bstack11l11l1l11l_opy_)
        if not os.path.exists(bstack11l1l111ll1_opy_) or not os.path.isdir(bstack11l1l111ll1_opy_):
            self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᣎ").format(bstack11l1l111ll1_opy_))
        else:
            self.logger.info(bstack1ll1lll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᣏ").format(bstack11l1l111ll1_opy_))
            with os.scandir(bstack11l1l111ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111llll_opy_:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᣐ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1lll_opy_ (u"ࠦࠧᣑ")
                        log_entry = bstack1l1l11lll1l_opy_(
                            kind=bstack1ll1lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᣒ"),
                            message=bstack1ll1lll_opy_ (u"ࠨࠢᣓ"),
                            level=bstack1ll1lll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᣔ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1111llll1_opy_=entry.stat().st_size,
                            bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᣕ"),
                            bstack111lll_opy_=os.path.abspath(entry.path),
                            bstack1l1111lllll_opy_=hook.get(TestFramework.bstack11l1l111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111llll_opy_.add(abs_path)
        hook[bstack1ll1lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᣖ")] = logs
    def bstack1l111ll11ll_opy_(
        self,
        bstack11llllll1l1_opy_: bstack1l1l1lllll1_opy_,
        entries: List[bstack1l1l11lll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᣗ"))
        req.platform_index = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11l1ll11l_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᣘ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack11llllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack11llllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack11llllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11ll1l111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.uuid = entry.bstack11l1ll11l1l_opy_
            log_entry.test_framework_state = bstack11llllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᣙ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1lll_opy_ (u"ࠨࠢᣚ")
            if entry.kind == bstack1ll1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᣛ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1111llll1_opy_
                log_entry.file_path = entry.bstack111lll_opy_
        def bstack1l11111l1ll_opy_():
            bstack11lllll111_opy_ = datetime.now()
            try:
                self.bstack1l1llll1lll_opy_.LogCreatedEvent(req)
                bstack11llllll1l1_opy_.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᣜ"), datetime.now() - bstack11lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᣝ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1l1111ll_opy_.enqueue(bstack1l11111l1ll_opy_)
    def __11l1ll1l11l_opy_(self, instance) -> None:
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᣞ")
        bstack11l11llll11_opy_ = {bstack1ll1lll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᣟ"): bstack1l1l11lll11_opy_.bstack11l1lll1ll1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1l1lllll_opy_(instance, bstack11l11llll11_opy_)
    @staticmethod
    def bstack11l1l1l1lll_opy_(instance: bstack1l1l1lllll1_opy_, bstack11l1ll1llll_opy_: str):
        bstack11l1ll1ll1l_opy_ = (
            bstack1l1l1l1l111_opy_.bstack11l1l1lll1l_opy_
            if bstack11l1ll1llll_opy_ == bstack1l1l1l1l111_opy_.bstack11l1l11l11l_opy_
            else bstack1l1l1l1l111_opy_.bstack11l11l1l1l1_opy_
        )
        bstack11l1l1ll111_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1llll_opy_, None)
        bstack11l1l1l1l1l_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1ll1l_opy_, None) if bstack11l1l1ll111_opy_ else None
        return (
            bstack11l1l1l1l1l_opy_[bstack11l1l1ll111_opy_][-1]
            if isinstance(bstack11l1l1l1l1l_opy_, dict) and len(bstack11l1l1l1l1l_opy_.get(bstack11l1l1ll111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1ll1111l_opy_(instance: bstack1l1l1lllll1_opy_, bstack11l1ll1llll_opy_: str):
        hook = bstack1l1l1l1l111_opy_.bstack11l1l1l1lll_opy_(instance, bstack11l1ll1llll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1lll1l1l_opy_, []).clear()
    @staticmethod
    def __11l1ll111l1_opy_(instance: bstack1l1l1lllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᣠ"), None)):
            return
        if os.getenv(bstack1ll1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᣡ"), bstack1ll1lll_opy_ (u"ࠢ࠲ࠤᣢ")) != bstack1ll1lll_opy_ (u"ࠣ࠳ࠥᣣ"):
            bstack1l1l1l1l111_opy_.logger.warning(bstack1ll1lll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᣤ"))
            return
        bstack11l1ll1lll1_opy_ = {
            bstack1ll1lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᣥ"): (bstack1l1l1l1l111_opy_.bstack11l11l1ll11_opy_, bstack1l1l1l1l111_opy_.bstack11l11l1l1l1_opy_),
            bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᣦ"): (bstack1l1l1l1l111_opy_.bstack11l1l11l11l_opy_, bstack1l1l1l1l111_opy_.bstack11l1l1lll1l_opy_),
        }
        for when in (bstack1ll1lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᣧ"), bstack1ll1lll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᣨ"), bstack1ll1lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᣩ")):
            bstack11l11lll1l1_opy_ = args[1].get_records(when)
            if not bstack11l11lll1l1_opy_:
                continue
            records = [
                bstack1l1l11lll1l_opy_(
                    kind=TestFramework.bstack1l1111l1ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1lll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᣪ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1lll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᣫ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l11lll1l1_opy_
                if isinstance(getattr(r, bstack1ll1lll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᣬ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1ll1l1ll_opy_, bstack11l1ll1ll1l_opy_ = bstack11l1ll1lll1_opy_.get(when, (None, None))
            bstack11l1l11llll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1l1ll_opy_, None) if bstack11l1ll1l1ll_opy_ else None
            bstack11l1l1l1l1l_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, bstack11l1ll1ll1l_opy_, None) if bstack11l1l11llll_opy_ else None
            if isinstance(bstack11l1l1l1l1l_opy_, dict) and len(bstack11l1l1l1l1l_opy_.get(bstack11l1l11llll_opy_, [])) > 0:
                hook = bstack11l1l1l1l1l_opy_[bstack11l1l11llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1lll1l1l_opy_ in hook:
                    hook[TestFramework.bstack11l1lll1l1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack11l1l1l111l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l11lllll1_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1l1l1l111_opy_.__11l11ll11l1_opy_(test.location) if hasattr(test, bstack1ll1lll_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᣭ")) else getattr(test, bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᣮ"), None)
        test_name = test.name if hasattr(test, bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᣯ")) else None
        bstack11l1ll111ll_opy_ = test.fspath.strpath if hasattr(test, bstack1ll1lll_opy_ (u"ࠢࡧࡵࡳࡥࡹ࡮ࠢᣰ")) and test.fspath else None
        if not test_id or not test_name or not bstack11l1ll111ll_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll1lll_opy_ (u"ࠣࡱࡥ࡮ࠧᣱ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l11l1l111_opy_ = []
        try:
            bstack11l11l1l111_opy_ = bstack11llll1l_opy_.bstack1lll1ll11l1_opy_(test)
        except:
            bstack1l1l1l1l111_opy_.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳ࠭ࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡴࡨࡷࡴࡲࡶࡦࡦࠣ࡭ࡳࠦࡃࡍࡋࠥᣲ"))
        return {
            TestFramework.bstack1l11ll11l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1lll111_opy_: test_id,
            TestFramework.bstack1l11lll1l1l_opy_: test_name,
            TestFramework.bstack11lll1lllll_opy_: getattr(test, bstack1ll1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᣳ"), None),
            TestFramework.bstack11l1ll1l1l1_opy_: bstack11l1ll111ll_opy_,
            TestFramework.bstack11l1ll1l111_opy_: bstack1l1l1l1l111_opy_.__11l1ll11111_opy_(test),
            TestFramework.bstack11l11lll11l_opy_: code,
            TestFramework.bstack11lll1111ll_opy_: TestFramework.bstack11l11l1lll1_opy_,
            TestFramework.bstack11ll11l1111_opy_: test_id,
            TestFramework.bstack11l11l11lll_opy_: bstack11l11l1l111_opy_
        }
    @staticmethod
    def __11l1ll11111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll1lll_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤᣴ"), [])
            markers.extend([getattr(m, bstack1ll1lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᣵ"), None) for m in own_markers if getattr(m, bstack1ll1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᣶"), None)])
            current = getattr(current, bstack1ll1lll_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢ᣷"), None)
        return markers
    @staticmethod
    def __11l11ll11l1_opy_(location):
        return bstack1ll1lll_opy_ (u"ࠣ࠼࠽ࠦ᣸").join(filter(lambda x: isinstance(x, str), location))