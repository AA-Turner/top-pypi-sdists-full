# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llll1lll11_opy_ import bstack1lllllll1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1111lll1l_opy_ import bstack11llllll111_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1lll1lll_opy_,
    bstack1lll1lllll1_opy_,
    bstack1lll111llll_opy_,
    bstack1l111111l11_opy_,
    bstack1ll1lll1l11_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1lll11111_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll111l111_opy_
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import bstack111111l1l1_opy_
bstack1l1ll1ll111_opy_ = bstack1l1lll11111_opy_()
bstack1l1ll11l11l_opy_ = bstack111l111_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᐡ")
bstack1l111l1ll11_opy_ = bstack111l111_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᐢ")
bstack1l1111l11l1_opy_ = bstack111l111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᐣ")
bstack1l111lll11l_opy_ = 1.0
_1l1ll1l1111_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11111ll1l_opy_ = bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᐤ")
    bstack1l11l1111ll_opy_ = bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᐥ")
    bstack1l11l11111l_opy_ = bstack111l111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᐦ")
    bstack11lllllllll_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᐧ")
    bstack1l111lll111_opy_ = bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᐨ")
    bstack1l111ll1111_opy_: bool
    bstack1111111lll_opy_: bstack111111l1l1_opy_  = None
    bstack1l111ll1l1l_opy_ = [
        bstack1ll1lll1lll_opy_.BEFORE_ALL,
        bstack1ll1lll1lll_opy_.AFTER_ALL,
        bstack1ll1lll1lll_opy_.BEFORE_EACH,
        bstack1ll1lll1lll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111111ll1_opy_: Dict[str, str],
        bstack1ll11l11ll1_opy_: List[str]=[bstack111l111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᐩ")],
        bstack1111111lll_opy_: bstack111111l1l1_opy_ = None,
        bstack1lll1l11l1l_opy_=None
    ):
        super().__init__(bstack1ll11l11ll1_opy_, bstack1l111111ll1_opy_, bstack1111111lll_opy_)
        self.bstack1l111ll1111_opy_ = any(bstack111l111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᐪ") in item.lower() for item in bstack1ll11l11ll1_opy_)
        self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
    def track_event(
        self,
        context: bstack1l111111l11_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        test_hook_state: bstack1lll111llll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1lll1lll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111ll1l1l_opy_:
            bstack11llllll111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1lll1lll_opy_.NONE:
            self.logger.warning(bstack111l111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᐫ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠧࠨᐬ"))
            return
        if not self.bstack1l111ll1111_opy_:
            self.logger.warning(bstack111l111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᐭ") + str(str(self.bstack1ll11l11ll1_opy_)) + bstack111l111_opy_ (u"ࠢࠣᐮ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᐯ") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥᐰ"))
            return
        instance = self.__1l1111ll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᐱ") + str(args) + bstack111l111_opy_ (u"ࠦࠧᐲ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111ll1l1l_opy_ and test_hook_state == bstack1lll111llll_opy_.PRE:
                bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack11ll1l11l_opy_.value)
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack111l111_opy_ (u"ࠧࡀࠢᐳ")+str(test_framework_state.name)
                TestFramework.bstack1l111ll1lll_opy_(instance, name, bstack1ll11llll11_opy_)
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᐴ").format(e))
        try:
            if test_framework_state == bstack1ll1lll1lll_opy_.TEST:
                if not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l111l1111l_opy_) and test_hook_state == bstack1lll111llll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111l1llll_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack111l111_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᐵ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠣࠤᐶ"))
                if test_hook_state == bstack1lll111llll_opy_.PRE and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11111llll_opy_(instance, args)
                    self.logger.debug(bstack111l111_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᐷ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠥࠦᐸ"))
                elif test_hook_state == bstack1lll111llll_opy_.POST and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l111_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᐹ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠧࠨᐺ"))
            elif test_framework_state == bstack1ll1lll1lll_opy_.STEP:
                if test_hook_state == bstack1lll111llll_opy_.PRE:
                    PytestBDDFramework.__11lllll1ll1_opy_(instance, args)
                elif test_hook_state == bstack1lll111llll_opy_.POST:
                    PytestBDDFramework.__1l111llllll_opy_(instance, args)
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG and test_hook_state == bstack1lll111llll_opy_.POST:
                PytestBDDFramework.__1l111ll1ll1_opy_(instance, *args)
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG_REPORT and test_hook_state == bstack1lll111llll_opy_.POST:
                self.__1l1111lll1l_opy_(instance, *args)
                self.__1l111ll11l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111ll1l1l_opy_:
                self.__1l111l111ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᐻ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠢࠣᐼ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1111111ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111ll1l1l_opy_ and test_hook_state == bstack1lll111llll_opy_.POST:
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack111l111_opy_ (u"ࠣ࠼ࠥᐽ")+str(test_framework_state.name)
                bstack1ll11llll11_opy_ = TestFramework.bstack1l11l1111l1_opy_(instance, name)
                bstack1llll1111l1_opy_.end(EVENTS.bstack11ll1l11l_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᐾ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᐿ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᑀ").format(e))
    def bstack1l1lll1ll11_opy_(self):
        return self.bstack1l111ll1111_opy_
    def __1l11l111ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111l111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᑁ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll11l1l1_opy_(rep, [bstack111l111_opy_ (u"ࠨࡷࡩࡧࡱࠦᑂ"), bstack111l111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᑃ"), bstack111l111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᑄ"), bstack111l111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᑅ"), bstack111l111_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᑆ"), bstack111l111_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᑇ")])
        return None
    def __1l1111lll1l_opy_(self, instance: bstack1lll1lllll1_opy_, *args):
        result = self.__1l11l111ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111llll_opy_ = None
        if result.get(bstack111l111_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑈ"), None) == bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᑉ") and len(args) > 1 and getattr(args[1], bstack111l111_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᑊ"), None) is not None:
            failure = [{bstack111l111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᑋ"): [args[1].excinfo.exconly(), result.get(bstack111l111_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᑌ"), None)]}]
            bstack111111llll_opy_ = bstack111l111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᑍ") if bstack111l111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᑎ") in getattr(args[1].excinfo, bstack111l111_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᑏ"), bstack111l111_opy_ (u"ࠨࠢᑐ")) else bstack111l111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᑑ")
        bstack1l111l11l1l_opy_ = result.get(bstack111l111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑒ"), TestFramework.bstack1l111llll1l_opy_)
        if bstack1l111l11l1l_opy_ != TestFramework.bstack1l111llll1l_opy_:
            TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1ll11ll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111ll1l1_opy_(instance, {
            TestFramework.bstack1l11lllll11_opy_: failure,
            TestFramework.bstack1l11111l111_opy_: bstack111111llll_opy_,
            TestFramework.bstack1l1l1111111_opy_: bstack1l111l11l1l_opy_,
        })
    def __1l1111ll1ll_opy_(
        self,
        context: bstack1l111111l11_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        test_hook_state: bstack1lll111llll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1lll1lll_opy_.SETUP_FIXTURE:
            instance = self.__1l1111l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l1111l1ll1_opy_ bstack1l1111l1l1l_opy_ this to be bstack111l111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑓ")
            if test_framework_state == bstack1ll1lll1lll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lllllll1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack111l111_opy_ (u"ࠥࡲࡴࡪࡥࠣᑔ"), None), bstack111l111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑕ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111l111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᑖ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack111l111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑗ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll11l1l_opy_(target) if target else None
        return instance
    def __1l111l111ll_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        test_hook_state: bstack1lll111llll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1111ll111_opy_ = TestFramework.bstack1111111l1l_opy_(instance, PytestBDDFramework.bstack1l11l1111ll_opy_, {})
        if not key in bstack1l1111ll111_opy_:
            bstack1l1111ll111_opy_[key] = []
        bstack1l1111l111l_opy_ = TestFramework.bstack1111111l1l_opy_(instance, PytestBDDFramework.bstack1l11l11111l_opy_, {})
        if not key in bstack1l1111l111l_opy_:
            bstack1l1111l111l_opy_[key] = []
        bstack1l1111ll11l_opy_ = {
            PytestBDDFramework.bstack1l11l1111ll_opy_: bstack1l1111ll111_opy_,
            PytestBDDFramework.bstack1l11l11111l_opy_: bstack1l1111l111l_opy_,
        }
        if test_hook_state == bstack1lll111llll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack111l111_opy_ (u"ࠢ࡬ࡧࡼࠦᑘ"): key,
                TestFramework.bstack1l111111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11llllll11l_opy_: TestFramework.bstack1l111l1l1l1_opy_,
                TestFramework.bstack11lllllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11111l1l1_opy_: [],
                TestFramework.bstack1l1111l1111_opy_: hook_name,
                TestFramework.bstack1l111l11l11_opy_: bstack1lll111l111_opy_.bstack1l111ll111l_opy_()
            }
            bstack1l1111ll111_opy_[key].append(hook)
            bstack1l1111ll11l_opy_[PytestBDDFramework.bstack11lllllllll_opy_] = key
        elif test_hook_state == bstack1lll111llll_opy_.POST:
            bstack1l11111lll1_opy_ = bstack1l1111ll111_opy_.get(key, [])
            hook = bstack1l11111lll1_opy_.pop() if bstack1l11111lll1_opy_ else None
            if hook:
                result = self.__1l11l111ll1_opy_(*args)
                if result:
                    bstack1l11l111l11_opy_ = result.get(bstack111l111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑙ"), TestFramework.bstack1l111l1l1l1_opy_)
                    if bstack1l11l111l11_opy_ != TestFramework.bstack1l111l1l1l1_opy_:
                        hook[TestFramework.bstack11llllll11l_opy_] = bstack1l11l111l11_opy_
                hook[TestFramework.bstack1l11l111lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l11l11_opy_] = bstack1lll111l111_opy_.bstack1l111ll111l_opy_()
                self.bstack1l1111lll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1l1ll_opy_, [])
                self.bstack1l1l1ll1l11_opy_(instance, logs)
                bstack1l1111l111l_opy_[key].append(hook)
                bstack1l1111ll11l_opy_[PytestBDDFramework.bstack1l111lll111_opy_] = key
        TestFramework.bstack1l1111ll1l1_opy_(instance, bstack1l1111ll11l_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᑚ") + str(bstack1l1111l111l_opy_) + bstack111l111_opy_ (u"ࠥࠦᑛ"))
    def __1l1111l11ll_opy_(
        self,
        context: bstack1l111111l11_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        test_hook_state: bstack1lll111llll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll11l1l1_opy_(args[0], [bstack111l111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑜ"), bstack111l111_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᑝ"), bstack111l111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᑞ"), bstack111l111_opy_ (u"ࠢࡪࡦࡶࠦᑟ"), bstack111l111_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᑠ"), bstack111l111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᑡ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack111l111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᑢ")) else fixturedef.get(bstack111l111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑣ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111l111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᑤ")) else None
        node = request.node if hasattr(request, bstack111l111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑥ")) else None
        target = request.node.nodeid if hasattr(node, bstack111l111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑦ")) else None
        baseid = fixturedef.get(bstack111l111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᑧ"), None) or bstack111l111_opy_ (u"ࠤࠥᑨ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111l111_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᑩ")):
            target = PytestBDDFramework.__1l111l1ll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111l111_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᑪ")) else None
            if target and not TestFramework.bstack1lllll11l1l_opy_(target):
                self.__11lllllll1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111l111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑫ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠨࠢᑬ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111l111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᑭ") + str(target) + bstack111l111_opy_ (u"ࠣࠤᑮ"))
            return None
        instance = TestFramework.bstack1lllll11l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack111l111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᑯ") + str(target) + bstack111l111_opy_ (u"ࠥࠦᑰ"))
            return None
        bstack1l111ll11ll_opy_ = TestFramework.bstack1111111l1l_opy_(instance, PytestBDDFramework.bstack1l11111ll1l_opy_, {})
        if os.getenv(bstack111l111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᑱ"), bstack111l111_opy_ (u"ࠧ࠷ࠢᑲ")) == bstack111l111_opy_ (u"ࠨ࠱ࠣᑳ"):
            bstack1l111l11111_opy_ = bstack111l111_opy_ (u"ࠢ࠻ࠤᑴ").join((scope, fixturename))
            bstack1l111l111l1_opy_ = datetime.now(tz=timezone.utc)
            bstack11llllllll1_opy_ = {
                bstack111l111_opy_ (u"ࠣ࡭ࡨࡽࠧᑵ"): bstack1l111l11111_opy_,
                bstack111l111_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᑶ"): PytestBDDFramework.__1l111111l1l_opy_(request.node, scenario),
                bstack111l111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᑷ"): fixturedef,
                bstack111l111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᑸ"): scope,
                bstack111l111_opy_ (u"ࠧࡺࡹࡱࡧࠥᑹ"): None,
            }
            try:
                if test_hook_state == bstack1lll111llll_opy_.POST and callable(getattr(args[-1], bstack111l111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᑺ"), None)):
                    bstack11llllllll1_opy_[bstack111l111_opy_ (u"ࠢࡵࡻࡳࡩࠧᑻ")] = TestFramework.bstack1l1lll1l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111llll_opy_.PRE:
                bstack11llllllll1_opy_[bstack111l111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᑼ")] = uuid4().__str__()
                bstack11llllllll1_opy_[PytestBDDFramework.bstack11lllllll11_opy_] = bstack1l111l111l1_opy_
            elif test_hook_state == bstack1lll111llll_opy_.POST:
                bstack11llllllll1_opy_[PytestBDDFramework.bstack1l11l111lll_opy_] = bstack1l111l111l1_opy_
            if bstack1l111l11111_opy_ in bstack1l111ll11ll_opy_:
                bstack1l111ll11ll_opy_[bstack1l111l11111_opy_].update(bstack11llllllll1_opy_)
                self.logger.debug(bstack111l111_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᑽ") + str(bstack1l111ll11ll_opy_[bstack1l111l11111_opy_]) + bstack111l111_opy_ (u"ࠥࠦᑾ"))
            else:
                bstack1l111ll11ll_opy_[bstack1l111l11111_opy_] = bstack11llllllll1_opy_
                self.logger.debug(bstack111l111_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᑿ") + str(len(bstack1l111ll11ll_opy_)) + bstack111l111_opy_ (u"ࠧࠨᒀ"))
        TestFramework.bstack1111111111_opy_(instance, PytestBDDFramework.bstack1l11111ll1l_opy_, bstack1l111ll11ll_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᒁ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠢࠣᒂ"))
        return instance
    def __11lllllll1l_opy_(
        self,
        context: bstack1l111111l11_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllllll1ll_opy_.create_context(target)
        ob = bstack1lll1lllll1_opy_(ctx, self.bstack1ll11l11ll1_opy_, self.bstack1l111111ll1_opy_, test_framework_state)
        TestFramework.bstack1l1111ll1l1_opy_(ob, {
            TestFramework.bstack1ll111ll1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1ll1ll1_opy_: context.test_framework_version,
            TestFramework.bstack1l1111lllll_opy_: [],
            PytestBDDFramework.bstack1l11111ll1l_opy_: {},
            PytestBDDFramework.bstack1l11l11111l_opy_: {},
            PytestBDDFramework.bstack1l11l1111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1l11111111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1ll11l1lll1_opy_, context.platform_index)
        TestFramework.bstack1lllll1llll_opy_[ctx.id] = ob
        self.logger.debug(bstack111l111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᒃ") + str(TestFramework.bstack1lllll1llll_opy_.keys()) + bstack111l111_opy_ (u"ࠤࠥᒄ"))
        return ob
    @staticmethod
    def __1l11111llll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭ᒅ"): id(step),
                bstack111l111_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᒆ"): step.name,
                bstack111l111_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ᒇ"): step.keyword,
            })
        meta = {
            bstack111l111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᒈ"): {
                bstack111l111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒉ"): feature.name,
                bstack111l111_opy_ (u"ࠨࡲࡤࡸ࡭࠭ᒊ"): feature.filename,
                bstack111l111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᒋ"): feature.description
            },
            bstack111l111_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᒌ"): {
                bstack111l111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒍ"): scenario.name
            },
            bstack111l111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒎ"): steps,
            bstack111l111_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᒏ"): PytestBDDFramework.__1l1111llll1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11111l11l_opy_: meta
            }
        )
    def bstack1l1111lll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᒐ")
        global _1l1ll1l1111_opy_
        platform_index = os.environ[bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᒑ")]
        bstack1l1ll111ll1_opy_ = os.path.join(bstack1l1ll1ll111_opy_, (bstack1l1ll11l11l_opy_ + str(platform_index)), bstack1l111l1ll11_opy_)
        if not os.path.exists(bstack1l1ll111ll1_opy_) or not os.path.isdir(bstack1l1ll111ll1_opy_):
            return
        logs = hook.get(bstack111l111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᒒ"), [])
        with os.scandir(bstack1l1ll111ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l1111_opy_:
                    self.logger.info(bstack111l111_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᒓ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l111_opy_ (u"ࠦࠧᒔ")
                    log_entry = bstack1ll1lll1l11_opy_(
                        kind=bstack111l111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒕ"),
                        message=bstack111l111_opy_ (u"ࠨࠢᒖ"),
                        level=bstack111l111_opy_ (u"ࠢࠣᒗ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll111lll_opy_=entry.stat().st_size,
                        bstack1l1ll1l1lll_opy_=bstack111l111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᒘ"),
                        bstack11l111_opy_=os.path.abspath(entry.path),
                        bstack1l11l111111_opy_=hook.get(TestFramework.bstack1l111111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l1111_opy_.add(abs_path)
        platform_index = os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒙ")]
        bstack1l111l1l11l_opy_ = os.path.join(bstack1l1ll1ll111_opy_, (bstack1l1ll11l11l_opy_ + str(platform_index)), bstack1l111l1ll11_opy_, bstack1l1111l11l1_opy_)
        if not os.path.exists(bstack1l111l1l11l_opy_) or not os.path.isdir(bstack1l111l1l11l_opy_):
            self.logger.info(bstack111l111_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᒚ").format(bstack1l111l1l11l_opy_))
        else:
            self.logger.info(bstack111l111_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᒛ").format(bstack1l111l1l11l_opy_))
            with os.scandir(bstack1l111l1l11l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l1111_opy_:
                        self.logger.info(bstack111l111_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒜ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l111_opy_ (u"ࠨࠢᒝ")
                        log_entry = bstack1ll1lll1l11_opy_(
                            kind=bstack111l111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒞ"),
                            message=bstack111l111_opy_ (u"ࠣࠤᒟ"),
                            level=bstack111l111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᒠ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll111lll_opy_=entry.stat().st_size,
                            bstack1l1ll1l1lll_opy_=bstack111l111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒡ"),
                            bstack11l111_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1l11ll_opy_=hook.get(TestFramework.bstack1l111111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l1111_opy_.add(abs_path)
        hook[bstack111l111_opy_ (u"ࠦࡱࡵࡧࡴࠤᒢ")] = logs
    def bstack1l1l1ll1l11_opy_(
        self,
        bstack1l1lll111ll_opy_: bstack1lll1lllll1_opy_,
        entries: List[bstack1ll1lll1l11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᒣ"))
        req.platform_index = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll11l1lll1_opy_)
        req.execution_context.hash = str(bstack1l1lll111ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll111ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1l1ll1ll1_opy_)
            log_entry.uuid = entry.bstack1l11l111111_opy_ if entry.bstack1l11l111111_opy_ else TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll11l11l1l_opy_)
            log_entry.test_framework_state = bstack1l1lll111ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᒤ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111l111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒥ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll111lll_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1l1lll1ll_opy_():
            bstack1l1111lll_opy_ = datetime.now()
            try:
                self.bstack1lll1l11l1l_opy_.LogCreatedEvent(req)
                bstack1l1lll111ll_opy_.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᒦ"), datetime.now() - bstack1l1111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣᒧ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111lll_opy_.enqueue(bstack1l1l1lll1ll_opy_)
    def __1l111ll11l1_opy_(self, instance) -> None:
        bstack111l111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᒨ")
        bstack1l1111ll11l_opy_ = {bstack111l111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᒩ"): bstack1lll111l111_opy_.bstack1l111ll111l_opy_()}
        TestFramework.bstack1l1111ll1l1_opy_(instance, bstack1l1111ll11l_opy_)
    @staticmethod
    def __11lllll1ll1_opy_(instance, args):
        request, bstack11llllll1l1_opy_ = args
        bstack1l11l111l1l_opy_ = id(bstack11llllll1l1_opy_)
        bstack1l11111l1ll_opy_ = instance.data[TestFramework.bstack1l11111l11l_opy_]
        step = next(filter(lambda st: st[bstack111l111_opy_ (u"ࠬ࡯ࡤࠨᒪ")] == bstack1l11l111l1l_opy_, bstack1l11111l1ll_opy_[bstack111l111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒫ")]), None)
        step.update({
            bstack111l111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᒬ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11111l1ll_opy_[bstack111l111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒭ")]) if st[bstack111l111_opy_ (u"ࠩ࡬ࡨࠬᒮ")] == step[bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭ᒯ")]), None)
        if index is not None:
            bstack1l11111l1ll_opy_[bstack111l111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒰ")][index] = step
        instance.data[TestFramework.bstack1l11111l11l_opy_] = bstack1l11111l1ll_opy_
    @staticmethod
    def __1l111llllll_opy_(instance, args):
        bstack111l111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᒱ")
        bstack1l111lll1ll_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11llllll1l1_opy_ = args[1]
        bstack1l11l111l1l_opy_ = id(bstack11llllll1l1_opy_)
        bstack1l11111l1ll_opy_ = instance.data[TestFramework.bstack1l11111l11l_opy_]
        step = None
        if bstack1l11l111l1l_opy_ is not None and bstack1l11111l1ll_opy_.get(bstack111l111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᒲ")):
            step = next(filter(lambda st: st[bstack111l111_opy_ (u"ࠧࡪࡦࠪᒳ")] == bstack1l11l111l1l_opy_, bstack1l11111l1ll_opy_[bstack111l111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒴ")]), None)
            step.update({
                bstack111l111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᒵ"): bstack1l111lll1ll_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack111l111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᒶ"): bstack111l111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒷ"),
                bstack111l111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᒸ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack111l111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᒹ"): bstack111l111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒺ"),
                })
        index = next((i for i, st in enumerate(bstack1l11111l1ll_opy_[bstack111l111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒻ")]) if st[bstack111l111_opy_ (u"ࠩ࡬ࡨࠬᒼ")] == step[bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭ᒽ")]), None)
        if index is not None:
            bstack1l11111l1ll_opy_[bstack111l111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᒾ")][index] = step
        instance.data[TestFramework.bstack1l11111l11l_opy_] = bstack1l11111l1ll_opy_
    @staticmethod
    def __1l1111llll1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack111l111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᒿ")):
                examples = list(node.callspec.params[bstack111l111_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᓀ")].values())
            return examples
        except:
            return []
    def bstack1l1ll1ll11l_opy_(self, instance: bstack1lll1lllll1_opy_, bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_]):
        bstack1l111lll1l1_opy_ = (
            PytestBDDFramework.bstack11lllllllll_opy_
            if bstack1llllll111l_opy_[1] == bstack1lll111llll_opy_.PRE
            else PytestBDDFramework.bstack1l111lll111_opy_
        )
        hook = PytestBDDFramework.bstack1l1111l1lll_opy_(instance, bstack1l111lll1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11111l1l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1111lllll_opy_, []))
        return entries
    def bstack1l1lll1ll1l_opy_(self, instance: bstack1lll1lllll1_opy_, bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_]):
        bstack1l111lll1l1_opy_ = (
            PytestBDDFramework.bstack11lllllllll_opy_
            if bstack1llllll111l_opy_[1] == bstack1lll111llll_opy_.PRE
            else PytestBDDFramework.bstack1l111lll111_opy_
        )
        PytestBDDFramework.bstack1l1111l1l11_opy_(instance, bstack1l111lll1l1_opy_)
        TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1111lllll_opy_, []).clear()
    @staticmethod
    def bstack1l1111l1lll_opy_(instance: bstack1lll1lllll1_opy_, bstack1l111lll1l1_opy_: str):
        bstack1l111l1lll1_opy_ = (
            PytestBDDFramework.bstack1l11l11111l_opy_
            if bstack1l111lll1l1_opy_ == PytestBDDFramework.bstack1l111lll111_opy_
            else PytestBDDFramework.bstack1l11l1111ll_opy_
        )
        bstack1l111lllll1_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1l111lll1l1_opy_, None)
        bstack1l111l11lll_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1l111l1lll1_opy_, None) if bstack1l111lllll1_opy_ else None
        return (
            bstack1l111l11lll_opy_[bstack1l111lllll1_opy_][-1]
            if isinstance(bstack1l111l11lll_opy_, dict) and len(bstack1l111l11lll_opy_.get(bstack1l111lllll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l1111l1l11_opy_(instance: bstack1lll1lllll1_opy_, bstack1l111lll1l1_opy_: str):
        hook = PytestBDDFramework.bstack1l1111l1lll_opy_(instance, bstack1l111lll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11111l1l1_opy_, []).clear()
    @staticmethod
    def __1l111ll1ll1_opy_(instance: bstack1lll1lllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111l111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᓁ"), None)):
            return
        if os.getenv(bstack111l111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᓂ"), bstack111l111_opy_ (u"ࠤ࠴ࠦᓃ")) != bstack111l111_opy_ (u"ࠥ࠵ࠧᓄ"):
            PytestBDDFramework.logger.warning(bstack111l111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᓅ"))
            return
        bstack1l1111111l1_opy_ = {
            bstack111l111_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓆ"): (PytestBDDFramework.bstack11lllllllll_opy_, PytestBDDFramework.bstack1l11l1111ll_opy_),
            bstack111l111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᓇ"): (PytestBDDFramework.bstack1l111lll111_opy_, PytestBDDFramework.bstack1l11l11111l_opy_),
        }
        for when in (bstack111l111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᓈ"), bstack111l111_opy_ (u"ࠣࡥࡤࡰࡱࠨᓉ"), bstack111l111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᓊ")):
            bstack11lllll1lll_opy_ = args[1].get_records(when)
            if not bstack11lllll1lll_opy_:
                continue
            records = [
                bstack1ll1lll1l11_opy_(
                    kind=TestFramework.bstack1l1ll11lll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111l111_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᓋ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111l111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᓌ")) and r.created
                        else None
                    ),
                )
                for r in bstack11lllll1lll_opy_
                if isinstance(getattr(r, bstack111l111_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᓍ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11111ll11_opy_, bstack1l111l1lll1_opy_ = bstack1l1111111l1_opy_.get(when, (None, None))
            bstack11llllll1ll_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1l11111ll11_opy_, None) if bstack1l11111ll11_opy_ else None
            bstack1l111l11lll_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1l111l1lll1_opy_, None) if bstack11llllll1ll_opy_ else None
            if isinstance(bstack1l111l11lll_opy_, dict) and len(bstack1l111l11lll_opy_.get(bstack11llllll1ll_opy_, [])) > 0:
                hook = bstack1l111l11lll_opy_[bstack11llllll1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11111l1l1_opy_ in hook:
                    hook[TestFramework.bstack1l11111l1l1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1111lllll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111l1llll_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11l1111l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l111l1l111_opy_(request.node, scenario)
        bstack1l111l11ll1_opy_ = feature.filename
        if not bstack11l1111l_opy_ or not test_name or not bstack1l111l11ll1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll11l11l1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1111l_opy_: bstack11l1111l_opy_,
            TestFramework.bstack1ll111l111l_opy_: test_name,
            TestFramework.bstack1l1l1l1l111_opy_: bstack11l1111l_opy_,
            TestFramework.bstack1l111ll1l11_opy_: bstack1l111l11ll1_opy_,
            TestFramework.bstack1l111llll11_opy_: PytestBDDFramework.__1l111111l1l_opy_(feature, scenario),
            TestFramework.bstack1l111111111_opy_: code,
            TestFramework.bstack1l1l1111111_opy_: TestFramework.bstack1l111llll1l_opy_,
            TestFramework.bstack1l11l1l1l11_opy_: test_name
        }
    @staticmethod
    def __1l111l1l111_opy_(node, scenario):
        if hasattr(node, bstack111l111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᓎ")):
            parts = node.nodeid.rsplit(bstack111l111_opy_ (u"ࠢ࡜ࠤᓏ"))
            params = parts[-1]
            return bstack111l111_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣᓐ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111111l1l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack111l111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᓑ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack111l111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᓒ")) else [])
    @staticmethod
    def __1l111l1ll1l_opy_(location):
        return bstack111l111_opy_ (u"ࠦ࠿ࡀࠢᓓ").join(filter(lambda x: isinstance(x, str), location))