# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll111ll11_opy_ import bstack1l111l1l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll11l11_opy_,
    bstack1lll1l1l1l1_opy_,
    bstack1lll1lll111_opy_,
    bstack1l1111l1l1l_opy_,
    bstack1lll111l1l1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1llllll_opy_
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1ll11_opy_ import bstack1lll11l1lll_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack11l1l1l1ll_opy_
bstack1l1lll11l1l_opy_ = bstack1l1l1llllll_opy_()
bstack1l1111lllll_opy_ = 1.0
bstack1l1llllll1l_opy_ = bstack1l1l1l1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᑷ")
bstack1l111111111_opy_ = bstack1l1l1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᑸ")
bstack1l1111111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᑹ")
bstack1l111111l11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᑺ")
bstack11lllllllll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᑻ")
_1l1lll111l1_opy_ = set()
class bstack1lll1llll11_opy_(TestFramework):
    bstack1l11l1l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᑼ")
    bstack1l11l11lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᑽ")
    bstack1l11111lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᑾ")
    bstack1l111lll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᑿ")
    bstack1l11l1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᒀ")
    bstack1l111llll1l_opy_: bool
    bstack111111lll1_opy_: bstack111111l1l1_opy_  = None
    bstack1ll1ll111l1_opy_ = None
    bstack1l1111llll1_opy_ = [
        bstack1ll1ll11l11_opy_.BEFORE_ALL,
        bstack1ll1ll11l11_opy_.AFTER_ALL,
        bstack1ll1ll11l11_opy_.BEFORE_EACH,
        bstack1ll1ll11l11_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l11111l_opy_: Dict[str, str],
        bstack1ll1l111ll1_opy_: List[str]=[bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᒁ")],
        bstack111111lll1_opy_: bstack111111l1l1_opy_=None,
        bstack1ll1ll111l1_opy_=None
    ):
        super().__init__(bstack1ll1l111ll1_opy_, bstack1l11l11111l_opy_, bstack111111lll1_opy_)
        self.bstack1l111llll1l_opy_ = any(bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᒂ") in item.lower() for item in bstack1ll1l111ll1_opy_)
        self.bstack1ll1ll111l1_opy_ = bstack1ll1ll111l1_opy_
    def track_event(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll11l11_opy_.TEST or test_framework_state in bstack1lll1llll11_opy_.bstack1l1111llll1_opy_:
            bstack1l111l1l11l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll11l11_opy_.NONE:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᒃ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠤࠥᒄ"))
            return
        if not self.bstack1l111llll1l_opy_:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᒅ") + str(str(self.bstack1ll1l111ll1_opy_)) + bstack1l1l1l1_opy_ (u"ࠦࠧᒆ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᒇ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢᒈ"))
            return
        instance = self.__1l111l1llll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᒉ") + str(args) + bstack1l1l1l1_opy_ (u"ࠣࠤᒊ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1llll11_opy_.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll1lll111_opy_.PRE:
                bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1l11lll111_opy_.value)
                name = str(EVENTS.bstack1l11lll111_opy_.name)+bstack1l1l1l1_opy_ (u"ࠤ࠽ࠦᒋ")+str(test_framework_state.name)
                TestFramework.bstack1l11l111l1l_opy_(instance, name, bstack1ll111ll1l1_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᒌ").format(e))
        try:
            if not TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l11l111l11_opy_) and test_hook_state == bstack1lll1lll111_opy_.PRE:
                test = bstack1lll1llll11_opy_.__1l11l111111_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᒍ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠧࠨᒎ"))
            if test_framework_state == bstack1ll1ll11l11_opy_.TEST:
                if test_hook_state == bstack1lll1lll111_opy_.PRE and not TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_):
                    TestFramework.bstack1lllll1111l_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᒏ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠢࠣᒐ"))
                elif test_hook_state == bstack1lll1lll111_opy_.POST and not TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1lll1l111_opy_):
                    TestFramework.bstack1lllll1111l_opy_(instance, TestFramework.bstack1l1lll1l111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᒑ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠤࠥᒒ"))
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG and test_hook_state == bstack1lll1lll111_opy_.POST:
                bstack1lll1llll11_opy_.__1l111ll1l11_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG_REPORT and test_hook_state == bstack1lll1lll111_opy_.POST:
                self.__1l1111ll11l_opy_(instance, *args)
                self.__1l111llllll_opy_(instance)
            elif test_framework_state in bstack1lll1llll11_opy_.bstack1l1111llll1_opy_:
                self.__1l111111l1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᒓ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠦࠧᒔ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111l11l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1llll11_opy_.bstack1l1111llll1_opy_ and test_hook_state == bstack1lll1lll111_opy_.POST:
                name = str(EVENTS.bstack1l11lll111_opy_.name)+bstack1l1l1l1_opy_ (u"ࠧࡀࠢᒕ")+str(test_framework_state.name)
                bstack1ll111ll1l1_opy_ = TestFramework.bstack1l111l1l1ll_opy_(instance, name)
                bstack1lll1ll11l1_opy_.end(EVENTS.bstack1l11lll111_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᒖ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᒗ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᒘ").format(e))
    def bstack1l1ll1l1l11_opy_(self):
        return self.bstack1l111llll1l_opy_
    def __1l11l1111ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᒙ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll1ll1ll_opy_(rep, [bstack1l1l1l1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᒚ"), bstack1l1l1l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᒛ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᒜ"), bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᒝ"), bstack1l1l1l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᒞ"), bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᒟ")])
        return None
    def __1l1111ll11l_opy_(self, instance: bstack1lll1l1l1l1_opy_, *args):
        result = self.__1l11l1111ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack11111l11ll_opy_ = None
        if result.get(bstack1l1l1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᒠ"), None) == bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᒡ") and len(args) > 1 and getattr(args[1], bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᒢ"), None) is not None:
            failure = [{bstack1l1l1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᒣ"): [args[1].excinfo.exconly(), result.get(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᒤ"), None)]}]
            bstack11111l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᒥ") if bstack1l1l1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᒦ") in getattr(args[1].excinfo, bstack1l1l1l1_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᒧ"), bstack1l1l1l1_opy_ (u"ࠥࠦᒨ")) else bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᒩ")
        bstack1l11111l11l_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᒪ"), TestFramework.bstack1l11l11ll1l_opy_)
        if bstack1l11111l11l_opy_ != TestFramework.bstack1l11l11ll1l_opy_:
            TestFramework.bstack1lllll1111l_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11111ll1l_opy_(instance, {
            TestFramework.bstack1l1l111l1l1_opy_: failure,
            TestFramework.bstack1l111lllll1_opy_: bstack11111l11ll_opy_,
            TestFramework.bstack1l1l111ll11_opy_: bstack1l11111l11l_opy_,
        })
    def __1l111l1llll_opy_(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll11l11_opy_.SETUP_FIXTURE:
            instance = self.__1l1111l1111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111l1111l_opy_ bstack1l111ll111l_opy_ this to be bstack1l1l1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒫ")
            if test_framework_state == bstack1ll1ll11l11_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l111ll1111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᒬ"), None), bstack1l1l1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒭ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1l1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᒮ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llllllllll_opy_(target) if target else None
        return instance
    def __1l111111l1l_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11l111ll1_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1lll1llll11_opy_.bstack1l11l11lll1_opy_, {})
        if not key in bstack1l11l111ll1_opy_:
            bstack1l11l111ll1_opy_[key] = []
        bstack1l1111lll11_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1lll1llll11_opy_.bstack1l11111lll1_opy_, {})
        if not key in bstack1l1111lll11_opy_:
            bstack1l1111lll11_opy_[key] = []
        bstack1l11l1l1l1l_opy_ = {
            bstack1lll1llll11_opy_.bstack1l11l11lll1_opy_: bstack1l11l111ll1_opy_,
            bstack1lll1llll11_opy_.bstack1l11111lll1_opy_: bstack1l1111lll11_opy_,
        }
        if test_hook_state == bstack1lll1lll111_opy_.PRE:
            hook = {
                bstack1l1l1l1_opy_ (u"ࠥ࡯ࡪࡿࠢᒯ"): key,
                TestFramework.bstack1l11l11l1ll_opy_: uuid4().__str__(),
                TestFramework.bstack1l111l1l111_opy_: TestFramework.bstack1l111l1ll11_opy_,
                TestFramework.bstack1l1111ll1l1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11111ll11_opy_: [],
                TestFramework.bstack1l11l1111l1_opy_: args[1] if len(args) > 1 else bstack1l1l1l1_opy_ (u"ࠫࠬᒰ"),
                TestFramework.bstack1l111ll1lll_opy_: bstack1lll11l1lll_opy_.bstack1l11111l1ll_opy_()
            }
            bstack1l11l111ll1_opy_[key].append(hook)
            bstack1l11l1l1l1l_opy_[bstack1lll1llll11_opy_.bstack1l111lll1ll_opy_] = key
        elif test_hook_state == bstack1lll1lll111_opy_.POST:
            bstack1l1111l11ll_opy_ = bstack1l11l111ll1_opy_.get(key, [])
            hook = bstack1l1111l11ll_opy_.pop() if bstack1l1111l11ll_opy_ else None
            if hook:
                result = self.__1l11l1111ll_opy_(*args)
                if result:
                    bstack1l1111ll1ll_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᒱ"), TestFramework.bstack1l111l1ll11_opy_)
                    if bstack1l1111ll1ll_opy_ != TestFramework.bstack1l111l1ll11_opy_:
                        hook[TestFramework.bstack1l111l1l111_opy_] = bstack1l1111ll1ll_opy_
                hook[TestFramework.bstack1l1111l111l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111ll1lll_opy_]= bstack1lll11l1lll_opy_.bstack1l11111l1ll_opy_()
                self.bstack1l111l11ll1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l1111lll1l_opy_, [])
                if logs: self.bstack1l1lll11111_opy_(instance, logs)
                bstack1l1111lll11_opy_[key].append(hook)
                bstack1l11l1l1l1l_opy_[bstack1lll1llll11_opy_.bstack1l11l1l1ll1_opy_] = key
        TestFramework.bstack1l11111ll1l_opy_(instance, bstack1l11l1l1l1l_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᒲ") + str(bstack1l1111lll11_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣᒳ"))
    def __1l1111l1111_opy_(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll1ll1ll_opy_(args[0], [bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᒴ"), bstack1l1l1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᒵ"), bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᒶ"), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡪࡳࠣᒷ"), bstack1l1l1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᒸ"), bstack1l1l1l1_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᒹ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1l1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᒺ")) else fixturedef.get(bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᒻ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1l1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᒼ")) else None
        node = request.node if hasattr(request, bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣᒽ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1l1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᒾ")) else None
        baseid = fixturedef.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᒿ"), None) or bstack1l1l1l1_opy_ (u"ࠨࠢᓀ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1l1l1_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᓁ")):
            target = bstack1lll1llll11_opy_.__1l111llll11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᓂ")) else None
            if target and not TestFramework.bstack1llllllllll_opy_(target):
                self.__1l111ll1111_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᓃ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠥࠦᓄ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᓅ") + str(target) + bstack1l1l1l1_opy_ (u"ࠧࠨᓆ"))
            return None
        instance = TestFramework.bstack1llllllllll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᓇ") + str(target) + bstack1l1l1l1_opy_ (u"ࠢࠣᓈ"))
            return None
        bstack1l111l111ll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1lll1llll11_opy_.bstack1l11l1l111l_opy_, {})
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᓉ"), bstack1l1l1l1_opy_ (u"ࠤ࠴ࠦᓊ")) == bstack1l1l1l1_opy_ (u"ࠥ࠵ࠧᓋ"):
            bstack1l111l1ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࠿ࠨᓌ").join((scope, fixturename))
            bstack1l11l11ll11_opy_ = datetime.now(tz=timezone.utc)
            bstack1l111lll11l_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠧࡱࡥࡺࠤᓍ"): bstack1l111l1ll1l_opy_,
                bstack1l1l1l1_opy_ (u"ࠨࡴࡢࡩࡶࠦᓎ"): bstack1lll1llll11_opy_.__1l11l1l1111_opy_(request.node),
                bstack1l1l1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᓏ"): fixturedef,
                bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᓐ"): scope,
                bstack1l1l1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᓑ"): None,
            }
            try:
                if test_hook_state == bstack1lll1lll111_opy_.POST and callable(getattr(args[-1], bstack1l1l1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᓒ"), None)):
                    bstack1l111lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤᓓ")] = TestFramework.bstack1l1llllllll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1lll111_opy_.PRE:
                bstack1l111lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥᓔ")] = uuid4().__str__()
                bstack1l111lll11l_opy_[bstack1lll1llll11_opy_.bstack1l1111ll1l1_opy_] = bstack1l11l11ll11_opy_
            elif test_hook_state == bstack1lll1lll111_opy_.POST:
                bstack1l111lll11l_opy_[bstack1lll1llll11_opy_.bstack1l1111l111l_opy_] = bstack1l11l11ll11_opy_
            if bstack1l111l1ll1l_opy_ in bstack1l111l111ll_opy_:
                bstack1l111l111ll_opy_[bstack1l111l1ll1l_opy_].update(bstack1l111lll11l_opy_)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᓕ") + str(bstack1l111l111ll_opy_[bstack1l111l1ll1l_opy_]) + bstack1l1l1l1_opy_ (u"ࠢࠣᓖ"))
            else:
                bstack1l111l111ll_opy_[bstack1l111l1ll1l_opy_] = bstack1l111lll11l_opy_
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᓗ") + str(len(bstack1l111l111ll_opy_)) + bstack1l1l1l1_opy_ (u"ࠤࠥᓘ"))
        TestFramework.bstack1lllll1111l_opy_(instance, bstack1lll1llll11_opy_.bstack1l11l1l111l_opy_, bstack1l111l111ll_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᓙ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠦࠧᓚ"))
        return instance
    def __1l111ll1111_opy_(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llllll11ll_opy_.create_context(target)
        ob = bstack1lll1l1l1l1_opy_(ctx, self.bstack1ll1l111ll1_opy_, self.bstack1l11l11111l_opy_, test_framework_state)
        TestFramework.bstack1l11111ll1l_opy_(ob, {
            TestFramework.bstack1ll1l11l1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l1ll1111l1_opy_: context.test_framework_version,
            TestFramework.bstack1l111l1lll1_opy_: [],
            bstack1lll1llll11_opy_.bstack1l11l1l111l_opy_: {},
            bstack1lll1llll11_opy_.bstack1l11111lll1_opy_: {},
            bstack1lll1llll11_opy_.bstack1l11l11lll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lllll1111l_opy_(ob, TestFramework.bstack1l11l11l111_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lllll1111l_opy_(ob, TestFramework.bstack1ll111ll1ll_opy_, context.platform_index)
        TestFramework.bstack1llllllll11_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᓛ") + str(TestFramework.bstack1llllllll11_opy_.keys()) + bstack1l1l1l1_opy_ (u"ࠨࠢᓜ"))
        return ob
    def bstack1l1lll1111l_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_]):
        bstack1l11l11l1l1_opy_ = (
            bstack1lll1llll11_opy_.bstack1l111lll1ll_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1lll1lll111_opy_.PRE
            else bstack1lll1llll11_opy_.bstack1l11l1l1ll1_opy_
        )
        hook = bstack1lll1llll11_opy_.bstack1l111l11111_opy_(instance, bstack1l11l11l1l1_opy_)
        entries = hook.get(TestFramework.bstack1l11111ll11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, []))
        return entries
    def bstack1l1lll11l11_opy_(self, instance: bstack1lll1l1l1l1_opy_, bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_]):
        bstack1l11l11l1l1_opy_ = (
            bstack1lll1llll11_opy_.bstack1l111lll1ll_opy_
            if bstack1lllll11ll1_opy_[1] == bstack1lll1lll111_opy_.PRE
            else bstack1lll1llll11_opy_.bstack1l11l1l1ll1_opy_
        )
        bstack1lll1llll11_opy_.bstack1l111l111l1_opy_(instance, bstack1l11l11l1l1_opy_)
        TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, []).clear()
    def bstack1l111l11ll1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1l1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᓝ")
        global _1l1lll111l1_opy_
        platform_index = os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᓞ")]
        bstack1l1ll111l1l_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1llllll1l_opy_ + str(platform_index)), bstack1l111111l11_opy_)
        if not os.path.exists(bstack1l1ll111l1l_opy_) or not os.path.isdir(bstack1l1ll111l1l_opy_):
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢᓟ").format(bstack1l1ll111l1l_opy_))
            return
        logs = hook.get(bstack1l1l1l1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᓠ"), [])
        with os.scandir(bstack1l1ll111l1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1lll111l1_opy_:
                    self.logger.info(bstack1l1l1l1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᓡ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1l1l1_opy_ (u"ࠧࠨᓢ")
                    log_entry = bstack1lll111l1l1_opy_(
                        kind=bstack1l1l1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᓣ"),
                        message=bstack1l1l1l1_opy_ (u"ࠢࠣᓤ"),
                        level=bstack1l1l1l1_opy_ (u"ࠣࠤᓥ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1ll11llll_opy_=entry.stat().st_size,
                        bstack1l1llll1l1l_opy_=bstack1l1l1l1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᓦ"),
                        bstack111l1l1_opy_=os.path.abspath(entry.path),
                        bstack1l11l1l1l11_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                    )
                    logs.append(log_entry)
                    _1l1lll111l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᓧ")]
        bstack1l11111l111_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1llllll1l_opy_ + str(platform_index)), bstack1l111111l11_opy_, bstack11lllllllll_opy_)
        if not os.path.exists(bstack1l11111l111_opy_) or not os.path.isdir(bstack1l11111l111_opy_):
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᓨ").format(bstack1l11111l111_opy_))
        else:
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᓩ").format(bstack1l11111l111_opy_))
            with os.scandir(bstack1l11111l111_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1lll111l1_opy_:
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᓪ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1l1l1_opy_ (u"ࠢࠣᓫ")
                        log_entry = bstack1lll111l1l1_opy_(
                            kind=bstack1l1l1l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᓬ"),
                            message=bstack1l1l1l1_opy_ (u"ࠤࠥᓭ"),
                            level=bstack1l1l1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᓮ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1ll11llll_opy_=entry.stat().st_size,
                            bstack1l1llll1l1l_opy_=bstack1l1l1l1_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᓯ"),
                            bstack111l1l1_opy_=os.path.abspath(entry.path),
                            bstack1l1ll1ll11l_opy_=hook.get(TestFramework.bstack1l11l11l1ll_opy_)
                        )
                        logs.append(log_entry)
                        _1l1lll111l1_opy_.add(abs_path)
        hook[bstack1l1l1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᓰ")] = logs
    def bstack1l1lll11111_opy_(
        self,
        bstack1l1lll111ll_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1lll111l1l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᓱ"))
        req.platform_index = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll111ll1ll_opy_)
        req.execution_context.hash = str(bstack1l1lll111ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll1l11l1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1ll1111l1_opy_)
            log_entry.uuid = entry.bstack1l11l1l1l11_opy_
            log_entry.test_framework_state = bstack1l1lll111ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1l1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᓲ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1l1l1_opy_ (u"ࠣࠤᓳ")
            if entry.kind == bstack1l1l1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᓴ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll11llll_opy_
                log_entry.file_path = entry.bstack111l1l1_opy_
        def bstack1l1lll11lll_opy_():
            bstack1l1ll1l1ll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll111l1_opy_.LogCreatedEvent(req)
                bstack1l1lll111ll_opy_.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᓵ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᓶ").format(str(e)))
                traceback.print_exc()
        self.bstack111111lll1_opy_.enqueue(bstack1l1lll11lll_opy_)
    def __1l111llllll_opy_(self, instance) -> None:
        bstack1l1l1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᓷ")
        bstack1l11l1l1l1l_opy_ = {bstack1l1l1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᓸ"): bstack1lll11l1lll_opy_.bstack1l11111l1ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11111ll1l_opy_(instance, bstack1l11l1l1l1l_opy_)
    @staticmethod
    def bstack1l111l11111_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11l11l1l1_opy_: str):
        bstack1l1111l1ll1_opy_ = (
            bstack1lll1llll11_opy_.bstack1l11111lll1_opy_
            if bstack1l11l11l1l1_opy_ == bstack1lll1llll11_opy_.bstack1l11l1l1ll1_opy_
            else bstack1lll1llll11_opy_.bstack1l11l11lll1_opy_
        )
        bstack1l111l1l1l1_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l11l11l1l1_opy_, None)
        bstack1l1111l1lll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l1111l1ll1_opy_, None) if bstack1l111l1l1l1_opy_ else None
        return (
            bstack1l1111l1lll_opy_[bstack1l111l1l1l1_opy_][-1]
            if isinstance(bstack1l1111l1lll_opy_, dict) and len(bstack1l1111l1lll_opy_.get(bstack1l111l1l1l1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l111l1_opy_(instance: bstack1lll1l1l1l1_opy_, bstack1l11l11l1l1_opy_: str):
        hook = bstack1lll1llll11_opy_.bstack1l111l11111_opy_(instance, bstack1l11l11l1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11111ll11_opy_, []).clear()
    @staticmethod
    def __1l111ll1l11_opy_(instance: bstack1lll1l1l1l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1l1l1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᓹ"), None)):
            return
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᓺ"), bstack1l1l1l1_opy_ (u"ࠤ࠴ࠦᓻ")) != bstack1l1l1l1_opy_ (u"ࠥ࠵ࠧᓼ"):
            bstack1lll1llll11_opy_.logger.warning(bstack1l1l1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᓽ"))
            return
        bstack1l111ll1ll1_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᓾ"): (bstack1lll1llll11_opy_.bstack1l111lll1ll_opy_, bstack1lll1llll11_opy_.bstack1l11l11lll1_opy_),
            bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᓿ"): (bstack1lll1llll11_opy_.bstack1l11l1l1ll1_opy_, bstack1lll1llll11_opy_.bstack1l11111lll1_opy_),
        }
        for when in (bstack1l1l1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᔀ"), bstack1l1l1l1_opy_ (u"ࠣࡥࡤࡰࡱࠨᔁ"), bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᔂ")):
            bstack1l111ll11l1_opy_ = args[1].get_records(when)
            if not bstack1l111ll11l1_opy_:
                continue
            records = [
                bstack1lll111l1l1_opy_(
                    kind=TestFramework.bstack1l1ll111lll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1l1l1_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᔃ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1l1l1_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᔄ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l111ll11l1_opy_
                if isinstance(getattr(r, bstack1l1l1l1_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᔅ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11111l1l1_opy_, bstack1l1111l1ll1_opy_ = bstack1l111ll1ll1_opy_.get(when, (None, None))
            bstack1l11l11llll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l11111l1l1_opy_, None) if bstack1l11111l1l1_opy_ else None
            bstack1l1111l1lll_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, bstack1l1111l1ll1_opy_, None) if bstack1l11l11llll_opy_ else None
            if isinstance(bstack1l1111l1lll_opy_, dict) and len(bstack1l1111l1lll_opy_.get(bstack1l11l11llll_opy_, [])) > 0:
                hook = bstack1l1111l1lll_opy_[bstack1l11l11llll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11111ll11_opy_ in hook:
                    hook[TestFramework.bstack1l11111ll11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l111111_opy_(test) -> Dict[str, Any]:
        bstack1l1l11lll1_opy_ = bstack1lll1llll11_opy_.__1l111llll11_opy_(test.location) if hasattr(test, bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᔆ")) else getattr(test, bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᔇ"), None)
        test_name = test.name if hasattr(test, bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᔈ")) else None
        bstack1l111l11l1l_opy_ = test.fspath.strpath if hasattr(test, bstack1l1l1l1_opy_ (u"ࠤࡩࡷࡵࡧࡴࡩࠤᔉ")) and test.fspath else None
        if not bstack1l1l11lll1_opy_ or not test_name or not bstack1l111l11l1l_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1l1l1_opy_ (u"ࠥࡳࡧࡰࠢᔊ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l11111111l_opy_ = []
        try:
            bstack1l11111111l_opy_ = bstack11l1l1l1ll_opy_.bstack1111llllll_opy_(test)
        except:
            bstack1lll1llll11_opy_.logger.warning(bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵ࠯ࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡪࡹ࡯࡭ࡸࡨࡨࠥ࡯࡮ࠡࡅࡏࡍࠧᔋ"))
        return {
            TestFramework.bstack1ll1l11lll1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l111l11_opy_: bstack1l1l11lll1_opy_,
            TestFramework.bstack1ll111llll1_opy_: test_name,
            TestFramework.bstack1l1l1lll1ll_opy_: getattr(test, bstack1l1l1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᔌ"), None),
            TestFramework.bstack1l11l11l11l_opy_: bstack1l111l11l1l_opy_,
            TestFramework.bstack1l1111ll111_opy_: bstack1lll1llll11_opy_.__1l11l1l1111_opy_(test),
            TestFramework.bstack1l11l1l11ll_opy_: code,
            TestFramework.bstack1l1l111ll11_opy_: TestFramework.bstack1l11l11ll1l_opy_,
            TestFramework.bstack1l11ll1l1l1_opy_: bstack1l1l11lll1_opy_,
            TestFramework.bstack1l1111111ll_opy_: bstack1l11111111l_opy_
        }
    @staticmethod
    def __1l11l1l1111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1l1l1_opy_ (u"ࠨ࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠦᔍ"), [])
            markers.extend([getattr(m, bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᔎ"), None) for m in own_markers if getattr(m, bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᔏ"), None)])
            current = getattr(current, bstack1l1l1l1_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᔐ"), None)
        return markers
    @staticmethod
    def __1l111llll11_opy_(location):
        return bstack1l1l1l1_opy_ (u"ࠥ࠾࠿ࠨᔑ").join(filter(lambda x: isinstance(x, str), location))