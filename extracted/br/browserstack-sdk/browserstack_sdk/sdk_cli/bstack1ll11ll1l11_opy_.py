# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll1ll11_opy_ import bstack11llll11lll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll111ll_opy_,
    bstack1ll111l1lll_opy_,
    bstack1ll1l111111_opy_,
    bstack11lllll1l11_opy_,
    bstack1ll11l1l11l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1111l11_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1lllll11_opy_ import bstack1ll1ll1ll11_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack1lll11ll11_opy_
bstack1l11ll111ll_opy_ = bstack1l1l1111l11_opy_()
bstack11llll1ll1l_opy_ = 1.0
bstack1l1l11l11l1_opy_ = bstack1l1111_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᗠ")
bstack11ll11lllll_opy_ = bstack1l1111_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᗡ")
bstack11ll11lll1l_opy_ = bstack1l1111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᗢ")
bstack11ll1l11l11_opy_ = bstack1l1111_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᗣ")
bstack11ll1l1111l_opy_ = bstack1l1111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᗤ")
_1l11lll1ll1_opy_ = set()
class bstack1ll1l1lllll_opy_(TestFramework):
    bstack11llll11l1l_opy_ = bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᗥ")
    bstack11ll1ll1111_opy_ = bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࠦᗦ")
    bstack11ll1ll1lll_opy_ = bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᗧ")
    bstack11ll1l11l1l_opy_ = bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࠥᗨ")
    bstack11ll1ll111l_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᗩ")
    bstack11ll1l11ll1_opy_: bool
    bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_  = None
    bstack1ll1111l1ll_opy_ = None
    bstack11lll1ll1ll_opy_ = [
        bstack1ll1ll111ll_opy_.BEFORE_ALL,
        bstack1ll1ll111ll_opy_.AFTER_ALL,
        bstack1ll1ll111ll_opy_.BEFORE_EACH,
        bstack1ll1ll111ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll1l1l11l_opy_: Dict[str, str],
        bstack1l1ll1l1l1l_opy_: List[str]=[bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᗪ")],
        bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_=None,
        bstack1ll1111l1ll_opy_=None
    ):
        super().__init__(bstack1l1ll1l1l1l_opy_, bstack11ll1l1l11l_opy_, bstack1lll1llll1l_opy_)
        self.bstack11ll1l11ll1_opy_ = any(bstack1l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᗫ") in item.lower() for item in bstack1l1ll1l1l1l_opy_)
        self.bstack1ll1111l1ll_opy_ = bstack1ll1111l1ll_opy_
    def track_event(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll111ll_opy_.TEST or test_framework_state in bstack1ll1l1lllll_opy_.bstack11lll1ll1ll_opy_:
            bstack11llll11lll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll111ll_opy_.NONE:
            self.logger.warning(bstack1l1111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࡩࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࠨᗬ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠨࠢᗭ"))
            return
        if not self.bstack11ll1l11ll1_opy_:
            self.logger.warning(bstack1l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠽ࠣᗮ") + str(str(self.bstack1l1ll1l1l1l_opy_)) + bstack1l1111_opy_ (u"ࠣࠤᗯ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᗰ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᗱ"))
            return
        instance = self.__11ll1l1lll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡦࡸࡧࡴ࠿ࠥᗲ") + str(args) + bstack1l1111_opy_ (u"ࠧࠨᗳ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1l1lllll_opy_.bstack11lll1ll1ll_opy_:
                bstack1ll1111lll_opy_ = bstack1l1111_opy_ (u"ࠨࠢᗴ")
                name = bstack1l1111_opy_ (u"ࠢࠣᗵ")
                if (test_hook_state == bstack1ll1l111111_opy_.PRE):
                    bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11ll1l11111_opy_.value)
                    name = str(EVENTS.bstack11ll1l11111_opy_.name)+bstack1l1111_opy_ (u"ࠣ࠼ࠥᗶ")+str(test_framework_state.name)
                else:
                    bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11ll11llll1_opy_.value)
                    name = str(EVENTS.bstack11ll11llll1_opy_.name)+bstack1l1111_opy_ (u"ࠤ࠽ࠦᗷ")+str(test_framework_state.name)
                TestFramework.bstack11lll1ll111_opy_(instance, name, bstack1ll1111lll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᗸ").format(e))
        try:
            if not TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack11lllll111l_opy_) and test_hook_state == bstack1ll1l111111_opy_.PRE:
                test = bstack1ll1l1lllll_opy_.__11ll1lll1l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1111_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᗹ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠧࠨᗺ"))
            if test_framework_state == bstack1ll1ll111ll_opy_.TEST:
                if test_hook_state == bstack1ll1l111111_opy_.PRE and not TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l11lll1l11_opy_):
                    TestFramework.bstack1lll11l1ll1_opy_(instance, TestFramework.bstack1l11lll1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᗻ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠢࠣᗼ"))
                elif test_hook_state == bstack1ll1l111111_opy_.POST and not TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l11_opy_):
                    TestFramework.bstack1lll11l1ll1_opy_(instance, TestFramework.bstack1l1l11l1l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1111_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᗽ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠤࠥᗾ"))
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG and test_hook_state == bstack1ll1l111111_opy_.POST:
                bstack1ll1l1lllll_opy_.__11llll1ll11_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG_REPORT and test_hook_state == bstack1ll1l111111_opy_.POST:
                self.__11llll1l111_opy_(instance, *args)
                self.__11ll1lll1ll_opy_(instance)
            elif test_framework_state in bstack1ll1l1lllll_opy_.bstack11lll1ll1ll_opy_:
                self.__11lll111l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᗿ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠦࠧᘀ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lllll11ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1l1lllll_opy_.bstack11lll1ll1ll_opy_:
                bstack1ll1111lll_opy_ = bstack1l1111_opy_ (u"ࠧࠨᘁ")
                name = bstack1l1111_opy_ (u"ࠨࠢᘂ")
                if (test_hook_state == bstack1ll1l111111_opy_.PRE):
                    name = str(EVENTS.bstack11ll1l11111_opy_.name)+bstack1l1111_opy_ (u"ࠢ࠻ࠤᘃ")+str(test_framework_state.name)
                    bstack1ll1111lll_opy_ = TestFramework.bstack11ll1llllll_opy_(instance, name)
                    bstack11ll111lll_opy_.end(EVENTS.bstack11ll1l11111_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘄ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘅ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11ll11llll1_opy_.name)+bstack1l1111_opy_ (u"ࠥ࠾ࠧᘆ")+str(test_framework_state.name)
                    bstack1ll1111lll_opy_ = TestFramework.bstack11ll1llllll_opy_(instance, name)
                    bstack11ll111lll_opy_.end(EVENTS.bstack11ll11llll1_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘇ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᘈ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᘉ").format(e))
    def bstack1l11lll11ll_opy_(self):
        return self.bstack11ll1l11ll1_opy_
    def __11lll11llll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1111_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᘊ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l1111111_opy_(rep, [bstack1l1111_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᘋ"), bstack1l1111_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᘌ"), bstack1l1111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᘍ"), bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᘎ"), bstack1l1111_opy_ (u"ࠧࡹ࡫ࡪࡲࡳࡩࡩࠨᘏ"), bstack1l1111_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᘐ")])
        return None
    def __11llll1l111_opy_(self, instance: bstack1ll111l1lll_opy_, *args):
        result = self.__11lll11llll_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llll1111l1_opy_ = None
        if result.get(bstack1l1111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᘑ"), None) == bstack1l1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᘒ") and len(args) > 1 and getattr(args[1], bstack1l1111_opy_ (u"ࠤࡨࡼࡨ࡯࡮ࡧࡱࠥᘓ"), None) is not None:
            failure = [{bstack1l1111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᘔ"): [args[1].excinfo.exconly(), result.get(bstack1l1111_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᘕ"), None)]}]
            bstack1llll1111l1_opy_ = bstack1l1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᘖ") if bstack1l1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᘗ") in getattr(args[1].excinfo, bstack1l1111_opy_ (u"ࠢࡵࡻࡳࡩࡳࡧ࡭ࡦࠤᘘ"), bstack1l1111_opy_ (u"ࠣࠤᘙ")) else bstack1l1111_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᘚ")
        bstack11lll11l11l_opy_ = result.get(bstack1l1111_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᘛ"), TestFramework.bstack11lll1l111l_opy_)
        if bstack11lll11l11l_opy_ != TestFramework.bstack11lll1l111l_opy_:
            TestFramework.bstack1lll11l1ll1_opy_(instance, TestFramework.bstack1l1l1111lll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11llll1llll_opy_(instance, {
            TestFramework.bstack1l111l1ll11_opy_: failure,
            TestFramework.bstack11lll11lll1_opy_: bstack1llll1111l1_opy_,
            TestFramework.bstack1l111l1l1l1_opy_: bstack11lll11l11l_opy_,
        })
    def __11ll1l1lll1_opy_(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll111ll_opy_.SETUP_FIXTURE:
            instance = self.__11llll11l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lll1l1111_opy_ bstack11ll1l1l1ll_opy_ this to be bstack1l1111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᘜ")
            if test_framework_state == bstack1ll1ll111ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lll1l1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᘝ"), None), bstack1l1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᘞ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᘟ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll11l1lll_opy_(target) if target else None
        return instance
    def __11lll111l11_opy_(
        self,
        instance: bstack1ll111l1lll_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11llll1lll1_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack1ll1l1lllll_opy_.bstack11ll1ll1111_opy_, {})
        if not key in bstack11llll1lll1_opy_:
            bstack11llll1lll1_opy_[key] = []
        bstack11lll11l1ll_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack1ll1l1lllll_opy_.bstack11ll1ll1lll_opy_, {})
        if not key in bstack11lll11l1ll_opy_:
            bstack11lll11l1ll_opy_[key] = []
        bstack11ll1l1llll_opy_ = {
            bstack1ll1l1lllll_opy_.bstack11ll1ll1111_opy_: bstack11llll1lll1_opy_,
            bstack1ll1l1lllll_opy_.bstack11ll1ll1lll_opy_: bstack11lll11l1ll_opy_,
        }
        if test_hook_state == bstack1ll1l111111_opy_.PRE:
            hook = {
                bstack1l1111_opy_ (u"ࠣ࡭ࡨࡽࠧᘠ"): key,
                TestFramework.bstack11lll1l1lll_opy_: uuid4().__str__(),
                TestFramework.bstack11llll11111_opy_: TestFramework.bstack11lll11l111_opy_,
                TestFramework.bstack11lllll1l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11lll1ll11l_opy_: [],
                TestFramework.bstack11lll111l1l_opy_: args[1] if len(args) > 1 else bstack1l1111_opy_ (u"ࠩࠪᘡ"),
                TestFramework.bstack11llll111l1_opy_: bstack1ll1ll1ll11_opy_.bstack11ll1llll11_opy_()
            }
            bstack11llll1lll1_opy_[key].append(hook)
            bstack11ll1l1llll_opy_[bstack1ll1l1lllll_opy_.bstack11ll1l11l1l_opy_] = key
        elif test_hook_state == bstack1ll1l111111_opy_.POST:
            bstack11ll1ll11l1_opy_ = bstack11llll1lll1_opy_.get(key, [])
            hook = bstack11ll1ll11l1_opy_.pop() if bstack11ll1ll11l1_opy_ else None
            if hook:
                result = self.__11lll11llll_opy_(*args)
                if result:
                    bstack11lll11ll1l_opy_ = result.get(bstack1l1111_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᘢ"), TestFramework.bstack11lll11l111_opy_)
                    if bstack11lll11ll1l_opy_ != TestFramework.bstack11lll11l111_opy_:
                        hook[TestFramework.bstack11llll11111_opy_] = bstack11lll11ll1l_opy_
                hook[TestFramework.bstack11ll1ll1ll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11llll111l1_opy_]= bstack1ll1ll1ll11_opy_.bstack11ll1llll11_opy_()
                self.bstack11ll1l1l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack11lll11ll11_opy_, [])
                if logs: self.bstack1l1l111l1ll_opy_(instance, logs)
                bstack11lll11l1ll_opy_[key].append(hook)
                bstack11ll1l1llll_opy_[bstack1ll1l1lllll_opy_.bstack11ll1ll111l_opy_] = key
        TestFramework.bstack11llll1llll_opy_(instance, bstack11ll1l1llll_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࡰ࡫ࡹࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩࡃࡻࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࡽࠡࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥ࠿ࠥᘣ") + str(bstack11lll11l1ll_opy_) + bstack1l1111_opy_ (u"ࠧࠨᘤ"))
    def __11llll11l11_opy_(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l1111111_opy_(args[0], [bstack1l1111_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᘥ"), bstack1l1111_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᘦ"), bstack1l1111_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᘧ"), bstack1l1111_opy_ (u"ࠤ࡬ࡨࡸࠨᘨ"), bstack1l1111_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᘩ"), bstack1l1111_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᘪ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᘫ")) else fixturedef.get(bstack1l1111_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᘬ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1111_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᘭ")) else None
        node = request.node if hasattr(request, bstack1l1111_opy_ (u"ࠣࡰࡲࡨࡪࠨᘮ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᘯ")) else None
        baseid = fixturedef.get(bstack1l1111_opy_ (u"ࠥࡦࡦࡹࡥࡪࡦࠥᘰ"), None) or bstack1l1111_opy_ (u"ࠦࠧᘱ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1111_opy_ (u"ࠧࡥࡰࡺࡨࡸࡲࡨ࡯ࡴࡦ࡯ࠥᘲ")):
            target = bstack1ll1l1lllll_opy_.__11lll1ll1l1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1111_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᘳ")) else None
            if target and not TestFramework.bstack1lll11l1lll_opy_(target):
                self.__11lll1l1l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࡾࠢࡱࡳࡩ࡫࠽ࡼࡰࡲࡨࡪࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᘴ") + str(test_hook_state) + bstack1l1111_opy_ (u"ࠣࠤᘵ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᘶ") + str(target) + bstack1l1111_opy_ (u"ࠥࠦᘷ"))
            return None
        instance = TestFramework.bstack1lll11l1lll_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1111_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡦࡦࡹࡥࡪࡦࡀࡿࡧࡧࡳࡦ࡫ࡧࢁࠥࡺࡡࡳࡩࡨࡸࡂࠨᘸ") + str(target) + bstack1l1111_opy_ (u"ࠧࠨᘹ"))
            return None
        bstack11ll1ll1l1l_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack1ll1l1lllll_opy_.bstack11llll11l1l_opy_, {})
        if os.getenv(bstack1l1111_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡌࡉ࡙ࡖࡘࡖࡊ࡙ࠢᘺ"), bstack1l1111_opy_ (u"ࠢ࠲ࠤᘻ")) == bstack1l1111_opy_ (u"ࠣ࠳ࠥᘼ"):
            bstack11lll1lll11_opy_ = bstack1l1111_opy_ (u"ࠤ࠽ࠦᘽ").join((scope, fixturename))
            bstack11ll1lll111_opy_ = datetime.now(tz=timezone.utc)
            bstack11lllll11l1_opy_ = {
                bstack1l1111_opy_ (u"ࠥ࡯ࡪࡿࠢᘾ"): bstack11lll1lll11_opy_,
                bstack1l1111_opy_ (u"ࠦࡹࡧࡧࡴࠤᘿ"): bstack1ll1l1lllll_opy_.__11lll1llll1_opy_(request.node),
                bstack1l1111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࠨᙀ"): fixturedef,
                bstack1l1111_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᙁ"): scope,
                bstack1l1111_opy_ (u"ࠢࡵࡻࡳࡩࠧᙂ"): None,
            }
            try:
                if test_hook_state == bstack1ll1l111111_opy_.POST and callable(getattr(args[-1], bstack1l1111_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᙃ"), None)):
                    bstack11lllll11l1_opy_[bstack1l1111_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᙄ")] = TestFramework.bstack1l1l11l11ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1l111111_opy_.PRE:
                bstack11lllll11l1_opy_[bstack1l1111_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᙅ")] = uuid4().__str__()
                bstack11lllll11l1_opy_[bstack1ll1l1lllll_opy_.bstack11lllll1l1l_opy_] = bstack11ll1lll111_opy_
            elif test_hook_state == bstack1ll1l111111_opy_.POST:
                bstack11lllll11l1_opy_[bstack1ll1l1lllll_opy_.bstack11ll1ll1ll1_opy_] = bstack11ll1lll111_opy_
            if bstack11lll1lll11_opy_ in bstack11ll1ll1l1l_opy_:
                bstack11ll1ll1l1l_opy_[bstack11lll1lll11_opy_].update(bstack11lllll11l1_opy_)
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࠧᙆ") + str(bstack11ll1ll1l1l_opy_[bstack11lll1lll11_opy_]) + bstack1l1111_opy_ (u"ࠧࠨᙇ"))
            else:
                bstack11ll1ll1l1l_opy_[bstack11lll1lll11_opy_] = bstack11lllll11l1_opy_
                self.logger.debug(bstack1l1111_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡷࡨࡵࡰࡦ࠿ࡾࡷࡨࡵࡰࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡁࢀࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࢁࠥࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳ࠾ࠤᙈ") + str(len(bstack11ll1ll1l1l_opy_)) + bstack1l1111_opy_ (u"ࠢࠣᙉ"))
        TestFramework.bstack1lll11l1ll1_opy_(instance, bstack1ll1l1lllll_opy_.bstack11llll11l1l_opy_, bstack11ll1ll1l1l_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࡾࡰࡪࡴࠨࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠬࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᙊ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠤࠥᙋ"))
        return instance
    def __11lll1l1l1l_opy_(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1lll1l1llll_opy_.create_context(target)
        ob = bstack1ll111l1lll_opy_(ctx, self.bstack1l1ll1l1l1l_opy_, self.bstack11ll1l1l11l_opy_, test_framework_state)
        TestFramework.bstack11llll1llll_opy_(ob, {
            TestFramework.bstack1l1lll1ll1l_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1l1111l_opy_: context.test_framework_version,
            TestFramework.bstack11lll111ll1_opy_: [],
            bstack1ll1l1lllll_opy_.bstack11llll11l1l_opy_: {},
            bstack1ll1l1lllll_opy_.bstack11ll1ll1lll_opy_: {},
            bstack1ll1l1lllll_opy_.bstack11ll1ll1111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll11l1ll1_opy_(ob, TestFramework.bstack11lll1l1l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll11l1ll1_opy_(ob, TestFramework.bstack1l1ll1l11ll_opy_, context.platform_index)
        TestFramework.bstack1lll11ll1ll_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1111_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡨࡺࡸ࠯࡫ࡧࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᙌ") + str(TestFramework.bstack1lll11ll1ll_opy_.keys()) + bstack1l1111_opy_ (u"ࠦࠧᙍ"))
        return ob
    def bstack1l11ll11lll_opy_(self, instance: bstack1ll111l1lll_opy_, bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_]):
        bstack11lll1lllll_opy_ = (
            bstack1ll1l1lllll_opy_.bstack11ll1l11l1l_opy_
            if bstack1lll111llll_opy_[1] == bstack1ll1l111111_opy_.PRE
            else bstack1ll1l1lllll_opy_.bstack11ll1ll111l_opy_
        )
        hook = bstack1ll1l1lllll_opy_.bstack11lll11111l_opy_(instance, bstack11lll1lllll_opy_)
        entries = hook.get(TestFramework.bstack11lll1ll11l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack11lll111ll1_opy_, []))
        return entries
    def bstack1l11lllll11_opy_(self, instance: bstack1ll111l1lll_opy_, bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_]):
        bstack11lll1lllll_opy_ = (
            bstack1ll1l1lllll_opy_.bstack11ll1l11l1l_opy_
            if bstack1lll111llll_opy_[1] == bstack1ll1l111111_opy_.PRE
            else bstack1ll1l1lllll_opy_.bstack11ll1ll111l_opy_
        )
        bstack1ll1l1lllll_opy_.bstack11lllll1ll1_opy_(instance, bstack11lll1lllll_opy_)
        TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack11lll111ll1_opy_, []).clear()
    def bstack11ll1l1l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᙎ")
        global _1l11lll1ll1_opy_
        platform_index = os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᙏ")]
        bstack1l11ll1ll1l_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l1l11l11l1_opy_ + str(platform_index)), bstack11ll1l11l11_opy_)
        if not os.path.exists(bstack1l11ll1ll1l_opy_) or not os.path.isdir(bstack1l11ll1ll1l_opy_):
            self.logger.debug(bstack1l1111_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷࡷࠥࡺ࡯ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡾࢁࠧᙐ").format(bstack1l11ll1ll1l_opy_))
            return
        logs = hook.get(bstack1l1111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᙑ"), [])
        with os.scandir(bstack1l11ll1ll1l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11lll1ll1_opy_:
                    self.logger.info(bstack1l1111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᙒ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1111_opy_ (u"ࠥࠦᙓ")
                    log_entry = bstack1ll11l1l11l_opy_(
                        kind=bstack1l1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᙔ"),
                        message=bstack1l1111_opy_ (u"ࠧࠨᙕ"),
                        level=bstack1l1111_opy_ (u"ࠨࠢᙖ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11ll1l11l_opy_=entry.stat().st_size,
                        bstack1l11ll1l1ll_opy_=bstack1l1111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᙗ"),
                        bstack1llllll1_opy_=os.path.abspath(entry.path),
                        bstack11lll111111_opy_=hook.get(TestFramework.bstack11lll1l1lll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11lll1ll1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᙘ")]
        bstack11llll11ll1_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l1l11l11l1_opy_ + str(platform_index)), bstack11ll1l11l11_opy_, bstack11ll1l1111l_opy_)
        if not os.path.exists(bstack11llll11ll1_opy_) or not os.path.isdir(bstack11llll11ll1_opy_):
            self.logger.info(bstack1l1111_opy_ (u"ࠤࡑࡳࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧࠤࡦࡺ࠺ࠡࡽࢀࠦᙙ").format(bstack11llll11ll1_opy_))
        else:
            self.logger.info(bstack1l1111_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᙚ").format(bstack11llll11ll1_opy_))
            with os.scandir(bstack11llll11ll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11lll1ll1_opy_:
                        self.logger.info(bstack1l1111_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᙛ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1111_opy_ (u"ࠧࠨᙜ")
                        log_entry = bstack1ll11l1l11l_opy_(
                            kind=bstack1l1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᙝ"),
                            message=bstack1l1111_opy_ (u"ࠢࠣᙞ"),
                            level=bstack1l1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᙟ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11ll1l11l_opy_=entry.stat().st_size,
                            bstack1l11ll1l1ll_opy_=bstack1l1111_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᙠ"),
                            bstack1llllll1_opy_=os.path.abspath(entry.path),
                            bstack1l1l11lllll_opy_=hook.get(TestFramework.bstack11lll1l1lll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11lll1ll1_opy_.add(abs_path)
        hook[bstack1l1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᙡ")] = logs
    def bstack1l1l111l1ll_opy_(
        self,
        bstack1l11l1lll11_opy_: bstack1ll111l1lll_opy_,
        entries: List[bstack1ll11l1l11l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡘࡋࡓࡔࡋࡒࡒࡤࡏࡄࠣᙢ"))
        req.platform_index = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1ll1l11ll_opy_)
        req.client_worker_id = bstack1l1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᙣ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11l1lll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11l1lll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11l1lll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1lll1ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1l1l1111l_opy_)
            log_entry.uuid = entry.bstack11lll111111_opy_
            log_entry.test_framework_state = bstack1l11l1lll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᙤ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1111_opy_ (u"ࠢࠣᙥ")
            if entry.kind == bstack1l1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᙦ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l11l_opy_
                log_entry.file_path = entry.bstack1llllll1_opy_
        def bstack1l11ll1111l_opy_():
            bstack1ll1lll11l_opy_ = datetime.now()
            try:
                self.bstack1ll1111l1ll_opy_.LogCreatedEvent(req)
                bstack1l11l1lll11_opy_.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᙧ"), datetime.now() - bstack1ll1lll11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡻࡾࠤᙨ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll1llll1l_opy_.enqueue(bstack1l11ll1111l_opy_)
    def __11ll1lll1ll_opy_(self, instance) -> None:
        bstack1l1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡎࡲࡥࡩࡹࠠࡤࡷࡶࡸࡴࡳࠠࡵࡣࡪࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡤࡪࡥࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡬ࡦࡸࡨࡰࠥࡩࡵࡴࡶࡲࡱࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡪࡷࡵ࡭ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡹࡸࡺ࡯࡮ࡖࡤ࡫ࡒࡧ࡮ࡢࡩࡨࡶࠥࡧ࡮ࡥࠢࡸࡴࡩࡧࡴࡦࡵࠣࡸ࡭࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡶࡸࡦࡺࡥࠡࡷࡶ࡭ࡳ࡭ࠠࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᙩ")
        bstack11ll1l1llll_opy_ = {bstack1l1111_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᙪ"): bstack1ll1ll1ll11_opy_.bstack11ll1llll11_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11llll1llll_opy_(instance, bstack11ll1l1llll_opy_)
    @staticmethod
    def bstack11lll11111l_opy_(instance: bstack1ll111l1lll_opy_, bstack11lll1lllll_opy_: str):
        bstack11ll1l11lll_opy_ = (
            bstack1ll1l1lllll_opy_.bstack11ll1ll1lll_opy_
            if bstack11lll1lllll_opy_ == bstack1ll1l1lllll_opy_.bstack11ll1ll111l_opy_
            else bstack1ll1l1lllll_opy_.bstack11ll1ll1111_opy_
        )
        bstack11llll111ll_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11lll1lllll_opy_, None)
        bstack11llll1l1l1_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11ll1l11lll_opy_, None) if bstack11llll111ll_opy_ else None
        return (
            bstack11llll1l1l1_opy_[bstack11llll111ll_opy_][-1]
            if isinstance(bstack11llll1l1l1_opy_, dict) and len(bstack11llll1l1l1_opy_.get(bstack11llll111ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lllll1ll1_opy_(instance: bstack1ll111l1lll_opy_, bstack11lll1lllll_opy_: str):
        hook = bstack1ll1l1lllll_opy_.bstack11lll11111l_opy_(instance, bstack11lll1lllll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11lll1ll11l_opy_, []).clear()
    @staticmethod
    def __11llll1ll11_opy_(instance: bstack1ll111l1lll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᙫ"), None)):
            return
        if os.getenv(bstack1l1111_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᙬ"), bstack1l1111_opy_ (u"ࠣ࠳ࠥ᙭")) != bstack1l1111_opy_ (u"ࠤ࠴ࠦ᙮"):
            bstack1ll1l1lllll_opy_.logger.warning(bstack1l1111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᙯ"))
            return
        bstack11ll1lll11l_opy_ = {
            bstack1l1111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᙰ"): (bstack1ll1l1lllll_opy_.bstack11ll1l11l1l_opy_, bstack1ll1l1lllll_opy_.bstack11ll1ll1111_opy_),
            bstack1l1111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᙱ"): (bstack1ll1l1lllll_opy_.bstack11ll1ll111l_opy_, bstack1ll1l1lllll_opy_.bstack11ll1ll1lll_opy_),
        }
        for when in (bstack1l1111_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᙲ"), bstack1l1111_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᙳ"), bstack1l1111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᙴ")):
            bstack11llll1l1ll_opy_ = args[1].get_records(when)
            if not bstack11llll1l1ll_opy_:
                continue
            records = [
                bstack1ll11l1l11l_opy_(
                    kind=TestFramework.bstack1l1l11ll11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1111_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᙵ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1111_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᙶ")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll1l1ll_opy_
                if isinstance(getattr(r, bstack1l1111_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᙷ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll1l1l111_opy_, bstack11ll1l11lll_opy_ = bstack11ll1lll11l_opy_.get(when, (None, None))
            bstack11lll1lll1l_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11ll1l1l111_opy_, None) if bstack11ll1l1l111_opy_ else None
            bstack11llll1l1l1_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, bstack11ll1l11lll_opy_, None) if bstack11lll1lll1l_opy_ else None
            if isinstance(bstack11llll1l1l1_opy_, dict) and len(bstack11llll1l1l1_opy_.get(bstack11lll1lll1l_opy_, [])) > 0:
                hook = bstack11llll1l1l1_opy_[bstack11lll1lll1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11lll1ll11l_opy_ in hook:
                    hook[TestFramework.bstack11lll1ll11l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack11lll111ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1lll1l1_opy_(test) -> Dict[str, Any]:
        bstack1l1llll1ll_opy_ = bstack1ll1l1lllll_opy_.__11lll1ll1l1_opy_(test.location) if hasattr(test, bstack1l1111_opy_ (u"ࠧࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᙸ")) else getattr(test, bstack1l1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᙹ"), None)
        test_name = test.name if hasattr(test, bstack1l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᙺ")) else None
        bstack11ll1lllll1_opy_ = test.fspath.strpath if hasattr(test, bstack1l1111_opy_ (u"ࠣࡨࡶࡴࡦࡺࡨࠣᙻ")) and test.fspath else None
        if not bstack1l1llll1ll_opy_ or not test_name or not bstack11ll1lllll1_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1111_opy_ (u"ࠤࡲࡦ࡯ࠨᙼ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11ll1l111ll_opy_ = []
        try:
            bstack11ll1l111ll_opy_ = bstack1lll11ll11_opy_.bstack11111l1111_opy_(test)
        except:
            bstack1ll1l1lllll_opy_.logger.warning(bstack1l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴ࠮ࠣࡸࡪࡹࡴࠡࡵࡦࡳࡵ࡫ࡳࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡵࡩࡸࡵ࡬ࡷࡧࡧࠤ࡮ࡴࠠࡄࡎࡌࠦᙽ"))
        return {
            TestFramework.bstack1l1lll111ll_opy_: uuid4().__str__(),
            TestFramework.bstack11lllll111l_opy_: bstack1l1llll1ll_opy_,
            TestFramework.bstack1l1ll11111l_opy_: test_name,
            TestFramework.bstack1l11l1l1111_opy_: getattr(test, bstack1l1111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᙾ"), None),
            TestFramework.bstack11llll1l11l_opy_: bstack11ll1lllll1_opy_,
            TestFramework.bstack11lll11l1l1_opy_: bstack1ll1l1lllll_opy_.__11lll1llll1_opy_(test),
            TestFramework.bstack11ll1l1ll11_opy_: code,
            TestFramework.bstack1l111l1l1l1_opy_: TestFramework.bstack11lll1l111l_opy_,
            TestFramework.bstack1l111111lll_opy_: bstack1l1llll1ll_opy_,
            TestFramework.bstack11ll1l111l1_opy_: bstack11ll1l111ll_opy_
        }
    @staticmethod
    def __11lll1llll1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1111_opy_ (u"ࠧࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠥᙿ"), [])
            markers.extend([getattr(m, bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ "), None) for m in own_markers if getattr(m, bstack1l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᚁ"), None)])
            current = getattr(current, bstack1l1111_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᚂ"), None)
        return markers
    @staticmethod
    def __11lll1ll1l1_opy_(location):
        return bstack1l1111_opy_ (u"ࠤ࠽࠾ࠧᚃ").join(filter(lambda x: isinstance(x, str), location))