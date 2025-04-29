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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lllll1lll1_opy_,
    bstack1lll1ll111l_opy_,
    bstack1lll1lll1l1_opy_,
    bstack1l11l1111ll_opy_,
    bstack1lll1ll1lll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1llll1111_opy_
from bstack_utils.bstack1llll1l1_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lllll1l1ll_opy_ import bstack1lll1l11ll1_opy_
from bstack_utils.bstack11l1111ll1_opy_ import bstack1ll1l111l1_opy_
bstack1l1lll1llll_opy_ = bstack1l1llll1111_opy_()
bstack1l11l1ll11l_opy_ = 1.0
bstack1ll11111l1l_opy_ = bstack1llllll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᐝ")
bstack1l111l11lll_opy_ = bstack1llllll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᐞ")
bstack1l111l111ll_opy_ = bstack1llllll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᐟ")
bstack1l111l111l1_opy_ = bstack1llllll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᐠ")
bstack1l111l11ll1_opy_ = bstack1llllll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᐡ")
_1l1ll1lllll_opy_ = set()
class bstack1lll11l11ll_opy_(TestFramework):
    bstack1l11ll1l11l_opy_ = bstack1llllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᐢ")
    bstack1l11lll1l1l_opy_ = bstack1llllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᐣ")
    bstack1l11l1ll1l1_opy_ = bstack1llllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᐤ")
    bstack1l111l1llll_opy_ = bstack1llllll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᐥ")
    bstack1l111l1l11l_opy_ = bstack1llllll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᐦ")
    bstack1l11lll11ll_opy_: bool
    bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_  = None
    bstack1lllll1llll_opy_ = None
    bstack1l111l1l111_opy_ = [
        bstack1lllll1lll1_opy_.BEFORE_ALL,
        bstack1lllll1lll1_opy_.AFTER_ALL,
        bstack1lllll1lll1_opy_.BEFORE_EACH,
        bstack1lllll1lll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11lll1lll_opy_: Dict[str, str],
        bstack1ll1l1l11l1_opy_: List[str]=[bstack1llllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᐧ")],
        bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_=None,
        bstack1lllll1llll_opy_=None
    ):
        super().__init__(bstack1ll1l1l11l1_opy_, bstack1l11lll1lll_opy_, bstack1111l1ll11_opy_)
        self.bstack1l11lll11ll_opy_ = any(bstack1llllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᐨ") in item.lower() for item in bstack1ll1l1l11l1_opy_)
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
        if test_framework_state == bstack1lllll1lll1_opy_.TEST or test_framework_state in bstack1lll11l11ll_opy_.bstack1l111l1l111_opy_:
            bstack1l111ll1l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lllll1lll1_opy_.NONE:
            self.logger.warning(bstack1llllll_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᐩ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠥࠦᐪ"))
            return
        if not self.bstack1l11lll11ll_opy_:
            self.logger.warning(bstack1llllll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᐫ") + str(str(self.bstack1ll1l1l11l1_opy_)) + bstack1llllll_opy_ (u"ࠧࠨᐬ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1llllll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐭ") + str(kwargs) + bstack1llllll_opy_ (u"ࠢࠣᐮ"))
            return
        instance = self.__1l111lll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1llllll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᐯ") + str(args) + bstack1llllll_opy_ (u"ࠤࠥᐰ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll11l11ll_opy_.bstack1l111l1l111_opy_ and test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                bstack1ll1ll111l1_opy_ = bstack1lll1llll1l_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack1lll111l11_opy_.value)
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack1llllll_opy_ (u"ࠥ࠾ࠧᐱ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll1ll11_opy_(instance, name, bstack1ll1ll111l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1llllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᐲ").format(e))
        try:
            if not TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1l11ll1111l_opy_) and test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                test = bstack1lll11l11ll_opy_.__1l111ll11l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1llllll_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐳ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠨࠢᐴ"))
            if test_framework_state == bstack1lllll1lll1_opy_.TEST:
                if test_hook_state == bstack1lll1lll1l1_opy_.PRE and not TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll111lllll_opy_):
                    TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll111lllll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1llllll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐵ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠣࠤᐶ"))
                elif test_hook_state == bstack1lll1lll1l1_opy_.POST and not TestFramework.bstack11111lll1l_opy_(instance, TestFramework.bstack1ll11111111_opy_):
                    TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll11111111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1llllll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐷ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠥࠦᐸ"))
            elif test_framework_state == bstack1lllll1lll1_opy_.LOG and test_hook_state == bstack1lll1lll1l1_opy_.POST:
                bstack1lll11l11ll_opy_.__1l11llll11l_opy_(instance, *args)
            elif test_framework_state == bstack1lllll1lll1_opy_.LOG_REPORT and test_hook_state == bstack1lll1lll1l1_opy_.POST:
                self.__1l11l11111l_opy_(instance, *args)
                self.__1l11l1l1ll1_opy_(instance)
            elif test_framework_state in bstack1lll11l11ll_opy_.bstack1l111l1l111_opy_:
                self.__1l11l11ll1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1llllll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᐹ") + str(instance.ref()) + bstack1llllll_opy_ (u"ࠧࠨᐺ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11ll1l1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll11l11ll_opy_.bstack1l111l1l111_opy_ and test_hook_state == bstack1lll1lll1l1_opy_.POST:
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack1llllll_opy_ (u"ࠨ࠺ࠣᐻ")+str(test_framework_state.name)
                bstack1ll1ll111l1_opy_ = TestFramework.bstack1l111lll111_opy_(instance, name)
                bstack1lll1llll1l_opy_.end(EVENTS.bstack1lll111l11_opy_.value, bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᐼ"), bstack1ll1ll111l1_opy_+bstack1llllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᐽ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1llllll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᐾ").format(e))
    def bstack1ll11111lll_opy_(self):
        return self.bstack1l11lll11ll_opy_
    def __1l11l1llll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1llllll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᐿ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11111l11_opy_(rep, [bstack1llllll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᑀ"), bstack1llllll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑁ"), bstack1llllll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᑂ"), bstack1llllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᑃ"), bstack1llllll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᑄ"), bstack1llllll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᑅ")])
        return None
    def __1l11l11111l_opy_(self, instance: bstack1lll1ll111l_opy_, *args):
        result = self.__1l11l1llll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1llll_opy_ = None
        if result.get(bstack1llllll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑆ"), None) == bstack1llllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑇ") and len(args) > 1 and getattr(args[1], bstack1llllll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᑈ"), None) is not None:
            failure = [{bstack1llllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᑉ"): [args[1].excinfo.exconly(), result.get(bstack1llllll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᑊ"), None)]}]
            bstack1111l1llll_opy_ = bstack1llllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᑋ") if bstack1llllll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᑌ") in getattr(args[1].excinfo, bstack1llllll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᑍ"), bstack1llllll_opy_ (u"ࠦࠧᑎ")) else bstack1llllll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᑏ")
        bstack1l11l111l1l_opy_ = result.get(bstack1llllll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑐ"), TestFramework.bstack1l111l1ll1l_opy_)
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
            target = None # bstack1l111lll11l_opy_ bstack1l11ll11l11_opy_ this to be bstack1llllll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑑ")
            if test_framework_state == bstack1lllll1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l111lll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lllll1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1llllll_opy_ (u"ࠣࡰࡲࡨࡪࠨᑒ"), None), bstack1llllll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑓ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1llllll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑔ"), None):
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
        bstack1l11ll11ll1_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11lll1l1l_opy_, {})
        if not key in bstack1l11ll11ll1_opy_:
            bstack1l11ll11ll1_opy_[key] = []
        bstack1l11ll111l1_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11l1ll1l1_opy_, {})
        if not key in bstack1l11ll111l1_opy_:
            bstack1l11ll111l1_opy_[key] = []
        bstack1l111l1l1l1_opy_ = {
            bstack1lll11l11ll_opy_.bstack1l11lll1l1l_opy_: bstack1l11ll11ll1_opy_,
            bstack1lll11l11ll_opy_.bstack1l11l1ll1l1_opy_: bstack1l11ll111l1_opy_,
        }
        if test_hook_state == bstack1lll1lll1l1_opy_.PRE:
            hook = {
                bstack1llllll_opy_ (u"ࠦࡰ࡫ࡹࠣᑕ"): key,
                TestFramework.bstack1l11l1ll1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1l1l1l_opy_: TestFramework.bstack1l11l111ll1_opy_,
                TestFramework.bstack1l111l1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1l111l_opy_: [],
                TestFramework.bstack1l111llll1l_opy_: args[1] if len(args) > 1 else bstack1llllll_opy_ (u"ࠬ࠭ᑖ"),
                TestFramework.bstack1l111ll1lll_opy_: bstack1lll1l11ll1_opy_.bstack1l11l11l11l_opy_()
            }
            bstack1l11ll11ll1_opy_[key].append(hook)
            bstack1l111l1l1l1_opy_[bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_] = key
        elif test_hook_state == bstack1lll1lll1l1_opy_.POST:
            bstack1l11l1111l1_opy_ = bstack1l11ll11ll1_opy_.get(key, [])
            hook = bstack1l11l1111l1_opy_.pop() if bstack1l11l1111l1_opy_ else None
            if hook:
                result = self.__1l11l1llll1_opy_(*args)
                if result:
                    bstack1l11l1l1111_opy_ = result.get(bstack1llllll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑗ"), TestFramework.bstack1l11l111ll1_opy_)
                    if bstack1l11l1l1111_opy_ != TestFramework.bstack1l11l111ll1_opy_:
                        hook[TestFramework.bstack1l11l1l1l1l_opy_] = bstack1l11l1l1111_opy_
                hook[TestFramework.bstack1l111ll111l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll1lll_opy_]= bstack1lll1l11ll1_opy_.bstack1l11l11l11l_opy_()
                self.bstack1l111llll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11llll111_opy_, [])
                if logs: self.bstack1ll111llll1_opy_(instance, logs)
                bstack1l11ll111l1_opy_[key].append(hook)
                bstack1l111l1l1l1_opy_[bstack1lll11l11ll_opy_.bstack1l111l1l11l_opy_] = key
        TestFramework.bstack1l11l1lll1l_opy_(instance, bstack1l111l1l1l1_opy_)
        self.logger.debug(bstack1llllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᑘ") + str(bstack1l11ll111l1_opy_) + bstack1llllll_opy_ (u"ࠣࠤᑙ"))
    def __1l11lll111l_opy_(
        self,
        context: bstack1l11l1111ll_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        test_hook_state: bstack1lll1lll1l1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11111l11_opy_(args[0], [bstack1llllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑚ"), bstack1llllll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᑛ"), bstack1llllll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᑜ"), bstack1llllll_opy_ (u"ࠧ࡯ࡤࡴࠤᑝ"), bstack1llllll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᑞ"), bstack1llllll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᑟ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1llllll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑠ")) else fixturedef.get(bstack1llllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑡ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1llllll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᑢ")) else None
        node = request.node if hasattr(request, bstack1llllll_opy_ (u"ࠦࡳࡵࡤࡦࠤᑣ")) else None
        target = request.node.nodeid if hasattr(node, bstack1llllll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑤ")) else None
        baseid = fixturedef.get(bstack1llllll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᑥ"), None) or bstack1llllll_opy_ (u"ࠢࠣᑦ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1llllll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᑧ")):
            target = bstack1lll11l11ll_opy_.__1l111ll1l1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1llllll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᑨ")) else None
            if target and not TestFramework.bstack11111ll1ll_opy_(target):
                self.__1l11l111lll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1llllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑩ") + str(test_hook_state) + bstack1llllll_opy_ (u"ࠦࠧᑪ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1llllll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᑫ") + str(target) + bstack1llllll_opy_ (u"ࠨࠢᑬ"))
            return None
        instance = TestFramework.bstack11111ll1ll_opy_(target)
        if not instance:
            self.logger.warning(bstack1llllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᑭ") + str(target) + bstack1llllll_opy_ (u"ࠣࠤᑮ"))
            return None
        bstack1l11l11l111_opy_ = TestFramework.bstack111111lll1_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11ll1l11l_opy_, {})
        if os.getenv(bstack1llllll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᑯ"), bstack1llllll_opy_ (u"ࠥ࠵ࠧᑰ")) == bstack1llllll_opy_ (u"ࠦ࠶ࠨᑱ"):
            bstack1l111ll11ll_opy_ = bstack1llllll_opy_ (u"ࠧࡀࠢᑲ").join((scope, fixturename))
            bstack1l11ll1l1ll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll1lll1_opy_ = {
                bstack1llllll_opy_ (u"ࠨ࡫ࡦࡻࠥᑳ"): bstack1l111ll11ll_opy_,
                bstack1llllll_opy_ (u"ࠢࡵࡣࡪࡷࠧᑴ"): bstack1lll11l11ll_opy_.__1l11l1ll111_opy_(request.node),
                bstack1llllll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᑵ"): fixturedef,
                bstack1llllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑶ"): scope,
                bstack1llllll_opy_ (u"ࠥࡸࡾࡶࡥࠣᑷ"): None,
            }
            try:
                if test_hook_state == bstack1lll1lll1l1_opy_.POST and callable(getattr(args[-1], bstack1llllll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᑸ"), None)):
                    bstack1l11ll1lll1_opy_[bstack1llllll_opy_ (u"ࠧࡺࡹࡱࡧࠥᑹ")] = TestFramework.bstack1l1lll1ll11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1lll1l1_opy_.PRE:
                bstack1l11ll1lll1_opy_[bstack1llllll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᑺ")] = uuid4().__str__()
                bstack1l11ll1lll1_opy_[bstack1lll11l11ll_opy_.bstack1l111l1l1ll_opy_] = bstack1l11ll1l1ll_opy_
            elif test_hook_state == bstack1lll1lll1l1_opy_.POST:
                bstack1l11ll1lll1_opy_[bstack1lll11l11ll_opy_.bstack1l111ll111l_opy_] = bstack1l11ll1l1ll_opy_
            if bstack1l111ll11ll_opy_ in bstack1l11l11l111_opy_:
                bstack1l11l11l111_opy_[bstack1l111ll11ll_opy_].update(bstack1l11ll1lll1_opy_)
                self.logger.debug(bstack1llllll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᑻ") + str(bstack1l11l11l111_opy_[bstack1l111ll11ll_opy_]) + bstack1llllll_opy_ (u"ࠣࠤᑼ"))
            else:
                bstack1l11l11l111_opy_[bstack1l111ll11ll_opy_] = bstack1l11ll1lll1_opy_
                self.logger.debug(bstack1llllll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᑽ") + str(len(bstack1l11l11l111_opy_)) + bstack1llllll_opy_ (u"ࠥࠦᑾ"))
        TestFramework.bstack1111l11lll_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11ll1l11l_opy_, bstack1l11l11l111_opy_)
        self.logger.debug(bstack1llllll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᑿ") + str(instance.ref()) + bstack1llllll_opy_ (u"ࠧࠨᒀ"))
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
            bstack1lll11l11ll_opy_.bstack1l11ll1l11l_opy_: {},
            bstack1lll11l11ll_opy_.bstack1l11l1ll1l1_opy_: {},
            bstack1lll11l11ll_opy_.bstack1l11lll1l1l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l11lll_opy_(ob, TestFramework.bstack1l11ll11111_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l11lll_opy_(ob, TestFramework.bstack1ll11lll1l1_opy_, context.platform_index)
        TestFramework.bstack1111l11l11_opy_[ctx.id] = ob
        self.logger.debug(bstack1llllll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᒁ") + str(TestFramework.bstack1111l11l11_opy_.keys()) + bstack1llllll_opy_ (u"ࠢࠣᒂ"))
        return ob
    def bstack1l1lll111l1_opy_(self, instance: bstack1lll1ll111l_opy_, bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_]):
        bstack1l11l11l1l1_opy_ = (
            bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_
            if bstack1111111lll_opy_[1] == bstack1lll1lll1l1_opy_.PRE
            else bstack1lll11l11ll_opy_.bstack1l111l1l11l_opy_
        )
        hook = bstack1lll11l11ll_opy_.bstack1l11l1lll11_opy_(instance, bstack1l11l11l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11l1l111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, []))
        return entries
    def bstack1l1llll1ll1_opy_(self, instance: bstack1lll1ll111l_opy_, bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_]):
        bstack1l11l11l1l1_opy_ = (
            bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_
            if bstack1111111lll_opy_[1] == bstack1lll1lll1l1_opy_.PRE
            else bstack1lll11l11ll_opy_.bstack1l111l1l11l_opy_
        )
        bstack1lll11l11ll_opy_.bstack1l11l11llll_opy_(instance, bstack1l11l11l1l1_opy_)
        TestFramework.bstack111111lll1_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, []).clear()
    def bstack1l111llll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1llllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᒃ")
        global _1l1ll1lllll_opy_
        platform_index = os.environ[bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒄ")]
        bstack1ll1111ll1l_opy_ = os.path.join(bstack1l1lll1llll_opy_, (bstack1ll11111l1l_opy_ + str(platform_index)), bstack1l111l111l1_opy_)
        if not os.path.exists(bstack1ll1111ll1l_opy_) or not os.path.isdir(bstack1ll1111ll1l_opy_):
            self.logger.info(bstack1llllll_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᒅ").format(bstack1ll1111ll1l_opy_))
            return
        logs = hook.get(bstack1llllll_opy_ (u"ࠦࡱࡵࡧࡴࠤᒆ"), [])
        with os.scandir(bstack1ll1111ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1lllll_opy_:
                    self.logger.info(bstack1llllll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒇ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1llllll_opy_ (u"ࠨࠢᒈ")
                    log_entry = bstack1lll1ll1lll_opy_(
                        kind=bstack1llllll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒉ"),
                        message=bstack1llllll_opy_ (u"ࠣࠤᒊ"),
                        level=bstack1llllll_opy_ (u"ࠤࠥᒋ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll111ll_opy_=entry.stat().st_size,
                        bstack1ll111l1ll1_opy_=bstack1llllll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒌ"),
                        bstack11l11_opy_=os.path.abspath(entry.path),
                        bstack1l11ll111ll_opy_=hook.get(TestFramework.bstack1l11l1ll1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1lllll_opy_.add(abs_path)
        platform_index = os.environ[bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᒍ")]
        bstack1l11ll1llll_opy_ = os.path.join(bstack1l1lll1llll_opy_, (bstack1ll11111l1l_opy_ + str(platform_index)), bstack1l111l111l1_opy_, bstack1l111l11ll1_opy_)
        if not os.path.exists(bstack1l11ll1llll_opy_) or not os.path.isdir(bstack1l11ll1llll_opy_):
            self.logger.info(bstack1llllll_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᒎ").format(bstack1l11ll1llll_opy_))
        else:
            self.logger.info(bstack1llllll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᒏ").format(bstack1l11ll1llll_opy_))
            with os.scandir(bstack1l11ll1llll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1lllll_opy_:
                        self.logger.info(bstack1llllll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒐ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1llllll_opy_ (u"ࠣࠤᒑ")
                        log_entry = bstack1lll1ll1lll_opy_(
                            kind=bstack1llllll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒒ"),
                            message=bstack1llllll_opy_ (u"ࠥࠦᒓ"),
                            level=bstack1llllll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᒔ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll111ll_opy_=entry.stat().st_size,
                            bstack1ll111l1ll1_opy_=bstack1llllll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒕ"),
                            bstack11l11_opy_=os.path.abspath(entry.path),
                            bstack1l1lll1l1ll_opy_=hook.get(TestFramework.bstack1l11l1ll1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1lllll_opy_.add(abs_path)
        hook[bstack1llllll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒖ")] = logs
    def bstack1ll111llll1_opy_(
        self,
        bstack1ll111l11ll_opy_: bstack1lll1ll111l_opy_,
        entries: List[bstack1lll1ll1lll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1llllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᒗ"))
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
            log_entry.message = entry.message.encode(bstack1llllll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒘ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1llllll_opy_ (u"ࠤࠥᒙ")
            if entry.kind == bstack1llllll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᒚ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll111ll_opy_
                log_entry.file_path = entry.bstack11l11_opy_
        def bstack1l1lllll1ll_opy_():
            bstack11l1ll1l1_opy_ = datetime.now()
            try:
                self.bstack1lllll1llll_opy_.LogCreatedEvent(req)
                bstack1ll111l11ll_opy_.bstack1lll11111_opy_(bstack1llllll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᒛ"), datetime.now() - bstack11l1ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1llllll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᒜ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll11_opy_.enqueue(bstack1l1lllll1ll_opy_)
    def __1l11l1l1ll1_opy_(self, instance) -> None:
        bstack1llllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒝ")
        bstack1l111l1l1l1_opy_ = {bstack1llllll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᒞ"): bstack1lll1l11ll1_opy_.bstack1l11l11l11l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l1lll1l_opy_(instance, bstack1l111l1l1l1_opy_)
    @staticmethod
    def bstack1l11l1lll11_opy_(instance: bstack1lll1ll111l_opy_, bstack1l11l11l1l1_opy_: str):
        bstack1l111l1lll1_opy_ = (
            bstack1lll11l11ll_opy_.bstack1l11l1ll1l1_opy_
            if bstack1l11l11l1l1_opy_ == bstack1lll11l11ll_opy_.bstack1l111l1l11l_opy_
            else bstack1lll11l11ll_opy_.bstack1l11lll1l1l_opy_
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
        hook = bstack1lll11l11ll_opy_.bstack1l11l1lll11_opy_(instance, bstack1l11l11l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1l111l_opy_, []).clear()
    @staticmethod
    def __1l11llll11l_opy_(instance: bstack1lll1ll111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1llllll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᒟ"), None)):
            return
        if os.getenv(bstack1llllll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᒠ"), bstack1llllll_opy_ (u"ࠥ࠵ࠧᒡ")) != bstack1llllll_opy_ (u"ࠦ࠶ࠨᒢ"):
            bstack1lll11l11ll_opy_.logger.warning(bstack1llllll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᒣ"))
            return
        bstack1l111llllll_opy_ = {
            bstack1llllll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᒤ"): (bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_, bstack1lll11l11ll_opy_.bstack1l11lll1l1l_opy_),
            bstack1llllll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᒥ"): (bstack1lll11l11ll_opy_.bstack1l111l1l11l_opy_, bstack1lll11l11ll_opy_.bstack1l11l1ll1l1_opy_),
        }
        for when in (bstack1llllll_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᒦ"), bstack1llllll_opy_ (u"ࠤࡦࡥࡱࡲࠢᒧ"), bstack1llllll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᒨ")):
            bstack1l111ll1ll1_opy_ = args[1].get_records(when)
            if not bstack1l111ll1ll1_opy_:
                continue
            records = [
                bstack1lll1ll1lll_opy_(
                    kind=TestFramework.bstack1l1lllll111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1llllll_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᒩ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1llllll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᒪ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll1ll1_opy_
                if isinstance(getattr(r, bstack1llllll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᒫ"), None), str) and r.message.strip()
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
    def __1l111ll11l1_opy_(test) -> Dict[str, Any]:
        bstack1lll1l1l11_opy_ = bstack1lll11l11ll_opy_.__1l111ll1l1l_opy_(test.location) if hasattr(test, bstack1llllll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᒬ")) else getattr(test, bstack1llllll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒭ"), None)
        test_name = test.name if hasattr(test, bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒮ")) else None
        bstack1l11l11ll11_opy_ = test.fspath.strpath if hasattr(test, bstack1llllll_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᒯ")) and test.fspath else None
        if not bstack1lll1l1l11_opy_ or not test_name or not bstack1l11l11ll11_opy_:
            return None
        code = None
        if hasattr(test, bstack1llllll_opy_ (u"ࠦࡴࡨࡪࠣᒰ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l11l11_opy_ = []
        try:
            bstack1l111l11l11_opy_ = bstack1ll1l111l1_opy_.bstack111l11ll11_opy_(test)
        except:
            bstack1lll11l11ll_opy_.logger.warning(bstack1llllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᒱ"))
        return {
            TestFramework.bstack1ll1l11l1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll1111l_opy_: bstack1lll1l1l11_opy_,
            TestFramework.bstack1ll1ll11ll1_opy_: test_name,
            TestFramework.bstack1l1ll1l11ll_opy_: getattr(test, bstack1llllll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒲ"), None),
            TestFramework.bstack1l11lll1111_opy_: bstack1l11l11ll11_opy_,
            TestFramework.bstack1l11lll1ll1_opy_: bstack1lll11l11ll_opy_.__1l11l1ll111_opy_(test),
            TestFramework.bstack1l111lllll1_opy_: code,
            TestFramework.bstack1l1l1l1lll1_opy_: TestFramework.bstack1l111l1ll1l_opy_,
            TestFramework.bstack1l1l1111l11_opy_: bstack1lll1l1l11_opy_,
            TestFramework.bstack1l111l11l1l_opy_: bstack1l111l11l11_opy_
        }
    @staticmethod
    def __1l11l1ll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1llllll_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᒳ"), [])
            markers.extend([getattr(m, bstack1llllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᒴ"), None) for m in own_markers if getattr(m, bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒵ"), None)])
            current = getattr(current, bstack1llllll_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᒶ"), None)
        return markers
    @staticmethod
    def __1l111ll1l1l_opy_(location):
        return bstack1llllll_opy_ (u"ࠦ࠿ࡀࠢᒷ").join(filter(lambda x: isinstance(x, str), location))