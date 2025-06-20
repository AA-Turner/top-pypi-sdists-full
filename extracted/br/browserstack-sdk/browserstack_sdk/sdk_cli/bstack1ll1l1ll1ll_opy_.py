# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack111111l111_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1ll1_opy_ import bstack1l111l11l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1llll11111l_opy_,
    bstack1llll111l11_opy_,
    bstack1ll1l1lll11_opy_,
    bstack1l11l11l1l1_opy_,
    bstack1lll11lll11_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lllll111_opy_
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack111111ll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1l11ll_opy_ import bstack1lll11ll1ll_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1ll11_opy_
bstack1l1ll11ll1l_opy_ = bstack1l1lllll111_opy_()
bstack1l11l11111l_opy_ = 1.0
bstack1l1lllllll1_opy_ = bstack11ll11_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᑶ")
bstack11lllllllll_opy_ = bstack11ll11_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᑷ")
bstack1l111111111_opy_ = bstack11ll11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᑸ")
bstack1l1111111ll_opy_ = bstack11ll11_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᑹ")
bstack1l11111111l_opy_ = bstack11ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᑺ")
_1l1ll1lll11_opy_ = set()
class bstack1lll1lllll1_opy_(TestFramework):
    bstack1l111lll111_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᑻ")
    bstack1l11l111ll1_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᑼ")
    bstack1l11111l111_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᑽ")
    bstack1l1111llll1_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᑾ")
    bstack1l11111lll1_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᑿ")
    bstack1l111ll11ll_opy_: bool
    bstack111111l1ll_opy_: bstack111111ll1l_opy_  = None
    bstack1llll1l1l11_opy_ = None
    bstack1l111l11ll1_opy_ = [
        bstack1llll11111l_opy_.BEFORE_ALL,
        bstack1llll11111l_opy_.AFTER_ALL,
        bstack1llll11111l_opy_.BEFORE_EACH,
        bstack1llll11111l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l111ll_opy_: Dict[str, str],
        bstack1ll11l11l1l_opy_: List[str]=[bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᒀ")],
        bstack111111l1ll_opy_: bstack111111ll1l_opy_=None,
        bstack1llll1l1l11_opy_=None
    ):
        super().__init__(bstack1ll11l11l1l_opy_, bstack1l111l111ll_opy_, bstack111111l1ll_opy_)
        self.bstack1l111ll11ll_opy_ = any(bstack11ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᒁ") in item.lower() for item in bstack1ll11l11l1l_opy_)
        self.bstack1llll1l1l11_opy_ = bstack1llll1l1l11_opy_
    def track_event(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1llll11111l_opy_.TEST or test_framework_state in bstack1lll1lllll1_opy_.bstack1l111l11ll1_opy_:
            bstack1l111l11l1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1llll11111l_opy_.NONE:
            self.logger.warning(bstack11ll11_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᒂ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠣࠤᒃ"))
            return
        if not self.bstack1l111ll11ll_opy_:
            self.logger.warning(bstack11ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᒄ") + str(str(self.bstack1ll11l11l1l_opy_)) + bstack11ll11_opy_ (u"ࠥࠦᒅ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᒆ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨᒇ"))
            return
        instance = self.__1l1111l11ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᒈ") + str(args) + bstack11ll11_opy_ (u"ࠢࠣᒉ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1lllll1_opy_.bstack1l111l11ll1_opy_ and test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l11l1lll1_opy_.value)
                name = str(EVENTS.bstack1l11l1lll1_opy_.name)+bstack11ll11_opy_ (u"ࠣ࠼ࠥᒊ")+str(test_framework_state.name)
                TestFramework.bstack1l1111l11l1_opy_(instance, name, bstack1ll11ll111l_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᒋ").format(e))
        try:
            if not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l11l1l1ll1_opy_) and test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                test = bstack1lll1lllll1_opy_.__1l1111ll1ll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11ll11_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᒌ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠦࠧᒍ"))
            if test_framework_state == bstack1llll11111l_opy_.TEST:
                if test_hook_state == bstack1ll1l1lll11_opy_.PRE and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll1lll1_opy_):
                    TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1lll1lll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᒎ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠨࠢᒏ"))
                elif test_hook_state == bstack1ll1l1lll11_opy_.POST and not TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_):
                    TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1lll1l111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᒐ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠣࠤᒑ"))
            elif test_framework_state == bstack1llll11111l_opy_.LOG and test_hook_state == bstack1ll1l1lll11_opy_.POST:
                bstack1lll1lllll1_opy_.__1l11111l1l1_opy_(instance, *args)
            elif test_framework_state == bstack1llll11111l_opy_.LOG_REPORT and test_hook_state == bstack1ll1l1lll11_opy_.POST:
                self.__1l1111l1l11_opy_(instance, *args)
                self.__1l111l1l1ll_opy_(instance)
            elif test_framework_state in bstack1lll1lllll1_opy_.bstack1l111l11ll1_opy_:
                self.__1l111l1lll1_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᒒ") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠥࠦᒓ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11111ll1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1lllll1_opy_.bstack1l111l11ll1_opy_ and test_hook_state == bstack1ll1l1lll11_opy_.POST:
                name = str(EVENTS.bstack1l11l1lll1_opy_.name)+bstack11ll11_opy_ (u"ࠦ࠿ࠨᒔ")+str(test_framework_state.name)
                bstack1ll11ll111l_opy_ = TestFramework.bstack1l111ll111l_opy_(instance, name)
                bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1l11l1lll1_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᒕ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᒖ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᒗ").format(e))
    def bstack1l1llllllll_opy_(self):
        return self.bstack1l111ll11ll_opy_
    def __1l111l1ll11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᒘ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll1lll1l_opy_(rep, [bstack11ll11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᒙ"), bstack11ll11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᒚ"), bstack11ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᒛ"), bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᒜ"), bstack11ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᒝ"), bstack11ll11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᒞ")])
        return None
    def __1l1111l1l11_opy_(self, instance: bstack1llll111l11_opy_, *args):
        result = self.__1l111l1ll11_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l111l_opy_ = None
        if result.get(bstack11ll11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᒟ"), None) == bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᒠ") and len(args) > 1 and getattr(args[1], bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᒡ"), None) is not None:
            failure = [{bstack11ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᒢ"): [args[1].excinfo.exconly(), result.get(bstack11ll11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᒣ"), None)]}]
            bstack11111l111l_opy_ = bstack11ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᒤ") if bstack11ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᒥ") in getattr(args[1].excinfo, bstack11ll11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᒦ"), bstack11ll11_opy_ (u"ࠤࠥᒧ")) else bstack11ll11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᒨ")
        bstack1l11l11llll_opy_ = result.get(bstack11ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᒩ"), TestFramework.bstack1l111111l1l_opy_)
        if bstack1l11l11llll_opy_ != TestFramework.bstack1l111111l1l_opy_:
            TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1llll11ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1111lll11_opy_(instance, {
            TestFramework.bstack1l1l11l1lll_opy_: failure,
            TestFramework.bstack1l1111ll1l1_opy_: bstack11111l111l_opy_,
            TestFramework.bstack1l1l11l11l1_opy_: bstack1l11l11llll_opy_,
        })
    def __1l1111l11ll_opy_(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1llll11111l_opy_.SETUP_FIXTURE:
            instance = self.__1l1111l111l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l1l111_opy_ bstack1l111ll1l11_opy_ this to be bstack11ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᒪ")
            if test_framework_state == bstack1llll11111l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l111l11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1llll11111l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᒫ"), None), bstack11ll11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᒬ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒭ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111111l1_opy_(target) if target else None
        return instance
    def __1l111l1lll1_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l1111l1l1l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1lll1lllll1_opy_.bstack1l11l111ll1_opy_, {})
        if not key in bstack1l1111l1l1l_opy_:
            bstack1l1111l1l1l_opy_[key] = []
        bstack1l11l1l111l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1lll1lllll1_opy_.bstack1l11111l111_opy_, {})
        if not key in bstack1l11l1l111l_opy_:
            bstack1l11l1l111l_opy_[key] = []
        bstack1l111ll1lll_opy_ = {
            bstack1lll1lllll1_opy_.bstack1l11l111ll1_opy_: bstack1l1111l1l1l_opy_,
            bstack1lll1lllll1_opy_.bstack1l11111l111_opy_: bstack1l11l1l111l_opy_,
        }
        if test_hook_state == bstack1ll1l1lll11_opy_.PRE:
            hook = {
                bstack11ll11_opy_ (u"ࠤ࡮ࡩࡾࠨᒮ"): key,
                TestFramework.bstack1l111111ll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111l1111_opy_: TestFramework.bstack1l1111l1ll1_opy_,
                TestFramework.bstack1l1111ll11l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1111lllll_opy_: [],
                TestFramework.bstack1l11l1l11ll_opy_: args[1] if len(args) > 1 else bstack11ll11_opy_ (u"ࠪࠫᒯ"),
                TestFramework.bstack1l111ll11l1_opy_: bstack1lll11ll1ll_opy_.bstack1l111llll11_opy_()
            }
            bstack1l1111l1l1l_opy_[key].append(hook)
            bstack1l111ll1lll_opy_[bstack1lll1lllll1_opy_.bstack1l1111llll1_opy_] = key
        elif test_hook_state == bstack1ll1l1lll11_opy_.POST:
            bstack1l111lllll1_opy_ = bstack1l1111l1l1l_opy_.get(key, [])
            hook = bstack1l111lllll1_opy_.pop() if bstack1l111lllll1_opy_ else None
            if hook:
                result = self.__1l111l1ll11_opy_(*args)
                if result:
                    bstack1l11111llll_opy_ = result.get(bstack11ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᒰ"), TestFramework.bstack1l1111l1ll1_opy_)
                    if bstack1l11111llll_opy_ != TestFramework.bstack1l1111l1ll1_opy_:
                        hook[TestFramework.bstack1l1111l1111_opy_] = bstack1l11111llll_opy_
                hook[TestFramework.bstack1l111lll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll11l1_opy_]= bstack1lll11ll1ll_opy_.bstack1l111llll11_opy_()
                self.bstack1l11l1l1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l11lll_opy_, [])
                if logs: self.bstack1l1ll11l1ll_opy_(instance, logs)
                bstack1l11l1l111l_opy_[key].append(hook)
                bstack1l111ll1lll_opy_[bstack1lll1lllll1_opy_.bstack1l11111lll1_opy_] = key
        TestFramework.bstack1l1111lll11_opy_(instance, bstack1l111ll1lll_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᒱ") + str(bstack1l11l1l111l_opy_) + bstack11ll11_opy_ (u"ࠨࠢᒲ"))
    def __1l1111l111l_opy_(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll1lll1l_opy_(args[0], [bstack11ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᒳ"), bstack11ll11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᒴ"), bstack11ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᒵ"), bstack11ll11_opy_ (u"ࠥ࡭ࡩࡹࠢᒶ"), bstack11ll11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᒷ"), bstack11ll11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᒸ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11ll11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒹ")) else fixturedef.get(bstack11ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᒺ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᒻ")) else None
        node = request.node if hasattr(request, bstack11ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᒼ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᒽ")) else None
        baseid = fixturedef.get(bstack11ll11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᒾ"), None) or bstack11ll11_opy_ (u"ࠧࠨᒿ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᓀ")):
            target = bstack1lll1lllll1_opy_.__1l111l11l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᓁ")) else None
            if target and not TestFramework.bstack11111111l1_opy_(target):
                self.__1l11l111l11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᓂ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠤࠥᓃ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᓄ") + str(target) + bstack11ll11_opy_ (u"ࠦࠧᓅ"))
            return None
        instance = TestFramework.bstack11111111l1_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᓆ") + str(target) + bstack11ll11_opy_ (u"ࠨࠢᓇ"))
            return None
        bstack1l111l1111l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1lll1lllll1_opy_.bstack1l111lll111_opy_, {})
        if os.getenv(bstack11ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᓈ"), bstack11ll11_opy_ (u"ࠣ࠳ࠥᓉ")) == bstack11ll11_opy_ (u"ࠤ࠴ࠦᓊ"):
            bstack1l111lll11l_opy_ = bstack11ll11_opy_ (u"ࠥ࠾ࠧᓋ").join((scope, fixturename))
            bstack1l11l1111l1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1111l1lll_opy_ = {
                bstack11ll11_opy_ (u"ࠦࡰ࡫ࡹࠣᓌ"): bstack1l111lll11l_opy_,
                bstack11ll11_opy_ (u"ࠧࡺࡡࡨࡵࠥᓍ"): bstack1lll1lllll1_opy_.__1l11l1l1111_opy_(request.node),
                bstack11ll11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᓎ"): fixturedef,
                bstack11ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᓏ"): scope,
                bstack11ll11_opy_ (u"ࠣࡶࡼࡴࡪࠨᓐ"): None,
            }
            try:
                if test_hook_state == bstack1ll1l1lll11_opy_.POST and callable(getattr(args[-1], bstack11ll11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᓑ"), None)):
                    bstack1l1111l1lll_opy_[bstack11ll11_opy_ (u"ࠥࡸࡾࡶࡥࠣᓒ")] = TestFramework.bstack1l1ll11l111_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1l1lll11_opy_.PRE:
                bstack1l1111l1lll_opy_[bstack11ll11_opy_ (u"ࠦࡺࡻࡩࡥࠤᓓ")] = uuid4().__str__()
                bstack1l1111l1lll_opy_[bstack1lll1lllll1_opy_.bstack1l1111ll11l_opy_] = bstack1l11l1111l1_opy_
            elif test_hook_state == bstack1ll1l1lll11_opy_.POST:
                bstack1l1111l1lll_opy_[bstack1lll1lllll1_opy_.bstack1l111lll1ll_opy_] = bstack1l11l1111l1_opy_
            if bstack1l111lll11l_opy_ in bstack1l111l1111l_opy_:
                bstack1l111l1111l_opy_[bstack1l111lll11l_opy_].update(bstack1l1111l1lll_opy_)
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᓔ") + str(bstack1l111l1111l_opy_[bstack1l111lll11l_opy_]) + bstack11ll11_opy_ (u"ࠨࠢᓕ"))
            else:
                bstack1l111l1111l_opy_[bstack1l111lll11l_opy_] = bstack1l1111l1lll_opy_
                self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᓖ") + str(len(bstack1l111l1111l_opy_)) + bstack11ll11_opy_ (u"ࠣࠤᓗ"))
        TestFramework.bstack1llllllllll_opy_(instance, bstack1lll1lllll1_opy_.bstack1l111lll111_opy_, bstack1l111l1111l_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᓘ") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠥࠦᓙ"))
        return instance
    def __1l11l111l11_opy_(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llllll1l1l_opy_.create_context(target)
        ob = bstack1llll111l11_opy_(ctx, self.bstack1ll11l11l1l_opy_, self.bstack1l111l111ll_opy_, test_framework_state)
        TestFramework.bstack1l1111lll11_opy_(ob, {
            TestFramework.bstack1ll11l11lll_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1l11ll_opy_: context.test_framework_version,
            TestFramework.bstack1l111lll1l1_opy_: [],
            bstack1lll1lllll1_opy_.bstack1l111lll111_opy_: {},
            bstack1lll1lllll1_opy_.bstack1l11111l111_opy_: {},
            bstack1lll1lllll1_opy_.bstack1l11l111ll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllllllll_opy_(ob, TestFramework.bstack1l11111l11l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllllllll_opy_(ob, TestFramework.bstack1ll1l11111l_opy_, context.platform_index)
        TestFramework.bstack1lllllll111_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᓚ") + str(TestFramework.bstack1lllllll111_opy_.keys()) + bstack11ll11_opy_ (u"ࠧࠨᓛ"))
        return ob
    def bstack1l1ll1l11l1_opy_(self, instance: bstack1llll111l11_opy_, bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_]):
        bstack1l111l1l11l_opy_ = (
            bstack1lll1lllll1_opy_.bstack1l1111llll1_opy_
            if bstack111111111l_opy_[1] == bstack1ll1l1lll11_opy_.PRE
            else bstack1lll1lllll1_opy_.bstack1l11111lll1_opy_
        )
        hook = bstack1lll1lllll1_opy_.bstack1l11l111lll_opy_(instance, bstack1l111l1l11l_opy_)
        entries = hook.get(TestFramework.bstack1l1111lllll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l111lll1l1_opy_, []))
        return entries
    def bstack1l1ll1l1l11_opy_(self, instance: bstack1llll111l11_opy_, bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_]):
        bstack1l111l1l11l_opy_ = (
            bstack1lll1lllll1_opy_.bstack1l1111llll1_opy_
            if bstack111111111l_opy_[1] == bstack1ll1l1lll11_opy_.PRE
            else bstack1lll1lllll1_opy_.bstack1l11111lll1_opy_
        )
        bstack1lll1lllll1_opy_.bstack1l1111lll1l_opy_(instance, bstack1l111l1l11l_opy_)
        TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l111lll1l1_opy_, []).clear()
    def bstack1l11l1l1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᓜ")
        global _1l1ll1lll11_opy_
        platform_index = os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᓝ")]
        bstack1l1ll111l11_opy_ = os.path.join(bstack1l1ll11ll1l_opy_, (bstack1l1lllllll1_opy_ + str(platform_index)), bstack1l1111111ll_opy_)
        if not os.path.exists(bstack1l1ll111l11_opy_) or not os.path.isdir(bstack1l1ll111l11_opy_):
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᓞ").format(bstack1l1ll111l11_opy_))
            return
        logs = hook.get(bstack11ll11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᓟ"), [])
        with os.scandir(bstack1l1ll111l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1lll11_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᓠ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll11_opy_ (u"ࠦࠧᓡ")
                    log_entry = bstack1lll11lll11_opy_(
                        kind=bstack11ll11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᓢ"),
                        message=bstack11ll11_opy_ (u"ࠨࠢᓣ"),
                        level=bstack11ll11_opy_ (u"ࠢࠣᓤ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll1ll1l_opy_=entry.stat().st_size,
                        bstack1l1ll1l1lll_opy_=bstack11ll11_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᓥ"),
                        bstack1llll11_opy_=os.path.abspath(entry.path),
                        bstack1l11l111l1l_opy_=hook.get(TestFramework.bstack1l111111ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1lll11_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᓦ")]
        bstack1l11l11lll1_opy_ = os.path.join(bstack1l1ll11ll1l_opy_, (bstack1l1lllllll1_opy_ + str(platform_index)), bstack1l1111111ll_opy_, bstack1l11111111l_opy_)
        if not os.path.exists(bstack1l11l11lll1_opy_) or not os.path.isdir(bstack1l11l11lll1_opy_):
            self.logger.info(bstack11ll11_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᓧ").format(bstack1l11l11lll1_opy_))
        else:
            self.logger.info(bstack11ll11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᓨ").format(bstack1l11l11lll1_opy_))
            with os.scandir(bstack1l11l11lll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1lll11_opy_:
                        self.logger.info(bstack11ll11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᓩ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll11_opy_ (u"ࠨࠢᓪ")
                        log_entry = bstack1lll11lll11_opy_(
                            kind=bstack11ll11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᓫ"),
                            message=bstack11ll11_opy_ (u"ࠣࠤᓬ"),
                            level=bstack11ll11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᓭ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll1ll1l_opy_=entry.stat().st_size,
                            bstack1l1ll1l1lll_opy_=bstack11ll11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᓮ"),
                            bstack1llll11_opy_=os.path.abspath(entry.path),
                            bstack1l1l1lllll1_opy_=hook.get(TestFramework.bstack1l111111ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1lll11_opy_.add(abs_path)
        hook[bstack11ll11_opy_ (u"ࠦࡱࡵࡧࡴࠤᓯ")] = logs
    def bstack1l1ll11l1ll_opy_(
        self,
        bstack1l1lll1l1l1_opy_: bstack1llll111l11_opy_,
        entries: List[bstack1lll11lll11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᓰ"))
        req.platform_index = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll1l11111l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11l11lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1ll1l11ll_opy_)
            log_entry.uuid = entry.bstack1l11l111l1l_opy_
            log_entry.test_framework_state = bstack1l1lll1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᓱ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll11_opy_ (u"ࠢࠣᓲ")
            if entry.kind == bstack11ll11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᓳ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1ll1l_opy_
                log_entry.file_path = entry.bstack1llll11_opy_
        def bstack1l1lll111l1_opy_():
            bstack1ll1lll1ll_opy_ = datetime.now()
            try:
                self.bstack1llll1l1l11_opy_.LogCreatedEvent(req)
                bstack1l1lll1l1l1_opy_.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᓴ"), datetime.now() - bstack1ll1lll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᓵ").format(str(e)))
                traceback.print_exc()
        self.bstack111111l1ll_opy_.enqueue(bstack1l1lll111l1_opy_)
    def __1l111l1l1ll_opy_(self, instance) -> None:
        bstack11ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᓶ")
        bstack1l111ll1lll_opy_ = {bstack11ll11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᓷ"): bstack1lll11ll1ll_opy_.bstack1l111llll11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l1111lll11_opy_(instance, bstack1l111ll1lll_opy_)
    @staticmethod
    def bstack1l11l111lll_opy_(instance: bstack1llll111l11_opy_, bstack1l111l1l11l_opy_: str):
        bstack1l111ll1l1l_opy_ = (
            bstack1lll1lllll1_opy_.bstack1l11111l111_opy_
            if bstack1l111l1l11l_opy_ == bstack1lll1lllll1_opy_.bstack1l11111lll1_opy_
            else bstack1lll1lllll1_opy_.bstack1l11l111ll1_opy_
        )
        bstack1l111llllll_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111l1l11l_opy_, None)
        bstack1l1111ll111_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111ll1l1l_opy_, None) if bstack1l111llllll_opy_ else None
        return (
            bstack1l1111ll111_opy_[bstack1l111llllll_opy_][-1]
            if isinstance(bstack1l1111ll111_opy_, dict) and len(bstack1l1111ll111_opy_.get(bstack1l111llllll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l1111lll1l_opy_(instance: bstack1llll111l11_opy_, bstack1l111l1l11l_opy_: str):
        hook = bstack1lll1lllll1_opy_.bstack1l11l111lll_opy_(instance, bstack1l111l1l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l1111lllll_opy_, []).clear()
    @staticmethod
    def __1l11111l1l1_opy_(instance: bstack1llll111l11_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll11_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᓸ"), None)):
            return
        if os.getenv(bstack11ll11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᓹ"), bstack11ll11_opy_ (u"ࠣ࠳ࠥᓺ")) != bstack11ll11_opy_ (u"ࠤ࠴ࠦᓻ"):
            bstack1lll1lllll1_opy_.logger.warning(bstack11ll11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᓼ"))
            return
        bstack1l11l1l1l11_opy_ = {
            bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᓽ"): (bstack1lll1lllll1_opy_.bstack1l1111llll1_opy_, bstack1lll1lllll1_opy_.bstack1l11l111ll1_opy_),
            bstack11ll11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᓾ"): (bstack1lll1lllll1_opy_.bstack1l11111lll1_opy_, bstack1lll1lllll1_opy_.bstack1l11111l111_opy_),
        }
        for when in (bstack11ll11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᓿ"), bstack11ll11_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᔀ"), bstack11ll11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᔁ")):
            bstack1l11l11ll11_opy_ = args[1].get_records(when)
            if not bstack1l11l11ll11_opy_:
                continue
            records = [
                bstack1lll11lll11_opy_(
                    kind=TestFramework.bstack1l1ll1111l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll11_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᔂ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll11_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᔃ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11l11ll11_opy_
                if isinstance(getattr(r, bstack11ll11_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᔄ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l111ll1ll1_opy_, bstack1l111ll1l1l_opy_ = bstack1l11l1l1l11_opy_.get(when, (None, None))
            bstack1l11l11l111_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111ll1ll1_opy_, None) if bstack1l111ll1ll1_opy_ else None
            bstack1l1111ll111_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, bstack1l111ll1l1l_opy_, None) if bstack1l11l11l111_opy_ else None
            if isinstance(bstack1l1111ll111_opy_, dict) and len(bstack1l1111ll111_opy_.get(bstack1l11l11l111_opy_, [])) > 0:
                hook = bstack1l1111ll111_opy_[bstack1l11l11l111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l1111lllll_opy_ in hook:
                    hook[TestFramework.bstack1l1111lllll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l111lll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1111ll1ll_opy_(test) -> Dict[str, Any]:
        bstack1lll111111_opy_ = bstack1lll1lllll1_opy_.__1l111l11l11_opy_(test.location) if hasattr(test, bstack11ll11_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᔅ")) else getattr(test, bstack11ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᔆ"), None)
        test_name = test.name if hasattr(test, bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᔇ")) else None
        bstack1l111111lll_opy_ = test.fspath.strpath if hasattr(test, bstack11ll11_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᔈ")) and test.fspath else None
        if not bstack1lll111111_opy_ or not test_name or not bstack1l111111lll_opy_:
            return None
        code = None
        if hasattr(test, bstack11ll11_opy_ (u"ࠤࡲࡦ࡯ࠨᔉ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1111111l1_opy_ = []
        try:
            bstack1l1111111l1_opy_ = bstack11l1ll11_opy_.bstack111ll111ll_opy_(test)
        except:
            bstack1lll1lllll1_opy_.logger.warning(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᔊ"))
        return {
            TestFramework.bstack1ll1l11ll11_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l1l1ll1_opy_: bstack1lll111111_opy_,
            TestFramework.bstack1ll1l111l1l_opy_: test_name,
            TestFramework.bstack1l1l1ll11ll_opy_: getattr(test, bstack11ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᔋ"), None),
            TestFramework.bstack1l111l11111_opy_: bstack1l111111lll_opy_,
            TestFramework.bstack1l111l1llll_opy_: bstack1lll1lllll1_opy_.__1l11l1l1111_opy_(test),
            TestFramework.bstack1l111l111l1_opy_: code,
            TestFramework.bstack1l1l11l11l1_opy_: TestFramework.bstack1l111111l1l_opy_,
            TestFramework.bstack1l11ll1l1ll_opy_: bstack1lll111111_opy_,
            TestFramework.bstack1l111111l11_opy_: bstack1l1111111l1_opy_
        }
    @staticmethod
    def __1l11l1l1111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11ll11_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᔌ"), [])
            markers.extend([getattr(m, bstack11ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᔍ"), None) for m in own_markers if getattr(m, bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᔎ"), None)])
            current = getattr(current, bstack11ll11_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᔏ"), None)
        return markers
    @staticmethod
    def __1l111l11l11_opy_(location):
        return bstack11ll11_opy_ (u"ࠤ࠽࠾ࠧᔐ").join(filter(lambda x: isinstance(x, str), location))