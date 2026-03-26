# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack1ll11ll1l11_opy_, bstack11lll111_opy_, bstack1l11l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1111_opy_ import bstack1l1llll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1lllll1_opy_, TestHookState, bstack1l1l11lll1l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack11lll11l1_opy_, bstack1l1111l1lll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11llll1llll_opy_ = [bstack1ll1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᖀ"), bstack1ll1lll_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᖁ"), bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦᖂ"), bstack1ll1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࠨᖃ"), bstack1ll1lll_opy_ (u"ࠨࡰࡢࡶ࡫ࠦᖄ")]
bstack1l11111l1l1_opy_ = bstack1l1111l1lll_opy_()
bstack11lllll111l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᖅ")
bstack1l111ll11l1_opy_ = {
    bstack1ll1lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡋࡷࡩࡲࠨᖆ"): bstack11llll1llll_opy_,
    bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡓࡥࡨࡱࡡࡨࡧࠥᖇ"): bstack11llll1llll_opy_,
    bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡑࡴࡪࡵ࡭ࡧࠥᖈ"): bstack11llll1llll_opy_,
    bstack1ll1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡈࡲࡡࡴࡵࠥᖉ"): bstack11llll1llll_opy_,
    bstack1ll1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠢᖊ"): bstack11llll1llll_opy_
    + [
        bstack1ll1lll_opy_ (u"ࠨ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬࡯ࡣࡰࡩࠧᖋ"),
        bstack1ll1lll_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᖌ"),
        bstack1ll1lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦ࡫ࡱࡪࡴࠨᖍ"),
        bstack1ll1lll_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᖎ"),
        bstack1ll1lll_opy_ (u"ࠥࡧࡦࡲ࡬ࡴࡲࡨࡧࠧᖏ"),
        bstack1ll1lll_opy_ (u"ࠦࡨࡧ࡬࡭ࡱࡥ࡮ࠧᖐ"),
        bstack1ll1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦᖑ"),
        bstack1ll1lll_opy_ (u"ࠨࡳࡵࡱࡳࠦᖒ"),
        bstack1ll1lll_opy_ (u"ࠢࡥࡷࡵࡥࡹ࡯࡯࡯ࠤᖓ"),
        bstack1ll1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᖔ"),
    ],
    bstack1ll1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥ࡮ࡴ࠮ࡔࡧࡶࡷ࡮ࡵ࡮ࠣᖕ"): [bstack1ll1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡲࡤࡸ࡭ࠨᖖ"), bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡩࡥ࡮ࡲࡥࡥࠤᖗ"), bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡶࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨᖘ"), bstack1ll1lll_opy_ (u"ࠨࡩࡵࡧࡰࡷࠧᖙ")],
    bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡤࡱࡱࡪ࡮࡭࠮ࡄࡱࡱࡪ࡮࡭ࠢᖚ"): [bstack1ll1lll_opy_ (u"ࠣ࡫ࡱࡺࡴࡩࡡࡵ࡫ࡲࡲࡤࡶࡡࡳࡣࡰࡷࠧᖛ"), bstack1ll1lll_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᖜ")],
    bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳ࡌࡩࡹࡶࡸࡶࡪࡊࡥࡧࠤᖝ"): [bstack1ll1lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᖞ"), bstack1ll1lll_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᖟ"), bstack1ll1lll_opy_ (u"ࠨࡦࡶࡰࡦࠦᖠ"), bstack1ll1lll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᖡ"), bstack1ll1lll_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᖢ"), bstack1ll1lll_opy_ (u"ࠤ࡬ࡨࡸࠨᖣ")],
    bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳࡙ࡵࡣࡔࡨࡵࡺ࡫ࡳࡵࠤᖤ"): [bstack1ll1lll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᖥ"), bstack1ll1lll_opy_ (u"ࠧࡶࡡࡳࡣࡰࠦᖦ"), bstack1ll1lll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡤ࡯࡮ࡥࡧࡻࠦᖧ")],
    bstack1ll1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡳࡷࡱࡲࡪࡸ࠮ࡄࡣ࡯ࡰࡎࡴࡦࡰࠤᖨ"): [bstack1ll1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᖩ"), bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࠤᖪ")],
    bstack1ll1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡔ࡯ࡥࡧࡎࡩࡾࡽ࡯ࡳࡦࡶࠦᖫ"): [bstack1ll1lll_opy_ (u"ࠦࡳࡵࡤࡦࠤᖬ"), bstack1ll1lll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᖭ")],
    bstack1ll1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡏࡤࡶࡰࠨᖮ"): [bstack1ll1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᖯ"), bstack1ll1lll_opy_ (u"ࠣࡣࡵ࡫ࡸࠨᖰ"), bstack1ll1lll_opy_ (u"ࠤ࡮ࡻࡦࡸࡧࡴࠤᖱ")],
}
_1l11111llll_opy_ = set()
class bstack1lll11ll1_opy_(bstack1ll111l11ll_opy_):
    bstack1l11111l111_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡨࡪࡪࡸࡲࡦࡦࠥᖲ")
    bstack11llllll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠦࡎࡔࡆࡐࠤᖳ")
    bstack1l111l1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡋࡒࡓࡑࡕࠦᖴ")
    bstack1l111l11l1l_opy_: Callable
    bstack11lllllllll_opy_: Callable
    def __init__(self, bstack1l1ll1ll1ll_opy_, bstack1l1lll111ll_opy_):
        super().__init__()
        self.bstack1l11lllll1l_opy_ = bstack1l1lll111ll_opy_
        if os.getenv(bstack1ll1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡕ࠱࠲࡛ࠥᖵ"), bstack1ll1lll_opy_ (u"ࠢ࠲ࠤᖶ")) != bstack1ll1lll_opy_ (u"ࠣ࠳ࠥᖷ") or not self.is_enabled():
            return
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11lllll11_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1111lll_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l11ll11111_opy_((event, state), self.bstack1l111l1ll1l_opy_)
        bstack1l1ll1ll1ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.POST), self.bstack1l111ll1l1l_opy_)
        self.bstack1l111l11l1l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l111ll1111_opy_(bstack1lll11ll1_opy_.bstack11llllll1ll_opy_, self.bstack1l111l11l1l_opy_)
        self.bstack11lllllllll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l111ll1111_opy_(bstack1lll11ll1_opy_.bstack1l111l1l11l_opy_, self.bstack11lllllllll_opy_)
        self.bstack1l111111111_opy_ = builtins.print
        builtins.print = self.bstack11llll1ll11_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l111l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l111l1l1ll_opy_() or f.bstack1l1111111ll_opy_()) and instance:
            bstack1l1111l111l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll11l1l111_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack11lllll111_opy_ = datetime.now()
                entries = f.bstack1l1111ll1ll_opy_(instance, bstack1ll11l1l111_opy_)
                if entries:
                    self.bstack1l111ll11ll_opy_(instance, entries)
                    instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤᖸ"), datetime.now() - bstack11lllll111_opy_)
                    f.bstack1l111l1ll11_opy_(instance, bstack1ll11l1l111_opy_)
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᖹ"), datetime.now() - bstack1l1111l111l_opy_)
                return # bstack1l111111ll1_opy_ not send this event with the bstack11lllll1l1l_opy_ bstack11llllllll1_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l1111ll11l_opy_)
            ):
                f.bstack1lll1111ll_opy_(instance, bstack1lll11ll1_opy_.bstack1l11111l111_opy_, True)
                return # bstack1l111111ll1_opy_ not send this event bstack1l111l111l1_opy_ bstack11llll1lll1_opy_
            elif (
                f.bstack1ll1l11llll_opy_(instance, bstack1lll11ll1_opy_.bstack1l11111l111_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l1111ll11l_opy_)
            ):
                self.bstack1l111l1ll1l_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack11lllll111_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l111l1l1ll_opy_():
                bstack11llllll11l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll1lll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᖺ"), None), data.pop(bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᖻ"), {}).values()),
                    key=lambda x: x[bstack1ll1lll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᖼ")],
                )
                data.update({bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᖽ"): bstack11llllll11l_opy_})
            elif f.bstack1l1111111ll_opy_():
                bstack1l111l1l1l1_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll1lll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᖾ"), None), data.pop(bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡬ࡧࡼࡻࡴࡸࡤࡴࠤᖿ"), {}).values()),
                    key=lambda x: x[bstack1ll1lll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᗀ")],
                )
                data.update({bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᗁ"): bstack1l111l1l1l1_opy_})
            if bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_ in data:
                data.pop(bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_)
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᗂ"), datetime.now() - bstack11lllll111_opy_)
            bstack11lllll111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack11lllll11ll_opy_)
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᗃ"), datetime.now() - bstack11lllll111_opy_)
            if TestFramework.bstack1l11ll11l1l_opy_ in data:
                self.bstack11llllllll1_opy_(instance, bstack1ll11l1l111_opy_, event_json=event_json)
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᗄ"), datetime.now() - bstack1l1111l111l_opy_)
    def bstack1l11lllll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
        bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack111111ll11_opy_.value)
        self.bstack1l11lllll1l_opy_.bstack1l1111l11ll_opy_(instance, f, bstack1ll11l1l111_opy_, *args, **kwargs)
        try:
            req = self.bstack1l11lllll1l_opy_.bstack1l1111l1l11_opy_(instance, f, bstack1ll11l1l111_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵࠢࡪࡩࡹࡥࡣࡣࡶࡢࡩࡻ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣ࡟ࢀࢃ࡝ࠡࡽࢀࡠࡳࢁࡽࠣᗅ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l11111ll11_opy_ data not ready for robot-playwright at the time of bstack1l11lllll11_opy_, so bstack11lllll11l1_opy_ will send bstack1l11111ll11_opy_ event in bstack1l1l1111lll_opy_ for robot-playwright
            self.bstack1l111111l11_opy_(f, instance, req)
        bstack1l1l11ll1_opy_.end(EVENTS.bstack111111ll11_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᗆ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᗇ"), status=True, failure=None, test_name=None)
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1l11llll_opy_(instance, self.bstack1l11lllll1l_opy_.bstack11lllll1ll1_opy_, False):
            try:
                req = self.bstack1l11lllll1l_opy_.bstack1l1111l1l11_opy_(instance, f, bstack1ll11l1l111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷࠤ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡡࡻࡾ࡟ࠣࡿࢂࡢ࡮ࡼࡿࠥᗈ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l111111l11_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11111l11l_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1l111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll1lll_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠣ࡫ࡗࡖࡃࠡࡥࡤࡰࡱࡀࠠࡏࡱࠣࡺࡦࡲࡩࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠣᗉ"))
            return
        bstack11lllll111_opy_ = datetime.now()
        try:
            r = self.bstack1l1llll1lll_opy_.TestSessionEvent(req)
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡧࡹࡩࡳࡺࠢᗊ"), datetime.now() - bstack11lllll111_opy_)
            f.bstack1lll1111ll_opy_(instance, self.bstack1l11lllll1l_opy_.bstack11lllll1ll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll1lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᗋ") + str(r) + bstack1ll1lll_opy_ (u"ࠣࠤᗌ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᗍ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᗎ"))
            traceback.print_exc()
            raise e
    def bstack1l111ll1l1l_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        _driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        _1l111l1lll1_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll111l1111_opy_.bstack1l1l11111ll_opy_(method_name):
            return
        if f.bstack1l11llll11l_opy_(*args) == bstack1ll111l1111_opy_.bstack1l1111l1111_opy_:
            bstack1l1111l111l_opy_ = datetime.now()
            screenshot = result.get(bstack1ll1lll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᗏ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣ࡭ࡲࡧࡧࡦࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡸࡷࠨᗐ"))
                return
            bstack11llllll1l1_opy_ = self.bstack1l111l11l11_opy_(instance)
            if bstack11llllll1l1_opy_:
                entry = bstack1l1l11lll1l_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l111ll11ll_opy_(bstack11llllll1l1_opy_, [entry])
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡥࡹࡧࡦࡹࡹ࡫ࠢᗑ"), datetime.now() - bstack1l1111l111l_opy_)
            else:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡦࡵࡷࠤ࡫ࡵࡲࠡࡹ࡫࡭ࡨ࡮ࠠࡵࡪ࡬ࡷࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡺࡥࡸࠦࡴࡢ࡭ࡨࡲࠥࡨࡹࠡࡦࡵ࡭ࡻ࡫ࡲ࠾ࠢࡾࢁࠧᗒ").format(instance.ref()))
        event = {}
        bstack11llllll1l1_opy_ = self.bstack1l111l11l11_opy_(instance)
        if bstack11llllll1l1_opy_:
            self.bstack1l11111lll1_opy_(event, bstack11llllll1l1_opy_)
            if event.get(bstack1ll1lll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᗓ")):
                self.bstack1l111ll11ll_opy_(bstack11llllll1l1_opy_, event[bstack1ll1lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᗔ")])
            else:
                self.logger.debug(bstack1ll1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡯ࡳ࡬ࡹࠠࡧࡱࡵࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡧࡹࡩࡳࡺࠢᗕ"))
    @measure(event_name=EVENTS.bstack1l1111l11l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1l111ll11ll_opy_(
        self,
        bstack11llllll1l1_opy_: bstack1l1l1lllll1_opy_,
        entries: List[bstack1l1l11lll1l_opy_],
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11l1ll11l_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᗖ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack11llllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack11llllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack11llllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11ll1l111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.uuid = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack1l11ll11l1l_opy_)
            log_entry.test_framework_state = bstack11llllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᗗ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll1lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᗘ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1111llll1_opy_
                log_entry.file_path = entry.bstack111lll_opy_
        def bstack1l11111l1ll_opy_():
            bstack11lllll111_opy_ = datetime.now()
            try:
                self.bstack1l1llll1lll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack11llllll1l1_opy_.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᗙ"), datetime.now() - bstack11lllll111_opy_)
                elif entry.kind == TestFramework.bstack11lllll1l11_opy_:
                    bstack11llllll1l1_opy_.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᗚ"), datetime.now() - bstack11lllll111_opy_)
                else:
                    bstack11llllll1l1_opy_.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨᗛ"), datetime.now() - bstack11lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᗜ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1l1111ll_opy_.enqueue(bstack1l11111l1ll_opy_)
    @measure(event_name=EVENTS.bstack11lllllll11_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack11llllllll1_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_)
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᗝ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll1l111_opy_)
        req.test_framework_version = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11111111l_opy_)
        req.test_framework_state = bstack1ll11l1l111_opy_[0].name
        req.test_hook_state = bstack1ll11l1l111_opy_[1].name
        started_at = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l111l1l111_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l111ll1l11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack11lllll11ll_opy_)).encode(bstack1ll1lll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᗞ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11111l1ll_opy_():
            bstack11lllll111_opy_ = datetime.now()
            try:
                self.bstack1l1llll1lll_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡩࡻ࡫࡮ࡵࠤᗟ"), datetime.now() - bstack11lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1lll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᗠ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1l1111ll_opy_.enqueue(bstack1l11111l1ll_opy_)
    def bstack1l111l11l11_opy_(self, instance: bstack1ll11ll1l11_opy_):
        bstack1l1111ll111_opy_ = TestFramework.bstack1ll111ll1ll_opy_(instance.context)
        for t in bstack1l1111ll111_opy_:
            bstack11lllll1lll_opy_ = TestFramework.bstack1ll1l11llll_opy_(t, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
            if not bstack11lll11l1_opy_() and len(bstack11lllll1lll_opy_) == 0:
                bstack11lllll1lll_opy_ = TestFramework.bstack1ll1l11llll_opy_(t, bstack1l1llll11ll_opy_.bstack11lllllll1l_opy_, [])
            if any(instance is d[1] for d in bstack11lllll1lll_opy_):
                return t
    def bstack1l111111l1l_opy_(self, message):
        self.bstack1l111l11l1l_opy_(message + bstack1ll1lll_opy_ (u"ࠣ࡞ࡱࠦᗡ"))
    def log_error(self, message):
        self.bstack11lllllllll_opy_(message + bstack1ll1lll_opy_ (u"ࠤ࡟ࡲࠧᗢ"))
    def bstack1l111ll1111_opy_(self, level, original_func):
        def bstack11lllll1111_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1ll1lll_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦᗣ") in message or bstack1ll1lll_opy_ (u"ࠦࡠ࡙ࡄࡌࡅࡏࡍࡢࠨᗤ") in message or bstack1ll1lll_opy_ (u"ࠧࡡࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠤᗥ") in message:
                        return return_value
                    bstack1l1111ll111_opy_ = TestFramework.bstack1l11111ll1l_opy_()
                    if not bstack1l1111ll111_opy_:
                        return return_value
                    bstack11llllll1l1_opy_ = next(
                        (
                            instance
                            for instance in bstack1l1111ll111_opy_
                            if TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
                        ),
                        None,
                    )
                    if not bstack11llllll1l1_opy_:
                        return return_value
                    entry = bstack1l1l11lll1l_opy_(TestFramework.bstack1l1111l1ll1_opy_, message, level)
                    self.bstack1l111ll11ll_opy_(bstack11llllll1l1_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack11lllll1111_opy_
    def bstack11llll1ll11_opy_(self):
        def bstack1l111l11111_opy_(*args, **kwargs):
            try:
                self.bstack1l111111111_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1ll1lll_opy_ (u"࠭ࠠࠨᗦ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1ll1lll_opy_ (u"ࠢࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥࠣᗧ") in message:
                    return
                bstack1l1111ll111_opy_ = TestFramework.bstack1l11111ll1l_opy_()
                if not bstack1l1111ll111_opy_:
                    return
                bstack11llllll1l1_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1111ll111_opy_
                        if TestFramework.bstack1ll1l1lll1l_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
                    ),
                    None,
                )
                if not bstack11llllll1l1_opy_:
                    return
                entry = bstack1l1l11lll1l_opy_(TestFramework.bstack1l1111l1ll1_opy_, message, bstack1lll11ll1_opy_.bstack11llllll1ll_opy_)
                self.bstack1l111ll11ll_opy_(bstack11llllll1l1_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111111111_opy_(bstack1ll11l1ll11_opy_ (u"ࠣ࡝ࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠤࡑࡵࡧࠡࡥࡤࡴࡹࡻࡲࡦࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨᗨ"))
                except:
                    pass
        return bstack1l111l11111_opy_
    def bstack1l11111lll1_opy_(self, event: dict, instance=None) -> None:
        global _1l11111llll_opy_
        levels = [bstack1ll1lll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᗩ"), bstack1ll1lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᗪ")]
        bstack1l111l1llll_opy_ = bstack1ll1lll_opy_ (u"ࠦࠧᗫ")
        if instance is not None:
            try:
                bstack1l111l1llll_opy_ = TestFramework.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡵࡪࡦࠣࡪࡷࡵ࡭ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥᗬ").format(e))
        bstack11llll1ll1l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᗭ")]
                bstack1l1111lll1l_opy_ = os.path.join(bstack1l11111l1l1_opy_, (bstack11lllll111l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1111lll1l_opy_):
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡲࡴࡺࠠࡱࡴࡨࡷࡪࡴࡴࠡࡨࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡗࡩࡸࡺࠠࡢࡰࡧࠤࡇࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᗮ").format(bstack1l1111lll1l_opy_))
                    continue
                file_names = os.listdir(bstack1l1111lll1l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1111lll1l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11111llll_opy_:
                        self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᗯ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1111l1l1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1111l1l1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll1lll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᗰ"):
                                entry = bstack1l1l11lll1l_opy_(
                                    kind=bstack1ll1lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᗱ"),
                                    message=bstack1ll1lll_opy_ (u"ࠦࠧᗲ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1111llll1_opy_=file_size,
                                    bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᗳ"),
                                    bstack111lll_opy_=os.path.abspath(file_path),
                                    bstack1lll1l1l1l_opy_=bstack1l111l1llll_opy_
                                )
                            elif level == bstack1ll1lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᗴ"):
                                entry = bstack1l1l11lll1l_opy_(
                                    kind=bstack1ll1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᗵ"),
                                    message=bstack1ll1lll_opy_ (u"ࠣࠤᗶ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1111llll1_opy_=file_size,
                                    bstack1l111l11ll1_opy_=bstack1ll1lll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᗷ"),
                                    bstack111lll_opy_=os.path.abspath(file_path),
                                    bstack1l1111lllll_opy_=bstack1l111l1llll_opy_
                                )
                            bstack11llll1ll1l_opy_.append(entry)
                            _1l11111llll_opy_.add(abs_path)
                        except Exception as bstack11llllll111_opy_:
                            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᗸ").format(bstack11llllll111_opy_))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᗹ").format(e))
        event[bstack1ll1lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᗺ")] = bstack11llll1ll1l_opy_
class bstack11lllll11ll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l111111lll_opy_ = set()
        kwargs[bstack1ll1lll_opy_ (u"ࠨࡳ࡬࡫ࡳ࡯ࡪࡿࡳࠣᗻ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1111111l1_opy_(obj, self.bstack1l111111lll_opy_)
def bstack1l111l1111l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1111111l1_opy_(obj, bstack1l111111lll_opy_=None, max_depth=3):
    if bstack1l111111lll_opy_ is None:
        bstack1l111111lll_opy_ = set()
    if id(obj) in bstack1l111111lll_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l111111lll_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111ll111l_opy_ = TestFramework.bstack1l111l11lll_opy_(obj)
    bstack1l111l111ll_opy_ = next((k.lower() in bstack1l111ll111l_opy_.lower() for k in bstack1l111ll11l1_opy_.keys()), None)
    if bstack1l111l111ll_opy_:
        obj = TestFramework.bstack1l1111lll11_opy_(obj, bstack1l111ll11l1_opy_[bstack1l111l111ll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll1lll_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥᗼ")):
            keys = getattr(obj, bstack1ll1lll_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦᗽ"), [])
        elif hasattr(obj, bstack1ll1lll_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦᗾ")):
            keys = getattr(obj, bstack1ll1lll_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧᗿ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll1lll_opy_ (u"ࠦࡤࠨᘀ"))}
        if not obj and bstack1l111ll111l_opy_ == bstack1ll1lll_opy_ (u"ࠧࡶࡡࡵࡪ࡯࡭ࡧ࠴ࡐࡰࡵ࡬ࡼࡕࡧࡴࡩࠤᘁ"):
            obj = {bstack1ll1lll_opy_ (u"ࠨࡰࡢࡶ࡫ࠦᘂ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111l1111l_opy_(key) or str(key).startswith(bstack1ll1lll_opy_ (u"ࠢࡠࠤᘃ")):
            continue
        if value is not None and bstack1l111l1111l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1111111l1_opy_(value, bstack1l111111lll_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1111111l1_opy_(o, bstack1l111111lll_opy_, max_depth) for o in value]))
    return result or None