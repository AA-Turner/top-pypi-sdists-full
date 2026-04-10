# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll11111l_opy_ import bstack1l1ll1l1l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack111ll11l1_opy_ import bstack111lll11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11l11ll_opy_,
    TestHookState,
    bstack1ll1ll1ll11_opy_,
    bstack111l1111ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11lll1l1111_opy_
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l111lll_opy_ import bstack1l11lll1lll_opy_
from bstack_utils.bstack1l1l11l1_opy_ import bstack111l111ll1_opy_
bstack11ll11ll111_opy_ = bstack11lll1l1111_opy_()
bstack111lll1ll11_opy_ = 1.0
bstack11lll111lll_opy_ = bstack1ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᦜ")
bstack111ll111ll1_opy_ = bstack1ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᦝ")
bstack111ll11l1l1_opy_ = bstack1ll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᦞ")
bstack111ll1111ll_opy_ = bstack1ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᦟ")
bstack111ll111l11_opy_ = bstack1ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᦠ")
_11ll11l1l11_opy_ = set()
class bstack1l1l1ll1l1l_opy_(TestFramework):
    bstack111ll1l11l1_opy_ = bstack1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᦡ")
    bstack111ll11l1ll_opy_ = bstack1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᦢ")
    bstack111lll111l1_opy_ = bstack1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᦣ")
    bstack111llll1l1l_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᦤ")
    bstack111ll1l1lll_opy_ = bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᦥ")
    bstack111llll11ll_opy_: bool
    bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_  = None
    bstack1ll11ll11l_opy_ = None
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1ll1l_opy_: Dict[str, str],
        bstack1l1l111111l_opy_: List[str]=[bstack1ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᦦ")],
        bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_=None,
        bstack1ll11ll11l_opy_=None
    ):
        super().__init__(bstack1l1l111111l_opy_, bstack1l11ll1ll1l_opy_, bstack1l1lll11ll1_opy_)
        self.bstack111llll11ll_opy_ = any(bstack1ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᦧ") in item.lower() for item in bstack1l1l111111l_opy_)
        self.bstack1ll11ll11l_opy_ = bstack1ll11ll11l_opy_
    def track_event(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1l1ll1l1l_opy_.bstack111ll1l1l1l_opy_:
            bstack111lll11l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᦨ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠥࠦᦩ"))
            return
        if not self.bstack111llll11ll_opy_:
            self.logger.warning(bstack1ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᦪ") + str(str(self.bstack1l1l111111l_opy_)) + bstack1ll_opy_ (u"ࠧࠨᦫ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᦬") + str(kwargs) + bstack1ll_opy_ (u"ࠢࠣ᦭"))
            return
        instance = self.__111ll1l1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢ᦮") + str(args) + bstack1ll_opy_ (u"ࠤࠥ᦯"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1l1ll1l1l_opy_.bstack111ll1l1l1l_opy_:
                bstack1lll1lll11_opy_ = bstack1ll_opy_ (u"ࠥࠦᦰ")
                name = bstack1ll_opy_ (u"ࠦࠧᦱ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111ll111lll_opy_.value)
                    name = str(EVENTS.bstack111ll111lll_opy_.name)+bstack1ll_opy_ (u"ࠧࡀࠢᦲ")+str(test_framework_state.name)
                else:
                    bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack111ll11l111_opy_.value)
                    name = str(EVENTS.bstack111ll11l111_opy_.name)+bstack1ll_opy_ (u"ࠨ࠺ࠣᦳ")+str(test_framework_state.name)
                TestFramework.bstack11l1111l1l1_opy_(instance, name, bstack1lll1lll11_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᦴ").format(e))
        try:
            if not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11l1ll11111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1l1ll1l1l_opy_.__111lll1l111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᦵ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠤࠥᦶ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᦷ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠦࠧᦸ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11lll111111_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11lll111111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᦹ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠨࠢᦺ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1l1ll1l1l_opy_.__111llll1lll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll11ll1_opy_(instance, *args)
                self.__11l11111l11_opy_(instance)
            elif test_framework_state in bstack1l1l1ll1l1l_opy_.bstack111ll1l1l1l_opy_:
                self.__111ll1ll11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᦻ") + str(instance.ref()) + bstack1ll_opy_ (u"ࠣࠤᦼ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111ll1ll1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1l1ll1l1l_opy_.bstack111ll1l1l1l_opy_:
                bstack1lll1lll11_opy_ = bstack1ll_opy_ (u"ࠤࠥᦽ")
                name = bstack1ll_opy_ (u"ࠥࠦᦾ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll111lll_opy_.name)+bstack1ll_opy_ (u"ࠦ࠿ࠨᦿ")+str(test_framework_state.name)
                    bstack1lll1lll11_opy_ = TestFramework.bstack111ll1ll111_opy_(instance, name)
                    bstack1l11l1ll11_opy_.end(EVENTS.bstack111ll111lll_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᧀ"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᧁ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll11l111_opy_.name)+bstack1ll_opy_ (u"ࠢ࠻ࠤᧂ")+str(test_framework_state.name)
                    bstack1lll1lll11_opy_ = TestFramework.bstack111ll1ll111_opy_(instance, name)
                    bstack1l11l1ll11_opy_.end(EVENTS.bstack111ll11l111_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᧃ"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᧄ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᧅ").format(e))
    def bstack11ll1l11lll_opy_(self):
        return self.bstack111llll11ll_opy_
    def bstack11ll1ll1l11_opy_(self):
        return False
    def __11l1111l1ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᧆ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11lll11llll_opy_(rep, [bstack1ll_opy_ (u"ࠧࡽࡨࡦࡰࠥᧇ"), bstack1ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᧈ"), bstack1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᧉ"), bstack1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ᧊"), bstack1ll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥ᧋"), bstack1ll_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤ᧌")])
        return None
    def __111lll11ll1_opy_(self, instance: bstack1l1l11l11ll_opy_, *args):
        result = self.__11l1111l1ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1lll_opy_ = None
        if result.get(bstack1ll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᧍"), None) == bstack1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᧎") and len(args) > 1 and getattr(args[1], bstack1ll_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢ᧏"), None) is not None:
            failure = [{bstack1ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ᧐"): [args[1].excinfo.exconly(), result.get(bstack1ll_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢ᧑"), None)]}]
            bstack1ll111l1lll_opy_ = bstack1ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ᧒") if bstack1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ᧓") in getattr(args[1].excinfo, bstack1ll_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨ᧔"), bstack1ll_opy_ (u"ࠧࠨ᧕")) else bstack1ll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ᧖")
        bstack111lll1l1l1_opy_ = result.get(bstack1ll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ᧗"), TestFramework.bstack11l111ll111_opy_)
        if bstack111lll1l1l1_opy_ != TestFramework.bstack11l111ll111_opy_:
            TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack111lllllll1_opy_(instance, {
            TestFramework.bstack11l1ll11l11_opy_: failure,
            TestFramework.bstack111ll1l1l11_opy_: bstack1ll111l1lll_opy_,
            TestFramework.bstack11l1ll11lll_opy_: bstack111lll1l1l1_opy_,
        })
    def __111ll1l1ll1_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll11ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1ll111l_opy_ bstack111lll1l11l_opy_ this to be bstack1ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᧘")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111ll1lll1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ᧙"), None), bstack1ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᧚"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᧛"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll1lll1l_opy_(target) if target else None
        return instance
    def __111ll1ll11l_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l111111ll_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack111ll11l1ll_opy_, {})
        if not key in bstack11l111111ll_opy_:
            bstack11l111111ll_opy_[key] = []
        bstack111lll1lll1_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack111lll111l1_opy_, {})
        if not key in bstack111lll1lll1_opy_:
            bstack111lll1lll1_opy_[key] = []
        bstack111lll11111_opy_ = {
            bstack1l1l1ll1l1l_opy_.bstack111ll11l1ll_opy_: bstack11l111111ll_opy_,
            bstack1l1l1ll1l1l_opy_.bstack111lll111l1_opy_: bstack111lll1lll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1ll_opy_ (u"ࠧࡱࡥࡺࠤ᧜"): key,
                TestFramework.bstack111lllll111_opy_: uuid4().__str__(),
                TestFramework.bstack11l1111lll1_opy_: TestFramework.bstack11l1111ll1l_opy_,
                TestFramework.bstack11l11111ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l11ll_opy_: [],
                TestFramework.bstack111ll1llll1_opy_: args[1] if len(args) > 1 else bstack1ll_opy_ (u"࠭ࠧ᧝"),
                TestFramework.bstack11l111l1ll1_opy_: bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()
            }
            bstack11l111111ll_opy_[key].append(hook)
            bstack111lll11111_opy_[bstack1l1l1ll1l1l_opy_.bstack111llll1l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111lll1llll_opy_ = bstack11l111111ll_opy_.get(key, [])
            hook = bstack111lll1llll_opy_.pop() if bstack111lll1llll_opy_ else None
            if hook:
                result = self.__11l1111l1ll_opy_(*args)
                if result:
                    bstack11l11111l1l_opy_ = result.get(bstack1ll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ᧞"), TestFramework.bstack11l1111ll1l_opy_)
                    if bstack11l11111l1l_opy_ != TestFramework.bstack11l1111ll1l_opy_:
                        hook[TestFramework.bstack11l1111lll1_opy_] = bstack11l11111l1l_opy_
                hook[TestFramework.bstack111lllll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l111l1ll1_opy_]= bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()
                self.bstack111lll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111llll1111_opy_, [])
                if logs: self.bstack11lll1lll1_opy_(instance, logs)
                bstack111lll1lll1_opy_[key].append(hook)
                bstack111lll11111_opy_[bstack1l1l1ll1l1l_opy_.bstack111ll1l1lll_opy_] = key
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢ᧟") + str(bstack111lll1lll1_opy_) + bstack1ll_opy_ (u"ࠤࠥ᧠"))
    def __111ll11ll1l_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11lll11llll_opy_(args[0], [bstack1ll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ᧡"), bstack1ll_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧ᧢"), bstack1ll_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ᧣"), bstack1ll_opy_ (u"ࠨࡩࡥࡵࠥ᧤"), bstack1ll_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤ᧥"), bstack1ll_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣ᧦")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ᧧")) else fixturedef.get(bstack1ll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ᧨"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤ᧩")) else None
        node = request.node if hasattr(request, bstack1ll_opy_ (u"ࠧࡴ࡯ࡥࡧࠥ᧪")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨ᧫")) else None
        baseid = fixturedef.get(bstack1ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢ᧬"), None) or bstack1ll_opy_ (u"ࠣࠤ᧭")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢ᧮")):
            target = bstack1l1l1ll1l1l_opy_.__11l11111lll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧ᧯")) else None
            if target and not TestFramework.bstack1l1ll1lll1l_opy_(target):
                self.__111ll1lll1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨ᧰") + str(test_hook_state) + bstack1ll_opy_ (u"ࠧࠨ᧱"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦ᧲") + str(target) + bstack1ll_opy_ (u"ࠢࠣ᧳"))
            return None
        instance = TestFramework.bstack1l1ll1lll1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥ᧴") + str(target) + bstack1ll_opy_ (u"ࠤࠥ᧵"))
            return None
        bstack111llllll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack111ll1l11l1_opy_, {})
        if os.getenv(bstack1ll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦ᧶"), bstack1ll_opy_ (u"ࠦ࠶ࠨ᧷")) == bstack1ll_opy_ (u"ࠧ࠷ࠢ᧸"):
            bstack11l111l1111_opy_ = bstack1ll_opy_ (u"ࠨ࠺ࠣ᧹").join((scope, fixturename))
            bstack11l111l1l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack11l111l1lll_opy_ = {
                bstack1ll_opy_ (u"ࠢ࡬ࡧࡼࠦ᧺"): bstack11l111l1111_opy_,
                bstack1ll_opy_ (u"ࠣࡶࡤ࡫ࡸࠨ᧻"): bstack1l1l1ll1l1l_opy_.__11l111l11l1_opy_(request.node),
                bstack1ll_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥ᧼"): fixturedef,
                bstack1ll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ᧽"): scope,
                bstack1ll_opy_ (u"ࠦࡹࡿࡰࡦࠤ᧾"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤ᧿"), None)):
                    bstack11l111l1lll_opy_[bstack1ll_opy_ (u"ࠨࡴࡺࡲࡨࠦᨀ")] = TestFramework.bstack11ll11ll1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l111l1lll_opy_[bstack1ll_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᨁ")] = uuid4().__str__()
                bstack11l111l1lll_opy_[bstack1l1l1ll1l1l_opy_.bstack11l11111ll1_opy_] = bstack11l111l1l1l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l111l1lll_opy_[bstack1l1l1ll1l1l_opy_.bstack111lllll1ll_opy_] = bstack11l111l1l1l_opy_
            if bstack11l111l1111_opy_ in bstack111llllll11_opy_:
                bstack111llllll11_opy_[bstack11l111l1111_opy_].update(bstack11l111l1lll_opy_)
                self.logger.debug(bstack1ll_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᨂ") + str(bstack111llllll11_opy_[bstack11l111l1111_opy_]) + bstack1ll_opy_ (u"ࠤࠥᨃ"))
            else:
                bstack111llllll11_opy_[bstack11l111l1111_opy_] = bstack11l111l1lll_opy_
                self.logger.debug(bstack1ll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᨄ") + str(len(bstack111llllll11_opy_)) + bstack1ll_opy_ (u"ࠦࠧᨅ"))
        TestFramework.bstack1l1l1l1l_opy_(instance, bstack1l1l1ll1l1l_opy_.bstack111ll1l11l1_opy_, bstack111llllll11_opy_)
        self.logger.debug(bstack1ll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᨆ") + str(instance.ref()) + bstack1ll_opy_ (u"ࠨࠢᨇ"))
        return instance
    def __111ll1lll1l_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l11_opy_.create_context(target)
        ob = bstack1l1l11l11ll_opy_(ctx, self.bstack1l1l111111l_opy_, self.bstack1l11ll1ll1l_opy_, test_framework_state)
        TestFramework.bstack111lllllll1_opy_(ob, {
            TestFramework.bstack1l11111111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11ll_opy_: context.test_framework_version,
            TestFramework.bstack111ll11llll_opy_: [],
            bstack1l1l1ll1l1l_opy_.bstack111ll1l11l1_opy_: {},
            bstack1l1l1ll1l1l_opy_.bstack111lll111l1_opy_: {},
            bstack1l1l1ll1l1l_opy_.bstack111ll11l1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1l1l1l1l_opy_(ob, TestFramework.bstack111lll1ll1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1l1l1l1l_opy_(ob, TestFramework.bstack1l1111l11l1_opy_, context.platform_index)
        TestFramework.bstack1l111l11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᨈ") + str(TestFramework.bstack1l111l11l_opy_.keys()) + bstack1ll_opy_ (u"ࠣࠤᨉ"))
        return ob
    def bstack11ll11llll1_opy_(self, instance: bstack1l1l11l11ll_opy_, bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            bstack1l1l1ll1l1l_opy_.bstack111llll1l1l_opy_
            if bstack1l1ll1lll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1ll1l1l_opy_.bstack111ll1l1lll_opy_
        )
        hook = bstack1l1l1ll1l1l_opy_.bstack111lll1111l_opy_(instance, bstack11l11111111_opy_)
        entries = hook.get(TestFramework.bstack11l111l11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, []))
        return entries
    def bstack11ll1l1lll1_opy_(self, instance: bstack1l1l11l11ll_opy_, bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l11111111_opy_ = (
            bstack1l1l1ll1l1l_opy_.bstack111llll1l1l_opy_
            if bstack1l1ll1lll11_opy_[1] == TestHookState.PRE
            else bstack1l1l1ll1l1l_opy_.bstack111ll1l1lll_opy_
        )
        bstack1l1l1ll1l1l_opy_.bstack11l1111llll_opy_(instance, bstack11l11111111_opy_)
        TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, []).clear()
    def bstack111lll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᨊ")
        global _11ll11l1l11_opy_
        platform_index = os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᨋ")]
        bstack11ll11l1ll1_opy_ = os.path.join(bstack11ll11ll111_opy_, (bstack11lll111lll_opy_ + str(platform_index)), bstack111ll1111ll_opy_)
        if not os.path.exists(bstack11ll11l1ll1_opy_) or not os.path.isdir(bstack11ll11l1ll1_opy_):
            self.logger.debug(bstack1ll_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤᨌ").format(bstack11ll11l1ll1_opy_))
            return
        logs = hook.get(bstack1ll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᨍ"), [])
        with os.scandir(bstack11ll11l1ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll11l1l11_opy_:
                    self.logger.info(bstack1ll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᨎ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll_opy_ (u"ࠢࠣᨏ")
                    log_entry = bstack111l1111ll_opy_(
                        kind=bstack1ll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᨐ"),
                        message=bstack1ll_opy_ (u"ࠤࠥᨑ"),
                        level=bstack1ll_opy_ (u"ࠥࠦᨒ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1ll1111_opy_=entry.stat().st_size,
                        bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᨓ"),
                        bstack1ll11l1_opy_=os.path.abspath(entry.path),
                        bstack11l111l111l_opy_=hook.get(TestFramework.bstack111lllll111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll11l1l11_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᨔ")]
        bstack111lllll1l1_opy_ = os.path.join(bstack11ll11ll111_opy_, (bstack11lll111lll_opy_ + str(platform_index)), bstack111ll1111ll_opy_, bstack111ll111l11_opy_)
        if not os.path.exists(bstack111lllll1l1_opy_) or not os.path.isdir(bstack111lllll1l1_opy_):
            self.logger.info(bstack1ll_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᨕ").format(bstack111lllll1l1_opy_))
        else:
            self.logger.info(bstack1ll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᨖ").format(bstack111lllll1l1_opy_))
            with os.scandir(bstack111lllll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll11l1l11_opy_:
                        self.logger.info(bstack1ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᨗ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll_opy_ (u"ࠤᨘࠥ")
                        log_entry = bstack111l1111ll_opy_(
                            kind=bstack1ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᨙ"),
                            message=bstack1ll_opy_ (u"ࠦࠧᨚ"),
                            level=bstack1ll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᨛ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1ll1111_opy_=entry.stat().st_size,
                            bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ᨜"),
                            bstack1ll11l1_opy_=os.path.abspath(entry.path),
                            bstack11lll1l11l1_opy_=hook.get(TestFramework.bstack111lllll111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll11l1l11_opy_.add(abs_path)
        hook[bstack1ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ᨝")] = logs
    def bstack11lll1lll1_opy_(
        self,
        bstack111111l1l1_opy_: bstack1l1l11l11ll_opy_,
        entries: List[bstack111l1111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧ᨞"))
        req.platform_index = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l1111l11l1_opy_)
        req.client_worker_id = bstack1ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᨟").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack111111l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack111111l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack111111l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack11ll11l11ll_opy_)
            log_entry.uuid = entry.bstack11l111l111l_opy_
            log_entry.test_framework_state = bstack111111l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᨠ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll_opy_ (u"ࠦࠧᨡ")
            if entry.kind == bstack1ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᨢ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1ll1111_opy_
                log_entry.file_path = entry.bstack1ll11l1_opy_
        def bstack11ll1l111l1_opy_():
            bstack1l1111ll_opy_ = datetime.now()
            try:
                self.bstack1ll11ll11l_opy_.LogCreatedEvent(req)
                bstack111111l1l1_opy_.bstack1lll11ll11_opy_(bstack1ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᨣ"), datetime.now() - bstack1l1111ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᨤ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11ll1_opy_.enqueue(bstack11ll1l111l1_opy_)
    def __11l11111l11_opy_(self, instance) -> None:
        bstack1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᨥ")
        bstack111lll11111_opy_ = {bstack1ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᨦ"): bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        bstack1l11lll1lll_opy_.bstack111llll11l1_opy_()
    @staticmethod
    def bstack111lll1111l_opy_(instance: bstack1l1l11l11ll_opy_, bstack11l11111111_opy_: str):
        bstack111lll1l1ll_opy_ = (
            bstack1l1l1ll1l1l_opy_.bstack111lll111l1_opy_
            if bstack11l11111111_opy_ == bstack1l1l1ll1l1l_opy_.bstack111ll1l1lll_opy_
            else bstack1l1l1ll1l1l_opy_.bstack111ll11l1ll_opy_
        )
        bstack111ll1l1111_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack11l11111111_opy_, None)
        bstack111ll11ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll1l1ll_opy_, None) if bstack111ll1l1111_opy_ else None
        return (
            bstack111ll11ll11_opy_[bstack111ll1l1111_opy_][-1]
            if isinstance(bstack111ll11ll11_opy_, dict) and len(bstack111ll11ll11_opy_.get(bstack111ll1l1111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111llll_opy_(instance: bstack1l1l11l11ll_opy_, bstack11l11111111_opy_: str):
        hook = bstack1l1l1ll1l1l_opy_.bstack111lll1111l_opy_(instance, bstack11l11111111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l111l11ll_opy_, []).clear()
    @staticmethod
    def __111llll1lll_opy_(instance: bstack1l1l11l11ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᨧ"), None)):
            return
        if os.getenv(bstack1ll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᨨ"), bstack1ll_opy_ (u"ࠧ࠷ࠢᨩ")) != bstack1ll_opy_ (u"ࠨ࠱ࠣᨪ"):
            bstack1l1l1ll1l1l_opy_.logger.warning(bstack1ll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᨫ"))
            return
        bstack111lll11lll_opy_ = {
            bstack1ll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᨬ"): (bstack1l1l1ll1l1l_opy_.bstack111llll1l1l_opy_, bstack1l1l1ll1l1l_opy_.bstack111ll11l1ll_opy_),
            bstack1ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᨭ"): (bstack1l1l1ll1l1l_opy_.bstack111ll1l1lll_opy_, bstack1l1l1ll1l1l_opy_.bstack111lll111l1_opy_),
        }
        for when in (bstack1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᨮ"), bstack1ll_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᨯ"), bstack1ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᨰ")):
            bstack111ll1l111l_opy_ = args[1].get_records(when)
            if not bstack111ll1l111l_opy_:
                continue
            records = [
                bstack111l1111ll_opy_(
                    kind=TestFramework.bstack11ll11ll11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᨱ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᨲ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll1l111l_opy_
                if isinstance(getattr(r, bstack1ll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᨳ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111lll11l1l_opy_, bstack111lll1l1ll_opy_ = bstack111lll11lll_opy_.get(when, (None, None))
            bstack11l1111ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll11l1l_opy_, None) if bstack111lll11l1l_opy_ else None
            bstack111ll11ll11_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack111lll1l1ll_opy_, None) if bstack11l1111ll11_opy_ else None
            if isinstance(bstack111ll11ll11_opy_, dict) and len(bstack111ll11ll11_opy_.get(bstack11l1111ll11_opy_, [])) > 0:
                hook = bstack111ll11ll11_opy_[bstack11l1111ll11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l111l11ll_opy_ in hook:
                    hook[TestFramework.bstack11l111l11ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll1l111_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1l1ll1l1l_opy_.__11l11111lll_opy_(test.location) if hasattr(test, bstack1ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᨴ")) else getattr(test, bstack1ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᨵ"), None)
        test_name = test.name if hasattr(test, bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨶ")) else None
        bstack111llllll1l_opy_ = test.fspath.strpath if hasattr(test, bstack1ll_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᨷ")) and test.fspath else None
        if not test_id or not test_name or not bstack111llllll1l_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll_opy_ (u"ࠨ࡯ࡣ࡬ࠥᨸ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack111ll111l1l_opy_ = []
        try:
            bstack111ll111l1l_opy_ = bstack111l111ll1_opy_.bstack1lll11ll111_opy_(test)
        except:
            bstack1l1l1ll1l1l_opy_.logger.warning(bstack1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᨹ"))
        return {
            TestFramework.bstack1l1111ll1l1_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll11111_opy_: test_id,
            TestFramework.bstack1l111111lll_opy_: test_name,
            TestFramework.bstack11ll111l1ll_opy_: getattr(test, bstack1ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᨺ"), None),
            TestFramework.bstack111llllllll_opy_: bstack111llllll1l_opy_,
            TestFramework.bstack11l111l1l11_opy_: bstack1l1l1ll1l1l_opy_.__11l111l11l1_opy_(test),
            TestFramework.bstack111ll1ll1ll_opy_: code,
            TestFramework.bstack11l1ll11lll_opy_: TestFramework.bstack11l111ll111_opy_,
            TestFramework.bstack11l11l1l1ll_opy_: test_id,
            TestFramework.bstack111ll11l11l_opy_: bstack111ll111l1l_opy_
        }
    @staticmethod
    def __11l111l11l1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᨻ"), [])
            markers.extend([getattr(m, bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᨼ"), None) for m in own_markers if getattr(m, bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨽ"), None)])
            current = getattr(current, bstack1ll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᨾ"), None)
        return markers
    @staticmethod
    def __11l11111lll_opy_(location):
        return bstack1ll_opy_ (u"ࠨ࠺࠻ࠤᨿ").join(filter(lambda x: isinstance(x, str), location))