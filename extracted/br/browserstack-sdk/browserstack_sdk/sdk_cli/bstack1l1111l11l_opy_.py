# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import bstack1ll111lllll_opy_, bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l111_opy_ import bstack1l1l1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1l111l1_opy_, TestHookState, bstack1l1l1l1lll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l111l1111_opy_, bstack1l11111l11l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l111l1111l_opy_ = [bstack1ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᖑ"), bstack1ll11_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᖒ"), bstack1ll11_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢᖓ"), bstack1ll11_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࠤᖔ"), bstack1ll11_opy_ (u"ࠤࡳࡥࡹ࡮ࠢᖕ")]
bstack11llll1l1ll_opy_ = bstack1l11111l11l_opy_()
bstack11lllll1l1l_opy_ = bstack1ll11_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᖖ")
bstack11llllllll1_opy_ = {
    bstack1ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡎࡺࡥ࡮ࠤᖗ"): bstack1l111l1111l_opy_,
    bstack1ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡖࡡࡤ࡭ࡤ࡫ࡪࠨᖘ"): bstack1l111l1111l_opy_,
    bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡍࡰࡦࡸࡰࡪࠨᖙ"): bstack1l111l1111l_opy_,
    bstack1ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡄ࡮ࡤࡷࡸࠨᖚ"): bstack1l111l1111l_opy_,
    bstack1ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡈࡸࡲࡨࡺࡩࡰࡰࠥᖛ"): bstack1l111l1111l_opy_
    + [
        bstack1ll11_opy_ (u"ࠤࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡲࡦࡳࡥࠣᖜ"),
        bstack1ll11_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᖝ"),
        bstack1ll11_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩ࡮ࡴࡦࡰࠤᖞ"),
        bstack1ll11_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢᖟ"),
        bstack1ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠣᖠ"),
        bstack1ll11_opy_ (u"ࠢࡤࡣ࡯ࡰࡴࡨࡪࠣᖡ"),
        bstack1ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢᖢ"),
        bstack1ll11_opy_ (u"ࠤࡶࡸࡴࡶࠢᖣ"),
        bstack1ll11_opy_ (u"ࠥࡨࡺࡸࡡࡵ࡫ࡲࡲࠧᖤ"),
        bstack1ll11_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᖥ"),
    ],
    bstack1ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡪࡰ࠱ࡗࡪࡹࡳࡪࡱࡱࠦᖦ"): [bstack1ll11_opy_ (u"ࠨࡳࡵࡣࡵࡸࡵࡧࡴࡩࠤᖧ"), bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡸ࡬ࡡࡪ࡮ࡨࡨࠧᖨ"), bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡹࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤᖩ"), bstack1ll11_opy_ (u"ࠤ࡬ࡸࡪࡳࡳࠣᖪ")],
    bstack1ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡧࡴࡴࡦࡪࡩ࠱ࡇࡴࡴࡦࡪࡩࠥᖫ"): [bstack1ll11_opy_ (u"ࠦ࡮ࡴࡶࡰࡥࡤࡸ࡮ࡵ࡮ࡠࡲࡤࡶࡦࡳࡳࠣᖬ"), bstack1ll11_opy_ (u"ࠧࡧࡲࡨࡵࠥᖭ")],
    bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡈ࡬ࡼࡹࡻࡲࡦࡆࡨࡪࠧᖮ"): [bstack1ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᖯ"), bstack1ll11_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤᖰ"), bstack1ll11_opy_ (u"ࠤࡩࡹࡳࡩࠢᖱ"), bstack1ll11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᖲ"), bstack1ll11_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨᖳ"), bstack1ll11_opy_ (u"ࠧ࡯ࡤࡴࠤᖴ")],
    bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡕࡸࡦࡗ࡫ࡱࡶࡧࡶࡸࠧᖵ"): [bstack1ll11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧᖶ"), bstack1ll11_opy_ (u"ࠣࡲࡤࡶࡦࡳࠢᖷ"), bstack1ll11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡠ࡫ࡱࡨࡪࡾࠢᖸ")],
    bstack1ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡶࡺࡴ࡮ࡦࡴ࠱ࡇࡦࡲ࡬ࡊࡰࡩࡳࠧᖹ"): [bstack1ll11_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᖺ"), bstack1ll11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࠧᖻ")],
    bstack1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡐࡲࡨࡪࡑࡥࡺࡹࡲࡶࡩࡹࠢᖼ"): [bstack1ll11_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᖽ"), bstack1ll11_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᖾ")],
    bstack1ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡒࡧࡲ࡬ࠤᖿ"): [bstack1ll11_opy_ (u"ࠥࡲࡦࡳࡥࠣᗀ"), bstack1ll11_opy_ (u"ࠦࡦࡸࡧࡴࠤᗁ"), bstack1ll11_opy_ (u"ࠧࡱࡷࡢࡴࡪࡷࠧᗂ")],
}
_1l1111111l1_opy_ = set()
class bstack1l11l111l_opy_(bstack1ll111l11ll_opy_):
    bstack11lllllll11_opy_ = bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࠨᗃ")
    bstack1l1111l11ll_opy_ = bstack1ll11_opy_ (u"ࠢࡊࡐࡉࡓࠧᗄ")
    bstack1l1111lllll_opy_ = bstack1ll11_opy_ (u"ࠣࡇࡕࡖࡔࡘࠢᗅ")
    bstack1l111l1l111_opy_: Callable
    bstack11llllll1l1_opy_: Callable
    def __init__(self, bstack1l1l11ll1l1_opy_, bstack1l1l1l1ll11_opy_):
        super().__init__()
        self.bstack1l11ll111ll_opy_ = bstack1l1l1l1ll11_opy_
        if os.getenv(bstack1ll11_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡑ࠴࠵࡞ࠨᗆ"), bstack1ll11_opy_ (u"ࠥ࠵ࠧᗇ")) != bstack1ll11_opy_ (u"ࠦ࠶ࠨᗈ") or not self.is_enabled():
            return
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11llll1ll_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1l111_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l11lll1lll_opy_((event, state), self.bstack1l111111l11_opy_)
        bstack1l1l11ll1l1_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.POST), self.bstack1l111111111_opy_)
        self.bstack1l111l1l111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l111l1lll1_opy_(bstack1l11l111l_opy_.bstack1l1111l11ll_opy_, self.bstack1l111l1l111_opy_)
        self.bstack11llllll1l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l111l1lll1_opy_(bstack1l11l111l_opy_.bstack1l1111lllll_opy_, self.bstack11llllll1l1_opy_)
        self.bstack1l111l11lll_opy_ = builtins.print
        builtins.print = self.bstack1l1111ll1ll_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l111111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l111l1l11l_opy_() or f.bstack11lllllll1l_opy_()) and instance:
            bstack1l111111ll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll11l11lll_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack11l111ll1_opy_ = datetime.now()
                entries = f.bstack1l1111l1l1l_opy_(instance, bstack1ll11l11lll_opy_)
                if entries:
                    self.bstack11llllll1ll_opy_(instance, entries)
                    instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࠧᗉ"), datetime.now() - bstack11l111ll1_opy_)
                    f.bstack1l1111llll1_opy_(instance, bstack1ll11l11lll_opy_)
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᗊ"), datetime.now() - bstack1l111111ll1_opy_)
                return # bstack1l111l1l1ll_opy_ not send this event with the bstack1l111l1ll1l_opy_ bstack11lllll111l_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l111l1l1l1_opy_)
            ):
                f.bstack1l11lllll_opy_(instance, bstack1l11l111l_opy_.bstack11lllllll11_opy_, True)
                return # bstack1l111l1l1ll_opy_ not send this event bstack1l1111lll11_opy_ bstack1l111l111l1_opy_
            elif (
                f.bstack1ll1ll1l1l1_opy_(instance, bstack1l11l111l_opy_.bstack11lllllll11_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l111l1l1l1_opy_)
            ):
                self.bstack1l111111l11_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack11l111ll1_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l111l1l11l_opy_():
                bstack11lllll11ll_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᗋ"), None), data.pop(bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᗌ"), {}).values()),
                    key=lambda x: x[bstack1ll11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᗍ")],
                )
                data.update({bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᗎ"): bstack11lllll11ll_opy_})
            elif f.bstack11lllllll1l_opy_():
                bstack1l11111111l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᗏ"), None), data.pop(bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᗐ"), {}).values()),
                    key=lambda x: x[bstack1ll11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᗑ")],
                )
                data.update({bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡱࡥࡺࡹࡲࡶࡩࡹࠢᗒ"): bstack1l11111111l_opy_})
            if bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_ in data:
                data.pop(bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_)
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣ࡬ࡶࡳࡳࡀࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᗓ"), datetime.now() - bstack11l111ll1_opy_)
            bstack11l111ll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11111l1l1_opy_)
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᗔ"), datetime.now() - bstack11l111ll1_opy_)
            if TestFramework.bstack1l11l1lll11_opy_ in data:
                self.bstack11lllll111l_opy_(instance, bstack1ll11l11lll_opy_, event_json=event_json)
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᗕ"), datetime.now() - bstack1l111111ll1_opy_)
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
        bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11ll1111l_opy_.value)
        self.bstack1l11ll111ll_opy_.bstack1l11111l1ll_opy_(instance, f, bstack1ll11l11lll_opy_, *args, **kwargs)
        try:
            req = self.bstack1l11ll111ll_opy_.bstack1l111ll11ll_opy_(instance, f, bstack1ll11l11lll_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸࠥ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿࡛ࠦࡼࡿࡠࠤࢀࢃ࡜࡯ࡽࢀࠦᗖ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack11lllll1l11_opy_ data not ready for robot-playwright at the time of bstack1l11llll1ll_opy_, so bstack1l111ll11l1_opy_ will send bstack11lllll1l11_opy_ event in bstack1l11ll1l111_opy_ for robot-playwright
            self.bstack1l1111111ll_opy_(f, instance, req)
        bstack11ll11l1ll_opy_.end(EVENTS.bstack11ll1111l_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᗗ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᗘ"), status=True, failure=None, test_name=None)
    def bstack1l11ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1ll1l1l1_opy_(instance, self.bstack1l11ll111ll_opy_.bstack1l111l11ll1_opy_, False):
            try:
                req = self.bstack1l11ll111ll_opy_.bstack1l111ll11ll_opy_(instance, f, bstack1ll11l11lll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺࠠࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡝ࡾࢁࡢࠦࡻࡾ࡞ࡱࡿࢂࠨᗙ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l1111111ll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack11llllll11l_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l1111111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹࠦࡧࡓࡒࡆࠤࡨࡧ࡬࡭࠼ࠣࡒࡴࠦࡶࡢ࡮࡬ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠦᗚ"))
            return
        bstack11l111ll1_opy_ = datetime.now()
        try:
            r = self.bstack1l1ll1ll111_opy_.TestSessionEvent(req)
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡪࡼࡥ࡯ࡶࠥᗛ"), datetime.now() - bstack11l111ll1_opy_)
            f.bstack1l11lllll_opy_(instance, self.bstack1l11ll111ll_opy_.bstack1l111l11ll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᗜ") + str(r) + bstack1ll11_opy_ (u"ࠦࠧᗝ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᗞ") + str(e) + bstack1ll11_opy_ (u"ࠨࠢᗟ"))
            traceback.print_exc()
            raise e
    def bstack1l111111111_opy_(
        self,
        f: bstack1ll11111111_opy_,
        _driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        _1l11111llll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll11111111_opy_.bstack1l11l1l1lll_opy_(method_name):
            return
        if f.bstack1l1l111ll11_opy_(*args) == bstack1ll11111111_opy_.bstack11llll1ll11_opy_:
            bstack1l111111ll1_opy_ = datetime.now()
            screenshot = result.get(bstack1ll11_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨᗠ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll11_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡩ࡮ࡣࡪࡩࠥࡨࡡࡴࡧ࠹࠸ࠥࡹࡴࡳࠤᗡ"))
                return
            bstack1l1111ll11l_opy_ = self.bstack1l111111l1l_opy_(instance)
            if bstack1l1111ll11l_opy_:
                entry = bstack1l1l1l1lll1_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack11llllll1ll_opy_(bstack1l1111ll11l_opy_, [entry])
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡨࡼࡪࡩࡵࡵࡧࠥᗢ"), datetime.now() - bstack1l111111ll1_opy_)
            else:
                self.logger.warning(bstack1ll11_opy_ (u"ࠥࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷࡩࡸࡺࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸ࡭࡯ࡳࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡽࡡࡴࠢࡷࡥࡰ࡫࡮ࠡࡤࡼࠤࡩࡸࡩࡷࡧࡵࡁࠥࢁࡽࠣᗣ").format(instance.ref()))
        event = {}
        bstack1l1111ll11l_opy_ = self.bstack1l111111l1l_opy_(instance)
        if bstack1l1111ll11l_opy_:
            self.bstack11llll1l1l1_opy_(event, bstack1l1111ll11l_opy_)
            if event.get(bstack1ll11_opy_ (u"ࠦࡱࡵࡧࡴࠤᗤ")):
                self.bstack11llllll1ll_opy_(bstack1l1111ll11l_opy_, event[bstack1ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᗥ")])
            else:
                self.logger.debug(bstack1ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡲ࡯ࡨࡵࠣࡪࡴࡸࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡪࡼࡥ࡯ࡶࠥᗦ"))
    @measure(event_name=EVENTS.bstack1l1111l1111_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11llllll1ll_opy_(
        self,
        bstack1l1111ll11l_opy_: bstack1l1l1l111l1_opy_,
        entries: List[bstack1l1l1l1lll1_opy_],
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11llll11l_opy_)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᗧ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111ll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111ll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111ll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11l11llll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11111lll1_opy_)
            log_entry.uuid = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack1l11l1lll11_opy_)
            log_entry.test_framework_state = bstack1l1111ll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᗨ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᗩ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11llll1lll1_opy_
                log_entry.file_path = entry.bstack1l11ll_opy_
        def bstack1l111l1llll_opy_():
            bstack11l111ll1_opy_ = datetime.now()
            try:
                self.bstack1l1ll1ll111_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l1111ll11l_opy_.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᗪ"), datetime.now() - bstack11l111ll1_opy_)
                elif entry.kind == TestFramework.bstack11llll1llll_opy_:
                    bstack1l1111ll11l_opy_.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᗫ"), datetime.now() - bstack11l111ll1_opy_)
                else:
                    bstack1l1111ll11l_opy_.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤᗬ"), datetime.now() - bstack11l111ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᗭ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll11llll11_opy_.enqueue(bstack1l111l1llll_opy_)
    @measure(event_name=EVENTS.bstack1l1111l1l11_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack11lllll111l_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
        req.client_worker_id = bstack1ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᗮ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l11llll_opy_)
        req.test_framework_version = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11111lll1_opy_)
        req.test_framework_state = bstack1ll11l11lll_opy_[0].name
        req.test_hook_state = bstack1ll11l11lll_opy_[1].name
        started_at = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l111ll1111_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack11lllll1lll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11111l1l1_opy_)).encode(bstack1ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᗯ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l111l1llll_opy_():
            bstack11l111ll1_opy_ = datetime.now()
            try:
                self.bstack1l1ll1ll111_opy_.TestFrameworkEvent(req)
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧᗰ"), datetime.now() - bstack11l111ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᗱ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll11llll11_opy_.enqueue(bstack1l111l1llll_opy_)
    def bstack1l111111l1l_opy_(self, instance: bstack1ll111lllll_opy_):
        bstack1l11111ll11_opy_ = TestFramework.bstack1ll11lll1ll_opy_(instance.context)
        for t in bstack1l11111ll11_opy_:
            bstack11lllll11l1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(t, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
            if not bstack1l111l1111_opy_() and len(bstack11lllll11l1_opy_) == 0:
                bstack11lllll11l1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(t, bstack1l1l1l11ll1_opy_.bstack1l1111ll111_opy_, [])
            if any(instance is d[1] for d in bstack11lllll11l1_opy_):
                return t
    def bstack11llllll111_opy_(self, message):
        self.bstack1l111l1l111_opy_(message + bstack1ll11_opy_ (u"ࠦࡡࡴࠢᗲ"))
    def log_error(self, message):
        self.bstack11llllll1l1_opy_(message + bstack1ll11_opy_ (u"ࠧࡢ࡮ࠣᗳ"))
    def bstack1l111l1lll1_opy_(self, level, original_func):
        def bstack1l111111lll_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1ll11_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢᗴ") in message or bstack1ll11_opy_ (u"ࠢ࡜ࡕࡇࡏࡈࡒࡉ࡞ࠤᗵ") in message or bstack1ll11_opy_ (u"ࠣ࡝࡚ࡩࡧࡊࡲࡪࡸࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠧᗶ") in message:
                        return return_value
                    bstack1l11111ll11_opy_ = TestFramework.bstack1l1111l111l_opy_()
                    if not bstack1l11111ll11_opy_:
                        return return_value
                    bstack1l1111ll11l_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11111ll11_opy_
                            if TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
                        ),
                        None,
                    )
                    if not bstack1l1111ll11l_opy_:
                        return return_value
                    entry = bstack1l1l1l1lll1_opy_(TestFramework.bstack11lllllllll_opy_, message, level)
                    self.bstack11llllll1ll_opy_(bstack1l1111ll11l_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l111111lll_opy_
    def bstack1l1111ll1ll_opy_(self):
        def bstack1l11111ll1l_opy_(*args, **kwargs):
            try:
                self.bstack1l111l11lll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1ll11_opy_ (u"ࠩࠣࠫᗷ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1ll11_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦᗸ") in message:
                    return
                bstack1l11111ll11_opy_ = TestFramework.bstack1l1111l111l_opy_()
                if not bstack1l11111ll11_opy_:
                    return
                bstack1l1111ll11l_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11111ll11_opy_
                        if TestFramework.bstack1ll1ll11111_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
                    ),
                    None,
                )
                if not bstack1l1111ll11l_opy_:
                    return
                entry = bstack1l1l1l1lll1_opy_(TestFramework.bstack11lllllllll_opy_, message, bstack1l11l111l_opy_.bstack1l1111l11ll_opy_)
                self.bstack11llllll1ll_opy_(bstack1l1111ll11l_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111l11lll_opy_(bstack1ll11l1ll11_opy_ (u"ࠦࡠࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࡣࠠࡍࡱࡪࠤࡨࡧࡰࡵࡷࡵࡩࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤᗹ"))
                except:
                    pass
        return bstack1l11111ll1l_opy_
    def bstack11llll1l1l1_opy_(self, event: dict, instance=None) -> None:
        global _1l1111111l1_opy_
        levels = [bstack1ll11_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᗺ"), bstack1ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᗻ")]
        bstack1l1111lll1l_opy_ = bstack1ll11_opy_ (u"ࠢࠣᗼ")
        if instance is not None:
            try:
                bstack1l1111lll1l_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡸ࡭ࡩࠦࡦࡳࡱࡰࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨᗽ").format(e))
        bstack1l1111l1lll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᗾ")]
                bstack1l111l111ll_opy_ = os.path.join(bstack11llll1l1ll_opy_, (bstack11lllll1l1l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l111l111ll_opy_):
                    self.logger.debug(bstack1ll11_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡮ࡰࡶࠣࡴࡷ࡫ࡳࡦࡰࡷࠤ࡫ࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡚ࠥࡥࡴࡶࠣࡥࡳࡪࠠࡃࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨᗿ").format(bstack1l111l111ll_opy_))
                    continue
                file_names = os.listdir(bstack1l111l111ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l111l111ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1111111l1_opy_:
                        self.logger.info(bstack1ll11_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᘀ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack11llll1ll1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack11llll1ll1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll11_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᘁ"):
                                entry = bstack1l1l1l1lll1_opy_(
                                    kind=bstack1ll11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᘂ"),
                                    message=bstack1ll11_opy_ (u"ࠢࠣᘃ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11llll1lll1_opy_=file_size,
                                    bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᘄ"),
                                    bstack1l11ll_opy_=os.path.abspath(file_path),
                                    bstack1l11ll111l_opy_=bstack1l1111lll1l_opy_
                                )
                            elif level == bstack1ll11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᘅ"):
                                entry = bstack1l1l1l1lll1_opy_(
                                    kind=bstack1ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᘆ"),
                                    message=bstack1ll11_opy_ (u"ࠦࠧᘇ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11llll1lll1_opy_=file_size,
                                    bstack1l11111l111_opy_=bstack1ll11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᘈ"),
                                    bstack1l11ll_opy_=os.path.abspath(file_path),
                                    bstack1l111l1ll11_opy_=bstack1l1111lll1l_opy_
                                )
                            bstack1l1111l1lll_opy_.append(entry)
                            _1l1111111l1_opy_.add(abs_path)
                        except Exception as bstack1l1111l1ll1_opy_:
                            self.logger.error(bstack1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᘉ").format(bstack1l1111l1ll1_opy_))
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨᘊ").format(e))
        event[bstack1ll11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᘋ")] = bstack1l1111l1lll_opy_
class bstack1l11111l1l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11lllll1ll1_opy_ = set()
        kwargs[bstack1ll11_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦᘌ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack11lllll1111_opy_(obj, self.bstack11lllll1ll1_opy_)
def bstack1l1111l11l1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack11lllll1111_opy_(obj, bstack11lllll1ll1_opy_=None, max_depth=3):
    if bstack11lllll1ll1_opy_ is None:
        bstack11lllll1ll1_opy_ = set()
    if id(obj) in bstack11lllll1ll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11lllll1ll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111l11111_opy_ = TestFramework.bstack1l111l11l11_opy_(obj)
    bstack1l111ll111l_opy_ = next((k.lower() in bstack1l111l11111_opy_.lower() for k in bstack11llllllll1_opy_.keys()), None)
    if bstack1l111ll111l_opy_:
        obj = TestFramework.bstack1l111l11l1l_opy_(obj, bstack11llllllll1_opy_[bstack1l111ll111l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll11_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᘍ")):
            keys = getattr(obj, bstack1ll11_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢᘎ"), [])
        elif hasattr(obj, bstack1ll11_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᘏ")):
            keys = getattr(obj, bstack1ll11_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᘐ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll11_opy_ (u"ࠢࡠࠤᘑ"))}
        if not obj and bstack1l111l11111_opy_ == bstack1ll11_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧᘒ"):
            obj = {bstack1ll11_opy_ (u"ࠤࡳࡥࡹ࡮ࠢᘓ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1111l11l1_opy_(key) or str(key).startswith(bstack1ll11_opy_ (u"ࠥࡣࠧᘔ")):
            continue
        if value is not None and bstack1l1111l11l1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack11lllll1111_opy_(value, bstack11lllll1ll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack11lllll1111_opy_(o, bstack11lllll1ll1_opy_, max_depth) for o in value]))
    return result or None