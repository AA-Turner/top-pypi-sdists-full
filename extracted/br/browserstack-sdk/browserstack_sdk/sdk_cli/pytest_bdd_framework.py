# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack111111111l_opy_ import bstack1lllll11lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1ll11_opy_ import bstack1l111l1l111_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1lllll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1ll1llll1ll_opy_,
    bstack1l111ll111l_opy_,
    bstack1lll1l1llll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1ll1l11l1_opy_
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1l11l_opy_ import bstack1ll1lll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111lll_opy_
bstack1l1ll1l111l_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l1l1lll111_opy_ = bstack1111l1l_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᐮ")
bstack11llllll11l_opy_ = bstack1111l1l_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᐯ")
bstack1l1111ll1ll_opy_ = bstack1111l1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᐰ")
bstack1l111ll1111_opy_ = 1.0
_1l1l1ll11ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1111l1_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᐱ")
    bstack1l11111111l_opy_ = bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᐲ")
    bstack1l11111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᐳ")
    bstack1l111l11ll1_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᐴ")
    bstack1l1111l1111_opy_ = bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᐵ")
    bstack1l11111llll_opy_: bool
    bstack1111111ll1_opy_: bstack1111111lll_opy_  = None
    bstack11llllll111_opy_ = [
        bstack1lll1lllll1_opy_.BEFORE_ALL,
        bstack1lll1lllll1_opy_.AFTER_ALL,
        bstack1lll1lllll1_opy_.BEFORE_EACH,
        bstack1lll1lllll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11111l111_opy_: Dict[str, str],
        bstack1ll11ll1111_opy_: List[str]=[bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᐶ")],
        bstack1111111ll1_opy_: bstack1111111lll_opy_ = None,
        bstack1ll1ll11l11_opy_=None
    ):
        super().__init__(bstack1ll11ll1111_opy_, bstack1l11111l111_opy_, bstack1111111ll1_opy_)
        self.bstack1l11111llll_opy_ = any(bstack1111l1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᐷ") in item.lower() for item in bstack1ll11ll1111_opy_)
        self.bstack1ll1ll11l11_opy_ = bstack1ll1ll11l11_opy_
    def track_event(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1lllll1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11llllll111_opy_:
            bstack1l111l1l111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1lllll1_opy_.NONE:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᐸ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠦࠧᐹ"))
            return
        if not self.bstack1l11111llll_opy_:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᐺ") + str(str(self.bstack1ll11ll1111_opy_)) + bstack1111l1l_opy_ (u"ࠨࠢᐻ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐼ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤᐽ"))
            return
        instance = self.__1l1111l111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᐾ") + str(args) + bstack1111l1l_opy_ (u"ࠥࠦᐿ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11llllll111_opy_ and test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11l1l1l1_opy_.value)
                name = str(EVENTS.bstack11l1l1l1_opy_.name)+bstack1111l1l_opy_ (u"ࠦ࠿ࠨᑀ")+str(test_framework_state.name)
                TestFramework.bstack1l1111l1ll1_opy_(instance, name, bstack1ll111l1ll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᑁ").format(e))
        try:
            if test_framework_state == bstack1lll1lllll1_opy_.TEST:
                if not TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l111l111l1_opy_) and test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111lll111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑂ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠢࠣᑃ"))
                if test_hook_state == bstack1ll1llll1ll_opy_.PRE and not TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11llllll1ll_opy_(instance, args)
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑄ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠤࠥᑅ"))
                elif test_hook_state == bstack1ll1llll1ll_opy_.POST and not TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑆ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠦࠧᑇ"))
            elif test_framework_state == bstack1lll1lllll1_opy_.STEP:
                if test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                    PytestBDDFramework.__1l111111ll1_opy_(instance, args)
                elif test_hook_state == bstack1ll1llll1ll_opy_.POST:
                    PytestBDDFramework.__1l111ll1l1l_opy_(instance, args)
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG and test_hook_state == bstack1ll1llll1ll_opy_.POST:
                PytestBDDFramework.__1l1111l1l1l_opy_(instance, *args)
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG_REPORT and test_hook_state == bstack1ll1llll1ll_opy_.POST:
                self.__1l1111111l1_opy_(instance, *args)
                self.__1l111l1l11l_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11llllll111_opy_:
                self.__1l111l11111_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᑈ") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠨࠢᑉ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lllll1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11llllll111_opy_ and test_hook_state == bstack1ll1llll1ll_opy_.POST:
                name = str(EVENTS.bstack11l1l1l1_opy_.name)+bstack1111l1l_opy_ (u"ࠢ࠻ࠤᑊ")+str(test_framework_state.name)
                bstack1ll111l1ll1_opy_ = TestFramework.bstack1l111l1111l_opy_(instance, name)
                bstack1lll11111ll_opy_.end(EVENTS.bstack11l1l1l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᑋ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᑌ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᑍ").format(e))
    def bstack1l1l1llll11_opy_(self):
        return self.bstack1l11111llll_opy_
    def __1l11111ll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111l1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᑎ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1l1lll1_opy_(rep, [bstack1111l1l_opy_ (u"ࠧࡽࡨࡦࡰࠥᑏ"), bstack1111l1l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑐ"), bstack1111l1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᑑ"), bstack1111l1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᑒ"), bstack1111l1l_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᑓ"), bstack1111l1l_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᑔ")])
        return None
    def __1l1111111l1_opy_(self, instance: bstack1lll1l1ll1l_opy_, *args):
        result = self.__1l11111ll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111l1ll_opy_ = None
        if result.get(bstack1111l1l_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑕ"), None) == bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᑖ") and len(args) > 1 and getattr(args[1], bstack1111l1l_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᑗ"), None) is not None:
            failure = [{bstack1111l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᑘ"): [args[1].excinfo.exconly(), result.get(bstack1111l1l_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᑙ"), None)]}]
            bstack111111l1ll_opy_ = bstack1111l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᑚ") if bstack1111l1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᑛ") in getattr(args[1].excinfo, bstack1111l1l_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᑜ"), bstack1111l1l_opy_ (u"ࠧࠨᑝ")) else bstack1111l1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᑞ")
        bstack11lllllll1l_opy_ = result.get(bstack1111l1l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑟ"), TestFramework.bstack1l111lllll1_opy_)
        if bstack11lllllll1l_opy_ != TestFramework.bstack1l111lllll1_opy_:
            TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll111l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l111111_opy_(instance, {
            TestFramework.bstack1l1l11111l1_opy_: failure,
            TestFramework.bstack1l1111111ll_opy_: bstack111111l1ll_opy_,
            TestFramework.bstack1l1l1111l1l_opy_: bstack11lllllll1l_opy_,
        })
    def __1l1111l111l_opy_(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1lllll1_opy_.SETUP_FIXTURE:
            instance = self.__11lllll1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11llllll1l1_opy_ bstack1l111ll1lll_opy_ this to be bstack1111l1l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑠ")
            if test_framework_state == bstack1lll1lllll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111111l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1111l1l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᑡ"), None), bstack1111l1l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑢ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111l1l_opy_ (u"ࠦࡳࡵࡤࡦࠤᑣ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1111l1l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑤ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll1111l_opy_(target) if target else None
        return instance
    def __1l111l11111_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1111l11l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, PytestBDDFramework.bstack1l11111111l_opy_, {})
        if not key in bstack1l1111l11l1_opy_:
            bstack1l1111l11l1_opy_[key] = []
        bstack1l111l111ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, PytestBDDFramework.bstack1l11111l1ll_opy_, {})
        if not key in bstack1l111l111ll_opy_:
            bstack1l111l111ll_opy_[key] = []
        bstack1l111l1lll1_opy_ = {
            PytestBDDFramework.bstack1l11111111l_opy_: bstack1l1111l11l1_opy_,
            PytestBDDFramework.bstack1l11111l1ll_opy_: bstack1l111l111ll_opy_,
        }
        if test_hook_state == bstack1ll1llll1ll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1111l1l_opy_ (u"ࠨ࡫ࡦࡻࠥᑥ"): key,
                TestFramework.bstack1l111111111_opy_: uuid4().__str__(),
                TestFramework.bstack1l111l1l1ll_opy_: TestFramework.bstack1l1111ll111_opy_,
                TestFramework.bstack1l1111lll1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l11111l_opy_: [],
                TestFramework.bstack1l111ll11l1_opy_: hook_name,
                TestFramework.bstack1l111111l11_opy_: bstack1ll1lll11l1_opy_.bstack1l111lll1ll_opy_()
            }
            bstack1l1111l11l1_opy_[key].append(hook)
            bstack1l111l1lll1_opy_[PytestBDDFramework.bstack1l111l11ll1_opy_] = key
        elif test_hook_state == bstack1ll1llll1ll_opy_.POST:
            bstack11lllll1ll1_opy_ = bstack1l1111l11l1_opy_.get(key, [])
            hook = bstack11lllll1ll1_opy_.pop() if bstack11lllll1ll1_opy_ else None
            if hook:
                result = self.__1l11111ll11_opy_(*args)
                if result:
                    bstack1l111l1llll_opy_ = result.get(bstack1111l1l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑦ"), TestFramework.bstack1l1111ll111_opy_)
                    if bstack1l111l1llll_opy_ != TestFramework.bstack1l1111ll111_opy_:
                        hook[TestFramework.bstack1l111l1l1ll_opy_] = bstack1l111l1llll_opy_
                hook[TestFramework.bstack11lllll1l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111111l11_opy_] = bstack1ll1lll11l1_opy_.bstack1l111lll1ll_opy_()
                self.bstack1l11111l11l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1111l11ll_opy_, [])
                self.bstack1l1l1ll1lll_opy_(instance, logs)
                bstack1l111l111ll_opy_[key].append(hook)
                bstack1l111l1lll1_opy_[PytestBDDFramework.bstack1l1111l1111_opy_] = key
        TestFramework.bstack1l11l111111_opy_(instance, bstack1l111l1lll1_opy_)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᑧ") + str(bstack1l111l111ll_opy_) + bstack1111l1l_opy_ (u"ࠤࠥᑨ"))
    def __11lllll1lll_opy_(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1l1lll1_opy_(args[0], [bstack1111l1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᑩ"), bstack1111l1l_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᑪ"), bstack1111l1l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᑫ"), bstack1111l1l_opy_ (u"ࠨࡩࡥࡵࠥᑬ"), bstack1111l1l_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᑭ"), bstack1111l1l_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᑮ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1111l1l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑯ")) else fixturedef.get(bstack1111l1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᑰ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111l1l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᑱ")) else None
        node = request.node if hasattr(request, bstack1111l1l_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᑲ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111l1l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑳ")) else None
        baseid = fixturedef.get(bstack1111l1l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᑴ"), None) or bstack1111l1l_opy_ (u"ࠣࠤᑵ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111l1l_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᑶ")):
            target = PytestBDDFramework.__1l111llll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111l1l_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᑷ")) else None
            if target and not TestFramework.bstack1lllll1111l_opy_(target):
                self.__1l111111l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᑸ") + str(test_hook_state) + bstack1111l1l_opy_ (u"ࠧࠨᑹ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᑺ") + str(target) + bstack1111l1l_opy_ (u"ࠢࠣᑻ"))
            return None
        instance = TestFramework.bstack1lllll1111l_opy_(target)
        if not instance:
            self.logger.warning(bstack1111l1l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᑼ") + str(target) + bstack1111l1l_opy_ (u"ࠤࠥᑽ"))
            return None
        bstack1l1111ll1l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, PytestBDDFramework.bstack1l11l1111l1_opy_, {})
        if os.getenv(bstack1111l1l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᑾ"), bstack1111l1l_opy_ (u"ࠦ࠶ࠨᑿ")) == bstack1111l1l_opy_ (u"ࠧ࠷ࠢᒀ"):
            bstack11lllllll11_opy_ = bstack1111l1l_opy_ (u"ࠨ࠺ࠣᒁ").join((scope, fixturename))
            bstack1l1111ll11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l11l1l_opy_ = {
                bstack1111l1l_opy_ (u"ࠢ࡬ࡧࡼࠦᒂ"): bstack11lllllll11_opy_,
                bstack1111l1l_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᒃ"): PytestBDDFramework.__1l11111l1l1_opy_(request.node, scenario),
                bstack1111l1l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᒄ"): fixturedef,
                bstack1111l1l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᒅ"): scope,
                bstack1111l1l_opy_ (u"ࠦࡹࡿࡰࡦࠤᒆ"): None,
            }
            try:
                if test_hook_state == bstack1ll1llll1ll_opy_.POST and callable(getattr(args[-1], bstack1111l1l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᒇ"), None)):
                    bstack1l111l11l1l_opy_[bstack1111l1l_opy_ (u"ࠨࡴࡺࡲࡨࠦᒈ")] = TestFramework.bstack1l1ll11lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1llll1ll_opy_.PRE:
                bstack1l111l11l1l_opy_[bstack1111l1l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᒉ")] = uuid4().__str__()
                bstack1l111l11l1l_opy_[PytestBDDFramework.bstack1l1111lll1l_opy_] = bstack1l1111ll11l_opy_
            elif test_hook_state == bstack1ll1llll1ll_opy_.POST:
                bstack1l111l11l1l_opy_[PytestBDDFramework.bstack11lllll1l1l_opy_] = bstack1l1111ll11l_opy_
            if bstack11lllllll11_opy_ in bstack1l1111ll1l1_opy_:
                bstack1l1111ll1l1_opy_[bstack11lllllll11_opy_].update(bstack1l111l11l1l_opy_)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᒊ") + str(bstack1l1111ll1l1_opy_[bstack11lllllll11_opy_]) + bstack1111l1l_opy_ (u"ࠤࠥᒋ"))
            else:
                bstack1l1111ll1l1_opy_[bstack11lllllll11_opy_] = bstack1l111l11l1l_opy_
                self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᒌ") + str(len(bstack1l1111ll1l1_opy_)) + bstack1111l1l_opy_ (u"ࠦࠧᒍ"))
        TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l11l1111l1_opy_, bstack1l1111ll1l1_opy_)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᒎ") + str(instance.ref()) + bstack1111l1l_opy_ (u"ࠨࠢᒏ"))
        return instance
    def __1l111111l1l_opy_(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllll11lll_opy_.create_context(target)
        ob = bstack1lll1l1ll1l_opy_(ctx, self.bstack1ll11ll1111_opy_, self.bstack1l11111l111_opy_, test_framework_state)
        TestFramework.bstack1l11l111111_opy_(ob, {
            TestFramework.bstack1ll111lll11_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll11llll_opy_: context.test_framework_version,
            TestFramework.bstack1l111ll1ll1_opy_: [],
            PytestBDDFramework.bstack1l11l1111l1_opy_: {},
            PytestBDDFramework.bstack1l11111l1ll_opy_: {},
            PytestBDDFramework.bstack1l11111111l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack11llllllll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack1ll11l1ll1l_opy_, context.platform_index)
        TestFramework.bstack1111111111_opy_[ctx.id] = ob
        self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᒐ") + str(TestFramework.bstack1111111111_opy_.keys()) + bstack1111l1l_opy_ (u"ࠣࠤᒑ"))
        return ob
    @staticmethod
    def __11llllll1ll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬᒒ"): id(step),
                bstack1111l1l_opy_ (u"ࠪࡸࡪࡾࡴࠨᒓ"): step.name,
                bstack1111l1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᒔ"): step.keyword,
            })
        meta = {
            bstack1111l1l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᒕ"): {
                bstack1111l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒖ"): feature.name,
                bstack1111l1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᒗ"): feature.filename,
                bstack1111l1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᒘ"): feature.description
            },
            bstack1111l1l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᒙ"): {
                bstack1111l1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᒚ"): scenario.name
            },
            bstack1111l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒛ"): steps,
            bstack1111l1l_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᒜ"): PytestBDDFramework.__1l1111llll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11lllllllll_opy_: meta
            }
        )
    def bstack1l11111l11l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᒝ")
        global _1l1l1ll11ll_opy_
        platform_index = os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᒞ")]
        bstack1l1lll1l1ll_opy_ = os.path.join(bstack1l1ll1l111l_opy_, (bstack1l1l1lll111_opy_ + str(platform_index)), bstack11llllll11l_opy_)
        if not os.path.exists(bstack1l1lll1l1ll_opy_) or not os.path.isdir(bstack1l1lll1l1ll_opy_):
            return
        logs = hook.get(bstack1111l1l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᒟ"), [])
        with os.scandir(bstack1l1lll1l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1l1ll11ll_opy_:
                    self.logger.info(bstack1111l1l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᒠ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111l1l_opy_ (u"ࠥࠦᒡ")
                    log_entry = bstack1lll1l1llll_opy_(
                        kind=bstack1111l1l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᒢ"),
                        message=bstack1111l1l_opy_ (u"ࠧࠨᒣ"),
                        level=bstack1111l1l_opy_ (u"ࠨࠢᒤ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l1ll1111_opy_=entry.stat().st_size,
                        bstack1l1ll1l1ll1_opy_=bstack1111l1l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᒥ"),
                        bstack1l1llll_opy_=os.path.abspath(entry.path),
                        bstack1l11l1111ll_opy_=hook.get(TestFramework.bstack1l111111111_opy_)
                    )
                    logs.append(log_entry)
                    _1l1l1ll11ll_opy_.add(abs_path)
        platform_index = os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᒦ")]
        bstack1l111l1ll11_opy_ = os.path.join(bstack1l1ll1l111l_opy_, (bstack1l1l1lll111_opy_ + str(platform_index)), bstack11llllll11l_opy_, bstack1l1111ll1ll_opy_)
        if not os.path.exists(bstack1l111l1ll11_opy_) or not os.path.isdir(bstack1l111l1ll11_opy_):
            self.logger.info(bstack1111l1l_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᒧ").format(bstack1l111l1ll11_opy_))
        else:
            self.logger.info(bstack1111l1l_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᒨ").format(bstack1l111l1ll11_opy_))
            with os.scandir(bstack1l111l1ll11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1l1ll11ll_opy_:
                        self.logger.info(bstack1111l1l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᒩ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111l1l_opy_ (u"ࠧࠨᒪ")
                        log_entry = bstack1lll1l1llll_opy_(
                            kind=bstack1111l1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᒫ"),
                            message=bstack1111l1l_opy_ (u"ࠢࠣᒬ"),
                            level=bstack1111l1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᒭ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l1ll1111_opy_=entry.stat().st_size,
                            bstack1l1ll1l1ll1_opy_=bstack1111l1l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᒮ"),
                            bstack1l1llll_opy_=os.path.abspath(entry.path),
                            bstack1l1lll11ll1_opy_=hook.get(TestFramework.bstack1l111111111_opy_)
                        )
                        logs.append(log_entry)
                        _1l1l1ll11ll_opy_.add(abs_path)
        hook[bstack1111l1l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᒯ")] = logs
    def bstack1l1l1ll1lll_opy_(
        self,
        bstack1l1l1l1ll1l_opy_: bstack1lll1l1ll1l_opy_,
        entries: List[bstack1lll1l1llll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111l1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᒰ"))
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll11l1ll1l_opy_)
        req.execution_context.hash = str(bstack1l1l1l1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll111lll11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1l1ll11llll_opy_)
            log_entry.uuid = entry.bstack1l11l1111ll_opy_ if entry.bstack1l11l1111ll_opy_ else TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll1111ll1l_opy_)
            log_entry.test_framework_state = bstack1l1l1l1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l1l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᒱ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111l1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᒲ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1ll1111_opy_
                log_entry.file_path = entry.bstack1l1llll_opy_
        def bstack1l1ll1lll1l_opy_():
            bstack1ll1l1lll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11l11_opy_.LogCreatedEvent(req)
                bstack1l1l1l1ll1l_opy_.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᒳ"), datetime.now() - bstack1ll1l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᒴ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1lll1l_opy_)
    def __1l111l1l11l_opy_(self, instance) -> None:
        bstack1111l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᒵ")
        bstack1l111l1lll1_opy_ = {bstack1111l1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᒶ"): bstack1ll1lll11l1_opy_.bstack1l111lll1ll_opy_()}
        TestFramework.bstack1l11l111111_opy_(instance, bstack1l111l1lll1_opy_)
    @staticmethod
    def __1l111111ll1_opy_(instance, args):
        request, bstack1l1111l1l11_opy_ = args
        bstack1l111l11l11_opy_ = id(bstack1l1111l1l11_opy_)
        bstack1l1111l1lll_opy_ = instance.data[TestFramework.bstack11lllllllll_opy_]
        step = next(filter(lambda st: st[bstack1111l1l_opy_ (u"ࠫ࡮ࡪࠧᒷ")] == bstack1l111l11l11_opy_, bstack1l1111l1lll_opy_[bstack1111l1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒸ")]), None)
        step.update({
            bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᒹ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1111l1lll_opy_[bstack1111l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒺ")]) if st[bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫᒻ")] == step[bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬᒼ")]), None)
        if index is not None:
            bstack1l1111l1lll_opy_[bstack1111l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")][index] = step
        instance.data[TestFramework.bstack11lllllllll_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def __1l111ll1l1l_opy_(instance, args):
        bstack1111l1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᒾ")
        bstack1l11111ll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1111l1l11_opy_ = args[1]
        bstack1l111l11l11_opy_ = id(bstack1l1111l1l11_opy_)
        bstack1l1111l1lll_opy_ = instance.data[TestFramework.bstack11lllllllll_opy_]
        step = None
        if bstack1l111l11l11_opy_ is not None and bstack1l1111l1lll_opy_.get(bstack1111l1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")):
            step = next(filter(lambda st: st[bstack1111l1l_opy_ (u"࠭ࡩࡥࠩᓀ")] == bstack1l111l11l11_opy_, bstack1l1111l1lll_opy_[bstack1111l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓁ")]), None)
            step.update({
                bstack1111l1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓂ"): bstack1l11111ll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1111l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓃ"): bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᓄ"),
                bstack1111l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᓅ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1111l1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓆ"): bstack1111l1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᓇ"),
                })
        index = next((i for i, st in enumerate(bstack1l1111l1lll_opy_[bstack1111l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓈ")]) if st[bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫᓉ")] == step[bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬᓊ")]), None)
        if index is not None:
            bstack1l1111l1lll_opy_[bstack1111l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓋ")][index] = step
        instance.data[TestFramework.bstack11lllllllll_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def __1l1111llll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1111l1l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᓌ")):
                examples = list(node.callspec.params[bstack1111l1l_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᓍ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1l11ll_opy_(self, instance: bstack1lll1l1ll1l_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_]):
        bstack1l111lll1l1_opy_ = (
            PytestBDDFramework.bstack1l111l11ll1_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1ll1llll1ll_opy_.PRE
            else PytestBDDFramework.bstack1l1111l1111_opy_
        )
        hook = PytestBDDFramework.bstack1l111ll1l11_opy_(instance, bstack1l111lll1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11l11111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l111ll1ll1_opy_, []))
        return entries
    def bstack1l1ll1ll1l1_opy_(self, instance: bstack1lll1l1ll1l_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_]):
        bstack1l111lll1l1_opy_ = (
            PytestBDDFramework.bstack1l111l11ll1_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1ll1llll1ll_opy_.PRE
            else PytestBDDFramework.bstack1l1111l1111_opy_
        )
        PytestBDDFramework.bstack1l11111lll1_opy_(instance, bstack1l111lll1l1_opy_)
        TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l111ll1ll1_opy_, []).clear()
    @staticmethod
    def bstack1l111ll1l11_opy_(instance: bstack1lll1l1ll1l_opy_, bstack1l111lll1l1_opy_: str):
        bstack1l111111lll_opy_ = (
            PytestBDDFramework.bstack1l11111l1ll_opy_
            if bstack1l111lll1l1_opy_ == PytestBDDFramework.bstack1l1111l1111_opy_
            else PytestBDDFramework.bstack1l11111111l_opy_
        )
        bstack11lllll11ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111lll1l1_opy_, None)
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111111lll_opy_, None) if bstack11lllll11ll_opy_ else None
        return (
            bstack1l111l1ll1l_opy_[bstack11lllll11ll_opy_][-1]
            if isinstance(bstack1l111l1ll1l_opy_, dict) and len(bstack1l111l1ll1l_opy_.get(bstack11lllll11ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11111lll1_opy_(instance: bstack1lll1l1ll1l_opy_, bstack1l111lll1l1_opy_: str):
        hook = PytestBDDFramework.bstack1l111ll1l11_opy_(instance, bstack1l111lll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l11111l_opy_, []).clear()
    @staticmethod
    def __1l1111l1l1l_opy_(instance: bstack1lll1l1ll1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111l1l_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᓎ"), None)):
            return
        if os.getenv(bstack1111l1l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᓏ"), bstack1111l1l_opy_ (u"ࠣ࠳ࠥᓐ")) != bstack1111l1l_opy_ (u"ࠤ࠴ࠦᓑ"):
            PytestBDDFramework.logger.warning(bstack1111l1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᓒ"))
            return
        bstack1l111l1l1l1_opy_ = {
            bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᓓ"): (PytestBDDFramework.bstack1l111l11ll1_opy_, PytestBDDFramework.bstack1l11111111l_opy_),
            bstack1111l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᓔ"): (PytestBDDFramework.bstack1l1111l1111_opy_, PytestBDDFramework.bstack1l11111l1ll_opy_),
        }
        for when in (bstack1111l1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᓕ"), bstack1111l1l_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᓖ"), bstack1111l1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᓗ")):
            bstack1l111lll11l_opy_ = args[1].get_records(when)
            if not bstack1l111lll11l_opy_:
                continue
            records = [
                bstack1lll1l1llll_opy_(
                    kind=TestFramework.bstack1l1lll11l11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111l1l_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᓘ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111l1l_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᓙ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111lll11l_opy_
                if isinstance(getattr(r, bstack1111l1l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᓚ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111llllll_opy_, bstack1l111111lll_opy_ = bstack1l111l1l1l1_opy_.get(when, (None, None))
            bstack1l111llll11_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111llllll_opy_, None) if bstack1l111llllll_opy_ else None
            bstack1l111l1ll1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111111lll_opy_, None) if bstack1l111llll11_opy_ else None
            if isinstance(bstack1l111l1ll1l_opy_, dict) and len(bstack1l111l1ll1l_opy_.get(bstack1l111llll11_opy_, [])) > 0:
                hook = bstack1l111l1ll1l_opy_[bstack1l111llll11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l11111l_opy_ in hook:
                    hook[TestFramework.bstack1l11l11111l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l111ll1ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111lll111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1111ll11l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1111lll11_opy_(request.node, scenario)
        bstack1l1111lllll_opy_ = feature.filename
        if not bstack1111ll11l_opy_ or not test_name or not bstack1l1111lllll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1111ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l111l1_opy_: bstack1111ll11l_opy_,
            TestFramework.bstack1ll111l1l11_opy_: test_name,
            TestFramework.bstack1l1l1l11lll_opy_: bstack1111ll11l_opy_,
            TestFramework.bstack1l111l11lll_opy_: bstack1l1111lllll_opy_,
            TestFramework.bstack11lllll11l1_opy_: PytestBDDFramework.__1l11111l1l1_opy_(feature, scenario),
            TestFramework.bstack1l111ll11ll_opy_: code,
            TestFramework.bstack1l1l1111l1l_opy_: TestFramework.bstack1l111lllll1_opy_,
            TestFramework.bstack1l11l1l111l_opy_: test_name
        }
    @staticmethod
    def __1l1111lll11_opy_(node, scenario):
        if hasattr(node, bstack1111l1l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᓛ")):
            parts = node.nodeid.rsplit(bstack1111l1l_opy_ (u"ࠨ࡛ࠣᓜ"))
            params = parts[-1]
            return bstack1111l1l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᓝ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11111l1l1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1111l1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᓞ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1111l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᓟ")) else [])
    @staticmethod
    def __1l111llll1l_opy_(location):
        return bstack1111l1l_opy_ (u"ࠥ࠾࠿ࠨᓠ").join(filter(lambda x: isinstance(x, str), location))