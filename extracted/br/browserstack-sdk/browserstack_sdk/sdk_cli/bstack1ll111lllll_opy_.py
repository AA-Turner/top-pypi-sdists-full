# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1l1l111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1l1111_opy_ import bstack11ll1ll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll11l1l1l1_opy_,
    bstack1ll1ll111l1_opy_,
    bstack1ll1111llll_opy_,
    bstack11lll11llll_opy_,
    bstack1ll1lll11ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l11ll1ll1l_opy_
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lll1111ll1_opy_ import bstack1ll1ll1ll11_opy_
from bstack_utils.bstack1111llll11_opy_ import bstack1ll11l1l1l_opy_
bstack1l1l111ll1l_opy_ = bstack1l11ll1ll1l_opy_()
bstack11lll111l1l_opy_ = 1.0
bstack1l11ll1l111_opy_ = bstack11l1ll1_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᗦ")
bstack11ll1l11111_opy_ = bstack11l1ll1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᗧ")
bstack11ll1l1111l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᗨ")
bstack11ll11llll1_opy_ = bstack11l1ll1_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᗩ")
bstack11ll11lll11_opy_ = bstack11l1ll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᗪ")
_1l11llll111_opy_ = set()
class bstack1ll1l1ll1l1_opy_(TestFramework):
    bstack11llll11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᗫ")
    bstack11ll1ll1ll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᗬ")
    bstack11lll1lllll_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᗭ")
    bstack11ll1l11l11_opy_ = bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᗮ")
    bstack11lll1ll11l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᗯ")
    bstack11lll11l1l1_opy_: bool
    bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_  = None
    bstack1ll1llll1ll_opy_ = None
    bstack11llll1llll_opy_ = [
        bstack1ll11l1l1l1_opy_.BEFORE_ALL,
        bstack1ll11l1l1l1_opy_.AFTER_ALL,
        bstack1ll11l1l1l1_opy_.BEFORE_EACH,
        bstack1ll11l1l1l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll1l11lll_opy_: Dict[str, str],
        bstack1l1lll1l1ll_opy_: List[str]=[bstack11l1ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᗰ")],
        bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_=None,
        bstack1ll1llll1ll_opy_=None
    ):
        super().__init__(bstack1l1lll1l1ll_opy_, bstack11ll1l11lll_opy_, bstack1lll1llll11_opy_)
        self.bstack11lll11l1l1_opy_ = any(bstack11l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᗱ") in item.lower() for item in bstack1l1lll1l1ll_opy_)
        self.bstack1ll1llll1ll_opy_ = bstack1ll1llll1ll_opy_
    def track_event(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll11l1l1l1_opy_.TEST or test_framework_state in bstack1ll1l1ll1l1_opy_.bstack11llll1llll_opy_:
            bstack11ll1ll1111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll11l1l1l1_opy_.NONE:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᗲ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠧࠨᗳ"))
            return
        if not self.bstack11lll11l1l1_opy_:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᗴ") + str(str(self.bstack1l1lll1l1ll_opy_)) + bstack11l1ll1_opy_ (u"ࠢࠣᗵ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᗶ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᗷ"))
            return
        instance = self.__11lll1l11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᗸ") + str(args) + bstack11l1ll1_opy_ (u"ࠦࠧᗹ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1l1ll1l1_opy_.bstack11llll1llll_opy_:
                bstack1lll1llll1_opy_ = bstack11l1ll1_opy_ (u"ࠧࠨᗺ")
                name = bstack11l1ll1_opy_ (u"ࠨࠢᗻ")
                if (test_hook_state == bstack1ll1111llll_opy_.PRE):
                    bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack11ll11ll1l1_opy_.value)
                    name = str(EVENTS.bstack11ll11ll1l1_opy_.name)+bstack11l1ll1_opy_ (u"ࠢ࠻ࠤᗼ")+str(test_framework_state.name)
                else:
                    bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack11ll11ll1ll_opy_.value)
                    name = str(EVENTS.bstack11ll11ll1ll_opy_.name)+bstack11l1ll1_opy_ (u"ࠣ࠼ࠥᗽ")+str(test_framework_state.name)
                TestFramework.bstack11ll1l1l1l1_opy_(instance, name, bstack1lll1llll1_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶࠥࡶࡲࡦ࠼ࠣࡿࢂࠨᗾ").format(e))
        try:
            if not TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_) and test_hook_state == bstack1ll1111llll_opy_.PRE:
                test = bstack1ll1l1ll1l1_opy_.__11lll111ll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡰࡴࡧࡤࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᗿ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠦࠧᘀ"))
            if test_framework_state == bstack1ll11l1l1l1_opy_.TEST:
                if test_hook_state == bstack1ll1111llll_opy_.PRE and not TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll1ll11_opy_):
                    TestFramework.bstack1lll1l1111l_opy_(instance, TestFramework.bstack1l11ll1ll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡹࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᘁ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠨࠢᘂ"))
                elif test_hook_state == bstack1ll1111llll_opy_.POST and not TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l1l11lll11_opy_):
                    TestFramework.bstack1lll1l1111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᘃ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠣࠤᘄ"))
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG and test_hook_state == bstack1ll1111llll_opy_.POST:
                bstack1ll1l1ll1l1_opy_.__11llll111ll_opy_(instance, *args)
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG_REPORT and test_hook_state == bstack1ll1111llll_opy_.POST:
                self.__11lll1111ll_opy_(instance, *args)
                self.__11ll1l1ll11_opy_(instance)
            elif test_framework_state in bstack1ll1l1ll1l1_opy_.bstack11llll1llll_opy_:
                self.__11lll11111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᘅ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠥࠦᘆ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lll1ll111_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1l1ll1l1_opy_.bstack11llll1llll_opy_:
                bstack1lll1llll1_opy_ = bstack11l1ll1_opy_ (u"ࠦࠧᘇ")
                name = bstack11l1ll1_opy_ (u"ࠧࠨᘈ")
                if (test_hook_state == bstack1ll1111llll_opy_.PRE):
                    name = str(EVENTS.bstack11ll11ll1l1_opy_.name)+bstack11l1ll1_opy_ (u"ࠨ࠺ࠣᘉ")+str(test_framework_state.name)
                    bstack1lll1llll1_opy_ = TestFramework.bstack11lllll11ll_opy_(instance, name)
                    bstack1ll1111ll_opy_.end(EVENTS.bstack11ll11ll1l1_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘊ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘋ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11ll11ll1ll_opy_.name)+bstack11l1ll1_opy_ (u"ࠤ࠽ࠦᘌ")+str(test_framework_state.name)
                    bstack1lll1llll1_opy_ = TestFramework.bstack11lllll11ll_opy_(instance, name)
                    bstack1ll1111ll_opy_.end(EVENTS.bstack11ll11ll1ll_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘍ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘎ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᘏ").format(e))
    def bstack1l1l11l11l1_opy_(self):
        return self.bstack11lll11l1l1_opy_
    def __11ll1l1l11l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1ll1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᘐ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11l1lll11_opy_(rep, [bstack11l1ll1_opy_ (u"ࠢࡸࡪࡨࡲࠧᘑ"), bstack11l1ll1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᘒ"), bstack11l1ll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᘓ"), bstack11l1ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᘔ"), bstack11l1ll1_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠧᘕ"), bstack11l1ll1_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᘖ")])
        return None
    def __11lll1111ll_opy_(self, instance: bstack1ll1ll111l1_opy_, *args):
        result = self.__11ll1l1l11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llll11111l_opy_ = None
        if result.get(bstack11l1ll1_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᘗ"), None) == bstack11l1ll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᘘ") and len(args) > 1 and getattr(args[1], bstack11l1ll1_opy_ (u"ࠣࡧࡻࡧ࡮ࡴࡦࡰࠤᘙ"), None) is not None:
            failure = [{bstack11l1ll1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᘚ"): [args[1].excinfo.exconly(), result.get(bstack11l1ll1_opy_ (u"ࠥࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠤᘛ"), None)]}]
            bstack1llll11111l_opy_ = bstack11l1ll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᘜ") if bstack11l1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᘝ") in getattr(args[1].excinfo, bstack11l1ll1_opy_ (u"ࠨࡴࡺࡲࡨࡲࡦࡳࡥࠣᘞ"), bstack11l1ll1_opy_ (u"ࠢࠣᘟ")) else bstack11l1ll1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᘠ")
        bstack11lll1ll1l1_opy_ = result.get(bstack11l1ll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᘡ"), TestFramework.bstack11ll1l1l111_opy_)
        if bstack11lll1ll1l1_opy_ != TestFramework.bstack11ll1l1l111_opy_:
            TestFramework.bstack1lll1l1111l_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11lll1111l1_opy_(instance, {
            TestFramework.bstack1l111ll111l_opy_: failure,
            TestFramework.bstack11llll1ll11_opy_: bstack1llll11111l_opy_,
            TestFramework.bstack1l111l1ll11_opy_: bstack11lll1ll1l1_opy_,
        })
    def __11lll1l11l1_opy_(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll11l1l1l1_opy_.SETUP_FIXTURE:
            instance = self.__11ll1lll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1l1lll1_opy_ bstack11lll11lll1_opy_ this to be bstack11l1ll1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᘢ")
            if test_framework_state == bstack1ll11l1l1l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll1lll1l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1ll1_opy_ (u"ࠦࡳࡵࡤࡦࠤᘣ"), None), bstack11l1ll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᘤ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᘥ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll11ll11l_opy_(target) if target else None
        return instance
    def __11lll11111l_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11ll1lllll1_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1ll1l1_opy_.bstack11ll1ll1ll1_opy_, {})
        if not key in bstack11ll1lllll1_opy_:
            bstack11ll1lllll1_opy_[key] = []
        bstack11llll1l11l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1ll1l1_opy_.bstack11lll1lllll_opy_, {})
        if not key in bstack11llll1l11l_opy_:
            bstack11llll1l11l_opy_[key] = []
        bstack11lll1l1ll1_opy_ = {
            bstack1ll1l1ll1l1_opy_.bstack11ll1ll1ll1_opy_: bstack11ll1lllll1_opy_,
            bstack1ll1l1ll1l1_opy_.bstack11lll1lllll_opy_: bstack11llll1l11l_opy_,
        }
        if test_hook_state == bstack1ll1111llll_opy_.PRE:
            hook = {
                bstack11l1ll1_opy_ (u"ࠢ࡬ࡧࡼࠦᘦ"): key,
                TestFramework.bstack11llll1lll1_opy_: uuid4().__str__(),
                TestFramework.bstack11ll1llll1l_opy_: TestFramework.bstack11llll1ll1l_opy_,
                TestFramework.bstack11ll1ll1lll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11lll1l1l1l_opy_: [],
                TestFramework.bstack11lll1llll1_opy_: args[1] if len(args) > 1 else bstack11l1ll1_opy_ (u"ࠨࠩᘧ"),
                TestFramework.bstack11ll1lll111_opy_: bstack1ll1ll1ll11_opy_.bstack11ll1l111l1_opy_()
            }
            bstack11ll1lllll1_opy_[key].append(hook)
            bstack11lll1l1ll1_opy_[bstack1ll1l1ll1l1_opy_.bstack11ll1l11l11_opy_] = key
        elif test_hook_state == bstack1ll1111llll_opy_.POST:
            bstack11ll1l11l1l_opy_ = bstack11ll1lllll1_opy_.get(key, [])
            hook = bstack11ll1l11l1l_opy_.pop() if bstack11ll1l11l1l_opy_ else None
            if hook:
                result = self.__11ll1l1l11l_opy_(*args)
                if result:
                    bstack11llll11l11_opy_ = result.get(bstack11l1ll1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᘨ"), TestFramework.bstack11llll1ll1l_opy_)
                    if bstack11llll11l11_opy_ != TestFramework.bstack11llll1ll1l_opy_:
                        hook[TestFramework.bstack11ll1llll1l_opy_] = bstack11llll11l11_opy_
                hook[TestFramework.bstack11llll1l111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1lll111_opy_]= bstack1ll1ll1ll11_opy_.bstack11ll1l111l1_opy_()
                self.bstack11ll1l1ll1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11lll11ll1l_opy_, [])
                if logs: self.bstack1l11lll1lll_opy_(instance, logs)
                bstack11llll1l11l_opy_[key].append(hook)
                bstack11lll1l1ll1_opy_[bstack1ll1l1ll1l1_opy_.bstack11lll1ll11l_opy_] = key
        TestFramework.bstack11lll1111l1_opy_(instance, bstack11lll1l1ll1_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡ࡫ࡳࡴࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾ࡯ࡪࡿࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࡂࢁࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࢃࠠࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠾ࠤᘩ") + str(bstack11llll1l11l_opy_) + bstack11l1ll1_opy_ (u"ࠦࠧᘪ"))
    def __11ll1lll1ll_opy_(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11l1lll11_opy_(args[0], [bstack11l1ll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᘫ"), bstack11l1ll1_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᘬ"), bstack11l1ll1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᘭ"), bstack11l1ll1_opy_ (u"ࠣ࡫ࡧࡷࠧᘮ"), bstack11l1ll1_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᘯ"), bstack11l1ll1_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᘰ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11l1ll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᘱ")) else fixturedef.get(bstack11l1ll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᘲ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1ll1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᘳ")) else None
        node = request.node if hasattr(request, bstack11l1ll1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᘴ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1ll1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᘵ")) else None
        baseid = fixturedef.get(bstack11l1ll1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᘶ"), None) or bstack11l1ll1_opy_ (u"ࠥࠦᘷ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1ll1_opy_ (u"ࠦࡤࡶࡹࡧࡷࡱࡧ࡮ࡺࡥ࡮ࠤᘸ")):
            target = bstack1ll1l1ll1l1_opy_.__11lll111l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1ll1_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᘹ")) else None
            if target and not TestFramework.bstack1lll11ll11l_opy_(target):
                self.__11ll1lll1l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡦࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡰࡲࡨࡪࡃࡻ࡯ࡱࡧࡩࢂࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࠣᘺ") + str(test_hook_state) + bstack11l1ll1_opy_ (u"ࠢࠣᘻ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࡃࡻࡧ࡫ࡻࡸࡺࡸࡥࡥࡧࡩࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᘼ") + str(target) + bstack11l1ll1_opy_ (u"ࠤࠥᘽ"))
            return None
        instance = TestFramework.bstack1lll11ll11l_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡥࡥࡸ࡫ࡩࡥ࠿ࡾࡦࡦࡹࡥࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᘾ") + str(target) + bstack11l1ll1_opy_ (u"ࠦࠧᘿ"))
            return None
        bstack11lll1l1l11_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack1ll1l1ll1l1_opy_.bstack11llll11l1l_opy_, {})
        if os.getenv(bstack11l1ll1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡋࡏࡘࡕࡗࡕࡉࡘࠨᙀ"), bstack11l1ll1_opy_ (u"ࠨ࠱ࠣᙁ")) == bstack11l1ll1_opy_ (u"ࠢ࠲ࠤᙂ"):
            bstack11llll1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠣ࠼ࠥᙃ").join((scope, fixturename))
            bstack11lllll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll1lll11l_opy_ = {
                bstack11l1ll1_opy_ (u"ࠤ࡮ࡩࡾࠨᙄ"): bstack11llll1l1ll_opy_,
                bstack11l1ll1_opy_ (u"ࠥࡸࡦ࡭ࡳࠣᙅ"): bstack1ll1l1ll1l1_opy_.__11ll1l111ll_opy_(request.node),
                bstack11l1ll1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࠧᙆ"): fixturedef,
                bstack11l1ll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᙇ"): scope,
                bstack11l1ll1_opy_ (u"ࠨࡴࡺࡲࡨࠦᙈ"): None,
            }
            try:
                if test_hook_state == bstack1ll1111llll_opy_.POST and callable(getattr(args[-1], bstack11l1ll1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᙉ"), None)):
                    bstack11ll1lll11l_opy_[bstack11l1ll1_opy_ (u"ࠣࡶࡼࡴࡪࠨᙊ")] = TestFramework.bstack1l1l11l1ll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1111llll_opy_.PRE:
                bstack11ll1lll11l_opy_[bstack11l1ll1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᙋ")] = uuid4().__str__()
                bstack11ll1lll11l_opy_[bstack1ll1l1ll1l1_opy_.bstack11ll1ll1lll_opy_] = bstack11lllll111l_opy_
            elif test_hook_state == bstack1ll1111llll_opy_.POST:
                bstack11ll1lll11l_opy_[bstack1ll1l1ll1l1_opy_.bstack11llll1l111_opy_] = bstack11lllll111l_opy_
            if bstack11llll1l1ll_opy_ in bstack11lll1l1l11_opy_:
                bstack11lll1l1l11_opy_[bstack11llll1l1ll_opy_].update(bstack11ll1lll11l_opy_)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࠦᙌ") + str(bstack11lll1l1l11_opy_[bstack11llll1l1ll_opy_]) + bstack11l1ll1_opy_ (u"ࠦࠧᙍ"))
            else:
                bstack11lll1l1l11_opy_[bstack11llll1l1ll_opy_] = bstack11ll1lll11l_opy_
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡀࡿࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࢀࠤࡹࡸࡡࡤ࡭ࡨࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࠣᙎ") + str(len(bstack11lll1l1l11_opy_)) + bstack11l1ll1_opy_ (u"ࠨࠢᙏ"))
        TestFramework.bstack1lll1l1111l_opy_(instance, bstack1ll1l1ll1l1_opy_.bstack11llll11l1l_opy_, bstack11lll1l1l11_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࡽ࡯ࡩࡳ࠮ࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠫࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᙐ") + str(instance.ref()) + bstack11l1ll1_opy_ (u"ࠣࠤᙑ"))
        return instance
    def __11ll1lll1l1_opy_(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lll1l1l111_opy_.create_context(target)
        ob = bstack1ll1ll111l1_opy_(ctx, self.bstack1l1lll1l1ll_opy_, self.bstack11ll1l11lll_opy_, test_framework_state)
        TestFramework.bstack11lll1111l1_opy_(ob, {
            TestFramework.bstack1l1llllll11_opy_: context.test_framework_name,
            TestFramework.bstack1l1l111llll_opy_: context.test_framework_version,
            TestFramework.bstack11ll1l1l1ll_opy_: [],
            bstack1ll1l1ll1l1_opy_.bstack11llll11l1l_opy_: {},
            bstack1ll1l1ll1l1_opy_.bstack11lll1lllll_opy_: {},
            bstack1ll1l1ll1l1_opy_.bstack11ll1ll1ll1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1l1111l_opy_(ob, TestFramework.bstack11lll1l1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1l1111l_opy_(ob, TestFramework.bstack1l1l1lll1l1_opy_, context.platform_index)
        TestFramework.bstack1lll1ll11ll_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡧࡹࡾ࠮ࡪࡦࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᙒ") + str(TestFramework.bstack1lll1ll11ll_opy_.keys()) + bstack11l1ll1_opy_ (u"ࠥࠦᙓ"))
        return ob
    def bstack1l11llll1ll_opy_(self, instance: bstack1ll1ll111l1_opy_, bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_]):
        bstack11lll11l111_opy_ = (
            bstack1ll1l1ll1l1_opy_.bstack11ll1l11l11_opy_
            if bstack1lll1l1ll11_opy_[1] == bstack1ll1111llll_opy_.PRE
            else bstack1ll1l1ll1l1_opy_.bstack11lll1ll11l_opy_
        )
        hook = bstack1ll1l1ll1l1_opy_.bstack11ll1l1llll_opy_(instance, bstack11lll11l111_opy_)
        entries = hook.get(TestFramework.bstack11lll1l1l1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, []))
        return entries
    def bstack1l11lll11ll_opy_(self, instance: bstack1ll1ll111l1_opy_, bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_]):
        bstack11lll11l111_opy_ = (
            bstack1ll1l1ll1l1_opy_.bstack11ll1l11l11_opy_
            if bstack1lll1l1ll11_opy_[1] == bstack1ll1111llll_opy_.PRE
            else bstack1ll1l1ll1l1_opy_.bstack11lll1ll11l_opy_
        )
        bstack1ll1l1ll1l1_opy_.bstack11lll1ll1ll_opy_(instance, bstack11lll11l111_opy_)
        TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, []).clear()
    def bstack11ll1l1ll1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᙔ")
        global _1l11llll111_opy_
        platform_index = os.environ[bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᙕ")]
        bstack1l11llll11l_opy_ = os.path.join(bstack1l1l111ll1l_opy_, (bstack1l11ll1l111_opy_ + str(platform_index)), bstack11ll11llll1_opy_)
        if not os.path.exists(bstack1l11llll11l_opy_) or not os.path.isdir(bstack1l11llll11l_opy_):
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶࡶࠤࡹࡵࠠࡱࡴࡲࡧࡪࡹࡳࠡࡽࢀࠦᙖ").format(bstack1l11llll11l_opy_))
            return
        logs = hook.get(bstack11l1ll1_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᙗ"), [])
        with os.scandir(bstack1l11llll11l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11llll111_opy_:
                    self.logger.info(bstack11l1ll1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᙘ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1ll1_opy_ (u"ࠤࠥᙙ")
                    log_entry = bstack1ll1lll11ll_opy_(
                        kind=bstack11l1ll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᙚ"),
                        message=bstack11l1ll1_opy_ (u"ࠦࠧᙛ"),
                        level=bstack11l1ll1_opy_ (u"ࠧࠨᙜ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11ll1l1l1_opy_=entry.stat().st_size,
                        bstack1l11lll111l_opy_=bstack11l1ll1_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᙝ"),
                        bstack1ll1lll_opy_=os.path.abspath(entry.path),
                        bstack11ll1llllll_opy_=hook.get(TestFramework.bstack11llll1lll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l11llll111_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᙞ")]
        bstack11llll11ll1_opy_ = os.path.join(bstack1l1l111ll1l_opy_, (bstack1l11ll1l111_opy_ + str(platform_index)), bstack11ll11llll1_opy_, bstack11ll11lll11_opy_)
        if not os.path.exists(bstack11llll11ll1_opy_) or not os.path.isdir(bstack11llll11ll1_opy_):
            self.logger.info(bstack11l1ll1_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᙟ").format(bstack11llll11ll1_opy_))
        else:
            self.logger.info(bstack11l1ll1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᙠ").format(bstack11llll11ll1_opy_))
            with os.scandir(bstack11llll11ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11llll111_opy_:
                        self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᙡ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1ll1_opy_ (u"ࠦࠧᙢ")
                        log_entry = bstack1ll1lll11ll_opy_(
                            kind=bstack11l1ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᙣ"),
                            message=bstack11l1ll1_opy_ (u"ࠨࠢᙤ"),
                            level=bstack11l1ll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᙥ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11ll1l1l1_opy_=entry.stat().st_size,
                            bstack1l11lll111l_opy_=bstack11l1ll1_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᙦ"),
                            bstack1ll1lll_opy_=os.path.abspath(entry.path),
                            bstack1l1l11l1l11_opy_=hook.get(TestFramework.bstack11llll1lll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l11llll111_opy_.add(abs_path)
        hook[bstack11l1ll1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᙧ")] = logs
    def bstack1l11lll1lll_opy_(
        self,
        bstack1l11lll1ll1_opy_: bstack1ll1ll111l1_opy_,
        entries: List[bstack1ll1lll11ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᙨ"))
        req.platform_index = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1l1lll1l1_opy_)
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᙩ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11lll1ll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11lll1ll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11lll1ll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1llllll11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1l111llll_opy_)
            log_entry.uuid = entry.bstack11ll1llllll_opy_
            log_entry.test_framework_state = bstack1l11lll1ll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1ll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᙪ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l1ll1_opy_ (u"ࠨࠢᙫ")
            if entry.kind == bstack11l1ll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᙬ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l1l1_opy_
                log_entry.file_path = entry.bstack1ll1lll_opy_
        def bstack1l11ll1llll_opy_():
            bstack111ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1ll1llll1ll_opy_.LogCreatedEvent(req)
                bstack1l11lll1ll1_opy_.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ᙭"), datetime.now() - bstack111ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1ll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡽࠣ᙮").format(str(e)))
                traceback.print_exc()
        self.bstack1lll1llll11_opy_.enqueue(bstack1l11ll1llll_opy_)
    def __11ll1l1ll11_opy_(self, instance) -> None:
        bstack11l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᙯ")
        bstack11lll1l1ll1_opy_ = {bstack11l1ll1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᙰ"): bstack1ll1ll1ll11_opy_.bstack11ll1l111l1_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11lll1111l1_opy_(instance, bstack11lll1l1ll1_opy_)
    @staticmethod
    def bstack11ll1l1llll_opy_(instance: bstack1ll1ll111l1_opy_, bstack11lll11l111_opy_: str):
        bstack11llll1l1l1_opy_ = (
            bstack1ll1l1ll1l1_opy_.bstack11lll1lllll_opy_
            if bstack11lll11l111_opy_ == bstack1ll1l1ll1l1_opy_.bstack11lll1ll11l_opy_
            else bstack1ll1l1ll1l1_opy_.bstack11ll1ll1ll1_opy_
        )
        bstack11ll1ll111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11lll11l111_opy_, None)
        bstack11lll1l111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11llll1l1l1_opy_, None) if bstack11ll1ll111l_opy_ else None
        return (
            bstack11lll1l111l_opy_[bstack11ll1ll111l_opy_][-1]
            if isinstance(bstack11lll1l111l_opy_, dict) and len(bstack11lll1l111l_opy_.get(bstack11ll1ll111l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lll1ll1ll_opy_(instance: bstack1ll1ll111l1_opy_, bstack11lll11l111_opy_: str):
        hook = bstack1ll1l1ll1l1_opy_.bstack11ll1l1llll_opy_(instance, bstack11lll11l111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11lll1l1l1l_opy_, []).clear()
    @staticmethod
    def __11llll111ll_opy_(instance: bstack1ll1ll111l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1ll1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᙱ"), None)):
            return
        if os.getenv(bstack11l1ll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᙲ"), bstack11l1ll1_opy_ (u"ࠢ࠲ࠤᙳ")) != bstack11l1ll1_opy_ (u"ࠣ࠳ࠥᙴ"):
            bstack1ll1l1ll1l1_opy_.logger.warning(bstack11l1ll1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᙵ"))
            return
        bstack11ll1ll11l1_opy_ = {
            bstack11l1ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᙶ"): (bstack1ll1l1ll1l1_opy_.bstack11ll1l11l11_opy_, bstack1ll1l1ll1l1_opy_.bstack11ll1ll1ll1_opy_),
            bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᙷ"): (bstack1ll1l1ll1l1_opy_.bstack11lll1ll11l_opy_, bstack1ll1l1ll1l1_opy_.bstack11lll1lllll_opy_),
        }
        for when in (bstack11l1ll1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᙸ"), bstack11l1ll1_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᙹ"), bstack11l1ll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᙺ")):
            bstack11llll11lll_opy_ = args[1].get_records(when)
            if not bstack11llll11lll_opy_:
                continue
            records = [
                bstack1ll1lll11ll_opy_(
                    kind=TestFramework.bstack1l1l11l1l1l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1ll1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᙻ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1ll1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᙼ")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll11lll_opy_
                if isinstance(getattr(r, bstack11l1ll1_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᙽ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11lll11ll11_opy_, bstack11llll1l1l1_opy_ = bstack11ll1ll11l1_opy_.get(when, (None, None))
            bstack11ll1l11ll1_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11lll11ll11_opy_, None) if bstack11lll11ll11_opy_ else None
            bstack11lll1l111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, bstack11llll1l1l1_opy_, None) if bstack11ll1l11ll1_opy_ else None
            if isinstance(bstack11lll1l111l_opy_, dict) and len(bstack11lll1l111l_opy_.get(bstack11ll1l11ll1_opy_, [])) > 0:
                hook = bstack11lll1l111l_opy_[bstack11ll1l11ll1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11lll1l1l1l_opy_ in hook:
                    hook[TestFramework.bstack11lll1l1l1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack11ll1l1l1ll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11lll111ll1_opy_(test) -> Dict[str, Any]:
        bstack1111ll111_opy_ = bstack1ll1l1ll1l1_opy_.__11lll111l11_opy_(test.location) if hasattr(test, bstack11l1ll1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᙾ")) else getattr(test, bstack11l1ll1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᙿ"), None)
        test_name = test.name if hasattr(test, bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ ")) else None
        bstack11llll1111l_opy_ = test.fspath.strpath if hasattr(test, bstack11l1ll1_opy_ (u"ࠢࡧࡵࡳࡥࡹ࡮ࠢᚁ")) and test.fspath else None
        if not bstack1111ll111_opy_ or not test_name or not bstack11llll1111l_opy_:
            return None
        code = None
        if hasattr(test, bstack11l1ll1_opy_ (u"ࠣࡱࡥ࡮ࠧᚂ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11ll11lll1l_opy_ = []
        try:
            bstack11ll11lll1l_opy_ = bstack1ll11l1l1l_opy_.bstack11111l11l1_opy_(test)
        except:
            bstack1ll1l1ll1l1_opy_.logger.warning(bstack11l1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳ࠭ࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡴࡨࡷࡴࡲࡶࡦࡦࠣ࡭ࡳࠦࡃࡍࡋࠥᚃ"))
        return {
            TestFramework.bstack1l1llll1l11_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1ll1l1l_opy_: bstack1111ll111_opy_,
            TestFramework.bstack1l1l1lll11l_opy_: test_name,
            TestFramework.bstack1l11l1l1l11_opy_: getattr(test, bstack11l1ll1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᚄ"), None),
            TestFramework.bstack11lll111111_opy_: bstack11llll1111l_opy_,
            TestFramework.bstack11lll11l11l_opy_: bstack1ll1l1ll1l1_opy_.__11ll1l111ll_opy_(test),
            TestFramework.bstack11llll111l1_opy_: code,
            TestFramework.bstack1l111l1ll11_opy_: TestFramework.bstack11ll1l1l111_opy_,
            TestFramework.bstack1l111111111_opy_: bstack1111ll111_opy_,
            TestFramework.bstack11ll11lllll_opy_: bstack11ll11lll1l_opy_
        }
    @staticmethod
    def __11ll1l111ll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11l1ll1_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤᚅ"), [])
            markers.extend([getattr(m, bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᚆ"), None) for m in own_markers if getattr(m, bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᚇ"), None)])
            current = getattr(current, bstack11l1ll1_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᚈ"), None)
        return markers
    @staticmethod
    def __11lll111l11_opy_(location):
        return bstack11l1ll1_opy_ (u"ࠣ࠼࠽ࠦᚉ").join(filter(lambda x: isinstance(x, str), location))