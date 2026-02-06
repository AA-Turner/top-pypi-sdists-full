# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1ll1lllll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1ll1lll_opy_ import bstack11ll11lll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll11111l1l_opy_,
    bstack1ll11111ll1_opy_,
    bstack1ll11l1l11l_opy_,
    bstack11lll1l1lll_opy_,
    bstack1ll1l11ll11_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l11lll1lll_opy_
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll11ll11l1_opy_ import bstack1ll1l1l111l_opy_
from bstack_utils.bstack1111l1lll1_opy_ import bstack1l1l11llll_opy_
bstack1l1l11l1ll1_opy_ = bstack1l11lll1lll_opy_()
bstack11lll1l1l1l_opy_ = 1.0
bstack1l11l1ll11l_opy_ = bstack11lllll_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᘆ")
bstack11ll11ll111_opy_ = bstack11lllll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᘇ")
bstack11ll11ll11l_opy_ = bstack11lllll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᘈ")
bstack11ll11l1lll_opy_ = bstack11lllll_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᘉ")
bstack11ll11l11ll_opy_ = bstack11lllll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᘊ")
_1l11ll1lll1_opy_ = set()
class bstack1ll1ll111l1_opy_(TestFramework):
    bstack11lll111l11_opy_ = bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᘋ")
    bstack11lll1111l1_opy_ = bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᘌ")
    bstack11lll11l11l_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᘍ")
    bstack11llll11ll1_opy_ = bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᘎ")
    bstack11ll11llll1_opy_ = bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᘏ")
    bstack11llll111l1_opy_: bool
    bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_  = None
    bstack1ll1l1l1ll1_opy_ = None
    bstack11ll11ll1ll_opy_ = [
        bstack1ll11111l1l_opy_.BEFORE_ALL,
        bstack1ll11111l1l_opy_.AFTER_ALL,
        bstack1ll11111l1l_opy_.BEFORE_EACH,
        bstack1ll11111l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11llll1ll11_opy_: Dict[str, str],
        bstack1l1ll1l111l_opy_: List[str]=[bstack11lllll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᘐ")],
        bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_=None,
        bstack1ll1l1l1ll1_opy_=None
    ):
        super().__init__(bstack1l1ll1l111l_opy_, bstack11llll1ll11_opy_, bstack1lll11ll111_opy_)
        self.bstack11llll111l1_opy_ = any(bstack11lllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᘑ") in item.lower() for item in bstack1l1ll1l111l_opy_)
        self.bstack1ll1l1l1ll1_opy_ = bstack1ll1l1l1ll1_opy_
    def track_event(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll11111l1l_opy_.TEST or test_framework_state in bstack1ll1ll111l1_opy_.bstack11ll11ll1ll_opy_:
            bstack11ll11lll1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll11111l1l_opy_.NONE:
            self.logger.warning(bstack11lllll_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᘒ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠤࠥᘓ"))
            return
        if not self.bstack11llll111l1_opy_:
            self.logger.warning(bstack11lllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᘔ") + str(str(self.bstack1l1ll1l111l_opy_)) + bstack11lllll_opy_ (u"ࠦࠧᘕ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11lllll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᘖ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᘗ"))
            return
        instance = self.__11ll1lll1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᘘ") + str(args) + bstack11lllll_opy_ (u"ࠣࠤᘙ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1ll111l1_opy_.bstack11ll11ll1ll_opy_:
                bstack1ll11111l_opy_ = bstack11lllll_opy_ (u"ࠤࠥᘚ")
                name = bstack11lllll_opy_ (u"ࠥࠦᘛ")
                if (test_hook_state == bstack1ll11l1l11l_opy_.PRE):
                    bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack11ll11l1ll1_opy_.value)
                    name = str(EVENTS.bstack11ll11l1ll1_opy_.name)+bstack11lllll_opy_ (u"ࠦ࠿ࠨᘜ")+str(test_framework_state.name)
                else:
                    bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack11ll11l1l11_opy_.value)
                    name = str(EVENTS.bstack11ll11l1l11_opy_.name)+bstack11lllll_opy_ (u"ࠧࡀࠢᘝ")+str(test_framework_state.name)
                TestFramework.bstack11lll1lll1l_opy_(instance, name, bstack1ll11111l_opy_)
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᘞ").format(e))
        try:
            if not TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack11ll1l111l1_opy_) and test_hook_state == bstack1ll11l1l11l_opy_.PRE:
                test = bstack1ll1ll111l1_opy_.__11ll1lll11l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᘟ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠣࠤᘠ"))
            if test_framework_state == bstack1ll11111l1l_opy_.TEST:
                if test_hook_state == bstack1ll11l1l11l_opy_.PRE and not TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11ll11l11_opy_):
                    TestFramework.bstack1lll1ll1lll_opy_(instance, TestFramework.bstack1l11ll11l11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lllll_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᘡ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠥࠦᘢ"))
                elif test_hook_state == bstack1ll11l1l11l_opy_.POST and not TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_):
                    TestFramework.bstack1lll1ll1lll_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11lllll_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᘣ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠧࠨᘤ"))
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG and test_hook_state == bstack1ll11l1l11l_opy_.POST:
                bstack1ll1ll111l1_opy_.__11llll111ll_opy_(instance, *args)
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG_REPORT and test_hook_state == bstack1ll11l1l11l_opy_.POST:
                self.__11llll11l11_opy_(instance, *args)
                self.__11lll1l11l1_opy_(instance)
            elif test_framework_state in bstack1ll1ll111l1_opy_.bstack11ll11ll1ll_opy_:
                self.__11ll1l1111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11lllll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᘥ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠢࠣᘦ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1lll1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1ll111l1_opy_.bstack11ll11ll1ll_opy_:
                bstack1ll11111l_opy_ = bstack11lllll_opy_ (u"ࠣࠤᘧ")
                name = bstack11lllll_opy_ (u"ࠤࠥᘨ")
                if (test_hook_state == bstack1ll11l1l11l_opy_.PRE):
                    name = str(EVENTS.bstack11ll11l1ll1_opy_.name)+bstack11lllll_opy_ (u"ࠥ࠾ࠧᘩ")+str(test_framework_state.name)
                    bstack1ll11111l_opy_ = TestFramework.bstack11ll1lll111_opy_(instance, name)
                    bstack1lll11l1ll_opy_.end(EVENTS.bstack11ll11l1ll1_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘪ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᘫ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11ll11l1l11_opy_.name)+bstack11lllll_opy_ (u"ࠨ࠺ࠣᘬ")+str(test_framework_state.name)
                    bstack1ll11111l_opy_ = TestFramework.bstack11ll1lll111_opy_(instance, name)
                    bstack1lll11l1ll_opy_.end(EVENTS.bstack11ll11l1l11_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘭ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘮ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᘯ").format(e))
    def bstack1l1l11ll1l1_opy_(self):
        return self.bstack11llll111l1_opy_
    def __11ll1l1l1l1_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11lllll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᘰ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1l11ll11l_opy_(rep, [bstack11lllll_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᘱ"), bstack11lllll_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᘲ"), bstack11lllll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᘳ"), bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᘴ"), bstack11lllll_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᘵ"), bstack11lllll_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᘶ")])
        return None
    def __11llll11l11_opy_(self, instance: bstack1ll11111ll1_opy_, *args):
        result = self.__11ll1l1l1l1_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llll1111ll_opy_ = None
        if result.get(bstack11lllll_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᘷ"), None) == bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᘸ") and len(args) > 1 and getattr(args[1], bstack11lllll_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᘹ"), None) is not None:
            failure = [{bstack11lllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᘺ"): [args[1].excinfo.exconly(), result.get(bstack11lllll_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᘻ"), None)]}]
            bstack1llll1111ll_opy_ = bstack11lllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᘼ") if bstack11lllll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᘽ") in getattr(args[1].excinfo, bstack11lllll_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᘾ"), bstack11lllll_opy_ (u"ࠦࠧᘿ")) else bstack11lllll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᙀ")
        bstack11lll111lll_opy_ = result.get(bstack11lllll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᙁ"), TestFramework.bstack11lll1ll111_opy_)
        if bstack11lll111lll_opy_ != TestFramework.bstack11lll1ll111_opy_:
            TestFramework.bstack1lll1ll1lll_opy_(instance, TestFramework.bstack1l1l111ll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll11lll11_opy_(instance, {
            TestFramework.bstack1l111ll1111_opy_: failure,
            TestFramework.bstack11lll111ll1_opy_: bstack1llll1111ll_opy_,
            TestFramework.bstack1l111l1ll11_opy_: bstack11lll111lll_opy_,
        })
    def __11ll1lll1l1_opy_(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll11111l1l_opy_.SETUP_FIXTURE:
            instance = self.__11lll11l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1ll11ll_opy_ bstack11ll1ll1ll1_opy_ this to be bstack11lllll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᙂ")
            if test_framework_state == bstack1ll11111l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11lll11l111_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11lllll_opy_ (u"ࠣࡰࡲࡨࡪࠨᙃ"), None), bstack11lllll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᙄ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11lllll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᙅ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll111ll1l_opy_(target) if target else None
        return instance
    def __11ll1l1111l_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11lll1l111l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack1ll1ll111l1_opy_.bstack11lll1111l1_opy_, {})
        if not key in bstack11lll1l111l_opy_:
            bstack11lll1l111l_opy_[key] = []
        bstack11llll1111l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack1ll1ll111l1_opy_.bstack11lll11l11l_opy_, {})
        if not key in bstack11llll1111l_opy_:
            bstack11llll1111l_opy_[key] = []
        bstack11ll1ll1l1l_opy_ = {
            bstack1ll1ll111l1_opy_.bstack11lll1111l1_opy_: bstack11lll1l111l_opy_,
            bstack1ll1ll111l1_opy_.bstack11lll11l11l_opy_: bstack11llll1111l_opy_,
        }
        if test_hook_state == bstack1ll11l1l11l_opy_.PRE:
            hook = {
                bstack11lllll_opy_ (u"ࠦࡰ࡫ࡹࠣᙆ"): key,
                TestFramework.bstack11ll1l11l1l_opy_: uuid4().__str__(),
                TestFramework.bstack11lll1l1ll1_opy_: TestFramework.bstack11lll11111l_opy_,
                TestFramework.bstack11ll1l11lll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll1l11l11_opy_: [],
                TestFramework.bstack11lll1ll1ll_opy_: args[1] if len(args) > 1 else bstack11lllll_opy_ (u"ࠬ࠭ᙇ"),
                TestFramework.bstack11lll11llll_opy_: bstack1ll1l1l111l_opy_.bstack11ll1l11111_opy_()
            }
            bstack11lll1l111l_opy_[key].append(hook)
            bstack11ll1ll1l1l_opy_[bstack1ll1ll111l1_opy_.bstack11llll11ll1_opy_] = key
        elif test_hook_state == bstack1ll11l1l11l_opy_.POST:
            bstack11ll11lllll_opy_ = bstack11lll1l111l_opy_.get(key, [])
            hook = bstack11ll11lllll_opy_.pop() if bstack11ll11lllll_opy_ else None
            if hook:
                result = self.__11ll1l1l1l1_opy_(*args)
                if result:
                    bstack11ll1l1ll11_opy_ = result.get(bstack11lllll_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᙈ"), TestFramework.bstack11lll11111l_opy_)
                    if bstack11ll1l1ll11_opy_ != TestFramework.bstack11lll11111l_opy_:
                        hook[TestFramework.bstack11lll1l1ll1_opy_] = bstack11ll1l1ll11_opy_
                hook[TestFramework.bstack11lll111l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lll11llll_opy_]= bstack1ll1l1l111l_opy_.bstack11ll1l11111_opy_()
                self.bstack11lll1ll11l_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l1l11l_opy_, [])
                if logs: self.bstack1l1l111lll1_opy_(instance, logs)
                bstack11llll1111l_opy_[key].append(hook)
                bstack11ll1ll1l1l_opy_[bstack1ll1ll111l1_opy_.bstack11ll11llll1_opy_] = key
        TestFramework.bstack11ll11lll11_opy_(instance, bstack11ll1ll1l1l_opy_)
        self.logger.debug(bstack11lllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᙉ") + str(bstack11llll1111l_opy_) + bstack11lllll_opy_ (u"ࠣࠤᙊ"))
    def __11lll11l1l1_opy_(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1l11ll11l_opy_(args[0], [bstack11lllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᙋ"), bstack11lllll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᙌ"), bstack11lllll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᙍ"), bstack11lllll_opy_ (u"ࠧ࡯ࡤࡴࠤᙎ"), bstack11lllll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᙏ"), bstack11lllll_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᙐ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11lllll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᙑ")) else fixturedef.get(bstack11lllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᙒ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11lllll_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᙓ")) else None
        node = request.node if hasattr(request, bstack11lllll_opy_ (u"ࠦࡳࡵࡤࡦࠤᙔ")) else None
        target = request.node.nodeid if hasattr(node, bstack11lllll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᙕ")) else None
        baseid = fixturedef.get(bstack11lllll_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᙖ"), None) or bstack11lllll_opy_ (u"ࠢࠣᙗ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11lllll_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᙘ")):
            target = bstack1ll1ll111l1_opy_.__11ll1l111ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11lllll_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᙙ")) else None
            if target and not TestFramework.bstack1lll111ll1l_opy_(target):
                self.__11lll11l111_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11lllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᙚ") + str(test_hook_state) + bstack11lllll_opy_ (u"ࠦࠧᙛ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11lllll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᙜ") + str(target) + bstack11lllll_opy_ (u"ࠨࠢᙝ"))
            return None
        instance = TestFramework.bstack1lll111ll1l_opy_(target)
        if not instance:
            self.logger.warning(bstack11lllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᙞ") + str(target) + bstack11lllll_opy_ (u"ࠣࠤᙟ"))
            return None
        bstack11ll1l1l1ll_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack1ll1ll111l1_opy_.bstack11lll111l11_opy_, {})
        if os.getenv(bstack11lllll_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᙠ"), bstack11lllll_opy_ (u"ࠥ࠵ࠧᙡ")) == bstack11lllll_opy_ (u"ࠦ࠶ࠨᙢ"):
            bstack11ll1ll11l1_opy_ = bstack11lllll_opy_ (u"ࠧࡀࠢᙣ").join((scope, fixturename))
            bstack11llll11lll_opy_ = datetime.now(tz=timezone.utc)
            bstack11lll1111ll_opy_ = {
                bstack11lllll_opy_ (u"ࠨ࡫ࡦࡻࠥᙤ"): bstack11ll1ll11l1_opy_,
                bstack11lllll_opy_ (u"ࠢࡵࡣࡪࡷࠧᙥ"): bstack1ll1ll111l1_opy_.__11ll1lllll1_opy_(request.node),
                bstack11lllll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᙦ"): fixturedef,
                bstack11lllll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᙧ"): scope,
                bstack11lllll_opy_ (u"ࠥࡸࡾࡶࡥࠣᙨ"): None,
            }
            try:
                if test_hook_state == bstack1ll11l1l11l_opy_.POST and callable(getattr(args[-1], bstack11lllll_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᙩ"), None)):
                    bstack11lll1111ll_opy_[bstack11lllll_opy_ (u"ࠧࡺࡹࡱࡧࠥᙪ")] = TestFramework.bstack1l11llll1ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll11l1l11l_opy_.PRE:
                bstack11lll1111ll_opy_[bstack11lllll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᙫ")] = uuid4().__str__()
                bstack11lll1111ll_opy_[bstack1ll1ll111l1_opy_.bstack11ll1l11lll_opy_] = bstack11llll11lll_opy_
            elif test_hook_state == bstack1ll11l1l11l_opy_.POST:
                bstack11lll1111ll_opy_[bstack1ll1ll111l1_opy_.bstack11lll111l1l_opy_] = bstack11llll11lll_opy_
            if bstack11ll1ll11l1_opy_ in bstack11ll1l1l1ll_opy_:
                bstack11ll1l1l1ll_opy_[bstack11ll1ll11l1_opy_].update(bstack11lll1111ll_opy_)
                self.logger.debug(bstack11lllll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᙬ") + str(bstack11ll1l1l1ll_opy_[bstack11ll1ll11l1_opy_]) + bstack11lllll_opy_ (u"ࠣࠤ᙭"))
            else:
                bstack11ll1l1l1ll_opy_[bstack11ll1ll11l1_opy_] = bstack11lll1111ll_opy_
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧ᙮") + str(len(bstack11ll1l1l1ll_opy_)) + bstack11lllll_opy_ (u"ࠥࠦᙯ"))
        TestFramework.bstack1lll1ll1lll_opy_(instance, bstack1ll1ll111l1_opy_.bstack11lll111l11_opy_, bstack11ll1l1l1ll_opy_)
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᙰ") + str(instance.ref()) + bstack11lllll_opy_ (u"ࠧࠨᙱ"))
        return instance
    def __11lll11l111_opy_(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1lllll1l_opy_.create_context(target)
        ob = bstack1ll11111ll1_opy_(ctx, self.bstack1l1ll1l111l_opy_, self.bstack11llll1ll11_opy_, test_framework_state)
        TestFramework.bstack11ll11lll11_opy_(ob, {
            TestFramework.bstack1l1ll111ll1_opy_: context.test_framework_name,
            TestFramework.bstack1l11ll1ll1l_opy_: context.test_framework_version,
            TestFramework.bstack11llll11l1l_opy_: [],
            bstack1ll1ll111l1_opy_.bstack11lll111l11_opy_: {},
            bstack1ll1ll111l1_opy_.bstack11lll11l11l_opy_: {},
            bstack1ll1ll111l1_opy_.bstack11lll1111l1_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll1ll1lll_opy_(ob, TestFramework.bstack11ll1ll111l_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll1ll1lll_opy_(ob, TestFramework.bstack1l1l1lllll1_opy_, context.platform_index)
        TestFramework.bstack1ll1llll11l_opy_[ctx.id] = ob
        self.logger.debug(bstack11lllll_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᙲ") + str(TestFramework.bstack1ll1llll11l_opy_.keys()) + bstack11lllll_opy_ (u"ࠢࠣᙳ"))
        return ob
    def bstack1l11ll1111l_opy_(self, instance: bstack1ll11111ll1_opy_, bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_]):
        bstack11ll1l1l111_opy_ = (
            bstack1ll1ll111l1_opy_.bstack11llll11ll1_opy_
            if bstack1lll1l11lll_opy_[1] == bstack1ll11l1l11l_opy_.PRE
            else bstack1ll1ll111l1_opy_.bstack11ll11llll1_opy_
        )
        hook = bstack1ll1ll111l1_opy_.bstack11lll1ll1l1_opy_(instance, bstack11ll1l1l111_opy_)
        entries = hook.get(TestFramework.bstack11ll1l11l11_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11llll11l1l_opy_, []))
        return entries
    def bstack1l1l11111l1_opy_(self, instance: bstack1ll11111ll1_opy_, bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_]):
        bstack11ll1l1l111_opy_ = (
            bstack1ll1ll111l1_opy_.bstack11llll11ll1_opy_
            if bstack1lll1l11lll_opy_[1] == bstack1ll11l1l11l_opy_.PRE
            else bstack1ll1ll111l1_opy_.bstack11ll11llll1_opy_
        )
        bstack1ll1ll111l1_opy_.bstack11lll1l11ll_opy_(instance, bstack11ll1l1l111_opy_)
        TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11llll11l1l_opy_, []).clear()
    def bstack11lll1ll11l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᙴ")
        global _1l11ll1lll1_opy_
        platform_index = os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᙵ")]
        bstack1l11ll1l11l_opy_ = os.path.join(bstack1l1l11l1ll1_opy_, (bstack1l11l1ll11l_opy_ + str(platform_index)), bstack11ll11l1lll_opy_)
        if not os.path.exists(bstack1l11ll1l11l_opy_) or not os.path.isdir(bstack1l11ll1l11l_opy_):
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᙶ").format(bstack1l11ll1l11l_opy_))
            return
        logs = hook.get(bstack11lllll_opy_ (u"ࠦࡱࡵࡧࡴࠤᙷ"), [])
        with os.scandir(bstack1l11ll1l11l_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11ll1lll1_opy_:
                    self.logger.info(bstack11lllll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᙸ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11lllll_opy_ (u"ࠨࠢᙹ")
                    log_entry = bstack1ll1l11ll11_opy_(
                        kind=bstack11lllll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᙺ"),
                        message=bstack11lllll_opy_ (u"ࠣࠤᙻ"),
                        level=bstack11lllll_opy_ (u"ࠤࠥᙼ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l111l11l_opy_=entry.stat().st_size,
                        bstack1l1l11l1l1l_opy_=bstack11lllll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᙽ"),
                        bstack1111ll1_opy_=os.path.abspath(entry.path),
                        bstack11llll1l1ll_opy_=hook.get(TestFramework.bstack11ll1l11l1l_opy_)
                    )
                    logs.append(log_entry)
                    _1l11ll1lll1_opy_.add(abs_path)
        platform_index = os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᙾ")]
        bstack11ll1l1lll1_opy_ = os.path.join(bstack1l1l11l1ll1_opy_, (bstack1l11l1ll11l_opy_ + str(platform_index)), bstack11ll11l1lll_opy_, bstack11ll11l11ll_opy_)
        if not os.path.exists(bstack11ll1l1lll1_opy_) or not os.path.isdir(bstack11ll1l1lll1_opy_):
            self.logger.info(bstack11lllll_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᙿ").format(bstack11ll1l1lll1_opy_))
        else:
            self.logger.info(bstack11lllll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧ ").format(bstack11ll1l1lll1_opy_))
            with os.scandir(bstack11ll1l1lll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11ll1lll1_opy_:
                        self.logger.info(bstack11lllll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᚁ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11lllll_opy_ (u"ࠣࠤᚂ")
                        log_entry = bstack1ll1l11ll11_opy_(
                            kind=bstack11lllll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᚃ"),
                            message=bstack11lllll_opy_ (u"ࠥࠦᚄ"),
                            level=bstack11lllll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᚅ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l111l11l_opy_=entry.stat().st_size,
                            bstack1l1l11l1l1l_opy_=bstack11lllll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᚆ"),
                            bstack1111ll1_opy_=os.path.abspath(entry.path),
                            bstack1l11lll1111_opy_=hook.get(TestFramework.bstack11ll1l11l1l_opy_)
                        )
                        logs.append(log_entry)
                        _1l11ll1lll1_opy_.add(abs_path)
        hook[bstack11lllll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᚇ")] = logs
    def bstack1l1l111lll1_opy_(
        self,
        bstack1l1l111l1ll_opy_: bstack1ll11111ll1_opy_,
        entries: List[bstack1ll1l11ll11_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᚈ"))
        req.platform_index = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1l1lllll1_opy_)
        req.client_worker_id = bstack11lllll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᚉ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1l111l1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l111l1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l111l1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1ll111ll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l11ll1ll1l_opy_)
            log_entry.uuid = entry.bstack11llll1l1ll_opy_
            log_entry.test_framework_state = bstack1l1l111l1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lllll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᚊ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11lllll_opy_ (u"ࠥࠦᚋ")
            if entry.kind == bstack11lllll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᚌ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l111l11l_opy_
                log_entry.file_path = entry.bstack1111ll1_opy_
        def bstack1l1l11l11ll_opy_():
            bstack1l1111l111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1ll1_opy_.LogCreatedEvent(req)
                bstack1l1l111l1ll_opy_.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᚍ"), datetime.now() - bstack1l1111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lllll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡾࢁࠧᚎ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll11ll111_opy_.enqueue(bstack1l1l11l11ll_opy_)
    def __11lll1l11l1_opy_(self, instance) -> None:
        bstack11lllll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡑࡵࡡࡥࡵࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡳࡧࡤࡸࡪࡹࠠࡢࠢࡧ࡭ࡨࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡥࡸࡷࡹࡵ࡭ࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡶࡪࡺࡲࡪࡧࡹࡩࡩࠦࡦࡳࡱࡰࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡣࡱࡨࠥࡻࡰࡥࡣࡷࡩࡸࠦࡴࡩࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡴࡢࡶࡨࠤࡺࡹࡩ࡯ࡩࠣࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᚏ")
        bstack11ll1ll1l1l_opy_ = {bstack11lllll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᚐ"): bstack1ll1l1l111l_opy_.bstack11ll1l11111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll11lll11_opy_(instance, bstack11ll1ll1l1l_opy_)
    @staticmethod
    def bstack11lll1ll1l1_opy_(instance: bstack1ll11111ll1_opy_, bstack11ll1l1l111_opy_: str):
        bstack11llll1l11l_opy_ = (
            bstack1ll1ll111l1_opy_.bstack11lll11l11l_opy_
            if bstack11ll1l1l111_opy_ == bstack1ll1ll111l1_opy_.bstack11ll11llll1_opy_
            else bstack1ll1ll111l1_opy_.bstack11lll1111l1_opy_
        )
        bstack11lll11lll1_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11ll1l1l111_opy_, None)
        bstack11ll1l1ll1l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11llll1l11l_opy_, None) if bstack11lll11lll1_opy_ else None
        return (
            bstack11ll1l1ll1l_opy_[bstack11lll11lll1_opy_][-1]
            if isinstance(bstack11ll1l1ll1l_opy_, dict) and len(bstack11ll1l1ll1l_opy_.get(bstack11lll11lll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11lll1l11ll_opy_(instance: bstack1ll11111ll1_opy_, bstack11ll1l1l111_opy_: str):
        hook = bstack1ll1ll111l1_opy_.bstack11lll1ll1l1_opy_(instance, bstack11ll1l1l111_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll1l11l11_opy_, []).clear()
    @staticmethod
    def __11llll111ll_opy_(instance: bstack1ll11111ll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11lllll_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡥࡲࡶࡩࡹࠢᚑ"), None)):
            return
        if os.getenv(bstack11lllll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡏࡓࡌ࡙ࠢᚒ"), bstack11lllll_opy_ (u"ࠦ࠶ࠨᚓ")) != bstack11lllll_opy_ (u"ࠧ࠷ࠢᚔ"):
            bstack1ll1ll111l1_opy_.logger.warning(bstack11lllll_opy_ (u"ࠨࡩࡨࡰࡲࡶ࡮ࡴࡧࠡࡥࡤࡴࡱࡵࡧࠣᚕ"))
            return
        bstack11lll11l1ll_opy_ = {
            bstack11lllll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᚖ"): (bstack1ll1ll111l1_opy_.bstack11llll11ll1_opy_, bstack1ll1ll111l1_opy_.bstack11lll1111l1_opy_),
            bstack11lllll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᚗ"): (bstack1ll1ll111l1_opy_.bstack11ll11llll1_opy_, bstack1ll1ll111l1_opy_.bstack11lll11l11l_opy_),
        }
        for when in (bstack11lllll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᚘ"), bstack11lllll_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᚙ"), bstack11lllll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᚚ")):
            bstack11llll1l111_opy_ = args[1].get_records(when)
            if not bstack11llll1l111_opy_:
                continue
            records = [
                bstack1ll1l11ll11_opy_(
                    kind=TestFramework.bstack1l11ll111l1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11lllll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠣ᚛")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11lllll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠢ᚜")) and r.created
                        else None
                    ),
                )
                for r in bstack11llll1l111_opy_
                if isinstance(getattr(r, bstack11lllll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ᚝"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11llll11111_opy_, bstack11llll1l11l_opy_ = bstack11lll11l1ll_opy_.get(when, (None, None))
            bstack11lll111111_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11llll11111_opy_, None) if bstack11llll11111_opy_ else None
            bstack11ll1l1ll1l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, bstack11llll1l11l_opy_, None) if bstack11lll111111_opy_ else None
            if isinstance(bstack11ll1l1ll1l_opy_, dict) and len(bstack11ll1l1ll1l_opy_.get(bstack11lll111111_opy_, [])) > 0:
                hook = bstack11ll1l1ll1l_opy_[bstack11lll111111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll1l11l11_opy_ in hook:
                    hook[TestFramework.bstack11ll1l11l11_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack11llll11l1l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1lll11l_opy_(test) -> Dict[str, Any]:
        bstack1ll11llll1_opy_ = bstack1ll1ll111l1_opy_.__11ll1l111ll_opy_(test.location) if hasattr(test, bstack11lllll_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥ᚞")) else getattr(test, bstack11lllll_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᚟"), None)
        test_name = test.name if hasattr(test, bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᚠ")) else None
        bstack11lll1l1111_opy_ = test.fspath.strpath if hasattr(test, bstack11lllll_opy_ (u"ࠦ࡫ࡹࡰࡢࡶ࡫ࠦᚡ")) and test.fspath else None
        if not bstack1ll11llll1_opy_ or not test_name or not bstack11lll1l1111_opy_:
            return None
        code = None
        if hasattr(test, bstack11lllll_opy_ (u"ࠧࡵࡢ࡫ࠤᚢ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11ll11ll1l1_opy_ = []
        try:
            bstack11ll11ll1l1_opy_ = bstack1l1l11llll_opy_.bstack1111111lll_opy_(test)
        except:
            bstack1ll1ll111l1_opy_.logger.warning(bstack11lllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷ࠱ࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡸࡥࡴࡱ࡯ࡺࡪࡪࠠࡪࡰࠣࡇࡑࡏࠢᚣ"))
        return {
            TestFramework.bstack1l1lll1l111_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1l111l1_opy_: bstack1ll11llll1_opy_,
            TestFramework.bstack1l1lll11111_opy_: test_name,
            TestFramework.bstack1l11l1l1111_opy_: getattr(test, bstack11lllll_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᚤ"), None),
            TestFramework.bstack11ll1ll1lll_opy_: bstack11lll1l1111_opy_,
            TestFramework.bstack11lll11ll11_opy_: bstack1ll1ll111l1_opy_.__11ll1lllll1_opy_(test),
            TestFramework.bstack11lll1l1l11_opy_: code,
            TestFramework.bstack1l111l1ll11_opy_: TestFramework.bstack11lll1ll111_opy_,
            TestFramework.bstack11lllllll11_opy_: bstack1ll11llll1_opy_,
            TestFramework.bstack11ll11l1l1l_opy_: bstack11ll11ll1l1_opy_
        }
    @staticmethod
    def __11ll1lllll1_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11lllll_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᚥ"), [])
            markers.extend([getattr(m, bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᚦ"), None) for m in own_markers if getattr(m, bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᚧ"), None)])
            current = getattr(current, bstack11lllll_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᚨ"), None)
        return markers
    @staticmethod
    def __11ll1l111ll_opy_(location):
        return bstack11lllll_opy_ (u"ࠧࡀ࠺ࠣᚩ").join(filter(lambda x: isinstance(x, str), location))