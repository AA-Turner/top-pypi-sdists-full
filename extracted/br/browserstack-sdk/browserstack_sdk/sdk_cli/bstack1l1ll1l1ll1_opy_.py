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
bstack1l1111l1l1l_opy_ = bstack1111l_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤ៽")
bstack11l1l11ll11_opy_ = bstack1111l_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ៾")
bstack11l1l11l111_opy_ = bstack1111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣ៿")
bstack11l1l111lll_opy_ = bstack1111l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ᠀")
bstack11l1l11l1ll_opy_ = bstack1111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ᠁")
_1l11111l1ll_opy_ = set()
class bstack1l1ll11lll1_opy_(TestFramework):
    bstack11l1l1l11l1_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ᠂")
    bstack11ll11l111l_opy_ = bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨ᠃")
    bstack11ll1111ll1_opy_ = bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ᠄")
    bstack11l1ll11l1l_opy_ = bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧ᠅")
    bstack11l1lll1l11_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢ᠆")
    bstack11l1llll1l1_opy_: bool
    bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_  = None
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
        bstack1l11lll111l_opy_: List[str]=[bstack1111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧ᠇")],
        bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_=None,
        bstack1ll1ll1lll1_opy_=None
    ):
        super().__init__(bstack1l11lll111l_opy_, bstack11l1l11llll_opy_, bstack1ll1ll11lll_opy_)
        self.bstack11l1llll1l1_opy_ = any(bstack1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨ᠈") in item.lower() for item in bstack1l11lll111l_opy_)
        self.bstack1ll1ll1lll1_opy_ = bstack1ll1ll1lll1_opy_
    def track_event(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1ll11lll1_opy_.bstack11l1ll1l111_opy_:
            bstack11l1l1lll11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣ᠉") + str(test_hook_state) + bstack1111l_opy_ (u"ࠣࠤ᠊"))
            return
        if not self.bstack11l1llll1l1_opy_:
            self.logger.warning(bstack1111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥ᠋") + str(str(self.bstack1l11lll111l_opy_)) + bstack1111l_opy_ (u"ࠥࠦ᠌"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᠍") + str(kwargs) + bstack1111l_opy_ (u"ࠧࠨ᠎"))
            return
        instance = self.__11ll11l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧ᠏") + str(args) + bstack1111l_opy_ (u"ࠢࠣ᠐"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1ll11lll1_opy_.bstack11l1ll1l111_opy_:
                bstack1l1llll1_opy_ = bstack1111l_opy_ (u"ࠣࠤ᠑")
                name = bstack1111l_opy_ (u"ࠤࠥ᠒")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11l1l11ll1l_opy_.value)
                    name = str(EVENTS.bstack11l1l11ll1l_opy_.name)+bstack1111l_opy_ (u"ࠥ࠾ࠧ᠓")+str(test_framework_state.name)
                else:
                    bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack11l1l111ll1_opy_.value)
                    name = str(EVENTS.bstack11l1l111ll1_opy_.name)+bstack1111l_opy_ (u"ࠦ࠿ࠨ᠔")+str(test_framework_state.name)
                TestFramework.bstack11l1ll1l11l_opy_(instance, name, bstack1l1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤ᠕").format(e))
        try:
            if not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack11llll1l1l1_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1ll11lll1_opy_.__11l1lllll1l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1111l_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᠖") + str(test_hook_state) + bstack1111l_opy_ (u"ࠢࠣ᠗"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11l111l11_opy_):
                    TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l111l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᠘") + str(test_hook_state) + bstack1111l_opy_ (u"ࠤࠥ᠙"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_):
                    TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᠚") + str(test_hook_state) + bstack1111l_opy_ (u"ࠦࠧ᠛"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1ll11lll1_opy_.__11l1ll1l1l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll111l111_opy_(instance, *args)
                self.__11ll1111l1l_opy_(instance)
            elif test_framework_state in bstack1l1ll11lll1_opy_.bstack11l1ll1l111_opy_:
                self.__11ll111l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᠜") + str(instance.ref()) + bstack1111l_opy_ (u"ࠨࠢ᠝"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1lll1ll1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1ll11lll1_opy_.bstack11l1ll1l111_opy_:
                bstack1l1llll1_opy_ = bstack1111l_opy_ (u"ࠢࠣ᠞")
                name = bstack1111l_opy_ (u"ࠣࠤ᠟")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1l11ll1l_opy_.name)+bstack1111l_opy_ (u"ࠤ࠽ࠦᠠ")+str(test_framework_state.name)
                    bstack1l1llll1_opy_ = TestFramework.bstack11l1lllllll_opy_(instance, name)
                    bstack1l11ll1l1_opy_.end(EVENTS.bstack11l1l11ll1l_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᠡ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᠢ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1l111ll1_opy_.name)+bstack1111l_opy_ (u"ࠧࡀࠢᠣ")+str(test_framework_state.name)
                    bstack1l1llll1_opy_ = TestFramework.bstack11l1lllllll_opy_(instance, name)
                    bstack1l11ll1l1_opy_.end(EVENTS.bstack11l1l111ll1_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᠤ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᠥ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᠦ").format(e))
    def bstack1l11111llll_opy_(self):
        return self.bstack11l1llll1l1_opy_
    def bstack1l1111l11l1_opy_(self):
        return False
    def __11ll11l11l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᠧ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11111l1l1_opy_(rep, [bstack1111l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᠨ"), bstack1111l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᠩ"), bstack1111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᠪ"), bstack1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᠫ"), bstack1111l_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᠬ"), bstack1111l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᠭ")])
        return None
    def __11ll111l111_opy_(self, instance: bstack1ll111lllll_opy_, *args):
        result = self.__11ll11l11l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll11l1l1l_opy_ = None
        if result.get(bstack1111l_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᠮ"), None) == bstack1111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᠯ") and len(args) > 1 and getattr(args[1], bstack1111l_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᠰ"), None) is not None:
            failure = [{bstack1111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᠱ"): [args[1].excinfo.exconly(), result.get(bstack1111l_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᠲ"), None)]}]
            bstack1lll11l1l1l_opy_ = bstack1111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᠳ") if bstack1111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᠴ") in getattr(args[1].excinfo, bstack1111l_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᠵ"), bstack1111l_opy_ (u"ࠥࠦᠶ")) else bstack1111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᠷ")
        bstack11l1llll1ll_opy_ = result.get(bstack1111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᠸ"), TestFramework.bstack11ll1111l11_opy_)
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
            instance = self.__11l1llll11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111llll11_opy_ bstack11l1llllll1_opy_ this to be bstack1111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᠹ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll111111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1111l_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᠺ"), None), bstack1111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᠻ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᠼ"), None):
                target = args[0].nodeid
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
        bstack11l1ll1111l_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11lll1_opy_.bstack11ll11l111l_opy_, {})
        if not key in bstack11l1ll1111l_opy_:
            bstack11l1ll1111l_opy_[key] = []
        bstack11ll11ll1ll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11lll1_opy_.bstack11ll1111ll1_opy_, {})
        if not key in bstack11ll11ll1ll_opy_:
            bstack11ll11ll1ll_opy_[key] = []
        bstack11l1lllll11_opy_ = {
            bstack1l1ll11lll1_opy_.bstack11ll11l111l_opy_: bstack11l1ll1111l_opy_,
            bstack1l1ll11lll1_opy_.bstack11ll1111ll1_opy_: bstack11ll11ll1ll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1111l_opy_ (u"ࠥ࡯ࡪࡿࠢᠽ"): key,
                TestFramework.bstack11l1ll1l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack11ll111ll11_opy_: TestFramework.bstack11ll1111111_opy_,
                TestFramework.bstack11ll111l1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll11111_opy_: [],
                TestFramework.bstack11l1l1l1l11_opy_: args[1] if len(args) > 1 else bstack1111l_opy_ (u"ࠫࠬᠾ"),
                TestFramework.bstack11l1l1l1lll_opy_: bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()
            }
            bstack11l1ll1111l_opy_[key].append(hook)
            bstack11l1lllll11_opy_[bstack1l1ll11lll1_opy_.bstack11l1ll11l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l1ll11lll_opy_ = bstack11l1ll1111l_opy_.get(key, [])
            hook = bstack11l1ll11lll_opy_.pop() if bstack11l1ll11lll_opy_ else None
            if hook:
                result = self.__11ll11l11l1_opy_(*args)
                if result:
                    bstack11l1l1ll11l_opy_ = result.get(bstack1111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᠿ"), TestFramework.bstack11ll1111111_opy_)
                    if bstack11l1l1ll11l_opy_ != TestFramework.bstack11ll1111111_opy_:
                        hook[TestFramework.bstack11ll111ll11_opy_] = bstack11l1l1ll11l_opy_
                hook[TestFramework.bstack11l1ll1llll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1l1l1lll_opy_]= bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()
                self.bstack11l1ll1ll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll1ll11_opy_, [])
                if logs: self.bstack1l11l1l111l_opy_(instance, logs)
                bstack11ll11ll1ll_opy_[key].append(hook)
                bstack11l1lllll11_opy_[bstack1l1ll11lll1_opy_.bstack11l1lll1l11_opy_] = key
        TestFramework.bstack11ll1111lll_opy_(instance, bstack11l1lllll11_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᡀ") + str(bstack11ll11ll1ll_opy_) + bstack1111l_opy_ (u"ࠢࠣᡁ"))
    def __11l1llll11l_opy_(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11111l1l1_opy_(args[0], [bstack1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᡂ"), bstack1111l_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᡃ"), bstack1111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᡄ"), bstack1111l_opy_ (u"ࠦ࡮ࡪࡳࠣᡅ"), bstack1111l_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᡆ"), bstack1111l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᡇ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᡈ")) else fixturedef.get(bstack1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᡉ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᡊ")) else None
        node = request.node if hasattr(request, bstack1111l_opy_ (u"ࠥࡲࡴࡪࡥࠣᡋ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᡌ")) else None
        baseid = fixturedef.get(bstack1111l_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᡍ"), None) or bstack1111l_opy_ (u"ࠨࠢᡎ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111l_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᡏ")):
            target = bstack1l1ll11lll1_opy_.__11ll111lll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111l_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᡐ")) else None
            if target and not TestFramework.bstack1ll1l11l111_opy_(target):
                self.__11ll111111l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᡑ") + str(test_hook_state) + bstack1111l_opy_ (u"ࠥࠦᡒ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᡓ") + str(target) + bstack1111l_opy_ (u"ࠧࠨᡔ"))
            return None
        instance = TestFramework.bstack1ll1l11l111_opy_(target)
        if not instance:
            self.logger.warning(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᡕ") + str(target) + bstack1111l_opy_ (u"ࠢࠣᡖ"))
            return None
        bstack11l1lll1111_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11lll1_opy_.bstack11l1l1l11l1_opy_, {})
        if os.getenv(bstack1111l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᡗ"), bstack1111l_opy_ (u"ࠤ࠴ࠦᡘ")) == bstack1111l_opy_ (u"ࠥ࠵ࠧᡙ"):
            bstack11l1l11lll1_opy_ = bstack1111l_opy_ (u"ࠦ࠿ࠨᡚ").join((scope, fixturename))
            bstack11l1ll11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1l1ll111_opy_ = {
                bstack1111l_opy_ (u"ࠧࡱࡥࡺࠤᡛ"): bstack11l1l11lll1_opy_,
                bstack1111l_opy_ (u"ࠨࡴࡢࡩࡶࠦᡜ"): bstack1l1ll11lll1_opy_.__11ll11ll111_opy_(request.node),
                bstack1111l_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᡝ"): fixturedef,
                bstack1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᡞ"): scope,
                bstack1111l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᡟ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᡠ"), None)):
                    bstack11l1l1ll111_opy_[bstack1111l_opy_ (u"ࠦࡹࡿࡰࡦࠤᡡ")] = TestFramework.bstack1l1111l11ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l1l1ll111_opy_[bstack1111l_opy_ (u"ࠧࡻࡵࡪࡦࠥᡢ")] = uuid4().__str__()
                bstack11l1l1ll111_opy_[bstack1l1ll11lll1_opy_.bstack11ll111l1l1_opy_] = bstack11l1ll11ll1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1l1ll111_opy_[bstack1l1ll11lll1_opy_.bstack11l1ll1llll_opy_] = bstack11l1ll11ll1_opy_
            if bstack11l1l11lll1_opy_ in bstack11l1lll1111_opy_:
                bstack11l1lll1111_opy_[bstack11l1l11lll1_opy_].update(bstack11l1l1ll111_opy_)
                self.logger.debug(bstack1111l_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᡣ") + str(bstack11l1lll1111_opy_[bstack11l1l11lll1_opy_]) + bstack1111l_opy_ (u"ࠢࠣᡤ"))
            else:
                bstack11l1lll1111_opy_[bstack11l1l11lll1_opy_] = bstack11l1l1ll111_opy_
                self.logger.debug(bstack1111l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᡥ") + str(len(bstack11l1lll1111_opy_)) + bstack1111l_opy_ (u"ࠤࠥᡦ"))
        TestFramework.bstack1ll1lllll11_opy_(instance, bstack1l1ll11lll1_opy_.bstack11l1l1l11l1_opy_, bstack11l1lll1111_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᡧ") + str(instance.ref()) + bstack1111l_opy_ (u"ࠦࠧᡨ"))
        return instance
    def __11ll111111l_opy_(
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
            bstack1l1ll11lll1_opy_.bstack11l1l1l11l1_opy_: {},
            bstack1l1ll11lll1_opy_.bstack11ll1111ll1_opy_: {},
            bstack1l1ll11lll1_opy_.bstack11ll11l111l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1lllll11_opy_(ob, TestFramework.bstack11l1ll111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1lllll11_opy_(ob, TestFramework.bstack1l1l1l111ll_opy_, context.platform_index)
        TestFramework.bstack1ll1lll111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1111l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᡩ") + str(TestFramework.bstack1ll1lll111l_opy_.keys()) + bstack1111l_opy_ (u"ࠨࠢᡪ"))
        return ob
    def bstack1l111llllll_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11ll11l_opy_ = (
            bstack1l1ll11lll1_opy_.bstack11l1ll11l1l_opy_
            if bstack1ll1l111l11_opy_[1] == TestHookState.PRE
            else bstack1l1ll11lll1_opy_.bstack11l1lll1l11_opy_
        )
        hook = bstack1l1ll11lll1_opy_.bstack11l1lll1lll_opy_(instance, bstack11ll11ll11l_opy_)
        entries = hook.get(TestFramework.bstack11l1ll11111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, []))
        return entries
    def bstack1l111lll111_opy_(self, instance: bstack1ll111lllll_opy_, bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll11ll11l_opy_ = (
            bstack1l1ll11lll1_opy_.bstack11l1ll11l1l_opy_
            if bstack1ll1l111l11_opy_[1] == TestHookState.PRE
            else bstack1l1ll11lll1_opy_.bstack11l1lll1l11_opy_
        )
        bstack1l1ll11lll1_opy_.bstack11l1llll111_opy_(instance, bstack11ll11ll11l_opy_)
        TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, []).clear()
    def bstack11l1ll1ll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᡫ")
        global _1l11111l1ll_opy_
        platform_index = os.environ[bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᡬ")]
        bstack1l111l1ll1l_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), bstack11l1l111lll_opy_)
        if not os.path.exists(bstack1l111l1ll1l_opy_) or not os.path.isdir(bstack1l111l1ll1l_opy_):
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢᡭ").format(bstack1l111l1ll1l_opy_))
            return
        logs = hook.get(bstack1111l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᡮ"), [])
        with os.scandir(bstack1l111l1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11111l1ll_opy_:
                    self.logger.info(bstack1111l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᡯ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111l_opy_ (u"ࠧࠨᡰ")
                    log_entry = bstack1l1lllllll1_opy_(
                        kind=bstack1111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᡱ"),
                        message=bstack1111l_opy_ (u"ࠢࠣᡲ"),
                        level=bstack1111l_opy_ (u"ࠣࠤᡳ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11l11l1l1_opy_=entry.stat().st_size,
                        bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᡴ"),
                        bstack1llll1l_opy_=os.path.abspath(entry.path),
                        bstack11ll11l1111_opy_=hook.get(TestFramework.bstack11l1ll1l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11111l1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᡵ")]
        bstack11ll11l1l11_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), bstack11l1l111lll_opy_, bstack11l1l11l1ll_opy_)
        if not os.path.exists(bstack11ll11l1l11_opy_) or not os.path.isdir(bstack11ll11l1l11_opy_):
            self.logger.info(bstack1111l_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᡶ").format(bstack11ll11l1l11_opy_))
        else:
            self.logger.info(bstack1111l_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᡷ").format(bstack11ll11l1l11_opy_))
            with os.scandir(bstack11ll11l1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack1111l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᡸ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111l_opy_ (u"ࠢࠣ᡹")
                        log_entry = bstack1l1lllllll1_opy_(
                            kind=bstack1111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᡺"),
                            message=bstack1111l_opy_ (u"ࠤࠥ᡻"),
                            level=bstack1111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ᡼"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11l11l1l1_opy_=entry.stat().st_size,
                            bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᡽"),
                            bstack1llll1l_opy_=os.path.abspath(entry.path),
                            bstack1l111ll11ll_opy_=hook.get(TestFramework.bstack11l1ll1l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11111l1ll_opy_.add(abs_path)
        hook[bstack1111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥ᡾")] = logs
    def bstack1l11l1l111l_opy_(
        self,
        bstack1l111lll1ll_opy_: bstack1ll111lllll_opy_,
        entries: List[bstack1l1lllllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥ᡿"))
        req.platform_index = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l111ll_opy_)
        req.client_worker_id = bstack1111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᢀ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111lll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111lll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111lll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l1ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11l11ll1l_opy_)
            log_entry.uuid = entry.bstack11ll11l1111_opy_
            log_entry.test_framework_state = bstack1l111lll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᢁ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1111l_opy_ (u"ࠤࠥᢂ")
            if entry.kind == bstack1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᢃ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11l1l1_opy_
                log_entry.file_path = entry.bstack1llll1l_opy_
        def bstack1l11111lll1_opy_():
            bstack1lll1l11l_opy_ = datetime.now()
            try:
                self.bstack1ll1ll1lll1_opy_.LogCreatedEvent(req)
                bstack1l111lll1ll_opy_.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᢄ"), datetime.now() - bstack1lll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᢅ").format(str(e)))
                traceback.print_exc()
        self.bstack1ll1ll11lll_opy_.enqueue(bstack1l11111lll1_opy_)
    def __11ll1111l1l_opy_(self, instance) -> None:
        bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᢆ")
        bstack11l1lllll11_opy_ = {bstack1111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᢇ"): bstack1ll111lll11_opy_.bstack11l1lll11l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll1111lll_opy_(instance, bstack11l1lllll11_opy_)
    @staticmethod
    def bstack11l1lll1lll_opy_(instance: bstack1ll111lllll_opy_, bstack11ll11ll11l_opy_: str):
        bstack11ll11ll1l1_opy_ = (
            bstack1l1ll11lll1_opy_.bstack11ll1111ll1_opy_
            if bstack11ll11ll11l_opy_ == bstack1l1ll11lll1_opy_.bstack11l1lll1l11_opy_
            else bstack1l1ll11lll1_opy_.bstack11ll11l111l_opy_
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
        hook = bstack1l1ll11lll1_opy_.bstack11l1lll1lll_opy_(instance, bstack11ll11ll11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll11111_opy_, []).clear()
    @staticmethod
    def __11l1ll1l1l1_opy_(instance: bstack1ll111lllll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᢈ"), None)):
            return
        if os.getenv(bstack1111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᢉ"), bstack1111l_opy_ (u"ࠥ࠵ࠧᢊ")) != bstack1111l_opy_ (u"ࠦ࠶ࠨᢋ"):
            bstack1l1ll11lll1_opy_.logger.warning(bstack1111l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᢌ"))
            return
        bstack11l1lll11ll_opy_ = {
            bstack1111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᢍ"): (bstack1l1ll11lll1_opy_.bstack11l1ll11l1l_opy_, bstack1l1ll11lll1_opy_.bstack11ll11l111l_opy_),
            bstack1111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᢎ"): (bstack1l1ll11lll1_opy_.bstack11l1lll1l11_opy_, bstack1l1ll11lll1_opy_.bstack11ll1111ll1_opy_),
        }
        for when in (bstack1111l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᢏ"), bstack1111l_opy_ (u"ࠤࡦࡥࡱࡲࠢᢐ"), bstack1111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᢑ")):
            bstack11ll111l1ll_opy_ = args[1].get_records(when)
            if not bstack11ll111l1ll_opy_:
                continue
            records = [
                bstack1l1lllllll1_opy_(
                    kind=TestFramework.bstack1l1111l1111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᢒ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᢓ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll111l1ll_opy_
                if isinstance(getattr(r, bstack1111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᢔ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1lll1l1l_opy_, bstack11ll11ll1l1_opy_ = bstack11l1lll11ll_opy_.get(when, (None, None))
            bstack11ll11111ll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11l1lll1l1l_opy_, None) if bstack11l1lll1l1l_opy_ else None
            bstack11l1l1llll1_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, bstack11ll11ll1l1_opy_, None) if bstack11ll11111ll_opy_ else None
            if isinstance(bstack11l1l1llll1_opy_, dict) and len(bstack11l1l1llll1_opy_.get(bstack11ll11111ll_opy_, [])) > 0:
                hook = bstack11l1l1llll1_opy_[bstack11ll11111ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll11111_opy_ in hook:
                    hook[TestFramework.bstack11l1ll11111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack11l1l1ll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11l1lllll1l_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1ll11lll1_opy_.__11ll111lll1_opy_(test.location) if hasattr(test, bstack1111l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᢕ")) else getattr(test, bstack1111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᢖ"), None)
        test_name = test.name if hasattr(test, bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᢗ")) else None
        bstack11ll111ll1l_opy_ = test.fspath.strpath if hasattr(test, bstack1111l_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᢘ")) and test.fspath else None
        if not test_id or not test_name or not bstack11ll111ll1l_opy_:
            return None
        code = None
        if hasattr(test, bstack1111l_opy_ (u"ࠦࡴࡨࡪࠣᢙ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l1l11l11l_opy_ = []
        try:
            bstack11l1l11l11l_opy_ = bstack11l11ll1l1_opy_.bstack1lllll11ll1_opy_(test)
        except:
            bstack1l1ll11lll1_opy_.logger.warning(bstack1111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᢚ"))
        return {
            TestFramework.bstack1l11ll1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11llll1l1l1_opy_: test_id,
            TestFramework.bstack1l1l111llll_opy_: test_name,
            TestFramework.bstack1l11111l111_opy_: getattr(test, bstack1111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᢛ"), None),
            TestFramework.bstack11l1ll111l1_opy_: bstack11ll111ll1l_opy_,
            TestFramework.bstack11l1lll111l_opy_: bstack1l1ll11lll1_opy_.__11ll11ll111_opy_(test),
            TestFramework.bstack11l1ll11l11_opy_: code,
            TestFramework.bstack11lll1ll1l1_opy_: TestFramework.bstack11ll1111l11_opy_,
            TestFramework.bstack11ll1l1ll11_opy_: test_id,
            TestFramework.bstack11l1l11l1l1_opy_: bstack11l1l11l11l_opy_
        }
    @staticmethod
    def __11ll11ll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1111l_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᢜ"), [])
            markers.extend([getattr(m, bstack1111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᢝ"), None) for m in own_markers if getattr(m, bstack1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᢞ"), None)])
            current = getattr(current, bstack1111l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᢟ"), None)
        return markers
    @staticmethod
    def __11ll111lll1_opy_(location):
        return bstack1111l_opy_ (u"ࠦ࠿ࡀࠢᢠ").join(filter(lambda x: isinstance(x, str), location))