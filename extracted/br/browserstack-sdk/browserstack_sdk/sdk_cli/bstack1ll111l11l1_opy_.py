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
bstack1l11ll11ll1_opy_ = bstack1111_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᝒ")
bstack11l1l1ll1ll_opy_ = bstack1111_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᝓ")
bstack11l1ll1111l_opy_ = bstack1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᝔")
bstack11l1l1llll1_opy_ = bstack1111_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧ᝕")
bstack11l1l1lll11_opy_ = bstack1111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ᝖")
_1l111l1l11l_opy_ = set()
class bstack1l1ll1ll1l1_opy_(TestFramework):
    bstack11ll1111lll_opy_ = bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦ᝗")
    bstack11ll11lll11_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥ᝘")
    bstack11ll11ll1ll_opy_ = bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧ᝙")
    bstack11ll11l111l_opy_ = bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤ᝚")
    bstack11ll1111l1l_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ᝛")
    bstack11ll11ll111_opy_: bool
    bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_  = None
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
        bstack1l1ll111l11_opy_: List[str]=[bstack1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤ᝜")],
        bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_=None,
        bstack1lll111l111_opy_=None
    ):
        super().__init__(bstack1l1ll111l11_opy_, bstack11ll11l1l1l_opy_, bstack1ll1lllll1l_opy_)
        self.bstack11ll11ll111_opy_ = any(bstack1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥ᝝") in item.lower() for item in bstack1l1ll111l11_opy_)
        self.bstack1lll111l111_opy_ = bstack1lll111l111_opy_
    def track_event(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1ll1ll1l1_opy_.bstack11ll11llll1_opy_:
            bstack11ll11lll1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧ᝞") + str(test_hook_state) + bstack1111_opy_ (u"ࠧࠨ᝟"))
            return
        if not self.bstack11ll11ll111_opy_:
            self.logger.warning(bstack1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᝠ") + str(str(self.bstack1l1ll111l11_opy_)) + bstack1111_opy_ (u"ࠢࠣᝡ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝢ") + str(kwargs) + bstack1111_opy_ (u"ࠤࠥᝣ"))
            return
        instance = self.__11ll11l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᝤ") + str(args) + bstack1111_opy_ (u"ࠦࠧᝥ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1ll1ll1l1_opy_.bstack11ll11llll1_opy_:
                bstack1l1l1llll1_opy_ = bstack1111_opy_ (u"ࠧࠨᝦ")
                name = bstack1111_opy_ (u"ࠨࠢᝧ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l1l1lllll_opy_.value)
                    name = str(EVENTS.bstack11l1l1lllll_opy_.name)+bstack1111_opy_ (u"ࠢ࠻ࠤᝨ")+str(test_framework_state.name)
                else:
                    bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l1ll11111_opy_.value)
                    name = str(EVENTS.bstack11l1ll11111_opy_.name)+bstack1111_opy_ (u"ࠣ࠼ࠥᝩ")+str(test_framework_state.name)
                TestFramework.bstack11ll11ll11l_opy_(instance, name, bstack1l1l1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᝪ").format(e))
        try:
            if not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack11llll1ll1l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1ll1ll1l1_opy_.__11ll111l1l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1111_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᝫ") + str(test_hook_state) + bstack1111_opy_ (u"ࠦࠧᝬ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_):
                    TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ᝭") + str(test_hook_state) + bstack1111_opy_ (u"ࠨࠢᝮ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l11l1l111l_opy_):
                    TestFramework.bstack1lll1l11l1l_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᝯ") + str(test_hook_state) + bstack1111_opy_ (u"ࠣࠤᝰ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1ll1ll1l1_opy_.__11l1ll1llll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11l1lll11ll_opy_(instance, *args)
                self.__11l1lllll11_opy_(instance)
            elif test_framework_state in bstack1l1ll1ll1l1_opy_.bstack11ll11llll1_opy_:
                self.__11l1ll1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ᝱") + str(instance.ref()) + bstack1111_opy_ (u"ࠥࠦᝲ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1111l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1ll1ll1l1_opy_.bstack11ll11llll1_opy_:
                bstack1l1l1llll1_opy_ = bstack1111_opy_ (u"ࠦࠧᝳ")
                name = bstack1111_opy_ (u"ࠧࠨ᝴")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1l1lllll_opy_.name)+bstack1111_opy_ (u"ࠨ࠺ࠣ᝵")+str(test_framework_state.name)
                    bstack1l1l1llll1_opy_ = TestFramework.bstack11ll11111ll_opy_(instance, name)
                    bstack1l11l1ll_opy_.end(EVENTS.bstack11l1l1lllll_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᝶"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᝷"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1ll11111_opy_.name)+bstack1111_opy_ (u"ࠤ࠽ࠦ᝸")+str(test_framework_state.name)
                    bstack1l1l1llll1_opy_ = TestFramework.bstack11ll11111ll_opy_(instance, name)
                    bstack1l11l1ll_opy_.end(EVENTS.bstack11l1ll11111_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᝹"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᝺"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ᝻").format(e))
    def bstack1l111l1ll11_opy_(self):
        return self.bstack11ll11ll111_opy_
    def bstack1l11l11l111_opy_(self):
        return False
    def __11l1lll1lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥ᝼"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111ll11ll_opy_(rep, [bstack1111_opy_ (u"ࠢࡸࡪࡨࡲࠧ᝽"), bstack1111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᝾"), bstack1111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ᝿"), bstack1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥក"), bstack1111_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧខ"), bstack1111_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦគ")])
        return None
    def __11l1lll11ll_opy_(self, instance: bstack1ll11ll111l_opy_, *args):
        result = self.__11l1lll1lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll1111_opy_ = None
        if result.get(bstack1111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢឃ"), None) == bstack1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢង") and len(args) > 1 and getattr(args[1], bstack1111_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤច"), None) is not None:
            failure = [{bstack1111_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬឆ"): [args[1].excinfo.exconly(), result.get(bstack1111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤជ"), None)]}]
            bstack1lll1ll1111_opy_ = bstack1111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧឈ") if bstack1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣញ") in getattr(args[1].excinfo, bstack1111_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣដ"), bstack1111_opy_ (u"ࠢࠣឋ")) else bstack1111_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤឌ")
        bstack11l1lll1111_opy_ = result.get(bstack1111_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥឍ"), TestFramework.bstack11l1ll11ll1_opy_)
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
            instance = self.__11ll1l1l1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l11111_opy_ bstack11ll11111l1_opy_ this to be bstack1111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥណ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll1l1ll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1111_opy_ (u"ࠦࡳࡵࡤࡦࠤត"), None), bstack1111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧថ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨទ"), None):
                target = args[0].nodeid
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
        bstack11ll1l1l1l1_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11ll11lll11_opy_, {})
        if not key in bstack11ll1l1l1l1_opy_:
            bstack11ll1l1l1l1_opy_[key] = []
        bstack11ll1111ll1_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11ll11ll1ll_opy_, {})
        if not key in bstack11ll1111ll1_opy_:
            bstack11ll1111ll1_opy_[key] = []
        bstack11ll1l11ll1_opy_ = {
            bstack1l1ll1ll1l1_opy_.bstack11ll11lll11_opy_: bstack11ll1l1l1l1_opy_,
            bstack1l1ll1ll1l1_opy_.bstack11ll11ll1ll_opy_: bstack11ll1111ll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1111_opy_ (u"ࠢ࡬ࡧࡼࠦធ"): key,
                TestFramework.bstack11l1lll1l1l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1ll1l111_opy_: TestFramework.bstack11ll1l11l1l_opy_,
                TestFramework.bstack11ll1111111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll11l11_opy_: [],
                TestFramework.bstack11ll1l1ll1l_opy_: args[1] if len(args) > 1 else bstack1111_opy_ (u"ࠨࠩន"),
                TestFramework.bstack11ll1l1l11l_opy_: bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()
            }
            bstack11ll1l1l1l1_opy_[key].append(hook)
            bstack11ll1l11ll1_opy_[bstack1l1ll1ll1l1_opy_.bstack11ll11l111l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1lllllll_opy_ = bstack11ll1l1l1l1_opy_.get(key, [])
            hook = bstack11l1lllllll_opy_.pop() if bstack11l1lllllll_opy_ else None
            if hook:
                result = self.__11l1lll1lll_opy_(*args)
                if result:
                    bstack11ll1l1111l_opy_ = result.get(bstack1111_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥប"), TestFramework.bstack11ll1l11l1l_opy_)
                    if bstack11ll1l1111l_opy_ != TestFramework.bstack11ll1l11l1l_opy_:
                        hook[TestFramework.bstack11l1ll1l111_opy_] = bstack11ll1l1111l_opy_
                hook[TestFramework.bstack11ll111l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1l1l11l_opy_]= bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()
                self.bstack11ll111llll_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l111l1_opy_, [])
                if logs: self.bstack1l11l1l1lll_opy_(instance, logs)
                bstack11ll1111ll1_opy_[key].append(hook)
                bstack11ll1l11ll1_opy_[bstack1l1ll1ll1l1_opy_.bstack11ll1111l1l_opy_] = key
        TestFramework.bstack11l1llll111_opy_(instance, bstack11ll1l11ll1_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤផ") + str(bstack11ll1111ll1_opy_) + bstack1111_opy_ (u"ࠦࠧព"))
    def __11ll1l1l1ll_opy_(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111ll11ll_opy_(args[0], [bstack1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦភ"), bstack1111_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢម"), bstack1111_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢយ"), bstack1111_opy_ (u"ࠣ࡫ࡧࡷࠧរ"), bstack1111_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦល"), bstack1111_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥវ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥឝ")) else fixturedef.get(bstack1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦឞ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦស")) else None
        node = request.node if hasattr(request, bstack1111_opy_ (u"ࠢ࡯ࡱࡧࡩࠧហ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣឡ")) else None
        baseid = fixturedef.get(bstack1111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤអ"), None) or bstack1111_opy_ (u"ࠥࠦឣ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤឤ")):
            target = bstack1l1ll1ll1l1_opy_.__11ll1l11l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢឥ")) else None
            if target and not TestFramework.bstack1ll1l1l1lll_opy_(target):
                self.__11ll1l1ll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣឦ") + str(test_hook_state) + bstack1111_opy_ (u"ࠢࠣឧ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨឨ") + str(target) + bstack1111_opy_ (u"ࠤࠥឩ"))
            return None
        instance = TestFramework.bstack1ll1l1l1lll_opy_(target)
        if not instance:
            self.logger.warning(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧឪ") + str(target) + bstack1111_opy_ (u"ࠦࠧឫ"))
            return None
        bstack11l1llll1ll_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11ll1111lll_opy_, {})
        if os.getenv(bstack1111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨឬ"), bstack1111_opy_ (u"ࠨ࠱ࠣឭ")) == bstack1111_opy_ (u"ࠢ࠲ࠤឮ"):
            bstack11l1lll111l_opy_ = bstack1111_opy_ (u"ࠣ࠼ࠥឯ").join((scope, fixturename))
            bstack11l1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll111l1ll_opy_ = {
                bstack1111_opy_ (u"ࠤ࡮ࡩࡾࠨឰ"): bstack11l1lll111l_opy_,
                bstack1111_opy_ (u"ࠥࡸࡦ࡭ࡳࠣឱ"): bstack1l1ll1ll1l1_opy_.__11l1lll1ll1_opy_(request.node),
                bstack1111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧឲ"): fixturedef,
                bstack1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦឳ"): scope,
                bstack1111_opy_ (u"ࠨࡴࡺࡲࡨࠦ឴"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦ឵"), None)):
                    bstack11ll111l1ll_opy_[bstack1111_opy_ (u"ࠣࡶࡼࡴࡪࠨា")] = TestFramework.bstack1l11l1l1111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11ll111l1ll_opy_[bstack1111_opy_ (u"ࠤࡸࡹ࡮ࡪࠢិ")] = uuid4().__str__()
                bstack11ll111l1ll_opy_[bstack1l1ll1ll1l1_opy_.bstack11ll1111111_opy_] = bstack11l1ll1lll1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11ll111l1ll_opy_[bstack1l1ll1ll1l1_opy_.bstack11ll111l111_opy_] = bstack11l1ll1lll1_opy_
            if bstack11l1lll111l_opy_ in bstack11l1llll1ll_opy_:
                bstack11l1llll1ll_opy_[bstack11l1lll111l_opy_].update(bstack11ll111l1ll_opy_)
                self.logger.debug(bstack1111_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦី") + str(bstack11l1llll1ll_opy_[bstack11l1lll111l_opy_]) + bstack1111_opy_ (u"ࠦࠧឹ"))
            else:
                bstack11l1llll1ll_opy_[bstack11l1lll111l_opy_] = bstack11ll111l1ll_opy_
                self.logger.debug(bstack1111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣឺ") + str(len(bstack11l1llll1ll_opy_)) + bstack1111_opy_ (u"ࠨࠢុ"))
        TestFramework.bstack1lll1l11l1l_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11ll1111lll_opy_, bstack11l1llll1ll_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢូ") + str(instance.ref()) + bstack1111_opy_ (u"ࠣࠤួ"))
        return instance
    def __11ll1l1ll11_opy_(
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
            bstack1l1ll1ll1l1_opy_.bstack11ll1111lll_opy_: {},
            bstack1l1ll1ll1l1_opy_.bstack11ll11ll1ll_opy_: {},
            bstack1l1ll1ll1l1_opy_.bstack11ll11lll11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1l11l1l_opy_(ob, TestFramework.bstack11l1llll11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l11l1l_opy_(ob, TestFramework.bstack1l1l11l1ll1_opy_, context.platform_index)
        TestFramework.bstack1lll1111lll_opy_[ctx.id] = ob
        self.logger.debug(bstack1111_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤើ") + str(TestFramework.bstack1lll1111lll_opy_.keys()) + bstack1111_opy_ (u"ࠥࠦឿ"))
        return ob
    def bstack1l11l11111l_opy_(self, instance: bstack1ll11ll111l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11l1l11_opy_ = (
            bstack1l1ll1ll1l1_opy_.bstack11ll11l111l_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1l1ll1ll1l1_opy_.bstack11ll1111l1l_opy_
        )
        hook = bstack1l1ll1ll1l1_opy_.bstack11ll11lllll_opy_(instance, bstack11ll11l1l11_opy_)
        entries = hook.get(TestFramework.bstack11l1ll11l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, []))
        return entries
    def bstack1l11l11ll11_opy_(self, instance: bstack1ll11ll111l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11l1l11_opy_ = (
            bstack1l1ll1ll1l1_opy_.bstack11ll11l111l_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1l1ll1ll1l1_opy_.bstack11ll1111l1l_opy_
        )
        bstack1l1ll1ll1l1_opy_.bstack11ll1l1l111_opy_(instance, bstack11ll11l1l11_opy_)
        TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, []).clear()
    def bstack11ll111llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥៀ")
        global _1l111l1l11l_opy_
        platform_index = os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬេ")]
        bstack1l111l111l1_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), bstack11l1l1llll1_opy_)
        if not os.path.exists(bstack1l111l111l1_opy_) or not os.path.isdir(bstack1l111l111l1_opy_):
            self.logger.debug(bstack1111_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦែ").format(bstack1l111l111l1_opy_))
            return
        logs = hook.get(bstack1111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧៃ"), [])
        with os.scandir(bstack1l111l111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111l1l11l_opy_:
                    self.logger.info(bstack1111_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨោ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111_opy_ (u"ࠤࠥៅ")
                    log_entry = bstack1ll11lllll1_opy_(
                        kind=bstack1111_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧំ"),
                        message=bstack1111_opy_ (u"ࠦࠧះ"),
                        level=bstack1111_opy_ (u"ࠧࠨៈ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111l11ll1_opy_=entry.stat().st_size,
                        bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ៉"),
                        bstack1llll_opy_=os.path.abspath(entry.path),
                        bstack11ll11l1111_opy_=hook.get(TestFramework.bstack11l1lll1l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111l1l11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ៊")]
        bstack11ll111ll1l_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), bstack11l1l1llll1_opy_, bstack11l1l1lll11_opy_)
        if not os.path.exists(bstack11ll111ll1l_opy_) or not os.path.isdir(bstack11ll111ll1l_opy_):
            self.logger.info(bstack1111_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥ់").format(bstack11ll111ll1l_opy_))
        else:
            self.logger.info(bstack1111_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣ៌").format(bstack11ll111ll1l_opy_))
            with os.scandir(bstack11ll111ll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111l1l11l_opy_:
                        self.logger.info(bstack1111_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣ៍").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111_opy_ (u"ࠦࠧ៎")
                        log_entry = bstack1ll11lllll1_opy_(
                            kind=bstack1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢ៏"),
                            message=bstack1111_opy_ (u"ࠨࠢ័"),
                            level=bstack1111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ៑"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111l11ll1_opy_=entry.stat().st_size,
                            bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄ្ࠣ"),
                            bstack1llll_opy_=os.path.abspath(entry.path),
                            bstack1l111l1111l_opy_=hook.get(TestFramework.bstack11l1lll1l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111l1l11l_opy_.add(abs_path)
        hook[bstack1111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢ៓")] = logs
    def bstack1l11l1l1lll_opy_(
        self,
        bstack1l111ll11l1_opy_: bstack1ll11ll111l_opy_,
        entries: List[bstack1ll11lllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢ។"))
        req.platform_index = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l11l1ll1_opy_)
        req.client_worker_id = bstack1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ៕").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll11l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll11l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll11l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l1111l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l111llll11_opy_)
            log_entry.uuid = entry.bstack11ll11l1111_opy_
            log_entry.test_framework_state = bstack1l111ll11l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ៖"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1111_opy_ (u"ࠨࠢៗ")
            if entry.kind == bstack1111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ៘"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111l11ll1_opy_
                log_entry.file_path = entry.bstack1llll_opy_
        def bstack1l111ll1111_opy_():
            bstack1l1llll111_opy_ = datetime.now()
            try:
                self.bstack1lll111l111_opy_.LogCreatedEvent(req)
                bstack1l111ll11l1_opy_.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ៙"), datetime.now() - bstack1l1llll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣ៚").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1lllll1l_opy_.enqueue(bstack1l111ll1111_opy_)
    def __11l1lllll11_opy_(self, instance) -> None:
        bstack1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ៛")
        bstack11ll1l11ll1_opy_ = {bstack1111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨៜ"): bstack1l1ll1l1lll_opy_.bstack11l1ll1l1l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l1llll111_opy_(instance, bstack11ll1l11ll1_opy_)
    @staticmethod
    def bstack11ll11lllll_opy_(instance: bstack1ll11ll111l_opy_, bstack11ll11l1l11_opy_: str):
        bstack11l1llll1l1_opy_ = (
            bstack1l1ll1ll1l1_opy_.bstack11ll11ll1ll_opy_
            if bstack11ll11l1l11_opy_ == bstack1l1ll1ll1l1_opy_.bstack11ll1111l1l_opy_
            else bstack1l1ll1ll1l1_opy_.bstack11ll11lll11_opy_
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
        hook = bstack1l1ll1ll1l1_opy_.bstack11ll11lllll_opy_(instance, bstack11ll11l1l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll11l11_opy_, []).clear()
    @staticmethod
    def __11l1ll1llll_opy_(instance: bstack1ll11ll111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥ៝"), None)):
            return
        if os.getenv(bstack1111_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥ៞"), bstack1111_opy_ (u"ࠢ࠲ࠤ៟")) != bstack1111_opy_ (u"ࠣ࠳ࠥ០"):
            bstack1l1ll1ll1l1_opy_.logger.warning(bstack1111_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦ១"))
            return
        bstack11ll1l111ll_opy_ = {
            bstack1111_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ២"): (bstack1l1ll1ll1l1_opy_.bstack11ll11l111l_opy_, bstack1l1ll1ll1l1_opy_.bstack11ll11lll11_opy_),
            bstack1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ៣"): (bstack1l1ll1ll1l1_opy_.bstack11ll1111l1l_opy_, bstack1l1ll1ll1l1_opy_.bstack11ll11ll1ll_opy_),
        }
        for when in (bstack1111_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ៤"), bstack1111_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ៥"), bstack1111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ៦")):
            bstack11l1ll111l1_opy_ = args[1].get_records(when)
            if not bstack11l1ll111l1_opy_:
                continue
            records = [
                bstack1ll11lllll1_opy_(
                    kind=TestFramework.bstack1l111l1l1l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦ៧")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥ៨")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1ll111l1_opy_
                if isinstance(getattr(r, bstack1111_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ៩"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1ll111ll_opy_, bstack11l1llll1l1_opy_ = bstack11ll1l111ll_opy_.get(when, (None, None))
            bstack11ll111111l_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1ll111ll_opy_, None) if bstack11l1ll111ll_opy_ else None
            bstack11ll111ll11_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, bstack11l1llll1l1_opy_, None) if bstack11ll111111l_opy_ else None
            if isinstance(bstack11ll111ll11_opy_, dict) and len(bstack11ll111ll11_opy_.get(bstack11ll111111l_opy_, [])) > 0:
                hook = bstack11ll111ll11_opy_[bstack11ll111111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll11l11_opy_ in hook:
                    hook[TestFramework.bstack11l1ll11l11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11ll1l11lll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll111l1l1_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1ll1ll1l1_opy_.__11ll1l11l11_opy_(test.location) if hasattr(test, bstack1111_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨ៪")) else getattr(test, bstack1111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ៫"), None)
        test_name = test.name if hasattr(test, bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ៬")) else None
        bstack11l1lllll1l_opy_ = test.fspath.strpath if hasattr(test, bstack1111_opy_ (u"ࠢࡧࡵࡳࡥࡹ࡮ࠢ៭")) and test.fspath else None
        if not test_id or not test_name or not bstack11l1lllll1l_opy_:
            return None
        code = None
        if hasattr(test, bstack1111_opy_ (u"ࠣࡱࡥ࡮ࠧ៮")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l1l1ll1l1_opy_ = []
        try:
            bstack11l1l1ll1l1_opy_ = bstack11l111ll11_opy_.bstack11111l1l11_opy_(test)
        except:
            bstack1l1ll1ll1l1_opy_.logger.warning(bstack1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳ࠭ࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡴࡨࡷࡴࡲࡶࡦࡦࠣ࡭ࡳࠦࡃࡍࡋࠥ៯"))
        return {
            TestFramework.bstack1l1l11l1l1l_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1ll1l_opy_: test_id,
            TestFramework.bstack1l1l11lll11_opy_: test_name,
            TestFramework.bstack1l1111lll11_opy_: getattr(test, bstack1111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ៰"), None),
            TestFramework.bstack11l1lll11l1_opy_: bstack11l1lllll1l_opy_,
            TestFramework.bstack11l1ll11l1l_opy_: bstack1l1ll1ll1l1_opy_.__11l1lll1ll1_opy_(test),
            TestFramework.bstack11ll111lll1_opy_: code,
            TestFramework.bstack11lllll111l_opy_: TestFramework.bstack11l1ll11ll1_opy_,
            TestFramework.bstack11ll1lll1l1_opy_: test_id,
            TestFramework.bstack11l1l1lll1l_opy_: bstack11l1l1ll1l1_opy_
        }
    @staticmethod
    def __11l1lll1ll1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1111_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤ៱"), [])
            markers.extend([getattr(m, bstack1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ៲"), None) for m in own_markers if getattr(m, bstack1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ៳"), None)])
            current = getattr(current, bstack1111_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢ៴"), None)
        return markers
    @staticmethod
    def __11ll1l11l11_opy_(location):
        return bstack1111_opy_ (u"ࠣ࠼࠽ࠦ៵").join(filter(lambda x: isinstance(x, str), location))