# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack11111111ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack11ll111ll1_opy_ import bstack1l111lll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll1ll1l1_opy_,
    bstack1llllll11ll_opy_,
    bstack1llll1lll1l_opy_,
    bstack1l11l1l1ll1_opy_,
    bstack1lll1l111l1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lll1111l_opy_
from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1l1l1_opy_ import bstack1111l1ll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll111111l_opy_ import bstack1lll11ll11l_opy_
from bstack_utils.bstack11l111l111_opy_ import bstack1l11ll11ll_opy_
bstack1ll111l1l1l_opy_ = bstack1l1lll1111l_opy_()
bstack1l11ll1111l_opy_ = 1.0
bstack1l1ll1lll1l_opy_ = bstack1l1lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᐢ")
bstack1l111l11l1l_opy_ = bstack1l1lll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᐣ")
bstack1l111l11ll1_opy_ = bstack1l1lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᐤ")
bstack1l111l111ll_opy_ = bstack1l1lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᐥ")
bstack1l111l11lll_opy_ = bstack1l1lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᐦ")
_1ll111ll11l_opy_ = set()
class bstack1lll11l11ll_opy_(TestFramework):
    bstack1l11lll1l11_opy_ = bstack1l1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᐧ")
    bstack1l111l1llll_opy_ = bstack1l1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᐨ")
    bstack1l11l11lll1_opy_ = bstack1l1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᐩ")
    bstack1l11lll111l_opy_ = bstack1l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᐪ")
    bstack1l11ll111l1_opy_ = bstack1l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᐫ")
    bstack1l111l1lll1_opy_: bool
    bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_  = None
    bstack1lll1ll1l11_opy_ = None
    bstack1l111ll11ll_opy_ = [
        bstack1llll1ll1l1_opy_.BEFORE_ALL,
        bstack1llll1ll1l1_opy_.AFTER_ALL,
        bstack1llll1ll1l1_opy_.BEFORE_EACH,
        bstack1llll1ll1l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l11l11l_opy_: Dict[str, str],
        bstack1ll1l1111l1_opy_: List[str]=[bstack1l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᐬ")],
        bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_=None,
        bstack1lll1ll1l11_opy_=None
    ):
        super().__init__(bstack1ll1l1111l1_opy_, bstack1l11l11l11l_opy_, bstack1111l1l1l1_opy_)
        self.bstack1l111l1lll1_opy_ = any(bstack1l1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᐭ") in item.lower() for item in bstack1ll1l1111l1_opy_)
        self.bstack1lll1ll1l11_opy_ = bstack1lll1ll1l11_opy_
    def track_event(
        self,
        context: bstack1l11l1l1ll1_opy_,
        test_framework_state: bstack1llll1ll1l1_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1llll1ll1l1_opy_.TEST or test_framework_state in bstack1lll11l11ll_opy_.bstack1l111ll11ll_opy_:
            bstack1l111lll1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll1ll1l1_opy_.NONE:
            self.logger.warning(bstack1l1lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᐮ") + str(test_hook_state) + bstack1l1lll_opy_ (u"ࠣࠤᐯ"))
            return
        if not self.bstack1l111l1lll1_opy_:
            self.logger.warning(bstack1l1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᐰ") + str(str(self.bstack1ll1l1111l1_opy_)) + bstack1l1lll_opy_ (u"ࠥࠦᐱ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐲ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠧࠨᐳ"))
            return
        instance = self.__1l11l1llll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᐴ") + str(args) + bstack1l1lll_opy_ (u"ࠢࠣᐵ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll11l11ll_opy_.bstack1l111ll11ll_opy_ and test_hook_state == bstack1llll1lll1l_opy_.PRE:
                bstack1ll1l11lll1_opy_ = bstack1lll1lll111_opy_.bstack1ll1l1ll1l1_opy_(EVENTS.bstack1l111ll1l1_opy_.value)
                name = str(EVENTS.bstack1l111ll1l1_opy_.name)+bstack1l1lll_opy_ (u"ࠣ࠼ࠥᐶ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll1l111_opy_(instance, name, bstack1ll1l11lll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᐷ").format(e))
        try:
            if not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l11lll11l1_opy_) and test_hook_state == bstack1llll1lll1l_opy_.PRE:
                test = bstack1lll11l11ll_opy_.__1l111llllll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐸ") + str(test_hook_state) + bstack1l1lll_opy_ (u"ࠦࠧᐹ"))
            if test_framework_state == bstack1llll1ll1l1_opy_.TEST:
                if test_hook_state == bstack1llll1lll1l_opy_.PRE and not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111l1lll_opy_):
                    TestFramework.bstack1111l11l1l_opy_(instance, TestFramework.bstack1ll111l1lll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐺ") + str(test_hook_state) + bstack1l1lll_opy_ (u"ࠨࠢᐻ"))
                elif test_hook_state == bstack1llll1lll1l_opy_.POST and not TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_):
                    TestFramework.bstack1111l11l1l_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐼ") + str(test_hook_state) + bstack1l1lll_opy_ (u"ࠣࠤᐽ"))
            elif test_framework_state == bstack1llll1ll1l1_opy_.LOG and test_hook_state == bstack1llll1lll1l_opy_.POST:
                bstack1lll11l11ll_opy_.__1l111l1l111_opy_(instance, *args)
            elif test_framework_state == bstack1llll1ll1l1_opy_.LOG_REPORT and test_hook_state == bstack1llll1lll1l_opy_.POST:
                self.__1l11l11l1l1_opy_(instance, *args)
                self.__1l11ll11l11_opy_(instance)
            elif test_framework_state in bstack1lll11l11ll_opy_.bstack1l111ll11ll_opy_:
                self.__1l11l11ll11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᐾ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠥࠦᐿ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l11llll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll11l11ll_opy_.bstack1l111ll11ll_opy_ and test_hook_state == bstack1llll1lll1l_opy_.POST:
                name = str(EVENTS.bstack1l111ll1l1_opy_.name)+bstack1l1lll_opy_ (u"ࠦ࠿ࠨᑀ")+str(test_framework_state.name)
                bstack1ll1l11lll1_opy_ = TestFramework.bstack1l11llll11l_opy_(instance, name)
                bstack1lll1lll111_opy_.end(EVENTS.bstack1l111ll1l1_opy_.value, bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᑁ"), bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᑂ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᑃ").format(e))
    def bstack1l1lllll1ll_opy_(self):
        return self.bstack1l111l1lll1_opy_
    def __1l11l1l1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᑄ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11111l1l_opy_(rep, [bstack1l1lll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᑅ"), bstack1l1lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑆ"), bstack1l1lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᑇ"), bstack1l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᑈ"), bstack1l1lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᑉ"), bstack1l1lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᑊ")])
        return None
    def __1l11l11l1l1_opy_(self, instance: bstack1llllll11ll_opy_, *args):
        result = self.__1l11l1l1l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll1111_opy_ = None
        if result.get(bstack1l1lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑋ"), None) == bstack1l1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᑌ") and len(args) > 1 and getattr(args[1], bstack1l1lll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᑍ"), None) is not None:
            failure = [{bstack1l1lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᑎ"): [args[1].excinfo.exconly(), result.get(bstack1l1lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᑏ"), None)]}]
            bstack1111ll1111_opy_ = bstack1l1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᑐ") if bstack1l1lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᑑ") in getattr(args[1].excinfo, bstack1l1lll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᑒ"), bstack1l1lll_opy_ (u"ࠤࠥᑓ")) else bstack1l1lll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᑔ")
        bstack1l11l1lll1l_opy_ = result.get(bstack1l1lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑕ"), TestFramework.bstack1l11l1111l1_opy_)
        if bstack1l11l1lll1l_opy_ != TestFramework.bstack1l11l1111l1_opy_:
            TestFramework.bstack1111l11l1l_opy_(instance, TestFramework.bstack1ll111111l1_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l111ll11l1_opy_(instance, {
            TestFramework.bstack1l1l1l1llll_opy_: failure,
            TestFramework.bstack1l11l11ll1l_opy_: bstack1111ll1111_opy_,
            TestFramework.bstack1l1l1ll1ll1_opy_: bstack1l11l1lll1l_opy_,
        })
    def __1l11l1llll1_opy_(
        self,
        context: bstack1l11l1l1ll1_opy_,
        test_framework_state: bstack1llll1ll1l1_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1llll1ll1l1_opy_.SETUP_FIXTURE:
            instance = self.__1l111ll1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll11ll1_opy_ bstack1l111llll1l_opy_ this to be bstack1l1lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑖ")
            if test_framework_state == bstack1llll1ll1l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111ll1l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll1ll1l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑗ"), None), bstack1l1lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑘ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑙ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111111l11_opy_(target) if target else None
        return instance
    def __1l11l11ll11_opy_(
        self,
        instance: bstack1llllll11ll_opy_,
        test_framework_state: bstack1llll1ll1l1_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11lll1111_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_, {})
        if not key in bstack1l11lll1111_opy_:
            bstack1l11lll1111_opy_[key] = []
        bstack1l11l1l11ll_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11l11lll1_opy_, {})
        if not key in bstack1l11l1l11ll_opy_:
            bstack1l11l1l11ll_opy_[key] = []
        bstack1l111lllll1_opy_ = {
            bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_: bstack1l11lll1111_opy_,
            bstack1lll11l11ll_opy_.bstack1l11l11lll1_opy_: bstack1l11l1l11ll_opy_,
        }
        if test_hook_state == bstack1llll1lll1l_opy_.PRE:
            hook = {
                bstack1l1lll_opy_ (u"ࠤ࡮ࡩࡾࠨᑚ"): key,
                TestFramework.bstack1l11l11111l_opy_: uuid4().__str__(),
                TestFramework.bstack1l111l1l11l_opy_: TestFramework.bstack1l11llll111_opy_,
                TestFramework.bstack1l11ll1l1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1ll111_opy_: [],
                TestFramework.bstack1l11l1ll11l_opy_: args[1] if len(args) > 1 else bstack1l1lll_opy_ (u"ࠪࠫᑛ"),
                TestFramework.bstack1l11ll1ll11_opy_: bstack1lll11ll11l_opy_.bstack1l111llll11_opy_()
            }
            bstack1l11lll1111_opy_[key].append(hook)
            bstack1l111lllll1_opy_[bstack1lll11l11ll_opy_.bstack1l11lll111l_opy_] = key
        elif test_hook_state == bstack1llll1lll1l_opy_.POST:
            bstack1l11l1111ll_opy_ = bstack1l11lll1111_opy_.get(key, [])
            hook = bstack1l11l1111ll_opy_.pop() if bstack1l11l1111ll_opy_ else None
            if hook:
                result = self.__1l11l1l1l11_opy_(*args)
                if result:
                    bstack1l111lll11l_opy_ = result.get(bstack1l1lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑜ"), TestFramework.bstack1l11llll111_opy_)
                    if bstack1l111lll11l_opy_ != TestFramework.bstack1l11llll111_opy_:
                        hook[TestFramework.bstack1l111l1l11l_opy_] = bstack1l111lll11l_opy_
                hook[TestFramework.bstack1l111l1l1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11ll1ll11_opy_]= bstack1lll11ll11l_opy_.bstack1l111llll11_opy_()
                self.bstack1l11l111l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1ll11_opy_, [])
                if logs: self.bstack1ll111lll11_opy_(instance, logs)
                bstack1l11l1l11ll_opy_[key].append(hook)
                bstack1l111lllll1_opy_[bstack1lll11l11ll_opy_.bstack1l11ll111l1_opy_] = key
        TestFramework.bstack1l111ll11l1_opy_(instance, bstack1l111lllll1_opy_)
        self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᑝ") + str(bstack1l11l1l11ll_opy_) + bstack1l1lll_opy_ (u"ࠨࠢᑞ"))
    def __1l111ll1111_opy_(
        self,
        context: bstack1l11l1l1ll1_opy_,
        test_framework_state: bstack1llll1ll1l1_opy_,
        test_hook_state: bstack1llll1lll1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11111l1l_opy_(args[0], [bstack1l1lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑟ"), bstack1l1lll_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᑠ"), bstack1l1lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᑡ"), bstack1l1lll_opy_ (u"ࠥ࡭ࡩࡹࠢᑢ"), bstack1l1lll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᑣ"), bstack1l1lll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᑤ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᑥ")) else fixturedef.get(bstack1l1lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑦ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᑧ")) else None
        node = request.node if hasattr(request, bstack1l1lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᑨ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑩ")) else None
        baseid = fixturedef.get(bstack1l1lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᑪ"), None) or bstack1l1lll_opy_ (u"ࠧࠨᑫ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1lll_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᑬ")):
            target = bstack1lll11l11ll_opy_.__1l11l11l1ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᑭ")) else None
            if target and not TestFramework.bstack1111111l11_opy_(target):
                self.__1l111ll1l11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᑮ") + str(test_hook_state) + bstack1l1lll_opy_ (u"ࠤࠥᑯ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᑰ") + str(target) + bstack1l1lll_opy_ (u"ࠦࠧᑱ"))
            return None
        instance = TestFramework.bstack1111111l11_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᑲ") + str(target) + bstack1l1lll_opy_ (u"ࠨࠢᑳ"))
            return None
        bstack1l111l1l1l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11lll1l11_opy_, {})
        if os.getenv(bstack1l1lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᑴ"), bstack1l1lll_opy_ (u"ࠣ࠳ࠥᑵ")) == bstack1l1lll_opy_ (u"ࠤ࠴ࠦᑶ"):
            bstack1l11l1l1l1l_opy_ = bstack1l1lll_opy_ (u"ࠥ࠾ࠧᑷ").join((scope, fixturename))
            bstack1l11l111lll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l1l1111_opy_ = {
                bstack1l1lll_opy_ (u"ࠦࡰ࡫ࡹࠣᑸ"): bstack1l11l1l1l1l_opy_,
                bstack1l1lll_opy_ (u"ࠧࡺࡡࡨࡵࠥᑹ"): bstack1lll11l11ll_opy_.__1l11lll1lll_opy_(request.node),
                bstack1l1lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᑺ"): fixturedef,
                bstack1l1lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑻ"): scope,
                bstack1l1lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᑼ"): None,
            }
            try:
                if test_hook_state == bstack1llll1lll1l_opy_.POST and callable(getattr(args[-1], bstack1l1lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᑽ"), None)):
                    bstack1l11l1l1111_opy_[bstack1l1lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᑾ")] = TestFramework.bstack1ll11111l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1lll1l_opy_.PRE:
                bstack1l11l1l1111_opy_[bstack1l1lll_opy_ (u"ࠦࡺࡻࡩࡥࠤᑿ")] = uuid4().__str__()
                bstack1l11l1l1111_opy_[bstack1lll11l11ll_opy_.bstack1l11ll1l1ll_opy_] = bstack1l11l111lll_opy_
            elif test_hook_state == bstack1llll1lll1l_opy_.POST:
                bstack1l11l1l1111_opy_[bstack1lll11l11ll_opy_.bstack1l111l1l1ll_opy_] = bstack1l11l111lll_opy_
            if bstack1l11l1l1l1l_opy_ in bstack1l111l1l1l1_opy_:
                bstack1l111l1l1l1_opy_[bstack1l11l1l1l1l_opy_].update(bstack1l11l1l1111_opy_)
                self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᒀ") + str(bstack1l111l1l1l1_opy_[bstack1l11l1l1l1l_opy_]) + bstack1l1lll_opy_ (u"ࠨࠢᒁ"))
            else:
                bstack1l111l1l1l1_opy_[bstack1l11l1l1l1l_opy_] = bstack1l11l1l1111_opy_
                self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᒂ") + str(len(bstack1l111l1l1l1_opy_)) + bstack1l1lll_opy_ (u"ࠣࠤᒃ"))
        TestFramework.bstack1111l11l1l_opy_(instance, bstack1lll11l11ll_opy_.bstack1l11lll1l11_opy_, bstack1l111l1l1l1_opy_)
        self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᒄ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠥࠦᒅ"))
        return instance
    def __1l111ll1l11_opy_(
        self,
        context: bstack1l11l1l1ll1_opy_,
        test_framework_state: bstack1llll1ll1l1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111111ll_opy_.create_context(target)
        ob = bstack1llllll11ll_opy_(ctx, self.bstack1ll1l1111l1_opy_, self.bstack1l11l11l11l_opy_, test_framework_state)
        TestFramework.bstack1l111ll11l1_opy_(ob, {
            TestFramework.bstack1ll1l1ll11l_opy_: context.test_framework_name,
            TestFramework.bstack1ll111ll111_opy_: context.test_framework_version,
            TestFramework.bstack1l111ll1lll_opy_: [],
            bstack1lll11l11ll_opy_.bstack1l11lll1l11_opy_: {},
            bstack1lll11l11ll_opy_.bstack1l11l11lll1_opy_: {},
            bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l11l1l_opy_(ob, TestFramework.bstack1l11ll11lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l11l1l_opy_(ob, TestFramework.bstack1ll1l1lllll_opy_, context.platform_index)
        TestFramework.bstack111111l11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᒆ") + str(TestFramework.bstack111111l11l_opy_.keys()) + bstack1l1lll_opy_ (u"ࠧࠨᒇ"))
        return ob
    def bstack1l1lll11l1l_opy_(self, instance: bstack1llllll11ll_opy_, bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_]):
        bstack1l11l1l1lll_opy_ = (
            bstack1lll11l11ll_opy_.bstack1l11lll111l_opy_
            if bstack1lllllll1l1_opy_[1] == bstack1llll1lll1l_opy_.PRE
            else bstack1lll11l11ll_opy_.bstack1l11ll111l1_opy_
        )
        hook = bstack1lll11l11ll_opy_.bstack1l111ll1ll1_opy_(instance, bstack1l11l1l1lll_opy_)
        entries = hook.get(TestFramework.bstack1l11l1ll111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l111ll1lll_opy_, []))
        return entries
    def bstack1ll111llll1_opy_(self, instance: bstack1llllll11ll_opy_, bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_]):
        bstack1l11l1l1lll_opy_ = (
            bstack1lll11l11ll_opy_.bstack1l11lll111l_opy_
            if bstack1lllllll1l1_opy_[1] == bstack1llll1lll1l_opy_.PRE
            else bstack1lll11l11ll_opy_.bstack1l11ll111l1_opy_
        )
        bstack1lll11l11ll_opy_.bstack1l111lll1ll_opy_(instance, bstack1l11l1l1lll_opy_)
        TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l111ll1lll_opy_, []).clear()
    def bstack1l11l111l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᒈ")
        global _1ll111ll11l_opy_
        platform_index = os.environ[bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᒉ")]
        bstack1l1llll1lll_opy_ = os.path.join(bstack1ll111l1l1l_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), bstack1l111l111ll_opy_)
        if not os.path.exists(bstack1l1llll1lll_opy_) or not os.path.isdir(bstack1l1llll1lll_opy_):
            self.logger.info(bstack1l1lll_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᒊ").format(bstack1l1llll1lll_opy_))
            return
        logs = hook.get(bstack1l1lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᒋ"), [])
        with os.scandir(bstack1l1llll1lll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111ll11l_opy_:
                    self.logger.info(bstack1l1lll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᒌ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1lll_opy_ (u"ࠦࠧᒍ")
                    log_entry = bstack1lll1l111l1_opy_(
                        kind=bstack1l1lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒎ"),
                        message=bstack1l1lll_opy_ (u"ࠨࠢᒏ"),
                        level=bstack1l1lll_opy_ (u"ࠢࠣᒐ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll111l1111_opy_=entry.stat().st_size,
                        bstack1l1lllllll1_opy_=bstack1l1lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᒑ"),
                        bstack11l1lll_opy_=os.path.abspath(entry.path),
                        bstack1l11l11l111_opy_=hook.get(TestFramework.bstack1l11l11111l_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111ll11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒒ")]
        bstack1l11l111ll1_opy_ = os.path.join(bstack1ll111l1l1l_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), bstack1l111l111ll_opy_, bstack1l111l11lll_opy_)
        if not os.path.exists(bstack1l11l111ll1_opy_) or not os.path.isdir(bstack1l11l111ll1_opy_):
            self.logger.info(bstack1l1lll_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᒓ").format(bstack1l11l111ll1_opy_))
        else:
            self.logger.info(bstack1l1lll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᒔ").format(bstack1l11l111ll1_opy_))
            with os.scandir(bstack1l11l111ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1l1lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒕ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1lll_opy_ (u"ࠨࠢᒖ")
                        log_entry = bstack1lll1l111l1_opy_(
                            kind=bstack1l1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒗ"),
                            message=bstack1l1lll_opy_ (u"ࠣࠤᒘ"),
                            level=bstack1l1lll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᒙ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll111l1111_opy_=entry.stat().st_size,
                            bstack1l1lllllll1_opy_=bstack1l1lll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒚ"),
                            bstack11l1lll_opy_=os.path.abspath(entry.path),
                            bstack1ll1111l11l_opy_=hook.get(TestFramework.bstack1l11l11111l_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111ll11l_opy_.add(abs_path)
        hook[bstack1l1lll_opy_ (u"ࠦࡱࡵࡧࡴࠤᒛ")] = logs
    def bstack1ll111lll11_opy_(
        self,
        bstack1l1llllll11_opy_: bstack1llllll11ll_opy_,
        entries: List[bstack1lll1l111l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᒜ"))
        req.platform_index = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll1l1lllll_opy_)
        req.execution_context.hash = str(bstack1l1llllll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llllll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llllll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll1l1ll11l_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll111ll111_opy_)
            log_entry.uuid = entry.bstack1l11l11l111_opy_
            log_entry.test_framework_state = bstack1l1llllll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᒝ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1lll_opy_ (u"ࠢࠣᒞ")
            if entry.kind == bstack1l1lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒟ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll111l1111_opy_
                log_entry.file_path = entry.bstack11l1lll_opy_
        def bstack1l1llll1111_opy_():
            bstack1ll1l11l_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.LogCreatedEvent(req)
                bstack1l1llllll11_opy_.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᒠ"), datetime.now() - bstack1ll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᒡ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1l1l1_opy_.enqueue(bstack1l1llll1111_opy_)
    def __1l11ll11l11_opy_(self, instance) -> None:
        bstack1l1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒢ")
        bstack1l111lllll1_opy_ = {bstack1l1lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᒣ"): bstack1lll11ll11l_opy_.bstack1l111llll11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l111ll11l1_opy_(instance, bstack1l111lllll1_opy_)
    @staticmethod
    def bstack1l111ll1ll1_opy_(instance: bstack1llllll11ll_opy_, bstack1l11l1l1lll_opy_: str):
        bstack1l11ll11111_opy_ = (
            bstack1lll11l11ll_opy_.bstack1l11l11lll1_opy_
            if bstack1l11l1l1lll_opy_ == bstack1lll11l11ll_opy_.bstack1l11ll111l1_opy_
            else bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_
        )
        bstack1l11l1l11l1_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l11l1l1lll_opy_, None)
        bstack1l11ll1ll1l_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l11ll11111_opy_, None) if bstack1l11l1l11l1_opy_ else None
        return (
            bstack1l11ll1ll1l_opy_[bstack1l11l1l11l1_opy_][-1]
            if isinstance(bstack1l11ll1ll1l_opy_, dict) and len(bstack1l11ll1ll1l_opy_.get(bstack1l11l1l11l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111lll1ll_opy_(instance: bstack1llllll11ll_opy_, bstack1l11l1l1lll_opy_: str):
        hook = bstack1lll11l11ll_opy_.bstack1l111ll1ll1_opy_(instance, bstack1l11l1l1lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1ll111_opy_, []).clear()
    @staticmethod
    def __1l111l1l111_opy_(instance: bstack1llllll11ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1lll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᒤ"), None)):
            return
        if os.getenv(bstack1l1lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᒥ"), bstack1l1lll_opy_ (u"ࠣ࠳ࠥᒦ")) != bstack1l1lll_opy_ (u"ࠤ࠴ࠦᒧ"):
            bstack1lll11l11ll_opy_.logger.warning(bstack1l1lll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᒨ"))
            return
        bstack1l11ll1llll_opy_ = {
            bstack1l1lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᒩ"): (bstack1lll11l11ll_opy_.bstack1l11lll111l_opy_, bstack1lll11l11ll_opy_.bstack1l111l1llll_opy_),
            bstack1l1lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᒪ"): (bstack1lll11l11ll_opy_.bstack1l11ll111l1_opy_, bstack1lll11l11ll_opy_.bstack1l11l11lll1_opy_),
        }
        for when in (bstack1l1lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᒫ"), bstack1l1lll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᒬ"), bstack1l1lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᒭ")):
            bstack1l11l1l111l_opy_ = args[1].get_records(when)
            if not bstack1l11l1l111l_opy_:
                continue
            records = [
                bstack1lll1l111l1_opy_(
                    kind=TestFramework.bstack1l1ll1llll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1lll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᒮ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1lll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᒯ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11l1l111l_opy_
                if isinstance(getattr(r, bstack1l1lll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᒰ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l111111_opy_, bstack1l11ll11111_opy_ = bstack1l11ll1llll_opy_.get(when, (None, None))
            bstack1l111lll111_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l11l111111_opy_, None) if bstack1l11l111111_opy_ else None
            bstack1l11ll1ll1l_opy_ = TestFramework.bstack11111l11l1_opy_(instance, bstack1l11ll11111_opy_, None) if bstack1l111lll111_opy_ else None
            if isinstance(bstack1l11ll1ll1l_opy_, dict) and len(bstack1l11ll1ll1l_opy_.get(bstack1l111lll111_opy_, [])) > 0:
                hook = bstack1l11ll1ll1l_opy_[bstack1l111lll111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l1ll111_opy_ in hook:
                    hook[TestFramework.bstack1l11l1ll111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l111ll1lll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111llllll_opy_(test) -> Dict[str, Any]:
        bstack1ll111lll_opy_ = bstack1lll11l11ll_opy_.__1l11l11l1ll_opy_(test.location) if hasattr(test, bstack1l1lll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᒱ")) else getattr(test, bstack1l1lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒲ"), None)
        test_name = test.name if hasattr(test, bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᒳ")) else None
        bstack1l111ll111l_opy_ = test.fspath.strpath if hasattr(test, bstack1l1lll_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᒴ")) and test.fspath else None
        if not bstack1ll111lll_opy_ or not test_name or not bstack1l111ll111l_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1lll_opy_ (u"ࠤࡲࡦ࡯ࠨᒵ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l11l11_opy_ = []
        try:
            bstack1l111l11l11_opy_ = bstack1l11ll11ll_opy_.bstack111lll111l_opy_(test)
        except:
            bstack1lll11l11ll_opy_.logger.warning(bstack1l1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᒶ"))
        return {
            TestFramework.bstack1ll1l1l11l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11lll11l1_opy_: bstack1ll111lll_opy_,
            TestFramework.bstack1ll1l11ll11_opy_: test_name,
            TestFramework.bstack1l1ll1l11ll_opy_: getattr(test, bstack1l1lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᒷ"), None),
            TestFramework.bstack1l111ll1l1l_opy_: bstack1l111ll111l_opy_,
            TestFramework.bstack1l11ll111ll_opy_: bstack1lll11l11ll_opy_.__1l11lll1lll_opy_(test),
            TestFramework.bstack1l11ll11l1l_opy_: code,
            TestFramework.bstack1l1l1ll1ll1_opy_: TestFramework.bstack1l11l1111l1_opy_,
            TestFramework.bstack1l1l111l1ll_opy_: bstack1ll111lll_opy_,
            TestFramework.bstack1l111l111l1_opy_: bstack1l111l11l11_opy_
        }
    @staticmethod
    def __1l11lll1lll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1lll_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᒸ"), [])
            markers.extend([getattr(m, bstack1l1lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᒹ"), None) for m in own_markers if getattr(m, bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᒺ"), None)])
            current = getattr(current, bstack1l1lll_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᒻ"), None)
        return markers
    @staticmethod
    def __1l11l11l1ll_opy_(location):
        return bstack1l1lll_opy_ (u"ࠤ࠽࠾ࠧᒼ").join(filter(lambda x: isinstance(x, str), location))