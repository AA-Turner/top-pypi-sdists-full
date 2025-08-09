# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1lllllll1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack11l1llll11_opy_ import bstack1l111l111l1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l111ll_opy_,
    bstack1lll1111l1l_opy_,
    bstack1lll1ll1l1l_opy_,
    bstack1l1111lllll_opy_,
    bstack1llll111l1l_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1llll1111_opy_
from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll1111ll1_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack111111l11l_opy_
bstack1l1llll1ll1_opy_ = bstack1l1llll1111_opy_()
bstack1l1ll111111_opy_ = bstack11l1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᐣ")
bstack1l111lll111_opy_ = bstack11l1_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᐤ")
bstack1l111llll11_opy_ = bstack11l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᐥ")
bstack1l111ll1ll1_opy_ = 1.0
_1l1l1ll1lll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l1111111l1_opy_ = bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᐦ")
    bstack1l111111lll_opy_ = bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᐧ")
    bstack1l111111l1l_opy_ = bstack11l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᐨ")
    bstack1l11l11l1l1_opy_ = bstack11l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᐩ")
    bstack1l111l1l11l_opy_ = bstack11l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᐪ")
    bstack1l11l111l11_opy_: bool
    bstack111111ll11_opy_: bstack111111l11l_opy_  = None
    bstack1l11l1111ll_opy_ = [
        bstack1lll1l111ll_opy_.BEFORE_ALL,
        bstack1lll1l111ll_opy_.AFTER_ALL,
        bstack1lll1l111ll_opy_.BEFORE_EACH,
        bstack1lll1l111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1111l111l_opy_: Dict[str, str],
        bstack1ll11l11ll1_opy_: List[str]=[bstack11l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᐫ")],
        bstack111111ll11_opy_: bstack111111l11l_opy_ = None,
        bstack1ll1llllll1_opy_=None
    ):
        super().__init__(bstack1ll11l11ll1_opy_, bstack1l1111l111l_opy_, bstack111111ll11_opy_)
        self.bstack1l11l111l11_opy_ = any(bstack11l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᐬ") in item.lower() for item in bstack1ll11l11ll1_opy_)
        self.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
    def track_event(
        self,
        context: bstack1l1111lllll_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1lll1ll1l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l111ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11l1111ll_opy_:
            bstack1l111l111l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l111ll_opy_.NONE:
            self.logger.warning(bstack11l1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᐭ") + str(test_hook_state) + bstack11l1_opy_ (u"ࠢࠣᐮ"))
            return
        if not self.bstack1l11l111l11_opy_:
            self.logger.warning(bstack11l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᐯ") + str(str(self.bstack1ll11l11ll1_opy_)) + bstack11l1_opy_ (u"ࠤࠥᐰ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᐱ") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧᐲ"))
            return
        instance = self.__1l111ll1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᐳ") + str(args) + bstack11l1_opy_ (u"ࠨࠢᐴ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l1111ll_opy_ and test_hook_state == bstack1lll1ll1l1l_opy_.PRE:
                bstack1ll111llll1_opy_ = bstack1ll1ll11111_opy_.bstack1ll11lll11l_opy_(EVENTS.bstack11111ll1l_opy_.value)
                name = str(EVENTS.bstack11111ll1l_opy_.name)+bstack11l1_opy_ (u"ࠢ࠻ࠤᐵ")+str(test_framework_state.name)
                TestFramework.bstack1l111l11l11_opy_(instance, name, bstack1ll111llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᐶ").format(e))
        try:
            if test_framework_state == bstack1lll1l111ll_opy_.TEST:
                if not TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l11l111l1l_opy_) and test_hook_state == bstack1lll1ll1l1l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111l1111l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l1_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᐷ") + str(test_hook_state) + bstack11l1_opy_ (u"ࠥࠦᐸ"))
                if test_hook_state == bstack1lll1ll1l1l_opy_.PRE and not TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l1llll1l11_opy_):
                    TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1llll1l11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l11l11l_opy_(instance, args)
                    self.logger.debug(bstack11l1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᐹ") + str(test_hook_state) + bstack11l1_opy_ (u"ࠧࠨᐺ"))
                elif test_hook_state == bstack1lll1ll1l1l_opy_.POST and not TestFramework.bstack1llll1llll1_opy_(instance, TestFramework.bstack1l1llll11l1_opy_):
                    TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1llll11l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᐻ") + str(test_hook_state) + bstack11l1_opy_ (u"ࠢࠣᐼ"))
            elif test_framework_state == bstack1lll1l111ll_opy_.STEP:
                if test_hook_state == bstack1lll1ll1l1l_opy_.PRE:
                    PytestBDDFramework.__1l1111111ll_opy_(instance, args)
                elif test_hook_state == bstack1lll1ll1l1l_opy_.POST:
                    PytestBDDFramework.__1l1111l1ll1_opy_(instance, args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG and test_hook_state == bstack1lll1ll1l1l_opy_.POST:
                PytestBDDFramework.__1l111l111ll_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG_REPORT and test_hook_state == bstack1lll1ll1l1l_opy_.POST:
                self.__1l111lll11l_opy_(instance, *args)
                self.__1l111l11111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11l1111ll_opy_:
                self.__1l1111ll11l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᐽ") + str(instance.ref()) + bstack11l1_opy_ (u"ࠤࠥᐾ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l1111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l1111ll_opy_ and test_hook_state == bstack1lll1ll1l1l_opy_.POST:
                name = str(EVENTS.bstack11111ll1l_opy_.name)+bstack11l1_opy_ (u"ࠥ࠾ࠧᐿ")+str(test_framework_state.name)
                bstack1ll111llll1_opy_ = TestFramework.bstack1l11111l11l_opy_(instance, name)
                bstack1ll1ll11111_opy_.end(EVENTS.bstack11111ll1l_opy_.value, bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᑀ"), bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᑁ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᑂ").format(e))
    def bstack1l1l1llllll_opy_(self):
        return self.bstack1l11l111l11_opy_
    def __1l1111ll1l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᑃ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1lll11ll1_opy_(rep, [bstack11l1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᑄ"), bstack11l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᑅ"), bstack11l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᑆ"), bstack11l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑇ"), bstack11l1_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᑈ"), bstack11l1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᑉ")])
        return None
    def __1l111lll11l_opy_(self, instance: bstack1lll1111l1l_opy_, *args):
        result = self.__1l1111ll1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l111l_opy_ = None
        if result.get(bstack11l1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑊ"), None) == bstack11l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᑋ") and len(args) > 1 and getattr(args[1], bstack11l1_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᑌ"), None) is not None:
            failure = [{bstack11l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᑍ"): [args[1].excinfo.exconly(), result.get(bstack11l1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᑎ"), None)]}]
            bstack11111l111l_opy_ = bstack11l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᑏ") if bstack11l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᑐ") in getattr(args[1].excinfo, bstack11l1_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᑑ"), bstack11l1_opy_ (u"ࠣࠤᑒ")) else bstack11l1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᑓ")
        bstack1l11l111111_opy_ = result.get(bstack11l1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑔ"), TestFramework.bstack1l111l1l1ll_opy_)
        if bstack1l11l111111_opy_ != TestFramework.bstack1l111l1l1ll_opy_:
            TestFramework.bstack1111111lll_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111llllll_opy_(instance, {
            TestFramework.bstack1l1l111111l_opy_: failure,
            TestFramework.bstack1l111ll11ll_opy_: bstack11111l111l_opy_,
            TestFramework.bstack1l1l111lll1_opy_: bstack1l11l111111_opy_,
        })
    def __1l111ll1111_opy_(
        self,
        context: bstack1l1111lllll_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1lll1ll1l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l111ll_opy_.SETUP_FIXTURE:
            instance = self.__1l111llll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11111lll1_opy_ bstack1l1111l1l1l_opy_ this to be bstack11l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑕ")
            if test_framework_state == bstack1lll1l111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lllllll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᑖ"), None), bstack11l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑗ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᑘ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑙ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll11111_opy_(target) if target else None
        return instance
    def __1l1111ll11l_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1lll1ll1l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11111l111_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l111111lll_opy_, {})
        if not key in bstack1l11111l111_opy_:
            bstack1l11111l111_opy_[key] = []
        bstack1l111l11l1l_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l111111l1l_opy_, {})
        if not key in bstack1l111l11l1l_opy_:
            bstack1l111l11l1l_opy_[key] = []
        bstack1l1111llll1_opy_ = {
            PytestBDDFramework.bstack1l111111lll_opy_: bstack1l11111l111_opy_,
            PytestBDDFramework.bstack1l111111l1l_opy_: bstack1l111l11l1l_opy_,
        }
        if test_hook_state == bstack1lll1ll1l1l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l1_opy_ (u"ࠤ࡮ࡩࡾࠨᑚ"): key,
                TestFramework.bstack1l111lllll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l111lll1l1_opy_: TestFramework.bstack1l111l1l1l1_opy_,
                TestFramework.bstack1l1111ll1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111l1llll_opy_: [],
                TestFramework.bstack1l11l11l111_opy_: hook_name,
                TestFramework.bstack1l111ll1lll_opy_: bstack1llll111111_opy_.bstack1l11111llll_opy_()
            }
            bstack1l11111l111_opy_[key].append(hook)
            bstack1l1111llll1_opy_[PytestBDDFramework.bstack1l11l11l1l1_opy_] = key
        elif test_hook_state == bstack1lll1ll1l1l_opy_.POST:
            bstack11llllll1ll_opy_ = bstack1l11111l111_opy_.get(key, [])
            hook = bstack11llllll1ll_opy_.pop() if bstack11llllll1ll_opy_ else None
            if hook:
                result = self.__1l1111ll1l1_opy_(*args)
                if result:
                    bstack1l11l111ll1_opy_ = result.get(bstack11l1_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑛ"), TestFramework.bstack1l111l1l1l1_opy_)
                    if bstack1l11l111ll1_opy_ != TestFramework.bstack1l111l1l1l1_opy_:
                        hook[TestFramework.bstack1l111lll1l1_opy_] = bstack1l11l111ll1_opy_
                hook[TestFramework.bstack1l11111l1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll1lll_opy_] = bstack1llll111111_opy_.bstack1l11111llll_opy_()
                self.bstack11lllllllll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l11111l_opy_, [])
                self.bstack1l1ll1l1111_opy_(instance, logs)
                bstack1l111l11l1l_opy_[key].append(hook)
                bstack1l1111llll1_opy_[PytestBDDFramework.bstack1l111l1l11l_opy_] = key
        TestFramework.bstack1l111llllll_opy_(instance, bstack1l1111llll1_opy_)
        self.logger.debug(bstack11l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᑜ") + str(bstack1l111l11l1l_opy_) + bstack11l1_opy_ (u"ࠧࠨᑝ"))
    def __1l111llll1l_opy_(
        self,
        context: bstack1l1111lllll_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1lll1ll1l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1lll11ll1_opy_(args[0], [bstack11l1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᑞ"), bstack11l1_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᑟ"), bstack11l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᑠ"), bstack11l1_opy_ (u"ࠤ࡬ࡨࡸࠨᑡ"), bstack11l1_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᑢ"), bstack11l1_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᑣ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᑤ")) else fixturedef.get(bstack11l1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᑥ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᑦ")) else None
        node = request.node if hasattr(request, bstack11l1_opy_ (u"ࠣࡰࡲࡨࡪࠨᑧ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑨ")) else None
        baseid = fixturedef.get(bstack11l1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᑩ"), None) or bstack11l1_opy_ (u"ࠦࠧᑪ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᑫ")):
            target = PytestBDDFramework.__1l111l1lll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᑬ")) else None
            if target and not TestFramework.bstack1lllll11111_opy_(target):
                self.__11lllllll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᑭ") + str(test_hook_state) + bstack11l1_opy_ (u"ࠣࠤᑮ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᑯ") + str(target) + bstack11l1_opy_ (u"ࠥࠦᑰ"))
            return None
        instance = TestFramework.bstack1lllll11111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᑱ") + str(target) + bstack11l1_opy_ (u"ࠧࠨᑲ"))
            return None
        bstack1l111111111_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, PytestBDDFramework.bstack1l1111111l1_opy_, {})
        if os.getenv(bstack11l1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᑳ"), bstack11l1_opy_ (u"ࠢ࠲ࠤᑴ")) == bstack11l1_opy_ (u"ࠣ࠳ࠥᑵ"):
            bstack1l1111ll111_opy_ = bstack11l1_opy_ (u"ࠤ࠽ࠦᑶ").join((scope, fixturename))
            bstack11llllllll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l11ll1_opy_ = {
                bstack11l1_opy_ (u"ࠥ࡯ࡪࡿࠢᑷ"): bstack1l1111ll111_opy_,
                bstack11l1_opy_ (u"ࠦࡹࡧࡧࡴࠤᑸ"): PytestBDDFramework.__1l111l1ll1l_opy_(request.node, scenario),
                bstack11l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᑹ"): fixturedef,
                bstack11l1_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᑺ"): scope,
                bstack11l1_opy_ (u"ࠢࡵࡻࡳࡩࠧᑻ"): None,
            }
            try:
                if test_hook_state == bstack1lll1ll1l1l_opy_.POST and callable(getattr(args[-1], bstack11l1_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᑼ"), None)):
                    bstack1l111l11ll1_opy_[bstack11l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᑽ")] = TestFramework.bstack1l1lll1111l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1ll1l1l_opy_.PRE:
                bstack1l111l11ll1_opy_[bstack11l1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᑾ")] = uuid4().__str__()
                bstack1l111l11ll1_opy_[PytestBDDFramework.bstack1l1111ll1ll_opy_] = bstack11llllllll1_opy_
            elif test_hook_state == bstack1lll1ll1l1l_opy_.POST:
                bstack1l111l11ll1_opy_[PytestBDDFramework.bstack1l11111l1ll_opy_] = bstack11llllllll1_opy_
            if bstack1l1111ll111_opy_ in bstack1l111111111_opy_:
                bstack1l111111111_opy_[bstack1l1111ll111_opy_].update(bstack1l111l11ll1_opy_)
                self.logger.debug(bstack11l1_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᑿ") + str(bstack1l111111111_opy_[bstack1l1111ll111_opy_]) + bstack11l1_opy_ (u"ࠧࠨᒀ"))
            else:
                bstack1l111111111_opy_[bstack1l1111ll111_opy_] = bstack1l111l11ll1_opy_
                self.logger.debug(bstack11l1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᒁ") + str(len(bstack1l111111111_opy_)) + bstack11l1_opy_ (u"ࠢࠣᒂ"))
        TestFramework.bstack1111111lll_opy_(instance, PytestBDDFramework.bstack1l1111111l1_opy_, bstack1l111111111_opy_)
        self.logger.debug(bstack11l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᒃ") + str(instance.ref()) + bstack11l1_opy_ (u"ࠤࠥᒄ"))
        return instance
    def __11lllllll11_opy_(
        self,
        context: bstack1l1111lllll_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllllll1l1_opy_.create_context(target)
        ob = bstack1lll1111l1l_opy_(ctx, self.bstack1ll11l11ll1_opy_, self.bstack1l1111l111l_opy_, test_framework_state)
        TestFramework.bstack1l111llllll_opy_(ob, {
            TestFramework.bstack1ll111lll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll1ll1l_opy_: context.test_framework_version,
            TestFramework.bstack1l111ll11l1_opy_: [],
            PytestBDDFramework.bstack1l1111111l1_opy_: {},
            PytestBDDFramework.bstack1l111111l1l_opy_: {},
            PytestBDDFramework.bstack1l111111lll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111lll_opy_(ob, TestFramework.bstack1l1111l11l1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111lll_opy_(ob, TestFramework.bstack1ll11l1ll1l_opy_, context.platform_index)
        TestFramework.bstack1lllll1llll_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᒅ") + str(TestFramework.bstack1lllll1llll_opy_.keys()) + bstack11l1_opy_ (u"ࠦࠧᒆ"))
        return ob
    @staticmethod
    def __1l11l11l11l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1_opy_ (u"ࠬ࡯ࡤࠨᒇ"): id(step),
                bstack11l1_opy_ (u"࠭ࡴࡦࡺࡷࠫᒈ"): step.name,
                bstack11l1_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᒉ"): step.keyword,
            })
        meta = {
            bstack11l1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᒊ"): {
                bstack11l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒋ"): feature.name,
                bstack11l1_opy_ (u"ࠪࡴࡦࡺࡨࠨᒌ"): feature.filename,
                bstack11l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᒍ"): feature.description
            },
            bstack11l1_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᒎ"): {
                bstack11l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒏ"): scenario.name
            },
            bstack11l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᒐ"): steps,
            bstack11l1_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᒑ"): PytestBDDFramework.__1l111ll1l1l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111l1l111_opy_: meta
            }
        )
    def bstack11lllllllll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᒒ")
        global _1l1l1ll1lll_opy_
        platform_index = os.environ[bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒓ")]
        bstack1l1llll1l1l_opy_ = os.path.join(bstack1l1llll1ll1_opy_, (bstack1l1ll111111_opy_ + str(platform_index)), bstack1l111lll111_opy_)
        if not os.path.exists(bstack1l1llll1l1l_opy_) or not os.path.isdir(bstack1l1llll1l1l_opy_):
            return
        logs = hook.get(bstack11l1_opy_ (u"ࠦࡱࡵࡧࡴࠤᒔ"), [])
        with os.scandir(bstack1l1llll1l1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1l1ll1lll_opy_:
                    self.logger.info(bstack11l1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒕ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1_opy_ (u"ࠨࠢᒖ")
                    log_entry = bstack1llll111l1l_opy_(
                        kind=bstack11l1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒗ"),
                        message=bstack11l1_opy_ (u"ࠣࠤᒘ"),
                        level=bstack11l1_opy_ (u"ࠤࠥᒙ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1lllll_opy_=entry.stat().st_size,
                        bstack1l1ll11lll1_opy_=bstack11l1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒚ"),
                        bstack1l111ll_opy_=os.path.abspath(entry.path),
                        bstack1l111l1ll11_opy_=hook.get(TestFramework.bstack1l111lllll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1l1ll1lll_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᒛ")]
        bstack1l111ll1l11_opy_ = os.path.join(bstack1l1llll1ll1_opy_, (bstack1l1ll111111_opy_ + str(platform_index)), bstack1l111lll111_opy_, bstack1l111llll11_opy_)
        if not os.path.exists(bstack1l111ll1l11_opy_) or not os.path.isdir(bstack1l111ll1l11_opy_):
            self.logger.info(bstack11l1_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᒜ").format(bstack1l111ll1l11_opy_))
        else:
            self.logger.info(bstack11l1_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᒝ").format(bstack1l111ll1l11_opy_))
            with os.scandir(bstack1l111ll1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1l1ll1lll_opy_:
                        self.logger.info(bstack11l1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒞ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1_opy_ (u"ࠣࠤᒟ")
                        log_entry = bstack1llll111l1l_opy_(
                            kind=bstack11l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒠ"),
                            message=bstack11l1_opy_ (u"ࠥࠦᒡ"),
                            level=bstack11l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᒢ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1lllll_opy_=entry.stat().st_size,
                            bstack1l1ll11lll1_opy_=bstack11l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒣ"),
                            bstack1l111ll_opy_=os.path.abspath(entry.path),
                            bstack1l1l1lll1ll_opy_=hook.get(TestFramework.bstack1l111lllll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1l1ll1lll_opy_.add(abs_path)
        hook[bstack11l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒤ")] = logs
    def bstack1l1ll1l1111_opy_(
        self,
        bstack1l1lll111l1_opy_: bstack1lll1111l1l_opy_,
        entries: List[bstack1llll111l1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᒥ"))
        req.platform_index = TestFramework.bstack1lllllllll1_opy_(bstack1l1lll111l1_opy_, TestFramework.bstack1ll11l1ll1l_opy_)
        req.execution_context.hash = str(bstack1l1lll111l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllllllll1_opy_(bstack1l1lll111l1_opy_, TestFramework.bstack1ll111lll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllllllll1_opy_(bstack1l1lll111l1_opy_, TestFramework.bstack1l1lll1ll1l_opy_)
            log_entry.uuid = entry.bstack1l111l1ll11_opy_ if entry.bstack1l111l1ll11_opy_ else TestFramework.bstack1lllllllll1_opy_(bstack1l1lll111l1_opy_, TestFramework.bstack1ll1l111l1l_opy_)
            log_entry.test_framework_state = bstack1l1lll111l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒦ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒧ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1lllll_opy_
                log_entry.file_path = entry.bstack1l111ll_opy_
        def bstack1l1ll1ll11l_opy_():
            bstack11ll111l1l_opy_ = datetime.now()
            try:
                self.bstack1ll1llllll1_opy_.LogCreatedEvent(req)
                bstack1l1lll111l1_opy_.bstack1ll11lll11_opy_(bstack11l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᒨ"), datetime.now() - bstack11ll111l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᒩ").format(str(e)))
                traceback.print_exc()
        self.bstack111111ll11_opy_.enqueue(bstack1l1ll1ll11l_opy_)
    def __1l111l11111_opy_(self, instance) -> None:
        bstack11l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᒪ")
        bstack1l1111llll1_opy_ = {bstack11l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᒫ"): bstack1llll111111_opy_.bstack1l11111llll_opy_()}
        TestFramework.bstack1l111llllll_opy_(instance, bstack1l1111llll1_opy_)
    @staticmethod
    def __1l1111111ll_opy_(instance, args):
        request, bstack1l1111lll11_opy_ = args
        bstack1l1111lll1l_opy_ = id(bstack1l1111lll11_opy_)
        bstack1l1111l1lll_opy_ = instance.data[TestFramework.bstack1l111l1l111_opy_]
        step = next(filter(lambda st: st[bstack11l1_opy_ (u"ࠧࡪࡦࠪᒬ")] == bstack1l1111lll1l_opy_, bstack1l1111l1lll_opy_[bstack11l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒭ")]), None)
        step.update({
            bstack11l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᒮ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1111l1lll_opy_[bstack11l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒯ")]) if st[bstack11l1_opy_ (u"ࠫ࡮ࡪࠧᒰ")] == step[bstack11l1_opy_ (u"ࠬ࡯ࡤࠨᒱ")]), None)
        if index is not None:
            bstack1l1111l1lll_opy_[bstack11l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒲ")][index] = step
        instance.data[TestFramework.bstack1l111l1l111_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def __1l1111l1ll1_opy_(instance, args):
        bstack11l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡮ࡥ࡯ࠢ࡯ࡩࡳࠦࡡࡳࡩࡶࠤ࡮ࡹࠠ࠳࠮ࠣ࡭ࡹࠦࡳࡪࡩࡱ࡭࡫࡯ࡥࡴࠢࡷ࡬ࡪࡸࡥࠡ࡫ࡶࠤࡳࡵࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠱ࠥࡡࡲࡦࡳࡸࡩࡸࡺࠬࠡࡵࡷࡩࡵࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠳ࠡࡶ࡫ࡩࡳࠦࡴࡩࡧࠣࡰࡦࡹࡴࠡࡸࡤࡰࡺ࡫ࠠࡪࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᒳ")
        bstack1l11111ll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1111lll11_opy_ = args[1]
        bstack1l1111lll1l_opy_ = id(bstack1l1111lll11_opy_)
        bstack1l1111l1lll_opy_ = instance.data[TestFramework.bstack1l111l1l111_opy_]
        step = None
        if bstack1l1111lll1l_opy_ is not None and bstack1l1111l1lll_opy_.get(bstack11l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒴ")):
            step = next(filter(lambda st: st[bstack11l1_opy_ (u"ࠩ࡬ࡨࠬᒵ")] == bstack1l1111lll1l_opy_, bstack1l1111l1lll_opy_[bstack11l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒶ")]), None)
            step.update({
                bstack11l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᒷ"): bstack1l11111ll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᒸ"): bstack11l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒹ"),
                bstack11l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᒺ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᒻ"): bstack11l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᒼ"),
                })
        index = next((i for i, st in enumerate(bstack1l1111l1lll_opy_[bstack11l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")]) if st[bstack11l1_opy_ (u"ࠫ࡮ࡪࠧᒾ")] == step[bstack11l1_opy_ (u"ࠬ࡯ࡤࠨᒿ")]), None)
        if index is not None:
            bstack1l1111l1lll_opy_[bstack11l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓀ")][index] = step
        instance.data[TestFramework.bstack1l111l1l111_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def __1l111ll1l1l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᓁ")):
                examples = list(node.callspec.params[bstack11l1_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᓂ")].values())
            return examples
        except:
            return []
    def bstack1l1ll11l1ll_opy_(self, instance: bstack1lll1111l1l_opy_, bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_]):
        bstack1l1111l1l11_opy_ = (
            PytestBDDFramework.bstack1l11l11l1l1_opy_
            if bstack1lllllll11l_opy_[1] == bstack1lll1ll1l1l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        hook = PytestBDDFramework.bstack1l111111l11_opy_(instance, bstack1l1111l1l11_opy_)
        entries = hook.get(TestFramework.bstack1l111l1llll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l111ll11l1_opy_, []))
        return entries
    def bstack1l1ll11111l_opy_(self, instance: bstack1lll1111l1l_opy_, bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_]):
        bstack1l1111l1l11_opy_ = (
            PytestBDDFramework.bstack1l11l11l1l1_opy_
            if bstack1lllllll11l_opy_[1] == bstack1lll1ll1l1l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        PytestBDDFramework.bstack1l11111111l_opy_(instance, bstack1l1111l1l11_opy_)
        TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l111ll11l1_opy_, []).clear()
    @staticmethod
    def bstack1l111111l11_opy_(instance: bstack1lll1111l1l_opy_, bstack1l1111l1l11_opy_: str):
        bstack1l111ll111l_opy_ = (
            PytestBDDFramework.bstack1l111111l1l_opy_
            if bstack1l1111l1l11_opy_ == PytestBDDFramework.bstack1l111l1l11l_opy_
            else PytestBDDFramework.bstack1l111111lll_opy_
        )
        bstack1l1111l11ll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l1111l1l11_opy_, None)
        bstack1l111l11lll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l111ll111l_opy_, None) if bstack1l1111l11ll_opy_ else None
        return (
            bstack1l111l11lll_opy_[bstack1l1111l11ll_opy_][-1]
            if isinstance(bstack1l111l11lll_opy_, dict) and len(bstack1l111l11lll_opy_.get(bstack1l1111l11ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11111111l_opy_(instance: bstack1lll1111l1l_opy_, bstack1l1111l1l11_opy_: str):
        hook = PytestBDDFramework.bstack1l111111l11_opy_(instance, bstack1l1111l1l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111l1llll_opy_, []).clear()
    @staticmethod
    def __1l111l111ll_opy_(instance: bstack1lll1111l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᓃ"), None)):
            return
        if os.getenv(bstack11l1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᓄ"), bstack11l1_opy_ (u"ࠦ࠶ࠨᓅ")) != bstack11l1_opy_ (u"ࠧ࠷ࠢᓆ"):
            PytestBDDFramework.logger.warning(bstack11l1_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᓇ"))
            return
        bstack11llllll1l1_opy_ = {
            bstack11l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᓈ"): (PytestBDDFramework.bstack1l11l11l1l1_opy_, PytestBDDFramework.bstack1l111111lll_opy_),
            bstack11l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᓉ"): (PytestBDDFramework.bstack1l111l1l11l_opy_, PytestBDDFramework.bstack1l111111l1l_opy_),
        }
        for when in (bstack11l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᓊ"), bstack11l1_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᓋ"), bstack11l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᓌ")):
            bstack1l111lll1ll_opy_ = args[1].get_records(when)
            if not bstack1l111lll1ll_opy_:
                continue
            records = [
                bstack1llll111l1l_opy_(
                    kind=TestFramework.bstack1l1ll111l11_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᓍ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᓎ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111lll1ll_opy_
                if isinstance(getattr(r, bstack11l1_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᓏ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l1111l1111_opy_, bstack1l111ll111l_opy_ = bstack11llllll1l1_opy_.get(when, (None, None))
            bstack1l11111l1l1_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l1111l1111_opy_, None) if bstack1l1111l1111_opy_ else None
            bstack1l111l11lll_opy_ = TestFramework.bstack1lllllllll1_opy_(instance, bstack1l111ll111l_opy_, None) if bstack1l11111l1l1_opy_ else None
            if isinstance(bstack1l111l11lll_opy_, dict) and len(bstack1l111l11lll_opy_.get(bstack1l11111l1l1_opy_, [])) > 0:
                hook = bstack1l111l11lll_opy_[bstack1l11111l1l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111l1llll_opy_ in hook:
                    hook[TestFramework.bstack1l111l1llll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l111ll11l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111l1111l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l111lll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l111lll_opy_(request.node, scenario)
        bstack11lllllll1l_opy_ = feature.filename
        if not bstack1l111lll1_opy_ or not test_name or not bstack11lllllll1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l111l1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l111l1l_opy_: bstack1l111lll1_opy_,
            TestFramework.bstack1ll11lll1ll_opy_: test_name,
            TestFramework.bstack1l1l1l1ll11_opy_: bstack1l111lll1_opy_,
            TestFramework.bstack11llllll11l_opy_: bstack11lllllll1l_opy_,
            TestFramework.bstack1l11111ll11_opy_: PytestBDDFramework.__1l111l1ll1l_opy_(feature, scenario),
            TestFramework.bstack1l111111ll1_opy_: code,
            TestFramework.bstack1l1l111lll1_opy_: TestFramework.bstack1l111l1l1ll_opy_,
            TestFramework.bstack1l11l1l1l1l_opy_: test_name
        }
    @staticmethod
    def __1l11l111lll_opy_(node, scenario):
        if hasattr(node, bstack11l1_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᓐ")):
            parts = node.nodeid.rsplit(bstack11l1_opy_ (u"ࠤ࡞ࠦᓑ"))
            params = parts[-1]
            return bstack11l1_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᓒ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111l1ll1l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᓓ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l1_opy_ (u"ࠬࡺࡡࡨࡵࠪᓔ")) else [])
    @staticmethod
    def __1l111l1lll1_opy_(location):
        return bstack11l1_opy_ (u"ࠨ࠺࠻ࠤᓕ").join(filter(lambda x: isinstance(x, str), location))