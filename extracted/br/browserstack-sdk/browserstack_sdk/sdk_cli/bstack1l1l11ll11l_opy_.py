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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllll11l11_opy_,
    bstack1lllll111ll_opy_,
    bstack1lll1lll1ll_opy_,
    bstack1l1l1l1l1l1_opy_,
    bstack1llll11ll1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1lllllll1l1_opy_
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1llll1l1l1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l1l1_opy_ import bstack1l1lll1l1ll_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll111ll_opy_
bstack1lllllll111_opy_ = bstack1lllllll1l1_opy_()
bstack1l1lll1llll_opy_ = 1.0
bstack1111111lll_opy_ = bstack11l1111_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧጾ")
bstack1l1l11lllll_opy_ = bstack11l1111_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤጿ")
bstack1l1l11lll11_opy_ = bstack11l1111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦፀ")
bstack1l1l11ll1ll_opy_ = bstack11l1111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦፁ")
bstack1l1l11ll111_opy_ = bstack11l1111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣፂ")
_1llll11lll1_opy_ = set()
class bstack1l1l11ll1l1_opy_(TestFramework):
    bstack1l1l1l1l1ll_opy_ = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥፃ")
    bstack1l1l1llll1l_opy_ = bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤፄ")
    bstack1l1l1ll1l11_opy_ = bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦፅ")
    bstack1l1ll1ll1ll_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣፆ")
    bstack1l1ll1ll111_opy_ = bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥፇ")
    bstack1l1ll1ll1l1_opy_: bool
    bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_  = None
    bstack1lll1llll1l_opy_ = None
    bstack1l1l1l1lll1_opy_ = [
        bstack1lllll11l11_opy_.BEFORE_ALL,
        bstack1lllll11l11_opy_.AFTER_ALL,
        bstack1lllll11l11_opy_.BEFORE_EACH,
        bstack1lllll11l11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1lll1l11l_opy_: Dict[str, str],
        bstack1l1l1lll111_opy_: List[str]=[bstack11l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣፈ")],
        bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_=None,
        bstack1lll1llll1l_opy_=None
    ):
        super().__init__(bstack1l1l1lll111_opy_, bstack1l1lll1l11l_opy_, bstack1llll1l1l1l_opy_)
        self.bstack1l1ll1ll1l1_opy_ = any(bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤፉ") in item.lower() for item in bstack1l1l1lll111_opy_)
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
        if test_framework_state == bstack1lllll11l11_opy_.TEST or test_framework_state in bstack1l1l11ll1l1_opy_.bstack1l1l1l1lll1_opy_:
            bstack1l1ll1l111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllll11l11_opy_.NONE:
            self.logger.warning(bstack11l1111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦፊ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠦࠧፋ"))
            return
        if not self.bstack1l1ll1ll1l1_opy_:
            self.logger.warning(bstack11l1111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨፌ") + str(str(self.bstack1l1l1lll111_opy_)) + bstack11l1111_opy_ (u"ࠨࠢፍ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤፎ") + str(kwargs) + bstack11l1111_opy_ (u"ࠣࠤፏ"))
            return
        instance = self.__1l1l1lll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣፐ") + str(args) + bstack11l1111_opy_ (u"ࠥࠦፑ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1l1l11ll1l1_opy_.bstack1l1l1l1lll1_opy_ and test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack11ll1l11l_opy_.value)
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack11l1111_opy_ (u"ࠦ࠿ࠨፒ")+str(test_framework_state.name)
                TestFramework.bstack1l1ll1lll11_opy_(instance, name, bstack1lll1lll11l_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤፓ").format(e))
        try:
            if not TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1l1ll11l111_opy_) and test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                test = bstack1l1l11ll1l1_opy_.__1l1l1l11111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨፔ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠢࠣፕ"))
            if test_framework_state == bstack1lllll11l11_opy_.TEST:
                if test_hook_state == bstack1lll1lll1ll_opy_.PRE and not TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1lllll1ll1l_opy_):
                    TestFramework.bstack1llll111l11_opy_(instance, TestFramework.bstack1lllll1ll1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1111_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨፖ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠤࠥፗ"))
                elif test_hook_state == bstack1lll1lll1ll_opy_.POST and not TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1lll1lll111_opy_):
                    TestFramework.bstack1llll111l11_opy_(instance, TestFramework.bstack1lll1lll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨፘ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠦࠧፙ"))
            elif test_framework_state == bstack1lllll11l11_opy_.LOG and test_hook_state == bstack1lll1lll1ll_opy_.POST:
                bstack1l1l11ll1l1_opy_.__1l1llll111l_opy_(instance, *args)
            elif test_framework_state == bstack1lllll11l11_opy_.LOG_REPORT and test_hook_state == bstack1lll1lll1ll_opy_.POST:
                self.__1l1l1l11l1l_opy_(instance, *args)
                self.__1l1ll1l11l1_opy_(instance)
            elif test_framework_state in bstack1l1l11ll1l1_opy_.bstack1l1l1l1lll1_opy_:
                self.__1l1llll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨፚ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠨࠢ፛"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l1l1ll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1l1l11ll1l1_opy_.bstack1l1l1l1lll1_opy_ and test_hook_state == bstack1lll1lll1ll_opy_.POST:
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack11l1111_opy_ (u"ࠢ࠻ࠤ፜")+str(test_framework_state.name)
                bstack1lll1lll11l_opy_ = TestFramework.bstack1l1l1ll11ll_opy_(instance, name)
                bstack1lll1l1l11l_opy_.end(EVENTS.bstack11ll1l11l_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ፝"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ፞"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ፟").format(e))
    def bstack1lllllll1ll_opy_(self):
        return self.bstack1l1ll1ll1l1_opy_
    def __1l1l1ll1lll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣ፠"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1lll1ll11ll_opy_(rep, [bstack11l1111_opy_ (u"ࠧࡽࡨࡦࡰࠥ፡"), bstack11l1111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ።"), bstack11l1111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ፣"), bstack11l1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ፤"), bstack11l1111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥ፥"), bstack11l1111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤ፦")])
        return None
    def __1l1l1l11l1l_opy_(self, instance: bstack1lllll111ll_opy_, *args):
        result = self.__1l1l1ll1lll_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111llll_opy_ = None
        if result.get(bstack11l1111_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ፧"), None) == bstack11l1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ፨") and len(args) > 1 and getattr(args[1], bstack11l1111_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢ፩"), None) is not None:
            failure = [{bstack11l1111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ፪"): [args[1].excinfo.exconly(), result.get(bstack11l1111_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢ፫"), None)]}]
            bstack111111llll_opy_ = bstack11l1111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ፬") if bstack11l1111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ፭") in getattr(args[1].excinfo, bstack11l1111_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨ፮"), bstack11l1111_opy_ (u"ࠧࠨ፯")) else bstack11l1111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ፰")
        bstack1l1lll11lll_opy_ = result.get(bstack11l1111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ፱"), TestFramework.bstack1l1lll11ll1_opy_)
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
            target = None # bstack1l1l1llll11_opy_ bstack1l1l1lll1l1_opy_ this to be bstack11l1111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ፲")
            if test_framework_state == bstack1lllll11l11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1ll11111l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllll11l11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ፳"), None), bstack11l1111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ፴"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ፵"), None):
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
        bstack1l1l1l111ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1l11ll1l1_opy_.bstack1l1l1llll1l_opy_, {})
        if not key in bstack1l1l1l111ll_opy_:
            bstack1l1l1l111ll_opy_[key] = []
        bstack1l1ll11l1ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1l11ll1l1_opy_.bstack1l1l1ll1l11_opy_, {})
        if not key in bstack1l1ll11l1ll_opy_:
            bstack1l1ll11l1ll_opy_[key] = []
        bstack1l1l1l11l11_opy_ = {
            bstack1l1l11ll1l1_opy_.bstack1l1l1llll1l_opy_: bstack1l1l1l111ll_opy_,
            bstack1l1l11ll1l1_opy_.bstack1l1l1ll1l11_opy_: bstack1l1ll11l1ll_opy_,
        }
        if test_hook_state == bstack1lll1lll1ll_opy_.PRE:
            hook = {
                bstack11l1111_opy_ (u"ࠧࡱࡥࡺࠤ፶"): key,
                TestFramework.bstack1l1l1l11lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1lll1lll1_opy_: TestFramework.bstack1l1ll111111_opy_,
                TestFramework.bstack1l1l1l1ll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1l1ll1ll1_opy_: [],
                TestFramework.bstack1l1lll111l1_opy_: args[1] if len(args) > 1 else bstack11l1111_opy_ (u"࠭ࠧ፷"),
                TestFramework.bstack1l1llll1111_opy_: bstack1l1lll1l1ll_opy_.bstack1l1ll1l1lll_opy_()
            }
            bstack1l1l1l111ll_opy_[key].append(hook)
            bstack1l1l1l11l11_opy_[bstack1l1l11ll1l1_opy_.bstack1l1ll1ll1ll_opy_] = key
        elif test_hook_state == bstack1lll1lll1ll_opy_.POST:
            bstack1l1l1ll111l_opy_ = bstack1l1l1l111ll_opy_.get(key, [])
            hook = bstack1l1l1ll111l_opy_.pop() if bstack1l1l1ll111l_opy_ else None
            if hook:
                result = self.__1l1l1ll1lll_opy_(*args)
                if result:
                    bstack1l1lll1ll11_opy_ = result.get(bstack11l1111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣ፸"), TestFramework.bstack1l1ll111111_opy_)
                    if bstack1l1lll1ll11_opy_ != TestFramework.bstack1l1ll111111_opy_:
                        hook[TestFramework.bstack1l1lll1lll1_opy_] = bstack1l1lll1ll11_opy_
                hook[TestFramework.bstack1l1lll11l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l1llll1111_opy_]= bstack1l1lll1l1ll_opy_.bstack1l1ll1l1lll_opy_()
                self.bstack1l1ll1l1l11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1ll11ll11_opy_, [])
                if logs: self.bstack1lll1ll111l_opy_(instance, logs)
                bstack1l1ll11l1ll_opy_[key].append(hook)
                bstack1l1l1l11l11_opy_[bstack1l1l11ll1l1_opy_.bstack1l1ll1ll111_opy_] = key
        TestFramework.bstack1l1ll1111ll_opy_(instance, bstack1l1l1l11l11_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢ፹") + str(bstack1l1ll11l1ll_opy_) + bstack11l1111_opy_ (u"ࠤࠥ፺"))
    def __1l1llll1ll1_opy_(
        self,
        context: bstack1l1l1l1l1l1_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll1lll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1lll1ll11ll_opy_(args[0], [bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ፻"), bstack11l1111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧ፼"), bstack11l1111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ፽"), bstack11l1111_opy_ (u"ࠨࡩࡥࡵࠥ፾"), bstack11l1111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤ፿"), bstack11l1111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᎀ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11l1111_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎁ")) else fixturedef.get(bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᎂ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᎃ")) else None
        node = request.node if hasattr(request, bstack11l1111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᎄ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᎅ")) else None
        baseid = fixturedef.get(bstack11l1111_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᎆ"), None) or bstack11l1111_opy_ (u"ࠣࠤᎇ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1111_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᎈ")):
            target = bstack1l1l11ll1l1_opy_.__1l1l1l1l111_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1111_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᎉ")) else None
            if target and not TestFramework.bstack1l1l1lllll1_opy_(target):
                self.__1l1ll11111l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᎊ") + str(test_hook_state) + bstack11l1111_opy_ (u"ࠧࠨᎋ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᎌ") + str(target) + bstack11l1111_opy_ (u"ࠢࠣᎍ"))
            return None
        instance = TestFramework.bstack1l1l1lllll1_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᎎ") + str(target) + bstack11l1111_opy_ (u"ࠤࠥᎏ"))
            return None
        bstack1l1ll11llll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1l11ll1l1_opy_.bstack1l1l1l1l1ll_opy_, {})
        if os.getenv(bstack11l1111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦ᎐"), bstack11l1111_opy_ (u"ࠦ࠶ࠨ᎑")) == bstack11l1111_opy_ (u"ࠧ࠷ࠢ᎒"):
            bstack1l1l1llllll_opy_ = bstack11l1111_opy_ (u"ࠨ࠺ࠣ᎓").join((scope, fixturename))
            bstack1l1l1l11ll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1l1l1111l_opy_ = {
                bstack11l1111_opy_ (u"ࠢ࡬ࡧࡼࠦ᎔"): bstack1l1l1llllll_opy_,
                bstack11l1111_opy_ (u"ࠣࡶࡤ࡫ࡸࠨ᎕"): bstack1l1l11ll1l1_opy_.__1l1ll11lll1_opy_(request.node),
                bstack11l1111_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥ᎖"): fixturedef,
                bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ᎗"): scope,
                bstack11l1111_opy_ (u"ࠦࡹࡿࡰࡦࠤ᎘"): None,
            }
            try:
                if test_hook_state == bstack1lll1lll1ll_opy_.POST and callable(getattr(args[-1], bstack11l1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤ᎙"), None)):
                    bstack1l1l1l1111l_opy_[bstack11l1111_opy_ (u"ࠨࡴࡺࡲࡨࠦ᎚")] = TestFramework.bstack1lll1l11l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1lll1ll_opy_.PRE:
                bstack1l1l1l1111l_opy_[bstack11l1111_opy_ (u"ࠢࡶࡷ࡬ࡨࠧ᎛")] = uuid4().__str__()
                bstack1l1l1l1111l_opy_[bstack1l1l11ll1l1_opy_.bstack1l1l1l1ll11_opy_] = bstack1l1l1l11ll1_opy_
            elif test_hook_state == bstack1lll1lll1ll_opy_.POST:
                bstack1l1l1l1111l_opy_[bstack1l1l11ll1l1_opy_.bstack1l1lll11l1l_opy_] = bstack1l1l1l11ll1_opy_
            if bstack1l1l1llllll_opy_ in bstack1l1ll11llll_opy_:
                bstack1l1ll11llll_opy_[bstack1l1l1llllll_opy_].update(bstack1l1l1l1111l_opy_)
                self.logger.debug(bstack11l1111_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤ᎜") + str(bstack1l1ll11llll_opy_[bstack1l1l1llllll_opy_]) + bstack11l1111_opy_ (u"ࠤࠥ᎝"))
            else:
                bstack1l1ll11llll_opy_[bstack1l1l1llllll_opy_] = bstack1l1l1l1111l_opy_
                self.logger.debug(bstack11l1111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨ᎞") + str(len(bstack1l1ll11llll_opy_)) + bstack11l1111_opy_ (u"ࠦࠧ᎟"))
        TestFramework.bstack1llll111l11_opy_(instance, bstack1l1l11ll1l1_opy_.bstack1l1l1l1l1ll_opy_, bstack1l1ll11llll_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᎠ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠨࠢᎡ"))
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
            bstack1l1l11ll1l1_opy_.bstack1l1l1l1l1ll_opy_: {},
            bstack1l1l11ll1l1_opy_.bstack1l1l1ll1l11_opy_: {},
            bstack1l1l11ll1l1_opy_.bstack1l1l1llll1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll111l11_opy_(ob, TestFramework.bstack1l1l1ll1l1l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll111l11_opy_(ob, TestFramework.bstack1llllll1lll_opy_, context.platform_index)
        TestFramework.bstack1ll11llllll_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᎢ") + str(TestFramework.bstack1ll11llllll_opy_.keys()) + bstack11l1111_opy_ (u"ࠣࠤᎣ"))
        return ob
    def bstack1llll11ll11_opy_(self, instance: bstack1lllll111ll_opy_, bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_]):
        bstack1l1l1l1llll_opy_ = (
            bstack1l1l11ll1l1_opy_.bstack1l1ll1ll1ll_opy_
            if bstack1llll11l111_opy_[1] == bstack1lll1lll1ll_opy_.PRE
            else bstack1l1l11ll1l1_opy_.bstack1l1ll1ll111_opy_
        )
        hook = bstack1l1l11ll1l1_opy_.bstack1l1l1lll11l_opy_(instance, bstack1l1l1l1llll_opy_)
        entries = hook.get(TestFramework.bstack1l1l1ll1ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, []))
        return entries
    def bstack1llll111ll1_opy_(self, instance: bstack1lllll111ll_opy_, bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_]):
        bstack1l1l1l1llll_opy_ = (
            bstack1l1l11ll1l1_opy_.bstack1l1ll1ll1ll_opy_
            if bstack1llll11l111_opy_[1] == bstack1lll1lll1ll_opy_.PRE
            else bstack1l1l11ll1l1_opy_.bstack1l1ll1ll111_opy_
        )
        bstack1l1l11ll1l1_opy_.bstack1l1ll1l11ll_opy_(instance, bstack1l1l1l1llll_opy_)
        TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1l111l1_opy_, []).clear()
    def bstack1l1ll1l1l11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᎤ")
        global _1llll11lll1_opy_
        platform_index = os.environ[bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᎥ")]
        bstack1lllll1l111_opy_ = os.path.join(bstack1lllllll111_opy_, (bstack1111111lll_opy_ + str(platform_index)), bstack1l1l11ll1ll_opy_)
        if not os.path.exists(bstack1lllll1l111_opy_) or not os.path.isdir(bstack1lllll1l111_opy_):
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤᎦ").format(bstack1lllll1l111_opy_))
            return
        logs = hook.get(bstack11l1111_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᎧ"), [])
        with os.scandir(bstack1lllll1l111_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1llll11lll1_opy_:
                    self.logger.info(bstack11l1111_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᎨ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1111_opy_ (u"ࠢࠣᎩ")
                    log_entry = bstack1llll11ll1l_opy_(
                        kind=bstack11l1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᎪ"),
                        message=bstack11l1111_opy_ (u"ࠤࠥᎫ"),
                        level=bstack11l1111_opy_ (u"ࠥࠦᎬ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack111111l1l1_opy_=entry.stat().st_size,
                        bstack1llll1l1111_opy_=bstack11l1111_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᎭ"),
                        bstack1ll1l_opy_=os.path.abspath(entry.path),
                        bstack1l1ll11l1l1_opy_=hook.get(TestFramework.bstack1l1l1l11lll_opy_)
                    )
                    logs.append(log_entry)
                    _1llll11lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᎮ")]
        bstack1l1ll1lllll_opy_ = os.path.join(bstack1lllllll111_opy_, (bstack1111111lll_opy_ + str(platform_index)), bstack1l1l11ll1ll_opy_, bstack1l1l11ll111_opy_)
        if not os.path.exists(bstack1l1ll1lllll_opy_) or not os.path.isdir(bstack1l1ll1lllll_opy_):
            self.logger.info(bstack11l1111_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᎯ").format(bstack1l1ll1lllll_opy_))
        else:
            self.logger.info(bstack11l1111_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᎰ").format(bstack1l1ll1lllll_opy_))
            with os.scandir(bstack1l1ll1lllll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1llll11lll1_opy_:
                        self.logger.info(bstack11l1111_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᎱ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1111_opy_ (u"ࠤࠥᎲ")
                        log_entry = bstack1llll11ll1l_opy_(
                            kind=bstack11l1111_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᎳ"),
                            message=bstack11l1111_opy_ (u"ࠦࠧᎴ"),
                            level=bstack11l1111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᎵ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack111111l1l1_opy_=entry.stat().st_size,
                            bstack1llll1l1111_opy_=bstack11l1111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᎶ"),
                            bstack1ll1l_opy_=os.path.abspath(entry.path),
                            bstack1llll111111_opy_=hook.get(TestFramework.bstack1l1l1l11lll_opy_)
                        )
                        logs.append(log_entry)
                        _1llll11lll1_opy_.add(abs_path)
        hook[bstack11l1111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᎷ")] = logs
    def bstack1lll1ll111l_opy_(
        self,
        bstack1llllll111l_opy_: bstack1lllll111ll_opy_,
        entries: List[bstack1llll11ll1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᎸ"))
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
            log_entry.message = entry.message.encode(bstack11l1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᎹ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l1111_opy_ (u"ࠥࠦᎺ")
            if entry.kind == bstack11l1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᎻ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack111111l1l1_opy_
                log_entry.file_path = entry.bstack1ll1l_opy_
        def bstack1llll1l11ll_opy_():
            bstack1ll1l1l1_opy_ = datetime.now()
            try:
                self.bstack1lll1llll1l_opy_.LogCreatedEvent(req)
                bstack1llllll111l_opy_.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᎼ"), datetime.now() - bstack1ll1l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᎽ").format(str(e)))
                traceback.print_exc()
        self.bstack1llll1l1l1l_opy_.enqueue(bstack1llll1l11ll_opy_)
    def __1l1ll1l11l1_opy_(self, instance) -> None:
        bstack11l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᎾ")
        bstack1l1l1l11l11_opy_ = {bstack11l1111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᎿ"): bstack1l1lll1l1ll_opy_.bstack1l1ll1l1lll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1ll1111ll_opy_(instance, bstack1l1l1l11l11_opy_)
    @staticmethod
    def bstack1l1l1lll11l_opy_(instance: bstack1lllll111ll_opy_, bstack1l1l1l1llll_opy_: str):
        bstack1l1ll1llll1_opy_ = (
            bstack1l1l11ll1l1_opy_.bstack1l1l1ll1l11_opy_
            if bstack1l1l1l1llll_opy_ == bstack1l1l11ll1l1_opy_.bstack1l1ll1ll111_opy_
            else bstack1l1l11ll1l1_opy_.bstack1l1l1llll1l_opy_
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
        hook = bstack1l1l11ll1l1_opy_.bstack1l1l1lll11l_opy_(instance, bstack1l1l1l1llll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1l1ll1ll1_opy_, []).clear()
    @staticmethod
    def __1l1llll111l_opy_(instance: bstack1lllll111ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1111_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᏀ"), None)):
            return
        if os.getenv(bstack11l1111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᏁ"), bstack11l1111_opy_ (u"ࠦ࠶ࠨᏂ")) != bstack11l1111_opy_ (u"ࠧ࠷ࠢᏃ"):
            bstack1l1l11ll1l1_opy_.logger.warning(bstack11l1111_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᏄ"))
            return
        bstack1l1ll11l11l_opy_ = {
            bstack11l1111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᏅ"): (bstack1l1l11ll1l1_opy_.bstack1l1ll1ll1ll_opy_, bstack1l1l11ll1l1_opy_.bstack1l1l1llll1l_opy_),
            bstack11l1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᏆ"): (bstack1l1l11ll1l1_opy_.bstack1l1ll1ll111_opy_, bstack1l1l11ll1l1_opy_.bstack1l1l1ll1l11_opy_),
        }
        for when in (bstack11l1111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᏇ"), bstack11l1111_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᏈ"), bstack11l1111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᏉ")):
            bstack1l1l1ll11l1_opy_ = args[1].get_records(when)
            if not bstack1l1l1ll11l1_opy_:
                continue
            records = [
                bstack1llll11ll1l_opy_(
                    kind=TestFramework.bstack1lllllll11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᏊ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1111_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᏋ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1l1ll11l1_opy_
                if isinstance(getattr(r, bstack11l1111_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᏌ"), None), str) and r.message.strip()
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
    def __1l1l1l11111_opy_(test) -> Dict[str, Any]:
        bstack1ll111lll1_opy_ = bstack1l1l11ll1l1_opy_.__1l1l1l1l111_opy_(test.location) if hasattr(test, bstack11l1111_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᏍ")) else getattr(test, bstack11l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᏎ"), None)
        test_name = test.name if hasattr(test, bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᏏ")) else None
        bstack1l1ll11ll1l_opy_ = test.fspath.strpath if hasattr(test, bstack11l1111_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᏐ")) and test.fspath else None
        if not bstack1ll111lll1_opy_ or not test_name or not bstack1l1ll11ll1l_opy_:
            return None
        code = None
        if hasattr(test, bstack11l1111_opy_ (u"ࠧࡵࡢ࡫ࠤᏑ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1l11llll1_opy_ = []
        try:
            bstack1l1l11llll1_opy_ = bstack1l1ll111ll_opy_.bstack1111lllll1_opy_(test)
        except:
            bstack1l1l11ll1l1_opy_.logger.warning(bstack11l1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᏒ"))
        return {
            TestFramework.bstack1lll1l1ll1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l1ll11l111_opy_: bstack1ll111lll1_opy_,
            TestFramework.bstack1lll11lllll_opy_: test_name,
            TestFramework.bstack1lll11l1l1l_opy_: getattr(test, bstack11l1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᏓ"), None),
            TestFramework.bstack1l1l1l1l11l_opy_: bstack1l1ll11ll1l_opy_,
            TestFramework.bstack1l1lll1ll1l_opy_: bstack1l1l11ll1l1_opy_.__1l1ll11lll1_opy_(test),
            TestFramework.bstack1l1ll1l1l1l_opy_: code,
            TestFramework.bstack1ll1l11l111_opy_: TestFramework.bstack1l1lll11ll1_opy_,
            TestFramework.bstack1ll1111lll1_opy_: bstack1ll111lll1_opy_,
            TestFramework.bstack1l1l11lll1l_opy_: bstack1l1l11llll1_opy_
        }
    @staticmethod
    def __1l1ll11lll1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11l1111_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᏔ"), [])
            markers.extend([getattr(m, bstack11l1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᏕ"), None) for m in own_markers if getattr(m, bstack11l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᏖ"), None)])
            current = getattr(current, bstack11l1111_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᏗ"), None)
        return markers
    @staticmethod
    def __1l1l1l1l111_opy_(location):
        return bstack11l1111_opy_ (u"ࠧࡀ࠺ࠣᏘ").join(filter(lambda x: isinstance(x, str), location))