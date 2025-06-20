# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack111111l111_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1ll1_opy_ import bstack1l111l11l1l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll11111l_opy_,
    bstack1llll111l11_opy_,
    bstack1ll1l1lll11_opy_,
    bstack1l11l11l1l1_opy_,
    bstack1lll11lll11_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1lllll111_opy_
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11ll_opy_ import bstack1lll11ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack111111ll1l_opy_
bstack1l1ll11ll1l_opy_ = bstack1l1lllll111_opy_()
bstack1l1lllllll1_opy_ = bstack11ll11_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᏂ")
bstack1l111l1l1l1_opy_ = bstack11ll11_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᏃ")
bstack1l11l11l11l_opy_ = bstack11ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᏄ")
bstack1l11l11111l_opy_ = 1.0
_1l1ll1lll11_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111lll111_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᏅ")
    bstack1l11l111ll1_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᏆ")
    bstack1l11111l111_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᏇ")
    bstack1l1111llll1_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᏈ")
    bstack1l11111lll1_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᏉ")
    bstack1l111ll11ll_opy_: bool
    bstack111111l1ll_opy_: bstack111111ll1l_opy_  = None
    bstack1l111l11ll1_opy_ = [
        bstack1llll11111l_opy_.BEFORE_ALL,
        bstack1llll11111l_opy_.AFTER_ALL,
        bstack1llll11111l_opy_.BEFORE_EACH,
        bstack1llll11111l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l111ll_opy_: Dict[str, str],
        bstack1ll11l11l1l_opy_: List[str]=[bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᏊ")],
        bstack111111l1ll_opy_: bstack111111ll1l_opy_ = None,
        bstack1llll1l1l11_opy_=None
    ):
        super().__init__(bstack1ll11l11l1l_opy_, bstack1l111l111ll_opy_, bstack111111l1ll_opy_)
        self.bstack1l111ll11ll_opy_ = any(bstack11ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᏋ") in item.lower() for item in bstack1ll11l11l1l_opy_)
        self.bstack1llll1l1l11_opy_ = bstack1llll1l1l11_opy_
    def track_event(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1llll11111l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111l11ll1_opy_:
            bstack1l111l11l1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll11111l_opy_.NONE:
            self.logger.warning(bstack11ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᏌ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠣࠤᏍ"))
            return
        if not self.bstack1l111ll11ll_opy_:
            self.logger.warning(bstack11ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᏎ") + str(str(self.bstack1ll11l11l1l_opy_)) + bstack11ll11_opy_ (u"ࠥࠦᏏ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏐ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨᏑ"))
            return
        instance = self.__1l1111l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᏒ") + str(args) + bstack11ll11_opy_ (u"ࠢࠣᏓ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l11ll1_opy_ and test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l11l1lll1_opy_.value)
                name = str(EVENTS.bstack1l11l1lll1_opy_.name)+bstack11ll11_opy_ (u"ࠣ࠼ࠥᏔ")+str(test_framework_state.name)
                TestFramework.bstack1l1111l11l1_opy_(instance, name, bstack1ll11ll111l_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᏕ").format(e))
        try:
            if test_framework_state == bstack1llll11111l_opy_.TEST:
                if not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l11l1l1ll1_opy_) and test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l1111ll1ll_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11ll11_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏖ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠦࠧᏗ"))
                if test_hook_state == bstack1ll1l1lll11_opy_.PRE and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll1lll1_opy_):
                    TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1lll1lll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l11l1ll_opy_(instance, args)
                    self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏘ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠨࠢᏙ"))
                elif test_hook_state == bstack1ll1l1lll11_opy_.POST and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_):
                    TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1lll1l111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏚ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠣࠤᏛ"))
            elif test_framework_state == bstack1llll11111l_opy_.STEP:
                if test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                    PytestBDDFramework.__1l11111l1ll_opy_(instance, args)
                elif test_hook_state == bstack1ll1l1lll11_opy_.POST:
                    PytestBDDFramework.__1l11l1l11l1_opy_(instance, args)
            elif test_framework_state == bstack1llll11111l_opy_.LOG and test_hook_state == bstack1ll1l1lll11_opy_.POST:
                PytestBDDFramework.__1l11111l1l1_opy_(instance, *args)
            elif test_framework_state == bstack1llll11111l_opy_.LOG_REPORT and test_hook_state == bstack1ll1l1lll11_opy_.POST:
                self.__1l1111l1l11_opy_(instance, *args)
                self.__1l111l1l1ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111l11ll1_opy_:
                self.__1l111l1lll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᏜ") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠥࠦᏝ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11111ll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l11ll1_opy_ and test_hook_state == bstack1ll1l1lll11_opy_.POST:
                name = str(EVENTS.bstack1l11l1lll1_opy_.name)+bstack11ll11_opy_ (u"ࠦ࠿ࠨᏞ")+str(test_framework_state.name)
                bstack1ll11ll111l_opy_ = TestFramework.bstack1l111ll111l_opy_(instance, name)
                bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1l11l1lll1_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏟ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏠ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᏡ").format(e))
    def bstack1l1llllllll_opy_(self):
        return self.bstack1l111ll11ll_opy_
    def __1l111l1ll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᏢ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll1lll1l_opy_(rep, [bstack11ll11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᏣ"), bstack11ll11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᏤ"), bstack11ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᏥ"), bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᏦ"), bstack11ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᏧ"), bstack11ll11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᏨ")])
        return None
    def __1l1111l1l11_opy_(self, instance: bstack1llll111l11_opy_, *args):
        result = self.__1l111l1ll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l111l_opy_ = None
        if result.get(bstack11ll11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᏩ"), None) == bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᏪ") and len(args) > 1 and getattr(args[1], bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᏫ"), None) is not None:
            failure = [{bstack11ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᏬ"): [args[1].excinfo.exconly(), result.get(bstack11ll11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᏭ"), None)]}]
            bstack11111l111l_opy_ = bstack11ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᏮ") if bstack11ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᏯ") in getattr(args[1].excinfo, bstack11ll11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᏰ"), bstack11ll11_opy_ (u"ࠤࠥᏱ")) else bstack11ll11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᏲ")
        bstack1l11l11llll_opy_ = result.get(bstack11ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᏳ"), TestFramework.bstack1l111111l1l_opy_)
        if bstack1l11l11llll_opy_ != TestFramework.bstack1l111111l1l_opy_:
            TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1llll11ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111lll11_opy_(instance, {
            TestFramework.bstack1l1l11l1lll_opy_: failure,
            TestFramework.bstack1l1111ll1l1_opy_: bstack11111l111l_opy_,
            TestFramework.bstack1l1l11l11l1_opy_: bstack1l11l11llll_opy_,
        })
    def __1l1111l11ll_opy_(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1llll11111l_opy_.SETUP_FIXTURE:
            instance = self.__1l1111l111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l1l111_opy_ bstack1l111ll1l11_opy_ this to be bstack11ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᏴ")
            if test_framework_state == bstack1llll11111l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l111l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll11111l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᏵ"), None), bstack11ll11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᏶"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll11_opy_ (u"ࠣࡰࡲࡨࡪࠨ᏷"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᏸ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111111l1_opy_(target) if target else None
        return instance
    def __1l111l1lll1_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1111l1l1l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, PytestBDDFramework.bstack1l11l111ll1_opy_, {})
        if not key in bstack1l1111l1l1l_opy_:
            bstack1l1111l1l1l_opy_[key] = []
        bstack1l11l1l111l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, PytestBDDFramework.bstack1l11111l111_opy_, {})
        if not key in bstack1l11l1l111l_opy_:
            bstack1l11l1l111l_opy_[key] = []
        bstack1l111ll1lll_opy_ = {
            PytestBDDFramework.bstack1l11l111ll1_opy_: bstack1l1111l1l1l_opy_,
            PytestBDDFramework.bstack1l11111l111_opy_: bstack1l11l1l111l_opy_,
        }
        if test_hook_state == bstack1ll1l1lll11_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11ll11_opy_ (u"ࠥ࡯ࡪࡿࠢᏹ"): key,
                TestFramework.bstack1l111111ll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111l1111_opy_: TestFramework.bstack1l1111l1ll1_opy_,
                TestFramework.bstack1l1111ll11l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111lllll_opy_: [],
                TestFramework.bstack1l11l1l11ll_opy_: hook_name,
                TestFramework.bstack1l111ll11l1_opy_: bstack1lll11ll1ll_opy_.bstack1l111llll11_opy_()
            }
            bstack1l1111l1l1l_opy_[key].append(hook)
            bstack1l111ll1lll_opy_[PytestBDDFramework.bstack1l1111llll1_opy_] = key
        elif test_hook_state == bstack1ll1l1lll11_opy_.POST:
            bstack1l111lllll1_opy_ = bstack1l1111l1l1l_opy_.get(key, [])
            hook = bstack1l111lllll1_opy_.pop() if bstack1l111lllll1_opy_ else None
            if hook:
                result = self.__1l111l1ll11_opy_(*args)
                if result:
                    bstack1l11111llll_opy_ = result.get(bstack11ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᏺ"), TestFramework.bstack1l1111l1ll1_opy_)
                    if bstack1l11111llll_opy_ != TestFramework.bstack1l1111l1ll1_opy_:
                        hook[TestFramework.bstack1l1111l1111_opy_] = bstack1l11111llll_opy_
                hook[TestFramework.bstack1l111lll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll11l1_opy_] = bstack1lll11ll1ll_opy_.bstack1l111llll11_opy_()
                self.bstack1l11l1l1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l11lll_opy_, [])
                self.bstack1l1ll11l1ll_opy_(instance, logs)
                bstack1l11l1l111l_opy_[key].append(hook)
                bstack1l111ll1lll_opy_[PytestBDDFramework.bstack1l11111lll1_opy_] = key
        TestFramework.bstack1l1111lll11_opy_(instance, bstack1l111ll1lll_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᏻ") + str(bstack1l11l1l111l_opy_) + bstack11ll11_opy_ (u"ࠨࠢᏼ"))
    def __1l1111l111l_opy_(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll1lll1l_opy_(args[0], [bstack11ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᏽ"), bstack11ll11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤ᏾"), bstack11ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤ᏿"), bstack11ll11_opy_ (u"ࠥ࡭ࡩࡹࠢ᐀"), bstack11ll11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᐁ"), bstack11ll11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᐂ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᐃ")) else fixturedef.get(bstack11ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐄ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᐅ")) else None
        node = request.node if hasattr(request, bstack11ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᐆ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᐇ")) else None
        baseid = fixturedef.get(bstack11ll11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᐈ"), None) or bstack11ll11_opy_ (u"ࠧࠨᐉ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᐊ")):
            target = PytestBDDFramework.__1l111l11l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᐋ")) else None
            if target and not TestFramework.bstack11111111l1_opy_(target):
                self.__1l11l111l11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐌ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠤࠥᐍ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᐎ") + str(target) + bstack11ll11_opy_ (u"ࠦࠧᐏ"))
            return None
        instance = TestFramework.bstack11111111l1_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᐐ") + str(target) + bstack11ll11_opy_ (u"ࠨࠢᐑ"))
            return None
        bstack1l111l1111l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, PytestBDDFramework.bstack1l111lll111_opy_, {})
        if os.getenv(bstack11ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᐒ"), bstack11ll11_opy_ (u"ࠣ࠳ࠥᐓ")) == bstack11ll11_opy_ (u"ࠤ࠴ࠦᐔ"):
            bstack1l111lll11l_opy_ = bstack11ll11_opy_ (u"ࠥ࠾ࠧᐕ").join((scope, fixturename))
            bstack1l11l1111l1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1111l1lll_opy_ = {
                bstack11ll11_opy_ (u"ࠦࡰ࡫ࡹࠣᐖ"): bstack1l111lll11l_opy_,
                bstack11ll11_opy_ (u"ࠧࡺࡡࡨࡵࠥᐗ"): PytestBDDFramework.__1l11l1l1111_opy_(request.node, scenario),
                bstack11ll11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᐘ"): fixturedef,
                bstack11ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐙ"): scope,
                bstack11ll11_opy_ (u"ࠣࡶࡼࡴࡪࠨᐚ"): None,
            }
            try:
                if test_hook_state == bstack1ll1l1lll11_opy_.POST and callable(getattr(args[-1], bstack11ll11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᐛ"), None)):
                    bstack1l1111l1lll_opy_[bstack11ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣᐜ")] = TestFramework.bstack1l1ll11l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                bstack1l1111l1lll_opy_[bstack11ll11_opy_ (u"ࠦࡺࡻࡩࡥࠤᐝ")] = uuid4().__str__()
                bstack1l1111l1lll_opy_[PytestBDDFramework.bstack1l1111ll11l_opy_] = bstack1l11l1111l1_opy_
            elif test_hook_state == bstack1ll1l1lll11_opy_.POST:
                bstack1l1111l1lll_opy_[PytestBDDFramework.bstack1l111lll1ll_opy_] = bstack1l11l1111l1_opy_
            if bstack1l111lll11l_opy_ in bstack1l111l1111l_opy_:
                bstack1l111l1111l_opy_[bstack1l111lll11l_opy_].update(bstack1l1111l1lll_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᐞ") + str(bstack1l111l1111l_opy_[bstack1l111lll11l_opy_]) + bstack11ll11_opy_ (u"ࠨࠢᐟ"))
            else:
                bstack1l111l1111l_opy_[bstack1l111lll11l_opy_] = bstack1l1111l1lll_opy_
                self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᐠ") + str(len(bstack1l111l1111l_opy_)) + bstack11ll11_opy_ (u"ࠣࠤᐡ"))
        TestFramework.bstack1llllllllll_opy_(instance, PytestBDDFramework.bstack1l111lll111_opy_, bstack1l111l1111l_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᐢ") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠥࠦᐣ"))
        return instance
    def __1l11l111l11_opy_(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llllll1l1l_opy_.create_context(target)
        ob = bstack1llll111l11_opy_(ctx, self.bstack1ll11l11l1l_opy_, self.bstack1l111l111ll_opy_, test_framework_state)
        TestFramework.bstack1l1111lll11_opy_(ob, {
            TestFramework.bstack1ll11l11lll_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1l11ll_opy_: context.test_framework_version,
            TestFramework.bstack1l111lll1l1_opy_: [],
            PytestBDDFramework.bstack1l111lll111_opy_: {},
            PytestBDDFramework.bstack1l11111l111_opy_: {},
            PytestBDDFramework.bstack1l11l111ll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllllllll_opy_(ob, TestFramework.bstack1l11111l11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllllllll_opy_(ob, TestFramework.bstack1ll1l11111l_opy_, context.platform_index)
        TestFramework.bstack1lllllll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᐤ") + str(TestFramework.bstack1lllllll111_opy_.keys()) + bstack11ll11_opy_ (u"ࠧࠨᐥ"))
        return ob
    @staticmethod
    def __1l11l11l1ll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll11_opy_ (u"࠭ࡩࡥࠩᐦ"): id(step),
                bstack11ll11_opy_ (u"ࠧࡵࡧࡻࡸࠬᐧ"): step.name,
                bstack11ll11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᐨ"): step.keyword,
            })
        meta = {
            bstack11ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᐩ"): {
                bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨᐪ"): feature.name,
                bstack11ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩᐫ"): feature.filename,
                bstack11ll11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᐬ"): feature.description
            },
            bstack11ll11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᐭ"): {
                bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᐮ"): scenario.name
            },
            bstack11ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐯ"): steps,
            bstack11ll11_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᐰ"): PytestBDDFramework.__1l11l1111ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11111ll11_opy_: meta
            }
        )
    def bstack1l11l1l1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᐱ")
        global _1l1ll1lll11_opy_
        platform_index = os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐲ")]
        bstack1l1ll111l11_opy_ = os.path.join(bstack1l1ll11ll1l_opy_, (bstack1l1lllllll1_opy_ + str(platform_index)), bstack1l111l1l1l1_opy_)
        if not os.path.exists(bstack1l1ll111l11_opy_) or not os.path.isdir(bstack1l1ll111l11_opy_):
            return
        logs = hook.get(bstack11ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᐳ"), [])
        with os.scandir(bstack1l1ll111l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1lll11_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᐴ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll11_opy_ (u"ࠢࠣᐵ")
                    log_entry = bstack1lll11lll11_opy_(
                        kind=bstack11ll11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᐶ"),
                        message=bstack11ll11_opy_ (u"ࠤࠥᐷ"),
                        level=bstack11ll11_opy_ (u"ࠥࠦᐸ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll1ll1l_opy_=entry.stat().st_size,
                        bstack1l1ll1l1lll_opy_=bstack11ll11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᐹ"),
                        bstack1llll11_opy_=os.path.abspath(entry.path),
                        bstack1l11l111l1l_opy_=hook.get(TestFramework.bstack1l111111ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1lll11_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᐺ")]
        bstack1l11l11lll1_opy_ = os.path.join(bstack1l1ll11ll1l_opy_, (bstack1l1lllllll1_opy_ + str(platform_index)), bstack1l111l1l1l1_opy_, bstack1l11l11l11l_opy_)
        if not os.path.exists(bstack1l11l11lll1_opy_) or not os.path.isdir(bstack1l11l11lll1_opy_):
            self.logger.info(bstack11ll11_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᐻ").format(bstack1l11l11lll1_opy_))
        else:
            self.logger.info(bstack11ll11_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᐼ").format(bstack1l11l11lll1_opy_))
            with os.scandir(bstack1l11l11lll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1lll11_opy_:
                        self.logger.info(bstack11ll11_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᐽ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll11_opy_ (u"ࠤࠥᐾ")
                        log_entry = bstack1lll11lll11_opy_(
                            kind=bstack11ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᐿ"),
                            message=bstack11ll11_opy_ (u"ࠦࠧᑀ"),
                            level=bstack11ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᑁ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll1ll1l_opy_=entry.stat().st_size,
                            bstack1l1ll1l1lll_opy_=bstack11ll11_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᑂ"),
                            bstack1llll11_opy_=os.path.abspath(entry.path),
                            bstack1l1l1lllll1_opy_=hook.get(TestFramework.bstack1l111111ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1lll11_opy_.add(abs_path)
        hook[bstack11ll11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᑃ")] = logs
    def bstack1l1ll11l1ll_opy_(
        self,
        bstack1l1lll1l1l1_opy_: bstack1llll111l11_opy_,
        entries: List[bstack1lll11lll11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᑄ"))
        req.platform_index = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll1l11111l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11l11lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1ll1l11ll_opy_)
            log_entry.uuid = entry.bstack1l11l111l1l_opy_
            log_entry.test_framework_state = bstack1l1lll1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᑅ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll11_opy_ (u"ࠥࠦᑆ")
            if entry.kind == bstack11ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᑇ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1ll1l_opy_
                log_entry.file_path = entry.bstack1llll11_opy_
        def bstack1l1lll111l1_opy_():
            bstack1ll1lll1ll_opy_ = datetime.now()
            try:
                self.bstack1llll1l1l11_opy_.LogCreatedEvent(req)
                bstack1l1lll1l1l1_opy_.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᑈ"), datetime.now() - bstack1ll1lll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᑉ").format(str(e)))
                traceback.print_exc()
        self.bstack111111l1ll_opy_.enqueue(bstack1l1lll111l1_opy_)
    def __1l111l1l1ll_opy_(self, instance) -> None:
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᑊ")
        bstack1l111ll1lll_opy_ = {bstack11ll11_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᑋ"): bstack1lll11ll1ll_opy_.bstack1l111llll11_opy_()}
        TestFramework.bstack1l1111lll11_opy_(instance, bstack1l111ll1lll_opy_)
    @staticmethod
    def __1l11111l1ll_opy_(instance, args):
        request, bstack1l11l11ll1l_opy_ = args
        bstack1l111llll1l_opy_ = id(bstack1l11l11ll1l_opy_)
        bstack1l11l111111_opy_ = instance.data[TestFramework.bstack1l11111ll11_opy_]
        step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬᑌ")] == bstack1l111llll1l_opy_, bstack1l11l111111_opy_[bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑍ")]), None)
        step.update({
            bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᑎ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11l111111_opy_[bstack11ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑏ")]) if st[bstack11ll11_opy_ (u"࠭ࡩࡥࠩᑐ")] == step[bstack11ll11_opy_ (u"ࠧࡪࡦࠪᑑ")]), None)
        if index is not None:
            bstack1l11l111111_opy_[bstack11ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑒ")][index] = step
        instance.data[TestFramework.bstack1l11111ll11_opy_] = bstack1l11l111111_opy_
    @staticmethod
    def __1l11l1l11l1_opy_(instance, args):
        bstack11ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᑓ")
        bstack1l111l1ll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l11ll1l_opy_ = args[1]
        bstack1l111llll1l_opy_ = id(bstack1l11l11ll1l_opy_)
        bstack1l11l111111_opy_ = instance.data[TestFramework.bstack1l11111ll11_opy_]
        step = None
        if bstack1l111llll1l_opy_ is not None and bstack1l11l111111_opy_.get(bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑔ")):
            step = next(filter(lambda st: st[bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧᑕ")] == bstack1l111llll1l_opy_, bstack1l11l111111_opy_[bstack11ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑖ")]), None)
            step.update({
                bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᑗ"): bstack1l111l1ll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᑘ"): bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᑙ"),
                bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᑚ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᑛ"): bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑜ"),
                })
        index = next((i for i, st in enumerate(bstack1l11l111111_opy_[bstack11ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑝ")]) if st[bstack11ll11_opy_ (u"࠭ࡩࡥࠩᑞ")] == step[bstack11ll11_opy_ (u"ࠧࡪࡦࠪᑟ")]), None)
        if index is not None:
            bstack1l11l111111_opy_[bstack11ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑠ")][index] = step
        instance.data[TestFramework.bstack1l11111ll11_opy_] = bstack1l11l111111_opy_
    @staticmethod
    def __1l11l1111ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᑡ")):
                examples = list(node.callspec.params[bstack11ll11_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᑢ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1l11l1_opy_(self, instance: bstack1llll111l11_opy_, bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_]):
        bstack1l111l1l11l_opy_ = (
            PytestBDDFramework.bstack1l1111llll1_opy_
            if bstack111111111l_opy_[1] == bstack1ll1l1lll11_opy_.PRE
            else PytestBDDFramework.bstack1l11111lll1_opy_
        )
        hook = PytestBDDFramework.bstack1l11l111lll_opy_(instance, bstack1l111l1l11l_opy_)
        entries = hook.get(TestFramework.bstack1l1111lllll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l111lll1l1_opy_, []))
        return entries
    def bstack1l1ll1l1l11_opy_(self, instance: bstack1llll111l11_opy_, bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_]):
        bstack1l111l1l11l_opy_ = (
            PytestBDDFramework.bstack1l1111llll1_opy_
            if bstack111111111l_opy_[1] == bstack1ll1l1lll11_opy_.PRE
            else PytestBDDFramework.bstack1l11111lll1_opy_
        )
        PytestBDDFramework.bstack1l1111lll1l_opy_(instance, bstack1l111l1l11l_opy_)
        TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l111lll1l1_opy_, []).clear()
    @staticmethod
    def bstack1l11l111lll_opy_(instance: bstack1llll111l11_opy_, bstack1l111l1l11l_opy_: str):
        bstack1l111ll1l1l_opy_ = (
            PytestBDDFramework.bstack1l11111l111_opy_
            if bstack1l111l1l11l_opy_ == PytestBDDFramework.bstack1l11111lll1_opy_
            else PytestBDDFramework.bstack1l11l111ll1_opy_
        )
        bstack1l111llllll_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111l1l11l_opy_, None)
        bstack1l1111ll111_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111ll1l1l_opy_, None) if bstack1l111llllll_opy_ else None
        return (
            bstack1l1111ll111_opy_[bstack1l111llllll_opy_][-1]
            if isinstance(bstack1l1111ll111_opy_, dict) and len(bstack1l1111ll111_opy_.get(bstack1l111llllll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l1111lll1l_opy_(instance: bstack1llll111l11_opy_, bstack1l111l1l11l_opy_: str):
        hook = PytestBDDFramework.bstack1l11l111lll_opy_(instance, bstack1l111l1l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111lllll_opy_, []).clear()
    @staticmethod
    def __1l11111l1l1_opy_(instance: bstack1llll111l11_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᑣ"), None)):
            return
        if os.getenv(bstack11ll11_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᑤ"), bstack11ll11_opy_ (u"ࠨ࠱ࠣᑥ")) != bstack11ll11_opy_ (u"ࠢ࠲ࠤᑦ"):
            PytestBDDFramework.logger.warning(bstack11ll11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᑧ"))
            return
        bstack1l11l1l1l11_opy_ = {
            bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᑨ"): (PytestBDDFramework.bstack1l1111llll1_opy_, PytestBDDFramework.bstack1l11l111ll1_opy_),
            bstack11ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᑩ"): (PytestBDDFramework.bstack1l11111lll1_opy_, PytestBDDFramework.bstack1l11111l111_opy_),
        }
        for when in (bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᑪ"), bstack11ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᑫ"), bstack11ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᑬ")):
            bstack1l11l11ll11_opy_ = args[1].get_records(when)
            if not bstack1l11l11ll11_opy_:
                continue
            records = [
                bstack1lll11lll11_opy_(
                    kind=TestFramework.bstack1l1ll1111l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᑭ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᑮ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11l11ll11_opy_
                if isinstance(getattr(r, bstack11ll11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᑯ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111ll1ll1_opy_, bstack1l111ll1l1l_opy_ = bstack1l11l1l1l11_opy_.get(when, (None, None))
            bstack1l11l11l111_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111ll1ll1_opy_, None) if bstack1l111ll1ll1_opy_ else None
            bstack1l1111ll111_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111ll1l1l_opy_, None) if bstack1l11l11l111_opy_ else None
            if isinstance(bstack1l1111ll111_opy_, dict) and len(bstack1l1111ll111_opy_.get(bstack1l11l11l111_opy_, [])) > 0:
                hook = bstack1l1111ll111_opy_[bstack1l11l11l111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111lllll_opy_ in hook:
                    hook[TestFramework.bstack1l1111lllll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l111lll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1111ll1ll_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1lll111111_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l111ll1111_opy_(request.node, scenario)
        bstack1l111111lll_opy_ = feature.filename
        if not bstack1lll111111_opy_ or not test_name or not bstack1l111111lll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l11ll11_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l1l1ll1_opy_: bstack1lll111111_opy_,
            TestFramework.bstack1ll1l111l1l_opy_: test_name,
            TestFramework.bstack1l1l1ll11ll_opy_: bstack1lll111111_opy_,
            TestFramework.bstack1l111l11111_opy_: bstack1l111111lll_opy_,
            TestFramework.bstack1l111l1llll_opy_: PytestBDDFramework.__1l11l1l1111_opy_(feature, scenario),
            TestFramework.bstack1l111l111l1_opy_: code,
            TestFramework.bstack1l1l11l11l1_opy_: TestFramework.bstack1l111111l1l_opy_,
            TestFramework.bstack1l11ll1l1ll_opy_: test_name
        }
    @staticmethod
    def __1l111ll1111_opy_(node, scenario):
        if hasattr(node, bstack11ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑰ")):
            parts = node.nodeid.rsplit(bstack11ll11_opy_ (u"ࠦࡠࠨᑱ"))
            params = parts[-1]
            return bstack11ll11_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᑲ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1l1111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᑳ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᑴ")) else [])
    @staticmethod
    def __1l111l11l11_opy_(location):
        return bstack11ll11_opy_ (u"ࠣ࠼࠽ࠦᑵ").join(filter(lambda x: isinstance(x, str), location))