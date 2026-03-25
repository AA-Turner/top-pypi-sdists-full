# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1l1ll111_opy_ import bstack1ll1l1111l1_opy_, bstack1l1111llll_opy_, bstack1ll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1l1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111l1l_opy_ import bstack1l1lllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l11l_opy_ import bstack1l1lll1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1llll1lll_opy_, TestHookState, bstack1l1l1l1lll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll11111l1_opy_, bstack1l111ll1111_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l1111ll111_opy_ = [bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᕨ"), bstack1l1_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᕩ"), bstack1l1_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᕪ"), bstack1l1_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥᕫ"), bstack1l1_opy_ (u"ࠥࡴࡦࡺࡨࠣᕬ")]
bstack1l11111l1l1_opy_ = bstack1l111ll1111_opy_()
bstack1l111111ll1_opy_ = bstack1l1_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᕭ")
bstack11lllll1lll_opy_ = {
    bstack1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᕮ"): bstack1l1111ll111_opy_,
    bstack1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᕯ"): bstack1l1111ll111_opy_,
    bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᕰ"): bstack1l1111ll111_opy_,
    bstack1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᕱ"): bstack1l1111ll111_opy_,
    bstack1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᕲ"): bstack1l1111ll111_opy_
    + [
        bstack1l1_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᕳ"),
        bstack1l1_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᕴ"),
        bstack1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᕵ"),
        bstack1l1_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᕶ"),
        bstack1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᕷ"),
        bstack1l1_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤᕸ"),
        bstack1l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᕹ"),
        bstack1l1_opy_ (u"ࠥࡷࡹࡵࡰࠣᕺ"),
        bstack1l1_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨᕻ"),
        bstack1l1_opy_ (u"ࠧࡽࡨࡦࡰࠥᕼ"),
    ],
    bstack1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧᕽ"): [bstack1l1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥᕾ"), bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᕿ"), bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᖀ"), bstack1l1_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᖁ")],
    bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᖂ"): [bstack1l1_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᖃ"), bstack1l1_opy_ (u"ࠨࡡࡳࡩࡶࠦᖄ")],
    bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᖅ"): [bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᖆ"), bstack1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᖇ"), bstack1l1_opy_ (u"ࠥࡪࡺࡴࡣࠣᖈ"), bstack1l1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᖉ"), bstack1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᖊ"), bstack1l1_opy_ (u"ࠨࡩࡥࡵࠥᖋ")],
    bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᖌ"): [bstack1l1_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᖍ"), bstack1l1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣᖎ"), bstack1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᖏ")],
    bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨᖐ"): [bstack1l1_opy_ (u"ࠧࡽࡨࡦࡰࠥᖑ"), bstack1l1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨᖒ")],
    bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣᖓ"): [bstack1l1_opy_ (u"ࠣࡰࡲࡨࡪࠨᖔ"), bstack1l1_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᖕ")],
    bstack1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥᖖ"): [bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᖗ"), bstack1l1_opy_ (u"ࠧࡧࡲࡨࡵࠥᖘ"), bstack1l1_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨᖙ")],
}
_1l111l11l1l_opy_ = set()
class bstack1ll11lllll_opy_(bstack1l1l1lllll1_opy_):
    bstack1l111l1lll1_opy_ = bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢᖚ")
    bstack1l1111lll1l_opy_ = bstack1l1_opy_ (u"ࠣࡋࡑࡊࡔࠨᖛ")
    bstack11llllll111_opy_ = bstack1l1_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣᖜ")
    bstack11llllll1ll_opy_: Callable
    bstack1l111lll1l1_opy_: Callable
    def __init__(self, bstack1l1lll1l11l_opy_, bstack1l1ll11ll1l_opy_):
        super().__init__()
        self.bstack1l11llll1l1_opy_ = bstack1l1ll11ll1l_opy_
        if os.getenv(bstack1l1_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢᖝ"), bstack1l1_opy_ (u"ࠦ࠶ࠨᖞ")) != bstack1l1_opy_ (u"ࠧ࠷ࠢᖟ") or not self.is_enabled():
            return
        TestFramework.bstack1l1l11ll111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11ll1ll11_opy_)
        TestFramework.bstack1l1l11ll111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11llll1ll_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1l11ll111_opy_((event, state), self.bstack1l1111l11ll_opy_)
        bstack1l1lll1l11l_opy_.bstack1l1l11ll111_opy_((bstack1l1111llll_opy_.bstack1ll1ll1lll1_opy_, bstack1ll1l11l1_opy_.POST), self.bstack11llllllll1_opy_)
        self.bstack11llllll1ll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1111l1ll1_opy_(bstack1ll11lllll_opy_.bstack1l1111lll1l_opy_, self.bstack11llllll1ll_opy_)
        self.bstack1l111lll1l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1111l1ll1_opy_(bstack1ll11lllll_opy_.bstack11llllll111_opy_, self.bstack1l111lll1l1_opy_)
        self.bstack1l1111l1l11_opy_ = builtins.print
        builtins.print = self.bstack1l111ll11ll_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll1lll_opy_,
        bstack1ll11ll1lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l1111ll11l_opy_() or f.bstack1l1111l1l1l_opy_()) and instance:
            bstack11lllll1ll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll11ll1lll_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1l1lll11l1_opy_ = datetime.now()
                entries = f.bstack1l1111l1111_opy_(instance, bstack1ll11ll1lll_opy_)
                if entries:
                    self.bstack11lllllll11_opy_(instance, entries)
                    instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨᖠ"), datetime.now() - bstack1l1lll11l1_opy_)
                    f.bstack1l111ll1l11_opy_(instance, bstack1ll11ll1lll_opy_)
                instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᖡ"), datetime.now() - bstack11lllll1ll1_opy_)
                return # bstack1l111lll11l_opy_ not send this event with the bstack1l111l1llll_opy_ bstack11lllllll1l_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_)
            ):
                f.bstack1ll1l11lll_opy_(instance, bstack1ll11lllll_opy_.bstack1l111l1lll1_opy_, True)
                return # bstack1l111lll11l_opy_ not send this event bstack1l111l11ll1_opy_ bstack1l1111111l1_opy_
            elif (
                f.bstack1ll1ll11l1l_opy_(instance, bstack1ll11lllll_opy_.bstack1l111l1lll1_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_)
            ):
                self.bstack1l1111l11ll_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1l1lll11l1_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l1111ll11l_opy_():
                bstack1l1111lllll_opy_ = sorted(
                    filter(lambda x: x.get(bstack1l1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᖢ"), None), data.pop(bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᖣ"), {}).values()),
                    key=lambda x: x[bstack1l1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᖤ")],
                )
                data.update({bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᖥ"): bstack1l1111lllll_opy_})
            elif f.bstack1l1111l1l1l_opy_():
                bstack1l11111l11l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1l1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᖦ"), None), data.pop(bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᖧ"), {}).values()),
                    key=lambda x: x[bstack1l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᖨ")],
                )
                data.update({bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᖩ"): bstack1l11111l11l_opy_})
            if bstack1l1lllll11l_opy_.bstack1l1111ll1ll_opy_ in data:
                data.pop(bstack1l1lllll11l_opy_.bstack1l1111ll1ll_opy_)
            instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᖪ"), datetime.now() - bstack1l1lll11l1_opy_)
            bstack1l1lll11l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11111ll11_opy_)
            instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᖫ"), datetime.now() - bstack1l1lll11l1_opy_)
            if TestFramework.bstack1l11l1lll1l_opy_ in data:
                self.bstack11lllllll1l_opy_(instance, bstack1ll11ll1lll_opy_, event_json=event_json)
            instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᖬ"), datetime.now() - bstack11lllll1ll1_opy_)
    def bstack1l11ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll1lll_opy_,
        bstack1ll11ll1lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l1l1ll_opy_ import bstack111l1111l_opy_
        bstack111l1l111_opy_ = bstack111l1111l_opy_.bstack1ll1l1l1l_opy_(EVENTS.bstack1l1111ll1_opy_.value)
        self.bstack1l11llll1l1_opy_.bstack1l111111l11_opy_(instance, f, bstack1ll11ll1lll_opy_, *args, **kwargs)
        try:
            req = self.bstack1l11llll1l1_opy_.bstack1l111l11lll_opy_(instance, f, bstack1ll11ll1lll_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࠦࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡜ࡽࢀࡡࠥࢁࡽ࡝ࡰࡾࢁࠧᖭ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l11111llll_opy_ data not ready for robot-playwright at the time of bstack1l11ll1ll11_opy_, so bstack1l111lll111_opy_ will send bstack1l11111llll_opy_ event in bstack1l11llll1ll_opy_ for robot-playwright
            self.bstack1l111ll11l1_opy_(f, instance, req)
        bstack111l1111l_opy_.end(EVENTS.bstack1l1111ll1_opy_.value, bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᖮ"), bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᖯ"), status=True, failure=None, test_name=None)
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll1lll_opy_,
        bstack1ll11ll1lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1ll11l1l_opy_(instance, self.bstack1l11llll1l1_opy_.bstack1l1111111ll_opy_, False):
            try:
                req = self.bstack1l11llll1l1_opy_.bstack1l111l11lll_opy_(instance, f, bstack1ll11ll1lll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴࠡࡩࡨࡸࡤࡩࡢࡵࡡࡨࡺࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡞ࡿࢂࡣࠠࡼࡿ࡟ࡲࢀࢃࠢᖰ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l111ll11l1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l111l111ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l111ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll1lll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧᖱ"))
            return
        bstack1l1lll11l1_opy_ = datetime.now()
        try:
            r = self.bstack1l1ll11l111_opy_.TestSessionEvent(req)
            instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦᖲ"), datetime.now() - bstack1l1lll11l1_opy_)
            f.bstack1ll1l11lll_opy_(instance, self.bstack1l11llll1l1_opy_.bstack1l1111111ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᖳ") + str(r) + bstack1l1_opy_ (u"ࠧࠨᖴ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᖵ") + str(e) + bstack1l1_opy_ (u"ࠢࠣᖶ"))
            traceback.print_exc()
            raise e
    def bstack11llllllll1_opy_(
        self,
        f: bstack1l1lll1l1ll_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1l1111l1_opy_, str],
        _1l11111111l_opy_: Tuple[bstack1l1111llll_opy_, bstack1ll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l1lll1l1ll_opy_.bstack1l11lllllll_opy_(method_name):
            return
        if f.bstack1l1l11l1lll_opy_(*args) == bstack1l1lll1l1ll_opy_.bstack1l111l1l1l1_opy_:
            bstack11lllll1ll1_opy_ = datetime.now()
            screenshot = result.get(bstack1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᖷ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥᖸ"))
                return
            bstack1l11111l1ll_opy_ = self.bstack1l111l1l11l_opy_(instance)
            if bstack1l11111l1ll_opy_:
                entry = bstack1l1l1l1lll1_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack11lllllll11_opy_(bstack1l11111l1ll_opy_, [entry])
                instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦᖹ"), datetime.now() - bstack11lllll1ll1_opy_)
            else:
                self.logger.warning(bstack1l1_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤᖺ").format(instance.ref()))
        event = {}
        bstack1l11111l1ll_opy_ = self.bstack1l111l1l11l_opy_(instance)
        if bstack1l11111l1ll_opy_:
            self.bstack1l111lll1ll_opy_(event, bstack1l11111l1ll_opy_)
            if event.get(bstack1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᖻ")):
                self.bstack11lllllll11_opy_(bstack1l11111l1ll_opy_, event[bstack1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᖼ")])
            else:
                self.logger.debug(bstack1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦᖽ"))
    @measure(event_name=EVENTS.bstack1l1111l111l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11lllllll11_opy_(
        self,
        bstack1l11111l1ll_opy_: bstack1l1llll1lll_opy_,
        entries: List[bstack1l1l1l1lll1_opy_],
    ):
        self.bstack1l11lll111l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l1l1111l1l_opy_)
        req.client_worker_id = bstack1l1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᖾ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11111l1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11111l1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11111l1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l11lll1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l111l111l1_opy_)
            log_entry.uuid = TestFramework.bstack1ll1ll11l1l_opy_(bstack1l11111l1ll_opy_, TestFramework.bstack1l11l1lll1l_opy_)
            log_entry.test_framework_state = bstack1l11111l1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᖿ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᗀ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lllllllll_opy_
                log_entry.file_path = entry.bstack1llllll1_opy_
        def bstack1l1111llll1_opy_():
            bstack1l1lll11l1_opy_ = datetime.now()
            try:
                self.bstack1l1ll11l111_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l11111l1ll_opy_.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣᗁ"), datetime.now() - bstack1l1lll11l1_opy_)
                elif entry.kind == TestFramework.bstack1l111l1111l_opy_:
                    bstack1l11111l1ll_opy_.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᗂ"), datetime.now() - bstack1l1lll11l1_opy_)
                else:
                    bstack1l11111l1ll_opy_.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥᗃ"), datetime.now() - bstack1l1lll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᗄ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l1111llll1_opy_)
    @measure(event_name=EVENTS.bstack1l111l1l111_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11lllllll1l_opy_(
        self,
        instance: bstack1l1llll1lll_opy_,
        bstack1ll11ll1lll_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l11lll111l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_)
        req.client_worker_id = bstack1l1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᗅ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack1l11lll1l11_opy_)
        req.test_framework_version = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack1l111l111l1_opy_)
        req.test_framework_state = bstack1ll11ll1lll_opy_[0].name
        req.test_hook_state = bstack1ll11ll1lll_opy_[1].name
        started_at = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack1l1111l1lll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack11llllll11l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11111ll11_opy_)).encode(bstack1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᗆ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1111llll1_opy_():
            bstack1l1lll11l1_opy_ = datetime.now()
            try:
                self.bstack1l1ll11l111_opy_.TestFrameworkEvent(req)
                instance.bstack11l11ll11l_opy_(bstack1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡦࡸࡨࡲࡹࠨᗇ"), datetime.now() - bstack1l1lll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᗈ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l1111llll1_opy_)
    def bstack1l111l1l11l_opy_(self, instance: bstack1ll1l1111l1_opy_):
        bstack1l111111lll_opy_ = TestFramework.bstack1ll11l11111_opy_(instance.context)
        for t in bstack1l111111lll_opy_:
            bstack1l111111111_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(t, bstack1l1lllll11l_opy_.bstack1l1111ll1ll_opy_, [])
            if not bstack1ll11111l1_opy_() and len(bstack1l111111111_opy_) == 0:
                bstack1l111111111_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(t, bstack1l1lllll11l_opy_.bstack1l111ll1lll_opy_, [])
            if any(instance is d[1] for d in bstack1l111111111_opy_):
                return t
    def bstack1l111l11111_opy_(self, message):
        self.bstack11llllll1ll_opy_(message + bstack1l1_opy_ (u"ࠧࡢ࡮ࠣᗉ"))
    def log_error(self, message):
        self.bstack1l111lll1l1_opy_(message + bstack1l1_opy_ (u"ࠨ࡜࡯ࠤᗊ"))
    def bstack1l1111l1ll1_opy_(self, level, original_func):
        def bstack1l111l11l11_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1l1_opy_ (u"ࠢࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥࠣᗋ") in message or bstack1l1_opy_ (u"ࠣ࡝ࡖࡈࡐࡉࡌࡊ࡟ࠥᗌ") in message or bstack1l1_opy_ (u"ࠤ࡞࡛ࡪࡨࡄࡳ࡫ࡹࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠨᗍ") in message:
                        return return_value
                    bstack1l111111lll_opy_ = TestFramework.bstack1l111l1ll1l_opy_()
                    if not bstack1l111111lll_opy_:
                        return return_value
                    bstack1l11111l1ll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l111111lll_opy_
                            if TestFramework.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_)
                        ),
                        None,
                    )
                    if not bstack1l11111l1ll_opy_:
                        return return_value
                    entry = bstack1l1l1l1lll1_opy_(TestFramework.bstack11lllll1l1l_opy_, message, level)
                    self.bstack11lllllll11_opy_(bstack1l11111l1ll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l111l11l11_opy_
    def bstack1l111ll11ll_opy_(self):
        def bstack1l111l1l1ll_opy_(*args, **kwargs):
            try:
                self.bstack1l1111l1l11_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l1_opy_ (u"ࠪࠤࠬᗎ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l1_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧᗏ") in message:
                    return
                bstack1l111111lll_opy_ = TestFramework.bstack1l111l1ll1l_opy_()
                if not bstack1l111111lll_opy_:
                    return
                bstack1l11111l1ll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l111111lll_opy_
                        if TestFramework.bstack1ll1l1l1l11_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_)
                    ),
                    None,
                )
                if not bstack1l11111l1ll_opy_:
                    return
                entry = bstack1l1l1l1lll1_opy_(TestFramework.bstack11lllll1l1l_opy_, message, bstack1ll11lllll_opy_.bstack1l1111lll1l_opy_)
                self.bstack11lllllll11_opy_(bstack1l11111l1ll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1111l1l11_opy_(bstack1ll11l111l1_opy_ (u"ࠧࡡࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠡࡎࡲ࡫ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥᗐ"))
                except:
                    pass
        return bstack1l111l1l1ll_opy_
    def bstack1l111lll1ll_opy_(self, event: dict, instance=None) -> None:
        global _1l111l11l1l_opy_
        levels = [bstack1l1_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᗑ"), bstack1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᗒ")]
        bstack1l111llll1l_opy_ = bstack1l1_opy_ (u"ࠣࠤᗓ")
        if instance is not None:
            try:
                bstack1l111llll1l_opy_ = TestFramework.bstack1ll1ll11l1l_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡹ࡮ࡪࠠࡧࡴࡲࡱࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᗔ").format(e))
        bstack1l11111lll1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᗕ")]
                bstack1l111ll1ll1_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack1l111111ll1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l111ll1ll1_opy_):
                    self.logger.debug(bstack1l1_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡯ࡱࡷࠤࡵࡸࡥࡴࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡔࡦࡵࡷࠤࡦࡴࡤࠡࡄࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᗖ").format(bstack1l111ll1ll1_opy_))
                    continue
                file_names = os.listdir(bstack1l111ll1ll1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l111ll1ll1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l111l11l1l_opy_:
                        self.logger.info(bstack1l1_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᗗ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack11lllll1l11_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack11lllll1l11_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᗘ"):
                                entry = bstack1l1l1l1lll1_opy_(
                                    kind=bstack1l1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᗙ"),
                                    message=bstack1l1_opy_ (u"ࠣࠤᗚ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11lllllllll_opy_=file_size,
                                    bstack1l111l1ll11_opy_=bstack1l1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᗛ"),
                                    bstack1llllll1_opy_=os.path.abspath(file_path),
                                    bstack1l11lllll1_opy_=bstack1l111llll1l_opy_
                                )
                            elif level == bstack1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᗜ"):
                                entry = bstack1l1l1l1lll1_opy_(
                                    kind=bstack1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᗝ"),
                                    message=bstack1l1_opy_ (u"ࠧࠨᗞ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11lllllllll_opy_=file_size,
                                    bstack1l111l1ll11_opy_=bstack1l1_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᗟ"),
                                    bstack1llllll1_opy_=os.path.abspath(file_path),
                                    bstack1l11111ll1l_opy_=bstack1l111llll1l_opy_
                                )
                            bstack1l11111lll1_opy_.append(entry)
                            _1l111l11l1l_opy_.add(abs_path)
                        except Exception as bstack1l111llll11_opy_:
                            self.logger.error(bstack1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨᗠ").format(bstack1l111llll11_opy_))
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᗡ").format(e))
        event[bstack1l1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᗢ")] = bstack1l11111lll1_opy_
class bstack1l11111ll11_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1111l11l1_opy_ = set()
        kwargs[bstack1l1_opy_ (u"ࠥࡷࡰ࡯ࡰ࡬ࡧࡼࡷࠧᗣ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l111ll1l1l_opy_(obj, self.bstack1l1111l11l1_opy_)
def bstack1l111111l1l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l111ll1l1l_opy_(obj, bstack1l1111l11l1_opy_=None, max_depth=3):
    if bstack1l1111l11l1_opy_ is None:
        bstack1l1111l11l1_opy_ = set()
    if id(obj) in bstack1l1111l11l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1111l11l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111ll111l_opy_ = TestFramework.bstack1l11111l111_opy_(obj)
    bstack11llllll1l1_opy_ = next((k.lower() in bstack1l111ll111l_opy_.lower() for k in bstack11lllll1lll_opy_.keys()), None)
    if bstack11llllll1l1_opy_:
        obj = TestFramework.bstack1l1111lll11_opy_(obj, bstack11lllll1lll_opy_[bstack11llllll1l1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢᗤ")):
            keys = getattr(obj, bstack1l1_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣᗥ"), [])
        elif hasattr(obj, bstack1l1_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᗦ")):
            keys = getattr(obj, bstack1l1_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤᗧ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1_opy_ (u"ࠣࡡࠥᗨ"))}
        if not obj and bstack1l111ll111l_opy_ == bstack1l1_opy_ (u"ࠤࡳࡥࡹ࡮࡬ࡪࡤ࠱ࡔࡴࡹࡩࡹࡒࡤࡸ࡭ࠨᗩ"):
            obj = {bstack1l1_opy_ (u"ࠥࡴࡦࡺࡨࠣᗪ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111111l1l_opy_(key) or str(key).startswith(bstack1l1_opy_ (u"ࠦࡤࠨᗫ")):
            continue
        if value is not None and bstack1l111111l1l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l111ll1l1l_opy_(value, bstack1l1111l11l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l111ll1l1l_opy_(o, bstack1l1111l11l1_opy_, max_depth) for o in value]))
    return result or None