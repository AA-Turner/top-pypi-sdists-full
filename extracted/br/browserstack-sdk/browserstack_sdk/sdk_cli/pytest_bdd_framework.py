# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll111l_opy_ import bstack1llll1lll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1ll_opy_ import bstack1l1111lllll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll11l1l_opy_,
    bstack1lll11l1111_opy_,
    bstack1lll111l1l1_opy_,
    bstack1l111l1l11l_opy_,
    bstack1ll1lll1l11_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1ll11ll1l_opy_
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1l1ll1_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
bstack1l1lll1lll1_opy_ = bstack1l1ll11ll1l_opy_()
bstack1l1ll1l11ll_opy_ = bstack1l11ll1_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᐬ")
bstack1l1111l1lll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᐭ")
bstack1l1111l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᐮ")
bstack1l111ll1l1l_opy_ = 1.0
_1l1ll1111ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l1111ll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᐯ")
    bstack1l111lll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᐰ")
    bstack1l1111l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᐱ")
    bstack1l1111l111l_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᐲ")
    bstack1l1111l11ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᐳ")
    bstack1l11l1111l1_opy_: bool
    bstack1111111ll1_opy_: bstack11111111ll_opy_  = None
    bstack1l111l1llll_opy_ = [
        bstack1ll1ll11l1l_opy_.BEFORE_ALL,
        bstack1ll1ll11l1l_opy_.AFTER_ALL,
        bstack1ll1ll11l1l_opy_.BEFORE_EACH,
        bstack1ll1ll11l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11lllll111l_opy_: Dict[str, str],
        bstack1ll111ll1l1_opy_: List[str]=[bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᐴ")],
        bstack1111111ll1_opy_: bstack11111111ll_opy_ = None,
        bstack1lll111111l_opy_=None
    ):
        super().__init__(bstack1ll111ll1l1_opy_, bstack11lllll111l_opy_, bstack1111111ll1_opy_)
        self.bstack1l11l1111l1_opy_ = any(bstack1l11ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᐵ") in item.lower() for item in bstack1ll111ll1l1_opy_)
        self.bstack1lll111111l_opy_ = bstack1lll111111l_opy_
    def track_event(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll11l1l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111l1llll_opy_:
            bstack1l1111lllll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll11l1l_opy_.NONE:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᐶ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠤࠥᐷ"))
            return
        if not self.bstack1l11l1111l1_opy_:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᐸ") + str(str(self.bstack1ll111ll1l1_opy_)) + bstack1l11ll1_opy_ (u"ࠦࠧᐹ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐺ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢᐻ"))
            return
        instance = self.__1l111l1l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᐼ") + str(args) + bstack1l11ll1_opy_ (u"ࠣࠤᐽ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1llll_opy_ and test_hook_state == bstack1lll111l1l1_opy_.PRE:
                bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1l111ll1_opy_.value)
                name = str(EVENTS.bstack1l111ll1_opy_.name)+bstack1l11ll1_opy_ (u"ࠤ࠽ࠦᐾ")+str(test_framework_state.name)
                TestFramework.bstack1l111lllll1_opy_(instance, name, bstack1ll111l1lll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᐿ").format(e))
        try:
            if test_framework_state == bstack1ll1ll11l1l_opy_.TEST:
                if not TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l11l11111l_opy_) and test_hook_state == bstack1lll111l1l1_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11111lll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᑀ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠧࠨᑁ"))
                if test_hook_state == bstack1lll111l1l1_opy_.PRE and not TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_):
                    TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11llllll11l_opy_(instance, args)
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᑂ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠢࠣᑃ"))
                elif test_hook_state == bstack1lll111l1l1_opy_.POST and not TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_):
                    TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᑄ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠤࠥᑅ"))
            elif test_framework_state == bstack1ll1ll11l1l_opy_.STEP:
                if test_hook_state == bstack1lll111l1l1_opy_.PRE:
                    PytestBDDFramework.__1l111ll11ll_opy_(instance, args)
                elif test_hook_state == bstack1lll111l1l1_opy_.POST:
                    PytestBDDFramework.__11lllll1l11_opy_(instance, args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG and test_hook_state == bstack1lll111l1l1_opy_.POST:
                PytestBDDFramework.__11llllll111_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG_REPORT and test_hook_state == bstack1lll111l1l1_opy_.POST:
                self.__11lllllllll_opy_(instance, *args)
                self.__1l1111l1111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111l1llll_opy_:
                self.__1l111l1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᑆ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠦࠧᑇ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111ll1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1llll_opy_ and test_hook_state == bstack1lll111l1l1_opy_.POST:
                name = str(EVENTS.bstack1l111ll1_opy_.name)+bstack1l11ll1_opy_ (u"ࠧࡀࠢᑈ")+str(test_framework_state.name)
                bstack1ll111l1lll_opy_ = TestFramework.bstack1l111lll111_opy_(instance, name)
                bstack1lll11111l1_opy_.end(EVENTS.bstack1l111ll1_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᑉ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᑊ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᑋ").format(e))
    def bstack1l1lll11111_opy_(self):
        return self.bstack1l11l1111l1_opy_
    def __1l111ll1ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11ll1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᑌ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll111111_opy_(rep, [bstack1l11ll1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᑍ"), bstack1l11ll1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑎ"), bstack1l11ll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᑏ"), bstack1l11ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᑐ"), bstack1l11ll1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᑑ"), bstack1l11ll1_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᑒ")])
        return None
    def __11lllllllll_opy_(self, instance: bstack1lll11l1111_opy_, *args):
        result = self.__1l111ll1ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111l1l1_opy_ = None
        if result.get(bstack1l11ll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑓ"), None) == bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᑔ") and len(args) > 1 and getattr(args[1], bstack1l11ll1_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᑕ"), None) is not None:
            failure = [{bstack1l11ll1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᑖ"): [args[1].excinfo.exconly(), result.get(bstack1l11ll1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᑗ"), None)]}]
            bstack111111l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᑘ") if bstack1l11ll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᑙ") in getattr(args[1].excinfo, bstack1l11ll1_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᑚ"), bstack1l11ll1_opy_ (u"ࠥࠦᑛ")) else bstack1l11ll1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᑜ")
        bstack1l11111l111_opy_ = result.get(bstack1l11ll1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑝ"), TestFramework.bstack1l111111lll_opy_)
        if bstack1l11111l111_opy_ != TestFramework.bstack1l111111lll_opy_:
            TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111l111l1_opy_(instance, {
            TestFramework.bstack1l1l1111l11_opy_: failure,
            TestFramework.bstack1l11111l1ll_opy_: bstack111111l1l1_opy_,
            TestFramework.bstack1l1l1111ll1_opy_: bstack1l11111l111_opy_,
        })
    def __1l111l1l1l1_opy_(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll11l1l_opy_.SETUP_FIXTURE:
            instance = self.__11llllllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l1111lll11_opy_ bstack1l1111llll1_opy_ this to be bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑞ")
            if test_framework_state == bstack1ll1ll11l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11llllll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11ll1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᑟ"), None), bstack1l11ll1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑠ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11ll1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᑡ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l11ll1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑢ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll11l1l_opy_(target) if target else None
        return instance
    def __1l111l1l1ll_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l11lll_opy_ = TestFramework.bstack1llllllllll_opy_(instance, PytestBDDFramework.bstack1l111lll1ll_opy_, {})
        if not key in bstack1l111l11lll_opy_:
            bstack1l111l11lll_opy_[key] = []
        bstack1l1111ll11l_opy_ = TestFramework.bstack1llllllllll_opy_(instance, PytestBDDFramework.bstack1l1111l11l1_opy_, {})
        if not key in bstack1l1111ll11l_opy_:
            bstack1l1111ll11l_opy_[key] = []
        bstack11lllllll1l_opy_ = {
            PytestBDDFramework.bstack1l111lll1ll_opy_: bstack1l111l11lll_opy_,
            PytestBDDFramework.bstack1l1111l11l1_opy_: bstack1l1111ll11l_opy_,
        }
        if test_hook_state == bstack1lll111l1l1_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l11ll1_opy_ (u"ࠦࡰ࡫ࡹࠣᑣ"): key,
                TestFramework.bstack1l11111ll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l111ll1111_opy_: TestFramework.bstack1l111l1ll11_opy_,
                TestFramework.bstack1l111l111ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111ll1ll_opy_: [],
                TestFramework.bstack1l11111l1l1_opy_: hook_name,
                TestFramework.bstack11lllll11ll_opy_: bstack1lll1l111ll_opy_.bstack1l111llllll_opy_()
            }
            bstack1l111l11lll_opy_[key].append(hook)
            bstack11lllllll1l_opy_[PytestBDDFramework.bstack1l1111l111l_opy_] = key
        elif test_hook_state == bstack1lll111l1l1_opy_.POST:
            bstack1l111111111_opy_ = bstack1l111l11lll_opy_.get(key, [])
            hook = bstack1l111111111_opy_.pop() if bstack1l111111111_opy_ else None
            if hook:
                result = self.__1l111ll1ll1_opy_(*args)
                if result:
                    bstack1l111ll11l1_opy_ = result.get(bstack1l11ll1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑤ"), TestFramework.bstack1l111l1ll11_opy_)
                    if bstack1l111ll11l1_opy_ != TestFramework.bstack1l111l1ll11_opy_:
                        hook[TestFramework.bstack1l111ll1111_opy_] = bstack1l111ll11l1_opy_
                hook[TestFramework.bstack11lllllll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lllll11ll_opy_] = bstack1lll1l111ll_opy_.bstack1l111llllll_opy_()
                self.bstack1l111ll1lll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111111l1l_opy_, [])
                self.bstack1l1l1ll1ll1_opy_(instance, logs)
                bstack1l1111ll11l_opy_[key].append(hook)
                bstack11lllllll1l_opy_[PytestBDDFramework.bstack1l1111l11ll_opy_] = key
        TestFramework.bstack1l111l111l1_opy_(instance, bstack11lllllll1l_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᑥ") + str(bstack1l1111ll11l_opy_) + bstack1l11ll1_opy_ (u"ࠢࠣᑦ"))
    def __11llllllll1_opy_(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll111111_opy_(args[0], [bstack1l11ll1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑧ"), bstack1l11ll1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᑨ"), bstack1l11ll1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᑩ"), bstack1l11ll1_opy_ (u"ࠦ࡮ࡪࡳࠣᑪ"), bstack1l11ll1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᑫ"), bstack1l11ll1_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᑬ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l11ll1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑭ")) else fixturedef.get(bstack1l11ll1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑮ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11ll1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᑯ")) else None
        node = request.node if hasattr(request, bstack1l11ll1_opy_ (u"ࠥࡲࡴࡪࡥࠣᑰ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11ll1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑱ")) else None
        baseid = fixturedef.get(bstack1l11ll1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᑲ"), None) or bstack1l11ll1_opy_ (u"ࠨࠢᑳ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11ll1_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᑴ")):
            target = PytestBDDFramework.__1l111l1111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11ll1_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᑵ")) else None
            if target and not TestFramework.bstack1lllll11l1l_opy_(target):
                self.__11llllll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᑶ") + str(test_hook_state) + bstack1l11ll1_opy_ (u"ࠥࠦᑷ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᑸ") + str(target) + bstack1l11ll1_opy_ (u"ࠧࠨᑹ"))
            return None
        instance = TestFramework.bstack1lllll11l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᑺ") + str(target) + bstack1l11ll1_opy_ (u"ࠢࠣᑻ"))
            return None
        bstack1l111l11ll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, PytestBDDFramework.bstack1l1111ll1l1_opy_, {})
        if os.getenv(bstack1l11ll1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᑼ"), bstack1l11ll1_opy_ (u"ࠤ࠴ࠦᑽ")) == bstack1l11ll1_opy_ (u"ࠥ࠵ࠧᑾ"):
            bstack1l11111l11l_opy_ = bstack1l11ll1_opy_ (u"ࠦ࠿ࠨᑿ").join((scope, fixturename))
            bstack1l1111l1l11_opy_ = datetime.now(tz=timezone.utc)
            bstack11llllll1l1_opy_ = {
                bstack1l11ll1_opy_ (u"ࠧࡱࡥࡺࠤᒀ"): bstack1l11111l11l_opy_,
                bstack1l11ll1_opy_ (u"ࠨࡴࡢࡩࡶࠦᒁ"): PytestBDDFramework.__1l11111llll_opy_(request.node, scenario),
                bstack1l11ll1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᒂ"): fixturedef,
                bstack1l11ll1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᒃ"): scope,
                bstack1l11ll1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᒄ"): None,
            }
            try:
                if test_hook_state == bstack1lll111l1l1_opy_.POST and callable(getattr(args[-1], bstack1l11ll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᒅ"), None)):
                    bstack11llllll1l1_opy_[bstack1l11ll1_opy_ (u"ࠦࡹࡿࡰࡦࠤᒆ")] = TestFramework.bstack1l1ll111ll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111l1l1_opy_.PRE:
                bstack11llllll1l1_opy_[bstack1l11ll1_opy_ (u"ࠧࡻࡵࡪࡦࠥᒇ")] = uuid4().__str__()
                bstack11llllll1l1_opy_[PytestBDDFramework.bstack1l111l111ll_opy_] = bstack1l1111l1l11_opy_
            elif test_hook_state == bstack1lll111l1l1_opy_.POST:
                bstack11llllll1l1_opy_[PytestBDDFramework.bstack11lllllll11_opy_] = bstack1l1111l1l11_opy_
            if bstack1l11111l11l_opy_ in bstack1l111l11ll1_opy_:
                bstack1l111l11ll1_opy_[bstack1l11111l11l_opy_].update(bstack11llllll1l1_opy_)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᒈ") + str(bstack1l111l11ll1_opy_[bstack1l11111l11l_opy_]) + bstack1l11ll1_opy_ (u"ࠢࠣᒉ"))
            else:
                bstack1l111l11ll1_opy_[bstack1l11111l11l_opy_] = bstack11llllll1l1_opy_
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᒊ") + str(len(bstack1l111l11ll1_opy_)) + bstack1l11ll1_opy_ (u"ࠤࠥᒋ"))
        TestFramework.bstack1llllll1ll1_opy_(instance, PytestBDDFramework.bstack1l1111ll1l1_opy_, bstack1l111l11ll1_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᒌ") + str(instance.ref()) + bstack1l11ll1_opy_ (u"ࠦࠧᒍ"))
        return instance
    def __11llllll1ll_opy_(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll1lll11_opy_.create_context(target)
        ob = bstack1lll11l1111_opy_(ctx, self.bstack1ll111ll1l1_opy_, self.bstack11lllll111l_opy_, test_framework_state)
        TestFramework.bstack1l111l111l1_opy_(ob, {
            TestFramework.bstack1ll1l111l1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1l1l1ll_opy_: context.test_framework_version,
            TestFramework.bstack1l111llll1l_opy_: [],
            PytestBDDFramework.bstack1l1111ll1l1_opy_: {},
            PytestBDDFramework.bstack1l1111l11l1_opy_: {},
            PytestBDDFramework.bstack1l111lll1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllll1ll1_opy_(ob, TestFramework.bstack11lllll11l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllll1ll1_opy_(ob, TestFramework.bstack1ll1111l1l1_opy_, context.platform_index)
        TestFramework.bstack1llllll1lll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᒎ") + str(TestFramework.bstack1llllll1lll_opy_.keys()) + bstack1l11ll1_opy_ (u"ࠨࠢᒏ"))
        return ob
    @staticmethod
    def __11llllll11l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪᒐ"): id(step),
                bstack1l11ll1_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᒑ"): step.name,
                bstack1l11ll1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᒒ"): step.keyword,
            })
        meta = {
            bstack1l11ll1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᒓ"): {
                bstack1l11ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒔ"): feature.name,
                bstack1l11ll1_opy_ (u"ࠬࡶࡡࡵࡪࠪᒕ"): feature.filename,
                bstack1l11ll1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᒖ"): feature.description
            },
            bstack1l11ll1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᒗ"): {
                bstack1l11ll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᒘ"): scenario.name
            },
            bstack1l11ll1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒙ"): steps,
            bstack1l11ll1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᒚ"): PytestBDDFramework.__1l111l11111_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l1ll1l_opy_: meta
            }
        )
    def bstack1l111ll1lll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᒛ")
        global _1l1ll1111ll_opy_
        platform_index = os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᒜ")]
        bstack1l1ll11ll11_opy_ = os.path.join(bstack1l1lll1lll1_opy_, (bstack1l1ll1l11ll_opy_ + str(platform_index)), bstack1l1111l1lll_opy_)
        if not os.path.exists(bstack1l1ll11ll11_opy_) or not os.path.isdir(bstack1l1ll11ll11_opy_):
            return
        logs = hook.get(bstack1l11ll1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒝ"), [])
        with os.scandir(bstack1l1ll11ll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1111ll_opy_:
                    self.logger.info(bstack1l11ll1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒞ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l11ll1_opy_ (u"ࠣࠤᒟ")
                    log_entry = bstack1ll1lll1l11_opy_(
                        kind=bstack1l11ll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒠ"),
                        message=bstack1l11ll1_opy_ (u"ࠥࠦᒡ"),
                        level=bstack1l11ll1_opy_ (u"ࠦࠧᒢ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1l111l_opy_=entry.stat().st_size,
                        bstack1l1ll1l1l11_opy_=bstack1l11ll1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒣ"),
                        bstack111l111_opy_=os.path.abspath(entry.path),
                        bstack1l1111111ll_opy_=hook.get(TestFramework.bstack1l11111ll11_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1111ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᒤ")]
        bstack11lllll1l1l_opy_ = os.path.join(bstack1l1lll1lll1_opy_, (bstack1l1ll1l11ll_opy_ + str(platform_index)), bstack1l1111l1lll_opy_, bstack1l1111l1l1l_opy_)
        if not os.path.exists(bstack11lllll1l1l_opy_) or not os.path.isdir(bstack11lllll1l1l_opy_):
            self.logger.info(bstack1l11ll1_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᒥ").format(bstack11lllll1l1l_opy_))
        else:
            self.logger.info(bstack1l11ll1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᒦ").format(bstack11lllll1l1l_opy_))
            with os.scandir(bstack11lllll1l1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1111ll_opy_:
                        self.logger.info(bstack1l11ll1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᒧ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l11ll1_opy_ (u"ࠥࠦᒨ")
                        log_entry = bstack1ll1lll1l11_opy_(
                            kind=bstack1l11ll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᒩ"),
                            message=bstack1l11ll1_opy_ (u"ࠧࠨᒪ"),
                            level=bstack1l11ll1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᒫ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1l111l_opy_=entry.stat().st_size,
                            bstack1l1ll1l1l11_opy_=bstack1l11ll1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᒬ"),
                            bstack111l111_opy_=os.path.abspath(entry.path),
                            bstack1l1l1ll1l1l_opy_=hook.get(TestFramework.bstack1l11111ll11_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1111ll_opy_.add(abs_path)
        hook[bstack1l11ll1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᒭ")] = logs
    def bstack1l1l1ll1ll1_opy_(
        self,
        bstack1l1lll11lll_opy_: bstack1lll11l1111_opy_,
        entries: List[bstack1ll1lll1l11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l11ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᒮ"))
        req.platform_index = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll1111l1l1_opy_)
        req.execution_context.hash = str(bstack1l1lll11lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll11lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll11lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll1l111l1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1l1l1l1l1ll_opy_)
            log_entry.uuid = entry.bstack1l1111111ll_opy_ if entry.bstack1l1111111ll_opy_ else TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll111ll1ll_opy_)
            log_entry.test_framework_state = bstack1l1lll11lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l11ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᒯ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l11ll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᒰ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1l111l_opy_
                log_entry.file_path = entry.bstack111l111_opy_
        def bstack1l1l1ll1lll_opy_():
            bstack1l11ll1ll_opy_ = datetime.now()
            try:
                self.bstack1lll111111l_opy_.LogCreatedEvent(req)
                bstack1l1lll11lll_opy_.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᒱ"), datetime.now() - bstack1l11ll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᒲ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1l1ll1lll_opy_)
    def __1l1111l1111_opy_(self, instance) -> None:
        bstack1l11ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᒳ")
        bstack11lllllll1l_opy_ = {bstack1l11ll1_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᒴ"): bstack1lll1l111ll_opy_.bstack1l111llllll_opy_()}
        TestFramework.bstack1l111l111l1_opy_(instance, bstack11lllllll1l_opy_)
    @staticmethod
    def __1l111ll11ll_opy_(instance, args):
        request, bstack1l11l111111_opy_ = args
        bstack1l111l11l11_opy_ = id(bstack1l11l111111_opy_)
        bstack1l111lll1l1_opy_ = instance.data[TestFramework.bstack1l111l1ll1l_opy_]
        step = next(filter(lambda st: st[bstack1l11ll1_opy_ (u"ࠩ࡬ࡨࠬᒵ")] == bstack1l111l11l11_opy_, bstack1l111lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒶ")]), None)
        step.update({
            bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᒷ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒸ")]) if st[bstack1l11ll1_opy_ (u"࠭ࡩࡥࠩᒹ")] == step[bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪᒺ")]), None)
        if index is not None:
            bstack1l111lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒻ")][index] = step
        instance.data[TestFramework.bstack1l111l1ll1l_opy_] = bstack1l111lll1l1_opy_
    @staticmethod
    def __11lllll1l11_opy_(instance, args):
        bstack1l11ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᒼ")
        bstack1l11111111l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l111111_opy_ = args[1]
        bstack1l111l11l11_opy_ = id(bstack1l11l111111_opy_)
        bstack1l111lll1l1_opy_ = instance.data[TestFramework.bstack1l111l1ll1l_opy_]
        step = None
        if bstack1l111l11l11_opy_ is not None and bstack1l111lll1l1_opy_.get(bstack1l11ll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")):
            step = next(filter(lambda st: st[bstack1l11ll1_opy_ (u"ࠫ࡮ࡪࠧᒾ")] == bstack1l111l11l11_opy_, bstack1l111lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")]), None)
            step.update({
                bstack1l11ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᓀ"): bstack1l11111111l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l11ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᓁ"): bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᓂ"),
                bstack1l11ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᓃ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l11ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᓄ"): bstack1l11ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᓅ"),
                })
        index = next((i for i, st in enumerate(bstack1l111lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓆ")]) if st[bstack1l11ll1_opy_ (u"࠭ࡩࡥࠩᓇ")] == step[bstack1l11ll1_opy_ (u"ࠧࡪࡦࠪᓈ")]), None)
        if index is not None:
            bstack1l111lll1l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓉ")][index] = step
        instance.data[TestFramework.bstack1l111l1ll1l_opy_] = bstack1l111lll1l1_opy_
    @staticmethod
    def __1l111l11111_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l11ll1_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᓊ")):
                examples = list(node.callspec.params[bstack1l11ll1_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᓋ")].values())
            return examples
        except:
            return []
    def bstack1l1l1ll11ll_opy_(self, instance: bstack1lll11l1111_opy_, bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_]):
        bstack1l11111ll1l_opy_ = (
            PytestBDDFramework.bstack1l1111l111l_opy_
            if bstack1lllll1llll_opy_[1] == bstack1lll111l1l1_opy_.PRE
            else PytestBDDFramework.bstack1l1111l11ll_opy_
        )
        hook = PytestBDDFramework.bstack1l111111ll1_opy_(instance, bstack1l11111ll1l_opy_)
        entries = hook.get(TestFramework.bstack1l1111ll1ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l111llll1l_opy_, []))
        return entries
    def bstack1l1l1ll111l_opy_(self, instance: bstack1lll11l1111_opy_, bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_]):
        bstack1l11111ll1l_opy_ = (
            PytestBDDFramework.bstack1l1111l111l_opy_
            if bstack1lllll1llll_opy_[1] == bstack1lll111l1l1_opy_.PRE
            else PytestBDDFramework.bstack1l1111l11ll_opy_
        )
        PytestBDDFramework.bstack1l111llll11_opy_(instance, bstack1l11111ll1l_opy_)
        TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l111llll1l_opy_, []).clear()
    @staticmethod
    def bstack1l111111ll1_opy_(instance: bstack1lll11l1111_opy_, bstack1l11111ll1l_opy_: str):
        bstack1l1111ll111_opy_ = (
            PytestBDDFramework.bstack1l1111l11l1_opy_
            if bstack1l11111ll1l_opy_ == PytestBDDFramework.bstack1l1111l11ll_opy_
            else PytestBDDFramework.bstack1l111lll1ll_opy_
        )
        bstack1l1111lll1l_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l11111ll1l_opy_, None)
        bstack1l111l1lll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l1111ll111_opy_, None) if bstack1l1111lll1l_opy_ else None
        return (
            bstack1l111l1lll1_opy_[bstack1l1111lll1l_opy_][-1]
            if isinstance(bstack1l111l1lll1_opy_, dict) and len(bstack1l111l1lll1_opy_.get(bstack1l1111lll1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111llll11_opy_(instance: bstack1lll11l1111_opy_, bstack1l11111ll1l_opy_: str):
        hook = PytestBDDFramework.bstack1l111111ll1_opy_(instance, bstack1l11111ll1l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111ll1ll_opy_, []).clear()
    @staticmethod
    def __11llllll111_opy_(instance: bstack1lll11l1111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11ll1_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᓌ"), None)):
            return
        if os.getenv(bstack1l11ll1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᓍ"), bstack1l11ll1_opy_ (u"ࠨ࠱ࠣᓎ")) != bstack1l11ll1_opy_ (u"ࠢ࠲ࠤᓏ"):
            PytestBDDFramework.logger.warning(bstack1l11ll1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᓐ"))
            return
        bstack1l111lll11l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᓑ"): (PytestBDDFramework.bstack1l1111l111l_opy_, PytestBDDFramework.bstack1l111lll1ll_opy_),
            bstack1l11ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᓒ"): (PytestBDDFramework.bstack1l1111l11ll_opy_, PytestBDDFramework.bstack1l1111l11l1_opy_),
        }
        for when in (bstack1l11ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᓓ"), bstack1l11ll1_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᓔ"), bstack1l11ll1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᓕ")):
            bstack11lllll1lll_opy_ = args[1].get_records(when)
            if not bstack11lllll1lll_opy_:
                continue
            records = [
                bstack1ll1lll1l11_opy_(
                    kind=TestFramework.bstack1l1ll1l1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11ll1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᓖ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11ll1_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᓗ")) and r.created
                        else None
                    ),
                )
                for r in bstack11lllll1lll_opy_
                if isinstance(getattr(r, bstack1l11ll1_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᓘ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111l11l1l_opy_, bstack1l1111ll111_opy_ = bstack1l111lll11l_opy_.get(when, (None, None))
            bstack1l1111l1ll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l111l11l1l_opy_, None) if bstack1l111l11l1l_opy_ else None
            bstack1l111l1lll1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, bstack1l1111ll111_opy_, None) if bstack1l1111l1ll1_opy_ else None
            if isinstance(bstack1l111l1lll1_opy_, dict) and len(bstack1l111l1lll1_opy_.get(bstack1l1111l1ll1_opy_, [])) > 0:
                hook = bstack1l111l1lll1_opy_[bstack1l1111l1ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111ll1ll_opy_ in hook:
                    hook[TestFramework.bstack1l1111ll1ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l111llll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11111lll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack111lllll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1111111l1_opy_(request.node, scenario)
        bstack1l111l1l111_opy_ = feature.filename
        if not bstack111lllll1_opy_ or not test_name or not bstack1l111l1l111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll111ll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l11111l_opy_: bstack111lllll1_opy_,
            TestFramework.bstack1ll11llll1l_opy_: test_name,
            TestFramework.bstack1l1l1l111l1_opy_: bstack111lllll1_opy_,
            TestFramework.bstack1l111111l11_opy_: bstack1l111l1l111_opy_,
            TestFramework.bstack1l111ll111l_opy_: PytestBDDFramework.__1l11111llll_opy_(feature, scenario),
            TestFramework.bstack11lllll1ll1_opy_: code,
            TestFramework.bstack1l1l1111ll1_opy_: TestFramework.bstack1l111111lll_opy_,
            TestFramework.bstack1l11l1l11l1_opy_: test_name
        }
    @staticmethod
    def __1l1111111l1_opy_(node, scenario):
        if hasattr(node, bstack1l11ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᓙ")):
            parts = node.nodeid.rsplit(bstack1l11ll1_opy_ (u"ࠦࡠࠨᓚ"))
            params = parts[-1]
            return bstack1l11ll1_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᓛ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11111llll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l11ll1_opy_ (u"࠭ࡴࡢࡩࡶࠫᓜ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l11ll1_opy_ (u"ࠧࡵࡣࡪࡷࠬᓝ")) else [])
    @staticmethod
    def __1l111l1111l_opy_(location):
        return bstack1l11ll1_opy_ (u"ࠣ࠼࠽ࠦᓞ").join(filter(lambda x: isinstance(x, str), location))