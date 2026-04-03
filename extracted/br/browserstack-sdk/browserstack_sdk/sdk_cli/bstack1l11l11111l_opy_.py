# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll11ll1l_opy_ import bstack1l1ll11l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l111111l1_opy_ import bstack111lllll111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l1ll1ll_opy_,
    TestHookState,
    bstack1lll11l111l_opy_,
    bstack111l1111l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11ll11ll11l_opy_
from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11l11_opy_ import bstack1l1lll11ll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll1ll1_opy_ import bstack1l1l111111l_opy_
from bstack_utils.bstack111ll111ll_opy_ import bstack11l1l1l1_opy_
bstack11ll11l1ll1_opy_ = bstack11ll11ll11l_opy_()
bstack111lll1ll1l_opy_ = 1.0
bstack11lll11111l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᦙ")
bstack111ll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᦚ")
bstack111ll11lll1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᦛ")
bstack111ll11l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᦜ")
bstack111ll11llll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᦝ")
_11ll1llllll_opy_ = set()
class bstack1l11ll1llll_opy_(TestFramework):
    bstack111lll11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᦞ")
    bstack11l111111ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᦟ")
    bstack111llll1111_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᦠ")
    bstack11l11111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᦡ")
    bstack111lllll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᦢ")
    bstack111llll1l11_opy_: bool
    bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_  = None
    bstack1llll11l11_opy_ = None
    bstack111lll1111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1l1l1l111_opy_: Dict[str, str],
        bstack1l111llllll_opy_: List[str]=[bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᦣ")],
        bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_=None,
        bstack1llll11l11_opy_=None
    ):
        super().__init__(bstack1l111llllll_opy_, bstack1l1l1l1l111_opy_, bstack1l1lll11l11_opy_)
        self.bstack111llll1l11_opy_ = any(bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᦤ") in item.lower() for item in bstack1l111llllll_opy_)
        self.bstack1llll11l11_opy_ = bstack1llll11l11_opy_
    def track_event(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l11ll1llll_opy_.bstack111lll1111l_opy_:
            bstack111lllll111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᦥ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠢࠣᦦ"))
            return
        if not self.bstack111llll1l11_opy_:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᦧ") + str(str(self.bstack1l111llllll_opy_)) + bstack1ll1l11_opy_ (u"ࠤࠥᦨ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᦩ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠦࠧᦪ"))
            return
        instance = self.__11l111ll11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᦫ") + str(args) + bstack1ll1l11_opy_ (u"ࠨࠢ᦬"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l11ll1llll_opy_.bstack111lll1111l_opy_:
                bstack1l111ll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࠣ᦭")
                name = bstack1ll1l11_opy_ (u"ࠣࠤ᦮")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l111ll1ll_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack111ll11l11l_opy_.value)
                    name = str(EVENTS.bstack111ll11l11l_opy_.name)+bstack1ll1l11_opy_ (u"ࠤ࠽ࠦ᦯")+str(test_framework_state.name)
                else:
                    bstack1l111ll1ll_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack111ll11l1l1_opy_.value)
                    name = str(EVENTS.bstack111ll11l1l1_opy_.name)+bstack1ll1l11_opy_ (u"ࠥ࠾ࠧᦰ")+str(test_framework_state.name)
                TestFramework.bstack111llll1ll1_opy_(instance, name, bstack1l111ll1ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᦱ").format(e))
        try:
            if not TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11l1ll1llll_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l11ll1llll_opy_.__111lll1l1l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᦲ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠨࠢᦳ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l1ll11_opy_):
                    TestFramework.bstack1ll11l1ll_opy_(instance, TestFramework.bstack11ll1l1ll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᦴ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠣࠤᦵ"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11lll1111ll_opy_):
                    TestFramework.bstack1ll11l1ll_opy_(instance, TestFramework.bstack11lll1111ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᦶ") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠥࠦᦷ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l11ll1llll_opy_.__11l1111l11l_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lllll11l_opy_(instance, *args)
                self.__111llll1lll_opy_(instance)
            elif test_framework_state in bstack1l11ll1llll_opy_.bstack111lll1111l_opy_:
                self.__111lll1l11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᦸ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠧࠨᦹ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111llllllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l11ll1llll_opy_.bstack111lll1111l_opy_:
                bstack1l111ll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠢᦺ")
                name = bstack1ll1l11_opy_ (u"ࠢࠣᦻ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll11l11l_opy_.name)+bstack1ll1l11_opy_ (u"ࠣ࠼ࠥᦼ")+str(test_framework_state.name)
                    bstack1l111ll1ll_opy_ = TestFramework.bstack111lllll1l1_opy_(instance, name)
                    bstack11l1111l1l_opy_.end(EVENTS.bstack111ll11l11l_opy_.value, bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᦽ"), bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᦾ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll11l1l1_opy_.name)+bstack1ll1l11_opy_ (u"ࠦ࠿ࠨᦿ")+str(test_framework_state.name)
                    bstack1l111ll1ll_opy_ = TestFramework.bstack111lllll1l1_opy_(instance, name)
                    bstack11l1111l1l_opy_.end(EVENTS.bstack111ll11l1l1_opy_.value, bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᧀ"), bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᧁ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᧂ").format(e))
    def bstack11ll1l11lll_opy_(self):
        return self.bstack111llll1l11_opy_
    def bstack11ll1lll1l1_opy_(self):
        return False
    def __111lll1llll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll1l11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᧃ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11ll1l1111l_opy_(rep, [bstack1ll1l11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᧄ"), bstack1ll1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᧅ"), bstack1ll1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᧆ"), bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᧇ"), bstack1ll1l11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᧈ"), bstack1ll1l11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᧉ")])
        return None
    def __111lllll11l_opy_(self, instance: bstack1l11l1ll1ll_opy_, *args):
        result = self.__111lll1llll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1lll_opy_ = None
        if result.get(bstack1ll1l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᧊"), None) == bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᧋") and len(args) > 1 and getattr(args[1], bstack1ll1l11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦ᧌"), None) is not None:
            failure = [{bstack1ll1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᧍"): [args[1].excinfo.exconly(), result.get(bstack1ll1l11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦ᧎"), None)]}]
            bstack1ll111l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᧏") if bstack1ll1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ᧐") in getattr(args[1].excinfo, bstack1ll1l11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥ᧑"), bstack1ll1l11_opy_ (u"ࠤࠥ᧒")) else bstack1ll1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ᧓")
        bstack11l1111l111_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᧔"), TestFramework.bstack11l111l11ll_opy_)
        if bstack11l1111l111_opy_ != TestFramework.bstack11l111l11ll_opy_:
            TestFramework.bstack1ll11l1ll_opy_(instance, TestFramework.bstack11ll1lll1ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l111lll1l_opy_(instance, {
            TestFramework.bstack11l1ll11l1l_opy_: failure,
            TestFramework.bstack111llllll1l_opy_: bstack1ll111l1lll_opy_,
            TestFramework.bstack11l1ll1ll11_opy_: bstack11l1111l111_opy_,
        })
    def __11l111ll11l_opy_(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111llllll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1lll111_opy_ bstack11l111ll1l1_opy_ this to be bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᧕")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111lll1l111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᧖"), None), bstack1ll1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᧗"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᧘"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll1l1l1l_opy_(target) if target else None
        return instance
    def __111lll1l11l_opy_(
        self,
        instance: bstack1l11l1ll1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l111l1ll1_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack1l11ll1llll_opy_.bstack11l111111ll_opy_, {})
        if not key in bstack11l111l1ll1_opy_:
            bstack11l111l1ll1_opy_[key] = []
        bstack111lll11lll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack1l11ll1llll_opy_.bstack111llll1111_opy_, {})
        if not key in bstack111lll11lll_opy_:
            bstack111lll11lll_opy_[key] = []
        bstack11l111lll11_opy_ = {
            bstack1l11ll1llll_opy_.bstack11l111111ll_opy_: bstack11l111l1ll1_opy_,
            bstack1l11ll1llll_opy_.bstack111llll1111_opy_: bstack111lll11lll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1ll1l11_opy_ (u"ࠤ࡮ࡩࡾࠨ᧙"): key,
                TestFramework.bstack111llll111l_opy_: uuid4().__str__(),
                TestFramework.bstack11l1111llll_opy_: TestFramework.bstack11l1111l1l1_opy_,
                TestFramework.bstack111ll1llll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll1l1lll_opy_: [],
                TestFramework.bstack111ll1l11l1_opy_: args[1] if len(args) > 1 else bstack1ll1l11_opy_ (u"ࠪࠫ᧚"),
                TestFramework.bstack11l1111111l_opy_: bstack1l1l111111l_opy_.bstack111lll1ll11_opy_()
            }
            bstack11l111l1ll1_opy_[key].append(hook)
            bstack11l111lll11_opy_[bstack1l11ll1llll_opy_.bstack11l11111l1l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l11111ll1_opy_ = bstack11l111l1ll1_opy_.get(key, [])
            hook = bstack11l11111ll1_opy_.pop() if bstack11l11111ll1_opy_ else None
            if hook:
                result = self.__111lll1llll_opy_(*args)
                if result:
                    bstack11l111l11l1_opy_ = result.get(bstack1ll1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᧛"), TestFramework.bstack11l1111l1l1_opy_)
                    if bstack11l111l11l1_opy_ != TestFramework.bstack11l1111l1l1_opy_:
                        hook[TestFramework.bstack11l1111llll_opy_] = bstack11l111l11l1_opy_
                hook[TestFramework.bstack111llll11ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l1111111l_opy_]= bstack1l1l111111l_opy_.bstack111lll1ll11_opy_()
                self.bstack111lll11l11_opy_(hook)
                logs = hook.get(TestFramework.bstack111lll111l1_opy_, [])
                if logs: self.bstack1l1ll1lll_opy_(instance, logs)
                bstack111lll11lll_opy_[key].append(hook)
                bstack11l111lll11_opy_[bstack1l11ll1llll_opy_.bstack111lllll1ll_opy_] = key
        TestFramework.bstack11l111lll1l_opy_(instance, bstack11l111lll11_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦ᧜") + str(bstack111lll11lll_opy_) + bstack1ll1l11_opy_ (u"ࠨࠢ᧝"))
    def __111llllll11_opy_(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11ll1l1111l_opy_(args[0], [bstack1ll1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᧞"), bstack1ll1l11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤ᧟"), bstack1ll1l11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤ᧠"), bstack1ll1l11_opy_ (u"ࠥ࡭ࡩࡹࠢ᧡"), bstack1ll1l11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨ᧢"), bstack1ll1l11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧ᧣")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1ll1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ᧤")) else fixturedef.get(bstack1ll1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᧥"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll1l11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨ᧦")) else None
        node = request.node if hasattr(request, bstack1ll1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ᧧")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll1l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᧨")) else None
        baseid = fixturedef.get(bstack1ll1l11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦ᧩"), None) or bstack1ll1l11_opy_ (u"ࠧࠨ᧪")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll1l11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦ᧫")):
            target = bstack1l11ll1llll_opy_.__11l111111l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll1l11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤ᧬")) else None
            if target and not TestFramework.bstack1l1ll1l1l1l_opy_(target):
                self.__111lll1l111_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ᧭") + str(test_hook_state) + bstack1ll1l11_opy_ (u"ࠤࠥ᧮"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣ᧯") + str(target) + bstack1ll1l11_opy_ (u"ࠦࠧ᧰"))
            return None
        instance = TestFramework.bstack1l1ll1l1l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢ᧱") + str(target) + bstack1ll1l11_opy_ (u"ࠨࠢ᧲"))
            return None
        bstack111ll1l1ll1_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack1l11ll1llll_opy_.bstack111lll11l1l_opy_, {})
        if os.getenv(bstack1ll1l11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣ᧳"), bstack1ll1l11_opy_ (u"ࠣ࠳ࠥ᧴")) == bstack1ll1l11_opy_ (u"ࠤ࠴ࠦ᧵"):
            bstack111ll1lllll_opy_ = bstack1ll1l11_opy_ (u"ࠥ࠾ࠧ᧶").join((scope, fixturename))
            bstack111ll1lll11_opy_ = datetime.now(tz=timezone.utc)
            bstack11l11111l11_opy_ = {
                bstack1ll1l11_opy_ (u"ࠦࡰ࡫ࡹࠣ᧷"): bstack111ll1lllll_opy_,
                bstack1ll1l11_opy_ (u"ࠧࡺࡡࡨࡵࠥ᧸"): bstack1l11ll1llll_opy_.__111ll1ll11l_opy_(request.node),
                bstack1ll1l11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢ᧹"): fixturedef,
                bstack1ll1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᧺"): scope,
                bstack1ll1l11_opy_ (u"ࠣࡶࡼࡴࡪࠨ᧻"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1ll1l11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨ᧼"), None)):
                    bstack11l11111l11_opy_[bstack1ll1l11_opy_ (u"ࠥࡸࡾࡶࡥࠣ᧽")] = TestFramework.bstack11ll1ll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11l11111l11_opy_[bstack1ll1l11_opy_ (u"ࠦࡺࡻࡩࡥࠤ᧾")] = uuid4().__str__()
                bstack11l11111l11_opy_[bstack1l11ll1llll_opy_.bstack111ll1llll1_opy_] = bstack111ll1lll11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l11111l11_opy_[bstack1l11ll1llll_opy_.bstack111llll11ll_opy_] = bstack111ll1lll11_opy_
            if bstack111ll1lllll_opy_ in bstack111ll1l1ll1_opy_:
                bstack111ll1l1ll1_opy_[bstack111ll1lllll_opy_].update(bstack11l11111l11_opy_)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨ᧿") + str(bstack111ll1l1ll1_opy_[bstack111ll1lllll_opy_]) + bstack1ll1l11_opy_ (u"ࠨࠢᨀ"))
            else:
                bstack111ll1l1ll1_opy_[bstack111ll1lllll_opy_] = bstack11l11111l11_opy_
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᨁ") + str(len(bstack111ll1l1ll1_opy_)) + bstack1ll1l11_opy_ (u"ࠣࠤᨂ"))
        TestFramework.bstack1ll11l1ll_opy_(instance, bstack1l11ll1llll_opy_.bstack111lll11l1l_opy_, bstack111ll1l1ll1_opy_)
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᨃ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠥࠦᨄ"))
        return instance
    def __111lll1l111_opy_(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll11l1l1_opy_.create_context(target)
        ob = bstack1l11l1ll1ll_opy_(ctx, self.bstack1l111llllll_opy_, self.bstack1l1l1l1l111_opy_, test_framework_state)
        TestFramework.bstack11l111lll1l_opy_(ob, {
            TestFramework.bstack11llllll1l1_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11l1_opy_: context.test_framework_version,
            TestFramework.bstack111llll1l1l_opy_: [],
            bstack1l11ll1llll_opy_.bstack111lll11l1l_opy_: {},
            bstack1l11ll1llll_opy_.bstack111llll1111_opy_: {},
            bstack1l11ll1llll_opy_.bstack11l111111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll11l1ll_opy_(ob, TestFramework.bstack111ll1l1l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll11l1ll_opy_(ob, TestFramework.bstack1l111ll1l1l_opy_, context.platform_index)
        TestFramework.bstack11l111111_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᨅ") + str(TestFramework.bstack11l111111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠧࠨᨆ"))
        return ob
    def bstack11ll1l1l1ll_opy_(self, instance: bstack1l11l1ll1ll_opy_, bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l111l1111_opy_ = (
            bstack1l11ll1llll_opy_.bstack11l11111l1l_opy_
            if bstack1l1ll1ll1ll_opy_[1] == TestHookState.PRE
            else bstack1l11ll1llll_opy_.bstack111lllll1ll_opy_
        )
        hook = bstack1l11ll1llll_opy_.bstack11l1111lll1_opy_(instance, bstack11l111l1111_opy_)
        entries = hook.get(TestFramework.bstack111ll1l1lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack111llll1l1l_opy_, []))
        return entries
    def bstack11lll11ll1l_opy_(self, instance: bstack1l11l1ll1ll_opy_, bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l111l1111_opy_ = (
            bstack1l11ll1llll_opy_.bstack11l11111l1l_opy_
            if bstack1l1ll1ll1ll_opy_[1] == TestHookState.PRE
            else bstack1l11ll1llll_opy_.bstack111lllll1ll_opy_
        )
        bstack1l11ll1llll_opy_.bstack11l11111lll_opy_(instance, bstack11l111l1111_opy_)
        TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack111llll1l1l_opy_, []).clear()
    def bstack111lll11l11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᨇ")
        global _11ll1llllll_opy_
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᨈ")]
        bstack11ll11l1l11_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11lll11111l_opy_ + str(platform_index)), bstack111ll11l1ll_opy_)
        if not os.path.exists(bstack11ll11l1l11_opy_) or not os.path.isdir(bstack11ll11l1l11_opy_):
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᨉ").format(bstack11ll11l1l11_opy_))
            return
        logs = hook.get(bstack1ll1l11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᨊ"), [])
        with os.scandir(bstack11ll11l1l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1llllll_opy_:
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᨋ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll1l11_opy_ (u"ࠦࠧᨌ")
                    log_entry = bstack111l1111l_opy_(
                        kind=bstack1ll1l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᨍ"),
                        message=bstack1ll1l11_opy_ (u"ࠨࠢᨎ"),
                        level=bstack1ll1l11_opy_ (u"ࠢࠣᨏ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11lll1l111l_opy_=entry.stat().st_size,
                        bstack11ll1l1l1l1_opy_=bstack1ll1l11_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᨐ"),
                        bstack11ll_opy_=os.path.abspath(entry.path),
                        bstack11l111l1l11_opy_=hook.get(TestFramework.bstack111llll111l_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1llllll_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᨑ")]
        bstack11l111l1l1l_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11lll11111l_opy_ + str(platform_index)), bstack111ll11l1ll_opy_, bstack111ll11llll_opy_)
        if not os.path.exists(bstack11l111l1l1l_opy_) or not os.path.isdir(bstack11l111l1l1l_opy_):
            self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᨒ").format(bstack11l111l1l1l_opy_))
        else:
            self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᨓ").format(bstack11l111l1l1l_opy_))
            with os.scandir(bstack11l111l1l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1llllll_opy_:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᨔ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll1l11_opy_ (u"ࠨࠢᨕ")
                        log_entry = bstack111l1111l_opy_(
                            kind=bstack1ll1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᨖ"),
                            message=bstack1ll1l11_opy_ (u"ࠣࠤᨗ"),
                            level=bstack1ll1l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᨘ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11lll1l111l_opy_=entry.stat().st_size,
                            bstack11ll1l1l1l1_opy_=bstack1ll1l11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᨙ"),
                            bstack11ll_opy_=os.path.abspath(entry.path),
                            bstack11ll1ll1l1l_opy_=hook.get(TestFramework.bstack111llll111l_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1llllll_opy_.add(abs_path)
        hook[bstack1ll1l11_opy_ (u"ࠦࡱࡵࡧࡴࠤᨚ")] = logs
    def bstack1l1ll1lll_opy_(
        self,
        bstack1l11lll11l_opy_: bstack1l11l1ll1ll_opy_,
        entries: List[bstack111l1111l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᨛ"))
        req.platform_index = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack1l111ll1l1l_opy_)
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᨜").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11lll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11lll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11lll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11llllll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11ll11l11l1_opy_)
            log_entry.uuid = entry.bstack11l111l1l11_opy_
            log_entry.test_framework_state = bstack1l11lll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᨝"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1ll1l11_opy_ (u"ࠣࠤ᨞")
            if entry.kind == bstack1ll1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᨟"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lll1l111l_opy_
                log_entry.file_path = entry.bstack11ll_opy_
        def bstack11ll1lll11l_opy_():
            bstack1l1l11llll_opy_ = datetime.now()
            try:
                self.bstack1llll11l11_opy_.LogCreatedEvent(req)
                bstack1l11lll11l_opy_.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᨠ"), datetime.now() - bstack1l1l11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᨡ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l11_opy_.enqueue(bstack11ll1lll11l_opy_)
    def __111llll1lll_opy_(self, instance) -> None:
        bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᨢ")
        bstack11l111lll11_opy_ = {bstack1ll1l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᨣ"): bstack1l1l111111l_opy_.bstack111lll1ll11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l111lll1l_opy_(instance, bstack11l111lll11_opy_)
    @staticmethod
    def bstack11l1111lll1_opy_(instance: bstack1l11l1ll1ll_opy_, bstack11l111l1111_opy_: str):
        bstack111lllllll1_opy_ = (
            bstack1l11ll1llll_opy_.bstack111llll1111_opy_
            if bstack11l111l1111_opy_ == bstack1l11ll1llll_opy_.bstack111lllll1ll_opy_
            else bstack1l11ll1llll_opy_.bstack11l111111ll_opy_
        )
        bstack11l111ll1ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack11l111l1111_opy_, None)
        bstack111ll1l11ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack111lllllll1_opy_, None) if bstack11l111ll1ll_opy_ else None
        return (
            bstack111ll1l11ll_opy_[bstack11l111ll1ll_opy_][-1]
            if isinstance(bstack111ll1l11ll_opy_, dict) and len(bstack111ll1l11ll_opy_.get(bstack11l111ll1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l11111lll_opy_(instance: bstack1l11l1ll1ll_opy_, bstack11l111l1111_opy_: str):
        hook = bstack1l11ll1llll_opy_.bstack11l1111lll1_opy_(instance, bstack11l111l1111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll1l1lll_opy_, []).clear()
    @staticmethod
    def __11l1111l11l_opy_(instance: bstack1l11l1ll1ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll1l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᨤ"), None)):
            return
        if os.getenv(bstack1ll1l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᨥ"), bstack1ll1l11_opy_ (u"ࠤ࠴ࠦᨦ")) != bstack1ll1l11_opy_ (u"ࠥ࠵ࠧᨧ"):
            bstack1l11ll1llll_opy_.logger.warning(bstack1ll1l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᨨ"))
            return
        bstack111llll11l1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᨩ"): (bstack1l11ll1llll_opy_.bstack11l11111l1l_opy_, bstack1l11ll1llll_opy_.bstack11l111111ll_opy_),
            bstack1ll1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᨪ"): (bstack1l11ll1llll_opy_.bstack111lllll1ll_opy_, bstack1l11ll1llll_opy_.bstack111llll1111_opy_),
        }
        for when in (bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᨫ"), bstack1ll1l11_opy_ (u"ࠣࡥࡤࡰࡱࠨᨬ"), bstack1ll1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᨭ")):
            bstack111ll1l1l1l_opy_ = args[1].get_records(when)
            if not bstack111ll1l1l1l_opy_:
                continue
            records = [
                bstack111l1111l_opy_(
                    kind=TestFramework.bstack11lll11l111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll1l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᨮ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll1l11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᨯ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll1l1l1l_opy_
                if isinstance(getattr(r, bstack1ll1l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᨰ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111lll1lll1_opy_, bstack111lllllll1_opy_ = bstack111llll11l1_opy_.get(when, (None, None))
            bstack111ll1ll1ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack111lll1lll1_opy_, None) if bstack111lll1lll1_opy_ else None
            bstack111ll1l11ll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, bstack111lllllll1_opy_, None) if bstack111ll1ll1ll_opy_ else None
            if isinstance(bstack111ll1l11ll_opy_, dict) and len(bstack111ll1l11ll_opy_.get(bstack111ll1ll1ll_opy_, [])) > 0:
                hook = bstack111ll1l11ll_opy_[bstack111ll1ll1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll1l1lll_opy_ in hook:
                    hook[TestFramework.bstack111ll1l1lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack111llll1l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll1l1l1_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l11ll1llll_opy_.__11l111111l1_opy_(test.location) if hasattr(test, bstack1ll1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᨱ")) else getattr(test, bstack1ll1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᨲ"), None)
        test_name = test.name if hasattr(test, bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᨳ")) else None
        bstack111lll1l1ll_opy_ = test.fspath.strpath if hasattr(test, bstack1ll1l11_opy_ (u"ࠤࡩࡷࡵࡧࡴࡩࠤᨴ")) and test.fspath else None
        if not test_id or not test_name or not bstack111lll1l1ll_opy_:
            return None
        code = None
        if hasattr(test, bstack1ll1l11_opy_ (u"ࠥࡳࡧࡰࠢᨵ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack111ll11ll1l_opy_ = []
        try:
            bstack111ll11ll1l_opy_ = bstack11l1l1l1_opy_.bstack1lll1ll11l1_opy_(test)
        except:
            bstack1l11ll1llll_opy_.logger.warning(bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵ࠯ࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡪࡹ࡯࡭ࡸࡨࡨࠥ࡯࡮ࠡࡅࡏࡍࠧᨶ"))
        return {
            TestFramework.bstack1l111l1lll1_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll1llll_opy_: test_id,
            TestFramework.bstack1l111ll11l1_opy_: test_name,
            TestFramework.bstack11ll111ll11_opy_: getattr(test, bstack1ll1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᨷ"), None),
            TestFramework.bstack11l1111ll11_opy_: bstack111lll1l1ll_opy_,
            TestFramework.bstack111ll1l111l_opy_: bstack1l11ll1llll_opy_.__111ll1ll11l_opy_(test),
            TestFramework.bstack111lll11111_opy_: code,
            TestFramework.bstack11l1ll1ll11_opy_: TestFramework.bstack11l111l11ll_opy_,
            TestFramework.bstack11l11l1l11l_opy_: test_id,
            TestFramework.bstack111ll1l1111_opy_: bstack111ll11ll1l_opy_
        }
    @staticmethod
    def __111ll1ll11l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1ll1l11_opy_ (u"ࠨ࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠦᨸ"), [])
            markers.extend([getattr(m, bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨹ"), None) for m in own_markers if getattr(m, bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᨺ"), None)])
            current = getattr(current, bstack1ll1l11_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᨻ"), None)
        return markers
    @staticmethod
    def __11l111111l1_opy_(location):
        return bstack1ll1l11_opy_ (u"ࠥ࠾࠿ࠨᨼ").join(filter(lambda x: isinstance(x, str), location))