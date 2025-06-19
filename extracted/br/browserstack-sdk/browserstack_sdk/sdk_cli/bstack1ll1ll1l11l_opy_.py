# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllllll1l_opy_ import bstack11111l11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll111_opy_ import bstack1l111ll11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11lllll_opy_,
    bstack1lll1111l1l_opy_,
    bstack1lllll1111l_opy_,
    bstack1l11l1l1lll_opy_,
    bstack1lll11111l1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lll111l1_opy_
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack11111lll11_opy_ import bstack11111ll11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1ll1lll1_opy_ import bstack1ll1llll1ll_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack11l1ll111_opy_
bstack1l1ll1l11l1_opy_ = bstack1l1lll111l1_opy_()
bstack1l111lllll1_opy_ = 1.0
bstack1l1ll1l1111_opy_ = bstack111lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᑨ")
bstack1l11111llll_opy_ = bstack111lll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᑩ")
bstack1l1111l11ll_opy_ = bstack111lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᑪ")
bstack1l11111lll1_opy_ = bstack111lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᑫ")
bstack1l1111l1111_opy_ = bstack111lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᑬ")
_1l1llll1ll1_opy_ = set()
class bstack1lllll11l1l_opy_(TestFramework):
    bstack1l111llll11_opy_ = bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᑭ")
    bstack1l111l1l11l_opy_ = bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࠨᑮ")
    bstack1l111lll1ll_opy_ = bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᑯ")
    bstack1l11l1l1ll1_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࠧᑰ")
    bstack1l111l1l1l1_opy_ = bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᑱ")
    bstack1l111ll1lll_opy_: bool
    bstack11111lll11_opy_: bstack11111ll11l_opy_  = None
    bstack1lll1ll1l11_opy_ = None
    bstack1l11l11lll1_opy_ = [
        bstack1lll11lllll_opy_.BEFORE_ALL,
        bstack1lll11lllll_opy_.AFTER_ALL,
        bstack1lll11lllll_opy_.BEFORE_EACH,
        bstack1lll11lllll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l11l11_opy_: Dict[str, str],
        bstack1ll11l1ll1l_opy_: List[str]=[bstack111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᑲ")],
        bstack11111lll11_opy_: bstack11111ll11l_opy_=None,
        bstack1lll1ll1l11_opy_=None
    ):
        super().__init__(bstack1ll11l1ll1l_opy_, bstack1l111l11l11_opy_, bstack11111lll11_opy_)
        self.bstack1l111ll1lll_opy_ = any(bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᑳ") in item.lower() for item in bstack1ll11l1ll1l_opy_)
        self.bstack1lll1ll1l11_opy_ = bstack1lll1ll1l11_opy_
    def track_event(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11lllll_opy_.TEST or test_framework_state in bstack1lllll11l1l_opy_.bstack1l11l11lll1_opy_:
            bstack1l111ll11l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11lllll_opy_.NONE:
            self.logger.warning(bstack111lll_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫ࡤࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࠣᑴ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠣࠤᑵ"))
            return
        if not self.bstack1l111ll1lll_opy_:
            self.logger.warning(bstack111lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠿ࠥᑶ") + str(str(self.bstack1ll11l1ll1l_opy_)) + bstack111lll_opy_ (u"ࠥࠦᑷ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack111lll_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᑸ") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨᑹ"))
            return
        instance = self.__1l11l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡡࡳࡩࡶࡁࠧᑺ") + str(args) + bstack111lll_opy_ (u"ࠢࠣᑻ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lllll11l1l_opy_.bstack1l11l11lll1_opy_ and test_hook_state == bstack1lllll1111l_opy_.PRE:
                bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1lll111l11_opy_.value)
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack111lll_opy_ (u"ࠣ࠼ࠥᑼ")+str(test_framework_state.name)
                TestFramework.bstack1l111ll1111_opy_(instance, name, bstack1ll11llll11_opy_)
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᑽ").format(e))
        try:
            if not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l111l1llll_opy_) and test_hook_state == bstack1lllll1111l_opy_.PRE:
                test = bstack1lllll11l1l_opy_.__1l1111llll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack111lll_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᑾ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠦࠧᑿ"))
            if test_framework_state == bstack1lll11lllll_opy_.TEST:
                if test_hook_state == bstack1lllll1111l_opy_.PRE and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1llll11ll_opy_):
                    TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111lll_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᒀ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠨࠢᒁ"))
                elif test_hook_state == bstack1lllll1111l_opy_.POST and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11111l1l_opy_):
                    TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1ll11111l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack111lll_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᒂ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠣࠤᒃ"))
            elif test_framework_state == bstack1lll11lllll_opy_.LOG and test_hook_state == bstack1lllll1111l_opy_.POST:
                bstack1lllll11l1l_opy_.__1l11l11l111_opy_(instance, *args)
            elif test_framework_state == bstack1lll11lllll_opy_.LOG_REPORT and test_hook_state == bstack1lllll1111l_opy_.POST:
                self.__1l11l1llll1_opy_(instance, *args)
                self.__1l11l11llll_opy_(instance)
            elif test_framework_state in bstack1lllll11l1l_opy_.bstack1l11l11lll1_opy_:
                self.__1l11l11ll11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᒄ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠥࠦᒅ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l1ll11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lllll11l1l_opy_.bstack1l11l11lll1_opy_ and test_hook_state == bstack1lllll1111l_opy_.POST:
                name = str(EVENTS.bstack1lll111l11_opy_.name)+bstack111lll_opy_ (u"ࠦ࠿ࠨᒆ")+str(test_framework_state.name)
                bstack1ll11llll11_opy_ = TestFramework.bstack1l111ll111l_opy_(instance, name)
                bstack1llll1l1l11_opy_.end(EVENTS.bstack1lll111l11_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᒇ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᒈ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᒉ").format(e))
    def bstack1l1llll1l1l_opy_(self):
        return self.bstack1l111ll1lll_opy_
    def __1l111l1l1ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack111lll_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᒊ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll1111l1l1_opy_(rep, [bstack111lll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᒋ"), bstack111lll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᒌ"), bstack111lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᒍ"), bstack111lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᒎ"), bstack111lll_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᒏ"), bstack111lll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᒐ")])
        return None
    def __1l11l1llll1_opy_(self, instance: bstack1lll1111l1l_opy_, *args):
        result = self.__1l111l1l1ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111lllll_opy_ = None
        if result.get(bstack111lll_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᒑ"), None) == bstack111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᒒ") and len(args) > 1 and getattr(args[1], bstack111lll_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦᒓ"), None) is not None:
            failure = [{bstack111lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᒔ"): [args[1].excinfo.exconly(), result.get(bstack111lll_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᒕ"), None)]}]
            bstack11111lllll_opy_ = bstack111lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᒖ") if bstack111lll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᒗ") in getattr(args[1].excinfo, bstack111lll_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᒘ"), bstack111lll_opy_ (u"ࠤࠥᒙ")) else bstack111lll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᒚ")
        bstack1l11l1l1l11_opy_ = result.get(bstack111lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᒛ"), TestFramework.bstack1l11ll11111_opy_)
        if bstack1l11l1l1l11_opy_ != TestFramework.bstack1l11ll11111_opy_:
            TestFramework.bstack11111ll111_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l111l11_opy_(instance, {
            TestFramework.bstack1l1l11ll1ll_opy_: failure,
            TestFramework.bstack1l111l11111_opy_: bstack11111lllll_opy_,
            TestFramework.bstack1l1l1l1l1l1_opy_: bstack1l11l1l1l11_opy_,
        })
    def __1l11l1lllll_opy_(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11lllll_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1lll1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll1111l_opy_ bstack1l11l111l1l_opy_ this to be bstack111lll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᒜ")
            if test_framework_state == bstack1lll11lllll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l111ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11lllll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack111lll_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᒝ"), None), bstack111lll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᒞ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack111lll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒟ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111l11l1_opy_(target) if target else None
        return instance
    def __1l11l11ll11_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l11l1l1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1lllll11l1l_opy_.bstack1l111l1l11l_opy_, {})
        if not key in bstack1l11l11l1l1_opy_:
            bstack1l11l11l1l1_opy_[key] = []
        bstack1l11ll111ll_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1lllll11l1l_opy_.bstack1l111lll1ll_opy_, {})
        if not key in bstack1l11ll111ll_opy_:
            bstack1l11ll111ll_opy_[key] = []
        bstack1l1111ll111_opy_ = {
            bstack1lllll11l1l_opy_.bstack1l111l1l11l_opy_: bstack1l11l11l1l1_opy_,
            bstack1lllll11l1l_opy_.bstack1l111lll1ll_opy_: bstack1l11ll111ll_opy_,
        }
        if test_hook_state == bstack1lllll1111l_opy_.PRE:
            hook = {
                bstack111lll_opy_ (u"ࠤ࡮ࡩࡾࠨᒠ"): key,
                TestFramework.bstack1l11l1111l1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l1l_opy_: TestFramework.bstack1l11l11l1ll_opy_,
                TestFramework.bstack1l111l11ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l111ll1ll1_opy_: [],
                TestFramework.bstack1l11l1l1l1l_opy_: args[1] if len(args) > 1 else bstack111lll_opy_ (u"ࠪࠫᒡ"),
                TestFramework.bstack1l11l1111ll_opy_: bstack1ll1llll1ll_opy_.bstack1l111llll1l_opy_()
            }
            bstack1l11l11l1l1_opy_[key].append(hook)
            bstack1l1111ll111_opy_[bstack1lllll11l1l_opy_.bstack1l11l1l1ll1_opy_] = key
        elif test_hook_state == bstack1lllll1111l_opy_.POST:
            bstack1l11ll11l11_opy_ = bstack1l11l11l1l1_opy_.get(key, [])
            hook = bstack1l11ll11l11_opy_.pop() if bstack1l11ll11l11_opy_ else None
            if hook:
                result = self.__1l111l1l1ll_opy_(*args)
                if result:
                    bstack1l11l1l11ll_opy_ = result.get(bstack111lll_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᒢ"), TestFramework.bstack1l11l11l1ll_opy_)
                    if bstack1l11l1l11ll_opy_ != TestFramework.bstack1l11l11l1ll_opy_:
                        hook[TestFramework.bstack1l11ll11l1l_opy_] = bstack1l11l1l11ll_opy_
                hook[TestFramework.bstack1l111l111l1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11l1111ll_opy_]= bstack1ll1llll1ll_opy_.bstack1l111llll1l_opy_()
                self.bstack1l111lll11l_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l111111_opy_, [])
                if logs: self.bstack1l1lllll111_opy_(instance, logs)
                bstack1l11ll111ll_opy_[key].append(hook)
                bstack1l1111ll111_opy_[bstack1lllll11l1l_opy_.bstack1l111l1l1l1_opy_] = key
        TestFramework.bstack1l11l111l11_opy_(instance, bstack1l1111ll111_opy_)
        self.logger.debug(bstack111lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦᒣ") + str(bstack1l11ll111ll_opy_) + bstack111lll_opy_ (u"ࠨࠢᒤ"))
    def __1l11l1lll1l_opy_(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll1111l1l1_opy_(args[0], [bstack111lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᒥ"), bstack111lll_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᒦ"), bstack111lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᒧ"), bstack111lll_opy_ (u"ࠥ࡭ࡩࡹࠢᒨ"), bstack111lll_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᒩ"), bstack111lll_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᒪ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack111lll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒫ")) else fixturedef.get(bstack111lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᒬ"), None)
        fixturename = request.fixturename if hasattr(request, bstack111lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᒭ")) else None
        node = request.node if hasattr(request, bstack111lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᒮ")) else None
        target = request.node.nodeid if hasattr(node, bstack111lll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᒯ")) else None
        baseid = fixturedef.get(bstack111lll_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᒰ"), None) or bstack111lll_opy_ (u"ࠧࠨᒱ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack111lll_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᒲ")):
            target = bstack1lllll11l1l_opy_.__1l11l11l11l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack111lll_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᒳ")) else None
            if target and not TestFramework.bstack11111l11l1_opy_(target):
                self.__1l11l111ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack111lll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᒴ") + str(test_hook_state) + bstack111lll_opy_ (u"ࠤࠥᒵ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack111lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᒶ") + str(target) + bstack111lll_opy_ (u"ࠦࠧᒷ"))
            return None
        instance = TestFramework.bstack11111l11l1_opy_(target)
        if not instance:
            self.logger.warning(bstack111lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᒸ") + str(target) + bstack111lll_opy_ (u"ࠨࠢᒹ"))
            return None
        bstack1l1111ll1l1_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1lllll11l1l_opy_.bstack1l111llll11_opy_, {})
        if os.getenv(bstack111lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓࠣᒺ"), bstack111lll_opy_ (u"ࠣ࠳ࠥᒻ")) == bstack111lll_opy_ (u"ࠤ࠴ࠦᒼ"):
            bstack1l11l1ll1l1_opy_ = bstack111lll_opy_ (u"ࠥ࠾ࠧᒽ").join((scope, fixturename))
            bstack1l1111l1lll_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l1l1111_opy_ = {
                bstack111lll_opy_ (u"ࠦࡰ࡫ࡹࠣᒾ"): bstack1l11l1ll1l1_opy_,
                bstack111lll_opy_ (u"ࠧࡺࡡࡨࡵࠥᒿ"): bstack1lllll11l1l_opy_.__1l111lll111_opy_(request.node),
                bstack111lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢᓀ"): fixturedef,
                bstack111lll_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᓁ"): scope,
                bstack111lll_opy_ (u"ࠣࡶࡼࡴࡪࠨᓂ"): None,
            }
            try:
                if test_hook_state == bstack1lllll1111l_opy_.POST and callable(getattr(args[-1], bstack111lll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᓃ"), None)):
                    bstack1l11l1l1111_opy_[bstack111lll_opy_ (u"ࠥࡸࡾࡶࡥࠣᓄ")] = TestFramework.bstack1ll1111ll11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lllll1111l_opy_.PRE:
                bstack1l11l1l1111_opy_[bstack111lll_opy_ (u"ࠦࡺࡻࡩࡥࠤᓅ")] = uuid4().__str__()
                bstack1l11l1l1111_opy_[bstack1lllll11l1l_opy_.bstack1l111l11ll1_opy_] = bstack1l1111l1lll_opy_
            elif test_hook_state == bstack1lllll1111l_opy_.POST:
                bstack1l11l1l1111_opy_[bstack1lllll11l1l_opy_.bstack1l111l111l1_opy_] = bstack1l1111l1lll_opy_
            if bstack1l11l1ll1l1_opy_ in bstack1l1111ll1l1_opy_:
                bstack1l1111ll1l1_opy_[bstack1l11l1ll1l1_opy_].update(bstack1l11l1l1111_opy_)
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᓆ") + str(bstack1l1111ll1l1_opy_[bstack1l11l1ll1l1_opy_]) + bstack111lll_opy_ (u"ࠨࠢᓇ"))
            else:
                bstack1l1111ll1l1_opy_[bstack1l11l1ll1l1_opy_] = bstack1l11l1l1111_opy_
                self.logger.debug(bstack111lll_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᓈ") + str(len(bstack1l1111ll1l1_opy_)) + bstack111lll_opy_ (u"ࠣࠤᓉ"))
        TestFramework.bstack11111ll111_opy_(instance, bstack1lllll11l1l_opy_.bstack1l111llll11_opy_, bstack1l1111ll1l1_opy_)
        self.logger.debug(bstack111lll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᓊ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠥࠦᓋ"))
        return instance
    def __1l11l111ll1_opy_(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack11111l11ll_opy_.create_context(target)
        ob = bstack1lll1111l1l_opy_(ctx, self.bstack1ll11l1ll1l_opy_, self.bstack1l111l11l11_opy_, test_framework_state)
        TestFramework.bstack1l11l111l11_opy_(ob, {
            TestFramework.bstack1ll11ll11ll_opy_: context.test_framework_name,
            TestFramework.bstack1l1lll1l1ll_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1l11l1_opy_: [],
            bstack1lllll11l1l_opy_.bstack1l111llll11_opy_: {},
            bstack1lllll11l1l_opy_.bstack1l111lll1ll_opy_: {},
            bstack1lllll11l1l_opy_.bstack1l111l1l11l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11111ll111_opy_(ob, TestFramework.bstack1l11l111lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11111ll111_opy_(ob, TestFramework.bstack1ll1l11ll1l_opy_, context.platform_index)
        TestFramework.bstack1lllll1ll11_opy_[ctx.id] = ob
        self.logger.debug(bstack111lll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᓌ") + str(TestFramework.bstack1lllll1ll11_opy_.keys()) + bstack111lll_opy_ (u"ࠧࠨᓍ"))
        return ob
    def bstack1l1lll1ll1l_opy_(self, instance: bstack1lll1111l1l_opy_, bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_]):
        bstack1l111l1lll1_opy_ = (
            bstack1lllll11l1l_opy_.bstack1l11l1l1ll1_opy_
            if bstack11111l1l11_opy_[1] == bstack1lllll1111l_opy_.PRE
            else bstack1lllll11l1l_opy_.bstack1l111l1l1l1_opy_
        )
        hook = bstack1lllll11l1l_opy_.bstack1l1111l1l11_opy_(instance, bstack1l111l1lll1_opy_)
        entries = hook.get(TestFramework.bstack1l111ll1ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, []))
        return entries
    def bstack1l1lllll1ll_opy_(self, instance: bstack1lll1111l1l_opy_, bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_]):
        bstack1l111l1lll1_opy_ = (
            bstack1lllll11l1l_opy_.bstack1l11l1l1ll1_opy_
            if bstack11111l1l11_opy_[1] == bstack1lllll1111l_opy_.PRE
            else bstack1lllll11l1l_opy_.bstack1l111l1l1l1_opy_
        )
        bstack1lllll11l1l_opy_.bstack1l111l111ll_opy_(instance, bstack1l111l1lll1_opy_)
        TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, []).clear()
    def bstack1l111lll11l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᓎ")
        global _1l1llll1ll1_opy_
        platform_index = os.environ[bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᓏ")]
        bstack1l1lll11ll1_opy_ = os.path.join(bstack1l1ll1l11l1_opy_, (bstack1l1ll1l1111_opy_ + str(platform_index)), bstack1l11111lll1_opy_)
        if not os.path.exists(bstack1l1lll11ll1_opy_) or not os.path.isdir(bstack1l1lll11ll1_opy_):
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᓐ").format(bstack1l1lll11ll1_opy_))
            return
        logs = hook.get(bstack111lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᓑ"), [])
        with os.scandir(bstack1l1lll11ll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1llll1ll1_opy_:
                    self.logger.info(bstack111lll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᓒ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack111lll_opy_ (u"ࠦࠧᓓ")
                    log_entry = bstack1lll11111l1_opy_(
                        kind=bstack111lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᓔ"),
                        message=bstack111lll_opy_ (u"ࠨࠢᓕ"),
                        level=bstack111lll_opy_ (u"ࠢࠣᓖ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll1ll1ll_opy_=entry.stat().st_size,
                        bstack1l1lll1llll_opy_=bstack111lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᓗ"),
                        bstack11ll1_opy_=os.path.abspath(entry.path),
                        bstack1l111l1ll1l_opy_=hook.get(TestFramework.bstack1l11l1111l1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1llll1ll1_opy_.add(abs_path)
        platform_index = os.environ[bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᓘ")]
        bstack1l111llllll_opy_ = os.path.join(bstack1l1ll1l11l1_opy_, (bstack1l1ll1l1111_opy_ + str(platform_index)), bstack1l11111lll1_opy_, bstack1l1111l1111_opy_)
        if not os.path.exists(bstack1l111llllll_opy_) or not os.path.isdir(bstack1l111llllll_opy_):
            self.logger.info(bstack111lll_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᓙ").format(bstack1l111llllll_opy_))
        else:
            self.logger.info(bstack111lll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᓚ").format(bstack1l111llllll_opy_))
            with os.scandir(bstack1l111llllll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1llll1ll1_opy_:
                        self.logger.info(bstack111lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᓛ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack111lll_opy_ (u"ࠨࠢᓜ")
                        log_entry = bstack1lll11111l1_opy_(
                            kind=bstack111lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᓝ"),
                            message=bstack111lll_opy_ (u"ࠣࠤᓞ"),
                            level=bstack111lll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᓟ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll1ll1ll_opy_=entry.stat().st_size,
                            bstack1l1lll1llll_opy_=bstack111lll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᓠ"),
                            bstack11ll1_opy_=os.path.abspath(entry.path),
                            bstack1ll11111l11_opy_=hook.get(TestFramework.bstack1l11l1111l1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1llll1ll1_opy_.add(abs_path)
        hook[bstack111lll_opy_ (u"ࠦࡱࡵࡧࡴࠤᓡ")] = logs
    def bstack1l1lllll111_opy_(
        self,
        bstack1l1lllll1l1_opy_: bstack1lll1111l1l_opy_,
        entries: List[bstack1lll11111l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack111lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᓢ"))
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll1l11ll1l_opy_)
        req.execution_context.hash = str(bstack1l1lllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll11ll11ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1l1lll1l1ll_opy_)
            log_entry.uuid = entry.bstack1l111l1ll1l_opy_
            log_entry.test_framework_state = bstack1l1lllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack111lll_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᓣ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack111lll_opy_ (u"ࠢࠣᓤ")
            if entry.kind == bstack111lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᓥ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1ll_opy_
                log_entry.file_path = entry.bstack11ll1_opy_
        def bstack1ll1111111l_opy_():
            bstack11ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.LogCreatedEvent(req)
                bstack1l1lllll1l1_opy_.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᓦ"), datetime.now() - bstack11ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᓧ").format(str(e)))
                traceback.print_exc()
        self.bstack11111lll11_opy_.enqueue(bstack1ll1111111l_opy_)
    def __1l11l11llll_opy_(self, instance) -> None:
        bstack111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᓨ")
        bstack1l1111ll111_opy_ = {bstack111lll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᓩ"): bstack1ll1llll1ll_opy_.bstack1l111llll1l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l111l11_opy_(instance, bstack1l1111ll111_opy_)
    @staticmethod
    def bstack1l1111l1l11_opy_(instance: bstack1lll1111l1l_opy_, bstack1l111l1lll1_opy_: str):
        bstack1l1111lllll_opy_ = (
            bstack1lllll11l1l_opy_.bstack1l111lll1ll_opy_
            if bstack1l111l1lll1_opy_ == bstack1lllll11l1l_opy_.bstack1l111l1l1l1_opy_
            else bstack1lllll11l1l_opy_.bstack1l111l1l11l_opy_
        )
        bstack1l11l1ll11l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l111l1lll1_opy_, None)
        bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l1111lllll_opy_, None) if bstack1l11l1ll11l_opy_ else None
        return (
            bstack1l111ll1l11_opy_[bstack1l11l1ll11l_opy_][-1]
            if isinstance(bstack1l111ll1l11_opy_, dict) and len(bstack1l111ll1l11_opy_.get(bstack1l11l1ll11l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l111ll_opy_(instance: bstack1lll1111l1l_opy_, bstack1l111l1lll1_opy_: str):
        hook = bstack1lllll11l1l_opy_.bstack1l1111l1l11_opy_(instance, bstack1l111l1lll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l111ll1ll1_opy_, []).clear()
    @staticmethod
    def __1l11l11l111_opy_(instance: bstack1lll1111l1l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack111lll_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᓪ"), None)):
            return
        if os.getenv(bstack111lll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᓫ"), bstack111lll_opy_ (u"ࠣ࠳ࠥᓬ")) != bstack111lll_opy_ (u"ࠤ࠴ࠦᓭ"):
            bstack1lllll11l1l_opy_.logger.warning(bstack111lll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᓮ"))
            return
        bstack1l1111ll11l_opy_ = {
            bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᓯ"): (bstack1lllll11l1l_opy_.bstack1l11l1l1ll1_opy_, bstack1lllll11l1l_opy_.bstack1l111l1l11l_opy_),
            bstack111lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᓰ"): (bstack1lllll11l1l_opy_.bstack1l111l1l1l1_opy_, bstack1lllll11l1l_opy_.bstack1l111lll1ll_opy_),
        }
        for when in (bstack111lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᓱ"), bstack111lll_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᓲ"), bstack111lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᓳ")):
            bstack1l11ll111l1_opy_ = args[1].get_records(when)
            if not bstack1l11ll111l1_opy_:
                continue
            records = [
                bstack1lll11111l1_opy_(
                    kind=TestFramework.bstack1l1lll1111l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack111lll_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᓴ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack111lll_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᓵ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll111l1_opy_
                if isinstance(getattr(r, bstack111lll_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᓶ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l11111l_opy_, bstack1l1111lllll_opy_ = bstack1l1111ll11l_opy_.get(when, (None, None))
            bstack1l1111l1l1l_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l11l11111l_opy_, None) if bstack1l11l11111l_opy_ else None
            bstack1l111ll1l11_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, bstack1l1111lllll_opy_, None) if bstack1l1111l1l1l_opy_ else None
            if isinstance(bstack1l111ll1l11_opy_, dict) and len(bstack1l111ll1l11_opy_.get(bstack1l1111l1l1l_opy_, [])) > 0:
                hook = bstack1l111ll1l11_opy_[bstack1l1111l1l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l111ll1ll1_opy_ in hook:
                    hook[TestFramework.bstack1l111ll1ll1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1111llll1_opy_(test) -> Dict[str, Any]:
        bstack11lll1111l_opy_ = bstack1lllll11l1l_opy_.__1l11l11l11l_opy_(test.location) if hasattr(test, bstack111lll_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᓷ")) else getattr(test, bstack111lll_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᓸ"), None)
        test_name = test.name if hasattr(test, bstack111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᓹ")) else None
        bstack1l111l1111l_opy_ = test.fspath.strpath if hasattr(test, bstack111lll_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᓺ")) and test.fspath else None
        if not bstack11lll1111l_opy_ or not test_name or not bstack1l111l1111l_opy_:
            return None
        code = None
        if hasattr(test, bstack111lll_opy_ (u"ࠤࡲࡦ࡯ࠨᓻ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l1111l11l1_opy_ = []
        try:
            bstack1l1111l11l1_opy_ = bstack11l1ll111_opy_.bstack1111lllll1_opy_(test)
        except:
            bstack1lllll11l1l_opy_.logger.warning(bstack111lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᓼ"))
        return {
            TestFramework.bstack1ll11lll11l_opy_: uuid4().__str__(),
            TestFramework.bstack1l111l1llll_opy_: bstack11lll1111l_opy_,
            TestFramework.bstack1ll11l1l1ll_opy_: test_name,
            TestFramework.bstack1l1ll111ll1_opy_: getattr(test, bstack111lll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᓽ"), None),
            TestFramework.bstack1l111l11lll_opy_: bstack1l111l1111l_opy_,
            TestFramework.bstack1l111ll11ll_opy_: bstack1lllll11l1l_opy_.__1l111lll111_opy_(test),
            TestFramework.bstack1l1111lll1l_opy_: code,
            TestFramework.bstack1l1l1l1l1l1_opy_: TestFramework.bstack1l11ll11111_opy_,
            TestFramework.bstack1l11lllll11_opy_: bstack11lll1111l_opy_,
            TestFramework.bstack1l1111l111l_opy_: bstack1l1111l11l1_opy_
        }
    @staticmethod
    def __1l111lll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack111lll_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᓾ"), [])
            markers.extend([getattr(m, bstack111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᓿ"), None) for m in own_markers if getattr(m, bstack111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᔀ"), None)])
            current = getattr(current, bstack111lll_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᔁ"), None)
        return markers
    @staticmethod
    def __1l11l11l11l_opy_(location):
        return bstack111lll_opy_ (u"ࠤ࠽࠾ࠧᔂ").join(filter(lambda x: isinstance(x, str), location))