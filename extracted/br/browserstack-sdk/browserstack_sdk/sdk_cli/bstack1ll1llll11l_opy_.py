# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lllll11l1l_opy_ import bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l111l11ll_opy_ import bstack1l111l11111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l11l1l_opy_,
    bstack1ll1ll11l1l_opy_,
    bstack1lll111l111_opy_,
    bstack1l111l11l1l_opy_,
    bstack1ll1l1ll11l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1llllll_opy_
from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack1111111lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l1ll1_opy_ import bstack1ll1lll1111_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l11l1l1l1_opy_
bstack1l1ll1lllll_opy_ = bstack1l1l1llllll_opy_()
bstack1l111ll11l1_opy_ = 1.0
bstack1l1llll111l_opy_ = bstackl_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᓕ")
bstack11lllll11l1_opy_ = bstackl_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᓖ")
bstack11llll1llll_opy_ = bstackl_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᓗ")
bstack11lllll111l_opy_ = bstackl_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᓘ")
bstack11lllll1111_opy_ = bstackl_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᓙ")
_1l1ll1l111l_opy_ = set()
class bstack1lll1ll1111_opy_(TestFramework):
    bstack1l111111111_opy_ = bstackl_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᓚ")
    bstack1l111l1l1ll_opy_ = bstackl_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᓛ")
    bstack1l11l111l11_opy_ = bstackl_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᓜ")
    bstack11lllll1ll1_opy_ = bstackl_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᓝ")
    bstack1l1111l11ll_opy_ = bstackl_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᓞ")
    bstack1l1111lll1l_opy_: bool
    bstack111111l1l1_opy_: bstack1111111lll_opy_  = None
    bstack1lll1l1l1ll_opy_ = None
    bstack1l1111l1111_opy_ = [
        bstack1lll1l11l1l_opy_.BEFORE_ALL,
        bstack1lll1l11l1l_opy_.AFTER_ALL,
        bstack1lll1l11l1l_opy_.BEFORE_EACH,
        bstack1lll1l11l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1111lllll_opy_: Dict[str, str],
        bstack1ll1l11111l_opy_: List[str]=[bstackl_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᓟ")],
        bstack111111l1l1_opy_: bstack1111111lll_opy_=None,
        bstack1lll1l1l1ll_opy_=None
    ):
        super().__init__(bstack1ll1l11111l_opy_, bstack1l1111lllll_opy_, bstack111111l1l1_opy_)
        self.bstack1l1111lll1l_opy_ = any(bstackl_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᓠ") in item.lower() for item in bstack1ll1l11111l_opy_)
        self.bstack1lll1l1l1ll_opy_ = bstack1lll1l1l1ll_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l11l1l_opy_.TEST or test_framework_state in bstack1lll1ll1111_opy_.bstack1l1111l1111_opy_:
            bstack1l111l11111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l11l1l_opy_.NONE:
            self.logger.warning(bstackl_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᓡ") + str(test_hook_state) + bstackl_opy_ (u"ࠧࠨᓢ"))
            return
        if not self.bstack1l1111lll1l_opy_:
            self.logger.warning(bstackl_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᓣ") + str(str(self.bstack1ll1l11111l_opy_)) + bstackl_opy_ (u"ࠢࠣᓤ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstackl_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᓥ") + str(kwargs) + bstackl_opy_ (u"ࠤࠥᓦ"))
            return
        instance = self.__1l111l111ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstackl_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᓧ") + str(args) + bstackl_opy_ (u"ࠦࠧᓨ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1ll1111_opy_.bstack1l1111l1111_opy_ and test_hook_state == bstack1lll111l111_opy_.PRE:
                bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack1ll1l1111l_opy_.value)
                name = str(EVENTS.bstack1ll1l1111l_opy_.name)+bstackl_opy_ (u"ࠧࡀࠢᓩ")+str(test_framework_state.name)
                TestFramework.bstack1l1111ll1l1_opy_(instance, name, bstack1ll11lll11l_opy_)
        except Exception as e:
            self.logger.debug(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᓪ").format(e))
        try:
            if not TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l111ll1l11_opy_) and test_hook_state == bstack1lll111l111_opy_.PRE:
                test = bstack1lll1ll1111_opy_.__1l11l1111l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstackl_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᓫ") + str(test_hook_state) + bstackl_opy_ (u"ࠣࠤᓬ"))
            if test_framework_state == bstack1lll1l11l1l_opy_.TEST:
                if test_hook_state == bstack1lll111l111_opy_.PRE and not TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1lll111ll_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll111ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstackl_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᓭ") + str(test_hook_state) + bstackl_opy_ (u"ࠥࠦᓮ"))
                elif test_hook_state == bstack1lll111l111_opy_.POST and not TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1lll11111_opy_):
                    TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1lll11111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstackl_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᓯ") + str(test_hook_state) + bstackl_opy_ (u"ࠧࠨᓰ"))
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG and test_hook_state == bstack1lll111l111_opy_.POST:
                bstack1lll1ll1111_opy_.__1l111llll11_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG_REPORT and test_hook_state == bstack1lll111l111_opy_.POST:
                self.__1l111l11l11_opy_(instance, *args)
                self.__1l11111llll_opy_(instance)
            elif test_framework_state in bstack1lll1ll1111_opy_.bstack1l1111l1111_opy_:
                self.__1l1111l1l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstackl_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᓱ") + str(instance.ref()) + bstackl_opy_ (u"ࠢࠣᓲ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1111ll111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1ll1111_opy_.bstack1l1111l1111_opy_ and test_hook_state == bstack1lll111l111_opy_.POST:
                name = str(EVENTS.bstack1ll1l1111l_opy_.name)+bstackl_opy_ (u"ࠣ࠼ࠥᓳ")+str(test_framework_state.name)
                bstack1ll11lll11l_opy_ = TestFramework.bstack1l1111ll1ll_opy_(instance, name)
                bstack1lll11lll1l_opy_.end(EVENTS.bstack1ll1l1111l_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᓴ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᓵ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstackl_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᓶ").format(e))
    def bstack1l1ll11111l_opy_(self):
        return self.bstack1l1111lll1l_opy_
    def __1l11111ll1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstackl_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᓷ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1l1ll11_opy_(rep, [bstackl_opy_ (u"ࠨࡷࡩࡧࡱࠦᓸ"), bstackl_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᓹ"), bstackl_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᓺ"), bstackl_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᓻ"), bstackl_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᓼ"), bstackl_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᓽ")])
        return None
    def __1l111l11l11_opy_(self, instance: bstack1ll1ll11l1l_opy_, *args):
        result = self.__1l11111ll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack111111ll11_opy_ = None
        if result.get(bstackl_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᓾ"), None) == bstackl_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᓿ") and len(args) > 1 and getattr(args[1], bstackl_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᔀ"), None) is not None:
            failure = [{bstackl_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᔁ"): [args[1].excinfo.exconly(), result.get(bstackl_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᔂ"), None)]}]
            bstack111111ll11_opy_ = bstackl_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᔃ") if bstackl_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᔄ") in getattr(args[1].excinfo, bstackl_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᔅ"), bstackl_opy_ (u"ࠨࠢᔆ")) else bstackl_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᔇ")
        bstack11llllll1l1_opy_ = result.get(bstackl_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᔈ"), TestFramework.bstack1l11111l1ll_opy_)
        if bstack11llllll1l1_opy_ != TestFramework.bstack1l11111l1ll_opy_:
            TestFramework.bstack1lllllllll1_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11111l1l1_opy_(instance, {
            TestFramework.bstack1l1l11111ll_opy_: failure,
            TestFramework.bstack1l11111ll11_opy_: bstack111111ll11_opy_,
            TestFramework.bstack1l11lllll1l_opy_: bstack11llllll1l1_opy_,
        })
    def __1l111l111ll_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l11l1l_opy_.SETUP_FIXTURE:
            instance = self.__1l1111lll11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111ll1lll_opy_ bstack1l111lll1ll_opy_ this to be bstackl_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᔉ")
            if test_framework_state == bstack1lll1l11l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111l1l11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstackl_opy_ (u"ࠥࡲࡴࡪࡥࠣᔊ"), None), bstackl_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᔋ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstackl_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᔌ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111111111_opy_(target) if target else None
        return instance
    def __1l1111l1l11_opy_(
        self,
        instance: bstack1ll1ll11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111l111l1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l111l1l1ll_opy_, {})
        if not key in bstack1l111l111l1_opy_:
            bstack1l111l111l1_opy_[key] = []
        bstack1l111llll1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l11l111l11_opy_, {})
        if not key in bstack1l111llll1l_opy_:
            bstack1l111llll1l_opy_[key] = []
        bstack1l111l1l111_opy_ = {
            bstack1lll1ll1111_opy_.bstack1l111l1l1ll_opy_: bstack1l111l111l1_opy_,
            bstack1lll1ll1111_opy_.bstack1l11l111l11_opy_: bstack1l111llll1l_opy_,
        }
        if test_hook_state == bstack1lll111l111_opy_.PRE:
            hook = {
                bstackl_opy_ (u"ࠨ࡫ࡦࡻࠥᔍ"): key,
                TestFramework.bstack1l111llllll_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111ll11l_opy_: TestFramework.bstack11llllll111_opy_,
                TestFramework.bstack11lllllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1111ll_opy_: [],
                TestFramework.bstack1l1111l1lll_opy_: args[1] if len(args) > 1 else bstackl_opy_ (u"ࠧࠨᔎ"),
                TestFramework.bstack1l111l1llll_opy_: bstack1ll1lll1111_opy_.bstack1l111111lll_opy_()
            }
            bstack1l111l111l1_opy_[key].append(hook)
            bstack1l111l1l111_opy_[bstack1lll1ll1111_opy_.bstack11lllll1ll1_opy_] = key
        elif test_hook_state == bstack1lll111l111_opy_.POST:
            bstack1l111l1ll1l_opy_ = bstack1l111l111l1_opy_.get(key, [])
            hook = bstack1l111l1ll1l_opy_.pop() if bstack1l111l1ll1l_opy_ else None
            if hook:
                result = self.__1l11111ll1l_opy_(*args)
                if result:
                    bstack11llllll1ll_opy_ = result.get(bstackl_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᔏ"), TestFramework.bstack11llllll111_opy_)
                    if bstack11llllll1ll_opy_ != TestFramework.bstack11llllll111_opy_:
                        hook[TestFramework.bstack1l1111ll11l_opy_] = bstack11llllll1ll_opy_
                hook[TestFramework.bstack1l11l111ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l1llll_opy_]= bstack1ll1lll1111_opy_.bstack1l111111lll_opy_()
                self.bstack1l111l1l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111ll1ll1_opy_, [])
                if logs: self.bstack1l1ll1l1111_opy_(instance, logs)
                bstack1l111llll1l_opy_[key].append(hook)
                bstack1l111l1l111_opy_[bstack1lll1ll1111_opy_.bstack1l1111l11ll_opy_] = key
        TestFramework.bstack1l11111l1l1_opy_(instance, bstack1l111l1l111_opy_)
        self.logger.debug(bstackl_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᔐ") + str(bstack1l111llll1l_opy_) + bstackl_opy_ (u"ࠥࠦᔑ"))
    def __1l1111lll11_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        test_hook_state: bstack1lll111l111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1l1ll11_opy_(args[0], [bstackl_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᔒ"), bstackl_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᔓ"), bstackl_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᔔ"), bstackl_opy_ (u"ࠢࡪࡦࡶࠦᔕ"), bstackl_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᔖ"), bstackl_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᔗ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstackl_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᔘ")) else fixturedef.get(bstackl_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᔙ"), None)
        fixturename = request.fixturename if hasattr(request, bstackl_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᔚ")) else None
        node = request.node if hasattr(request, bstackl_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᔛ")) else None
        target = request.node.nodeid if hasattr(node, bstackl_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᔜ")) else None
        baseid = fixturedef.get(bstackl_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᔝ"), None) or bstackl_opy_ (u"ࠤࠥᔞ")
        if (not target or len(baseid) > 0) and hasattr(request, bstackl_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᔟ")):
            target = bstack1lll1ll1111_opy_.__1l11l11111l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstackl_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᔠ")) else None
            if target and not TestFramework.bstack1111111111_opy_(target):
                self.__1l111l1l11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstackl_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᔡ") + str(test_hook_state) + bstackl_opy_ (u"ࠨࠢᔢ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstackl_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᔣ") + str(target) + bstackl_opy_ (u"ࠣࠤᔤ"))
            return None
        instance = TestFramework.bstack1111111111_opy_(target)
        if not instance:
            self.logger.warning(bstackl_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᔥ") + str(target) + bstackl_opy_ (u"ࠥࠦᔦ"))
            return None
        bstack1l111111ll1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1l111111111_opy_, {})
        if os.getenv(bstackl_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᔧ"), bstackl_opy_ (u"ࠧ࠷ࠢᔨ")) == bstackl_opy_ (u"ࠨ࠱ࠣᔩ"):
            bstack1l111l1lll1_opy_ = bstackl_opy_ (u"ࠢ࠻ࠤᔪ").join((scope, fixturename))
            bstack1l11111l111_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1111l11l1_opy_ = {
                bstackl_opy_ (u"ࠣ࡭ࡨࡽࠧᔫ"): bstack1l111l1lll1_opy_,
                bstackl_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᔬ"): bstack1lll1ll1111_opy_.__1l111lll1l1_opy_(request.node),
                bstackl_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᔭ"): fixturedef,
                bstackl_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᔮ"): scope,
                bstackl_opy_ (u"ࠧࡺࡹࡱࡧࠥᔯ"): None,
            }
            try:
                if test_hook_state == bstack1lll111l111_opy_.POST and callable(getattr(args[-1], bstackl_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᔰ"), None)):
                    bstack1l1111l11l1_opy_[bstackl_opy_ (u"ࠢࡵࡻࡳࡩࠧᔱ")] = TestFramework.bstack1l1ll1l11ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll111l111_opy_.PRE:
                bstack1l1111l11l1_opy_[bstackl_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᔲ")] = uuid4().__str__()
                bstack1l1111l11l1_opy_[bstack1lll1ll1111_opy_.bstack11lllllll11_opy_] = bstack1l11111l111_opy_
            elif test_hook_state == bstack1lll111l111_opy_.POST:
                bstack1l1111l11l1_opy_[bstack1lll1ll1111_opy_.bstack1l11l111ll1_opy_] = bstack1l11111l111_opy_
            if bstack1l111l1lll1_opy_ in bstack1l111111ll1_opy_:
                bstack1l111111ll1_opy_[bstack1l111l1lll1_opy_].update(bstack1l1111l11l1_opy_)
                self.logger.debug(bstackl_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᔳ") + str(bstack1l111111ll1_opy_[bstack1l111l1lll1_opy_]) + bstackl_opy_ (u"ࠥࠦᔴ"))
            else:
                bstack1l111111ll1_opy_[bstack1l111l1lll1_opy_] = bstack1l1111l11l1_opy_
                self.logger.debug(bstackl_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᔵ") + str(len(bstack1l111111ll1_opy_)) + bstackl_opy_ (u"ࠧࠨᔶ"))
        TestFramework.bstack1lllllllll1_opy_(instance, bstack1lll1ll1111_opy_.bstack1l111111111_opy_, bstack1l111111ll1_opy_)
        self.logger.debug(bstackl_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᔷ") + str(instance.ref()) + bstackl_opy_ (u"ࠢࠣᔸ"))
        return instance
    def __1l111l1l11l_opy_(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l11l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll1lllll_opy_.create_context(target)
        ob = bstack1ll1ll11l1l_opy_(ctx, self.bstack1ll1l11111l_opy_, self.bstack1l1111lllll_opy_, test_framework_state)
        TestFramework.bstack1l11111l1l1_opy_(ob, {
            TestFramework.bstack1ll1l1111l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll1l1l1_opy_: context.test_framework_version,
            TestFramework.bstack11lllllll1l_opy_: [],
            bstack1lll1ll1111_opy_.bstack1l111111111_opy_: {},
            bstack1lll1ll1111_opy_.bstack1l11l111l11_opy_: {},
            bstack1lll1ll1111_opy_.bstack1l111l1l1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack11llllllll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllllllll1_opy_(ob, TestFramework.bstack1ll111ll1l1_opy_, context.platform_index)
        TestFramework.bstack1lllllll1ll_opy_[ctx.id] = ob
        self.logger.debug(bstackl_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᔹ") + str(TestFramework.bstack1lllllll1ll_opy_.keys()) + bstackl_opy_ (u"ࠤࠥᔺ"))
        return ob
    def bstack1l1l1lll1l1_opy_(self, instance: bstack1ll1ll11l1l_opy_, bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_]):
        bstack1l111lll111_opy_ = (
            bstack1lll1ll1111_opy_.bstack11lllll1ll1_opy_
            if bstack1lllll1l1ll_opy_[1] == bstack1lll111l111_opy_.PRE
            else bstack1lll1ll1111_opy_.bstack1l1111l11ll_opy_
        )
        hook = bstack1lll1ll1111_opy_.bstack11lllllllll_opy_(instance, bstack1l111lll111_opy_)
        entries = hook.get(TestFramework.bstack1l11l1111ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []))
        return entries
    def bstack1l1ll1ll111_opy_(self, instance: bstack1ll1ll11l1l_opy_, bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_]):
        bstack1l111lll111_opy_ = (
            bstack1lll1ll1111_opy_.bstack11lllll1ll1_opy_
            if bstack1lllll1l1ll_opy_[1] == bstack1lll111l111_opy_.PRE
            else bstack1lll1ll1111_opy_.bstack1l1111l11ll_opy_
        )
        bstack1lll1ll1111_opy_.bstack1l11111l11l_opy_(instance, bstack1l111lll111_opy_)
        TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack11lllllll1l_opy_, []).clear()
    def bstack1l111l1l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstackl_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᔻ")
        global _1l1ll1l111l_opy_
        platform_index = os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᔼ")]
        bstack1l1lll1ll1l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack11lllll111l_opy_)
        if not os.path.exists(bstack1l1lll1ll1l_opy_) or not os.path.isdir(bstack1l1lll1ll1l_opy_):
            self.logger.debug(bstackl_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᔽ").format(bstack1l1lll1ll1l_opy_))
            return
        logs = hook.get(bstackl_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᔾ"), [])
        with os.scandir(bstack1l1lll1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l111l_opy_:
                    self.logger.info(bstackl_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᔿ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstackl_opy_ (u"ࠣࠤᕀ")
                    log_entry = bstack1ll1l1ll11l_opy_(
                        kind=bstackl_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᕁ"),
                        message=bstackl_opy_ (u"ࠥࠦᕂ"),
                        level=bstackl_opy_ (u"ࠦࠧᕃ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llll11l1_opy_=entry.stat().st_size,
                        bstack1l1ll1lll1l_opy_=bstackl_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᕄ"),
                        bstack11llll_opy_=os.path.abspath(entry.path),
                        bstack1l111111l11_opy_=hook.get(TestFramework.bstack1l111llllll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l111l_opy_.add(abs_path)
        platform_index = os.environ[bstackl_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᕅ")]
        bstack1l11111111l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack11lllll111l_opy_, bstack11lllll1111_opy_)
        if not os.path.exists(bstack1l11111111l_opy_) or not os.path.isdir(bstack1l11111111l_opy_):
            self.logger.info(bstackl_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᕆ").format(bstack1l11111111l_opy_))
        else:
            self.logger.info(bstackl_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᕇ").format(bstack1l11111111l_opy_))
            with os.scandir(bstack1l11111111l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l111l_opy_:
                        self.logger.info(bstackl_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᕈ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstackl_opy_ (u"ࠥࠦᕉ")
                        log_entry = bstack1ll1l1ll11l_opy_(
                            kind=bstackl_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᕊ"),
                            message=bstackl_opy_ (u"ࠧࠨᕋ"),
                            level=bstackl_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᕌ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llll11l1_opy_=entry.stat().st_size,
                            bstack1l1ll1lll1l_opy_=bstackl_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᕍ"),
                            bstack11llll_opy_=os.path.abspath(entry.path),
                            bstack1l1l1l1lll1_opy_=hook.get(TestFramework.bstack1l111llllll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l111l_opy_.add(abs_path)
        hook[bstackl_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᕎ")] = logs
    def bstack1l1ll1l1111_opy_(
        self,
        bstack1l1l1l1llll_opy_: bstack1ll1ll11l1l_opy_,
        entries: List[bstack1ll1l1ll11l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstackl_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᕏ"))
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll111ll1l1_opy_)
        req.execution_context.hash = str(bstack1l1l1l1llll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1llll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1llll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll1l1111l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1l1lll1l1l1_opy_)
            log_entry.uuid = entry.bstack1l111111l11_opy_
            log_entry.test_framework_state = bstack1l1l1l1llll_opy_.state.name
            log_entry.message = entry.message.encode(bstackl_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᕐ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstackl_opy_ (u"ࠦࠧᕑ")
            if entry.kind == bstackl_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᕒ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll11l1_opy_
                log_entry.file_path = entry.bstack11llll_opy_
        def bstack1l1ll11l1l1_opy_():
            bstack1l1ll11l1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1l1ll_opy_.LogCreatedEvent(req)
                bstack1l1l1l1llll_opy_.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᕓ"), datetime.now() - bstack1l1ll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstackl_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᕔ").format(str(e)))
                traceback.print_exc()
        self.bstack111111l1l1_opy_.enqueue(bstack1l1ll11l1l1_opy_)
    def __1l11111llll_opy_(self, instance) -> None:
        bstackl_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᕕ")
        bstack1l111l1l111_opy_ = {bstackl_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᕖ"): bstack1ll1lll1111_opy_.bstack1l111111lll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11111l1l1_opy_(instance, bstack1l111l1l111_opy_)
    @staticmethod
    def bstack11lllllllll_opy_(instance: bstack1ll1ll11l1l_opy_, bstack1l111lll111_opy_: str):
        bstack1l111l1111l_opy_ = (
            bstack1lll1ll1111_opy_.bstack1l11l111l11_opy_
            if bstack1l111lll111_opy_ == bstack1lll1ll1111_opy_.bstack1l1111l11ll_opy_
            else bstack1lll1ll1111_opy_.bstack1l111l1l1ll_opy_
        )
        bstack1l111111l1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111lll111_opy_, None)
        bstack1l11l111111_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1111l_opy_, None) if bstack1l111111l1l_opy_ else None
        return (
            bstack1l11l111111_opy_[bstack1l111111l1l_opy_][-1]
            if isinstance(bstack1l11l111111_opy_, dict) and len(bstack1l11l111111_opy_.get(bstack1l111111l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11111l11l_opy_(instance: bstack1ll1ll11l1l_opy_, bstack1l111lll111_opy_: str):
        hook = bstack1lll1ll1111_opy_.bstack11lllllllll_opy_(instance, bstack1l111lll111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1111ll_opy_, []).clear()
    @staticmethod
    def __1l111llll11_opy_(instance: bstack1ll1ll11l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstackl_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᕗ"), None)):
            return
        if os.getenv(bstackl_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᕘ"), bstackl_opy_ (u"ࠧ࠷ࠢᕙ")) != bstackl_opy_ (u"ࠨ࠱ࠣᕚ"):
            bstack1lll1ll1111_opy_.logger.warning(bstackl_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᕛ"))
            return
        bstack1l11111lll1_opy_ = {
            bstackl_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᕜ"): (bstack1lll1ll1111_opy_.bstack11lllll1ll1_opy_, bstack1lll1ll1111_opy_.bstack1l111l1l1ll_opy_),
            bstackl_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᕝ"): (bstack1lll1ll1111_opy_.bstack1l1111l11ll_opy_, bstack1lll1ll1111_opy_.bstack1l11l111l11_opy_),
        }
        for when in (bstackl_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᕞ"), bstackl_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᕟ"), bstackl_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᕠ")):
            bstack1l1111llll1_opy_ = args[1].get_records(when)
            if not bstack1l1111llll1_opy_:
                continue
            records = [
                bstack1ll1l1ll11l_opy_(
                    kind=TestFramework.bstack1l1lll1l1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstackl_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᕡ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstackl_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᕢ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1111llll1_opy_
                if isinstance(getattr(r, bstackl_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᕣ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111l1ll11_opy_, bstack1l111l1111l_opy_ = bstack1l11111lll1_opy_.get(when, (None, None))
            bstack1l11l111l1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1ll11_opy_, None) if bstack1l111l1ll11_opy_ else None
            bstack1l11l111111_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1111l_opy_, None) if bstack1l11l111l1l_opy_ else None
            if isinstance(bstack1l11l111111_opy_, dict) and len(bstack1l11l111111_opy_.get(bstack1l11l111l1l_opy_, [])) > 0:
                hook = bstack1l11l111111_opy_[bstack1l11l111l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l1111ll_opy_ in hook:
                    hook[TestFramework.bstack1l11l1111ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack11lllllll1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l1111l1_opy_(test) -> Dict[str, Any]:
        bstack1lll11ll_opy_ = bstack1lll1ll1111_opy_.__1l11l11111l_opy_(test.location) if hasattr(test, bstackl_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᕤ")) else getattr(test, bstackl_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᕥ"), None)
        test_name = test.name if hasattr(test, bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᕦ")) else None
        bstack1l1111111ll_opy_ = test.fspath.strpath if hasattr(test, bstackl_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᕧ")) and test.fspath else None
        if not bstack1lll11ll_opy_ or not test_name or not bstack1l1111111ll_opy_:
            return None
        code = None
        if hasattr(test, bstackl_opy_ (u"ࠨ࡯ࡣ࡬ࠥᕨ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11lllll1l11_opy_ = []
        try:
            bstack11lllll1l11_opy_ = bstack1l11l1l1l1_opy_.bstack111l11llll_opy_(test)
        except:
            bstack1lll1ll1111_opy_.logger.warning(bstackl_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᕩ"))
        return {
            TestFramework.bstack1ll11l11lll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111ll1l11_opy_: bstack1lll11ll_opy_,
            TestFramework.bstack1ll1l111l1l_opy_: test_name,
            TestFramework.bstack1l1l1l111ll_opy_: getattr(test, bstackl_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᕪ"), None),
            TestFramework.bstack1l1111l1l1l_opy_: bstack1l1111111ll_opy_,
            TestFramework.bstack1l1111111l1_opy_: bstack1lll1ll1111_opy_.__1l111lll1l1_opy_(test),
            TestFramework.bstack1l111ll11ll_opy_: code,
            TestFramework.bstack1l11lllll1l_opy_: TestFramework.bstack1l11111l1ll_opy_,
            TestFramework.bstack1l11l1l1l11_opy_: bstack1lll11ll_opy_,
            TestFramework.bstack11lllll11ll_opy_: bstack11lllll1l11_opy_
        }
    @staticmethod
    def __1l111lll1l1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstackl_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᕫ"), [])
            markers.extend([getattr(m, bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᕬ"), None) for m in own_markers if getattr(m, bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᕭ"), None)])
            current = getattr(current, bstackl_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᕮ"), None)
        return markers
    @staticmethod
    def __1l11l11111l_opy_(location):
        return bstackl_opy_ (u"ࠨ࠺࠻ࠤᕯ").join(filter(lambda x: isinstance(x, str), location))