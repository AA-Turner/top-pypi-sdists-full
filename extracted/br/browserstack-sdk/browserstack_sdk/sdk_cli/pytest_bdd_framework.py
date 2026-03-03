# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1111ll1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lllll11_opy_ import bstack11ll111llll_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll11l1l_opy_,
    bstack1ll1l111111_opy_,
    bstack1l1llll1l1l_opy_,
    bstack11l1llllll1_opy_,
    bstack1ll1l1l11ll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l11llll11l_opy_
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1llll_opy_ import bstack1ll11ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lll11lll11_opy_
bstack1l11lll1111_opy_ = bstack1l11llll11l_opy_()
bstack1l11lll1l11_opy_ = bstack11ll111_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᘃ")
bstack11ll1l11ll1_opy_ = bstack11ll111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᘄ")
bstack11ll11l11l1_opy_ = bstack11ll111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᘅ")
bstack11ll11l111l_opy_ = 1.0
_1l11l1ll1l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l1llll1l1_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᘆ")
    bstack11ll11lllll_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᘇ")
    bstack11l1llll1ll_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᘈ")
    bstack11lll111l11_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᘉ")
    bstack11ll11l1l11_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᘊ")
    bstack11ll1ll11ll_opy_: bool
    bstack1lll11llll1_opy_: bstack1lll11lll11_opy_  = None
    bstack11ll1l1l11l_opy_ = [
        bstack1ll1ll11l1l_opy_.BEFORE_ALL,
        bstack1ll1ll11l1l_opy_.AFTER_ALL,
        bstack1ll1ll11l1l_opy_.BEFORE_EACH,
        bstack1ll1ll11l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll1l1111l_opy_: Dict[str, str],
        bstack1l1l1ll1l1l_opy_: List[str]=[bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᘋ")],
        bstack1lll11llll1_opy_: bstack1lll11lll11_opy_ = None,
        bstack1l1llllll1l_opy_=None
    ):
        super().__init__(bstack1l1l1ll1l1l_opy_, bstack11ll1l1111l_opy_, bstack1lll11llll1_opy_)
        self.bstack11ll1ll11ll_opy_ = any(bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᘌ") in item.lower() for item in bstack1l1l1ll1l1l_opy_)
        self.bstack1l1llllll1l_opy_ = bstack1l1llllll1l_opy_
    def track_event(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll11l1l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11ll1l1l11l_opy_:
            bstack11ll111llll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll11l1l_opy_.NONE:
            self.logger.warning(bstack11ll111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᘍ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠦࠧᘎ"))
            return
        if not self.bstack11ll1ll11ll_opy_:
            self.logger.warning(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᘏ") + str(str(self.bstack1l1l1ll1l1l_opy_)) + bstack11ll111_opy_ (u"ࠨࠢᘐ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᘑ") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤᘒ"))
            return
        instance = self.__11ll1l111ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᘓ") + str(args) + bstack11ll111_opy_ (u"ࠥࠦᘔ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11ll1l1l11l_opy_ and test_hook_state == bstack1l1llll1l1l_opy_.PRE:
                bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1ll1ll1l11_opy_.value)
                name = str(EVENTS.bstack1ll1ll1l11_opy_.name)+bstack11ll111_opy_ (u"ࠦ࠿ࠨᘕ")+str(test_framework_state.name)
                TestFramework.bstack11ll1111l1l_opy_(instance, name, bstack11llllllll_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᘖ").format(e))
        try:
            if test_framework_state == bstack1ll1ll11l1l_opy_.TEST:
                if not TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11ll1l1llll_opy_) and test_hook_state == bstack1l1llll1l1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll1l11lll_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᘗ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠢࠣᘘ"))
                if test_hook_state == bstack1l1llll1l1l_opy_.PRE and not TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1lll11_opy_):
                    TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11l1lll11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11ll1ll1l1l_opy_(instance, args)
                    self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᘙ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠤࠥᘚ"))
                elif test_hook_state == bstack1l1llll1l1l_opy_.POST and not TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l11llll_opy_):
                    TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᘛ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠦࠧᘜ"))
            elif test_framework_state == bstack1ll1ll11l1l_opy_.STEP:
                if test_hook_state == bstack1l1llll1l1l_opy_.PRE:
                    PytestBDDFramework.__11ll111ll1l_opy_(instance, args)
                elif test_hook_state == bstack1l1llll1l1l_opy_.POST:
                    PytestBDDFramework.__11ll1llll1l_opy_(instance, args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG and test_hook_state == bstack1l1llll1l1l_opy_.POST:
                PytestBDDFramework.__11l1lllll11_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG_REPORT and test_hook_state == bstack1l1llll1l1l_opy_.POST:
                self.__11ll11l1l1l_opy_(instance, *args)
                self.__11ll1l1ll11_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11ll1l1l11l_opy_:
                self.__11ll111111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᘝ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠨࠢᘞ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lll111l1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11ll1l1l11l_opy_ and test_hook_state == bstack1l1llll1l1l_opy_.POST:
                name = str(EVENTS.bstack1ll1ll1l11_opy_.name)+bstack11ll111_opy_ (u"ࠢ࠻ࠤᘟ")+str(test_framework_state.name)
                bstack11llllllll_opy_ = TestFramework.bstack11ll11l1lll_opy_(instance, name)
                bstack1111l1l1l_opy_.end(EVENTS.bstack1ll1ll1l11_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘠ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘡ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᘢ").format(e))
    def bstack1l11l111lll_opy_(self):
        return self.bstack11ll1ll11ll_opy_
    def __11ll1111111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᘣ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11ll111l1_opy_(rep, [bstack11ll111_opy_ (u"ࠧࡽࡨࡦࡰࠥᘤ"), bstack11ll111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᘥ"), bstack11ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᘦ"), bstack11ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᘧ"), bstack11ll111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᘨ"), bstack11ll111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᘩ")])
        return None
    def __11ll11l1l1l_opy_(self, instance: bstack1ll1l111111_opy_, *args):
        result = self.__11ll1111111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll11ll_opy_ = None
        if result.get(bstack11ll111_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᘪ"), None) == bstack11ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᘫ") and len(args) > 1 and getattr(args[1], bstack11ll111_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᘬ"), None) is not None:
            failure = [{bstack11ll111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᘭ"): [args[1].excinfo.exconly(), result.get(bstack11ll111_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᘮ"), None)]}]
            bstack1lll1ll11ll_opy_ = bstack11ll111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᘯ") if bstack11ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᘰ") in getattr(args[1].excinfo, bstack11ll111_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᘱ"), bstack11ll111_opy_ (u"ࠧࠨᘲ")) else bstack11ll111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᘳ")
        bstack11ll11ll1l1_opy_ = result.get(bstack11ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᘴ"), TestFramework.bstack11ll1111lll_opy_)
        if bstack11ll11ll1l1_opy_ != TestFramework.bstack11ll1111lll_opy_:
            TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll11111ll_opy_(instance, {
            TestFramework.bstack1l1111l1l1l_opy_: failure,
            TestFramework.bstack11ll111lll1_opy_: bstack1lll1ll11ll_opy_,
            TestFramework.bstack1l11111l1l1_opy_: bstack11ll11ll1l1_opy_,
        })
    def __11ll1l111ll_opy_(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll11l1l_opy_.SETUP_FIXTURE:
            instance = self.__11ll1ll1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lll1111ll_opy_ bstack11ll111l1l1_opy_ this to be bstack11ll111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᘵ")
            if test_framework_state == bstack1ll1ll11l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll111l1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᘶ"), None), bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᘷ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll111_opy_ (u"ࠦࡳࡵࡤࡦࠤᘸ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᘹ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll1111111_opy_(target) if target else None
        return instance
    def __11ll111111l_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1llll111_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, PytestBDDFramework.bstack11ll11lllll_opy_, {})
        if not key in bstack11l1llll111_opy_:
            bstack11l1llll111_opy_[key] = []
        bstack11ll1l11l1l_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, PytestBDDFramework.bstack11l1llll1ll_opy_, {})
        if not key in bstack11ll1l11l1l_opy_:
            bstack11ll1l11l1l_opy_[key] = []
        bstack11ll11lll1l_opy_ = {
            PytestBDDFramework.bstack11ll11lllll_opy_: bstack11l1llll111_opy_,
            PytestBDDFramework.bstack11l1llll1ll_opy_: bstack11ll1l11l1l_opy_,
        }
        if test_hook_state == bstack1l1llll1l1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11ll111_opy_ (u"ࠨ࡫ࡦࡻࠥᘺ"): key,
                TestFramework.bstack11ll1llllll_opy_: uuid4().__str__(),
                TestFramework.bstack11ll11ll111_opy_: TestFramework.bstack11ll1lllll1_opy_,
                TestFramework.bstack11ll1lll1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll11ll1ll_opy_: [],
                TestFramework.bstack11ll1ll11l1_opy_: hook_name,
                TestFramework.bstack11ll1ll111l_opy_: bstack1ll11ll1l1l_opy_.bstack11ll11l1111_opy_()
            }
            bstack11l1llll111_opy_[key].append(hook)
            bstack11ll11lll1l_opy_[PytestBDDFramework.bstack11lll111l11_opy_] = key
        elif test_hook_state == bstack1l1llll1l1l_opy_.POST:
            bstack11ll1lll111_opy_ = bstack11l1llll111_opy_.get(key, [])
            hook = bstack11ll1lll111_opy_.pop() if bstack11ll1lll111_opy_ else None
            if hook:
                result = self.__11ll1111111_opy_(*args)
                if result:
                    bstack11l1llll11l_opy_ = result.get(bstack11ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᘻ"), TestFramework.bstack11ll1lllll1_opy_)
                    if bstack11l1llll11l_opy_ != TestFramework.bstack11ll1lllll1_opy_:
                        hook[TestFramework.bstack11ll11ll111_opy_] = bstack11l1llll11l_opy_
                hook[TestFramework.bstack11ll1lll11l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1ll111l_opy_] = bstack1ll11ll1l1l_opy_.bstack11ll11l1111_opy_()
                self.bstack11ll1ll1111_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l1ll1l_opy_, [])
                self.bstack1l11l11l1l1_opy_(instance, logs)
                bstack11ll1l11l1l_opy_[key].append(hook)
                bstack11ll11lll1l_opy_[PytestBDDFramework.bstack11ll11l1l11_opy_] = key
        TestFramework.bstack11ll11111ll_opy_(instance, bstack11ll11lll1l_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᘼ") + str(bstack11ll1l11l1l_opy_) + bstack11ll111_opy_ (u"ࠤࠥᘽ"))
    def __11ll1ll1lll_opy_(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11ll111l1_opy_(args[0], [bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᘾ"), bstack11ll111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᘿ"), bstack11ll111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᙀ"), bstack11ll111_opy_ (u"ࠨࡩࡥࡵࠥᙁ"), bstack11ll111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᙂ"), bstack11ll111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᙃ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11ll111_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᙄ")) else fixturedef.get(bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᙅ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᙆ")) else None
        node = request.node if hasattr(request, bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᙇ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᙈ")) else None
        baseid = fixturedef.get(bstack11ll111_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᙉ"), None) or bstack11ll111_opy_ (u"ࠣࠤᙊ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll111_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᙋ")):
            target = PytestBDDFramework.__11l1lllll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll111_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᙌ")) else None
            if target and not TestFramework.bstack1lll1111111_opy_(target):
                self.__11ll111l1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᙍ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠧࠨᙎ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᙏ") + str(target) + bstack11ll111_opy_ (u"ࠢࠣᙐ"))
            return None
        instance = TestFramework.bstack1lll1111111_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᙑ") + str(target) + bstack11ll111_opy_ (u"ࠤࠥᙒ"))
            return None
        bstack11lll111lll_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, PytestBDDFramework.bstack11l1llll1l1_opy_, {})
        if os.getenv(bstack11ll111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᙓ"), bstack11ll111_opy_ (u"ࠦ࠶ࠨᙔ")) == bstack11ll111_opy_ (u"ࠧ࠷ࠢᙕ"):
            bstack11lll111111_opy_ = bstack11ll111_opy_ (u"ࠨ࠺ࠣᙖ").join((scope, fixturename))
            bstack11ll111l111_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll1lll1l1_opy_ = {
                bstack11ll111_opy_ (u"ࠢ࡬ࡧࡼࠦᙗ"): bstack11lll111111_opy_,
                bstack11ll111_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᙘ"): PytestBDDFramework.__11ll111ll11_opy_(request.node, scenario),
                bstack11ll111_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᙙ"): fixturedef,
                bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᙚ"): scope,
                bstack11ll111_opy_ (u"ࠦࡹࡿࡰࡦࠤᙛ"): None,
            }
            try:
                if test_hook_state == bstack1l1llll1l1l_opy_.POST and callable(getattr(args[-1], bstack11ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᙜ"), None)):
                    bstack11ll1lll1l1_opy_[bstack11ll111_opy_ (u"ࠨࡴࡺࡲࡨࠦᙝ")] = TestFramework.bstack1l111ll1lll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1l1llll1l1l_opy_.PRE:
                bstack11ll1lll1l1_opy_[bstack11ll111_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᙞ")] = uuid4().__str__()
                bstack11ll1lll1l1_opy_[PytestBDDFramework.bstack11ll1lll1ll_opy_] = bstack11ll111l111_opy_
            elif test_hook_state == bstack1l1llll1l1l_opy_.POST:
                bstack11ll1lll1l1_opy_[PytestBDDFramework.bstack11ll1lll11l_opy_] = bstack11ll111l111_opy_
            if bstack11lll111111_opy_ in bstack11lll111lll_opy_:
                bstack11lll111lll_opy_[bstack11lll111111_opy_].update(bstack11ll1lll1l1_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᙟ") + str(bstack11lll111lll_opy_[bstack11lll111111_opy_]) + bstack11ll111_opy_ (u"ࠤࠥᙠ"))
            else:
                bstack11lll111lll_opy_[bstack11lll111111_opy_] = bstack11ll1lll1l1_opy_
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᙡ") + str(len(bstack11lll111lll_opy_)) + bstack11ll111_opy_ (u"ࠦࠧᙢ"))
        TestFramework.bstack1lll11l1111_opy_(instance, PytestBDDFramework.bstack11l1llll1l1_opy_, bstack11lll111lll_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᙣ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠨࠢᙤ"))
        return instance
    def __11ll111l1ll_opy_(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1lllllll_opy_.create_context(target)
        ob = bstack1ll1l111111_opy_(ctx, self.bstack1l1l1ll1l1l_opy_, self.bstack11ll1l1111l_opy_, test_framework_state)
        TestFramework.bstack11ll11111ll_opy_(ob, {
            TestFramework.bstack1l1ll1ll1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l11l1l11l1_opy_: context.test_framework_version,
            TestFramework.bstack11ll11ll11l_opy_: [],
            PytestBDDFramework.bstack11l1llll1l1_opy_: {},
            PytestBDDFramework.bstack11l1llll1ll_opy_: {},
            PytestBDDFramework.bstack11ll11lllll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll11l1111_opy_(ob, TestFramework.bstack11ll1111l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll11l1111_opy_(ob, TestFramework.bstack1l1ll1lll11_opy_, context.platform_index)
        TestFramework.bstack1ll1lll1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᙥ") + str(TestFramework.bstack1ll1lll1ll1_opy_.keys()) + bstack11ll111_opy_ (u"ࠣࠤᙦ"))
        return ob
    @staticmethod
    def __11ll1ll1l1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬᙧ"): id(step),
                bstack11ll111_opy_ (u"ࠪࡸࡪࡾࡴࠨᙨ"): step.name,
                bstack11ll111_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᙩ"): step.keyword,
            })
        meta = {
            bstack11ll111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᙪ"): {
                bstack11ll111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙫ"): feature.name,
                bstack11ll111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᙬ"): feature.filename,
                bstack11ll111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᙭"): feature.description
            },
            bstack11ll111_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ᙮"): {
                bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨᙯ"): scenario.name
            },
            bstack11ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᙰ"): steps,
            bstack11ll111_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᙱ"): PytestBDDFramework.__11ll11l11ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11ll1llll11_opy_: meta
            }
        )
    def bstack11ll1ll1111_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᙲ")
        global _1l11l1ll1l1_opy_
        platform_index = os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᙳ")]
        bstack1l11ll111ll_opy_ = os.path.join(bstack1l11lll1111_opy_, (bstack1l11lll1l11_opy_ + str(platform_index)), bstack11ll1l11ll1_opy_)
        if not os.path.exists(bstack1l11ll111ll_opy_) or not os.path.isdir(bstack1l11ll111ll_opy_):
            return
        logs = hook.get(bstack11ll111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᙴ"), [])
        with os.scandir(bstack1l11ll111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11l1ll1l1_opy_:
                    self.logger.info(bstack11ll111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᙵ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll111_opy_ (u"ࠥࠦᙶ")
                    log_entry = bstack1ll1l1l11ll_opy_(
                        kind=bstack11ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᙷ"),
                        message=bstack11ll111_opy_ (u"ࠧࠨᙸ"),
                        level=bstack11ll111_opy_ (u"ࠨࠢᙹ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11ll1l1ll_opy_=entry.stat().st_size,
                        bstack1l11l11ll11_opy_=bstack11ll111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᙺ"),
                        bstack1_opy_=os.path.abspath(entry.path),
                        bstack11lll1111l1_opy_=hook.get(TestFramework.bstack11ll1llllll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11l1ll1l1_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᙻ")]
        bstack11lll11111l_opy_ = os.path.join(bstack1l11lll1111_opy_, (bstack1l11lll1l11_opy_ + str(platform_index)), bstack11ll1l11ll1_opy_, bstack11ll11l11l1_opy_)
        if not os.path.exists(bstack11lll11111l_opy_) or not os.path.isdir(bstack11lll11111l_opy_):
            self.logger.info(bstack11ll111_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᙼ").format(bstack11lll11111l_opy_))
        else:
            self.logger.info(bstack11ll111_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᙽ").format(bstack11lll11111l_opy_))
            with os.scandir(bstack11lll11111l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11l1ll1l1_opy_:
                        self.logger.info(bstack11ll111_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᙾ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll111_opy_ (u"ࠧࠨᙿ")
                        log_entry = bstack1ll1l1l11ll_opy_(
                            kind=bstack11ll111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ "),
                            message=bstack11ll111_opy_ (u"ࠢࠣᚁ"),
                            level=bstack11ll111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᚂ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11ll1l1ll_opy_=entry.stat().st_size,
                            bstack1l11l11ll11_opy_=bstack11ll111_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᚃ"),
                            bstack1_opy_=os.path.abspath(entry.path),
                            bstack1l11lll1lll_opy_=hook.get(TestFramework.bstack11ll1llllll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11l1ll1l1_opy_.add(abs_path)
        hook[bstack11ll111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᚄ")] = logs
    def bstack1l11l11l1l1_opy_(
        self,
        bstack1l11ll11ll1_opy_: bstack1ll1l111111_opy_,
        entries: List[bstack1ll1l1l11ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᚅ"))
        req.platform_index = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1ll1lll11_opy_)
        req.client_worker_id = bstack11ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᚆ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11ll11ll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11ll11ll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11ll11ll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1ll1ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l11l1l11l1_opy_)
            log_entry.uuid = entry.bstack11lll1111l1_opy_ if entry.bstack11lll1111l1_opy_ else TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1l11ll1ll_opy_)
            log_entry.test_framework_state = bstack1l11ll11ll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᚇ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᚈ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l1ll_opy_
                log_entry.file_path = entry.bstack1_opy_
        def bstack1l11ll1l11l_opy_():
            bstack11lll11111_opy_ = datetime.now()
            try:
                self.bstack1l1llllll1l_opy_.LogCreatedEvent(req)
                bstack1l11ll11ll1_opy_.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᚉ"), datetime.now() - bstack11lll11111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᚊ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll11llll1_opy_.enqueue(bstack1l11ll1l11l_opy_)
    def __11ll1l1ll11_opy_(self, instance) -> None:
        bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᚋ")
        bstack11ll11lll1l_opy_ = {bstack11ll111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᚌ"): bstack1ll11ll1l1l_opy_.bstack11ll11l1111_opy_()}
        TestFramework.bstack11ll11111ll_opy_(instance, bstack11ll11lll1l_opy_)
    @staticmethod
    def __11ll111ll1l_opy_(instance, args):
        request, bstack11ll1l111l1_opy_ = args
        bstack11ll11l1ll1_opy_ = id(bstack11ll1l111l1_opy_)
        bstack11lll111ll1_opy_ = instance.data[TestFramework.bstack11ll1llll11_opy_]
        step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠬ࡯ࡤࠨᚍ")] == bstack11ll11l1ll1_opy_, bstack11lll111ll1_opy_[bstack11ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚎ")]), None)
        step.update({
            bstack11ll111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚏ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11lll111ll1_opy_[bstack11ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚐ")]) if st[bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬᚑ")] == step[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ᚒ")]), None)
        if index is not None:
            bstack11lll111ll1_opy_[bstack11ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚓ")][index] = step
        instance.data[TestFramework.bstack11ll1llll11_opy_] = bstack11lll111ll1_opy_
    @staticmethod
    def __11ll1llll1l_opy_(instance, args):
        bstack11ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᚔ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll1l111l1_opy_ = args[1]
        bstack11ll11l1ll1_opy_ = id(bstack11ll1l111l1_opy_)
        bstack11lll111ll1_opy_ = instance.data[TestFramework.bstack11ll1llll11_opy_]
        step = None
        if bstack11ll11l1ll1_opy_ is not None and bstack11lll111ll1_opy_.get(bstack11ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚕ")):
            step = next(filter(lambda st: st[bstack11ll111_opy_ (u"ࠧࡪࡦࠪᚖ")] == bstack11ll11l1ll1_opy_, bstack11lll111ll1_opy_[bstack11ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᚗ")]), None)
            step.update({
                bstack11ll111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚘ"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11ll111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᚙ"): bstack11ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚚ"),
                bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭᚛"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᚜"): bstack11ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᚝"),
                })
        index = next((i for i, st in enumerate(bstack11lll111ll1_opy_[bstack11ll111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᚞")]) if st[bstack11ll111_opy_ (u"ࠩ࡬ࡨࠬ᚟")] == step[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭ᚠ")]), None)
        if index is not None:
            bstack11lll111ll1_opy_[bstack11ll111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚡ")][index] = step
        instance.data[TestFramework.bstack11ll1llll11_opy_] = bstack11lll111ll1_opy_
    @staticmethod
    def __11ll11l11ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11ll111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᚢ")):
                examples = list(node.callspec.params[bstack11ll111_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᚣ")].values())
            return examples
        except:
            return []
    def bstack1l111lll11l_opy_(self, instance: bstack1ll1l111111_opy_, bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_]):
        bstack11l1lll1lll_opy_ = (
            PytestBDDFramework.bstack11lll111l11_opy_
            if bstack1ll1ll1llll_opy_[1] == bstack1l1llll1l1l_opy_.PRE
            else PytestBDDFramework.bstack11ll11l1l11_opy_
        )
        hook = PytestBDDFramework.bstack11ll1ll1ll1_opy_(instance, bstack11l1lll1lll_opy_)
        entries = hook.get(TestFramework.bstack11ll11ll1ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, []))
        return entries
    def bstack1l111llllll_opy_(self, instance: bstack1ll1l111111_opy_, bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_]):
        bstack11l1lll1lll_opy_ = (
            PytestBDDFramework.bstack11lll111l11_opy_
            if bstack1ll1ll1llll_opy_[1] == bstack1l1llll1l1l_opy_.PRE
            else PytestBDDFramework.bstack11ll11l1l11_opy_
        )
        PytestBDDFramework.bstack11ll111l11l_opy_(instance, bstack11l1lll1lll_opy_)
        TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, []).clear()
    @staticmethod
    def bstack11ll1ll1ll1_opy_(instance: bstack1ll1l111111_opy_, bstack11l1lll1lll_opy_: str):
        bstack11l1lllllll_opy_ = (
            PytestBDDFramework.bstack11l1llll1ll_opy_
            if bstack11l1lll1lll_opy_ == PytestBDDFramework.bstack11ll11l1l11_opy_
            else PytestBDDFramework.bstack11ll11lllll_opy_
        )
        bstack11ll1l11l11_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11l1lll1lll_opy_, None)
        bstack11ll11llll1_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11l1lllllll_opy_, None) if bstack11ll1l11l11_opy_ else None
        return (
            bstack11ll11llll1_opy_[bstack11ll1l11l11_opy_][-1]
            if isinstance(bstack11ll11llll1_opy_, dict) and len(bstack11ll11llll1_opy_.get(bstack11ll1l11l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll111l11l_opy_(instance: bstack1ll1l111111_opy_, bstack11l1lll1lll_opy_: str):
        hook = PytestBDDFramework.bstack11ll1ll1ll1_opy_(instance, bstack11l1lll1lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll11ll1ll_opy_, []).clear()
    @staticmethod
    def __11l1lllll11_opy_(instance: bstack1ll1l111111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᚤ"), None)):
            return
        if os.getenv(bstack11ll111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᚥ"), bstack11ll111_opy_ (u"ࠤ࠴ࠦᚦ")) != bstack11ll111_opy_ (u"ࠥ࠵ࠧᚧ"):
            PytestBDDFramework.logger.warning(bstack11ll111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᚨ"))
            return
        bstack11ll1l1lll1_opy_ = {
            bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᚩ"): (PytestBDDFramework.bstack11lll111l11_opy_, PytestBDDFramework.bstack11ll11lllll_opy_),
            bstack11ll111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᚪ"): (PytestBDDFramework.bstack11ll11l1l11_opy_, PytestBDDFramework.bstack11l1llll1ll_opy_),
        }
        for when in (bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᚫ"), bstack11ll111_opy_ (u"ࠣࡥࡤࡰࡱࠨᚬ"), bstack11ll111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᚭ")):
            bstack11ll11111l1_opy_ = args[1].get_records(when)
            if not bstack11ll11111l1_opy_:
                continue
            records = [
                bstack1ll1l1l11ll_opy_(
                    kind=TestFramework.bstack1l111lll111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll111_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᚮ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᚯ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll11111l1_opy_
                if isinstance(getattr(r, bstack11ll111_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᚰ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll1l1l1ll_opy_, bstack11l1lllllll_opy_ = bstack11ll1l1lll1_opy_.get(when, (None, None))
            bstack11ll1ll1l11_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11ll1l1l1ll_opy_, None) if bstack11ll1l1l1ll_opy_ else None
            bstack11ll11llll1_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11l1lllllll_opy_, None) if bstack11ll1ll1l11_opy_ else None
            if isinstance(bstack11ll11llll1_opy_, dict) and len(bstack11ll11llll1_opy_.get(bstack11ll1ll1l11_opy_, [])) > 0:
                hook = bstack11ll11llll1_opy_[bstack11ll1ll1l11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll11ll1ll_opy_ in hook:
                    hook[TestFramework.bstack11ll11ll1ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1l11lll_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack111lll1111_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__11ll11lll11_opy_(request.node, scenario)
        bstack11ll1111ll1_opy_ = feature.filename
        if not bstack111lll1111_opy_ or not test_name or not bstack11ll1111ll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l11ll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1l1llll_opy_: bstack111lll1111_opy_,
            TestFramework.bstack1l1l1l1111l_opy_: test_name,
            TestFramework.bstack1l111ll111l_opy_: bstack111lll1111_opy_,
            TestFramework.bstack11ll1l1l111_opy_: bstack11ll1111ll1_opy_,
            TestFramework.bstack11ll1l1l1l1_opy_: PytestBDDFramework.__11ll111ll11_opy_(feature, scenario),
            TestFramework.bstack11ll1l11111_opy_: code,
            TestFramework.bstack1l11111l1l1_opy_: TestFramework.bstack11ll1111lll_opy_,
            TestFramework.bstack11lll1lllll_opy_: test_name
        }
    @staticmethod
    def __11ll11lll11_opy_(node, scenario):
        if hasattr(node, bstack11ll111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᚱ")):
            parts = node.nodeid.rsplit(bstack11ll111_opy_ (u"ࠢ࡜ࠤᚲ"))
            params = parts[-1]
            return bstack11ll111_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᚳ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11ll111ll11_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᚴ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᚵ")) else [])
    @staticmethod
    def __11l1lllll1l_opy_(location):
        return bstack11ll111_opy_ (u"ࠦ࠿ࡀࠢᚶ").join(filter(lambda x: isinstance(x, str), location))