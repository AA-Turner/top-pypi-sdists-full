# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1lllll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l1l11_opy_ import bstack1l111l1l111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1ll111l_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1lll1111l1l_opy_,
    bstack1l111l11l11_opy_,
    bstack1lll111ll1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1ll1l11l1_opy_
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111ll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1lll_opy_ import bstack1llll1l11l1_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack1l1111l1_opy_
bstack1l1l1llll11_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l11111l1l1_opy_ = 1.0
bstack1l1l1ll1ll1_opy_ = bstack11ll1l1_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᒗ")
bstack11llllll1ll_opy_ = bstack11ll1l1_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᒘ")
bstack11lllll1lll_opy_ = bstack11ll1l1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᒙ")
bstack11lllll1ll1_opy_ = bstack11ll1l1_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᒚ")
bstack11llllll11l_opy_ = bstack11ll1l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᒛ")
_1l1ll11l1l1_opy_ = set()
class bstack1ll1llll1ll_opy_(TestFramework):
    bstack1l111lllll1_opy_ = bstack11ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᒜ")
    bstack1l111111111_opy_ = bstack11ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᒝ")
    bstack11lllllll11_opy_ = bstack11ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᒞ")
    bstack1l1111111ll_opy_ = bstack11ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᒟ")
    bstack1l11111ll11_opy_ = bstack11ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᒠ")
    bstack1l111l111l1_opy_: bool
    bstack111111lll1_opy_: bstack111111ll11_opy_  = None
    bstack1lll1l1ll1l_opy_ = None
    bstack1l111l1lll1_opy_ = [
        bstack1lll1ll111l_opy_.BEFORE_ALL,
        bstack1lll1ll111l_opy_.AFTER_ALL,
        bstack1lll1ll111l_opy_.BEFORE_EACH,
        bstack1lll1ll111l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1111l11l1_opy_: Dict[str, str],
        bstack1ll11l1l1ll_opy_: List[str]=[bstack11ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᒡ")],
        bstack111111lll1_opy_: bstack111111ll11_opy_=None,
        bstack1lll1l1ll1l_opy_=None
    ):
        super().__init__(bstack1ll11l1l1ll_opy_, bstack1l1111l11l1_opy_, bstack111111lll1_opy_)
        self.bstack1l111l111l1_opy_ = any(bstack11ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᒢ") in item.lower() for item in bstack1ll11l1l1ll_opy_)
        self.bstack1lll1l1ll1l_opy_ = bstack1lll1l1ll1l_opy_
    def track_event(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1ll111l_opy_.TEST or test_framework_state in bstack1ll1llll1ll_opy_.bstack1l111l1lll1_opy_:
            bstack1l111l1l111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1ll111l_opy_.NONE:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᒣ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠨࠢᒤ"))
            return
        if not self.bstack1l111l111l1_opy_:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᒥ") + str(str(self.bstack1ll11l1l1ll_opy_)) + bstack11ll1l1_opy_ (u"ࠣࠤᒦ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᒧ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠥࠦᒨ"))
            return
        instance = self.__1l1111ll111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᒩ") + str(args) + bstack11ll1l1_opy_ (u"ࠧࠨᒪ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1llll1ll_opy_.bstack1l111l1lll1_opy_ and test_hook_state == bstack1lll1111l1l_opy_.PRE:
                bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack11l1111ll1_opy_.value)
                name = str(EVENTS.bstack11l1111ll1_opy_.name)+bstack11ll1l1_opy_ (u"ࠨ࠺ࠣᒫ")+str(test_framework_state.name)
                TestFramework.bstack1l1111lll1l_opy_(instance, name, bstack1ll11l111ll_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴࠣࡴࡷ࡫࠺ࠡࡽࢀࠦᒬ").format(e))
        try:
            if not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l111l11lll_opy_) and test_hook_state == bstack1lll1111l1l_opy_.PRE:
                test = bstack1ll1llll1ll_opy_.__1l111111ll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠣ࡮ࡲࡥࡩ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᒭ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠤࠥᒮ"))
            if test_framework_state == bstack1lll1ll111l_opy_.TEST:
                if test_hook_state == bstack1lll1111l1l_opy_.PRE and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll11ll1_opy_):
                    TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1lll11ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᒯ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠦࠧᒰ"))
                elif test_hook_state == bstack1lll1111l1l_opy_.POST and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1l1lll111_opy_):
                    TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᒱ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠨࠢᒲ"))
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG and test_hook_state == bstack1lll1111l1l_opy_.POST:
                bstack1ll1llll1ll_opy_.__1l111111lll_opy_(instance, *args)
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG_REPORT and test_hook_state == bstack1lll1111l1l_opy_.POST:
                self.__1l111l11l1l_opy_(instance, *args)
                self.__1l11l1111ll_opy_(instance)
            elif test_framework_state in bstack1ll1llll1ll_opy_.bstack1l111l1lll1_opy_:
                self.__1l11111111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᒳ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠣࠤᒴ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111111l1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1llll1ll_opy_.bstack1l111l1lll1_opy_ and test_hook_state == bstack1lll1111l1l_opy_.POST:
                name = str(EVENTS.bstack11l1111ll1_opy_.name)+bstack11ll1l1_opy_ (u"ࠤ࠽ࠦᒵ")+str(test_framework_state.name)
                bstack1ll11l111ll_opy_ = TestFramework.bstack1l111lll111_opy_(instance, name)
                bstack1llll11lll1_opy_.end(EVENTS.bstack11l1111ll1_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᒶ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᒷ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᒸ").format(e))
    def bstack1l1l1lll1l1_opy_(self):
        return self.bstack1l111l111l1_opy_
    def __1l1111l111l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᒹ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll1l1l1l_opy_(rep, [bstack11ll1l1_opy_ (u"ࠢࡸࡪࡨࡲࠧᒺ"), bstack11ll1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᒻ"), bstack11ll1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᒼ"), bstack11ll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᒽ"), bstack11ll1l1_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᒾ"), bstack11ll1l1_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᒿ")])
        return None
    def __1l111l11l1l_opy_(self, instance: bstack1ll1l1lll1l_opy_, *args):
        result = self.__1l1111l111l_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l1111_opy_ = None
        if result.get(bstack11ll1l1_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᓀ"), None) == bstack11ll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᓁ") and len(args) > 1 and getattr(args[1], bstack11ll1l1_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᓂ"), None) is not None:
            failure = [{bstack11ll1l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᓃ"): [args[1].excinfo.exconly(), result.get(bstack11ll1l1_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᓄ"), None)]}]
            bstack11111l1111_opy_ = bstack11ll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᓅ") if bstack11ll1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᓆ") in getattr(args[1].excinfo, bstack11ll1l1_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᓇ"), bstack11ll1l1_opy_ (u"ࠢࠣᓈ")) else bstack11ll1l1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᓉ")
        bstack1l111ll1lll_opy_ = result.get(bstack11ll1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᓊ"), TestFramework.bstack1l111l1l11l_opy_)
        if bstack1l111ll1lll_opy_ != TestFramework.bstack1l111l1l11l_opy_:
            TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111l1l1l_opy_(instance, {
            TestFramework.bstack1l1l111l1ll_opy_: failure,
            TestFramework.bstack1l11111l11l_opy_: bstack11111l1111_opy_,
            TestFramework.bstack1l1l111ll1l_opy_: bstack1l111ll1lll_opy_,
        })
    def __1l1111ll111_opy_(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1ll111l_opy_.SETUP_FIXTURE:
            instance = self.__11llllllll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll11ll_opy_ bstack1l1111lllll_opy_ this to be bstack11ll1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᓋ")
            if test_framework_state == bstack1lll1ll111l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111ll11l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll1l1_opy_ (u"ࠦࡳࡵࡤࡦࠤᓌ"), None), bstack11ll1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᓍ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᓎ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll11111_opy_(target) if target else None
        return instance
    def __1l11111111l_opy_(
        self,
        instance: bstack1ll1l1lll1l_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111lll1ll_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1ll1llll1ll_opy_.bstack1l111111111_opy_, {})
        if not key in bstack1l111lll1ll_opy_:
            bstack1l111lll1ll_opy_[key] = []
        bstack1l11l111l1l_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1ll1llll1ll_opy_.bstack11lllllll11_opy_, {})
        if not key in bstack1l11l111l1l_opy_:
            bstack1l11l111l1l_opy_[key] = []
        bstack1l111ll1l1l_opy_ = {
            bstack1ll1llll1ll_opy_.bstack1l111111111_opy_: bstack1l111lll1ll_opy_,
            bstack1ll1llll1ll_opy_.bstack11lllllll11_opy_: bstack1l11l111l1l_opy_,
        }
        if test_hook_state == bstack1lll1111l1l_opy_.PRE:
            hook = {
                bstack11ll1l1_opy_ (u"ࠢ࡬ࡧࡼࠦᓏ"): key,
                TestFramework.bstack1l111ll111l_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111llll1_opy_: TestFramework.bstack1l111l11111_opy_,
                TestFramework.bstack1l111l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l111lll_opy_: [],
                TestFramework.bstack1l111ll1111_opy_: args[1] if len(args) > 1 else bstack11ll1l1_opy_ (u"ࠨࠩᓐ"),
                TestFramework.bstack1l11111llll_opy_: bstack1llll1l11l1_opy_.bstack1l11l111l11_opy_()
            }
            bstack1l111lll1ll_opy_[key].append(hook)
            bstack1l111ll1l1l_opy_[bstack1ll1llll1ll_opy_.bstack1l1111111ll_opy_] = key
        elif test_hook_state == bstack1lll1111l1l_opy_.POST:
            bstack1l11l11ll11_opy_ = bstack1l111lll1ll_opy_.get(key, [])
            hook = bstack1l11l11ll11_opy_.pop() if bstack1l11l11ll11_opy_ else None
            if hook:
                result = self.__1l1111l111l_opy_(*args)
                if result:
                    bstack1l111111l11_opy_ = result.get(bstack11ll1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᓑ"), TestFramework.bstack1l111l11111_opy_)
                    if bstack1l111111l11_opy_ != TestFramework.bstack1l111l11111_opy_:
                        hook[TestFramework.bstack1l1111llll1_opy_] = bstack1l111111l11_opy_
                hook[TestFramework.bstack1l1111lll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11111llll_opy_]= bstack1llll1l11l1_opy_.bstack1l11l111l11_opy_()
                self.bstack1l11l11l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111lll11l_opy_, [])
                if logs: self.bstack1l1ll11l11l_opy_(instance, logs)
                bstack1l11l111l1l_opy_[key].append(hook)
                bstack1l111ll1l1l_opy_[bstack1ll1llll1ll_opy_.bstack1l11111ll11_opy_] = key
        TestFramework.bstack1l1111l1l1l_opy_(instance, bstack1l111ll1l1l_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᓒ") + str(bstack1l11l111l1l_opy_) + bstack11ll1l1_opy_ (u"ࠦࠧᓓ"))
    def __11llllllll1_opy_(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        test_hook_state: bstack1lll1111l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll1l1l1l_opy_(args[0], [bstack11ll1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᓔ"), bstack11ll1l1_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᓕ"), bstack11ll1l1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᓖ"), bstack11ll1l1_opy_ (u"ࠣ࡫ࡧࡷࠧᓗ"), bstack11ll1l1_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᓘ"), bstack11ll1l1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᓙ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11ll1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᓚ")) else fixturedef.get(bstack11ll1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᓛ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll1l1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᓜ")) else None
        node = request.node if hasattr(request, bstack11ll1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᓝ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᓞ")) else None
        baseid = fixturedef.get(bstack11ll1l1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᓟ"), None) or bstack11ll1l1_opy_ (u"ࠥࠦᓠ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll1l1_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᓡ")):
            target = bstack1ll1llll1ll_opy_.__1l11111l111_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll1l1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᓢ")) else None
            if target and not TestFramework.bstack1lllll11111_opy_(target):
                self.__1l111ll11l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᓣ") + str(test_hook_state) + bstack11ll1l1_opy_ (u"ࠢࠣᓤ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᓥ") + str(target) + bstack11ll1l1_opy_ (u"ࠤࠥᓦ"))
            return None
        instance = TestFramework.bstack1lllll11111_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᓧ") + str(target) + bstack11ll1l1_opy_ (u"ࠦࠧᓨ"))
            return None
        bstack1l111ll1ll1_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1ll1llll1ll_opy_.bstack1l111lllll1_opy_, {})
        if os.getenv(bstack11ll1l1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᓩ"), bstack11ll1l1_opy_ (u"ࠨ࠱ࠣᓪ")) == bstack11ll1l1_opy_ (u"ࠢ࠲ࠤᓫ"):
            bstack1l1111ll1l1_opy_ = bstack11ll1l1_opy_ (u"ࠣ࠼ࠥᓬ").join((scope, fixturename))
            bstack1l11l11111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111l111ll_opy_ = {
                bstack11ll1l1_opy_ (u"ࠤ࡮ࡩࡾࠨᓭ"): bstack1l1111ll1l1_opy_,
                bstack11ll1l1_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᓮ"): bstack1ll1llll1ll_opy_.__1l111l1l1ll_opy_(request.node),
                bstack11ll1l1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᓯ"): fixturedef,
                bstack11ll1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᓰ"): scope,
                bstack11ll1l1_opy_ (u"ࠨࡴࡺࡲࡨࠦᓱ"): None,
            }
            try:
                if test_hook_state == bstack1lll1111l1l_opy_.POST and callable(getattr(args[-1], bstack11ll1l1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᓲ"), None)):
                    bstack1l111l111ll_opy_[bstack11ll1l1_opy_ (u"ࠣࡶࡼࡴࡪࠨᓳ")] = TestFramework.bstack1l1ll1ll1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1111l1l_opy_.PRE:
                bstack1l111l111ll_opy_[bstack11ll1l1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᓴ")] = uuid4().__str__()
                bstack1l111l111ll_opy_[bstack1ll1llll1ll_opy_.bstack1l111l1ll11_opy_] = bstack1l11l11111l_opy_
            elif test_hook_state == bstack1lll1111l1l_opy_.POST:
                bstack1l111l111ll_opy_[bstack1ll1llll1ll_opy_.bstack1l1111lll11_opy_] = bstack1l11l11111l_opy_
            if bstack1l1111ll1l1_opy_ in bstack1l111ll1ll1_opy_:
                bstack1l111ll1ll1_opy_[bstack1l1111ll1l1_opy_].update(bstack1l111l111ll_opy_)
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᓵ") + str(bstack1l111ll1ll1_opy_[bstack1l1111ll1l1_opy_]) + bstack11ll1l1_opy_ (u"ࠦࠧᓶ"))
            else:
                bstack1l111ll1ll1_opy_[bstack1l1111ll1l1_opy_] = bstack1l111l111ll_opy_
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᓷ") + str(len(bstack1l111ll1ll1_opy_)) + bstack11ll1l1_opy_ (u"ࠨࠢᓸ"))
        TestFramework.bstack1lllll1ll1l_opy_(instance, bstack1ll1llll1ll_opy_.bstack1l111lllll1_opy_, bstack1l111ll1ll1_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᓹ") + str(instance.ref()) + bstack11ll1l1_opy_ (u"ࠣࠤᓺ"))
        return instance
    def __1l111ll11l1_opy_(
        self,
        context: bstack1l111l11l11_opy_,
        test_framework_state: bstack1lll1ll111l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lllll11l11_opy_.create_context(target)
        ob = bstack1ll1l1lll1l_opy_(ctx, self.bstack1ll11l1l1ll_opy_, self.bstack1l1111l11l1_opy_, test_framework_state)
        TestFramework.bstack1l1111l1l1l_opy_(ob, {
            TestFramework.bstack1ll11lll111_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1111l1_opy_: context.test_framework_version,
            TestFramework.bstack11lllllll1l_opy_: [],
            bstack1ll1llll1ll_opy_.bstack1l111lllll1_opy_: {},
            bstack1ll1llll1ll_opy_.bstack11lllllll11_opy_: {},
            bstack1ll1llll1ll_opy_.bstack1l111111111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllll1ll1l_opy_(ob, TestFramework.bstack11lllllllll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllll1ll1l_opy_(ob, TestFramework.bstack1ll111ll11l_opy_, context.platform_index)
        TestFramework.bstack1llllll11l1_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᓻ") + str(TestFramework.bstack1llllll11l1_opy_.keys()) + bstack11ll1l1_opy_ (u"ࠥࠦᓼ"))
        return ob
    def bstack1l1ll1l111l_opy_(self, instance: bstack1ll1l1lll1l_opy_, bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_]):
        bstack1l111l1l1l1_opy_ = (
            bstack1ll1llll1ll_opy_.bstack1l1111111ll_opy_
            if bstack1llllllllll_opy_[1] == bstack1lll1111l1l_opy_.PRE
            else bstack1ll1llll1ll_opy_.bstack1l11111ll11_opy_
        )
        hook = bstack1ll1llll1ll_opy_.bstack1l11l1111l1_opy_(instance, bstack1l111l1l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11l111lll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []))
        return entries
    def bstack1l1ll11l111_opy_(self, instance: bstack1ll1l1lll1l_opy_, bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_]):
        bstack1l111l1l1l1_opy_ = (
            bstack1ll1llll1ll_opy_.bstack1l1111111ll_opy_
            if bstack1llllllllll_opy_[1] == bstack1lll1111l1l_opy_.PRE
            else bstack1ll1llll1ll_opy_.bstack1l11111ll11_opy_
        )
        bstack1ll1llll1ll_opy_.bstack1l111llllll_opy_(instance, bstack1l111l1l1l1_opy_)
        TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []).clear()
    def bstack1l11l11l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᓽ")
        global _1l1ll11l1l1_opy_
        platform_index = os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᓾ")]
        bstack1l1lll1l11l_opy_ = os.path.join(bstack1l1l1llll11_opy_, (bstack1l1l1ll1ll1_opy_ + str(platform_index)), bstack11lllll1ll1_opy_)
        if not os.path.exists(bstack1l1lll1l11l_opy_) or not os.path.isdir(bstack1l1lll1l11l_opy_):
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦᓿ").format(bstack1l1lll1l11l_opy_))
            return
        logs = hook.get(bstack11ll1l1_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᔀ"), [])
        with os.scandir(bstack1l1lll1l11l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll11l1l1_opy_:
                    self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᔁ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll1l1_opy_ (u"ࠤࠥᔂ")
                    log_entry = bstack1lll111ll1l_opy_(
                        kind=bstack11ll1l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᔃ"),
                        message=bstack11ll1l1_opy_ (u"ࠦࠧᔄ"),
                        level=bstack11ll1l1_opy_ (u"ࠧࠨᔅ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll1llll_opy_=entry.stat().st_size,
                        bstack1l1ll1lllll_opy_=bstack11ll1l1_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᔆ"),
                        bstack11111ll_opy_=os.path.abspath(entry.path),
                        bstack1l111l1llll_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll11l1l1_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᔇ")]
        bstack1l11l11l1ll_opy_ = os.path.join(bstack1l1l1llll11_opy_, (bstack1l1l1ll1ll1_opy_ + str(platform_index)), bstack11lllll1ll1_opy_, bstack11llllll11l_opy_)
        if not os.path.exists(bstack1l11l11l1ll_opy_) or not os.path.isdir(bstack1l11l11l1ll_opy_):
            self.logger.info(bstack11ll1l1_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᔈ").format(bstack1l11l11l1ll_opy_))
        else:
            self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᔉ").format(bstack1l11l11l1ll_opy_))
            with os.scandir(bstack1l11l11l1ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll11l1l1_opy_:
                        self.logger.info(bstack11ll1l1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᔊ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll1l1_opy_ (u"ࠦࠧᔋ")
                        log_entry = bstack1lll111ll1l_opy_(
                            kind=bstack11ll1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᔌ"),
                            message=bstack11ll1l1_opy_ (u"ࠨࠢᔍ"),
                            level=bstack11ll1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᔎ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll1llll_opy_=entry.stat().st_size,
                            bstack1l1ll1lllll_opy_=bstack11ll1l1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᔏ"),
                            bstack11111ll_opy_=os.path.abspath(entry.path),
                            bstack1l1llll111l_opy_=hook.get(TestFramework.bstack1l111ll111l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll11l1l1_opy_.add(abs_path)
        hook[bstack11ll1l1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᔐ")] = logs
    def bstack1l1ll11l11l_opy_(
        self,
        bstack1l1lll1l1l1_opy_: bstack1ll1l1lll1l_opy_,
        entries: List[bstack1lll111ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᔑ"))
        req.platform_index = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll111ll11l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11lll111_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1ll1111l1_opy_)
            log_entry.uuid = entry.bstack1l111l1llll_opy_
            log_entry.test_framework_state = bstack1l1lll1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᔒ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll1l1_opy_ (u"ࠧࠨᔓ")
            if entry.kind == bstack11ll1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᔔ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1llll_opy_
                log_entry.file_path = entry.bstack11111ll_opy_
        def bstack1l1ll1l1l11_opy_():
            bstack11ll11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1ll1l_opy_.LogCreatedEvent(req)
                bstack1l1lll1l1l1_opy_.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᔕ"), datetime.now() - bstack11ll11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᔖ").format(str(e)))
                traceback.print_exc()
        self.bstack111111lll1_opy_.enqueue(bstack1l1ll1l1l11_opy_)
    def __1l11l1111ll_opy_(self, instance) -> None:
        bstack11ll1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᔗ")
        bstack1l111ll1l1l_opy_ = {bstack11ll1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᔘ"): bstack1llll1l11l1_opy_.bstack1l11l111l11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1111l1l1l_opy_(instance, bstack1l111ll1l1l_opy_)
    @staticmethod
    def bstack1l11l1111l1_opy_(instance: bstack1ll1l1lll1l_opy_, bstack1l111l1l1l1_opy_: str):
        bstack1l111l1ll1l_opy_ = (
            bstack1ll1llll1ll_opy_.bstack11lllllll11_opy_
            if bstack1l111l1l1l1_opy_ == bstack1ll1llll1ll_opy_.bstack1l11111ll11_opy_
            else bstack1ll1llll1ll_opy_.bstack1l111111111_opy_
        )
        bstack1l1111ll1ll_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l111l1l1l1_opy_, None)
        bstack1l111llll11_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l111l1ll1l_opy_, None) if bstack1l1111ll1ll_opy_ else None
        return (
            bstack1l111llll11_opy_[bstack1l1111ll1ll_opy_][-1]
            if isinstance(bstack1l111llll11_opy_, dict) and len(bstack1l111llll11_opy_.get(bstack1l1111ll1ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111llllll_opy_(instance: bstack1ll1l1lll1l_opy_, bstack1l111l1l1l1_opy_: str):
        hook = bstack1ll1llll1ll_opy_.bstack1l11l1111l1_opy_(instance, bstack1l111l1l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l111lll_opy_, []).clear()
    @staticmethod
    def __1l111111lll_opy_(instance: bstack1ll1l1lll1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᔙ"), None)):
            return
        if os.getenv(bstack11ll1l1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᔚ"), bstack11ll1l1_opy_ (u"ࠨ࠱ࠣᔛ")) != bstack11ll1l1_opy_ (u"ࠢ࠲ࠤᔜ"):
            bstack1ll1llll1ll_opy_.logger.warning(bstack11ll1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᔝ"))
            return
        bstack1l1111l1111_opy_ = {
            bstack11ll1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᔞ"): (bstack1ll1llll1ll_opy_.bstack1l1111111ll_opy_, bstack1ll1llll1ll_opy_.bstack1l111111111_opy_),
            bstack11ll1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᔟ"): (bstack1ll1llll1ll_opy_.bstack1l11111ll11_opy_, bstack1ll1llll1ll_opy_.bstack11lllllll11_opy_),
        }
        for when in (bstack11ll1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᔠ"), bstack11ll1l1_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᔡ"), bstack11ll1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᔢ")):
            bstack1l111ll1l11_opy_ = args[1].get_records(when)
            if not bstack1l111ll1l11_opy_:
                continue
            records = [
                bstack1lll111ll1l_opy_(
                    kind=TestFramework.bstack1l1ll11ll1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll1l1_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᔣ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll1l1_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᔤ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll1l11_opy_
                if isinstance(getattr(r, bstack11ll1l1_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᔥ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l111111_opy_, bstack1l111l1ll1l_opy_ = bstack1l1111l1111_opy_.get(when, (None, None))
            bstack1l111l11ll1_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l11l111111_opy_, None) if bstack1l11l111111_opy_ else None
            bstack1l111llll11_opy_ = TestFramework.bstack11111111ll_opy_(instance, bstack1l111l1ll1l_opy_, None) if bstack1l111l11ll1_opy_ else None
            if isinstance(bstack1l111llll11_opy_, dict) and len(bstack1l111llll11_opy_.get(bstack1l111l11ll1_opy_, [])) > 0:
                hook = bstack1l111llll11_opy_[bstack1l111l11ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l111lll_opy_ in hook:
                    hook[TestFramework.bstack1l11l111lll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111111ll1_opy_(test) -> Dict[str, Any]:
        bstack1111ll1ll_opy_ = bstack1ll1llll1ll_opy_.__1l11111l111_opy_(test.location) if hasattr(test, bstack11ll1l1_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᔦ")) else getattr(test, bstack11ll1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᔧ"), None)
        test_name = test.name if hasattr(test, bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᔨ")) else None
        bstack1l11l11l111_opy_ = test.fspath.strpath if hasattr(test, bstack11ll1l1_opy_ (u"ࠨࡦࡴࡲࡤࡸ࡭ࠨᔩ")) and test.fspath else None
        if not bstack1111ll1ll_opy_ or not test_name or not bstack1l11l11l111_opy_:
            return None
        code = None
        if hasattr(test, bstack11ll1l1_opy_ (u"ࠢࡰࡤ࡭ࠦᔪ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11llllll1l1_opy_ = []
        try:
            bstack11llllll1l1_opy_ = bstack1l1111l1_opy_.bstack1111lllll1_opy_(test)
        except:
            bstack1ll1llll1ll_opy_.logger.warning(bstack11ll1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠬࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡳࡧࡶࡳࡱࡼࡥࡥࠢ࡬ࡲࠥࡉࡌࡊࠤᔫ"))
        return {
            TestFramework.bstack1ll11l11l11_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l11lll_opy_: bstack1111ll1ll_opy_,
            TestFramework.bstack1ll11ll11l1_opy_: test_name,
            TestFramework.bstack1l1l1l1l111_opy_: getattr(test, bstack11ll1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᔬ"), None),
            TestFramework.bstack1l1111ll11l_opy_: bstack1l11l11l111_opy_,
            TestFramework.bstack1l1111l11ll_opy_: bstack1ll1llll1ll_opy_.__1l111l1l1ll_opy_(test),
            TestFramework.bstack1l1111111l1_opy_: code,
            TestFramework.bstack1l1l111ll1l_opy_: TestFramework.bstack1l111l1l11l_opy_,
            TestFramework.bstack1l11l1ll1l1_opy_: bstack1111ll1ll_opy_,
            TestFramework.bstack11llllll111_opy_: bstack11llllll1l1_opy_
        }
    @staticmethod
    def __1l111l1l1ll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11ll1l1_opy_ (u"ࠥࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠣᔭ"), [])
            markers.extend([getattr(m, bstack11ll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᔮ"), None) for m in own_markers if getattr(m, bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᔯ"), None)])
            current = getattr(current, bstack11ll1l1_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᔰ"), None)
        return markers
    @staticmethod
    def __1l11111l111_opy_(location):
        return bstack11ll1l1_opy_ (u"ࠢ࠻࠼ࠥᔱ").join(filter(lambda x: isinstance(x, str), location))