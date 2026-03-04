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
bstack1l111l1l111_opy_ = bstack1lll1l_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣ៵")
bstack11l1l1llll1_opy_ = bstack1lll1l_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧ៶")
bstack11l1l1lll11_opy_ = bstack1lll1l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ៷")
bstack11l1l1lll1l_opy_ = bstack1lll1l_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢ៸")
bstack11l1ll1111l_opy_ = bstack1lll1l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ៹")
_1l111ll1l1l_opy_ = set()
class bstack1l1ll1lllll_opy_(TestFramework):
    bstack11l1l1l1ll1_opy_ = bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨ៺")
    bstack11l1ll1lll1_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧ៻")
    bstack11ll11lll1l_opy_ = bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢ៼")
    bstack11l1lll1lll_opy_ = bstack1lll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦ៽")
    bstack11ll11111l1_opy_ = bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨ៾")
    bstack11l1l1ll1l1_opy_: bool
    bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_ = None
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
        bstack1l1l1ll1l1l_opy_: List[str] = [bstack1lll1l_opy_ (u"ࠦࡷࡵࡢࡰࡶࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠧ៿")],
        bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_ = None,
        bstack1lll111lll1_opy_=None
    ):
        super().__init__(bstack1l1l1ll1l1l_opy_, bstack11l1llll1ll_opy_, bstack1lll111111l_opy_)
        self.bstack11l1l1ll1l1_opy_ = any(bstack1lll1l_opy_ (u"ࠧࡸ࡯ࡣࡱࡷࠦ᠀") in item.lower() for item in bstack1l1l1ll1l1l_opy_)
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
    def track_event(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l1ll1lllll_opy_.bstack11l1lll11l1_opy_:
            bstack11ll11l1ll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥ᠁").format(test_framework_state, test_hook_state))
            return
        if not self.bstack11l1l1ll1l1_opy_:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࡼࡿࠥ᠂").format(str(self.bstack1l1l1ll1l1l_opy_)))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁࡽࠣ᠃").format(args, kwargs))
            return
        instance = self.__11ll11ll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠥ᠄").format(test_framework_state, test_hook_state, args))
            return
        try:
            if instance != None and test_framework_state in bstack1l1ll1lllll_opy_.bstack11l1lll11l1_opy_:
                bstack1ll111111l_opy_ = bstack1lll1l_opy_ (u"ࠥࠦ᠅")
                name = bstack1lll1l_opy_ (u"ࠦࠧ᠆")
                if (test_hook_state == TestHookState.PRE):
                    bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11l1ll111ll_opy_.value)
                    name = str(EVENTS.bstack11l1ll111ll_opy_.name) + bstack1lll1l_opy_ (u"ࠧࡀࠢ᠇") + str(test_framework_state.name)
                else:
                    bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack11l1ll111l1_opy_.value)
                    name = str(EVENTS.bstack11l1ll111l1_opy_.name) + bstack1lll1l_opy_ (u"ࠨ࠺ࠣ᠈") + str(test_framework_state.name)
                TestFramework.bstack11ll1l11l1l_opy_(instance, name, bstack1ll111111l_opy_)
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦ᠉").format(e))
        try:
            if not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack11lllll1111_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l1ll1lllll_opy_.__11l1l1ll11l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥࡷࡧࡱࡸࡂࢁࡽ࠯ࡽࢀࠦ᠊").format(instance.ref(), test_framework_state, test_hook_state))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l111l11l1l_opy_):
                    TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l111l11l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࢃ࠮ࡼࡿࠥ᠋").format(instance.ref(), test_framework_state, test_hook_state))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_):
                    TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠤ᠌").format(instance.ref(), test_framework_state, test_hook_state))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l1ll1lllll_opy_.__11ll111llll_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__11ll1111l11_opy_(instance, *args)
                self.__11ll1l1111l_opy_(instance)
            elif test_framework_state in bstack1l1ll1lllll_opy_.bstack11l1lll11l1_opy_:
                self.__11ll11llll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࢂ࠴ࡻࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠢ᠍").format(test_framework_state, test_hook_state, instance.ref()))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1ll1l11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance != None and test_framework_state in bstack1l1ll1lllll_opy_.bstack11l1lll11l1_opy_:
                bstack1ll111111l_opy_ = bstack1lll1l_opy_ (u"ࠧࠨ᠎")
                name = bstack1lll1l_opy_ (u"ࠨࠢ᠏")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack11l1ll111ll_opy_.name) + bstack1lll1l_opy_ (u"ࠢ࠻ࠤ᠐") + str(test_framework_state.name)
                    bstack1ll111111l_opy_ = TestFramework.bstack11ll111111l_opy_(instance, name)
                    bstack1l11l11ll1_opy_.end(EVENTS.bstack11l1ll111ll_opy_.value, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᠑"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᠒"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1ll111l1_opy_.name) + bstack1lll1l_opy_ (u"ࠥ࠾ࠧ᠓") + str(test_framework_state.name)
                    bstack1ll111111l_opy_ = TestFramework.bstack11ll111111l_opy_(instance, name)
                    bstack1l11l11ll1_opy_.end(EVENTS.bstack11l1ll111l1_opy_.value, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᠔"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᠕"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨ᠖").format(e))
    def bstack1l11l1l11l1_opy_(self):
        return self.bstack11l1l1ll1l1_opy_
    def bstack1l11l111lll_opy_(self):
        return False
    def __11l1l1l1111_opy_(self, *args):
        bstack1lll1l_opy_ (u"ࠢࠣࠤࡓࡥࡷࡹࡥࠡࡔࡲࡦࡴࡺࠠࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡶࡪࡹࡵ࡭ࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧ᠗")
        if len(args) > 1 and hasattr(args[1], bstack1lll1l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ᠘")):
            result = args[1]
            if result:
                return TestFramework.bstack1l111l1l1l1_opy_(result, [bstack1lll1l_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ᠙"), bstack1lll1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦ᠚"), bstack1lll1l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡷ࡭ࡲ࡫ࠢ᠛"), bstack1lll1l_opy_ (u"ࠧ࡫࡮ࡥࡶ࡬ࡱࡪࠨ᠜"), bstack1lll1l_opy_ (u"ࠨࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠦ᠝")])
        return None
    def __11ll1111l11_opy_(self, instance: bstack1ll111l1l1l_opy_, *args):
        result = self.__11l1l1l1111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll111l_opy_ = None
        status = result.get(bstack1lll1l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᠞"), bstack1lll1l_opy_ (u"ࠣࡐࡒࡘࠥࡘࡕࡏࠤ᠟"))
        if status == bstack1lll1l_opy_ (u"ࠤࡉࡅࡎࡒࠢᠠ") and result.get(bstack1lll1l_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᠡ")):
            failure = [{bstack1lll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᠢ"): [result.get(bstack1lll1l_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᠣ"), bstack1lll1l_opy_ (u"ࠨࠢᠤ"))]}]
            bstack1lll1ll111l_opy_ = bstack1lll1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᠥ")
        bstack11ll1l1l111_opy_ = TestFramework.bstack11l1ll1llll_opy_
        if status == bstack1lll1l_opy_ (u"ࠣࡒࡄࡗࡘࠨᠦ"):
            bstack11ll1l1l111_opy_ = bstack1lll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᠧ")
        elif status == bstack1lll1l_opy_ (u"ࠥࡊࡆࡏࡌࠣᠨ"):
            bstack11ll1l1l111_opy_ = bstack1lll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᠩ")
        elif status == bstack1lll1l_opy_ (u"࡙ࠧࡋࡊࡒࠥᠪ"):
            bstack11ll1l1l111_opy_ = bstack1lll1l_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᠫ")
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
            instance = self.__11l1l1l1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None
            if test_framework_state == TestFrameworkState.INIT_TEST:
                test = args[0] if len(args) > 0 else None
                target = self.__11l1l1l11l1_opy_(test) if test else None
                if target:
                    self.__11l1l1ll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                target = kwargs.get(bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᠬ"), None)
            elif hasattr(args[0], bstack1lll1l_opy_ (u"ࠣ࡫ࡧࠦᠭ")) if len(args) > 0 else False:
                target = args[0].id
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
        bstack11l1lll1l11_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack1l1ll1lllll_opy_.bstack11l1ll1lll1_opy_, {})
        if not key in bstack11l1lll1l11_opy_:
            bstack11l1lll1l11_opy_[key] = []
        bstack11l1llllll1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack1l1ll1lllll_opy_.bstack11ll11lll1l_opy_, {})
        if not key in bstack11l1llllll1_opy_:
            bstack11l1llllll1_opy_[key] = []
        bstack11ll11ll111_opy_ = {
            bstack1l1ll1lllll_opy_.bstack11l1ll1lll1_opy_: bstack11l1lll1l11_opy_,
            bstack1l1ll1lllll_opy_.bstack11ll11lll1l_opy_: bstack11l1llllll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook_name = bstack1lll1l_opy_ (u"ࠤࠥᠮ")
            if len(args) > 0 and hasattr(args[0], bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᠯ")):
                hook_name = args[0].name
            hook = {
                bstack1lll1l_opy_ (u"ࠦࡰ࡫ࡹࠣᠰ"): key,
                TestFramework.bstack11ll1111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11l1llll11l_opy_: TestFramework.bstack11ll11ll1ll_opy_,
                TestFramework.bstack11ll1l1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1l111l1_opy_: [],
                TestFramework.bstack11ll1111l1l_opy_: hook_name,
                TestFramework.bstack11ll11l11ll_opy_: bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()
            }
            bstack11l1lll1l11_opy_[key].append(hook)
            bstack11ll11ll111_opy_[bstack1l1ll1lllll_opy_.bstack11l1lll1lll_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11ll11l1111_opy_ = bstack11l1lll1l11_opy_.get(key, [])
            hook = bstack11ll11l1111_opy_.pop() if bstack11ll11l1111_opy_ else None
            if hook:
                result = self.__11l1l1l1111_opy_(*args)
                if result:
                    bstack11l1ll1l1ll_opy_ = result.get(bstack1lll1l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᠱ"), TestFramework.bstack11ll11ll1ll_opy_)
                    if bstack11l1ll1l1ll_opy_ == bstack1lll1l_opy_ (u"ࠨࡐࡂࡕࡖࠦᠲ"):
                        bstack11l1ll1l1ll_opy_ = bstack1lll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᠳ")
                    elif bstack11l1ll1l1ll_opy_ == bstack1lll1l_opy_ (u"ࠣࡈࡄࡍࡑࠨᠴ"):
                        bstack11l1ll1l1ll_opy_ = bstack1lll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᠵ")
                    if bstack11l1ll1l1ll_opy_ != TestFramework.bstack11ll11ll1ll_opy_:
                        hook[TestFramework.bstack11l1llll11l_opy_] = bstack11l1ll1l1ll_opy_
                hook[TestFramework.bstack11l1llll1l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll11l11ll_opy_] = bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()
                self.bstack11l1lll11ll_opy_(hook)
                logs = hook.get(TestFramework.bstack11l1ll11ll1_opy_, [])
                if logs:
                    self.bstack1l111l1lll1_opy_(instance, logs)
                bstack11l1llllll1_opy_[key].append(hook)
                bstack11ll11ll111_opy_[bstack1l1ll1lllll_opy_.bstack11ll11111l1_opy_] = key
        TestFramework.bstack11ll1l111ll_opy_(instance, bstack11ll11ll111_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁ࠳ࢁࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࢁࡽࠣᠶ").format(key, test_hook_state, bstack11l1lll1l11_opy_, bstack11l1llllll1_opy_))
    def __11l1l1l1lll_opy_(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1lll1l_opy_ (u"ࠦࠧࠨࡔࡳࡣࡦ࡯ࠥࡘ࡯ࡣࡱࡷࠤࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡬ࡧࡼࡻࡴࡸࡤࠡࡧࡹࡩࡳࡺࡳࠡࠪࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡰࡺࡶࡨࡷࡹࠦࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࠤࠥࠦᠷ")
        keyword = args[0] if len(args) > 0 else None
        if not keyword:
            return None
        keyword_name = getattr(keyword, bstack1lll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᠸ"), None)
        bstack1lll111llll_opy_ = getattr(keyword, bstack1lll1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᠹ"), None)
        test_id = kwargs.get(bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᠺ"), None)
        if not test_id:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟࡬ࡧࡼࡻࡴࡸࡤࡠࡧࡹࡩࡳࡺ࠺ࠡࡰࡲࠤࡹ࡫ࡳࡵࡡ࡬ࡨࠥ࡯࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠥᠻ").format(keyword_name))
            return None
        instance = TestFramework.bstack1ll1l1l111l_opy_(test_id)
        if not instance:
            self.logger.warning(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠ࡭ࡨࡽࡼࡵࡲࡥࡡࡨࡺࡪࡴࡴ࠻ࠢࡱࡳࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡸࡪࡹࡴࡠ࡫ࡧࡁࢀࢃࠢᠼ").format(test_id))
            return None
        bstack11l1l1l111l_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack1l1ll1lllll_opy_.bstack11l1l1l1ll1_opy_, {})
        if os.getenv(bstack1lll1l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡎࡉ࡞࡝ࡏࡓࡆࡖࠦᠽ"), bstack1lll1l_opy_ (u"ࠦ࠶ࠨᠾ")) == bstack1lll1l_opy_ (u"ࠧ࠷ࠢᠿ"):
            bstack11l1l1ll111_opy_ = bstack1lll1l_opy_ (u"ࠨࡻࡾ࠼ࡾࢁࠧᡀ").format(bstack1lll111llll_opy_, keyword_name)
            bstack11ll11l11l1_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1l1l1l1l_opy_ = {
                bstack1lll1l_opy_ (u"ࠢ࡬ࡧࡼࠦᡁ"): bstack11l1l1ll111_opy_,
                bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᡂ"): keyword_name,
                bstack1lll1l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᡃ"): bstack1lll111llll_opy_,
            }
            if test_hook_state == TestHookState.PRE:
                bstack11l1l1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᡄ")] = uuid4().__str__()
                bstack11l1l1l1l1l_opy_[bstack1l1ll1lllll_opy_.bstack11ll1l1l1ll_opy_] = bstack11ll11l11l1_opy_
            elif test_hook_state == TestHookState.POST:
                bstack11l1l1l1l1l_opy_[bstack1l1ll1lllll_opy_.bstack11l1llll1l1_opy_] = bstack11ll11l11l1_opy_
                if len(args) > 1 and hasattr(args[1], bstack1lll1l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᡅ")):
                    bstack11l1l1l1l1l_opy_[bstack1lll1l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᡆ")] = args[1].status
            if bstack11l1l1ll111_opy_ in bstack11l1l1l111l_opy_:
                bstack11l1l1l111l_opy_[bstack11l1l1ll111_opy_].update(bstack11l1l1l1l1l_opy_)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠ࡬ࡧࡼࡻࡴࡸࡤ࠾ࡽࢀࠤࡹࡿࡰࡦ࠿ࡾࢁࠧᡇ").format(keyword_name, bstack1lll111llll_opy_))
            else:
                bstack11l1l1l111l_opy_[bstack11l1l1ll111_opy_] = bstack11l1l1l1l1l_opy_
                self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦ࡫ࡦࡻࡺࡳࡷࡪ࠽ࡼࡿࠣࡸࡾࡶࡥ࠾ࡽࢀࠦᡈ").format(keyword_name, bstack1lll111llll_opy_))
        TestFramework.bstack1lll1l11lll_opy_(instance, bstack1l1ll1lllll_opy_.bstack11l1l1l1ll1_opy_, bstack11l1l1l111l_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠ࡬ࡧࡼࡻࡴࡸࡤࡴ࠿ࡾࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠥᡉ").format(len(bstack11l1l1l111l_opy_), instance.ref()))
        return instance
    def __11l1l1ll1ll_opy_(
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
            bstack1l1ll1lllll_opy_.bstack11l1l1l1ll1_opy_: {},
            bstack1l1ll1lllll_opy_.bstack11ll11lll1l_opy_: {},
            bstack1l1ll1lllll_opy_.bstack11l1ll1lll1_opy_: {},
        })
        test = args[0] if len(args) > 0 else None
        if test and hasattr(test, bstack1lll1l_opy_ (u"ࠤࡶࡳࡺࡸࡣࡦࠤᡊ")):
            TestFramework.bstack1lll1l11lll_opy_(ob, TestFramework.bstack11ll11lll11_opy_, str(test.source))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l11lll_opy_(ob, TestFramework.bstack1l1l1lll111_opy_, context.platform_index)
        TestFramework.bstack1lll1l1111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࡼࡿࠥᡋ").format(ctx.id, target, args, TestFramework.bstack1lll1l1111l_opy_.keys()))
        return ob
    def bstack1l11ll1l11l_opy_(self, instance: bstack1ll111l1l1l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111ll1_opy_ = (
            bstack1l1ll1lllll_opy_.bstack11l1lll1lll_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1l1ll1lllll_opy_.bstack11ll11111l1_opy_
        )
        hook = bstack1l1ll1lllll_opy_.bstack11l1ll1l1l1_opy_(instance, bstack11ll1111ll1_opy_)
        entries = hook.get(TestFramework.bstack11ll1l111l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, []))
        return entries
    def bstack1l11l1lll11_opy_(self, instance: bstack1ll111l1l1l_opy_, bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11ll1111ll1_opy_ = (
            bstack1l1ll1lllll_opy_.bstack11l1lll1lll_opy_
            if bstack1ll1ll1ll1l_opy_[1] == TestHookState.PRE
            else bstack1l1ll1lllll_opy_.bstack11ll11111l1_opy_
        )
        bstack1l1ll1lllll_opy_.bstack11ll11l1l1l_opy_(instance, bstack11ll1111ll1_opy_)
        TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, []).clear()
    def bstack11l1lll11ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1lll1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᡌ")
        global _1l111ll1l1l_opy_
        platform_index = os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᡍ")]
        bstack1l11l1111l1_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), bstack11l1l1lll1l_opy_)
        if not os.path.exists(bstack1l11l1111l1_opy_) or not os.path.isdir(bstack1l11l1111l1_opy_):
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦᡎ").format(bstack1l11l1111l1_opy_))
            return
        logs = hook.get(bstack1lll1l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᡏ"), [])
        with os.scandir(bstack1l11l1111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111ll1l1l_opy_:
                    self.logger.info(bstack1lll1l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᡐ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1lll1l_opy_ (u"ࠤࠥᡑ")
                    log_entry = bstack1ll11ll1l1l_opy_(
                        kind=bstack1lll1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᡒ"),
                        message=bstack1lll1l_opy_ (u"ࠦࠧᡓ"),
                        level=bstack1lll1l_opy_ (u"ࠧࠨᡔ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11l11llll_opy_=entry.stat().st_size,
                        bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᡕ"),
                        bstack1ll11ll_opy_=os.path.abspath(entry.path),
                        bstack11ll11l111l_opy_=hook.get(TestFramework.bstack11ll1111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l111ll1l1l_opy_.add(abs_path)
        platform_index = os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᡖ")]
        bstack11l1ll1ll11_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), bstack11l1l1lll1l_opy_, bstack11l1ll1111l_opy_)
        if not os.path.exists(bstack11l1ll1ll11_opy_) or not os.path.isdir(bstack11l1ll1ll11_opy_):
            self.logger.info(bstack1lll1l_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᡗ").format(bstack11l1ll1ll11_opy_))
        else:
            self.logger.info(bstack1lll1l_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᡘ").format(bstack11l1ll1ll11_opy_))
            with os.scandir(bstack11l1ll1ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111ll1l1l_opy_:
                        self.logger.info(bstack1lll1l_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᡙ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1lll1l_opy_ (u"ࠦࠧᡚ")
                        log_entry = bstack1ll11ll1l1l_opy_(
                            kind=bstack1lll1l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᡛ"),
                            message=bstack1lll1l_opy_ (u"ࠨࠢᡜ"),
                            level=bstack1lll1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᡝ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11l11llll_opy_=entry.stat().st_size,
                            bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᡞ"),
                            bstack1ll11ll_opy_=os.path.abspath(entry.path),
                            bstack1l111llll1l_opy_=hook.get(TestFramework.bstack11ll1111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l111ll1l1l_opy_.add(abs_path)
        hook[bstack1lll1l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᡟ")] = logs
    def bstack1l111l1lll1_opy_(
        self,
        bstack1l111ll1lll_opy_: bstack1ll111l1l1l_opy_,
        entries: List[bstack1ll11ll1l1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1lll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᡠ"))
        req.platform_index = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l1lll111_opy_)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᡡ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l111ll1l_opy_, bstack1lll1l_opy_ (u"ࠧࠨᡢ"))
            log_entry.test_framework_version = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l11l11l1ll_opy_, bstack1lll1l_opy_ (u"ࠨࠢᡣ"))
            log_entry.uuid = entry.bstack11ll11l111l_opy_ or bstack1lll1l_opy_ (u"ࠢࠣᡤ")
            log_entry.test_framework_state = bstack1l111ll1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1lll1l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᡥ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1lll1l_opy_ (u"ࠤࠥᡦ")
            if entry.kind == bstack1lll1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᡧ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11llll_opy_
                log_entry.file_path = entry.bstack1ll11ll_opy_
        def bstack1l11ll11ll1_opy_():
            bstack1l1l11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.LogCreatedEvent(req)
                bstack1l111ll1lll_opy_.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᡨ"), datetime.now() - bstack1l1l11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1lll1l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᡩ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll111111l_opy_.enqueue(bstack1l11ll11ll1_opy_)
    def __11ll1l1111l_opy_(self, instance) -> None:
        bstack1lll1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᡪ")
        bstack11ll11ll111_opy_ = {bstack1lll1l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᡫ"): bstack1l1ll1ll1ll_opy_.bstack11ll1l11111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll1l111ll_opy_(instance, bstack11ll11ll111_opy_)
    @staticmethod
    def bstack11l1ll1l1l1_opy_(instance: bstack1ll111l1l1l_opy_, bstack11ll1111ll1_opy_: str):
        bstack11l1ll11l11_opy_ = (
            bstack1l1ll1lllll_opy_.bstack11ll11lll1l_opy_
            if bstack11ll1111ll1_opy_ == bstack1l1ll1lllll_opy_.bstack11ll11111l1_opy_
            else bstack1l1ll1lllll_opy_.bstack11l1ll1lll1_opy_
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
        hook = bstack1l1ll1lllll_opy_.bstack11l1ll1l1l1_opy_(instance, bstack11ll1111ll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1l111l1_opy_, []).clear()
    @staticmethod
    def __11ll111llll_opy_(instance: bstack1ll111l1l1l_opy_, *args):
        bstack1lll1l_opy_ (u"ࠣࠤࠥࡔࡷࡵࡣࡦࡵࡶࠤࡗࡵࡢࡰࡶࠣࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡬ࡰࡩࠣࡱࡪࡹࡳࡢࡩࡨࡷࠧࠨࠢᡬ")
        if len(args) < 1:
            return
        if os.getenv(bstack1lll1l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᡭ"), bstack1lll1l_opy_ (u"ࠥ࠵ࠧᡮ")) != bstack1lll1l_opy_ (u"ࠦ࠶ࠨᡯ"):
            bstack1l1ll1lllll_opy_.logger.warning(bstack1lll1l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦ࡬ࡰࡩࡶࠦᡰ"))
            return
        message = args[0]
        if not hasattr(message, bstack1lll1l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᡱ")):
            return
        is_screenshot = hasattr(message, bstack1lll1l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᡲ")) and message.kind == bstack1lll1l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᡳ")
        log_entry = bstack1ll11ll1l1l_opy_(
            kind=TestFramework.KIND_SCREENSHOT if is_screenshot else TestFramework.bstack1l111l1l1ll_opy_,
            message=message.message if hasattr(message, bstack1lll1l_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᡴ")) else bstack1lll1l_opy_ (u"ࠥࠦᡵ"),
            level=None if is_screenshot else (message.level if hasattr(message, bstack1lll1l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥᡶ")) else None),
            timestamp=(
                datetime.strptime(message.timestamp, bstack1lll1l_opy_ (u"࡙ࠧࠫࠦ࡯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠥᡷ")).replace(tzinfo=timezone.utc)
                if hasattr(message, bstack1lll1l_opy_ (u"ࠨࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠤᡸ")) and message.timestamp
                else datetime.now(tz=timezone.utc)
            ),
        )
        bstack11l1lll1111_opy_ = {
            bstack1lll1l_opy_ (u"ࠢࡔࡇࡗ࡙ࡕࠨ᡹"): (bstack1l1ll1lllll_opy_.bstack11l1lll1lll_opy_, bstack1l1ll1lllll_opy_.bstack11l1ll1lll1_opy_),
            bstack1lll1l_opy_ (u"ࠣࡖࡈࡅࡗࡊࡏࡘࡐࠥ᡺"): (bstack1l1ll1lllll_opy_.bstack11ll11111l1_opy_, bstack1l1ll1lllll_opy_.bstack11ll11lll1l_opy_),
        }
        bstack11l1l1l1l11_opy_ = None
        if len(args) > 1:
            bstack11l1l1l1l11_opy_ = args[1]
        if bstack11l1l1l1l11_opy_ and bstack11l1l1l1l11_opy_ in bstack11l1lll1111_opy_:
            bstack11ll111l111_opy_, bstack11l1ll11l11_opy_ = bstack11l1lll1111_opy_[bstack11l1l1l1l11_opy_]
            bstack11ll1l1l1l1_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11ll111l111_opy_, None)
            bstack11ll11l1lll_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, bstack11l1ll11l11_opy_, None) if bstack11ll1l1l1l1_opy_ else None
            if isinstance(bstack11ll11l1lll_opy_, dict) and len(bstack11ll11l1lll_opy_.get(bstack11ll1l1l1l1_opy_, [])) > 0:
                hook = bstack11ll11l1lll_opy_[bstack11ll1l1l1l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1l111l1_opy_ in hook:
                    hook[TestFramework.bstack11ll1l111l1_opy_].append(log_entry)
                    return
        logs = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack11l1ll11l1l_opy_, [])
        logs.append(log_entry)
    @staticmethod
    def __11l1l1ll11l_opy_(test) -> Dict[str, Any]:
        bstack1lll1l_opy_ (u"ࠤࠥࠦࡕࡧࡲࡴࡧࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡺࡥࡴࡶࠣࡳࡧࡰࡥࡤࡶࠥࠦࠧ᡻")
        test_id = bstack1l1ll1lllll_opy_.__11l1l1l11l1_opy_(test)
        test_name = test.name if hasattr(test, bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᡼")) else None
        bstack11l1llll111_opy_ = str(test.source) if hasattr(test, bstack1lll1l_opy_ (u"ࠦࡸࡵࡵࡳࡥࡨࠦ᡽")) else None
        if not test_id or not test_name:
            return None
        test_tags = list(test.tags) if hasattr(test, bstack1lll1l_opy_ (u"ࠧࡺࡡࡨࡵࠥ᡾")) else []
        bstack11l1l1l11ll_opy_ =bstack1lll1l_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣ᡿").format(bstack1lll1l_opy_ (u"ࠢࠡࠤᢀ").join(test_tags), test_name) if test_tags else test_name
        bstack11l1l1lllll_opy_ = []
        if bstack11l1llll111_opy_:
            from browserstack_sdk.bstack1llllll1lll_opy_ import RobotHandler
            bstack11l1l1lllll_opy_ = RobotHandler.bstack111111l1ll_opy_(bstack11l1llll111_opy_)
        if not bstack11l1l1lllll_opy_ and test_name:
            bstack11l1l1lllll_opy_ = [test_name]
        return {
            TestFramework.bstack1l1l1l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack11lllll1111_opy_: test_id,
            TestFramework.bstack1l1l111llll_opy_: test_name,
            TestFramework.bstack1l1111ll1l1_opy_: test_id,
            TestFramework.bstack11ll111lll1_opy_: bstack11l1llll111_opy_,
            TestFramework.bstack11l1lllll1l_opy_: test_tags,
            TestFramework.bstack11ll1l11ll1_opy_: bstack11l1l1l11ll_opy_,
            TestFramework.bstack1l1111111l1_opy_: TestFramework.bstack11l1ll1llll_opy_,
            TestFramework.bstack11lll1111l1_opy_: test_id,
            TestFramework.bstack11l1ll11111_opy_: bstack11l1l1lllll_opy_
        }
    @staticmethod
    def __11l1l1l11l1_opy_(test):
        bstack1lll1l_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡶࡰ࡬ࡵࡺ࡫ࠠࡵࡧࡶࡸࠥࡏࡄࠡࡨࡵࡳࡲࠦࡒࡰࡤࡲࡸࠥࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡶࡨࡷࡹࠦ࡯ࡣ࡬ࡨࡧࡹࠨࠢࠣᢁ")
        if hasattr(test, bstack1lll1l_opy_ (u"ࠤ࡬ࡨࠧᢂ")):
            return test.id
        elif hasattr(test, bstack1lll1l_opy_ (u"ࠥࡰࡴࡴࡧ࡯ࡣࡰࡩࠧᢃ")):
            return test.longname
        elif hasattr(test, bstack1lll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᢄ")):
            return test.name
        return None