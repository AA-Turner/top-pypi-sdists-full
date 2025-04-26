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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll1111ll_opy_,
    bstack1lll1lllll1_opy_,
    bstack1lll1l1l11l_opy_,
    bstack1l11l1l111l_opy_,
    bstack1ll1lllllll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1llll1lll_opy_
from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1l1l1_opy_ import bstack1111l1ll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll11111l1_opy_ import bstack1llll11llll_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111l1llll_opy_
bstack1l1llllllll_opy_ = bstack1l1llll1lll_opy_()
bstack1l11ll1ll11_opy_ = 1.0
bstack1l1ll1lll1l_opy_ = bstack1l11lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᐛ")
bstack1l111l111l1_opy_ = bstack1l11lll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᐜ")
bstack1l111l111ll_opy_ = bstack1l11lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᐝ")
bstack1l111l11ll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᐞ")
bstack1l111l11l11_opy_ = bstack1l11lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᐟ")
_1ll111111l1_opy_ = set()
class bstack1lll1lll11l_opy_(TestFramework):
    bstack1l111l1l1ll_opy_ = bstack1l11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᐠ")
    bstack1l111l1ll11_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᐡ")
    bstack1l111l1l1l1_opy_ = bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᐢ")
    bstack1l111ll111l_opy_ = bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᐣ")
    bstack1l111l1ll1l_opy_ = bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᐤ")
    bstack1l11ll1l111_opy_: bool
    bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_  = None
    bstack1lll1ll11ll_opy_ = None
    bstack1l11ll1lll1_opy_ = [
        bstack1llll1111ll_opy_.BEFORE_ALL,
        bstack1llll1111ll_opy_.AFTER_ALL,
        bstack1llll1111ll_opy_.BEFORE_EACH,
        bstack1llll1111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll111_opy_: Dict[str, str],
        bstack1ll1l11ll11_opy_: List[str]=[bstack1l11lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᐥ")],
        bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_=None,
        bstack1lll1ll11ll_opy_=None
    ):
        super().__init__(bstack1ll1l11ll11_opy_, bstack1l11llll111_opy_, bstack1111l1l1l1_opy_)
        self.bstack1l11ll1l111_opy_ = any(bstack1l11lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᐦ") in item.lower() for item in bstack1ll1l11ll11_opy_)
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
        if test_framework_state == bstack1llll1111ll_opy_.TEST or test_framework_state in bstack1lll1lll11l_opy_.bstack1l11ll1lll1_opy_:
            bstack1l11l11111l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll1111ll_opy_.NONE:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᐧ") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠣࠤᐨ"))
            return
        if not self.bstack1l11ll1l111_opy_:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᐩ") + str(str(self.bstack1ll1l11ll11_opy_)) + bstack1l11lll_opy_ (u"ࠥࠦᐪ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᐫ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨᐬ"))
            return
        instance = self.__1l11ll1ll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᐭ") + str(args) + bstack1l11lll_opy_ (u"ࠢࠣᐮ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1lll11l_opy_.bstack1l11ll1lll1_opy_ and test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack11l111l1_opy_.value)
                name = str(EVENTS.bstack11l111l1_opy_.name)+bstack1l11lll_opy_ (u"ࠣ࠼ࠥᐯ")+str(test_framework_state.name)
                TestFramework.bstack1l11l11lll1_opy_(instance, name, bstack1ll1ll1l111_opy_)
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᐰ").format(e))
        try:
            if not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l11ll11111_opy_) and test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                test = bstack1lll1lll11l_opy_.__1l111lllll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐱ") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠦࠧᐲ"))
            if test_framework_state == bstack1llll1111ll_opy_.TEST:
                if test_hook_state == bstack1lll1l1l11l_opy_.PRE and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1l1lllll1ll_opy_):
                    TestFramework.bstack1111l111ll_opy_(instance, TestFramework.bstack1l1lllll1ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐳ") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠨࠢᐴ"))
                elif test_hook_state == bstack1lll1l1l11l_opy_.POST and not TestFramework.bstack11111ll11l_opy_(instance, TestFramework.bstack1ll111ll11l_opy_):
                    TestFramework.bstack1111l111ll_opy_(instance, TestFramework.bstack1ll111ll11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᐵ") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠣࠤᐶ"))
            elif test_framework_state == bstack1llll1111ll_opy_.LOG and test_hook_state == bstack1lll1l1l11l_opy_.POST:
                bstack1lll1lll11l_opy_.__1l111ll11ll_opy_(instance, *args)
            elif test_framework_state == bstack1llll1111ll_opy_.LOG_REPORT and test_hook_state == bstack1lll1l1l11l_opy_.POST:
                self.__1l11lll1ll1_opy_(instance, *args)
                self.__1l11ll1111l_opy_(instance)
            elif test_framework_state in bstack1lll1lll11l_opy_.bstack1l11ll1lll1_opy_:
                self.__1l111l1llll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᐷ") + str(instance.ref()) + bstack1l11lll_opy_ (u"ࠥࠦᐸ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111lll1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1lll11l_opy_.bstack1l11ll1lll1_opy_ and test_hook_state == bstack1lll1l1l11l_opy_.POST:
                name = str(EVENTS.bstack11l111l1_opy_.name)+bstack1l11lll_opy_ (u"ࠦ࠿ࠨᐹ")+str(test_framework_state.name)
                bstack1ll1ll1l111_opy_ = TestFramework.bstack1l11l1111l1_opy_(instance, name)
                bstack1ll1llll111_opy_.end(EVENTS.bstack11l111l1_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᐺ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᐻ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᐼ").format(e))
    def bstack1ll111llll1_opy_(self):
        return self.bstack1l11ll1l111_opy_
    def __1l11l1l1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l11lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᐽ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll11l11111_opy_(rep, [bstack1l11lll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᐾ"), bstack1l11lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᐿ"), bstack1l11lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᑀ"), bstack1l11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᑁ"), bstack1l11lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᑂ"), bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᑃ")])
        return None
    def __1l11lll1ll1_opy_(self, instance: bstack1lll1lllll1_opy_, *args):
        result = self.__1l11l1l1l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111l1llll_opy_ = None
        if result.get(bstack1l11lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᑄ"), None) == bstack1l11lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᑅ") and len(args) > 1 and getattr(args[1], bstack1l11lll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᑆ"), None) is not None:
            failure = [{bstack1l11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᑇ"): [args[1].excinfo.exconly(), result.get(bstack1l11lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᑈ"), None)]}]
            bstack1111l1llll_opy_ = bstack1l11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᑉ") if bstack1l11lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᑊ") in getattr(args[1].excinfo, bstack1l11lll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᑋ"), bstack1l11lll_opy_ (u"ࠤࠥᑌ")) else bstack1l11lll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᑍ")
        bstack1l111lll111_opy_ = result.get(bstack1l11lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑎ"), TestFramework.bstack1l11lll111l_opy_)
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
            target = None # bstack1l111lll11l_opy_ bstack1l11l1lll11_opy_ this to be bstack1l11lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑏ")
            if test_framework_state == bstack1llll1111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l11l11l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll1111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l11lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᑐ"), None), bstack1l11lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑑ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l11lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑒ"), None):
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
        bstack1l11ll1l11l_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111l1ll11_opy_, {})
        if not key in bstack1l11ll1l11l_opy_:
            bstack1l11ll1l11l_opy_[key] = []
        bstack1l11lll1l1l_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111l1l1l1_opy_, {})
        if not key in bstack1l11lll1l1l_opy_:
            bstack1l11lll1l1l_opy_[key] = []
        bstack1l11ll11lll_opy_ = {
            bstack1lll1lll11l_opy_.bstack1l111l1ll11_opy_: bstack1l11ll1l11l_opy_,
            bstack1lll1lll11l_opy_.bstack1l111l1l1l1_opy_: bstack1l11lll1l1l_opy_,
        }
        if test_hook_state == bstack1lll1l1l11l_opy_.PRE:
            hook = {
                bstack1l11lll_opy_ (u"ࠤ࡮ࡩࡾࠨᑓ"): key,
                TestFramework.bstack1l11ll11ll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l11_opy_: TestFramework.bstack1l11l1lll1l_opy_,
                TestFramework.bstack1l11l1l1111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11lll11ll_opy_: [],
                TestFramework.bstack1l11lll1lll_opy_: args[1] if len(args) > 1 else bstack1l11lll_opy_ (u"ࠪࠫᑔ"),
                TestFramework.bstack1l111l1lll1_opy_: bstack1llll11llll_opy_.bstack1l11l1ll11l_opy_()
            }
            bstack1l11ll1l11l_opy_[key].append(hook)
            bstack1l11ll11lll_opy_[bstack1lll1lll11l_opy_.bstack1l111ll111l_opy_] = key
        elif test_hook_state == bstack1lll1l1l11l_opy_.POST:
            bstack1l11lll11l1_opy_ = bstack1l11ll1l11l_opy_.get(key, [])
            hook = bstack1l11lll11l1_opy_.pop() if bstack1l11lll11l1_opy_ else None
            if hook:
                result = self.__1l11l1l1l11_opy_(*args)
                if result:
                    bstack1l11l1l1l1l_opy_ = result.get(bstack1l11lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᑕ"), TestFramework.bstack1l11l1lll1l_opy_)
                    if bstack1l11l1l1l1l_opy_ != TestFramework.bstack1l11l1lll1l_opy_:
                        hook[TestFramework.bstack1l11ll11l11_opy_] = bstack1l11l1l1l1l_opy_
                hook[TestFramework.bstack1l11l111ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111l1lll1_opy_]= bstack1llll11llll_opy_.bstack1l11l1ll11l_opy_()
                self.bstack1l11ll111ll_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1llll1_opy_, [])
                if logs: self.bstack1ll111l11ll_opy_(instance, logs)
                bstack1l11lll1l1l_opy_[key].append(hook)
                bstack1l11ll11lll_opy_[bstack1lll1lll11l_opy_.bstack1l111l1ll1l_opy_] = key
        TestFramework.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11lll_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᑖ") + str(bstack1l11lll1l1l_opy_) + bstack1l11lll_opy_ (u"ࠨࠢᑗ"))
    def __1l11l11l1l1_opy_(
        self,
        context: bstack1l11l1l111l_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        test_hook_state: bstack1lll1l1l11l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll11l11111_opy_(args[0], [bstack1l11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑘ"), bstack1l11lll_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᑙ"), bstack1l11lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᑚ"), bstack1l11lll_opy_ (u"ࠥ࡭ࡩࡹࠢᑛ"), bstack1l11lll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᑜ"), bstack1l11lll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᑝ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l11lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᑞ")) else fixturedef.get(bstack1l11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑟ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l11lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᑠ")) else None
        node = request.node if hasattr(request, bstack1l11lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᑡ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l11lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑢ")) else None
        baseid = fixturedef.get(bstack1l11lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᑣ"), None) or bstack1l11lll_opy_ (u"ࠧࠨᑤ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l11lll_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᑥ")):
            target = bstack1lll1lll11l_opy_.__1l111llllll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᑦ")) else None
            if target and not TestFramework.bstack1111111l1l_opy_(target):
                self.__1l11l11l11l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᑧ") + str(test_hook_state) + bstack1l11lll_opy_ (u"ࠤࠥᑨ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᑩ") + str(target) + bstack1l11lll_opy_ (u"ࠦࠧᑪ"))
            return None
        instance = TestFramework.bstack1111111l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᑫ") + str(target) + bstack1l11lll_opy_ (u"ࠨࠢᑬ"))
            return None
        bstack1l11l1l11ll_opy_ = TestFramework.bstack1111111111_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111l1l1ll_opy_, {})
        if os.getenv(bstack1l11lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᑭ"), bstack1l11lll_opy_ (u"ࠣ࠳ࠥᑮ")) == bstack1l11lll_opy_ (u"ࠤ࠴ࠦᑯ"):
            bstack1l111ll11l1_opy_ = bstack1l11lll_opy_ (u"ࠥ࠾ࠧᑰ").join((scope, fixturename))
            bstack1l11l111l1l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11llll11l_opy_ = {
                bstack1l11lll_opy_ (u"ࠦࡰ࡫ࡹࠣᑱ"): bstack1l111ll11l1_opy_,
                bstack1l11lll_opy_ (u"ࠧࡺࡡࡨࡵࠥᑲ"): bstack1lll1lll11l_opy_.__1l11ll1llll_opy_(request.node),
                bstack1l11lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᑳ"): fixturedef,
                bstack1l11lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑴ"): scope,
                bstack1l11lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᑵ"): None,
            }
            try:
                if test_hook_state == bstack1lll1l1l11l_opy_.POST and callable(getattr(args[-1], bstack1l11lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᑶ"), None)):
                    bstack1l11llll11l_opy_[bstack1l11lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᑷ")] = TestFramework.bstack1l1llll1111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1l1l11l_opy_.PRE:
                bstack1l11llll11l_opy_[bstack1l11lll_opy_ (u"ࠦࡺࡻࡩࡥࠤᑸ")] = uuid4().__str__()
                bstack1l11llll11l_opy_[bstack1lll1lll11l_opy_.bstack1l11l1l1111_opy_] = bstack1l11l111l1l_opy_
            elif test_hook_state == bstack1lll1l1l11l_opy_.POST:
                bstack1l11llll11l_opy_[bstack1lll1lll11l_opy_.bstack1l11l111ll1_opy_] = bstack1l11l111l1l_opy_
            if bstack1l111ll11l1_opy_ in bstack1l11l1l11ll_opy_:
                bstack1l11l1l11ll_opy_[bstack1l111ll11l1_opy_].update(bstack1l11llll11l_opy_)
                self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᑹ") + str(bstack1l11l1l11ll_opy_[bstack1l111ll11l1_opy_]) + bstack1l11lll_opy_ (u"ࠨࠢᑺ"))
            else:
                bstack1l11l1l11ll_opy_[bstack1l111ll11l1_opy_] = bstack1l11llll11l_opy_
                self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᑻ") + str(len(bstack1l11l1l11ll_opy_)) + bstack1l11lll_opy_ (u"ࠣࠤᑼ"))
        TestFramework.bstack1111l111ll_opy_(instance, bstack1lll1lll11l_opy_.bstack1l111l1l1ll_opy_, bstack1l11l1l11ll_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᑽ") + str(instance.ref()) + bstack1l11lll_opy_ (u"ࠥࠦᑾ"))
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
            bstack1lll1lll11l_opy_.bstack1l111l1l1ll_opy_: {},
            bstack1lll1lll11l_opy_.bstack1l111l1l1l1_opy_: {},
            bstack1lll1lll11l_opy_.bstack1l111l1ll11_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111l111ll_opy_(ob, TestFramework.bstack1l111ll1ll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111l111ll_opy_(ob, TestFramework.bstack1ll1l111lll_opy_, context.platform_index)
        TestFramework.bstack11111lllll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᑿ") + str(TestFramework.bstack11111lllll_opy_.keys()) + bstack1l11lll_opy_ (u"ࠧࠨᒀ"))
        return ob
    def bstack1ll111l1lll_opy_(self, instance: bstack1lll1lllll1_opy_, bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_]):
        bstack1l11l1ll1ll_opy_ = (
            bstack1lll1lll11l_opy_.bstack1l111ll111l_opy_
            if bstack11111l11ll_opy_[1] == bstack1lll1l1l11l_opy_.PRE
            else bstack1lll1lll11l_opy_.bstack1l111l1ll1l_opy_
        )
        hook = bstack1lll1lll11l_opy_.bstack1l11l111l11_opy_(instance, bstack1l11l1ll1ll_opy_)
        entries = hook.get(TestFramework.bstack1l11lll11ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l111l1l11l_opy_, []))
        return entries
    def bstack1l1lll1ll1l_opy_(self, instance: bstack1lll1lllll1_opy_, bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_]):
        bstack1l11l1ll1ll_opy_ = (
            bstack1lll1lll11l_opy_.bstack1l111ll111l_opy_
            if bstack11111l11ll_opy_[1] == bstack1lll1l1l11l_opy_.PRE
            else bstack1lll1lll11l_opy_.bstack1l111l1ll1l_opy_
        )
        bstack1lll1lll11l_opy_.bstack1l11l111lll_opy_(instance, bstack1l11l1ll1ll_opy_)
        TestFramework.bstack1111111111_opy_(instance, TestFramework.bstack1l111l1l11l_opy_, []).clear()
    def bstack1l11ll111ll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l11lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᒁ")
        global _1ll111111l1_opy_
        platform_index = os.environ[bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᒂ")]
        bstack1l1lll1l1l1_opy_ = os.path.join(bstack1l1llllllll_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), bstack1l111l11ll1_opy_)
        if not os.path.exists(bstack1l1lll1l1l1_opy_) or not os.path.isdir(bstack1l1lll1l1l1_opy_):
            self.logger.info(bstack1l11lll_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᒃ").format(bstack1l1lll1l1l1_opy_))
            return
        logs = hook.get(bstack1l11lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᒄ"), [])
        with os.scandir(bstack1l1lll1l1l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111111l1_opy_:
                    self.logger.info(bstack1l11lll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᒅ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l11lll_opy_ (u"ࠦࠧᒆ")
                    log_entry = bstack1ll1lllllll_opy_(
                        kind=bstack1l11lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᒇ"),
                        message=bstack1l11lll_opy_ (u"ࠨࠢᒈ"),
                        level=bstack1l11lll_opy_ (u"ࠢࠣᒉ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll1111111l_opy_=entry.stat().st_size,
                        bstack1ll11111111_opy_=bstack1l11lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᒊ"),
                        bstack11111l1_opy_=os.path.abspath(entry.path),
                        bstack1l11l11ll11_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒋ")]
        bstack1l11l1111ll_opy_ = os.path.join(bstack1l1llllllll_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), bstack1l111l11ll1_opy_, bstack1l111l11l11_opy_)
        if not os.path.exists(bstack1l11l1111ll_opy_) or not os.path.isdir(bstack1l11l1111ll_opy_):
            self.logger.info(bstack1l11lll_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᒌ").format(bstack1l11l1111ll_opy_))
        else:
            self.logger.info(bstack1l11lll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᒍ").format(bstack1l11l1111ll_opy_))
            with os.scandir(bstack1l11l1111ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111111l1_opy_:
                        self.logger.info(bstack1l11lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒎ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l11lll_opy_ (u"ࠨࠢᒏ")
                        log_entry = bstack1ll1lllllll_opy_(
                            kind=bstack1l11lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒐ"),
                            message=bstack1l11lll_opy_ (u"ࠣࠤᒑ"),
                            level=bstack1l11lll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᒒ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll1111111l_opy_=entry.stat().st_size,
                            bstack1ll11111111_opy_=bstack1l11lll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒓ"),
                            bstack11111l1_opy_=os.path.abspath(entry.path),
                            bstack1ll11111l11_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111111l1_opy_.add(abs_path)
        hook[bstack1l11lll_opy_ (u"ࠦࡱࡵࡧࡴࠤᒔ")] = logs
    def bstack1ll111l11ll_opy_(
        self,
        bstack1ll111ll1ll_opy_: bstack1lll1lllll1_opy_,
        entries: List[bstack1ll1lllllll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᒕ"))
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
            log_entry.message = entry.message.encode(bstack1l11lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᒖ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l11lll_opy_ (u"ࠢࠣᒗ")
            if entry.kind == bstack1l11lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒘ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll1111111l_opy_
                log_entry.file_path = entry.bstack11111l1_opy_
        def bstack1ll111lllll_opy_():
            bstack1ll1ll11ll_opy_ = datetime.now()
            try:
                self.bstack1lll1ll11ll_opy_.LogCreatedEvent(req)
                bstack1ll111ll1ll_opy_.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᒙ"), datetime.now() - bstack1ll1ll11ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᒚ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1l1l1_opy_.enqueue(bstack1ll111lllll_opy_)
    def __1l11ll1111l_opy_(self, instance) -> None:
        bstack1l11lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᒛ")
        bstack1l11ll11lll_opy_ = {bstack1l11lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᒜ"): bstack1llll11llll_opy_.bstack1l11l1ll11l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11ll11l1l_opy_(instance, bstack1l11ll11lll_opy_)
    @staticmethod
    def bstack1l11l111l11_opy_(instance: bstack1lll1lllll1_opy_, bstack1l11l1ll1ll_opy_: str):
        bstack1l11lll1l11_opy_ = (
            bstack1lll1lll11l_opy_.bstack1l111l1l1l1_opy_
            if bstack1l11l1ll1ll_opy_ == bstack1lll1lll11l_opy_.bstack1l111l1ll1l_opy_
            else bstack1lll1lll11l_opy_.bstack1l111l1ll11_opy_
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
        hook = bstack1lll1lll11l_opy_.bstack1l11l111l11_opy_(instance, bstack1l11l1ll1ll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11lll11ll_opy_, []).clear()
    @staticmethod
    def __1l111ll11ll_opy_(instance: bstack1lll1lllll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l11lll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᒝ"), None)):
            return
        if os.getenv(bstack1l11lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᒞ"), bstack1l11lll_opy_ (u"ࠣ࠳ࠥᒟ")) != bstack1l11lll_opy_ (u"ࠤ࠴ࠦᒠ"):
            bstack1lll1lll11l_opy_.logger.warning(bstack1l11lll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᒡ"))
            return
        bstack1l111ll1l11_opy_ = {
            bstack1l11lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᒢ"): (bstack1lll1lll11l_opy_.bstack1l111ll111l_opy_, bstack1lll1lll11l_opy_.bstack1l111l1ll11_opy_),
            bstack1l11lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᒣ"): (bstack1lll1lll11l_opy_.bstack1l111l1ll1l_opy_, bstack1lll1lll11l_opy_.bstack1l111l1l1l1_opy_),
        }
        for when in (bstack1l11lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᒤ"), bstack1l11lll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᒥ"), bstack1l11lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᒦ")):
            bstack1l111llll11_opy_ = args[1].get_records(when)
            if not bstack1l111llll11_opy_:
                continue
            records = [
                bstack1ll1lllllll_opy_(
                    kind=TestFramework.bstack1l1lllllll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l11lll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᒧ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l11lll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᒨ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111llll11_opy_
                if isinstance(getattr(r, bstack1l11lll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᒩ"), None), str) and r.message.strip()
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
    def __1l111lllll1_opy_(test) -> Dict[str, Any]:
        bstack1ll1l111l_opy_ = bstack1lll1lll11l_opy_.__1l111llllll_opy_(test.location) if hasattr(test, bstack1l11lll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᒪ")) else getattr(test, bstack1l11lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒫ"), None)
        test_name = test.name if hasattr(test, bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᒬ")) else None
        bstack1l11l1l1lll_opy_ = test.fspath.strpath if hasattr(test, bstack1l11lll_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᒭ")) and test.fspath else None
        if not bstack1ll1l111l_opy_ or not test_name or not bstack1l11l1l1lll_opy_:
            return None
        code = None
        if hasattr(test, bstack1l11lll_opy_ (u"ࠤࡲࡦ࡯ࠨᒮ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l11lll_opy_ = []
        try:
            bstack1l111l11lll_opy_ = bstack111l1llll_opy_.bstack111ll1ll11_opy_(test)
        except:
            bstack1lll1lll11l_opy_.logger.warning(bstack1l11lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᒯ"))
        return {
            TestFramework.bstack1ll1ll11lll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll11111_opy_: bstack1ll1l111l_opy_,
            TestFramework.bstack1ll1ll111l1_opy_: test_name,
            TestFramework.bstack1l1ll1l1ll1_opy_: getattr(test, bstack1l11lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᒰ"), None),
            TestFramework.bstack1l11l11l111_opy_: bstack1l11l1l1lll_opy_,
            TestFramework.bstack1l11ll1l1l1_opy_: bstack1lll1lll11l_opy_.__1l11ll1llll_opy_(test),
            TestFramework.bstack1l11lll1111_opy_: code,
            TestFramework.bstack1l1l1ll11ll_opy_: TestFramework.bstack1l11lll111l_opy_,
            TestFramework.bstack1l1l111l1l1_opy_: bstack1ll1l111l_opy_,
            TestFramework.bstack1l111l11l1l_opy_: bstack1l111l11lll_opy_
        }
    @staticmethod
    def __1l11ll1llll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l11lll_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᒱ"), [])
            markers.extend([getattr(m, bstack1l11lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᒲ"), None) for m in own_markers if getattr(m, bstack1l11lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᒳ"), None)])
            current = getattr(current, bstack1l11lll_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᒴ"), None)
        return markers
    @staticmethod
    def __1l111llllll_opy_(location):
        return bstack1l11lll_opy_ (u"ࠤ࠽࠾ࠧᒵ").join(filter(lambda x: isinstance(x, str), location))