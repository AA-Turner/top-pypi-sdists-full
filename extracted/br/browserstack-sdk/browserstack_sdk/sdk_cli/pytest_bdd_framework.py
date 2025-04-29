# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack111111llll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll111l1_opy_ import bstack1l111ll1l11_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllll1lll1_opy_,
    bstack1lll1ll111l_opy_,
    bstack1lll1lll1l1_opy_,
    bstack1l11l1111ll_opy_,
    bstack1lll1ll1lll_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1llll1111_opy_
from bstack_utils.bstack1llll1l1_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lllll1l1ll_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
bstack1l1lll1llll_opy_ = bstack1l1llll1111_opy_()
bstack1ll11111l1l_opy_ = bstack1llllll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨ፩")
bstack1l111ll1111_opy_ = bstack1llllll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥ፪")
bstack1l111l1ll11_opy_ = bstack1llllll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ፫")
bstack1l11l1ll11l_opy_ = 1.0
_1l1ll1lllll_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11ll1l11l_opy_ = bstack1llllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ፬")
    bstack1l11lll1l1l_opy_ = bstack1llllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ፭")
    bstack1l11l1ll1l1_opy_ = bstack1llllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ፮")
    bstack1l111l1llll_opy_ = bstack1llllll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢ፯")
    bstack1l111l1l11l_opy_ = bstack1llllll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤ፰")
    bstack1l11lll11ll_opy_: bool
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_  = None
    bstack1l111l1l111_opy_ = [
        bstack1lllll1lll1_opy_.BEFORE_ALL,
        bstack1lllll1lll1_opy_.AFTER_ALL,
        bstack1lllll1lll1_opy_.BEFORE_EACH,
        bstack1lllll1lll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11lll1lll_opy_: Dict[str, str],
        bstack1ll1l1l11l1_opy_: List[str]=[bstack1llllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ፱")],
        bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_ = None,
        bstack1lllll1llll_opy_=None
    ):
        super().__init__(bstack1ll1l1l11l1_opy_, bstack1l11lll1lll_opy_, bstack1111l1ll11_opy_)
        self.bstack1l11lll11ll_opy_ = any(bstack1llllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ፲") in item.lower() for item in bstack1ll1l1l11l1_opy_)
        self.bstack1lllll1llll_opy_ = bstack1lllll1llll_opy_
    def track_event(
        self,
        context: bstack1l11l1111ll_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        test_hook_state: bstack1lll1lll1l1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lllll1lll1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111l1l111_opy_:
            bstack1l111ll1l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllll1lll1_opy_.NONE:
            self.logger.warning(bstack1llllll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥ፳") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠥࠦ፴"))
            return
        if not self.bstack1l11lll11ll_opy_:
            self.logger.warning(bstack1llllll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧ፵") + str(str(self.bstack1ll1l1l11l1_opy_)) + bstack1llllll_opy_ (u"ࠧࠨ፶"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1llllll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ፷") + str(kwargs) + bstack1llllll_opy_ (u"ࠢࠣ፸"))
            return
        instance = self.__1l111lll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1llllll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢ፹") + str(args) + bstack1llllll_opy_ (u"ࠤࠥ፺"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1l111_opy_ and test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                bstack1ll1ll111l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack1lll111l11_opy_.value)
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack1llllll_opy_ (u"ࠥ࠾ࠧ፻")+str(test_framework_state.name)
                TestFramework.bstack1l11ll1ll11_opy_(instance, name, bstack1ll1ll111l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1llllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣ፼").format(e))
        try:
            if test_framework_state == bstack1lllll1lll1_opy_.TEST:
                if not TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11ll1111l_opy_) and test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l111ll11l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1llllll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ፽") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠨࠢ፾"))
                if test_hook_state == bstack1lll1lll1l1_opy_.PRE and not TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111lllll_opy_):
                    TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll111lllll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11lll11l1_opy_(instance, args)
                    self.logger.debug(bstack1llllll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ፿") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠣࠤᎀ"))
                elif test_hook_state == bstack1lll1lll1l1_opy_.POST and not TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll11111111_opy_):
                    TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll11111111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1llllll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎁ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠥࠦᎂ"))
            elif test_framework_state == bstack1lllll1lll1_opy_.STEP:
                if test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                    PytestBDDFramework.__1l111lll1ll_opy_(instance, args)
                elif test_hook_state == bstack1lll1lll1l1_opy_.POST:
                    PytestBDDFramework.__1l11ll11lll_opy_(instance, args)
            elif test_framework_state == bstack1lllll1lll1_opy_.LOG and test_hook_state == bstack1lll1lll1l1_opy_.POST:
                PytestBDDFramework.__1l11llll11l_opy_(instance, *args)
            elif test_framework_state == bstack1lllll1lll1_opy_.LOG_REPORT and test_hook_state == bstack1lll1lll1l1_opy_.POST:
                self.__1l11l11111l_opy_(instance, *args)
                self.__1l11l1l1ll1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111l1l111_opy_:
                self.__1l11l11ll1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1llllll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᎃ") + str(instance.ref()) + bstack1llllll_opy_ (u"ࠧࠨᎄ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11ll1l1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1l111_opy_ and test_hook_state == bstack1lll1lll1l1_opy_.POST:
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack1llllll_opy_ (u"ࠨ࠺ࠣᎅ")+str(test_framework_state.name)
                bstack1ll1ll111l1_opy_ = TestFramework.bstack1l111lll111_opy_(instance, name)
                bstack1lll1llll1l_opy_.end(EVENTS.bstack1lll111l11_opy_.value, bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᎆ"), bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᎇ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1llllll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᎈ").format(e))
    def bstack1ll11111lll_opy_(self):
        return self.bstack1l11lll11ll_opy_
    def __1l11l1llll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1llllll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᎉ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11111l11_opy_(rep, [bstack1llllll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᎊ"), bstack1llllll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᎋ"), bstack1llllll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᎌ"), bstack1llllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᎍ"), bstack1llllll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᎎ"), bstack1llllll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᎏ")])
        return None
    def __1l11l11111l_opy_(self, instance: bstack1lll1ll111l_opy_, *args):
        result = self.__1l11l1llll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1llll_opy_ = None
        if result.get(bstack1llllll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᎐"), None) == bstack1llllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ᎑") and len(args) > 1 and getattr(args[1], bstack1llllll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨ᎒"), None) is not None:
            failure = [{bstack1llllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᎓"): [args[1].excinfo.exconly(), result.get(bstack1llllll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ᎔"), None)]}]
            bstack1111l1llll_opy_ = bstack1llllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ᎕") if bstack1llllll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ᎖") in getattr(args[1].excinfo, bstack1llllll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧ᎗"), bstack1llllll_opy_ (u"ࠦࠧ᎘")) else bstack1llllll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ᎙")
        bstack1l11l111l1l_opy_ = result.get(bstack1llllll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢ᎚"), TestFramework.bstack1l111l1ll1l_opy_)
        if bstack1l11l111l1l_opy_ != TestFramework.bstack1l111l1ll1l_opy_:
            TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l1lll1l_opy_(instance, {
            TestFramework.bstack1l1l1lll11l_opy_: failure,
            TestFramework.bstack1l11l111111_opy_: bstack1111l1llll_opy_,
            TestFramework.bstack1l1l1l1lll1_opy_: bstack1l11l111l1l_opy_,
        })
    def __1l111lll1l1_opy_(
        self,
        context: bstack1l11l1111ll_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        test_hook_state: bstack1lll1lll1l1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lllll1lll1_opy_.SETUP_FIXTURE:
            instance = self.__1l11lll111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111lll11l_opy_ bstack1l11ll11l11_opy_ this to be bstack1llllll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᎛")
            if test_framework_state == bstack1lllll1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l111lll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllll1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1llllll_opy_ (u"ࠣࡰࡲࡨࡪࠨ᎜"), None), bstack1llllll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᎝"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1llllll_opy_ (u"ࠥࡲࡴࡪࡥࠣ᎞"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1llllll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦ᎟"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111ll1ll_opy_(target) if target else None
        return instance
    def __1l11l11ll1l_opy_(
        self,
        instance: bstack1lll1ll111l_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        test_hook_state: bstack1lll1lll1l1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11ll11ll1_opy_ = TestFramework.bstack111111lll1_opy_(instance, PytestBDDFramework.bstack1l11lll1l1l_opy_, {})
        if not key in bstack1l11ll11ll1_opy_:
            bstack1l11ll11ll1_opy_[key] = []
        bstack1l11ll111l1_opy_ = TestFramework.bstack111111lll1_opy_(instance, PytestBDDFramework.bstack1l11l1ll1l1_opy_, {})
        if not key in bstack1l11ll111l1_opy_:
            bstack1l11ll111l1_opy_[key] = []
        bstack1l111l1l1l1_opy_ = {
            PytestBDDFramework.bstack1l11lll1l1l_opy_: bstack1l11ll11ll1_opy_,
            PytestBDDFramework.bstack1l11l1ll1l1_opy_: bstack1l11ll111l1_opy_,
        }
        if test_hook_state == bstack1lll1lll1l1_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1llllll_opy_ (u"ࠧࡱࡥࡺࠤᎠ"): key,
                TestFramework.bstack1l11l1ll1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1l1l1l_opy_: TestFramework.bstack1l11l111ll1_opy_,
                TestFramework.bstack1l111l1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1l111l_opy_: [],
                TestFramework.bstack1l111llll1l_opy_: hook_name,
                TestFramework.bstack1l111ll1lll_opy_: bstack1lll1l11ll1_opy_.bstack1l11l11l11l_opy_()
            }
            bstack1l11ll11ll1_opy_[key].append(hook)
            bstack1l111l1l1l1_opy_[PytestBDDFramework.bstack1l111l1llll_opy_] = key
        elif test_hook_state == bstack1lll1lll1l1_opy_.POST:
            bstack1l11l1111l1_opy_ = bstack1l11ll11ll1_opy_.get(key, [])
            hook = bstack1l11l1111l1_opy_.pop() if bstack1l11l1111l1_opy_ else None
            if hook:
                result = self.__1l11l1llll1_opy_(*args)
                if result:
                    bstack1l11l1l1111_opy_ = result.get(bstack1llllll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᎡ"), TestFramework.bstack1l11l111ll1_opy_)
                    if bstack1l11l1l1111_opy_ != TestFramework.bstack1l11l111ll1_opy_:
                        hook[TestFramework.bstack1l11l1l1l1l_opy_] = bstack1l11l1l1111_opy_
                hook[TestFramework.bstack1l111ll111l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll1lll_opy_] = bstack1lll1l11ll1_opy_.bstack1l11l11l11l_opy_()
                self.bstack1l111llll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11llll111_opy_, [])
                self.bstack1ll111llll1_opy_(instance, logs)
                bstack1l11ll111l1_opy_[key].append(hook)
                bstack1l111l1l1l1_opy_[PytestBDDFramework.bstack1l111l1l11l_opy_] = key
        TestFramework.bstack1l11l1lll1l_opy_(instance, bstack1l111l1l1l1_opy_)
        self.logger.debug(bstack1llllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᎢ") + str(bstack1l11ll111l1_opy_) + bstack1llllll_opy_ (u"ࠣࠤᎣ"))
    def __1l11lll111l_opy_(
        self,
        context: bstack1l11l1111ll_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        test_hook_state: bstack1lll1lll1l1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11111l11_opy_(args[0], [bstack1llllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎤ"), bstack1llllll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᎥ"), bstack1llllll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᎦ"), bstack1llllll_opy_ (u"ࠧ࡯ࡤࡴࠤᎧ"), bstack1llllll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᎨ"), bstack1llllll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᎩ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1llllll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᎪ")) else fixturedef.get(bstack1llllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎫ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1llllll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᎬ")) else None
        node = request.node if hasattr(request, bstack1llllll_opy_ (u"ࠦࡳࡵࡤࡦࠤᎭ")) else None
        target = request.node.nodeid if hasattr(node, bstack1llllll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᎮ")) else None
        baseid = fixturedef.get(bstack1llllll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᎯ"), None) or bstack1llllll_opy_ (u"ࠢࠣᎰ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1llllll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᎱ")):
            target = PytestBDDFramework.__1l111ll1l1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1llllll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᎲ")) else None
            if target and not TestFramework.bstack11111ll1ll_opy_(target):
                self.__1l11l111lll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1llllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎳ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠦࠧᎴ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1llllll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᎵ") + str(target) + bstack1llllll_opy_ (u"ࠨࠢᎶ"))
            return None
        instance = TestFramework.bstack11111ll1ll_opy_(target)
        if not instance:
            self.logger.warning(bstack1llllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᎷ") + str(target) + bstack1llllll_opy_ (u"ࠣࠤᎸ"))
            return None
        bstack1l11l11l111_opy_ = TestFramework.bstack111111lll1_opy_(instance, PytestBDDFramework.bstack1l11ll1l11l_opy_, {})
        if os.getenv(bstack1llllll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᎹ"), bstack1llllll_opy_ (u"ࠥ࠵ࠧᎺ")) == bstack1llllll_opy_ (u"ࠦ࠶ࠨᎻ"):
            bstack1l111ll11ll_opy_ = bstack1llllll_opy_ (u"ࠧࡀࠢᎼ").join((scope, fixturename))
            bstack1l11ll1l1ll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll1lll1_opy_ = {
                bstack1llllll_opy_ (u"ࠨ࡫ࡦࡻࠥᎽ"): bstack1l111ll11ll_opy_,
                bstack1llllll_opy_ (u"ࠢࡵࡣࡪࡷࠧᎾ"): PytestBDDFramework.__1l11l1ll111_opy_(request.node, scenario),
                bstack1llllll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᎿ"): fixturedef,
                bstack1llllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᏀ"): scope,
                bstack1llllll_opy_ (u"ࠥࡸࡾࡶࡥࠣᏁ"): None,
            }
            try:
                if test_hook_state == bstack1lll1lll1l1_opy_.POST and callable(getattr(args[-1], bstack1llllll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᏂ"), None)):
                    bstack1l11ll1lll1_opy_[bstack1llllll_opy_ (u"ࠧࡺࡹࡱࡧࠥᏃ")] = TestFramework.bstack1l1lll1ll11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                bstack1l11ll1lll1_opy_[bstack1llllll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᏄ")] = uuid4().__str__()
                bstack1l11ll1lll1_opy_[PytestBDDFramework.bstack1l111l1l1ll_opy_] = bstack1l11ll1l1ll_opy_
            elif test_hook_state == bstack1lll1lll1l1_opy_.POST:
                bstack1l11ll1lll1_opy_[PytestBDDFramework.bstack1l111ll111l_opy_] = bstack1l11ll1l1ll_opy_
            if bstack1l111ll11ll_opy_ in bstack1l11l11l111_opy_:
                bstack1l11l11l111_opy_[bstack1l111ll11ll_opy_].update(bstack1l11ll1lll1_opy_)
                self.logger.debug(bstack1llllll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᏅ") + str(bstack1l11l11l111_opy_[bstack1l111ll11ll_opy_]) + bstack1llllll_opy_ (u"ࠣࠤᏆ"))
            else:
                bstack1l11l11l111_opy_[bstack1l111ll11ll_opy_] = bstack1l11ll1lll1_opy_
                self.logger.debug(bstack1llllll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᏇ") + str(len(bstack1l11l11l111_opy_)) + bstack1llllll_opy_ (u"ࠥࠦᏈ"))
        TestFramework.bstack1111l11lll_opy_(instance, PytestBDDFramework.bstack1l11ll1l11l_opy_, bstack1l11l11l111_opy_)
        self.logger.debug(bstack1llllll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᏉ") + str(instance.ref()) + bstack1llllll_opy_ (u"ࠧࠨᏊ"))
        return instance
    def __1l11l111lll_opy_(
        self,
        context: bstack1l11l1111ll_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack111111llll_opy_.create_context(target)
        ob = bstack1lll1ll111l_opy_(ctx, self.bstack1ll1l1l11l1_opy_, self.bstack1l11lll1lll_opy_, test_framework_state)
        TestFramework.bstack1l11l1lll1l_opy_(ob, {
            TestFramework.bstack1ll1ll1l1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll11l11_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1lllll_opy_: [],
            PytestBDDFramework.bstack1l11ll1l11l_opy_: {},
            PytestBDDFramework.bstack1l11l1ll1l1_opy_: {},
            PytestBDDFramework.bstack1l11lll1l1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l11lll_opy_(ob, TestFramework.bstack1l11ll11111_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l11lll_opy_(ob, TestFramework.bstack1ll11lll1l1_opy_, context.platform_index)
        TestFramework.bstack1111l11l11_opy_[ctx.id] = ob
        self.logger.debug(bstack1llllll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᏋ") + str(TestFramework.bstack1111l11l11_opy_.keys()) + bstack1llllll_opy_ (u"ࠢࠣᏌ"))
        return ob
    @staticmethod
    def __1l11lll11l1_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1llllll_opy_ (u"ࠨ࡫ࡧࠫᏍ"): id(step),
                bstack1llllll_opy_ (u"ࠩࡷࡩࡽࡺࠧᏎ"): step.name,
                bstack1llllll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᏏ"): step.keyword,
            })
        meta = {
            bstack1llllll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᏐ"): {
                bstack1llllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏑ"): feature.name,
                bstack1llllll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᏒ"): feature.filename,
                bstack1llllll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᏓ"): feature.description
            },
            bstack1llllll_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᏔ"): {
                bstack1llllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏕ"): scenario.name
            },
            bstack1llllll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏖ"): steps,
            bstack1llllll_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭Ꮧ"): PytestBDDFramework.__1l11l11l1ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11l1l1lll_opy_: meta
            }
        )
    def bstack1l111llll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1llllll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᏘ")
        global _1l1ll1lllll_opy_
        platform_index = os.environ[bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮩ")]
        bstack1ll1111ll1l_opy_ = os.path.join(bstack1l1lll1llll_opy_, (bstack1ll11111l1l_opy_ + str(platform_index)), bstack1l111ll1111_opy_)
        if not os.path.exists(bstack1ll1111ll1l_opy_) or not os.path.isdir(bstack1ll1111ll1l_opy_):
            return
        logs = hook.get(bstack1llllll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᏚ"), [])
        with os.scandir(bstack1ll1111ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1lllll_opy_:
                    self.logger.info(bstack1llllll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᏛ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1llllll_opy_ (u"ࠤࠥᏜ")
                    log_entry = bstack1lll1ll1lll_opy_(
                        kind=bstack1llllll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᏝ"),
                        message=bstack1llllll_opy_ (u"ࠦࠧᏞ"),
                        level=bstack1llllll_opy_ (u"ࠧࠨᏟ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll111ll_opy_=entry.stat().st_size,
                        bstack1ll111l1ll1_opy_=bstack1llllll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᏠ"),
                        bstack11l11_opy_=os.path.abspath(entry.path),
                        bstack1l11ll111ll_opy_=hook.get(TestFramework.bstack1l11l1ll1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1lllll_opy_.add(abs_path)
        platform_index = os.environ[bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᏡ")]
        bstack1l11ll1llll_opy_ = os.path.join(bstack1l1lll1llll_opy_, (bstack1ll11111l1l_opy_ + str(platform_index)), bstack1l111ll1111_opy_, bstack1l111l1ll11_opy_)
        if not os.path.exists(bstack1l11ll1llll_opy_) or not os.path.isdir(bstack1l11ll1llll_opy_):
            self.logger.info(bstack1llllll_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᏢ").format(bstack1l11ll1llll_opy_))
        else:
            self.logger.info(bstack1llllll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᏣ").format(bstack1l11ll1llll_opy_))
            with os.scandir(bstack1l11ll1llll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1lllll_opy_:
                        self.logger.info(bstack1llllll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᏤ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1llllll_opy_ (u"ࠦࠧᏥ")
                        log_entry = bstack1lll1ll1lll_opy_(
                            kind=bstack1llllll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏦ"),
                            message=bstack1llllll_opy_ (u"ࠨࠢᏧ"),
                            level=bstack1llllll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᏨ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll111ll_opy_=entry.stat().st_size,
                            bstack1ll111l1ll1_opy_=bstack1llllll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᏩ"),
                            bstack11l11_opy_=os.path.abspath(entry.path),
                            bstack1l1lll1l1ll_opy_=hook.get(TestFramework.bstack1l11l1ll1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1lllll_opy_.add(abs_path)
        hook[bstack1llllll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᏪ")] = logs
    def bstack1ll111llll1_opy_(
        self,
        bstack1ll111l11ll_opy_: bstack1lll1ll111l_opy_,
        entries: List[bstack1lll1ll1lll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1llllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᏫ"))
        req.platform_index = TestFramework.bstack111111lll1_opy_(bstack1ll111l11ll_opy_, TestFramework.bstack1ll11lll1l1_opy_)
        req.execution_context.hash = str(bstack1ll111l11ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll111l11ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll111l11ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack111111lll1_opy_(bstack1ll111l11ll_opy_, TestFramework.bstack1ll1ll1l1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack111111lll1_opy_(bstack1ll111l11ll_opy_, TestFramework.bstack1l1lll11l11_opy_)
            log_entry.uuid = entry.bstack1l11ll111ll_opy_
            log_entry.test_framework_state = bstack1ll111l11ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1llllll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏬ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1llllll_opy_ (u"ࠧࠨᏭ")
            if entry.kind == bstack1llllll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᏮ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll111ll_opy_
                log_entry.file_path = entry.bstack11l11_opy_
        def bstack1l1lllll1ll_opy_():
            bstack11l1ll1l1_opy_ = datetime.now()
            try:
                self.bstack1lllll1llll_opy_.LogCreatedEvent(req)
                bstack1ll111l11ll_opy_.bstack1lll11111_opy_(bstack1llllll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᏯ"), datetime.now() - bstack11l1ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1llllll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢᏰ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1lllll1ll_opy_)
    def __1l11l1l1ll1_opy_(self, instance) -> None:
        bstack1llllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᏱ")
        bstack1l111l1l1l1_opy_ = {bstack1llllll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᏲ"): bstack1lll1l11ll1_opy_.bstack1l11l11l11l_opy_()}
        TestFramework.bstack1l11l1lll1l_opy_(instance, bstack1l111l1l1l1_opy_)
    @staticmethod
    def __1l111lll1ll_opy_(instance, args):
        request, bstack1l11l11lll1_opy_ = args
        bstack1l11l1l1l11_opy_ = id(bstack1l11l11lll1_opy_)
        bstack1l11l1l11ll_opy_ = instance.data[TestFramework.bstack1l11l1l1lll_opy_]
        step = next(filter(lambda st: st[bstack1llllll_opy_ (u"ࠫ࡮ࡪࠧᏳ")] == bstack1l11l1l1l11_opy_, bstack1l11l1l11ll_opy_[bstack1llllll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏴ")]), None)
        step.update({
            bstack1llllll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᏵ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11l1l11ll_opy_[bstack1llllll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭᏶")]) if st[bstack1llllll_opy_ (u"ࠨ࡫ࡧࠫ᏷")] == step[bstack1llllll_opy_ (u"ࠩ࡬ࡨࠬᏸ")]), None)
        if index is not None:
            bstack1l11l1l11ll_opy_[bstack1llllll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏹ")][index] = step
        instance.data[TestFramework.bstack1l11l1l1lll_opy_] = bstack1l11l1l11ll_opy_
    @staticmethod
    def __1l11ll11lll_opy_(instance, args):
        bstack1llllll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᏺ")
        bstack1l11ll1ll1l_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l11l11lll1_opy_ = args[1]
        bstack1l11l1l1l11_opy_ = id(bstack1l11l11lll1_opy_)
        bstack1l11l1l11ll_opy_ = instance.data[TestFramework.bstack1l11l1l1lll_opy_]
        step = None
        if bstack1l11l1l1l11_opy_ is not None and bstack1l11l1l11ll_opy_.get(bstack1llllll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏻ")):
            step = next(filter(lambda st: st[bstack1llllll_opy_ (u"࠭ࡩࡥࠩᏼ")] == bstack1l11l1l1l11_opy_, bstack1l11l1l11ll_opy_[bstack1llllll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᏽ")]), None)
            step.update({
                bstack1llllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᏾"): bstack1l11ll1ll1l_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1llllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᏿"): bstack1llllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᐀"),
                bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᐁ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1llllll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᐂ"): bstack1llllll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᐃ"),
                })
        index = next((i for i, st in enumerate(bstack1l11l1l11ll_opy_[bstack1llllll_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐄ")]) if st[bstack1llllll_opy_ (u"ࠨ࡫ࡧࠫᐅ")] == step[bstack1llllll_opy_ (u"ࠩ࡬ࡨࠬᐆ")]), None)
        if index is not None:
            bstack1l11l1l11ll_opy_[bstack1llllll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐇ")][index] = step
        instance.data[TestFramework.bstack1l11l1l1lll_opy_] = bstack1l11l1l11ll_opy_
    @staticmethod
    def __1l11l11l1ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1llllll_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᐈ")):
                examples = list(node.callspec.params[bstack1llllll_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᐉ")].values())
            return examples
        except:
            return []
    def bstack1l1lll111l1_opy_(self, instance: bstack1lll1ll111l_opy_, bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_]):
        bstack1l11l11l1l1_opy_ = (
            PytestBDDFramework.bstack1l111l1llll_opy_
            if bstack1111111lll_opy_[1] == bstack1lll1lll1l1_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        hook = PytestBDDFramework.bstack1l11l1lll11_opy_(instance, bstack1l11l11l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11l1l111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, []))
        return entries
    def bstack1l1llll1ll1_opy_(self, instance: bstack1lll1ll111l_opy_, bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_]):
        bstack1l11l11l1l1_opy_ = (
            PytestBDDFramework.bstack1l111l1llll_opy_
            if bstack1111111lll_opy_[1] == bstack1lll1lll1l1_opy_.PRE
            else PytestBDDFramework.bstack1l111l1l11l_opy_
        )
        PytestBDDFramework.bstack1l11l11llll_opy_(instance, bstack1l11l11l1l1_opy_)
        TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, []).clear()
    @staticmethod
    def bstack1l11l1lll11_opy_(instance: bstack1lll1ll111l_opy_, bstack1l11l11l1l1_opy_: str):
        bstack1l111l1lll1_opy_ = (
            PytestBDDFramework.bstack1l11l1ll1l1_opy_
            if bstack1l11l11l1l1_opy_ == PytestBDDFramework.bstack1l111l1l11l_opy_
            else PytestBDDFramework.bstack1l11lll1l1l_opy_
        )
        bstack1l11ll1l111_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1l11l11l1l1_opy_, None)
        bstack1l11l1l11l1_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1l111l1lll1_opy_, None) if bstack1l11ll1l111_opy_ else None
        return (
            bstack1l11l1l11l1_opy_[bstack1l11ll1l111_opy_][-1]
            if isinstance(bstack1l11l1l11l1_opy_, dict) and len(bstack1l11l1l11l1_opy_.get(bstack1l11ll1l111_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11l11llll_opy_(instance: bstack1lll1ll111l_opy_, bstack1l11l11l1l1_opy_: str):
        hook = PytestBDDFramework.bstack1l11l1lll11_opy_(instance, bstack1l11l11l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1l111l_opy_, []).clear()
    @staticmethod
    def __1l11llll11l_opy_(instance: bstack1lll1ll111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1llllll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᐊ"), None)):
            return
        if os.getenv(bstack1llllll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᐋ"), bstack1llllll_opy_ (u"ࠣ࠳ࠥᐌ")) != bstack1llllll_opy_ (u"ࠤ࠴ࠦᐍ"):
            PytestBDDFramework.logger.warning(bstack1llllll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᐎ"))
            return
        bstack1l111llllll_opy_ = {
            bstack1llllll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᐏ"): (PytestBDDFramework.bstack1l111l1llll_opy_, PytestBDDFramework.bstack1l11lll1l1l_opy_),
            bstack1llllll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᐐ"): (PytestBDDFramework.bstack1l111l1l11l_opy_, PytestBDDFramework.bstack1l11l1ll1l1_opy_),
        }
        for when in (bstack1llllll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᐑ"), bstack1llllll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᐒ"), bstack1llllll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᐓ")):
            bstack1l111ll1ll1_opy_ = args[1].get_records(when)
            if not bstack1l111ll1ll1_opy_:
                continue
            records = [
                bstack1lll1ll1lll_opy_(
                    kind=TestFramework.bstack1l1lllll111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1llllll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᐔ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1llllll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᐕ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll1ll1_opy_
                if isinstance(getattr(r, bstack1llllll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᐖ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l111l11_opy_, bstack1l111l1lll1_opy_ = bstack1l111llllll_opy_.get(when, (None, None))
            bstack1l11ll11l1l_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1l11l111l11_opy_, None) if bstack1l11l111l11_opy_ else None
            bstack1l11l1l11l1_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1l111l1lll1_opy_, None) if bstack1l11ll11l1l_opy_ else None
            if isinstance(bstack1l11l1l11l1_opy_, dict) and len(bstack1l11l1l11l1_opy_.get(bstack1l11ll11l1l_opy_, [])) > 0:
                hook = bstack1l11l1l11l1_opy_[bstack1l11ll11l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l1l111l_opy_ in hook:
                    hook[TestFramework.bstack1l11l1l111l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111ll11l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1lll1l1l11_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11lll1l11_opy_(request.node, scenario)
        bstack1l11l11ll11_opy_ = feature.filename
        if not bstack1lll1l1l11_opy_ or not test_name or not bstack1l11l11ll11_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l11l1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll1111l_opy_: bstack1lll1l1l11_opy_,
            TestFramework.bstack1ll1ll11ll1_opy_: test_name,
            TestFramework.bstack1l1ll1l11ll_opy_: bstack1lll1l1l11_opy_,
            TestFramework.bstack1l11lll1111_opy_: bstack1l11l11ll11_opy_,
            TestFramework.bstack1l11lll1ll1_opy_: PytestBDDFramework.__1l11l1ll111_opy_(feature, scenario),
            TestFramework.bstack1l111lllll1_opy_: code,
            TestFramework.bstack1l1l1l1lll1_opy_: TestFramework.bstack1l111l1ll1l_opy_,
            TestFramework.bstack1l1l1111l11_opy_: test_name
        }
    @staticmethod
    def __1l11lll1l11_opy_(node, scenario):
        if hasattr(node, bstack1llllll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᐗ")):
            parts = node.nodeid.rsplit(bstack1llllll_opy_ (u"ࠨ࡛ࠣᐘ"))
            params = parts[-1]
            return bstack1llllll_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᐙ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1ll111_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1llllll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐚ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1llllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᐛ")) else [])
    @staticmethod
    def __1l111ll1l1l_opy_(location):
        return bstack1llllll_opy_ (u"ࠥ࠾࠿ࠨᐜ").join(filter(lambda x: isinstance(x, str), location))