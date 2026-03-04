# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll1l1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l11ll11_opy_ import bstack11ll11l1ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1ll111l1l1l_opy_,
    TestHookState,
    bstack1lll1l11l1l_opy_,
    bstack1ll11ll1l1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l111l11lll_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1ll1lllll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1111ll11_opy_ import bstack1l1ll1ll1ll_opy_
from bstack_utils.bstack1111ll1111_opy_ import bstack111lllll1_opy_
bstack1l11l1lllll_opy_ = bstack1l111l11lll_opy_()
bstack11ll1111111_opy_ = 1.0
bstack1l111l1l111_opy_ = bstack1lll1l_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᝑ")
bstack11l1l1llll1_opy_ = bstack1lll1l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᝒ")
bstack11l1l1lll11_opy_ = bstack1lll1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᝓ")
bstack11l1l1lll1l_opy_ = bstack1lll1l_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦ᝔")
bstack11l1ll1111l_opy_ = bstack1lll1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ᝕")
_1l111ll1l1l_opy_ = set()
class bstack1l1ll1lll1l_opy_(TestFramework):
    bstack11ll1l1ll11_opy_ = bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥ᝖")
    bstack11l1ll1lll1_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤ᝗")
    bstack11ll11lll1l_opy_ = bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ᝘")
    bstack11l1lll1lll_opy_ = bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ᝙")
    bstack11ll11111l1_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ᝚")
    bstack11l1lll1l1l_opy_: bool
    bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_  = None
    bstack1lll111lll1_opy_ = None
    bstack11l1lll11l1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11l1llll1ll_opy_: Dict[str, str],
        bstack1l1l1ll1l1l_opy_: List[str]=[bstack1lll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣ᝛")],
        bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_=None,
        bstack1lll111lll1_opy_=None
    ):
        super().__init__(bstack1l1l1ll1l1l_opy_, bstack11l1llll1ll_opy_, bstack1lll111111l_opy_)
        self.bstack11l1lll1l1l_opy_ = any(bstack1lll1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤ᝜") in item.lower() for item in bstack1l1l1ll1l1l_opy_)
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
    def track_event(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1ll1lll1l_opy_.bstack11l1lll11l1_opy_:
            bstack11ll11l1ll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦ᝝") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠦࠧ᝞"))
            return
        if not self.bstack11l1lll1l1l_opy_:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨ᝟") + str(str(self.bstack1l1l1ll1l1l_opy_)) + bstack1lll1l_opy_ (u"ࠨࠢᝠ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝡ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠣࠤᝢ"))
            return
        instance = self.__11ll11ll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᝣ") + str(args) + bstack1lll1l_opy_ (u"ࠥࠦᝤ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1ll1lll1l_opy_.bstack11l1lll11l1_opy_:
                bstack1ll111111l_opy_ = bstack1lll1l_opy_ (u"ࠦࠧᝥ")
                name = bstack1lll1l_opy_ (u"ࠧࠨᝦ")
                if (test_hook_state == TestHookState.PRE):
                    bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11l1ll111ll_opy_.value)
                    name = str(EVENTS.bstack11l1ll111ll_opy_.name)+bstack1lll1l_opy_ (u"ࠨ࠺ࠣᝧ")+str(test_framework_state.name)
                else:
                    bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11l1ll111l1_opy_.value)
                    name = str(EVENTS.bstack11l1ll111l1_opy_.name)+bstack1lll1l_opy_ (u"ࠢ࠻ࠤᝨ")+str(test_framework_state.name)
                TestFramework.bstack11ll1l11l1l_opy_(instance, name, bstack1ll111111l_opy_)
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᝩ").format(e))
        try:
            if not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack11lllll1111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1ll1lll1l_opy_.__11ll1ll1111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᝪ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠥࠦᝫ"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l111l11l1l_opy_):
                    TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l111l11l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᝬ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠧࠨ᝭"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_):
                    TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᝮ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠢࠣᝯ"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1ll1lll1l_opy_.__11ll111llll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll1111l11_opy_(instance, *args)
                self.__11ll1l1111l_opy_(instance)
            elif test_framework_state in bstack1l1ll1lll1l_opy_.bstack11l1lll11l1_opy_:
                self.__11ll11llll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᝰ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠤࠥ᝱"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1ll1lll1l_opy_.bstack11l1lll11l1_opy_:
                bstack1ll111111l_opy_ = bstack1lll1l_opy_ (u"ࠥࠦᝲ")
                name = bstack1lll1l_opy_ (u"ࠦࠧᝳ")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1ll111ll_opy_.name)+bstack1lll1l_opy_ (u"ࠧࡀࠢ᝴")+str(test_framework_state.name)
                    bstack1ll111111l_opy_ = TestFramework.bstack11ll111111l_opy_(instance, name)
                    bstack1l11l11ll1_opy_.end(EVENTS.bstack11l1ll111ll_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᝵"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᝶"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1ll111l1_opy_.name)+bstack1lll1l_opy_ (u"ࠣ࠼ࠥ᝷")+str(test_framework_state.name)
                    bstack1ll111111l_opy_ = TestFramework.bstack11ll111111l_opy_(instance, name)
                    bstack1l11l11ll1_opy_.end(EVENTS.bstack11l1ll111l1_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᝸"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᝹"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᝺").format(e))
    def bstack1l11l111lll_opy_(self):
        return self.bstack11l1lll1l1l_opy_
    def bstack1l11l1l11l1_opy_(self):
        return False
    def __11ll1l1ll1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1lll1l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤ᝻"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l111l1l1l1_opy_(rep, [bstack1lll1l_opy_ (u"ࠨࡷࡩࡧࡱࠦ᝼"), bstack1lll1l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ᝽"), bstack1lll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ᝾"), bstack1lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᝿"), bstack1lll1l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦក"), bstack1lll1l_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥខ")])
        return None
    def __11ll1111l11_opy_(self, instance: bstack1ll111l1l1l_opy_, *args):
        result = self.__11ll1l1ll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll111l_opy_ = None
        if result.get(bstack1lll1l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨគ"), None) == bstack1lll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨឃ") and len(args) > 1 and getattr(args[1], bstack1lll1l_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣង"), None) is not None:
            failure = [{bstack1lll1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫច"): [args[1].excinfo.exconly(), result.get(bstack1lll1l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣឆ"), None)]}]
            bstack1lll1ll111l_opy_ = bstack1lll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦជ") if bstack1lll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢឈ") in getattr(args[1].excinfo, bstack1lll1l_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢញ"), bstack1lll1l_opy_ (u"ࠨࠢដ")) else bstack1lll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣឋ")
        bstack11ll1l1l111_opy_ = result.get(bstack1lll1l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤឌ"), TestFramework.bstack11l1ll1llll_opy_)
        if bstack11ll1l1l111_opy_ != TestFramework.bstack11l1ll1llll_opy_:
            TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1l111ll_opy_(instance, {
            TestFramework.bstack11llllll1l1_opy_: failure,
            TestFramework.bstack11ll111ll11_opy_: bstack1lll1ll111l_opy_,
            TestFramework.bstack1l1111111l1_opy_: bstack11ll1l1l111_opy_,
        })
    def __11ll11ll1l1_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__11ll1l11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll1ll1_opy_ bstack11l1lllll11_opy_ this to be bstack1lll1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤឍ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll11111ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack1lll1l_opy_ (u"ࠥࡲࡴࡪࡥࠣណ"), None), bstack1lll1l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦត"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1lll1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧថ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1l1l111l_opy_(target) if target else None
        return instance
    def __11ll11llll1_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1l11_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack1l1ll1lll1l_opy_.bstack11l1ll1lll1_opy_, {})
        if not key in bstack11l1lll1l11_opy_:
            bstack11l1lll1l11_opy_[key] = []
        bstack11l1llllll1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack1l1ll1lll1l_opy_.bstack11ll11lll1l_opy_, {})
        if not key in bstack11l1llllll1_opy_:
            bstack11l1llllll1_opy_[key] = []
        bstack11ll11ll111_opy_ = {
            bstack1l1ll1lll1l_opy_.bstack11l1ll1lll1_opy_: bstack11l1lll1l11_opy_,
            bstack1l1ll1lll1l_opy_.bstack11ll11lll1l_opy_: bstack11l1llllll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1lll1l_opy_ (u"ࠨ࡫ࡦࡻࠥទ"): key,
                TestFramework.bstack11ll1111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11l1llll11l_opy_: TestFramework.bstack11ll11ll1ll_opy_,
                TestFramework.bstack11ll1l1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1l111l1_opy_: [],
                TestFramework.bstack11ll1111l1l_opy_: args[1] if len(args) > 1 else bstack1lll1l_opy_ (u"ࠧࠨធ"),
                TestFramework.bstack11ll11l11ll_opy_: bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()
            }
            bstack11l1lll1l11_opy_[key].append(hook)
            bstack11ll11ll111_opy_[bstack1l1ll1lll1l_opy_.bstack11l1lll1lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11ll11l1111_opy_ = bstack11l1lll1l11_opy_.get(key, [])
            hook = bstack11ll11l1111_opy_.pop() if bstack11ll11l1111_opy_ else None
            if hook:
                result = self.__11ll1l1ll1l_opy_(*args)
                if result:
                    bstack11l1ll1l1ll_opy_ = result.get(bstack1lll1l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤន"), TestFramework.bstack11ll11ll1ll_opy_)
                    if bstack11l1ll1l1ll_opy_ != TestFramework.bstack11ll11ll1ll_opy_:
                        hook[TestFramework.bstack11l1llll11l_opy_] = bstack11l1ll1l1ll_opy_
                hook[TestFramework.bstack11l1llll1l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll11l11ll_opy_]= bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()
                self.bstack11l1lll11ll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll11ll1_opy_, [])
                if logs: self.bstack1l111l1lll1_opy_(instance, logs)
                bstack11l1llllll1_opy_[key].append(hook)
                bstack11ll11ll111_opy_[bstack1l1ll1lll1l_opy_.bstack11ll11111l1_opy_] = key
        TestFramework.bstack11ll1l111ll_opy_(instance, bstack11ll11ll111_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣប") + str(bstack11l1llllll1_opy_) + bstack1lll1l_opy_ (u"ࠥࠦផ"))
    def __11ll1l11lll_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l111l1l1l1_opy_(args[0], [bstack1lll1l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥព"), bstack1lll1l_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨភ"), bstack1lll1l_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨម"), bstack1lll1l_opy_ (u"ࠢࡪࡦࡶࠦយ"), bstack1lll1l_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥរ"), bstack1lll1l_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤល")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1lll1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤវ")) else fixturedef.get(bstack1lll1l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥឝ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1lll1l_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥឞ")) else None
        node = request.node if hasattr(request, bstack1lll1l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦស")) else None
        target = request.node.nodeid if hasattr(node, bstack1lll1l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢហ")) else None
        baseid = fixturedef.get(bstack1lll1l_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣឡ"), None) or bstack1lll1l_opy_ (u"ࠤࠥអ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1lll1l_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣឣ")):
            target = bstack1l1ll1lll1l_opy_.__11ll111ll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1lll1l_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨឤ")) else None
            if target and not TestFramework.bstack1ll1l1l111l_opy_(target):
                self.__11ll11111ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢឥ") + str(test_hook_state) + bstack1lll1l_opy_ (u"ࠨࠢឦ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧឧ") + str(target) + bstack1lll1l_opy_ (u"ࠣࠤឨ"))
            return None
        instance = TestFramework.bstack1ll1l1l111l_opy_(target)
        if not instance:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦឩ") + str(target) + bstack1lll1l_opy_ (u"ࠥࠦឪ"))
            return None
        bstack11l1ll1l111_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack1l1ll1lll1l_opy_.bstack11ll1l1ll11_opy_, {})
        if os.getenv(bstack1lll1l_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧឫ"), bstack1lll1l_opy_ (u"ࠧ࠷ࠢឬ")) == bstack1lll1l_opy_ (u"ࠨ࠱ࠣឭ"):
            bstack11ll1l1lll1_opy_ = bstack1lll1l_opy_ (u"ࠢ࠻ࠤឮ").join((scope, fixturename))
            bstack11ll11l11l1_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll1l11l11_opy_ = {
                bstack1lll1l_opy_ (u"ࠣ࡭ࡨࡽࠧឯ"): bstack11ll1l1lll1_opy_,
                bstack1lll1l_opy_ (u"ࠤࡷࡥ࡬ࡹࠢឰ"): bstack1l1ll1lll1l_opy_.__11ll111l1ll_opy_(request.node),
                bstack1lll1l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦឱ"): fixturedef,
                bstack1lll1l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥឲ"): scope,
                bstack1lll1l_opy_ (u"ࠧࡺࡹࡱࡧࠥឳ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack1lll1l_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥ឴"), None)):
                    bstack11ll1l11l11_opy_[bstack1lll1l_opy_ (u"ࠢࡵࡻࡳࡩࠧ឵")] = TestFramework.bstack1l11l11l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack11ll1l11l11_opy_[bstack1lll1l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨា")] = uuid4().__str__()
                bstack11ll1l11l11_opy_[bstack1l1ll1lll1l_opy_.bstack11ll1l1l1ll_opy_] = bstack11ll11l11l1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11ll1l11l11_opy_[bstack1l1ll1lll1l_opy_.bstack11l1llll1l1_opy_] = bstack11ll11l11l1_opy_
            if bstack11ll1l1lll1_opy_ in bstack11l1ll1l111_opy_:
                bstack11l1ll1l111_opy_[bstack11ll1l1lll1_opy_].update(bstack11ll1l11l11_opy_)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥិ") + str(bstack11l1ll1l111_opy_[bstack11ll1l1lll1_opy_]) + bstack1lll1l_opy_ (u"ࠥࠦី"))
            else:
                bstack11l1ll1l111_opy_[bstack11ll1l1lll1_opy_] = bstack11ll1l11l11_opy_
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢឹ") + str(len(bstack11l1ll1l111_opy_)) + bstack1lll1l_opy_ (u"ࠧࠨឺ"))
        TestFramework.bstack1lll1l11lll_opy_(instance, bstack1l1ll1lll1l_opy_.bstack11ll1l1ll11_opy_, bstack11l1ll1l111_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨុ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠢࠣូ"))
        return instance
    def __11ll11111ll_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1ll1l1ll_opy_.create_context(target)
        ob = bstack1ll111l1l1l_opy_(ctx, self.bstack1l1l1ll1l1l_opy_, self.bstack11l1llll1ll_opy_, test_framework_state)
        TestFramework.bstack11ll1l111ll_opy_(ob, {
            TestFramework.bstack1l1l111ll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l11l11l1ll_opy_: context.test_framework_version,
            TestFramework.bstack11l1ll11l1l_opy_: [],
            bstack1l1ll1lll1l_opy_.bstack11ll1l1ll11_opy_: {},
            bstack1l1ll1lll1l_opy_.bstack11ll11lll1l_opy_: {},
            bstack1l1ll1lll1l_opy_.bstack11l1ll1lll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1l11lll_opy_(ob, TestFramework.bstack11ll11lll11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l11lll_opy_(ob, TestFramework.bstack1l1l1lll111_opy_, context.platform_index)
        TestFramework.bstack1lll1l1111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣួ") + str(TestFramework.bstack1lll1l1111l_opy_.keys()) + bstack1lll1l_opy_ (u"ࠤࠥើ"))
        return ob
    def bstack1l11ll1l11l_opy_(self, instance: bstack1ll111l1l1l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111ll1_opy_ = (
            bstack1l1ll1lll1l_opy_.bstack11l1lll1lll_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1l1ll1lll1l_opy_.bstack11ll11111l1_opy_
        )
        hook = bstack1l1ll1lll1l_opy_.bstack11l1ll1l1l1_opy_(instance, bstack11ll1111ll1_opy_)
        entries = hook.get(TestFramework.bstack11ll1l111l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, []))
        return entries
    def bstack1l11l1lll11_opy_(self, instance: bstack1ll111l1l1l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111ll1_opy_ = (
            bstack1l1ll1lll1l_opy_.bstack11l1lll1lll_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1l1ll1lll1l_opy_.bstack11ll11111l1_opy_
        )
        bstack1l1ll1lll1l_opy_.bstack11ll11l1l1l_opy_(instance, bstack11ll1111ll1_opy_)
        TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, []).clear()
    def bstack11l1lll11ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1lll1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤឿ")
        global _1l111ll1l1l_opy_
        platform_index = os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫៀ")]
        bstack1l11l1111l1_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), bstack11l1l1lll1l_opy_)
        if not os.path.exists(bstack1l11l1111l1_opy_) or not os.path.isdir(bstack1l11l1111l1_opy_):
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥេ").format(bstack1l11l1111l1_opy_))
            return
        logs = hook.get(bstack1lll1l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦែ"), [])
        with os.scandir(bstack1l11l1111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111ll1l1l_opy_:
                    self.logger.info(bstack1lll1l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧៃ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1lll1l_opy_ (u"ࠣࠤោ")
                    log_entry = bstack1ll11ll1l1l_opy_(
                        kind=bstack1lll1l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦៅ"),
                        message=bstack1lll1l_opy_ (u"ࠥࠦំ"),
                        level=bstack1lll1l_opy_ (u"ࠦࠧះ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11l11llll_opy_=entry.stat().st_size,
                        bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧៈ"),
                        bstack1ll11ll_opy_=os.path.abspath(entry.path),
                        bstack11ll11l111l_opy_=hook.get(TestFramework.bstack11ll1111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l111ll1l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭៉")]
        bstack11l1ll1ll11_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), bstack11l1l1lll1l_opy_, bstack11l1ll1111l_opy_)
        if not os.path.exists(bstack11l1ll1ll11_opy_) or not os.path.isdir(bstack11l1ll1ll11_opy_):
            self.logger.info(bstack1lll1l_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤ៊").format(bstack11l1ll1ll11_opy_))
        else:
            self.logger.info(bstack1lll1l_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢ់").format(bstack11l1ll1ll11_opy_))
            with os.scandir(bstack11l1ll1ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111ll1l1l_opy_:
                        self.logger.info(bstack1lll1l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ៌").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1lll1l_opy_ (u"ࠥࠦ៍")
                        log_entry = bstack1ll11ll1l1l_opy_(
                            kind=bstack1lll1l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ៎"),
                            message=bstack1lll1l_opy_ (u"ࠧࠨ៏"),
                            level=bstack1lll1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ័"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11l11llll_opy_=entry.stat().st_size,
                            bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ៑"),
                            bstack1ll11ll_opy_=os.path.abspath(entry.path),
                            bstack1l111llll1l_opy_=hook.get(TestFramework.bstack11ll1111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l111ll1l1l_opy_.add(abs_path)
        hook[bstack1lll1l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ្")] = logs
    def bstack1l111l1lll1_opy_(
        self,
        bstack1l111ll1lll_opy_: bstack1ll111l1l1l_opy_,
        entries: List[bstack1ll11ll1l1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1lll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨ៓"))
        req.platform_index = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l1lll111_opy_)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ។").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l111ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l11l11l1ll_opy_)
            log_entry.uuid = entry.bstack11ll11l111l_opy_
            log_entry.test_framework_state = bstack1l111ll1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1lll1l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ៕"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1lll1l_opy_ (u"ࠧࠨ៖")
            if entry.kind == bstack1lll1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣៗ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11llll_opy_
                log_entry.file_path = entry.bstack1ll11ll_opy_
        def bstack1l11ll11ll1_opy_():
            bstack1l1l11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.LogCreatedEvent(req)
                bstack1l111ll1lll_opy_.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ៘"), datetime.now() - bstack1l1l11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1lll1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ៙").format(str(e)))
                traceback.print_exc()
        self.bstack1lll111111l_opy_.enqueue(bstack1l11ll11ll1_opy_)
    def __11ll1l1111l_opy_(self, instance) -> None:
        bstack1lll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ៚")
        bstack11ll11ll111_opy_ = {bstack1lll1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ៛"): bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll1l111ll_opy_(instance, bstack11ll11ll111_opy_)
    @staticmethod
    def bstack11l1ll1l1l1_opy_(instance: bstack1ll111l1l1l_opy_, bstack11ll1111ll1_opy_: str):
        bstack11l1ll11l11_opy_ = (
            bstack1l1ll1lll1l_opy_.bstack11ll11lll1l_opy_
            if bstack11ll1111ll1_opy_ == bstack1l1ll1lll1l_opy_.bstack11ll11111l1_opy_
            else bstack1l1ll1lll1l_opy_.bstack11l1ll1lll1_opy_
        )
        bstack11ll111l1l1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11ll1111ll1_opy_, None)
        bstack11ll11l1lll_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11l1ll11l11_opy_, None) if bstack11ll111l1l1_opy_ else None
        return (
            bstack11ll11l1lll_opy_[bstack11ll111l1l1_opy_][-1]
            if isinstance(bstack11ll11l1lll_opy_, dict) and len(bstack11ll11l1lll_opy_.get(bstack11ll111l1l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll11l1l1l_opy_(instance: bstack1ll111l1l1l_opy_, bstack11ll1111ll1_opy_: str):
        hook = bstack1l1ll1lll1l_opy_.bstack11l1ll1l1l1_opy_(instance, bstack11ll1111ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1l111l1_opy_, []).clear()
    @staticmethod
    def __11ll111llll_opy_(instance: bstack1ll111l1l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1lll1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤៜ"), None)):
            return
        if os.getenv(bstack1lll1l_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤ៝"), bstack1lll1l_opy_ (u"ࠨ࠱ࠣ៞")) != bstack1lll1l_opy_ (u"ࠢ࠲ࠤ៟"):
            bstack1l1ll1lll1l_opy_.logger.warning(bstack1lll1l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥ០"))
            return
        bstack11l1lll1111_opy_ = {
            bstack1lll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣ១"): (bstack1l1ll1lll1l_opy_.bstack11l1lll1lll_opy_, bstack1l1ll1lll1l_opy_.bstack11l1ll1lll1_opy_),
            bstack1lll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ២"): (bstack1l1ll1lll1l_opy_.bstack11ll11111l1_opy_, bstack1l1ll1lll1l_opy_.bstack11ll11lll1l_opy_),
        }
        for when in (bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ៣"), bstack1lll1l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥ៤"), bstack1lll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣ៥")):
            bstack11l1lllllll_opy_ = args[1].get_records(when)
            if not bstack11l1lllllll_opy_:
                continue
            records = [
                bstack1ll11ll1l1l_opy_(
                    kind=TestFramework.bstack1l111l1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1lll1l_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥ៦")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1lll1l_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤ៧")) and r.created
                        else None
                    ),
                )
                for r in bstack11l1lllllll_opy_
                if isinstance(getattr(r, bstack1lll1l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ៨"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll111l111_opy_, bstack11l1ll11l11_opy_ = bstack11l1lll1111_opy_.get(when, (None, None))
            bstack11ll1l1l1l1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11ll111l111_opy_, None) if bstack11ll111l111_opy_ else None
            bstack11ll11l1lll_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11l1ll11l11_opy_, None) if bstack11ll1l1l1l1_opy_ else None
            if isinstance(bstack11ll11l1lll_opy_, dict) and len(bstack11ll11l1lll_opy_.get(bstack11ll1l1l1l1_opy_, [])) > 0:
                hook = bstack11ll11l1lll_opy_[bstack11ll1l1l1l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1l111l1_opy_ in hook:
                    hook[TestFramework.bstack11ll1l111l1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1ll1111_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l1ll1lll1l_opy_.__11ll111ll1l_opy_(test.location) if hasattr(test, bstack1lll1l_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧ៩")) else getattr(test, bstack1lll1l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ៪"), None)
        test_name = test.name if hasattr(test, bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ៫")) else None
        bstack11l1llll111_opy_ = test.fspath.strpath if hasattr(test, bstack1lll1l_opy_ (u"ࠨࡦࡴࡲࡤࡸ࡭ࠨ៬")) and test.fspath else None
        if not test_id or not test_name or not bstack11l1llll111_opy_:
            return None
        code = None
        if hasattr(test, bstack1lll1l_opy_ (u"ࠢࡰࡤ࡭ࠦ៭")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l1l1lllll_opy_ = []
        try:
            bstack11l1l1lllll_opy_ = bstack111lllll1_opy_.bstack111111l1ll_opy_(test)
        except:
            bstack1l1ll1lll1l_opy_.logger.warning(bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠬࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡳࡧࡶࡳࡱࡼࡥࡥࠢ࡬ࡲࠥࡉࡌࡊࠤ៮"))
        return {
            TestFramework.bstack1l1l1l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11lllll1111_opy_: test_id,
            TestFramework.bstack1l1l111llll_opy_: test_name,
            TestFramework.bstack1l1111ll1l1_opy_: getattr(test, bstack1lll1l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ៯"), None),
            TestFramework.bstack11ll111lll1_opy_: bstack11l1llll111_opy_,
            TestFramework.bstack11l1lllll1l_opy_: bstack1l1ll1lll1l_opy_.__11ll111l1ll_opy_(test),
            TestFramework.bstack11ll1l11ll1_opy_: code,
            TestFramework.bstack1l1111111l1_opy_: TestFramework.bstack11l1ll1llll_opy_,
            TestFramework.bstack11lll1111l1_opy_: test_id,
            TestFramework.bstack11l1ll11111_opy_: bstack11l1l1lllll_opy_
        }
    @staticmethod
    def __11ll111l1ll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1lll1l_opy_ (u"ࠥࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠣ៰"), [])
            markers.extend([getattr(m, bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ៱"), None) for m in own_markers if getattr(m, bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ៲"), None)])
            current = getattr(current, bstack1lll1l_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨ៳"), None)
        return markers
    @staticmethod
    def __11ll111ll1l_opy_(location):
        return bstack1lll1l_opy_ (u"ࠢ࠻࠼ࠥ៴").join(filter(lambda x: isinstance(x, str), location))