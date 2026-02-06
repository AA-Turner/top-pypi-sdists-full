# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1ll1lllll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1lll_opy_ import bstack11ll11lll1l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll11111l1l_opy_,
    bstack1ll11111ll1_opy_,
    bstack1ll11l1l11l_opy_,
    bstack11lll1l1lll_opy_,
    bstack1ll1l11ll11_opy_,
)
import traceback
from bstack_utils.helper import bstack1l11lll1lll_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll11ll11l1_opy_ import bstack1ll1l1l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1lll11l1lll_opy_
bstack1l1l11l1ll1_opy_ = bstack1l11lll1lll_opy_()
bstack1l11l1ll11l_opy_ = bstack11lllll_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᕒ")
bstack11ll1ll1111_opy_ = bstack11lllll_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᕓ")
bstack11ll1l1llll_opy_ = bstack11lllll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᕔ")
bstack11lll1l1l1l_opy_ = 1.0
_1l11ll1lll1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11lll111l11_opy_ = bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᕕ")
    bstack11lll1111l1_opy_ = bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᕖ")
    bstack11lll11l11l_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᕗ")
    bstack11llll11ll1_opy_ = bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᕘ")
    bstack11ll11llll1_opy_ = bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᕙ")
    bstack11llll111l1_opy_: bool
    bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_  = None
    bstack11ll11ll1ll_opy_ = [
        bstack1ll11111l1l_opy_.BEFORE_ALL,
        bstack1ll11111l1l_opy_.AFTER_ALL,
        bstack1ll11111l1l_opy_.BEFORE_EACH,
        bstack1ll11111l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11llll1ll11_opy_: Dict[str, str],
        bstack1l1ll1l111l_opy_: List[str]=[bstack11lllll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᕚ")],
        bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_ = None,
        bstack1ll1l1l1ll1_opy_=None
    ):
        super().__init__(bstack1l1ll1l111l_opy_, bstack11llll1ll11_opy_, bstack1lll11ll111_opy_)
        self.bstack11llll111l1_opy_ = any(bstack11lllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᕛ") in item.lower() for item in bstack1l1ll1l111l_opy_)
        self.bstack1ll1l1l1ll1_opy_ = bstack1ll1l1l1ll1_opy_
    def track_event(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll11111l1l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11ll11ll1ll_opy_:
            bstack11ll11lll1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll11111l1l_opy_.NONE:
            self.logger.warning(bstack11lllll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᕜ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠤࠥᕝ"))
            return
        if not self.bstack11llll111l1_opy_:
            self.logger.warning(bstack11lllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᕞ") + str(str(self.bstack1l1ll1l111l_opy_)) + bstack11lllll_opy_ (u"ࠦࠧᕟ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11lllll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᕠ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᕡ"))
            return
        instance = self.__11ll1lll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᕢ") + str(args) + bstack11lllll_opy_ (u"ࠣࠤᕣ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11ll11ll1ll_opy_ and test_hook_state == bstack1ll11l1l11l_opy_.PRE:
                bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1ll1l1l11l_opy_.value)
                name = str(EVENTS.bstack1ll1l1l11l_opy_.name)+bstack11lllll_opy_ (u"ࠤ࠽ࠦᕤ")+str(test_framework_state.name)
                TestFramework.bstack11lll1lll1l_opy_(instance, name, bstack1ll11111l_opy_)
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᕥ").format(e))
        try:
            if test_framework_state == bstack1ll11111l1l_opy_.TEST:
                if not TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack11ll1l111l1_opy_) and test_hook_state == bstack1ll11l1l11l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll1lll11l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᕦ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠧࠨᕧ"))
                if test_hook_state == bstack1ll11l1l11l_opy_.PRE and not TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11ll11l11_opy_):
                    TestFramework.bstack1lll1ll1lll_opy_(instance, TestFramework.bstack1l11ll11l11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11lll1lll11_opy_(instance, args)
                    self.logger.debug(bstack11lllll_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᕨ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠢࠣᕩ"))
                elif test_hook_state == bstack1ll11l1l11l_opy_.POST and not TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_):
                    TestFramework.bstack1lll1ll1lll_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lllll_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᕪ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠤࠥᕫ"))
            elif test_framework_state == bstack1ll11111l1l_opy_.STEP:
                if test_hook_state == bstack1ll11l1l11l_opy_.PRE:
                    PytestBDDFramework.__11ll1llll1l_opy_(instance, args)
                elif test_hook_state == bstack1ll11l1l11l_opy_.POST:
                    PytestBDDFramework.__11ll1llllll_opy_(instance, args)
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG and test_hook_state == bstack1ll11l1l11l_opy_.POST:
                PytestBDDFramework.__11llll111ll_opy_(instance, *args)
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG_REPORT and test_hook_state == bstack1ll11l1l11l_opy_.POST:
                self.__11llll11l11_opy_(instance, *args)
                self.__11lll1l11l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11ll11ll1ll_opy_:
                self.__11ll1l1111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᕬ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠦࠧᕭ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1lll1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11ll11ll1ll_opy_ and test_hook_state == bstack1ll11l1l11l_opy_.POST:
                name = str(EVENTS.bstack1ll1l1l11l_opy_.name)+bstack11lllll_opy_ (u"ࠧࡀࠢᕮ")+str(test_framework_state.name)
                bstack1ll11111l_opy_ = TestFramework.bstack11ll1lll111_opy_(instance, name)
                bstack1lll11l1ll_opy_.end(EVENTS.bstack1ll1l1l11l_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᕯ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᕰ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᕱ").format(e))
    def bstack1l1l11ll1l1_opy_(self):
        return self.bstack11llll111l1_opy_
    def __11ll1l1l1l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11lllll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᕲ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l11ll11l_opy_(rep, [bstack11lllll_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᕳ"), bstack11lllll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᕴ"), bstack11lllll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᕵ"), bstack11lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᕶ"), bstack11lllll_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᕷ"), bstack11lllll_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᕸ")])
        return None
    def __11llll11l11_opy_(self, instance: bstack1ll11111ll1_opy_, *args):
        result = self.__11ll1l1l1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llll1111ll_opy_ = None
        if result.get(bstack11lllll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᕹ"), None) == bstack11lllll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᕺ") and len(args) > 1 and getattr(args[1], bstack11lllll_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᕻ"), None) is not None:
            failure = [{bstack11lllll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᕼ"): [args[1].excinfo.exconly(), result.get(bstack11lllll_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᕽ"), None)]}]
            bstack1llll1111ll_opy_ = bstack11lllll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᕾ") if bstack11lllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᕿ") in getattr(args[1].excinfo, bstack11lllll_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᖀ"), bstack11lllll_opy_ (u"ࠥࠦᖁ")) else bstack11lllll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᖂ")
        bstack11lll111lll_opy_ = result.get(bstack11lllll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᖃ"), TestFramework.bstack11lll1ll111_opy_)
        if bstack11lll111lll_opy_ != TestFramework.bstack11lll1ll111_opy_:
            TestFramework.bstack1lll1ll1lll_opy_(instance, TestFramework.bstack1l1l111ll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll11lll11_opy_(instance, {
            TestFramework.bstack1l111ll1111_opy_: failure,
            TestFramework.bstack11lll111ll1_opy_: bstack1llll1111ll_opy_,
            TestFramework.bstack1l111l1ll11_opy_: bstack11lll111lll_opy_,
        })
    def __11ll1lll1l1_opy_(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll11111l1l_opy_.SETUP_FIXTURE:
            instance = self.__11lll11l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1ll11ll_opy_ bstack11ll1ll1ll1_opy_ this to be bstack11lllll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᖄ")
            if test_framework_state == bstack1ll11111l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lll11l111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11lllll_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᖅ"), None), bstack11lllll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᖆ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11lllll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᖇ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11lllll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᖈ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll111ll1l_opy_(target) if target else None
        return instance
    def __11ll1l1111l_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11lll1l111l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, PytestBDDFramework.bstack11lll1111l1_opy_, {})
        if not key in bstack11lll1l111l_opy_:
            bstack11lll1l111l_opy_[key] = []
        bstack11llll1111l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, PytestBDDFramework.bstack11lll11l11l_opy_, {})
        if not key in bstack11llll1111l_opy_:
            bstack11llll1111l_opy_[key] = []
        bstack11ll1ll1l1l_opy_ = {
            PytestBDDFramework.bstack11lll1111l1_opy_: bstack11lll1l111l_opy_,
            PytestBDDFramework.bstack11lll11l11l_opy_: bstack11llll1111l_opy_,
        }
        if test_hook_state == bstack1ll11l1l11l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11lllll_opy_ (u"ࠦࡰ࡫ࡹࠣᖉ"): key,
                TestFramework.bstack11ll1l11l1l_opy_: uuid4().__str__(),
                TestFramework.bstack11lll1l1ll1_opy_: TestFramework.bstack11lll11111l_opy_,
                TestFramework.bstack11ll1l11lll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1l11l11_opy_: [],
                TestFramework.bstack11lll1ll1ll_opy_: hook_name,
                TestFramework.bstack11lll11llll_opy_: bstack1ll1l1l111l_opy_.bstack11ll1l11111_opy_()
            }
            bstack11lll1l111l_opy_[key].append(hook)
            bstack11ll1ll1l1l_opy_[PytestBDDFramework.bstack11llll11ll1_opy_] = key
        elif test_hook_state == bstack1ll11l1l11l_opy_.POST:
            bstack11ll11lllll_opy_ = bstack11lll1l111l_opy_.get(key, [])
            hook = bstack11ll11lllll_opy_.pop() if bstack11ll11lllll_opy_ else None
            if hook:
                result = self.__11ll1l1l1l1_opy_(*args)
                if result:
                    bstack11ll1l1ll11_opy_ = result.get(bstack11lllll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᖊ"), TestFramework.bstack11lll11111l_opy_)
                    if bstack11ll1l1ll11_opy_ != TestFramework.bstack11lll11111l_opy_:
                        hook[TestFramework.bstack11lll1l1ll1_opy_] = bstack11ll1l1ll11_opy_
                hook[TestFramework.bstack11lll111l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lll11llll_opy_] = bstack1ll1l1l111l_opy_.bstack11ll1l11111_opy_()
                self.bstack11lll1ll11l_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l1l11l_opy_, [])
                self.bstack1l1l111lll1_opy_(instance, logs)
                bstack11llll1111l_opy_[key].append(hook)
                bstack11ll1ll1l1l_opy_[PytestBDDFramework.bstack11ll11llll1_opy_] = key
        TestFramework.bstack11ll11lll11_opy_(instance, bstack11ll1ll1l1l_opy_)
        self.logger.debug(bstack11lllll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᖋ") + str(bstack11llll1111l_opy_) + bstack11lllll_opy_ (u"ࠢࠣᖌ"))
    def __11lll11l1l1_opy_(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l11ll11l_opy_(args[0], [bstack11lllll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᖍ"), bstack11lllll_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᖎ"), bstack11lllll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᖏ"), bstack11lllll_opy_ (u"ࠦ࡮ࡪࡳࠣᖐ"), bstack11lllll_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᖑ"), bstack11lllll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᖒ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11lllll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᖓ")) else fixturedef.get(bstack11lllll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᖔ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11lllll_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᖕ")) else None
        node = request.node if hasattr(request, bstack11lllll_opy_ (u"ࠥࡲࡴࡪࡥࠣᖖ")) else None
        target = request.node.nodeid if hasattr(node, bstack11lllll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᖗ")) else None
        baseid = fixturedef.get(bstack11lllll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᖘ"), None) or bstack11lllll_opy_ (u"ࠨࠢᖙ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11lllll_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᖚ")):
            target = PytestBDDFramework.__11ll1l111ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11lllll_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᖛ")) else None
            if target and not TestFramework.bstack1lll111ll1l_opy_(target):
                self.__11lll11l111_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᖜ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠥࠦᖝ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11lllll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᖞ") + str(target) + bstack11lllll_opy_ (u"ࠧࠨᖟ"))
            return None
        instance = TestFramework.bstack1lll111ll1l_opy_(target)
        if not instance:
            self.logger.warning(bstack11lllll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᖠ") + str(target) + bstack11lllll_opy_ (u"ࠢࠣᖡ"))
            return None
        bstack11ll1l1l1ll_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, PytestBDDFramework.bstack11lll111l11_opy_, {})
        if os.getenv(bstack11lllll_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᖢ"), bstack11lllll_opy_ (u"ࠤ࠴ࠦᖣ")) == bstack11lllll_opy_ (u"ࠥ࠵ࠧᖤ"):
            bstack11ll1ll11l1_opy_ = bstack11lllll_opy_ (u"ࠦ࠿ࠨᖥ").join((scope, fixturename))
            bstack11llll11lll_opy_ = datetime.now(tz=timezone.utc)
            bstack11lll1111ll_opy_ = {
                bstack11lllll_opy_ (u"ࠧࡱࡥࡺࠤᖦ"): bstack11ll1ll11l1_opy_,
                bstack11lllll_opy_ (u"ࠨࡴࡢࡩࡶࠦᖧ"): PytestBDDFramework.__11ll1lllll1_opy_(request.node, scenario),
                bstack11lllll_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᖨ"): fixturedef,
                bstack11lllll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᖩ"): scope,
                bstack11lllll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᖪ"): None,
            }
            try:
                if test_hook_state == bstack1ll11l1l11l_opy_.POST and callable(getattr(args[-1], bstack11lllll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᖫ"), None)):
                    bstack11lll1111ll_opy_[bstack11lllll_opy_ (u"ࠦࡹࡿࡰࡦࠤᖬ")] = TestFramework.bstack1l11llll1ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll11l1l11l_opy_.PRE:
                bstack11lll1111ll_opy_[bstack11lllll_opy_ (u"ࠧࡻࡵࡪࡦࠥᖭ")] = uuid4().__str__()
                bstack11lll1111ll_opy_[PytestBDDFramework.bstack11ll1l11lll_opy_] = bstack11llll11lll_opy_
            elif test_hook_state == bstack1ll11l1l11l_opy_.POST:
                bstack11lll1111ll_opy_[PytestBDDFramework.bstack11lll111l1l_opy_] = bstack11llll11lll_opy_
            if bstack11ll1ll11l1_opy_ in bstack11ll1l1l1ll_opy_:
                bstack11ll1l1l1ll_opy_[bstack11ll1ll11l1_opy_].update(bstack11lll1111ll_opy_)
                self.logger.debug(bstack11lllll_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᖮ") + str(bstack11ll1l1l1ll_opy_[bstack11ll1ll11l1_opy_]) + bstack11lllll_opy_ (u"ࠢࠣᖯ"))
            else:
                bstack11ll1l1l1ll_opy_[bstack11ll1ll11l1_opy_] = bstack11lll1111ll_opy_
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᖰ") + str(len(bstack11ll1l1l1ll_opy_)) + bstack11lllll_opy_ (u"ࠤࠥᖱ"))
        TestFramework.bstack1lll1ll1lll_opy_(instance, PytestBDDFramework.bstack11lll111l11_opy_, bstack11ll1l1l1ll_opy_)
        self.logger.debug(bstack11lllll_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᖲ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠦࠧᖳ"))
        return instance
    def __11lll11l111_opy_(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1lllll1l_opy_.create_context(target)
        ob = bstack1ll11111ll1_opy_(ctx, self.bstack1l1ll1l111l_opy_, self.bstack11llll1ll11_opy_, test_framework_state)
        TestFramework.bstack11ll11lll11_opy_(ob, {
            TestFramework.bstack1l1ll111ll1_opy_: context.test_framework_name,
            TestFramework.bstack1l11ll1ll1l_opy_: context.test_framework_version,
            TestFramework.bstack11llll11l1l_opy_: [],
            PytestBDDFramework.bstack11lll111l11_opy_: {},
            PytestBDDFramework.bstack11lll11l11l_opy_: {},
            PytestBDDFramework.bstack11lll1111l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1ll1lll_opy_(ob, TestFramework.bstack11ll1ll111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1ll1lll_opy_(ob, TestFramework.bstack1l1l1lllll1_opy_, context.platform_index)
        TestFramework.bstack1ll1llll11l_opy_[ctx.id] = ob
        self.logger.debug(bstack11lllll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᖴ") + str(TestFramework.bstack1ll1llll11l_opy_.keys()) + bstack11lllll_opy_ (u"ࠨࠢᖵ"))
        return ob
    @staticmethod
    def __11lll1lll11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lllll_opy_ (u"ࠧࡪࡦࠪᖶ"): id(step),
                bstack11lllll_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᖷ"): step.name,
                bstack11lllll_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᖸ"): step.keyword,
            })
        meta = {
            bstack11lllll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᖹ"): {
                bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᖺ"): feature.name,
                bstack11lllll_opy_ (u"ࠬࡶࡡࡵࡪࠪᖻ"): feature.filename,
                bstack11lllll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᖼ"): feature.description
            },
            bstack11lllll_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᖽ"): {
                bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᖾ"): scenario.name
            },
            bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᖿ"): steps,
            bstack11lllll_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᗀ"): PytestBDDFramework.__11ll1l11ll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11lll1llll1_opy_: meta
            }
        )
    def bstack11lll1ll11l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11lllll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᗁ")
        global _1l11ll1lll1_opy_
        platform_index = os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᗂ")]
        bstack1l11ll1l11l_opy_ = os.path.join(bstack1l1l11l1ll1_opy_, (bstack1l11l1ll11l_opy_ + str(platform_index)), bstack11ll1ll1111_opy_)
        if not os.path.exists(bstack1l11ll1l11l_opy_) or not os.path.isdir(bstack1l11ll1l11l_opy_):
            return
        logs = hook.get(bstack11lllll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᗃ"), [])
        with os.scandir(bstack1l11ll1l11l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11ll1lll1_opy_:
                    self.logger.info(bstack11lllll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᗄ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11lllll_opy_ (u"ࠣࠤᗅ")
                    log_entry = bstack1ll1l11ll11_opy_(
                        kind=bstack11lllll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᗆ"),
                        message=bstack11lllll_opy_ (u"ࠥࠦᗇ"),
                        level=bstack11lllll_opy_ (u"ࠦࠧᗈ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l111l11l_opy_=entry.stat().st_size,
                        bstack1l1l11l1l1l_opy_=bstack11lllll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᗉ"),
                        bstack1111ll1_opy_=os.path.abspath(entry.path),
                        bstack11llll1l1ll_opy_=hook.get(TestFramework.bstack11ll1l11l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l11ll1lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᗊ")]
        bstack11ll1l1lll1_opy_ = os.path.join(bstack1l1l11l1ll1_opy_, (bstack1l11l1ll11l_opy_ + str(platform_index)), bstack11ll1ll1111_opy_, bstack11ll1l1llll_opy_)
        if not os.path.exists(bstack11ll1l1lll1_opy_) or not os.path.isdir(bstack11ll1l1lll1_opy_):
            self.logger.info(bstack11lllll_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᗋ").format(bstack11ll1l1lll1_opy_))
        else:
            self.logger.info(bstack11lllll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᗌ").format(bstack11ll1l1lll1_opy_))
            with os.scandir(bstack11ll1l1lll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11ll1lll1_opy_:
                        self.logger.info(bstack11lllll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᗍ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11lllll_opy_ (u"ࠥࠦᗎ")
                        log_entry = bstack1ll1l11ll11_opy_(
                            kind=bstack11lllll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᗏ"),
                            message=bstack11lllll_opy_ (u"ࠧࠨᗐ"),
                            level=bstack11lllll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᗑ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l111l11l_opy_=entry.stat().st_size,
                            bstack1l1l11l1l1l_opy_=bstack11lllll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᗒ"),
                            bstack1111ll1_opy_=os.path.abspath(entry.path),
                            bstack1l11lll1111_opy_=hook.get(TestFramework.bstack11ll1l11l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l11ll1lll1_opy_.add(abs_path)
        hook[bstack11lllll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᗓ")] = logs
    def bstack1l1l111lll1_opy_(
        self,
        bstack1l1l111l1ll_opy_: bstack1ll11111ll1_opy_,
        entries: List[bstack1ll1l11ll11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᗔ"))
        req.platform_index = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1l1lllll1_opy_)
        req.client_worker_id = bstack11lllll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᗕ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1l111l1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l111l1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l111l1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1ll111ll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l11ll1ll1l_opy_)
            log_entry.uuid = entry.bstack11llll1l1ll_opy_ if entry.bstack11llll1l1ll_opy_ else TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1lll1l111_opy_)
            log_entry.test_framework_state = bstack1l1l111l1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lllll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᗖ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11lllll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᗗ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l111l11l_opy_
                log_entry.file_path = entry.bstack1111ll1_opy_
        def bstack1l1l11l11ll_opy_():
            bstack1l1111l111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1ll1_opy_.LogCreatedEvent(req)
                bstack1l1l111l1ll_opy_.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᗘ"), datetime.now() - bstack1l1111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lllll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᗙ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll11ll111_opy_.enqueue(bstack1l1l11l11ll_opy_)
    def __11lll1l11l1_opy_(self, instance) -> None:
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᗚ")
        bstack11ll1ll1l1l_opy_ = {bstack11lllll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᗛ"): bstack1ll1l1l111l_opy_.bstack11ll1l11111_opy_()}
        TestFramework.bstack11ll11lll11_opy_(instance, bstack11ll1ll1l1l_opy_)
    @staticmethod
    def __11ll1llll1l_opy_(instance, args):
        request, bstack11ll1llll11_opy_ = args
        bstack11lll1lllll_opy_ = id(bstack11ll1llll11_opy_)
        bstack11llll1l1l1_opy_ = instance.data[TestFramework.bstack11lll1llll1_opy_]
        step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭ᗜ")] == bstack11lll1lllll_opy_, bstack11llll1l1l1_opy_[bstack11lllll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᗝ")]), None)
        step.update({
            bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᗞ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11llll1l1l1_opy_[bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᗟ")]) if st[bstack11lllll_opy_ (u"ࠧࡪࡦࠪᗠ")] == step[bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫᗡ")]), None)
        if index is not None:
            bstack11llll1l1l1_opy_[bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᗢ")][index] = step
        instance.data[TestFramework.bstack11lll1llll1_opy_] = bstack11llll1l1l1_opy_
    @staticmethod
    def __11ll1llllll_opy_(instance, args):
        bstack11lllll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᗣ")
        bstack11lll11ll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll1llll11_opy_ = args[1]
        bstack11lll1lllll_opy_ = id(bstack11ll1llll11_opy_)
        bstack11llll1l1l1_opy_ = instance.data[TestFramework.bstack11lll1llll1_opy_]
        step = None
        if bstack11lll1lllll_opy_ is not None and bstack11llll1l1l1_opy_.get(bstack11lllll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᗤ")):
            step = next(filter(lambda st: st[bstack11lllll_opy_ (u"ࠬ࡯ࡤࠨᗥ")] == bstack11lll1lllll_opy_, bstack11llll1l1l1_opy_[bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᗦ")]), None)
            step.update({
                bstack11lllll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᗧ"): bstack11lll11ll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11lllll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᗨ"): bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗩ"),
                bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᗪ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11lllll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᗫ"): bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᗬ"),
                })
        index = next((i for i, st in enumerate(bstack11llll1l1l1_opy_[bstack11lllll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᗭ")]) if st[bstack11lllll_opy_ (u"ࠧࡪࡦࠪᗮ")] == step[bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫᗯ")]), None)
        if index is not None:
            bstack11llll1l1l1_opy_[bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᗰ")][index] = step
        instance.data[TestFramework.bstack11lll1llll1_opy_] = bstack11llll1l1l1_opy_
    @staticmethod
    def __11ll1l11ll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11lllll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᗱ")):
                examples = list(node.callspec.params[bstack11lllll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᗲ")].values())
            return examples
        except:
            return []
    def bstack1l11ll1111l_opy_(self, instance: bstack1ll11111ll1_opy_, bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_]):
        bstack11ll1l1l111_opy_ = (
            PytestBDDFramework.bstack11llll11ll1_opy_
            if bstack1lll1l11lll_opy_[1] == bstack1ll11l1l11l_opy_.PRE
            else PytestBDDFramework.bstack11ll11llll1_opy_
        )
        hook = PytestBDDFramework.bstack11lll1ll1l1_opy_(instance, bstack11ll1l1l111_opy_)
        entries = hook.get(TestFramework.bstack11ll1l11l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11llll11l1l_opy_, []))
        return entries
    def bstack1l1l11111l1_opy_(self, instance: bstack1ll11111ll1_opy_, bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_]):
        bstack11ll1l1l111_opy_ = (
            PytestBDDFramework.bstack11llll11ll1_opy_
            if bstack1lll1l11lll_opy_[1] == bstack1ll11l1l11l_opy_.PRE
            else PytestBDDFramework.bstack11ll11llll1_opy_
        )
        PytestBDDFramework.bstack11lll1l11ll_opy_(instance, bstack11ll1l1l111_opy_)
        TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11llll11l1l_opy_, []).clear()
    @staticmethod
    def bstack11lll1ll1l1_opy_(instance: bstack1ll11111ll1_opy_, bstack11ll1l1l111_opy_: str):
        bstack11llll1l11l_opy_ = (
            PytestBDDFramework.bstack11lll11l11l_opy_
            if bstack11ll1l1l111_opy_ == PytestBDDFramework.bstack11ll11llll1_opy_
            else PytestBDDFramework.bstack11lll1111l1_opy_
        )
        bstack11lll11lll1_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11ll1l1l111_opy_, None)
        bstack11ll1l1ll1l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11llll1l11l_opy_, None) if bstack11lll11lll1_opy_ else None
        return (
            bstack11ll1l1ll1l_opy_[bstack11lll11lll1_opy_][-1]
            if isinstance(bstack11ll1l1ll1l_opy_, dict) and len(bstack11ll1l1ll1l_opy_.get(bstack11lll11lll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lll1l11ll_opy_(instance: bstack1ll11111ll1_opy_, bstack11ll1l1l111_opy_: str):
        hook = PytestBDDFramework.bstack11lll1ll1l1_opy_(instance, bstack11ll1l1l111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1l11l11_opy_, []).clear()
    @staticmethod
    def __11llll111ll_opy_(instance: bstack1ll11111ll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11lllll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᗳ"), None)):
            return
        if os.getenv(bstack11lllll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᗴ"), bstack11lllll_opy_ (u"ࠢ࠲ࠤᗵ")) != bstack11lllll_opy_ (u"ࠣ࠳ࠥᗶ"):
            PytestBDDFramework.logger.warning(bstack11lllll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᗷ"))
            return
        bstack11lll11l1ll_opy_ = {
            bstack11lllll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᗸ"): (PytestBDDFramework.bstack11llll11ll1_opy_, PytestBDDFramework.bstack11lll1111l1_opy_),
            bstack11lllll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᗹ"): (PytestBDDFramework.bstack11ll11llll1_opy_, PytestBDDFramework.bstack11lll11l11l_opy_),
        }
        for when in (bstack11lllll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᗺ"), bstack11lllll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᗻ"), bstack11lllll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᗼ")):
            bstack11llll1l111_opy_ = args[1].get_records(when)
            if not bstack11llll1l111_opy_:
                continue
            records = [
                bstack1ll1l11ll11_opy_(
                    kind=TestFramework.bstack1l11ll111l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11lllll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᗽ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11lllll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᗾ")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll1l111_opy_
                if isinstance(getattr(r, bstack11lllll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᗿ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11llll11111_opy_, bstack11llll1l11l_opy_ = bstack11lll11l1ll_opy_.get(when, (None, None))
            bstack11lll111111_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11llll11111_opy_, None) if bstack11llll11111_opy_ else None
            bstack11ll1l1ll1l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11llll1l11l_opy_, None) if bstack11lll111111_opy_ else None
            if isinstance(bstack11ll1l1ll1l_opy_, dict) and len(bstack11ll1l1ll1l_opy_.get(bstack11lll111111_opy_, [])) > 0:
                hook = bstack11ll1l1ll1l_opy_[bstack11lll111111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1l11l11_opy_ in hook:
                    hook[TestFramework.bstack11ll1l11l11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11llll11l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1lll11l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1ll11llll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__11ll1ll1l11_opy_(request.node, scenario)
        bstack11lll1l1111_opy_ = feature.filename
        if not bstack1ll11llll1_opy_ or not test_name or not bstack11lll1l1111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1lll1l111_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1l111l1_opy_: bstack1ll11llll1_opy_,
            TestFramework.bstack1l1lll11111_opy_: test_name,
            TestFramework.bstack1l11l1l1111_opy_: bstack1ll11llll1_opy_,
            TestFramework.bstack11ll1ll1lll_opy_: bstack11lll1l1111_opy_,
            TestFramework.bstack11lll11ll11_opy_: PytestBDDFramework.__11ll1lllll1_opy_(feature, scenario),
            TestFramework.bstack11lll1l1l11_opy_: code,
            TestFramework.bstack1l111l1ll11_opy_: TestFramework.bstack11lll1ll111_opy_,
            TestFramework.bstack11lllllll11_opy_: test_name
        }
    @staticmethod
    def __11ll1ll1l11_opy_(node, scenario):
        if hasattr(node, bstack11lllll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᘀ")):
            parts = node.nodeid.rsplit(bstack11lllll_opy_ (u"ࠧࡡࠢᘁ"))
            params = parts[-1]
            return bstack11lllll_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᘂ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll1lllll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11lllll_opy_ (u"ࠧࡵࡣࡪࡷࠬᘃ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11lllll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᘄ")) else [])
    @staticmethod
    def __11ll1l111ll_opy_(location):
        return bstack11lllll_opy_ (u"ࠤ࠽࠾ࠧᘅ").join(filter(lambda x: isinstance(x, str), location))