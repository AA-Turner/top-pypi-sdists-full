# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1111111111_opy_
from browserstack_sdk.sdk_cli.utils.bstack11ll1lll11_opy_ import bstack1l1111lll11_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l1ll11_opy_,
    bstack1lll11ll1l1_opy_,
    bstack1ll1lllll11_opy_,
    bstack1l111l11l1l_opy_,
    bstack1ll1l1l1ll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1l1lll1l1_opy_
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll1ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
bstack1l1ll1llll1_opy_ = bstack1l1l1lll1l1_opy_()
bstack1l1ll11111l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᐭ")
bstack11llllllll1_opy_ = bstack1ll11ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᐮ")
bstack1l11111ll1l_opy_ = bstack1ll11ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᐯ")
bstack11lllll1ll1_opy_ = 1.0
_1l1ll1l111l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l1111l1111_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᐰ")
    bstack1l1111ll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᐱ")
    bstack1l111l1l111_opy_ = bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᐲ")
    bstack1l111l11l11_opy_ = bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᐳ")
    bstack1l1111l1l1l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᐴ")
    bstack1l111lll1ll_opy_: bool
    bstack1111111ll1_opy_: bstack11111111ll_opy_  = None
    bstack11lllll11ll_opy_ = [
        bstack1lll1l1ll11_opy_.BEFORE_ALL,
        bstack1lll1l1ll11_opy_.AFTER_ALL,
        bstack1lll1l1ll11_opy_.BEFORE_EACH,
        bstack1lll1l1ll11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111ll1lll_opy_: Dict[str, str],
        bstack1ll1l111l11_opy_: List[str]=[bstack1ll11ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᐵ")],
        bstack1111111ll1_opy_: bstack11111111ll_opy_ = None,
        bstack1ll1llllll1_opy_=None
    ):
        super().__init__(bstack1ll1l111l11_opy_, bstack1l111ll1lll_opy_, bstack1111111ll1_opy_)
        self.bstack1l111lll1ll_opy_ = any(bstack1ll11ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᐶ") in item.lower() for item in bstack1ll1l111l11_opy_)
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l1ll11_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11lllll11ll_opy_:
            bstack1l1111lll11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l1ll11_opy_.NONE:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᐷ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠥࠦᐸ"))
            return
        if not self.bstack1l111lll1ll_opy_:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᐹ") + str(str(self.bstack1ll1l111l11_opy_)) + bstack1ll11ll_opy_ (u"ࠧࠨᐺ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐻ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣᐼ"))
            return
        instance = self.__1l111l11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᐽ") + str(args) + bstack1ll11ll_opy_ (u"ࠤࠥᐾ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11lllll11ll_opy_ and test_hook_state == bstack1ll1lllll11_opy_.PRE:
                bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack1ll11l111l_opy_.value)
                name = str(EVENTS.bstack1ll11l111l_opy_.name)+bstack1ll11ll_opy_ (u"ࠥ࠾ࠧᐿ")+str(test_framework_state.name)
                TestFramework.bstack1l1111ll11l_opy_(instance, name, bstack1ll111ll1ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᑀ").format(e))
        try:
            if test_framework_state == bstack1lll1l1ll11_opy_.TEST:
                if not TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1111l1l11_opy_) and test_hook_state == bstack1ll1lllll11_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11lllllll1l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑁ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠨࠢᑂ"))
                if test_hook_state == bstack1ll1lllll11_opy_.PRE and not TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1lll11111_opy_):
                    TestFramework.bstack1llll1l1lll_opy_(instance, TestFramework.bstack1l1lll11111_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l111111ll1_opy_(instance, args)
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑃ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠣࠤᑄ"))
                elif test_hook_state == bstack1ll1lllll11_opy_.POST and not TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll111lll_opy_):
                    TestFramework.bstack1llll1l1lll_opy_(instance, TestFramework.bstack1l1ll111lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑅ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠥࠦᑆ"))
            elif test_framework_state == bstack1lll1l1ll11_opy_.STEP:
                if test_hook_state == bstack1ll1lllll11_opy_.PRE:
                    PytestBDDFramework.__1l11111l1ll_opy_(instance, args)
                elif test_hook_state == bstack1ll1lllll11_opy_.POST:
                    PytestBDDFramework.__1l111111l11_opy_(instance, args)
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG and test_hook_state == bstack1ll1lllll11_opy_.POST:
                PytestBDDFramework.__1l1111ll1ll_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG_REPORT and test_hook_state == bstack1ll1lllll11_opy_.POST:
                self.__1l111l1llll_opy_(instance, *args)
                self.__1l11111lll1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11lllll11ll_opy_:
                self.__1l111l1111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᑇ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠧࠨᑈ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11llllll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11lllll11ll_opy_ and test_hook_state == bstack1ll1lllll11_opy_.POST:
                name = str(EVENTS.bstack1ll11l111l_opy_.name)+bstack1ll11ll_opy_ (u"ࠨ࠺ࠣᑉ")+str(test_framework_state.name)
                bstack1ll111ll1ll_opy_ = TestFramework.bstack11lllllll11_opy_(instance, name)
                bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1ll11l111l_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᑊ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᑋ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᑌ").format(e))
    def bstack1l1ll1l11l1_opy_(self):
        return self.bstack1l111lll1ll_opy_
    def __1l1111l1ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1ll11ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᑍ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1ll1111_opy_(rep, [bstack1ll11ll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᑎ"), bstack1ll11ll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑏ"), bstack1ll11ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᑐ"), bstack1ll11ll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᑑ"), bstack1ll11ll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᑒ"), bstack1ll11ll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᑓ")])
        return None
    def __1l111l1llll_opy_(self, instance: bstack1lll11ll1l1_opy_, *args):
        result = self.__1l1111l1ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111l11l_opy_ = None
        if result.get(bstack1ll11ll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑔ"), None) == bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑕ") and len(args) > 1 and getattr(args[1], bstack1ll11ll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᑖ"), None) is not None:
            failure = [{bstack1ll11ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᑗ"): [args[1].excinfo.exconly(), result.get(bstack1ll11ll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᑘ"), None)]}]
            bstack111111l11l_opy_ = bstack1ll11ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᑙ") if bstack1ll11ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᑚ") in getattr(args[1].excinfo, bstack1ll11ll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᑛ"), bstack1ll11ll_opy_ (u"ࠦࠧᑜ")) else bstack1ll11ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᑝ")
        bstack1l1111111ll_opy_ = result.get(bstack1ll11ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑞ"), TestFramework.bstack1l1111llll1_opy_)
        if bstack1l1111111ll_opy_ != TestFramework.bstack1l1111llll1_opy_:
            TestFramework.bstack1llll1l1lll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111l1lll_opy_(instance, {
            TestFramework.bstack1l1l111111l_opy_: failure,
            TestFramework.bstack1l111llll1l_opy_: bstack111111l11l_opy_,
            TestFramework.bstack1l1l11111l1_opy_: bstack1l1111111ll_opy_,
        })
    def __1l111l11lll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l1ll11_opy_.SETUP_FIXTURE:
            instance = self.__11lllll1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11111l1l1_opy_ bstack1l111ll11ll_opy_ this to be bstack1ll11ll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑟ")
            if test_framework_state == bstack1lll1l1ll11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111llll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1ll11ll_opy_ (u"ࠣࡰࡲࡨࡪࠨᑠ"), None), bstack1ll11ll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑡ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1ll11ll_opy_ (u"ࠥࡲࡴࡪࡥࠣᑢ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1ll11ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑣ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llllllll11_opy_(target) if target else None
        return instance
    def __1l111l1111l_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l11111l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, PytestBDDFramework.bstack1l1111ll1l1_opy_, {})
        if not key in bstack1l11l11111l_opy_:
            bstack1l11l11111l_opy_[key] = []
        bstack1l11111111l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, PytestBDDFramework.bstack1l111l1l111_opy_, {})
        if not key in bstack1l11111111l_opy_:
            bstack1l11111111l_opy_[key] = []
        bstack1l1111l11l1_opy_ = {
            PytestBDDFramework.bstack1l1111ll1l1_opy_: bstack1l11l11111l_opy_,
            PytestBDDFramework.bstack1l111l1l111_opy_: bstack1l11111111l_opy_,
        }
        if test_hook_state == bstack1ll1lllll11_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1ll11ll_opy_ (u"ࠧࡱࡥࡺࠤᑤ"): key,
                TestFramework.bstack1l111ll11l1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l111111_opy_: TestFramework.bstack1l111lll1l1_opy_,
                TestFramework.bstack1l111ll1111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11llllll111_opy_: [],
                TestFramework.bstack1l111111l1l_opy_: hook_name,
                TestFramework.bstack1l111l1l11l_opy_: bstack1lll1ll11l1_opy_.bstack1l111lll111_opy_()
            }
            bstack1l11l11111l_opy_[key].append(hook)
            bstack1l1111l11l1_opy_[PytestBDDFramework.bstack1l111l11l11_opy_] = key
        elif test_hook_state == bstack1ll1lllll11_opy_.POST:
            bstack1l111l111ll_opy_ = bstack1l11l11111l_opy_.get(key, [])
            hook = bstack1l111l111ll_opy_.pop() if bstack1l111l111ll_opy_ else None
            if hook:
                result = self.__1l1111l1ll1_opy_(*args)
                if result:
                    bstack1l111l1ll1l_opy_ = result.get(bstack1ll11ll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑥ"), TestFramework.bstack1l111lll1l1_opy_)
                    if bstack1l111l1ll1l_opy_ != TestFramework.bstack1l111lll1l1_opy_:
                        hook[TestFramework.bstack1l11l111111_opy_] = bstack1l111l1ll1l_opy_
                hook[TestFramework.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l1l11l_opy_] = bstack1lll1ll11l1_opy_.bstack1l111lll111_opy_()
                self.bstack1l11111llll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111111111_opy_, [])
                self.bstack1l1ll11l111_opy_(instance, logs)
                bstack1l11111111l_opy_[key].append(hook)
                bstack1l1111l11l1_opy_[PytestBDDFramework.bstack1l1111l1l1l_opy_] = key
        TestFramework.bstack1l1111l1lll_opy_(instance, bstack1l1111l11l1_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᑦ") + str(bstack1l11111111l_opy_) + bstack1ll11ll_opy_ (u"ࠣࠤᑧ"))
    def __11lllll1lll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1ll1111_opy_(args[0], [bstack1ll11ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑨ"), bstack1ll11ll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᑩ"), bstack1ll11ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᑪ"), bstack1ll11ll_opy_ (u"ࠧ࡯ࡤࡴࠤᑫ"), bstack1ll11ll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᑬ"), bstack1ll11ll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᑭ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1ll11ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑮ")) else fixturedef.get(bstack1ll11ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑯ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1ll11ll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᑰ")) else None
        node = request.node if hasattr(request, bstack1ll11ll_opy_ (u"ࠦࡳࡵࡤࡦࠤᑱ")) else None
        target = request.node.nodeid if hasattr(node, bstack1ll11ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑲ")) else None
        baseid = fixturedef.get(bstack1ll11ll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᑳ"), None) or bstack1ll11ll_opy_ (u"ࠢࠣᑴ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1ll11ll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᑵ")):
            target = PytestBDDFramework.__1l1111lllll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1ll11ll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᑶ")) else None
            if target and not TestFramework.bstack1llllllll11_opy_(target):
                self.__1l111llll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑷ") + str(test_hook_state) + bstack1ll11ll_opy_ (u"ࠦࠧᑸ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᑹ") + str(target) + bstack1ll11ll_opy_ (u"ࠨࠢᑺ"))
            return None
        instance = TestFramework.bstack1llllllll11_opy_(target)
        if not instance:
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᑻ") + str(target) + bstack1ll11ll_opy_ (u"ࠣࠤᑼ"))
            return None
        bstack11lllll1l1l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, PytestBDDFramework.bstack1l1111l1111_opy_, {})
        if os.getenv(bstack1ll11ll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᑽ"), bstack1ll11ll_opy_ (u"ࠥ࠵ࠧᑾ")) == bstack1ll11ll_opy_ (u"ࠦ࠶ࠨᑿ"):
            bstack1l111lll11l_opy_ = bstack1ll11ll_opy_ (u"ࠧࡀࠢᒀ").join((scope, fixturename))
            bstack1l111l1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l111l1_opy_ = {
                bstack1ll11ll_opy_ (u"ࠨ࡫ࡦࡻࠥᒁ"): bstack1l111lll11l_opy_,
                bstack1ll11ll_opy_ (u"ࠢࡵࡣࡪࡷࠧᒂ"): PytestBDDFramework.__1l111ll1l11_opy_(request.node, scenario),
                bstack1ll11ll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᒃ"): fixturedef,
                bstack1ll11ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᒄ"): scope,
                bstack1ll11ll_opy_ (u"ࠥࡸࡾࡶࡥࠣᒅ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lllll11_opy_.POST and callable(getattr(args[-1], bstack1ll11ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᒆ"), None)):
                    bstack1l111l111l1_opy_[bstack1ll11ll_opy_ (u"ࠧࡺࡹࡱࡧࠥᒇ")] = TestFramework.bstack1l1ll1lllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lllll11_opy_.PRE:
                bstack1l111l111l1_opy_[bstack1ll11ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᒈ")] = uuid4().__str__()
                bstack1l111l111l1_opy_[PytestBDDFramework.bstack1l111ll1111_opy_] = bstack1l111l1lll1_opy_
            elif test_hook_state == bstack1ll1lllll11_opy_.POST:
                bstack1l111l111l1_opy_[PytestBDDFramework.bstack1l111l11111_opy_] = bstack1l111l1lll1_opy_
            if bstack1l111lll11l_opy_ in bstack11lllll1l1l_opy_:
                bstack11lllll1l1l_opy_[bstack1l111lll11l_opy_].update(bstack1l111l111l1_opy_)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᒉ") + str(bstack11lllll1l1l_opy_[bstack1l111lll11l_opy_]) + bstack1ll11ll_opy_ (u"ࠣࠤᒊ"))
            else:
                bstack11lllll1l1l_opy_[bstack1l111lll11l_opy_] = bstack1l111l111l1_opy_
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᒋ") + str(len(bstack11lllll1l1l_opy_)) + bstack1ll11ll_opy_ (u"ࠥࠦᒌ"))
        TestFramework.bstack1llll1l1lll_opy_(instance, PytestBDDFramework.bstack1l1111l1111_opy_, bstack11lllll1l1l_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᒍ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠧࠨᒎ"))
        return instance
    def __1l111llll11_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111111111_opy_.create_context(target)
        ob = bstack1lll11ll1l1_opy_(ctx, self.bstack1ll1l111l11_opy_, self.bstack1l111ll1lll_opy_, test_framework_state)
        TestFramework.bstack1l1111l1lll_opy_(ob, {
            TestFramework.bstack1ll11ll111l_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1l1111_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1l1ll_opy_: [],
            PytestBDDFramework.bstack1l1111l1111_opy_: {},
            PytestBDDFramework.bstack1l111l1l111_opy_: {},
            PytestBDDFramework.bstack1l1111ll1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll1l1lll_opy_(ob, TestFramework.bstack1l1111lll1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll1l1lll_opy_(ob, TestFramework.bstack1ll1111lll1_opy_, context.platform_index)
        TestFramework.bstack1lllllll111_opy_[ctx.id] = ob
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᒏ") + str(TestFramework.bstack1lllllll111_opy_.keys()) + bstack1ll11ll_opy_ (u"ࠢࠣᒐ"))
        return ob
    @staticmethod
    def __1l111111ll1_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫᒑ"): id(step),
                bstack1ll11ll_opy_ (u"ࠩࡷࡩࡽࡺࠧᒒ"): step.name,
                bstack1ll11ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᒓ"): step.keyword,
            })
        meta = {
            bstack1ll11ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᒔ"): {
                bstack1ll11ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒕ"): feature.name,
                bstack1ll11ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᒖ"): feature.filename,
                bstack1ll11ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᒗ"): feature.description
            },
            bstack1ll11ll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᒘ"): {
                bstack1ll11ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒙ"): scenario.name
            },
            bstack1ll11ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒚ"): steps,
            bstack1ll11ll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᒛ"): PytestBDDFramework.__1l11l1111l1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l1111ll111_opy_: meta
            }
        )
    def bstack1l11111llll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒜ")
        global _1l1ll1l111l_opy_
        platform_index = os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᒝ")]
        bstack1l1ll1l1l11_opy_ = os.path.join(bstack1l1ll1llll1_opy_, (bstack1l1ll11111l_opy_ + str(platform_index)), bstack11llllllll1_opy_)
        if not os.path.exists(bstack1l1ll1l1l11_opy_) or not os.path.isdir(bstack1l1ll1l1l11_opy_):
            return
        logs = hook.get(bstack1ll11ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᒞ"), [])
        with os.scandir(bstack1l1ll1l1l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l111l_opy_:
                    self.logger.info(bstack1ll11ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᒟ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1ll11ll_opy_ (u"ࠤࠥᒠ")
                    log_entry = bstack1ll1l1l1ll1_opy_(
                        kind=bstack1ll11ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᒡ"),
                        message=bstack1ll11ll_opy_ (u"ࠦࠧᒢ"),
                        level=bstack1ll11ll_opy_ (u"ࠧࠨᒣ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l1lll11l_opy_=entry.stat().st_size,
                        bstack1l1l1ll1ll1_opy_=bstack1ll11ll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᒤ"),
                        bstack11l111l_opy_=os.path.abspath(entry.path),
                        bstack11lllll1l11_opy_=hook.get(TestFramework.bstack1l111ll11l1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l111l_opy_.add(abs_path)
        platform_index = os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᒥ")]
        bstack11llllll1ll_opy_ = os.path.join(bstack1l1ll1llll1_opy_, (bstack1l1ll11111l_opy_ + str(platform_index)), bstack11llllllll1_opy_, bstack1l11111ll1l_opy_)
        if not os.path.exists(bstack11llllll1ll_opy_) or not os.path.isdir(bstack11llllll1ll_opy_):
            self.logger.info(bstack1ll11ll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᒦ").format(bstack11llllll1ll_opy_))
        else:
            self.logger.info(bstack1ll11ll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᒧ").format(bstack11llllll1ll_opy_))
            with os.scandir(bstack11llllll1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l111l_opy_:
                        self.logger.info(bstack1ll11ll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᒨ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1ll11ll_opy_ (u"ࠦࠧᒩ")
                        log_entry = bstack1ll1l1l1ll1_opy_(
                            kind=bstack1ll11ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒪ"),
                            message=bstack1ll11ll_opy_ (u"ࠨࠢᒫ"),
                            level=bstack1ll11ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᒬ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l1lll11l_opy_=entry.stat().st_size,
                            bstack1l1l1ll1ll1_opy_=bstack1ll11ll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᒭ"),
                            bstack11l111l_opy_=os.path.abspath(entry.path),
                            bstack1l1ll11l1ll_opy_=hook.get(TestFramework.bstack1l111ll11l1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l111l_opy_.add(abs_path)
        hook[bstack1ll11ll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᒮ")] = logs
    def bstack1l1ll11l111_opy_(
        self,
        bstack1l1ll1ll1l1_opy_: bstack1lll11ll1l1_opy_,
        entries: List[bstack1ll1l1l1ll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1ll11ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᒯ"))
        req.platform_index = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll1111lll1_opy_)
        req.execution_context.hash = str(bstack1l1ll1ll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1ll1ll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1ll1ll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll11ll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1l1ll1l1111_opy_)
            log_entry.uuid = entry.bstack11lllll1l11_opy_ if entry.bstack11lllll1l11_opy_ else TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll11l1111l_opy_)
            log_entry.test_framework_state = bstack1l1ll1ll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᒰ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll11ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒱ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1lll11l_opy_
                log_entry.file_path = entry.bstack11l111l_opy_
        def bstack1l1ll1l11ll_opy_():
            bstack1ll111l11_opy_ = datetime.now()
            try:
                self.bstack1ll1llllll1_opy_.LogCreatedEvent(req)
                bstack1l1ll1ll1l1_opy_.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᒲ"), datetime.now() - bstack1ll111l11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᒳ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1l11ll_opy_)
    def __1l11111lll1_opy_(self, instance) -> None:
        bstack1ll11ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᒴ")
        bstack1l1111l11l1_opy_ = {bstack1ll11ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᒵ"): bstack1lll1ll11l1_opy_.bstack1l111lll111_opy_()}
        TestFramework.bstack1l1111l1lll_opy_(instance, bstack1l1111l11l1_opy_)
    @staticmethod
    def __1l11111l1ll_opy_(instance, args):
        request, bstack11lllll11l1_opy_ = args
        bstack1l11111ll11_opy_ = id(bstack11lllll11l1_opy_)
        bstack11llllll1l1_opy_ = instance.data[TestFramework.bstack1l1111ll111_opy_]
        step = next(filter(lambda st: st[bstack1ll11ll_opy_ (u"ࠪ࡭ࡩ࠭ᒶ")] == bstack1l11111ll11_opy_, bstack11llllll1l1_opy_[bstack1ll11ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒷ")]), None)
        step.update({
            bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᒸ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11llllll1l1_opy_[bstack1ll11ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒹ")]) if st[bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪᒺ")] == step[bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫᒻ")]), None)
        if index is not None:
            bstack11llllll1l1_opy_[bstack1ll11ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒼ")][index] = step
        instance.data[TestFramework.bstack1l1111ll111_opy_] = bstack11llllll1l1_opy_
    @staticmethod
    def __1l111111l11_opy_(instance, args):
        bstack1ll11ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᒽ")
        bstack1l111lllll1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11lllll11l1_opy_ = args[1]
        bstack1l11111ll11_opy_ = id(bstack11lllll11l1_opy_)
        bstack11llllll1l1_opy_ = instance.data[TestFramework.bstack1l1111ll111_opy_]
        step = None
        if bstack1l11111ll11_opy_ is not None and bstack11llllll1l1_opy_.get(bstack1ll11ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒾ")):
            step = next(filter(lambda st: st[bstack1ll11ll_opy_ (u"ࠬ࡯ࡤࠨᒿ")] == bstack1l11111ll11_opy_, bstack11llllll1l1_opy_[bstack1ll11ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓀ")]), None)
            step.update({
                bstack1ll11ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᓁ"): bstack1l111lllll1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1ll11ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᓂ"): bstack1ll11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᓃ"),
                bstack1ll11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᓄ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1ll11ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓅ"): bstack1ll11ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᓆ"),
                })
        index = next((i for i, st in enumerate(bstack11llllll1l1_opy_[bstack1ll11ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓇ")]) if st[bstack1ll11ll_opy_ (u"ࠧࡪࡦࠪᓈ")] == step[bstack1ll11ll_opy_ (u"ࠨ࡫ࡧࠫᓉ")]), None)
        if index is not None:
            bstack11llllll1l1_opy_[bstack1ll11ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᓊ")][index] = step
        instance.data[TestFramework.bstack1l1111ll111_opy_] = bstack11llllll1l1_opy_
    @staticmethod
    def __1l11l1111l1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1ll11ll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᓋ")):
                examples = list(node.callspec.params[bstack1ll11ll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᓌ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1ll11l_opy_(self, instance: bstack1lll11ll1l1_opy_, bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_]):
        bstack1l111l1ll11_opy_ = (
            PytestBDDFramework.bstack1l111l11l11_opy_
            if bstack1llll1ll1l1_opy_[1] == bstack1ll1lllll11_opy_.PRE
            else PytestBDDFramework.bstack1l1111l1l1l_opy_
        )
        hook = PytestBDDFramework.bstack1l111l11ll1_opy_(instance, bstack1l111l1ll11_opy_)
        entries = hook.get(TestFramework.bstack11llllll111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []))
        return entries
    def bstack1l1l1ll11l1_opy_(self, instance: bstack1lll11ll1l1_opy_, bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_]):
        bstack1l111l1ll11_opy_ = (
            PytestBDDFramework.bstack1l111l11l11_opy_
            if bstack1llll1ll1l1_opy_[1] == bstack1ll1lllll11_opy_.PRE
            else PytestBDDFramework.bstack1l1111l1l1l_opy_
        )
        PytestBDDFramework.bstack11lllll111l_opy_(instance, bstack1l111l1ll11_opy_)
        TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []).clear()
    @staticmethod
    def bstack1l111l11ll1_opy_(instance: bstack1lll11ll1l1_opy_, bstack1l111l1ll11_opy_: str):
        bstack1l11111l11l_opy_ = (
            PytestBDDFramework.bstack1l111l1l111_opy_
            if bstack1l111l1ll11_opy_ == PytestBDDFramework.bstack1l1111l1l1l_opy_
            else PytestBDDFramework.bstack1l1111ll1l1_opy_
        )
        bstack1l111111lll_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l111l1ll11_opy_, None)
        bstack1l111ll1ll1_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l11111l11l_opy_, None) if bstack1l111111lll_opy_ else None
        return (
            bstack1l111ll1ll1_opy_[bstack1l111111lll_opy_][-1]
            if isinstance(bstack1l111ll1ll1_opy_, dict) and len(bstack1l111ll1ll1_opy_.get(bstack1l111111lll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lllll111l_opy_(instance: bstack1lll11ll1l1_opy_, bstack1l111l1ll11_opy_: str):
        hook = PytestBDDFramework.bstack1l111l11ll1_opy_(instance, bstack1l111l1ll11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11llllll111_opy_, []).clear()
    @staticmethod
    def __1l1111ll1ll_opy_(instance: bstack1lll11ll1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1ll11ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᓍ"), None)):
            return
        if os.getenv(bstack1ll11ll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᓎ"), bstack1ll11ll_opy_ (u"ࠢ࠲ࠤᓏ")) != bstack1ll11ll_opy_ (u"ࠣ࠳ࠥᓐ"):
            PytestBDDFramework.logger.warning(bstack1ll11ll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᓑ"))
            return
        bstack1l1111l111l_opy_ = {
            bstack1ll11ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᓒ"): (PytestBDDFramework.bstack1l111l11l11_opy_, PytestBDDFramework.bstack1l1111ll1l1_opy_),
            bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᓓ"): (PytestBDDFramework.bstack1l1111l1l1l_opy_, PytestBDDFramework.bstack1l111l1l111_opy_),
        }
        for when in (bstack1ll11ll_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓔ"), bstack1ll11ll_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᓕ"), bstack1ll11ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᓖ")):
            bstack1l11111l111_opy_ = args[1].get_records(when)
            if not bstack1l11111l111_opy_:
                continue
            records = [
                bstack1ll1l1l1ll1_opy_(
                    kind=TestFramework.bstack1l1ll1l1lll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1ll11ll_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᓗ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1ll11ll_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᓘ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11111l111_opy_
                if isinstance(getattr(r, bstack1ll11ll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᓙ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111ll111l_opy_, bstack1l11111l11l_opy_ = bstack1l1111l111l_opy_.get(when, (None, None))
            bstack1l111ll1l1l_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l111ll111l_opy_, None) if bstack1l111ll111l_opy_ else None
            bstack1l111ll1ll1_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, bstack1l11111l11l_opy_, None) if bstack1l111ll1l1l_opy_ else None
            if isinstance(bstack1l111ll1ll1_opy_, dict) and len(bstack1l111ll1ll1_opy_.get(bstack1l111ll1l1l_opy_, [])) > 0:
                hook = bstack1l111ll1ll1_opy_[bstack1l111ll1l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11llllll111_opy_ in hook:
                    hook[TestFramework.bstack11llllll111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11lllllll1l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l1l1ll1l1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1111l11ll_opy_(request.node, scenario)
        bstack1l111l1l1l1_opy_ = feature.filename
        if not bstack1l1l1ll1l1_opy_ or not test_name or not bstack1l111l1l1l1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11l1111l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1111l1l11_opy_: bstack1l1l1ll1l1_opy_,
            TestFramework.bstack1ll11l111l1_opy_: test_name,
            TestFramework.bstack1l1l1l11ll1_opy_: bstack1l1l1ll1l1_opy_,
            TestFramework.bstack11lllllllll_opy_: bstack1l111l1l1l1_opy_,
            TestFramework.bstack1l111llllll_opy_: PytestBDDFramework.__1l111ll1l11_opy_(feature, scenario),
            TestFramework.bstack1l1111111l1_opy_: code,
            TestFramework.bstack1l1l11111l1_opy_: TestFramework.bstack1l1111llll1_opy_,
            TestFramework.bstack1l11l1l11l1_opy_: test_name
        }
    @staticmethod
    def __1l1111l11ll_opy_(node, scenario):
        if hasattr(node, bstack1ll11ll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᓚ")):
            parts = node.nodeid.rsplit(bstack1ll11ll_opy_ (u"ࠧࡡࠢᓛ"))
            params = parts[-1]
            return bstack1ll11ll_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᓜ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111ll1l11_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1ll11ll_opy_ (u"ࠧࡵࡣࡪࡷࠬᓝ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1ll11ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᓞ")) else [])
    @staticmethod
    def __1l1111lllll_opy_(location):
        return bstack1ll11ll_opy_ (u"ࠤ࠽࠾ࠧᓟ").join(filter(lambda x: isinstance(x, str), location))