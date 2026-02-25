# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l111_opy_ import bstack11ll1l11ll1_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1l1llllll1l_opy_,
    bstack1l1llll111l_opy_,
    bstack1ll11lll1ll_opy_,
    bstack11ll111l11l_opy_,
    bstack1ll11l111l1_opy_,
)
import traceback
from bstack_utils.helper import bstack1l11ll1111l_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1111ll_opy_ import bstack1ll11l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll11llll1_opy_
bstack1l111lll1l1_opy_ = bstack1l11ll1111l_opy_()
bstack1l11lll1111_opy_ = bstack11l1l11_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᘆ")
bstack11ll1lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᘇ")
bstack11ll1l1lll1_opy_ = bstack11l1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᘈ")
bstack11ll11ll111_opy_ = 1.0
_1l11l11ll1l_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack11l1llll1ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᘉ")
    bstack11ll11lllll_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᘊ")
    bstack11ll1111l1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᘋ")
    bstack11l1lllll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᘌ")
    bstack11ll1llllll_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᘍ")
    bstack11ll1lllll1_opy_: bool
    bstack1lll1l11111_opy_: bstack1lll11llll1_opy_  = None
    bstack11lll111ll1_opy_ = [
        bstack1l1llllll1l_opy_.BEFORE_ALL,
        bstack1l1llllll1l_opy_.AFTER_ALL,
        bstack1l1llllll1l_opy_.BEFORE_EACH,
        bstack1l1llllll1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll111ll1l_opy_: Dict[str, str],
        bstack1l1l1ll1ll1_opy_: List[str]=[bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᘎ")],
        bstack1lll1l11111_opy_: bstack1lll11llll1_opy_ = None,
        bstack1ll1ll11111_opy_=None
    ):
        super().__init__(bstack1l1l1ll1ll1_opy_, bstack11ll111ll1l_opy_, bstack1lll1l11111_opy_)
        self.bstack11ll1lllll1_opy_ = any(bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᘏ") in item.lower() for item in bstack1l1l1ll1ll1_opy_)
        self.bstack1ll1ll11111_opy_ = bstack1ll1ll11111_opy_
    def track_event(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1l1llllll1l_opy_.TEST or test_framework_state in PytestBDDFramework.bstack11lll111ll1_opy_:
            bstack11ll1l11ll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1l1llllll1l_opy_.NONE:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᘐ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠢࠣᘑ"))
            return
        if not self.bstack11ll1lllll1_opy_:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᘒ") + str(str(self.bstack1l1l1ll1ll1_opy_)) + bstack11l1l11_opy_ (u"ࠤࠥᘓ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᘔ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧᘕ"))
            return
        instance = self.__11ll1111111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᘖ") + str(args) + bstack11l1l11_opy_ (u"ࠨࠢᘗ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11lll111ll1_opy_ and test_hook_state == bstack1ll11lll1ll_opy_.PRE:
                bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11l1l11l1l_opy_.value)
                name = str(EVENTS.bstack11l1l11l1l_opy_.name)+bstack11l1l11_opy_ (u"ࠢ࠻ࠤᘘ")+str(test_framework_state.name)
                TestFramework.bstack11ll11llll1_opy_(instance, name, bstack1l1l1l1111_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᘙ").format(e))
        try:
            if test_framework_state == bstack1l1llllll1l_opy_.TEST:
                if not TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack11l1lllll1l_opy_) and test_hook_state == bstack1ll11lll1ll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__11ll1111ll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᘚ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠥࠦᘛ"))
                if test_hook_state == bstack1ll11lll1ll_opy_.PRE and not TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11l11l11l_opy_):
                    TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11l11l11l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__11lll111l1l_opy_(instance, args)
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᘜ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠧࠨᘝ"))
                elif test_hook_state == bstack1ll11lll1ll_opy_.POST and not TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11llllll1_opy_):
                    TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11llllll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᘞ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠢࠣᘟ"))
            elif test_framework_state == bstack1l1llllll1l_opy_.STEP:
                if test_hook_state == bstack1ll11lll1ll_opy_.PRE:
                    PytestBDDFramework.__11ll1ll11ll_opy_(instance, args)
                elif test_hook_state == bstack1ll11lll1ll_opy_.POST:
                    PytestBDDFramework.__11ll1l11lll_opy_(instance, args)
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG and test_hook_state == bstack1ll11lll1ll_opy_.POST:
                PytestBDDFramework.__11ll1ll1111_opy_(instance, *args)
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG_REPORT and test_hook_state == bstack1ll11lll1ll_opy_.POST:
                self.__11ll1l111ll_opy_(instance, *args)
                self.__11ll11ll1ll_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack11lll111ll1_opy_:
                self.__11ll1ll1l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᘠ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠤࠥᘡ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1l111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack11lll111ll1_opy_ and test_hook_state == bstack1ll11lll1ll_opy_.POST:
                name = str(EVENTS.bstack11l1l11l1l_opy_.name)+bstack11l1l11_opy_ (u"ࠥ࠾ࠧᘢ")+str(test_framework_state.name)
                bstack1l1l1l1111_opy_ = TestFramework.bstack11ll1ll11l1_opy_(instance, name)
                bstack11ll1l1l1_opy_.end(EVENTS.bstack11l1l11l1l_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘣ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᘤ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᘥ").format(e))
    def bstack1l11ll111l1_opy_(self):
        return self.bstack11ll1lllll1_opy_
    def __11ll1ll111l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᘦ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11l111111_opy_(rep, [bstack11l1l11_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᘧ"), bstack11l1l11_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᘨ"), bstack11l1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᘩ"), bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᘪ"), bstack11l1l11_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᘫ"), bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᘬ")])
        return None
    def __11ll1l111ll_opy_(self, instance: bstack1l1llll111l_opy_, *args):
        result = self.__11ll1ll111l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll1l11_opy_ = None
        if result.get(bstack11l1l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᘭ"), None) == bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᘮ") and len(args) > 1 and getattr(args[1], bstack11l1l11_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᘯ"), None) is not None:
            failure = [{bstack11l1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᘰ"): [args[1].excinfo.exconly(), result.get(bstack11l1l11_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᘱ"), None)]}]
            bstack1lll1ll1l11_opy_ = bstack11l1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᘲ") if bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᘳ") in getattr(args[1].excinfo, bstack11l1l11_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᘴ"), bstack11l1l11_opy_ (u"ࠣࠤᘵ")) else bstack11l1l11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᘶ")
        bstack11ll1l1111l_opy_ = result.get(bstack11l1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᘷ"), TestFramework.bstack11ll111ll11_opy_)
        if bstack11ll1l1111l_opy_ != TestFramework.bstack11ll111ll11_opy_:
            TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1l11111_opy_(instance, {
            TestFramework.bstack1l111111lll_opy_: failure,
            TestFramework.bstack11ll111llll_opy_: bstack1lll1ll1l11_opy_,
            TestFramework.bstack1l1111l11l1_opy_: bstack11ll1l1111l_opy_,
        })
    def __11ll1111111_opy_(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1l1llllll1l_opy_.SETUP_FIXTURE:
            instance = self.__11ll1l1l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1lll11l_opy_ bstack11ll11111ll_opy_ this to be bstack11l1l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᘸ")
            if test_framework_state == bstack1l1llllll1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll11lll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᘹ"), None), bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᘺ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᘻ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᘼ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll11ll11l_opy_(target) if target else None
        return instance
    def __11ll1ll1l11_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11ll111l1ll_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, PytestBDDFramework.bstack11ll11lllll_opy_, {})
        if not key in bstack11ll111l1ll_opy_:
            bstack11ll111l1ll_opy_[key] = []
        bstack11ll11l11ll_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, PytestBDDFramework.bstack11ll1111l1l_opy_, {})
        if not key in bstack11ll11l11ll_opy_:
            bstack11ll11l11ll_opy_[key] = []
        bstack11ll11ll1l1_opy_ = {
            PytestBDDFramework.bstack11ll11lllll_opy_: bstack11ll111l1ll_opy_,
            PytestBDDFramework.bstack11ll1111l1l_opy_: bstack11ll11l11ll_opy_,
        }
        if test_hook_state == bstack1ll11lll1ll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l1l11_opy_ (u"ࠤ࡮ࡩࡾࠨᘽ"): key,
                TestFramework.bstack11l1llllll1_opy_: uuid4().__str__(),
                TestFramework.bstack11ll1ll1lll_opy_: TestFramework.bstack11ll11111l1_opy_,
                TestFramework.bstack11ll1llll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll11lll1l_opy_: [],
                TestFramework.bstack11ll111111l_opy_: hook_name,
                TestFramework.bstack11lll1111l1_opy_: bstack1ll11l1l1l1_opy_.bstack11ll11l111l_opy_()
            }
            bstack11ll111l1ll_opy_[key].append(hook)
            bstack11ll11ll1l1_opy_[PytestBDDFramework.bstack11l1lllll11_opy_] = key
        elif test_hook_state == bstack1ll11lll1ll_opy_.POST:
            bstack11ll1l1ll1l_opy_ = bstack11ll111l1ll_opy_.get(key, [])
            hook = bstack11ll1l1ll1l_opy_.pop() if bstack11ll1l1ll1l_opy_ else None
            if hook:
                result = self.__11ll1ll111l_opy_(*args)
                if result:
                    bstack11ll1l1l11l_opy_ = result.get(bstack11l1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᘾ"), TestFramework.bstack11ll11111l1_opy_)
                    if bstack11ll1l1l11l_opy_ != TestFramework.bstack11ll11111l1_opy_:
                        hook[TestFramework.bstack11ll1ll1lll_opy_] = bstack11ll1l1l11l_opy_
                hook[TestFramework.bstack11lll111lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lll1111l1_opy_] = bstack1ll11l1l1l1_opy_.bstack11ll11l111l_opy_()
                self.bstack11ll1ll1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll11l1l1l_opy_, [])
                self.bstack1l11ll11111_opy_(instance, logs)
                bstack11ll11l11ll_opy_[key].append(hook)
                bstack11ll11ll1l1_opy_[PytestBDDFramework.bstack11ll1llllll_opy_] = key
        TestFramework.bstack11ll1l11111_opy_(instance, bstack11ll11ll1l1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᘿ") + str(bstack11ll11l11ll_opy_) + bstack11l1l11_opy_ (u"ࠧࠨᙀ"))
    def __11ll1l1l1l1_opy_(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11l111111_opy_(args[0], [bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᙁ"), bstack11l1l11_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᙂ"), bstack11l1l11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᙃ"), bstack11l1l11_opy_ (u"ࠤ࡬ࡨࡸࠨᙄ"), bstack11l1l11_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᙅ"), bstack11l1l11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᙆ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l1l11_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᙇ")) else fixturedef.get(bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᙈ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1l11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᙉ")) else None
        node = request.node if hasattr(request, bstack11l1l11_opy_ (u"ࠣࡰࡲࡨࡪࠨᙊ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᙋ")) else None
        baseid = fixturedef.get(bstack11l1l11_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᙌ"), None) or bstack11l1l11_opy_ (u"ࠦࠧᙍ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1l11_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᙎ")):
            target = PytestBDDFramework.__11ll1lll1ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᙏ")) else None
            if target and not TestFramework.bstack1lll11ll11l_opy_(target):
                self.__11ll11lll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᙐ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠣࠤᙑ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᙒ") + str(target) + bstack11l1l11_opy_ (u"ࠥࠦᙓ"))
            return None
        instance = TestFramework.bstack1lll11ll11l_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᙔ") + str(target) + bstack11l1l11_opy_ (u"ࠧࠨᙕ"))
            return None
        bstack11ll111lll1_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, PytestBDDFramework.bstack11l1llll1ll_opy_, {})
        if os.getenv(bstack11l1l11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᙖ"), bstack11l1l11_opy_ (u"ࠢ࠲ࠤᙗ")) == bstack11l1l11_opy_ (u"ࠣ࠳ࠥᙘ"):
            bstack11ll1lll111_opy_ = bstack11l1l11_opy_ (u"ࠤ࠽ࠦᙙ").join((scope, fixturename))
            bstack11lll11l111_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1llll11l_opy_ = {
                bstack11l1l11_opy_ (u"ࠥ࡯ࡪࡿࠢᙚ"): bstack11ll1lll111_opy_,
                bstack11l1l11_opy_ (u"ࠦࡹࡧࡧࡴࠤᙛ"): PytestBDDFramework.__11l1llll111_opy_(request.node, scenario),
                bstack11l1l11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᙜ"): fixturedef,
                bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᙝ"): scope,
                bstack11l1l11_opy_ (u"ࠢࡵࡻࡳࡩࠧᙞ"): None,
            }
            try:
                if test_hook_state == bstack1ll11lll1ll_opy_.POST and callable(getattr(args[-1], bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᙟ"), None)):
                    bstack11l1llll11l_opy_[bstack11l1l11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᙠ")] = TestFramework.bstack1l11lll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll11lll1ll_opy_.PRE:
                bstack11l1llll11l_opy_[bstack11l1l11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᙡ")] = uuid4().__str__()
                bstack11l1llll11l_opy_[PytestBDDFramework.bstack11ll1llll11_opy_] = bstack11lll11l111_opy_
            elif test_hook_state == bstack1ll11lll1ll_opy_.POST:
                bstack11l1llll11l_opy_[PytestBDDFramework.bstack11lll111lll_opy_] = bstack11lll11l111_opy_
            if bstack11ll1lll111_opy_ in bstack11ll111lll1_opy_:
                bstack11ll111lll1_opy_[bstack11ll1lll111_opy_].update(bstack11l1llll11l_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᙢ") + str(bstack11ll111lll1_opy_[bstack11ll1lll111_opy_]) + bstack11l1l11_opy_ (u"ࠧࠨᙣ"))
            else:
                bstack11ll111lll1_opy_[bstack11ll1lll111_opy_] = bstack11l1llll11l_opy_
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᙤ") + str(len(bstack11ll111lll1_opy_)) + bstack11l1l11_opy_ (u"ࠢࠣᙥ"))
        TestFramework.bstack1lll111ll11_opy_(instance, PytestBDDFramework.bstack11l1llll1ll_opy_, bstack11ll111lll1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᙦ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠤࠥᙧ"))
        return instance
    def __11ll11lll11_opy_(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1llllll1_opy_.create_context(target)
        ob = bstack1l1llll111l_opy_(ctx, self.bstack1l1l1ll1ll1_opy_, self.bstack11ll111ll1l_opy_, test_framework_state)
        TestFramework.bstack11ll1l11111_opy_(ob, {
            TestFramework.bstack1l1ll1l1lll_opy_: context.test_framework_name,
            TestFramework.bstack1l11l1l11ll_opy_: context.test_framework_version,
            TestFramework.bstack11l1lllllll_opy_: [],
            PytestBDDFramework.bstack11l1llll1ll_opy_: {},
            PytestBDDFramework.bstack11ll1111l1l_opy_: {},
            PytestBDDFramework.bstack11ll11lllll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll111ll11_opy_(ob, TestFramework.bstack11ll11l1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll111ll11_opy_(ob, TestFramework.bstack1l1l1l1ll11_opy_, context.platform_index)
        TestFramework.bstack1ll1ll1ll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᙨ") + str(TestFramework.bstack1ll1ll1ll1l_opy_.keys()) + bstack11l1l11_opy_ (u"ࠦࠧᙩ"))
        return ob
    @staticmethod
    def __11lll111l1l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᙪ"): id(step),
                bstack11l1l11_opy_ (u"࠭ࡴࡦࡺࡷࠫᙫ"): step.name,
                bstack11l1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᙬ"): step.keyword,
            })
        meta = {
            bstack11l1l11_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ᙭"): {
                bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᙮"): feature.name,
                bstack11l1l11_opy_ (u"ࠪࡴࡦࡺࡨࠨᙯ"): feature.filename,
                bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᙰ"): feature.description
            },
            bstack11l1l11_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᙱ"): {
                bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙲ"): scenario.name
            },
            bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᙳ"): steps,
            bstack11l1l11_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᙴ"): PytestBDDFramework.__11ll11l11l1_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack11lll11111l_opy_: meta
            }
        )
    def bstack11ll1ll1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᙵ")
        global _1l11l11ll1l_opy_
        platform_index = os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᙶ")]
        bstack1l11l111l11_opy_ = os.path.join(bstack1l111lll1l1_opy_, (bstack1l11lll1111_opy_ + str(platform_index)), bstack11ll1lll1l1_opy_)
        if not os.path.exists(bstack1l11l111l11_opy_) or not os.path.isdir(bstack1l11l111l11_opy_):
            return
        logs = hook.get(bstack11l1l11_opy_ (u"ࠦࡱࡵࡧࡴࠤᙷ"), [])
        with os.scandir(bstack1l11l111l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11l11ll1l_opy_:
                    self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᙸ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1l11_opy_ (u"ࠨࠢᙹ")
                    log_entry = bstack1ll11l111l1_opy_(
                        kind=bstack11l1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᙺ"),
                        message=bstack11l1l11_opy_ (u"ࠣࠤᙻ"),
                        level=bstack11l1l11_opy_ (u"ࠤࠥᙼ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11lll1lll_opy_=entry.stat().st_size,
                        bstack1l11ll1lll1_opy_=bstack11l1l11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᙽ"),
                        bstack1lll1ll_opy_=os.path.abspath(entry.path),
                        bstack11lll111111_opy_=hook.get(TestFramework.bstack11l1llllll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l11l11ll1l_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᙾ")]
        bstack11ll111l1l1_opy_ = os.path.join(bstack1l111lll1l1_opy_, (bstack1l11lll1111_opy_ + str(platform_index)), bstack11ll1lll1l1_opy_, bstack11ll1l1lll1_opy_)
        if not os.path.exists(bstack11ll111l1l1_opy_) or not os.path.isdir(bstack11ll111l1l1_opy_):
            self.logger.info(bstack11l1l11_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᙿ").format(bstack11ll111l1l1_opy_))
        else:
            self.logger.info(bstack11l1l11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧ ").format(bstack11ll111l1l1_opy_))
            with os.scandir(bstack11ll111l1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11l11ll1l_opy_:
                        self.logger.info(bstack11l1l11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᚁ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1l11_opy_ (u"ࠣࠤᚂ")
                        log_entry = bstack1ll11l111l1_opy_(
                            kind=bstack11l1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᚃ"),
                            message=bstack11l1l11_opy_ (u"ࠥࠦᚄ"),
                            level=bstack11l1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᚅ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11lll1lll_opy_=entry.stat().st_size,
                            bstack1l11ll1lll1_opy_=bstack11l1l11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᚆ"),
                            bstack1lll1ll_opy_=os.path.abspath(entry.path),
                            bstack1l11l1ll11l_opy_=hook.get(TestFramework.bstack11l1llllll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l11l11ll1l_opy_.add(abs_path)
        hook[bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᚇ")] = logs
    def bstack1l11ll11111_opy_(
        self,
        bstack1l111llllll_opy_: bstack1l1llll111l_opy_,
        entries: List[bstack1ll11l111l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᚈ"))
        req.platform_index = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᚉ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111llllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111llllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111llllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1ll1l1lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l11l1l11ll_opy_)
            log_entry.uuid = entry.bstack11lll111111_opy_ if entry.bstack11lll111111_opy_ else TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1l11lll11_opy_)
            log_entry.test_framework_state = bstack1l111llllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᚊ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᚋ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11lll1lll_opy_
                log_entry.file_path = entry.bstack1lll1ll_opy_
        def bstack1l11l1l1lll_opy_():
            bstack111l11l1l1_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11111_opy_.LogCreatedEvent(req)
                bstack1l111llllll_opy_.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᚌ"), datetime.now() - bstack111l11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᚍ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll1l11111_opy_.enqueue(bstack1l11l1l1lll_opy_)
    def __11ll11ll1ll_opy_(self, instance) -> None:
        bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᚎ")
        bstack11ll11ll1l1_opy_ = {bstack11l1l11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᚏ"): bstack1ll11l1l1l1_opy_.bstack11ll11l111l_opy_()}
        TestFramework.bstack11ll1l11111_opy_(instance, bstack11ll11ll1l1_opy_)
    @staticmethod
    def __11ll1ll11ll_opy_(instance, args):
        request, bstack11ll1l1l111_opy_ = args
        bstack11ll1111lll_opy_ = id(bstack11ll1l1l111_opy_)
        bstack11ll1l1ll11_opy_ = instance.data[TestFramework.bstack11lll11111l_opy_]
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫᚐ")] == bstack11ll1111lll_opy_, bstack11ll1l1ll11_opy_[bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᚑ")]), None)
        step.update({
            bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚒ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack11ll1l1ll11_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚓ")]) if st[bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᚔ")] == step[bstack11l1l11_opy_ (u"࠭ࡩࡥࠩᚕ")]), None)
        if index is not None:
            bstack11ll1l1ll11_opy_[bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᚖ")][index] = step
        instance.data[TestFramework.bstack11lll11111l_opy_] = bstack11ll1l1ll11_opy_
    @staticmethod
    def __11ll1l11lll_opy_(instance, args):
        bstack11l1l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡽࡨࡦࡰࠣࡰࡪࡴࠠࡢࡴࡪࡷࠥ࡯ࡳࠡ࠴࠯ࠤ࡮ࡺࠠࡴ࡫ࡪࡲ࡮࡬ࡩࡦࡵࠣࡸ࡭࡫ࡲࡦࠢ࡬ࡷࠥࡴ࡯ࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠲࡛ࠦࡳࡧࡴࡹࡪࡹࡴ࠭ࠢࡶࡸࡪࡶ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠴ࠢࡷ࡬ࡪࡴࠠࡵࡪࡨࠤࡱࡧࡳࡵࠢࡹࡥࡱࡻࡥࠡ࡫ࡶࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᚗ")
        finished_at = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack11ll1l1l111_opy_ = args[1]
        bstack11ll1111lll_opy_ = id(bstack11ll1l1l111_opy_)
        bstack11ll1l1ll11_opy_ = instance.data[TestFramework.bstack11lll11111l_opy_]
        step = None
        if bstack11ll1111lll_opy_ is not None and bstack11ll1l1ll11_opy_.get(bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᚘ")):
            step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭ᚙ")] == bstack11ll1111lll_opy_, bstack11ll1l1ll11_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚚ")]), None)
            step.update({
                bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᚛"): finished_at,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᚜"): bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᚝"),
                bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᚞"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᚟"): bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚠ"),
                })
        index = next((i for i, st in enumerate(bstack11ll1l1ll11_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚡ")]) if st[bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨᚢ")] == step[bstack11l1l11_opy_ (u"࠭ࡩࡥࠩᚣ")]), None)
        if index is not None:
            bstack11ll1l1ll11_opy_[bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᚤ")][index] = step
        instance.data[TestFramework.bstack11lll11111l_opy_] = bstack11ll1l1ll11_opy_
    @staticmethod
    def __11ll11l11l1_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l1l11_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᚥ")):
                examples = list(node.callspec.params[bstack11l1l11_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᚦ")].values())
            return examples
        except:
            return []
    def bstack1l11ll1l11l_opy_(self, instance: bstack1l1llll111l_opy_, bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_]):
        bstack11ll1111l11_opy_ = (
            PytestBDDFramework.bstack11l1lllll11_opy_
            if bstack1lll11ll111_opy_[1] == bstack1ll11lll1ll_opy_.PRE
            else PytestBDDFramework.bstack11ll1llllll_opy_
        )
        hook = PytestBDDFramework.bstack11ll1l1llll_opy_(instance, bstack11ll1111l11_opy_)
        entries = hook.get(TestFramework.bstack11ll11lll1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11l1lllllll_opy_, []))
        return entries
    def bstack1l11l1ll1l1_opy_(self, instance: bstack1l1llll111l_opy_, bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_]):
        bstack11ll1111l11_opy_ = (
            PytestBDDFramework.bstack11l1lllll11_opy_
            if bstack1lll11ll111_opy_[1] == bstack1ll11lll1ll_opy_.PRE
            else PytestBDDFramework.bstack11ll1llllll_opy_
        )
        PytestBDDFramework.bstack11ll11l1ll1_opy_(instance, bstack11ll1111l11_opy_)
        TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11l1lllllll_opy_, []).clear()
    @staticmethod
    def bstack11ll1l1llll_opy_(instance: bstack1l1llll111l_opy_, bstack11ll1111l11_opy_: str):
        bstack11lll1111ll_opy_ = (
            PytestBDDFramework.bstack11ll1111l1l_opy_
            if bstack11ll1111l11_opy_ == PytestBDDFramework.bstack11ll1llllll_opy_
            else PytestBDDFramework.bstack11ll11lllll_opy_
        )
        bstack11lll111l11_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11ll1111l11_opy_, None)
        bstack11ll1ll1ll1_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11lll1111ll_opy_, None) if bstack11lll111l11_opy_ else None
        return (
            bstack11ll1ll1ll1_opy_[bstack11lll111l11_opy_][-1]
            if isinstance(bstack11ll1ll1ll1_opy_, dict) and len(bstack11ll1ll1ll1_opy_.get(bstack11lll111l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll11l1ll1_opy_(instance: bstack1l1llll111l_opy_, bstack11ll1111l11_opy_: str):
        hook = PytestBDDFramework.bstack11ll1l1llll_opy_(instance, bstack11ll1111l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll11lll1l_opy_, []).clear()
    @staticmethod
    def __11ll1ll1111_opy_(instance: bstack1l1llll111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1l11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᚧ"), None)):
            return
        if os.getenv(bstack11l1l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᚨ"), bstack11l1l11_opy_ (u"ࠧ࠷ࠢᚩ")) != bstack11l1l11_opy_ (u"ࠨ࠱ࠣᚪ"):
            PytestBDDFramework.logger.warning(bstack11l1l11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᚫ"))
            return
        bstack11ll1l11l11_opy_ = {
            bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᚬ"): (PytestBDDFramework.bstack11l1lllll11_opy_, PytestBDDFramework.bstack11ll11lllll_opy_),
            bstack11l1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᚭ"): (PytestBDDFramework.bstack11ll1llllll_opy_, PytestBDDFramework.bstack11ll1111l1l_opy_),
        }
        for when in (bstack11l1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᚮ"), bstack11l1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᚯ"), bstack11l1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᚰ")):
            bstack11ll11l1111_opy_ = args[1].get_records(when)
            if not bstack11ll11l1111_opy_:
                continue
            records = [
                bstack1ll11l111l1_opy_(
                    kind=TestFramework.bstack1l111lll1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1l11_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᚱ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1l11_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᚲ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll11l1111_opy_
                if isinstance(getattr(r, bstack11l1l11_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᚳ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1llll1l1_opy_, bstack11lll1111ll_opy_ = bstack11ll1l11l11_opy_.get(when, (None, None))
            bstack11ll111l111_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11l1llll1l1_opy_, None) if bstack11l1llll1l1_opy_ else None
            bstack11ll1ll1ll1_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11lll1111ll_opy_, None) if bstack11ll111l111_opy_ else None
            if isinstance(bstack11ll1ll1ll1_opy_, dict) and len(bstack11ll1ll1ll1_opy_.get(bstack11ll111l111_opy_, [])) > 0:
                hook = bstack11ll1ll1ll1_opy_[bstack11ll111l111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll11lll1l_opy_ in hook:
                    hook[TestFramework.bstack11ll11lll1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11l1lllllll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1111ll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1l11l1lll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__11ll11l1l11_opy_(request.node, scenario)
        bstack11ll1l11l1l_opy_ = feature.filename
        if not bstack1l11l1lll_opy_ or not test_name or not bstack11ll1l11l1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1l1l11lll11_opy_: uuid4().__str__(),
            TestFramework.bstack11l1lllll1l_opy_: bstack1l11l1lll_opy_,
            TestFramework.bstack1l1ll11llll_opy_: test_name,
            TestFramework.bstack1l111ll1111_opy_: bstack1l11l1lll_opy_,
            TestFramework.bstack11ll11ll11l_opy_: bstack11ll1l11l1l_opy_,
            TestFramework.bstack11ll1llll1l_opy_: PytestBDDFramework.__11l1llll111_opy_(feature, scenario),
            TestFramework.bstack11ll1l1l1ll_opy_: code,
            TestFramework.bstack1l1111l11l1_opy_: TestFramework.bstack11ll111ll11_opy_,
            TestFramework.bstack11lll1l1lll_opy_: test_name
        }
    @staticmethod
    def __11ll11l1l11_opy_(node, scenario):
        if hasattr(node, bstack11l1l11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᚴ")):
            parts = node.nodeid.rsplit(bstack11l1l11_opy_ (u"ࠥ࡟ࠧᚵ"))
            params = parts[-1]
            return bstack11l1l11_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᚶ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __11l1llll111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪᚷ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l1l11_opy_ (u"࠭ࡴࡢࡩࡶࠫᚸ")) else [])
    @staticmethod
    def __11ll1lll1ll_opy_(location):
        return bstack11l1l11_opy_ (u"ࠢ࠻࠼ࠥᚹ").join(filter(lambda x: isinstance(x, str), location))