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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1lll1lll_opy_,
    bstack1lll1lllll1_opy_,
    bstack1lll111llll_opy_,
    bstack1l111111l11_opy_,
    bstack1ll1lll1l11_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lll11111_opy_
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11ll1ll_opy_ import bstack1lll111l111_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11llll1l11_opy_
bstack1l1ll1ll111_opy_ = bstack1l1lll11111_opy_()
bstack1l111lll11l_opy_ = 1.0
bstack1l1ll11l11l_opy_ = bstack111l111_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᓔ")
bstack11lllll1111_opy_ = bstack111l111_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᓕ")
bstack11lllll1l1l_opy_ = bstack111l111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᓖ")
bstack11lllll1l11_opy_ = bstack111l111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᓗ")
bstack11lllll11l1_opy_ = bstack111l111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᓘ")
_1l1ll1l1111_opy_ = set()
class bstack1lll1l111ll_opy_(TestFramework):
    bstack1l11111ll1l_opy_ = bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᓙ")
    bstack1l11l1111ll_opy_ = bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᓚ")
    bstack1l11l11111l_opy_ = bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᓛ")
    bstack11lllllllll_opy_ = bstack111l111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᓜ")
    bstack1l111lll111_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᓝ")
    bstack1l111ll1111_opy_: bool
    bstack1111111lll_opy_: bstack111111l1l1_opy_  = None
    bstack1lll1l11l1l_opy_ = None
    bstack1l111ll1l1l_opy_ = [
        bstack1ll1lll1lll_opy_.BEFORE_ALL,
        bstack1ll1lll1lll_opy_.AFTER_ALL,
        bstack1ll1lll1lll_opy_.BEFORE_EACH,
        bstack1ll1lll1lll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111111ll1_opy_: Dict[str, str],
        bstack1ll11l11ll1_opy_: List[str]=[bstack111l111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᓞ")],
        bstack1111111lll_opy_: bstack111111l1l1_opy_=None,
        bstack1lll1l11l1l_opy_=None
    ):
        super().__init__(bstack1ll11l11ll1_opy_, bstack1l111111ll1_opy_, bstack1111111lll_opy_)
        self.bstack1l111ll1111_opy_ = any(bstack111l111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᓟ") in item.lower() for item in bstack1ll11l11ll1_opy_)
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
        if test_framework_state == bstack1ll1lll1lll_opy_.TEST or test_framework_state in bstack1lll1l111ll_opy_.bstack1l111ll1l1l_opy_:
            bstack11llllll111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1lll1lll_opy_.NONE:
            self.logger.warning(bstack111l111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᓠ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠦࠧᓡ"))
            return
        if not self.bstack1l111ll1111_opy_:
            self.logger.warning(bstack111l111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᓢ") + str(str(self.bstack1ll11l11ll1_opy_)) + bstack111l111_opy_ (u"ࠨࠢᓣ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111l111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᓤ") + str(kwargs) + bstack111l111_opy_ (u"ࠣࠤᓥ"))
            return
        instance = self.__1l1111ll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᓦ") + str(args) + bstack111l111_opy_ (u"ࠥࠦᓧ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1l111ll_opy_.bstack1l111ll1l1l_opy_ and test_hook_state == bstack1lll111llll_opy_.PRE:
                bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack11ll1l11l_opy_.value)
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack111l111_opy_ (u"ࠦ࠿ࠨᓨ")+str(test_framework_state.name)
                TestFramework.bstack1l111ll1lll_opy_(instance, name, bstack1ll11llll11_opy_)
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲࠡࡲࡵࡩ࠿ࠦࡻࡾࠤᓩ").format(e))
        try:
            if not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l111l1111l_opy_) and test_hook_state == bstack1lll111llll_opy_.PRE:
                test = bstack1lll1l111ll_opy_.__1l111l1llll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111l111_opy_ (u"ࠨ࡬ࡰࡣࡧࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᓪ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠢࠣᓫ"))
            if test_framework_state == bstack1ll1lll1lll_opy_.TEST:
                if test_hook_state == bstack1lll111llll_opy_.PRE and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l111_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᓬ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠤࠥᓭ"))
                elif test_hook_state == bstack1lll111llll_opy_.POST and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_):
                    TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111l111_opy_ (u"ࠥࡷࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᓮ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠦࠧᓯ"))
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG and test_hook_state == bstack1lll111llll_opy_.POST:
                bstack1lll1l111ll_opy_.__1l111ll1ll1_opy_(instance, *args)
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG_REPORT and test_hook_state == bstack1lll111llll_opy_.POST:
                self.__1l1111lll1l_opy_(instance, *args)
                self.__1l111ll11l1_opy_(instance)
            elif test_framework_state in bstack1lll1l111ll_opy_.bstack1l111ll1l1l_opy_:
                self.__1l111l111ll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᓰ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠨࠢᓱ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1111111ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1l111ll_opy_.bstack1l111ll1l1l_opy_ and test_hook_state == bstack1lll111llll_opy_.POST:
                name = str(EVENTS.bstack11ll1l11l_opy_.name)+bstack111l111_opy_ (u"ࠢ࠻ࠤᓲ")+str(test_framework_state.name)
                bstack1ll11llll11_opy_ = TestFramework.bstack1l11l1111l1_opy_(instance, name)
                bstack1llll1111l1_opy_.end(EVENTS.bstack11ll1l11l_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᓳ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᓴ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥᓵ").format(e))
    def bstack1l1lll1ll11_opy_(self):
        return self.bstack1l111ll1111_opy_
    def __1l11l111ll1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111l111_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᓶ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll11l1l1_opy_(rep, [bstack111l111_opy_ (u"ࠧࡽࡨࡦࡰࠥᓷ"), bstack111l111_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᓸ"), bstack111l111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᓹ"), bstack111l111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᓺ"), bstack111l111_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠥᓻ"), bstack111l111_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᓼ")])
        return None
    def __1l1111lll1l_opy_(self, instance: bstack1lll1lllll1_opy_, *args):
        result = self.__1l11l111ll1_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111llll_opy_ = None
        if result.get(bstack111l111_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᓽ"), None) == bstack111l111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᓾ") and len(args) > 1 and getattr(args[1], bstack111l111_opy_ (u"ࠨࡥࡹࡥ࡬ࡲ࡫ࡵࠢᓿ"), None) is not None:
            failure = [{bstack111l111_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᔀ"): [args[1].excinfo.exconly(), result.get(bstack111l111_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᔁ"), None)]}]
            bstack111111llll_opy_ = bstack111l111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᔂ") if bstack111l111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᔃ") in getattr(args[1].excinfo, bstack111l111_opy_ (u"ࠦࡹࡿࡰࡦࡰࡤࡱࡪࠨᔄ"), bstack111l111_opy_ (u"ࠧࠨᔅ")) else bstack111l111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᔆ")
        bstack1l111l11l1l_opy_ = result.get(bstack111l111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᔇ"), TestFramework.bstack1l111llll1l_opy_)
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
            target = None # bstack1l1111l1ll1_opy_ bstack1l1111l1l1l_opy_ this to be bstack111l111_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᔈ")
            if test_framework_state == bstack1ll1lll1lll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lllllll1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack111l111_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᔉ"), None), bstack111l111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᔊ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111l111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᔋ"), None):
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
        bstack1l1111ll111_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11l1111ll_opy_, {})
        if not key in bstack1l1111ll111_opy_:
            bstack1l1111ll111_opy_[key] = []
        bstack1l1111l111l_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11l11111l_opy_, {})
        if not key in bstack1l1111l111l_opy_:
            bstack1l1111l111l_opy_[key] = []
        bstack1l1111ll11l_opy_ = {
            bstack1lll1l111ll_opy_.bstack1l11l1111ll_opy_: bstack1l1111ll111_opy_,
            bstack1lll1l111ll_opy_.bstack1l11l11111l_opy_: bstack1l1111l111l_opy_,
        }
        if test_hook_state == bstack1lll111llll_opy_.PRE:
            hook = {
                bstack111l111_opy_ (u"ࠧࡱࡥࡺࠤᔌ"): key,
                TestFramework.bstack1l111111lll_opy_: uuid4().__str__(),
                TestFramework.bstack11llllll11l_opy_: TestFramework.bstack1l111l1l1l1_opy_,
                TestFramework.bstack11lllllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11111l1l1_opy_: [],
                TestFramework.bstack1l1111l1111_opy_: args[1] if len(args) > 1 else bstack111l111_opy_ (u"࠭ࠧᔍ"),
                TestFramework.bstack1l111l11l11_opy_: bstack1lll111l111_opy_.bstack1l111ll111l_opy_()
            }
            bstack1l1111ll111_opy_[key].append(hook)
            bstack1l1111ll11l_opy_[bstack1lll1l111ll_opy_.bstack11lllllllll_opy_] = key
        elif test_hook_state == bstack1lll111llll_opy_.POST:
            bstack1l11111lll1_opy_ = bstack1l1111ll111_opy_.get(key, [])
            hook = bstack1l11111lll1_opy_.pop() if bstack1l11111lll1_opy_ else None
            if hook:
                result = self.__1l11l111ll1_opy_(*args)
                if result:
                    bstack1l11l111l11_opy_ = result.get(bstack111l111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᔎ"), TestFramework.bstack1l111l1l1l1_opy_)
                    if bstack1l11l111l11_opy_ != TestFramework.bstack1l111l1l1l1_opy_:
                        hook[TestFramework.bstack11llllll11l_opy_] = bstack1l11l111l11_opy_
                hook[TestFramework.bstack1l11l111lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l11l11_opy_]= bstack1lll111l111_opy_.bstack1l111ll111l_opy_()
                self.bstack1l1111lll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1l1ll_opy_, [])
                if logs: self.bstack1l1l1ll1l11_opy_(instance, logs)
                bstack1l1111l111l_opy_[key].append(hook)
                bstack1l1111ll11l_opy_[bstack1lll1l111ll_opy_.bstack1l111lll111_opy_] = key
        TestFramework.bstack1l1111ll1l1_opy_(instance, bstack1l1111ll11l_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡩࡱࡲ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼ࡭ࡨࡽࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࡀࡿ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࢁࠥ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡃࠢᔏ") + str(bstack1l1111l111l_opy_) + bstack111l111_opy_ (u"ࠤࠥᔐ"))
    def __1l1111l11ll_opy_(
        self,
        context: bstack1l111111l11_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        test_hook_state: bstack1lll111llll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll11l1l1_opy_(args[0], [bstack111l111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᔑ"), bstack111l111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᔒ"), bstack111l111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᔓ"), bstack111l111_opy_ (u"ࠨࡩࡥࡵࠥᔔ"), bstack111l111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᔕ"), bstack111l111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᔖ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack111l111_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᔗ")) else fixturedef.get(bstack111l111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᔘ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111l111_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᔙ")) else None
        node = request.node if hasattr(request, bstack111l111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᔚ")) else None
        target = request.node.nodeid if hasattr(node, bstack111l111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᔛ")) else None
        baseid = fixturedef.get(bstack111l111_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᔜ"), None) or bstack111l111_opy_ (u"ࠣࠤᔝ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111l111_opy_ (u"ࠤࡢࡴࡾ࡬ࡵ࡯ࡥ࡬ࡸࡪࡳࠢᔞ")):
            target = bstack1lll1l111ll_opy_.__1l111l1ll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111l111_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᔟ")) else None
            if target and not TestFramework.bstack1lllll11l1l_opy_(target):
                self.__11lllllll1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111l111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡫ࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦ࡮ࡰࡦࡨࡁࢀࡴ࡯ࡥࡧࢀࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࠨᔠ") + str(test_hook_state) + bstack111l111_opy_ (u"ࠧࠨᔡ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111l111_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᔢ") + str(target) + bstack111l111_opy_ (u"ࠢࠣᔣ"))
            return None
        instance = TestFramework.bstack1lllll11l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack111l111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡣࡣࡶࡩ࡮ࡪ࠽ࡼࡤࡤࡷࡪ࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᔤ") + str(target) + bstack111l111_opy_ (u"ࠤࠥᔥ"))
            return None
        bstack1l111ll11ll_opy_ = TestFramework.bstack1111111l1l_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11111ll1l_opy_, {})
        if os.getenv(bstack111l111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡉࡍ࡝࡚ࡕࡓࡇࡖࠦᔦ"), bstack111l111_opy_ (u"ࠦ࠶ࠨᔧ")) == bstack111l111_opy_ (u"ࠧ࠷ࠢᔨ"):
            bstack1l111l11111_opy_ = bstack111l111_opy_ (u"ࠨ࠺ࠣᔩ").join((scope, fixturename))
            bstack1l111l111l1_opy_ = datetime.now(tz=timezone.utc)
            bstack11llllllll1_opy_ = {
                bstack111l111_opy_ (u"ࠢ࡬ࡧࡼࠦᔪ"): bstack1l111l11111_opy_,
                bstack111l111_opy_ (u"ࠣࡶࡤ࡫ࡸࠨᔫ"): bstack1lll1l111ll_opy_.__1l111111l1l_opy_(request.node),
                bstack111l111_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࠥᔬ"): fixturedef,
                bstack111l111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᔭ"): scope,
                bstack111l111_opy_ (u"ࠦࡹࡿࡰࡦࠤᔮ"): None,
            }
            try:
                if test_hook_state == bstack1lll111llll_opy_.POST and callable(getattr(args[-1], bstack111l111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᔯ"), None)):
                    bstack11llllllll1_opy_[bstack111l111_opy_ (u"ࠨࡴࡺࡲࡨࠦᔰ")] = TestFramework.bstack1l1lll1l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111llll_opy_.PRE:
                bstack11llllllll1_opy_[bstack111l111_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᔱ")] = uuid4().__str__()
                bstack11llllllll1_opy_[bstack1lll1l111ll_opy_.bstack11lllllll11_opy_] = bstack1l111l111l1_opy_
            elif test_hook_state == bstack1lll111llll_opy_.POST:
                bstack11llllllll1_opy_[bstack1lll1l111ll_opy_.bstack1l11l111lll_opy_] = bstack1l111l111l1_opy_
            if bstack1l111l11111_opy_ in bstack1l111ll11ll_opy_:
                bstack1l111ll11ll_opy_[bstack1l111l11111_opy_].update(bstack11llllllll1_opy_)
                self.logger.debug(bstack111l111_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࠤᔲ") + str(bstack1l111ll11ll_opy_[bstack1l111l11111_opy_]) + bstack111l111_opy_ (u"ࠤࠥᔳ"))
            else:
                bstack1l111ll11ll_opy_[bstack1l111l11111_opy_] = bstack11llllllll1_opy_
                self.logger.debug(bstack111l111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡾࠢࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࠨᔴ") + str(len(bstack1l111ll11ll_opy_)) + bstack111l111_opy_ (u"ࠦࠧᔵ"))
        TestFramework.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11111ll1l_opy_, bstack1l111ll11ll_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࡻ࡭ࡧࡱࠬࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠩࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᔶ") + str(instance.ref()) + bstack111l111_opy_ (u"ࠨࠢᔷ"))
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
            bstack1lll1l111ll_opy_.bstack1l11111ll1l_opy_: {},
            bstack1lll1l111ll_opy_.bstack1l11l11111l_opy_: {},
            bstack1lll1l111ll_opy_.bstack1l11l1111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1l11111111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111111111_opy_(ob, TestFramework.bstack1ll11l1lll1_opy_, context.platform_index)
        TestFramework.bstack1lllll1llll_opy_[ctx.id] = ob
        self.logger.debug(bstack111l111_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡥࡷࡼ࠳࡯ࡤ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᔸ") + str(TestFramework.bstack1lllll1llll_opy_.keys()) + bstack111l111_opy_ (u"ࠣࠤᔹ"))
        return ob
    def bstack1l1ll1ll11l_opy_(self, instance: bstack1lll1lllll1_opy_, bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_]):
        bstack1l111lll1l1_opy_ = (
            bstack1lll1l111ll_opy_.bstack11lllllllll_opy_
            if bstack1llllll111l_opy_[1] == bstack1lll111llll_opy_.PRE
            else bstack1lll1l111ll_opy_.bstack1l111lll111_opy_
        )
        hook = bstack1lll1l111ll_opy_.bstack1l1111l1lll_opy_(instance, bstack1l111lll1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11111l1l1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1111lllll_opy_, []))
        return entries
    def bstack1l1lll1ll1l_opy_(self, instance: bstack1lll1lllll1_opy_, bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_]):
        bstack1l111lll1l1_opy_ = (
            bstack1lll1l111ll_opy_.bstack11lllllllll_opy_
            if bstack1llllll111l_opy_[1] == bstack1lll111llll_opy_.PRE
            else bstack1lll1l111ll_opy_.bstack1l111lll111_opy_
        )
        bstack1lll1l111ll_opy_.bstack1l1111l1l11_opy_(instance, bstack1l111lll1l1_opy_)
        TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1111lllll_opy_, []).clear()
    def bstack1l1111lll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111l111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡳࡱࡦࡩࡸࡹࡥࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤࡹ࡮ࡥࠡࡌࡤࡺࡦࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗ࡬࡮ࡹࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡃࡩࡧࡦ࡯ࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢ࡬ࡲࡸ࡯ࡤࡦࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡉࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠭ࠢࡵࡩࡵࡲࡡࡤࡧࡶࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦࠥ࡯࡮ࠡ࡫ࡷࡷࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡌࡪࠥࡧࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡯ࡤࡸࡨ࡮ࡥࡴࠢࡤࠤࡲࡵࡤࡪࡨ࡬ࡩࡩࠦࡨࡰࡱ࡮࠱ࡱ࡫ࡶࡦ࡮ࠣࡪ࡮ࡲࡥ࠭ࠢ࡬ࡸࠥࡩࡲࡦࡣࡷࡩࡸࠦࡡࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࠣࡻ࡮ࡺࡨࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡥࡵࡣ࡬ࡰࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡙ࠥࡩ࡮࡫࡯ࡥࡷࡲࡹ࠭ࠢ࡬ࡸࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡴࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡥࡽࠥࡸࡥࡱ࡮ࡤࡧ࡮ࡴࡧࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡖ࡫ࡩࠥࡩࡲࡦࡣࡷࡩࡩࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡤࡶࡪࠦࡡࡥࡦࡨࡨࠥࡺ࡯ࠡࡶ࡫ࡩࠥ࡮࡯ࡰ࡭ࠪࡷࠥࠨ࡬ࡰࡩࡶࠦࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࠺ࠡࡖ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡘࡪࡹࡴࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦ࡭ࡰࡰ࡬ࡸࡴࡸࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᔺ")
        global _1l1ll1l1111_opy_
        platform_index = os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᔻ")]
        bstack1l1ll111ll1_opy_ = os.path.join(bstack1l1ll1ll111_opy_, (bstack1l1ll11l11l_opy_ + str(platform_index)), bstack11lllll1l11_opy_)
        if not os.path.exists(bstack1l1ll111ll1_opy_) or not os.path.isdir(bstack1l1ll111ll1_opy_):
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࡴࠢࡷࡳࠥࡶࡲࡰࡥࡨࡷࡸࠦࡻࡾࠤᔼ").format(bstack1l1ll111ll1_opy_))
            return
        logs = hook.get(bstack111l111_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᔽ"), [])
        with os.scandir(bstack1l1ll111ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l1111_opy_:
                    self.logger.info(bstack111l111_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᔾ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111l111_opy_ (u"ࠢࠣᔿ")
                    log_entry = bstack1ll1lll1l11_opy_(
                        kind=bstack111l111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᕀ"),
                        message=bstack111l111_opy_ (u"ࠤࠥᕁ"),
                        level=bstack111l111_opy_ (u"ࠥࠦᕂ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll111lll_opy_=entry.stat().st_size,
                        bstack1l1ll1l1lll_opy_=bstack111l111_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᕃ"),
                        bstack11l111_opy_=os.path.abspath(entry.path),
                        bstack1l11l111111_opy_=hook.get(TestFramework.bstack1l111111lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l1111_opy_.add(abs_path)
        platform_index = os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᕄ")]
        bstack1l111l1l11l_opy_ = os.path.join(bstack1l1ll1ll111_opy_, (bstack1l1ll11l11l_opy_ + str(platform_index)), bstack11lllll1l11_opy_, bstack11lllll11l1_opy_)
        if not os.path.exists(bstack1l111l1l11l_opy_) or not os.path.isdir(bstack1l111l1l11l_opy_):
            self.logger.info(bstack111l111_opy_ (u"ࠨࡎࡰࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤࠡࡣࡷ࠾ࠥࢁࡽࠣᕅ").format(bstack1l111l1l11l_opy_))
        else:
            self.logger.info(bstack111l111_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡨࡵࡳࡲࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᕆ").format(bstack1l111l1l11l_opy_))
            with os.scandir(bstack1l111l1l11l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l1111_opy_:
                        self.logger.info(bstack111l111_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᕇ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111l111_opy_ (u"ࠤࠥᕈ")
                        log_entry = bstack1ll1lll1l11_opy_(
                            kind=bstack111l111_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᕉ"),
                            message=bstack111l111_opy_ (u"ࠦࠧᕊ"),
                            level=bstack111l111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᕋ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll111lll_opy_=entry.stat().st_size,
                            bstack1l1ll1l1lll_opy_=bstack111l111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᕌ"),
                            bstack11l111_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1l11ll_opy_=hook.get(TestFramework.bstack1l111111lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l1111_opy_.add(abs_path)
        hook[bstack111l111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᕍ")] = logs
    def bstack1l1l1ll1l11_opy_(
        self,
        bstack1l1lll111ll_opy_: bstack1lll1lllll1_opy_,
        entries: List[bstack1ll1lll1l11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡕࡈࡗࡘࡏࡏࡏࡡࡌࡈࠧᕎ"))
        req.platform_index = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll11l1lll1_opy_)
        req.execution_context.hash = str(bstack1l1lll111ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll111ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1l1ll1ll1_opy_)
            log_entry.uuid = entry.bstack1l11l111111_opy_
            log_entry.test_framework_state = bstack1l1lll111ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᕏ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111l111_opy_ (u"ࠥࠦᕐ")
            if entry.kind == bstack111l111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᕑ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll111lll_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1l1lll1ll_opy_():
            bstack1l1111lll_opy_ = datetime.now()
            try:
                self.bstack1lll1l11l1l_opy_.LogCreatedEvent(req)
                bstack1l1lll111ll_opy_.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᕒ"), datetime.now() - bstack1l1111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᕓ").format(str(e)))
                traceback.print_exc()
        self.bstack1111111lll_opy_.enqueue(bstack1l1l1lll1ll_opy_)
    def __1l111ll11l1_opy_(self, instance) -> None:
        bstack111l111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᕔ")
        bstack1l1111ll11l_opy_ = {bstack111l111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᕕ"): bstack1lll111l111_opy_.bstack1l111ll111l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1111ll1l1_opy_(instance, bstack1l1111ll11l_opy_)
    @staticmethod
    def bstack1l1111l1lll_opy_(instance: bstack1lll1lllll1_opy_, bstack1l111lll1l1_opy_: str):
        bstack1l111l1lll1_opy_ = (
            bstack1lll1l111ll_opy_.bstack1l11l11111l_opy_
            if bstack1l111lll1l1_opy_ == bstack1lll1l111ll_opy_.bstack1l111lll111_opy_
            else bstack1lll1l111ll_opy_.bstack1l11l1111ll_opy_
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
        hook = bstack1lll1l111ll_opy_.bstack1l1111l1lll_opy_(instance, bstack1l111lll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11111l1l1_opy_, []).clear()
    @staticmethod
    def __1l111ll1ll1_opy_(instance: bstack1lll1lllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111l111_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᕖ"), None)):
            return
        if os.getenv(bstack111l111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᕗ"), bstack111l111_opy_ (u"ࠦ࠶ࠨᕘ")) != bstack111l111_opy_ (u"ࠧ࠷ࠢᕙ"):
            bstack1lll1l111ll_opy_.logger.warning(bstack111l111_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᕚ"))
            return
        bstack1l1111111l1_opy_ = {
            bstack111l111_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᕛ"): (bstack1lll1l111ll_opy_.bstack11lllllllll_opy_, bstack1lll1l111ll_opy_.bstack1l11l1111ll_opy_),
            bstack111l111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᕜ"): (bstack1lll1l111ll_opy_.bstack1l111lll111_opy_, bstack1lll1l111ll_opy_.bstack1l11l11111l_opy_),
        }
        for when in (bstack111l111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᕝ"), bstack111l111_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᕞ"), bstack111l111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᕟ")):
            bstack11lllll1lll_opy_ = args[1].get_records(when)
            if not bstack11lllll1lll_opy_:
                continue
            records = [
                bstack1ll1lll1l11_opy_(
                    kind=TestFramework.bstack1l1ll11lll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111l111_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣᕠ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111l111_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢᕡ")) and r.created
                        else None
                    ),
                )
                for r in bstack11lllll1lll_opy_
                if isinstance(getattr(r, bstack111l111_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᕢ"), None), str) and r.message.strip()
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
    def __1l111l1llll_opy_(test) -> Dict[str, Any]:
        bstack11l1111l_opy_ = bstack1lll1l111ll_opy_.__1l111l1ll1l_opy_(test.location) if hasattr(test, bstack111l111_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᕣ")) else getattr(test, bstack111l111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᕤ"), None)
        test_name = test.name if hasattr(test, bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣᕥ")) else None
        bstack1l111l11ll1_opy_ = test.fspath.strpath if hasattr(test, bstack111l111_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᕦ")) and test.fspath else None
        if not bstack11l1111l_opy_ or not test_name or not bstack1l111l11ll1_opy_:
            return None
        code = None
        if hasattr(test, bstack111l111_opy_ (u"ࠧࡵࡢ࡫ࠤᕧ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11lllll111l_opy_ = []
        try:
            bstack11lllll111l_opy_ = bstack11llll1l11_opy_.bstack111l1l111l_opy_(test)
        except:
            bstack1lll1l111ll_opy_.logger.warning(bstack111l111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᕨ"))
        return {
            TestFramework.bstack1ll11l11l1l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1111l_opy_: bstack11l1111l_opy_,
            TestFramework.bstack1ll111l111l_opy_: test_name,
            TestFramework.bstack1l1l1l1l111_opy_: getattr(test, bstack111l111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᕩ"), None),
            TestFramework.bstack1l111ll1l11_opy_: bstack1l111l11ll1_opy_,
            TestFramework.bstack1l111llll11_opy_: bstack1lll1l111ll_opy_.__1l111111l1l_opy_(test),
            TestFramework.bstack1l111111111_opy_: code,
            TestFramework.bstack1l1l1111111_opy_: TestFramework.bstack1l111llll1l_opy_,
            TestFramework.bstack1l11l1l1l11_opy_: bstack11l1111l_opy_,
            TestFramework.bstack11lllll11ll_opy_: bstack11lllll111l_opy_
        }
    @staticmethod
    def __1l111111l1l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack111l111_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᕪ"), [])
            markers.extend([getattr(m, bstack111l111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᕫ"), None) for m in own_markers if getattr(m, bstack111l111_opy_ (u"ࠥࡲࡦࡳࡥࠣᕬ"), None)])
            current = getattr(current, bstack111l111_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᕭ"), None)
        return markers
    @staticmethod
    def __1l111l1ll1l_opy_(location):
        return bstack111l111_opy_ (u"ࠧࡀ࠺ࠣᕮ").join(filter(lambda x: isinstance(x, str), location))