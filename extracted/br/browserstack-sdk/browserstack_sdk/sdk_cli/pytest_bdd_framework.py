# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1111111l1l_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1ll_opy_ import bstack1l111l111l1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1lll111l_opy_,
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111111l_opy_,
    bstack11lllll1lll_opy_,
    bstack1ll1ll111ll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1ll1lll11_opy_
from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11l1_opy_ import bstack1ll1lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack111111l111_opy_ import bstack1111111lll_opy_
bstack1l1ll1l1l11_opy_ = bstack1l1ll1lll11_opy_()
bstack1l1lll1l1l1_opy_ = bstack1111lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᐩ")
bstack1l111ll111l_opy_ = bstack1111lll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᐪ")
bstack11llllll111_opy_ = bstack1111lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᐫ")
bstack1l111l1111l_opy_ = 1.0
_1l1ll111ll1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11111ll11_opy_ = bstack1111lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᐬ")
    bstack1l11111l1l1_opy_ = bstack1111lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᐭ")
    bstack1l1111l11l1_opy_ = bstack1111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᐮ")
    bstack1l1111l1l11_opy_ = bstack1111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᐯ")
    bstack1l111llllll_opy_ = bstack1111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᐰ")
    bstack1l111ll11ll_opy_: bool
    bstack111111l111_opy_: bstack1111111lll_opy_  = None
    bstack1l111ll1111_opy_ = [
        bstack1ll1lll111l_opy_.BEFORE_ALL,
        bstack1ll1lll111l_opy_.AFTER_ALL,
        bstack1ll1lll111l_opy_.BEFORE_EACH,
        bstack1ll1lll111l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l111111_opy_: Dict[str, str],
        bstack1ll11l111ll_opy_: List[str]=[bstack1111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᐱ")],
        bstack111111l111_opy_: bstack1111111lll_opy_ = None,
        bstack1lll1llll11_opy_=None
    ):
        super().__init__(bstack1ll11l111ll_opy_, bstack1l11l111111_opy_, bstack111111l111_opy_)
        self.bstack1l111ll11ll_opy_ = any(bstack1111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᐲ") in item.lower() for item in bstack1ll11l111ll_opy_)
        self.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
    def track_event(
        self,
        context: bstack11lllll1lll_opy_,
        test_framework_state: bstack1ll1lll111l_opy_,
        test_hook_state: bstack1lll111111l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1lll111l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111ll1111_opy_:
            bstack1l111l111l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1lll111l_opy_.NONE:
            self.logger.warning(bstack1111lll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᐳ") + str(test_hook_state) + bstack1111lll_opy_ (u"ࠨࠢᐴ"))
            return
        if not self.bstack1l111ll11ll_opy_:
            self.logger.warning(bstack1111lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᐵ") + str(str(self.bstack1ll11l111ll_opy_)) + bstack1111lll_opy_ (u"ࠣࠤᐶ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1111lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᐷ") + str(kwargs) + bstack1111lll_opy_ (u"ࠥࠦᐸ"))
            return
        instance = self.__11lllllll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᐹ") + str(args) + bstack1111lll_opy_ (u"ࠧࠨᐺ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111ll1111_opy_ and test_hook_state == bstack1lll111111l_opy_.PRE:
                bstack1ll11l1l11l_opy_ = bstack1ll1llll11l_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1ll11l1ll_opy_.value)
                name = str(EVENTS.bstack1ll11l1ll_opy_.name)+bstack1111lll_opy_ (u"ࠨ࠺ࠣᐻ")+str(test_framework_state.name)
                TestFramework.bstack1l11111111l_opy_(instance, name, bstack1ll11l1l11l_opy_)
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᐼ").format(e))
        try:
            if test_framework_state == bstack1ll1lll111l_opy_.TEST:
                if not TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l111llll11_opy_) and test_hook_state == bstack1lll111111l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111ll1l1l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1111lll_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᐽ") + str(test_hook_state) + bstack1111lll_opy_ (u"ࠤࠥᐾ"))
                if test_hook_state == bstack1lll111111l_opy_.PRE and not TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_):
                    TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l111l1l11l_opy_(instance, args)
                    self.logger.debug(bstack1111lll_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᐿ") + str(test_hook_state) + bstack1111lll_opy_ (u"ࠦࠧᑀ"))
                elif test_hook_state == bstack1lll111111l_opy_.POST and not TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_):
                    TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1111lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᑁ") + str(test_hook_state) + bstack1111lll_opy_ (u"ࠨࠢᑂ"))
            elif test_framework_state == bstack1ll1lll111l_opy_.STEP:
                if test_hook_state == bstack1lll111111l_opy_.PRE:
                    PytestBDDFramework.__1l1111l1lll_opy_(instance, args)
                elif test_hook_state == bstack1lll111111l_opy_.POST:
                    PytestBDDFramework.__1l111l11111_opy_(instance, args)
            elif test_framework_state == bstack1ll1lll111l_opy_.LOG and test_hook_state == bstack1lll111111l_opy_.POST:
                PytestBDDFramework.__1l1111ll1ll_opy_(instance, *args)
            elif test_framework_state == bstack1ll1lll111l_opy_.LOG_REPORT and test_hook_state == bstack1lll111111l_opy_.POST:
                self.__1l1111lll11_opy_(instance, *args)
                self.__1l11l11l111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111ll1111_opy_:
                self.__11llllllll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1111lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᑃ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠣࠤᑄ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111lll111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111ll1111_opy_ and test_hook_state == bstack1lll111111l_opy_.POST:
                name = str(EVENTS.bstack1ll11l1ll_opy_.name)+bstack1111lll_opy_ (u"ࠤ࠽ࠦᑅ")+str(test_framework_state.name)
                bstack1ll11l1l11l_opy_ = TestFramework.bstack1l111l1ll11_opy_(instance, name)
                bstack1ll1llll11l_opy_.end(EVENTS.bstack1ll11l1ll_opy_.value, bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᑆ"), bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᑇ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᑈ").format(e))
    def bstack1l1llll1111_opy_(self):
        return self.bstack1l111ll11ll_opy_
    def __1l11l111l1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1111lll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᑉ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll11ll11_opy_(rep, [bstack1111lll_opy_ (u"ࠢࡸࡪࡨࡲࠧᑊ"), bstack1111lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑋ"), bstack1111lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᑌ"), bstack1111lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᑍ"), bstack1111lll_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᑎ"), bstack1111lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᑏ")])
        return None
    def __1l1111lll11_opy_(self, instance: bstack1ll1ll1l1l1_opy_, *args):
        result = self.__1l11l111l1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111ll1l_opy_ = None
        if result.get(bstack1111lll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑐ"), None) == bstack1111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᑑ") and len(args) > 1 and getattr(args[1], bstack1111lll_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᑒ"), None) is not None:
            failure = [{bstack1111lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᑓ"): [args[1].excinfo.exconly(), result.get(bstack1111lll_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᑔ"), None)]}]
            bstack111111ll1l_opy_ = bstack1111lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᑕ") if bstack1111lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᑖ") in getattr(args[1].excinfo, bstack1111lll_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᑗ"), bstack1111lll_opy_ (u"ࠢࠣᑘ")) else bstack1111lll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᑙ")
        bstack1l11l111lll_opy_ = result.get(bstack1111lll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑚ"), TestFramework.bstack11llllll1ll_opy_)
        if bstack1l11l111lll_opy_ != TestFramework.bstack11llllll1ll_opy_:
            TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111111l11_opy_(instance, {
            TestFramework.bstack1l1l111l111_opy_: failure,
            TestFramework.bstack1l11l111l11_opy_: bstack111111ll1l_opy_,
            TestFramework.bstack1l1l111ll11_opy_: bstack1l11l111lll_opy_,
        })
    def __11lllllll11_opy_(
        self,
        context: bstack11lllll1lll_opy_,
        test_framework_state: bstack1ll1lll111l_opy_,
        test_hook_state: bstack1lll111111l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1lll111l_opy_.SETUP_FIXTURE:
            instance = self.__1l111111ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l11l1l_opy_ bstack1l1111l1l1l_opy_ this to be bstack1111lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑛ")
            if test_framework_state == bstack1ll1lll111l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l1111l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1lll111l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1111lll_opy_ (u"ࠦࡳࡵࡤࡦࠤᑜ"), None), bstack1111lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑝ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1111lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑞ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1111lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑟ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll1111l_opy_(target) if target else None
        return instance
    def __11llllllll1_opy_(
        self,
        instance: bstack1ll1ll1l1l1_opy_,
        test_framework_state: bstack1ll1lll111l_opy_,
        test_hook_state: bstack1lll111111l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l111ll1_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, PytestBDDFramework.bstack1l11111l1l1_opy_, {})
        if not key in bstack1l11l111ll1_opy_:
            bstack1l11l111ll1_opy_[key] = []
        bstack1l111l1lll1_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, PytestBDDFramework.bstack1l1111l11l1_opy_, {})
        if not key in bstack1l111l1lll1_opy_:
            bstack1l111l1lll1_opy_[key] = []
        bstack1l111l1ll1l_opy_ = {
            PytestBDDFramework.bstack1l11111l1l1_opy_: bstack1l11l111ll1_opy_,
            PytestBDDFramework.bstack1l1111l11l1_opy_: bstack1l111l1lll1_opy_,
        }
        if test_hook_state == bstack1lll111111l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1111lll_opy_ (u"ࠣ࡭ࡨࡽࠧᑠ"): key,
                TestFramework.bstack11llllll11l_opy_: uuid4().__str__(),
                TestFramework.bstack1l111lllll1_opy_: TestFramework.bstack1l11111lll1_opy_,
                TestFramework.bstack1l1111l1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111111l1_opy_: [],
                TestFramework.bstack1l111111lll_opy_: hook_name,
                TestFramework.bstack1l1111l1111_opy_: bstack1ll1lll1l11_opy_.bstack1l111l1l1l1_opy_()
            }
            bstack1l11l111ll1_opy_[key].append(hook)
            bstack1l111l1ll1l_opy_[PytestBDDFramework.bstack1l1111l1l11_opy_] = key
        elif test_hook_state == bstack1lll111111l_opy_.POST:
            bstack1l1111111ll_opy_ = bstack1l11l111ll1_opy_.get(key, [])
            hook = bstack1l1111111ll_opy_.pop() if bstack1l1111111ll_opy_ else None
            if hook:
                result = self.__1l11l111l1l_opy_(*args)
                if result:
                    bstack1l111l1l111_opy_ = result.get(bstack1111lll_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑡ"), TestFramework.bstack1l11111lll1_opy_)
                    if bstack1l111l1l111_opy_ != TestFramework.bstack1l11111lll1_opy_:
                        hook[TestFramework.bstack1l111lllll1_opy_] = bstack1l111l1l111_opy_
                hook[TestFramework.bstack1l1111ll111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l1111l1111_opy_] = bstack1ll1lll1l11_opy_.bstack1l111l1l1l1_opy_()
                self.bstack11lllllll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11111llll_opy_, [])
                self.bstack1l1ll1llll1_opy_(instance, logs)
                bstack1l111l1lll1_opy_[key].append(hook)
                bstack1l111l1ll1l_opy_[PytestBDDFramework.bstack1l111llllll_opy_] = key
        TestFramework.bstack1l111111l11_opy_(instance, bstack1l111l1ll1l_opy_)
        self.logger.debug(bstack1111lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᑢ") + str(bstack1l111l1lll1_opy_) + bstack1111lll_opy_ (u"ࠦࠧᑣ"))
    def __1l111111ll1_opy_(
        self,
        context: bstack11lllll1lll_opy_,
        test_framework_state: bstack1ll1lll111l_opy_,
        test_hook_state: bstack1lll111111l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll11ll11_opy_(args[0], [bstack1111lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᑤ"), bstack1111lll_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᑥ"), bstack1111lll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᑦ"), bstack1111lll_opy_ (u"ࠣ࡫ࡧࡷࠧᑧ"), bstack1111lll_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᑨ"), bstack1111lll_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᑩ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1111lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑪ")) else fixturedef.get(bstack1111lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᑫ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1111lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᑬ")) else None
        node = request.node if hasattr(request, bstack1111lll_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᑭ")) else None
        target = request.node.nodeid if hasattr(node, bstack1111lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑮ")) else None
        baseid = fixturedef.get(bstack1111lll_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᑯ"), None) or bstack1111lll_opy_ (u"ࠥࠦᑰ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1111lll_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᑱ")):
            target = PytestBDDFramework.__1l11111l1ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1111lll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᑲ")) else None
            if target and not TestFramework.bstack1lllll1111l_opy_(target):
                self.__1l11l1111l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1111lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᑳ") + str(test_hook_state) + bstack1111lll_opy_ (u"ࠢࠣᑴ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1111lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᑵ") + str(target) + bstack1111lll_opy_ (u"ࠤࠥᑶ"))
            return None
        instance = TestFramework.bstack1lllll1111l_opy_(target)
        if not instance:
            self.logger.warning(bstack1111lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᑷ") + str(target) + bstack1111lll_opy_ (u"ࠦࠧᑸ"))
            return None
        bstack1l1111lll1l_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, PytestBDDFramework.bstack1l11111ll11_opy_, {})
        if os.getenv(bstack1111lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᑹ"), bstack1111lll_opy_ (u"ࠨ࠱ࠣᑺ")) == bstack1111lll_opy_ (u"ࠢ࠲ࠤᑻ"):
            bstack1l111ll1lll_opy_ = bstack1111lll_opy_ (u"ࠣ࠼ࠥᑼ").join((scope, fixturename))
            bstack1l111lll11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111111l1l_opy_ = {
                bstack1111lll_opy_ (u"ࠤ࡮ࡩࡾࠨᑽ"): bstack1l111ll1lll_opy_,
                bstack1111lll_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᑾ"): PytestBDDFramework.__1l111llll1l_opy_(request.node, scenario),
                bstack1111lll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᑿ"): fixturedef,
                bstack1111lll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒀ"): scope,
                bstack1111lll_opy_ (u"ࠨࡴࡺࡲࡨࠦᒁ"): None,
            }
            try:
                if test_hook_state == bstack1lll111111l_opy_.POST and callable(getattr(args[-1], bstack1111lll_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᒂ"), None)):
                    bstack1l111111l1l_opy_[bstack1111lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᒃ")] = TestFramework.bstack1l1ll11lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111111l_opy_.PRE:
                bstack1l111111l1l_opy_[bstack1111lll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᒄ")] = uuid4().__str__()
                bstack1l111111l1l_opy_[PytestBDDFramework.bstack1l1111l1ll1_opy_] = bstack1l111lll11l_opy_
            elif test_hook_state == bstack1lll111111l_opy_.POST:
                bstack1l111111l1l_opy_[PytestBDDFramework.bstack1l1111ll111_opy_] = bstack1l111lll11l_opy_
            if bstack1l111ll1lll_opy_ in bstack1l1111lll1l_opy_:
                bstack1l1111lll1l_opy_[bstack1l111ll1lll_opy_].update(bstack1l111111l1l_opy_)
                self.logger.debug(bstack1111lll_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᒅ") + str(bstack1l1111lll1l_opy_[bstack1l111ll1lll_opy_]) + bstack1111lll_opy_ (u"ࠦࠧᒆ"))
            else:
                bstack1l1111lll1l_opy_[bstack1l111ll1lll_opy_] = bstack1l111111l1l_opy_
                self.logger.debug(bstack1111lll_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᒇ") + str(len(bstack1l1111lll1l_opy_)) + bstack1111lll_opy_ (u"ࠨࠢᒈ"))
        TestFramework.bstack1llllll1l1l_opy_(instance, PytestBDDFramework.bstack1l11111ll11_opy_, bstack1l1111lll1l_opy_)
        self.logger.debug(bstack1111lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᒉ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠣࠤᒊ"))
        return instance
    def __1l11l1111l1_opy_(
        self,
        context: bstack11lllll1lll_opy_,
        test_framework_state: bstack1ll1lll111l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllll1l111_opy_.create_context(target)
        ob = bstack1ll1ll1l1l1_opy_(ctx, self.bstack1ll11l111ll_opy_, self.bstack1l11l111111_opy_, test_framework_state)
        TestFramework.bstack1l111111l11_opy_(ob, {
            TestFramework.bstack1ll11l1l1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll1l111_opy_: context.test_framework_version,
            TestFramework.bstack1l11111l111_opy_: [],
            PytestBDDFramework.bstack1l11111ll11_opy_: {},
            PytestBDDFramework.bstack1l1111l11l1_opy_: {},
            PytestBDDFramework.bstack1l11111l1l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllll1l1l_opy_(ob, TestFramework.bstack1l11111l11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllll1l1l_opy_(ob, TestFramework.bstack1ll11l1ll11_opy_, context.platform_index)
        TestFramework.bstack1lllllll11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1111lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᒋ") + str(TestFramework.bstack1lllllll11l_opy_.keys()) + bstack1111lll_opy_ (u"ࠥࠦᒌ"))
        return ob
    @staticmethod
    def __1l111l1l11l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1111lll_opy_ (u"ࠫ࡮ࡪࠧᒍ"): id(step),
                bstack1111lll_opy_ (u"ࠬࡺࡥࡹࡶࠪᒎ"): step.name,
                bstack1111lll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᒏ"): step.keyword,
            })
        meta = {
            bstack1111lll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᒐ"): {
                bstack1111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᒑ"): feature.name,
                bstack1111lll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᒒ"): feature.filename,
                bstack1111lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᒓ"): feature.description
            },
            bstack1111lll_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᒔ"): {
                bstack1111lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᒕ"): scenario.name
            },
            bstack1111lll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒖ"): steps,
            bstack1111lll_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᒗ"): PytestBDDFramework.__1l111l11ll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l111ll_opy_: meta
            }
        )
    def bstack11lllllll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1111lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᒘ")
        global _1l1ll111ll1_opy_
        platform_index = os.environ[bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒙ")]
        bstack1l1ll1l11ll_opy_ = os.path.join(bstack1l1ll1l1l11_opy_, (bstack1l1lll1l1l1_opy_ + str(platform_index)), bstack1l111ll111l_opy_)
        if not os.path.exists(bstack1l1ll1l11ll_opy_) or not os.path.isdir(bstack1l1ll1l11ll_opy_):
            return
        logs = hook.get(bstack1111lll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᒚ"), [])
        with os.scandir(bstack1l1ll1l11ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll111ll1_opy_:
                    self.logger.info(bstack1111lll_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᒛ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1111lll_opy_ (u"ࠧࠨᒜ")
                    log_entry = bstack1ll1ll111ll_opy_(
                        kind=bstack1111lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᒝ"),
                        message=bstack1111lll_opy_ (u"ࠢࠣᒞ"),
                        level=bstack1111lll_opy_ (u"ࠣࠤᒟ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll111l11_opy_=entry.stat().st_size,
                        bstack1l1lll1ll11_opy_=bstack1111lll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᒠ"),
                        bstack1l1111_opy_=os.path.abspath(entry.path),
                        bstack1l11111ll1l_opy_=hook.get(TestFramework.bstack11llllll11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll111ll1_opy_.add(abs_path)
        platform_index = os.environ[bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒡ")]
        bstack1l1111llll1_opy_ = os.path.join(bstack1l1ll1l1l11_opy_, (bstack1l1lll1l1l1_opy_ + str(platform_index)), bstack1l111ll111l_opy_, bstack11llllll111_opy_)
        if not os.path.exists(bstack1l1111llll1_opy_) or not os.path.isdir(bstack1l1111llll1_opy_):
            self.logger.info(bstack1111lll_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᒢ").format(bstack1l1111llll1_opy_))
        else:
            self.logger.info(bstack1111lll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᒣ").format(bstack1l1111llll1_opy_))
            with os.scandir(bstack1l1111llll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll111ll1_opy_:
                        self.logger.info(bstack1111lll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᒤ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1111lll_opy_ (u"ࠢࠣᒥ")
                        log_entry = bstack1ll1ll111ll_opy_(
                            kind=bstack1111lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒦ"),
                            message=bstack1111lll_opy_ (u"ࠤࠥᒧ"),
                            level=bstack1111lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᒨ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll111l11_opy_=entry.stat().st_size,
                            bstack1l1lll1ll11_opy_=bstack1111lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᒩ"),
                            bstack1l1111_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1lllll_opy_=hook.get(TestFramework.bstack11llllll11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll111ll1_opy_.add(abs_path)
        hook[bstack1111lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᒪ")] = logs
    def bstack1l1ll1llll1_opy_(
        self,
        bstack1l1ll11l11l_opy_: bstack1ll1ll1l1l1_opy_,
        entries: List[bstack1ll1ll111ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᒫ"))
        req.platform_index = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1ll11l1ll11_opy_)
        req.execution_context.hash = str(bstack1l1ll11l11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1ll11l11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1ll11l11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1ll11l1l1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1l1lll1l111_opy_)
            log_entry.uuid = entry.bstack1l11111ll1l_opy_ if entry.bstack1l11111ll1l_opy_ else TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1ll111lllll_opy_)
            log_entry.test_framework_state = bstack1l1ll11l11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᒬ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒭ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll111l11_opy_
                log_entry.file_path = entry.bstack1l1111_opy_
        def bstack1l1ll11111l_opy_():
            bstack11l1l1ll1l_opy_ = datetime.now()
            try:
                self.bstack1lll1llll11_opy_.LogCreatedEvent(req)
                bstack1l1ll11l11l_opy_.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᒮ"), datetime.now() - bstack11l1l1ll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᒯ").format(str(e)))
                traceback.print_exc()
        self.bstack111111l111_opy_.enqueue(bstack1l1ll11111l_opy_)
    def __1l11l11l111_opy_(self, instance) -> None:
        bstack1111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒰ")
        bstack1l111l1ll1l_opy_ = {bstack1111lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᒱ"): bstack1ll1lll1l11_opy_.bstack1l111l1l1l1_opy_()}
        TestFramework.bstack1l111111l11_opy_(instance, bstack1l111l1ll1l_opy_)
    @staticmethod
    def __1l1111l1lll_opy_(instance, args):
        request, bstack11lllllllll_opy_ = args
        bstack1l111ll1l11_opy_ = id(bstack11lllllllll_opy_)
        bstack1l1111ll11l_opy_ = instance.data[TestFramework.bstack1l111l111ll_opy_]
        step = next(filter(lambda st: st[bstack1111lll_opy_ (u"࠭ࡩࡥࠩᒲ")] == bstack1l111ll1l11_opy_, bstack1l1111ll11l_opy_[bstack1111lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒳ")]), None)
        step.update({
            bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᒴ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1111ll11l_opy_[bstack1111lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒵ")]) if st[bstack1111lll_opy_ (u"ࠪ࡭ࡩ࠭ᒶ")] == step[bstack1111lll_opy_ (u"ࠫ࡮ࡪࠧᒷ")]), None)
        if index is not None:
            bstack1l1111ll11l_opy_[bstack1111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒸ")][index] = step
        instance.data[TestFramework.bstack1l111l111ll_opy_] = bstack1l1111ll11l_opy_
    @staticmethod
    def __1l111l11111_opy_(instance, args):
        bstack1111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡭࡫࡮ࠡ࡮ࡨࡲࠥࡧࡲࡨࡵࠣ࡭ࡸࠦ࠲࠭ࠢ࡬ࡸࠥࡹࡩࡨࡰ࡬ࡪ࡮࡫ࡳࠡࡶ࡫ࡩࡷ࡫ࠠࡪࡵࠣࡲࡴࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠰ࠤࡠࡸࡥࡲࡷࡨࡷࡹ࠲ࠠࡴࡶࡨࡴࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠹ࠠࡵࡪࡨࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡷࡣ࡯ࡹࡪࠦࡩࡴࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒹ")
        bstack1l111111111_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11lllllllll_opy_ = args[1]
        bstack1l111ll1l11_opy_ = id(bstack11lllllllll_opy_)
        bstack1l1111ll11l_opy_ = instance.data[TestFramework.bstack1l111l111ll_opy_]
        step = None
        if bstack1l111ll1l11_opy_ is not None and bstack1l1111ll11l_opy_.get(bstack1111lll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒺ")):
            step = next(filter(lambda st: st[bstack1111lll_opy_ (u"ࠨ࡫ࡧࠫᒻ")] == bstack1l111ll1l11_opy_, bstack1l1111ll11l_opy_[bstack1111lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᒼ")]), None)
            step.update({
                bstack1111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᒽ"): bstack1l111111111_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1111lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᒾ"): bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒿ"),
                bstack1111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᓀ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᓁ"): bstack1111lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᓂ"),
                })
        index = next((i for i, st in enumerate(bstack1l1111ll11l_opy_[bstack1111lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᓃ")]) if st[bstack1111lll_opy_ (u"ࠪ࡭ࡩ࠭ᓄ")] == step[bstack1111lll_opy_ (u"ࠫ࡮ࡪࠧᓅ")]), None)
        if index is not None:
            bstack1l1111ll11l_opy_[bstack1111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓆ")][index] = step
        instance.data[TestFramework.bstack1l111l111ll_opy_] = bstack1l1111ll11l_opy_
    @staticmethod
    def __1l111l11ll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1111lll_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᓇ")):
                examples = list(node.callspec.params[bstack1111lll_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᓈ")].values())
            return examples
        except:
            return []
    def bstack1l1l1lll1ll_opy_(self, instance: bstack1ll1ll1l1l1_opy_, bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_]):
        bstack1l1111lllll_opy_ = (
            PytestBDDFramework.bstack1l1111l1l11_opy_
            if bstack1llllll11ll_opy_[1] == bstack1lll111111l_opy_.PRE
            else PytestBDDFramework.bstack1l111llllll_opy_
        )
        hook = PytestBDDFramework.bstack1l111ll11l1_opy_(instance, bstack1l1111lllll_opy_)
        entries = hook.get(TestFramework.bstack1l1111111l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l11111l111_opy_, []))
        return entries
    def bstack1l1lll11lll_opy_(self, instance: bstack1ll1ll1l1l1_opy_, bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_]):
        bstack1l1111lllll_opy_ = (
            PytestBDDFramework.bstack1l1111l1l11_opy_
            if bstack1llllll11ll_opy_[1] == bstack1lll111111l_opy_.PRE
            else PytestBDDFramework.bstack1l111llllll_opy_
        )
        PytestBDDFramework.bstack1l111l11l11_opy_(instance, bstack1l1111lllll_opy_)
        TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l11111l111_opy_, []).clear()
    @staticmethod
    def bstack1l111ll11l1_opy_(instance: bstack1ll1ll1l1l1_opy_, bstack1l1111lllll_opy_: str):
        bstack1l111l1llll_opy_ = (
            PytestBDDFramework.bstack1l1111l11l1_opy_
            if bstack1l1111lllll_opy_ == PytestBDDFramework.bstack1l111llllll_opy_
            else PytestBDDFramework.bstack1l11111l1l1_opy_
        )
        bstack1l11l1111ll_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, bstack1l1111lllll_opy_, None)
        bstack1l11l11111l_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, bstack1l111l1llll_opy_, None) if bstack1l11l1111ll_opy_ else None
        return (
            bstack1l11l11111l_opy_[bstack1l11l1111ll_opy_][-1]
            if isinstance(bstack1l11l11111l_opy_, dict) and len(bstack1l11l11111l_opy_.get(bstack1l11l1111ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l11l11_opy_(instance: bstack1ll1ll1l1l1_opy_, bstack1l1111lllll_opy_: str):
        hook = PytestBDDFramework.bstack1l111ll11l1_opy_(instance, bstack1l1111lllll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111111l1_opy_, []).clear()
    @staticmethod
    def __1l1111ll1ll_opy_(instance: bstack1ll1ll1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1111lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᓉ"), None)):
            return
        if os.getenv(bstack1111lll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᓊ"), bstack1111lll_opy_ (u"ࠥ࠵ࠧᓋ")) != bstack1111lll_opy_ (u"ࠦ࠶ࠨᓌ"):
            PytestBDDFramework.logger.warning(bstack1111lll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᓍ"))
            return
        bstack11llllll1l1_opy_ = {
            bstack1111lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᓎ"): (PytestBDDFramework.bstack1l1111l1l11_opy_, PytestBDDFramework.bstack1l11111l1l1_opy_),
            bstack1111lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᓏ"): (PytestBDDFramework.bstack1l111llllll_opy_, PytestBDDFramework.bstack1l1111l11l1_opy_),
        }
        for when in (bstack1111lll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᓐ"), bstack1111lll_opy_ (u"ࠤࡦࡥࡱࡲࠢᓑ"), bstack1111lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᓒ")):
            bstack1l111lll1l1_opy_ = args[1].get_records(when)
            if not bstack1l111lll1l1_opy_:
                continue
            records = [
                bstack1ll1ll111ll_opy_(
                    kind=TestFramework.bstack1l1l1ll1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1111lll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᓓ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1111lll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᓔ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111lll1l1_opy_
                if isinstance(getattr(r, bstack1111lll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᓕ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111lll1ll_opy_, bstack1l111l1llll_opy_ = bstack11llllll1l1_opy_.get(when, (None, None))
            bstack1l111l11lll_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, bstack1l111lll1ll_opy_, None) if bstack1l111lll1ll_opy_ else None
            bstack1l11l11111l_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, bstack1l111l1llll_opy_, None) if bstack1l111l11lll_opy_ else None
            if isinstance(bstack1l11l11111l_opy_, dict) and len(bstack1l11l11111l_opy_.get(bstack1l111l11lll_opy_, [])) > 0:
                hook = bstack1l11l11111l_opy_[bstack1l111l11lll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111111l1_opy_ in hook:
                    hook[TestFramework.bstack1l1111111l1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l11111l111_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111ll1l1l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11l1l1l11_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1111l111l_opy_(request.node, scenario)
        bstack1l1111l11ll_opy_ = feature.filename
        if not bstack11l1l1l11_opy_ or not test_name or not bstack1l1111l11ll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll111lllll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111llll11_opy_: bstack11l1l1l11_opy_,
            TestFramework.bstack1ll1111llll_opy_: test_name,
            TestFramework.bstack1l1l1l1111l_opy_: bstack11l1l1l11_opy_,
            TestFramework.bstack1l111ll1ll1_opy_: bstack1l1111l11ll_opy_,
            TestFramework.bstack1l111l1l1ll_opy_: PytestBDDFramework.__1l111llll1l_opy_(feature, scenario),
            TestFramework.bstack1l1111ll1l1_opy_: code,
            TestFramework.bstack1l1l111ll11_opy_: TestFramework.bstack11llllll1ll_opy_,
            TestFramework.bstack1l11l1ll11l_opy_: test_name
        }
    @staticmethod
    def __1l1111l111l_opy_(node, scenario):
        if hasattr(node, bstack1111lll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᓖ")):
            parts = node.nodeid.rsplit(bstack1111lll_opy_ (u"ࠣ࡝ࠥᓗ"))
            params = parts[-1]
            return bstack1111lll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᓘ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111llll1l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1111lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᓙ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1111lll_opy_ (u"ࠫࡹࡧࡧࡴࠩᓚ")) else [])
    @staticmethod
    def __1l11111l1ll_opy_(location):
        return bstack1111lll_opy_ (u"ࠧࡀ࠺ࠣᓛ").join(filter(lambda x: isinstance(x, str), location))