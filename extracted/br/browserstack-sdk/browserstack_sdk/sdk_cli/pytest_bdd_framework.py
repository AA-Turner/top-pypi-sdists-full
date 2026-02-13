# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l111ll_opy_ import bstack11ll1l1l1l1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1l1lllllll1_opy_,
    bstack1ll11l111ll_opy_,
    bstack1l1lllll1ll_opy_,
    bstack11ll1l1llll_opy_,
    bstack1l1lll1l11l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l11l11l11l_opy_
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l111_opy_ import bstack1ll11lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lll11l111l_opy_
bstack1l11l1ll11l_opy_ = bstack1l11l11l11l_opy_()
bstack1l111l1l1l1_opy_ = bstack11l11_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᗼ")
bstack11ll1l1111l_opy_ = bstack11l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᗽ")
bstack11l1ll1ll11_opy_ = bstack11l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᗾ")
bstack11ll1111111_opy_ = 1.0
_1l111lll1ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l1lllll11_opy_ = bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᗿ")
    bstack11l1lll11ll_opy_ = bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᘀ")
    bstack11ll111111l_opy_ = bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᘁ")
    bstack11ll1l11111_opy_ = bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᘂ")
    bstack11ll1ll1l1l_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᘃ")
    bstack11ll11l1ll1_opy_: bool
    bstack1lll111lll1_opy_: bstack1lll11l111l_opy_  = None
    bstack11l1ll1l1l1_opy_ = [
        bstack1l1lllllll1_opy_.BEFORE_ALL,
        bstack1l1lllllll1_opy_.AFTER_ALL,
        bstack1l1lllllll1_opy_.BEFORE_EACH,
        bstack1l1lllllll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll111lll1_opy_: Dict[str, str],
        bstack1l1l1l11l1l_opy_: List[str]=[bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᘄ")],
        bstack1lll111lll1_opy_: bstack1lll11l111l_opy_ = None,
        bstack1ll1l1l1lll_opy_=None
    ):
        super().__init__(bstack1l1l1l11l1l_opy_, bstack11ll111lll1_opy_, bstack1lll111lll1_opy_)
        self.bstack11ll11l1ll1_opy_ = any(bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᘅ") in item.lower() for item in bstack1l1l1l11l1l_opy_)
        self.bstack1ll1l1l1lll_opy_ = bstack1ll1l1l1lll_opy_
    def track_event(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1l1lllllll1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11l1ll1l1l1_opy_:
            bstack11ll1l1l1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1l1lllllll1_opy_.NONE:
            self.logger.warning(bstack11l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᘆ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠦࠧᘇ"))
            return
        if not self.bstack11ll11l1ll1_opy_:
            self.logger.warning(bstack11l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᘈ") + str(str(self.bstack1l1l1l11l1l_opy_)) + bstack11l11_opy_ (u"ࠨࠢᘉ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᘊ") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤᘋ"))
            return
        instance = self.__11ll1l111l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᘌ") + str(args) + bstack11l11_opy_ (u"ࠥࠦᘍ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll1l1l1_opy_ and test_hook_state == bstack1l1lllll1ll_opy_.PRE:
                bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11l1llllll_opy_.value)
                name = str(EVENTS.bstack11l1llllll_opy_.name)+bstack11l11_opy_ (u"ࠦ࠿ࠨᘎ")+str(test_framework_state.name)
                TestFramework.bstack11ll1111lll_opy_(instance, name, bstack1l111l111l_opy_)
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᘏ").format(e))
        try:
            if test_framework_state == bstack1l1lllllll1_opy_.TEST:
                if not TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack11ll1ll11ll_opy_) and test_hook_state == bstack1l1lllll1ll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll11l11ll_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l11_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᘐ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠢࠣᘑ"))
                if test_hook_state == bstack1l1lllll1ll_opy_.PRE and not TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l111ll1l1l_opy_):
                    TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l111ll1l1l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11ll11111l1_opy_(instance, args)
                    self.logger.debug(bstack11l11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᘒ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠤࠥᘓ"))
                elif test_hook_state == bstack1l1lllll1ll_opy_.POST and not TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l11l1ll111_opy_):
                    TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1ll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l11_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᘔ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠦࠧᘕ"))
            elif test_framework_state == bstack1l1lllllll1_opy_.STEP:
                if test_hook_state == bstack1l1lllll1ll_opy_.PRE:
                    PytestBDDFramework.__11ll1lll11l_opy_(instance, args)
                elif test_hook_state == bstack1l1lllll1ll_opy_.POST:
                    PytestBDDFramework.__11l1lllllll_opy_(instance, args)
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG and test_hook_state == bstack1l1lllll1ll_opy_.POST:
                PytestBDDFramework.__11l1ll1l1ll_opy_(instance, *args)
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG_REPORT and test_hook_state == bstack1l1lllll1ll_opy_.POST:
                self.__11l1lll1111_opy_(instance, *args)
                self.__11l1llll1ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11l1ll1l1l1_opy_:
                self.__11ll11l1lll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᘖ") + str(instance.ref()) + bstack11l11_opy_ (u"ࠨࠢᘗ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1lll1lll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11l1ll1l1l1_opy_ and test_hook_state == bstack1l1lllll1ll_opy_.POST:
                name = str(EVENTS.bstack11l1llllll_opy_.name)+bstack11l11_opy_ (u"ࠢ࠻ࠤᘘ")+str(test_framework_state.name)
                bstack1l111l111l_opy_ = TestFramework.bstack11ll1111l11_opy_(instance, name)
                bstack111l1lllll_opy_.end(EVENTS.bstack11l1llllll_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘙ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘚ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᘛ").format(e))
    def bstack1l11l1lll1l_opy_(self):
        return self.bstack11ll11l1ll1_opy_
    def __11ll11lll1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᘜ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11ll1ll11_opy_(rep, [bstack11l11_opy_ (u"ࠧࡽࡨࡦࡰࠥᘝ"), bstack11l11_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᘞ"), bstack11l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᘟ"), bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᘠ"), bstack11l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᘡ"), bstack11l11_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᘢ")])
        return None
    def __11l1lll1111_opy_(self, instance: bstack1ll11l111ll_opy_, *args):
        result = self.__11ll11lll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1l11lll_opy_ = None
        if result.get(bstack11l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᘣ"), None) == bstack11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᘤ") and len(args) > 1 and getattr(args[1], bstack11l11_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᘥ"), None) is not None:
            failure = [{bstack11l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᘦ"): [args[1].excinfo.exconly(), result.get(bstack11l11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᘧ"), None)]}]
            bstack1lll1l11lll_opy_ = bstack11l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᘨ") if bstack11l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᘩ") in getattr(args[1].excinfo, bstack11l11_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᘪ"), bstack11l11_opy_ (u"ࠧࠨᘫ")) else bstack11l11_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᘬ")
        bstack11ll11ll111_opy_ = result.get(bstack11l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᘭ"), TestFramework.bstack11ll11lll11_opy_)
        if bstack11ll11ll111_opy_ != TestFramework.bstack11ll11lll11_opy_:
            TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l111llll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1l11l1l_opy_(instance, {
            TestFramework.bstack1l111111111_opy_: failure,
            TestFramework.bstack11ll11l11l1_opy_: bstack1lll1l11lll_opy_,
            TestFramework.bstack1l111111l1l_opy_: bstack11ll11ll111_opy_,
        })
    def __11ll1l111l1_opy_(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1l1lllllll1_opy_.SETUP_FIXTURE:
            instance = self.__11ll1ll11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1111l1l_opy_ bstack11ll1l11l11_opy_ this to be bstack11l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᘮ")
            if test_framework_state == bstack1l1lllllll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll11llll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᘯ"), None), bstack11l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᘰ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l11_opy_ (u"ࠦࡳࡵࡤࡦࠤᘱ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᘲ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1ll11111_opy_(target) if target else None
        return instance
    def __11ll11l1lll_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1l1l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, PytestBDDFramework.bstack11l1lll11ll_opy_, {})
        if not key in bstack11l1lll1l1l_opy_:
            bstack11l1lll1l1l_opy_[key] = []
        bstack11l1lll1l11_opy_ = TestFramework.bstack1lll111111l_opy_(instance, PytestBDDFramework.bstack11ll111111l_opy_, {})
        if not key in bstack11l1lll1l11_opy_:
            bstack11l1lll1l11_opy_[key] = []
        bstack11ll1l1l111_opy_ = {
            PytestBDDFramework.bstack11l1lll11ll_opy_: bstack11l1lll1l1l_opy_,
            PytestBDDFramework.bstack11ll111111l_opy_: bstack11l1lll1l11_opy_,
        }
        if test_hook_state == bstack1l1lllll1ll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l11_opy_ (u"ࠨ࡫ࡦࡻࠥᘳ"): key,
                TestFramework.bstack11l1ll1l11l_opy_: uuid4().__str__(),
                TestFramework.bstack11ll111ll1l_opy_: TestFramework.bstack11ll1lll111_opy_,
                TestFramework.bstack11ll11l1l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll1ll1l_opy_: [],
                TestFramework.bstack11l1llll11l_opy_: hook_name,
                TestFramework.bstack11ll1ll1111_opy_: bstack1ll11lll1l1_opy_.bstack11ll11l1111_opy_()
            }
            bstack11l1lll1l1l_opy_[key].append(hook)
            bstack11ll1l1l111_opy_[PytestBDDFramework.bstack11ll1l11111_opy_] = key
        elif test_hook_state == bstack1l1lllll1ll_opy_.POST:
            bstack11ll11ll1ll_opy_ = bstack11l1lll1l1l_opy_.get(key, [])
            hook = bstack11ll11ll1ll_opy_.pop() if bstack11ll11ll1ll_opy_ else None
            if hook:
                result = self.__11ll11lll1l_opy_(*args)
                if result:
                    bstack11l1lll111l_opy_ = result.get(bstack11l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᘴ"), TestFramework.bstack11ll1lll111_opy_)
                    if bstack11l1lll111l_opy_ != TestFramework.bstack11ll1lll111_opy_:
                        hook[TestFramework.bstack11ll111ll1l_opy_] = bstack11l1lll111l_opy_
                hook[TestFramework.bstack11l1llll111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1ll1111_opy_] = bstack1ll11lll1l1_opy_.bstack11ll11l1111_opy_()
                self.bstack11ll1ll1lll_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll11ll1l1_opy_, [])
                self.bstack1l11l11l111_opy_(instance, logs)
                bstack11l1lll1l11_opy_[key].append(hook)
                bstack11ll1l1l111_opy_[PytestBDDFramework.bstack11ll1ll1l1l_opy_] = key
        TestFramework.bstack11ll1l11l1l_opy_(instance, bstack11ll1l1l111_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᘵ") + str(bstack11l1lll1l11_opy_) + bstack11l11_opy_ (u"ࠤࠥᘶ"))
    def __11ll1ll11l1_opy_(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11ll1ll11_opy_(args[0], [bstack11l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᘷ"), bstack11l11_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᘸ"), bstack11l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᘹ"), bstack11l11_opy_ (u"ࠨࡩࡥࡵࠥᘺ"), bstack11l11_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᘻ"), bstack11l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᘼ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᘽ")) else fixturedef.get(bstack11l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᘾ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l11_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᘿ")) else None
        node = request.node if hasattr(request, bstack11l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᙀ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᙁ")) else None
        baseid = fixturedef.get(bstack11l11_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᙂ"), None) or bstack11l11_opy_ (u"ࠣࠤᙃ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l11_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᙄ")):
            target = PytestBDDFramework.__11l1llllll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l11_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᙅ")) else None
            if target and not TestFramework.bstack1ll1ll11111_opy_(target):
                self.__11ll11llll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᙆ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠧࠨᙇ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᙈ") + str(target) + bstack11l11_opy_ (u"ࠢࠣᙉ"))
            return None
        instance = TestFramework.bstack1ll1ll11111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᙊ") + str(target) + bstack11l11_opy_ (u"ࠤࠥᙋ"))
            return None
        bstack11ll111l1ll_opy_ = TestFramework.bstack1lll111111l_opy_(instance, PytestBDDFramework.bstack11l1lllll11_opy_, {})
        if os.getenv(bstack11l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᙌ"), bstack11l11_opy_ (u"ࠦ࠶ࠨᙍ")) == bstack11l11_opy_ (u"ࠧ࠷ࠢᙎ"):
            bstack11ll111l11l_opy_ = bstack11l11_opy_ (u"ࠨ࠺ࠣᙏ").join((scope, fixturename))
            bstack11ll1l1l1ll_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll11111ll_opy_ = {
                bstack11l11_opy_ (u"ࠢ࡬ࡧࡼࠦᙐ"): bstack11ll111l11l_opy_,
                bstack11l11_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᙑ"): PytestBDDFramework.__11ll11ll11l_opy_(request.node, scenario),
                bstack11l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᙒ"): fixturedef,
                bstack11l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᙓ"): scope,
                bstack11l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᙔ"): None,
            }
            try:
                if test_hook_state == bstack1l1lllll1ll_opy_.POST and callable(getattr(args[-1], bstack11l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᙕ"), None)):
                    bstack11ll11111ll_opy_[bstack11l11_opy_ (u"ࠨࡴࡺࡲࡨࠦᙖ")] = TestFramework.bstack1l11ll1l1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1l1lllll1ll_opy_.PRE:
                bstack11ll11111ll_opy_[bstack11l11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᙗ")] = uuid4().__str__()
                bstack11ll11111ll_opy_[PytestBDDFramework.bstack11ll11l1l1l_opy_] = bstack11ll1l1l1ll_opy_
            elif test_hook_state == bstack1l1lllll1ll_opy_.POST:
                bstack11ll11111ll_opy_[PytestBDDFramework.bstack11l1llll111_opy_] = bstack11ll1l1l1ll_opy_
            if bstack11ll111l11l_opy_ in bstack11ll111l1ll_opy_:
                bstack11ll111l1ll_opy_[bstack11ll111l11l_opy_].update(bstack11ll11111ll_opy_)
                self.logger.debug(bstack11l11_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᙘ") + str(bstack11ll111l1ll_opy_[bstack11ll111l11l_opy_]) + bstack11l11_opy_ (u"ࠤࠥᙙ"))
            else:
                bstack11ll111l1ll_opy_[bstack11ll111l11l_opy_] = bstack11ll11111ll_opy_
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᙚ") + str(len(bstack11ll111l1ll_opy_)) + bstack11l11_opy_ (u"ࠦࠧᙛ"))
        TestFramework.bstack1ll1lll111l_opy_(instance, PytestBDDFramework.bstack11l1lllll11_opy_, bstack11ll111l1ll_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᙜ") + str(instance.ref()) + bstack11l11_opy_ (u"ࠨࠢᙝ"))
        return instance
    def __11ll11llll1_opy_(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1llll111_opy_.create_context(target)
        ob = bstack1ll11l111ll_opy_(ctx, self.bstack1l1l1l11l1l_opy_, self.bstack11ll111lll1_opy_, test_framework_state)
        TestFramework.bstack11ll1l11l1l_opy_(ob, {
            TestFramework.bstack1l1l1l11l11_opy_: context.test_framework_name,
            TestFramework.bstack1l11l111l11_opy_: context.test_framework_version,
            TestFramework.bstack11ll111llll_opy_: [],
            PytestBDDFramework.bstack11l1lllll11_opy_: {},
            PytestBDDFramework.bstack11ll111111l_opy_: {},
            PytestBDDFramework.bstack11l1lll11ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1lll111l_opy_(ob, TestFramework.bstack11ll1l111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1lll111l_opy_(ob, TestFramework.bstack1l1l111l11l_opy_, context.platform_index)
        TestFramework.bstack1lll111l1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack11l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᙞ") + str(TestFramework.bstack1lll111l1l1_opy_.keys()) + bstack11l11_opy_ (u"ࠣࠤᙟ"))
        return ob
    @staticmethod
    def __11ll11111l1_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l11_opy_ (u"ࠩ࡬ࡨࠬᙠ"): id(step),
                bstack11l11_opy_ (u"ࠪࡸࡪࡾࡴࠨᙡ"): step.name,
                bstack11l11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᙢ"): step.keyword,
            })
        meta = {
            bstack11l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᙣ"): {
                bstack11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙤ"): feature.name,
                bstack11l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᙥ"): feature.filename,
                bstack11l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᙦ"): feature.description
            },
            bstack11l11_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᙧ"): {
                bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᙨ"): scenario.name
            },
            bstack11l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᙩ"): steps,
            bstack11l11_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᙪ"): PytestBDDFramework.__11l1lllll1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11ll1l1ll1l_opy_: meta
            }
        )
    def bstack11ll1ll1lll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᙫ")
        global _1l111lll1ll_opy_
        platform_index = os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᙬ")]
        bstack1l11l1111ll_opy_ = os.path.join(bstack1l11l1ll11l_opy_, (bstack1l111l1l1l1_opy_ + str(platform_index)), bstack11ll1l1111l_opy_)
        if not os.path.exists(bstack1l11l1111ll_opy_) or not os.path.isdir(bstack1l11l1111ll_opy_):
            return
        logs = hook.get(bstack11l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᙭"), [])
        with os.scandir(bstack1l11l1111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111lll1ll_opy_:
                    self.logger.info(bstack11l11_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢ᙮").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l11_opy_ (u"ࠥࠦᙯ")
                    log_entry = bstack1l1lll1l11l_opy_(
                        kind=bstack11l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᙰ"),
                        message=bstack11l11_opy_ (u"ࠧࠨᙱ"),
                        level=bstack11l11_opy_ (u"ࠨࠢᙲ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111ll11l1_opy_=entry.stat().st_size,
                        bstack1l11l11ll1l_opy_=bstack11l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᙳ"),
                        bstack1111l1_opy_=os.path.abspath(entry.path),
                        bstack11ll1ll1l11_opy_=hook.get(TestFramework.bstack11l1ll1l11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111lll1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᙴ")]
        bstack11l1ll1llll_opy_ = os.path.join(bstack1l11l1ll11l_opy_, (bstack1l111l1l1l1_opy_ + str(platform_index)), bstack11ll1l1111l_opy_, bstack11l1ll1ll11_opy_)
        if not os.path.exists(bstack11l1ll1llll_opy_) or not os.path.isdir(bstack11l1ll1llll_opy_):
            self.logger.info(bstack11l11_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᙵ").format(bstack11l1ll1llll_opy_))
        else:
            self.logger.info(bstack11l11_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᙶ").format(bstack11l1ll1llll_opy_))
            with os.scandir(bstack11l1ll1llll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111lll1ll_opy_:
                        self.logger.info(bstack11l11_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᙷ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l11_opy_ (u"ࠧࠨᙸ")
                        log_entry = bstack1l1lll1l11l_opy_(
                            kind=bstack11l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᙹ"),
                            message=bstack11l11_opy_ (u"ࠢࠣᙺ"),
                            level=bstack11l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᙻ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111ll11l1_opy_=entry.stat().st_size,
                            bstack1l11l11ll1l_opy_=bstack11l11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᙼ"),
                            bstack1111l1_opy_=os.path.abspath(entry.path),
                            bstack1l111lll1l1_opy_=hook.get(TestFramework.bstack11l1ll1l11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111lll1ll_opy_.add(abs_path)
        hook[bstack11l11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᙽ")] = logs
    def bstack1l11l11l111_opy_(
        self,
        bstack1l111l1ll1l_opy_: bstack1ll11l111ll_opy_,
        entries: List[bstack1l1lll1l11l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᙾ"))
        req.platform_index = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l111l11l_opy_)
        req.client_worker_id = bstack11l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᙿ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111l1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111l1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111l1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l1l11l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l11l111l11_opy_)
            log_entry.uuid = entry.bstack11ll1ll1l11_opy_ if entry.bstack11ll1ll1l11_opy_ else TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l11l11l1_opy_)
            log_entry.test_framework_state = bstack1l111l1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ "))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᚁ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111ll11l1_opy_
                log_entry.file_path = entry.bstack1111l1_opy_
        def bstack1l11ll11l1l_opy_():
            bstack1lllll111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1lll_opy_.LogCreatedEvent(req)
                bstack1l111l1ll1l_opy_.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᚂ"), datetime.now() - bstack1lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᚃ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll111lll1_opy_.enqueue(bstack1l11ll11l1l_opy_)
    def __11l1llll1ll_opy_(self, instance) -> None:
        bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᚄ")
        bstack11ll1l1l111_opy_ = {bstack11l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᚅ"): bstack1ll11lll1l1_opy_.bstack11ll11l1111_opy_()}
        TestFramework.bstack11ll1l11l1l_opy_(instance, bstack11ll1l1l111_opy_)
    @staticmethod
    def __11ll1lll11l_opy_(instance, args):
        request, bstack11ll1l1lll1_opy_ = args
        bstack11ll11lllll_opy_ = id(bstack11ll1l1lll1_opy_)
        bstack11ll1l11ll1_opy_ = instance.data[TestFramework.bstack11ll1l1ll1l_opy_]
        step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠬ࡯ࡤࠨᚆ")] == bstack11ll11lllll_opy_, bstack11ll1l11ll1_opy_[bstack11l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚇ")]), None)
        step.update({
            bstack11l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚈ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11ll1l11ll1_opy_[bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚉ")]) if st[bstack11l11_opy_ (u"ࠩ࡬ࡨࠬᚊ")] == step[bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭ᚋ")]), None)
        if index is not None:
            bstack11ll1l11ll1_opy_[bstack11l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚌ")][index] = step
        instance.data[TestFramework.bstack11ll1l1ll1l_opy_] = bstack11ll1l11ll1_opy_
    @staticmethod
    def __11l1lllllll_opy_(instance, args):
        bstack11l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᚍ")
        bstack11l1ll1l111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll1l1lll1_opy_ = args[1]
        bstack11ll11lllll_opy_ = id(bstack11ll1l1lll1_opy_)
        bstack11ll1l11ll1_opy_ = instance.data[TestFramework.bstack11ll1l1ll1l_opy_]
        step = None
        if bstack11ll11lllll_opy_ is not None and bstack11ll1l11ll1_opy_.get(bstack11l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚎ")):
            step = next(filter(lambda st: st[bstack11l11_opy_ (u"ࠧࡪࡦࠪᚏ")] == bstack11ll11lllll_opy_, bstack11ll1l11ll1_opy_[bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚐ")]), None)
            step.update({
                bstack11l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚑ"): bstack11l1ll1l111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᚒ"): bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚓ"),
                bstack11l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᚔ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᚕ"): bstack11l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᚖ"),
                })
        index = next((i for i, st in enumerate(bstack11ll1l11ll1_opy_[bstack11l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚗ")]) if st[bstack11l11_opy_ (u"ࠩ࡬ࡨࠬᚘ")] == step[bstack11l11_opy_ (u"ࠪ࡭ࡩ࠭ᚙ")]), None)
        if index is not None:
            bstack11ll1l11ll1_opy_[bstack11l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚚ")][index] = step
        instance.data[TestFramework.bstack11ll1l1ll1l_opy_] = bstack11ll1l11ll1_opy_
    @staticmethod
    def __11l1lllll1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ᚛")):
                examples = list(node.callspec.params[bstack11l11_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬ᚜")].values())
            return examples
        except:
            return []
    def bstack1l11l11lll1_opy_(self, instance: bstack1ll11l111ll_opy_, bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_]):
        bstack11l1ll1lll1_opy_ = (
            PytestBDDFramework.bstack11ll1l11111_opy_
            if bstack1ll1l1lll1l_opy_[1] == bstack1l1lllll1ll_opy_.PRE
            else PytestBDDFramework.bstack11ll1ll1l1l_opy_
        )
        hook = PytestBDDFramework.bstack11ll111l111_opy_(instance, bstack11l1ll1lll1_opy_)
        entries = hook.get(TestFramework.bstack11l1ll1ll1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack11ll111llll_opy_, []))
        return entries
    def bstack1l111llll11_opy_(self, instance: bstack1ll11l111ll_opy_, bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_]):
        bstack11l1ll1lll1_opy_ = (
            PytestBDDFramework.bstack11ll1l11111_opy_
            if bstack1ll1l1lll1l_opy_[1] == bstack1l1lllll1ll_opy_.PRE
            else PytestBDDFramework.bstack11ll1ll1l1l_opy_
        )
        PytestBDDFramework.bstack11l1lll1ll1_opy_(instance, bstack11l1ll1lll1_opy_)
        TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack11ll111llll_opy_, []).clear()
    @staticmethod
    def bstack11ll111l111_opy_(instance: bstack1ll11l111ll_opy_, bstack11l1ll1lll1_opy_: str):
        bstack11l1lll11l1_opy_ = (
            PytestBDDFramework.bstack11ll111111l_opy_
            if bstack11l1ll1lll1_opy_ == PytestBDDFramework.bstack11ll1ll1l1l_opy_
            else PytestBDDFramework.bstack11l1lll11ll_opy_
        )
        bstack11ll1ll111l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11l1ll1lll1_opy_, None)
        bstack11ll1l1l11l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11l1lll11l1_opy_, None) if bstack11ll1ll111l_opy_ else None
        return (
            bstack11ll1l1l11l_opy_[bstack11ll1ll111l_opy_][-1]
            if isinstance(bstack11ll1l1l11l_opy_, dict) and len(bstack11ll1l1l11l_opy_.get(bstack11ll1ll111l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1lll1ll1_opy_(instance: bstack1ll11l111ll_opy_, bstack11l1ll1lll1_opy_: str):
        hook = PytestBDDFramework.bstack11ll111l111_opy_(instance, bstack11l1ll1lll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll1ll1l_opy_, []).clear()
    @staticmethod
    def __11l1ll1l1ll_opy_(instance: bstack1ll11l111ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧ᚝"), None)):
            return
        if os.getenv(bstack11l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧ᚞"), bstack11l11_opy_ (u"ࠤ࠴ࠦ᚟")) != bstack11l11_opy_ (u"ࠥ࠵ࠧᚠ"):
            PytestBDDFramework.logger.warning(bstack11l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᚡ"))
            return
        bstack11l1llll1l1_opy_ = {
            bstack11l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᚢ"): (PytestBDDFramework.bstack11ll1l11111_opy_, PytestBDDFramework.bstack11l1lll11ll_opy_),
            bstack11l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᚣ"): (PytestBDDFramework.bstack11ll1ll1l1l_opy_, PytestBDDFramework.bstack11ll111111l_opy_),
        }
        for when in (bstack11l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᚤ"), bstack11l11_opy_ (u"ࠣࡥࡤࡰࡱࠨᚥ"), bstack11l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᚦ")):
            bstack11ll1l1ll11_opy_ = args[1].get_records(when)
            if not bstack11ll1l1ll11_opy_:
                continue
            records = [
                bstack1l1lll1l11l_opy_(
                    kind=TestFramework.bstack1l11ll1l111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᚧ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᚨ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll1l1ll11_opy_
                if isinstance(getattr(r, bstack11l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᚩ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll1111ll1_opy_, bstack11l1lll11l1_opy_ = bstack11l1llll1l1_opy_.get(when, (None, None))
            bstack11ll11l111l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11ll1111ll1_opy_, None) if bstack11ll1111ll1_opy_ else None
            bstack11ll1l1l11l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11l1lll11l1_opy_, None) if bstack11ll11l111l_opy_ else None
            if isinstance(bstack11ll1l1l11l_opy_, dict) and len(bstack11ll1l1l11l_opy_.get(bstack11ll11l111l_opy_, [])) > 0:
                hook = bstack11ll1l1l11l_opy_[bstack11ll11l111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll1ll1l_opy_ in hook:
                    hook[TestFramework.bstack11l1ll1ll1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack11ll111llll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll11l11ll_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1lllll11ll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__11ll111ll11_opy_(request.node, scenario)
        bstack11ll1ll1ll1_opy_ = feature.filename
        if not bstack1lllll11ll_opy_ or not test_name or not bstack11ll1ll1ll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l11l11l1_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1ll11ll_opy_: bstack1lllll11ll_opy_,
            TestFramework.bstack1l1ll11111l_opy_: test_name,
            TestFramework.bstack1l111l11111_opy_: bstack1lllll11ll_opy_,
            TestFramework.bstack11ll111l1l1_opy_: bstack11ll1ll1ll1_opy_,
            TestFramework.bstack11ll1l11lll_opy_: PytestBDDFramework.__11ll11ll11l_opy_(feature, scenario),
            TestFramework.bstack11ll11l1l11_opy_: code,
            TestFramework.bstack1l111111l1l_opy_: TestFramework.bstack11ll11lll11_opy_,
            TestFramework.bstack11lll11ll11_opy_: test_name
        }
    @staticmethod
    def __11ll111ll11_opy_(node, scenario):
        if hasattr(node, bstack11l11_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᚪ")):
            parts = node.nodeid.rsplit(bstack11l11_opy_ (u"ࠢ࡜ࠤᚫ"))
            params = parts[-1]
            return bstack11l11_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᚬ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll11ll11l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᚭ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᚮ")) else [])
    @staticmethod
    def __11l1llllll1_opy_(location):
        return bstack11l11_opy_ (u"ࠦ࠿ࡀࠢᚯ").join(filter(lambda x: isinstance(x, str), location))