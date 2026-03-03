# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll1111ll1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1lllll11_opy_ import bstack11ll111llll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1ll1ll11l1l_opy_,
    bstack1ll1l111111_opy_,
    bstack1l1llll1l1l_opy_,
    bstack11l1llllll1_opy_,
    bstack1ll1l1l11ll_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l11llll11l_opy_
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lll11lll11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1llll_opy_ import bstack1ll11ll1l1l_opy_
from bstack_utils.bstack1111ll1l1l_opy_ import bstack11lll1ll1_opy_
bstack1l11lll1111_opy_ = bstack1l11llll11l_opy_()
bstack11ll11l111l_opy_ = 1.0
bstack1l11lll1l11_opy_ = bstack11ll111_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᚷ")
bstack11l1lll1l1l_opy_ = bstack11ll111_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᚸ")
bstack11l1lll11ll_opy_ = bstack11ll111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᚹ")
bstack11l1lll11l1_opy_ = bstack11ll111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᚺ")
bstack11l1lll1ll1_opy_ = bstack11ll111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᚻ")
_1l11l1ll1l1_opy_ = set()
class bstack1ll11l1llll_opy_(TestFramework):
    bstack11l1llll1l1_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᚼ")
    bstack11ll11lllll_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࠤᚽ")
    bstack11l1llll1ll_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᚾ")
    bstack11lll111l11_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᚿ")
    bstack11ll11l1l11_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᛀ")
    bstack11ll1ll11ll_opy_: bool
    bstack1lll11llll1_opy_: bstack1lll11lll11_opy_  = None
    bstack1l1llllll1l_opy_ = None
    bstack11ll1l1l11l_opy_ = [
        bstack1ll1ll11l1l_opy_.BEFORE_ALL,
        bstack1ll1ll11l1l_opy_.AFTER_ALL,
        bstack1ll1ll11l1l_opy_.BEFORE_EACH,
        bstack1ll1ll11l1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll1l1111l_opy_: Dict[str, str],
        bstack1l1l1ll1l1l_opy_: List[str]=[bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᛁ")],
        bstack1lll11llll1_opy_: bstack1lll11lll11_opy_=None,
        bstack1l1llllll1l_opy_=None
    ):
        super().__init__(bstack1l1l1ll1l1l_opy_, bstack11ll1l1111l_opy_, bstack1lll11llll1_opy_)
        self.bstack11ll1ll11ll_opy_ = any(bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᛂ") in item.lower() for item in bstack1l1l1ll1l1l_opy_)
        self.bstack1l1llllll1l_opy_ = bstack1l1llllll1l_opy_
    def track_event(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1ll1ll11l1l_opy_.TEST or test_framework_state in bstack1ll11l1llll_opy_.bstack11ll1l1l11l_opy_:
            bstack11ll111llll_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1ll1ll11l1l_opy_.NONE:
            self.logger.warning(bstack11ll111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࠦᛃ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠦࠧᛄ"))
            return
        if not self.bstack11ll1ll11ll_opy_:
            self.logger.warning(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡂࠨᛅ") + str(str(self.bstack1l1l1ll1l1l_opy_)) + bstack11ll111_opy_ (u"ࠨࠢᛆ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᛇ") + str(kwargs) + bstack11ll111_opy_ (u"ࠣࠤᛈ"))
            return
        instance = self.__11ll1l111ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡤࡶ࡬ࡹ࠽ࠣᛉ") + str(args) + bstack11ll111_opy_ (u"ࠥࠦᛊ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll11l1llll_opy_.bstack11ll1l1l11l_opy_:
                bstack11llllllll_opy_ = bstack11ll111_opy_ (u"ࠦࠧᛋ")
                name = bstack11ll111_opy_ (u"ࠧࠨᛌ")
                if (test_hook_state == bstack1l1llll1l1l_opy_.PRE):
                    bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack11l1ll1llll_opy_.value)
                    name = str(EVENTS.bstack11l1ll1llll_opy_.name)+bstack11ll111_opy_ (u"ࠨ࠺ࠣᛍ")+str(test_framework_state.name)
                else:
                    bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack11l1lll111l_opy_.value)
                    name = str(EVENTS.bstack11l1lll111l_opy_.name)+bstack11ll111_opy_ (u"ࠢ࠻ࠤᛎ")+str(test_framework_state.name)
                TestFramework.bstack11ll1111l1l_opy_(instance, name, bstack11llllllll_opy_)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵࠤࡵࡸࡥ࠻ࠢࡾࢁࠧᛏ").format(e))
        try:
            if not TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11ll1l1llll_opy_) and test_hook_state == bstack1l1llll1l1l_opy_.PRE:
                test = bstack1ll11l1llll_opy_.__11ll1l11lll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11ll111_opy_ (u"ࠤ࡯ࡳࡦࡪࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᛐ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠥࠦᛑ"))
            if test_framework_state == bstack1ll1ll11l1l_opy_.TEST:
                if test_hook_state == bstack1l1llll1l1l_opy_.PRE and not TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1lll11_opy_):
                    TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11l1lll11_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡳࡵࡣࡵࡸࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᛒ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠧࠨᛓ"))
                elif test_hook_state == bstack1l1llll1l1l_opy_.POST and not TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l11llll_opy_):
                    TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11l11llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡧࡱࡨࠥ࡬࡯ࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᛔ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠢࠣᛕ"))
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG and test_hook_state == bstack1l1llll1l1l_opy_.POST:
                bstack1ll11l1llll_opy_.__11l1lllll11_opy_(instance, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG_REPORT and test_hook_state == bstack1l1llll1l1l_opy_.POST:
                self.__11ll11l1l1l_opy_(instance, *args)
                self.__11ll1l1ll11_opy_(instance)
            elif test_framework_state in bstack1ll11l1llll_opy_.bstack11ll1l1l11l_opy_:
                self.__11ll111111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᛖ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠤࠥᛗ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lll111l1l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll11l1llll_opy_.bstack11ll1l1l11l_opy_:
                bstack11llllllll_opy_ = bstack11ll111_opy_ (u"ࠥࠦᛘ")
                name = bstack11ll111_opy_ (u"ࠦࠧᛙ")
                if (test_hook_state == bstack1l1llll1l1l_opy_.PRE):
                    name = str(EVENTS.bstack11l1ll1llll_opy_.name)+bstack11ll111_opy_ (u"ࠧࡀࠢᛚ")+str(test_framework_state.name)
                    bstack11llllllll_opy_ = TestFramework.bstack11ll11l1lll_opy_(instance, name)
                    bstack1111l1l1l_opy_.end(EVENTS.bstack11l1ll1llll_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᛛ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᛜ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1lll111l_opy_.name)+bstack11ll111_opy_ (u"ࠣ࠼ࠥᛝ")+str(test_framework_state.name)
                    bstack11llllllll_opy_ = TestFramework.bstack11ll11l1lll_opy_(instance, name)
                    bstack1111l1l1l_opy_.end(EVENTS.bstack11l1lll111l_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛞ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛟ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᛠ").format(e))
    def bstack1l11l111lll_opy_(self):
        return self.bstack11ll1ll11ll_opy_
    def __11ll1111111_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11ll111_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᛡ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11ll111l1_opy_(rep, [bstack11ll111_opy_ (u"ࠨࡷࡩࡧࡱࠦᛢ"), bstack11ll111_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᛣ"), bstack11ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᛤ"), bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᛥ"), bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᛦ"), bstack11ll111_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᛧ")])
        return None
    def __11ll11l1l1l_opy_(self, instance: bstack1ll1l111111_opy_, *args):
        result = self.__11ll1111111_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll11ll_opy_ = None
        if result.get(bstack11ll111_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᛨ"), None) == bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᛩ") and len(args) > 1 and getattr(args[1], bstack11ll111_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᛪ"), None) is not None:
            failure = [{bstack11ll111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ᛫"): [args[1].excinfo.exconly(), result.get(bstack11ll111_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣ᛬"), None)]}]
            bstack1lll1ll11ll_opy_ = bstack11ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ᛭") if bstack11ll111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᛮ") in getattr(args[1].excinfo, bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᛯ"), bstack11ll111_opy_ (u"ࠨࠢᛰ")) else bstack11ll111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᛱ")
        bstack11ll11ll1l1_opy_ = result.get(bstack11ll111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᛲ"), TestFramework.bstack11ll1111lll_opy_)
        if bstack11ll11ll1l1_opy_ != TestFramework.bstack11ll1111lll_opy_:
            TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll11111ll_opy_(instance, {
            TestFramework.bstack1l1111l1l1l_opy_: failure,
            TestFramework.bstack11ll111lll1_opy_: bstack1lll1ll11ll_opy_,
            TestFramework.bstack1l11111l1l1_opy_: bstack11ll11ll1l1_opy_,
        })
    def __11ll1l111ll_opy_(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1ll1ll11l1l_opy_.SETUP_FIXTURE:
            instance = self.__11ll1ll1lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11lll1111ll_opy_ bstack11ll111l1l1_opy_ this to be bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᛳ")
            if test_framework_state == bstack1ll1ll11l1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll111l1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࠣᛴ"), None), bstack11ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᛵ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11ll111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᛶ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll1111111_opy_(target) if target else None
        return instance
    def __11ll111111l_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11l1llll111_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack1ll11l1llll_opy_.bstack11ll11lllll_opy_, {})
        if not key in bstack11l1llll111_opy_:
            bstack11l1llll111_opy_[key] = []
        bstack11ll1l11l1l_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack1ll11l1llll_opy_.bstack11l1llll1ll_opy_, {})
        if not key in bstack11ll1l11l1l_opy_:
            bstack11ll1l11l1l_opy_[key] = []
        bstack11ll11lll1l_opy_ = {
            bstack1ll11l1llll_opy_.bstack11ll11lllll_opy_: bstack11l1llll111_opy_,
            bstack1ll11l1llll_opy_.bstack11l1llll1ll_opy_: bstack11ll1l11l1l_opy_,
        }
        if test_hook_state == bstack1l1llll1l1l_opy_.PRE:
            hook = {
                bstack11ll111_opy_ (u"ࠨ࡫ࡦࡻࠥᛷ"): key,
                TestFramework.bstack11ll1llllll_opy_: uuid4().__str__(),
                TestFramework.bstack11ll11ll111_opy_: TestFramework.bstack11ll1lllll1_opy_,
                TestFramework.bstack11ll1lll1ll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll11ll1ll_opy_: [],
                TestFramework.bstack11ll1ll11l1_opy_: args[1] if len(args) > 1 else bstack11ll111_opy_ (u"ࠧࠨᛸ"),
                TestFramework.bstack11ll1ll111l_opy_: bstack1ll11ll1l1l_opy_.bstack11ll11l1111_opy_()
            }
            bstack11l1llll111_opy_[key].append(hook)
            bstack11ll11lll1l_opy_[bstack1ll11l1llll_opy_.bstack11lll111l11_opy_] = key
        elif test_hook_state == bstack1l1llll1l1l_opy_.POST:
            bstack11ll1lll111_opy_ = bstack11l1llll111_opy_.get(key, [])
            hook = bstack11ll1lll111_opy_.pop() if bstack11ll1lll111_opy_ else None
            if hook:
                result = self.__11ll1111111_opy_(*args)
                if result:
                    bstack11l1llll11l_opy_ = result.get(bstack11ll111_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᛹"), TestFramework.bstack11ll1lllll1_opy_)
                    if bstack11l1llll11l_opy_ != TestFramework.bstack11ll1lllll1_opy_:
                        hook[TestFramework.bstack11ll11ll111_opy_] = bstack11l1llll11l_opy_
                hook[TestFramework.bstack11ll1lll11l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11ll1ll111l_opy_]= bstack1ll11ll1l1l_opy_.bstack11ll11l1111_opy_()
                self.bstack11ll1ll1111_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll1l1ll1l_opy_, [])
                if logs: self.bstack1l11l11l1l1_opy_(instance, logs)
                bstack11ll1l11l1l_opy_[key].append(hook)
                bstack11ll11lll1l_opy_[bstack1ll11l1llll_opy_.bstack11ll11l1l11_opy_] = key
        TestFramework.bstack11ll11111ll_opy_(instance, bstack11ll11lll1l_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣ᛺") + str(bstack11ll1l11l1l_opy_) + bstack11ll111_opy_ (u"ࠥࠦ᛻"))
    def __11ll1ll1lll_opy_(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11ll111l1_opy_(args[0], [bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ᛼"), bstack11ll111_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨ᛽"), bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨ᛾"), bstack11ll111_opy_ (u"ࠢࡪࡦࡶࠦ᛿"), bstack11ll111_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᜀ"), bstack11ll111_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᜁ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᜂ")) else fixturedef.get(bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᜃ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11ll111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᜄ")) else None
        node = request.node if hasattr(request, bstack11ll111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᜅ")) else None
        target = request.node.nodeid if hasattr(node, bstack11ll111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᜆ")) else None
        baseid = fixturedef.get(bstack11ll111_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᜇ"), None) or bstack11ll111_opy_ (u"ࠤࠥᜈ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11ll111_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᜉ")):
            target = bstack1ll11l1llll_opy_.__11l1lllll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11ll111_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᜊ")) else None
            if target and not TestFramework.bstack1lll1111111_opy_(target):
                self.__11ll111l1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᜋ") + str(test_hook_state) + bstack11ll111_opy_ (u"ࠨࠢᜌ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11ll111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᜍ") + str(target) + bstack11ll111_opy_ (u"ࠣࠤᜎ"))
            return None
        instance = TestFramework.bstack1lll1111111_opy_(target)
        if not instance:
            self.logger.warning(bstack11ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᜏ") + str(target) + bstack11ll111_opy_ (u"ࠥࠦᜐ"))
            return None
        bstack11lll111lll_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack1ll11l1llll_opy_.bstack11l1llll1l1_opy_, {})
        if os.getenv(bstack11ll111_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᜑ"), bstack11ll111_opy_ (u"ࠧ࠷ࠢᜒ")) == bstack11ll111_opy_ (u"ࠨ࠱ࠣᜓ"):
            bstack11lll111111_opy_ = bstack11ll111_opy_ (u"ࠢ࠻ࠤ᜔").join((scope, fixturename))
            bstack11ll111l111_opy_ = datetime.now(tz=timezone.utc)
            bstack11ll1lll1l1_opy_ = {
                bstack11ll111_opy_ (u"ࠣ࡭ࡨࡽ᜕ࠧ"): bstack11lll111111_opy_,
                bstack11ll111_opy_ (u"ࠤࡷࡥ࡬ࡹࠢ᜖"): bstack1ll11l1llll_opy_.__11ll111ll11_opy_(request.node),
                bstack11ll111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦ᜗"): fixturedef,
                bstack11ll111_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥ᜘"): scope,
                bstack11ll111_opy_ (u"ࠧࡺࡹࡱࡧࠥ᜙"): None,
            }
            try:
                if test_hook_state == bstack1l1llll1l1l_opy_.POST and callable(getattr(args[-1], bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥ᜚"), None)):
                    bstack11ll1lll1l1_opy_[bstack11ll111_opy_ (u"ࠢࡵࡻࡳࡩࠧ᜛")] = TestFramework.bstack1l111ll1lll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1l1llll1l1l_opy_.PRE:
                bstack11ll1lll1l1_opy_[bstack11ll111_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ᜜")] = uuid4().__str__()
                bstack11ll1lll1l1_opy_[bstack1ll11l1llll_opy_.bstack11ll1lll1ll_opy_] = bstack11ll111l111_opy_
            elif test_hook_state == bstack1l1llll1l1l_opy_.POST:
                bstack11ll1lll1l1_opy_[bstack1ll11l1llll_opy_.bstack11ll1lll11l_opy_] = bstack11ll111l111_opy_
            if bstack11lll111111_opy_ in bstack11lll111lll_opy_:
                bstack11lll111lll_opy_[bstack11lll111111_opy_].update(bstack11ll1lll1l1_opy_)
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥ᜝") + str(bstack11lll111lll_opy_[bstack11lll111111_opy_]) + bstack11ll111_opy_ (u"ࠥࠦ᜞"))
            else:
                bstack11lll111lll_opy_[bstack11lll111111_opy_] = bstack11ll1lll1l1_opy_
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᜟ") + str(len(bstack11lll111lll_opy_)) + bstack11ll111_opy_ (u"ࠧࠨᜠ"))
        TestFramework.bstack1lll11l1111_opy_(instance, bstack1ll11l1llll_opy_.bstack11l1llll1l1_opy_, bstack11lll111lll_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᜡ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠢࠣᜢ"))
        return instance
    def __11ll111l1ll_opy_(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1lllllll_opy_.create_context(target)
        ob = bstack1ll1l111111_opy_(ctx, self.bstack1l1l1ll1l1l_opy_, self.bstack11ll1l1111l_opy_, test_framework_state)
        TestFramework.bstack11ll11111ll_opy_(ob, {
            TestFramework.bstack1l1ll1ll1l1_opy_: context.test_framework_name,
            TestFramework.bstack1l11l1l11l1_opy_: context.test_framework_version,
            TestFramework.bstack11ll11ll11l_opy_: [],
            bstack1ll11l1llll_opy_.bstack11l1llll1l1_opy_: {},
            bstack1ll11l1llll_opy_.bstack11l1llll1ll_opy_: {},
            bstack1ll11l1llll_opy_.bstack11ll11lllll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll11l1111_opy_(ob, TestFramework.bstack11ll1111l11_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll11l1111_opy_(ob, TestFramework.bstack1l1ll1lll11_opy_, context.platform_index)
        TestFramework.bstack1ll1lll1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᜣ") + str(TestFramework.bstack1ll1lll1ll1_opy_.keys()) + bstack11ll111_opy_ (u"ࠤࠥᜤ"))
        return ob
    def bstack1l111lll11l_opy_(self, instance: bstack1ll1l111111_opy_, bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_]):
        bstack11l1lll1lll_opy_ = (
            bstack1ll11l1llll_opy_.bstack11lll111l11_opy_
            if bstack1ll1ll1llll_opy_[1] == bstack1l1llll1l1l_opy_.PRE
            else bstack1ll11l1llll_opy_.bstack11ll11l1l11_opy_
        )
        hook = bstack1ll11l1llll_opy_.bstack11ll1ll1ll1_opy_(instance, bstack11l1lll1lll_opy_)
        entries = hook.get(TestFramework.bstack11ll11ll1ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, []))
        return entries
    def bstack1l111llllll_opy_(self, instance: bstack1ll1l111111_opy_, bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_]):
        bstack11l1lll1lll_opy_ = (
            bstack1ll11l1llll_opy_.bstack11lll111l11_opy_
            if bstack1ll1ll1llll_opy_[1] == bstack1l1llll1l1l_opy_.PRE
            else bstack1ll11l1llll_opy_.bstack11ll11l1l11_opy_
        )
        bstack1ll11l1llll_opy_.bstack11ll111l11l_opy_(instance, bstack11l1lll1lll_opy_)
        TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, []).clear()
    def bstack11ll1ll1111_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᜥ")
        global _1l11l1ll1l1_opy_
        platform_index = os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᜦ")]
        bstack1l11ll111ll_opy_ = os.path.join(bstack1l11lll1111_opy_, (bstack1l11lll1l11_opy_ + str(platform_index)), bstack11l1lll11l1_opy_)
        if not os.path.exists(bstack1l11ll111ll_opy_) or not os.path.isdir(bstack1l11ll111ll_opy_):
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᜧ").format(bstack1l11ll111ll_opy_))
            return
        logs = hook.get(bstack11ll111_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᜨ"), [])
        with os.scandir(bstack1l11ll111ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11l1ll1l1_opy_:
                    self.logger.info(bstack11ll111_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᜩ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11ll111_opy_ (u"ࠣࠤᜪ")
                    log_entry = bstack1ll1l1l11ll_opy_(
                        kind=bstack11ll111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᜫ"),
                        message=bstack11ll111_opy_ (u"ࠥࠦᜬ"),
                        level=bstack11ll111_opy_ (u"ࠦࠧᜭ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11ll1l1ll_opy_=entry.stat().st_size,
                        bstack1l11l11ll11_opy_=bstack11ll111_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᜮ"),
                        bstack1_opy_=os.path.abspath(entry.path),
                        bstack11lll1111l1_opy_=hook.get(TestFramework.bstack11ll1llllll_opy_)
                    )
                    logs.append(log_entry)
                    _1l11l1ll1l1_opy_.add(abs_path)
        platform_index = os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᜯ")]
        bstack11lll11111l_opy_ = os.path.join(bstack1l11lll1111_opy_, (bstack1l11lll1l11_opy_ + str(platform_index)), bstack11l1lll11l1_opy_, bstack11l1lll1ll1_opy_)
        if not os.path.exists(bstack11lll11111l_opy_) or not os.path.isdir(bstack11lll11111l_opy_):
            self.logger.info(bstack11ll111_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᜰ").format(bstack11lll11111l_opy_))
        else:
            self.logger.info(bstack11ll111_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᜱ").format(bstack11lll11111l_opy_))
            with os.scandir(bstack11lll11111l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11l1ll1l1_opy_:
                        self.logger.info(bstack11ll111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᜲ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11ll111_opy_ (u"ࠥࠦᜳ")
                        log_entry = bstack1ll1l1l11ll_opy_(
                            kind=bstack11ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᜴"),
                            message=bstack11ll111_opy_ (u"ࠧࠨ᜵"),
                            level=bstack11ll111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ᜶"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11ll1l1ll_opy_=entry.stat().st_size,
                            bstack1l11l11ll11_opy_=bstack11ll111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ᜷"),
                            bstack1_opy_=os.path.abspath(entry.path),
                            bstack1l11lll1lll_opy_=hook.get(TestFramework.bstack11ll1llllll_opy_)
                        )
                        logs.append(log_entry)
                        _1l11l1ll1l1_opy_.add(abs_path)
        hook[bstack11ll111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᜸")] = logs
    def bstack1l11l11l1l1_opy_(
        self,
        bstack1l11ll11ll1_opy_: bstack1ll1l111111_opy_,
        entries: List[bstack1ll1l1l11ll_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨ᜹"))
        req.platform_index = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1ll1lll11_opy_)
        req.client_worker_id = bstack11ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᜺").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11ll11ll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11ll11ll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11ll11ll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1ll1ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l11l1l11l1_opy_)
            log_entry.uuid = entry.bstack11lll1111l1_opy_
            log_entry.test_framework_state = bstack1l11ll11ll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᜻"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11ll111_opy_ (u"ࠧࠨ᜼")
            if entry.kind == bstack11ll111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᜽"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l1ll_opy_
                log_entry.file_path = entry.bstack1_opy_
        def bstack1l11ll1l11l_opy_():
            bstack11lll11111_opy_ = datetime.now()
            try:
                self.bstack1l1llllll1l_opy_.LogCreatedEvent(req)
                bstack1l11ll11ll1_opy_.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ᜾"), datetime.now() - bstack11lll11111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ᜿").format(str(e)))
                traceback.print_exc()
        self.bstack1lll11llll1_opy_.enqueue(bstack1l11ll1l11l_opy_)
    def __11ll1l1ll11_opy_(self, instance) -> None:
        bstack11ll111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᝀ")
        bstack11ll11lll1l_opy_ = {bstack11ll111_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᝁ"): bstack1ll11ll1l1l_opy_.bstack11ll11l1111_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll11111ll_opy_(instance, bstack11ll11lll1l_opy_)
    @staticmethod
    def bstack11ll1ll1ll1_opy_(instance: bstack1ll1l111111_opy_, bstack11l1lll1lll_opy_: str):
        bstack11l1lllllll_opy_ = (
            bstack1ll11l1llll_opy_.bstack11l1llll1ll_opy_
            if bstack11l1lll1lll_opy_ == bstack1ll11l1llll_opy_.bstack11ll11l1l11_opy_
            else bstack1ll11l1llll_opy_.bstack11ll11lllll_opy_
        )
        bstack11ll1l11l11_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11l1lll1lll_opy_, None)
        bstack11ll11llll1_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11l1lllllll_opy_, None) if bstack11ll1l11l11_opy_ else None
        return (
            bstack11ll11llll1_opy_[bstack11ll1l11l11_opy_][-1]
            if isinstance(bstack11ll11llll1_opy_, dict) and len(bstack11ll11llll1_opy_.get(bstack11ll1l11l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll111l11l_opy_(instance: bstack1ll1l111111_opy_, bstack11l1lll1lll_opy_: str):
        hook = bstack1ll11l1llll_opy_.bstack11ll1ll1ll1_opy_(instance, bstack11l1lll1lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll11ll1ll_opy_, []).clear()
    @staticmethod
    def __11l1lllll11_opy_(instance: bstack1ll1l111111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡧࡴࡸࡤࡴࠤᝂ"), None)):
            return
        if os.getenv(bstack11ll111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡑࡕࡇࡔࠤᝃ"), bstack11ll111_opy_ (u"ࠨ࠱ࠣᝄ")) != bstack11ll111_opy_ (u"ࠢ࠲ࠤᝅ"):
            bstack1ll11l1llll_opy_.logger.warning(bstack11ll111_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡩ࡯ࡩࠣࡧࡦࡶ࡬ࡰࡩࠥᝆ"))
            return
        bstack11ll1l1lll1_opy_ = {
            bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᝇ"): (bstack1ll11l1llll_opy_.bstack11lll111l11_opy_, bstack1ll11l1llll_opy_.bstack11ll11lllll_opy_),
            bstack11ll111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᝈ"): (bstack1ll11l1llll_opy_.bstack11ll11l1l11_opy_, bstack1ll11l1llll_opy_.bstack11l1llll1ll_opy_),
        }
        for when in (bstack11ll111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᝉ"), bstack11ll111_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᝊ"), bstack11ll111_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᝋ")):
            bstack11ll11111l1_opy_ = args[1].get_records(when)
            if not bstack11ll11111l1_opy_:
                continue
            records = [
                bstack1ll1l1l11ll_opy_(
                    kind=TestFramework.bstack1l111lll111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11ll111_opy_ (u"ࠢ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠥᝌ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11ll111_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠤᝍ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll11111l1_opy_
                if isinstance(getattr(r, bstack11ll111_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᝎ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11ll1l1l1ll_opy_, bstack11l1lllllll_opy_ = bstack11ll1l1lll1_opy_.get(when, (None, None))
            bstack11ll1ll1l11_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11ll1l1l1ll_opy_, None) if bstack11ll1l1l1ll_opy_ else None
            bstack11ll11llll1_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, bstack11l1lllllll_opy_, None) if bstack11ll1ll1l11_opy_ else None
            if isinstance(bstack11ll11llll1_opy_, dict) and len(bstack11ll11llll1_opy_.get(bstack11ll1ll1l11_opy_, [])) > 0:
                hook = bstack11ll11llll1_opy_[bstack11ll1ll1l11_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll11ll1ll_opy_ in hook:
                    hook[TestFramework.bstack11ll11ll1ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack11ll11ll11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1l11lll_opy_(test) -> Dict[str, Any]:
        bstack111lll1111_opy_ = bstack1ll11l1llll_opy_.__11l1lllll1l_opy_(test.location) if hasattr(test, bstack11ll111_opy_ (u"ࠥࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᝏ")) else getattr(test, bstack11ll111_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᝐ"), None)
        test_name = test.name if hasattr(test, bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᝑ")) else None
        bstack11ll1111ll1_opy_ = test.fspath.strpath if hasattr(test, bstack11ll111_opy_ (u"ࠨࡦࡴࡲࡤࡸ࡭ࠨᝒ")) and test.fspath else None
        if not bstack111lll1111_opy_ or not test_name or not bstack11ll1111ll1_opy_:
            return None
        code = None
        if hasattr(test, bstack11ll111_opy_ (u"ࠢࡰࡤ࡭ࠦᝓ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l1lll1l11_opy_ = []
        try:
            bstack11l1lll1l11_opy_ = bstack11lll1ll1_opy_.bstack111111ll1l_opy_(test)
        except:
            bstack1ll11l1llll_opy_.logger.warning(bstack11ll111_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡷࡩࡸࡺࠠࡴࡥࡲࡴࡪࡹࠬࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡳࡧࡶࡳࡱࡼࡥࡥࠢ࡬ࡲࠥࡉࡌࡊࠤ᝔"))
        return {
            TestFramework.bstack1l1l11ll1ll_opy_: uuid4().__str__(),
            TestFramework.bstack11ll1l1llll_opy_: bstack111lll1111_opy_,
            TestFramework.bstack1l1l1l1111l_opy_: test_name,
            TestFramework.bstack1l111ll111l_opy_: getattr(test, bstack11ll111_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤ᝕"), None),
            TestFramework.bstack11ll1l1l111_opy_: bstack11ll1111ll1_opy_,
            TestFramework.bstack11ll1l1l1l1_opy_: bstack1ll11l1llll_opy_.__11ll111ll11_opy_(test),
            TestFramework.bstack11ll1l11111_opy_: code,
            TestFramework.bstack1l11111l1l1_opy_: TestFramework.bstack11ll1111lll_opy_,
            TestFramework.bstack11lll1lllll_opy_: bstack111lll1111_opy_,
            TestFramework.bstack11l1lll1111_opy_: bstack11l1lll1l11_opy_
        }
    @staticmethod
    def __11ll111ll11_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11ll111_opy_ (u"ࠥࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠣ᝖"), [])
            markers.extend([getattr(m, bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᝗"), None) for m in own_markers if getattr(m, bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᝘"), None)])
            current = getattr(current, bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨ᝙"), None)
        return markers
    @staticmethod
    def __11l1lllll1l_opy_(location):
        return bstack11ll111_opy_ (u"ࠢ࠻࠼ࠥ᝚").join(filter(lambda x: isinstance(x, str), location))