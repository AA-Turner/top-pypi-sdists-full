# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1lll1lll_opy_ import bstack1l1lll111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll111l1_opy_ import bstack1l1ll1l111l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllll11l11_opy_,
    bstack1lllll111ll_opy_,
    bstack1lll1lll1ll_opy_,
    bstack1l1l1l1l1l1_opy_,
    bstack1llll11ll1l_opy_,
)
import traceback
from bstack_utils.helper import bstack1lllllll1l1_opy_
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l1l1_opy_ import bstack1l1lll1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l1l_opy_ import bstack1ll1llllll1_opy_
bstack1lllllll111_opy_ = bstack1lllllll1l1_opy_()
bstack1111111lll_opy_ = bstack11l1111_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢኊ")
bstack1l1lll1111l_opy_ = bstack11l1111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦኋ")
bstack1l1ll111ll1_opy_ = bstack11l1111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣኌ")
bstack1l1lll1llll_opy_ = 1.0
_1llll11lll1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l1l1l1l1ll_opy_ = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥኍ")
    bstack1l1l1llll1l_opy_ = bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤ኎")
    bstack1l1l1ll1l11_opy_ = bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦ኏")
    bstack1l1ll1ll1ll_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣነ")
    bstack1l1ll1ll111_opy_ = bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥኑ")
    bstack1l1ll1ll1l1_opy_: bool
    bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_  = None
    bstack1l1l1l1lll1_opy_ = [
        bstack1lllll11l11_opy_.BEFORE_ALL,
        bstack1lllll11l11_opy_.AFTER_ALL,
        bstack1lllll11l11_opy_.BEFORE_EACH,
        bstack1lllll11l11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1lll1l11l_opy_: Dict[str, str],
        bstack1l1l1lll111_opy_: List[str]=[bstack11l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧኒ")],
        bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_ = None,
        bstack1lll1llll1l_opy_=None
    ):
        super().__init__(bstack1l1l1lll111_opy_, bstack1l1lll1l11l_opy_, bstack1llll1l1l1l_opy_)
        self.bstack1l1ll1ll1l1_opy_ = any(bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨና") in item.lower() for item in bstack1l1l1lll111_opy_)
        self.bstack1lll1llll1l_opy_ = bstack1lll1llll1l_opy_
    def track_event(
        self,
        context: bstack1l1l1l1l1l1_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll1lll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lllll11l11_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_:
            bstack1l1ll1l111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllll11l11_opy_.NONE:
            self.logger.warning(bstack11l1111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦኔ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠦࠧን"))
            return
        if not self.bstack1l1ll1ll1l1_opy_:
            self.logger.warning(bstack11l1111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨኖ") + str(str(self.bstack1l1l1lll111_opy_)) + bstack11l1111_opy_ (u"ࠨࠢኗ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኘ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤኙ"))
            return
        instance = self.__1l1l1lll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣኚ") + str(args) + bstack11l1111_opy_ (u"ࠥࠦኛ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_ and test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack11ll1l11l_opy_.value)
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack11l1111_opy_ (u"ࠦ࠿ࠨኜ")+str(test_framework_state.name)
                TestFramework.bstack1l1ll1lll11_opy_(instance, name, bstack1lll1lll11l_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤኝ").format(e))
        try:
            if test_framework_state == bstack1lllll11l11_opy_.TEST:
                if not TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1ll11l111_opy_) and test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l1l1l11111_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨኞ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠢࠣኟ"))
                if test_hook_state == bstack1lll1lll1ll_opy_.PRE and not TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1lllll1ll1l_opy_):
                    TestFramework.bstack1llll111l11_opy_(instance, TestFramework.bstack1lllll1ll1l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l1ll1l1111_opy_(instance, args)
                    self.logger.debug(bstack11l1111_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨአ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠤࠥኡ"))
                elif test_hook_state == bstack1lll1lll1ll_opy_.POST and not TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1lll1lll111_opy_):
                    TestFramework.bstack1llll111l11_opy_(instance, TestFramework.bstack1lll1lll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨኢ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠦࠧኣ"))
            elif test_framework_state == bstack1lllll11l11_opy_.STEP:
                if test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                    PytestBDDFramework.__1l1llll1l1l_opy_(instance, args)
                elif test_hook_state == bstack1lll1lll1ll_opy_.POST:
                    PytestBDDFramework.__1l1lll1l111_opy_(instance, args)
            elif test_framework_state == bstack1lllll11l11_opy_.LOG and test_hook_state == bstack1lll1lll1ll_opy_.POST:
                PytestBDDFramework.__1l1llll111l_opy_(instance, *args)
            elif test_framework_state == bstack1lllll11l11_opy_.LOG_REPORT and test_hook_state == bstack1lll1lll1ll_opy_.POST:
                self.__1l1l1l11l1l_opy_(instance, *args)
                self.__1l1ll1l11l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_:
                self.__1l1llll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨኤ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠨࠢእ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l1l1ll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l1l1l1lll1_opy_ and test_hook_state == bstack1lll1lll1ll_opy_.POST:
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack11l1111_opy_ (u"ࠢ࠻ࠤኦ")+str(test_framework_state.name)
                bstack1lll1lll11l_opy_ = TestFramework.bstack1l1l1ll11ll_opy_(instance, name)
                bstack1lll1l1l11l_opy_.end(EVENTS.bstack11ll1l11l_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኧ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢከ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥኩ").format(e))
    def bstack1lllllll1ll_opy_(self):
        return self.bstack1l1ll1ll1l1_opy_
    def __1l1l1ll1lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣኪ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1lll1ll11ll_opy_(rep, [bstack11l1111_opy_ (u"ࠧࡽࡨࡦࡰࠥካ"), bstack11l1111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢኬ"), bstack11l1111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢክ"), bstack11l1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣኮ"), bstack11l1111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥኯ"), bstack11l1111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤኰ")])
        return None
    def __1l1l1l11l1l_opy_(self, instance: bstack1lllll111ll_opy_, *args):
        result = self.__1l1l1ll1lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111llll_opy_ = None
        if result.get(bstack11l1111_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ኱"), None) == bstack11l1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧኲ") and len(args) > 1 and getattr(args[1], bstack11l1111_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢኳ"), None) is not None:
            failure = [{bstack11l1111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪኴ"): [args[1].excinfo.exconly(), result.get(bstack11l1111_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢኵ"), None)]}]
            bstack111111llll_opy_ = bstack11l1111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ኶") if bstack11l1111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ኷") in getattr(args[1].excinfo, bstack11l1111_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨኸ"), bstack11l1111_opy_ (u"ࠧࠨኹ")) else bstack11l1111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢኺ")
        bstack1l1lll11lll_opy_ = result.get(bstack11l1111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣኻ"), TestFramework.bstack1l1lll11ll1_opy_)
        if bstack1l1lll11lll_opy_ != TestFramework.bstack1l1lll11ll1_opy_:
            TestFramework.bstack1llll111l11_opy_(instance, TestFramework.bstack11111111l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1ll1111ll_opy_(instance, {
            TestFramework.bstack1ll1l111l11_opy_: failure,
            TestFramework.bstack1l1ll1l1ll1_opy_: bstack111111llll_opy_,
            TestFramework.bstack1ll1l11l111_opy_: bstack1l1lll11lll_opy_,
        })
    def __1l1l1lll1ll_opy_(
        self,
        context: bstack1l1l1l1l1l1_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll1lll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lllll11l11_opy_.SETUP_FIXTURE:
            instance = self.__1l1llll1ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l1l1llll11_opy_ bstack1l1l1lll1l1_opy_ this to be bstack11l1111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣኼ")
            if test_framework_state == bstack1lllll11l11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1ll11111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllll11l11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࠢኽ"), None), bstack11l1111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥኾ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1111_opy_ (u"ࠦࡳࡵࡤࡦࠤ኿"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11l1111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧዀ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1l1l1lllll1_opy_(target) if target else None
        return instance
    def __1l1llll11l1_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll1lll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1l1l111ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, PytestBDDFramework.bstack1l1l1llll1l_opy_, {})
        if not key in bstack1l1l1l111ll_opy_:
            bstack1l1l1l111ll_opy_[key] = []
        bstack1l1ll11l1ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, PytestBDDFramework.bstack1l1l1ll1l11_opy_, {})
        if not key in bstack1l1ll11l1ll_opy_:
            bstack1l1ll11l1ll_opy_[key] = []
        bstack1l1l1l11l11_opy_ = {
            PytestBDDFramework.bstack1l1l1llll1l_opy_: bstack1l1l1l111ll_opy_,
            PytestBDDFramework.bstack1l1l1ll1l11_opy_: bstack1l1ll11l1ll_opy_,
        }
        if test_hook_state == bstack1lll1lll1ll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11l1111_opy_ (u"ࠨ࡫ࡦࡻࠥ዁"): key,
                TestFramework.bstack1l1l1l11lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1lll1lll1_opy_: TestFramework.bstack1l1ll111111_opy_,
                TestFramework.bstack1l1l1l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1l1ll1ll1_opy_: [],
                TestFramework.bstack1l1lll111l1_opy_: hook_name,
                TestFramework.bstack1l1llll1111_opy_: bstack1l1lll1l1ll_opy_.bstack1l1ll1l1lll_opy_()
            }
            bstack1l1l1l111ll_opy_[key].append(hook)
            bstack1l1l1l11l11_opy_[PytestBDDFramework.bstack1l1ll1ll1ll_opy_] = key
        elif test_hook_state == bstack1lll1lll1ll_opy_.POST:
            bstack1l1l1ll111l_opy_ = bstack1l1l1l111ll_opy_.get(key, [])
            hook = bstack1l1l1ll111l_opy_.pop() if bstack1l1l1ll111l_opy_ else None
            if hook:
                result = self.__1l1l1ll1lll_opy_(*args)
                if result:
                    bstack1l1lll1ll11_opy_ = result.get(bstack11l1111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣዂ"), TestFramework.bstack1l1ll111111_opy_)
                    if bstack1l1lll1ll11_opy_ != TestFramework.bstack1l1ll111111_opy_:
                        hook[TestFramework.bstack1l1lll1lll1_opy_] = bstack1l1lll1ll11_opy_
                hook[TestFramework.bstack1l1lll11l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l1llll1111_opy_] = bstack1l1lll1l1ll_opy_.bstack1l1ll1l1lll_opy_()
                self.bstack1l1ll1l1l11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1ll11ll11_opy_, [])
                self.bstack1lll1ll111l_opy_(instance, logs)
                bstack1l1ll11l1ll_opy_[key].append(hook)
                bstack1l1l1l11l11_opy_[PytestBDDFramework.bstack1l1ll1ll111_opy_] = key
        TestFramework.bstack1l1ll1111ll_opy_(instance, bstack1l1l1l11l11_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢዃ") + str(bstack1l1ll11l1ll_opy_) + bstack11l1111_opy_ (u"ࠤࠥዄ"))
    def __1l1llll1ll1_opy_(
        self,
        context: bstack1l1l1l1l1l1_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll1lll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1lll1ll11ll_opy_(args[0], [bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤዅ"), bstack11l1111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧ዆"), bstack11l1111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ዇"), bstack11l1111_opy_ (u"ࠨࡩࡥࡵࠥወ"), bstack11l1111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤዉ"), bstack11l1111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣዊ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11l1111_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣዋ")) else fixturedef.get(bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤዌ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤው")) else None
        node = request.node if hasattr(request, bstack11l1111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥዎ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨዏ")) else None
        baseid = fixturedef.get(bstack11l1111_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢዐ"), None) or bstack11l1111_opy_ (u"ࠣࠤዑ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1111_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢዒ")):
            target = PytestBDDFramework.__1l1l1l1l111_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1111_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧዓ")) else None
            if target and not TestFramework.bstack1l1l1lllll1_opy_(target):
                self.__1l1ll11111l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨዔ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠧࠨዕ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦዖ") + str(target) + bstack11l1111_opy_ (u"ࠢࠣ዗"))
            return None
        instance = TestFramework.bstack1l1l1lllll1_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥዘ") + str(target) + bstack11l1111_opy_ (u"ࠤࠥዙ"))
            return None
        bstack1l1ll11llll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, PytestBDDFramework.bstack1l1l1l1l1ll_opy_, {})
        if os.getenv(bstack11l1111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦዚ"), bstack11l1111_opy_ (u"ࠦ࠶ࠨዛ")) == bstack11l1111_opy_ (u"ࠧ࠷ࠢዜ"):
            bstack1l1l1llllll_opy_ = bstack11l1111_opy_ (u"ࠨ࠺ࠣዝ").join((scope, fixturename))
            bstack1l1l1l11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1l1l1111l_opy_ = {
                bstack11l1111_opy_ (u"ࠢ࡬ࡧࡼࠦዞ"): bstack1l1l1llllll_opy_,
                bstack11l1111_opy_ (u"ࠣࡶࡤ࡫ࡸࠨዟ"): PytestBDDFramework.__1l1ll11lll1_opy_(request.node, scenario),
                bstack11l1111_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥዠ"): fixturedef,
                bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤዡ"): scope,
                bstack11l1111_opy_ (u"ࠦࡹࡿࡰࡦࠤዢ"): None,
            }
            try:
                if test_hook_state == bstack1lll1lll1ll_opy_.POST and callable(getattr(args[-1], bstack11l1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤዣ"), None)):
                    bstack1l1l1l1111l_opy_[bstack11l1111_opy_ (u"ࠨࡴࡺࡲࡨࠦዤ")] = TestFramework.bstack1lll1l11l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                bstack1l1l1l1111l_opy_[bstack11l1111_opy_ (u"ࠢࡶࡷ࡬ࡨࠧዥ")] = uuid4().__str__()
                bstack1l1l1l1111l_opy_[PytestBDDFramework.bstack1l1l1l1ll11_opy_] = bstack1l1l1l11ll1_opy_
            elif test_hook_state == bstack1lll1lll1ll_opy_.POST:
                bstack1l1l1l1111l_opy_[PytestBDDFramework.bstack1l1lll11l1l_opy_] = bstack1l1l1l11ll1_opy_
            if bstack1l1l1llllll_opy_ in bstack1l1ll11llll_opy_:
                bstack1l1ll11llll_opy_[bstack1l1l1llllll_opy_].update(bstack1l1l1l1111l_opy_)
                self.logger.debug(bstack11l1111_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤዦ") + str(bstack1l1ll11llll_opy_[bstack1l1l1llllll_opy_]) + bstack11l1111_opy_ (u"ࠤࠥዧ"))
            else:
                bstack1l1ll11llll_opy_[bstack1l1l1llllll_opy_] = bstack1l1l1l1111l_opy_
                self.logger.debug(bstack11l1111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨየ") + str(len(bstack1l1ll11llll_opy_)) + bstack11l1111_opy_ (u"ࠦࠧዩ"))
        TestFramework.bstack1llll111l11_opy_(instance, PytestBDDFramework.bstack1l1l1l1l1ll_opy_, bstack1l1ll11llll_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧዪ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠨࠢያ"))
        return instance
    def __1l1ll11111l_opy_(
        self,
        context: bstack1l1l1l1l1l1_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1l1lll111ll_opy_.create_context(target)
        ob = bstack1lllll111ll_opy_(ctx, self.bstack1l1l1lll111_opy_, self.bstack1l1lll1l11l_opy_, test_framework_state)
        TestFramework.bstack1l1ll1111ll_opy_(ob, {
            TestFramework.bstack1lll1ll1l11_opy_: context.test_framework_name,
            TestFramework.bstack1lll1l11ll1_opy_: context.test_framework_version,
            TestFramework.bstack1l1l1l111l1_opy_: [],
            PytestBDDFramework.bstack1l1l1l1l1ll_opy_: {},
            PytestBDDFramework.bstack1l1l1ll1l11_opy_: {},
            PytestBDDFramework.bstack1l1l1llll1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll111l11_opy_(ob, TestFramework.bstack1l1l1ll1l1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll111l11_opy_(ob, TestFramework.bstack1llllll1lll_opy_, context.platform_index)
        TestFramework.bstack1ll11llllll_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢዬ") + str(TestFramework.bstack1ll11llllll_opy_.keys()) + bstack11l1111_opy_ (u"ࠣࠤይ"))
        return ob
    @staticmethod
    def __1l1ll1l1111_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1111_opy_ (u"ࠩ࡬ࡨࠬዮ"): id(step),
                bstack11l1111_opy_ (u"ࠪࡸࡪࡾࡴࠨዯ"): step.name,
                bstack11l1111_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬደ"): step.keyword,
            })
        meta = {
            bstack11l1111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ዱ"): {
                bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫዲ"): feature.name,
                bstack11l1111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬዳ"): feature.filename,
                bstack11l1111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ዴ"): feature.description
            },
            bstack11l1111_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫድ"): {
                bstack11l1111_opy_ (u"ࠪࡲࡦࡳࡥࠨዶ"): scenario.name
            },
            bstack11l1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪዷ"): steps,
            bstack11l1111_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧዸ"): PytestBDDFramework.__1l1ll1ll11l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l1ll111lll_opy_: meta
            }
        )
    def bstack1l1ll1l1l11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧዹ")
        global _1llll11lll1_opy_
        platform_index = os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧዺ")]
        bstack1lllll1l111_opy_ = os.path.join(bstack1lllllll111_opy_, (bstack1111111lll_opy_ + str(platform_index)), bstack1l1lll1111l_opy_)
        if not os.path.exists(bstack1lllll1l111_opy_) or not os.path.isdir(bstack1lllll1l111_opy_):
            return
        logs = hook.get(bstack11l1111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨዻ"), [])
        with os.scandir(bstack1lllll1l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1llll11lll1_opy_:
                    self.logger.info(bstack11l1111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢዼ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1111_opy_ (u"ࠥࠦዽ")
                    log_entry = bstack1llll11ll1l_opy_(
                        kind=bstack11l1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨዾ"),
                        message=bstack11l1111_opy_ (u"ࠧࠨዿ"),
                        level=bstack11l1111_opy_ (u"ࠨࠢጀ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack111111l1l1_opy_=entry.stat().st_size,
                        bstack1llll1l1111_opy_=bstack11l1111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢጁ"),
                        bstack1ll1l_opy_=os.path.abspath(entry.path),
                        bstack1l1ll11l1l1_opy_=hook.get(TestFramework.bstack1l1l1l11lll_opy_)
                    )
                    logs.append(log_entry)
                    _1llll11lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨጂ")]
        bstack1l1ll1lllll_opy_ = os.path.join(bstack1lllllll111_opy_, (bstack1111111lll_opy_ + str(platform_index)), bstack1l1lll1111l_opy_, bstack1l1ll111ll1_opy_)
        if not os.path.exists(bstack1l1ll1lllll_opy_) or not os.path.isdir(bstack1l1ll1lllll_opy_):
            self.logger.info(bstack11l1111_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦጃ").format(bstack1l1ll1lllll_opy_))
        else:
            self.logger.info(bstack11l1111_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤጄ").format(bstack1l1ll1lllll_opy_))
            with os.scandir(bstack1l1ll1lllll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1llll11lll1_opy_:
                        self.logger.info(bstack11l1111_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤጅ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1111_opy_ (u"ࠧࠨጆ")
                        log_entry = bstack1llll11ll1l_opy_(
                            kind=bstack11l1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣጇ"),
                            message=bstack11l1111_opy_ (u"ࠢࠣገ"),
                            level=bstack11l1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧጉ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack111111l1l1_opy_=entry.stat().st_size,
                            bstack1llll1l1111_opy_=bstack11l1111_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤጊ"),
                            bstack1ll1l_opy_=os.path.abspath(entry.path),
                            bstack1llll111111_opy_=hook.get(TestFramework.bstack1l1l1l11lll_opy_)
                        )
                        logs.append(log_entry)
                        _1llll11lll1_opy_.add(abs_path)
        hook[bstack11l1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣጋ")] = logs
    def bstack1lll1ll111l_opy_(
        self,
        bstack1llllll111l_opy_: bstack1lllll111ll_opy_,
        entries: List[bstack1llll11ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣጌ"))
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1llllll1lll_opy_)
        req.execution_context.hash = str(bstack1llllll111l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1llllll111l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1llllll111l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1lll1ll1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1lll1l11ll1_opy_)
            log_entry.uuid = entry.bstack1l1ll11l1l1_opy_
            log_entry.test_framework_state = bstack1llllll111l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1111_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦግ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l1111_opy_ (u"ࠨࠢጎ")
            if entry.kind == bstack11l1111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤጏ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack111111l1l1_opy_
                log_entry.file_path = entry.bstack1ll1l_opy_
        def bstack1llll1l11ll_opy_():
            bstack1ll1l1l1_opy_ = datetime.now()
            try:
                self.bstack1lll1llll1l_opy_.LogCreatedEvent(req)
                bstack1llllll111l_opy_.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧጐ"), datetime.now() - bstack1ll1l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣ጑").format(str(e)))
                traceback.print_exc()
        self.bstack1llll1l1l1l_opy_.enqueue(bstack1llll1l11ll_opy_)
    def __1l1ll1l11l1_opy_(self, instance) -> None:
        bstack11l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣጒ")
        bstack1l1l1l11l11_opy_ = {bstack11l1111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨጓ"): bstack1l1lll1l1ll_opy_.bstack1l1ll1l1lll_opy_()}
        TestFramework.bstack1l1ll1111ll_opy_(instance, bstack1l1l1l11l11_opy_)
    @staticmethod
    def __1l1llll1l1l_opy_(instance, args):
        request, bstack1l1ll1111l1_opy_ = args
        bstack1l1lll11l11_opy_ = id(bstack1l1ll1111l1_opy_)
        bstack1l1lll11111_opy_ = instance.data[TestFramework.bstack1l1ll111lll_opy_]
        step = next(filter(lambda st: st[bstack11l1111_opy_ (u"ࠬ࡯ࡤࠨጔ")] == bstack1l1lll11l11_opy_, bstack1l1lll11111_opy_[bstack11l1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬጕ")]), None)
        step.update({
            bstack11l1111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ጖"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l1lll11111_opy_[bstack11l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ጗")]) if st[bstack11l1111_opy_ (u"ࠩ࡬ࡨࠬጘ")] == step[bstack11l1111_opy_ (u"ࠪ࡭ࡩ࠭ጙ")]), None)
        if index is not None:
            bstack1l1lll11111_opy_[bstack11l1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪጚ")][index] = step
        instance.data[TestFramework.bstack1l1ll111lll_opy_] = bstack1l1lll11111_opy_
    @staticmethod
    def __1l1lll1l111_opy_(instance, args):
        bstack11l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡬ࡪࡴࠠ࡭ࡧࡱࠤࡦࡸࡧࡴࠢ࡬ࡷࠥ࠸ࠬࠡ࡫ࡷࠤࡸ࡯ࡧ࡯࡫ࡩ࡭ࡪࡹࠠࡵࡪࡨࡶࡪࠦࡩࡴࠢࡱࡳࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠯ࠣ࡟ࡷ࡫ࡱࡶࡧࡶࡸ࠱ࠦࡳࡵࡧࡳࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࡤࡶ࡬ࡹࠠࡢࡴࡨࠤ࠸ࠦࡴࡩࡧࡱࠤࡹ࡮ࡥࠡ࡮ࡤࡷࡹࠦࡶࡢ࡮ࡸࡩࠥ࡯ࡳࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣጛ")
        bstack1l1ll1lll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1ll1111l1_opy_ = args[1]
        bstack1l1lll11l11_opy_ = id(bstack1l1ll1111l1_opy_)
        bstack1l1lll11111_opy_ = instance.data[TestFramework.bstack1l1ll111lll_opy_]
        step = None
        if bstack1l1lll11l11_opy_ is not None and bstack1l1lll11111_opy_.get(bstack11l1111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬጜ")):
            step = next(filter(lambda st: st[bstack11l1111_opy_ (u"ࠧࡪࡦࠪጝ")] == bstack1l1lll11l11_opy_, bstack1l1lll11111_opy_[bstack11l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧጞ")]), None)
            step.update({
                bstack11l1111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧጟ"): bstack1l1ll1lll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11l1111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪጠ"): bstack11l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጡ"),
                bstack11l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ጢ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11l1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ጣ"): bstack11l1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧጤ"),
                })
        index = next((i for i, st in enumerate(bstack1l1lll11111_opy_[bstack11l1111_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧጥ")]) if st[bstack11l1111_opy_ (u"ࠩ࡬ࡨࠬጦ")] == step[bstack11l1111_opy_ (u"ࠪ࡭ࡩ࠭ጧ")]), None)
        if index is not None:
            bstack1l1lll11111_opy_[bstack11l1111_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪጨ")][index] = step
        instance.data[TestFramework.bstack1l1ll111lll_opy_] = bstack1l1lll11111_opy_
    @staticmethod
    def __1l1ll1ll11l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11l1111_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧጩ")):
                examples = list(node.callspec.params[bstack11l1111_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬጪ")].values())
            return examples
        except:
            return []
    def bstack1llll11ll11_opy_(self, instance: bstack1lllll111ll_opy_, bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_]):
        bstack1l1l1l1llll_opy_ = (
            PytestBDDFramework.bstack1l1ll1ll1ll_opy_
            if bstack1llll11l111_opy_[1] == bstack1lll1lll1ll_opy_.PRE
            else PytestBDDFramework.bstack1l1ll1ll111_opy_
        )
        hook = PytestBDDFramework.bstack1l1l1lll11l_opy_(instance, bstack1l1l1l1llll_opy_)
        entries = hook.get(TestFramework.bstack1l1l1ll1ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, []))
        return entries
    def bstack1llll111ll1_opy_(self, instance: bstack1lllll111ll_opy_, bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_]):
        bstack1l1l1l1llll_opy_ = (
            PytestBDDFramework.bstack1l1ll1ll1ll_opy_
            if bstack1llll11l111_opy_[1] == bstack1lll1lll1ll_opy_.PRE
            else PytestBDDFramework.bstack1l1ll1ll111_opy_
        )
        PytestBDDFramework.bstack1l1ll1l11ll_opy_(instance, bstack1l1l1l1llll_opy_)
        TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, []).clear()
    @staticmethod
    def bstack1l1l1lll11l_opy_(instance: bstack1lllll111ll_opy_, bstack1l1l1l1llll_opy_: str):
        bstack1l1ll1llll1_opy_ = (
            PytestBDDFramework.bstack1l1l1ll1l11_opy_
            if bstack1l1l1l1llll_opy_ == PytestBDDFramework.bstack1l1ll1ll111_opy_
            else PytestBDDFramework.bstack1l1l1llll1l_opy_
        )
        bstack1l1ll111l1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1l1l1llll_opy_, None)
        bstack1l1l1ll1111_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1ll1llll1_opy_, None) if bstack1l1ll111l1l_opy_ else None
        return (
            bstack1l1l1ll1111_opy_[bstack1l1ll111l1l_opy_][-1]
            if isinstance(bstack1l1l1ll1111_opy_, dict) and len(bstack1l1l1ll1111_opy_.get(bstack1l1ll111l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l1ll1l11ll_opy_(instance: bstack1lllll111ll_opy_, bstack1l1l1l1llll_opy_: str):
        hook = PytestBDDFramework.bstack1l1l1lll11l_opy_(instance, bstack1l1l1l1llll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1l1ll1ll1_opy_, []).clear()
    @staticmethod
    def __1l1llll111l_opy_(instance: bstack1lllll111ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧጫ"), None)):
            return
        if os.getenv(bstack11l1111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧጬ"), bstack11l1111_opy_ (u"ࠤ࠴ࠦጭ")) != bstack11l1111_opy_ (u"ࠥ࠵ࠧጮ"):
            PytestBDDFramework.logger.warning(bstack11l1111_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨጯ"))
            return
        bstack1l1ll11l11l_opy_ = {
            bstack11l1111_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦጰ"): (PytestBDDFramework.bstack1l1ll1ll1ll_opy_, PytestBDDFramework.bstack1l1l1llll1l_opy_),
            bstack11l1111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣጱ"): (PytestBDDFramework.bstack1l1ll1ll111_opy_, PytestBDDFramework.bstack1l1l1ll1l11_opy_),
        }
        for when in (bstack11l1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨጲ"), bstack11l1111_opy_ (u"ࠣࡥࡤࡰࡱࠨጳ"), bstack11l1111_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦጴ")):
            bstack1l1l1ll11l1_opy_ = args[1].get_records(when)
            if not bstack1l1l1ll11l1_opy_:
                continue
            records = [
                bstack1llll11ll1l_opy_(
                    kind=TestFramework.bstack1lllllll11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1111_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨጵ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧጶ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1l1ll11l1_opy_
                if isinstance(getattr(r, bstack11l1111_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨጷ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l1llll1l11_opy_, bstack1l1ll1llll1_opy_ = bstack1l1ll11l11l_opy_.get(when, (None, None))
            bstack1l1llll11ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1llll1l11_opy_, None) if bstack1l1llll1l11_opy_ else None
            bstack1l1l1ll1111_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1ll1llll1_opy_, None) if bstack1l1llll11ll_opy_ else None
            if isinstance(bstack1l1l1ll1111_opy_, dict) and len(bstack1l1l1ll1111_opy_.get(bstack1l1llll11ll_opy_, [])) > 0:
                hook = bstack1l1l1ll1111_opy_[bstack1l1llll11ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1l1ll1ll1_opy_ in hook:
                    hook[TestFramework.bstack1l1l1ll1ll1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1l1l11111_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1ll111lll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1ll111l11_opy_(request.node, scenario)
        bstack1l1ll11ll1l_opy_ = feature.filename
        if not bstack1ll111lll1_opy_ or not test_name or not bstack1l1ll11ll1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1lll1l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1ll11l111_opy_: bstack1ll111lll1_opy_,
            TestFramework.bstack1lll11lllll_opy_: test_name,
            TestFramework.bstack1lll11l1l1l_opy_: bstack1ll111lll1_opy_,
            TestFramework.bstack1l1l1l1l11l_opy_: bstack1l1ll11ll1l_opy_,
            TestFramework.bstack1l1lll1ll1l_opy_: PytestBDDFramework.__1l1ll11lll1_opy_(feature, scenario),
            TestFramework.bstack1l1ll1l1l1l_opy_: code,
            TestFramework.bstack1ll1l11l111_opy_: TestFramework.bstack1l1lll11ll1_opy_,
            TestFramework.bstack1ll1111lll1_opy_: test_name
        }
    @staticmethod
    def __1l1ll111l11_opy_(node, scenario):
        if hasattr(node, bstack11l1111_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨጸ")):
            parts = node.nodeid.rsplit(bstack11l1111_opy_ (u"ࠢ࡜ࠤጹ"))
            params = parts[-1]
            return bstack11l1111_opy_ (u"ࠣࡽࢀࠤࡠࢁࡽࠣጺ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l1ll11lll1_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11l1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧጻ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11l1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨጼ")) else [])
    @staticmethod
    def __1l1l1l1l111_opy_(location):
        return bstack11l1111_opy_ (u"ࠦ࠿ࡀࠢጽ").join(filter(lambda x: isinstance(x, str), location))