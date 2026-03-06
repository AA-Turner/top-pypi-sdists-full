# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1ll1ll1l111_opy_, bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll11ll111l_opy_, TestHookState, bstack1ll11lllll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l111l1ll1l_opy_, bstack1l111l11lll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l11l1l1ll1_opy_ = [bstack1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᒔ"), bstack1111_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᒕ"), bstack1111_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᒖ"), bstack1111_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣᒗ"), bstack1111_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᒘ")]
bstack1l11ll111ll_opy_ = bstack1l111l11lll_opy_()
bstack1l11ll11ll1_opy_ = bstack1111_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᒙ")
bstack1l111l111ll_opy_ = {
    bstack1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡍࡹ࡫࡭ࠣᒚ"): bstack1l11l1l1ll1_opy_,
    bstack1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡕࡧࡣ࡬ࡣࡪࡩࠧᒛ"): bstack1l11l1l1ll1_opy_,
    bstack1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡓ࡯ࡥࡷ࡯ࡩࠧᒜ"): bstack1l11l1l1ll1_opy_,
    bstack1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡃ࡭ࡣࡶࡷࠧᒝ"): bstack1l11l1l1ll1_opy_,
    bstack1111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡇࡷࡱࡧࡹ࡯࡯࡯ࠤᒞ"): bstack1l11l1l1ll1_opy_
    + [
        bstack1111_opy_ (u"ࠣࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡱࡥࡲ࡫ࠢᒟ"),
        bstack1111_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᒠ"),
        bstack1111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨ࡭ࡳ࡬࡯ࠣᒡ"),
        bstack1111_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᒢ"),
        bstack1111_opy_ (u"ࠧࡩࡡ࡭࡮ࡶࡴࡪࡩࠢᒣ"),
        bstack1111_opy_ (u"ࠨࡣࡢ࡮࡯ࡳࡧࡰࠢᒤ"),
        bstack1111_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᒥ"),
        bstack1111_opy_ (u"ࠣࡵࡷࡳࡵࠨᒦ"),
        bstack1111_opy_ (u"ࠤࡧࡹࡷࡧࡴࡪࡱࡱࠦᒧ"),
        bstack1111_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᒨ"),
    ],
    bstack1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡩ࡯࠰ࡖࡩࡸࡹࡩࡰࡰࠥᒩ"): [bstack1111_opy_ (u"ࠧࡹࡴࡢࡴࡷࡴࡦࡺࡨࠣᒪ"), bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡷ࡫ࡧࡩ࡭ࡧࡧࠦᒫ"), bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡸࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣᒬ"), bstack1111_opy_ (u"ࠣ࡫ࡷࡩࡲࡹࠢᒭ")],
    bstack1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡦࡳࡳ࡬ࡩࡨ࠰ࡆࡳࡳ࡬ࡩࡨࠤᒮ"): [bstack1111_opy_ (u"ࠥ࡭ࡳࡼ࡯ࡤࡣࡷ࡭ࡴࡴ࡟ࡱࡣࡵࡥࡲࡹࠢᒯ"), bstack1111_opy_ (u"ࠦࡦࡸࡧࡴࠤᒰ")],
    bstack1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡇ࡫ࡻࡸࡺࡸࡥࡅࡧࡩࠦᒱ"): [bstack1111_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᒲ"), bstack1111_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᒳ"), bstack1111_opy_ (u"ࠣࡨࡸࡲࡨࠨᒴ"), bstack1111_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᒵ"), bstack1111_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᒶ"), bstack1111_opy_ (u"ࠦ࡮ࡪࡳࠣᒷ")],
    bstack1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡔࡷࡥࡖࡪࡷࡵࡦࡵࡷࠦᒸ"): [bstack1111_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᒹ"), bstack1111_opy_ (u"ࠢࡱࡣࡵࡥࡲࠨᒺ"), bstack1111_opy_ (u"ࠣࡲࡤࡶࡦࡳ࡟ࡪࡰࡧࡩࡽࠨᒻ")],
    bstack1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡵࡹࡳࡴࡥࡳ࠰ࡆࡥࡱࡲࡉ࡯ࡨࡲࠦᒼ"): [bstack1111_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᒽ"), bstack1111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࠦᒾ")],
    bstack1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡏࡱࡧࡩࡐ࡫ࡹࡸࡱࡵࡨࡸࠨᒿ"): [bstack1111_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᓀ"), bstack1111_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᓁ")],
    bstack1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡑࡦࡸ࡫ࠣᓂ"): [bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᓃ"), bstack1111_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᓄ"), bstack1111_opy_ (u"ࠦࡰࡽࡡࡳࡩࡶࠦᓅ")],
}
_1l111l1l11l_opy_ = set()
class bstack11111lll1_opy_(bstack1ll111l1l1l_opy_):
    bstack1l11l111l11_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࠧᓆ")
    bstack1l11l1lll11_opy_ = bstack1111_opy_ (u"ࠨࡉࡏࡈࡒࠦᓇ")
    bstack1l11ll111l1_opy_ = bstack1111_opy_ (u"ࠢࡆࡔࡕࡓࡗࠨᓈ")
    bstack1l111ll1lll_opy_: Callable
    bstack1l1111lllll_opy_: Callable
    def __init__(self, bstack1ll1l1111ll_opy_, bstack1ll11l1lll1_opy_):
        super().__init__()
        self.bstack1l1l1lll111_opy_ = bstack1ll11l1lll1_opy_
        if os.getenv(bstack1111_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡐ࠳࠴࡝ࠧᓉ"), bstack1111_opy_ (u"ࠤ࠴ࠦᓊ")) != bstack1111_opy_ (u"ࠥ࠵ࠧᓋ") or not self.is_enabled():
            return
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l11ll_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1ll111ll1_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1ll1111ll_opy_((event, state), self.bstack1l11l1ll1ll_opy_)
        bstack1ll1l1111ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.POST), self.bstack1l111ll111l_opy_)
        self.bstack1l111ll1lll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11l1l11l1_opy_(bstack11111lll1_opy_.bstack1l11l1lll11_opy_, self.bstack1l111ll1lll_opy_)
        self.bstack1l1111lllll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11l1l11l1_opy_(bstack11111lll1_opy_.bstack1l11ll111l1_opy_, self.bstack1l1111lllll_opy_)
        self.bstack1l111ll1ll1_opy_ = builtins.print
        builtins.print = self.bstack1l11l1lll1l_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l111l1ll11_opy_() or f.bstack1l11l11l111_opy_()) and instance:
            bstack1l11l11l11l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1ll1ll1l_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1l1llll111_opy_ = datetime.now()
                entries = f.bstack1l11l11111l_opy_(instance, bstack1ll1ll1ll1l_opy_)
                if entries:
                    self.bstack1l11l1l1lll_opy_(instance, entries)
                    instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦᓌ"), datetime.now() - bstack1l1llll111_opy_)
                    f.bstack1l11l11ll11_opy_(instance, bstack1ll1ll1ll1l_opy_)
                instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣᓍ"), datetime.now() - bstack1l11l11l11l_opy_)
                return # bstack1l11l1ll1l1_opy_ not send this event with the bstack1l111lll1l1_opy_ bstack1l111lllll1_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l111ll1l11_opy_)
            ):
                f.bstack1lll1l11l1l_opy_(instance, bstack11111lll1_opy_.bstack1l11l111l11_opy_, True)
                return # bstack1l11l1ll1l1_opy_ not send this event bstack1l11ll11l1l_opy_ bstack1l11ll11lll_opy_
            elif (
                f.bstack1lll1l11111_opy_(instance, bstack11111lll1_opy_.bstack1l11l111l11_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l111ll1l11_opy_)
            ):
                self.bstack1l11l1ll1ll_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1l1llll111_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l111l1ll11_opy_():
                bstack1l11l1l11ll_opy_ = sorted(
                    filter(lambda x: x.get(bstack1111_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᓎ"), None), data.pop(bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᓏ"), {}).values()),
                    key=lambda x: x[bstack1111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᓐ")],
                )
                data.update({bstack1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᓑ"): bstack1l11l1l11ll_opy_})
            elif f.bstack1l11l11l111_opy_():
                bstack1l11l11l1l1_opy_ = sorted(
                    filter(lambda x: x.get(bstack1111_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᓒ"), None), data.pop(bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᓓ"), {}).values()),
                    key=lambda x: x[bstack1111_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᓔ")],
                )
                data.update({bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᓕ"): bstack1l11l11l1l1_opy_})
            if bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_ in data:
                data.pop(bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_)
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᓖ"), datetime.now() - bstack1l1llll111_opy_)
            bstack1l1llll111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11l1l1l1l_opy_)
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᓗ"), datetime.now() - bstack1l1llll111_opy_)
            if TestFramework.bstack1l1l11l1l1l_opy_ in data:
                self.bstack1l111lllll1_opy_(instance, bstack1ll1ll1ll1l_opy_, event_json=event_json)
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᓘ"), datetime.now() - bstack1l11l11l11l_opy_)
    def bstack1l1l11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
        bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1llll111l1_opy_.value)
        self.bstack1l1l1lll111_opy_.bstack1l11l1111ll_opy_(instance, f, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1l1lll111_opy_.bstack1l11l111111_opy_(instance, f, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷࠤ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡡࡻࡾ࡟ࠣࡿࢂࡢ࡮ࡼࡿࠥᓙ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l11l11lll1_opy_ data not ready for robot-playwright at the time of bstack1l1l11l11ll_opy_, so bstack1l111l11111_opy_ will send bstack1l11l11lll1_opy_ event in bstack1l1ll111ll1_opy_ for robot-playwright
            self.bstack1l111llllll_opy_(f, instance, req)
        bstack1l11l1ll_opy_.end(EVENTS.bstack1llll111l1_opy_.value, bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᓚ"), bstack1l1l1llll1_opy_ + bstack1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᓛ"), status=True, failure=None, test_name=None)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll1l11111_opy_(instance, self.bstack1l1l1lll111_opy_.bstack1l111lll1ll_opy_, False):
            try:
                req = self.bstack1l1l1lll111_opy_.bstack1l11l111111_opy_(instance, f, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࠦࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡜ࡽࢀࡡࠥࢁࡽ࡝ࡰࡾࢁࠧᓜ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l111llllll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l111lll11l_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l111llllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥᓝ"))
            return
        bstack1l1llll111_opy_ = datetime.now()
        try:
            r = self.bstack1lll111l111_opy_.TestSessionEvent(req)
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤᓞ"), datetime.now() - bstack1l1llll111_opy_)
            f.bstack1lll1l11l1l_opy_(instance, self.bstack1l1l1lll111_opy_.bstack1l111lll1ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᓟ") + str(r) + bstack1111_opy_ (u"ࠥࠦᓠ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᓡ") + str(e) + bstack1111_opy_ (u"ࠧࠨᓢ"))
            traceback.print_exc()
            raise e
    def bstack1l111ll111l_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        _1l11l111lll_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll11l11111_opy_.bstack1l1l111l1ll_opy_(method_name):
            return
        if f.bstack1l1l1l11lll_opy_(*args) == bstack1ll11l11111_opy_.bstack1l111ll1l1l_opy_:
            bstack1l11l11l11l_opy_ = datetime.now()
            screenshot = result.get(bstack1111_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᓣ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1111_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲࠣᓤ"))
                return
            bstack1l111ll11l1_opy_ = self.bstack1l111l1l1ll_opy_(instance)
            if bstack1l111ll11l1_opy_:
                entry = bstack1ll11lllll1_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l11l1l1lll_opy_(bstack1l111ll11l1_opy_, [entry])
                instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤᓥ"), datetime.now() - bstack1l11l11l11l_opy_)
            else:
                self.logger.warning(bstack1111_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢᓦ").format(instance.ref()))
        event = {}
        bstack1l111ll11l1_opy_ = self.bstack1l111l1l1ll_opy_(instance)
        if bstack1l111ll11l1_opy_:
            self.bstack1l11ll1111l_opy_(event, bstack1l111ll11l1_opy_)
            if event.get(bstack1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᓧ")):
                self.bstack1l11l1l1lll_opy_(bstack1l111ll11l1_opy_, event[bstack1111_opy_ (u"ࠦࡱࡵࡧࡴࠤᓨ")])
            else:
                self.logger.debug(bstack1111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤᓩ"))
    @measure(event_name=EVENTS.bstack1l11ll11111_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l11l1l1lll_opy_(
        self,
        bstack1l111ll11l1_opy_: bstack1ll11ll111l_opy_,
        entries: List[bstack1ll11lllll1_opy_],
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l11l1ll1_opy_)
        req.client_worker_id = bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᓪ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll11l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll11l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll11l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l1111l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l111llll11_opy_)
            log_entry.uuid = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1l11l1l1l_opy_)
            log_entry.test_framework_state = bstack1l111ll11l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᓫ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᓬ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111l11ll1_opy_
                log_entry.file_path = entry.bstack1llll_opy_
        def bstack1l111ll1111_opy_():
            bstack1l1llll111_opy_ = datetime.now()
            try:
                self.bstack1lll111l111_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l111ll11l1_opy_.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᓭ"), datetime.now() - bstack1l1llll111_opy_)
                elif entry.kind == TestFramework.bstack1l11l111ll1_opy_:
                    bstack1l111ll11l1_opy_.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᓮ"), datetime.now() - bstack1l1llll111_opy_)
                else:
                    bstack1l111ll11l1_opy_.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣᓯ"), datetime.now() - bstack1l1llll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᓰ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1lllll1l_opy_.enqueue(bstack1l111ll1111_opy_)
    @measure(event_name=EVENTS.bstack1l11ll11l11_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l111lllll1_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1ll1_opy_)
        req.client_worker_id = bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᓱ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l111llll11_opy_)
        req.test_framework_state = bstack1ll1ll1ll1l_opy_[0].name
        req.test_hook_state = bstack1ll1ll1ll1l_opy_[1].name
        started_at = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l11l1lllll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11l1l1l1l_opy_)).encode(bstack1111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᓲ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l111ll1111_opy_():
            bstack1l1llll111_opy_ = datetime.now()
            try:
                self.bstack1lll111l111_opy_.TestFrameworkEvent(req)
                instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦᓳ"), datetime.now() - bstack1l1llll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᓴ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1lllll1l_opy_.enqueue(bstack1l111ll1111_opy_)
    def bstack1l111l1l1ll_opy_(self, instance: bstack1ll1ll1l111_opy_):
        bstack1l1111llll1_opy_ = TestFramework.bstack1ll1l1ll11l_opy_(instance.context)
        for t in bstack1l1111llll1_opy_:
            bstack1l111l1l111_opy_ = TestFramework.bstack1lll1l11111_opy_(t, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
            if not bstack1l111l1ll1l_opy_() and len(bstack1l111l1l111_opy_) == 0:
                bstack1l111l1l111_opy_ = TestFramework.bstack1lll1l11111_opy_(t, bstack1ll1l111l1l_opy_.bstack1l111l1llll_opy_, [])
            if any(instance is d[1] for d in bstack1l111l1l111_opy_):
                return t
    def bstack1l11l11l1ll_opy_(self, message):
        self.bstack1l111ll1lll_opy_(message + bstack1111_opy_ (u"ࠥࡠࡳࠨᓵ"))
    def log_error(self, message):
        self.bstack1l1111lllll_opy_(message + bstack1111_opy_ (u"ࠦࡡࡴࠢᓶ"))
    def bstack1l11l1l11l1_opy_(self, level, original_func):
        def bstack1l11l111l1l_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1111_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨᓷ") in message or bstack1111_opy_ (u"ࠨ࡛ࡔࡆࡎࡇࡑࡏ࡝ࠣᓸ") in message or bstack1111_opy_ (u"ࠢ࡜࡙ࡨࡦࡉࡸࡩࡷࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠦᓹ") in message:
                        return return_value
                    bstack1l1111llll1_opy_ = TestFramework.bstack1l11l1llll1_opy_()
                    if not bstack1l1111llll1_opy_:
                        return return_value
                    bstack1l111ll11l1_opy_ = next(
                        (
                            instance
                            for instance in bstack1l1111llll1_opy_
                            if TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111ll11l1_opy_:
                        return return_value
                    entry = bstack1ll11lllll1_opy_(TestFramework.bstack1l111l1l1l1_opy_, message, level)
                    self.bstack1l11l1l1lll_opy_(bstack1l111ll11l1_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l11l111l1l_opy_
    def bstack1l11l1lll1l_opy_(self):
        def bstack1l111llll1l_opy_(*args, **kwargs):
            try:
                self.bstack1l111ll1ll1_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1111_opy_ (u"ࠨࠢࠪᓺ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1111_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᓻ") in message:
                    return
                bstack1l1111llll1_opy_ = TestFramework.bstack1l11l1llll1_opy_()
                if not bstack1l1111llll1_opy_:
                    return
                bstack1l111ll11l1_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1111llll1_opy_
                        if TestFramework.bstack1ll1l1l1ll1_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_)
                    ),
                    None,
                )
                if not bstack1l111ll11l1_opy_:
                    return
                entry = bstack1ll11lllll1_opy_(TestFramework.bstack1l111l1l1l1_opy_, message, bstack11111lll1_opy_.bstack1l11l1lll11_opy_)
                self.bstack1l11l1l1lll_opy_(bstack1l111ll11l1_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111ll1ll1_opy_(bstack1ll1l1l11l1_opy_ (u"ࠥ࡟ࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠦࡌࡰࡩࠣࡧࡦࡶࡴࡶࡴࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣᓼ"))
                except:
                    pass
        return bstack1l111llll1l_opy_
    def bstack1l11ll1111l_opy_(self, event: dict, instance=None) -> None:
        global _1l111l1l11l_opy_
        levels = [bstack1111_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᓽ"), bstack1111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᓾ")]
        bstack1l11l1ll111_opy_ = bstack1111_opy_ (u"ࠨࠢᓿ")
        if instance is not None:
            try:
                bstack1l11l1ll111_opy_ = TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_)
            except Exception as e:
                self.logger.warning(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᔀ").format(e))
        bstack1l11l11llll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᔁ")]
                bstack1l111l111l1_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l11ll11ll1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l111l111l1_opy_):
                    self.logger.debug(bstack1111_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᔂ").format(bstack1l111l111l1_opy_))
                    continue
                file_names = os.listdir(bstack1l111l111l1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l111l111l1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l111l1l11l_opy_:
                        self.logger.info(bstack1111_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᔃ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l11l1ll11l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l11l1ll11l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1111_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᔄ"):
                                entry = bstack1ll11lllll1_opy_(
                                    kind=bstack1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᔅ"),
                                    message=bstack1111_opy_ (u"ࠨࠢᔆ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l111l11ll1_opy_=file_size,
                                    bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᔇ"),
                                    bstack1llll_opy_=os.path.abspath(file_path),
                                    bstack1ll111ll1l_opy_=bstack1l11l1ll111_opy_
                                )
                            elif level == bstack1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᔈ"):
                                entry = bstack1ll11lllll1_opy_(
                                    kind=bstack1111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᔉ"),
                                    message=bstack1111_opy_ (u"ࠥࠦᔊ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l111l11ll1_opy_=file_size,
                                    bstack1l11ll1l111_opy_=bstack1111_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᔋ"),
                                    bstack1llll_opy_=os.path.abspath(file_path),
                                    bstack1l111l1111l_opy_=bstack1l11l1ll111_opy_
                                )
                            bstack1l11l11llll_opy_.append(entry)
                            _1l111l1l11l_opy_.add(abs_path)
                        except Exception as bstack1l11l11ll1l_opy_:
                            self.logger.error(bstack1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᔌ").format(bstack1l11l11ll1l_opy_))
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᔍ").format(e))
        event[bstack1111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᔎ")] = bstack1l11l11llll_opy_
class bstack1l11l1l1l1l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l11l1l1l11_opy_ = set()
        kwargs[bstack1111_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥᔏ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l111l11l11_opy_(obj, self.bstack1l11l1l1l11_opy_)
def bstack1l111lll111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l111l11l11_opy_(obj, bstack1l11l1l1l11_opy_=None, max_depth=3):
    if bstack1l11l1l1l11_opy_ is None:
        bstack1l11l1l1l11_opy_ = set()
    if id(obj) in bstack1l11l1l1l11_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l11l1l1l11_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111l11l1l_opy_ = TestFramework.bstack1l11l1l1111_opy_(obj)
    bstack1l111l1lll1_opy_ = next((k.lower() in bstack1l111l11l1l_opy_.lower() for k in bstack1l111l111ll_opy_.keys()), None)
    if bstack1l111l1lll1_opy_:
        obj = TestFramework.bstack1l111ll11ll_opy_(obj, bstack1l111l111ll_opy_[bstack1l111l1lll1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1111_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᔐ")):
            keys = getattr(obj, bstack1111_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᔑ"), [])
        elif hasattr(obj, bstack1111_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᔒ")):
            keys = getattr(obj, bstack1111_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᔓ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1111_opy_ (u"ࠨ࡟ࠣᔔ"))}
        if not obj and bstack1l111l11l1l_opy_ == bstack1111_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦᔕ"):
            obj = {bstack1111_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᔖ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111lll111_opy_(key) or str(key).startswith(bstack1111_opy_ (u"ࠤࡢࠦᔗ")):
            continue
        if value is not None and bstack1l111lll111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l111l11l11_opy_(value, bstack1l11l1l1l11_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l111l11l11_opy_(o, bstack1l11l1l1l11_opy_, max_depth) for o in value]))
    return result or None