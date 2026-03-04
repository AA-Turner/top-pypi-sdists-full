# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import bstack1ll1llll11l_opy_, bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111lll_opy_ import bstack1ll11ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111l1l1l_opy_, TestHookState, bstack1ll11ll1l1l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l11ll1l1l1_opy_, bstack1l111l11lll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l111ll1111_opy_ = [bstack1lll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᒓ"), bstack1lll1l_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᒔ"), bstack1lll1l_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧᒕ"), bstack1lll1l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࠢᒖ"), bstack1lll1l_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᒗ")]
bstack1l11l1lllll_opy_ = bstack1l111l11lll_opy_()
bstack1l111l1l111_opy_ = bstack1lll1l_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᒘ")
bstack1l11l1ll1l1_opy_ = {
    bstack1lll1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢᒙ"): bstack1l111ll1111_opy_,
    bstack1lll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦᒚ"): bstack1l111ll1111_opy_,
    bstack1lll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦᒛ"): bstack1l111ll1111_opy_,
    bstack1lll1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦᒜ"): bstack1l111ll1111_opy_,
    bstack1lll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣᒝ"): bstack1l111ll1111_opy_
    + [
        bstack1lll1l_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨᒞ"),
        bstack1lll1l_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᒟ"),
        bstack1lll1l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢᒠ"),
        bstack1lll1l_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᒡ"),
        bstack1lll1l_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨᒢ"),
        bstack1lll1l_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨᒣ"),
        bstack1lll1l_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᒤ"),
        bstack1lll1l_opy_ (u"ࠢࡴࡶࡲࡴࠧᒥ"),
        bstack1lll1l_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥᒦ"),
        bstack1lll1l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᒧ"),
    ],
    bstack1lll1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤᒨ"): [bstack1lll1l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢᒩ"), bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥᒪ"), bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᒫ"), bstack1lll1l_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨᒬ")],
    bstack1lll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣᒭ"): [bstack1lll1l_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨᒮ"), bstack1lll1l_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᒯ")],
    bstack1lll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥᒰ"): [bstack1lll1l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᒱ"), bstack1lll1l_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᒲ"), bstack1lll1l_opy_ (u"ࠢࡧࡷࡱࡧࠧᒳ"), bstack1lll1l_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᒴ"), bstack1lll1l_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᒵ"), bstack1lll1l_opy_ (u"ࠥ࡭ࡩࡹࠢᒶ")],
    bstack1lll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥᒷ"): [bstack1lll1l_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᒸ"), bstack1lll1l_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧᒹ"), bstack1lll1l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧᒺ")],
    bstack1lll1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥᒻ"): [bstack1lll1l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᒼ"), bstack1lll1l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥᒽ")],
    bstack1lll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧᒾ"): [bstack1lll1l_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᒿ"), bstack1lll1l_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᓀ")],
    bstack1lll1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢᓁ"): [bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᓂ"), bstack1lll1l_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᓃ"), bstack1lll1l_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥᓄ")],
}
_1l111ll1l1l_opy_ = set()
class bstack1111l11l_opy_(bstack1ll11l1ll11_opy_):
    bstack1l11ll111l1_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦᓅ")
    bstack1l11l11ll11_opy_ = bstack1lll1l_opy_ (u"ࠧࡏࡎࡇࡑࠥᓆ")
    bstack1l11l11l11l_opy_ = bstack1lll1l_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧᓇ")
    bstack1l11ll11111_opy_: Callable
    bstack1l111l1ll1l_opy_: Callable
    def __init__(self, bstack1ll1111l1l1_opy_, bstack1ll11111ll1_opy_):
        super().__init__()
        self.bstack1l1l111l111_opy_ = bstack1ll11111ll1_opy_
        if os.getenv(bstack1lll1l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦᓈ"), bstack1lll1l_opy_ (u"ࠣ࠳ࠥᓉ")) != bstack1lll1l_opy_ (u"ࠤ࠴ࠦᓊ") or not self.is_enabled():
            return
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l1l1lll1_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1l1111l_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1l1lll1ll_opy_((event, state), self.bstack1l11l1ll11l_opy_)
        bstack1ll1111l1l1_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.POST), self.bstack1l11l1lll1l_opy_)
        self.bstack1l11ll11111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l111llllll_opy_(bstack1111l11l_opy_.bstack1l11l11ll11_opy_, self.bstack1l11ll11111_opy_)
        self.bstack1l111l1ll1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l111llllll_opy_(bstack1111l11l_opy_.bstack1l11l11l11l_opy_, self.bstack1l111l1ll1l_opy_)
        self.bstack1l111lll1l1_opy_ = builtins.print
        builtins.print = self.bstack1l111l11l11_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l11l111lll_opy_() or f.bstack1l11l1l11l1_opy_()) and instance:
            bstack1l111llll11_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1ll1ll1l_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1l1l11ll1_opy_ = datetime.now()
                entries = f.bstack1l11ll1l11l_opy_(instance, bstack1ll1ll1ll1l_opy_)
                if entries:
                    self.bstack1l111l1lll1_opy_(instance, entries)
                    instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥᓋ"), datetime.now() - bstack1l1l11ll1_opy_)
                    f.bstack1l11l1lll11_opy_(instance, bstack1ll1ll1ll1l_opy_)
                instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᓌ"), datetime.now() - bstack1l111llll11_opy_)
                return # bstack1l11l111ll1_opy_ not send this event with the bstack1l111l111ll_opy_ bstack1l11l11lll1_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_)
            ):
                f.bstack1lll1l11lll_opy_(instance, bstack1111l11l_opy_.bstack1l11ll111l1_opy_, True)
                return # bstack1l11l111ll1_opy_ not send this event bstack1l11ll11lll_opy_ bstack1l11ll11l11_opy_
            elif (
                f.bstack1lll111l1l1_opy_(instance, bstack1111l11l_opy_.bstack1l11ll111l1_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_)
            ):
                self.bstack1l11l1ll11l_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1l1l11ll1_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l11l111lll_opy_():
                bstack1l111lll11l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1lll1l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᓍ"), None), data.pop(bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᓎ"), {}).values()),
                    key=lambda x: x[bstack1lll1l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᓏ")],
                )
                data.update({bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᓐ"): bstack1l111lll11l_opy_})
            elif f.bstack1l11l1l11l1_opy_():
                bstack1l11l111l1l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1lll1l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᓑ"), None), data.pop(bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᓒ"), {}).values()),
                    key=lambda x: x[bstack1lll1l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᓓ")],
                )
                data.update({bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᓔ"): bstack1l11l111l1l_opy_})
            if bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_ in data:
                data.pop(bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_)
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᓕ"), datetime.now() - bstack1l1l11ll1_opy_)
            bstack1l1l11ll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11l1llll1_opy_)
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᓖ"), datetime.now() - bstack1l1l11ll1_opy_)
            if TestFramework.bstack1l1l1l1ll1l_opy_ in data:
                self.bstack1l11l11lll1_opy_(instance, bstack1ll1ll1ll1l_opy_, event_json=event_json)
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᓗ"), datetime.now() - bstack1l111llll11_opy_)
    def bstack1l1l1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
        bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack1l11l11l1_opy_.value)
        self.bstack1l1l111l111_opy_.bstack1l11l1l1l11_opy_(instance, f, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1l111l111_opy_.bstack1l11l1l111l_opy_(instance, f, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶࠣ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡠࢁࡽ࡞ࠢࡾࢁࡡࡴࡻࡾࠤᓘ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l111lll1ll_opy_ data not ready for robot-playwright at the time of bstack1l1l1l1lll1_opy_, so bstack1l111ll1ll1_opy_ will send bstack1l111lll1ll_opy_ event in bstack1l1l1l1111l_opy_ for robot-playwright
            self.bstack1l111l111l1_opy_(f, instance, req)
        bstack1l11l11ll1_opy_.end(EVENTS.bstack1l11l11l1_opy_.value, bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᓙ"), bstack1ll111111l_opy_ + bstack1lll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᓚ"), status=True, failure=None, test_name=None)
    def bstack1l1l1l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll111l1l1_opy_(instance, self.bstack1l1l111l111_opy_.bstack1l11l11l1l1_opy_, False):
            try:
                req = self.bstack1l1l111l111_opy_.bstack1l11l1l111l_opy_(instance, f, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1lll1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸࠥ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿࡛ࠦࡼࡿࡠࠤࢀࢃ࡜࡯ࡽࢀࠦᓛ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l111l111l1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11l111111_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l111l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲ࠺ࠡࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠤᓜ"))
            return
        bstack1l1l11ll1_opy_ = datetime.now()
        try:
            r = self.bstack1lll111lll1_opy_.TestSessionEvent(req)
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡨࡺࡪࡴࡴࠣᓝ"), datetime.now() - bstack1l1l11ll1_opy_)
            f.bstack1lll1l11lll_opy_(instance, self.bstack1l1l111l111_opy_.bstack1l11l11l1l1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1lll1l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᓞ") + str(r) + bstack1lll1l_opy_ (u"ࠤࠥᓟ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᓠ") + str(e) + bstack1lll1l_opy_ (u"ࠦࠧᓡ"))
            traceback.print_exc()
            raise e
    def bstack1l11l1lll1l_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        _1l11l11111l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll11l11l11_opy_.bstack1l1l11lllll_opy_(method_name):
            return
        if f.bstack1l1l1llll1l_opy_(*args) == bstack1ll11l11l11_opy_.bstack1l11l1l1lll_opy_:
            bstack1l111llll11_opy_ = datetime.now()
            screenshot = result.get(bstack1lll1l_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᓢ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡮ࡳࡡࡨࡧࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡹࡸࠢᓣ"))
                return
            bstack1l111ll1lll_opy_ = self.bstack1l11l1111ll_opy_(instance)
            if bstack1l111ll1lll_opy_:
                entry = bstack1ll11ll1l1l_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l111l1lll1_opy_(bstack1l111ll1lll_opy_, [entry])
                instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡦࡺࡨࡧࡺࡺࡥࠣᓤ"), datetime.now() - bstack1l111llll11_opy_)
            else:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠣࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡧࡶࡸࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶ࡫࡭ࡸࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡻࡦࡹࠠࡵࡣ࡮ࡩࡳࠦࡢࡺࠢࡧࡶ࡮ࡼࡥࡳ࠿ࠣࡿࢂࠨᓥ").format(instance.ref()))
        event = {}
        bstack1l111ll1lll_opy_ = self.bstack1l11l1111ll_opy_(instance)
        if bstack1l111ll1lll_opy_:
            self.bstack1l11l1l1111_opy_(event, bstack1l111ll1lll_opy_)
            if event.get(bstack1lll1l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᓦ")):
                self.bstack1l111l1lll1_opy_(bstack1l111ll1lll_opy_, event[bstack1lll1l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᓧ")])
            else:
                self.logger.debug(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡰࡴ࡭ࡳࠡࡨࡲࡶࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡨࡺࡪࡴࡴࠣᓨ"))
    @measure(event_name=EVENTS.bstack1l111l11ll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l111l1lll1_opy_(
        self,
        bstack1l111ll1lll_opy_: bstack1ll111l1l1l_opy_,
        entries: List[bstack1ll11ll1l1l_opy_],
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l1lll111_opy_)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᓩ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l111ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l11l11l1ll_opy_)
            log_entry.uuid = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1l1l1ll1l_opy_)
            log_entry.test_framework_state = bstack1l111ll1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1lll1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᓪ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1lll1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᓫ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11llll_opy_
                log_entry.file_path = entry.bstack1ll11ll_opy_
        def bstack1l11ll11ll1_opy_():
            bstack1l1l11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l111ll1lll_opy_.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᓬ"), datetime.now() - bstack1l1l11ll1_opy_)
                elif entry.kind == TestFramework.bstack1l11l1l1ll1_opy_:
                    bstack1l111ll1lll_opy_.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᓭ"), datetime.now() - bstack1l1l11ll1_opy_)
                else:
                    bstack1l111ll1lll_opy_.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡰࡴ࡭ࠢᓮ"), datetime.now() - bstack1l1l11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1lll1l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᓯ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll111111l_opy_.enqueue(bstack1l11ll11ll1_opy_)
    @measure(event_name=EVENTS.bstack1l111l1llll_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l11l11lll1_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1lll111_opy_)
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᓰ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l111ll1l_opy_)
        req.test_framework_version = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l11l11l1ll_opy_)
        req.test_framework_state = bstack1ll1ll1ll1l_opy_[0].name
        req.test_hook_state = bstack1ll1ll1ll1l_opy_[1].name
        started_at = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l111l11l1l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11l1llll1_opy_)).encode(bstack1lll1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᓱ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11ll11ll1_opy_():
            bstack1l1l11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll111lll1_opy_.TestFrameworkEvent(req)
                instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡪࡼࡥ࡯ࡶࠥᓲ"), datetime.now() - bstack1l1l11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1lll1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᓳ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll111111l_opy_.enqueue(bstack1l11ll11ll1_opy_)
    def bstack1l11l1111ll_opy_(self, instance: bstack1ll1llll11l_opy_):
        bstack1l11l1ll1ll_opy_ = TestFramework.bstack1ll1lll1l1l_opy_(instance.context)
        for t in bstack1l11l1ll1ll_opy_:
            bstack1l111lll111_opy_ = TestFramework.bstack1lll111l1l1_opy_(t, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
            if not bstack1l11ll1l1l1_opy_() and len(bstack1l111lll111_opy_) == 0:
                bstack1l111lll111_opy_ = TestFramework.bstack1lll111l1l1_opy_(t, bstack1ll11ll1lll_opy_.bstack1l11ll111ll_opy_, [])
            if any(instance is d[1] for d in bstack1l111lll111_opy_):
                return t
    def bstack1l111ll11l1_opy_(self, message):
        self.bstack1l11ll11111_opy_(message + bstack1lll1l_opy_ (u"ࠤ࡟ࡲࠧᓴ"))
    def log_error(self, message):
        self.bstack1l111l1ll1l_opy_(message + bstack1lll1l_opy_ (u"ࠥࡠࡳࠨᓵ"))
    def bstack1l111llllll_opy_(self, level, original_func):
        def bstack1l11l1l1l1l_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1lll1l_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧᓶ") in message or bstack1lll1l_opy_ (u"ࠧࡡࡓࡅࡍࡆࡐࡎࡣࠢᓷ") in message or bstack1lll1l_opy_ (u"ࠨ࡛ࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠥᓸ") in message:
                        return return_value
                    bstack1l11l1ll1ll_opy_ = TestFramework.bstack1l111ll1l11_opy_()
                    if not bstack1l11l1ll1ll_opy_:
                        return return_value
                    bstack1l111ll1lll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11l1ll1ll_opy_
                            if TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111ll1lll_opy_:
                        return return_value
                    entry = bstack1ll11ll1l1l_opy_(TestFramework.bstack1l111l1l1ll_opy_, message, level)
                    self.bstack1l111l1lll1_opy_(bstack1l111ll1lll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l11l1l1l1l_opy_
    def bstack1l111l11l11_opy_(self):
        def bstack1l11l111l11_opy_(*args, **kwargs):
            try:
                self.bstack1l111lll1l1_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1lll1l_opy_ (u"ࠧࠡࠩᓹ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1lll1l_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤᓺ") in message:
                    return
                bstack1l11l1ll1ll_opy_ = TestFramework.bstack1l111ll1l11_opy_()
                if not bstack1l11l1ll1ll_opy_:
                    return
                bstack1l111ll1lll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11l1ll1ll_opy_
                        if TestFramework.bstack1ll1l1l1l1l_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
                    ),
                    None,
                )
                if not bstack1l111ll1lll_opy_:
                    return
                entry = bstack1ll11ll1l1l_opy_(TestFramework.bstack1l111l1l1ll_opy_, message, bstack1111l11l_opy_.bstack1l11l11ll11_opy_)
                self.bstack1l111l1lll1_opy_(bstack1l111ll1lll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111lll1l1_opy_(bstack1ll1l1ll11l_opy_ (u"ࠤ࡞ࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠥࡒ࡯ࡨࠢࡦࡥࡵࡺࡵࡳࡧࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢᓻ"))
                except:
                    pass
        return bstack1l11l111l11_opy_
    def bstack1l11l1l1111_opy_(self, event: dict, instance=None) -> None:
        global _1l111ll1l1l_opy_
        levels = [bstack1lll1l_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᓼ"), bstack1lll1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᓽ")]
        bstack1l11l1ll111_opy_ = bstack1lll1l_opy_ (u"ࠧࠨᓾ")
        if instance is not None:
            try:
                bstack1l11l1ll111_opy_ = TestFramework.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
            except Exception as e:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᓿ").format(e))
        bstack1l11ll1111l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᔀ")]
                bstack1l11l1111l1_opy_ = os.path.join(bstack1l11l1lllll_opy_, (bstack1l111l1l111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11l1111l1_opy_):
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᔁ").format(bstack1l11l1111l1_opy_))
                    continue
                file_names = os.listdir(bstack1l11l1111l1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11l1111l1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l111ll1l1l_opy_:
                        self.logger.info(bstack1lll1l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᔂ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l111ll11ll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l111ll11ll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1lll1l_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᔃ"):
                                entry = bstack1ll11ll1l1l_opy_(
                                    kind=bstack1lll1l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᔄ"),
                                    message=bstack1lll1l_opy_ (u"ࠧࠨᔅ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11l11llll_opy_=file_size,
                                    bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᔆ"),
                                    bstack1ll11ll_opy_=os.path.abspath(file_path),
                                    bstack1ll11lllll_opy_=bstack1l11l1ll111_opy_
                                )
                            elif level == bstack1lll1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᔇ"):
                                entry = bstack1ll11ll1l1l_opy_(
                                    kind=bstack1lll1l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᔈ"),
                                    message=bstack1lll1l_opy_ (u"ࠤࠥᔉ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11l11llll_opy_=file_size,
                                    bstack1l111l1l11l_opy_=bstack1lll1l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᔊ"),
                                    bstack1ll11ll_opy_=os.path.abspath(file_path),
                                    bstack1l111llll1l_opy_=bstack1l11l1ll111_opy_
                                )
                            bstack1l11ll1111l_opy_.append(entry)
                            _1l111ll1l1l_opy_.add(abs_path)
                        except Exception as bstack1l11ll11l1l_opy_:
                            self.logger.error(bstack1lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᔋ").format(bstack1l11ll11l1l_opy_))
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᔌ").format(e))
        event[bstack1lll1l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᔍ")] = bstack1l11ll1111l_opy_
class bstack1l11l1llll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l11ll1l111_opy_ = set()
        kwargs[bstack1lll1l_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤᔎ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l111ll111l_opy_(obj, self.bstack1l11ll1l111_opy_)
def bstack1l111l1111l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l111ll111l_opy_(obj, bstack1l11ll1l111_opy_=None, max_depth=3):
    if bstack1l11ll1l111_opy_ is None:
        bstack1l11ll1l111_opy_ = set()
    if id(obj) in bstack1l11ll1l111_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l11ll1l111_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111l11111_opy_ = TestFramework.bstack1l11l11l111_opy_(obj)
    bstack1l111l1ll11_opy_ = next((k.lower() in bstack1l111l11111_opy_.lower() for k in bstack1l11l1ll1l1_opy_.keys()), None)
    if bstack1l111l1ll11_opy_:
        obj = TestFramework.bstack1l111l1l1l1_opy_(obj, bstack1l11l1ll1l1_opy_[bstack1l111l1ll11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1lll1l_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦᔏ")):
            keys = getattr(obj, bstack1lll1l_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᔐ"), [])
        elif hasattr(obj, bstack1lll1l_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧᔑ")):
            keys = getattr(obj, bstack1lll1l_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᔒ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1lll1l_opy_ (u"ࠧࡥࠢᔓ"))}
        if not obj and bstack1l111l11111_opy_ == bstack1lll1l_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥᔔ"):
            obj = {bstack1lll1l_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᔕ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111l1111l_opy_(key) or str(key).startswith(bstack1lll1l_opy_ (u"ࠣࡡࠥᔖ")):
            continue
        if value is not None and bstack1l111l1111l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l111ll111l_opy_(value, bstack1l11ll1l111_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l111ll111l_opy_(o, bstack1l11ll1l111_opy_, max_depth) for o in value]))
    return result or None