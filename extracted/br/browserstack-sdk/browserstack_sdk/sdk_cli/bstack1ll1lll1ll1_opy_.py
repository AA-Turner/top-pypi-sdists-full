# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllll11l11_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l1l1ll_opy_ import bstack1l11111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11ll1l1_opy_,
    bstack1ll1lll11ll_opy_,
    bstack1ll1lll1111_opy_,
    bstack11llllll1ll_opy_,
    bstack1lll1ll111l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1ll111l_opy_
from bstack_utils.bstack1lll111l1l_opy_ import bstack1ll1lll1l11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1llll111_opy_ import bstack1ll1llll11l_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1l111l1_opy_
bstack1l1ll1lll11_opy_ = bstack1l1l1ll111l_opy_()
bstack1l111ll111l_opy_ = 1.0
bstack1l1lll1111l_opy_ = bstack1l1_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᓎ")
bstack11lllll1lll_opy_ = bstack1l1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᓏ")
bstack11lllll1ll1_opy_ = bstack1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᓐ")
bstack11lllll11l1_opy_ = bstack1l1_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᓑ")
bstack11lllll11ll_opy_ = bstack1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᓒ")
_1l1ll111lll_opy_ = set()
class bstack1ll1ll1lll1_opy_(TestFramework):
    bstack1l111ll1111_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᓓ")
    bstack1l111111lll_opy_ = bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᓔ")
    bstack1l1111lll11_opy_ = bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᓕ")
    bstack1l1111l1111_opy_ = bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᓖ")
    bstack1l111l11l1l_opy_ = bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᓗ")
    bstack1l11111111l_opy_: bool
    bstack1111111ll1_opy_: bstack111111l1l1_opy_  = None
    bstack1llll11l1l1_opy_ = None
    bstack1l1111ll111_opy_ = [
        bstack1lll11ll1l1_opy_.BEFORE_ALL,
        bstack1lll11ll1l1_opy_.AFTER_ALL,
        bstack1lll11ll1l1_opy_.BEFORE_EACH,
        bstack1lll11ll1l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111111l1l_opy_: Dict[str, str],
        bstack1ll11l11l11_opy_: List[str]=[bstack1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᓘ")],
        bstack1111111ll1_opy_: bstack111111l1l1_opy_=None,
        bstack1llll11l1l1_opy_=None
    ):
        super().__init__(bstack1ll11l11l11_opy_, bstack1l111111l1l_opy_, bstack1111111ll1_opy_)
        self.bstack1l11111111l_opy_ = any(bstack1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᓙ") in item.lower() for item in bstack1ll11l11l11_opy_)
        self.bstack1llll11l1l1_opy_ = bstack1llll11l1l1_opy_
    def track_event(
        self,
        context: bstack11llllll1ll_opy_,
        test_framework_state: bstack1lll11ll1l1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11ll1l1_opy_.TEST or test_framework_state in bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_:
            bstack1l11111l111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11ll1l1_opy_.NONE:
            self.logger.warning(bstack1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᓚ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠧࠨᓛ"))
            return
        if not self.bstack1l11111111l_opy_:
            self.logger.warning(bstack1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᓜ") + str(str(self.bstack1ll11l11l11_opy_)) + bstack1l1_opy_ (u"ࠢࠣᓝ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓞ") + str(kwargs) + bstack1l1_opy_ (u"ࠤࠥᓟ"))
            return
        instance = self.__1l111l11111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᓠ") + str(args) + bstack1l1_opy_ (u"ࠦࠧᓡ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_ and test_hook_state == bstack1ll1lll1111_opy_.PRE:
                bstack1ll1l111l11_opy_ = bstack1ll1lll1l11_opy_.bstack1ll1l11l1ll_opy_(EVENTS.bstack1l1l111lll_opy_.value)
                name = str(EVENTS.bstack1l1l111lll_opy_.name)+bstack1l1_opy_ (u"ࠧࡀࠢᓢ")+str(test_framework_state.name)
                TestFramework.bstack1l111llll1l_opy_(instance, name, bstack1ll1l111l11_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᓣ").format(e))
        try:
            if not TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l111l111l1_opy_) and test_hook_state == bstack1ll1lll1111_opy_.PRE:
                test = bstack1ll1ll1lll1_opy_.__1l11l1111ll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᓤ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠣࠤᓥ"))
            if test_framework_state == bstack1lll11ll1l1_opy_.TEST:
                if test_hook_state == bstack1ll1lll1111_opy_.PRE and not TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_):
                    TestFramework.bstack1llll1ll1ll_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᓦ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠥࠦᓧ"))
                elif test_hook_state == bstack1ll1lll1111_opy_.POST and not TestFramework.bstack1llllllll11_opy_(instance, TestFramework.bstack1l1ll11l11l_opy_):
                    TestFramework.bstack1llll1ll1ll_opy_(instance, TestFramework.bstack1l1ll11l11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᓨ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠧࠨᓩ"))
            elif test_framework_state == bstack1lll11ll1l1_opy_.LOG and test_hook_state == bstack1ll1lll1111_opy_.POST:
                bstack1ll1ll1lll1_opy_.__1l11111ll11_opy_(instance, *args)
            elif test_framework_state == bstack1lll11ll1l1_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1111_opy_.POST:
                self.__1l111lll111_opy_(instance, *args)
                self.__11llllll11l_opy_(instance)
            elif test_framework_state in bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_:
                self.__1l111l1l1ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᓪ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠢࠣᓫ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l1l1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1ll1lll1_opy_.bstack1l1111ll111_opy_ and test_hook_state == bstack1ll1lll1111_opy_.POST:
                name = str(EVENTS.bstack1l1l111lll_opy_.name)+bstack1l1_opy_ (u"ࠣ࠼ࠥᓬ")+str(test_framework_state.name)
                bstack1ll1l111l11_opy_ = TestFramework.bstack1l1111ll1ll_opy_(instance, name)
                bstack1ll1lll1l11_opy_.end(EVENTS.bstack1l1l111lll_opy_.value, bstack1ll1l111l11_opy_+bstack1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᓭ"), bstack1ll1l111l11_opy_+bstack1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᓮ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᓯ").format(e))
    def bstack1l1ll11llll_opy_(self):
        return self.bstack1l11111111l_opy_
    def __11llllllll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᓰ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1ll1111_opy_(rep, [bstack1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦᓱ"), bstack1l1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᓲ"), bstack1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᓳ"), bstack1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᓴ"), bstack1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᓵ"), bstack1l1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᓶ")])
        return None
    def __1l111lll111_opy_(self, instance: bstack1ll1lll11ll_opy_, *args):
        result = self.__11llllllll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111ll1l_opy_ = None
        if result.get(bstack1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᓷ"), None) == bstack1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᓸ") and len(args) > 1 and getattr(args[1], bstack1l1_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᓹ"), None) is not None:
            failure = [{bstack1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᓺ"): [args[1].excinfo.exconly(), result.get(bstack1l1_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᓻ"), None)]}]
            bstack111111ll1l_opy_ = bstack1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᓼ") if bstack1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᓽ") in getattr(args[1].excinfo, bstack1l1_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᓾ"), bstack1l1_opy_ (u"ࠨࠢᓿ")) else bstack1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᔀ")
        bstack1l111111111_opy_ = result.get(bstack1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᔁ"), TestFramework.bstack1l11111l11l_opy_)
        if bstack1l111111111_opy_ != TestFramework.bstack1l11111l11l_opy_:
            TestFramework.bstack1llll1ll1ll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11lllllllll_opy_(instance, {
            TestFramework.bstack1l1l111l1l1_opy_: failure,
            TestFramework.bstack1l11111llll_opy_: bstack111111ll1l_opy_,
            TestFramework.bstack1l11llllll1_opy_: bstack1l111111111_opy_,
        })
    def __1l111l11111_opy_(
        self,
        context: bstack11llllll1ll_opy_,
        test_framework_state: bstack1lll11ll1l1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11ll1l1_opy_.SETUP_FIXTURE:
            instance = self.__1l111l1111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lllllll1l_opy_ bstack1l11l1111l1_opy_ this to be bstack1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᔂ")
            if test_framework_state == bstack1lll11ll1l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1111ll11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11ll1l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣᔃ"), None), bstack1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᔄ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᔅ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lllll111ll_opy_(target) if target else None
        return instance
    def __1l111l1l1ll_opy_(
        self,
        instance: bstack1ll1lll11ll_opy_,
        test_framework_state: bstack1lll11ll1l1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l1l11l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l111111lll_opy_, {})
        if not key in bstack1l111l1l11l_opy_:
            bstack1l111l1l11l_opy_[key] = []
        bstack1l111ll11ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1111lll11_opy_, {})
        if not key in bstack1l111ll11ll_opy_:
            bstack1l111ll11ll_opy_[key] = []
        bstack1l1111l11ll_opy_ = {
            bstack1ll1ll1lll1_opy_.bstack1l111111lll_opy_: bstack1l111l1l11l_opy_,
            bstack1ll1ll1lll1_opy_.bstack1l1111lll11_opy_: bstack1l111ll11ll_opy_,
        }
        if test_hook_state == bstack1ll1lll1111_opy_.PRE:
            hook = {
                bstack1l1_opy_ (u"ࠨ࡫ࡦࡻࠥᔆ"): key,
                TestFramework.bstack11llllll111_opy_: uuid4().__str__(),
                TestFramework.bstack1l111lll1ll_opy_: TestFramework.bstack1l11l111l1l_opy_,
                TestFramework.bstack1l111ll1l11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111l1l11_opy_: [],
                TestFramework.bstack1l111llllll_opy_: args[1] if len(args) > 1 else bstack1l1_opy_ (u"ࠧࠨᔇ"),
                TestFramework.bstack1l11111l1ll_opy_: bstack1ll1llll11l_opy_.bstack1l111l11ll1_opy_()
            }
            bstack1l111l1l11l_opy_[key].append(hook)
            bstack1l1111l11ll_opy_[bstack1ll1ll1lll1_opy_.bstack1l1111l1111_opy_] = key
        elif test_hook_state == bstack1ll1lll1111_opy_.POST:
            bstack1l111l11lll_opy_ = bstack1l111l1l11l_opy_.get(key, [])
            hook = bstack1l111l11lll_opy_.pop() if bstack1l111l11lll_opy_ else None
            if hook:
                result = self.__11llllllll1_opy_(*args)
                if result:
                    bstack1l1111l1l1l_opy_ = result.get(bstack1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᔈ"), TestFramework.bstack1l11l111l1l_opy_)
                    if bstack1l1111l1l1l_opy_ != TestFramework.bstack1l11l111l1l_opy_:
                        hook[TestFramework.bstack1l111lll1ll_opy_] = bstack1l1111l1l1l_opy_
                hook[TestFramework.bstack1l1111l11l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11111l1ll_opy_]= bstack1ll1llll11l_opy_.bstack1l111l11ll1_opy_()
                self.bstack1l111l1ll11_opy_(hook)
                logs = hook.get(TestFramework.bstack11lllllll11_opy_, [])
                if logs: self.bstack1l1lll1ll11_opy_(instance, logs)
                bstack1l111ll11ll_opy_[key].append(hook)
                bstack1l1111l11ll_opy_[bstack1ll1ll1lll1_opy_.bstack1l111l11l1l_opy_] = key
        TestFramework.bstack11lllllllll_opy_(instance, bstack1l1111l11ll_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᔉ") + str(bstack1l111ll11ll_opy_) + bstack1l1_opy_ (u"ࠥࠦᔊ"))
    def __1l111l1111l_opy_(
        self,
        context: bstack11llllll1ll_opy_,
        test_framework_state: bstack1lll11ll1l1_opy_,
        test_hook_state: bstack1ll1lll1111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1ll1111_opy_(args[0], [bstack1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᔋ"), bstack1l1_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᔌ"), bstack1l1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᔍ"), bstack1l1_opy_ (u"ࠢࡪࡦࡶࠦᔎ"), bstack1l1_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᔏ"), bstack1l1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᔐ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᔑ")) else fixturedef.get(bstack1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᔒ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᔓ")) else None
        node = request.node if hasattr(request, bstack1l1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᔔ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᔕ")) else None
        baseid = fixturedef.get(bstack1l1_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᔖ"), None) or bstack1l1_opy_ (u"ࠤࠥᔗ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᔘ")):
            target = bstack1ll1ll1lll1_opy_.__1l1111111l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᔙ")) else None
            if target and not TestFramework.bstack1lllll111ll_opy_(target):
                self.__1l1111ll11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᔚ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠨࠢᔛ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᔜ") + str(target) + bstack1l1_opy_ (u"ࠣࠤᔝ"))
            return None
        instance = TestFramework.bstack1lllll111ll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᔞ") + str(target) + bstack1l1_opy_ (u"ࠥࠦᔟ"))
            return None
        bstack1l1111l1lll_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l111ll1111_opy_, {})
        if os.getenv(bstack1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᔠ"), bstack1l1_opy_ (u"ࠧ࠷ࠢᔡ")) == bstack1l1_opy_ (u"ࠨ࠱ࠣᔢ"):
            bstack1l111ll1lll_opy_ = bstack1l1_opy_ (u"ࠢ࠻ࠤᔣ").join((scope, fixturename))
            bstack1l11111lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111lll11l_opy_ = {
                bstack1l1_opy_ (u"ࠣ࡭ࡨࡽࠧᔤ"): bstack1l111ll1lll_opy_,
                bstack1l1_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᔥ"): bstack1ll1ll1lll1_opy_.__1l11l11l111_opy_(request.node),
                bstack1l1_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᔦ"): fixturedef,
                bstack1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᔧ"): scope,
                bstack1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥᔨ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1111_opy_.POST and callable(getattr(args[-1], bstack1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᔩ"), None)):
                    bstack1l111lll11l_opy_[bstack1l1_opy_ (u"ࠢࡵࡻࡳࡩࠧᔪ")] = TestFramework.bstack1l1l1lll1ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1111_opy_.PRE:
                bstack1l111lll11l_opy_[bstack1l1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᔫ")] = uuid4().__str__()
                bstack1l111lll11l_opy_[bstack1ll1ll1lll1_opy_.bstack1l111ll1l11_opy_] = bstack1l11111lll1_opy_
            elif test_hook_state == bstack1ll1lll1111_opy_.POST:
                bstack1l111lll11l_opy_[bstack1ll1ll1lll1_opy_.bstack1l1111l11l1_opy_] = bstack1l11111lll1_opy_
            if bstack1l111ll1lll_opy_ in bstack1l1111l1lll_opy_:
                bstack1l1111l1lll_opy_[bstack1l111ll1lll_opy_].update(bstack1l111lll11l_opy_)
                self.logger.debug(bstack1l1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᔬ") + str(bstack1l1111l1lll_opy_[bstack1l111ll1lll_opy_]) + bstack1l1_opy_ (u"ࠥࠦᔭ"))
            else:
                bstack1l1111l1lll_opy_[bstack1l111ll1lll_opy_] = bstack1l111lll11l_opy_
                self.logger.debug(bstack1l1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᔮ") + str(len(bstack1l1111l1lll_opy_)) + bstack1l1_opy_ (u"ࠧࠨᔯ"))
        TestFramework.bstack1llll1ll1ll_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l111ll1111_opy_, bstack1l1111l1lll_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᔰ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠢࠣᔱ"))
        return instance
    def __1l1111ll11l_opy_(
        self,
        context: bstack11llllll1ll_opy_,
        test_framework_state: bstack1lll11ll1l1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llllll1l1l_opy_.create_context(target)
        ob = bstack1ll1lll11ll_opy_(ctx, self.bstack1ll11l11l11_opy_, self.bstack1l111111l1l_opy_, test_framework_state)
        TestFramework.bstack11lllllllll_opy_(ob, {
            TestFramework.bstack1ll111l11l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1ll1l11_opy_: context.test_framework_version,
            TestFramework.bstack1l1111ll1l1_opy_: [],
            bstack1ll1ll1lll1_opy_.bstack1l111ll1111_opy_: {},
            bstack1ll1ll1lll1_opy_.bstack1l1111lll11_opy_: {},
            bstack1ll1ll1lll1_opy_.bstack1l111111lll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll1ll1ll_opy_(ob, TestFramework.bstack1l1111111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll1ll1ll_opy_(ob, TestFramework.bstack1ll11l111ll_opy_, context.platform_index)
        TestFramework.bstack1llllll1l11_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᔲ") + str(TestFramework.bstack1llllll1l11_opy_.keys()) + bstack1l1_opy_ (u"ࠤࠥᔳ"))
        return ob
    def bstack1l1l1ll11ll_opy_(self, instance: bstack1ll1lll11ll_opy_, bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_]):
        bstack1l111l11l11_opy_ = (
            bstack1ll1ll1lll1_opy_.bstack1l1111l1111_opy_
            if bstack1111111l1l_opy_[1] == bstack1ll1lll1111_opy_.PRE
            else bstack1ll1ll1lll1_opy_.bstack1l111l11l1l_opy_
        )
        hook = bstack1ll1ll1lll1_opy_.bstack11llllll1l1_opy_(instance, bstack1l111l11l11_opy_)
        entries = hook.get(TestFramework.bstack1l1111l1l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_, []))
        return entries
    def bstack1l1lll1lll1_opy_(self, instance: bstack1ll1lll11ll_opy_, bstack1111111l1l_opy_: Tuple[bstack1lll11ll1l1_opy_, bstack1ll1lll1111_opy_]):
        bstack1l111l11l11_opy_ = (
            bstack1ll1ll1lll1_opy_.bstack1l1111l1111_opy_
            if bstack1111111l1l_opy_[1] == bstack1ll1lll1111_opy_.PRE
            else bstack1ll1ll1lll1_opy_.bstack1l111l11l1l_opy_
        )
        bstack1ll1ll1lll1_opy_.bstack1l11111ll1l_opy_(instance, bstack1l111l11l11_opy_)
        TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_, []).clear()
    def bstack1l111l1ll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᔴ")
        global _1l1ll111lll_opy_
        platform_index = os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᔵ")]
        bstack1l1ll11l1ll_opy_ = os.path.join(bstack1l1ll1lll11_opy_, (bstack1l1lll1111l_opy_ + str(platform_index)), bstack11lllll11l1_opy_)
        if not os.path.exists(bstack1l1ll11l1ll_opy_) or not os.path.isdir(bstack1l1ll11l1ll_opy_):
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᔶ").format(bstack1l1ll11l1ll_opy_))
            return
        logs = hook.get(bstack1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᔷ"), [])
        with os.scandir(bstack1l1ll11l1ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll111lll_opy_:
                    self.logger.info(bstack1l1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᔸ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1_opy_ (u"ࠣࠤᔹ")
                    log_entry = bstack1lll1ll111l_opy_(
                        kind=bstack1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᔺ"),
                        message=bstack1l1_opy_ (u"ࠥࠦᔻ"),
                        level=bstack1l1_opy_ (u"ࠦࠧᔼ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll1l1ll_opy_=entry.stat().st_size,
                        bstack1l1lll11111_opy_=bstack1l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᔽ"),
                        bstack11l111_opy_=os.path.abspath(entry.path),
                        bstack1l111llll11_opy_=hook.get(TestFramework.bstack11llllll111_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll111lll_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᔾ")]
        bstack1l1111lll1l_opy_ = os.path.join(bstack1l1ll1lll11_opy_, (bstack1l1lll1111l_opy_ + str(platform_index)), bstack11lllll11l1_opy_, bstack11lllll11ll_opy_)
        if not os.path.exists(bstack1l1111lll1l_opy_) or not os.path.isdir(bstack1l1111lll1l_opy_):
            self.logger.info(bstack1l1_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᔿ").format(bstack1l1111lll1l_opy_))
        else:
            self.logger.info(bstack1l1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᕀ").format(bstack1l1111lll1l_opy_))
            with os.scandir(bstack1l1111lll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll111lll_opy_:
                        self.logger.info(bstack1l1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᕁ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1_opy_ (u"ࠥࠦᕂ")
                        log_entry = bstack1lll1ll111l_opy_(
                            kind=bstack1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᕃ"),
                            message=bstack1l1_opy_ (u"ࠧࠨᕄ"),
                            level=bstack1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᕅ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll1l1ll_opy_=entry.stat().st_size,
                            bstack1l1lll11111_opy_=bstack1l1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᕆ"),
                            bstack11l111_opy_=os.path.abspath(entry.path),
                            bstack1l1ll11ll11_opy_=hook.get(TestFramework.bstack11llllll111_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll111lll_opy_.add(abs_path)
        hook[bstack1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᕇ")] = logs
    def bstack1l1lll1ll11_opy_(
        self,
        bstack1l1lll1ll1l_opy_: bstack1ll1lll11ll_opy_,
        entries: List[bstack1lll1ll111l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᕈ"))
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll11l111ll_opy_)
        req.execution_context.hash = str(bstack1l1lll1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1ll111l11l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(bstack1l1lll1ll1l_opy_, TestFramework.bstack1l1l1ll1l11_opy_)
            log_entry.uuid = entry.bstack1l111llll11_opy_
            log_entry.test_framework_state = bstack1l1lll1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᕉ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1_opy_ (u"ࠦࠧᕊ")
            if entry.kind == bstack1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᕋ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1l1ll_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1ll11lll1_opy_():
            bstack111l1lll_opy_ = datetime.now()
            try:
                self.bstack1llll11l1l1_opy_.LogCreatedEvent(req)
                bstack1l1lll1ll1l_opy_.bstack11l1l1111_opy_(bstack1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᕌ"), datetime.now() - bstack111l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᕍ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll11lll1_opy_)
    def __11llllll11l_opy_(self, instance) -> None:
        bstack1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᕎ")
        bstack1l1111l11ll_opy_ = {bstack1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᕏ"): bstack1ll1llll11l_opy_.bstack1l111l11ll1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11lllllllll_opy_(instance, bstack1l1111l11ll_opy_)
    @staticmethod
    def bstack11llllll1l1_opy_(instance: bstack1ll1lll11ll_opy_, bstack1l111l11l11_opy_: str):
        bstack1l1111lllll_opy_ = (
            bstack1ll1ll1lll1_opy_.bstack1l1111lll11_opy_
            if bstack1l111l11l11_opy_ == bstack1ll1ll1lll1_opy_.bstack1l111l11l1l_opy_
            else bstack1ll1ll1lll1_opy_.bstack1l111111lll_opy_
        )
        bstack1l1111llll1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111l11l11_opy_, None)
        bstack1l11111l1l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1111lllll_opy_, None) if bstack1l1111llll1_opy_ else None
        return (
            bstack1l11111l1l1_opy_[bstack1l1111llll1_opy_][-1]
            if isinstance(bstack1l11111l1l1_opy_, dict) and len(bstack1l11111l1l1_opy_.get(bstack1l1111llll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11111ll1l_opy_(instance: bstack1ll1lll11ll_opy_, bstack1l111l11l11_opy_: str):
        hook = bstack1ll1ll1lll1_opy_.bstack11llllll1l1_opy_(instance, bstack1l111l11l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111l1l11_opy_, []).clear()
    @staticmethod
    def __1l11111ll11_opy_(instance: bstack1ll1lll11ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᕐ"), None)):
            return
        if os.getenv(bstack1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᕑ"), bstack1l1_opy_ (u"ࠧ࠷ࠢᕒ")) != bstack1l1_opy_ (u"ࠨ࠱ࠣᕓ"):
            bstack1ll1ll1lll1_opy_.logger.warning(bstack1l1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᕔ"))
            return
        bstack1l11l11l11l_opy_ = {
            bstack1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᕕ"): (bstack1ll1ll1lll1_opy_.bstack1l1111l1111_opy_, bstack1ll1ll1lll1_opy_.bstack1l111111lll_opy_),
            bstack1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᕖ"): (bstack1ll1ll1lll1_opy_.bstack1l111l11l1l_opy_, bstack1ll1ll1lll1_opy_.bstack1l1111lll11_opy_),
        }
        for when in (bstack1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᕗ"), bstack1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᕘ"), bstack1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᕙ")):
            bstack1l111l111ll_opy_ = args[1].get_records(when)
            if not bstack1l111l111ll_opy_:
                continue
            records = [
                bstack1lll1ll111l_opy_(
                    kind=TestFramework.bstack1l1llll11l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᕚ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᕛ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111l111ll_opy_
                if isinstance(getattr(r, bstack1l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᕜ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111111ll1_opy_, bstack1l1111lllll_opy_ = bstack1l11l11l11l_opy_.get(when, (None, None))
            bstack1l11l111l11_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l111111ll1_opy_, None) if bstack1l111111ll1_opy_ else None
            bstack1l11111l1l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, bstack1l1111lllll_opy_, None) if bstack1l11l111l11_opy_ else None
            if isinstance(bstack1l11111l1l1_opy_, dict) and len(bstack1l11111l1l1_opy_.get(bstack1l11l111l11_opy_, [])) > 0:
                hook = bstack1l11111l1l1_opy_[bstack1l11l111l11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111l1l11_opy_ in hook:
                    hook[TestFramework.bstack1l1111l1l11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l1111ll_opy_(test) -> Dict[str, Any]:
        bstack1ll111l1ll_opy_ = bstack1ll1ll1lll1_opy_.__1l1111111l1_opy_(test.location) if hasattr(test, bstack1l1_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᕝ")) else getattr(test, bstack1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᕞ"), None)
        test_name = test.name if hasattr(test, bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᕟ")) else None
        bstack1l11l111ll1_opy_ = test.fspath.strpath if hasattr(test, bstack1l1_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᕠ")) and test.fspath else None
        if not bstack1ll111l1ll_opy_ or not test_name or not bstack1l11l111ll1_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1_opy_ (u"ࠨ࡯ࡣ࡬ࠥᕡ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11lllll1l1l_opy_ = []
        try:
            bstack11lllll1l1l_opy_ = bstack11l1l111l1_opy_.bstack1111lllll1_opy_(test)
        except:
            bstack1ll1ll1lll1_opy_.logger.warning(bstack1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᕢ"))
        return {
            TestFramework.bstack1ll111l1lll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l111l1_opy_: bstack1ll111l1ll_opy_,
            TestFramework.bstack1ll11l11ll1_opy_: test_name,
            TestFramework.bstack1l1l1l1l11l_opy_: getattr(test, bstack1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᕣ"), None),
            TestFramework.bstack1l111l1lll1_opy_: bstack1l11l111ll1_opy_,
            TestFramework.bstack1l1111l1ll1_opy_: bstack1ll1ll1lll1_opy_.__1l11l11l111_opy_(test),
            TestFramework.bstack1l11l111111_opy_: code,
            TestFramework.bstack1l11llllll1_opy_: TestFramework.bstack1l11111l11l_opy_,
            TestFramework.bstack1l11l1lll1l_opy_: bstack1ll111l1ll_opy_,
            TestFramework.bstack11lllll1l11_opy_: bstack11lllll1l1l_opy_
        }
    @staticmethod
    def __1l11l11l111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᕤ"), [])
            markers.extend([getattr(m, bstack1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᕥ"), None) for m in own_markers if getattr(m, bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᕦ"), None)])
            current = getattr(current, bstack1l1_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᕧ"), None)
        return markers
    @staticmethod
    def __1l1111111l1_opy_(location):
        return bstack1l1_opy_ (u"ࠨ࠺࠻ࠤᕨ").join(filter(lambda x: isinstance(x, str), location))