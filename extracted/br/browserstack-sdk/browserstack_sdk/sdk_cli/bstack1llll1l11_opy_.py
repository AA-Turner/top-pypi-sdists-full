# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1ll1l1lll1l_opy_, bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1ll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111lllll_opy_, TestHookState, bstack1l1lllllll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack111l1ll11l_opy_, bstack1l111llll1l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l1111ll111_opy_ = [bstack1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᔷ"), bstack1111l_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᔸ"), bstack1111l_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᔹ"), bstack1111l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥᔺ"), bstack1111l_opy_ (u"ࠥࡴࡦࡺࡨࠣᔻ")]
bstack1l111l1ll11_opy_ = bstack1l111llll1l_opy_()
bstack1l1111l1l1l_opy_ = bstack1111l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᔼ")
bstack1l111l111ll_opy_ = {
    bstack1111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᔽ"): bstack1l1111ll111_opy_,
    bstack1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᔾ"): bstack1l1111ll111_opy_,
    bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᔿ"): bstack1l1111ll111_opy_,
    bstack1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᕀ"): bstack1l1111ll111_opy_,
    bstack1111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᕁ"): bstack1l1111ll111_opy_
    + [
        bstack1111l_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᕂ"),
        bstack1111l_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᕃ"),
        bstack1111l_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᕄ"),
        bstack1111l_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᕅ"),
        bstack1111l_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᕆ"),
        bstack1111l_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤᕇ"),
        bstack1111l_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᕈ"),
        bstack1111l_opy_ (u"ࠥࡷࡹࡵࡰࠣᕉ"),
        bstack1111l_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨᕊ"),
        bstack1111l_opy_ (u"ࠧࡽࡨࡦࡰࠥᕋ"),
    ],
    bstack1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧᕌ"): [bstack1111l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥᕍ"), bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᕎ"), bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᕏ"), bstack1111l_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᕐ")],
    bstack1111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᕑ"): [bstack1111l_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᕒ"), bstack1111l_opy_ (u"ࠨࡡࡳࡩࡶࠦᕓ")],
    bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᕔ"): [bstack1111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᕕ"), bstack1111l_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᕖ"), bstack1111l_opy_ (u"ࠥࡪࡺࡴࡣࠣᕗ"), bstack1111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᕘ"), bstack1111l_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᕙ"), bstack1111l_opy_ (u"ࠨࡩࡥࡵࠥᕚ")],
    bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᕛ"): [bstack1111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᕜ"), bstack1111l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣᕝ"), bstack1111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᕞ")],
    bstack1111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨᕟ"): [bstack1111l_opy_ (u"ࠧࡽࡨࡦࡰࠥᕠ"), bstack1111l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨᕡ")],
    bstack1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣᕢ"): [bstack1111l_opy_ (u"ࠣࡰࡲࡨࡪࠨᕣ"), bstack1111l_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᕤ")],
    bstack1111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥᕥ"): [bstack1111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᕦ"), bstack1111l_opy_ (u"ࠧࡧࡲࡨࡵࠥᕧ"), bstack1111l_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨᕨ")],
}
_1l11111l1ll_opy_ = set()
class bstack11l1l111ll_opy_(bstack1ll1111l1ll_opy_):
    bstack1l11l11llll_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢᕩ")
    bstack1l11l111lll_opy_ = bstack1111l_opy_ (u"ࠣࡋࡑࡊࡔࠨᕪ")
    bstack1l111l1l11l_opy_ = bstack1111l_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣᕫ")
    bstack1l1111l1lll_opy_: Callable
    bstack1l111l1lll1_opy_: Callable
    def __init__(self, bstack1ll111ll111_opy_, bstack1l1lll1l11l_opy_):
        super().__init__()
        self.bstack1l1l111lll1_opy_ = bstack1l1lll1l11l_opy_
        if os.getenv(bstack1111l_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢᕬ"), bstack1111l_opy_ (u"ࠦ࠶ࠨᕭ")) != bstack1111l_opy_ (u"ࠧ࠷ࠢᕮ") or not self.is_enabled():
            return
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l1lll_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1llll_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1l11llll1_opy_((event, state), self.bstack1l11l11111l_opy_)
        bstack1ll111ll111_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.POST), self.bstack1l111ll1lll_opy_)
        self.bstack1l1111l1lll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1111lllll_opy_(bstack11l1l111ll_opy_.bstack1l11l111lll_opy_, self.bstack1l1111l1lll_opy_)
        self.bstack1l111l1lll1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1111lllll_opy_(bstack11l1l111ll_opy_.bstack1l111l1l11l_opy_, self.bstack1l111l1lll1_opy_)
        self.bstack1l11l1111l1_opy_ = builtins.print
        builtins.print = self.bstack1l111lllll1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l11111llll_opy_() or f.bstack1l1111l11l1_opy_()) and instance:
            bstack1l1111l1l11_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1l111l11_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1lll1l11l_opy_ = datetime.now()
                entries = f.bstack1l111llllll_opy_(instance, bstack1ll1l111l11_opy_)
                if entries:
                    self.bstack1l11l1l111l_opy_(instance, entries)
                    instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨᕯ"), datetime.now() - bstack1lll1l11l_opy_)
                    f.bstack1l111lll111_opy_(instance, bstack1ll1l111l11_opy_)
                instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᕰ"), datetime.now() - bstack1l1111l1l11_opy_)
                return # bstack1l111ll1ll1_opy_ not send this event with the bstack1l1111lll11_opy_ bstack1l11l11ll11_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_)
            ):
                f.bstack1ll1lllll11_opy_(instance, bstack11l1l111ll_opy_.bstack1l11l11llll_opy_, True)
                return # bstack1l111ll1ll1_opy_ not send this event bstack1l111l1111l_opy_ bstack1l1111ll1ll_opy_
            elif (
                f.bstack1ll1lll1l11_opy_(instance, bstack11l1l111ll_opy_.bstack1l11l11llll_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_)
            ):
                self.bstack1l11l11111l_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1lll1l11l_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l11111llll_opy_():
                bstack1l111ll111l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᕱ"), None), data.pop(bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᕲ"), {}).values()),
                    key=lambda x: x[bstack1111l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᕳ")],
                )
                data.update({bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᕴ"): bstack1l111ll111l_opy_})
            elif f.bstack1l1111l11l1_opy_():
                bstack1l111l11l1l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1111l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᕵ"), None), data.pop(bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᕶ"), {}).values()),
                    key=lambda x: x[bstack1111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᕷ")],
                )
                data.update({bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᕸ"): bstack1l111l11l1l_opy_})
            if bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_ in data:
                data.pop(bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_)
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᕹ"), datetime.now() - bstack1lll1l11l_opy_)
            bstack1lll1l11l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l111l1l1ll_opy_)
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᕺ"), datetime.now() - bstack1lll1l11l_opy_)
            if TestFramework.bstack1l11ll1ll1l_opy_ in data:
                self.bstack1l11l11ll11_opy_(instance, bstack1ll1l111l11_opy_, event_json=event_json)
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᕻ"), datetime.now() - bstack1l1111l1l11_opy_)
    def bstack1l1l11l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
        bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1llllll1l1_opy_.value)
        self.bstack1l1l111lll1_opy_.bstack1l111l111l1_opy_(instance, f, bstack1ll1l111l11_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1l111lll1_opy_.bstack1l11l1111ll_opy_(instance, f, bstack1ll1l111l11_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࠦࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡜ࡽࢀࡡࠥࢁࡽ࡝ࡰࡾࢁࠧᕼ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l111l11111_opy_ data not ready for robot-playwright at the time of bstack1l1l11l1lll_opy_, so bstack1l111llll11_opy_ will send bstack1l111l11111_opy_ event in bstack1l11ll1llll_opy_ for robot-playwright
            self.bstack1l111l11l11_opy_(f, instance, req)
        bstack1l11ll1l1_opy_.end(EVENTS.bstack1llllll1l1_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᕽ"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᕾ"), status=True, failure=None, test_name=None)
    def bstack1l11ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1lll1l11_opy_(instance, self.bstack1l1l111lll1_opy_.bstack1l1111lll1l_opy_, False):
            try:
                req = self.bstack1l1l111lll1_opy_.bstack1l11l1111ll_opy_(instance, f, bstack1ll1l111l11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴࠡࡩࡨࡸࡤࡩࡢࡵࡡࡨࡺࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡞ࡿࢂࡣࠠࡼࡿ࡟ࡲࢀࢃࠢᕿ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l111l11l11_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l111l1l1l1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l111l11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧᖀ"))
            return
        bstack1lll1l11l_opy_ = datetime.now()
        try:
            r = self.bstack1ll1ll1lll1_opy_.TestSessionEvent(req)
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦᖁ"), datetime.now() - bstack1lll1l11l_opy_)
            f.bstack1ll1lllll11_opy_(instance, self.bstack1l1l111lll1_opy_.bstack1l1111lll1l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᖂ") + str(r) + bstack1111l_opy_ (u"ࠧࠨᖃ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᖄ") + str(e) + bstack1111l_opy_ (u"ࠢࠣᖅ"))
            traceback.print_exc()
            raise e
    def bstack1l111ll1lll_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        _1l111ll1111_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll111ll1ll_opy_.bstack1l1l1111111_opy_(method_name):
            return
        if f.bstack1l11llll1ll_opy_(*args) == bstack1ll111ll1ll_opy_.bstack1l111l1llll_opy_:
            bstack1l1111l1l11_opy_ = datetime.now()
            screenshot = result.get(bstack1111l_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᖆ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1111l_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥᖇ"))
                return
            bstack1l111lll1ll_opy_ = self.bstack1l111lll1l1_opy_(instance)
            if bstack1l111lll1ll_opy_:
                entry = bstack1l1lllllll1_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l11l1l111l_opy_(bstack1l111lll1ll_opy_, [entry])
                instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦᖈ"), datetime.now() - bstack1l1111l1l11_opy_)
            else:
                self.logger.warning(bstack1111l_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤᖉ").format(instance.ref()))
        event = {}
        bstack1l111lll1ll_opy_ = self.bstack1l111lll1l1_opy_(instance)
        if bstack1l111lll1ll_opy_:
            self.bstack1l1111ll1l1_opy_(event, bstack1l111lll1ll_opy_)
            if event.get(bstack1111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᖊ")):
                self.bstack1l11l1l111l_opy_(bstack1l111lll1ll_opy_, event[bstack1111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᖋ")])
            else:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦᖌ"))
    @measure(event_name=EVENTS.bstack1l1111ll11l_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l11l1l111l_opy_(
        self,
        bstack1l111lll1ll_opy_: bstack1ll111lllll_opy_,
        entries: List[bstack1l1lllllll1_opy_],
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l111ll_opy_)
        req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᖍ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111lll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111lll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111lll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l1l1l1ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11l11ll1l_opy_)
            log_entry.uuid = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11ll1ll1l_opy_)
            log_entry.test_framework_state = bstack1l111lll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᖎ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᖏ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11l11l1l1_opy_
                log_entry.file_path = entry.bstack1llll1l_opy_
        def bstack1l11111lll1_opy_():
            bstack1lll1l11l_opy_ = datetime.now()
            try:
                self.bstack1ll1ll1lll1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l111lll1ll_opy_.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᖐ"), datetime.now() - bstack1lll1l11l_opy_)
                elif entry.kind == TestFramework.bstack1l1111l111l_opy_:
                    bstack1l111lll1ll_opy_.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᖑ"), datetime.now() - bstack1lll1l11l_opy_)
                else:
                    bstack1l111lll1ll_opy_.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥᖒ"), datetime.now() - bstack1lll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᖓ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1ll11lll_opy_.enqueue(bstack1l11111lll1_opy_)
    @measure(event_name=EVENTS.bstack1l1111llll1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l11l11ll11_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_)
        req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᖔ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11l11ll1l_opy_)
        req.test_framework_state = bstack1ll1l111l11_opy_[0].name
        req.test_hook_state = bstack1ll1l111l11_opy_[1].name
        started_at = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11l111l11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l111l1l1ll_opy_)).encode(bstack1111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᖕ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11111lll1_opy_():
            bstack1lll1l11l_opy_ = datetime.now()
            try:
                self.bstack1ll1ll1lll1_opy_.TestFrameworkEvent(req)
                instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡦࡸࡨࡲࡹࠨᖖ"), datetime.now() - bstack1lll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᖗ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1ll11lll_opy_.enqueue(bstack1l11111lll1_opy_)
    def bstack1l111lll1l1_opy_(self, instance: bstack1ll1l1lll1l_opy_):
        bstack1l11l111111_opy_ = TestFramework.bstack1ll1l111ll1_opy_(instance.context)
        for t in bstack1l11l111111_opy_:
            bstack1l111lll11l_opy_ = TestFramework.bstack1ll1lll1l11_opy_(t, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
            if not bstack111l1ll11l_opy_() and len(bstack1l111lll11l_opy_) == 0:
                bstack1l111lll11l_opy_ = TestFramework.bstack1ll1lll1l11_opy_(t, bstack1l1ll11l1ll_opy_.bstack1l111l11lll_opy_, [])
            if any(instance is d[1] for d in bstack1l111lll11l_opy_):
                return t
    def bstack1l11l11l11l_opy_(self, message):
        self.bstack1l1111l1lll_opy_(message + bstack1111l_opy_ (u"ࠧࡢ࡮ࠣᖘ"))
    def log_error(self, message):
        self.bstack1l111l1lll1_opy_(message + bstack1111l_opy_ (u"ࠨ࡜࡯ࠤᖙ"))
    def bstack1l1111lllll_opy_(self, level, original_func):
        def bstack1l11l11lll1_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1111l_opy_ (u"ࠢࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥࠣᖚ") in message or bstack1111l_opy_ (u"ࠣ࡝ࡖࡈࡐࡉࡌࡊ࡟ࠥᖛ") in message or bstack1111l_opy_ (u"ࠤ࡞࡛ࡪࡨࡄࡳ࡫ࡹࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠨᖜ") in message:
                        return return_value
                    bstack1l11l111111_opy_ = TestFramework.bstack1l11l111ll1_opy_()
                    if not bstack1l11l111111_opy_:
                        return return_value
                    bstack1l111lll1ll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11l111111_opy_
                            if TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111lll1ll_opy_:
                        return return_value
                    entry = bstack1l1lllllll1_opy_(TestFramework.bstack1l1111l1111_opy_, message, level)
                    self.bstack1l11l1l111l_opy_(bstack1l111lll1ll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l11l11lll1_opy_
    def bstack1l111lllll1_opy_(self):
        def bstack1l11111ll11_opy_(*args, **kwargs):
            try:
                self.bstack1l11l1111l1_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1111l_opy_ (u"ࠪࠤࠬᖝ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1111l_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧᖞ") in message:
                    return
                bstack1l11l111111_opy_ = TestFramework.bstack1l11l111ll1_opy_()
                if not bstack1l11l111111_opy_:
                    return
                bstack1l111lll1ll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11l111111_opy_
                        if TestFramework.bstack1ll1l1l11ll_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
                    ),
                    None,
                )
                if not bstack1l111lll1ll_opy_:
                    return
                entry = bstack1l1lllllll1_opy_(TestFramework.bstack1l1111l1111_opy_, message, bstack11l1l111ll_opy_.bstack1l11l111lll_opy_)
                self.bstack1l11l1l111l_opy_(bstack1l111lll1ll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l11l1111l1_opy_(bstack1ll1l11l1ll_opy_ (u"ࠧࡡࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠡࡎࡲ࡫ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥᖟ"))
                except:
                    pass
        return bstack1l11111ll11_opy_
    def bstack1l1111ll1l1_opy_(self, event: dict, instance=None) -> None:
        global _1l11111l1ll_opy_
        levels = [bstack1111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᖠ"), bstack1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᖡ")]
        bstack1l1111l1ll1_opy_ = bstack1111l_opy_ (u"ࠣࠤᖢ")
        if instance is not None:
            try:
                bstack1l1111l1ll1_opy_ = TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
            except Exception as e:
                self.logger.warning(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡹ࡮ࡪࠠࡧࡴࡲࡱࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᖣ").format(e))
        bstack1l11l111l1l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᖤ")]
                bstack1l111l1ll1l_opy_ = os.path.join(bstack1l111l1ll11_opy_, (bstack1l1111l1l1l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l111l1ll1l_opy_):
                    self.logger.debug(bstack1111l_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡯ࡱࡷࠤࡵࡸࡥࡴࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡔࡦࡵࡷࠤࡦࡴࡤࠡࡄࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᖥ").format(bstack1l111l1ll1l_opy_))
                    continue
                file_names = os.listdir(bstack1l111l1ll1l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l111l1ll1l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack1111l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᖦ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l11l11l111_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l11l11l111_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᖧ"):
                                entry = bstack1l1lllllll1_opy_(
                                    kind=bstack1111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᖨ"),
                                    message=bstack1111l_opy_ (u"ࠣࠤᖩ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11l11l1l1_opy_=file_size,
                                    bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᖪ"),
                                    bstack1llll1l_opy_=os.path.abspath(file_path),
                                    bstack111lll1111_opy_=bstack1l1111l1ll1_opy_
                                )
                            elif level == bstack1111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᖫ"):
                                entry = bstack1l1lllllll1_opy_(
                                    kind=bstack1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᖬ"),
                                    message=bstack1111l_opy_ (u"ࠧࠨᖭ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11l11l1l1_opy_=file_size,
                                    bstack1l111l11ll1_opy_=bstack1111l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᖮ"),
                                    bstack1llll1l_opy_=os.path.abspath(file_path),
                                    bstack1l111ll11ll_opy_=bstack1l1111l1ll1_opy_
                                )
                            bstack1l11l111l1l_opy_.append(entry)
                            _1l11111l1ll_opy_.add(abs_path)
                        except Exception as bstack1l11l11l1ll_opy_:
                            self.logger.error(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨᖯ").format(bstack1l11l11l1ll_opy_))
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᖰ").format(e))
        event[bstack1111l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᖱ")] = bstack1l11l111l1l_opy_
class bstack1l111l1l1ll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l11l1l11l1_opy_ = set()
        kwargs[bstack1111l_opy_ (u"ࠥࡷࡰ࡯ࡰ࡬ࡧࡼࡷࠧᖲ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l11l1l1111_opy_(obj, self.bstack1l11l1l11l1_opy_)
def bstack1l111l1l111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l11l1l1111_opy_(obj, bstack1l11l1l11l1_opy_=None, max_depth=3):
    if bstack1l11l1l11l1_opy_ is None:
        bstack1l11l1l11l1_opy_ = set()
    if id(obj) in bstack1l11l1l11l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l11l1l11l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111ll11l1_opy_ = TestFramework.bstack1l1111l11ll_opy_(obj)
    bstack1l11111ll1l_opy_ = next((k.lower() in bstack1l111ll11l1_opy_.lower() for k in bstack1l111l111ll_opy_.keys()), None)
    if bstack1l11111ll1l_opy_:
        obj = TestFramework.bstack1l11111l1l1_opy_(obj, bstack1l111l111ll_opy_[bstack1l11111ll1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1111l_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢᖳ")):
            keys = getattr(obj, bstack1111l_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣᖴ"), [])
        elif hasattr(obj, bstack1111l_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᖵ")):
            keys = getattr(obj, bstack1111l_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤᖶ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1111l_opy_ (u"ࠣࡡࠥᖷ"))}
        if not obj and bstack1l111ll11l1_opy_ == bstack1111l_opy_ (u"ࠤࡳࡥࡹ࡮࡬ࡪࡤ࠱ࡔࡴࡹࡩࡹࡒࡤࡸ࡭ࠨᖸ"):
            obj = {bstack1111l_opy_ (u"ࠥࡴࡦࡺࡨࠣᖹ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111l1l111_opy_(key) or str(key).startswith(bstack1111l_opy_ (u"ࠦࡤࠨᖺ")):
            continue
        if value is not None and bstack1l111l1l111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l11l1l1111_opy_(value, bstack1l11l1l11l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l11l1l1111_opy_(o, bstack1l11l1l11l1_opy_, max_depth) for o in value]))
    return result or None