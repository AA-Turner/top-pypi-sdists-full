# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l111ll_opy_ import bstack11ll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1l1lllllll1_opy_,
    bstack1ll11l111ll_opy_,
    bstack1l1lllll1ll_opy_,
    bstack11ll1l1llll_opy_,
    bstack1l1lll1l11l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l11l11l11l_opy_
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l111_opy_ import bstack1ll11lll1l1_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack11l1ll111l_opy_
bstack1l11l1ll11l_opy_ = bstack1l11l11l11l_opy_()
bstack11ll1111111_opy_ = 1.0
bstack1l111l1l1l1_opy_ = bstack11l11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᚰ")
bstack11l1ll11l11_opy_ = bstack11l11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᚱ")
bstack11l1ll111ll_opy_ = bstack11l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᚲ")
bstack11l1ll11l1l_opy_ = bstack11l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᚳ")
bstack11l1ll111l1_opy_ = bstack11l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᚴ")
_1l111lll1ll_opy_ = set()
class bstack1ll111lll1l_opy_(TestFramework):
    bstack11l1lllll11_opy_ = bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᚵ")
    bstack11l1lll11ll_opy_ = bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᚶ")
    bstack11ll111111l_opy_ = bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᚷ")
    bstack11ll1l11111_opy_ = bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᚸ")
    bstack11ll1ll1l1l_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᚹ")
    bstack11ll11l1ll1_opy_: bool
    bstack1lll111lll1_opy_: bstack1lll11l111l_opy_  = None
    bstack1ll1l1l1lll_opy_ = None
    bstack11l1ll1l1l1_opy_ = [
        bstack1l1lllllll1_opy_.BEFORE_ALL,
        bstack1l1lllllll1_opy_.AFTER_ALL,
        bstack1l1lllllll1_opy_.BEFORE_EACH,
        bstack1l1lllllll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll111lll1_opy_: Dict[str, str],
        bstack1l1l1l11l1l_opy_: List[str]=[bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᚺ")],
        bstack1lll111lll1_opy_: bstack1lll11l111l_opy_=None,
        bstack1ll1l1l1lll_opy_=None
    ):
        super().__init__(bstack1l1l1l11l1l_opy_, bstack11ll111lll1_opy_, bstack1lll111lll1_opy_)
        self.bstack11ll11l1ll1_opy_ = any(bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᚻ") in item.lower() for item in bstack1l1l1l11l1l_opy_)
        self.bstack1ll1l1l1lll_opy_ = bstack1ll1l1l1lll_opy_
    def track_event(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1l1lllllll1_opy_.TEST or test_framework_state in bstack1ll111lll1l_opy_.bstack11l1ll1l1l1_opy_:
            bstack11ll1l1l1l1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1l1lllllll1_opy_.NONE:
            self.logger.warning(bstack11l11_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᚼ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠦࠧᚽ"))
            return
        if not self.bstack11ll11l1ll1_opy_:
            self.logger.warning(bstack11l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᚾ") + str(str(self.bstack1l1l1l11l1l_opy_)) + bstack11l11_opy_ (u"ࠨࠢᚿ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᛀ") + str(kwargs) + bstack11l11_opy_ (u"ࠣࠤᛁ"))
            return
        instance = self.__11ll1l111l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᛂ") + str(args) + bstack11l11_opy_ (u"ࠥࠦᛃ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll111lll1l_opy_.bstack11l1ll1l1l1_opy_:
                bstack1l111l111l_opy_ = bstack11l11_opy_ (u"ࠦࠧᛄ")
                name = bstack11l11_opy_ (u"ࠧࠨᛅ")
                if (test_hook_state == bstack1l1lllll1ll_opy_.PRE):
                    bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11l1ll1111l_opy_.value)
                    name = str(EVENTS.bstack11l1ll1111l_opy_.name)+bstack11l11_opy_ (u"ࠨ࠺ࠣᛆ")+str(test_framework_state.name)
                else:
                    bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11l1ll11ll1_opy_.value)
                    name = str(EVENTS.bstack11l1ll11ll1_opy_.name)+bstack11l11_opy_ (u"ࠢ࠻ࠤᛇ")+str(test_framework_state.name)
                TestFramework.bstack11ll1111lll_opy_(instance, name, bstack1l111l111l_opy_)
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᛈ").format(e))
        try:
            if not TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack11ll1ll11ll_opy_) and test_hook_state == bstack1l1lllll1ll_opy_.PRE:
                test = bstack1ll111lll1l_opy_.__11ll11l11ll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11l11_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᛉ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠥࠦᛊ"))
            if test_framework_state == bstack1l1lllllll1_opy_.TEST:
                if test_hook_state == bstack1l1lllll1ll_opy_.PRE and not TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l111ll1l1l_opy_):
                    TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l111ll1l1l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l11_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᛋ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠧࠨᛌ"))
                elif test_hook_state == bstack1l1lllll1ll_opy_.POST and not TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l11l1ll111_opy_):
                    TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1ll111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᛍ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠢࠣᛎ"))
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG and test_hook_state == bstack1l1lllll1ll_opy_.POST:
                bstack1ll111lll1l_opy_.__11l1ll1l1ll_opy_(instance, *args)
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG_REPORT and test_hook_state == bstack1l1lllll1ll_opy_.POST:
                self.__11l1lll1111_opy_(instance, *args)
                self.__11l1llll1ll_opy_(instance)
            elif test_framework_state in bstack1ll111lll1l_opy_.bstack11l1ll1l1l1_opy_:
                self.__11ll11l1lll_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᛏ") + str(instance.ref()) + bstack11l11_opy_ (u"ࠤࠥᛐ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11l1lll1lll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll111lll1l_opy_.bstack11l1ll1l1l1_opy_:
                bstack1l111l111l_opy_ = bstack11l11_opy_ (u"ࠥࠦᛑ")
                name = bstack11l11_opy_ (u"ࠦࠧᛒ")
                if (test_hook_state == bstack1l1lllll1ll_opy_.PRE):
                    name = str(EVENTS.bstack11l1ll1111l_opy_.name)+bstack11l11_opy_ (u"ࠧࡀࠢᛓ")+str(test_framework_state.name)
                    bstack1l111l111l_opy_ = TestFramework.bstack11ll1111l11_opy_(instance, name)
                    bstack111l1lllll_opy_.end(EVENTS.bstack11l1ll1111l_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᛔ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᛕ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1ll11ll1_opy_.name)+bstack11l11_opy_ (u"ࠣ࠼ࠥᛖ")+str(test_framework_state.name)
                    bstack1l111l111l_opy_ = TestFramework.bstack11ll1111l11_opy_(instance, name)
                    bstack111l1lllll_opy_.end(EVENTS.bstack11l1ll11ll1_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛗ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛘ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᛙ").format(e))
    def bstack1l11l1lll1l_opy_(self):
        return self.bstack11ll11l1ll1_opy_
    def __11ll11lll1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᛚ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11ll1ll11_opy_(rep, [bstack11l11_opy_ (u"ࠨࡷࡩࡧࡱࠦᛛ"), bstack11l11_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᛜ"), bstack11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᛝ"), bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᛞ"), bstack11l11_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᛟ"), bstack11l11_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᛠ")])
        return None
    def __11l1lll1111_opy_(self, instance: bstack1ll11l111ll_opy_, *args):
        result = self.__11ll11lll1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1l11lll_opy_ = None
        if result.get(bstack11l11_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᛡ"), None) == bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᛢ") and len(args) > 1 and getattr(args[1], bstack11l11_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᛣ"), None) is not None:
            failure = [{bstack11l11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᛤ"): [args[1].excinfo.exconly(), result.get(bstack11l11_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᛥ"), None)]}]
            bstack1lll1l11lll_opy_ = bstack11l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᛦ") if bstack11l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᛧ") in getattr(args[1].excinfo, bstack11l11_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᛨ"), bstack11l11_opy_ (u"ࠨࠢᛩ")) else bstack11l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᛪ")
        bstack11ll11ll111_opy_ = result.get(bstack11l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᛫"), TestFramework.bstack11ll11lll11_opy_)
        if bstack11ll11ll111_opy_ != TestFramework.bstack11ll11lll11_opy_:
            TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l111llll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1l11l1l_opy_(instance, {
            TestFramework.bstack1l111111111_opy_: failure,
            TestFramework.bstack11ll11l11l1_opy_: bstack1lll1l11lll_opy_,
            TestFramework.bstack1l111111l1l_opy_: bstack11ll11ll111_opy_,
        })
    def __11ll1l111l1_opy_(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1l1lllllll1_opy_.SETUP_FIXTURE:
            instance = self.__11ll1ll11l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1111l1l_opy_ bstack11ll1l11l11_opy_ this to be bstack11l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᛬")
            if test_framework_state == bstack1l1lllllll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll11llll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l11_opy_ (u"ࠥࡲࡴࡪࡥࠣ᛭"), None), bstack11l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᛮ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᛯ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1ll1ll11111_opy_(target) if target else None
        return instance
    def __11ll11l1lll_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1lll1l1l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack1ll111lll1l_opy_.bstack11l1lll11ll_opy_, {})
        if not key in bstack11l1lll1l1l_opy_:
            bstack11l1lll1l1l_opy_[key] = []
        bstack11l1lll1l11_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack1ll111lll1l_opy_.bstack11ll111111l_opy_, {})
        if not key in bstack11l1lll1l11_opy_:
            bstack11l1lll1l11_opy_[key] = []
        bstack11ll1l1l111_opy_ = {
            bstack1ll111lll1l_opy_.bstack11l1lll11ll_opy_: bstack11l1lll1l1l_opy_,
            bstack1ll111lll1l_opy_.bstack11ll111111l_opy_: bstack11l1lll1l11_opy_,
        }
        if test_hook_state == bstack1l1lllll1ll_opy_.PRE:
            hook = {
                bstack11l11_opy_ (u"ࠨ࡫ࡦࡻࠥᛰ"): key,
                TestFramework.bstack11l1ll1l11l_opy_: uuid4().__str__(),
                TestFramework.bstack11ll111ll1l_opy_: TestFramework.bstack11ll1lll111_opy_,
                TestFramework.bstack11ll11l1l1l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l1ll1ll1l_opy_: [],
                TestFramework.bstack11l1llll11l_opy_: args[1] if len(args) > 1 else bstack11l11_opy_ (u"ࠧࠨᛱ"),
                TestFramework.bstack11ll1ll1111_opy_: bstack1ll11lll1l1_opy_.bstack11ll11l1111_opy_()
            }
            bstack11l1lll1l1l_opy_[key].append(hook)
            bstack11ll1l1l111_opy_[bstack1ll111lll1l_opy_.bstack11ll1l11111_opy_] = key
        elif test_hook_state == bstack1l1lllll1ll_opy_.POST:
            bstack11ll11ll1ll_opy_ = bstack11l1lll1l1l_opy_.get(key, [])
            hook = bstack11ll11ll1ll_opy_.pop() if bstack11ll11ll1ll_opy_ else None
            if hook:
                result = self.__11ll11lll1l_opy_(*args)
                if result:
                    bstack11l1lll111l_opy_ = result.get(bstack11l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᛲ"), TestFramework.bstack11ll1lll111_opy_)
                    if bstack11l1lll111l_opy_ != TestFramework.bstack11ll1lll111_opy_:
                        hook[TestFramework.bstack11ll111ll1l_opy_] = bstack11l1lll111l_opy_
                hook[TestFramework.bstack11l1llll111_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1ll1111_opy_]= bstack1ll11lll1l1_opy_.bstack11ll11l1111_opy_()
                self.bstack11ll1ll1lll_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll11ll1l1_opy_, [])
                if logs: self.bstack1l11l11l111_opy_(instance, logs)
                bstack11l1lll1l11_opy_[key].append(hook)
                bstack11ll1l1l111_opy_[bstack1ll111lll1l_opy_.bstack11ll1ll1l1l_opy_] = key
        TestFramework.bstack11ll1l11l1l_opy_(instance, bstack11ll1l1l111_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᛳ") + str(bstack11l1lll1l11_opy_) + bstack11l11_opy_ (u"ࠥࠦᛴ"))
    def __11ll1ll11l1_opy_(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11ll1ll11_opy_(args[0], [bstack11l11_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᛵ"), bstack11l11_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᛶ"), bstack11l11_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᛷ"), bstack11l11_opy_ (u"ࠢࡪࡦࡶࠦᛸ"), bstack11l11_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥ᛹"), bstack11l11_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤ᛺")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ᛻")) else fixturedef.get(bstack11l11_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ᛼"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥ᛽")) else None
        node = request.node if hasattr(request, bstack11l11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ᛾")) else None
        target = request.node.nodeid if hasattr(node, bstack11l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢ᛿")) else None
        baseid = fixturedef.get(bstack11l11_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᜀ"), None) or bstack11l11_opy_ (u"ࠤࠥᜁ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l11_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᜂ")):
            target = bstack1ll111lll1l_opy_.__11l1llllll1_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l11_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᜃ")) else None
            if target and not TestFramework.bstack1ll1ll11111_opy_(target):
                self.__11ll11llll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᜄ") + str(test_hook_state) + bstack11l11_opy_ (u"ࠨࠢᜅ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᜆ") + str(target) + bstack11l11_opy_ (u"ࠣࠤᜇ"))
            return None
        instance = TestFramework.bstack1ll1ll11111_opy_(target)
        if not instance:
            self.logger.warning(bstack11l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᜈ") + str(target) + bstack11l11_opy_ (u"ࠥࠦᜉ"))
            return None
        bstack11ll111l1ll_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack1ll111lll1l_opy_.bstack11l1lllll11_opy_, {})
        if os.getenv(bstack11l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᜊ"), bstack11l11_opy_ (u"ࠧ࠷ࠢᜋ")) == bstack11l11_opy_ (u"ࠨ࠱ࠣᜌ"):
            bstack11ll111l11l_opy_ = bstack11l11_opy_ (u"ࠢ࠻ࠤᜍ").join((scope, fixturename))
            bstack11ll1l1l1ll_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll11111ll_opy_ = {
                bstack11l11_opy_ (u"ࠣ࡭ࡨࡽࠧᜎ"): bstack11ll111l11l_opy_,
                bstack11l11_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᜏ"): bstack1ll111lll1l_opy_.__11ll11ll11l_opy_(request.node),
                bstack11l11_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᜐ"): fixturedef,
                bstack11l11_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᜑ"): scope,
                bstack11l11_opy_ (u"ࠧࡺࡹࡱࡧࠥᜒ"): None,
            }
            try:
                if test_hook_state == bstack1l1lllll1ll_opy_.POST and callable(getattr(args[-1], bstack11l11_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᜓ"), None)):
                    bstack11ll11111ll_opy_[bstack11l11_opy_ (u"ࠢࡵࡻࡳࡩ᜔ࠧ")] = TestFramework.bstack1l11ll1l1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1l1lllll1ll_opy_.PRE:
                bstack11ll11111ll_opy_[bstack11l11_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ᜕")] = uuid4().__str__()
                bstack11ll11111ll_opy_[bstack1ll111lll1l_opy_.bstack11ll11l1l1l_opy_] = bstack11ll1l1l1ll_opy_
            elif test_hook_state == bstack1l1lllll1ll_opy_.POST:
                bstack11ll11111ll_opy_[bstack1ll111lll1l_opy_.bstack11l1llll111_opy_] = bstack11ll1l1l1ll_opy_
            if bstack11ll111l11l_opy_ in bstack11ll111l1ll_opy_:
                bstack11ll111l1ll_opy_[bstack11ll111l11l_opy_].update(bstack11ll11111ll_opy_)
                self.logger.debug(bstack11l11_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥ᜖") + str(bstack11ll111l1ll_opy_[bstack11ll111l11l_opy_]) + bstack11l11_opy_ (u"ࠥࠦ᜗"))
            else:
                bstack11ll111l1ll_opy_[bstack11ll111l11l_opy_] = bstack11ll11111ll_opy_
                self.logger.debug(bstack11l11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢ᜘") + str(len(bstack11ll111l1ll_opy_)) + bstack11l11_opy_ (u"ࠧࠨ᜙"))
        TestFramework.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack11l1lllll11_opy_, bstack11ll111l1ll_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᜚") + str(instance.ref()) + bstack11l11_opy_ (u"ࠢࠣ᜛"))
        return instance
    def __11ll11llll1_opy_(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1llll111_opy_.create_context(target)
        ob = bstack1ll11l111ll_opy_(ctx, self.bstack1l1l1l11l1l_opy_, self.bstack11ll111lll1_opy_, test_framework_state)
        TestFramework.bstack11ll1l11l1l_opy_(ob, {
            TestFramework.bstack1l1l1l11l11_opy_: context.test_framework_name,
            TestFramework.bstack1l11l111l11_opy_: context.test_framework_version,
            TestFramework.bstack11ll111llll_opy_: [],
            bstack1ll111lll1l_opy_.bstack11l1lllll11_opy_: {},
            bstack1ll111lll1l_opy_.bstack11ll111111l_opy_: {},
            bstack1ll111lll1l_opy_.bstack11l1lll11ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1ll1lll111l_opy_(ob, TestFramework.bstack11ll1l111ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1ll1lll111l_opy_(ob, TestFramework.bstack1l1l111l11l_opy_, context.platform_index)
        TestFramework.bstack1lll111l1l1_opy_[ctx.id] = ob
        self.logger.debug(bstack11l11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣ᜜") + str(TestFramework.bstack1lll111l1l1_opy_.keys()) + bstack11l11_opy_ (u"ࠤࠥ᜝"))
        return ob
    def bstack1l11l11lll1_opy_(self, instance: bstack1ll11l111ll_opy_, bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_]):
        bstack11l1ll1lll1_opy_ = (
            bstack1ll111lll1l_opy_.bstack11ll1l11111_opy_
            if bstack1ll1l1lll1l_opy_[1] == bstack1l1lllll1ll_opy_.PRE
            else bstack1ll111lll1l_opy_.bstack11ll1ll1l1l_opy_
        )
        hook = bstack1ll111lll1l_opy_.bstack11ll111l111_opy_(instance, bstack11l1ll1lll1_opy_)
        entries = hook.get(TestFramework.bstack11l1ll1ll1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack11ll111llll_opy_, []))
        return entries
    def bstack1l111llll11_opy_(self, instance: bstack1ll11l111ll_opy_, bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_]):
        bstack11l1ll1lll1_opy_ = (
            bstack1ll111lll1l_opy_.bstack11ll1l11111_opy_
            if bstack1ll1l1lll1l_opy_[1] == bstack1l1lllll1ll_opy_.PRE
            else bstack1ll111lll1l_opy_.bstack11ll1ll1l1l_opy_
        )
        bstack1ll111lll1l_opy_.bstack11l1lll1ll1_opy_(instance, bstack11l1ll1lll1_opy_)
        TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack11ll111llll_opy_, []).clear()
    def bstack11ll1ll1lll_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᜞")
        global _1l111lll1ll_opy_
        platform_index = os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᜟ")]
        bstack1l11l1111ll_opy_ = os.path.join(bstack1l11l1ll11l_opy_, (bstack1l111l1l1l1_opy_ + str(platform_index)), bstack11l1ll11l1l_opy_)
        if not os.path.exists(bstack1l11l1111ll_opy_) or not os.path.isdir(bstack1l11l1111ll_opy_):
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᜠ").format(bstack1l11l1111ll_opy_))
            return
        logs = hook.get(bstack11l11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᜡ"), [])
        with os.scandir(bstack1l11l1111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l111lll1ll_opy_:
                    self.logger.info(bstack11l11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᜢ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l11_opy_ (u"ࠣࠤᜣ")
                    log_entry = bstack1l1lll1l11l_opy_(
                        kind=bstack11l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᜤ"),
                        message=bstack11l11_opy_ (u"ࠥࠦᜥ"),
                        level=bstack11l11_opy_ (u"ࠦࠧᜦ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l111ll11l1_opy_=entry.stat().st_size,
                        bstack1l11l11ll1l_opy_=bstack11l11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᜧ"),
                        bstack1111l1_opy_=os.path.abspath(entry.path),
                        bstack11ll1ll1l11_opy_=hook.get(TestFramework.bstack11l1ll1l11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l111lll1ll_opy_.add(abs_path)
        platform_index = os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᜨ")]
        bstack11l1ll1llll_opy_ = os.path.join(bstack1l11l1ll11l_opy_, (bstack1l111l1l1l1_opy_ + str(platform_index)), bstack11l1ll11l1l_opy_, bstack11l1ll111l1_opy_)
        if not os.path.exists(bstack11l1ll1llll_opy_) or not os.path.isdir(bstack11l1ll1llll_opy_):
            self.logger.info(bstack11l11_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᜩ").format(bstack11l1ll1llll_opy_))
        else:
            self.logger.info(bstack11l11_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᜪ").format(bstack11l1ll1llll_opy_))
            with os.scandir(bstack11l1ll1llll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l111lll1ll_opy_:
                        self.logger.info(bstack11l11_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᜫ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l11_opy_ (u"ࠥࠦᜬ")
                        log_entry = bstack1l1lll1l11l_opy_(
                            kind=bstack11l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᜭ"),
                            message=bstack11l11_opy_ (u"ࠧࠨᜮ"),
                            level=bstack11l11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᜯ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l111ll11l1_opy_=entry.stat().st_size,
                            bstack1l11l11ll1l_opy_=bstack11l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᜰ"),
                            bstack1111l1_opy_=os.path.abspath(entry.path),
                            bstack1l111lll1l1_opy_=hook.get(TestFramework.bstack11l1ll1l11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l111lll1ll_opy_.add(abs_path)
        hook[bstack11l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᜱ")] = logs
    def bstack1l11l11l111_opy_(
        self,
        bstack1l111l1ll1l_opy_: bstack1ll11l111ll_opy_,
        entries: List[bstack1l1lll1l11l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᜲ"))
        req.platform_index = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l111l11l_opy_)
        req.client_worker_id = bstack11l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᜳ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111l1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111l1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111l1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l1l11l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l11l111l11_opy_)
            log_entry.uuid = entry.bstack11ll1ll1l11_opy_
            log_entry.test_framework_state = bstack1l111l1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺᜴ࠥ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l11_opy_ (u"ࠧࠨ᜵")
            if entry.kind == bstack11l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᜶"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111ll11l1_opy_
                log_entry.file_path = entry.bstack1111l1_opy_
        def bstack1l11ll11l1l_opy_():
            bstack1lllll111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1lll_opy_.LogCreatedEvent(req)
                bstack1l111l1ll1l_opy_.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ᜷"), datetime.now() - bstack1lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ᜸").format(str(e)))
                traceback.print_exc()
        self.bstack1lll111lll1_opy_.enqueue(bstack1l11ll11l1l_opy_)
    def __11l1llll1ll_opy_(self, instance) -> None:
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ᜹")
        bstack11ll1l1l111_opy_ = {bstack11l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ᜺"): bstack1ll11lll1l1_opy_.bstack11ll11l1111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll1l11l1l_opy_(instance, bstack11ll1l1l111_opy_)
    @staticmethod
    def bstack11ll111l111_opy_(instance: bstack1ll11l111ll_opy_, bstack11l1ll1lll1_opy_: str):
        bstack11l1lll11l1_opy_ = (
            bstack1ll111lll1l_opy_.bstack11ll111111l_opy_
            if bstack11l1ll1lll1_opy_ == bstack1ll111lll1l_opy_.bstack11ll1ll1l1l_opy_
            else bstack1ll111lll1l_opy_.bstack11l1lll11ll_opy_
        )
        bstack11ll1ll111l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11l1ll1lll1_opy_, None)
        bstack11ll1l1l11l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11l1lll11l1_opy_, None) if bstack11ll1ll111l_opy_ else None
        return (
            bstack11ll1l1l11l_opy_[bstack11ll1ll111l_opy_][-1]
            if isinstance(bstack11ll1l1l11l_opy_, dict) and len(bstack11ll1l1l11l_opy_.get(bstack11ll1ll111l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11l1lll1ll1_opy_(instance: bstack1ll11l111ll_opy_, bstack11l1ll1lll1_opy_: str):
        hook = bstack1ll111lll1l_opy_.bstack11ll111l111_opy_(instance, bstack11l1ll1lll1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11l1ll1ll1l_opy_, []).clear()
    @staticmethod
    def __11l1ll1l1ll_opy_(instance: bstack1ll11l111ll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤ᜻"), None)):
            return
        if os.getenv(bstack11l11_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤ᜼"), bstack11l11_opy_ (u"ࠨ࠱ࠣ᜽")) != bstack11l11_opy_ (u"ࠢ࠲ࠤ᜾"):
            bstack1ll111lll1l_opy_.logger.warning(bstack11l11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥ᜿"))
            return
        bstack11l1llll1l1_opy_ = {
            bstack11l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᝀ"): (bstack1ll111lll1l_opy_.bstack11ll1l11111_opy_, bstack1ll111lll1l_opy_.bstack11l1lll11ll_opy_),
            bstack11l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᝁ"): (bstack1ll111lll1l_opy_.bstack11ll1ll1l1l_opy_, bstack1ll111lll1l_opy_.bstack11ll111111l_opy_),
        }
        for when in (bstack11l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᝂ"), bstack11l11_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᝃ"), bstack11l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᝄ")):
            bstack11ll1l1ll11_opy_ = args[1].get_records(when)
            if not bstack11ll1l1ll11_opy_:
                continue
            records = [
                bstack1l1lll1l11l_opy_(
                    kind=TestFramework.bstack1l11ll1l111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l11_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᝅ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᝆ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll1l1ll11_opy_
                if isinstance(getattr(r, bstack11l11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᝇ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll1111ll1_opy_, bstack11l1lll11l1_opy_ = bstack11l1llll1l1_opy_.get(when, (None, None))
            bstack11ll11l111l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11ll1111ll1_opy_, None) if bstack11ll1111ll1_opy_ else None
            bstack11ll1l1l11l_opy_ = TestFramework.bstack1lll111111l_opy_(instance, bstack11l1lll11l1_opy_, None) if bstack11ll11l111l_opy_ else None
            if isinstance(bstack11ll1l1l11l_opy_, dict) and len(bstack11ll1l1l11l_opy_.get(bstack11ll11l111l_opy_, [])) > 0:
                hook = bstack11ll1l1l11l_opy_[bstack11ll11l111l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11l1ll1ll1l_opy_ in hook:
                    hook[TestFramework.bstack11l1ll1ll1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack11ll111llll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll11l11ll_opy_(test) -> Dict[str, Any]:
        bstack1lllll11ll_opy_ = bstack1ll111lll1l_opy_.__11l1llllll1_opy_(test.location) if hasattr(test, bstack11l11_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᝈ")) else getattr(test, bstack11l11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᝉ"), None)
        test_name = test.name if hasattr(test, bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᝊ")) else None
        bstack11ll1ll1ll1_opy_ = test.fspath.strpath if hasattr(test, bstack11l11_opy_ (u"ࠨࡦࡴࡲࡤࡸ࡭ࠨᝋ")) and test.fspath else None
        if not bstack1lllll11ll_opy_ or not test_name or not bstack11ll1ll1ll1_opy_:
            return None
        code = None
        if hasattr(test, bstack11l11_opy_ (u"ࠢࡰࡤ࡭ࠦᝌ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l1ll11lll_opy_ = []
        try:
            bstack11l1ll11lll_opy_ = bstack11l1ll111l_opy_.bstack11111l11ll_opy_(test)
        except:
            bstack1ll111lll1l_opy_.logger.warning(bstack11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠬࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡳࡧࡶࡳࡱࡼࡥࡥࠢ࡬ࡲࠥࡉࡌࡊࠤᝍ"))
        return {
            TestFramework.bstack1l1l11l11l1_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1ll11ll_opy_: bstack1lllll11ll_opy_,
            TestFramework.bstack1l1ll11111l_opy_: test_name,
            TestFramework.bstack1l111l11111_opy_: getattr(test, bstack11l11_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᝎ"), None),
            TestFramework.bstack11ll111l1l1_opy_: bstack11ll1ll1ll1_opy_,
            TestFramework.bstack11ll1l11lll_opy_: bstack1ll111lll1l_opy_.__11ll11ll11l_opy_(test),
            TestFramework.bstack11ll11l1l11_opy_: code,
            TestFramework.bstack1l111111l1l_opy_: TestFramework.bstack11ll11lll11_opy_,
            TestFramework.bstack11lll11ll11_opy_: bstack1lllll11ll_opy_,
            TestFramework.bstack11l1ll11111_opy_: bstack11l1ll11lll_opy_
        }
    @staticmethod
    def __11ll11ll11l_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11l11_opy_ (u"ࠥࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠣᝏ"), [])
            markers.extend([getattr(m, bstack11l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᝐ"), None) for m in own_markers if getattr(m, bstack11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᝑ"), None)])
            current = getattr(current, bstack11l11_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᝒ"), None)
        return markers
    @staticmethod
    def __11l1llllll1_opy_(location):
        return bstack11l11_opy_ (u"ࠢ࠻࠼ࠥᝓ").join(filter(lambda x: isinstance(x, str), location))