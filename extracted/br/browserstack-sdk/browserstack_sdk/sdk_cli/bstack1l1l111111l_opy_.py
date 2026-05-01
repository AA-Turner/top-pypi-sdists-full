# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1l1ll1l1lll_opy_ import bstack1l1ll1l1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1llllll_opy_ import bstack111ll1ll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1ll11l1_opy_,
    TestHookState,
    bstack1ll1lllll1l_opy_,
    bstack11l1l1l1ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack11ll11l1lll_opy_
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1lll1111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l11ll1l1_opy_ import bstack1l11ll1111l_opy_
from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
bstack11ll11l1ll1_opy_ = bstack11ll11l1lll_opy_()
bstack111llll1l1l_opy_ = 1.0
bstack11ll1ll1l11_opy_ = bstack111ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᧆ")
bstack111ll1111ll_opy_ = bstack111ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᧇ")
bstack111l1llll11_opy_ = bstack111ll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᧈ")
bstack111l1lllll1_opy_ = bstack111ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᧉ")
bstack111l1llll1l_opy_ = bstack111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ᧊")
_11ll111lll1_opy_ = set()
class bstack1l11lll11l1_opy_(TestFramework):
    bstack111lll1l11l_opy_ = bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ᧋")
    bstack111ll1l1ll1_opy_ = bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ᧌")
    bstack111lll11l1l_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ᧍")
    bstack111lllll11l_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢ᧎")
    bstack111llll1ll1_opy_ = bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤ᧏")
    bstack11l1111ll1l_opy_: bool
    bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_  = None
    bstack111111ll1l_opy_ = None
    bstack111llll111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll11l_opy_: Dict[str, str],
        bstack1l1l11l1111_opy_: List[str]=[bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢ᧐")],
        bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_=None,
        bstack111111ll1l_opy_=None
    ):
        super().__init__(bstack1l1l11l1111_opy_, bstack1l11llll11l_opy_, bstack1l1ll1llll1_opy_)
        self.bstack11l1111ll1l_opy_ = any(bstack111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣ᧑") in item.lower() for item in bstack1l1l11l1111_opy_)
        self.bstack111111ll1l_opy_ = bstack111111ll1l_opy_
    def track_event(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.TEST or test_framework_state in bstack1l11lll11l1_opy_.bstack111llll111l_opy_:
            bstack111ll1ll1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == TestFrameworkState.NONE:
            self.logger.warning(bstack111ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥ᧒") + str(test_hook_state) + bstack111ll_opy_ (u"ࠥࠦ᧓"))
            return
        if not self.bstack11l1111ll1l_opy_:
            self.logger.warning(bstack111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧ᧔") + str(str(self.bstack1l1l11l1111_opy_)) + bstack111ll_opy_ (u"ࠧࠨ᧕"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᧖") + str(kwargs) + bstack111ll_opy_ (u"ࠢࠣ᧗"))
            return
        instance = self.__11l11111lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢ᧘") + str(args) + bstack111ll_opy_ (u"ࠤࠥ᧙"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l11lll11l1_opy_.bstack111llll111l_opy_:
                bstack11111l11l_opy_ = bstack111ll_opy_ (u"ࠥࠦ᧚")
                name = bstack111ll_opy_ (u"ࠦࠧ᧛")
                if (test_hook_state == TestHookState.PRE):
                    bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111l1llllll_opy_.value)
                    name = str(EVENTS.bstack111l1llllll_opy_.name)+bstack111ll_opy_ (u"ࠧࡀࠢ᧜")+str(test_framework_state.name)
                else:
                    bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111ll1111l1_opy_.value)
                    name = str(EVENTS.bstack111ll1111l1_opy_.name)+bstack111ll_opy_ (u"ࠨ࠺ࠣ᧝")+str(test_framework_state.name)
                TestFramework.bstack111ll1l1l1l_opy_(instance, name, bstack11111l11l_opy_)
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦ᧞").format(e))
        try:
            if not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_) and test_hook_state == TestHookState.PRE:
                test = bstack1l11lll11l1_opy_.__111lll11111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111ll_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣ᧟") + str(test_hook_state) + bstack111ll_opy_ (u"ࠤࠥ᧠"))
            if test_framework_state == TestFrameworkState.TEST:
                if test_hook_state == TestHookState.PRE and not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣ᧡") + str(test_hook_state) + bstack111ll_opy_ (u"ࠦࠧ᧢"))
                elif test_hook_state == TestHookState.POST and not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11llll_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11lll11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111ll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣ᧣") + str(test_hook_state) + bstack111ll_opy_ (u"ࠨࠢ᧤"))
            elif test_framework_state == TestFrameworkState.LOG and test_hook_state == TestHookState.POST:
                bstack1l11lll11l1_opy_.__111lll1ll11_opy_(instance, *args)
            elif test_framework_state == TestFrameworkState.LOG_REPORT and test_hook_state == TestHookState.POST:
                self.__111ll1ll111_opy_(instance, *args)
                self.__111llll11l1_opy_(instance)
            elif test_framework_state in bstack1l11lll11l1_opy_.bstack111llll111l_opy_:
                self.__111ll11l1l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣ᧥") + str(instance.ref()) + bstack111ll_opy_ (u"ࠣࠤ᧦"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack111ll1l1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l11lll11l1_opy_.bstack111llll111l_opy_:
                bstack11111l11l_opy_ = bstack111ll_opy_ (u"ࠤࠥ᧧")
                name = bstack111ll_opy_ (u"ࠥࠦ᧨")
                if (test_hook_state == TestHookState.PRE):
                    name = str(EVENTS.bstack111l1llllll_opy_.name)+bstack111ll_opy_ (u"ࠦ࠿ࠨ᧩")+str(test_framework_state.name)
                    bstack11111l11l_opy_ = TestFramework.bstack111ll1lllll_opy_(instance, name)
                    bstack111l1l1l_opy_.end(EVENTS.bstack111l1llllll_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᧪"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᧫"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack111ll1111l1_opy_.name)+bstack111ll_opy_ (u"ࠢ࠻ࠤ᧬")+str(test_framework_state.name)
                    bstack11111l11l_opy_ = TestFramework.bstack111ll1lllll_opy_(instance, name)
                    bstack111l1l1l_opy_.end(EVENTS.bstack111ll1111l1_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᧭"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᧮"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ᧯").format(e))
    def bstack11ll1l111ll_opy_(self):
        return self.bstack11l1111ll1l_opy_
    def bstack11ll1ll1l1l_opy_(self):
        return False
    def __11l1111lll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣ᧰"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack11lll1111ll_opy_(rep, [bstack111ll_opy_ (u"ࠧࡽࡨࡦࡰࠥ᧱"), bstack111ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᧲"), bstack111ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ᧳"), bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ᧴"), bstack111ll_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥ᧵"), bstack111ll_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤ᧶")])
        return None
    def __111ll1ll111_opy_(self, instance: bstack1l1l1ll11l1_opy_, *args):
        result = self.__11l1111lll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1ll111l111l_opy_ = None
        if result.get(bstack111ll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᧷"), None) == bstack111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᧸") and len(args) > 1 and getattr(args[1], bstack111ll_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢ᧹"), None) is not None:
            failure = [{bstack111ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ᧺"): [args[1].excinfo.exconly(), result.get(bstack111ll_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢ᧻"), None)]}]
            bstack1ll111l111l_opy_ = bstack111ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ᧼") if bstack111ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ᧽") in getattr(args[1].excinfo, bstack111ll_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨ᧾"), bstack111ll_opy_ (u"ࠧࠨ᧿")) else bstack111ll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᨀ")
        bstack111llllll1l_opy_ = result.get(bstack111ll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᨁ"), TestFramework.bstack11l11111111_opy_)
        if bstack111llllll1l_opy_ != TestFramework.bstack11l11111111_opy_:
            TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11lll11111l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11l11111l11_opy_(instance, {
            TestFramework.bstack11l1l1ll1ll_opy_: failure,
            TestFramework.bstack111lll1l1l1_opy_: bstack1ll111l111l_opy_,
            TestFramework.bstack11l1ll11l11_opy_: bstack111llllll1l_opy_,
        })
    def __11l11111lll_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
            instance = self.__111ll1l1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1111l1l_opy_ bstack111ll111l11_opy_ this to be bstack111ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᨂ")
            if test_framework_state == TestFrameworkState.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__111lllllll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == TestFrameworkState.LOG:
                nodeid = getattr(getattr(args[0], bstack111ll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᨃ"), None), bstack111ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᨄ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᨅ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1l1llllll_opy_(target) if target else None
        return instance
    def __111ll11l1l1_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
    ):
        key = test_framework_state.name
        bstack111ll1l1lll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack1l11lll11l1_opy_.bstack111ll1l1ll1_opy_, {})
        if not key in bstack111ll1l1lll_opy_:
            bstack111ll1l1lll_opy_[key] = []
        bstack111lll111l1_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack1l11lll11l1_opy_.bstack111lll11l1l_opy_, {})
        if not key in bstack111lll111l1_opy_:
            bstack111lll111l1_opy_[key] = []
        bstack111llllllll_opy_ = {
            bstack1l11lll11l1_opy_.bstack111ll1l1ll1_opy_: bstack111ll1l1lll_opy_,
            bstack1l11lll11l1_opy_.bstack111lll11l1l_opy_: bstack111lll111l1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack111ll_opy_ (u"ࠧࡱࡥࡺࠤᨆ"): key,
                TestFramework.bstack111llll1111_opy_: uuid4().__str__(),
                TestFramework.bstack111ll1l11l1_opy_: TestFramework.bstack111lll1lll1_opy_,
                TestFramework.bstack111lll1llll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll11l111_opy_: [],
                TestFramework.bstack111ll11ll1l_opy_: args[1] if len(args) > 1 else bstack111ll_opy_ (u"࠭ࠧᨇ"),
                TestFramework.bstack11l11111l1l_opy_: bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()
            }
            bstack111ll1l1lll_opy_[key].append(hook)
            bstack111llllllll_opy_[bstack1l11lll11l1_opy_.bstack111lllll11l_opy_] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l111l111l_opy_ = bstack111ll1l1lll_opy_.get(key, [])
            hook = bstack11l111l111l_opy_.pop() if bstack11l111l111l_opy_ else None
            if hook:
                result = self.__11l1111lll1_opy_(*args)
                if result:
                    bstack111ll11l11l_opy_ = result.get(bstack111ll_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᨈ"), TestFramework.bstack111lll1lll1_opy_)
                    if bstack111ll11l11l_opy_ != TestFramework.bstack111lll1lll1_opy_:
                        hook[TestFramework.bstack111ll1l11l1_opy_] = bstack111ll11l11l_opy_
                hook[TestFramework.bstack111llll1l11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11l11111l1l_opy_]= bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()
                self.bstack111lll1l1ll_opy_(hook)
                logs = hook.get(TestFramework.bstack111ll111lll_opy_, [])
                if logs: self.bstack1l1111ll1l_opy_(instance, logs)
                bstack111lll111l1_opy_[key].append(hook)
                bstack111llllllll_opy_[bstack1l11lll11l1_opy_.bstack111llll1ll1_opy_] = key
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᨉ") + str(bstack111lll111l1_opy_) + bstack111ll_opy_ (u"ࠤࠥᨊ"))
    def __111ll1l1111_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack11lll1111ll_opy_(args[0], [bstack111ll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᨋ"), bstack111ll_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᨌ"), bstack111ll_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᨍ"), bstack111ll_opy_ (u"ࠨࡩࡥࡵࠥᨎ"), bstack111ll_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᨏ"), bstack111ll_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᨐ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack111ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᨑ")) else fixturedef.get(bstack111ll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᨒ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111ll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᨓ")) else None
        node = request.node if hasattr(request, bstack111ll_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᨔ")) else None
        target = request.node.nodeid if hasattr(node, bstack111ll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᨕ")) else None
        baseid = fixturedef.get(bstack111ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᨖ"), None) or bstack111ll_opy_ (u"ࠣࠤᨗ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111ll_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳᨘࠢ")):
            target = bstack1l11lll11l1_opy_.__11l1111llll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111ll_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᨙ")) else None
            if target and not TestFramework.bstack1l1l1llllll_opy_(target):
                self.__111lllllll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᨚ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠧࠨᨛ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦ᨜") + str(target) + bstack111ll_opy_ (u"ࠢࠣ᨝"))
            return None
        instance = TestFramework.bstack1l1l1llllll_opy_(target)
        if not instance:
            self.logger.warning(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥ᨞") + str(target) + bstack111ll_opy_ (u"ࠤࠥ᨟"))
            return None
        bstack111ll1ll11l_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack1l11lll11l1_opy_.bstack111lll1l11l_opy_, {})
        if os.getenv(bstack111ll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᨠ"), bstack111ll_opy_ (u"ࠦ࠶ࠨᨡ")) == bstack111ll_opy_ (u"ࠧ࠷ࠢᨢ"):
            bstack11l111111l1_opy_ = bstack111ll_opy_ (u"ࠨ࠺ࠣᨣ").join((scope, fixturename))
            bstack11l111111ll_opy_ = datetime.now(tz=timezone.utc)
            bstack111ll1ll1ll_opy_ = {
                bstack111ll_opy_ (u"ࠢ࡬ࡧࡼࠦᨤ"): bstack11l111111l1_opy_,
                bstack111ll_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᨥ"): bstack1l11lll11l1_opy_.__111ll1l11ll_opy_(request.node),
                bstack111ll_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᨦ"): fixturedef,
                bstack111ll_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᨧ"): scope,
                bstack111ll_opy_ (u"ࠦࡹࡿࡰࡦࠤᨨ"): None,
            }
            try:
                if test_hook_state == TestHookState.POST and callable(getattr(args[-1], bstack111ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᨩ"), None)):
                    bstack111ll1ll1ll_opy_[bstack111ll_opy_ (u"ࠨࡴࡺࡲࡨࠦᨪ")] = TestFramework.bstack11ll1l11l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == TestHookState.PRE:
                bstack111ll1ll1ll_opy_[bstack111ll_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᨫ")] = uuid4().__str__()
                bstack111ll1ll1ll_opy_[bstack1l11lll11l1_opy_.bstack111lll1llll_opy_] = bstack11l111111ll_opy_
            elif test_hook_state == TestHookState.POST:
                bstack111ll1ll1ll_opy_[bstack1l11lll11l1_opy_.bstack111llll1l11_opy_] = bstack11l111111ll_opy_
            if bstack11l111111l1_opy_ in bstack111ll1ll11l_opy_:
                bstack111ll1ll11l_opy_[bstack11l111111l1_opy_].update(bstack111ll1ll1ll_opy_)
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᨬ") + str(bstack111ll1ll11l_opy_[bstack11l111111l1_opy_]) + bstack111ll_opy_ (u"ࠤࠥᨭ"))
            else:
                bstack111ll1ll11l_opy_[bstack11l111111l1_opy_] = bstack111ll1ll1ll_opy_
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᨮ") + str(len(bstack111ll1ll11l_opy_)) + bstack111ll_opy_ (u"ࠦࠧᨯ"))
        TestFramework.bstack11ll11l1_opy_(instance, bstack1l11lll11l1_opy_.bstack111lll1l11l_opy_, bstack111ll1ll11l_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᨰ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠨࠢᨱ"))
        return instance
    def __111lllllll1_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        target: Any,
        *args,
    ):
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        ob = bstack1l1l1ll11l1_opy_(ctx, self.bstack1l1l11l1111_opy_, self.bstack1l11llll11l_opy_, test_framework_state)
        TestFramework.bstack11l11111l11_opy_(ob, {
            TestFramework.bstack1l1111l111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll1l11l1l_opy_: context.test_framework_version,
            TestFramework.bstack111lll1ll1l_opy_: [],
            bstack1l11lll11l1_opy_.bstack111lll1l11l_opy_: {},
            bstack1l11lll11l1_opy_.bstack111lll11l1l_opy_: {},
            bstack1l11lll11l1_opy_.bstack111ll1l1ll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11ll11l1_opy_(ob, TestFramework.bstack11l1111l1l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11ll11l1_opy_(ob, TestFramework.bstack1l111111111_opy_, context.platform_index)
        TestFramework.bstack111l11l1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᨲ") + str(TestFramework.bstack111l11l1l1_opy_.keys()) + bstack111ll_opy_ (u"ࠣࠤᨳ"))
        return ob
    def bstack11lll111l1l_opy_(self, instance: bstack1l1l1ll11l1_opy_, bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1111l11l_opy_ = (
            bstack1l11lll11l1_opy_.bstack111lllll11l_opy_
            if bstack1l1l1lll11l_opy_[1] == TestHookState.PRE
            else bstack1l11lll11l1_opy_.bstack111llll1ll1_opy_
        )
        hook = bstack1l11lll11l1_opy_.bstack111ll11ll11_opy_(instance, bstack11l1111l11l_opy_)
        entries = hook.get(TestFramework.bstack111ll11l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, []))
        return entries
    def bstack11lll11l1ll_opy_(self, instance: bstack1l1l1ll11l1_opy_, bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        bstack11l1111l11l_opy_ = (
            bstack1l11lll11l1_opy_.bstack111lllll11l_opy_
            if bstack1l1l1lll11l_opy_[1] == TestHookState.PRE
            else bstack1l11lll11l1_opy_.bstack111llll1ll1_opy_
        )
        bstack1l11lll11l1_opy_.bstack11l1111111l_opy_(instance, bstack11l1111l11l_opy_)
        TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, []).clear()
    def bstack111lll1l1ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᨴ")
        global _11ll111lll1_opy_
        platform_index = os.environ[bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᨵ")]
        bstack11ll11lllll_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), bstack111l1lllll1_opy_)
        if not os.path.exists(bstack11ll11lllll_opy_) or not os.path.isdir(bstack11ll11lllll_opy_):
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤᨶ").format(bstack11ll11lllll_opy_))
            return
        logs = hook.get(bstack111ll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᨷ"), [])
        with os.scandir(bstack11ll11lllll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _11ll111lll1_opy_:
                    self.logger.info(bstack111ll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᨸ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111ll_opy_ (u"ࠢࠣᨹ")
                    log_entry = bstack11l1l1l1ll_opy_(
                        kind=bstack111ll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᨺ"),
                        message=bstack111ll_opy_ (u"ࠤࠥᨻ"),
                        level=bstack111ll_opy_ (u"ࠥࠦᨼ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack11ll1lll111_opy_=entry.stat().st_size,
                        bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᨽ"),
                        bstack111l1_opy_=os.path.abspath(entry.path),
                        bstack111llllll11_opy_=hook.get(TestFramework.bstack111llll1111_opy_)
                    )
                    logs.append(log_entry)
                    _11ll111lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᨾ")]
        bstack111lllll1l1_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), bstack111l1lllll1_opy_, bstack111l1llll1l_opy_)
        if not os.path.exists(bstack111lllll1l1_opy_) or not os.path.isdir(bstack111lllll1l1_opy_):
            self.logger.info(bstack111ll_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᨿ").format(bstack111lllll1l1_opy_))
        else:
            self.logger.info(bstack111ll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᩀ").format(bstack111lllll1l1_opy_))
            with os.scandir(bstack111lllll1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _11ll111lll1_opy_:
                        self.logger.info(bstack111ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᩁ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111ll_opy_ (u"ࠤࠥᩂ")
                        log_entry = bstack11l1l1l1ll_opy_(
                            kind=bstack111ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᩃ"),
                            message=bstack111ll_opy_ (u"ࠦࠧᩄ"),
                            level=bstack111ll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᩅ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack11ll1lll111_opy_=entry.stat().st_size,
                            bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᩆ"),
                            bstack111l1_opy_=os.path.abspath(entry.path),
                            bstack11lll11ll1l_opy_=hook.get(TestFramework.bstack111llll1111_opy_)
                        )
                        logs.append(log_entry)
                        _11ll111lll1_opy_.add(abs_path)
        hook[bstack111ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᩇ")] = logs
    def bstack1l1111ll1l_opy_(
        self,
        bstack1llllllll_opy_: bstack1l1l1ll11l1_opy_,
        entries: List[bstack11l1l1l1ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᩈ"))
        req.platform_index = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l111111111_opy_)
        req.client_worker_id = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᩉ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1llllllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1llllllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1llllllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l1111l111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack11ll1l11l1l_opy_)
            log_entry.uuid = entry.bstack111llllll11_opy_
            log_entry.test_framework_state = bstack1llllllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᩊ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111ll_opy_ (u"ࠦࠧᩋ")
            if entry.kind == bstack111ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᩌ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1lll111_opy_
                log_entry.file_path = entry.bstack111l1_opy_
        def bstack11lll111lll_opy_():
            bstack1l11111lll_opy_ = datetime.now()
            try:
                self.bstack111111ll1l_opy_.LogCreatedEvent(req)
                bstack1llllllll_opy_.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᩍ"), datetime.now() - bstack1l11111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᩎ").format(str(e)))
                traceback.print_exc()
        self.bstack1l1ll1llll1_opy_.enqueue(bstack11lll111lll_opy_)
    def __111llll11l1_opy_(self, instance) -> None:
        bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᩏ")
        bstack111llllllll_opy_ = {bstack111ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᩐ"): bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        bstack1l11ll1111l_opy_.bstack111lll11lll_opy_()
    @staticmethod
    def bstack111ll11ll11_opy_(instance: bstack1l1l1ll11l1_opy_, bstack11l1111l11l_opy_: str):
        bstack111lll1111l_opy_ = (
            bstack1l11lll11l1_opy_.bstack111lll11l1l_opy_
            if bstack11l1111l11l_opy_ == bstack1l11lll11l1_opy_.bstack111llll1ll1_opy_
            else bstack1l11lll11l1_opy_.bstack111ll1l1ll1_opy_
        )
        bstack11l1111ll11_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack11l1111l11l_opy_, None)
        bstack111lllll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1111l_opy_, None) if bstack11l1111ll11_opy_ else None
        return (
            bstack111lllll1ll_opy_[bstack11l1111ll11_opy_][-1]
            if isinstance(bstack111lllll1ll_opy_, dict) and len(bstack111lllll1ll_opy_.get(bstack11l1111ll11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1111111l_opy_(instance: bstack1l1l1ll11l1_opy_, bstack11l1111l11l_opy_: str):
        hook = bstack1l11lll11l1_opy_.bstack111ll11ll11_opy_(instance, bstack11l1111l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack111ll11l111_opy_, []).clear()
    @staticmethod
    def __111lll1ll11_opy_(instance: bstack1l1l1ll11l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᩑ"), None)):
            return
        if os.getenv(bstack111ll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᩒ"), bstack111ll_opy_ (u"ࠧ࠷ࠢᩓ")) != bstack111ll_opy_ (u"ࠨ࠱ࠣᩔ"):
            bstack1l11lll11l1_opy_.logger.warning(bstack111ll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᩕ"))
            return
        bstack111llll11ll_opy_ = {
            bstack111ll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᩖ"): (bstack1l11lll11l1_opy_.bstack111lllll11l_opy_, bstack1l11lll11l1_opy_.bstack111ll1l1ll1_opy_),
            bstack111ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᩗ"): (bstack1l11lll11l1_opy_.bstack111llll1ll1_opy_, bstack1l11lll11l1_opy_.bstack111lll11l1l_opy_),
        }
        for when in (bstack111ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᩘ"), bstack111ll_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᩙ"), bstack111ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᩚ")):
            bstack111ll111l1l_opy_ = args[1].get_records(when)
            if not bstack111ll111l1l_opy_:
                continue
            records = [
                bstack11l1l1l1ll_opy_(
                    kind=TestFramework.bstack11ll1l1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111ll_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᩛ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111ll_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᩜ")) and r.created
                        else None
                    ),
                )
                for r in bstack111ll111l1l_opy_
                if isinstance(getattr(r, bstack111ll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᩝ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack111lll1l111_opy_, bstack111lll1111l_opy_ = bstack111llll11ll_opy_.get(when, (None, None))
            bstack11l111l1111_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1l111_opy_, None) if bstack111lll1l111_opy_ else None
            bstack111lllll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111lll1111l_opy_, None) if bstack11l111l1111_opy_ else None
            if isinstance(bstack111lllll1ll_opy_, dict) and len(bstack111lllll1ll_opy_.get(bstack11l111l1111_opy_, [])) > 0:
                hook = bstack111lllll1ll_opy_[bstack11l111l1111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack111ll11l111_opy_ in hook:
                    hook[TestFramework.bstack111ll11l111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __111lll11111_opy_(test) -> Dict[str, Any]:
        test_id = bstack1l11lll11l1_opy_.__11l1111llll_opy_(test.location) if hasattr(test, bstack111ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᩞ")) else getattr(test, bstack111ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᩟"), None)
        test_name = test.name if hasattr(test, bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩠")) else None
        bstack11l1111l111_opy_ = test.fspath.strpath if hasattr(test, bstack111ll_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᩡ")) and test.fspath else None
        if not test_id or not test_name or not bstack11l1111l111_opy_:
            return None
        code = None
        if hasattr(test, bstack111ll_opy_ (u"ࠨ࡯ࡣ࡬ࠥᩢ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack111ll11111l_opy_ = []
        try:
            bstack111ll11111l_opy_ = bstack111ll111_opy_.bstack1lll1l1l1l1_opy_(test)
        except:
            bstack1l11lll11l1_opy_.logger.warning(bstack111ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᩣ"))
        return {
            TestFramework.bstack1l11111111l_opy_: uuid4().__str__(),
            TestFramework.bstack11l1l1ll11l_opy_: test_id,
            TestFramework.bstack1l1111lll11_opy_: test_name,
            TestFramework.bstack11l1llll111_opy_: getattr(test, bstack111ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᩤ"), None),
            TestFramework.bstack11l1111l1ll_opy_: bstack11l1111l111_opy_,
            TestFramework.bstack111ll1llll1_opy_: bstack1l11lll11l1_opy_.__111ll1l11ll_opy_(test),
            TestFramework.bstack111ll11l1ll_opy_: code,
            TestFramework.bstack11l1ll11l11_opy_: TestFramework.bstack11l11111111_opy_,
            TestFramework.bstack11l11l1111l_opy_: test_id,
            TestFramework.bstack111ll111111_opy_: bstack111ll11111l_opy_
        }
    @staticmethod
    def __111ll1l11ll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack111ll_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᩥ"), [])
            markers.extend([getattr(m, bstack111ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᩦ"), None) for m in own_markers if getattr(m, bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩧ"), None)])
            current = getattr(current, bstack111ll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᩨ"), None)
        return markers
    @staticmethod
    def __11l1111llll_opy_(location):
        return bstack111ll_opy_ (u"ࠨ࠺࠻ࠤᩩ").join(filter(lambda x: isinstance(x, str), location))