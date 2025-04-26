# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111l1111_opy_
from browserstack_sdk.sdk_cli.utils.bstack111ll11l_opy_ import bstack1l11l11111l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll1111ll_opy_,
    bstack1lll1lllll1_opy_,
    bstack1lll1l1l11l_opy_,
    bstack1l11l1l111l_opy_,
    bstack1ll1lllllll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1llll1lll_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll11111l1_opy_ import bstack1llll11llll_opy_
from browserstack_sdk.sdk_cli.bstack1111l1l1l1_opy_ import bstack1111l1ll11_opy_
bstack1l1llllllll_opy_ = bstack1l1llll1lll_opy_()
bstack1l1ll1lll1l_opy_ = bstack1l11lll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦ፧")
bstack1l111ll1l1l_opy_ = bstack1l11lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ፨")
bstack1l11l1ll1l1_opy_ = bstack1l11lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ፩")
bstack1l11ll1ll11_opy_ = 1.0
_1ll111111l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l111l1l1ll_opy_ = bstack1l11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ፪")
    bstack1l111l1ll11_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨ፫")
    bstack1l111l1l1l1_opy_ = bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ፬")
    bstack1l111ll111l_opy_ = bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧ፭")
    bstack1l111l1ll1l_opy_ = bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢ፮")
    bstack1l11ll1l111_opy_: bool
    bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_  = None
    bstack1l11ll1lll1_opy_ = [
        bstack1llll1111ll_opy_.BEFORE_ALL,
        bstack1llll1111ll_opy_.AFTER_ALL,
        bstack1llll1111ll_opy_.BEFORE_EACH,
        bstack1llll1111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll111_opy_: Dict[str, str],
        bstack1ll1l11ll11_opy_: List[str]=[bstack1l11lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ፯")],
        bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_ = None,
        bstack1lll1ll11ll_opy_=None
    ):
        super().__init__(bstack1ll1l11ll11_opy_, bstack1l11llll111_opy_, bstack1111l1l1l1_opy_)
        self.bstack1l11ll1l111_opy_ = any(bstack1l11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ፰") in item.lower() for item in bstack1ll1l11ll11_opy_)
        self.bstack1lll1ll11ll_opy_ = bstack1lll1ll11ll_opy_
    def track_event(
        self,
        context: bstack1l11l1l111l_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        test_hook_state: bstack1lll1l1l11l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1llll1111ll_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11ll1lll1_opy_:
            bstack1l11l11111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll1111ll_opy_.NONE:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣ፱") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠣࠤ፲"))
            return
        if not self.bstack1l11ll1l111_opy_:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥ፳") + str(str(self.bstack1ll1l11ll11_opy_)) + bstack1l11lll_opy_ (u"ࠥࠦ፴"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ፵") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨ፶"))
            return
        instance = self.__1l11ll1ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧ፷") + str(args) + bstack1l11lll_opy_ (u"ࠢࠣ፸"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11ll1lll1_opy_ and test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack11l111l1_opy_.value)
                name = str(EVENTS.bstack11l111l1_opy_.name)+bstack1l11lll_opy_ (u"ࠣ࠼ࠥ፹")+str(test_framework_state.name)
                TestFramework.bstack1l11l11lll1_opy_(instance, name, bstack1ll1ll1l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨ፺").format(e))
        try:
            if test_framework_state == bstack1llll1111ll_opy_.TEST:
                if not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l11ll11111_opy_) and test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111lllll1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ፻") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠦࠧ፼"))
                if test_hook_state == bstack1lll1l1l11l_opy_.PRE and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lllll1ll_opy_):
                    TestFramework.bstack1111l111ll_opy_(instance, TestFramework.bstack1l1lllll1ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11ll1l1ll_opy_(instance, args)
                    self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ፽") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠨࠢ፾"))
                elif test_hook_state == bstack1lll1l1l11l_opy_.POST and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll111ll11l_opy_):
                    TestFramework.bstack1111l111ll_opy_(instance, TestFramework.bstack1ll111ll11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥ፿") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠣࠤᎀ"))
            elif test_framework_state == bstack1llll1111ll_opy_.STEP:
                if test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                    PytestBDDFramework.__1l11l11llll_opy_(instance, args)
                elif test_hook_state == bstack1lll1l1l11l_opy_.POST:
                    PytestBDDFramework.__1l11l11l1ll_opy_(instance, args)
            elif test_framework_state == bstack1llll1111ll_opy_.LOG and test_hook_state == bstack1lll1l1l11l_opy_.POST:
                PytestBDDFramework.__1l111ll11ll_opy_(instance, *args)
            elif test_framework_state == bstack1llll1111ll_opy_.LOG_REPORT and test_hook_state == bstack1lll1l1l11l_opy_.POST:
                self.__1l11lll1ll1_opy_(instance, *args)
                self.__1l11ll1111l_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11ll1lll1_opy_:
                self.__1l111l1llll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᎁ") + str(instance.ref()) + bstack1l11lll_opy_ (u"ࠥࠦᎂ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111lll1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11ll1lll1_opy_ and test_hook_state == bstack1lll1l1l11l_opy_.POST:
                name = str(EVENTS.bstack11l111l1_opy_.name)+bstack1l11lll_opy_ (u"ࠦ࠿ࠨᎃ")+str(test_framework_state.name)
                bstack1ll1ll1l111_opy_ = TestFramework.bstack1l11l1111l1_opy_(instance, name)
                bstack1ll1llll111_opy_.end(EVENTS.bstack11l111l1_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᎄ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᎅ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᎆ").format(e))
    def bstack1ll111llll1_opy_(self):
        return self.bstack1l11ll1l111_opy_
    def __1l11l1l1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᎇ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11l11111_opy_(rep, [bstack1l11lll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᎈ"), bstack1l11lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᎉ"), bstack1l11lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᎊ"), bstack1l11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᎋ"), bstack1l11lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᎌ"), bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᎍ")])
        return None
    def __1l11lll1ll1_opy_(self, instance: bstack1lll1lllll1_opy_, *args):
        result = self.__1l11l1l1l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1llll_opy_ = None
        if result.get(bstack1l11lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᎎ"), None) == bstack1l11lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᎏ") and len(args) > 1 and getattr(args[1], bstack1l11lll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦ᎐"), None) is not None:
            failure = [{bstack1l11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᎑"): [args[1].excinfo.exconly(), result.get(bstack1l11lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦ᎒"), None)]}]
            bstack1111l1llll_opy_ = bstack1l11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᎓") if bstack1l11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ᎔") in getattr(args[1].excinfo, bstack1l11lll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥ᎕"), bstack1l11lll_opy_ (u"ࠤࠥ᎖")) else bstack1l11lll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ᎗")
        bstack1l111lll111_opy_ = result.get(bstack1l11lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᎘"), TestFramework.bstack1l11lll111l_opy_)
        if bstack1l111lll111_opy_ != TestFramework.bstack1l11lll111l_opy_:
            TestFramework.bstack1111l111ll_opy_(instance, TestFramework.bstack1ll111l1l11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11ll11l1l_opy_(instance, {
            TestFramework.bstack1l1l1lll1ll_opy_: failure,
            TestFramework.bstack1l111lll1l1_opy_: bstack1111l1llll_opy_,
            TestFramework.bstack1l1l1ll11ll_opy_: bstack1l111lll111_opy_,
        })
    def __1l11ll1ll1l_opy_(
        self,
        context: bstack1l11l1l111l_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        test_hook_state: bstack1lll1l1l11l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1llll1111ll_opy_.SETUP_FIXTURE:
            instance = self.__1l11l11l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111lll11l_opy_ bstack1l11l1lll11_opy_ this to be bstack1l11lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᎙")
            if test_framework_state == bstack1llll1111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l11l11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll1111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᎚"), None), bstack1l11lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᎛"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11lll_opy_ (u"ࠣࡰࡲࡨࡪࠨ᎜"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l11lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᎝"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111111l1l_opy_(target) if target else None
        return instance
    def __1l111l1llll_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        test_hook_state: bstack1lll1l1l11l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11ll1l11l_opy_ = TestFramework.bstack1111111111_opy_(instance, PytestBDDFramework.bstack1l111l1ll11_opy_, {})
        if not key in bstack1l11ll1l11l_opy_:
            bstack1l11ll1l11l_opy_[key] = []
        bstack1l11lll1l1l_opy_ = TestFramework.bstack1111111111_opy_(instance, PytestBDDFramework.bstack1l111l1l1l1_opy_, {})
        if not key in bstack1l11lll1l1l_opy_:
            bstack1l11lll1l1l_opy_[key] = []
        bstack1l11ll11lll_opy_ = {
            PytestBDDFramework.bstack1l111l1ll11_opy_: bstack1l11ll1l11l_opy_,
            PytestBDDFramework.bstack1l111l1l1l1_opy_: bstack1l11lll1l1l_opy_,
        }
        if test_hook_state == bstack1lll1l1l11l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l11lll_opy_ (u"ࠥ࡯ࡪࡿࠢ᎞"): key,
                TestFramework.bstack1l11ll11ll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l11_opy_: TestFramework.bstack1l11l1lll1l_opy_,
                TestFramework.bstack1l11l1l1111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11lll11ll_opy_: [],
                TestFramework.bstack1l11lll1lll_opy_: hook_name,
                TestFramework.bstack1l111l1lll1_opy_: bstack1llll11llll_opy_.bstack1l11l1ll11l_opy_()
            }
            bstack1l11ll1l11l_opy_[key].append(hook)
            bstack1l11ll11lll_opy_[PytestBDDFramework.bstack1l111ll111l_opy_] = key
        elif test_hook_state == bstack1lll1l1l11l_opy_.POST:
            bstack1l11lll11l1_opy_ = bstack1l11ll1l11l_opy_.get(key, [])
            hook = bstack1l11lll11l1_opy_.pop() if bstack1l11lll11l1_opy_ else None
            if hook:
                result = self.__1l11l1l1l11_opy_(*args)
                if result:
                    bstack1l11l1l1l1l_opy_ = result.get(bstack1l11lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᎟"), TestFramework.bstack1l11l1lll1l_opy_)
                    if bstack1l11l1l1l1l_opy_ != TestFramework.bstack1l11l1lll1l_opy_:
                        hook[TestFramework.bstack1l11ll11l11_opy_] = bstack1l11l1l1l1l_opy_
                hook[TestFramework.bstack1l11l111ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l1lll1_opy_] = bstack1llll11llll_opy_.bstack1l11l1ll11l_opy_()
                self.bstack1l11ll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1llll1_opy_, [])
                self.bstack1ll111l11ll_opy_(instance, logs)
                bstack1l11lll1l1l_opy_[key].append(hook)
                bstack1l11ll11lll_opy_[PytestBDDFramework.bstack1l111l1ll1l_opy_] = key
        TestFramework.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11lll_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᎠ") + str(bstack1l11lll1l1l_opy_) + bstack1l11lll_opy_ (u"ࠨࠢᎡ"))
    def __1l11l11l1l1_opy_(
        self,
        context: bstack1l11l1l111l_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        test_hook_state: bstack1lll1l1l11l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11l11111_opy_(args[0], [bstack1l11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᎢ"), bstack1l11lll_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᎣ"), bstack1l11lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᎤ"), bstack1l11lll_opy_ (u"ࠥ࡭ࡩࡹࠢᎥ"), bstack1l11lll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᎦ"), bstack1l11lll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᎧ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l11lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᎨ")) else fixturedef.get(bstack1l11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᎩ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᎪ")) else None
        node = request.node if hasattr(request, bstack1l11lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᎫ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᎬ")) else None
        baseid = fixturedef.get(bstack1l11lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᎭ"), None) or bstack1l11lll_opy_ (u"ࠧࠨᎮ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11lll_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᎯ")):
            target = PytestBDDFramework.__1l111llllll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᎰ")) else None
            if target and not TestFramework.bstack1111111l1l_opy_(target):
                self.__1l11l11l11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᎱ") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠤࠥᎲ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᎳ") + str(target) + bstack1l11lll_opy_ (u"ࠦࠧᎴ"))
            return None
        instance = TestFramework.bstack1111111l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᎵ") + str(target) + bstack1l11lll_opy_ (u"ࠨࠢᎶ"))
            return None
        bstack1l11l1l11ll_opy_ = TestFramework.bstack1111111111_opy_(instance, PytestBDDFramework.bstack1l111l1l1ll_opy_, {})
        if os.getenv(bstack1l11lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᎷ"), bstack1l11lll_opy_ (u"ࠣ࠳ࠥᎸ")) == bstack1l11lll_opy_ (u"ࠤ࠴ࠦᎹ"):
            bstack1l111ll11l1_opy_ = bstack1l11lll_opy_ (u"ࠥ࠾ࠧᎺ").join((scope, fixturename))
            bstack1l11l111l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11llll11l_opy_ = {
                bstack1l11lll_opy_ (u"ࠦࡰ࡫ࡹࠣᎻ"): bstack1l111ll11l1_opy_,
                bstack1l11lll_opy_ (u"ࠧࡺࡡࡨࡵࠥᎼ"): PytestBDDFramework.__1l11ll1llll_opy_(request.node, scenario),
                bstack1l11lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᎽ"): fixturedef,
                bstack1l11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᎾ"): scope,
                bstack1l11lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᎿ"): None,
            }
            try:
                if test_hook_state == bstack1lll1l1l11l_opy_.POST and callable(getattr(args[-1], bstack1l11lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᏀ"), None)):
                    bstack1l11llll11l_opy_[bstack1l11lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᏁ")] = TestFramework.bstack1l1llll1111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                bstack1l11llll11l_opy_[bstack1l11lll_opy_ (u"ࠦࡺࡻࡩࡥࠤᏂ")] = uuid4().__str__()
                bstack1l11llll11l_opy_[PytestBDDFramework.bstack1l11l1l1111_opy_] = bstack1l11l111l1l_opy_
            elif test_hook_state == bstack1lll1l1l11l_opy_.POST:
                bstack1l11llll11l_opy_[PytestBDDFramework.bstack1l11l111ll1_opy_] = bstack1l11l111l1l_opy_
            if bstack1l111ll11l1_opy_ in bstack1l11l1l11ll_opy_:
                bstack1l11l1l11ll_opy_[bstack1l111ll11l1_opy_].update(bstack1l11llll11l_opy_)
                self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᏃ") + str(bstack1l11l1l11ll_opy_[bstack1l111ll11l1_opy_]) + bstack1l11lll_opy_ (u"ࠨࠢᏄ"))
            else:
                bstack1l11l1l11ll_opy_[bstack1l111ll11l1_opy_] = bstack1l11llll11l_opy_
                self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᏅ") + str(len(bstack1l11l1l11ll_opy_)) + bstack1l11lll_opy_ (u"ࠣࠤᏆ"))
        TestFramework.bstack1111l111ll_opy_(instance, PytestBDDFramework.bstack1l111l1l1ll_opy_, bstack1l11l1l11ll_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᏇ") + str(instance.ref()) + bstack1l11lll_opy_ (u"ࠥࠦᏈ"))
        return instance
    def __1l11l11l11l_opy_(
        self,
        context: bstack1l11l1l111l_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111l1111_opy_.create_context(target)
        ob = bstack1lll1lllll1_opy_(ctx, self.bstack1ll1l11ll11_opy_, self.bstack1l11llll111_opy_, test_framework_state)
        TestFramework.bstack1l11ll11l1l_opy_(ob, {
            TestFramework.bstack1ll1l1ll111_opy_: context.test_framework_name,
            TestFramework.bstack1ll1111l1ll_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1l11l_opy_: [],
            PytestBDDFramework.bstack1l111l1l1ll_opy_: {},
            PytestBDDFramework.bstack1l111l1l1l1_opy_: {},
            PytestBDDFramework.bstack1l111l1ll11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l111ll_opy_(ob, TestFramework.bstack1l111ll1ll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l111ll_opy_(ob, TestFramework.bstack1ll1l111lll_opy_, context.platform_index)
        TestFramework.bstack11111lllll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᏉ") + str(TestFramework.bstack11111lllll_opy_.keys()) + bstack1l11lll_opy_ (u"ࠧࠨᏊ"))
        return ob
    @staticmethod
    def __1l11ll1l1ll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11lll_opy_ (u"࠭ࡩࡥࠩᏋ"): id(step),
                bstack1l11lll_opy_ (u"ࠧࡵࡧࡻࡸࠬᏌ"): step.name,
                bstack1l11lll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᏍ"): step.keyword,
            })
        meta = {
            bstack1l11lll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᏎ"): {
                bstack1l11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨᏏ"): feature.name,
                bstack1l11lll_opy_ (u"ࠫࡵࡧࡴࡩࠩᏐ"): feature.filename,
                bstack1l11lll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᏑ"): feature.description
            },
            bstack1l11lll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᏒ"): {
                bstack1l11lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏓ"): scenario.name
            },
            bstack1l11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᏔ"): steps,
            bstack1l11lll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᏕ"): PytestBDDFramework.__1l111l1l111_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l111ll1111_opy_: meta
            }
        )
    def bstack1l11ll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l11lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᏖ")
        global _1ll111111l1_opy_
        platform_index = os.environ[bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᏗ")]
        bstack1l1lll1l1l1_opy_ = os.path.join(bstack1l1llllllll_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), bstack1l111ll1l1l_opy_)
        if not os.path.exists(bstack1l1lll1l1l1_opy_) or not os.path.isdir(bstack1l1lll1l1l1_opy_):
            return
        logs = hook.get(bstack1l11lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᏘ"), [])
        with os.scandir(bstack1l1lll1l1l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111111l1_opy_:
                    self.logger.info(bstack1l11lll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᏙ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l11lll_opy_ (u"ࠢࠣᏚ")
                    log_entry = bstack1ll1lllllll_opy_(
                        kind=bstack1l11lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᏛ"),
                        message=bstack1l11lll_opy_ (u"ࠤࠥᏜ"),
                        level=bstack1l11lll_opy_ (u"ࠥࠦᏝ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll1111111l_opy_=entry.stat().st_size,
                        bstack1ll11111111_opy_=bstack1l11lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᏞ"),
                        bstack11111l1_opy_=os.path.abspath(entry.path),
                        bstack1l11l11ll11_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᏟ")]
        bstack1l11l1111ll_opy_ = os.path.join(bstack1l1llllllll_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), bstack1l111ll1l1l_opy_, bstack1l11l1ll1l1_opy_)
        if not os.path.exists(bstack1l11l1111ll_opy_) or not os.path.isdir(bstack1l11l1111ll_opy_):
            self.logger.info(bstack1l11lll_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᏠ").format(bstack1l11l1111ll_opy_))
        else:
            self.logger.info(bstack1l11lll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᏡ").format(bstack1l11l1111ll_opy_))
            with os.scandir(bstack1l11l1111ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111111l1_opy_:
                        self.logger.info(bstack1l11lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᏢ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l11lll_opy_ (u"ࠤࠥᏣ")
                        log_entry = bstack1ll1lllllll_opy_(
                            kind=bstack1l11lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᏤ"),
                            message=bstack1l11lll_opy_ (u"ࠦࠧᏥ"),
                            level=bstack1l11lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᏦ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll1111111l_opy_=entry.stat().st_size,
                            bstack1ll11111111_opy_=bstack1l11lll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᏧ"),
                            bstack11111l1_opy_=os.path.abspath(entry.path),
                            bstack1ll11111l11_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111111l1_opy_.add(abs_path)
        hook[bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᏨ")] = logs
    def bstack1ll111l11ll_opy_(
        self,
        bstack1ll111ll1ll_opy_: bstack1lll1lllll1_opy_,
        entries: List[bstack1ll1lllllll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᏩ"))
        req.platform_index = TestFramework.bstack1111111111_opy_(bstack1ll111ll1ll_opy_, TestFramework.bstack1ll1l111lll_opy_)
        req.execution_context.hash = str(bstack1ll111ll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll111ll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll111ll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111111111_opy_(bstack1ll111ll1ll_opy_, TestFramework.bstack1ll1l1ll111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111111111_opy_(bstack1ll111ll1ll_opy_, TestFramework.bstack1ll1111l1ll_opy_)
            log_entry.uuid = entry.bstack1l11l11ll11_opy_
            log_entry.test_framework_state = bstack1ll111ll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l11lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᏪ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l11lll_opy_ (u"ࠥࠦᏫ")
            if entry.kind == bstack1l11lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᏬ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll1111111l_opy_
                log_entry.file_path = entry.bstack11111l1_opy_
        def bstack1ll111lllll_opy_():
            bstack1ll1ll11ll_opy_ = datetime.now()
            try:
                self.bstack1lll1ll11ll_opy_.LogCreatedEvent(req)
                bstack1ll111ll1ll_opy_.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᏭ"), datetime.now() - bstack1ll1ll11ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᏮ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1l1l1_opy_.enqueue(bstack1ll111lllll_opy_)
    def __1l11ll1111l_opy_(self, instance) -> None:
        bstack1l11lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᏯ")
        bstack1l11ll11lll_opy_ = {bstack1l11lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᏰ"): bstack1llll11llll_opy_.bstack1l11l1ll11l_opy_()}
        TestFramework.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11lll_opy_)
    @staticmethod
    def __1l11l11llll_opy_(instance, args):
        request, bstack1l11l1l1ll1_opy_ = args
        bstack1l11l111111_opy_ = id(bstack1l11l1l1ll1_opy_)
        bstack1l11l1ll111_opy_ = instance.data[TestFramework.bstack1l111ll1111_opy_]
        step = next(filter(lambda st: st[bstack1l11lll_opy_ (u"ࠩ࡬ࡨࠬᏱ")] == bstack1l11l111111_opy_, bstack1l11l1ll111_opy_[bstack1l11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏲ")]), None)
        step.update({
            bstack1l11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᏳ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11l1ll111_opy_[bstack1l11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏴ")]) if st[bstack1l11lll_opy_ (u"࠭ࡩࡥࠩᏵ")] == step[bstack1l11lll_opy_ (u"ࠧࡪࡦࠪ᏶")]), None)
        if index is not None:
            bstack1l11l1ll111_opy_[bstack1l11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᏷")][index] = step
        instance.data[TestFramework.bstack1l111ll1111_opy_] = bstack1l11l1ll111_opy_
    @staticmethod
    def __1l11l11l1ll_opy_(instance, args):
        bstack1l11lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᏸ")
        bstack1l11l1l11l1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l1l1ll1_opy_ = args[1]
        bstack1l11l111111_opy_ = id(bstack1l11l1l1ll1_opy_)
        bstack1l11l1ll111_opy_ = instance.data[TestFramework.bstack1l111ll1111_opy_]
        step = None
        if bstack1l11l111111_opy_ is not None and bstack1l11l1ll111_opy_.get(bstack1l11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏹ")):
            step = next(filter(lambda st: st[bstack1l11lll_opy_ (u"ࠫ࡮ࡪࠧᏺ")] == bstack1l11l111111_opy_, bstack1l11l1ll111_opy_[bstack1l11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏻ")]), None)
            step.update({
                bstack1l11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᏼ"): bstack1l11l1l11l1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᏽ"): bstack1l11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᏾"),
                bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᏿"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l11lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᐀"): bstack1l11lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᐁ"),
                })
        index = next((i for i, st in enumerate(bstack1l11l1ll111_opy_[bstack1l11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐂ")]) if st[bstack1l11lll_opy_ (u"࠭ࡩࡥࠩᐃ")] == step[bstack1l11lll_opy_ (u"ࠧࡪࡦࠪᐄ")]), None)
        if index is not None:
            bstack1l11l1ll111_opy_[bstack1l11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐅ")][index] = step
        instance.data[TestFramework.bstack1l111ll1111_opy_] = bstack1l11l1ll111_opy_
    @staticmethod
    def __1l111l1l111_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l11lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᐆ")):
                examples = list(node.callspec.params[bstack1l11lll_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᐇ")].values())
            return examples
        except:
            return []
    def bstack1ll111l1lll_opy_(self, instance: bstack1lll1lllll1_opy_, bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_]):
        bstack1l11l1ll1ll_opy_ = (
            PytestBDDFramework.bstack1l111ll111l_opy_
            if bstack11111l11ll_opy_[1] == bstack1lll1l1l11l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1ll1l_opy_
        )
        hook = PytestBDDFramework.bstack1l11l111l11_opy_(instance, bstack1l11l1ll1ll_opy_)
        entries = hook.get(TestFramework.bstack1l11lll11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l111l1l11l_opy_, []))
        return entries
    def bstack1l1lll1ll1l_opy_(self, instance: bstack1lll1lllll1_opy_, bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_]):
        bstack1l11l1ll1ll_opy_ = (
            PytestBDDFramework.bstack1l111ll111l_opy_
            if bstack11111l11ll_opy_[1] == bstack1lll1l1l11l_opy_.PRE
            else PytestBDDFramework.bstack1l111l1ll1l_opy_
        )
        PytestBDDFramework.bstack1l11l111lll_opy_(instance, bstack1l11l1ll1ll_opy_)
        TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l111l1l11l_opy_, []).clear()
    @staticmethod
    def bstack1l11l111l11_opy_(instance: bstack1lll1lllll1_opy_, bstack1l11l1ll1ll_opy_: str):
        bstack1l11lll1l11_opy_ = (
            PytestBDDFramework.bstack1l111l1l1l1_opy_
            if bstack1l11l1ll1ll_opy_ == PytestBDDFramework.bstack1l111l1ll1l_opy_
            else PytestBDDFramework.bstack1l111l1ll11_opy_
        )
        bstack1l11l1lllll_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1l11l1ll1ll_opy_, None)
        bstack1l11l11ll1l_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1l11lll1l11_opy_, None) if bstack1l11l1lllll_opy_ else None
        return (
            bstack1l11l11ll1l_opy_[bstack1l11l1lllll_opy_][-1]
            if isinstance(bstack1l11l11ll1l_opy_, dict) and len(bstack1l11l11ll1l_opy_.get(bstack1l11l1lllll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11l111lll_opy_(instance: bstack1lll1lllll1_opy_, bstack1l11l1ll1ll_opy_: str):
        hook = PytestBDDFramework.bstack1l11l111l11_opy_(instance, bstack1l11l1ll1ll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11lll11ll_opy_, []).clear()
    @staticmethod
    def __1l111ll11ll_opy_(instance: bstack1lll1lllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᐈ"), None)):
            return
        if os.getenv(bstack1l11lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᐉ"), bstack1l11lll_opy_ (u"ࠨ࠱ࠣᐊ")) != bstack1l11lll_opy_ (u"ࠢ࠲ࠤᐋ"):
            PytestBDDFramework.logger.warning(bstack1l11lll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᐌ"))
            return
        bstack1l111ll1l11_opy_ = {
            bstack1l11lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᐍ"): (PytestBDDFramework.bstack1l111ll111l_opy_, PytestBDDFramework.bstack1l111l1ll11_opy_),
            bstack1l11lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᐎ"): (PytestBDDFramework.bstack1l111l1ll1l_opy_, PytestBDDFramework.bstack1l111l1l1l1_opy_),
        }
        for when in (bstack1l11lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᐏ"), bstack1l11lll_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᐐ"), bstack1l11lll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᐑ")):
            bstack1l111llll11_opy_ = args[1].get_records(when)
            if not bstack1l111llll11_opy_:
                continue
            records = [
                bstack1ll1lllllll_opy_(
                    kind=TestFramework.bstack1l1lllllll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11lll_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᐒ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᐓ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111llll11_opy_
                if isinstance(getattr(r, bstack1l11lll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᐔ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111ll1lll_opy_, bstack1l11lll1l11_opy_ = bstack1l111ll1l11_opy_.get(when, (None, None))
            bstack1l11ll111l1_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1l111ll1lll_opy_, None) if bstack1l111ll1lll_opy_ else None
            bstack1l11l11ll1l_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1l11lll1l11_opy_, None) if bstack1l11ll111l1_opy_ else None
            if isinstance(bstack1l11l11ll1l_opy_, dict) and len(bstack1l11l11ll1l_opy_.get(bstack1l11ll111l1_opy_, [])) > 0:
                hook = bstack1l11l11ll1l_opy_[bstack1l11ll111l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11lll11ll_opy_ in hook:
                    hook[TestFramework.bstack1l11lll11ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l111l1l11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111lllll1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1ll1l111l_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l111llll1l_opy_(request.node, scenario)
        bstack1l11l1l1lll_opy_ = feature.filename
        if not bstack1ll1l111l_opy_ or not test_name or not bstack1l11l1l1lll_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1ll11lll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll11111_opy_: bstack1ll1l111l_opy_,
            TestFramework.bstack1ll1ll111l1_opy_: test_name,
            TestFramework.bstack1l1ll1l1ll1_opy_: bstack1ll1l111l_opy_,
            TestFramework.bstack1l11l11l111_opy_: bstack1l11l1l1lll_opy_,
            TestFramework.bstack1l11ll1l1l1_opy_: PytestBDDFramework.__1l11ll1llll_opy_(feature, scenario),
            TestFramework.bstack1l11lll1111_opy_: code,
            TestFramework.bstack1l1l1ll11ll_opy_: TestFramework.bstack1l11lll111l_opy_,
            TestFramework.bstack1l1l111l1l1_opy_: test_name
        }
    @staticmethod
    def __1l111llll1l_opy_(node, scenario):
        if hasattr(node, bstack1l11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᐕ")):
            parts = node.nodeid.rsplit(bstack1l11lll_opy_ (u"ࠦࡠࠨᐖ"))
            params = parts[-1]
            return bstack1l11lll_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᐗ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11ll1llll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l11lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᐘ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l11lll_opy_ (u"ࠧࡵࡣࡪࡷࠬᐙ")) else [])
    @staticmethod
    def __1l111llllll_opy_(location):
        return bstack1l11lll_opy_ (u"ࠣ࠼࠽ࠦᐚ").join(filter(lambda x: isinstance(x, str), location))