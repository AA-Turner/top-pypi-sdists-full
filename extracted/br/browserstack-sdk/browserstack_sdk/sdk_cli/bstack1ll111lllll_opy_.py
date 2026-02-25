# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import threading
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l111_opy_ import bstack11ll1l11ll1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1l1llllll1l_opy_,
    bstack1l1llll111l_opy_,
    bstack1ll11lll1ll_opy_,
    bstack11ll111l11l_opy_,
    bstack1ll11l111l1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l11ll1111l_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll11llll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1l1111ll_opy_ import bstack1ll11l1l1l1_opy_
from bstack_utils.bstack1111lll11l_opy_ import bstack1l111111_opy_
bstack1l111lll1l1_opy_ = bstack1l11ll1111l_opy_()
bstack11ll11ll111_opy_ = 1.0
bstack1l11lll1111_opy_ = bstack11l1l11_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᚺ")
bstack11l1lll1l11_opy_ = bstack11l1l11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᚻ")
bstack11l1lll111l_opy_ = bstack11l1l11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᚼ")
bstack11l1lll1111_opy_ = bstack11l1l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᚽ")
bstack11l1lll11ll_opy_ = bstack11l1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᚾ")
_1l11l11ll1l_opy_ = set()
class bstack1ll11ll11l1_opy_(TestFramework):
    bstack11l1llll1ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᚿ")
    bstack11ll11lllll_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠧᛀ")
    bstack11ll1111l1l_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠢᛁ")
    bstack11l1lllll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠦᛂ")
    bstack11ll1llllll_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩࠨᛃ")
    bstack11ll1lllll1_opy_: bool
    bstack1lll1l11111_opy_: bstack1lll11llll1_opy_  = None
    bstack1ll1ll11111_opy_ = None
    bstack11lll111ll1_opy_ = [
        bstack1l1llllll1l_opy_.BEFORE_ALL,
        bstack1l1llllll1l_opy_.AFTER_ALL,
        bstack1l1llllll1l_opy_.BEFORE_EACH,
        bstack1l1llllll1l_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11ll111ll1l_opy_: Dict[str, str],
        bstack1l1l1ll1ll1_opy_: List[str]=[bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᛄ")],
        bstack1lll1l11111_opy_: bstack1lll11llll1_opy_=None,
        bstack1ll1ll11111_opy_=None
    ):
        super().__init__(bstack1l1l1ll1ll1_opy_, bstack11ll111ll1l_opy_, bstack1lll1l11111_opy_)
        self.bstack11ll1lllll1_opy_ = any(bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᛅ") in item.lower() for item in bstack1l1l1ll1ll1_opy_)
        self.bstack1ll1ll11111_opy_ = bstack1ll1ll11111_opy_
    def track_event(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1l1llllll1l_opy_.TEST or test_framework_state in bstack1ll11ll11l1_opy_.bstack11lll111ll1_opy_:
            bstack11ll1l11ll1_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1l1llllll1l_opy_.NONE:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࠢᛆ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠢࠣᛇ"))
            return
        if not self.bstack11ll1lllll1_opy_:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠾ࠤᛈ") + str(str(self.bstack1l1l1ll1ll1_opy_)) + bstack11l1l11_opy_ (u"ࠤࠥᛉ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᛊ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧᛋ"))
            return
        instance = self.__11ll1111111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡧࡲࡨࡵࡀࠦᛌ") + str(args) + bstack11l1l11_opy_ (u"ࠨࠢᛍ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll11ll11l1_opy_.bstack11lll111ll1_opy_:
                bstack1l1l1l1111_opy_ = bstack11l1l11_opy_ (u"ࠢࠣᛎ")
                name = bstack11l1l11_opy_ (u"ࠣࠤᛏ")
                if (test_hook_state == bstack1ll11lll1ll_opy_.PRE):
                    bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11l1lll1lll_opy_.value)
                    name = str(EVENTS.bstack11l1lll1lll_opy_.name)+bstack11l1l11_opy_ (u"ࠤ࠽ࠦᛐ")+str(test_framework_state.name)
                else:
                    bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack11l1lll1ll1_opy_.value)
                    name = str(EVENTS.bstack11l1lll1ll1_opy_.name)+bstack11l1l11_opy_ (u"ࠥ࠾ࠧᛑ")+str(test_framework_state.name)
                TestFramework.bstack11ll11llll1_opy_(instance, name, bstack1l1l1l1111_opy_)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᛒ").format(e))
        try:
            if not TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack11l1lllll1l_opy_) and test_hook_state == bstack1ll11lll1ll_opy_.PRE:
                test = bstack1ll11ll11l1_opy_.__11ll1111ll1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᛓ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠨࠢᛔ"))
            if test_framework_state == bstack1l1llllll1l_opy_.TEST:
                if test_hook_state == bstack1ll11lll1ll_opy_.PRE and not TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11l11l11l_opy_):
                    TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11l11l11l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᛕ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠣࠤᛖ"))
                elif test_hook_state == bstack1ll11lll1ll_opy_.POST and not TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11llllll1_opy_):
                    TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11llllll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᛗ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠥࠦᛘ"))
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG and test_hook_state == bstack1ll11lll1ll_opy_.POST:
                bstack1ll11ll11l1_opy_.__11ll1ll1111_opy_(instance, *args)
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG_REPORT and test_hook_state == bstack1ll11lll1ll_opy_.POST:
                self.__11ll1l111ll_opy_(instance, *args)
                self.__11ll11ll1ll_opy_(instance)
            elif test_framework_state in bstack1ll11ll11l1_opy_.bstack11lll111ll1_opy_:
                self.__11ll1ll1l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᛙ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠧࠨᛚ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11ll1l111l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll11ll11l1_opy_.bstack11lll111ll1_opy_:
                bstack1l1l1l1111_opy_ = bstack11l1l11_opy_ (u"ࠨࠢᛛ")
                name = bstack11l1l11_opy_ (u"ࠢࠣᛜ")
                if (test_hook_state == bstack1ll11lll1ll_opy_.PRE):
                    name = str(EVENTS.bstack11l1lll1lll_opy_.name)+bstack11l1l11_opy_ (u"ࠣ࠼ࠥᛝ")+str(test_framework_state.name)
                    bstack1l1l1l1111_opy_ = TestFramework.bstack11ll1ll11l1_opy_(instance, name)
                    bstack11ll1l1l1_opy_.end(EVENTS.bstack11l1lll1lll_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛞ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛟ"), True, None, test_framework_state.name)
                else:
                    name = str(EVENTS.bstack11l1lll1ll1_opy_.name)+bstack11l1l11_opy_ (u"ࠦ࠿ࠨᛠ")+str(test_framework_state.name)
                    bstack1l1l1l1111_opy_ = TestFramework.bstack11ll1ll11l1_opy_(instance, name)
                    bstack11ll1l1l1_opy_.end(EVENTS.bstack11l1lll1ll1_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᛡ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᛢ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᛣ").format(e))
    def bstack1l11ll111l1_opy_(self):
        return self.bstack11ll1lllll1_opy_
    def __11ll1ll111l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᛤ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l11l111111_opy_(rep, [bstack11l1l11_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᛥ"), bstack11l1l11_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᛦ"), bstack11l1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᛧ"), bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᛨ"), bstack11l1l11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠢᛩ"), bstack11l1l11_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᛪ")])
        return None
    def __11ll1l111ll_opy_(self, instance: bstack1l1llll111l_opy_, *args):
        result = self.__11ll1ll111l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1lll1ll1l11_opy_ = None
        if result.get(bstack11l1l11_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤ᛫"), None) == bstack11l1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ᛬") and len(args) > 1 and getattr(args[1], bstack11l1l11_opy_ (u"ࠥࡩࡽࡩࡩ࡯ࡨࡲࠦ᛭"), None) is not None:
            failure = [{bstack11l1l11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᛮ"): [args[1].excinfo.exconly(), result.get(bstack11l1l11_opy_ (u"ࠧࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠦᛯ"), None)]}]
            bstack1lll1ll1l11_opy_ = bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᛰ") if bstack11l1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᛱ") in getattr(args[1].excinfo, bstack11l1l11_opy_ (u"ࠣࡶࡼࡴࡪࡴࡡ࡮ࡧࠥᛲ"), bstack11l1l11_opy_ (u"ࠤࠥᛳ")) else bstack11l1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᛴ")
        bstack11ll1l1111l_opy_ = result.get(bstack11l1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᛵ"), TestFramework.bstack11ll111ll11_opy_)
        if bstack11ll1l1111l_opy_ != TestFramework.bstack11ll111ll11_opy_:
            TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack11ll1l11111_opy_(instance, {
            TestFramework.bstack1l111111lll_opy_: failure,
            TestFramework.bstack11ll111llll_opy_: bstack1lll1ll1l11_opy_,
            TestFramework.bstack1l1111l11l1_opy_: bstack11ll1l1111l_opy_,
        })
    def __11ll1111111_opy_(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1l1llllll1l_opy_.SETUP_FIXTURE:
            instance = self.__11ll1l1l1l1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11ll1lll11l_opy_ bstack11ll11111ll_opy_ this to be bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᛶ")
            if test_framework_state == bstack1l1llllll1l_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__11ll11lll11_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᛷ"), None), bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᛸ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11l1l11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᛹"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1lll11ll11l_opy_(target) if target else None
        return instance
    def __11ll1ll1l11_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11ll111l1ll_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack1ll11ll11l1_opy_.bstack11ll11lllll_opy_, {})
        if not key in bstack11ll111l1ll_opy_:
            bstack11ll111l1ll_opy_[key] = []
        bstack11ll11l11ll_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack1ll11ll11l1_opy_.bstack11ll1111l1l_opy_, {})
        if not key in bstack11ll11l11ll_opy_:
            bstack11ll11l11ll_opy_[key] = []
        bstack11ll11ll1l1_opy_ = {
            bstack1ll11ll11l1_opy_.bstack11ll11lllll_opy_: bstack11ll111l1ll_opy_,
            bstack1ll11ll11l1_opy_.bstack11ll1111l1l_opy_: bstack11ll11l11ll_opy_,
        }
        if test_hook_state == bstack1ll11lll1ll_opy_.PRE:
            hook = {
                bstack11l1l11_opy_ (u"ࠤ࡮ࡩࡾࠨ᛺"): key,
                TestFramework.bstack11l1llllll1_opy_: uuid4().__str__(),
                TestFramework.bstack11ll1ll1lll_opy_: TestFramework.bstack11ll11111l1_opy_,
                TestFramework.bstack11ll1llll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11ll11lll1l_opy_: [],
                TestFramework.bstack11ll111111l_opy_: args[1] if len(args) > 1 else bstack11l1l11_opy_ (u"ࠪࠫ᛻"),
                TestFramework.bstack11lll1111l1_opy_: bstack1ll11l1l1l1_opy_.bstack11ll11l111l_opy_()
            }
            bstack11ll111l1ll_opy_[key].append(hook)
            bstack11ll11ll1l1_opy_[bstack1ll11ll11l1_opy_.bstack11l1lllll11_opy_] = key
        elif test_hook_state == bstack1ll11lll1ll_opy_.POST:
            bstack11ll1l1ll1l_opy_ = bstack11ll111l1ll_opy_.get(key, [])
            hook = bstack11ll1l1ll1l_opy_.pop() if bstack11ll1l1ll1l_opy_ else None
            if hook:
                result = self.__11ll1ll111l_opy_(*args)
                if result:
                    bstack11ll1l1l11l_opy_ = result.get(bstack11l1l11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧ᛼"), TestFramework.bstack11ll11111l1_opy_)
                    if bstack11ll1l1l11l_opy_ != TestFramework.bstack11ll11111l1_opy_:
                        hook[TestFramework.bstack11ll1ll1lll_opy_] = bstack11ll1l1l11l_opy_
                hook[TestFramework.bstack11lll111lll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack11lll1111l1_opy_]= bstack1ll11l1l1l1_opy_.bstack11ll11l111l_opy_()
                self.bstack11ll1ll1l1l_opy_(hook)
                logs = hook.get(TestFramework.bstack11ll11l1l1l_opy_, [])
                if logs: self.bstack1l11ll11111_opy_(instance, logs)
                bstack11ll11l11ll_opy_[key].append(hook)
                bstack11ll11ll1l1_opy_[bstack1ll11ll11l1_opy_.bstack11ll1llllll_opy_] = key
        TestFramework.bstack11ll1l11111_opy_(instance, bstack11ll11ll1l1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡭ࡵ࡯࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡱࡥࡺࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪ࠽ࡼࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡾࠢ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡀࠦ᛽") + str(bstack11ll11l11ll_opy_) + bstack11l1l11_opy_ (u"ࠨࠢ᛾"))
    def __11ll1l1l1l1_opy_(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l11l111111_opy_(args[0], [bstack11l1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᛿"), bstack11l1l11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᜀ"), bstack11l1l11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᜁ"), bstack11l1l11_opy_ (u"ࠥ࡭ࡩࡹࠢᜂ"), bstack11l1l11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᜃ"), bstack11l1l11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᜄ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᜅ")) else fixturedef.get(bstack11l1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᜆ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11l1l11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᜇ")) else None
        node = request.node if hasattr(request, bstack11l1l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᜈ")) else None
        target = request.node.nodeid if hasattr(node, bstack11l1l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᜉ")) else None
        baseid = fixturedef.get(bstack11l1l11_opy_ (u"ࠦࡧࡧࡳࡦ࡫ࡧࠦᜊ"), None) or bstack11l1l11_opy_ (u"ࠧࠨᜋ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11l1l11_opy_ (u"ࠨ࡟ࡱࡻࡩࡹࡳࡩࡩࡵࡧࡰࠦᜌ")):
            target = bstack1ll11ll11l1_opy_.__11ll1lll1ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11l1l11_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᜍ")) else None
            if target and not TestFramework.bstack1lll11ll11l_opy_(target):
                self.__11ll11lll11_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡧࡹࡩࡳࡺ࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࡿࠣࡲࡴࡪࡥ࠾ࡽࡱࡳࡩ࡫ࡽࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࠥᜎ") + str(test_hook_state) + bstack11l1l11_opy_ (u"ࠤࠥᜏ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡧࡩ࡫ࢃࠠࡴࡥࡲࡴࡪࡃࡻࡴࡥࡲࡴࡪࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᜐ") + str(target) + bstack11l1l11_opy_ (u"ࠦࠧᜑ"))
            return None
        instance = TestFramework.bstack1lll11ll11l_opy_(target)
        if not instance:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡧࡧࡳࡦ࡫ࡧࡁࢀࡨࡡࡴࡧ࡬ࡨࢂࠦࡴࡢࡴࡪࡩࡹࡃࠢᜒ") + str(target) + bstack11l1l11_opy_ (u"ࠨࠢᜓ"))
            return None
        bstack11ll111lll1_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack1ll11ll11l1_opy_.bstack11l1llll1ll_opy_, {})
        if os.getenv(bstack11l1l11_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡆࡊ࡚ࡗ࡙ࡗࡋࡓ᜔ࠣ"), bstack11l1l11_opy_ (u"ࠣ࠳᜕ࠥ")) == bstack11l1l11_opy_ (u"ࠤ࠴ࠦ᜖"):
            bstack11ll1lll111_opy_ = bstack11l1l11_opy_ (u"ࠥ࠾ࠧ᜗").join((scope, fixturename))
            bstack11lll11l111_opy_ = datetime.now(tz=timezone.utc)
            bstack11l1llll11l_opy_ = {
                bstack11l1l11_opy_ (u"ࠦࡰ࡫ࡹࠣ᜘"): bstack11ll1lll111_opy_,
                bstack11l1l11_opy_ (u"ࠧࡺࡡࡨࡵࠥ᜙"): bstack1ll11ll11l1_opy_.__11l1llll111_opy_(request.node),
                bstack11l1l11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࠢ᜚"): fixturedef,
                bstack11l1l11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨ᜛"): scope,
                bstack11l1l11_opy_ (u"ࠣࡶࡼࡴࡪࠨ᜜"): None,
            }
            try:
                if test_hook_state == bstack1ll11lll1ll_opy_.POST and callable(getattr(args[-1], bstack11l1l11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨ᜝"), None)):
                    bstack11l1llll11l_opy_[bstack11l1l11_opy_ (u"ࠥࡸࡾࡶࡥࠣ᜞")] = TestFramework.bstack1l11lll1l11_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll11lll1ll_opy_.PRE:
                bstack11l1llll11l_opy_[bstack11l1l11_opy_ (u"ࠦࡺࡻࡩࡥࠤᜟ")] = uuid4().__str__()
                bstack11l1llll11l_opy_[bstack1ll11ll11l1_opy_.bstack11ll1llll11_opy_] = bstack11lll11l111_opy_
            elif test_hook_state == bstack1ll11lll1ll_opy_.POST:
                bstack11l1llll11l_opy_[bstack1ll11ll11l1_opy_.bstack11lll111lll_opy_] = bstack11lll11l111_opy_
            if bstack11ll1lll111_opy_ in bstack11ll111lll1_opy_:
                bstack11ll111lll1_opy_[bstack11ll1lll111_opy_].update(bstack11l1llll11l_opy_)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࠨᜠ") + str(bstack11ll111lll1_opy_[bstack11ll1lll111_opy_]) + bstack11l1l11_opy_ (u"ࠨࠢᜡ"))
            else:
                bstack11ll111lll1_opy_[bstack11ll1lll111_opy_] = bstack11l1llll11l_opy_
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡴࡣࡹࡩࡩࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤ࡫࡯ࡸࡵࡷࡵࡩࡂࢁࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࢂࠦࡴࡳࡣࡦ࡯ࡪࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠿ࠥᜢ") + str(len(bstack11ll111lll1_opy_)) + bstack11l1l11_opy_ (u"ࠣࠤᜣ"))
        TestFramework.bstack1lll111ll11_opy_(instance, bstack1ll11ll11l1_opy_.bstack11l1llll1ll_opy_, bstack11ll111lll1_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࡿࡱ࡫࡮ࠩࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶ࠭ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᜤ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠥࠦᜥ"))
        return instance
    def __11ll11lll11_opy_(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1ll1llllll1_opy_.create_context(target)
        ob = bstack1l1llll111l_opy_(ctx, self.bstack1l1l1ll1ll1_opy_, self.bstack11ll111ll1l_opy_, test_framework_state)
        TestFramework.bstack11ll1l11111_opy_(ob, {
            TestFramework.bstack1l1ll1l1lll_opy_: context.test_framework_name,
            TestFramework.bstack1l11l1l11ll_opy_: context.test_framework_version,
            TestFramework.bstack11l1lllllll_opy_: [],
            bstack1ll11ll11l1_opy_.bstack11l1llll1ll_opy_: {},
            bstack1ll11ll11l1_opy_.bstack11ll1111l1l_opy_: {},
            bstack1ll11ll11l1_opy_.bstack11ll11lllll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1lll111ll11_opy_(ob, TestFramework.bstack11ll11l1lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1lll111ll11_opy_(ob, TestFramework.bstack1l1l1l1ll11_opy_, context.platform_index)
        TestFramework.bstack1ll1ll1ll1l_opy_[ctx.id] = ob
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡩࡴࡹ࠰࡬ࡨࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᜦ") + str(TestFramework.bstack1ll1ll1ll1l_opy_.keys()) + bstack11l1l11_opy_ (u"ࠧࠨᜧ"))
        return ob
    def bstack1l11ll1l11l_opy_(self, instance: bstack1l1llll111l_opy_, bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_]):
        bstack11ll1111l11_opy_ = (
            bstack1ll11ll11l1_opy_.bstack11l1lllll11_opy_
            if bstack1lll11ll111_opy_[1] == bstack1ll11lll1ll_opy_.PRE
            else bstack1ll11ll11l1_opy_.bstack11ll1llllll_opy_
        )
        hook = bstack1ll11ll11l1_opy_.bstack11ll1l1llll_opy_(instance, bstack11ll1111l11_opy_)
        entries = hook.get(TestFramework.bstack11ll11lll1l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11l1lllllll_opy_, []))
        return entries
    def bstack1l11l1ll1l1_opy_(self, instance: bstack1l1llll111l_opy_, bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_]):
        bstack11ll1111l11_opy_ = (
            bstack1ll11ll11l1_opy_.bstack11l1lllll11_opy_
            if bstack1lll11ll111_opy_[1] == bstack1ll11lll1ll_opy_.PRE
            else bstack1ll11ll11l1_opy_.bstack11ll1llllll_opy_
        )
        bstack1ll11ll11l1_opy_.bstack11ll11l1ll1_opy_(instance, bstack11ll1111l11_opy_)
        TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11l1lllllll_opy_, []).clear()
    def bstack11ll1ll1l1l_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡔࡷࡵࡣࡦࡵࡶࡩࡸࠦࡴࡩࡧࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡸ࡯࡭ࡪ࡮ࡤࡶࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡇ࡭࡫ࡣ࡬ࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡩ࡯ࡵ࡬ࡨࡪࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡆࡰࡴࠣࡩࡦࡩࡨࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠱ࠦࡲࡦࡲ࡯ࡥࡨ࡫ࡳࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣࠢ࡬ࡲࠥ࡯ࡴࡴࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡉࡧࠢࡤࠤ࡫࡯࡬ࡦࠢ࡬ࡲࠥࡺࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡳࡡࡵࡥ࡫ࡩࡸࠦࡡࠡ࡯ࡲࡨ࡮࡬ࡩࡦࡦࠣ࡬ࡴࡵ࡫࠮࡮ࡨࡺࡪࡲࠠࡧ࡫࡯ࡩ࠱ࠦࡩࡵࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࠠࡸ࡫ࡷ࡬ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡖ࡭ࡲ࡯࡬ࡢࡴ࡯ࡽ࠱ࠦࡩࡵࠢࡳࡶࡴࡩࡥࡴࡵࡨࡷࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠡ࡫ࡱࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡢࡺࠢࡵࡩࡵࡲࡡࡤ࡫ࡱ࡫ࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱࡚ࠥࡨࡦࠢࡦࡶࡪࡧࡴࡦࡦࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡡࡳࡧࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢ࡫ࡳࡴࡱࠧࡴࠢࠥࡰࡴ࡭ࡳࠣࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮࠾࡚ࠥࡨࡦࠢࡨࡺࡪࡴࡴࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡱࡵࡧࡴࠢࡤࡲࡩࠦࡨࡰࡱ࡮ࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡶ࡫࡯ࡨࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡱࡴࡴࡩࡵࡱࡵ࡭ࡳ࡭࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᜨ")
        global _1l11l11ll1l_opy_
        platform_index = os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᜩ")]
        bstack1l11l111l11_opy_ = os.path.join(bstack1l111lll1l1_opy_, (bstack1l11lll1111_opy_ + str(platform_index)), bstack11l1lll1111_opy_)
        if not os.path.exists(bstack1l11l111l11_opy_) or not os.path.isdir(bstack1l11l111l11_opy_):
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࡸࠦࡴࡰࠢࡳࡶࡴࡩࡥࡴࡵࠣࡿࢂࠨᜪ").format(bstack1l11l111l11_opy_))
            return
        logs = hook.get(bstack11l1l11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᜫ"), [])
        with os.scandir(bstack1l11l111l11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l11l11ll1l_opy_:
                    self.logger.info(bstack11l1l11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᜬ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11l1l11_opy_ (u"ࠦࠧᜭ")
                    log_entry = bstack1ll11l111l1_opy_(
                        kind=bstack11l1l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᜮ"),
                        message=bstack11l1l11_opy_ (u"ࠨࠢᜯ"),
                        level=bstack11l1l11_opy_ (u"ࠢࠣᜰ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l11lll1lll_opy_=entry.stat().st_size,
                        bstack1l11ll1lll1_opy_=bstack11l1l11_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᜱ"),
                        bstack1lll1ll_opy_=os.path.abspath(entry.path),
                        bstack11lll111111_opy_=hook.get(TestFramework.bstack11l1llllll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l11l11ll1l_opy_.add(abs_path)
        platform_index = os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᜲ")]
        bstack11ll111l1l1_opy_ = os.path.join(bstack1l111lll1l1_opy_, (bstack1l11lll1111_opy_ + str(platform_index)), bstack11l1lll1111_opy_, bstack11l1lll11ll_opy_)
        if not os.path.exists(bstack11ll111l1l1_opy_) or not os.path.isdir(bstack11ll111l1l1_opy_):
            self.logger.info(bstack11l1l11_opy_ (u"ࠥࡒࡴࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡦࡰࡷࡱࡨࠥࡧࡴ࠻ࠢࡾࢁࠧᜳ").format(bstack11ll111l1l1_opy_))
        else:
            self.logger.info(bstack11l1l11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿ᜴ࠥ").format(bstack11ll111l1l1_opy_))
            with os.scandir(bstack11ll111l1l1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l11l11ll1l_opy_:
                        self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ᜵").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11l1l11_opy_ (u"ࠨࠢ᜶")
                        log_entry = bstack1ll11l111l1_opy_(
                            kind=bstack11l1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᜷"),
                            message=bstack11l1l11_opy_ (u"ࠣࠤ᜸"),
                            level=bstack11l1l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨ᜹"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l11lll1lll_opy_=entry.stat().st_size,
                            bstack1l11ll1lll1_opy_=bstack11l1l11_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥ᜺"),
                            bstack1lll1ll_opy_=os.path.abspath(entry.path),
                            bstack1l11l1ll11l_opy_=hook.get(TestFramework.bstack11l1llllll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l11l11ll1l_opy_.add(abs_path)
        hook[bstack11l1l11_opy_ (u"ࠦࡱࡵࡧࡴࠤ᜻")] = logs
    def bstack1l11ll11111_opy_(
        self,
        bstack1l111llllll_opy_: bstack1l1llll111l_opy_,
        entries: List[bstack1ll11l111l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤ᜼"))
        req.platform_index = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᜽").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111llllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111llllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111llllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1ll1l1lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l11l1l11ll_opy_)
            log_entry.uuid = entry.bstack11lll111111_opy_
            log_entry.test_framework_state = bstack1l111llllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᜾"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11l1l11_opy_ (u"ࠣࠤ᜿")
            if entry.kind == bstack11l1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᝀ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11lll1lll_opy_
                log_entry.file_path = entry.bstack1lll1ll_opy_
        def bstack1l11l1l1lll_opy_():
            bstack111l11l1l1_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11111_opy_.LogCreatedEvent(req)
                bstack1l111llllll_opy_.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᝁ"), datetime.now() - bstack111l11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᝂ").format(str(e)))
                traceback.print_exc()
        self.bstack1lll1l11111_opy_.enqueue(bstack1l11l1l1lll_opy_)
    def __11ll11ll1ll_opy_(self, instance) -> None:
        bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᝃ")
        bstack11ll11ll1l1_opy_ = {bstack11l1l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᝄ"): bstack1ll11l1l1l1_opy_.bstack11ll11l111l_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack11ll1l11111_opy_(instance, bstack11ll11ll1l1_opy_)
    @staticmethod
    def bstack11ll1l1llll_opy_(instance: bstack1l1llll111l_opy_, bstack11ll1111l11_opy_: str):
        bstack11lll1111ll_opy_ = (
            bstack1ll11ll11l1_opy_.bstack11ll1111l1l_opy_
            if bstack11ll1111l11_opy_ == bstack1ll11ll11l1_opy_.bstack11ll1llllll_opy_
            else bstack1ll11ll11l1_opy_.bstack11ll11lllll_opy_
        )
        bstack11lll111l11_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11ll1111l11_opy_, None)
        bstack11ll1ll1ll1_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11lll1111ll_opy_, None) if bstack11lll111l11_opy_ else None
        return (
            bstack11ll1ll1ll1_opy_[bstack11lll111l11_opy_][-1]
            if isinstance(bstack11ll1ll1ll1_opy_, dict) and len(bstack11ll1ll1ll1_opy_.get(bstack11lll111l11_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack11ll11l1ll1_opy_(instance: bstack1l1llll111l_opy_, bstack11ll1111l11_opy_: str):
        hook = bstack1ll11ll11l1_opy_.bstack11ll1l1llll_opy_(instance, bstack11ll1111l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11ll11lll1l_opy_, []).clear()
    @staticmethod
    def __11ll1ll1111_opy_(instance: bstack1l1llll111l_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᝅ"), None)):
            return
        if os.getenv(bstack11l1l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᝆ"), bstack11l1l11_opy_ (u"ࠤ࠴ࠦᝇ")) != bstack11l1l11_opy_ (u"ࠥ࠵ࠧᝈ"):
            bstack1ll11ll11l1_opy_.logger.warning(bstack11l1l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᝉ"))
            return
        bstack11ll1l11l11_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᝊ"): (bstack1ll11ll11l1_opy_.bstack11l1lllll11_opy_, bstack1ll11ll11l1_opy_.bstack11ll11lllll_opy_),
            bstack11l1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᝋ"): (bstack1ll11ll11l1_opy_.bstack11ll1llllll_opy_, bstack1ll11ll11l1_opy_.bstack11ll1111l1l_opy_),
        }
        for when in (bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᝌ"), bstack11l1l11_opy_ (u"ࠣࡥࡤࡰࡱࠨᝍ"), bstack11l1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᝎ")):
            bstack11ll11l1111_opy_ = args[1].get_records(when)
            if not bstack11ll11l1111_opy_:
                continue
            records = [
                bstack1ll11l111l1_opy_(
                    kind=TestFramework.bstack1l111lll1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11l1l11_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᝏ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11l1l11_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᝐ")) and r.created
                        else None
                    ),
                )
                for r in bstack11ll11l1111_opy_
                if isinstance(getattr(r, bstack11l1l11_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᝑ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack11l1llll1l1_opy_, bstack11lll1111ll_opy_ = bstack11ll1l11l11_opy_.get(when, (None, None))
            bstack11ll111l111_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11l1llll1l1_opy_, None) if bstack11l1llll1l1_opy_ else None
            bstack11ll1ll1ll1_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, bstack11lll1111ll_opy_, None) if bstack11ll111l111_opy_ else None
            if isinstance(bstack11ll1ll1ll1_opy_, dict) and len(bstack11ll1ll1ll1_opy_.get(bstack11ll111l111_opy_, [])) > 0:
                hook = bstack11ll1ll1ll1_opy_[bstack11ll111l111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11ll11lll1l_opy_ in hook:
                    hook[TestFramework.bstack11ll11lll1l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack11l1lllllll_opy_, [])
            logs.extend(records)
    @staticmethod
    def __11ll1111ll1_opy_(test) -> Dict[str, Any]:
        bstack1l11l1lll_opy_ = bstack1ll11ll11l1_opy_.__11ll1lll1ll_opy_(test.location) if hasattr(test, bstack11l1l11_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᝒ")) else getattr(test, bstack11l1l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᝓ"), None)
        test_name = test.name if hasattr(test, bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᝔")) else None
        bstack11ll1l11l1l_opy_ = test.fspath.strpath if hasattr(test, bstack11l1l11_opy_ (u"ࠤࡩࡷࡵࡧࡴࡩࠤ᝕")) and test.fspath else None
        if not bstack1l11l1lll_opy_ or not test_name or not bstack11ll1l11l1l_opy_:
            return None
        code = None
        if hasattr(test, bstack11l1l11_opy_ (u"ࠥࡳࡧࡰࠢ᝖")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11l1lll11l1_opy_ = []
        try:
            bstack11l1lll11l1_opy_ = bstack1l111111_opy_.bstack111111lll1_opy_(test)
        except:
            bstack1ll11ll11l1_opy_.logger.warning(bstack11l1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵ࠯ࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡪࡹ࡯࡭ࡸࡨࡨࠥ࡯࡮ࠡࡅࡏࡍࠧ᝗"))
        return {
            TestFramework.bstack1l1l11lll11_opy_: uuid4().__str__(),
            TestFramework.bstack11l1lllll1l_opy_: bstack1l11l1lll_opy_,
            TestFramework.bstack1l1ll11llll_opy_: test_name,
            TestFramework.bstack1l111ll1111_opy_: getattr(test, bstack11l1l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧ᝘"), None),
            TestFramework.bstack11ll11ll11l_opy_: bstack11ll1l11l1l_opy_,
            TestFramework.bstack11ll1llll1l_opy_: bstack1ll11ll11l1_opy_.__11l1llll111_opy_(test),
            TestFramework.bstack11ll1l1l1ll_opy_: code,
            TestFramework.bstack1l1111l11l1_opy_: TestFramework.bstack11ll111ll11_opy_,
            TestFramework.bstack11lll1l1lll_opy_: bstack1l11l1lll_opy_,
            TestFramework.bstack11l1lll1l1l_opy_: bstack11l1lll11l1_opy_
        }
    @staticmethod
    def __11l1llll111_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11l1l11_opy_ (u"ࠨ࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠦ᝙"), [])
            markers.extend([getattr(m, bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᝚"), None) for m in own_markers if getattr(m, bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᝛"), None)])
            current = getattr(current, bstack11l1l11_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤ᝜"), None)
        return markers
    @staticmethod
    def __11ll1lll1ll_opy_(location):
        return bstack11l1l11_opy_ (u"ࠥ࠾࠿ࠨ᝝").join(filter(lambda x: isinstance(x, str), location))