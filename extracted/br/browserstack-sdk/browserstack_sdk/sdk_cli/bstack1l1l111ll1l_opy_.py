# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1ll11lll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack111111ll1l_opy_ import bstack11l111l111l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l1ll111_opy_,
    TestHookState,
    bstack1ll1lll111l_opy_,
    bstack11lll1ll1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11lll11111l_opy_
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll111l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11ll1_opy_ import bstack1l1l1l1lll1_opy_
from bstack_utils.bstack11l1l111l_opy_ import bstack1l1lll1l1_opy_
bstack11lll11l1ll_opy_ = bstack11lll11111l_opy_()
bstack111llllll1l_opy_ = 1.0
bstack11ll111ll11_opy_ = bstack1l1111l_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᦷ")
bstack111ll1111l1_opy_ = bstack1l1111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᦸ")
bstack111l1llllll_opy_ = bstack1l1111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᦹ")
bstack111ll111111_opy_ = bstack1l1111l_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᦺ")
bstack111ll1111ll_opy_ = bstack1l1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᦻ")
_11ll111llll_opy_ = set()
class bstack1l11l1l111l_opy_(TestFramework):
    bstack111ll1ll1l1_opy_ = bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᦼ")
    bstack111lll11l1l_opy_ = bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᦽ")
    bstack111ll1l1ll1_opy_ = bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᦾ")
    bstack111lllll111_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᦿ")
    bstack111ll1l11l1_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᧀ")
    bstack11l111l11ll_opy_: bool
    bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_  = None
    bstack11l1ll1lll_opy_ = None
    bstack111ll11ll11_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1l1l1lll111_opy_: List[str]=[bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᧁ")],
        bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_=None,
        bstack11l1ll1lll_opy_=None
    ):
        super().__init__(bstack1l1l1lll111_opy_, bstack1l111lllll1_opy_, bstack1l1lll11l1l_opy_)
        self.bstack11l111l11ll_opy_ = any(bstack1l1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᧂ") in item.lower() for item in bstack1l1l1lll111_opy_)
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
    def track_event(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l11l1l111l_opy_.bstack111ll11ll11_opy_:
            bstack11l111l111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᧃ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠤࠥᧄ"))
            return
        if not self.bstack11l111l11ll_opy_:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᧅ") + str(str(self.bstack1l1l1lll111_opy_)) + bstack1l1111l_opy_ (u"ࠦࠧᧆ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᧇ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠨࠢᧈ"))
            return
        instance = self.__11l111l1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᧉ") + str(args) + bstack1l1111l_opy_ (u"ࠣࠤ᧊"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l11l1l111l_opy_.bstack111ll11ll11_opy_:
                bstack1l11l1l11_opy_ = bstack1l1111l_opy_ (u"ࠤࠥ᧋")
                name = bstack1l1111l_opy_ (u"ࠥࠦ᧌")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111ll111l1l_opy_.value)
                    name = str(EVENTS.bstack111ll111l1l_opy_.name)+bstack1l1111l_opy_ (u"ࠦ࠿ࠨ᧍")+str(test_framework_state.name)
                else:
                    bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack111ll111l11_opy_.value)
                    name = str(EVENTS.bstack111ll111l11_opy_.name)+bstack1l1111l_opy_ (u"ࠧࡀࠢ᧎")+str(test_framework_state.name)
                TestFramework.bstack111lll11ll1_opy_(instance, name, bstack1l11l1l11_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥ᧏").format(e))
        try:
            if not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11l1ll11111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l11l1l111l_opy_.__111ll1l111l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ᧐") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠣࠤ᧑"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11lll1111ll_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11lll1111ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ᧒") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠥࠦ᧓"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢ᧔") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠧࠨ᧕"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l11l1l111l_opy_.__11l111111l1_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll11111_opy_(instance, *args)
                self.__11l1111llll_opy_(instance)
            elif test_framework_state in bstack1l11l1l111l_opy_.bstack111ll11ll11_opy_:
                self.__111ll1l1111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢ᧖") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠢࠣ᧗"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111lllll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l11l1l111l_opy_.bstack111ll11ll11_opy_:
                bstack1l11l1l11_opy_ = bstack1l1111l_opy_ (u"ࠣࠤ᧘")
                name = bstack1l1111l_opy_ (u"ࠤࠥ᧙")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111ll111l1l_opy_.name)+bstack1l1111l_opy_ (u"ࠥ࠾ࠧ᧚")+str(test_framework_state.name)
                    bstack1l11l1l11_opy_ = TestFramework.bstack111ll1l1l11_opy_(instance, name)
                    bstack11lll1111_opy_.end(EVENTS.bstack111ll111l1l_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᧛"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᧜"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll111l11_opy_.name)+bstack1l1111l_opy_ (u"ࠨ࠺ࠣ᧝")+str(test_framework_state.name)
                    bstack1l11l1l11_opy_ = TestFramework.bstack111ll1l1l11_opy_(instance, name)
                    bstack11lll1111_opy_.end(EVENTS.bstack111ll111l11_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᧞"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᧟"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ᧠").format(e))
    def bstack11ll11l111l_opy_(self):
        return self.bstack11l111l11ll_opy_
    def bstack11ll1l11l1l_opy_(self):
        return False
    def __111lll1l11l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ᧡"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11ll1lll1l1_opy_(rep, [bstack1l1111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤ᧢"), bstack1l1111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨ᧣"), bstack1l1111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ᧤"), bstack1l1111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ᧥"), bstack1l1111l_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤ᧦"), bstack1l1111l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣ᧧")])
        return None
    def __111lll11111_opy_(self, instance: bstack1l11l1ll111_opy_, *args):
        result = self.__111lll1l11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        if result.get(bstack1l1111l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᧨"), None) == bstack1l1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ᧩") and len(args) > 1 and getattr(args[1], bstack1l1111l_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨ᧪"), None) is not None:
            failure = [{bstack1l1111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᧫"): [args[1].excinfo.exconly(), result.get(bstack1l1111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ᧬"), None)]}]
            bstack1ll111l1l1l_opy_ = bstack1l1111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ᧭") if bstack1l1111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ᧮") in getattr(args[1].excinfo, bstack1l1111l_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧ᧯"), bstack1l1111l_opy_ (u"ࠦࠧ᧰")) else bstack1l1111l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ᧱")
        bstack111ll11l111_opy_ = result.get(bstack1l1111l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᧲"), TestFramework.bstack111lll1l1ll_opy_)
        if bstack111ll11l111_opy_ != TestFramework.bstack111lll1l1ll_opy_:
            TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11ll111l11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack111ll1lllll_opy_(instance, {
            TestFramework.bstack11l1l1ll11l_opy_: failure,
            TestFramework.bstack111ll11l1ll_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack11l1ll1111l_opy_: bstack111ll11l111_opy_,
        })
    def __11l111l1l11_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll11ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1l1l1ll_opy_ bstack111lll1111l_opy_ this to be bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᧳")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111ll1ll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1111l_opy_ (u"ࠣࡰࡲࡨࡪࠨ᧴"), None), bstack1l1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᧵"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᧶"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1ll1ll1ll_opy_(target) if target else None
        return instance
    def __111ll1l1111_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack111lll1l111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l11l1l111l_opy_.bstack111lll11l1l_opy_, {})
        if not key in bstack111lll1l111_opy_:
            bstack111lll1l111_opy_[key] = []
        bstack111llllllll_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l11l1l111l_opy_.bstack111ll1l1ll1_opy_, {})
        if not key in bstack111llllllll_opy_:
            bstack111llllllll_opy_[key] = []
        bstack111llllll11_opy_ = {
            bstack1l11l1l111l_opy_.bstack111lll11l1l_opy_: bstack111lll1l111_opy_,
            bstack1l11l1l111l_opy_.bstack111ll1l1ll1_opy_: bstack111llllllll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1l1111l_opy_ (u"ࠦࡰ࡫ࡹࠣ᧷"): key,
                TestFramework.bstack11l1111l111_opy_: uuid4().__str__(),
                TestFramework.bstack111lll111ll_opy_: TestFramework.bstack111ll1lll11_opy_,
                TestFramework.bstack111ll11lll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll111lll_opy_: [],
                TestFramework.bstack11l1111ll1l_opy_: args[1] if len(args) > 1 else bstack1l1111l_opy_ (u"ࠬ࠭᧸"),
                TestFramework.bstack111lll1llll_opy_: bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()
            }
            bstack111lll1l111_opy_[key].append(hook)
            bstack111llllll11_opy_[bstack1l11l1l111l_opy_.bstack111lllll111_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llll1lll_opy_ = bstack111lll1l111_opy_.get(key, [])
            hook = bstack111llll1lll_opy_.pop() if bstack111llll1lll_opy_ else None
            if hook:
                result = self.__111lll1l11l_opy_(*args)
                if result:
                    bstack11l1111l1l1_opy_ = result.get(bstack1l1111l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᧹"), TestFramework.bstack111ll1lll11_opy_)
                    if bstack11l1111l1l1_opy_ != TestFramework.bstack111ll1lll11_opy_:
                        hook[TestFramework.bstack111lll111ll_opy_] = bstack11l1111l1l1_opy_
                hook[TestFramework.bstack11l111111ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111lll1llll_opy_]= bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()
                self.bstack11l1111l1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111llll1l1l_opy_, [])
                if logs: self.bstack1llll111ll_opy_(instance, logs)
                bstack111llllllll_opy_[key].append(hook)
                bstack111llllll11_opy_[bstack1l11l1l111l_opy_.bstack111ll1l11l1_opy_] = key
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨ᧺") + str(bstack111llllllll_opy_) + bstack1l1111l_opy_ (u"ࠣࠤ᧻"))
    def __111ll11ll1l_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11ll1lll1l1_opy_(args[0], [bstack1l1111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ᧼"), bstack1l1111l_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦ᧽"), bstack1l1111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦ᧾"), bstack1l1111l_opy_ (u"ࠧ࡯ࡤࡴࠤ᧿"), bstack1l1111l_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᨀ"), bstack1l1111l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᨁ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᨂ")) else fixturedef.get(bstack1l1111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᨃ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1111l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᨄ")) else None
        node = request.node if hasattr(request, bstack1l1111l_opy_ (u"ࠦࡳࡵࡤࡦࠤᨅ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1111l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᨆ")) else None
        baseid = fixturedef.get(bstack1l1111l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᨇ"), None) or bstack1l1111l_opy_ (u"ࠢࠣᨈ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1111l_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᨉ")):
            target = bstack1l11l1l111l_opy_.__111lll11lll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1111l_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᨊ")) else None
            if target and not TestFramework.bstack1l1ll1ll1ll_opy_(target):
                self.__111ll1ll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᨋ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠦࠧᨌ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᨍ") + str(target) + bstack1l1111l_opy_ (u"ࠨࠢᨎ"))
            return None
        instance = TestFramework.bstack1l1ll1ll1ll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᨏ") + str(target) + bstack1l1111l_opy_ (u"ࠣࠤᨐ"))
            return None
        bstack11l11111l11_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l11l1l111l_opy_.bstack111ll1ll1l1_opy_, {})
        if os.getenv(bstack1l1111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᨑ"), bstack1l1111l_opy_ (u"ࠥ࠵ࠧᨒ")) == bstack1l1111l_opy_ (u"ࠦ࠶ࠨᨓ"):
            bstack11l1111l11l_opy_ = bstack1l1111l_opy_ (u"ࠧࡀࠢᨔ").join((scope, fixturename))
            bstack111ll1l1lll_opy_ = datetime.now(tz=timezone.utc)
            bstack111ll11llll_opy_ = {
                bstack1l1111l_opy_ (u"ࠨ࡫ࡦࡻࠥᨕ"): bstack11l1111l11l_opy_,
                bstack1l1111l_opy_ (u"ࠢࡵࡣࡪࡷࠧᨖ"): bstack1l11l1l111l_opy_.__111lll1l1l1_opy_(request.node),
                bstack1l1111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᨗ"): fixturedef,
                bstack1l1111l_opy_ (u"ࠤࡶࡧࡴࡶࡥᨘࠣ"): scope,
                bstack1l1111l_opy_ (u"ࠥࡸࡾࡶࡥࠣᨙ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1l1111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᨚ"), None)):
                    bstack111ll11llll_opy_[bstack1l1111l_opy_ (u"ࠧࡺࡹࡱࡧࠥᨛ")] = TestFramework.bstack11lll11ll11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111ll11llll_opy_[bstack1l1111l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦ᨜")] = uuid4().__str__()
                bstack111ll11llll_opy_[bstack1l11l1l111l_opy_.bstack111ll11lll1_opy_] = bstack111ll1l1lll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111ll11llll_opy_[bstack1l11l1l111l_opy_.bstack11l111111ll_opy_] = bstack111ll1l1lll_opy_
            if bstack11l1111l11l_opy_ in bstack11l11111l11_opy_:
                bstack11l11111l11_opy_[bstack11l1111l11l_opy_].update(bstack111ll11llll_opy_)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣ᨝") + str(bstack11l11111l11_opy_[bstack11l1111l11l_opy_]) + bstack1l1111l_opy_ (u"ࠣࠤ᨞"))
            else:
                bstack11l11111l11_opy_[bstack11l1111l11l_opy_] = bstack111ll11llll_opy_
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧ᨟") + str(len(bstack11l11111l11_opy_)) + bstack1l1111l_opy_ (u"ࠥࠦᨠ"))
        TestFramework.bstack111l1llll1_opy_(instance, bstack1l11l1l111l_opy_.bstack111ll1ll1l1_opy_, bstack11l11111l11_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᨡ") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠧࠨᨢ"))
        return instance
    def __111ll1ll1ll_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll11lll1_opy_.create_context(target)
        ob = bstack1l11l1ll111_opy_(ctx, self.bstack1l1l1lll111_opy_, self.bstack1l111lllll1_opy_, test_framework_state)
        TestFramework.bstack111ll1lllll_opy_(ob, {
            TestFramework.bstack1l11111l11l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l1lll_opy_: context.test_framework_version,
            TestFramework.bstack111lll1lll1_opy_: [],
            bstack1l11l1l111l_opy_.bstack111ll1ll1l1_opy_: {},
            bstack1l11l1l111l_opy_.bstack111ll1l1ll1_opy_: {},
            bstack1l11l1l111l_opy_.bstack111lll11l1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111l1llll1_opy_(ob, TestFramework.bstack11l1111lll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111l1llll1_opy_(ob, TestFramework.bstack1l111l1l111_opy_, context.platform_index)
        TestFramework.bstack1lllll1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᨣ") + str(TestFramework.bstack1lllll1ll1_opy_.keys()) + bstack1l1111l_opy_ (u"ࠢࠣᨤ"))
        return ob
    def bstack11lll1l111l_opy_(self, instance: bstack1l11l1ll111_opy_, bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            bstack1l11l1l111l_opy_.bstack111lllll111_opy_
            if bstack1l1ll1ll111_opy_[1] == TestHookState.PRE
            else bstack1l11l1l111l_opy_.bstack111ll1l11l1_opy_
        )
        hook = bstack1l11l1l111l_opy_.bstack111ll1l11ll_opy_(instance, bstack111lll11l11_opy_)
        entries = hook.get(TestFramework.bstack111ll111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, []))
        return entries
    def bstack11ll1llll1l_opy_(self, instance: bstack1l11l1ll111_opy_, bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11l11_opy_ = (
            bstack1l11l1l111l_opy_.bstack111lllll111_opy_
            if bstack1l1ll1ll111_opy_[1] == TestHookState.PRE
            else bstack1l11l1l111l_opy_.bstack111ll1l11l1_opy_
        )
        bstack1l11l1l111l_opy_.bstack111lllll1ll_opy_(instance, bstack111lll11l11_opy_)
        TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, []).clear()
    def bstack11l1111l1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᨥ")
        global _11ll111llll_opy_
        platform_index = os.environ[bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᨦ")]
        bstack11lll11l111_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), bstack111ll111111_opy_)
        if not os.path.exists(bstack11lll11l111_opy_) or not os.path.isdir(bstack11lll11l111_opy_):
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᨧ").format(bstack11lll11l111_opy_))
            return
        logs = hook.get(bstack1l1111l_opy_ (u"ࠦࡱࡵࡧࡴࠤᨨ"), [])
        with os.scandir(bstack11lll11l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll111llll_opy_:
                    self.logger.info(bstack1l1111l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᨩ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1111l_opy_ (u"ࠨࠢᨪ")
                    log_entry = bstack11lll1ll1l_opy_(
                        kind=bstack1l1111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᨫ"),
                        message=bstack1l1111l_opy_ (u"ࠣࠤᨬ"),
                        level=bstack1l1111l_opy_ (u"ࠤࠥᨭ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll11l1111_opy_=entry.stat().st_size,
                        bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᨮ"),
                        bstack111111_opy_=os.path.abspath(entry.path),
                        bstack111ll1l1l1l_opy_=hook.get(TestFramework.bstack11l1111l111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll111llll_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᨯ")]
        bstack111llll11l1_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), bstack111ll111111_opy_, bstack111ll1111ll_opy_)
        if not os.path.exists(bstack111llll11l1_opy_) or not os.path.isdir(bstack111llll11l1_opy_):
            self.logger.info(bstack1l1111l_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᨰ").format(bstack111llll11l1_opy_))
        else:
            self.logger.info(bstack1l1111l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᨱ").format(bstack111llll11l1_opy_))
            with os.scandir(bstack111llll11l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll111llll_opy_:
                        self.logger.info(bstack1l1111l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᨲ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1111l_opy_ (u"ࠣࠤᨳ")
                        log_entry = bstack11lll1ll1l_opy_(
                            kind=bstack1l1111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᨴ"),
                            message=bstack1l1111l_opy_ (u"ࠥࠦᨵ"),
                            level=bstack1l1111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᨶ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll11l1111_opy_=entry.stat().st_size,
                            bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᨷ"),
                            bstack111111_opy_=os.path.abspath(entry.path),
                            bstack11ll111l111_opy_=hook.get(TestFramework.bstack11l1111l111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll111llll_opy_.add(abs_path)
        hook[bstack1l1111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᨸ")] = logs
    def bstack1llll111ll_opy_(
        self,
        bstack1l111ll1ll_opy_: bstack1l11l1ll111_opy_,
        entries: List[bstack11lll1ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᨹ"))
        req.platform_index = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l111l1l111_opy_)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᨺ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l11111l11l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11ll11l1lll_opy_)
            log_entry.uuid = entry.bstack111ll1l1l1l_opy_
            log_entry.test_framework_state = bstack1l111ll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᨻ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1111l_opy_ (u"ࠥࠦᨼ")
            if entry.kind == bstack1l1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᨽ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll11l1111_opy_
                log_entry.file_path = entry.bstack111111_opy_
        def bstack11ll11lll11_opy_():
            bstack11l11l1l_opy_ = datetime.now()
            try:
                self.bstack11l1ll1lll_opy_.LogCreatedEvent(req)
                bstack1l111ll1ll_opy_.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᨾ"), datetime.now() - bstack11l11l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᨿ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11lll11_opy_)
    def __11l1111llll_opy_(self, instance) -> None:
        bstack1l1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᩀ")
        bstack111llllll11_opy_ = {bstack1l1111l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᩁ"): bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        bstack1l1l1l1lll1_opy_.bstack111lll1ll11_opy_()
    @staticmethod
    def bstack111ll1l11ll_opy_(instance: bstack1l11l1ll111_opy_, bstack111lll11l11_opy_: str):
        bstack11l11111111_opy_ = (
            bstack1l11l1l111l_opy_.bstack111ll1l1ll1_opy_
            if bstack111lll11l11_opy_ == bstack1l11l1l111l_opy_.bstack111ll1l11l1_opy_
            else bstack1l11l1l111l_opy_.bstack111lll11l1l_opy_
        )
        bstack11l111l11l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack111lll11l11_opy_, None)
        bstack111lll111l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack11l11111111_opy_, None) if bstack11l111l11l1_opy_ else None
        return (
            bstack111lll111l1_opy_[bstack11l111l11l1_opy_][-1]
            if isinstance(bstack111lll111l1_opy_, dict) and len(bstack111lll111l1_opy_.get(bstack11l111l11l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack111lllll1ll_opy_(instance: bstack1l11l1ll111_opy_, bstack111lll11l11_opy_: str):
        hook = bstack1l11l1l111l_opy_.bstack111ll1l11ll_opy_(instance, bstack111lll11l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll111lll_opy_, []).clear()
    @staticmethod
    def __11l111111l1_opy_(instance: bstack1l11l1ll111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1111l_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᩂ"), None)):
            return
        if os.getenv(bstack1l1111l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᩃ"), bstack1l1111l_opy_ (u"ࠦ࠶ࠨᩄ")) != bstack1l1111l_opy_ (u"ࠧ࠷ࠢᩅ"):
            bstack1l11l1l111l_opy_.logger.warning(bstack1l1111l_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᩆ"))
            return
        bstack111llll1l11_opy_ = {
            bstack1l1111l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᩇ"): (bstack1l11l1l111l_opy_.bstack111lllll111_opy_, bstack1l11l1l111l_opy_.bstack111lll11l1l_opy_),
            bstack1l1111l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᩈ"): (bstack1l11l1l111l_opy_.bstack111ll1l11l1_opy_, bstack1l11l1l111l_opy_.bstack111ll1l1ll1_opy_),
        }
        for when in (bstack1l1111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᩉ"), bstack1l1111l_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᩊ"), bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᩋ")):
            bstack111ll1lll1l_opy_ = args[1].get_records(when)
            if not bstack111ll1lll1l_opy_:
                continue
            records = [
                bstack11lll1ll1l_opy_(
                    kind=TestFramework.bstack11lll11llll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1111l_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᩌ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1111l_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᩍ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll1lll1l_opy_
                if isinstance(getattr(r, bstack1l1111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᩎ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111llll111l_opy_, bstack11l11111111_opy_ = bstack111llll1l11_opy_.get(when, (None, None))
            bstack111ll1ll111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack111llll111l_opy_, None) if bstack111llll111l_opy_ else None
            bstack111lll111l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack11l11111111_opy_, None) if bstack111ll1ll111_opy_ else None
            if isinstance(bstack111lll111l1_opy_, dict) and len(bstack111lll111l1_opy_.get(bstack111ll1ll111_opy_, [])) > 0:
                hook = bstack111lll111l1_opy_[bstack111ll1ll111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll111lll_opy_ in hook:
                    hook[TestFramework.bstack111ll111lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111ll1l111l_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l11l1l111l_opy_.__111lll11lll_opy_(test.location) if hasattr(test, bstack1l1111l_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᩏ")) else getattr(test, bstack1l1111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᩐ"), None)
        test_name = test.name if hasattr(test, bstack1l1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᩑ")) else None
        bstack111ll11l1l1_opy_ = test.fspath.strpath if hasattr(test, bstack1l1111l_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᩒ")) and test.fspath else None
        if not test_id or not test_name or not bstack111ll11l1l1_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1111l_opy_ (u"ࠧࡵࡢ࡫ࠤᩓ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack111ll111ll1_opy_ = []
        try:
            bstack111ll111ll1_opy_ = bstack1l1lll1l1_opy_.bstack1lll1l11ll1_opy_(test)
        except:
            bstack1l11l1l111l_opy_.logger.warning(bstack1l1111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᩔ"))
        return {
            TestFramework.bstack11llllll111_opy_: uuid4().__str__(),
            TestFramework.bstack11l1ll11111_opy_: test_id,
            TestFramework.bstack1l111l11l1l_opy_: test_name,
            TestFramework.bstack11ll11111l1_opy_: getattr(test, bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᩕ"), None),
            TestFramework.bstack11l1111ll11_opy_: bstack111ll11l1l1_opy_,
            TestFramework.bstack11l11111ll1_opy_: bstack1l11l1l111l_opy_.__111lll1l1l1_opy_(test),
            TestFramework.bstack11l1111111l_opy_: code,
            TestFramework.bstack11l1ll1111l_opy_: TestFramework.bstack111lll1l1ll_opy_,
            TestFramework.bstack11l11l11l1l_opy_: test_id,
            TestFramework.bstack111ll11111l_opy_: bstack111ll111ll1_opy_
        }
    @staticmethod
    def __111lll1l1l1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1111l_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᩖ"), [])
            markers.extend([getattr(m, bstack1l1111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩗ"), None) for m in own_markers if getattr(m, bstack1l1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᩘ"), None)])
            current = getattr(current, bstack1l1111l_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᩙ"), None)
        return markers
    @staticmethod
    def __111lll11lll_opy_(location):
        return bstack1l1111l_opy_ (u"ࠧࡀ࠺ࠣᩚ").join(filter(lambda x: isinstance(x, str), location))