# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllllll1l_opy_ import bstack11111l11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll111_opy_ import bstack1l111ll11l1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11lllll_opy_,
    bstack1lll1111l1l_opy_,
    bstack1lllll1111l_opy_,
    bstack1l11l1l1lll_opy_,
    bstack1lll11111l1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1lll111l1_opy_
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll1lll1_opy_ import bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack11111lll11_opy_ import bstack11111ll11l_opy_
bstack1l1ll1l11l1_opy_ = bstack1l1lll111l1_opy_()
bstack1l1ll1l1111_opy_ = bstack111lll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᎴ")
bstack1l111lll1l1_opy_ = bstack111lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᎵ")
bstack1l11l1lll11_opy_ = bstack111lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᎶ")
bstack1l111lllll1_opy_ = 1.0
_1l1llll1ll1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111llll11_opy_ = bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᎷ")
    bstack1l111l1l11l_opy_ = bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᎸ")
    bstack1l111lll1ll_opy_ = bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᎹ")
    bstack1l11l1l1ll1_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᎺ")
    bstack1l111l1l1l1_opy_ = bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᎻ")
    bstack1l111ll1lll_opy_: bool
    bstack11111lll11_opy_: bstack11111ll11l_opy_  = None
    bstack1l11l11lll1_opy_ = [
        bstack1lll11lllll_opy_.BEFORE_ALL,
        bstack1lll11lllll_opy_.AFTER_ALL,
        bstack1lll11lllll_opy_.BEFORE_EACH,
        bstack1lll11lllll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l11l11_opy_: Dict[str, str],
        bstack1ll11l1ll1l_opy_: List[str]=[bstack111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᎼ")],
        bstack11111lll11_opy_: bstack11111ll11l_opy_ = None,
        bstack1lll1ll1l11_opy_=None
    ):
        super().__init__(bstack1ll11l1ll1l_opy_, bstack1l111l11l11_opy_, bstack11111lll11_opy_)
        self.bstack1l111ll1lll_opy_ = any(bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᎽ") in item.lower() for item in bstack1ll11l1ll1l_opy_)
        self.bstack1lll1ll1l11_opy_ = bstack1lll1ll1l11_opy_
    def track_event(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11lllll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11l11lll1_opy_:
            bstack1l111ll11l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11lllll_opy_.NONE:
            self.logger.warning(bstack111lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᎾ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠣࠤᎿ"))
            return
        if not self.bstack1l111ll1lll_opy_:
            self.logger.warning(bstack111lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᏀ") + str(str(self.bstack1ll11l1ll1l_opy_)) + bstack111lll_opy_ (u"ࠥࠦᏁ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏂ") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨᏃ"))
            return
        instance = self.__1l11l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᏄ") + str(args) + bstack111lll_opy_ (u"ࠢࠣᏅ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l11lll1_opy_ and test_hook_state == bstack1lllll1111l_opy_.PRE:
                bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1lll111l11_opy_.value)
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack111lll_opy_ (u"ࠣ࠼ࠥᏆ")+str(test_framework_state.name)
                TestFramework.bstack1l111ll1111_opy_(instance, name, bstack1ll11llll11_opy_)
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᏇ").format(e))
        try:
            if test_framework_state == bstack1lll11lllll_opy_.TEST:
                if not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l111l1llll_opy_) and test_hook_state == bstack1lllll1111l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l1111llll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack111lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏈ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠦࠧᏉ"))
                if test_hook_state == bstack1lllll1111l_opy_.PRE and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1llll11ll_opy_):
                    TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l1ll111_opy_(instance, args)
                    self.logger.debug(bstack111lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏊ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠨࠢᏋ"))
                elif test_hook_state == bstack1lllll1111l_opy_.POST and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11111l1l_opy_):
                    TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1ll11111l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᏌ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠣࠤᏍ"))
            elif test_framework_state == bstack1lll11lllll_opy_.STEP:
                if test_hook_state == bstack1lllll1111l_opy_.PRE:
                    PytestBDDFramework.__1l111ll1l1l_opy_(instance, args)
                elif test_hook_state == bstack1lllll1111l_opy_.POST:
                    PytestBDDFramework.__1l11l1l111l_opy_(instance, args)
            elif test_framework_state == bstack1lll11lllll_opy_.LOG and test_hook_state == bstack1lllll1111l_opy_.POST:
                PytestBDDFramework.__1l11l11l111_opy_(instance, *args)
            elif test_framework_state == bstack1lll11lllll_opy_.LOG_REPORT and test_hook_state == bstack1lllll1111l_opy_.POST:
                self.__1l11l1llll1_opy_(instance, *args)
                self.__1l11l11llll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11l11lll1_opy_:
                self.__1l11l11ll11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᏎ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠥࠦᏏ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l1ll11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l11lll1_opy_ and test_hook_state == bstack1lllll1111l_opy_.POST:
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack111lll_opy_ (u"ࠦ࠿ࠨᏐ")+str(test_framework_state.name)
                bstack1ll11llll11_opy_ = TestFramework.bstack1l111ll111l_opy_(instance, name)
                bstack1llll1l1l11_opy_.end(EVENTS.bstack1lll111l11_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏑ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏒ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᏓ").format(e))
    def bstack1l1llll1l1l_opy_(self):
        return self.bstack1l111ll1lll_opy_
    def __1l111l1l1ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᏔ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll1111l1l1_opy_(rep, [bstack111lll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᏕ"), bstack111lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᏖ"), bstack111lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᏗ"), bstack111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᏘ"), bstack111lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᏙ"), bstack111lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᏚ")])
        return None
    def __1l11l1llll1_opy_(self, instance: bstack1lll1111l1l_opy_, *args):
        result = self.__1l111l1l1ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111lllll_opy_ = None
        if result.get(bstack111lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᏛ"), None) == bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᏜ") and len(args) > 1 and getattr(args[1], bstack111lll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᏝ"), None) is not None:
            failure = [{bstack111lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᏞ"): [args[1].excinfo.exconly(), result.get(bstack111lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᏟ"), None)]}]
            bstack11111lllll_opy_ = bstack111lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᏠ") if bstack111lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᏡ") in getattr(args[1].excinfo, bstack111lll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᏢ"), bstack111lll_opy_ (u"ࠤࠥᏣ")) else bstack111lll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᏤ")
        bstack1l11l1l1l11_opy_ = result.get(bstack111lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᏥ"), TestFramework.bstack1l11ll11111_opy_)
        if bstack1l11l1l1l11_opy_ != TestFramework.bstack1l11ll11111_opy_:
            TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l111l11_opy_(instance, {
            TestFramework.bstack1l1l11ll1ll_opy_: failure,
            TestFramework.bstack1l111l11111_opy_: bstack11111lllll_opy_,
            TestFramework.bstack1l1l1l1l1l1_opy_: bstack1l11l1l1l11_opy_,
        })
    def __1l11l1lllll_opy_(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11lllll_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1lll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll1111l_opy_ bstack1l11l111l1l_opy_ this to be bstack111lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᏦ")
            if test_framework_state == bstack1lll11lllll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l111ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11lllll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack111lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᏧ"), None), bstack111lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᏨ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111lll_opy_ (u"ࠣࡰࡲࡨࡪࠨᏩ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack111lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᏪ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111l11l1_opy_(target) if target else None
        return instance
    def __1l11l11ll11_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l11l1l1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l111l1l11l_opy_, {})
        if not key in bstack1l11l11l1l1_opy_:
            bstack1l11l11l1l1_opy_[key] = []
        bstack1l11ll111ll_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l111lll1ll_opy_, {})
        if not key in bstack1l11ll111ll_opy_:
            bstack1l11ll111ll_opy_[key] = []
        bstack1l1111ll111_opy_ = {
            PytestBDDFramework.bstack1l111l1l11l_opy_: bstack1l11l11l1l1_opy_,
            PytestBDDFramework.bstack1l111lll1ll_opy_: bstack1l11ll111ll_opy_,
        }
        if test_hook_state == bstack1lllll1111l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack111lll_opy_ (u"ࠥ࡯ࡪࡿࠢᏫ"): key,
                TestFramework.bstack1l11l1111l1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l1l_opy_: TestFramework.bstack1l11l11l1ll_opy_,
                TestFramework.bstack1l111l11ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111ll1ll1_opy_: [],
                TestFramework.bstack1l11l1l1l1l_opy_: hook_name,
                TestFramework.bstack1l11l1111ll_opy_: bstack1ll1llll1ll_opy_.bstack1l111llll1l_opy_()
            }
            bstack1l11l11l1l1_opy_[key].append(hook)
            bstack1l1111ll111_opy_[PytestBDDFramework.bstack1l11l1l1ll1_opy_] = key
        elif test_hook_state == bstack1lllll1111l_opy_.POST:
            bstack1l11ll11l11_opy_ = bstack1l11l11l1l1_opy_.get(key, [])
            hook = bstack1l11ll11l11_opy_.pop() if bstack1l11ll11l11_opy_ else None
            if hook:
                result = self.__1l111l1l1ll_opy_(*args)
                if result:
                    bstack1l11l1l11ll_opy_ = result.get(bstack111lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᏬ"), TestFramework.bstack1l11l11l1ll_opy_)
                    if bstack1l11l1l11ll_opy_ != TestFramework.bstack1l11l11l1ll_opy_:
                        hook[TestFramework.bstack1l11ll11l1l_opy_] = bstack1l11l1l11ll_opy_
                hook[TestFramework.bstack1l111l111l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l1111ll_opy_] = bstack1ll1llll1ll_opy_.bstack1l111llll1l_opy_()
                self.bstack1l111lll11l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l111111_opy_, [])
                self.bstack1l1lllll111_opy_(instance, logs)
                bstack1l11ll111ll_opy_[key].append(hook)
                bstack1l1111ll111_opy_[PytestBDDFramework.bstack1l111l1l1l1_opy_] = key
        TestFramework.bstack1l11l111l11_opy_(instance, bstack1l1111ll111_opy_)
        self.logger.debug(bstack111lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᏭ") + str(bstack1l11ll111ll_opy_) + bstack111lll_opy_ (u"ࠨࠢᏮ"))
    def __1l11l1lll1l_opy_(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll1111l1l1_opy_(args[0], [bstack111lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᏯ"), bstack111lll_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᏰ"), bstack111lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᏱ"), bstack111lll_opy_ (u"ࠥ࡭ࡩࡹࠢᏲ"), bstack111lll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᏳ"), bstack111lll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᏴ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack111lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᏵ")) else fixturedef.get(bstack111lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᏶"), None)
        fixturename = request.fixturename if hasattr(request, bstack111lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨ᏷")) else None
        node = request.node if hasattr(request, bstack111lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᏸ")) else None
        target = request.node.nodeid if hasattr(node, bstack111lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᏹ")) else None
        baseid = fixturedef.get(bstack111lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᏺ"), None) or bstack111lll_opy_ (u"ࠧࠨᏻ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111lll_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᏼ")):
            target = PytestBDDFramework.__1l11l11l11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᏽ")) else None
            if target and not TestFramework.bstack11111l11l1_opy_(target):
                self.__1l11l111ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ᏾") + str(test_hook_state) + bstack111lll_opy_ (u"ࠤࠥ᏿"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣ᐀") + str(target) + bstack111lll_opy_ (u"ࠦࠧᐁ"))
            return None
        instance = TestFramework.bstack11111l11l1_opy_(target)
        if not instance:
            self.logger.warning(bstack111lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᐂ") + str(target) + bstack111lll_opy_ (u"ࠨࠢᐃ"))
            return None
        bstack1l1111ll1l1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l111llll11_opy_, {})
        if os.getenv(bstack111lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᐄ"), bstack111lll_opy_ (u"ࠣ࠳ࠥᐅ")) == bstack111lll_opy_ (u"ࠤ࠴ࠦᐆ"):
            bstack1l11l1ll1l1_opy_ = bstack111lll_opy_ (u"ࠥ࠾ࠧᐇ").join((scope, fixturename))
            bstack1l1111l1lll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l1l1111_opy_ = {
                bstack111lll_opy_ (u"ࠦࡰ࡫ࡹࠣᐈ"): bstack1l11l1ll1l1_opy_,
                bstack111lll_opy_ (u"ࠧࡺࡡࡨࡵࠥᐉ"): PytestBDDFramework.__1l111lll111_opy_(request.node, scenario),
                bstack111lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᐊ"): fixturedef,
                bstack111lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐋ"): scope,
                bstack111lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᐌ"): None,
            }
            try:
                if test_hook_state == bstack1lllll1111l_opy_.POST and callable(getattr(args[-1], bstack111lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᐍ"), None)):
                    bstack1l11l1l1111_opy_[bstack111lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᐎ")] = TestFramework.bstack1ll1111ll11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lllll1111l_opy_.PRE:
                bstack1l11l1l1111_opy_[bstack111lll_opy_ (u"ࠦࡺࡻࡩࡥࠤᐏ")] = uuid4().__str__()
                bstack1l11l1l1111_opy_[PytestBDDFramework.bstack1l111l11ll1_opy_] = bstack1l1111l1lll_opy_
            elif test_hook_state == bstack1lllll1111l_opy_.POST:
                bstack1l11l1l1111_opy_[PytestBDDFramework.bstack1l111l111l1_opy_] = bstack1l1111l1lll_opy_
            if bstack1l11l1ll1l1_opy_ in bstack1l1111ll1l1_opy_:
                bstack1l1111ll1l1_opy_[bstack1l11l1ll1l1_opy_].update(bstack1l11l1l1111_opy_)
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᐐ") + str(bstack1l1111ll1l1_opy_[bstack1l11l1ll1l1_opy_]) + bstack111lll_opy_ (u"ࠨࠢᐑ"))
            else:
                bstack1l1111ll1l1_opy_[bstack1l11l1ll1l1_opy_] = bstack1l11l1l1111_opy_
                self.logger.debug(bstack111lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᐒ") + str(len(bstack1l1111ll1l1_opy_)) + bstack111lll_opy_ (u"ࠣࠤᐓ"))
        TestFramework.bstack11111ll111_opy_(instance, PytestBDDFramework.bstack1l111llll11_opy_, bstack1l1111ll1l1_opy_)
        self.logger.debug(bstack111lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᐔ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠥࠦᐕ"))
        return instance
    def __1l11l111ll1_opy_(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111l11ll_opy_.create_context(target)
        ob = bstack1lll1111l1l_opy_(ctx, self.bstack1ll11l1ll1l_opy_, self.bstack1l111l11l11_opy_, test_framework_state)
        TestFramework.bstack1l11l111l11_opy_(ob, {
            TestFramework.bstack1ll11ll11ll_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll1l1ll_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1l11l1_opy_: [],
            PytestBDDFramework.bstack1l111llll11_opy_: {},
            PytestBDDFramework.bstack1l111lll1ll_opy_: {},
            PytestBDDFramework.bstack1l111l1l11l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11111ll111_opy_(ob, TestFramework.bstack1l11l111lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11111ll111_opy_(ob, TestFramework.bstack1ll1l11ll1l_opy_, context.platform_index)
        TestFramework.bstack1lllll1ll11_opy_[ctx.id] = ob
        self.logger.debug(bstack111lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᐖ") + str(TestFramework.bstack1lllll1ll11_opy_.keys()) + bstack111lll_opy_ (u"ࠧࠨᐗ"))
        return ob
    @staticmethod
    def __1l11l1ll111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111lll_opy_ (u"࠭ࡩࡥࠩᐘ"): id(step),
                bstack111lll_opy_ (u"ࠧࡵࡧࡻࡸࠬᐙ"): step.name,
                bstack111lll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᐚ"): step.keyword,
            })
        meta = {
            bstack111lll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᐛ"): {
                bstack111lll_opy_ (u"ࠪࡲࡦࡳࡥࠨᐜ"): feature.name,
                bstack111lll_opy_ (u"ࠫࡵࡧࡴࡩࠩᐝ"): feature.filename,
                bstack111lll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᐞ"): feature.description
            },
            bstack111lll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᐟ"): {
                bstack111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᐠ"): scenario.name
            },
            bstack111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐡ"): steps,
            bstack111lll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᐢ"): PytestBDDFramework.__1l111l1l111_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l1111ll1ll_opy_: meta
            }
        )
    def bstack1l111lll11l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᐣ")
        global _1l1llll1ll1_opy_
        platform_index = os.environ[bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐤ")]
        bstack1l1lll11ll1_opy_ = os.path.join(bstack1l1ll1l11l1_opy_, (bstack1l1ll1l1111_opy_ + str(platform_index)), bstack1l111lll1l1_opy_)
        if not os.path.exists(bstack1l1lll11ll1_opy_) or not os.path.isdir(bstack1l1lll11ll1_opy_):
            return
        logs = hook.get(bstack111lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᐥ"), [])
        with os.scandir(bstack1l1lll11ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1llll1ll1_opy_:
                    self.logger.info(bstack111lll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᐦ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111lll_opy_ (u"ࠢࠣᐧ")
                    log_entry = bstack1lll11111l1_opy_(
                        kind=bstack111lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᐨ"),
                        message=bstack111lll_opy_ (u"ࠤࠥᐩ"),
                        level=bstack111lll_opy_ (u"ࠥࠦᐪ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1ll1ll_opy_=entry.stat().st_size,
                        bstack1l1lll1llll_opy_=bstack111lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᐫ"),
                        bstack11ll1_opy_=os.path.abspath(entry.path),
                        bstack1l111l1ll1l_opy_=hook.get(TestFramework.bstack1l11l1111l1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1llll1ll1_opy_.add(abs_path)
        platform_index = os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᐬ")]
        bstack1l111llllll_opy_ = os.path.join(bstack1l1ll1l11l1_opy_, (bstack1l1ll1l1111_opy_ + str(platform_index)), bstack1l111lll1l1_opy_, bstack1l11l1lll11_opy_)
        if not os.path.exists(bstack1l111llllll_opy_) or not os.path.isdir(bstack1l111llllll_opy_):
            self.logger.info(bstack111lll_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᐭ").format(bstack1l111llllll_opy_))
        else:
            self.logger.info(bstack111lll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᐮ").format(bstack1l111llllll_opy_))
            with os.scandir(bstack1l111llllll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1llll1ll1_opy_:
                        self.logger.info(bstack111lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᐯ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111lll_opy_ (u"ࠤࠥᐰ")
                        log_entry = bstack1lll11111l1_opy_(
                            kind=bstack111lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᐱ"),
                            message=bstack111lll_opy_ (u"ࠦࠧᐲ"),
                            level=bstack111lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᐳ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1ll1ll_opy_=entry.stat().st_size,
                            bstack1l1lll1llll_opy_=bstack111lll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᐴ"),
                            bstack11ll1_opy_=os.path.abspath(entry.path),
                            bstack1ll11111l11_opy_=hook.get(TestFramework.bstack1l11l1111l1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1llll1ll1_opy_.add(abs_path)
        hook[bstack111lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᐵ")] = logs
    def bstack1l1lllll111_opy_(
        self,
        bstack1l1lllll1l1_opy_: bstack1lll1111l1l_opy_,
        entries: List[bstack1lll11111l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᐶ"))
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll1l11ll1l_opy_)
        req.execution_context.hash = str(bstack1l1lllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll11ll11ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1l1lll1l1ll_opy_)
            log_entry.uuid = entry.bstack1l111l1ll1l_opy_
            log_entry.test_framework_state = bstack1l1lllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack111lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᐷ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111lll_opy_ (u"ࠥࠦᐸ")
            if entry.kind == bstack111lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᐹ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1ll_opy_
                log_entry.file_path = entry.bstack11ll1_opy_
        def bstack1ll1111111l_opy_():
            bstack11ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.LogCreatedEvent(req)
                bstack1l1lllll1l1_opy_.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᐺ"), datetime.now() - bstack11ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᐻ").format(str(e)))
                traceback.print_exc()
        self.bstack11111lll11_opy_.enqueue(bstack1ll1111111l_opy_)
    def __1l11l11llll_opy_(self, instance) -> None:
        bstack111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᐼ")
        bstack1l1111ll111_opy_ = {bstack111lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᐽ"): bstack1ll1llll1ll_opy_.bstack1l111llll1l_opy_()}
        TestFramework.bstack1l11l111l11_opy_(instance, bstack1l1111ll111_opy_)
    @staticmethod
    def __1l111ll1l1l_opy_(instance, args):
        request, bstack1l1111lll11_opy_ = args
        bstack1l111l11l1l_opy_ = id(bstack1l1111lll11_opy_)
        bstack1l11l11ll1l_opy_ = instance.data[TestFramework.bstack1l1111ll1ll_opy_]
        step = next(filter(lambda st: st[bstack111lll_opy_ (u"ࠩ࡬ࡨࠬᐾ")] == bstack1l111l11l1l_opy_, bstack1l11l11ll1l_opy_[bstack111lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐿ")]), None)
        step.update({
            bstack111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᑀ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11l11ll1l_opy_[bstack111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑁ")]) if st[bstack111lll_opy_ (u"࠭ࡩࡥࠩᑂ")] == step[bstack111lll_opy_ (u"ࠧࡪࡦࠪᑃ")]), None)
        if index is not None:
            bstack1l11l11ll1l_opy_[bstack111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑄ")][index] = step
        instance.data[TestFramework.bstack1l1111ll1ll_opy_] = bstack1l11l11ll1l_opy_
    @staticmethod
    def __1l11l1l111l_opy_(instance, args):
        bstack111lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᑅ")
        bstack1l11l1ll1ll_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1111lll11_opy_ = args[1]
        bstack1l111l11l1l_opy_ = id(bstack1l1111lll11_opy_)
        bstack1l11l11ll1l_opy_ = instance.data[TestFramework.bstack1l1111ll1ll_opy_]
        step = None
        if bstack1l111l11l1l_opy_ is not None and bstack1l11l11ll1l_opy_.get(bstack111lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᑆ")):
            step = next(filter(lambda st: st[bstack111lll_opy_ (u"ࠫ࡮ࡪࠧᑇ")] == bstack1l111l11l1l_opy_, bstack1l11l11ll1l_opy_[bstack111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑈ")]), None)
            step.update({
                bstack111lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᑉ"): bstack1l11l1ll1ll_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᑊ"): bstack111lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᑋ"),
                bstack111lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᑌ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack111lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᑍ"): bstack111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑎ"),
                })
        index = next((i for i, st in enumerate(bstack1l11l11ll1l_opy_[bstack111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᑏ")]) if st[bstack111lll_opy_ (u"࠭ࡩࡥࠩᑐ")] == step[bstack111lll_opy_ (u"ࠧࡪࡦࠪᑑ")]), None)
        if index is not None:
            bstack1l11l11ll1l_opy_[bstack111lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑒ")][index] = step
        instance.data[TestFramework.bstack1l1111ll1ll_opy_] = bstack1l11l11ll1l_opy_
    @staticmethod
    def __1l111l1l111_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack111lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᑓ")):
                examples = list(node.callspec.params[bstack111lll_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᑔ")].values())
            return examples
        except:
            return []
    def bstack1l1lll1ll1l_opy_(self, instance: bstack1lll1111l1l_opy_, bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_]):
        bstack1l111l1lll1_opy_ = (
            PytestBDDFramework.bstack1l11l1l1ll1_opy_
            if bstack11111l1l11_opy_[1] == bstack1lllll1111l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l1l1_opy_
        )
        hook = PytestBDDFramework.bstack1l1111l1l11_opy_(instance, bstack1l111l1lll1_opy_)
        entries = hook.get(TestFramework.bstack1l111ll1ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, []))
        return entries
    def bstack1l1lllll1ll_opy_(self, instance: bstack1lll1111l1l_opy_, bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_]):
        bstack1l111l1lll1_opy_ = (
            PytestBDDFramework.bstack1l11l1l1ll1_opy_
            if bstack11111l1l11_opy_[1] == bstack1lllll1111l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l1l1_opy_
        )
        PytestBDDFramework.bstack1l111l111ll_opy_(instance, bstack1l111l1lll1_opy_)
        TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, []).clear()
    @staticmethod
    def bstack1l1111l1l11_opy_(instance: bstack1lll1111l1l_opy_, bstack1l111l1lll1_opy_: str):
        bstack1l1111lllll_opy_ = (
            PytestBDDFramework.bstack1l111lll1ll_opy_
            if bstack1l111l1lll1_opy_ == PytestBDDFramework.bstack1l111l1l1l1_opy_
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        bstack1l11l1ll11l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1lll1_opy_, None)
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l1111lllll_opy_, None) if bstack1l11l1ll11l_opy_ else None
        return (
            bstack1l111ll1l11_opy_[bstack1l11l1ll11l_opy_][-1]
            if isinstance(bstack1l111ll1l11_opy_, dict) and len(bstack1l111ll1l11_opy_.get(bstack1l11l1ll11l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l111ll_opy_(instance: bstack1lll1111l1l_opy_, bstack1l111l1lll1_opy_: str):
        hook = PytestBDDFramework.bstack1l1111l1l11_opy_(instance, bstack1l111l1lll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111ll1ll1_opy_, []).clear()
    @staticmethod
    def __1l11l11l111_opy_(instance: bstack1lll1111l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᑕ"), None)):
            return
        if os.getenv(bstack111lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᑖ"), bstack111lll_opy_ (u"ࠨ࠱ࠣᑗ")) != bstack111lll_opy_ (u"ࠢ࠲ࠤᑘ"):
            PytestBDDFramework.logger.warning(bstack111lll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᑙ"))
            return
        bstack1l1111ll11l_opy_ = {
            bstack111lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᑚ"): (PytestBDDFramework.bstack1l11l1l1ll1_opy_, PytestBDDFramework.bstack1l111l1l11l_opy_),
            bstack111lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᑛ"): (PytestBDDFramework.bstack1l111l1l1l1_opy_, PytestBDDFramework.bstack1l111lll1ll_opy_),
        }
        for when in (bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᑜ"), bstack111lll_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᑝ"), bstack111lll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᑞ")):
            bstack1l11ll111l1_opy_ = args[1].get_records(when)
            if not bstack1l11ll111l1_opy_:
                continue
            records = [
                bstack1lll11111l1_opy_(
                    kind=TestFramework.bstack1l1lll1111l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111lll_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᑟ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᑠ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll111l1_opy_
                if isinstance(getattr(r, bstack111lll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᑡ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l11111l_opy_, bstack1l1111lllll_opy_ = bstack1l1111ll11l_opy_.get(when, (None, None))
            bstack1l1111l1l1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l11l11111l_opy_, None) if bstack1l11l11111l_opy_ else None
            bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l1111lllll_opy_, None) if bstack1l1111l1l1l_opy_ else None
            if isinstance(bstack1l111ll1l11_opy_, dict) and len(bstack1l111ll1l11_opy_.get(bstack1l1111l1l1l_opy_, [])) > 0:
                hook = bstack1l111ll1l11_opy_[bstack1l1111l1l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111ll1ll1_opy_ in hook:
                    hook[TestFramework.bstack1l111ll1ll1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1111llll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11lll1111l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1111l1ll1_opy_(request.node, scenario)
        bstack1l111l1111l_opy_ = feature.filename
        if not bstack11lll1111l_opy_ or not test_name or not bstack1l111l1111l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1llll_opy_: bstack11lll1111l_opy_,
            TestFramework.bstack1ll11l1l1ll_opy_: test_name,
            TestFramework.bstack1l1ll111ll1_opy_: bstack11lll1111l_opy_,
            TestFramework.bstack1l111l11lll_opy_: bstack1l111l1111l_opy_,
            TestFramework.bstack1l111ll11ll_opy_: PytestBDDFramework.__1l111lll111_opy_(feature, scenario),
            TestFramework.bstack1l1111lll1l_opy_: code,
            TestFramework.bstack1l1l1l1l1l1_opy_: TestFramework.bstack1l11ll11111_opy_,
            TestFramework.bstack1l11lllll11_opy_: test_name
        }
    @staticmethod
    def __1l1111l1ll1_opy_(node, scenario):
        if hasattr(node, bstack111lll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑢ")):
            parts = node.nodeid.rsplit(bstack111lll_opy_ (u"ࠦࡠࠨᑣ"))
            params = parts[-1]
            return bstack111lll_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᑤ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111lll111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack111lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᑥ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack111lll_opy_ (u"ࠧࡵࡣࡪࡷࠬᑦ")) else [])
    @staticmethod
    def __1l11l11l11l_opy_(location):
        return bstack111lll_opy_ (u"ࠣ࠼࠽ࠦᑧ").join(filter(lambda x: isinstance(x, str), location))