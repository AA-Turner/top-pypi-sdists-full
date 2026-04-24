# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1l1ll1l1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11lll1_opy_ import bstack111lll1111l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l111llll11_opy_,
    TestHookState,
    bstack1lll111l1l1_opy_,
    bstack1llll111ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11ll1lll1ll_opy_
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11lllllll_opy_ import bstack1l1l111111l_opy_
from bstack_utils.bstack11lll111_opy_ import bstack1lll1l11l_opy_
bstack11ll11ll1l1_opy_ = bstack11ll1lll1ll_opy_()
bstack111lllll1l1_opy_ = 1.0
bstack11lll1l1111_opy_ = bstack111ll11_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᦵ")
bstack111ll111lll_opy_ = bstack111ll11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᦶ")
bstack111ll1111ll_opy_ = bstack111ll11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᦷ")
bstack111ll111l1l_opy_ = bstack111ll11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᦸ")
bstack111ll1111l1_opy_ = bstack111ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᦹ")
_11ll1l11111_opy_ = set()
class bstack1l11l1l1111_opy_(TestFramework):
    bstack111lll11111_opy_ = bstack111ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᦺ")
    bstack111ll1ll111_opy_ = bstack111ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᦻ")
    bstack11l111111l1_opy_ = bstack111ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᦼ")
    bstack111ll1llll1_opy_ = bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᦽ")
    bstack111lll1l1l1_opy_ = bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᦾ")
    bstack111llllllll_opy_: bool
    bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_  = None
    bstack1l1l1l1l1l_opy_ = None
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1111l_opy_: Dict[str, str],
        bstack1l11lll1ll1_opy_: List[str]=[bstack111ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᦿ")],
        bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_=None,
        bstack1l1l1l1l1l_opy_=None
    ):
        super().__init__(bstack1l11lll1ll1_opy_, bstack1l11ll1111l_opy_, bstack1l1lll11l1l_opy_)
        self.bstack111llllllll_opy_ = any(bstack111ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᧀ") in item.lower() for item in bstack1l11lll1ll1_opy_)
        self.bstack1l1l1l1l1l_opy_ = bstack1l1l1l1l1l_opy_
    def track_event(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l11l1l1111_opy_.bstack111ll1l1l1l_opy_:
            bstack111lll1111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111ll11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᧁ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠢࠣᧂ"))
            return
        if not self.bstack111llllllll_opy_:
            self.logger.warning(bstack111ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᧃ") + str(str(self.bstack1l11lll1ll1_opy_)) + bstack111ll11_opy_ (u"ࠤࠥᧄ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᧅ") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧᧆ"))
            return
        instance = self.__111lll1l11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᧇ") + str(args) + bstack111ll11_opy_ (u"ࠨࠢᧈ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l11l1l1111_opy_.bstack111ll1l1l1l_opy_:
                bstack11111l11ll_opy_ = bstack111ll11_opy_ (u"ࠢࠣᧉ")
                name = bstack111ll11_opy_ (u"ࠣࠤ᧊")
                if (test_hook_state == TestHookState.PRE):
                    bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack111ll11l111_opy_.value)
                    name = str(EVENTS.bstack111ll11l111_opy_.name)+bstack111ll11_opy_ (u"ࠤ࠽ࠦ᧋")+str(test_framework_state.name)
                else:
                    bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack111ll111l11_opy_.value)
                    name = str(EVENTS.bstack111ll111l11_opy_.name)+bstack111ll11_opy_ (u"ࠥ࠾ࠧ᧌")+str(test_framework_state.name)
                TestFramework.bstack11l1111ll11_opy_(instance, name, bstack11111l11ll_opy_)
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣ᧍").format(e))
        try:
            if not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11l1l1l1l1l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l11l1l1111_opy_.__111lll1lll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111ll11_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ᧎") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠨࠢ᧏"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11ll1l111l1_opy_):
                    TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11ll1l111l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ᧐") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠣࠤ᧑"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11ll1l11l11_opy_):
                    TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11ll1l11l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll11_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ᧒") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠥࠦ᧓"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l11l1l1111_opy_.__111llll111l_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111ll11lll1_opy_(instance, *args)
                self.__111llll1l11_opy_(instance)
            elif test_framework_state in bstack1l11l1l1111_opy_.bstack111ll1l1l1l_opy_:
                self.__11l111l111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ᧔") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠧࠨ᧕"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1111llll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l11l1l1111_opy_.bstack111ll1l1l1l_opy_:
                bstack11111l11ll_opy_ = bstack111ll11_opy_ (u"ࠨࠢ᧖")
                name = bstack111ll11_opy_ (u"ࠢࠣ᧗")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll11l111_opy_.name)+bstack111ll11_opy_ (u"ࠣ࠼ࠥ᧘")+str(test_framework_state.name)
                    bstack11111l11ll_opy_ = TestFramework.bstack111ll1l1111_opy_(instance, name)
                    bstack1ll1l11l1_opy_.end(EVENTS.bstack111ll11l111_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᧙"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᧚"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll111l11_opy_.name)+bstack111ll11_opy_ (u"ࠦ࠿ࠨ᧛")+str(test_framework_state.name)
                    bstack11111l11ll_opy_ = TestFramework.bstack111ll1l1111_opy_(instance, name)
                    bstack1ll1l11l1_opy_.end(EVENTS.bstack111ll111l11_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᧜"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᧝"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ᧞").format(e))
    def bstack11ll1lll111_opy_(self):
        return self.bstack111llllllll_opy_
    def bstack11ll111llll_opy_(self):
        return False
    def __111ll1ll1l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111ll11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧ᧟"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11ll11ll11l_opy_(rep, [bstack111ll11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ᧠"), bstack111ll11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᧡"), bstack111ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ᧢"), bstack111ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᧣"), bstack111ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢ᧤"), bstack111ll11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ᧥")])
        return None
    def __111ll11lll1_opy_(self, instance: bstack1l111llll11_opy_, *args):
        result = self.__111ll1ll1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        if result.get(bstack111ll11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᧦"), None) == bstack111ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᧧") and len(args) > 1 and getattr(args[1], bstack111ll11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦ᧨"), None) is not None:
            failure = [{bstack111ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᧩"): [args[1].excinfo.exconly(), result.get(bstack111ll11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦ᧪"), None)]}]
            bstack1ll111l1l1l_opy_ = bstack111ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᧫") if bstack111ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ᧬") in getattr(args[1].excinfo, bstack111ll11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥ᧭"), bstack111ll11_opy_ (u"ࠤࠥ᧮")) else bstack111ll11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ᧯")
        bstack111ll11ll1l_opy_ = result.get(bstack111ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᧰"), TestFramework.bstack111ll11llll_opy_)
        if bstack111ll11ll1l_opy_ != TestFramework.bstack111ll11llll_opy_:
            TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11lll1l11l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l111l11ll_opy_(instance, {
            TestFramework.bstack11l1ll111ll_opy_: failure,
            TestFramework.bstack111lll1llll_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack11l1ll11111_opy_: bstack111ll11ll1l_opy_,
        })
    def __111lll1l11l_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111llllll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll11l111l_opy_ bstack111lll1l111_opy_ this to be bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᧱")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111lll1ll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack111ll11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᧲"), None), bstack111ll11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᧳"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᧴"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll111l11_opy_(target) if target else None
        return instance
    def __11l111l111l_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l11111l1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack1l11l1l1111_opy_.bstack111ll1ll111_opy_, {})
        if not key in bstack11l11111l1l_opy_:
            bstack11l11111l1l_opy_[key] = []
        bstack111ll1lll1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack1l11l1l1111_opy_.bstack11l111111l1_opy_, {})
        if not key in bstack111ll1lll1l_opy_:
            bstack111ll1lll1l_opy_[key] = []
        bstack111lll1ll1l_opy_ = {
            bstack1l11l1l1111_opy_.bstack111ll1ll111_opy_: bstack11l11111l1l_opy_,
            bstack1l11l1l1111_opy_.bstack11l111111l1_opy_: bstack111ll1lll1l_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack111ll11_opy_ (u"ࠤ࡮ࡩࡾࠨ᧵"): key,
                TestFramework.bstack11l11111l11_opy_: uuid4().__str__(),
                TestFramework.bstack111lll11ll1_opy_: TestFramework.bstack111ll11l1ll_opy_,
                TestFramework.bstack111ll1l1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l1111_opy_: [],
                TestFramework.bstack11l11111ll1_opy_: args[1] if len(args) > 1 else bstack111ll11_opy_ (u"ࠪࠫ᧶"),
                TestFramework.bstack111ll1ll11l_opy_: bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()
            }
            bstack11l11111l1l_opy_[key].append(hook)
            bstack111lll1ll1l_opy_[bstack1l11l1l1111_opy_.bstack111ll1llll1_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llllll1l_opy_ = bstack11l11111l1l_opy_.get(key, [])
            hook = bstack111llllll1l_opy_.pop() if bstack111llllll1l_opy_ else None
            if hook:
                result = self.__111ll1ll1l1_opy_(*args)
                if result:
                    bstack11l111111ll_opy_ = result.get(bstack111ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᧷"), TestFramework.bstack111ll11l1ll_opy_)
                    if bstack11l111111ll_opy_ != TestFramework.bstack111ll11l1ll_opy_:
                        hook[TestFramework.bstack111lll11ll1_opy_] = bstack11l111111ll_opy_
                hook[TestFramework.bstack111llll1lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111ll1ll11l_opy_]= bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()
                self.bstack111llll11ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll1lll11_opy_, [])
                if logs: self.bstack11l1ll11_opy_(instance, logs)
                bstack111ll1lll1l_opy_[key].append(hook)
                bstack111lll1ll1l_opy_[bstack1l11l1l1111_opy_.bstack111lll1l1l1_opy_] = key
        TestFramework.bstack11l111l11ll_opy_(instance, bstack111lll1ll1l_opy_)
        self.logger.debug(bstack111ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦ᧸") + str(bstack111ll1lll1l_opy_) + bstack111ll11_opy_ (u"ࠨࠢ᧹"))
    def __111llllll11_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11ll11ll11l_opy_(args[0], [bstack111ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᧺"), bstack111ll11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤ᧻"), bstack111ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤ᧼"), bstack111ll11_opy_ (u"ࠥ࡭ࡩࡹࠢ᧽"), bstack111ll11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨ᧾"), bstack111ll11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧ᧿")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack111ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᨀ")) else fixturedef.get(bstack111ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᨁ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111ll11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᨂ")) else None
        node = request.node if hasattr(request, bstack111ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᨃ")) else None
        target = request.node.nodeid if hasattr(node, bstack111ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᨄ")) else None
        baseid = fixturedef.get(bstack111ll11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᨅ"), None) or bstack111ll11_opy_ (u"ࠧࠨᨆ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111ll11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᨇ")):
            target = bstack1l11l1l1111_opy_.__11l1111lll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111ll11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᨈ")) else None
            if target and not TestFramework.bstack1l1ll111l11_opy_(target):
                self.__111lll1ll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᨉ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠤࠥᨊ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᨋ") + str(target) + bstack111ll11_opy_ (u"ࠦࠧᨌ"))
            return None
        instance = TestFramework.bstack1l1ll111l11_opy_(target)
        if not instance:
            self.logger.warning(bstack111ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᨍ") + str(target) + bstack111ll11_opy_ (u"ࠨࠢᨎ"))
            return None
        bstack111lll111l1_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack1l11l1l1111_opy_.bstack111lll11111_opy_, {})
        if os.getenv(bstack111ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᨏ"), bstack111ll11_opy_ (u"ࠣ࠳ࠥᨐ")) == bstack111ll11_opy_ (u"ࠤ࠴ࠦᨑ"):
            bstack11l1111l11l_opy_ = bstack111ll11_opy_ (u"ࠥ࠾ࠧᨒ").join((scope, fixturename))
            bstack111ll11l11l_opy_ = datetime.now(tz=timezone.utc)
            bstack111llll11l1_opy_ = {
                bstack111ll11_opy_ (u"ࠦࡰ࡫ࡹࠣᨓ"): bstack11l1111l11l_opy_,
                bstack111ll11_opy_ (u"ࠧࡺࡡࡨࡵࠥᨔ"): bstack1l11l1l1111_opy_.__111lll1l1ll_opy_(request.node),
                bstack111ll11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᨕ"): fixturedef,
                bstack111ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᨖ"): scope,
                bstack111ll11_opy_ (u"ࠣࡶࡼࡴࡪࠨᨗ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack111ll11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᨘ"), None)):
                    bstack111llll11l1_opy_[bstack111ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣᨙ")] = TestFramework.bstack11ll11lllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111llll11l1_opy_[bstack111ll11_opy_ (u"ࠦࡺࡻࡩࡥࠤᨚ")] = uuid4().__str__()
                bstack111llll11l1_opy_[bstack1l11l1l1111_opy_.bstack111ll1l1ll1_opy_] = bstack111ll11l11l_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111llll11l1_opy_[bstack1l11l1l1111_opy_.bstack111llll1lll_opy_] = bstack111ll11l11l_opy_
            if bstack11l1111l11l_opy_ in bstack111lll111l1_opy_:
                bstack111lll111l1_opy_[bstack11l1111l11l_opy_].update(bstack111llll11l1_opy_)
                self.logger.debug(bstack111ll11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᨛ") + str(bstack111lll111l1_opy_[bstack11l1111l11l_opy_]) + bstack111ll11_opy_ (u"ࠨࠢ᨜"))
            else:
                bstack111lll111l1_opy_[bstack11l1111l11l_opy_] = bstack111llll11l1_opy_
                self.logger.debug(bstack111ll11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥ᨝") + str(len(bstack111lll111l1_opy_)) + bstack111ll11_opy_ (u"ࠣࠤ᨞"))
        TestFramework.bstack11l1ll11ll_opy_(instance, bstack1l11l1l1111_opy_.bstack111lll11111_opy_, bstack111lll111l1_opy_)
        self.logger.debug(bstack111ll11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᨟") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠥࠦᨠ"))
        return instance
    def __111lll1ll11_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        ob = bstack1l111llll11_opy_(ctx, self.bstack1l11lll1ll1_opy_, self.bstack1l11ll1111l_opy_, test_framework_state)
        TestFramework.bstack11l111l11ll_opy_(ob, {
            TestFramework.bstack1l111ll11ll_opy_: context.test_framework_name,
            TestFramework.bstack11lll11111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1111ll1l_opy_: [],
            bstack1l11l1l1111_opy_.bstack111lll11111_opy_: {},
            bstack1l11l1l1111_opy_.bstack11l111111l1_opy_: {},
            bstack1l11l1l1111_opy_.bstack111ll1ll111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11l1ll11ll_opy_(ob, TestFramework.bstack111ll1l11ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11l1ll11ll_opy_(ob, TestFramework.bstack11llllll1ll_opy_, context.platform_index)
        TestFramework.bstack1111l11ll_opy_[ctx.id] = ob
        self.logger.debug(bstack111ll11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᨡ") + str(TestFramework.bstack1111l11ll_opy_.keys()) + bstack111ll11_opy_ (u"ࠧࠨᨢ"))
        return ob
    def bstack11ll1ll11l1_opy_(self, instance: bstack1l111llll11_opy_, bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            bstack1l11l1l1111_opy_.bstack111ll1llll1_opy_
            if bstack1l1ll11l11l_opy_[1] == TestHookState.PRE
            else bstack1l11l1l1111_opy_.bstack111lll1l1l1_opy_
        )
        hook = bstack1l11l1l1111_opy_.bstack111llll1111_opy_(instance, bstack111lll11l11_opy_)
        entries = hook.get(TestFramework.bstack11l111l1111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, []))
        return entries
    def bstack11lll1l111l_opy_(self, instance: bstack1l111llll11_opy_, bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            bstack1l11l1l1111_opy_.bstack111ll1llll1_opy_
            if bstack1l1ll11l11l_opy_[1] == TestHookState.PRE
            else bstack1l11l1l1111_opy_.bstack111lll1l1l1_opy_
        )
        bstack1l11l1l1111_opy_.bstack11l1111111l_opy_(instance, bstack111lll11l11_opy_)
        TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, []).clear()
    def bstack111llll11ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᨣ")
        global _11ll1l11111_opy_
        platform_index = os.environ[bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᨤ")]
        bstack11lll11l1ll_opy_ = os.path.join(bstack11ll11ll1l1_opy_, (bstack11lll1l1111_opy_ + str(platform_index)), bstack111ll111l1l_opy_)
        if not os.path.exists(bstack11lll11l1ll_opy_) or not os.path.isdir(bstack11lll11l1ll_opy_):
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᨥ").format(bstack11lll11l1ll_opy_))
            return
        logs = hook.get(bstack111ll11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᨦ"), [])
        with os.scandir(bstack11lll11l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1l11111_opy_:
                    self.logger.info(bstack111ll11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᨧ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111ll11_opy_ (u"ࠦࠧᨨ")
                    log_entry = bstack1llll111ll_opy_(
                        kind=bstack111ll11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᨩ"),
                        message=bstack111ll11_opy_ (u"ࠨࠢᨪ"),
                        level=bstack111ll11_opy_ (u"ࠢࠣᨫ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1l1l1ll_opy_=entry.stat().st_size,
                        bstack11ll1ll1l1l_opy_=bstack111ll11_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᨬ"),
                        bstack1l11l11_opy_=os.path.abspath(entry.path),
                        bstack11l1111l1l1_opy_=hook.get(TestFramework.bstack11l11111l11_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1l11111_opy_.add(abs_path)
        platform_index = os.environ[bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᨭ")]
        bstack111llll1ll1_opy_ = os.path.join(bstack11ll11ll1l1_opy_, (bstack11lll1l1111_opy_ + str(platform_index)), bstack111ll111l1l_opy_, bstack111ll1111l1_opy_)
        if not os.path.exists(bstack111llll1ll1_opy_) or not os.path.isdir(bstack111llll1ll1_opy_):
            self.logger.info(bstack111ll11_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᨮ").format(bstack111llll1ll1_opy_))
        else:
            self.logger.info(bstack111ll11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᨯ").format(bstack111llll1ll1_opy_))
            with os.scandir(bstack111llll1ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1l11111_opy_:
                        self.logger.info(bstack111ll11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᨰ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111ll11_opy_ (u"ࠨࠢᨱ")
                        log_entry = bstack1llll111ll_opy_(
                            kind=bstack111ll11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᨲ"),
                            message=bstack111ll11_opy_ (u"ࠣࠤᨳ"),
                            level=bstack111ll11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᨴ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1l1l1ll_opy_=entry.stat().st_size,
                            bstack11ll1ll1l1l_opy_=bstack111ll11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᨵ"),
                            bstack1l11l11_opy_=os.path.abspath(entry.path),
                            bstack11ll111l1l1_opy_=hook.get(TestFramework.bstack11l11111l11_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1l11111_opy_.add(abs_path)
        hook[bstack111ll11_opy_ (u"ࠦࡱࡵࡧࡴࠤᨶ")] = logs
    def bstack11l1ll11_opy_(
        self,
        bstack1l1l1l11l_opy_: bstack1l111llll11_opy_,
        entries: List[bstack1llll111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᨷ"))
        req.platform_index = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack11llllll1ll_opy_)
        req.client_worker_id = bstack111ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᨸ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1l1l11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack1l111ll11ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack11lll11111l_opy_)
            log_entry.uuid = entry.bstack11l1111l1l1_opy_
            log_entry.test_framework_state = bstack1l1l1l11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack111ll11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᨹ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111ll11_opy_ (u"ࠣࠤᨺ")
            if entry.kind == bstack111ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᨻ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1l1l1ll_opy_
                log_entry.file_path = entry.bstack1l11l11_opy_
        def bstack11ll11l11l1_opy_():
            bstack111l1lllll_opy_ = datetime.now()
            try:
                self.bstack1l1l1l1l1l_opy_.LogCreatedEvent(req)
                bstack1l1l1l11l_opy_.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᨼ"), datetime.now() - bstack111l1lllll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᨽ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11l11l1_opy_)
    def __111llll1l11_opy_(self, instance) -> None:
        bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᨾ")
        bstack111lll1ll1l_opy_ = {bstack111ll11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᨿ"): bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l111l11ll_opy_(instance, bstack111lll1ll1l_opy_)
        bstack1l1l111111l_opy_.bstack111lll11lll_opy_()
    @staticmethod
    def bstack111llll1111_opy_(instance: bstack1l111llll11_opy_, bstack111lll11l11_opy_: str):
        bstack111llll1l1l_opy_ = (
            bstack1l11l1l1111_opy_.bstack11l111111l1_opy_
            if bstack111lll11l11_opy_ == bstack1l11l1l1111_opy_.bstack111lll1l1l1_opy_
            else bstack1l11l1l1111_opy_.bstack111ll1ll111_opy_
        )
        bstack11l1111l111_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111lll11l11_opy_, None)
        bstack111ll1l1lll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111llll1l1l_opy_, None) if bstack11l1111l111_opy_ else None
        return (
            bstack111ll1l1lll_opy_[bstack11l1111l111_opy_][-1]
            if isinstance(bstack111ll1l1lll_opy_, dict) and len(bstack111ll1l1lll_opy_.get(bstack11l1111l111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111111l_opy_(instance: bstack1l111llll11_opy_, bstack111lll11l11_opy_: str):
        hook = bstack1l11l1l1111_opy_.bstack111llll1111_opy_(instance, bstack111lll11l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l111l1111_opy_, []).clear()
    @staticmethod
    def __111llll111l_opy_(instance: bstack1l111llll11_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111ll11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᩀ"), None)):
            return
        if os.getenv(bstack111ll11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᩁ"), bstack111ll11_opy_ (u"ࠤ࠴ࠦᩂ")) != bstack111ll11_opy_ (u"ࠥ࠵ࠧᩃ"):
            bstack1l11l1l1111_opy_.logger.warning(bstack111ll11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᩄ"))
            return
        bstack11l111l1l11_opy_ = {
            bstack111ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᩅ"): (bstack1l11l1l1111_opy_.bstack111ll1llll1_opy_, bstack1l11l1l1111_opy_.bstack111ll1ll111_opy_),
            bstack111ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᩆ"): (bstack1l11l1l1111_opy_.bstack111lll1l1l1_opy_, bstack1l11l1l1111_opy_.bstack11l111111l1_opy_),
        }
        for when in (bstack111ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᩇ"), bstack111ll11_opy_ (u"ࠣࡥࡤࡰࡱࠨᩈ"), bstack111ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᩉ")):
            bstack11l111l1l1l_opy_ = args[1].get_records(when)
            if not bstack11l111l1l1l_opy_:
                continue
            records = [
                bstack1llll111ll_opy_(
                    kind=TestFramework.bstack11lll1111ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111ll11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᩊ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111ll11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᩋ")) and r.created
                        else None
                    ),
                )
                for r in bstack11l111l1l1l_opy_
                if isinstance(getattr(r, bstack111ll11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᩌ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111ll11ll11_opy_, bstack111llll1l1l_opy_ = bstack11l111l1l11_opy_.get(when, (None, None))
            bstack111lllll1ll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111ll11ll11_opy_, None) if bstack111ll11ll11_opy_ else None
            bstack111ll1l1lll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111llll1l1l_opy_, None) if bstack111lllll1ll_opy_ else None
            if isinstance(bstack111ll1l1lll_opy_, dict) and len(bstack111ll1l1lll_opy_.get(bstack111lllll1ll_opy_, [])) > 0:
                hook = bstack111ll1l1lll_opy_[bstack111lllll1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l111l1111_opy_ in hook:
                    hook[TestFramework.bstack11l111l1111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll1lll1_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l11l1l1111_opy_.__11l1111lll1_opy_(test.location) if hasattr(test, bstack111ll11_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᩍ")) else getattr(test, bstack111ll11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᩎ"), None)
        test_name = test.name if hasattr(test, bstack111ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᩏ")) else None
        bstack111lllll11l_opy_ = test.fspath.strpath if hasattr(test, bstack111ll11_opy_ (u"ࠤࡩࡷࡵࡧࡴࡩࠤᩐ")) and test.fspath else None
        if not test_id or not test_name or not bstack111lllll11l_opy_:
            return None
        code = None
        if hasattr(test, bstack111ll11_opy_ (u"ࠥࡳࡧࡰࠢᩑ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack111ll11111l_opy_ = []
        try:
            bstack111ll11111l_opy_ = bstack1lll1l11l_opy_.bstack1lll1l1l1l1_opy_(test)
        except:
            bstack1l11l1l1111_opy_.logger.warning(bstack111ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵ࠯ࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡪࡹ࡯࡭ࡸࡨࡨࠥ࡯࡮ࠡࡅࡏࡍࠧᩒ"))
        return {
            TestFramework.bstack1l111l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11l1l1l1l1l_opy_: test_id,
            TestFramework.bstack1l111l1lll1_opy_: test_name,
            TestFramework.bstack11ll111111l_opy_: getattr(test, bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᩓ"), None),
            TestFramework.bstack11l1111l1ll_opy_: bstack111lllll11l_opy_,
            TestFramework.bstack111ll1l1l11_opy_: bstack1l11l1l1111_opy_.__111lll1l1ll_opy_(test),
            TestFramework.bstack111lll111ll_opy_: code,
            TestFramework.bstack11l1ll11111_opy_: TestFramework.bstack111ll11llll_opy_,
            TestFramework.bstack11l11l1l1ll_opy_: test_id,
            TestFramework.bstack111ll111ll1_opy_: bstack111ll11111l_opy_
        }
    @staticmethod
    def __111lll1l1ll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack111ll11_opy_ (u"ࠨ࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠦᩔ"), [])
            markers.extend([getattr(m, bstack111ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᩕ"), None) for m in own_markers if getattr(m, bstack111ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨᩖ"), None)])
            current = getattr(current, bstack111ll11_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᩗ"), None)
        return markers
    @staticmethod
    def __11l1111lll1_opy_(location):
        return bstack111ll11_opy_ (u"ࠥ࠾࠿ࠨᩘ").join(filter(lambda x: isinstance(x, str), location))