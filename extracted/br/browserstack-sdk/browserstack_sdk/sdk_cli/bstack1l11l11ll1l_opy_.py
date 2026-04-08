# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1l1ll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1111l111l1_opy_ import bstack111l1llllll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11ll11l_opy_,
    TestHookState,
    bstack1ll1lll1l1l_opy_,
    bstack11lllllll1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1ll1lllll_opy_
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l11l_opy_ import bstack1l1ll1111ll_opy_
from bstack_utils.bstack1l1l1111_opy_ import bstack111l1l1l11_opy_
bstack11l1llll1l1_opy_ = bstack1l1ll1lllll_opy_()
bstack111ll111ll1_opy_ = 1.0
bstack11ll111llll_opy_ = bstack111l_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ᫑")
bstack111l1lll111_opy_ = bstack111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ᫒")
bstack111l1lll11l_opy_ = bstack111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ᫓")
bstack111l1lll1l1_opy_ = bstack111l_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦ᫔")
bstack111l1ll1ll1_opy_ = bstack111l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ᫕")
_11ll1111l1l_opy_ = set()
class bstack1l11l1l1ll1_opy_(TestFramework):
    bstack111l1ll11ll_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࡵࠥ᫖")
    bstack111ll11l111_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤ᫗")
    bstack111ll1lll11_opy_ = bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ᫘")
    bstack111ll111lll_opy_ = bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ᫙")
    bstack111ll1l1ll1_opy_ = bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ᫚")
    bstack111l1l1ll1l_opy_: bool
    bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_ = None
    bstack11l11lll11_opy_ = None
    bstack1l1l1l1lll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1lll1l111_opy_: Dict[str, str],
        bstack1l1ll1ll11l_opy_: List[str] = [bstack111l_opy_ (u"ࠣࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ᫛")],
        bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_ = None,
        bstack11l11lll11_opy_=None
    ):
        super().__init__(bstack1l1ll1ll11l_opy_, bstack1l1lll1l111_opy_, bstack1l1l1ll11l1_opy_)
        self.bstack111l1l1ll1l_opy_ = any(bstack111l_opy_ (u"ࠤࡵࡳࡧࡵࡴࠣ᫜") in item.lower() for item in bstack1l1ll1ll11l_opy_)
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
    def track_event(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l11l1l1ll1_opy_.bstack1l1l1l1lll1_opy_:
            bstack111l1llllll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠢ᫝").format(test_framework_state, test_hook_state))
            return
        if not self.bstack111l1l1ll1l_opy_:
            self.logger.warning(bstack111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࢀࢃࠢ᫞").format(str(self.bstack1l1ll1ll11l_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧ᫟").format(args, kwargs))
            return
        instance = self.__111lll11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠢ᫠").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l11l1l1ll1_opy_.bstack1l1l1l1lll1_opy_:
                bstack1l1l111lll_opy_ = bstack111l_opy_ (u"ࠢࠣ᫡")
                name = bstack111l_opy_ (u"ࠣࠤ᫢")
                if (test_hook_state == TestHookState.PRE):
                    bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111l1llll11_opy_.value)
                    name = str(EVENTS.bstack111l1llll11_opy_.name) + bstack111l_opy_ (u"ࠤ࠽ࠦ᫣") + str(test_framework_state.name)
                else:
                    bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack111l1lll1ll_opy_.value)
                    name = str(EVENTS.bstack111l1lll1ll_opy_.name) + bstack111l_opy_ (u"ࠥ࠾ࠧ᫤") + str(test_framework_state.name)
                TestFramework.bstack111ll1llll1_opy_(instance, name, bstack1l1l111lll_opy_)
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣ᫥").format(e))
        try:
            if not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1ll111l1l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l11l1l1ll1_opy_.__111l1l1llll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111l_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࢁ࠳ࢁࡽࠣ᫦").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࢀ࠲ࢀࢃࠢ᫧").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠨ᫨").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l11l1l1ll1_opy_.__111ll1lllll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111lll1lll1_opy_(instance, *args)
                self.__1l1l1l11l11_opy_(instance)
            elif test_framework_state in bstack1l11l1l1ll1_opy_.bstack1l1l1l1lll1_opy_:
                self.__111ll1111l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡿ࠱ࡿࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠦ᫩").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l1l11lll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l11l1l1ll1_opy_.bstack1l1l1l1lll1_opy_:
                bstack1l1l111lll_opy_ = bstack111l_opy_ (u"ࠤࠥ᫪")
                name = bstack111l_opy_ (u"ࠥࠦ᫫")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111l1llll11_opy_.name) + bstack111l_opy_ (u"ࠦ࠿ࠨ᫬") + str(test_framework_state.name)
                    bstack1l1l111lll_opy_ = TestFramework.bstack111ll1l1lll_opy_(instance, name)
                    bstack11lll11111_opy_.end(EVENTS.bstack111l1llll11_opy_.value, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᫭"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᫮"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111l1lll1ll_opy_.name) + bstack111l_opy_ (u"ࠢ࠻ࠤ᫯") + str(test_framework_state.name)
                    bstack1l1l111lll_opy_ = TestFramework.bstack111ll1l1lll_opy_(instance, name)
                    bstack11lll11111_opy_.end(EVENTS.bstack111l1lll1ll_opy_.value, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᫰"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᫱"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ᫲").format(e))
    def bstack1l1lll11111_opy_(self):
        return self.bstack111l1l1ll1l_opy_
    def bstack1l1l1llll1l_opy_(self):
        return False
    def __111l1l1l1l1_opy_(self, *args):
        bstack111l_opy_ (u"ࠦࠧࠨࡐࡢࡴࡶࡩࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡧࡶࡹࡱࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤ᫳")
        if len(args) > 1 and hasattr(args[1], bstack111l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᫴")):
            result = args[1]
            if result:
                return TestFramework.bstack11l1ll1ll11_opy_(result, [bstack111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨ᫵"), bstack111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ᫶"), bstack111l_opy_ (u"ࠣࡵࡷࡥࡷࡺࡴࡪ࡯ࡨࠦ᫷"), bstack111l_opy_ (u"ࠤࡨࡲࡩࡺࡩ࡮ࡧࠥ᫸"), bstack111l_opy_ (u"ࠥࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠣ᫹")])
        return None
    def __111lll1lll1_opy_(self, instance: bstack1l1l11ll11l_opy_, *args):
        result = self.__111l1l1l1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l1l1l_opy_ = None
        status = result.get(bstack111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᫺"), bstack111l_opy_ (u"ࠧࡔࡏࡕࠢࡕ࡙ࡓࠨ᫻"))
        if status == bstack111l_opy_ (u"ࠨࡆࡂࡋࡏࠦ᫼") and result.get(bstack111l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ᫽")):
            failure = [{bstack111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ᫾"): [result.get(bstack111l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥ᫿"), bstack111l_opy_ (u"ࠥࠦᬀ"))]}]
            bstack1ll111l1l1l_opy_ = bstack111l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᬁ")
        bstack111lll1l11l_opy_ = TestFramework.bstack1l1lll11l11_opy_
        if status == bstack111l_opy_ (u"ࠧࡖࡁࡔࡕࠥᬂ"):
            bstack111lll1l11l_opy_ = bstack111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᬃ")
        elif status == bstack111l_opy_ (u"ࠢࡇࡃࡌࡐࠧᬄ"):
            bstack111lll1l11l_opy_ = bstack111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᬅ")
        elif status == bstack111l_opy_ (u"ࠤࡖࡏࡎࡖࠢᬆ"):
            bstack111lll1l11l_opy_ = bstack111l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᬇ")
        if bstack111lll1l11l_opy_ != TestFramework.bstack1l1lll11l11_opy_:
            TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1l1l1111l_opy_(instance, {
            TestFramework.bstack1l1ll1111l1_opy_: failure,
            TestFramework.bstack1l1l1lll111_opy_: bstack1ll111l1l1l_opy_,
            TestFramework.bstack1l1ll1lll11_opy_: bstack111lll1l11l_opy_,
        })
    def __111lll11lll_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111l1ll1l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__111l1ll11l1_opy_(test) if test else None
                if target:
                    self.__111l1ll1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᬈ"), None)
            elif hasattr(args[0], bstack111l_opy_ (u"ࠧ࡯ࡤࠣᬉ")) if len(args) > 0 else False:
                target = args[0].id
            instance = TestFramework.bstack1l1l1l1l11l_opy_(target) if target else None
        return instance
    def __111ll1111l1_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1ll1l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l11l1l1ll1_opy_.bstack111ll11l111_opy_, {})
        if not key in bstack1l1ll1l11ll_opy_:
            bstack1l1ll1l11ll_opy_[key] = []
        bstack1l1l11lll11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l11l1l1ll1_opy_.bstack111ll1lll11_opy_, {})
        if not key in bstack1l1l11lll11_opy_:
            bstack1l1l11lll11_opy_[key] = []
        bstack1l1ll11l1l1_opy_ = {
            bstack1l11l1l1ll1_opy_.bstack111ll11l111_opy_: bstack1l1ll1l11ll_opy_,
            bstack1l11l1l1ll1_opy_.bstack111ll1lll11_opy_: bstack1l1l11lll11_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack111l_opy_ (u"ࠨࠢᬊ")
            if len(args) > 0 and hasattr(args[0], bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᬋ")):
                hook_name = args[0].name
            hook = {
                bstack111l_opy_ (u"ࠣ࡭ࡨࡽࠧᬌ"): key,
                TestFramework.bstack1l1ll11llll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1ll11ll1l_opy_: TestFramework.bstack1l1ll11lll1_opy_,
                TestFramework.bstack1l1l11llll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1ll11l111_opy_: [],
                TestFramework.bstack1l1ll11l1ll_opy_: hook_name,
                TestFramework.bstack111lll1l111_opy_: bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()
            }
            bstack1l1ll1l11ll_opy_[key].append(hook)
            bstack1l1ll11l1l1_opy_[bstack1l11l1l1ll1_opy_.bstack111ll111lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack1l1l1l1llll_opy_ = bstack1l1ll1l11ll_opy_.get(key, [])
            hook = bstack1l1l1l1llll_opy_.pop() if bstack1l1l1l1llll_opy_ else None
            if hook:
                result = self.__111l1l1l1l1_opy_(*args)
                if result:
                    bstack111ll11111l_opy_ = result.get(bstack111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᬍ"), TestFramework.bstack1l1ll11lll1_opy_)
                    if bstack111ll11111l_opy_ == bstack111l_opy_ (u"ࠥࡔࡆ࡙ࡓࠣᬎ"):
                        bstack111ll11111l_opy_ = bstack111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᬏ")
                    elif bstack111ll11111l_opy_ == bstack111l_opy_ (u"ࠧࡌࡁࡊࡎࠥᬐ"):
                        bstack111ll11111l_opy_ = bstack111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᬑ")
                    if bstack111ll11111l_opy_ != TestFramework.bstack1l1ll11lll1_opy_:
                        hook[TestFramework.bstack1l1ll11ll1l_opy_] = bstack111ll11111l_opy_
                hook[TestFramework.bstack1l1ll1ll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack111lll1l111_opy_] = bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()
                self.bstack111ll1lll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll1l1l1l_opy_, [])
                if logs:
                    self.bstack11l1lll11_opy_(instance, logs)
                bstack1l1l11lll11_opy_[key].append(hook)
                bstack1l1ll11l1l1_opy_[bstack1l11l1l1ll1_opy_.bstack111ll1l1ll1_opy_] = key
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾ࠰ࡾࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࡾࢁࠧᬒ").format(key, test_hook_state, bstack1l1ll1l11ll_opy_, bstack1l1l11lll11_opy_))
    def __111l1ll1l11_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111l_opy_ (u"ࠣࠤࠥࡘࡷࡧࡣ࡬ࠢࡕࡳࡧࡵࡴࠡࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࡸࡱࡵࡨࠥ࡫ࡶࡦࡰࡷࡷࠥ࠮ࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡴࡾࡺࡥࡴࡶࠣࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࠨࠢࠣᬓ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬔ"), None)
        bstack1l1llll1111_opy_ = getattr(keyword, bstack111l_opy_ (u"ࠥࡸࡾࡶࡥࠣᬕ"), None)
        test_id = kwargs.get(bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᬖ"), None)
        if not test_id:
            self.logger.debug(bstack111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡰ࡫ࡹࡸࡱࡵࡨࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡴ࡯ࠡࡶࡨࡷࡹࡥࡩࡥࠢ࡬ࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠢᬗ").format(keyword_name))
            return None
        instance = TestFramework.bstack1l1l1l1l11l_opy_(test_id)
        if not instance:
            self.logger.warning(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤࡱࡥࡺࡹࡲࡶࡩࡥࡥࡷࡧࡱࡸ࠿ࠦ࡮ࡰࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤ࡯ࡤ࠾ࡽࢀࠦᬘ").format(test_id))
            return None
        bstack111l1ll1111_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack1l11l1l1ll1_opy_.bstack111l1ll11ll_opy_, {})
        if os.getenv(bstack111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡋࡆ࡛࡚ࡓࡗࡊࡓࠣᬙ"), bstack111l_opy_ (u"ࠣ࠳ࠥᬚ")) == bstack111l_opy_ (u"ࠤ࠴ࠦᬛ"):
            bstack111l1ll111l_opy_ = bstack111l_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤᬜ").format(bstack1l1llll1111_opy_, keyword_name)
            bstack111lll11l11_opy_ = datetime.now(tz=timezone.utc)
            bstack111l1l1lll1_opy_ = {
                bstack111l_opy_ (u"ࠦࡰ࡫ࡹࠣᬝ"): bstack111l1ll111l_opy_,
                bstack111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬞ"): keyword_name,
                bstack111l_opy_ (u"ࠨࡴࡺࡲࡨࠦᬟ"): bstack1l1llll1111_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack111l1l1lll1_opy_[bstack111l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᬠ")] = uuid4().__str__()
                bstack111l1l1lll1_opy_[bstack1l11l1l1ll1_opy_.bstack1l1l11llll1_opy_] = bstack111lll11l11_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111l1l1lll1_opy_[bstack1l11l1l1ll1_opy_.bstack1l1ll1ll1ll_opy_] = bstack111lll11l11_opy_
                if len(args) > 1 and hasattr(args[1], bstack111l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᬡ")):
                    bstack111l1l1lll1_opy_[bstack111l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᬢ")] = args[1].status
            if bstack111l1ll111l_opy_ in bstack111l1ll1111_opy_:
                bstack111l1ll1111_opy_[bstack111l1ll111l_opy_].update(bstack111l1l1lll1_opy_)
                self.logger.debug(bstack111l_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡂࢁࡽࠡࡶࡼࡴࡪࡃࡻࡾࠤᬣ").format(keyword_name, bstack1l1llll1111_opy_))
            else:
                bstack111l1ll1111_opy_[bstack111l1ll111l_opy_] = bstack111l1l1lll1_opy_
                self.logger.debug(bstack111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡯ࡪࡿࡷࡰࡴࡧࡁࢀࢃࠠࡵࡻࡳࡩࡂࢁࡽࠣᬤ").format(keyword_name, bstack1l1llll1111_opy_))
        TestFramework.bstack1l11l1ll11_opy_(instance, bstack1l11l1l1ll1_opy_.bstack111l1ll11ll_opy_, bstack111l1ll1111_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤࡰ࡫ࡹࡸࡱࡵࡨࡸࡃࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠢᬥ").format(len(bstack111l1ll1111_opy_), instance.ref()))
        return instance
    def __111l1ll1l1l_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1l1ll1l1l_opy_.create_context(target)
        ob = bstack1l1l11ll11l_opy_(ctx, self.bstack1l1ll1ll11l_opy_, self.bstack1l1lll1l111_opy_, test_framework_state)
        TestFramework.bstack1l1l1l1111l_opy_(ob, {
            TestFramework.bstack1l1ll1l1l11_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1lll1l1_opy_: context.test_framework_version,
            TestFramework.bstack1l1l11lllll_opy_: [],
            bstack1l11l1l1ll1_opy_.bstack111l1ll11ll_opy_: {},
            bstack1l11l1l1ll1_opy_.bstack111ll1lll11_opy_: {},
            bstack1l11l1l1ll1_opy_.bstack111ll11l111_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack111l_opy_ (u"ࠨࡳࡰࡷࡵࡧࡪࠨᬦ")):
            TestFramework.bstack1l11l1ll11_opy_(ob, TestFramework.bstack111ll1l11l1_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1l11l1ll11_opy_(ob, TestFramework.bstack1l1l1l11ll1_opy_, context.platform_index)
        TestFramework.bstack1l111l111_opy_[ctx.id] = ob
        self.logger.debug(bstack111l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࢀࢃࠢᬧ").format(ctx.id, target, args, TestFramework.bstack1l111l111_opy_.keys()))
        return ob
    def bstack1l1lll1111l_opy_(self, instance: bstack1l1l11ll11l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11ll1_opy_ = (
            bstack1l11l1l1ll1_opy_.bstack111ll111lll_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else bstack1l11l1l1ll1_opy_.bstack111ll1l1ll1_opy_
        )
        hook = bstack1l11l1l1ll1_opy_.bstack111ll1ll1l1_opy_(instance, bstack111lll11ll1_opy_)
        entries = hook.get(TestFramework.bstack1l1ll11l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, []))
        return entries
    def bstack1l1l1l11111_opy_(self, instance: bstack1l1l11ll11l_opy_, bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack111lll11ll1_opy_ = (
            bstack1l11l1l1ll1_opy_.bstack111ll111lll_opy_
            if bstack1l1l1lllll1_opy_[1] == TestHookState.PRE
            else bstack1l11l1l1ll1_opy_.bstack111ll1l1ll1_opy_
        )
        bstack1l11l1l1ll1_opy_.bstack111ll11ll11_opy_(instance, bstack111lll11ll1_opy_)
        TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, []).clear()
    def bstack111ll1lll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᬨ")
        global _11ll1111l1l_opy_
        platform_index = os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᬩ")]
        bstack1l1l1l1l1ll_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), bstack111l1lll1l1_opy_)
        if not os.path.exists(bstack1l1l1l1l1ll_opy_) or not os.path.isdir(bstack1l1l1l1l1ll_opy_):
            self.logger.debug(bstack111l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᬪ").format(bstack1l1l1l1l1ll_opy_))
            return
        logs = hook.get(bstack111l_opy_ (u"ࠦࡱࡵࡧࡴࠤᬫ"), [])
        with os.scandir(bstack1l1l1l1l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll1111l1l_opy_:
                    self.logger.info(bstack111l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᬬ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l_opy_ (u"ࠨࠢᬭ")
                    log_entry = bstack11lllllll1_opy_(
                        kind=bstack111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᬮ"),
                        message=bstack111l_opy_ (u"ࠣࠤᬯ"),
                        level=bstack111l_opy_ (u"ࠤࠥᬰ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                        bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᬱ"),
                        bstack1lllllll_opy_=os.path.abspath(entry.path),
                        bstack111ll1ll1ll_opy_=hook.get(TestFramework.bstack1l1ll11llll_opy_)
                    )
                    logs.append(log_entry)
                    _11ll1111l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᬲ")]
        bstack111llll1111_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), bstack111l1lll1l1_opy_, bstack111l1ll1ll1_opy_)
        if not os.path.exists(bstack111llll1111_opy_) or not os.path.isdir(bstack111llll1111_opy_):
            self.logger.info(bstack111l_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᬳ").format(bstack111llll1111_opy_))
        else:
            self.logger.info(bstack111l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁ᬴ࠧ").format(bstack111llll1111_opy_))
            with os.scandir(bstack111llll1111_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll1111l1l_opy_:
                        self.logger.info(bstack111l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᬵ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l_opy_ (u"ࠣࠤᬶ")
                        log_entry = bstack11lllllll1_opy_(
                            kind=bstack111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᬷ"),
                            message=bstack111l_opy_ (u"ࠥࠦᬸ"),
                            level=bstack111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᬹ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                            bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᬺ"),
                            bstack1lllllll_opy_=os.path.abspath(entry.path),
                            bstack11ll1111111_opy_=hook.get(TestFramework.bstack1l1ll11llll_opy_)
                        )
                        logs.append(log_entry)
                        _11ll1111l1l_opy_.add(abs_path)
        hook[bstack111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᬻ")] = logs
    def bstack11l1lll11_opy_(
        self,
        bstack1lll1l1lll_opy_: bstack1l1l11ll11l_opy_,
        entries: List[bstack11lllllll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᬼ"))
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1l11ll1_opy_)
        req.client_worker_id = bstack111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᬽ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1lll1l1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1lll1l1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1lll1l1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1ll1l1l11_opy_, bstack111l_opy_ (u"ࠤࠥᬾ"))
            log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1lll1l1_opy_, bstack111l_opy_ (u"ࠥࠦᬿ"))
            log_entry.uuid = entry.bstack111ll1ll1ll_opy_ or bstack111l_opy_ (u"ࠦࠧᭀ")
            log_entry.test_framework_state = bstack1lll1l1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᭁ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111l_opy_ (u"ࠨࠢᭂ")
            if entry.kind == bstack111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᭃ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack11ll11l1ll1_opy_():
            bstack1lllllll1ll_opy_ = datetime.now()
            try:
                self.bstack11l11lll11_opy_.LogCreatedEvent(req)
                bstack1lll1l1lll_opy_.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸ᭄ࠧ"), datetime.now() - bstack1lllllll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᭅ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1l1ll11l1_opy_.enqueue(bstack11ll11l1ll1_opy_)
    def __1l1l1l11l11_opy_(self, instance) -> None:
        bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᭆ")
        bstack1l1ll11l1l1_opy_ = {bstack111l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᭇ"): bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
    @staticmethod
    def bstack111ll1ll1l1_opy_(instance: bstack1l1l11ll11l_opy_, bstack111lll11ll1_opy_: str):
        bstack111ll11l1ll_opy_ = (
            bstack1l11l1l1ll1_opy_.bstack111ll1lll11_opy_
            if bstack111lll11ll1_opy_ == bstack1l11l1l1ll1_opy_.bstack111ll1l1ll1_opy_
            else bstack1l11l1l1ll1_opy_.bstack111ll11l111_opy_
        )
        bstack111lll11l1l_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111lll11ll1_opy_, None)
        bstack111ll1l1l11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11l1ll_opy_, None) if bstack111lll11l1l_opy_ else None
        return (
            bstack111ll1l1l11_opy_[bstack111lll11l1l_opy_][-1]
            if isinstance(bstack111ll1l1l11_opy_, dict) and len(bstack111ll1l1l11_opy_.get(bstack111lll11l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack111ll11ll11_opy_(instance: bstack1l1l11ll11l_opy_, bstack111lll11ll1_opy_: str):
        hook = bstack1l11l1l1ll1_opy_.bstack111ll1ll1l1_opy_(instance, bstack111lll11ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1ll11l111_opy_, []).clear()
    @staticmethod
    def __111ll1lllll_opy_(instance: bstack1l1l11ll11l_opy_, *args):
        bstack111l_opy_ (u"ࠧࠨࠢࡑࡴࡲࡧࡪࡹࡳࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࡴࠤࠥࠦᭈ")
        if len(args) < 1:
            return
        if os.getenv(bstack111l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᭉ"), bstack111l_opy_ (u"ࠢ࠲ࠤᭊ")) != bstack111l_opy_ (u"ࠣ࠳ࠥᭋ"):
            bstack1l11l1l1ll1_opy_.logger.warning(bstack111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡰࡴ࡭ࡳࠣᭌ"))
            return
        message = args[0]
        if not hasattr(message, bstack111l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ᭍")):
            return
        is_screenshot = hasattr(message, bstack111l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ᭎")) and message.kind == bstack111l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩ᭏")
        log_entry = bstack11lllllll1_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack11l1lllll11_opy_,
            message=message.message if hasattr(message, bstack111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᭐")) else bstack111l_opy_ (u"ࠢࠣ᭑"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack111l_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢ᭒")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack111l_opy_ (u"ࠤࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠢ᭓")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack111l_opy_ (u"ࠥࡸ࡮ࡳࡥࡴࡶࡤࡱࡵࠨ᭔")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack111lll1111l_opy_ = {
            bstack111l_opy_ (u"ࠦࡘࡋࡔࡖࡒࠥ᭕"): (bstack1l11l1l1ll1_opy_.bstack111ll111lll_opy_, bstack1l11l1l1ll1_opy_.bstack111ll11l111_opy_),
            bstack111l_opy_ (u"࡚ࠧࡅࡂࡔࡇࡓ࡜ࡔࠢ᭖"): (bstack1l11l1l1ll1_opy_.bstack111ll1l1ll1_opy_, bstack1l11l1l1ll1_opy_.bstack111ll1lll11_opy_),
        }
        bstack111l1l1ll11_opy_ = None
        if len(args) > 1:
            bstack111l1l1ll11_opy_ = args[1]
        if bstack111l1l1ll11_opy_ and bstack111l1l1ll11_opy_ in bstack111lll1111l_opy_:
            bstack111ll11l11l_opy_, bstack111ll11l1ll_opy_ = bstack111lll1111l_opy_[bstack111l1l1ll11_opy_]
            bstack111lll1llll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11l11l_opy_, None)
            bstack111ll1l1l11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111ll11l1ll_opy_, None) if bstack111lll1llll_opy_ else None
            if isinstance(bstack111ll1l1l11_opy_, dict) and len(bstack111ll1l1l11_opy_.get(bstack111lll1llll_opy_, [])) > 0:
                hook = bstack111ll1l1l11_opy_[bstack111lll1llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1ll11l111_opy_ in hook:
                    hook[TestFramework.bstack1l1ll11l111_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __111l1l1llll_opy_(test) -> Dict[str, Any]:
        bstack111l_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡓࡱࡥࡳࡹࠦࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡷࡩࡸࡺࠠࡰࡤ࡭ࡩࡨࡺࠢࠣࠤ᭗")
        test_id = bstack1l11l1l1ll1_opy_.__111l1ll11l1_opy_(test)
        test_name = test.name if hasattr(test, bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭘")) else None
        bstack111ll11llll_opy_ = str(test.source) if hasattr(test, bstack111l_opy_ (u"ࠣࡵࡲࡹࡷࡩࡥࠣ᭙")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack111l_opy_ (u"ࠤࡷࡥ࡬ࡹࠢ᭚")) else []
        bstack111l1l1l1ll_opy_ =bstack111l_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧ᭛").format(bstack111l_opy_ (u"ࠦࠥࠨ᭜").join(test_tags), test_name) if test_tags else test_name
        bstack111l1ll1lll_opy_ = []
        if bstack111ll11llll_opy_:
            from browserstack_sdk.bstack1lll1l1llll_opy_ import RobotHandler
            bstack111l1ll1lll_opy_ = RobotHandler.bstack1lll1ll1l11_opy_(bstack111ll11llll_opy_)
        if not bstack111l1ll1lll_opy_ and test_name:
            bstack111l1ll1lll_opy_ = [test_name]
        return {
            TestFramework.bstack1l1l1lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1ll111l1l_opy_: test_id,
            TestFramework.bstack1l1ll1lll1l_opy_: test_name,
            TestFramework.bstack1l1ll11ll11_opy_: test_id,
            TestFramework.bstack1l1ll111lll_opy_: bstack111ll11llll_opy_,
            TestFramework.bstack1l1ll1ll1l1_opy_: test_tags,
            TestFramework.bstack1l1ll111l11_opy_: bstack111l1l1l1ll_opy_,
            TestFramework.bstack1l1ll1lll11_opy_: TestFramework.bstack1l1lll11l11_opy_,
            TestFramework.bstack1l1l1lll1ll_opy_: test_id,
            TestFramework.bstack1l1l1l1ll1l_opy_: bstack111l1ll1lll_opy_
        }
    @staticmethod
    def __111l1ll11l1_opy_(test):
        bstack111l_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡺࡴࡩࡲࡷࡨࠤࡹ࡫ࡳࡵࠢࡌࡈࠥ࡬ࡲࡰ࡯ࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡺࡥࡴࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧ᭝")
        if hasattr(test, bstack111l_opy_ (u"ࠨࡩࡥࠤ᭞")):
            return test.id
        elif hasattr(test, bstack111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡳࡧ࡭ࡦࠤ᭟")):
            return test.longname
        elif hasattr(test, bstack111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭠")):
            return test.name
        return None