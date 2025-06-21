# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll111ll11_opy_ import bstack1l111l1l11l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll11l11_opy_,
    bstack1lll1l1l1l1_opy_,
    bstack1lll1lll111_opy_,
    bstack1l1111l1l1l_opy_,
    bstack1lll111l1l1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1l1llllll_opy_
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1ll11_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111l1l1_opy_
bstack1l1lll11l1l_opy_ = bstack1l1l1llllll_opy_()
bstack1l1llllll1l_opy_ = bstack1l1l1l1_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᏃ")
bstack1l11l1l11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᏄ")
bstack1l111ll11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᏅ")
bstack1l1111lllll_opy_ = 1.0
_1l1lll111l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᏆ")
    bstack1l11l11lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᏇ")
    bstack1l11111lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᏈ")
    bstack1l111lll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᏉ")
    bstack1l11l1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᏊ")
    bstack1l111llll1l_opy_: bool
    bstack111111lll1_opy_: bstack111111l1l1_opy_  = None
    bstack1l1111llll1_opy_ = [
        bstack1ll1ll11l11_opy_.BEFORE_ALL,
        bstack1ll1ll11l11_opy_.AFTER_ALL,
        bstack1ll1ll11l11_opy_.BEFORE_EACH,
        bstack1ll1ll11l11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l11111l_opy_: Dict[str, str],
        bstack1ll1l111ll1_opy_: List[str]=[bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᏋ")],
        bstack111111lll1_opy_: bstack111111l1l1_opy_ = None,
        bstack1ll1ll111l1_opy_=None
    ):
        super().__init__(bstack1ll1l111ll1_opy_, bstack1l11l11111l_opy_, bstack111111lll1_opy_)
        self.bstack1l111llll1l_opy_ = any(bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᏌ") in item.lower() for item in bstack1ll1l111ll1_opy_)
        self.bstack1ll1ll111l1_opy_ = bstack1ll1ll111l1_opy_
    def track_event(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll11l11_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_:
            bstack1l111l1l11l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll11l11_opy_.NONE:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᏍ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠤࠥᏎ"))
            return
        if not self.bstack1l111llll1l_opy_:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᏏ") + str(str(self.bstack1ll1l111ll1_opy_)) + bstack1l1l1l1_opy_ (u"ࠦࠧᏐ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏑ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢᏒ"))
            return
        instance = self.__1l111l1llll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᏓ") + str(args) + bstack1l1l1l1_opy_ (u"ࠣࠤᏔ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll1lll111_opy_.PRE:
                bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1l11lll111_opy_.value)
                name = str(EVENTS.bstack1l11lll111_opy_.name)+bstack1l1l1l1_opy_ (u"ࠤ࠽ࠦᏕ")+str(test_framework_state.name)
                TestFramework.bstack1l11l111l1l_opy_(instance, name, bstack1ll111ll1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᏖ").format(e))
        try:
            if test_framework_state == bstack1ll1ll11l11_opy_.TEST:
                if not TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l11l111l11_opy_) and test_hook_state == bstack1lll1lll111_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11l111111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᏗ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠧࠨᏘ"))
                if test_hook_state == bstack1lll1lll111_opy_.PRE and not TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_):
                    TestFramework.bstack1lllll1111l_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11111llll_opy_(instance, args)
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᏙ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠢࠣᏚ"))
                elif test_hook_state == bstack1lll1lll111_opy_.POST and not TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1lll1l111_opy_):
                    TestFramework.bstack1lllll1111l_opy_(instance, TestFramework.bstack1l1lll1l111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᏛ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠤࠥᏜ"))
            elif test_framework_state == bstack1ll1ll11l11_opy_.STEP:
                if test_hook_state == bstack1lll1lll111_opy_.PRE:
                    PytestBDDFramework.__1l111111lll_opy_(instance, args)
                elif test_hook_state == bstack1lll1lll111_opy_.POST:
                    PytestBDDFramework.__1l11l111lll_opy_(instance, args)
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG and test_hook_state == bstack1lll1lll111_opy_.POST:
                PytestBDDFramework.__1l111ll1l11_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG_REPORT and test_hook_state == bstack1lll1lll111_opy_.POST:
                self.__1l1111ll11l_opy_(instance, *args)
                self.__1l111llllll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_:
                self.__1l111111l1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᏝ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠦࠧᏞ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l11l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll1lll111_opy_.POST:
                name = str(EVENTS.bstack1l11lll111_opy_.name)+bstack1l1l1l1_opy_ (u"ࠧࡀࠢᏟ")+str(test_framework_state.name)
                bstack1ll111ll1l1_opy_ = TestFramework.bstack1l111l1l1ll_opy_(instance, name)
                bstack1lll1ll11l1_opy_.end(EVENTS.bstack1l11lll111_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᏠ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᏡ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᏢ").format(e))
    def bstack1l1ll1l1l11_opy_(self):
        return self.bstack1l111llll1l_opy_
    def __1l11l1111ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᏣ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll1ll1ll_opy_(rep, [bstack1l1l1l1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᏤ"), bstack1l1l1l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᏥ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᏦ"), bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᏧ"), bstack1l1l1l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᏨ"), bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᏩ")])
        return None
    def __1l1111ll11l_opy_(self, instance: bstack1lll1l1l1l1_opy_, *args):
        result = self.__1l11l1111ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l11ll_opy_ = None
        if result.get(bstack1l1l1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᏪ"), None) == bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᏫ") and len(args) > 1 and getattr(args[1], bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᏬ"), None) is not None:
            failure = [{bstack1l1l1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᏭ"): [args[1].excinfo.exconly(), result.get(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᏮ"), None)]}]
            bstack11111l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᏯ") if bstack1l1l1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᏰ") in getattr(args[1].excinfo, bstack1l1l1l1_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᏱ"), bstack1l1l1l1_opy_ (u"ࠥࠦᏲ")) else bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᏳ")
        bstack1l11111l11l_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᏴ"), TestFramework.bstack1l11l11ll1l_opy_)
        if bstack1l11111l11l_opy_ != TestFramework.bstack1l11l11ll1l_opy_:
            TestFramework.bstack1lllll1111l_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11111ll1l_opy_(instance, {
            TestFramework.bstack1l1l111l1l1_opy_: failure,
            TestFramework.bstack1l111lllll1_opy_: bstack11111l11ll_opy_,
            TestFramework.bstack1l1l111ll11_opy_: bstack1l11111l11l_opy_,
        })
    def __1l111l1llll_opy_(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll11l11_opy_.SETUP_FIXTURE:
            instance = self.__1l1111l1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l1111l_opy_ bstack1l111ll111l_opy_ this to be bstack1l1l1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᏵ")
            if test_framework_state == bstack1ll1ll11l11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111ll1111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧ᏶"), None), bstack1l1l1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᏷"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1l1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᏸ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᏹ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llllllllll_opy_(target) if target else None
        return instance
    def __1l111111l1l_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l111ll1_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, PytestBDDFramework.bstack1l11l11lll1_opy_, {})
        if not key in bstack1l11l111ll1_opy_:
            bstack1l11l111ll1_opy_[key] = []
        bstack1l1111lll11_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, PytestBDDFramework.bstack1l11111lll1_opy_, {})
        if not key in bstack1l1111lll11_opy_:
            bstack1l1111lll11_opy_[key] = []
        bstack1l11l1l1l1l_opy_ = {
            PytestBDDFramework.bstack1l11l11lll1_opy_: bstack1l11l111ll1_opy_,
            PytestBDDFramework.bstack1l11111lll1_opy_: bstack1l1111lll11_opy_,
        }
        if test_hook_state == bstack1lll1lll111_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1l1l1_opy_ (u"ࠦࡰ࡫ࡹࠣᏺ"): key,
                TestFramework.bstack1l11l11l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l111l1l111_opy_: TestFramework.bstack1l111l1ll11_opy_,
                TestFramework.bstack1l1111ll1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11111ll11_opy_: [],
                TestFramework.bstack1l11l1111l1_opy_: hook_name,
                TestFramework.bstack1l111ll1lll_opy_: bstack1lll11l1lll_opy_.bstack1l11111l1ll_opy_()
            }
            bstack1l11l111ll1_opy_[key].append(hook)
            bstack1l11l1l1l1l_opy_[PytestBDDFramework.bstack1l111lll1ll_opy_] = key
        elif test_hook_state == bstack1lll1lll111_opy_.POST:
            bstack1l1111l11ll_opy_ = bstack1l11l111ll1_opy_.get(key, [])
            hook = bstack1l1111l11ll_opy_.pop() if bstack1l1111l11ll_opy_ else None
            if hook:
                result = self.__1l11l1111ll_opy_(*args)
                if result:
                    bstack1l1111ll1ll_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᏻ"), TestFramework.bstack1l111l1ll11_opy_)
                    if bstack1l1111ll1ll_opy_ != TestFramework.bstack1l111l1ll11_opy_:
                        hook[TestFramework.bstack1l111l1l111_opy_] = bstack1l1111ll1ll_opy_
                hook[TestFramework.bstack1l1111l111l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll1lll_opy_] = bstack1lll11l1lll_opy_.bstack1l11111l1ll_opy_()
                self.bstack1l111l11ll1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1111lll1l_opy_, [])
                self.bstack1l1lll11111_opy_(instance, logs)
                bstack1l1111lll11_opy_[key].append(hook)
                bstack1l11l1l1l1l_opy_[PytestBDDFramework.bstack1l11l1l1ll1_opy_] = key
        TestFramework.bstack1l11111ll1l_opy_(instance, bstack1l11l1l1l1l_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᏼ") + str(bstack1l1111lll11_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣᏽ"))
    def __1l1111l1111_opy_(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll1ll1ll_opy_(args[0], [bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᏾"), bstack1l1l1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥ᏿"), bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥ᐀"), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡪࡳࠣᐁ"), bstack1l1l1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᐂ"), bstack1l1l1l1_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᐃ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1l1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᐄ")) else fixturedef.get(bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᐅ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1l1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᐆ")) else None
        node = request.node if hasattr(request, bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣᐇ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1l1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᐈ")) else None
        baseid = fixturedef.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᐉ"), None) or bstack1l1l1l1_opy_ (u"ࠨࠢᐊ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1l1l1_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᐋ")):
            target = PytestBDDFramework.__1l111llll11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᐌ")) else None
            if target and not TestFramework.bstack1llllllllll_opy_(target):
                self.__1l111ll1111_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᐍ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠥࠦᐎ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᐏ") + str(target) + bstack1l1l1l1_opy_ (u"ࠧࠨᐐ"))
            return None
        instance = TestFramework.bstack1llllllllll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᐑ") + str(target) + bstack1l1l1l1_opy_ (u"ࠢࠣᐒ"))
            return None
        bstack1l111l111ll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, PytestBDDFramework.bstack1l11l1l111l_opy_, {})
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᐓ"), bstack1l1l1l1_opy_ (u"ࠤ࠴ࠦᐔ")) == bstack1l1l1l1_opy_ (u"ࠥ࠵ࠧᐕ"):
            bstack1l111l1ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࠿ࠨᐖ").join((scope, fixturename))
            bstack1l11l11ll11_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111lll11l_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠧࡱࡥࡺࠤᐗ"): bstack1l111l1ll1l_opy_,
                bstack1l1l1l1_opy_ (u"ࠨࡴࡢࡩࡶࠦᐘ"): PytestBDDFramework.__1l11l1l1111_opy_(request.node, scenario),
                bstack1l1l1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᐙ"): fixturedef,
                bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᐚ"): scope,
                bstack1l1l1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᐛ"): None,
            }
            try:
                if test_hook_state == bstack1lll1lll111_opy_.POST and callable(getattr(args[-1], bstack1l1l1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᐜ"), None)):
                    bstack1l111lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤᐝ")] = TestFramework.bstack1l1llllllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1lll111_opy_.PRE:
                bstack1l111lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥᐞ")] = uuid4().__str__()
                bstack1l111lll11l_opy_[PytestBDDFramework.bstack1l1111ll1l1_opy_] = bstack1l11l11ll11_opy_
            elif test_hook_state == bstack1lll1lll111_opy_.POST:
                bstack1l111lll11l_opy_[PytestBDDFramework.bstack1l1111l111l_opy_] = bstack1l11l11ll11_opy_
            if bstack1l111l1ll1l_opy_ in bstack1l111l111ll_opy_:
                bstack1l111l111ll_opy_[bstack1l111l1ll1l_opy_].update(bstack1l111lll11l_opy_)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᐟ") + str(bstack1l111l111ll_opy_[bstack1l111l1ll1l_opy_]) + bstack1l1l1l1_opy_ (u"ࠢࠣᐠ"))
            else:
                bstack1l111l111ll_opy_[bstack1l111l1ll1l_opy_] = bstack1l111lll11l_opy_
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᐡ") + str(len(bstack1l111l111ll_opy_)) + bstack1l1l1l1_opy_ (u"ࠤࠥᐢ"))
        TestFramework.bstack1lllll1111l_opy_(instance, PytestBDDFramework.bstack1l11l1l111l_opy_, bstack1l111l111ll_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᐣ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠦࠧᐤ"))
        return instance
    def __1l111ll1111_opy_(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llllll11ll_opy_.create_context(target)
        ob = bstack1lll1l1l1l1_opy_(ctx, self.bstack1ll1l111ll1_opy_, self.bstack1l11l11111l_opy_, test_framework_state)
        TestFramework.bstack1l11111ll1l_opy_(ob, {
            TestFramework.bstack1ll1l11l1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1111l1_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1lll1_opy_: [],
            PytestBDDFramework.bstack1l11l1l111l_opy_: {},
            PytestBDDFramework.bstack1l11111lll1_opy_: {},
            PytestBDDFramework.bstack1l11l11lll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllll1111l_opy_(ob, TestFramework.bstack1l11l11l111_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllll1111l_opy_(ob, TestFramework.bstack1ll111ll1ll_opy_, context.platform_index)
        TestFramework.bstack1llllllll11_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᐥ") + str(TestFramework.bstack1llllllll11_opy_.keys()) + bstack1l1l1l1_opy_ (u"ࠨࠢᐦ"))
        return ob
    @staticmethod
    def __1l11111llll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪᐧ"): id(step),
                bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᐨ"): step.name,
                bstack1l1l1l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᐩ"): step.keyword,
            })
        meta = {
            bstack1l1l1l1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᐪ"): {
                bstack1l1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᐫ"): feature.name,
                bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪᐬ"): feature.filename,
                bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᐭ"): feature.description
            },
            bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᐮ"): {
                bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᐯ"): scenario.name
            },
            bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐰ"): steps,
            bstack1l1l1l1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᐱ"): PytestBDDFramework.__1l111l11lll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111ll1l1l_opy_: meta
            }
        )
    def bstack1l111l11ll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1l1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᐲ")
        global _1l1lll111l1_opy_
        platform_index = os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᐳ")]
        bstack1l1ll111l1l_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1llllll1l_opy_ + str(platform_index)), bstack1l11l1l11l1_opy_)
        if not os.path.exists(bstack1l1ll111l1l_opy_) or not os.path.isdir(bstack1l1ll111l1l_opy_):
            return
        logs = hook.get(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᐴ"), [])
        with os.scandir(bstack1l1ll111l1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1lll111l1_opy_:
                    self.logger.info(bstack1l1l1l1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᐵ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1l1l1_opy_ (u"ࠣࠤᐶ")
                    log_entry = bstack1lll111l1l1_opy_(
                        kind=bstack1l1l1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᐷ"),
                        message=bstack1l1l1l1_opy_ (u"ࠥࠦᐸ"),
                        level=bstack1l1l1l1_opy_ (u"ࠦࠧᐹ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll11llll_opy_=entry.stat().st_size,
                        bstack1l1llll1l1l_opy_=bstack1l1l1l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᐺ"),
                        bstack111l1l1_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l1l11_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1lll111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᐻ")]
        bstack1l11111l111_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1llllll1l_opy_ + str(platform_index)), bstack1l11l1l11l1_opy_, bstack1l111ll11ll_opy_)
        if not os.path.exists(bstack1l11111l111_opy_) or not os.path.isdir(bstack1l11111l111_opy_):
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᐼ").format(bstack1l11111l111_opy_))
        else:
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᐽ").format(bstack1l11111l111_opy_))
            with os.scandir(bstack1l11111l111_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1lll111l1_opy_:
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᐾ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1l1l1_opy_ (u"ࠥࠦᐿ")
                        log_entry = bstack1lll111l1l1_opy_(
                            kind=bstack1l1l1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᑀ"),
                            message=bstack1l1l1l1_opy_ (u"ࠧࠨᑁ"),
                            level=bstack1l1l1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᑂ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll11llll_opy_=entry.stat().st_size,
                            bstack1l1llll1l1l_opy_=bstack1l1l1l1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᑃ"),
                            bstack111l1l1_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1ll11l_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1lll111l1_opy_.add(abs_path)
        hook[bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᑄ")] = logs
    def bstack1l1lll11111_opy_(
        self,
        bstack1l1lll111ll_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1lll111l1l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᑅ"))
        req.platform_index = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll111ll1ll_opy_)
        req.execution_context.hash = str(bstack1l1lll111ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll1l11l1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1ll1111l1_opy_)
            log_entry.uuid = entry.bstack1l11l1l1l11_opy_
            log_entry.test_framework_state = bstack1l1lll111ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1l1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᑆ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1l1l1_opy_ (u"ࠦࠧᑇ")
            if entry.kind == bstack1l1l1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᑈ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll11llll_opy_
                log_entry.file_path = entry.bstack111l1l1_opy_
        def bstack1l1lll11lll_opy_():
            bstack1l1ll1l1ll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll111l1_opy_.LogCreatedEvent(req)
                bstack1l1lll111ll_opy_.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᑉ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᑊ").format(str(e)))
                traceback.print_exc()
        self.bstack111111lll1_opy_.enqueue(bstack1l1lll11lll_opy_)
    def __1l111llllll_opy_(self, instance) -> None:
        bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᑋ")
        bstack1l11l1l1l1l_opy_ = {bstack1l1l1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᑌ"): bstack1lll11l1lll_opy_.bstack1l11111l1ll_opy_()}
        TestFramework.bstack1l11111ll1l_opy_(instance, bstack1l11l1l1l1l_opy_)
    @staticmethod
    def __1l111111lll_opy_(instance, args):
        request, bstack1l1111l11l1_opy_ = args
        bstack1l111111ll1_opy_ = id(bstack1l1111l11l1_opy_)
        bstack1l1111l1l11_opy_ = instance.data[TestFramework.bstack1l111ll1l1l_opy_]
        step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭ᑍ")] == bstack1l111111ll1_opy_, bstack1l1111l1l11_opy_[bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑎ")]), None)
        step.update({
            bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᑏ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1111l1l11_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑐ")]) if st[bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪᑑ")] == step[bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫᑒ")]), None)
        if index is not None:
            bstack1l1111l1l11_opy_[bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᑓ")][index] = step
        instance.data[TestFramework.bstack1l111ll1l1l_opy_] = bstack1l1111l1l11_opy_
    @staticmethod
    def __1l11l111lll_opy_(instance, args):
        bstack1l1l1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᑔ")
        bstack1l111lll1l1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1111l11l1_opy_ = args[1]
        bstack1l111111ll1_opy_ = id(bstack1l1111l11l1_opy_)
        bstack1l1111l1l11_opy_ = instance.data[TestFramework.bstack1l111ll1l1l_opy_]
        step = None
        if bstack1l111111ll1_opy_ is not None and bstack1l1111l1l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᑕ")):
            step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠬ࡯ࡤࠨᑖ")] == bstack1l111111ll1_opy_, bstack1l1111l1l11_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑗ")]), None)
            step.update({
                bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᑘ"): bstack1l111lll1l1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᑙ"): bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑚ"),
                bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᑛ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᑜ"): bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᑝ"),
                })
        index = next((i for i, st in enumerate(bstack1l1111l1l11_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᑞ")]) if st[bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪᑟ")] == step[bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫᑠ")]), None)
        if index is not None:
            bstack1l1111l1l11_opy_[bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᑡ")][index] = step
        instance.data[TestFramework.bstack1l111ll1l1l_opy_] = bstack1l1111l1l11_opy_
    @staticmethod
    def __1l111l11lll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑢ")):
                examples = list(node.callspec.params[bstack1l1l1l1_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᑣ")].values())
            return examples
        except:
            return []
    def bstack1l1lll1111l_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_]):
        bstack1l11l11l1l1_opy_ = (
            PytestBDDFramework.bstack1l111lll1ll_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1lll1lll111_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1ll1_opy_
        )
        hook = PytestBDDFramework.bstack1l111l11111_opy_(instance, bstack1l11l11l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11111ll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, []))
        return entries
    def bstack1l1lll11l11_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_]):
        bstack1l11l11l1l1_opy_ = (
            PytestBDDFramework.bstack1l111lll1ll_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1lll1lll111_opy_.PRE
            else PytestBDDFramework.bstack1l11l1l1ll1_opy_
        )
        PytestBDDFramework.bstack1l111l111l1_opy_(instance, bstack1l11l11l1l1_opy_)
        TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, []).clear()
    @staticmethod
    def bstack1l111l11111_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11l11l1l1_opy_: str):
        bstack1l1111l1ll1_opy_ = (
            PytestBDDFramework.bstack1l11111lll1_opy_
            if bstack1l11l11l1l1_opy_ == PytestBDDFramework.bstack1l11l1l1ll1_opy_
            else PytestBDDFramework.bstack1l11l11lll1_opy_
        )
        bstack1l111l1l1l1_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l11l11l1l1_opy_, None)
        bstack1l1111l1lll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l1111l1ll1_opy_, None) if bstack1l111l1l1l1_opy_ else None
        return (
            bstack1l1111l1lll_opy_[bstack1l111l1l1l1_opy_][-1]
            if isinstance(bstack1l1111l1lll_opy_, dict) and len(bstack1l1111l1lll_opy_.get(bstack1l111l1l1l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l111l1_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11l11l1l1_opy_: str):
        hook = PytestBDDFramework.bstack1l111l11111_opy_(instance, bstack1l11l11l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11111ll11_opy_, []).clear()
    @staticmethod
    def __1l111ll1l11_opy_(instance: bstack1lll1l1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᑤ"), None)):
            return
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᑥ"), bstack1l1l1l1_opy_ (u"ࠢ࠲ࠤᑦ")) != bstack1l1l1l1_opy_ (u"ࠣ࠳ࠥᑧ"):
            PytestBDDFramework.logger.warning(bstack1l1l1l1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᑨ"))
            return
        bstack1l111ll1ll1_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᑩ"): (PytestBDDFramework.bstack1l111lll1ll_opy_, PytestBDDFramework.bstack1l11l11lll1_opy_),
            bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᑪ"): (PytestBDDFramework.bstack1l11l1l1ll1_opy_, PytestBDDFramework.bstack1l11111lll1_opy_),
        }
        for when in (bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᑫ"), bstack1l1l1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᑬ"), bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᑭ")):
            bstack1l111ll11l1_opy_ = args[1].get_records(when)
            if not bstack1l111ll11l1_opy_:
                continue
            records = [
                bstack1lll111l1l1_opy_(
                    kind=TestFramework.bstack1l1ll111lll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1l1l1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᑮ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1l1l1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᑯ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll11l1_opy_
                if isinstance(getattr(r, bstack1l1l1l1_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᑰ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11111l1l1_opy_, bstack1l1111l1ll1_opy_ = bstack1l111ll1ll1_opy_.get(when, (None, None))
            bstack1l11l11llll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l11111l1l1_opy_, None) if bstack1l11111l1l1_opy_ else None
            bstack1l1111l1lll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l1111l1ll1_opy_, None) if bstack1l11l11llll_opy_ else None
            if isinstance(bstack1l1111l1lll_opy_, dict) and len(bstack1l1111l1lll_opy_.get(bstack1l11l11llll_opy_, [])) > 0:
                hook = bstack1l1111l1lll_opy_[bstack1l11l11llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11111ll11_opy_ in hook:
                    hook[TestFramework.bstack1l11111ll11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l111111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l1l11lll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l111lll111_opy_(request.node, scenario)
        bstack1l111l11l1l_opy_ = feature.filename
        if not bstack1l1l11lll1_opy_ or not test_name or not bstack1l111l11l1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l11lll1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l111l11_opy_: bstack1l1l11lll1_opy_,
            TestFramework.bstack1ll111llll1_opy_: test_name,
            TestFramework.bstack1l1l1lll1ll_opy_: bstack1l1l11lll1_opy_,
            TestFramework.bstack1l11l11l11l_opy_: bstack1l111l11l1l_opy_,
            TestFramework.bstack1l1111ll111_opy_: PytestBDDFramework.__1l11l1l1111_opy_(feature, scenario),
            TestFramework.bstack1l11l1l11ll_opy_: code,
            TestFramework.bstack1l1l111ll11_opy_: TestFramework.bstack1l11l11ll1l_opy_,
            TestFramework.bstack1l11ll1l1l1_opy_: test_name
        }
    @staticmethod
    def __1l111lll111_opy_(node, scenario):
        if hasattr(node, bstack1l1l1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᑱ")):
            parts = node.nodeid.rsplit(bstack1l1l1l1_opy_ (u"ࠧࡡࠢᑲ"))
            params = parts[-1]
            return bstack1l1l1l1_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᑳ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1l1111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1l1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬᑴ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1l1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᑵ")) else [])
    @staticmethod
    def __1l111llll11_opy_(location):
        return bstack1l1l1l1_opy_ (u"ࠤ࠽࠾ࠧᑶ").join(filter(lambda x: isinstance(x, str), location))