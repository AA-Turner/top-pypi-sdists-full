# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack111111ll1l_opy_ import bstack111111l111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1l1l_opy_ import bstack1l11l1l111l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll111ll11_opy_,
    bstack1lll1ll1ll1_opy_,
    bstack1lll1l111l1_opy_,
    bstack1l111lll111_opy_,
    bstack1lll1111ll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1ll111l1ll1_opy_
from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll111111l_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1ll11_opy_
bstack1ll111111ll_opy_ = bstack1ll111l1ll1_opy_()
bstack1l1lll1ll11_opy_ = bstack11lll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦ፮")
bstack1l11ll11lll_opy_ = bstack11lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ፯")
bstack1l111ll11l1_opy_ = bstack11lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ፰")
bstack1l11l111lll_opy_ = 1.0
_1l1ll1ll1ll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1ll11l_opy_ = bstack11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ፱")
    bstack1l111l1llll_opy_ = bstack11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨ፲")
    bstack1l11l11ll1l_opy_ = bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ፳")
    bstack1l11l1ll111_opy_ = bstack11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧ፴")
    bstack1l11lll1l11_opy_ = bstack11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢ፵")
    bstack1l11lll1l1l_opy_: bool
    bstack1111l1l1ll_opy_: bstack1111l1ll11_opy_  = None
    bstack1l111l1l1l1_opy_ = [
        bstack1lll111ll11_opy_.BEFORE_ALL,
        bstack1lll111ll11_opy_.AFTER_ALL,
        bstack1lll111ll11_opy_.BEFORE_EACH,
        bstack1lll111ll11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l1111l1_opy_: Dict[str, str],
        bstack1ll1l111l1l_opy_: List[str]=[bstack11lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ፶")],
        bstack1111l1l1ll_opy_: bstack1111l1ll11_opy_ = None,
        bstack1llllll1l11_opy_=None
    ):
        super().__init__(bstack1ll1l111l1l_opy_, bstack1l11l1111l1_opy_, bstack1111l1l1ll_opy_)
        self.bstack1l11lll1l1l_opy_ = any(bstack11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ፷") in item.lower() for item in bstack1ll1l111l1l_opy_)
        self.bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_
    def track_event(
        self,
        context: bstack1l111lll111_opy_,
        test_framework_state: bstack1lll111ll11_opy_,
        test_hook_state: bstack1lll1l111l1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll111ll11_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_:
            bstack1l11l1l111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll111ll11_opy_.NONE:
            self.logger.warning(bstack11lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣ፸") + str(test_hook_state) + bstack11lll_opy_ (u"ࠣࠤ፹"))
            return
        if not self.bstack1l11lll1l1l_opy_:
            self.logger.warning(bstack11lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥ፺") + str(str(self.bstack1ll1l111l1l_opy_)) + bstack11lll_opy_ (u"ࠥࠦ፻"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ፼") + str(kwargs) + bstack11lll_opy_ (u"ࠧࠨ፽"))
            return
        instance = self.__1l111llll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧ፾") + str(args) + bstack11lll_opy_ (u"ࠢࠣ፿"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_ and test_hook_state == bstack1lll1l111l1_opy_.PRE:
                bstack1ll11lll1l1_opy_ = bstack1ll1llllll1_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l1l1l111l_opy_.value)
                name = str(EVENTS.bstack1l1l1l111l_opy_.name)+bstack11lll_opy_ (u"ࠣ࠼ࠥᎀ")+str(test_framework_state.name)
                TestFramework.bstack1l11lll1lll_opy_(instance, name, bstack1ll11lll1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᎁ").format(e))
        try:
            if test_framework_state == bstack1lll111ll11_opy_.TEST:
                if not TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_) and test_hook_state == bstack1lll1l111l1_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111lll11l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᎂ") + str(test_hook_state) + bstack11lll_opy_ (u"ࠦࠧᎃ"))
                if test_hook_state == bstack1lll1l111l1_opy_.PRE and not TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_):
                    TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11ll11l11_opy_(instance, args)
                    self.logger.debug(bstack11lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᎄ") + str(test_hook_state) + bstack11lll_opy_ (u"ࠨࠢᎅ"))
                elif test_hook_state == bstack1lll1l111l1_opy_.POST and not TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1ll111l11ll_opy_):
                    TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll111l11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᎆ") + str(test_hook_state) + bstack11lll_opy_ (u"ࠣࠤᎇ"))
            elif test_framework_state == bstack1lll111ll11_opy_.STEP:
                if test_hook_state == bstack1lll1l111l1_opy_.PRE:
                    PytestBDDFramework.__1l11l1l1lll_opy_(instance, args)
                elif test_hook_state == bstack1lll1l111l1_opy_.POST:
                    PytestBDDFramework.__1l11l1l11l1_opy_(instance, args)
            elif test_framework_state == bstack1lll111ll11_opy_.LOG and test_hook_state == bstack1lll1l111l1_opy_.POST:
                PytestBDDFramework.__1l11ll111ll_opy_(instance, *args)
            elif test_framework_state == bstack1lll111ll11_opy_.LOG_REPORT and test_hook_state == bstack1lll1l111l1_opy_.POST:
                self.__1l111l1l111_opy_(instance, *args)
                self.__1l111ll1111_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_:
                self.__1l11lll11l1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᎈ") + str(instance.ref()) + bstack11lll_opy_ (u"ࠥࠦᎉ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11ll1l111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_ and test_hook_state == bstack1lll1l111l1_opy_.POST:
                name = str(EVENTS.bstack1l1l1l111l_opy_.name)+bstack11lll_opy_ (u"ࠦ࠿ࠨᎊ")+str(test_framework_state.name)
                bstack1ll11lll1l1_opy_ = TestFramework.bstack1l111l11ll1_opy_(instance, name)
                bstack1ll1llllll1_opy_.end(EVENTS.bstack1l1l1l111l_opy_.value, bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᎋ"), bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᎌ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᎍ").format(e))
    def bstack1ll11111ll1_opy_(self):
        return self.bstack1l11lll1l1l_opy_
    def __1l11ll11l1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᎎ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11111lll_opy_(rep, [bstack11lll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᎏ"), bstack11lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᎐"), bstack11lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ᎑"), bstack11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ᎒"), bstack11lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢ᎓"), bstack11lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ᎔")])
        return None
    def __1l111l1l111_opy_(self, instance: bstack1lll1ll1ll1_opy_, *args):
        result = self.__1l11ll11l1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1llll_opy_ = None
        if result.get(bstack11lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᎕"), None) == bstack11lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᎖") and len(args) > 1 and getattr(args[1], bstack11lll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦ᎗"), None) is not None:
            failure = [{bstack11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᎘"): [args[1].excinfo.exconly(), result.get(bstack11lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦ᎙"), None)]}]
            bstack1111l1llll_opy_ = bstack11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᎚") if bstack11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ᎛") in getattr(args[1].excinfo, bstack11lll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥ᎜"), bstack11lll_opy_ (u"ࠤࠥ᎝")) else bstack11lll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ᎞")
        bstack1l11ll1llll_opy_ = result.get(bstack11lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᎟"), TestFramework.bstack1l11ll11111_opy_)
        if bstack1l11ll1llll_opy_ != TestFramework.bstack1l11ll11111_opy_:
            TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l1l1l11_opy_(instance, {
            TestFramework.bstack1l1l1lll11l_opy_: failure,
            TestFramework.bstack1l11ll11ll1_opy_: bstack1111l1llll_opy_,
            TestFramework.bstack1l1l1lll111_opy_: bstack1l11ll1llll_opy_,
        })
    def __1l111llll1l_opy_(
        self,
        context: bstack1l111lll111_opy_,
        test_framework_state: bstack1lll111ll11_opy_,
        test_hook_state: bstack1lll1l111l1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll111ll11_opy_.SETUP_FIXTURE:
            instance = self.__1l111l1lll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11l1ll1ll_opy_ bstack1l11l1l1ll1_opy_ this to be bstack11lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᎠ")
            if test_framework_state == bstack1lll111ll11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111lll1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll111ll11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᎡ"), None), bstack11lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᎢ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11lll_opy_ (u"ࠣࡰࡲࡨࡪࠨᎣ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11lll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᎤ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111111l11_opy_(target) if target else None
        return instance
    def __1l11lll11l1_opy_(
        self,
        instance: bstack1lll1ll1ll1_opy_,
        test_framework_state: bstack1lll111ll11_opy_,
        test_hook_state: bstack1lll1l111l1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l11lll1_opy_ = TestFramework.bstack111111l1l1_opy_(instance, PytestBDDFramework.bstack1l111l1llll_opy_, {})
        if not key in bstack1l11l11lll1_opy_:
            bstack1l11l11lll1_opy_[key] = []
        bstack1l11ll1l1ll_opy_ = TestFramework.bstack111111l1l1_opy_(instance, PytestBDDFramework.bstack1l11l11ll1l_opy_, {})
        if not key in bstack1l11ll1l1ll_opy_:
            bstack1l11ll1l1ll_opy_[key] = []
        bstack1l111ll1l1l_opy_ = {
            PytestBDDFramework.bstack1l111l1llll_opy_: bstack1l11l11lll1_opy_,
            PytestBDDFramework.bstack1l11l11ll1l_opy_: bstack1l11ll1l1ll_opy_,
        }
        if test_hook_state == bstack1lll1l111l1_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11lll_opy_ (u"ࠥ࡯ࡪࡿࠢᎥ"): key,
                TestFramework.bstack1l11ll111l1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1ll1l1_opy_: TestFramework.bstack1l11l1l1111_opy_,
                TestFramework.bstack1l111ll1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111l1l11l_opy_: [],
                TestFramework.bstack1l11l11111l_opy_: hook_name,
                TestFramework.bstack1l11l111l11_opy_: bstack1llll11l111_opy_.bstack1l111l1ll1l_opy_()
            }
            bstack1l11l11lll1_opy_[key].append(hook)
            bstack1l111ll1l1l_opy_[PytestBDDFramework.bstack1l11l1ll111_opy_] = key
        elif test_hook_state == bstack1lll1l111l1_opy_.POST:
            bstack1l11ll1l1l1_opy_ = bstack1l11l11lll1_opy_.get(key, [])
            hook = bstack1l11ll1l1l1_opy_.pop() if bstack1l11ll1l1l1_opy_ else None
            if hook:
                result = self.__1l11ll11l1l_opy_(*args)
                if result:
                    bstack1l11l111l1l_opy_ = result.get(bstack11lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᎦ"), TestFramework.bstack1l11l1l1111_opy_)
                    if bstack1l11l111l1l_opy_ != TestFramework.bstack1l11l1l1111_opy_:
                        hook[TestFramework.bstack1l11l1ll1l1_opy_] = bstack1l11l111l1l_opy_
                hook[TestFramework.bstack1l11l1lll11_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l111l11_opy_] = bstack1llll11l111_opy_.bstack1l111l1ll1l_opy_()
                self.bstack1l11l111ll1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1111ll_opy_, [])
                self.bstack1ll111l1lll_opy_(instance, logs)
                bstack1l11ll1l1ll_opy_[key].append(hook)
                bstack1l111ll1l1l_opy_[PytestBDDFramework.bstack1l11lll1l11_opy_] = key
        TestFramework.bstack1l11l1l1l11_opy_(instance, bstack1l111ll1l1l_opy_)
        self.logger.debug(bstack11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᎧ") + str(bstack1l11ll1l1ll_opy_) + bstack11lll_opy_ (u"ࠨࠢᎨ"))
    def __1l111l1lll1_opy_(
        self,
        context: bstack1l111lll111_opy_,
        test_framework_state: bstack1lll111ll11_opy_,
        test_hook_state: bstack1lll1l111l1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11111lll_opy_(args[0], [bstack11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᎩ"), bstack11lll_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᎪ"), bstack11lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᎫ"), bstack11lll_opy_ (u"ࠥ࡭ࡩࡹࠢᎬ"), bstack11lll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᎭ"), bstack11lll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᎮ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᎯ")) else fixturedef.get(bstack11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᎰ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᎱ")) else None
        node = request.node if hasattr(request, bstack11lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᎲ")) else None
        target = request.node.nodeid if hasattr(node, bstack11lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᎳ")) else None
        baseid = fixturedef.get(bstack11lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᎴ"), None) or bstack11lll_opy_ (u"ࠧࠨᎵ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11lll_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᎶ")):
            target = PytestBDDFramework.__1l11lll111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᎷ")) else None
            if target and not TestFramework.bstack1111111l11_opy_(target):
                self.__1l111lll1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᎸ") + str(test_hook_state) + bstack11lll_opy_ (u"ࠤࠥᎹ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᎺ") + str(target) + bstack11lll_opy_ (u"ࠦࠧᎻ"))
            return None
        instance = TestFramework.bstack1111111l11_opy_(target)
        if not instance:
            self.logger.warning(bstack11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᎼ") + str(target) + bstack11lll_opy_ (u"ࠨࠢᎽ"))
            return None
        bstack1l11l11l111_opy_ = TestFramework.bstack111111l1l1_opy_(instance, PytestBDDFramework.bstack1l11l1ll11l_opy_, {})
        if os.getenv(bstack11lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᎾ"), bstack11lll_opy_ (u"ࠣ࠳ࠥᎿ")) == bstack11lll_opy_ (u"ࠤ࠴ࠦᏀ"):
            bstack1l111l1ll11_opy_ = bstack11lll_opy_ (u"ࠥ࠾ࠧᏁ").join((scope, fixturename))
            bstack1l11l11ll11_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111lll1l1_opy_ = {
                bstack11lll_opy_ (u"ࠦࡰ࡫ࡹࠣᏂ"): bstack1l111l1ll11_opy_,
                bstack11lll_opy_ (u"ࠧࡺࡡࡨࡵࠥᏃ"): PytestBDDFramework.__1l111llllll_opy_(request.node, scenario),
                bstack11lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᏄ"): fixturedef,
                bstack11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᏅ"): scope,
                bstack11lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᏆ"): None,
            }
            try:
                if test_hook_state == bstack1lll1l111l1_opy_.POST and callable(getattr(args[-1], bstack11lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᏇ"), None)):
                    bstack1l111lll1l1_opy_[bstack11lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᏈ")] = TestFramework.bstack1ll1111llll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1l111l1_opy_.PRE:
                bstack1l111lll1l1_opy_[bstack11lll_opy_ (u"ࠦࡺࡻࡩࡥࠤᏉ")] = uuid4().__str__()
                bstack1l111lll1l1_opy_[PytestBDDFramework.bstack1l111ll1ll1_opy_] = bstack1l11l11ll11_opy_
            elif test_hook_state == bstack1lll1l111l1_opy_.POST:
                bstack1l111lll1l1_opy_[PytestBDDFramework.bstack1l11l1lll11_opy_] = bstack1l11l11ll11_opy_
            if bstack1l111l1ll11_opy_ in bstack1l11l11l111_opy_:
                bstack1l11l11l111_opy_[bstack1l111l1ll11_opy_].update(bstack1l111lll1l1_opy_)
                self.logger.debug(bstack11lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᏊ") + str(bstack1l11l11l111_opy_[bstack1l111l1ll11_opy_]) + bstack11lll_opy_ (u"ࠨࠢᏋ"))
            else:
                bstack1l11l11l111_opy_[bstack1l111l1ll11_opy_] = bstack1l111lll1l1_opy_
                self.logger.debug(bstack11lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᏌ") + str(len(bstack1l11l11l111_opy_)) + bstack11lll_opy_ (u"ࠣࠤᏍ"))
        TestFramework.bstack11111llll1_opy_(instance, PytestBDDFramework.bstack1l11l1ll11l_opy_, bstack1l11l11l111_opy_)
        self.logger.debug(bstack11lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᏎ") + str(instance.ref()) + bstack11lll_opy_ (u"ࠥࠦᏏ"))
        return instance
    def __1l111lll1ll_opy_(
        self,
        context: bstack1l111lll111_opy_,
        test_framework_state: bstack1lll111ll11_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack111111l111_opy_.create_context(target)
        ob = bstack1lll1ll1ll1_opy_(ctx, self.bstack1ll1l111l1l_opy_, self.bstack1l11l1111l1_opy_, test_framework_state)
        TestFramework.bstack1l11l1l1l11_opy_(ob, {
            TestFramework.bstack1ll1l1111l1_opy_: context.test_framework_name,
            TestFramework.bstack1ll111l1111_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1l1ll_opy_: [],
            PytestBDDFramework.bstack1l11l1ll11l_opy_: {},
            PytestBDDFramework.bstack1l11l11ll1l_opy_: {},
            PytestBDDFramework.bstack1l111l1llll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11111llll1_opy_(ob, TestFramework.bstack1l111ll111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11111llll1_opy_(ob, TestFramework.bstack1ll1l1l111l_opy_, context.platform_index)
        TestFramework.bstack111111111l_opy_[ctx.id] = ob
        self.logger.debug(bstack11lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᏐ") + str(TestFramework.bstack111111111l_opy_.keys()) + bstack11lll_opy_ (u"ࠧࠨᏑ"))
        return ob
    @staticmethod
    def __1l11ll11l11_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11lll_opy_ (u"࠭ࡩࡥࠩᏒ"): id(step),
                bstack11lll_opy_ (u"ࠧࡵࡧࡻࡸࠬᏓ"): step.name,
                bstack11lll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᏔ"): step.keyword,
            })
        meta = {
            bstack11lll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᏕ"): {
                bstack11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨᏖ"): feature.name,
                bstack11lll_opy_ (u"ࠫࡵࡧࡴࡩࠩᏗ"): feature.filename,
                bstack11lll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᏘ"): feature.description
            },
            bstack11lll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᏙ"): {
                bstack11lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏚ"): scenario.name
            },
            bstack11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᏛ"): steps,
            bstack11lll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᏜ"): PytestBDDFramework.__1l11ll1111l_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11ll1lll1_opy_: meta
            }
        )
    def bstack1l11l111ll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᏝ")
        global _1l1ll1ll1ll_opy_
        platform_index = os.environ[bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᏞ")]
        bstack1ll1111lll1_opy_ = os.path.join(bstack1ll111111ll_opy_, (bstack1l1lll1ll11_opy_ + str(platform_index)), bstack1l11ll11lll_opy_)
        if not os.path.exists(bstack1ll1111lll1_opy_) or not os.path.isdir(bstack1ll1111lll1_opy_):
            return
        logs = hook.get(bstack11lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᏟ"), [])
        with os.scandir(bstack1ll1111lll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1ll1ll_opy_:
                    self.logger.info(bstack11lll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᏠ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11lll_opy_ (u"ࠢࠣᏡ")
                    log_entry = bstack1lll1111ll1_opy_(
                        kind=bstack11lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᏢ"),
                        message=bstack11lll_opy_ (u"ࠤࠥᏣ"),
                        level=bstack11lll_opy_ (u"ࠥࠦᏤ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llll111l_opy_=entry.stat().st_size,
                        bstack1ll111l11l1_opy_=bstack11lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᏥ"),
                        bstack111ll11_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l11ll_opy_=hook.get(TestFramework.bstack1l11ll111l1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1ll1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᏦ")]
        bstack1l11lll1ll1_opy_ = os.path.join(bstack1ll111111ll_opy_, (bstack1l1lll1ll11_opy_ + str(platform_index)), bstack1l11ll11lll_opy_, bstack1l111ll11l1_opy_)
        if not os.path.exists(bstack1l11lll1ll1_opy_) or not os.path.isdir(bstack1l11lll1ll1_opy_):
            self.logger.info(bstack11lll_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᏧ").format(bstack1l11lll1ll1_opy_))
        else:
            self.logger.info(bstack11lll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᏨ").format(bstack1l11lll1ll1_opy_))
            with os.scandir(bstack1l11lll1ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1ll1ll_opy_:
                        self.logger.info(bstack11lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᏩ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11lll_opy_ (u"ࠤࠥᏪ")
                        log_entry = bstack1lll1111ll1_opy_(
                            kind=bstack11lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᏫ"),
                            message=bstack11lll_opy_ (u"ࠦࠧᏬ"),
                            level=bstack11lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᏭ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llll111l_opy_=entry.stat().st_size,
                            bstack1ll111l11l1_opy_=bstack11lll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᏮ"),
                            bstack111ll11_opy_=os.path.abspath(entry.path),
                            bstack1l1llll1lll_opy_=hook.get(TestFramework.bstack1l11ll111l1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1ll1ll_opy_.add(abs_path)
        hook[bstack11lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᏯ")] = logs
    def bstack1ll111l1lll_opy_(
        self,
        bstack1l1llllll1l_opy_: bstack1lll1ll1ll1_opy_,
        entries: List[bstack1lll1111ll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᏰ"))
        req.platform_index = TestFramework.bstack111111l1l1_opy_(bstack1l1llllll1l_opy_, TestFramework.bstack1ll1l1l111l_opy_)
        req.execution_context.hash = str(bstack1l1llllll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llllll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llllll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack111111l1l1_opy_(bstack1l1llllll1l_opy_, TestFramework.bstack1ll1l1111l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack111111l1l1_opy_(bstack1l1llllll1l_opy_, TestFramework.bstack1ll111l1111_opy_)
            log_entry.uuid = entry.bstack1l11l1l11ll_opy_
            log_entry.test_framework_state = bstack1l1llllll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᏱ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11lll_opy_ (u"ࠥࠦᏲ")
            if entry.kind == bstack11lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᏳ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll111l_opy_
                log_entry.file_path = entry.bstack111ll11_opy_
        def bstack1l1lll1111l_opy_():
            bstack111ll1lll_opy_ = datetime.now()
            try:
                self.bstack1llllll1l11_opy_.LogCreatedEvent(req)
                bstack1l1llllll1l_opy_.bstack11ll111111_opy_(bstack11lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᏴ"), datetime.now() - bstack111ll1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᏵ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1l1ll_opy_.enqueue(bstack1l1lll1111l_opy_)
    def __1l111ll1111_opy_(self, instance) -> None:
        bstack11lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ᏶")
        bstack1l111ll1l1l_opy_ = {bstack11lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥ᏷"): bstack1llll11l111_opy_.bstack1l111l1ll1l_opy_()}
        TestFramework.bstack1l11l1l1l11_opy_(instance, bstack1l111ll1l1l_opy_)
    @staticmethod
    def __1l11l1l1lll_opy_(instance, args):
        request, bstack1l111ll1lll_opy_ = args
        bstack1l111ll1l11_opy_ = id(bstack1l111ll1lll_opy_)
        bstack1l11ll1ll1l_opy_ = instance.data[TestFramework.bstack1l11ll1lll1_opy_]
        step = next(filter(lambda st: st[bstack11lll_opy_ (u"ࠩ࡬ࡨࠬᏸ")] == bstack1l111ll1l11_opy_, bstack1l11ll1ll1l_opy_[bstack11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏹ")]), None)
        step.update({
            bstack11lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᏺ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11ll1ll1l_opy_[bstack11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏻ")]) if st[bstack11lll_opy_ (u"࠭ࡩࡥࠩᏼ")] == step[bstack11lll_opy_ (u"ࠧࡪࡦࠪᏽ")]), None)
        if index is not None:
            bstack1l11ll1ll1l_opy_[bstack11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᏾")][index] = step
        instance.data[TestFramework.bstack1l11ll1lll1_opy_] = bstack1l11ll1ll1l_opy_
    @staticmethod
    def __1l11l1l11l1_opy_(instance, args):
        bstack11lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡷࡩࡧࡱࠤࡱ࡫࡮ࠡࡣࡵ࡫ࡸࠦࡩࡴࠢ࠵࠰ࠥ࡯ࡴࠡࡵ࡬࡫ࡳ࡯ࡦࡪࡧࡶࠤࡹ࡮ࡥࡳࡧࠣ࡭ࡸࠦ࡮ࡰࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࡳࠡࡣࡵࡩࠥ࠳ࠠ࡜ࡴࡨࡵࡺ࡫ࡳࡵ࠮ࠣࡷࡹ࡫ࡰ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭࡫ࠦࡡࡳࡩࡶࠤࡦࡸࡥࠡ࠵ࠣࡸ࡭࡫࡮ࠡࡶ࡫ࡩࠥࡲࡡࡴࡶࠣࡺࡦࡲࡵࡦࠢ࡬ࡷࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ᏿")
        bstack1l111lllll1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l111ll1lll_opy_ = args[1]
        bstack1l111ll1l11_opy_ = id(bstack1l111ll1lll_opy_)
        bstack1l11ll1ll1l_opy_ = instance.data[TestFramework.bstack1l11ll1lll1_opy_]
        step = None
        if bstack1l111ll1l11_opy_ is not None and bstack1l11ll1ll1l_opy_.get(bstack11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᐀")):
            step = next(filter(lambda st: st[bstack11lll_opy_ (u"ࠫ࡮ࡪࠧᐁ")] == bstack1l111ll1l11_opy_, bstack1l11ll1ll1l_opy_[bstack11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐂ")]), None)
            step.update({
                bstack11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᐃ"): bstack1l111lllll1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᐄ"): bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐅ"),
                bstack11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᐆ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐇ"): bstack11lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᐈ"),
                })
        index = next((i for i, st in enumerate(bstack1l11ll1ll1l_opy_[bstack11lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐉ")]) if st[bstack11lll_opy_ (u"࠭ࡩࡥࠩᐊ")] == step[bstack11lll_opy_ (u"ࠧࡪࡦࠪᐋ")]), None)
        if index is not None:
            bstack1l11ll1ll1l_opy_[bstack11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐌ")][index] = step
        instance.data[TestFramework.bstack1l11ll1lll1_opy_] = bstack1l11ll1ll1l_opy_
    @staticmethod
    def __1l11ll1111l_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11lll_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᐍ")):
                examples = list(node.callspec.params[bstack11lll_opy_ (u"ࠪࡣࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡧࡻࡥࡲࡶ࡬ࡦࠩᐎ")].values())
            return examples
        except:
            return []
    def bstack1l1lll11lll_opy_(self, instance: bstack1lll1ll1ll1_opy_, bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_]):
        bstack1l11l11l1l1_opy_ = (
            PytestBDDFramework.bstack1l11l1ll111_opy_
            if bstack1111111ll1_opy_[1] == bstack1lll1l111l1_opy_.PRE
            else PytestBDDFramework.bstack1l11lll1l11_opy_
        )
        hook = PytestBDDFramework.bstack1l11lll1111_opy_(instance, bstack1l11l11l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l111l1l11l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []))
        return entries
    def bstack1ll111ll1l1_opy_(self, instance: bstack1lll1ll1ll1_opy_, bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_]):
        bstack1l11l11l1l1_opy_ = (
            PytestBDDFramework.bstack1l11l1ll111_opy_
            if bstack1111111ll1_opy_[1] == bstack1lll1l111l1_opy_.PRE
            else PytestBDDFramework.bstack1l11lll1l11_opy_
        )
        PytestBDDFramework.bstack1l111ll11ll_opy_(instance, bstack1l11l11l1l1_opy_)
        TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, []).clear()
    @staticmethod
    def bstack1l11lll1111_opy_(instance: bstack1lll1ll1ll1_opy_, bstack1l11l11l1l1_opy_: str):
        bstack1l11l11l1ll_opy_ = (
            PytestBDDFramework.bstack1l11l11ll1l_opy_
            if bstack1l11l11l1l1_opy_ == PytestBDDFramework.bstack1l11lll1l11_opy_
            else PytestBDDFramework.bstack1l111l1llll_opy_
        )
        bstack1l11l1l1l1l_opy_ = TestFramework.bstack111111l1l1_opy_(instance, bstack1l11l11l1l1_opy_, None)
        bstack1l11ll1l11l_opy_ = TestFramework.bstack111111l1l1_opy_(instance, bstack1l11l11l1ll_opy_, None) if bstack1l11l1l1l1l_opy_ else None
        return (
            bstack1l11ll1l11l_opy_[bstack1l11l1l1l1l_opy_][-1]
            if isinstance(bstack1l11ll1l11l_opy_, dict) and len(bstack1l11ll1l11l_opy_.get(bstack1l11l1l1l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111ll11ll_opy_(instance: bstack1lll1ll1ll1_opy_, bstack1l11l11l1l1_opy_: str):
        hook = PytestBDDFramework.bstack1l11lll1111_opy_(instance, bstack1l11l11l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111l1l11l_opy_, []).clear()
    @staticmethod
    def __1l11ll111ll_opy_(instance: bstack1lll1ll1ll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᐏ"), None)):
            return
        if os.getenv(bstack11lll_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᐐ"), bstack11lll_opy_ (u"ࠨ࠱ࠣᐑ")) != bstack11lll_opy_ (u"ࠢ࠲ࠤᐒ"):
            PytestBDDFramework.logger.warning(bstack11lll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᐓ"))
            return
        bstack1l11lll11ll_opy_ = {
            bstack11lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᐔ"): (PytestBDDFramework.bstack1l11l1ll111_opy_, PytestBDDFramework.bstack1l111l1llll_opy_),
            bstack11lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᐕ"): (PytestBDDFramework.bstack1l11lll1l11_opy_, PytestBDDFramework.bstack1l11l11ll1l_opy_),
        }
        for when in (bstack11lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᐖ"), bstack11lll_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᐗ"), bstack11lll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᐘ")):
            bstack1l111l11lll_opy_ = args[1].get_records(when)
            if not bstack1l111l11lll_opy_:
                continue
            records = [
                bstack1lll1111ll1_opy_(
                    kind=TestFramework.bstack1ll111l1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11lll_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᐙ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11lll_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᐚ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111l11lll_opy_
                if isinstance(getattr(r, bstack11lll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᐛ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111llll11_opy_, bstack1l11l11l1ll_opy_ = bstack1l11lll11ll_opy_.get(when, (None, None))
            bstack1l11l1llll1_opy_ = TestFramework.bstack111111l1l1_opy_(instance, bstack1l111llll11_opy_, None) if bstack1l111llll11_opy_ else None
            bstack1l11ll1l11l_opy_ = TestFramework.bstack111111l1l1_opy_(instance, bstack1l11l11l1ll_opy_, None) if bstack1l11l1llll1_opy_ else None
            if isinstance(bstack1l11ll1l11l_opy_, dict) and len(bstack1l11ll1l11l_opy_.get(bstack1l11l1llll1_opy_, [])) > 0:
                hook = bstack1l11ll1l11l_opy_[bstack1l11l1llll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111l1l11l_opy_ in hook:
                    hook[TestFramework.bstack1l111l1l11l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111lll11l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack111111l11_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11ll1ll11_opy_(request.node, scenario)
        bstack1l11l111111_opy_ = feature.filename
        if not bstack111111l11_opy_ or not test_name or not bstack1l11l111111_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l1ll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l1lll1l_opy_: bstack111111l11_opy_,
            TestFramework.bstack1ll1ll1l1ll_opy_: test_name,
            TestFramework.bstack1l1ll1l11ll_opy_: bstack111111l11_opy_,
            TestFramework.bstack1l11l11l11l_opy_: bstack1l11l111111_opy_,
            TestFramework.bstack1l11l1lllll_opy_: PytestBDDFramework.__1l111llllll_opy_(feature, scenario),
            TestFramework.bstack1l11l11llll_opy_: code,
            TestFramework.bstack1l1l1lll111_opy_: TestFramework.bstack1l11ll11111_opy_,
            TestFramework.bstack1l1l111l111_opy_: test_name
        }
    @staticmethod
    def __1l11ll1ll11_opy_(node, scenario):
        if hasattr(node, bstack11lll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᐜ")):
            parts = node.nodeid.rsplit(bstack11lll_opy_ (u"ࠦࡠࠨᐝ"))
            params = parts[-1]
            return bstack11lll_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᐞ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l111llllll_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11lll_opy_ (u"࠭ࡴࡢࡩࡶࠫᐟ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11lll_opy_ (u"ࠧࡵࡣࡪࡷࠬᐠ")) else [])
    @staticmethod
    def __1l11lll111l_opy_(location):
        return bstack11lll_opy_ (u"ࠣ࠼࠽ࠦᐡ").join(filter(lambda x: isinstance(x, str), location))